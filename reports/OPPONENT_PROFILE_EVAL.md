# Opponent Profile Trace Evaluation

Date: 2026-06-16

Commit base: `48f4efe`

## Scope

This stage added `scripts/run_profile_trace.py` and used it to answer what the
current profiler sees during real local matches.

No Kaggle submission was made. Raw trace files were written under ignored
`outputs/profile_traces/` and are not committed.

## Trace Command Shape

Example:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python scripts\run_profile_trace.py `
  --agent-a local/agents/adaptive_agent `
  --agent-b local/agents/public/tamrazov_starwars `
  --seed 1 `
  --max-steps 220 `
  --output outputs\profile_traces\adaptive_vs_tamrazov_starwars_seed1.jsonl
```

Each JSONL row records:

- `step`
- `player`
- `agent_id`
- `enemy_id`
- `enemy_agent_id`
- `scores`
- `confidence`
- `observed_new_fleets`
- raw count fields

## Runs

All required trace matches completed with match status `ok`.

| Opponent | Seeds | Result note |
|---|---:|---|
| `baselines/starter` | 1,2,3 | adaptive won all three trace matches |
| `pilkwang_structured` | 1,2,3 | public agent won all three trace matches |
| `tamrazov_starwars` | 1,2,3 | public agent won all three trace matches |
| `sigmaborov_reinforce` | 1,2,3 | public agent won all three trace matches |
| `ykhnkf_distance_prioritized` | 1,2,3 | public agent won all three trace matches |
| `vkhydras_peak_heuristic` | 1,2,3 | public agent won all three trace matches |

Environment note:

`kaggle_environments` prints OpenSpiel/litellm load warnings in this
environment, including unavailable pokerkit games and `werewolf` missing
`litellm`. These messages did not stop Orbit Wars matches; trace scripts exited
successfully and match status was `ok`.

## Recognition Summary

The table below summarizes adaptive player 0 profiling opponent player 1.

| Opponent | Avg confidence | Final confidence | Main high labels | Effective trigger labels |
|---|---:|---:|---|---|
| `starter` | 0.682 | 1.000 | `turtle`, `neutral_rusher`, `crash_exploiter`, `production_greedy` | `neutral_rusher`, `turtle`, `production_greedy`, `crash_exploiter` |
| `pilkwang_structured` | 0.881 | 1.000 | `overcommitter`, `neutral_rusher`, `crash_exploiter`, `enemy_rusher`, `big_stack` | `neutral_rusher`, `overcommitter`, `crash_exploiter` |
| `tamrazov_starwars` | 0.894 | 1.000 | `overcommitter`, `neutral_rusher`, `crash_exploiter`, `production_greedy`, `enemy_rusher` | `neutral_rusher`, `enemy_rusher`, `production_greedy`, `big_stack`, `overcommitter`, `crash_exploiter` |
| `sigmaborov_reinforce` | 0.893 | 1.000 | `overcommitter`, `neutral_rusher`, `crash_exploiter`, `production_greedy`, `enemy_rusher` | `neutral_rusher`, `production_greedy`, `big_stack`, `overcommitter`, `crash_exploiter` |
| `ykhnkf_distance_prioritized` | 0.906 | 1.000 | `overcommitter`, `neutral_rusher`, `enemy_rusher`, `big_stack`, `crash_exploiter` | `neutral_rusher`, `enemy_rusher`, `production_greedy`, `overcommitter`, `crash_exploiter` |
| `vkhydras_peak_heuristic` | 0.857 | 1.000 | `overcommitter`, `neutral_rusher`, `big_stack`, `crash_exploiter`, `enemy_rusher` | `neutral_rusher`, `enemy_rusher`, `big_stack`, `overcommitter`, `crash_exploiter` |

Interpretation:

- strong public agents are mostly recognized as high-commit/high-pressure
  neutral expanders with conflict targeting and occasional early attacks
- `overcommitter` is the most common high signal across strong agents
- `neutral_rusher` is also common across nearly every public opponent
- `big_stack` is most meaningful for `vkhydras_peak_heuristic`
- `production_greedy` appears in traces, but current counter policy does not
  consume it

## Turn Snapshot Summary

Average top labels at selected turns:

| Opponent | Turn 20 | Turn 50 | Turn 100 | Turn 200/latest |
|---|---|---|---|---|
| `starter` | conf 0.275; `neutral_rusher` 0.674, `turtle` 0.638, `production_greedy` 0.467 | conf 0.713; `neutral_rusher` 0.670, `turtle` 0.523 | conf 1.000; `crash_exploiter` 0.688 | conf 1.000; `crash_exploiter` 0.734 |
| `pilkwang_structured` | conf 0.494; `overcommitter` 1.000, `neutral_rusher` 0.792 | conf 0.963; `overcommitter` 0.829, `neutral_rusher` 0.650 | conf 1.000; `overcommitter` 0.650, `crash_exploiter` 0.595 | conf 1.000; `overcommitter` 0.692 |
| `tamrazov_starwars` | conf 0.525; `overcommitter` 0.985, `neutral_rusher` 0.786, `production_greedy` 0.652 | conf 0.963; `overcommitter` 0.892, `neutral_rusher` 0.768, `crash_exploiter` 0.664 | conf 1.000; `overcommitter` 0.747, `neutral_rusher` 0.671 | conf 1.000; `crash_exploiter` 0.554 |
| `sigmaborov_reinforce` | conf 0.588; `overcommitter` 1.000, `neutral_rusher` 0.797, `production_greedy` 0.606 | conf 0.963; `overcommitter` 0.826, `neutral_rusher` 0.713 | conf 1.000; `overcommitter` 0.659, `neutral_rusher` 0.599 | conf 1.000; `overcommitter` 0.792 |
| `ykhnkf_distance_prioritized` | conf 0.744; `overcommitter` 0.938, `neutral_rusher` 0.673 | conf 0.963; `overcommitter` 0.881, `neutral_rusher` 0.726 | conf 1.000; `overcommitter` 0.633, `neutral_rusher` 0.566 | conf 1.000; `overcommitter` 0.708 |
| `vkhydras_peak_heuristic` | conf 0.588; `overcommitter` 1.000, `neutral_rusher` 0.704 | conf 0.963; `overcommitter` 0.943, `neutral_rusher` 0.596, `big_stack` 0.523 | conf 1.000; `overcommitter` 0.876, `big_stack` 0.652 | conf 1.000; `overcommitter` 0.858, `big_stack` 0.674 |

## Obvious Misjudgments

1. `turtle` raw score is high at step 0 for every opponent because no fleets
   have been observed yet. The current confidence/effective gate usually
   prevents early runtime impact, but raw profile summaries can be misleading.

2. `overcommitter` is high for nearly all strong public agents. This is partly
   real high-commit play, but the label is too broad to distinguish strong
   public openings from reckless overcommit.

3. `crash_exploiter` triggers for starter by late turns. This confirms the
   earlier coverage review: the current feature is really conflict-targeting,
   not proof of true crash exploitation.

4. `production_greedy` appears against strong agents but has no active counter
   branch. This makes the trace informative but not currently actionable.

## Labels That Almost Never Trigger

Using current runtime-style effective gates:

- `comet_greedy` did not materially trigger in these 18 traces.
- `weakest_targeter` did not materially trigger.
- `weak_bot` did not materially trigger for the traced public agents.
- `center_greedy` did not become a runtime policy trigger.

This is not necessarily bad. The traced opponents are mostly strong public
agents, not intentionally weak bots.

## Labels That Trigger Too Early

Raw scores:

- `turtle` is raw-high immediately at step 0.
- `production_greedy` can be raw-high from the first few neutral captures.
- `overcommitter` often becomes raw-high by turns 2-5 for strong agents.

Effective runtime gates:

- `overcommitter` can still trigger early against `ykhnkf` around turn 13 and
  against `tamrazov`/`sigmaborov` in the low 20s.
- This may encourage counterattack bonus before the adaptive wrapper has enough
  context to know whether the opponent is actually vulnerable.

## Labels That Trigger Too Late

- Against `starter`, effective `neutral_rusher`/`turtle`/`production_greedy`
  triggers appear around turns 64-76. This is late for a weak opponent and means
  weak/starter-specific exploitation is not yet useful.
- `enemy_rusher` often triggers after the main opening has already happened.
- `comet_greedy` has no useful windowed trigger in this trace set.

## Counter Policy Impact

Current counter policy consumes:

- `enemy_rusher`
- `neutral_rusher`
- `turtle`
- `big_stack`
- `overcommitter`
- `comet_greedy`
- `reinforce_heavy`
- `crash_exploiter`
- `weakest_targeter`

Most practical runtime modifications in these traces therefore come from:

- `neutral_rusher`
- `overcommitter`
- `crash_exploiter`
- `big_stack` against vkhydras-like agents
- `enemy_rusher` in some pressure matches

Risk:

- `neutral_rusher + overcommitter` may fire against nearly every strong public
  agent. If the later tournament shows adaptive underperforms base, these two
  branches are first suspects.
- `production_greedy` has evidence in traces but does not affect current policy.
- `weak_bot` is now implemented but not yet useful enough to enable aggressive
  anti-weak behavior.

## Validation

Repository-local tests after adding the trace script:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python -m pytest tests -q
```

Result:

```text
19 passed in 0.05s
```

## Stage 2 Conclusion

Profile tracing is now available and shows the profiler can explain broad
opponent pressure patterns, but labels remain too coarse for confident strategy
tuning. Proceed to base-vs-adaptive tournament before adding or strengthening
counter policies.
