from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orbitwars_eval.loader import DEFAULT_ZOO, resolve_agents  # noqa: E402
from orbitwars_agent.candidate_loader import load_candidate  # noqa: E402

logging.getLogger("kaggle_environments").setLevel(logging.ERROR)
logging.getLogger("kaggle_environments.envs.open_spiel_env.open_spiel_env").setLevel(logging.ERROR)

PHASE_SNAPSHOT_STEPS = [20, 50, 100, 150, 200]

FIELDNAMES = [
    "series",
    "match_id",
    "seed",
    "player_count",
    "agent_0",
    "agent_1",
    "agent_2",
    "agent_3",
    "winner",
    "winner_index",
    "status",
    "turns",
    "duration_s",
    "scores",
    "score_0",
    "score_1",
    "score_2",
    "score_3",
    "rank_0",
    "rank_1",
    "rank_2",
    "rank_3",
    "snapshot_20",
    "snapshot_50",
    "snapshot_100",
    "snapshot_150",
    "snapshot_200",
    "error",
]


def _parse_seeds(raw: str) -> list[int]:
    raw = raw.strip()
    if not raw:
        return [1]
    if "-" in raw and "," not in raw:
        start, end = raw.split("-", 1)
        return list(range(int(start), int(end) + 1))
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def _clear_adaptive_module() -> None:
    for name in list(sys.modules):
        if name == "orbitwars_agent.adaptive_agent":
            del sys.modules[name]


def _load_agent(agent_dir: Path):
    _clear_adaptive_module()
    return load_candidate(agent_dir).agent


def _extract_outcome(replay: dict[str, Any], agent_ids: list[str]) -> tuple[str | None, int | None, list[int], int, str]:
    steps = replay.get("steps") or []
    if not steps:
        return None, None, [], 0, "crashed"
    final_step = steps[-1]
    if not final_step:
        return None, None, [], 0, "crashed"

    rewards = [state.get("reward") for state in final_step]
    winner_indexes = [i for i, reward in enumerate(rewards) if reward == 1]
    winner_index = winner_indexes[0] if len(winner_indexes) == 1 else None
    winner = agent_ids[winner_index] if winner_index is not None else None

    num_players = len(agent_ids)
    scores = [0] * num_players
    observation = final_step[0].get("observation", {})
    for planet in observation.get("planets", []):
        owner = planet[1] if len(planet) > 1 else -1
        ships = planet[5] if len(planet) > 5 else 0
        if 0 <= owner < num_players:
            scores[owner] += int(ships)
    for fleet in observation.get("fleets", []):
        owner = fleet[1] if len(fleet) > 1 else -1
        ships = fleet[6] if len(fleet) > 6 else 0
        if 0 <= owner < num_players:
            scores[owner] += int(ships)

    statuses = [state.get("status") for state in final_step]
    if "ERROR" in statuses:
        status = "crashed"
    elif "TIMEOUT" in statuses:
        status = "timeout"
    elif "INVALID" in statuses:
        status = "invalid_action"
    elif winner is None:
        status = "draw"
    else:
        status = "ok"

    return winner, winner_index, scores, len(steps), status


def _ranks(scores: list[int]) -> list[int]:
    ordered = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
    ranks = [0] * len(scores)
    previous_score = None
    previous_rank = 0
    for idx, (player_idx, score) in enumerate(ordered, start=1):
        rank = previous_rank if score == previous_score else idx
        ranks[player_idx] = rank
        previous_rank = rank
        previous_score = score
    return ranks


def _phase_snapshots(replay: dict[str, Any], player_count: int) -> dict[int, list[dict[str, Any]]]:
    steps = replay.get("steps") or []
    snapshots: dict[int, list[dict[str, Any]]] = {}
    if not steps:
        return snapshots
    for requested_step in PHASE_SNAPSHOT_STEPS:
        step_index = min(int(requested_step), max(0, len(steps) - 1))
        step_states = steps[step_index] or []
        observation = (step_states[0].get("observation", {}) if step_states else {}) or {}
        prod = [0.0] * int(player_count)
        planets = [0] * int(player_count)
        ships = [0.0] * int(player_count)
        for planet in observation.get("planets", []):
            owner = planet[1] if len(planet) > 1 else -1
            planet_ships = planet[5] if len(planet) > 5 else 0
            production = planet[6] if len(planet) > 6 else 0
            if 0 <= owner < int(player_count):
                planets[owner] += 1
                ships[owner] += float(planet_ships)
                prod[owner] += float(production)
        for fleet in observation.get("fleets", []):
            owner = fleet[1] if len(fleet) > 1 else -1
            fleet_ships = fleet[6] if len(fleet) > 6 else 0
            if 0 <= owner < int(player_count):
                ships[owner] += float(fleet_ships)

        prod_ranks = _ranks([int(value) for value in prod])
        max_prod = max(prod) if prod else 0.0
        snapshots[int(requested_step)] = [
            {
                "actual_step": int(step_index),
                "prod": round(float(prod[idx]), 4),
                "prod_gap": round(float(prod[idx] - max_prod), 4),
                "prod_rank": int(prod_ranks[idx]) if idx < len(prod_ranks) else "",
                "planets": int(planets[idx]),
                "ships": round(float(ships[idx]), 4),
            }
            for idx in range(int(player_count))
        ]
    return snapshots


def _run_match(agent_ids: list[str], *, seed: int, match_id: int, series: str) -> dict[str, Any]:
    from kaggle_environments import make

    refs = resolve_agents(agent_ids, zoo_root=DEFAULT_ZOO)
    start = time.monotonic()
    try:
        callables = [_load_agent(ref.path) for ref in refs]
        env = make("orbit_wars", configuration={"randomSeed": int(seed)}, debug=False)
        env.run(callables)
        duration_s = time.monotonic() - start
        replay = env.toJSON()
        winner, winner_index, scores, turns, status = _extract_outcome(replay, agent_ids)
        snapshots = _phase_snapshots(replay, len(agent_ids))
        error = ""
    except Exception as exc:
        duration_s = time.monotonic() - start
        winner = None
        winner_index = None
        scores = []
        turns = 0
        status = "crashed"
        snapshots = {}
        error = f"{type(exc).__name__}: {exc}"

    ranks = _ranks(scores) if scores else []
    row: dict[str, Any] = {
        "series": series,
        "match_id": match_id,
        "seed": seed,
        "player_count": len(agent_ids),
        "winner": winner or "",
        "winner_index": "" if winner_index is None else winner_index,
        "status": status,
        "turns": turns,
        "duration_s": round(duration_s, 4),
        "scores": json.dumps(scores, separators=(",", ":")),
        "error": error,
    }
    for idx in range(4):
        row[f"agent_{idx}"] = agent_ids[idx] if idx < len(agent_ids) else ""
        row[f"score_{idx}"] = scores[idx] if idx < len(scores) else ""
        row[f"rank_{idx}"] = ranks[idx] if idx < len(ranks) else ""
    for snapshot_step in PHASE_SNAPSHOT_STEPS:
        row[f"snapshot_{snapshot_step}"] = json.dumps(
            snapshots.get(snapshot_step, []),
            separators=(",", ":"),
        )
    return row


def _write_row(writer: csv.DictWriter, row: dict[str, Any], handle) -> None:
    writer.writerow(row)
    handle.flush()


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    stats = defaultdict(
        lambda: {
            "games": 0,
            "wins": 0,
            "draws": 0,
            "errors": 0,
            "avg_rank_sum": 0.0,
            "avg_final_ships_sum": 0.0,
            "positions": defaultdict(lambda: {"games": 0, "wins": 0}),
            "rank_distribution": Counter(),
        }
    )
    per_pair = defaultdict(lambda: {"games": 0, "wins": Counter(), "draws": 0, "errors": 0})
    seed_outcomes = defaultdict(Counter)
    for row in rows:
        player_count = int(row["player_count"])
        agents = [row[f"agent_{idx}"] for idx in range(player_count)]
        scores = json.loads(row["scores"]) if row["scores"] else []
        winner = row["winner"] or None
        status = row["status"]
        pair_key = " vs ".join(sorted(agents))
        per_pair[pair_key]["games"] += 1
        if status not in ("ok", "draw"):
            per_pair[pair_key]["errors"] += 1
        if winner:
            per_pair[pair_key]["wins"][winner] += 1
        else:
            per_pair[pair_key]["draws"] += 1
        seed_outcomes[str(row["seed"])][winner or status] += 1

        for idx, agent_id in enumerate(agents):
            stats[agent_id]["games"] += 1
            if winner == agent_id:
                stats[agent_id]["wins"] += 1
                stats[agent_id]["positions"][str(idx)]["wins"] += 1
            if winner is None:
                stats[agent_id]["draws"] += 1
            if status not in ("ok", "draw"):
                stats[agent_id]["errors"] += 1
            stats[agent_id]["positions"][str(idx)]["games"] += 1
            if idx < len(scores):
                stats[agent_id]["avg_final_ships_sum"] += scores[idx]
            rank_value = row.get(f"rank_{idx}")
            if rank_value not in ("", None):
                rank_int = int(rank_value)
                stats[agent_id]["avg_rank_sum"] += rank_int
                stats[agent_id]["rank_distribution"][str(rank_int)] += 1

    normalized_stats = {}
    for agent_id, values in stats.items():
        games = values["games"] or 1
        positions = {}
        for position, position_values in values["positions"].items():
            pos_games = position_values["games"] or 1
            positions[position] = {
                "games": position_values["games"],
                "wins": position_values["wins"],
                "winrate": round(position_values["wins"] / pos_games, 4),
            }
        normalized_stats[agent_id] = {
            "games": values["games"],
            "wins": values["wins"],
            "losses": values["games"] - values["wins"] - values["draws"],
            "draws": values["draws"],
            "errors": values["errors"],
            "winrate": round(values["wins"] / games, 4),
            "avg_rank": round(values["avg_rank_sum"] / games, 4),
            "avg_final_ships": round(values["avg_final_ships_sum"] / games, 2),
            "positions": positions,
            "rank_distribution": dict(values["rank_distribution"]),
        }

    normalized_pairs = {}
    for key, values in per_pair.items():
        normalized_pairs[key] = {
            "games": values["games"],
            "wins": dict(values["wins"]),
            "draws": values["draws"],
            "errors": values["errors"],
        }

    return {
        "agent_summary": normalized_stats,
        "pair_summary": normalized_pairs,
        "seed_outcomes": {seed: dict(counter) for seed, counter in seed_outcomes.items()},
    }


def _match_orders(args: argparse.Namespace) -> list[list[str]]:
    if args.cmd == "pair":
        base = [args.agent_a, args.agent_b]
        if not args.bidirectional:
            return [base]
        return [base, [args.agent_b, args.agent_a]]
    if args.cmd == "gauntlet":
        orders: list[list[str]] = []
        for opponent in args.opponents:
            orders.append([args.challenger, opponent])
            if args.bidirectional:
                orders.append([opponent, args.challenger])
        return orders
    return [args.agents]


def _run(args: argparse.Namespace) -> dict[str, Any]:
    seeds = _parse_seeds(args.seeds)
    orders = _match_orders(args)
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "matches.csv"
    rows: list[dict[str, Any]] = []
    match_id = 0
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for seed in seeds:
            for order in orders:
                match_id += 1
                row = _run_match(order, seed=seed, match_id=match_id, series=args.series)
                rows.append(row)
                _write_row(writer, row, handle)
                if args.progress:
                    print(
                        json.dumps(
                            {
                                "match_id": row["match_id"],
                                "seed": row["seed"],
                                "agents": [row[f"agent_{idx}"] for idx in range(int(row["player_count"]))],
                                "winner": row["winner"],
                                "status": row["status"],
                                "turns": row["turns"],
                                "duration_s": row["duration_s"],
                            },
                            ensure_ascii=False,
                        ),
                        flush=True,
                    )
    result = {
        "series": args.series,
        "cmd": args.cmd,
        "seeds": seeds,
        "match_count": len(rows),
        "matches_csv": str(csv_path),
        "summary": _summarize(rows),
    }
    (output_dir / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", default="eval")
    parser.add_argument("--seeds", default="1")
    parser.add_argument("--out", default="outputs/tournament_raw/eval")
    parser.add_argument("--progress", action="store_true")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    pair = subparsers.add_parser("pair")
    pair.add_argument("agent_a")
    pair.add_argument("agent_b")
    pair.add_argument("--bidirectional", action="store_true")

    gauntlet = subparsers.add_parser("gauntlet")
    gauntlet.add_argument("challenger")
    gauntlet.add_argument("--opponents", nargs="+", required=True)
    gauntlet.add_argument("--bidirectional", action="store_true")

    ffa = subparsers.add_parser("free-for-all")
    ffa.add_argument("--agents", nargs="+", required=True)

    args = parser.parse_args()
    result = _run(args)
    print(json.dumps({"series": result["series"], "match_count": result["match_count"], "summary": result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
