# Alyce V9 Local Eval - 2026-06-20

## Scope

Evaluated:

```text
agents/variants/alyce_v9_4p_mission_router
```

This is local regression evidence only. It is not an official Kaggle score.

Raw local outputs, not committed:

```text
outputs/v9_eval/pair_v6/matches.csv
outputs/v9_eval/pair_v8/matches.csv
outputs/v9_eval/ffa_pos0/matches.csv
outputs/v9_eval/ffa_pos1/matches.csv
outputs/v9_eval/ffa_pos2/matches.csv
outputs/v9_eval/ffa_pos3/matches.csv
```

## Verification

```text
python -m py_compile agents/variants/alyce_v9_4p_mission_router/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v9_4p_mission_router
```

Result:

```text
py_compile: pass
smoke: pass
errors: 0
timeouts: 0
```

## 1v1 Screens

### V9 vs V6

Command:

```text
python scripts/run_eval_tournament.py --series v9_pair_v6_s1_3 --seeds 1-3 --out outputs/v9_eval/pair_v6 --progress pair local/agents/variants/alyce_v9_4p_mission_router local/agents/variants/alyce_v6_prod_gap_mode --bidirectional
```

Result:

| Agent | Games | Wins | Draws | Avg rank | Avg final ships | Errors |
|---|---:|---:|---:|---:|---:|---:|
| V9 | 6 | 3 | 1 | 1.333 | 1139.3 | 0 |
| V6 | 6 | 2 | 1 | 1.500 | 691.7 | 0 |

### V9 vs V8

Command:

```text
python scripts/run_eval_tournament.py --series v9_pair_v8_s1_3 --seeds 1-3 --out outputs/v9_eval/pair_v8 --progress pair local/agents/variants/alyce_v9_4p_mission_router local/agents/variants/alyce_v8_md_coverage_mission --bidirectional
```

Result:

| Agent | Games | Wins | Draws | Avg rank | Avg final ships | Errors |
|---|---:|---:|---:|---:|---:|---:|
| V9 | 6 | 4 | 0 | 1.333 | 1340.7 | 0 |
| V8 | 6 | 2 | 0 | 1.667 | 624.0 | 0 |

Interpretation:

```text
V9 does not obviously break 2P/local 1v1 behavior in this small screen.
This is not enough to infer official strength.
```

## 4P Rotated Family Screen

Pool:

```text
V6
V7
V8
V9
```

Seeds:

```text
1-3
```

V9 by position:

| V9 position | Games | Wins | Avg rank | Avg final ships | Errors |
|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 0 | 2.000 | 0.0 | 0 |
| 1 | 3 | 1 | 1.667 | 860.0 | 0 |
| 2 | 3 | 1 | 1.667 | 784.3 | 0 |
| 3 | 3 | 2 | 1.333 | 1081.3 | 0 |

Combined:

```text
V9 4P rotated: 4 wins / 12 games
errors: 0
timeouts: 0
```

Step snapshot comparison across the same 12 local 4P games:

| Agent | Step | Avg prod | Avg prod gap | Avg prod rank |
|---|---:|---:|---:|---:|
| V9 | 50 | 15.92 | -6.75 | 2.33 |
| V9 | 100 | 14.50 | -23.08 | 2.42 |
| V6 | 50 | 16.25 | -6.42 | 1.92 |
| V6 | 100 | 19.25 | -18.33 | 2.42 |
| V8 | 50 | 10.42 | -12.25 | 3.17 |
| V8 | 100 | 9.33 | -28.25 | 2.58 |
| V7 | 50 | 15.75 | -6.92 | 2.08 |
| V7 | 100 | 19.00 | -18.58 | 2.00 |

Interpretation:

```text
V9 is better than V8 on the local phase metrics, but not better than V6.
The V9 mission router is too position-sensitive and does not yet improve the
step100 production gap that motivated the change.
```

## Decision

Do not submit V9.

V9 is useful because:

```text
it is valid and smoke-tested;
it implements the mission-router layer requested by the replay analysis;
it does not alter 2P config;
it performs acceptably in 1v1 screens;
it improves over V8 in the small local family screen.
```

V9 is not enough because:

```text
4P position 0 collapses;
step100 production gap is worse than V6 in the local family screen;
the mission router lacks a positive replacement mission when it suppresses
public-sacrifice actions;
there is still no post-arrival holdability simulation.
```

## Next Work

Next branch should refine V9 rather than submit it:

```text
1. Add V9 mission trace counts for public-sacrifice, center, trailing, and
   leader-pressure penalties.
2. Check whether position-0 collapse is caused by over-penalizing expansion or
   by missing replacement missions.
3. Convert some hard/large penalties into a positive safe-frontier mission
   preference instead of pure suppression.
4. Add a local replay-inspired case suite from the V6/V7/V8 worst 4P episodes.
5. Keep 2P unchanged until a dedicated corner-source lifecycle trace exists.
```
