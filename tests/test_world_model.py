from orbitwars_agent.world_model import (
    build_game_state,
    compute_incoming_fleets_by_planet,
    detect_threatened_own_planets,
    get_enemy_ids,
    get_my_planets,
    predict_garrison_at_arrival,
)


def _obs():
    return {
        "player": 0,
        "step": 12,
        "angular_velocity": 0.03,
        "remainingOverageTime": 8.0,
        "comet_planet_ids": [],
        "initial_planets": [
            [0, 0, 10.0, 10.0, 2.0, 10, 2],
            [1, 1, 20.0, 10.0, 2.0, 20, 2],
        ],
        "planets": [
            [0, 0, 10.0, 10.0, 2.0, 10, 2],
            [1, 1, 20.0, 10.0, 2.0, 20, 2],
        ],
        "fleets": [
            [7, 1, 19.0, 10.0, 3.1415926535, 1, 15],
        ],
    }


def test_build_game_state_helpers():
    state = build_game_state(_obs())
    assert state.player_id == 0
    assert state.remaining_overage_time == 8.0
    assert [p.id for p in get_my_planets(state)] == [0]
    assert get_enemy_ids(state) == [1]


def test_incoming_and_threat_detection():
    state = build_game_state(_obs())
    incoming = compute_incoming_fleets_by_planet(state)
    assert 0 in incoming
    assert predict_garrison_at_arrival(state, 0, 20) < 10 + 2 * 20
    threatened = detect_threatened_own_planets(state, horizon_turns=20)
    assert [p.id for p in threatened] == [0]

