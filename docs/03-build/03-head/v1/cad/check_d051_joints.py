"""D-051 audit: the -Y pitch pivot and the leg-to-disc joints.

Measured from the live B-rep (`load_parts(catalog=False)`): pivot stack (pin
in the D-bore and through the bearing, bearing seated on its lip, retainer
heads flush with the leg face, pin end under the retainer), insert and socket
walls, screw engagement, the frame's assembly float, and the minimum distance
from every new or changed part to every part that moves relative to it over
the 7 x 8 roll x pitch grid clamped to the A+ envelope (the D-049 audit grid).
Writes generated/d051-joints.json. Screw stacks: check_fasteners.py.
"""
import json, math, sys
from pathlib import Path
from build123d import Vector, Compound
import layout_model as m
import feetech as fe
import motion_envelope as env
from cad_cache import load_parts
from inspection_scene import posed

HERE = Path(__file__).parent
MIN_CLEAR = .99
MIN_WALL = 1.2
p = load_parts(catalog=False)
S = {n: d['shape'] for n, d in p.items()}
F = {n: d['frame'] for n, d in p.items()}
facts, failures = {}, []


def need(name, ok, value):
    facts[name] = value
    if not ok: failures.append(name)


def vol(x):
    return sum(v.volume for v in m.pieces(x))


t, k = fe.TRUNNION, fe.LEG_KEY
PX, PZ, d = m.PITCH_X, m.PITCH_Z, m.YAW_DISC_TOP_Z
pin, brg, ret = S['pitch_trunnion_D6x12_pin'], S['pitch_trunnion_bearing_MR106ZZ'], S['pitch_trunnion_retainer']
frame, legm, legp, disc = (S['connected_pitch_frame_roll_servo_saddle'], S['yaw_yoke_leg_-55'],
                           S['yaw_yoke_leg_55'], S['yaw_turntable_disc_flush'])
outer = -(fe.LEG_INNER_Y + 6)

# --- -Y pivot ------------------------------------------------------------------
pb, bb = pin.bounding_box(), brg.bounding_box()
need('pin_in_frame_bore_mm', pb.max.Y - t['bore_y'][0] >= 6.5, round(pb.max.Y - t['bore_y'][0], 3))
need('pin_spans_bearing', pb.min.Y <= bb.min.Y and pb.max.Y >= bb.max.Y, [round(pb.min.Y, 2), round(pb.max.Y, 2)])
need('pin_to_frame_mm', 0 < pin.distance_to(frame) <= .06, round(pin.distance_to(frame), 3))
need('pin_to_bearing_bore_mm', 0 < pin.distance_to(brg) <= .06, round(pin.distance_to(brg), 3))
need('pin_end_to_retainer_mm', .1 <= pin.distance_to(ret) <= .3, round(pin.distance_to(ret), 3))
need('pin_to_leg_mm', pin.distance_to(legm) >= .9, round(pin.distance_to(legm), 3))
need('bearing_seated_in_leg', brg.distance_to(legm) < 1e-3, round(brg.distance_to(legm), 4))
need('bearing_to_frame_mm', brg.distance_to(frame) >= MIN_CLEAR, round(brg.distance_to(frame), 3))
need('retainer_on_bearing', ret.distance_to(brg) < 1e-3, round(ret.distance_to(brg), 4))
# The retainer bears on the outer ring only: relief over the inner ring.
need('retainer_relief_clears_inner_ring', t['plate_relief'][0] > t['bearing']['d'] / 2 + .6, t['plate_relief'][0])
need('lip_hole_clears_inner_ring_mm', t['lip_hole_r'] - (t['bearing']['d'] / 2 + .6) >= .2, round(t['lip_hole_r'] - 3.6, 3))
lip = t['lip_y'][1] - t['lip_y'][0]
need('lip_thickness_mm', lip >= .7 - 1e-6, round(lip, 3))
heads = [S[n] for n in S if n.startswith('pitch_trunnion_retainer_M2x4')]
proud = max(-h.bounding_box().min.Y + outer for h in heads)
need('retainer_heads_not_proud_of_leg_face_mm', proud <= 1e-3, round(proud, 3))
need('retainer_not_proud_of_leg_face_mm', -ret.bounding_box().min.Y + outer <= 0, round(-ret.bounding_box().min.Y + outer, 3))
# Insert pocket walls: to the bearing seat, to the pitch-stop slot (R9..R11
# over Y -55..-51, 137..205 deg plus the pin) and to the leg's own outline.
walls = []
for (x, z), deg in zip(m.trunnion_screw_points(), t['screw_deg']):
    to_seat = t['screw_r'] - 1.6 - t['seat_r']
    ang = min(abs(deg - a) for a in (137., 205.)) if not 137 <= deg <= 205 else 0
    to_slot = 2 * t['screw_r'] * math.sin(math.radians(ang) / 2) - 1.6 - 1. if 137 > deg or deg > 205 else -1
    probe = m.yspan(1.6 + MIN_WALL, t['recess_floor_y'], t['recess_floor_y'] + t['insert_pocket'], x, z)
    outside = probe.volume - vol(probe.intersect(legm + m.yspan(1.6, -60, -50, x, z)))
    walls.append(dict(deg=deg, to_seat=round(to_seat, 3), to_slot=round(to_slot, 3), wall_ring_outside_leg_mm3=round(outside, 4)))
need('retainer_insert_walls', all(w['to_seat'] >= MIN_WALL and w['to_slot'] >= MIN_WALL and w['wall_ring_outside_leg_mm3'] < .01 for w in walls), walls)
fb = frame.distance_to(legm)
need('frame_float_minus_horn_pocket_mm', fb - fe.HORN_POCKET_DEPTH >= .2, round(fb - fe.HORN_POCKET_DEPTH, 3))

# --- Leg feet --------------------------------------------------------------------
for s_, leg in ((1, legp), (-1, legm)):
    tag = f'{55 * s_}'
    key = Compound(children=m.pieces(disc.intersect(m.block(PX + k['dx'][0] - .01, PX + k['dx'][1] + .01, *sorted((s_ * (k['y'][0] - .01), s_ * (k['y'][1] + .01))), d + .01, d + k['h'] + .01))))
    kv = vol(key)
    need(f'key_{tag}_volume_mm3', kv > .9 * (k['dx'][1] - k['dx'][0]) * (k['y'][1] - k['y'][0]) * k['h'] - 60, round(kv, 2))
    need(f'key_{tag}_overlap_with_leg_mm3', vol(key.intersect(leg)) < 1e-4 if key else True, round(vol(key.intersect(leg)), 5))
    sock = m.block(PX + k['dx'][0] - k['clear'], PX + k['dx'][1] + k['clear'], *sorted((s_ * (k['y'][0] - k['clear']), s_ * (k['y'][1] + k['clear']))), d, d + k['h'] + k['top_clear'])
    # Socket walls: grow the socket by the minimum wall and require it to stay in the leg.
    grown = m.block(PX + k['dx'][0] - k['clear'] - MIN_WALL, PX + k['dx'][1] + k['clear'] + MIN_WALL,
                    *sorted((s_ * (k['y'][0] - k['clear'] - MIN_WALL), s_ * (k['y'][1] + k['clear'] + MIN_WALL))), d + .05, d + k['h'] + k['top_clear'] + MIN_WALL)
    shell = grown - sock
    inside = vol(shell.intersect(leg))
    holes = sum(vol(m.yspan(1.15, s_ * 47, s_ * 52, PX + dx, d + k['screw_h']).intersect(shell)) for dx in k['screw_dx'])
    need(f'socket_{tag}_wall_ge_1p2', shell.volume - inside - holes < .5, round(shell.volume - inside - holes, 3))
    for dx in k['screw_dx']:
        sc = S[f'yaw_leg_to_disc_M2x6_{55 * s_}_{dx:g}']
        # Shank length inside the key's insert pocket, and wall round the pocket.
        sb = sc.bounding_box()
        tip = sb.max.Y if s_ > 0 else -sb.min.Y
        eng = min(tip, k['y'][0] + 3.) - k['y'][0]
        need(f'leg_screw_{tag}_{dx:g}_insert_engagement_mm', eng >= 2.4, round(eng, 3))
        need(f'leg_screw_{tag}_{dx:g}_tip_in_pocket', tip <= k['y'][0] + k['insert_pocket'] - .1, round(tip, 3))
        w = min(dx - 1.6 - k['dx'][0], k['dx'][1] - dx - 1.6, k['h'] - k['screw_h'] - 1.6)
        need(f'leg_screw_{tag}_{dx:g}_key_wall_mm', w >= MIN_WALL, round(w, 3))
    gap = k['screw_dx'][1] - k['screw_dx'][0] - 3.2
    need(f'key_{tag}_pocket_web_mm', gap >= MIN_WALL, round(gap, 3))

# --- Posed clearance ---------------------------------------------------------
NEW = ['pitch_trunnion_D6x12_pin', 'pitch_trunnion_bearing_MR106ZZ', 'pitch_trunnion_retainer',
       'connected_pitch_frame_roll_servo_saddle', 'yaw_yoke_leg_55', 'yaw_yoke_leg_-55', 'yaw_turntable_disc_flush'] + \
      [n for n in S if n.startswith(('pitch_trunnion_retainer_M2x4', 'yaw_leg_to_disc_M2x6'))]
# Running fits on the pivot axis: pin in the bearing bore (0.05 mm modelled
# radial gap) and the pin end 0.2 mm under the retainer; both are measured
# above, and the pin is coaxial with the pitch axis, so they cannot change.
intended = {frozenset(x) for x in [('connected_pitch_frame_roll_servo_saddle', 'yaw_yoke_leg_-55'),
                                   ('pitch_trunnion_D6x12_pin', 'pitch_trunnion_bearing_MR106ZZ'),
                                   ('pitch_trunnion_D6x12_pin', 'pitch_trunnion_retainer')]}
phys = [n for n in S if p[n]['kind'] == 'physical']
rolls = [m.ROLL_STOP[0], -14, -7, 0, 7, 14, m.ROLL_STOP[1]]
pitches = [m.PITCH_STOP[0], -15, -5, 5, 15, 25, 35, m.PITCH_STOP[1]]
if '--fast' in sys.argv: rolls, pitches = [m.ROLL_STOP[0], 0, m.ROLL_STOP[1]], [m.PITCH_STOP[0], 0, m.PITCH_STOP[1]]
poses = env.grid_poses(env.load(), rolls, pitches)
worst = {}
for r, q in poses:
    P = {n: posed(S[n], F[n], r, q, 0) for n in phys}
    for a in NEW:
        ba = P[a].bounding_box()
        for b in phys:
            if b == a or F[a] == F[b] or frozenset((a, b)) in intended: continue
            bx = P[b].bounding_box()
            if any(ba.min.to_tuple()[i] > bx.max.to_tuple()[i] + 3 or bx.min.to_tuple()[i] > ba.max.to_tuple()[i] + 3 for i in range(3)):
                continue
            v = P[a].distance_to(P[b]); key = tuple(sorted((a, b)))
            if key not in worst or v < worst[key][0]: worst[key] = (v, r, q)
    print(f'pose {r:+.1f}/{q:+.0f} pairs {len(worst)}', flush=True)
posed_min = sorted(({'a': x[0], 'b': x[1], 'min_mm': round(v[0], 3), 'roll': v[1], 'pitch': v[2]} for x, v in worst.items()), key=lambda x: x['min_mm'])
# Pairs that existed before D-051 may stay as close as they were (D-050 leg
# sweep and the committed D-049 mounts audit); new pairs must keep 1 mm.
base = {}
for f_ in ('leg-clearance-d050.json',):
    for kk, v in json.loads((HERE / 'generated' / f_).read_text()).items(): base[kk] = v[0]
mounts = json.loads((HERE / 'generated' / 'feetech-mounts.json').read_text())
for x in mounts['posed_min_clearance']: base[f"{x['a']}|{x['b']}"] = x['min_mm']
def base_of(x):
    for kk in (f"{x['a']}|{x['b']}", f"{x['b']}|{x['a']}"):
        if kk in base: return base[kk]
low, inherited = [], []
for x in posed_min:
    if x['min_mm'] >= MIN_CLEAR: continue
    b0 = base_of(x)
    (inherited if b0 is not None and x['min_mm'] >= b0 - .005 else low).append(dict(x, before_mm=b0))
facts['posed_inherited_not_worse'] = inherited
need('posed_new_or_worse_below_1mm', not low, low)
res = dict(method=__doc__.strip().splitlines()[0], poses=len(poses), facts=facts, posed_min_clearance=posed_min[:40],
           failures=failures, passed=not failures,
           limitations=['Nominal B-rep; MR106ZZ, D-shaft, insert and screw fits are catalogue values to confirm on received parts.',
                        'Joint compliance is not in the leg FEA (bench B6).'])
out = 'd051-joints-fast.json' if '--fast' in sys.argv else 'd051-joints.json'
(HERE / 'generated' / out).write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps({kk: v for kk, v in facts.items() if not kk.startswith('posed_')}, indent=1))
print('LOW', json.dumps(low, indent=1))
print('PASS' if not failures else f'FAIL: {failures}')
raise SystemExit(0 if not failures else 1)
