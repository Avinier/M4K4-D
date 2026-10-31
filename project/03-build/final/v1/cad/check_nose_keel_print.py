"""Nose and keel prints (nose and keel pages §4–§5): insert and screw pilots and print orientation of
the pod seat, sensor lid, touch cap, keel, wear shoe, TCRT bezel and height shims, measured on the
chassis tree with the droid edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md, plus
../../../01-chassis/v1/cad. `--survey` prints bed and support for all six faces of every print
instead of running the checks.

Overhangs: the frame check counted only flat faces pointing straight at the bed. These parts are
lofted and faceted, so every face is tessellated and each triangle steeper than 45° to the bed
(normal within 45° of the bed direction) counts. A flat one is bridged when material lies within
BRIDGE on both sides along one in-plane axis, or is a ledge within LEDGE on one side (the frame's
rule). A sloped one prints when its face runs at most LEDGE across, measured downhill (a chamfer);
the rest needs support. Holes under 3 mm radius print as small arches and are left out.
"""

import importlib.util
import math
from pathlib import Path
import sys

from build123d import GeomType, Location, Vector
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRep import BRep_Tool
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt, gp_Dir, gp_Lin
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

BRIDGE = 15.0       # mm a printer bridges between two supported ends
LEDGE = 2.0         # mm of cantilever, flat or sloped, that prints without support
STEEP = math.cos(math.radians(44.0))   # 45° chamfers print; anything shallower counts
PRINTS = ("BALL_POD_PRINTED_SEAT", "BALL_POD_SENSOR_LID", "BALL_NOSE_TOUCH_CAP", "REAR_KEEL_FACETED_BODY",
          "REAR_KEEL_REPLACEABLE_WEAR_SHOE", "REAR_TCRT_BEZEL_WITH_GUARDS", "REAR_TCRT_HEIGHT_SHIM_1")
DIRS = {"-Z": (0, 0, -1), "+Z": (0, 0, 1), "-X": (-1, 0, 0), "+X": (1, 0, 0), "-Y": (0, -1, 0), "+Y": (0, 1, 0)}
results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}", flush=True)


def leaves(tree):
    out = {}

    def walk(node, loc):
        kids = list(node.children) if getattr(node, "children", None) else []
        if kids:
            for kid in kids:
                walk(kid, loc * node.location)
        else:
            out[node.label or f"?{len(out)}"] = entry._shifted(node, loc)
    walk(tree, Location())
    return out


_classifiers = {}


def solid_at(shape, p):
    # Load the topology once; reclassifying points must not rebuild it thousands of times.
    key = id(shape)
    if key not in _classifiers:
        _classifiers[key] = (shape, [BRepClass3d_SolidClassifier(s.wrapped) for s in shape.solids()])
    point = gp_Pnt(*p)
    for classifier in _classifiers[key][1]:
        classifier.Perform(point, 1e-6)
        if classifier.State() == TopAbs_IN:
            return True
    return False


_ray_intersectors = {}


def _wall(shape, p, axis, sgn):
    """First material on the same 0.5 mm sample grid, at most BRIDGE away.

    A ray finds candidate entry boundaries so empty intervals do not trigger dozens
    of costly OCC solid classifications on a loft. Candidates are still classified
    on the original grid: thin features between grid points remain unsampled.
    """
    def inside(k):
        q = list(p)
        q[axis] += sgn * 0.5 * k
        return solid_at(shape, tuple(q))

    if inside(1):
        return 0.5
    key = id(shape)
    if key not in _ray_intersectors:
        intersector = IntCurvesFace_ShapeIntersector()
        intersector.Load(shape.wrapped, 1e-7)
        _ray_intersectors[key] = (shape, intersector)
    intersector = _ray_intersectors[key][1]
    direction = [0.0, 0.0, 0.0]
    direction[axis] = sgn
    intersector.Perform(gp_Lin(gp_Pnt(*p), gp_Dir(*direction)), 0.0, BRIDGE)
    assert intersector.IsDone(), "overhang support ray failed"
    candidates = set()
    for i in range(1, intersector.NbPnt() + 1):
        k = max(1, math.ceil((intersector.WParameter(i) - 1e-7) / 0.5))
        candidates.update((k, k + 1))  # exact-boundary points classify ON, not IN
    for k in sorted(candidates):
        if 1 < k <= int(BRIDGE / 0.5) and inside(k):
            return 0.5 * k
    return None


def _small_hole(face):
    if face.geom_type != GeomType.CYLINDER:
        return False
    cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
    if cyl.Radius() >= 3.0:
        return False
    # Only concave bores get the small-arch exemption, never convex pins or bosses.
    p = face.position_at(0.5, 0.5)
    loc, direction = cyl.Location(), cyl.Axis().Direction()
    axis = Vector(direction.X(), direction.Y(), direction.Z())
    radial = p - Vector(loc.X(), loc.Y(), loc.Z())
    radial = radial - axis * radial.dot(axis)
    return face.normal_at(p).dot(radial) < 0.0


def bed_and_overhang(shape, down):
    """(bed mm2, [(area, height, where)]) with `down` toward the bed; see the module docstring."""
    d = Vector(*down)
    axis = max(range(3), key=lambda i: abs(down[i]))
    plane = [i for i in range(3) if i != axis]
    bb = shape.bounding_box()
    top = max(bb.min.dot(d), bb.max.dot(d))
    bed, need = 0.0, []
    for f in shape.faces():
        if _small_hole(f):
            continue
        flat = f.geom_type == GeomType.PLANE
        if flat:
            n = f.normal_at(f.center())
            if n.dot(d) < STEEP:
                continue
        verts, tris = f.tessellate(0.05, 0.2)
        flat_normal = f.normal_at(f.center()) if flat else None
        face_vertices = [Vector(v.X, v.Y, v.Z) for v in f.vertices()]
        area_need = area_all = 0.0
        for i, j, k in tris:
            a, b, c = verts[i], verts[j], verts[k]
            cross = (b - a).cross(c - a)
            twice_area = cross.length
            area = twice_area / 2.0
            if area < 1e-6:
                continue
            g = (a + b + c) * (1.0 / 3.0)
            # build123d tessellate reverses winding for reversed OCC faces.
            # Triangle normals avoid costly repeated projections onto loft surfaces.
            n = flat_normal if flat else cross * (1.0 / twice_area)
            nd = n.dot(d)
            if nd < STEEP:
                continue
            h = top - g.dot(d)
            if h < 1e-3 and nd > 0.999:
                bed += area
                continue
            if h < 0.2:
                continue
            area_all += area
            if nd > 0.999:          # flat: bridge or ledge
                q = list(tuple(g))
                q[axis] += 0.3 * down[axis]
                ok = False
                for ax in plane:
                    lo, hi = _wall(shape, q, ax, -1), _wall(shape, q, ax, 1)
                    if (lo is not None and hi is not None and lo + hi <= BRIDGE) or min(w for w in (lo, hi, 99.0) if w is not None) <= LEDGE:
                        ok = True
                        break
            else:                   # sloped: a chamfer prints if it runs at most LEDGE downhill
                hz = n - d * nd
                hz = hz * (1.0 / hz.length)
                proj = [v.dot(hz) for v in face_vertices]
                ok = max(proj) - min(proj) <= LEDGE + 0.05
            if not ok:
                area_need += area
        if area_need > 0.5:
            fb = f.bounding_box()
            need.append((round(area_need), round(top - f.center().dot(d), 1),
                         f"X{fb.min.X:.1f}..{fb.max.X:.1f} Y{fb.min.Y:.1f}..{fb.max.Y:.1f} Z{fb.min.Z:.1f}..{fb.max.Z:.1f}"))
    return bed, sorted(need, reverse=True)


def survey(parts, labels=PRINTS):
    for label in labels:
        s = parts[label]
        print(f"\n== {label}: {s.volume / 1000:.3f} cm3, {len(s.solids())} solid, bbox {tuple(round(v, 2) for v in s.bounding_box().size)}", flush=True)
        for name, d in DIRS.items():
            bed, need = bed_and_overhang(s, d)
            print(f"  down {name}: bed {bed:7.1f} mm2  support {sum(a for a, _, _ in need):6.0f} mm2", flush=True)
            for row in need[:8]:
                print(f"        {row}", flush=True)


import body_chassis_model as M  # noqa: E402  (01-chassis/v1/cad on PYTHONPATH)

N = entry.NOSE_KEEL_FIX
GAP = 0.05
SEAT, FRONT, REAR, KEEL = "BALL_POD_PRINTED_SEAT", "CHASSIS_FRAME_FRONT_MODULE", "CHASSIS_FRAME_REAR_MODULE", "REAR_KEEL_FACETED_BODY"
SHOE, BEZEL = "REAR_KEEL_REPLACEABLE_WEAR_SHOE", "REAR_TCRT_BEZEL_WITH_GUARDS"
# (label, bed direction, how, min bed mm2, max support mm2): D-078.
PLAN = ((SEAT, (0, 0, -1), "seat face down", 1200.0, 0.0),
        ("BALL_POD_SENSOR_LID", (1, 0, 0), "front end down", 60.0, 100.0),
        ("BALL_NOSE_TOUCH_CAP", (0, 0, 1), "top down", 140.0, 40.0),
        (KEEL, (0, 0, 1), "seat face down", 190.0, 330.0),
        (SHOE, (0, 0, -1), "sole down", 100.0, 0.0),
        (BEZEL, (0, 0, -1), "lips down, as it sits", 50.0, 30.0),
        ("REAR_TCRT_HEIGHT_SHIM_1", (0, 0, -1), "flat", 110.0, 0.0))


def pt(axis, c, r, k, a, n=16):
    u, v = r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)
    x, y, z = c
    return {"x": (a, y + u, z + v), "y": (x + u, a, z + v), "z": (x + u, y + v, a)}[axis]


def bore(shape, axis, c, r, a0, a1):
    """(open inside r over a0..a1, material just outside r) at five depths, sixteen directions."""
    depths = [a0 + (a1 - a0) * f for f in (0.05, 0.25, 0.5, 0.75, 0.95)]
    empty = all(not solid_at(shape, pt(axis, c, r - GAP, k, a)) for a in depths for k in range(16))
    wall = all(solid_at(shape, pt(axis, c, r + GAP, k, a)) for a in depths for k in range(16))
    return empty, wall


def wall(shape, axis, c, r, depths):
    """Least material from radius r outward, over sixteen directions and the given depths."""
    least = 99.0
    for a in depths:
        for k in range(16):
            w = 0.0
            while w < 6.0 and solid_at(shape, pt(axis, c, r + w + 0.05, k, a)):
                w += 0.05
            least = min(least, w)
    return round(least, 2)


def bottom(shape, axis, c, r, start, sgn, limit=15.0):
    """Distance from `start` along the axis to the first material inside radius r (8 directions)."""
    a = start
    while abs(a - start) < limit:
        a += sgn * 0.05
        if any(solid_at(shape, pt(axis, c, r, k, a, 8)) for k in range(8)):
            return round(abs(a - start), 2)
    return limit


def tip_angle(shape):
    """Least tip-back angle, deg, about the wheel contact line (X 0, Z 0) at which shape meets the floor."""
    return min(math.degrees(math.atan2(v.Z, -v.X)) for v in shape.vertices() if v.X < 0)


def main():
    parts = leaves(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    if "--survey" in sys.argv:
        labels = [arg for arg in sys.argv[1:] if arg != "--survey"] or PRINTS
        assert all(label in PRINTS for label in labels), "unknown print label in survey"
        survey(parts, labels)
        return
    raw = leaves(B.chassis_v1_reference())
    r_ins, _, length = N["insert"]

    # 1. Caster seat: the M3 x 6 fills the 6 mm seat; the bore is through, Ø4.0.
    seat = parts[SEAT]
    for k, (x, y) in enumerate(M.ball_screw_points(), start=1):
        empty, mat = bore(seat, "z", (x, y, 0.0), 2.0, 29.0, N["seat_relief"][1] if k == 1 else 35.0)  # insert 1: below its relief
        w = wall(seat, "z", (x, y, 0.0), r_ins, (29.5, 32.0, 34.4))
        ins = parts[f"BALL_SEAT_HEATSET_INSERT_{k}"].bounding_box()
        check(f"J07A seat bore {k} ({x:.2f}, {y:+.2f}) Ø4.0 through, M3 x 6 inside it", empty and mat and abs(ins.min.Z - 29.0) < 1e-6
              and abs(ins.max.Z - 35.0) < 1e-6 and w >= 1.0,
              f"open {empty}, material round it {mat}; insert Z {ins.min.Z:.2f}-{ins.max.Z:.2f} ({length} mm, flush both faces); least wall past OD 4.4: {w} mm")
    x, y = M.ball_screw_points()[0]
    r, z0, _ = N["seat_relief"]
    empty = all(not solid_at(seat, pt("z", (x, y, 0.0), r - GAP, k, 34.75)) for k in range(16))
    floor = all(solid_at(seat, pt("z", (x, y, 0.0), r + GAP, k, 34.75)) for k in range(16))
    gp2y = parts["GP2Y0A21YK0F_STEP"].bounding_box()
    check("J07A insert 1 relief Ø5.0 x 0.5 under the GP2Y", empty and floor and gp2y.min.X < x + r,
          f"relief open {empty}, floor round it {floor}; GP2Y rear X {gp2y.min.X:.2f}, relief to X {x + r:.2f}")

    # 2. Crossmember pod pilots (J07B): 7 mm for the 6 mm insert.
    front = parts[FRONT]
    for k, (y, z) in enumerate(M.BALL_POD_SCREWS_YZ, start=1):
        empty, mat = bore(front, "x", (0.0, y, z), 2.0, 85.2, 92.0)
        deep = bottom(front, "x", (0.0, y, z), 1.9, 92.0, -1)
        w = wall(front, "x", (0.0, y, z), r_ins, (86.5, 89.0, 91.5))
        check(f"J07B crossmember pilot Y{y:+.0f} Ø4.0, ≥ 7 mm", empty and mat and deep >= length + 1.0 - 0.06 and w >= 1.5,
              f"open {empty}, material {mat}; {deep} mm deep; least wall {w} mm")

    # 3. Keel pilots in the rear crossmember (J09A): 7 mm, Ø3.4 beyond for the screw tips.
    rear = parts[REAR]
    for k, (x, y) in enumerate(M.rear_keel_screw_points(), start=1):
        empty, mat = bore(rear, "z", (x, y, 0.0), 2.0, 34.0, 41.0)
        deep = bottom(rear, "z", (x, y, 0.0), 1.9, 34.0, 1)
        clear = bottom(rear, "z", (x, y, 0.0), 1.6, 34.0, 1)
        tip = parts[f"REAR_KEEL_M3X30_SCREW_{k}"].bounding_box().max.Z
        w = wall(rear, "z", (x, y, 0.0), r_ins, (34.5, 37.0, 39.5))
        check(f"J09A keel pilot {k} ({x}, {y:+}) Ø4.0, ≥ 7 mm", empty and mat and deep >= 6.94 and 34.0 + clear - tip >= 1.0 and w >= 1.5,
              f"{deep} mm deep; Ø3.4 to Z {34.0 + clear:.2f}, screw tip Z {tip:.2f}; least wall {w} mm")

    # 4. Thread in each insert (ISO 7380 / 4762 M3 into the M3 x 6).
    rows = []
    for k in range(1, 4):
        top = parts[f"BALL_M3_SHANK_{k}"].bounding_box().max.Z
        rows.append((f"J07A {k}", min(top, 35.0) - 29.0))
    for k in range(1, 3):
        tip = parts[f"BALL_POD_M3_SHANK_{k}"].bounding_box().min.X
        rows.append((f"J07B {k}", 92.0 - max(tip, 86.0)))
    for k in range(1, 5):
        tip = parts[f"REAR_KEEL_M3X30_SCREW_{k}"].bounding_box().max.Z
        rows.append((f"J09A {k}", min(tip, 40.0) - 34.0))
    check("M3 screws keep ≥ 5 mm of thread in the M3 x 6 inserts", all(e >= 4.99 for _, e in rows),
          ", ".join(f"{n} {e:.1f}" for n, e in rows))

    # 5. M2 thread-forming pilots, Ø1.6 (0.8 x d).
    lx, ly = M.LID_SCREW_XY
    empty, mat = bore(seat, "z", (lx, ly, 0.0), 0.8, 37.0, 48.9)
    lid_tip = parts["BALL_POD_LID_M2X8_CSK_SCREW"].bounding_box().min.Z
    w = wall(seat, "z", (lx, ly, 0.0), 1.0, (40.0, 44.0, 48.0))
    check("J08C lid pilot Ø1.6 in the boss", empty and mat and lid_tip - 36.0 >= 1.0 and w >= 1.0,
          f"open {empty}; tip Z {lid_tip:.1f}, pilot bottom Z 36.0; wall past the thread {w} mm")
    keel = parts[KEEL]
    (sx, sy), (px, py) = M.REAR_TCRT_FIX_POINTS
    _, _, deepest = N["bezel_pilot"]
    zero_tip = N["belly"] - M.REAR_TCRT_BEZEL_T + 10.0          # zero shims: plate underside + screw length
    empty, mat = bore(keel, "z", (sx, sy, 0.0), 0.8, 12.5, deepest - 0.1)
    w = wall(keel, "z", (sx, sy, 0.0), 1.0, (13.0, 16.0, 19.0))
    check("J09B bezel pilot Ø1.6 runs ≥ 1 mm past the screw tip at zero shims", empty and mat and deepest - zero_tip >= 0.99,
          f"open {empty}; pilot to Z {deepest}, tip at zero shims Z {zero_tip:.1f}; wall past the thread {w} mm (toward the TCRT pocket)")
    pin_top = N["belly"] + 6.0
    deep = bottom(keel, "z", (px, py, 0.0), 0.9, N["belly"], 1)
    check("J09B pin hole clears the pin at zero shims by ≥ 1 mm", N["belly"] + deep - pin_top >= 0.99,
          f"hole to Z {N['belly'] + deep:.2f}, pin top Z {pin_top:.1f}")
    shoe = parts[SHOE]
    sz = M.SKID_SHOE_BOTTOM_Z + M.SKID_SHOE_SIZE[2] + M.REAR_KEEL_SHOE_TONGUE[2] / 2.0
    empty, mat = bore(shoe, "y", (M.SKID_PAD_CENTER[0], 0.0, sz), 0.8, -1.8, 1.8)
    top = shoe.bounding_box().max.Z
    check("J10A shoe pilot Ø1.6 under ≥ 1.2 mm of tongue", empty and top - (sz + 0.8) >= 1.2 - 1e-6,
          f"open {empty}; roof {top - (sz + 0.8):.2f} mm (tongue top Z {top:.2f})")
    groove = all(not solid_at(keel, (M.SKID_PAD_CENTER[0] + dx, 0.0, N["tongue_top"] + 0.05)) for dx in (-4.0, 0.0, 4.0))
    check("J10A keel groove clears the taller tongue", groove, f"groove open at Z {N['tongue_top'] + 0.05}: {groove}")

    # 6. Shims and the sensor flat (D-077 2).
    shims = [parts[f"REAR_TCRT_HEIGHT_SHIM_{k}"].bounding_box() for k in (1, 2)]
    t = [round(b.max.Z - b.min.Z, 3) for b in shims]
    bez = parts[BEZEL].bounding_box()
    flat = all(not solid_at(keel, (x, 0.0 + dy, N["belly"] - 0.1)) and solid_at(keel, (x, dy, N["belly"] + 0.1))
               for x in (-60.0, -50.0) for dy in (-6.5, 6.5))
    check("J09B shims 1.2 mm; two set the face at Z 10 under the Z 12.4 flat; lips at Z 7",
          all(abs(v - N["shim_t"]) < 1e-3 for v in t) and abs(min(b.min.Z for b in shims) - 10.0) < 1e-3
          and abs(max(b.max.Z for b in shims) - N["belly"]) < 1e-3 and flat and abs(bez.min.Z - 7.0) < 1e-3,
          f"shims {t} mm, Z {min(b.min.Z for b in shims):.2f}-{max(b.max.Z for b in shims):.2f}; flat at Z {N['belly']} {flat}; lips Z {bez.min.Z:.2f}")
    # Tip-back order at the nominal stack, and the range.
    ang = {n: tip_angle(parts[l]) for n, l in (("shoe", SHOE), ("guards", BEZEL), ("keel", KEEL), ("sensor", "TCRT5000_REAR_STEP"))}
    check("Tipping back, the shoe meets the floor first (D-014 order)", ang["shoe"] < ang["guards"] < ang["sensor"] and ang["shoe"] < ang["keel"],
          ", ".join(f"{n} {a:.2f}°" for n, a in ang.items()))
    lip_x = M.REAR_KEEL_GUARD_X[0]
    for n in (0, 1, 3, 4):
        z_lip = N["belly"] - n * N["shim_t"] - 3.0
        a = math.degrees(math.atan2(z_lip, -lip_x))
        print(f"        {n} shims: face Z {z_lip + 3.0:.1f}, lips Z {z_lip:.1f}, guards meet the floor at {a:.2f}° (shoe {ang['shoe']:.2f}°)")

    # Real case support, rather than a bounding-box overlap with the ledge.
    # The vendor part's projecting optical baffle sets min Z; its case is rounded.
    def overlap(a, b):
        common = a & b
        return sum(s.volume for s in common.solids()) if common is not None else 0.0

    sensor = parts["TCRT5000_REAR_STEP"]
    bezel = parts[BEZEL]
    static = overlap(sensor, bezel)
    down = overlap(entry._shifted(sensor, Location((0, 0, -0.05))), bezel)
    check("J09B contoured cradles hold the actual case within 0.05 mm at the unchanged datum",
          static < 1e-3 and down > 0.1 and abs(sensor.bounding_box().min.Z - 10.0) < 1e-5,
          f"static overlap {static:.5f}; 0.05 mm down {down:.3f} mm3; sensor min Z {sensor.bounding_box().min.Z:.3f}")
    old_down = overlap(entry._shifted(raw["TCRT5000_REAR_STEP"], Location((0, 0, -0.2))), raw[BEZEL])
    check("planted: unedited flat bezel lets the actual sensor drop 0.2 mm without support",
          old_down < 1e-3, f"overlap {old_down:.5f} mm3")
    gaps = []
    for count in range(5):
        shift = Location((0, 0, (2 - count) * N["shim_t"]))
        posed = entry._shifted(bezel, shift)
        gaps.append((count, overlap(posed, keel), overlap(posed, entry._shifted(sensor, shift))))
    check("J09B cradles clear keel and sensor at every zero-to-four-shim setting",
          all(k < 1e-3 and t < 1e-3 for _, k, t in gaps), f"(count, keel mm3, sensor mm3) {gaps}")
    shim_hits = [overlap(bezel, parts[f"REAR_TCRT_HEIGHT_SHIM_{k}"]) for k in (1, 2)]
    check("J09B widened shim windows clear the cradles", max(shim_hits) < 1e-3, f"{shim_hits} mm3")

    gp2y_fixed, gp2y_raw = parts["GP2Y0A21YK0F_STEP"], raw["GP2Y0A21YK0F_STEP"]
    bb, rb = gp2y_fixed.bounding_box(), gp2y_raw.bounding_box()
    bounds_delta = max(abs(a - b) for a, b in zip((*bb.min, *bb.max), (*rb.min, *rb.max)))
    volume_delta = abs(gp2y_fixed.volume - gp2y_raw.volume)
    check("GP2Y ear-trim topology healed without moving its fitting envelope",
          BRepCheck_Analyzer(gp2y_fixed.wrapped).IsValid() and bounds_delta < 1e-6 and volume_delta < 1e-3,
          f"bounds delta {bounds_delta:.8f} mm; volume delta {volume_delta:.7f} mm3")
    check("planted: unedited trimmed GP2Y has invalid topology",
          not BRepCheck_Analyzer(gp2y_raw.wrapped).IsValid(), "unchanged subsystem ear-trim boolean")

    # 7. PCB-15 slot edits (D-059, D-063) still in the seat.
    board = parts["BALL_NOSE_HALL_CARRIER_PCB"]
    overlap = sum(s.volume for s in (seat & board).solids())
    walls = solid_at(seat, (127.3, 7.5, 33.0)) and not solid_at(seat, (126.3, 10.0, 33.0)) and not solid_at(seat, (125.9, 10.0, 34.5))
    check("PCB-15 slot (D-059, D-063) still in the seat", overlap < 1e-3 and walls, f"board overlap {overlap:.4f} mm3; slot and relief {walls}")

    # 8. Every print is one closed, valid, positive-volume solid (both installed shims).
    for label in (*PRINTS, "REAR_TCRT_HEIGHT_SHIM_2"):
        solids = parts[label].solids()
        n = len(solids)
        valid = n == 1 and BRepCheck_Analyzer(parts[label].wrapped).IsValid() and all(s.volume > 0 and all(BRep_Tool.IsClosed_s(shell.wrapped) for shell in s.shells()) for s in solids)
        dv = (parts[label].volume - raw[label].volume) / 1000.0 if label in raw else 0.0
        check(f"{label} one valid closed positive-volume solid", valid, f"{n} solid; {parts[label].volume / 1000:.3f} cm3 ({dv:+.3f})")

    # 9. Planted: the unedited parts.
    rk = raw[REAR]
    deep = [bottom(rk, "z", (x, y, 0.0), 1.9, 34.0, 1) for x, y in M.rear_keel_screw_points()]
    rkeel = raw[KEEL]
    old_pilot = 12.0 + bottom(rkeel, "z", (sx, sy, 0.0), 0.75, 12.0, 1)
    old_tip = 12.0 - M.REAR_TCRT_BEZEL_T + 10.0
    old_roof = raw[SHOE].bounding_box().max.Z - (sz + 0.8)
    old_t = raw["REAR_TCRT_HEIGHT_SHIM_1"].bounding_box()
    check("planted: unedited keel pilots < 7 mm, bezel pilot ends at the zero-shim tip, shoe roof < 1.2, shims 1.0",
          max(deep) < 6.9 and old_pilot - old_tip < 0.5 and old_roof < 0.6 and old_t.max.Z - old_t.min.Z < 1.1,
          f"keel pilots {deep}; bezel pilot Z {old_pilot:.2f} vs tip {old_tip:.1f}; roof {old_roof:.2f}; shim {old_t.max.Z - old_t.min.Z:.2f}")

    # 10. Orientation (D-078).
    for label, down, how, bed_min, support_max in PLAN:
        bed, need = bed_and_overhang(parts[label], down)
        area = sum(a for a, _, _ in need)
        check(f"{label} prints {how}", bed >= bed_min and area <= support_max,
              f"bed {bed:.0f} mm2 (min {bed_min:.0f}); support {area} mm2 (max {support_max:.0f})")
        for row in need:
            print(f"        support: {row[0]} mm2, {row[1]} mm up, {row[2]}")
    bed, need = bed_and_overhang(parts["BALL_NOSE_TOUCH_CAP"], (1, 0, 0))
    fingers = [row for row in need if abs(row[1] - 5.0) < 0.3]
    check("planted: nose face down leaves the snap fingers' first layers over their slits", len(fingers) >= 2,
          f"{fingers}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
