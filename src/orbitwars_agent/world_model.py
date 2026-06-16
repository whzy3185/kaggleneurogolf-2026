from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Optional

from .physics import distance_xy, eta, fleet_speed, segment_distance_to_point
from .types import FleetState, GameState, PlanetState


def _obs_get(obs: Any, name: str, default: Any) -> Any:
    if isinstance(obs, dict):
        return obs.get(name, default)
    return getattr(obs, name, default)


def _planet(raw: Iterable[Any]) -> PlanetState:
    if isinstance(raw, PlanetState):
        return raw
    pid, owner, x, y, radius, ships, production = raw
    return PlanetState(int(pid), int(owner), float(x), float(y), float(radius), int(ships), int(production))


def _fleet(raw: Iterable[Any]) -> FleetState:
    if isinstance(raw, FleetState):
        return raw
    fid, owner, x, y, angle, from_planet_id, ships = raw
    return FleetState(int(fid), int(owner), float(x), float(y), float(angle), int(from_planet_id), int(ships))


def build_game_state(obs: Any, inferred_step: int = 0) -> GameState:
    planets = [_planet(raw) for raw in _obs_get(obs, "planets", [])]
    fleets = [_fleet(raw) for raw in _obs_get(obs, "fleets", [])]
    initial_raw = _obs_get(obs, "initial_planets", [])
    initial_planets = [_planet(raw) for raw in initial_raw] if initial_raw else planets
    comet_ids = {int(pid) for pid in _obs_get(obs, "comet_planet_ids", [])}
    step = int(_obs_get(obs, "step", inferred_step))
    return GameState(
        step=step,
        player=int(_obs_get(obs, "player", 0)),
        angular_velocity=float(_obs_get(obs, "angular_velocity", 0.0)),
        planets=planets,
        fleets=fleets,
        initial_planets=initial_planets,
        comet_planet_ids=comet_ids,
        comets=_obs_get(obs, "comets", []),
        remaining_overage_time=_obs_get(obs, "remainingOverageTime", None),
    )


def get_my_planets(state: GameState) -> List[PlanetState]:
    return state.my_planets


def get_enemy_planets(state: GameState) -> List[PlanetState]:
    return state.enemy_planets


def get_neutral_planets(state: GameState) -> List[PlanetState]:
    return state.neutral_planets


def get_enemy_ids(state: GameState) -> list[int]:
    return sorted({planet.owner for planet in state.planets if planet.owner not in (-1, state.player)})


def likely_fleet_target(
    fleet: FleetState,
    state: GameState,
    horizon_turns: int = 80,
    radius_margin: float = 1.5,
) -> Optional[PlanetState]:
    speed = fleet_speed(fleet.ships)
    end_x = fleet.x + math.cos(fleet.angle) * speed * horizon_turns
    end_y = fleet.y + math.sin(fleet.angle) * speed * horizon_turns
    candidates: List[tuple[float, float, PlanetState]] = []
    for planet in state.planets:
        if planet.id == fleet.from_planet_id:
            continue
        miss = segment_distance_to_point(fleet.x, fleet.y, end_x, end_y, planet.x, planet.y)
        if miss <= planet.radius + radius_margin:
            progress = distance_xy(fleet.x, fleet.y, planet.x, planet.y)
            candidates.append((miss, progress, planet))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


def infer_fleet_target(fleet: FleetState, state: GameState, horizon_turns: int = 80) -> Optional[PlanetState]:
    return likely_fleet_target(fleet, state, horizon_turns=horizon_turns)


def incoming_fleets_by_planet(state: GameState) -> Dict[int, List[FleetState]]:
    incoming: Dict[int, List[FleetState]] = {}
    for fleet in state.fleets:
        target = likely_fleet_target(fleet, state)
        if target is not None:
            incoming.setdefault(target.id, []).append(fleet)
    return incoming


def compute_incoming_fleets_by_planet(state: GameState) -> Dict[int, List[FleetState]]:
    return incoming_fleets_by_planet(state)


def predict_garrison_at_arrival(state: GameState, planet_id: int, turns: int) -> int:
    planet = state.planets_by_id.get(planet_id)
    if planet is None:
        return 0
    garrison = planet.ships
    if planet.owner != -1:
        garrison += max(0, int(turns)) * max(0, planet.production)
    for fleet in incoming_fleets_by_planet(state).get(planet_id, []):
        dist = distance_xy(fleet.x, fleet.y, planet.x, planet.y)
        if eta(dist, fleet.ships) <= turns:
            if fleet.owner == planet.owner:
                garrison += fleet.ships
            else:
                garrison -= fleet.ships
    return garrison


def detect_threatened_own_planets(state: GameState, horizon_turns: int = 80) -> list[PlanetState]:
    threatened: list[PlanetState] = []
    incoming = incoming_fleets_by_planet(state)
    for planet in state.my_planets:
        enemy_pressure = 0
        for fleet in incoming.get(planet.id, []):
            if fleet.owner != state.player:
                dist = distance_xy(fleet.x, fleet.y, planet.x, planet.y)
                if eta(dist, fleet.ships) <= horizon_turns:
                    enemy_pressure += fleet.ships
        if enemy_pressure > planet.ships:
            threatened.append(planet)
    return threatened
