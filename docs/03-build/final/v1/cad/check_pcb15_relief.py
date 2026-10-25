"""D-059: measure the PCB-15 component relief that DROID_CUTS cuts from the nose seat.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds only the chassis tree (about 40 s), not the whole droid.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Vector

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

RELIEF = (125.7, 126.6, 7.8, 12.2, 30.3, 35.01)
SLOT_BACK_X = 126.5  # back wall of the board slot (board X 126.6 less 0.1 clearance)
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
    top = 35.0
    # Box less the slot strip and the groove it overlaps: anything less means it opened another cavity.
    expected = (x1 - x0) * (y1 - y0) * (top - z0) - (x1 - SLOT_BACK_X) * (y1 - y0) * (top - z0) \
        - (SLOT_BACK_X - x0) * (y1 - GROOVE[0]) * (top - GROOVE[2])
    removed = seat0.volume - seat.volume
    left = seat & entry._cut_box(*RELIEF)
    left = left.volume if left else 0.0
    # A 0.6 mm shell around the pocket must still be solid.
    shell = [(x0 - 0.6, 7.2 + 0.4 * i, 30.6 + 0.5 * k) for i in range(15) for k in range(9)]
    shell += [(x, y, 30.6 + 0.5 * k) for x in (125.9, 126.3) for y in (y0 - 0.6, y1 + 0.6) for k in range(9)]
    shell += [(x, 7.2 + 0.4 * i, z0 - 0.6) for x in (125.1, 125.9, 126.3) for i in range(15)]
    holes = [p for p in shell if not _in_groove(p[1], p[2]) and not seat.is_inside(Vector(*p))]
    backed = [seat.is_inside(Vector(SLOT_BACK_X - 0.05, y, 32.0)) for y in (7.3, 12.7)]
    gap = board.distance(seat)
    print(f"removed {removed:.3f} mm3 (expected {expected:.3f}); seat left in relief {left:.4f} mm3")
    print(f"shell holes {len(holes)}; board ends backed {backed}; board-to-seat gap {gap:.3f} mm")
    ok = abs(removed - expected) < 0.01 and left < 1e-6 and not holes and all(backed) and gap > 0.09
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
