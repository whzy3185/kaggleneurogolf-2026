from __future__ import annotations

from orbitwars_eval import tournament


def _fake_match(agent_ids, *, seed, mode):
    return {
        "agent_ids": list(agent_ids),
        "winner": agent_ids[0],
        "scores": [1, 0],
        "turns": 1,
        "duration_s": 0.0,
        "seed": seed,
        "status": "ok",
    }


def test_bidirectional_gauntlet_pairs(monkeypatch, tmp_path):
    monkeypatch.setattr(tournament, "run_match", _fake_match)

    result = tournament.run_gauntlet(
        "A",
        ["B", "C"],
        seeds=[11, 12],
        output_dir=tmp_path,
        bidirectional=True,
    )

    pairs = [match["agent_ids"] for match in result["matches"]]
    assert pairs == [
        ["A", "B"],
        ["B", "A"],
        ["A", "B"],
        ["B", "A"],
        ["A", "C"],
        ["C", "A"],
        ["A", "C"],
        ["C", "A"],
    ]
    assert result["bidirectional"] is True


def test_bidirectional_round_robin_pairs(monkeypatch, tmp_path):
    monkeypatch.setattr(tournament, "run_match", _fake_match)

    result = tournament.run_round_robin(
        ["A", "B", "C"],
        seeds=[7],
        output_dir=tmp_path,
        bidirectional=True,
    )

    pairs = [match["agent_ids"] for match in result["matches"]]
    assert pairs == [
        ["A", "B"],
        ["B", "A"],
        ["A", "C"],
        ["C", "A"],
        ["B", "C"],
        ["C", "B"],
    ]
    assert result["bidirectional"] is True
