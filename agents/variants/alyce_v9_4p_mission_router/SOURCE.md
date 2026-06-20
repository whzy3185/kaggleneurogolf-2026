# Alyce V9 4P Mission Router Source

Source id: `alyce_v9_4p_mission_router`

Date: 2026-06-20

## Lineage

This variant is derived from the current official best in this repository:

```text
agents/variants/alyce_v6_prod_gap_mode
submission_id: 53852919
public score snapshot: 1177.8
```

The upstream public lineage remains:

```text
Kaggle code: alycemiki/light-ver-1200-simple-orbit-intruder
Author: Alyce Miki
URL: https://www.kaggle.com/code/alycemiki/light-ver-1200-simple-orbit-intruder
```

## Why V9 Exists

V7 and V8 were submitted only for data collection and did not replace V6:

```text
V7 official score: 920.2
V8 official score: 1134.8
V6 official score: 1177.8
```

The V6/V7/V8 replay review showed that selected-action recovery alone is not
enough. V9 starts again from V6 and adds a 4P-only mission router before greedy
selection.

## V9 Delta

V9 keeps V6 behavior:

- V2/V6 orbit-lite planner.
- 4P trap/contested/safe neutral scoring.
- source reserve and source depletion penalty.
- leader asset bonus and low-value rear enemy penalty.
- V5/V6 selected-action trace and V6 production-gap mode.
- 2P and 3P presets unchanged.

V9 adds in `main.py`:

- 4P close-enemy-count approximation per candidate target.
- true production rank/gap context inside the 4P candidate adjustment path.
- opening public-sacrifice penalty/veto for far, center, or shared-zone targets.
- contested center / middle-galaxy penalty for step 35-90.
- trailing low-impact enemy penalty.
- bad leader-pressure penalty when a leader target is low production or not
  holdable.
- `ORBIT_V9_TRACE_PATH` alias for local selected-action trace output.

It does not:

- change 2P/3P config;
- add new supplemental attacks;
- hardcode opponents;
- use network access;
- read external data or secrets;
- modify bundled `orbit_lite/` helper code.

## Current Status

```text
local research candidate
not submitted
not promoted
```
