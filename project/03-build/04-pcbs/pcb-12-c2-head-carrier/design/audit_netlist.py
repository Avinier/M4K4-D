"""Check PCB-12's exported Nightly netlist against the manifest and the D-092/D-100/D-102 contracts."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

AGREED_ZERO_PADS = {"1", "2", "3", "4", "5", "7", "8", "9", "10", "11", "12"}   # 5V GND 3V3 GPIO1/2/4/5/6, GPIO7/8/9


def main():
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    exported = K.parse((HERE / "pcb-12-c2-head-carrier.net").read_text())
    actual = {(K.find(node, "ref")[1], K.find(node, "pin")[1]): K.find(net, "name")[1].lstrip("/")
              for net in K.find(exported, "nets")[1:] for node in K.find_all(net, "node")}
    expected = {(ref, pin): net for ref, item in manifest.items() if not ref.startswith("#")
                for pin, net in item["pins"].items() if net}
    errors = [dict(ref=r, pin=p, expected=n, actual=actual.get((r, p))) for (r, p), n in expected.items() if actual.get((r, p)) != n]
    at = lambda ref, pin: actual.get((ref, str(pin)))
    pins_of = lambda net: sorted(k for k, v in actual.items() if v == net)
    refs_of = lambda net: {r for r, _ in pins_of(net)}
    isolated = lambda v: v is None or v.startswith("unconnected")
    dnp = {r for r, i in manifest.items() if i.get("dnp")}
    zero_used = {p for (r, p), v in actual.items() if r == "U1" and not isolated(v)}
    checks = {
        "manifest_matches_export": not errors,
        "j1_j9_1_order_plus_c2_power": [at("J1", p) for p in range(1, 8)] ==
            ["GND_SIG", "C0TX_P", "C0TX_N", "C2TX_N", "C2TX_P", "+5V_C2", "GND"],
        "rs422_receive_c0tx_polarity": at("U2", 8) == "C0TX_P" and at("U2", 7) == "C0TX_N",
        "rs422_drive_c2tx_polarity": at("U2", 5) == "C2TX_P" and at("U2", 6) == "C2TX_N",
        "c0tx_terminated_here_only": refs_of("C0TX_P") == {"J1", "U2", "R2"} and refs_of("C0TX_N") == {"J1", "U2", "R2"}
            and refs_of("C2TX_P") == {"J1", "U2"} and refs_of("C2TX_N") == {"J1", "U2"},
        "ground_bonds_each_one_0r": all(refs_of(n) - {f"#FLG0{k}" for k in range(1, 7)} == {c, r}
                                        for n, c, r in (("GND_SIG", "J1", "R1"), ("GND_HEAD_REF", "J2", "R7"),
                                                        ("GND_DISPLAY", "J3", "R10")))
            and all(manifest[r]["value"] == "0R" for r in ("R1", "R7", "R10")),
        "servo_data_one_pull_up_to_3v3": refs_of("SERVO_DATA") == {"J2", "U4", "R4", "R5"}
            and at("R5", 1) == "+3V3" and at("J2", 2) == "SERVO_DATA",
        "servo_direction_complementary": at("U3", 1) == at("U4", 1) == "SERVO_DIR"
            and manifest["U3"]["symbol"].endswith("1G126") and manifest["U4"]["symbol"].endswith("1G125")
            and at("R6", 2) == "GND",
        "display_half_duplex_de_re_tied": at("U5", 2) == at("U5", 3) == "DISP_DE" and at("R9", 2) == "GND"
            and not refs_of("DISP_A") - {"U5", "J3"} and [at("J3", p) for p in (1, 2, 3)] == ["GND_DISPLAY", "DISP_B", "DISP_A"],
        "zero_uses_agreed_pads_only": zero_used == AGREED_ZERO_PADS,
        "zero_power": at("U1", 1) == "+5V_C2" and at("U1", 2) == "GND" and at("U1", 3) == "+3V3",
        "no_servo_or_display_power_on_board": not any(n in actual.values() for n in ("+6V3_HEAD_PR", "+5V_DISPLAY", "GND_HEAD")),
        "logic_on_3v3": all(at(r, p) == "+3V3" for r, p in (("U2", 1), ("U3", 5), ("U4", 5), ("U5", 8))),
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
