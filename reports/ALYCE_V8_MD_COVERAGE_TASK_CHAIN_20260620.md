# Alyce V8 MD Coverage Task Chain - 2026-06-20

## Goal

Continue from the V6 official best and cover the full replay/report evidence
base without pretending that one more threshold tweak is a complete 4P strategy.

## Stage 0 - Freeze Current Best

Status: complete.

```text
official best: alyce_v6_prod_gap_mode
submission_id: 53852919
public score snapshot: 1177.8
V7 status: paused research draft, not submitted
```

## Stage 1 - Coverage Matrix

Status: complete.

Output:

```text
reports/ALYCE_REPLAY_MD_COVERAGE_MATRIX_20260620.md
```

Finding:

```text
V8 must preserve V6, add trace/snapshots, add multi-size source safety, and
avoid broad static far-low penalties.
```

## Stage 2 - Evaluation Tooling

Status: complete.

Change:

```text
scripts/run_eval_tournament.py
```

The local tournament CSV now records:

```text
snapshot_20
snapshot_50
snapshot_100
snapshot_150
snapshot_200
```

Each snapshot stores per-player:

```text
prod
prod_gap
prod_rank
planets
ships
```

This directly matches the replay reports' recurring step 50/100 production-gap
diagnosis.

## Stage 3 - V8 Candidate Implementation

Status: complete.

New candidate:

```text
agents/variants/alyce_v8_md_coverage_mission
```

Implemented:

```text
1. V6 official-best base.
2. 4P multi-size drain tiers: 60%, 80%, 100%.
3. True production-leader gap.
4. V8 recovery-risk selected-action filter.
5. Candidate top-label trace via ORBIT_V8_TRACE_PATH.
6. Low-impact leader/kingmaker risk label.
```

Not implemented by design:

```text
full third-party cleanup simulation
full mission generator
rank-improvement counterfactual
multi-source contested-neutral swarm
```

## Stage 4 - Verification Plan

Minimum verification before any submission discussion:

```text
python -m py_compile agents/variants/alyce_v8_md_coverage_mission/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v8_md_coverage_mission
```

Small local screens:

```text
V8 vs V6, seeds 1-3 bidirectional
V8 vs V2, seeds 1-3 bidirectional
V1/V2/V6/V8 4P with V8 in each seat, seeds 1-3
```

Trace check:

```text
ORBIT_V8_TRACE_PATH=outputs/v8_eval/trace/v8_vs_v6_seed1.jsonl
```

The trace must show whether V8 actually triggers candidate labels rather than
silently behaving like V6.

## Stage 5 - Go / No-Go Rule

Do not submit V8 unless:

```text
errors = 0
timeouts = 0
V8 does not collapse in 4P rotated screen
trace shows understandable interventions
V8 preserves or improves V6 in direct local screens
```

If these gates fail:

```text
keep V6 as official best
use V8 trace to decide whether selected-action filters are exhausted
next branch should implement trace-first FFA context / reaction map, not submit
```
