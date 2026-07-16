# Team Commit Context

This file summarizes all 109 commits so the personal timeline is not read as a solo project history. The full chronological list is in `data/all_commits.csv`.

## Author Distribution

| Author identity | Commits |
| --- | ---: |
| jokerrrrr `<3220829322@qq.com>` | 31 |
| lljjcc426 GitHub noreply | 26 |
| whzy `<2402686765@qq.com>` | 26 |
| lljjcc426 `<3115250840@qq.com>` | 9 |
| lc666 | 7 |
| WaterXiao-git | 4 |
| muelsyse `<2402686765@qq.com>` | 3 |
| llllllc | 2 |
| Blacklions | 1 |

Personal identity is the combined `whzy` and `muelsyse` email identity, totaling 29 commits.

## Commit Volume by Day

| Date | All commits | Team phase |
| --- | ---: | --- |
| 2026-07-09 | 33 | Workspace creation, assignments, task mirrors, first C/D/E tooling. |
| 2026-07-10 | 8 | Group-specific baselines and first model experiments. |
| 2026-07-11 | 6 | Parent recovery and objective correction. |
| 2026-07-12 | 18 | Deep per-task campaigns, local gains, and cross-group strategy. |
| 2026-07-13 | 11 | Public archive analysis, cumulative batches, and full-source scan. |
| 2026-07-14 | 11 | Full-400 optimization, runtime failures, hardening, and exact batches. |
| 2026-07-15 | 16 | Source-safe stacks, hidden-risk isolation, exact contractions, final integration. |
| 2026-07-16 | 6 | Final B-group integration record and post-competition cleanup. |

## Team Decision Phases

### Phase 1: Parallel ownership

The repository divided 400 tasks among groups and established group workspaces. Personal commits concentrated on C and later copied D tasks for cross-group study. Other authors simultaneously developed A/B/D/E solutions, so the parent package evolved independently of C work.

### Phase 2: Per-task experimentation

Groups built specialized ONNX models and local validators. The personal C campaign emphasized full coverage and task cards, while other groups produced independent accepted candidates. At this stage, cross-group gains were hard to compose because parent identity and candidate provenance were not yet uniform.

### Phase 3: Parent-aware integration

The 400-model parent became the unit of integration. Personal C commits introduced strict cost comparison and later full-400 tooling. Team submissions increasingly rebased onto the latest known package instead of replacing models from stale local baselines.

### Phase 4: Public-source acceleration

A 399-model public archive changed the score frontier. Personal commits benchmarked and then directly batched many lower-cost artifacts; other groups also studied public and team packages. This phase produced the largest rapid gain, but also introduced compliance, provenance, and hidden-distribution concerns.

### Phase 5: Safety and exact transforms

Runtime failures and hidden regressions forced better controls: forbidden operators, negative-padding rejection, candidate states, SHA-bound parents, deterministic ZIPs, and isolated submissions. Exact transforms and factorization then produced smaller but more reliable gains.

### Phase 6: Final team integration

After the last personal commit on Jul 15, B-group commits integrated a broader audited set:

- `5a4b214`: original rewrite batch.
- `2f565c8` / `07326a2`: exact batch2 and online result `7388.17` on its branch baseline.
- `361a857`: integrate submission5 across all 400 tasks.
- `0ef0128`: record final online score `7420.93`.
- `13691a6`: post-final task018 compaction record.

Therefore `7420.93` is the result of team composition, not the direct score of the last personal branch.

## Branch and Merge Notes

- 28 of 29 personal commits are ancestors of the final source `origin/main`.
- `63b208c` remains only on `codex/full400-hardening-round1` and contains the final contraction scripts and v137 pending-era report.
- `b28ccc9` and `3907fd2` are merge commits authored under the same personal email. Their numstat repeats branch changes and should not be treated as new implementation volume.
- The final source main head audited is `13691a6`, later than the personal branch head.

## Overall Team Assessment

The team was strongest at parallel search and late integration. It was weaker at establishing common safety contracts before submissions. The repository eventually acquired robust baseline and candidate controls, but only after the search space, artifact sources, and submission count had already expanded. Future teams should start with the final hardening architecture and then parallelize modeling inside that framework.
