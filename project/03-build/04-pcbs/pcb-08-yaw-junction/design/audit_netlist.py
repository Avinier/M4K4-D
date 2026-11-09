"""Check PCB-08's exported Nightly netlist against the circuit manifest and the D-100 contracts."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

HEAD, C2, DISP = "+6V0_HEAD_PR", "+5V_C2", "+5V_DISPLAY"
POWER = (HEAD, C2, DISP, "GND_HEAD", "GND_C2", "GND_DISPLAY", "+11V1_YAW")


def main():
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    exported = K.parse((HERE / "pcb-08-yaw-junction.net").read_text())
    actual = {
        (K.find(node, "ref")[1], K.find(node, "pin")[1]): K.find(net, "name")[1].lstrip("/")
        for net in K.find(exported, "nets")[1:]
        for node in K.find_all(net, "node")
    }
    expected = {
        (ref, pin): net
        for ref, item in manifest.items() if not ref.startswith("#")
        for pin, net in item["pins"].items() if net
    }
    errors = [dict(ref=ref, pin=pin, expected=net, actual=actual.get((ref, pin)))
              for (ref, pin), net in expected.items() if actual.get((ref, pin)) != net]
    at = lambda ref, pin: actual.get((ref, str(pin)))
    pins_of = lambda net: sorted(k for k, v in actual.items() if v == net)
    j3 = [at("J3", p) for p in range(1, 23)]
    j4 = [at("J4", p) for p in range(1, 23)]
    checks = {
        "manifest_matches_export": not errors,
        "j8_1_harness_order": [at("J1", p) for p in range(1, 7)] ==
            [HEAD, C2, DISP, "GND_HEAD", "GND_C2", "GND_DISPLAY"],
        "j8_6_head_7_plus_7": j3[:7] == [HEAD] * 7 and j3[7:14] == ["GND_HEAD"] * 7,
        "j8_6_c2_display_2_plus_2": j3[14:] == [C2, C2, "GND_C2", "GND_C2", DISP, DISP, "GND_DISPLAY", "GND_DISPLAY"],
        "j8_7_signal_only": not any(n in POWER for n in j4),
        "j8_7_map": j4[:9] == ["GND_SIG", "C0TX_P", "C0TX_N", "GND_SIG", "C2TX_N", "C2TX_P", "GND_SIG", "SERVO_DATA", "GND_SIG"],
        "j8_7_10_to_22_isolated": all(n is None or n.startswith("unconnected") for n in j4[9:]),
        "j8_4_w24_order": [at("J2", p) for p in range(1, 6)] == ["LINK_GND", "C0TX_P", "C0TX_N", "C2TX_N", "C2TX_P"]
            and (at("J2", 6) is None or at("J2", 6).startswith("unconnected")),
        "rs422_pairs_pass_through": all(sorted(r for r, _ in pins_of(n)) == ["J2", "J4"]
                                        for n in ("C0TX_P", "C0TX_N", "C2TX_N", "C2TX_P")),
        "link_gnd_only_through_r1": pins_of("LINK_GND") == [("J2", "1"), ("R1", "1")],
        "gnd_sig_members": {r for r, _ in pins_of("GND_SIG")} == {"J4", "J5", "J6", "R1", "TP2"},
        "j8_8_yaw_order": [at("J5", p) for p in range(1, 4)] == ["GND_SIG", "+11V1_YAW", "SERVO_DATA"],
        "yaw_rail_only_w17_to_j8_8": pins_of("+11V1_YAW") == [("J5", "2"), ("J6", "1")],
        "power_returns_separate": all({r for r, _ in pins_of(n)} <= {"J1", "J3"} for n in ("GND_HEAD", "GND_C2", "GND_DISPLAY")),
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
