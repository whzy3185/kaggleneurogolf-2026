# Adaptive Agent Integration

Date: 2026-06-16

Integrated candidate:

```text
Pilkwang base agent
+ action safety validation
+ WorldModel
+ OpponentProfiler
+ confidence-gated CounterPolicy
+ supplemental defense/expansion/counter moves
```

Files:

| File | Role |
|---|---|
| `agents/base_agent.py` | selected Pilkwang base wrapper |
| `agents/adaptive_agent/main.py` | candidate entrypoint |
| `src/orbitwars_agent/adaptive_agent.py` | integration logic |

Behavior:

1. Call the selected base agent first.
2. Validate base actions for legal shape, owned source planet, finite angle, and
   available ship budget.
3. Build `GameState`.
4. Update `OpponentProfiler`.
5. Convert profiles to `StrategyModifiers`.
6. Generate supplemental moves from the lightweight adaptive layer.
7. Merge base and supplemental moves without exceeding source ship budgets.
8. On any exception, fallback to the selected base agent.

Safety:

- No debug printing.
- Fallback-safe.
- Legal action filter before return.
- Simple time guard: if base call and state setup already consume most of the
  turn budget, return validated base actions.
- Supplemental moves are disabled unless either:
  - own planets have clear incoming enemy pressure, or
  - an opponent profile has confidence >= 0.55 and an effective trait score
    >= 0.55.
- `agents/adaptive_agent/main.py` avoids relying solely on `__file__`, because
  `kaggle_environments.agent.get_last_callable()` executes file agents in a
  sparse namespace during local file-path evaluation.

Validation note:

An initial always-on supplemental smoke match over-intervened against the
selected base behavior. The current integration is intentionally conservative:
without high-confidence evidence, it behaves like the Pilkwang base plus action
validation/fallback.

The first file-path adaptive smoke also exposed an entrypoint bug: callable
execution worked, but file-path execution failed to initialize `src` imports
reliably and behaved like an empty agent. The entrypoint now discovers the repo
root from `__file__` when available and from the current working directory as a
fallback.

Latest local validation:

| Command | Result |
|---|---|
| `python scripts\smoke_adaptive_agent.py` | returns legal actions |
| `python scripts\run_match.py local/agents/adaptive_agent baselines/starter --seed 501` | adaptive won, 3258-0, 128 turns |
| `python scripts\run_match.py baselines/starter local/agents/adaptive_agent --seed 501` | adaptive won, 2207-0, 128 turns |
| `python scripts\run_match.py local/agents/adaptive_agent baselines/starter --seed 502` | adaptive won, 1693-0, 155 turns |
| `python scripts\run_match.py baselines/starter local/agents/adaptive_agent --seed 502` | adaptive won, 2087-0, 130 turns |

Current decision:

This candidate is integrated but not selected for submission. It needs a
tournament comparison against `agents/base_agent.py` and public opponents.
