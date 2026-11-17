"""One cut list for the chassis, head (W47) and body harnesses, from CAD centrelines.

Cut = centreline + 2 x 15 mm terminations (+ the body's slack/service allowances, already
in body-harness-lengths.json). Chassis wires use the visible-wire centrelines of
chassis_harness.py; head wires use head_harness.body_wire_paths (body port through the
neck to the head clamp) and the head fan-out leads. Splice/termination envelopes are
excluded. All E: string-route and record W lengths on the built robot.
Writes harness-cut-list.json and harness-cut-list.csv.
"""

import csv
import json
import math
from pathlib import Path

import module_checks as C
import chassis_harness as CH
import head_harness as HH

HERE = Path(__file__).resolve().parent
TERM = 15.0


def length(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def main():
    entry = C.load_entry()
    rows = []
    CH.build_chassis_harness(entry)
    # Wires whose CAD centreline stops short (pack-side ends and the unplaced HN-006 fan-out are not
    # modelled): cut = max(CAD + terminations, 05-harness §4.1 E allowance), flagged partial.
    PARTIAL = {"W01_": 120, "W02P_": 110, "W06_": 90, "W07_": 90, "W05t_": 110}
    for label, pts in CH.LAST_PATHS.items():
        cad = length(pts)
        floor = next((v for k, v in PARTIAL.items() if label.startswith(k)), 0)
        rows.append(dict(harness="chassis", label=label, cad_mm=round(cad, 1), allowance_mm=2 * TERM,
                         cut_mm_E=round(max(cad + 2 * TERM, floor)), partial=bool(floor)))
    # W47: one continuous conductor from PCB-08 through the neck to its head termination (README §4.3);
    # its head fan-out is added here instead of being cut as a separate wire.
    leads = {k: length([tuple(p) for p in v]) for k, v in HH.lead_paths().items()}
    servo = leads["SERVO_ROLL"] + HH.SERVO_LOOP_LENGTH + length(HH.SERVO_P_PATH)
    dest = {"+6V3_HEAD_PR": servo, "GND_HEAD": servo, "SERVO_DATA": servo,
            "+5V_DISPLAY": leads["DISPLAY_POWER"], "GND_DISPLAY": leads["DISPLAY_POWER"],
            "STRIPPED_HDMI": leads["HEAD_CAMERA_HDMI"]}
    for label, pts, _, _ in HH.body_wire_paths(entry.HEAD_ORIGIN_IN_CHASSIS, include_neck=True):
        net = label[4:].rsplit("_AWG", 1)[0]
        fan = next((v for k, v in dest.items() if net.startswith(k)), leads["PCB12_J1"])
        cad = length(pts) + fan
        rows.append(dict(harness="head W47", label=label, cad_mm=round(cad, 1), allowance_mm=2 * TERM,
                         cut_mm_E=round(cad + 2 * TERM), partial=False))
    cad = leads["PCB12_J2_BRANCH"]
    rows.append(dict(harness="head fan-out", label="W47_LEAD_PCB12_J2_BRANCH", cad_mm=round(cad, 1),
                     allowance_mm=2 * TERM, cut_mm_E=round(cad + 2 * TERM), partial=False))
    body = json.loads((HERE / "body-harness-lengths.json").read_text())["wires"]
    for w in body:
        rows.append(dict(harness="body", label=w["label"], cad_mm=w["cad_mm"],
                         allowance_mm=round(w["cut_mm_E"] - w["cad_mm"], 1), cut_mm_E=w["cut_mm_E"], partial=False))
    totals = {}
    for r in rows:
        totals[r["harness"]] = totals.get(r["harness"], 0) + r["cut_mm_E"]
    doc = dict(note=__doc__.strip().splitlines()[0] + " All E.", totals_mm_E=totals, rows=rows)
    (HERE / "harness-cut-list.json").write_text(json.dumps(doc, indent=1) + "\n")
    with open(HERE / "harness-cut-list.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    print(len(rows), "rows", totals)


if __name__ == "__main__":
    main()
