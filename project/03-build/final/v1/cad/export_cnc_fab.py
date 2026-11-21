"""Fabrication STEPs for Makad's machined (CNC) parts that had none, from the same
source constants the droid geometry uses. Writes to ../fab/:

- CH-013_ballast_bar.step: C110 copper bar 9 x 60 x 19 (D-026 envelope, D-109
  copper), two M3 tapped holes from the deck face. Frame: length along X (droid
  Y, centred), thickness along Y (droid X, centred), the deck (top) face at z 19.
- BO-047_pinion_shaft.step: Ø5 h6 x 17.4 yaw pinion shaft (D-044), the stock's
  0.5 mm D-flat full length; no tapped hole since D-125 (the fixed half is held by
  Loctite 641). Frame: axis Z, hub (bottom) end at z 0, top at z 17.4, flat on -Y.
- BO-046_fixed_pinion_half.step + .dxf: the D-125 aluminium fixed pinion half,
  2 mm, m1 z37 thinned involute, Ø5 bore with the D-flat at 2.05, Ø2 peg hole at
  r 10 on +Y (d125_pinion_dbore.metal_half_local). Frame: the world shifted to the
  pinion axis, bottom face at z 0, flat on -Y. The DXF is the bottom-face profile
  for wire EDM or fibre laser.
- HD-009_pivot_pin.step: Ø6 h6 x 11.5 pitch -Y pivot pin (D-051), 0.5 mm D-flat
  full length. No M2 extraction hole: the stock is hardened EN-31 rod (BOM
  2026-11-21), which cannot be tapped. Frame: axis Z, inner (boss) end at z 0,
  outer (retainer) end at z 11.5, flat on -Y (head +Z at neutral).
- HD-034_roll_spindle.step: Ø6 h6 x 44.4 roll spindle (M016; D-053, D-120), front
  D-flat 0.5 deep (cradle set screw, head +Z) and rear flat 0.5 deep (collar set
  screws, head +Y). Frame: axis Z, rear (collar) end at z 0, front end at z 44.4;
  head X -> local Z, head +Z -> local -Y, head +Y -> local -X.

The STEPs add what a shop makes and the droid leaves out: end chamfers, tap-drill
holes with 118 deg points (threads are called out on the drawings, not modelled),
and the D-flats. `nominal()` returns each part as the droid draws it, in the
same local frame; check_cnc_fab.py compares those to the droid leaves.

CH-012, CH-052 (export_axle_fab.py) and HD-004 (export_d120_fab.py) keep their own
exporters. cnc_drawings.py makes the PDFs; package_cnc.py copies the pack to
04-print/04-cnc/upload/.

Run from this folder with the legacy runtime (seconds; nothing big is built):

    MAKAD_RELIEF_SERIAL=1 PYTHONPATH=../../../03-head/v1/cad:../../../02-body/v1/cad:. \\
      $CAD_PY export_cnc_fab.py
"""
import json
import math
from pathlib import Path

from build123d import Axis, Box, Cone, Cylinder, Face, Location, Wire, export_step, revolve

import body_v1_model as B
import d120_roll_horn_hub as D
import feetech as fe
import d125_pinion_dbore as P125

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "fab"

STEEL, COPPER, AL7075 = 7.85e-3, 8.94e-3, 2.81e-3   # g/mm3
DRILL_POINT = 118.0
M2_DRILL, M3_DRILL = 1.6, 2.5             # ISO coarse tap drills

# --- Part facts (everything a drawing dimensions comes from here) ----------
BAL = dict(t=B.BALLAST_X[1] - B.BALLAST_X[0], l=2 * B.BALLAST_HALF_Y, h=B.BALLAST_Z[1] - B.BALLAST_Z[0],
           hole_y=tuple(B.BALLAST_SCREW_Y), hole_x=B.BALLAST_SCREW_X - sum(B.BALLAST_X) / 2,
           thread=B.BALLAST_SCREW_THREAD_DEPTH, drill=B.BALLAST_SCREW_HOLE_DEPTH, edge=0.3)
PIN5 = dict(r=B.YAW_SHAFT[0], l=B.YAW_SHAFT[2] - B.YAW_SHAFT[1], flat=0.5,
            cham_bottom=0.3, cham_top=0.2,
            bond=(0.0, B.YAW_DRIVE_COLLAR[2] - B.YAW_SHAFT[1]),                    # hub + collar, z 0..7
            fixed_half=(B.YAW_PINION_Z[1] - B.YAW_SCISSOR_HALF_FACE - B.YAW_SHAFT[1],
                        B.YAW_PINION_Z[1] - B.YAW_SHAFT[1]))                       # D-keyed half, z 15.4..17.4
_t = fe.TRUNNION
PIN6 = dict(r=_t["pin_r"], l=_t["pin_y"][1] - _t["pin_y"][0], flat=_t["pin_r"] - _t["pin_flat"],
            cham_inner=0.3, cham_outer=0.1,
            boss=(0.0, _t["pin_y"][1] - _t["bore_y"][0]),                          # D-bore engagement 6.7
            bearing=(_t["pin_y"][1] - _t["lip_y"][0], _t["pin_y"][1] - _t["recess_floor_y"]))  # MR106 inner ring
_sx0, _sx1 = fe.SPINDLE_X
_sf = fe.SPINDLE_FRONT
SPN = dict(r=3.0, l=_sx1 - _sx0, flat=3.0 - _sf["flat"], cham=0.3,
           front_flat=(_sf["bore"][0] - _sx0, _sx1 - _sx0),                          # z 34.6..44.4
           rear_flat=(0.0, D.SPINDLE_FLAT["x"][1] - _sx0), rear_depth=D.SPINDLE_FLAT["depth"],
           bearings=[(x - 2.5 - _sx0, x + 2.5 - _sx0) for x in sorted(fe.ROLL_BEARING_X)],  # 696-2Z, B 5
           collar=(0.0, D.COLLAR_X[1] - _sx0), set_screw_z=[x - _sx0 for x in D.COLLAR["set_x"]],
           cradle_screw_z=_sf["screw_x"] - _sx0)


# --- Helpers ---------------------------------------------------------------
def turned(points):
    """Solid of revolution about Z from (r, z) points listed from the axis round the outline."""
    wire = Wire.make_polygon([(r, 0.0, z) for r, z in points], close=True)
    return revolve(Face(wire), Axis.Z, 360.0)


def plain_shaft(r, length, c0, c1):
    """Ø2r x length on Z from 0, chamfered c0 x 45 at z 0 and c1 x 45 at the far end."""
    pts = [(0.0, 0.0)]
    pts += [(r - c0, 0.0), (r, c0)] if c0 else [(r, 0.0)]
    pts += [(r, length - c1), (r - c1, length)] if c1 else [(r, length)]
    pts += [(0.0, length)]
    return turned(pts)


def flat_cut(r, depth, z0, z1, side):
    """Material outside a flat `depth` deep on `side` ('-Y' or '-X'), from z0 to z1."""
    w, d = 2 * r + 2, r + 1
    if side == "-Y":
        box = Box(w, d, z1 - z0).moved(Location((0, -(r - depth) - d / 2, (z0 + z1) / 2)))
    else:
        box = Box(d, w, z1 - z0).moved(Location((-(r - depth) - d / 2, 0, (z0 + z1) / 2)))
    return box


def one_solid(shape, label):
    solids = shape.solids()
    assert len(solids) == 1, (label, len(solids))
    s = solids[0]
    assert s.is_valid, label
    s.label = label
    return s


# --- Parts -----------------------------------------------------------------
def ballast_bar(nominal=False):
    t, l, h = BAL["t"], BAL["l"], BAL["h"]
    bar = Box(l, t, h).moved(Location((0, 0, h / 2)))
    if nominal:   # the droid: Ø3 x 9 flat-bottomed holes, sharp edges
        for x in BAL["hole_y"]:
            bar -= Cylinder(1.5, BAL["drill"] + 0.5).moved(Location((x, BAL["hole_x"], h - (BAL["drill"] - 0.5) / 2)))
        return one_solid(bar, "CH-013_nominal")
    from build123d import chamfer
    bar = chamfer(bar.edges(), BAL["edge"])
    for x in BAL["hole_y"]:
        bar -= _hole_from_top(M3_DRILL / 2, BAL["drill"], h, x, BAL["hole_x"], lead=0.3)
    return one_solid(bar, "CH-013_BALLAST_BAR_C110")


def pinion_shaft(nominal=False):
    r, l = PIN5["r"], PIN5["l"]
    if nominal:   # the droid since D-125: round with the stock's full-length flat
        s = Cylinder(r, l).moved(Location((0, 0, l / 2))) - flat_cut(r, PIN5["flat"], -1, l + 1, "-Y")
        return one_solid(s, "BO-047_nominal")
    s = plain_shaft(r, l, PIN5["cham_bottom"], PIN5["cham_top"])
    s -= flat_cut(r, PIN5["flat"], -1, l + 1, "-Y")
    return one_solid(s, "BO-047_PINION_SHAFT")


def fixed_pinion_half(nominal=False):
    """D-125 aluminium half; the droid's fixed half less the pressed peg. Tooth-edge
    breaks are a drawing note, so the made and nominal solids are the same."""
    return one_solid(P125.metal_half_local(), "BO-046_nominal" if nominal else "BO-046_FIXED_PINION_HALF_7075")


def pivot_pin(nominal=False):
    r, l = PIN6["r"], PIN6["l"]
    if nominal:
        s = Cylinder(r, l).moved(Location((0, 0, l / 2))) - flat_cut(r, PIN6["flat"], -1, l + 1, "-Y")
        return one_solid(s, "HD-009_nominal")
    s = plain_shaft(r, l, PIN6["cham_inner"], PIN6["cham_outer"])
    s -= flat_cut(r, PIN6["flat"], -1, l + 1, "-Y")
    return one_solid(s, "HD-009_PIVOT_PIN")


def roll_spindle(nominal=False):
    r, l = SPN["r"], SPN["l"]
    s = Cylinder(r, l).moved(Location((0, 0, l / 2))) if nominal else plain_shaft(r, l, SPN["cham"], SPN["cham"])
    f0, f1 = SPN["front_flat"]
    s -= flat_cut(r, SPN["flat"], f0, f1 + 1, "-Y")
    r0, r1 = SPN["rear_flat"]
    s -= flat_cut(r, SPN["rear_depth"], r0 - 1, r1, "-X")
    return one_solid(s, "HD-034_nominal" if nominal else "HD-034_ROLL_SPINDLE")


def _hole_from_top(r, depth, top, x=0.0, y=0.0, lead=0.2):
    """Tap-drill hole down from z `top`: full diameter for `depth`, a 118 deg point below,
    and a 90 deg lead-in countersink `lead` wide at the mouth."""
    cone_h = r / math.tan(math.radians(DRILL_POINT / 2))
    hole = Cylinder(r, depth + 0.5).moved(Location((0, 0, top - depth / 2 + 0.25)))
    hole += Cone(0.0, r, cone_h).moved(Location((0, 0, top - depth - cone_h / 2)))
    hole += Cone(r, r + lead + 0.1, lead + 0.1).moved(Location((0, 0, top - lead / 2 + 0.05)))
    return hole.moved(Location((x, y, 0)))


PARTS = {
    "CH-013_ballast_bar": (ballast_bar, COPPER),
    "BO-047_pinion_shaft": (pinion_shaft, STEEL),
    "BO-046_fixed_pinion_half": (fixed_pinion_half, AL7075),
    "HD-009_pivot_pin": (pivot_pin, STEEL),
    "HD-034_roll_spindle": (roll_spindle, STEEL),
}


def self_checks():
    """Facts the drawings and the RFQ rely on, from the source constants."""
    rows = {}
    # Spindle: both flats clear of the 696 bearing journals; the flats sit under their screws.
    (b0, b1), (b2, b3) = SPN["bearings"]
    rows["spindle_rear_flat_clear_of_rear_bearing_mm"] = round(b0 - SPN["rear_flat"][1], 3)
    rows["spindle_front_flat_clear_of_front_bearing_mm"] = round(SPN["front_flat"][0] - b3, 3)
    rows["spindle_collar_set_screws_on_rear_flat"] = all(SPN["rear_flat"][0] + 1.5 <= z <= SPN["rear_flat"][1] - 1.5 for z in SPN["set_screw_z"])
    rows["spindle_cradle_screw_on_front_flat"] = SPN["front_flat"][0] + 1.5 <= SPN["cradle_screw_z"] <= SPN["front_flat"][1] - 1.5
    # Pivot pin: chamfers stay outside the MR106 inner-ring band.
    rows["pivot_outer_chamfer_inside_bearing_band_mm"] = round(PIN6["l"] - PIN6["bearing"][1], 3)
    ok = (rows["spindle_rear_flat_clear_of_rear_bearing_mm"] >= 2.0 and rows["spindle_front_flat_clear_of_front_bearing_mm"] >= 0.4
          and rows["spindle_collar_set_screws_on_rear_flat"] and rows["spindle_cradle_screw_on_front_flat"]
         )
    return ok, rows


def half_dxf(path):
    """Bottom-face profile of the fixed half (mm, layer CUT) for wire EDM or fibre laser."""
    from build123d import ExportDXF, Axis as _A
    face = fixed_pinion_half().faces().sort_by(_A.Z)[0]
    exp = ExportDXF()
    exp.add_layer("CUT")
    exp.add_shape(face, layer="CUT")
    exp.write(str(path))


def main():
    OUT.mkdir(exist_ok=True)
    ok, rows = self_checks()
    for k, v in rows.items():
        print(f"  {k}: {v}")
    assert ok, rows
    facts = {"BAL": BAL, "PIN5": PIN5, "PIN6": PIN6, "SPN": SPN, "parts": {}}
    for name, (build, rho) in PARTS.items():
        part, nom = build(), build(nominal=True)
        bb = part.bounding_box()
        nb = nom.bounding_box()
        # Inside the droid part's envelope (chamfers, holes and BO-047's new flat only remove
        # material), and the same length along Z.
        for a in "XYZ":
            assert getattr(bb.max, a) <= getattr(nb.max, a) + 1e-6 and getattr(bb.min, a) >= getattr(nb.min, a) - 1e-6, (name, a)
        assert abs(bb.size.Z - nb.size.Z) < 1e-6 and abs(bb.size.X - nb.size.X) < 1e-6, name
        export_step(part, str(OUT / f"{name}.step"))
        g = part.volume * rho
        facts["parts"][name] = dict(size=[round(bb.size.X, 3), round(bb.size.Y, 3), round(bb.size.Z, 3)],
                                    volume_mm3=round(part.volume, 2), mass_g=round(g, 2),
                                    nominal_volume_mm3=round(nom.volume, 2))
        print(f"wrote {name}.step: {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm, {g:.2f} g")
    half_dxf(OUT / "BO-046_fixed_pinion_half.dxf")
    facts["PINION_HALF"] = dict(t=P125.B.YAW_SCISSOR_HALF_FACE, bore_r=P125.R, bore_flat=P125.BORE_FLAT,
                                peg=P125.PEG, teeth=P125.B.YAW_GEAR_TEETH, module=P125.B.YAW_GEAR_MODULE,
                                backlash=P125.B.YAW_GEAR_BACKLASH, phase=P125.PHASE)
    (OUT / "cnc-facts.json").write_text(json.dumps(facts, indent=1) + "\n")


if __name__ == "__main__":
    main()
