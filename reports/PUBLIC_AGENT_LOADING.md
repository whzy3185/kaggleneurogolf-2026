# Public Agent Loading Report

Date: 2026-06-16

Scope: load high-value public Orbit Wars agents into a uniform local structure:

```text
agents/public/<source_id>/main.py
agents/public/<source_id>/SOURCE.md
agents/public/<source_id>/WRAPPER.md
```

All sources are public Kaggle/GitHub artifacts identified in the Stage 3/4
audit. Notebook title scores are treated as public claims only, not official
leaderboard evidence.

## Installed Agents

| source_id | priority | source | family | load status |
|---|---|---|---|---|
| `pilkwang_structured` | P0 | `pilkwang/orbit-wars-structured-baseline` | hybrid layered | already present, load ok |
| `tamrazov_starwars` | P0 | `romantamrazov/orbit-star-wars-lb-max-1224` | hybrid layered | load ok |
| `sigmaborov_reinforce` | P0 | `sigmaborov/lb-958-1-orbit-wars-2026-reinforce` | defense reinforcement | load ok |
| `ykhnkf_distance_prioritized` | P0 | `ykhnkf/distance-prioritized-agent-lb-max-score-1100` | distance prioritized | load ok |
| `vkhydras_peak_heuristic` | P0 | `vkhydras/orbit-wars-heuristic-bots` | hybrid layered | load ok |
| `producer_v2` | P1 | `slawekbiel/the-producer-v2` | production greedy | load failed: missing `orbit_lite` package |
| `sigmaborov_starter` | P1 | `sigmaborov/orbit-wars-2026-starter` | sun/physics starter | load ok |
| `yuriygreben_architect` | P1 | `yuriygreben/orbit-wars-physics-aware-architect` | world model | load ok |
| `konbu17_rule_ml_validator` | P1 | `konbu17/orbit-wars-rule-base-ml-shot-validator-hybrid` | hybrid layered + ML validator | load ok |

`producer_v2` was extracted from the public notebook, but its `main.py` imports
`orbit_lite.*` sibling modules that were not emitted by that notebook pull.
This is recorded as `missing dependency`; it should either be replaced with the
multi-file Producer package or loaded from a source that includes `orbit_lite/`.

## P0 Smoke Test

Command shape:

```bash
python scripts/run_match.py local/agents/public/<id> local/. --seed 1 --out outputs/public_agent_smoke/<id>_vs_main_seed1.json
```

The `local/` prefix is required by this repository's `orbitwars_eval.loader`.

| source_id | load_ok | match_ok | winner | scores | turns | duration_s |
|---|---:|---:|---|---:|---:|---:|
| `pilkwang_structured` | yes | yes | `local/agents/public/pilkwang_structured` | `[1049, 0]` | 131 | 3.52 |
| `tamrazov_starwars` | yes | yes | `local/agents/public/tamrazov_starwars` | `[7298, 0]` | 247 | 8.38 |
| `sigmaborov_reinforce` | yes | yes | `local/agents/public/sigmaborov_reinforce` | `[3882, 0]` | 171 | 1.68 |
| `ykhnkf_distance_prioritized` | yes | yes | `local/agents/public/ykhnkf_distance_prioritized` | `[4309, 0]` | 165 | 6.01 |
| `vkhydras_peak_heuristic` | yes | yes | `local/agents/public/vkhydras_peak_heuristic` | `[2868, 0]` | 79 | 0.85 |

These are local smoke checks only. They are not official leaderboard scores,
not tournament rankings, and not a claim that the current adaptive agent has
those margins in real Kaggle play.

## P1 Smoke Test

| source_id | load_ok | match_ok | winner | scores | turns | duration_s |
|---|---:|---:|---|---:|---:|---:|
| `sigmaborov_starter` | yes | yes | `local/agents/public/sigmaborov_starter` | `[3045, 0]` | 102 | 0.87 |
| `yuriygreben_architect` | yes | yes | `local/agents/public/yuriygreben_architect` | `[2376, 0]` | 119 | 2.69 |
| `konbu17_rule_ml_validator` | yes | yes | `local/agents/public/konbu17_rule_ml_validator` | `[2846, 0]` | 175 | 11.88 |
| `producer_v2` | no | no | n/a | n/a | n/a | n/a |

## Loading Notes

- Notebook sources that wrote `submission.py` were stored as local `main.py`.
- Additional writefile modules were copied when present, e.g.
  `konbu17_rule_ml_validator/decode_weights.py`.
- `pilkwang_structured` already existed before this stage; this stage added
  `WRAPPER.md`.
- `configs/public_agent_pool.yaml` records source, priority, load status, and
  smoke outputs.

## Next Loading Work

1. Replace or complete `producer_v2` with a source that includes `orbit_lite/`.
2. Add bidirectional smoke tests so each public agent also plays as player 1.
3. Add a small public-agent benchmark pool config for Stage 10 validation.
4. Consider wrapping GitHub agents from `ayushmk7`, `alvinng4`, `JTHCode`, and
   `dyyfk` after the P0/P1 pool is stable.

