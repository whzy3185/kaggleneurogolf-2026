# Alyce V9 Official Replay + Code/Discussion Refresh - 2026-06-21

## Scope

User requested:

```text
1. Download and fully analyze V9 official games.
2. Re-upload V6 once.
3. Check Kaggle Code and Discussion for new ideas.
```

No code change is made in this report.

## Official Submission State

Latest CLI query during this review:

| Submission | Message | Status | Public score |
|---:|---|---|---:|
| `53907214` | `alyce_v6_prod_gap_mode_resubmit_after_v9_5da551f` | `SubmissionStatus.PENDING` | n/a |
| `53904277` | `alyce_v9_4p_mission_router_de5bd16` | `SubmissionStatus.COMPLETE` | `1081.3` |
| `53852919` | `alyce_v6_prod_gap_mode_1db7614` | `SubmissionStatus.COMPLETE` | `1177.8` |

Conclusion: V9 is rejected as a promotion candidate. The current completed
official best remains V6 at `1177.8`. V6 was re-uploaded as requested and is
pending at the time of this report.

## V9 Replay Download

Local replay root:

```text
D:\orbitwars_replays\alyce_v9_latest
```

Downloaded files:

```text
D:\orbitwars_replays\alyce_v9_latest\analysis\submission_53904277_episodes.csv
D:\orbitwars_replays\alyce_v9_latest\analysis\episode_ids.txt
D:\orbitwars_replays\alyce_v9_latest\episodes\episode-*.json
```

Visible episode count:

```text
public episodes: 27
validation episodes: 1
total replay files: 28
```

Commands:

```text
kaggle competitions episodes 53904277 -v
kaggle competitions replay <episode_id> -p D:\orbitwars_replays\alyce_v9_latest\episodes
python scripts\analyze_4p_game_theory_replays.py --input v9=D:\orbitwars_replays\alyce_v9_latest\episodes --output-dir D:\orbitwars_replays\alyce_v9_latest\analysis --include-validation
python scripts\analyze_4p_game_theory_replays.py --input v6=D:\orbitwars_replays\alyce_v6_latest\episodes --input v8=D:\orbitwars_replays\alyce_v8_latest\episodes --input v9=D:\orbitwars_replays\alyce_v9_latest\episodes --output-dir D:\orbitwars_replays\alyce_v689_comparison --include-validation
```

Analysis outputs:

```text
D:\orbitwars_replays\alyce_v9_latest\analysis\game_theory_episode_summary.csv
D:\orbitwars_replays\alyce_v9_latest\analysis\game_theory_phase_snapshots.csv
D:\orbitwars_replays\alyce_v9_latest\analysis\game_theory_action_events.csv
D:\orbitwars_replays\alyce_v9_latest\analysis\game_theory_summary.json
D:\orbitwars_replays\alyce_v689_comparison\game_theory_summary.json
```

Replay limitation: official replay JSON exposes observations and final submitted
actions. It does not expose internal candidate scores or which V9 penalty fired.
Target labels below are inferred from source planet, launch angle, and nearest
angular planet at the action step.

## V9 Public Replay Summary

V9 public sample:

| Mode | First | Non-first | Total |
|---|---:|---:|---:|
| 2P | 6 | 4 | 10 |
| 4P | 6 | 11 | 17 |

Aggregate:

```text
avg_final_prod: 25.3333
avg_final_prod_rank: 1.5556
avg_final_ships: 1118.6296
```

The simple first-place rate is not the official score. Official score depends on
opponent quality, rating uncertainty, match order, and 2P/4P mix.

## V9 vs V6/V8 Phase Comparison

The important comparison is 4P non-first games because those drive most observed
collapses.

| Variant | Public 4P episodes | 4P first | 4P non-first | 4P non-first step50 prod/gap/rank | 4P non-first step100 prod/gap/rank |
|---|---:|---:|---:|---|---|
| V6 | 34 | 11 | 23 | `9.35 / -6.87 / 2.78` | `7.22 / -19.39 / 2.87` |
| V8 | 12 | 3 | 9 | `9.89 / -9.78 / 3.11` | `9.00 / -28.56 / 2.56` |
| V9 | 17 | 6 | 11 | `11.91 / -5.73 / 2.55` | `8.09 / -23.73 / 2.82` |

Interpretation:

```text
V9 improved the step50 4P non-first production gap versus V6/V8.
V9 did not preserve that gain through step100.
V9 is better than V8 on this metric, but still worse than V6 in official score.
The mission router delays or softens the early collapse in some games, but it
does not solve the durable-production conversion problem.
```

2P non-first comparison:

| Variant | 2P non-first step50 prod/gap/rank | 2P non-first step100 prod/gap/rank |
|---|---|---|
| V6 | `24.12 / -2.29 / 1.41` | `23.06 / -11.94 / 1.82` |
| V9 | `20.75 / -1.75 / 1.25` | `23.00 / -16.75 / 2.00` |

Interpretation:

```text
V9 did not intentionally change 2P, but the packaged branch still shows worse
2P loss separation at step100 in this sample. Treat this as a warning against
shipping broad mission filters without isolating 2P behavior.
```

## V9 Action Mix

V9 public actions by phase:

| Phase | Enemy | Neutral | Mine | Center target rate | Third-party cleanup risk |
|---|---:|---:|---:|---:|---:|
| opening 0-50 | 29.02% | 44.84% | 26.13% | 6.74% | 26.27% |
| mid 50-150 | 35.46% | 16.31% | 48.22% | 7.02% | 20.46% |
| late-mid 150-300 | 20.70% | 13.33% | 65.96% | 1.75% | 1.40% |
| end 300-500 | 7.26% | 16.13% | 76.61% | 0.40% | 0.00% |

Compared with V6:

```text
V6 opening third-party cleanup risk: 14.06%
V9 opening third-party cleanup risk: 26.27%

V6 mid third-party cleanup risk: 9.75%
V9 mid third-party cleanup risk: 20.46%
```

This is the clearest V9 regression. The mission router penalized some bad public
targets, but the final selected action stream still contains too many moves
where multiple enemies are close enough to respond or clean up. In game-theory
terms, V9 still creates public-good opportunities for other players: we spend
ships, a third party harvests the weakened target or punishes our depleted
source.

## Representative Failure Patterns

### Episode `135017dc-6d3e-11f1-83e5-0242ac130205`

4P non-first. Key snapshots:

```text
step50: our_prod 9, prod_gap -17, prod_rank 3
step100: our_prod 0, prod_gap -38, prod_rank 4
```

Opening actions include repeated long-distance launches with very negative
reaction gaps:

```text
step 3: neutral prod2, distance 78.09, reaction_gap -45.42, close enemies 2
step 10: neutral prod4, distance 45.46, reaction_gap -22.15, close enemies 1
step 19: neutral prod5, distance 34.31, reaction_gap -15.97, close enemies 2
step 30: neutral prod1, distance 88.29, reaction_gap -73.05, close enemies 3
step 31-43: repeated enemy/neutral long sends from the same source region
```

This is exactly the failure the V9 router was supposed to reduce. The reason it
still appears is likely that V9 penalties are applied at candidate scoring time,
but the base planner still has alternative long/frontier/regroup actions that
look locally valid after the worst candidate is suppressed.

### Episode `dee61412-6d45-11f1-8d5e-0242ac130202`

4P non-first. Key snapshots:

```text
step50: our_prod 14, prod_gap -12, prod_rank 4
step100: our_prod 7, prod_gap -70, prod_rank 2
```

This episode shows early expansion and pressure mixed together:

```text
step 4-9: repeated neutral attempts, including prod5/2 at long distance
step 18-33: many enemy launches with reaction_gap equal to negative distance
step 35-80: repeated enemy and mine traffic while multiple enemies are close
```

The problem is not simply "too much expansion" or "too much attack"; it is
uncommitted mission identity. V9 opens several fronts, then shifts into pressure
and recapture traffic before the early production base is stable.

## Root Cause

V9's core idea was reasonable:

```text
4P should avoid public sacrifice, contested center traps, bad leader pressure,
and low-value attacks on trailing players.
```

Official replay says the implementation is incomplete:

```text
1. The filter is mostly punitive; it suppresses some bad choices but does not
   reliably create a positive safe-frontier replacement mission.
2. Candidate-level penalties are too late in the pipeline. The final action can
   still be a different risky launch from the same depleted source or same
   public-risk region.
3. Enemy/neutral/mine traffic remains too mixed in the first 80 turns. A 4P
   player needs a coherent early posture: safe production first, avoid becoming
   the shared target, then intervene when leader growth is visible.
4. V9 increases inferred third-party cleanup risk versus V6. That explains why
   local step50 improvement did not translate into official score.
```

## Code区 Refresh

Kaggle Code queried:

```text
kaggle kernels list --competition orbit-wars --sort-by dateRun --page-size 20
kaggle kernels list --competition orbit-wars --sort-by scoreDescending --page-size 25
kaggle kernels list --competition orbit-wars --search "meta snapshot" --sort-by dateRun --page-size 20
kaggle kernels list --competition orbit-wars --search "replay" --sort-by dateRun --page-size 20
```

Pulled notebooks into ignored `external/`:

```text
external/kaggle_notebooks/pilkwang__orbit-wars-meta-snapshot-0621
external/kaggle_notebooks/slawekbiel__am-i-in-the-top-10-replays-yet
external/kaggle_notebooks/evgendvorkin__orbit-wars-v8-max-1250-score
external/kaggle_notebooks/amgedalfaqih__apex-hybrid-dynamic-ring-control-border-defense
```

### `pilkwang/orbit-wars-meta-snapshot-0621`

URL:

```text
https://www.kaggle.com/code/pilkwang/orbit-wars-meta-snapshot-0621
```

Key idea:

```text
Role-split submission portfolio, not a single universal agent.
```

Notebook variants:

| Variant | Claimed role |
|---|---|
| `PRIMARY_PLAYERCOUNT_4P_FIX` | high-ceiling primary with strong 4P seat spread |
| `CHALLENGER_R_K_WAVE_COMPLEMENT` | mid-size wave complement that wins different 2P games while preserving 4P |
| `BACKUP_FRONTIER_SHORTLIST` | safer all-around fallback |
| `BACKUP_LIGHT_2P_CONTROL` | intruder-style 2P control, weaker 4P |

This is directly relevant. Our repeated attempts tried to force one modified
agent to cover all modes. The public meta snapshot suggests portfolio
decorrelation matters: use separate active profiles or at least explicitly
separate 2P control, 4P primary, and fallback frontier behavior.

### `slawekbiel/am-i-in-the-top-10-replays-yet`

URL:

```text
https://www.kaggle.com/code/slawekbiel/am-i-in-the-top-10-replays-yet
```

Key idea:

```text
Use the public top-10% replay datasets to count where your team appears and
which opponents you face most often, without fully unzipping every replay.
```

This reinforces a measurement gap in our workflow. We currently download own
episodes, but do not routinely compare our episode distribution against daily
top-10% replay datasets. That should be added before another strategic rewrite.

### `evgendvorkin/orbit-wars-v8-max-1250-score`

URL:

```text
https://www.kaggle.com/code/evgendvorkin/orbit-wars-v8-max-1250-score
```

The notebook contains a large standalone rule/search system. High-value ideas
visible in code:

```text
world model and forward projection
enemy race ETA for neutrals
mode detection
4P opponent profile update
defense coalition
comet evacuation
anti-snipe veto
neutral tempo gate
endgame ROI gate
launch blackout
counter-snipe planning
coalition expansion
hammer and multiprong attack modes
deterministic tie-break hash
```

This points away from another small scoring penalty. The useful transferable
idea is not one parameter; it is a staged planner with a single point of truth
for committing fleets, explicit target locks, and forward checks before a launch.

### `AmgedAlfaqih/apex-hybrid-dynamic-ring-control-border-defense`

URL:

```text
https://www.kaggle.com/code/AmgedAlfaqih/apex-hybrid-dynamic-ring-control-border-defense
```

Visible ideas:

```text
dynamic ROI curve
elastic/shrinking ring conquest
KNN source selection per target
committed-fleet penalty
border planet defense boost
proactive defense with doomed/savable split
comet boost
player-count-specific configs
```

Several of these overlap with our V9 intent. The important difference is that
the notebook defines source/target mission structure earlier in the planner,
whereas our V9 is still mostly a candidate penalty layer.

## Discussion区 Refresh

Queried:

```text
kaggle competitions topics list orbit-wars -s recent -v
kaggle competitions topics list orbit-wars -s top -v
kaggle competitions topics list orbit-wars -s active -v
kaggle competitions topic-messages orbit-wars <topic_id> -n -1 -v
```

Local cached discussion CSV:

```text
external/kaggle_discussions_recent_20260621.csv
external/kaggle_discussions_top_20260621.csv
external/kaggle_discussions_active_20260621.csv
external/kaggle_discussion_709418_4p_20260621.csv
external/kaggle_discussion_710613_agents_20260621.csv
external/kaggle_discussion_708962_score_drop_20260621.csv
external/kaggle_discussion_704741_lessons_20260621.csv
```

### `Most of the games now are 4 players`

URL:

```text
https://www.kaggle.com/competitions/orbit-wars/discussion/709418
```

Important signal:

```text
The scheduler emits 50/50 2P/4P games, but because 4P games have twice as many
seats as 2P games, an individual submission can observe more 4P seats. Several
users reported early-run imbalance and large early Elo swings.
```

Actionable consequence:

```text
Do not optimize only for raw 50/50 game count. Treat 4P as disproportionately
important for early rating trajectory and data collection.
```

### `Why are 3 agents shown on my leaderboard entry?`

URL:

```text
https://www.kaggle.com/competitions/orbit-wars/discussion/710613
```

Signal:

```text
Leaderboard active-agent counts can temporarily show multiple agents; one user
reported it returned to normal after resubmission.
```

Actionable consequence:

```text
Repeated submissions may affect visible active-agent bookkeeping. We should
track submission ids and scorecard state carefully, but this discussion does
not prove a strategy change by itself.
```

### `Why did the scores drop so much today?`

URL:

```text
https://www.kaggle.com/competitions/orbit-wars/discussion/708962
```

Signals:

```text
Official reply: no backend changes.
Users report score drops due to improving field and variance.
One high-ranked participant says they use RL.
Another comment says rule-based Producer has some luck/variance.
```

Actionable consequence:

```text
Treat score drift as live-meta movement. A single official score snapshot is
not enough; compare replay behavior and repeated score trajectory.
```

### `Lessons learned so far in this competition`

URL:

```text
https://www.kaggle.com/competitions/orbit-wars/discussion/704741
```

Signals:

```text
PPO/RL can train to high leaderboard scores when curriculum/opponent/eval are
right.
For heuristic work, public advice is to incorporate solving/optimization
problems rather than static hand-coded rules.
Behavior cloning top replays can fit typical moves but may fail to clone the
lookahead/search structure.
```

Actionable consequence:

```text
For our current rule-based path, the next useful step is a small optimizer or
forward-check gate, not another static penalty.
```

## V6 Re-upload

User requested uploading V6 again.

Package:

```text
dist/alyce_v6_prod_gap_mode_20260619.tar.gz
sha256: 8F64DE7C6FA6817C568F70547DCEB5FAF6A2933AD56D1CC54B9372AB333B126F
size_bytes: 59857
```

Command:

```text
kaggle competitions submit -c orbit-wars -f dist\alyce_v6_prod_gap_mode_20260619.tar.gz -m "alyce_v6_prod_gap_mode_resubmit_after_v9_5da551f"
```

Immediate result:

```text
submission_id: 53907214
status: SubmissionStatus.PENDING
public_score: n/a
```

## Next Optimization Route

Do not continue V9 as-is.

Next branch should be based on V6 and should avoid broad suppressive penalties.
The evidence supports this route:

```text
1. Add a positive safe-frontier mission, not just public-risk penalties.
2. Move risk checks earlier than final candidate scoring:
   source -> mission -> target -> commit, with a target lock/commit ledger.
3. Add a forward-check gate for 4P public targets:
   "after our launch, who can arrive before/soon after us and profit?"
4. Add explicit 4P active-seat posture:
   early production survival, avoid public sacrifice, intervene only when the
   leader gap becomes concrete.
5. Keep 2P isolated. V9's score and replay sample show that 4P filters can
   still harm or fail to preserve 2P behavior.
6. Add top-10% replay dataset tracking to measure whether our games resemble
   strong-player replays rather than only our own losses.
7. Consider a portfolio approach:
   V6-like official-best profile, a 4P seat-spread profile, and a 2P wave/control
   complement. Pilkwang's 0621 snapshot explicitly frames the meta this way.
```

Immediate no-go list:

```text
do not submit V9 again
do not add more scalar penalties without trace counters
do not optimize against local 4P family self-play only
do not collapse 2P and 4P into one shared mission policy
```
