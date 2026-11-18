"""Check PCB-17's exported Nightly netlist and placed board against the D-116 contract."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

TAPS = (("BM", "F1", "J1", "J2", "A"), ("BMINUS", "F2", "J3", "J4", "B"), ("BPLUS", "F3", "J5", "J6", "B"))


def main():
    exported = K.parse((HERE / "pcb-17-balance-fuse-cards.net").read_text())
    actual = {(K.find(node, "ref")[1], K.find(node, "pin")[1]): K.find(net, "name")[1].lstrip("/")
              for net in K.find(exported, "nets")[1:] for node in K.find_all(net, "node")}
    pads = json.loads((HERE / "placement-readback.json").read_text())
    refs_of = lambda net: {r for (r, _), v in actual.items() if v == net}
    checks = {}
    for tap, f, jc, jo, card in TAPS:
        checks[f"{tap}_cell_pad_to_fuse_pin1"] = actual.get((jc, "1")) == actual.get((f, "1")) == f"{tap}_CELL"
        checks[f"{tap}_fuse_pin2_to_fused_pad"] = actual.get((jo, "1")) == actual.get((f, "2")) == f"{tap}_FUSED"
        checks[f"{tap}_nets_touch_only_their_card"] = refs_of(f"{tap}_CELL") == {jc, f} and refs_of(f"{tap}_FUSED") == {f, jo}
        # Pin 1 (cell side) must face the card's BMS pad end: card A y 100, card B y 110.
        y1, y2 = pads[f]["1"][1], pads[f]["2"][1]
        checks[f"{tap}_pin1_toward_bms_pad_end"] = (y1 < y2) if card == "A" else (y1 > y2)
    checks["no_cell_net_shares_a_fused_net"] = len({v for v in actual.values()}) == 6
    report = dict(result="PASS" if all(checks.values()) else "FAIL", checks=checks)
    (HERE / "netlist-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['result']}: {sum(checks.values())}/{len(checks)}")
    for k, v in checks.items():
        print(("PASS " if v else "FAIL ") + k)
    raise SystemExit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
