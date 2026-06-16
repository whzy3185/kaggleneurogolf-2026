# Targeted Trait Expansion

Date: 2026-06-16

Motivation:

The bidirectional gauntlet showed that the current adaptive candidate loses to
`external/tamrazov-starwars` and `external/sigmaborov-reinforce`. Their local
metadata/source indicate forward simulation, reinforcement, crash/gang-up
exploitation, and weakest-target pressure.

Implemented profiler traits:

| Trait | Signal |
|---|---|
| `reinforce_heavy` | enemy fleets target planets already owned by that enemy |
| `crash_exploiter` | enemy fleets target a planet already involved in visible third-party incoming pressure |
| `weakest_targeter` | enemy fleets target the currently weakest enemy owner in multi-enemy states |

Counter policy wiring:

- `reinforce_heavy`: slightly increases attack pressure and counterattack bonus,
  slightly reduces expansion.
- `crash_exploiter`: raises reserve/defense and lowers max commit ratio.
- `weakest_targeter`: raises reserve/defense.

The adaptive agent only allows supplemental moves when a trait clears the same
confidence gate as the existing policy: profile confidence >= 0.55 and effective
trait score >= 0.55.

Validation:

| Check | Result |
|---|---|
| `python -m pytest tests -q` | 14 passed |
| `python -m compileall -q src agents scripts tests` | passed |
| `python scripts\smoke_adaptive_agent.py` | returned legal actions |
| `python scripts\run_match.py local/agents/adaptive_agent baselines/starter --seed 701` | adaptive won, 2040-0, 99 turns |
| `python scripts\run_match.py local/agents/adaptive_agent external/tamrazov-starwars --seed 702` | adaptive lost, 0-5931, 189 turns |

Decision:

This stage improves observability and targeted-control hooks, but it does not
yet solve the strongest benchmark losses. The next useful step is tactical:
implement concrete anti-Tamrazov/anti-Sigmaborov action selection, then rerun
the bidirectional gauntlet before considering any new Kaggle submission.
