# Alyce Intervention V4 Optimization Task Chain - 2026-06-19

## Scope

This task chain is based on all prior Orbit Wars reports in this repository,
especially:

- `ALYCE_INTRUDER_FULL_CODE_DECISION_REPORT.md`
- `ALYCE_ELO_AND_OPPONENT_STRATEGY_RECHECK.md`
- `ALYCE_52_REPLAY_REVIEW_20260618.md`
- `TXT_BASED_4P_IMPROVEMENT_DESIGN_20260618.md`
- `OFFICIAL_REPLAY_PHASE_REVIEW_20260618.md`
- `ALYCE_FIRST_VERSION_FAILURE_COMMONALITY_20260619.md`
- `V2_LATEST_REPLAY_AND_V3_SUBMISSION_SYNTHESIS_20260619.md`
- `V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md`

Current official state before V4:

```text
current official best in repo: V2 submission 53827977
latest visible score: 1087.7
V3 submission 53842450: 1018.9
Alyce repro 53793561: 1069.1
```

Do not submit V4 until it beats the current official-best logic in local
validation and has a submit confirmation card.

## Consolidated Diagnosis

The reports agree on one central point:

```text
The failure is not lack of activity.
The failure is launch conversion in 4P: targets are not reliably holdable, some
leader pressure is low-impact, and attack candidates often beat regroup when the
agent is already losing production position.
```

V3 proved that a static far-low penalty is too narrow. A correct V4 must cover:

1. Candidate-change trace.
2. 2P/4P mode separation.
3. 4P rank/phase policy.
4. Reaction and holdability estimates.
5. Safe/contested/trap neutral labels.
6. Leader/threat/rear enemy labels.
7. Anti-kingmaker behavior.
8. Source protection only where it does not kill winning full-drain tempo.
9. Attack-vs-regroup arbitration.
10. Local evaluation before any package or submit.

## Requirement Matrix

| Prior report requirement | V4 treatment |
|---|---|
| Trace before trusting policy | Add local-only `ORBIT_V4_TRACE_PATH` jsonl trace. |
| Do not globally lower ROI | Keep Intervention ROI/wave machinery unchanged. |
| Do not delete actions broadly | Use soft score changes only. |
| Preserve full-drain tempo when useful | Keep all Intervention candidate size tiers. |
| Reaction map / holdability | Add rough reaction-distance and post-capture margin labels. |
| Trap neutral rejection | Start as soft trap-neutral penalty, not hard veto. |
| Safe neutral bonus | Add small bonus only for high-production, non-reactive neutrals. |
| Leader target nuance | Remove V3's blanket leader-owned exemption for low-value weak targets. |
| Anti-kingmaker | Penalize weak non-leader enemy targets and weak leader targets differently. |
| Source protection | Apply only to high-production source, meaningful pressure, low source-after, and weak target context. |
| Rank/phase mode | Use production rank/gap and step window around 45-170. |
| Attack-vs-regroup | Penalize bad attacks while leaving ships for existing regroup. |
| 2P non-regression | Keep V4 safety scorer gated to 4P only. |
| Validation by rank distribution | Required before package/submit. |

## Stage 0 - Freeze Baseline

Inputs:

```text
reports/SCORECARD.md
reports/V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md
agents/variants/alyce_intervention_v3
external/kaggle_outputs/alycemiki__intervention-command-w-ffa/submission_extracted
```

Output:

```text
reports/ALYCE_INTERVENTION_V4_TASK_CHAIN_20260619.md
```

Gate:

```text
V4 starts as an unsubmitted local candidate.
Current final remains V2.
```

## Stage 1 - V4 Candidate Implementation

Create:

```text
agents/variants/alyce_intervention_v4/
```

Implementation constraints:

- Keep `main.py` + `orbit_lite/` shape.
- Keep `def agent(obs)`.
- Do not change upstream movement, intercept, garrison, or adapter code unless
  required by a measured bug.
- Apply 4P logic inside candidate scoring before greedy selection.
- Do not write trace files unless `ORBIT_V4_TRACE_PATH` is explicitly set.

V4 scoring labels:

```text
prod_rank
prod_gap
leader
far_low_nonleader_enemy
leader_low_value_weak
trap_neutral
safe_neutral
source_protect
trailing_bad_attack
top_changed
```

## Stage 2 - Smoke And Trace Validation

Required checks:

```text
python -m py_compile agents/variants/alyce_intervention_v4/main.py
python scripts/smoke_candidate.py agents/variants/alyce_intervention_v4
```

4P trace smoke:

```text
$env:ORBIT_V4_TRACE_PATH='outputs/alyce_intervention_v4_trace_smoke/trace.jsonl'
python scripts/run_eval_tournament.py --series alyce_intervention_v4_4p_trace_smoke ...
```

Pass criteria:

- syntax pass;
- smoke pass;
- 4P branch no error/timeout;
- trace file contains rank/gap/label counters;
- trace shows top candidate sometimes changes, but not on nearly every turn.

## Stage 3 - Early Micro-Screen

Run only small screens first:

```text
2P:
  V4 vs original Intervention, 2 seeds bidirectional

4P:
  V4 + V3 + original Intervention + V2, 3-5 seeds with position rotation
```

Early failure interpretation:

- If source_protect dominates trace, narrow it.
- If top_changed is near zero, the policy is inert.
- If top_changed is very high and V4 loses, penalties are too invasive.
- If 4P loses with low trap/far-low counters, the missing piece is not those
  labels and needs holdability/regroup refinement.

## Stage 4 - Replay-Inspired Validation

Replay-derived cases to emulate:

- V3 loss `80649187`: leader-owned low-production target was not enough reason
  to attack; need holdability.
- V3 loss `80641852`: repeated far prod-1 neutral actions.
- V3 loss `80643617`: repeated penalty-like far non-leader enemy attacks.
- V2 4P losses: step 50-100 production collapse and excess enemy targeting.
- Alyce 52 replay set: 4P rank-3/4 collapse with low durable production.

Metrics:

```text
errors
timeouts
2P winrate vs original
4P average rank
4P rank<=2 rate
step50 production gap
step100 production gap
trace top_changed rate
trap_neutral count
source_protect count
leader_low_value_weak count
```

## Stage 5 - V4 Tuning Rules

Allowed tuning:

- lower or raise soft penalties;
- narrow source protection;
- adjust trap-neutral penalty;
- adjust leader low-value hold penalty;
- add a small safe-neutral bonus;
- tune only 4P unless 2P evidence requires a separate change.

Not allowed before evidence:

- hard target deletion;
- broad global reserve;
- opponent-name logic;
- disabling full-drain;
- package/submit on smoke alone.

## Stage 6 - Packaging Gate

Only package if:

```text
2P non-regression: no obvious local collapse
4P smoke: no error/timeout
4P screen: V4 not worse than V2/V3/original on average rank
trace: action changes are explainable and bounded
```

If passed:

```text
reports/PACKAGING_REPORT_ALYCE_V4.md
reports/SUBMIT_CONFIRM_ALYCE_V4.md
```

Do not run `kaggle competitions submit` without explicit user confirmation.

## Stage 7 - Official Result Gate

If V4 is later submitted:

- download all visible V4 episodes;
- compare against V2 with the same replay analyzer;
- update `reports/SCORECARD.md`;
- promote only if official score beats V2 and replay failure modes are not
  worse.

## Current Decision

V4 can proceed as a local candidate implementation and trace experiment.

It is not yet a final candidate and is not ready for Kaggle submission.
