# Score and Failure Retrospective

The Kaggle CLI returned 200 submission records after competition close. Public and private scores are identical in the captured final state. This file highlights submissions that changed engineering decisions; `data/kaggle_submissions.json` contains the full list.

## Calibrated Positive Stacks

| Ref | Description | Score | Evidence |
| ---: | --- | ---: | --- |
| 54604279 | Eight-task C local stack | 7276.61 | Predicted aggregate gain about +3.1086; observed about +3.11. |
| 54608730 | Parent-aware C22 overlay | 7278.75 | Predicted +0.9191; observed +0.92. |
| 54634057 | Fifth cumulative C batch | 7297.02 | Five-batch predicted +0.9837; observed +0.98. |
| 54716955 | Isolated task187 | 7408.86 | Proved task187 positive after a two-task hidden regression. |
| 54720080 | Exact cleanup plus task267 | 7409.23 | Small exact transforms stacked cleanly. |
| 54723486 | task110 CP65 plus task243 selector | 7410.01 | Large exact factorization plus selector fusion. |
| 54725120 | Exact factors without task055 | 7410.40 | Removing hidden-unsafe task055 restored the expected direction. |
| 54729003 | task002/task224/task249 terminal factors | 7410.55 | Exact terminal reductions. |
| 54729703 | task108/task217/task275 contractions | 7410.67 | Latest verified parent used by the personal closeout. |
| 54733776 | Audited GitHub integration | 7419.90 | Broader team-safe integration excluded locally unsafe changes. |
| 54736568 | Final all-400 integration | 7420.93 | Final complete team score. |

## Failure 1: Platform-Incompatible Models

Several local models passed ONNX checker or local Runtime but failed Kaggle processing. The main classes were:

- `uint8 TopK` in task233/task366.
- negative padding produced by Conv/QLinearConv support cropping.
- operator/dtype combinations accepted by model checking but unsupported by the competition runtime.
- malformed task173/task233/task366 variants in an early rebuilt package.

Decision lesson: checker validity, local ORT execution, and competition runtime compatibility are separate gates. A runtime capability matrix and a forbidden-op audit must exist before candidate promotion.

## Failure 2: task251 Hidden-Distribution Regression

| Ref | Package | Score |
| ---: | --- | ---: |
| 54715535 | Parent | 7407.70 |
| 54716159 | task187 + task251 | 7391.08 |
| 54716955 | task187 isolated | 7408.86 |

The isolated task187 submission proved positive, so task251 caused the large hidden regression. Public examples and local cost were insufficient to establish the rule over hidden inputs.

What worked: immediate task isolation and permanent blocking of the task251 candidate family.

What should have happened earlier: every semantic rewrite without a generator proof should have been isolated before entering a cumulative stack.

## Failure 3: task055 Hidden Failure

| Ref | Package | Score |
| ---: | --- | ---: |
| 54723486 | Parent | 7410.01 |
| 54724494 | Add task055 plus exact factors | 7392.80 |
| 54725120 | Same exact factors, remove task055 | 7410.40 |

This is a clean A/B attribution. Removing task055 recovered the parent and preserved the exact-factor gains. The response was correct, but the submission could have been avoided with a generator-backed proof or an isolated task055 probe.

## Failure 4: v137 task075/task383

| Ref | Package | Score |
| ---: | --- | ---: |
| 54729703 | Parent | 7410.67 |
| 54730760 | task075 + task383 constant components | 7393.09 |

Local evidence looked strong:

- task075: public `265/265`, exact random-grid `2000/2000`, cost `559 -> 554`.
- task383: public `266/266`, exact random-grid `2000/2000`, cost `2593 -> 2530`.
- Package: `400/400`, inherited-SHA plus full replacement validation, predicted `+0.03358`.

The failure shows that the exact comparison domain was incomplete. `random-grid` selected dimensions from public examples. A contraction can be algebraically valid for tested fixed selector dimensions and fail for an unseen legal shape. The repository already had a `random-grid-all-shapes` mode, but it was not required for promotion. Combining two unverified tasks also prevented immediate attribution.

Required correction for future competitions:

1. Define the legal shape domain from the generator or competition contract.
2. Prove each contraction symbolically for that domain or test every legal dimension.
3. Run `random-grid-all-shapes`, not public-shape cycling.
4. Submit each shape-sensitive candidate in isolation before stacking.
5. Promote the baseline only after the online result is COMPLETE and non-negative.

## Submission Strategy Review

### Effective

- Five cumulative C batches on Jul 13 provided attribution while preserving quota.
- Parent-aware overlays matched predicted deltas.
- Single-task isolation resolved task187/task251.
- Removing task055 and resubmitting the same safe factor set created a clean causal comparison.

### Ineffective

- The ALL399 13-batch campaign prioritized throughput and included a duplicate batch 07.
- Multiple source-derived tasks were sometimes stacked before hidden behavior was known.
- A small predicted positive delta was submitted despite shape-domain uncertainty in v137.
- Submission descriptions were useful but not a substitute for a machine-readable parent/candidate/online registry.

## Final Attribution Boundary

The final score `7420.93` is a team result. Personal commits contributed C-group models, full-400 optimization infrastructure, public-source analysis, safety gates, and exact contraction methods. It would be incorrect to attribute the entire final delta to the 29 personal commits because:

- many package parents already included A/B/D/E group work;
- public archive models supplied a large portion of the mid-competition gain;
- the final 7420.93 integration was recorded by B-group commits after the last personal main commit;
- the final personal v137 package was a regression and was not the final parent.
