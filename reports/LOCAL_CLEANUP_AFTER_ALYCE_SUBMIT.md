# Local Cleanup After Alyce Submit

Date: 2026-06-18

## User Direction

After submitting the Alyce Intruder reproduction, remove local obsolete content
that is no longer useful, while keeping GitHub history as the record of the
approach change.

## Removed Local Ignored Content

The following ignored local-only content was removed:

- `drafts/vkhydras_targeted_v1_obsolete/`
- `outputs/targeted_v1/`
- `dist/alyce_intruder_stage/`
- `dist/orbitwars_reworked_submit/`
- `dist/main.py`
- `dist/orbitwars_reworked_d67a11e.tar.gz`
- `dist/orbitwars_reworked_d67a11e_fix1.tar.gz`
- local `__pycache__/` directories under `agents/`, `src/`, `tests/`, and `scripts/`

The submitted Alyce package was kept locally:

```text
dist/alyce_intruder_repro_20260618.tar.gz
```

## Kept Content

The following remained because it is still useful:

- `agents/public/alyce_intruder_repro/`
- `external/kaggle_outputs/` public output cache
- `external/kaggle_notebooks/` public notebook cache
- `reports/` audit and decision records
- `configs/base_agent_v2.yaml`

## GitHub Record

GitHub should record the change in direction through committed reports and
configs, not through local ignored draft folders:

- `reports/PUBLIC_OUTPUT_SOURCE_RECHECK_20260617.md`
- `reports/WORKTREE_CLEANUP_AFTER_SOURCE_RECHECK.md`
- `reports/PUBLIC_OUTPUT_CANDIDATE_REGISTRY.md`
- `reports/CANDIDATE_LOADER_REWORK.md`
- `reports/ALYCE_INTRUDER_DEEP_DIVE_AND_REPRO.md`
- `reports/ALYCE_INTRUDER_SUBMISSION_RESULT.md`
- `configs/base_agent_v2.yaml`

## Current State

The Vkhydras targeted draft is no longer present locally. The main line is now
centered on Alyce Intruder as the submitted public-output reproduction candidate,
with Vkhydras retained only as the current completed official score baseline
until the Alyce submission completes.
