# Source Registry

Date: 2026-06-16

This registry records public Orbit Wars sources for reuse and benchmarking. It
does not treat author LB claims as our official scores. Our only official score
so far is submission `53729904`, public score `600.0`, from the Kaggle starter.

| Source ID | Source | Evidence | Claimed/Observed | Status | Value |
|---|---|---|---:|---|---|
| `official_starter_600` | Kaggle official starter | S | observed 600.0 | submitted by us | score floor and contract check |
| `orbit_wars_lab` | `automatylicza/orbit-wars-lab` | B | n/a | cloned | evaluation harness and agent zoo |
| `pilkwang_structured` | Kaggle notebook via lab | B | ~1000 claim | available | likely base candidate |
| `tamrazov_starwars` | Kaggle notebook via lab | B | 1224 claim | available | strong benchmark |
| `ykhnkf_distance_prioritized` | Kaggle notebook via lab | B | 1100 claim | available | strong benchmark/base candidate |
| `sigmaborov_reinforce` | Kaggle notebook via lab | B | 958.1 claim | available | readable reinforce reference |
| `sigmaborov_starter` | Kaggle notebook via lab | B | n/a | available | compact sun-dodge/defense reference |
| `yuriygreben_architect` | Kaggle notebook via lab | B | n/a | available | 5-layer architecture reference |
| `kashiwaba_rl` | Kaggle notebook via lab | B | n/a | available | RL feature reference, not first base |
| `vkhydras_peak_heuristic` | GitHub archive | B | 1166.7 claim | cloned | high-value heuristic lineage |
| `vkhydras_last_heuristic` | GitHub archive | B | 1152.8 claim | cloned | opponent-intelligence ideas |
| `pascal_orbitwork_v14` | Kaggle notebook via lab | B | n/a | available | additional heuristic variant |
| `projectedanx_kaggle_orbit_wars_2026` | GitHub repo | C | n/a | cloned | low immediate value |
| `ayushmk7_orbitwarskaggle` | GitHub repo | C | n/a | clone timeout | pending verification |
| `abdulbasith5_orbitwars_kaggle` | GitHub repo | C | n/a | clone timeout | pending verification |
| `michaelriedl_orbit_wars_torch` | GitHub repo | C | n/a | clone timeout/missing | pending verification |

Evidence levels:

- S: official score from our own real submission.
- A: public output or notebook runnable with strong leaderboard evidence.
- B: complete code likely reproducible locally.
- C: idea, partial code, or unavailable in this run.
- D: low-value, unverifiable, duplicate, or high-risk source.

