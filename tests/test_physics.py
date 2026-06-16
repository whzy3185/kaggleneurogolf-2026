import math

from orbitwars_agent.physics import (
    angle_to,
    distance,
    eta_turns,
    fleet_speed,
    is_orbiting_planet,
    segment_intersects_sun,
)
from orbitwars_agent.types import Planet


def test_distance_angle_and_speed():
    a = Planet(0, 0, 0.0, 0.0, 1.0, 10, 1)
    b = Planet(1, -1, 3.0, 4.0, 1.0, 10, 1)
    assert distance(a, b) == 5.0
    assert math.isclose(angle_to(a, b), math.atan2(4.0, 3.0))
    assert fleet_speed(1) == 1.0
    assert fleet_speed(1000) == 6.0
    assert eta_turns(10.0, 1) == 10


def test_sun_and_orbiting_checks():
    assert segment_intersects_sun(0.0, 50.0, 100.0, 50.0)
    assert not segment_intersects_sun(0.0, 0.0, 10.0, 0.0)
    inner = Planet(0, -1, 60.0, 50.0, 1.0, 5, 1)
    outer = Planet(1, -1, 95.0, 95.0, 1.0, 5, 1)
    assert is_orbiting_planet(inner)
    assert not is_orbiting_planet(outer)

