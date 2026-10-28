"""Deterministic source-level checks for RP-03 integrated Layout 01."""

from __future__ import annotations

import json
from pathlib import Path

import body_chassis_model as M


HERE = Path(__file__).resolve().parent


def main():
    transformed_yaw = tuple(
        M.HEAD_ORIGIN_IN_CHASSIS[index] + M.HEAD_LOCAL_YAW[index]
        for index in range(3)
    )
    wheel_l_y = tuple(M.wheel_assembly("L").children[0].bounding_box().center())[1]
    wheel_r_y = tuple(M.wheel_assembly("R").children[0].bounding_box().center())[1]
    rear_tail = M.rear_skid_tcrt_module()
    tail_shell, tail_internals, tail_floor, tail_cap = rear_tail.children
    tail_spine, tail_cartridge, tail_cable = tail_internals.children
    tail_shoe, tail_guard_l, tail_guard_r = tail_floor.children
    tail_sensor_package = tail_cartridge.children[0]
    rear_crossmember = M._box(16.0, 116.0, 14.0, (-56.0, 0.0, 41.0), "CHECK_REAR_CROSSMEMBER", M.FRAME_BLUE)
    tail_root_overlap = (tail_shell & rear_crossmember).volume
    tail_shoe_overlap = (tail_shell & tail_shoe).volume
    tail_cap_overlap = (tail_shell & tail_cap).volume
    tail_guard_overlaps = [(tail_shell & guard).volume for guard in (tail_guard_l, tail_guard_r)]
    tail_sensor_shell_collision = (tail_shell & tail_sensor_package).volume
    tail_spine_root_overlap = (tail_spine & rear_crossmember).volume
    top_level_labels = [child.label for child in M.build_assembly().children]
    terminal_link_lengths = [
        abs(M.REAR_TAIL_STATIONS[index][0] - M.REAR_TAIL_STATIONS[index - 1][0])
        for index in range(len(M.REAR_TAIL_STATIONS) - 2, len(M.REAR_TAIL_STATIONS))
    ]
    checks = [
        ("concept_a_track", M.TRACK == 170.0, {"actual_mm": M.TRACK}),
        ("wheel_geometry_mirrors_about_centerline", abs(wheel_l_y + wheel_r_y) < 1e-9, {"left_center_y_mm": wheel_l_y, "right_center_y_mm": wheel_r_y}),
        ("wheel_geometry_track_is_170", abs((wheel_l_y - wheel_r_y) - M.TRACK) < 1e-9, {"measured_track_mm": wheel_l_y - wheel_r_y}),
        ("loaded_radius_matches_axle_height", M.WHEEL_OD / 2.0 == M.AXLE_Z, {"radius_mm": M.WHEEL_OD / 2.0, "axle_z_mm": M.AXLE_Z}),
        ("wheel_well_has_radial_clearance", M.WHEEL_WELL_RADIAL_CLEARANCE >= 3.0, {"radial_clearance_mm": M.WHEEL_WELL_RADIAL_CLEARANCE}),
        ("axle_crossmember_reaches_wheel_hubs", M.AXLE_CROSSMEMBER_WIDTH / 2.0 >= M.TRACK / 2.0 - M.WHEEL_WIDTH / 2.0, {"crossmember_half_width_mm": M.AXLE_CROSSMEMBER_WIDTH / 2.0, "wheel_inner_face_y_mm": M.TRACK / 2.0 - M.WHEEL_WIDTH / 2.0}),
        ("ball_transfer_is_frozen_default", M.BALL_CONTACT == (110.0, 0.0, 0.0), {"contact_mm": M.BALL_CONTACT}),
        ("ball_mount_is_fixed_not_interchangeable", M.BALL_MOUNT_MODE == "FIXED_3HOLE_NON_INTERCHANGEABLE", {"mount_mode": M.BALL_MOUNT_MODE}),
        ("ball_flange_seats_on_load_collar", abs(M.BALL_COLLAR_Z0 + M.BALL_COLLAR_HEIGHT - M.BALL_NATIVE_HEIGHT) < 1e-9, {"collar_top_z_mm": M.BALL_COLLAR_Z0 + M.BALL_COLLAR_HEIGHT, "flange_bottom_z_mm": M.BALL_NATIVE_HEIGHT}),
        ("ball_housing_clears_load_collar", M.BALL_COLLAR_BORE_RADIUS > M.BALL_HOUSING_WIDTH / 2.0, {"collar_bore_radius_mm": M.BALL_COLLAR_BORE_RADIUS, "housing_radius_mm": M.BALL_HOUSING_WIDTH / 2.0}),
        ("nose_rails_land_in_collar_wall", M.BALL_COLLAR_BORE_RADIUS < M.BALL_RAIL_OFFSET_Y < M.BALL_COLLAR_OUTER_RADIUS, {"rail_offset_y_mm": M.BALL_RAIL_OFFSET_Y, "collar_wall_mm": [M.BALL_COLLAR_BORE_RADIUS, M.BALL_COLLAR_OUTER_RADIUS]}),
        ("rp01_yaw_transform_closes", all(abs(transformed_yaw[i] - M.HEAD_YAW_DATUM[i]) < 1e-9 for i in range(3)), {"transformed_mm": transformed_yaw, "datum_mm": M.HEAD_YAW_DATUM}),
        ("body_fits_track_width", M.BODY_WIDTH_LOWER < M.TRACK + M.WHEEL_WIDTH, {"body_width_mm": M.BODY_WIDTH_LOWER, "wheel_stance_mm": M.TRACK + M.WHEEL_WIDTH}),
        ("body_ground_clearance_in_baseline_band", 25.0 <= M.BODY_Z_BOTTOM <= 35.0, {"body_bottom_mm": M.BODY_Z_BOTTOM, "target_mm": [25.0, 35.0]}),
        ("visible_body_height_in_baseline_band", 105.0 <= M.BODY_Z_TOP - M.BODY_Z_BOTTOM <= 115.0, {"body_height_mm": M.BODY_Z_TOP - M.BODY_Z_BOTTOM, "target_mm": [105.0, 115.0]}),
        ("neutral_stack_is_documented_304_mm", abs(M.OVERALL_PHYSICAL_HEIGHT - 304.0) < 1e-9, {"overall_height_mm": M.OVERALL_PHYSICAL_HEIGHT, "rounded_target_mm": 300.0}),
        ("neck_allocation_is_60_mm", abs(M.NECK_ALLOCATION - 60.0) < 1e-9, {"neck_allocation_mm": M.NECK_ALLOCATION}),
        ("rear_tcrt_is_only_cliff_channel", M.TCRT_CHANNELS == ("REAR",), {"channels": M.TCRT_CHANNELS}),
        ("rear_tcrt_has_contact_lookahead", M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0] >= M.TCRT_REAR_LOOKAHEAD, {"sensor_x_mm": M.TCRT_REAR_CENTER[0], "skid_contact_x_mm": M.SKID_PAD_CENTER[0], "lookahead_mm": M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0]}),
        ("rear_tcrt_optical_face_matches_raised_datum", abs(M.TCRT_REAR_CENTER[2] - M.TCRT_PACKAGE_SIZE[2] / 2.0 - M.TCRT_OPTICAL_FACE_Z) < 1e-9 and M.TCRT_OPTICAL_FACE_Z == 10.0, {"optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("rear_tcrt_lookahead_remains_bounded", 25.0 <= M.TCRT_REAR_LOOKAHEAD <= 30.0, {"lookahead_mm": M.TCRT_REAR_LOOKAHEAD}),
        ("tcrt_guard_is_lower_than_optical_face", 0.0 < M.TCRT_GUARD_BOTTOM_Z < M.TCRT_OPTICAL_FACE_Z, {"guard_bottom_z_mm": M.TCRT_GUARD_BOTTOM_Z, "optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("rear_skid_is_first_sacrificial_contact", M.SKID_SHOE_BOTTOM_Z < M.TCRT_GUARD_BOTTOM_Z, {"skid_bottom_z_mm": M.SKID_SHOE_BOTTOM_Z, "sensor_guard_bottom_z_mm": M.TCRT_GUARD_BOTTOM_Z}),
        ("rear_skid_pad_is_below_connected_root", M.SKID_PAD_CENTER[2] < M.SKID_ROOT_DATUM[2] and M.SKID_PAD_CENTER[0] < M.SKID_ROOT_DATUM[0], {"root_mm": M.SKID_ROOT_DATUM, "pad_mm": M.SKID_PAD_CENTER}),
        ("rear_tail_is_multi_link_faceted_arc", M.REAR_TAIL_STYLE == "MULTI_LINK_FACETED_ARC" and len(M.REAR_TAIL_STATIONS) >= 10, {"style": M.REAR_TAIL_STYLE, "station_count": len(M.REAR_TAIL_STATIONS)}),
        ("rear_tail_terminal_links_are_short", max(terminal_link_lengths) <= 7.0, {"terminal_link_lengths_mm": terminal_link_lengths}),
        ("rear_tail_tip_is_pointed", M.REAR_TAIL_STATIONS[-1][1] <= 2.0 and M.REAR_TAIL_STATIONS[-1][3] - M.REAR_TAIL_STATIONS[-1][2] <= 4.0, {"tip_half_width_mm": M.REAR_TAIL_STATIONS[-1][1], "tip_height_mm": M.REAR_TAIL_STATIONS[-1][3] - M.REAR_TAIL_STATIONS[-1][2]}),
        ("rear_tail_uses_head_ivory", M.REAR_TAIL_VISIBLE_COLOR == M.IVORY, {"tail_color": M.REAR_TAIL_VISIBLE_COLOR, "head_palette_ivory": M.IVORY}),
        ("rear_tail_shell_is_translucent", 0.0 < M.REAR_TAIL_SHELL_ALPHA < 0.5, {"shell_alpha": M.REAR_TAIL_SHELL_ALPHA}),
        ("rear_tail_has_hollow_wall_definition", 1.5 <= M.REAR_TAIL_WALL <= 3.0 and len(M.REAR_TAIL_INNER_STATIONS) >= 8, {"wall_mm": M.REAR_TAIL_WALL, "inner_station_count": len(M.REAR_TAIL_INNER_STATIONS)}),
        ("rear_skid_tcrt_is_separate_top_level_group", "REAR_SKID_TCRT_MODULE" in top_level_labels, {"top_level_labels": top_level_labels}),
        ("rear_tail_root_overlaps_crossmember", tail_root_overlap > 0.0, {"overlap_volume_mm3": tail_root_overlap}),
        ("rear_tail_spine_enters_crossmember", tail_spine_root_overlap > 0.0, {"overlap_volume_mm3": tail_spine_root_overlap}),
        ("rear_tail_shoe_is_attached", tail_shoe_overlap > 0.0, {"overlap_volume_mm3": tail_shoe_overlap}),
        ("rear_tail_guards_are_attached", all(value > 0.0 for value in tail_guard_overlaps), {"overlap_volumes_mm3": tail_guard_overlaps}),
        ("rear_tail_cap_is_attached", tail_cap_overlap > 0.0, {"overlap_volume_mm3": tail_cap_overlap}),
        ("rear_tcrt_package_clears_shell", tail_sensor_shell_collision < 1e-6, {"collision_volume_mm3": tail_sensor_shell_collision}),
        ("rear_tail_tip_is_upturned", sum(M.REAR_TAIL_STATIONS[-1][2:4]) / 2.0 > sum(M.REAR_TAIL_STATIONS[-2][2:4]) / 2.0, {"sensor_station_center_z_mm": sum(M.REAR_TAIL_STATIONS[-2][2:4]) / 2.0, "tip_center_z_mm": sum(M.REAR_TAIL_STATIONS[-1][2:4]) / 2.0}),
        ("rear_tail_cap_is_flush", abs(M.REAR_TAIL_CAP_TOP_Z - M.REAR_TAIL_STATIONS[6][3]) < 1e-9, {"cap_top_z_mm": M.REAR_TAIL_CAP_TOP_Z, "sensor_station_top_z_mm": M.REAR_TAIL_STATIONS[6][3]}),
        ("tactile_nose_precedes_ball_surface", M.TACTILE_NOSE_FACE_X > M.BALL_CONTACT[0] + M.BALL_DIAMETER / 2.0, {"tactile_face_x_mm": M.TACTILE_NOSE_FACE_X, "ball_front_x_mm": M.BALL_CONTACT[0] + M.BALL_DIAMETER / 2.0}),
        ("tactile_nose_has_bounded_travel", 2.0 <= M.TACTILE_NOSE_TRAVEL <= 4.0, {"travel_mm": M.TACTILE_NOSE_TRAVEL}),
        ("battery_forward_of_axle", M.BATTERY_CENTER[0] > 0.0, {"battery_x_mm": M.BATTERY_CENTER[0]}),
        ("head_source_exists", (M.HEAD_DIR / "layout_model.py").exists(), {"path": str(M.HEAD_DIR / "layout_model.py")}),
        ("pi_step_exists", (M.PURCHASED / "raspberry_pi_5.step").exists(), {"path": str(M.PURCHASED / "raspberry_pi_5.step")}),
        ("bearing_step_exists", (M.PURCHASED / "bearing_608zz.step").exists(), {"path": str(M.PURCHASED / "bearing_608zz.step")}),
        ("com_inside_support_x", 0.0 < M.mass_properties()["com_mm"][0] < M.BALL_CONTACT[0], {"com_x_mm": M.mass_properties()["com_mm"][0]}),
        ("com_below_head_yaw", M.mass_properties()["com_mm"][2] < M.HEAD_YAW_DATUM[2], {"com_z_mm": M.mass_properties()["com_mm"][2]}),
    ]
    payload = {
        "layout_id": M.LAYOUT_ID,
        "ok": all(row[1] for row in checks),
        "checks": [{"name": name, "ok": ok, "evidence": evidence} for name, ok, evidence in checks],
    }
    out = HERE / "generated"
    out.mkdir(parents=True, exist_ok=True)
    (out / "checks.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = ["# RP-03 Layout 01 deterministic checks", ""]
    lines.extend(f"- [{'x' if ok else ' '}] `{name}` — {evidence}" for name, ok, evidence in checks)
    (out / "checks.md").write_text("\n".join(lines) + "\n")
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
