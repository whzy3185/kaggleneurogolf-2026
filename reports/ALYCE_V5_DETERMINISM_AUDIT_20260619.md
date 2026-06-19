# Alyce V5 Determinism Audit - 2026-06-19

## Purpose

Before trusting another small local screen, we audited whether same-seed local
Orbit Wars matches repeat deterministically.

This was required by:

```text
reports/ALYCE_V4_SIM_CAUSE_ANALYSIS_20260619.md
reports/ALYCE_V5_IMPROVEMENT_TASK_CHAIN_20260619.md
```

## Tool Added

```text
scripts/run_determinism_audit.py
```

The script repeats exactly one local match order with the same seed and writes:

```text
outputs/determinism_audit_*/matches.csv
outputs/determinism_audit_*/summary.json
```

It records whether the winner and score/rank signature are stable.

## Command

```text
python scripts/run_determinism_audit.py \
  --series v2_v1_v3_v4_seed1_repeat3 \
  --seed 1 \
  --repeats 3 \
  --out outputs/determinism_audit_v2_v1_v3_v4_seed1_r3 \
  --progress \
  --agents \
    local/agents/variants/alyce_4p_ffa_v2 \
    local/agents/variants/alyce_4p_ffa_v1 \
    local/agents/variants/alyce_intervention_v3 \
    local/agents/variants/alyce_intervention_v4
```

## Result

Same seed, same four agents, same order, repeated 3 times:

| Repeat | Winner | Status | Turns | Scores |
|---:|---|---|---:|---|
| 1 | draw | draw | 500 | `[1953,1953,1953,1953]` |
| 2 | V1 | ok | 179 | `[0,3283,0,0]` |
| 3 | V3 | ok | 263 | `[0,0,5040,0]` |

Summary:

```text
winner_stable: false
score_signature_stable: false
```

## Interpretation

Local evaluation is useful as a screen, but not as precise single-game replay
evidence.

Consequences:

1. Do not explain strategy from one local seed as if it were deterministic.
2. Prefer aggregate screens and official replay analysis.
3. Treat small local winrate changes as weak evidence.
4. Any candidate must beat the current baseline across a broader local sample
   before packaging or submission.

## Go / No-Go Effect

This audit does not block local experimentation, but it raises the evidence bar:

```text
same-seed local games are not stable enough for exact-turn causal claims.
```

