# Alyce V6 All Submissions and Tuned Resubmit - 2026-06-22

## Scope

User requested:

```text
try a small V6 parameter adjustment
submit V6 again
combine all V6 submission game records
```

This report covers:

1. existing V6 official submissions;
2. newly downloaded V6 resubmission replays;
3. combined V6 replay analysis;
4. the small V6-tuned parameter candidate submitted on 2026-06-22.

No local tournament result is treated as an official score.

## Current Official Submission State

Latest Kaggle CLI snapshot used in this report:

| submission | package | message | status | public score |
|---:|---|---|---|---:|
| `53852919` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | `alyce_v6_prod_gap_mode_1db7614` | COMPLETE | `1177.8` |
| `53907214` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | `alyce_v6_prod_gap_mode_resubmit_after_v9_5da551f` | COMPLETE | `1110.4` |
| `53939587` | `alyce_v6_tuned_resubmit_20260622.tar.gz` | `alyce_v6_tuned_resubmit_20260622` | PENDING | n/a |

The existing official best remains submission `53852919` at `1177.8` until a
new completed submission beats it.

## Replay Data

Original V6 replay root:

```text
D:\orbitwars_replays\alyce_v6_latest
```

V6 resubmit replay root:

```text
D:\orbitwars_replays\alyce_v6_resubmit_53907214
```

Combined analysis output:

```text
D:\orbitwars_replays\alyce_v6_combined_53852919_53907214\analysis
```

Generated files:

```text
game_theory_episode_summary.csv
game_theory_phase_snapshots.csv
game_theory_action_events.csv
game_theory_summary.json
```

Replay coverage:

| variant | public episodes | 2P public | 4P public | validation |
|---|---:|---:|---:|---:|
| `v6_original` | 72 | 38 | 34 | 1 |
| `v6_resubmit` | 73 | 42 | 31 | 1 |
| combined | 145 | 80 | 65 | 2 |

Important limitation: official replay JSON exposes observations and submitted
actions, not V6 internal scores or trace state. Target labels and risk features
are inferred from source planet, launch angle, ownership, distance, and later
visible actions.

## V6 Replay Synthesis

Both V6 runs show the same structural shape:

1. 2P remains acceptable and should not be disturbed by this tuning pass.
2. 4P first-place games usually keep production close to the leader by step 50.
3. 4P non-first games are usually already behind by step 50 and collapse by
   step 100.
4. The recurrent failure mode is not runtime or package format; it is 4P
   production conversion after early/mid contested commitments.

### 4P Phase Split

| variant | group | step50 prod | step50 gap | step50 rank | step100 prod | step100 gap | step100 rank |
|---|---|---:|---:|---:|---:|---:|---:|
| `v6_original` | first | 13.9091 | -0.2727 | 1.0909 | 26.4545 | 0.0000 | 1.0000 |
| `v6_original` | non-first | 9.3478 | -6.8696 | 2.7826 | 7.2174 | -19.3913 | 2.8696 |
| `v6_resubmit` | first | 13.2222 | -1.3333 | 1.5556 | 24.7778 | -0.6667 | 1.2222 |
| `v6_resubmit` | non-first | 10.5909 | -4.9545 | 2.4091 | 7.5000 | -20.6818 | 2.9091 |

The common signal is the step 50 to step 100 cliff in 4P non-first games. The
second V6 run was not identical in opponent pool, but it reproduces the same
failure mechanism.

### Action Mix

| variant | phase | enemy rate | neutral rate | mine/regroup rate | cleanup risk | avg commit | avg distance |
|---|---|---:|---:|---:|---:|---:|---:|
| `v6_original` | opening 0-50 | 0.2497 | 0.5089 | 0.2413 | 0.1406 | 0.7451 | 43.2484 |
| `v6_original` | mid 50-150 | 0.3344 | 0.1905 | 0.4750 | 0.0975 | 0.7666 | 38.0992 |
| `v6_resubmit` | opening 0-50 | 0.2955 | 0.4559 | 0.2486 | 0.1691 | 0.7401 | 44.4578 |
| `v6_resubmit` | mid 50-150 | 0.3618 | 0.1621 | 0.4761 | 0.0780 | 0.7734 | 39.2319 |

Read: V6 wins are not won by avoiding all attacks. The issue is the timing and
state of those attacks: when V6 is already losing the production race in 4P, it
still spends high local fractions into enemy/frontier situations often enough to
lock in the collapse.

## Tuned Candidate

Candidate path:

```text
agents/variants/alyce_v6_tuned_resubmit_20260622
```

Package:

```text
dist/alyce_v6_tuned_resubmit_20260622.tar.gz
```

Package metadata:

```text
size_bytes: 59726
sha256: E19311170CE12FC338696F73891A7F8788B4C4D838733E565CF71E4F8D182DF9
members:
  main.py
  orbit_lite/
```

Submitted:

```text
submission_id: 53939587
message: alyce_v6_tuned_resubmit_20260622
status_at_submit_check: SubmissionStatus.PENDING
```

## Parameter Delta

This is intentionally a small 4P-only parameter adjustment. It does not change
2P, 3P, planner core, bundled helper code, or package structure.

Changed 4P preset parameters:

| parameter | V6 | V6 tuned |
|---|---:|---:|
| `v6_gap_step_start` | 45 | 42 |
| `v6_gap_step_end` | 170 | 180 |
| `v6_prod_gap_trigger` | -6.0 | -5.0 |
| `v6_prod_rank_trigger` | 3 | 3 |
| `v6_gap_alt_score_gap` | 5.5 | 5.9 |
| `v6_gap_depletion_ratio` | 0.78 | 0.76 |
| `v6_gap_safe_reaction_gap` | 1.5 | 1.4 |
| `v6_gap_force_bonus` | 0.08 | 0.085 |

Rationale:

```text
Move V6 production-gap replacement slightly earlier and make its safe
alternative acceptance slightly wider, but avoid the V10/V7/V8 mistake of adding
new broad mission logic or suppressing V6's base tempo.
```

An earlier, more aggressive trial with `prod_rank_trigger=2` was rejected before
submission after a short 4P sanity check showed obvious risk. The submitted
candidate uses the narrower values above.

## Verification

Commands run before submission:

```text
python -m py_compile agents\variants\alyce_v6_tuned_resubmit_20260622\main.py
python scripts\smoke_candidate.py agents\variants\alyce_v6_tuned_resubmit_20260622 --seed 23 --json
tar --exclude='__pycache__' --exclude='*.pyc' -czf dist\alyce_v6_tuned_resubmit_20260622.tar.gz -C agents\variants\alyce_v6_tuned_resubmit_20260622 main.py orbit_lite
python scripts\smoke_candidate.py outputs\package_smoke\alyce_v6_tuned_resubmit_20260622 --seed 24 --json
```

Results:

```text
py_compile: pass
source smoke: pass
package smoke: pass
submission upload: success
initial Kaggle status: PENDING
```

## Decision State

Current official best:

```text
V6 original submission 53852919 at 1177.8
```

V6 tuned submission:

```text
pending; no score yet
```

Next action after completion:

1. query `kaggle competitions submissions -c orbit-wars`;
2. if `53939587` completes, record its public score;
3. download only its latest visible episodes;
4. compare its 4P non-first step50/step100 production gap against both V6 runs;
5. promote only if it beats `1177.8` or shows a clear replay-level improvement
   without 2P collapse.

