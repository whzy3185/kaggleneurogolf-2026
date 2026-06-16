import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orbitwars_eval.tournament import run_gauntlet, run_round_robin


def _parse_seeds(raw: str) -> list[int]:
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    rr = sub.add_parser("round-robin")
    rr.add_argument("--agents", nargs="+", required=True)
    rr.add_argument("--seeds", default="42")
    rr.add_argument("--mode", choices=["fast", "faithful"], default="fast")
    rr.add_argument("--out", default="outputs/eval/round_robin")
    rr.add_argument("--bidirectional", action="store_true")

    gauntlet = sub.add_parser("gauntlet")
    gauntlet.add_argument("challenger")
    gauntlet.add_argument("--opponents", nargs="+", required=True)
    gauntlet.add_argument("--seeds", default="42")
    gauntlet.add_argument("--mode", choices=["fast", "faithful"], default="fast")
    gauntlet.add_argument("--out", default="outputs/eval/gauntlet")
    gauntlet.add_argument("--bidirectional", action="store_true")

    args = parser.parse_args()
    seeds = _parse_seeds(args.seeds)
    if args.cmd == "round-robin":
        result = run_round_robin(
            args.agents,
            seeds=seeds,
            mode=args.mode,
            output_dir=Path(args.out),
            bidirectional=args.bidirectional,
        )
    else:
        result = run_gauntlet(
            args.challenger,
            args.opponents,
            seeds=seeds,
            mode=args.mode,
            output_dir=Path(args.out),
            bidirectional=args.bidirectional,
        )
    print(json.dumps({"shape": result["shape"], "summary": result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
