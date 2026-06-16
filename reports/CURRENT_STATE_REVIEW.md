# Current State Review

Date: 2026-06-16

## Repository State

- Repo: `https://github.com/whzy3185/kaggleorbit`
- Local path: `E:\orbitwars_adaptive_agent`
- Latest commit reviewed: `bda19b6ce27a829cc3140604e666540089a971fc`
- Branch state at review start: `main...origin/main`, clean worktree

Recent work already present:

- official starter connectivity submission
- public source registry
- local Orbit Wars evaluation harness
- selected Pilkwang base wrapper
- world model, opponent profiler, counter policy, adaptive wrapper
- bidirectional local gauntlet support
- targeted profiler traits for reinforcement/crash/weakest-target behavior

## Official Scorecard

Current official scorecard has one real Kaggle submission:

| Submission ID | Message | Source | Public score | Status |
|---:|---|---|---:|---|
| `53729904` | `20260616_official_starter_connectivity_baseline` | official starter `main.py` | `317.8` | `SubmissionStatus.COMPLETE` |

No adaptive candidate has been submitted. Local tournament results are not
official leaderboard scores.

## Base Agent

Selected base agent: `pilkwang_structured`.

Tracked files:

- `agents/public/pilkwang_structured/main.py`
- `agents/public/pilkwang_structured/SOURCE.md`
- `agents/base_agent.py`
- `configs/base_agent.yaml`

Selection rationale in the current repo:

- strongest first local smoke round-robin among tested candidates
- Apache 2.0 metadata via `orbit-wars-lab`
- layered world model and physics-aware scoring structure
- easier to wrap and patch than larger simulation-heavy agents

Known caveats:

- the original base-selection tournament used only two seeds
- local engine results are not official scores
- later bidirectional checks showed player-order sensitivity exists in this
  competition, so all future comparisons should use bidirectional matches

## Adaptive Agent State

Current adaptive candidate:

```text
Pilkwang base agent
+ action validation
+ local WorldModel
+ OpponentProfiler
+ confidence-gated CounterPolicy
+ optional supplemental moves
```

Current behavior:

- calls base agent first
- validates returned actions for legal source, finite angle, and ship budget
- updates profiler and builds strategy modifiers
- returns base actions unless high-confidence profiler signals or urgent
  defense pressure justify supplemental actions
- falls back to the selected base on exceptions

Current decision:

The adaptive agent is runnable, but not submission-ready. Existing reports show
it beats starter/nearest/ykhnkf in a short local bidirectional gauntlet, but
loses to `tamrazov_starwars` and `sigmaborov_reinforce`. No new submission
should be made before a broader public-agent and discussion audit.

## Source Registry Completeness

The existing source registry is useful but incomplete for a full intelligence
audit.

Already registered:

- official starter
- `automatylicza/orbit-wars-lab`
- Pilkwang structured baseline
- Tamrazov Starwars
- ykhnkf distance-prioritized
- Sigmaborov reinforce/starter
- Yuriy Greben architect
- Kashiwaba RL tutorial
- vkhydras heuristic bots
- Pascal orbitwork
- projectedanx framework
- partial/timeout records for ayushmk7, abdulbasith5, michaelriedl

Still incomplete:

- Kaggle Discussion has not been systematically reviewed
- Kaggle Code/notebook registry is not complete and vote/update/license fields
  are missing for many entries
- GitHub search needs a fresh pass for all known repos and adjacent forks
- leaderboard/final medal/replay visibility has not been audited
- public agent pool is not yet normalized into `agents/public/<source_id>/`
  for every P0/P1 source
- notebook title LB claims are recorded as claims but not independently verified

## Missing Evidence

High-priority missing evidence:

1. Official rules and replay access details refreshed from Kaggle pages.
2. Full discussion registry, especially rule updates, strategy posts, replay
   visibility, and high-rank team comments.
3. Complete Kaggle notebook registry with download/repro status.
4. GitHub repo registry with license, files, and reuse risk.
5. Leaderboard/top-team visibility audit.
6. Explicit proof whether gold/high-rank replays are accessible in this session.
7. Macro strategy taxonomy across public agents.
8. Profiler/counter coverage review against that taxonomy.
9. Next optimization candidates grounded in public evidence rather than local
   smoke results alone.

## Immediate Audit Direction

Do not submit. Do not continue blind strategy edits. The next stages should
refresh official rules, collect public notebooks/repos/discussions, and only
then decide whether the profiler/counter design is aligned with the real public
strategy landscape.
