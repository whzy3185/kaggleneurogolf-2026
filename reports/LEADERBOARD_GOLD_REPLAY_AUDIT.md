# Orbit Wars Leaderboard / Gold Replay Audit

Date: 2026-06-16

This stage checks current leaderboard visibility and whether gold/high-rank
replays can be inspected. It does not submit anything and does not download
large replay archives.

## Leaderboard Status

- Current public leaderboard: visible through Kaggle CLI.
- Full public leaderboard CSV: downloaded to ignored `outputs/audit/leaderboard/`.
- Snapshot file:
  `outputs/audit/leaderboard/unzipped/orbit-wars-publicleaderboard-2026-06-16T12_06_58.csv`
- Top team at snapshot time: `Isaiah @ Tufa Labs`, score/rating `1782.5`.
- Final leaderboard: not final yet on 2026-06-16.
- Gold/silver/bronze medal teams: not available yet.

Gold team replay is not accessible in this session.

Reason: final gold teams do not exist yet as of 2026-06-16. The competition is
still in active public leaderboard play and the final post-deadline evaluation
period has not completed.

Evidence:

- Current leaderboard has active submission dates through 2026-06-16.
- Stage 1 official rules review recorded the final post-deadline game period.
- No final medal labels are present in the current leaderboard CSV.

Next manual check:

- After the final leaderboard/medals are published, identify gold teams from
  the final leaderboard UI/API, then check whether episode IDs or daily replay
  datasets expose their replays.

## Current Top Leaderboard Snapshot

Top 10 at the 2026-06-16 snapshot:

| Rank | Team | Public score/rating | Last submission date |
|---:|---|---:|---|
| 1 | Isaiah @ Tufa Labs | 1782.5 | 2026-06-14 01:18:29 |
| 2 | Jake Will | 1745.1 | 2026-06-09 23:23:04 |
| 3 | Xiangyu Liu | 1675.2 | 2026-06-15 13:59:12 |
| 4 | Ender | 1613.6 | 2026-06-16 07:29:05 |
| 5 | M & J & M.ver2 | 1601.1 | 2026-06-16 03:14:10 |
| 6 | Boey | 1598.2 | 2026-06-16 06:27:44 |
| 7 | Hober Malloc | 1576.5 | 2026-06-16 08:42:45 |
| 8 | flg | 1569.7 | 2026-06-15 16:45:43 |
| 9 | Vadasz & Ascalon | 1568.2 | 2026-06-13 14:50:58 |
| 10 | TonyK | 1564.3 | 2026-06-12 23:19:58 |

Full top-25 registry: `configs/top_team_registry.yaml`.

## Replay Access Tests

Confirmed:

1. Public daily episode index is visible:
   `kaggle/orbit-wars-episodes-index`.
2. Daily replay dataset files are visible, e.g.
   `kaggle/orbit-wars-episodes-2026-06-15`.
3. Individual replay JSON files can be downloaded from the daily dataset.
4. Replay JSON includes:
   - `info.TeamNames`
   - `info.EpisodeId`
   - `configuration.seed`
   - per-step `action`
   - per-step observations
5. Actions are visible in downloaded replay JSON.
6. Agent code is not visible in replay JSON.
7. Agent logs remain private to the user's own agent per Stage 2 discussion
   evidence.

Current high-rank replay samples downloaded:

| Episode | Teams visible in replay |
|---:|---|
| 79968955 | Jake Will, Ender, Hober Malloc, Isaiah @ Tufa Labs |
| 79968870 | Boey, CPMP, Radek Osmulski, aaa |
| 79968841 | flg, ma name, Roche Overflow, Abhyuday |
| 79968923 | Gregor Lied, vkhydras, 213tubo, bowwowforeach |
| 79968910 | bowwowforeach, CPMP, Man Penguin, luckyappley |

This means current high-ranking public replays are visible when an episode ID
or daily dataset file is known. It does not mean final gold replays are known,
because final gold teams do not exist yet.

## Episode Listing Limits

The current CLI leaderboard gives `TeamId`, not `submissionId`.

Tests:

```bash
kaggle competitions episodes 15654628 -v
kaggle competitions episodes 15649057 -v
kaggle competitions episodes 15653847 -v
```

Result: `No episodes found`.

Interpretation: in this session, top leaderboard `TeamId` cannot be used as a
submission ID. To list episodes through `kaggle competitions episodes`, a
submission ID is needed. Daily public datasets are therefore the working route
for high-rank replay samples unless the UI or another public source exposes a
submission ID.

## Public Notebooks / Discussion For Top Teams

For current top-10 team member usernames, this command shape was tested:

```bash
kaggle kernels list --competition orbit-wars --user <username> --page-size 20 -v
```

Result for the tested top-10 member usernames: no visible Orbit Wars notebooks
were returned by the CLI in this session.

Discussion mapping is limited because `kaggle competitions topic-messages`
returned blank `authorName` fields in this session. No strategy is inferred
from unseen discussion posts.

## Strategy Evidence Boundary

Allowed evidence:

- downloaded public replay actions
- public notebooks/repos/discussion posts
- official rules/discussion statements

Not allowed / not available:

- private agent code
- other teams' private logs
- final gold strategy before final medal teams exist
- inferring private strategy from leaderboard rank alone

