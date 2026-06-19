# Alyce 4P FFA V2 Official Replay Review - 2026-06-19

## Scope

This review covers the official Kaggle submission:

```text
submission_id: 53827977
message: alyce_4p_ffa_v2_soft_contested_filter_20260619
public_score: 600.0
status: COMPLETE
```

The purpose is to analyze the actual V2 official games, not local tournament
games, and identify why the V2 line underperformed the current official best
`alyce_intruder_repro_20260618` score `1062.9`.

## Markdown / GitHub Completeness Check

Before this review, the Orbit Wars repository was clean:

```text
git status -sb
## main...origin/main
```

Markdown check:

```text
tracked md files: 100
workspace md files excluding ignored directories: 101
untracked difference: pytest_cache/README.md
```

No project report markdown was missing from Git. The only untracked markdown
found was `pytest_cache/README.md`, which is cache/tooling output and not a
repository report.

## Downloaded Replays

Command source:

```text
kaggle competitions episodes 53827977 -v
kaggle competitions replay <episode_id> -p D:\orbitwars_replays\alyce_4p_ffa_v2_latest\episodes
```

Local replay root:

```text
D:\orbitwars_replays\alyce_4p_ffa_v2_latest
```

Generated local analysis files:

```text
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\submission_53827977_episodes.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\episode_ids.txt
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_episode_summary.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_action_events.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_key_snapshots.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_phase_summary.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_analysis_summary.json
```

Downloaded:

```text
total replay files: 27
public episodes: 26
validation self-play episodes: 1
```

The replay JSON contains observations and actions. It does not contain the
agent's internal planner logs, candidate scores, or exact branch trace. Any
"decision cause" below is therefore a code-and-action inference, not a private
runtime log.

## Result Summary

Public official episodes only:

| Mode | Wins | Losses | Notes |
|---|---:|---:|---|
| 2P | 10 | 4 | 2P losses often begin after apparently good early expansion. |
| 4P | 8 | 4 | 4P losses show earlier production collapse by step 50-100. |
| Combined | 18 | 8 | Official score still low because ladder rating depends opponent quality and all episodes. |

Validation:

```text
episode 80588533: V2 self-play, player 1 beat player 0.
```

This confirms that self-play is not a guaranteed draw. Symmetric code can
diverge because seat position, map geometry, tie-breaking, and action timing
create asymmetric target selections.

## Phase-Level Signals

The most useful signal is not raw win count. It is the phase difference between
winning and losing games.

### Production Gap

Average production gap to leader:

| Step | 4P wins | 4P losses | Interpretation |
|---:|---:|---:|---|
| 20 | -1.50 | 0.00 | Opening can look acceptable even in future losses. |
| 50 | -3.00 | -8.75 | Losses begin falling behind by first consolidation. |
| 100 | -1.75 | -23.75 | All sampled 4P losses are behind by step 100. |
| 150 | 0.00 | -45.50 | Surviving loss samples are already strategically dead. |

2P losses behave differently:

| Step | 2P wins | 2P losses |
|---:|---:|---:|
| 50 | 0.00 | 0.00 |
| 100 | 0.00 | -6.00 |
| 200 | 0.00 | -21.33 |

This means the 4P issue is earlier and more severe. The 2P issue is more often
midgame conversion after an initially decent expansion.

### Action Mix

Per player-phase average from inferred targets:

| Phase | Outcome | Enemy rate | Neutral rate | Mine/regroup rate | Notes |
|---|---|---:|---:|---:|---|
| opening 0-50 | win | 0.184 | 0.606 | 0.209 | Normal expansion heavy opening. |
| opening 0-50 | loss | 0.231 | 0.619 | 0.149 | Losses already hit enemies more and regroup less. |
| 50-150 | win | 0.359 | 0.238 | 0.403 | More consolidation/regroup in wins. |
| 50-150 | loss | 0.473 | 0.242 | 0.284 | Losses over-index on enemy targets. |
| 150-300 | win | 0.247 | 0.192 | 0.561 | Winners consolidate and move mass internally. |
| 150-300 | loss | 0.446 | 0.162 | 0.392 | Losing midgame keeps attacking while weakened. |

The visible pattern is consistent:

```text
loss = higher enemy-target rate + lower mine/regroup rate + weaker production conversion
```

The action target inference is approximate: target is estimated from source,
angle, and nearest angular match. It is good enough for aggregate behavior, but
not exact mission labeling.

## Key Losing Episodes

### Episode 80598044 - 4P Early Collapse

Teams:

```text
w...123456 | Nabid Nur | muelsyse111 | INV
our index: 2
winner: INV
turns: 111
```

Key snapshots:

| Step | Our production | Rank | Gap to leader | Planets |
|---:|---:|---:|---:|---:|
| 20 | 15 | 1 | 0 | 4 |
| 50 | 4 | 4 | -24 | 2 |
| 100 | 0 | 3 | -58 | 0 |

Critical inferred actions:

| Step | Action |
|---:|---|
| 12 | From source 8 to far neutral prod 1, distance 100.18, 24 ships. |
| 13 | From source 2 to far enemy prod 2, distance 69.00, 16 ships. |
| 27 | Two enemy attacks while still rank 1 production. |
| 47-50 | More far low-value targets after production already collapsed. |

Interpretation:

V2 starts well, then spends early tempo on distant or enemy targets instead of
locking down the production lead. By step 50 the production base is already
mostly gone.

### Episode 80598085 - 4P Far Low-Value Neutral Loop

Teams:

```text
Daniel Bekker | muelsyse111 | Love Mathur | Eissam.0
our index: 1
winner: Daniel Bekker
turns: 140
```

Key snapshots:

| Step | Our production | Rank | Gap to leader | Planets |
|---:|---:|---:|---:|---:|
| 20 | 8 | 1 | 0 | 3 |
| 50 | 13 | 2 | -5 | 4 |
| 100 | 5 | 3 | -23 | 1 |

Critical inferred actions:

| Step | Action |
|---:|---|
| 19-20 | Repeated far neutral prod 1 at distance 93.01. |
| 25 | Far low-value neutral and far low-value enemy while production drops to rank 4. |
| 27-32 | More low-value neutral expansion despite unstable front. |

Interpretation:

This is exactly the failure pattern that a soft far-low neutral penalty was
intended to catch. The penalty must be narrow because some far targets are still
valuable, but prod 1 at 80-100 distance in early 4P is usually bad tempo.

### Episode 80602917 - 4P Delayed Collapse

Teams:

```text
Fallen player | Doug | onThoze | muelsyse111
our index: 3
winner: onThoze
turns: 187
```

Key snapshots:

| Step | Our production | Rank | Gap to leader | Planets |
|---:|---:|---:|---:|---:|
| 20 | 13 | 1 | 0 | 3 |
| 50 | 20 | 2 | -6 | 5 |
| 100 | 39 | 2 | -4 | 10 |
| 150 | 24 | 2 | -34 | 6 |

Critical inferred actions:

| Step | Action |
|---:|---|
| 18 | Enemy prod 2 at distance 45.87. |
| 26 | Neutral prod 1 at distance 108.42. |
| 76-96 | Several far low-value enemy attacks as production lead turns into deficit. |

Interpretation:

This is not an opening-only problem. V2 can reach a strong midgame and still
convert it into a loss by attacking far low-value assets instead of defending or
consolidating high-production territory.

### Episode 80592336 - 2P Overextension After Strong Expansion

Teams:

```text
LevelUp Vinay | muelsyse111
our index: 1
winner: LevelUp Vinay
turns: 500
```

Key snapshots:

| Step | Our production | Rank | Gap to leader | Planets |
|---:|---:|---:|---:|---:|
| 20 | 6 | 1 | 0 | 3 |
| 50 | 31 | 1 | 0 | 13 |
| 100 | 28 | 2 | -6 | 11 |
| 200 | 8 | 2 | -46 | 3 |

Critical inferred actions:

| Step | Action |
|---:|---|
| 23 | Neutral prod 1 at distance 89.51. |
| 37 | Multiple far enemy prod 2 targets at 95+ distance. |
| 46-51 | Repeated far low-value neutral/enemy actions. |

Interpretation:

2P does not use the V2 4P mission filter, so these losses are not caused by
the 4P filter itself. They come from the older V2 base planner structure: one
safe-drain size per source-target candidate and insufficient target-quality
control.

## Code-Level Cause

Relevant files:

```text
agents/variants/alyce_4p_ffa_v2/main.py
agents/variants/alyce_4p_ffa_v2/orbit_lite/planner_core.py
```

### 1. V2 Is Still The Older Light-Derived Planner

In `plan_lite_waves`, V2 uses:

```text
drain = safe_drain(...)
sizes = drain.view(S, 1).expand(S, T).floor().clamp(min=1.0)
```

That means each source-target candidate is basically one full safe-drain size.
It does not use the full Intervention v15 multi-option set:

```text
full safe-drain
floor-sized fleet
0.5 drain
0.75 drain
1.0 drain
```

So when V2 chooses a questionable target, it often commits too much tempo to
that target.

### 2. 4P Mission Filter Is Too Narrow In The Wrong Places

V2 4P filter enables:

```text
enable_ffa_mission_filter=True
```

It handles:

- severe trap neutral veto;
- soft contested neutral penalty;
- safe neutral bonus;
- source depletion penalty;
- leader asset bonus;
- low-value rear enemy penalty;
- nearby threat bonus.

But it does not directly penalize:

```text
far prod-1 neutral targets
```

unless they are also contested/trapped by enemy ETA. Many bad replay actions are
not necessarily "contested"; they are simply poor tempo because they are far
and low production.

### 3. Low-Value Enemy Penalty Can Be Overridden

V2 has:

```text
low_value_rear = enemy target, not leader, prod <= 2, eta > ffa_enemy_rear_eta
rear_penalty = 5.0 + eta * 0.5
```

But enemy low-value attacks can still survive when:

- the target belongs to the current leader;
- the target is treated as a nearby threat neighbor;
- the base competitive score is high enough;
- replay target inference points to a low-value planet but the internal planner
  aimed for an intercept path near another moving target.

This explains why the report should not claim every far-low action is a direct
filter bug. The confirmed issue is that the visible behavior is too willing to
spend tempo there.

### 4. Dynamic ROI Can Amplify Bad States

V2 `_adjust_config` lowers ROI and increases waves when behind:

```text
if ratio < 1.0: lower roi_threshold
if ratio < 0.70: add waves
```

This is reasonable in principle, but in losing games it can amplify bad
attacks after the agent is already behind. In other words, the planner becomes
more willing to fire, but the target-quality layer is not strong enough to
ensure those extra actions are the right actions.

### 5. Regroup Exists But Is Underselected In Losses

The aggregate behavior shows lower mine/regroup rate in losses:

```text
50-150 wins: mine/regroup rate 0.403
50-150 losses: mine/regroup rate 0.284
150-300 wins: mine/regroup rate 0.561
150-300 losses: mine/regroup rate 0.392
```

This suggests the issue is not "regroup missing from code"; it is that attack
candidates still outscore regroup candidates too often in bad positions.

## Why V2 Official Score Was Poor

The official replay evidence supports the earlier local finding:

```text
V2 is not a good final line.
```

The primary failure is not package/runtime. It is strategy structure:

1. V2 is weaker than full Alyce Intervention because it lacks multi-size
   candidate selection.
2. It can win many low/mid official episodes, but loses enough higher-quality
   matchups to rate poorly.
3. 4P losses are decided early by production conversion failure.
4. 2P losses show that the issue is broader than the 4P filter.
5. The filter tries to solve "contested neutral" but the actual replay problem
   is more often "low-value remote tempo sink" and "attack over regroup".

## Optimization Direction

Do not keep tuning V2 as the main candidate.

Recommended next line:

```text
Base: full Alyce Intervention / ProducerLite v15
Change type: candidate scoring only
No hard action deletion
No global reserve layer
No post-hoc wrapper moves
```

For the next code attempt:

1. Add trace counters for candidate penalties:
   - far low neutral penalty count;
   - far low enemy penalty count;
   - selected action changed count;
   - phase/step of changed action.
2. Make far-low penalties softer than V3:
   - `far_enemy_penalty` around `1.0-1.5`, not `3.5`;
   - apply mainly before step `180`;
   - do not penalize high-production or leader assets.
3. Add production-state gating:
   - if already trailing in 4P by production, prefer regroup/near high-prod
     defense over remote low-value attacks;
   - if leading, do not bleed lead into far prod-1 targets.
4. For 2P, do not enable 4P-specific FFA logic, but consider a very small
   generic far prod-1 neutral penalty because V2 2P losses also show that
   pattern.
5. Validate on official replay-inspired local pools before another Kaggle
   submit.

## Current Decision

No Kaggle submission was made in this review.

V2 remains rejected:

```text
official score: 600.0
do not promote
do not resubmit unchanged
```

The next implementation should be an evidence-gated V4/V3b on top of full
Alyce Intervention, not more patching of the V2 branch.
