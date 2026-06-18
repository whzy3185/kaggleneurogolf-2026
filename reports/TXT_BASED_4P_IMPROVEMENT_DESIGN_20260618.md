# Txt-Based 4P Improvement Design

Date: 2026-06-18

Scope:

- Primary input: `C:\Users\zyc\OneDrive\文档\# 上下文完整总结.txt`
- Related local context: Alyce Intruder reproduction and code decision reports.
- Excluded input for this design: high-rank leaderboard replay records and rank-board phase analysis.

This report intentionally designs from the user's txt strategy notes first. It does
not use gold/high-rank replay conclusions as evidence. The goal is to produce a
clean improvement direction that can be implemented and tested locally without
mixing in leaderboard-derived assumptions.

## 1. Core Diagnosis

The txt's main point is not that the current base needs more ad-hoc thresholds.
It is that 4-player Orbit Wars is a different game from 2-player Orbit Wars.

In 2P, attacking an enemy planet is close to zero-sum:

```text
my_gain - enemy_gain
enemy_loss is also my relative gain
```

In 4P, attacking a target can pay a third player:

```text
I spend ships attacking A.
B/C spend nothing.
B/C clean up the weakened front or capture the opened neutral.
My local tactical win becomes a rank loss.
```

Therefore the current design gap is not just "ROI too high" or "send more ships".
The missing layer is a 4P FFA mission layer that answers:

```text
After this launch arrives, who actually benefits?
Can I hold the target after capture?
Does this action suppress the leader or feed another player?
Does it improve my rank survival, not only my local ship delta?
```

## 2. What To Preserve

The current Alyce-style base already has several valuable pieces:

- A good movement and garrison projection model.
- Dynamic player-count presets.
- Source safe-drain logic.
- Capture floor checks.
- Greedy wave selection.
- Defensive regroup.
- Relative strength adjustment through ROI and wave count.

The first improvement should not replace these. It should add a thin 4P decision
layer around target generation and candidate scoring.

Preserve:

- 2P behavior by default.
- Existing movement/garrison engine approximation.
- Existing action format and runtime memory.
- Existing deterministic heuristic style.

Avoid in the first version:

- New neural training.
- Opponent-name hardcoding.
- Large rewrites of the movement model.
- Adding late supplemental attacks after the base has already spent the source budget.
- A broad "adaptive profiler" that labels opponents but cannot affect core scoring early enough.

## 3. Proposed Candidate: Alyce 4P FFA Mission Layer V1

Working name:

```text
alyce_4p_ffa_mission_v1
```

Top-level routing:

```python
def agent(obs):
    player_count = infer_player_count(obs)
    if player_count < 4:
        return base_agent(obs)
    return plan_4p_ffa_mission_v1(obs)
```

The important constraint is that `plan_4p_ffa_mission_v1` should run before final
action selection. It should shape which targets/candidates enter the greedy
planner, not append actions afterward.

## 4. FFA Context

Before scoring targets, build a compact per-turn FFA context:

```text
player_strength[p] =
    owned_production[p] * prod_weight
  + planet_ships[p]
  + fleet_ships[p] * fleet_weight
  + frontier_control[p] * frontier_weight
```

Derived fields:

```text
self_id
alive_players
rank_by_strength
self_rank
leader
runner_up
weakest
leader_gap = strength[leader] - strength[self]
phase = opening / midgame / lategame
remaining_turns
```

Initial weights should stay simple:

```text
prod_weight: 18 to 28
fleet_weight: 0.5 to 0.8
frontier_weight: small, initially optional
```

This is not an Elo model. It is a live board-state model. It answers who is
currently winning, who is catchable, and who should not be fed.

## 5. Reaction Map

The most urgent primitive from the txt is the reaction map:

```text
my_best_eta[target]
enemy_best_eta[target][enemy]
enemy_best_pressure[target][enemy]
reaction_gap = min_enemy_eta - my_best_eta
```

This should be computed for neutral and enemy planets using legal source planets
and the existing intercept/movement machinery where possible.

The reaction map drives:

- Safe neutral classification.
- Contested neutral classification.
- Trap neutral rejection.
- Enemy target holdability.
- Third-party cleanup risk.

This is the first feature to implement because it directly fixes the failure
mode "we sent enough to occupy on arrival, but not enough to keep the target
after any nearby enemy response".

## 6. Neutral Target Classification

Do not treat all neutral planets as equal ROI targets in 4P.

### Safe Neutral

Condition:

```text
my_best_eta + hold_margin < min_enemy_best_eta
```

Meaning:

- I arrive first.
- Enemies cannot cheaply answer within a short hold window.
- Capturing does not empty a critical source.

Score shape:

```text
safe_neutral_score =
    production * remaining_value_horizon
  + safe_neutral_bonus
  - ships_needed
  - eta * eta_penalty
  - source_depletion_penalty
```

These should be the default 4P expansion targets.

### Contested Neutral

Condition:

```text
abs(my_best_eta - min_enemy_best_eta) <= contest_window
```

Allowed mission types:

- `contested_neutral_snipe`: arrive just after an enemy opens the neutral.
- `contested_neutral_swarm`: use multiple sources if the arrival window is tight.
- `avoid`: reject if we cannot overmargin or snipe cleanly.

Do not use ordinary single-wave capture for this class unless the post-capture
garrison survives enemy response.

### Trap Neutral

Condition:

```text
enemy_reaction_eta <= my_eta + 2
and enemy_available_pressure > my_post_capture_garrison
```

or:

```text
target is close to two or more enemies
and my ETA/send cost is high
and hold check fails
```

Default action: reject.

This filter is critical because high-production neutrals can be bait. In 4P, a
planet that is profitable in isolation can still be a losing move if it becomes
a low-cost capture for someone else.

## 7. Enemy Target Classification

Enemy planets should not enter one generic "attack target" bucket.

### Leader Asset

Target belongs to current leader.

Bonus:

```text
leader_bonus =
    leader_weight * max(0, player_strength[leader] - player_strength[self])
```

But this must be gated:

```text
can_capture
can_hold_for_hold_horizon
third_party_cleanup_risk is not high
source_depletion_risk is acceptable
```

If these gates fail, attacking the leader may be kingmaking rather than leader
suppression.

### Threat Neighbor

Target directly threatens our high-production or frontier planets.

Score component:

```text
threat_reduction =
    pressure_on_my_frontier_before
  - pressure_on_my_frontier_after
```

This target can be valuable even if production ROI is not high, because it
reduces collapse risk.

### Enemy Rear / Low-Value Enemy

Reject by default when:

```text
target is far
target production is low
target is not leader-owned
target is not elimination-critical
ETA is long
```

This prevents sending ships into low-impact backline captures that make us weak
on the actual front.

### Elimination Target

Allowed mostly in late game or against a nearly dead player.

Gate:

```text
enemy_total_strength is low
target is a final/key production point
my post-launch rank does not drop from top2 to bottom2
third parties cannot take the main reward immediately
```

## 8. Mission Layer

The txt's strongest design recommendation is to generate missions first, then
sort globally. This is better than mixing all targets in one score.

Mission priority:

```text
1. defense_hold
2. rescue_or_recapture
3. safe_neutral
4. contested_neutral_snipe
5. leader_pressure
6. threat_neighbor_attack
7. swarm_attack
8. crash_exploit
9. regroup
10. terminal_all_in
```

For V1, implement only the safer subset:

```text
V1A:
  defense_hold
  rescue_or_recapture
  safe_neutral
  contested_neutral_snipe
  leader_pressure with strict hold gate
  threat_neighbor_attack
  regroup
```

Defer:

```text
crash_exploit
deep synchronized swarm
learned controller
full counterfactual third-party simulation
```

Reason: the first version should reduce obvious bad 4P moves without increasing
action instability.

## 9. 4P Score Function

The score should distinguish self gain from rank/risk effects:

```text
mission_score =
    base_flow_score
  + self_gain
  - leader_weight * positive_leader_gain
  - runnerup_weight * positive_runnerup_gain
  - third_party_cleanup_risk
  - kingmaking_penalty
  - source_depletion_penalty
  + survival_bonus
  + leader_pressure_bonus
  + threat_reduction_bonus
```

Definitions:

```text
third_party_cleanup_risk =
    nearby_enemy_pressure_after_capture
  - my_post_capture_garrison
```

```text
kingmaking_penalty =
    max(0, third_party_gain_after_my_attack - my_gain_after_attack)
```

```text
survival_bonus =
    value of keeping top2/top3 rank and avoiding last-place collapse
```

In V1, these can be approximations. The point is not perfect game theory; the
point is to stop treating all positive tactical flow deltas as equal.

## 10. Multi-Size Drain

The txt explicitly flags single-size safe drain as a weakness. Current Light
Intruder-style planning often uses one large send from each source. That is strong
when target choice is right, but punishing when target choice is wrong.

V1 should evaluate small drain tiers:

```text
exact_capture_floor
50 percent of safe_drain
75 percent of safe_drain
100 percent of safe_drain
```

Candidate is legal only if:

```text
send_size >= capture_floor
post_source_garrison >= reserve_floor_for_phase
post_target_garrison survives hold check
```

Expected benefit:

- Fewer overcommits into neutrals.
- Better defense retention.
- More options for contested snipes.
- Less "all ships leave one source for a marginal target".

## 11. Phase Policy Without High-Rank Replay Assumptions

This report does not use high-rank replay phase evidence. The phase policy below
comes only from the txt's game-structure reasoning.

Opening:

- Prefer safe neutrals.
- Reject trap neutrals.
- Avoid leader pressure unless target is nearby and holdable.
- Keep reserve floor higher on frontier sources.

Midgame:

- Classify leader, runner-up, weakest.
- Apply leader pressure only where third-party cleanup risk is low.
- Attack threat neighbors before low-value rear planets.
- Use contested neutral snipe instead of paying full neutral cost when possible.

Endgame:

- Reduce value horizon for production.
- Increase rank/survival value.
- Allow elimination targets if they improve rank and do not feed a third party.
- Allow terminal all-in only when remaining production no longer repays waiting.

## 12. Implementation Plan

### Stage 1: FFA Context

Add a small context builder:

```text
FfaContext:
  player_strength
  rank
  leader
  runner_up
  weakest
  self_rank
  phase
```

Validation:

- Unit test strength ordering on synthetic observations.
- Trace output for first 100 turns in 4P local games.

### Stage 2: Reaction Map

Compute:

```text
my_best_eta
enemy_best_eta_by_player
reaction_gap
enemy_pressure_by_target
```

Validation:

- Synthetic map where one neutral is safe, one contested, one trap.
- Trace labels match expected classification.

### Stage 3: Neutral Filter

Before candidate scoring, label neutrals:

```text
safe_neutral
contested_neutral
trap_neutral
```

Action:

- Keep safe neutrals.
- Allow contested neutrals only as snipe/overmargin.
- Reject trap neutrals unless late-game all-in overrides.

### Stage 4: Enemy Target Filter

Label:

```text
leader_asset
threat_neighbor
enemy_rear
elimination_target
```

Action:

- Boost holdable leader assets.
- Boost threat neighbors.
- Reject distant enemy rear targets.
- Gate elimination by rank safety.

### Stage 5: Multi-Size Drain

Replace one-size source-target candidate with tiered send candidates. Keep the
existing greedy selector but feed it more disciplined candidates.

### Stage 6: Mission Trace

Every selected launch should log, locally only:

```json
{
  "step": 80,
  "mission": "safe_neutral",
  "source": 12,
  "target": 4,
  "send": 18,
  "eta": 5,
  "target_label": "safe_neutral",
  "self_rank": 2,
  "leader": 1,
  "reaction_gap": 6,
  "score": 31.2,
  "reject_reasons_seen": ["trap_neutral", "enemy_rear"]
}
```

Do not submit trace output. Use it to debug whether the agent is actually making
the intended 4P decisions.

## 13. Validation Plan

No code should be promoted or submitted until these questions are answered:

```text
1. Does 2P behavior stay unchanged or close to unchanged?
2. Does 4P reduce early source depletion?
3. Does safe neutral hold rate improve?
4. Are trap neutrals actually rejected?
5. Does leader pressure avoid obvious third-party cleanup?
6. Does average rank improve, not only win count?
7. Are errors/timeouts still zero?
```

Suggested local metrics:

```text
2P non-regression:
  base vs mission_v1, 50 seeds bidirectional

4P mixed pool:
  base, mission_v1, alyce_intruder, vkhydras/producers, 50+ games with position rotation

Mission metrics:
  safe_neutral_attempts
  safe_neutral_hold_10_turn_rate
  contested_snipe_attempts
  trap_rejections
  leader_pressure_attempts
  leader_pressure_hold_rate
  source_depletion_losses
  rank_at_50/100/200/final
```

Pass criteria for V1A:

```text
2P winrate vs base >= 45 percent
4P avg_rank improves or rank<=2 rate improves
errors = 0
timeouts = 0
mission trace is explainable
```

## 14. First-Code Recommendation

The first useful code task should not be a full targeted agent. It should be:

```text
Implement FfaContext + ReactionMap + NeutralLabel trace only.
```

Then run local 4P games and inspect labels before allowing the labels to affect
actions. This prevents building another large policy on unverified assumptions.

After label traces are correct, enable only:

```text
trap_neutral rejection
safe_neutral bonus
enemy_rear penalty
source reserve floor by phase
```

Only after that should leader pressure and multi-size drain be enabled.

## 15. Summary

The improved idea is a 4P-only FFA mission layer over the current Alyce-style
base:

- Keep 2P mostly unchanged.
- Build live player strength/rank context.
- Build reaction maps for target holdability.
- Classify neutrals as safe/contested/trap.
- Classify enemy planets as leader asset/threat/rear/elimination.
- Generate mission candidates instead of raw target candidates.
- Penalize third-party cleanup and kingmaking.
- Add multi-size drain to reduce overcommit.
- Require mission trace before trusting the policy.

This directly follows the txt's first-principles point: in 4P, the correct target
is not the one with the best isolated capture score; it is the one whose arrival
and aftermath improve our relative rank without handing the board to a third
player.
