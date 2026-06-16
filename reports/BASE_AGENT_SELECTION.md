# Base Agent Selection

Date: 2026-06-16

Selected base agent: `pilkwang_structured`.

This is based on a local smoke round-robin, not an official Kaggle score.

## Candidate Results

Command:

```powershell
python scripts\run_tournament.py round-robin `
  --agents external/pilkwang-structured external/tamrazov-starwars external/ykhnkf-distance-prioritized external/sigmaborov-reinforce baselines/starter `
  --seeds 401,402 `
  --out outputs\eval\base_selection_rr
```

Summary:

| Candidate | Wins | Losses | Draws | Errors | Games |
|---|---:|---:|---:|---:|---:|
| `external/pilkwang-structured` | 8 | 0 | 0 | 0 | 8 |
| `external/tamrazov-starwars` | 5 | 3 | 0 | 0 | 8 |
| `external/sigmaborov-reinforce` | 5 | 3 | 0 | 0 | 8 |
| `baselines/starter` | 2 | 6 | 0 | 0 | 8 |
| `external/ykhnkf-distance-prioritized` | 0 | 8 | 0 | 0 | 8 |

## Why Not Starter

The official starter was already used for the connectivity submission and got
official public score `317.8`. It is a contract baseline, not a strategy base.
It lacks a world model, defensive forecast, and scoring architecture.

## Why Pilkwang

- Best local smoke record: 8-0.
- Apache 2.0 metadata in `orbit-wars-lab`.
- Clear Physics + WorldModel + Strategy architecture.
- Exposes both `agent()` and `build_world()`, which gives us a bridge for
  safety wrappers and future score-modifier integration.
- Lower immediate integration risk than the largest simulation-heavy variants.

## Risks

- The smoke round-robin used only two seeds.
- `orbit-wars-lab` local results are not official scores.
- Author metadata notes strong 1v1 and weak 1v3 behavior.
- Further evaluation must include 4-player and held-out public opponents.

## Current Files

| File | Purpose |
|---|---|
| `agents/public/pilkwang_structured/main.py` | tracked source copy |
| `agents/public/pilkwang_structured/SOURCE.md` | provenance and hash |
| `agents/base_agent.py` | stable wrapper |
| `configs/base_agent.yaml` | selection metadata |
