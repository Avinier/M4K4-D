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
    checks = [
        ("concept_a_track", M.TRACK == 170.0, {"actual_mm": M.TRACK}),
        ("wheel_geometry_mirrors_about_centerline", abs(wheel_l_y + wheel_r_y) < 1e-9, {"left_center_y_mm": wheel_l_y, "right_center_y_mm": wheel_r_y}),
        ("wheel_geometry_track_is_170", abs((wheel_l_y - wheel_r_y) - M.TRACK) < 1e-9, {"measured_track_mm": wheel_l_y - wheel_r_y}),
        ("loaded_radius_matches_axle_height", M.WHEEL_OD / 2.0 == M.AXLE_Z, {"radius_mm": M.WHEEL_OD / 2.0, "axle_z_mm": M.AXLE_Z}),
        ("wheel_well_has_radial_clearance", M.WHEEL_WELL_RADIAL_CLEARANCE >= 3.0, {"radial_clearance_mm": M.WHEEL_WELL_RADIAL_CLEARANCE}),
        ("axle_crossmember_reaches_wheel_hubs", M.AXLE_CROSSMEMBER_WIDTH / 2.0 >= M.TRACK / 2.0 - M.WHEEL_WIDTH / 2.0, {"crossmember_half_width_mm": M.AXLE_CROSSMEMBER_WIDTH / 2.0, "wheel_inner_face_y_mm": M.TRACK / 2.0 - M.WHEEL_WIDTH / 2.0}),
        ("ball_transfer_is_frozen_default", M.BALL_CONTACT == (110.0, 0.0, 0.0), {"contact_mm": M.BALL_CONTACT}),
        ("ball_mount_is_fixed_not_interchangeable", M.BALL_MOUNT_MODE == "FIXED_3HOLE_NON_INTERCHANGEABLE", {"mount_mode": M.BALL_MOUNT_MODE}),
        ("rp01_yaw_transform_closes", all(abs(transformed_yaw[i] - M.HEAD_YAW_DATUM[i]) < 1e-9 for i in range(3)), {"transformed_mm": transformed_yaw, "datum_mm": M.HEAD_YAW_DATUM}),
        ("body_fits_track_width", M.BODY_WIDTH_LOWER < M.TRACK + M.WHEEL_WIDTH, {"body_width_mm": M.BODY_WIDTH_LOWER, "wheel_stance_mm": M.TRACK + M.WHEEL_WIDTH}),
        ("body_ground_clearance_in_baseline_band", 25.0 <= M.BODY_Z_BOTTOM <= 35.0, {"body_bottom_mm": M.BODY_Z_BOTTOM, "target_mm": [25.0, 35.0]}),
        ("visible_body_height_in_baseline_band", 105.0 <= M.BODY_Z_TOP - M.BODY_Z_BOTTOM <= 115.0, {"body_height_mm": M.BODY_Z_TOP - M.BODY_Z_BOTTOM, "target_mm": [105.0, 115.0]}),
        ("neutral_stack_is_documented_304_mm", abs(M.OVERALL_PHYSICAL_HEIGHT - 304.0) < 1e-9, {"overall_height_mm": M.OVERALL_PHYSICAL_HEIGHT, "rounded_target_mm": 300.0}),
        ("neck_allocation_is_60_mm", abs(M.NECK_ALLOCATION - 60.0) < 1e-9, {"neck_allocation_mm": M.NECK_ALLOCATION}),
        ("rear_tcrt_is_only_cliff_channel", M.TCRT_CHANNELS == ("REAR",), {"channels": M.TCRT_CHANNELS}),
        ("rear_tcrt_has_contact_lookahead", M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0] >= M.TCRT_REAR_LOOKAHEAD, {"sensor_x_mm": M.TCRT_REAR_CENTER[0], "skid_contact_x_mm": M.SKID_PAD_CENTER[0], "lookahead_mm": M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0]}),
        ("rear_tcrt_optical_face_has_5mm_clearance", abs(M.TCRT_REAR_CENTER[2] - M.TCRT_PACKAGE_SIZE[2] / 2.0 - M.TCRT_OPTICAL_FACE_Z) < 1e-9, {"optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("tcrt_guard_is_lower_than_optical_face", 0.0 < M.TCRT_GUARD_BOTTOM_Z < M.TCRT_OPTICAL_FACE_Z, {"guard_bottom_z_mm": M.TCRT_GUARD_BOTTOM_Z, "optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("rear_skid_pad_is_below_connected_root", M.SKID_PAD_CENTER[2] < M.SKID_ROOT_DATUM[2] and M.SKID_PAD_CENTER[0] < M.SKID_ROOT_DATUM[0], {"root_mm": M.SKID_ROOT_DATUM, "pad_mm": M.SKID_PAD_CENTER}),
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
