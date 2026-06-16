# Official Rules Review

Date: 2026-06-16

Sources checked:

- `kaggle competitions files orbit-wars`
- `kaggle competitions pages orbit-wars`
- `kaggle competitions pages orbit-wars --content --page-name ...`
- `data/official/README.md`
- `data/official/agents.md`
- `kaggle competitions leaderboard orbit-wars -s`
- `kaggle kernels list --competition orbit-wars --search starter`

No submission command was run.

## Official Files

Kaggle CLI lists these competition files:

| File | Size |
|---|---:|
| `README.md` | 8241 |
| `agents.md` | 6486 |
| `main.py` | 2079 |

The pages endpoint lists:

```text
data-description
Description
Evaluation
rules
abstract
Timeline
Prizes
Getting Started
How to Play Orbit Wars
AGENTS.md
```

Page contents were cached under ignored `outputs/audit/pages/`.

## Game Rules

Orbit Wars is a continuous 2D RTS game on a 100x100 board with a sun at
`(50, 50)`.

Core mechanics from the official README:

- supports 2-player and 4-player games
- 500 turn limit
- winner is highest total ships on planets plus fleets, or last player standing
- planets are represented as `[id, owner, x, y, radius, ships, production]`
- fleets are represented as `[id, owner, x, y, angle, from_planet_id, ships]`
- owned planets generate ships every turn
- orbiting planets rotate around the sun using `initial_planets` and
  `angular_velocity`
- fleets move in straight lines, can leave bounds, hit the sun, or collide with
  planets
- comets spawn at turns 50, 150, 250, 350, and 450
- comet path data is visible in `obs.comets`
- default `actTimeout` is 1 second

Turn order:

1. comet expiration
2. comet spawning
3. fleet launch
4. production
5. fleet movement
6. planet rotation and comet movement
7. combat resolution

## Evaluation

The official Evaluation page says:

- each team can submit up to 5 agents per day
- only the latest 2 submissions are tracked for final submissions
- each submission plays ladder episodes against similarly rated bots
- only the team's best scoring bot is shown on the leaderboard
- new submissions receive more frequent episodes for faster feedback
- a validation episode is run first, against copies of the submitted bot
- valid submissions initialize at rating 600
- rating is modeled as a Gaussian estimate with skill and uncertainty
- the score margin in an episode does not affect rating updates
- after the submission deadline, games continue for approximately two weeks

Competition-specific rules state this is a Simulation competition and there is
no Private Leaderboard in Simulation competitions. Final standings come from the
leaderboard after the post-deadline convergence period.

Timeline page:

- start: 2026-04-16
- final submission deadline variable is shown as `${competition.Deadline}` in
  the CLI page content
- games continue from 2026-06-24 to approximately 2026-07-08, or until
  convergence

## Submission Format

Official `agents.md` says:

- single-file submissions must have `main.py` at the root
- `main.py` must expose an `agent` function
- multi-file agents can be bundled as `submission.tar.gz` with `main.py` at the
  root
- notebook submission is also supported by Kaggle CLI

The starter agent exposes:

```python
def agent(obs):
    ...
```

The local environment also supports callables like `agent(obs, config)` during
local testing, but the official starter documentation only requires `agent(obs)`.

## Data, Network, and Sharing Rules

Competition-specific and general rules indicate:

- Competition Data is under Apache 2.0.
- External data/models are allowed only if public, free or reasonably
  accessible, and not otherwise prohibited.
- During episode evaluation, a submission may not pull external information in
  or send information out.
- Private code sharing outside a team is prohibited.
- Public code sharing is allowed if it is made available to all participants on
  Kaggle discussion or notebooks and uses an OSI-approved license.
- Winners may be required to provide a detailed reproducibility description and
  license winning code under CC-BY 4.0.

## Required Questions

| Question | Answer |
|---|---|
| 1. 2-player or 4-player? | Official README says the game supports 2 or 4 players. The downloaded own replay tested in this session was 2-player. 4-player ladder usage remains to be checked from episodes/replays. |
| 2. Leaderboard rating calculation? | Skill rating updates after episodes using a Gaussian skill/uncertainty model. Win/loss/draw changes rating; score margin does not affect update magnitude. New submissions start at 600 after validation. |
| 3. Replay/episode public? | Rules say replays may be publicly available and downloadable. Our own public episode list and replay download worked. |
| 4. Can other-team episodes be downloaded? | status: unknown; reason: Stage 1 only downloaded our own public episode. Need a visible third-party episode id or replay link to test. next_check: Stage 6 leaderboard/replay audit. |
| 5. Can public notebooks be viewed? | Yes for visible public notebooks: `kaggle kernels list --competition orbit-wars --search starter` returned public kernels. Full notebook review is Stage 3. |
| 6. Can final leaderboard/gold/silver/bronze be seen? | Current leaderboard top teams are visible. Final leaderboard and medals are not final on 2026-06-16 because post-deadline games are scheduled for 2026-06-24 to about 2026-07-08. |
| 7. Must agent expose `main.py` / `agent(obs)`? | Yes. Official submission guide requires root `main.py` with an `agent` function. |
| 8. Multi-file tar.gz allowed? | Yes. Official guide says multi-file agents can be bundled as `submission.tar.gz` with `main.py` at the root. |
| 9. External data allowed? | Yes with restrictions: public/free or reasonably accessible, license-compatible, and reproducible. |
| 10. Network allowed? | No during episode evaluation: submissions may not pull information in or send information out. |

## Current Leaderboard Visibility

`kaggle competitions leaderboard orbit-wars -s` returned visible current top
teams on 2026-06-16. The first rows included:

| Team | Score |
|---|---:|
| Isaiah @ Tufa Labs | 1788.1 |
| Jake Will | 1741.7 |
| Xiangyu Liu | 1664.7 |
| Ender | 1637.0 |
| M & J & M.ver2 | 1589.9 |

These are current public leaderboard ratings, not final medals.

## Unknowns Deferred

```yaml
other_team_replay_download:
  status: unknown
  reason: no third-party episode id was confirmed in Stage 1
  next_check: Stage 6
4_player_ladder_frequency:
  status: unknown
  reason: the sampled own episode replay was 2-player
  next_check: inspect more public episodes and leaderboard replay metadata
final_medal_teams:
  status: unknown
  reason: competition is not final on 2026-06-16
  next_check: Stage 6 current leaderboard/top-team visibility audit
```
