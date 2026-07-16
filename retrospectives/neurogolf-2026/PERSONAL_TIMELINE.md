# Personal Commit Timeline

Identity rule: author email `2402686765@qq.com`. This includes 26 commits authored as `whzy` and 3 as `muelsyse`. Statistics are Git numstat totals; merge commits repeat branch changes and are not additional implementation volume.

## July 9: Establishing C Group and Finding the Real Objective

### `e7c262d1` 12:55 - Add workplace C Kaggle scaffold

- Scope: 61 files, `+3019` lines.
- Decision: create a reproducible C workspace with data checks, baseline scripts, kernel metadata, validation, reports, and logs.
- Assessment: necessary infrastructure, but it began from a generic Kaggle scaffold while the competition's real optimization unit was per-task ONNX cost. Useful foundation, not direct score work.

### `c61bd558` 12:56 - Document workplace C upload status

- Scope: 3 files, `+56` lines.
- Decision: immediately record fork/push state.
- Assessment: operationally harmless but too granular. This should have been folded into the scaffold commit.

### `349f3648` 14:14 - Add Workplace C task dashboard

- Scope: 10 files, `+670/-3`.
- Decision: add an HTML dashboard, refresh/serve scripts, and a C progress table.
- Assessment: improved visibility across many tasks, but was premature relative to the missing cost/validator pipeline. It optimized coordination before the scoring loop was fully understood.

### `b6543f48` 14:38 - Add full NeuroGolf task mirror for Workplace C

- Scope: 550 files, `+1741/-76`.
- Decision: mirror all 400 task JSON files and normalize `workplace C` naming.
- Assessment: high leverage for offline analysis and complete task visibility. The cost was a very large snapshot commit that should ideally have been a generated dataset or release artifact.

### `9d898e90` 15:59 - C score improvement aggressive checkpoint

- Scope: 107 files, `+7005`.
- Decision: establish cost diff, artifact scan, quick-win ranking, task-card generation, candidate validation, score ledgers, and ONNX surgery probes.
- Assessment: this was the first correct shift toward measured cost reduction. It also created substantial document/template volume before proving a strong candidate, making the commit broader than necessary.

### `251cb9bb` 16:00 - Update C score report checkpoint status

- Scope: 1 file, `+7/-1`.
- Decision: record checkpoint state.
- Assessment: pure bookkeeping and a clear squash candidate.

### `c62c95f0` 21:00 - Add task158 accepted resize stamp improvement

- Scope: 40 files, `+2310/-148`.
- Decision: deeply model task158, preserve input with sparse overwrite logic, and accept a lower-cost resize/stamp candidate.
- Result: cost `28483 -> 28023`, predicted `+0.01628`; the next displayed team score moved `7271.93 -> 7271.95`.
- Assessment: the first meaningful end-to-end success. It connected rule analysis, full public validation, cost reduction, package rebase, and online evidence.

### `a770de6f` 21:02 - Update task158 checkpoint status

- Scope: 1 file, `+4/-4`.
- Decision: update the report after the accepted task158 result.
- Assessment: should have been amended into `c62c95f0`.

### `af72da56` 22:43 - Add task286 rule model and ONNX probe

- Scope: 40 files, `+2223/-15`.
- Decision: attack the high-cost task286 with a dedicated rule model and graph probe.
- Result: established the bitset/propagation structure and difficulty, but did not produce a decisive accepted reduction in this commit.
- Assessment: useful negative evidence on a high-upside target. Better than low-cost polishing, though the report/debug footprint remained large.

## July 11: Correcting the Optimization Objective

### `a6d449c4` 20:51 - Document C score retrospective and next build plan

- Scope: 42 files, `+4500`.
- Decision: explicitly abandon the “all C tasks above 20 points” objective and maximize aggregate point delta. Add parent recovery, status refresh, task runners, and submission controls.
- Result: recognized that parameter reduction alone was insufficient because intermediate activation memory dominates official cost; documented runtime gaps such as uint8 Einsum.
- Assessment: strategically one of the best commits. It corrected the objective and made parent recovery a first-class problem. The amount of documentation was excessive, but the decision itself changed the trajectory.

### `710b5ff8` 22:41 - Advance C individual ONNX model coverage

- Scope: 42 files, `+1481`.
- Decision: expand independent model attempts and track per-task completion rather than only P0/P1 tasks.
- Assessment: improved coverage and exposed reusable patterns, but introduced a breadth metric that later risked becoming another proxy objective.

## July 12: Breadth-First Modeling, Then Parent-Aware Integration

### `89240a42` 13:19 - Complete deep individual modeling for all C tasks

- Scope: 268 files, `+4512/-193`.
- Decision: require every C task to have a rule report, structurally different builder, candidate, and official cost diff.
- Result: `67/67` coverage; only task298 was newly accepted in this campaign (`135 -> 129`, online about `+0.05`). Ten fully correct rewrites were rejected because cost increased.
- Assessment: organizationally complete and scientifically useful, but low score return for a very large change. Its strongest value was proving that full rule correctness often loses to compact existing graphs.

### `a14951f2` 17:52 - Improve C local task score models

- Scope: 46 files, `+1903/-124`.
- Decision: focus on hard-margin one-node Conv models and support cropping rather than multi-tensor semantic rewrites.
- Result: eight accepted local reductions totaling about `+3.10725`, led by task193 (`910 -> 170`), task230 (`900 -> 460`), and task372 (`710 -> 360`).
- Assessment: a major technical improvement. It correctly exploited zero intermediate-memory terminal Conv graphs. The finite-window fitting method still needed hidden-domain safeguards, but online aggregate behavior later matched closely.

### `48e730ff` 18:48 - Add C task077 task096 task349 score gains

- Scope: 24 files, `+1234/-163`.
- Decision: continue three high-value structural compressions: threshold fusion, active-support projection, and collision-safe channel sharing.
- Result: local `+0.33079`; the preceding stack rebased to Kaggle moved `7273.50 -> 7276.61`, matching the predicted `+3.1086` aggregate.
- Assessment: strong targeted continuation with measurable online confirmation.

### `a3c00fa1` 20:50 - Advance C local task score plan

- Scope: 54 files, `+3000/-73`.
- Decision: broaden the second-round task-specific searches across separators, hard margins, line fusion, pad controls, and scalar logic.
- Assessment: retained useful negative searches and several accepted candidates, but mixed many task families into one commit, reducing causal clarity.

### `d019a86d` 21:17 - Document C submission5 rebase to 7278.75

- Scope: 2 files, `+85`.
- Decision: compare every accepted artifact against the exact supplied 400-model parent and overlay only strict cost winners.
- Result: 22 replacements; predicted `+0.91910`, observed `+0.92`, score `7277.83 -> 7278.75`.
- Assessment: the best integration decision in the personal history. It prevented stale and equal-cost artifacts from overwriting a stronger parent and established parent-aware selection as the invariant.

### `98dd3e0e` 22:51 - Mirror D tasks into C workspace and add CD strategy index

- Scope: 70 files, `+150`.
- Decision: expand the search from C to C+D by mirroring D task inputs and indexing methods.
- Assessment: enabled cross-group method transfer, but duplicated task data again. Shared source data with group-specific manifests would have been cleaner.

### `b28ccc90` 23:08 - Merge PR #2

- Scope shown against first parent: 70 files, `+150`.
- Decision: merge the C+D strategy branch.
- Assessment: integration only; it should not be counted as a second 70-file implementation contribution.

## July 13: Archive Intelligence and Aggressive Scale-Up

### `3d2fe525` 11:53 - Benchmark C+D archive methods and derive local optimizations

- Scope: 23 files, `+1170/-11`.
- Decision: benchmark a public 399-model archive, hold direct artifacts for compliance review, extract method families, and independently optimize source graphs.
- Result: identified 54 lower-cost C+D models and direct-output Einsum, QLinearConv, packed state, and selector fusion as high-value families. Independently improved task075; kept archive-derived replacements on hold.
- Assessment: excellent research discipline at this point: learn structure without silently treating claimed source score as verified or immediately replacing the parent.

### `734efb71` 13:25 - Verify five cumulative gains through 7297.02

- Scope: 10 files, `+329`.
- Decision: split 23 independent C replacements into five cumulative batches for online attribution.
- Result: `7296.04 -> 7297.02`; predicted `+0.98369`, observed `+0.98`.
- Assessment: good submission design. Five batches used quota but provided reliable calibration and showed the local scorer tracked the leaderboard.

### `4b744348` 16:35 - Scan all399 archive and record direct batch campaign

- Scope: 31 files, `+2658`.
- Decision: move from method learning to direct replacement of 128 locally lower-cost public-source artifacts, packaged as 13 cumulative batches of ten tasks.
- Result: completed batches matched local projections and drove the score rapidly from `7297.02` into the high `7370s`.
- Assessment: score-effective but the highest governance risk. It reversed the earlier compliance hold, blurred independent contribution versus artifact adoption, consumed many submissions, and created one duplicate batch. The campaign needed explicit rule-owner approval and stronger provenance labeling before execution.

## July 14: Full-400 Automation and Safety Hardening

### `c61118f2` 01:03 - Add validated full-400 ONNX optimization passes

- Scope: 43 files, `+5783/-6`.
- Decision: generalize work across A/C/D with full-400 cleanup, support cropping, campaign orchestration, fuzz comparison, rebase building, and task-specific models.
- Assessment: the most important scale transition. It made every candidate measurable against one parent. However, candidate safety and runtime capability were not yet strong enough, so later commits had to block public-example-selected and unsupported variants.

### `5e4d16d4` 02:15 - Expand exact ONNX optimization across all tasks

- Scope: 3 files, `+605/-10`.
- Decision: broaden exact cleanup and comparison across the full model set.
- Assessment: high leverage relative to commit size. Method reuse replaced repeated manual work.

### `836fdcb7` 02:21 - Parameterize verified parent package metadata

- Scope: 1 file, `+9/-4`.
- Decision: stop hardcoding parent identity and require metadata parameters.
- Assessment: small, high-value safety fix. Parent SHA binding should have existed before any cumulative campaign.

### `6a7a6b68` 02:23 - Build self-contained Kaggle submission kernels

- Scope: 1 file, `+134`.
- Decision: embed package submission logic into reproducible Kaggle kernels.
- Assessment: improved delivery reliability and reduced environment drift.

### `09c98d4e` 09:47 - Harden full-400 ONNX optimization and validation

- Scope: 50 files, `+5064/-312`.
- Decision: add baseline manifest, candidate registry and state machine, runtime-risk audits, exact comparison modes, QLinearConv zero-point-aware cropping, cache identity, deterministic ZIPs, CI, and blocked-candidate rules.
- Result: explicitly blocked uint8 TopK, negative padding, public-example selection, and unproven candidates.
- Assessment: the strongest engineering-quality commit. It was reactive, but it converted lessons from platform errors into enforceable gates.

### `3907fd22` 09:50 - Merge PR #3

- Scope shown against first parent: 52 files, `+5800/-314`.
- Decision: merge the hardening branch.
- Assessment: integration commit; implementation belongs primarily to the preceding hardening commits.

## July 15: Hidden-Distribution Learning and Final Contractions

### `6f0acd38` 15:30 - Record public-source gains and hidden-distribution safeguards

- Scope: 50 files, `+5107/-21`.
- Decision: preserve large public-source gains while adding runtime capability matrices, stronger blocked states, exact transform scans, external-source provenance, and hidden-regression records.
- Result: documented the task251 hidden regression: a combined package dropped `7407.70 -> 7391.08`; isolating task187 produced `7408.86`, attributing the failure to task251.
- Assessment: good evidence-driven correction. Isolation converted an unexplained package failure into a task-level block. The remaining weakness was that generator/all-shape validation was still not uniformly mandatory.

### `63b208cb` 23:26 - Add exact ONNX contraction optimizations and closeout results

- Scope: 45 files, `+6426/-56`; not merged into NGC source main.
- Decision: add exact terminal factorization, transpose-aware deduplication, private-axis precontraction, constant-component precontraction, incremental validation, and supporting single-task evidence.
- Local result: task075 `559 -> 554`, task383 `2593 -> 2530`; both passed all public examples and 2000 exact random-grid comparisons. The combined v137 package predicted `+0.03358` over `7410.67`.
- Online result after the commit: ref `54730760` scored `7393.09`, a `-17.58` regression.
- Assessment: the transform code and evidence discipline were materially better than early work, but the proof domain was incomplete. Random inputs cycled through public input shapes rather than all legal shapes. The two candidates were stacked without isolated online probes. This commit is the clearest demonstration that “exact on tested tensors” is not equivalent to “exact over the competition generator.”

## Commit-Hygiene Summary

- Strong: commits increasingly tied code, cost, validation, SHA, and online evidence together.
- Weak: early giant snapshot/report commits and tiny status-only follow-ups obscured decision boundaries.
- Weak: merge commits duplicate first-parent diff statistics and should not be read as new implementation.
- Weak: the final personal commit was pushed to a side branch but not merged into NGC main, so its source and post-submit failure were separated from the team’s canonical timeline.
- Recommended structure: one commit for transform implementation and tests, one for accepted task evidence, one for online result and baseline promotion.
