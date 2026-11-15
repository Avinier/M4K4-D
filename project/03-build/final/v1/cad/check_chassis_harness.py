"""Neutral-pose solid check for the added visible chassis signal and splice envelopes."""

import json
from pathlib import Path

import chassis_harness as H
import module_checks as C


ALLOWED_ENDPOINTS = {
    "W29": ("C3_J10_7_GHR08_MATED_PLUG",),
    "W30": ("C3_J10_3_GHR04_MATED_PLUG", "MOTOR_L_ENCODER_6PIN_CONNECTOR"),
    "W31": ("C3_J10_4_GHR04_MATED_PLUG", "MOTOR_R_ENCODER_6PIN_CONNECTOR"),
    "W32": ("C3_J10_5_GHR06_MATED_PLUG",),
    "W33": ("C3_J10_6_GHR06_MATED_PLUG",),
}


def main():
    entry, _, leaves = C.droid_tree()
    harness = H.build_chassis_harness(entry)
    groups = {g.label: list(g.children) for g in harness.children}
    signals = groups["Chassis control signals"]
    splices = [s for s in groups["Fused and switched distribution"]
               if s.label.startswith("HN006_")]
    power = [s for name in ("Fused and switched distribution", "Drive and motor",
                          "Head supply from tub") for s in groups[name]
             if not s.label.startswith("HN006_")]
    all_wires = [s for parts in groups.values() for s in parts]
    checks = []

    def check(label, hits):
        checks.append({"name": label, "pass": not hits, "unexpected": hits})

    check("34 cables and 2 splice envelopes", [] if len(all_wires) == 36
          and len(signals) == 5 and len(splices) == 2 else [len(all_wires), len(signals), len(splices)])
    for s in signals:
        stem = s.label.split("_", 1)[0]
        allowed = ALLOWED_ENDPOINTS[stem]
        hits = [hit for hit in C.clashes(s, leaves, min_vol=0.05)
                if hit[0] not in allowed]
        check(f"{stem} versus assembly", hits)
        overlaps = []
        for p in power:
            if C._hit(C._box(s), C._box(p)):
                volume = C.common(s, p)
                if volume > 0.05:
                    overlaps.append((p.label, round(volume, 4)))
        check(f"{stem} versus visible power", overlaps)
    for s in splices:
        check(f"{s.label} versus assembly", C.clashes(s, leaves, min_vol=0.05))
        overlaps = []
        for p in all_wires:
            if p is not s and C._hit(C._box(s), C._box(p)):
                volume = C.common(s, p)
                if volume > 0.05:
                    overlaps.append((p.label, round(volume, 4)))
        check(f"{s.label} versus visible wires", overlaps)
    result = {"scope": "neutral CAD pose; nominal outer cable and splice envelopes",
              "checks": checks, "passed": sum(c["pass"] for c in checks),
              "total": len(checks)}
    path = Path(__file__).with_name("check_chassis_harness-report.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['passed']}/{result['total']} checks; {path.name}")
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
