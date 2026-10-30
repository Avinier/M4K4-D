"""Fabrication files for the axle stack's non-printed custom parts, from the final droid
geometry (D-071): the turned stub (CH-012) and the aluminium bearing cap (CH-052).

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md
(about 1 min). Writes to ../fab/:

- CH-012_stub.step: the left stub with the D-071 Ø21 flange, axis Z, the inboard
  (motor) end at z 0 and the spigot tip at z 23. The set-screw hole is on -Y. Both
  sides use the same stub. stub_drawing.py makes the shop drawing from this file.
- CH-052_cap.step and CH-052_cap.dxf: the left cap, flat in XY and 1.2 mm thick
  (z 0..1.2). The DXF is the 2D cut profile in mm (layer CUT, circles only) for
  laser or waterjet. Both sides use the same cap.

Each part is checked against the droid tree before it is written: the moved solid
must have the same volume, and the stub's extents must match its drawing frame.
"""

import math
from pathlib import Path
import importlib.util

from build123d import Axis, GeomType, Location, Plane, export_step

import body_v1_model as B

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "fab"
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

STUB_END_Y, CAP_Y0, AXLE_Z = 73.0, 86.51, 42.0


def leaves(node, loc=Location(), out=None):
    out = {} if out is None else out
    kids = list(node.children) if getattr(node, "children", None) else []
    here = loc * node.location
    if kids:
        for kid in kids:
            leaves(kid, here, out)
    else:
        out[node.label] = node.moved(loc)
    return out


def to_local(shape, y0):
    """Axis along +Z from |Y| y0; world +Z (the set-screw side) becomes local -Y."""
    return shape.moved(Location((0.0, -y0, -AXLE_Z))).rotate(Axis.X, 90.0)


def cap_dxf(cap, path):
    import ezdxf
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.layers.add("CUT", color=7)
    msp = doc.modelspace()
    circles = []
    for edge in cap.edges():
        if edge.geom_type != GeomType.CIRCLE or abs(edge.center().Z) > 1e-6:
            continue
        c, r = edge.arc_center, edge.radius
        key = (round(c.X, 4), round(c.Y, 4), round(r, 4))
        if key not in circles:
            circles.append(key)
    for x, y, r in circles:
        msp.add_circle((x, y), r, dxfattribs={"layer": "CUT"})
    doc.saveas(path)
    return circles


def main():
    OUT.mkdir(exist_ok=True)
    parts = leaves(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    stub_w, cap_w = parts["WHEEL_L_STUB_SHAFT_8MM"], parts["AXLE_BEARING_CAP_L"]
    stub, cap = to_local(stub_w, STUB_END_Y), to_local(cap_w, CAP_Y0)
    for name, a, b in (("stub", stub_w, stub), ("cap", cap_w, cap)):
        assert abs(a.volume - b.volume) < 1e-6, name
    bb = stub.bounding_box()
    assert abs(bb.min.Z) < 1e-6 and abs(bb.max.Z - 23.0) < 1e-6 and abs(bb.max.X - 10.5) < 1e-6, bb
    cb = cap.bounding_box()
    assert abs(cb.min.Z) < 1e-6 and abs(cb.max.Z - 1.2) < 1e-6 and abs(cb.max.X - 16.0) < 1e-6, cb
    # The droid's boolean leaves a nested compound that the STEP writer refuses; each
    # part is one solid, so write that.
    assert len(stub.solids()) == 1 and len(cap.solids()) == 1
    stub, cap = stub.solids()[0], cap.solids()[0]
    stub.label, cap.label = "CH-012_STUB", "CH-052_BEARING_CAP"
    export_step(stub, str(OUT / "CH-012_stub.step"))
    export_step(cap, str(OUT / "CH-052_cap.step"))
    circles = cap_dxf(cap, OUT / "CH-052_cap.dxf")
    print(f"stub: {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm, {stub.volume:.1f} mm3 "
          f"({stub.volume * 7.85e-3:.1f} g steel)")
    print(f"cap: {len(circles)} circles in the DXF:")
    for x, y, r in sorted(circles, key=lambda c: -c[2]):
        print(f"  Ø{2 * r:.2f} at ({x:.2f}, {y:.2f}), R{math.hypot(x, y):.2f}")


if __name__ == "__main__":
    main()
