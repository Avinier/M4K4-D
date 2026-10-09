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

# +Y yoke leg stiffening (D-049). The leg now carries the pitch reaction from
# the horn to the disc; the old 8 x 6 mm spine screened at 8.6 N*m/rad in the
# leg FEA. The widened in-plane outline (Z disc+15 to the old leg top) is the free corridor of the R/P swept
# volume in the leg's own Y 52-58 slab (roll +/-21 in 1.5 deg, pitch -25..+43
# in 1 deg, 0.6 mm surface samples), less 1.5 mm, smoothed over +/-2 mm in Z,
# as (dx, dz) from the pitch axis. The foot fills the free neck below Z
# disc+15 inside the disc radius. Exact posed checks re-verify it.
LEG_SPINE_DXDZ = [(-31.99, -64.82), (-31.99, -63.82), (-31.99, -62.82), (-31.99, -61.82), (-22.69, -60.82), (-21.69, -59.82), (-21.69, -58.82), (-21.69, -57.82), (-21.69, -56.82), (-22.19, -55.82), (-22.19, -54.82), (-22.69, -53.82), (-23.19, -52.82), (-23.69, -51.82), (-24.19, -50.82), (-24.69, -49.82), (-25.19, -48.82), (-25.69, -47.82), (-26.19, -46.82), (-26.69, -45.82), (-27.19, -44.82), (-27.69, -43.82), (-28.19, -42.82), (-28.69, -41.82), (-29.19, -40.82), (-29.19, -39.82), (-29.19, -38.82), (-27.19, -37.82), (-26.19, -36.82), (-26.19, -35.82), (-26.19, -34.82), (-26.19, -33.82), (-27.19, -32.82), (-28.19, -31.82), (-29.19, -30.82), (-30.19, -29.82), (-31.19, -28.82), (-31.99, -27.82), (-31.99, -26.82), (-31.99, -25.82), (-31.99, -24.82), (-31.99, -23.82), (-31.99, -22.82), (-31.99, -21.82), (-31.99, -20.82), (-31.99, -19.82), (-31.99, -18.82), (-31.99, -17.82), (-31.99, -16.82), (-31.99, -15.82), (-31.99, -14.82), (-31.99, -13.82), (-31.99, -12.82), (-31.99, -11.82), (-31.19, -10.82), (-29.19, -9.82), (-27.19, -8.82), (-24.69, -7.82), (-22.69, -6.82), (-20.69, -5.82), (-18.19, -4.82), (-16.69, -3.82), (-16.19, -2.82), (-15.19, -1.82), (-14.19, -0.82), (-13.69, 0.18), (-12.69, 1.18), (-12.19, 2.18), (-11.19, 3.18), (-10.19, 4.18), (-9.69, 5.18), (10.0, 5.18), (10.0, 4.18), (10.0, 3.18), (10.0, 2.18), (10.0, 1.18), (10.0, 0.18), (10.0, -0.82), (10.0, -1.82), (10.0, -2.82), (10.0, -3.82), (10.0, -4.82), (10.0, -5.82), (10.0, -6.82), (10.0, -7.82), (10.0, -8.82), (10.0, -9.82), (10.0, -10.82), (10.0, -11.82), (10.0, -12.82), (9.31, -13.82), (8.31, -14.82), (7.31, -15.82), (6.31, -16.82), (5.31, -17.82), (4.31, -18.82), (3.81, -19.82), (2.81, -20.82), (1.81, -21.82), (0.81, -22.82), (-0.19, -23.82), (-1.19, -24.82), (-2.19, -25.82), (-2.69, -26.82), (-3.69, -27.82), (-4.69, -28.82), (-5.69, -29.82), (-6.69, -30.82), (-7.69, -31.82), (-8.69, -32.82), (-9.19, -33.82), (-10.19, -34.82), (-11.19, -35.82), (-12.19, -36.82), (-13.19, -37.82), (-14.19, -38.82), (-15.19, -39.82), (-15.19, -40.82), (-15.19, -41.82), (-15.19, -42.82), (-15.19, -43.82), (-15.19, -44.82), (-14.19, -45.82), (-11.69, -46.82), (-11.69, -47.82), (-11.69, -48.82), (-11.69, -49.82), (-12.19, -50.82), (-13.19, -51.82), (-14.19, -52.82), (-14.69, -53.82), (-14.69, -54.82), (-14.69, -55.82), (-14.69, -56.82), (-14.19, -57.82), (-13.19, -58.82), (-12.19, -59.82), (-11.19, -60.82), (-9.69, -61.82), (-2.19, -62.82), (10.0, -63.82), (10.0, -64.82)]
# Inner face at Y 48: from Y 46 its top corner came within 0.73 mm of the
# front bezel at roll -21 deg, pitch +43.
LEG_FOOT = dict(dx=(-29.99, -5.49), y=(48., 58.), h=15., r=61.5)
# Inboard rib (Y 48.5-52) on the spine from the foot to Z ~0: the free
# corridor of that slab, generated the same way on the final axes.
LEG_INBOARD_RIB = dict(y=(48.5, 52.), dxdz=[[-31.99, -65.05], [-31.99, -64.55], [-20.08, -64.05], [-20.08, -63.55], [-20.08, -63.05], [-20.08, -62.55], [-20.08, -62.05], [-20.08, -61.55], [-20.08, -61.05], [-20.08, -60.55], [-20.08, -60.05], [-20.08, -59.55], [-20.58, -59.05], [-20.58, -58.55], [-21.08, -58.05], [-21.08, -57.55], [-21.58, -57.05], [-21.58, -56.55], [-22.08, -56.05], [-22.08, -55.55], [-22.58, -55.05], [-22.58, -54.55], [-23.08, -54.05], [-23.08, -53.55], [-23.08, -53.05], [-23.58, -52.55], [-23.58, -52.05], [-24.08, -51.55], [-24.08, -51.05], [-24.58, -50.55], [-24.58, -50.05], [-25.08, -49.55], [-25.08, -49.05], [-25.58, -48.55], [-25.58, -48.05], [-26.08, -47.55], [-26.08, -47.05], [-24.08, -46.55], [-21.58, -46.05], [-18.08, -46.05], [-18.08, -46.55], [-18.08, -47.05], [-18.08, -47.55], [-18.08, -48.05], [-17.08, -48.55], [-16.58, -49.05], [-16.58, -49.55], [-14.08, -50.05], [-12.58, -50.55], [-12.58, -51.05], [-13.08, -51.55], [-13.58, -52.05], [-14.08, -52.55], [-14.58, -53.05], [-15.08, -53.55], [-15.58, -54.05], [-16.08, -54.55], [-16.58, -55.05], [-17.08, -55.55], [-17.08, -56.05], [-17.08, -56.55], [-17.08, -57.05], [-17.08, -57.55], [-17.08, -58.05], [-17.08, -58.55], [-17.08, -59.05], [-17.08, -59.55], [-16.58, -60.05], [-16.08, -60.55], [-15.58, -61.05], [-15.08, -61.55], [-14.58, -62.05], [-14.08, -62.55], [-13.58, -63.05], [-13.08, -63.55], [-12.08, -64.05], [-11.08, -64.55], [-9.08, -65.05]])
# The +Y ear's trim stack (R) passes the leg's outer face at roll -21 deg,
# pitch +13..+43 (0.4 mm before D-049; the A0 shift closed it). A 1.2 mm deep
# band (floor Y 56.8) along that contact path, inside the head and above the
# styling rail, keeps it clear: (dx, dz) corners about the pitch axis.
LEG_TRIM_RELIEF = dict(band=((-2.5, -37.3), (-2.5, -26.0), (-27.5, -13.7), (-27.5, -24.6)), y=(56.8, 58.2))
# Both legs: the -Y ear's stack follows the mirrored path (0.075 mm after the
# A0 shift; committed head 0.17 mm), so the band and rail apply to both.
# +Y only: a 0.5 mm outer-face step at the widened spine's rear edge, where
# the skin passes at roll -21 deg, pitch -25 (committed head: 0.72 mm).
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
