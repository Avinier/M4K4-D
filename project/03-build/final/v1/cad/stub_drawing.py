"""Shop drawing of the axle stub CH-012 (D-007, D-012, D-033, D-071), for a turning quote.

Reads ../fab/CH-012_stub.step, written by export_axle_fab.py from the final droid
geometry, and writes ../fab/CH-012_stub_drawing.pdf. Every dimension without `text`
is measured on that solid, so a model change moves it; a point that misses the solid is
reported as "measures blank paper".

Runs on cadgen 0.6.6 (the engineering-drawing module), not the legacy CAD runtime:

    PYTHONPATH=~/.claude/plugins/cache/text-to-cad/cad/0.6.6/packages/cadgen/src \\
      MPLCONFIGDIR=/tmp/mpl <legacy venv python> stub_drawing.py

Frame (export_axle_fab.py): axis Z, inboard (motor) end at z 0, spigot tip at z 23; the
radial set-screw hole on -Y. Values below come from chassis v1 body_chassis_model.py
(STUB_*, SET_SCREW_Y, WHEEL_SCREW_*) and D-071 (flange Ø21).
"""

import math
from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing

HERE = Path(__file__).resolve().parent
SEAT_R, SEAT_END = 4.0, 13.51          # Ø8 k5, from the inboard end to the shoulder face
SHOULDER_R, SHOULDER_END = 4.75, 18.0  # Ø9.5
FLANGE_R, FLANGE_END = 10.5, 20.0      # Ø21 x 2 (D-071)
SPIGOT_R, LENGTH = 5.0, 23.0           # Ø10 g6 x 3
BORE_R, BORE_DEPTH = 2.025, 9.0        # Ø4.05 H8 on the motor D-shaft
SET_Z = 1.8                            # radial M3 on the shaft flat (|Y| 74.8)
PCD_R = 8.0
FLANGE_HOLES = [(PCD_R * math.cos(math.radians(a)), -PCD_R * math.sin(math.radians(a))) for a in (30.0, 150.0, 270.0)]


@eng_drawing(out="../fab/CH-012_stub_drawing.pdf")
def stub_drawing():
    part = cadgen.read_step(HERE.parent / "fab" / "CH-012_stub.step")
    sheet = Sheet(
        "A3", scale=2.0, title="AXLE STUB", part_number="CH-012", material="EN8 (080M40) OR C45 STEEL",
        revision="A", author="MAKAD", general_tolerance="ISO 2768-m",
        revisions=[("A", "2026-10-30", "FIRST ISSUE; FLANGE DIA 21 (D-071)")],
        notes=[
            "QTY 3 (2 + 1 SPARE). AS TURNED, NO PLATING, LIGHT OIL.",
            "DIA 8 k5 = 8.001/8.007, DIA 10 g6 = 9.986/9.995, DIA 4.05 H8 = 4.050/4.068.",
            "TURN DIA 8, DIA 10 AND THE DIA 4.05 BORE IN ONE SETUP: CONCENTRIC WITHIN 0.02.",
            "SHOULDER FACE (13.51) AND BOTH FLANGE FACES SQUARE TO THE AXIS WITHIN 0.02.",
            "SHOULDER CORNER SHARP OR UNDERCUT, NO FILLET OVER R0.15: BEARINGS SEAT ON IT.",
            "CHAMFER INBOARD END 0.3 x 45 DEG (BEARING LEAD-IN). BREAK OTHER EDGES 0.2.",
            "RADIAL M3: ONE WALL ONLY, INTO THE BORE; DRILL DIA 2.5. ANGLE TO FLANGE HOLES FREE.",
            "SPIGOT END M3: THREAD 8 DEEP, DRILL DIA 2.5 x 9.5 DEEP. MASS ABOUT 13 g.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=48)

    # Profile (front view: X across, Z up; the radial hole faces the viewer).
    front.overall()
    # Ø8 goes below the front view and the other three above the right view: four rows
    # above the front view ran into the top view's label, and below it into the notes. An offset is sheet mm from the dimension's own points (z at 2:1).
    scale = 2.0
    front.dim((-SEAT_R, 0, 7.0), (SEAT_R, 0, 7.0), orientation="h", fit="k5", text="⌀<>", offset=-(7.0 * scale + 12))
    right.dim((0, -FLANGE_R, 19.0), (0, FLANGE_R, 19.0), orientation="h", text="⌀<>")
    right.dim((0, -SHOULDER_R, 16.0), (0, SHOULDER_R, 16.0), orientation="h", text="⌀<>")
    right.dim((0, -SPIGOT_R, 21.5), (0, SPIGOT_R, 21.5), orientation="h", fit="g6", text="⌀<>")
    front.dim((SEAT_R, 0, 0.0), (SEAT_R, 0, SEAT_END), orientation="v", tol=0.05)
    front.dim((SHOULDER_R, 0, SEAT_END), (SHOULDER_R, 0, SHOULDER_END), orientation="v")
    front.dim((FLANGE_R, 0, SHOULDER_END), (FLANGE_R, 0, FLANGE_END), orientation="v", tol=0.05)
    front.dim((-SEAT_R, 0, 0.0), (-SEAT_R, 0, SET_Z), orientation="v", tol=0.1)
    front.hole((0.0, -SEAT_R, SET_Z), 2.5, thread="M3x0.5 - 6H", label="ONE WALL", angle=200)
    front.note(f"⌀4.05 H8 ↧{BORE_DEPTH:g} FROM INBOARD END", (BORE_R, 0, BORE_DEPTH / 2), offset=(-44, 8))

    # Spigot end (top view): the flange holes and the tapped centre.
    top.hole((*FLANGE_HOLES[0], FLANGE_END), 2.5, thread="M3x0.5 - 6H", thru=True, count=3, label="ON ⌀16 PCD", angle=30)
    top.hole((0.0, 0.0, LENGTH), 2.5, thread="M3x0.5 - 6H", depth=8, angle=135)
    return sheet


if __name__ == "__main__":
    stub_drawing()
