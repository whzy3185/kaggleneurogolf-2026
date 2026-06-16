from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .physics import CENTER_X, CENTER_Y, clamp, distance_xy
from .types import FleetState, GameState, PlanetState
from .world_model import likely_fleet_target


@dataclass
class OpponentProfile:
    enemy_id: int
    observed_turns: int = 0
    new_fleets_count: int = 0
    neutral_target_count: int = 0
    own_target_count: int = 0
    enemy_target_count: int = 0
    self_target_count: int = 0
    weak_enemy_target_count: int = 0
    conflict_target_count: int = 0
    center_target_count: int = 0
    high_prod_target_count: int = 0
    comet_target_count: int = 0
    total_ships_sent: int = 0
    large_fleet_count: int = 0
    overcommit_count: int = 0
    first_attack_turn: Optional[int] = None
    max_commit_ratio: float = 0.0
    scores: Dict[str, float] = field(default_factory=dict)

    @property
    def confidence(self) -> float:
        fleet_factor = min(1.0, self.new_fleets_count / 8.0)
        turn_factor = min(1.0, self.observed_turns / 60.0)
        return clamp(0.75 * fleet_factor + 0.25 * turn_factor)

    @property
    def observed_new_fleets(self) -> int:
        return self.new_fleets_count

    @property
    def estimated_overcommit_count(self) -> int:
        return self.overcommit_count

    @property
    def reinforce_count(self) -> int:
        return 0

    @property
    def neutral_rusher(self) -> float:
        return self.scores.get("neutral_rusher", 0.0)

    @property
    def enemy_rusher(self) -> float:
        return self.scores.get("enemy_rusher", 0.0)

    @property
    def turtle(self) -> float:
        return self.scores.get("turtle", 0.0)

    @property
    def center_greedy(self) -> float:
        return self.scores.get("center_greedy", 0.0)

    @property
    def production_greedy(self) -> float:
        return self.scores.get("production_greedy", 0.0)

    @property
    def big_stack_attacker(self) -> float:
        return self.scores.get("big_stack", 0.0)

    @property
    def comet_greedy(self) -> float:
        return self.scores.get("comet_greedy", 0.0)

    @property
    def overcommitter(self) -> float:
        return self.scores.get("overcommitter", 0.0)

    @property
    def weak_bot(self) -> float:
        return self.scores.get("weak_bot", 0.0)

    @property
    def reinforce_heavy(self) -> float:
        return self.scores.get("reinforce_heavy", 0.0)

    @property
    def crash_exploiter(self) -> float:
        return self.scores.get("crash_exploiter", 0.0)

    @property
    def weakest_targeter(self) -> float:
        return self.scores.get("weakest_targeter", 0.0)


class OpponentProfiler:
    def __init__(self) -> None:
        self.profiles: Dict[int, OpponentProfile] = {}
        self.seen_fleet_ids: Set[int] = set()
        self.previous_state: Optional[GameState] = None

    def update(self, state: GameState) -> Dict[int, OpponentProfile]:
        for planet in state.planets:
            if planet.owner not in (-1, state.player):
                self._profile(planet.owner).observed_turns += 1

        for fleet in state.fleets:
            if fleet.owner == state.player or fleet.owner == -1:
                continue
            if fleet.id in self.seen_fleet_ids:
                continue
            self.seen_fleet_ids.add(fleet.id)
            self._record_new_enemy_fleet(state, fleet)

        for profile in self.profiles.values():
            self._refresh_scores(profile)

        self.previous_state = state
        return self.profiles

    def get_profile(self, enemy_id: int) -> OpponentProfile:
        return self._profile(enemy_id)

    def get_all_profiles(self) -> Dict[int, OpponentProfile]:
        return dict(self.profiles)

    def _profile(self, enemy_id: int) -> OpponentProfile:
        if enemy_id not in self.profiles:
            self.profiles[enemy_id] = OpponentProfile(enemy_id=enemy_id)
        return self.profiles[enemy_id]

    def _record_new_enemy_fleet(self, state: GameState, fleet: FleetState) -> None:
        profile = self._profile(fleet.owner)
        profile.new_fleets_count += 1
        profile.total_ships_sent += max(0, fleet.ships)
        if fleet.ships >= 25:
            profile.large_fleet_count += 1

        target = likely_fleet_target(fleet, state)
        if target is not None:
            self._record_target(state, profile, fleet, target)

        commit_ratio = self._estimate_commit_ratio(fleet)
        profile.max_commit_ratio = max(profile.max_commit_ratio, commit_ratio)
        if commit_ratio >= 0.65:
            profile.overcommit_count += 1

    def _record_target(
        self,
        state: GameState,
        profile: OpponentProfile,
        fleet: FleetState,
        target: PlanetState,
    ) -> None:
        if target.owner == -1:
            profile.neutral_target_count += 1
        elif target.owner == state.player:
            profile.own_target_count += 1
            if profile.first_attack_turn is None:
                profile.first_attack_turn = state.step
        elif target.owner == fleet.owner:
            profile.self_target_count += 1
        else:
            profile.enemy_target_count += 1
            if target.owner == self._weakest_enemy_owner(state):
                profile.weak_enemy_target_count += 1

        if distance_xy(target.x, target.y, CENTER_X, CENTER_Y) < 25.0:
            profile.center_target_count += 1
        if target.production >= 4:
            profile.high_prod_target_count += 1
        if target.id in state.comet_planet_ids:
            profile.comet_target_count += 1
        if self._targets_existing_conflict(state, fleet, target):
            profile.conflict_target_count += 1

    def _estimate_commit_ratio(self, fleet: FleetState) -> float:
        if self.previous_state is None:
            return 0.0
        prev_planet = self.previous_state.planets_by_id.get(fleet.from_planet_id)
        if prev_planet is None or prev_planet.owner != fleet.owner:
            return 0.0
        available = max(1, prev_planet.ships)
        return clamp(fleet.ships / available)

    def _refresh_scores(self, profile: OpponentProfile) -> None:
        total = max(1, profile.new_fleets_count)
        neutral_ratio = profile.neutral_target_count / total
        own_ratio = profile.own_target_count / total
        center_ratio = profile.center_target_count / total
        high_prod_ratio = profile.high_prod_target_count / total
        comet_ratio = profile.comet_target_count / total
        big_ratio = profile.large_fleet_count / total
        overcommit_ratio = profile.overcommit_count / total
        self_ratio = profile.self_target_count / total
        weak_enemy_ratio = profile.weak_enemy_target_count / total
        conflict_ratio = profile.conflict_target_count / total
        send_pressure = clamp(profile.total_ships_sent / max(1.0, 20.0 * max(1, profile.observed_turns)))
        low_send = 1.0 - clamp(profile.new_fleets_count / max(1.0, profile.observed_turns / 5.0))

        early_attack = 0.0
        if profile.first_attack_turn is not None and profile.first_attack_turn <= 80:
            early_attack = 1.0 - profile.first_attack_turn / 80.0

        profile.scores = {
            "neutral_rusher": clamp(0.55 * neutral_ratio + 0.25 * send_pressure + 0.20 * profile.max_commit_ratio - 0.20 * own_ratio),
            "enemy_rusher": clamp(0.60 * early_attack + 0.30 * own_ratio + 0.10 * profile.max_commit_ratio),
            "turtle": clamp(0.70 * low_send + 0.30 * (1.0 - send_pressure)),
            "center_greedy": clamp(0.75 * center_ratio + 0.25 * neutral_ratio),
            "production_greedy": clamp(0.80 * high_prod_ratio + 0.20 * neutral_ratio),
            "big_stack": clamp(0.75 * big_ratio + 0.25 * profile.max_commit_ratio),
            "comet_greedy": clamp(comet_ratio),
            "overcommitter": clamp(0.65 * overcommit_ratio + 0.35 * profile.max_commit_ratio),
            "reinforce_heavy": clamp(0.80 * self_ratio + 0.20 * low_send),
            "crash_exploiter": clamp(conflict_ratio),
            "weakest_targeter": clamp(weak_enemy_ratio),
            "weak_bot": 0.0,
            "confidence": profile.confidence,
        }

    def _weakest_enemy_owner(self, state: GameState) -> int | None:
        totals: Dict[int, int] = {}
        for planet in state.enemy_planets:
            totals[planet.owner] = totals.get(planet.owner, 0) + int(planet.ships) + int(planet.production) * 12
        for fleet in state.fleets:
            if fleet.owner not in (-1, state.player):
                totals[fleet.owner] = totals.get(fleet.owner, 0) + int(fleet.ships)
        if not totals:
            return None
        return min(totals, key=totals.get)

    def _targets_existing_conflict(self, state: GameState, fleet: FleetState, target: PlanetState) -> bool:
        for other in state.fleets:
            if other.id == fleet.id or other.owner in (-1, fleet.owner):
                continue
            other_target = likely_fleet_target(other, state)
            if other_target is not None and other_target.id == target.id:
                return True
        return False
