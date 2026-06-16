# Public Agent Summary

Date: 2026-06-16

Best immediate candidates:

| Rank | Candidate | Why |
|---:|---|---|
| 1 | `pilkwang_structured` | Layered Physics + WorldModel + Strategy, clear scoring hooks, Apache 2.0, already in lab |
| 2 | `vkhydras_peak_heuristic` | Highest cloned heuristic claim, detailed lineage, strong replay-analysis notes |
| 3 | `tamrazov_starwars` | Highest bundled Kaggle claim, simulation-based, useful benchmark |
| 4 | `ykhnkf_distance_prioritized` | Strong bundled claim, likely close to Pilkwang family structure |
| 5 | `sigmaborov_reinforce` | Lower claim but compact and readable, good implementation reference |

Integration observations:

- The strongest public heuristic agents already have physics prediction,
  arrival logic, defense/reinforcement, and scoring functions.
- The gap for our differentiated work is not "write another nearest target
  bot"; it is to add opponent tendency profiling as a conservative scoring
  modifier on top of an already strong baseline.
- `vkhydras` explicitly notes that self-play can overfit, and that evaluator
  correctness around enemy reactive snipes mattered more than simple
  aggression tuning. This supports using held-out public opponents instead of
  mirror-only validation.

Current base-agent lean:

`pilkwang_structured` is the safest first base candidate because it is Apache
2.0, already bundled by `orbit-wars-lab`, has a clear world-model architecture,
and is easier to patch than the largest high-claim variants. This is a
pre-tournament lean, not a final decision.

