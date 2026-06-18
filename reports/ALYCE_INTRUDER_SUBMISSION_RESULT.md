# Alyce Intruder Submission Result

Date: 2026-06-18

## Submission

```yaml
competition: orbit-wars
candidate: alyce_intruder_repro
source_slug: alycemiki/light-ver-1200-simple-orbit-intruder
package: dist/alyce_intruder_repro_20260618.tar.gz
package_type: multi_file_submission
sha256: E7407E0ECA360114FAB5C84884FCE7D609F470A0DD069A35782B62961F14E43F
package_bytes: 54548
submission_id: 53793561
message: alyce_intruder_repro_20260618
submitted_at_utc: 2026-06-18 02:42:29.803000
latest_status: SubmissionStatus.COMPLETE
public_score: 600.0
private_score: null
```

## Verification Before Submit

```yaml
exact_copy_check:
  checked_files: 14
  differences: 0
py_compile: pass
smoke_candidate_source:
  passed: true
  env_status: ok
  seed: 1
package_members:
  - main.py
  - orbit_lite/
package_smoke:
  passed: true
  env_status: ok
  seed: 2
```

The submitted archive contains `main.py` and `orbit_lite/` at archive root. It
does not include `external/`, `outputs/`, `data/`, `replays/`, previous tarballs,
or secrets.

## Latest CLI Snapshot

```text
53793561  alyce_intruder_repro_20260618.tar.gz  2026-06-18 02:42:29.803000  alyce_intruder_repro_20260618  SubmissionStatus.COMPLETE  600.0
53772702  main.py                               2026-06-17 10:33:52.853000  vkhydras_last_single_file_candidate_d7d937e_formatcheck  SubmissionStatus.COMPLETE  838.1
53772607  main.py                               2026-06-17 10:30:06.617000  vkhydras_last_single_file_candidate_d7d937e_resubmit1    SubmissionStatus.COMPLETE  812.2
```

## Current Interpretation

Alyce Intruder completed with public score `600.0`. It underperformed both the
current completed official best Vkhydras Last formatcheck submission `53772702`
with public score `838.1`, and the previous Pilkwang fallback at `678.9`.

Do not promote Alyce Intruder as final. Keep it as a reproduced public-output
reference for its implementation ideas: safe drain, ETA-aware capture floor,
dynamic ROI, late-game suppression, and `orbit_lite` movement forecasting.
