"""Frame prints (D-073, D-074): insert and screw pilots and print orientation of the two frame
modules, measured on the chassis tree with the droid edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis tree twice (with and without the droid edits) and the body once, about 3 min.

Each pilot is probed with points: empty inside the new radius, material just outside it,
at three depths along the pilot, eight directions round it. Checks:

1. J04 rail ends, 8 pilots: Ø4.0 from the rail face to 7 mm deep (the M3 x 6 insert plus 1 mm
   for the plastic it pushes ahead), material past that.
2. J11A tub bosses, 4 pilots: Ø4.0 over the 6.5 mm pilot.
3. J15B driver posts, 4 pilots: Ø3.5 over the 4.1 mm pilot (M2.5 x 4 insert, OD 3.9).
4. J15A IMU: a Ø1.6 pilot through the 4 mm deck at each screw.
5. Each module is still one solid; the volume change is the rings, pilots and D-074 fills.
6. Planted: the unedited modules have Ø4.3 / Ø3.9 pilots and no IMU pilot.
7. Orientation (D-074): the front module prints tub bottom down (-Z), the rear deck down (+Z),
   the hatch outer face down. Bed contact and the faces that need support are measured: planar
   faces facing the bed but above it, less the ones a printer bridges (both ends supported and
   at most BRIDGE long). The front's J13 sockets and J10-8 bore stay open through its fill.
8. The D-074 fills keep CLEAR from every chassis and body part.
9. Planted: the unedited front module stands on its tub walls only (477 mm2), and the unedited
   rear crossmember strip sits 8 mm off the bed.
"""

import importlib.util
import math
from pathlib import Path
import sys

from build123d import GeomType, Location, Vector
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

F = entry.FRAME_FIX
GAP = 0.05          # probe this far inside / outside the nominal radius
P = entry.FRAME_PRINT
CLEAR = 1.5         # mm from a D-074 fill to any other part
results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")


def modules(tree):
    out = {}

    def walk(node, loc):
        kids = list(node.children) if getattr(node, "children", None) else []
        if kids:
            for kid in kids:
                walk(kid, loc * node.location)
        elif (node.label or "").startswith(("CHASSIS_FRAME_", "BATTERY_TUB_BOTTOM_HATCH")):
            out[node.label] = entry._shifted(node, loc)
    walk(tree, Location())
    return out


def solid_at(shape, p):
    return any(BRepClass3d_SolidClassifier(s.wrapped, gp_Pnt(*p), 1e-6).State() == TopAbs_IN for s in shape.solids())


def ring(axis, centre, r, a):
    """Eight points at radius r round an axis ('x' or 'z') through centre, at axial position a."""
    x, y, z = centre
    for k in range(8):
        u, v = r * math.cos(k * math.pi / 4), r * math.sin(k * math.pi / 4)
        yield (a, y + u, z + v) if axis == "x" else (x + u, y + v, a)


def pilot(shape, axis, centre, r, a0, a1):
    """(empty inside r over a0..a1, material outside r over a0..a1)."""
    depths = [a0 + (a1 - a0) * f for f in (0.1, 0.5, 0.9)]
    empty = all(not solid_at(shape, p) for a in depths for p in ring(axis, centre, r - GAP, a))
    wall = all(solid_at(shape, p) for a in depths for p in ring(axis, centre, r + GAP, a))
    return empty, wall


def pilots(mods):
    """(name, module, axis, centre, a0, a1) for every pilot D-073 touches; a0..a1 from the open end."""
    out = []
    face, _, deep = F["j04_x"]
    for region, sx in (("FRONT", 1.0), ("REAR", -1.0)):
        for sy in (1.0, -1.0):
            for z in F["j04_z"]:
                y = sy * F["j04_y"][region]
                out.append((f"J04 {region.lower()} Y{y:+.1f} Z{z:.0f}", mods[f"CHASSIS_FRAME_{region}_MODULE"], "x",
                            (0.0, y, z), sx * face, sx * deep))
    front = mods["CHASSIS_FRAME_FRONT_MODULE"]
    for x, y in F["boss_xy"]:
        out.append((f"J11A boss ({x}, {y})", front, "z", (x, y, 0.0), *F["boss_z"]))
    for x, y in F["post_xy"]:
        out.append((f"J15B post ({x}, {y})", front, "z", (x, y, 0.0), F["post_z"][1], F["post_z"][0]))
    return out


BRIDGE = 15.0       # mm a printer bridges between two supported ends
LEDGE = 2.0         # mm of flat cantilever that prints without support
# Parts that mate with or sit inside the module: they may touch a fill, never overlap it.
MATES = ("AXLE_MOTOR_CARRIER_", "J04_")


def _wall(shape, p, axis, sgn, below):
    """Distance along axis (sign sgn) from p to material, at most BRIDGE; None if none."""
    for k in range(1, int(BRIDGE / 0.5) + 1):
        q = list(p)
        q[axis] += sgn * 0.5 * k
        if solid_at(shape, tuple(q)):
            return 0.5 * k
    return None


def bed_and_overhang(shape, down, step=2.0):
    """(bed mm2, [(area, height, bbox text)]) with `down` toward the bed.

    Planar faces facing the bed but above it are sampled on a step grid. A sample is bridged
    when, just under the face, material lies within BRIDGE on both sides along one of the two
    in-plane axes, or within LEDGE on one side (a short ledge); the rest needs support. Curved faces are pilots and sockets, which print as
    small arches, and are left out."""
    d = Vector(*down)
    axis = max(range(3), key=lambda i: abs(down[i]))
    plane = [i for i in range(3) if i != axis]
    bb = shape.bounding_box()
    top = max(bb.min.dot(d), bb.max.dot(d))
    bed, need = 0.0, []
    for f in shape.faces():
        if f.geom_type != GeomType.PLANE or f.normal_at(f.center()).dot(d) < 0.999:
            continue
        h = top - f.center().dot(d)
        if h < 1e-3:
            bed += f.area
            continue
        fb = f.bounding_box()
        lo, hi = (fb.min.X, fb.min.Y, fb.min.Z), (fb.max.X, fb.max.Y, fb.max.Z)
        level = f.center().to_tuple()[axis] + 0.3 * down[axis]   # just under the face, toward the bed
        n_need = n_all = 0
        a = lo[plane[0]] + step / 2.0
        while a < hi[plane[0]]:
            b = lo[plane[1]] + step / 2.0
            while b < hi[plane[1]]:
                q = [0.0, 0.0, 0.0]
                q[axis], q[plane[0]], q[plane[1]] = level, a, b
                on = list(q)
                on[axis] -= 0.3 * down[axis]
                if f.distance_to(Vector(*on)) < 1e-3:
                    n_all += 1
                    bridged = False
                    for ax in plane:
                        lo_w, hi_w = _wall(shape, q, ax, -1, level), _wall(shape, q, ax, 1, level)
                        if lo_w is not None and hi_w is not None and lo_w + hi_w <= BRIDGE:
                            bridged = True
                            break
                        if min(w for w in (lo_w, hi_w, 99.0) if w is not None) <= LEDGE:
                            bridged = True
                            break
                    n_need += not bridged
                b += step
            a += step
        if n_all and n_need:
            area = f.area * n_need / n_all
            need.append((round(area), round(h, 1), f"X{fb.min.X:.0f}..{fb.max.X:.0f} Y{fb.min.Y:.0f}..{fb.max.Y:.0f} Z{fb.min.Z:.0f}..{fb.max.Z:.0f}"))
    return bed, sorted(need, reverse=True)


def body_parts():
    out = []

    def walk(node, loc):
        kids = list(node.children) if getattr(node, "children", None) else []
        if kids:
            for kid in kids:
                walk(kid, loc * node.location)
        elif not (node.label or "").startswith("CHASSIS_FRAME_"):
            out.append((node.label or "?", entry._shifted(node, loc)))
    walk(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False), Location())
    walk(B.build_body_assembly(), Location())
    return out


def main():
    edited = modules(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    raw = modules(B.chassis_v1_reference())

    for name, shape, axis, c, a0, a1 in pilots(edited):
        r = F["post_r"] if name.startswith("J15B") else F["insert_r"]
        empty, wall = pilot(shape, axis, c, r, a0, a1)
        check(f"{name} pilot Ø{2 * r:.1f}", empty and wall, f"open inside R{r - GAP:.2f}: {empty}; material at R{r + GAP:.2f}: {wall}; "
              f"{abs(a1 - a0):.1f} mm deep")
        if name.startswith("J04"):
            beyond = a1 + math.copysign(0.3, a1)
            check(f"{name} pilot bottom at {abs(a1 - a0):.1f} mm (insert 6.0 + 1.0)", solid_at(shape, (beyond, c[1], c[2] + 1.85)),
                  f"material at |X| {abs(beyond):.1f}, 0.3 mm past the pilot bottom, outside the Ø3.4 screw clearance")

    front = edited["CHASSIS_FRAME_FRONT_MODULE"]
    z0, z1 = F["imu_z"]
    for x, y in F["imu_xy"]:
        empty, wall = pilot(front, "z", (x, y, 0.0), F["imu_r"], z0 + 0.1, z1 - 0.1)
        check(f"J15A IMU pilot Ø1.6 at ({x}, {y})", empty and wall, f"open through the deck: {empty}; material round it: {wall}")

    for label in ("CHASSIS_FRAME_FRONT_MODULE", "CHASSIS_FRAME_REAR_MODULE"):
        n, dv = len(edited[label].solids()), (edited[label].volume - raw[label].volume) / 1000.0
        fill = sum(sh.volume for lab, sh in entry._FRAME_PRINT_ADDS if lab == label) / 1000.0
        check(f"{label} is one solid, volume change = fills + pilot rings", n == 1 and abs(dv - fill) < 0.2,
              f"{n} solid; {raw[label].volume / 1000:.2f} -> {edited[label].volume / 1000:.2f} cm3 ({dv:+.3f}; D-074 fills {fill:.3f})")

    old = []
    for name, shape, axis, c, a0, a1 in pilots(raw):
        r_old = 1.95 if name.startswith("J15B") else 2.15
        old.append(pilot(shape, axis, c, r_old, a0 + 0.5 * (a1 - a0) * 0.2, a0 + 0.5 * (a1 - a0))[0])
    imu_raw = [solid_at(raw["CHASSIS_FRAME_FRONT_MODULE"], (x, y, 54.0)) for x, y in F["imu_xy"]]
    check("planted: the unedited pilots are Ø4.3 / Ø3.9 and the IMU deck is solid", all(old) and all(imu_raw),
          f"{sum(old)}/{len(old)} old pilots open at the old radius; IMU solid: {imu_raw}")


    # 7. Orientation (D-074).
    plan = (("CHASSIS_FRAME_FRONT_MODULE", (0, 0, -1), "tub bottom down", 2800.0, 2200.0),
            ("CHASSIS_FRAME_REAR_MODULE", (0, 0, 1), "deck top down", 3500.0, 500.0),
            ("BATTERY_TUB_BOTTOM_HATCH", (0, 0, -1), "outer face down", 4900.0, 0.0))
    for label, down, how, bed_min, support_max in plan:
        bed, need = bed_and_overhang(edited[label], down)
        area = sum(a for a, _, _ in need)
        check(f"{label} prints {how}", bed >= bed_min and area <= support_max,
              f"bed {bed:.0f} mm2 (min {bed_min:.0f}); support under {area} mm2 (max {support_max:.0f})")
        for row in need:
            print(f"        support: {row[0]} mm2, {row[1]} mm up, {row[2]}")
    front = edited["CHASSIS_FRAME_FRONT_MODULE"]
    z = (P["front_floor"] + P["front_old"]) / 2.0
    holes = [(x, y, P["j13_socket_r"]) for x, y in P["j13_sockets"]] + [P["nose_bore"]]
    open_ = {f"({x}, {y})": all(not solid_at(front, p) for p in ring("z", (x, y, 0.0), r - GAP, z)) for x, y, r in holes}
    check("front fill keeps the J13 nut sockets and the J10-8 bore open", all(open_.values()), f"{open_}")

    # 8. Clearance of the fills.
    others = body_parts()
    for label, fill in entry._FRAME_PRINT_ADDS:
        fb = fill.bounding_box()
        near = []
        for name, part in others:
            pb = part.bounding_box()
            if (pb.min.X > fb.max.X + 3 or pb.max.X < fb.min.X - 3 or pb.min.Y > fb.max.Y + 3 or pb.max.Y < fb.min.Y - 3
                    or pb.min.Z > fb.max.Z + 3 or pb.max.Z < fb.min.Z - 3):
                continue
            gap = BRepExtrema_DistShapeShape(fill.wrapped, part.wrapped).Value()
            if gap < 3.0:
                near.append((round(gap, 2), name, round(sum(x.volume for x in (fill & part).solids()), 4) if gap < 1e-3 else 0.0))
        near.sort()
        bad = [n for n in near if n[2] > 1e-3 or (n[0] < CLEAR - 1e-3 and not n[1].startswith(MATES))]
        check(f"{label} D-074 fill clear by {CLEAR} mm (J04 mates may touch, not overlap)", not bad,
              f"nearest: {[(g, n) for g, n, _ in near[:6]]}; failing: {bad}")

    # 9. Planted.
    bed_raw, _ = bed_and_overhang(raw["CHASSIS_FRAME_FRONT_MODULE"], (0, 0, -1))
    strip = solid_at(raw["CHASSIS_FRAME_REAR_MODULE"], (-44.5, 0.0, 54.0))
    check("planted: unedited front module stands on its tub walls only; unedited rear strip is open at Z 54",
          bed_raw < 600 and not strip, f"bed {bed_raw:.0f} mm2; rear strip solid at Z 54: {strip}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
