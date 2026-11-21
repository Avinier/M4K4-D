"""D-125: the yaw pinion's fixed half becomes aluminium, keyed on BO-047's D-flat.

D-044 keys the fixed scissor-pinion half (BO-046, upper 2 mm) to the shaft (BO-047)
by a D-flat, but the body source models the shaft and the bore round. A 2 mm PETG
half cannot carry the key load: the spring sits on the hub collar, so the 0.22 N.m
preload passes through the fixed half's key all the time (49-73 MPa on the flat,
`E`). The builder chose a metal fixed half (D-044's own fallback), 2026-11-21:

- Shaft: the droid's BO-047 gets the ordered D-shaft stock's flat (4.45-4.55
  across, 0.5 deep, 2.0 from the axis), full length, facing world -Y at neutral;
  fab/BO-047_pinion_shaft.step is the same solid.
- Fixed half: 7075-T6 (6061-T6 acceptable) 2.0 mm plate, the model's thinned
  m1 z37 involute, Ø5 H7 bore with a D-flat at 2.05 from the axis (0.05 clearance,
  the head D-bores' rule; about 2 deg play, which cannot open as lash while the
  demand stays under the preload). Held by Loctite 641 on the D-fit (CH-057),
  metal to steel. The D-044 M2 countersunk screw is dropped: its head (~Ø3.8)
  sits wholly on the Ø5 shaft end and never bore on the half.
- Pre-wind peg (D-044: "a peg on the fixed half, in an arc slot of the sprung
  half"): an ISO 8734 Ø2 x 4 dowel pressed through the half at r 10 on +Y, top
  flush, 1.8 mm into an arc slot in the sprung half. The spring turns the sprung
  half +θ (counter-clockwise seen from +Z) against the slot's clockwise end. The
  slot is 2.3 wide on the Ø2 peg, so the stop comes 0.86 deg after the end's centre
  passes the peg: at the meshed (neutral) position the half is 1.2 deg off the stop,
  0.39 mm at the pitch circle, inside D-044's 0.5 mm lead-in chamfers; on meshing
  the tooth flanks wind it back that far. The slot runs ~12.9 deg the other way so
  the half can be wound past and the fixed half dropped on.
- Unchanged: the BO-056 hub bore stays round (shaft bonded); the sprung half
  stays PETG, free on the round part of the shaft.

World frame = body frame (the droid places the body tree unmoved). The fab frame
is the world shifted by (-PX, -PY, -FIXED_Z[0]): no rotation, so the flat stays
on -Y and the tooth phase is the droid's.
"""
import math

from build123d import Box, Cylinder, Face, Location, Wire, extrude
import body_v1_model as B

PX = B.BODY_AXIS_X + B.YAW_PINION_CENTER[0]
PY = B.YAW_PINION_CENTER[1]
R, Z0, Z1 = B.YAW_SHAFT
SHAFT_FLAT = 2.0                                    # from the axis; stock 4.45-4.55 across -> 1.95-2.05
BORE_FLAT = 2.05
FIXED_Z = (B.YAW_PINION_Z[1] - B.YAW_SCISSOR_HALF_FACE, B.YAW_PINION_Z[1])        # 148.6-150.6
SPRUNG_Z = (B.YAW_PINION_Z[0], B.YAW_PINION_Z[0] + B.YAW_SCISSOR_HALF_FACE)         # 146.4-148.4
PHASE = 270.0 + 180.0 / B.YAW_GEAR_TEETH            # body_v1_model's pinion phase at yaw 0
PEG = dict(r=10.0, deg=90.0, d=2.0, length=4.0)     # ISO 8734 2 x 4 m6, top flush with the half
SLOT = dict(width=2.3, cw=0.35, ccw=12.0)           # end-centre angles from the peg at neutral (deg)
DENSITY = dict(al7075=2.81e-3, petg=1.20e-3, steel=7.85e-3)   # g/mm3 (PETG as check_d107_mass)


def _minus_y_slab(dist, z0, z1, reach, cx=PX, cy=PY):
    """Everything on the -Y side of the plane y = cy - dist, within `reach` of the axis."""
    depth = reach - dist
    return Box(2 * reach, depth, z1 - z0).moved(Location((cx, cy - dist - depth / 2, (z0 + z1) / 2)))


def peg_xy(cx=PX, cy=PY):
    a = math.radians(PEG["deg"])
    return cx + PEG["r"] * math.cos(a), cy + PEG["r"] * math.sin(a)


def shaft_flat_tool():
    """DROID_CUTS tool: the BO-047 flat, full length."""
    return _minus_y_slab(SHAFT_FLAT, Z0 - 1.0, Z1 + 1.0, R + 1.0)


def bore_key(cx=PX, cy=PY, z0=FIXED_Z[0], z1=FIXED_Z[1]):
    """Fills the round bore beyond the D-bore's flat; overlaps the gear by 0.3 mm radially."""
    disc = Cylinder(R + 0.3, z1 - z0).moved(Location((cx, cy, (z0 + z1) / 2)))
    return disc & _minus_y_slab(BORE_FLAT, z0, z1, R + 1.0, cx, cy)


def peg_pin(cx=PX, cy=PY, top=FIXED_Z[1]):
    x, y = peg_xy(cx, cy)
    return Cylinder(PEG["d"] / 2, PEG["length"]).moved(Location((x, y, top - PEG["length"] / 2)))


def sprung_slot_tool():
    """DROID_CUTS tool: the arc slot in the sprung half, through, with round ends."""
    z0, z1 = SPRUNG_Z[0] - 1.0, SPRUNG_Z[1] + 1.0
    w2, r = SLOT["width"] / 2, PEG["r"]
    a0, a1 = PEG["deg"] - SLOT["cw"], PEG["deg"] + SLOT["ccw"]
    far = r + w2 + 2.0
    pts = [(PX, PY, z0)] + [(PX + far / math.cos(math.radians((a1 - a0) / 4)) * math.cos(math.radians(a)),
                             PY + far / math.cos(math.radians((a1 - a0) / 4)) * math.sin(math.radians(a)), z0)
                            for a in (a0, (a0 + a1) / 2, a1)]
    wedge = extrude(Face(Wire.make_polygon(pts, close=True)), z1 - z0)
    ring = Cylinder(r + w2, z1 - z0).moved(Location((PX, PY, (z0 + z1) / 2))) - \
        Cylinder(r - w2, z1 - z0 + 1).moved(Location((PX, PY, (z0 + z1) / 2)))
    slot = ring & wedge
    for a in (a0, a1):
        x, y = PX + r * math.cos(math.radians(a)), PY + r * math.sin(math.radians(a))
        slot += Cylinder(w2, z1 - z0).moved(Location((x, y, (z0 + z1) / 2)))
    return slot


def metal_half_local():
    """The fixed half as made (fab frame): gear, Ø5 bore with the D-flat, Ø2 peg hole."""
    t = B.YAW_SCISSOR_HALF_FACE
    half = B._involute_gear(B.YAW_GEAR_TEETH, B.YAW_GEAR_MODULE, 0.0, t, 0.0, 0.0, PHASE)
    half -= Cylinder(R, t + 2).moved(Location((0, 0, t / 2)))
    half += bore_key(0.0, 0.0, 0.0, t)
    x, y = peg_xy(0.0, 0.0)
    half -= Cylinder(PEG["d"] / 2, t + 2).moved(Location((x, y, t / 2)))
    return half


CUTS = [(r"YAW_PINION_SHAFT_D5_STEEL", shaft_flat_tool()),
        (r"YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF", sprung_slot_tool())]
ADDS = [(r"YAW_DRIVE_SCISSOR_PINION_FIXED_HALF", bore_key()),
        (r"YAW_DRIVE_SCISSOR_PINION_FIXED_HALF", peg_pin())]   # the pressed dowel, fused for the droid
