# Alyce 4P FFA V2 Submission And Short Eval

Date: 2026-06-19

## Summary

User explicitly requested a Kaggle submission of the V2 variant while local
optimization continues. One V2 package was submitted. The submission is pending
at the time this report was written.

V2 is a research variant, not a proven final candidate. Local short eval shows
it is not stronger than the full Alyce Intervention public output. The next
optimization should move to the full Intervention/ProducerLite v15 codebase
rather than continuing to patch the older Light-derived V2 path.

## Package

Candidate:

```text
agents/variants/alyce_4p_ffa_v2
```

Submitted package:

```text
dist/alyce_4p_ffa_v2_20260619.tar.gz
```

Archive root contents:

```text
main.py
orbit_lite/
```

SHA256:

```text
44805225F46B24B582BCB71042726050F23F5C6AEBF3F4BECCB0CCC024F5AF4C
```

Size:

```text
56680 bytes
```

Pre-submit checks:

```text
python -m py_compile agents/variants/alyce_4p_ffa_v2/main.py
python scripts/smoke_candidate.py agents/variants/alyce_4p_ffa_v2
```

Result:

```text
py_compile: pass
smoke_candidate: pass
sample_actions_ok: true
env_status: ok
```

## Kaggle Submission

Command executed after explicit user instruction:

```text
kaggle competitions submit -c orbit-wars -f dist/alyce_4p_ffa_v2_20260619.tar.gz -m "alyce_4p_ffa_v2_soft_contested_filter_20260619"
```

Submission list immediately after upload:

```text
ref: 53827977
fileName: alyce_4p_ffa_v2_20260619.tar.gz
description: alyce_4p_ffa_v2_soft_contested_filter_20260619
status: SubmissionStatus.PENDING
publicScore: blank
```

Current official best visible in the same submission list:

```text
agent/package: alyce_intruder_repro_20260618.tar.gz
status: COMPLETE
publicScore: 1062.9
```

No official V2 score is available yet.

## V2 Change Rationale

V1 underperformed in 4P local testing. The key suspected issue was over-filtering:
the old implementation hard-rejected contested neutral candidates. Kaggle Code
and Discussion evidence points in the opposite direction for strong public
agents:

- Producer-style agents use projected ROI and regroup as the main structure.
- Alyce Intervention uses dynamic ROI, floor-sized/multi-tier fleets, comet
  guard/evacuation, and FFA leader pressure inside the planner.
- Public target-veto work uses narrow vetoes, not broad neutral suppression.
- Discussion around Producer and replay imitation repeatedly indicates that
  search/scoring structure matters more than blind post-hoc filters.

Therefore V2 changes were deliberately small:

- severe trap-neutral cases remain hard vetoes;
- ordinary contested neutral cases become a finite score penalty;
- 4P `max_waves_per_turn` was restored from 5 to 6;
- 4P source reserve caps were relaxed.

## Local Short Eval

Raw output files are under `outputs/` and are not committed.

### V2 vs V1

Command:

```text
python scripts/run_eval_tournament.py --series alyce_ffa_v2_pair_v1_short --seeds 1-2 --out outputs/alyce_ffa_v2_pair_v1_short pair local/agents/variants/alyce_4p_ffa_v2 local/agents/variants/alyce_4p_ffa_v1 --bidirectional
```

Result:

```text
games: 4
V2 wins: 2
V1 wins: 2
draws: 0
errors: 0
V2 avg_final_ships: 860.25
V1 avg_final_ships: 817.0
```

Interpretation:

```text
V2 did not show an immediate regression against V1 in this tiny screen.
The sample is too small to claim strength.
```

### V2 vs Alyce Intervention Public Output

Command:

```text
python scripts/run_eval_tournament.py --series alyce_ffa_v2_pair_intervention_short --seeds 1-2 --out outputs/alyce_ffa_v2_pair_intervention_short pair local/agents/variants/alyce_4p_ffa_v2 local/external/kaggle_outputs/alycemiki__intervention-command-w-ffa/submission_extracted --bidirectional
```

Result:

```text
games: 4
V2 wins: 1
Alyce Intervention wins: 3
draws: 0
errors: 0
V2 avg_final_ships: 766.0
Alyce Intervention avg_final_ships: 1168.0
```

Interpretation:

```text
V2 is still weaker than the full Alyce Intervention output in this short
screen. The result supports moving future work onto the full Intervention
codebase instead of continuing to tune the older Light-derived V2.
```

## Current Decision

Submit status:

```text
submitted: true
status: pending
do_not_resubmit_until_result: true
```

Next action:

```text
1. Query Kaggle later for ref 53827977.
2. If V2 errors, inspect package/runtime error before any resubmit.
3. If V2 completes below 1062.9, keep Alyce repro as official best.
4. Start next local optimization from Alyce Intervention/ProducerLite v15, not
   from the Light-derived V2 branch.
```

