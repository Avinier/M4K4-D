"""Shop drawings for the CNC pack: CH-013 ballast bar, BO-047 pinion shaft, BO-046 fixed
pinion half (D-125), HD-009 pivot
pin, HD-034 roll spindle (STEPs from export_cnc_fab.py) and CH-052 bearing cap (STEP
from export_axle_fab.py). CH-012 and HD-004 keep stub_drawing.py and d120_collar_drawing.py.

Every dimension without `text` is measured on the STEP; the feature positions come
from ../fab/cnc-facts.json, which export_cnc_fab.py writes from the source constants.
Tolerances are the design's: fits from the mating parts, flat sizes from the printed
D-bores (flat at 2.55 from the axis) and the stock the builder ordered (BOM 2026-11-21).

Runs on cadgen 0.6.6 like stub_drawing.py:

    PYTHONPATH=~/.claude/plugins/cache/text-to-cad/cad/0.6.6/packages/cadgen/src \\
      MPLCONFIGDIR=/tmp/mpl <legacy venv python> cnc_drawings.py
"""
import json
import math
from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing

HERE = Path(__file__).resolve().parent
FAB = HERE.parent / "fab"
FACTS = json.loads((FAB / "cnc-facts.json").read_text())
BAL, PIN5, PIN6, SPN = FACTS["BAL"], FACTS["PIN5"], FACTS["PIN6"], FACTS["SPN"]
DATE = "2026-11-21"
SHAFT_STEEL = "EN-31 HARDENED ROD h6 (SUPPLIED) OR EN8/C45 GROUND h6"


def mass(name):
    return FACTS["parts"][name]["mass_g"]


@eng_drawing(out="../fab/CH-013_ballast_bar_drawing.pdf")
def ballast_drawing():
    part = cadgen.read_step(FAB / "CH-013_ballast_bar.step")
    t, l, h = BAL["t"], BAL["l"], BAL["h"]
    y0, y1 = BAL["hole_y"]
    sheet = Sheet(
        "A3", scale=2.0, title="BALLAST BAR", part_number="CH-013", material="C110 / ETP COPPER (Cu >= 99.9 %)",
        revision="A", author="MAKAD", general_tolerance="ISO 2768-m",
        revisions=[("A", DATE, "FIRST ISSUE; COPPER PER D-109")],
        notes=[
            "QTY 1. MILL ALL SIX FACES FROM ~10 x 20 COPPER FLAT (SUPPLIED OR SHOP STOCK). NO PLATING.",
            f"MASS {mass('CH-013_ballast_bar'):.1f} g NOMINAL; WEIGH AND RECORD. DO NOT SUBSTITUTE BRASS OR STEEL (TIPPING MARGIN).",
            "TOP FACE (Z 19, THE DECK FACE) FLAT WITHIN 0.1. BREAK ALL EDGES 0.3 x 45 DEG.",
            f"2x M3x0.5-6H FROM THE TOP FACE, THREAD {BAL['thread']:g} DEEP, DRILL DIA 2.5 x {BAL['drill']:g} DEEP, C'SINK 0.3.",
            "COPPER IS GUMMY: SHARP SPIRAL-POINT OR FORMING TAP WITH CUTTING OIL; CLEAN THREADS, CHECK WITH AN M3 SCREW.",
            f"HOLE SPACING {y1 - y0:g} +/-0.1 ON THE CENTRE LINE (DECK HOLES DIA 3.4 GIVE 0.2 FLOAT).",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=40)
    front.overall()
    right.dim((0, -t / 2, h / 2), (0, t / 2, h / 2), orientation="h")
    top.dim((y0, 0, h), (y1, 0, h), orientation="h", tol=0.1)
    top.dim((-l / 2, 0, h / 2), (y0, 0, h), orientation="h")
    top.hole((y1, BAL["hole_x"], h), 2.5, thread="M3x0.5 - 6H", depth=BAL["thread"], count=2, angle=40)
    return sheet


def _shaft_sheet(**kw):
    return Sheet("A3", author="MAKAD", general_tolerance="ISO 2768-m", revision="A", **kw)


@eng_drawing(out="../fab/BO-047_pinion_shaft_drawing.pdf")
def pinion_shaft_drawing():
    part = cadgen.read_step(FAB / "BO-047_pinion_shaft.step")
    r, l, f = PIN5["r"], PIN5["l"], PIN5["flat"]
    sheet = _shaft_sheet(
        scale=4.0, title="YAW PINION SHAFT", part_number="BO-047",
        material="5 mm D-SHAFT STOCK (SUPPLIED) OR EN8/C45 / SS303 h6",
        revisions=[("A", DATE, "FIRST ISSUE (D-044, D-125): NO TAPPED HOLE")],
        notes=[
            "QTY 2 (1 + SPARE). CUT FROM THE SUPPLIED 5 mm GROUND D-SHAFT (FLAT 4.45-4.55 ACROSS, FULL LENGTH).",
            "DIA 5 h6 = 4.992/5.000 AS SUPPLIED. LENGTH 17.4 +/-0.1, ENDS SQUARE TO THE AXIS 0.05. NO HOLES.",
            f"CHAMFER BOTTOM END {PIN5['cham_bottom']:g} x 45, TOP END {PIN5['cham_top']:g} x 45. DEBURR THE FLAT EDGES. MASS ABOUT {mass('BO-047_pinion_shaft'):.1f} g.",
            f"Z 0-{PIN5['bond'][1]:g}: BONDED IN THE PRINTED HUB. Z {PIN5['fixed_half'][0]:g}-{l:g}: BO-046 ALUMINIUM HALF ON LOCTITE 641.",
            "LEAVE BOTH ENDS CLEAN AND OIL-FREE (ADHESIVE JOINTS).",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=44)
    front.overall()
    front.dim((-r, 0, l / 2), (r, 0, l / 2), orientation="h", fit="h6", text="⌀<>", offset=-(l / 2 * 4 + 14))
    right.dim((0, -(r - f), l / 2), (0, r, l / 2), orientation="h", tol=0.05)
    return sheet


@eng_drawing(out="../fab/BO-046_fixed_pinion_half_drawing.pdf")
def fixed_half_drawing():
    part = cadgen.read_step(FAB / "BO-046_fixed_pinion_half.step")
    g = FACTS["PINION_HALF"]
    t, br, bf, peg = g["t"], g["bore_r"], g["bore_flat"], g["peg"]
    m, z = g["module"], g["teeth"]
    alpha = math.radians(20.0)
    inv = math.tan(alpha) - alpha
    k = 5
    span = m * math.cos(alpha) * (math.pi * (k - 0.5) + z * inv) - (g["backlash"] / 2) * math.cos(alpha)
    da, df = m * (z + 2), m * (z - 2.5)
    sheet = Sheet(
        "A3", scale=2.0, title="FIXED PINION HALF", part_number="BO-046 (FIXED)",
        material="7075-T6 ALUMINIUM PLATE 2.0 (6061-T6 ACCEPTABLE)", revision="A", author="MAKAD",
        general_tolerance="ISO 2768-m", revisions=[("A", DATE, "FIRST ISSUE (D-125): METAL HALF")],
        notes=[
            f"QTY 2 (1 + SPARE). PLATE {t:g} +/-0.05, FLAT 0.03. CUT THE PROFILE FROM BO-046_fixed_pinion_half.dxf",
            "  (MM, LAYER CUT) BY WIRE EDM (PREFERRED) OR FIBRE LASER; OR GENERATE THE GEAR FROM THE DATA BELOW.",
            f"SPUR GEAR m {m:g}, z {z}, 20 DEG, x 0, TIP DIA {da:.1f}, ROOT DIA {df:.2f}; TEETH THINNED FOR 0.15 BACKLASH:",
            f"  SPAN OVER {k} TEETH W = {span:.3f} -0.03/+0. TOOTH PHASE TO THE FLAT IS NOT CRITICAL.",
            f"BORE DIA {2 * br:g} H7 = 5.000/5.012 WITH A FLAT {br + bf:.2f} +0.03/0 ACROSS (BORE WALL TO FLAT).",
            f"PEG HOLE DIA {peg['d']:g} H7 THRU AT R{peg['r']:g} ON THE FLAT'S CENTRE LINE, OPPOSITE THE FLAT.",
            "BREAK TOOTH EDGES 0.3 ON THE BOTTOM FACE (MESH LEAD-IN), 0.1 ON THE TOP; DEBURR THE BORE. NO FINISH.",
            f"ASSEMBLY: PRESS AN ISO 8734 DIA 2 x 4 m6 DOWEL FLUSH WITH THE TOP FACE. MASS ABOUT {mass('BO-046_fixed_pinion_half'):.1f} g.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=36)
    top.dim((0, -bf, t), (0, br, t), orientation="v", tol=(0.03, 0.0), offset=-50)
    top.hole((0.0, peg["r"], t), peg["d"], thru=True, fit="H7", angle=30)
    top.hole((0.0, 0.0, t), 2 * br, thru=True, fit="H7", label="WITH FLAT", angle=-35)
    front.dim((da / 2 - 0.2, 0, 0.0), (da / 2 - 0.2, 0, t), orientation="v", tol=0.05)
    return sheet


@eng_drawing(out="../fab/HD-009_pivot_pin_drawing.pdf")
def pivot_pin_drawing():
    part = cadgen.read_step(FAB / "HD-009_pivot_pin.step")
    r, l, f = PIN6["r"], PIN6["l"], PIN6["flat"]
    b0, b1 = PIN6["bearing"]
    sheet = _shaft_sheet(
        scale=5.0, title="PITCH PIVOT PIN", part_number="HD-009", material=SHAFT_STEEL,
        revisions=[("A", DATE, "FIRST ISSUE (D-051); NO M2 HOLE (HARDENED STOCK)")],
        notes=[
            "QTY 2 (1 + SPARE). CUT FROM THE SUPPLIED DIA 6 HARDENED ROD WITH AN ABRASIVE DISC; KEEP IT COOL.",
            "DIA 6 h6 = 5.992/6.000 AS SUPPLIED (DO NOT TURN OR POLISH). LENGTH 11.5 +/-0.05, ENDS SQUARE 0.05.",
            "GRIND THE FLAT FULL LENGTH, 5.5 +0/-0.05 ACROSS, PARALLEL TO THE AXIS 0.03. NO BURR ON THE FLAT EDGES.",
            f"CHAMFER INNER END (Z 0) {PIN6['cham_inner']:g} x 45 (LEAD-IN); OUTER END {PIN6['cham_outer']:g} x 45 MAX.",
            f"Z {b0:g}-{b1:g}: MR106 INNER RING SEAT; NO MARKS. MASS ABOUT {mass('HD-009_pivot_pin'):.1f} g.",
            "IF MADE FROM UNHARDENED EN8/C45 INSTEAD: SAME DRAWING, GRIND DIA 6 TO h6.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=44)
    front.overall()
    front.dim((-r, 0, l / 2), (r, 0, l / 2), orientation="h", fit="h6", text="⌀<>", offset=-(l / 2 * 5 + 14))
    right.dim((0, -(r - f), l / 2), (0, r, l / 2), orientation="h", tol=(0.0, 0.05))
    return sheet


@eng_drawing(out="../fab/HD-034_roll_spindle_drawing.pdf")
def roll_spindle_drawing():
    # Drawn horizontal, the usual way for a shaft: STEP z -> sheet X, so the rear flat
    # (STEP -X) faces up in the front view and the front flat (STEP -Y) faces the viewer.
    from build123d import Axis
    part = cadgen.read_step(FAB / "HD-034_roll_spindle.step").rotate(Axis.Y, 90)

    def P(x, y, z):          # STEP point -> drawing-model point
        return (z, y, -x)

    r, l, f, fr = SPN["r"], SPN["l"], SPN["flat"], SPN["rear_depth"]
    f0, f1 = SPN["front_flat"]
    _, r1 = SPN["rear_flat"]
    (j0, j1), (j2, j3) = SPN["bearings"]
    sheet = _shaft_sheet(
        scale=3.0, title="ROLL SPINDLE", part_number="HD-034", material=SHAFT_STEEL,
        revisions=[("A", DATE, "FIRST ISSUE (M016; D-053, D-120)")],
        notes=[
            "QTY 2 (1 + SPARE). CUT FROM THE SUPPLIED DIA 6 HARDENED ROD; LENGTH 44.4 +/-0.1, ENDS SQUARE 0.05.",
            "DIA 6 h6 = 5.992/6.000 AS SUPPLIED. TWO GROUND FLATS, EACH 5.5 +0/-0.05 ACROSS, PARALLEL TO THE AXIS 0.03:",
            f"  FRONT FLAT {f1 - f0:g} LONG FROM THE FRONT END (NOT SHORTER: THE CRADLE D-BORE STARTS THERE; MAX {f1 - f0 + 0.3:g}).",
            f"  REAR FLAT {r1:g} +/-0.3 LONG FROM THE REAR END, 90 +/-2 DEG FROM THE FRONT FLAT AS DRAWN:",
            "  SEEN FROM THE REAR END WITH THE FRONT FLAT AT 12 O'CLOCK, THE REAR FLAT IS AT 9 O'CLOCK.",
            f"BEARING JOURNALS Z {j0:g}-{j1:g} AND {j2:g}-{j3:g} (696-2Z): ROUND, NO MARKS. CHAMFER BOTH ENDS {SPN['cham']:g} x 45.",
            f"REAR END Z 0-{SPN['collar'][1]:g} SLIDES IN THE HD-004 DIA 6 H7 BORE. MASS ABOUT {mass('HD-034_roll_spindle'):.1f} g.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=40)
    front.overall()
    front.dim(P(-(r - fr), 0, 0.0), P(-(r - fr), 0, r1), orientation="h", tol=0.3)
    front.dim(P(-(r - fr), 0, 4.0), P(r, 0, 4.0), orientation="v", tol=(0.0, 0.05))
    right.dim(P(-r, 0, l), P(r, 0, l), orientation="v", fit="h6", text="⌀<>")
    top.dim(P(0, -(r - f), f0), P(0, -(r - f), l), orientation="h", tol=(0.3, 0.0))
    top.dim(P(0, -(r - f), 40.0), P(0, r, 40.0), orientation="v", tol=(0.0, 0.05))
    top.dim(P(0, -r, 0.0), P(0, -r, j0), orientation="h", text="<>")
    top.dim(P(0, -r, 0.0), P(0, -r, j2), orientation="h", text="<>")
    return sheet


@eng_drawing(out="../fab/CH-052_cap_drawing.pdf")
def cap_drawing():
    part = cadgen.read_step(FAB / "CH-052_cap.step")
    bb = part.bounding_box()
    t, od = bb.max.Z - bb.min.Z, bb.max.X - bb.min.X
    sheet = Sheet(
        "A3", scale=4.0, title="BEARING RETAINING CAP", part_number="CH-052",
        material="1.2 mm ALUMINIUM 5052-H32 OR 6061-T6", revision="A", author="MAKAD",
        general_tolerance="ISO 2768-m", revisions=[("A", DATE, "DRAWING ADDED TO THE D-071 DXF")],
        notes=[
            "QTY 3 (2 + 1 SPARE). CUT FROM CH-052_cap.dxf (MM, LAYER CUT): FIBRE LASER OR WATERJET, NOT CO2.",
            "SHEET 1.2 mm (1.0-1.5 ACCEPTABLE: STATE WHAT IS STOCKED BEFORE CUTTING). FLAT WITHIN 0.1.",
            "DEBURR BOTH FACES; NO DROSS ON THE DIA 12.5 BORE. NO FINISH REQUIRED.",
            "4x DIA 3.4 SCREW HOLES ON R12 (PCD 24) AT 45 DEG; 2x DIA 2.6 KEY HOLES AT R8.5 ON THE X AXIS.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True, gap=40)
    top.overall()
    a = math.radians(45)
    top.hole((12 * math.cos(a), 12 * math.sin(a), t), 3.4, thru=True, count=4, angle=45)
    top.hole((8.5, 0.0, t), 2.6, thru=True, count=2, angle=-30)
    top.hole((0.0, 0.0, t), 12.5, thru=True, angle=200)
    front.dim((od / 2, 0, 0.0), (od / 2, 0, t), orientation="v")
    return sheet


if __name__ == "__main__":
    for fn in (ballast_drawing, pinion_shaft_drawing, fixed_half_drawing, pivot_pin_drawing, roll_spindle_drawing, cap_drawing):
        fn()
