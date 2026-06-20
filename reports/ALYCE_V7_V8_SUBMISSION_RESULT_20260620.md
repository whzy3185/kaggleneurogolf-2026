# Alyce V7/V8 Submission Result - 2026-06-20

## Scope

User requested pausing local simulation and uploading both V7 and V8 to Kaggle
for official data collection.

Local simulation status at submission time:

```text
python simulation processes: none running
V8 vs V5/V6/V7 requested 12-game local screen: paused before completion
reason: user requested Kaggle upload instead
```

## Local Simulation Caveat

Local `kaggle_environments.make("orbit_wars", configuration={"randomSeed": ...})`
does exercise randomized Orbit Wars maps and environment state for the supplied
seed, including the local environment's map/star/planet/fleet mechanics.

It is not equivalent to official queue evaluation because:

```text
official opponent pool is different
official match scheduling/rating queue is hidden
official random sample is different
official runtime and package execution context may differ
score is a rating over many PvP games, not a single local tournament
```

Therefore local 2P/4P screens are useful only for regression and error checks.
Official Kaggle submissions are needed for real data collection.

## Source Commit

```text
source_commit: 4097566
message: feat: add alyce v7 v8 collection candidates
```

## Packages

| Candidate | Package | Bytes | SHA256 |
|---|---|---:|---|
| V7 | `dist/alyce_v7_continuous_recovery_20260620.tar.gz` | 60088 | `C2C05AD95BCB2F5FF1F08B9936E1FC13BBA611179CFE468F0A7C5A88CA896710` |
| V8 | `dist/alyce_v8_md_coverage_mission_20260620.tar.gz` | 60794 | `D27658FDBDC5A94AC9E939A51D02986E30D6221C7C161C6A4CC7F385C87CEE16` |

Both packages contain only:

```text
main.py
orbit_lite/
```

No `data/`, `external/`, `outputs/`, `replays/`, `kaggle.json`, token, cookie,
zip, or nested previous tarball is included.

## Kaggle Submissions

Latest CLI query after completion:

| Submission ID | File | Message | Status | Public score |
|---:|---|---|---|---:|
| 53874852 | `alyce_v7_continuous_recovery_20260620.tar.gz` | `alyce_v7_continuous_recovery_4097566` | `SubmissionStatus.COMPLETE` | 920.2 |
| 53874866 | `alyce_v8_md_coverage_mission_20260620.tar.gz` | `alyce_v8_md_coverage_mission_4097566` | `SubmissionStatus.COMPLETE` | 1134.8 |

Current completed official best remains:

```text
submission_id: 53852919
agent: alyce_v6_prod_gap_mode
public score snapshot: 1177.8
status: COMPLETE
```

## Replay Follow-up

Visible replays were downloaded after completion:

```text
V7: D:\orbitwars_replays\alyce_v7_latest
V8: D:\orbitwars_replays\alyce_v8_latest
combined V6/V7/V8 review: reports/ALYCE_V678_4P_GAME_THEORY_REPLAY_REVIEW_20260620.md
```

## Decision

Do not promote V7 or V8.

Interpretation:

```text
V7 is rejected.
V8 is below V6 and should be treated as data collection, not a new base.
Keep V6 as official best.
Next code direction should start from V6 and implement a 4P mission router
instead of another selected-action recovery threshold.
```
