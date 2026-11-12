"""D-106: the chassis harness routes, the body-lift plug lead exits and the print features they need.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 3 min.
Measures:
1. every harness reserve on the chassis (the D-106 routes and the older motor-pigtail, GP2Y-lead,
   balance-lead and charge-splice reserves) clear of every part, and the D-106 routes outside every
   non-harness reserve or keep-out (speaker cavity, plug corridors, PCB plug layers);
2. each route chain continuous (consecutive boxes touch or overlap);
3. room for the leads at both ends of every body-lift plug: 8 mm (Micro-Fit+) or 6 mm (Micro-Fit 3.0)
   along X past each end face, over the housing section, clear of parts;
4. the print features: the W03a deck slot, the J10-8 tunnel, notch and bore, the fuse-holder tie
   tunnel open on their axes; each tie lug standing on its print with its tunnel open.
"""

import module_checks as C

OWN_GROUP = "D-106 chassis harness routes"
OLDER = ("MOTOR_L_PIGTAIL_RESERVE", "MOTOR_R_PIGTAIL_RESERVE", "GP2Y_J10_8_SOLDERED_LEAD_RESERVE",
         "M12_BALANCE_", "CHARGE_SPLICE_AND_LEADS_RESERVE")
HARNESS_LIKE = ("HARNESS", "PIGTAIL", "BALANCE", "LEAD_RESERVE", "CHARGE_SPLICE")
EXIT = {"MICROFIT_PLUS": 8.0, "MICROFIT3": 6.0}


def _touch(a, b, tol=0.01):
    return all(a[i] <= b[i + 3] + tol and b[i] <= a[i + 3] + tol for i in range(3))


def main():
    entry, tree, leaves = C.droid_tree()
    r = C.Report("check_d106_harness")
    mine = [lf for lf in leaves if OWN_GROUP in lf.path]
    older = [lf for lf in leaves if any(lf.label.startswith(o) for o in OLDER)]
    r.check("routes_present", len(mine) == len(entry.D106_ROUTES) + 1, count=len(mine))
    plugs = {lf.label: lf for lf in leaves if "D-096 body-lift plugs" in "/".join(lf.path)}

    # 1. Clear of parts. A route may touch the part it enters (plug end, holder end, pigtail) but not overlap it.
    for lf in [*mine, *older]:
        hits = C.clashes(lf.shape, leaves, min_vol=1e-3)
        if lf.label.startswith("CHARGE_SPLICE"):          # the reserve wraps its own splice
            hits = [h for h in hits if not h[0].startswith("CHARGE_SPLICE")]
        r.check(f"clear_{lf.label}", not hits, clashes=hits)
    for lf in mine:
        rsv = [h for h in C.clashes(lf.shape, leaves, parts_only=False, min_vol=1e-3)
               if not any(t in h[0] for t in HARNESS_LIKE)]
        rsv = [h for h in rsv if not C.is_part(next(x.path for x in leaves if x.label == h[0]))]
        r.check(f"outside_keepouts_{lf.label}", not rsv, reserves=rsv)

    # 2. Chains.
    box = {lf.label.replace("HARNESS_D106_", ""): lf.box for lf in mine}
    for name, chain in entry.D106_CHAINS.items():
        gaps = [f"{a}->{b}" for a, b in zip(chain, chain[1:]) if not _touch(box[a], box[b])]
        r.check(f"chain_{name}", not gaps, breaks=gaps)
    r.check("chain_W34_bore", _touch(box["NOSE_J10_8_TUNNEL"], box["NOSE_J10_8_BORE"])
            and _touch(box["NOSE_J10_8_BORE"], box["NOSE_J10_8_RISER"]))

    # 3. Lead exits at the body-lift plugs.
    for name, fam, (x0, x1, y0, y1, z0, z1) in entry.BODYLIFT["plugs"]:
        L = EXIT[fam]
        own = (f"{name}_{fam}",)
        for end, xa, xb in (("-X body", x0 - L, x0), ("+X chassis", x1, x1 + L)):
            tool = C.blk((xa, xb, y0 + 0.5, y1 - 0.5, z0 + 0.5, z1 - 0.5))
            hits = [h for h in C.clashes(tool, leaves, min_vol=1e-3) if not h[0].startswith(own)]
            r.check(f"lead_exit_{name}_{end}", not hits, length=L, clashes=hits)

    # 4. Print features.
    front = C.find(leaves, "CHASSIS_FRAME_FRONT_MODULE").shape
    plate = C.find(leaves, "TUB_BAY_MODULE_PLATE").shape

    def inside(intervals, a, b):
        return [(p, q) for p, q in intervals if q > a + 0.05 and p < b - 0.05]

    sx0, sx1, sy0, sy1, _, _ = entry.D106["pack_slot"]
    for x, y in ((sx0 + 0.3, sy0 + 0.3), ((sx0 + sx1) / 2, (sy0 + sy1) / 2), (sx1 - 0.3, sy1 - 0.3)):
        m = inside(C.ray(front, (x, y, 0.0), (0, 0, 1)), 50.0, 57.0)
        r.check(f"pack_slot_open_{x:.1f}_{y:.1f}", not m, material=m)
    tx0, tx1, ty0, ty1, tz0, tz1 = entry.D106_NOSE["tunnel"]
    xm, zm = (tx0 + tx1) / 2, (tz0 + tz1) / 2
    m = inside(C.ray(front, (xm, -40.0, zm), (0, 1, 0)), ty0 + 40.0, ty1 + 40.0)   # t = y + 40
    r.check("nose_tunnel_open_along_Y", not m, material=m)
    floor = C.ray(front, (xm, 0.0, 0.0), (0, 0, 1))
    r.check("nose_tunnel_floor_and_roof", any(p <= 32.01 and q >= tz0 - 0.01 for p, q in floor)
            and any(abs(p - tz1) < 0.01 for p, q in floor), z_material=floor)
    m = inside(C.ray(front, (80.0, 0.0, 34.5), (1, 0, 0)), xm - 80.0, 12.0)   # t = x - 80, to the front face
    r.check("nose_notch_joins_channel", not m, material=m)
    bx, by = 86.0, -31.0
    m = inside(C.ray(front, (bx, by, 0.0), (0, 0, 1)), 33.0, 56.5)
    r.check("nose_bore_open_tunnel_to_deck", not m, material=m)
    cx0, cx1, cy0, cy1, cz0, cz1 = entry.D106["column_tunnel"]
    m = inside(C.ray(front, ((cx0 + cx1) / 2, 30.0, (cz0 + cz1) / 2), (0, 1, 0)), cy0 - 30.0, cy1 - 30.0)   # t = y - 30
    r.check("fuse_column_tie_tunnel_open", not m, material=m)
    w, t = entry.D106["lug_tunnel"]
    for shape, name, lugs, z0 in ((front, "deck", entry.D106["deck_lugs"], entry.TUB_BAY["plate"][4]),
                                  (plate, "plate", entry.D106["plate_lugs"], entry.TUB_BAY["plate"][5])):
        for x0, x1, y0, y1 in lugs:
            xmid, ymid = (x0 + x1) / 2, (y0 + y1) / 2
            roof = C.ray(shape, (xmid, ymid, 0.0), (0, 0, 1))
            post = C.ray(shape, (x0 + 0.5, ymid, 0.0), (0, 0, 1))
            tunnel = inside(C.ray(shape, (xmid, ymid - 20.0, z0 + t / 2), (0, 1, 0)), 20.0 - (ymid - y0) - 0.5, 20.0 + (y1 - ymid) + 0.5)
            ok = (any(abs(q - (z0 + entry.D106["lug_h"])) < 0.02 for p, q in roof)
                  and any(p <= z0 + 0.01 and q >= z0 + entry.D106["lug_h"] - 0.01 for p, q in post) and not tunnel)
            r.check(f"lug_{name}_{xmid:+.0f}_{ymid:+.0f}", ok, roof=roof, post=post, tunnel_material=tunnel)
    r.finish()


if __name__ == "__main__":
    main()
