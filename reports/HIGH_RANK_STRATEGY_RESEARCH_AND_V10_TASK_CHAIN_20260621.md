# High-Rank Strategy Research and V10 Task Chain

Date: 2026-06-21

## Executive Decision

Do not continue from V9. The next candidate should start from:

```text
agents/variants/alyce_v6_prod_gap_mode/
```

Selected next strategy:

```text
alyce_v10_v6_role_lock_safe_frontier
```

This is a 4-player-only safety and commitment layer on top of V6. The purpose is not to become more aggressive. The purpose is to preserve V6's production tempo while reducing the third-party cleanup and public-good sacrifice pattern that made V9 underperform.

No Kaggle submission was made in this stage.

## Current Official State

Latest live submission snapshot from Kaggle CLI on 2026-06-21:

| submission | file | public score | status | decision |
|---|---|---:|---|---|
| 53852919 | `alyce_v6_prod_gap_mode_20260619.tar.gz` | 1177.8 | COMPLETE | current official best |
| 53907214 | `alyce_v6_prod_gap_mode_20260619.tar.gz` | 1149.0 | COMPLETE | resubmission, does not replace old best |
| 53904277 | `alyce_v9_4p_mission_router_20260621.tar.gz` | 1061.7 | COMPLETE | reject as promotion candidate |
| 53874866 | `alyce_v8_md_coverage_mission_20260620.tar.gz` | 1008.6 | COMPLETE | reject |
| 53874852 | `alyce_v7_continuous_recovery_20260620.tar.gz` | 1018.1 | COMPLETE | reject |

The txt note recorded V9 at `1081.3`; the current CLI snapshot shows it drifted to `1061.7`. This does not change the decision: V9 remains below V6.

## Inputs Read

Local design note:

```text
C:/Users/zyc/OneDrive/文档/## 总结判断.txt
```

Key local reports considered:

```text
reports/ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md
reports/ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md
reports/ALYCE_V678_2P_CORNER_FORCE_REVIEW_20260620.md
reports/V7_PAUSE_AND_MD_COVERAGE_RECHECK_20260620.md
reports/ALYCE_V9_OFFICIAL_REPLAY_CODE_DISCUSSION_REVIEW_20260621.md
reports/SCORECARD.md
```

Fresh Kaggle caches created or refreshed:

```text
external/leaderboard_orbit_wars_20260621_refresh.txt
external/kaggle_code_score_desc_20260621_refresh.txt
external/kaggle_code_date_run_20260621_refresh.txt
external/kaggle_topics_hot_20260621_refresh.txt
external/kaggle_topics_top_20260621_refresh.txt
external/kaggle_topics_active_20260621_refresh.txt
external/kaggle_datasets_orbit_wars_replay_20260621_refresh.csv
```

Replay parquet summaries:

```text
outputs/high_rank_strategy_20260621/player_overall_summary.csv
outputs/high_rank_strategy_20260621/player_mode_summary.csv
outputs/high_rank_strategy_20260621/phase_snapshots.csv
outputs/high_rank_strategy_20260621/action_phase_summary.csv
outputs/high_rank_strategy_20260621/summary.json
```

The reproducible analysis script is:

```text
scripts/analyze_high_rank_replay_parquet.py
```

## Leaderboard Visibility Audit

The current leaderboard top names are visible, but their private code and internal strategy are not visible.

Top snapshot from `kaggle competitions leaderboard orbit-wars --show`:

| rank | team | score |
|---:|---|---:|
| 1 | Isaiah @ Tufa Labs | 1733.6 |
| 2 | Jake Will | 1679.4 |
| 3 | Boey | 1577.6 |
| 4 | flg | 1551.7 |
| 5 | Hober Malloc | 1551.3 |
| 6 | Felix M Neumann | 1523.5 |
| 7 | M & J & M.ver2 | 1505.3 |
| 8 | moriiiiiiiiim | 1503.2 |
| 9 | Audun Ljone Henriksen | 1502.4 |
| 10 | Vadasz & Ascalon | 1495.4 |

Visible:

- team names
- current public rating snapshot
- public notebook and dataset metadata
- public replay datasets where available

Not visible:

- private submission code
- exact runtime decision tree for top current submissions unless the team made it public
- private training checkpoints

Therefore this report does not claim to know the private strategy of Isaiah, Jake Will, Boey, or other current top teams. It only uses public replay data and public discussion/code evidence.

## Expanded Public Sources

### Kaggle Code

The refreshed Code list still shows the strongest public buckets are not Vkhydras-style light heuristics. Notable public sources:

| source | visible idea |
|---|---|
| `romantamrazov/orbit-wars-i-m-stronger` | strong public output candidate |
| `caoyupeng/v2-gru` | neural/GRU public output candidate |
| `shummingfang/orbit-wars-exp50` | strong public output candidate |
| `alycemiki/light-ver-1200-simple-orbit-intruder` | Alyce base family |
| `ranjeet258/orbit-wars-producer` | greedy ROI producer family |
| `pilkwang/orbit-wars-meta-snapshot-0621` | multi-variant portfolio/meta snapshot |
| `evgendvorkin/orbit-wars-v8-max-1250-score` | staged planner with defense, race, blackout, endgame gates |
| `AmgedAlfaqih/apex-hybrid-dynamic-ring-control-border-defense` | ring control, border defense, ROI curves |
| `slawekbiel/am-i-in-the-top-10-replays-yet` | replay mining workflow |

The important lesson is structural: high public work is converging on projected value, race/holdability checks, defense, and mode-specific logic. Pure scalar target penalty is too shallow.

### Discussion

Relevant public discussion evidence:

- `701894 Orbit Wars Daily Episode Datasets`: official daily episode datasets export top average-rated games up to 20 GB per day.
- `697413 Orbit Wars top-10% daily episode replay datasets`: top replay datasets are meant for opponent analysis, imitation learning, and high-leaderboard spectating.
- `704113 Introducing "The Producer" agent`: a simple planner is strong because it only sends ships when projected production value justifies it, then forwards spare ships to better frontier positions.
- `699003 Some considerations on evaluating targets`: target value must account for horizon/arrival and contested value; typical targets are not enough.
- `704741 Lessons learned so far in this competition`: for heuristic agents, the next unlock is adding solving/optimization rather than static rules.
- `708209 I cloned the #1 bot from its replays`: behavior cloning can reproduce typical moves but misses the search/lookahead behind them.
- `709418 Most of the games now are 4 players`: official response says the scheduler emits equal numbers of 2P and 4P games, which creates twice as many 4P seats as 2P seats.

Consequence: 4P must be treated as a first-class mode, but 2P should not be degraded just to patch 4P.

### Replay Datasets

Public datasets found:

| dataset | use |
|---|---|
| `kaggle/orbit-wars-episodes-index` | official daily episode dataset index |
| `kaggle/orbit-wars-episodes-2026-06-20` | current large official daily episode dump, not fully downloaded |
| `pawanmali/orbit-wars-elite-trajectories` | Elo >=1650 derived state/action features, README and loader inspected; large arrays not downloaded |
| `nbridelancetb/orbit-wars-replay-parquet` | May 2026 top-20 replay parquet subset, lightweight files downloaded and analyzed |
| `baseershah/orbit-wars-scraped-replays` | raw replay source candidate for later |
| `bovard/orbit-wars-top10-episodes-*` | daily top-10% replay datasets from April/May |

## Public High-Rank Replay Analysis

Dataset analyzed:

```text
nbridelancetb/orbit-wars-replay-parquet
```

Loaded subset:

```text
episodes.parquet
player_episodes.parquet
tick_summary.parquet
actions.parquet
episode_planets.parquet
```

Not loaded:

```text
planet_state.parquet
```

Reason: it is a larger full-state file. This pass focused on phase-level production, ships, fleet count, and source-level launch behavior.

Dataset size:

| metric | value |
|---|---:|
| episodes | 4992 |
| player rows | 11852 |
| actions | 3507229 |
| 2P games | 4058 |
| 4P games | 934 |

Current leaderboard names found in this May dataset include `Isaiah @ Tufa Labs`, `Jake Will`, `Vadasz`, and `Audun Ljone Henriksen`. This is historical May replay data, not direct proof of their current private submissions.

### 4P Winner vs Non-Winner Phase Pattern

Aggregate 4P winners:

| tick | avg production | avg planets | avg ships |
|---:|---:|---:|---:|
| 20 | 9.224 | 2.971 | 80.679 |
| 50 | 18.641 | 6.238 | 307.889 |
| 100 | 34.207 | 11.854 | 767.409 |
| 150 | 47.367 | 17.085 | 1592.984 |
| 200 | 53.816 | 19.971 | 2769.633 |

Aggregate 4P non-winners:

| tick | avg production | avg planets | avg ships |
|---:|---:|---:|---:|
| 20 | 8.676 | 2.827 | 79.755 |
| 50 | 13.456 | 4.555 | 237.878 |
| 100 | 10.513 | 3.729 | 261.423 |
| 150 | 6.871 | 2.502 | 235.476 |
| 200 | 5.039 | 1.877 | 247.535 |

The decisive gap is not just step 20. The decisive gap is the conversion from step 50 production into step 100 durable production. V9 improved part of the early window but failed to preserve it into step 100.

### 4P Launch Source Pattern

4P winners:

| phase | avg ships/action | median ships/action | high-prod source rate |
|---|---:|---:|---:|
| opening 0-50 | 29.008 | 22.0 | 0.481 |
| mid 50-150 | 39.278 | 22.0 | 0.403 |
| late mid 150-300 | 65.513 | 8.0 | 0.318 |
| end 300-500 | 259.021 | 14.0 | 0.299 |

4P non-winners:

| phase | avg ships/action | median ships/action | high-prod source rate |
|---|---:|---:|---:|
| opening 0-50 | 26.064 | 20.0 | 0.461 |
| mid 50-150 | 35.180 | 20.0 | 0.375 |
| late mid 150-300 | 36.221 | 10.0 | 0.283 |
| end 300-500 | 54.564 | 3.0 | 0.173 |

Interpreted cautiously:

- winners do not spam tiny early moves more than losers;
- winners are slightly more consolidated in ship commitment;
- winners keep using high-production sources into midgame;
- the public parquet subset does not include target ids in the action table, so this pass cannot prove exact target preference.

## Connection to V6 / V9 Evidence

From the txt and previous reports:

| variant | 4P non-first step50 prod/gap/rank | 4P non-first step100 prod/gap/rank | opening cleanup risk | mid cleanup risk |
|---|---|---|---:|---:|
| V6 | `9.35 / -6.87 / 2.78` | `7.22 / -19.39 / 2.87` | 14.06% | 9.75% |
| V8 | `9.89 / -9.78 / 3.11` | `9.00 / -28.56 / 2.56` | not selected | not selected |
| V9 | `11.91 / -5.73 / 2.55` | `8.09 / -23.73 / 2.82` | 26.27% | 20.46% |

High-rank public replay data says winners need step50 to step100 durable production. V9 increased early activity but also increased third-party cleanup risk. That is the wrong trade.

The next candidate should not add more attack. It should convert V6's already-good official score into safer 4P survival by blocking the specific actions that create public goods for third parties.

## Selected Strategy

Selected candidate:

```text
alyce_v10_v6_role_lock_safe_frontier
```

Base:

```text
agents/variants/alyce_v6_prod_gap_mode/
```

Mode scope:

```text
2P: unchanged
3P: unchanged
4P: enable V10 safety layer
```

Core idea:

```text
Do not choose missions at the candidate tail after all scoring is done.
In 4P, lock the source/region mission first, then veto actions that violate
holdability, source survival, or public-good risk.
```

Modules:

1. `mission_identity_lock`
   - Determine whether this source should expand, hold, reinforce, regroup, or attack.
   - Avoid mixed early behavior from the same source cluster.

2. `source_region_commitment_lock`
   - Track commitment from current observed fleets and source region, not fragile long-lived hidden state.
   - Prevent same source region from alternating between expansion, recapture, and attack within a short window.

3. `launch_blackout_and_source_cooldown`
   - After a risky or large launch from a source, temporarily lower or veto additional launches from the same source/region.
   - Goal: preserve living force and avoid exposing border planets.

4. `anti_public_good_action_veto`
   - Veto actions that weaken us while creating an easy capture for a third player.
   - Use enemy proximity count, arrival race gap, source depletion, and projected post-launch reserve.

5. `forward_holdability_check_lite`
   - Approximate whether the target/source state remains holdable after ETA plus a small margin.
   - This is a lightweight heuristic, not a full search rewrite.

6. `replay_metric_guardrail`
   - Measure cleanup-risk proxy, step50 production, step100 production gap, and 4P non-first behavior before packaging.

Explicitly rejected:

- continuing from V9;
- broad 2P modification;
- pure center rush;
- increasing raw launch volume;
- imitation-only strategy;
- treating current leaderboard private strategies as known.

## Full Task Chain

### Stage 0 - Freeze Research Baseline

Status: completed in this report.

Actions:

```text
1. Read txt conclusion.
2. Confirm current official best.
3. Refresh leaderboard, submissions, Code, Discussion, datasets.
4. Analyze public high-rank replay parquet.
```

Artifacts:

```text
reports/HIGH_RANK_STRATEGY_RESEARCH_AND_V10_TASK_CHAIN_20260621.md
configs/alyce_v10_strategy_selection.yaml
scripts/analyze_high_rank_replay_parquet.py
```

### Stage 1 - Create V10 From V6

Copy:

```text
agents/variants/alyce_v6_prod_gap_mode/
```

to:

```text
agents/variants/alyce_v10_v6_role_lock_safe_frontier/
```

Do not copy V7/V8/V9 changes except measured constants that are independently justified.

Report:

```text
reports/ALYCE_V10_BASELINE_FREEZE_20260621.md
```

### Stage 2 - Add 4P Context Detector

Implement a minimal detector:

```python
is_four_player = observed_player_count >= 4
early = step <= 80
mid = 80 < step <= 180
late = step > 180
```

Do not alter 2P/3P action scoring.

Report:

```text
reports/ALYCE_V10_MODE_CONTEXT_IMPLEMENTATION_20260621.md
```

### Stage 3 - Implement Mission Identity Lock

For each source/source-region in 4P, choose one mission family:

```text
hold_source
safe_expand
reinforce_frontier
counter_only_if_clean
late_attack
```

Veto action families that conflict with the locked mission during early and midgame.

Acceptance condition:

```text
No source cluster should create expansion+enemy-pressure+recapture loops in the first 80 turns unless source reserve remains safe.
```

### Stage 4 - Implement Source Cooldown and Blackout

Rules:

```text
1. Large launch from source -> cooldown.
2. Border source under multi-enemy proximity -> blackout unless reinforcing or escaping.
3. High-production source below reserve floor -> no discretionary launch.
4. Newly captured source -> no non-defense launch until stabilized.
```

This targets the V9 failure where candidate penalties were too late.

### Stage 5 - Implement Anti-Public-Good Veto

Veto if:

```text
1. two or more enemies can benefit from our launch;
2. target is contested and our arrival is not clearly first/decisive;
3. post-launch source reserve falls below local threat margin;
4. projected target would be immediately cleaned by a third party;
5. action improves the current strongest opponent more than us.
```

This is the central 4P game-theory patch.

### Stage 6 - Implement Forward Holdability Check Lite

Do not build a full simulator yet. Add a cheap check:

```text
value_after_eta = target_production_gain - enemy_arrival_risk - source_depletion_risk
```

Only allow early 4P expansion/attack when:

```text
value_after_eta > threshold
```

or the action is defensive.

### Stage 7 - Local Smoke and Determinism Gate

Run:

```bash
python -m py_compile agents/variants/alyce_v10_v6_role_lock_safe_frontier/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v10_v6_role_lock_safe_frontier
```

Report:

```text
reports/ALYCE_V10_SMOKE_AND_DETERMINISM_20260621.md
```

### Stage 8 - Local 4P Screen

Minimum:

```text
v10 + v6 + v8 + v9, 12 games, rotated positions
v10 + v6 + Alyce original + Producer-like public candidate, 12 games
v10 + v6 + strongest local public output pool, 12 games if loader supports it
```

Metrics:

```text
avg rank
rank<=2 rate
early death
step50 production
step100 production
cleanup-risk proxy
source blackout count
veto count by reason
```

Report:

```text
reports/ALYCE_V10_LOCAL_4P_EVAL_20260621.md
```

### Stage 9 - 2P Regression Gate

Because V10 should not touch 2P, run:

```text
v10 vs v6, 20 seeds bidirectional
v10 vs Alyce original, 20 seeds bidirectional
```

Go/no-go:

```text
2P should be statistically indistinguishable from V6 except for harmless deterministic tie differences.
```

### Stage 10 - Replay-Metric Comparison Against V6/V9

Compare V10 local traces and any official-like replays against:

```text
V6 cleanup risk: opening 14.06%, mid 9.75%
V9 cleanup risk: opening 26.27%, mid 20.46%
High-rank public 4P winner trajectory: step50 production 18.641, step100 production 34.207
```

V10 does not need to match high-rank production immediately. It must at least avoid V9's cleanup-risk regression.

### Stage 11 - Package Confirmation Only

If local gates pass:

```text
dist/alyce_v10_v6_role_lock_safe_frontier_20260621.tar.gz
```

Generate:

```text
reports/PACKAGING_REPORT_ALYCE_V10_20260621.md
reports/SUBMIT_CONFIRM_ALYCE_V10_20260621.md
```

Do not submit without explicit user confirmation.

## Go / No-Go Rule

V10 can proceed to package confirmation only if:

```text
1. It starts from V6 and leaves 2P/3P effectively unchanged.
2. 4P local average rank is not worse than V6.
3. cleanup-risk proxy is lower than V9 and preferably lower than V6.
4. step50 production is not materially worse than V6.
5. step100 production/gap is not worse than V9.
6. no errors/timeouts.
```

If these fail, do not submit. Revert the V10 layer and keep V6 as official best.

## Source Links

- Kaggle competition leaderboard: https://www.kaggle.com/competitions/orbit-wars/leaderboard
- Official daily episode dataset index: https://www.kaggle.com/datasets/kaggle/orbit-wars-episodes-index
- Top-20 replay parquet dataset: https://www.kaggle.com/datasets/nbridelancetb/orbit-wars-replay-parquet
- Elite trajectories dataset: https://www.kaggle.com/datasets/pawanmali/orbit-wars-elite-trajectories
- Producer discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/704113
- Daily episode datasets discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/701894
- Top-10 replay datasets discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/697413
- 4P scheduling discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/709418
- Clone top bot discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/708209
- Lessons learned discussion: https://www.kaggle.com/competitions/orbit-wars/discussion/704741
