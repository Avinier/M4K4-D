"""Frame assembly and service (frame page §6): tool access per joint in the state each step is
done in, and the D-075 J13 deck inserts, measured on the chassis and body trees with the droid
edits applied.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis tree twice and the body once, about 5 min.

Tools are modelled across their corners: 2 mm hex r 1.155, 2.5 mm hex r 1.443, 1.5 mm hex
r 0.87, PH1 shaft r 2.25, PH0 / T6 shaft r 1.5, a Ø3 backing dowel. Checks:

1. J13 (D-075), three top-driven points: the nut socket is filled back to the rail and deck, the
   Ø5.5 insert pilot is open 9 mm from the deck top, the M4 x 12 keeps at least 5 mm of thread
   in the insert and stops at least 1 mm above the pilot bottom, the plain nut is gone and an
   insert is in its place. The front-left socket (bolt from below into the body foot cassette) stays open.
2. Rear J04 keys: rail wall on every side of the key tongue again. Planted: the unedited rear
   module (the inner wall was 6 %).
3. J04: a 2 mm L-key (16 mm leg along the bay, long leg up) reaches each of the eight screws with
   the modules and carriers in place and the motor out. Planted: the motor blocks it.
4. J11A: a 2 mm key reaches each hatch screw from below with the body on.
5. J12: the ballast bar drops out with the hatch off (planted: the hatch blocks it); a PH1
   reaches each screw from above with the body off.
6. J13: a 2.5 mm key reaches each top-driven bolt from above with only the body frame and its
   cassette fitted (body assembly step 1); the front-left bolt's key reaches it from below 1 mm
   clear of the hatch, and the bolt itself comes out downward through the D-076 hatch notch
   (planted: the unnotched hatch).
7. J15A, J15B: the IMU driver and the 1.5 mm key reach their screws from above, body off.
8. J15B inner posts: a Ø3 dowel backs each post from below through the open tub (hatch and pack
   out) while its insert is pressed.
"""

import importlib.util
from pathlib import Path
import sys

from build123d import Box, Cylinder, Location
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

J = entry.J13_FIX
TOL = 1e-3
results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")


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


def solid_at(shape, p):
    return any(BRepClass3d_SolidClassifier(s.wrapped, gp_Pnt(*p), 1e-6).State() == TopAbs_IN for s in shape.solids())


def zc(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def xc(r, x0, x1, y, z):
    return Cylinder(r, x1 - x0, rotation=(0, 90, 0)).moved(Location(((x0 + x1) / 2.0, y, z)))


def box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))


def hits(tool, parts, skip=()):
    tb = tool.bounding_box()
    out = {}
    for name, part in parts.items():
        if name.startswith(skip):
            continue
        pb = part.bounding_box()
        if (pb.min.X > tb.max.X or pb.max.X < tb.min.X or pb.min.Y > tb.max.Y or pb.max.Y < tb.min.Y
                or pb.min.Z > tb.max.Z or pb.max.Z < tb.min.Z):
            continue
        v = sum(s.volume for s in (tool & part).solids())
        if v > TOL:
            out[name] = round(v, 2)
    return out


def subset(parts, prefixes=(), drop=()):
    return {k: v for k, v in parts.items() if (not prefixes or k.startswith(prefixes)) and not k.startswith(drop)}


def key_walls(module, carrier):
    """% of rail wall within 0.6 mm of each face of the carrier's key tongue in this rail end."""
    bb = carrier.bounding_box()
    sx = 1.0 if module.bounding_box().center().X > 0 else -1.0
    sy = 1.0 if bb.center().Y > 0 else -1.0
    zone = box(*sorted((sx * 17.0, sx * 21.0)), *sorted((sy * 49.0, sy * 54.0)), 40.0, 46.0)
    t = (carrier & zone).bounding_box()
    out = {}
    for name, wb in (("inner", (t.min.X, t.max.X, *((t.min.Y - 0.6, t.min.Y - 0.1) if sy > 0 else (t.max.Y + 0.1, t.max.Y + 0.6)), t.min.Z, t.max.Z)),
                     ("outer", (t.min.X, t.max.X, *((t.max.Y + 0.1, t.max.Y + 0.6) if sy > 0 else (t.min.Y - 0.6, t.min.Y - 0.1)), t.min.Z, t.max.Z)),
                     ("floor", (t.min.X, t.max.X, t.min.Y, t.max.Y, t.min.Z - 0.6, t.min.Z - 0.1)),
                     ("roof", (t.min.X, t.max.X, t.min.Y, t.max.Y, t.max.Z + 0.1, t.max.Z + 0.6))):
        probe = box(*wb)
        out[name] = round(100.0 * sum(s.volume for s in (module & probe).solids()) / probe.volume)
    return out


def main():
    chassis = leaves(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    raw = leaves(B.chassis_v1_reference())
    body = leaves(entry._apply_droid_cuts(B.build_body_assembly(), strict=False))
    front, rear = chassis["CHASSIS_FRAME_FRONT_MODULE"], chassis["CHASSIS_FRAME_REAR_MODULE"]

    # 1. J13 deck inserts (D-075).
    for k, (x, y) in enumerate(J["points"], start=1):
        mod = front if x > 0 else rear
        sy = 1.0 if y > 0 else -1.0
        filled = solid_at(mod, (x, y + sy * 4.0, 45.0)) and all(solid_at(mod, (x + dx, y + dy, 52.5))
                                                               for dx, dy in ((4.0, 0), (-4.0, 0), (0, 4.0), (0, -4.0)))
        p0, p1 = J["pilot_z"]
        pilot = all(not solid_at(mod, (x + dx, y + dy, z)) for z in (p0 + 0.2, (p0 + p1) / 2, p1 - 0.2)
                    for dx, dy in ((2.7, 0), (-2.7, 0), (0, 2.7), (0, -2.7)))
        deck = all(solid_at(mod, (x + dx, y + dy, 54.0)) for dx, dy in ((2.8, 0), (-2.8, 0), (0, 2.8), (0, -2.8)))
        floor = solid_at(mod, (x, y + sy * 1.0, p0 - 0.3))
        check(f"J13 ({x}, {y}) socket filled, Ø5.5 pilot {p1 - p0:.0f} mm deep", filled and pilot and deck and floor,
              f"filled {filled}; pilot open {pilot}; deck round it {deck}; pilot floor {floor}")
        shank = body.get(f"BODY_CHASSIS_M4_SHANK_{k}")
        tip = shank.bounding_box().min.Z
        thread = J["insert"][3] - max(tip, J["insert"][2])
        check(f"J13 ({x}, {y}) M4 x 12 in the M4 x 8 insert", thread >= 5.0 and tip - p0 >= 1.0,
              f"{thread:.1f} mm of thread; tip {tip - p0:.1f} mm above the pilot bottom")
        check(f"J13 ({x}, {y}) nut removed, insert fitted", f"BODY_CHASSIS_M4_NUT_{k}" not in body
              and f"J13_DECK_INSERT_M4X8_{k}" in chassis, "plain nut gone; J13_DECK_INSERT present")
    for label, fill in entry._J13_ADDS:
        fb = fill.bounding_box()
        near = []
        for name, part in {**chassis, **body}.items():
            if name.startswith(("CHASSIS_FRAME_", "J13_DECK_INSERT", "BODY_CHASSIS_M4_", "AXLE_MOTOR_CARRIER_", "J04_",
                                "BODY_CHASSIS_LOCATING_PIN_")):   # pins sit in the module's own holes (row below)
                continue
            pb = part.bounding_box()
            if (pb.min.X > fb.max.X + 2 or pb.max.X < fb.min.X - 2 or pb.min.Y > fb.max.Y + 2 or pb.max.Y < fb.min.Y - 2
                    or pb.min.Z > fb.max.Z + 2 or pb.max.Z < fb.min.Z - 2):
                continue
            gap = BRepExtrema_DistShapeShape(fill.wrapped, part.wrapped).Value()
            if gap < 2.0:
                near.append((round(gap, 2), name))
        c = fb.center()
        carrier_overlap = sum(sum(s.volume for s in (fill & chassis[f"AXLE_MOTOR_CARRIER_{t}"]).solids()) for t in ("L", "R"))
        check(f"J13 fill and boss at ({c.X:.0f}, {c.Y:.0f}) clear by 1.0 mm", all(g >= 1.0 for g, _ in near) and carrier_overlap < TOL,
              f"nearest {sorted(near)[:4] or 'none within 2 mm'}; carrier overlap {carrier_overlap:.3f} mm3")
    for px, py, pr in J["pin_holes"]:
        mod = front if px > 0 else rear
        through = all(not solid_at(mod, (px + dx, py + dy, z)) for z in (45.0, 50.0, 54.0)
                      for dx, dy in ((pr - 0.1, 0), (-(pr - 0.1), 0), (0, pr - 0.1), (0, -(pr - 0.1))))
        check(f"J13 locating-pin hole ({px}, {py}) Ø{2 * pr:.1f} still through the deck and boss", through, f"open {through}")
    open_fl = all(not solid_at(front, (64.0 + dx, 48.0 + dy, 42.0)) for dx, dy in ((4.5, 0), (-4.5, 0), (0, 4.5), (0, -4.5)))
    check("J13 front-left (64, 48) socket stays open for its bolt from below", open_fl and "BODY_CHASSIS_M4_NUT_4" in body,
          f"open {open_fl}; cassette nut kept")

    # 2. Rear J04 key walls.
    for tag in ("L", "R"):
        now = key_walls(rear, chassis[f"AXLE_MOTOR_CARRIER_{tag}"])
        was = key_walls(raw["CHASSIS_FRAME_REAR_MODULE"], chassis[f"AXLE_MOTOR_CARRIER_{tag}"])
        ref = key_walls(front, chassis[f"AXLE_MOTOR_CARRIER_{tag}"])
        check(f"rear J04 key {tag} walled on all sides (as the front)", all(now[s] >= ref[s] - 5 for s in now),
              f"rear {now}; front {ref}")
        check(f"planted: unedited rear key {tag} inner wall missing", was["inner"] < 20, f"unedited {was}")

    # 3. J04 L-key, motor out.
    frame_state = subset(chassis, ("CHASSIS_FRAME_", "AXLE_MOTOR_CARRIER_", "J04_"))
    blocked = []
    for name, screw in subset(chassis, ("J04_CARRIER_SCREW_",)).items():
        bb = screw.bounding_box()
        sx = 1.0 if bb.center().X > 0 else -1.0
        x_head, y, z = sx * 15.0, bb.center().Y, bb.center().Z
        key = xc(1.155, *sorted((x_head, x_head - sx * 16.0)), y, z) + zc(1.155, z, 160.0, x_head - sx * 16.0, y)
        h = hits(key, frame_state, skip=(name,))
        check(f"J04 {name[-12:]} L-key, motor out", not h, f"{h or 'clear'}")
        blocked.append(bool(hits(key, subset(chassis, ("MOTOR_",)))))
    check("planted: the motor blocks every J04 key", all(blocked), f"{sum(blocked)}/{len(blocked)}")

    # 4. J11A from below, body on.
    everything = {**chassis, **body}
    for name, screw in subset(chassis, ("J11A_HATCH_SCREW_",)).items():
        c, bb = screw.bounding_box().center(), screw.bounding_box()
        h = hits(zc(1.155, -40.0, bb.min.Z + 0.2, c.X, c.Y), everything, skip=(name,))
        check(f"J11A {name[-1]} key from below, body on", not h, f"{h or 'clear'}")

    # 5. J12 ballast.
    bar = chassis["BALLAST_STEEL_BAR"]
    drop = box(69.5, 78.5, -30.0, 30.0, -10.0, 33.0)
    open_state = subset(chassis, drop=("BALLAST_", "BATTERY_", "PACK_", "J11A_HATCH_SCREW"))
    h = hits(drop, open_state)
    check("J12 bar drops out with the hatch and pack out", not h, f"{h or 'clear'}")
    check("planted: the hatch blocks the bar", bool(hits(drop, subset(chassis, ("BATTERY_TUB_BOTTOM_HATCH",)))), "hatch in the way")
    for y in (-20.0, 20.0):
        h = hits(zc(2.25, 56.0, 200.0, 74.0, y), chassis, skip=("BALLAST_",))
        check(f"J12 (74, {y}) PH1 from above, body off", not h, f"{h or 'clear'}")

    # 6. J13 keys, body frame only.
    frame_on = {**chassis, **subset(body, ("BODY_FRAME_MAIN_PRINT", "BODY_FRAME_FRONT_LEFT_FOOT_CASSETTE", "BODY_CHASSIS_"))}
    for k, (x, y) in enumerate(J["points"], start=1):
        head = body[f"BODY_CHASSIS_M4_HEAD_{k}"].bounding_box()
        h = hits(zc(1.443, head.max.Z - 1.5, 200.0, x, y), frame_on, skip=("BODY_CHASSIS_M4_",))
        check(f"J13 ({x}, {y}) 2.5 mm key from above, body frame only", not h, f"{h or 'clear'}")
    head = body["BODY_CHASSIS_M4_HEAD_4"]
    hb = head.bounding_box()
    key = zc(1.443, -20.0, hb.min.Z + 1.5, 64.0, 48.0)
    h = hits(key, everything, skip=("BODY_CHASSIS_M4_",))
    gap = BRepExtrema_DistShapeShape(key.wrapped, chassis["BATTERY_TUB_BOTTOM_HATCH"].wrapped).Value()
    check("J13 front-left (64, 48) 2.5 mm key from below, hatch on", not h and gap >= 1.0, f"{h or 'clear'}; {gap:.2f} mm to the hatch")
    # D-076: the bolt itself (head R4.0) comes out downward past the notched hatch.
    path = zc(4.0, -20.0, hb.max.Z, 64.0, 48.0)
    h = hits(path, everything, skip=("BODY_CHASSIS_M4_",))
    gap = BRepExtrema_DistShapeShape(path.wrapped, chassis["BATTERY_TUB_BOTTOM_HATCH"].wrapped).Value()
    check("J13 front-left bolt comes out downward with the hatch on (D-076)", not h and gap >= 0.5, f"{h or 'clear'}; {gap:.2f} mm to the hatch notch")
    check("planted: the unnotched hatch blocks that bolt", bool(hits(path, {"hatch": raw["BATTERY_TUB_BOTTOM_HATCH"]})), "head meets the hatch")

    # 7. J15A, J15B from above, body off.
    for name, head in subset(chassis, ("IMU_M2_SCREW_HEAD_",)).items():
        c, bb = head.bounding_box().center(), head.bounding_box()
        h = hits(zc(1.5, bb.max.Z - 0.5, 200.0, c.X, c.Y), chassis, skip=("IMU_M2_SCREW",))
        check(f"J15A {name[-1]} driver from above, body off", not h, f"{h or 'clear'}")
    for x, y in entry.FRAME_FIX["post_xy"]:
        h = hits(zc(0.87, 68.6, 200.0, x, y), chassis, skip=("DRIVER_SCREW_",))
        check(f"J15B ({x}, {y}) 1.5 mm key from above, body off", not h, f"{h or 'clear'}")

    # 8. Backing dowel under the inner posts, hatch and pack out.
    for x, y in entry.FRAME_FIX["post_xy"][::2]:
        sy = 1.0 if y > 0 else -1.0
        yd = y - sy * 2.0                     # under the half of the post over the aperture
        dowel = zc(1.5, -10.0, 55.9, x, yd)
        h = hits(dowel, open_state)
        under = not solid_at(front, (x, yd, 53.0))
        check(f"J15B inner post ({x}, {y}) backed by a Ø3 dowel from below", not h and under,
              f"{h or 'clear'}; post underside open over the aperture: {under}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
