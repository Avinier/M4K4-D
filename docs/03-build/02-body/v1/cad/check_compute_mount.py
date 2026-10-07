"""Check the compute tray, the Pi 5 and Active Cooler retention, and the tray install path (D-042).

Measures, against the body v1 model:
- the tray is one print and the Pi PCB sits on the four boss tops;
- the bosses clear the Pi's underside parts by 0.3 mm, and nothing on the tray enters the
  cooler push-pin tip keep-outs;
- the M2.5 screw heads clear the Pi's top parts and the cooler by 0.3 mm; thread engagement;
- the tray sits on its three supports (rear -Y lug, front -Y column, rear +Y block), and
  the inserts sit inside them;
- no clash between the tray, its hardware, the Pi and cooler and any fixed body or
  chassis part (harness route reserves are reported, not failed);
- the Pi USB-C power-plug reserve clears the purchased C3 DevKitC after installation;
- a straight driver reaches each tray screw from above;
- the tray, Pi and cooler slide in from the front 2 mm high (C3 carrier, PCB-09 and
  the plugged harness go in afterwards), then drop onto the lugs; the vendor Pi and
  cooler leaves sweep as their bounding boxes.
"""

import json
from pathlib import Path

from build123d import Location

import body_v1_model as body

HERE = Path(__file__).resolve().parent
TOL = 1e-3
LATER = ("C3_", "BODY_FRAME_C3_", "C0_LINK", "C0_GPIO", "HARNESS_", "PCB09", "SPEAKER_")  # fitted after the tray (the speaker with the front panel)


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


_BOXES = {}


def box(shape):
    """Cached bounding box: the optimal box of the vendor STEP surfaces is slow to recompute."""
    key = id(shape)
    if key not in _BOXES:
        _BOXES[key] = (shape, shape.bounding_box())
    return _BOXES[key][1]


def overlap(a, b):
    aa, bb = box(a), box(b)
    if (aa.max.X <= bb.min.X or bb.max.X <= aa.min.X or
        aa.max.Y <= bb.min.Y or bb.max.Y <= aa.min.Y or
        aa.max.Z <= bb.min.Z or bb.max.Z <= aa.min.Z):
        return 0.0
    common = a & b
    return 0.0 if common is None else round(common.volume, 3)


def clashes(movers, parts):
    found = {}
    for m in movers:
        for p in parts:
            v = overlap(m, p)
            if v > TOL:
                found[f"{m.label}:{p.label}"] = v
    return found


def label(p):
    return p.label or ""


electronics = body.electronics()
tray_group = next(c for c in electronics.children if c.label == "COMPUTE_TRAY_AND_PI_FIXINGS")
tray_leaves = leaves(tray_group)
tray = next(p for p in tray_leaves if label(p) == "COMPUTE_TRAY")
keep_outs = [p for p in tray_leaves if "KEEP_OUT" in label(p)]
hardware = [p for p in tray_leaves if p is not tray and p not in keep_outs]
pi_screws = [p for p in hardware if label(p).startswith("PI5_M25X6_SCREW_")]
pi_inserts = [p for p in hardware if label(p).startswith("PI5_M25_INSERT_")]
tray_screws = [p for p in hardware if label(p).startswith("TRAY_M3X8_SCREW_")]
lug_inserts = [p for p in hardware if label(p).startswith("TRAY_LUG_M3_INSERT_")]
pi = leaves(body.raspberry_pi5())
for k, p in enumerate(pi):
    p.label = f"PI5_STEP_LEAF_{k}"
pcb = max(pi, key=lambda p: p.bounding_box().size.X * p.bounding_box().size.Y if p.bounding_box().size.Z < 2.0 else 0.0)
pi_parts = [p for p in pi if p is not pcb]
cooler = leaves(next(c for c in electronics.children if c.label == "PI5_ACTIVE_COOLER_STEP"))
for k, p in enumerate(cooler):
    p.label = f"PI5_ACTIVE_COOLER_LEAF_{k}"
frame = leaves(body.body_primary_frame())
frame_main = next(p for p in frame if label(p) == "BODY_FRAME_MAIN_PRINT")

# The electronics group carries its own Pi 5 and cooler; exclude them by group (the
# vendor leaves are unlabelled), or the unit is tested against its own duplicate.
own_compute = {id(leaf) for c in electronics.children
               if c.label in ("C0_RASPBERRY_PI5_EXACT_STEP", "PI5_ACTIVE_COOLER_STEP", "COMPUTE_TRAY_AND_PI_FIXINGS")
               for leaf in leaves(c)}
fixed = [
    *frame,
    *leaves(body.chassis_v1_reference()),
    *(p for p in leaves(electronics) if id(p) not in own_compute),
    *leaves(body.body_audio()),
    *leaves(body.body_yaw_stage()),
    *leaves(body.connectors_and_exits()),
]
harness = leaves(body.harness_routes())
unit = [tray, *pi_screws, *pi_inserts, *pi, *cooler]

results = {}
results["tray_solids"] = len(tray.solids())
results["tray_volume_cm3"] = round(tray.volume / 1000.0, 2)
results["pcb_bottom_z_mm"] = round(pcb.bounding_box().min.Z, 3)
results["pcb_to_boss_gap_mm"] = round(pcb.distance(tray), 3)
# Clearances as clash tests on grown solids: B-rep distance to the vendor STEP surfaces can stall.
GROW = 0.3
underside = [p for p in pi_parts if p.bounding_box().max.Z <= body.PI_PCB_TOP_Z + 0.5]
grown_bosses = []
for k, (x, y) in enumerate(body.PI_MOUNT_HOLES, start=1):
    g = body._z_cylinder(body.PI_BOSS_RADIUS + GROW, body.COMPUTE_TRAY_BOX[5], body.PI_PCB_BOTTOM_Z - 0.01, x, y)
    g.label = f"PI_BOSS_{k}_GROWN_{GROW}"
    grown_bosses.append(g)
results["bosses_grown_0.3_vs_pi_underside_mm3"] = clashes(grown_bosses, underside)
results["tray_and_hardware_vs_pin_keep_out_mm3"] = clashes([tray, *hardware], keep_outs)
results["pin_keep_out_to_tray_mm"] = round(min(k.distance(tray) for k in keep_outs), 2)
results["pi_screw_heads_vs_pi_and_cooler_mm3"] = clashes(pi_screws, [*pi_parts, *cooler])
grown_heads = []
for k, (x, y) in enumerate(body.PI_MOUNT_HOLES, start=1):
    g = body._z_cylinder(body.PI_SCREW[1] + GROW, body.PI_PCB_TOP_Z + 0.01, body.PI_PCB_TOP_Z + body.PI_SCREW[2] + GROW, x, y)
    g.label = f"PI_SCREW_HEAD_{k}_GROWN_{GROW}"
    grown_heads.append(g)
results["pi_screw_heads_grown_0.3_vs_pi_and_cooler_mm3"] = clashes(grown_heads, [*pi_parts, *cooler])
radius, insert_length = body.PI_INSERT
screw_length = body.PI_SCREW[0]
results["pi_screw_thread_below_pcb_mm"] = round(screw_length - (body.PI_PCB_TOP_Z - body.PI_PCB_BOTTOM_Z), 2)
results["pi_insert_pilot_depth_mm"] = body.PI_INSERT_PILOT_DEPTH
results["tray_screw_thread_in_lug_mm"] = round(body.TRAY_SCREW[0] - (body.COMPUTE_TRAY_BOX[5] - body.COMPUTE_TRAY_BOX[4]), 2)
results["ears_on_lugs_gap_mm"] = round(tray.distance(frame_main), 3)
results["lug_inserts_vs_frame_mm3"] = clashes(lug_inserts, [frame_main])  # inserts sit in their pilots
cx0, cx1, cy0, cy1 = body.TRAY_FRONT_COLUMN[:4]
fx, fy = body.TRAY_FRONT_MOUNT
bx0, bx1, by0, by1 = body.TRAY_REAR_PY_BLOCK[:4]
rx, ry = body.TRAY_REAR_PY_MOUNT
results["lug_wall_round_insert_mm"] = round(min(
    body.TRAY_EAR_HALF_X - body.FRAME_INSERT_RADIUS,
    min(abs(abs(y) - body.TRAY_LUG_Y[0]) for _, y in body.TRAY_EAR_MOUNTS) - body.FRAME_INSERT_RADIUS,
    min(fx - cx0, cx1 - fx, fy - cy0, cy1 - fy) - body.FRAME_INSERT_RADIUS,
    min(rx - bx0, bx1 - rx, ry - by0, by1 - ry) - body.FRAME_INSERT_RADIUS,
), 2)
results["tray_screw_heads_vs_tray_rib_mm3"] = clashes(tray_screws, [tray])
results["unit_vs_fixed_mm3"] = clashes([*unit, *hardware], fixed)
results["unit_vs_harness_reserves_mm3_info"] = clashes([tray], harness)
# The Pi power plug is placed after the tray and is excluded from its install
# sweep. It still needs a clash-free final position beside the C3 DevKitC.
c3_group = next(c for c in electronics.children if label(c) == "C3_CARRIER_PCB10_WITH_DEVKITC")
c3_devkit = next(c for c in c3_group.children if label(c) == "C3_ESP32_S3_DEVKITC_STEP")
pi_power_plug = body._block(*body.PI_POWER_PLUG_RESERVE)
pi_power_plug.label = "PI5_POWER_USBC_RIGHT_ANGLE_PLUG_RESERVE"
results["pi_power_plug_vs_c3_devkitc_mm3"] = overlap(pi_power_plug, c3_devkit)
results["pi_and_cooler_to_tray_hardware_mm3"] = clashes([*pi_parts, *cooler], [tray_screw for tray_screw in tray_screws])

# Driver to each tray screw: a Ø6 tool from the head up to Z 126.
access = {}
for s in tray_screws:
    bb = s.bounding_box()
    cx, cy = (bb.min.X + bb.max.X) / 2.0, (bb.min.Y + bb.max.Y) / 2.0
    tool = body._z_cylinder(3.0, bb.max.Z + 0.5, 126.0, cx, cy)
    tool.label = f"DRIVER_{label(s)}"
    # Lead routes and plugs (RESERVE/PLUG) are fitted after the tray.
    hit = clashes([tool], [p for p in fixed if not any(t in label(p) for t in ("KEEP_OUT", "RESERVE", "PLUG"))])
    if hit:
        access[label(s)] = hit
results["tray_screw_driver_clashes"] = access

# Install path: lifted 2 mm, slid in along -X from 90 mm out.
sweep_fixed = [p for p in fixed if not label(p).startswith(LATER) and "RESERVE" not in label(p)
               and "KEEP_OUT" not in label(p) and "PLUG" not in label(p)]
# Crop the fixed parts to the corridor the unit passes through; whole-frame booleans are slow.
corridor = body._block(-45.0, 175.0, -62.0, 62.0, 84.0, 116.0)
cropped = []
for p in sweep_fixed:
    if overlap(p, corridor) > TOL:
        c = p & corridor
        c.label = label(p)
        cropped.append(c)
sweep_fixed = cropped
fixed_boxes = [(p, box(p)) for p in sweep_fixed]
# The vendor Pi and cooler leaves sweep as their bounding boxes (conservative): booleans on
# their moved B-spline and self-intersecting solids stall and run out of memory.
envelopes = []
for p in [*pi, *cooler]:
    bb = box(p)
    e = body._block(bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z)
    e.label = f"{label(p)}_BOX"
    envelopes.append(e)
sweep_movers = [tray, *pi_screws, *pi_inserts, *envelopes]
sweep = {}
lift = body.TRAY_INSTALL_LIFT
for step in range(0, 19):
    dx = 5.0 * step
    hit = {}
    for p in sweep_movers:
        a = box(p)  # move the cached box, and the shape only where the boxes meet
        ax0, ax1, az0, az1 = a.min.X + dx, a.max.X + dx, a.min.Z + lift, a.max.Z + lift
        moved = None
        for f, b in fixed_boxes:
            if (ax1 <= b.min.X or b.max.X <= ax0 or a.max.Y <= b.min.Y or b.max.Y <= a.min.Y
                    or az1 <= b.min.Z or b.max.Z <= az0):
                continue
            if moved is None:
                moved = p.moved(Location((dx, 0.0, lift)))
            common = moved & f
            v = 0.0 if common is None else round(common.volume, 3)
            if v > TOL:
                hit[f"{label(p)}:{label(f)}"] = v
    if hit:
        sweep[f"+{dx:.0f}"] = hit
results["install_sweep_clashes"] = sweep
results["install_sweep_excludes"] = list(LATER) + ["*RESERVE*", "*KEEP_OUT*", "*PLUG*"]

out = HERE / "generated" / "compute-mount-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))

assert results["tray_solids"] == 1, "tray must be one print"
assert results["pcb_to_boss_gap_mm"] <= 0.01, "Pi PCB must land on the bosses"
assert not results["bosses_grown_0.3_vs_pi_underside_mm3"], "bosses need 0.3 mm round the Pi's underside parts"
assert not results["pi_screw_heads_grown_0.3_vs_pi_and_cooler_mm3"], "screw heads need 0.3 mm round the Pi's top parts"
assert not results["tray_and_hardware_vs_pin_keep_out_mm3"], "push-pin tips need their clearance"
assert not results["pi_screw_heads_vs_pi_and_cooler_mm3"]
assert results["pi_screw_thread_below_pcb_mm"] >= 3.0
assert results["tray_screw_thread_in_lug_mm"] >= 4.0
assert results["ears_on_lugs_gap_mm"] <= 0.01, "ears must sit on the lugs"
assert results["lug_wall_round_insert_mm"] >= 1.2
for key in ("lug_inserts_vs_frame_mm3", "tray_screw_heads_vs_tray_rib_mm3", "unit_vs_fixed_mm3", "pi_and_cooler_to_tray_hardware_mm3", "tray_screw_driver_clashes", "install_sweep_clashes"):
    assert not results[key], f"{key} not clear"
assert results["pi_power_plug_vs_c3_devkitc_mm3"] <= TOL, "Pi power-plug envelope intersects C3 DevKitC; select and model a fitting plug"
print("ALL PASS")
