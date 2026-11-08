"""Check PCB-09's exported Nightly netlist against the generated circuit manifest."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402


def main():
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    exported = K.parse((HERE / "pcb-09-c0-link-adapter.net").read_text())
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
    checks = {
        "manifest_matches_export": not errors,
        "j6_pin_order": [at("J6", pin) for pin in range(1, 7)] ==
            ["+3V3_PI", "I2C_GPIO_SDA", "I2C_GPIO_SCL", "GND", "BTN_SENSE", "PWR_OFF"],
        "local_bus_header": at("J1", 36) == "I2C_GPIO_SDA" and at("J1", 37) == "I2C_GPIO_SCL",
        "button_off_header": at("J1", 32) == "BTN_GPIO12" and at("J1", 33) == "OFF_GPIO13",
        "i2c1_stays_on_test_pads": at("J1", 3) == at("TP1", 1) == "I2C1_SDA"
            and at("J1", 5) == at("TP2", 1) == "I2C1_SCL"
            and at("J6", 2) != "I2C1_SDA" and at("J6", 3) != "I2C1_SCL",
        "five_volt_sense_isolated": sorted(k for k, v in actual.items() if v == "5V_SENSE_TP_ONLY") ==
            [("J4", "10"), ("TP4", "1")],
    }
    report = dict(result="PASS" if all(checks.values()) else "FAIL",
                  exported_component_pins_checked=len(expected), checks=checks, errors=errors)
    (HERE / "netlist-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['result']}: {len(expected)} connected pins; {len(errors)} manifest mismatches")
    raise SystemExit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
