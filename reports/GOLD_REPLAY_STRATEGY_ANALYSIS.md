# High-Rank Replay Strategy Analysis

Date: 2026-06-16

Gold replay status: skipped as gold analysis.

Reason: final gold teams do not exist yet on 2026-06-16, so no gold-medal
strategy claims are made from unseen or non-final gold replays.

This report analyzes a small set of visible current high-rank public replays
downloaded from the official daily replay dataset. The analysis is descriptive
and approximate; it does not infer private code.

## Replay Sample

Source: `kaggle/orbit-wars-episodes-2026-06-15`

Downloaded sample files under ignored `replays/audit/daily_sample/`:

| Episode | Players | Winner by reward | Current high-rank teams included |
|---:|---|---|---|
| 79968955 | Jake Will, Ender, Hober Malloc, Isaiah @ Tufa Labs | Jake Will | rank 1, 2, 4, 7 |
| 79968870 | Boey, CPMP, Radek Osmulski, aaa | Radek Osmulski | rank 6, 24, 53 |
| 79968841 | flg, ma name, Roche Overflow, Abhyuday | flg | rank 8, 38, 30, 37 |
| 79968923 | Gregor Lied, vkhydras, 213tubo, bowwowforeach | 213tubo | rank 12, 13, 23, 26 |
| 79968910 | bowwowforeach, CPMP, Man Penguin, luckyappley | luckyappley | rank 23, 24 |

Feature JSONL was written to ignored:

```text
outputs/replay_features/high_rank_replay_features_20260616.jsonl
```

## Extraction Method

The extractor used only public replay fields:

- per-step actions
- per-step observations
- planet ownership/garrison/production
- `info.TeamNames`
- rewards/statuses

Approximation limits:

- Target is estimated by matching each action's source+angle ray to the nearest
  current planet. Moving target interception means some target assignments can
  be off by one or more turns.
- Defense is approximated as sending to a currently friendly planet.
- Multi-source attack is same-step, same-player, multiple-source sends toward
  the same estimated target.
- Counter/recapture is inferred from ownership transitions within a short
  window, not from private intention.
- Episodes ended before turn 300, so late-game 300-500 analysis is unavailable
  for this sample.

## Opening First 50 Turns

Observed high-rank opening traits:

1. Early neutral capture is selective, not pure nearest spam.
   The sampled high-rank players usually captured 2-5 neutral planets by turn
   50.

2. First enemy attacks are often early but not immediate.
   In the current top-1/top-2/top-4/top-7 replay `79968955`, first estimated
   enemy attack turns were:
   - Jake Will: 27
   - Ender: 30
   - Hober Malloc: 23
   - Isaiah @ Tufa Labs: 27

3. Launch commit ratios are high.
   In `79968955`, average commit ratio was about 0.89-1.00 for the four
   high-rank players. This looks more like floor/capture-sized committed
   launches than tiny probing.

4. High-production target preference is visible.
   In `79968955`, estimated high-production target ratios:
   - Jake Will: 0.5106
   - Ender: 0.6429
   - Hober Malloc: 0.6264
   - Isaiah @ Tufa Labs: 0.5469

5. Center-target ratio was low in this sample.
   Most sampled players had near-zero center target ratio by the ray-target
   metric. That does not prove center control is unimportant; it only means
   these public replays did not show center-first openings under this metric.

## Mid Game 50-300

The episodes ended before 300 turns, but most action happened in the 50-205
range.

Replay `79968955`:

| Team | Defense/reinforce approx | Multi-source approx | Comet actions approx | Recapture/counter approx | Target switching | Mid actions |
|---|---:|---:|---:|---:|---:|---:|
| Jake Will | 30 | 0 | 4 | 7 | 32 | 82 |
| Ender | 4 | 0 | 0 | 0 | 5 | 4 |
| Hober Malloc | 35 | 1 | 2 | 4 | 27 | 45 |
| Isaiah @ Tufa Labs | 24 | 1 | 2 | 6 | 22 | 51 |

Replay `79968923`:

| Team | Defense/reinforce approx | Multi-source approx | Comet actions approx | Recapture/counter approx | Target switching | Mid actions |
|---|---:|---:|---:|---:|---:|---:|
| Gregor Lied | 36 | 0 | 2 | 10 | 31 | 64 |
| vkhydras | 6 | 1 | 0 | 5 | 11 | 21 |
| 213tubo | 105 | 7 | 12 | 9 | 51 | 184 |
| bowwowforeach | 20 | 1 | 5 | 4 | 14 | 36 |

Macro reading:

- Active winners in the sample are not single-shot agents. They keep issuing
  midgame actions, reinforce or move into friendly planets, and switch targets.
- Some high-rank agents show many defense/reinforcement-like sends; this
  supports adding anti-recapture and threatened-planet features to profiler
  traces.
- Multi-source attacks appear, but not every high-rank action pattern is
  dominated by same-step multi-source sends. Multi-source is one tactic, not a
  universal signature.
- Comet interaction is present but uneven. 213tubo's sampled win had high comet
  action count; `79968955` top-match players had only 0-4 comet actions by this
  approximate metric.

## Late Game 300-500

Skipped for this sample.

Reason: all sampled episodes ended before turn 300:

- 79968841: 215 steps
- 79968870: 141 steps
- 79968910: 204 steps
- 79968923: 178 steps
- 79968955: 205 steps

No late all-in, evacuation, total-war, or turn-300+ convergence claims are made
from these replays.

## Strategy Features Supported By Visible Replays

The small sample supports these public-strategy features:

- high production target preference
- high-commit capture-sized launches
- early attack/contest after initial expansion
- reinforcement/recapture-aware midgame movement
- target switching rather than one fixed target
- occasional multi-source pressure
- uneven but real comet contesting

## What This Does Not Prove

- It does not reveal final gold strategy.
- It does not reveal private agent code.
- It does not prove all current top teams use the same strategy family.
- It does not prove center control is weak; the sampled boards and approximate
  target matching simply did not show center-heavy openings.
- It does not replace a larger replay-feature dataset.

## Direct Implications For Adaptive Agent Work

1. Add replay-derived profiler trace logging before further counter-policy
   tuning.
2. Detect high-commit expansion/rush separately from pure nearest/starter play.
3. Add recently captured planet / recapture windows to profiler and counter
   policy.
4. Track high-production target preference and defense-like friendly sends.
5. Split comet behavior into timing and action-count signals rather than a
   single boolean `comet_greedy` label.

