# Alyce V7 Continuous Recovery Source

Source id: `alyce_v7_continuous_recovery`

Date: 2026-06-20

## Lineage

This variant is derived from the current repo official best:

```text
agents/variants/alyce_v6_prod_gap_mode
```

The upstream public lineage remains:

```text
Kaggle code: alycemiki/light-ver-1200-simple-orbit-intruder
Author: Alyce Miki
URL: https://www.kaggle.com/code/alycemiki/light-ver-1200-simple-orbit-intruder
```

Attribution remains attached to Alyce Miki and the referenced Producer/Orbit
Wars utility lineage recorded in the V2 source notes.

## Why V7 Exists

Previous reports rejected the V3/V4 direction and the V6 official replay review
identified the remaining gap:

```text
reports/ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md
reports/ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md
```

The key lesson is that successful variants must keep the V2/V6 tempo and only
intervene at the selected-action level. V7 starts from V6 and tries to widen the
production recovery gate without adding new attacks.

## V7 Delta

V7 changes only `main.py`.

It keeps V2's 4P behavior:

- severe trap neutral hard veto;
- soft contested neutral penalty;
- safe neutral bonus;
- source reserve and source depletion penalty;
- leader asset bonus;
- low-value rear enemy penalty.

It adds:

- selected-action trace via `ORBIT_V7_TRACE_PATH`;
- a narrow 4P-only selected top-candidate replacement filter;
- V6 production-gap mode, corrected to compare against the real production
  leader rather than the strength leader;
- a continuous 4P recovery risk score.

The filter only acts when:

```text
1. the current top action is clearly low-value or source-depleting;
2. a close-score valid alternative exists;
3. the alternative is safer by production gain, reaction gap, or lower depletion.
```

The V7 continuous recovery mode is gated by:

```text
turn 35-190
production gap <= -3 or production rank >= 2
selected top action has enough accumulated risk:
  source depletion / important source
  low target production
  bad reaction gap
  distance from frontier
  low-impact leader target
```

When those gates pass, V7 can prefer a close-score alternative that is a safer
regroup/defense, nearer frontier target, better production target, or has a
safer enemy reaction gap.

It does not:

- add new attacks;
- hardcode opponents;
- read local files unless `ORBIT_V7_TRACE_PATH` is explicitly set for local
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

