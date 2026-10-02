"""Verify the shell joint and its top-down assembly path on chassis v1."""

import json
from pathlib import Path

from build123d import Location

import body_v1_model as body

HERE = Path(__file__).resolve().parent


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    ab, bb = a.bounding_box(), b.bounding_box()
    if (ab.max.X <= bb.min.X or bb.max.X <= ab.min.X or
        ab.max.Y <= bb.min.Y or bb.max.Y <= ab.min.Y or
        ab.max.Z <= bb.min.Z or bb.max.Z <= ab.min.Z):
        return 0.0
    return round((a & b).volume, 3)


shell = body.body_shell()
frame = leaves(body.body_primary_frame())
hardware = leaves(body.shell_frame_hardware())
chassis = leaves(body.chassis_v1_reference())
# The E-stop operator is carried by the rear service panel. It goes in with
# that panel after the shell, even though the combined review shows its final
# installed position in the chassis reference group.
chassis_at_shell_install = [
    part for part in chassis if not (part.label or "").startswith("ESTOP_XA1E_")
]
electronics = [
    part for part in leaves(body.electronics())
    if not (part.label or "").startswith("ESTOP_XA1E_")
]
results = {
    "shell_connected_solids": len(shell.solids()),
    "shell_frame_overlap_mm3": {},
    "shell_chassis_overlap_mm3": {},
    "shell_hardware_overlap_mm3": {},
    "lowering_overlap_mm3": {},
    "screw_driver_overlap_mm3": {},
}

assert len(shell.solids()) == 1, "shell must be one connected print"
assert len(hardware) == 8, "four M3 inserts and four M3 screws required"

for name, parts, key in (
    ("frame", frame, "shell_frame_overlap_mm3"),
    ("chassis", chassis, "shell_chassis_overlap_mm3"),
    ("joint", hardware, "shell_hardware_overlap_mm3"),
):
    for part in parts:
        value = overlap(shell, part)
        if value > 0.001:
            results[key][part.label or name] = value

fixed_during_lowering = [*chassis_at_shell_install, *frame, *electronics]
for dz in (0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120):
    moved = shell.moved(Location((0, 0, dz)))
    hits = {}
    for part in fixed_during_lowering:
        value = overlap(moved, part)
        if value > 0.001:
            hits[part.label or "unnamed"] = value
    if hits:
        results["lowering_overlap_mm3"][str(dz)] = hits

# A straight driver can reach each side-facing screw from outside the shell.
for x in body.SHELL_FRAME_X:
    for sign in (-1.0, 1.0):
        y0, y1 = sorted((sign * 81.8, sign * 125.0))
        tool = body._axial_bore_y(2.5, y0, y1, x, body.SHELL_FRAME_Z)
        for part in [shell, *frame, *chassis_at_shell_install]:
            value = overlap(tool, part)
            if value > 0.001:
                results["screw_driver_overlap_mm3"][f"{x},{sign}:{part.label}"] = value

out = HERE / "generated" / "shell-frame-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
assert not any(results[key] for key in (
    "shell_frame_overlap_mm3", "shell_chassis_overlap_mm3",
    "shell_hardware_overlap_mm3", "lowering_overlap_mm3",
    "screw_driver_overlap_mm3",
)), "shell/frame assembly has clashes"
