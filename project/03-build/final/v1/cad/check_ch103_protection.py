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
    x0, x1, _, _, z0, z1 = b["carrier"]
    wx0, wx1, wz0, wz1 = C.find(leaves, label).shape.bounding_box().min.X, C.find(leaves, label).shape.bounding_box().max.X, 40., 50.
    r.check("carrier_fits_tub_window", x0 >= 26.9 and x1 <= 49.5 and z0 >= wz0 and z1 <= wz1,
            carrier=b["carrier"], window=(26.9, 49.5, 40., 50.))
    # The pack leaves downward through the bottom hatch (body_chassis_model:
    # "drops out downward"), so a pack-carried card must translate -Z with the
    # pack. Skip only parts that move with it; the tub wall/window must clear.
    moving = skip + ("BATTERY_BMS_", "W02P_", "M12_BALANCE_PACK_LEAD_")
    hit = C.sweep([(label, card)], leaves, (0, 0, -1),
                  [0.5 * i for i in range(1, 41)], skip=moving)
    r.check("carrier_drops_with_pack", hit is None, first_hit=hit, travel_mm=20,
            note="2026-11-18 review: the earlier -Y sweep skipped the cells and moved the card through the pack")
    r.check("three_separate_tap_fuses", len(b["fuse_z"]) == 3 and
            min(y - x for x, y in zip(b["fuse_z"], b["fuse_z"][1:])) >= 2.5,
            tap_z=b["fuse_z"])
    r.finish()


if __name__ == "__main__":
    main()
