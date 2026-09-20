#!/usr/bin/env python3
"""Deterministic pass-1 checks. Paper values with capture classes. No gate claim."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib import params as P
from lib.frames import frames
from lib.mass import mass_rows, physics

GEN = ROOT / "generated"


def check(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": detail}


def main():
    dims = json.loads((GEN / "dimensions.json").read_text())
    phys = json.loads((GEN / "physics.json").read_text())
    mass = json.loads((GEN / "mass-register.json").read_text())
    fb, fc = frames("ball"), frames("caster")
    rows = mass_rows("ball")
    pb = physics(rows, "ball")

    checks = []
    checks.append(check("track_170", P.TRACK == 170.0, str(P.TRACK)))
    checks.append(check("axle_42", P.H_AXLE == 42.0, str(P.H_AXLE)))
    checks.append(check("contact_x_in_band", P.FRONT_CONTACT_X_MIN <= P.FRONT_CONTACT_X <= P.FRONT_CONTACT_X_MAX))
    checks.append(check("contact_x_identical", fb["F_FRONT_CONTACT"][0] == fc["F_FRONT_CONTACT"][0],
                        f"{fb['F_FRONT_CONTACT'][0]} vs {fc['F_FRONT_CONTACT'][0]}"))
    checks.append(check("shim_ball_in_0_15", P.SHIM_MIN <= P.BALL_SHIM <= P.SHIM_MAX, str(P.BALL_SHIM)))
    checks.append(check("shim_caster_in_0_15", P.SHIM_MIN <= P.CASTER_SHIM <= P.SHIM_MAX, str(P.CASTER_SHIM)))
    checks.append(check("shim_reaches_both_native",
                        abs((P.BALL_NATIVE_H + P.BALL_SHIM) - P.H_AXLE) < 1e-6
                        and abs((P.CASTER_NATIVE_H + P.CASTER_SHIM) - P.H_AXLE) < 1e-6))
    checks.append(check("skid_reach_in_band", P.SKID_REACH_MIN <= P.SKID_REACH <= P.SKID_REACH_MAX))
    checks.append(check("skid_height_in_band", P.SKID_H_MIN <= P.SKID_HEIGHT <= P.SKID_H_MAX))
    checks.append(check("not_frozen_14_70", not (P.SKID_HEIGHT == 14 and P.SKID_REACH == 70)))
    batt_xmin = P.BATTERY_X - P.BATTERY_BODY[0] / 2
    checks.append(check("battery_entirely_forward", batt_xmin > 0, f"xmin={batt_xmin}"))
    checks.append(check("bay_cannot_sit_at_or_behind_axle", P.BAY_X_MIN > 0, str(P.BAY_X_MIN)))
    checks.append(check("a_tip_positive", pb["a_tip_positive"], str(pb["a_tip_m_s2"])))
    checks.append(check("skid_inequality", pb["skid_inequality_ok"],
                        f"h/d={pb['skid_h_over_d']:.4f} < x/h={pb['x_over_h']:.4f}"))
    checks.append(check("drive_mass_band", pb["drive_band_ok"], str(pb["drive_mass_g"])))
    zero = [r["id"] for r in rows if r["state"] == "installed" and r["mass_g"] <= 0]
    checks.append(check("no_zero_mass_installed", zero == [], str(zero)))
    checks.append(check("sku_not_frozen", P.SKU_FROZEN is False))
    checks.append(check("dimensions_json_agrees_params", dims["track_mm"] == P.TRACK and dims["h_axle_mm"] == P.H_AXLE))
    stance = P.TRACK + P.WHEEL_WIDTH
    checks.append(check("stance_within_205", stance <= P.CON14_W + 1e-6, f"stance={stance}"))
    # Overall D: cliff lead + skid reach is a finding, not a silent shrink
    overall_d = P.FRONT_CONTACT_X + P.CLIFF_F_LEAD + 6 + P.SKID_REACH + P.SKID_PAD[0] / 2
    checks.append(check("overall_d_reported", True, f"extrema_d≈{overall_d:.1f} vs CON-14 {P.CON14_D} (HOLD if >)"))
    checks.append(check("wheel_axes_height", fb["F_WHEEL_L"][2] == fb["F_WHEEL_R"][2] == P.H_AXLE))
    checks.append(check("u_register_present", (GEN / "u-register.md").exists()))

    failed = [c for c in checks if not c["ok"]]
    report = {"ok": not failed, "checks": checks, "failed": failed, "gate_claim": False, "purchase": False}
    (GEN / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [f"# Pass 1 checks  {'PASS' if report['ok'] else 'FAIL'}", "",
             "No gate result. No ADR closure. No purchase.", ""]
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        lines.append(f"- [{mark}] {c['name']}" + (f" — {c['detail']}" if c["detail"] else ""))
    (GEN / "checks.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
