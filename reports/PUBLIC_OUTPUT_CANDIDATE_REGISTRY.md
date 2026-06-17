# Public Output Candidate Registry

Date: 2026-06-17

## Purpose

This registry promotes the fresh Kaggle public output packages found during the
source recheck into the local candidate pool. The goal is to reselect the base
agent from actual runnable output packages before doing any further targeted
filter work.

## Scope Guard

- These entries are Kaggle public output packages, not just notebook source
  listings.
- Several candidates are multi-file submissions with `main.py` plus support
  modules such as `orbit_lite/`.
- They are registered for local benchmarking only.
- Their notebook titles or public claims are not treated as our official score.
- Their local tournament results are not leaderboard scores.
- License and attribution risk remains separate from local benchmarking.
- The package contents remain under ignored `external/` paths and are not
  committed.

## Primary Fresh Output Candidates

| ID | Kaggle slug | Package type | Smoke | Min screen vs Vkhydras |
|---|---|---|---|---:|
| `ranjeet_producer` | `ranjeet258/orbit-wars-producer` | multi-file output | pass | 6-0 |
| `tamrazov_stronger` | `romantamrazov/orbit-wars-i-m-stronger` | multi-file output | pass | 6-0 |
| `alyce_intruder` | `alycemiki/light-ver-1200-simple-orbit-intruder` | multi-file output | pass | 6-0 |
| `caoyupeng_gru` | `caoyupeng/v2-gru` | multi-file output | pass | 5-1 |
| `shumming_exp50` | `shummingfang/orbit-wars-exp50` | multi-file output | pass | 6-0 |

Observed local cache paths:

```text
external/kaggle_outputs/ranjeet258__orbit-wars-producer/submission_extracted
external/kaggle_outputs/romantamrazov__orbit-wars-i-m-stronger/submission_extracted
external/kaggle_outputs/alycemiki__light-ver-1200-simple-orbit-intruder/submission_extracted
external/kaggle_outputs/caoyupeng__v2-gru/submission_extracted
external/kaggle_outputs/shummingfang__orbit-wars-exp50/submission_extracted
```

## Optional Expansion Candidates

The following outputs were also downloaded and smoke checked. They are kept out
of the first P0 base-selection set unless the primary pool is inconclusive:

- `reyhanksatria/orbit-wars-reyhan-ksatria`
- `mirzayasirabdullah07/best-orbit-wars-notebook`
- `jek1wantaufik/orbit-wars-submission-build-and-testing`
- `jek1wantaufik/simplified-orbit-wars-agent`
- `alycemiki/intervention-command-w-ffa`

## Baselines Kept For Comparison

| ID | Role |
|---|---|
| `vkhydras_last` | current official workspace best, but no longer assumed strongest public base |
| `pilkwang_structured` | previous official best and earlier base |
| `tamrazov_starwars` | public P0 benchmark |
| `sigmaborov_reinforce` | public P0 benchmark |
| `ykhnkf_distance_prioritized` | public P0 benchmark |
| `vkhydras_peak_heuristic` | public P0 benchmark |
| `current_dist_main` | current packaged local candidate |

## Current Evidence

The minimal 3-seed bidirectional screen from
`reports/PUBLIC_OUTPUT_SOURCE_RECHECK_20260617.md` is enough to reject
Vkhydras Last as the unquestioned base, but it is not enough to choose a new
base. The next gate is a larger 2-player round-robin and 4-player mixed-pool
screen.

## Next Action

Implement loader and runner support for directory-based multi-file candidates,
then run the fresh output screen before selecting `base_agent_v2`.
