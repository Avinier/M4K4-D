#!/usr/bin/env python3
"""Write generated dimensions, frames, mass, physics, U-register, connectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib import params as P
from lib.frames import frames
from lib.mass import drive_kinematics, mass_rows, physics

GEN = ROOT / "generated"
GEN.mkdir(exist_ok=True)


def dump(name, obj):
    path = GEN / name
    path.write_text(json.dumps(obj, indent=2) + "\n")
    return path


def main():
    ball_fr = {k: v for k, v in frames("ball").items() if k.startswith("F_")}
    cas_fr = {k: v for k, v in frames("caster").items() if k.startswith("F_")}
    rows_b = mass_rows("ball")
    rows_c = mass_rows("caster")
    phys_b = physics(rows_b, "ball")
    phys_c = physics(rows_c, "caster")
    kin = drive_kinematics()

    dims = {
        "layout": P.LAYOUT_ID,
        "rev": P.LAYOUT_REV,
        "sku_frozen": P.SKU_FROZEN,
        "wheel_family_displayed": P.WHEEL_FAMILY_DISPLAYED,
        "h_axle_mm": P.H_AXLE,
        "track_mm": P.TRACK,
        "loaded_radius_mm": P.LOADED_RADIUS,
        "loaded_radius_note": "Assumed equal to h_axle. Squash is U and gates the shim.",
        "front_contact_x_mm": P.FRONT_CONTACT_X,
        "front_contact_band_mm": [P.FRONT_CONTACT_X_MIN, P.FRONT_CONTACT_X_MAX],
        "ball_native_h_mm": P.BALL_NATIVE_H,
        "caster_native_h_mm": P.CASTER_NATIVE_H,
        "ball_shim_mm": P.BALL_SHIM,
        "caster_shim_mm": P.CASTER_SHIM,
        "shim_band_mm": [P.SHIM_MIN, P.SHIM_MAX],
        "contact_x_ball_equals_caster": ball_fr["F_FRONT_CONTACT"][0] == cas_fr["F_FRONT_CONTACT"][0],
        "skid_reach_mm": P.SKID_REACH,
        "skid_height_mm": P.SKID_HEIGHT,
        "skid_reach_band_mm": [P.SKID_REACH_MIN, P.SKID_REACH_MAX],
        "skid_height_band_mm": [P.SKID_H_MIN, P.SKID_H_MAX],
        "wheel_families": {
            "A": {"od": P.WHEEL_A_OD, "width": P.WHEEL_A_W, "mass": P.WHEEL_A_MASS, "composed": False},
            "B": {"od": P.WHEEL_B_OD, "width": P.WHEEL_B_W, "mass": P.WHEEL_B_MASS, "composed": False},
            "C": {"od": P.WHEEL_C_OD, "width": P.WHEEL_C_W, "mass": P.WHEEL_C_MASS, "composed": True},
        },
        "con14_mm": {"h": P.CON14_H, "w": P.CON14_W, "d": P.CON14_D},
        "ground_clearance_band_mm": [P.GROUND_CLEARANCE_MIN, P.GROUND_CLEARANCE_MAX],
        "f_neck_mm": list(P.F_NECK),
        "head_origin_in_chassis_mm": list(P.HEAD_ORIGIN_IN_CHASSIS),
        "head_import_rotation": "identity",
        "motor_stall_conflict": {
            "oz_aslong_mA_Nm": list(P.MOTOR_STALL_OZ),
            "nfp_mA_Nm": list(P.MOTOR_STALL_NFP),
            "averaged": False,
        },
        "caster_trail_display_mm_U": P.CASTER_TRAIL_DISPLAY,
        "gp2y_oa_from_body_L_mm": P.IR_OA_FROM_LEFT,
        "gp2y_oa_side_mm": P.IR_OA_SIDE,
    }
    dump("dimensions.json", dims)
    dump("frames.json", {"ball": ball_fr, "caster": cas_fr})
    dump("mass-register.json", {"ball": rows_b, "caster": rows_c})
    dump("physics.json", {"ball": phys_b, "caster": phys_c, "kinematics": kin})

    u_items = [
        ["India 6 V ~176 RPM encoder SKU", "bench reference unit"],
        ["D-shaft vs round on bought wheel", "hub print"],
        ["Caster trail millimetres", "flutter / BM-07"],
        ["Ball C_rr and laminate dent", "D21 iterate-to-caster"],
        ["Gearbox radial rating", "whether 608s are mandatory"],
        ["SPI IMU module outline", "base keep-out"],
        ["GP2Y optical-axis as a single ray", "look-ahead from contact; lens-centre D adopted"],
        ["Loaded wheel radius squash", "shim stack vs 42 mm"],
        ["DevKitC USB-plug stick-out and mass", "service keep-out"],
        ["Ø84 skate hub/spoke 2D", "family C envelope only"],
    ]
    (GEN / "u-register.md").write_text(
        "# Open U register — pass 1 must not close these\n\n"
        "| Item | Gates |\n|---|---|\n"
        + "\n".join(f"| {a} | {b} |" for a, b in u_items)
        + "\n\nNo lead is frozen. No purchase. No gate result.\n"
    )

    (GEN / "support-interface.md").write_text(
        "# Front-support interface\n\n"
        "| Article | Native h | Shim vs 42 mm axle | Hole pattern | Contact x | 360° sweep |\n"
        "|---|---:|---:|---|---:|---|\n"
        f"| Ball D21 class (Pololu 2691 envelope) | {P.BALL_NATIVE_H} | {P.BALL_SHIM} | 3×M3, span {P.BALL_HOLE_SPAN}, PCD {P.BALL_PCD} | {P.FRONT_CONTACT_X} | housing Ø{P.BALL_HOUSING_D}+4 ghost |\n"
        f"| Caster D20 class 33×38 | {P.CASTER_NATIVE_H} | {P.CASTER_SHIM} | 30×23 M4 | {P.FRONT_CONTACT_X} | trail {P.CASTER_TRAIL_MIN}–{P.CASTER_TRAIL_MAX} U, displayed {P.CASTER_TRAIL_DISPLAY} |\n\n"
        "Contact x is identical. Trail does not move F_FRONT_CONTACT; it moves the swivel axis.\n"
    )

    (GEN / "connector-table.md").write_text(
        "# Connector table (keep-out class, family is RP-02)\n\n"
        "| Source | Destination | Family | Mate dir | Disconnect order |\n"
        "|---|---|---|---|---|\n"
        "| MOTOR_L pigtail | DRIVER_L | PH2.0 6-pin class | inboard then up | 3 after arm-off |\n"
        "| MOTOR_R pigtail | DRIVER_R | PH2.0 6-pin class | inboard then up | 4 |\n"
        "| DRIVER_L/R logic | C3 | Dupont forbidden; keyed | body cavity | 2 |\n"
        "| CLIFF_* | C3 GPIO | native GPIO, no expander | harness_sense | 5 |\n"
        "| IR_FRONT | C3 ADC | analog + divider | +x at contact | 6 |\n"
        "| IMU_BASE | C3 SPI | SPI+INT1 | rigid base | 7 |\n"
        "| Neck trunk | body demate | keyed, both-face strain relief | +z at F_NECK | 1 last-on first-off |\n"
    )

    (GEN / "dimensions.md").write_text(
        f"# Pass 1 dimensions ({P.LAYOUT_REV})\n\n"
        f"Displayed wheel family **{P.WHEEL_FAMILY_DISPLAYED}**. SKU frozen: **{P.SKU_FROZEN}**.\n\n"
        f"- Track {P.TRACK} mm, axle {P.H_AXLE} mm, loaded radius assumption {P.LOADED_RADIUS} mm (squash U).\n"
        f"- Front contact x {P.FRONT_CONTACT_X} mm (band {P.FRONT_CONTACT_X_MIN}–{P.FRONT_CONTACT_X_MAX}), identical ball/caster: {dims['contact_x_ball_equals_caster']}.\n"
        f"- Ball shim {P.BALL_SHIM} mm, caster shim {P.CASTER_SHIM} mm, stack 0–15 mm.\n"
        f"- Skid displayed {P.SKID_REACH} × {P.SKID_HEIGHT} mm inside bands {P.SKID_REACH_MIN}–{P.SKID_REACH_MAX} / {P.SKID_H_MIN}–{P.SKID_H_MAX}. Not a 14/70 freeze.\n"
        f"- Scored CoM (ball, g) {phys_b['com_mm']}, mass {phys_b['mass_g']:.1f} g, a_tip {phys_b['a_tip_m_s2']:.3f} m/s², sign ok {phys_b['a_tip_positive']}.\n"
        f"- Drive row {phys_b['drive_mass_g']:.1f} g, band ok {phys_b['drive_band_ok']}.\n"
        f"- Skid inequality h/d={phys_b['skid_h_over_d']:.4f} vs x/h={phys_b['x_over_h']:.4f}, ok {phys_b['skid_inequality_ok']}.\n"
        f"- Head import identity rotation, origin {P.HEAD_ORIGIN_IN_CHASSIS}, F_NECK {P.F_NECK}.\n"
    )
    print(f"wrote {GEN}")


if __name__ == "__main__":
    main()
