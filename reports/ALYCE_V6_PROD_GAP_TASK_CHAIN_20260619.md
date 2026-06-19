# Alyce V6 Production Gap Task Chain - 2026-06-19

## Starting Point

V5 was submitted by explicit user request, but its local 4P evidence did not
justify promotion. The current practical baseline remains V2:

```text
agents/variants/alyce_4p_ffa_v2
official submission: 53827977
latest CLI score at V5 submission time: 1073.1
```

V6 continues from:

```text
agents/variants/alyce_v5_v2_trace_filter
```

The reason is trace support: V5 already exposes selected-action before/after
labels without changing the bundled planner core.

## Evidence To Preserve

From prior reports:

1. `ALYCE_4P_FFA_V2_OFFICIAL_REPLAY_REVIEW_20260619.md`
   - 4P losses separate by production gap at step 50-100.
   - Losing phases are more enemy-heavy and less regroup/consolidation-heavy.

2. `V3_OFFICIAL_REPLAY_EFFECTIVENESS_REVIEW_20260619.md`
   - Broad static far-low penalties are not enough.
   - Need phase/rank context and selected-action trace.

3. `ALYCE_V5_LOCAL_EVAL_20260619.md`
   - V5 selected-action filter is safe but too low-frequency.
   - Next attempt should be V2 base plus selected trace plus production-gap
     mode switch.

4. `ALYCE_V5_DETERMINISM_AUDIT_20260619.md`
   - Local matches are screen evidence, not exact deterministic proof.
   - Same seed/order may drift, so judge by multiple small views and avoid
     overfitting one replay.

## V6 Design

Create:

```text
agents/variants/alyce_v6_prod_gap_mode
```

Do not modify V2 or V5 in place.

V6 keeps V2/V5:

```text
severe trap neutral hard veto
soft contested neutral penalty
safe neutral bonus
source reserve/depletion penalty
leader asset bonus
low-value rear enemy penalty
selected-action trace
```

V6 adds one mode:

```text
4P production-gap mode
```

Activation gate:

```text
player_count >= 4
turn 45-170
production gap <= -6 or production rank >= 3
```

Bad selected top action:

```text
enemy target:
  target production <= 3
  source production >= 3
  depletion ratio >= 0.78
  enemy reaction gap <= 1

neutral target:
  target production <= 3
  distance >= 50
  enemy reaction gap <= 1
```

Valid alternative:

```text
score within 5.5 of original
not already low/far/source-depleting
improves production, reaction gap, depletion, regroup, or frontier distance
```

This is intentionally still selected-action-only. It does not add new attacks,
does not hardcode opponent names, and does not alter 2P/3P presets.

## Validation Plan

Minimum checks:

```text
python -m py_compile agents/variants/alyce_v6_prod_gap_mode/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v6_prod_gap_mode
```

Local screen:

```text
V6 vs V2, seeds 1-5 bidirectional
V6 vs V1, seeds 1-5 bidirectional
V1/V2/V3/V6 4P with V6 fixed and then rotated through all seats
two V6 trace reruns using ORBIT_V6_TRACE_PATH
```

Go / no-go:

```text
V6 can proceed only if it improves 4P average rank and does not regress badly
against V1/V2.
```

If V6 only helps narrow local cases:

```text
Do not submit.
Use trace results to design V7 with a wider but still protected mode gate.
```
