"""CH-103 pack-carried fuse-card fit and removal screen (millimetres)."""

import module_checks as C


def main():
    entry, _, leaves = C.droid_tree()
    r = C.Report("check_ch103_protection")
    skip = ("M12_CH103_", "M12_BALANCE_PACK_LEAD_", "BATTERY_CELL_",
            "BATTERY_END_STRAP_", "PACK_FOAM", "PACK_STRAP")
    moving = skip + ("BATTERY_BMS_", "W02P_")
    bms = C.find(leaves, "BATTERY_BMS_PCB01_PACK_PROTECTION").shape.bounding_box()
    plate = C.find(leaves, "TUB_BAY_MODULE_PLATE").shape
    from build123d import Box, Location
    taps = []
    for spec in entry.BALANCE_FUSE["cards"]:
        n = spec["name"]
        label = f"M12_CH103_{n}_FUSE_CARD_POTTED_ENVELOPE"
        card = C.find(leaves, label).shape
        hits = C.clashes(card, leaves, skip=skip, min_vol=.01)
        r.check(f"{n}_clear_of_fixed_parts", not hits, clashes=hits)
        x0, x1, y0, y1, z0, z1 = spec["carrier"]
        r.check(f"{n}_lies_on_bms", x0 >= bms.min.X and x1 <= bms.max.X and y0 >= bms.min.Y
                and y1 <= bms.max.Y and z0 >= bms.max.Z, carrier=spec["carrier"])
        gap = C.distance(card, plate)
        r.check(f"{n}_plate_pocket_clears_card", gap >= 0.3, clearance_mm=round(gap, 3))
        px0, px1, py0, py1, pz0, pz1 = spec["pocket"]
        roof = Box(px1 - px0, py1 - py0, 1.95).moved(Location(((px0 + px1) / 2, (py0 + py1) / 2, pz1 + 0.975)))
        solid = C.piece_common(roof, plate) / roof.volume
        r.check(f"{n}_pocket_roof_at_least_2mm", solid > 0.999, solid_fraction=round(solid, 4))
        # The pack leaves downward through the bottom hatch, so a pack-carried
        # card translates -Z with it; skip only parts that move with the pack.
        hit = C.sweep([(label, card)], leaves, (0, 0, -1), [0.5 * i for i in range(1, 41)], skip=moving)
        r.check(f"{n}_drops_with_pack", hit is None, first_hit=hit, travel_mm=20)
        for tap, box in spec["fuses"]:
            cx, cy = (box[0] + box[1]) / 2, (box[2] + box[3]) / 2
            px, py = entry.BMS_PADS[tap]
            taps.append((tap, round(((cx - px) ** 2 + (cy - py) ** 2) ** .5, 1)))
    r.check("one_fuse_per_tap", sorted(t for t, _ in taps) == ["B_MINUS", "B_PLUS", "MID"], taps=taps)
    r.check("pad_to_fuse_stubs_at_most_15mm", all(d <= 15.0 for _, d in taps),
            stub_mm=dict(taps), note="straight-line pad-to-fuse distance; pads E from HW-391 photos")
    r.finish()


if __name__ == "__main__":
    main()
