# Alyce Miki ELO / Opponent Strategy Recheck

Date: 2026-06-18

## 1. Scope

This recheck focuses on the user's question: Alyce Miki's Orbit Wars code/discussion
material mentions ELO and different strategies against different opponents. The
previous full code report correctly described the submitted Light Intruder package,
but it was incomplete as a description of Alyce's broader strategy line.

Checked sources:

- Kaggle Code: `alycemiki/elo1245-a-simple-but-considerate-solution`
- Kaggle Code: `alycemiki/intervention-command-w-ffa`
- Kaggle Code: `alycemiki/orbit-wars-ver-02`
- Kaggle Code: `alycemiki/light-ver-1200-simple-orbit-intruder`
- Kaggle competition Discussion topic `704777`: Proportion of 4P vs 2P for top players
- Kaggle competition Discussion topic `707953`: gained Elo after losing 4-player game
- Kaggle competition Discussion topic `705041`: leaderboard reset / ELO fairness

Important access note:

- Competition Discussion topics are accessible through the current Kaggle CLI.
- Code notebook contents are accessible through `kaggle kernels pull`.
- Kaggle Code page comment threads are not exposed by the current Kaggle CLI
  session. I did not fabricate hidden notebook comments.

## 2. Corrected Conclusion

Yes, Alyce's related Code material explicitly includes ELO-aware and
opponent-strength-aware strategy ideas.

However, those ideas are not all active in the Light Intruder submission package.
The Alyce line should be read as a sequence:

1. `orbit-wars-ver-02`: heavier mode-aware controller ideas.
2. `intervention-command-w-ffa`: Producer-derived FFA/intervention version with
   explicit meta-game notes.
3. `elo1245-a-simple-but-considerate-solution`: ASCS controller with 24-feature
   history and GRU shell, but no active learned weights.
4. `light-ver-1200-simple-orbit-intruder`: intentionally simplified final-style
   lightweight package with no GRU, no FFA bonus module, and single-size planning.

Therefore:

- Light Intruder is a simplified heuristic package.
- Alyce's broader design thinking is clearly mode-aware and opponent-aware.
- If we use Alyce as a base or inspiration, we should not copy only Light Intruder;
  we should reintroduce the safest parts of the heavier controller line.

## 3. ELO / Meta-Game Evidence

### 3.1 ASCS / ELO1245

The ELO1245 notebook states that one solution is not enough across:

- 2-player vs 4-player games
- quick vs long games
- different ELO bands

Its controller uses a 24-dimensional global feature vector and a 12-step history.
The active fallback is heuristic because GRU weights are not embedded.

Main controller branches:

- Ahead: raise ROI, reduce waves, damp FFA aggression.
- Even: keep neutral tempo.
- Behind: lower ROI, increase waves, increase FFA pressure.
- 4P under strong enemy pressure: increase FFA aggression.
- Late behind: reduce ROI further and add waves.

This is not direct opponent-name recognition. It is opponent-state recognition:
relative strength, production gap, leader gap, player count, and time.

### 3.2 Intervention Command w/ FFA

This notebook is the clearest source for the user's point.

It explicitly frames separate 2P and 4P configs as a meta-game choice. Its key
claim is that low-ELO and high-ELO match contexts reward different modes: 4P
pressure matters heavily in lower bands, while 2P survival matters more in higher
bands.

Its opponent-differentiation logic is also explicit:

- When trailing in 2P, it avoids feeding into stronger opponents by using a
  higher trailing ROI and a higher reinforcement-risk beta.
- In 4P it lowers ROI and uses smaller fleets, but keeps reinforcement safety.
- Weak enemies imply a lower reinforcement floor and more aggression.
- Strong enemies imply a higher reinforcement floor and more conservative sends.
- In 4P it adds anti-snowball pressure against the strongest player.

This is important because the model does not need a separate "opponent profiler"
label to react differently. It uses pressure and strength proxies directly inside
the candidate score and safety floor.

### 3.3 Orbit Wars ver.02

This version makes the 2P/4P distinction sharper:

- In 2P, being ahead means pressing harder to snowball.
- In 4P, being ahead means playing safer to avoid overextension.
- In 4P, being behind means becoming more aggressive toward the leader.
- Very dominant enemy strength boosts leader-targeting pressure.
- Late game can override normal controller settings so ships are not left idle.
- It includes anti-kingmaker logic: avoid helping the leader by farming weak
  opponents who are already far behind.

This is the closest Alyce notebook to a complete mode policy:

- 2P: snowball and direct survival.
- 4P: leader suppression, anti-kingmaker, and controlled aggression.
- Late game: commit unused ships when future production no longer matters.

### 3.4 Light Intruder

Light Intruder deliberately removes several heavier modules:

- no GRU or learned controller
- no explicit FFA leader bonus module
- no multi-tier planner
- single-size safe-drain planner

It keeps:

- mode presets for 2P/3P/4P
- continuous ROI lowering when behind
- late urgency after step 350
- extra wave when behind or late
- movement/garrison projection
- safe-drain candidate generation

So the current reproduced Light Intruder is not the full Alyce strategy stack.
It is a compact subset.

## 4. Discussion Evidence

### 4.1 4P vs 2P proportions

Topic `704777` matters because it explains why mode split is not cosmetic. The
visible messages say top players appeared to receive mostly 2P games, while lower
rank bands could see many more 4P games. One visible comment summarizes that
top-player matchmaking can be close to all 2P due to few same-level opponents,
while top-200/top-300 may see around two-thirds 4P.

Implication:

- A single local 2P gauntlet is not enough.
- A candidate optimized for 4P can look strong at one rating band and weaker at
  another.
- Alyce's low-ELO/high-ELO wording is plausible as a meta-game adaptation, not
  just a code comment.

### 4.2 Elo movement in 4P

Topic `707953` reports a player losing a 4P game but gaining Elo. This does not
prove Alyce's strategy, but it reinforces that 4P rating movement is not a simple
win/loss binary. Rank, opponent uncertainty, and relative ratings can affect the
score.

Implication:

- Local "won/lost" labels are less informative for 4P than rank distribution and
  opponent rating context.
- A 4P strategy can be rational even if it does not always rank first, provided
  it avoids catastrophic last-place finishes against stronger pools.

### 4.3 Leaderboard reset / ELO fairness

Topic `705041` discusses final rating continuity and round-robin fairness. The
useful takeaway is not a final official answer, but that participants were aware
that rating history and match frequency could affect submission strategy.

Implication:

- The right validation target is not only "beats one public bot locally."
- We need 2P, 4P, position rotation, and stability against mixed-strength pools.

## 5. What "Different Enemies" Means In Alyce Code

Alyce does not appear to implement hard-coded enemy-name counters in the checked
notebooks. Instead, different enemy behavior is handled through measurable state:

| Enemy / match condition | Alyce-style response |
| --- | --- |
| We are ahead in 2P | lower or maintain ROI, keep pressure, snowball |
| We are ahead in 4P | raise ROI or damp FFA, avoid overextension |
| We are behind in 2P | lower ROI carefully, more waves, stronger reinforcement risk control |
| We are behind in 4P | lower ROI, increase leader pressure, avoid passive collapse |
| Enemy much stronger than us | higher safety floor / FFA pressure toward leader |
| Enemy weak | lower safety floor, more aggressive capture/attack |
| 4P runaway leader | add leader attack and target production bonuses |
| Weak non-leader target | penalize to avoid kingmaking |
| Late game | reduce ROI / add waves / disable wasteful regroup |
| High reinforcement threat | increase capture margin or avoid feeding |

This is a better model than our earlier "profile label then counter action"
approach because it changes the base planner's thresholds before action selection,
instead of appending late supplemental moves after the base has already spent
ships.

## 6. Implementation Implications For Our Next Agent

The actionable path is not to build a large external opponent profiler first.
The Alyce evidence points to a smaller and more robust design:

1. Mode policy:
   - separate 2P and 4P configs
   - 4P should include leader pressure and anti-kingmaker
   - 2P should prioritize direct snowball/survival

2. Relative-strength controller:
   - compute our strength, leader strength, enemy max strength, production gaps
   - adjust ROI, waves, FFA multiplier, and reserve floor before candidate scoring

3. Reinforcement-risk adaptation:
   - use stronger enemy pressure to increase required capture margin
   - avoid sending ships into targets that can be trivially reinforced

4. Multi-tier drain:
   - generate floor-sized, 50%, 75%, and full-drain candidates
   - avoid wasting full safe-drain when a smaller fleet already captures

5. Late-game override:
   - after a defined progress threshold, reduce ROI and fade regroup
   - near the end, unused ships on planets should be treated as wasted value

6. 4P anti-snowball:
   - attack leader when profitable
   - penalize attacks on weak non-leaders that help the leader

7. Evaluation:
   - validate 2P and 4P separately
   - include rank distribution, not only winrate
   - include position rotation
   - compare against Alyce Light Intruder, Producer-style candidates, and GRU-style
     public outputs

## 7. Correction To Existing Alyce Report

The existing `ALYCE_INTRUDER_FULL_CODE_DECISION_REPORT.md` is accurate for the
Light Intruder package, but it should not be read as "Alyce has no ELO/opponent
strategy ideas." Correct framing:

- Light Intruder: simplified heuristic submission.
- ASCS / Intervention / ver.02: broader Alyce design line with mode/ELO/relative
  strength strategy.
- Reproduction of Light Intruder alone is not enough for a targeted candidate.
- The next useful reproduction should preserve Alyce's safe core while restoring
  selected Intervention/ver.02 controller ideas.

## 8. Recommended Next Reproduction Target

Use Alyce Intruder only as the safe movement/projection base, then reproduce a
minimal "Alyce Controller v2" with these pieces:

1. Light Intruder movement and projection core.
2. Intervention-style dynamic ROI and reinforcement beta.
3. ver.02-style 2P/4P branch.
4. 4P leader bonus plus anti-kingmaker penalty.
5. Multi-tier drain candidates.
6. Late-game regroup fade.

Do not add:

- hard-coded opponent names
- unverified GRU weights
- late supplemental actions after ship budget is already spent
- local-only ELO assumptions as official score claims

## 9. Bottom Line

The user's concern is valid. Alyce's broader material does mention ELO and
different strategies for different match/opponent conditions. The current Light
Intruder reproduction is only the lightweight end of that line. For scoring
improvement, the next step should be to reconstruct the stronger Alyce-style
controller around mode split, strength ratio, reinforcement risk, FFA leader
pressure, anti-kingmaker logic, multi-tier drain, and late-game urgency.

