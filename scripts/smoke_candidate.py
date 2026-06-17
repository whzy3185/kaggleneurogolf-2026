from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orbitwars_agent.candidate_loader import load_candidate  # noqa: E402
from smoke_single_file_agent import _extract_status, _minimal_obs, _validate_actions  # noqa: E402


logging.getLogger("kaggle_environments").setLevel(logging.ERROR)
logging.getLogger("kaggle_environments.envs.open_spiel_env.open_spiel_env").setLevel(logging.ERROR)


def run_smoke(path: Path, *, seed: int) -> dict[str, Any]:
    from kaggle_environments import make

    start = time.monotonic()
    loaded = load_candidate(path)
    sample_actions = loaded.agent(_minimal_obs())
    actions_ok, actions_error = _validate_actions(sample_actions)

    env = make("orbit_wars", configuration={"randomSeed": int(seed)}, debug=False)
    env.run([loaded.agent, "random"])
    duration_s = time.monotonic() - start
    status, rewards, turns = _extract_status(env.toJSON())
    return {
        "source_path": str(loaded.source_path),
        "candidate_dir": str(loaded.candidate_dir),
        "main_py": str(loaded.main_py),
        "package_type": loaded.package_type,
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
    parser.add_argument("candidate")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_smoke(Path(args.candidate), seed=args.seed)
    result["passed"] = (
        result["has_agent"]
        and result["sample_actions_ok"]
        and result["env_status"] == "ok"
        and result["turns"] > 0
    )
    print(json.dumps(result, indent=2 if args.json else None))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
