"""Check the body skeleton against the current, unmodified chassis v1 model."""

import importlib.util
import json
from pathlib import Path

from build123d import Location

import body_v1_model as body

HERE = Path(__file__).resolve().parent
CHASSIS_SOURCE = HERE.parents[2] / "01-chassis" / "v1" / "cad" / "body_chassis_model.py"
spec = importlib.util.spec_from_file_location("locked_chassis_v1", CHASSIS_SOURCE)
chassis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chassis)


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    ab, bb = a.bounding_box(), b.bounding_box()
    if (ab.max.X <= bb.min.X or bb.max.X <= ab.min.X or
        ab.max.Y <= bb.min.Y or bb.max.Y <= ab.min.Y or
        ab.max.Z <= bb.min.Z or bb.max.Z <= ab.min.Z):
        return 0.0
    common = a & b
    return 0.0 if common is None else round(common.volume, 4)


main, cassette = leaves(body.body_primary_frame())
chassis_parts = [part for part in leaves(chassis.build_chassis_v1()) if not (part.label or "").startswith("BODY_CHASSIS_")]
mount_hardware = leaves(body.body_chassis_mount_hardware())
joint_hardware = leaves(body.body_frame_joint_hardware())

assert body.BODY_MOUNT_POINTS == chassis.BODY_MOUNT_POINTS
assert body.BODY_LOCATING_POINTS == chassis.BODY_LOCATING_POINTS
assert body.BODY_MOUNT_PAD_Z0 == chassis.DECK_Z + 2.0
assert len(main.solids()) == len(cassette.solids()) == 1, "body prints must each be connected"

results = {
    "mount_points_mm": body.BODY_MOUNT_POINTS,
    "locating_points_mm": body.BODY_LOCATING_POINTS,
    "main_connected_solids": len(main.solids()),
    "cassette_connected_solids": len(cassette.solids()),
    "frame_chassis_overlap_mm3": {},
    "frame_mount_hardware_overlap_mm3": {},
    "vertical_lift_overlap_mm3": {},
    "cassette_slide_overlap_mm3": {},
    "tool_path_overlap_mm3": {},
    "underside_socket_overlap_mm3": {},
}

for body_part in (main, cassette):
    for part in chassis_parts:
        value = overlap(body_part, part)
        if value > 0.001:
            results["frame_chassis_overlap_mm3"][f"{body_part.label} x {part.label}"] = value

for body_part in (main, cassette):
    for part in mount_hardware + joint_hardware:
        value = overlap(body_part, part)
        if value > 0.001:
            results["frame_mount_hardware_overlap_mm3"][f"{body_part.label} x {part.label}"] = value

for dz in (0.5, 1.0, 2.0, 5.0, 8.0, 12.0):
    lifted = main.moved(Location((0, 0, dz)))
    hits = {}
    for part in chassis_parts:
        value = overlap(lifted, part)
        if value > 0.001:
            bb = (lifted & part).bounding_box()
            hits[part.label] = {"volume": value, "bounds": [round(v, 2) for v in (bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z)]}
    if hits:
        results["vertical_lift_overlap_mm3"][str(dz)] = hits

for dy in (-0.5, -1.0, -2.0, -5.0, -10.0, -20.0):
    moved = cassette.moved(Location((0, dy, 0)))
    hits = {part.label: overlap(moved, part) for part in chassis_parts}
    hits[main.label] = overlap(moved, main)
    hits = {label: value for label, value in hits.items() if value > 0.001}
    if hits:
        results["cassette_slide_overlap_mm3"][str(dy)] = hits

for index, (x, y) in enumerate(body.BODY_MOUNT_POINTS, 1):
    if (x, y) == body.BODY_CASSETTE_MOUNT:
        continue
    tool = body._z_cylinder(body.BODY_M4_TOOL_RADIUS, 62.4, body.BODY_Z_TOP + 1.0, x, y)
    value = overlap(main, tool)
    if value > 0.001:
        results["tool_path_overlap_mm3"][str(index)] = value

# The reversed fourth bolt is tightened from beneath the existing rail relief.
x, y = body.BODY_CASSETTE_MOUNT
socket = body._z_cylinder(4.8, 34.0, 49.6, x, y)
for part in chassis_parts:
    value = overlap(socket, part)
    if value > 0.001:
        results["underside_socket_overlap_mm3"][part.label] = value

out = HERE / "generated" / "body-frame-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
assert not any(results[key] for key in (
    "frame_chassis_overlap_mm3", "frame_mount_hardware_overlap_mm3",
    "vertical_lift_overlap_mm3", "cassette_slide_overlap_mm3", "tool_path_overlap_mm3",
    "underside_socket_overlap_mm3",
)), "body frame fit has clashes"
