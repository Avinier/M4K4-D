"""Export the D-049 pitch frame and +Y yoke leg plus the datums the FEA needs.

argv: out prefix. Run from the cad folder's parent: python fea/export_parts.py /tmp/x
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import layout_model as m
import feetech as fe
from build123d import export_step
p = m.build_parts(catalog=False)
for key, name in [('frame', 'connected_pitch_frame_roll_servo_saddle'), ('leg', 'yaw_yoke_leg_55')]:
    s = p[name]['shape']
    export_step(s, f'{sys.argv[1]}_{key}.step')
meta = dict(axes=m.AXES, pitch_x=m.PITCH_X, pitch_z=m.PITCH_Z, roll_y=m.ROLL_Y, roll_z=m.ROLL_Z,
            clock_deg=fe.PITCH_CLOCK_DEG, pitch_ear_seat_y=fe.PITCH_EAR_Y[0], roll_ear_seat_x=fe.ROLL_EAR_X[1],
            case_x=fe.CASE_X, ear_x=fe.EAR_X, case_half_w=fe.CASE_HALF_W, window_clear=fe.ROLL_WINDOW_CLEAR,
            cartridge_x=fe.CARTRIDGE_X, leg_inner_y=fe.LEG_INNER_Y, horn_top_y=fe.HORN_TOP_Y,
            horn_pocket_r=fe.LEG_HORN_POCKET_R, disc_top_z=m.YAW_DISC_TOP_Z,
            frame_volume=p['connected_pitch_frame_roll_servo_saddle']['shape'].volume)
json.dump(meta, open(sys.argv[1] + '.json', 'w'), indent=1)
print(meta)
