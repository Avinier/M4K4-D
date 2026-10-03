"""Check the rear-panel charge inlet (PCB-13, D-040).

Measures, against the body v1 model:
- the pocket floor sits inside the sloped panel skin everywhere round the pocket;
- the GCT USB4140 mouth is flush with the pocket floor;
- a USB Type-C maximum overmold (12.35 x 6.5 mm, sharp corners) enters the pocket
  and its 30 mm corridor clears the panel, shell and every fixed part;
- PCB-13 seats on the printed pad, the receptacle passes the panel, and the M2
  thread-forming screws keep their engagement and skin;
- PCB-13, the W16 lead and the PCB-02 J2-8 plug clear everything else, with at
  least 1 mm from PCB-13's parts to PCB-02;
- the rear panel's inlet pad and PCB-13 slide off along -X (40 mm in 4 mm steps)
  without touching the shell, the panel frame or a fixed part.
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
rear = body.body_panels().children[1]
hardware = body.panel_mount_hardware().children
rear_frame = [p for p in hardware if (p.label or "") == "REAR_PANEL_INTERNAL_FRAME_WITH_BOSSES"]
rear_screws = [p for p in hardware if (p.label or "").startswith("REAR_PANEL_M3_")]
electronics = leaves(body.electronics())
inlet = [p for p in electronics if (p.label or "").startswith("PCB13_")]
receptacle = next(p for p in inlet if p.label == "PCB13_GCT_USB4140_VERTICAL_RECEPTACLE")
board = next(p for p in inlet if p.label == "PCB13_CHARGE_INLET_PCB")
parts_env = next(p for p in inlet if p.label == "PCB13_STUSB4500_PFET_TVS_PARTS_ENVELOPE")
screws = [p for p in inlet if "SCREW" in p.label]
pcb02 = [p for p in electronics if (p.label or "").startswith("PCB02_CHARGE_AND_SYSTEM_POWER")]
connectors = leaves(body.connectors_and_exits())
corridor = next(p for p in connectors if p.label == "CHARGE_INLET_OUTSIDE_PLUG_CORRIDOR_KEEP_OUT")
leads = [p for p in connectors if (p.label or "").startswith("CHARGE_INLET_W16_LEAD_RESERVE")]
j28 = [p for p in connectors if (p.label or "").startswith("J2_8_") or (p.label or "") == "PCB02_PY_EDGE_CONNECTORS_J28_RESERVE"]
fixed = [
    *leaves(body.body_primary_frame()),
    *(p for p in leaves(body.chassis_v1_reference()) if not (p.label or "").startswith("ESTOP_XA1E_")),
    *(p for p in electronics if not (p.label or "").startswith(("ESTOP_XA1E_", "POWER_BUTTON_", "PCB13_"))),
]
others = [p for p in connectors if p not in (corridor, *leads, *j28)]

results = {}

# Pocket floor inside the sloped skin round the whole pocket outline.
cy, cz = body.CHARGE_INLET_CENTER_YZ
pw, ph, _ = body.CHARGE_INLET_POCKET
floor = body.CHARGE_INLET_POCKET_FLOOR_X
depths = [floor - (body._shell_end_x("REAR", cz + dz) - body.SHELL_THICKNESS)
          for dz in [(-ph / 2.0) + i * ph / 40.0 for i in range(41)]]
results["pocket_depth_min_max_mm"] = [round(min(depths), 3), round(max(depths), 3)]
results["rear_panel_solids"] = len(rear.solids())

rb = receptacle.bounding_box()
results["mouth_to_pocket_floor_mm"] = round(rb.min.X - floor, 3)
results["receptacle_yz_mm"] = [round(rb.max.Y - rb.min.Y, 2), round(rb.max.Z - rb.min.Z, 2)]
results["board_to_pad_gap_mm"] = round(board.distance(rear), 3)
results["receptacle_to_panel_clearance_mm"] = round(receptacle.distance(rear), 3)
# Side clearance: the panel in a slab above the pocket floor (the floor itself is
# the overmold's stop), against the maximum-overmold corridor.
slab = body._block(floor - 0.55, floor - 0.1, -40.0, 40.0, 40.0, 90.0)
results["overmold_to_pocket_wall_mm"] = round(corridor.distance(rear & slab), 3)
results["pcb13_parts_to_pcb02_mm"] = round(min(parts_env.distance(p) for p in pcb02), 3)
results["pcb13_screw_heads_to_pcb02_mm"] = round(min(s.distance(p) for s in screws for p in pcb02), 3)

# Screws: engagement in the pad and print left beyond each pilot.
seat = body.CHARGE_INLET_BOARD_SEAT_X
length, _, _, _ = body.PCB13_SCREW
engagement = length - body.PCB_THICKNESS
results["screw_engagement_mm"] = round(engagement, 2)
results["skin_beyond_pilot_mm"] = {
    f"Y{y:+.0f}": round((seat - body.PCB13_PILOT_DEPTH) - (body._shell_end_x("REAR", z) - body.SHELL_THICKNESS), 2)
    for y, z in body.PCB13_SCREW_YZ
}

# Interferences.
results["inlet_vs_rear_panel_mm3"] = clashes(inlet, [rear])
results["corridor_vs_parts_mm3"] = clashes([corridor], [rear, shell, *rear_frame, *rear_screws, *fixed])
results["inlet_vs_fixed_mm3"] = clashes(inlet, [shell, *rear_frame, *fixed, *others, *leads, *j28])
results["lead_and_j28_vs_fixed_mm3"] = clashes([*leads, *j28], [shell, *rear_frame, rear, *fixed, *others])

# Removal: the panel and PCB-13 slide out along -X together (W16 unplugged at J2-8).
pad, cuts = body.rear_panel_charge_inlet()
pad = pad - cuts
pad.label = "REAR_PANEL_CHARGE_INLET_PAD"
sliders = [*inlet, pad]
sweep = {}
for step in range(1, 11):
    dx = -4.0 * step
    moved = [p.moved(Location((dx, 0.0, 0.0))) for p in sliders]
    for m, src in zip(moved, sliders):
        m.label = src.label
    hit = clashes(moved, [shell, *rear_frame, *fixed, *others])
    if hit:
        sweep[f"{dx:+.0f}"] = hit
results["removal_sweep_clashes"] = sweep

out = HERE / "generated" / "charge-inlet-fit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))

assert results["rear_panel_solids"] == 1, "rear panel must stay one print"
assert results["pocket_depth_min_max_mm"][0] >= 0.5, "pocket floor must stay inside the skin"
assert abs(results["mouth_to_pocket_floor_mm"]) <= 0.05, "receptacle mouth must be flush with the pocket floor"
assert results["board_to_pad_gap_mm"] <= 0.01, "PCB-13 must seat on the pad"
assert results["receptacle_to_panel_clearance_mm"] >= 0.2
assert results["overmold_to_pocket_wall_mm"] >= 0.3, "maximum overmold must enter the pocket"
assert results["pcb13_parts_to_pcb02_mm"] >= 1.0
assert results["screw_engagement_mm"] >= 3.0
assert min(results["skin_beyond_pilot_mm"].values()) >= 1.0
for key in ("inlet_vs_rear_panel_mm3", "corridor_vs_parts_mm3", "inlet_vs_fixed_mm3",
            "lead_and_j28_vs_fixed_mm3", "removal_sweep_clashes"):
    assert not results[key], f"{key} not clear"
print("ALL PASS")
