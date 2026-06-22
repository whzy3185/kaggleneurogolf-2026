# Alyce V6 Batch Resubmissions - 2026-06-22

## Request

User requested:

```text
submit the updated V6
then submit the V6 original body three more times
```

## Pre-Submit State

Latest Kaggle CLI check before the batch showed:

| submission | package | status | public score |
|---:|---|---|---:|
| `53939587` | `alyce_v6_tuned_resubmit_20260622.tar.gz` | COMPLETE | `975.4` |
| `53907214` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | COMPLETE | `1110.4` |
| `53852919` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | COMPLETE | `1177.8` |

Interpretation:

```text
The first tuned V6 submission underperformed. The original V6 submission
53852919 remains the official best observed in this repository.
```

## Submitted Batch

Executed command family:

```text
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_tuned_resubmit_20260622.tar.gz -m "alyce_v6_tuned_resubmit_batch_20260622_181147_1of1"
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_prod_gap_mode_20260619.tar.gz -m "alyce_v6_original_batch_20260622_181147_1of3"
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_prod_gap_mode_20260619.tar.gz -m "alyce_v6_original_batch_20260622_181147_2of3"
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_prod_gap_mode_20260619.tar.gz -m "alyce_v6_original_batch_20260622_181147_3of3"
```

Kaggle accepted all four uploads.

## Submission IDs

| submission | package | message | status at immediate check | public score |
|---:|---|---|---|---:|
| `53942314` | `alyce_v6_tuned_resubmit_20260622.tar.gz` | `alyce_v6_tuned_resubmit_batch_20260622_181147_1of1` | PENDING | n/a |
| `53942315` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | `alyce_v6_original_batch_20260622_181147_1of3` | PENDING | n/a |
| `53942318` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | `alyce_v6_original_batch_20260622_181147_2of3` | PENDING | n/a |
| `53942319` | `alyce_v6_prod_gap_mode_20260619.tar.gz` | `alyce_v6_original_batch_20260622_181147_3of3` | PENDING | n/a |

## Package Hashes

```text
updated V6 tuned:
  path: dist\alyce_v6_tuned_resubmit_20260622.tar.gz
  sha256: E19311170CE12FC338696F73891A7F8788B4C4D838733E565CF71E4F8D182DF9

original V6:
  path: dist\alyce_v6_prod_gap_mode_20260619.tar.gz
  sha256: 8F64DE7C6FA6817C568F70547DCEB5FAF6A2933AD56D1CC54B9372AB333B126F
```

## Follow-Up

Do not infer quality from the pending rows. Next check should query:

```text
kaggle competitions submissions -c orbit-wars
```

If any of the three original V6 reuploads beats `1177.8`, update
`reports/SCORECARD.md` and treat that submission as the current official best.
If the updated tuned V6 remains below the original V6 line, keep it rejected.

