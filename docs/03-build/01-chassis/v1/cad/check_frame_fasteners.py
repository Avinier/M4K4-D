"""Fast checks for the D-030 frame fasteners, pack restraint and driver mounts.

Covers J05/J06 (crossmember to rails), J16 (decks to rails), J11A (hatch
screws), J11B (pack straps and foam), J15B (driver posts and tie lugs), the
ISO 7380 heads at J01/J04 and the ISO 4029 M3 x 3 set screw. Run from this
folder with the text-to-cad 0.4.28 runtime:
python check_frame_fasteners.py
Writes generated/frame-fastener-checks.json.
"""
import json
import math
import os
import sys

sys.path.insert(0, ".")
M = __import__(os.environ.get("CHECK_MODEL", "body_chassis_model"))
from build123d import Location  # noqa: E402  (after the model import; never `import *`, it shadows M)


def _vol(s):
    return 0.0 if s is None else s.volume


def leaves(s):
    k = getattr(s, "children", None)
    return [l for c in k for l in leaves(c)] if k else [s]


def meet(a, b, tol=1e-6):
    # Containment counts as meeting (BoundBox.overlaps() misses it).
    p, q = a.bounding_box(), b.bounding_box()
    return (p.min.X < q.max.X - tol and q.min.X < p.max.X - tol and p.min.Y < q.max.Y - tol
            and q.min.Y < p.max.Y - tol and p.min.Z < q.max.Z - tol and q.min.Z < p.max.Z - tol)


def near(a, b, pad):
    p, q = a.bounding_box(), b.bounding_box()
    return (p.min.X - pad < q.max.X and q.min.X - pad < p.max.X and p.min.Y - pad < q.max.Y
            and q.min.Y - pad < p.max.Y and p.min.Z - pad < q.max.Z and q.min.Z - pad < p.max.Z)


def span(s, axis):
    b = s.bounding_box()
    return {"X": (b.min.X, b.max.X), "Y": (b.min.Y, b.max.Y), "Z": (b.min.Z, b.max.Z)}[axis]


def overlap_len(a, b):
    return round(max(0.0, min(a[1], b[1]) - max(a[0], b[0])), 3)


frame = M.chassis_frame()
frame_parts = leaves(frame)
by = {p.label: p for p in frame_parts}
decks = [p for p in frame_parts if p.label == "CHASSIS_DECK_WITH_BODY_INTERFACE"]  # REAR, FRONT
deck_rear, deck_front = decks
# The new hardware is taken from the assembled frame, so each solid exists once.
_labels = lambda c: {l.label for l in leaves(c)}
hardware = [p for p in frame_parts if p.label in _labels(M.frame_joint_hardware())]
restraint = [p for p in frame_parts if p.label in _labels(M.battery_restraint())]
driver_hw = [p for p in frame_parts if p.label in _labels(M.driver_mount_hardware())]
el = M.electronics()
drivers = [c for c in el.children if c.label.startswith("ADAFRUIT_3297")]
driver_leaves = [l for d in drivers for l in leaves(d)]
battery = next(c for c in el.children if c.label == "BATTERY_2S1P_18650_PACK")
pack = leaves(battery)
shell = next(l for l in leaves(M.body_shell()) if l.label == "BODY_SHELL")
others = [
    *frame_parts, shell, *leaves(M.body_panels()), *leaves(M.panel_mount_hardware()), *leaves(M.body_primary_frame()),
    *[l for c in el.children if c.label != battery.label for l in leaves(c)], *pack,
    *M.sensors().children, *leaves(M.harness_routes()), *leaves(M.body_audio()),
    *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R")),
    *leaves(M.wheel_assembly("L")), *leaves(M.wheel_assembly("R")),
    *leaves(M.bearing_pair("L")), *leaves(M.bearing_pair("R")),
    *leaves(M.body_chassis_mount_hardware()), *leaves(M.rear_skid_tcrt_module()), *leaves(M.ball_transfer()),
]
R = {}

# 1. Clashes of every changed or new solid against the whole model.
changed = [
    *[p for p in frame_parts if p.label.startswith(("CHASSIS_RAIL_", "FRONT_CROSSMEMBER", "REAR_SKID_CROSSMEMBER",
                                                    "BATTERY_TUB", "AXLE_MOTOR_CARRIER_", "AXLE_BEARING_HOUSING_",
                                                    "AXLE_MOTOR_SCREW_", "J04_CARRIER_SCREW_"))],
    *decks, *hardware, *restraint, *driver_hw, *driver_leaves,
    *[l for s in "LR" for l in leaves(M.wheel_assembly(s)) if "SET_SCREW" in l.label],
]
seen, clashes = set(), {}
for part in changed:
    for other in others + [p for p in changed if p not in others]:
        if other is part or other.label == part.label or not meet(part, other):
            continue
        key = frozenset((id(part), id(other)))
        if key in seen:
            continue
        seen.add(key)
        v = _vol(part & other)
        if v > 1e-3:
            clashes[f"{part.label} x {other.label}"] = round(v, 3)
# Designed overlaps recorded before D-030 and unchanged by it: the IMU M2 shanks
# thread 4 mm into the deck (D-028); the CNC Kitchen inserts' 0.3 mm knurl
# interference in the crossmembers (D-011, D-014); the motor-face screw threads in
# the gearbox (measured by check_layout.py motor_face_joint_is_engaged).
ACCEPTED = {k for k in clashes if ("IMU_M2_SCREW_SHANK" in k and "CHASSIS_DECK_WITH_BODY_INTERFACE" in k)
            or ("CROSSMEMBER" in k and "HEATSET_INSERT" in k)
            or ("AXLE_MOTOR_SCREW_M3X6_" in k and "_GEARBOX" in k)}
R["clashes"] = {k: v for k, v in clashes.items() if k not in ACCEPTED}
R["accepted_overlaps"] = {k: clashes[k] for k in ACCEPTED}
os.makedirs("generated", exist_ok=True)
with open("generated/frame-fastener-checks.partial.json", "w") as f:
    json.dump(R, f, indent=2)  # progress copy; the full run takes ~20 min
print("clash sweep done", flush=True)

# 2. Thread engagement: screw shank span inside its insert, along the screw axis.
def shank_span(screw, axis, r=1.5):
    return span(screw, axis) if axis != "Z" else span(screw, "Z")


def engagement(screw_label, insert_label, axis):
    sc, ins = next(h for h in hardware if h.label == screw_label), next(h for h in hardware if h.label == insert_label)
    return overlap_len(span(sc, axis), span(ins, axis))


eng = {}
for j in ("J05", "J06"):
    length = M.J05_SCREW[0] if j == "J05" else M.J06_SCREW[0]
    for s in "LR":
        eng[f"{j}_{s}"] = engagement(f"{j}_SCREW_M3X{int(length)}_{s}", f"{j}_RAIL_INSERT_M3_{s}", "X")
for k in range(1, len(M.J16_POINTS) + 1):
    for s in "LR":
        sc = next(h for h in hardware if h.label == f"J16_SCREW_M3X10_{k}_{s}")
        ins = next(h for h in hardware if h.label == f"J16_RAIL_INSERT_M3_{k}_{s}")
        eng[f"J16_{k}_{s}"] = overlap_len((span(sc, "Z")[0], M.DECK_Z + 2.0), span(ins, "Z"))
for k in range(1, 5):
    sc = next(h for h in hardware if h.label == f"J11A_HATCH_SCREW_M3X6_{k}")
    ins = next(h for h in hardware if h.label == f"J11A_BOSS_INSERT_M3_{k}")
    eng[f"J11A_{k}"] = overlap_len((M.BATTERY_TUB_FLOOR_Z[0], span(sc, "Z")[1]), span(ins, "Z"))
for k, h in enumerate([h for h in driver_hw if "SCREW" in h.label], start=1):
    ins = next(i for i in driver_hw if i.label == f"DRIVER_POST_INSERT_M25_{k}")
    eng[f"J15B_{k}"] = overlap_len((span(h, "Z")[0], M.DRIVER_PCB_Z + M.PCB_THICKNESS), span(ins, "Z"))
R["thread_engagement_mm"] = eng

# 3. Inserts can be pressed in: sweep each insert 15 mm out of its pilot along the
# press direction and intersect with its own host print only.
rails = {p.label: p for p in frame_parts if p.label.startswith("CHASSIS_RAIL_")}
press = {}
for h in hardware + driver_hw:
    if "INSERT" not in h.label:
        continue
    b = h.bounding_box()
    if h.label.startswith(("J05", "J06")):
        side, region = h.label[-1], "FRONT" if h.label.startswith("J05") else "REAR"
        host, d = rails[f"CHASSIS_RAIL_{side}_{region}"], (1.0 if region == "FRONT" else -1.0, 0.0, 0.0)
    elif h.label.startswith("J16"):
        side = h.label[-1]
        region = "FRONT" if b.center().X > 0 else "REAR"
        host, d = rails[f"CHASSIS_RAIL_{side}_{region}"], (0.0, 0.0, 1.0)
    elif h.label.startswith("J11A"):
        host, d = deck_front, (0.0, 0.0, -1.0)
    else:
        host, d = deck_front, (0.0, 0.0, 1.0)
    path = h
    for step in range(1, 16):
        path = path + h.moved(Location(tuple(c * step for c in d)))
    press[h.label] = round(_vol(path & host), 3)
R["insert_press_path_overlap_mm3"] = press

# 4. J05/J06 tongues seat in their pockets (fit allowance, no clash).
R["tongue_side_clearance_mm"] = round(M.RAIL_POCKET_HALF_Y - M.RAIL_TONGUE_HALF_Y, 3)
R["tongue_insert_wall_mm"] = round(M.RAIL_TONGUE_HALF_Y - M.FRAME_INSERT_RADIUS, 3)

# 5. Set screw (ISO 4029 M3 x 3 faced to 2.5): the screw itself turned about the axle in 3 deg steps.
set_screw = {}
for s in "LR":
    wheel = {c.label: c for c in M.wheel_assembly(s).children}
    scr = wheel[f"WHEEL_{s}_SET_SCREW_M3X2_5"]
    r_max = max(math.hypot(v.X, v.Z - M.AXLE_Z) for v in scr.vertices())
    b = scr.bounding_box()
    ring = M._axial_bore_y(r_max, b.min.Y, b.max.Y, 0.0, M.AXLE_Z)  # candidate filter only
    static = [p for p in frame_parts if p.label.startswith(("AXLE_", "J04"))] + leaves(M.motor_envelope(s))
    static = [t for t in static if "OUTPUT_SHAFT" not in t.label and near(ring, t, 3.0)]
    axle = M.Axis((0.0, 0.0, M.AXLE_Z), (0.0, 1.0, 0.0))
    gap = min((round(scr.rotate(axle, a).distance_to(t), 3), t.label) for a in range(0, 360, 3) for t in static)
    shaft = next(c for c in M.motor_envelope(s).children if "OUTPUT_SHAFT" in c.label)
    set_screw[s] = {"r_max_mm": round(r_max, 3), "min_swept_gap_mm": gap[0], "to": gap[1],
                    "on_shaft_flat_mm": round(scr.distance_to(shaft), 4),
                    "proud_of_stub_mm": round(b.max.Z - (M.AXLE_Z + M.STUB_SHAFT_RADIUS), 3)}
R["set_screw"] = set_screw

# 6. Motor-face and J04 button heads seat on their counterbore/recess floors.
heads = {}
for p in frame_parts:
    if p.label.startswith("AXLE_MOTOR_SCREW_M3X6_"):
        s = p.label.split("_")[-2]
        heads[p.label] = {"to_carrier_mm": round(p.distance_to(by[f"AXLE_MOTOR_CARRIER_{s}"]), 4),
                          "to_inner_bearing_mm": round(p.distance_to(M.bearing_pair(s).children[0]), 3)}
    elif p.label.startswith("J04_CARRIER_SCREW_"):
        s = p.label.split("_")[4]
        heads[p.label] = {"to_carrier_mm": round(p.distance_to(by[f"AXLE_MOTOR_CARRIER_{s}"]), 4)}
R["button_heads"] = heads

# 7. Drivers sit on their posts.
R["driver_pcb_to_deck_mm"] = {d.label: round(next(l for l in leaves(d) if l.label.endswith("_PCB")).distance_to(deck_front), 4) for d in drivers}

# 8. Pack restraint: straps and foam touch the pack, hatch and tub, without overlap.
straps = [p for p in restraint if "STRAP" in p.label]
R["strap_to_pack_mm"] = {s.label: round(min(s.distance_to(p) for p in pack), 4) for s in straps}
R["strap_to_hatch_mm"] = {s.label: round(s.distance_to(by["BATTERY_TUB_BOTTOM_HATCH"]), 4) for s in straps}
R["foam_to_pack_mm"] = {f.label: round(min(f.distance_to(p) for p in pack), 4) for f in restraint if "FOAM" in f.label}
bms = next(p for p in pack if "BMS" in p.label)
R["strap_to_bms_mm"] = round(min(s.distance_to(bms) for s in straps), 4)

# 9. Service: with the four J11A screws out, hatch + straps + pack drop 60 mm clear.
# Each moving part's bounding box, extruded 60 mm down, is a conservative sweep.
moving = [by["BATTERY_TUB_BOTTOM_HATCH"], *straps, *pack]
static = [o for o in others if o not in moving and not o.label.startswith(("J11A_HATCH_SCREW", "PACK_FOAM"))]
blockers = {}
for part in moving:
    b = part.bounding_box()
    sweep = M._block(b.min.X, b.max.X, b.min.Y, b.max.Y, b.min.Z - 60.0, b.max.Z - 0.01)
    for o in static:
        if meet(sweep, o):
            v = _vol(sweep & o)
            if v > 1e-3:
                blockers[f"{part.label} x {o.label}"] = round(v, 3)
R["pack_cartridge_drop_blockers_mm3"] = blockers
with open("generated/frame-fastener-checks.partial.json", "w") as f:
    json.dump(R, f, indent=2)

rows = [
    ("no_new_clashes", not R["clashes"], R["clashes"]),
    ("thread_engagement_min", all(v >= (3.5 if k.startswith("J15B") else 4.0) for k, v in eng.items()),
     {**eng, "rule": "M3 >= 4.0 mm in the insert; M2.5 >= 3.5 mm"}),
    ("inserts_pressable_from_free_face", all(v < 1e-3 for v in press.values()), press),
    ("tongue_fit", R["tongue_side_clearance_mm"] >= 0.2 and R["tongue_insert_wall_mm"] >= 1.8,
     {"side_clearance_mm": R["tongue_side_clearance_mm"], "insert_wall_mm": R["tongue_insert_wall_mm"]}),
    ("set_screw_swept_clear", all(v["min_swept_gap_mm"] >= 1.5 and v["on_shaft_flat_mm"] < 1e-6 for v in set_screw.values()), set_screw),
    ("button_heads_seated", all(v["to_carrier_mm"] < 1e-6 and v.get("to_inner_bearing_mm", 1.0) >= 0.4 for v in heads.values()), heads),
    ("drivers_on_posts", all(v < 1e-6 for v in R["driver_pcb_to_deck_mm"].values()), R["driver_pcb_to_deck_mm"]),
    ("pack_restrained", all(v < 1e-6 for v in [*R["strap_to_pack_mm"].values(), *R["strap_to_hatch_mm"].values(), *R["foam_to_pack_mm"].values()]) and R["strap_to_bms_mm"] >= 0.0,
     {k: R[k] for k in ("strap_to_pack_mm", "strap_to_hatch_mm", "foam_to_pack_mm", "strap_to_bms_mm")}),
    ("pack_cartridge_drops_out", not blockers, blockers),
]
out = [{"check": n, "pass": bool(ok), "value": v} for n, ok, v in rows]
os.makedirs("generated", exist_ok=True)
with open("generated/frame-fastener-checks.json", "w") as f:
    json.dump({"rows": out, "accepted_overlaps": R["accepted_overlaps"]}, f, indent=2)
for r in out:
    print(("PASS " if r["pass"] else "FAIL ") + r["check"])
    if not r["pass"]:
        print("   ", json.dumps(r["value"])[:1500])
print("accepted:", R["accepted_overlaps"])
