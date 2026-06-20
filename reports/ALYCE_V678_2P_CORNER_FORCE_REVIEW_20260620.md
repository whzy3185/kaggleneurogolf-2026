# Alyce V6/V7/V8 2P Corner And Force Review - 2026-06-20

## Scope

This report opens the requested 2P replay review in parallel with the 4P mission
work. It uses the same visible official V6/V7/V8 replay set as:

```text
reports/ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md
```

Additional analyzer fields were added to:

```text
scripts/analyze_4p_game_theory_replays.py
```

New per-action labels:

```text
source_center_dist
source_corner_dist
target_corner_dist
source_edge_dist
target_edge_dist
corner_source
corner_target
edge_source
edge_target
force_preservation_risk
corner_overcommit_risk
```

The raw replay and CSV outputs remain outside Git:

```text
D:\orbitwars_replays\alyce_v678_game_theory_analysis
```

## 2P Official Replay Coverage

| Variant | Episodes | First | First rate | Avg final prod | Avg final prod rank | Avg final ships |
|---|---:|---:|---:|---:|---:|---:|
| V6 | 38 | 21 | 0.553 | 33.18 | 1.42 | 1060.6 |
| V7 | 9 | 6 | 0.667 | 36.78 | 1.33 | 1730.4 |
| V8 | 9 | 8 | 0.889 | 58.33 | 1.11 | 1786.3 |

The V7/V8 2P sample is small. It explains why V8 can look attractive locally or
in visible 2P, but it does not overrule the official total score:

```text
V8 2P visible sample is strong.
V8 4P hard games still collapse.
V6 remains official best.
```

## 2P Phase Separation

| Variant | Result | Step | N | Prod | Gap | Rank | Planets | Ships |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| V6 | first | 20 | 21 | 9.95 | 0.00 | 1.00 | 3.24 | 83.6 |
| V6 | first | 50 | 21 | 25.14 | -1.67 | 1.29 | 8.52 | 455.3 |
| V6 | first | 100 | 21 | 37.33 | 0.00 | 1.00 | 12.62 | 862.6 |
| V6 | non_first | 20 | 17 | 7.76 | -0.18 | 1.12 | 2.88 | 74.6 |
| V6 | non_first | 50 | 17 | 24.12 | -2.29 | 1.41 | 8.06 | 411.7 |
| V6 | non_first | 100 | 17 | 23.06 | -11.94 | 1.82 | 7.94 | 555.1 |
| V6 | non_first | 150 | 17 | 8.35 | -43.41 | 1.94 | 2.82 | 246.1 |
| V6 | non_first | 200 | 17 | 4.53 | -51.18 | 1.94 | 1.59 | 134.8 |

Main read:

```text
2P losses are not usually decided as early as 4P losses. V6 2P non-first games
are still close at step 50, then separate heavily by step 100-150.
```

This differs from 4P:

```text
4P failures often become strategically terminal by step 50.
2P failures often remain playable at step 50 but lose conversion / force
preservation in the midgame.
```

## Corner / Edge / Force Metrics

| Variant | Result | Phase | Actions | Enemy | Neutral | Mine | CornerSrc | CornerTgt | EdgeSrc | ForceRisk | CornerOver | Commit | Dist | DirectResp/action |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V6 | first | opening_0_50 | 592 | 0.238 | 0.507 | 0.255 | 0.397 | 0.525 | 0.375 | 175 | 111 | 0.802 | 45.9 | 4.22 |
| V6 | non_first | opening_0_50 | 521 | 0.217 | 0.493 | 0.290 | 0.403 | 0.528 | 0.426 | 118 | 79 | 0.758 | 46.0 | 5.31 |
| V6 | first | mid_50_150 | 3218 | 0.324 | 0.192 | 0.484 | 0.448 | 0.530 | 0.449 | 889 | 229 | 0.815 | 41.4 | 8.08 |
| V6 | non_first | mid_50_150 | 2819 | 0.275 | 0.173 | 0.552 | 0.551 | 0.576 | 0.582 | 554 | 159 | 0.746 | 36.1 | 8.00 |
| V6 | first | late_mid_150_300 | 1749 | 0.323 | 0.220 | 0.457 | 0.427 | 0.494 | 0.471 | 528 | 0 | 0.831 | 42.8 | 7.84 |
| V6 | non_first | late_mid_150_300 | 890 | 0.203 | 0.166 | 0.630 | 0.608 | 0.566 | 0.556 | 190 | 0 | 0.699 | 31.0 | 3.62 |

Interpretation:

1. Corner and edge play is not itself bad.
   - V6 wins and losses both use corner/edge sources heavily.
   - A blanket corner penalty would damage wins.

2. V6 2P losses are not obviously more opening overcommit-heavy than wins.
   - V6 opening force-risk count is lower in non-first games than first games
     because winning games also spend aggressively from strong corner sources.

3. The more important 2P signal is midgame conversion.
   - V6 non-first games have high mine/regroup rate in `50-150`, but production
     gap still opens by step 100.
   - That suggests defensive/regroup actions happen after the strategic
     production race has already turned, or they protect the wrong corner/edge
     assets.

## Worst V6 2P Non-First Episodes

| Episode | Turns | g50 | g100 | Final prod | Final planets | Final ships | Teams |
|---:|---:|---:|---:|---:|---:|---:|---|
| `22c5eb74-6c67-11f1-89b6-0242ac130202` | 98 | -8 | -64 | 0 | 0 | 0 | Gerar Del Toro / muelsyse111 |
| `ee948e2e-6c01-11f1-b9f7-0242ac130202` | 131 | -12 | -32 | 0 | 0 | 0 | muelsyse111 / Criquet |
| `880948be-6c44-11f1-bfcb-0242ac130202` | 162 | 0 | -20 | 0 | 0 | 0 | muelsyse111 / Flamadesombra |
| `67b70d46-6c5b-11f1-a4cf-0242ac130202` | 500 | -6 | -18 | 1 | 1 | 428 | muelsyse111 / MMMMok |
| `9271ffe2-6c28-11f1-893a-0242ac130203` | 145 | 0 | -16 | 0 | 0 | 0 | muelsyse111 / pantheon of ducks |

These games support a midgame audit:

```text
step 50 can look recoverable,
step 100 often shows decisive production loss,
late regroup cannot recover if the corner/edge production base has been traded
for targets that do not become durable.
```

## Representative 2P Risk Actions

V6 examples from non-first games:

| Episode | Step | Type | srcP | srcCorner | tgtP | tgtCorner | Sent | Commit | Dist | Reaction gap | Captured | Lost |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `7cc817ba-6c02-11f1-ab7d-0242ac130204` | 2 | neutral | 2 | 20.1 | 4 | 36.3 | 12 | 0.86 | 65.4 | -2.6 |  |  |
| `a618ae3e-6c4a-11f1-b4fa-0242ac130204` | 2 | neutral | 2 | 26.0 | 2 | 37.6 | 12 | 0.86 | 98.1 | -85.2 |  |  |
| `1baccc1c-6bfa-11f1-b7f0-0242ac130203` | 3 | neutral | 2 | 36.7 | 3 | 37.0 | 14 | 0.88 | 84.8 | -37.6 |  |  |
| `8b9e6028-6c0c-11f1-8f0b-0242ac130202` | 11 | neutral | 5 | 31.8 | 5 | 31.8 | 20 | 0.80 | 67.7 | -13.0 | 61 |  |
| `22c5eb74-6c67-11f1-89b6-0242ac130202` | 11 | neutral | 4 | 25.9 | 4 | 25.9 | 16 | 0.80 | 68.5 | -20.2 |  |  |

These are not enough to justify a 2P policy change alone because some winning
2P games also contain high-commit corner sends. They do justify a future trace
question:

```text
When a corner/edge source sends far with negative reaction gap, does the target
become a stable production asset by step 50/100?
```

## 2P Decision

Do not change 2P in V9.

Reason:

```text
The 2P evidence is real but not clean enough. V6/V8 2P behavior can be strong,
and broad force-preservation rules could damage winning openings. V9 should
focus on 4P only while preserving CONFIG_2P unchanged.
```

Recommended future 2P-specific branch:

```text
alyce_v10_2p_corner_lifecycle
```

It should be trace-first:

```text
1. Track corner source lifecycle after each high-commit send.
2. Label whether the target becomes stable production by step+30/step+60.
3. Compare high-commit corner sends in wins and losses.
4. Only then add a narrow 2P corner-force filter.
```
