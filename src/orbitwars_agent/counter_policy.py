from __future__ import annotations

from typing import Dict

from .opponent_profiler import OpponentProfile
from .strategy_modifiers import StrategyModifiers


def effective(profile: OpponentProfile, key: str) -> float:
    return profile.scores.get(key, 0.0) * profile.confidence


def build_strategy_modifiers(profiles: Dict[int, OpponentProfile]) -> StrategyModifiers:
    mods = StrategyModifiers()
    if not profiles:
        return mods

    enemy_rush = max(effective(profile, "enemy_rusher") for profile in profiles.values())
    neutral_rush = max(effective(profile, "neutral_rusher") for profile in profiles.values())
    turtle = max(effective(profile, "turtle") for profile in profiles.values())
    big_stack = max(effective(profile, "big_stack") for profile in profiles.values())
    overcommit = max(effective(profile, "overcommitter") for profile in profiles.values())
    comet = max(effective(profile, "comet_greedy") for profile in profiles.values())
    reinforce_heavy = max(effective(profile, "reinforce_heavy") for profile in profiles.values())
    crash_exploiter = max(effective(profile, "crash_exploiter") for profile in profiles.values())
    weakest_targeter = max(effective(profile, "weakest_targeter") for profile in profiles.values())

    if enemy_rush > 0.55:
        mods.reserve_floor_delta += 6
        mods.defense_weight_mult *= 1.4
        mods.expansion_weight_mult *= 0.9
        mods.risky_expansion_penalty += 0.25
        mods.max_commit_ratio_delta -= 0.10

    if neutral_rush > 0.55:
        mods.counterattack_bonus += 10.0
        mods.expansion_weight_mult *= 0.95
        for enemy_id, profile in profiles.items():
            if effective(profile, "neutral_rusher") > 0.55:
                mods.target_enemy_bias[enemy_id] = max(mods.target_enemy_bias.get(enemy_id, 1.0), 1.08)

    if turtle > 0.55:
        mods.attack_weight_mult *= 0.80
        mods.expansion_weight_mult *= 1.25
        mods.comet_weight_mult *= 1.15

    if big_stack > 0.55:
        mods.defense_weight_mult *= 1.25
        mods.counterattack_bonus += 8.0

    if overcommit > 0.55:
        mods.counterattack_bonus += 15.0
        mods.risky_expansion_penalty = max(0.0, mods.risky_expansion_penalty - 0.10)
        mods.max_commit_ratio_delta += 0.08

    if comet > 0.55:
        mods.comet_weight_mult *= 1.25

    if reinforce_heavy > 0.55:
        mods.attack_weight_mult *= 1.08
        mods.expansion_weight_mult *= 0.95
        mods.counterattack_bonus += 6.0

    if crash_exploiter > 0.55:
        mods.reserve_floor_delta += 4
        mods.defense_weight_mult *= 1.15
        mods.max_commit_ratio_delta -= 0.06

    if weakest_targeter > 0.55:
        mods.reserve_floor_delta += 3
        mods.defense_weight_mult *= 1.10

    return mods


__all__ = ["StrategyModifiers", "build_strategy_modifiers", "effective"]
