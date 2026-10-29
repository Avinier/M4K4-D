"""Wheel print fixes (D-070): hub-cap pegs moved onto the hub, the tyre's print state, and
the print orientations, measured on the chassis tree with the droid edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis tree only, about 1 min.

Wheel frame as in wheel_model.py: axis Y, +y outboard; on the droid Y = +-(85 + y),
Z = 42 + z. Checks:

1. Cap: no material below its underside (y 12), so it prints underside down; the old
   pegs and the column stub are gone; the two holes are open, roofed and walled by bosses.
2. Hub: the old holes are filled and the two pegs stand on the face.
3. Assembly: cap, rim, wheel screws and cap screw do not overlap; peg-in-hole clearances.
4. Print orientation: the rim lip side down and the cap underside down leave only the
   faces listed as overhangs (rim: spoke backs and hub web; cap: bridges).
5. One print serves both sides: right rim, ring and cap are the left ones turned over
   about an axis across the wheel; the right tyre is the left one moved across, unturned.
6. Tyre print state: Ø73.6 bore, 19.3 wide, the keys still clear the ribs, and the
   assembled tyre is unchanged.
7. Planted: the subsystem cap, without the edits, fails check 1.
"""

import importlib.util
import math
from pathlib import Path
import sys

from build123d import Axis, Cylinder, GeomType, Location

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

M = entry.WHEEL_PEGS
TOL = 1e-3
results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")


def leaves(node, loc=Location(), out=None):
    out = {} if out is None else out
    kids = list(node.children) if getattr(node, "children", None) else []
    here = loc * node.location
    if kids:
        for kid in kids:
            leaves(kid, here, out)
    elif (node.label or "").startswith("WHEEL_"):
        out[node.label] = node.moved(loc)
    return out


def vol(shape):
    if shape is None:
        return 0.0
    return sum(s.volume for s in shape.solids()) if shape.solids() else 0.0


def common(a, b):
    return vol(a & b)


def cyl(side, r, y0, y1, angle=None):
    x = z = 0.0
    if angle is not None:
        x, z = M["r"] * math.sin(math.radians(angle)), M["r"] * math.cos(math.radians(angle))
    return entry._wheel_cyl(side, r, y0, y1, x, z)


def downward_faces(shape, bed_y, side):
    """Planar faces that point at the bed but are above it; the part rises toward side * +Y."""
    out = []
    for face in shape.faces():
        if face.geom_type != GeomType.PLANE:
            continue
        n, c = face.normal_at(face.center()), face.center()
        if abs(n.Y + side) < TOL and abs(c.Y - bed_y) > TOL:
            out.append((round(side * c.Y - 85.0, 2), round(face.area, 1)))
    return out


def ycyl(r, y0, y1):
    """Cylinder on the axis in the wheel frame (origin on the wheel centre)."""
    return Cylinder(r, y1 - y0, rotation=(90, 0, 0)).moved(Location((0.0, (y0 + y1) / 2.0, 0.0)))


def sym_diff(a, b):
    return vol(a - b) + vol(b - a)


def main():
    raw = B.chassis_v1_reference()
    parts = leaves(entry._apply_droid_cuts(raw, strict=False))
    before = leaves(B.chassis_v1_reference())
    f, depth, peg_len = M["face"], M["depth"], M["peg_len"]

    for side, tag in ((1, "L"), (-1, "R")):
        cap, rim = parts[f"WHEEL_{tag}_HUB_CAP_PETG"], parts[f"WHEEL_{tag}_RIM_PETG"]
        bb = cap.bounding_box()
        under = side * (bb.min.Y if side > 0 else bb.max.Y) - 85.0
        check(f"{tag} cap underside flat at y 12", abs(under - f) < TOL, f"lowest cap material at y {under:.3f}")
        stub = sum(common(cap, cyl(side, M["peg"] + 0.05, f - peg_len - 0.1, f, a)) for a in M["angles"])
        stub += common(cap, cyl(side, M["column"][0], M["column"][1], f))
        check(f"{tag} cap: old pegs and column stub gone", stub < TOL, f"{stub:.4f} mm3 below y 12")
        open_ = sum(common(cap, cyl(side, M["hole"] - 0.01, f, f + depth - 0.01, a)) for a in M["angles"])
        roof = sum(common(cap, cyl(side, M["hole"], f + depth, M["recess_top"], a)) for a in M["angles"])
        roof_full = 2 * math.pi * M["hole"] ** 2 * (M["recess_top"] - f - depth)
        check(f"{tag} cap: Ø{2 * M['hole']:.1f} x {depth} holes open and roofed", open_ < TOL and abs(roof - roof_full) < 0.01,
              f"{open_:.4f} mm3 in the holes; roof {roof:.3f}/{roof_full:.3f} mm3")
        wall = sum(common(cap, cyl(side, M["boss"] - 0.01, f + 0.01, M["recess_top"] - 0.01, a)
                          - cyl(side, M["hole"] + 0.01, f, M["recess_top"], a)) for a in M["angles"])
        wall_full = 2 * math.pi * ((M["boss"] - 0.01) ** 2 - (M["hole"] + 0.01) ** 2) * (M["recess_top"] - f - 0.02)
        check(f"{tag} cap: {M['boss'] - M['hole']:.2f} mm wall round each hole", abs(wall - wall_full) < 0.02,
              f"{wall:.3f}/{wall_full:.3f} mm3 solid")
        col = common(cap, cyl(side, 4.5, f + 0.01, M["recess_top"] - 0.01) - cyl(side, 1.7, f, M["recess_top"]))
        check(f"{tag} cap: screw column kept above y 12", col > 0.9 * math.pi * (4.5 ** 2 - 1.7 ** 2) * 1.88,
              f"{col:.1f} mm3")

        fill = sum(common(rim, cyl(side, M["hole"] - 0.01, f - depth, f - 0.01, a)) for a in M["angles"])
        fill_full = 2 * math.pi * (M["hole"] - 0.01) ** 2 * (depth - 0.01)
        check(f"{tag} hub: old holes filled", abs(fill - fill_full) < 0.01, f"{fill:.3f}/{fill_full:.3f} mm3")
        pegs = sum(common(rim, cyl(side, M["peg"] - 0.01, f + 0.01, f + peg_len - 0.01, a)) for a in M["angles"])
        pegs_full = 2 * math.pi * (M["peg"] - 0.01) ** 2 * (peg_len - 0.02)
        above = sum(common(rim, cyl(side, M["peg"] + 0.05, f + peg_len + 0.01, f + peg_len + 1.0, a)) for a in M["angles"])
        check(f"{tag} hub: Ø{2 * M['peg']:.1f} x {peg_len} pegs on the face", abs(pegs - pegs_full) < 0.01 and above < TOL,
              f"{pegs:.3f}/{pegs_full:.3f} mm3; {above:.4f} above")

        others = {k: v for k, v in parts.items() if k.startswith(f"WHEEL_{tag}_") and k != f"WHEEL_{tag}_HUB_CAP_PETG"
                  and ("RIM" in k or "SCREW_M3X6" in k or "CAP_SCREW" in k or "STUB" in k)}
        clash = {k: common(cap, v) for k, v in others.items()}
        clash = {k: v for k, v in clash.items() if v > TOL}
        check(f"{tag} cap clear of rim, pegs, wheel screws, cap screw and stub", not clash,
              f"{len(others)} parts; overlaps {clash or 'none'}")

        rim_down = downward_faces(rim, side * 73.0, side)
        levels = sorted({y for y, _ in rim_down})
        check(f"{tag} rim, lip side down: overhangs only on spoke backs (y 5) and hub web (y 8)",
              set(levels) <= {5.0, 8.0}, f"{[(y, round(sum(a for yy, a in rim_down if yy == y))) for y in levels]} (y, mm2)")
        cap_down = downward_faces(cap, side * 97.0, side)
        levels = sorted({y for y, _ in cap_down})
        check(f"{tag} cap, underside down: only the recess roof and hole roofs (bridges)",
              set(levels) <= {round(f + depth, 2), M["recess_top"]},
              f"{[(y, round(sum(a for yy, a in cap_down if yy == y), 1)) for y in levels]} (y, mm2); "
              f"widest bridge {11.2 - 4.5:.1f} mm, column to recess wall")

    old = before["WHEEL_L_HUB_CAP_PETG"].bounding_box().min.Y - 85.0
    check("planted: the unedited cap fails the flat-underside test", old < f - 1.0,
          f"subsystem cap reaches y {old:.2f} (pegs), 1.5 mm below its underside")

    radial, end = M["hole"] - M["peg"], depth - peg_len
    check("peg fit", abs(radial - 0.15) < TOL and abs(end - 0.3) < TOL, f"{radial:.2f} mm radial, {end:.2f} mm at the tip")

    flip = Axis((0.0, 0.0, 42.0), (math.sin(math.radians(120.0)), 0.0, math.cos(math.radians(120.0))))
    for name in ("RIM_PETG", "CLAMP_RING_PETG", "HUB_CAP_PETG"):
        d = sym_diff(parts[f"WHEEL_L_{name}"].rotate(flip, 180.0), parts[f"WHEEL_R_{name}"])
        check(f"one {name} print for both sides", d < 0.05, f"right = left turned over: {d:.4f} mm3 different")
    # The tyre is symmetric about its mid-plane, so the right one is the left one moved across
    # unturned: the same face is +Y on both, and both chevrons lead forward at the top.
    d = sym_diff(parts["WHEEL_L_TYRE_TPU95A_L"].moved(Location((0.0, -169.0, 0.0))), parts["WHEEL_R_TYRE_TPU95A_R"])
    check("one tyre print for both sides", d < 0.05, f"right = left moved across, not turned: {d:.4f} mm3 different")

    tyre = entry.wheel_tyre_print()
    bb = tyre.bounding_box()
    width = bb.max.Y - bb.min.Y
    bore = min(math.hypot(v.X, v.Z) for v in tyre.vertices())
    stretch = (37.0 - bore) / bore * 100.0
    check("tyre print state", abs(width - 19.3) < TOL and abs(bore - 36.8) < TOL and abs(bb.max.X - 42.0) < 0.01,
          f"bore Ø{2 * bore:.2f} (stretch {stretch:.2f} % onto Ø74), width {width:.2f} (0.30 squeeze), OD {2 * bb.max.X:.2f}")
    rim_w = parts["WHEEL_L_RIM_PETG"].moved(Location((0.0, -85.0, -42.0)))
    over = tyre & rim_w
    flank = common(over, ycyl(40.0, -10.0, 9.0) - ycyl(37.01, -10.0, 9.0))
    lip = common(over, ycyl(40.0, -10.2, -10.0) - ycyl(37.0, -10.2, -10.0))
    check("tyre print state: the keys still clear the ribs", flank < TOL,
          f"overlap with the rim over the seat outside R 37.01: {flank:.4f} mm3; bore stretch and lip squeeze "
          f"{vol(over):.1f} mm3, of it {lip:.1f} at the lip")
    same = all(sym_diff(parts[k], before[k]) < TOL for k in ("WHEEL_L_TYRE_TPU95A_L", "WHEEL_R_TYRE_TPU95A_R"))
    check("assembled tyres unchanged", same, "the droid shows the fitted state")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
