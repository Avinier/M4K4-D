"""AABB screen of STS3045M trial placements against live head parts.

This builds layout_model.py from source. AABB overlap is a conservative flag,
not a solid intersection or approved mount. The legacy XC330 reference,
adapter and saddle are intentionally listed separately as replacement work.
"""

import json
import sys
from pathlib import Path
from build123d import Axis, Location, import_step
import layout_model as head

HERE = Path(__file__).resolve().parent
servo = import_step(HERE / "purchased/sts3045m_reference.step")


def bounds(shape):
    b = shape.bounding_box()
    return [(getattr(b.min, a), getattr(b.max, a)) for a in "XYZ"]


def overlaps(a, b):
    return all(x0 < y1 and y0 < x1 for (x0, x1), (y0, y1) in zip(a, b))


placements = {
    "roll_tabs_vertical": servo.rotate(Axis.Y, 90).moved(
        Location((-112, head.ROLL_Y, head.ROLL_Z))),
    "roll_tabs_lateral": servo.rotate(Axis.Z, 90).rotate(Axis.Y, 90).moved(
        Location((-112, head.ROLL_Y, head.ROLL_Z))),
    "pitch_tabs_forward": servo.rotate(Axis.X, -90).moved(
        Location((head.PITCH_X, 16, head.PITCH_Z))),
    "pitch_tabs_rearward": servo.rotate(Axis.Z, 180).rotate(Axis.X, -90).moved(
        Location((head.PITCH_X, 16, head.PITCH_Z))),
}
print("building live head geometry", flush=True)
parts = head.build_parts(catalog=False)
print(f"built {len(parts)} head entries", flush=True)
all_targets = {name: data["shape"] for name, data in parts.items()}
targets = {name: data["shape"] for name, data in parts.items()
           if name.startswith(("main_octagonal_skin",
                               "removable_octagonal_rear_cover",
                               "rear_pitch_trim_washer_stack_max",
                               "front_bezel_integral_camera_crown",
                               "display_module_1to1_envelope",
                               "display_connector_and_flashing_access_reserve",
                               "connected_rolling_cradle_flange_ear_stalks",
                               "pitch_trunnion_49",
                               "removable_roll_servo_saddle_strap",
                               "connected_pitch_frame_roll_servo_saddle",
                               "pitch_servo_to_yoke_adapter_trial",
                               "yaw_yoke_leg_",
                               "bearing_cartridge_trial",
                               "roll_XC330_",
                               "pitch_XC330_"))}
result = {
    "method": ("AABB screen plus exact overlap for non-legacy named parts"
               if "--exact" in sys.argv else "conservative AABB only"),
    "head_source": "layout_model.build_parts(catalog=False)",
    "target_entries": list(targets),
    "placements": {},
}
for name, shape in placements.items():
    box = bounds(shape)
    all_hits = [target for target, other in all_targets.items()
                if overlaps(box, bounds(other))]
    hits = [target for target, other in targets.items()
            if overlaps(box, bounds(other))]
    exact = []
    if "--exact" in sys.argv:
        for target in hits:
            if target.startswith(("roll_XC330_", "pitch_XC330_")):
                continue
            print(f"exact {name} / {target}", flush=True)
            volume = 0.0
            regions = []
            for servo_solid in shape.solids():
                for target_solid in targets[target].solids():
                    if not overlaps(bounds(servo_solid), bounds(target_solid)):
                        continue
                    common = servo_solid & target_solid
                    if common is not None and common.volume > 0.001:
                        volume += common.volume
                        regions.append([[round(lo, 3), round(hi, 3)]
                                        for lo, hi in bounds(common)])
            if volume > 0.001:
                exact.append({"part": target,
                              "overlap_mm3": round(volume, 3),
                              "regions_mm": regions})
    result["placements"][name] = {
        "bounds_mm": [[round(lo, 3), round(hi, 3)] for lo, hi in box],
        "aabb_hits": hits,
        "all_part_aabb_hits": all_hits,
        "exact_intersections": exact if "--exact" in sys.argv else None,
    }
    print(f"{name}: {hits}", flush=True)
out = HERE / "generated/feetech-head-fit.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {out}", flush=True)
