# Alyce Intervention V4 Implementation - 2026-06-19

## Summary

Implemented a local V4 candidate:

```text
agents/variants/alyce_intervention_v4/
```

V4 is not submitted and is not promoted.

Current official best remains:

```text
submission_id: 53827977
agent: alyce_4p_ffa_v2
latest visible public score: 1087.7
```

## Source

V4 is copied from:

```text
agents/variants/alyce_intervention_v3/
```

The upstream public source remains:

```text
external/kaggle_outputs/alycemiki__intervention-command-w-ffa/submission_extracted
```

## Implemented V4 Changes

Changed only:

```text
agents/variants/alyce_intervention_v4/main.py
agents/variants/alyce_intervention_v4/SOURCE.md
agents/variants/alyce_intervention_v4/WRAPPER.md
```

The `orbit_lite/` engine files were copied unchanged.

### 1. V4 4P Context Scorer

V3's `_apply_ffa_v3_safety_penalty(...)` was replaced with:

```text
_apply_ffa_v4_context_score(...)
```

It is enabled only for 4-player games:

```text
enable_ffa_v4_safety=True in CONFIG_4P
```

It adds soft score changes for:

- far low-value non-leader enemy targets;
- far low-value neutral targets;
- trap neutrals by rough reaction-distance and post-capture margin;
- safe high-production neutrals;
- high-production source depletion under pressure;
- trailing early/mid low-value attacks;
- low-value leader-owned targets that are not holdable.

It does not:

- delete actions;
- disable full-drain or multi-size candidate tiers;
- alter 2P config;
- change movement, intercept, garrison, comet, or adapter code;
- hardcode opponent names.

### 2. Leader Exception Fix

V3 exempted current leader-owned low-value enemy targets from the far-low enemy
penalty. V4 narrows that:

```text
leader-owned low-value targets can still be penalized when holdability is weak,
reaction is bad, or source protection is violated.
```

This directly responds to V3 replay example `80649187`.

### 3. Trace Output

Added local-only trace support:

```text
ORBIT_V4_TRACE_PATH=outputs/alyce_intervention_v4_trace_smoke/trace.jsonl
```

When the environment variable is unset, V4 writes nothing.

Trace fields:

```text
step
player_count
prod_rank
prod_gap
leader
top_changed
trap_neutral
safe_neutral_bonus
far_low_nonleader_enemy
leader_low_value_weak
source_protect
trailing_bad_attack
```

## Verification

### Syntax

Command:

```text
python -m py_compile agents/variants/alyce_intervention_v4/main.py
```

Result:

```text
pass
```

### Candidate Smoke

Command:

```text
python scripts/smoke_candidate.py agents/variants/alyce_intervention_v4
```

Result:

```text
passed: true
env_status: ok
sample_actions_ok: true
turns: 74
seed: 1
```

The OpenSpiel warnings are environment noise also seen in prior runs; they did
not affect Orbit Wars smoke.

### 2P Micro-Screen

Command:

```text
python scripts/run_eval_tournament.py \
  --series alyce_intervention_v4_2p_smoke \
  --seeds 1-2 \
  --out outputs/alyce_intervention_v4_2p_smoke \
  --progress \
  pair local/agents/variants/alyce_intervention_v4 \
       local/external/kaggle_outputs/alycemiki__intervention-command-w-ffa/submission_extracted \
  --bidirectional
```

Result:

```text
games: 4
V4 wins: 4
original Intervention wins: 0
errors: 0
```

Interpretation:

```text
This is only a micro-screen. It shows no immediate 2P breakage, not a reliable
strength claim.
```

### 4P Smoke

Initial 4P smoke:

```text
series: alyce_intervention_v4_4p_smoke
seed: 1
agents: V4, V3, original Intervention, V2
winner: V3
V4 rank: 2
errors: 0
```

Trace-enabled tuned 4P smoke:

```text
series: alyce_intervention_v4_4p_trace_smoke_tuned
seed: 3
agents: V4, V3, original Intervention, V2
winner: V2
V4 rank: 2
errors: 0
```

Interpretation:

```text
V4 4P branch runs, but current small samples do not show superiority.
Do not package or submit.
```

## Trace Findings

Before narrowing source protection, trace smoke showed:

```text
rows: 499
top_changed: 270
source_protect: 4155
trap_neutral: 531
safe_neutral_bonus: 649
```

This was too invasive and violated the replay lesson that broad source reserve
can kill winning tempo.

After tuning:

```text
rows: 165
top_changed: 4
source_protect: 32
trap_neutral: 163
safe_neutral_bonus: 52
far_low_nonleader_enemy: 0
leader_low_value_weak: 0
trailing_bad_attack: 0
```

Current interpretation:

- Trace now works.
- Source protection is no longer dominating the policy.
- The tested seed did not exercise far-low enemy or leader-low-value labels.
- V4 still needs replay-inspired cases to test the labels it was designed for.

## Coverage Against Prior Reports

| Required item | Status in V4 |
|---|---|
| Candidate-change trace | Implemented local-only jsonl trace. |
| 2P/4P separation | Implemented: V4 scorer gated to 4P. |
| Rank/phase policy | Implemented first pass using production rank/gap and step 45-170. |
| Reaction/holdability | Implemented rough reaction-distance and post-capture margin. |
| Trap neutral | Implemented as soft penalty. |
| Safe neutral | Implemented as soft bonus. |
| Leader target nuance | Implemented weak-hold leader low-value penalty. |
| Anti-kingmaker | Partially implemented through non-leader low-value penalties. |
| Source protection | Implemented but tuned down after trace. |
| Attack-vs-regroup | Implemented indirectly by penalizing bad attacks and leaving ships for regroup. |
| Full mission labels | Partial; enough for trace, not a full planner rewrite. |
| Packaging/submission | Not done; not justified yet. |

## Current Decision

```text
V4 is a valid local candidate implementation.
V4 is not a proven improvement.
Do not submit V4.
Continue with targeted replay-inspired validation and label-specific tuning.
```

## Next Required Work

1. Run a replay-inspired 4P suite targeting V3 loss patterns:
   - `80649187`
   - `80641852`
   - `80643617`
   - V2 losses with step100 production collapse.

2. Expand 4P screen with position rotation:
   - V4
   - V2 official best
   - V3
   - original Intervention
   - Alyce repro

3. Inspect trace:
   - `top_changed` rate;
   - label counts by phase;
   - whether changed turns correlate with better step50/100 production.

4. Tune only after trace evidence:
   - if top_changed too low, policy is inert;
   - if source_protect too high, narrow again;
   - if trap_neutral dominates but V4 still loses, add holdability rather than
     stronger trap penalty;
   - if leader_low_value never triggers, construct a targeted local case before
     claiming that leader nuance is solved.

5. Package only after local 4P average rank improves.
