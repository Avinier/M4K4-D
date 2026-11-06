"""D-095: mass and centre of mass after the D-093 module change, and the forward tipping margin.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 3 min.
The whole-robot register is the hand-kept MASS_ROWS in body_v1_model.py (rp06-mass-register-is-
manual). Subsystem sources stay unchanged, so this script applies D-095's rows on top of it:

- removed: the PCB-02, PCB-13, PCB-03, PCB-04 and PCB-07 rows; the PCB-05 and PCB-06 shares of
  BODY_AUDIO (6 g at the old PCB-05 centre, 3 g at the D-037 mic-array centre);
- added, measured from the D-095 solids: the three new prints at 1.20 g/cm3 (the body frame's
  near-solid PETG figure) and every new screw, insert and standoff (steel 7.85, brass 8.50);
- added, D (vendor) or E (estimate): each bought module at its CAD centroid;
- printed-part changes: the frame, shell, rear panel, tray and front deck measured before (the
  committed makad-v1.step.py, from git HEAD) and after D-095, at their register densities.

Then CoM, a_tip = g x / z at the neutral pose, and the conservative worst head pose exactly as
body check_body_layout.py computes them, against the 1.582 m/s2 minimum (BA-06).
"""

import json
import math
import subprocess
import types
from pathlib import Path

import module_checks as C

PETG_BODY, PETG_CHASSIS, STEEL, BRASS = 1.20, 0.571, 7.85, 8.50
A_TIP_MIN = 9.81 * 20.0 / 124.0
DROPPED_ROWS = ("PCB02_CHARGE_AND_SYSTEM_POWER", "CHARGE_INLET_PCB13", "PCB03_MOTOR_GATE_AND_HEAD_RAIL",
                "PCB04_BRANCH_CONVERTERS", "IMU_PCB07")
# Bought modules: label prefix -> (mass g, evidence)
MODULE_MASS = {
    "M1_POLOLU_2813": (2.7, "D Pololu #2813 specs"),
    "M2_POLOLU_2572": (7.5, "D Pololu #2572 specs"),
    "M3_POLOLU_2572": (7.5, "D Pololu #2572 specs"),
    "M4_POLOLU_4082": (3.5, "D Pololu #4082 specs"),
    "M5_POLOLU_4082": (3.5, "D Pololu #4082 specs"),
    "M6_INA226_R010_BOARD": (3.0, "E INA226 board with 2512 shunt, unweighed"),
    "M7_ADAFRUIT_4438_LSM6DSOX_BOARD": (2.0, "E Adafruit #4438 class breakout"),
    "M8_MAX98357A_BOARD": (3.0, "E #3006-class breakout with screw terminal"),
    "M9_INMP441_FRONT_L_BOARD": (1.0, "E INMP441 module"),
    "M9_INMP441_FRONT_R_BOARD": (1.0, "E INMP441 module"),
    "M9_INMP441_REAR_L_BOARD": (1.0, "E INMP441 module"),
    "M9_INMP441_REAR_R_BOARD": (1.0, "E INMP441 module"),
    "M12_XT30U_FEMALE_CHARGE_PORT": (1.5, "E AMASS XT30U-F with solder cups"),
    "M12_JST_XHP_3_BALANCE_PORT_PLUG": (0.5, "E XHP-3 with three SXH contacts"),
    "M12_JST_PA_3P_BALANCE_BREAK_MATED_PAIR": (0.5, "E PAP-03V-S + PALR-03VF with contacts"),
    "CHARGE_SPLICE_HEATSHRUNK_AWG16": (4.4, "E butt splice 1.5 g + 2 x AWG16 x 150 mm XT30 leads 2.9 g"),
    "M13_AUDIO_HUB_PERFBOARD": (3.0, "E perfboard with resistors and wire ends"),
}
# Leads with no solid: (mass g, centroid, evidence)
EXTRA = {"BALANCE_LEAD_3XAWG24": (4.3, None, "E 3 x AWG24 x 0.55 m at 2.6 g/m, at the lead reserves' centroid")}
PRINTS = ("TUB_BAY_MODULE_PLATE", "REAR_BAY_MODULE_PLATE", "IMU_ADAPTER_LSM6DSOX")
EDITED = {"BODY_FRAME_MAIN_PRINT": PETG_BODY, "BODY_SHELL": PETG_BODY, "REAR_SERVICE_PANEL_OCTAGONAL": PETG_BODY,
          "COMPUTE_TRAY": PETG_BODY, "CHASSIS_FRAME_FRONT_MODULE": PETG_CHASSIS}


def centroid(shape):
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, p)
    c = p.CentreOfMass()
    return p.Mass(), (c.X(), c.Y(), c.Z())


def head_entry():
    """The committed makad-v1.step.py (git HEAD), loaded as a module in this folder's place."""
    src = subprocess.run(["git", "show", "HEAD:./makad-v1.step.py"], cwd=C.HERE, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("makad_v1_head")
    mod.__file__ = str(C.HERE / "makad-v1.step.py")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def edited_volumes(entry):
    import body_v1_model as B
    from build123d import Compound
    tree = entry._apply_droid_cuts(Compound(children=[B.build_body_assembly(), B.chassis_v1_reference()]), strict=False)
    out = {}
    for path, node, loc in C._leaves(tree):
        if path[-1] in EDITED:
            out[path[-1]] = centroid(C.place(node, loc))
    return out


def tip(rows, M):
    """Neutral and worst-pose a_tip from register rows [(name, g, (x, y, z))], as check_body_layout.py."""
    total = sum(r[1] for r in rows)
    com = tuple(sum(r[1] * r[2][i] for r in rows) / total for i in range(3))
    x, y, z = com
    register = {r[0]: r for r in rows}
    head_tree = json.loads((M.HEAD_DIR / "mass-placement.json").read_text())
    pitch, roll, axes = head_tree["working"]["pitch"], head_tree["working"]["roll"], head_tree["axes"]
    pitch_off = math.hypot(pitch["center_mm"][0] - axes["pitch_x"], pitch["center_mm"][2] - axes["pitch_z"])
    roll_off = math.hypot(roll["center_mm"][1] - axes["roll_y"], roll["center_mm"][2] - axes["roll_z"])
    pr = (2 * pitch["mass_g"] * pitch_off + 2 * roll["mass_g"] * roll_off) / total
    yaw_r = math.hypot(M.HEAD_LOCAL_COM[0] - M.HEAD_LOCAL_YAW[0], M.HEAD_LOCAL_COM[1])
    yaw_shift = M.HEAD_MASS_G * ((M.BODY_AXIS_X - yaw_r) - register["HEAD_V1"][2][0]) / total
    wx, wz = x + yaw_shift - pr, z + pr
    return dict(mass_g=total, com_mm=com, a_tip=9.81 * x / z, worst_pose_a_tip=9.81 * wx / wz)


def main():
    import body_v1_model as M
    r = C.Report("check_d095_mass")
    base = [(n, g, tuple(c)) for n, g, c, _ in M.MASS_ROWS]
    before = tip(base, M)
    r.check("register_baseline_reproduces_body_mass_properties", abs(before["mass_g"] - M.mass_properties()["mass_g"]) < 0.01,
            mass_g=before["mass_g"], com_mm=before["com_mm"], a_tip=before["a_tip"], worst_pose_a_tip=before["worst_pose_a_tip"])

    rows = [row for row in base if row[0] not in DROPPED_ROWS]
    removed = [row for row in base if row[0] in DROPPED_ROWS]
    delta = [("BODY_AUDIO: PCB-05 share", -6.0, tuple(M.PCB05_CENTER), "RP03-CAD-11 PCB-05 ~6 g"),
             ("BODY_AUDIO: PCB-06 boards and D-037 hardware", -3.0, (16.0, 0.0, 113.0), "mic boards ~2 g + D-037 ~1 g")]

    entry, tree, leaves = C.droid_tree()
    for lf in leaves:
        lab = lf.label
        key = next((k for k in MODULE_MASS if lab.startswith(k)), None)
        if key:
            g, why = MODULE_MASS[key]
            delta.append((lab, g, centroid(lf.shape)[1], why))
        elif lab in PRINTS:
            v, c = centroid(lf.shape)
            delta.append((lab, v * PETG_BODY / 1000.0, c, f"measured {v / 1000:.2f} cm3 x {PETG_BODY}"))
        elif ("Bought modules" in "/".join(lf.path) or lab.startswith(("TUB_BAY_", "REAR_BAY_", "YAW_JUNCTION_J8_8"))) and C.is_part(lf.path) \
                and any(k in lab for k in ("SCREW", "INSERT", "STANDOFF", "WASHER", "HEADER", "MATED_PLUG")) and "TERMINAL" not in lab:
            v, c = centroid(lf.shape)
            rho = BRASS if ("INSERT" in lab or "STANDOFF" in lab) else (1.3 if ("HEADER" in lab or "PLUG" in lab) else STEEL)
            delta.append((lab, v * rho / 1000.0, c, f"measured {v:.1f} mm3 x {rho}"))
    lead = [lf for lf in leaves if "M12_BALANCE_" in lf.label and "RESERVE" in lf.label]
    vols = [centroid(lf.shape) for lf in lead]
    vt = sum(v for v, _ in vols)
    lead_c = tuple(sum(v * c[i] for v, c in vols) / vt for i in range(3))
    g, _, why = EXTRA["BALANCE_LEAD_3XAWG24"]
    delta.append(("BALANCE_LEAD_3XAWG24", g, lead_c, why))
    # Old PCB-08 sideband headers and plugs (J8-3, J8-5): about 1 g out of the PCB-08 row.
    delta.append(("YAW_JUNCTION_PCB08: J8-3/J8-5 removed", -1.0, (-3.4, -36.5, 117.0), "E two GH8 headers and plugs"))

    C.log("measuring printed-part changes against git HEAD")
    after = edited_volumes(entry)
    prior = edited_volumes(head_entry())
    for name, rho in EDITED.items():
        (va, ca), (vb, cb) = after[name], prior[name]
        dv = va - vb
        if abs(dv) < 1e-3:
            continue
        c = tuple((va * ca[i] - vb * cb[i]) / dv for i in range(3))
        delta.append((f"{name} change", dv * rho / 1000.0, c, f"measured {dv:+.0f} mm3 x {rho}"))

    rows += [(n, g, c) for n, g, c, _ in delta]
    now = tip(rows, M)
    r.check("removed_rows", True, rows=[(n, g) for n, g, _ in removed], total_g=-sum(g for _, g, _ in removed))
    r.check("added_rows", True, total_g=sum(d[1] for d in delta), rows=[(n, round(g, 2), [round(v, 1) for v in c], why) for n, g, c, why in delta])
    r.check("neutral_a_tip_above_minimum", now["a_tip"] >= A_TIP_MIN, a_tip=now["a_tip"], before=before["a_tip"], minimum=A_TIP_MIN,
            mass_g=now["mass_g"], mass_before_g=before["mass_g"], com_mm=now["com_mm"], com_before_mm=before["com_mm"])
    r.check("worst_head_pose_a_tip_above_minimum", now["worst_pose_a_tip"] >= A_TIP_MIN, worst_pose_a_tip=now["worst_pose_a_tip"],
            before=before["worst_pose_a_tip"], minimum=A_TIP_MIN)
    r.finish()


if __name__ == "__main__":
    main()
