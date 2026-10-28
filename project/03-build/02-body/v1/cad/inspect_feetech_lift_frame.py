"""Locate residual lifted-servo frame overlaps after deleting the XC330 pad."""
from pathlib import Path
from build123d import Axis, import_step
import body_v1_model as body

servo = import_step(Path(__file__).parent / "purchased/waveshare_feetech_st3215_hs_servo.step")
servo = servo.rotate(Axis.X, -90)
servo = servo.translate((body.BODY_AXIS_X + body.YAW_PINION_CENTER[0],
    body.YAW_PINION_CENTER[1], body.YAW_SERVO_TOP_Z + 15-servo.bounding_box().max.Z))
frame = body.body_primary_frame() - body._block(*body.YAW_SERVO_BRACKET)
for i, s in enumerate(servo.solids()):
    for j, f in enumerate(frame.solids()):
        hit = s & f
        if hit is not None and hit.volume > 0.001:
            print(i, j, round(hit.volume,3), hit.bounding_box(),
                  "servo",s.bounding_box(), flush=True)
