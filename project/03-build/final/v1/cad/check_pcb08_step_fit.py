"""Probe the routed PCB-08 STEP against the final-v1 robot.

The KiCad STEP currently has a board core, J2 and R1. The missing J1,
J3/J4, J5 and J6 bodies keep this from being a populated fit release.
"""

from build123d import Location
from cadgen.step_scene import import_step

import module_checks as C


STEP = "../../../04-pcbs/pcb-08-yaw-junction/cad/pcb-08-yaw-junction-revA.step"
EXPECTED = {"J1", "J2", "J3", "J4", "J5", "J6", "R1"}


def box6(shape):
    b = shape.bounding_box()
    return tuple(round(v, 3) for v in (b.min.X, b.min.Y, b.min.Z,
                                        b.max.X, b.max.Y, b.max.Z))


def main():
    shape = import_step(STEP)
    parts = {c.label: c for c in shape.children if c.solids()}
    core = next(c for name, c in parts.items() if name not in EXPECTED)
    core_z = core.bounding_box().max.Z - core.bounding_box().min.Z
    # KiCad --user-origin 0x0mm: STEP X=KiCad X, Y=-KiCad Y. Nominal 1.6 mm
    # board is centred on the CAD reserve's Z 112.0..113.6 interval.
    loc = Location((-100, 100, 112.0 + (1.6 - core_z) / 2))
    _entry, _tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_step_fit")
    board = core.moved(loc)
    bb = board.bounding_box()
    r.check("board_outline_matches_cad",
            abs(bb.min.X + 22) < 0.01 and abs(bb.max.X - 20) < 0.01
            and abs(bb.min.Y + 44) < 0.01 and abs(bb.max.Y + 23) < 0.01,
            bounds=box6(board), core_thickness=round(core_z, 3))
    skip = ("YAW_JUNCTION",)
    for label, part in (("board", board), ("J2", parts["J2"].moved(loc)),
                        ("R1", parts["R1"].moved(loc))):
        hits = C.clashes(part, leaves, skip=skip)
        gap, near = C.min_gap(part, leaves, skip=skip)
        r.check(label + "_external_clearance", not hits,
                clashes=hits, nearest=near, min_gap=round(gap, 3), bounds=box6(part))
    j2 = parts["J2"].moved(loc)
    reserve = C.find(leaves, "YAW_JUNCTION_J8_4_JST_GH_BM06B_HEADER").box
    jb = j2.bounding_box()
    r.check("j2_centered_on_mated_plug_datum",
            abs((jb.min.X + jb.max.X) / 2 - (reserve[0] + reserve[3]) / 2) < 0.02
            and abs((jb.min.Y + jb.max.Y) / 2 - (reserve[1] + reserve[4]) / 2) < 0.02,
            actual=box6(j2), reserve=reserve)
    missing = sorted(EXPECTED - parts.keys())
    r.check("populated_models_present", not missing, missing=missing,
            note="J3/J4 FH34 footprints have no 3D model; J1/J5/J6 stock model files are unavailable")
    r.finish()


if __name__ == "__main__":
    main()
