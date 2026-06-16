# Opponent Profiler Coverage Review

Date: 2026-06-16

Inputs:

- `reports/MACRO_STRATEGY_TAXONOMY.md`
- `configs/strategy_taxonomy.yaml`
- `src/orbitwars_agent/opponent_profiler.py`
- `src/orbitwars_agent/counter_policy.py`
- `src/orbitwars_agent/adaptive_agent.py`
- visible current high-rank replay sample summary in `reports/GOLD_REPLAY_STRATEGY_ANALYSIS.md`

## Implementation Snapshot

The current profiler is a lightweight action-observation classifier. It only
records newly observed enemy fleets, estimates their target with
`likely_fleet_target`, then computes cumulative ratios.

Important mechanics:

- `observed_turns` is incremented once per enemy-owned planet per update, not
  once per enemy per game turn (`opponent_profiler.py:105-108`).
- `confidence` is `0.75 * min(new_fleets / 8, 1) + 0.25 * min(observed_turns / 60, 1)`
  (`opponent_profiler.py:32-36`).
- `reinforce_count` is a placeholder and always returns `0`
  (`opponent_profiler.py:46-48`).
- `weak_bot` is a placeholder and is always scored as `0.0`
  (`opponent_profiler.py:220`).
- `production_greedy` and `center_greedy` are computed but are not consumed by
  the current counter/adaptive trigger path.

## Coverage Against Macro Strategy Families

| Strategy family | Current coverage | Notes |
|---|---:|---|
| `nearest_expander` | weak | Can appear as `neutral_rusher`, but no nearest/ETA test exists. |
| `production_greedy_expander` | partial but unused | `production_greedy` tracks high-production target ratio, but counter policy does not consume it. |
| `distance_prioritized_rusher` | weak | Early pressure may raise `enemy_rusher`/`neutral_rusher`; no distance-to-frontier or nearest-opponent feature. |
| `center_control_agent` | partial but unused | `center_greedy` is computed, but no counter consumes it. |
| `sun_dodge_physics_agent` | not covered | The profiler does not measure aiming safety, rejected shots, or sun avoidance behavior. |
| `world_model_forecaster` | not directly covered | Forecasting is inferred only indirectly through targets; no future-arrival or garrison-prediction signal. |
| `defense_reinforcement_agent` | partial | Own-planet targeting increments `self_target_count` and `reinforce_heavy`, but there is no threatened-planet context or true reinforcement count. |
| `multi_source_gangup_agent` | not covered | No same-target multi-source window, synchronized ETA, or convergence count. |
| `comet_greedy_agent` | partial | Only current comet target ratio is counted; no spawn-window or preposition behavior. |
| `big_stack_hammer` | partial | Large fleet count and max commit ratio can detect big sends, but not stack buildup or convergence. |
| `total_war_endgame_agent` | not covered | No remaining-turn phase features. |
| `crash_exploit_or_collision_agent` | weak/misleading | `crash_exploiter` means targeting an existing conflict, not observing an actual crash exploit. |
| `turtle_defender` | weak | Based on low sending rate, but `observed_turns` is planet-count weighted. |
| `RL_policy_agent` | not covered | No behavior-specific RL signature is defined. |
| `hybrid_layered_agent` | facet-only | Some sub-behaviors are covered, but there is no hybrid decomposition or dominant-mode trace. |

## Required Checks

### weak_bot

Status: not implemented.

Evidence: `weak_bot` property exists, but `_refresh_scores` sets
`"weak_bot": 0.0` unconditionally. No counter-policy branch consumes
`weak_bot`.

Impact: starter-like or clearly weak bots cannot be identified as a separate
family. They can only be mis-bucketed into `neutral_rusher`, `turtle`, or no
profile at all.

### crash_exploiter

Status: behavior evidence is insufficient.

The profiler increments `conflict_target_count` when a new enemy fleet targets a
planet already targeted by another non-same-owner fleet. That is useful as a
"third-party conflict targeter" feature, but it is not evidence of post-crash
sniping or collision exploitation.

Public code contains real crash-exploit mission logic in Pilkwang/Yuriy/Tamrazov
lineage, but this profiler cannot distinguish:

- opportunistic pile-on to a contested planet
- weak-enemy targeting
- actual arrival-after-crash exploitation
- old engine collision quirks

Recommendation: rename the observed feature to `conflict_targeter` unless true
arrival/crash timing is added.

### comet_greedy Around 50/150/250/350/450

Status: not stable.

Current score is only `comet_target_count / new_fleets_count`. It has no comet
spawn-window phase feature, no preposition detection before spawn, no comet
lifetime weighting, and no per-window reset. A single early comet target is
diluted by later normal actions, while a late short burst may not reach the
effective threshold before the window closes.

Recommendation: track windowed comet metrics for each expected comet phase and
separate `comet_targeter` from `comet_prepositioner`.

### neutral_rusher Versus production_greedy

Status: confounded.

`neutral_rusher` uses neutral target ratio, send pressure, and max commit ratio.
`production_greedy` uses high-production target ratio plus neutral ratio. High
production neutral openings can light up both features, but the profiler does
not check ROI, ETA discount, production horizon, or target production relative
to alternative neutrals.

Impact: Producer-style agents may be mislabeled as rushers, and nearest/starter
expanders may be mislabeled as production-greedy when early neutrals happen to
have production >= 4.

### enemy_rusher False Positives

Status: likely.

`enemy_rusher` uses first attack before turn 80, own-target ratio, and max
commit ratio. This can catch real direct aggression, but it can also label normal
early border contests against our newly captured planets as "rush" in both 2P
and 4P settings. It also ignores whether the attack was profitable, close-range,
multi-source, or a recapture attempt.

Recommendation: split `enemy_rusher` into `direct_home_rusher`,
`frontier_contester`, and `recapture_attacker`.

### turtle And observed_turns

Status: distorted by accounting.

`observed_turns` is incremented per enemy-owned planet per step. An enemy with
more planets gains observed time faster, so `low_send` can rise or fall for
economic expansion reasons rather than actual passivity. This affects `turtle`
and `reinforce_heavy`.

Recommendation: store `last_seen_step` / `first_seen_step` and count one
observation per enemy per game step. Keep planet-count exposure as a separate
feature if useful.

### confidence Timing

Status: coarse and probably late for low-action strong agents.

Adaptive supplements require both profile confidence >= 0.55 and an effective
score >= 0.55. Since `effective(score) = score * confidence`, a raw score of
0.70 requires confidence about 0.79 to pass. This means many profile-specific
counters will not fire until roughly 7-8 observed fleets or inflated
`observed_turns`. Conversely, multi-planet enemies can gain confidence faster
than intended because `observed_turns` is planet-count weighted.

Recommendation: log real match traces before changing thresholds, then use
behavior-specific confidence instead of one global confidence.

## Coverage Gaps With Highest Impact

1. No trace logging of profile scores by turn, so current thresholds cannot be
   validated against public agents or high-rank replays.
2. No explicit recapture/recently-captured-planet detection, despite discussion
   evidence that one-turn-after-capture recapture matters.
3. No real production ROI classifier for Producer-style agents.
4. No multi-source convergence classifier.
5. No phase/window model for comet timing.
6. No 4-player threat-priority model; all enemy profiles are reduced with max().
7. No direct weak/starter-like bot classifier.
8. No endgame all-in classifier.

## Conclusion

The current profiler is a useful first-pass feature counter, but it does not yet
cover the dominant public strategy taxonomy deeply enough to drive targeted
adaptation. It can weakly identify early aggression, neutral expansion, large
sends, comet targeting, self-targeting, and contested targeting. It cannot yet
separate Producer-style ROI, recapture timing, world-model planning,
multi-source attacks, true crash exploitation, or 4-player diplomatic threat
priority.
