# Alyce V9 Submission Result - 2026-06-21

## Scope

User explicitly requested uploading V9 to Kaggle.

This report records the upload and immediate CLI state only. V9 is not promoted
unless the official submission completes above the current best.

## Source

```text
source_commit: de5bd16
source_commit_message: feat: add alyce v9 mission router research
source_path: agents/variants/alyce_v9_4p_mission_router
```

V9 starts from official-best V6 and adds a 4-player mission router. Local review
before upload found V9 useful as a research branch but not clearly stronger than
V6.

## Package

```text
package: dist/alyce_v9_4p_mission_router_20260621.tar.gz
size_bytes: 60706
sha256: B92AE1DBE94523179149FB4F7D65909CE4AD2201118081D8F74A5E1431B93366
```

Archive members:

```text
main.py
orbit_lite/
```

The package was rebuilt after an initial local archive accidentally included
`__pycache__`. The submitted archive excludes `__pycache__` and `*.pyc`.

## Pre-Submit Checks

```text
python -m py_compile agents\variants\alyce_v9_4p_mission_router\main.py
python scripts\smoke_candidate.py agents\variants\alyce_v9_4p_mission_router
python scripts\smoke_candidate.py outputs\v9_package_smoke_20260621
```

Result:

```text
py_compile: pass
source smoke: pass
package-extracted smoke: pass
```

## Kaggle Submission

Command:

```text
kaggle competitions submit -c orbit-wars -f dist\alyce_v9_4p_mission_router_20260621.tar.gz -m "alyce_v9_4p_mission_router_de5bd16"
```

Immediate CLI result:

```text
submission_id: 53904277
file: alyce_v9_4p_mission_router_20260621.tar.gz
message: alyce_v9_4p_mission_router_de5bd16
date_utc: 2026-06-21 06:25:14.323000
status: SubmissionStatus.PENDING
public_score: n/a
```

Later CLI refresh during the V9 replay review:

```text
submission_id: 53904277
status: SubmissionStatus.COMPLETE
public_score: 1077.5
```

Latest visible completed best at upload time:

```text
submission_id: 53852919
agent: alyce_v6_prod_gap_mode
public_score: 1177.8
status: SubmissionStatus.COMPLETE
```

## Decision

Do not promote V9.

V9 completed below the current official best V6 score `1177.8`. Visible replay
analysis is recorded in:

```text
reports/ALYCE_V9_OFFICIAL_REPLAY_CODE_DISCUSSION_REVIEW_20260621.md
```

User also requested a V6 re-upload after the V9 review:

```text
submission_id: 53907214
file: alyce_v6_prod_gap_mode_20260619.tar.gz
message: alyce_v6_prod_gap_mode_resubmit_after_v9_5da551f
status: SubmissionStatus.COMPLETE
public_score: 600.0
```

The completed official best remains the earlier V6 submission `53852919` at
`1177.8`. The V6 re-upload should be treated as a fresh official run for data,
not as a replacement for the prior best snapshot.
