"""Targeted checks for the harness changes in D-039 (05-harness/README.md).

The connector rows of check_layout.py, run on their own: connector reserves and
real connector bodies against the hardware, against each other, plugs inside
their reserves, the board-edge fit, and the pack disconnect slide path. It also
measures the new pack NTC break and BATBUS star splices. Run from this folder
with the text-to-cad 0.4.28 runtime (about 2 min):
python check_harness.py
Writes generated/harness-checks.json.
"""
import json

from build123d import Compound

import check_layout as CL
from check_layout import M, _boxes_meet, _vol


def leaves(shape):
    kids = getattr(shape, "children", None)
    return [leaf for kid in kids for leaf in leaves(kid)] if kids else [shape]


def by_label(shapes, label):
    return next(s for s in shapes if s.label == label)


def clash_map(parts, others, skip=lambda part, other: False):
    found = {}
    for part in parts:
        for other in others:
            if other is part or skip(part, other) or not _boxes_meet(part, other):
                continue
            volume = _vol(part & other)
            if volume > 1e-3:
                found[f"{part.label} x {other.label}"] = round(volume, 2)
    return found


CL._memoise_builders()
chassis_frame = M.chassis_frame()
chassis_static = leaves(Compound(children=[c for c in chassis_frame.children if c.label != "BALL_POD"]))
power_group = by_label(M.electronics().children, "POWER_DISTRIBUTION_BOARDS")
power_parts = leaves(power_group)
connector_others = [
    *chassis_static, *leaves(by_label(chassis_frame.children, "BALL_POD")),
    M.body_shell(), *leaves(M.body_panels()), *leaves(M.panel_mount_hardware()), *leaves(M.body_primary_frame()),
    *power_parts, *[c for c in M.electronics().children if c.label not in ("POWER_DISTRIBUTION_BOARDS", "IMU_PCB07")],
    *[c for c in M.sensors().children if c.label != "GP2Y_OPTICAL_AXIS"],
    *leaves(M.body_yaw_stage()), *M.yaw_drive_moving_parts(),
    *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R")), *leaves(M.battery_tub()),
    *leaves(M.body_audio()), *leaves(M.imu_board()), *leaves(M.rear_skid_tcrt_module()), *leaves(M.ball_transfer()),
    *leaves(M.wheel_assembly("L")), *leaves(M.wheel_assembly("R")), *leaves(M.body_chassis_mount_hardware()),
    *leaves(M.bearing_pair("L")), *leaves(M.bearing_pair("R")),
]
connector_leaves = leaves(M.connectors_and_exits())
slide_path = by_label(connector_leaves, "PACK_DISCONNECT_SERVICE_SLIDE_PATH_KEEP_OUT")
is_reserve = lambda label: "RESERVE" in label or "KEEP_OUT" in label
reserves = [p for p in connector_leaves if is_reserve(p.label) and p is not slide_path]
bodies = [p for p in connector_leaves if not is_reserve(p.label)]
R = {}

# Same rows and exemptions as check_layout.py.
R["reserve_clashes"] = clash_map(
    reserves, connector_others,
    skip=lambda part, other: part.label.startswith("C3_CARRIER_") and other.label == "C3_CARRIER_PCB10_WITH_DEVKITC",
)
R["body_clashes"] = {
    k: v for k, v in clash_map(bodies, connector_others).items()
    if not (k.startswith("PCB05_J") and k.endswith("PCB05_AUDIO_FRONT_END_PARTS_RESERVE"))
}
R["body_self_clashes"] = {}
for i, a in enumerate(bodies):
    for b in bodies[i + 1:]:
        if _boxes_meet(a, b) and _vol(a & b) > 1e-3:
            R["body_self_clashes"][f"{a.label} x {b.label}"] = round(_vol(a & b), 2)
R["reserve_self_clashes"] = {}
for i, a in enumerate(reserves):
    for b in reserves[i + 1:]:
        if _boxes_meet(a, b) and _vol(a & b) > 1e-3:
            R["reserve_self_clashes"][f"{a.label} x {b.label}"] = round(_vol(a & b), 2)
R["plugs_outside_reserve"] = {}
for plug in [p for p in bodies if "MATED_PLUG" in p.label or "MATED_PAIR" in p.label]:
    inside = max((_vol(plug & r) for r in reserves if _boxes_meet(plug, r)), default=0.0)
    if inside < 0.98 * plug.volume:
        R["plugs_outside_reserve"][plug.label] = round(1.0 - inside / plug.volume, 3)
R["edge_fit"] = {}
for name, strip in M.CONNECTOR_EDGE_STRIPS.items():
    widths = [round(M.connector_width(fam, n), 2) for _cid, fam, n, _what in strip["connectors"]]
    needed = sum(widths) + M.CONNECTOR_GAP * (len(widths) - 1)
    span = strip["span"][1] - strip["span"][0]
    R["edge_fit"][name] = {"needed_mm": round(needed, 2), "free_edge_mm": span, "margin_mm": round(span - needed, 2),
                           "connectors": {c[0]: f"{c[1]} {c[2]}p, {w} mm" for c, w in zip(strip["connectors"], widths)}}
pack_like = lambda label: label.startswith("BATTERY_") and not label.startswith("BATTERY_TUB")
R["slide_path_blockers"] = clash_map([slide_path], [o for o in connector_others if not pack_like(o.label)])

# The D-039 additions, measured.
ntc = by_label(bodies, "PACK_NTC_BREAK_JST_SM2_WIRE_TO_WIRE_MATED_PAIR").bounding_box()
window = M.TUB_SERVICE_WINDOW
R["ntc_break"] = {
    "x_mm": [round(ntc.min.X, 2), round(ntc.max.X, 2)], "z_mm": [round(ntc.min.Z, 2), round(ntc.max.Z, 2)],
    "gap_behind_to_window_x1_mm": round(ntc.min.X - window[1], 2),
    "cross_section_fits_window": (ntc.max.Y - ntc.min.Y) < (window[1] - window[0]) and (ntc.max.Z - ntc.min.Z) < (window[3] - window[2]),
}
splices = {p.label: p.bounding_box() for p in bodies if "BUTT_SPLICE" in p.label}
J31 = [p for p in bodies if p.label.startswith("J3_1_")]
R["splices"] = {k: {"x": [round(b.min.X, 2), round(b.max.X, 2)], "y": [round(b.min.Y, 2), round(b.max.Y, 2)],
                    "z": [round(b.min.Z, 2), round(b.max.Z, 2)]} for k, b in splices.items()}
R["splice_to_j3_1_mm"] = round(min(p.distance_to(J31[0]) for p in bodies if "BUTT_SPLICE" in p.label), 2) if J31 else None
R["deleted_j2_2_absent"] = not any(p.label.startswith("J2_2_") for p in bodies)

ok = {
    "connector_reserves_clear_of_real_hardware": not R["reserve_clashes"],
    "connector_bodies_clear_of_hardware_and_each_other": not R["body_clashes"] and not R["body_self_clashes"],
    "connector_reserves_do_not_overlap_each_other": not R["reserve_self_clashes"],
    "mated_plugs_sit_inside_their_reserves": not R["plugs_outside_reserve"],
    "edge_power_connectors_fit_free_board_edges": all(v["margin_mm"] >= 0.0 for v in R["edge_fit"].values()),
    "pack_disconnect_slide_path_clear": not R["slide_path_blockers"],
    "ntc_break_passes_tub_window": R["ntc_break"]["cross_section_fits_window"],
    "j2_2_deleted": R["deleted_j2_2_absent"],
}
R["pass"] = ok
(M.Path(__file__).resolve().parent / "generated" / "harness-checks.json").write_text(json.dumps(R, indent=1) + "\n")
print(json.dumps(R, indent=1))
print("ALL PASS" if all(ok.values()) else "FAIL: " + ", ".join(k for k, v in ok.items() if not v))
