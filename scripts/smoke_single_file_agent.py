from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import sys
import time
import uuid
from pathlib import Path
from typing import Any


logging.getLogger("kaggle_environments").setLevel(logging.ERROR)
logging.getLogger("kaggle_environments.envs.open_spiel_env.open_spiel_env").setLevel(logging.ERROR)


def _load_agent(path: Path):
    module_name = f"single_file_agent_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load Python module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    agent_fn = getattr(module, "agent", None)
    if agent_fn is None or not callable(agent_fn):
        raise AttributeError(f"{path} does not expose callable agent(obs)")
    return agent_fn


def _validate_actions(actions: Any) -> tuple[bool, str]:
    if actions is None:
        return False, "agent returned None"
    if not isinstance(actions, list):
        return False, f"agent returned {type(actions).__name__}, expected list"
    for idx, action in enumerate(actions):
        if not isinstance(action, (list, tuple)):
            return False, f"action {idx} is {type(action).__name__}, expected list/tuple"
        if len(action) != 3:
            return False, f"action {idx} length is {len(action)}, expected 3"
        try:
            int(action[0])
            float(action[1])
            ships = int(action[2])
        except (TypeError, ValueError) as exc:
            return False, f"action {idx} has invalid scalar values: {exc}"
        if ships <= 0:
            return False, f"action {idx} has non-positive ships: {ships}"
    return True, ""


def _minimal_obs() -> dict[str, Any]:
    return {
        "player": 0,
        "step": 0,
        "planets": [
            [0, 0, 20.0, 50.0, 2.0, 50, 2],
            [1, 1, 80.0, 50.0, 2.0, 50, 2],
            [2, -1, 50.0, 25.0, 2.0, 10, 1],
            [3, -1, 50.0, 75.0, 2.0, 10, 1],
        ],
        "fleets": [],
        "initial_planets": [
            [0, 0, 20.0, 50.0, 2.0, 50, 2],
            [1, 1, 80.0, 50.0, 2.0, 50, 2],
            [2, -1, 50.0, 25.0, 2.0, 10, 1],
            [3, -1, 50.0, 75.0, 2.0, 10, 1],
        ],
        "angular_velocity": 0.0,
        "comets": [],
        "comet_planet_ids": [],
    }


def _extract_status(replay: dict[str, Any]) -> tuple[str, list[int], int]:
    steps = replay.get("steps") or []
    if not steps:
        return "crashed", [], 0
    final_step = steps[-1]
    statuses = [state.get("status") for state in final_step]
    if "ERROR" in statuses:
        status = "error"
    elif "TIMEOUT" in statuses:
        status = "timeout"
    elif "INVALID" in statuses:
        status = "invalid"
    else:
        status = "ok"
    rewards = [state.get("reward") for state in final_step]
    return status, rewards, len(steps)


def run_smoke(path: Path, *, seed: int) -> dict[str, Any]:
    from kaggle_environments import make

    start = time.monotonic()
    agent_fn = _load_agent(path)
    sample_actions = agent_fn(_minimal_obs())
    actions_ok, actions_error = _validate_actions(sample_actions)

    env = make("orbit_wars", configuration={"randomSeed": int(seed)}, debug=False)
    env.run([agent_fn, "random"])
    duration_s = time.monotonic() - start
    replay = env.toJSON()
    status, rewards, turns = _extract_status(replay)

    return {
        "agent_path": str(path),
        "has_agent": True,
        "sample_actions_ok": actions_ok,
        "sample_actions_error": actions_error,
        "env_status": status,
        "rewards": rewards,
        "turns": turns,
        "duration_s": round(duration_s, 4),
        "seed": seed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("agent_file")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.agent_file).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    result = run_smoke(path, seed=args.seed)
    passed = (
        result["has_agent"]
        and result["sample_actions_ok"]
        and result["env_status"] == "ok"
        and result["turns"] > 0
    )
    result["passed"] = passed
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, separators=(",", ":")))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
