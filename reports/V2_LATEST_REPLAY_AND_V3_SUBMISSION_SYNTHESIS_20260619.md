# V2 Latest Replay And V3 Submission Synthesis - 2026-06-19

## Executive Summary

This stage did not modify strategy code.

Actions completed:

1. Packaged and submitted `alyce_intervention_v3` to Kaggle.
2. Refreshed the official status of V2 and prior Alyce reproduction.
3. Downloaded the latest V2 official episode replays.
4. Re-ran V2 replay phase/action analysis on the expanded replay set.
5. Compared the new data against previous strategy reports.
6. Updated `reports/SCORECARD.md`.

Current official state from Kaggle CLI:

| Submission | Status | Public score | Note |
|---:|---|---:|---|
| `53842450` V3 | `SubmissionStatus.COMPLETE` | `600.0` | Uploaded this stage; only validation replay visible at review time. |
| `53827977` V2 | `SubmissionStatus.COMPLETE` | `1101.6` | Current official best in repo. |
| `53793561` Alyce repro | `SubmissionStatus.COMPLETE` | `1069.1` | Previous official best. |

The earlier V2 score `600.0` was a stale/incomplete rating snapshot. After more
official games, the same V2 submission is now visible at `1101.6`. That changes
the interpretation materially: the V2 line is officially effective relative to
the prior Alyce reproduction, but the replay data still shows clear 4P holes.

## Package And Submission

V3 source:

```text
agents/variants/alyce_intervention_v3
```

Package:

```text
dist/alyce_intervention_v3_20260619.tar.gz
```

Package contents:

```text
main.py
orbit_lite/
```

SHA256:

```text
166D8C827A2F91FA28DF943F7611A145082538747293D7DACBFC3B0C9E026B90
```

Pre-submit checks:

```text
python -m py_compile agents/variants/alyce_intervention_v3/main.py
python scripts/smoke_candidate.py agents/variants/alyce_intervention_v3
```

Result:

```text
py_compile: pass
smoke_candidate: pass
sample_actions_ok: true
env_status: ok
```

Submit command:

```text
kaggle competitions submit -c orbit-wars -f dist/alyce_intervention_v3_20260619.tar.gz -m "alyce_intervention_v3_soft_far_low_penalty_b1542f4"
```

Kaggle result at report time:

```text
ref: 53842450
status: SubmissionStatus.COMPLETE
publicScore: 600.0
```

Visible V3 replay data at report time:

```text
D:\orbitwars_replays\alyce_intervention_v3_latest\episodes
episode_count: 1
episode: 80634227
TeamNames: muelsyse111 | muelsyse111 | muelsyse111 | muelsyse111
rewards: 1 | 1 | 1 | 1
type: validation/self-play-like replay
```

No public ladder V3 replay sample was visible yet, so the V3 score should be
treated as not competitive with V2 and not analytically rich enough for a phase
comparison.

## Latest V2 Replay Dataset

V2 submission:

```text
submission_id: 53827977
message: alyce_4p_ffa_v2_soft_contested_filter_20260619
current public score: 1101.6
```

Replay root:

```text
D:\orbitwars_replays\alyce_4p_ffa_v2_latest
```

Analysis files:

```text
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\submission_53827977_episodes_latest.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\episode_ids_latest.txt
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_episode_summary.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_action_events.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_key_snapshots.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_phase_summary.csv
D:\orbitwars_replays\alyce_4p_ffa_v2_latest\analysis\v2_analysis_summary.json
```

Downloaded replay count:

```text
previous replay files: 27
latest replay files: 55
newly downloaded this stage: 28
public replays: 54
validation self-play replays: 1
```

Mode split from public replays:

| Mode | First-place wins | Non-first episodes | Total |
|---|---:|---:|---:|
| 2P | 17 | 12 | 29 |
| 4P | 9 | 16 | 25 |
| Combined | 26 | 28 | 54 |

Important caveat:

```text
Replay first-place count is not the same as official rating movement.
The public score is rating-based and depends on opponent ratings and match
composition. Do not derive official score from simple replay win count.
```

## Updated Phase Findings

### Production Gap

Average production gap to current leader:

| Step | 2P wins | 2P losses | 4P wins | 4P losses |
|---:|---:|---:|---:|---:|
| 20 | -0.12 | -0.42 | -1.33 | -1.19 |
| 50 | 0.00 | -1.75 | -2.67 | -5.75 |
| 100 | 0.00 | -9.83 | -1.56 | -24.50 |
| 150 | -0.50 | -18.75 | 0.00 | -39.33 |

Interpretation:

- 2P losses usually stay close through step 50, then fall behind by step 100-150.
- 4P losses are already separating at step 50 and are usually strategically dead by step 100.
- This exactly matches the older Alyce 52-replay finding: 4P is decided by early production conversion, not by late tactics.

### 4P Action Mix

4P phase target mix:

| Phase | Outcome | Enemy rate | Neutral rate | Mine/regroup rate |
|---|---|---:|---:|---:|
| 0-50 | win | 0.180 | 0.678 | 0.142 |
| 0-50 | loss | 0.305 | 0.482 | 0.212 |
| 50-150 | win | 0.430 | 0.244 | 0.325 |
| 50-150 | loss | 0.518 | 0.250 | 0.232 |
| 150-300 | win | 0.308 | 0.183 | 0.508 |
| 150-300 | loss | 0.744 | 0.087 | 0.168 |

4P losses are more enemy-target heavy, especially after step 50. The strongest
bad signature is the midgame:

```text
4P mid 150-300 losses:
enemy_rate: 0.744
mine/regroup_rate: 0.168
```

That is the same behavior seen in earlier reports:

```text
once behind, Alyce/V2 keeps attacking, but the attacks do not restore production.
```

### Far-Low Target Signal

Approximate far-low target counts from inferred target:

| Phase | Outcome | Far-low enemy | Far-low neutral | Actions |
|---|---|---:|---:|---:|
| 4P 0-50 | win | 11 | 4 | 182 |
| 4P 0-50 | loss | 22 | 34 | 440 |
| 4P 50-150 | win | 51 | 28 | 782 |
| 4P 50-150 | loss | 59 | 93 | 1167 |
| 4P 150-300 | win | 17 | 10 | 318 |
| 4P 150-300 | loss | 10 | 9 | 171 |

The far-low neutral issue remains visible in losing 4P openings and early-mid
games. However, it is not the whole story. Losses also have much higher general
enemy pressure and weaker regroup/consolidation after step 50.

## Comparison Against Previous Reports

### Prior Report: `ALYCE_52_REPLAY_REVIEW_20260618.md`

Previous conclusion:

```text
Alyce is stronger in 2P than 4P.
4P failures are unstable early/mid production and poor conversion after
contested expansion or enemy pressure.
```

Latest V2 data:

```text
Still true.
```

V2 improves official rating, but 4P public replay sample is still weak:

```text
4P first-place count: 9 / 25
4P loss step100 avg production gap: -24.50
```

### Prior Report: `TXT_BASED_4P_IMPROVEMENT_DESIGN_20260618.md`

Previous design thesis:

```text
4P is not a zero-sum 2P game.
The missing layer is a mission layer that asks who benefits after my launch.
```

Latest V2 data:

```text
Confirmed.
```

The replay sample repeatedly shows V2 spending tempo on enemy pressure while
the production base collapses. This is exactly the 4P third-party problem:
winning a local fight or opening a target does not necessarily improve rank.

### Prior Report: `ALYCE_FIRST_VERSION_FAILURE_COMMONALITY_20260619.md`

Previous conclusion:

```text
Full safe-drain is not automatically bad.
Bad games fail because target selection and aftermath evaluation are wrong.
```

Latest V2 data:

```text
Confirmed, with nuance.
```

The V2 official score now proves that the older "V2 is simply bad" conclusion
was premature. But the replay features still say the same thing structurally:
do not suppress tempo globally; improve which tempo is allowed and when.

### Prior Report: `ALYCE_INTERVENTION_V3_ATTEMPT_20260619.md`

Previous V3 local conclusion:

```text
V3 is technically valid but local 4P screen did not justify submission.
```

Current status:

```text
V3 has now been submitted by user request.
Official result: 600.0 COMPLETE.
Visible replay: validation/self-play only.
```

The latest V2 replay data makes V3's hypothesis more plausible in one narrow
area:

```text
far low-production targets are genuinely overrepresented in 4P loss phases.
```

But the same data also says V3 is incomplete:

```text
far-low penalty alone does not address attack-vs-regroup selection,
holdability, third-party cleanup, or rank-dependent mode.
```

## Effectiveness Of The Last Changes

### V2 Change Effectiveness

Officially effective:

```text
V2 current score: 1101.6
Alyce repro current score: 1069.1
delta: +32.5
```

This invalidates the earlier decision that V2 should be treated as rejected
based only on the early `600.0` score snapshot.

However, this is not an ablation proof that every V2 component was good. V2
combined:

- contested-neutral softening;
- 4P source reserve relaxation;
- 4P wave restoration;
- older Light-derived planner structure;
- current official matchmaking sample.

The correct conclusion is:

```text
V2 as a submitted package is currently useful and should be the official best.
The reason is not fully isolated.
```

### V3 Change Effectiveness

Officially ineffective so far:

```text
V3 status: COMPLETE
V3 public score: 600.0
V2 public score: 1101.6
```

Local evidence remains mixed:

```text
2P V3 vs original Intervention short screen: 3-1
4P V3 vs original Intervention short screen: 1-3
```

The latest V2 replay data supports the general direction of V3, but the
submission result does not support the exact V3 package as a replacement for
V2. With only validation/self-play replay visible, the official result cannot
yet be turned into a rich decision-trace comparison, but it is enough for a
go/no-go:

```text
do not promote V3
do not resubmit unchanged
V3 far enemy penalty may be too large.
V3 does not include trace counters.
V3 does not distinguish early/mid/late or current rank.
```

## What Is Still Missing

The obvious missing components are now clearer:

1. Candidate-change trace.
   - We need to know when a penalty changes the selected action, not just that
     a penalty exists.

2. 4P rank/phase mode.
   - Step 50 and step 100 production rank should change behavior.
   - A losing 4P agent should not keep selecting the same attack-heavy mode.

3. Holdability / aftermath scoring.
   - Capture score should ask whether the target survives enemy response.
   - Reaction map is more important than static target production.

4. Attack-vs-regroup arbitration.
   - Losses show too much enemy pressure and too little consolidation after the
     production gap starts forming.

5. Source neighborhood protection.
   - A high-production source/frontier needs a local safety margin; not a global
     reserve, but source-specific aftermath protection.

6. 2P and 4P separation.
   - 2P losses happen later and need different handling than 4P losses.
   - 4P fixes should not leak into 2P without evidence.

7. Official replay comparison for V3.
   - Once `53842450` completes, download its episodes and compare against V2
     using the same metrics.

## Next Task Chain

Do not modify code until V3 official result is known.

### Stage A - Poll V3

```text
kaggle competitions submissions -c orbit-wars
```

V3 has completed at `600.0`, so:

- update `SCORECARD.md`;
- keep V2 as current official best;
- record the single visible V3 validation replay;
- do not compare V2 vs V3 by phase until V3 has public ladder episodes.

### Stage B - Build Replay Delta Report

Required report:

```text
reports/V2_VS_V3_OFFICIAL_REPLAY_DELTA_20260619.md
```

Metrics:

- official score delta;
- 2P and 4P first-place count if V3 public ladder episodes become visible;
- step 50/100 production gap;
- 4P enemy_rate / mine_rate by phase;
- far-low target rate;
- collapse episode examples.

### Stage C - Design V4 Only After V3 Result

V3 underperformed V2 officially:

- keep V2 as official best;
- do not continue hardening V3 penalty;
- build a lighter V4/V3b around trace-only, rank/phase mode, and softer
  penalties first.

### Stage D - Candidate Scoring Changes To Consider Later

Potential code changes, not done in this stage:

1. `selected_action_trace` in local/offline evaluation only.
2. `phase_rank_mode`:
   - leading: preserve production and avoid unnecessary remote low-value fights;
   - trailing: attack leader assets only if holdable; otherwise consolidate.
3. `holdability_score`:
   - use enemy ETA and pressure after capture.
4. `regroup_priority_boost` when:
   - 4P,
   - step 50-150,
   - production gap negative,
   - source neighborhood is threatened.
5. Reduce V3 far enemy penalty from `3.5` to a smaller value if official result
   confirms over-suppression.

## Current Decision

Current official best:

```text
V2 submission 53827977
public score 1101.6
```

V3:

```text
submission 53842450
status COMPLETE
public score 600.0
visible replay: validation/self-play only
```

No further code change should be made until the next change has action-change
trace instrumentation and a validation plan against the V2 replay failure
patterns.
