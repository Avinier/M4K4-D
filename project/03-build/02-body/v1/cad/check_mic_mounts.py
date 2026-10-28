"""Verify the shell-mounted PCB-06 microphone boards (D-037).

Each board lands on a printed boss on the shell's inner skin, a foam gasket in a
pocket round the port seals it, and two M2 thread-forming screws clamp it. The
boards ride with the shell when it is lowered; check_shell_frame_fit.py covers
that path. This script checks the seat, seal, port, screws and static clearance.
"""

import json
import math
from pathlib import Path

from build123d import Location, Vector

import body_v1_model as M

HERE = Path(__file__).resolve().parent
MIN_SKIN_BEYOND_PILOT = 0.8  # mm of shell left outside each blind M2 pilot
MIN_ENGAGEMENT = 2.5  # mm of M2 thread formed into the boss (1.25 d)
GASKET_COMPRESSION = (0.20, 0.40)  # closed-cell foam working range
UPPER_RAIL_ABS_Y = 68.0  # inboard face of the frame's upper side rails
LOWERING_CLEARANCE = 0.5


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    ab, bb = a.bounding_box(), b.bounding_box()
    if (ab.max.X <= bb.min.X or bb.max.X <= ab.min.X or
        ab.max.Y <= bb.min.Y or bb.max.Y <= ab.min.Y or
        ab.max.Z <= bb.min.Z or bb.max.Z <= ab.min.Z):
        return 0.0
    common = a & b
    return 0.0 if common is None else round(common.volume, 3)


def material_beyond(shell, x, y_start, z, sign, step=0.02):
    """Shell material along +|Y| from y_start until the first exit, mm."""
    y = y_start + step / 2.0
    while shell.is_inside(Vector(x, sign * y, z)):
        y += step
    return y - y_start - step / 2.0


def main():
    shell = M.body_shell()
    audio = M.body_audio()
    mic_groups = [c for c in audio.children if (c.label or "").startswith("PDM_MIC_")]
    mic_parts = [leaf for group in mic_groups for leaf in leaves(group)]
    other_audio = [leaf for c in audio.children if not (c.label or "").startswith("PDM_MIC_") for leaf in leaves(c)]
    others = [
        *leaves(M.body_primary_frame()), *leaves(M.electronics()), *leaves(M.sensors()),
        *leaves(M.harness_routes()), *leaves(M.connectors_and_exits()), *other_audio,
        *leaves(M.body_panels()), *leaves(M.panel_mount_hardware()), *leaves(M.shell_frame_hardware()),
        *leaves(M.wheel_arch_hardware()), *leaves(M.body_yaw_stage()), *M.yaw_drive_moving_parts(),
        *leaves(M.chassis_v1_reference()),
    ]

    results = {"per_mic": {}, "mic_shell_overlap_mm3": {}, "mic_other_overlap_mm3": {}, "mic_self_overlap_mm3": {}}
    f = M.MIC_BOARD_OUTER_Y
    wy = M.MIC_BOARD_SIZE[1]
    compression = 1.0 - M.MIC_GASKET_POCKET_DEPTH / M.MIC_GASKET_FREE_THICKNESS
    engagement = M.MIC_SCREW_LENGTH - wy

    for x, y, z, name in M.MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0
        centre = -1.0 if x > M.BODY_AXIS_X else 1.0
        group = next(g for g in mic_groups if g.label == f"PDM_MIC_{name}")
        parts = {leaf.label: leaf for leaf in leaves(group)}
        board = parts[f"PDM_MIC_{name}_PCB06"]
        package = parts[f"PDM_MIC_{name}_IM73D122"].bounding_box()
        gasket = parts[f"PDM_MIC_{name}_GASKET"]

        # Seated: the board's outer face touches the boss, and no part enters the shell.
        seated = overlap(board.moved(Location((0.0, sign * 0.05, 0.0))), shell) > 0.0
        gasket_seated = overlap(gasket.moved(Location((0.0, sign * 0.05, 0.0))), shell) > 0.0
        # Sound path: Ø0.7 probe from the mic's port face out past the skin.
        probe = M._axial_bore_y(0.35, sign * (f - wy), sign * 90.0, x, z)
        path_blockers = {p.label: v for p in (shell, board, gasket) if (v := overlap(probe, p)) > 0.001}
        # Port bore exits the outer skin: the skin point on the port axis is open.
        skin_y = M._shell_station_at(z)[3]
        port_open = not shell.is_inside(Vector(x, sign * (skin_y - 0.3), z))
        # Screws: thread engagement and skin left outside each blind pilot.
        screws = {}
        for dv in (M.MIC_SCREW_V, -M.MIC_SCREW_V):
            remaining = material_beyond(shell, x, f + M.MIC_SCREW_PILOT_DEPTH, z + dv, sign)
            screws[f"z{z + dv:.1f}"] = {
                "skin_beyond_pilot_mm": round(remaining, 2),
                "pilot_bottom_abs_y_mm": f + M.MIC_SCREW_PILOT_DEPTH,
                "outer_skin_abs_y_mm": round(M._shell_station_at(z + dv)[3], 2),
            }
        inboard_most = min(min(abs(p.bounding_box().min.Y), abs(p.bounding_box().max.Y)) for p in parts.values())
        boss_wall_to_inner_skin = M._shell_station_at(z)[3] - M.SHELL_THICKNESS - f
        results["per_mic"][name] = {
            "port_mm": [x, y, z],
            "board_outer_abs_y_mm": f,
            "board_seated_on_boss": seated,
            "gasket_seated_in_pocket": gasket_seated,
            # STEP bbox centre is the package centre; the sound port is MIC_PORT_OFFSET
            # from it toward the body centre (datasheet Fig. 13).
            "sound_port_off_axis_mm": round(math.hypot(package.center().X + centre * M.MIC_PORT_OFFSET - x, package.center().Z - z), 3),
            "package_size_mm": [round(package.size.X, 2), round(package.size.Y, 2), round(package.size.Z, 2)],
            "sound_path_blockers_mm3": path_blockers,
            "port_open_through_skin": port_open,
            "port_chain_length_mm": round(skin_y - f + wy, 2),  # skin to mic: bore + gasket + PCB
            "boss_depth_at_port_axis_mm": round(boss_wall_to_inner_skin, 2),
            "screws": screws,
            "inboard_most_abs_y_mm": round(inboard_most, 2),
            "upper_rail_lowering_clearance_mm": round(inboard_most - UPPER_RAIL_ABS_Y, 2),
        }

        for label, part in parts.items():
            v = overlap(part, shell)
            if v > 0.001:
                results["mic_shell_overlap_mm3"][label] = v
        items = list(parts.values())
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                v = overlap(a, b)
                if v > 0.001:
                    results["mic_self_overlap_mm3"][f"{a.label}:{b.label}"] = v

    for part in mic_parts:
        for other in others:
            v = overlap(part, other)
            if v > 0.001:
                results["mic_other_overlap_mm3"][f"{part.label}:{other.label or 'unnamed'}"] = v

    # E: Helmholtz estimate of the port chain (bore + gasket + PCB hole) into an
    # assumed 1-3 mm3 mic front chamber; speech needs < 8 kHz.
    c = 343_000.0
    worst_bore = max(M._shell_station_at(z)[3] - f for _, _, z, _ in M.MICROPHONE_PORTS)  # gasket ID + boss + skin
    r1, r2 = M.MIC_PORT_RADIUS, M.MIC_PCB_PORT_RADIUS
    inertance = (worst_bore + 0.85 * r1) / (math.pi * r1**2) + (wy + 2 * 0.85 * r2) / (math.pi * r2**2)
    resonance = {f"{v} mm3": round(c / (2 * math.pi) * math.sqrt(1.0 / (v * inertance))) for v in (1.0, 2.0, 3.0)}

    results["design"] = {
        "gasket_compression": round(compression, 3),
        "screw_engagement_mm": engagement,
        "worst_port_chain_length_mm": round(worst_bore + wy, 2),
        "port_resonance_hz_by_front_chamber_E": resonance,
        "upper_rail_abs_y_mm": UPPER_RAIL_ABS_Y,
    }
    per = results["per_mic"].values()
    checks = {
        "four_mic_boards": len(mic_groups) == 4,
        "boards_seated_on_bosses": all(v["board_seated_on_boss"] for v in per),
        "gaskets_seated_in_pockets": all(v["gasket_seated_in_pocket"] for v in per),
        "gasket_compression_in_range": GASKET_COMPRESSION[0] <= compression <= GASKET_COMPRESSION[1],
        "sound_ports_on_port_axes": all(v["sound_port_off_axis_mm"] < 0.01 for v in per),
        "packages_are_vendor_step_outline": all(abs(v["package_size_mm"][0] - 4.0) < 0.01 and abs(v["package_size_mm"][2] - 3.0) < 0.01 for v in per),
        "sound_paths_clear": all(not v["sound_path_blockers_mm3"] for v in per),
        "ports_open_through_skin": all(v["port_open_through_skin"] for v in per),
        "screw_engagement": engagement >= MIN_ENGAGEMENT,
        "skin_beyond_pilots": all(s["skin_beyond_pilot_mm"] >= MIN_SKIN_BEYOND_PILOT for v in per for s in v["screws"].values()),
        "boards_pass_upper_rails_when_lowered": all(v["upper_rail_lowering_clearance_mm"] >= LOWERING_CLEARANCE for v in per),
        "mic_parts_clear_shell": not results["mic_shell_overlap_mm3"],
        "mic_parts_clear_each_other": not results["mic_self_overlap_mm3"],
        "mic_parts_clear_body_and_chassis": not results["mic_other_overlap_mm3"],
        "port_resonance_above_8k_E": min(resonance.values()) > 8000,
        "shell_one_solid": len(shell.solids()) == 1,
    }
    results["checks"] = checks
    results["ok"] = all(checks.values())
    out = HERE / "generated" / "mic-mount-fit.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    if not results["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
