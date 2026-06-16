# Counter Policy Coverage Review

Date: 2026-06-16

Inputs:

- `src/orbitwars_agent/counter_policy.py`
- `src/orbitwars_agent/strategy_modifiers.py`
- `src/orbitwars_agent/adaptive_agent.py`
- `reports/PROFILER_COVERAGE_REVIEW.md`
- `reports/MACRO_STRATEGY_TAXONOMY.md`

## Current Counter Chain

The active path is:

1. `OpponentProfiler.update(state)` computes cumulative profile scores.
2. `build_strategy_modifiers(profiles)` reduces all enemies with `max()` and
   writes global `StrategyModifiers`.
3. `adaptive_agent.agent()` calls the selected base agent first.
4. Supplemental actions are added only when `_should_add_supplement` passes.
5. Supplemental actions use generic reinforcement and generic target scoring.

This means the current policy is wrapper-level adaptation. It does not inject
profile-aware scores into the base agent's internal mission selection.

## Consumed Profile Scores

| Profile score | Counter behavior | Adaptive effect |
|---|---|---|
| `enemy_rusher` | raises reserve/defense, reduces expansion, reduces max commit | used |
| `neutral_rusher` | adds counterattack bonus, slightly reduces expansion, biases target enemy | used |
| `turtle` | lowers attack, raises expansion and comet weight | used |
| `big_stack` | raises defense and counterattack bonus | used |
| `overcommitter` | raises counterattack and max commit | used |
| `comet_greedy` | raises comet target weight | used |
| `reinforce_heavy` | slightly raises attack/counterattack, lowers expansion | used |
| `crash_exploiter` | raises reserve/defense, lowers max commit | used but feature is weak |
| `weakest_targeter` | raises reserve/defense | used |

## Computed Or Defined But Not Effectively Used

| Field | Status | Evidence |
|---|---|---|
| `production_greedy` | unused | computed in profiler, no counter branch, not in `_should_add_supplement` |
| `center_greedy` | unused | computed in profiler, no counter branch, not in `_should_add_supplement` |
| `weak_bot` | dead | profiler always sets 0.0; no counter branch |
| `reinforce_count` | dead | property always returns 0 |
| `scores["confidence"]` | redundant | `effective()` uses `profile.confidence`, not this score entry |
| `risky_expansion_penalty` | dead modifier | counter writes it, adaptive target scoring never reads it |
| `center_weight_mult` | dormant | adaptive can read it, but counter policy never changes it |

## Strategy Family Coverage

| Macro family | Counter quality | Notes |
|---|---:|---|
| `nearest_expander` | weak | Counter uses generic counterattack/expansion shifts, not high-value denial. |
| `production_greedy_expander` | missing | No active branch for Producer-style ROI/high-production targeting. |
| `distance_prioritized_rusher` | weak | Rush branch is not distance-aware or nearest-front aware. |
| `center_control_agent` | missing | No branch sets `center_weight_mult` or contested-center logic. |
| `sun_dodge_physics_agent` | missing | No aiming benchmark/counter behavior. |
| `world_model_forecaster` | missing | No direct response to forecast/search agents beyond generic pressure. |
| `defense_reinforcement_agent` | partial | `reinforce_heavy` increases pressure, but no bait/drain/source-counter logic. |
| `multi_source_gangup_agent` | missing | No convergence detection or anti-gangup reserve plan. |
| `comet_greedy_agent` | partial | Only increases our comet weight after observed comet targets. |
| `big_stack_hammer` | partial | Raises defense/counterattack but no stack-specific evacuation or source disruption. |
| `total_war_endgame_agent` | missing | No phase threshold or mirror all-in response. |
| `crash_exploit_or_collision_agent` | weak | Current feature is conflict targeting, not true crash exploitation. |
| `turtle_defender` | partial | Expands more and attacks less, but no multi-front pressure plan. |
| `RL_policy_agent` | missing | No family-specific counter; should be benchmark-driven. |
| `hybrid_layered_agent` | weak | Broad modifiers cannot target sub-behaviors of layered agents. |

## Current Policy Strengths

- The modifier surface is small and safe enough for quick experiments.
- Threatened-planet reinforcement is always allowed to trigger supplemental
  actions, independent of profile confidence.
- Target enemy bias allows one enemy profile to influence target choice in 4P.
- Max commit and reserve controls are useful levers against rush/overcommit.

## Current Policy Risks

- It is global rather than per-source/per-target. In 4P, one enemy's profile can
  change our behavior toward every opponent.
- It is reactive and often late because `_should_add_supplement` gates on high
  effective scores.
- It works after the base agent has already chosen actions. The merge prevents
  illegal overspending, but it cannot coordinate with the base mission queue.
- `risky_expansion_penalty` looks meaningful in tests/design, but has no runtime
  effect.
- Production/center classifiers are calculated but never change behavior.
- A misdetected `crash_exploiter` can raise reserves against ordinary contested
  planets.

## Required Checks

### Which Counter Policies Have No Practical Use?

- `production_greedy` and `center_greedy` have no counter branches.
- `weak_bot` cannot fire because the profiler never scores it above zero.
- `risky_expansion_penalty` is written by `enemy_rusher` and `overcommitter`
  branches but never consumed in adaptive scoring.
- `center_weight_mult` is readable by `_target_score`, but no current branch
  changes it.

### Are Existing Counters Reasonable?

Conceptually yes, but they are broad. Enemy rush -> reserve/defense, turtle ->
expand, overcommit -> counterattack, and comet -> contest comet are defensible
first responses. The weakness is not the direction; it is the lack of evidence
that the features trigger at the right time and the lack of target-specific
execution.

### Does The Policy Cover Public Strong Agents?

Only partially. It can respond to visible aggression, large sends, and comet
targets. It does not directly counter the public meta's strongest recurring
patterns: production ROI planning, recapture windows, multi-source convergence,
defensive redeployment, and world-model/search horizon effects.

## Recommended Fix Order

1. Add profile trace logging and run it across the loaded public agent pool.
2. Fix `observed_turns` and confidence accounting before changing thresholds.
3. Add active branches for production-greedy and center/high-production control.
4. Add recapture and recently-captured enemy-planet features.
5. Move high-value modifiers into base-agent scoring or a shared scoring layer,
   instead of relying only on wrapper-level supplemental moves.
