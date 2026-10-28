"""Export the P-frame solid plus the datums the FEA needs. argv: layout dir, out prefix."""
import sys, json
sys.path.insert(0, sys.argv[1])
import layout_model as m
from build123d import export_step, Compound
p = m.build_parts(catalog=False)
frame = p['connected_pitch_frame_roll_servo_saddle']['shape']
export_step(frame, sys.argv[2] + '.step')
meta = dict(axes=m.AXES, pitch_x=m.PITCH_X, pitch_z=m.PITCH_Z, roll_y=m.ROLL_Y, roll_z=m.ROLL_Z,
            volume=frame.volume, bbox=[list(frame.bounding_box().min), list(frame.bounding_box().max)])
json.dump(meta, open(sys.argv[2] + '.json', 'w'), indent=1)
print(meta)
