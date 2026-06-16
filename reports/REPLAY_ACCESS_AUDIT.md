# Replay Access Audit

Date: 2026-06-16

No submission command was run.

## Commands Checked

```text
kaggle competitions episodes 53729904 -v
kaggle competitions replay 80134917 -p replays/audit
```

## Own Submission Episodes

Our official starter submission `53729904` has visible episodes. The CLI listed
public completed episodes and one validation episode.

Observed examples:

| Episode ID | State | Type |
|---:|---|---|
| `80134917` | `EpisodeState.COMPLETED` | `EpisodeType.EPISODE_TYPE_PUBLIC` |
| `80130822` | `EpisodeState.COMPLETED` | `EpisodeType.EPISODE_TYPE_PUBLIC` |
| `80119030` | `EpisodeState.COMPLETED` | `EpisodeType.EPISODE_TYPE_VALIDATION` |

## Replay Download Test

Downloaded:

```text
replays/audit/episode-80134917-replay.json
```

This file is intentionally under ignored `replays/` and is not committed.

Parsed structure:

| Field | Observed |
|---|---:|
| JSON keys | `configuration`, `description`, `id`, `info`, `module_version`, `name`, `rewards`, `schema_version`, `specification`, `statuses`, `steps`, `title`, `version` |
| steps | 500 |
| players | 2 |
| final statuses | `DONE`, `DONE` |
| visible non-empty actions in first 50 steps | 16 |

Conclusion:

- Own public replay download works in this session.
- The replay contains observations and actions, so feature extraction from
  visible replay JSON is technically possible.

## Other Teams

```yaml
gold_or_high_rank_replay_access:
  status: unknown
  reason: Stage 1 did not identify a third-party episode id for a top team
  evidence:
    - rules say episode replays may be publicly available and downloadable
    - own public episode replay downloaded successfully
  next_check:
    - Stage 6 leaderboard/top-team audit
    - search discussions and profiles for episode/replay links
    - test `kaggle competitions replay <episode_id>` only if a public episode id is visible
```

## Replay Policy Evidence

Competition-specific rules state that a replay of each episode, including the
actions taken by a submission, may be publicly available and downloadable.

The word "may" matters: this audit does not assume gold/high-rank replay access
until a visible high-rank episode is actually found and downloaded.
