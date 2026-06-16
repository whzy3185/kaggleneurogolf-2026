# Opponent Profiler Fix Report

Date: 2026-06-16

Commit base: `49a94d7`

## Scope

This stage fixed only obvious profiler issues that could pollute later
evaluation. It did not add broad new strategy logic.

Changed files:

- `src/orbitwars_agent/opponent_profiler.py`
- `tests/test_opponent_profiler.py`

## Fix 1 - observed_turns Accounting

Previous behavior:

- `observed_turns` incremented once for every enemy-owned planet.
- An enemy with three owned planets could gain three observed turns in one
  state update.

New behavior:

- each enemy id observed in a state update increments `observed_turns` at most
  once
- observed enemies are gathered from both enemy-owned planets and visible enemy
  fleets

Why this matters:

- confidence is partly based on observed turns
- turtle and send-pressure scores depend on observed turns
- the old accounting could make successful expanders look more observed or more
  passive than they really were

## Fix 2 - Minimal weak_bot Signal

Previous behavior:

- `weak_bot` existed in the public profile surface but was always `0.0`

New minimal signal:

- low-production target ratio
- unknown/uninferable target ratio
- excessive tiny fleets
- a small no-reinforcement proxy after at least six observed fleets

No sun-collision-like behavior was implemented because the current profiler does
not reliably evaluate enemy path collision quality. This avoids writing a fake
signal.

Risk:

- `weak_bot` is still a rough signal and should not drive aggressive policy
  changes until profile traces show low false positives.

## Fix 3 - Profile Snapshot Export

Added:

- `OpponentProfile.to_dict()`
- `OpponentProfiler.export_profiles(step)`

Purpose:

- support profile trace logging in Stage 2
- make per-turn scores, counts, confidence, and raw counters easy to serialize

## Tests Added

`tests/test_opponent_profiler.py` now covers:

1. `observed_turns` counts each enemy once per state update.
2. early attack against our own planet raises `enemy_rusher`.
3. repeated neutral targeting raises `neutral_rusher`.
4. `weak_bot` is no longer fixed at zero.
5. early confidence does not inflate from multiple enemy-owned planets.
6. profile export includes step, enemy id, counts, and scores.

## Validation

Profiler-only test:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python -m pytest tests\test_opponent_profiler.py -q
```

Result:

```text
8 passed in 0.04s
```

Repository-local tests:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python -m pytest tests -q
```

Result:

```text
19 passed in 0.05s
```

## Remaining Limitations

- `weak_bot` is intentionally conservative and approximate.
- `reinforce_count` remains a property returning `0`; true reinforcement context
  still requires threatened-planet or ownership-transition features.
- `crash_exploiter` still means conflict-targeting, not proven crash exploit.
- profile scores still need real match trace evaluation before counter-policy
  thresholds should be trusted.

## Stage 1 Conclusion

Proceed to profile trace evaluation. Do not tune counter policy yet.
