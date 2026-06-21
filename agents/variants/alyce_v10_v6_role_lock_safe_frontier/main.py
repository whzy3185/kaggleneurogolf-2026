from __future__ import annotations

import dataclasses
import json
import os
import sys
from dataclasses import dataclass, replace

# Make the sibling ``orbit_lite`` package importable wherever this file runs.
try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _HERE = os.getcwd()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import torch
from torch import Tensor

from orbit_lite.geometry import fleet_speed
from orbit_lite.intercept_aim import intercept_angle
from orbit_lite.movement import MovementConfig, PlanetMovement
from orbit_lite.movement_step import (
    apply_private_planned_launches,
    concat_launch_entries,
    disambiguate_duplicate_launches,
    ensure_planet_movement,
    infer_planned_launches_from_entries,
)
from orbit_lite.obs import parse_obs
from orbit_lite.distance_cache import build_distance_cache
from orbit_lite.planner_core import (
    _candidate_indices,
    _empty_entries,
    _greedy_select,
    _plan_regroup,
    build_target_shortlist,
    capture_floor,
    empty_action_row,
    entries_to_sparse_payload,
    largest_initial_player_count,
    make_launch_set,
    reachable_mask,
    reinforcement_timing_factor,
    safe_drain,
    score_candidates,
)
from orbit_lite.adapter import single_obs_to_tensor, sparse_action_row_to_moves


TOTAL_STEPS = 500


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProducerLiteConfig:
    """Minimal config with dynamic-adjustment hooks."""
    # Planning
    horizon: int = 18
    max_sources_per_lane: int = 12
    max_offensive_targets: int = 12
    max_defensive_targets: int = 4
    max_waves_per_turn: int = 6
    roi_threshold: float = 1.40
    min_ships_to_launch: float = 4.0
    # Reinforcement risk (β)
    reinforce_size_beta: float = 2.2
    reinforce_eta_free: float = 3.0
    reinforce_eta_scale: float = 12.0
    # Regroup
    enable_regroup: bool = True
    max_regroup_time: float = 7.0
    regroup_pressure_delta_min: float = 0.25
    max_regroup_sources_per_lane: int = 6
    max_regroup_targets_per_source: int = 7
    regroup_pressure_norm: str = "none"
    regroup_time_penalty_weight: float = 1e-3
    # 4P FFA safety layer. Disabled for 2P/3P presets.
    enable_ffa_mission_filter: bool = False
    ffa_safe_neutral_gap: float = 4.0
    ffa_contested_neutral_gap: float = 1.0
    ffa_trap_neutral_gap: float = -2.0
    ffa_contested_min_surplus: float = 1.0
    ffa_contested_pressure_mult: float = 0.01
    ffa_contested_penalty_mult: float = 0.65
    ffa_contested_pressure_penalty_mult: float = 0.015
    ffa_hard_veto_prod_max: float = 2.0
    ffa_hard_veto_surplus_margin: float = -2.0
    ffa_source_reserve_frac: float = 0.05
    ffa_source_reserve_prod_mult: float = 0.5
    ffa_source_reserve_pressure_mult: float = 0.02
    ffa_source_pressure_gate: float = 0.75
    ffa_enemy_rear_eta: float = 9.0
    ffa_enemy_rear_prod_max: float = 2.0
    ffa_leader_bonus_weight: float = 0.08
    ffa_threat_neighbor_dist: float = 45.0
    ffa_threat_neighbor_bonus: float = 3.0
    # V6 selected-action safety filter. Unlike the rejected V4 branch, this
    # starts from V2 and only changes the current top candidate when a clearly
    # safer close-score alternative exists. The extra V6 mode only activates
    # in 4P early/mid games after production rank or gap has already degraded.
    enable_v5_selected_filter: bool = False
    enable_v5_trace: bool = False
    v5_low_neutral_prod_max: float = 1.0
    v5_low_enemy_prod_max: float = 2.0
    v5_far_dist: float = 55.0
    v5_source_depletion_ratio: float = 0.88
    v5_alt_score_gap: float = 4.0
    v5_alt_min_prod_gain: float = 2.0
    v5_alt_safe_reaction_gap: float = 2.0
    v5_force_bonus: float = 0.05
    enable_v6_prod_gap_mode: bool = False
    v6_gap_step_start: int = 45
    v6_gap_step_end: int = 170
    v6_prod_gap_trigger: float = -6.0
    v6_prod_rank_trigger: int = 3
    v6_gap_alt_score_gap: float = 5.5
    v6_gap_low_target_prod_max: float = 3.0
    v6_gap_high_source_prod_min: float = 3.0
    v6_gap_depletion_ratio: float = 0.78
    v6_gap_bad_reaction_gap: float = 1.0
    v6_gap_safe_reaction_gap: float = 1.5
    v6_gap_near_dist: float = 50.0
    v6_gap_force_bonus: float = 0.08
    # V10: conservative 4P source/mission lock. This starts from V6, not V9.
    # The goal is to reduce third-party cleanup / public-good launches while
    # preserving V6 tempo. It is active only in the 4P preset.
    enable_v10_role_lock: bool = False
    enable_v10_trace: bool = False
    v10_activation_step_start: int = 0
    v10_early_step_end: int = 80
    v10_mid_step_end: int = 190
    v10_safe_reaction_gap: float = 5.0
    v10_hard_reaction_gap: float = 0.0
    v10_multi_enemy_eta_margin: float = 8.0
    v10_public_depletion_ratio: float = 0.72
    v10_high_source_prod_min: float = 3.0
    v10_low_target_prod_max: float = 2.0
    v10_source_reserve_frac: float = 0.14
    v10_source_reserve_prod_mult: float = 0.85
    v10_source_reserve_pressure_mult: float = 0.035
    v10_blackout_depletion_ratio: float = 0.82
    v10_center_dist: float = 32.0
    v10_far_dist: float = 58.0
    v10_public_good_penalty: float = 18.0
    v10_center_sacrifice_penalty: float = 11.0
    v10_trailing_low_enemy_penalty: float = 12.0
    v10_safe_frontier_bonus: float = 3.5


# ---------------------------------------------------------------------------
# Dynamic adjustment — single lightweight function
# ---------------------------------------------------------------------------

def _owner_strength(obs, prod: Tensor, player_count: int) -> Tensor:
    """Per-owner production + 2.5% ships as strength proxy. [player_count]"""
    dtype = prod.dtype
    device = prod.device
    strength = torch.zeros(int(player_count), dtype=dtype, device=device)
    owner = obs.owner_abs.to(device=device)
    alive = obs.alive.to(device=device)
    ships = obs.ships.to(device=device, dtype=dtype)
    prod_v = prod.to(device=device, dtype=dtype)
    for oid in range(int(player_count)):
        mask = alive & (owner == oid)
        if bool(mask.any()):
            strength[oid] = prod_v[mask].sum() + 0.025 * ships[mask].sum()
    return strength


def _adjust_config(
    config: ProducerLiteConfig,
    *,
    obs,
    prod: Tensor,
    step: int,
    player_count: int,
) -> ProducerLiteConfig:
    """Continuous dynamic adjustment based on game state.

    Two knobs:
      1. Strength-ratio → ROI / waves (continuous, not tiered)
      2. Time remaining  → suppress late arrivals + devalue late neutrals
         (applied later in candidate scoring)
    No hard thresholds, no phase switches — smooth interpolation.
    """
    pid = int(obs.player_id)
    strength = _owner_strength(obs, prod, int(player_count))
    if pid < 0 or pid >= int(player_count) or strength.numel() == 0:
        return config

    my = float(strength[pid].item())
    leader = float(strength.max().item())
    ratio = my / max(leader, 1e-6)  # my_strength / leader_strength

    # --- ROI: continuous ramp ---
    #   ratio >= 1.0  → no change (we are leading)
    #   ratio = 0.80  → ROI - 0.05
    #   ratio = 0.50  → ROI - 0.15
    #   ratio = 0.30  → ROI - 0.25
    if ratio < 1.0:
        # deficit in [0, 1]: 0 = even, 1 = we have nothing
        deficit = 1.0 - ratio
        roi_drop = 0.25 * deficit * deficit  # quadratic: small deficit → small drop
        new_roi = max(1.10, float(config.roi_threshold) - roi_drop)
        # Late-game extra push: after step 350, if still behind, drop more
        remaining = TOTAL_STEPS - int(step)
        if remaining < 150 and ratio < 0.90:
            time_urgency = (150 - remaining) / 150.0  # 0→1 as game ends
            new_roi = max(1.10, new_roi - 0.10 * time_urgency * deficit)
        config = replace(config, roi_threshold=new_roi)

    # --- Waves: one extra wave when behind or in late game ---
    base_waves = int(config.max_waves_per_turn)
    if ratio < 0.70:
        base_waves = min(7, base_waves + 1)
    remaining = TOTAL_STEPS - int(step)
    if remaining < 100 and ratio < 0.95:
        base_waves = min(7, base_waves + 1)
    config = replace(config, max_waves_per_turn=base_waves)

    return config


# ---------------------------------------------------------------------------
# Movement + pressure helpers
# ---------------------------------------------------------------------------

def _movement_config(config: ProducerLiteConfig, *, player_count: int) -> MovementConfig:
    return MovementConfig(
        movement_horizon=int(config.horizon),
        drift_epsilon=1e-3,
        track_fleets=True,
        player_count=int(player_count),
        max_tracked_fleets=128,
    )


def cheap_enemy_pressure(obs, cache, *, horizon: float, player_id: int) -> Tensor:
    """Distance-decayed reachable enemy mass per planet — [P]."""
    P = int(obs.P)
    device = obs.device
    dtype = obs.ships.dtype
    if P == 0:
        return torch.zeros(P, dtype=dtype, device=device)
    d0 = cache.cross_dist[0].to(dtype)
    ships = obs.ships.to(dtype)
    speeds = fleet_speed(ships.clamp(min=1e-6))
    reach_dist = (speeds.view(P, 1) * float(horizon)).clamp(min=1e-6)
    enemy = obs.alive & (obs.owner_abs >= 0) & (obs.owner_abs != int(player_id))
    eye = torch.eye(P, device=device, dtype=torch.bool)
    valid = enemy.view(P, 1) & obs.alive.view(1, P) & ~eye
    decay = (1.0 - d0 / reach_dist).clamp(min=0.0)
    contrib = torch.where(valid, ships.view(P, 1) * decay, torch.zeros_like(decay))
    return contrib.sum(dim=0)


def _ffa_strength(obs, prod: Tensor, player_count: int) -> Tensor:
    """Live 4P strength proxy: production plus planet and fleet mass."""
    strength = _owner_strength(obs, prod, int(player_count)).clone()
    ships = obs.ships.to(dtype=strength.dtype, device=strength.device)
    prod_v = prod.to(dtype=strength.dtype, device=strength.device)
    owner = obs.owner_abs.to(device=strength.device)
    alive = obs.alive.to(device=strength.device)
    for oid in range(int(player_count)):
        planet_mask = alive & (owner == oid)
        if bool(planet_mask.any()):
            strength[oid] += 0.02 * ships[planet_mask].sum() + 0.5 * prod_v[planet_mask].sum()
        fleet_mask = obs.f_alive.to(device=strength.device) & (
            obs.f_owner.to(device=strength.device) == float(oid)
        )
        if bool(fleet_mask.any()):
            strength[oid] += 0.35 * obs.f_ships.to(dtype=strength.dtype, device=strength.device)[fleet_mask].sum()
    return strength


def _best_eta_to_targets(
    obs,
    cache,
    *,
    source_mask: Tensor,
    target_idx: Tensor,
    max_k: int,
) -> Tensor:
    """Approximate best integer ETA from any source in source_mask to targets."""
    T = int(target_idx.shape[0])
    dtype = cache.dtype
    device = cache.device
    inf = torch.full((T,), float("inf"), dtype=dtype, device=device)
    K = max(0, min(int(max_k), int(cache.K)))
    P = int(obs.P)
    if K <= 0 or T == 0 or P == 0:
        return inf
    src_mask = source_mask.to(device=device, dtype=torch.bool) & obs.alive.to(device=device)
    if not bool(src_mask.any()):
        return inf
    turns = torch.arange(1, K + 1, dtype=dtype, device=device)
    speed = fleet_speed(obs.ships.to(dtype=dtype, device=device).clamp(min=1.0))
    cross = cache.cross_dist[1 : K + 1].to(dtype=dtype, device=device)
    reachable = cross <= speed.view(1, P, 1) * turns.view(K, 1, 1)
    eye = torch.eye(P, dtype=torch.bool, device=device).view(1, P, P)
    reachable = reachable & src_mask.view(1, P, 1) & obs.alive.to(device=device).view(1, 1, P) & ~eye
    reachable_by_turn = reachable.any(dim=1)  # [K, P]
    eta_grid = torch.where(
        reachable_by_turn,
        turns.view(K, 1).expand(K, P),
        torch.full((K, P), float("inf"), dtype=dtype, device=device),
    )
    best_all = eta_grid.min(dim=0).values
    return best_all[target_idx.clamp(0, max(P - 1, 0))]


def _apply_4p_source_reserve(
    drain: Tensor,
    *,
    obs,
    prod: Tensor,
    source_idx: Tensor,
    enemy_mass: Tensor | None,
    config: ProducerLiteConfig,
    step: int,
) -> Tensor:
    """Keep some ships on valuable or pressured 4P sources before candidate sizing."""
    if drain.numel() == 0:
        return drain
    P = int(obs.P)
    src = source_idx.clamp(0, max(P - 1, 0))
    dtype = drain.dtype
    ships = obs.ships[src].to(dtype=dtype, device=drain.device)
    prod_s = prod[src].to(dtype=dtype, device=drain.device)
    if enemy_mass is None:
        pressure = torch.zeros_like(ships)
    else:
        pressure = enemy_mass[src].to(dtype=dtype, device=drain.device)
    reserve = torch.maximum(
        ships * float(config.ffa_source_reserve_frac),
        prod_s * float(config.ffa_source_reserve_prod_mult),
    )
    reserve = torch.maximum(reserve, pressure * float(config.ffa_source_reserve_pressure_mult))
    needs_reserve = (prod_s >= 3.0) | (pressure >= ships * float(config.ffa_source_pressure_gate))
    reserve = torch.where(needs_reserve, reserve, torch.zeros_like(reserve))
    if (
        bool(config.enable_v10_role_lock)
        and int(config.v10_activation_step_start) <= int(step) <= int(config.v10_mid_step_end)
    ):
        # V10 locks important early/mid sources before candidate scoring. V9
        # proved that late penalties can still route the same source into a
        # different public-good launch. This is intentionally source-centric.
        source_locked = (prod_s >= float(config.v10_high_source_prod_min)) | (
            pressure >= ships * 0.50
        )
        source_floor = torch.maximum(
            ships * float(config.v10_source_reserve_frac),
            prod_s * float(config.v10_source_reserve_prod_mult),
        )
        source_floor = torch.maximum(
            source_floor,
            pressure * float(config.v10_source_reserve_pressure_mult),
        )
        if int(step) <= int(config.v10_early_step_end):
            source_floor = torch.where(
                prod_s >= float(config.v10_high_source_prod_min),
                torch.maximum(source_floor, ships * 0.20),
                source_floor,
            )
        reserve = torch.where(source_locked, torch.maximum(reserve, source_floor), reserve)
    cap = (ships - reserve).clamp(min=0.0)
    return torch.minimum(drain, cap)


def _apply_4p_candidate_adjustments(
    *,
    score: Tensor,
    obs,
    cache,
    prod: Tensor,
    target_idx: Tensor,
    cand_src: Tensor,
    cand_send: Tensor,
    cand_eta: Tensor,
    cand_tgt_short: Tensor,
    cand_is_def: Tensor,
    cand_valid: Tensor,
    floor_at_arr: Tensor,
    enemy_mass: Tensor | None,
    config: ProducerLiteConfig,
    player_count: int,
) -> Tensor:
    """4P FFA target-quality filter before greedy launch selection."""
    if score.numel() == 0 or not bool(cand_valid.any()):
        return score

    P = int(obs.P)
    device = score.device
    dtype = score.dtype
    pid = int(obs.player_id)
    tgt = target_idx[cand_tgt_short].clamp(0, max(P - 1, 0))
    src = cand_src.reshape(-1).clamp(0, max(P - 1, 0))
    send = cand_send.reshape(-1).to(dtype=dtype, device=device)
    eta = cand_eta.reshape(-1).to(dtype=dtype, device=device)
    floor_flat = floor_at_arr.reshape(-1).to(dtype=dtype, device=device)
    owner = obs.owner_abs.to(device=device)[tgt].long()
    prod_t = prod.to(dtype=dtype, device=device)[tgt]
    prod_s = prod.to(dtype=dtype, device=device)[src]
    ships_s = obs.ships.to(dtype=dtype, device=device)[src].clamp(min=1.0)

    enemy_source_mask = (
        obs.alive
        & obs.is_enemy
        & (obs.ships >= float(config.min_ships_to_launch))
    )
    enemy_eta_targets = _best_eta_to_targets(
        obs, cache, source_mask=enemy_source_mask, target_idx=target_idx,
        max_k=int(config.horizon),
    )
    enemy_eta = enemy_eta_targets[cand_tgt_short].to(dtype=dtype, device=device)
    reaction_gap = enemy_eta - eta
    if enemy_mass is None:
        pressure_t = torch.zeros_like(score)
        pressure_s = torch.zeros_like(score)
    else:
        pressure_vec = enemy_mass.to(dtype=dtype, device=device)
        pressure_t = pressure_vec[tgt]
        pressure_s = pressure_vec[src]

    is_neutral = (owner < 0) & (~cand_is_def)
    is_enemy_target = (owner >= 0) & (owner != pid) & (~cand_is_def)
    surplus = send - floor_flat
    surplus_need = torch.maximum(
        torch.full_like(score, float(config.ffa_contested_min_surplus)),
        prod_t * 1.5 + pressure_t * float(config.ffa_contested_pressure_mult),
    )

    trap_neutral = is_neutral & (reaction_gap < float(config.ffa_trap_neutral_gap))
    bad_contested = (
        is_neutral
        & (reaction_gap <= float(config.ffa_contested_neutral_gap))
        & (surplus < surplus_need)
    )
    severe_trap = (
        trap_neutral
        & (prod_t <= float(config.ffa_hard_veto_prod_max))
        & (surplus < float(config.ffa_hard_veto_surplus_margin))
    )
    score = torch.where(cand_valid & severe_trap, torch.full_like(score, float("-inf")), score)

    contested_shortfall = (surplus_need - surplus).clamp(min=0.0)
    contested_penalty = (
        contested_shortfall * float(config.ffa_contested_penalty_mult)
        + pressure_t * float(config.ffa_contested_pressure_penalty_mult)
    )
    soft_contested = bad_contested & ~severe_trap
    score = score - torch.where(soft_contested & cand_valid, contested_penalty, torch.zeros_like(score))

    safe_neutral = is_neutral & (reaction_gap >= float(config.ffa_safe_neutral_gap))
    safe_bonus = prod_t * 0.75 + reaction_gap.clamp(min=0.0, max=8.0) * 0.35
    score = score + torch.where(safe_neutral & cand_valid, safe_bonus, torch.zeros_like(score))

    depletion_ratio = send / ships_s
    source_at_risk = (prod_s >= 3.0) | (pressure_s >= ships_s * float(config.ffa_source_pressure_gate))
    depletion_penalty = (
        (depletion_ratio - 0.80).clamp(min=0.0) * send * 0.45
        + prod_s * 0.8
        + pressure_s * 0.03
    )
    score = score - torch.where(
        source_at_risk & (depletion_ratio > 0.80) & cand_valid,
        depletion_penalty,
        torch.zeros_like(score),
    )

    strength = _ffa_strength(obs, prod, int(player_count))
    leader = int(strength.argmax().item()) if strength.numel() > 0 else pid
    leader_gap = torch.zeros((), dtype=dtype, device=device)
    if 0 <= leader < int(player_count) and 0 <= pid < int(player_count):
        leader_gap = (strength[leader] - strength[pid]).to(dtype=dtype, device=device).clamp(min=0.0)
    leader_asset = is_enemy_target & (owner == leader) & (leader != pid)
    holdable = (reaction_gap >= -0.5) | (surplus > pressure_t * 0.08)
    leader_bonus = leader_gap * float(config.ffa_leader_bonus_weight) + prod_t * 1.25
    score = score + torch.where(
        leader_asset & holdable & cand_valid,
        leader_bonus,
        torch.zeros_like(score),
    )

    low_value_rear = (
        is_enemy_target
        & (owner != leader)
        & (prod_t <= float(config.ffa_enemy_rear_prod_max))
        & (eta > float(config.ffa_enemy_rear_eta))
    )
    rear_penalty = 5.0 + eta * 0.5
    score = score - torch.where(low_value_rear & cand_valid, rear_penalty, torch.zeros_like(score))

    high_value_owned = obs.owned & (prod >= 3.0)
    if bool(high_value_owned.any()):
        dist_to_owned = cache.cross_dist[0][tgt][:, high_value_owned].amin(dim=-1).to(dtype=dtype)
        threat_neighbor = is_enemy_target & (dist_to_owned <= float(config.ffa_threat_neighbor_dist))
        threat_bonus = float(config.ffa_threat_neighbor_bonus) + prod_t
        score = score + torch.where(
            threat_neighbor & cand_valid,
            threat_bonus,
            torch.zeros_like(score),
        )
    return score


_V10_TRACE_LAST: dict = {}


def _apply_v10_role_lock_filter(
    *,
    score: Tensor,
    obs,
    cache,
    prod: Tensor,
    target_idx: Tensor,
    cand_src: Tensor,
    cand_send: Tensor,
    cand_eta: Tensor,
    cand_tgt_short: Tensor,
    cand_is_def: Tensor,
    cand_valid: Tensor,
    enemy_mass: Tensor | None,
    config: ProducerLiteConfig,
    player_count: int,
    step: int,
) -> Tensor:
    """V10 4P role/source lock.

    This is deliberately conservative: it never adds standalone attacks. It
    only hard-vetoes or penalizes actions that look like public goods for a
    third player, then gives a small bonus to already valid safe-frontier
    candidates so the planner still has a replacement path.
    """
    global _V10_TRACE_LAST
    if not bool(config.enable_v10_role_lock) or int(player_count) < 4 or score.numel() == 0:
        return score

    P = int(obs.P)
    if P <= 0:
        return score

    device = score.device
    dtype = score.dtype
    pid = int(obs.player_id)
    valid = cand_valid.reshape(-1).to(device=device, dtype=torch.bool) & torch.isfinite(score)
    if not bool(valid.any()):
        if bool(config.enable_v10_trace):
            _V10_TRACE_LAST = {
                "step": int(step),
                "player": pid,
                "player_count": int(player_count),
                "changed_top": False,
                "reason": "no_valid_candidate",
            }
        return score

    flat_src = cand_src.reshape(-1).clamp(0, max(P - 1, 0)).long()
    flat_send = cand_send.reshape(-1).to(dtype=dtype, device=device)
    flat_eta = cand_eta.reshape(-1).to(dtype=dtype, device=device)
    flat_tgt_short = cand_tgt_short.reshape(-1)
    flat_tgt = target_idx[flat_tgt_short].clamp(0, max(P - 1, 0)).long()

    owner = obs.owner_abs.to(device=device)[flat_tgt].long()
    target_prod = prod.to(device=device, dtype=dtype)[flat_tgt]
    source_prod = prod.to(device=device, dtype=dtype)[flat_src]
    source_ships = obs.ships.to(device=device, dtype=dtype)[flat_src].clamp(min=1.0)
    source_after = (source_ships - flat_send).clamp(min=0.0)
    target_distance = cache.cross_dist[0].to(dtype=dtype, device=device)[flat_src, flat_tgt]
    target_center_dist = torch.sqrt(
        (obs.x.to(dtype=dtype, device=device)[flat_tgt] - 50.0) ** 2
        + (obs.y.to(dtype=dtype, device=device)[flat_tgt] - 50.0) ** 2
    )

    enemy_source_mask = (
        obs.alive
        & obs.is_enemy
        & (obs.ships >= float(config.min_ships_to_launch))
    )
    enemy_eta_targets = _best_eta_to_targets(
        obs, cache, source_mask=enemy_source_mask, target_idx=target_idx,
        max_k=int(config.horizon),
    )
    reaction_gap = enemy_eta_targets[flat_tgt_short].to(dtype=dtype, device=device) - flat_eta

    close_enemy_count = torch.zeros_like(score)
    per_enemy_eta: list[Tensor] = []
    for oid in range(int(player_count)):
        if oid == pid:
            continue
        owner_source_mask = (
            obs.alive
            & (obs.owner_abs == float(oid))
            & (obs.ships >= float(config.min_ships_to_launch))
        )
        owner_eta = _best_eta_to_targets(
            obs, cache, source_mask=owner_source_mask, target_idx=target_idx,
            max_k=int(config.horizon),
        )
        per_enemy_eta.append(owner_eta.to(dtype=dtype, device=device))
    if per_enemy_eta:
        enemy_eta_by_owner = torch.stack(per_enemy_eta, dim=0)
        cand_enemy_eta = enemy_eta_by_owner[:, flat_tgt_short]
        close_enemy_count = (
            cand_enemy_eta <= (flat_eta.unsqueeze(0) + float(config.v10_multi_enemy_eta_margin))
        ).to(dtype=dtype).sum(dim=0)

    pressure_s = (
        enemy_mass[flat_src].to(dtype=dtype, device=device)
        if enemy_mass is not None
        else torch.zeros_like(source_ships)
    )
    pressure_t = (
        enemy_mass[flat_tgt].to(dtype=dtype, device=device)
        if enemy_mass is not None
        else torch.zeros_like(target_prod)
    )

    owner_is_mine = (owner == pid) | cand_is_def.reshape(-1)
    owner_is_neutral = (owner < 0) & ~cand_is_def.reshape(-1)
    owner_is_enemy = (owner >= 0) & (owner != pid) & (owner < int(player_count)) & ~cand_is_def.reshape(-1)
    public_target = owner_is_neutral | owner_is_enemy
    depletion_ratio = flat_send / source_ships

    source_locked = (source_prod >= float(config.v10_high_source_prod_min)) | (
        pressure_s >= source_ships * 0.50
    )
    reserve_floor = torch.maximum(
        source_ships * float(config.v10_source_reserve_frac),
        source_prod * float(config.v10_source_reserve_prod_mult),
    )
    reserve_floor = torch.maximum(
        reserve_floor,
        pressure_s * float(config.v10_source_reserve_pressure_mult),
    )
    source_reserve_violation = source_locked & public_target & (source_after < reserve_floor)

    strength = _ffa_strength(obs, prod, int(player_count))
    leader = int(strength.argmax().detach().item()) if strength.numel() > 0 else pid
    prod_by_owner = torch.zeros(int(player_count), dtype=dtype, device=device)
    owner_all = obs.owner_abs.to(device=device).long()
    for oid in range(int(player_count)):
        prod_by_owner[oid] = prod[(obs.alive & (owner_all == oid))].sum()
    my_prod = prod_by_owner[pid] if 0 <= pid < int(player_count) else torch.zeros((), dtype=dtype, device=device)
    leader_prod = prod_by_owner[leader] if 0 <= leader < int(player_count) else my_prod
    prod_gap = float((my_prod - leader_prod).detach().item())
    prod_rank = int((prod_by_owner > my_prod).sum().detach().item()) + 1
    trailing = (prod_gap <= float(config.v6_prod_gap_trigger)) or (prod_rank >= int(config.v6_prod_rank_trigger))

    hard_veto = torch.zeros_like(valid)
    penalty = torch.zeros_like(score)
    step_early = int(step) <= int(config.v10_early_step_end)
    step_mid = int(step) <= int(config.v10_mid_step_end)
    multi_enemy_close = close_enemy_count >= 2.0
    unsafe_reaction = reaction_gap < float(config.v10_safe_reaction_gap)
    hard_unsafe_reaction = reaction_gap <= float(config.v10_hard_reaction_gap)
    center_or_shared = (target_center_dist <= float(config.v10_center_dist)) | multi_enemy_close
    far_target = target_distance >= float(config.v10_far_dist)
    low_value_target = target_prod <= float(config.v10_low_target_prod_max)

    v10_active = step_mid and int(step) >= int(config.v10_activation_step_start)
    if v10_active:
        public_good = (
            public_target
            & valid
            & unsafe_reaction
            & (
                multi_enemy_close
                | source_reserve_violation
                | ((depletion_ratio >= float(config.v10_public_depletion_ratio)) & center_or_shared)
            )
            & (
                center_or_shared
                | far_target
                | low_value_target
                | (pressure_t >= flat_send * 0.25)
            )
        )
        hard_public_good = public_good & (
            (low_value_target & multi_enemy_close & hard_unsafe_reaction)
            | (
                source_reserve_violation
                & (depletion_ratio >= float(config.v10_blackout_depletion_ratio))
                & (multi_enemy_close | center_or_shared)
            )
            | (step_early & center_or_shared & multi_enemy_close)
        )
        hard_veto = hard_veto | hard_public_good
        penalty = penalty + torch.where(
            public_good & ~hard_public_good,
            torch.full_like(score, float(config.v10_public_good_penalty))
            + close_enemy_count * 1.75
            + (float(config.v10_safe_reaction_gap) - reaction_gap).clamp(min=0.0) * 0.75
            + (depletion_ratio - float(config.v10_public_depletion_ratio)).clamp(min=0.0) * flat_send * 0.18
            + torch.where(source_reserve_violation, source_prod + pressure_s * 0.03, torch.zeros_like(score)),
            torch.zeros_like(score),
        )

        center_sacrifice = (
            public_target
            & valid
            & center_or_shared
            & unsafe_reaction
            & (depletion_ratio >= 0.64)
            & (source_prod >= 2.0)
        )
        penalty = penalty + torch.where(
            center_sacrifice & ~hard_veto,
            torch.full_like(score, float(config.v10_center_sacrifice_penalty))
            + close_enemy_count
            + target_center_dist.clamp(max=50.0) * 0.05,
            torch.zeros_like(score),
        )

        low_enemy_while_trailing = (
            bool(trailing)
            & owner_is_enemy
            & (owner != leader)
            & low_value_target
            & unsafe_reaction
            & (
                source_reserve_violation
                | ((depletion_ratio >= float(config.v10_public_depletion_ratio)) & multi_enemy_close)
            )
            & valid
        )
        hard_veto = hard_veto | (
            low_enemy_while_trailing
            & hard_unsafe_reaction
            & (depletion_ratio >= float(config.v10_blackout_depletion_ratio))
        )
        penalty = penalty + torch.where(
            low_enemy_while_trailing & ~hard_veto,
            torch.full_like(score, float(config.v10_trailing_low_enemy_penalty)),
            torch.zeros_like(score),
        )

    if bool(v10_active):
        safe_frontier = (
            public_target
            & valid
            & (target_prod >= 3.0)
            & (reaction_gap >= float(config.v10_safe_reaction_gap))
            & (close_enemy_count <= 1.0)
            & (depletion_ratio <= float(config.v10_public_depletion_ratio))
            & ~source_reserve_violation
        )
    else:
        safe_frontier = torch.zeros_like(valid)
    bonus = torch.where(
        safe_frontier,
        torch.full_like(score, float(config.v10_safe_frontier_bonus))
        + target_prod.clamp(min=0.0, max=5.0) * 0.30
        + reaction_gap.clamp(min=0.0, max=8.0) * 0.15,
        torch.zeros_like(score),
    )

    before_masked = torch.where(valid, score, torch.full_like(score, float("-inf")))
    before_idx = int(torch.argmax(before_masked).detach().item())
    adjusted = score - penalty + bonus
    adjusted = torch.where(hard_veto & ~owner_is_mine, torch.full_like(score, float("-inf")), adjusted)
    after_masked = torch.where(valid & torch.isfinite(adjusted), adjusted, torch.full_like(score, float("-inf")))
    after_idx = int(torch.argmax(after_masked).detach().item()) if bool(torch.isfinite(after_masked).any()) else before_idx

    if bool(config.enable_v10_trace):
        def item_float(vec: Tensor, idx: int) -> float:
            return float(vec[idx].detach().item())

        def item_int(vec: Tensor, idx: int) -> int:
            return int(vec[idx].detach().item())

        _V10_TRACE_LAST = {
            "step": int(step),
            "player": pid,
            "player_count": int(player_count),
            "changed_top": bool(after_idx != before_idx),
            "reason": "role_lock_filter",
            "prod_gap": prod_gap,
            "prod_rank": int(prod_rank),
            "trailing": bool(trailing),
            "hard_veto_count": int((hard_veto & valid).sum().detach().item()),
            "public_good_penalty_count": int(((penalty > 0.0) & valid).sum().detach().item()),
            "safe_frontier_bonus_count": int((safe_frontier & valid).sum().detach().item()),
            "source_reserve_violation_count": int((source_reserve_violation & valid).sum().detach().item()),
            "before_idx": before_idx,
            "before_src": item_int(flat_src, before_idx),
            "before_tgt": item_int(flat_tgt, before_idx),
            "before_send": item_float(flat_send, before_idx),
            "before_score": item_float(score, before_idx),
            "before_owner": item_int(owner, before_idx),
            "before_target_prod": item_float(target_prod, before_idx),
            "before_source_prod": item_float(source_prod, before_idx),
            "before_reaction_gap": item_float(reaction_gap, before_idx),
            "before_close_enemy_count": item_float(close_enemy_count, before_idx),
            "before_depletion_ratio": item_float(depletion_ratio, before_idx),
            "before_hard_veto": bool(hard_veto[before_idx].detach().item()),
            "after_idx": after_idx,
            "after_src": item_int(flat_src, after_idx),
            "after_tgt": item_int(flat_tgt, after_idx),
            "after_send": item_float(flat_send, after_idx),
            "after_score": item_float(adjusted, after_idx),
            "after_owner": item_int(owner, after_idx),
            "after_target_prod": item_float(target_prod, after_idx),
            "after_source_prod": item_float(source_prod, after_idx),
            "after_reaction_gap": item_float(reaction_gap, after_idx),
            "after_close_enemy_count": item_float(close_enemy_count, after_idx),
            "after_depletion_ratio": item_float(depletion_ratio, after_idx),
        }
    return adjusted


_V6_TRACE_LAST: dict = {}


def _apply_v5_selected_action_filter(
    *,
    score: Tensor,
    obs,
    cache,
    prod: Tensor,
    target_idx: Tensor,
    cand_src: Tensor,
    cand_send: Tensor,
    cand_eta: Tensor,
    cand_tgt_short: Tensor,
    cand_is_def: Tensor,
    cand_valid: Tensor,
    enemy_mass: Tensor | None,
    config: ProducerLiteConfig,
    player_count: int,
    step: int,
) -> Tensor:
    """Narrow V6 top-action replacement with trace."""
    global _V6_TRACE_LAST
    if int(player_count) < 4 or score.numel() == 0:
        return score

    P = int(obs.P)
    device = score.device
    dtype = score.dtype
    pid = int(obs.player_id)
    valid = cand_valid.reshape(-1) & torch.isfinite(score)
    if not bool(valid.any()):
        if bool(config.enable_v5_trace):
            _V6_TRACE_LAST = {
                "step": int(step),
                "player": pid,
                "player_count": int(player_count),
                "changed": False,
                "reason": "no_valid_candidate",
            }
        return score

    masked = torch.where(valid, score, torch.full_like(score, float("-inf")))
    before_idx = int(torch.argmax(masked).detach().item())
    before_score = masked[before_idx]
    fired = bool(torch.isfinite(before_score) and before_score > float(config.roi_threshold))

    flat_src = cand_src.reshape(-1).clamp(0, max(P - 1, 0)).long()
    flat_send = cand_send.reshape(-1).to(dtype=dtype, device=device)
    flat_eta = cand_eta.reshape(-1).to(dtype=dtype, device=device)
    flat_tgt_short = cand_tgt_short.reshape(-1)
    flat_tgt = target_idx[flat_tgt_short].clamp(0, max(P - 1, 0)).long()

    owner = obs.owner_abs.to(device=device)[flat_tgt].long()
    target_prod = prod.to(device=device, dtype=dtype)[flat_tgt]
    target_ships = obs.ships.to(device=device, dtype=dtype)[flat_tgt]
    source_prod = prod.to(device=device, dtype=dtype)[flat_src]
    source_ships = obs.ships.to(device=device, dtype=dtype)[flat_src].clamp(min=1.0)
    source_after = (source_ships - flat_send).clamp(min=0.0)
    target_distance = cache.cross_dist[0].to(dtype=dtype, device=device)[flat_src, flat_tgt]

    enemy_source_mask = (
        obs.alive
        & obs.is_enemy
        & (obs.ships >= float(config.min_ships_to_launch))
    )
    enemy_eta_targets = _best_eta_to_targets(
        obs, cache, source_mask=enemy_source_mask, target_idx=target_idx,
        max_k=int(config.horizon),
    )
    reaction_gap = enemy_eta_targets[flat_tgt_short].to(dtype=dtype, device=device) - flat_eta

    pressure_s = (
        enemy_mass[flat_src].to(dtype=dtype, device=device)
        if enemy_mass is not None
        else torch.zeros_like(source_ships)
    )
    depletion_ratio = flat_send / source_ships
    strength = _ffa_strength(obs, prod, int(player_count))
    leader = int(strength.argmax().detach().item()) if strength.numel() > 0 else pid
    owner_abs = obs.owner_abs.to(device=device).long()
    prod_by_owner = torch.zeros(int(player_count), dtype=dtype, device=device)
    for oid in range(int(player_count)):
        prod_by_owner[oid] = prod[(obs.alive & (owner_abs == oid))].sum()
    my_prod_t = prod_by_owner[pid] if 0 <= pid < int(player_count) else torch.tensor(0.0, dtype=dtype, device=device)
    leader_prod_t = prod_by_owner[leader] if 0 <= leader < int(player_count) else torch.tensor(0.0, dtype=dtype, device=device)
    my_prod = float(my_prod_t.detach().item())
    leader_prod = float(leader_prod_t.detach().item())
    prod_gap = my_prod - leader_prod
    prod_rank = 1
    for oid in range(int(player_count)):
        if oid != pid and float(prod_by_owner[oid].detach().item()) > my_prod + 1e-6:
            prod_rank += 1
    v6_gap_active = (
        bool(config.enable_v6_prod_gap_mode)
        and int(config.v6_gap_step_start) <= int(step) <= int(config.v6_gap_step_end)
        and (
            prod_gap <= float(config.v6_prod_gap_trigger)
            or prod_rank >= int(config.v6_prod_rank_trigger)
        )
    )

    owner_is_enemy = (owner >= 0) & (owner != pid) & (owner < int(player_count)) & ~cand_is_def.reshape(-1)
    owner_is_neutral = (owner < 0) & ~cand_is_def.reshape(-1)
    owner_is_mine = (owner == pid) | cand_is_def.reshape(-1)
    nonleader_enemy = owner_is_enemy & (owner != leader)

    low_far_neutral = (
        owner_is_neutral
        & (target_prod <= float(config.v5_low_neutral_prod_max))
        & (target_distance >= float(config.v5_far_dist))
    )
    low_far_nonleader_enemy = (
        nonleader_enemy
        & (target_prod <= float(config.v5_low_enemy_prod_max))
        & ((target_distance >= float(config.v5_far_dist)) | (flat_eta > float(config.ffa_enemy_rear_eta)))
    )
    depleted_source = (
        (depletion_ratio >= float(config.v5_source_depletion_ratio))
        & ((source_prod >= 3.0) | (pressure_s >= source_ships * float(config.ffa_source_pressure_gate)))
        & (
            (target_prod <= float(config.v5_low_enemy_prod_max))
            | (reaction_gap < 0.0)
            | (target_distance >= float(config.v5_far_dist))
        )
    )
    bad_top_mask = low_far_neutral | low_far_nonleader_enemy | depleted_source
    gap_mode_bad_attack = (
        v6_gap_active
        & ~owner_is_mine
        & (
            (
                owner_is_enemy
                & (target_prod <= float(config.v6_gap_low_target_prod_max))
                & (source_prod >= float(config.v6_gap_high_source_prod_min))
                & (depletion_ratio >= float(config.v6_gap_depletion_ratio))
                & (reaction_gap <= float(config.v6_gap_bad_reaction_gap))
            )
            | (
                owner_is_neutral
                & (target_prod <= float(config.v6_gap_low_target_prod_max))
                & (target_distance >= float(config.v6_gap_near_dist))
                & (reaction_gap <= float(config.v6_gap_bad_reaction_gap))
            )
        )
    )
    bad_top_mask = bad_top_mask | gap_mode_bad_attack
    bad_top = bool(fired and bad_top_mask[before_idx].detach().item())

    before_reason = "ok"
    if bad_top:
        if bool(gap_mode_bad_attack[before_idx].detach().item()):
            before_reason = "prod_gap_bad_attack_with_safe_alt"
        elif bool(low_far_neutral[before_idx].detach().item()):
            before_reason = "far_low_neutral_with_safe_alt"
        elif bool(low_far_nonleader_enemy[before_idx].detach().item()):
            before_reason = "far_low_nonleader_enemy_with_safe_alt"
        else:
            before_reason = "source_depletion_with_safe_alt"

    alt_score_gap = float(config.v6_gap_alt_score_gap) if v6_gap_active else float(config.v5_alt_score_gap)
    score_gap_ok = score >= (before_score - alt_score_gap)
    prod_gain_ok = target_prod >= (target_prod[before_idx] + float(config.v5_alt_min_prod_gain))
    reaction_ok = reaction_gap >= float(config.v5_alt_safe_reaction_gap)
    gap_reaction_ok = reaction_gap >= float(config.v6_gap_safe_reaction_gap)
    gap_regroup_ok = v6_gap_active & owner_is_mine
    gap_frontier_ok = (
        v6_gap_active
        & (target_distance <= float(config.v6_gap_near_dist))
        & ((target_prod >= target_prod[before_idx]) | (reaction_gap >= 0.0))
    )
    depletion_ok = depletion_ratio <= torch.minimum(
        depletion_ratio[before_idx] - 0.05,
        torch.full_like(depletion_ratio, 0.84),
    )
    not_bad_alt = ~(low_far_neutral | low_far_nonleader_enemy | depleted_source | gap_mode_bad_attack)
    idx_arange = torch.arange(score.numel(), device=device)
    alt_mask = (
        bad_top
        & valid
        & (idx_arange != before_idx)
        & (score > float(config.roi_threshold))
        & score_gap_ok
        & not_bad_alt
        & (prod_gain_ok | reaction_ok | depletion_ok | gap_reaction_ok | gap_regroup_ok | gap_frontier_ok)
    )

    changed = False
    after_idx = before_idx
    adjusted = score
    if bool(alt_mask.any()):
        gap_alt_bonus = torch.zeros_like(score)
        if v6_gap_active:
            gap_alt_bonus = (
                torch.where(owner_is_mine, torch.full_like(score, 1.8), torch.zeros_like(score))
                + target_prod.clamp(min=0.0, max=5.0) * 0.45
                + reaction_gap.clamp(min=-2.0, max=8.0) * 0.20
                - target_distance.clamp(min=0.0, max=120.0) * 0.008
                - depletion_ratio.clamp(min=0.0, max=1.0) * 0.55
            )
        alt_scores = torch.where(alt_mask, score + gap_alt_bonus, torch.full_like(score, float("-inf")))
        after_idx = int(torch.argmax(alt_scores).detach().item())
        adjusted = score.clone()
        adjusted[after_idx] = torch.maximum(
            adjusted[after_idx],
            before_score + (float(config.v6_gap_force_bonus) if v6_gap_active else float(config.v5_force_bonus)),
        )
        adjusted[before_idx] = torch.minimum(
            adjusted[before_idx],
            score[after_idx] - (float(config.v6_gap_force_bonus) if v6_gap_active else float(config.v5_force_bonus)),
        )
        changed = after_idx != before_idx

    if bool(config.enable_v5_trace):
        def item_float(vec: Tensor, idx: int) -> float:
            return float(vec[idx].detach().item())

        def item_int(vec: Tensor, idx: int) -> int:
            return int(vec[idx].detach().item())

        _V6_TRACE_LAST = {
            "step": int(step),
            "player": pid,
            "player_count": int(player_count),
            "changed": bool(changed),
            "reason": before_reason if changed else ("bad_no_alt" if bad_top else "no_bad_top"),
            "my_prod": my_prod,
            "leader_prod": leader_prod,
            "prod_gap": prod_gap,
            "prod_rank": int(prod_rank),
            "v6_gap_active": bool(v6_gap_active),
            "before_idx": before_idx,
            "before_src": item_int(flat_src, before_idx),
            "before_tgt": item_int(flat_tgt, before_idx),
            "before_send": item_float(flat_send, before_idx),
            "before_score": item_float(score, before_idx),
            "before_owner": item_int(owner, before_idx),
            "before_target_prod": item_float(target_prod, before_idx),
            "before_target_ships": item_float(target_ships, before_idx),
            "before_source_ships": item_float(source_ships, before_idx),
            "before_source_prod": item_float(source_prod, before_idx),
            "before_distance": item_float(target_distance, before_idx),
            "before_reaction_gap": item_float(reaction_gap, before_idx),
            "before_depletion_ratio": item_float(depletion_ratio, before_idx),
            "after_idx": after_idx,
            "after_src": item_int(flat_src, after_idx),
            "after_tgt": item_int(flat_tgt, after_idx),
            "after_send": item_float(flat_send, after_idx),
            "after_score": item_float(adjusted, after_idx),
            "after_owner": item_int(owner, after_idx),
            "after_target_prod": item_float(target_prod, after_idx),
            "after_target_ships": item_float(target_ships, after_idx),
            "after_source_ships": item_float(source_ships, after_idx),
            "after_source_prod": item_float(source_prod, after_idx),
            "after_distance": item_float(target_distance, after_idx),
            "after_reaction_gap": item_float(reaction_gap, after_idx),
            "after_depletion_ratio": item_float(depletion_ratio, after_idx),
            "alt_count": int(alt_mask.sum().detach().item()) if bad_top else 0,
            "low_far_neutral_count": int((low_far_neutral & valid).sum().detach().item()),
            "low_far_nonleader_enemy_count": int((low_far_nonleader_enemy & valid).sum().detach().item()),
            "depleted_source_count": int((depleted_source & valid).sum().detach().item()),
            "gap_mode_bad_attack_count": int((gap_mode_bad_attack & valid).sum().detach().item()),
        }
    return adjusted


# ---------------------------------------------------------------------------
# Late-game candidate suppression
# ---------------------------------------------------------------------------

def _suppress_late_candidates(
    *,
    score: Tensor,
    obs,
    target_idx: Tensor,
    cand_tgt_short: Tensor,
    cand_is_def: Tensor,
    cand_eta: Tensor,
    step: int,
    player_id: int,
) -> Tensor:
    """Suppress attacks that arrive too late; devalue late neutral captures."""
    remaining = TOTAL_STEPS - int(step)
    # Only activate in last 120 turns
    if remaining > 120:
        return score
    P = int(obs.P)
    if P <= 0 or score.numel() == 0:
        return score
    device = score.device
    dtype = score.dtype
    pid = int(player_id)
    tgt_abs = target_idx[cand_tgt_short].clamp(0, P - 1)
    tgt_owner = obs.owner_abs.to(device=device)[tgt_abs].long()
    eta = cand_eta.reshape(score.shape).to(device=device, dtype=dtype)

    is_neutral = tgt_owner < 0
    is_enemy = (tgt_owner >= 0) & (tgt_owner != pid) & (~cand_is_def)

    # Too late to matter
    neutral_margin = max(1.0, float(remaining) - 8.0)
    enemy_margin = max(1.0, float(remaining) - 4.0)
    too_late = (is_neutral & (eta > neutral_margin)) | (is_enemy & (eta > enemy_margin))

    # Late neutrals depreciate — fewer turns to repay launch cost
    neutral_factor = ((float(remaining) - eta) / max(1.0, 80.0)).clamp(min=0.20, max=1.0)
    score = torch.where(is_neutral, score * neutral_factor, score)
    return torch.where(too_late, torch.full_like(score, float("-inf")), score)


# ---------------------------------------------------------------------------
# Core planner
# ---------------------------------------------------------------------------

def plan_lite_waves(
    *,
    movement: PlanetMovement,
    obs,
    obs_tensors: dict,
    cache,
    garrison_status,
    prod: Tensor,
    alive_by_step: Tensor,
    config: ProducerLiteConfig,
    player_count: int,
):
    """Single-size attack planner + regroup. One candidate per (source, target)."""
    P = obs.P
    device = obs.device
    dtype = obs.ships.dtype
    pid = int(obs.player_id)
    step = int(obs_tensors["step"].reshape(-1)[0].item())

    H_axis = int(garrison_status.ships.shape[-1])
    H = max(H_axis - 1, 0)
    K_eta = max(1, min(int(config.horizon), H))
    W = max(1, int(config.max_waves_per_turn))

    source_mask = obs.owned & obs.alive & (obs.ships >= float(config.min_ships_to_launch))
    if not bool(source_mask.any()):
        return _empty_entries(device, dtype)

    S_cap = max(1, min(int(config.max_sources_per_lane), P))
    source_idx, source_exists = _candidate_indices(obs.ships, source_mask, S_cap)
    target_idx, target_exists = build_target_shortlist(
        obs, obs_tensors, garrison_status, cache,
        config=config, K_eta=K_eta, H=H, prod=prod, source_mask=source_mask,
    )
    if not bool(target_exists.any()):
        return _empty_entries(device, dtype)
    S = int(source_idx.shape[0])
    T = int(target_idx.shape[0])
    target_is_mine = obs.owned[target_idx.clamp(0, P - 1)]

    source_ships = obs.ships[source_idx.clamp(0, P - 1)].to(dtype)
    H_eff = torch.full((), float(H), dtype=dtype, device=device)
    drain = safe_drain(
        garrison_status, source_idx=source_idx, source_ships=source_ships,
        H_eff=H_eff, player_id=pid,
    )

    eta_cap = torch.full((T,), float(K_eta), dtype=dtype, device=device)

    # Enemy pressure — reused for β floor and regroup
    beta = float(config.reinforce_size_beta)
    enemy_mass = (
        cheap_enemy_pressure(obs, cache, horizon=float(K_eta), player_id=pid)
        if beta > 0.0 or bool(config.enable_regroup) else None
    )
    if bool(config.enable_ffa_mission_filter) and int(player_count) >= 4:
        drain = _apply_4p_source_reserve(
            drain, obs=obs, prod=prod, source_idx=source_idx,
            enemy_mass=enemy_mass, config=config, step=int(step),
        )

    # Reinforcement risk floor
    reinforcement = None
    if beta > 0.0:
        enemy_mass_t = enemy_mass[target_idx.clamp(0, P - 1)]
        k_arange = torch.arange(1, K_eta + 1, device=device, dtype=dtype)
        rho = reinforcement_timing_factor(
            k_arange, eta_free=float(config.reinforce_eta_free),
            eta_scale=float(config.reinforce_eta_scale),
        )
        reinforcement = beta * rho.view(1, K_eta) * enemy_mass_t.view(T, 1)
    floor = capture_floor(
        garrison_status, target_idx=target_idx, k_max=K_eta,
        capture_overhead=1.0, player_id=pid,
        reinforcement=reinforcement,
    )
    K = int(floor.shape[-1])

    # Single size = safe_drain (full garrison launch)
    sizes = drain.view(S, 1).expand(S, T).floor().clamp(min=1.0)

    active = reachable_mask(
        movement, source_idx=source_idx, target_idx=target_idx,
        fleet_sizes=sizes.unsqueeze(-1), eta_cap=eta_cap,
    ).squeeze(-1)
    aim = intercept_angle(
        movement,
        source_idx.unsqueeze(1),
        target_idx.unsqueeze(0),
        sizes,
        active=active,
    )
    angle = aim["angle"]
    eta = aim["eta"]
    viable = aim["viable"] & (eta <= eta_cap.view(1, T))

    if K > 0:
        k_arr = (eta.clamp(min=1.0, max=float(K)).ceil().long() - 1).clamp(0, K - 1)
        floor_at_arr = floor.unsqueeze(0).expand(S, T, K).gather(-1, k_arr.unsqueeze(-1)).squeeze(-1)
    else:
        floor_at_arr = torch.ones(S, T, dtype=dtype, device=device)
    clears_floor = sizes >= floor_at_arr

    src_neq_tgt = source_idx.view(S, 1) != target_idx.view(1, T)
    valid = (
        viable & clears_floor & (sizes >= float(config.min_ships_to_launch))
        & src_neq_tgt & source_exists.view(S, 1) & target_exists.view(1, T)
    )

    L = 1
    C = S * T
    cand_src = source_idx.view(S, 1).expand(S, T).reshape(C, L)
    cand_tgt_slot = target_idx.view(1, T).expand(S, T).reshape(C)
    cand_tgt_short = torch.arange(T, device=device).view(1, T).expand(S, T).reshape(C)
    cand_send = torch.where(valid, sizes, torch.zeros_like(sizes)).reshape(C, L)
    cand_angle = angle.reshape(C, L)
    cand_eta = torch.where(valid, eta, torch.ones_like(eta)).reshape(C, L)
    cand_active = valid.reshape(C, L)
    cand_valid = valid.reshape(C)
    cand_is_def = target_is_mine[cand_tgt_short]

    launches = make_launch_set(
        source_slots=cand_src,
        target_slots=cand_tgt_slot.unsqueeze(-1).expand(C, L),
        ships=cand_send,
        eta=cand_eta,
        valid=cand_active & cand_valid.unsqueeze(-1),
        player_id=pid,
    )
    score = score_candidates(
        garrison_status, prod=prod, alive_by_step=alive_by_step,
        player_count=int(player_count), launches=launches, player_id=pid,
    )

    # Late-game suppression
    score = _suppress_late_candidates(
        score=score, obs=obs, target_idx=target_idx,
        cand_tgt_short=cand_tgt_short, cand_is_def=cand_is_def,
        cand_eta=cand_eta, step=int(step), player_id=pid,
    )
    if bool(config.enable_ffa_mission_filter) and int(player_count) >= 4:
        score = _apply_4p_candidate_adjustments(
            score=score, obs=obs, cache=cache, prod=prod, target_idx=target_idx,
            cand_src=cand_src, cand_send=cand_send, cand_eta=cand_eta,
            cand_tgt_short=cand_tgt_short, cand_is_def=cand_is_def,
            cand_valid=cand_valid, floor_at_arr=floor_at_arr.reshape(C),
            enemy_mass=enemy_mass, config=config, player_count=int(player_count),
        )
    if bool(config.enable_v10_role_lock) and int(player_count) >= 4:
        score = _apply_v10_role_lock_filter(
            score=score, obs=obs, cache=cache, prod=prod, target_idx=target_idx,
            cand_src=cand_src, cand_send=cand_send, cand_eta=cand_eta,
            cand_tgt_short=cand_tgt_short, cand_is_def=cand_is_def,
            cand_valid=cand_valid, enemy_mass=enemy_mass, config=config,
            player_count=int(player_count), step=int(step),
        )

    score = torch.where(cand_valid, score, torch.full_like(score, float("-inf")))
    if bool(config.enable_v5_selected_filter) and int(player_count) >= 4:
        score = _apply_v5_selected_action_filter(
            score=score, obs=obs, cache=cache, prod=prod, target_idx=target_idx,
            cand_src=cand_src, cand_send=cand_send, cand_eta=cand_eta,
            cand_tgt_short=cand_tgt_short, cand_is_def=cand_is_def,
            cand_valid=cand_valid, enemy_mass=enemy_mass, config=config,
            player_count=int(player_count), step=int(step),
        )

    wave_entries, leftover = _greedy_select(
        P=P, W=W, device=device, dtype=dtype, score=score,
        cand_src=cand_src, cand_send=cand_send, cand_angle=cand_angle, cand_eta=cand_eta,
        cand_active=cand_active, cand_tgt_slot=cand_tgt_slot, cand_tgt_short=cand_tgt_short,
        cand_is_def=cand_is_def, source_budget=obs.ships.to(dtype).clone(),
        target_exists=target_exists, roi_threshold=float(config.roi_threshold),
    )

    if not bool(config.enable_regroup):
        return wave_entries

    regroup_entries = _plan_regroup(
        movement=movement, obs=obs, obs_tensors=obs_tensors, garrison_status=garrison_status,
        leftover=leftover, original_ships=obs.ships.to(dtype), pressure=enemy_mass,
        config=config, H=H,
    )
    return concat_launch_entries([wave_entries, regroup_entries])


# ---------------------------------------------------------------------------
# Turn pipeline
# ---------------------------------------------------------------------------

def run_turn(obs_tensors: dict, *, config: ProducerLiteConfig, player_count: int, memory) -> dict:
    global _V6_TRACE_LAST, _V10_TRACE_LAST
    _V6_TRACE_LAST = {}
    _V10_TRACE_LAST = {}
    device = obs_tensors["planets"].device
    obs = parse_obs(obs_tensors)
    P = obs.P
    if P == 0:
        return empty_action_row(device)

    movement = ensure_planet_movement(
        obs_tensors=obs_tensors,
        expected_cfg=_movement_config(config, player_count=int(player_count)),
        cached_movement=getattr(memory, "movement", None),
    )
    memory.movement = movement
    step = int(obs_tensors["step"].reshape(-1)[0].item())

    # Dynamic adjustment: continuously tune ROI + waves based on game state
    config = _adjust_config(
        config, obs=obs, prod=movement.planet_prod, step=step, player_count=int(player_count)
    )

    cache = build_distance_cache(movement, max_k=int(config.horizon))
    H = int(config.horizon)
    status = movement.garrison_status(max_horizon=H)
    alive_by_step = movement.alive_by_step[: H + 1]

    entries = plan_lite_waves(
        movement=movement, obs=obs, obs_tensors=obs_tensors, cache=cache,
        garrison_status=status, prod=movement.planet_prod,
        alive_by_step=alive_by_step, config=config, player_count=int(player_count),
    )
    entries = disambiguate_duplicate_launches(entries)
    launches = infer_planned_launches_from_entries(
        obs_tensors=obs_tensors, movement=movement, entries=entries, player_id=int(obs.player_id),
    )
    apply_private_planned_launches(
        movement=movement, launches=launches, owner_id=int(obs.player_id),
        obs_tensors=obs_tensors,
    )
    planet_ids = obs_tensors["planets"][..., 0].long()
    return entries_to_sparse_payload(entries, planet_ids=planet_ids)


# ---------------------------------------------------------------------------
# Mode presets
# ---------------------------------------------------------------------------

CONFIG_2P = ProducerLiteConfig()  # ROI=1.40, horizon=18, waves=6

CONFIG_3P = replace(
    ProducerLiteConfig(),
    horizon=15,
    max_sources_per_lane=8,
    max_offensive_targets=10,
    max_defensive_targets=3,
    roi_threshold=1.35,
)

CONFIG_4P = replace(
    ProducerLiteConfig(),
    horizon=13,
    roi_threshold=1.25,
    max_sources_per_lane=7,
    max_defensive_targets=2,
    max_waves_per_turn=6,
    max_regroup_time=6.0,
    max_regroup_targets_per_source=8,
    enable_ffa_mission_filter=True,
    ffa_source_reserve_frac=0.03,
    ffa_source_reserve_prod_mult=0.30,
    ffa_source_reserve_pressure_mult=0.015,
    enable_v5_selected_filter=True,
    enable_v5_trace=True,
    enable_v6_prod_gap_mode=True,
    enable_v10_role_lock=True,
    enable_v10_trace=True,
)


def _config_for(player_count: int) -> ProducerLiteConfig:
    pc = int(player_count)
    if pc >= 4:
        return CONFIG_4P
    elif pc == 3:
        return CONFIG_3P
    return CONFIG_2P


# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------

class ProducerLiteMemory:
    def __init__(self) -> None:
        self.movement = None
        self.cached_player_count: int | None = None
        self.last_sparse_action_row: dict | None = None

    def reset(self) -> None:
        self.movement = None
        self.cached_player_count = None
        self.last_sparse_action_row = None


class ProducerLiteRuntime:
    def __init__(self, memory: ProducerLiteMemory | None = None) -> None:
        self.memory = memory if memory is not None else ProducerLiteMemory()

    def reset(self) -> None:
        self.memory.reset()

    def tensor_action(self, obs_tensors: dict):
        mem = self.memory
        if bool((obs_tensors["step"] == 0).all()):
            mem.cached_player_count = None
        if mem.cached_player_count is None:
            mem.cached_player_count = largest_initial_player_count(obs_tensors)
        config = _config_for(mem.cached_player_count)
        row = run_turn(
            obs_tensors, config=config,
            player_count=int(mem.cached_player_count), memory=mem,
        )
        trace_path = (
            os.environ.get("ORBIT_V10_TRACE_PATH")
            or os.environ.get("ORBIT_V6_TRACE_PATH")
            or os.environ.get("ORBIT_V5_TRACE_PATH")
        )
        trace_payload = {}
        if _V6_TRACE_LAST:
            trace_payload.update(_V6_TRACE_LAST)
        if _V10_TRACE_LAST:
            trace_payload["v10"] = _V10_TRACE_LAST
        if trace_path and trace_payload:
            try:
                trace_dir = os.path.dirname(trace_path)
                if trace_dir:
                    os.makedirs(trace_dir, exist_ok=True)
                with open(trace_path, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(trace_payload, sort_keys=True) + "\n")
            except Exception:
                pass
        mem.last_sparse_action_row = row
        return row


_RUNTIME = ProducerLiteRuntime()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def agent(obs):
    """Single-observation entry point for local play and Kaggle."""
    player = obs.get("player", 0) if isinstance(obs, dict) else obs.player
    player_id = int(player)
    obs_tensors = single_obs_to_tensor(obs, player_id=player_id)
    with torch.no_grad():
        sparse_row = _RUNTIME.tensor_action(obs_tensors)
    return sparse_action_row_to_moves(sparse_row, obs, player_id=player_id)
