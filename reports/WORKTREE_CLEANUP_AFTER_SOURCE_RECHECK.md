# Worktree Cleanup After Public Output Source Recheck

Date: 2026-06-17

## Context

The latest public output recheck showed that Vkhydras Last is not a confirmed
highest-value public base. It is only the current official workspace best and a
light heuristic candidate. Several fresh Kaggle output packages beat it in the
local 3-seed bidirectional screen:

| Candidate | Local screen vs Vkhydras Last |
|---|---:|
| `ranjeet258/orbit-wars-producer` | 6-0 |
| `romantamrazov/orbit-wars-i-m-stronger` | 6-0 |
| `alycemiki/light-ver-1200-simple-orbit-intruder` | 6-0 |
| `caoyupeng/v2-gru` | 5-1 |
| `shummingfang/orbit-wars-exp50` | 6-0 |

These are local results only, not official Kaggle scores. They are still enough
to pause Vkhydras-targeted work as the main optimization direction.

## Paused Draft Files

The following uncommitted Vkhydras targeted draft areas were moved out of the
main source tree:

- `agents/variants/vkh_last_targeted_v1/`
- `agents/variants/base_plus_source_safety_filter/`
- `configs/action_filter_v1.yaml`
- `configs/mode_policy.yaml`
- `reports/ACTION_FILTER_V1_DESIGN.md`
- `reports/ETA_TOOLS_IMPLEMENTATION.md`
- `reports/GAME_MODE_POLICY_DESIGN.md`
- `reports/OPPONENT_PROFILER_V2_IMPLEMENTATION.md`
- `reports/VKH_LAST_TARGETED_V1_IMPLEMENTATION.md`
- `src/orbitwars_agent/action_filter_v1.py`
- `src/orbitwars_agent/eta_tools.py`
- `src/orbitwars_agent/game_mode.py`
- `src/orbitwars_agent/opponent_profiler_v2.py`
- `tests/test_action_filter_v1.py`
- `tests/test_eta_tools.py`
- `tests/test_game_mode.py`
- `tests/test_opponent_profiler_v2.py`

## Archive Location

The paused files are preserved locally under:

```text
drafts/vkhydras_targeted_v1_obsolete/
```

`drafts/` is gitignored. The archive is intentionally local-only and is not part
of the main branch.

## Reason

The Vkhydras targeted V1 draft was based on the wrong base-selection premise. It
also failed its first non-regression test against the base:

```yaml
vkhydras_last_base_vs_targeted_v1:
  seeds: 10
  bidirectional: true
  base_wins: 15
  targeted_wins: 5
  errors: 0
```

Continuing that direction before reselecting the base would mix a rejected
strategy branch into the main improvement path.

## Main Branch State

The main branch should now continue from:

```text
97643cb audit: recheck public output candidates
```

with only this cleanup report and `.gitignore` update added. No unverified
targeted V1 code is intended for main.

## Next Gate

Proceed to the fresh public output candidate registry, multi-file candidate
loader support, and larger 2-player / 4-player screens before selecting a new
base.
