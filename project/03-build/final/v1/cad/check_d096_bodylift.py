"""D-096: the four body-lift power plugs and the switched star splices in the final droid.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: every new part 0.5 mm clear of the robot's parts; no new part inside another reserve
(harness trunks, motor pigtails, balance lead, splice, keep-outs); each mated pair can be unmated
before the lift with the shell off and the tray in (05-harness §7.2): drawn 40 mm out on its slack,
or separated in place with 20 mm of hand room; the star splices sit above the rear lower cross rail.
"""

import module_checks as C

OWN = ("D-096 body-lift plugs and switched star",)
GAP = 0.5
DIRECTIONS = {"-Y": (0, -1, 0), "+Y": (0, 1, 0), "-X": (-1, 0, 0), "+X": (1, 0, 0), "+Z": (0, 0, 1)}
WITHDRAW = [2.0 * k for k in range(1, 21)]          # to 40 mm
UNMATE = [1.0 * k for k in range(1, 13)]            # 12 mm along the mating axis


def main():
    entry, tree, leaves = C.droid_tree()
    m = entry.BODYLIFT
    r = C.Report("check_d096_bodylift")
    mine = C.own(leaves, *OWN)
    r.check("parts_present", len(mine) == 2 * len(m["plugs"]) + len(m["stars"]), count=len(mine))

    # 1. Static clearance to parts, and no overlap with any other reserve.
    for lf in mine:
        hits = C.clashes(lf.shape, leaves, skip=OWN)
        gap, near = C.min_gap(lf.shape, leaves, skip=OWN)
        r.check(f"clear_{lf.label}", not hits and gap >= GAP, clashes=hits, min_gap=gap, nearest=near)
        rsv = [h for h in C.clashes(lf.shape, leaves, skip=OWN, parts_only=False) if h not in hits]
        r.check(f"outside_reserves_{lf.label}", not rsv, reserves=rsv)

    # 2. Unmating before the lift. Either the mated pair can be drawn 40 mm out on its lead slack in
    #    some direction, or it unmates in place: one half moves 12 mm along the mating axis (X) away
    #    from its mate (Micro-Fit engagement is under 10 mm) and the pair has 20 mm of hand room in
    #    some direction. The 40 mm lead slack itself is a first-build harness check (05-harness §7.2).
    for name, fam, box in m["plugs"]:
        pair = [(lf.label, lf.shape) for lf in mine if lf.label.startswith(name + "_")]
        draw = {}
        for d, v in DIRECTIONS.items():
            hit = C.sweep(pair, leaves, v, WITHDRAW, skip=OWN)
            draw[d] = 40.0 if hit is None else hit[0] - 2.0
        rec = [p for p in pair if "RECEPTACLE" in p[0]]
        plg = [p for p in pair if "PLUG_HALF" in p[0]]
        sep = {"receptacle -X": C.sweep(rec, leaves, (-1, 0, 0), UNMATE, skip=OWN) is None,
               "plug +X": C.sweep(plg, leaves, (1, 0, 0), UNMATE, skip=OWN) is None}
        drawn = any(v >= 40.0 for v in draw.values())
        in_place = any(sep.values()) and max(draw.values()) >= 20.0
        route = "draw 40 mm" if drawn else ("unmate in place" if in_place else "none")
        r.check(f"unmate_{name}", drawn or in_place, route=route, clear_draw_mm=draw, separate_12mm=sep)

    # 3. Stars above the rail (rail underside Z 61, top Z 69 at X -36..-28) and under the tray (Z 84.5).
    z_bot = m["star_z"] - m["star_r"]
    z_top = m["star_z"] + m["star_r"]
    r.check("stars_above_rail_below_tray", z_bot >= 69.3 and z_top <= 84.0, star_bottom=z_bot, star_top=z_top)
    r.finish()


if __name__ == "__main__":
    main()
