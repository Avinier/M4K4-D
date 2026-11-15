"""Reproducible CH-103 envelope screen at the D-095 pack exit.

The Ø4 x 12 mm body includes an assumed insulated sleeve/joint allowance (E).
It is not the bare 0251001 fuse drawing or a full search of the pack interior.
The study deliberately keeps the existing J-PK, PA and printed geometry fixed.
"""

import json
from pathlib import Path

from build123d import Cylinder, Location

import module_checks as C


ENVELOPE_DIAMETER = 4.0
ENVELOPE_LENGTH = 12.0
ROWS = (
    ("cell_side_low", "X", [(34, 31.5, 43), (46, 31.5, 43), (58, 31.5, 43)]),
    ("cell_side_high", "X", [(34, 31.5, 46), (46, 31.5, 46), (58, 31.5, 46)]),
    ("exit_beside_jpk", "Y", [(33, 40, 44), (40, 40, 44), (47, 40, 44)]),
    ("exit_above_jpk", "Y", [(33, 38, 48), (40, 38, 48), (47, 38, 48)]),
)


def main():
    _, _, leaves = C.droid_tree()
    rows = []
    for name, axis, positions in ROWS:
        results = []
        for xyz in positions:
            fuse = Cylinder(ENVELOPE_DIAMETER / 2, ENVELOPE_LENGTH,
                            rotation=(0, 90, 0) if axis == "X" else (90, 0, 0))
            fuse = fuse.moved(Location(xyz))
            hits = C.clashes(fuse, leaves, min_vol=0.05)
            results.append({"centre_mm": xyz, "clashes_mm3": hits})
        rows.append({"name": name, "axis": axis, "taps": results,
                     "all_clear": all(not tap["clashes_mm3"] for tap in results)})
    result = {
        "study": "CH-103 balance-tap fuse envelope screen",
        "assumption": "three insulated cylindrical envelopes, diameter 4 mm, length 12 mm (E)",
        "scope": "four candidate three-fuse rows at D-095 pack exit; fixed current geometry",
        "rows": rows,
        "clear_rows": [row["name"] for row in rows if row["all_clear"]],
    }
    path = Path(__file__).with_name("study_ch103_fuse_fit-report.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{len(result['clear_rows'])}/{len(rows)} candidate three-fuse rows clear; {path.name}")


if __name__ == "__main__":
    main()
