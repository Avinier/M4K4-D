"""D-095: the tub bay (was PCB-03) with the two S18V20ALVs on their printed plate.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: the plate seated on the deck strips, the four insert pilots and their walls, screw and
insert engagement, the M2 bosses, every new part clear of the robot, the modules under the signal
trunks, wire room at the module terminals, and the plate going on from above (body off).
"""

import module_checks as C

OWN = ("TUB_BAY_", "M2 head", "M3 yaw")
TRUNKS = ("HARNESS_SIGNAL_TRUNK", "HARNESS_SENSOR_TRUNK")


def main():
    entry, tree, leaves = C.droid_tree()
    m = entry.TUB_BAY
    r = C.Report("check_bay_tub")
    plate = C.find(leaves, "TUB_BAY_MODULE_PLATE").shape
    deck = C.find(leaves, "CHASSIS_FRAME_FRONT_MODULE").shape
    z0, top = m["plate"][4], m["plate"][5]

    # 1. Seated: touching the deck, not in it, and deck under every fixing.
    r.check("plate_on_deck_no_overlap", C.common(plate, deck) < 0.01, overlap_mm3=C.common(plate, deck), gap=C.distance(plate, deck))
    under = {f"{x:+.0f},{y:+.0f}": all(C.point_in(deck, (x + dx, y + dy, z0 - 0.3)) for dx, dy in ((3.2, 0), (-3.2, 0), (0, 3.2), (0, -3.2)))
             for x, y in (*m["fix_rear"], *m["fix_front"])}
    r.check("deck_material_round_every_fixing", all(under.values()), points=under)

    # 2. Insert pilots: walls all round (annulus 2.0-3.2 mm fully in the deck over the insert length).
    for (x, y), (_, _, length) in [*[(p, m["insert_rear"]) for p in m["fix_rear"]], *[(p, m["insert_front"]) for p in m["fix_front"]]]:
        ring = C.blk((x - 3.2, x + 3.2, y - 3.2, y + 3.2, z0 - length, z0 - 0.05))
        hole = entry._z_cyl(m["pilot_r"], z0 - length - 1, z0 + 1, x, y)
        ann = entry._z_cyl(3.2, z0 - length, z0 - 0.05, x, y) - hole
        f = C.frac_inside(ann, deck)
        open_pilot = C.common(entry._z_cyl(m["pilot_r"] - 0.05, z0 - length + 0.1, z0 - 0.1, x, y), deck)
        r.check(f"insert_pilot_walls_{x:+.0f}_{y:+.0f}", f > 0.97 and open_pilot < 0.01, wall_fraction=f, material_in_pilot_mm3=open_pilot)

    # 3. Engagement: M3 thread inside each insert; M2 thread in each boss pilot.
    for (x, y), length, ins in [*[(p, 6.0, m["insert_rear"]) for p in m["fix_rear"]], *[(p, 8.0, m["insert_front"]) for p in m["fix_front"]]]:
        tip = top - length
        engage = min(z0, z0) - max(tip, z0 - ins[2])
        r.check(f"m3_thread_in_insert_{x:+.0f}_{y:+.0f}", engage >= 3.0 and tip >= z0 - ins[2] - 0.6, engaged_mm=engage, insert_mm=ins[2], tip_z=tip)
    board_top = entry.TUB_BOARD_Z + entry.PCB_T
    tip = board_top - m["screw_len"]
    pilot_bottom = top + m["boss"][1] - m["pilot"][1]
    r.check("m2_boss_engagement", (entry.TUB_BOARD_Z - tip) >= 3.0 and tip > pilot_bottom + 0.2,
            engaged_mm=entry.TUB_BOARD_Z - tip, tip_z=tip, pilot_bottom_z=pilot_bottom, plate_bottom_z=z0)
    bosses = entry.tub_bosses()
    holes = [h for _, loc in entry.tub_module_frames() for h in (entry._world(loc, *p)[:2] for p in entry.VENDOR_HOLES["S18V20X"])]
    err = max(min(((bx - hx) ** 2 + (by - hy) ** 2) ** 0.5 for bx, by in bosses) for hx, hy in holes)
    r.check("bosses_on_module_holes", err < 1e-6, worst_offset_mm=err, bosses=len(bosses))

    # 4. Static clearance of every new part against the rest of the robot (0.2 mm), own parts excluded.
    subjects = [lf for lf in C.own(leaves, *OWN) if C.is_part(lf.path)]
    for lf in subjects:
        hits = C.clashes(lf.shape, leaves, skip=OWN + ("CHASSIS_FRAME_FRONT_MODULE",) if "INSERT" in lf.label or "SCREW" in lf.label else OWN)
        gap, near = C.min_gap(lf.shape, leaves, skip=OWN + (("CHASSIS_FRAME_FRONT_MODULE",) if lf.label.startswith(("TUB_BAY_MODULE_PLATE", "TUB_BAY_DECK", "TUB_BAY_PLATE")) else ()))
        r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)

    # 5. Modules stay under the signal trunks; wire room at both terminal ends.
    trunk_z = min(C.find(leaves, t).box[2] for t in TRUNKS)
    mod_top = max(lf.box[5] for lf in leaves if "S18V20ALV" in lf.label)
    r.check("modules_under_signal_trunks", mod_top <= trunk_z - 0.3, module_top_z=mod_top, trunk_bottom_z=trunk_z)
    for name, x0 in m["modules"]:
        for sy in (1, -1):
            box = C.blk((x0, x0 + 20.96, *sorted((sy * 21.6, sy * 27.6)), entry.TUB_BOARD_Z, entry.TUB_BOARD_Z + 9.6))
            hits = C.clashes(box, leaves, skip=OWN)
            r.check(f"terminal_wire_room_{name}_{'+' if sy > 0 else '-'}y", not hits, box_6mm=hits)

    # 6. The plate and modules go on from above with the body off: chassis parts only.
    chassis_side = ("CHASSIS_V1_REFERENCE", "M7 IMU", "M12_JST_PA_3P")
    body_off = [lf for lf in leaves if any(k in "/".join(lf.path) for k in chassis_side)]
    group = [(lf.label, lf.shape) for lf in subjects if "SCREW" not in lf.label and "INSERT" not in lf.label]
    hit = C.sweep(group, body_off, (0, 0, 1), [0.5 + 1.0 * k for k in range(40)], skip=OWN + ("CHASSIS_FRAME_FRONT_MODULE",))
    r.check("plate_lowers_onto_deck_body_off", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
