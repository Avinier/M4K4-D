"""Check the body cooling path (D-042): enclosure fan, side intake grille, rear exhaust slots.

Measures, against the body v1 model:
- the fan and its screws clear every fixed body and chassis part, and the shell;
- the shell lowers past the fan, its screws, the W41 lead and the fan web;
- the side grille is open between the fan face and the outside, clear of the
  wheel-arch pod, its 90 deg screw boss and the FRONT_L mic boss;
- the rear slots pass through the panel inside the panel-frame aperture;
- the distance from each grille to each mic port (RP-05 AR-61);
- grille free areas, and a first-order estimate of the internal air rise.

The thermal numbers are an estimate (E) for comparing options, not a measurement.
"""

import json
import math
from pathlib import Path

from build123d import Location, Vertex

import body_v1_model as body

HERE = Path(__file__).resolve().parent
TOL = 1e-3

# Thermal estimate inputs (E).
LOADS_W = {"light: Pi 4 W + converters 2.5 W": 6.5, "typical: Pi 6 W + 2.5 W": 8.5, "heavy: Pi 8 W + 3 W": 11.0}
UA_WALLS_W_K = 0.44  # 0.135 m2 skin, ~3.3 W/m2K natural convection + radiation both sides
RHO, CP = 1.15, 1007.0  # air at about 35 C
ROOM_K = 308.0
CD = 0.6
FLOOR_INLET_MM2 = 10000.0  # measured 2026-10-04: >= 11,600 mm2 free in horizontal sections Z 31-90; rounded down
STACK_HEIGHT_M = 0.071  # floor (Z ~35) to the outlet centroid (Z ~106)
# BO-040 is a 2-wire DC 5 V 3010 hydraulic fan (D-043) with no published curve. These
# are typical listing-class figures for such fans (E, unmeasured): replace them with the
# bench measurement. The fan is switched on/off (gpio-fan), so it runs at full speed or not
# at all; the 50 % row is a sensitivity case for a weaker fan than the listing class.
FAN_Q_MAX_M3_S = 5.1 / 3600.0  # about 3.0 CFM free air
FAN_P_MAX_PA = 3.0 * 9.81  # about 3 mm H2O shut-off
FAN_FLOW_FACTORS = {"fan_on_half_listing_flow": 0.5, "fan_on_listing_flow": 1.0}


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
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


shell = body.body_shell()
panels = body.body_panels()
rear = panels.children[1]
pods = [p for p in leaves(panels) if label(p).startswith("WHEEL_ARCH_POD_")]
panel_hw = body.panel_mount_hardware().children
rear_frame = next(p for p in panel_hw if label(p) == "REAR_PANEL_INTERNAL_FRAME_WITH_BOSSES")
electronics = leaves(body.electronics())
fan = [p for p in electronics if label(p).startswith("ENCLOSURE_FAN_")]
fan_body = [p for p in fan if "SCREW" not in label(p)]
harness = leaves(body.harness_routes())
w41 = [p for p in harness if label(p).startswith("HARNESS_W41_")]
frame = leaves(body.body_primary_frame())
frame_main = next(p for p in frame if label(p) == "BODY_FRAME_MAIN_PRINT")
fixed = [
    *frame,
    *leaves(body.chassis_v1_reference()),
    *(p for p in electronics if p not in fan),
    *leaves(body.body_audio()),
    *leaves(body.body_yaw_stage()),
    *leaves(body.connectors_and_exits()),
    *(p for p in harness if p not in w41),
    *leaves(body.wheel_arch_hardware()),
    *leaves(body.shell_frame_hardware()),
    *panel_hw,
    *leaves(panels),
]
fixed = [p for p in fixed if not label(p).startswith(("ESTOP_XA1E_",))]

results = {}
cx, cz = body.ENCLOSURE_FAN_CENTER
grille = body._fan_grille_cuts()
grille.label = "FAN_GRILLE_SLOTS"
grille_area = grille.volume / 35.0  # prisms along Y, 35 mm long
rear_slots = body.rear_vent_slots()
rear_area = sum(s.volume for s in rear_slots) / 30.0
for k, s in enumerate(rear_slots):
    s.label = f"REAR_VENT_SLOT_{k}"
results["side_grille_free_area_mm2"] = round(grille_area, 1)
results["rear_slots_free_area_mm2"] = round(rear_area, 1)
results["fan_vs_fixed_mm3"] = clashes(fan, fixed)
results["fan_vs_shell_mm3"] = clashes(fan, [shell])
results["fan_face_to_collar_mm"] = round(min(f.distance(shell) for f in fan_body), 2)
results["fan_seated_on_web_gap_mm"] = round(fan_body[0].distance(frame_main), 3)
# W41 ends in its own plug at J9-4, inside PCB-09's reserves.
results["w41_vs_fixed_mm3"] = clashes(w41, [p for p in fixed if not label(p).startswith(("C0_RASPBERRY", "C0_LINK_ADAPTER_J94"))])

# Air path between the fan face and the outer skin, inside the grille radius.
y_fan = body.ENCLOSURE_FAN_Y[1]
path = body._axial_bore_y(body.FAN_GRILLE_RADIUS, y_fan + 0.05, 95.0, cx, cz) & body._shell_outer()
path.label = "FAN_INTAKE_AIR_PATH"
results["intake_path_vs_parts_mm3"] = clashes([path], [p for p in fixed if p not in pods])
results["intake_path_skin_blocked_fraction"] = round(overlap(path, shell) / path.volume, 3)
results["grille_vs_pods_mm3"] = clashes([grille], pods)
pod_boss = body._axial_bore_y(body.WHEEL_ARCH_BOSS_RADIUS, 60.0, 95.0, 0.0, body.AXLE_Z + body.WHEEL_ARCH_FASTENER_RADIUS)
pod_boss.label = "WHEEL_ARCH_90DEG_BOSS"
port = next(p for p in body.MICROPHONE_PORTS if p[3] == "FRONT_L")
mic_boss = body._mic_boss(port[0], port[2], 1.0) & body._shell_outer()
mic_boss.label = "FRONT_L_MIC_BOSS"
collar = body._fan_collar() & body._shell_outer()
collar.label = "FAN_COLLAR"
results["grille_and_collar_vs_bosses_mm3"] = clashes([grille, collar], [pod_boss, mic_boss])
results["collar_to_bosses_mm"] = {b.label: round(collar.distance(b), 2) for b in (pod_boss, mic_boss)}

# Rear slots must pass the panel frame and the shell (inside the aperture).
rear_band = body._sloped_panel_band("REAR", -body.SHELL_THICKNESS, 0.0)
openings = [s & rear_band for s in rear_slots]
through = []
for s in rear_slots:
    t = s.moved(Location((0.0, 0.0, 0.0)))
    t.label = s.label
    through.append(t)
results["rear_slots_vs_panel_frame_and_shell_mm3"] = clashes(through, [rear_frame, shell])
results["rear_slots_cut_panel_mm3"] = round(sum(overlap(s, rear_band) for s in rear_slots), 1)

# Distances to the mic ports (outer skin points), to the openings in the skin and panel.
dist = {}
for x, y, z, name in body.MICROPHONE_PORTS:
    v = Vertex(x, y, z)
    dist[name] = {"side_grille_edge_mm": round(v.distance(grille), 1),
                  "side_grille_centre_mm": round(math.dist((x, y, z), (cx, 76.0, cz)), 1),
                  "rear_slot_openings_mm": round(min(v.distance(o) for o in openings), 1)}
results["mic_port_distances"] = dist

# Shell lowering past the fan, its screws, the W41 lead and the fan web.
region = body._block(-2.0, 50.0, 50.0, 96.0, 28.0, 142.0)
shell_local = shell & region
shell_local.label = "BODY_SHELL_LOCAL"
web_local = frame_main & body._block(*body.FAN_WEB_X, 50.0, 70.0, 60.0, 134.0)
web_local.label = "FRAME_FAN_WEB_LOCAL"
movers_fixed = [*fan, *w41, web_local]
# The +Y mic boards, their screws and pigtails ride down with the shell.
shell_riders = [p for p in leaves(body.body_audio()) if "_FRONT_L" in label(p) or "_REAR_L" in label(p)]
sweep = {}
for step in range(1, 57):
    dz = 2.0 * step
    moved = shell_local.moved(Location((0.0, 0.0, dz)))
    moved.label = shell_local.label
    riders = []
    for p in shell_riders:
        m = p.moved(Location((0.0, 0.0, dz)))
        m.label = label(p)
        riders.append(m)
    hit = clashes([moved, *riders], movers_fixed)
    if hit:
        sweep[f"+{dz:.0f}"] = hit
results["shell_lowering_sweep_clashes"] = sweep


# First-order thermal estimate (E).
def fan_flow(duty, area_in_m2, area_web_m2):
    """Operating point of a fan with a linear curve against two orifices in series."""
    q_max, p_max = FAN_Q_MAX_M3_S * duty, FAN_P_MAX_PA * duty**2
    k = 0.5 * RHO * (1.0 / (CD * area_in_m2) ** 2 + 1.0 / (CD * area_web_m2) ** 2
                     + 1.0 / (CD * FLOOR_INLET_MM2 * 1e-6) ** 2)
    lo, hi = 0.0, q_max
    for _ in range(60):
        q = (lo + hi) / 2.0
        if q_max * (1.0 - k * q * q / p_max) > q:
            lo = q
        else:
            hi = q
    return q


leak = 2.0 * math.pi * body.FAN_COLLAR[0] * (body.FAN_COLLAR[2] - body.ENCLOSURE_FAN_Y[1])
fresh = grille_area / (grille_area + leak)
web_area = math.pi * body.FAN_WEB_OPENING_RADIUS**2
thermal = {"assumptions": {
    "wall_conductance_W_K": UA_WALLS_W_K, "floor_inlet_mm2": FLOOR_INLET_MM2, "orifice_cd": CD,
    "collar_leak_mm2": round(leak, 1), "fresh_air_fraction": round(fresh, 3),
    "fan_curve": "BO-040 hydraulic 3010 5 V, E listing class: linear between 5.1 m3/h free and 3.0 mm H2O shut-off; the half-flow case scales flow by 0.5 and pressure by 0.25",
    "room_K": ROOM_K, "status": "E: estimate for comparing options; measure on the bench",
}}
flows = {}
for name, factor in FAN_FLOW_FACTORS.items():
    flows[name] = fan_flow(factor, (grille_area + leak) * 1e-6, web_area * 1e-6)
thermal["fan_flow_l_s"] = {k: round(v * 1000.0, 3) for k, v in flows.items()}
rise = {}
for name, watts in LOADS_W.items():
    row = {}
    for case, q in flows.items():
        row[case] = round(watts / (UA_WALLS_W_K + RHO * CP * q * fresh), 1)
    # Fan stopped: stack flow through the floor and the rear slots plus half the side grille.
    a_out = (rear_area + 0.5 * grille_area) * 1e-6
    a_eff = 1.0 / math.sqrt(1.0 / a_out**2 + 1.0 / (FLOOR_INLET_MM2 * 1e-6) ** 2)
    lo, hi = 0.0, 60.0
    for _ in range(60):
        dt = (lo + hi) / 2.0
        q_stack = CD * a_eff * math.sqrt(2.0 * 9.81 * STACK_HEIGHT_M * dt / ROOM_K)
        if UA_WALLS_W_K * dt + RHO * CP * q_stack * dt < watts:
            lo = dt
        else:
            hi = dt
    row["fan_off_vents"] = round(lo, 1)
    row["sealed_no_vents"] = round(watts / UA_WALLS_W_K, 1)
    rise[name] = row
thermal["internal_air_rise_K"] = rise
results["thermal_estimate"] = thermal

out = HERE / "generated" / "cooling-path.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))

for key in ("fan_vs_fixed_mm3", "fan_vs_shell_mm3", "w41_vs_fixed_mm3", "intake_path_vs_parts_mm3",
            "grille_vs_pods_mm3", "grille_and_collar_vs_bosses_mm3", "rear_slots_vs_panel_frame_and_shell_mm3",
            "shell_lowering_sweep_clashes"):
    assert not results[key], f"{key} not clear"
assert results["fan_face_to_collar_mm"] >= 0.5
assert results["fan_seated_on_web_gap_mm"] <= 0.01
assert results["rear_slots_cut_panel_mm3"] > 0.0
assert min(d["rear_slot_openings_mm"] for d in dist.values()) >= 40.0, "rear slots too close to a mic port"
# The side grille sits midway between the +Y ports, its edge about 24 mm from each (D-043; was 14 mm from FRONT_L).
assert min(d["side_grille_edge_mm"] for d in dist.values()) >= 22.0, "side grille moved closer to a mic port"
print("ALL PASS")
