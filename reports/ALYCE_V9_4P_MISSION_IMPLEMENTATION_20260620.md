# Alyce V9 4P Mission Implementation - 2026-06-20

## Scope

Implemented:

```text
agents/variants/alyce_v9_4p_mission_router
```

Base:

```text
agents/variants/alyce_v6_prod_gap_mode
```

This branch directly follows:

```text
reports/ALYCE_V9_4P_MISSION_AND_2P_REVIEW_TASK_CHAIN_20260620.md
reports/ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md
reports/ALYCE_V678_2P_CORNER_FORCE_REVIEW_20260620.md
```

## What Changed

Only the new V9 variant was modified. V6 is untouched.

V9 keeps:

```text
V6 official-best base
V6 4P trap/contested/safe neutral scoring
V6 source reserve and source depletion penalty
V6 selected-action trace/filter
V6 production-gap selected-action mode
2P/3P presets unchanged
```

V9 adds these config flags in `ProducerLiteConfig`:

```text
enable_v9_mission_router
v9_opening_end
v9_center_step_end
v9_center_dist
v9_far_dist
v9_safe_reaction_gap
v9_close_enemy_eta_margin
v9_public_depletion_ratio
v9_opening_public_penalty
v9_center_public_penalty
v9_public_hard_reaction_gap
v9_public_low_prod_max
v9_trailing_prod_gap
v9_trailing_prod_rank
v9_trailing_low_enemy_penalty
v9_leader_asset_prod_min
v9_leader_hold_reaction_gap
```

V9 adds these candidate-level signals inside the 4P candidate adjustment path:

```text
close_enemy_count
true production leader
production gap
production rank
target center distance
source depletion ratio
shared-zone target label
opening public-sacrifice label
contested-center label
trailing low-impact enemy label
bad leader-pressure label
```

## Mission Router Logic

The V9 router runs before greedy selection, not after a move has already been
chosen.

### Opening Public Sacrifice

Applies before step 35.

Penalizes or vetoes candidates that combine:

```text
public target: neutral or enemy
far target, center/middle target, or shared-zone target
unsafe reaction gap
source depletion or important source
```

Hard veto is limited to:

```text
low-production target
bad negative reaction gap
shared-zone target
high source depletion
```

The aim is to prevent the V6/V7/V8 replay pattern where a locally positive
capture becomes a public sacrifice for two other players.

### Contested Center / Middle Galaxy

Applies from step 35 to step 90.

Penalizes center/shared-zone candidates with weak reaction gap, especially when
the source is being depleted. This is intentionally a penalty, not a broad veto,
because V6/V8 winning games can still use center/frontier pressure when the
board state is favorable.

### Trailing Low-Impact Enemy

Applies when:

```text
prod_gap <= -6
or prod_rank >= 3
```

Penalizes low-production enemy targets with unsafe reaction gaps. This follows
the V6/V7/V8 replay conclusion that attacking low-impact targets while trailing
often increases direct response pressure without improving rank.

### Leader Pressure Gate

While trailing, V9 penalizes leader-owned targets that are:

```text
low production
or not holdable by reaction-gap proxy
```

This is meant to avoid kingmaking: damaging the leader only matters when the
target is holdable or rank-improving.

## 2P Status

No 2P policy change was made.

Reason:

```text
reports/ALYCE_V678_2P_CORNER_FORCE_REVIEW_20260620.md found that 2P corner and
edge play is not cleanly bad. Many winning games also use high-commit corner
sends. The correct next 2P branch should be trace-first, not a broad filter.
```

## Verification

Commands run:

```text
python -m py_compile agents/variants/alyce_v9_4p_mission_router/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v9_4p_mission_router
```

Result:

```text
py_compile: pass
smoke: pass
sample_actions_ok: true
env_status: ok
```

## Decision

V9 is a local research candidate.

Do not submit V9 from this implementation alone.
