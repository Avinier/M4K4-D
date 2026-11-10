"""Check PCB-16's exported Nightly netlist against the manifest and the D-100/D-103 contracts."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

HEAD, C2, DISP = "+6V3_HEAD_PR", "+5V_C2", "+5V_DISPLAY"
POWER = (HEAD, "GND_HEAD", C2, "GND_C2", DISP, "GND_DISPLAY")


def main():
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    exported = K.parse((HERE / "pcb-16-head-junction.net").read_text())
    actual = {(K.find(node, "ref")[1], K.find(node, "pin")[1]): K.find(net, "name")[1].lstrip("/")
              for net in K.find(exported, "nets")[1:] for node in K.find_all(net, "node")}
    expected = {(ref, pin): net for ref, item in manifest.items() if not ref.startswith("#")
                for pin, net in item["pins"].items() if net}
    errors = [dict(ref=r, pin=p, expected=n, actual=actual.get((r, p))) for (r, p), n in expected.items() if actual.get((r, p)) != n]
    at = lambda ref, pin: actual.get((ref, str(pin)))
    iso = lambda v: v is None or v.startswith("unconnected")
    cond43 = {n: at("J1", 23 - n) for n in range(1, 23)}      # conductor n sits on contact 23-n
    cond42 = {n: at("J2", 23 - n) for n in range(1, 23)}
    refs_of = lambda net: {r for (r, _), v in actual.items() if v == net}
    checks = {
        "manifest_matches_export": not errors,
        "w42_conductors_match_j8_6": [cond42[n] for n in range(1, 23)] ==
            [HEAD] * 7 + ["GND_HEAD"] * 7 + [C2, C2, "GND_C2", "GND_C2", DISP, DISP, "GND_DISPLAY", "GND_DISPLAY"],
        "w43_conductors_match_j8_7": [cond43[n] for n in range(1, 10)] ==
            ["GND_SIG", "C0TX_P", "C0TX_N", "GND_SIG", "C2TX_N", "C2TX_P", "GND_SIG", "SERVO_DATA", "GND_SIG"]
            and all(iso(cond43[n]) for n in range(10, 23)),
        "w43_carries_no_power": not any(v in POWER for (r, _), v in actual.items() if r == "J1"),
        "pcb12_j1_lead_pads": [at("J4", p) for p in range(1, 6)] == ["GND_SIG", "C0TX_P", "C0TX_N", "C2TX_N", "C2TX_P"]
            and [at("J5", p) for p in (1, 2)] == [C2, "GND_C2"],
        "servo_data_pads": at("J4", 6) == at("J4", 7) == "SERVO_DATA",
        "head_power_pads": [at("J3", p) for p in (1, 2)] == [HEAD, "GND_HEAD"],
        "display_power": [at("J6", p) for p in (1, 2)] == [DISP, "GND_DISPLAY"],
        "grounds_kept_separate": refs_of("GND_HEAD") == {"J2", "J3"} and refs_of("GND_C2") == {"J2", "J5"}
            and refs_of("GND_DISPLAY") == {"J2", "J6"} and refs_of("GND_SIG") == {"J1", "J4"},
        "servo_data_hub": refs_of("SERVO_DATA") == {"J1", "J4"},
    }
    report = dict(result="PASS" if all(checks.values()) else "FAIL", exported_component_pins_checked=len(expected),
                  checks=checks, errors=errors)
    (HERE / "netlist-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['result']}: {len(expected)} connected pins; {len(errors)} manifest mismatches")
    for k, v in checks.items():
        print(("PASS " if v else "FAIL ") + k)
    raise SystemExit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
