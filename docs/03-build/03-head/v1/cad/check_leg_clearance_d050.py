"""D-049/D-050: minimum distance from both yoke legs to every R/P part (7 x 8 A+ grid).

Writes generated/leg-clearance-d050.json (pairs below 1.5 mm). Compare with
generated/feetech-mounts-baseline.json, measured the same way on the
committed pre-D-049 head: no pair may be closer than it was there.
Run from this folder: python check_leg_clearance.py
"""
import sys, os, json
sys.path.insert(0, os.getcwd())
import layout_model as m, motion_envelope as env
from inspection_scene import posed
p = m.build_parts(catalog=False)
rolls=[m.ROLL_STOP[0],-14,-7,0,7,14,m.ROLL_STOP[1]]; pitches=[m.PITCH_STOP[0],-15,-5,5,15,25,35,m.PITCH_STOP[1]]
poses = env.grid_poses(env.load(), rolls, pitches)
out = {}
for leg in ['yaw_yoke_leg_55', 'yaw_yoke_leg_-55']:
    L = p[leg]['shape']; lb = L.bounding_box()
    for n, d in p.items():
        if d['kind'] != 'physical' or d['frame'] not in 'RP': continue
        best = None
        for r, q in poses:
            s = posed(d['shape'], d['frame'], r, q, 0); b = s.bounding_box()
            if any(tuple(b.min)[i] > tuple(lb.max)[i] + 3 or tuple(lb.min)[i] > tuple(b.max)[i] + 3 for i in range(3)): continue
            v = s.distance_to(L)
            if best is None or v < best[0]: best = (v, r, q)
        if best and best[0] < 1.5: out[f'{leg}|{n}'] = [round(best[0], 3), best[1], best[2]]
json.dump(out, open('generated/leg-clearance-d050.json', 'w'), indent=1)
for k, v in sorted(out.items(), key=lambda kv: kv[1][0]): print(f'{k:70s} {v}')
