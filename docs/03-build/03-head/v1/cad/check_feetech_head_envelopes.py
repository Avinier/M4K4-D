"""Locate the drawing-based STS3045M envelope at current pitch/roll axes.

This is a layout screen, not a head assembly collision or mounting proof.
The case datum is the output axis at the case bottom; the spline tip is Z=33.1.
"""

import json
from pathlib import Path
from build123d import Axis, Location, import_step
import layout_model as head

HERE = Path(__file__).resolve().parent
STEP = HERE / "purchased/sts3045m_reference.step"
servo = import_step(STEP)


def bounds(shape):
    bb = shape.bounding_box()
    return [[round(getattr(bb.min, k), 3),
             round(getattr(bb.max, k), 3)] for k in "XYZ"]


def record(shape, origin, axis_tip, note):
    return {"origin_mm": list(origin), "shaft_tip_mm": list(axis_tip),
            "bounds_mm": bounds(shape), "placement_note": note}


placements = {}
# Shaft points +X toward the existing roll coupling; the case extends rearward.
roll_origin = (-112.0, head.ROLL_Y, head.ROLL_Z)
roll = servo.rotate(Axis.Y, 90).moved(Location(roll_origin))
placements["roll_tabs_vertical"] = record(
    roll, roll_origin, (roll_origin[0]+33.1, roll_origin[1], roll_origin[2]),
    "shaft +X; 48.8 mm tab span approximately vertical; case rear X=-112")
# Clocking the servo 90 degrees about its own shaft puts the long mounting
# direction laterally, a useful alternative for a redesigned saddle.
roll_side = servo.rotate(Axis.Z, 90).rotate(Axis.Y, 90).moved(Location(roll_origin))
placements["roll_tabs_lateral"] = record(
    roll_side, roll_origin,
    (roll_origin[0]+33.1, roll_origin[1], roll_origin[2]),
    "shaft +X; 48.8 mm tab span approximately lateral")

# Pitch shaft points +Y toward the +Y trunnion; X clockings test the cable
# and case reach without assuming a finished horn or yoke adapter.
pitch_origin = (head.PITCH_X, 16.0, head.PITCH_Z)
pitch = servo.rotate(Axis.X, -90).moved(Location(pitch_origin))
placements["pitch_tabs_forward"] = record(
    pitch, pitch_origin,
    (pitch_origin[0], pitch_origin[1]+33.1, pitch_origin[2]),
    "shaft +Y; long tab/case reach forward (+X)")
pitch_back = servo.rotate(Axis.Z, 180).rotate(Axis.X, -90).moved(Location(pitch_origin))
placements["pitch_tabs_rearward"] = record(
    pitch_back, pitch_origin,
    (pitch_origin[0], pitch_origin[1]+33.1, pitch_origin[2]),
    "shaft +Y; long tab/case reach rearward (-X)")

result = {
    "method": "AABB placement screen from source STEP and current A0 axes",
    "source_step": str(STEP.relative_to(HERE)),
    "axes_mm": head.AXES,
    "nominal_outer_head_box_mm": [[-head.MAIN_D, 0],
                                  [-head.MAIN_W/2, head.MAIN_W/2],
                                  [0, head.MAIN_H]],
    "placements": placements,
    "limitations": ["outer head box ignores tapered shell and wall thickness",
                    "no exact servo-to-frame intersections or motion sweep",
                    "horn, spline teeth, screw/thread and cable details unmeasured"],
}
out = HERE / "generated/feetech-head-envelopes.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"output": str(out),
                  "bounds_mm": {key: value["bounds_mm"]
                                for key, value in placements.items()}}, indent=2))
