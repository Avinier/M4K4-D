"""Check the selected sloped shell's removable panel interfaces."""

import json
from pathlib import Path

import body_v1_model as body

HERE = Path(__file__).resolve().parent


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if (aa.max.X <= bb.min.X or bb.max.X <= aa.min.X or
        aa.max.Y <= bb.min.Y or bb.max.Y <= aa.min.Y or
        aa.max.Z <= bb.min.Z or bb.max.Z <= aa.min.Z):
        return 0.0
    return round((a & b).volume, 3)


shell = body.body_shell()
panels = body.body_panels()
front, rear = panels.children[:2]
hardware = body.panel_mount_hardware().children
frames = [part for part in hardware if "FRAME_WITH_BOSSES" in (part.label or "")]
speaker = [part for part in leaves(body.body_audio()) if (part.label or "").startswith("SPEAKER_K50WP_")]
estop = body.estop_switch()
fixed = [
    *leaves(body.body_primary_frame()),
    *(part for part in leaves(body.chassis_v1_reference())
      if not (part.label or "").startswith("ESTOP_XA1E_")),
    *(part for part in leaves(body.electronics())
      if not (part.label or "").startswith("ESTOP_XA1E_")),
]
results = {
    "panel_solids": {front.label: len(front.solids()), rear.label: len(rear.solids())},
    "panel_shell_gap_mm": {front.label: round(shell.distance(front), 3),
                           rear.label: round(shell.distance(rear), 3)},
    "panel_shell_overlap_mm3": {},
    "panel_frame_overlap_mm3": {},
    "panel_fixed_overlap_mm3": {},
    "panel_function_overlap_mm3": {},
    "panel_screw_overlap_mm3": {},
    "panel_driver_overlap_mm3": {},
}
for panel, frame, functional in ((front, frames[0], speaker), (rear, frames[1], estop)):
    for key, parts in (
        ("panel_shell_overlap_mm3", [shell]),
        ("panel_frame_overlap_mm3", [frame]),
        ("panel_fixed_overlap_mm3", fixed),
        ("panel_function_overlap_mm3", functional),
        ("panel_screw_overlap_mm3", [part for part in hardware if
            (part.label or "").startswith(panel.label.split("_")[0] + "_PANEL_M3_")]),
    ):
        for part in parts:
            value = overlap(panel, part)
            if value > 0.001:
                results[key][f"{panel.label}:{part.label}"] = value

for head in (part for part in hardware if "_PANEL_M3_HEAD_" in (part.label or "")):
    bounds = head.bounding_box()
    front_side = head.label.startswith("FRONT")
    x0, x1 = ((bounds.max.X + 0.5, bounds.max.X + 25.5) if front_side else
              (bounds.min.X - 25.5, bounds.min.X - 0.5))
    tool = body._axial_bore_x(
        2.5, x0, x1,
        (bounds.min.Y + bounds.max.Y) / 2.0,
        (bounds.min.Z + bounds.max.Z) / 2.0,
    )
    for part in [shell, *fixed]:
        value = overlap(tool, part)
        if value > 0.001:
            results["panel_driver_overlap_mm3"][f"{head.label}:{part.label}"] = value

out = HERE / "generated" / "body-panel-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
assert all(value == 1 for value in results["panel_solids"].values())
assert all(value <= 0.2 for value in results["panel_shell_gap_mm"].values()), "panel must meet shell land"
assert not any(results[key] for key in results if key.endswith("overlap_mm3")), "panel interface has clashes"
