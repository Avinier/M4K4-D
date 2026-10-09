"""D-049 STS3045M pitch/roll installation: servo poses, output couplings, mounts.

Pitch: the servo rides on the pitch frame (P) with its spline on the pitch
axis pointing +Y; its 25T horn is screwed to the +Y yoke leg (Y), so the case
turns round a fixed output. Roll: the servo sits on a mount plate behind the
torsion box (P) with its spline on the roll axis pointing +X, driving the
spindle (R) through a goBILDA clamping coupler.

Sources: Feetech STS3045M drawing (purchased/sts3045m_reference-brief.md);
goBILDA 4001-0025-0006 official STEP (purchased/). Horn values are `E`
(25T aluminium disc horn listing values, HD-002 hold) and must be measured on
the received part before the leg pocket and screw holes are printed.
"""
import math
from build123d import Axis, Compound, Location
from layout_axes import AXES

ROLL_Y, ROLL_Z = AXES['roll_y'], AXES['roll_z']
PITCH_X, PITCH_Z = AXES['pitch_x'], AXES['pitch_z']

# Servo envelope in its own frame: output axis at the case-bottom origin,
# +Z along the spline, long case direction +X (drawing, D unless noted).
SERVO_MASS_G = 34.8
CASE_X = (-12., 24.)
CASE_HALF_W = 7.5
CASE_H = 29.2
BOSS_TOP = 29.5               # S: Ø10.4 x 0.3 boss
SPLINE_TOP = 33.1
EAR_Z = (19.7, 21.7)
EAR_X = (-18.4, 30.4)
SLOT_X = (-15.3, 27.3)
SLOT_Y = (-3.75, 3.75)
SLOT_R = 2.1
NOZZLE_TIP_X = -15.5          # S: lead nozzle tip on the shaft-end face
NOZZLE_Z = (1.7, 4.2)

# Clearances between the coupled parts and the servo boss.
OUTPUT_GAP = .3

# --- Roll ---------------------------------------------------------------
# The servo case sits 1.0 mm in front of the rear cover's inner face (X
# -113.4), which fixes the 17 mm coupler's front face at X-65.6. The rear
# bearing moves 4.4 mm forward (spacing 22 -> 17.6) so the cartridge's rear
# face and retainer plate keep 1.0 / 0.9 mm from the turning coupler.
COUPLER_LENGTH = 17.0                     # D: STEP spline face to bore end
COUPLER_SPLINE_DEPTH_TO_FLOOR = 4.5       # D: spline face to the bore floor
COUPLER_FRONT_X = -65.6
ROLL_BEARING_X = (-43., -60.6)
CARTRIDGE_X = (COUPLER_FRONT_X + 1.0, -39.)
CARTRIDGE_SCREW_X = (-57.5, -46.)
COUPLER_SPLINE_FACE_X = COUPLER_FRONT_X - COUPLER_LENGTH
ROLL_CASE_BOTTOM_X = COUPLER_SPLINE_FACE_X - OUTPUT_GAP - BOSS_TOP
ROLL_EAR_X = (ROLL_CASE_BOTTOM_X + EAR_Z[0], ROLL_CASE_BOTTOM_X + EAR_Z[1])
COUPLER_FLOOR_X = COUPLER_SPLINE_FACE_X + COUPLER_SPLINE_DEPTH_TO_FLOOR
SPINDLE_X = (COUPLER_FLOOR_X + 3. + .5, -40.)   # 3 mm M3 head + 0.5 mm
# Mount plate on the ears' front faces, joined to the torsion box rear wall.
ROLL_PLATE_T = 5.
ROLL_PLATE_HALF_Y = 18.7
ROLL_PLATE_Z = (ROLL_Z - 31.4, ROLL_Z + 19.4)
ROLL_WINDOW_CLEAR = .3
# The C2 tray's service path (lift +Z27, then out to -X) passes the plate's
# -Y upper corner: above Z 51.5 the plate stops at Y -14.7 (tray edge Y-16.2).
ROLL_PLATE_C2_RELIEF = dict(y_max=-14.7, z_min=51.5)

# --- Pitch --------------------------------------------------------------
# Long case side down-rear at 244 deg in XZ (from +X towards +Z): the only
# clocking that clears the roll-swept cradle with >= 1 mm (D-049 sweep map).
PITCH_CLOCK_DEG = 244.
HORN = dict(  # E: 25T aluminium disc horn, listing values; HD-002 hold
    disc_r=10., disc_t=2., hub_r=5., hub_t=2.5, bore_r=2.95, web=1.1,
    pcd_r=7., holes_deg=(45., 135., 225., 315.), screw_r=1.6, mass_density=2.70e-3)
HORN_POCKET_DEPTH = .6        # radial location in the leg; 0.6 < 1 mm frame float
LEG_INNER_Y = 52.
HORN_TOP_Y = LEG_INNER_Y + HORN_POCKET_DEPTH
HORN_BOTTOM_Y = HORN_TOP_Y - HORN['disc_t'] - HORN['hub_t']
PITCH_CASE_BOTTOM_Y = HORN_BOTTOM_Y - OUTPUT_GAP - BOSS_TOP
PITCH_EAR_Y = (PITCH_CASE_BOTTOM_Y + EAR_Z[0], PITCH_CASE_BOTTOM_Y + EAR_Z[1])
# 1.0 mm wall round the horn pocket; at r 12 the pad's top edge came within
# 0.48 mm of the skin at roll -21 deg (committed head: 0.72 mm).
LEG_PAD_R = 11.2
LEG_HORN_POCKET_R = HORN['disc_r'] + .2
LEG_CENTRE_HOLE_R = 3.25
M3_CLEAR_R, M3_HEAD_CBORE_R, M3_HEAD_CBORE_D = 1.7, 3.1, 1.8
# Collar: a 6 mm XZ-plane plate under the ears, joined to the box front wall.
COLLAR_T = 6.
COLLAR_WINDOW_CLEAR = .3
COLLAR_BAND = (7.8, 13.)      # rear-up band beside the case, local Y
COLLAR_FLOOR = (-68.5, -51., 16.9, 21.9)   # X, Z of the keel-to-collar floor

# M2 ear joint: ISO 7380 M2 x 6 on an ISO 7089 M2.5 washer (Ø2.7/Ø6 x 0.5)
# into the head's M2 x 3 insert. The 4.2 mm slot sits 3.3 mm from the case
# end, so an M3 insert would leave 0.8-1.0 mm of wall beside the case window.
# The Ø3.5 M2 head is smaller than the slot; a 0.3 mm M2 washer would span the
# slot with 1 mm unsupported and dish under preload. The Ø6 washer bears
# 0.9 mm beyond the slot edge and stops 0.3 mm short of the case end wall at
# nominal (tab-root fillet unmeasured).
WASHER = dict(r_in=1.35, r_out=3.0, t=.5)

# Yoke legs (D-050 restyle). Both legs share one faceted outline. D-049 used
# the +Y leg's free corridor directly: the R/P swept volume in its Y 52-58 slab
# (roll +/-21 in 1.5 deg, pitch -25..+43 in 1 deg, 0.6 mm samples) less 1.5 mm,
# traced in 1 mm steps. That left stair-stepped edges, a ledge out to dx +10 at
# disc+15 and a 24.5 x 15 mm box foot, all visible between the disc and the
# head. Here the corridor is eroded 0.5 mm and simplified at 0.45 mm (shapely),
# so every facet lies inside it, and the ledge and box give way to a plinth.
# The fit is unioned with the pre-D-049 leg (free by construction: the skin,
# ear and cradle reliefs are cut by it), which carries the waist's front edge
# out to dx -13.5. The waist and the arm keep that full width: the leg's
# in-plane stiffness goes with width cubed, and narrower drawn outlines
# screened at 24-32 N*m/rad against D-049's 49.9. (dx, dz) from the pitch
# axis; None = disc top.
LEG_OUTLINE_DXDZ = (
    (-21.5, None), (-5.5, None), (-9.0, -65.05), (-11.51, -61.21),
    (-13.5, -58.9), (-13.5, -37.27), (9.5, -12.66), (9.5, 4.68),
    (-9.38, 4.68), (-16.3, -4.16), (-31.49, -12.0), (-31.49, -27.64),
    (-25.69, -33.61), (-25.69, -37.03), (-28.69, -39.13), (-28.69, -40.7),
    (-21.69, -54.7), (-21.5, -60.34))
# Plinth (Y 48-58, mirrored on -Y): a ruled loft from the D-049 foot's plan on
# the disc top to 12.4 mm wide at disc+15, inside the foot box that D-049
# showed free. Its outer face keeps the leg's vertical rear edge (r 61.8 at the
# outer face, inside the disc's flat top at r 61.9).
LEG_PLINTH = dict(base=((-29.99, 48.), (-5.49, 48.), (-5.49, 58.), (-21.5, 58.)),
                  top=(-21.5, -9.0, 48.5, 58.), h=15.)
# Inboard gusset (Y 48.5-52) on the plinth: the D-049 inboard-rib corridor
# (that slab's own free space) fitted the same way.
LEG_GUSSET = dict(y=(48.5, 52.), dxdz=(
    (-19.58, -65.05), (-12.2, -65.05), (-17.58, -59.76), (-17.58, -55.34),
    (-13.13, -50.89), (-17.08, -49.96), (-17.08, -49.26), (-18.58, -48.36),
    (-18.58, -46.55), (-25.5, -47.42), (-19.58, -59.34)))
# Outer-face spine recess and its inlay, ending at disc+30.5 so the waist keeps
# a >= 1.2 mm lip in front of the pocket.
LEG_SPINE_FACET = dict(recess=((-20.1, 9.), (-16.2, 13.), (-16.4, -46.), (-20.1, -49.5)),
                       inlay=((-19.8, 9.75), (-16.5, 13.15), (-16.7, -46.72), (-19.8, -49.65)))
# The first two points of each are heights above the disc top, the last two dz.
# The +Y ear's trim stack (R) passes the leg's outer face at roll -21 deg,
# pitch +13..+43 (0.4 mm before D-049; the A0 shift closed it). A 1.2 mm deep
# band (floor Y 56.8) along that contact path, inside the head and above the
# styling rail, keeps it clear: (dx, dz) corners about the pitch axis.
LEG_TRIM_RELIEF = dict(band=((-2.5, -37.3), (-2.5, -26.0), (-27.5, -13.7), (-27.5, -24.6)), y=(56.8, 58.2))
# Both legs: the -Y ear's stack follows the mirrored path (0.075 mm after the
# A0 shift; committed head 0.17 mm), so the band and rail apply to both.
# Both legs (D-050; +Y only in D-049): a 0.5 mm outer-face step at the
# spine's rear edge, where the skin passes at roll -/+21 deg, pitch -25
# (committed head: 0.72 mm; the D-050 -Y leg without it: 0.77 mm).
LEG_SKIN_STEP = dict(dx=(-27.5, -24.5), dz=(-38.5, -30.5), y=(57.5, 58.2))
# The outer-face styling rails stop at Z disc+32.5 (was about disc+48): their
# upper halves, under the head, came within 0.06 / 0.20 mm of the ears' amber
# rings at roll -/+21 deg after the A0 shift (committed head: 0.22 / 0.35 mm).
LEG_RAIL_TOP_ABOVE_DISC = 32.5


def u_v(deg=PITCH_CLOCK_DEG):
    """Unit vectors in XZ of the servo's local +X (long side) and +Y."""
    a = math.radians(deg)
    ux, uz = math.cos(a), math.sin(a)
    return (ux, uz), (uz, -ux)


def place_roll(shape):
    """Servo local frame -> head: spline +X on the roll axis, long side -Z."""
    return shape.rotate(Axis.Y, 90).moved(Location((ROLL_CASE_BOTTOM_X, ROLL_Y, ROLL_Z)))


def place_pitch(shape):
    """Servo local frame -> head: spline +Y on the pitch axis, long side at PITCH_CLOCK_DEG."""
    return shape.rotate(Axis.X, -90).rotate(Axis.Y, -PITCH_CLOCK_DEG).moved(
        Location((PITCH_X, PITCH_CASE_BOTTOM_Y, PITCH_Z)))


def roll_local_to_head(x, y, z):
    return (ROLL_CASE_BOTTOM_X + z, ROLL_Y + y, ROLL_Z - x)


def pitch_local_to_head(x, y, z):
    (ux, uz), (vx, vz) = u_v()
    return (PITCH_X + x * ux + y * vx, PITCH_CASE_BOTTOM_Y + z, PITCH_Z + x * uz + y * vz)


def slots(local_to_head, z):
    return [local_to_head(x, y, z) for x in SLOT_X for y in SLOT_Y]


def place_coupler(shape):
    """goBILDA STEP frame -> head. STEP axis is +Y at (X-57.36, Z18.34); the
    spline face is STEP Y 6.77 and the clamp boss is +Z. Head: spline face at
    COUPLER_SPLINE_FACE_X, axis +X on the roll axis, clamp boss up at neutral."""
    s = shape.moved(Location((57.36, -6.77, -18.34))).rotate(Axis.Z, -90)
    return s.moved(Location((COUPLER_SPLINE_FACE_X, ROLL_Y, ROLL_Z)))
