# Alyce V8 MD Coverage Mission Source

Source id: `alyce_v8_md_coverage_mission`

Date: 2026-06-20

## Lineage

This variant is derived from the current official best observed in this repo:

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

Attribution remains attached to Alyce Miki and the referenced Producer/Orbit
Wars utility lineage recorded in the V2/V6 source notes.

## Evidence Basis

V8 is designed from the replay/design coverage matrix in:

```text
reports/ALYCE_REPLAY_MD_COVERAGE_MATRIX_20260620.md
reports/ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md
reports/TXT_BASED_4P_IMPROVEMENT_DESIGN_20260618.md
reports/ALYCE_52_REPLAY_REVIEW_20260618.md
reports/V2_LATEST_REPLAY_AND_V3_SUBMISSION_SYNTHESIS_20260619.md
reports/V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md
reports/ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md
reports/ALYCE_V6_LOCAL_EVAL_20260619.md
```

The common finding is that 4P losses are not caused by simple inactivity. They
come from early/mid production collapse, overcommitted frontier sources,
unholdable or low-impact attacks, and lack of rank/aftermath awareness.

## V8 Delta

V8 keeps V6 behavior and changes only `main.py`.

It preserves:

- V2/V6 4P FFA mission filter;
- V6 selected-action filter;
- V6 production-gap mode;
- no opponent-name hardcoding;
- no network access;
- no external data dependency.

It adds:

- multi-size drain candidates in 4P: `60%`, `80%`, and `100%` of safe drain;
- real production-leader comparison for production gap;
- V8 replay-risk selected-action gate for turn `35-190`;
- top-candidate label trace via `ORBIT_V8_TRACE_PATH`;
- low-impact leader target risk;
- source-depletion, target-production, distance, and reaction-gap risk terms.

The V8 filter only changes the selected top action if:

```text
1. the current top action is risky under replay-derived labels;
2. V8 is in a 4P recovery window;
3. a close-score alternative exists;
4. the alternative improves production, reaction gap, depletion, frontier
   distance, or regroup/defense safety.
```

## What V8 Still Does Not Claim

V8 is not a complete mission planner. It still does not implement:

- full third-party cleanup simulation;
- true arrival-aftermath holdability forecast;
- counterfactual rank-improvement proof;
- explicit contested-neutral multi-source swarm timing.

Those remain next-stage tasks if V8 local evidence is positive.

## Current Status

```text
local research candidate
not submitted
not promoted
```
