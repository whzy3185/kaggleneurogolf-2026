# Adaptive Failure Analysis

Date: 2026-06-17

Scope: local analysis only. No Kaggle submission was run.

## Trigger

Stage 3 direct tournament showed adaptive_full is clearly weaker than the selected base:

| matchup | games | base wins | adaptive_full wins | timeout/errors |
| --- | ---: | ---: | ---: | ---: |
| base vs adaptive_full, seeds 1-50, bidirectional | 100 | 97 | 3 | 0 |

Public-opponent seed-1 screening also showed adaptive_full only beats starter and loses both sides to six stronger public agents.

Because this meets the stop condition, adaptive_full is rejected as a packaging or submission candidate.

## Checked Failure Modes

| check | finding |
| --- | --- |
| Supplemental moves stealing base ship budget | Likely. adaptive_full runs base first, then appends extra moves from remaining ships. This can alter source-planet reserves and send budget without being part of the base planner's target scoring. |
| Base actions consume all ships before counters matter | Likely. The wrapper has no budget reservation before calling the base agent, so counter moves only use leftovers. |
| Confidence gate too low/high | Mixed. Stage 2 profile traces showed strong agents often trigger overcommitter/neutral_rusher/crash_exploiter labels; those labels can become actionable without proving that the added response improves the base plan. |
| neutral_rusher false response | Likely risk. Strong expansion agents commonly look like neutral rushers, but counterattacking them through post-actions performed poorly. |
| turtle response causing over-expansion | Possible. Turtle branch increases expansion and comet weighting, which can reinforce the wrong behavior when the opponent is simply not attacking early. |
| comet_greedy long-distance sending | Possible. comet_greedy did not materially trigger in Stage 2, but it remains unproven and should stay disabled until targeted tests exist. |
| overcommitter unsafe counterattack | Likely risk. The branch increases counterattack bonus and can increase max commit ratio, which conflicts with the current need to preserve base stability. |

## Defense-Only Check

A quick seed-1 bidirectional smoke was run:

```text
python scripts/run_eval_tournament.py --series estimate_base_defense_only --seeds 1 --out outputs/tournament_raw/estimate_base_defense_only --progress pair local/agents/base_agent_entry local/agents/variants/adaptive_defense_only --bidirectional
```

Result:

| matchup | games | base wins | defense_only wins | timeout/errors |
| --- | ---: | ---: | ---: | ---: |
| base vs adaptive_defense_only, seed 1, bidirectional | 2 | 2 | 0 | 0 |

This is only a smoke check, but it is enough to avoid selecting defense_only as the current final candidate.

## Stage 4 Decision

Selected current final candidate:

```text
base_safe_fallback
```

Entrypoint:

```text
local/agents/base_agent_entry
```

Rationale:

- base is the only candidate with strong direct evidence in the local tournament;
- adaptive_full has a severe negative result;
- defense_only is not yet proven safe;
- continuing to package adaptive_full would violate the task's "do not blindly add functionality" instruction.

## Constraints For Next Adaptive Attempt

The next adaptive implementation should be constrained before another full tournament:

1. Supplemental moves must have a small explicit budget cap.
2. No policy may increase `max_commit_ratio` above the base behavior by default.
3. `neutral_rusher`, `turtle`, `comet_greedy`, and `overcommitter` should remain disabled until ablation proves positive value.
4. Counter actions should only fire on concrete incoming threats or very high-confidence profile signals.
5. A base action safety filter or budget reservation must happen before or during base planning, not only after base actions are emitted.

## Next Step

Do not proceed to packaging or submit confirmation for adaptive_full.

Proceed to integration rework only if the goal remains to rescue adaptive behavior. Otherwise, keep `base_safe_fallback` as the current candidate and document that no adaptive improvement has been proven.
