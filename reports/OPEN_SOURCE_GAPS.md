# Open Source Gaps

Date: 2026-06-16

Resolved in this pass:

- `automatylicza/orbit-wars-lab` cloned to ignored `external/`.
- `vkhydras/orbit-wars-heuristic-bots` cloned to ignored `external/`.
- `projectedanx/kaggle-orbit-wars-2026` cloned to ignored `external/`.
- Bundled `orbit-wars-lab` metadata inspected for Pilkwang, Tamrazov, Ykhnkf,
  Sigmaborov, Yuriy Greben, Kashiwaba RL, and Pascal Orbitwork.

Gaps:

| Source | Gap | Impact | Next action |
|---|---|---|---|
| `ayushmk7/OrbitWarsKaggle` | SSH/HTTPS clone timed out and left only an empty `.git` dir | Cannot evaluate yet | Retry later or inspect with browser |
| `abdulbasith5/OrbitWars_Kaggle` | SSH/HTTPS clone timed out and left only an empty `.git` dir | Cannot evaluate yet | Retry later or inspect with browser |
| `michaelriedl/orbit-wars-torch` | clone timed out or repo unavailable in this run | RL track not available | Deprioritize until heuristic track is benchmarked |
| Kaggle discussion posts | Not locally mirrored | Some engine-update details may be missing | Use `orbit-wars-lab` note about 2026-04-25 reset as current guardrail |

Safety notes:

- `external/` remains ignored and must not be committed.
- Author LB claims stay as claims until reproduced or submitted by this account.
- The official starter score `317.8` is the only current official score in our
  scorecard.
