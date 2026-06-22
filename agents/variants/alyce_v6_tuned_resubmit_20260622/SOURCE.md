# Alyce V6 Tuned Resubmit Source

Source id: `alyce_v6_tuned_resubmit_20260622`

Date: 2026-06-22

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
V6-derived parameter-only resubmission candidate
not promoted unless official score beats the existing V6 best
```

## 2026-06-22 Tuned Delta

This candidate starts from `agents/variants/alyce_v6_prod_gap_mode` and changes
only 4P production-gap selected-action parameters.

Reason:

```text
Both visible V6 submission runs show the same structural pattern: 2P is
acceptable, while 4P non-first games usually fall into a production gap by
step 50-100. The adjustment should therefore stay 4P-only and narrow.
```

Changed 4P preset parameters:

```text
v6_gap_step_start: 45 -> 42
v6_gap_step_end: 170 -> 180
v6_prod_gap_trigger: -6.0 -> -5.0
v6_prod_rank_trigger: unchanged at 3
v6_gap_alt_score_gap: 5.5 -> 5.9
v6_gap_depletion_ratio: 0.78 -> 0.76
v6_gap_safe_reaction_gap: 1.5 -> 1.4
v6_gap_force_bonus: 0.08 -> 0.085
```

Unchanged:

```text
2P preset
3P preset
planner core
orbit_lite helper code
package structure
```

