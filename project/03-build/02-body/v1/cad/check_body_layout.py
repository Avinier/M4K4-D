"""Audit body-v1 mass, axes, envelope and the current stability screen.

This uses the printable CAD solids rather than the old Layout 02 shell/frame
allowances. It is an estimate until the selected print process and hardware are
weighed. Fit and assembly paths have their own checks beside this script.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import body_v1_model as M


HERE = Path(__file__).resolve().parent
PETG_SKIN_G_CM3 = 1.20  # near-solid 2.4 mm walls and conservative frame estimate
PETG_ARCH_G_CM3 = 0.571  # same effective infill-density assumption as chassis
STEEL_G_CM3 = 7.85
BRASS_G_CM3 = 8.50
PHYSICS_MARGIN_A_TIP_MIN = 9.81 * 20.0 / 124.0


def properties(items):
    """Mass, mass centroid, and vertical-axis inertia about the ground origin."""
    rows = []
    for shape, density in items:
        mass = shape.volume * density / 1000.0
        centre = shape.center()
        izz = (shape.matrix_of_inertia[2][2] * density / 1000.0
               + mass * (centre.X**2 + centre.Y**2))
        rows.append((shape.label, mass, (centre.X, centre.Y, centre.Z), izz))
    total = sum(row[1] for row in rows)
    com = tuple(sum(row[1] * row[2][axis] for row in rows) / total for axis in range(3))
    return {
        "mass_g": total,
        "com_mm": com,
        "yaw_inertia_about_ground_origin_g_mm2": sum(row[3] for row in rows),
        "components": [
            {"name": name, "mass_g": mass, "com_mm": centre}
            for name, mass, centre, _ in rows
        ],
    }


def main():
    shell = M.body_shell()
    panels = M.body_panels()
    panel_mount = M.panel_mount_hardware()
    frame = M.body_primary_frame()

    shell_items = [(shell, PETG_SKIN_G_CM3)]
    shell_items += [
        (part, PETG_ARCH_G_CM3 if part.label.startswith("WHEEL_ARCH_") else PETG_SKIN_G_CM3)
        for part in panels.children
    ]
    shell_items += [
        (part, PETG_SKIN_G_CM3) for part in panel_mount.children
        if "FRAME_WITH_BOSSES" in part.label or "WEDGE_WASHER" in part.label
    ]
    printed_frame_items = [(part, PETG_SKIN_G_CM3) for part in frame.children]
    frame_items = list(printed_frame_items)
    for group in (M.body_chassis_mount_hardware(), M.body_frame_joint_hardware(),
                  M.shell_frame_hardware()):
        frame_items += [
            (part, BRASS_G_CM3 if "NUT" in part.label or "INSERT" in part.label else STEEL_G_CM3)
            for part in group.children
        ]

    shell_props = properties(shell_items)
    printed_frame_props = properties(printed_frame_items)
    frame_props = properties(frame_items)
    yaw_parts = [*M.body_yaw_stage().children, *M.yaw_drive_moving_parts()]
    yaw_shell_clashes = {}
    for part in yaw_parts:
        intersection = shell & part
        volume = 0.0 if intersection is None else intersection.volume
        if volume > 0.001:
            yaw_shell_clashes[part.label] = volume
    register = {row[0]: row for row in M.MASS_ROWS}
    robot = M.mass_properties()
    x, y, z = robot["com_mm"]
    a_tip = 9.81 * x / z
    ball_share = x / M.BALL_CONTACT[0]
    com_cross_pitch = math.degrees(math.atan2(x, z))
    head_mass = M.HEAD_MASS_G
    head_yaw_local = M.HEAD_LOCAL_COM
    yaw_radius = math.hypot(head_yaw_local[0] - M.HEAD_LOCAL_YAW[0], head_yaw_local[1])
    head_mass_tree = json.loads((M.HEAD_DIR / "mass-placement.json").read_text())
    pitch = head_mass_tree["working"]["pitch"]
    roll = head_mass_tree["working"]["roll"]
    axes = head_mass_tree["axes"]
    pitch_offset = math.hypot(pitch["center_mm"][0] - axes["pitch_x"],
                              pitch["center_mm"][2] - axes["pitch_z"])
    roll_offset = math.hypot(roll["center_mm"][1] - axes["roll_y"],
                             roll["center_mm"][2] - axes["roll_z"])
    # Any rotation can move its mass centroid by at most twice its radius from
    # the axis. Include those small shifts in a conservative yaw/pose bound.
    pitch_roll_x_bound = (2 * pitch["mass_g"] * pitch_offset
                          + 2 * roll["mass_g"] * roll_offset) / robot["mass_g"]
    head_x_min = M.BODY_AXIS_X - yaw_radius
    yaw_x_shift = head_mass * (head_x_min - register["HEAD_V1"][2][0]) / robot["mass_g"]
    worst_pose_x = x + yaw_x_shift - pitch_roll_x_bound
    worst_pose_z = z + pitch_roll_x_bound
    worst_pose_a_tip = 9.81 * worst_pose_x / worst_pose_z
    harness_row = register["HARNESS_AND_FASTENERS"]
    harness_mass, harness_x = harness_row[1], harness_row[2][0]
    required_ratio = PHYSICS_MARGIN_A_TIP_MIN / 9.81
    harness_min_x = harness_x + robot["mass_g"] / harness_mass * (
        required_ratio * worst_pose_z - worst_pose_x)
    harness_rear_x_scenario = -20.0
    harness_rear_a_tip = 9.81 * (
        worst_pose_x + harness_mass * (harness_rear_x_scenario - harness_x) / robot["mass_g"]
    ) / worst_pose_z
    # Measure the actual chassis-v1 skid shoe at the ground datum.
    skid_shoe = M.rear_skid_tcrt_module().children[0].children[1].children[0]
    skid_angle = min(math.degrees(math.atan2(vertex.Z, -vertex.X))
                     for vertex in skid_shoe.vertices() if vertex.X < 0.0)

    def matches(name, measured):
        _, mass, centre, _ = register[name]
        return abs(mass - measured["mass_g"]) < 0.1 and all(
            abs(centre[i] - measured["com_mm"][i]) < 0.11 for i in range(3)
        )

    checks = {
        "shell_and_panels_match_mass_register": matches("BODY_SHELL_AND_PANELS", shell_props),
        "frame_and_joints_match_mass_register": matches("BODY_PRIMARY_FRAME", frame_props),
        # D-042: the +Y fan-intake grille and collar make the shell slightly asymmetric.
        "shell_symmetric_about_y": abs(shell.center().Y) < 0.5,
        "head_yaw_axis_unchanged": M.HEAD_YAW_DATUM == (16.0, 0.0, 140.0),
        "head_sweep_above_shell": M.HEAD_SWEEP_FLOOR_Z - M.BODY_Z_TOP >= 15.0,
        "yaw_stage_and_moving_parts_clear_shell": not yaw_shell_clashes,
        "mount_pattern_unchanged": set(M.BODY_MOUNT_POINTS) == {(-22.0, -48.0), (-22.0, 48.0), (64.0, -48.0), (64.0, 48.0)},
        "body_width_within_205_mm_baseline": 2 * max(station[3] for station in M.SHELL_STATIONS) <= 205.0,
        "com_between_axle_and_ball": 0.0 < x < M.BALL_CONTACT[0],
        "forward_tip_margin_screen": a_tip >= PHYSICS_MARGIN_A_TIP_MIN,
        "head_pose_tip_margin_screen": worst_pose_a_tip >= PHYSICS_MARGIN_A_TIP_MIN,
        "ball_share_above_spin_walk_flag": ball_share >= 0.09,
        "skid_contacts_before_com_crosses_axle": skid_angle < com_cross_pitch,
        "com_below_head_yaw": z < M.HEAD_YAW_DATUM[2],
    }
    payload = {
        "scope": "body-v1 source geometry and whole-robot estimated mass register; neutral head pose",
        "assumptions": {
            "petg_skin_and_frame_g_cm3": PETG_SKIN_G_CM3,
            "petg_arch_effective_g_cm3": PETG_ARCH_G_CM3,
            "steel_g_cm3": STEEL_G_CM3,
            "brass_g_cm3": BRASS_G_CM3,
            "mass_is_estimated_not_weighed": True,
        },
        "shell_and_panels": shell_props,
        "printed_frame_only": printed_frame_props,
        "frame_and_joints": frame_props,
        "whole_robot": {
            **robot,
            "forward_tip_acceleration_m_s2": a_tip,
            "forward_tip_screen_min_m_s2": PHYSICS_MARGIN_A_TIP_MIN,
            "ball_static_share": ball_share,
            "com_over_axle_pitch_deg": com_cross_pitch,
            "rear_skid_first_contact_pitch_deg": skid_angle,
            "reverse_launch_or_forward_brake_tip_acceleration_m_s2": 9.81 * (M.BALL_CONTACT[0] - x) / z,
            "axle_line_lateral_tip_proxy_m_s2": 9.81 * (M.TRACK / 2.0 - abs(y)) / z,
            "neutral_spin_centripetal_at_220_deg_s_m_s2": math.radians(220.0)**2 * x / 1000.0,
            "head_pose_conservative_tip_acceleration_m_s2": worst_pose_a_tip,
            "head_yaw_com_offset_from_axis_mm": yaw_radius,
            "head_pitch_carried_com_offset_from_axis_mm": pitch_offset,
            "head_roll_carried_com_offset_from_axis_mm": roll_offset,
            "printed_enclosure_yaw_inertia_about_drive_axis_kg_m2": (
                shell_props["yaw_inertia_about_ground_origin_g_mm2"]
                + printed_frame_props["yaw_inertia_about_ground_origin_g_mm2"]) / 1e9,
            "unweighed_harness_fastener_allowance_g": harness_mass,
            "allowance_assumed_x_mm": harness_x,
            "allowance_min_x_for_pose_screen_mm": harness_min_x,
            "allowance_if_at_x_minus20_a_tip_m_s2": harness_rear_a_tip,
        },
        "axes": {
            "head_yaw_datum_mm": M.HEAD_YAW_DATUM,
            "head_sweep_floor_z_mm": M.HEAD_SWEEP_FLOOR_Z,
            "head_sweep_to_shell_clearance_mm": M.HEAD_SWEEP_FLOOR_Z - M.BODY_Z_TOP,
            "yaw_shell_clashes_mm3": yaw_shell_clashes,
        },
        "envelope": {
            "shell_x_mm": (min(s[1] for s in M.SHELL_STATIONS), max(s[2] for s in M.SHELL_STATIONS)),
            "shell_width_max_mm": 2 * max(s[3] for s in M.SHELL_STATIONS),
            "shell_z_mm": (M.BODY_Z_BOTTOM, M.BODY_Z_TOP),
        },
        "checks": checks,
        "ok": all(checks.values()),
    }
    out = HERE / "generated" / "body-layout-checks.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"ok": payload["ok"], "checks": checks,
                      "whole_robot": payload["whole_robot"],
                      "shell_mass_g": shell_props["mass_g"],
                      "frame_mass_g": frame_props["mass_g"]}, indent=2))
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
