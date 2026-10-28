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
    common = a & b  # build123d returns None for an empty intersection
    return 0.0 if common is None else round(common.volume, 3)


shell = body.body_shell()  # includes the two internal panel frames (D-045)
panels = body.body_panels()
front, rear = panels.children[:2]
hardware = body.panel_mount_hardware().children
speaker = [part for part in leaves(body.body_audio()) if (part.label or "").startswith("SPEAKER_K50WP_")]
estop = body.power_button_mushroom()
fixed = [
    *leaves(body.body_primary_frame()),
    *(part for part in leaves(body.chassis_v1_reference())
      if not (part.label or "").startswith("ESTOP_XA1E_")),
    *(part for part in leaves(body.electronics())
      if not (part.label or "").startswith(("ESTOP_XA1E_", "POWER_BUTTON_"))),
]
results = {
    "panel_solids": {front.label: len(front.solids()), rear.label: len(rear.solids())},
    "panel_shell_gap_mm": {front.label: round(shell.distance(front), 3),
                           rear.label: round(shell.distance(rear), 3)},
    "panel_shell_overlap_mm3": {},
    "panel_fixed_overlap_mm3": {},
    "panel_function_overlap_mm3": {},
    "panel_screw_overlap_mm3": {},
    "panel_driver_overlap_mm3": {},
    "fastener_shell_overlap_mm3": {},
    "insert_press_overlap_mm3": {},
    "fastener_stack_mm": {},
}
for panel, functional in ((front, speaker), (rear, estop)):
    for key, parts in (
        ("panel_shell_overlap_mm3", [shell]),
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

# D-045: the screws and inserts sit in the shell-printed frame bosses.
for part in hardware:
    name = part.label or ""
    if "_PANEL_M3_INSERT_" in name or "_PANEL_M3_SHANK_" in name or "_PANEL_M3_HEAD_" in name:
        value = overlap(part, shell)
        if value > 0.001:
            results["fastener_shell_overlap_mm3"][name] = value

# With the panel off, a Ø6 soldering-iron tip reaches each boss face straight
# through the opening to press its insert.
for face in ("FRONT", "REAR"):
    inward = body._panel_inward(face)
    for index, (y, z) in enumerate(body._panel_fasteners(face), start=1):
        front_x, back_x = body._panel_boss_ends(face, z)
        tool = body._axial_bore_x(3.0, *sorted((front_x - inward * 0.1, front_x - inward * 30.0)), y, z)
        value = overlap(tool, shell)
        if value > 0.001:
            results["insert_press_overlap_mm3"][f"{face}_{index}"] = value
        tip_x = body._panel_head_seat_x(face, z) + inward * body.PANEL_SCREW_LENGTH
        results["fastener_stack_mm"][f"{face}_{index}"] = {
            "boss_length": round(abs(back_x - front_x), 2),
            "insert_pilot_depth": body.PANEL_INSERT_PILOT_DEPTH,
            "pilot_wall": round(body.PANEL_BOSS_RADIUS - body.FRAME_INSERT_RADIUS, 2),
            "thread_in_insert": round(min(inward * (tip_x - front_x), body.FRAME_INSERT_LENGTH), 2),
            "tip_short_of_boss_back": round(inward * (back_x - tip_x), 2),
        }

out = HERE / "generated" / "body-panel-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
assert all(value == 1 for value in results["panel_solids"].values())
assert all(value <= 0.2 for value in results["panel_shell_gap_mm"].values()), "panel must meet shell land"
assert not any(results[key] for key in results if key.endswith("overlap_mm3")), "panel interface has clashes"
for name, stack in results["fastener_stack_mm"].items():
    assert stack["boss_length"] >= stack["insert_pilot_depth"] + 0.5, f"{name}: boss too short for the insert pilot"
    assert stack["pilot_wall"] >= 1.35, f"{name}: insert pilot wall too thin"
    assert stack["thread_in_insert"] >= 3.0, f"{name}: under 3 mm of M3 thread in the insert"
    assert stack["tip_short_of_boss_back"] >= 0.0, f"{name}: screw tip passes the boss"
