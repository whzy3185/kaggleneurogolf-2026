# Alyce V6 Local Eval - 2026-06-19

## Summary

Implemented:

```text
agents/variants/alyce_v6_prod_gap_mode
```

V6 is a local research candidate. It is **not submitted** and **not promoted**.

## Implementation

V6 starts from V5, which itself starts from V2. The new logic is limited to the
4P selected-action filter in `main.py`.

New config fields include:

```text
enable_v6_prod_gap_mode
v6_gap_step_start / v6_gap_step_end
v6_prod_gap_trigger
v6_prod_rank_trigger
v6_gap_alt_score_gap
v6_gap_depletion_ratio
v6_gap_safe_reaction_gap
```

Trace path:

```text
ORBIT_V6_TRACE_PATH
```

V6 keeps compatibility with `ORBIT_V5_TRACE_PATH` for local tooling only.

## Verification

```text
python -m py_compile agents/variants/alyce_v6_prod_gap_mode/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v6_prod_gap_mode
```

Result:

```text
py_compile: pass
smoke: pass
sample_actions_ok: true
env_status: ok
```

## Local 1v1 Screen

Seeds 1-5, bidirectional.

| Matchup | V6 wins | Opponent wins | Draws | V6 avg rank | Opp avg rank | Errors |
|---|---:|---:|---:|---:|---:|---:|
| V6 vs V2 | 5 | 3 | 2 | 1.3 | 1.5 | 0 |
| V6 vs V1 | 3 | 4 | 3 | 1.4 | 1.3 | 0 |

Interpretation:

```text
V6 does not obviously regress against V2 in this small 1v1 screen, but it still
does not reliably beat V1.
```

## 4P Fixed-Seat Screen

Setup:

```text
V1, V2, V3, V6
seeds 1-5
V6 fixed in position 3
```

| Agent | Wins | Avg rank | Avg final ships | Errors |
|---|---:|---:|---:|---:|
| V6 | 3/5 | 1.4 | 2958.0 | 0 |
| V2 | 1/5 | 1.8 | 705.8 | 0 |
| V1 | 1/5 | 2.0 | 382.8 | 0 |
| V3 | 0/5 | 2.2 | 0.0 | 0 |

This looks promising but is not enough because previous local results showed
seat sensitivity and same-seed drift.

## 4P Seat Rotation Screen

Setup:

```text
V1, V2, V3, V6
seeds 1-3
V6 rotated through positions 0, 1, 2, 3
```

V6 by seat:

| V6 position | Games | Wins | Avg rank | Avg final ships |
|---:|---:|---:|---:|---:|
| 0 | 3 | 0 | 2.0 | 0.0 |
| 1 | 3 | 0 | 2.0 | 1780.33 |
| 2 | 3 | 1 | 1.6667 | 680.67 |
| 3 | 3 | 0 | 2.0 | 0.0 |

Combined:

```text
V6 rotated: 1 win / 12 games, avg_rank about 1.9167, errors 0
```

The fixed-seat screen and rotated-seat screen disagree strongly. This repeats
the known local stability problem and means V6 is not a submit candidate.

## Trace Check

Two trace reruns:

```text
outputs/v6_eval/trace/pos0_seed1.jsonl
outputs/v6_eval/trace/pos2_seed2.jsonl
```

These files are intentionally under `outputs/` and not committed.

Trace summary:

| Trace | Rows | Changed top action | V6 gap active | Gap-mode changed |
|---|---:|---:|---:|---:|
| pos0_seed1 | 118 | 1 | 0 | 0 |
| pos2_seed2 | 129 | 4 | 14 | 1 |

Changed examples:

```text
pos0_seed1 step 88:
  reason: source_depletion_with_safe_alt
  before: target prod 2, distance 33.69
  after: target prod 4, distance 47.68

pos2_seed2 step 64:
  reason: prod_gap_bad_attack_with_safe_alt
  before: target prod 1, distance 21.18
  after: target prod 4, distance 14.62
```

Interpretation:

```text
The production-gap mode is wired correctly and can change a selected action, but
it triggers too rarely. Most action changes are still V5 source-depletion
replacements.
```

## Decision

```text
Do not submit V6.
Keep V2 as practical official baseline until V5 result completes.
```

V6 is directionally useful because:

```text
it preserves runtime validity;
it does not corrupt 2P in the small screen;
it produces real selected-action trace;
it can replace a bad top action with a higher-production alternative.
```

V6 is not enough because:

```text
4P seat-rotated performance is weak;
the new production-gap branch triggers only once in two traced games;
same-seed reruns can produce different outcomes, so isolated wins are not proof;
V6 still does not directly model holdability or third-party aftermath.
```

## Next Route

V7 should not be a Kaggle submission until it passes a rotated 4P gate.

Recommended V7 task chain:

1. Add trace counters for every candidate label, not only selected top action.
2. Record step 50/100 production rank and gap in local match CSV.
3. Widen production-gap mode from `rank >= 3` to a continuous risk score:
   production gap, source production, depletion, target production, reaction
   gap, and distance.
4. Keep the action selected-action-only, but choose alternative using a
   holdability/frontier score instead of simple close-score bonuses.
5. Validate on:
   - V7 vs V2 20 seeds bidirectional;
   - V7 vs V1 20 seeds bidirectional;
   - V1/V2/V3/V7 4P, 5 seeds per seat;
   - V2/V5/V6/V7 4P family screen.
