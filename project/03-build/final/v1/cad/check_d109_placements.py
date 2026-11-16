"""D-109 Level 2: the new body-harness envelopes clear printed parts, modules and each other."""

import module_checks as C
import d109_body_parts as P


def main():
    entry, _, leaves = C.droid_tree()
    new = P.parts(entry._tag)
    labels = {s.label for s in new}
    others = [lf for lf in leaves if lf.label not in labels]
    r = C.Report("check_d109_placements")
    for s in new:
        hits = C.clashes(s, others, min_vol=0.05, parts_only=False)
        hits = [h for h in hits if not h[0].startswith(("HARNESS_", "M12_BALANCE_"))]
        r.check(f"{s.label} clear", not hits, hits=hits[:8], gap=C.min_gap(s, others, reach=3.0, parts_only=False))
    r.finish()


if __name__ == "__main__":
    main()
