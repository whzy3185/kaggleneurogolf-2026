# Tournament Base vs Adaptive

Date: 2026-06-17

Scope: local evaluation only. These results are not official leaderboard scores. No `kaggle competitions submit` command was run.

## Runner Changes

The original `scripts/run_tournament.py` file-agent run was stopped after it exceeded 30 minutes without writing incremental results. The stopped command was:

```text
python scripts/run_tournament.py gauntlet local/agents/variants/adaptive_full --opponents local/agents/base_agent_entry --seeds 1..50 --bidirectional
```

To make long evals auditable, `scripts/run_eval_tournament.py` was added. It:

- reloads agent modules for each match so global profiler state does not leak across games;
- calls Kaggle's local Orbit Wars environment with callable agents;
- writes `outputs/tournament_raw/*/matches.csv` after every match;
- writes `outputs/tournament_raw/*/results.json` at the end;
- supports 2-player pair, gauntlet, and 4-player free-for-all smoke runs.

`outputs/` is gitignored and was not staged.

## Variants

| variant | entrypoint | notes |
| --- | --- | --- |
| base | `local/agents/base_agent_entry` | selected Pilkwang structured base through `agents/base_agent.py` |
| adaptive_full | `local/agents/variants/adaptive_full` | profiler + all current counter branches + supplemental moves |
| adaptive_no_profiler | `local/agents/variants/adaptive_no_profiler` | configured for later ablation |
| adaptive_defense_only | `local/agents/variants/adaptive_defense_only` | configured for later constrained candidate testing |

## Formal Base vs Adaptive Result

Command:

```text
python scripts/run_eval_tournament.py --series base_vs_adaptive_full_50 --seeds 1-50 --out outputs/tournament_raw/base_vs_adaptive_full_50 --progress pair local/agents/base_agent_entry local/agents/variants/adaptive_full --bidirectional
```

Result:

| metric | base | adaptive_full |
| --- | ---: | ---: |
| games | 100 | 100 |
| wins | 97 | 3 |
| winrate | 97.0% | 3.0% |
| avg rank | 1.03 | 1.97 |
| avg final ships | 5117.51 | 80.45 |
| timeout/error count | 0 | 0 |

Position sensitivity:

| adaptive_full position | adaptive wins | base wins |
| ---: | ---: | ---: |
| player 0 | 0 | 50 |
| player 1 | 3 | 47 |

Seed sensitivity:

- `randomSeed` values 1 through 50 were passed to the local Kaggle environment.
- Every match completed with status `ok`.
- adaptive_full won only 3 of 50 bidirectional seed pairs, and never swept a seed pair.

Interpretation:

adaptive_full is clearly weaker than the selected base agent. This is not a runtime stability failure; it is a negative strategic integration result.

## Public Opponent Screening

The full requested 20 seeds per public opponent was not completed after the direct base-vs-adaptive result showed a severe regression. Instead, a seed-1 bidirectional screening was run to avoid a starter-only conclusion and to check direction against the public pool.

adaptive_full command:

```text
python scripts/run_eval_tournament.py --series adaptive_full_public_screen_seed1 --seeds 1 --out outputs/tournament_raw/adaptive_full_public_screen_seed1 --progress gauntlet local/agents/variants/adaptive_full --opponents baselines/starter local/agents/public/pilkwang_structured local/agents/public/tamrazov_starwars local/agents/public/sigmaborov_reinforce local/agents/public/ykhnkf_distance_prioritized local/agents/public/vkhydras_peak_heuristic local/agents/public/vkhydras_last_heuristic --bidirectional
```

base command used the same opponent list with `local/agents/base_agent_entry`.

| opponent | adaptive_full result | base result |
| --- | ---: | ---: |
| starter | 2-0 | 2-0 |
| pilkwang_structured | 0-2 | 1-1 |
| tamrazov_starwars | 0-2 | 1-1 |
| sigmaborov_reinforce | 0-2 | 2-0 |
| ykhnkf_distance_prioritized | 0-2 | 0-2 |
| vkhydras_peak_heuristic | 0-2 | 0-2 |
| vkhydras_last_heuristic | 0-2 | 0-2 |

Screening interpretation:

- adaptive_full only beats starter in this screen.
- adaptive_full underperforms base against Pilkwang, Tamrazov, and SigmaBorov in the same seed-1 bidirectional setup.
- This screening is not a replacement for the originally requested 20-seed public-opponent tournament. It is enough to support the Stage 3 stop condition because adaptive_full already lost decisively to base in 100 direct games.

## 4-Player Smoke

Command:

```text
python scripts/run_eval_tournament.py --series four_player_smoke_seed1 --seeds 1 --out outputs/tournament_raw/four_player_smoke_seed1 --progress free-for-all --agents local/agents/base_agent_entry local/agents/variants/adaptive_full local/agents/public/tamrazov_starwars local/agents/public/sigmaborov_reinforce
```

Result:

| agent | rank | final ships | win |
| --- | ---: | ---: | --- |
| tamrazov_starwars | 1 | 4109 | yes |
| base_agent_entry | 2 | 0 | no |
| adaptive_full | 2 | 0 | no |
| sigmaborov_reinforce | 2 | 0 | no |

The 4-player runner works, but only a smoke test was run. The requested 20-seed 4-player evaluation was not run because the 2-player formal test already triggered the "adaptive weaker than base" stop condition, and local match runtime is high.

## Decision

Do not package or submit adaptive_full.

Proceed to Stage 4 and constrain the adaptive layer. The most likely causes are:

- supplemental moves consume or redirect ship budget after the base agent has already made its plan;
- high-risk policy branches such as `neutral_rusher`, `turtle`, `overcommitter`, and `comet_greedy` can push extra attacks/expansion into a base strategy that is already strong;
- confidence-gated profile reactions are not integrated into the base agent's internal scoring, so they operate as late add-ons rather than coherent planning.

Immediate Stage 4 direction:

1. Make the final candidate conservative by default.
2. Prefer base fallback or defense-only behavior over full supplemental policy.
3. Keep public-opponent and 4-player full-size evals blocked until the constrained variant can at least approach base in direct head-to-head.
