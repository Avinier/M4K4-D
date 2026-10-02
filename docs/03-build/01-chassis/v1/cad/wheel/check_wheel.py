"""Measured geometry checks for the chassis v1 wheel (D-004, D-005).

Every check measures built solids (bounding boxes, boolean overlap volumes,
distances), not the constants that made them. Writes generated/checks.json
and generated/checks.md. Run from this folder with the text-to-cad runtime.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import build123d as bd

import wheel_model as W

OUT = Path(__file__).parent / "generated"
TOL = 1e-3  # mm^3 overlap treated as touching
DENSITY = {"PETG": 1.27, "TPU95A": 1.21, "STEEL": 7.9, "INSERT": 8.4}  # g/cm^3


def leaves(shape):
    kids = list(getattr(shape, "children", []) or [])
    if not kids:
        return [shape]
    return [leaf for kid in kids for leaf in leaves(kid)]


def vol(shape):
    return sum(s.volume for s in shape.solids()) if shape is not None else 0.0


def overlap(a, b):
    common = a & b
    return vol(common) if common is not None else 0.0


def radial_extent(shape):
    bb = shape.bounding_box()
    return max(abs(bb.min.X), abs(bb.max.X), abs(bb.min.Z), abs(bb.max.Z))


def density_for(label):
    for key, rho in (("PETG", "PETG"), ("TPU", "TPU95A"), ("SCREW", "STEEL"), ("INSERT", "INSERT")):  # noqa
        if key in label:
            return DENSITY[rho]
    raise KeyError(label)


def check_wheel():
    wheel = W.wheel()
    parts = {leaf.label: leaf for leaf in leaves(wheel)}
    rows = []

    def add(name, ok, value):
        rows.append({"check": name, "pass": bool(ok), "value": value})

    tyre = parts["WHEEL_TYRE_TPU95A_L"]
    rim = parts["WHEEL_RIM_PETG"]
    ring = parts["WHEEL_CLAMP_RING_PETG"]
    od = 2.0 * radial_extent(tyre)
    add("tread_od_is_84", abs(od - W.WHEEL_OD) < 0.05, {"od_mm": round(od, 3)})

    cap = parts["WHEEL_HUB_CAP_PETG"]
    body = [p for label, p in parts.items() if "SCREW" not in label and "HUB_CAP" not in label]
    ys = [p.bounding_box() for p in body]
    y0, y1 = min(b.min.Y for b in ys), max(b.max.Y for b in ys)
    add("rim_tyre_ring_within_24mm_envelope", y0 >= W.Y_IN - 1e-6 and y1 <= W.Y_OUT + 1e-6, {"y_mm": [round(y0, 3), round(y1, 3)]})
    y_all = max(p.bounding_box().max.Y for p in parts.values())
    add("hub_cap_and_heads_proud_le_4p5mm", y_all - W.Y_OUT <= 4.5, {"mm": round(y_all - W.Y_OUT, 3), "robot_width_mm": round(2 * (85 + y_all), 1), "target_mm": 205})

    ring_r = radial_extent(ring)
    add("clamp_ring_within_tread", ring_r < W.CARCASS_RADIUS, {"ring_max_r_mm": round(ring_r, 3), "carcass_r_mm": W.CARCASS_RADIUS})

    # D-007 interface: bearing-housing pocket, turning stub flange, spigot bore, wheel screws.
    keepout = W._ycyl(W.BOSS_POCKET_RADIUS, W.Y_IN - 1.0, W.BOSS_POCKET_FLOOR_Y)
    # The wheel screws and (D-033) the central cap screw run on into the steel stub,
    # which fills this pocket on the axle line; the keep-out is for the bearing housing.
    intrusion = sum(overlap(p, keepout) for label, p in parts.items() if "WHEEL_SCREW_M3X6" not in label and "CAP_SCREW" not in label)
    add("pocket_R18_clear_to_y8", intrusion < TOL, {"overlap_mm3": round(intrusion, 4), "floor_abs_y": 85 + W.BOSS_POCKET_FLOOR_Y})
    flange = W._ycyl(W.STUB_FLANGE["radius"] + 0.5, W.STUB_FLANGE["y"][0], W.STUB_FLANGE["y"][1] - 0.01)
    add("stub_flange_turns_free_in_pocket", overlap(rim, flange) < TOL, {"overlap_mm3": round(overlap(rim, flange), 4)})
    spigot = W._ycyl(W.HUB_BORE_RADIUS - 0.01, *W.STUB_SPIGOT_Y)
    add("spigot_bore_R5_open", overlap(rim, spigot) < TOL, {"overlap_mm3": round(overlap(rim, spigot), 4)})
    bore_cyl = W._ycyl(W.HUB_BORE_RADIUS, *W.HUB_Y)
    web_walls = [bore_cyl.distance_to(W._at_pcd(W._ycyl(W.WHEEL_SCREW["clear_radius"], *W.HUB_Y), W.WHEEL_SCREW["pcd_r"], a)) for a in W.WHEEL_SCREW["angles"]]
    add("spigot_bore_to_screw_hole_wall_ge_1p2mm", min(web_walls) >= 1.2, {"wall_mm": round(min(web_walls), 3), "web_mm": W.HUB_Y[1] - W.HUB_Y[0], "note": "D-007 geometry"})
    heads, tips = [], []
    for n, angle in enumerate(W.WHEEL_SCREW["angles"], start=1):
        seat = W._at_pcd(W._ring(W.WHEEL_SCREW["clear_radius"], W.WHEEL_SCREW_HEAD["radius"], W.Y_OUT - 0.5, W.Y_OUT), W.WHEEL_SCREW["pcd_r"], angle)
        heads.append(overlap(rim, seat) / seat.volume)
        tips.append(parts[f"WHEEL_SCREW_M3X6_{n}"].bounding_box().min.Y)
    add("wheel_screws_seat_on_web_and_end_at_flange_face", min(heads) > 0.99 and max(abs(t - W.STUB_FLANGE["y"][0]) for t in tips) < 1e-6,
        {"seat_fill": round(min(heads), 3), "tip_y": round(max(tips), 3), "flange_inner_face_y": W.STUB_FLANGE["y"][0]})
    # D-033: the cap is solid from its screw hole out to the recess edge over the
    # bore and wheel screws, and the central head (wider than the hole) closes the rest.
    lid = W._ring(W.CAP_SCREW["clear_radius"], W.CAP_RECESS["radius"], W.CAP_RECESS["y"][1], W.CAP_SCREW_SEAT_Y)
    add("hub_cap_covers_bore_and_screws", overlap(cap, lid) > 0.99 * lid.volume and W.CAP_SCREW["head_radius"] > W.CAP_SCREW["clear_radius"],
        {"cover": round(overlap(cap, lid) / lid.volume, 3), "recess_to_y": W.CAP_RECESS["y"][1], "head_r_mm": W.CAP_SCREW["head_radius"], "hole_r_mm": W.CAP_SCREW["clear_radius"]})

    # Spokes carry the load: a band under each spoke slot is solid full width.
    fills = []
    floor_top = W.Y_OUT - W.SPOKE_SLOT["depth"]
    for angle in W._spoke_angles():
        band = W._radial_box(W.SPOKE_WIDTH - 0.2, W.HUB_Y[0] + 0.1, floor_top - 0.1, W.HUB_AF / 2.0 + 1.0, W.INNER_RING_R[0] - 0.5, angle)
        fills.append(overlap(rim, band) / band.volume)
    under_slot = floor_top - W.HUB_Y[0]
    add("spokes_solid_under_slot_ge_2mm", min(fills) > 0.99 and under_slot >= 2.0 - 1e-6, {"min_fill": round(min(fills), 3), "floor_under_slot_in_pocket_mm": round(under_slot, 2), "spoke_depth_mm": {"in_pocket": W.HUB_Y[1] - W.HUB_Y[0], "outside": W.Y_OUT - W.FACE_Y[0]}})

    # D-033 central cap screw: ISO 7380 M3 x 10 into the stub's tapped spigot end (y 11).
    cs = parts["WHEEL_CAP_SCREW_M3X10"]
    tip = cs.bounding_box().min.Y
    spigot_tip = W.STUB_SPIGOT_Y[1]
    engagement = spigot_tip - tip
    add("cap_screw_engagement_in_stub_ge_6mm", engagement >= 6.0 and tip >= spigot_tip - W.STUB_CAP_TAP["thread"] - 1e-6,
        {"engagement_mm": round(engagement, 2), "tip_y": round(tip, 2), "thread_bottom_y": spigot_tip - W.STUB_CAP_TAP["thread"]})
    seat = W._ring(W.CAP_SCREW["clear_radius"], W.CAP_SCREW["head_radius"], W.CAP_SCREW_SEAT_Y - 0.5, W.CAP_SCREW_SEAT_Y)
    head_top = cs.bounding_box().max.Y
    add("cap_screw_head_seated_and_recessed", overlap(cap, seat) > 0.99 * seat.volume and head_top <= W.CAP_BOSS_Y[1] - 0.2,
        {"seat_fill": round(overlap(cap, seat) / seat.volume, 3), "head_below_boss_top_mm": round(W.CAP_BOSS_Y[1] - head_top, 3)})
    column = cap & W._ycyl(W.CAP_COLUMN["radius"] + 0.01, W.CAP_COLUMN["y0"] - 0.1, W.CAP_RECESS["y"][1])
    head_gap = min(column.distance_to(parts[f"WHEEL_SCREW_M3X6_{n}"]) for n in (1, 2, 3))
    spigot_gap = round(column.bounding_box().min.Y - spigot_tip, 3)
    add("cap_column_clears_wheel_screws_and_spigot", head_gap >= 0.5 and spigot_gap >= 0.5,
        {"to_wheel_screw_heads_mm": round(head_gap, 3), "above_spigot_tip_mm": spigot_gap,
         "under_head_column_mm": round(W.CAP_SCREW_SEAT_Y - W.CAP_COLUMN["y0"], 2)})
    # Clocking pegs sit in their hub holes with clearance, not bottomed, and the holes keep a wall to the hub hex.
    outside_hex = W._ycyl(20.0, W.HUB_Y[0], W.Y_OUT) - W._yprism(6, W.HUB_AF / 2.0, W.HUB_Y[0] - 1.0, W.Y_OUT + 1.0)
    pegs, walls = [], []
    for angle in W.CAP_PEG["angles"]:
        hole = W._at_pcd(W._ycyl(W.CAP_PEG["hole_radius"], W.Y_OUT - W.CAP_PEG["hole_depth"], W.Y_OUT), W.CAP_PEG["r"], angle)
        peg = cap & W._at_pcd(W._ycyl(W.CAP_PEG["radius"] + 0.01, W.Y_OUT - W.CAP_PEG["length"] - 0.1, W.Y_OUT), W.CAP_PEG["r"], angle)
        pegs.append(round(vol(peg), 3))
        walls.append(hole.distance_to(outside_hex))
    add("cap_pegs_clock_cap_in_hub_holes", all(v > 1.0 for v in pegs) and min(walls) >= 0.8
        and W.CAP_PEG["hole_radius"] > W.CAP_PEG["radius"] and W.CAP_PEG["hole_depth"] > W.CAP_PEG["length"],
        {"peg_volume_mm3": pegs, "hole_wall_to_hex_mm": round(min(walls), 3), "radial_clearance_mm": round(W.CAP_PEG["hole_radius"] - W.CAP_PEG["radius"], 3)})

    worst = 0.0
    pairs = []
    for (la, a), (lb, b) in itertools.combinations(parts.items(), 2):
        v = overlap(a, b)
        if v > TOL:
            pairs.append([la, lb, round(v, 4)])
        worst = max(worst, v)
    add("no_part_interference", not pairs, {"max_overlap_mm3": round(worst, 4), "pairs": pairs})

    floor = tyre.bounding_box().min.Z
    add("unloaded_contact_at_axle_minus_42", abs(floor + W.WHEEL_OD / 2.0) < 0.05, {"z_mm": round(floor, 3), "note": "loaded radius is a physical measurement"})

    side_band_in = W._ring(W.SEAT_RADIUS + 1.0, W.LIP_RADIUS - 0.01, W.LIP_Y[1] - 0.5, W.LIP_Y[1])
    side_band_out = W._ring(W.SEAT_RADIUS + 1.0, W.LIP_RADIUS - 0.01, W.RING_Y[0], W.RING_Y[0] + 0.5)
    add("tyre_trapped_by_inboard_lip", overlap(rim, side_band_in) > 0.99 * side_band_in.volume, {"cover": round(overlap(rim, side_band_in) / side_band_in.volume, 3)})
    add("tyre_trapped_by_clamp_ring", overlap(ring, side_band_out) > 0.99 * side_band_out.volume, {"cover": round(overlap(ring, side_band_out) / side_band_out.volume, 3)})
    turned = tyre.rotate(bd.Axis.Y, 360.0 / W.RIB_COUNT / 2.0)
    add("ribs_key_tyre_against_rotation", overlap(rim, turned) > 50.0, {"overlap_if_turned_half_pitch_mm3": round(overlap(rim, turned), 1)})

    # Tread: lug volume and the fraction of the contact line (bottom generator) that is lug.
    lugs = tyre - W._ycyl(W.CARCASS_RADIUS, W.Y_IN, W.Y_OUT)
    probes, hits = 72, 0
    for i in range(probes):
        a = i * 360.0 / probes
        line = W._radial_box(0.4, W.TYRE_Y[0], W.TYRE_Y[1], W.WHEEL_OD / 2.0 - 0.3, W.WHEEL_OD / 2.0, a)
        hits += overlap(lugs, line) > 1e-3
    add("contact_line_always_on_a_lug", hits == probes, {"probe_angles_hit": f"{hits}/{probes}", "lug_volume_mm3": round(vol(lugs), 1)})

    dists = []
    for angle in W._screw_angles():
        hole = W._at_pcd(W._ycyl(W.INSERT["hole_radius"], *W.INSERT_HOLE_Y), W.SCREW_PCD_RADIUS, angle)
        inner = W._ycyl(W.RIM_BORE_RADIUS, *W.INSERT_HOLE_Y)
        outer_skin = W._ring(W.SEAT_RADIUS, W.SEAT_RADIUS + 2.0, *W.INSERT_HOLE_Y)
        dists.append(min(hole.distance_to(inner), hole.distance_to(outer_skin)))
    add("insert_hole_wall_ge_1mm", min(dists) >= 1.0 - 1e-6, {"min_wall_mm": round(min(dists), 3)})
    screw = parts["WHEEL_RING_SCREW_M3X8_1"]
    insert = parts["WHEEL_RING_INSERT_M3_1"]
    tip = screw.bounding_box().min.Y
    add("screw_reaches_through_insert", tip <= insert.bounding_box().min.Y + 1e-6, {"screw_tip_y": round(tip, 3), "insert_y": [round(insert.bounding_box().min.Y, 3), round(insert.bounding_box().max.Y, 3)]})

    # Handedness: on the robot both tyres' chevrons must lead toward +X at the top.
    lead = {}
    for side in ("L", "R"):
        leaves_ = {p.label: p for p in W.mounted_leaves(side, 170.0, 0.0)}
        t = leaves_[f"WHEEL_{side}_TYRE_TPU95A_{side}"]
        yc = (1.0 if side == "L" else -1.0) * (85.0 + W.CHEVRON_APEX_Y)
        ye = (1.0 if side == "L" else -1.0) * (85.0 + W.TYRE_Y[1] - 1.0)
        # The chevrons overlap in projection, so isolate the one lug solid nearest the top.
        lugs_ = t - bd.Cylinder(W.CARCASS_RADIUS, 400.0, align=(bd.Align.CENTER,) * 3).rotate(bd.Axis.X, -90.0)
        top = max(lugs_.solids(), key=lambda so: so.center().Z - abs(so.center().X))

        def x_at(y):
            piece = top & bd.Box(40.0, 0.6, 10.0).moved(bd.Location((0.0, y, W.WHEEL_OD / 2.0)))
            return piece.center().X if piece is not None and vol(piece) > 1e-3 else None
        apex, edge = x_at(yc), x_at(ye)
        lead[side] = None if apex is None or edge is None else round(apex - edge, 2)
    add("both_tyres_lead_forward_when_mounted", all(v is not None and v > 1.0 for v in lead.values()), {"apex_ahead_of_edge_mm": lead, "note": "right tyre is the left mirrored"})

    mass = {label: round(vol(p) / 1000.0 * density_for(label), 2) for label, p in parts.items()}
    row = sum(v for k, v in mass.items() if "WHEEL_SCREW_M3X6" not in k)
    add("mass_estimate_g", True, {"per_wheel_g": round(sum(mass.values()), 1), "register_row_g": round(row, 1), "note": "register row excludes the D-007 wheel screws", "parts_g": mass})
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    rows = check_wheel()
    (OUT / "checks.json").write_text(json.dumps(rows, indent=2) + "\n")
    lines = ["# Wheel checks", "", "Generated by `check_wheel.py` from measured solids.", "", "| Check | Result | Value |", "|---|---|---|"]
    for r in rows:
        value = {k: v for k, v in r["value"].items() if k != "parts_g"}
        lines.append(f"| {r['check']} | {'PASS' if r['pass'] else 'FAIL'} | `{json.dumps(value)}` |")
    (OUT / "checks.md").write_text("\n".join(lines) + "\n")
    failed = [r for r in rows if not r["pass"]]
    print("\n".join(lines))
    print(f"\n{len(rows) - len(failed)}/{len(rows)} pass")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
