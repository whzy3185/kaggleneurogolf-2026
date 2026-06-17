# Candidate Loader Rework

Date: 2026-06-17

## Problem

Fresh Kaggle public outputs are usually directory-style submission packages:

```text
submission_extracted/
  main.py
  orbit_lite/
```

The previous tournament script dynamically loaded `main.py` without registering
the module in `sys.modules` and without temporarily adding the candidate
directory to `sys.path`. Dataclass-heavy agents such as Alyce Miki's public
outputs crashed during local evaluation with:

```text
AttributeError: 'NoneType' object has no attribute '__dict__'
```

That meant multi-file public outputs could be incorrectly evaluated as broken.

## Fix

Added `src/orbitwars_agent/candidate_loader.py` with:

- single-file and directory candidate support;
- clear `main.py` existence errors;
- `sys.modules[module_name]` registration before `exec_module`;
- temporary candidate-directory `sys.path` insertion;
- restoration of global `sys.path` after load;
- clearing bundled package modules such as `orbit_lite` before loading the next
  candidate to reduce cross-candidate leakage.

`scripts/run_eval_tournament.py` now uses this loader. `scripts/smoke_candidate.py`
provides a direct smoke check for either a file or directory candidate.

## Validation

Unit tests cover:

- single-file candidate load;
- directory candidate load with sibling import;
- dataclass candidate load;
- missing `main.py` error;
- no permanent `sys.path` mutation.

## Impact

This is required before any fair 2P/4P screen of Alyce, Ranjeet, Tamrazov
Stronger, Shumming Exp50, GRU, or other public output packages.
