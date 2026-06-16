# Orbit Wars GitHub Repository Review

Date: 2026-06-16

This audit registers GitHub repositories related to Orbit Wars and statically
scans the mandatory/high-value subset. Large cloned/downloaded contents are
kept under ignored `external/` directories.

## Collection Methods

- GitHub REST repository search for:
  - `orbit-wars`
  - `"orbit wars" kaggle`
  - `kaggle orbit wars`
  - `orbit_wars agent`
  - `OrbitWarsKaggle`
  - `orbit-wars-heuristic`
  - `orbit-wars-torch`
  - `"orbit wars" reinforcement`
  - `"orbit wars" baseline`
- Direct GitHub metadata calls for mandatory/high-value repositories.
- GitHub zipball download into `external/github_zip_repos/`.
- Filtered zipball extraction for `abdulbasith5/OrbitWars_Kaggle` because the
  repository includes a large `.venv/site-packages` tree with deep Windows
  paths.

`gh` CLI was not installed in this environment, so this stage used public REST
API calls and zipballs. Unauthenticated GitHub API rate limit was reached near
the end of direct metadata refresh; search results and local zip scans were
already available.

## Coverage

- GitHub search/API registered repositories: 103
- High-value repositories downloaded and statically scanned: 16
- Registry output: `configs/github_repo_registry.yaml`
- Code map output: `reports/OPEN_SOURCE_CODE_MAP.md`

## Mandatory Repositories

| Repo | Status | Strategy / role | Valuable files | Risk / reuse |
|---|---|---|---|---|
| `automatylicza/orbit-wars-lab` | downloaded | local tournament runner + visualizer | `README.md`, `agents/`, `orbit_wars_app/`, `tests/`, `docs/` | Tooling/reference only; useful for local eval and bundled public agents. |
| `ayushmk7/OrbitWarsKaggle` | downloaded | traceable rule-based / source agent | `main.py`, `src/`, `submission/`, `tests/`, `docs/` | Candidate source/reference after wrapper smoke test. |
| `abdulbasith5/OrbitWars_Kaggle` | filtered download | hybrid RL/rule agent workspace | `main.py`, `rl/`, `reports/`, `local_eval.py` | Repository includes `.venv`; filtered extraction required; high import risk. |
| `vkhydras/orbit-wars-heuristic-bots` | downloaded | heuristic bot archive / peak heuristic | versioned `.py` bot files | High-value opponent pool source; files are standalone versions and need wrapper naming. |
| `projectedanx/kaggle-orbit-wars-2026` | downloaded | experimental hybrid workspace | many docs/tests/scripts | Noisy experimental workspace; inspect before reusing anything. |
| `michaelriedl/orbit-wars-torch` | downloaded | batched PyTorch environment | `orbit_wars_torch/`, `example/train_ppo.py` | Fast-env/RL reference, not a direct opponent agent. |
| `vinupriyesh/kaggle-environments-orbit-wars` | downloaded | official env fork | `kaggle_environments/envs/orbit_wars/orbit_wars.py` | Environment reference; do not treat as a strategy agent. |

## Additional High-Value Repositories

| Repo | Strategy / role | Why it matters |
|---|---|---|
| `MatthewWHuang/orbit-wars` | tooling visualizer/tournament/bundler | Matches high-value discussion tooling; includes replay/visualize/tournament/bundle scripts. |
| `alvinng4/OrbitWars` | precompute/physics agent | Companion to C lookup precompute discussion; includes `main.py`, host env, tournament runner. |
| `emanuellcs/orbit-wars-beam-search` | world-model beam search / native | C++20 beam-search agent and Python packaging/opponents; strategically valuable but build-heavy. |
| `PERO-99/nova-orbit-agent` | hybrid layered agent | Submission-ready agent with validation scripts, tournament tooling, UI. |
| `JTHCode/orbit-wars-agent` | hybrid layered agent | Compact `main.py` + `orbit_agent/core.py` + build script. |
| `AdarshGoel2001/orbitWars` | RL / BC workspace | Behavior cloning/training scripts and submission code; high dependency risk. |
| `MarianodelRio/OrbitWars` | RL bot workspace | Dataset, bots, trainer, PPO/torch style layout. |
| `TryDotAtwo/Orbit-Wars-2D-Transformer` | transformer/RL trainer | Native/Rust/dashboard plus Kaggle submission path; high build/dependency risk. |
| `dyyfk/Kaggle_Orbit_Wars_Refactored` | rule-based + MLP scorer | Small `main.py`, `sim.py`, `train.py`, tests, viz. |

## Repository Family Counts

From the registry tags:

| Family | Count |
|---|---:|
| unknown_or_low_signal | 58 |
| hybrid_layered_agent | 18 |
| tooling_visualizer_tournament | 8 |
| RL_policy_agent | 7 |
| world_model_forecaster | 4 |
| hybrid_rl_rule_agent | 1 |
| precompute_physics_agent | 1 |
| traceable_rule_based_agent | 1 |
| hybrid_ml_scorer_agent | 1 |
| world_model_beam_search_agent | 1 |
| fast_env_rl_tooling | 1 |
| experimental_hybrid_workspace | 1 |
| official_env_fork | 1 |

## Main Findings

1. GitHub open source is more tooling-heavy than Kaggle Code.
   The highest-confidence GitHub repos are visualizers, tournament runners,
   env forks, fast RL environments, and development workspaces rather than
   clean drop-in agents.

2. The most reusable direct opponent sources are limited.
   `vkhydras/orbit-wars-heuristic-bots`, `ayushmk7/OrbitWarsKaggle`,
   `alvinng4/OrbitWars`, `emanuellcs/orbit-wars-beam-search`,
   `PERO-99/nova-orbit-agent`, `JTHCode/orbit-wars-agent`, and
   `dyyfk/Kaggle_Orbit_Wars_Refactored` are the most obvious candidates for
   wrapper work.

3. Native/search repos are strategically valuable but not cheap to load.
   `emanuellcs/orbit-wars-beam-search` and `TryDotAtwo/Orbit-Wars-2D-Transformer`
   use native/build or dashboard components. They should inform strategy and
   benchmarks before being treated as easy opponent pool entries.

4. RL/BC repos reinforce the discussion consensus.
   RL work focuses on faster environments, replay datasets, BC/PPO, transformers,
   and opponent pools. These are useful as opponent families and future research
   direction, but high risk for immediate submission reuse.

5. Some repositories contain bulky or unsafe-to-vendor artifacts.
   `abdulbasith5/OrbitWars_Kaggle` includes `.venv/site-packages`; model
   checkpoints also appear in some repos. These should stay in ignored
   `external/` and never be vendored into the submission repo without license
   and size review.

## Stage 5 Loading Recommendations

Load first:

- `vkhydras/orbit-wars-heuristic-bots`
- `ayushmk7/OrbitWarsKaggle`
- `alvinng4/OrbitWars`
- `JTHCode/orbit-wars-agent`
- `dyyfk/Kaggle_Orbit_Wars_Refactored`

Inspect before loading:

- `PERO-99/nova-orbit-agent`
- `emanuellcs/orbit-wars-beam-search`
- `AdarshGoel2001/orbitWars`
- `abdulbasith5/OrbitWars_Kaggle`

Use as tooling/reference:

- `automatylicza/orbit-wars-lab`
- `MatthewWHuang/orbit-wars`
- `michaelriedl/orbit-wars-torch`
- `vinupriyesh/kaggle-environments-orbit-wars`

