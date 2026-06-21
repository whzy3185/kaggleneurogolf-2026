"""Summarize public high-rank Orbit Wars replay parquet files.

The script expects the lightweight parquet subset from
``nbridelancetb/orbit-wars-replay-parquet`` and writes CSV/JSON summaries under
``outputs/``.  It intentionally avoids loading ``planet_state.parquet`` so it
can run quickly on the local workspace.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


DEFAULT_PLAYERS = [
    "Isaiah @ Tufa Labs",
    "Jake Will",
    "Vadasz",
    "Audun Ljone Henriksen",
    "typeIIIfairy",
    "3Comets",
    "bowwowforeach",
    "TonyK",
    "Erfan Eshratifar",
]


def read_parquet(root: Path, name: str) -> pd.DataFrame:
    path = root / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"missing parquet file: {path}")
    return pd.read_parquet(path)


def summarize_players(player_episodes: pd.DataFrame, episodes: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    players = player_episodes.merge(
        episodes[["episode_id", "n_players"]],
        on="episode_id",
        how="left",
    )

    overall = (
        players.groupby("name", dropna=False)
        .agg(
            games=("episode_id", "count"),
            wins=("is_winner", "sum"),
            avg_reward=("reward", "mean"),
        )
        .reset_index()
    )
    overall["winrate"] = overall["wins"] / overall["games"]
    overall = overall.sort_values(["games", "winrate"], ascending=[False, False])

    by_mode = (
        players.groupby(["name", "n_players"], dropna=False)
        .agg(
            games=("episode_id", "count"),
            wins=("is_winner", "sum"),
            avg_reward=("reward", "mean"),
        )
        .reset_index()
    )
    by_mode["winrate"] = by_mode["wins"] / by_mode["games"]
    by_mode = by_mode.sort_values(["name", "n_players"])
    return overall, by_mode


def phase_snapshots(
    tick_summary: pd.DataFrame,
    player_episodes: pd.DataFrame,
    episodes: pd.DataFrame,
    target_players: list[str],
) -> pd.DataFrame:
    snapshots = tick_summary[tick_summary["tick"].isin([20, 50, 100, 150, 200, 300])].copy()
    snapshots = snapshots.merge(
        episodes[["episode_id", "n_players", "winner_slot"]],
        on="episode_id",
        how="left",
    )
    snapshots = snapshots.merge(
        player_episodes[["episode_id", "slot", "name", "is_winner"]],
        on=["episode_id", "slot"],
        how="left",
    )

    rows: list[dict] = []

    def add_group(frame: pd.DataFrame, group_name: str) -> None:
        if frame.empty:
            return
        grouped = frame.groupby(["tick", "n_players"], dropna=False)
        for (tick, n_players), g in grouped:
            rows.append(
                {
                    "group": group_name,
                    "tick": int(tick),
                    "n_players": int(n_players),
                    "n": int(len(g)),
                    "avg_prod": round(float(g["production"].mean()), 3),
                    "avg_planets": round(float(g["n_planets"].mean()), 3),
                    "avg_ships": round(float(g["total_ships"].mean()), 3),
                    "avg_fleets": round(float(g["n_fleets"].mean()), 3),
                    "winrate": round(float(g["is_winner"].mean()), 3),
                }
            )

    add_group(snapshots[snapshots["is_winner"] == 1], "all_winners")
    add_group(snapshots[snapshots["is_winner"] == 0], "all_non_winners")
    add_group(snapshots[snapshots["name"].isin(target_players)], "target_players")
    for player in target_players:
        add_group(snapshots[snapshots["name"] == player], player)

    return pd.DataFrame(rows).sort_values(["group", "tick", "n_players"])


def action_phase_summary(actions: pd.DataFrame, episodes: pd.DataFrame, player_episodes: pd.DataFrame, planets: pd.DataFrame) -> pd.DataFrame:
    actions = actions.copy()
    actions["phase"] = pd.cut(
        actions["tick"],
        bins=[-1, 50, 150, 300, 500],
        labels=["opening_0_50", "mid_50_150", "late_mid_150_300", "end_300_500"],
    )
    actions = actions.merge(episodes[["episode_id", "n_players", "winner_slot"]], on="episode_id", how="left")
    actions = actions.merge(player_episodes[["episode_id", "slot", "name", "is_winner"]], on=["episode_id", "slot"], how="left")
    source_meta = planets[["episode_id", "planet_id", "production", "orbit_radius", "is_comet"]].rename(
        columns={
            "planet_id": "src_planet_id",
            "production": "src_production",
            "orbit_radius": "src_orbit_radius",
            "is_comet": "src_is_comet",
        }
    )
    actions = actions.merge(source_meta, on=["episode_id", "src_planet_id"], how="left")
    actions["high_prod_source"] = actions["src_production"].fillna(0) >= 3
    actions["static_inner_source"] = actions["src_orbit_radius"].fillna(9999) <= 45

    rows: list[dict] = []
    for group_name, group_frame in [
        ("all_winners", actions[actions["is_winner"] == 1]),
        ("all_non_winners", actions[actions["is_winner"] == 0]),
        ("target_players", actions[actions["name"].isin(DEFAULT_PLAYERS)]),
    ]:
        if group_frame.empty:
            continue
        for (n_players, phase), g in group_frame.groupby(["n_players", "phase"], observed=True):
            rows.append(
                {
                    "group": group_name,
                    "n_players": int(n_players),
                    "phase": str(phase),
                    "actions": int(len(g)),
                    "avg_ship_per_action": round(float(g["n_ships"].mean()), 3),
                    "median_ship_per_action": round(float(g["n_ships"].median()), 3),
                    "high_prod_source_rate": round(float(g["high_prod_source"].mean()), 3),
                    "inner_source_rate": round(float(g["static_inner_source"].mean()), 3),
                }
            )

    return pd.DataFrame(rows).sort_values(["group", "n_players", "phase"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="external/datasets/replay_parquet")
    parser.add_argument("--output-dir", default="outputs/high_rank_strategy_20260621")
    parser.add_argument("--players", nargs="*", default=DEFAULT_PLAYERS)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    episodes = read_parquet(input_dir, "episodes")
    player_episodes = read_parquet(input_dir, "player_episodes")
    tick_summary = read_parquet(input_dir, "tick_summary")
    actions = read_parquet(input_dir, "actions")
    planets = read_parquet(input_dir, "episode_planets")

    overall, by_mode = summarize_players(player_episodes, episodes)
    snapshots = phase_snapshots(tick_summary, player_episodes, episodes, args.players)
    action_summary = action_phase_summary(actions, episodes, player_episodes, planets)

    overall.to_csv(output_dir / "player_overall_summary.csv", index=False)
    by_mode.to_csv(output_dir / "player_mode_summary.csv", index=False)
    snapshots.to_csv(output_dir / "phase_snapshots.csv", index=False)
    action_summary.to_csv(output_dir / "action_phase_summary.csv", index=False)

    summary = {
        "dataset": "nbridelancetb/orbit-wars-replay-parquet",
        "episodes": int(len(episodes)),
        "player_rows": int(len(player_episodes)),
        "actions": int(len(actions)),
        "mode_counts": {str(k): int(v) for k, v in episodes["n_players"].value_counts().sort_index().items()},
        "top_overall_by_games": overall.head(12).to_dict(orient="records"),
        "target_players": args.players,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
