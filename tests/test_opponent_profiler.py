from orbitwars_agent.opponent_profiler import OpponentProfiler
from orbitwars_agent.world_model import build_game_state


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
