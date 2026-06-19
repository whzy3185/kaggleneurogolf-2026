# Alyce V6 Production Gap Mode Source

Source id: `alyce_v6_prod_gap_mode`

Date: 2026-06-19

## Lineage

This variant is derived from the current repo practical baseline:

```text
agents/variants/alyce_4p_ffa_v2
```

The upstream public lineage remains:

```text
Kaggle code: alycemiki/light-ver-1200-simple-orbit-intruder
Author: Alyce Miki
URL: https://www.kaggle.com/code/alycemiki/light-ver-1200-simple-orbit-intruder
```

Attribution remains attached to Alyce Miki and the referenced Producer/Orbit
Wars utility lineage recorded in the V2 source notes.

## Why V6 Exists

Previous reports rejected the V3/V4 direction:

```text
reports/ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md
```

The key lesson was that V4 used the wrong parent branch and added a broad score
layer without selected-action proof. V6 starts from V2 instead and preserves the
V2 4P mission filter.

## V6 Delta

V6 changes only `main.py`.

It keeps V2's 4P behavior:

- severe trap neutral hard veto;
- soft contested neutral penalty;
- safe neutral bonus;
- source reserve and source depletion penalty;
- leader asset bonus;
- low-value rear enemy penalty.

It adds:

- selected-action trace via `ORBIT_V6_TRACE_PATH`;
- a narrow 4P-only selected top-candidate replacement filter;
- a 4P early/mid production-gap mode.

The filter only acts when:

```text
1. the current top action is clearly low-value or source-depleting;
2. a close-score valid alternative exists;
3. the alternative is safer by production gain, reaction gap, or lower depletion.
```

The production-gap mode is additionally gated by:

```text
turn 45-170
production gap <= -6 or production rank >= 3
current selected action is a low-value attack/capture from an important source
```

When those gates pass, V6 can prefer a close-score alternative that is a safer
regroup/defense, nearer frontier target, better production target, or has a
safer enemy reaction gap.

It does not:

- add new attacks;
- hardcode opponents;
- read local files unless `ORBIT_V6_TRACE_PATH` is explicitly set for local
  debugging;
- use network access;
- change 2P/3P presets;
- change bundled `orbit_lite/` helper code.

## Current Status

```text
local research candidate
not submitted
not promoted
```

