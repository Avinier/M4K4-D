"""Check the rear-panel mushroom power button and its W40 lead (D-041).

Measures, against the body v1 model:
- the mushroom sits in the well with side clearance and clears the panel;
- the button clears PCB-02 by at least 1 mm and its contact-block keep-out by the
  0.4 mm running gap;
- the W40 lead reserves and the J2-9 plug clear every fixed body and chassis part,
  the shell, the rear panel and its frame;
- the button slides off along -X with the panel (40 mm in 4 mm steps) without
  touching the shell, the panel frame or a fixed part.
"""

import json
from pathlib import Path

from build123d import Location

import body_v1_model as body

HERE = Path(__file__).resolve().parent
TOL = 1e-3


def leaves(shape):
    children = getattr(shape, "children", None)
    return [leaf for child in children for leaf in leaves(child)] if children else [shape]


def overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if (aa.max.X <= bb.min.X or bb.max.X <= aa.min.X or
        aa.max.Y <= bb.min.Y or bb.max.Y <= aa.min.Y or
        aa.max.Z <= bb.min.Z or bb.max.Z <= aa.min.Z):
        return 0.0
    common = a & b
    return 0.0 if common is None else round(common.volume, 3)


def clashes(movers, parts):
    found = {}
    for m in movers:
        for p in parts:
            v = overlap(m, p)
            if v > TOL:
                found[f"{m.label}:{p.label}"] = v
    return found


shell = body.body_shell()
panels = body.body_panels()
rear = panels.children[1]
hardware = body.panel_mount_hardware().children
rear_frame = [p for p in hardware if (p.label or "") == "REAR_PANEL_INTERNAL_FRAME_WITH_BOSSES"]
rear_screws = [p for p in hardware if (p.label or "").startswith("REAR_PANEL_M3_")]
electronics = leaves(body.electronics())
button_all = [p for p in electronics if (p.label or "").startswith("POWER_BUTTON_MUSHROOM_")]
button = [p for p in button_all if "KEEP_OUT" not in p.label]
mushroom = next(p for p in button if p.label == "POWER_BUTTON_MUSHROOM_D29")
pcb02 = [p for p in electronics if (p.label or "").startswith("PCB02_CHARGE_AND_SYSTEM_POWER")]
connectors = leaves(body.connectors_and_exits())
leads = [p for p in connectors if (p.label or "").startswith("POWER_BUTTON_W40_LEAD_RESERVE")]
j29 = [p for p in connectors if (p.label or "") == "J2_9_GHR02_MATED_PLUG"]
fixed = [
    *leaves(body.body_primary_frame()),
    # The chassis reference still carries the old XA1E E-stop at the same place.
    *(p for p in leaves(body.chassis_v1_reference()) if not (p.label or "").startswith("ESTOP_XA1E_")),
    *(p for p in electronics if not (p.label or "").startswith("POWER_BUTTON_")),
]
others = [p for p in connectors if p not in (*leads, *j29)]

results = {
    "button_parts": sorted(p.label for p in button_all),
    "rear_panel_solids": len(rear.solids()),
    "mushroom_to_well_mm": round(mushroom.distance(rear), 2),
    "button_to_pcb02_mm": round(min(b.distance(p) for b in button for p in pcb02), 2),
    "keep_out_to_pcb02_mm": round(min(b.distance(p) for b in button_all if "KEEP_OUT" in b.label for p in pcb02), 2),
    "button_vs_rear_panel_mm3": clashes(button, [rear]),
    "button_vs_fixed_mm3": clashes(button_all, [shell, *rear_frame, *rear_screws, *fixed, *others, *j29]),
    "lead_and_j29_vs_fixed_mm3": clashes([*leads, *j29], [shell, *rear_frame, rear, *fixed, *others]),
}

# Removal: the panel and the button slide out along -X together (W40 unplugged at J2-9).
sweep = {}
for step in range(1, 11):
    dx = -4.0 * step
    moved = [p.moved(Location((dx, 0.0, 0.0))) for p in button]
    for m, src in zip(moved, button):
        m.label = src.label
    hit = clashes(moved, [shell, *rear_frame, *fixed, *others])
    if hit:
        sweep[f"{dx:+.0f}"] = hit
results["removal_sweep_clashes"] = sweep

out = HERE / "generated" / "power-button-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))

assert results["rear_panel_solids"] == 1, "rear panel must stay one print"
assert results["mushroom_to_well_mm"] >= 2.0, "mushroom needs side clearance in the well"
assert results["button_to_pcb02_mm"] >= 1.0
assert results["keep_out_to_pcb02_mm"] >= 0.4, "running-gap minimum (chassis power_boards_keep_running_gaps)"
for key in ("button_vs_rear_panel_mm3", "button_vs_fixed_mm3", "lead_and_j29_vs_fixed_mm3", "removal_sweep_clashes"):
    assert not results[key], f"{key} not clear"
print("ALL PASS")
