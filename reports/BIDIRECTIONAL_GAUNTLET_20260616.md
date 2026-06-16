# Bidirectional Gauntlet

Date: 2026-06-16

Purpose:

The first base-selection tournament only evaluated one player order per pair.
Stage 8 adds bidirectional local gauntlets so every head-to-head covers both
player 0 and player 1 positions.

Harness change:

```text
scripts/run_tournament.py ... --bidirectional
```

This runs `[challenger, opponent]` and `[opponent, challenger]` for each seed.

Command:

```text
python scripts\run_tournament.py gauntlet local/agents/adaptive_agent --opponents baselines/starter baselines/nearest-sniper external/tamrazov-starwars external/sigmaborov-reinforce external/ykhnkf-distance-prioritized --seeds 601 --bidirectional --out outputs\eval\adaptive_bidirectional_gauntlet_20260616
```

Result:

| Opponent | Adaptive Record | Notes |
|---|---:|---|
| `baselines/starter` | 2-0 | won both positions |
| `baselines/nearest-sniper` | 2-0 | won both positions |
| `external/tamrazov-starwars` | 0-2 | lost both positions |
| `external/sigmaborov-reinforce` | 0-2 | lost both positions |
| `external/ykhnkf-distance-prioritized` | 2-0 | won both positions |

Overall local record: 6-4.

Important caveats:

- This is local-only evidence, not an official Kaggle score.
- The lab runner records seed for audit, but its own comment says the current
  Kaggle engine path does not reliably consume that seed internally.
- OpenSpiel/litellm warnings are unrelated to Orbit Wars match completion.

Observed target priorities:

1. `external/tamrazov-starwars`
   - Metadata describes a strong forward-simulation agent with sun-dodge,
     multi-step intercept, gang-up, crash-exploit, and total-war endgame.
   - Source has explicit weakest-enemy and gang-up weighting.
2. `external/sigmaborov-reinforce`
   - Metadata describes a forward-simulation agent with comet-aware aim,
     sun-dodge, reinforcement, and rolling-horizon planning.
   - Source prioritizes reinforcement missions before captures.

Counter hypotheses for the next stage:

- Add exposure-aware reserve logic so our base does not present easy crash or
  gang-up windows.
- Detect early reinforcement-heavy opponents and delay low-value neutral
  captures that become overextended.
- Add a lightweight "deny reinforce engine" mode: prefer attacks that force
  the opponent to spend ships reinforcing rather than racing every neutral.
- Expand profiler traits for `reinforce_heavy`, `crash_exploiter`, and
  `weakest_targeter`; current traits are too coarse for these two opponents.

Current decision:

Adaptive is runnable and stronger than starter/nearest/ykhnkf locally, but it is
not submission-ready because it loses 0-4 against the two strongest public
benchmarks in this short bidirectional suite.
