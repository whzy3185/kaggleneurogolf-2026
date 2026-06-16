# Counter Policy Design

Date: 2026-06-16

Implemented files:

| File | Purpose |
|---|---|
| `src/orbitwars_agent/strategy_modifiers.py` | shared dataclass for safe strategy modifiers |
| `src/orbitwars_agent/counter_policy.py` | confidence-gated profile-to-modifier rules |

Counter rules:

| Profile signal | Gate | Modifier |
|---|---|---|
| `enemy_rusher` | score * confidence > 0.55 | reserve up, defense up, expansion down, max commit down |
| `neutral_rusher` | score * confidence > 0.55 | counterattack bonus, mild target enemy bias |
| `turtle` | score * confidence > 0.55 | attack down, expansion up, comet up |
| `big_stack` | score * confidence > 0.55 | defense up, counterattack bonus |
| `overcommitter` | score * confidence > 0.55 | counterattack bonus, max commit slightly up |
| `comet_greedy` | score * confidence > 0.55 | comet weight up |

Design constraint:

No rule directly emits actions or swaps the full strategy. Rules only change
weights, reserve floors, commit ratios, and per-enemy bias. This limits damage
from early false positives.

Validation:

```powershell
$env:PYTHONPATH='E:\orbitwars_adaptive_agent\src'
python -m pytest tests\test_counter_policy.py -q
```

Result: pass.

