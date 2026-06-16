from __future__ import annotations

from typing import List

from .counter_policy import StrategyModifiers, build_strategy_modifiers
from .opponent_profiler import OpponentProfiler
from .physics import angle_to_planet, distance, eta
from .types import GameState, PlanetState
from .world_model import build_game_state, incoming_fleets_by_planet

_PROFILER = OpponentProfiler()
_STEP = 0


def agent(obs):
    global _STEP
    try:
        state = build_game_state(obs, inferred_step=_STEP)
        _STEP = state.step + 1
        profiles = _PROFILER.update(state)
        modifiers = build_strategy_modifiers(profiles)
        return choose_actions(state, modifiers)
    except Exception:
        return []


def choose_actions(state: GameState, modifiers: StrategyModifiers) -> List[List[float]]:
    moves: List[List[float]] = []
    if not state.my_planets:
        return moves

    committed_by_source = {planet.id: 0 for planet in state.my_planets}
    reserve_floor = max(2, 4 + modifiers.reserve_floor_delta)
    max_commit_ratio = min(0.85, max(0.25, 0.62 + modifiers.max_commit_ratio_delta))

    moves.extend(_reinforce_threatened_planets(state, modifiers, committed_by_source, reserve_floor))

    targets = [planet for planet in state.planets if planet.owner != state.player]
    scored_targets = sorted(
        targets,
        key=lambda target: _target_score(state, target, modifiers),
        reverse=True,
    )

    for source in sorted(state.my_planets, key=lambda planet: planet.ships, reverse=True):
        already = committed_by_source.get(source.id, 0)
        max_send = int(source.ships * max_commit_ratio) - already
        available = max(0, min(source.ships - reserve_floor - already, max_send))
        if available <= 0:
            continue

        best = _best_target_for_source(state, source, scored_targets, modifiers)
        if best is None:
            continue

        needed = max(1, best.ships + (1 if best.owner == -1 else 3))
        send = min(available, needed)
        if send <= 0 or send < needed:
            continue
        moves.append([source.id, angle_to_planet(source, best), int(send)])
        committed_by_source[source.id] = already + int(send)

    return moves[:12]


def _reinforce_threatened_planets(
    state: GameState,
    modifiers: StrategyModifiers,
    committed_by_source: dict[int, int],
    reserve_floor: int,
) -> List[List[float]]:
    moves: List[List[float]] = []
    incoming = incoming_fleets_by_planet(state)
    my_by_id = {planet.id: planet for planet in state.my_planets}
    for target_id, fleets in incoming.items():
        target = my_by_id.get(target_id)
        if target is None:
            continue
        enemy_ships = sum(fleet.ships for fleet in fleets if fleet.owner != state.player)
        if enemy_ships <= target.ships + 2:
            continue
        need = int((enemy_ships - target.ships + 3) * modifiers.defense_weight_mult)
        helper = _nearest_helper(state, target, committed_by_source, reserve_floor)
        if helper is None:
            continue
        available = max(0, helper.ships - reserve_floor - committed_by_source.get(helper.id, 0))
        send = min(available, need)
        if send > 0:
            moves.append([helper.id, angle_to_planet(helper, target), int(send)])
            committed_by_source[helper.id] = committed_by_source.get(helper.id, 0) + int(send)
    return moves


def _nearest_helper(
    state: GameState,
    target: PlanetState,
    committed_by_source: dict[int, int],
    reserve_floor: int,
) -> PlanetState | None:
    candidates = []
    for planet in state.my_planets:
        if planet.id == target.id:
            continue
        available = planet.ships - reserve_floor - committed_by_source.get(planet.id, 0)
        if available > 0:
            candidates.append((distance(planet, target), planet))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    return candidates[0][1]


def _target_score(state: GameState, target: PlanetState, modifiers: StrategyModifiers) -> float:
    base = 5.0 * target.production - 0.35 * target.ships
    if target.owner == -1:
        base *= modifiers.expansion_weight_mult
    else:
        enemy_bias = modifiers.target_enemy_bias.get(target.owner, 1.0)
        base *= modifiers.attack_weight_mult * enemy_bias
    if target.id in state.comet_planet_ids:
        base *= modifiers.comet_weight_mult
    center_distance = ((target.x - 50.0) ** 2 + (target.y - 50.0) ** 2) ** 0.5
    if center_distance < 25.0:
        base *= modifiers.center_weight_mult
    return base


def _best_target_for_source(
    state: GameState,
    source: PlanetState,
    scored_targets: List[PlanetState],
    modifiers: StrategyModifiers,
) -> PlanetState | None:
    best_score = None
    best_target = None
    for target in scored_targets[:14]:
        travel = distance(source, target)
        turns = eta(travel, max(1, min(source.ships, target.ships + 3)))
        score = _target_score(state, target, modifiers) / (1.0 + 0.12 * turns)
        if target.owner != -1:
            score += modifiers.counterattack_bonus
        if best_score is None or score > best_score:
            best_score = score
            best_target = target
    return best_target
