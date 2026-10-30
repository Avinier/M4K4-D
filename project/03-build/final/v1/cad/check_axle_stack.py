"""Axle-stack assembly fixes (D-071): tool access, the alignment plug and print orientations,
measured on the chassis tree with the droid edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis tree twice (with and without the droid edits), about 1.5 min.

The axle is the line X 0, Z 42; |Y| runs outboard. Keys are modelled across their corners:
2 mm hex r 1.155, 1.5 mm hex r 0.87. Checks, both sides:

1. Stub flange Ø21: no steel outside R10.5 at the flange, the rest of it intact, and
   1.0 mm of steel outside the wheel-screw threads.
2. Housing screws: a straight 2 mm key reaches each one with the stub in place.
3. Housing screw holes close to Ø3.2 over the full housing; the screws stay clear.
4. Set screw: a straight 1.5 mm key from +Z is clear (wheel off).
5. Alignment plug (CH-089) in the housing: clear of every part present at that step, its
   fits, its shaft engagement, captured by the cap, and the face-screw keys clear through
   it. With the bearings and stub in place instead, those keys are blocked: the reason for it.
6. Print orientation: housing inboard face down, carrier outboard face down, plug on its
   outboard end; the faces that would need support are listed.
7. Planted: the unedited stub blocks the housing-screw key, and the unedited carrier the
   set-screw key.
8. Housing screws, M3 x 16 (D-072): the tip stays clear of the bottom of its blind hole by
   more than the worst-case stack (TIP_STACK), and a screw at its short limit still
   engages the insert by MIN_ENGAGE. Planted: the old M3 x 18 does not.
"""

import importlib.util
import math
from pathlib import Path
import sys

from build123d import Cylinder, GeomType, Location

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

M = entry.AXLE_FIX
KEY2, KEY15 = 1.155, 0.87
SCREW = "AXLE_CAP_SCREW_M3X16_"   # D-072; the subsystem tree has AXLE_CAP_SCREW_M3X18_
# Tip stack for the housing screws, mm: ISO 7380 length +0.35 (js15, 10-18 mm), 1.2 mm
# aluminium cap -0.08, and 0.5 for plastic pushed below the insert when it is melted in.
TIP_STACK = 0.35 + 0.08 + 0.5
MIN_ENGAGE = 1.5                  # thread in the insert with the screw 0.35 short: 3 pitches
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
    else:
        out[node.label] = node.moved(loc)
    return out


def vol(shape):
    try:
        return sum(s.volume for s in shape.solids())
    except Exception:
        return 0.0


def common(a, b):
    return vol(a & b)


def zcyl(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def boxes_meet(a, b):
    p, q = a.bounding_box(), b.bounding_box()
    return not (p.max.X < q.min.X or q.max.X < p.min.X or p.max.Y < q.min.Y or q.max.Y < p.min.Y
                or p.max.Z < q.min.Z or q.max.Z < p.min.Z)


def hits(tool, parts):
    out = {}
    for name, shape in parts.items():
        if boxes_meet(tool, shape):
            v = common(tool, shape)
            if v > TOL:
                out[name] = round(v, 3)
    return out


def overhangs(shape, side, bed, up):
    """Planar faces pointing at the bed but above it; the part rises toward up * side * Y."""
    res = {}
    for face in shape.faces():
        if face.geom_type != GeomType.PLANE:
            continue
        n, c = face.normal_at(face.center()), face.center()
        if abs(n.Y + up * side) < TOL and abs(c.Y - side * bed) > TOL:
            key = round(abs(c.Y), 2)
            res[key] = round(res.get(key, 0.0) + face.area, 1)
    return res


def screw_tip(tree, name, carrier, insert):
    """(tip to hole bottom, thread in the insert, plastic skin under the hole), mm.

    The hole bottom is found by probing the carrier along the screw axis, from the gearbox
    face (|Y| 69) to the tip, with a thin rod: whatever plastic it meets is the skin.
    """
    bb = tree[name].bounding_box()
    x, z, tip = bb.center().X, bb.center().Z, min(abs(bb.min.Y), abs(bb.max.Y))
    side = 1 if bb.center().Y > 0 else -1
    rod = entry._axle_cyl(side, 0.5, 69.0, tip, x, z - 42.0)
    skin = common(carrier, rod) / (math.pi * 0.25)
    ib = insert.bounding_box()
    insert_top = max(abs(ib.min.Y), abs(ib.max.Y))
    return tip - (69.0 + skin), insert_top - max(tip, min(abs(ib.min.Y), abs(ib.max.Y))), skin


def near_axle(parts, side, tag):
    """Leaves of one side's axle and wheel, by label."""
    keep = ("AXLE_", "BEARING_688ZZ", "MOTOR_", f"WHEEL_{tag}_", "J04_")
    return {k: v for k, v in parts.items() if any(t in k for t in keep) and f"_{tag}" in k}


def main():
    parts = leaves(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    before = leaves(B.chassis_v1_reference())
    r_new, a0, a1 = M["flange"]

    for side, tag in ((1, "L"), (-1, "R")):
        local = near_axle(parts, side, tag)
        stub = parts[f"WHEEL_{tag}_STUB_SHAFT_8MM"]
        wheel = {k for k in local if k.startswith(f"WHEEL_{tag}_") and "STUB" not in k and "SET_SCREW" not in k}
        wheel_off = {k: v for k, v in local.items() if k not in wheel}

        outside = common(stub, entry._axle_cyl(side, 14.0, a0, a1) - entry._axle_cyl(side, r_new + 0.01, a0 - 1, a1 + 1))
        ring = common(stub, entry._axle_cyl(side, r_new - 0.01, a0 + 0.01, a1 - 0.01) - entry._axle_cyl(side, 9.6, a0, a1))
        ring_full = math.pi * ((r_new - 0.01) ** 2 - 9.6 ** 2) * (a1 - a0 - 0.02)
        check(f"{tag} stub flange Ø{2 * r_new:.0f}", outside < TOL and abs(ring - ring_full) < 0.05,
              f"{outside:.4f} mm3 outside R{r_new}; ring R9.6-{r_new} {ring:.2f}/{ring_full:.2f} mm3; "
              f"{r_new - 8.0 - 1.5:.1f} mm of steel outside the wheel-screw threads")

        screws = [k for k in local if k.startswith(f"{SCREW}{tag}_")]
        blocked = {}
        for name in screws:
            bb = local[name].bounding_box()
            x, z = bb.center().X, bb.center().Z
            top = max(abs(bb.min.Y), abs(bb.max.Y))
            key = entry._axle_cyl(side, KEY2, top + 0.05, 130.0, x, z - 42.0)
            h = hits(key, {k: v for k, v in wheel_off.items() if k != name})
            if h:
                blocked[name] = h
        clear = M["screw_r"] - KEY2 - r_new
        check(f"{tag} housing screws: straight 2 mm key with the stub in", not blocked and len(screws) == 4,
              f"{len(screws)} screws; {blocked or 'all clear'}; key {clear:.3f} mm off the flange")

        housing = local[f"AXLE_BEARING_HOUSING_{tag}"]
        hole, h0, h1 = M["housing_hole"]
        filled, full, clash = 0.0, 0.0, 0.0
        for angle in M["screw_angles"]:
            x, z = M["screw_r"] * math.cos(math.radians(angle)), M["screw_r"] * math.sin(math.radians(angle))
            tube = entry._axle_cyl(side, 1.69, h0 + 0.01, h1 - 0.01, x, z) - entry._axle_cyl(side, hole + 0.01, h0, h1, x, z)
            filled += common(housing, tube)
            full += vol(tube)
        for name in screws:
            clash += common(housing, local[name])
        check(f"{tag} housing screw holes Ø{2 * hole:.1f}", abs(filled - full) < 0.05 and clash < TOL,
              f"wall R{hole}-1.7 {filled:.2f}/{full:.2f} mm3; screws in the housing {clash:.4f} mm3; "
              f"{hole - 1.5:.2f} mm radial on the M3 shank")

        tips = {}
        for prefix, tree in ((SCREW, local), ("AXLE_CAP_SCREW_M3X18_", before)):
            tips[prefix] = [screw_tip(tree, name, tree[f"AXLE_MOTOR_CARRIER_{tag}"],
                                      tree[f"AXLE_PLATE_INSERT_M3_{tag}_{name[-1]}"])
                            for name in sorted(k for k in tree if k.startswith(f"{prefix}{tag}_"))]
        new, old = tips[SCREW], tips["AXLE_CAP_SCREW_M3X18_"]
        margin, engage = min(t[0] for t in new), min(t[1] for t in new) - 0.35
        check(f"{tag} housing screw tips clear of the hole bottom, M3 x 16", len(new) == 4 and margin > TIP_STACK
              and engage >= MIN_ENGAGE,
              f"tip {margin:.2f} mm above the hole bottom (stack {TIP_STACK:.2f}); {engage:.2f} mm in the insert "
              f"at the short limit (min {MIN_ENGAGE}); {min(t[2] for t in new):.2f} mm of plastic over the gearbox face")
        check(f"{tag} planted: the M3 x 18 tip is within the stack", len(old) == 4 and min(t[0] for t in old) < TIP_STACK,
              f"{min(t[0] for t in old):.2f} mm above the hole bottom")

        ss = local[f"WHEEL_{tag}_SET_SCREW_M3X2_5"].bounding_box()
        key = zcyl(KEY15, ss.max.Z + 0.05, 75.0, 0.0, side * 74.8)
        h = hits(key, {k: v for k, v in wheel_off.items() if "SET_SCREW" not in k})
        check(f"{tag} set screw: straight 1.5 mm key from +Z", not h, f"{h or 'clear'}")
        old = before[f"AXLE_MOTOR_CARRIER_{tag}"]
        check(f"{tag} planted: unedited carrier blocks that key", common(key, old) > TOL,
              f"{common(key, old):.3f} mm3")

        plug = entry.axle_alignment_plug(side)
        present = {k: v for k, v in local.items() if k.startswith(("AXLE_", "MOTOR_"))}
        h = hits(plug, present)
        check(f"{tag} alignment plug clear of every part present when it is used", not h,
              f"{len(present)} parts (carrier, housing, cap, motor, shaft, face and housing screws, inserts); {h or 'none'}")
        shaft = local[f"MOTOR_{tag}_OUTPUT_SHAFT"].bounding_box()
        engage = max(abs(shaft.min.Y), abs(shaft.max.Y)) - M["plug_nose"][1]
        cap_id = 6.25
        check(f"{tag} alignment plug fits", engage > 6.0 and M["plug_body"][0] > cap_id,
              f"{engage:.1f} mm on the shaft (Ø{2 * M['plug_bore']:.2f} bore, 0.025 radial); body R{M['plug_body'][0]} in the R8.0 seat; "
              f"nose R{M['plug_nose'][0]} in the R6.25 cavity; held in by the cap (ID R{cap_id}); "
              f"{(M['plug_body'][1] - 76.51) + (86.51 - M['plug_body'][2]):.2f} mm axial play")
        both = {}
        for x in (-M["key_x"], M["key_x"]):
            key = entry._axle_cyl(side, KEY2, 73.5, 130.0, x, 0.0)
            with_plug = hits(key, {**{k: v for k, v in present.items() if "MOTOR_SCREW" not in k}, "PLUG": plug})
            with_stub = hits(key, {k: v for k, v in wheel_off.items() if "MOTOR_SCREW" not in k})
            both[x] = (with_plug, sorted(with_stub))
        ok = all(not wp for wp, _ in both.values())
        check(f"{tag} face screws: 2 mm keys clear through the plug", ok,
              f"{ {x: v[0] or 'clear' for x, v in both.items()} }; with the bearings and stub instead: "
              f"{ {x: v[1] for x, v in both.items()} }")

        print(f"      {tag} print overhangs (|Y|: mm2):")
        print(f"        housing, inboard face down: {overhangs(housing, side, 74.0, +1) or 'none'}")
        print(f"        carrier, outboard face down: {overhangs(local[f'AXLE_MOTOR_CARRIER_{tag}'], side, 74.0, -1)}")
        print(f"        plug, outboard end down: {overhangs(plug, side, M['plug_body'][2], -1) or 'none'}")
        check(f"{tag} housing prints inboard face down with no support", not overhangs(housing, side, 74.0, +1), "no overhang faces")
        check(f"{tag} plug prints on its outboard end with no support", not overhangs(plug, side, M["plug_body"][2], -1), "no overhang faces")

    blocked = {}
    for name in [k for k in parts if k.startswith(f"{SCREW}L_")]:
        bb = parts[name].bounding_box()
        key = entry._axle_cyl(1, KEY2, bb.max.Y + 0.05, 130.0, bb.center().X, bb.center().Z - 42.0)
        blocked[name] = round(common(key, before["WHEEL_L_STUB_SHAFT_8MM"]), 3)
    check("planted: the unedited Ø24 flange blocks every housing-screw key", all(v > TOL for v in blocked.values()),
          f"{blocked}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
