"""D-109: body wires vs the D-107 head-harness solids in the body (W47 run, stripped HDMI, Pi FPC).

The head harness is visible-harness geometry, not droid-tree leaves, so the
neutral body checks cannot see it. Rows: no solid overlap > 0.05 mm3 between any
body wire and any head-harness solid below Z 135 (the body side of the yaw bore),
and at least 0.5 mm nominal gap (a tied crossing; cables are E envelopes).
"""

from build123d import Compound, Location

import module_checks as C
import body_harness as H
from head_harness import build_head_harness


def leaves(node, out):
    kids = list(getattr(node, "children", []) or [])
    if not kids:
        out.append(node)
    for k in kids:
        leaves(k, out)
    return out


def main():
    entry = C.load_entry()
    head = build_head_harness(entry).children[0].moved(Location(entry.HEAD_ORIGIN_IN_CHASSIS))
    placed = lambda node: [(p[-1], C.place(n, l)) for p, n, l in C._leaves(node)]
    solids = [(n, s) for n, s in placed(Compound(children=[head])) if C._box(s)[2] < 135.0]
    body = placed(H.build_body_harness(entry))
    r = C.Report("check_body_vs_head")
    by_wire = {}
    for name, w in body:
        by_wire.setdefault(name.rsplit("_", 1)[0] if name[-2:].isdigit() else name, []).append(w)
    for wname, pieces in by_wire.items():
        w = Compound(children=pieces)
        hits = []
        for sname, s in solids:
            if C._hit(C._box(w), C._box(s)):
                v = C.common(w, s)
                if v > 0.05:
                    hits.append((sname, round(v, 3)))
        near = sorted((round(C.distance(w, s), 2), sname) for sname, s in solids if C._hit(C._box(w), C._box(s), 3.0))
        gap = near[0] if near else None
        r.check(f"{wname} vs head harness", not hits and (gap is None or gap[0] >= 0.5), hits=hits[:6], nearest=gap)
    r.finish()


if __name__ == "__main__":
    main()
