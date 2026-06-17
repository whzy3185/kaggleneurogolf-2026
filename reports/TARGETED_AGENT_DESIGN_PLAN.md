# Vkhydras Last Targeted Agent Design Plan

Date: 2026-06-17

This is a design and task-chain document only. It does not change runtime
behavior and does not submit to Kaggle.

## Objective

Use the current official-best Vkhydras Last agent as the base, then build a
behavior-aware targeted layer that reacts differently to different enemy
behavior families without destroying the base agent's tempo.

Current official baseline:

```yaml
agent: vkhydras_last_heuristic single-file candidate
submission_id: 53772702
public_score: 713.0
status: COMPLETE
package: dist/main.py
```

The first candidate must be conservative. V1 is not an adaptive attack wrapper.
It is a profile-aware safety filter around Vkhydras Last actions.

## First Principles

1. A strong base is valuable because its tempo, reserves, and mission queue are
   internally coherent.
2. The previous adaptive wrapper failed because it added actions after the base
   had already spent the important ship budget.
3. The safest first step is to preserve the base decision unless a measurable
   opponent behavior makes that specific action risky.
4. A behavior label is useful only if it changes a local decision: source,
   target, ship count, reserve floor, or timing.
5. Local tournament results are not official Kaggle scores.
6. No Kaggle submission should happen until a submit confirmation card is
   generated and the user explicitly confirms submission.

## V1 Architecture

```text
obs
  -> parse state
  -> update behavior-only opponent profiler
  -> call Vkhydras Last base agent
  -> parse proposed base actions
  -> run ETA / threat / reserve checks
  -> delete or shrink risky actions
  -> return legal final action list
```

V1 allowed operations:

- keep base action unchanged;
- reduce ships in a base action;
- delete a base action;
- raise a local reserve floor for a source planet;
- block a source planet for the current step when outgoing movement would make
  it vulnerable.

V1 forbidden operations:

- add a new attack action;
- add a new expansion action;
- retarget a base action to a new planet;
- hardcode opponent names or public-agent ids;
- use local files, network, secrets, or debug prints in the Kaggle candidate.

## Behavior Families And Targeted Responses

### enemy_rusher

Meaning: an opponent directly pressures our planets early or repeatedly, with
short ETA and high own-target ratio.

Signals:

- early enemy fleets targeting our planets;
- short ETA to our frontier or home planets;
- high commit ratio into owned planets;
- repeated attacks before we can build a reserve.

Allowed response:

- raise reserve floor on threatened planets;
- delete or shrink outgoing actions from threatened sources;
- keep high-production threatened planets better defended;
- prefer not to empty planets that are within the enemy response horizon.

Forbidden response:

- blind counterattack;
- new revenge attack;
- global reserve increase across unrelated planets.

### neutral_rusher

Meaning: an opponent captures many neutral planets quickly, often with high
opening send pressure.

Signals:

- high neutral-target ratio;
- many capture-sized fleets into neutral planets;
- low concern for production value or travel cost.

Allowed response:

- avoid sending from planets that would become rushable;
- shrink base expansion actions to low-value contested neutral planets;
- protect our newly captured neutral planets when enemy ETA is short.

Forbidden response:

- unconditional counterattack;
- blocking all expansion just because the enemy expands.

### production_greedy

Meaning: an opponent prioritizes high-production planets and production-positive
captures.

Signals:

- high production target ratio;
- repeated neutral or enemy targets with strong future production;
- defense around high-production holdings.

Allowed response:

- keep extra reserve on our high-production planets;
- shrink outgoing actions from high-production sources under threat;
- block low-margin attacks that expose production centers.

Forbidden response:

- overpaying to deny every high-production target;
- sending new attack actions in V1.

### turtle

Meaning: an opponent sends few fleets, holds high reserves, or reinforces more
than it attacks.

Signals:

- low send rate after corrected observed-turn accounting;
- high garrison retention;
- many own-planet reinforcement sends.

Allowed response:

- mostly keep Vkhydras Last expansion and value actions;
- delete only low-margin attacks into heavily defended targets;
- avoid letting the filter become passive.

Forbidden response:

- forced all-in;
- shrinking normal expansion just because the enemy is quiet.

### big_stack

Meaning: an opponent builds or launches large fleets that can flip a planet or
force a late hammer.

Signals:

- large fleet ratio;
- high max commit ratio;
- converging enemy fleets to the same target;
- depleted source after a large send.

Allowed response:

- block outgoing actions from the likely target;
- raise reserve floor on the likely target;
- delete low-value base actions that prevent survival;
- allow later source-counter logic only after V1 filter proves safe.

Forbidden response:

- split weak counterattacks;
- new attack generated only from the big-stack score.

### overcommitter

Meaning: an opponent empties sources or sends capture amounts with little local
reserve.

Signals:

- high send fraction from a source;
- source garrison drops below nearby threat threshold;
- repeated attacks that leave the sender vulnerable.

Allowed response:

- if Vkhydras Last already attacks that source, avoid filtering it out;
- preserve our ships so the base can exploit on later turns;
- do not delete safe base attacks into recently depleted sources.

Forbidden response:

- add a new attack solely because the overcommit score is high.

### comet_greedy

Meaning: an opponent over-prioritizes comet planets or spends too much around
comet windows.

Signals:

- high comet-target ratio;
- repeated comet contests around known windows;
- fleets sent to low-lifetime or low-value comet targets.

Allowed response:

- blacklist low-quality comet base actions;
- shrink comet sends with poor ETA / value / lifetime;
- keep strong comet actions if the base already selected them and value is
  positive.

Forbidden response:

- global comet boost;
- new comet mission in V1.

### weakest_targeter

Meaning: an opponent attacks weakly defended planets or the weakest player in a
4-player state.

Signals:

- attacks against low-garrison planets;
- target selection follows weakness more than production;
- pressure concentrates on the current weakest neighbor.

Allowed response:

- protect low-garrison planets;
- block outgoing actions from planets that would become the weakest target;
- increase reserve only on exposed frontier planets.

Forbidden response:

- revenge attack;
- treating every enemy as equally dangerous in 4-player games.

## Task Chain

### Phase 0: Freeze Current Baseline

Read:

```text
reports/SCORECARD.md
reports/SUBMISSION_RESULT_VKH_LAST.md
reports/TARGETED_AGENT_DESIGN_CONTEXT.md
configs/base_agent.yaml
configs/final_agent.yaml
agents/public/vkhydras_last_heuristic/main.py
dist/main.py
```

Deliverable:

```text
reports/TARGETED_AGENT_PHASE0_BASELINE.md
```

Required content:

- current commit;
- current official best;
- source and package hash;
- known failed adaptive result;
- explicit statement that no Kaggle submission was made.

Commit:

```bash
git add reports/TARGETED_AGENT_PHASE0_BASELINE.md
git commit -m "audit: freeze targeted agent baseline"
```

### Phase 1: Build ETA And Threat Helpers

Goal: create small reusable helpers for safety decisions. These helpers must be
independent from opponent names.

Candidate files:

```text
src/orbitwars_agent/eta_tools.py
tests/test_eta_tools.py
```

Required helper outputs:

- distance and ETA between planet/fleet positions;
- incoming enemy pressure by target and time horizon;
- enemy response horizon for each owned planet;
- source vulnerability after a proposed send;
- target value summary: owner, ships, production, ETA, comet flag.

Deliverable:

```text
reports/TARGETED_AGENT_ETA_TOOLS.md
```

Tests:

- ETA monotonic with distance;
- incoming pressure groups by target;
- a proposed send can be classified as safe or unsafe;
- comet targets are marked without forcing comet preference.

Commit:

```bash
git add src/orbitwars_agent/eta_tools.py tests/test_eta_tools.py reports/TARGETED_AGENT_ETA_TOOLS.md
git commit -m "feat: add targeted agent eta and threat helpers"
```

### Phase 2: Implement OpponentProfiler V2

Goal: behavior-only profiling with corrected accounting and traceable outputs.

Candidate files:

```text
src/orbitwars_agent/opponent_profiler_v2.py
tests/test_opponent_profiler_v2.py
```

Required properties:

- one observed-turn increment per enemy per step;
- per-enemy profile scores;
- per-profile confidence where possible;
- no opponent id/name hardcoding;
- `to_dict(step)` export for trace logging.

Profiles:

```text
enemy_rusher
neutral_rusher
production_greedy
turtle
big_stack
overcommitter
comet_greedy
weakest_targeter
```

Deliverable:

```text
reports/TARGETED_AGENT_PROFILER_V2.md
```

Tests:

- observed turns are not multiplied by enemy planet count;
- early attack raises `enemy_rusher`;
- high neutral capture raises `neutral_rusher`;
- high-production targeting raises `production_greedy`;
- low send rate does not become turtle in the first few turns;
- `to_dict` contains stable keys.

Commit:

```bash
git add src/orbitwars_agent/opponent_profiler_v2.py tests/test_opponent_profiler_v2.py reports/TARGETED_AGENT_PROFILER_V2.md
git commit -m "feat: add behavior-only opponent profiler v2"
```

### Phase 3: Add Profile Trace Evaluation

Goal: see what the profiler detects against real public agents before using it
to change actions.

Reuse or extend:

```text
scripts/run_profile_trace.py
```

Output path:

```text
outputs/profile_traces/
```

`outputs/` must remain untracked.

Required opponents:

```text
starter
pilkwang_structured
tamrazov_starwars
sigmaborov_reinforce
ykhnkf_distance_prioritized
vkhydras_peak_heuristic
vkhydras_last_heuristic mirror
```

Minimum run:

```text
3 seeds per matchup, bidirectional if supported
turn snapshots: 20, 50, 100, 200, final
```

Deliverable:

```text
reports/TARGETED_AGENT_PROFILE_TRACE_V2.md
```

Required conclusions:

- which profiles trigger for each public agent;
- average first-trigger turn;
- confidence at trigger;
- false-positive risks;
- labels that do not trigger.

Commit:

```bash
git add scripts/run_profile_trace.py reports/TARGETED_AGENT_PROFILE_TRACE_V2.md
git commit -m "eval: trace targeted opponent profiles"
```

### Phase 4: Implement Action Filter V1

Goal: safely filter Vkhydras Last proposed actions. Do not add new actions.

Candidate files:

```text
src/orbitwars_agent/action_filter_v1.py
tests/test_action_filter_v1.py
```

Inputs:

- parsed state;
- base actions from Vkhydras Last;
- `OpponentProfilerV2` output;
- ETA/threat helper output;
- `configs/targeted_agent_policy.yaml`.

Outputs:

- legal final action list;
- filter audit record for local trace only.

Allowed edits:

- delete action;
- reduce send amount;
- block source for current turn;
- keep action unchanged.

Deliverable:

```text
reports/TARGETED_AGENT_ACTION_FILTER_V1.md
```

Tests:

- never creates a new target;
- never increases ships;
- preserves legal action format;
- blocks threatened-source send against `enemy_rusher`;
- shrinks high-production-source send under threat;
- does not block normal safe expansion;
- no file/network/secrets access.

Commit:

```bash
git add src/orbitwars_agent/action_filter_v1.py tests/test_action_filter_v1.py reports/TARGETED_AGENT_ACTION_FILTER_V1.md
git commit -m "feat: add conservative targeted action filter"
```

### Phase 5: Integrate Candidate Agent

Goal: wrap Vkhydras Last with the filter while preserving fallback behavior.

Candidate path:

```text
agents/variants/vkh_last_targeted_v1/main.py
```

Runtime contract:

- exposes `agent(obs)`;
- calls Vkhydras Last base first;
- catches filter errors and returns base actions;
- no debug prints;
- no external file dependencies in the eventual packaged candidate.

Deliverable:

```text
reports/TARGETED_AGENT_INTEGRATION_V1.md
```

Smoke tests:

```bash
python -m py_compile agents/variants/vkh_last_targeted_v1/main.py
python scripts/smoke_single_file_agent.py agents/variants/vkh_last_targeted_v1/main.py
```

Commit:

```bash
git add agents/variants/vkh_last_targeted_v1/main.py reports/TARGETED_AGENT_INTEGRATION_V1.md
git commit -m "feat: integrate vkhydras targeted filter candidate"
```

### Phase 6: Base Non-Regression Tournament

Goal: prove the filter does not obviously hurt the official-best base.

Required matchup:

```text
vkhydras_last_heuristic base vs vkh_last_targeted_v1
50 seeds
bidirectional
```

Primary gate:

```yaml
min_targeted_winrate_vs_base: 0.45
max_errors: 0
max_timeouts: 0
```

Stronger go-forward preference:

```yaml
preferred_targeted_winrate_vs_base: 0.50
or:
  four_player_avg_rank_improves: true
```

Deliverable:

```text
reports/TARGETED_AGENT_BASE_NONREGRESSION.md
```

If targeted loses badly, stop and reduce to reserve-only or abandon V1.

Commit:

```bash
git add reports/TARGETED_AGENT_BASE_NONREGRESSION.md
git commit -m "eval: test targeted candidate against vkhydras base"
```

### Phase 7: Public Pool Evaluation

Goal: measure targeted behavior across strategy families, not only mirror
matches.

P0 opponents:

```text
pilkwang_structured
tamrazov_starwars
sigmaborov_reinforce
ykhnkf_distance_prioritized
vkhydras_peak_heuristic
official/starter or sigmaborov_starter
```

Minimum:

```text
20 seeds per opponent, bidirectional if supported
```

Metrics:

- wins and losses;
- winrate;
- average rank;
- average final ships;
- errors;
- timeouts;
- filtered action count;
- deleted action count;
- shrunk action count;
- per-profile trigger count;
- negative cases where filtering caused a visible loss.

Deliverable:

```text
reports/TARGETED_AGENT_PUBLIC_POOL_EVAL.md
```

Commit:

```bash
git add reports/TARGETED_AGENT_PUBLIC_POOL_EVAL.md
git commit -m "eval: benchmark targeted candidate against public pool"
```

### Phase 8: 4-Player Evaluation

Goal: verify the filter does not collapse in multi-opponent games.

Minimum pools:

```text
targeted + pilkwang + tamrazov + sigmaborov
targeted + ykhnkf + vkhydras_peak + starter
base + the same opponent pools for comparison
```

Minimum:

```text
20 seeds per pool, rotate positions if runner supports it
```

Metrics:

- average rank;
- rank distribution;
- position sensitivity;
- errors;
- timeouts;
- profile trigger distribution per enemy;
- cases where one enemy incorrectly changes actions toward all enemies.

Deliverable:

```text
reports/TARGETED_AGENT_4P_EVAL.md
```

Commit:

```bash
git add reports/TARGETED_AGENT_4P_EVAL.md
git commit -m "eval: test targeted candidate in four-player pools"
```

### Phase 9: Ablation

Goal: identify which targeted responses are useful and which are harmful.

Variants:

```text
base
targeted_reserve_only
targeted_enemy_rusher_only
targeted_big_stack_only
targeted_production_guard_only
targeted_comet_filter_only
targeted_all_filters
```

Required outputs:

- per-variant winrate;
- per-opponent delta;
- filter counts;
- profile trigger counts;
- negative cases;
- recommended final enabled filters.

Deliverables:

```text
reports/TARGETED_AGENT_ABLATION.md
configs/targeted_agent_policy.yaml
```

Commit:

```bash
git add reports/TARGETED_AGENT_ABLATION.md configs/targeted_agent_policy.yaml
git commit -m "eval: ablate targeted action filters"
```

### Phase 10: Go / No-Go Decision

Goal: decide whether to package or reject the targeted candidate.

Package only if all are true:

```yaml
errors: 0
timeouts: 0
base_nonregression_passed: true
public_pool_not_worse_than_base: true
four_player_not_worse_than_base: true
filter_benefit_explained_by_traces: true
```

Preferred promotion criteria:

```yaml
targeted_winrate_vs_base: ">= 0.50"
or:
  public_pool_delta_positive: true
or:
  four_player_avg_rank_improves: true
```

If failed:

- keep official best as Vkhydras Last 713.0;
- write failure analysis;
- do not package;
- do not submit.

Deliverable:

```text
reports/TARGETED_AGENT_GO_NO_GO.md
```

Commit:

```bash
git add reports/TARGETED_AGENT_GO_NO_GO.md
git commit -m "analysis: decide targeted candidate go no-go"
```

### Phase 11: Single-File Packaging

Only run this phase after the go decision passes.

Goal: generate `dist/main.py` for the selected targeted candidate.

Command pattern:

```bash
python scripts/package_single_file_agent.py \
  --source agents/variants/vkh_last_targeted_v1/main.py \
  --output dist/main.py
python -m py_compile dist/main.py
python scripts/smoke_single_file_agent.py dist/main.py
```

Deliverables:

```text
reports/TARGETED_AGENT_PACKAGING_REPORT.md
reports/TARGETED_AGENT_FINAL_CARD.md
```

Commit:

```bash
git add dist/main.py reports/TARGETED_AGENT_PACKAGING_REPORT.md reports/TARGETED_AGENT_FINAL_CARD.md
git commit -m "package: prepare targeted vkhydras candidate"
```

### Phase 12: Submit Confirmation Card

Goal: prepare but do not submit.

Deliverable:

```text
reports/SUBMIT_CONFIRM_TARGETED_AGENT.md
```

Required content:

```yaml
competition_slug: orbit-wars
current_official_best:
  agent: vkhydras_last_heuristic
  score: 713.0
candidate:
  id: vkh_last_targeted_v1
  package: dist/main.py
  sha256:
local_evidence:
  base_nonregression:
  public_pool:
  four_player:
  ablation:
known_risks:
exact_submit_command:
manual_confirmation_required: true
submitted: false
```

Commit:

```bash
git add reports/SUBMIT_CONFIRM_TARGETED_AGENT.md
git commit -m "report: create targeted agent submit confirmation"
```

### Phase 13: Stop For User Confirmation

No submission is allowed unless the user explicitly confirms.

Accepted user confirmation examples:

```text
submit targeted
confirm submit vkh_last_targeted_v1
```

Then and only then execute one Kaggle submit, query status, update scorecard,
and commit the submission result.

## Failure Paths

### If filter-only loses badly to base

Action:

- disable all non-defense filters;
- keep only threatened-source reserve blocking;
- rerun base non-regression.

If still weak:

- abandon targeted V1;
- keep official best as Vkhydras Last 713.0.

### If public pool improves but 4-player collapses

Action:

- add per-enemy locality gates;
- avoid global profile reductions;
- require source-target-specific threat evidence.

### If traces are noisy or profiles do not trigger

Action:

- do not tune thresholds blindly;
- improve profile features first;
- keep Vkhydras Last unchanged.

### If packaging fails

Action:

- fix single-file import and banned-pattern issues;
- run smoke again;
- do not submit until a new confirmation card is generated.

## Next Code Task

The next implementation task should be Phase 1 plus Phase 2 only:

```text
ETA/threat helpers
OpponentProfilerV2
profile export
unit tests
no runtime behavior change
```

This keeps the first code step measurable and avoids repeating the previous
wrapper-level adaptive failure.
