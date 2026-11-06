"""D-095: the tray bay (was PCB-04) with the two S13V30F5s hanging from the compute tray.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: each standoff lands on solid tray (not a vent), the tray holes keep their walls, screw
engagement, the top screw heads under the Pi, every part clear of the robot, the D-072 motor cable
keep-out (nothing new below Z 63 or over the motor pigtails), solder room under the pin rows, and
the body (with the tray and modules) lowering onto the chassis.
"""

import module_checks as C

OWN = ("M4 Pi 5 V", "M5 shared 5 V")
MOTOR_RESERVES = ("MOTOR_L_PIGTAIL_RESERVE", "MOTOR_R_PIGTAIL_RESERVE")
D072_FLOOR = 63.0                      # PCB-04 underside, which the D-072 keep-out was written against


def main():
    entry, tree, leaves = C.droid_tree()
    m = entry.TRAY_BAY
    r = C.Report("check_bay_tray")
    tray = C.find(leaves, "COMPUTE_TRAY").shape
    z = m["tray_z"]

    # 1. Standoff lands and holes: the Ø3.7 land fully under tray material; a 1.3 mm wall round each hole.
    for x, y in entry.tray_holes():
        land = entry._z_cyl(m["standoff"][0], z + 0.05, z + 1.0, x, y) - entry._z_cyl(m["hole_r"], z, z + 1.1, x, y)
        wall = entry._z_cyl(m["hole_r"] + 1.3, z + 0.05, z + 2.95, x, y) - entry._z_cyl(m["hole_r"], z, z + 3.0, x, y)
        hole_open = C.common(entry._z_cyl(m["hole_r"] - 0.05, z + 0.05, z + 2.95, x, y), tray)
        fl, fw = C.frac_inside(land, tray), C.frac_inside(wall, tray)
        r.check(f"standoff_land_and_hole_{x:+.1f}_{y:+.1f}", fl > 0.99 and fw > 0.97 and hole_open < 0.01,
                land_fraction=fl, wall_fraction=fw, material_in_hole_mm3=hole_open)

    # 2. Engagement in the 5 mm standoffs; the two screws do not meet inside it.
    tray_top = z + 3.0
    top_tip = tray_top - m["top_screw"]
    under = entry.TRAY_BOARD_TOP - entry.PCB_T
    bottom_tip = under + m["bottom_screw"]
    r.check("standoff_thread_engagement", (z - top_tip) >= 1.9 and (bottom_tip - entry.TRAY_BOARD_TOP) >= 2.0 and top_tip - bottom_tip >= 0.3,
            top_engaged=z - top_tip, bottom_engaged=bottom_tip - entry.TRAY_BOARD_TOP, gap_between_tips=top_tip - bottom_tip)

    # 3. Clearance of every new part (0.2 mm); standoffs touch the tray by design, screws pass it.
    subjects = [lf for lf in C.own(leaves, *OWN) if C.is_part(lf.path)]
    for lf in subjects:
        skip = OWN + (("COMPUTE_TRAY",) if any(k in lf.label for k in ("STANDOFF", "TRAY_SCREW")) else ())
        hits = C.clashes(lf.shape, leaves, skip=skip)
        gap, near = C.min_gap(lf.shape, leaves, skip=skip)
        r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)
    pi = C.find(leaves, "C0_RASPBERRY_PI5_EXACT_STEP")
    heads = [lf for lf in subjects if "TRAY_SCREW" in lf.label]
    head_gap = min(C.distance(lf.shape, pi.solid) for lf in heads)
    r.check("tray_screw_heads_under_pi", head_gap >= 0.5, min_gap_to_pi_box=head_gap)

    # 4. D-072: nothing new under Z 63 or over the motor pigtail reserves.
    low = min(lf.box[2] for lf in subjects)
    res_top = max(C.find(leaves, t).box[5] for t in MOTOR_RESERVES)
    over = []
    for t in MOTOR_RESERVES:
        b = C.find(leaves, t).box
        column = C.blk((b[0], b[3], b[1], b[4], b[2], D072_FLOOR))
        over += [h for h in C.clashes(column, leaves) if h[0] not in MOTOR_RESERVES and any(h[0] == lf.label for lf in subjects)]
    r.check("d072_motor_cable_keep_out", low >= D072_FLOOR and not over, lowest_module_z=low, pigtail_reserve_top=res_top,
            vertical_margin=low - res_top, new_parts_over_reserves=over)

    # 5. Solder room under each pin row (components face down): 3 mm below the board edge band, clear.
    for name, loc in entry.tray_module_frames():
        a, b = entry._world(loc, 5.0, 0.3), entry._world(loc, 18.0, 5.0)
        under_z = entry.TRAY_BOARD_TOP - entry.PCB_T
        band = C.blk((min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1]), under_z - 3.0, under_z - 0.05))
        hits = [h for h in C.clashes(band, leaves) if not h[0].startswith(name)]
        r.check(f"pin_row_solder_room_{name}", not hits, clashes=hits)

    # 6. The body comes down onto the chassis with the tray and modules on it: chassis parts only.
    chassis_side = ("CHASSIS_V1_REFERENCE", "M2 head", "M3 yaw", "M7 IMU", "M12_JST_PA_3P")
    below = [lf for lf in leaves if any(k in "/".join(lf.path) for k in chassis_side)]
    group = [(lf.label, lf.shape) for lf in subjects]
    hit = C.sweep(group, below, (0, 0, 1), [1.0 * k for k in range(0, 81, 2)])
    r.check("body_lowering_with_tray_modules", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
