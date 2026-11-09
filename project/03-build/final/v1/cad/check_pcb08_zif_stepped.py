"""PCB-08 FH34SRJ follow-up probe: Pi parts under the back-to-back ZIF, and the stepped stack.

The earlier check_pcb08_zif_envelopes.py tested the back-to-back lower ZIF
against the Pi 5 vendor STEP as one bounding box. Here the Pi's own solids
are surveyed with Bnd_Box (no booleans on vendor leaves) to find what really
sits under the extension.

Stepped stack: both ZIFs on the top face with mouths toward +X. The inner
cable leaves its stiffener straight, climbs in an S-bend and passes over the
outer ZIF's 1.0 mm body, as the stacked cassette FFCs arrive anyway. The
outer cable is latched first; the inner cable then lies over the outer
actuator. Assumed (E): 1.0 mm straight exit before bending, S-bend
radius 3.0 mm (about 10x the 0.3 mm FFC), opened back-flip actuator 1.8 mm
deep and 3.4 mm above the board. Body boxes are Hirose's 13 x 3.8 x 1.0 mm;
this is not the land pattern or a populated fit.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
"""

import math

from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer

import module_checks as C

BOARD_TOP = 113.6
EXT = (10.0, 20.0, -42.0, -24.5)            # +X FFC extension XY
MAIN = (-22.0, 10.0, -44.0, -23.0)          # main plate XY
Y0, Y1 = -40.0, -27.0                       # 13 mm ZIF width
CAB_Y = (-39.25, -27.75)                    # 11.5 mm cable
SKIP = ("YAW_JUNCTION_PCB08_BOARD", "YAW_JUNCTION_PCB08_FFC_EXTENSION", "YAW_JUNCTION_PCB08_ZIF")

DEPTH, HEIGHT = 3.8, 1.0
STIFF = 1.0                                 # E: straight exit before bending
R_BEND = 3.0                                # E: S-bend radius
ACT_D, ACT_H = 1.8, 3.4                     # E: opened actuator
CLEAR = 0.3                                 # cable over the outer body
CAB_Z = (113.95, 114.25)                    # straight cable in the mouth
X_END = 25.0                                # toward the cassette exit


def face_boxes(shape):
    """Bnd_Box of every face in a placed vendor compound (no booleans).

    Faces, not solids: vendor STEPs may carry shell-only parts that a solid
    walk would miss."""
    out = []
    ex = TopExp_Explorer(shape.wrapped, TopAbs_FACE)
    while ex.More():
        b = Bnd_Box()
        BRepBndLib.AddOptimal_s(ex.Current(), b, False, False)
        out.append(b.Get())
        ex.Next()
    return out


def s_bend_run(rise, r):
    """Horizontal length of two equal arcs of radius r climbing `rise`."""
    return 2 * math.sqrt(r * rise - rise * rise / 4)


def main():
    _entry, _tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_zif_stepped")
    print("PCB-08 leaves:", sorted({lf.label for lf in leaves if "YAW_JUNCTION" in lf.label}), flush=True)

    # 1. Pi survey under the extension: tallest real solid below the board.
    pi = C.find(leaves, "C0_RASPBERRY_PI5_EXACT_STEP")
    window = (EXT[0], X_END, CAB_Y[0], CAB_Y[1])
    under = [b for b in face_boxes(pi.shape)
             if b[0] < window[1] and window[0] < b[3] and b[1] < window[3] and window[2] < b[4]]
    top = max((b[5] for b in under), default=None)
    lower_body_z0 = 112.0 - HEIGHT
    r.check("pi_faces_found_under_extension", bool(under), count=len(under), tallest_z=top)
    r.check("back_to_back_lower_zif_clears_pi_faces", top is not None and top + 0.2 <= lower_body_z0,
            pi_top=top, lower_zif_bottom=lower_body_z0, gap=None if top is None else round(lower_body_z0 - top, 3),
            note="0.2 mm margin over the tallest Pi face in the extension window")

    # 2. Stepped stack geometry.
    rise = (BOARD_TOP + HEIGHT + CLEAR + 0.15) - sum(CAB_Z) / 2
    run = s_bend_run(rise, R_BEND)
    outer = (EXT[1] - 0.5 - DEPTH, EXT[1] - 0.5, Y0, Y1, BOARD_TOP, BOARD_TOP + HEIGHT)
    inner_x1 = outer[0] - ACT_D - run - STIFF       # bend ends before the outer actuator zone
    inner = (inner_x1 - DEPTH, inner_x1, Y0, Y1, BOARD_TOP, BOARD_TOP + HEIGHT)
    raised = (BOARD_TOP + HEIGHT + CLEAR, BOARD_TOP + HEIGHT + CLEAR + 0.3)
    inner_stiff = (inner[1], inner[1] + STIFF, *CAB_Y, *CAB_Z)
    inner_bend = (inner[1] + STIFF, inner[1] + STIFF + run, *CAB_Y, CAB_Z[0], raised[1])
    inner_over = (inner[1] + STIFF + run, X_END, *CAB_Y, *raised)
    outer_exit = (outer[1], X_END, *CAB_Y, *CAB_Z)
    act_outer = (outer[0] - ACT_D, outer[0], Y0, Y1, BOARD_TOP, BOARD_TOP + ACT_H)
    act_inner = (inner[0] - ACT_D, inner[0], Y0, Y1, BOARD_TOP, BOARD_TOP + ACT_H)

    def on_board(b):
        in_ext = EXT[0] <= b[0] and b[1] <= EXT[1] and EXT[2] <= b[2] and b[3] <= EXT[3]
        in_main = MAIN[0] <= b[0] and b[1] <= MAIN[1] and MAIN[2] <= b[2] and b[3] <= MAIN[3]
        in_both = MAIN[0] <= b[0] and b[1] <= EXT[1] and max(MAIN[2], EXT[2]) <= b[2] and b[3] <= min(MAIN[3], EXT[3])
        return in_ext or in_main or in_both

    r.check("stepped_geometry", on_board(inner) and on_board(outer) and on_board(act_inner),
            rise=round(rise, 3), s_bend_run=round(run, 3), inner_body=inner, outer_body=outer,
            inner_actuator_open=act_inner,
            note="inner body straddles the main plate and extension; keep that XY free in the layout")
    # The Hirose solder tabs extend 0.15 mm beyond the 3.8 mm housing in the
    # insertion direction. Enforce D-062's 0.3 mm copper-to-edge rule.
    outer_tab_edge = outer[1] + 0.15
    r.check("outer_solder_tab_within_board", outer_tab_edge + 0.3 <= EXT[1] + 1e-6,
            tab_edge=round(outer_tab_edge, 3), board_edge=EXT[1],
            clearance=round(EXT[1] - outer_tab_edge, 3))
    r.check("inner_cable_over_outer_body", inner_over[0] <= act_outer[0] and inner_over[4] >= outer[5] + CLEAR - 1e-6,
            raised_from_x=round(inner_over[0], 3), raised_z=raised, outer_top=outer[5])

    for name, box in (("inner_body", inner), ("outer_body", outer), ("inner_stiffener", inner_stiff),
                      ("inner_bend", inner_bend), ("inner_raised_cable", inner_over), ("outer_cable", outer_exit),
                      ("inner_actuator_open", act_inner), ("outer_actuator_open", act_outer)):
        hits = C.clashes(C.blk(box), leaves, skip=SKIP)
        gap, near = C.min_gap(C.blk(box), leaves, skip=SKIP)
        r.check(f"{name}_clear_of_robot", not hits, clashes=hits, nearest=near, min_gap=gap, box=box)

    # 3. Room above: real solids (vendor leaves as boxes) in the column the
    # opened actuators and raised cable need; bounding boxes of large prints
    # such as the body frame would report false clashes.
    column = (act_inner[0], X_END, Y0, Y1, BOARD_TOP + HEIGHT, BOARD_TOP + ACT_H + 0.2)
    hits = C.clashes(C.blk(column), leaves, skip=SKIP)
    gap, near = C.min_gap(C.blk(column), leaves, skip=SKIP, reach=10.0)
    r.check("headroom_over_stepped_stack", not hits, clashes=hits, nearest=near, gap_from_column=gap, column=column)
    r.finish()


if __name__ == "__main__":
    main()
