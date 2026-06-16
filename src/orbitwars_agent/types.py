from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Set


@dataclass(frozen=True)
class PlanetState:
    id: int
    owner: int
    x: float
    y: float
    radius: float
    ships: int
    production: int


@dataclass(frozen=True)
class FleetState:
    id: int
    owner: int
    x: float
    y: float
    angle: float
    from_planet_id: int
    ships: int


@dataclass
class GameState:
    step: int
    player: int
    angular_velocity: float
    planets: List[PlanetState]
    fleets: List[FleetState]
    initial_planets: List[PlanetState]
    comet_planet_ids: Set[int]
    comets: List[Any] | None = None
    remaining_overage_time: float | None = None

    @property
    def player_id(self) -> int:
        return self.player

    @property
    def planets_by_id(self) -> Dict[int, PlanetState]:
        return {planet.id: planet for planet in self.planets}

    @property
    def initial_planets_by_id(self) -> Dict[int, PlanetState]:
        return {planet.id: planet for planet in self.initial_planets}

    @property
    def my_planets(self) -> List[PlanetState]:
        return [planet for planet in self.planets if planet.owner == self.player]

    @property
    def enemy_planets(self) -> List[PlanetState]:
        return [planet for planet in self.planets if planet.owner not in (-1, self.player)]

    @property
    def neutral_planets(self) -> List[PlanetState]:
        return [planet for planet in self.planets if planet.owner == -1]

    @property
    def enemy_fleets(self) -> List[FleetState]:
        return [fleet for fleet in self.fleets if fleet.owner != self.player]

    @property
    def my_fleets(self) -> List[FleetState]:
        return [fleet for fleet in self.fleets if fleet.owner == self.player]


Planet = PlanetState
Fleet = FleetState

