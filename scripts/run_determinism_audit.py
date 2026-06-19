from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_eval_tournament import FIELDNAMES, _run_match, _summarize  # noqa: E402


def _score_signature(row: dict[str, Any]) -> str:
    player_count = int(row["player_count"])
    ranks = [str(row.get(f"rank_{idx}", "")) for idx in range(player_count)]
    scores = [str(row.get(f"score_{idx}", "")) for idx in range(player_count)]
    return "|".join(
        [
            str(row.get("winner", "")),
            str(row.get("status", "")),
            ",".join(ranks),
            ",".join(scores),
        ]
    )


def _run(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    csv_path = output_dir / "matches.csv"
    fieldnames = ["repeat", *FIELDNAMES]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for repeat in range(1, int(args.repeats) + 1):
            row = _run_match(args.agents, seed=int(args.seed), match_id=repeat, series=args.series)
            row_with_repeat = {"repeat": repeat, **row}
            rows.append(row)
            writer.writerow(row_with_repeat)
            handle.flush()
            if args.progress:
                print(
                    json.dumps(
                        {
                            "repeat": repeat,
                            "winner": row["winner"],
                            "status": row["status"],
                            "turns": row["turns"],
                            "scores": row["scores"],
                            "duration_s": row["duration_s"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

    winners = Counter(row.get("winner", "") or row.get("status", "") for row in rows)
    signatures = Counter(_score_signature(row) for row in rows)
    deterministic = len(signatures) == 1
    winner_stable = len(winners) == 1
    result = {
        "series": args.series,
        "seed": int(args.seed),
        "repeats": int(args.repeats),
        "agents": args.agents,
        "matches_csv": str(csv_path),
        "winner_stable": winner_stable,
        "score_signature_stable": deterministic,
        "winner_counts": dict(winners),
        "score_signature_counts": dict(signatures),
        "summary": _summarize(rows),
    }
    (output_dir / "summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Repeat one local Orbit Wars match to audit determinism.")
    parser.add_argument("--series", default="determinism_audit")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", default="outputs/determinism_audit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--agents", nargs="+", required=True)
    args = parser.parse_args()
    result = _run(args)
    print(
        json.dumps(
            {
                "series": result["series"],
                "winner_stable": result["winner_stable"],
                "score_signature_stable": result["score_signature_stable"],
                "winner_counts": result["winner_counts"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

