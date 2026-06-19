# Alyce V5 Submission Result - 2026-06-19

## Submission

Kaggle submission was explicitly requested by the user for the V5 candidate.

```text
competition: orbit-wars
submission_id: 53851968
message: alyce_v5_v2_trace_filter_fd3c2b7
file: alyce_v5_v2_trace_filter_20260619.tar.gz
status_latest_cli: SubmissionStatus.COMPLETE
public_score_latest_cli: 756.7
private_score_latest_cli: n/a
```

Exact command executed:

```bash
kaggle competitions submit -c orbit-wars -f dist\alyce_v5_v2_trace_filter_20260619.tar.gz -m "alyce_v5_v2_trace_filter_fd3c2b7"
```

## Package

```text
source: agents/variants/alyce_v5_v2_trace_filter
package: dist/alyce_v5_v2_trace_filter_20260619.tar.gz
size_bytes: 59162
sha256: 2C8553B6E537DF5D24628EC8FABD5B8F730253EDE65077FE6451E97F7E785E94
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
source candidate smoke: pass
package extracted main.py exists: yes
package extracted orbit_lite exists: yes
package extracted smoke: pass
blocked package members: none
secret/network keyword scan: no matches for kaggle.json/token/password/cookie/requests/urllib/socket
```

## Latest Submission Snapshot

CLI query immediately after submission:

```text
53851968  alyce_v5_v2_trace_filter_20260619.tar.gz  2026-06-19 14:30:43.467000  alyce_v5_v2_trace_filter_fd3c2b7  SubmissionStatus.PENDING
53842450  alyce_intervention_v3_20260619.tar.gz     2026-06-19 08:49:46.003000  alyce_intervention_v3_soft_far_low_penalty_b1542f4  SubmissionStatus.COMPLETE  1013.4
53827977  alyce_4p_ffa_v2_20260619.tar.gz           2026-06-19 03:21:33.053000  alyce_4p_ffa_v2_soft_contested_filter_20260619      SubmissionStatus.COMPLETE  1073.1
53793561  alyce_intruder_repro_20260618.tar.gz      2026-06-18 02:42:29.803000  alyce_intruder_repro_20260618                       SubmissionStatus.COMPLETE  1069.1
```

## Interpretation

V5 completed at `756.7`. This is a clear rejection result: it is far below V2,
V3, and the Alyce reproduction.

Local V5 evidence before submission was mixed:

```text
1v1 V5 vs V2: 5-1 in the small local screen
1v1 V5 vs V1: 2-3-1 in the small local screen
4P V1/V2/V3/V5 family screen: V2 6/12 wins, V5 2/12 wins
determinism audit: repeated same seed/order was not stable
```

The package was submitted because the user explicitly requested a V5 upload, not
because the local 4P gate justified promotion.

## Status Update

Latest CLI query after the V6 upload:

```text
53851968  alyce_v5_v2_trace_filter_20260619.tar.gz  SubmissionStatus.COMPLETE  756.7
```

Do not continue V5 as a candidate. The local 4P warning was predictive enough:
V5's low-frequency selected-action changes did not generalize on the official
ladder.

## Next Check

Poll V6 status without resubmitting:

```bash
kaggle competitions submissions -c orbit-wars
```
