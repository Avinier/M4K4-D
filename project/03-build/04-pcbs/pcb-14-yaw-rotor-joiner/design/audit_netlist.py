"""Check PCB-14's exported Nightly netlist against the circuit manifest and the D-101 straight-through map."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402


def main():
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    exported = K.parse((HERE / "pcb-14-yaw-rotor-joiner.net").read_text())
    actual = {
        (K.find(node, "ref")[1], K.find(node, "pin")[1]): K.find(net, "name")[1].lstrip("/")
        for net in K.find(exported, "nets")[1:]
        for node in K.find_all(net, "node")
    }
    expected = {
        (ref, pin): net
        for ref, item in manifest.items()
        for pin, net in item["pins"].items() if net
    }
    errors = [dict(ref=ref, pin=pin, expected=net, actual=actual.get((ref, pin)))
              for (ref, pin), net in expected.items() if actual.get((ref, pin)) != net]
    members = {}
    for (ref, pin), net in actual.items():
        members.setdefault(net, []).append((ref, int(pin)))
    checks = {
        "manifest_matches_export": not errors,
        "two_connectors_only": {r for r, _ in actual} == {"J1", "J2"},
        "lower_contact_n_is_conductor_n": all(actual.get(("J1", str(n))) == f"FFC{n:02d}" for n in range(1, 23)),
        # Straight-through (D-101): J1 contact n lies under J2 contact 23-n on the board.
        "straight_through_n_to_23_minus_n": all(sorted(members.get(f"FFC{n:02d}", [])) == [("J1", n), ("J2", 23 - n)]
                                                for n in range(1, 23)),
        "22_nets_two_pins_each": len(members) == 22 and all(len(v) == 2 for v in members.values()),
        "no_contact_isolated": all(actual.get((r, str(p))) for r in ("J1", "J2") for p in range(1, 23)),
    }
    report = dict(result="PASS" if all(checks.values()) else "FAIL",
                  exported_component_pins_checked=len(expected), checks=checks, errors=errors)
    (HERE / "netlist-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['result']}: {len(expected)} connected pins; {len(errors)} manifest mismatches")
    for k, v in checks.items():
        print(("PASS " if v else "FAIL ") + k)
    raise SystemExit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
