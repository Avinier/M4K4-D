"""Exact follow-up at a PCB-09-avoiding pinion angle, still only a fit screen."""
import json
import math
import sys
from pathlib import Path
from build123d import Axis, Compound, Location, import_step
import body_v1_model as body

HERE = Path(__file__).resolve().parent
servo = import_step(HERE / "purchased/waveshare_feetech_st3215_hs_servo.step")
angle = float(sys.argv[1]) if len(sys.argv) > 1 else 210.0
lift = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
radius = 2 * body.YAW_GEAR_PITCH_RADIUS
x = body.BODY_AXIS_X + radius * math.cos(math.radians(angle))
y = radius * math.sin(math.radians(angle))
part = servo.rotate(Axis.X, -90)
part = part.translate((x, y, body.YAW_SERVO_TOP_Z+lift-part.bounding_box().max.Z))


def bounds(s):
    b = s.bounding_box()
    return [(getattr(b.min, k), getattr(b.max, k)) for k in "XYZ"]


def overlaps(a, b):
    return all(a0 < b1 and b0 < a1 for (a0, a1), (b0, b1) in zip(a, b))


def volume(other):
    total = 0.0
    for a in part.solids():
        for b in other.solids():
            if overlaps(bounds(a), bounds(b)):
                common = a & b
                if common is not None:
                    total += common.volume
    return round(total, 3)


checks = {
    "BODY_PRIMARY_FRAME_CURRENT": body.body_primary_frame(),
    "PCB09_COMPLETE": body._c0_link_adapter(),
    "PI5_STEP": body.raspberry_pi5(),
}
checks["BODY_FRAME_WITHOUT_XC330_PAD"] = (checks["BODY_PRIMARY_FRAME_CURRENT"]
                                         - body._block(*body.YAW_SERVO_BRACKET))
cooler = body._purchased_step("Heatsink+fan RPi-5.STEP", "PI5_ACTIVE_COOLER_STEP",
                              [(Axis.X, 90.0)])
posts = sorted((s for s in cooler.solids() if 100.0 < s.volume < 140.0),
               key=lambda s: s.bounding_box().center().X)
post_a = posts[0].bounding_box().center()
plate_z0 = max(cooler.solids(), key=lambda s: s.volume).bounding_box().min.Z
cooler = cooler.moved(Location((body.PI_COOLER_HOLE_A[0]-post_a.X,
    body.PI_COOLER_HOLE_A[1]-post_a.Y, body.PI_SOC_TOP_Z-plate_z0)))
checks["PI5_ACTIVE_COOLER_STEP"] = Compound(children=list(cooler.solids()))

result = {"angle_deg": angle, "clock_deg": 0, "axial_lift_mm": lift,
          "pinion_xy_mm": [round(x, 3), round(y, 3)],
          "case_bounds_mm": [[round(v, 3) for v in pair] for pair in bounds(part)],
          "exact_intersections_mm3": {}}
for name, shape in checks.items():
    result["exact_intersections_mm3"][name] = volume(shape)
    print(name, result["exact_intersections_mm3"][name], flush=True)
out = HERE / f"generated/feetech-yaw-relocation-{angle:g}deg-lift{lift:g}.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {out}")
