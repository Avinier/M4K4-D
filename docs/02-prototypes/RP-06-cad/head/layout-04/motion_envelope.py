"""Layout 04 roll/pitch sweep record against the yaw disc.

For each whole pitch degree up to the hard stops, the table gives the roll
interval that keeps the lowest R/P-carried point at or above SWEEP_FLOOR_Z.
The hard stops sit STOP_MARGIN_DEG beyond storyboard usable travel; at the
Layout 04 neck the floor lies below the full hard-stop sweep, so every row is
the full stop range and the stops alone keep the head off the disc. The file
also records the sweep with a further 1 deg of stop overtravel.
"""
import json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
ENVELOPE_PATH = HERE / 'motion-envelope.json'
# Usable travel (storyboard) and hard stops 3 deg beyond it, per storyboard.md:
# stops must sit outside usable travel with their own margin.
ROLL_USABLE, PITCH_USABLE = (-18.0, 18.0), (-22.0, 40.0)
STOP_MARGIN_DEG = 3.0
ROLL_STOP = (ROLL_USABLE[0] - STOP_MARGIN_DEG, ROLL_USABLE[1] + STOP_MARGIN_DEG)
PITCH_STOP = (PITCH_USABLE[0] - STOP_MARGIN_DEG, PITCH_USABLE[1] + STOP_MARGIN_DEG)
TABLE_STEP = 1.0


def _rotation(axis_dir, angle_deg):
    k = np.asarray(axis_dir, float); k /= np.linalg.norm(k)
    a = math.radians(angle_deg)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


def _about(points, origin, axis_dir, angle_deg):
    o = np.asarray(origin, float)
    return (points - o) @ _rotation(axis_dir, angle_deg).T + o


class Sweep:
    """Lowest R/P-carried point for any roll/pitch, from one tessellation."""

    def __init__(self, parts, m):
        self.m = m
        clouds = {'R': [], 'P': []}
        for d in parts.values():
            if d['frame'] in clouds:
                verts, _ = d['shape'].tessellate(0.05, 0.2)
                clouds[d['frame']].append(np.array([tuple(v) for v in verts]))
        self.r = np.vstack(clouds['R'])
        self.p = np.vstack(clouds['P'])

    def min_z(self, roll, pitch):
        m = self.m
        roll_o, pitch_o = (0, m.ROLL_Y, m.ROLL_Z), (m.PITCH_X, 0, m.PITCH_Z)
        r = _about(_about(self.r, roll_o, (1, 0, 0), roll), pitch_o, (0, 1, 0), pitch)
        p = _about(self.p, pitch_o, (0, 1, 0), pitch)
        return float(min(r[:, 2].min(), p[:, 2].min()))


def _limit(sweep, pitch, floor, sign):
    """Largest |roll| in 0.25° steps (one side) that keeps min Z >= floor."""
    best = 0.0
    for q in np.arange(0.25, ROLL_STOP[1] + 1e-9, 0.25):
        if sweep.min_z(sign * q, pitch) < floor:
            break
        best = float(q)
    return best


def solve(sweep, floor):
    rows = []
    for pitch in np.arange(PITCH_STOP[0], PITCH_STOP[1] + 1e-9, TABLE_STEP):
        # Whole-degree roll limits are rounded toward zero for firmware.
        rows.append(dict(pitch_deg=float(pitch),
                         roll_min_deg=-math.floor(_limit(sweep, pitch, floor, -1)),
                         roll_max_deg=math.floor(_limit(sweep, pitch, floor, 1))))
    return rows


def roll_interval(table, pitch):
    """Firmware rule: the narrower of the two neighbouring table rows."""
    rows = table['rows']
    pitch = max(PITCH_STOP[0], min(PITCH_STOP[1], pitch))
    lo = max((r for r in rows if r['pitch_deg'] <= pitch + 1e-9), key=lambda r: r['pitch_deg'])
    hi = min((r for r in rows if r['pitch_deg'] >= pitch - 1e-9), key=lambda r: r['pitch_deg'])
    return max(lo['roll_min_deg'], hi['roll_min_deg']), min(lo['roll_max_deg'], hi['roll_max_deg'])


def allowed(table, roll, pitch):
    lo, hi = roll_interval(table, pitch)
    return PITCH_STOP[0] <= pitch <= PITCH_STOP[1] and lo - 1e-9 <= roll <= hi + 1e-9


def clamp_roll(table, roll, pitch):
    lo, hi = roll_interval(table, pitch)
    return max(lo, min(hi, roll))


def grid_poses(table, rolls, pitches):
    """Roll x pitch sample grid clamped onto the envelope; boundary poses kept."""
    return sorted({(float(clamp_roll(table, r, q)), float(q)) for q in pitches for r in rolls})


def load():
    return json.loads(ENVELOPE_PATH.read_text())


if __name__ == '__main__' and '--write' in sys.argv:
    import layout_model as m
    sweep = Sweep(m.build_parts(catalog=False, reliefs=False), m)
    table = dict(
        method='Tessellated R/P solids (0.05 mm), no relief cuts; per-pitch roll limits at 0.25° search, rounded toward zero.',
        sweep_floor_z_mm=m.SWEEP_FLOOR_Z, yaw_disc_top_z_mm=m.YAW_DISC_TOP_Z,
        clearance_to_disc_top_mm=m.SWEEP_FLOOR_Z - m.YAW_DISC_TOP_Z,
        body_top_z_mm=m.BODY_TOP_Z, yaw_disc_proud_mm=m.YAW_DISC_PROUD,
        yaw_disc=dict(radius_mm=m.YAW_DISC_R, thickness_mm=m.YAW_DISC_THICKNESS, bore_radius_mm=m.YAW_BORE_R),
        usable_travel=dict(roll_deg=list(ROLL_USABLE), pitch_deg=list(PITCH_USABLE)),
        hard_stops=dict(roll_deg=list(ROLL_STOP), pitch_deg=list(PITCH_STOP)),
        firmware_rule='Hold commanded roll inside the narrower interval of the neighbouring whole-degree pitch rows.',
        rows=solve(sweep, m.SWEEP_FLOOR_Z))
    worst_inside = (1e9, None)
    for pitch in np.arange(PITCH_STOP[0], PITCH_STOP[1] + 1e-9, 0.5):
        lo, hi = roll_interval(table, pitch)
        for roll in np.arange(lo, hi + 1e-9, 0.5):
            z = sweep.min_z(roll, pitch)
            if z < worst_inside[0]:
                worst_inside = (z, [float(roll), float(pitch)])
    fault = min((sweep.min_z(r, p), [r, p]) for r in ROLL_STOP for p in PITCH_STOP)
    table['verified_0p5deg_grid'] = dict(lowest_z_mm=round(worst_inside[0], 3), at_roll_pitch=worst_inside[1],
                                         passed=worst_inside[0] >= m.SWEEP_FLOOR_Z - 1e-6)
    table['hard_stop_fault_case'] = dict(
        lowest_z_mm=round(fault[0], 3), at_roll_pitch=fault[1],
        below_disc_top_mm=round(max(0.0, m.YAW_DISC_TOP_Z - fault[0]), 3),
        note='Per-axis hard-stop corner. When below_disc_top_mm is 0 the hard stops alone keep the head off the disc.')
    over = min((sweep.min_z(r, p), [r, p]) for r in (ROLL_STOP[0] - 1, ROLL_STOP[1] + 1) for p in (PITCH_STOP[0] - 1, PITCH_STOP[1] + 1))
    table['overtravel_1deg_case'] = dict(lowest_z_mm=round(over[0], 3), at_roll_pitch=over[1],
                                         clearance_to_disc_top_mm=round(over[0] - m.YAW_DISC_TOP_Z, 3))
    table['hard_stops_alone_keep_4mm'] = fault[0] - m.YAW_DISC_TOP_Z >= 4.0 - 1e-9
    table['pure_axis_lowest_z_mm'] = dict(
        pitch=round(min(sweep.min_z(0, p) for p in PITCH_STOP), 3),
        roll=round(min(sweep.min_z(r, 0) for r in ROLL_STOP), 3))
    ENVELOPE_PATH.write_text(json.dumps(table, indent=2) + '\n')
    print(json.dumps({k: v for k, v in table.items() if k != 'rows'}, indent=2))
    ok = table['verified_0p5deg_grid']['passed'] and table['overtravel_1deg_case']['clearance_to_disc_top_mm'] >= 2.0
    raise SystemExit(0 if ok else 1)
