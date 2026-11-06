"""D-095 (D-093 Q9): the Adafruit LSM6DSOX on its printed adapter at the J15A holes.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: the adapter seated on the deck, coaxial with the D-075 J15A pilots, J15A screw and board
screw engagement, the chip's place against PCB-07's, every part clear of the robot (tub-bay plate
included), wire room over both header rows, and the board going on from above (body off).
"""

import module_checks as C

OWN = ("IMU_ADAPTER_LSM6DSOX", "M7 IMU")
PCB07_CHIP = (21.0, 0.0)


def main():
    entry, tree, leaves = C.droid_tree()
    m = entry.IMU
    r = C.Report("check_imu_adapter")
    adapter = C.find(leaves, "IMU_ADAPTER_LSM6DSOX").shape
    deck = C.find(leaves, "CHASSIS_FRAME_FRONT_MODULE").shape
    ov = C.common(adapter, deck)
    r.check("adapter_on_deck", ov < 0.01 and C.distance(adapter, deck) < 0.01, overlap_mm3=ov)
    for x, y in m["j15a"]:
        pilot_open = C.common(entry._z_cyl(0.75, 52.1, 55.9, x, y), deck)
        wall = C.frac_inside(entry._z_cyl(2.0, 52.05, 55.95, x, y) - entry._z_cyl(0.8, 51, 57, x, y), deck)
        r.check(f"j15a_pilot_{y:+.1f}", pilot_open < 0.01 and wall > 0.97, material_in_pilot=pilot_open, wall_fraction=wall)
    at = m["adapter"][5]
    tip = at - m["j15a_screw"]
    r.check("j15a_screw_engagement", 56.0 - tip >= 3.5 and tip >= 51.9, engaged=56.0 - tip, tip_z=tip)
    board_top = entry.IMU_BOARD_Z + m["board"][2]
    tip = board_top - 5.0
    r.check("board_screw_engagement", entry.IMU_BOARD_Z - tip >= 3.0 and tip >= m["adapter"][4] + 0.2 + 0.2, engaged=entry.IMU_BOARD_Z - tip, tip_z=tip)
    chip = C.find(leaves, "M7_LSM6DSOX_LGA14").box
    cx, cy = (chip[0] + chip[3]) / 2, (chip[1] + chip[4]) / 2
    off = ((cx - PCB07_CHIP[0]) ** 2 + (cy - PCB07_CHIP[1]) ** 2) ** 0.5
    r.check("chip_near_pcb07_chip", off <= 1.0, chip_xy=(cx, cy), offset_mm=off)

    subjects = [lf for lf in C.own(leaves, *OWN) if C.is_part(lf.path)]
    for lf in subjects:
        skip = OWN + (("CHASSIS_FRAME_FRONT_MODULE",) if lf.label.startswith(("IMU_ADAPTER", "M7_J15A")) else ())
        hits = C.clashes(lf.shape, leaves, skip=skip)
        gap, near = C.min_gap(lf.shape, leaves, skip=skip)
        r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)
    x1, bw = m["board_x1"], m["board"][0]
    for name, v in (("JP1_front", 2.54), ("JP2_rear", 15.24)):
        x = x1 - v
        band = C.blk((x - 1.5, x + 1.5, -bw / 2 + 2.0, bw / 2 - 2.0, board_top + 0.05, board_top + 6.0))
        hits = [h for h in C.clashes(band, leaves) if not h[0].startswith("M7_")]
        r.check(f"wire_room_over_{name}", not hits, clashes=hits)
    chassis_side = [lf for lf in leaves if any(k in "/".join(lf.path) for k in ("CHASSIS_V1_REFERENCE", "M2 head", "M3 yaw", "M12_JST_PA_3P"))]
    hit = C.sweep([(lf.label, lf.shape) for lf in subjects if lf.label.startswith("M7_") and "J15A" not in lf.label],
                  chassis_side, (0, 0, 1), [0.5 + k for k in range(30)], skip=OWN)
    r.check("board_goes_on_from_above", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
