"""D-086/D-087 gate: room behind PCB-02 for back-side SMD logic.

Builds the body and chassis trees the same way as check_pcb02_mount.py, then
sweeps slabs behind the board's back face (world X -49.6, normal -X) over the
board outline, minus the PCB-13 facing zone (world Y -14..14, Z <= 71.5) and
the four 3.5 mm mount keepouts, and minus the top-centre strip (world
Y -14..14, Z >= 87.5) where the rear service panel comes within 0.5 mm of the
back face (mapped 2026-11-03); that strip is a back-face no-parts zone too. A slab of depth d must not intersect any solid
except PCB-02 itself and its edge frame. Back-side parts are at most 1.2 mm
tall (SOT-23/1206); the gate is 2.0 mm (part plus 0.8 mm). The planted case is
a slab reaching 3.0 mm into the PCB-13 zone, which must hit PCB-13.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Shape, Solid, Box, Cylinder, Pos, Rot
from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
from OCP.TopoDS import TopoDS

import body_v1_model as B

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
M = entry.PCB02_MOUNT
BACK_X = M["board"][0]                 # -49.6
GATE = 2.0
PANEL_Z0 = 87.5   # rear-panel-near strip lower edge, world Z


def place(node, loc):
    moved = node.wrapped.Moved(loc.wrapped)
    if moved.ShapeType() == TopAbs_COMPOUND:
        return Compound(TopoDS.Compound_s(moved))
    if moved.ShapeType() == TopAbs_SOLID:
        return Solid(TopoDS.Solid_s(moved))
    return Shape.cast(moved)


def leaves(node, loc=Location(), path=()):
    here = loc * node.location
    name = path + (node.label or "?",)
    kids = list(node.children) if getattr(node, "children", None) else []
    if not kids:
        yield name, node, loc
    else:
        for child in kids:
            yield from leaves(child, here, name)


def block(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def slab(depth, with_pcb13_zone=False):
    s = block(BACK_X - depth, BACK_X, -25.0, 25.0, M["board"][4], M["board"][5])
    if not with_pcb13_zone:
        s = s - block(BACK_X - depth - 1, BACK_X + 1, -14.0, 14.0, M["board"][4] - 1, 71.5)
        s = s - block(BACK_X - depth - 1, BACK_X + 1, -14.0, 14.0, PANEL_Z0, M["board"][5] + 1)
    for y, z in M["holes"]:
        s = s - Pos(BACK_X - depth / 2, y, z) * Rot(0, 90, 0) * Cylinder(M["courtyard_r"], depth + 2)
    return s


def vol(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def main():
    tree = entry._apply_droid_cuts(Compound(children=[B.build_body_assembly(), B.chassis_v1_reference()]), strict=False)
    solids = [(p, place(n, l)) for p, n, l in leaves(tree) if n.wrapped is not None and not n.wrapped.IsNull()]
    solids = [(p, s) for p, s in solids if "PCB02_CHARGE_AND_SYSTEM_POWER" not in "/".join(p)
              and not any(t in p[-1] for t in ("RESERVE", "CORRIDOR", "KEEP_OUT", "SWEEP"))]
    frame = entry.pcb02_mount_frame()
    ok = True
    for depth in (1.0, 1.5, GATE, 2.5, 3.0):
        s = slab(depth) - frame
        hits = [(p[-1], v) for p, x in solids if (v := vol(s, x)) > 1e-4]
        print(f"{'PASS' if not hits else 'HIT '}  depth {depth:.1f} mm behind back face: "
              + ("clear" if not hits else "; ".join(f"{n} {v:.3f} mm3" for n, v in hits[:6])), flush=True)
        if depth <= GATE and hits: ok = False
    # D-087: only 0402 R/C (<= 0.55 mm) may sit on the back inside the PCB-13 zone.
    for depth in (0.55, 1.0):
        z13 = block(BACK_X - depth, BACK_X, -14.0, 14.0, M["board"][4], 71.5) - frame
        h13 = [(p[-1], v) for p, x in solids if (v := vol(z13, x)) > 1e-4]
        print(f"{'PASS' if not h13 else 'HIT '}  PCB-13 zone, depth {depth:.2f} mm (0402 gate): "
              + ("clear" if not h13 else "; ".join(f"{n} {v:.3f} mm3" for n, v in h13[:4])), flush=True)
        ok &= not h13
    planted = slab(3.0, with_pcb13_zone=True) - frame
    phits = [p[-1] for p, x in solids if vol(planted, x) > 1e-4]
    pcb13 = any("PCB13" in n for n in phits)
    print(f"{'PASS' if pcb13 else 'FAIL'}  planted: 3.0 mm slab over the PCB-13 zone hits {phits[:4]}", flush=True)
    ok &= pcb13
    near = block(BACK_X - 1.0, BACK_X, -8.0, 8.0, 90.0, 94.0) - frame
    nhits = [p[-1] for p, x in solids if vol(near, x) > 1e-4]
    pn = any("REAR_SERVICE_PANEL" in n for n in nhits)
    print(f"{'PASS' if pn else 'FAIL'}  planted: 1.0 mm slab in the panel strip hits {nhits[:3]}", flush=True)
    ok &= pn
    print("RESULT", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
