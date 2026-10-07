"""Diagnose current-centre HS/Pi/PCB collision regions for design iteration."""
from pathlib import Path
from build123d import Axis, import_step
import body_v1_model as body

HERE = Path(__file__).resolve().parent
servo = import_step(HERE / "purchased/waveshare_feetech_st3215_hs_servo.step")
servo = servo.rotate(Axis.X, -90)
x = body.BODY_AXIS_X + body.YAW_PINION_CENTER[0]
y = body.YAW_PINION_CENTER[1]
servo = servo.translate((x, y, body.YAW_SERVO_TOP_Z-servo.bounding_box().max.Z))


def b(s):
    q = s.bounding_box()
    return tuple((round(getattr(q.min, k), 2), round(getattr(q.max, k), 2)) for k in "XYZ")


for name, target in (("PI", body.raspberry_pi5()),
                     ("SOCKET", body._block(*body.C0_GPIO_SOCKET)),
                     ("STRIP", body._block(*body.C0_LINK_ADAPTER_STRIP))):
    for i, a in enumerate(servo.solids()):
        for j, c in enumerate(target.solids()):
            if all(lo1 < hi2 and lo2 < hi1 for (lo1,hi1),(lo2,hi2) in zip(b(a),b(c))):
                hit = a & c
                if hit is not None and hit.volume > 0.01:
                    print(name, i, j, round(hit.volume,2), b(hit), "servo",b(a),"target",b(c), flush=True)
