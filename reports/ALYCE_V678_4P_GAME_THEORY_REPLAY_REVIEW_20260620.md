# Alyce V6/V7/V8 4P Game-Theory Replay Review - 2026-06-20

## Scope

User requested a full 4P decision review covering:

```text
V6 current official best
V7 continuous recovery experiment
V8 MD coverage / mission experiment
```

This review uses all currently visible official replay files downloaded for
these submissions:

```text
V6: D:\orbitwars_replays\alyce_v6_latest
V7: D:\orbitwars_replays\alyce_v7_latest
V8: D:\orbitwars_replays\alyce_v8_latest
Combined analysis: D:\orbitwars_replays\alyce_v678_game_theory_analysis
```

Generated local analysis files, not committed:

```text
D:\orbitwars_replays\alyce_v678_game_theory_analysis\game_theory_episode_summary.csv
D:\orbitwars_replays\alyce_v678_game_theory_analysis\game_theory_phase_snapshots.csv
D:\orbitwars_replays\alyce_v678_game_theory_analysis\game_theory_action_events.csv
D:\orbitwars_replays\alyce_v678_game_theory_analysis\game_theory_summary.json
```

Committed tooling:

```text
scripts/analyze_4p_game_theory_replays.py
```

Important limitation:

```text
Official replay JSON exposes observations and submitted actions. It does not
expose Alyce internal candidate scores or neural/logit state. Target labels,
reaction gaps, and response links below are inferred from visible source planet,
launch angle, current planet ownership, and later visible actions.
```

## Official Status

Latest Kaggle CLI query:

| Variant | Submission | Status | Public score |
|---|---:|---|---:|
| V6 | `53852919` | `SubmissionStatus.COMPLETE` | `1177.8` |
| V7 | `53874852` | `SubmissionStatus.COMPLETE` | `920.2` |
| V8 | `53874866` | `SubmissionStatus.COMPLETE` | `1134.8` |

Conclusion:

```text
V6 remains the official best.
V8 is a useful data-collection experiment but did not beat V6.
V7 is clearly rejected.
```

## Replay Coverage

Public replay rows analyzed:

| Variant | 2P public episodes | 4P public episodes | Validation/self-play |
|---|---:|---:|---:|
| V6 | 38 | 34 | 1 |
| V7 | 9 | 15 | 1 |
| V8 | 9 | 12 | 1 |

The V7/V8 visible sample is smaller than V6 because fewer official public games
were visible at analysis time. Treat V7/V8 replay stats as directional, but the
official score ordering is already decisive.

## 4P Game Nature

4P Orbit Wars is not a simple extension of 2P.

In 2P, most enemy attacks are close to zero-sum:

```text
I spend ships -> enemy loses planet/ships -> my relative position improves.
```

In 4P, the same action creates externalities:

```text
I spend ships attacking A.
B and C spend nothing.
A defends or counterattacks me.
B/C can clean up the weakened target, my depleted source, or a center neutral.
```

The game is closer to a dynamic free-for-all common-pool game:

1. Center and high-value frontier planets are public contested resources.
2. Early visible overcommit changes opponent incentives.
3. A local tactical win can become a global rank loss if a third party captures
   the aftermath.
4. Hitting the leader is only good when the action is holdable or rank-improving;
   otherwise it is kingmaking for another non-leader.
5. Being slightly behind is recoverable; becoming the cheapest victim for two
   neighbors is usually terminal.

Therefore a 4P agent needs a mission layer that asks:

```text
Who benefits after this action resolves?
Can I hold the planet after arrival?
Does this reveal a depleted source and invite two-sided pressure?
Will the leader grow because I am busy fighting a non-leader?
Is the action rank-improving, or only score-positive in isolation?
```

## Public Episode Summary

| Variant | Mode | Episodes | First | First rate | Avg final prod | Avg final prod rank | Avg final ships |
|---|---:|---:|---:|---:|---:|---:|---:|
| V6 | 2P | 38 | 21 | 0.553 | 33.18 | 1.42 | 1060.6 |
| V6 | 4P | 34 | 11 | 0.324 | 16.35 | 1.68 | 1117.9 |
| V7 | 2P | 9 | 6 | 0.667 | 36.78 | 1.33 | 1730.4 |
| V7 | 4P | 15 | 3 | 0.200 | 12.53 | 1.80 | 1534.3 |
| V8 | 2P | 9 | 8 | 0.889 | 58.33 | 1.11 | 1786.3 |
| V8 | 4P | 12 | 3 | 0.250 | 13.08 | 1.83 | 1388.1 |

Read:

```text
V8 looked good in visible 2P and some 4P games, but official rating still stayed
below V6. The likely cost is not runtime failure; it is worse match-quality
generalization and remaining 4P collapse in hard games.
```

## 4P Non-First Phase Collapse

| Variant | Step | N | Avg prod | Avg gap to prod leader | Avg prod rank | Avg planets | Avg ships |
|---|---:|---:|---:|---:|---:|---:|---:|
| V6 | 20 | 23 | 7.57 | -1.39 | 1.78 | 2.61 | 76.6 |
| V6 | 50 | 23 | 9.35 | -6.87 | 2.78 | 3.00 | 173.4 |
| V6 | 100 | 23 | 7.22 | -19.39 | 2.87 | 2.30 | 144.8 |
| V6 | 150 | 23 | 2.48 | -41.09 | 2.70 | 1.00 | 95.8 |
| V6 | 200 | 23 | 1.22 | -51.04 | 2.09 | 0.43 | 59.1 |
| V7 | 20 | 12 | 7.17 | -1.33 | 1.67 | 2.42 | 86.7 |
| V7 | 50 | 12 | 12.08 | -4.67 | 2.33 | 3.75 | 235.7 |
| V7 | 100 | 12 | 13.50 | -14.50 | 2.50 | 4.58 | 338.7 |
| V7 | 150 | 12 | 10.50 | -28.08 | 2.33 | 3.25 | 338.0 |
| V7 | 200 | 12 | 5.08 | -44.33 | 2.17 | 1.75 | 221.4 |
| V8 | 20 | 9 | 6.78 | -0.56 | 1.56 | 2.67 | 62.9 |
| V8 | 50 | 9 | 9.89 | -9.78 | 3.11 | 3.33 | 157.1 |
| V8 | 100 | 9 | 9.00 | -28.56 | 2.56 | 3.00 | 168.2 |
| V8 | 150 | 9 | 6.44 | -44.11 | 2.11 | 2.11 | 133.3 |
| V8 | 200 | 9 | 0.00 | -58.00 | 2.11 | 0.00 | 0.0 |

Main conclusion:

```text
The 4P loss is usually decided by step 50-100. V8 did not fix this; its visible
4P non-first games are slightly better at step 20 but worse by step 50/100 than
V6. That means the extra V8 filter/multi-size machinery is not enough and may
be disturbing the opening production race.
```

## Action Response Evidence

The analyzer counts visible opponent responses in the 12 turns after each of our
actions. This is not causal proof, but it is useful evidence for the user's
question: "does our action induce opponent decisions?"

| Variant | Result | Phase | Actions | Enemy | Neutral | Mine | Center | Cleanup risk | Early sacrifice | Commit | Direct response/action | Third-party/action |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V6 | first | opening_0_50 | 234 | 0.256 | 0.594 | 0.150 | 0.034 | 0.321 | 69 | 0.690 | 2.53 | 0.64 |
| V6 | non_first | opening_0_50 | 559 | 0.290 | 0.490 | 0.220 | 0.023 | 0.345 | 155 | 0.695 | 3.77 | 0.79 |
| V6 | first | mid_50_150 | 1121 | 0.364 | 0.194 | 0.442 | 0.030 | 0.255 | 30 | 0.761 | 4.31 | 0.40 |
| V6 | non_first | mid_50_150 | 1197 | 0.475 | 0.225 | 0.301 | 0.028 | 0.442 | 50 | 0.689 | 10.63 | 1.03 |
| V7 | first | opening_0_50 | 67 | 0.269 | 0.657 | 0.075 | 0.000 | 0.373 | 21 | 0.747 | 2.75 | 0.66 |
| V7 | non_first | opening_0_50 | 299 | 0.348 | 0.411 | 0.241 | 0.017 | 0.375 | 65 | 0.662 | 2.93 | 0.45 |
| V7 | first | mid_50_150 | 251 | 0.418 | 0.195 | 0.386 | 0.012 | 0.335 | 12 | 0.783 | 7.45 | 0.35 |
| V7 | non_first | mid_50_150 | 1084 | 0.409 | 0.148 | 0.444 | 0.036 | 0.271 | 21 | 0.699 | 7.66 | 0.76 |
| V8 | first | opening_0_50 | 121 | 0.116 | 0.579 | 0.306 | 0.041 | 0.215 | 17 | 0.595 | 1.76 | 0.21 |
| V8 | non_first | opening_0_50 | 288 | 0.253 | 0.587 | 0.160 | 0.101 | 0.469 | 51 | 0.622 | 2.48 | 0.53 |
| V8 | first | mid_50_150 | 356 | 0.382 | 0.194 | 0.424 | 0.017 | 0.371 | 10 | 0.680 | 4.39 | 0.42 |
| V8 | non_first | mid_50_150 | 774 | 0.474 | 0.159 | 0.367 | 0.080 | 0.351 | 19 | 0.638 | 7.45 | 0.75 |

Interpretation:

1. V6 non-first games provoke far more direct responses by midgame than V6 wins.
   Once V6 is behind, nearly half its midgame actions target enemies, and
   opponent direct-response density rises sharply.
2. V8 reduces opening commit and direct responses in some cases, but its 4P
   non-first center-target rate rises to `0.101` in opening and `0.080` in
   midgame. The extra multi-size options did not stop it from entering common
   contested space while behind.
3. The problem is not simply "do not attack". V6/V8 wins still attack. The
   difference is whether attacks happen from a stable production base and whether
   the target is holdable/rank-improving.

## Why Openings Lose Naturally

The phrase "lose naturally" matches the replay data. In many 4P non-first games,
the bot follows a locally reasonable sequence:

```text
capture nearby small neutral
use the new source to reach a higher-value or center/frontier target
spend high fraction of local ships
enter a shared reaction zone
opponents respond, defend, or clean up
our production rank drops by step 50
regroup/enemy actions become reactive rather than strategic
```

The issue is not that an individual action is illegal or obviously irrational
under 2P scoring. The issue is that 4P changes the payoff matrix:

```text
An opening move can be positive in isolated capture value but negative in
expected rank value because it creates an exploitable weak front.
```

### V6 example: episode `80696452`

Teams:

```text
muelsyse111 / linrock / SUN / shyjin
```

Phase snapshots:

| Step | Prod | Gap | Rank | Planets | Ships |
|---:|---:|---:|---:|---:|---:|
| 20 | 4 | -7 | 4 | 1 | 90 |
| 50 | 5 | -17 | 4 | 2 | 151 |
| 100 | 0 | -33 | 4 | 0 | 0 |

Key opening decisions:

| Step | Target | Source prod | Target prod | Sent | Commit | Distance | Reaction gap | Close enemies | Later note |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 16 | neutral | 4 | 2 | 67 | 0.91 | 68.3 | -40.1 | 3 | high-risk expansion into shared zone |
| 25 | neutral | 1 | 5 | 52 | 0.98 | 24.8 | 10.4 | 0 | captured at 31, lost at 43 |
| 28 | enemy | 4 | 1 | 51 | 0.93 | 87.0 | -87.0 | 3 | low-holdability enemy pressure |
| 34 | neutral | 2 | 5 | 71 | 0.97 | 32.4 | 5.4 | 1 | captured at 42, lost at 45 |
| 49 | enemy | 2 | 5 | 39 | 0.46 | 15.7 | -15.7 | 1 | captured at 52, lost at 53 |

Code-level read:

```text
V6 inherits V2's candidate scoring plus source reserve and production-gap
selected-action filter. These actions are still plausible because production
targets and attack flow remain attractive. The filter is too late and too
narrow: it sees selected-action risk, but it does not run a true
post-capture/third-party aftermath model before the opening candidate is made.
```

### V7 example: episode `80845404`

Teams:

```text
muelsyse111 / Carbon / istinetz / TONDUCLOI
```

Phase snapshots:

| Step | Prod | Gap | Rank | Planets | Ships |
|---:|---:|---:|---:|---:|---:|
| 20 | 9 | 0 | 1 | 3 | 79 |
| 50 | 0 | -15 | 4 | 0 | 43 |
| 100 | 0 | -27 | 4 | 0 | 0 |

Key opening decisions:

| Step | Target | Source prod | Target prod | Sent | Commit | Distance | Reaction gap | Close enemies | Later note |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 14 | neutral | 3 | 1 | 24 | 0.71 | 96.3 | -69.9 | 3 | far low-value trap |
| 16 | enemy | 3 | 3 | 9 | 0.69 | 83.0 | -83.0 | 3 | early enemy pressure in shared zone |
| 27 | mine/regroup | 3 | 3 | 50 | 0.94 | 12.6 | 27.0 | 0 | own asset later lost at 37 |
| 35 | enemy | 3 | 3 | 56 | 0.92 | 44.4 | -44.4 | 1 | local attack while rank already unstable |
| 37 | enemy | 3 | 3 | 56 | 0.92 | 41.9 | -41.9 | 2 | captured at 45, lost at 50 |

Code-level read:

```text
V7's continuous recovery branch starts at step 35 and depends on being behind by
production/rank. It cannot prevent the step 14-18 far/shared-zone opening. By
the time it becomes active, the game has shifted into a defensive cascade.
```

### V8 example: episode `80840075`

Teams:

```text
kglctf / Light&Thunder / Nawatix / muelsyse111
```

Phase snapshots:

| Step | Prod | Gap | Rank | Planets | Ships |
|---:|---:|---:|---:|---:|---:|
| 20 | 3 | -3 | 3 | 3 | 35 |
| 50 | 5 | -17 | 4 | 4 | 94 |
| 100 | 2 | -42 | 2 | 2 | 24 |
| 150 | 0 | -47 | 2 | 0 | 0 |

Key opening decisions:

| Step | Target | Source prod | Target prod | Sent | Commit | Distance | Reaction gap | Close enemies | Later note |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 32 | neutral | 1 | 5 | 43 | 0.70 | 62.3 | -49.2 | 2 | center/frontier high-prod trap |
| 33 | neutral | 1 | 3 | 14 | 0.74 | 88.7 | -68.7 | 3 | far shared-zone neutral |
| 38 | enemy | 2 | 1 | 31 | 0.94 | 79.3 | -79.3 | 3 | low-holdability enemy pressure |
| 45 | neutral | 1 | 3 | 17 | 0.94 | 97.6 | -81.9 | 3 | far shared-zone neutral |
| 54 | neutral | 2 | 3 | 46 | 0.92 | 70.7 | -56.6 | 3 | recovery still spends into trap |

Code-level read:

```text
V8 adds 60/80/100 percent drain tiers and replay-risk selected-action filtering,
but it still allows risky targets to enter the candidate set. Multi-size drain
can reduce the cost of a bad idea, but it does not make a bad center/frontier
mission good. V8 needs a mission-level veto before candidate scoring, not only
a safer replacement after scoring.
```

## Middle Galaxy / Center Decision

The current center logic is too implicit. Center or middle-galaxy targets are
not always bad, but they are public goods with high third-party reaction value.

Do not enter center/frontier in opening unless:

```text
my_eta + hold_margin < min_enemy_eta
and close_enemy_count <= 1
and post_capture_garrison survives one response window
and source keeps enough reserve to not become the cheapest victim
and the target materially improves production rank by step 50
```

If this fails, the action is a "public sacrifice":

```text
I pay the capture cost.
Someone else gets the cleanup option.
Two neighbors learn that my source is depleted.
The production leader grows because I am fighting in the commons.
```

## Leader Growth / Midgame Intervention

The user asked whether we should notice the strongest opponent growing due to
another player's mistake.

Replay evidence supports this, but only with a holdability gate.

Bad intervention:

```text
attack low-production leader-owned rear planet
reaction_gap < 0
target cannot be held
source is depleted
result: leader or third party captures aftermath; we lose rank
```

Good intervention:

```text
leader production gap is increasing at step 50/100
target is a leader high-production/frontier asset
our ETA is not worse than nearby enemies
post-capture garrison survives at least one response
the action also improves our rank, not just damages the leader
```

This needs a leader-trajectory model:

```text
leader_prod_gap_20_50
leader_prod_gap_50_100
leader_planet_gain
leader_nearby_enemy_mistake: enemy launched away from leader-front, leaving
  leader-facing high-prod asset underdefended
```

## Why V7/V8 Failed To Replace V6

V7 failure:

```text
The recovery filter starts too late and is selected-action only. It cannot
prevent opening missions that create the step-50 collapse. Official score 920.2
confirms it is not a candidate.
```

V8 failure:

```text
V8 helps some visible 2P and low-risk 4P cases, but 4P non-first games still
fall behind by step 50/100. The center/opening risk rate rises in V8 non-first
games. Multi-size drain and top-candidate trace are useful tooling, but they are
not a full FFA mission policy.
```

V6 remains best because:

```text
It preserves Alyce/V2 tempo and changes less. It still has the same 4P collapse
pattern, but it damages fewer strong cases than V7/V8.
```

## Required 4P Decision Nodes For Next Version

The next candidate should not be "V8 with another threshold." It should be a
4P mission router before final scoring.

### Node 1 - Opening Safe Expansion

Applies:

```text
step < 35
player_count == 4
```

Decision:

```text
Prefer safe local production and backline orbit assets.
Reject far/center targets unless holdability gate passes.
Reject early enemy targets unless they are immediate threat-neighbor defense or
free rank-improving capture.
```

Hard checks:

```text
reaction_gap >= 4 for ordinary neutral
close_enemy_count <= 1
target_center_dist > 25 unless safe/holdable
source_post_send >= reserve_floor(source_prod, pressure)
```

### Node 2 - Contested Center / Middle Galaxy

Applies:

```text
35 <= step < 90
target_center_dist <= 30 or close_enemy_count >= 2
```

Decision:

```text
Do not single-source full-send into center.
Allow center only if multi-source timing arrives together and post-capture
garrison survives the nearest enemy response.
Otherwise choose regroup/frontier-safe alternative.
```

### Node 3 - Anti-Focus / Reputation Control

Applies:

```text
4P opening and midgame
```

Decision:

```text
Avoid becoming the cheapest target for two players.
```

Signals:

```text
source_depletion_ratio > 0.75
two enemies can hit source/target within response window
recent direct attacks on us are rising
our prod_rank >= 3 and enemy action rate toward us is high
```

Effect:

```text
raise reserve floor
prefer mine/regroup/frontier consolidation
disable low-impact enemy attacks
```

### Node 4 - Leader Trajectory Intervention

Applies:

```text
step 50-150
leader production gap widening
another player has just overcommitted or abandoned a leader-facing front
```

Decision:

```text
Attack leader only if the target is high production, frontier-relevant, and
holdable. Otherwise recover production and avoid kingmaking.
```

### Node 5 - Trailing Recovery

Applies:

```text
prod_rank >= 3 or prod_gap <= -6
```

Decision:

```text
No low-impact enemy targets.
No far neutrals with negative reaction gap.
Only actions that improve production rank, protect survival, or hit a holdable
leader asset.
```

## Implementation Route

Recommended next branch:

```text
alyce_v9_4p_mission_router
base: V6, not V7/V8
```

Keep from V8:

```text
candidate trace labels
phase snapshot analyzer
multi-size candidate infrastructure only if the mission is already valid
```

Discard as primary policy:

```text
V7/V8 continuous selected-action recovery as the main fix
```

Add before candidate scoring:

```text
1. 4P reaction map for every candidate target.
2. center/frontier danger label.
3. opening safe-expansion gate.
4. anti-focus source reserve gate.
5. leader trajectory and rank-improvement labels.
6. holdability veto for center/enemy targets.
```

Validation gates before another submit:

```text
1. V9 vs V6 local smoke: no errors/timeouts.
2. Replay-inspired cases from V6/V7/V8 worst episodes listed above.
3. 4P rotated local screen with phase snapshots, not just final win count.
4. Confirm fewer opening risky center/shared-zone actions than V6/V8.
5. Confirm step50/100 production gap improves in replay-inspired cases.
6. Do not submit unless V9 preserves V6 2P and does not reduce V6-like safe wins.
```

## Current Decision

```text
Do not promote V7 or V8.
Keep V6 as official best.
Use this review to design a V9 4P mission router.
```
