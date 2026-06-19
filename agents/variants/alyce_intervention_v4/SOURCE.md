# Alyce Intervention V4 Source

Source id: `alyce_intervention_v4`

Base package:

- Kaggle output slug: `alycemiki/intervention-command-w-ffa`
- Local upstream source: `external/kaggle_outputs/alycemiki__intervention-command-w-ffa/submission_extracted`
- Immediate implementation parent: `agents/variants/alyce_intervention_v3`
- Package type: multi-file submission with `main.py` and `orbit_lite/`

V4 changes:

- Preserves the full Alyce Intervention package structure.
- Keeps the v15 planner mechanisms: dynamic ROI, full safe-drain options,
  floor-sized fleets, fractional fleet tiers, regroup fade, comet handling, and
  4P FFA anti-snowball bonuses.
- Replaces the V3 static far-low target penalty with a 4P context scorer.
- Adds candidate-level labels for production rank, leader, reaction distance,
  rough holdability, high-production source depletion, safe neutral, trap
  neutral, low-value non-leader enemy, and low-value leader target with weak
  holdability.
- Keeps all changes as soft score adjustments, not hard action deletion.

Reason:

- V3 official replay review showed that static far-low penalties were
  insufficient.
- The repeated failure pattern is 4P production collapse around turns 50-100,
  often caused by a mixture of weak holdability, leader-pressure mistakes,
  attack-over-regroup behavior, and source depletion.
- V4 is meant to test a narrower, context-aware scoring layer without removing
  Alyce Intervention's core tempo.

Attribution:

- Original public Kaggle output belongs to Alyce Miki.
- This repository records the modification path for local evaluation and does
  not claim the public output score as our own official score.
