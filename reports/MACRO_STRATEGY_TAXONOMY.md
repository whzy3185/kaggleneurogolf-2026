# Orbit Wars Macro Strategy Taxonomy

Date: 2026-06-16

Evidence sources:

- official rules and replay access review
- 234 visible discussion topics / 1,378 messages
- 298 Kaggle Code entries, 27 pulled/static scanned
- 103 GitHub repositories, 16 downloaded/static scanned
- 9 loaded public agents, 8 match-smoked locally
- 5 visible current high-rank replay samples

Full structured labels: `configs/strategy_taxonomy.yaml`.

## Taxonomy

| Family | Definition | Public prevalence |
|---|---|---|
| `nearest_expander` | Starter-like nearest neutral expansion. | Common in tutorials and low-signal notebooks. |
| `production_greedy_expander` | ROI/future-production planner; sends when capture/defense improves production. | Very important after Producer release. |
| `distance_prioritized_rusher` | Prioritizes nearby opponents/frontiers and short-distance pressure. | Visible in ykhnkf lineage. |
| `center_control_agent` | Targets central/high-value orbital positions for geometry control. | Weak direct evidence in sampled replays; design idea only. |
| `sun_dodge_physics_agent` | Safe aiming, sun collision checks, moving target intercepts. | Embedded in most strong public heuristics. |
| `world_model_forecaster` | Future ownership/garrison/arrival timelines and projected action scoring. | Dominant in Pilkwang/Tamrazov/Yuriy/Sigmaborov-style code. |
| `defense_reinforcement_agent` | Threatened planet reinforcement, rescue, and recapture. | Very common in strong public agents. |
| `multi_source_gangup_agent` | Coordinates several sources against one target. | Present in layered public agents and some replay samples. |
| `comet_greedy_agent` | Prioritizes comet planets or comet timing windows. | Uneven; comet logic common, pure comet greed less universal. |
| `big_stack_hammer` | Aggregates large fleets/stacks for hard-to-react attacks. | Explicit in vkhydras archive and discussion comments. |
| `total_war_endgame_agent` | Late all-in / total-war mode near episode end. | Present in code, not visible in short sampled replays. |
| `crash_exploit_or_collision_agent` | Post-crash snipes or collision/path mechanism exploitation. | Present in Pilkwang/Yuriy descriptions; old engine bugs fixed. |
| `turtle_defender` | Conservative reserve-heavy/economic defense/counterattack. | Mentioned in replay clustering; not a dominant named public release. |
| `RL_policy_agent` | PPO/BC/neural/transformer policy. | Active but high-cost; public code often training infra. |
| `hybrid_layered_agent` | Multi-layer blend of physics, world model, defense, attack, comet, endgame. | Largest high-value public family. |

## Labeled Public Agents

| Agent | Primary family | Secondary families | Evidence | Confidence |
|---|---|---|---|---|
| `official_getting_started` | `nearest_expander` | `sun_dodge_physics_agent` | official notebook/rules | high |
| `sigmaborov_starter` | `sun_dodge_physics_agent` | `nearest_expander`, `comet_greedy_agent` | loaded + smoke ok | high |
| `pilkwang_structured` | `hybrid_layered_agent` | world model, defense, multi-source, crash, total war | loaded + smoke ok | high |
| `tamrazov_starwars` | `hybrid_layered_agent` | world model, defense, multi-source, comet | loaded + smoke ok | high |
| `ykhnkf_distance_prioritized` | `distance_prioritized_rusher` | hybrid, world model, defense | loaded + smoke ok | high |
| `sigmaborov_reinforce` | `defense_reinforcement_agent` | world model, hybrid, multi-source | loaded + smoke ok | high |
| `vkhydras_peak_heuristic` | `big_stack_hammer` | hybrid, defense, total war | GitHub archive + smoke ok | high |
| `producer_agent` | `production_greedy_expander` | defense, turtle | discussion + pulled notebook | high |
| `producer_v2` | `production_greedy_expander` | defense | pulled notebook; local missing dependency | medium |
| `kuni05_producer_submission` | `production_greedy_expander` | defense, comet | pulled multi-file notebook | medium |
| `konbu17_rule_ml_validator` | `hybrid_layered_agent` | sun, world model, multi-source | loaded + smoke ok | high |
| `yuriygreben_architect` | `world_model_forecaster` | hybrid, multi-source, crash | loaded + smoke ok | high |
| `aidensong_search_value` | `world_model_forecaster` | hybrid, learned value | pulled notebook | medium |
| `yashm917_sim_value` | `world_model_forecaster` | defense | pulled notebook | medium |
| `debugendless_sun_dodging` | `sun_dodge_physics_agent` | world model, defense | pulled notebook | medium |
| `emanuellcs_beam_search` | `world_model_forecaster` | sun, multi-source | GitHub static scan | medium |
| `alvinng4_precompute` | `sun_dodge_physics_agent` | world model | discussion + GitHub scan | medium |
| `kashiwaba_rl_tutorial` | `RL_policy_agent` | starter baseline | pulled tutorial | medium |
| `souldrive_clone_analysis` | `RL_policy_agent` | world-model/search evidence | discussion + notebook | high |

## Main Public Strategy Clusters

1. Hybrid layered world-model agents are the largest strong public cluster.
   They combine safe physics, future arrival ledgers, ownership timelines,
   reinforcement, recapture, multi-source pressure, comet logic, and endgame
   thresholds.

2. Producer-style ROI planners are a separate cluster.
   They are not just smaller Pilkwang agents. Their core is production ROI,
   capture floors, flow/frontline movement, and avoiding negative-production
   attacks.

3. Distance-prioritized pressure is a recognizable subfamily.
   It can look like a rusher, but often sits on top of a layered baseline.

4. Defense/recapture is no longer optional.
   Discussion, public code, and high-rank replay samples all support threatened
   planet reinforcement and recapture/counter windows as mainstream behavior.

5. RL/BC is active but not the fastest near-term reuse path.
   Public RL artifacts mostly support future training/evaluation. The most
   actionable ML lesson is that cloning actions without search/lookahead can
   lose badly to a planner.

## Replay-Supported Features

The sampled current high-rank replays support these behaviors:

- selective early neutral captures
- early enemy contest around turns 23-32 in top replay `79968955`
- high-commit capture-sized sends
- high-production target preference
- midgame reinforcement-like friendly sends
- target switching
- occasional multi-source pressure
- uneven comet contesting

No final gold strategy is claimed.

## Counter Ideas For Adaptive Agent

| Opponent family | Counter idea |
|---|---|
| `nearest_expander` | Outvalue with production/ETA scoring; punish travel-time blindness. |
| `production_greedy_expander` | Deny production-positive captures, bait ROI thresholds, recapture newly captured planets. |
| `distance_prioritized_rusher` | Reserve against nearest-frontier pressure; counterattack drained closest sources. |
| `sun_dodge_physics_agent` | Improve our aimer; exploit over-conservative path rejection. |
| `world_model_forecaster` | Create reactive reinforcement/recapture states not captured by static forecast. |
| `defense_reinforcement_agent` | Force defense drain with multi-front pressure, then hit support/source planets. |
| `multi_source_gangup_agent` | Detect converging fleets early; reinforce or evacuate target and counter depleted sources. |
| `comet_greedy_agent` | Preposition around spawn windows; avoid overpaying for low-lifetime comet planets. |
| `big_stack_hammer` | Track stack growth, reinforce target floors, disrupt/recapture after hammer launch. |
| `total_war_endgame_agent` | Detect remaining-turn all-in thresholds and mirror/evacuate rather than over-defend. |
| `RL_policy_agent` | Benchmark off-distribution states and exploit missing search/lookahead. |
| `hybrid_layered_agent` | Profile sub-behaviors; broad hybrid label alone is too coarse for counters. |

## Implication

The next adaptive-agent work should not add more broad labels first. It should
generate real profile traces against the loaded public pool and measure when
specific behaviors become detectable: high-commit expansion, defense
reinforcement, recapture windows, comet timing, multi-source convergence, and
big-stack hammer buildup.

