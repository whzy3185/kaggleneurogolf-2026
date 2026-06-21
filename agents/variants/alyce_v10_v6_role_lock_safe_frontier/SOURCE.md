# Alyce V10 V6 Role Lock Safe Frontier Source

Source id: `alyce_v10_v6_role_lock_safe_frontier`

Date: 2026-06-21

## Lineage

This variant is derived directly from:

```text
agents/variants/alyce_v6_prod_gap_mode
```

It intentionally does not derive from V7, V8, or V9. Those branches are retained
as official replay evidence and regression opponents, not as the parent code.

The upstream public lineage remains:

```text
Kaggle code: alycemiki/light-ver-1200-simple-orbit-intruder
Author: Alyce Miki
URL: https://www.kaggle.com/code/alycemiki/light-ver-1200-simple-orbit-intruder
```

## Why V10 Exists

The V5+ report chain established:

- V6 is the current official best in this repo.
- V7/V8 selected-action filtering did not beat V6 officially.
- V9 improved some early 4P production snapshots but increased third-party
  cleanup risk, so it is rejected as a promotion candidate.
- High-rank public replay summaries emphasize durable step50 to step100
  production conversion, not raw extra aggression.

The design report is:

```text
reports/HIGH_RANK_STRATEGY_RESEARCH_AND_V10_TASK_CHAIN_20260621.md
```

## V10 Delta

V10 changes only `main.py` relative to V6.

It keeps V6 behavior:

- 2P and 3P presets are unchanged.
- V6 4P FFA target-quality adjustments remain.
- V6 selected-action trace and production-gap selected-filter remain.
- Bundled `orbit_lite/` helper code is unchanged.

It adds a 4P-only conservative layer:

- source-centric reserve lock before candidate construction;
- source/region commitment-style blackout through stricter early/mid drain;
- anti-public-good hard veto for multi-enemy, unsafe-reaction, source-depleting
  actions;
- center/shared-zone sacrifice penalty;
- trailing low-value nonleader enemy attack penalty;
- small safe-frontier bonus for already-valid, high-production, low-cleanup-risk
  targets;
- `ORBIT_V10_TRACE_PATH` support for local inspection.

It does not:

- add standalone new attacks;
- hardcode opponent names;
- read external data or secrets;
- use network access;
- change 2P/3P presets;
- submit to Kaggle by itself.

## Current Status

```text
local V10 candidate
not submitted
not promoted
```
