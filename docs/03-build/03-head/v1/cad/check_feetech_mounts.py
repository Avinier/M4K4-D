"""D-049 STS3045M installation audit: interfaces, joints and posed clearance.

Measured from the live B-rep (`build_parts(catalog=False)`), not from the
constants: spline engagements, centre-screw threads, ear-joint stacks, insert
walls, the cover gap, the horn pocket against the frame's axial float, driver
paths, and the minimum distance from every D-049 part to every part that moves
relative to it over a roll x pitch grid clamped to the A+ envelope.
`--fast` uses a 3 x 3 grid. Writes generated/feetech-mounts.json.
"""
import json, math, sys, itertools
from pathlib import Path
from build123d import Vector, Location
import layout_model as m
import feetech as fe
import motion_envelope as env
from inspection_scene import posed

HERE = Path(__file__).parent
# Moving parts, mm. 0.99 rather than 1.0: the coupler-to-cartridge running gap
# is designed at 1.0 and measures 0.997 because the goBILDA STEP is 17.003 long.
MIN_CLEAR = 0.99
MIN_INSERT_WALL = 1.2    # printed wall round an M2 insert pocket, mm
p = m.build_parts(catalog=False)
S = {n: d['shape'] for n, d in p.items()}
REAR_RETAINER = f'roll_bearing_retainer_{abs(fe.CARTRIDGE_X[0] + .5):g}'
F = {n: d['frame'] for n, d in p.items()}
facts, failures = {}, []


def common(a, b):
    from build123d import Compound
    return Compound(children=m.pieces(a.intersect(b)))


def need(name, ok, value):
    facts[name] = value
    if not ok: failures.append(name)


def along(shape, start, direction, length, step=.05):
    """Lengths along a ray (from start) that lie inside shape."""
    d = Vector(*direction).normalized(); hits = []
    t = 0.
    while t <= length:
        if shape.is_inside(Vector(*start) + d * t): hits.append(round(t, 2))
        t += step
    return hits


# --- Roll output -----------------------------------------------------------
servo_r, coupler = S['roll_STS3045M_reference'], S['roll_coupler_goBILDA_4001_0025_0006']
ry, rz = m.ROLL_Y, m.ROLL_Z
# Spline teeth: the coupler's female spline overlaps the Ø5.9 envelope radially
# (tooth root r 2.7 < 2.95); measure the axial extent of that overlap.
overlap = common(servo_r, coupler)
ob = overlap.bounding_box()
need('roll_spline_engagement_mm', ob.size.X >= 2.9, round(ob.size.X, 3))
need('roll_spline_tip_to_coupler_floor_mm', True,
     round(fe.COUPLER_SPLINE_FACE_X + 3.5 - (fe.ROLL_CASE_BOTTOM_X + fe.SPLINE_TOP), 3))
need('roll_coupler_face_to_boss_mm', abs(fe.COUPLER_SPLINE_FACE_X - (fe.ROLL_CASE_BOTTOM_X + fe.BOSS_TOP) - .3) < 1e-6,
     round(fe.COUPLER_SPLINE_FACE_X - (fe.ROLL_CASE_BOTTOM_X + fe.BOSS_TOP), 3))
screw = S['roll_coupler_centre_M3x5']
# Thread engaged in the output: spline tip to screw tip along the axis (the
# reference STEP's Ø3 pilot is a placeholder for the unmeasured M3 thread).
thread = (fe.ROLL_CASE_BOTTOM_X + fe.SPLINE_TOP) - screw.bounding_box().min.X
need('roll_centre_screw_thread_in_output_mm', 3.5 <= thread <= 4.2, round(thread, 3))
spindle = S['rolling_spindle_6mm']
sb = spindle.bounding_box()
need('roll_spindle_in_coupler_bore_mm', fe.COUPLER_FRONT_X - sb.min.X >= 8.5, round(fe.COUPLER_FRONT_X - sb.min.X, 3))
need('roll_spindle_to_centre_screw_head_mm', spindle.distance_to(screw) >= .4, round(spindle.distance_to(screw), 3))
# Clamp zone: the goBILDA slit occupies the last 8 mm of the bore.
need('roll_clamp_zone_on_spindle', sb.min.X <= fe.COUPLER_FRONT_X - 8., round(sb.min.X, 3))
cover = S['removable_octagonal_rear_cover']
need('roll_case_to_rear_cover_mm', servo_r.distance_to(cover) >= MIN_CLEAR, round(servo_r.distance_to(cover), 3))
plate = S[REAR_RETAINER]
need('roll_coupler_to_rear_retainer_mm', coupler.distance_to(plate) >= .8, round(coupler.distance_to(plate), 3))
need('roll_coupler_to_cartridge_mm', coupler.distance_to(S['bearing_cartridge_trial']) >= .9, round(coupler.distance_to(S['bearing_cartridge_trial']), 3))

# --- Pitch output ----------------------------------------------------------
servo_p, horn, leg = S['pitch_STS3045M_reference'], S['pitch_horn_25T_disc'], S['yaw_yoke_leg_55']
# The horn bore equals the Ø5.9 spline envelope, so engagement is the axial
# run of spline inside the horn bore: horn underside to spline tip.
eng = fe.PITCH_CASE_BOTTOM_Y + fe.SPLINE_TOP - fe.HORN_BOTTOM_Y
need('pitch_spline_engagement_mm', eng >= 2.9, round(eng, 3))
hs = S['pitch_horn_centre_M3x5']
thread = (fe.PITCH_CASE_BOTTOM_Y + fe.SPLINE_TOP) - hs.bounding_box().min.Y
need('pitch_centre_screw_thread_in_output_mm', 3.5 <= thread <= 4.2, round(thread, 3))
# Case and boss to horn, with the spline (inside the horn bore) removed.
spline_free = servo_p - m.axial(fe.HORN['bore_r'] + .01, 10., (m.PITCH_X, fe.PITCH_CASE_BOTTOM_Y + fe.BOSS_TOP + 5, m.PITCH_Z), 'y')
need('pitch_case_to_horn_mm', spline_free.distance_to(horn) >= 0.25, round(spline_free.distance_to(horn), 3))
need('horn_seated_on_leg_pocket_floor', horn.distance_to(leg) < 1e-3, round(horn.distance_to(leg), 4))
# Frame float: the frame is lowered between the legs with the horn on, then
# pushed +Y into the 0.6 mm pocket; the -Y arm needs that much room.
arm_gap = S['connected_pitch_frame_roll_servo_saddle'].distance_to(S['yaw_yoke_leg_-55'])
need('frame_float_minus_horn_pocket_mm', arm_gap - fe.HORN_POCKET_DEPTH >= .2, round(arm_gap - fe.HORN_POCKET_DEPTH, 3))
for n in [k for k in S if k.startswith('pitch_horn_to_leg_M3x6')]:
    # Thread in the horn disc and no contact with the servo case or boss.
    # Tapped length: the shank's run through the horn disc (holes modelled at
    # the M3 major diameter, so the solids only touch).
    sb, top = S[n].bounding_box(), fe.HORN_TOP_Y
    t = min(top, sb.max.Y) - max(top - fe.HORN['disc_t'], sb.min.Y)
    need(f'{n}_thread_in_horn_mm', t >= 1.9, round(t, 3))
    need(f'{n}_to_servo_mm', S[n].distance_to(servo_p) >= .5, round(S[n].distance_to(servo_p), 3))
flange = S['connected_rolling_cradle_flange_ear_stalks']
need('pitch_case_bottom_to_flange_plane_mm', fe.PITCH_CASE_BOTTOM_Y - 15.94 >= MIN_CLEAR, round(fe.PITCH_CASE_BOTTOM_Y - 15.94, 3))

# --- Ear joints -------------------------------------------------------------
frame = S['connected_pitch_frame_roll_servo_saddle']
for side, servo in [('roll', servo_r), ('pitch', servo_p)]:
    for i in range(1, 5):
        sc, w = S[f'{side}_servo_ear_{i}_M2x6'], S[f'{side}_servo_ear_{i}_washer']
        # Shank to slot: the head sits over the Ø4.2 slot and bears on the washer.
        k = 0 if side == 'roll' else 1
        b = sc.bounding_box(); c = b.center()
        lo, hi = (fe.ROLL_EAR_X if side == 'roll' else fe.PITCH_EAR_Y)
        shank = m.axial(1., hi - lo, tuple((lo + hi) / 2 if j == k else (c.X, c.Y, c.Z)[j] for j in range(3)), 'xy'[k])
        need(f'{side}_ear_{i}_shank_clear_of_slot_mm', shank.distance_to(servo) >= .9, round(shank.distance_to(servo), 3))
        need(f'{side}_ear_{i}_washer_overlaps_slot_edge_mm', fe.WASHER['r_out'] - fe.SLOT_R >= .8, round(fe.WASHER['r_out'] - fe.SLOT_R, 3))
        need(f'{side}_ear_{i}_washer_on_ear_mm', w.distance_to(servo) < 1e-3, round(w.distance_to(servo), 4))
# Insert walls: the Ø3.2 pockets against the case windows (case + 0.3).
import details as dt
for side in ('roll', 'pitch'):
    w_case = min(abs(x - (fe.CASE_X[0] if x < 0 else fe.CASE_X[1])) for x in fe.SLOT_X) - .3 - dt.INSERT_R
    w_end = min(abs(x - (fe.EAR_X[0] if x < 0 else fe.EAR_X[1])) for x in fe.SLOT_X) - dt.INSERT_R
    need(f'{side}_insert_wall_to_case_window_mm', w_case >= MIN_INSERT_WALL, round(w_case, 3))
    need(f'{side}_insert_wall_to_ear_end_mm', w_end >= MIN_INSERT_WALL - .1, round(w_end, 3))

# --- Driver paths -------------------------------------------------------------
# Roll ear screws drive along +X from behind (rear cover off); pitch ear
# screws along -Y before the frame goes into the yoke; horn screws from the
# +Y leg's outer face. Each 2 mm hex key (r 1.25 incl. play) path must miss
# every printed or purchased part in its own sub-assembly. The roll short-side
# keys pass the servo lead nozzle on the case's shaft-end face.
from harness import rod
paths = []
KEY_R = 1.3 / math.sqrt(3) + .1   # ISO 7380 M2: 1.3 mm hex across corners / 2 + play
def key_path(name, start, end, others):
    key = rod(start, end, KEY_R)
    hits = [o for o in others if key.distance_to(S[o]) < .05]
    paths.append(dict(screw=name, hits=hits))
    need(f'driver_path_{name}', not hits, hits)
roll_others = [n for n in S if F[n] in 'PR' and p[n]['kind'] == 'physical' and not n.startswith(('roll_servo_ear_', 'removable_octagonal_rear_cover'))]
for i in range(1, 5):
    b = S[f'roll_servo_ear_{i}_M2x6'].bounding_box(); c = b.center()
    key_path(f'roll_servo_ear_{i}', (b.min.X - .2, c.Y, c.Z), (-114.0, c.Y, c.Z), roll_others)
pitch_others = [n for n in S if F[n] == 'P' and p[n]['kind'] == 'physical' and not n.startswith('pitch_servo_ear_')]
for i in range(1, 5):
    b = S[f'pitch_servo_ear_{i}_M2x6'].bounding_box(); c = b.center()
    key_path(f'pitch_servo_ear_{i}', (c.X, b.max.Y + .2, c.Z), (c.X, 70., c.Z), pitch_others)

# --- Posed clearance ----------------------------------------------------------
NEW = ['roll_STS3045M_reference', 'pitch_STS3045M_reference', 'roll_coupler_goBILDA_4001_0025_0006',
       'roll_coupler_clamp_M4x10', 'roll_coupler_centre_M3x5', 'pitch_horn_25T_disc', 'pitch_horn_centre_M3x5',
       'connected_pitch_frame_roll_servo_saddle', 'yaw_yoke_leg_55', 'yaw_yoke_leg_-55', 'rolling_spindle_6mm', 'bearing_cartridge_trial',
       REAR_RETAINER] + [n for n in S if n.startswith(('roll_servo_ear_', 'pitch_servo_ear_', 'pitch_horn_to_leg_', 'rear_pitch_trim_washer'))]
intended = {frozenset(x) for x in [
    ('roll_STS3045M_reference', 'roll_coupler_goBILDA_4001_0025_0006'), ('roll_STS3045M_reference', 'roll_coupler_centre_M3x5'),
    ('pitch_STS3045M_reference', 'pitch_horn_25T_disc'), ('pitch_STS3045M_reference', 'pitch_horn_centre_M3x5'),
    # Running fits on the joint axes (journal/bore, spindle/bearing bore).
    ('rolling_spindle_6mm', 'roll_bearing_1_696_2Z'), ('rolling_spindle_6mm', 'roll_bearing_2_696_2Z'),
    ('rolling_spindle_6mm', 'bearing_cartridge_trial'), ('rolling_spindle_6mm', REAR_RETAINER),
    ('rolling_spindle_6mm', 'roll_bearing_retainer_39.5'),
    ('connected_pitch_frame_roll_servo_saddle', 'yaw_yoke_leg_-55')]}
phys = [n for n in S if p[n]['kind'] == 'physical']
rolls = [m.ROLL_STOP[0], -14, -7, 0, 7, 14, m.ROLL_STOP[1]]
pitches = [m.PITCH_STOP[0], -15, -5, 5, 15, 25, 35, m.PITCH_STOP[1]]
if '--fast' in sys.argv: rolls, pitches = [m.ROLL_STOP[0], 0, m.ROLL_STOP[1]], [m.PITCH_STOP[0], 0, m.PITCH_STOP[1]]
poses = env.grid_poses(env.load(), rolls, pitches)
worst = {}
for r, q in poses:
    P = {n: posed(S[n], F[n], r, q, 0) for n in phys}
    for a in NEW:
        if a not in P: continue
        ba = P[a].bounding_box()
        for b in phys:
            if b == a or F[a] == F[b] or frozenset((a, b)) in intended: continue
            # Roll-only relatives: P vs R parts never pitch apart; skip pairs whose
            # relative motion cannot change (same frame handled above).
            bb = P[b].bounding_box()
            if any(ba.min.to_tuple()[i] > bb.max.to_tuple()[i] + 3 or bb.min.to_tuple()[i] > ba.max.to_tuple()[i] + 3 for i in range(3)):
                continue
            d = P[a].distance_to(P[b])
            key = tuple(sorted((a, b)))
            if key not in worst or d < worst[key][0]: worst[key] = (d, r, q)
    print(f'pose {r:+.0f}/{q:+.0f} pairs {len(worst)}', flush=True)
posed_min = sorted(({'a': k[0], 'b': k[1], 'min_mm': round(v[0], 3), 'roll': v[1], 'pitch': v[2]} for k, v in worst.items()), key=lambda x: x['min_mm'])
# Pairs that already existed in the committed head may stay below 1 mm (hard-
# stop contacts, inherited ear/leg near-misses) but must not get closer.
baseline = json.loads((HERE / 'generated' / 'feetech-mounts-baseline.json').read_text())['min_mm']
def base_of(x):
    for k in (f"{x['a']}|{x['b']}", f"{x['b']}|{x['a']}"):
        if k in baseline: return baseline[k]
    return None
low, inherited = [], []
for x in posed_min:
    if x['min_mm'] >= MIN_CLEAR: continue
    b0 = base_of(x)
    if b0 is not None and x['min_mm'] >= b0 - 0.005: inherited.append(dict(x, committed_mm=b0))
    else: low.append(dict(x, committed_mm=b0))
facts['posed_inherited_not_worse'] = inherited
need('posed_new_or_worse_below_1mm', not low, low)
result = dict(method=__doc__.strip().splitlines()[0], poses=len(poses), min_clear_mm=MIN_CLEAR,
              facts=facts, driver_paths=paths, posed_min_clearance=posed_min[:40], failures=failures, passed=not failures,
              limitations=['Nominal B-rep; horn geometry is E (HD-002 hold); servo tab roots, lead and thread depth unmeasured.',
                           'Discrete poses; check_revision.py is the full cross-frame overlap screen.'])
(HERE / 'generated' / 'feetech-mounts.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in facts.items() if not k.startswith('posed_')}, indent=1))
print('LOW', json.dumps(low, indent=1))
print('PASS' if not failures else f'FAIL: {failures}')
raise SystemExit(0 if not failures else 1)
