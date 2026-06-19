# Alyce V5 Improvement Task Chain - 2026-06-19

## Current Decision

Current practical baseline remains:

```text
agents/variants/alyce_4p_ffa_v2
official submission: 53827977
latest recorded public score: 1087.7
```

Rejected directions:

```text
alyce_intervention_v3: official score below V2
alyce_intervention_v4: local 4P family screen below V2/V1/V3
```

V5 must not continue the V3/V4 branch. It must start from V2 and preserve V2's
working 4P mission filter.

## Evidence To Respect

From previous reports:

1. `ALYCE_52_REPLAY_REVIEW_20260618.md`
   - Alyce is stronger in 2P than 4P.
   - 4P failures are not inactivity; they are poor conversion of launches into
     stable production.

2. `V2_LATEST_REPLAY_AND_V3_SUBMISSION_SYNTHESIS_20260619.md`
   - V2 is current official best in repo.
   - V2 4P losses separate by step 50 and are often strategically dead by step
     100.
   - 4P losses are more enemy-target heavy after step 50.

3. `V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md`
   - Static far-low penalties are too narrow.
   - Need selected-action trace, not just label counts.

4. `ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md`
   - V4 failed because it used the wrong parent branch and only adjusted broad
     candidate scores.
   - Same-seed local reruns were not fully stable, so determinism must be audited
     before trusting small screens.

## Hard Gates

No Kaggle submit during this task chain.

Do not treat local tournament output as official score.

Do not continue if V5 does not beat or at least match V2 locally in the small
family screen.

Do not modify V2 in place. Create a new variant:

```text
agents/variants/alyce_v5_v2_trace_filter/
```

## Stage 0 - Determinism Audit

Goal:

```text
Know whether same seed / same agent order is reproducible enough for local
screening.
```

Implement:

```text
scripts/run_determinism_audit.py
```

Inputs:

```text
--agents <agent paths...>
--seed
--repeats
--out
```

Output:

```text
outputs/determinism_audit_*/matches.csv
outputs/determinism_audit_*/summary.json
```

Report:

```text
reports/ALYCE_V5_DETERMINISM_AUDIT_20260619.md
```

Pass condition:

```text
Winner and score/rank pattern should usually repeat. If not, local eval remains
screen-only and V5 must be judged by larger samples.
```

## Stage 1 - Selected-Action Trace

Goal:

```text
Record the selected source/target/send before and after the new narrow filter.
```

V5 trace path:

```text
ORBIT_V5_TRACE_PATH=outputs/alyce_v5_trace/<case>/trace.jsonl
```

Required fields:

```text
step
player
player_count
before_src
before_tgt
before_send
before_score
after_src
after_tgt
after_send
after_score
changed
reason
my_prod
leader_prod
prod_gap
source_ships
source_prod
target_owner
target_prod
target_ships
target_distance
```

No trace file should be written unless the environment variable is set.

## Stage 2 - V5 Narrow Filter

Base:

```text
agents/variants/alyce_4p_ffa_v2
```

Preserve:

```text
severe trap hard veto
soft contested neutral penalty
safe neutral bonus
source depletion penalty
```

Add only one narrow selected-action filter after the normal V2 score is computed
and before greedy selection:

```text
If 4P and the selected top candidate is clearly low-value and risky,
choose a better-scoring safe alternative only if it is clearly available.
```

Allowed replacement reasons:

```text
far_low_neutral_with_safe_alt
far_low_nonleader_enemy_with_safe_alt
source_depletion_with_safe_alt
```

Do not add new attacks. Do not force regroup. Do not hardcode opponents.

Replacement gate:

```text
alternative must be valid,
alternative score must be close enough to original,
alternative target production must be higher or reaction/holdability safer,
alternative must not worsen source depletion,
candidate switch only affects the selected top candidate for one greedy wave.
```

## Stage 3 - Local Validation

Minimum smoke:

```text
python -m py_compile agents/variants/alyce_v5_v2_trace_filter/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v5_v2_trace_filter
```

Minimum local screen:

```text
1v1:
  V5 vs V2, seeds 1-3 bidirectional
  V5 vs V1, seeds 1-3 bidirectional

4P:
  V1/V2/V3/V5 with V5 rotated across positions, seeds 1-3
```

Pass condition:

```text
V5 should not be below V2 in 4P average rank and should not show error/timeout.
```

## Stage 4 - Go / No-Go

Generate:

```text
reports/ALYCE_V5_LOCAL_EVAL_20260619.md
```

If V5 loses the small local family screen:

```text
reject V5, keep V2
```

If V5 is close or better:

```text
run larger screen before any package or submit card
```

No Kaggle submit in this task chain.

