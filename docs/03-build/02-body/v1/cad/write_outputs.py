"""Write body-v1 dimensional and mass-register reports from the CAD source."""

from __future__ import annotations

import json
from pathlib import Path

import body_v1_model as M


HERE = Path(__file__).resolve().parent
OUT = HERE / "generated"

# The shared mass register describes the whole robot. These are its rows that
# correspond to the body scope; the mixed harness row is deliberately omitted.
BODY_MASS_ROWS = {
    "BODY_SHELL_AND_PANELS",
    "BODY_PRIMARY_FRAME",
    "RASPBERRY_PI5_AND_COOLER",
    "PCB02_CHARGE_AND_SYSTEM_POWER",
    "PCB03_MOTOR_GATE_AND_HEAD_RAIL",
    "PCB04_BRANCH_CONVERTERS",
    "C3_DEVKITC_N8",
    "C3_CARRIER_PCB10",
    "YAW_JUNCTION_PCB08",
    "C0_LINK_ADAPTER_PCB09",
    "ESTOP_XA1E_BV3U02KT_R",
    "BODY_AUDIO",
    "BODY_YAW_STAGE",
}


def _write_json(name: str, payload: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    dimensions = {
        "layout_id": M.LAYOUT_ID,
        "layout_revision": M.LAYOUT_REV,
        "units": "mm",
        "coordinate_convention": "+X forward, +Y robot-left, +Z up; origin on ground at the drive axle",
        "body_shell_x_mm": [min(s[1] for s in M.SHELL_STATIONS), max(s[2] for s in M.SHELL_STATIONS)],
        "body_shell_z_mm": [M.BODY_Z_BOTTOM, M.BODY_Z_TOP],
        "body_width_lower_upper_mm": [2 * M.SHELL_STATIONS[0][3], 2 * M.SHELL_STATIONS[-1][3]],
        "body_width_shoulder_z42_mm": 2 * M.SHELL_STATIONS[1][3],
        "body_width_max_mm": 2 * max(s[3] for s in M.SHELL_STATIONS),
        "body_shell_stations_z_rear_front_halfwidth_mm": [list(s) for s in M.SHELL_STATIONS],
        "shell_thickness_mm": M.SHELL_THICKNESS,
        "body_mount_points_xy_mm": [list(point) for point in M.BODY_MOUNT_POINTS],
        "body_locating_points_xy_mm": [list(point) for point in M.BODY_LOCATING_POINTS],
        "panel_overlap_mm": M.PANEL_OVERLAP,
        "front_panel_width_bottom_top_mm": [M.FRONT_PANEL_BOTTOM_WIDTH, M.FRONT_PANEL_TOP_WIDTH],
        "rear_panel_width_bottom_top_mm": [M.REAR_PANEL_BOTTOM_WIDTH, M.REAR_PANEL_TOP_WIDTH],
        "front_panel_fasteners_yz_mm": [list(point) for point in M.FRONT_PANEL_FASTENERS],
        "rear_panel_fasteners_yz_mm": [list(point) for point in M.REAR_PANEL_FASTENERS],
        "speaker_center_mm": list(M.SPEAKER_CENTER),
        "speaker_basket_diameter_mm": M.SPEAKER_BASKET_DIAMETER,
        "microphone_ports": [
            {"center_mm": list(port[:3]), "name": port[3]}
            for port in M.MICROPHONE_PORTS
        ],
        "compute_center_mm": list(M.PI_CENTER),
        "pi_cooler_headroom_mm": M.PI_COOLER_HEADROOM,
        "head_yaw_datum_mm": list(M.HEAD_YAW_DATUM),
        "yaw_bearing_radii_mm": list(M.YAW_BEARING_RADII),
        "yaw_bearing_z_mm": list(M.YAW_BEARING_Z),
        "yaw_servo_envelope_mm": list(M.YAW_SERVO_ENVELOPE),
        "yaw_disc_top_z_mm": M.YAW_DISC_TOP_Z,
        "head_sweep_floor_z_mm": M.HEAD_SWEEP_FLOOR_Z,
    }
    _write_json("dimensions.json", dimensions)
    _write_json("frames.json", {
        key: list(value) for key, value in M.FRAMES.items()
        if key in {"F_GROUND", "F_BODY_BASE", "F_HEAD_YAW", "F_COMPUTE_TRAY"}
    })

    rows = [row for row in M.MASS_ROWS if row[0] in BODY_MASS_ROWS]
    mass = sum(row[1] for row in rows)
    com = [sum(row[1] * row[2][axis] for row in rows) / mass for axis in range(3)]
    robot = M.mass_properties()
    _write_json("mass-properties.json", {
        "scope": "body register rows only; partial estimate, not a full body mass or solid measurement",
        "mass_g": mass,
        "com_mm": com,
        "whole_robot_estimate": {
            **robot,
            "forward_tip_acceleration_m_s2": 9.81 * robot["com_mm"][0] / robot["com_mm"][2],
            "ball_static_share": robot["com_mm"][0] / M.BALL_CONTACT[0],
        },
        "rows": [
            {"id": name, "mass_g": row_mass, "com_mm": list(row_com), "source": source}
            for name, row_mass, row_com, source in rows
        ],
        "exclusions": "Head, chassis, battery, drive, deck sensors, and mixed HARNESS_AND_FASTENERS row",
    })

    (OUT / "dimensions.md").write_text(
        "# Body v1 dimensions\n\n"
        f"- Shell: X {dimensions['body_shell_x_mm'][0]:.1f}…{dimensions['body_shell_x_mm'][1]:.1f} mm; "
        f"Z {M.BODY_Z_BOTTOM:.1f}…{M.BODY_Z_TOP:.1f} mm.\n"
        f"- Bottom / roof width: {dimensions['body_width_lower_upper_mm'][0]:.1f} / {dimensions['body_width_lower_upper_mm'][1]:.1f} mm; "
        f"Z 42 shoulder width {dimensions['body_width_shoulder_z42_mm']:.1f} mm; "
        f"maximum belly width {dimensions['body_width_max_mm']:.1f} mm.\n"
        f"- Shell wall: {M.SHELL_THICKNESS:.1f} mm.\n"
        f"- Chassis interface: {len(M.BODY_MOUNT_POINTS)} M4 mounting points and "
        f"{len(M.BODY_LOCATING_POINTS)} locating points.\n"
        f"- Service panels: {len(M.FRONT_PANEL_FASTENERS)} front and "
        f"{len(M.REAR_PANEL_FASTENERS)} rear fasteners; {M.PANEL_OVERLAP:.1f} mm overlap.\n"
        f"- Head yaw datum: {M.HEAD_YAW_DATUM} mm.\n\n"
        "Generated from `body_v1_model.py`; edit the source, then rerun `write_outputs.py`.\n"
    )
    (OUT / "mass-properties.md").write_text(
        "# Body v1 mass register subset\n\n"
        f"- Listed body rows: {mass:.1f} g.\n"
        f"- Listed-row CoM: X={com[0]:.1f}, Y={com[1]:.1f}, Z={com[2]:.1f} mm.\n\n"
        f"- Whole-robot register: {robot['mass_g']:.1f} g; CoM X={robot['com_mm'][0]:.2f}, "
        f"Y={robot['com_mm'][1]:.2f}, Z={robot['com_mm'][2]:.2f} mm; "
        f"neutral a_tip={9.81 * robot['com_mm'][0] / robot['com_mm'][2]:.3f} m/s².\n\n"
        "This is a partial estimate from the shared whole-robot register. It excludes the "
        "head, chassis, battery, drive and deck sensors, plus the mixed harness/fastener row. "
        "It is not a measured body mass or a complete assembly mass.\n"
    )


if __name__ == "__main__":
    main()
