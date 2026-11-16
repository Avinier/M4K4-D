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
    for label, pts in CH.LAST_PATHS.items():
        cad = length(pts)
        rows.append(dict(harness="chassis", label=label, cad_mm=round(cad, 1), allowance_mm=2 * TERM,
                         cut_mm_E=round(cad + 2 * TERM)))
    for label, pts, _, _ in HH.body_wire_paths(entry.HEAD_ORIGIN_IN_CHASSIS, include_neck=True):
        cad = length(pts)
        rows.append(dict(harness="head W47", label=label, cad_mm=round(cad, 1), allowance_mm=2 * TERM,
                         cut_mm_E=round(cad + 2 * TERM)))
    for name, pts in HH.lead_paths().items():
        cad = length([tuple(p) for p in pts])
        rows.append(dict(harness="head fan-out", label=f"W47_LEAD_{name}", cad_mm=round(cad, 1),
                         allowance_mm=TERM, cut_mm_E=round(cad + TERM)))
    body = json.loads((HERE / "body-harness-lengths.json").read_text())["wires"]
    for w in body:
        rows.append(dict(harness="body", label=w["label"], cad_mm=w["cad_mm"],
                         allowance_mm=round(w["cut_mm_E"] - w["cad_mm"], 1), cut_mm_E=w["cut_mm_E"]))
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
