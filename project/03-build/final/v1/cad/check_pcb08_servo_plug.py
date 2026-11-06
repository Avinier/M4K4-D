"""D-095 (D-093): room on PCB-08's placeholder for the yaw servo plug moved from PCB-03 J3-5.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 1 min.
Measures: J8-3/J8-5 gone, the Feetech 5264-3P header on the board inside its outline, header and
mated plug clear of the robot (yaw cassette, risers and the C3 DevKitC included), and a straight
pull path for the plug.
"""

import module_checks as C

OWN = ("YAW_JUNCTION_J8_8_",)


def main():
    entry, tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_servo_plug")
    gone = [lf.label for lf in leaves if "YAW_JUNCTION_J8_3" in lf.label or "YAW_JUNCTION_J8_5" in lf.label]
    r.check("sideband_headers_removed", not gone, left=gone)
    board = C.find(leaves, "YAW_JUNCTION_PCB08_BOARD").box
    hdr = C.find(leaves, "YAW_JUNCTION_J8_8_FEETECH_5264_3P_HEADER")
    inside = board[0] <= hdr.box[0] and hdr.box[3] <= board[3] and board[1] <= hdr.box[1] and hdr.box[4] <= board[4] and abs(hdr.box[2] - board[5]) < 0.01
    r.check("header_on_board_outline", inside, header=[round(v, 2) for v in hdr.box], board=[round(v, 2) for v in board])
    for label in ("YAW_JUNCTION_J8_8_FEETECH_5264_3P_HEADER", "YAW_JUNCTION_J8_8_YAW_SERVO_5264_3P_MATED_PLUG"):
        lf = C.find(leaves, label)
        skip = OWN + (("YAW_JUNCTION_PCB08_BOARD",) if "HEADER" in label else ())
        hits = C.clashes(lf.shape, leaves, skip=skip)
        gap, near = C.min_gap(lf.shape, leaves, skip=skip)
        r.check(f"clear_{label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)
    plug = C.find(leaves, "YAW_JUNCTION_J8_8_YAW_SERVO_5264_3P_MATED_PLUG")
    hit = C.sweep([(plug.label, plug.shape)], leaves, (0, 0, 1), [0.5 + k for k in range(6)], skip=OWN)
    r.check("plug_pulls_straight_up_6mm", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
