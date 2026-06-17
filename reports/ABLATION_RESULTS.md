# Ablation Results

Date: 2026-06-17

Scope: local evaluation only. No Kaggle submission was run.

## Status

Full adaptive ablation was not expanded to all requested variants because Stage 3 produced a severe direct regression:

```text
base vs adaptive_full, seeds 1-50, bidirectional: base 97, adaptive_full 3, errors 0
```

Running large ablations on variants built from the same post-base supplemental integration would spend time on candidates that already fail the primary gate. This report records the limited ablation evidence and the stop decision.

## Results

| variant | command scope | wins vs base | losses vs base | errors | decision |
| --- | --- | ---: | ---: | ---: | --- |
| base | reference | n/a | n/a | 0 | selected fallback |
| adaptive_full | 50 seeds, bidirectional | 3 | 97 | 0 | rejected |
| adaptive_defense_only | seed 1, bidirectional smoke | 0 | 2 | 0 | not selected |
| adaptive_no_profiler | seed 1, bidirectional smoke | 0 | 2 | 0 | not selected |
| counterattack_only | not run | n/a | n/a | n/a | blocked by full regression |
| comet_only | not run | n/a | n/a | n/a | blocked by full regression and no Stage 2 trigger value |
| anti_rusher_only | not run | n/a | n/a | n/a | blocked until budget-protected integration exists |
| anti_turtle_only | not run | n/a | n/a | n/a | blocked because turtle response is suspected harmful |
| overcommit_only | not run | n/a | n/a | n/a | blocked because overcommit branch can increase commit ratio |

Raw local outputs were written under:

```text
outputs/tournament_raw/base_vs_adaptive_full_50/
outputs/tournament_raw/estimate_base_defense_only/
outputs/tournament_raw/estimate_base_no_profiler/
```

These files are intentionally gitignored.

## Trigger Counts

Profile trigger counts were not recomputed inside the tournament runner. Stage 2 profile traces remain the current evidence:

- strong public agents were often labeled `neutral_rusher`, `overcommitter`, and sometimes `crash_exploiter`;
- `weak_bot`, `comet_greedy`, `weakest_targeter`, and `center_greedy` were not materially useful in the trace set;
- labels that triggered did not translate into positive counter-policy value in Stage 3.

## Negative Cases

Observed negative cases:

- adaptive_full loses heavily to base despite no timeout/errors;
- adaptive_full loses both sides against six stronger public agents in seed-1 screening;
- adaptive_no_profiler also loses to base in the seed-1 smoke, pointing to post-base supplemental action risk independent of profiler labels;
- defense_only is not proven safe.

## Conclusion

No adaptive variant has demonstrated positive value. The ablation result is therefore a stop, not a tuning pass.

Selected current candidate remains:

```text
base_safe_fallback
```

Do not package adaptive_full, adaptive_defense_only, or adaptive_no_profiler as the final submission candidate.
