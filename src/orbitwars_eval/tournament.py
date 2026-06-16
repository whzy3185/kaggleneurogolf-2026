from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path

from .metrics import summarize_matches
from .runner import run_match


def run_round_robin(
    agent_ids: list[str],
    *,
    seeds: list[int],
    mode: str = "fast",
    output_dir: Path,
    bidirectional: bool = False,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    matches: list[dict] = []
    for agent_a, agent_b in itertools.combinations(agent_ids, 2):
        for seed in seeds:
            matches.append(run_match([agent_a, agent_b], seed=seed, mode=mode))
            if bidirectional:
                matches.append(run_match([agent_b, agent_a], seed=seed, mode=mode))
    summary = summarize_matches(matches)
    result = {
        "shape": "round_robin",
        "mode": mode,
        "bidirectional": bidirectional,
        "matches": matches,
        "summary": summary,
    }
    (output_dir / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    _write_csv(output_dir / "matches.csv", matches)
    return result


def run_gauntlet(
    challenger: str,
    opponents: list[str],
    *,
    seeds: list[int],
    mode: str = "fast",
    output_dir: Path,
    bidirectional: bool = False,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    matches: list[dict] = []
    for opponent in opponents:
        for seed in seeds:
            matches.append(run_match([challenger, opponent], seed=seed, mode=mode))
            if bidirectional:
                matches.append(run_match([opponent, challenger], seed=seed, mode=mode))
    summary = summarize_matches(matches)
    result = {
        "shape": "gauntlet",
        "challenger": challenger,
        "mode": mode,
        "bidirectional": bidirectional,
        "matches": matches,
        "summary": summary,
    }
    (output_dir / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    _write_csv(output_dir / "matches.csv", matches)
    return result


def _write_csv(path: Path, matches: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["agent_0", "agent_1", "winner", "scores", "turns", "duration_s", "status", "seed"],
        )
        writer.writeheader()
        for match in matches:
            agents = match.get("agent_ids", [])
            writer.writerow(
                {
                    "agent_0": agents[0] if len(agents) > 0 else "",
                    "agent_1": agents[1] if len(agents) > 1 else "",
                    "winner": match.get("winner"),
                    "scores": match.get("scores"),
                    "turns": match.get("turns"),
                    "duration_s": match.get("duration_s"),
                    "status": match.get("status"),
                    "seed": match.get("seed"),
                }
            )
