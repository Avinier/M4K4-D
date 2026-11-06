"""D-095: the rear bay (was PCB-02): power switch, INA226 and charge splice on the rear-bay plate.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: the arms seated on the cross rail, the insert pilots and walls, screw engagement, the
counterbore and driver path from the rear, both boards in their cradles (rim gap, on the pads),
every part clear of the robot, the splice reserve, the plate sliding in from the rear with the
panel off, and the body lowering onto the chassis.
"""

import module_checks as C

OWN = ("REAR_BAY_", "M1 power switch", "M6 INA226", "CHARGE_SPLICE")
PANEL = ("REAR_SERVICE_PANEL", "REAR_PANEL_", "POWER_BUTTON_MUSHROOM", "M12_XT30", "M12_JST_XHP")


def main():
    entry, tree, leaves = C.droid_tree()
    m, cr = entry.REAR_BAY, entry.CRADLE
    r = C.Report("check_bay_rear")
    plate = C.find(leaves, "REAR_BAY_MODULE_PLATE").shape
    frame = C.find(leaves, "BODY_FRAME_MAIN_PRINT").shape
    face = m["rail_face"]

    # 1. Arms on the rail face, not in it; rail material behind each arm end.
    r.check("arms_on_rail_no_overlap", C.common(plate, frame) < 0.01, overlap_mm3=C.common(plate, frame), gap=C.distance(plate, frame))
    for y, z in m["screw_yz"]:
        pts = [(face + 0.3, y + dy, z + dz) for dy, dz in ((3.5, 0), (-3.5, 0), (0, 2.6), (0, -2.6))]
        r.check(f"rail_behind_arm_{y:+.0f}", all(C.point_in(frame, p) for p in pts), points=[C.point_in(frame, p) for p in pts])

    # 2. Pilots and engagement.
    rad, depth = m["rail_pilot"]
    for y, z in m["screw_yz"]:
        ann = entry._x_cyl(rad + 1.4, face + 0.05, face + depth, y, z) - entry._x_cyl(rad, face - 1, face + depth + 1, y, z)
        open_pilot = C.common(entry._x_cyl(rad - 0.05, face + 0.1, face + depth - 0.1, y, z), frame)
        f = C.frac_inside(ann, frame)
        r.check(f"rail_pilot_walls_{y:+.0f}", f > 0.97 and open_pilot < 0.01, wall_fraction_1p4mm=f, material_in_pilot_mm3=open_pilot)
    seat = m["cbore"][1]
    tip = seat + m["screw_len"]
    engaged = min(tip, face + m["insert"][2]) - face
    r.check("m3x16_engagement_in_insert", engaged >= 5.0 and tip <= face + depth - 0.2, engaged_mm=engaged, tip_x=tip, pilot_end_x=face + depth)
    # Counterbore: head clears it radially; a Ø6 driver path runs out the back (panel off).
    for y, z in m["screw_yz"]:
        path = entry._x_cyl(3.0, seat - 40.0, seat - entry.M3_BUTTON[1] - 0.05, y, z)
        hits = C.clashes(path, leaves, skip=PANEL + ("REAR_BAY_PLATE_M3X16",))
        r.check(f"driver_path_from_rear_{y:+.0f}", not hits and m["cbore"][0] - entry.M3_BUTTON[0] >= 0.2,
                radial_head_clearance=m["cbore"][0] - entry.M3_BUTTON[0], clashes=hits)

    # 3. Boards in their cradles: on the pads, 0.2 mm off the rim.
    pad_top = m["plate"][1] + cr["pad"]
    for label in ("M1_POLOLU_2813_PUSHBUTTON_POWER_SWITCH_HP_STEP", "M6_INA226_R010_BOARD_UNMEASURED"):
        lf = C.find(leaves, label)
        gap = C.distance(lf.shape, plate)
        on_pads = abs(lf.box[0] - pad_top) < 0.02
        ov = C.common(lf.shape, plate)
        r.check(f"in_cradle_{label}", on_pads and ov < 0.01, board_back_x=lf.box[0], pad_top_x=pad_top, overlap_mm3=ov, distance_to_plate=gap)
    sw = C.find(leaves, "M1_POLOLU_2813_PUSHBUTTON_POWER_SWITCH_HP_STEP")
    r.check("switch_terminal_edge_open", sw.box[4] < 0.0, switch_y_max=sw.box[4], ina_y_min=entry.INA226_AT[0])

    # 4. Clearance of every new part (0.2 mm) against the robot; own and intended contacts excluded.
    subjects = [lf for lf in C.own(leaves, *OWN) if C.is_part(lf.path)]
    for lf in subjects:
        skip = OWN + (("BODY_FRAME_MAIN_PRINT",) if lf.label.startswith(("REAR_BAY_MODULE_PLATE", "REAR_BAY_RAIL", "REAR_BAY_PLATE")) else ())
        hits = C.clashes(lf.shape, leaves, skip=skip)
        gap, near = C.min_gap(lf.shape, leaves, skip=skip)
        r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)
    res = C.find(leaves, "CHARGE_SPLICE_AND_LEADS_RESERVE")
    r.check("splice_reserve_clear", not C.clashes(res.shape, leaves, skip=OWN), clashes=C.clashes(res.shape, leaves, skip=OWN))

    # 5. Install: plate, boards and splice slide +X onto the rail with the rear panel off.
    group = [(lf.label, lf.shape) for lf in subjects if "SCREW" not in lf.label and "INSERT" not in lf.label]
    hit = C.sweep(group, leaves, (-1, 0, 0), [0.3 + 1.0 * k for k in range(25)], skip=OWN + PANEL)
    r.check("slides_in_from_rear_panel_off", hit is None, first_hit=hit)

    # 6. Body lowering onto the chassis with the rear bay fitted: chassis-side parts only.
    chassis_side = ("CHASSIS_V1_REFERENCE", "M2 head", "M3 yaw", "M7 IMU", "M12_JST_PA_3P")
    below = [lf for lf in leaves if any(k in "/".join(lf.path) for k in chassis_side)]
    hit = C.sweep([(lf.label, lf.shape) for lf in subjects], below, (0, 0, 1), [1.0 * k for k in range(0, 81, 2)])
    r.check("body_lowering_with_rear_bay", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
