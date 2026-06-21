# Alyce V10 Implementation and Local Eval

Date: 2026-06-21

## Decision

V10 has been built as a local research candidate, but it is **not** a submit candidate.

Retained source:

```text
agents/variants/alyce_v10_v6_role_lock_safe_frontier
```

Parent:

```text
agents/variants/alyce_v6_prod_gap_mode
```

Current official best remains:

```text
alyce_v6_prod_gap_mode
submission_id: 53852919
public score: 1177.8
```

No Kaggle submission was made.

## V5+ Report Coverage

The V10 implementation was checked against the report chain after V5:

| report | required lesson | V10 treatment |
|---|---|---|
| `ALYCE_V5_DETERMINISM_AUDIT_20260619.md` | preserve deterministic loading and traceability | V10 is a copied V6 directory candidate; py_compile and smoke pass |
| `ALYCE_V5_LOCAL_EVAL_20260619.md` | selected-action trace is useful but local screens are not official | V10 adds `ORBIT_V10_TRACE_PATH`; local result is not treated as official |
| `ALYCE_V5_SUBMISSION_RESULT_20260619.md` | V5 improved over earlier attempts but did not become final | V10 does not inherit V5 alone; it starts from V6 |
| `ALYCE_V6_PROD_GAP_TASK_CHAIN_20260619.md` | production-gap mode on V2/V5 trace line | V10 keeps V6 production-gap selected filter |
| `ALYCE_V6_LOCAL_EVAL_20260619.md` | local 4P can be pessimistic, but trace and phase snapshots matter | V10 eval writes trace and uses `run_eval_tournament` phase snapshots |
| `ALYCE_V6_OFFICIAL_REPLAY_REVIEW_20260620.md` | V6 is best but 4P non-first falls behind by step50/100 | V10 targets 4P only and keeps 2P/3P unchanged |
| `ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md` | avoid public-good sacrifices and third-party cleanup | V10 adds public-good veto and source/region lock proxies |
| `ALYCE_V678_2P_CORNER_FORCE_REVIEW_20260620.md` | preserve living force in corner/2P decisions | V10 does not alter 2P preset |
| `V7_PAUSE_AND_MD_COVERAGE_RECHECK_20260620.md` | V7 covered only selected-action subset; full mission/source layer was missing | V10 adds pre-candidate source reserve and candidate hard veto, not just top-action replacement |
| `ALYCE_V8_MD_COVERAGE_TASK_CHAIN_20260620.md` | V8 still missed full third-party cleanup and mission generator | V10 implements a conservative public-good veto, but still not full simulation |
| `ALYCE_V9_OFFICIAL_REPLAY_CODE_DISCUSSION_REVIEW_20260621.md` | V9 increased cleanup risk; broad candidate penalty is dangerous | V10 avoids V9 parent code and was tuned after broad hard-veto overfired |
| `HIGH_RANK_STRATEGY_RESEARCH_AND_V10_TASK_CHAIN_20260621.md` | high-rank evidence favors durable step50 to step100 production | V10 tries to preserve V6 tempo and block public-good launches, but local 4P did not validate improvement |

No V5+ MD conclusion was intentionally skipped. The main uncovered item remains
full counterfactual third-party simulation; this implementation only has a
lightweight proxy.

## Implementation

V10 changes only:

```text
agents/variants/alyce_v10_v6_role_lock_safe_frontier/main.py
agents/variants/alyce_v10_v6_role_lock_safe_frontier/SOURCE.md
agents/variants/alyce_v10_v6_role_lock_safe_frontier/WRAPPER.md
```

Core additions:

1. V10 4P config fields.
2. Source-centric reserve lock in `_apply_4p_source_reserve`.
3. `_apply_v10_role_lock_filter` after V6 FFA candidate adjustments and before V6 selected-action filter.
4. `ORBIT_V10_TRACE_PATH` trace payload.

V10 hard-veto / penalty signals:

```text
multi_enemy_close
unsafe reaction gap
source reserve violation
center/shared-zone sacrifice
low-value nonleader enemy attack while trailing
high-production safe-frontier bonus
```

Kept unchanged:

```text
2P preset
3P preset
V6 production-gap filter
orbit_lite helper package
Kaggle agent(obs) entrypoint
```

## Tuning Attempts

Three V10 variants were tried in-place during this build:

| attempt | change | 4P local result | decision |
|---|---|---|---|
| initial strict role lock | strong source reserve and broad public-good hard veto | V10 1/12 wins, avg rank 2.1667 | too restrictive |
| tuned role lock | lighter reserve; hard veto requires multi-enemy/shared-zone or severe source loss | V10 2/12 wins, avg rank 1.8333 | retained as best local V10 |
| late-gated role lock | preserve first 45 turns, activate near V6 production-gap window | V10 1/12 wins plus one draw, avg rank 2.0833 | worse than tuned |

The final code retains the tuned role lock.

## Verification

Static and smoke:

```text
python -m py_compile agents/variants/alyce_v10_v6_role_lock_safe_frontier/main.py
python scripts/smoke_candidate.py agents/variants/alyce_v10_v6_role_lock_safe_frontier --seed 5 --json
```

Result:

```text
py_compile: pass
smoke: pass
sample actions: valid
env status: ok
errors: 0
```

2P local non-regression screen:

```text
python scripts/run_eval_tournament.py --series v10_2p_vs_v6 --seeds 1-5 --out outputs/v10_eval/2p_vs_v6 pair local/agents/variants/alyce_v10_v6_role_lock_safe_frontier local/agents/variants/alyce_v6_prod_gap_mode --bidirectional
```

Result:

| agent | games | wins | winrate | avg rank | errors |
|---|---:|---:|---:|---:|---:|
| V10 | 10 | 7 | 0.7000 | 1.3000 | 0 |
| V6 | 10 | 3 | 0.3000 | 1.7000 | 0 |

This is not proof V10 is stronger in 2P; V10 should not touch 2P, and small-seed
local variance is high. It only shows no obvious runtime regression.

4P local screens against V6/V8/V9:

| attempt | V10 games | V10 wins | V10 winrate | V10 avg rank | V6 wins | V6 avg rank | errors |
|---|---:|---:|---:|---:|---:|---:|---:|
| initial strict | 12 | 1 | 0.0833 | 2.1667 | 4 | 1.6667 | 0 |
| tuned retained | 12 | 2 | 0.1667 | 1.8333 | 4 | 1.6667 | 0 |
| late-gated | 12 | 1 | 0.0833 | 2.0833 | 2 | 1.8333 | 0 |

The tuned V10 still fails the V10 go/no-go gate:

```text
local 4P avg rank is worse than V6
local 4P win count is worse than V6
```

## Root Cause From Local Trace

The initial strict version overfired:

```text
hard_veto_count and public_good_penalty_count were non-trivial even when close_enemy_count was only 1
```

That misclassified some direct one-enemy attacks as public-good actions. The tuned
version fixed the obvious overbroad condition by requiring multi-enemy/shared-zone
or severe source reserve loss for hard veto.

The remaining issue is structural:

```text
V10 blocks some bad actions, but does not provide a strong replacement mission.
```

When the veto fires, V6's candidate pool may fall back to actions that preserve
ships but do not convert step50 production into step100 durable production. This
matches the high-rank replay lesson: blocking bad moves is insufficient without a
positive holdable frontier/defense plan.

## Go / No-Go

Status:

```text
NO-GO for package
NO-GO for Kaggle submission
```

Reasons:

1. V10 does not beat V6 in the 4P local rotated screen.
2. V10 remains a proxy veto layer, not a full mission generator.
3. The local trace suggests missing positive replacement logic after veto.
4. V6 remains the official best and should not be displaced.

## Next Work

The next useful direction is not another scalar penalty. It should add a positive
replacement mission after a veto:

```text
1. identify holdable frontier source/target pairs;
2. generate a defense/regroup replacement action when public-good veto fires;
3. score replacement by step100 production durability, not just immediate ROI;
4. compare V10 replacement traces against V6 official bad-turn examples;
5. only then rerun 4P local screen and package consideration.
```

Do not submit this V10 candidate without new evidence.
