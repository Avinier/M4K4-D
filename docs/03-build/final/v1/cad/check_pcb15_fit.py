"""PCB-15 stage-1 fit: place the KiCad board STEP in the nose seat and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds only the chassis tree (about 40 s), not the whole droid.

KiCad's STEP has the board core at Z 0..0.71 (copper not modelled), Y flipped, and the
board outline at KiCad x 100..106, y 100..104.6 (04-pcbs/pcb-15-nose-hall/README.md).
It is placed with STEP X -> world Y, STEP Y -> world Z, STEP Z -> world X, the core
centred on the board's nominal mid-plane (world X 126.6 since D-063).
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Plane, import_step

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

BOARD_STEP = Path(__file__).resolve().parents[3] / "04-pcbs/pcb-15-nose-hall/cad/pcb-15-nose-hall-revA.step"
CORE = 0.71                     # board core thickness in the STEP
MID_X = 126.6                   # nominal board mid-plane: D-063 board X 126.2..127.0
TRAVEL = 3.0                    # TACTILE_NOSE_TRAVEL: cap rest to the pod-face stop
POD_FACE_X = 128.5              # BALL_POD_X[1]: the stop plane
PLACE = Location(Plane(origin=(MID_X - CORE / 2.0, -93.0, 135.0), x_dir=(0, 1, 0), z_dir=(1, 0, 0)))


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


def _vol(shape):
    return shape.volume if shape else 0.0


def main():
    tree = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference()]), strict=False)
    seat = _part(tree, "BALL_POD_PRINTED_SEAT")
    magnet = _part(tree, "BALL_NOSE_MAGNET_D3X1P5_N35").moved(Location((-TRAVEL, 0, 0)))
    cap = _part(tree, "BALL_NOSE_TOUCH_CAP").moved(Location((-TRAVEL, 0, 0)))

    board = import_step(str(BOARD_STEP))
    parts = {}
    for child in board.children:
        solid = Compound(child.solids()).moved(PLACE)  # flatten: booleans on nested STEP children misbehave
        name = "PCB" if child.label.endswith("_PCB") else child.label
        parts.setdefault(name, []).append(solid)

    ok = True
    for name, solids in parts.items():
        for i, s in enumerate(solids):
            bb = s.bounding_box()
            clash = _vol(s & seat)
            gap = s.distance(seat)
            print(f"{name}[{i}] X {bb.min.X:.3f}-{bb.max.X:.3f} Y {bb.min.Y:.3f}-{bb.max.Y:.3f} "
                  f"Z {bb.min.Z:.3f}-{bb.max.Z:.3f}  seat clash {clash:.4f} mm3, gap {gap:.3f} mm")
            ok &= clash < 1e-6

    u1 = parts["SOT-23"][0]
    top = u1.bounding_box().max.X
    m_clash, c_clash = _vol(u1 & magnet), _vol(u1 & cap)
    print(f"U1 model top X {top:.3f}; pod-face stop X {POD_FACE_X:.3f}; air at the stop {POD_FACE_X - top:+.3f} mm")
    print(f"U1 vs magnet at the stop: clash {m_clash:.4f} mm3; vs cap at the stop: clash {c_clash:.4f} mm3")
    # Analytic bounds for the real part (TI DBZ0003A: body 1.12 max; board 0.8 +-10 % in the
    # 1.0 mm slot X 126.1-127.1 of D-063).
    copper, solder = 0.035, 0.05
    nominal = MID_X + 0.4 + copper + 0.03 + 1.0
    worst = 127.1 + copper + solder + 1.12
    print(f"real U1 top: nominal {nominal:.3f} (air {POD_FACE_X - nominal:+.3f}); "
          f"worst, board against the front slot wall {worst:.3f} (air {POD_FACE_X - worst:+.3f})")
    ok &= m_clash < 1e-6 and c_clash < 1e-6 and POD_FACE_X - top > 0.0 and POD_FACE_X - worst > 0.0
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
