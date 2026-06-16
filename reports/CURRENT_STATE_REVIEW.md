# Current Adaptive Agent State Review

Date: 2026-06-16

## Repository State

- Repo: `https://github.com/whzy3185/kaggleorbit`
- Local path: `E:\orbitwars_adaptive_agent`
- Current commit reviewed: `4e4f6a3905681954f11cd9b7d5b947a07f27598d`
- Branch state at review start: `main...origin/main`, clean worktree

Recent commits already present:

- full open-source and discussion audit
- public notebook and GitHub repo registries
- loaded public agent pool
- high-rank replay visibility audit
- macro strategy taxonomy
- profiler/counter coverage review
- next optimization candidate list

## Current Official Score

The scorecard has one real Kaggle submission:

| Submission ID | Message | Source | Public score | Status |
|---:|---|---|---:|---|
| `53729904` | `20260616_official_starter_connectivity_baseline` | official starter `main.py` | `317.8` | `SubmissionStatus.COMPLETE` |

No adaptive agent has been submitted. Local match and tournament results are
local-only evidence, not official leaderboard scores.

## Base Agent

Selected base agent: `pilkwang_structured`.

Tracked files:

- `agents/public/pilkwang_structured/main.py`
- `agents/public/pilkwang_structured/SOURCE.md`
- `agents/base_agent.py`
- `configs/base_agent.yaml`

Selection evidence:

- strongest early local smoke round-robin among the first tested candidates
- Apache 2.0 metadata
- physics-aware layered world model and mission scoring
- easier integration risk than larger simulation-heavy variants

Current caveat:

The original base selection used a very small sample. The current task must
prove whether the adaptive wrapper is better than this base, not assume it.

## Adaptive Agent Status

Current adaptive candidate:

```text
Pilkwang base agent
+ action safety validation
+ local WorldModel
+ OpponentProfiler
+ confidence-gated CounterPolicy
+ optional supplemental defense/expansion/counter moves
```

Runtime flow:

1. call the selected base agent first
2. validate base actions
3. build `GameState`
4. update `OpponentProfiler`
5. convert profiles into `StrategyModifiers`
6. only when gated, append supplemental moves
7. merge without exceeding source ship budgets
8. fallback to base agent on exceptions

Current decision:

The adaptive agent is runnable but not proven stronger than the base. It is not
submission-ready. The next work must first fix profiler accounting issues, then
trace profile recognition, then run base-vs-adaptive tournaments.

## Existing Tests

Repository-local tests:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python -m pytest tests -q
```

Result during this review:

```text
14 passed in 0.06s
```

Important test invocation note:

Plain `pytest -q` from the repo root is not currently a valid signal because it
collects ignored third-party test files under `external/` and misses local
`PYTHONPATH`. That broad collection failed with external dependency/import
errors such as missing `fastapi` and duplicate third-party test module names.
Use the scoped command above for this repo's tests.

## Existing Evidence And Reports

Useful current reports:

- `reports/SCORECARD.md`
- `reports/SOURCE_REGISTRY.md`
- `reports/PUBLIC_AGENT_SUMMARY.md`
- `reports/LOCAL_EVAL_SETUP.md`
- `reports/BASE_AGENT_SELECTION.md`
- `reports/WORLD_MODEL_IMPLEMENTATION.md`
- `reports/OPPONENT_PROFILER_DESIGN.md`
- `reports/COUNTER_POLICY_DESIGN.md`
- `reports/ADAPTIVE_AGENT_INTEGRATION.md`
- `reports/OPEN_SOURCE_AND_DISCUSSION_AUDIT_SUMMARY.md`
- `reports/MACRO_STRATEGY_TAXONOMY.md`
- `reports/PROFILER_COVERAGE_REVIEW.md`
- `reports/COUNTER_POLICY_COVERAGE_REVIEW.md`
- `reports/OPTIMIZATION_DIRECTION_REVIEW.md`

Registry note:

`reports/SOURCE_REGISTRY.md` is older than the later full audit and still
contains some early timeout notes. More complete current registries are:

- `configs/kaggle_notebook_registry.yaml`
- `configs/github_repo_registry.yaml`
- `configs/public_agent_pool.yaml`
- `configs/strategy_taxonomy.yaml`

## Missing Reports

Still missing for a submit-quality candidate:

- `reports/PROFILER_FIX_REPORT.md`
- `reports/OPPONENT_PROFILE_EVAL.md`
- `reports/TOURNAMENT_BASE_VS_ADAPTIVE.md`
- `reports/ADAPTIVE_FAILURE_ANALYSIS.md` if adaptive loses
- `reports/ABLATION_RESULTS.md`
- `reports/PARAMETER_SELECTION.md`
- `reports/ADAPTIVE_INTEGRATION_REWORK.md` if wrapper budget is weak
- `reports/FINAL_TOURNAMENT_REPORT.md`
- `reports/PACKAGING_REPORT.md`
- `reports/FINAL_AGENT_CARD.md`
- `reports/SUBMIT_CONFIRM_ADAPTIVE_AGENT.md`
- `reports/HANDOFF.md`
- `reports/NEXT_PROMPT.md`

## Next Blocker

The immediate blocker is profiler reliability:

- `observed_turns` currently increments once per enemy-owned planet per update,
  which can distort confidence, turtle, and send-pressure features.
- `weak_bot` currently exists as an output but is always `0.0`.
- there is no profile snapshot/export method for trace logging.

These issues should be fixed before profile evaluation or adaptive-vs-base
tournaments, otherwise the tournament may measure polluted counter triggers
rather than the intended adaptive design.

## Stage 0 Conclusion

Proceed to Stage 1. Do not submit. Do not package. Do not add new strategic
features until profiler accounting and trace observability are fixed.
