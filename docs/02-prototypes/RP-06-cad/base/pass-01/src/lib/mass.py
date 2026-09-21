"""Mass register and paper physics. Capture classes W/D/E/U. No gate claims."""

from __future__ import annotations

from lib import params as P
from lib.frames import frames


def _head_com_chassis():
    ox, oy, oz = P.HEAD_ORIGIN_IN_CHASSIS
    cx, cy, cz = P.HEAD_LOCAL_COM
    return (ox + cx, oy + cy, oz + cz)


def mass_rows(support="ball"):
    fr = frames(support)
    hx, hy, hz = _head_com_chassis()
    ball_or_cas = (
        ("R-BALL", "Pololu 1in class envelope D21 lead", 1, P.BALL_MASS, "vendor", "D",
         (P.FRONT_CONTACT_X, 0.0, P.BALL_D / 2), "installed")
        if support == "ball" else
        ("R-CAS", "Ø30 swivel class envelope D20 swap", 1, P.CASTER_MASS, "estimate", "E",
         (P.FRONT_CONTACT_X, 0.0, P.CASTER_WHEEL_D / 2), "installed")
    )
    rows = [
        ("R-MTR-L", "JGA25-370-class keep-out with encoder", 1, P.MOTOR_MASS, "vendor", "D",
         (0.0, 40.0, P.H_AXLE), "installed"),
        ("R-MTR-R", "JGA25-370-class keep-out with encoder", 1, P.MOTOR_MASS, "vendor", "D",
         (0.0, -40.0, P.H_AXLE), "installed"),
        ("R-WHL-L", f"wheel family {P.WHEEL_FAMILY_DISPLAYED}", 1, P.WHEEL_MASS, "vendor", "D",
         fr["F_WHEEL_L"], "installed"),
        ("R-WHL-R", f"wheel family {P.WHEEL_FAMILY_DISPLAYED}", 1, P.WHEEL_MASS, "vendor", "D",
         fr["F_WHEEL_R"], "installed"),
        ("R-HUB-L", "printed 608 carrier + 2×608", 1, P.PRINT_MASS_HUB + 12.1 * 2, "CAD density", "E",
         (0.0, P.WHEEL_Y_L - 18.0, P.H_AXLE), "installed"),
        ("R-HUB-R", "printed 608 carrier + 2×608", 1, P.PRINT_MASS_HUB + 12.1 * 2, "CAD density", "E",
         (0.0, P.WHEEL_Y_R + 18.0, P.H_AXLE), "installed"),
        ("R-CLP-L", "printed motor clamp", 1, P.PRINT_MASS_CLAMP, "CAD density", "E",
         (0.0, 48.0, P.H_AXLE), "installed"),
        ("R-CLP-R", "printed motor clamp", 1, P.PRINT_MASS_CLAMP, "CAD density", "E",
         (0.0, -48.0, P.H_AXLE), "installed"),
        ("R-FRM", "open axle frame", 1, P.PRINT_MASS_FRAME, "CAD density", "E",
         (20.0, 0.0, 36.0), "installed"),
        ("R-MNT", "front mount + shim", 1, P.PRINT_MASS_MOUNT, "CAD density", "E",
         (P.FRONT_CONTACT_X, 0.0, P.H_AXLE), "installed"),
        ("R-ADP", "installed front adapter", 1, P.PRINT_MASS_ADP, "CAD density", "E",
         (P.FRONT_CONTACT_X, 0.0, 20.0), "installed"),
        ball_or_cas,
        ("R-SKID", "skid carrier + pad", 1, P.PRINT_MASS_SKID, "CAD density", "E",
         (-P.SKID_REACH, 0.0, P.SKID_HEIGHT), "installed"),
        ("R-BAY", "ballast bay structure", 1, P.PRINT_MASS_BAY, "CAD density", "E",
         (50.0, 0.0, 28.0), "installed"),
        ("R-BATT", "pack/dummy forward of axle", 1, P.BATTERY_MASS, "estimate", "E",
         (P.BATTERY_X, 0.0, P.BATTERY_Z), "installed"),
        ("R-BALLAST", "ballast lump, independent x/h", 1, P.BALLAST_MASS, "estimate", "E",
         (P.BALLAST_X, 0.0, P.BALLAST_Z), "installed"),
        ("R-C3", "ESP32-S3-DevKitC-1-N8 keep-out", 1, 12.0, "estimate", "E",
         (48.0, 22.0, 72.0), "installed"),
        ("R-DRV-L", "DRV8874-class installed keep-out", 1, P.DRV_MASS, "vendor", "D",
         (30.0, 18.0, 55.0), "installed"),
        ("R-DRV-R", "DRV8874-class installed keep-out", 1, P.DRV_MASS, "vendor", "D",
         (30.0, -18.0, 55.0), "installed"),
        ("R-IR", "GP2Y-class envelope", 1, 3.6, "vendor", "D",
         fr["F_IR_OPTICAL"], "installed"),
        ("R-CLF", "three TCRT-class patches", 3, 0.23, "vendor", "D",
         fr["F_CLIFF_F"], "installed"),
        ("R-BMP", "printed bar + two switches", 1, P.PRINT_MASS_BUMPER + 8.0, "estimate", "E",
         fr["F_BUMPER"], "installed"),
        ("R-IMU", "SPI IMU module envelope U", 1, 2.0, "estimate", "U",
         fr["F_IMU"], "installed"),
        ("R-HARN", "harness volumes (no second cable mass)", 1, 25.0, "estimate", "E",
         (20.0, 0.0, 90.0), "installed"),
        ("R-HDUM", "Layout 03 complete-head lump M008=20g", 1, P.HEAD_MASS_NOM, "CAD density", "E",
         (hx, hy, hz), "installed"),
        ("FASTENERS", "M3/M4 class allowance", 1, 18.0, "estimate", "E",
         (0.0, 0.0, 40.0), "installed"),
        ("CONTINGENCY", "documented line, not hidden margin", 1, 40.0, "estimate", "E",
         (20.0, 0.0, 40.0), "installed"),
    ]
    out = []
    for rid, desc, qty, mass, source, cap, com, state in rows:
        out.append({
            "id": rid, "description": desc, "qty": qty, "mass_g": mass,
            "source": source, "capture": cap, "com_mm": com, "state": state,
        })
    return out


def placed_com(rows):
    m = 0.0
    mx = my = mz = 0.0
    for r in rows:
        if r["state"] != "installed":
            continue
        w = r["mass_g"] * r["qty"]
        m += w
        mx += w * r["com_mm"][0]
        my += w * r["com_mm"][1]
        mz += w * r["com_mm"][2]
    if m <= 0:
        raise ValueError("zero mass register")
    return m, (mx / m, my / m, mz / m)


def physics(rows, support="ball"):
    m, com = placed_com(rows)
    x, y, h = com
    g = 9.81
    a_tip = g * (x / 1000.0) / (h / 1000.0) if h > 0 else float("-inf")
    d = P.SKID_REACH
    skid_h = P.SKID_HEIGHT
    ineq_left = skid_h / d
    ineq_right = x / h if h else 0.0
    drive_ids = {"R-MTR-L", "R-MTR-R", "R-WHL-L", "R-WHL-R", "R-HUB-L", "R-HUB-R",
                 "R-CLP-L", "R-CLP-R", "R-MNT", "R-ADP", "R-SKID", "R-DRV-L", "R-DRV-R"}
    if support == "ball":
        drive_ids.add("R-BALL")
    else:
        drive_ids.add("R-CAS")
    drive = sum(r["mass_g"] * r["qty"] for r in rows if r["id"] in drive_ids)
    return {
        "mass_g": m,
        "com_mm": com,
        "a_tip_m_s2": a_tip,
        "a_tip_positive": a_tip > 0,
        "skid_h_over_d": ineq_left,
        "x_over_h": ineq_right,
        "skid_inequality_ok": ineq_left < ineq_right,
        "drive_mass_g": drive,
        "drive_band_ok": P.DRIVE_MASS_MIN <= drive <= P.DRIVE_MASS_MAX,
        "battery_x": P.BATTERY_X,
        "battery_forward": P.BATTERY_X > 0,
    }


def drive_kinematics():
    r = P.LOADED_RADIUS / 1000.0
    v070 = 0.70
    rpm_070 = v070 / (2 * 3.141592653589793 * r) * 60.0
    track = P.TRACK / 1000.0
    yaw = 220.0 * 3.141592653589793 / 180.0
    rpm_spin = (yaw * track / 2) / (2 * 3.141592653589793 * r) * 60.0
    cpr = 11 * 35
    circ = 2 * 3.141592653589793 * r
    mm_per_count = circ * 1000.0 / cpr
    counts_creep = 0.04 / circ * cpr
    return {
        "loaded_radius_m": r,
        "rpm_at_0_70": rpm_070,
        "rpm_spin_220dps": rpm_spin,
        "mm_per_count": mm_per_count,
        "counts_s_at_creep": counts_creep,
        "encoder_ok": mm_per_count <= 2.0 and counts_creep >= 20.0,
    }
