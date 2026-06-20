# Alyce Replay MD Coverage Matrix - 2026-06-20

## Purpose

This report consolidates the replay and strategy markdown files that drove the
Alyce line of work. The goal is to prevent another narrow patch from claiming to
cover the whole evidence base.

Current official best in this repo:

```text
agent: alyce_v6_prod_gap_mode
submission_id: 53852919
public score snapshot: 1177.8
```

## Reviewed Documents

| Document | Main evidence | Required response |
|---|---|---|
| `ALYCE_INTRUDER_FULL_CODE_DECISION_REPORT.md` | Alyce is a greedy producer/orbit-lite planner with dynamic ROI, target scoring, regroup, and utility code. | Preserve Alyce/Producer structure unless a change has strong evidence. |
| `ALYCE_ELO_AND_OPPONENT_STRATEGY_RECHECK.md` | Public discussion mentioned ELO/local variance and opponent-sensitive behavior. | Do not overfit a single local matchup; use phase/rank evidence. |
| `ALYCE_52_REPLAY_REVIEW_20260618.md` | 4P failures are early/mid production conversion, source depletion, poor holdability, missing rank-aware enemy labels. | Add FFA labels, reaction gap, source safety, rank/production trace, multi-size drain. |
| `TXT_BASED_4P_IMPROVEMENT_DESIGN_20260618.md` | First-principles 4P mission layer: safe/trap neutral, leader asset, threat neighbor, rear enemy, rank/survival value, multi-size drain. | Build FFA context/reaction map/mission trace before trusting policy. |
| `OFFICIAL_REPLAY_PHASE_REVIEW_20260618.md` | Phase split matters; opening/mid/late patterns differ. | Local eval must record step 50/100/150 metrics, not only final rank. |
| `ALYCE_FIRST_VERSION_FAILURE_COMMONALITY_20260619.md` | First version losses share target-quality and source-budget problems. | Avoid broad aggression; inspect concrete bad decisions. |
| `V2_LATEST_REPLAY_AND_V3_SUBMISSION_SYNTHESIS_20260619.md` | V2 official improved but 4P holes remain; V3 was submitted and should be judged from official replay, not local guess. | Require trace instrumentation and production-gap validation. |
| `V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md` | Broad far-low penalty did not fix 4P collapse; leader-pressure can become kingmaking. | Avoid static penalties; require holdability/rank context. |
| `ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md` | V4 failed because it used the wrong parent branch and a broad scorer without replacement proof. | Start from V2/V6, not V3/V4; only change top action with safe alternatives. |
| `ALYCE_V5_IMPROVEMENT_TASK_CHAIN_20260619.md` | V5 introduced selected-action trace/filter but should be narrow. | Keep selected-action proof; do not trust untraced policy changes. |
| `ALYCE_V5_LOCAL_EVAL_20260619.md` | Determinism/local screens are noisy; V5 was not enough. | Keep local eval but treat it as evidence, not official truth. |
| `ALYCE_V6_PROD_GAP_TASK_CHAIN_20260619.md` | V6 should add production-gap mode on V2/V5 trace line. | Preserve V6 as the official best base. |
| `ALYCE_V6_LOCAL_EVAL_20260619.md` | Local 4P was pessimistic; V6 branch triggered too rarely; recommended wider V7/V8 risk score and better trace. | Add candidate-label trace and production snapshots. |
| `ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md` | V6 official score is best, but 4P non-first games still fall behind by step 50/100. | Start from V6, widen risk gate, preserve tempo, avoid blind submission. |

## Requirement Coverage

| Requirement | Evidence source | V8 action |
|---|---|---|
| Keep V6/V2 base, not V3/V4 | V4 cause analysis, V6 official review | V8 copies `alyce_v6_prod_gap_mode`. |
| Preserve Alyce tempo and orbit-lite structure | Alyce full code report | V8 keeps bundled `orbit_lite` and planner structure. |
| Add phase production metrics to local eval | official phase review, V6 review | `scripts/run_eval_tournament.py` now writes `snapshot_20/50/100/150/200`. |
| Record production rank/gap | V2/V3/V6 reviews | Snapshots include `prod`, `prod_gap`, and `prod_rank` per player. |
| Add candidate-label trace | 52 replay review, V5/V6 eval | V8 trace writes top candidate labels via `ORBIT_V8_TRACE_PATH`. |
| Compare to true production leader | V6 review | V8 uses `prod_by_owner.argmax()` for production gap. |
| Source depletion protection | 52 replay review, txt design | V8 retains V6 source reserve and adds multi-size send tiers. |
| Multi-size drain | txt design, 52 replay review | V8 4P exposes 60/80/100 percent safe-drain candidates. |
| Reaction gap / holdability proxy | txt design, V3/V6 reviews | V8 includes reaction gap in risk and alternative acceptance. |
| Avoid unholdable low-value targets while trailing | V6 review | V8 risk combines target production, distance, reaction gap, and source depletion. |
| Leader/kingmaker guard | txt design, V3 review | V8 marks low-impact leader targets as risky in recovery mode. |
| Preserve selected-action replacement proof | V4/V5 reports | V8 only changes current top action when a close safer alternative exists. |
| Avoid broad static far-low penalty | V3/V6 reviews | V8 uses gated risk only after production position is degraded. |

## Still Not Fully Covered

These items are intentionally not claimed as complete in V8:

```text
full third-party cleanup simulation
true post-arrival holdability forecast
rank-improvement counterfactual for leader pressure / elimination
contested-neutral multi-source swarm timing
full FFA mission generator separate from candidate scoring
```

They require deeper planner surgery and should only follow if V8-style trace
shows that selected-action filtering cannot repair the remaining 4P failures.

## Execution Decision

Implement V8 as an evidence-coverage candidate:

```text
base: alyce_v6_prod_gap_mode
variant: agents/variants/alyce_v8_md_coverage_mission
submit: no
promotion: no
validation: smoke + small 1v1 + small 4P rotated screen
```
