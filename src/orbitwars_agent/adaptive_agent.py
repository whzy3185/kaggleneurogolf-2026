from __future__ import annotations

import importlib.util
import math
import time
from pathlib import Path
from types import ModuleType
from typing import Any, List

from .counter_policy import StrategyModifiers, build_strategy_modifiers, effective
from .opponent_profiler import OpponentProfile, OpponentProfiler
from .physics import angle_to_planet, distance, eta
from .types import GameState, PlanetState
from .world_model import build_game_state, detect_threatened_own_planets, incoming_fleets_by_planet

_PROFILER = OpponentProfiler()
_STEP = 0
_BASE_MODULE: ModuleType | None = None
_ROOT = Path(__file__).resolve().parents[2]
_BASE_AGENT_PATH = _ROOT / "agents" / "base_agent.py"
_DEFAULT_ENABLED_POLICIES = (
    "enemy_rusher",
    "neutral_rusher",
    "turtle",
    "big_stack",
    "overcommitter",
    "comet_greedy",
    "reinforce_heavy",
    "crash_exploiter",
    "weakest_targeter",
)
_SETTING_KEYS = {
    "use_profiler",
    "use_counter_policy",
    "use_supplemental_moves",
    "enabled_policies",
}


def _load_base_module() -> ModuleType:
    global _BASE_MODULE
    if _BASE_MODULE is not None:
        return _BASE_MODULE
    spec = importlib.util.spec_from_file_location("orbitwars_selected_base_agent", _BASE_AGENT_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load base agent from {_BASE_AGENT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _BASE_MODULE = module
    return module


def _call_base_agent(obs: Any, config: Any = None) -> list:
    module = _load_base_module()
    if config is None:
        result = module.agent(obs)
    else:
        result = module.agent(obs, config=config)
    return result if isinstance(result, list) else []


def reset_state() -> None:
    global _PROFILER, _STEP
    _PROFILER = OpponentProfiler()
    _STEP = 0


def _resolve_settings(config: Any) -> tuple[dict[str, Any], Any]:
    settings: dict[str, Any] = {
        "use_profiler": True,
        "use_counter_policy": True,
        "use_supplemental_moves": True,
        "enabled_policies": _DEFAULT_ENABLED_POLICIES,
    }
    if isinstance(config, dict) and _SETTING_KEYS.intersection(config):
        settings.update({key: config[key] for key in _SETTING_KEYS if key in config})
        if settings.get("enabled_policies") is not None:
            settings["enabled_policies"] = tuple(settings["enabled_policies"])
        return settings, None
    return settings, config


def agent(obs, config=None):
    global _STEP
    start = time.perf_counter()
    try:
        settings, base_config = _resolve_settings(config)
        state = build_game_state(obs, inferred_step=_STEP)
        _STEP = state.step + 1
        base_actions = _validate_actions(state, _call_base_agent(obs, config=base_config))
        profiles = _PROFILER.update(state) if settings["use_profiler"] else {}
        if settings["use_counter_policy"]:
            modifiers = build_strategy_modifiers(
                profiles,
                enabled_policies=settings["enabled_policies"],
            )
        else:
            modifiers = StrategyModifiers()
        if time.perf_counter() - start > 0.75:
            return base_actions
        if not settings["use_supplemental_moves"]:
            return base_actions
        if not _should_add_supplement(state, profiles, settings["enabled_policies"]):
            return base_actions
        supplemental = choose_actions(state, modifiers)
        return _merge_actions(state, base_actions, supplemental)
    except Exception:
        try:
            return _call_base_agent(obs, config=config)
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


def _validate_actions(state: GameState, actions: list) -> list[list[float]]:
    own = {planet.id: planet for planet in state.my_planets}
    committed: dict[int, int] = {}
    valid: list[list[float]] = []
    if not isinstance(actions, list):
        return valid
    for action in actions:
        if not isinstance(action, (list, tuple)) or len(action) != 3:
            continue
        from_id, angle, ships = action
        try:
            from_id = int(from_id)
            angle = float(angle)
            ships = int(ships)
        except (TypeError, ValueError):
            continue
        source = own.get(from_id)
        if source is None or ships <= 0 or not math.isfinite(angle):
            continue
        already = committed.get(from_id, 0)
        allowed = max(0, source.ships - already)
        if allowed <= 0:
            continue
        send = min(ships, allowed)
        if send > 0:
            valid.append([from_id, angle, send])
            committed[from_id] = already + send
    return valid


def _merge_actions(state: GameState, base_actions: list, supplemental: list) -> list[list[float]]:
    own = {planet.id: planet for planet in state.my_planets}
    merged: list[list[float]] = []
    committed: dict[int, int] = {}
    for action in base_actions + supplemental:
        if not isinstance(action, (list, tuple)) or len(action) != 3:
            continue
        from_id, angle, ships = int(action[0]), float(action[1]), int(action[2])
        source = own.get(from_id)
        if source is None or ships <= 0 or not math.isfinite(angle):
            continue
        already = committed.get(from_id, 0)
        remaining = max(0, source.ships - already)
        if remaining <= 0:
            continue
        send = min(ships, remaining)
        merged.append([from_id, angle, send])
        committed[from_id] = already + send
    return merged[:16]


def _should_add_supplement(
    state: GameState,
    profiles: dict[int, OpponentProfile],
    enabled_policies: tuple[str, ...] | None = _DEFAULT_ENABLED_POLICIES,
) -> bool:
    if detect_threatened_own_planets(state, horizon_turns=45):
        return True
    for profile in profiles.values():
        if profile.confidence < 0.55:
            continue
        for key in enabled_policies or ():
            if effective(profile, key) >= 0.55:
                return True
    return False


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
