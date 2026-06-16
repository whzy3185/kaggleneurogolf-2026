# Orbit Wars Open Source And Discussion Audit Summary

Date: 2026-06-16

Draft base commit: `f9fbb8d84ebcbbc030819db1a71ddd2f81b16f38`

This summary is the readable conclusion of the full audit. The commit that adds
this file is reported by `git log` after commit.

## 1. Competition Content Read

The audit re-read and recorded:

- Kaggle Orbit Wars official pages: overview, evaluation, rules, data,
  submission format, agents guide, leaderboard behavior, and replay access.
- Kaggle CLI visible files and pages.
- 234 visible Kaggle discussion topics / 1,378 messages.
- 298 Kaggle Code entries; 27 notebooks/static code packages were pulled and
  scanned.
- 103 GitHub repositories; 16 high-value repos were downloaded/static scanned.
- Public daily episode datasets and 5 current high-rank replay samples.
- Current local repo reports/configs/source registry/base/adaptive/profiler code.

Primary local audit reports:

- `reports/OFFICIAL_RULES_REVIEW.md`
- `reports/REPLAY_ACCESS_AUDIT.md`
- `reports/DISCUSSION_REVIEW.md`
- `reports/KAGGLE_NOTEBOOK_REVIEW.md`
- `reports/GITHUB_REPO_REVIEW.md`
- `reports/PUBLIC_AGENT_LOADING.md`
- `reports/LEADERBOARD_GOLD_REPLAY_AUDIT.md`
- `reports/GOLD_REPLAY_STRATEGY_ANALYSIS.md`
- `reports/MACRO_STRATEGY_TAXONOMY.md`
- `reports/PROFILER_COVERAGE_REVIEW.md`
- `reports/COUNTER_POLICY_COVERAGE_REVIEW.md`
- `reports/OPTIMIZATION_DIRECTION_REVIEW.md`

## 2. Key Discussion Conclusions

- Official/staff discussion indicates replay files are public, but private agent
  logs remain private.
- Kaggle CLI can list/download own submission episodes; high-rank public replay
  data is also available through official daily episode datasets.
- 4-player symmetry, replay/download UI, matchmaking, and leaderboard variance
  were recurring official/community topics.
- Community agents converged on production ROI, safe physics, future-world
  modeling, reinforcement/recapture, and multi-source pressure.
- Replay/episode tooling and datasets are valuable, but large daily datasets
  must be sampled carefully.
- Notebook titles or claimed LB scores were treated as claims only, not as
  official scores.

## 3. Public Agent Count And High-Value Agents

Registered Kaggle Code entries: 298.

Pulled/static scanned Kaggle notebooks or packages: 27.

Registered GitHub repos: 103.

Downloaded/static scanned GitHub repos: 16.

Loaded local public agents: 9.

Local smoke-tested agents: 8 match-smoked successfully; Producer V2 was recorded
but blocked by a missing local dependency in the extracted wrapper.

High-value public agents/repos:

- `pilkwang_structured`
- `tamrazov_starwars`
- `ykhnkf_distance_prioritized`
- `sigmaborov_reinforce`
- `vkhydras_peak_heuristic`
- `producer_agent` / `producer_v2`
- `sigmaborov_starter`
- `yuriygreben_architect`
- `konbu17_rule_ml_validator`
- `kashiwaba_rl_tutorial`
- `automatylicza/orbit-wars-lab`
- `michaelriedl/orbit-wars-torch`
- `emanuellcs/orbit-wars-beam-search`
- `alvinng4/OrbitWars`

## 4. Leaderboard And Gold Replay Visibility

Current public leaderboard was visible through Kaggle CLI on 2026-06-16.

Final medal teams were not available in this session. Therefore gold-team replay
analysis was not performed and no gold-team strategy claim is made.

Current high-rank replay samples were visible through official daily episode
datasets. Those samples include public replay actions and observations, but not
private agent code or private logs.

Gold team replay is not accessible in this session.

Reason: final gold teams do not exist or are not identifiable yet as final medal
teams in the 2026-06-16 session.

Evidence:

- CLI leaderboard is visible.
- Top-team names and public ratings are visible.
- Final medal labels are not visible.
- Current high-rank daily replay samples are visible.
- Direct `episodes` queries using top leaderboard team ids returned no episodes
  in this session, while daily replay datasets provided visible samples.

Next manual check:

- Recheck final leaderboard after medals/final standings are published.
- For final gold teams, check profile notebooks, discussion posts, and replay
  dataset mapping again.

## 5. Visible High-Rank Replay Strategy Notes

Only current high-rank sample replays were analyzed, not final gold replays.

Observed sample-level patterns:

- Opening had selective expansion, usually 2-5 neutral captures in the first 50
  turns for sampled high-rank players.
- First attacks in one top sample appeared around turns 23-30.
- Opening commit ratios were high in the extracted sample, often near 0.9-1.0.
- High-production target ratio was visible and material in the sampled opening.
- Midgame showed reinforcement-like sends, target switching, and occasional
  multi-source behavior.
- Late-game 300-500 behavior was not extractable from the small sample because
  sampled games ended before turn 300.

No unseen gold replay strategy is inferred.

## 6. Macro Strategy Classification

The audit defines 15 macro families in `configs/strategy_taxonomy.yaml`:

1. `nearest_expander`
2. `production_greedy_expander`
3. `distance_prioritized_rusher`
4. `center_control_agent`
5. `sun_dodge_physics_agent`
6. `world_model_forecaster`
7. `defense_reinforcement_agent`
8. `multi_source_gangup_agent`
9. `comet_greedy_agent`
10. `big_stack_hammer`
11. `total_war_endgame_agent`
12. `crash_exploit_or_collision_agent`
13. `turtle_defender`
14. `RL_policy_agent`
15. `hybrid_layered_agent`

Most mainstream public strong agents are not single-trick bots. The dominant
strong public cluster is `hybrid_layered_agent`: safe physics plus world model,
reinforcement/recapture, target scoring, multi-source pressure, comet handling,
and endgame thresholds.

The most strategically important separate public family is
`production_greedy_expander`, especially Producer-style ROI planners.

## 7. Current Profiler Coverage

The current profiler can weakly or partially cover:

- early direct pressure through `enemy_rusher`
- neutral expansion pressure through `neutral_rusher`
- large sends through `big_stack`
- comet targeting through `comet_greedy`
- self-targeting/reinforcement-like behavior through `reinforce_heavy`
- weak-enemy targeting through `weakest_targeter`
- contested target pile-on through current `crash_exploiter` feature
- low-send behavior through `turtle`

These are useful first-pass features, but most are cumulative ratios rather than
phase-aware behavioral models.

## 8. Current Profiler Gaps

Major gaps:

- `weak_bot` is not implemented; it is always `0.0`.
- `production_greedy` is computed but not consumed by counter policy.
- `center_greedy` is computed but not consumed by counter policy.
- true recapture/recent ownership transition behavior is not detected.
- true multi-source convergence is not detected.
- true crash exploit is not detected; current feature only means "targets an
  existing conflict".
- comet timing around expected windows is not modeled.
- world-model/search/RL behavior is not directly identifiable.
- 4-player threat prioritization is too coarse.
- `observed_turns` is currently planet-count weighted, which distorts turtle and
  confidence timing.

## 9. Counter Policy Assessment

Directionally reasonable, but too broad and too late.

Reasonable parts:

- rush -> more reserve/defense
- turtle -> more expansion/comet
- overcommit -> counterattack
- comet targeter -> contest comet more
- big stack -> more defense/counterattack

Problems:

- It is global across enemies, which is risky in 4-player.
- It is wrapper-level; base agent chooses actions before adaptive supplements.
- `risky_expansion_penalty` is written but not consumed.
- `center_weight_mult` can be read but is never changed by counter policy.
- `production_greedy`, `center_greedy`, and `weak_bot` do not affect runtime.
- Current thresholds have not been validated with per-turn traces.

## 10. Top 5 Optimization Directions

1. Add profile trace logging and run it across the public P0 agent pool.
2. Fix `observed_turns` / confidence accounting.
3. Build a repeatable opponent-family benchmark pool.
4. Add recently-captured/recapture detection and conservative recapture bonus.
5. Activate production-greedy and high-production/center control counters.

## 11. Recommended Next First Task

Next first task: profile trace logging.

Reason: without per-turn recognition traces, threshold changes and new counter
branches will remain guesswork. The trace harness should be local-only, optional,
and write outputs under ignored `outputs/profile_traces/`.

## 12. Submission Status

Kaggle competition submission: No.

No `kaggle competitions submit` command was called in this audit.

Git commits were made for audit artifacts only.

## 13. Source Links

- Competition: https://www.kaggle.com/competitions/orbit-wars
- Episodes index dataset: https://www.kaggle.com/datasets/kaggle/orbit-wars-episodes-index
- Pilkwang structured baseline: https://www.kaggle.com/code/pilkwang/orbit-wars-structured-baseline
- Tamrazov Star Wars: https://www.kaggle.com/code/romantamrazov/orbit-star-wars-lb-max-1224
- YKHNKF distance prioritized: https://www.kaggle.com/code/ykhnkf/distance-prioritized-agent-lb-max-score-1100
- Producer agent: https://www.kaggle.com/code/slawekbiel/the-producer-agent
- Vkhydras heuristic bots: https://github.com/vkhydras/orbit-wars-heuristic-bots
- Orbit Wars lab: https://github.com/automatylicza/orbit-wars-lab
