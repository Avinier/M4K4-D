"""D-109 Level 0: every body-harness endpoint exists in the droid tree; stale reserves are gone."""

import re

import module_checks as C
from body_harness_endpoints import resolve

STALE = (r"POWER_BUTTON_W40_LEAD_RESERVE_\d", r"PI5_POWER_PIGTAIL_DROP_RESERVE",
         r"HARNESS_HEAD_RISER_\w+")


def main():
    _, _, leaves = C.droid_tree()
    r = C.Report("check_body_endpoints")
    for name, e in resolve(leaves).items():
        r.check(f"endpoint {name}", e["box"] is not None, label=e["label"], matches=e["matches"],
                mouth=e["mouth"], direction=e["direction"], wires=e["wires"],
                box=[round(v, 2) for v in e["box"]] if e["box"] else None)
    for pattern in STALE:
        hits = [lf.label for lf in leaves if re.fullmatch(pattern, lf.label)]
        r.check(f"stale {pattern} removed", not hits, hits=hits)
    r.finish()


if __name__ == "__main__":
    main()
