"""Shop drawing of the roll hub collar HD-004 (D-120), for a turning quote.

Reads ../fab/HD-004_roll_hub_collar.step (export_d120_fab.py) and writes
../fab/HD-004_roll_hub_collar_drawing.pdf. Runs on cadgen 0.6.6 like stub_drawing.py:

    PYTHONPATH=~/.claude/plugins/cache/text-to-cad/cad/0.6.6/packages/cadgen/src \\
      MPLCONFIGDIR=/tmp/mpl <legacy venv python> d120_collar_drawing.py

Frame: axis Z, horn (flange) face at z 0, front end at z 12.5, set-screw holes on -Y.
Values from d120_roll_horn_hub.py (COLLAR, HORN PCD).
"""
import math
from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing

HERE = Path(__file__).resolve().parent
FLANGE_R, FLANGE_T, SHAFT_R, LENGTH, BORE_R = 10.0, 4.0, 6.0, 12.5, 3.0
SET_Z = (5.8, 9.7)                  # from the horn face (head X -72.3, -68.4 vs -78.1)
PCD_R = 7.0
M2 = (PCD_R * math.sin(math.radians(45)), -PCD_R * math.cos(math.radians(45)))


@eng_drawing(out="../fab/HD-004_roll_hub_collar_drawing.pdf")
def collar_drawing():
    part = cadgen.read_step(HERE.parent / "fab" / "HD-004_roll_hub_collar.step")
    sheet = Sheet(
        "A3", scale=2.5, title="ROLL HUB COLLAR", part_number="HD-004", material="6061-T6 OR 6082-T6 ALUMINIUM",
        revision="A", author="MAKAD", general_tolerance="ISO 2768-m",
        revisions=[("A", "2026-11-19", "FIRST ISSUE (D-120)")],
        notes=[
            "QTY 2 (1 + SPARE). DEBURR, NO PLATING. MASS ABOUT 4.8 g. BREAK EDGES 0.2, BORE CHAMFER 0.3 BOTH ENDS.",
            "BORE DIA 6 H7 = 6.000/6.012 THRU (SLIDING FIT ON THE 6 mm SPINDLE). TURN DIA 20, DIA 12, BORE AND",
            "  THE HORN FACE (Z 0) IN ONE SETUP; FACE SQUARE TO BORE 0.02. M3: DRILL 2.5, ONE WALL INTO THE BORE.",
            "4x M2 (DRILL 1.6, TAP THRU) MUST MATCH THE SUPPLIED 25T HORN'S HOLES: CHECK OR SPOT THROUGH THE HORN.",
            "THE ROLL SPINDLE IT FITS (WITH ITS REAR SET-SCREW FLAT) IS DRAWN SEPARATELY: HD-034_roll_spindle_drawing.pdf.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=40)
    front.dim((-FLANGE_R, 0, 0.0), (-FLANGE_R, 0, LENGTH), orientation="v", offset=-12)
    front.dim((-FLANGE_R, 0, 2.0), (FLANGE_R, 0, 2.0), orientation="h", text="⌀<>", offset=-(2.0 * 2.5 + 12))
    right.dim((0, -SHAFT_R, 10.0), (0, SHAFT_R, 10.0), orientation="h", text="⌀<>")
    right.dim((0, FLANGE_R, 0.0), (0, FLANGE_R, FLANGE_T), orientation="v", tol=0.05)
    front.dim((SHAFT_R, 0, 0.0), (SHAFT_R, 0, SET_Z[0]), orientation="v", tol=0.1)
    front.dim((SHAFT_R, 0, 0.0), (SHAFT_R, 0, SET_Z[1]), orientation="v", tol=0.1)
    front.hole((0.0, -SHAFT_R, SET_Z[0]), 2.5, thread="M3x0.5 - 6H", count=2, label="INTO BORE", angle=30)
    top.hole((0.0, 0.0, LENGTH), 2 * BORE_R, thru=True, fit="H7", angle=135)
    top.hole((M2[0], M2[1], FLANGE_T), 1.6, thread="M2x0.4 - 6H", thru=True, count=4, label="ON ⌀14 PCD", angle=-40)
    return sheet


if __name__ == "__main__":
    collar_drawing()
