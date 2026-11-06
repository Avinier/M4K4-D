"""D-095 (D-093 R3): the balance lead and its break in the +Y pack channel.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 3 min.
Measures: the JST PA 3P mated pair clear of the channel walls, J-PK and the pack with the body-side
loop beside it; the channel's free width there; the pair sliding back to the tub window and through
it (pack out, J-PK out first); the deck hole and its walls; every lead reserve clear of real parts;
and a planted JST-XH 3P pair (9.9 mm across Y) in the same place, which must not fit with the loop.
"""

import module_checks as C

PAIR = "M12_JST_PA_3P_BALANCE_BREAK_MATED_PAIR"
OWN = ("M12_",)
PACK = ("BATTERY", "PACK_STRAP", "PACK_FOAM", "PACK_DISCONNECT", "BATTERY_TUB_BOTTOM_HATCH")
WINDOW = (26.9, 49.5, 40.0, 50.0)          # body_chassis_model TUB_SERVICE_WINDOW: x0, x1, z0, z1


def main():
    entry, tree, leaves = C.droid_tree()
    b = entry.BALANCE
    r = C.Report("check_balance_channel")
    pair = C.find(leaves, PAIR).shape
    deck = C.find(leaves, "CHASSIS_FRAME_FRONT_MODULE").shape

    # 1. Static: the pair clear of the frame, J-PK and pack by 0.3 mm.
    hits = C.clashes(pair, leaves, skip=OWN)
    gap, near = C.min_gap(pair, leaves, skip=OWN)
    r.check("pa_pair_clear_in_channel", not hits and gap >= 0.3, clashes=hits, min_gap=gap, nearest=near)
    x0, x1, y0, y1, z0, z1 = b["pair"]
    widths = []
    for x in (x0 + 1, (x0 + x1) / 2, x1 - 1):
        for z in (z0 + 0.5, (z0 + z1) / 2, z1 - 0.5):
            iv = C.ray(deck, (x, 20.0, z), (0, 1, 0))
            walls = [20.0 + t for seg in iv for t in seg]
            inner = max((w for w in walls if w <= y0 + 1e-6), default=None)
            outer = min((w for w in walls if w >= y1 - 1e-6), default=99.0)
            widths.append((round(x, 1), round(z, 1), inner, outer))
    free = min(o - i for _, _, i, o in widths if i is not None)
    r.check("channel_width_at_break", free >= (y1 - y0) + 2.0 + 0.6, free_width=free, pair_width=y1 - y0, loop_width=2.0, samples=widths)

    # 2. Pack out: J-PK and the pack are gone; the pair slides back to the window and into the tub.
    hit = C.sweep([(PAIR, pair)], leaves, (-1, 0, 0), [0.5 * k for k in range(1, 2 * int(x0 - WINDOW[0]) - 2)], skip=OWN + PACK)
    r.check("pa_pair_slides_back_to_window", hit is None, first_hit=hit, travel=x0 - WINDOW[0] - 1)
    back = C.moved(pair, (WINDOW[0] + 1.0 - x0, 0, 0))
    bb = C._box(back)
    fits = WINDOW[0] <= bb[0] and bb[3] <= WINDOW[1] and WINDOW[2] <= bb[2] and bb[5] <= WINDOW[3]
    hit2 = C.sweep([(PAIR, back)], leaves, (0, -1, 0), [0.5 * k for k in range(1, 26)], skip=OWN + PACK)
    r.check("pa_pair_passes_tub_window", fits and hit2 is None, pair_box_at_window=[round(v, 2) for v in bb], window=WINDOW, first_hit=hit2)

    # 3. Deck hole: open through, 1 mm of deck all round.
    x, y, rad = b["deck_hole"]
    open_mm3 = C.common(entry._z_cyl(rad - 0.05, 52.1, 55.9, x, y), deck)
    ring = entry._z_cyl(rad + 1.0, 52.05, 55.95, x, y) - entry._z_cyl(rad, 51, 57, x, y)
    r.check("deck_hole_open_with_walls", open_mm3 < 0.01 and C.frac_inside(ring, deck) > 0.97, material_in_hole_mm3=open_mm3, wall_fraction_1mm=C.frac_inside(ring, deck))

    # 4. Lead reserves against real parts (the plugs they end at, and each other, excluded).
    for lf in leaves:
        if "M12_BALANCE_" in lf.label and "RESERVE" in lf.label:
            hits = C.clashes(lf.shape, leaves, skip=OWN, min_vol=0.01)
            r.check(f"reserve_clear_{lf.label}", not hits, clashes=hits)

    # 5. Planted JST-XH 3P mated pair (9.9 x 5.75, E) in the PA pair's place beside the loop: must clash.
    xh = C.blk((x0, x1, y0, y0 + 9.9, z0, z0 + 5.75))
    loop = C.find(leaves, "M12_BALANCE_BODY_LEAD_RESERVE_1").shape
    xh_hits = C.clashes(xh, leaves, skip=OWN) + ([("loop", C.common(xh, loop))] if C.common(xh, loop) > 1e-4 else [])
    r.check("planted_xh_3p_does_not_fit", bool(xh_hits), clashes=xh_hits)
    r.finish()


if __name__ == "__main__":
    main()
