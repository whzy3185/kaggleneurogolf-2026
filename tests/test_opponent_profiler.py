import math

from orbitwars_agent.opponent_profiler import OpponentProfiler
from orbitwars_agent.world_model import build_game_state


def _state(step, planets, fleets=None, player=0):
    return build_game_state(
        {
            "player": player,
            "step": step,
            "planets": planets,
            "initial_planets": planets,
            "fleets": fleets or [],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )


def test_observed_turns_counts_each_enemy_once_per_update():
    profiler = OpponentProfiler()
    planets = [
        [0, 0, 10.0, 10.0, 2.0, 20, 2],
        [1, 1, 80.0, 80.0, 2.0, 40, 2],
        [2, 1, 60.0, 80.0, 2.0, 10, 3],
        [3, 1, 80.0, 60.0, 2.0, 10, 3],
    ]

    profile = profiler.update(_state(1, planets))[1]
    assert profile.observed_turns == 1
    assert profile.confidence < 0.02

    profile = profiler.update(_state(2, planets))[1]
    assert profile.observed_turns == 2
    assert profile.confidence < 0.02


def test_profiler_records_new_enemy_fleet_and_scores():
    profiler = OpponentProfiler()
    prev = build_game_state(
        {
            "player": 0,
            "step": 1,
            "planets": [
                [0, 0, 10.0, 10.0, 2.0, 20, 2],
                [1, 1, 80.0, 80.0, 2.0, 40, 2],
                [2, -1, 60.0, 80.0, 2.0, 6, 4],
            ],
            "initial_planets": [],
            "fleets": [],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )
    profiler.update(prev)

    current = build_game_state(
        {
            "player": 0,
            "step": 2,
            "planets": prev.planets,
            "initial_planets": [],
            "fleets": [
                [9, 1, 79.0, 80.0, 3.1415926535, 1, 30],
            ],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )
    profiles = profiler.update(current)
    profile = profiles[1]
    assert profile.observed_new_fleets == 1
    assert profile.total_ships_sent == 30
    assert profile.confidence > 0
    assert "enemy_rusher" in profile.scores


def test_enemy_rusher_rises_on_early_attack_against_own_planet():
    profiler = OpponentProfiler()
    planets = [
        [0, 0, 10.0, 10.0, 2.0, 20, 2],
        [1, 1, 80.0, 80.0, 2.0, 80, 2],
    ]
    profiler.update(_state(1, planets))

    angle = math.atan2(10.0 - 79.0, 10.0 - 79.0)
    profile = profiler.update(
        _state(
            10,
            planets,
            fleets=[
                [21, 1, 79.0, 79.0, angle, 1, 25],
            ],
        )
    )[1]

    assert profile.own_target_count == 1
    assert profile.enemy_rusher > 0.5


def test_neutral_rusher_rises_on_repeated_neutral_targets():
    profiler = OpponentProfiler()
    planets = [
        [0, 0, 10.0, 10.0, 2.0, 20, 2],
        [1, 1, 80.0, 80.0, 2.0, 100, 2],
        [2, -1, 60.0, 80.0, 2.0, 5, 3],
    ]
    profiler.update(_state(1, planets))

    fleets = [
        [30 + idx, 1, 79.0, 80.0, math.pi, 1, 10]
        for idx in range(5)
    ]
    profile = profiler.update(_state(12, planets, fleets=fleets))[1]

    assert profile.neutral_target_count == 5
    assert profile.neutral_rusher > 0.7


def test_weak_bot_signal_is_not_fixed_at_zero():
    profiler = OpponentProfiler()
    planets = [
        [0, 0, 10.0, 10.0, 2.0, 20, 2],
        [1, 1, 80.0, 80.0, 2.0, 100, 2],
        [2, -1, 60.0, 80.0, 2.0, 2, 0],
    ]
    profiler.update(_state(1, planets))

    fleets = [
        [40 + idx, 1, 79.0, 80.0, math.pi, 1, 1]
        for idx in range(6)
    ]
    profile = profiler.update(_state(20, planets, fleets=fleets))[1]

    assert profile.low_prod_target_count == 6
    assert profile.small_fleet_count == 6
    assert profile.weak_bot > 0.5


def test_profiler_exports_profile_snapshot():
    profiler = OpponentProfiler()
    planets = [
        [0, 0, 10.0, 10.0, 2.0, 20, 2],
        [1, 1, 80.0, 80.0, 2.0, 100, 2],
    ]
    profiler.update(_state(3, planets))

    exported = profiler.export_profiles(step=3)
    assert exported["step"] == 3
    assert "1" in exported["profiles"]
    assert exported["profiles"]["1"]["enemy_id"] == 1
    assert "scores" in exported["profiles"]["1"]


def test_profiler_detects_reinforce_heavy_targeting():
    profiler = OpponentProfiler()
    prev = build_game_state(
        {
            "player": 0,
            "step": 1,
            "planets": [
                [0, 0, 10.0, 10.0, 2.0, 20, 2],
                [1, 1, 80.0, 80.0, 2.0, 40, 2],
                [2, 1, 60.0, 80.0, 2.0, 6, 4],
            ],
            "initial_planets": [],
            "fleets": [],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )
    profiler.update(prev)

    current = build_game_state(
        {
            "player": 0,
            "step": 2,
            "planets": prev.planets,
            "initial_planets": [],
            "fleets": [
                [10, 1, 79.0, 80.0, 3.1415926535, 1, 12],
            ],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )

    profile = profiler.update(current)[1]
    assert profile.self_target_count == 1
    assert profile.reinforce_heavy > 0


def test_profiler_detects_conflict_and_weakest_targeting():
    profiler = OpponentProfiler()
    prev = build_game_state(
        {
            "player": 0,
            "step": 1,
            "planets": [
                [0, 0, 10.0, 10.0, 2.0, 20, 2],
                [1, 1, 80.0, 80.0, 2.0, 50, 3],
                [2, 2, 60.0, 80.0, 2.0, 5, 1],
                [3, 3, 40.0, 80.0, 2.0, 50, 3],
            ],
            "initial_planets": [],
            "fleets": [],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )
    profiler.update(prev)

    current = build_game_state(
        {
            "player": 0,
            "step": 2,
            "planets": prev.planets,
            "initial_planets": [],
            "fleets": [
                [11, 1, 79.0, 80.0, 3.1415926535, 1, 20],
                [12, 3, 41.0, 80.0, 0.0, 3, 20],
            ],
            "comet_planet_ids": [],
            "angular_velocity": 0.0,
        }
    )

    profile = profiler.update(current)[1]
    assert profile.weak_enemy_target_count == 1
    assert profile.conflict_target_count == 1
    assert profile.weakest_targeter > 0
    assert profile.crash_exploiter > 0
