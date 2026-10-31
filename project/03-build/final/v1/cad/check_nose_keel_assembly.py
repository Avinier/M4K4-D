"""Nose and keel assembly and service (nose and keel pages §6): tool access and removal paths per
joint in the state each step is done in, measured on the chassis and body trees with the droid edits
applied. Body on throughout unless a row says otherwise.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md, plus
../../../01-chassis/v1/cad. Builds the chassis tree and the body once, about 5 min.

Tools are modelled across their corners: 2 mm hex r 1.155 (ISO 7380 M3), 2.5 mm hex r 1.443
(ISO 4762 M3), PH0 shaft r 1.5 (M2 pan and countersunk thread-formers), a Ø6 iron tip r 3.0.
Parts are swept along their removal path in 1 mm steps. Checks:

1. J07A: the 2 mm key reaches each caster screw from below with the housing, ball and rollers
   unsnapped; the base then drops 40 mm. Planted: the housing blocks the keys.
2. J08B: the cap slides 20 mm forward with its fingers spread (hooks out of their slots). Planted:
   with the hooks in, the slot walls stop it.
3. J08C: the PH0 reaches the lid screw from above; with the cap off and the screw out the lid
   slides 12 mm forward, then lifts 40 mm. Planted: the cap stops the lid sliding.
4. J08A: the GP2Y and its soldered lead lift 40 mm, lid and cap off. Planted: the lid holds it.
5. J08B: the Hall board lifts 30 mm out of its slot once the GP2Y is out. Planted: the GP2Y.
6. J07B: body off; a short 2 mm L-key enters above the open pocket, cap, lid and GP2Y out;
   then the pod, with the caster, Hall board and springs, slides 40 mm forward out of the shell
   notch. Planted: the GP2Y blocks the keys; the screws hold the pod.
7. Inserts: the iron reaches each crossmember pod pilot along -X with the pod off (frame on the
   bench), and each keel pilot from below.
8. J09A: the 2.5 mm key reaches each keel screw from below with the keel, shoe and bezel fitted;
   with the screws out (and the TCRT out, item 9) the keel drops 40 mm through the shell slot.
   Planted: a screw holds the keel.
9. J09B: the PH0 reaches the bezel screw from below; the bezel and shims drop 30 mm; then the TCRT
   and its lead joint drop 40 mm out of the pocket. Planted: the bezel holds the TCRT.
10. J10A: the PH0 reaches the shoe screw from +Y, wheels on; with it out the shoe slides 15 mm
    forward out of the groove. Planted: the screw holds the shoe.
"""

import importlib.util
from pathlib import Path
import sys

from build123d import Axis, Box, Cylinder, Location

import body_v1_model as B
import body_chassis_model as M  # 01-chassis/v1/cad on PYTHONPATH

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

TOL = 1e-3
SKIP = ("RESERVE", "KEEP_OUT", "CORRIDOR", "SLIDE_PATH", "OPTICAL_AXIS", "PHYSICS", "AXES", "HARNESS_", "TRAVEL")
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
        elif node.label == "GP2Y_J10_8_SOLDERED_LEAD_RESERVE" or not any(s in (node.label or "") for s in SKIP):
            out[node.label or f"?{len(out)}"] = entry._shifted(node, loc)
    walk(tree, Location())
    return out


def zc(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def xc(r, x0, x1, y, z):
    return Cylinder(r, x1 - x0, rotation=(0, 90, 0)).moved(Location(((x0 + x1) / 2.0, y, z)))


def yc(r, y0, y1, x, z):
    return Cylinder(r, y1 - y0, rotation=(90, 0, 0)).moved(Location((x, (y0 + y1) / 2.0, z)))


def _near(a, b, pad=0.0):
    return not (a.min.X > b.max.X + pad or a.max.X < b.min.X - pad or a.min.Y > b.max.Y + pad or a.max.Y < b.min.Y - pad
                or a.min.Z > b.max.Z + pad or a.max.Z < b.min.Z - pad)


_part_bounds = {}


def bounds(part):
    key = id(part)
    if key not in _part_bounds:
        _part_bounds[key] = (part, part.bounding_box())
    return _part_bounds[key][1]


def hits(tool, parts, skip=()):
    tb = tool.bounding_box()
    out = {}
    for name, part in parts.items():
        if name.startswith(skip) or not _near(bounds(part), tb):
            continue
        intersection = tool & part
        v = sum(s.volume for s in intersection.solids()) if intersection is not None else 0.0
        if v > TOL:
            out[name] = round(v, 2)
    return out


def sweep(moving, vector, distance, state):
    """First hit of each fixed part as the moving parts travel along vector, 1 mm steps."""
    assert moving, "service sweep selected no moving parts"
    first = {}
    fixed = {k: v for k, v in state.items() if k not in moving}
    for step in range(1, int(distance) + 1):
        for part in moving.values():
            moved = entry._shifted(part, Location(tuple(c * step for c in vector)))
            for name in hits(moved, fixed):
                first.setdefault(name, step)
    return first


def pick(parts, prefixes):
    return {k: v for k, v in parts.items() if k.startswith(prefixes)}


def drop(parts, prefixes):
    return {k: v for k, v in parts.items() if not k.startswith(prefixes)}


def main():
    chassis = leaves(entry._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    body = leaves(entry._apply_droid_cuts(B.build_body_assembly(), strict=False))
    allp = {**chassis, **body}
    lead = pick(chassis, ("GP2Y_J10_8_SOLDERED_LEAD_RESERVE",))
    check("J08A final-tree soldered lead reserve is included", len(lead) == 1,
          f"{list(lead)}")

    # 1. J07A caster, from below.
    caster_off = ("BALL_TRANSFER_PURCHASED_HOUSING", "BALL_TRANSFER_POM_BALL", "BALL_TRANSFER_ROLLER_")
    state = drop(allp, caster_off)
    blocked = []
    for k in range(1, 4):
        head = chassis[f"BALL_M3_HEAD_{k}"].bounding_box()
        c = head.center()
        key = zc(1.155, -60.0, head.min.Z + 0.5, c.X, c.Y)
        h = hits(key, state, skip=(f"BALL_M3_HEAD_{k}", f"BALL_M3_SHANK_{k}"))
        check(f"J07A screw {k}: 2 mm key from below, housing and ball unsnapped", not h, f"{h or 'clear'}")
        blocked.append(bool(hits(key, pick(allp, caster_off))))
    check("planted: the caster housing blocks every J07A key", all(blocked), f"{sum(blocked)}/3")
    h = sweep(pick(chassis, caster_off), (0, 0, -1), 40, allp)
    check("J07A housing, ball and rollers drop 40 mm after unsnapping", not h, f"{h or 'clear'}")
    base = pick(chassis, ("BALL_TRANSFER_PURCHASED_3HOLE_FLANGE",))
    h = sweep(base, (0, 0, -1), 40, drop(state, ("BALL_M3_",)))
    check("J07A caster base drops 40 mm, screws out", not h, f"{h or 'clear'}")

    # 2. J08B cap, fingers spread.
    hz = M.TACTILE_SNAP_HOOK_X, M.TACTILE_SNAP_HOOK_Z
    hook_zone = Box(hz[0][2] - hz[0][0] + 0.02, 60.0, hz[1][1] - hz[1][0]).moved(
        Location(((hz[0][0] + hz[0][2]) / 2.0, 0.0, (hz[1][0] + hz[1][1]) / 2.0)))
    cap = chassis["BALL_NOSE_TOUCH_CAP"]
    moving = {"cap": cap - hook_zone, "magnet": chassis["BALL_NOSE_MAGNET_D3X1P5_N35"]}
    h = sweep(moving, (1, 0, 0), 20, drop(allp, ("BALL_NOSE_TOUCH_CAP", "BALL_NOSE_MAGNET", "BALL_NOSE_RETURN_SPRING")))
    check("J08B cap slides 20 mm forward, fingers spread", not h, f"{h or 'clear'}")
    h = sweep({"cap": cap}, (1, 0, 0), 3, drop(allp, ("BALL_NOSE_TOUCH_CAP", "BALL_NOSE_MAGNET", "BALL_NOSE_RETURN_SPRING")))
    check("planted: with the hooks in, the slot walls hold the cap", "BALL_POD_PRINTED_SEAT" in h, f"{h}")

    # 3. J08C lid.
    lx, ly = M.LID_SCREW_XY
    top = chassis["BALL_POD_LID_M2X8_CSK_SCREW"].bounding_box().max.Z
    h = hits(zc(1.5, top - 0.5, 200.0, lx, ly), allp, skip=("BALL_POD_LID_M2X8",))
    check("J08C PH0 onto the lid screw from above, body on", not h, f"{h or 'clear'}")
    lid_state = drop(allp, ("BALL_NOSE_TOUCH_CAP", "BALL_NOSE_MAGNET", "BALL_NOSE_RETURN_SPRING", "BALL_POD_LID_M2X8"))
    lid = pick(chassis, ("BALL_POD_SENSOR_LID",))
    h = sweep(lid, (1, 0, 0), 11, lid_state)
    check("J08C lid slides 11 mm forward, cap off, screw out", not h, f"{h or 'clear'}")
    lid_fwd = {k: entry._shifted(v, Location((11.0, 0.0, 0.0))) for k, v in lid.items()}
    h = sweep(lid_fwd, (0, 0, 1), 40, lid_state)
    check("planted: lifting after only 11 mm meets the speaker panel", "FRONT_SERVICE_PANEL_EXPOSED_SPEAKER" in h, f"{h}")
    h = sweep(lid, (1, 0, 0), 12, lid_state)
    check("J08C lid slides 12 mm forward before lifting", not h, f"{h or 'clear'}")
    lid_fwd = {k: entry._shifted(v, Location((12.0, 0.0, 0.0))) for k, v in lid.items()}
    h = sweep(lid_fwd, (0, 0, 1), 40, lid_state)
    check("J08C lid lifts 40 mm after the 12 mm slide", not h, f"{h or 'clear'}")
    h = sweep(lid, (1, 0, 0), 14, lid_state)
    check("planted: over-sliding the lid meets the GP2Y at 13 mm", "GP2Y0A21YK0F_STEP" in h, f"{h}")
    h = sweep(lid, (1, 0, 0), 11, drop(allp, ("BALL_POD_LID_M2X8",)))
    check("planted: with the cap on, the lid can't slide", bool(h), f"{h}")

    # 4. J08A GP2Y up.
    sensor = pick(chassis, ("GP2Y0A21YK0F_STEP", "GP2Y_J10_8_SOLDERED_LEAD"))
    open_state = drop(lid_state, ("BALL_POD_SENSOR_LID",))
    h = sweep(sensor, (0, 0, 1), 40, open_state)
    check("J08A GP2Y and lead lift 40 mm, cap and lid off", not h, f"{h or 'clear'}")
    h = sweep(sensor, (0, 0, 1), 4, drop(allp, ("BALL_NOSE_TOUCH_CAP", "BALL_NOSE_MAGNET")))
    check("planted: the lid holds the GP2Y down", "BALL_POD_SENSOR_LID" in h, f"{h}")

    # 5. J08B Hall board up.
    hall = pick(chassis, ("BALL_NOSE_HALL_",))
    no_sensor = drop(open_state, ("GP2Y0A21YK0F_STEP", "GP2Y_J10_8_SOLDERED_LEAD"))
    h = sweep(hall, (0, 0, 1), 30, no_sensor)
    check("J08B Hall board lifts 30 mm out of its slot, GP2Y out", not h, f"{h or 'clear'}")
    h = sweep(hall, (0, 0, 1), 30, open_state)
    check("planted: the GP2Y stands over the Hall slot", any(k.startswith("GP2Y") for k in h), f"{h}")

    # 6. J07B pod screws: short L-key from above with the body off.
    pod_tool_state = {k: v for k, v in no_sensor.items() if k in chassis}  # body off
    blocked = []
    for k in range(1, 3):
        head = chassis[f"BALL_POD_M3_HEAD_{k}"].bounding_box()
        c = head.center()
        # Shortened L-key: 8 mm from the head face to bend, long leg up.
        # A full-length straight key meets the lid boss on the -Y side.
        bend = head.max.X + 8.0
        key = xc(1.155, head.max.X - 0.5, bend, c.Y, c.Z) + zc(1.155, c.Z, 100.0, bend, c.Y)
        h = hits(key, pod_tool_state, skip=(f"BALL_POD_M3_HEAD_{k}", f"BALL_POD_M3_SHANK_{k}"))
        check(f"J07B screw {k}: short 2 mm L-key, body off, cap, lid and GP2Y out", not h, f"{h or 'clear'}")
        tool_state = drop(pod_tool_state, (f"BALL_POD_M3_HEAD_{k}", f"BALL_POD_M3_SHANK_{k}"))
        h = sweep({"key": key}, (0, 0, 1), 40, tool_state)
        check(f"J07B screw {k}: L-key enters from above, body off", not h, f"{h or 'clear'}")
        swing = {}
        angles = range(0, 66) if c.Y > 0 else range(-65, 1)
        for angle in angles:
            posed = key.rotate(Axis((0, c.Y, c.Z), (1, 0, 0)), angle)
            for name in hits(posed, tool_state):
                swing.setdefault(name, angle)
        check(f"J07B screw {k}: 60 degree inward L-key swing for hex re-indexing", not swing, f"{swing or 'clear'}")
        if k == 2:
            h = sweep({"key": key}, (0, 0, 1), 40,
                      drop(no_sensor, (f"BALL_POD_M3_HEAD_{k}", f"BALL_POD_M3_SHANK_{k}")))
            check("planted: the fitted body blocks L-key entry", "BODY_SHELL" in h, f"{h}")
        straight = xc(1.155, head.max.X - 0.5, 220.0, c.Y, c.Z)
        blocked.append(any(n.startswith("GP2Y") for n in hits(straight, sensor)))
        if k == 2:
            h = hits(straight, no_sensor, skip=(f"BALL_POD_M3_HEAD_{k}", f"BALL_POD_M3_SHANK_{k}"))
            check("planted: a straight J07B -Y key meets the lid boss", "BALL_POD_PRINTED_SEAT" in h, f"{h}")
    check("planted: the GP2Y blocks both straight J07B keys", all(blocked), f"{sum(blocked)}/2")
    pod = pick(no_sensor, ("BALL_POD_PRINTED_SEAT", "BALL_SEAT_HEATSET_INSERT_", "BALL_TRANSFER_", "BALL_M3_", "BALL_NOSE_HALL_",
                           "BALL_NOSE_RETURN_SPRING"))
    h = sweep(pod, (1, 0, 0), 40, drop(no_sensor, ("BALL_POD_M3_",)))
    check("J07B pod and caster slide 40 mm forward out of the shell notch, screws out", not h, f"{h or 'clear'}")
    h = sweep(pod, (1, 0, 0), 2, no_sensor)
    check("planted: the J07B screws hold the pod", any(n.startswith("BALL_POD_M3_") for n in h), f"{h}")

    # 7. Inserts, frame on the bench.
    seat = {"seat": chassis["BALL_POD_PRINTED_SEAT"]}
    for k, (x, y) in enumerate(M.ball_screw_points(), start=1):
        h = hits(zc(3.0, -40.0, 28.95, x, y), seat)
        check(f"Iron from below into caster seat pilot {k}, caster off", not h, f"{h or 'clear'}")
    front = {"front": chassis["CHASSIS_FRAME_FRONT_MODULE"]}
    for y, z in M.BALL_POD_SCREWS_YZ:
        h = hits(xc(3.0, 92.05, 160.0, y, z), front)
        check(f"Iron along -X into the crossmember pod pilot Y{y:+.0f}, pod off", not h, f"{h or 'clear'}")
    rear = {"rear": chassis["CHASSIS_FRAME_REAR_MODULE"]}
    for x, y in M.rear_keel_screw_points():
        h = hits(zc(3.0, -40.0, 33.95, x, y), rear)
        check(f"Iron from below into the keel pilot ({x}, {y:+})", not h, f"{h or 'clear'}")

    # 8. J09A keel screws and the keel drop.
    for k in range(1, 5):
        sb = chassis[f"REAR_KEEL_M3X30_SCREW_{k}"].bounding_box()
        c = sb.center()
        h = hits(zc(1.443, -60.0, sb.min.Z + 1.5, c.X, c.Y), allp, skip=(f"REAR_KEEL_M3X30_SCREW_{k}",))
        check(f"J09A screw {k}: 2.5 mm key from below, keel, shoe and bezel on", not h, f"{h or 'clear'}")
    tcrt = ("TCRT5000_REAR_", "TCRT_REAR_LEAD_", "TCRT_REAR_J10_10_", "REAR_TCRT_")
    keel = pick(allp, ("REAR_KEEL_FACETED_BODY", "REAR_KEEL_REPLACEABLE_WEAR_SHOE", "REAR_KEEL_SHOE_M2X6"))
    h = sweep(keel, (0, 0, -1), 40, drop(allp, ("REAR_KEEL_M3X30_",) + tcrt))
    check("J09A keel drops 40 mm through the shell slot, screws and TCRT out", not h, f"{h or 'clear'}")
    h = sweep(keel, (0, 0, -1), 2, drop(allp, tcrt))
    check("planted: the J09A screws hold the keel", any(n.startswith("REAR_KEEL_M3X30_") for n in h), f"{h}")

    # 9. J09B bezel, shims, TCRT.
    sb = chassis["REAR_TCRT_BEZEL_M2X10_SCREW"].bounding_box()
    c = sb.center()
    h = hits(zc(1.5, -60.0, sb.min.Z + 0.5, c.X, c.Y), allp, skip=("REAR_TCRT_BEZEL_M2X10",))
    check("J09B PH0 onto the bezel screw from below", not h, f"{h or 'clear'}")
    bezel = pick(allp, ("REAR_TCRT_BEZEL_WITH_GUARDS", "REAR_TCRT_HEIGHT_SHIM_"))
    h = sweep(bezel, (0, 0, -1), 30, drop(allp, ("REAR_TCRT_BEZEL_M2X10",)))
    check("J09B bezel and shims drop 30 mm, screw out", not h, f"{h or 'clear'}")
    sensor = pick(allp, ("TCRT5000_REAR_", "TCRT_REAR_LEAD_"))
    h = sweep(sensor, (0, 0, -1), 40, drop(allp, ("REAR_TCRT_", "TCRT_REAR_J10_10_")))
    check("J09B TCRT and its lead joint drop 40 mm out of the pocket, bezel off", not h, f"{h or 'clear'}")
    h = hits(entry._shifted(sensor["TCRT5000_REAR_STEP"], Location((0, 0, -0.05))),
             pick(allp, ("REAR_TCRT_BEZEL_WITH_GUARDS",)))
    check("planted: the bezel holds the TCRT", "REAR_TCRT_BEZEL_WITH_GUARDS" in h, f"{h}")

    # 10. J10A shoe.
    sb = chassis["REAR_KEEL_SHOE_M2X6_SCREW"].bounding_box()
    c = sb.center()
    h = hits(yc(1.5, sb.max.Y - 0.5, 140.0, c.X, c.Z), allp, skip=("REAR_KEEL_SHOE_M2X6",))
    check("J10A PH0 onto the shoe screw from +Y, wheels on", not h, f"{h or 'clear'}")
    shoe = pick(allp, ("REAR_KEEL_REPLACEABLE_WEAR_SHOE",))
    h = sweep(shoe, (1, 0, 0), 15, drop(allp, ("REAR_KEEL_SHOE_M2X6",)))
    check("J10A shoe slides 15 mm forward, screw out", not h, f"{h or 'clear'}")
    h = sweep(shoe, (1, 0, 0), 2, allp)
    check("planted: the screw holds the shoe", "REAR_KEEL_SHOE_M2X6_SCREW" in h, f"{h}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
