# NeuroGolf 2026 Commit Retrospective

This retrospective covers the complete `lljjcc426/NGC-work` commit graph at the end of the competition, with detailed analysis of commits authored with `2402686765@qq.com` (`whzy` and `muelsyse`). It lives in `whzy3185/kaggleorbit`, not in NGC-work.

## Scope

- Source repository: `lljjcc426/NGC-work`
- Source main head audited: `13691a6262e15effe42ef4fa396d6f67a5217060`
- Total commits audited: `109`
- Personal commits: `29`
- Personal commits in source `origin/main`: `28`
- Personal commit outside source main: `63b208cbed822e5f21e2cfeac272a7bd9be9b348`
- Kaggle submissions captured after competition close: `200`
- Final complete team score: `7420.93` (`54736568`)

The raw evidence is reproducible through `scripts/extract_history.py`. Detailed records are in `data/all_commits.csv`, `data/personal_commits.csv`, and `data/kaggle_submissions.json`. The extractor automatically redacts token-shaped strings that appeared in historical submission descriptions.

## Executive Judgment

The work progressed through four distinct operating models:

1. **Repository and visibility first.** The first day created a complete C-group workspace, mirrored all 400 tasks, and built dashboards and task cards. This solved coordination, but generated more structure than score.
2. **Breadth-first individual modeling.** Every C task received an independent attempt. This produced useful negative evidence and a few real gains, but the return per changed file was low.
3. **Parent-aware score engineering.** The decisive improvement came when accepted candidates were compared against the latest 400-model parent and only strict cost winners were overlaid. Local predictions then matched Kaggle closely.
4. **Method transfer and full-400 automation.** Archive structure analysis, exact graph transforms, registries, deterministic packaging, and incremental validation scaled the work. This produced the largest score movement, but safety controls arrived after several runtime and hidden-distribution failures.

The personal contribution was strongest when it converted a task-specific insight into a parent-bound, exactly validated transform. It was weakest when coverage, documentation, or a local validation label was treated as an objective by itself.

## Score Timeline

| Date | Milestone | Score | Decision significance |
| --- | --- | ---: | --- |
| Jul 11 | task158 rebase | 7271.95 | First small online-positive C replacement; local delta matched display precision. |
| Jul 12 | task298 isolated | 7273.42 | Completed 67/67 deep-model coverage, but only one new accepted gain. |
| Jul 12 | eight-task local stack | 7276.61 | Hard-margin and support-crop designs produced about +3.11 as predicted. |
| Jul 12 | parent-aware 22-task overlay | 7278.75 | Expected +0.9191, observed +0.92; established the correct integration rule. |
| Jul 13 | five cumulative C batches | 7297.02 | Expected +0.9837, observed +0.98; good staged online verification. |
| Jul 13-14 | ALL399 public-source campaign | about 7378-7379 | Huge score acceleration, but provenance, compliance, and attribution risk increased sharply. |
| Jul 14 | exact full-400 passes | 7381.68+ | Shifted from per-task hand work to reusable exact transforms. |
| Jul 15 | source-safe and isolated task187 stacks | 7408.86 | Hidden failure on task251 was diagnosed by isolation. |
| Jul 15 | exact factor/contraction stacks | 7410.67 | Small structural reductions accumulated reliably through v136. |
| Jul 15 | v137 task075/task383 | 7393.09 | A predicted +0.0336 became -17.58 online; known-shape fuzz was not global equivalence. |
| Jul 15 | audited team integration | 7419.90 | Excluded unsafe local candidates and integrated the broader team set. |
| Jul 15 | final team package | 7420.93 | Final complete public/private score recorded after competition close. |

## Best Decisions

### 1. Replacing the 20-point target with aggregate score delta

The Jul 11 retrospective explicitly rejected the idea that every C task should exceed 20 points. This prevented continued work on cheap low-upside tasks and redirected effort toward large `log(old_cost/new_cost)` opportunities.

### 2. Parent-aware best-per-task rebasing

Commit `d019a86d` compared every candidate with the supplied 7277.83 parent, skipped equal-cost and stale artifacts, and overlaid 22 strict winners. The predicted and observed gains matched. This was the cleanest evidence that the local scorer and integration method were aligned.

### 3. Using failed independent models as measured counterexamples

The 67-task campaign did not pretend that rule correctness implied score improvement. Ten final candidates passed every public example but were rejected because their activation cost increased. This exposed the importance of intermediate tensor memory.

### 4. Turning task insights into reusable exact transforms

Support cropping, transpose-aware initializer deduplication, terminal Einsum factorization, and constant-component precontraction were more valuable than one-off model rewrites because they could be searched across hundreds of graphs.

### 5. Adding parent identity, candidate states, runtime audits, and deterministic ZIPs

The hardening round introduced the controls that should have existed earlier: baseline SHA binding, blocked/local-only states, forbidden-op scans, exact comparison modes, cache identity, deterministic packaging, and CI.

## Main Mistakes

### 1. Breadth was confused with progress

The 67/67 modeling milestone was organizationally useful, but it changed 268 files and produced only one newly accepted task in that campaign. A better early policy would have required a theoretical cost lower bound and an activation-budget sketch before implementing every independent graph.

### 2. Documentation and generated snapshots dominated early commits

Several large commits primarily created mirrors, task cards, dashboards, and reports. Two follow-up commits only changed checkpoint status. These should have been squashed or separated from optimization code. The history makes decision causality harder to read than necessary.

### 3. Safety architecture was reactive

Runtime-incompatible `uint8 TopK`, negative padding, public-example-selected candidates, and stale-parent risks were discovered after candidate generation and submissions. Registry and runtime capability gates should have preceded the full-400 campaign.

### 4. External source adoption weakened provenance and attribution

The Jul 13 archive analysis initially placed direct models on compliance hold, then the ALL399 campaign directly replaced 128 tasks in 13 batches. It was highly score-effective, but made it harder to distinguish independent method transfer from artifact adoption and consumed submission quota, including one duplicate batch.

### 5. “Exact” was scoped too narrowly in v137

`task075` and `task383` passed all public examples and 2000 exact random tests, but those random tests only used shapes already present in public data. The combined package dropped from 7410.67 to 7393.09. The transformation was exact on the tested shape domain, not on the competition's full shape domain. `random-grid-all-shapes` existed but was not the promotion gate, and the two changes were not isolated before stacking.

## What Should Be Reused

- Parent-bound candidate registry with explicit terminal states.
- Strict `candidate_cost < parent_cost` selection.
- Model and package SHA tracking.
- Deterministic root-only 400-file ZIP construction.
- Incremental validation by inherited model SHA plus full validation of replacements.
- Exact symbolic transforms with a declared shape domain.
- Single-task online isolation for high-risk or shape-sensitive changes.
- Negative-evidence retention for failed model families.

## What Should Change Next Time

1. Define the legal input shape and state space before calling a transform exact.
2. Run all-shape fuzz or generator validation, not only public-shape random grids.
3. Isolate every candidate whose proof depends on shape, padding, quantization, indexing, or external provenance.
4. Build registry, runtime matrix, deterministic packaging, and parent binding before mass optimization.
5. Keep commits small by decision: transform code, validation evidence, and online result should be distinct but linked commits.
6. Store generated task mirrors and large reports as release artifacts or datasets, not in core code history.
7. Use submission batches for attribution, not just throughput; never submit a duplicate cumulative batch.

## Files

- `KAGGLE_CODE_DISCUSSION_LESSONS.md`: public Kaggle Code and Discussion review collected after competition close, with reusable workflow lessons.
- `NGC_WORK_LOCAL_INVENTORY.md`: local NGC-work discovery, rename, repository state, and historical-path-reference audit.
- `guides/LOCAL_KAGGLE_SUBMISSION_PLAYBOOK.md`: reusable local Kaggle CLI, token setup, kernel, submission, polling, and failure-handling workflow.
- `guides/KAGGLE_OPTIMIZATION_STRATEGY_PLAYBOOK.md`: validation-first experiment selection, expected-value prioritization, rebasing, and submission-budget strategy.
- `PERSONAL_TIMELINE.md`: all 29 personal commits in chronological order.
- `TEAM_CONTEXT.md`: all-commit context and team integration.
- `SCORE_AND_FAILURES.md`: score milestones, runtime failures, and hidden-distribution lessons.
- `data/personal_commits.csv`: exact personal commit metadata and changed paths.
- `data/all_commits.csv`: complete 109-commit history.
- `data/kaggle_submissions.json`: 200 submission records captured after competition close.
- `scripts/extract_history.py`: reproducible extractor.
