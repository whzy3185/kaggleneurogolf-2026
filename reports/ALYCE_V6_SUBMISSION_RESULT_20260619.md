# Alyce V6 Submission Result - 2026-06-19

## Submission

Kaggle submission was explicitly requested by the user for the V6 candidate.

```text
competition: orbit-wars
submission_id: 53852919
message: alyce_v6_prod_gap_mode_1db7614
file: alyce_v6_prod_gap_mode_20260619.tar.gz
status_latest_cli: SubmissionStatus.PENDING
public_score_latest_cli: n/a
private_score_latest_cli: n/a
```

Exact command executed:

```bash
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_prod_gap_mode_20260619.tar.gz -m "alyce_v6_prod_gap_mode_1db7614"
```

## Package

```text
source: agents/variants/alyce_v6_prod_gap_mode
package: dist/alyce_v6_prod_gap_mode_20260619.tar.gz
size_bytes: 59857
sha256: 8F64DE7C6FA6817C568F70547DCEB5FAF6A2933AD56D1CC54B9372AB333B126F
member_count: 14
root_main_py: yes
root_orbit_lite_package: yes
```

Package members:

```text
main.py
orbit_lite/__init__.py
orbit_lite/adapter.py
orbit_lite/aiming.py
orbit_lite/constants.py
orbit_lite/distance_cache.py
orbit_lite/garrison_launch.py
orbit_lite/geometry.py
orbit_lite/intercept_aim.py
orbit_lite/movement.py
orbit_lite/movement_aiming.py
orbit_lite/movement_step.py
orbit_lite/obs.py
orbit_lite/planner_core.py
```

Pre-submit checks:

```text
py_compile source main.py: pass
package extracted main.py exists: yes
package extracted orbit_lite exists: yes
package extracted smoke: pass
blocked package members: none
secret/network keyword scan: no matches for kaggle.json/token/password/cookie/requests/urllib/socket
```

## Latest Submission Snapshot

CLI query immediately after submission:

```text
53852919  alyce_v6_prod_gap_mode_20260619.tar.gz    2026-06-19 15:04:36.520000  alyce_v6_prod_gap_mode_1db7614                    SubmissionStatus.PENDING
53851968  alyce_v5_v2_trace_filter_20260619.tar.gz  2026-06-19 14:30:43.467000  alyce_v5_v2_trace_filter_fd3c2b7                  SubmissionStatus.COMPLETE  756.7
53842450  alyce_intervention_v3_20260619.tar.gz     2026-06-19 08:49:46.003000  alyce_intervention_v3_soft_far_low_penalty_b1542f4 SubmissionStatus.COMPLETE 1021.7
53827977  alyce_4p_ffa_v2_20260619.tar.gz           2026-06-19 03:21:33.053000  alyce_4p_ffa_v2_soft_contested_filter_20260619     SubmissionStatus.COMPLETE 1073.1
53793561  alyce_intruder_repro_20260618.tar.gz      2026-06-18 02:42:29.803000  alyce_intruder_repro_20260618                      SubmissionStatus.COMPLETE 1069.1
```

## Interpretation

V6 is now in the official queue. No official score exists yet.

Local evidence before submission:

```text
py_compile: pass
smoke: pass
V6 vs V2 1v1 small screen: 5-3-2
V6 vs V1 1v1 small screen: 3-4-3
4P fixed-seat screen: promising
4P rotated-seat screen: unstable and not promotion-worthy
trace: production-gap mode changed one selected action in two traced games
```

The package was submitted because the user explicitly requested a V6 upload, not
because local 4P gates justified promotion.

## Current Candidate Ranking

At this snapshot:

```text
current best remains V2 submission 53827977 at 1073.1
Alyce repro 53793561 remains close at 1069.1
V3 remains below both at 1021.7
V5 is rejected at 756.7
V6 is pending
```

## Next Check

Poll status without resubmitting:

```bash
kaggle competitions submissions -c orbit-wars
```

If `53852919` completes, update:

```text
reports/SCORECARD.md
reports/ALYCE_V6_SUBMISSION_RESULT_20260619.md
```
