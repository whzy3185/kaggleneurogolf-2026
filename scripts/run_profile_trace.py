import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
LAB_ROOT = ROOT / "external" / "orbit-wars-lab"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(LAB_ROOT) not in sys.path:
    sys.path.insert(0, str(LAB_ROOT))

from orbit_wars_app.match import run_match as lab_run_match  # noqa: E402
from orbitwars_agent.opponent_profiler import OpponentProfiler  # noqa: E402
from orbitwars_agent.world_model import build_game_state  # noqa: E402
from orbitwars_eval.loader import DEFAULT_ZOO, resolve_agents  # noqa: E402


def _observation_at(step_state: Any) -> dict | None:
    if not isinstance(step_state, dict):
        return None
    obs = step_state.get("observation")
    return obs if isinstance(obs, dict) else None


def _trace_replay(
    replay: dict,
    *,
    agent_ids: list[str],
    max_steps: int | None,
) -> list[dict]:
    profilers = [OpponentProfiler() for _ in agent_ids]
    rows: list[dict] = []
    steps = replay.get("steps") or []
    if max_steps is not None:
        steps = steps[:max_steps]

    for step_index, step in enumerate(steps):
        if not isinstance(step, list):
            continue
        for player, step_state in enumerate(step[: len(agent_ids)]):
            obs = _observation_at(step_state)
            if obs is None:
                continue
            try:
                state = build_game_state(obs, inferred_step=step_index)
                profiles = profilers[player].update(state)
            except Exception as exc:
                rows.append(
                    {
                        "step": step_index,
                        "player": player,
                        "agent_id": agent_ids[player],
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue

            for enemy_id, profile in sorted(profiles.items()):
                snapshot = profile.to_dict()
                rows.append(
                    {
                        "step": state.step,
                        "player": player,
                        "agent_id": agent_ids[player],
                        "enemy_id": enemy_id,
                        "enemy_agent_id": agent_ids[enemy_id] if 0 <= enemy_id < len(agent_ids) else None,
                        "scores": snapshot["scores"],
                        "confidence": snapshot["confidence"],
                        "observed_new_fleets": snapshot["observed_new_fleets"],
                        "counts": {
                            key: value
                            for key, value in snapshot.items()
                            if key.endswith("_count") or key in ("observed_turns", "total_ships_sent")
                        },
                    }
                )
    return rows


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-a", required=True)
    parser.add_argument("--agent-b", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", choices=["fast", "faithful"], default="fast")
    parser.add_argument("--max-steps", type=int, default=0)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    refs = resolve_agents([args.agent_a, args.agent_b], zoo_root=DEFAULT_ZOO)
    outcome = lab_run_match(
        [ref.agent_id for ref in refs],
        [ref.path for ref in refs],
        seed=args.seed,
        mode=args.mode,  # type: ignore[arg-type]
    )
    max_steps = args.max_steps if args.max_steps > 0 else None
    rows = _trace_replay(
        outcome.replay,
        agent_ids=list(outcome.agent_ids),
        max_steps=max_steps,
    )

    if args.output:
        output = Path(args.output)
    else:
        safe_a = args.agent_a.replace("/", "__").replace("\\", "__")
        safe_b = args.agent_b.replace("/", "__").replace("\\", "__")
        output = ROOT / "outputs" / "profile_traces" / f"{safe_a}_vs_{safe_b}_seed{args.seed}.jsonl"
    _write_jsonl(output, rows)

    print(
        json.dumps(
            {
                "agent_ids": list(outcome.agent_ids),
                "winner": outcome.winner,
                "scores": list(outcome.scores),
                "turns": outcome.turns,
                "duration_s": outcome.duration_s,
                "seed": outcome.seed,
                "status": outcome.status,
                "trace_rows": len(rows),
                "output": str(output),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
