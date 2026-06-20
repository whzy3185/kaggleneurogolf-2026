# Alyce V9 4P Mission Router And 2P Corner Review Task Chain - 2026-06-20

## Goal

Continue from the official-best V6 branch and address the reports created after
V6 without dropping any constraint. The work has two parallel tracks:

```text
Track A: improve 4P strategy with a mission-level router before greedy scoring.
Track B: open a 2P replay review focused on corner/edge play and force preservation.
```

No Kaggle submit is part of this task chain.

## Current State

```text
latest commit before this chain: 7587f2e
official best: V6 alyce_v6_prod_gap_mode
submission_id: 53852919
public score: 1177.8
V7 official score: 920.2, rejected
V8 official score: 1134.8, rejected as promotion candidate
```

## V6-And-Later Reports Covered

The following reports were reviewed for this chain:

```text
reports/ALYCE_V6_PROD_GAP_TASK_CHAIN_20260619.md
reports/ALYCE_V6_LOCAL_EVAL_20260619.md
reports/ALYCE_V6_SUBMISSION_RESULT_20260619.md
reports/ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md
reports/V7_PAUSE_AND_MD_COVERAGE_RECHECK_20260620.md
reports/ALYCE_REPLAY_MD_COVERAGE_MATRIX_20260620.md
reports/ALYCE_V8_MD_COVERAGE_TASK_CHAIN_20260620.md
reports/ALYCE_V7_V8_SUBMISSION_RESULT_20260620.md
reports/ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md
reports/SCORECARD.md
```

Older reports remain background context through the coverage matrix, especially:

```text
ALYCE_52_REPLAY_REVIEW_20260618.md
TXT_BASED_4P_IMPROVEMENT_DESIGN_20260618.md
OFFICIAL_REPLAY_PHASE_REVIEW_20260618.md
V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md
ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md
```

## Consolidated Constraints

### Preserve

```text
1. Start from V6, not V7/V8/V3/V4.
2. Preserve Alyce orbit-lite planner and 2P default behavior.
3. Preserve V6 source reserve, V5/V6 selected-action trace/filter, and V6 prod-gap mode.
4. Keep local eval phase snapshots.
5. Treat local simulation as regression evidence only, not official truth.
```

### Do Not Repeat

```text
1. Do not use broad static far-low penalties as the primary fix.
2. Do not rely on selected-action recovery alone.
3. Do not add supplemental moves after the base already spent ships.
4. Do not hardcode opponent names.
5. Do not submit from small local screens.
```

### Must Add For 4P

```text
1. Candidate-level reaction map before greedy selection.
2. Center / middle-galaxy danger label.
3. Opening safe-expansion gate.
4. Anti-focus source reserve and public-sacrifice penalty.
5. Leader intervention only when target is holdable and rank-improving.
6. Trailing recovery veto for low-impact enemy and far unsafe neutral actions.
```

### Must Start For 2P

```text
1. Replay analysis of V6/V7/V8 2P episodes.
2. Corner/edge target and source labels.
3. Source force-preservation risk in corner/edge positions.
4. Identify whether 2P losses come from early corner overcommit or later conversion.
5. Do not change 2P policy until replay evidence justifies it.
```

## Stage 1 - Extend Replay Analyzer

Status: planned.

Extend:

```text
scripts/analyze_4p_game_theory_replays.py
```

Add per-action fields:

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

Rerun on:

```text
D:\orbitwars_replays\alyce_v6_latest\episodes
D:\orbitwars_replays\alyce_v7_latest\episodes
D:\orbitwars_replays\alyce_v8_latest\episodes
```

## Stage 2 - 2P Replay Review

Status: planned.

Output:

```text
reports/ALYCE_V678_2P_CORNER_FORCE_REVIEW_20260620.md
```

Must answer:

```text
1. Do 2P losses separate by step 50/100 production gap?
2. Are losing openings more corner/edge overcommit-heavy?
3. Are high-production corner sources depleted too early?
4. Does 2P need a policy change, or only future trace evidence?
```

## Stage 3 - Implement V9 4P Mission Router

Status: planned.

New variant:

```text
agents/variants/alyce_v9_4p_mission_router
```

Base:

```text
agents/variants/alyce_v6_prod_gap_mode
```

Implementation scope:

```text
1. Add V9 config flags in 4P only.
2. Add candidate-level close-enemy-count and production-rank/gap features.
3. Penalize or veto opening far/center/shared-zone missions before greedy selection.
4. Penalize anti-focus risks: source depletion plus multiple enemy reaction access.
5. Penalize low-impact leader/non-leader enemy targets while trailing.
6. Preserve 2P and 3P configs unchanged.
```

Do not include:

```text
new neural training
opponent-name logic
new action injection
large orbit_lite rewrites
Kaggle submission
```

## Stage 4 - Validation

Minimum checks:

```text
python -m py_compile agents/variants/alyce_v9_4p_mission_router/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v9_4p_mission_router
```

Local screens:

```text
V9 vs V6, seeds 1-3 bidirectional
V9 vs V8, seeds 1-3 bidirectional
V6/V7/V8/V9 4P, V9 in each position, seeds 1-3 if time permits
```

Evaluation focus:

```text
errors/timeouts
2P non-regression
4P step50/100 production gap
opening center/shared-zone risky actions
whether V9 preserves V6 tempo
```

## Stage 5 - Reports

Output:

```text
reports/ALYCE_V9_4P_MISSION_IMPLEMENTATION_20260620.md
reports/ALYCE_V9_LOCAL_EVAL_20260620.md
```

Decision:

```text
Do not submit V9 in this chain.
Promote only if later official-style evidence supports it.
```
