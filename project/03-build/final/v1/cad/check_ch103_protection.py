"""CH-103 pack-carried fuse-card fit and removal screen (millimetres)."""

import module_checks as C


def main():
    entry, _, leaves = C.droid_tree()
    r = C.Report("check_ch103_protection")
    label = "M12_CH103_THREE_FUSE_PACK_CARRIER_POTTED_ENVELOPE"
    card = C.find(leaves, label).shape
    skip = ("M12_CH103_", "M12_BALANCE_PACK_LEAD_", "BATTERY_CELL_",
            "BATTERY_END_STRAP_", "PACK_FOAM", "PACK_STRAP")
    hits = C.clashes(card, leaves, skip=skip, min_vol=.01)
    r.check("potted_card_clear_of_fixed_parts", not hits, clashes=hits)
    b = entry.BALANCE_FUSE
    bms = C.find(leaves, "BATTERY_BMS_PCB01_PACK_PROTECTION").shape.bounding_box()
    x0, x1, y0, y1, z0, z1 = b["carrier"]
    r.check("card_lies_on_bms", x0 >= bms.min.X and x1 <= bms.max.X and y0 >= bms.min.Y
            and y1 <= bms.max.Y and z0 >= bms.max.Z, carrier=b["carrier"],
            bms=[round(v, 2) for v in (bms.min.X, bms.max.X, bms.min.Y, bms.max.Y, bms.max.Z)])
    plate = C.find(leaves, "TUB_BAY_MODULE_PLATE").shape
    gap = C.distance(card, plate)
    r.check("plate_pocket_clears_card", gap >= 0.3, clearance_mm=round(gap, 3))
    # The 2.5 mm plate over the pocket must stay solid for at least 2.0 mm.
    from build123d import Box, Location
    px0, px1, py0, py1, pz0, pz1 = b["pocket"]
    roof = Box(px1 - px0, py1 - py0, 1.95).moved(Location(((px0 + px1) / 2, (py0 + py1) / 2, pz1 + 0.975)))
    solid = C.piece_common(roof, plate) / roof.volume
    r.check("pocket_roof_at_least_2mm", solid > 0.999, solid_fraction=round(solid, 4))
    # The pack leaves downward through the bottom hatch (body_chassis_model:
    # "drops out downward"), so a pack-carried card must translate -Z with the
    # pack. Skip only parts that move with it; the tub wall/window must clear.
    moving = skip + ("BATTERY_BMS_", "W02P_", "M12_BALANCE_PACK_LEAD_")
    hit = C.sweep([(label, card)], leaves, (0, 0, -1),
                  [0.5 * i for i in range(1, 41)], skip=moving)
    r.check("carrier_drops_with_pack", hit is None, first_hit=hit, travel_mm=20,
            note="2026-11-18 review: the earlier -Y sweep skipped the cells and moved the card through the pack")
    xs = sorted((f[0] + f[1]) / 2 for f in b["fuses"])
    r.check("three_separate_tap_fuses", len(xs) == 3 and min(q - p for p, q in zip(xs, xs[1:])) >= 3.0,
            fuse_x=xs)
    r.finish()


if __name__ == "__main__":
    main()
