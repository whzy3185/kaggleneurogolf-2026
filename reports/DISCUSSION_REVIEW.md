# Orbit Wars Discussion Review

Date: 2026-06-16

Scope: all Kaggle discussion topics visible through the current Kaggle CLI
session.

## Access Method

Commands used:

```bash
kaggle competitions topics list orbit-wars --sort-by hot --page-size 100 --page <n> -v
kaggle competitions topics list orbit-wars --sort-by top --page-size 100 --page <n> -v
kaggle competitions topics list orbit-wars --sort-by new --page-size 100 --page <n> -v
kaggle competitions topics list orbit-wars --sort-by recent --page-size 100 --page <n> -v
kaggle competitions topics list orbit-wars --sort-by active --page-size 100 --page <n> -v
kaggle competitions topic-messages orbit-wars <discussion_id> --page-size -1 -v
```

Intermediate CSV/text caches were kept under `outputs/audit/discussions/`
and are intentionally ignored by git.

## Coverage

- Visible topics collected: 234
- Visible messages collected: 1,378
- Registry output: `configs/discussion_registry.yaml`
- Topic author limitation: `authorName` was blank in the CLI output for this
  session, so registry entries use `unknown_cli_blank` instead of guessed
  authors.
- Hidden/private/deleted topics are not visible through this session and are
  not represented.

## High-Confidence Facts

1. Public replay access is allowed.
   Discussions `694210` and `694980` contain official/staff clarification that
   replays are public while agent logs are private to the user's own agent.
   This is the strongest available evidence that replay JSON analysis is
   permitted when using normal Kaggle access.

2. Agent logs are private.
   The same replay/log topics state that logs can be downloaded only for your
   own agent index. This audit does not attempt to access other teams' logs.

3. Public episodes and replay datasets are central community resources.
   Discussions `701894`, `697413`, and `701984` describe daily episode datasets,
   top-10% replay datasets, and a Parquet replay database. Dataset packaging
   and overlap must be verified before use.

4. Four-player symmetry and collision behavior changed during the competition.
   Discussions `694310`, `694910`, `692695`, `694605`, and `696043` document
   map symmetry, comet observation, OOB/sun collision, and swept-pair collision
   fixes. Old cached environments or old replays can differ from current play.

5. Runtime budget is tight but episode-local caching is valid.
   Discussions `700191` and `694188` report 1s `actTimeout`, a 60s overage
   bank, wall-clock timeout semantics, and fresh process per episode with
   module-level caches usable inside one episode.

6. Latest two submissions matter for final simulation play.
   Discussions `708352` and `704976` state that only the latest two submissions
   continue to play and are used for the final post-deadline run. There is no
   ordinary private leaderboard/manual final selection flow like tabular Kaggle
   competitions.

## Community Strategy Consensus

The public discussion consensus is no longer "nearest planet starter" play.
Most high-value public discussion clusters point toward one of five stronger
directions:

1. ROI / production-greedy heuristics.
   `704113` The Producer and `699003` target present-value scoring both argue
   that expansion and attacks should be judged by discounted future production,
   travel time, required ships, and whether a send actually improves total
   production.

2. World-model/search agents.
   Discussion around `708209`, `703674`, and `705482` repeatedly says raw
   behavior cloning is not enough because strong bots are doing search or
   option evaluation. The actionable lesson is to reproduce/improve the
   planner, not just imitate actions.

3. Physics-aware aiming and collision safety.
   `692752`, `703466`, and `704817` emphasize ETA, sun safety, intercept
   angle/turn lookup, and aiming benchmarks. Accuracy and speed of path
   prediction are recurring bottlenecks.

4. Replay-driven behavioral analysis.
   `701984` describes mission classification, player fingerprinting,
   build-order clustering, and early winner prediction from public replays.
   This directly supports profiler trace logging and opponent-family detection.

5. RL / BC with fast environments and curated data.
   `697725`, `704741`, `707869`, `708209`, `700270`, and `693755` show that
   RL/BC is active and may have a high ceiling, but the recurring warnings are
   high cost, unstable training, need for fast JAX/Torch/native environments,
   and covariate shift when cloning search agents.

## Required Discussion Categories

| Category | Representative discussions | Audit result |
|---|---:|---|
| Official announcements / rule updates | 694210, 694980, 694188, 705170, 708352, 704976 | Replay/log access, timeout, matchmaking, and final-submission behavior recorded. |
| Bug fixes | 694310, 694910, 692695, 694605, 696043, 698395 | Symmetry, comet observation, collision, and metadata issues recorded with current-version risk. |
| Starter or baseline improvements | 692752, 699003, 704113 | Starter weaknesses and production/ROI alternatives recorded. |
| High-score strategy sharing | 704113, 704741, 707869, 708209, 705482 | Claims recorded as community claims, not official leaderboard facts. |
| Strong agent releases | 704113, 708108, 704817, 694127, 702126 | Producer, agent dump, C lookup engine, labs/tooling registered. |
| Local eval vs leaderboard deviation | 698614, 704095, 701745, 700048 | Community tournaments and seed panels are useful but unofficial. |
| Replay visualization / data tools | 694127, 702126, 704849, 701894, 701984 | Multiple tools and datasets identified. |
| 2P / 4P strategy difference | 694273, 698659, 704777, 705019, 707660 | Mode mix and 4P weakness are recurring themes. |
| Gold / high-rank team posts | 703674, 704267, 708209, 704741 | No final gold teams exist yet on 2026-06-16; top-team strategy details are mostly speculation unless backed by public replays. |
| Reproducible code or notebook links | 694127, 702126, 704113, 703466, 700270, 708108 | Links carried into registry for Stage 3/4 collection. |

## High-Value Topic Notes

| ID | Type | Evidence | Key takeaway |
|---:|---|---|---|
| 694210 | official/replay | official/staff | `episodes`, `replay`, and `logs` CLI commands; replays public, logs private. |
| 694980 | official/replay | official/staff | UI replay download; all replays public. |
| 701894 | replay dataset | official/staff | Official daily dataset index for top average rated episodes, up to 20GB/day. |
| 697413 | replay dataset | community/staff | Top-10% replay datasets existed, but early manifest/replay completeness issues were reported. |
| 701984 | replay dataset | community | Parquet replay DB enables behavioral profiling; verify version/overlap before use. |
| 694310 | bugfix | official/staff | 4P map symmetry issue found and fixed. |
| 696043 | bugfix | official/staff | Fleet tunneling collision bug fixed with swept-pair logic. |
| 704113 | public agent | community claim | Producer: ROI production planner plus front-line redeployment; strong public greedy baseline. |
| 699003 | strategy | community | Present-value target scoring with travel-time discount is a strong baseline concept. |
| 708209 | ML/search | community claim | Cloning top replay actions lost to Producer because imitation missed 1-ply search/lookahead. |
| 697725 | RL | community claim | Fast env, entity transformer, feature engineering, self-play, and reward shaping are key RL themes. |
| 704741 | RL | community claim | PPO can train if environment/eval/curriculum are engineered; claims not treated as official scores. |
| 707869 | BC/RL | community claim | Supervised imitation can bootstrap RL if good decisions are curated rather than blindly copied. |
| 698614 | benchmark | community | 50-agent public tournament identifies useful public opponent pool candidates. |
| 704095 | benchmark | community | 109-agent tournament suggests many strong public agents share lineage; wrappers need validation. |
| 703466 | benchmark | community | Aiming benchmark from top-10% replay shots is directly relevant to attack generation. |
| 704817 | public code | community | C precompute engine provides intercept angle/turn tables and observed-fleet arrival events. |
| 698478 | strategy | community claim | Enemy fleet angles are visible; recapture-after-capture and arrival prediction matter. |
| 704777 | leaderboard/meta | community | Top players were observed receiving mostly 2P games; mode mix can affect score interpretation. |
| 705170 | official/meta | official/staff | Matchmaking/scoring fixes changed high-vs-low rating behavior and top-player opponent selection. |

## Leaderboard / Gold Caveat

As of 2026-06-16, Orbit Wars is still in active competition. Final gold,
silver, and bronze teams are not yet final. Discussion posts about top players
are therefore treated as current-ladder observations or speculation, not medal
evidence.

Visible public replays can be analyzed in Stage 6/7 if episode IDs are
available. Until a replay is actually downloaded and inspected, no private
strategy claim is made about a top or future gold team.

## Actionable Ideas For Later Stages

1. Build a replay-derived profiler trace: expansion timing, first attack,
   recapture attempts, fleet cadence, multi-source sends, and phase-specific
   reserve ratio.
2. Add explicit enemy fleet trajectory parsing; enemy angle/source/ships are
   visible and enough to infer many target/ETA events.
3. Benchmark against Producer-like ROI planners and public tournament winners,
   not only older starter-like bots.
4. Add separate 2P and 4P evaluation and profiling, because public discussion
   repeatedly reports mode-specific strength gaps.
5. Add an aiming benchmark before changing low-level attack generation.
6. Treat public notebook/LB-title score claims as leads only; validate locally
   and never write them as official leaderboard results.

## Manual Browser Checks Still Useful

- Kaggle UI may show richer author/profile context than the CLI did in this
  session.
- Some discussion attachments/images are not captured by CLI text.
- Current leaderboard links for a specific top submission should be checked in
  Stage 6 before claiming replay availability for that team.

