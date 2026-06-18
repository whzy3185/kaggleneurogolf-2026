# Official Replay Phase Review

Date: 2026-06-18

Scope:

1. Review the latest Alyce Intruder official submission replays.
2. Check whether current leaderboard high-rank team replays are accessible.
3. Slice visible high-rank replays by team id / team name.
4. Compare early / mid / late strategies by in-game strength rank.
5. Define the next optimization route without changing agent code in this stage.

No Kaggle submission was run.

## 1. Raw Data Locations

Raw files are intentionally outside git:

- Alyce latest replay root:
  `D:\orbitwars_replays\alyce_intruder_latest`
- Current high-rank replay root:
  `D:\orbitwars_replays\high_rank_current`
- Current leaderboard snapshot:
  `D:\orbitwars_replays\leaderboard_top_20260618.csv`

Generated local analysis files:

- `D:\orbitwars_replays\alyce_intruder_latest\analysis\episode_summary.csv`
- `D:\orbitwars_replays\alyce_intruder_latest\analysis\action_events.csv`
- `D:\orbitwars_replays\high_rank_current\rank_sliced_analysis\target_episode_name_index.csv`
- `D:\orbitwars_replays\high_rank_current\rank_sliced_analysis\selected_top10_episode_outcomes.csv`
- `D:\orbitwars_replays\high_rank_current\rank_sliced_analysis\selected_top10_phase_strategy.csv`
- `D:\orbitwars_replays\high_rank_current\rank_sliced_analysis\selected_top10_rank_phase_aggregate.csv`
- selected high-rank replay copies:
  `D:\orbitwars_replays\high_rank_current\selected_high_rank_replays`

## 2. Replay Access Result

Direct access by current leaderboard `teamId` does not work through the current
CLI session:

```text
kaggle competitions episodes <teamId>
```

For current top teams this returned:

```text
No episodes found
```

This does not mean replay is impossible. It means leaderboard `teamId` is not a
submission id accepted by `kaggle competitions episodes`.

Working access path:

1. Use the current leaderboard to define the high-rank `teamId` / `teamName`
   targets.
2. Use official daily episode datasets to find replay JSON files whose
   `info.TeamNames` include those target team names.
3. Analyze the replay JSON actions and observations.

Downloaded public dataset:

```text
kaggle/orbit-wars-episodes-2026-06-17
```

Local size:

```text
3709 episode JSON files
19.992 GB extracted
```

Important access boundary:

- Full replay observations and actions are visible.
- Other teams' private agent logs are not used.
- Final medals are not known yet, so "gold" and "silver" below mean current
  leaderboard high-rank proxy, not final medal claims.

## 3. Alyce Latest Replay Review

Submission:

```text
submission_id: 53793561
description: alyce_intruder_repro_20260618
visible episodes downloaded: 52
```

Mode split:

| Mode | Episodes | Result summary |
|---|---:|---|
| 2P | 26 | 18 rank-1 / 8 rank-2 |
| 4P | 26 | 8 rank-1 / 6 rank-2 / 6 rank-3 / 6 rank-4 |

2P aggregate:

- average rank: `1.3077`
- wins: `18 / 26`
- losses: `8 / 26`

4P aggregate:

- average rank: `2.3846`
- first-place rate: `8 / 26`
- bottom-two rate: `12 / 26`

### 3.1 Alyce 2P Pattern

2P wins:

- average actions: `111.2`
- enemy actions: `33.1`
- regroup actions: `50.5`
- final production: `65.4`
- final planets: `20.9`
- production at step 50: `30.3`
- production at step 100: `45.1`

2P losses:

- average actions: `169.8`
- enemy actions: `38.0`
- regroup actions: `87.6`
- final production: `2.5`
- final planets: `0.6`
- production at step 50: `19.1`
- production at step 100: `18.0`

Interpretation:

- Losing 2P games are not caused by lack of movement.
- They often show more total actions and more regroup than wins.
- The failure point is that early/mid production collapses or never catches up.

### 3.2 Alyce 4P Pattern

4P rank-1 games:

- average actions: `110.6`
- enemy actions: `42.5`
- regroup actions: `47.5`
- final production: `64.8`
- production at step 50: `24.9`
- production at step 100: `46.1`

4P non-wins:

- average actions: `103.9`
- enemy actions: `43.9`
- regroup actions: `45.1`
- final production: `3.1`
- production at step 50: `11.4`
- production at step 100: `9.1`

4P rank-4 failures:

- final production: `0` in all sampled rank-4 failures
- early production at step 50 is usually already low
- first enemy attack often occurs early, but does not convert into stable
  holdings

Interpretation:

- Alyce's 4P problem is not simply "not attacking enough."
- Non-winning 4P games have similar enemy/regroup action counts to winning
  games, but much weaker expansion and survivability.
- The 4P weakness is a target-quality / FFA-risk problem:
  - unsafe neutrals
  - contested neutrals
  - over-full safe-drain
  - missing leader / third-party risk logic
  - no explicit phase/rank policy

## 4. Current High-Rank Slice

Current leaderboard snapshot top range was read on 2026-06-18. The current top
10 teams used for slicing:

| Current rank | teamId | Team |
|---:|---:|---|
| 1 | 15654628 | Isaiah @ Tufa Labs |
| 2 | 15649057 | Jake Will |
| 3 | 15653847 | Xiangyu Liu |
| 4 | 15635910 | flg |
| 5 | 15821351 | Ender |
| 6 | 15660477 | Hober Malloc |
| 7 | 15733507 | Boey |
| 8 | 15708412 | Audun Ljone Henriksen |
| 9 | 15635790 | Vadasz & Ascalon |
| 10 | 15827519 | Felix M Neumann |

Full daily dataset matches for current top10 by `TeamNames`:

| Team | Matched target appearances |
|---|---:|
| flg | 218 |
| Xiangyu Liu | 191 |
| Jake Will | 172 |
| Ender | 158 |
| Isaiah @ Tufa Labs | 136 |
| Hober Malloc | 130 |
| Audun Ljone Henriksen | 110 |
| Vadasz & Ascalon | 84 |
| Boey | 80 |
| Felix M Neumann | 37 |

Complete phase analysis sample:

```text
selected episodes: 93
selected target appearances: 184
phase rows: 552
action event rows: 30790
```

Selected target appearances by team:

| Team | Samples | Wins | Avg final strength rank |
|---|---:|---:|---:|
| Isaiah @ Tufa Labs | 19 | 11 | 1.789 |
| Jake Will | 22 | 5 | 2.182 |
| Xiangyu Liu | 22 | 8 | 2.136 |
| flg | 25 | 10 | 2.080 |
| Ender | 22 | 7 | 2.182 |
| Hober Malloc | 19 | 7 | 1.947 |
| Boey | 16 | 9 | 1.500 |
| Audun Ljone Henriksen | 15 | 4 | 2.667 |
| Vadasz & Ascalon | 14 | 5 | 2.000 |
| Felix M Neumann | 10 | 5 | 1.700 |

## 5. Phase / Rank Method

For each target player in each replay, the local phase rank is computed from a
production-dominant strength proxy:

```text
strength = owned_production + 0.025 * (planet_ships + fleet_ships)
```

Phase boundaries:

| Phase | Turns |
|---|---|
| early | 0-50 |
| mid | 51-200 |
| late | 201-end |

For each phase, actions were classified approximately by inferred target:

- `neutral`
- `enemy`
- `self_regroup`

This is a replay-level inference from action angle to nearest plausible target.
It is enough for macro phase analysis but not a substitute for internal mission
labels.

## 6. High-Rank Phase Findings

### 6.1 Early Game

Across current top2 and current rank 3-10, early game is still mostly expansion.

Current top2, early phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate |
|---:|---:|---:|---:|---:|---:|
| 1 | 21 | 0.5185 | 0.2246 | 0.2569 | 0.9602 |
| 2 | 9 | 0.5680 | 0.1460 | 0.2860 | 0.9745 |
| 3 | 8 | 0.4595 | 0.2393 | 0.3013 | 0.9561 |
| 4 | 3 | 0.7105 | 0.1155 | 0.1740 | 0.9474 |

Current rank 3-10, early phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate |
|---:|---:|---:|---:|---:|---:|
| 1 | 43 | 0.4853 | 0.2118 | 0.3029 | 0.9676 |
| 2 | 58 | 0.4606 | 0.2336 | 0.3058 | 0.9541 |
| 3 | 17 | 0.4229 | 0.2212 | 0.3559 | 0.9299 |
| 4 | 25 | 0.4633 | 0.2598 | 0.2770 | 0.9290 |

Conclusion:

- High-rank players do not usually open by all-out enemy rushing.
- Early decisions are expansion-heavy, with substantial regroup/positioning.
- Early fullish sends are common, but this does not mean every fullish send is
  safe; high-rank players appear to pair them with better target selection and
  recovery.

### 6.2 Mid Game

The mid game is where in-game rank starts changing behavior.

Current top2, mid phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate |
|---:|---:|---:|---:|---:|---:|
| 1 | 14 | 0.1597 | 0.4955 | 0.3419 | 0.9249 |
| 2 | 14 | 0.1472 | 0.4674 | 0.3850 | 0.8732 |
| 3 | 5 | 0.0524 | 0.3837 | 0.3622 | 0.5877 |
| 4 | 8 | 0.0963 | 0.4664 | 0.1874 | 0.5377 |

Current rank 3-10, mid phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate |
|---:|---:|---:|---:|---:|---:|
| 1 | 56 | 0.1673 | 0.3624 | 0.4681 | 0.8213 |
| 2 | 45 | 0.1512 | 0.4132 | 0.4331 | 0.8341 |
| 3 | 21 | 0.1997 | 0.3565 | 0.4427 | 0.7298 |
| 4 | 21 | 0.1064 | 0.4685 | 0.3775 | 0.7872 |

Conclusion:

- By mid game, top players stop treating the board as expansion-only.
- Current top2 leaders apply much more enemy pressure than current rank 3-10
  leaders.
- Current rank 3-10 leaders regroup/consolidate more heavily.
- Rank-4 players in mid game also show high enemy rates, but their win rate is
  low. This likely represents forced/desperate attacks after falling behind,
  not a reliable comeback pattern.

### 6.3 Late Game

Late game is the clearest phase-rank split.

Current top2, late phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate | Win rate |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 14 | 0.0490 | 0.5031 | 0.2336 | 0.7258 | 0.8571 |
| 2 | 19 | 0.0381 | 0.2233 | 0.2121 | 0.3704 | 0.2105 |
| 3 | 2 | 0.0478 | 0.2407 | 0.2114 | 0.4212 | 0.0000 |
| 4 | 6 | 0.0039 | 0.0722 | 0.0906 | 0.1463 | 0.0000 |

Current rank 3-10, late phase:

| Phase rank | Samples | Neutral rate | Enemy rate | Regroup rate | Fullish rate | Win rate |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 55 | 0.0308 | 0.1360 | 0.3057 | 0.3124 | 0.9091 |
| 2 | 42 | 0.0364 | 0.2471 | 0.2152 | 0.3745 | 0.0714 |
| 3 | 23 | 0.0246 | 0.1518 | 0.1684 | 0.2162 | 0.0435 |
| 4 | 23 | 0.0030 | 0.1146 | 0.0997 | 0.1206 | 0.0435 |

Conclusion:

- Late rank-1 is usually decisive.
- Current top2 rank-1 players close much more aggressively than rank 3-10:
  enemy action rate `0.5031` vs `0.1360`.
- Rank-4 late game has almost no recovery signal. Once a player reaches late
  phase in rank 4, the game is usually already lost.
- Optimization should focus on early/mid prevention of collapse, not only late
  comeback logic.

## 7. Are High-Rank Players Phase/Rank Adaptive?

Yes, visible replay behavior strongly suggests phase/rank-dependent policy.

Observed macro policy:

1. Early:
   - prioritize safe expansion and positioning
   - do not over-prioritize enemy targets
   - use large sends, but only where the target and follow-up are viable

2. Mid:
   - reduce neutral-only behavior
   - increase enemy pressure and regroup
   - leaders convert expansion into attacks
   - trailing players attack more, but many attacks are too late if early
     expansion failed

3. Late:
   - rank-1 top players all-in or heavily pressure enemies
   - rank-2/3 players show partial pressure but low win conversion
   - rank-4 players are often already resource-dead

This is materially different from a single global ROI schedule.

## 8. Difference Versus Alyce Latest

Alyce Light's 4P non-wins resemble the bad high-rank pattern:

- low step-50 / step-100 production
- many actions but poor conversion
- final production often zero
- enemy attacks do not imply a good attack target
- regroup volume does not save a bad expansion base

High-rank top2 difference:

- early expansion remains strong even when not leading
- mid leaders become enemy-pressure heavy
- late leaders commit aggressively
- late rank-4 is avoided by not collapsing earlier

The next improvement should therefore be phase/rank-aware 4P planning, not just
a lower ROI or more actions.

## 9. Next Optimization Route

No code change is made in this stage. The recommended next code attempt should be
small and measured:

### P0: 4P phase/rank policy gate

Add a 4P-only policy layer:

```text
phase = early / mid / late
phase_strength_rank = rank by production + ship proxy
```

Use this to adjust scoring:

- early rank 1-4: preserve safe neutral expansion, avoid random enemy sends
- mid rank 1-2: increase leader/threat pressure
- mid rank 3-4: prioritize survival, recapture, safe neutral, and high-value
  contested snipes instead of blind enemy attacks
- late rank 1: terminal pressure / closeout
- late rank 2-3: targeted leader/threat pressure only
- late rank 4: avoid low-value sends; only elimination/survival missions

### P1: reaction map for neutral targets

For each neutral:

```text
my_best_eta
enemy_best_eta_by_owner
reaction_gap = min_enemy_eta - my_best_eta
```

Classify:

- safe neutral
- contested neutral
- trap neutral

This directly addresses Alyce 4P's early/mid production collapse.

### P2: enemy target classification

Classify enemy targets:

- leader asset
- threat neighbor
- enemy rear
- elimination target

Only apply enemy pressure when the target improves the rank game, not just local
ship delta.

### P3: multi-size drain

Alyce latest and high-rank samples both use many large sends, but Alyce lacks
choice. Add:

- exact floor
- 50%
- 75%
- 100%

Then penalize overcommit on safe neutral and low-value enemy targets.

### P4: mission trace before submission

Every move should be traceable as:

- safe_neutral
- contested_snipe
- leader_pressure
- threat_attack
- defense
- regroup
- terminal

Without mission labels, replay review cannot tell whether a move was good or
just lucky.

## 10. Immediate Go / No-Go

Do not submit another agent based only on this report.

Next useful task:

1. Implement a 4P-only phase/rank policy wrapper around Alyce Light or the chosen
   base.
2. Keep 2P path unchanged initially.
3. Run official-replay-inspired local evaluation and mission trace.
4. Compare against Alyce Light and Vkhydras Last before any Kaggle submission.

