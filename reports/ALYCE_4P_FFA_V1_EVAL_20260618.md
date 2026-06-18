# Alyce 4P FFA V1 Evaluation

Date: 2026-06-18

## 1. Scope

Candidate:

```text
agents/variants/alyce_4p_ffa_v1
```

Baseline:

```text
agents/public/alyce_intruder_repro
```

Purpose:

```text
Start local validation for the 4P FFA safety layer.
Do not submit to Kaggle.
Decide whether the current variant is promising enough for packaging.
```

Raw local outputs are under:

```text
outputs/alyce_4p_ffa_v1_eval/
```

They are intentionally not committed.

## 2. Commands

2P non-regression:

```text
python scripts\run_eval_tournament.py \
  --series alyce_4p_ffa_v1_2p_nonregression \
  --seeds 101-110 \
  --out outputs\alyce_4p_ffa_v1_eval\2p_nonregression \
  pair local/agents/variants/alyce_4p_ffa_v1 \
       local/agents/public/alyce_intruder_repro \
  --bidirectional
```

4P V1A position rotation:

```text
seeds: 201-204
games: 16
agents:
  - alyce_4p_ffa_v1
  - alyce_intruder_repro
  - vkhydras_last_heuristic
  - pilkwang_structured
variant position: 0, 1, 2, 3
```

V1.1 smoke:

```text
python -m py_compile agents\variants\alyce_4p_ffa_v1\main.py
python scripts\smoke_candidate.py agents\variants\alyce_4p_ffa_v1 --seed 41 --json
```

4P V1.1 quick rotation:

```text
seeds: 301-302
games: 8
same 4-agent pool
variant position: 0, 1, 2, 3
```

## 3. V1A Results

V1A was the first implemented version with stricter safety gates:

```text
trap_neutral_gap: -1
contested_neutral_gap: 3
source_reserve_frac: 0.12
source_reserve_prod_mult: 1.0
source_pressure_gate: 0.35
```

### 3.1 2P Non-Regression

20 bidirectional games versus original Alyce:

| Agent | Games | Wins | Draws | Errors | Winrate | Avg rank | Avg final ships |
|---|---:|---:|---:|---:|---:|---:|---:|
| `alyce_4p_ffa_v1` | 20 | 6 | 3 | 0 | 0.3000 | 1.5500 | 787.50 |
| `alyce_intruder_repro` | 20 | 11 | 3 | 0 | 0.5500 | 1.3000 | 1006.35 |

Route check:

- `player_count` was checked separately on a Kaggle 2P reset.
- It correctly resolves to `2`, so the 4P FFA layer is not being intentionally
  enabled in 2P.

Interpretation:

- This is not a hard proof of 2P regression because self-play/position effects
  can be noisy.
- It is still a warning: the variant is not clearly non-regressive.
- No packaging or submission should happen off this result.

### 3.2 4P Position Rotation

16 games, variant rotated through all four positions:

| Agent | Games | Wins | Errors | Winrate | Avg rank | Avg final ships | Rank distribution |
|---|---:|---:|---:|---:|---:|---:|---|
| `alyce_4p_ffa_v1` | 16 | 5 | 0 | 0.3125 | 1.6875 | 819.56 | 5 rank-1 / 11 rank-2 |
| `alyce_intruder_repro` | 16 | 10 | 0 | 0.6250 | 1.3750 | 1876.44 | 10 rank-1 / 6 rank-2 |
| `vkhydras_last_heuristic` | 16 | 1 | 0 | 0.0625 | 1.9375 | 95.69 | 1 rank-1 / 15 rank-2 |
| `pilkwang_structured` | 16 | 0 | 0 | 0.0000 | 2.0000 | 0.00 | 16 rank-2 |

Interpretation:

- The variant runs cleanly.
- It does not beat the original Alyce in this pool.
- The average final ships are much lower than the original Alyce.
- This strongly suggests V1A is over-filtering or over-reserving, reducing
  expansion tempo.

## 4. V1.1 Adjustment

After V1A underperformed, I reduced the safety gate strength:

```text
contested_neutral_gap: 3.0 -> 1.0
trap_neutral_gap: -1.0 -> -2.0
contested_min_surplus: 3.0 -> 1.0
contested_pressure_mult: 0.03 -> 0.01
source_reserve_frac: 0.12 -> 0.05
source_reserve_prod_mult: 1.0 -> 0.5
source_reserve_pressure_mult: 0.04 -> 0.02
source_pressure_gate: 0.35 -> 0.75
```

Intent:

```text
Keep the FFA safety concepts but stop suppressing normal expansion so heavily.
```

V1.1 smoke:

```text
py_compile: pass
smoke_candidate: pass
env_status: ok
```

## 5. V1.1 Quick 4P Results

8 games, same pool, all positions covered:

| Agent | Games | Wins | Errors | Winrate | Avg rank | Avg final ships | Rank distribution |
|---|---:|---:|---:|---:|---:|---:|---|
| `alyce_4p_ffa_v1` | 8 | 3 | 0 | 0.3750 | 1.6250 | 771.12 | 3 rank-1 / 5 rank-2 |
| `alyce_intruder_repro` | 8 | 5 | 0 | 0.6250 | 1.3750 | 1484.12 | 5 rank-1 / 3 rank-2 |
| `vkhydras_last_heuristic` | 8 | 0 | 0 | 0.0000 | 2.0000 | 0.00 | 8 rank-2 |
| `pilkwang_structured` | 8 | 0 | 0 | 0.0000 | 2.0000 | 0.00 | 8 rank-2 |

Position sensitivity for variant:

| Variant position | Games | Wins |
|---:|---:|---:|
| 0 | 2 | 1 |
| 1 | 2 | 2 |
| 2 | 2 | 0 |
| 3 | 2 | 0 |

Interpretation:

- V1.1 is slightly less bad than V1A in winrate but still behind original Alyce.
- It still has collapse-like games with zero final ships in some positions.
- The change does not yet solve Alyce's 4P weakness.

## 6. Decision

Current status:

```text
not submit-ready
not package-ready
do not upload to Kaggle
```

Reason:

```text
The variant has no runtime errors, but it does not outperform the original Alyce
baseline in the local samples. It also fails the spirit of 2P non-regression.
```

The reports were directionally correct: 4P needs a FFA layer. The implementation
is not yet good enough because the filters are still acting without visibility
into how often each rule fires.

## 7. Next Required Step

Before more tuning, add local mission counters:

```text
trap_neutral_reject_count
contested_neutral_reject_count
safe_neutral_bonus_count
source_depletion_penalty_count
leader_asset_bonus_count
enemy_rear_penalty_count
threat_neighbor_bonus_count
```

Then run the same 4P pool and answer:

```text
Which rule is actually responsible for lower final ships?
Is source reserve suppressing early expansion?
Are contested neutral gates rejecting good openings?
Is leader bonus ever triggering?
Are rear/threat labels affecting meaningful candidates?
```

Do not add more strategic features until that trace exists.

## 8. Submission Status

```text
submitted: false
official score: none
package generated: false
recommend submission: no
```
