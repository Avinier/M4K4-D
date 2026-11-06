"""D-095: the rear panel's XT30 charge port and JST-XH balance port, in place of the USB-C inlet.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: the panel stays one solid; the PCB-13 pocket, hole, relief and pilots are filled; both
openings run through with their 0.2 mm clearance and 1.2 mm walls to the pad edge; the mouths sit
just inside the sloped skin; the mating corridors outside and the port bodies inside are clear;
and the mushroom well (D-041) is unchanged against the body source.
"""

import module_checks as C

PANEL = "REAR_SERVICE_PANEL_OCTAGONAL"
OWN = ("M12_XT30", "M12_JST_XHP", "M12_BALANCE_BODY_LEAD_RESERVE_7")


def main():
    entry, tree, leaves = C.droid_tree()
    import body_v1_model as B
    r = C.Report("check_rear_panel_ports")
    panel = C.find(leaves, PANEL).shape
    r.check("panel_one_solid", len(panel.solids()) == 1, solids=len(panel.solids()))

    # 1. The old inlet cuts are solid again except where the new openings run.
    pad, cuts = B.rear_panel_charge_inlet()
    fill = pad & cuts
    for tool in entry.rear_panel_port_cuts():
        fill = fill - tool
    fv = C.volume(fill)
    r.check("pcb13_pocket_hole_relief_pilots_filled", C.frac_inside(fill, panel) > 0.999, fill_mm3=fv, filled_fraction=C.frac_inside(fill, panel))

    y0, y1, z0, z1 = B.PCB13_PAD
    seat = B.CHARGE_INLET_BOARD_SEAT_X
    for k in ("xt30", "xh"):
        p = entry.PORTS[k]
        (y, z), (w, h, length), c = p["yz"], p["body"], p["clear"]
        body = C.find(leaves, "M12_XT30U_FEMALE_CHARGE_PORT" if k == "xt30" else "M12_JST_XHP_3_BALANCE_PORT_PLUG").shape
        ov, gap = C.common(body, panel), C.distance(body, panel)
        r.check(f"{k}_opening_through_with_clearance", ov < 1e-3 and abs(gap - c) < 0.02, overlap_mm3=ov, radial_gap=gap, design=c)
        walls = dict(minus_y=(y - w / 2 - c) - y0, plus_y=y1 - (y + w / 2 + c), minus_z=(z - h / 2 - c) - z0, plus_z=z1 - (z + h / 2 + c))
        r.check(f"{k}_walls_to_pad_edge", min(walls.values()) >= 1.2, **walls)
        # A 1.2 mm ring round the opening is solid through the pad depth.
        outline = C.blk((-62.0, seat - 0.05, y - w / 2 - c - 1.2, y + w / 2 + c + 1.2, z - h / 2 - c - 1.2, z + h / 2 + c + 1.2))
        hole = C.blk((-70.0, -40.0, y - w / 2 - c, y + w / 2 + c, z - h / 2 - c, z + h / 2 + c))
        ring = outline - hole
        r.check(f"{k}_ring_solid", C.frac_inside(ring, panel) > 0.97, solid_fraction=C.frac_inside(ring, panel))
        # Mouth just inside the skin: outer face X on the port axis vs the mouth plane.
        hits = C.ray(panel, (-90.0, y + w / 2 + c + 0.6, z), (1, 0, 0))
        outer_x = -90.0 + hits[0][0] if hits else None
        mouth = entry.PORTS["face_x"] + entry.PORTS["recess"]
        r.check(f"{k}_mouth_recess", outer_x is not None and 0.2 <= mouth - outer_x <= 2.5, outer_face_x=outer_x, mouth_x=mouth)
        # Inside: the body is clear of everything but the panel; outside: the mating corridor.
        bh = C.clashes(body, leaves, skip=OWN + (PANEL,))
        bg, bn = C.min_gap(body, leaves, skip=OWN + (PANEL,))
        r.check(f"{k}_body_clear_inside", not bh and bg >= 0.3, clashes=bh, min_gap=bg, nearest=bn)
        corridor = C.find(leaves, f"M12_{k.upper()}_MATING_PLUG_CORRIDOR_KEEP_OUT").shape
        ch = C.clashes(corridor, leaves, skip=OWN)
        r.check(f"{k}_mating_corridor_clear", not ch, clashes=ch)

    # 2. The mushroom well is the body source's: panel material inside the well region unchanged.
    raw = next(p for p in B.body_panels().children if p.label == PANEL)
    zone = C.blk((-66.0, -40.0, -25.0, 25.0, 84.0, 128.0))
    a, b = C.common(raw, zone), C.common(panel, zone)
    r.check("mushroom_well_unchanged", abs(a - b) < 1e-3, source_mm3=a, droid_mm3=b)
    r.finish()


if __name__ == "__main__":
    main()
