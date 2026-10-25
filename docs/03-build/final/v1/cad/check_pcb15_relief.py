"""D-059/D-063: measure the PCB-15 relief and moved slot that DROID_CUTS/ADDS make in the nose seat.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds only the chassis tree (about 40 s), not the whole droid.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Vector

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

RELIEF = (125.3, 126.6, 7.8, 12.2, 30.3, 35.01)   # D-059, deepened 0.4 by D-063
BACK = (126.1, 126.5, 6.9, 13.1, 30.3, 35.01)     # D-063: slot back wall moved 0.4 back
FRONT = [(127.1, 127.5, 6.9, 8.3, 30.3, 35.0), (127.1, 127.5, 11.7, 13.1, 30.3, 35.0)]  # D-063 front wall
SLOT_BACK_X = 126.1  # back wall of the board slot (board X 126.2 less 0.1 clearance)
OLD_SLOT_X = (126.5, 127.5)  # the subsystem's slot, which the cuts open into
GROOVE = (9.5, 12.5, 33.5)  # lead groove behind the board: y0, y1, z0 (open to the seat top)


def _leaves(node, loc=Location()):
    here = loc * node.location
    kids = list(node.children) if getattr(node, "children", None) else []
    if not kids:
        yield node, loc
    for kid in kids:
        yield from _leaves(kid, here)


def _part(tree, label):
    found = [(n, l) for n, l in _leaves(tree) if n.label == label]
    assert len(found) == 1, (label, len(found))
    node, loc = found[0]
    return node.moved(loc)


def _in_groove(y, z):
    return GROOVE[0] <= y <= GROOVE[1] and z >= GROOVE[2]


def main():
    seat0 = _part(Compound(children=[entry.chassis_v1_reference()]), "BALL_POD_PRINTED_SEAT")
    after = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference()]))
    seat, board = _part(after, "BALL_POD_PRINTED_SEAT"), _part(after, "BALL_NOSE_HALL_CARRIER_PCB")
    x0, x1, y0, y1, z0, z1 = RELIEF
    bx0, bx1, by0, by1 = BACK[:4]
    top, h, hg = 35.0, 35.0 - z0, 35.0 - GROOVE[2]
    # Relief and back-wall boxes, less the old slot strip and the groove they overlap, less the
    # front-wall boxes added back into the old slot: any other figure means another cavity opened.
    union_xy = (x1 - x0) * (y1 - y0) + (bx1 - bx0) * (by1 - by0) - (bx1 - bx0) * (y1 - y0)
    in_slot = (x1 - OLD_SLOT_X[0]) * (y1 - y0)
    in_groove = (x1 - x0) * (y1 - GROOVE[0]) + (bx1 - bx0) * (GROOVE[1] - y1) - (x1 - OLD_SLOT_X[0]) * (y1 - GROOVE[0])
    added = sum((b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4]) for b in FRONT)
    expected = (union_xy - in_slot) * h - in_groove * hg - added
    removed = seat0.volume - seat.volume
    left = sum((seat & entry._cut_box(*b)).volume if (seat & entry._cut_box(*b)) else 0.0 for b in (RELIEF, BACK))
    walls = [seat.is_inside(Vector(127.3, y, z)) for y in (7.3, 12.7) for z in (30.6, 32.6, 34.7)]
    notch_open = not seat.is_inside(Vector(127.3, 10.0, 32.6))
    # A 0.6 mm shell around the pocket must still be solid.
    shell = [(x0 - 0.6, 7.2 + 0.4 * i, 30.6 + 0.5 * k) for i in range(15) for k in range(9)]
    shell += [(x, y, 30.6 + 0.5 * k) for x in (125.5, 125.9) for y in (y0 - 0.6, y1 + 0.6) for k in range(9)]
    shell += [(x, 7.2 + 0.4 * i, z0 - 0.6) for x in (125.5, 125.9, 126.3) for i in range(15)]
    holes = [p for p in shell if not _in_groove(p[1], p[2]) and not seat.is_inside(Vector(*p))]
    backed = [seat.is_inside(Vector(SLOT_BACK_X - 0.05, y, 32.0)) for y in (7.3, 12.7)]
    gap = board.distance(seat)
    print(f"removed {removed:.3f} mm3 (expected {expected:.3f}); seat left in relief {left:.4f} mm3")
    print(f"shell holes {len(holes)}; board ends backed {backed}; board-to-seat gap {gap:.3f} mm")
    print(f"front wall solid {walls}; notch open {notch_open}; board X {board.bounding_box().min.X:.3f}-{board.bounding_box().max.X:.3f}")
    ok = abs(removed - expected) < 0.01 and left < 1e-6 and not holes and all(backed) and gap > 0.09 \
        and all(walls) and notch_open
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
