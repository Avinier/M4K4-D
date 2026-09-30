"""Fast checks for the battery pack, battery tub and CH-038 ballast screws.

Covers the battery/ballast rows of check_layout.py plus the countersunk ballast
seat. Run from this folder with the text-to-cad 0.4.28 runtime:
python check_battery_ballast.py
Writes generated/battery-ballast-checks.json.
"""
import json
import os
import sys

sys.path.insert(0, ".")
M = __import__(os.environ.get("CHECK_MODEL", "body_chassis_model"))


def _vol(s):
    return 0.0 if s is None else s.volume


def leaves(s):
    k = getattr(s, "children", None)
    return [l for c in k for l in leaves(c)] if k else [s]


def by_label(ss, label):
    return next(s for s in ss if s.label == label)


def meet(a, b, tol=1e-6):
    # Containment counts as meeting (BoundBox.overlaps() misses it).
    p, q = a.bounding_box(), b.bounding_box()
    return (p.min.X < q.max.X - tol and q.min.X < p.max.X - tol and p.min.Y < q.max.Y - tol
            and q.min.Y < p.max.Y - tol and p.min.Z < q.max.Z - tol and q.min.Z < p.max.Z - tol)


def clash_map(parts, others, skip=()):
    out = {}
    for part in parts:
        for other in others:
            if other is part or frozenset((part.label, other.label)) in skip:
                continue
            if meet(part, other):
                v = _vol(part & other)
                if v > 1e-3:
                    out[f"{part.label} x {other.label}"] = round(v, 3)
    return out


frame_parts = leaves(M.chassis_frame())
deck_front = [p for p in frame_parts if p.label == "CHASSIS_DECK_WITH_BODY_INTERFACE"][1]  # FRONT print, carries the tub walls
hatch = by_label(frame_parts, "BATTERY_TUB_BOTTOM_HATCH")
ballast = [p for p in frame_parts if p.label.startswith("BALLAST_")]
bar = by_label(ballast, "BALLAST_STEEL_BAR")
heads = [p for p in ballast if "_HEAD_" in p.label]
shanks = [p for p in ballast if "_SHANK_" in p.label]
battery = by_label(M.electronics().children, "BATTERY_2S1P_18650_PACK")
battery_parts = leaves(battery)
shell = next(l for l in leaves(M.body_shell()) if l.label == "BODY_SHELL")
others = [
    *frame_parts, shell, *leaves(M.body_panels()), *leaves(M.panel_mount_hardware()), *leaves(M.body_primary_frame()),
    *[c for c in M.electronics().children if c.label != battery.label], *battery_parts,
    *M.sensors().children, *leaves(M.harness_routes()), *leaves(M.body_audio()),
    *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R")),
    *leaves(M.wheel_assembly("L")), *leaves(M.wheel_assembly("R")),
    *leaves(M.bearing_pair("L")), *leaves(M.bearing_pair("R")),
    *leaves(M.body_chassis_mount_hardware()), *leaves(M.rear_skid_tcrt_module()), *leaves(M.ball_transfer()),
]
R = {}

# Pack: no clashes, fits the tub with retention clearance, cells 1 mm apart.
R["battery_pack_is_clear"] = clash_map(battery_parts, [o for o in others if o not in battery_parts])
cells = sorted((p for p in battery_parts if "BATTERY_CELL_" in p.label), key=lambda p: p.bounding_box().center().X)
R["cell_gap_mm"] = round(cells[1].bounding_box().min.X - cells[0].bounding_box().max.X, 3)
pb = battery.bounding_box()
inner_x = (M.BATTERY_TUB_X[0] + M.BATTERY_TUB_WALL, M.BATTERY_TUB_X[1])
inner_y = M.BATTERY_TUB_HALF_Y - M.BATTERY_TUB_WALL
R["tub_margin_mm"] = {
    "rear_x": round(pb.min.X - inner_x[0], 3), "front_x": round(inner_x[1] - pb.max.X, 3),
    "side_y": round(min(pb.min.Y + inner_y, inner_y - pb.max.Y), 3),
    "floor_z": round(pb.min.Z - M.BATTERY_TUB_FLOOR_Z[1], 3), "below_deck_top_z": round(M.DECK_Z + 2.0 - pb.max.Z, 3),
}

# Tub (hatch, and the front deck print carrying the walls) against everything
# outside the frame, and the hatch against the frame too. These pairs overlapped
# before the 2026-09-30 cell-pitch change as well (hatch 1665, power 189 mm3);
# they are OPEN, reported but not counted as a pass or fail.
OPEN = {
    "BATTERY_TUB_BOTTOM_HATCH x BODY_SHELL": "hatch flange (tub X -3/+4, Y +/-10) is larger than the shell floor opening (X -1/+2.5, Y +/-1); unresolved",
    "CHASSIS_DECK_WITH_BODY_INTERFACE x BODY_SHELL": "shell-to-deck interface overlap; unresolved",
    "CHASSIS_DECK_WITH_BODY_INTERFACE x POWER_DISTRIBUTION_BOARDS": "proposal board envelopes and keep-outs; unresolved",
    "CHASSIS_DECK_WITH_BODY_INTERFACE x IMU_PCB07": "IMU M2 screws thread-form into the deck by design",
}
non_frame = [o for o in others if o not in frame_parts]
tub = clash_map([hatch], [o for o in others if o is not hatch and o not in battery_parts])
tub |= clash_map([deck_front], [o for o in non_frame if o not in battery_parts])
R["tub_clashes"] = {k: v for k, v in tub.items() if k not in OPEN}
R["tub_open"] = {k: {"mm3": v, "note": OPEN[k]} for k, v in tub.items() if k in OPEN}

# Ballast: no clashes except the shanks in the bar's tapped holes (coincident radius).
R["ballast_is_clear"] = clash_map(ballast, [o for o in others if o not in ballast])
R["ballast_self"] = clash_map(heads, [bar]) | clash_map(shanks, [bar])
R["csk_heads_seated"] = {h.label: {"gap_to_deck_mm": round(h.distance_to(deck_front), 4),
                                   "top_below_deck_top_mm": round(M.DECK_Z + 2.0 - h.bounding_box().max.Z, 3)} for h in heads}
R["shank_clear_of_deck_mm"] = {s.label: round(s.distance_to(deck_front), 3) for s in shanks}
R["screw_length_mm"] = round(heads[0].bounding_box().max.Z - shanks[0].bounding_box().min.Z, 3)
hole_floor = M.BALLAST_Z[1] - getattr(M, "BALLAST_SCREW_HOLE_DEPTH", M.BALLAST_SCREW_THREAD_DEPTH)
R["engagement_mm"] = round(M.BALLAST_Z[1] - shanks[0].bounding_box().min.Z, 3)
R["tip_to_hole_floor_mm"] = round(shanks[0].bounding_box().min.Z - hole_floor, 3)

mp = M.mass_properties()
com = mp["com_mm"]
R["mass_g"] = round(mp["mass_g"], 1)
R["com_mm"] = [round(c, 2) for c in com]
R["a_tip_m_s2"] = round(9.81 * com[0] / com[2], 3)
R["a_tip_min_m_s2"] = round(9.81 * 20.0 / 124.0, 3)

ok = {
    "battery_pack_is_clear": not R["battery_pack_is_clear"],
    "cells_more_than_1mm_apart": R["cell_gap_mm"] > 1.0,
    "pack_fits_tub": all(v >= 0.4 for k, v in R["tub_margin_mm"].items() if k != "floor_z") and -1e-6 <= R["tub_margin_mm"]["floor_z"] <= M.BATTERY_WRAP_T + 1e-6,
    "tub_has_no_new_clashes": not R["tub_clashes"],
    "ballast_is_clear": not R["ballast_is_clear"],
    "ballast_self_clear": not R["ballast_self"],
    "csk_heads_seated_flush_or_below": all(v["gap_to_deck_mm"] < 1e-3 and v["top_below_deck_top_mm"] >= 0.0 for v in R["csk_heads_seated"].values()),
    "screw_is_12mm": abs(R["screw_length_mm"] - 12.0) < 1e-3,
    "tip_clears_hole_floor": R["tip_to_hole_floor_mm"] > 0.0,
    "com_forward_of_physics_margin_line": R["a_tip_m_s2"] >= R["a_tip_min_m_s2"],
}
R["pass"] = ok
if os.environ.get("CHECK_MODEL") is None:
    (M.Path(__file__).resolve().parent / "generated" / "battery-ballast-checks.json").write_text(json.dumps(R, indent=1) + "\n")
print(json.dumps(R, indent=1))
print("ALL PASS" if all(ok.values()) else "FAIL: " + ", ".join(k for k, v in ok.items() if not v))
