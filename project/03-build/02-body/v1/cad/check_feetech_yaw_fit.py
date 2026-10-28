"""Screen ST3215-HS against the complete PCB-09 and authored yaw neighbours.

The official STEP has one invalid solid, so this is packaging evidence only.
Moving the pinion also requires new mount, stop, cassette and gear checks.
"""
import json
import math
from pathlib import Path
from build123d import Axis, Compound, Location, import_step
import body_v1_model as body

HERE = Path(__file__).resolve().parent
STEP = HERE / "purchased/waveshare_feetech_st3215_hs_servo.step"


def bounds(shape):
    bb = shape.bounding_box()
    return [[round(getattr(bb.min, k), 3), round(getattr(bb.max, k), 3)] for k in "XYZ"]


def overlaps(a, b):
    return all(a0 < b1 and b0 < a1 for (a0, a1), (b0, b1) in zip(a, b))


def intersection_volume(a, b):
    volume = 0.0
    for sa in a.solids():
        for sb in b.solids():
            if overlaps(bounds(sa), bounds(sb)):
                common = sa & sb
                if common is not None:
                    volume += common.volume
    return round(volume, 3)


def placed(servo, x, y, clock):
    part = servo.rotate(Axis.X, -90).rotate(Axis.Z, clock)
    return part.translate((x, y, body.YAW_SERVO_TOP_Z-part.bounding_box().max.Z))


servo = import_step(STEP)
frame = body.body_primary_frame()
box_specs = {
    "PCB09_GPIO_SOCKET": body.C0_GPIO_SOCKET,
    "PCB09_STRIP": body.C0_LINK_ADAPTER_STRIP,
    "PCB09_BRIDGE": body.C0_LINK_ADAPTER_BRIDGE,
    "PCB09_MAIN_BOX": body.C0_LINK_ADAPTER_BOX,
    "PCB09_TOP_PLUGS": body.C0_LINK_ADAPTER_TOP_PLUGS,
    "PCB09_SIDE_PLUG": body.C0_LINK_ADAPTER_SIDE_PLUG,
    "FAN_WEB": (*body.FAN_WEB_X, *body.FAN_WEB_Y, *body.FAN_WEB_Z),
    "C3_CARRIER_BOARD": body.C3_CARRIER_BOARD,
    "C3_GH_PLUG_LAYER": body.C3_GH_PLUG_LAYER,
}
fan_x, fan_z = body.ENCLOSURE_FAN_CENTER
box_specs["ENCLOSURE_FAN_BOX"] = (fan_x-15, fan_x+15, *body.ENCLOSURE_FAN_Y,
                                   fan_z-15, fan_z+15)
neighbours = {name: body._block(*spec) for name, spec in box_specs.items()}
neighbours["PI5_STEP"] = body.raspberry_pi5()

# Match the purchased cooler placement in body_v1_model.electronics().
cooler = body._purchased_step("Heatsink+fan RPi-5.STEP", "PI5_ACTIVE_COOLER_STEP",
                              [(Axis.X, 90.0)])
posts = sorted((s for s in cooler.solids() if 100.0 < s.volume < 140.0),
               key=lambda s: s.bounding_box().center().X)
post_a = posts[0].bounding_box().center()
plate_z0 = max(cooler.solids(), key=lambda s: s.volume).bounding_box().min.Z
cooler = cooler.moved(Location((body.PI_COOLER_HOLE_A[0]-post_a.X,
    body.PI_COOLER_HOLE_A[1]-post_a.Y, body.PI_SOC_TOP_Z-plate_z0)))
neighbours["PI5_ACTIVE_COOLER_STEP"] = Compound(children=list(cooler.solids()))

pinion_x = body.BODY_AXIS_X + body.YAW_PINION_CENTER[0]
pinion_y = body.YAW_PINION_CENTER[1]
result = {
    "method": "exact solid checks at current pinion; 30-degree polar AABB screen",
    "source_step": str(STEP.relative_to(HERE)),
    "source_topology_note": "one invalid manufacturer STEP solid; packaging only",
    "current_pinion_xy_mm": [pinion_x, pinion_y],
    "neighbour_bounds_mm": {k: bounds(v) for k, v in neighbours.items()},
    "rotations": {}, "polar_scan": [],
}

for clock in (0, 90, 180, 270):
    part = placed(servo, pinion_x, pinion_y, clock)
    volumes = {}
    for name, target in (("BODY_PRIMARY_FRAME", frame), *neighbours.items()):
        # All nonzero clockings already hit PCB-09 or the frame; their complex
        # Pi/cooler STEP intersections do not change the gate.
        if clock != 0 and name in ("PI5_STEP", "PI5_ACTIVE_COOLER_STEP"):
            continue
        if overlaps(bounds(part), bounds(target)):
            vol = intersection_volume(part, target)
            if vol > 0.001:
                volumes[name] = vol
    result["rotations"][str(clock)] = {
        "bounds_mm": bounds(part), "exact_intersections_mm3": volumes,
        "neighbour_aabb_hits": [name for name, target in neighbours.items()
                                if overlaps(bounds(part), bounds(target))],
        "pi_cooler_exact_screened": clock == 0}
    print(f"current pinion clock {clock}: {volumes}", flush=True)

radius = 2.0 * body.YAW_GEAR_PITCH_RADIUS
for angle in range(0, 360, 30):
    x = body.BODY_AXIS_X + radius * math.cos(math.radians(angle))
    y = radius * math.sin(math.radians(angle))
    clockings = {}
    for clock in (0, 90, 180, 270):
        part = placed(servo, x, y, clock)
        b = bounds(part)
        clockings[str(clock)] = {
            "bounds_mm": b,
            "neighbour_aabb_hits": [name for name, target in neighbours.items()
                                    if overlaps(b, bounds(target))],
            "current_frame_aabb_hit": overlaps(b, bounds(frame)),
        }
    result["polar_scan"].append({"angle_deg": angle,
        "pinion_xy_mm": [round(x, 3), round(y, 3)], "clockings": clockings})

output = HERE / "generated/feetech-yaw-fit.json"
output.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {output}")
