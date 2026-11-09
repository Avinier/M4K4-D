"""Pre-footprint FH34SRJ-22S envelope probe for PCB-08.

The boxes use Hirose's 13 x 3.8 x 1.0 mm *body* dimensions and a
11.5 mm-wide, 0.3 mm-thick straight cable-exit reserve. They are not the
land pattern, opened actuator, cable bend, or a populated-board fit check.
Run from this folder with the legacy CAD runtime described in ../README.md.
"""

import module_checks as C

BOARD = (10.0, 20.0, -42.0, -24.5, 112.0, 113.6)
SKIP = ("YAW_JUNCTION_PCB08_BOARD", "YAW_JUNCTION_PCB08_FFC_EXTENSION")


def overlap(a, b):
    return all(a[i] < b[i + 1] and b[i] < a[i + 1] for i in (0, 2, 4))


def within_xy(box):
    return BOARD[0] <= box[0] and box[1] <= BOARD[1] and BOARD[2] <= box[2] and box[3] <= BOARD[3]


def main():
    _entry, _tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_zif_envelopes")

    # Both same-face bodies can occupy X, but the inner cable's straight
    # stiffened exit intersects the outer connector. An immediate climb
    # cannot be assumed because the stiffener has to remain parallel.
    inner = (10.3, 14.1, -40.0, -27.0, 113.6, 114.6)
    outer = (16.0, 19.8, -40.0, -27.0, 113.6, 114.6)
    inner_exit = (14.1, 25.0, -39.25, -27.75, 113.95, 114.25)
    r.check("same_face_body_boxes_fit", within_xy(inner) and within_xy(outer) and not overlap(inner, outer), boxes=[inner, outer])
    r.check("same_face_stiffened_exit_blocked", overlap(inner_exit, outer), inner_exit=inner_exit, outer_body=outer)
    # Turn the inner ZIF 180 degrees so its cable leaves toward -X. This
    # avoids the other body, but may conflict with the existing main-board
    # connectors or require an FFC U-turn back toward the cassette.
    inward_exit = (4.0, 10.3, -39.25, -27.75, 113.95, 114.25)
    inward_hits = C.clashes(C.blk(inward_exit), leaves, skip=SKIP)
    r.check("opposed_mouth_inward_exit_clear_of_robot", not inward_hits and not overlap(inward_exit, outer), clashes=inward_hits, box=inward_exit)

    # Back-to-back candidate: both mouths face +X. The 0.3 mm cable strips
    # remain on opposite faces; the bottom connector tests the Z < 112 mm
    # clearance that the placeholder did not model.
    top = (16.0, 19.8, -40.0, -27.0, 113.6, 114.6)
    bottom = (16.0, 19.8, -40.0, -27.0, 111.0, 112.0)
    top_exit = (19.8, 25.0, -39.25, -27.75, 113.95, 114.25)
    bottom_exit = (19.8, 25.0, -39.25, -27.75, 111.35, 111.65)
    r.check("back_to_back_bodies_on_extension", within_xy(top) and within_xy(bottom) and not overlap(top, bottom), boxes=[top, bottom])
    for name, box in (("top_body", top), ("bottom_body", bottom), ("top_exit", top_exit), ("bottom_exit", bottom_exit)):
        hits = C.clashes(C.blk(box), leaves, skip=SKIP)
        gap, near = C.min_gap(C.blk(box), leaves, skip=SKIP)
        r.check(f"{name}_clear_of_robot_envelopes", not hits, clashes=hits, nearest=near, min_gap=gap, box=box)
    r.finish()


if __name__ == "__main__":
    main()
