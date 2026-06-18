# Alyce Intruder Deep Dive And Reproduction

Date: 2026-06-18

## Executive Decision

Use `alyce_intruder_repro` as the current practical base candidate for the next
submission check.

Reason: the previous Vkhydras line was a light heuristic and the public output
recheck found several Producer-family output packages that locally beat it in the
small screen. Alyce Intruder is one of the highest-signal public Code entries and
is structurally stronger than the earlier single-file heuristics because its
core action quality is enforced by world-model projection, safe source draining,
ETA-aware capture floors, and dynamic ROI.

This report does not claim Alyce's title score as our score. Official score can
only come from our own Kaggle submission.

## Source Refresh

Observed through Kaggle CLI:

```text
ref: alycemiki/light-ver-1200-simple-orbit-intruder
title: [Light ver. & 1200+] Simple Orbit Intruder
author: Alyce Miki
lastRunTime: 2026-06-15 01:55:21.737000
totalVotes: 147
```

The notebook and output package were refreshed to ignored local paths:

```text
external/kaggle_notebooks/alycemiki__light-ver-1200-simple-orbit-intruder
external/kaggle_outputs/alycemiki__light-ver-1200-simple-orbit-intruder
```

The output tar was extracted and reproduced into:

```text
agents/public/alyce_intruder_repro
```

## Reproduced Package Shape

```text
agents/public/alyce_intruder_repro/
  main.py
  orbit_lite/
    __init__.py
    adapter.py
    aiming.py
    constants.py
    distance_cache.py
    garrison_launch.py
    geometry.py
    intercept_aim.py
    movement.py
    movement_aiming.py
    movement_step.py
    obs.py
    planner_core.py
```

This is a multi-file agent. For submission it must be packaged as tar.gz with
`main.py` and `orbit_lite/` at archive root. It should not be forced into a
single file before we have official evidence that such rewriting preserves
behavior.

## Competition Structure That Matters

Orbit Wars is not a static nearest-target game. Good agents must handle:

- moving planets;
- ship-speed depending on fleet size;
- exact or approximate intercept aiming;
- neutral expansion versus enemy attack;
- source-planet safety after launching;
- reinforcements that can arrive before our fleet;
- 2-player and 4-player incentives;
- comet / temporary planet timing;
- finite 500-step horizon;
- late-game value decay for slow launches.

The most common weak-agent failure is sending a fleet that looks large enough
at launch time but is not large enough at arrival time. Alyce Intruder directly
addresses that failure through projected garrison status, ETA-aware capture
floor, and reinforcement margin.

## Intruder Design Philosophy

The notebook describes the design as:

- clean skeleton;
- single-size planner;
- `safe_drain` only;
- no heavy GRU controller;
- no multi-tier planner;
- no FFA bonus module;
- dynamic adjustment through one function;
- late-game candidate suppression.

The important engineering choice is simplification after experimentation.
Earlier Alyce notebooks included TinyGRU/controller hooks and heavier 2P/4P
logic. Intruder keeps the high-value mechanics but removes fragile control
layers.

## Core Pipeline

The per-turn path is:

1. Convert Kaggle observation into tensors.
2. Build or update planet movement forecast.
3. Estimate future garrison status over a horizon.
4. Adjust config based on current strength ratio and remaining time.
5. Build attack and defense target shortlist.
6. Compute safe source drain for owned planets.
7. Compute reachable source-target candidates and intercept angles.
8. Compute capture floor at candidate ETA.
9. Score candidates with projected competitive value.
10. Suppress late candidates that cannot pay back before game end.
11. Greedily choose waves under source budget and target mutex constraints.
12. Use leftover safe ships for pressure-based regroup.
13. Convert sparse tensor action rows back to Kaggle move lists.

## Key Mechanisms

### Safe Drain

`safe_drain` asks: how many ships can this source planet shed while still being
held over the forecast horizon?

This is the right first-principles source-budget rule. It avoids a common error:
using current ships as spendable ships even when the planet is about to be
captured or needs its garrison.

### Capture Floor

`capture_floor` computes owner-aware required ships at arrival turn:

- if the target is ours at arrival, one ship can reinforce;
- otherwise the fleet must beat projected defenders plus capture overhead;
- optional reinforcement margin inflates this floor.

This is the direct fix for low-quality launches that do not have enough ships
to occupy the target.

### ETA-Aware Reinforcement Risk

The agent estimates enemy pressure around each target and adds risk as a
function of ETA:

```text
rho = clamp((eta - eta_free) / eta_scale, 0, 1)
reinforcement = beta * rho * enemy_mass
```

Short flights get little penalty; long flights require more margin because the
enemy has time to react.

### Reachability And Intercept

The planner first uses a reachability gate, then exact-ish intercept aiming.
That keeps candidate generation efficient without trusting a naive straight-line
distance estimate.

### Dynamic ROI

Intruder computes player strength as:

```text
production + 0.025 * ships
```

If behind, it lowers ROI smoothly; in late game it lowers ROI further and may
add an extra wave. This is not hard-coded "rush after turn N" behavior. It is a
continuous pressure response.

### Late-Game Suppression

In the last 120 turns, neutral captures are devalued and attacks that arrive too
late are suppressed. This prevents slow expansion moves from wasting ships near
the end.

### Regroup

After attacks, the agent uses remaining safe ships to move from low-pressure
owned planets toward higher-pressure owned planets. This matters because a
strong agent does not only attack; it also reduces accidental collapses in the
middle.

## Strategy Taxonomy Placement

Primary family:

```text
hybrid_layered_agent
world_model_forecaster
production_greedy_expander
defense_reinforcement_agent
```

Secondary families:

```text
center/high-value control when production and proximity align
late-game tempo agent
limited turtle prevention via regroup and dynamic ROI
```

It is not primarily:

```text
pure nearest_expander
pure RL_policy_agent
name-specific targeted agent
crash exploit agent
hard-coded opponent profiler
```

## How It Compares To Other Public Strategy Families

### Nearest Expander

Nearest expanders take easy neutral planets but often under-send or over-drain.
Intruder keeps proximity in the target shortlist but requires capture floor and
safe drain, so it avoids many bad early launches.

### Production Greedy

Production greedy agents can overpay for distant high-production planets.
Intruder's ETA, reachability, and late-game suppression make this less reckless.

### Big Stack / Hammer

Big-stack agents save and hit hard. Intruder does not explicitly hoard; it
creates waves when candidates beat ROI. It can still launch large fleets because
single-size mode uses safe drain.

### Defensive / Turtle

Pure turtles lose tempo. Intruder only reinforces when future status suggests
friendly flips and uses regroup after attack planning. Defense is integrated,
not dominant.

### FFA Leader Attack

This light Intruder version intentionally removes the heavy FFA bonus layer.
That makes it simpler and less fragile, but may be weaker than Alyce's
`Intervention Command w/ FFA` in 4-player hidden pools.

### RL / GRU Controller

Earlier Alyce notebooks included a TinyGRU controller shell. Intruder removes
that dependency. This is probably why the public package is compact and robust:
the model layer was not needed for the current public output candidate.

## Strengths

- High action validity: attacks are checked against future target state.
- Good source safety: source budget is forecast-aware.
- Strong moving-target support through `orbit_lite`.
- Simple enough to package and inspect.
- Uses dynamic game-state adjustment without brittle opponent-name logic.
- Compatible with Kaggle multi-file submission format.

## Weaknesses And Risks

- It is still a public package; hidden official pool may already counter it.
- The light Intruder variant has less explicit 4P anti-leader logic than Alyce's
  FFA notebook.
- It depends on `torch`; Kaggle environment must support it.
- License/redistribution metadata is unclear in the local registry.
- It is not our own official result until the user-requested submission
  completes.

## Concrete Reuse Plan

Immediate:

1. Reproduce exact public output package.
2. Package as tar.gz without rewriting.
3. Submit once, as requested, and record official status.

Next if the score is good:

1. Use Intruder as `base_v2`.
2. Keep the base black-box first.
3. Add only safety filters that cannot increase ship spend.
4. Compare light Intruder against Alyce FFA, Ranjeet Producer, Tamrazov
   Stronger, Shumming Exp50, and Caoyupeng GRU before deeper modifications.

Next if the score is poor:

1. Do not keep it as final.
2. Treat it as a source of mechanisms: capture floor, safe drain, ROI, and
   late-game suppression.
3. Re-run the fresh output pool with the fixed multi-file candidate loader.

## Submission Status

At report creation time:

```text
submitted: yes
submission_id: 53793561
package: dist/alyce_intruder_repro_20260618.tar.gz
package_sha256: E7407E0ECA360114FAB5C84884FCE7D609F470A0DD069A35782B62961F14E43F
package_bytes: 54548
latest_status: SubmissionStatus.PENDING
official_score: unknown
```
