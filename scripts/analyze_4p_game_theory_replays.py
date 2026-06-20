from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


SNAPSHOT_STEPS = (20, 50, 100, 150, 200)
PHASES = (
    ("opening_0_50", 0, 50),
    ("mid_50_150", 50, 150),
    ("late_mid_150_300", 150, 300),
    ("end_300_500", 300, 501),
)
TEAM_NAME = "muelsyse111"


def _phase(step: int) -> str:
    for name, start, end in PHASES:
        if start <= step < end:
            return name
    return "unknown"


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _corner_dist(pos: tuple[float, float]) -> float:
    corners = ((0.0, 0.0), (0.0, 100.0), (100.0, 0.0), (100.0, 100.0))
    return min(_dist(pos, corner) for corner in corners)


def _edge_dist(pos: tuple[float, float]) -> float:
    return min(pos[0], pos[1], 100.0 - pos[0], 100.0 - pos[1])


def _angle_delta(a: float, b: float) -> float:
    return abs((a - b + math.pi) % (2 * math.pi) - math.pi)


def _planet_map(obs: dict[str, Any]) -> dict[int, list[Any]]:
    return {int(planet[0]): planet for planet in obs.get("planets", [])}


def _planet_pos(planet: list[Any]) -> tuple[float, float]:
    return float(planet[2]), float(planet[3])


def _owner(planet: list[Any]) -> int:
    return int(planet[1])


def _ships(planet: list[Any]) -> float:
    return float(planet[5])


def _prod(planet: list[Any]) -> float:
    return float(planet[6])


def _infer_target(obs: dict[str, Any], source_id: int, angle: float) -> dict[str, Any] | None:
    planets = _planet_map(obs)
    source = planets.get(int(source_id))
    if source is None:
        return None
    source_pos = _planet_pos(source)
    best: tuple[float, float, list[Any]] | None = None
    for planet in planets.values():
        if int(planet[0]) == int(source_id):
            continue
        target_pos = _planet_pos(planet)
        target_angle = math.atan2(target_pos[1] - source_pos[1], target_pos[0] - source_pos[0])
        delta = _angle_delta(float(angle), target_angle)
        distance = _dist(source_pos, target_pos)
        score = delta + min(distance, 120.0) * 0.0005
        if best is None or score < best[0]:
            best = (score, delta, planet)
    if best is None:
        return None
    _, delta, target = best
    distance = _dist(source_pos, _planet_pos(target))
    return {
        "target_id": int(target[0]),
        "target_owner": _owner(target),
        "target_prod": _prod(target),
        "target_ships": _ships(target),
        "target_x": float(target[2]),
        "target_y": float(target[3]),
        "target_center_dist": _dist(_planet_pos(target), (50.0, 50.0)),
        "distance": distance,
        "angle_delta": delta,
    }


def _player_count(replay: dict[str, Any]) -> int:
    if replay.get("steps"):
        return len(replay["steps"][0])
    return len(replay.get("rewards") or [])


def _our_indexes(replay: dict[str, Any], include_validation: bool = False) -> list[int]:
    names = replay.get("info", {}).get("TeamNames") or []
    indexes = [idx for idx, name in enumerate(names) if name == TEAM_NAME]
    if len(indexes) == 1:
        return indexes
    if include_validation and indexes:
        return indexes
    return []


def _prod_state(obs: dict[str, Any], player_count: int) -> tuple[list[float], list[int], list[float]]:
    prod = [0.0] * player_count
    planets = [0] * player_count
    ships = [0.0] * player_count
    for planet in obs.get("planets", []):
        owner = _owner(planet)
        if 0 <= owner < player_count:
            prod[owner] += _prod(planet)
            planets[owner] += 1
            ships[owner] += _ships(planet)
    for fleet in obs.get("fleets", []):
        owner = int(fleet[1])
        if 0 <= owner < player_count:
            ships[owner] += float(fleet[6])
    return prod, planets, ships


def _rank_values(values: list[float]) -> list[int]:
    ordered = sorted(enumerate(values), key=lambda item: item[1], reverse=True)
    ranks = [0] * len(values)
    prev_value = None
    prev_rank = 0
    for idx, (player, value) in enumerate(ordered, start=1):
        rank = prev_rank if value == prev_value else idx
        ranks[player] = rank
        prev_rank = rank
        prev_value = value
    return ranks


def _min_dist_to_owned(obs: dict[str, Any], player: int, target_pos: tuple[float, float]) -> float | None:
    distances = [
        _dist(_planet_pos(planet), target_pos)
        for planet in obs.get("planets", [])
        if _owner(planet) == int(player)
    ]
    if not distances:
        return None
    return min(distances)


def _reaction_features(
    obs: dict[str, Any],
    player_count: int,
    our_idx: int,
    target: dict[str, Any],
    source_dist: float,
) -> dict[str, Any]:
    target_pos = (float(target["target_x"]), float(target["target_y"]))
    enemy_distances: list[tuple[int, float]] = []
    for player in range(player_count):
        if player == our_idx:
            continue
        distance = _min_dist_to_owned(obs, player, target_pos)
        if distance is not None:
            enemy_distances.append((player, distance))
    if not enemy_distances:
        return {
            "nearest_enemy": "",
            "enemy_min_dist": "",
            "reaction_gap": "",
            "multi_enemy_close": 0,
            "third_party_cleanup_risk": 0,
        }
    nearest_enemy, enemy_min_dist = min(enemy_distances, key=lambda item: item[1])
    close_count = sum(1 for _, distance in enemy_distances if distance <= source_dist + 8.0)
    reaction_gap = enemy_min_dist - source_dist
    return {
        "nearest_enemy": int(nearest_enemy),
        "enemy_min_dist": round(enemy_min_dist, 4),
        "reaction_gap": round(reaction_gap, 4),
        "multi_enemy_close": int(close_count),
        "third_party_cleanup_risk": int(reaction_gap <= 8.0 and close_count >= 2),
    }


def _future_owner_timeline(replay: dict[str, Any], start_step: int, target_id: int, max_horizon: int = 60) -> list[tuple[int, int]]:
    timeline: list[tuple[int, int]] = []
    steps = replay.get("steps") or []
    for step_idx in range(start_step, min(len(steps), start_step + max_horizon + 1)):
        obs = (steps[step_idx][0].get("observation", {}) if steps[step_idx] else {}) or {}
        planet = _planet_map(obs).get(target_id)
        if planet is not None:
            timeline.append((step_idx, _owner(planet)))
    return timeline


def _future_response_counts(
    replay: dict[str, Any],
    step_idx: int,
    our_idx: int,
    target_id: int,
    target_owner: int,
    window: int = 12,
) -> dict[str, int]:
    direct = 0
    defense = 0
    third_party = 0
    steps = replay.get("steps") or []
    for future_idx in range(step_idx + 1, min(len(steps), step_idx + window + 1)):
        for player_idx, state in enumerate(steps[future_idx]):
            if player_idx == our_idx:
                continue
            obs = state.get("observation", {}) or {}
            for command in state.get("action") or []:
                if len(command) < 2:
                    continue
                inferred = _infer_target(obs, int(command[0]), float(command[1]))
                if inferred is None:
                    continue
                inferred_target = int(inferred["target_id"])
                inferred_owner = int(inferred["target_owner"])
                if inferred_owner == our_idx:
                    direct += 1
                if target_owner == player_idx and inferred_target == target_id:
                    defense += 1
                if inferred_target == target_id and player_idx != target_owner:
                    third_party += 1
    return {
        "future_direct_attacks_on_us": direct,
        "future_target_owner_defense": defense,
        "future_third_party_target_actions": third_party,
    }


def _target_type(target_owner: int, our_idx: int) -> str:
    if target_owner == -1:
        return "neutral"
    if target_owner == our_idx:
        return "mine"
    return "enemy"


def _summarize_replay(path: Path, variant: str, include_validation: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    replay = json.loads(path.read_text(encoding="utf-8"))
    player_count = _player_count(replay)
    our_indexes = _our_indexes(replay, include_validation=include_validation)
    if not our_indexes:
        return [], [], []
    names = replay.get("info", {}).get("TeamNames") or []
    rewards = replay.get("rewards") or []
    validation = int(len(set(names)) == 1 and names and names[0] == TEAM_NAME)
    episode_rows: list[dict[str, Any]] = []
    snapshot_rows: list[dict[str, Any]] = []
    action_rows: list[dict[str, Any]] = []

    steps = replay.get("steps") or []
    for our_idx in our_indexes:
        final_obs = (steps[-1][0].get("observation", {}) if steps else {}) or {}
        final_prod, final_planets, final_ships = _prod_state(final_obs, player_count)
        final_prod_ranks = _rank_values(final_prod)
        final_ship_ranks = _rank_values(final_ships)
        reward = rewards[our_idx] if our_idx < len(rewards) else ""
        result = "first" if reward == 1 else "non_first"
        episode_id = replay.get("id") or path.stem.replace("episode-", "").replace("-replay", "")

        episode_rows.append(
            {
                "variant": variant,
                "episode_id": episode_id,
                "path": str(path),
                "player_count": player_count,
                "our_index": our_idx,
                "validation": validation,
                "result": result,
                "reward": reward,
                "turns": len(steps),
                "team_names": " / ".join(str(name) for name in names),
                "final_prod": round(final_prod[our_idx], 4) if our_idx < len(final_prod) else "",
                "final_prod_rank": final_prod_ranks[our_idx] if our_idx < len(final_prod_ranks) else "",
                "final_planets": final_planets[our_idx] if our_idx < len(final_planets) else "",
                "final_ships": round(final_ships[our_idx], 4) if our_idx < len(final_ships) else "",
                "final_ship_rank": final_ship_ranks[our_idx] if our_idx < len(final_ship_ranks) else "",
            }
        )

        for requested in SNAPSHOT_STEPS:
            if not steps:
                continue
            step_idx = min(requested, len(steps) - 1)
            obs = (steps[step_idx][0].get("observation", {}) if steps[step_idx] else {}) or {}
            prod, planets, ships = _prod_state(obs, player_count)
            prod_ranks = _rank_values(prod)
            leader = max(range(player_count), key=lambda idx: prod[idx]) if player_count else ""
            snapshot_rows.append(
                {
                    "variant": variant,
                    "episode_id": episode_id,
                    "player_count": player_count,
                    "our_index": our_idx,
                    "validation": validation,
                    "result": result,
                    "requested_step": requested,
                    "actual_step": step_idx,
                    "our_prod": round(prod[our_idx], 4),
                    "leader_prod": round(prod[leader], 4) if leader != "" else "",
                    "prod_gap": round(prod[our_idx] - prod[leader], 4) if leader != "" else "",
                    "prod_rank": prod_ranks[our_idx],
                    "our_planets": planets[our_idx],
                    "our_ships": round(ships[our_idx], 4),
                    "leader_index": leader,
                    "leader_is_us": int(leader == our_idx) if leader != "" else "",
                    "leader_name": names[leader] if isinstance(leader, int) and leader < len(names) else "",
                }
            )

        for step_idx, step_states in enumerate(steps):
            if our_idx >= len(step_states):
                continue
            state = step_states[our_idx]
            obs = state.get("observation", {}) or {}
            prod, planets, ships = _prod_state(obs, player_count)
            prod_ranks = _rank_values(prod)
            leader = max(range(player_count), key=lambda idx: prod[idx]) if player_count else our_idx
            for command in state.get("action") or []:
                if len(command) < 3:
                    continue
                source_id = int(command[0])
                angle = float(command[1])
                sent = float(command[2])
                planets_by_id = _planet_map(obs)
                source = planets_by_id.get(source_id)
                if source is None:
                    continue
                source_ships = _ships(source)
                source_pos = _planet_pos(source)
                target = _infer_target(obs, source_id, angle)
                if target is None:
                    continue
                target_owner = int(target["target_owner"])
                target_kind = _target_type(target_owner, our_idx)
                commit = sent / max(source_ships + sent, 1.0)
                source_center_dist = _dist(source_pos, (50.0, 50.0))
                source_corner_dist = _corner_dist(source_pos)
                source_edge_dist = _edge_dist(source_pos)
                target_corner_dist = _corner_dist((float(target["target_x"]), float(target["target_y"])))
                target_edge_dist = _edge_dist((float(target["target_x"]), float(target["target_y"])))
                reaction = _reaction_features(obs, player_count, our_idx, target, float(target["distance"]))
                response = _future_response_counts(
                    replay,
                    step_idx,
                    our_idx,
                    int(target["target_id"]),
                    target_owner,
                )
                owner_timeline = _future_owner_timeline(replay, step_idx, int(target["target_id"]))
                captured_by_us_at = ""
                lost_after_capture_at = ""
                seen_us = False
                for future_step, owner in owner_timeline:
                    if owner == our_idx and not seen_us:
                        captured_by_us_at = future_step
                        seen_us = True
                    elif seen_us and owner not in (our_idx, -1):
                        lost_after_capture_at = future_step
                        break
                low_impact_enemy = int(target_kind == "enemy" and float(target["target_prod"]) <= 2 and float(target["distance"]) >= 35)
                center_target = int(float(target["target_center_dist"]) <= 25)
                early_sacrifice = int(
                    step_idx < 60
                    and commit >= 0.75
                    and target_kind in {"neutral", "enemy"}
                    and (reaction.get("third_party_cleanup_risk") == 1 or float(target["target_prod"]) <= 2)
                )
                force_preservation_risk = int(
                    commit >= 0.80
                    and target_kind in {"neutral", "enemy"}
                    and (
                        _prod(source) >= 3.0
                        or source_corner_dist <= 32.0
                        or source_edge_dist <= 12.0
                    )
                    and (
                        float(target["target_prod"]) <= 2.0
                        or reaction.get("third_party_cleanup_risk") == 1
                        or (
                            reaction.get("reaction_gap") not in ("", None)
                            and float(reaction["reaction_gap"]) <= 2.0
                        )
                    )
                )
                corner_overcommit_risk = int(
                    player_count == 2
                    and step_idx < 90
                    and source_corner_dist <= 35.0
                    and commit >= 0.75
                    and target_kind in {"neutral", "enemy"}
                    and (
                        float(target["distance"]) >= 35.0
                        or target_corner_dist > 35.0
                        or (
                            reaction.get("reaction_gap") not in ("", None)
                            and float(reaction["reaction_gap"]) <= 3.0
                        )
                    )
                )
                leader_target = int(target_owner == leader and target_kind == "enemy")
                action_rows.append(
                    {
                        "variant": variant,
                        "episode_id": episode_id,
                        "player_count": player_count,
                        "our_index": our_idx,
                        "validation": validation,
                        "result": result,
                        "step": step_idx,
                        "phase": _phase(step_idx),
                        "source_id": source_id,
                        "source_prod": round(_prod(source), 4),
                        "source_center_dist": round(source_center_dist, 4),
                        "source_corner_dist": round(source_corner_dist, 4),
                        "source_edge_dist": round(source_edge_dist, 4),
                        "corner_source": int(source_corner_dist <= 35.0),
                        "edge_source": int(source_edge_dist <= 12.0),
                        "source_ships_before": round(source_ships + sent, 4),
                        "source_ships_after_obs": round(source_ships, 4),
                        "sent": round(sent, 4),
                        "commit_ratio": round(commit, 4),
                        "target_id": int(target["target_id"]),
                        "target_type": target_kind,
                        "target_owner": target_owner,
                        "target_prod": round(float(target["target_prod"]), 4),
                        "target_ships": round(float(target["target_ships"]), 4),
                        "distance": round(float(target["distance"]), 4),
                        "target_center_dist": round(float(target["target_center_dist"]), 4),
                        "target_corner_dist": round(target_corner_dist, 4),
                        "target_edge_dist": round(target_edge_dist, 4),
                        "corner_target": int(target_corner_dist <= 35.0),
                        "edge_target": int(target_edge_dist <= 12.0),
                        "center_target": center_target,
                        "angle_delta": round(float(target["angle_delta"]), 4),
                        "prod_gap": round(prod[our_idx] - prod[leader], 4),
                        "prod_rank": prod_ranks[our_idx],
                        "leader_index": leader,
                        "leader_target": leader_target,
                        "low_impact_enemy": low_impact_enemy,
                        "early_sacrifice": early_sacrifice,
                        "force_preservation_risk": force_preservation_risk,
                        "corner_overcommit_risk": corner_overcommit_risk,
                        "captured_by_us_at": captured_by_us_at,
                        "lost_after_capture_at": lost_after_capture_at,
                        **reaction,
                        **response,
                    }
                )
    return episode_rows, snapshot_rows, action_rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _avg(rows: list[dict[str, Any]], field: str) -> float:
    values = [float(row[field]) for row in rows if row.get(field) not in ("", None)]
    return mean(values) if values else 0.0


def _aggregate(episode_rows: list[dict[str, Any]], snapshot_rows: list[dict[str, Any]], action_rows: list[dict[str, Any]]) -> dict[str, Any]:
    public_eps = [row for row in episode_rows if not int(row["validation"])]
    public_actions = [row for row in action_rows if not int(row["validation"])]
    public_snaps = [row for row in snapshot_rows if not int(row["validation"])]
    summary: dict[str, Any] = {
        "episodes": len(public_eps),
        "actions": len(public_actions),
        "by_variant": {},
    }
    for variant in sorted({row["variant"] for row in public_eps}):
        eps_v = [row for row in public_eps if row["variant"] == variant]
        acts_v = [row for row in public_actions if row["variant"] == variant]
        snaps_v = [row for row in public_snaps if row["variant"] == variant]
        mode_counter = Counter(str(row["player_count"]) + "P" for row in eps_v)
        win_counter = Counter((str(row["player_count"]) + "P", row["result"]) for row in eps_v)
        phase_mix: dict[str, dict[str, Any]] = {}
        for phase, _, _ in PHASES:
            rows = [row for row in acts_v if row["phase"] == phase]
            if not rows:
                continue
            phase_mix[phase] = {
                "actions": len(rows),
                "enemy_rate": round(sum(1 for row in rows if row["target_type"] == "enemy") / len(rows), 4),
                "neutral_rate": round(sum(1 for row in rows if row["target_type"] == "neutral") / len(rows), 4),
                "mine_rate": round(sum(1 for row in rows if row["target_type"] == "mine") / len(rows), 4),
                "center_rate": round(sum(int(row["center_target"]) for row in rows) / len(rows), 4),
                "early_sacrifice_count": sum(int(row["early_sacrifice"]) for row in rows),
                "force_preservation_risk_count": sum(int(row["force_preservation_risk"]) for row in rows),
                "corner_overcommit_risk_count": sum(int(row["corner_overcommit_risk"]) for row in rows),
                "third_party_cleanup_risk_rate": round(
                    sum(int(row["third_party_cleanup_risk"]) for row in rows) / len(rows), 4
                ),
                "corner_source_rate": round(sum(int(row["corner_source"]) for row in rows) / len(rows), 4),
                "corner_target_rate": round(sum(int(row["corner_target"]) for row in rows) / len(rows), 4),
                "edge_source_rate": round(sum(int(row["edge_source"]) for row in rows) / len(rows), 4),
                "edge_target_rate": round(sum(int(row["edge_target"]) for row in rows) / len(rows), 4),
                "avg_commit": round(_avg(rows, "commit_ratio"), 4),
                "avg_distance": round(_avg(rows, "distance"), 4),
                "future_direct_attacks_on_us": sum(int(row["future_direct_attacks_on_us"]) for row in rows),
                "future_target_owner_defense": sum(int(row["future_target_owner_defense"]) for row in rows),
                "future_third_party_target_actions": sum(int(row["future_third_party_target_actions"]) for row in rows),
            }
        snapshots: dict[str, dict[str, Any]] = {}
        for mode in (2, 4):
            for result in ("first", "non_first"):
                for requested in SNAPSHOT_STEPS:
                    rows = [
                        row
                        for row in snaps_v
                        if int(row["player_count"]) == mode
                        and row["result"] == result
                        and int(row["requested_step"]) == requested
                    ]
                    if not rows:
                        continue
                    snapshots[f"{mode}P_{result}_step{requested}"] = {
                        "n": len(rows),
                        "avg_prod": round(_avg(rows, "our_prod"), 4),
                        "avg_prod_gap": round(_avg(rows, "prod_gap"), 4),
                        "avg_prod_rank": round(_avg(rows, "prod_rank"), 4),
                        "avg_planets": round(_avg(rows, "our_planets"), 4),
                        "avg_ships": round(_avg(rows, "our_ships"), 4),
                    }
        summary["by_variant"][variant] = {
            "public_episodes": len(eps_v),
            "mode_counter": dict(mode_counter),
            "win_counter": {f"{mode}_{result}": count for (mode, result), count in win_counter.items()},
            "avg_final_prod": round(_avg(eps_v, "final_prod"), 4),
            "avg_final_prod_rank": round(_avg(eps_v, "final_prod_rank"), 4),
            "avg_final_ships": round(_avg(eps_v, "final_ships"), 4),
            "phase_mix": phase_mix,
            "snapshots": snapshots,
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="variant=episode_directory",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--include-validation", action="store_true")
    args = parser.parse_args()

    episode_rows: list[dict[str, Any]] = []
    snapshot_rows: list[dict[str, Any]] = []
    action_rows: list[dict[str, Any]] = []
    for item in args.input:
        variant, raw_path = item.split("=", 1)
        for path in sorted(Path(raw_path).glob("*.json")):
            eps, snaps, actions = _summarize_replay(path, variant, include_validation=args.include_validation)
            episode_rows.extend(eps)
            snapshot_rows.extend(snaps)
            action_rows.extend(actions)

    output_dir = Path(args.output_dir)
    _write_csv(output_dir / "game_theory_episode_summary.csv", episode_rows)
    _write_csv(output_dir / "game_theory_phase_snapshots.csv", snapshot_rows)
    _write_csv(output_dir / "game_theory_action_events.csv", action_rows)
    summary = _aggregate(episode_rows, snapshot_rows, action_rows)
    (output_dir / "game_theory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
