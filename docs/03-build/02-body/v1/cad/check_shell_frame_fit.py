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
    common = a & b  # None when the boxes touch but the solids do not
    return 0.0 if common is None else round(common.volume, 3)


shell = body.body_shell()
frame = leaves(body.body_primary_frame())
hardware = leaves(body.shell_frame_hardware())
# Wheel-arch pods, trims and their screws are fitted to the shell on the
# bench, so they are lowered with it.
arches = [part for part in leaves(body.body_panels()) if (part.label or "").startswith("WHEEL_ARCH_")]
arch_hardware = leaves(body.wheel_arch_hardware())
# The four PCB-06 mic boards are screwed to their shell bosses on the bench
# (D-037), with their pigtails unplugged, so they are lowered with it too.
audio = body.body_audio()
mic_parts = [leaf for group in audio.children if (group.label or "").startswith("PDM_MIC_") for leaf in leaves(group)]
shell_unit = [shell, *arches, *arch_hardware, *mic_parts]
# PCB-05 sits above the Pi before the shell goes on; the mic leads plug into it after.
pcb05 = [leaf for group in audio.children if (group.label or "") == "PCB05_AUDIO_FRONT_END" for leaf in leaves(group)]
pcb05_connectors = [leaf for leaf in leaves(body.connectors_and_exits()) if (leaf.label or "").startswith("PCB05_")]
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
    "wheel_arch_print_solids": {part.label: len(part.solids()) for part in arches},
    "wheel_arch_unit_overlap_mm3": {},
    "wheel_arch_driver_overlap_mm3": {},
}

assert len(shell.solids()) == 1, "shell must be one connected print"
assert len(hardware) == 8, "four M3 inserts and four M3 screws required"
assert len(arches) == 4 and len(arch_hardware) == 12, "two pods, two trims, six screws and six inserts required"
assert len(mic_parts) == 32, "four mic boards, each with package, gasket, two screw heads, two shanks and a pigtail"
assert pcb05 and pcb05_connectors, "PCB-05 and its edge connectors must be in the lowering check"
assert all(count == 1 for count in results["wheel_arch_print_solids"].values()), "each arch print must be one solid"

for name, parts, key in (
    ("frame", frame, "shell_frame_overlap_mm3"),
    ("chassis", chassis, "shell_chassis_overlap_mm3"),
    ("joint", hardware, "shell_hardware_overlap_mm3"),
):
    for unit_part in shell_unit:
        for part in parts:
            value = overlap(unit_part, part)
            if value > 0.001:
                results[key][f"{unit_part.label}:{part.label or name}"] = value

# The pods seat on the skin, the trims on the pods, the screws pass clearance
# holes into inserts, and the mic boards land on their bosses: no two members
# of the unit may intersect.
for i, a in enumerate(shell_unit):
    for b in shell_unit[i + 1:]:
        value = overlap(a, b)
        if value > 0.001:
            results["wheel_arch_unit_overlap_mm3"][f"{a.label}:{b.label}"] = value

fixed_during_lowering = [*chassis_at_shell_install, *frame, *electronics, *pcb05, *pcb05_connectors]
for dz in (0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120):
    hits = {}
    for unit_part in shell_unit:
        moved = unit_part.moved(Location((0, 0, dz)))
        for part in fixed_during_lowering:
            value = overlap(moved, part)
            if value > 0.001:
                hits[f"{unit_part.label}:{part.label or 'unnamed'}"] = value
    if hits:
        results["lowering_overlap_mm3"][str(dz)] = hits

# Pod screws are driven from inside the loose shell on the bench: a straight
# driver from each head toward the centre line must clear the shell.
for sign in (-1.0, 1.0):
    for x, z, skin_y in body._wheel_arch_fasteners():
        head_y = skin_y - body.SHELL_THICKNESS - body.WHEEL_ARCH_SEAT_DEPTH - 1.7
        y0, y1 = sorted((sign * 10.0, sign * (head_y - 0.5)))
        tool = body._axial_bore_y(2.5, y0, y1, x, z)
        value = overlap(tool, shell)
        if value > 0.001:
            results["wheel_arch_driver_overlap_mm3"][f"{x:.1f},{z:.1f},{sign}"] = value

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
    "screw_driver_overlap_mm3", "wheel_arch_unit_overlap_mm3",
    "wheel_arch_driver_overlap_mm3",
)), "shell/frame assembly has clashes"
