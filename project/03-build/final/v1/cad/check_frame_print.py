"""Frame pilots (D-073): insert and screw pilots of the two frame modules, measured on the
chassis tree with the droid edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis tree twice (with and without the droid edits), about 1 min.

Each pilot is probed with points: empty inside the new radius, material just outside it,
at three depths along the pilot, eight directions round it. Checks:

1. J04 rail ends, 8 pilots: Ø4.0 from the rail face to 7 mm deep (the M3 x 6 insert plus 1 mm
   for the plastic it pushes ahead), material past that.
2. J11A tub bosses, 4 pilots: Ø4.0 over the 6.5 mm pilot.
3. J15B driver posts, 4 pilots: Ø3.5 over the 4.1 mm pilot (M2.5 x 4 insert, OD 3.9).
4. J15A IMU: a Ø1.6 pilot through the 4 mm deck at each screw.
5. Each module is still one solid; the volume change is only the rings and pilots.
6. Planted: the unedited modules have Ø4.3 / Ø3.9 pilots and no IMU pilot.
"""

import importlib.util
import math
from pathlib import Path
import sys

from build123d import Location
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
        elif (node.label or "").startswith("CHASSIS_FRAME_"):
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
        check(f"{label} is one solid, volume change small", n == 1 and abs(dv) < 0.2,
              f"{n} solid; {raw[label].volume / 1000:.2f} -> {edited[label].volume / 1000:.2f} cm3 ({dv:+.3f})")

    old = []
    for name, shape, axis, c, a0, a1 in pilots(raw):
        r_old = 1.95 if name.startswith("J15B") else 2.15
        old.append(pilot(shape, axis, c, r_old, a0 + 0.5 * (a1 - a0) * 0.2, a0 + 0.5 * (a1 - a0))[0])
    imu_raw = [solid_at(raw["CHASSIS_FRAME_FRONT_MODULE"], (x, y, 54.0)) for x, y in F["imu_xy"]]
    check("planted: the unedited pilots are Ø4.3 / Ø3.9 and the IMU deck is solid", all(old) and all(imu_raw),
          f"{sum(old)}/{len(old)} old pilots open at the old radius; IMU solid: {imu_raw}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
