# Alyce Intruder Full Code Decision Report

Date: 2026-06-18

Scope:

- Executable reproduced package: `agents/public/alyce_intruder_repro/`
- Primary Kaggle Code source: `alycemiki/light-ver-1200-simple-orbit-intruder`
- Related Alyce notebooks reviewed for lineage only:
  - `alycemiki/orbit-wars-ver-02`
  - `alycemiki/elo1245-a-simple-but-considerate-solution`
  - `alycemiki/intervention-command-w-ffa`

Important distinction:

The submitted Alyce Intruder reproduction is not a trained neural policy. It is
a deterministic, Torch-based heuristic planner. The Alyce notebook family does
contain TinyGRU/controller designs and FFA intervention designs, but the current
Light Intruder package explicitly removes GRU, multi-size drain tiers, and FFA
bonus modules. Therefore training decisions are reported as upstream design
lineage, not as active behavior of the current package.

## 1. File Inventory

Tracked reproduced package:

| File | Lines | Role |
|---|---:|---|
| `main.py` | 528 | Kaggle entrypoint, mode config, dynamic config, planner orchestration |
| `orbit_lite/adapter.py` | 220 | Dict observation to padded tensors, sparse actions back to Kaggle moves |
| `orbit_lite/aiming.py` | 16 | Small orbit-phase helper |
| `orbit_lite/constants.py` | 61 | Board, tensor caps, comet constants |
| `orbit_lite/distance_cache.py` | 141 | Future cross-time distance cache and proximity ranking |
| `orbit_lite/garrison_launch.py` | 450 | Exact sparse launch combat/production flow delta scorer |
| `orbit_lite/geometry.py` | 99 | Fleet speed formula and lookup table |
| `orbit_lite/intercept_aim.py` | 287 | Continuous intercept angle solver and first-contact screen |
| `orbit_lite/movement.py` | 1962 | Future world model, planet/comet positions, fleet ledger, garrison projection |
| `orbit_lite/movement_aiming.py` | 70 | Swept segment hit helper |
| `orbit_lite/movement_step.py` | 298 | Runtime movement cache update, private planned launch injection |
| `orbit_lite/obs.py` | 196 | Parsed observation view and ownership masks |
| `orbit_lite/planner_core.py` | 633 | Candidate scoring, target shortlist, greedy wave selection, regroup |
| `orbit_lite/__init__.py` | 6 | Package marker |

Source metadata:

- `SOURCE.md` records public source, pull command, output command, file list,
  and attribution to Alyce Miki plus the referenced `slawekbiel/producer-orbit-wars-utils`.
- `WRAPPER.md` records that this is a direct multi-file output reproduction,
  not a wrapper around another local source.

## 2. High-Level Agent Architecture

The active agent path is:

1. `agent(obs)` in `main.py`
2. `single_obs_to_tensor(obs, player_id)` in `adapter.py`
3. `_RUNTIME.tensor_action(obs_tensors)` in `main.py`
4. `run_turn(...)` in `main.py`
5. `ensure_planet_movement(...)` in `movement_step.py`
6. `PlanetMovement.garrison_status(...)` in `movement.py`
7. `plan_lite_waves(...)` in `main.py`
8. `score_candidates(...)` and `_greedy_select(...)` in `planner_core.py`
9. `_plan_regroup(...)` in `planner_core.py`
10. `entries_to_sparse_payload(...)` then `sparse_action_row_to_moves(...)`

The policy is a layered heuristic:

- A world model predicts planet/comet motion and near-future garrison states.
- A target generator creates offensive enemy/neutral targets plus urgent friendly
  rescue targets.
- A source selector chooses owned planets with enough ships.
- A safe-drain rule decides how many ships can leave each source.
- A one-size attack candidate is built for each source/target pair.
- A sparse exact flow scorer estimates net competitive ship gain.
- A greedy selector fires high-score waves above ROI.
- A pressure-gradient regroup pass moves unused ships toward threatened owned planets.

## 3. Opening Presets

### 3.1 Base 2P Preset

`CONFIG_2P = ProducerLiteConfig()` uses the dataclass defaults:

| Parameter | Value | Meaning |
|---|---:|---|
| `horizon` | 18 | Predict up to 18 turns for target viability and garrison state |
| `max_sources_per_lane` | 12 | Consider top owned source planets by current ships |
| `max_offensive_targets` | 12 | Consider nearest enemy/neutral targets |
| `max_defensive_targets` | 4 | Reserve up to 4 own planets predicted to flip |
| `max_waves_per_turn` | 6 | Attack greedy can fire up to 6 waves |
| `roi_threshold` | 1.40 | Candidate must exceed this score to fire |
| `min_ships_to_launch` | 4 | Sources below 4 ships are ignored |
| `reinforce_size_beta` | 2.2 | Enemy pressure margin added to capture floor |
| `enable_regroup` | true | Unused safe ships can be moved defensively |
| `max_regroup_time` | 7 | Regroup only if destination reachable quickly |

Opening implication:

- The agent does not have a hard-coded first move.
- It waits until a source has enough ships and a candidate clears the ROI/capture
  gates.
- Early expansion is usually toward nearest reachable neutral targets with good
  projected score, not explicitly toward named planets.
- Because the send size is single-size `safe_drain`, early launches often send
  nearly all currently safe ships from a source.

### 3.2 3P Preset

`CONFIG_3P` lowers horizon to 15, source cap to 8, offensive targets to 10,
defensive targets to 3, and ROI to 1.35.

Interpretation:

- Shorter horizon and smaller search width reduce compute and long-range overcommit.
- Lower ROI makes it slightly more active than 2P on marginal opportunities.

### 3.3 4P Preset

`CONFIG_4P` uses horizon 13, ROI 1.25, source cap 7, defensive cap 2, waves 5,
regroup time 6, and regroup target cap 8.

Interpretation:

- 4P mode is shorter-horizon and more opportunistic.
- It does not include explicit leader targeting in the Light Intruder package.
- It relies on proximity, pressure, and competitive score rather than FFA bonus
  terms.

## 4. Runtime Memory And State

`ProducerLiteMemory` stores:

- `movement`: cached `PlanetMovement`
- `cached_player_count`: inferred once and reused

`ProducerLiteRuntime.tensor_action` resets memory when step becomes 0, infers
player count, chooses 2P/3P/4P config, and calls `run_turn`.

Key consequence:

- The agent has persistent per-episode memory, but only for movement/garrison
  tracking.
- It does not store opponent identity, learned opponent type, replay history, or
  long-term strategic labels.
- It injects private planned launches into its world model so future turns know
  about its own just-launched fleets even before the public observation fully
  reflects all internal intent.

## 5. Dynamic Config Decisions

`_owner_strength` computes a compact strength proxy:

```text
strength = owned production sum + 0.025 * owned ships
```

`_adjust_config` compares my strength to the current leader:

- If behind, lower ROI quadratically.
- If far behind, allow one extra wave.
- If late and behind, lower ROI further and possibly add another wave.

This is not a phase-based opening/midgame/endgame switch. It is a continuous
pressure adjustment. The only inputs are current owned production/ships and
remaining game time.

Strategic effect:

- When even or ahead, the agent keeps default ROI and avoids marginal throws.
- When behind, it accepts lower-value attacks and fires more waves.
- In self-play, small asymmetries can change the computed ratio by a little,
  lowering one side's ROI earlier than the other and changing candidate choice.

## 6. World Model

### 6.1 Observation Parsing

`adapter.py` pads Kaggle dict observations into fixed tensors:

- `planets`: `[P_MAX, 7]`
- `fleets`: `[F_MAX, 7]`
- `initial_planets`
- comet paths and comet planet IDs
- scalar metadata: player, player_count, angular velocity, next_fleet_id, step,
  episode steps, remaining overage time

`obs.py` exposes masks:

- owned planets
- enemy planets
- neutral planets
- alive planets/fleets
- ship vectors and owner vectors

### 6.2 Future Position Model

`movement.py` predicts:

- static planet positions
- orbiting planet positions from angular velocity
- comet positions and lifetime from path metadata
- swept collision geometry
- future ownership/ship trajectories

It also maintains:

- garrison projection cache
- tracked fleet ledger
- own planned launch bookkeeping
- reconciliation when observed fleets differ from internally planned fleets

This file is the real engine approximation. Most strategic sophistication in
Alyce Intruder depends on this world model being close to the Kaggle engine.

### 6.3 Garrison Projection

`PlanetMovement.garrison_status(max_horizon=H)` creates future owner/ships tables.
These are used by:

- defensive target detection
- capture floor
- safe drain
- candidate scoring
- regroup arrival ownership check

If the projection says an owned planet will flip, it can become a defensive target.

## 7. Target Shortlist Logic

`build_target_shortlist` creates one target list with two parts.

### 7.1 Offensive Targets

`attack_target_mask`:

- target can be enemy or neutral
- target must be alive
- target must not be a comet

Ranking:

- compute minimum future distance from any current source to each target
- prefer closer targets by `-proximity`
- select up to `max_offensive_targets`

### 7.2 Defensive Targets

`friendly_flip_targets`:

- detect currently owned planets that the do-nothing projection says will become
  non-owned within horizon
- rank by urgency:

```text
urgency = production * remaining_horizon_after_flip + current_ships
```

Interpretation:

- High-production or high-garrison planets about to flip are placed into the
  target list.
- Later, a defensive candidate has a capture floor of 1 because friendly ships
  reinforce rather than conquer.

## 8. Source Selection And Safe Drain

`source_mask` is:

```text
owned AND alive AND ships >= min_ships_to_launch
```

`_candidate_indices(obs.ships, source_mask, cap)` chooses the largest owned
garrisons first.

`safe_drain` computes the maximum ships that can leave while the source remains
held over the projected horizon:

- Look at future source ships where source is still mine.
- Find the minimum positive projected slack.
- Clamp by current source ships.
- If the source is already doomed in projection, it can shed all current ships.

Strategic effect:

- The agent often sends a large fraction, sometimes all, of a source.
- This is why it can be strong and fast, but also why wrong target choice can
  empty a front and cause cascading loss.

## 9. Candidate Construction

For each source-target pair:

1. `size = floor(safe_drain(source))`
2. `reachable_mask` checks whether the target can be contacted within horizon.
3. `intercept_angle` solves the continuous angle and ETA.
4. `capture_floor` calculates ships required at arrival.
5. Candidate is valid only if:

```text
viable_intercept
AND eta <= horizon
AND send_size >= capture_floor_at_eta
AND send_size >= min_ships_to_launch
AND source != target
AND source_exists
AND target_exists
```

Capture floor is owner-aware:

- If target is mine at arrival, floor is 1.
- Otherwise floor is projected defenders + 1 + enemy reinforcement margin.

Enemy reinforcement margin:

- `cheap_enemy_pressure` estimates distance-decayed enemy ship pressure.
- `reinforce_size_beta = 2.2` scales that pressure.
- Short ETA gets little/no extra margin; longer ETA gets more margin via
  `reinforcement_timing_factor`.

This is the main anti-"not enough ships to capture" safeguard in the Light
Intruder package.

## 10. Candidate Scoring

`score_candidates` calls `sparse_launch_flow_delta`, then `competitive_score`.

The competitive score is:

```text
my_net_ship_delta - sum(opponent_net_ship_delta)
```

The flow scorer estimates:

- ships produced
- ships lost to combat
- changed ownership at target cells
- enemy/friendly net change

This is not a hand-coded "attack enemy if close" rule. It is a local world-model
counterfactual: "if I launch this candidate, how much does the net competitive
ship balance improve?"

## 11. Greedy Wave Selection

`_greedy_select` repeatedly picks the best remaining candidate:

Selection gates:

- `score` must be finite
- target cannot already be taken this turn
- source must still have budget
- target cannot already have been used as a source this turn
- a defended target cannot also contribute ships in the same turn
- best score must exceed `roi_threshold`

Tie-breaking:

- `_stable_argmax` chooses the lowest candidate index among equal scores.
- Candidate index depends on source/target slot ordering.

This tie-break is deterministic but not symmetry-invariant. In self-play,
mirror planets can have different slot IDs. Equal or near-equal scores can
therefore split into different choices for player 0 and player 1.

## 12. Regroup Logic

After attack waves, `_plan_regroup` moves leftover ships.

Source condition:

```text
owned AND alive AND leftover >= min_ships_to_launch
```

Regroup send size:

```text
regroup_cap = min(leftover, safe_drain - already_committed)
```

Destination condition:

- destination is owned, alive, non-comet
- pressure(destination) - pressure(source) > `regroup_pressure_delta_min`
- ETA <= `max_regroup_time`
- destination still mine at arrival in projected garrison status

Score:

```text
pressure_gap - regroup_time_penalty_weight * eta
```

Strategic effect:

- Many observed "attacks" in replay are actually pressure-gradient regroup
  moves, not offensive candidate waves.
- This explains why replay actions sometimes do not match the top attack
  candidate trace. The final move list is `attack_entries + regroup_entries`.
- Regroup can look like huge movement from a strong rear planet toward a front
  planet, then that front planet immediately becomes the next launch source.

## 13. Late-Game Candidate Suppression

`_suppress_late_candidates` applies only after step 350.

Rules:

- If arrival ETA is too late relative to remaining game time, suppress the
  candidate.
- Neutral candidates are gradually devalued late.
- Defensive candidates are exempt from this late neutral devaluation.

Current self-play validation ended at step 237, so this logic did not decide
the observed self-play result.

## 14. Comet Handling

Current Light Intruder package:

- parses comet paths and comet planet IDs
- applies comet path overrides in movement projection
- excludes comet planets from normal offensive target shortlist
- excludes comet planets from regroup destinations

It does not contain the explicit comet evacuation helper found in
`intervention-command-w-ffa`.

Interpretation:

- This package is comet-aware enough not to treat comets like normal stable
  planets.
- It is not a specialized comet-farming or comet-evacuation agent.

## 15. Opening Behavior

There is no fixed build order. The opening emerges from:

- `min_ships_to_launch = 4`
- nearest target shortlist
- safe-drain send size
- capture floor
- ROI threshold
- production/ship competitive scoring

Typical behavior:

1. Home grows until a nearby neutral capture candidate clears the floor.
2. The first captures favor reachable high-value/proximal neutral planets.
3. Newly captured production planets become sources after enough ships accumulate.
4. Expansion accelerates because `safe_drain` allows large launches from high
   garrison sources.

From validation self-play `80405449`, the first mirrored action at replay step
12 sent 21 ships from each home to symmetric production-3 neutrals. This is
consistent with the opening logic above, not with a hard-coded script.

## 16. In-Game Decision Phases

### Expansion Phase

Dominant mechanisms:

- nearest offensive target shortlist
- capture floor
- one-size safe-drain launch
- sparse flow competitive score

Strength:

- expands quickly when nearby neutral values are good.
- avoids some underpowered attacks because floor includes projected defenders
  plus pressure margin.

Weakness:

- because only full safe-drain size is considered, it can overcommit where a
  smaller fleet would have captured the same target.

### Contest Phase

Dominant mechanisms:

- friendly flip detection
- defense target insertion
- competitive score against enemy-held planets
- regroup pressure routing

This is where most nontrivial behavior appears. The agent does not simply expand;
it creates local counterfactuals for attack/defense and then pushes leftover
ships toward high-pressure owned planets.

### Snowball Phase

Once one side has stronger front-line points:

- those front-line points become high-pressure regroup destinations
- they receive reinforcement
- they become strong future sources
- the greedy selector can fire multiple high-impact moves in later turns

This is exactly what happened in self-play: a few non-mirrored middle-game
choices gave player 1 better front-line garrisons; regroup then amplified the
difference.

### Late Phase

After step 350:

- attacks arriving too late are removed
- neutral targets are devalued
- if behind enough, dynamic ROI can drop further

The current package does not include the aggressive "terminal phase" from
`orbit-wars-ver-02`.

## 17. Self-Play Decision Cause: Why The Validation Game Was Not Symmetric

Replay note:

`steps[i].action` in replay is best interpreted as the action visible at that
frame after the previous decision has entered the environment. For code-source
cause analysis, inspect observation step `N` to explain replay action at step
`N+1`.

Observed validation `80405449`:

- step 0 to 100: both sides remain effectively mirrored.
- step 111 to 129: choices diverge.
- step 237: player 0 eliminated, player 1 wins.

Root code causes:

1. Candidate tie-break is deterministic by ascending candidate index, not by
   geometric symmetry. Mirror planets have different slots.
2. Attack candidates and regroup candidates are selected by separate mechanisms.
   A replay action may be a regroup move even if attack scoring would not fire.
3. Full safe-drain sends create high leverage. Once a side picks a slightly
   better front-line target, the next few turns see larger safe drains from that
   front.
4. Defense targets can consume actions that look like attacks. A player that is
   slightly behind can spend large moves restoring a projected flip while the
   other side spends large moves attacking.

Concrete sequence:

- Around the early 110s, player 1 produced larger offensive/front-line pressure
  moves while player 0 spent more on restoring/contesting recently flipped points.
- Around step 120 to 125, player 1 gained stronger ownership/control around
  high-pressure targets. The regroup layer then pushed more leftover ships into
  those front-line planets.
- At step 129, player 1 was able to launch a much larger three-source pressure
  sequence, while player 0 had smaller local responses. This is a consequence of
  earlier safe-drain/regroup positioning, not a standalone hard-coded choice.

## 18. Related Alyce Notebook Lineage

### 18.1 Light Intruder

The Light Intruder notebook explicitly states the simplified design:

- no GRU
- no learned controller
- no multi-size tiers
- no FFA leader bonus module
- single-size safe-drain planner

This is the code reproduced in `agents/public/alyce_intruder_repro`.

### 18.2 Orbit Wars ver.02

This notebook contains a heavier architecture:

- TinyGRU controller class
- `USE_GRU_CONTROLLER = True`
- `GRU_WEIGHTS_AVAILABLE = False`
- feature history with 12-step sequence length and 24 global features
- heuristic fallback controller
- terminal phase after last 40 turns
- multi-size candidate tiers
- FFA leader/prod/spread/weak-player adjustments

Important:

Because weights are not available in the notebook state, this is not evidence of
an active trained policy. It is a controller shell plus heuristic fallback unless
weights are supplied.

### 18.3 ELO1245 ASCS

This notebook has a similar controller idea:

- TinyGRU controller class
- 24-d global features
- 12-step history
- config adjustment output
- fallback to heuristic controller when weights are unavailable
- FFA multiplier logic for ahead/behind and anti-snowball behavior

Again, `GRU_WEIGHTS_AVAILABLE = False` in the local pulled notebook. Treat it as
design intent, not a reproduced trained agent.

### 18.4 Intervention Command w/ FFA

This notebook is a Producer V3 style heavier planner:

- multi-tier drain choices including full commit
- FFA leader attack bonus
- target production bonus
- dynamic ROI and wave count
- regroup fade
- explicit comet evacuation helper
- warmup helper

It is closer to a high-complexity targeted 4P heuristic than Light Intruder.
However, it is not the active code in the submitted Alyce Intruder reproduction.

## 19. Training / Deep Decision Layer

Current package:

- no training loop
- no optimizer
- no gradient update
- no checkpoint
- no embedded model weights
- `agent(obs)` runs under `torch.no_grad()`
- Torch is used as a vectorized numeric engine, not as a learned policy runtime

Related notebooks:

- define TinyGRU strategy controllers
- define global feature extraction
- define history padding
- define config clamp/adaptation
- fall back to heuristic controller when weights unavailable

Therefore:

- The active Light Intruder is a handcrafted world-model heuristic.
- The "deep" part is the exact predictive simulation and vectorized candidate
  scoring, not neural training.
- Any future trained/controller reproduction would require locating real weights
  or training code. The local Alyce notebooks do not provide enough evidence to
  claim an active trained GRU policy.

## 20. Strategic Strengths

1. Accurate future geometry:
   - moving planets
   - comets
   - swept contact
   - intercept aiming

2. Capture legality is stronger than naive bots:
   - capture floor uses projected defenders
   - pressure margin accounts for enemy reinforcement risk

3. Local counterfactual scoring:
   - attacks are scored by projected competitive ship delta, not only distance.

4. Fast expansion and fast punishment:
   - safe-drain allows large moves when projected safe.

5. Regroup layer:
   - unused ships are not left idle if a nearby owned planet is under pressure.

## 21. Strategic Weaknesses

1. Single-size full safe-drain only:
   - can overcommit where a smaller fleet is enough.
   - lacks 50/75/100 tier choice from heavier Alyce variants.

2. No explicit FFA leader logic:
   - 4P behavior may not attack runaway leaders aggressively enough.

3. No active learned controller:
   - cannot adapt config from trained sequence patterns.

4. Tie-break is slot-index based:
   - deterministic but can be seat-sensitive in symmetric maps.

5. Regroup can mask intent:
   - moves that look like attacks may be reinforcement routes, making local
     replay interpretation harder.

6. Late game is conservative compared with heavier variants:
   - no terminal all-in phase before step 500.

## 22. Implications For Our Next Agent

Do not treat Alyce Intruder as a black-box "highest model"; treat it as a strong
lightweight world-model heuristic. Useful components to borrow or modify:

1. Keep the movement/garrison projection model.
2. Add multi-size drain tiers before adding any opponent profiler.
3. Add action safety filters around full safe-drain source depletion.
4. Add explicit 4P leader/kingmaker scoring only after measuring 4P episodes.
5. Add late terminal policy separately from opening/midgame logic.
6. If using controller ideas, first confirm real weights or build a local
   training/evaluation pipeline. Do not assume the GRU notebooks are trained.

Recommended low-risk improvement order:

1. Instrument chosen candidate into attack vs regroup move labels.
2. Reproduce a few public episodes and classify which moves are attack, defense,
   or regroup.
3. Add multi-size candidate tiers: floor-sized, 50%, 75%, 100% safe-drain.
4. Add reserve floor for source planets that are high production or recently
   threatened.
5. Add 4P FFA leader bonus only in 4P and only with small bounded weight.
6. Add terminal all-in only after step 430 or when losing and no future value
   remains.

## 23. Bottom Line

Alyce Intruder is not a neural trained model in its submitted Light form. It is a
compact Producer-family heuristic built around:

- predictive movement
- exact garrison projection
- safe-drain full-size candidate generation
- competitive ship-delta scoring
- greedy wave selection
- pressure-gradient regroup

The most important implementation insight is that attack selection and regroup
selection are separate. A complete decision explanation must label both layers;
otherwise key replay moves will be misattributed to the attack scorer.

## 24. Addendum: Alyce ELO / Opponent Strategy Recheck

Follow-up recheck: `reports/ALYCE_ELO_AND_OPPONENT_STRATEGY_RECHECK.md`.

Correction to framing: this report describes the submitted Light Intruder package.
It should not be read as a full description of Alyce Miki's broader Orbit Wars
strategy line. Alyce's related notebooks include explicit ELO/mode/opponent-state
ideas:

- separate 2P / 4P strategy presets
- low-ELO vs high-ELO meta-game comments
- ahead/even/behind ROI and wave control
- stronger-enemy reinforcement-risk handling
- 4P leader pressure and anti-kingmaker logic
- late-game urgency / regroup fade in heavier variants

Light Intruder removes many of those modules on purpose. A stronger reproduction
should keep the Light Intruder movement/projection core, then selectively restore
the safer Intervention/ver.02 controller pieces instead of treating Light Intruder
as the complete Alyce strategy.
