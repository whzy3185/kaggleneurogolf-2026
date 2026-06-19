# Alyce V5 Local Eval - 2026-06-19

## Summary

Implemented a V5 research candidate:

```text
agents/variants/alyce_v5_v2_trace_filter
```

V5 starts from V2, not from the rejected V3/V4 branch.

V5 is **not submitted** and is **not promoted**.

## Why This Version

Previous conclusions:

```text
V2 is the current practical baseline.
V3 underperformed V2 officially.
V4 underperformed in local 4P family screen and used the wrong parent branch.
```

V5 follows the corrected route:

```text
base = agents/variants/alyce_4p_ffa_v2
```

It preserves V2's working 4P mission filter and adds only:

1. local selected-action trace via `ORBIT_V5_TRACE_PATH`;
2. a narrow selected top-candidate replacement filter.

## Implementation

Changed files:

```text
agents/variants/alyce_v5_v2_trace_filter/main.py
agents/variants/alyce_v5_v2_trace_filter/SOURCE.md
agents/variants/alyce_v5_v2_trace_filter/WRAPPER.md
scripts/run_determinism_audit.py
reports/ALYCE_V5_IMPROVEMENT_TASK_CHAIN_20260619.md
```

V5 preserves V2:

```text
severe trap neutral hard veto
soft contested neutral penalty
safe neutral bonus
source reserve
source depletion penalty
leader asset bonus
low-value rear enemy penalty
```

V5 adds a 4P-only filter:

```text
If the selected top action is low-value/risky and a close-score safer
alternative exists, promote the safer alternative.
```

Trace fields include before/after source, target, send size, score, owner,
production, ships, distance, reaction gap, depletion ratio, and reason.

No trace file is written unless:

```text
ORBIT_V5_TRACE_PATH
```

is set.

## Verification

Syntax:

```text
python -m py_compile agents/variants/alyce_v5_v2_trace_filter/main.py
```

Result:

```text
pass
```

Smoke:

```text
python scripts/smoke_candidate.py agents/variants/alyce_v5_v2_trace_filter
```

Result:

```text
passed: true
sample_actions_ok: true
env_status: ok
turns: 59
```

Trace smoke after tuning:

```text
outputs/alyce_v5_trace_smoke/seed1_tuned/trace.jsonl
```

Trace summary:

| Metric | Value |
|---|---:|
| trace rows | 157 |
| changed selected action | 1 |
| no_bad_top | 117 |
| bad_no_alt | 18 |
| no_valid_candidate | 21 |
| changed reason | `source_depletion_with_safe_alt` |

Interpretation:

```text
V5 is not a broad scorer. It is currently a low-frequency safety intervention.
```

## Local Screen

Important caveat:

```text
reports/ALYCE_V5_DETERMINISM_AUDIT_20260619.md showed same-seed repeated local
matches are not fully deterministic. These results are screen evidence only,
not official score evidence.
```

### 1v1

Seeds 1-3, bidirectional.

| Matchup | V5 wins | Opponent wins | Draws | V5 winrate | Errors |
|---|---:|---:|---:|---:|---:|
| V5 vs V2 | 5 | 1 | 0 | 83.3% | 0 |
| V5 vs V1 | 2 | 3 | 1 | 33.3% | 0 |

Read:

```text
V5 does not regress against V2 in this 1v1 screen, but still struggles against
V1. Because V5's new filter is 4P-only, 1v1 is not strong evidence for the V5
filter itself.
```

### 4P Family Screen

Setup:

```text
V1 + V2 + V3 + V5
seeds 1-3
V5 rotated through positions 0, 1, 2, 3
total games: 12
```

| Agent | Wins | Winrate | Avg rank | Avg final ships | Errors |
|---|---:|---:|---:|---:|---:|
| V2 | 6/12 | 50.0% | 1.5000 | 2908.00 | 0 |
| V1 | 2/12 | 16.7% | 1.9167 | 237.17 | 0 |
| V3 | 2/12 | 16.7% | 1.8333 | 495.25 | 0 |
| V5 | 2/12 | 16.7% | 1.9167 | 244.58 | 0 |

V5 by position:

| Position | Games | Wins | Winrate |
|---:|---:|---:|---:|
| 0 | 3 | 1 | 33.3% |
| 1 | 3 | 0 | 0.0% |
| 2 | 3 | 0 | 0.0% |
| 3 | 3 | 1 | 33.3% |

## Comparison To V4

V4 family screen:

```text
V2: 5 wins / 12
V4: 1 win / 12
```

V5 family screen:

```text
V2: 6 wins / 12
V5: 2 wins / 12
```

V5 is a cleaner and safer implementation direction than V4 because it starts
from V2 and provides selected-action trace. However, it still does not beat V2
in 4P.

## Decision

```text
V5 is valid as a local trace/filter experiment.
V5 is not a submit candidate.
Current official/practical baseline remains V2.
```

Reasons:

1. 4P is the important target, and V2 still wins the family screen.
2. V5's intervention is very low frequency.
3. Same-seed local eval is not deterministic enough to trust small wins.
4. V5 did not improve 4P avg rank or winrate against V2.

## Next Improvement Direction

Do not submit V5.

Next code attempt should keep V2 as base and use the V5 trace to design one of:

1. A position-aware 4P opening adjustment.
2. A stronger but still selected-action-only alternative chooser.
3. A midgame mode switch when production gap is already negative by step 50.
4. A replay-derived target-quality trace on official V2 losses, not only local
   generated games.

The most promising next target is:

```text
V6 = V2 base + selected-action trace + production-gap mode switch
```

but only after collecting trace on more V2/V5 4P losses.

