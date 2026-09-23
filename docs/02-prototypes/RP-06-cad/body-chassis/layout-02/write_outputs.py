"""Write generated dimensional, frame, and mass-property reports."""

from __future__ import annotations

import json
from pathlib import Path

import body_chassis_model as M


HERE = Path(__file__).resolve().parent
OUT = HERE / "generated"


def write_json(name, payload):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(payload, indent=2) + "\n")


def main():
    dims = {
        "layout_id": M.LAYOUT_ID,
        "layout_revision": M.LAYOUT_REV,
        "units": "mm",
        "coordinate_convention": "+X forward, +Y robot-left, +Z up; origin at axle ground-contact line",
        "wheel_track_mm": M.TRACK,
        "wheel_od_mm": M.WHEEL_OD,
        "wheel_width_mm": M.WHEEL_WIDTH,
        "axle_height_mm": M.AXLE_Z,
        "front_ball_contact_mm": list(M.BALL_CONTACT),
        "ball_mount_mode": M.BALL_MOUNT_MODE,
        "body_shell_x_mm": [M.BODY_X_REAR, M.BODY_X_FRONT],
        "body_shell_z_mm": [M.BODY_Z_BOTTOM, M.BODY_Z_TOP],
        "body_visible_height_mm": M.BODY_Z_TOP - M.BODY_Z_BOTTOM,
        "body_width_lower_mm": M.BODY_WIDTH_LOWER,
        "body_width_upper_mm": M.BODY_WIDTH_UPPER,
        "shell_thickness_mm": M.SHELL_THICKNESS,
        "body_mount_points_mm": [list(point) for point in M.BODY_MOUNT_POINTS],
        "body_locating_points_mm": [list(point) for point in M.BODY_LOCATING_POINTS],
        "body_mount_fastener": "M4 through-bolt, four places",
        "panel_overlap_mm": M.PANEL_OVERLAP,
        "front_panel_width_bottom_top_mm": [M.FRONT_PANEL_BOTTOM_WIDTH, M.FRONT_PANEL_TOP_WIDTH],
        "rear_panel_width_bottom_top_mm": [M.REAR_PANEL_BOTTOM_WIDTH, M.REAR_PANEL_TOP_WIDTH],
        "panel_edge_intent": "front and rear panel side edges are parallel to their corresponding shell end-profile side edges",
        "front_panel_fasteners_mm": [list(point) for point in M.FRONT_PANEL_FASTENERS],
        "rear_panel_fasteners_mm": [list(point) for point in M.REAR_PANEL_FASTENERS],
        "speaker_center_mm": list(M.SPEAKER_CENTER),
        "speaker_basket_diameter_mm": M.SPEAKER_BASKET_DIAMETER,
        "speaker_cone_diameter_mm": M.SPEAKER_CONE_DIAMETER,
        "microphone_ports": [list(port) for port in M.MICROPHONE_PORTS],
        "audio_status": "provisional requirement envelopes pending RP-05/RP-06 part selection",
        "head_yaw_datum_mm": list(M.HEAD_YAW_DATUM),
        "head_origin_in_chassis_mm": list(M.HEAD_ORIGIN_IN_CHASSIS),
        "head_local_yaw_mm": list(M.HEAD_LOCAL_YAW),
        "neck_allocation_mm": M.NECK_ALLOCATION,
        "neutral_overall_physical_height_mm": M.OVERALL_PHYSICAL_HEIGHT,
        "overall_height_status": f"{M.OVERALL_PHYSICAL_HEIGHT:.0f} mm neutral stack (Layout 04 head, 49.5 mm neck to the body top; was 304 mm)",
        "head_motion_envelope": "RP-01 Layout 04 motion-envelope.json: usable roll ±18 / pitch −22…+40, hard stops roll ±21 / pitch −25…+43; stops alone keep ≥4 mm to the yaw disc (≥2 mm at 1° overtravel)",
        "yaw_drive": "XC330-M181 through a 1:1 spur pair",
        "yaw_disc_top_z_mm": M.YAW_DISC_TOP_Z,
        "pi_cooler_headroom_mm": M.PI_COOLER_HEADROOM,
        "head_sweep_floor_z_mm": M.HEAD_SWEEP_FLOOR_Z,
        "rp01_yoke_status": "live Layout 04 straight legs on a flush yaw turntable; body-side bearing, ring gear, pinion and servo are packaging envelopes; not load-rated or fabrication-final",
        "tcrt_channels": list(M.TCRT_CHANNELS),
        "tcrt_rear_center_mm": list(M.TCRT_REAR_CENTER),
        "tcrt_optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z,
        "tcrt_guard_bottom_z_mm": M.TCRT_GUARD_BOTTOM_Z,
        "tcrt_rear_contact_lookahead_mm": M.TCRT_REAR_LOOKAHEAD,
        "tcrt_coverage_note": "CAD-context choice: rear-only cliff channel; no front or lateral cliff-safety claim",
        "rear_tail_status": "enabled" if M.REAR_TAIL_ENABLED else "parked accessory; geometry defined but excluded from the assembly",
        "rear_keel_color_alpha": [M.REAR_KEEL_COLOR, M.REAR_KEEL_ALPHA],
        "rear_tail_style": M.REAR_TAIL_STYLE,
        "rear_tail_visible_color": M.REAR_TAIL_VISIBLE_COLOR,
        "rear_tail_hub_color": M.REAR_TAIL_HUB_COLOR,
        "rear_tail_tip_color": M.REAR_TAIL_TIP_COLOR,
        "rear_tail_group": "REAR_SKID_TCRT_MODULE/REAR_TAIL_STINGER",
        "rear_tail_joints_x_z_width_height_mm": [list(joint) for joint in M.REAR_TAIL_JOINTS],
        "rear_tail_tip_mm": [M.REAR_TAIL_TIP[0], 0.0, M.REAR_TAIL_TIP[1]],
        "rear_tail_tip_section_w_h_mm": list(M.REAR_TAIL_TIP_SECTION),
        "rear_tail_root_screws_y_z_mm": [list(point) for point in M.REAR_TAIL_ROOT_SCREWS],
        "rear_tail_role": "cosmetic, static; four M3 screws driven from inside the rear panel into heat-set inserts in the hub",
        "rear_keel_group": "REAR_SKID_TCRT_MODULE/REAR_SKID_TCRT_KEEL",
        "rear_keel_stations_mm": [list(station) for station in M.REAR_KEEL_STATIONS],
        "rear_keel_mount": "four M3 screws up into REAR_SKID_CROSSMEMBER underside",
        "skid_pad_center_mm": list(M.SKID_PAD_CENTER),
    }
    write_json("dimensions.json", dims)
    write_json("frames.json", M.FRAMES)

    props = M.mass_properties()
    mass_payload = {
        "layout_id": M.LAYOUT_ID,
        "mass_g": props["mass_g"],
        "com_mm": list(props["com_mm"]),
        "rows": [
            {"id": row[0], "mass_g": row[1], "com_mm": list(row[2]), "source": row[3]}
            for row in M.MASS_ROWS
        ],
        "warning": "Estimated/custom masses require measured replacement before release.",
    }
    write_json("mass-properties.json", mass_payload)

    dimensions_md = [
        "# RP-03 Layout 02 generated dimensions",
        "",
        f"- Layout: `{M.LAYOUT_ID}` / `{M.LAYOUT_REV}`",
        f"- Wheel track: {M.TRACK:.1f} mm",
        f"- Wheel: {M.WHEEL_OD:.1f} × {M.WHEEL_WIDTH:.1f} mm",
        f"- Axle height: {M.AXLE_Z:.1f} mm",
        f"- Ball contact: `{M.BALL_CONTACT}` mm",
        f"- Ball mount: `{M.BALL_MOUNT_MODE}`",
        f"- Body shell: X {M.BODY_X_REAR:.1f}…{M.BODY_X_FRONT:.1f} mm; Z {M.BODY_Z_BOTTOM:.1f}…{M.BODY_Z_TOP:.1f} mm",
        f"- Visible body height: {M.BODY_Z_TOP - M.BODY_Z_BOTTOM:.1f} mm",
        f"- Body width: {M.BODY_WIDTH_LOWER:.1f} mm lower / {M.BODY_WIDTH_UPPER:.1f} mm upper",
        f"- Body/chassis interface: four M4 through-bolts at `{M.BODY_MOUNT_POINTS}` plus locating pins at `{M.BODY_LOCATING_POINTS}`",
        f"- Service-panel overlap: {M.PANEL_OVERLAP:.1f} mm; four M3 fasteners per panel",
        f"- Front panel widths: {M.FRONT_PANEL_BOTTOM_WIDTH:.2f} mm bottom / {M.FRONT_PANEL_TOP_WIDTH:.2f} mm top; sides parallel to front shell",
        f"- Rear panel widths: {M.REAR_PANEL_BOTTOM_WIDTH:.2f} mm bottom / {M.REAR_PANEL_TOP_WIDTH:.2f} mm top; sides parallel to rear shell",
        f"- Speaker: center `{M.SPEAKER_CENTER}` mm, {M.SPEAKER_CONE_DIAMETER:.1f} mm cone / {M.SPEAKER_BASKET_DIAMETER:.1f} mm basket",
        f"- Body microphones: four provisional PDM ports at `{M.MICROPHONE_PORTS}`",
        f"- Head-yaw datum: `{M.HEAD_YAW_DATUM}` mm",
        f"- RP-01 head origin in chassis: `{M.HEAD_ORIGIN_IN_CHASSIS}` mm",
        f"- Neutral physical height stack: {M.OVERALL_PHYSICAL_HEIGHT:.1f} mm ({M.NECK_ALLOCATION:.0f} mm neck; yaw disc top Z {M.YAW_DISC_TOP_Z:.1f}, {M.YAW_DISC_TOP_Z - M.BODY_Z_TOP:.1f} mm proud)",
        f"- Head sweep floor at the hard stops: Z {M.HEAD_SWEEP_FLOOR_Z:.1f} mm, {M.HEAD_SWEEP_FLOOR_Z - M.YAW_DISC_TOP_Z:.0f} mm above the yaw disc; Pi cooler headroom {M.PI_COOLER_HEADROOM:g} mm",
        f"- RP-01 yaw-yoke status: live Layout 04 turntable geometry; not load-rated or fabrication-final",
        f"- TCRT channels: `{M.TCRT_CHANNELS}`; rear center `{M.TCRT_REAR_CENTER}` mm",
        f"- TCRT optical face / sacrificial guard bottom: {M.TCRT_OPTICAL_FACE_Z:.1f} / {M.TCRT_GUARD_BOTTOM_Z:.1f} mm above ground",
        f"- Rear contact lookahead: {M.TCRT_REAR_LOOKAHEAD:.1f} mm",
        f"- Rear tail status: {'enabled' if M.REAR_TAIL_ENABLED else 'parked accessory, excluded from the assembly'}",
        f"- Rear keel finish: translucent `{M.REAR_KEEL_COLOR}` alpha {M.REAR_KEEL_ALPHA}",
        f"- Rear tail (when enabled): `{M.REAR_TAIL_STYLE}`, `{M.REAR_TAIL_HUB_COLOR}` root hub + {len(M.REAR_TAIL_JOINTS) - 1} telescoping `{M.REAR_TAIL_VISIBLE_COLOR}` segments + `{M.REAR_TAIL_TIP_COLOR}` chisel tip; cosmetic, panel-mounted with hidden M3 screws",
        f"- Rear tail hub face / tip: X={M.REAR_TAIL_ROOT_FACE_X:.1f} Z={M.REAR_TAIL_ROOT_Z:.1f}; tip X={M.REAR_TAIL_TIP[0]:.1f} Z={M.REAR_TAIL_TIP[1]:.1f} mm; tip section {M.REAR_TAIL_TIP_SECTION[0]:.1f} × {M.REAR_TAIL_TIP_SECTION[1]:.1f} mm",
        f"- Skid/TCRT keel: under `REAR_SKID_CROSSMEMBER`, X {M.REAR_KEEL_STATIONS[-1][0]:.1f} to {M.REAR_KEEL_STATIONS[0][0]:.1f} mm; skid pad center `{M.SKID_PAD_CENTER}` mm",
        "- Coverage: rear-only CAD-context choice; no front or lateral cliff-safety claim",
        "",
        "Generated from `body_chassis_model.py`; do not edit manually.",
    ]
    (OUT / "dimensions.md").write_text("\n".join(dimensions_md) + "\n")

    mass_md = [
        "# RP-03 Layout 02 generated mass properties",
        "",
        f"- Total modeled mass: {props['mass_g']:.1f} g",
        f"- Whole-robot CoM: X={props['com_mm'][0]:.2f}, Y={props['com_mm'][1]:.2f}, Z={props['com_mm'][2]:.2f} mm",
        "",
        "| Item | Mass (g) | CoM (mm) | Source |",
        "|---|---:|---|---|",
    ]
    for item, mass, com, source in M.MASS_ROWS:
        mass_md.append(f"| `{item}` | {mass:.2f} | ({com[0]:.2f}, {com[1]:.2f}, {com[2]:.2f}) | {source} |")
    mass_md.extend(["", "Estimated/custom masses must be replaced by measurements before release."])
    (OUT / "mass-properties.md").write_text("\n".join(mass_md) + "\n")


if __name__ == "__main__":
    main()
