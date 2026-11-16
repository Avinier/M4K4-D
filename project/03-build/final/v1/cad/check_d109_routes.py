"""D-109 Level 3: body route reserves clear every part; chains connect endpoint to endpoint."""

import module_checks as C
import d109_routes as R
from body_harness_endpoints import resolve

IGNORE = ("HARNESS_", "M12_BALANCE_", "C3_CARRIER_TOP_ENTRY_SIGNAL_PLUG_LAYER_RESERVE", "CHARGE_SPLICE_AND_LEADS_RESERVE",
          "YAW_JUNCTION_", "C0_LINK_ADAPTER_TOP_ENTRY_PLUG_RESERVE", "C0_LINK_ADAPTER_J91_PLUG_RESERVE")  # plug lead reserves  # rev A PCB-08 parts; rev B comes from pcb_integration (FIXED obstacles below)


def touches(a, b, pad=0.5):
    return all(a[i] <= b[i + 3] + pad and b[i] <= a[i + 3] + pad for i in range(3))


def as_bb(b):  # (x0,x1,y0,y1,z0,z1) -> (x0,y0,z0,x1,y1,z1)
    return (b[0], b[2], b[4], b[1], b[3], b[5])


def main():
    entry, _, leaves = C.droid_tree()
    ends = resolve(leaves)
    r = C.Report("check_d109_routes")
    # labels a box may touch: the endpoints of every chain that uses it
    allowed = {}
    for name, (a, boxes, b) in R.CHAINS.items():
        for bx in boxes:
            allowed.setdefault(bx, set()).update(
                ends[e]["label"] for e in (a, b) if e and ends[e]["matches"])
    for name, b in R.ROUTES.items():
        hits = [h for h in C.clashes(C.blk(b), leaves, min_vol=0.05, parts_only=False)
                if not h[0].startswith(IGNORE) and h[0] not in allowed.get(name, ())
                and not any(h[0].startswith(p) for p in ("D109_", "M9_INMP441", "J_S18", "J_BAT", "J_CHASSIS"))]
        where = []
        for lab, _ in hits[:4]:
            lf = next(l for l in leaves if l.label == lab)
            if lab == "?":
                lab = "/".join(lf.path[-3:])
            try:
                bb = C._box(C.blk(b) & lf.solid)
                where.append((lab, [round(v, 1) for v in bb]))
            except Exception:
                where.append((lab, None))
        from body_harness_endpoints import FIXED
        for fname, (fb, _, _) in FIXED.items():
            if ends[fname]["label"] in allowed.get(name, ()):
                continue
            ov = [max(b[2*i], fb[i]) < min(b[2*i+1], fb[i+3]) for i in range(3)]
            if all(ov):
                hits.append((f"PCB08_REVB_{fname}", None)); where.append((fname, list(fb)))
        r.check(f"box {name} clear", not hits, hits=hits[:6], where=where)
    for name, (a, boxes, b) in R.CHAINS.items():
        bbs = [as_bb(R.box(entry, n)) for n in boxes]
        gaps = [f"{boxes[i]}->{boxes[i+1]}" for i in range(len(bbs) - 1) if not touches(bbs[i], bbs[i + 1], 0.0)]
        start = a is None or touches(bbs[0], ends[a]["box"])
        end = touches(bbs[-1], ends[b]["box"])
        r.check(f"chain {name}", not gaps and start and end, gaps=gaps, start=start, end=end)
    r.finish()


if __name__ == "__main__":
    main()
