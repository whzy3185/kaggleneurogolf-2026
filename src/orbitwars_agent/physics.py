from __future__ import annotations

import math
from typing import Tuple

from .types import PlanetState

CENTER_X = 50.0
CENTER_Y = 50.0
SUN_RADIUS = 10.0
ROTATION_RADIUS_LIMIT = 50.0


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def distance_xy(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(ax - bx, ay - by)


def distance(a: PlanetState, b: PlanetState) -> float:
    return distance_xy(a.x, a.y, b.x, b.y)


def angle_to_xy(ax: float, ay: float, bx: float, by: float) -> float:
    return math.atan2(by - ay, bx - ax)


def angle_to_planet(source: PlanetState, target: PlanetState) -> float:
    return angle_to_xy(source.x, source.y, target.x, target.y)


def angle_to(source: PlanetState, target: PlanetState) -> float:
    return angle_to_planet(source, target)


def fleet_speed(ships: int, max_speed: float = 6.0) -> float:
    ships = max(1, int(ships))
    scale = (math.log(ships) / math.log(1000.0)) ** 1.5
    return 1.0 + (max_speed - 1.0) * scale


def eta(distance_value: float, ships: int) -> int:
    return max(1, int(math.ceil(distance_value / fleet_speed(ships))))


def eta_turns(distance_value: float, ships: int) -> int:
    return eta(distance_value, ships)


def is_orbiting(planet: PlanetState) -> bool:
    orbital_radius = distance_xy(planet.x, planet.y, CENTER_X, CENTER_Y)
    return orbital_radius + planet.radius < ROTATION_RADIUS_LIMIT


def is_orbiting_planet(planet: PlanetState) -> bool:
    return is_orbiting(planet)


def predict_orbit_position(
    planet: PlanetState,
    initial_planet: PlanetState | None,
    angular_velocity: float,
    future_step: int,
) -> Tuple[float, float]:
    base = initial_planet or planet
    radius = distance_xy(base.x, base.y, CENTER_X, CENTER_Y)
    if radius + base.radius >= ROTATION_RADIUS_LIMIT:
        return planet.x, planet.y
    base_angle = math.atan2(base.y - CENTER_Y, base.x - CENTER_X)
    angle = base_angle + angular_velocity * future_step
    return CENTER_X + math.cos(angle) * radius, CENTER_Y + math.sin(angle) * radius


def segment_distance_to_point(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    px: float,
    py: float,
) -> float:
    vx = bx - ax
    vy = by - ay
    wx = px - ax
    wy = py - ay
    denom = vx * vx + vy * vy
    if denom <= 1e-9:
        return distance_xy(ax, ay, px, py)
    t = clamp((wx * vx + wy * vy) / denom, 0.0, 1.0)
    cx = ax + t * vx
    cy = ay + t * vy
    return distance_xy(cx, cy, px, py)


def segment_intersects_circle(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    radius: float,
) -> bool:
    return segment_distance_to_point(ax, ay, bx, by, cx, cy) <= radius


def crosses_sun(ax: float, ay: float, bx: float, by: float, margin: float = 0.0) -> bool:
    return segment_intersects_circle(ax, ay, bx, by, CENTER_X, CENTER_Y, SUN_RADIUS + margin)


def segment_intersects_sun(ax: float, ay: float, bx: float, by: float, margin: float = 0.0) -> bool:
    return crosses_sun(ax, ay, bx, by, margin=margin)


def predict_comet_position(comet: dict, future_step: int) -> Tuple[float, float] | None:
    paths = comet.get("paths") if isinstance(comet, dict) else None
    path_index = comet.get("path_index", 0) if isinstance(comet, dict) else 0
    if not paths:
        return None
    first_path = paths[0]
    if not first_path:
        return None
    idx = min(len(first_path) - 1, max(0, int(path_index) + int(future_step)))
    point = first_path[idx]
    if len(point) < 2:
        return None
    return float(point[0]), float(point[1])
