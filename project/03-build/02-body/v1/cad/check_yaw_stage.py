"""Check the D-044 head yaw stage (BO-043 to BO-050, BO-056 to BO-062).

Geometry, against the body v1 model:
- the cartridge, cassette, servo drive and their fixings clear every fixed body
  and chassis part, and each other;
- the hub, rotor and PCB-14 sweep +-61 deg (the pinion counter-rotating with
  them) without touching anything, and the stop dog meets its bumps at +-62 deg;
- the involute mesh has no interference over a full tooth pitch, and the
  measured clearance matches the designed backlash;
- the bench-built cartridge lowers 40 mm onto the plate, and the pinion then
  drops 12 mm onto its shaft, without clashing;
- the pinion keeps axial clearance to the hub shoulder, clamp ring and disc;
- D-052 cable path: the FFC band passes the drum slit, each FFC's 45 deg fold
  fits the drum core, the PCB-14 joiner boards and ZIFs clear the rotor, hub
  and the head disc's pilot ring, their tabs are captured under the hub
  shoulder, the upper ZIFs lie inside the disc bore (demate with the disc on),
  and the head FFC stack sits in the disc channel below the disc top.

Engineering estimates (`E`, written to generated/yaw-stage.json): bearing static
safety and life, Lewis tooth stress in printed PETG, the preload spring, shaft
and servo side load, stop and uplift paths, drag against the servo margin, the
FFC rolling-loop kinematics, and the stage mass, centroid and yaw inertia for
the BODY_YAW_STAGE mass row.
"""

import json
import math
from pathlib import Path

from build123d import Location

import body_v1_model as body

HERE = Path(__file__).resolve().parent
TOL = 1e-3
G = 9.81


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


_BOXES = {}


def box(shape):
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


def clashes(movers, parts, skip=()):
    found = {}
    for m in movers:
        for p in parts:
            if m is p or (m.label, p.label) in skip or (p.label, m.label) in skip:
                continue
            v = overlap(m, p)
            if v > TOL:
                found[f"{m.label}:{p.label}"] = v
    return found


def label(p):
    return p.label or ""


def moved(parts, dx=0.0, dy=0.0, dz=0.0):
    out = []
    for p in parts:
        m = p.moved(Location((dx, dy, dz)))
        m.label = p.label
        out.append(m)
    return out


# --- Parts ------------------------------------------------------------------
stage = leaves(body.body_yaw_stage())
servo = [p for p in stage if not label(p).startswith(("YAW_", "PCB"))]  # unlabelled ST3215-HS STEP leaves (D-048)
for k, p in enumerate(servo):
    p.label = f"HS_STEP_LEAF_{k}"
pinion_labels = ("YAW_DRIVE_SCISSOR_", "YAW_PINION_SHAFT", "YAW_SCISSOR_PRELOAD", "YAW_DRIVE_HUB")
pinion = [p for p in stage if label(p).startswith(pinion_labels)]
flange_fix = [p for p in stage if label(p).startswith("YAW_FLANGE_")]
servo_fix = [p for p in stage if label(p).startswith("YAW_SERVO_M2X8_MOUNT_SCREW_")]
cartridge = [p for p in stage if p not in (*servo, *pinion, *flange_fix, *servo_fix)]
moving = body.yaw_drive_moving_parts()
by = {label(p): p for p in [*stage, *moving]}
hub = by["YAW_HUB_DRIVEN_GEAR_M1_Z37"]
rotor = by["YAW_ROTOR_CLAMP_DRUM_AND_STOP_DOG"]
housing = by["YAW_CARTRIDGE_HOUSING"]
fixed_half = by["YAW_DRIVE_SCISSOR_PINION_FIXED_HALF"]
sprung_half = by["YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF"]

frame = leaves(body.body_primary_frame())
electronics = leaves(body.electronics())
fixed = [
    *frame,
    *(p for p in leaves(body.chassis_v1_reference()) if not label(p).startswith("ESTOP_XA1E_")),
    *electronics,
    *leaves(body.body_audio()),
    *leaves(body.connectors_and_exits()),
    *leaves(body.harness_routes()),
    body.body_shell(),
]
# The head disc (RP-01 Layout 04, head-owned): the hub's top face carries it.
head = leaves(body.rp01_head_groups()[0])
# Leaves of the moved head group keep head-local placement; move the disc into chassis coordinates.
disc = []
for p in head:
    if "yaw_turntable_disc" in label(p):
        m = p.moved(Location(body.HEAD_ORIGIN_IN_CHASSIS))
        m.label = label(p)
        disc.append(m)
assert disc, "head disc not found"
fixed += disc
# Intended contacts and shared volumes: the disc sits on the hub top, the hub
# inserts are part of the hub bosses' bores, the PCB-14 reserve sits in the hub.
HUB_GROUP = ("YAW_HUB_", "YAW_ROTOR_", "PCB14_")

results = {}

# --- Static fit ---------------------------------------------------------------
results["stage_vs_fixed_mm3"] = clashes([*cartridge, *pinion, *flange_fix, *servo_fix, *servo], fixed)
stationary = [*cartridge, *pinion, *flange_fix, *servo_fix, *servo]
pairs = {}
engagement = {}
for i, a in enumerate(stationary):
    for b in stationary[i + 1:]:
        if a.label.startswith("HS_") and b.label.startswith("HS_"):
            continue
        v = overlap(a, b)
        if v > TOL:
            # Horn screws enter the horn. Case-mount screws must stay inside
            # the STEP's drilled holes: count any case overlap as a clash.
            screw = next((x for x in (a, b) if x.label.startswith("YAW_DRIVE_HUB_HORN_SCREW_")), None)
            other = b if screw is a else a
            if screw is not None and other.label.startswith("HS_"):
                engagement[f"{a.label}:{b.label}"] = v
                continue
            pairs[f"{a.label}:{b.label}"] = v
results["stage_internal_mm3"] = pairs
results["screw_engagement_in_servo_mm3_info"] = engagement
# Independent hole-axis measurement from the selected vendor STEP after its
# -90 deg X turn. The prior D-048 coordinates were 0.8 mm off all four axes;
# a screw/case overlap must never be waived as intentional thread engagement.
step_hole_xy = [(body.BODY_AXIS_X - (sx - body.YAW_SERVO_STEP_AXIS[0]),
                 body.YAW_PINION_CENTER[1] - sy)
                for sx in (-17.2, 7.25) for sy in (-10.25, 10.25)]
assert body.YAW_SERVO_CLOCK_DEG == 180.0, "update the STEP hole-axis transform"
results["mount_screw_axis_offset_mm"] = [round(min(math.dist((x, y), h) for h in step_hole_xy), 3)
                                          for x, y in body.YAW_SERVO_MOUNT_SCREWS]
results["moving_vs_fixed_at_0_mm3"] = clashes(moving, fixed)
results["frame_solids"] = len(next(p for p in frame if label(p) == "BODY_FRAME_MAIN_PRINT").solids())
results["hub_solids"] = len(hub.solids())
results["housing_solids"] = len(housing.solids())
results["rotor_solids"] = len(rotor.solids())

# Axial clearances (mm)
pz0, pz1 = body.YAW_PINION_Z
results["pinion_to_hub_shoulder_mm"] = round(pz0 - body.YAW_HUB_SHOULDER[3], 2)
results["pinion_to_clamp_ring_mm"] = round(pz0 - body.YAW_CLAMP_RING[3], 2)
results["pinion_to_disc_plate_mm"] = round(body.YAW_DISC_PLATE_BOTTOM_Z - pz1, 2)
results["driven_face_covers_pinion"] = body.YAW_GEAR_Z[0] <= pz0 and body.YAW_GEAR_Z[1] >= pz1
results["spring_to_bearing_od_mm"] = round(body.YAW_PINION_CENTER[1] - body.YAW_SPRING[1] / 2.0 - body.YAW_BEARING_RADII[1], 2)
results["cassette_to_cooler_top_mm"] = round(body.YAW_CASSETTE_FLOOR[1] - 107.0, 1)
results["disc_to_hub_contact_mm"] = round(min(d.distance(hub) for d in disc), 3)
results["pinion_to_disc_mm"] = round(min(d.distance(fixed_half) for d in disc), 3)

# --- Yaw sweep (hub, rotor and PCB-14 turn; the pinion counter-rotates) ----------
stationary_for_sweep = [p for p in [*cartridge, *flange_fix, *servo_fix, *servo] if not label(p).startswith(HUB_GROUP)]
sweep = {}
angles = [a for a in range(-61, 62, 4)] + [-61, 61]
for deg in sorted(set(angles)):
    mv = body.yaw_drive_moving_parts(deg)
    pin = [p for p in body.yaw_pinion_parts(deg)]
    hit = clashes(mv, [*stationary_for_sweep, *fixed])
    # The gear pair is checked as a mesh below; everything else on the pinion is checked here.
    hit.update(clashes(mv, pin, skip={("YAW_HUB_DRIVEN_GEAR_M1_Z37", "YAW_DRIVE_SCISSOR_PINION_FIXED_HALF"),
                                       ("YAW_HUB_DRIVEN_GEAR_M1_Z37", "YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF")}))
    if hit:
        sweep[str(deg)] = hit
results["yaw_sweep_clashes_mm3"] = sweep

# Hard stops: clear at +-61.5, dog on bump at +-62.5.
stop = {}
for deg in (61.5, -61.5, 62.5, -62.5):
    r = body._yaw_rotated(rotor, deg)
    r.label = rotor.label
    stop[str(deg)] = overlap(r, housing)
results["stop_dog_vs_housing_mm3"] = stop
results["stop_bump_centres_deg"] = [round(a, 2) for a in body._yaw_stop_bump_angles()]

# --- Gear mesh ------------------------------------------------------------------
pitch_deg = 360.0 / body.YAW_GEAR_TEETH
mesh = []
for k in range(0, 21):
    deg = pitch_deg * k / 20.0
    h = body._yaw_rotated(hub, deg)
    pin = {label(p): p for p in body.yaw_pinion_parts(deg)}
    for half_name in ("YAW_DRIVE_SCISSOR_PINION_FIXED_HALF", "YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF"):
        half = pin[half_name]
        common = h & half
        vol = 0.0 if common is None else common.volume
        mesh.append({"deg": round(deg, 3), "half": half_name[-10:], "overlap_mm3": round(vol, 4),
                     "gap_mm": round(h.distance(half), 4)})
results["mesh_min_gap_mm"] = min(m["gap_mm"] for m in mesh)
results["mesh_max_gap_mm"] = max(m["gap_mm"] for m in mesh)
results["mesh_max_overlap_mm3"] = max(m["overlap_mm3"] for m in mesh)

# --- Installation paths -----------------------------------------------------------
# The head disc goes on last (assembly step 5), so it is not in the way of steps 3 and 4.
before_disc = [p for p in fixed if p not in disc]
# 1. The bench-built cartridge (with the hub and rotor at yaw 0) lowers from 40 mm.
lower_set = [*cartridge, *moving]
lower = {}
for dz in range(40, 0, -2):
    hit = clashes(moved(lower_set, dz=float(dz)), [*before_disc, *servo, *servo_fix])
    if hit:
        lower[str(dz)] = hit
results["cartridge_lowering_clashes"] = lower
# 2. The pinion halves and spring drop onto the shaft (drive hub, shaft already fitted).
drop_set = [p for p in pinion if label(p).startswith(("YAW_DRIVE_SCISSOR_", "YAW_SCISSOR_PRELOAD"))]
drop = {}
for dz in range(12, 0, -1):
    hit = clashes(moved(drop_set, dz=float(dz)), [*cartridge, *flange_fix, *before_disc],
                  skip=set())
    if hit:
        drop[str(dz)] = hit
results["pinion_drop_clashes"] = drop

# --- Engineering estimates (E) ---------------------------------------------------
head_m = body.HEAD_MASS_G / 1000.0
head_com_z = body.HEAD_ORIGIN_IN_CHASSIS[2] + body.HEAD_LOCAL_COM[2]
bearing_mid = sum(body.YAW_BEARING_Z) / 2.0
arm = (head_com_z - bearing_mid) / 1000.0
robot_m = body.mass_properties()["mass_g"] / 1000.0
dm = (body.YAW_BEARING_RADII[0] + body.YAW_BEARING_RADII[1]) / 1000.0  # pitch diameter, m
C, C0, Z_BALLS = 6760.0, 6800.0, 20  # SKF 61810 class ratings, N (D); ball count E
cases = {
    "static_head_weight": (head_m * G, 0.0),
    "braking_2ms2": (head_m * G, head_m * 2.0 * arm),
    "bump_3g_lateral": (head_m * G * 3.0, head_m * G * 3.0 * arm),
    "lift_robot_by_head_x3": (-robot_m * G * 3.0, robot_m * G * 3.0 * 0.03),
    "fall_on_head_100N_at_100mm": (100.0, 100.0 * 0.100),
}
bearing = {}
for name, (fa, m) in cases.items():
    # Equivalent static load for a deep-groove bearing under moment: the moment
    # loads balls on one side as 2M/dm, the axial load shares across all of them.
    p0 = abs(fa) * 0.5 + 2.0 * m / dm
    bearing[name] = {"axial_N": round(fa, 1), "moment_Nm": round(m, 3), "P0_N": round(p0, 1), "s0": round(C0 / max(p0, 1e-6), 1)}
# Life: the busy-minute duty (fullproofmath) averages under 20 rpm; at 1 N equivalent
# dynamic load (head weight plus RMS motion) L10 is effectively unlimited.
p_dyn = head_m * G + 2.0 * head_m * 2.0 * arm / dm
l10_h = (C / p_dyn) ** 3 * 1e6 / (60.0 * 20.0)
results["bearing_61810_2Z"] = {"C_N": C, "C0_N": C0, "head_com_above_bearing_mm": round(arm * 1000.0, 1),
                               "cases": bearing, "L10_hours_at_20rpm": f"{l10_h:.2e}",
                               "tilt_play_deg_E": 0.11,
                               "note": "single deep-groove bearing: radial clearance gives ~0.1 deg tilt play (~0.2 mm at the crown) once moment exceeds head weight x dm/2 ~0.17 N.m; measure"}

# Lewis bending, printed PETG teeth (form factor Y for z37, 20 deg full depth).
Y_LEWIS = 0.383
rp = body.YAW_GEAR_PITCH_RADIUS / 1000.0
pre = body.YAW_SCISSOR_PRELOAD_NM
peak = body.YAW_PEAK_EXTERNAL_TORQUE_NM
limit = body.YAW_SERVO_CURRENT_LIMIT_TORQUE_NM
b_half = body.YAW_SCISSOR_HALF_FACE
lewis = {}
for name, torque in {"preload_only": pre, "preload_plus_peak": pre + peak, "preload_plus_current_limit": pre + limit}.items():
    ft = torque / rp
    lewis[name] = {"Ft_N": round(ft, 1), "pinion_half_MPa": round(ft / (b_half * body.YAW_GEAR_MODULE * Y_LEWIS), 1)}
rb = rp * math.cos(math.radians(body.YAW_GEAR_PRESSURE_ANGLE))
ra = rp + body.YAW_GEAR_MODULE / 1000.0
a = 2.0 * rp
contact_ratio = (2.0 * math.sqrt(ra ** 2 - rb ** 2) - a * math.sin(math.radians(body.YAW_GEAR_PRESSURE_ANGLE))) / (
    math.pi * body.YAW_GEAR_MODULE / 1000.0 * math.cos(math.radians(body.YAW_GEAR_PRESSURE_ANGLE)))
results["gears"] = {"module": body.YAW_GEAR_MODULE, "teeth": body.YAW_GEAR_TEETH, "centre_mm": round(2000 * rp, 2),
                    "contact_ratio": round(contact_ratio, 2), "backlash_nominal_mm": body.YAW_GEAR_BACKLASH,
                    "backlash_deg_without_scissor": round(math.degrees(body.YAW_GEAR_BACKLASH / (rp * 1000.0)), 2),
                    "lewis_PETG": lewis, "petg_flag_MPa": 15.0,
                    "note": "PETG FDM: ~14 MPa sustained at preload creeps; the spring follows it (self-compensating). Swap to metal pinion halves if B4 lash or tooth wear fails."}

# Torsion spring (music wire), the scissor preload.
wire, od, coils, sz0, sz1 = body.YAW_SPRING
d, D = wire / 1000.0, (od - wire) / 1000.0
E_STEEL = 207e9
k_rad = E_STEEL * d ** 4 / (64.0 * D * coils)
wind = pre / k_rad
c_idx = D / d
ki = (4 * c_idx ** 2 - c_idx - 1) / (4 * c_idx * (c_idx - 1))
sigma = ki * 32.0 * pre / (math.pi * d ** 3)
results["preload_spring"] = {"wire_mm": wire, "od_mm": od, "coils": coils, "rate_Nm_per_rad": round(k_rad, 3),
                             "windup_deg": round(math.degrees(wind), 1),
                             "windup_teeth": round(math.degrees(wind) / pitch_deg, 2),
                             "bending_stress_MPa": round(sigma / 1e6), "music_wire_allow_MPa_E": 1600,
                             "preload_loss_per_0.1mm_wear_Nm": round(k_rad * 0.1 / (rp * 1000.0), 4),
                             "body_length_mm": round((coils + 1) * wire, 1), "envelope_mm": round(sz1 - sz0, 1)}

# Shaft and servo side load: preload separating force plus the transmitted load.
alpha = math.radians(body.YAW_GEAR_PRESSURE_ANGLE)
f_sep = 2.0 * pre / rp * math.tan(alpha)
f_peak = math.hypot(peak / rp, f_sep + peak / rp * math.tan(alpha))
lever = (sum(body.YAW_PINION_Z) / 2.0 - body.YAW_DRIVE_HUB[1]) / 1000.0
m_servo = f_peak * lever
sigma_shaft = 32.0 * m_servo / (math.pi * (2.0 * body.YAW_SHAFT[0] / 1000.0) ** 3)
results["shaft_and_servo"] = {"radial_at_rest_N": round(f_sep, 1), "radial_at_peak_N": round(f_peak, 1),
                              "lever_mm": round(lever * 1000.0, 1), "moment_on_servo_output_Nm": round(m_servo, 3),
                              "shaft_bending_MPa": round(sigma_shaft / 1e6, 1),
                              "note": "ST3215-HS radial load is unpublished; D-048 lowered the servo 8 mm, so the lever grew. Bench B1/B4 with the pinion fitted"}

# Hard stop and uplift paths.
r0, r1, dz0, dz1, _, hw = body.YAW_STOP_DOG
r_contact = (max(r0, body.YAW_STOP_BUMP[0]) + min(r1, body.YAW_STOP_BUMP[1])) / 2.0
bump_area = (body.YAW_STOP_BUMP[3] - body.YAW_STOP_BUMP[2]) * 2.0 * body.YAW_STOP_BUMP[4]
stop_cases = {"servo_current_limit": limit, "hand_twist_2Nm": 2.0}
results["hard_stop"] = {"deg": body.YAW_HARD_STOP_DEG, "contact_radius_mm": round(r_contact, 2),
                        "engagement_mm": round(min(r1, body.YAW_STOP_BUMP[1]) - max(r0, body.YAW_STOP_BUMP[0]), 2),
                        "cases": {k: {"force_N": round(t / (r_contact / 1000.0), 1),
                                      "bump_shear_MPa": round(t / (r_contact / 1000.0) / bump_area, 1)} for k, t in stop_cases.items()}}
uplift = robot_m * G * 3.0
results["uplift_path"] = {"design_N": round(uplift, 1),
                          "rotor_screws": "3 x M2.5 thread-forming, 6.6 mm in the PETG spigot",
                          "per_screw_N": round(uplift / 3.0, 1),
                          "post_and_clamp_screws": "3 x M2 x 8 clamp ring (outer ring) and 3 x M3 x 6 flange screws into frame inserts",
                          "per_flange_screw_N": round(uplift / 3.0, 1)}

# Drag against the yaw servo margin (D-047 ST3215-HS screen: ~3x at 63 rpm; XC330 was 8%).
drag = {"bearing_2Z_E": 0.002, "bearing_2RS_E_for_comparison": 0.015,
        "scissor_mesh_friction_E": round(0.1 * pre, 3), "ffc_loop_restoring_E": 0.002}
results["drag_Nm"] = {**drag, "total_with_2Z_E": round(drag["bearing_2Z_E"] + drag["scissor_mesh_friction_E"] + drag["ffc_loop_restoring_E"], 3),
                      "flag": "small against the ST3215-HS margin; B1 measures it"}

# FFC rolling loop.
r_in = body.YAW_ROTOR_DRUM[1] + 0.2
r_out = body.YAW_CASSETTE_WALL[0] - 0.2
r_u = (r_out - r_in) / 2.0
frac_fold = r_in / (r_in + r_out)
cap = math.radians(body.YAW_FFC_CAPACITY_DEG)
# Inner wrap clockwise from the slit, U-turn, outer wrap anticlockwise to the
# exit: exit = slit - W_in + W_out. With the D-044 loop budget W_in + W_out,
# take the solution with |W_out - W_in| below the budget.
delta = (body.YAW_CASSETTE_EXIT_DEG - body.YAW_ROTOR_FFC_SLOT_DEG) % 360.0
delta = delta if abs(delta) < body.YAW_FFC_LOOP_BUDGET_DEG else delta - 360.0
w_in, w_out = (body.YAW_FFC_LOOP_BUDGET_DEG - delta) / 2.0, (body.YAW_FFC_LOOP_BUDGET_DEG + delta) / 2.0
a_in0, a_out0 = math.radians(w_in), math.radians(w_out)
results["ffc_loop"] = {"inner_wrap_r_mm": round(r_in, 2), "outer_wrap_r_mm": round(r_out, 2), "u_turn_r_mm": round(r_u, 2),
                       "fold_turns_per_rotor_turn": round(frac_fold, 3),
                       "slit_deg": body.YAW_ROTOR_FFC_SLOT_DEG, "exit_deg": body.YAW_CASSETTE_EXIT_DEG,
                       "neutral_wraps_deg": [round(w_in, 1), round(w_out, 1)],
                       "u_turn_at_neutral_deg": round((body.YAW_ROTOR_FFC_SLOT_DEG - w_in) % 360.0, 1),
                       "inner_wrap_at_capacity_deg": [round(math.degrees(a_in0 - (1 - frac_fold) * cap)), round(math.degrees(a_in0 + (1 - frac_fold) * cap))],
                       "outer_wrap_at_capacity_deg": [round(math.degrees(a_out0 - frac_fold * cap)), round(math.degrees(a_out0 + frac_fold * cap))],
                       "loop_length_mm": round(r_in * a_in0 + math.pi * r_u + r_out * a_out0, 1),
                       "band_height_mm": round(body.YAW_CASSETTE_WALL[3] - body.YAW_CASSETTE_WALL[2], 2), "ffc_width_mm": body.YAW_FFC_WIDTH,
                       "copper_strain_at_u_turn_pct_E": round(100.0 * 0.03 / r_u, 2)}

# --- D-052 cable path -------------------------------------------------------------
cp = {}
ax = body.BODY_AXIS_X
fz0, fz1 = body.YAW_FFC_BAND_Z
cp["slit_top_over_ffc_mm"] = round(body.YAW_ROTOR_DRUM[3] - fz1, 2)
cp["slit_width_minus_stack_mm"] = round(2 * body.YAW_ROTOR_FFC_SLOT_HALF_WIDTH - body.YAW_JOINER_COUNT * body.YAW_FFC_STACK_T, 2)
planes = body.yaw_ffc_planes_y()
fold_r = math.hypot(body.YAW_FFC_WIDTH / 2.0 + 0.15, max(abs(y) for y in planes) + body.YAW_FFC_STACK_T)
cp["fold_square_max_r_mm"] = round(fold_r, 2)
cp["fold_to_drum_bore_mm"] = round(body.YAW_ROTOR_DRUM[0] - fold_r, 2)
cp["fold_top_to_lower_zif_mouth_mm"] = round(body.YAW_JOINER_Z[0] - fz1, 2)
cp["fold_bottom_to_stator_floor_mm"] = round(fz0 - body.YAW_CASSETTE_FLOOR[2], 2)
# Planes 3.3 mm apart, reached from the 1.6 mm slit over the straight run to the fold.
run = body.YAW_ROTOR_DRUM[0] - (body.YAW_FFC_WIDTH / 2.0 + 0.15)
off = max(abs(y) for y in planes)
cp["fan_out_s_bend_radius_mm_E"] = round((run ** 2 + off ** 2) / (4.0 * off), 2)
joiner = {label(p): p for p in moving if label(p).startswith(("PCB14_", "YAW_ROTOR_FFC_"))}
hits = {}
for n, part in joiner.items():
    for other in (hub, rotor, *disc):
        v = overlap(part, other)
        if v > TOL:
            hits[f"{n}:{label(other)}"] = v
for i, a in enumerate(list(joiner)):
    for b in list(joiner)[i + 1:]:
        v = overlap(joiner[a], joiner[b])
        if v > TOL and not ("RESERVE" in a and "RESERVE" in b):
            hits[f"{a}:{b}"] = v
cp["joiner_overlaps_mm3"] = hits
boards = [p for n, p in joiner.items() if n.startswith("PCB14_JOINER_")]
upper = [p for n, p in joiner.items() if "UPPER_ZIF" in n]
cp["joiner_to_disc_mm"] = round(min(b.distance(dd) for b in boards for dd in disc), 3)
cp["joiner_to_hub_mm"] = round(min(b.distance(hub) for b in boards), 3)
def max_r(part):
    bb = box(part)
    return max(math.hypot(x - ax, y) for x in (bb.min.X, bb.max.X) for y in (bb.min.Y, bb.max.Y))
narrow = [p for n, p in joiner.items() if "ZIF" in n]
cp["zif_max_r_mm"] = round(max(max_r(p) for p in narrow), 2)
cp["board_narrow_max_r_mm"] = round(math.hypot(body.YAW_JOINER_HALF_LENGTH, max(abs(y) for y0, _a, _b in body._yaw_joiner_y() for y in (y0, y0 + body.YAW_JOINER_BOARD_T))), 2)
head_mod = body._load_head_model()
cp["disc_bore_r_mm"] = head_mod.YAW_CABLE_BORE_R
cp["upper_zifs_inside_disc_bore_mm"] = round(head_mod.YAW_CABLE_BORE_R - max(max_r(p) for p in upper), 2)
cp["board_to_disc_bore_mm"] = round(head_mod.YAW_CABLE_BORE_R - cp["board_narrow_max_r_mm"], 2)
cp["disc_pilot_radial_clearance_mm"] = round(body.YAW_GEAR_BORE_RADIUS - head_mod.YAW_HUB_PILOT_R, 3)
pilot_bottom = body.YAW_DISC_TOP_Z - head_mod.YAW_HUB_PILOT_DEPTH
cp["disc_pilot_engagement_mm"] = round(body.YAW_DISC_PLATE_BOTTOM_Z - max(pilot_bottom, body.YAW_HUB_SHOULDER[2]), 2)
cp["tab_capture_radial_mm"] = round(min(math.hypot(body.YAW_JOINER_TAB[0], y) for y0, _a, _b in body._yaw_joiner_y()
                                        for y in (y0, y0 + body.YAW_JOINER_BOARD_T)) - body.YAW_GEAR_BORE_RADIUS, 2)
cp["tab_lift_gap_mm"] = round(body.YAW_HUB_SHOULDER[2] - body.YAW_JOINER_TAB[2], 2)
cp["tabs_below_pilot_mm"] = round(pilot_bottom - body.YAW_JOINER_TAB[2], 2)
cp["post_to_spigot_mm"] = round(body.YAW_HUB_SPIGOT[0] - math.hypot(body.YAW_JOINER_POST[1], body.YAW_JOINER_POST[2]), 2)
# Head-side FFC stack (head harness group) against the disc and the joiner boards.
harness = []
for p in leaves(body.rp01_head_groups()[1]):
    if label(p).startswith("yaw_FFC_x3_"):
        # Like the disc, the leaves keep head-local placement.
        h = p.moved(Location(body.HEAD_ORIGIN_IN_CHASSIS))
        h.label = label(p)
        harness.append(h)
assert len(harness) == 2, "head yaw FFC jackets not found"
cp["head_ffc_vs_disc_mm3"] = {label(h): overlap(h, dd) for h in harness for dd in disc if overlap(h, dd) > TOL}
cp["head_ffc_vs_joiner_mm3"] = {f"{label(h)}:{n}": overlap(h, p) for h in harness for n, p in joiner.items()
                                if "RESERVE" not in n and overlap(h, p) > TOL}
cp["head_ffc_top_below_disc_top_mm"] = round(body.YAW_DISC_TOP_Z - max(box(h).max.Z for h in harness), 2)
cp["head_ffc_to_disc_mm"] = round(min(h.distance(dd) for h in harness for dd in disc), 3)
results["cable_path_d052"] = cp

# --- Mass register ------------------------------------------------------------------
PETG, STEEL, BRASS, FR4 = 1.20, 7.85, 8.50, 1.85
ZIF_G = 0.4  # E: 22-pin 0.5 mm side-entry ZIF
rows = []
for p in [*cartridge, *pinion, *flange_fix, *servo_fix, *moving]:
    name = label(p)
    if "RESERVE" in name:
        continue
    if name.startswith("YAW_BEARING_61810"):
        rows.append((name, body.YAW_BEARING_MASS_G, p.center()))
        continue
    if "_ZIF_" in name:
        rows.append((name, ZIF_G, p.center()))
        continue
    density = (FR4 if name.startswith("PCB14_JOINER_BOARD") else BRASS if "INSERT" in name
               else STEEL if any(t in name for t in ("SCREW", "SHAFT", "SPRING")) else PETG)
    rows.append((name, p.volume * density / 1000.0, p.center()))
servo_box = None
for p in servo:
    b = box(p)
    servo_box = b if servo_box is None else servo_box.add(b)
rows.append(("ST3215_HS", 68.0, servo_box.center()))  # Waveshare listing (D)
loop = by["YAW_FFC_ROLLING_LOOP_RESERVE"]
rows.append(("FFC_22P_X3_IN_CASSETTE_AND_DROPS", 4.5, loop.center()))
total = sum(r[1] for r in rows)
com = tuple(sum(r[1] * getattr(r[2], ax) for r in rows) / total for ax in "XYZ")
moving_names = {label(p) for p in moving}
izz = sum(r[1] * ((r[2].X - body.BODY_AXIS_X) ** 2 + r[2].Y ** 2) for r in rows if r[0] in moving_names) * 1e-9
results["mass"] = {"total_g": round(total, 1), "com_mm": [round(c, 2) for c in com],
                   "rows_g": {r[0]: round(r[1], 2) for r in rows},
                   "moving_yaw_inertia_kg_m2_lower_bound": f"{izz:.2e}",
                   "head_yaw_inertia_kg_m2": body._HEAD_YAW_MASS["estimated_inertia_kg_m2"]}
reg = {row[0]: row for row in body.MASS_ROWS}["BODY_YAW_STAGE"]
results["mass_register_matches"] = abs(reg[1] - total) < 0.15 and all(abs(reg[2][i] - com[i]) < 0.15 for i in range(3))

out = HERE / "generated" / "yaw-stage.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2, default=str) + "\n")
print(json.dumps(results, indent=2, default=str))

for key in ("stage_vs_fixed_mm3", "stage_internal_mm3", "moving_vs_fixed_at_0_mm3", "yaw_sweep_clashes_mm3",
            "cartridge_lowering_clashes", "pinion_drop_clashes"):
    assert not results[key], f"{key} not clear"
for key in ("frame_solids", "hub_solids", "housing_solids", "rotor_solids"):
    assert results[key] == 1, f"{key} must be one solid"
assert results["stop_dog_vs_housing_mm3"]["61.5"] <= TOL and results["stop_dog_vs_housing_mm3"]["-61.5"] <= TOL
assert results["stop_dog_vs_housing_mm3"]["62.5"] > TOL and results["stop_dog_vs_housing_mm3"]["-62.5"] > TOL
assert results["mesh_max_overlap_mm3"] <= TOL, "gear interference"
assert results["mesh_min_gap_mm"] > 0.02, "mesh has no running clearance"
assert results["pinion_to_hub_shoulder_mm"] >= 0.4 and results["pinion_to_clamp_ring_mm"] >= 0.4
assert results["pinion_to_disc_plate_mm"] >= 0.3 and results["driven_face_covers_pinion"]
assert results["spring_to_bearing_od_mm"] >= 0.4
assert results["disc_to_hub_contact_mm"] <= 0.01, "the disc must sit on the hub"
assert results["pinion_to_disc_mm"] >= 0.3
assert results["cassette_to_cooler_top_mm"] >= 10.5, "Pi cooler headroom"
assert results["ffc_loop"]["band_height_mm"] - body.YAW_FFC_WIDTH >= 0.5
assert min(results["ffc_loop"]["inner_wrap_at_capacity_deg"] + results["ffc_loop"]["outer_wrap_at_capacity_deg"]) >= 30
assert results["preload_spring"]["bending_stress_MPa"] <= results["preload_spring"]["music_wire_allow_MPa_E"]
assert results["preload_spring"]["body_length_mm"] <= results["preload_spring"]["envelope_mm"]
assert all(c["s0"] >= 4.0 for c in results["bearing_61810_2Z"]["cases"].values())
assert results["mass_register_matches"], "update the BODY_YAW_STAGE mass row from results['mass']"
cp = results["cable_path_d052"]
assert cp["slit_top_over_ffc_mm"] >= 0.5 and cp["slit_width_minus_stack_mm"] >= 0.3, "FFC band must pass the drum slit"
assert cp["fold_to_drum_bore_mm"] >= 1.0 and cp["fold_bottom_to_stator_floor_mm"] >= 0.3
assert cp["fold_top_to_lower_zif_mouth_mm"] >= 1.0, "straight tail before the lower ZIFs"
assert cp["fan_out_s_bend_radius_mm_E"] >= 2.5
assert not cp["joiner_overlaps_mm3"], "PCB-14 joiner parts clash"
assert cp["joiner_to_disc_mm"] >= 0.5 and cp["joiner_to_hub_mm"] >= 0.5
assert cp["upper_zifs_inside_disc_bore_mm"] >= 0.5 and cp["board_to_disc_bore_mm"] >= 0.5
assert 0.1 <= cp["disc_pilot_radial_clearance_mm"] <= 0.2 and cp["disc_pilot_engagement_mm"] >= 5.0
assert cp["tab_capture_radial_mm"] >= 0.3 and 0.3 <= cp["tab_lift_gap_mm"] <= 1.2 and cp["tabs_below_pilot_mm"] >= 0.5
assert cp["post_to_spigot_mm"] >= 1.0
assert not cp["head_ffc_vs_disc_mm3"] and not cp["head_ffc_vs_joiner_mm3"] and cp["head_ffc_top_below_disc_top_mm"] >= 0.3
assert max(results["mount_screw_axis_offset_mm"]) <= 0.1, "mount screws miss the STEP hole axes"
print("ALL PASS")
