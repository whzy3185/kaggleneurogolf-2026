# Targeted Agent Design Context

Date: 2026-06-17

Purpose: establish the baseline and constraints for the next targeted-agent
workstream. This document is a design context only. It does not change runtime
behavior and does not submit to Kaggle.

## Current Official Best

```yaml
agent: vkhydras_last_heuristic single-file candidate
submission_id: 53772702
message: vkhydras_last_single_file_candidate_d7d937e_formatcheck
public_score: 713.0
status: SubmissionStatus.COMPLETE
package: dist/main.py
sha256: 73679EC04C1521E2538FCF61013034B32729ED18CD0A5658C68090B65EC20049
```

Previous completed best:

```yaml
agent: pilkwang_structured single-file fallback
submission_id: 53767789
latest_observed_public_score: 678.9
```

## Current Local Base Candidate

The development baseline is now Vkhydras Last:

```text
agents/public/vkhydras_last_heuristic/main.py
```

The submitted package is:

```text
dist/main.py
```

`dist/main.py` is the cleaned single-file package generated from Vkhydras Last.
It strips the optional `ORBIT_TRACE` file-write branch and passed:

- `python -m py_compile dist\main.py`
- banned-pattern scan for file/network/secret/debug output patterns
- single-file smoke through `scripts/smoke_single_file_agent.py`
- starter file-agent smoke

## Why The Old Adaptive Path Failed

The old adaptive design was:

```text
base agent -> profiler -> counter policy -> supplemental moves
```

It failed the primary local gate:

```text
base vs adaptive_full, 50 seeds bidirectional: base 97, adaptive_full 3
```

The likely failure was not loading or timeout. It was planning interference:

- the base had already spent the important ship budget;
- supplemental moves were not part of the base mission queue;
- profile labels were broad and sometimes late or confounded;
- extra attacks/expansions could destroy the tempo and reserve assumptions of
  the strong base.

## Design Consequence

The new targeted design must not repeat wrapper-level aggression. V1 must be a
conservative safety layer:

```text
Vkhydras Last base actions
+ behavior-only opponent profiling
+ ETA / threat / reserve analysis
+ action filtering, shrinking, or blocking
= profile-aware safety-filtered candidate
```

V1 must not create new attack or expansion actions. It can only remove or reduce
risky base actions. Any later target reweighting must come after this filter-only
candidate proves it does not regress.

## Baseline Files

Current base files:

```text
agents/public/vkhydras_last_heuristic/main.py
dist/main.py
configs/base_agent.yaml
configs/final_agent.yaml
reports/SCORECARD.md
reports/SUBMISSION_RESULT_VKH_LAST.md
```

Future experimental paths:

```text
src/orbitwars_agent/eta_tools.py
src/orbitwars_agent/opponent_profiler_v2.py
src/orbitwars_agent/action_filter_v1.py
agents/variants/vkh_last_targeted_v1/main.py
configs/targeted_agent_policy.yaml
```

Final submission, if ever selected, must again be a single-file `dist/main.py`.

## Non-Goals

- No exact opponent name recognition.
- No hardcoded `if opponent == pilkwang/tamrazov/vkhydras`.
- No new supplemental attack actions in V1.
- No tar adaptive packaging as the primary path.
- No Kaggle submit without explicit user confirmation.

## Next Gate

The next phase is design only:

1. define behavior profiles;
2. define safe responses and forbidden responses;
3. define ETA/threat helper requirements;
4. define action-filter-only integration;
5. define tournament gates that prove the candidate does not hurt Vkhydras Last.
