from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StrategyModifiers:
    reserve_floor_delta: int = 0
    defense_weight_mult: float = 1.0
    expansion_weight_mult: float = 1.0
    attack_weight_mult: float = 1.0
    center_weight_mult: float = 1.0
    comet_weight_mult: float = 1.0
    counterattack_bonus: float = 0.0
    risky_expansion_penalty: float = 0.0
    max_commit_ratio_delta: float = 0.0
    target_enemy_bias: dict[int, float] = field(default_factory=dict)

