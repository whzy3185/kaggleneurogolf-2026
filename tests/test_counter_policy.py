from orbitwars_agent.counter_policy import build_strategy_modifiers
from orbitwars_agent.opponent_profiler import OpponentProfile


def _profile(enemy_id: int, key: str, score: float, confidence: float = 1.0) -> OpponentProfile:
    p = OpponentProfile(enemy_id=enemy_id, observed_turns=60, new_fleets_count=8)
    p.scores = {key: score, "confidence": confidence}
    return p


def test_enemy_rusher_modifies_defense_and_reserve():
    mods = build_strategy_modifiers({1: _profile(1, "enemy_rusher", 0.8)})
    assert mods.reserve_floor_delta >= 5
    assert mods.defense_weight_mult > 1.0
    assert mods.expansion_weight_mult < 1.0
    assert mods.max_commit_ratio_delta < 0


def test_neutral_rusher_adds_counter_bias_without_killing_expansion():
    mods = build_strategy_modifiers({2: _profile(2, "neutral_rusher", 0.8)})
    assert mods.counterattack_bonus >= 10.0
    assert 0.85 <= mods.expansion_weight_mult <= 1.0
    assert mods.target_enemy_bias[2] > 1.0


def test_turtle_and_comet_policy():
    mods = build_strategy_modifiers(
        {
            1: _profile(1, "turtle", 0.8),
            2: _profile(2, "comet_greedy", 0.8),
        }
    )
    assert mods.attack_weight_mult < 1.0
    assert mods.expansion_weight_mult > 1.0
    assert mods.comet_weight_mult > 1.0


def test_reinforce_heavy_adds_pressure_without_large_reserve_shift():
    mods = build_strategy_modifiers({1: _profile(1, "reinforce_heavy", 0.8)})
    assert mods.attack_weight_mult > 1.0
    assert mods.expansion_weight_mult < 1.0
    assert mods.counterattack_bonus >= 6.0


def test_crash_and_weakest_targeter_raise_defensive_reserve():
    mods = build_strategy_modifiers(
        {
            1: _profile(1, "crash_exploiter", 0.8),
            2: _profile(2, "weakest_targeter", 0.8),
        }
    )
    assert mods.reserve_floor_delta >= 7
    assert mods.defense_weight_mult > 1.0
    assert mods.max_commit_ratio_delta < 0


def test_enabled_policies_filter_counter_branches():
    mods = build_strategy_modifiers(
        {
            1: _profile(1, "neutral_rusher", 0.8),
            2: _profile(2, "enemy_rusher", 0.8),
        },
        enabled_policies=("enemy_rusher",),
    )
    assert mods.reserve_floor_delta >= 5
    assert mods.defense_weight_mult > 1.0
    assert mods.counterattack_bonus == 0.0
    assert mods.target_enemy_bias == {}
