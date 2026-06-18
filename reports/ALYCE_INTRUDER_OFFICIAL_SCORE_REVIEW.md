# Alyce Intruder Official Score Review

Date: 2026-06-18

## Result

```yaml
submission_id: 53793561
candidate: alyce_intruder_repro
source_slug: alycemiki/light-ver-1200-simple-orbit-intruder
status: SubmissionStatus.COMPLETE
public_score: 600.0
package: dist/alyce_intruder_repro_20260618.tar.gz
sha256: E7407E0ECA360114FAB5C84884FCE7D609F470A0DD069A35782B62961F14E43F
```

## Comparison

| Candidate | Submission | Status | Public score |
|---|---:|---|---:|
| Vkhydras Last formatcheck | 53772702 | COMPLETE | 838.1 |
| Vkhydras Last resubmit | 53772607 | COMPLETE | 812.2 |
| Pilkwang fallback | 53767789 | COMPLETE | 678.9 |
| Alyce Intruder reproduction | 53793561 | COMPLETE | 600.0 |

## Decision

Do not promote Alyce Intruder as final.

It is valuable as source material, but this exact public output reproduction
underperformed the current official workspace baseline. The repo should keep the
reproduced code and analysis because the implementation contains useful
mechanics:

- `safe_drain` source-budget protection;
- ETA-aware `capture_floor`;
- enemy reinforcement risk margin;
- moving-target forecast through `orbit_lite`;
- dynamic ROI;
- late-game candidate suppression;
- pressure-based regroup.

## Likely Interpretation

The title's public claim should not be treated as our score. Kaggle public
outputs can depend on notebook context, competition rating dynamics, hidden pool
changes, version mismatch, or simply not reproduce the claimed rating in our
submission context.

The result also means base selection cannot rely on single-source confidence.
The next useful step is to run a fixed-loader screen across the fresh public
output candidates:

- `ranjeet_producer`
- `tamrazov_stronger`
- `alyce_intruder`
- `caoyupeng_gru`
- `shumming_exp50`
- `vkhydras_last`
- `pilkwang_structured`

## Next Action

Use Vkhydras Last `838.1` as the current completed official baseline. Re-run
fresh output 2P/4P screens with `src/orbitwars_agent/candidate_loader.py` before
any further submission.
