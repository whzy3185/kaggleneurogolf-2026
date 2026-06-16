# Orbit Wars Open Source Code Map

Date: 2026-06-16

This map groups public Orbit Wars code into reusable categories. Paths under
`external/` are local ignored audit copies, not committed source dependencies.

## Direct Public Opponent Candidates

| Source | Local path | Main assets | Strategy notes |
|---|---|---|---|
| Kaggle `pilkwang/orbit-wars-structured-baseline` | `external/kaggle_notebooks/pilkwang__orbit-wars-structured-baseline` | `submission.py` written from notebook | Layered world model, timeline simulation, reinforcement, recapture, swarm, crash exploit. |
| Kaggle `romantamrazov/orbit-star-wars-lb-max-1224` | `external/kaggle_notebooks/romantamrazov__orbit-star-wars-lb-max-1224` | `submission.py` | Pilkwang-family layered hybrid with world-model/action scoring. |
| Kaggle `ykhnkf/distance-prioritized-agent-lb-max-score-1100` | `external/kaggle_notebooks/ykhnkf__distance-prioritized-agent-lb-max-score-1100` | `submission.py` | Distance-prioritized opponent/target weighting on layered baseline. |
| Kaggle `sigmaborov/lb-958-1-orbit-wars-2026-reinforce` | `external/kaggle_notebooks/sigmaborov__lb-958-1-orbit-wars-2026-reinforce` | `submission.py` | Reinforcement/defense-heavy public baseline. |
| Kaggle `slawekbiel/the-producer-agent` | `external/kaggle_notebooks/slawekbiel__the-producer-agent` | `main.py` | ROI production planner and frontline redeployment. |
| Kaggle `slawekbiel/the-producer-v2` | `external/kaggle_notebooks/slawekbiel__the-producer-v2` | `main.py` | Producer with improved enemy-flow/reinforcement modeling. |
| GitHub `vkhydras/orbit-wars-heuristic-bots` | `external/github_zip_repos/vkhydras__orbit-wars-heuristic-bots` | versioned `.py` submissions | Peak heuristic archive, including stack aggregation, reinforcement, doom evacuation, 2P focus variants. |
| GitHub `ayushmk7/OrbitWarsKaggle` | `external/github_zip_repos/ayushmk7__OrbitWarsKaggle` | `main.py`, `src/`, `submission/` | Traceable rule-based workspace with local eval/source split. |
| GitHub `alvinng4/OrbitWars` | `external/github_zip_repos/alvinng4__OrbitWars` | `main.py`, `src/`, `testing_env/` | Precompute/intercept lookup style; close to discussion post on C lookup tables. |
| GitHub `JTHCode/orbit-wars-agent` | `external/github_zip_repos/JTHCode__orbit-wars-agent` | `main.py`, `orbit_agent/core.py`, build script | Compact production agent candidate. |
| GitHub `dyyfk/Kaggle_Orbit_Wars_Refactored` | `external/github_zip_repos/dyyfk__Kaggle_Orbit_Wars_Refactored` | `main.py`, `sim.py`, `train.py`, tests | Rule-based candidate generation plus learned MLP scorer. |

## Evaluation And Replay Tooling

| Source | Assets | Use |
|---|---|---|
| GitHub `automatylicza/orbit-wars-lab` | `agents/`, `orbit_wars_app/`, Docker/web UI | Local tournament runner, visualizer, bundled agents, TrueSkill-like leaderboard. |
| GitHub `MatthewWHuang/orbit-wars` | `tournament.py`, `visualize.py`, `bundle.py`, `optimize.py`, `play_replay.py` | Visualizer, cinema/replay tooling, bundler, local tournament runner. |
| Kaggle `sangrampatil5150/api-download-replay-orbit-wars` | replay API notebook | Reference for public replay download workflow. |
| Kaggle `souldrive/why-cloning-the-1-bot-loses-to-greedy` | replay/BC analysis notebook | Evidence for replay action extraction and BC failure modes. |
| Kaggle daily datasets | `kaggle/orbit-wars-episodes-index`, top-10% replay datasets, Parquet replay DB | Replay-derived behavior features, profiler traces, mission labels. |

## Fast Environment / RL Infrastructure

| Source | Assets | Use |
|---|---|---|
| GitHub `michaelriedl/orbit-wars-torch` | `orbit_wars_torch/`, `example/train_ppo.py` | Batched PyTorch env reference for RL/rollout acceleration. |
| GitHub `vinupriyesh/kaggle-environments-orbit-wars` | `kaggle_environments/envs/orbit_wars/orbit_wars.py` | Official env fork/reference for engine behavior. |
| Kaggle `kashiwaba/orbit-wars-reinforcement-learning-tutorial` | `src/config.py`, `src/features.py`, `src/ppo.py`, `src/env.py` | PPO tutorial, feature pipeline, training structure. |
| GitHub `AdarshGoel2001/orbitWars` | BC/train scripts, action-space tools | Behavior cloning / self-play workspace; high dependency risk. |
| GitHub `MarianodelRio/OrbitWars` | `dataset/`, `bots/`, `trainer/`, `train.py` | PyTorch RL/BC bot workspace. |
| GitHub `TryDotAtwo/Orbit-Wars-2D-Transformer` | `kaggle_submission/`, `native/`, `crates/`, dashboard | Transformer trainer and native tooling; useful conceptually, build-heavy. |

## Physics, Aiming, And Search References

| Source | Assets | Use |
|---|---|---|
| Kaggle `slawekbiel/benchmark-for-aiming-implementation` | aiming benchmark notebook | Validate intercept/sun-safe aiming before changing attack generation. |
| GitHub `emanuellcs/orbit-wars-beam-search` | `src/`, `rules/`, CMake, `main.py`, `package_submission.py` | Native continuous physics + geometric beam-search agent. |
| GitHub `alvinng4/OrbitWars` | `src/`, `main.py`, `host/orbit_wars.py` | Intercept precompute/arrival-event ideas. |
| Kaggle `aidensong123/lb-highest-1000-search-learned-value-function` | `main.py`, value model loading | Simulated candidate outcomes ranked by learned value function. |
| Kaggle `yashm917/orbit-wars-sim-value-search-agent` | `main.py` | Sim + value search with defense and attack phases. |
| Kaggle `rahulchauhan016/orbit-wars-parallel-mcts-video-analytics` | MCTS/video analytics notebook | MCTS/analysis reference, not a drop-in agent. |

## Strategy Family Coverage From Open Source

The public codebase strongly covers:

- nearest/starter expansion
- production-greedy ROI planning
- distance-prioritized pressure
- sun-safe physics/aiming
- world-model forecasting
- reinforcement/recapture
- multi-source swarm/gang-up
- comet handling
- big-stack hammer / doom evacuation
- late/endgame flush
- RL / BC / transformer experiments
- replay datasets and behavioral analysis

The public codebase weakly covers:

- robust 4P coalition/threat prioritization
- reliable opponent-family profiler traces
- gold/final team strategy, because final medals do not exist yet and private
  code is not visible
- reproducible official leaderboard scoring, because matchmaking/scoring code is
  not fully public in discussions

## Next Use In This Project

1. Stage 5 should wrap only a small P0 pool first:
   `pilkwang_structured`, `tamrazov_starwars`, `sigmaborov_reinforce`,
   `ykhnkf_distance_prioritized`, `producer_v2`, and
   `vkhydras_peak_heuristic`.
2. Stage 8 taxonomy should treat Producer-style ROI planners and
   Pilkwang/Tamrazov world-model mission planners as different families.
3. Stage 9 profiler review should explicitly test for:
   recapture, big-stack hammer, defense reinforcement, production-greedy ROI,
   comet timing, and multi-source gang-up.
4. Code reuse must be gated by license, dependency size, `main.py` packaging,
   and smoke tests.

