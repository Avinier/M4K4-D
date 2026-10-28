"""RP-03 integrated body/chassis Layout 02.

Coordinate frame: millimetres; origin on ground at the drive-axle line and
robot centre plane; +X forward, +Y robot-left, +Z up.

The RP-01 Layout 04 head is composed from its live Python source; its yaw
datum, A0, mass and turntable size are read from that layout's generated files. Purchased
STEP geometry is imported through cadgen.step_scene.import_step.
"""

from __future__ import annotations

import functools
import importlib
import json
import math
import sys
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    Color,
    Compound,
    Cone,
    Cylinder,
    Kind,
    Location,
    Plane,
    Polygon,
    RectangleRounded,
    Sphere,
    extrude,
    loft,
    offset,
)
from cadgen import srgb
from cadgen.assembly import AssemblyHelper
try:
    # text-to-cad 0.4.28 runtime: cached imported-STEP path.
    from cadgen.step_scene import import_step
except ImportError:  # repository's older CAD venv compatibility for report scripts
    from build123d import import_step


HERE = Path(__file__).resolve().parent
# This v1 starting copy still composes the prototype's purchased STEP files and
# Layout 04 head. Keep these explicit until the chassis-only CAD is separated.
PROTOTYPE_CAD_ROOT = HERE.parents[3] / "02-prototypes" / "RP-06-cad"
PURCHASED = PROTOTYPE_CAD_ROOT / "body-chassis" / "layout-01" / "references" / "purchased"
# Vendor or vendor-derived STEPs added in 03-build (see purchased/README.md).
V1_PURCHASED = HERE / "purchased"
# Adafruit #3297 leaves in adafruit_3297_drv8833.step export order.
ADAFRUIT_3297_LEAVES = ("PCB", "U1_HTSSOP16", "U1_LEADS_A", "U1_LEADS_B", "R1_1206", "R2_1206",
                        "C1_0805", "C2_0805", "C3_0805", "C4_0805", "Q1_SOT23", "J1_TERMINAL_BLOCK")
HEAD_DIR = PROTOTYPE_CAD_ROOT / "head" / "layout-04"
# Drive wheel (D-008, D-009): rim, handed TPU tyres, clamp ring, hub cap and their
# hardware are modelled once in wheel/wheel_model.py; wheel_assembly() places them
# on the chassis and adds the D-007 stub.
sys.path.insert(0, str(HERE / "wheel"))
import wheel_model as WHEEL_MODEL  # noqa: E402

HEAD_MODEL = None


def _load_head_model():
    """Load RP-01 Layout 04 lazily from source for the actual CAD build.

    Report/check scripts can import this module without paying the full head
    build dependency cost. During `gen`, the text-to-cad runtime supplies the
    current cached STEP importer required by Layout 04.
    """
    global HEAD_MODEL
    if HEAD_MODEL is not None:
        return HEAD_MODEL
    if str(HEAD_DIR) not in sys.path:
        sys.path.insert(0, str(HEAD_DIR))
    for module_name in (
        "layout_axes",
        "motion_envelope",
        "layout_model",
        "details",
        "mass_layout",
        "harness",
        "optics",
        "inspection_scene",
        "write_dimensions",
    ):
        importlib.import_module(module_name)
    HEAD_MODEL = sys.modules["layout_model"]
    return HEAD_MODEL


# ---------------------------------------------------------------------------
# Central parameters
# ---------------------------------------------------------------------------

LAYOUT_ID = "RP03_BODY_CHASSIS_LAYOUT02"
LAYOUT_REV = "layout-02.0"

# Palette follows RP-01 Layout 03 so the whole robot reads as one assembly.
IVORY = "#E3DDC9"
SLATE = "#87949A"
SLATE_DARK = "#707D82"
FRAME_BLUE = "#86A1A8"
PANEL_WARM_GRAY = "#C5C0AD"
BRONZE = "#C38A47"
AMBER = "#B88636"
STEEL = "#B7BFC0"
RUBBER = "#343B40"
PCB_GREEN = "#2D8C53"

TRACK = 170.0
AXLE_Z = 42.0
WHEEL_OD = 84.0
WHEEL_WIDTH = 24.0
WHEEL_WELL_RADIAL_CLEARANCE = 4.0
WHEEL_WELL_SIDE_CLEARANCE = 4.0
WHEEL_CENTER_L = (0.0, TRACK / 2.0, AXLE_Z)
WHEEL_CENTER_R = (0.0, -TRACK / 2.0, AXLE_Z)
WHEEL_INNER_FACE_Y = TRACK / 2.0 - WHEEL_WIDTH / 2.0

# Axle stack (RP03-CAD-05), per side, as |Y| from the centre plane. The
# gearmotor's output face bolts to a 5 mm motor plate; a bolt-on printed
# housing carries a 688 ZZ pair and reaches into a pocket in the dished wheel,
# so nothing stationary sits inside the wheel's swept volume. A turned steel
# stub runs in the bearings, takes the motor's 4 mm D-shaft on a set screw at
# its inboard end and bolts to the wheel web by its flange (D-007). No axle
# crossmember: coaxial motors fill the axle line, so cheek plates carry each
# rail round its gearbox to the flange instead.
# Gearmotor: ThinkRobotics MOT3001-6V230RPM (generic JGA25-370 6 V with 11 PPR
# Hall encoder, ~26:1 inferred from the family's ~6,000 rpm base speed), the
# build choice in 03-build decisions.md D-003. No vendor STEP; modelled from
# the ThinkRobotics/JGA25 dimension drawing: O25 gearbox (length L varies 19-27
# mm with ratio; 21 mm assumed), O24.4 x 31 can, encoder board ~9 mm behind the
# can (40 mm REF can + encoder), O7 x 2.5 bushing boss, O4 D-shaft 12 mm from
# the faceplate with an 8 mm flat 3.5 mm across. The 6-pin encoder/motor
# connector sits on the board edge and is clocked rearward (-X).
# The face screw pattern is NOT on the drawing: 2 x M3 at +-8.5 mm is the
# common JGA25 pattern and is carried unverified, with an assumed 5 mm tapped
# depth. Measure spacing, thread, depth and gearbox length on the received
# unit before releasing the flange.
MOTOR_MODEL = "THINKROBOTICS_MOT3001_6V230RPM"
MOTOR_FACE_Y = 69.0
MOTOR_GEARBOX_RADIUS = 12.5
MOTOR_GEARBOX_LENGTH = 21.0  # assumed; drawing gives L = 19-27 by ratio
MOTOR_CAN_RADIUS = 12.2
MOTOR_CAN_LENGTH = 31.0
MOTOR_ENCODER_LENGTH = 9.0  # 40 mm REF (can + encoder) less the 31 mm can
MOTOR_ENCODER_HUB_RADIUS = 7.0  # O14 magnet/hub on the drawing
MOTOR_ENCODER_PCB_THICKNESS = 1.6
MOTOR_CONNECTOR_X = (-21.0, -12.2)  # 6-pin header + mated plug, radial off the board edge, rearward
MOTOR_CONNECTOR_HALF_Z = 7.0
MOTOR_SHAFT_RADIUS = 2.0
MOTOR_SHAFT_LENGTH = 12.0  # JGA25 drawing, from the faceplate
MOTOR_SHAFT_FLAT_LENGTH = 8.0
MOTOR_SHAFT_FLAT_ACROSS = 3.5
MOTOR_PILOT_RADIUS = 3.5  # O7 bushing boss locates the motor in the flange
MOTOR_PILOT_LENGTH = 2.5
MOTOR_SCREW_OFFSET = 8.5  # face M3 holes (unverified), on the axle line
MOTOR_SCREW_XZ = ((-MOTOR_SCREW_OFFSET, 0.0), (MOTOR_SCREW_OFFSET, 0.0))  # (X, Z - AXLE_Z)
MOTOR_SCREW_TAP_RADIUS = 1.25  # M3 tap drill
MOTOR_SCREW_HOLE_DEPTH = 5.0  # assumed; not published
# Axle stack (D-007, 03-build/01-chassis/v1/research/axle-stack.md), |Y| from the
# centre plane. The motor floats on its face screws until it has aligned to
# the stub, then they are tightened through key holes in the housing.
MOTOR_SCREW_LENGTH = 6.0  # ISO 7380 M3 x 6 button head (D-030; was DIN 7984 low head): 2.8 mm clamp + 3.2 mm thread
MOTOR_SCREW_HEAD_RADIUS = 2.85  # O5.7 x 1.65 button head, seated on the counterbore floor
MOTOR_SCREW_HEAD_HEIGHT = 1.65
MOTOR_SCREW_CLEAR_RADIUS = 1.8  # O3.6: +-0.3 mm float for self-alignment
MOTOR_SCREW_CBORE = (3.25, 2.2)  # O6.5 x 2.2 counterbore; head sits 0.2 below the plate face
AXLE_FLANGE_Y = (MOTOR_FACE_Y, 74.0)  # 5 mm motor plate (was 2 mm + 2 mm diaphragm)
AXLE_FLANGE_HALF_X = 17.0
AXLE_FLANGE_Z = (27.0, 57.0)
AXLE_PLATE_SQUARE_END_Y = 71.5  # square part stays 1.5 mm off the wheel's inner face (|Y| 73)
AXLE_PLATE_HUB_RADIUS = 16.5  # round part, 71.5-74, inside the wheel pocket with 1.5 mm radial gap
AXLE_PLATE_RECESS = (6.0, 2.5)  # radius, depth: floor at the pilot end (|Y| 71.5); stub end and set screw run 1.5 mm clear
AXLE_PILOT_HOLE_RADIUS = 3.8  # O7.6 on the O7 pilot: 0.3 mm radial float
AXLE_INSERT_RADIUS = 2.0  # M3 x 4 short heat-set insert, O4.0 envelope
AXLE_INSERT_DEPTH = 4.0
AXLE_HOUSING_Y = (74.0, 86.35)  # bolt-on printed bearing housing; bearings stand 0.15 proud
AXLE_HOUSING_RADIUS = 16.0  # 2.0 mm radial to the wheel pocket; 2.3 mm wall outside the screw holes
AXLE_HOUSING_SCREW_R = 12.0
AXLE_HOUSING_SCREW_ANGLES = (45.0, 135.0, 225.0, 315.0)  # degrees in XZ from +X; diagonals keep the inserts >= 4.5 mm off the plate edges
AXLE_HOUSING_INNER_RADIUS = 6.25  # inboard cavity and outer-ring shoulder (O12.5), 74-76.51
AXLE_KEY_HOLE_RADIUS = 1.3  # O2.6 axial key access to the face screws, opened into the bearing bore as a slot (0/180 deg, off the vertical load line)
AXLE_WINDOW_RADIUS = 1.7  # O3.4 radial set-screw slot at +Z, open to the housing base so the screw can be fitted
AXLE_CAP_Y = (86.51, 87.71)  # 1.2 mm aluminium retaining cap on the outer rings
AXLE_CAP_SCREW_LENGTH = 18.0  # ISO 7380 M3 x 18 button head through cap and housing into the insert
AXLE_BUTTON_HEAD = (2.85, 1.65)  # ISO 7380 M3 head radius, height
BEARING_MODEL = "688ZZ"  # OnlyScrews listing: 8 x 16 x 5, double metal shielded
BEARING_BORE_RADIUS = 4.0
BEARING_OD_RADIUS = 8.0
BEARING_WIDTH = 5.0
BEARING_Y = (79.01, 84.01)  # bearing centres: 76.51-81.51 and 81.51-86.51, faces touching
BEARING_SEAT_Y = (76.51, 86.51)
SET_SCREW_Y = 74.8  # ISO 4029 M3 cup point on the D-flat (+Z); tap-drill edge stays 0.46 mm from the first 688ZZ face
SET_SCREW_LENGTH = 2.5  # ISO 4029 M3 x 3 faced down 0.5 mm at the hex end (D-030; 2.5 is not a standard length); flush with the O8 stub, 1.54 mm swept to the face-screw heads
# Stub: one turned EN8 part. Ø8 through the bearings, Ø9.5 shoulder, Ø24
# flange carrying three tapped M3 for the wheel, Ø10 spigot centring the wheel.
STUB_SHAFT_RADIUS = 4.0
STUB_SHAFT_Y = (73.0, 96.0)  # inboard end (1.5 mm off the motor pilot) to spigot tip; 8 mm on the motor shaft
STUB_BORE = (2.025, 82.0)  # O4.05 bore radius, bore end |Y|
STUB_SHOULDER = (4.75, 86.51, 91.0)  # radius, |Y| span
STUB_FLANGE = (12.0, 91.0, 93.0)  # radius, |Y| span
STUB_SPIGOT = (5.0, 93.0, 96.0)
STUB_CAP_TAP = (8.0, 9.5)  # D-033: M3 thread depth and tap-drill depth into the spigot end, for the hub-cap screw
WHEEL_SCREW_PCD_R = 8.0
WHEEL_SCREW_ANGLES = (30.0, 150.0, 270.0)  # between the rim's six spokes; mirrored in wheel/wheel_model.py
WHEEL_SCREW_LENGTH = 6.0  # ISO 7380 M3 x 6, 4 mm web + 2 mm flange thread
WHEEL_POCKET_RADIUS = 18.0  # 2.5 mm radial running gap to the housing
WHEEL_POCKET_FLOOR_Y = 93.0  # web 93-97; the stub flange turns inside the pocket
WHEEL_HUB_BORE_RADIUS = 5.0  # O10 H7 on the spigot
AXLE_CHEEK_X = (13.5, 17.0)  # |X| span; 1 mm off the gearbox, clear of the can
AXLE_CHEEK_Y = (50.0, MOTOR_FACE_Y)  # rail inner face to the flange
J04_RECESS = (2.95, 2.1)  # radius, depth of the head recess in each cheek
J04_SCREW_LENGTH = 8.0  # ISO 7380 M3 x 8 into the 6 mm rail insert (D-030; was DIN 7984)
MOTOR_RELIEF_HALF_X = 17.0  # deck relief and shell-floor slot over the motors
WHEEL_RUNNING_CLEARANCE_MIN = 1.5

BALL_CONTACT = (110.0, 0.0, 0.0)
BALL_DIAMETER = 25.4
# Pololu ball caster 1" (item 2691 rollers / 2692 bearings; India: Fab.to.Lab, MG Super Labs).
# Drawing 2691: O34 base 8.8 thick, 29 mm overall, O3.2 holes 12.2 mm apart (an equilateral
# triangle, so the bolt circle is 12.2/sqrt(3) = O14.1). STEP: build_ball_caster_step.py.
BALL_HOUSING_RADIUS = 14.25
BALL_NATIVE_HEIGHT = 29.0  # floor to the vendor flange's top (seating) face
BALL_HOLE_RADIUS = 12.2 / math.sqrt(3.0)  # bolt-circle radius, 7.04 mm
BALL_HOLE_ANGLES_DEG = (0.0, 120.0, 240.0)  # clocked so every screw head sits inside the pod pocket
BALL_FLANGE_OD = 34.0
BALL_FLANGE_THICKNESS = 8.8
BALL_CASTER_STEP = "pololu_ball_caster_1in_2691.step"
BALL_MOUNT_MODE = "FIXED_3HOLE_NON_INTERCHANGEABLE"
# J07 (D-011): the drawing's section view gives a 2.7 mm web at each hole with an
# O6.3 counterbore from the ball side; the imported STEP lacks it, so ball_transfer()
# cuts it. The base is screwed from below (housing and ball unsnapped) into seat inserts.
BALL_FLANGE_WEB = 2.7
BALL_FLANGE_CBORE_RADIUS = 3.15
BALL_SCREW_LENGTH = 8.0  # ISO 7380 M3 x 8 button head: 2.7 web + 5.3 in the seat insert
# CNC Kitchen M3 x 5.7 standard heat-set insert: O4.0 hole, O4.6 knurl (D-011, CH-033).
M3_INSERT_BORE_RADIUS = 2.0
M3_INSERT_OD_RADIUS = 2.3
M3_INSERT_LENGTH = 5.7

# Lean ball pod (RP03-CAD-04): one printed block seats directly on the
# vendor flange, replacing the angled rails, load collar, keeper clips and
# shroud. Its open-topped pocket carries the centred GP2Y above the three
# ball screws; a lid closes it. Pod and lid share one octagonal section that
# echoes the body's eight-sided end profile. A tongue of that section passes
# the shell's lower front band through one open-bottom notch to the front
# crossmember, which sits inside the shell.
BALL_POD_X = (92.0, 128.5)  # rear face on the front crossmember = flange rear edge, front face
BALL_POD_HALF_WIDTH = 17.5  # at the shell notch (x 92-104); the prow swells ahead of it
BALL_POD_LOWER_CHAMFER = 2.5
BALL_POD_UPPER_CHAMFER = 6.0
BALL_POD_Z0 = BALL_NATIVE_HEIGHT  # seat face = vendor flange top
BALL_POD_SEAT_THICKNESS = 6.0  # D-011: carries the three caster inserts; its top is the GP2Y seat (Z 35)
BALL_POD_LID_Z = (49.0, 51.0)  # lid bottom, lid top over the sensor belt (the lid rakes down ahead of it)
# Prow plan: (x, half width, top Z, upper chamfer). Straight through the shell notch, swelling to
# 49 mm across the GP2Y's mounting belt (x 111.8-119.4), then in to a 35.6 mm nose. D-011: the
# nose is one constant section from x 122.5 to the face, so the touch cap slides 3 mm rearward
# along it (the old raked taper jammed the cap after 0.7 mm).
BALL_POD_STATIONS = (
    (92.0, 17.5, 51.0, 6.0),
    (104.0, 17.5, 51.0, 6.0),
    (110.5, 24.5, 51.0, 9.0),
    (121.0, 24.5, 51.0, 9.0),  # belt held 1.2 mm past the ear slot's front end
    (122.5, 17.8, 51.0, 2.0),  # nose top at the lid top: the real GP2Y body runs level to its lens face (Z 48)
    (128.5, 17.8, 51.0, 2.0),
)
BALL_POD_NOSE_X0 = BALL_POD_STATIONS[-2][0]  # start of the constant nose section
# Lid underside in XZ: level at Z 49, 1 mm over the GP2Y body to the pod face. (The D-011
# step down over a "lens hood" came from the misread A41 placement.)
BALL_POD_LID_UNDERSIDE = ((80.0, 49.0), (129.0, 49.0))
# Vestigial since the GP2Y ears are trimmed (D-027); kept so the pod print is unchanged.
# The GP2Y's ear flange (|y| 22.25, Z 35-36.6) must lift straight out, so its slots
# (x0, x1, |y| inner, |y| outer, z0, z1) run up to the lid and open through the upper chamfer
# as a window. D-011 holds the belt's full width 1.2 mm past the slot's front end (x 121.0);
# the old taper began at the slot end and left a 0.40 mm sliver there.
BALL_POD_EAR_SLOTS = (
    (111.4, 119.8, 14.6, 22.9, 35.0, 49.0),
    (111.4, 119.8, 14.6, 30.0, 42.0, 49.0),  # clears the chamfer wedge outside the window (was 0.5 mm)
)
BALL_POD_POCKET = (BALL_POD_X[0] + 3.0, 15.5)  # pocket rear x, half-width; open front and top
BALL_POD_POCKET_NECK = (42.9, 12.3)  # behind the belt: full width to Z 42.9, 45 deg in to |y| 12.3 (1.2 mm skin at Z 49)
BALL_POD_NECK_X1 = 109.0  # neck ends ahead of the GP2Y body (x 109.1), which lifts out through the full-width pocket
BALL_POD_SCREWS_YZ = ((10.0, 42.0), (-10.0, 42.0))  # M3 into crossmember inserts, driven from the pocket
BALL_POD_SCREW_LENGTH = 8.0  # ISO 7380 M3 x 8: 3 mm pod wall + 5 mm in the crossmember insert
# J10-8 cable (D-011): a round-cornered floor channel leaves through the pod's back wall
# below the crossmember (Z 32-35); a side groove brings the Hall board leads to it.
POD_CABLE_CHANNEL = (BALL_POD_X[0] - 1.0, 103.0, -3.0, 3.0, 32.0, 35.0)
POD_CABLE_CORNER = 1.0
POD_SWITCH_GROOVE = (100.0, 126.6, 9.5, 12.5, 33.5, 35.0)  # x0, x1, y0, y1, z0, z1: Hall board leads
# Lid retention (D-011, CH-003): a rear tongue drops into a groove in the pod's back wall that is
# open forward; the shell band holds the rear down (0.5 mm over the lid) and one M2 x 8
# countersunk thread-former holds the front. Removal: cap off, screw out, slide forward, lift.
LID_TONGUE = (93.5, 95.0, -6.0, 6.0, 47.0, 49.0)
LID_TONGUE_CLEARANCE = 0.2
LID_SCREW_XY = (111.8, -11.8)  # behind the GP2Y body (X 114.5), boss fused to the -Y pocket wall
LID_SCREW_LENGTH = 8.0
LID_SCREW_HEAD_RADIUS = 1.9  # M2 countersunk O3.8, 90 deg
LID_BOSS_RADIUS = 2.2
# Nose cable route to C3 carrier J10-8: under the crossmember, up a O5 bore through the
# crossmember and deck at (86, -31), then up beside the speaker cavity into the sensor trunk.
NOSE_CABLE_RISER_XY = (86.0, -31.0)
NOSE_CABLE_BORE_RADIUS = 2.5

# Body placement (RP03-CAD-06). Every body-side part (shell, panels, body
# frame, electronics, audio, harness, yaw stage and head) sits BODY_SHIFT_X
# forward of the drive axle; the drivetrain, ball, chassis and keel do not
# move. This carries ~1.96 kg forward and brings the whole-robot CoM from
# x +9.4 to about +21 mm (x/h ~0.20). Body-side X values below are written as
# their pre-shift value + BODY_SHIFT_X; BODY_AXIS_X is the body/yaw centre.
BODY_SHIFT_X = 16.0
# Adafruit #3297 boards (D-031): long side along Y, so the 17.8 mm width fits
# between the PCB-03 edge plugs (X 37) and the body-mount doglegs (X 58). Board X
# 38.5-56.3, |Y| 31.3-56.9, PCB underside Z 66.
DRIVER_CENTER_X = 31.4 + BODY_SHIFT_X
DRIVER_Y = 44.2  # inner posts clear the PCB-03 edge (|Y| 30) by 0.5 mm
DRIVER_PCB_Z = 66.0
DRIVER_TURN = 180.0  # deg about Z from the STEP: hole edge rearward on both boards; terminal block inboard on the left, outboard on the right
# J15B (D-030, D-031): each board's two plated O2.5 holes lie 2.54 mm in from one
# long edge, 20.32 mm apart. That edge faces rearward, so the posts (X 41.05)
# stay behind the body M4 feet (X 54). Each board sits on two printed posts on
# the front deck with M2.5 heat-set inserts.
DRIVER_HOLE_HALF_PITCH = 10.16
DRIVER_HOLE_X = DRIVER_CENTER_X - 8.89 + 2.54  # 41.05
DRIVER_POST_RADIUS = 3.5
DRIVER_INSERT = (1.95, 4.0)  # M2.5 x 4 brass insert, O3.9 OD, flush with the post top
DRIVER_SCREW = (6.0, 2.35, 1.5)  # M2.5 x 6 low button head: length, head radius, head height
# Motor-lead strain relief: one 2.5 mm tie bridge per side on the front deck,
# behind the boards where the leads drop to the motors.
DRIVER_TIE_LUG = (19.0, 24.0, 37.0, 43.0, 56.0, 59.0)  # x0, x1, |y0|, |y1|, z0, z1; tunnel along Y
HARNESS_MOTOR_BRANCH_X = 33.5  # X 30-37: across the deck behind the driver posts to the tie bridges, clear of the IMU (X 29)
BODY_AXIS_X = BODY_SHIFT_X
BODY_X_REAR = -74.0 + BODY_SHIFT_X
BODY_X_FRONT = 82.0 + BODY_SHIFT_X
BODY_Z_BOTTOM = 30.0
BODY_Z_TOP = 140.0
BODY_WIDTH_LOWER = 174.0
BODY_WIDTH_UPPER = 148.0
SHELL_THICKNESS = 2.4
# Every exterior skin (shell, service panels, wheel-arch pods) shares one
# see-through alpha so the internal packaging reads in every view.
SHELL_ALPHA = 0.28

# Layout 04 yaw stage (40 mm neck): the head's turntable disc stands proud of
# the body top; the yaw datum is the body-top plane on the yaw axis. Head A0,
# envelope, disc and yaw-carried mass are read from the head's generated files.
HEAD_AXES = json.loads((HEAD_DIR / "axes.json").read_text())
HEAD_ENVELOPE = json.loads((HEAD_DIR / "motion-envelope.json").read_text())
_HEAD_YAW_MASS = json.loads((HEAD_DIR / "mass-placement.json").read_text())["working"]["yaw"]
HEAD_YAW_DATUM = (BODY_AXIS_X, 0.0, 140.0)
HEAD_LOCAL_YAW = (HEAD_AXES["pitch_x"], 0.0, HEAD_ENVELOPE["body_top_z_mm"])
HEAD_ORIGIN_IN_CHASSIS = tuple(HEAD_YAW_DATUM[i] - HEAD_LOCAL_YAW[i] for i in range(3))
HEAD_LOCAL_COM = tuple(_HEAD_YAW_MASS["center_mm"])
HEAD_MASS_G = _HEAD_YAW_MASS["mass_g"]
HEAD_SWEEP_FLOOR_Z = HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_ENVELOPE["sweep_floor_z_mm"]
YAW_DISC_RADIUS = HEAD_ENVELOPE["yaw_disc"]["radius_mm"]
YAW_DISC_THICKNESS = HEAD_ENVELOPE["yaw_disc"]["thickness_mm"]
YAW_DISC_TOP_Z = HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_ENVELOPE["yaw_disc_top_z_mm"]
YAW_DISC_PLATE_BOTTOM_Z = YAW_DISC_TOP_Z - HEAD_ENVELOPE["yaw_disc"]["plate_mm"]
HEAD_CROWN_Z_LOCAL = 104.0
OVERALL_PHYSICAL_HEIGHT = HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_CROWN_Z_LOCAL
NECK_ALLOCATION = HEAD_ORIGIN_IN_CHASSIS[2] - BODY_Z_TOP

CHASSIS_RAIL_X0 = -46.0  # moved 16 mm forward with the body's rear wall
CHASSIS_RAIL_X1 = 92.0  # rails end at the front crossmember, inside the shell
FRONT_CROSSMEMBER_X = (80.0, 92.0)  # directly behind the ball flange, inside the shell
CHASSIS_RAIL_Y = 54.0
DECK_Z = 54.0

# Body/chassis service interface. Four M4 fasteners clamp body-frame feet to
# the chassis deck; diagonal locating pins carry repeatable assembly datum.
BODY_MOUNT_X = (-38.0 + BODY_SHIFT_X, 48.0 + BODY_SHIFT_X)
BODY_MOUNT_Y = (-48.0, 48.0)
BODY_MOUNT_CLEARANCE_RADIUS = 2.25
BODY_MOUNT_PAD_Z0 = 56.0
BODY_MOUNT_PAD_THICKNESS = 4.0
BODY_FRAME_LOWER_Z = 65.0
# Upper frame tops out at 134 so its cross-members carry the yaw adapter plate.
BODY_FRAME_UPPER_Z = 130.0
# The rear pin sits 10 mm further aft than the shift alone would put it, so
# its deck bore stays on the rear deck plate behind the motor relief.
BODY_LOCATING_POINTS = ((-43.0 + BODY_SHIFT_X, -42.0), (43.0 + BODY_SHIFT_X, 42.0))
BODY_MOUNT_POINTS = tuple((x, y) for x in BODY_MOUNT_X for y in BODY_MOUNT_Y)

# Service-panel interface. Each shell opening is the panel outline offset
# inward by PANEL_OVERLAP, so the panel laps a constant-width land all round.
# The panel perimeter repeats the body shell's eight-sided end profile, so
# the service breaks read as intentional facets rather than small
# trapezoidal inserts. Behind the shell end wall a separate internal frame
# carries four fused M3 bosses; front-access screws define removal direction.
PANEL_REVEAL = 1.0
PANEL_OVERLAP = 2.0
FRONT_SHELL_END_WIDTH_FACTOR = 0.92
REAR_SHELL_END_WIDTH_FACTOR = 0.90
SHELL_SIDE_EDGE_Z0 = BODY_Z_BOTTOM + 12.0
SHELL_SIDE_EDGE_Z1 = BODY_Z_TOP - 10.0
# The front panel starts above the chassis deck (top Z 56): the ball pod's
# tongue passes the front face below it, and the panel must lift off forward
# over the pod. The rear panel keeps a 12 mm lower
# margin. Both keep a 6 mm upper margin.
FRONT_PANEL_Z0 = 58.0
REAR_PANEL_Z0 = 42.0
PANEL_Z1 = 134.0
PANEL_LOWER_CORNER = 10.0
PANEL_UPPER_CORNER = 8.0
FRONT_PANEL_BOTTOM_WIDTH = 128.0
REAR_PANEL_BOTTOM_WIDTH = 126.0


def _panel_top_width(width_bottom, z0, shell_width_factor):
    """Top width whose straight side edge (between the clipped corners) is
    parallel to the shell end profile's side edge."""
    shell_slope = (BODY_WIDTH_LOWER - BODY_WIDTH_UPPER) * shell_width_factor / 2.0 / (
        SHELL_SIDE_EDGE_Z1 - SHELL_SIDE_EDGE_Z0
    )
    side_edge_height = (PANEL_Z1 - PANEL_UPPER_CORNER) - (z0 + PANEL_LOWER_CORNER)
    return width_bottom - 2.0 * side_edge_height * shell_slope


FRONT_PANEL_TOP_WIDTH = _panel_top_width(FRONT_PANEL_BOTTOM_WIDTH, FRONT_PANEL_Z0, FRONT_SHELL_END_WIDTH_FACTOR)
REAR_PANEL_TOP_WIDTH = _panel_top_width(REAR_PANEL_BOTTOM_WIDTH, REAR_PANEL_Z0, REAR_SHELL_END_WIDTH_FACTOR)
# Screw centres sit at least 7 mm inside the panel outline, so the 4.5 mm
# bosses clear the shell opening edge by 0.5 mm.
PANEL_FASTENER_MIN_INSET = 7.0
FRONT_PANEL_FASTENERS = ((-53.0, 67.0), (53.0, 67.0), (-46.0, 125.0), (46.0, 125.0))
REAR_PANEL_FASTENERS = ((-52.0, 51.0), (52.0, 51.0), (-44.0, 125.0), (44.0, 125.0))
# Internal frame: 2.4 mm plate behind the shell end wall, reaching 1 mm past
# the panel outline and 12 mm inside it. Bosses run from the panel's inner
# face through the frame and 2.6 mm beyond it for thread engagement.
PANEL_FRAME_THICKNESS = 2.4
PANEL_FRAME_OUTSET = 1.0
PANEL_FRAME_FLANGE = 12.0
PANEL_BOSS_RADIUS = 4.5
PANEL_BOSS_TAIL = 2.6
PANEL_SCREW_LENGTH = 8.0
# Front shell notch: the ball pod's tongue passes the lower front band, open
# to the bottom edge so the body still lowers onto the chassis.
FRONT_POD_NOTCH_CLEARANCE = 0.5

# Audio parts selected 2026-09-26 (RP03-CAD-11, ../../peripheral-selection.md): Visaton
# K 50 WP 8 ohm speaker, PCB-05 (MAX98357A + 2 x ADAU7002) and four PCB-06 boards with
# an Infineon IM73D122V01 each. The speaker's Ø50 x 18 mm outline and Ø46 cutout are
# Visaton's; its internal frame/basket/magnet split is estimated (no drawing read).
SPEAKER_CENTER = (72.0 + BODY_SHIFT_X, 0.0, 99.0)
SPEAKER_CONE_DIAMETER = 44.0
SPEAKER_BASKET_DIAMETER = 50.0
SPEAKER_DEPTH = 18.0
# Sealed back cavity: was 34 mm (X 63-97), which ran through the compute tray (X max 76) and
# the Pi 5 (X max 67), unchecked until RP03-CAD-11. Now X 77-97: 1 mm off the tray, ~46 cm3 gross.
SPEAKER_CAVITY_X = (77.0, 97.0)
SPEAKER_CAVITY_DEPTH = SPEAKER_CAVITY_X[1] - SPEAKER_CAVITY_X[0]
SPEAKER_CAVITY_CENTER_X = sum(SPEAKER_CAVITY_X) / 2.0
SPEAKER_FRONT_X = BODY_X_FRONT - 0.5  # frame face 0.5 mm behind the front panel's inner face
SPEAKER_CUTOUT_DIAMETER = 46.0
SPEAKER_FLANGE_DEPTH = 2.5
SPEAKER_BASKET_DEPTH = 9.0
SPEAKER_BASKET_REAR_DIAMETER = 30.0
SPEAKER_MAGNET_DIAMETER = 26.0
# PCB-05: 30 x 38 mm board plus parts reserve, 9 mm total, flat above the Pi 5's front end
# (Pi top Z 111.9) and forward of the cooler headroom, under the front upper cross (Z 126).
# The old 38 x 30 x 9 amplifier reservation at (49, 0, 103) sat inside the Pi 5 and cooler.
PCB05_CENTER = (60.0, 0.0, 118.5)
PCB05_SIZE = (30.0, 38.0, 9.0)
PCB05_BOARD_THICKNESS = 1.6
# PCB-06 mic boards: 12 x 8 x 1.0 mm, outer face on |Y| 70 against the port boot; the
# IM73D122 (4 x 3 x 1.2) sits on the port axis on the inboard face and a JST-SH 4-pin
# side-entry header (7 x 4.25 footprint, 2.95 tall) below it.
MIC_BOARD_OUTER_Y = 70.0
MIC_BOARD_SIZE = (12.0, 1.0, 9.5)  # 9.5 tall (was 8) so the 4.96 mm GH header clears the mic package
MIC_PACKAGE_SIZE = (4.0, 1.2, 3.0)
# PCB-07 IMU board: ICM-42688-P on 16 x 20 x 1.0 mm FR4, flat on the chassis deck crossbar
# (deck material X ~17.5-26.5 here; open over the motors and the battery on either side).
# Two M2 x 5 thread-forming screws at (IMU_SCREW_X, +-IMU_SCREW_HALF_Y) into the 4 mm deck.
IMU_BOARD_CENTER = (21.0, 0.0, DECK_Z + 2.0 + 0.5)
IMU_BOARD_SIZE = (16.0, 20.0, 1.0)
IMU_CHIP_SIZE = (3.0, 2.5, 0.91)
IMU_SCREW_X = 22.0
IMU_SCREW_HALF_Y = 7.5
# The GP2Y sits on the centreline in the ball pod, its face ahead of the ball
# contact, and looks forward through a window in the touch cap. RP-03
# physics.md §6 credits look-ahead from the leading (ball) contact, so a face
# ahead of it is credited and a face behind it is charged.
FRONT_RANGE_SENSOR_Y = 0.0
FRONT_RANGE_SENSOR_BOTTOM_Z = 35.0  # rests on the 6 mm pod seat (D-011); was on rails over the old screw heads
# Sharp datasheet E4-A00201EN: the lenses and the two O3.2 flange holes face the
# same way, the package is 13.5 deep along the optical axis, and the 13 mm body
# plus the S3B-PH connector on one edge make 18.9. The sensor lies lenses forward
# with the connector up; the lens centres are 6.5 above the body bottom. (The
# Layout 02 A41 placement read the connector as the front.)
FRONT_RANGE_LENS_ABOVE_BOTTOM = 6.5
FRONT_RANGE_SENSOR_Z = FRONT_RANGE_SENSOR_BOTTOM_Z + FRONT_RANGE_LENS_ABOVE_BOTTOM  # optical axis, Z 41.5
FRONT_RANGE_SENSOR_SIZE = (13.5, 44.5, 18.9)  # depth along the axis, flange width, height with connector
FRONT_RANGE_EAR_TRIM_HALF_WIDTH = 14.8  # D-027: both mounting ears cut off at the 29.5 mm body
FRONT_RANGE_POCKET_HALF_WIDTH = 15.0  # pod pocket ahead of X 122.1 (was 14.0 for the misread body)
FRONT_RANGE_LEAD_RESERVE_H = 2.0  # D-027: J10-8 wires soldered to the S3B-PH pins, bend above the header; 2.0 (was 3.0) keeps the lid hump (top Z 57.6) under the front panel's Z 58 lift-off path (D-029)
FRONT_RANGE_HUMP_CLEARANCE = 0.5
FRONT_RANGE_HUMP_WALL = 1.2
FRONT_RANGE_HUMP_REAR_RUN = 11.5  # lid slides 11 mm forward before it lifts (D-011); the lead runs back and down behind the sensor here
FRONT_RANGE_SENSOR_FACE_X = 128.0  # lens tip, 0.5 mm inside the pod front face
FRONT_RANGE_BODY_FRONT_X = 122.1  # start of the pod's narrow front pocket
FRONT_RANGE_WINDOW_SIZE = (27.0, 10.5)  # visor slit in the cap: width, height (full-round ends)
FRONT_RANGE_MIN_MM = 100.0
FRONT_RANGE_MAX_MM = 800.0  # GP2Y0A21YK0F rated range 100-800 mm
FRONT_RANGE_CYCLE_MS = 38.3
FRONT_RANGE_CYCLE_TOLERANCE_MS = 9.6
FRONT_RANGE_STOP_PATH_LIMIT_MS = 50.0
FRONT_RANGE_WINDOW_CLEARANCE = 1.0
# physics.md §6.2 / §10.2 required look-ahead from the ball contact.
FRONT_RANGE_REQUIRED_MM = {"0.50 m/s level": 179.0, "0.50 m/s 2deg downhill": 221.0, "0.70 m/s level": 289.0}
MICROPHONE_PORTS = (
    (38.0 + BODY_SHIFT_X, 70.0, 118.0, "FRONT_L"),
    (38.0 + BODY_SHIFT_X, -70.0, 118.0, "FRONT_R"),
    (-38.0 + BODY_SHIFT_X, 70.0, 108.0, "REAR_L"),
    (-38.0 + BODY_SHIFT_X, -70.0, 108.0, "REAR_R"),
)

# Head yaw stage under the proud disc. Nothing sits within PI_COOLER_HEADROOM
# of the Pi 5 active cooler. The adapter plate spans the upper-frame
# cross-members; the bearing and clock-spring reserve sit on it, and a 1:1
# spur pair under the disc plate couples an off-axis XC330-M181 yaw servo
# (129 rpm at 5 V vs 63 rpm peak yaw) with no speed reduction. The servo
# stands beside the cooler on +Y; a coupling shaft carries its output up to
# the pinion.
PI_COOLER_TOP_Z = 123.0  # headroom datum only; the real cooler now tops out near Z 109 (see PI_SOC_TOP_Z)
PI_SOC_TOP_Z = 97.7  # tallest package under the cooler plate on the Pi 5 STEP (BCM2712 96.65, RAM 97.7; PCB top 95.4)
PI_COOLER_HEADROOM = 10.5
YAW_PLATE_Z = (BODY_FRAME_UPPER_Z + 4.0, BODY_FRAME_UPPER_Z + 8.0)
YAW_PLATE_RADIUS = 33.5
YAW_PLATE_BAR_HALF_WIDTH = 29.0
YAW_BEARING_RADII = (25.0, 33.0)
YAW_BEARING_Z = (YAW_PLATE_Z[1], YAW_PLATE_Z[1] + 7.0)
YAW_CLOCKSPRING_RADII = (12.5, 24.0)
YAW_GEAR_PITCH_RADIUS = 18.5
YAW_GEAR_OUTER_RADIUS = 20.0
YAW_GEAR_BORE_RADIUS = 13.0
YAW_GEAR_RATIO = 1.0
YAW_PINION_CENTER = (0.0, 2.0 * YAW_GEAR_PITCH_RADIUS)  # offset from the yaw axis
# Spur pair: module 1, 37 teeth each (pitch Ø37), 20 deg pressure angle. The
# mesh is outside the M181's position loop, so plain lash reaches the head
# one-for-one: 0.05-0.10 mm at r 18.5 is 0.15-0.31 deg against the <=0.25 deg
# best-case hysteresis target (RP-01 gates.md P09). The pinion is therefore a
# scissor (split) gear: two 2.4 mm halves, the loose half turned against the
# fixed one by a torsion spring, so both flanks of the driven gear's teeth are
# always in contact until the transmitted torque exceeds the preload.
YAW_GEAR_MODULE = 1.0
YAW_GEAR_TEETH = 37
YAW_SCISSOR_HALF_FACE = 2.4
YAW_SCISSOR_GAP = 0.2
# Preload vs demand: the RP-01 screen's yaw peak external torque (0.1099 N*m
# at Layout 03's 0.001080 kg*m2) scales with the head's current yaw inertia and
# needs >= 1.5x margin; the M181 Current Limit (0.9 A x 0.333 N*m/A = 0.30 N*m)
# is the most it can ever drive. 0.22 N*m keeps the mesh lash-free over the
# whole motion envelope; above it (only past the design envelope, e.g. a
# collision) the halves part and lash returns.
YAW_SCISSOR_PRELOAD_NM = 0.22
YAW_PEAK_EXTERNAL_TORQUE_NM = 0.1099 * _HEAD_YAW_MASS["estimated_inertia_kg_m2"] / 0.001080
YAW_SERVO_CURRENT_LIMIT_TORQUE_NM = 0.9 * 0.333
YAW_SERVO_ENVELOPE = (-10.0 + BODY_AXIS_X, 10.0 + BODY_AXIS_X, 29.0, 55.0, 99.0, 133.0)
YAW_OPENING_RADIUS = 45.0
# RP-01 actuator screen: peak yaw 378 deg/s = 63 rpm at the output. XC330-M181
# no-load speed 95 / 129 rpm at 3.7 / 5.0 V (ROBOTIS e-manual).
YAW_PEAK_OUTPUT_RPM = 63.0
YAW_SERVO_NO_LOAD_RPM = {"3.7V": 95.0, "5.0V": 129.0}

PI_CENTER = (6.0 + BODY_SHIFT_X, 0.0, 102.0)
# Pi 5 cooler-post holes (STEP PCB), from the Pi's bounding-box corner: 58 x 37 mm apart.
PI_COOLER_HOLE_A = (PI_CENTER[0] - 45.0 + 5.25, PI_CENTER[1] - 28.8 + 11.1)
# Battery (RP03-CAD-06; RP03-CAD-07 for the pack): low in a chassis tub under
# the deck, forward of the motors, long side across the robot. It sits under the
# deck top and drops out downward through a bottom hatch; the shell floor is
# open under it. The pack is the RP-02 working selection of 2026-09-24: a 2S1P
# of two Samsung INR18650-25R cells lying side by side with a 2S 20 A balanced
# BMS board on top. Cell and BMS sizes are datasheet/listing values, not a
# vendor STEP; the BMS thickness is unverified.
BATTERY_CELL_DIAMETER = 18.4  # 25R body max 18.33 +/- 0.07 plus sleeve
BATTERY_CELL_LENGTH = 65.0  # 25R height 64.85 +/- 0.15 mm
BATTERY_CELL_PITCH = 19.5  # 1.1 mm between the two cells at 18.4 max; Samsung asks for more than 1 mm
BATTERY_END_STRAP_T = 1.0  # nickel strap, insulation cap and solder at each cell end
BATTERY_BMS_SIZE = (20.0, 48.0, 2.9)  # selected Robocraze module listing gives 48 x 20 mm only; 2.9 mm is a stale proposal placeholder, not a measured height
BATTERY_WRAP_T = 0.3  # heat-shrink sleeve under the cells and over the BMS
BATTERY_SIZE = (
    BATTERY_CELL_PITCH + BATTERY_CELL_DIAMETER + 2.0 * BATTERY_WRAP_T,
    BATTERY_CELL_LENGTH + 2.0 * BATTERY_END_STRAP_T,
    BATTERY_CELL_DIAMETER + BATTERY_BMS_SIZE[2] + 3.0 * BATTERY_WRAP_T,
)  # 38.5 x 67.0 x 23.5 mm envelope
BATTERY_TUB_FLOOR_Z = (30.5, 32.0)
BATTERY_TUB_WALL = 1.5
BATTERY_TUB_CLEARANCE = 1.5  # foam/retention gap between the pack and each tub wall
BATTERY_TUB_FRONT_X = 67.0  # front wall inner face; the pack sits against the front of the tub
BATTERY_TUB_X = (
    BATTERY_TUB_FRONT_X - BATTERY_SIZE[0] - 2.0 * BATTERY_TUB_CLEARANCE - BATTERY_TUB_WALL,
    BATTERY_TUB_FRONT_X,
)  # rear wall outer face, front wall inner face
BATTERY_TUB_HALF_Y = BATTERY_SIZE[1] / 2.0 + BATTERY_TUB_CLEARANCE + BATTERY_TUB_WALL
# Hatch flange carries the four screws into the tub bosses (TUB_BOSS_XY).
BATTERY_HATCH_X = (BATTERY_TUB_X[0] - 3.0, BATTERY_TUB_X[1] + BATTERY_TUB_WALL + 6.5)  # front edge flush with the front bosses
BATTERY_HATCH_HALF_Y = BATTERY_TUB_HALF_Y + 10.0
BATTERY_HATCH_GAP = 0.5  # running gap round the hatch in the shell floor opening
BATTERY_CENTER = (
    BATTERY_TUB_FRONT_X - BATTERY_TUB_CLEARANCE - BATTERY_SIZE[0] / 2.0,
    0.0,
    BATTERY_TUB_FLOOR_Z[1] + BATTERY_SIZE[2] / 2.0,
)  # X 27.0-65.5, Z 32-55.5
# Ballast (RP03-CAD-08): a mild-steel bar clamped under the deck between the
# battery tub's front wall and the front crossmember, hung from two M3
# countersunk screws (CH-038) from the deck top. It restores the register CoM to
# the physics.md 2.5 line after the lighter RP03-CAD-07 pack.
BALLAST_X = (69.5, 78.5)  # 1.0 mm off the tub front wall (X 68.5), 1.5 mm off the crossmember (X 80)
BALLAST_HALF_Y = 30.0
BALLAST_Z = (33.0, 52.0)  # top face against the deck underside (Z 52)
BALLAST_SCREW_Y = (-20.0, 20.0)
BALLAST_SCREW_X = 74.0
BALLAST_DENSITY_G_CM3 = 7.85
# CH-038 is an M3 x 12 Phillips countersunk screw (ISO 7046-1): 90 deg head,
# theoretical O6.3, actual rim O5.5 max, k 1.65. The deck carries a 90 deg
# countersink opened to O6.5, so the head seats 0.1 mm below the deck top.
BALLAST_SCREW_HEAD = (6.3, 5.5, 1.65)  # theoretical dk, actual dk max, k max
BALLAST_SCREW_SEAT_D = 6.5  # countersink diameter at the deck top (Z 56)
BALLAST_SCREW_LENGTH = 12.0  # overall, head included
BALLAST_SCREW_HEAD_TOP_Z = DECK_Z + 2.0 - (BALLAST_SCREW_SEAT_D - BALLAST_SCREW_HEAD[0]) / 2.0  # Z 55.9
BALLAST_SCREW_HEAD_Z = (BALLAST_SCREW_HEAD_TOP_Z - BALLAST_SCREW_HEAD[2], BALLAST_SCREW_HEAD_TOP_Z)  # Z 54.25-55.9
BALLAST_SCREW_TIP_Z = BALLAST_SCREW_HEAD_TOP_Z - BALLAST_SCREW_LENGTH  # Z 43.9: 8.1 mm in the bar
BALLAST_SCREW_THREAD_DEPTH = 8.0
BALLAST_SCREW_HOLE_DEPTH = 9.0  # tapped hole runs 1 mm past the thread so the tip does not bottom
_BALLAST_HEAD_CONE_H = (BALLAST_SCREW_HEAD[1] - 3.0) / 2.0  # 90 deg cone from O3 to the O5.5 rim
BALLAST_SCREW_VOLUME = (
    math.pi * _BALLAST_HEAD_CONE_H / 3.0 * (1.5**2 + 1.5 * BALLAST_SCREW_HEAD[1] / 2.0 + (BALLAST_SCREW_HEAD[1] / 2.0) ** 2)
    + math.pi * (BALLAST_SCREW_HEAD[1] / 2.0) ** 2 * (BALLAST_SCREW_HEAD[2] - _BALLAST_HEAD_CONE_H)
    + math.pi * 1.5**2 * (BALLAST_SCREW_LENGTH - BALLAST_SCREW_HEAD[2])
)  # mm3, recess ignored
BALLAST_BAR_G = (
    (BALLAST_X[1] - BALLAST_X[0]) * 2.0 * BALLAST_HALF_Y * (BALLAST_Z[1] - BALLAST_Z[0])
    - 2.0 * math.pi * 1.5**2 * BALLAST_SCREW_HOLE_DEPTH
) / 1000.0 * BALLAST_DENSITY_G_CM3
BALLAST_SCREWS_G = 2.0 * BALLAST_SCREW_VOLUME / 1000.0 * BALLAST_DENSITY_G_CM3
# Power distribution boards (RP-02 board-specs.md sec 2; PROPOSAL 2026-09-25).
# Placeholder envelopes for the four custom power/safety PCBs, the main-fuse
# holder and the E-stop. Sizes come from the RP-02 part inventory (nothing is
# laid out); positions are a proposal that the WS-H sizing notes could not fit
# as first drawn, so they are re-packed here against the measured model:
# PCB-04 and PCB-03 share the free band under the compute tray (X -27..59,
# Z 63..77, between the body's lower cross-members) and keep 1 mm gaps to the
# cross-members, each other and the Adafruit DRV8833 carriers. The band has no slack:
# 44 x 70 + 41 x 60 mm are the WS-H areas (3080 and 2460 mm2, reshaped from
# 70 x 44 and 56 x 44). Boxes are (x0, x1, y0, y1, z0, z1).
PCB_THICKNESS = 1.6
PCB02_BOX = (-49.6, -38.0, -25.0, 25.0, 58.0, 94.0)  # vertical, parts face +X; 50 x 36 mm board on the rear-panel frame
PCB03_BOX = (18.0, 59.0, -30.0, 30.0, 63.0, 75.0)  # motor gate, head rail, drive feed: 41 x 60 x 12
PCB04_BOX = (-27.0, 17.0, -35.0, 35.0, 63.0, 77.1)  # branch converters: 44 x 70 x 14.1 (1 mF-class hold-up caps 12.5 tall)
# Pack interface in the 11.3 mm channel between the tub's +Y wall and the chassis
# rail (connector-schedule.md CN-05, 2026-09-26). The Anderson SBS Mini (13 mm
# wide) fits nowhere near the tub, so the pack disconnect is a Molex Micro-Fit+
# 1x2 wire-to-wire pair (mated envelope E, drawing not fetched), mated only in
# OFF. It lies beside the tub behind a service window in the tub wall: with the
# hatch open and the pack lowered, the pair slides into the empty tub and is
# unplugged there. The tub's rear +Y screw boss shares the channel, so the
# bosses stop 1 mm over their insert pilots and the pair, window and slide path
# start 0.5 mm above them (D-028).
# Main fuse (CH-028/CH-029, D-032): no ATO fuse fits the channel (the fuse alone is
# 19.1 x 18.8 mm across its blades; the channel is 11.3 x 19.6). The Littelfuse
# 0FHA0001ZXJ inline holder (30 x 10 x 26 mm with the fuse) sits above the
# channel, about 25 mm over the disconnect (PA-02: still source-adjacent), fuse
# loading from the top. A printed bracket on the front deck carries it: a column
# in front of the body M4 foot and a shelf under the holder.
TUB_BOSS_TOP_Z = 39.5
PACK_DISCONNECT_PAIR_BOX = (27.0, 49.0, 39.5, 47.8, 40.0, 50.0)
PACK_FUSE_HOLDER_BOX = (52.0, 82.0, 39.0, 49.0, 73.0, 99.0)  # wire axis along X
FUSE_BRACKET_COLUMN = (75.0, 81.0, 40.0, 48.0)  # x0, x1, y0, y1; deck top to the shelf
FUSE_BRACKET_SHELF = (52.0, 82.0, 39.0, 49.0, 71.0, 73.0)
TUB_SERVICE_WINDOW = (26.9, 49.5, 40.0, 50.0)  # x0, x1, z0, z1 through the +Y tub wall
PACK_DISCONNECT_SLIDE_PATH = (27.0, 49.0, 30.0, 39.5, 40.0, 50.0)  # into the emptied tub
# Harness (05-harness/README.md, D-039). The pack NTC (CH-025, W02) breaks at a
# JST SM 2-way wire-to-wire pair lying along X in the +Y channel ahead of the
# disconnect, below the deck: the fuse left this space in D-032. To drop the pack,
# unplug J-PK first, then pull the NTC pair back to the tub window and unplug it.
PACK_NTC_BREAK_RESERVE = (51.0, 77.0, 40.0, 48.0, 41.0, 48.0)
PACK_NTC_BREAK_PAIR = (52.0, 76.0, 40.75, 47.25, 41.6, 47.4)  # JST SM 2p mated, 24 x 6.5 x 5.8 (E)
# Fused feed split (D-039): the fuse output and the pack negative each fork at a
# crimped butt splice (2 x AWG16 into 1) above the PCB-03 +Y edge; one branch
# runs to PCB-03 J3-1 (motor side), the other to PCB-02 J2-1. The negative
# splice is the power star. Two O6 x 26 mm splices side by side along X.
BATBUS_SPLICE_RESERVE = (20.0, 50.0, 36.0, 49.4, 76.5, 84.0)
BATBUS_SPLICE_RADIUS = 3.0
BATBUS_SPLICE_X = (22.0, 48.0)
BATBUS_SPLICE_YZ = {"POS": (46.0, 80.25), "NEG_STAR": (39.5, 80.25)}
# 7 x 7 mm hatch-screw bosses, each lapping 0.5 mm onto a tub wall: two outside
# the side walls at the rear, two on the front wall's face at Y +/-34.35, midway
# between the ballast bar (|Y| 30) and the channel (Y 38.7).
TUB_BOSS_XY = tuple(
    (x, sign * y)
    for x, y in (
        (BATTERY_TUB_X[0] + 4.0, BATTERY_TUB_HALF_Y + 3.0),
        (BATTERY_TUB_X[1] + BATTERY_TUB_WALL + 3.0, (BALLAST_HALF_Y + 38.7) / 2.0),
    )
    for sign in (-1.0, 1.0)
)
# Frame joint hardware (D-030, D-033). One insert article for J04 and J11A: an
# M3 x 6 brass heat-set insert (OD 4.4) in a O4.3 pilot (CH-061, CH-077). Button
# heads seat straight on the printed faces; no washers.
FRAME_INSERT_RADIUS = 2.15  # pilot and modeled insert envelope
FRAME_INSERT_LENGTH = 6.0
# D-033: each end of the frame is one print: the deck, both rails and the
# crossmember. The J05/J06 tongue joints and the J16 deck screws are gone. Where
# the deck covers a crossmember, the crossmember rises to the deck underside (Z 52):
# front from Z 51, rear from Z 48. Boxes are (x0, x1, y0, y1, z0, z1).
FRAME_MODULE_FILLS = {
    "FRONT": (80.0, 92.0, -56.0, 56.0, 51.0, 52.0),
    "REAR": (-41.0, -32.0, -56.0, 56.0, 48.0, 52.0),
}
# J11A: M3 x 6 from below through the 1.5 mm hatch into 6 mm boss inserts (4.5 mm thread).
J11A_SCREW_LENGTH = 6.0
# J11B (D-030): the pack is strapped to the hatch and both drop out together.
# Two 10 mm hook-and-loop straps loop under the hatch, up through slots beside
# the pack's X faces and over the cell tops, clear of the BMS (|Y| <= 24) and
# the cell-end straps. 1.5 mm closed-cell foam pads fill the cell-end gaps; the
# +Y pad stops short of the service window.
PACK_STRAP_Y = 29.0  # strap centres, |Y|
PACK_STRAP = (10.0, 1.2)  # width, thickness
PACK_STRAP_X = (25.8, 66.7)  # outer faces of the two risers
PACK_STRAP_Z = (29.3, 51.9)  # under the hatch to over the cell tops (cells top Z 50.7)
PACK_STRAP_SLOT = (0.2, 0.5)  # slot clearance in X and Y round the strap
PACK_FOAM_T = 1.5
PACK_FOAM_Z = (33.0, 50.0)
PACK_FOAM_X = {"-Y": (28.0, 64.0), "+Y": (50.5, 64.0)}

# E-stop: IDEC XA1E-BV3U02KT-R, the Ø16 unibody XA with a Ø29 mushroom and 2NC
# (one to the permit loop, one to C2), 14 g. IDEC XA datasheet: Ø16.2 cut-out,
# 0.8-4.5 mm panel, mushroom top 20.6 mm above the mounting face, 23.9 mm behind
# it. It replaces the Ø40 XW1E (20 mm proud, 46.4 mm deep, 40 g). The switch
# mounts on the floor of a tapered octagonal well printed with the rear panel,
# so the mushroom rises 12.6 mm out of a socket that repeats the panel outline
# instead of standing 20 mm off a flat wall. An amber octagonal bezel land round
# the well is the ISO 13850 yellow background and matches the ear inlays and
# arch trims. The well fits between PCB-02 (X >= -49.6 below Z 94) and the panel
# frame's top bar (X -55.6...-53.2, Z >= 122); the Pi's rear parts start at X -23.
ESTOP_CENTER_Z = 105.5
ESTOP_REAR_OUTER_X = BODY_X_REAR - SHELL_THICKNESS  # rear panel outer face
ESTOP_WELL_DEPTH = 8.0  # panel face to the mounting face on the well floor
ESTOP_WELL_FLOOR = 2.0
ESTOP_WELL_MOUTH = 34.0  # inner across-flats at the panel face: 2.5 mm round the mushroom
ESTOP_WELL_THROAT = 26.0  # inner across-flats at the floor (45 deg taper)
ESTOP_WELL_WALL = 1.6
ESTOP_BEZEL_ACROSS_FLATS = 42.0
ESTOP_BEZEL_PROUD = 1.2
ESTOP_CUTOUT_DIAMETER = 16.2
ESTOP_MUSHROOM_DIAMETER = 29.0
ESTOP_MUSHROOM_TOP_ABOVE_MOUNT = 20.6
ESTOP_MUSHROOM_SKIRT = 4.5  # skirt + dome envelope; the datasheet gives only the Ø and top height
ESTOP_MUSHROOM_DOME = 5.0
ESTOP_OPERATOR_BEZEL = (20.0, 2.1)  # Ø x height of the operator collar on the mounting face
ESTOP_STEM_DIAMETER = 12.0
ESTOP_DEPTH_BEHIND_PANEL = 23.9  # unibody, solder/tab #110; taken from the floor's back face
ESTOP_BODY_DIAMETER = 18.0
ESTOP_MOUNT_X = ESTOP_REAR_OUTER_X + ESTOP_WELL_DEPTH
ESTOP_FLOOR_BACK_X = ESTOP_MOUNT_X + ESTOP_WELL_FLOOR
ESTOP_KEEP_OUT = (ESTOP_FLOOR_BACK_X, ESTOP_FLOOR_BACK_X + ESTOP_DEPTH_BEHIND_PANEL, -11.0, 11.0, ESTOP_CENTER_Z - 11.0, ESTOP_CENTER_Z + 11.0)  # contact block, three #110 tabs and wiring
ESTOP_RED = "#C62F28"
ESTOP_AMBER = "#D39F36"  # the droid's amber, lifted toward safety yellow for the background

# Connectors and cable exits (../../connector-schedule.md, 2026-09-26). Rule:
# power connectors (Molex Micro-Fit+ / Micro-Fit 3.0, right-angle) sit on the
# free board edges and exit sideways; signal connectors (JST GH, and the XC330's
# JST EH) are top-entry headers inside the board outline and plug up into the
# layer between the board parts envelopes and the compute tray. Widths: JST GH
# from the JST catalogue (D) and Micro-Fit 3.0 from the Molex drawing via the
# KiCad fab outline (D); Micro-Fit+, JST EH, every height and every plug
# protrusion are estimates (E). Boxes are (x0, x1, y0, y1, z0, z1).
CONNECTOR_GAP = 1.0  # between neighbouring housings on one edge (E)


def connector_width(family, circuits):
    """Housing width along the board edge, mm."""
    cols = math.ceil(circuits / 2.0)
    return {
        "GH": 1.25 * circuits + 3.25,  # D: JST GH SMT header, dimension B
        "MF3": 3.0 * cols + 4.26,  # D: Molex 43045 dual row (43045-0200 7.26, -0400 10.26)
        "MF+": 3.0 * cols + 5.3,  # E: Micro-Fit+ dual row, drawing not fetched
        "EH": 2.5 * circuits + 2.5,  # E: JST EH (XC330 B3B-EH-A)
    }[family]


# Right-angle power connectors on the free board edges. "span" is the free
# length along the edge; the box is the mated plug plus the lead's first bend.
CONNECTOR_EDGE_STRIPS = {
    "PCB03_PY": {"box": (19.0, 37.0, 30.0, 50.0, 64.6, 75.0), "span": (19.0, 37.0), "connectors": [
        ("J3-2", "MF+", 2, "PB-DRIVE-L to the left DRV8833 carrier"),
        ("J3-1", "MF+", 2, "BATBUS-M in from the fuse-side star splice (D-039)"),
    ]},
    "PCB03_NY": {"box": (19.0, 37.0, -50.0, -30.0, 64.6, 75.0), "span": (19.0, 37.0), "connectors": [
        ("J3-3", "MF+", 2, "PB-DRIVE-R to the right DRV8833 carrier"),
        ("J3-4", "MF3", 2, "PB-HEAD pitch/roll trunk to the yaw junction J8-1 (D-039: Micro-Fit 3.0, AWG22)"),
    ]},
    "PCB04_NY": {"box": (-14.0, 15.0, -51.0, -35.0, 64.6, 77.0), "span": (-14.0, 15.0), "connectors": [
        ("J4-1", "MF+", 2, "PB-COMPUTE to the Pi 5 USB-C pigtail"),
        ("J4-2", "MF3", 4, "PB-SAFE-C2 and PB-DISPLAY to the yaw junction"),
        ("J4-4", "MF3", 2, "PB-SAFE-BASE to the C3 carrier J10-1"),
    ]},
    "PCB04_PY": {"box": (-14.0, 15.0, 35.0, 51.0, 64.6, 77.0), "span": (-14.0, 15.0), "connectors": [
        ("J4-3", "MF+", 4, "OPBUS and CHGBUS in from PCB-02 J2-3"),
        ("J4-5", "MF3", 2, "PB-AUDIO-OUT to PCB-05"),
    ]},
    # PCB-02 stands vertical: this edge runs along Z and the plugs exit -Y.
    "PCB02_NY": {"box": (-48.0, -38.0, -41.0, -25.0, 60.0, 94.0), "span": (60.0, 94.0), "connectors": [
        ("J2-1", "MF+", 2, "BATBUS-C in from the fuse-side star splice (D-039; J2-2 deleted)"),
        ("J2-3", "MF+", 4, "OPBUS and CHGBUS out to PCB-04 J4-3"),
    ]},
}
# Top-entry signal headers plug up into these layers (reserve = plugs + first bend).
CONNECTOR_TOP_LAYERS = {
    "PCB03": {"box": (19.0, 58.0, -29.0, 29.0, 75.0, 84.3), "connectors": [
        ("J3-5", "EH", 3, "XC330 yaw servo: VDD, GND, bus DATA"),
        ("J3-6", "GH", 6, "PCB-02 logic: CHARGE_ABSENT, ENERGY_OK, SYSTEM_ARM, MOTOR_PRESENT, 2 x GND"),
        ("J3-7", "GH", 4, "E-stop NC1 loop and NC2 status"),
        ("J3-8", "GH", 8, "head sideband from the yaw junction"),
        ("J3-9", "GH", 4, "C3_READY, MOTOR_PRESENT to C3, 2 x GND (C3 carrier J10-12)"),
    ]},
    "PCB04": {"box": (-26.0, 16.0, -34.0, 29.0, 77.1, 84.3), "connectors": [
        ("J4-6", "GH", 10, "EN_* / PG_* and the sequencing latch to PCB-02 J2-4"),
    ]},
    # PCB-02's parts face is +X, so its top-entry headers plug in along +X.
    "PCB02": {"box": (-38.0, -31.0, -24.0, 24.0, 69.5, 84.0), "connectors": [
        ("J2-4", "GH", 10, "EN_* / PG_* to PCB-04 J4-6"),
        ("J2-5", "GH", 6, "logic to PCB-03 J3-6"),
        ("J2-6", "GH", 8, "head sideband: STAT, INT_PB, KILL, V_PACK_ANA, CHG_ABSENT_3V3"),
        ("J2-7", "GH", 2, "pack NTC (103AT-2) to the BQ25798 TS input"),
    ]},
}

# Charge inlet (PCD-CON-05): a vertical-mount 16-pin USB-C receptacle on the back
# (-X) face of PCB-02, mouth 1.05 mm behind the rear panel's inner face, and a
# 13.2 x 7.2 mm plug cut-out through the panel. Envelope only; part number open.
CHARGE_INLET_CENTER_YZ = (0.0, 64.0)
CHARGE_INLET_RECEPTACLE = (-56.95, PCB02_BOX[0], -4.47, 4.47, 62.37, 65.63)
CHARGE_INLET_CUTOUT = (13.2, 7.2)
CHARGE_INLET_OUTSIDE_CORRIDOR = (BODY_X_REAR - SHELL_THICKNESS - 27.0, BODY_X_REAR - SHELL_THICKNESS, -6.5, 6.5, 60.5, 67.5)

# Pi 5 power: right-angle USB-C plug on the Pi's -Y edge (the port is at X -10.1,
# Z 96.2) and its pigtail down past the compute tray to PCB-04 J4-1.
PI_POWER_PLUG_RESERVE = (-16.2, -4.0, -44.0, -28.6, 92.2, 100.2)
PI_POWER_PIGTAIL_DROP = (-13.0, -7.0, -46.0, -39.0, 77.0, 92.2)  # lands on the PCB04_NY edge reserve (J4-1)

# Motor leads: the MOT3001 ships with a 6-pin cable; its motor pair is cut out and
# re-crimped to a Micro-Fit 3.0 1x2 wire-to-wire pair outboard of each DRV8833 carrier.
# D-031: the left pair lies along X over the board, 0.5 mm above the M2.5 screw
# heads (Z 69.1). The right board's terminal block is outboard (to Z 76.1), so the
# right pair stands along Y in front of it, between the block and the dogleg (X 58).
MOTOR_INLINE_RESERVE = {
    "L": (37.5, 58.0, 49.5, 59.0, 69.6, 82.0),  # starts past PCB03_PY's edge reserve (X 37)
    "R": (50.9, 57.9, -59.5, -38.5, 69.6, 82.0),
}

# Yaw service break: the clock-spring's stationary end lands on a small
# junction board (PCB-08) under the adapter plate on -Y, clear of the cooler
# headroom prism; its body-side cables drop down a -Y riser to PCB-03/04.
YAW_JUNCTION_BOX = (-22.0, 10.0, -44.0, -23.0, 112.0, 125.5)
# PCB-08: 32 x 21 x 1.6 mm plate at the bottom of the junction reserve. The
# clock-spring flex is soldered to it; body-side connectors: J8-1 Micro-Fit 3.0
# 2x3 right-angle (D-039) on the -X edge (exits -X, then down the riser) and three GH
# top-entry headers (J8-3/J8-5 sideband GH 8 x 2, J8-4 head link GH 6).
YAW_JUNCTION_PLATE_Z = (112.0, 113.6)
YAW_JUNCTION_MF_PLUG_RESERVE = (-40.0, -22.0, -41.0, -26.0, 113.6, 124.0)
YAW_JUNCTION_GH = (("J8-3", 8, -42.0), ("J8-5", 8, -35.5), ("J8-4", 6, -29.0))  # id, circuits, y0 (x0 -10)
# C0 link adapter (PCB-09): THVD1451 x 2 and the GH link/audio headers beside
# the yaw servo, fed from the Pi header by a 2 x 20 socket (8.5 mm, top Z 106.4,
# 0.6 mm under the XC330) and a 4.6 mm strip of the same board over it that
# stays inboard of the servo (Y <= 26.9, 0.1 mm clear): tight, measured, not
# yet bench-fitted. The bridge joins the strip to the wide part past the servo.
C0_GPIO_SOCKET = (-14.7, 37.1, 22.3, 28.3, 104.1, 106.4)  # socket body above the pin tips; the part round the pins is the header's own volume
C0_LINK_ADAPTER_STRIP = (-14.7, 26.0, 22.3, 26.9, 106.4, 108.2)
C0_LINK_ADAPTER_BRIDGE = (26.0, 37.1, 22.3, 28.5, 106.4, 108.2)
C0_LINK_ADAPTER_BOX = (26.0, 56.0, 28.5, 45.0, 104.0, 112.0)
C0_LINK_ADAPTER_PLATE_Z = (106.4, 108.0)
C0_LINK_ADAPTER_TOP_PLUGS = (36.0, 54.0, 29.0, 42.0, 112.0, 116.0)
C0_LINK_ADAPTER_SIDE_PLUG = (26.0, 38.0, 45.0, 54.0, 108.0, 112.5)
# C3 carrier (PCB-10, RP-02 CCD-HDL-03: DevKitC backplane with the base-link
# THVD1451, the TPS3436 window watchdog, READY logic, the 74LVC1G08 driver sleep gate; DRV8833 mapping in 04-pcbs/power-boards.md sec 2.4 (D-038),
# driver/sensor connectors and test points). Nothing modelled it, and the bare
# DevKitC floated over PCB-04 with its header pins in PCB-04's parts envelope.
# A free-volume scan found one home: standing vertical on the -Y side wall
# between the lower and upper rails, outboard of the Pi, components facing +Y.
# The DevKitC is soldered onto it through its own pin headers (2.5 mm plastic
# gap), so the C3 module is one replaceable part held by four M2.5 screws into
# lugs printed on the -Y rails. Signal headers are top-entry GH in the band
# below the DevKitC; power is one right-angle Micro-Fit 3.0 on the front edge.
C3_CARRIER_BOARD = (-14.0, 56.0, -58.4, -56.8, 82.0, 125.5)  # x0, x1, y0, y1, z0, z1 (board plate)
C3_DEVKIT_STANDOFF = 2.5  # header plastic between carrier and DevKitC
C3_DEVKIT_Z = (96.2, 124.5)  # DevKitC 28.3 mm board edge span
C3_GH_PLUG_LAYER = (-14.0, 56.0, -56.8, -46.0, 82.0, 95.2)
C3_POWER_PLUG_RESERVE = (56.0, 74.0, -56.8, -46.5, 84.0, 95.0)
C3_DEVKIT_USB_CORRIDOR = (-40.0, -11.5, -54.3, -48.8, 99.0, 122.0)  # service only, rear panel off
# Two 8 x 7.6 mm printed uprights between the -Y lower and upper rails carry
# M2.5 heat-set inserts; the carrier screws to them at four points.
C3_CARRIER_UPRIGHTS = ((-12.0, -4.0), (20.0, 28.0))  # x spans; Y -66..-58.4, Z 69..126
C3_CARRIER_SCREWS = ((-8.0, 86.0), (-8.0, 116.0), (24.0, 86.0), (24.0, 116.0))  # (x, z)
# Top-entry GH headers in two rows below the DevKitC: (id, circuits, x0).
C3_GH_ROWS = {
    86.0: (("J10-2", 6, -4.5), ("J10-5", 6, 7.25), ("J10-6", 6, 27.25), ("J10-8", 5, 39.0)),
    92.0: (("J10-7", 8, -13.0), ("J10-3", 4, 1.25), ("J10-4", 4, 10.5), ("J10-10", 4, 19.75), ("J10-12", 4, 29.0), ("J10-11", 3, 38.25)),
}
C3_CARRIER_CONNECTORS = [
    ("J10-1", "MF3", 2, "PB-SAFE-BASE from PCB-04 J4-4 (front edge, right-angle)"),
    ("J10-2", "GH", 6, "base link RS-422 to PCB-09 J9-2"),
    ("J10-3", "GH", 4, "encoder L"),
    ("J10-4", "GH", 4, "encoder R"),
    ("J10-5", "GH", 6, "left DRV8833: SLP (AND of GPIO21 and BASE_READY), IN1, IN2, FLT (wired-OR GPIO9), GND, spare (D-038)"),
    ("J10-6", "GH", 6, "right DRV8833: SLP (AND of GPIO21 and BASE_READY), IN1, IN2, FLT (wired-OR GPIO9), GND, spare (D-038)"),
    ("J10-7", "GH", 8, "IMU PCB-07 (SPI)"),
    ("J10-8", "GH", 5, "nose pod, one cable (D-013): +5V and Vo for the GP2Y0A21YK0F, GND, +3V3 and OUT for the DRV5055 Hall board"),
    ("J10-10", "GH", 4, "rear TCRT cartridge"),
    ("J10-11", "GH", 3, "E-stop status (GPIO3 input) from PCB-03"),
    ("J10-12", "GH", 4, "C3_READY, MOTOR_PRESENT to PCB-03 J3-9"),
]

# Floor-contact functions live in a compact faceted keel bolted under the rear
# crossmember. The crossmember and keel move forward with the body's rear wall
# (RP03-CAD-06).
REAR_CHASSIS_SHIFT_X = BODY_SHIFT_X
SKID_ROOT_DATUM = (-56.0 + REAR_CHASSIS_SHIFT_X, 0.0, 34.0)
SKID_SHOE_SIZE = (12.0, 10.0, 2.5)  # anti-tip contact only; sized for wear, not load spreading
SKID_SHOE_BOTTOM_Z = 3.5
SKID_PAD_CENTER = (-43.0 + REAR_CHASSIS_SHIFT_X, 0.0, SKID_SHOE_BOTTOM_Z + SKID_SHOE_SIZE[2] / 2.0)
TCRT_PACKAGE_SIZE = (10.2, 7.1, 7.0)  # Vishay STEP body incl. lens shoulders; was 5.8 wide
TCRT_OPTICAL_FACE_Z = 10.0
TCRT_GUARD_BOTTOM_Z = 7.0
TCRT_REAR_LOOKAHEAD = 27.0
TCRT_CHANNELS = ("REAR",)
TCRT_REAR_CENTER = (SKID_PAD_CENTER[0] - TCRT_REAR_LOOKAHEAD, 0.0, TCRT_OPTICAL_FACE_Z + TCRT_PACKAGE_SIZE[2] / 2.0)
REAR_KEEL_TOP_Z = 34.0  # underside of REAR_SKID_CROSSMEMBER
REAR_KEEL_STATIONS = (
    # x, half-width, lower-z, upper-z, corner chamfer
    (-33.0 + REAR_CHASSIS_SHIFT_X, 3.5, 14.0, 22.0, 0.8),                   # knife leading edge
    (-37.0 + REAR_CHASSIS_SHIFT_X, 7.0, SKID_SHOE_BOTTOM_Z + 2.5, 27.0, 1.5),  # shoe front, flat belly starts
    (-44.0 + REAR_CHASSIS_SHIFT_X, 8.0, SKID_SHOE_BOTTOM_Z + 2.5, 31.0, 1.8),
    (-48.0 + REAR_CHASSIS_SHIFT_X, 9.0, SKID_SHOE_BOTTOM_Z + 2.5, REAR_KEEL_TOP_Z, 2.0),  # crossmember seat
    (-54.0 + REAR_CHASSIS_SHIFT_X, 9.0, SKID_SHOE_BOTTOM_Z + 2.5, REAR_KEEL_TOP_Z, 2.0),  # seat rear
    (-62.0 + REAR_CHASSIS_SHIFT_X, 9.4, 12.0, REAR_KEEL_TOP_Z, 1.8),       # sensor flat starts ahead of the shim stack
    (-64.0 + REAR_CHASSIS_SHIFT_X, 9.5, 12.0, REAR_KEEL_TOP_Z, 1.8),       # sensor flat: belly at the shim-stack seat
    (-78.0 + REAR_CHASSIS_SHIFT_X, 9.5, 12.0, 26.0, 1.6),                  # 9.5 half-width: >= 3.9 mm pocket wall at the chamfer
    (-83.0 + REAR_CHASSIS_SHIFT_X, 3.0, 14.0, 20.0, 0.8),                   # sharp heel
)
# J09A: four ISO 4762 M3 x 30 (CH-034) up through the keel into CNC Kitchen
# M3 x 5.7 inserts in the crossmember underside. The rear pair sits 1.5 mm
# forward of the old X -45.5 so the insert keeps a 1.7 mm wall to the
# crossmember's rear face (X -48). Heads sit in O6.5 counterbores.
REAR_KEEL_SCREWS_X = (-52.5 + REAR_CHASSIS_SHIFT_X, -60.0 + REAR_CHASSIS_SHIFT_X)  # forward pair counterbores clear the shoe
REAR_KEEL_SCREW_Y = 5.5
REAR_KEEL_SCREW_LENGTH = 30.0
REAR_KEEL_SCREW_HEAD = (2.75, 3.0)  # ISO 4762 M3 head radius, height
REAR_KEEL_COUNTERBORE_RADIUS = 3.25
REAR_KEEL_HEAD_SEAT_Z = (9.5, 12.0)  # forward, rear pair: 0.5 / 0.6 mm recessed from the belly
REAR_KEEL_INSERT_Z = (REAR_KEEL_TOP_Z, REAR_KEEL_TOP_Z + M3_INSERT_LENGTH)
REAR_KEEL_SHELL_SLOT = (-73.0 + REAR_CHASSIS_SHIFT_X, -40.0 + REAR_CHASSIS_SHIFT_X, 10.5)  # x0, x1, half-width of the floor pass-through
# J09B: the TCRT drops into its pocket from below, leads into a 4-way
# low-profile socket on the breakout (CH-020, custom PCB reserve). A printed
# bezel carries both guard lips (J10B) and holds the sensor on 0.6 mm end
# ledges; one M2 screw plus one moulded pin fix it through the height shims.
# Optical height (J09) = keel belly (Z 12) - shims: 0-4 x 1 mm gives Z 12-8;
# the nominal stack is two shims (Z 10).
_TX = TCRT_REAR_CENTER[0]  # X -54
REAR_TCRT_POCKET = (_TX - 5.4, _TX + 5.4, -3.8, 3.8)  # x0, x1, y0, y1: 0.3 / 0.25 mm about the 10.2 x 7.1 package
REAR_TCRT_BELLY_Z = 12.0
REAR_TCRT_SHIM_T = 1.0
REAR_TCRT_SHIMS_NOMINAL = 2
REAR_TCRT_SHIMS_RANGE = (0, 4)  # optical face Z 12 .. 8
REAR_TCRT_BEZEL_T = 1.5
REAR_TCRT_BEZEL_X = (_TX - 7.5, _TX + 6.5)  # front end clears the rear counterbores
REAR_TCRT_BEZEL_HALF_Y = 7.5
REAR_TCRT_BEZEL_WINDOW_X = (_TX - 4.5, _TX + 4.5)  # 0.6 mm ledges under the package ends
REAR_TCRT_FIX_POINTS = ((_TX, -5.6), (_TX, 5.6))  # M2 x 10 ISO 7380 screw, O1.8 moulded pin
REAR_KEEL_GUARD_X = (_TX - 7.5, _TX + 5.0)
REAR_KEEL_GUARD_WIDTH = 2.5
REAR_KEEL_GUARD_HEIGHT = TCRT_OPTICAL_FACE_Z - REAR_TCRT_BEZEL_T - TCRT_GUARD_BOTTOM_Z  # lip under the bezel plate
# Rear TCRT lead (CH-020, 01-chassis/v1/research/rear-tcrt-lead.md, D-016): no board.
# A 4-core GH pigtail is soldered to the TCRT's 3.5 mm leads under heat-shrink
# and leaves straight up through the pocket, which runs out through the keel
# top; the only connector is the GH plug at C3 J10-10. The LED switch and the
# phototransistor load live on PCB-10.
REAR_TCRT_LEAD_JOINTS = (_TX - 3.7, _TX + 3.7, -2.3, 2.3, TCRT_OPTICAL_FACE_Z + TCRT_PACKAGE_SIZE[2] + 0.5, 24.0)
REAR_TCRT_PIGTAIL_XY = (_TX + 2.0, 0.0)  # 0.5 mm clear of the shell rear wall (X -55.6)
REAR_TCRT_PIGTAIL_RADIUS = 1.4  # 4 x AWG28 pre-crimped GH leads, sleeved
# The J10-10 cable leaves the plug upward behind the crossmember (X -55.6 to
# -48 between shell wall and crossmember), so neither the crossmember nor the
# deck is bored. A 30 mm slack loop lets the keel drop to unplug at the keel.
REAR_TCRT_CABLE_RISER = (-55.2, -51.2, -34.0, -26.0)  # beside PCB-02 (Y +-25)
REAR_TCRT_CABLE_RUN_Z = (78.0, 84.0)  # over PCB-04 (Z 77.1), under the compute tray (Z 84.5)
REAR_CROSSMEMBER_TIE_LUG = (-51.0, -48.0, -33.0, -27.0, 36.0, 44.0)
# J10A: the shoe slides in from the front on a dovetail tongue and is held by
# one M2 x 6 thread-forming screw driven across the tongue from the keel's +Y
# side: clearance in the keel wall, threads in the (replaceable) shoe.
REAR_KEEL_SHOE_TONGUE = (2.0, 3.0, 2.5)  # half-width at the shoe top, at the tongue top, height
REAR_KEEL_SHOE_GROOVE_CLEARANCE = 0.15
REAR_KEEL_SHOE_SCREW_SEAT_Y = 5.3  # head seat in a side counterbore; tip at Y -0.7

# The keel is translucent ivory so the TCRT cartridge, cable riser and M3
# hardware inside it stay visible for packaging review.
REAR_KEEL_COLOR = IVORY
REAR_KEEL_ALPHA = 0.34

# Touch cap: an octagonal hood sliding on the pod's constant nose section,
# open at the bottom and rear; the cap travels rearward onto a floor-mounted
# detector switch. It stops at the pod seat (Z 29), just below the
# sensor window: the lower skirt over the ball housing was cut 2026-09-24
# (RP03-CAD-04), so floor-level objects below the GP2Y beam are no longer
# caught by contact and meet the purchased ball housing first.
TACTILE_NOSE_TRAVEL = 3.0
TACTILE_CAP_INNER_X = BALL_POD_X[1] + TACTILE_NOSE_TRAVEL
TACTILE_CAP_WALL = 2.0
TACTILE_NOSE_FACE_X = TACTILE_CAP_INNER_X + TACTILE_CAP_WALL
TACTILE_CAP_ARM_X0 = BALL_POD_NOSE_X0 + TACTILE_NOSE_TRAVEL + 0.2  # rear edge stays on the constant nose at full travel
TACTILE_CAP_CLEARANCE = 0.5  # to the pod sides, top and chamfers (constant section, D-011)
# Retention (D-011, J08): one vertical snap finger per cap side, 2.0 mm thick and 16.5 mm long,
# free at the open bottom. Its hook (0.8 mm engagement, 45 deg lead-in on the rear face) rides in
# a slot in the pod flank: the slot's front wall holds the cap on, the pod face stops it at
# 3 mm. Spread the finger tips ~1 mm and slide the cap forward to remove it.
TACTILE_SNAP_FINGER_X = (TACTILE_CAP_ARM_X0, 128.5)
TACTILE_SNAP_SLIT = 0.6
TACTILE_SNAP_FINGER_TOP_Z = 45.5  # 11.7 mm from root to hook: ~2.2% bending strain at 1 mm spread
TACTILE_SNAP_HOOK_X = (TACTILE_CAP_ARM_X0, 126.5, 127.2)  # rear tip, end of the lead-in, retaining face (0.7 mm flat)
TACTILE_SNAP_HOOK_Z = (32.9, 34.7)
TACTILE_SNAP_HOOK_TIP_Y = 17.0  # |y|; the pod flank is at 17.8
TACTILE_SNAP_SLOT = (TACTILE_SNAP_HOOK_X[0] - TACTILE_NOSE_TRAVEL - 0.3, TACTILE_SNAP_HOOK_X[2], 16.8, 32.7, 34.9)  # x0, x1, |y| floor, z0, z1
# Nose contact sensing (D-013, CH-019/064/065/066): contactless. A TI DRV5055A3 linear Hall sensor
# (SOT-23, 3.3 V: 15 mV/mT, +-88 mT linear, 20 kHz, 10 us) on a 6.0 x 4.6 x 0.8 board standing in a
# slot in the seat's front face, facing +X, reads a selected axially magnetised O3 x 1.5 N35 magnet in the cap
# wall, below the window slit. +12 mT is only a bench starting threshold; measure before choosing
# released firmware values. Nothing mechanical bottoms, so the cap
# keeps its full 3 mm to the pod-face stop. Two selected RS PRO 821245 springs return the cap against
# the snap hooks; their higher preload/stop force and unsupported-length behavior need physical checks.
# The ESE22MV21 of D-011 is dropped: its full travel
# is 2.05 mm, not 3.
NOSE_HALL_BOARD = (126.6, 127.4, 7.0, 13.0, 30.4, BALL_POD_Z0 + BALL_POD_SEAT_THICKNESS)  # x0, x1, y0, y1, z0, z1
NOSE_HALL_SLOT_CLEARANCE = 0.1
NOSE_HALL_PACKAGE = (1.0, 2.92, 1.3, 2.37)  # SOT-23 body height (x), length (y), width (z), lead span (z)
NOSE_HALL_CENTER_YZ = (10.0, 32.6)
NOSE_HALL_ELEMENT_DEPTH = 0.65  # Hall plate below the package top; confirm on the TI mechanical drawing
NOSE_HALL_NOTCH = (8.3, 11.7, 31.2)  # y0, y1, z0 of the sensor notch through the seat's front face
NOSE_MAGNET = (1.5, 1.5)  # radius, length (selected Ø3 x 1.5 mm N35, axial; polarity to bench-check)
NOSE_SPRING_YZ = ((3.0, 32.0), (-3.0, 32.0))
NOSE_SPRING_POCKET = (1.65, 122.5)  # radius, pocket floor x (6 mm deep in the seat front face)
NOSE_SPRING = (1.375, 0.25, 15.7)  # RS PRO 821245 selected; OD 2.75, wire 0.25, free 15.7; modeled installed gap remains 9/6 pending load and buckling tests
TACTILE_CAP_INNER_HALF_WIDTH = BALL_POD_HALF_WIDTH + TACTILE_CAP_CLEARANCE
TACTILE_CAP_INNER_TOP_Z = BALL_POD_LID_Z[1] + 0.6
TACTILE_CAP_INNER_UPPER_CHAMFER = 6.9
TACTILE_CAP_Z = (BALL_POD_Z0, TACTILE_CAP_INNER_TOP_Z + TACTILE_CAP_WALL)
TACTILE_CAP_HALF_WIDTH = TACTILE_CAP_INNER_HALF_WIDTH + TACTILE_CAP_WALL
TACTILE_CAP_LOWER_CHAMFER = 3.0
TACTILE_CAP_UPPER_CHAMFER = 7.5
TACTILE_CAP_ALPHA = 0.45


FRAMES = {
    "F_GROUND": (0.0, 0.0, 0.0),
    "F_AXLE": (0.0, 0.0, AXLE_Z),
    "F_WHEEL_L": WHEEL_CENTER_L,
    "F_WHEEL_R": WHEEL_CENTER_R,
    "F_BALL_TRANSFER": BALL_CONTACT,
    "F_BODY_BASE": (BODY_AXIS_X, 0.0, BODY_Z_BOTTOM),
    "F_HEAD_YAW": HEAD_YAW_DATUM,
    "F_COMPUTE_TRAY": (PI_CENTER[0], PI_CENTER[1], 86.0),
    "F_POWER_BAY": BATTERY_CENTER,
    "F_SENSOR_FRONT": (FRONT_RANGE_SENSOR_FACE_X, FRONT_RANGE_SENSOR_Y, FRONT_RANGE_SENSOR_Z),
}


MASS_ROWS = [
    ("RP01_HEAD_LAYOUT04", HEAD_MASS_G, (
        HEAD_ORIGIN_IN_CHASSIS[0] + HEAD_LOCAL_COM[0],
        HEAD_ORIGIN_IN_CHASSIS[1] + HEAD_LOCAL_COM[1],
        HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_LOCAL_COM[2],
    ), "RP-01 generated mass tree"),
    ("BODY_SHELL_AND_PANELS", 285.6, (4.0 + BODY_SHIFT_X, 0.0, 96.0), "Layout 02 CAD estimate; +15 g for the internal panel frames (+15.6 cm3 net printed volume, near-solid 2.4 mm walls); -27.2 g for the -22.7 cm3 of shell floor opened over the motors, battery hatch and pod tongue (RP03-CAD-05/06) at ~1.2 g/cm3; +2.6 g for the ~0.9 cm2 x 2.4 mm of shell floor returned when the battery opening shrank to the 2S1P pack tub (RP03-CAD-07); -4.8 g for the measured -4.04 cm3 when the battery opening grew to clear the hatch flange and tub bosses (2026-10-01)"),
    ("BODY_PRIMARY_FRAME", 335.0, (4.0 + BODY_SHIFT_X, 0.0, 94.0), "Layout 02 CAD estimate incl. mounts"),
    ("CHASSIS_PRIMARY_FRAME", 219.1, (17.71, 0.15, 46.73), "D-033 (2026-10-02): -10.7 g for the ten J05/J06/J16 M3 screws and -3.8 g for their ten M3 x 6 inserts, measured from the solids at 7.9/8.5 g/cm3 (centroids (22.2, 0, 47.1) and (25.6, 0, 45.8)); +3.7 g for the measured +6.52 cm3 printed volume at 0.571 g/cm3 when the deck, rails and crossmember of each end became one module (crossmember fills to the deck underside, filled tongue pockets and screw/insert bores, no J16 ears); was 229.9 g at (18.32, 0.14, 46.71). D-032 (2026-10-02): +0.8 g for the main-fuse bracket on the front deck (column 0.72 + shelf 0.60 cm3 at 0.571 g/cm3, centroid (73.0, 44.0, 67.4)); D-030 (2026-10-01): +21.4 g of newly modeled hardware measured from the solids at 7.9/8.5 g/cm3, centroid (30.4, 0, 46.4): J05/J06/J16/J11A ISO 7380 screws and 14 M3 x 6 inserts, four M2.5 driver screws and inserts; +0.7 g for the measured +1.24 cm3 printed volume at 0.571 g/cm3 (driver posts and tie lugs, wider tongues and rear rail ends, moved J16 ears, hatch strap slots, wider J04 recesses; measured with the since-reverted set-screw recess/cavity growth, under 0.1 g), centroid about (35, 0, 64); was 207.0 g at (16.82, 0, 46.61). 2026-10-01: +0.2 g for the measured +0.29 cm3 when the front hatch bosses moved to the front wall, the bosses were cut to Z 39.5 and the hatch grew 4 mm forward; D-011: -0.3 g for the O5 J10-8 cable bore through the front crossmember and deck at (86, -31); D-010 J04 adds two integrated plate-and-cheek carriers, keyed rail joints, eight modeled M3 x 8 screws and eight 6 mm inserts; estimated +10.2 g total (about +0.7 g printed cheek/key volume and +9.5 g steel/brass hardware, preliminary geometry-density estimate); previous 196.9 g centroid (17.7, 0, 46.8). D-007 axle stack (2026-09-29), +20.9 g at the axle (X 0, Z 42): printed plate + housing replace the flange/boss/diaphragm, +7.24 cm3 measured at ~0.571 g/cm3 (+4.1 g); two 1.2 mm aluminium caps 1.52 cm3 (+4.1 g); eight M3 x 18 cap screws (+10.6 g); eight M3 brass inserts (+1.5 g); face screws M3 x 8 CSK -> M3 x 6 low head (+0.6 g); before that 176.0 g at (19.8, 0, 47.4): +2.1 g for the 2 mm motor-screw diaphragms and the pilot-hole plate (+3.65 cm3) and +1.8 g for four ISO 10642 M3 x 8 face screws (Pololu #4804 axle stack, 2026-09-26); front crossmember moved 13 mm forward to X 80-92, rails and deck extended to X 92 (+2.1 g, +3.3 g), battery-tub front wall added (+1.3 g); before that CAD estimate; 219.8 g before RP03-CAD-05/06, then -53.3 g for the net -93.3 cm3 printed volume at ~45% effective PETG density: axle crossmember and square carriers/gussets removed, flange bosses and gearbox cheeks added, rails split and shortened to X -46, deck opened over the motors and battery, rear crossmember moved 16 mm forward, 11.2 cm3 battery tub added; -1.2 g for the -2.1 cm3 smaller battery tub (RP03-CAD-07)"),
    ("WHEEL_L", 92.5, WHEEL_CENTER_L, "D-008 wheel from wheel/check_wheel.py at solid density: PETG rim, clamp ring and hub cap, TPU tyre, 6 x M3 x 8 ring screws with inserts, one central M3 x 10 cap screw (D-033; six M2 x 6 before, same 92.5 g) (was 87.3 for the D-007 plain rim); the stub and D-007 wheel screws are counted with the axle; CoM kept on the wheel centre, about 1 mm outboard in fact"),
    ("WHEEL_R", 92.5, WHEEL_CENTER_R, "D-008 wheel from wheel/check_wheel.py at solid density: PETG rim, clamp ring and hub cap, TPU tyre, 6 x M3 x 8 ring screws with inserts, one central M3 x 10 cap screw (D-033; six M2 x 6 before, same 92.5 g) (was 87.3 for the D-007 plain rim); the stub and D-007 wheel screws are counted with the axle; CoM kept on the wheel centre, about 1 mm outboard in fact"),
    ("AXLE_BEARINGS_AND_STUB_SHAFTS", 50.4, (0.0, 0.0, AXLE_Z), "D-033: -1.0 g for the M3 tapped hole in each stub's spigot end (hub-cap screw, 0.064 cm3 each at 7.85 g/cm3). D-012 estimate: two turned EN8 stubs with flange and spigot 30.9 g (29.9 g after D-033); four 688 ZZ bearings estimated at 4.05 g each = 16.2 g (weigh on receipt); six M3 x 6 button wheel screws 4.0 g; two M3 set screws, ISO 4029 M3 x 3 faced to 2.5 (D-030), 0.3 g. Symmetric about the centre plane; all masses estimated except measured stub geometry"),
    ("MOTOR_L", 110.0, (0.0, 40.2, AXLE_Z), "E: ThinkRobotics MOT3001-6V230RPM (03-build D-003, 2026-09-28); 110 g is the NFP-JGA25-370-EN figure for the same platform, ThinkRobotics lists 130 g shipping weight, weigh on receipt; Y is the modelled static volume centroid (uniform density, E); was Pololu #4804 101 g at Y 39.2"),
    ("MOTOR_R", 110.0, (0.0, -40.2, AXLE_Z), "E: ThinkRobotics MOT3001-6V230RPM (03-build D-003, 2026-09-28); 110 g is the NFP-JGA25-370-EN figure for the same platform, ThinkRobotics lists 130 g shipping weight, weigh on receipt; Y is the modelled static volume centroid (uniform density, E); was Pololu #4804 101 g at Y -39.2"),
    ("BALL_TRANSFER", 16.5, (BALL_CONTACT[0], 0.0, 14.0), "vendor"),
    ("BALLAST_STEEL_BAR", round(BALLAST_BAR_G + BALLAST_SCREWS_G, 1), (sum(BALLAST_X) / 2.0, 0.0, sum(BALLAST_Z) / 2.0), "E: mild-steel bar 9 x 60 x 19 mm at 7.85 g/cm3 (less two M3 tapped holes) + two M3 screws; sized so the register CoM clears the physics.md 2.5 line after the 110 g pack (RP03-CAD-08)"),
    ("BATTERY", 108.2, BATTERY_CENTER, "E: 2 x Samsung INR18650-25R (45 g max each = 90 g) + RP-02 PCB-01 pack-protection assembly (~5 g: 48 x 20 mm board 3.7 g + parts 1.3 g) + Bourns AC72ABD thermal cutoff and NTC (~0.7 g) + nickel straps, sleeve and AWG16 leads (~11 g) + pack-side Micro-Fit+ 1x2 half with terminals (~1.5 g, CN-05; was a ~6 g SBS Mini half); working selection, no purchase or measured mass; was 110 g with a generic ~8 g BMS (RP-02 board-specs.md sec 3, 2026-09-25)"),
    ("RASPBERRY_PI5_AND_COOLER", 76.0, PI_CENTER, "vendor + estimate"),
    # Replaces the single CONTROL_POWER_SENSORS row (121.5 g at (22, 0, 80), 2026-09-25). Masses are the RP-02
    # board-specs.md sec 2 / WS-H estimates (PCB 1.6 mm FR4 with copper about 3.8 g per 1000 mm2 plus the parts
    # inventory), not measurements; positions are the centres of the proposal boxes.
    ("PCB02_CHARGE_AND_SYSTEM_POWER", 18.0, ((PCB02_BOX[0] + PCB02_BOX[1]) / 2.0, 0.0, (PCB02_BOX[4] + PCB02_BOX[5]) / 2.0), "E (proposal): 50 x 36 mm board 6.8 g + USB-C 1.2 + connectors 3 + inductor 2 + capacitors 3 + ICs 0.6 + misc 1; vertical on the rear-panel frame"),
    ("PACK_INTERFACE_MICROFIT_PLUS_AND_FUSE", 11.0, tuple((3.0 * (PACK_DISCONNECT_PAIR_BOX[2 * i] + PACK_DISCONNECT_PAIR_BOX[2 * i + 1]) / 2.0 + 8.0 * (PACK_FUSE_HOLDER_BOX[2 * i] + PACK_FUSE_HOLDER_BOX[2 * i + 1]) / 2.0) / 11.0 for i in range(3)), "E: Micro-Fit+ 1x2 wire-to-wire pair with terminals ~3 g + ATOF 15 A holder and fuse ~6 g + ~2 g; was 14 g with an unplaced SBS Mini (CN-05)"),
    ("PCB03_MOTOR_GATE_AND_HEAD_RAIL", 24.0, (sum(PCB03_BOX[0:2]) / 2.0, 0.0, sum(PCB03_BOX[4:6]) / 2.0), "E (proposal): 2460 mm2 board 9.4 g + 4 x Micro-Fit+ 8 + inductor 3 + capacitors 2 + FETs, shunt, TVS, misc 1.6"),
    ("PCB04_BRANCH_CONVERTERS", 45.0, (sum(PCB04_BOX[0:2]) / 2.0, 0.0, sum(PCB04_BOX[4:6]) / 2.0), "E (proposal): WS-H 35 g (3080 mm2 board 11.7 g + inductors 5.4 + connectors 8 + ICs 1 + polymer/ceramics ~1) with the hold-up raised from 4 x 1 mF (~8 g) to 2 x 3.3 mF (~9 g each, Ø12.5 x 20 lying) per board-specs.md sec 8.1: +10 g; the board footprint is NOT enlarged (no slack in the bay)"),
    ("C3_DEVKITC_N8", 9.0, (sum(C3_CARRIER_BOARD[0:2]) / 2.0, C3_CARRIER_BOARD[3] + C3_DEVKIT_STANDOFF + 2.75, C3_DEVKIT_Z[0] + 14.15), "E: ESP32-S3-DevKitC-1-N8 board; moved 2026-09-26 onto the PCB-10 carrier on the -Y side wall"),
    ("C3_CARRIER_PCB10", 20.0, (sum(C3_CARRIER_BOARD[0:2]) / 2.0, C3_CARRIER_BOARD[2] - 1.0, sum(C3_CARRIER_BOARD[4:6]) / 2.0), "E (proposal): 70 x 43.5 mm board ~8.5 g + THVD1451, TPS3436, READY logic, SLEEP FETs ~1 g + 2 x 22-pin headers ~3 g + 10 GH and 1 Micro-Fit 3.0 header ~3 g + four M2.5 screws and inserts ~1 g; two printed uprights on the -Y rails ~3.5 g"),
    ("YAW_JUNCTION_PCB08", 4.0, (sum(YAW_JUNCTION_BOX[0:2]) / 2.0, sum(YAW_JUNCTION_BOX[2:4]) / 2.0, 116.0), "E: 32 x 21 mm board ~2 g + Micro-Fit 3.0 2x3 (D-039) and three GH headers ~2 g"),
    ("C0_LINK_ADAPTER_PCB09", 7.0, (30.0, 32.0, 107.5), "E: strip-and-wide board ~3 g + 2 x 20 socket ~2 g + 2 x THVD1451 and three GH headers ~2 g"),
    ("BATTERY_RESTRAINT", 3.4, (46.36, 0.0, 40.63), "D-030 J11B, measured from the solids: two 10 x 1.2 mm hook-and-loop strap loops at ~1.1 g/cm3 (3.3 g) and two 1.5 mm closed-cell foam pads at ~0.1 g/cm3 (0.05 g); estimate, not weighed"),
    ("ADAFRUIT_DRV8833_CARRIERS_X2", 6.0, (DRIVER_CENTER_X, 0.0, 68.5), "E: 2 x Adafruit #3297 boards, 25.4 x 17.8 mm board-file outline with the 3.5 mm terminal block fitted (10.1 mm tall), 3 g each; mass unmeasured"),
    ("IMU_PCB07", 2.5, (IMU_BOARD_CENTER[0], 0.0, IMU_BOARD_CENTER[2] + 1.0), "E: PCB-07 16 x 20 x 1.0 mm FR4 ~0.6 g + ICM-42688-P and JST-SH 8-pin ~0.3 g + two M2 x 5 ~0.6 g + 8-way AWG30 lead to C3 ~1 g (RP03-CAD-11); was a 2 g breakout estimate at (16, 0, 60)"),
    ("TCRT5000_BREAKOUT_AND_CABLE", 3.0, TCRT_REAR_CENTER, "E: TCRT5000 with a soldered 350 mm 4-core J10-10 GH lead (CH-020) and heat-shrink (D-016) (most of it rises to the C3 carrier; lumped at the sensor); was inside the old CONTROL_POWER_SENSORS row at the body centre"),
    ("ESTOP_XA1E_BV3U02KT_R", 14.0, ((5.0 * (ESTOP_MOUNT_X - ESTOP_MUSHROOM_TOP_ABOVE_MOUNT + 4.0) + 9.0 * (ESTOP_KEEP_OUT[0] + ESTOP_KEEP_OUT[1]) / 2.0) / 14.0, 0.0, ESTOP_CENTER_Z), "D: IDEC XA unibody Ø29 mushroom 14 g (XA datasheet); ~5 g mushroom and collar outside the well floor, ~9 g contact block behind it. Replaced the XW1E-BV402M-R row (40 g) on 2026-09-25. The rear-panel well and bezel add a net 0.14 cm3 (~0.2 g) of print, not booked"),
    ("BALL_NOSE_POD_SENSOR_CAP", 18.9, (111.4, 0.0, 37.9), "D-027: +0.2 g for the lid lead hump, raised nose top and wider front pocket (pod 12.45, lid 2.62, cap 2.12 cm3 measured, was 12.44/2.45/2.03, at ~0.571 g/cm3); earlier estimate predates the selected A21 sensor (3.6 g datasheet, ears trimmed), custom Hall carrier and O3 x 1.5 magnet; weigh received parts"),
    ("BODY_AUDIO", 60.0, (77.9, 0.0, 101.9), "RP03-CAD-11: Visaton K 50 WP 48 g (D) with its centroid at the magnet end, X ~85 + PCB-05 30 x 38 mm board and parts ~6 g (E) at (60, 0, 116) + four PCB-06 mic boards ~0.5 g each (E) + speaker leads and mic cables ~4 g (E); was 90 g at (64, 0, 102) for unselected parts"),
    ("HARNESS_AND_FASTENERS", 95.0, (4.0 + BODY_SHIFT_X, 0.0, 88.0), "estimate"),
    ("BODY_YAW_STAGE", 89.0, (BODY_AXIS_X, 13.5, 134.3), "E: 50 g thin-section bearing placeholder + 23 g XC330-M181 + 6 g driven spur + 6 g scissor pinion (two 2.4 mm halves) + 1 g torsion spring and retaining clip (2026-09-25) + 2 g clamp ring + 1 g coupling shaft; no SKU"),
    ("REAR_SKID_KEEL", 20.0, (-40.5, 0.0, 22.7), "J09/J10 rework 2026-09-30 (D-014, D-016), measured from the solids: keel body 14.64 cm3 at ~0.571 g/cm3 = 8.4 g at (-39.7, 0, 20.4) (D-016 closed the board cavity back to the sensor pocket); shoe 0.40, bezel with guard lips 0.30 and two 1 mm shims 0.24 cm3 printed solid at ~1.27 g/cm3 = 1.2 g; four ISO 4762 M3 x 30 ~8.4 g; four CNC Kitchen M3 x 5.7 crossmember inserts ~1.4 g; M2 x 10 and M2 x 6 screws ~0.6 g (the M2 x 5 board screw was dropped by D-015). Was 12.0 g at (-39.9, 0, 20.4); rear-crossmember cable bore closed and tie lug added (<0.1 g, left in the frame row)"),
]
def mass_properties():
    total = sum(row[1] for row in MASS_ROWS)
    com = tuple(sum(row[1] * row[2][axis] for row in MASS_ROWS) / total for axis in range(3))
    return {"mass_g": total, "com_mm": com}


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _paint(shape, label: str, color: str, alpha: float = 1.0):
    shape.label = label
    children = list(shape.children) if getattr(shape, "children", None) else []
    if children:
        for index, child in enumerate(children, start=1):
            _paint(child, child.label or f"{label}_{index:02}", color, alpha)
    else:
        shape.color = srgb(color, alpha)
    return shape


def _block(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(
        Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0))
    )


def _box(dx, dy, dz, center, label, color, alpha=1.0):
    return _paint(
        Box(dx, dy, dz).moved(Location(center)),
        label,
        color,
        alpha,
    )


def _cylinder(radius, height, center, label, color, alpha=1.0, axis="z"):
    # Construct at the origin with a true three-axis centre.  Translating a
    # default MIN-aligned cylinder before rotation compounds its half-height
    # offset into world Y/X and makes mirrored parts asymmetric.
    shape = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    if axis == "x":
        shape = shape.rotate(Axis.Y, 90.0)
    elif axis == "y":
        shape = shape.rotate(Axis.X, -90.0)
    return _paint(shape.moved(Location(center)), label, color, alpha)


def _wheel_well_tools():
    """Tyre swept-volume cutters at the frozen wheel/axle datums."""
    radius = WHEEL_OD / 2.0 + WHEEL_WELL_RADIAL_CLEARANCE
    width = WHEEL_WIDTH + 2.0 * WHEEL_WELL_SIDE_CLEARANCE
    return [
        _cylinder(radius, width, center, f"WHEEL_WELL_TOOL_{side}", "#FFFFFF", 1.0, "y")
        for side, center in (("L", WHEEL_CENTER_L), ("R", WHEEL_CENTER_R))
    ]


def _sphere(radius, center, label, color, alpha=1.0):
    return _paint(Sphere(radius).moved(Location(center)), label, color, alpha)


def _center_at(shape, center):
    c = tuple(shape.bounding_box().center())
    return shape.moved(Location((center[0] - c[0], center[1] - c[1], center[2] - c[2])))


def _purchased_step(filename, label, rotations=(), folder=PURCHASED):
    """Import a vendor STEP from the purchased folder and apply (axis, deg) turns."""
    part = import_step(str(folder / filename))
    for axis, angle in rotations:
        part = part.rotate(axis, angle)
    solids = list(part.solids())
    if len(solids) > 1:
        # Booleans on a nested imported assembly can read child placements as
        # local (false clashes); flat world-located solids intersect correctly.
        part = Compound(label=label, children=solids)
    part.label = label
    return part


def _place(shape, x=None, y=None, z=None, ref="center"):
    """Move so the bounding box hits x/y/z (`ref`: center, min or max on the given axes)."""
    box = shape.bounding_box()
    delta = []
    for axis, target in zip("XYZ", (x, y, z)):
        lo, hi = getattr(box.min, axis), getattr(box.max, axis)
        current = {"center": (lo + hi) / 2.0, "min": lo, "max": hi, "origin": 0.0}[ref if not isinstance(ref, dict) else ref.get(axis, "center")]
        delta.append(0.0 if target is None else target - current)
    moved = shape.moved(Location(tuple(delta)))
    solids = list(moved.solids())
    if len(solids) > 1:
        # Re-flatten after the move so each solid carries its world placement.
        moved = Compound(label=shape.label, children=solids)
    return moved


def _gh_header(circuits, label, rotations=(), top_entry=False):
    """JST GH header (step.parts, KiCad-derived STEP).

    Side entry SMxxB-GHS-TB: width along X, mating face on -Y, 4.25 tall.
    Top entry BMxxB-GHS-TBT: width along X, 4.96 deep in Y, 4.2 tall, mates from +Z.
    Board plane at Z 0 in both.
    """
    name = (f"jst_gh_bm{circuits:02d}b_ghs_tbt_1x{circuits:02d}_1mp_p1_25mm_vertical.step" if top_entry
            else f"jst_gh_sm{circuits:02d}b_ghs_tb_1x{circuits:02d}_1mp_p1_25mm_horizontal.step")
    part = _purchased_step(name, label, rotations)
    return _paint(part, label, "#E9E3D0", 1.0)


GH_PLUG_THICKNESS = 4.15  # GHR housing (D)
GH_PLUG_PROUD = 3.2  # housing beyond the header face when mated (E)


def gh_plug_width(circuits):
    return 1.25 * circuits + 1.25  # GHR-xxV-S dimension B (D)


def _cid(cid):
    return cid.replace("-", "_")


def _beam_xz(x0, z0, x1, z1, width, thickness, label, color):
    """Rectangular structural member centred between two XZ datum points."""
    dx = x1 - x0
    dz = z1 - z0
    length = math.hypot(dx, dz)
    angle = math.degrees(math.atan2(-dz, dx))
    beam = Box(length, width, thickness).rotate(Axis.Y, angle)
    beam = beam.moved(Location(((x0 + x1) / 2.0, 0.0, (z0 + z1) / 2.0)))
    return _paint(beam, label, color, 1.0)


def _axial_bore_x(radius, x0, x1, y, z):
    return Cylinder(radius, x1 - x0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(
        Axis.Y, 90.0
    ).moved(Location(((x0 + x1) / 2.0, y, z)))


def _axial_bore_y(radius, y0, y1, x, z):
    low, high = sorted((y0, y1))
    return Cylinder(radius, high - low, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(
        Axis.X, -90.0
    ).moved(Location((x, (low + high) / 2.0, z)))


def _nose_profile(x, half_width, z0, z1, chamfer):
    points = [
        (-half_width + chamfer, z0),
        (half_width - chamfer, z0),
        (half_width, z0 + chamfer),
        (half_width, z1 - chamfer),
        (half_width - chamfer, z1),
        (-half_width + chamfer, z1),
        (-half_width, z1 - chamfer),
        (-half_width, z0 + chamfer),
    ]
    return (Plane.YZ * Polygon(*points, align=None)).moved(Location((x, 0.0, 0.0)))


def _octagon_profile(x, half_width, z0, z1, lower_chamfer, upper_chamfer):
    """Eight-sided YZ section at X; lower_chamfer 0 leaves square bottom corners."""
    points = [(half_width, z1 - upper_chamfer), (half_width - upper_chamfer, z1),
              (-half_width + upper_chamfer, z1), (-half_width, z1 - upper_chamfer)]
    if lower_chamfer > 0.0:
        points += [(-half_width, z0 + lower_chamfer), (-half_width + lower_chamfer, z0),
                   (half_width - lower_chamfer, z0), (half_width, z0 + lower_chamfer)]
    else:
        points += [(-half_width, z0), (half_width, z0)]
    return (Plane.YZ * Polygon(*points, align=None)).moved(Location((x, 0.0, 0.0)))


def _pod_face(x, hw, top_z, upper_chamfer, grow=0.0):
    """Octagonal prow section at X; `grow` offsets every edge (cap cavity and skin)."""
    face = _octagon_profile(x, hw, BALL_POD_Z0, top_z, BALL_POD_LOWER_CHAMFER, upper_chamfer)
    if grow:
        face = offset(face, grow, kind=Kind.INTERSECTION).faces()[0]
    return face


def _ball_pod_solid():
    """Pod + lid outer solid: a ruled loft of the prow stations, crossmember to face."""
    return loft([_pod_face(*station) for station in BALL_POD_STATIONS], ruled=True)


def _lid_below():
    """Everything under the lid underside (level over the belt, stepped down over the lens)."""
    points = list(BALL_POD_LID_UNDERSIDE) + [(BALL_POD_LID_UNDERSIDE[-1][0], 20.0), (BALL_POD_LID_UNDERSIDE[0][0], 20.0)]
    return extrude(Plane.XZ * Polygon(*points, align=None), amount=80.0).moved(Location((0.0, -40.0, 0.0)))


def _z_cylinder(radius, z0, z1, x, y):
    """Vertical cylinder spanning exactly z0..z1."""
    return Cylinder(radius, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))


def ball_screw_points():
    return [
        (
            BALL_CONTACT[0] + BALL_HOLE_RADIUS * math.cos(math.radians(angle)),
            BALL_HOLE_RADIUS * math.sin(math.radians(angle)),
        )
        for angle in BALL_HOLE_ANGLES_DEG
    ]


def ball_pod():
    """Printed pod: seats on the vendor flange, bolts to the front crossmember."""
    x0, x1 = BALL_POD_X
    z0 = BALL_POD_Z0
    floor_z = z0 + BALL_POD_SEAT_THICKNESS
    pod = _ball_pod_solid() & _lid_below()
    pocket_x0, pocket_hw = BALL_POD_POCKET
    pod = pod - _block(BALL_POD_NECK_X1, FRONT_RANGE_BODY_FRONT_X + 0.2, -pocket_hw, pocket_hw, floor_z, BALL_POD_LID_Z[1] + 1.0)
    # Behind the belt the 45 deg upper chamfer crosses the pocket wall at Z 47, which left an open
    # slit under the lid. The pocket narrows at 45 deg above the pod screw heads instead (D-011).
    nz0, nhw = BALL_POD_POCKET_NECK
    neck = Plane.YZ * Polygon(
        (-pocket_hw, floor_z), (pocket_hw, floor_z), (pocket_hw, nz0), (nhw, nz0 + pocket_hw - nhw), (nhw, BALL_POD_LID_Z[1] + 1.0),
        (-nhw, BALL_POD_LID_Z[1] + 1.0), (-nhw, nz0 + pocket_hw - nhw), (-pocket_hw, nz0), align=None,
    )
    pod = pod - extrude(neck.moved(Location((pocket_x0, 0.0, 0.0))), amount=BALL_POD_NECK_X1 - pocket_x0 + 0.01)
    # Ahead of the sensor body only the lens hood needs room.
    fw = FRONT_RANGE_POCKET_HALF_WIDTH
    pod = pod - _block(FRONT_RANGE_BODY_FRONT_X, x1 + 1.0, -fw, fw, floor_z, BALL_POD_LID_Z[1] + 1.0)
    # The sensor's belt (44 mm across its ear flange, x 111.8-119.4) sits in stepped side slots.
    for ex0, ex1, ey0, ey1, ez0, ez1 in BALL_POD_EAR_SLOTS:
        for sign in (1.0, -1.0):
            pod = pod - _block(ex0, ex1, *sorted((sign * ey0, sign * ey1)), ez0, ez1)
    # Caster inserts, pressed from the seat face; the flange face bears on them.
    for x, y in ball_screw_points():
        pod = pod - _z_cylinder(M3_INSERT_BORE_RADIUS, z0 - 1.0, floor_z + 0.01, x, y)
    for y, z in BALL_POD_SCREWS_YZ:
        pod = pod - _axial_bore_x(1.65, x0 - 1.0, pocket_x0 + 1.0, y, z)
    # J10-8 cable channel out through the back wall, and the switch-pair groove.
    cx0, cx1, cy0, cy1, cz0, cz1 = POD_CABLE_CHANNEL
    r = POD_CABLE_CORNER
    yc, zc = (cy0 + cy1) / 2.0, (cz0 + cz1) / 2.0

    def _slot_face(x, grow):
        return (Plane.YZ * RectangleRounded(cy1 - cy0 + 2.0 * grow, cz1 - cz0 + 2.0 * grow, r + grow)).moved(Location((x, yc, zc)))

    # Through the back wall: round-cornered section with a 1 mm flared mouth on the outside.
    pod = pod - extrude(_slot_face(cx0, 0.0), amount=pocket_x0 + 0.5 - cx0)
    pod = pod - loft([_slot_face(x0 - 0.01, 1.0), _slot_face(x0 + 1.0, 0.0)], ruled=True)
    # Inside the pocket: an open trough with a rounded floor.
    trough = (Plane.YZ * RectangleRounded(cy1 - cy0, cz1 - cz0 + 2.0 * r, r)).moved(Location((pocket_x0, yc, zc + r)))
    pod = pod - extrude(trough, amount=cx1 - pocket_x0)
    pod = pod - _block(*POD_SWITCH_GROOVE)
    pod = pod - _block(POD_SWITCH_GROOVE[0], POD_SWITCH_GROOVE[0] + 3.0, cy0, POD_SWITCH_GROOVE[3], POD_SWITCH_GROOVE[4], floor_z + 0.01)
    # Hall board slot (open at the top) and the sensor notch through the seat's front face.
    bx0, bx1, by0, by1, bz0, bz1 = NOSE_HALL_BOARD
    c = NOSE_HALL_SLOT_CLEARANCE
    pod = pod - _block(bx0 - c, bx1 + c, by0 - c, by1 + c, bz0 - c, floor_z + 0.01)
    ny0, ny1, nz0 = NOSE_HALL_NOTCH
    pod = pod - _block(bx1, x1 + 1.0, ny0, ny1, nz0, floor_z + 0.01)
    # Return-spring pockets in the seat's front face.
    sr, sx0 = NOSE_SPRING_POCKET
    for y, z in NOSE_SPRING_YZ:
        pod = pod - _axial_bore_x(sr, sx0, x1 + 1.0, y, z)
    # Lid tongue groove, open forward into the pocket.
    tx0, tx1, ty0, ty1, tz0, tz1 = LID_TONGUE
    c = LID_TONGUE_CLEARANCE
    pod = pod - _block(tx0 - c, pocket_x0 + 0.5, ty0 - c, ty1 + c, tz0 - c, tz1 + 1.0)
    # Front lid-screw boss, fused to the -Y wall, with an M2 thread-forming pilot.
    lx, ly = LID_SCREW_XY
    boss_top = _lid_underside_z(lx)
    boss = _z_cylinder(LID_BOSS_RADIUS, floor_z - 0.5, boss_top, lx, ly) + _block(lx - LID_BOSS_RADIUS, lx + LID_BOSS_RADIUS, -(pocket_hw + 0.5), ly, floor_z - 0.5, boss_top)
    pod = pod + (boss & _lid_below())
    pod = pod - _z_cylinder(0.8, floor_z + 1.0, boss_top + 0.01, lx, ly)
    # Snap slots for the touch cap's fingers.
    sx0, sx1, sy, sz0, sz1 = TACTILE_SNAP_SLOT
    for sign in (1.0, -1.0):
        pod = pod - _block(sx0, sx1, *sorted((sign * sy, sign * 30.0)), sz0, sz1)
    return _paint(pod, "BALL_POD_PRINTED_SEAT", SLATE, 1.0)


def _lid_underside_z(x):
    pts = BALL_POD_LID_UNDERSIDE
    for (xa, za), (xb, zb) in zip(pts, pts[1:]):
        if xa <= x <= xb:
            return za + (zb - za) * (x - xa) / (xb - xa)
    raise ValueError(x)


def ball_pod_lid():
    lid = _ball_pod_solid() - _lid_below()
    # D-027: hump over the GP2Y header and its soldered J10-8 lead.
    outer, cavity = _gp2y_lead_hump()
    lid = lid + outer - cavity
    lid = lid + _block(*LID_TONGUE)
    lx, ly = LID_SCREW_XY
    top = BALL_POD_STATIONS[-1][2]
    lid = lid - _z_cylinder(1.1, _lid_underside_z(lx) - 1.0, top + 1.0, lx, ly)
    csk = Cone(0.0, LID_SCREW_HEAD_RADIUS + 0.1, LID_SCREW_HEAD_RADIUS + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lid = lid - csk.moved(Location((lx, ly, top - LID_SCREW_HEAD_RADIUS - 0.1)))
    lid = lid - _z_cylinder(LID_SCREW_HEAD_RADIUS + 0.1, top, top + 1.0, lx, ly)
    return _paint(lid, "BALL_POD_SENSOR_LID", SLATE, 1.0)


def nose_hall_element_x():
    return NOSE_HALL_BOARD[1] + NOSE_HALL_PACKAGE[0] - NOSE_HALL_ELEMENT_DEPTH


def _nose_sensing_parts():
    """Hall board and sensor in the seat, magnet in the cap, two return springs (D-013)."""
    bx0, bx1, by0, by1, bz0, bz1 = NOSE_HALL_BOARD
    h, length, width, span = NOSE_HALL_PACKAGE
    yc, zc = NOSE_HALL_CENTER_YZ
    board = _paint(_block(bx0, bx1, by0, by1, bz0, bz1), "BALL_NOSE_HALL_CARRIER_PCB", PCB_GREEN, 1.0)
    sensor = _block(bx1, bx1 + h, yc - length / 2.0, yc + length / 2.0, zc - width / 2.0, zc + width / 2.0)
    sensor += _block(bx1, bx1 + 0.3, yc - length / 2.0 + 0.3, yc + length / 2.0 - 0.3, zc - span / 2.0, zc + span / 2.0)
    sensor = _paint(sensor, "BALL_NOSE_HALL_DRV5055A3_SOT23", "#2B2B2B", 1.0)
    mr, ml = NOSE_MAGNET
    magnet = _paint(_axial_bore_x(mr, TACTILE_CAP_INNER_X, TACTILE_CAP_INNER_X + ml, yc, zc), "BALL_NOSE_MAGNET_D3X1P5_N35", "#9A9FA6", 1.0)
    r_out, wire, _free = NOSE_SPRING
    springs = [
        _paint(_axial_bore_x(r_out, NOSE_SPRING_POCKET[1], TACTILE_CAP_INNER_X, y, z) - _axial_bore_x(r_out - wire, NOSE_SPRING_POCKET[1] - 0.1, TACTILE_CAP_INNER_X + 0.1, y, z),
               f"BALL_NOSE_RETURN_SPRING_{side}", STEEL, 1.0)
        for (y, z), side in zip(NOSE_SPRING_YZ, ("L", "R"))
    ]
    return board, sensor, magnet, springs


def ball_pod_hardware():
    floor_z = BALL_POD_Z0 + BALL_POD_SEAT_THICKNESS
    parts = []
    head_r, head_h = AXLE_BUTTON_HEAD
    bearing_z = BALL_POD_Z0 - BALL_FLANGE_WEB  # counterbore floor in the vendor base
    for index, (x, y) in enumerate(ball_screw_points(), start=1):
        # ISO 7380 dome, approximated as a 0.35 mm rim plus a cone to the O3.2 top.
        head = _z_cylinder(head_r, bearing_z - 0.35, bearing_z, x, y) + Cone(
            1.6, head_r, head_h - 0.35, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((x, y, bearing_z - head_h)))
        parts.append(_paint(head, f"BALL_M3_HEAD_{index}", STEEL, 1.0))
        parts.append(_paint(_z_cylinder(1.35, bearing_z, bearing_z + BALL_SCREW_LENGTH, x, y), f"BALL_M3_SHANK_{index}", STEEL, 1.0))
        insert = _z_cylinder(M3_INSERT_OD_RADIUS, BALL_POD_Z0, BALL_POD_Z0 + M3_INSERT_LENGTH, x, y) - _z_cylinder(1.25, BALL_POD_Z0 - 0.1, BALL_POD_Z0 + M3_INSERT_LENGTH + 0.1, x, y)
        parts.append(_paint(insert, f"BALL_SEAT_HEATSET_INSERT_{index}", BRONZE, 1.0))
    pocket_x0 = BALL_POD_POCKET[0]
    x0 = BALL_POD_X[0]
    for index, (y, z) in enumerate(BALL_POD_SCREWS_YZ, start=1):
        parts.append(_cylinder(head_r, head_h, (pocket_x0 + head_h / 2.0, y, z), f"BALL_POD_M3_HEAD_{index}", STEEL, 1.0, "x"))
        parts.append(_cylinder(1.35, BALL_POD_SCREW_LENGTH, (pocket_x0 - BALL_POD_SCREW_LENGTH / 2.0, y, z), f"BALL_POD_M3_SHANK_{index}", STEEL, 1.0, "x"))
        insert = _axial_bore_x(M3_INSERT_OD_RADIUS, x0 - M3_INSERT_LENGTH, x0, y, z) - _axial_bore_x(1.25, x0 - M3_INSERT_LENGTH - 0.1, x0 + 0.1, y, z)
        parts.append(_paint(insert, f"BALL_POD_HEATSET_INSERT_{index}", BRONZE, 1.0))
    lx, ly = LID_SCREW_XY
    top = BALL_POD_STATIONS[-1][2]
    head_depth = LID_SCREW_HEAD_RADIUS - 1.0
    lid_screw = Cone(1.0, LID_SCREW_HEAD_RADIUS, head_depth, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(Location((lx, ly, top)))
    lid_screw += _z_cylinder(0.95, top - LID_SCREW_LENGTH, top - head_depth, lx, ly)
    parts.append(_paint(lid_screw, "BALL_POD_LID_M2X8_CSK_SCREW", STEEL, 1.0))
    return Compound(label="BALL_POD_HARDWARE", children=parts)


def rear_skid_tcrt_keel():
    """Compact faceted keel under the rear crossmember: skid shoe + TCRT."""
    tx, ty, tz = TCRT_REAR_CENTER
    keel = loft(
        [_nose_profile(x, half_width, z0, z1, chamfer) for x, half_width, z0, z1, chamfer in REAR_KEEL_STATIONS],
        ruled=True,
    )
    belly = REAR_TCRT_BELLY_Z
    face_z = belly - REAR_TCRT_SHIMS_NOMINAL * REAR_TCRT_SHIM_T
    assert abs(face_z - TCRT_OPTICAL_FACE_Z) < 1e-9, "nominal shim stack must set the optical datum"
    px0, px1, py0, py1 = REAR_TCRT_POCKET
    (fsx, fsy), (fpx, fpy) = REAR_TCRT_FIX_POINTS
    cuts = [
        # Sensor pocket, open below the belly so the TCRT drops out from
        # below, and up through the keel top for the soldered lead.
        _block(px0, px1, py0, py1, belly - 1.0, REAR_KEEL_TOP_Z + 1.0),
        _z_cylinder(0.8, belly - 1.0, 20.5, fsx, fsy),  # bezel M2 pilot, deep enough for zero shims
        _z_cylinder(1.0, belly - 1.0, 18.5, fpx, fpy),  # O2.0 hole for the O1.8 bezel pin
    ]
    screws = []
    screw_points = rear_keel_screw_points()
    head_r, head_h = REAR_KEEL_SCREW_HEAD
    for index, (x, y) in enumerate(screw_points, start=1):
        seat = REAR_KEEL_HEAD_SEAT_Z[0 if x == REAR_KEEL_SCREWS_X[0] else 1]
        cuts.append(_z_cylinder(1.7, seat - 0.1, REAR_KEEL_TOP_Z + 1.0, x, y))
        cuts.append(_z_cylinder(REAR_KEEL_COUNTERBORE_RADIUS, 0.0, seat, x, y))
        screw = _z_cylinder(head_r, seat - head_h, seat, x, y) + _z_cylinder(1.25, seat, seat + REAR_KEEL_SCREW_LENGTH, x, y)
        screws.append(_paint(screw, f"REAR_KEEL_M3X30_SCREW_{index}", STEEL, 1.0))

    # J10A wear shoe: slides in from the front on a dovetail, stops on the
    # groove end and is held by one M2 across the tongue.
    sx, sy, sz = SKID_SHOE_SIZE
    x0 = SKID_PAD_CENTER[0] - sx / 2.0
    x1 = SKID_PAD_CENTER[0] + sx / 2.0
    y0 = -sy / 2.0
    y1 = sy / 2.0
    c = 2.5
    shoe_top = SKID_SHOE_BOTTOM_Z + sz
    tongue_w0, tongue_w1, tongue_h = REAR_KEEL_SHOE_TONGUE
    gc = REAR_KEEL_SHOE_GROOVE_CLEARANCE

    def dovetail(xa, xb, grow):
        profile = Plane.YZ * Polygon(
            (-(tongue_w0 + grow), shoe_top - 0.01), (tongue_w0 + grow, shoe_top - 0.01),
            (tongue_w1 + grow, shoe_top + tongue_h + grow), (-(tongue_w1 + grow), shoe_top + tongue_h + grow),
            align=None,
        )
        return extrude(profile.moved(Location((xa, 0.0, 0.0))), amount=xb - xa)

    shoe_face = Plane.XY * Polygon(
        (x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c),
        (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c),
        align=None,
    )
    shoe = extrude(shoe_face.moved(Location((0.0, 0.0, SKID_SHOE_BOTTOM_Z))), amount=sz) + dovetail(x0 + 1.0, x1, 0.0)
    screw_z = shoe_top + tongue_h / 2.0
    screw_x = SKID_PAD_CENTER[0]
    seat_y = REAR_KEEL_SHOE_SCREW_SEAT_Y
    shoe = shoe - _axial_bore_y(0.8, -tongue_w1 - 0.1, tongue_w1 + 0.1, screw_x, screw_z)
    shoe = _paint(shoe, "REAR_KEEL_REPLACEABLE_WEAR_SHOE", IVORY, 1.0)
    cuts += [
        dovetail(x0 + 1.0 - gc, x1 + 8.0, gc),  # open at the front, where the belly rises
        _axial_bore_y(1.1, 0.0, seat_y, screw_x, screw_z),
        _axial_bore_y(1.9, seat_y, 12.0, screw_x, screw_z),
    ]
    shoe_screw = _axial_bore_y(1.75, seat_y, seat_y + 1.1, screw_x, screw_z) + _axial_bore_y(0.8, seat_y - 6.0, seat_y, screw_x, screw_z)
    screws.append(_paint(shoe_screw, "REAR_KEEL_SHOE_M2X6_SCREW", STEEL, 1.0))

    keel = _paint(keel - cuts, "REAR_KEEL_FACETED_BODY", REAR_KEEL_COLOR, REAR_KEEL_ALPHA)

    # J09B/J10B: bezel with both guard lips, over the nominal shim stack.
    bx0, bx1 = REAR_TCRT_BEZEL_X
    hy = REAR_TCRT_BEZEL_HALF_Y
    wx0, wx1 = REAR_TCRT_BEZEL_WINDOW_X
    bezel = _block(bx0, bx1, -hy, hy, face_z - REAR_TCRT_BEZEL_T, face_z) - _block(wx0, wx1, py0, py1, 0.0, face_z + 1.0)
    gx0, gx1 = REAR_KEEL_GUARD_X
    for sign in (1.0, -1.0):
        gy = sign * 5.6
        bezel += _block(gx0, gx1, gy - REAR_KEEL_GUARD_WIDTH / 2.0, gy + REAR_KEEL_GUARD_WIDTH / 2.0, TCRT_GUARD_BOTTOM_Z, face_z - REAR_TCRT_BEZEL_T + 0.01)
    bezel += _z_cylinder(0.9, face_z, face_z + 6.0, fpx, fpy)  # moulded locating pin
    bezel -= _z_cylinder(1.1, 0.0, face_z + 0.1, fsx, fsy)
    bezel -= _z_cylinder(1.9, 0.0, face_z - REAR_TCRT_BEZEL_T, fsx, fsy)  # button head recess through the lip
    bezel = _paint(bezel, "REAR_TCRT_BEZEL_WITH_GUARDS", IVORY, 1.0)
    shims = []
    for index in range(REAR_TCRT_SHIMS_NOMINAL):
        z0 = face_z + index * REAR_TCRT_SHIM_T
        shim = _block(bx0, bx1, -hy, hy, z0, z0 + REAR_TCRT_SHIM_T) - _block(px0, px1, py0, py1, 0.0, belly + 1.0)
        shim -= [_z_cylinder(1.1, 0.0, belly + 1.0, x, y) for x, y in REAR_TCRT_FIX_POINTS]
        shims.append(_paint(shim, f"REAR_TCRT_HEIGHT_SHIM_{index + 1}", STEEL, 0.78))
    bezel_screw = _z_cylinder(1.75, face_z - REAR_TCRT_BEZEL_T - 1.1, face_z - REAR_TCRT_BEZEL_T, fsx, fsy) + _z_cylinder(
        0.8, face_z - REAR_TCRT_BEZEL_T, face_z - REAR_TCRT_BEZEL_T + 10.0, fsx, fsy
    )
    screws.append(_paint(bezel_screw, "REAR_TCRT_BEZEL_M2X10_SCREW", STEEL, 1.0))

    cartridge = _tcrt_ski_cartridge("REAR", TCRT_REAR_CENTER)
    lz1 = REAR_TCRT_LEAD_JOINTS[5]
    cable = _paint(_z_cylinder(REAR_TCRT_PIGTAIL_RADIUS, lz1, 35.0, *REAR_TCRT_PIGTAIL_XY), "TCRT_REAR_J10_10_PIGTAIL", "#79C4CB", 0.9)
    floor_interface = Compound(label="REAR_KEEL_FLOOR_INTERFACE", children=[shoe, bezel, *shims])
    hardware = Compound(label="REAR_KEEL_HARDWARE", children=screws)
    return Compound(
        label="REAR_SKID_TCRT_KEEL",
        children=[keel, floor_interface, cartridge, cable, hardware],
    )


def rear_keel_screw_points():
    return [(x, sign * REAR_KEEL_SCREW_Y) for x in REAR_KEEL_SCREWS_X for sign in (1.0, -1.0)]


def rear_crossmember_inserts():
    """J09A: four CNC Kitchen M3 x 5.7 inserts, pressed in from the crossmember underside."""
    z0, z1 = REAR_KEEL_INSERT_Z
    return Compound(label="REAR_CROSSMEMBER_KEEL_INSERTS", children=[
        _paint(_z_cylinder(M3_INSERT_OD_RADIUS, z0, z1, x, y) - _z_cylinder(1.25, z0 - 0.1, z1 + 0.1, x, y), f"REAR_KEEL_HEATSET_INSERT_{index}", BRONZE, 1.0)
        for index, (x, y) in enumerate(rear_keel_screw_points(), start=1)
    ])


def rear_skid_tcrt_module():
    """Selectable rear group containing the under-body skid and TCRT keel."""
    return Compound(label="REAR_SKID_TCRT_MODULE", children=[rear_skid_tcrt_keel()])


def rear_ski_keel():
    """Compatibility alias for checks/scripts written before Layout 01.4."""
    return rear_skid_tcrt_module()


def _station_at(x):
    """Linear interpolation of the prow stations at X (half width, top Z, upper chamfer)."""
    st = BALL_POD_STATIONS
    for (xa, *va), (xb, *vb) in zip(st, st[1:]):
        if xa - 1e-9 <= x <= xb + 1e-9:
            t = (x - xa) / (xb - xa)
            return (x, *[a + (b - a) * t for a, b in zip(va, vb)])
    raise ValueError(x)


def _cap_sections(x_first, grow):
    """Prow stations ahead of the cap's rear edge, grown by `grow` (cap cavity or skin)."""
    stations = [_station_at(x_first)] + [st for st in BALL_POD_STATIONS if st[0] > x_first + 1e-6]
    return [_pod_face(*st, grow=grow) for st in stations]


def tactile_ball_nose():
    """Touch hood sliding on the constant nose: pod seat up to the lid, visor-slit window, snap fingers."""
    inner_x = TACTILE_CAP_INNER_X
    face_x = TACTILE_NOSE_FACE_X
    arm_x0 = TACTILE_CAP_ARM_X0
    gap = TACTILE_CAP_CLEARANCE
    skin = gap + TACTILE_CAP_WALL
    front = BALL_POD_STATIONS[-1]
    outer = loft(_cap_sections(arm_x0, skin), ruled=True)
    outer = outer + extrude(_pod_face(front[0], *front[1:], grow=skin), amount=inner_x - front[0])
    outer = outer + loft([_pod_face(inner_x, *front[1:], grow=skin), _pod_face(face_x, *front[1:], grow=0.8)], ruled=True)
    outer = outer & _block(arm_x0 - 1.0, face_x + 1.0, -60.0, 60.0, BALL_POD_Z0, 80.0)
    cavity = loft(_cap_sections(arm_x0 - 1.0, gap), ruled=True)
    cavity = cavity + extrude(_pod_face(front[0], *front[1:], grow=gap), amount=inner_x - front[0])
    cap = outer - cavity
    cap = cap - _front_range_window(FRONT_RANGE_WINDOW_CLEARANCE, inner_x - 1.0, face_x + 1.0)
    # D-027: top notch from the cap's rear edge so the lid's lead hump clears the 3 mm travel.
    hump = _gp2y_lead_hump()[0].bounding_box()
    cap = cap - _block(arm_x0 - 1.0, hump.max.X + TACTILE_NOSE_TRAVEL + gap, hump.min.Y - gap, hump.max.Y + gap, BALL_POD_LID_Z[1], 80.0)
    # Snap fingers (D-011): a slit ahead of each finger frees it from the open bottom up to
    # Z 45.5; the cap's open rear edge bounds it behind. Hooks ride in the pod's flank slots.
    fx0, fx1 = TACTILE_SNAP_FINGER_X
    hx0, hx1, hx2 = TACTILE_SNAP_HOOK_X
    hz0, hz1 = TACTILE_SNAP_HOOK_Z
    inner_hw = _station_at(BALL_POD_NOSE_X0)[1] + gap
    for sign in (1.0, -1.0):
        cap = cap - _block(fx1, fx1 + TACTILE_SNAP_SLIT, *sorted((sign * (inner_hw - 6.0), sign * 40.0)), BALL_POD_Z0 - 1.0, TACTILE_SNAP_FINGER_TOP_Z)
        tip = TACTILE_SNAP_HOOK_TIP_Y
        hook = Plane.XY * Polygon((hx0, inner_hw), (hx1, tip), (hx2, tip), (hx2, inner_hw + 0.5), (hx0, inner_hw + 0.5), align=None)
        hook = extrude(hook.moved(Location((0.0, 0.0, hz0))), amount=hz1 - hz0, dir=(0.0, 0.0, 1.0))
        cap = cap + (hook if sign > 0 else hook.mirror(Plane.XZ))
    cap = _paint(cap, "BALL_NOSE_TOUCH_CAP", IVORY, TACTILE_CAP_ALPHA)
    mr, ml = NOSE_MAGNET
    cap = cap - _axial_bore_x(mr + 0.03, inner_x - 0.01, inner_x + ml, *NOSE_HALL_CENTER_YZ)
    board, sensor, magnet, springs = _nose_sensing_parts()
    travel = _paint(
        extrude(_pod_face(front[0], *front[1:], grow=gap), amount=inner_x - front[0]),
        "BALL_NOSE_3MM_TRAVEL_RESERVE",
        "#D95FC5",
        0.14,
    )
    travel = travel & _block(BALL_POD_X[1], inner_x + 1.0, -60.0, 60.0, BALL_POD_Z0 - 2.0, 80.0)
    return Compound(label="BALL_NOSE_CONCEALED_CONTACT_MODULE", children=[cap, board, sensor, magnet, *springs, travel])


def _body_profile(x, inset=0.0, width_factor=1.0):
    z0 = BODY_Z_BOTTOM + inset
    z1 = BODY_Z_TOP - inset
    lower = BODY_WIDTH_LOWER * width_factor / 2.0 - inset
    upper = BODY_WIDTH_UPPER * width_factor / 2.0 - inset
    lower_corner = max(5.0, 12.0 - inset)
    upper_corner = max(4.0, 10.0 - inset)
    points = [
        (-lower + lower_corner, z0),
        (lower - lower_corner, z0),
        (lower, z0 + lower_corner),
        (upper, z1 - upper_corner),
        (upper - upper_corner, z1),
        (-upper + upper_corner, z1),
        (-upper, z1 - upper_corner),
        (-lower, z0 + lower_corner),
    ]
    return (Plane.YZ * Polygon(*points, align=None)).moved(Location((x, 0.0, 0.0)))


def _panel_solid(x0, x1, width_bottom, width_top, z0, z1, lower_corner=PANEL_LOWER_CORNER, upper_corner=PANEL_UPPER_CORNER, grow=0.0):
    """Extrude an octagonal service-panel profile on the shell end face.

    ``grow`` offsets the outline normal to every edge (negative shrinks),
    keeping sharp chamfer corners, so an opening or frame stays a constant
    distance from the panel edge all round.
    """
    lb = width_bottom / 2.0
    lt = width_top / 2.0
    lower_corner = min(lower_corner, lb - 1.0, (z1 - z0) / 3.0)
    upper_corner = min(upper_corner, lt - 1.0, (z1 - z0) / 3.0)
    points = [
        (-lb + lower_corner, z0),
        (lb - lower_corner, z0),
        (lb, z0 + lower_corner),
        (lt, z1 - upper_corner),
        (lt - upper_corner, z1),
        (-lt + upper_corner, z1),
        (-lt, z1 - upper_corner),
        (-lb, z0 + lower_corner),
    ]
    face = (Plane.YZ * Polygon(*points, align=None)).moved(Location((x0, 0.0, 0.0)))
    if grow:
        face = offset(face, grow, kind=Kind.INTERSECTION).faces()[0]
    return extrude(face, amount=x1 - x0)


def _service_panel_outline(face, x0, x1, grow=0.0):
    """Front or rear service-panel outline extruded between x0 and x1."""
    if face == "FRONT":
        return _panel_solid(x0, x1, FRONT_PANEL_BOTTOM_WIDTH, FRONT_PANEL_TOP_WIDTH, FRONT_PANEL_Z0, PANEL_Z1, grow=grow)
    return _panel_solid(x0, x1, REAR_PANEL_BOTTOM_WIDTH, REAR_PANEL_TOP_WIDTH, REAR_PANEL_Z0, PANEL_Z1, grow=grow)


def _front_range_window(clearance, x0, x1):
    """Visor slit through the cap: a full-round-ended slot centred on the lens axis."""
    width, height = FRONT_RANGE_WINDOW_SIZE
    width, height = width + 2.0 * (clearance - 1.0), height + 2.0 * (clearance - 1.0)
    r = height / 2.0
    half = width / 2.0 - r
    zc = FRONT_RANGE_SENSOR_Z
    slot = _block(x0, x1, FRONT_RANGE_SENSOR_Y - half, FRONT_RANGE_SENSOR_Y + half, zc - r, zc + r)
    for sign in (1.0, -1.0):
        slot = slot + _axial_bore_x(r, x0, x1, FRONT_RANGE_SENSOR_Y + sign * half, zc)
    return slot


def _panel(x0, x1, width_bottom, width_top, z0, z1, label, color, alpha):
    return _paint(
        _panel_solid(x0, x1, width_bottom, width_top, z0, z1),
        label,
        color,
        alpha,
    )


def _triad(origin, label, scale=18.0):
    x = _cylinder(0.8, scale, (origin[0] + scale / 2, origin[1], origin[2]), f"{label}_X", "#E53935", 0.9, "x")
    y = _cylinder(0.8, scale, (origin[0], origin[1] + scale / 2, origin[2]), f"{label}_Y", "#43A047", 0.9, "y")
    z = _cylinder(0.8, scale, (origin[0], origin[1], origin[2] + scale / 2), f"{label}_Z", "#1E88E5", 0.9, "z")
    hub = _sphere(1.8, origin, f"{label}_ORIGIN", "#212121", 1.0)
    return Compound(label=label, children=[x, y, z, hub])


# ---------------------------------------------------------------------------
# Authored parts and groups
# ---------------------------------------------------------------------------

def body_shell():
    outer = loft(
        [
            _body_profile(BODY_X_REAR, 0.0, REAR_SHELL_END_WIDTH_FACTOR),
            _body_profile(-58.0 + BODY_SHIFT_X, 0.0, 1.00),
            _body_profile(60.0 + BODY_SHIFT_X, 0.0, 1.00),
            _body_profile(BODY_X_FRONT, 0.0, FRONT_SHELL_END_WIDTH_FACTOR),
        ],
        ruled=True,
    )
    inner = loft(
        [
            _body_profile(BODY_X_REAR + SHELL_THICKNESS, SHELL_THICKNESS, REAR_SHELL_END_WIDTH_FACTOR),
            _body_profile(-56.0 + BODY_SHIFT_X, SHELL_THICKNESS, 1.00),
            _body_profile(58.0 + BODY_SHIFT_X, SHELL_THICKNESS, 1.00),
            _body_profile(BODY_X_FRONT - SHELL_THICKNESS, SHELL_THICKNESS, FRONT_SHELL_END_WIDTH_FACTOR),
        ],
        ruled=True,
    )
    shell = outer - inner
    # Openings are the panel outline offset inward by PANEL_OVERLAP: a
    # constant-width sealing land on every edge and clipped corner.
    front_opening = _service_panel_outline("FRONT", BODY_X_FRONT - 6.0, BODY_X_FRONT + 2.0, -PANEL_OVERLAP)
    rear_opening = _service_panel_outline("REAR", BODY_X_REAR - 5.0, BODY_X_REAR + 6.0, -PANEL_OVERLAP)
    # The ball pod's tongue passes the lower front band and runs over the
    # shell floor to the crossmember; the notch is open at the bottom, back to
    # the pod's rear face, so the body still lowers onto the chassis.
    pod_notch = _block(
        BALL_POD_X[0] - FRONT_POD_NOTCH_CLEARANCE,
        BODY_X_FRONT + 1.0,
        -BALL_POD_HALF_WIDTH - FRONT_POD_NOTCH_CLEARANCE,
        BALL_POD_HALF_WIDTH + FRONT_POD_NOTCH_CLEARANCE,
        BODY_Z_BOTTOM - 1.0,
        BALL_POD_LID_Z[1] + FRONT_POD_NOTCH_CLEARANCE,
    )
    microphone_ports = []
    for x, y, z, _name in MICROPHONE_PORTS:
        if y > 0.0:
            microphone_ports.append(_axial_bore_y(1.5, 66.0, 91.0, x, z))
        else:
            microphone_ports.append(_axial_bore_y(1.5, -91.0, -66.0, x, z))
    slot_x0, slot_x1, slot_half = REAR_KEEL_SHELL_SLOT
    floor_z = (BODY_Z_BOTTOM - 1.0, BODY_Z_BOTTOM + SHELL_THICKNESS + 1.0)
    keel_slot = _block(slot_x0, slot_x1, -slot_half, slot_half, *floor_z)
    # The coaxial motors hang below the floor plane (gearbox bottom Z 29.5); a
    # slot across the axle joins the two wheel wells so the body lowers over
    # them. The battery tub's bottom hatch sits in its own opening, which also
    # clears the tub's screw bosses.
    motor_slot = _block(-MOTOR_RELIEF_HALF_X, MOTOR_RELIEF_HALF_X, -MOTOR_FACE_Y - 1.0, MOTOR_FACE_Y + 1.0, *floor_z)
    g = BATTERY_HATCH_GAP
    battery_opening = _block(
        BATTERY_HATCH_X[0] - g, BATTERY_HATCH_X[1] + g, -BATTERY_HATCH_HALF_Y - g, BATTERY_HATCH_HALF_Y + g, *floor_z
    )
    # Head-yaw opening passes the rotating ring-gear skirt; the proud disc
    # covers it with a 1 mm running gap above the body top.
    yaw_opening = Cylinder(YAW_OPENING_RADIUS, 10.0).moved(Location((BODY_AXIS_X, 0.0, BODY_Z_TOP)))
    shell = shell - [
        front_opening, rear_opening, pod_notch, keel_slot, motor_slot, battery_opening, yaw_opening,
        *microphone_ports, *_wheel_well_tools(),
    ]
    return _paint(shell, "BODY_SHELL", IVORY, SHELL_ALPHA)


def body_panels():
    front_raw = _service_panel_outline("FRONT", BODY_X_FRONT, BODY_X_FRONT + SHELL_THICKNESS)
    grille_slots = [
        _block(BODY_X_FRONT - 1.0, BODY_X_FRONT + 4.0, y - 2.25, y + 2.25, 78.0, 116.0)
        for y in (-36.0, -24.0, -12.0, 0.0, 12.0, 24.0, 36.0)
    ]
    front_bores = [
        _axial_bore_x(1.65, BODY_X_FRONT - 2.0, BODY_X_FRONT + 5.0, y, z) for y, z in FRONT_PANEL_FASTENERS
    ]
    front = _paint(
        front_raw - [*grille_slots, *front_bores],
        "FRONT_SERVICE_PANEL_FUNCTIONAL_GRILLE",
        PANEL_WARM_GRAY,
        SHELL_ALPHA,
    )
    rear_raw = _service_panel_outline("REAR", BODY_X_REAR - SHELL_THICKNESS, BODY_X_REAR)
    rear_bores = [
        _axial_bore_x(1.65, BODY_X_REAR - 5.0, BODY_X_REAR + 3.0, y, z)
        for y, z in REAR_PANEL_FASTENERS
    ]
    cw, ch = CHARGE_INLET_CUTOUT
    cy, cz = CHARGE_INLET_CENTER_YZ
    inlet_cutout = _block(BODY_X_REAR - SHELL_THICKNESS - 1.0, BODY_X_REAR + 1.0, cy - cw / 2.0, cy + cw / 2.0, cz - ch / 2.0, cz + ch / 2.0)
    rear = _paint(
        rear_raw - rear_bores - _estop_well_outer() - inlet_cutout,
        "REAR_SERVICE_PANEL_OCTAGONAL",
        IVORY,
        SHELL_ALPHA,
    )
    top_badge = _box(2.0, 30.0, 4.0, (BODY_X_FRONT + 3.4, 0.0, 124.0), "FRONT_BADGE_LAND", AMBER, 0.92)
    wheel_arches = []
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        yc = sign * TRACK / 2.0
        pod_outer = _cylinder(52.0, 18.0, (0.0, yc, AXLE_Z), f"WHEEL_ARCH_OUTER_{side}", IVORY, 1.0, "y")
        pod_inner = _cylinder(46.0, 22.0, (0.0, yc, AXLE_Z), f"WHEEL_ARCH_INNER_{side}", IVORY, 1.0, "y")
        pod = pod_outer - pod_inner - _block(-58.0, 58.0, -105.0, 105.0, -10.0, AXLE_Z)
        pod = _paint(pod, f"WHEEL_ARCH_POD_{side}", IVORY, SHELL_ALPHA)

        outer_face_y = sign * (TRACK / 2.0 + WHEEL_WIDTH / 2.0 + 1.5)
        trim_outer = _cylinder(48.0, 3.0, (0.0, outer_face_y, AXLE_Z), f"WHEEL_ARCH_TRIM_OUTER_{side}", AMBER, 1.0, "y")
        trim_inner = _cylinder(44.0, 5.0, (0.0, outer_face_y, AXLE_Z), f"WHEEL_ARCH_TRIM_INNER_{side}", AMBER, 1.0, "y")
        trim = trim_outer - trim_inner - _block(-56.0, 56.0, -105.0, 105.0, -10.0, AXLE_Z)
        trim = _paint(trim, f"WHEEL_ARCH_UPPER_TRIM_{side}", AMBER, 0.92)
        wheel_arches.append(Compound(label=f"WHEEL_ARCH_{side}", children=[pod, trim]))
    return Compound(label="BODY_PANELS", children=[front, rear, *rear_panel_estop_well(), top_badge, *wheel_arches])


def panel_mount_hardware():
    """Internal panel frames with fused bosses, and front-access M3 screws.

    Each frame sits behind the shell end wall, laps PANEL_FRAME_OUTSET past
    the panel outline and reaches PANEL_FRAME_FLANGE inside it. Its bosses
    stand forward through the shell opening to the panel's inner face.
    """
    speaker_keep_out = _cylinder(
        SPEAKER_BASKET_DIAMETER / 2.0 + 2.0,
        SPEAKER_CAVITY_DEPTH,
        (SPEAKER_CAVITY_CENTER_X, SPEAKER_CENTER[1], SPEAKER_CENTER[2]),
        "SPEAKER_KEEP_OUT_TOOL",
        SLATE,
        1.0,
        "x",
    )
    parts = []
    for face, panel_x0, panel_x1, positions in (
        ("FRONT", BODY_X_FRONT, BODY_X_FRONT + SHELL_THICKNESS, FRONT_PANEL_FASTENERS),
        ("REAR", BODY_X_REAR, BODY_X_REAR - SHELL_THICKNESS, REAR_PANEL_FASTENERS),
    ):
        inward = -1.0 if face == "FRONT" else 1.0
        wall_inner_x = panel_x0 + inward * SHELL_THICKNESS
        frame_back_x = wall_inner_x + inward * PANEL_FRAME_THICKNESS
        boss_back_x = frame_back_x + inward * PANEL_BOSS_TAIL
        fx0, fx1 = sorted((wall_inner_x, frame_back_x))
        frame = _service_panel_outline(face, fx0, fx1, PANEL_FRAME_OUTSET) - _service_panel_outline(
            face, fx0 - 1.0, fx1 + 1.0, -PANEL_FRAME_FLANGE
        )
        bx0, bx1 = sorted((panel_x0, boss_back_x))
        for y, z in positions:
            frame = frame + _cylinder(PANEL_BOSS_RADIUS, bx1 - bx0, ((bx0 + bx1) / 2.0, y, z), "BOSS", SLATE, 1.0, "x")
        for y, z in positions:
            frame = frame - _axial_bore_x(1.4, bx0 - 1.0, bx1 + 1.0, y, z)
        if face == "FRONT":
            frame = frame - speaker_keep_out
        parts.append(_paint(frame, f"{face}_PANEL_INTERNAL_FRAME_WITH_BOSSES", SLATE_DARK, 1.0))
        outer_face_x = panel_x1
        for index, (y, z) in enumerate(positions, start=1):
            head = _cylinder(2.8, 1.8, (outer_face_x - inward * 0.9, y, z), f"{face}_PANEL_M3_HEAD_{index}", STEEL, 1.0, "x")
            shank = _cylinder(
                1.35,
                PANEL_SCREW_LENGTH,
                (outer_face_x + inward * PANEL_SCREW_LENGTH / 2.0, y, z),
                f"{face}_PANEL_M3_SHANK_{index}",
                STEEL,
                1.0,
                "x",
            )
            parts.extend([head, shank])
    return Compound(label="PANEL_MOUNT_HARDWARE", children=parts)


def battery_pack():
    """2S1P of two 18650 cells lying across the robot, BMS board on top.

    Cell axes run along Y. Straps and insulation are one plate at each cell
    end. The BMS lies on the cells with its long side along Y.
    """
    bx, by, bz = BATTERY_CENTER
    z0 = bz - BATTERY_SIZE[2] / 2.0
    r = BATTERY_CELL_DIAMETER / 2.0
    cell_z = z0 + BATTERY_WRAP_T + r
    cells = [
        _cylinder(r, BATTERY_CELL_LENGTH, (bx + dx, by, cell_z), f"BATTERY_CELL_{name}_SAMSUNG_25R_ENVELOPE", "#3D9B62", 1.0, "y")
        for name, dx in (("A", -BATTERY_CELL_PITCH / 2.0), ("B", BATTERY_CELL_PITCH / 2.0))
    ]
    strap_dx = BATTERY_CELL_PITCH + BATTERY_CELL_DIAMETER
    straps = [
        _box(strap_dx, BATTERY_END_STRAP_T, BATTERY_CELL_DIAMETER, (bx, by + sign * (BATTERY_CELL_LENGTH + BATTERY_END_STRAP_T) / 2.0, cell_z), f"BATTERY_END_STRAP_{tag}", STEEL, 1.0)
        for tag, sign in (("FRONT_Y", 1.0), ("REAR_Y", -1.0))
    ]
    bms_z0 = z0 + BATTERY_WRAP_T + BATTERY_CELL_DIAMETER + BATTERY_WRAP_T
    bms = _box(*BATTERY_BMS_SIZE, (bx, by, bms_z0 + BATTERY_BMS_SIZE[2] / 2.0), "BATTERY_BMS_PCB01_PACK_PROTECTION", "#1E6B45", 1.0)
    return Compound(label="BATTERY_2S1P_18650_PACK", children=[*cells, *straps, bms])


def ballast_bar():
    """Steel bar under the deck, ahead of the battery tub (RP03-CAD-08)."""
    bar = _block(*BALLAST_X, -BALLAST_HALF_Y, BALLAST_HALF_Y, *BALLAST_Z)
    for y in BALLAST_SCREW_Y:
        bar = bar - _z_cylinder(1.5, BALLAST_Z[1] - BALLAST_SCREW_HOLE_DEPTH, BALLAST_Z[1] + 0.5, BALLAST_SCREW_X, y)
    parts = [_paint(bar, "BALLAST_STEEL_BAR", STEEL, 1.0)]
    rim_r = BALLAST_SCREW_HEAD[1] / 2.0
    z0, z1 = BALLAST_SCREW_HEAD_Z
    for tag, y in zip(("L", "R"), BALLAST_SCREW_Y):
        # CH-038 CSK head: 90 deg cone to the O5.5 rim, then the rim up to the head top.
        cone = Cone(1.5, rim_r, _BALLAST_HEAD_CONE_H, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((BALLAST_SCREW_X, y, z0)))
        head = cone + _z_cylinder(rim_r, z0 + _BALLAST_HEAD_CONE_H, z1, BALLAST_SCREW_X, y)
        parts.append(_paint(head, f"BALLAST_M3_CSK_HEAD_{tag}", STEEL, 1.0))
        parts.append(_paint(_z_cylinder(1.5, BALLAST_SCREW_TIP_Z, z0, BALLAST_SCREW_X, y), f"BALLAST_M3_SHANK_{tag}", STEEL, 1.0))
    return Compound(label="BALLAST_BAR", children=parts)


def battery_tub(include_walls: bool = True):
    """Chassis tub under the deck: thin walls and a removable bottom hatch.

    The battery lies across the robot between the motors and a thin front
    wall (the front crossmember now sits further forward). The hatch hangs in an
    opening in the shell floor, so the pack drops out downward.
    """
    x0, x1 = BATTERY_TUB_X
    hw = BATTERY_TUB_HALF_Y
    w = BATTERY_TUB_WALL
    fz0, fz1 = BATTERY_TUB_FLOOR_Z
    top = DECK_Z - 2.0
    hatch = _paint(
        _block(*BATTERY_HATCH_X, -BATTERY_HATCH_HALF_Y, BATTERY_HATCH_HALF_Y, fz0, fz1), "BATTERY_TUB_BOTTOM_HATCH", SLATE, 1.0
    )
    walls = _block(x0, x0 + w, -hw, hw, fz1, top) + _block(x1, x1 + w, -hw, hw, fz1, top)
    for sign in (1.0, -1.0):
        walls = walls + _block(x0 + w, x1 + w, *sorted((sign * (hw - w), sign * hw)), fz1, top)
    # Service window in the +Y wall: the pack disconnect slides through it into
    # the emptied tub (connector-schedule.md CN-05).
    wx0, wx1, wz0, wz1 = TUB_SERVICE_WINDOW
    walls = walls - _block(wx0, wx1, hw - w - 1.0, hw + 1.0, wz0, wz1)
    # Four bosses sit outside the thin tub walls (TUB_BOSS_XY). The insert pilots are
    # provisional and must be calibrated with a printed coupon.
    for x, y in TUB_BOSS_XY:
        walls = walls + _block(x - 3.5, x + 3.5, y - 3.5, y + 3.5, fz1, TUB_BOSS_TOP_Z)
        walls = walls - _z_cylinder(2.15, 31.5, 38.5, x, y)
        hatch = hatch - _z_cylinder(1.7, fz0 - 1.0, fz1 + 1.0, x, y)
    # J11B strap slots beside the pack's X faces (D-030).
    sw, st = PACK_STRAP
    cx, cy = PACK_STRAP_SLOT
    for y_abs in (PACK_STRAP_Y, -PACK_STRAP_Y):
        for rx0, rx1 in ((PACK_STRAP_X[0], PACK_STRAP_X[0] + st), (PACK_STRAP_X[1] - st, PACK_STRAP_X[1])):
            hatch = hatch - _block(rx0 - cx, rx1 + cx, y_abs - sw / 2.0 - cy, y_abs + sw / 2.0 + cy, fz0 - 1.0, fz1 + 1.0)
    children = [hatch]
    if include_walls:
        children.append(_paint(walls, "BATTERY_TUB_WALLS", FRAME_BLUE, 1.0))
    return Compound(label="BATTERY_TUB", children=children)


def driver_mount_points():
    """J15B post axes: two per board under its plated holes (D-030, D-031)."""
    return [
        (DRIVER_HOLE_X, sy * (DRIVER_Y + dy))
        for sy in (1.0, -1.0)
        for dy in (-DRIVER_HOLE_HALF_PITCH, DRIVER_HOLE_HALF_PITCH)
    ]


def _frame_insert_z(x, y, z0):
    return _z_cylinder(FRAME_INSERT_RADIUS, z0, z0 + FRAME_INSERT_LENGTH, x, y) - _z_cylinder(1.5, z0 - 0.1, z0 + FRAME_INSERT_LENGTH + 0.1, x, y)


def frame_joint_hardware():
    """J11A hatch screws and boss inserts (D-030). D-033 removed the J05, J06 and J16 hardware."""
    parts = []
    head_r, head_h = AXLE_BUTTON_HEAD
    fz0, fz1 = BATTERY_TUB_FLOOR_Z
    for k, (x, y) in enumerate(TUB_BOSS_XY, start=1):
        screw = _z_cylinder(head_r, fz0 - head_h, fz0, x, y) + _z_cylinder(1.5, fz0, fz0 + J11A_SCREW_LENGTH, x, y)
        parts.append(_paint(screw, f"J11A_HATCH_SCREW_M3X6_{k}", STEEL, 1.0))
        parts.append(_paint(_frame_insert_z(x, y, fz1), f"J11A_BOSS_INSERT_M3_{k}", BRONZE, 1.0))
    return Compound(label="FRAME_JOINT_HARDWARE", children=parts)


def battery_restraint():
    """J11B (D-030): two hook-and-loop straps holding the pack to the hatch, and cell-end foam pads."""
    sw, st = PACK_STRAP
    x0, x1 = PACK_STRAP_X
    z0, z1 = PACK_STRAP_Z
    parts = []
    for side, y_abs in (("L", PACK_STRAP_Y), ("R", -PACK_STRAP_Y)):
        ya, yb = y_abs - sw / 2.0, y_abs + sw / 2.0
        loop = _block(x0, x1, ya, yb, z0, z1) - _block(x0 + st, x1 - st, ya - 1.0, yb + 1.0, z0 + st, z1 - st)
        parts.append(_paint(loop, f"PACK_STRAP_HOOK_LOOP_{side}", "#2B2F33", 1.0))
    inner_y = BATTERY_TUB_HALF_Y - BATTERY_TUB_WALL
    for tag, sy in (("+Y", 1.0), ("-Y", -1.0)):
        fx0, fx1 = PACK_FOAM_X[tag]
        y0, y1 = sorted((sy * (inner_y - PACK_FOAM_T), sy * inner_y))
        parts.append(_paint(_block(fx0, fx1, y0, y1, *PACK_FOAM_Z), f"PACK_FOAM_PAD_{'L' if sy > 0 else 'R'}", "#4A4F57", 1.0))
    return Compound(label="BATTERY_RESTRAINT", children=parts)


def driver_mount_hardware():
    """J15B (D-030): M2.5 inserts in the deck posts and M2.5 x 6 screws through the boards."""
    length, head_r, head_h = DRIVER_SCREW
    top = DRIVER_PCB_Z + PCB_THICKNESS
    parts = []
    for k, (x, y) in enumerate(driver_mount_points(), start=1):
        z0 = DRIVER_PCB_Z - DRIVER_INSERT[1]
        insert = _z_cylinder(DRIVER_INSERT[0], z0, DRIVER_PCB_Z, x, y) - _z_cylinder(1.25, z0 - 0.1, DRIVER_PCB_Z + 0.1, x, y)
        screw = _z_cylinder(head_r, top, top + head_h, x, y) + _z_cylinder(1.25, top - length, top, x, y)
        parts += [_paint(insert, f"DRIVER_POST_INSERT_M25_{k}", BRONZE, 1.0), _paint(screw, f"DRIVER_SCREW_M25X6_{k}", STEEL, 1.0)]
    return Compound(label="DRIVER_MOUNT_HARDWARE", children=parts)


def frame_deck(region: str):
    """Deck of one frame module (D-033); the front deck carries the integral battery tub."""
    x0, x1 = (-41.0, -17.0) if region == "REAR" else (17.0, CHASSIS_RAIL_X1)
    shape = _block(x0, x1, -56.0, 56.0, DECK_Z - 2.0, DECK_Z + 2.0)
    if region == "FRONT":
        bx, by, _bz = BATTERY_CENTER
        bdx, bdy, _bdz = BATTERY_SIZE
        shape -= _block(bx - bdx / 2.0 - 0.5, bx + bdx / 2.0 + 0.5,
                        by - bdy / 2.0 - 0.5, by + bdy / 2.0 + 0.5,
                        DECK_Z - 3.0, DECK_Z + 3.0)
        x0t, x1t = BATTERY_TUB_X
        hw, w = BATTERY_TUB_HALF_Y, BATTERY_TUB_WALL
        walls = _block(x0t, x0t + w, -hw, hw, BATTERY_TUB_FLOOR_Z[1], DECK_Z - 2.0)
        walls += _block(x1t, x1t + w, -hw, hw, BATTERY_TUB_FLOOR_Z[1], DECK_Z - 2.0)
        walls += _block(x0t + w, x1t + w, hw - w, hw, BATTERY_TUB_FLOOR_Z[1], DECK_Z - 2.0)
        walls += _block(x0t + w, x1t + w, -hw, -hw + w, BATTERY_TUB_FLOOR_Z[1], DECK_Z - 2.0)
        wx0, wx1, wz0, wz1 = TUB_SERVICE_WINDOW
        walls -= _block(wx0, wx1, hw - w - 1.0, hw + 1.0, wz0, wz1)
        for x, y in TUB_BOSS_XY:
            walls += _block(x - 3.5, x + 3.5, y - 3.5, y + 3.5, 32.0, TUB_BOSS_TOP_Z)
            walls -= _z_cylinder(2.15, 31.5, 38.5, x, y)
        shape += walls
        for y in BALLAST_SCREW_Y:
            shape -= _z_cylinder(1.7, DECK_Z - 3.0, DECK_Z + 3.0, BALLAST_SCREW_X, y)
        # D-032: main-fuse bracket, a column from the deck and a shelf under the holder.
        fx0, fx1, fy0, fy1 = FUSE_BRACKET_COLUMN
        shape += _block(fx0, fx1, fy0, fy1, DECK_Z + 1.99, FUSE_BRACKET_SHELF[4])
        shape += _block(*FUSE_BRACKET_SHELF)
        # J15B: driver posts with M2.5 insert pilots, and motor-lead tie bridges.
        for x, y in driver_mount_points():
            shape += _z_cylinder(DRIVER_POST_RADIUS, DECK_Z + 1.99, DRIVER_PCB_Z, x, y)
            shape -= _z_cylinder(DRIVER_INSERT[0], DRIVER_PCB_Z - DRIVER_INSERT[1] - 0.1, DRIVER_PCB_Z + 0.1, x, y)
            shape -= _z_cylinder(1.35, DRIVER_PCB_Z - DRIVER_INSERT[1] - 2.5, DRIVER_PCB_Z - DRIVER_INSERT[1], x, y)
        lx0, lx1, ly0, ly1, lz0, lz1 = DRIVER_TIE_LUG
        for sign in (1.0, -1.0):
            lug = _block(lx0, lx1, *sorted((sign * ly0, sign * ly1)), lz0 - 0.01, lz1)
            lug -= _block(lx0 + 1.0, lx1 - 1.0, *sorted((sign * (ly0 - 0.1), sign * (ly1 + 0.1))), lz0 - 0.02, lz0 + 1.5)
            shape += lug
    for x, y in BODY_MOUNT_POINTS:
        if x0 <= x <= x1:
            shape -= _z_cylinder(BODY_MOUNT_CLEARANCE_RADIUS, DECK_Z - 3.0, DECK_Z + 3.0, x, y)
    for x, y in BODY_LOCATING_POINTS:
        if x0 <= x <= x1:
            shape -= _z_cylinder(2.05, DECK_Z - 3.0, DECK_Z + 3.0, x, y)
    for y in BALLAST_SCREW_Y:
        if region == "FRONT":
            # 90 deg countersink for the CH-038 head, carried 1 mm above the deck top.
            seat_r = BALLAST_SCREW_SEAT_D / 2.0
            seat_z0 = DECK_Z + 2.0 - (seat_r - 1.7)
            shape -= Cone(1.7, seat_r + 1.0, seat_r - 1.7 + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((BALLAST_SCREW_X, y, seat_z0)))
    if region == "FRONT":
        shape -= _z_cylinder(NOSE_CABLE_BORE_RADIUS, DECK_Z - 3.0, DECK_Z + 3.0, *NOSE_CABLE_RISER_XY)
    return shape


def frame_rail(region: str, side: str):
    """One rail of a frame module (D-033): fused to its deck and crossmember, keyed to a J04 carrier."""
    sign = 1.0 if side == "L" else -1.0
    y0, y1 = sorted((sign * 50.0, sign * 58.0))
    x0, x1 = ((17.0, 80.0) if region == "FRONT" else (-32.0, -17.0))
    shape = _block(x0, x1, y0, y1, 35.0, 52.0)
    mount_x = 64.0 if region == "FRONT" else -22.0
    mount_y = sign * 48.0
    shape += _block(max(x0, mount_x - 6.5), min(x1, mount_x + 6.5), *sorted((sign * 52.0, sign * 64.0)), 35.0, 51.0)
    joint_y = sign * (54.0 if region == "FRONT" else 58.5)  # J04 screw axes
    if region == "REAR":
        # Widened end, X -32 to -23: a gusset into the full-width rear crossmember.
        shape += _block(-32.0, -23.0, *sorted((sign * 50.0, sign * 66.0)), 35.0, 52.0)
    shape -= _z_cylinder(5.2, 34.0, 53.0, mount_x, mount_y)
    if region == "FRONT":
        # J04: two axial heat-set inserts receive the removable side carrier.
        for z in (38.0, 48.0):
            shape -= _axial_bore_x(2.15, 17.0, 23.1, joint_y, z)
            shape -= _axial_bore_x(1.7, 23.0, 24.0, joint_y, z)
        # Asymmetric rectangular key establishes the carrier's Y/Z datum.
        key_y = sign * 51.5
        shape -= _block(17.0, 20.2, *sorted((key_y - 1.2, key_y + 1.2)), 41.3, 44.7)
    else:
        # Rear carrier screws enter from the open motor bay; inserts are
        # installed into the X=-17 end before the carrier is fitted.
        for z in (38.0, 48.0):
            shape -= _axial_bore_x(2.15, -23.1, -17.0, joint_y, z)
            shape -= _axial_bore_x(1.7, -24.0, -23.0, joint_y, z)
        key_y = sign * 51.5
        shape -= _block(-20.2, -17.0, *sorted((key_y - 1.2, key_y + 1.2)), 41.3, 44.7)
    return shape


def frame_crossmember(region: str):
    if region == "FRONT":
        shape = _block(80.0, 92.0, -62.0, 62.0, 35.0, 51.0)
        for y, z in BALL_POD_SCREWS_YZ:
            shape -= _axial_bore_x(M3_INSERT_BORE_RADIUS, 85.0, 93.0, y, z)
        shape -= _z_cylinder(NOSE_CABLE_BORE_RADIUS, 34.0, 52.0, *NOSE_CABLE_RISER_XY)
        return shape
    shape = Box(16.0, 132.0, 14.0).moved(Location((SKID_ROOT_DATUM[0], 0.0, 41.0)))
    # J09A receivers: insert bores from below, clearance above for the M3 x 30 tips.
    for x, y in rear_keel_screw_points():
        shape -= _z_cylinder(M3_INSERT_BORE_RADIUS, REAR_KEEL_TOP_Z - 1.0, REAR_KEEL_INSERT_Z[1] + 0.8, x, y)
        shape -= _z_cylinder(1.7, REAR_KEEL_TOP_Z - 1.0, REAR_KEEL_TOP_Z + 9.5, x, y)
    # Strain-relief lug on the rear face: a zip tie through the Y slot holds
    # the J10-10 cable at the foot of its riser.
    lx0, lx1, ly0, ly1, lz0, lz1 = REAR_CROSSMEMBER_TIE_LUG
    shape += _block(lx0, lx1 + 0.01, ly0, ly1, lz0, lz1) - _block(lx0 + 0.8, lx1 - 0.8, ly0 - 0.1, ly1 + 0.1, 38.5, 41.5)
    return shape


def frame_module(region: str):
    """D-033: one print per end of the frame: the deck, both rails and the crossmember.

    Replaces the J05/J06 tongue joints and the J16 deck screws (ten M3 screws and
    ten inserts). The two modules join only through the removable J04 carriers.
    The crossmember rises to the deck underside where the deck covers it
    (FRAME_MODULE_FILLS), and the J10-8 cable bore is recut through the joined
    front material.
    """
    shape = frame_deck(region) + frame_rail(region, "L") + frame_rail(region, "R") + frame_crossmember(region)
    shape = shape + _block(*FRAME_MODULE_FILLS[region])
    if region == "FRONT":
        shape = shape - _z_cylinder(NOSE_CABLE_BORE_RADIUS, 34.0, DECK_Z + 3.0, *NOSE_CABLE_RISER_XY)
    return _paint(shape, f"CHASSIS_FRAME_{region}_MODULE", FRAME_BLUE, 1.0)


def chassis_frame():
    # The deck, rails and front crossmember stop inside the shell's front
    # wall; only the ball pod's tongue passes the front face. The deck is two
    # plates either side of a relief over the coaxial motors (gearbox tops at
    # Z 54.5 reach into the deck plane), and the front plate is open over
    # the battery, which sits flush with the deck top.
    # D-033: each end is one print (deck, rails, crossmember); the J04 carriers join them.
    parts = [
        frame_module("FRONT"),
        frame_module("REAR"),
        rear_crossmember_inserts(),
        battery_tub(include_walls=False),
        ballast_bar(),
        frame_joint_hardware(),
        battery_restraint(),
        driver_mount_hardware(),
    ]

    # Axle stack (D-007). The wheel centres stay at the frozen 170 mm track.
    # Each gearmotor bolts its face to a 5 mm plate; a bolt-on printed housing
    # carries the 688 ZZ pair and reaches into the dished wheel's pocket without
    # touching it; a cap on the outer rings and three M3 x 18 into heat-set
    # inserts clamp housing and cap to the plate. Cheek plates tie the plate to
    # both rail segments through a located, four-screw J04 joint. The wheel
    # axles remain independent; no shaft spans the robot centreline.
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        plate, housing, cap, housing_hardware = axle_housing_stack(side)
        carrier = plate
        carrier_joint_parts = []
        for x_sign, joint_region in ((1.0, "FRONT"), (-1.0, "REAR")):
            cx0, cx1 = sorted((x_sign * AXLE_CHEEK_X[0], x_sign * AXLE_CHEEK_X[1]))
            # Two millimetres of cheek overlap into the 5 mm plate face; the
            # outboard edge still leaves 2 mm to the wheel's inner face.
            cy0, cy1 = sorted((sign * AXLE_CHEEK_Y[0], sign * (AXLE_CHEEK_Y[1] + 2.0)))
            cheek = _block(cx0, cx1, cy0, cy1, 35.0, 53.0)
            # Tongue fits a 0.2 mm-per-side pocket in the rail end. It keys
            # the carrier against lateral shift before the screws are clamped.
            key_y = sign * 51.5
            if joint_region == "FRONT":
                cheek += _block(17.0, 19.5, *sorted((key_y - 1.0, key_y + 1.0)), 41.5, 44.5)
                screw_x = (cx0, cx1)
            else:
                cheek += _block(-19.5, -17.0, *sorted((key_y - 1.0, key_y + 1.0)), 41.5, 44.5)
                screw_x = (cx0, cx1)
            screw_y = sign * (54.0 if joint_region == "FRONT" else 58.5)
            for z in (38.0, 48.0):
                cheek -= _axial_bore_x(1.7, cx0 - 0.1, cx1 + 0.1, screw_y, z)
                # Recess the button head from the motor-facing cheek face (D-030:
                # ISO 7380, O5.7 head in a O5.9 x 2.1 recess).
                cbx = (cx0, cx0 + J04_RECESS[1]) if x_sign > 0 else (cx1 - J04_RECESS[1], cx1)
                cheek -= _axial_bore_x(J04_RECESS[0], *cbx, screw_y, z)
                if joint_region == "FRONT":
                    insert_x = (17.0, 23.0)
                else:
                    insert_x = (-23.0, -17.0)
                seat_x = cbx[1] if x_sign > 0 else cbx[0]  # recess floor: the head's bearing face
                insert = _axial_bore_x(2.15, *insert_x, screw_y, z) - _axial_bore_x(
                    1.5, insert_x[0] - 0.1, insert_x[1] + 0.1, screw_y, z
                )
                carrier_joint_parts.append(_paint(insert, f"J04_RAIL_INSERT_M3_{side}_{joint_region}_{int(z)}", BRONZE, 1.0))
                head_r, head_h = AXLE_BUTTON_HEAD
                head = _axial_bore_x(head_r, *sorted((seat_x, seat_x - x_sign * head_h)), screw_y, z)
                shaft = _axial_bore_x(1.5, *sorted((seat_x, seat_x + x_sign * J04_SCREW_LENGTH)), screw_y, z)
                carrier_joint_parts.append(_paint(head + shaft, f"J04_CARRIER_SCREW_M3X8_{side}_{joint_region}_{int(z)}", STEEL, 1.0))
            carrier = carrier + cheek
        parts.append(_paint(carrier, f"AXLE_MOTOR_CARRIER_{side}", FRAME_BLUE, 1.0))
        parts.extend([housing, cap, housing_hardware, *carrier_joint_parts])
        parts.append(motor_face_screws(side))

    # Frozen, non-interchangeable ball-transfer nose (RP03-CAD-04): the
    # vendor flange's top face seats on the pod; three M3 from inside the
    # pocket clamp it; two M3 tie the pod to the crossmember. One load path.
    parts.append(Compound(label="BALL_POD", children=[ball_pod(), ball_pod_lid(), ball_pod_hardware()]))

    return Compound(label="CHASSIS_PRIMARY_FRAME", children=parts)


def body_primary_frame():
    parts = []
    for x in (BODY_AXIS_X - 48.0, BODY_AXIS_X + 48.0):
        for y in (-64.0, 64.0):
            parts.append(
                _box(
                    10.0,
                    10.0,
                    BODY_FRAME_UPPER_Z - 60.0,
                    (x, y, (BODY_FRAME_UPPER_Z + 60.0) / 2.0),
                    f"BODY_POST_{'F' if x > BODY_AXIS_X else 'R'}_{'L' if y > 0 else 'R'}",
                    FRAME_BLUE,
                )
            )
    for z, label in ((BODY_FRAME_LOWER_Z, "LOWER"), (BODY_FRAME_UPPER_Z, "UPPER")):
        parts.extend([
            _box(112.0, 8.0, 8.0, (BODY_AXIS_X, 64.0, z), f"BODY_{label}_RAIL_L", FRAME_BLUE),
            _box(112.0, 8.0, 8.0, (BODY_AXIS_X, -64.0, z), f"BODY_{label}_RAIL_R", FRAME_BLUE),
            _box(8.0, 120.0, 8.0, (BODY_AXIS_X + 48.0, 0.0, z), f"BODY_{label}_CROSS_FRONT", FRAME_BLUE),
            _box(8.0, 120.0, 8.0, (BODY_AXIS_X - 48.0, 0.0, z), f"BODY_{label}_CROSS_REAR", FRAME_BLUE),
        ])
    # Four bored feet seat on the chassis deck. Short dog-leg brackets connect
    # the inboard bolt pattern to the body posts without overlapping chassis
    # volume below the deck top plane.
    for mount_x, mount_y in BODY_MOUNT_POINTS:
        pad = Box(20.0, 18.0, BODY_MOUNT_PAD_THICKNESS).moved(
            Location((mount_x, mount_y, BODY_MOUNT_PAD_Z0 + BODY_MOUNT_PAD_THICKNESS / 2.0))
        )
        pad = pad - _z_cylinder(
            BODY_MOUNT_CLEARANCE_RADIUS,
            BODY_MOUNT_PAD_Z0 - 1.0,
            BODY_MOUNT_PAD_Z0 + BODY_MOUNT_PAD_THICKNESS + 1.0,
            mount_x,
            mount_y,
        )
        front = mount_x > BODY_AXIS_X
        corner_x = BODY_AXIS_X + (48.0 if front else -48.0)
        corner_y = 64.0 if mount_y > 0.0 else -64.0
        bracket = _box(
            abs(corner_x - mount_x) + 12.0,
            abs(corner_y - mount_y) + 8.0,
            12.0,
            ((corner_x + mount_x) / 2.0, (corner_y + mount_y) / 2.0, 64.0),
            f"BODY_MOUNT_DOGLEG_{'F' if front else 'R'}_{'L' if corner_y > 0 else 'R'}",
            FRAME_BLUE,
        )
        parts.extend([
            _paint(pad, f"BODY_M4_FOOT_{'F' if front else 'R'}_{'L' if mount_y > 0 else 'R'}", FRAME_BLUE, 1.0),
            bracket,
        ])
    for index, (x, y) in enumerate(BODY_LOCATING_POINTS, start=1):
        locator = Cylinder(5.0, 5.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
            Location((x, y, 58.5))
        )
        locator = locator - _z_cylinder(2.05, 55.0, 62.0, x, y)
        parts.append(_paint(locator, f"BODY_LOCATING_BOSS_{index}", SLATE_DARK, 1.0))
    parts.extend([
    ])
    # Head load path: plate spans the upper cross-members (which top out at
    # YAW_PLATE_Z[0]); central ring seats the yaw bearing.
    plate = _block(BODY_AXIS_X - 52.0, BODY_AXIS_X + 52.0, -YAW_PLATE_BAR_HALF_WIDTH, YAW_PLATE_BAR_HALF_WIDTH, *YAW_PLATE_Z) + Cylinder(
        YAW_PLATE_RADIUS, YAW_PLATE_Z[1] - YAW_PLATE_Z[0]
    ).moved(Location((BODY_AXIS_X, 0.0, sum(YAW_PLATE_Z) / 2.0)))
    plate = plate - Cylinder(9.0, 10.0).moved(Location((BODY_AXIS_X, 0.0, sum(YAW_PLATE_Z) / 2.0)))
    parts.append(_paint(plate, "HEAD_YAW_ADAPTER_PLATE", FRAME_BLUE))
    return Compound(label="BODY_PRIMARY_FRAME", children=parts)


def body_chassis_mount_hardware():
    parts = []
    for index, (x, y) in enumerate(BODY_MOUNT_POINTS, start=1):
        parts.extend([
            _cylinder(1.9, 12.0, (x, y, 56.0), f"BODY_CHASSIS_M4_SHANK_{index}", STEEL),
            _cylinder(4.0, 2.4, (x, y, 61.2), f"BODY_CHASSIS_M4_HEAD_{index}", STEEL),
            _cylinder(4.1, 3.2, (x, y, 50.4), f"BODY_CHASSIS_M4_NUT_{index}", BRONZE),
        ])
    for index, (x, y) in enumerate(BODY_LOCATING_POINTS, start=1):
        parts.append(_cylinder(2.0, 8.0, (x, y, 56.0), f"BODY_CHASSIS_LOCATING_PIN_{index}", STEEL))
    return Compound(label="BODY_CHASSIS_MOUNT_HARDWARE", children=parts)


def _check_wheel_interface():
    """The standalone wheel must keep the D-007 hub interface; fail loudly if either drifts."""
    W, half = WHEEL_MODEL, TRACK / 2.0
    pairs = {
        "od": (W.WHEEL_OD, WHEEL_OD),
        "width": (W.WHEEL_WIDTH, WHEEL_WIDTH),
        "pocket_radius": (W.BOSS_POCKET_RADIUS, WHEEL_POCKET_RADIUS),
        "pocket_floor_y": (half + W.BOSS_POCKET_FLOOR_Y, WHEEL_POCKET_FLOOR_Y),
        "hub_bore_radius": (W.HUB_BORE_RADIUS, WHEEL_HUB_BORE_RADIUS),
        "spigot_y": (tuple(half + y for y in W.STUB_SPIGOT_Y), STUB_SPIGOT[1:]),
        "flange": ((W.STUB_FLANGE["radius"], *(half + y for y in W.STUB_FLANGE["y"])), STUB_FLANGE),
        "screw_pcd_r": (W.WHEEL_SCREW["pcd_r"], WHEEL_SCREW_PCD_R),
        "screw_length": (W.WHEEL_SCREW["length"], WHEEL_SCREW_LENGTH),
        "screw_head": ((W.WHEEL_SCREW_HEAD["radius"], W.WHEEL_SCREW_HEAD["height"]), AXLE_BUTTON_HEAD),
        # wheel_model measures from +Z about Y; the chassis from +X toward +Z
        "screw_angles": (sorted(round(a % 360.0, 6) for a in W.WHEEL_SCREW["angles"]), sorted(round((90.0 - a) % 360.0, 6) for a in WHEEL_SCREW_ANGLES)),
        "cap_tap": ((W.STUB_CAP_TAP["thread"], W.STUB_CAP_TAP["drill"]), STUB_CAP_TAP),
    }
    bad = {k: v for k, v in pairs.items() if v[0] != v[1]}
    if bad:
        raise ValueError(f"wheel/wheel_model.py no longer matches the D-007 hub interface: {bad}")


def wheel_assembly(side: str):
    """Chassis v1 drive wheel (D-008, D-009) on a turned steel stub (D-007).

    Rim, handed TPU tyre, clamp ring, hub cap and wheel hardware come from
    wheel/wheel_model.py; the right wheel is the left mirrored, with the
    right-hand tyre. The pocket clears the bearing housing; the stub's Ø10
    spigot centres the web, three M3 x 6 through the web into its flange carry
    the torque, and an M3 set screw on the motor's D-flat drives the stub. One
    central M3 x 10 holds the hub cap in a tapped hole in the spigot end (D-033).
    """
    _check_wheel_interface()
    sign = 1.0 if side == "L" else -1.0
    ys = lambda y0, y1: (sign * y0, sign * y1)
    screw_xz = [_polar_xz(WHEEL_SCREW_PCD_R, a) for a in WHEEL_SCREW_ANGLES]
    wheel_parts = WHEEL_MODEL.mounted_leaves(side, TRACK, AXLE_Z)  # rim first

    stub = _axial_bore_y(STUB_SHAFT_RADIUS, *ys(STUB_SHAFT_Y[0], STUB_SHOULDER[1] + 0.01), 0.0, AXLE_Z)
    for radius, y0, y1 in (STUB_SHOULDER, STUB_FLANGE, STUB_SPIGOT):
        # the shoulder starts exactly at the bearing face; the larger steps overlap for fusion
        stub = stub + _axial_bore_y(radius, *ys(y0 if radius == STUB_SHOULDER[0] else y0 - 0.01, y1), 0.0, AXLE_Z)
    flat_z = AXLE_Z + MOTOR_SHAFT_FLAT_ACROSS - MOTOR_SHAFT_RADIUS
    # Cut one tool at a time; the tapped hole starts on the flat, not on the
    # bore axis, because a coincident start left the bore core as a stray solid.
    stub = stub - _axial_bore_y(STUB_BORE[0], *ys(STUB_SHAFT_Y[0] - 1.0, STUB_BORE[1]), 0.0, AXLE_Z)
    stub = stub - _z_cylinder(1.5, flat_z - 0.3, AXLE_Z + STUB_SHAFT_RADIUS + 1.0, 0.0, sign * SET_SCREW_Y)
    for x_off, z_off in screw_xz:
        stub = stub - _axial_bore_y(1.5, *ys(STUB_FLANGE[1] - 0.5, STUB_FLANGE[2] + 0.5), x_off, AXLE_Z + z_off)
    # D-033: M3 tapped hole in the spigot end for the hub-cap screw. The thread is cut
    # at the major diameter, as the flange holes are; the tap-drill point runs on below.
    tip = STUB_SPIGOT[2]
    stub = stub - _axial_bore_y(1.5, *ys(tip - STUB_CAP_TAP[0], tip + 0.5), 0.0, AXLE_Z)
    stub = stub - _axial_bore_y(1.25, *ys(tip - STUB_CAP_TAP[1], tip - STUB_CAP_TAP[0] + 0.01), 0.0, AXLE_Z)
    set_screw = _z_cylinder(1.5, flat_z, flat_z + SET_SCREW_LENGTH, 0.0, sign * SET_SCREW_Y)

    return Compound(label=f"WHEEL_{side}", children=[
        wheel_parts[0],
        _paint(stub, f"WHEEL_{side}_STUB_SHAFT_8MM", STEEL, 1.0),
        _paint(set_screw, f"WHEEL_{side}_SET_SCREW_M3X2_5", STEEL, 1.0),
        *wheel_parts[1:],
    ])


def _motor_y_span(sign, y_outboard, length):
    """Signed |Y| span running `length` inboard from `y_outboard`."""
    return sign * (y_outboard - length), sign * y_outboard


def motor_envelope(side: str):
    """ThinkRobotics MOT3001-6V230RPM (JGA25-370), from its drawing, output face on the flange at |Y| 69.

    Stationary body (gearbox, can, bushing boss, tapped face holes), encoder
    board with its rearward connector, and the output shaft, which turns with
    the stub. See the MOTOR_* notes for what is drawn and what is assumed.
    """
    sign = 1.0 if side == "L" else -1.0
    face = MOTOR_FACE_Y
    can_front = face - MOTOR_GEARBOX_LENGTH
    can_rear = can_front - MOTOR_CAN_LENGTH
    pcb_front = can_rear - MOTOR_ENCODER_LENGTH + MOTOR_ENCODER_PCB_THICKNESS
    pcb_rear = can_rear - MOTOR_ENCODER_LENGTH

    body = _axial_bore_y(MOTOR_GEARBOX_RADIUS, *_motor_y_span(sign, face, MOTOR_GEARBOX_LENGTH), 0.0, AXLE_Z)
    body = body + _axial_bore_y(MOTOR_CAN_RADIUS, *_motor_y_span(sign, can_front, MOTOR_CAN_LENGTH), 0.0, AXLE_Z)
    body = body + (
        _axial_bore_y(MOTOR_PILOT_RADIUS, sign * face, sign * (face + MOTOR_PILOT_LENGTH), 0.0, AXLE_Z)
        - _axial_bore_y(MOTOR_SHAFT_RADIUS + 0.05, sign * (face - 1.0), sign * (face + MOTOR_PILOT_LENGTH + 1.0), 0.0, AXLE_Z)
    )
    for x_off, z_off in MOTOR_SCREW_XZ:
        body = body - _axial_bore_y(
            MOTOR_SCREW_TAP_RADIUS, sign * (face - MOTOR_SCREW_HOLE_DEPTH), sign * (face + 0.01), x_off, AXLE_Z + z_off
        )

    hub = _axial_bore_y(MOTOR_ENCODER_HUB_RADIUS, sign * pcb_front, sign * can_rear, 0.0, AXLE_Z)
    pcb = _axial_bore_y(MOTOR_CAN_RADIUS, sign * pcb_rear, sign * pcb_front, 0.0, AXLE_Z)
    connector = _block(
        *MOTOR_CONNECTOR_X,
        *sorted((sign * pcb_rear, sign * (pcb_rear + 6.0))),
        AXLE_Z - MOTOR_CONNECTOR_HALF_Z,
        AXLE_Z + MOTOR_CONNECTOR_HALF_Z,
    )

    shaft_end = face + MOTOR_SHAFT_LENGTH
    shaft = _axial_bore_y(MOTOR_SHAFT_RADIUS, sign * face, sign * shaft_end, 0.0, AXLE_Z)
    flat_z = AXLE_Z + MOTOR_SHAFT_FLAT_ACROSS - MOTOR_SHAFT_RADIUS  # D-flat on +Z
    shaft = shaft - _block(
        -3.0, 3.0, *sorted((sign * (shaft_end - MOTOR_SHAFT_FLAT_LENGTH), sign * (shaft_end + 1.0))), flat_z, AXLE_Z + 3.0
    )

    gearbox = _paint(body, f"MOTOR_{side}_MOT3001_6V230_GEARBOX", BRONZE, 1.0)
    encoder = _paint(hub + pcb, f"MOTOR_{side}_ENCODER_CAP", SLATE_DARK, 1.0)
    plug = _paint(connector, f"MOTOR_{side}_ENCODER_6PIN_CONNECTOR", "#E9E4D4", 1.0)
    output = _paint(shaft, f"MOTOR_{side}_OUTPUT_SHAFT", STEEL, 1.0)
    # The supplied 6-pin cable leaves the plug rearward and turns up into
    # the reserve behind the axle, in the deck's motor relief.
    pigtail = _paint(
        _block(-21.0, -1.0, *sorted((sign * 6.0, sign * 18.0)), 56.5, 62.5),
        f"MOTOR_{side}_PIGTAIL_RESERVE",
        "#EF8A3D",
        0.34,
    )
    return Compound(label=f"MOTOR_{side}", children=[gearbox, encoder, plug, output, pigtail])


def _polar_xz(radius, angle_deg):
    """(X, Z - AXLE_Z) of a point on the axle face at `radius`, `angle_deg` from +X."""
    return (radius * math.cos(math.radians(angle_deg)), radius * math.sin(math.radians(angle_deg)))


def _housing_screw_xz():
    return [_polar_xz(AXLE_HOUSING_SCREW_R, a) for a in AXLE_HOUSING_SCREW_ANGLES]


def axle_housing_stack(side: str):
    """Motor plate, bearing housing, retaining cap, cap screws and inserts (D-007)."""
    sign = 1.0 if side == "L" else -1.0
    fy0, fy1 = AXLE_FLANGE_Y
    hy0, hy1 = AXLE_HOUSING_Y
    cy0, cy1 = AXLE_CAP_Y
    ys = lambda y0, y1: (sign * y0, sign * y1)

    plate = _block(-AXLE_FLANGE_HALF_X, AXLE_FLANGE_HALF_X, *sorted(ys(fy0, AXLE_PLATE_SQUARE_END_Y)), *AXLE_FLANGE_Z)
    plate = plate + _axial_bore_y(AXLE_PLATE_HUB_RADIUS, *ys(AXLE_PLATE_SQUARE_END_Y - 0.01, fy1), 0.0, AXLE_Z)
    cuts = [
        _axial_bore_y(AXLE_PILOT_HOLE_RADIUS, *ys(fy0 - 1.0, fy1 + 1.0), 0.0, AXLE_Z),
        _axial_bore_y(AXLE_PLATE_RECESS[0], *ys(fy1 - AXLE_PLATE_RECESS[1], fy1 + 1.0), 0.0, AXLE_Z),
    ]
    for x_off, z_off in MOTOR_SCREW_XZ:
        cuts.append(_axial_bore_y(MOTOR_SCREW_CLEAR_RADIUS, *ys(fy0 - 1.0, fy1 + 1.0), x_off, AXLE_Z + z_off))
        cuts.append(_axial_bore_y(MOTOR_SCREW_CBORE[0], *ys(fy1 - MOTOR_SCREW_CBORE[1], fy1 + 1.0), x_off, AXLE_Z + z_off))
    for x_off, z_off in _housing_screw_xz():
        cuts.append(_axial_bore_y(AXLE_INSERT_RADIUS, *ys(fy1 - AXLE_INSERT_DEPTH, fy1 + 1.0), x_off, AXLE_Z + z_off))
        cuts.append(_axial_bore_y(1.5, *ys(AXLE_CAP_Y[1] - AXLE_CAP_SCREW_LENGTH - 0.2, fy1), x_off, AXLE_Z + z_off))  # blind tip hole
    plate = _paint(plate - cuts, f"AXLE_MOTOR_PLATE_{side}", FRAME_BLUE, 1.0)

    housing = _axial_bore_y(AXLE_HOUSING_RADIUS, *ys(hy0, hy1), 0.0, AXLE_Z)
    cuts = [
        _axial_bore_y(AXLE_HOUSING_INNER_RADIUS, *ys(hy0 - 1.0, BEARING_SEAT_Y[0]), 0.0, AXLE_Z),
        _axial_bore_y(BEARING_OD_RADIUS, *ys(BEARING_SEAT_Y[0], hy1 + 1.0), 0.0, AXLE_Z),
        Cylinder(AXLE_WINDOW_RADIUS, AXLE_HOUSING_RADIUS + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0.0, sign * SET_SCREW_Y, AXLE_Z))
        ),
        _block(-AXLE_WINDOW_RADIUS, AXLE_WINDOW_RADIUS, *sorted(ys(hy0 - 1.0, SET_SCREW_Y)), AXLE_Z, AXLE_Z + AXLE_HOUSING_RADIUS + 1.0),
    ]
    for x_off, z_off in MOTOR_SCREW_XZ:
        # key slot: the O2.6 key path passes beside the bearing OD; bridge it into the bore
        x_in = math.copysign(BEARING_OD_RADIUS - 0.5, x_off)
        cuts.append(_block(*sorted((x_in, x_off)), *sorted(ys(hy0 - 1.0, hy1 + 1.0)), AXLE_Z - AXLE_KEY_HOLE_RADIUS, AXLE_Z + AXLE_KEY_HOLE_RADIUS))
    cap = _axial_bore_y(AXLE_HOUSING_RADIUS, *ys(cy0, cy1), 0.0, AXLE_Z) - _axial_bore_y(
        AXLE_HOUSING_INNER_RADIUS, *ys(cy0 - 1.0, cy1 + 1.0), 0.0, AXLE_Z
    )
    cap_cuts = []
    for x_off, z_off in _housing_screw_xz():
        for group in (cuts, cap_cuts):
            group.append(_axial_bore_y(1.7, *ys(hy0 - 1.0, cy1 + 1.0), x_off, AXLE_Z + z_off))
    for x_off, z_off in MOTOR_SCREW_XZ:
        for group in (cuts, cap_cuts):
            group.append(_axial_bore_y(AXLE_KEY_HOLE_RADIUS, *ys(hy0 - 1.0, cy1 + 1.0), x_off, AXLE_Z + z_off))
    housing = _paint(housing - cuts, f"AXLE_BEARING_HOUSING_{side}", FRAME_BLUE, 1.0)
    cap = _paint(cap - cap_cuts, f"AXLE_BEARING_CAP_{side}", STEEL, 1.0)

    hardware = []
    head_r, head_h = AXLE_BUTTON_HEAD
    for index, (x_off, z_off) in enumerate(_housing_screw_xz(), start=1):
        screw = _axial_bore_y(head_r, *ys(cy1, cy1 + head_h), x_off, AXLE_Z + z_off) + _axial_bore_y(
            1.5, *ys(cy1 - AXLE_CAP_SCREW_LENGTH, cy1), x_off, AXLE_Z + z_off
        )
        hardware.append(_paint(screw, f"AXLE_CAP_SCREW_M3X18_{side}_{index}", STEEL, 1.0))
        insert = _axial_bore_y(AXLE_INSERT_RADIUS, *ys(fy1 - AXLE_INSERT_DEPTH, fy1), x_off, AXLE_Z + z_off) - _axial_bore_y(
            1.5, *ys(fy1 - AXLE_INSERT_DEPTH - 1.0, fy1 + 1.0), x_off, AXLE_Z + z_off
        )
        hardware.append(_paint(insert, f"AXLE_PLATE_INSERT_M3_{side}_{index}", BRONZE, 1.0))
    return [plate, housing, cap, Compound(label=f"AXLE_HOUSING_HARDWARE_{side}", children=hardware)]


def motor_face_screws(side: str):
    """Two ISO 7380 M3 x 6 button-head screws, plate into the gearbox face, heads in counterbores (D-030)."""
    sign = 1.0 if side == "L" else -1.0
    head_top = AXLE_FLANGE_Y[1] - (MOTOR_SCREW_CBORE[1] - MOTOR_SCREW_HEAD_HEIGHT)
    head_bottom = head_top - MOTOR_SCREW_HEAD_HEIGHT
    # Domed head: a spherical cap dk 5.7 x k 1.65, not a cylinder. Trimmed at the
    # origin, turned +Z to +/-Y, then placed. Its rim is what nears the set screw.
    r, k = MOTOR_SCREW_HEAD_RADIUS, MOTOR_SCREW_HEAD_HEIGHT
    rs = (r * r + k * k) / (2.0 * k)
    cap = Sphere(rs).moved(Location((0.0, 0.0, k - rs))) & Box(2.0 * r + 1.0, 2.0 * r + 1.0, k, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cap = cap.rotate(Axis.X, -90.0 * sign)
    children = []
    for index, (x_off, z_off) in enumerate(MOTOR_SCREW_XZ, start=1):
        screw = cap.moved(Location((x_off, sign * head_bottom, AXLE_Z + z_off))) + _axial_bore_y(
            1.5, sign * (head_bottom - MOTOR_SCREW_LENGTH), sign * head_bottom, x_off, AXLE_Z + z_off
        )
        children.append(_paint(screw, f"AXLE_MOTOR_SCREW_M3X6_{side}_{index}", STEEL, 1.0))
    return Compound(label=f"AXLE_MOTOR_SCREWS_{side}", children=children)


def bearing_pair(side: str):
    """Two 688 ZZ (8 x 16 x 5) as rings with shield recesses; no supplier STEP."""
    sign = 1.0 if side == "L" else -1.0
    children = []
    for index, y_abs in enumerate(BEARING_Y, start=1):
        y0, y1 = y_abs - BEARING_WIDTH / 2.0, y_abs + BEARING_WIDTH / 2.0
        ring = _axial_bore_y(BEARING_OD_RADIUS, sign * y0, sign * y1, 0.0, AXLE_Z) - _axial_bore_y(
            BEARING_BORE_RADIUS, sign * (y0 - 1.0), sign * (y1 + 1.0), 0.0, AXLE_Z
        )
        for face in (y0, y1):
            shield = _axial_bore_y(6.1, sign * (face - 0.2), sign * (face + 0.2), 0.0, AXLE_Z) - _axial_bore_y(
                4.9, sign * (face - 1.0), sign * (face + 1.0), 0.0, AXLE_Z
            )
            ring = ring - shield
        children.append(_paint(ring, f"BEARING_{BEARING_MODEL}_{side}_{index}", STEEL, 1.0))
    return Compound(label=f"BEARING_PAIR_{side}", children=children)


def ball_transfer():
    """Pololu 1" ball caster (2691) from its STEP, ball contact on BALL_CONTACT."""
    part = import_step(str(PURCHASED / BALL_CASTER_STEP))
    part = part.moved(Location((BALL_CONTACT[0], BALL_CONTACT[1], BALL_CONTACT[2])))
    # STEP export order: ball, base (flange), shell (housing), three rollers. Flatten after the
    # move so every solid carries its world placement.
    ball, base, shell, *rollers = list(part.solids())
    # D-011: O6.3 counterbores from the ball side leave the drawing's 2.7 mm web (not in the STEP).
    for x, y in ball_screw_points():
        base = base - _z_cylinder(BALL_FLANGE_CBORE_RADIUS, BALL_CONTACT[2] + 15.0, BALL_NATIVE_HEIGHT - BALL_FLANGE_WEB, x, y)
    children = [
        _paint(ball, "BALL_TRANSFER_POM_BALL", IVORY, 1.0),
        _paint(base, "BALL_TRANSFER_PURCHASED_3HOLE_FLANGE", "#1B1E21", 1.0),
        _paint(shell, "BALL_TRANSFER_PURCHASED_HOUSING", "#1B1E21", 1.0),
    ]
    children += [_paint(r, f"BALL_TRANSFER_ROLLER_{k}", "#E9ECEE", 1.0) for k, r in enumerate(rollers, start=1)]
    return Compound(label="BALL_TRANSFER_PURCHASED_FIXED_MODULE", children=children)


def raspberry_pi5():
    pi = import_step(str(PURCHASED / "raspberry_pi_5.step")).rotate(Axis.X, 90.0)
    pi = _center_at(pi, PI_CENTER)
    pi = Compound(label="C0_RASPBERRY_PI5_EXACT_STEP", children=list(pi.solids()))  # flat: see _purchased_step
    return pi


def _estop_octagon(x, across_flats):
    """Regular octagon in the YZ plane at X, flats horizontal, on the E-stop axis."""
    r = across_flats / 2.0 / math.cos(math.pi / 8.0)
    points = [
        (r * math.cos(math.pi / 8.0 + k * math.pi / 4.0), ESTOP_CENTER_Z + r * math.sin(math.pi / 8.0 + k * math.pi / 4.0))
        for k in range(8)
    ]
    return (Plane.YZ * Polygon(*points, align=None)).moved(Location((x, 0.0, 0.0)))


def _estop_well_outer():
    """Outer skin of the rear-panel E-stop well: tapered socket plus the floor plate."""
    wall = 2.0 * ESTOP_WELL_WALL
    socket = loft([
        _estop_octagon(ESTOP_REAR_OUTER_X, ESTOP_WELL_MOUTH + wall),
        _estop_octagon(ESTOP_MOUNT_X, ESTOP_WELL_THROAT + wall),
    ], ruled=True)
    floor = extrude(_estop_octagon(ESTOP_MOUNT_X, ESTOP_WELL_THROAT + wall), amount=ESTOP_WELL_FLOOR)
    return socket + floor


def rear_panel_estop_well():
    """Tapered octagonal well printed with the rear panel, and its amber bezel land."""
    cavity = loft([
        _estop_octagon(ESTOP_REAR_OUTER_X - 0.01, ESTOP_WELL_MOUTH),
        _estop_octagon(ESTOP_MOUNT_X, ESTOP_WELL_THROAT),
    ], ruled=True)
    cutout = _axial_bore_x(ESTOP_CUTOUT_DIAMETER / 2.0, ESTOP_MOUNT_X - 1.0, ESTOP_FLOOR_BACK_X + 1.0, 0.0, ESTOP_CENTER_Z)
    well = _estop_well_outer() - cavity - cutout
    bezel = extrude(_estop_octagon(ESTOP_REAR_OUTER_X - ESTOP_BEZEL_PROUD, ESTOP_BEZEL_ACROSS_FLATS), amount=ESTOP_BEZEL_PROUD)
    bezel = bezel - extrude(_estop_octagon(ESTOP_REAR_OUTER_X - ESTOP_BEZEL_PROUD - 1.0, ESTOP_WELL_MOUTH + 2.0 * ESTOP_WELL_WALL), amount=ESTOP_BEZEL_PROUD + 2.0)
    return [
        _paint(well, "REAR_PANEL_ESTOP_WELL", SLATE_DARK, 1.0),
        _paint(bezel, "REAR_PANEL_ESTOP_AMBER_BEZEL", ESTOP_AMBER, 1.0),
    ]


def estop_switch():
    """IDEC XA1E-BV3U02KT-R: Ø29 domed mushroom, operator collar and unibody contact block."""
    top_x = ESTOP_MOUNT_X - ESTOP_MUSHROOM_TOP_ABOVE_MOUNT
    skirt_x1 = top_x + ESTOP_MUSHROOM_DOME + ESTOP_MUSHROOM_SKIRT
    r = ESTOP_MUSHROOM_DIAMETER / 2.0
    dome_r = (r * r + ESTOP_MUSHROOM_DOME ** 2) / (2.0 * ESTOP_MUSHROOM_DOME)
    # Trim the cap at the origin, then turn +Z to -X: trimming the placed sphere
    # returns the whole sphere in this OCC build.
    dome = Sphere(dome_r) & Box(2.0 * r, 2.0 * r, ESTOP_MUSHROOM_DOME + 1.0, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(Location((0.0, 0.0, dome_r + 1.0)))
    dome = dome.rotate(Axis.Y, -90.0).moved(Location((top_x + dome_r, 0.0, ESTOP_CENTER_Z)))
    skirt = _axial_bore_x(r, top_x + ESTOP_MUSHROOM_DOME, skirt_x1, 0.0, ESTOP_CENTER_Z)
    # A shallow grip groove round the skirt reads as the real cap's rim.
    skirt = skirt - (_axial_bore_x(r + 1.0, skirt_x1 - 2.2, skirt_x1 - 1.4, 0.0, ESTOP_CENTER_Z) - _axial_bore_x(r - 0.5, skirt_x1 - 3.0, skirt_x1, 0.0, ESTOP_CENTER_Z))
    collar_d, collar_h = ESTOP_OPERATOR_BEZEL
    collar = _axial_bore_x(collar_d / 2.0, ESTOP_MOUNT_X - collar_h, ESTOP_MOUNT_X, 0.0, ESTOP_CENTER_Z)
    stem = _axial_bore_x(ESTOP_STEM_DIAMETER / 2.0, skirt_x1, ESTOP_MOUNT_X - collar_h, 0.0, ESTOP_CENTER_Z)
    barrel = _axial_bore_x(ESTOP_CUTOUT_DIAMETER / 2.0 - 0.3, ESTOP_MOUNT_X, ESTOP_FLOOR_BACK_X, 0.0, ESTOP_CENTER_Z)
    body = _axial_bore_x(ESTOP_BODY_DIAMETER / 2.0, ESTOP_FLOOR_BACK_X, ESTOP_FLOOR_BACK_X + ESTOP_DEPTH_BEHIND_PANEL - 3.0, 0.0, ESTOP_CENTER_Z)
    tabs = [
        _block(ESTOP_FLOOR_BACK_X + ESTOP_DEPTH_BEHIND_PANEL - 3.0, ESTOP_FLOOR_BACK_X + ESTOP_DEPTH_BEHIND_PANEL, y - 3.2, y + 3.2, ESTOP_CENTER_Z + dz - 0.4, ESTOP_CENTER_Z + dz + 0.4)
        for y, dz in ((-5.5, -3.0), (5.5, -3.0), (0.0, 5.5))
    ]
    return [
        _paint(dome + skirt, "ESTOP_XA1E_MUSHROOM_D29", ESTOP_RED, 1.0),
        _paint(stem + collar + barrel, "ESTOP_XA1E_OPERATOR_COLLAR", "#3A4044", 1.0),
        _paint(body, "ESTOP_XA1E_UNIBODY_CONTACT_BLOCK", "#2E3336", 1.0),
        *[_paint(tab, f"ESTOP_XA1E_TAB_{i}", STEEL, 1.0) for i, tab in enumerate(tabs, start=1)],
    ]


def power_distribution_boards():
    """RP-02 custom power/safety board envelopes, main-fuse holder and E-stop (proposal).

    Each board is a 1.6 mm PCB plate plus a translucent parts envelope up to the
    stated total height. The E-stop keep-out is a reserved volume, not a solid
    that belongs to a part. The E-stop's well and bezel and the charge-inlet
    cut-out belong to the rear panel (body_panels); the inlet receptacle and its
    plug corridor are in connectors_and_exits().
    """
    def board(name, box, color, pcb_at_top=False):
        x0, x1, y0, y1, z0, z1 = box
        parts = []
        if name == "PCB02_CHARGE_AND_SYSTEM_POWER":
            # Vertical board: the PCB plate is the -X face, parts stand out toward +X.
            parts.append(_paint(_block(x0, x0 + PCB_THICKNESS, y0, y1, z0, z1), f"{name}_PCB", PCB_GREEN, 1.0))
            parts.append(_paint(_block(x0 + PCB_THICKNESS, x1, y0, y1, z0, z1), f"{name}_PARTS_ENVELOPE", color, 0.55))
        else:
            parts.append(_paint(_block(x0, x1, y0, y1, z0, z0 + PCB_THICKNESS), f"{name}_PCB", PCB_GREEN, 1.0))
            parts.append(_paint(_block(x0, x1, y0, y1, z0 + PCB_THICKNESS, z1), f"{name}_PARTS_ENVELOPE", color, 0.55))
        return Compound(label=name, children=parts)

    estop = Compound(label="ESTOP_XA1E_BV3U02KT_R", children=[
        *estop_switch(),
        _paint(_block(*ESTOP_KEEP_OUT), "ESTOP_XA1E_BEHIND_PANEL_KEEP_OUT", ESTOP_RED, 0.18),
    ])
    parts = [
        board("PCB02_CHARGE_AND_SYSTEM_POWER", PCB02_BOX, "#D38132"),
        board("PCB03_MOTOR_GATE_AND_HEAD_RAIL", PCB03_BOX, "#D38132"),
        board("PCB04_BRANCH_CONVERTERS", PCB04_BOX, "#D38132"),
        _paint(_block(*PACK_FUSE_HOLDER_BOX), "PACK_ATOF_FUSE_HOLDER_ENVELOPE", "#C55842", 0.74),
        _paint(_block(*PACK_DISCONNECT_PAIR_BOX), "PACK_DISCONNECT_MICROFIT_PLUS_1X2_MATED_ENVELOPE", "#E7A95B", 0.85),
        estop,
    ]
    return Compound(label="POWER_DISTRIBUTION_BOARDS", children=parts)


def electronics():
    # The battery lives in the chassis tub (RP03-CAD-06); it stays in this
    # group so the viewer's electronics toggle still shows it.
    battery = battery_pack()
    pi_tray = _box(108.0, 76.0, 3.0, (PI_CENTER[0], 0.0, 86.0), "COMPUTE_TRAY", "#7A858B", 1.0)
    # GrabCAD heatsink+fan STEP: +90 deg about X (the Pi's own turn) puts the two spring posts,
    # 58 x 37.6 mm apart, over the Pi's two cooler holes with the tips down; the -90 deg first used
    # mirrored that diagonal. The heatsink plate then sits on the tallest package under it (Z 97.7).
    cooler = _purchased_step("Heatsink+fan RPi-5.STEP", "PI5_ACTIVE_COOLER_STEP", [(Axis.X, 90.0)])
    posts = sorted((sl for sl in cooler.solids() if 100.0 < sl.volume < 140.0), key=lambda sl: sl.bounding_box().center().X)
    post_a = posts[0].bounding_box().center()
    plate_z0 = max(cooler.solids(), key=lambda sl: sl.volume).bounding_box().min.Z
    cooler = cooler.moved(Location((PI_COOLER_HOLE_A[0] - post_a.X, PI_COOLER_HOLE_A[1] - post_a.Y, PI_SOC_TOP_Z - plate_z0)))
    cooler = Compound(label="PI5_ACTIVE_COOLER_STEP", children=list(cooler.solids()))
    c3 = c3_carrier()
    # Adafruit #3297 board proxies; dimensions are nominal envelopes pending measurement.
    drivers = []
    for side, y in (("LEFT", DRIVER_Y), ("RIGHT", -DRIVER_Y)):
        # Board file-derived STEP (purchased/README.md); long side along Y, hole edge rearward (D-031).
        drv = _place(
            _purchased_step("adafruit_3297_drv8833.step", f"ADAFRUIT_3297_DRV8833_{side}", [(Axis.Z, DRIVER_TURN)], folder=V1_PURCHASED),
            DRIVER_CENTER_X, y, DRIVER_PCB_Z, ref={"Z": "min"},
        )
        leaves_ = list(drv.solids())
        assert len(leaves_) == len(ADAFRUIT_3297_LEAVES), len(leaves_)
        for leaf, name in zip(leaves_, ADAFRUIT_3297_LEAVES):
            _paint(leaf, f"DRV8833_{side}_{name}", "#16204A" if name == "PCB" else "#2D6338" if name.startswith("J1") else "#1E2426", 1.0)
        drivers.append(Compound(label=f"ADAFRUIT_3297_DRV8833_{side}", children=leaves_))
    driver_l, driver_r = drivers
    # The old power-distribution and safety envelopes are replaced by the RP-02 boards (power_distribution_boards).
    imu = imu_board()
    return Compound(label="BODY_ELECTRONICS", children=[
        battery,
        pi_tray,
        raspberry_pi5(),
        cooler,
        c3,
        driver_l,
        driver_r,
        power_distribution_boards(),
        imu,
    ])


def c3_carrier():
    """PCB-10 C3 carrier on the -Y side wall with the DevKitC soldered on (+Y face)."""
    x0, x1, y0, y1, z0, z1 = C3_CARRIER_BOARD
    board = _paint(_block(*C3_CARRIER_BOARD), "C3_CARRIER_PCB10_BOARD", PCB_GREEN, 1.0)
    # DevKitC: -90 deg about Z puts the USB end at the rear (-X); -90 deg about X
    # then turns its component side to +Y, off the carrier.
    devkit = _purchased_step("ESP32-S3-WROOM-1_devkit_2xUSBC_c.step", "C3_ESP32_S3_DEVKITC_STEP", [(Axis.Z, -90.0), (Axis.X, -90.0)])
    devkit = _place(devkit, (x0 + x1) / 2.0, y1 + C3_DEVKIT_STANDOFF, C3_DEVKIT_Z[0], ref={"X": "center", "Y": "min", "Z": "min"})
    # The DevKitC's two 22-pin male headers, soldered through the carrier.
    rows = [
        _paint(_block((x0 + x1) / 2.0 - 27.94, (x0 + x1) / 2.0 + 27.94, y1, y1 + C3_DEVKIT_STANDOFF, z - 1.27, z + 1.27), f"C3_DEVKIT_HEADER_ROW_{k}", "#2E3336", 1.0)
        for k, z in ((1, C3_DEVKIT_Z[0] + 1.6), (2, C3_DEVKIT_Z[1] - 1.6))
    ]
    uprights = [
        _paint(_block(ux0, ux1, -66.0, y0, BODY_FRAME_LOWER_Z + 4.0, BODY_FRAME_UPPER_Z - 4.0), f"BODY_FRAME_C3_CARRIER_UPRIGHT_{k}", FRAME_BLUE, 1.0)
        for k, (ux0, ux1) in enumerate(C3_CARRIER_UPRIGHTS, start=1)
    ]
    screws = []
    for k, (sx, sz) in enumerate(C3_CARRIER_SCREWS, start=1):
        head = _cylinder(2.25, 1.8, (sx, y1 + 0.9, sz), f"C3_CARRIER_M25_SCREW_HEAD_{k}", STEEL, 1.0, "y")
        shank = _cylinder(1.25, 6.0, (sx, y1 - 3.0, sz), f"C3_CARRIER_M25_SCREW_SHANK_{k}", STEEL, 1.0, "y")
        screws += [head, shank]
    # Top-entry GH headers: -90 deg about X turns the STEP's +Z (mating) to +Y.
    headers = []
    for zc, row in C3_GH_ROWS.items():
        for cid, n, hx0 in row:
            hdr = _place(_gh_header(n, f"C3_{_cid(cid)}_JST_GH_BM{n:02d}B_HEADER", [(Axis.X, -90.0)], top_entry=True), hx0, y1, zc, ref={"X": "min", "Y": "min", "Z": "center"})
            top = hdr.bounding_box().max.Y
            hc = (hdr.bounding_box().min.X + hdr.bounding_box().max.X) / 2.0
            plug = _box(gh_plug_width(n), GH_PLUG_PROUD, GH_PLUG_THICKNESS, (hc, top + GH_PLUG_PROUD / 2.0, zc), f"C3_{_cid(cid)}_GHR{n:02d}_MATED_PLUG", "#F4F1E6", 1.0)
            headers += [hdr, plug]
    # J10-1: Micro-Fit 3.0 2x1 right-angle on the front edge, mating +X.
    w = connector_width("MF3", 2)
    pz = (C3_POWER_PLUG_RESERVE[4] + C3_POWER_PLUG_RESERVE[5]) / 2.0
    headers.append(_paint(_block(x1 - 7.0, x1, y1, y1 + 10.0, pz - w / 2.0, pz + w / 2.0), "C3_J10_1_MICROFIT3_2P_RA_HEADER", "#2E3336", 1.0))
    headers.append(_paint(_block(x1, x1 + 12.0, y1, y1 + 10.0, pz - w / 2.0, pz + w / 2.0), "C3_J10_1_MICROFIT3_2P_MATED_PLUG", "#3A4044", 1.0))
    return Compound(label="C3_CARRIER_PCB10_WITH_DEVKITC", children=[board, devkit, *rows, *uprights, *screws, *headers])


def _tcrt_ski_cartridge(name, center):
    """TCRT5000 on its bezel with the J10-10 pigtail soldered to its leads (D-016)."""
    x, y, z = center
    parts = [
        # Optical face down (flip 180 deg about X); face plane at TCRT_OPTICAL_FACE_Z, leads point up.
        _place(
            _purchased_step("vishay_tcrt5000.step", f"TCRT5000_{name}_STEP", [(Axis.X, 180.0)]),
            x, y, TCRT_OPTICAL_FACE_Z, ref={"Z": "min"},
        ),
        _paint(_block(*REAR_TCRT_LEAD_JOINTS), f"TCRT_{name}_LEAD_JOINTS_HEATSHRINK", "#2E3336", 0.6),
    ]
    return Compound(label=f"TCRT_{name}_REAR_KEEL_CARTRIDGE", children=parts)


@functools.lru_cache(maxsize=None)
def _gp2y_package():
    """Sharp GP2Y0A21YK0F vendor STEP, ears trimmed (D-027), lenses +X, connector up."""
    # STEP frame: lenses +Z, width X, connector +Y. X 90 then Z 90 turns the
    # lenses to +X, the width to Y and the connector up.
    package = _place(
        _purchased_step("sharp_gp2y0a21yk0f.step", "GP2Y0A21YK0F_STEP", [(Axis.X, 90.0), (Axis.Z, 90.0)], folder=V1_PURCHASED),
        FRONT_RANGE_SENSOR_FACE_X, FRONT_RANGE_SENSOR_Y, FRONT_RANGE_SENSOR_BOTTOM_Z, ref={"X": "max", "Z": "min"},
    )
    t = FRONT_RANGE_EAR_TRIM_HALF_WIDTH
    package = package & _block(FRONT_RANGE_SENSOR_FACE_X - 30.0, FRONT_RANGE_SENSOR_FACE_X + 1.0, -t, t, 0.0, 80.0)
    return _paint(package, "GP2Y0A21YK0F_STEP", "#252525", 1.0)


@functools.lru_cache(maxsize=None)
def _gp2y_header_box():
    """Bounding box of the S3B-PH header: the part of the package above the 13 mm body."""
    z0 = FRONT_RANGE_SENSOR_BOTTOM_Z + 13.0
    return (_gp2y_package() & _block(0.0, 200.0, -30.0, 30.0, z0, z0 + 10.0)).bounding_box()


def _gp2y_lead_hump():
    """Lid hump over the header and lead (outer, cavity); the cap's top notch passes it."""
    hb = _gp2y_header_box()
    c, w = FRONT_RANGE_HUMP_CLEARANCE, FRONT_RANGE_HUMP_WALL
    top = hb.max.Z + FRONT_RANGE_LEAD_RESERVE_H + c
    x0 = hb.min.X - c - FRONT_RANGE_HUMP_REAR_RUN
    cavity = _block(x0, hb.max.X + c, hb.min.Y - c, hb.max.Y + c, BALL_POD_LID_Z[0] - 0.1, top)
    outer = _block(x0 - w, hb.max.X + c + w, hb.min.Y - c - w, hb.max.Y + c + w, BALL_POD_LID_Z[0], top + w)
    return outer, cavity


def sensors():
    package = _gp2y_package()
    hb = _gp2y_header_box()
    parts = [
        package,
        _paint(
            _block(hb.min.X, hb.max.X, hb.min.Y, hb.max.Y, hb.max.Z, hb.max.Z + FRONT_RANGE_LEAD_RESERVE_H),
            "GP2Y_J10_8_SOLDERED_LEAD_RESERVE",  # D-027: wires soldered to the S3B-PH pins, no plug
            "#79C4CB",
            0.30,
        ),
        _cylinder(1.2, 42.0, (FRONT_RANGE_SENSOR_FACE_X + 21.0, FRONT_RANGE_SENSOR_Y, FRONT_RANGE_SENSOR_Z), "GP2Y_OPTICAL_AXIS", "#EE4B3B", 0.70, "x"),
        tactile_ball_nose(),
    ]
    return Compound(label="BODY_SENSORS", children=parts)


def imu_board():
    """PCB-07: ICM-42688-P on its own board, screwed flat to the chassis deck crossbar."""
    cx, cy, cz = IMU_BOARD_CENTER
    bx, by, bz = IMU_BOARD_SIZE
    top = cz + bz / 2.0
    board = _box(bx, by, bz, IMU_BOARD_CENTER, "IMU_PCB07_BOARD", PCB_GREEN, 1.0)
    for sign in (1.0, -1.0):
        board = board - _z_cylinder(1.1, cz - bz, top + 1.0, IMU_SCREW_X, sign * IMU_SCREW_HALF_Y)
    chip = _box(*IMU_CHIP_SIZE, (cx, cy, top + IMU_CHIP_SIZE[2] / 2.0), "IMU_ICM42688P_PACKAGE", "#1E2426", 1.0)
    # JST GH SM08B-GHS-TB side entry, mating face on the board's -X edge
    # (STEP mating face is -Y: -90 deg about Z turns it to -X).
    connector = _place(
        _gh_header(8, "IMU_JST_GH_SM08B_HEADER", [(Axis.Z, -90.0)]),
        cx - bx / 2.0, cy, top, ref={"X": "min", "Y": "center", "Z": "min"},
    )
    parts = [_paint(board, "IMU_PCB07_BOARD", PCB_GREEN, 1.0), chip, connector]
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        # M2 x 5 pan head (Ø3.8 x 1.3) on the board; the shank thread-forms 4 mm into the deck.
        head = _paint(_z_cylinder(1.9, top, top + 1.3, IMU_SCREW_X, sign * IMU_SCREW_HALF_Y), f"IMU_M2_SCREW_HEAD_{side}", STEEL, 1.0)
        shank = _paint(_z_cylinder(1.0, top - 5.0, top, IMU_SCREW_X, sign * IMU_SCREW_HALF_Y), f"IMU_M2_SCREW_SHANK_{side}", STEEL, 1.0)
        parts.extend([head, shank])
    return Compound(label="IMU_PCB07", children=parts)


def _mic_board(x, y, z, name):
    """PCB-06: one IM73D122V01 on the port axis, inboard face, JST GH 4-pin below it."""
    sign = 1.0 if y > 0.0 else -1.0
    wx, wy, wz = MIC_BOARD_SIZE
    board_y = sign * (MIC_BOARD_OUTER_Y - wy / 2.0)
    board_z = z + 2.0 - wz / 2.0  # board top 2 mm over the mic axis; the GH header fills the rest below
    board = _box(wx, wy, wz, (x, board_y, board_z), f"PDM_MIC_{name}_PCB06", PCB_GREEN, 0.94)
    # Ø0.8 acoustic hole through the board on the port axis (Infineon footprint note).
    board = board - _cylinder(0.4, wy + 1.0, (x, board_y, z), "hole", PCB_GREEN, 1.0, "y")
    inboard = sign * (MIC_BOARD_OUTER_Y - wy)
    px, py, pz = MIC_PACKAGE_SIZE
    mic = _box(px, py, pz, (x, inboard - sign * py / 2.0, z), f"PDM_MIC_{name}_IM73D122", "#C9CDD0", 1.0)
    # JST GH SM04B-GHS-TB on the inboard face, mating face on the board's bottom
    # edge so the plug enters from below: STEP -Y (mating) to -Z, STEP +Z (height)
    # inboard. The right-hand board is the same header turned 180 deg about Z.
    turns = [(Axis.X, 90.0)] if sign > 0 else [(Axis.X, 90.0), (Axis.Z, 180.0)]
    connector = _place(
        _gh_header(4, f"PDM_MIC_{name}_JST_GH_SM04B_HEADER", turns),
        x, inboard, board_z - wz / 2.0, ref={"X": "center", "Y": "max" if sign > 0 else "min", "Z": "min"},
    )
    return [_paint(board, f"PDM_MIC_{name}_PCB06", PCB_GREEN, 0.94), mic, connector]


def body_audio():
    """Selected speaker (K 50 WP), PCB-05 front end and four PCB-06 microphone boards."""
    sx, sy, sz = SPEAKER_CENTER
    cavity = _cylinder(
        SPEAKER_BASKET_DIAMETER / 2.0 + 2.0,
        SPEAKER_CAVITY_DEPTH,
        (SPEAKER_CAVITY_CENTER_X, sy, sz),
        "SPEAKER_ACOUSTIC_CAVITY_KEEP_OUT",
        "#59B7D6",
        0.16,
        "x",
    )
    # Visaton K 50 WP: Ø50 frame flange at the front, basket tapering back to the magnet;
    # 18 mm overall from the frame face. Only the outline is vendor data.
    front = SPEAKER_FRONT_X
    flange_x1 = front - SPEAKER_FLANGE_DEPTH
    basket_x1 = flange_x1 - SPEAKER_BASKET_DEPTH
    rear = front - SPEAKER_DEPTH
    flange = _cylinder(SPEAKER_BASKET_DIAMETER / 2.0, SPEAKER_FLANGE_DEPTH, ((front + flange_x1) / 2.0, sy, sz), "flange", SLATE_DARK, 1.0, "x")
    flange = flange - _cylinder(SPEAKER_CONE_DIAMETER / 2.0, SPEAKER_FLANGE_DEPTH + 1.0, ((front + flange_x1) / 2.0, sy, sz), "cut", SLATE_DARK, 1.0, "x")
    # build123d Cone runs bottom (-Z) to top (+Z); -90 deg about Y puts the wide end forward (+X).
    basket = Cone(SPEAKER_CUTOUT_DIAMETER / 2.0, SPEAKER_BASKET_REAR_DIAMETER / 2.0, SPEAKER_BASKET_DEPTH).rotate(Axis.Y, -90.0)
    basket = basket.moved(Location(((flange_x1 + basket_x1) / 2.0, sy, sz)))
    cone = _cylinder(SPEAKER_CONE_DIAMETER / 2.0, 1.0, (front - 0.5, sy, sz), "SPEAKER_K50WP_CONE", "#252B2E", 1.0, "x")
    magnet = _cylinder(SPEAKER_MAGNET_DIAMETER / 2.0, basket_x1 - rear, ((basket_x1 + rear) / 2.0, sy, sz), "SPEAKER_K50WP_MAGNET", BRONZE, 1.0, "x")
    speaker = Compound(label="SPEAKER_VISATON_K50WP_8OHM", children=[
        _paint(flange, "SPEAKER_K50WP_FRAME_FLANGE", SLATE_DARK, 0.92),
        _paint(basket, "SPEAKER_K50WP_BASKET", SLATE_DARK, 0.92),
        cone,
        magnet,
    ])
    px, py, pz = PCB05_CENTER
    wx, wy, wz = PCB05_SIZE
    board_z0 = pz - wz / 2.0
    pcb05 = Compound(label="PCB05_AUDIO_FRONT_END", children=[
        _box(wx, wy, PCB05_BOARD_THICKNESS, (px, py, board_z0 + PCB05_BOARD_THICKNESS / 2.0), "PCB05_AUDIO_FRONT_END_PCB", PCB_GREEN, 1.0),
        _box(wx, wy, wz - PCB05_BOARD_THICKNESS, (px, py, board_z0 + PCB05_BOARD_THICKNESS + (wz - PCB05_BOARD_THICKNESS) / 2.0), "PCB05_AUDIO_FRONT_END_PARTS_RESERVE", PCB_GREEN, 0.30),
    ])
    parts = [cavity, speaker, pcb05]
    for x, y, z, name in MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0
        port = _cylinder(1.25, 8.0, (x, sign * 74.0, z), f"PDM_MIC_{name}_ACOUSTIC_PORT", "#252B2E", 1.0, "y")
        boot = _cylinder(3.0, 5.0, (x, sign * 72.5, z), f"PDM_MIC_{name}_PORT_BOOT", RUBBER, 0.90, "y")
        parts.append(Compound(label=f"PDM_MIC_{name}", children=[*_mic_board(x, y, z, name), port, boot]))
    return Compound(label="BODY_AUDIO", children=parts)


def _ring(r0, r1, z0, z1, x=BODY_AXIS_X):
    """Vertical ring on the body/yaw axis unless another X is given."""
    return Cylinder(r1, z1 - z0).moved(Location((x, 0.0, (z0 + z1) / 2.0))) - Cylinder(
        r0, z1 - z0 + 2.0
    ).moved(Location((x, 0.0, (z0 + z1) / 2.0)))


def body_yaw_stage():
    """Stationary half of the head yaw stage: bearing, pinion, shaft and servo."""
    px, py = YAW_PINION_CENTER
    px += BODY_AXIS_X
    gear_z = (YAW_BEARING_Z[1] + 1.0, YAW_DISC_PLATE_BOTTOM_Z)
    x0, x1, y0, y1, z0, z1 = YAW_SERVO_ENVELOPE
    # Scissor pinion: fixed half (keyed to the shaft) below, spring-loaded
    # loose half above, 0.2 mm apart; both engage the 5 mm driven gear face.
    half = YAW_SCISSOR_HALF_FACE
    pinion_fixed = Cylinder(YAW_GEAR_OUTER_RADIUS, half).moved(Location((px, py, gear_z[0] + half / 2.0)))
    pinion_loose = Cylinder(YAW_GEAR_OUTER_RADIUS, half).moved(Location((px, py, gear_z[0] + half + YAW_SCISSOR_GAP + half / 2.0)))
    shaft = Cylinder(2.5, gear_z[0] - z1).moved(Location((px, py, (gear_z[0] + z1) / 2.0)))
    return Compound(label="BODY_YAW_STAGE", children=[
        _paint(_ring(*YAW_BEARING_RADII, *YAW_BEARING_Z), "YAW_THIN_SECTION_BEARING_ENVELOPE", STEEL, 0.9),
        _paint(pinion_fixed, "YAW_DRIVE_SCISSOR_PINION_FIXED_HALF", STEEL, 1.0),
        _paint(pinion_loose, "YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF", BRONZE, 1.0),
        _paint(shaft, "YAW_SERVO_COUPLING_SHAFT", STEEL, 1.0),
        # XC330 dummy assembly: output horn axis is STEP Z, body runs -24.5..+9.5 in STEP Y
        # from that axis. -90 deg about Z runs the body along X (+180 hit the left upper rail; both clear the Pi
        # cooler), output axis on the pinion centre, horn top at z1.
        _place(
            _purchased_step("robotis_xc330_dummy_assy.step", "YAW_SERVO_XC330_M181_STEP", [(Axis.Z, -90.0)]),
            px, py, z1, ref={"X": "origin", "Y": "origin", "Z": "max"},
        ),
    ])


def yaw_drive_moving_parts():
    """Yaw-moving body-side parts in chassis coordinates (axisymmetric)."""
    gear_z = (YAW_BEARING_Z[1] + 1.0, YAW_DISC_PLATE_BOTTOM_Z)
    return [
        _paint(_ring(YAW_GEAR_BORE_RADIUS, YAW_GEAR_OUTER_RADIUS, *gear_z), "YAW_DRIVEN_SPUR_1TO1_ON_DISC", SLATE_DARK, 1.0),
        _paint(_ring(*YAW_BEARING_RADII, YAW_BEARING_Z[1], YAW_BEARING_Z[1] + 1.0), "YAW_BEARING_CLAMP_RING", SLATE_DARK, 1.0),
    ]


def yaw_drive_moving_local():
    """Yaw-moving body-side parts, in head-local coordinates (move with head)."""
    parts = yaw_drive_moving_parts()
    offset = Location(tuple(-v for v in HEAD_ORIGIN_IN_CHASSIS))
    return Compound(label="BODY_YAW_DRIVE_MOVING", children=[part.moved(offset) for part in parts])


def harness_routes():
    # Routed-volume representation: orange high current, red motor power,
    # cyan signal, and violet head link. Volumes include bend/strain reserve.
    parts = [
        # Power routes stay in the 7 mm slot under the PCB-03/04 plates (Z 56.5-63) and beside the IMU
        # (X 3.5-28.5, Y +-12.5): the trunk runs at Y +18 and the branch crosses aft of the IMU. The
        # motor-can top (Z 57.4 at Y >= 16) and the Y 6-18 pigtail reserve (X -13..-1) set the trunk's floor and rear end.
        _box(42.0, 10.0, 5.0, (21.0, 18.0, 60.0), "HARNESS_BATTERY_TRUNK", "#F28C28", 0.42),
        _box(7.0, 92.0, 6.0, (HARNESS_MOTOR_BRANCH_X, 0.0, 59.5), "HARNESS_MOTOR_BRANCH", "#D94A3A", 0.42),  # behind the driver posts, toward the tie bridges (D-031)
        _box(82.0, 8.0, 8.0, (30.0 + BODY_SHIFT_X, 26.0, 82.0), "HARNESS_SIGNAL_TRUNK", "#2FAFC2", 0.42),
        _box(82.0, 8.0, 8.0, (30.0 + BODY_SHIFT_X, -26.0, 82.0), "HARNESS_SENSOR_TRUNK", "#44BDD0", 0.42),
        # Flat clock-spring loop under the disc takes the ±55° yaw twist.
        _paint(_ring(*YAW_CLOCKSPRING_RADII, *YAW_BEARING_Z), "HARNESS_HEAD_YAW_CLOCKSPRING_RESERVE", "#9566D9", 0.20),
        # Head trunk (connector-schedule.md): down the plate's Ø18 bore, along the
        # plate underside to the -Y yaw junction, then down a -Y riser to PCB-03/04,
        # so it no longer passes through the compute tray and the Pi cooler.
        _paint(_block(BODY_AXIS_X - 6.0, BODY_AXIS_X + 6.0, -24.0, 6.0, 127.0, YAW_PLATE_Z[0] - 0.5), "HARNESS_HEAD_TRUNK_UNDER_PLATE", "#9566D9", 0.35),
        _paint(_block(-22.0, -2.0, -40.0, -23.0, 100.0, 126.0), "HARNESS_HEAD_RISER_UPPER", "#9566D9", 0.35),
        _paint(_block(-28.0, -16.0, -50.0, -40.0, 75.0, 112.0), "HARNESS_HEAD_RISER_LOWER", "#9566D9", 0.35),
        # CSI (PCN-36 15-to-22 FFC, 11.5 mm wide): straight down the axis bore and
        # beside the cooler into the Pi 5's rear FPC socket; demated at the Pi.
        _paint(_block(BODY_AXIS_X, 30.0, -26.5, -11.0, 127.0, YAW_PLATE_Z[0] - 0.5), "HARNESS_CSI_FFC_UNDER_PLATE", "#65A584", 0.35),
        _paint(_block(26.0, 29.0, -26.5, -11.0, 99.6, 127.0), "HARNESS_CSI_FFC_DROP_TO_PI_CAM", "#65A584", 0.35),
        # Nose pod J10-8 (D-011): GP2Y lead plus switch pair as one flat 5-way run from the pod's
        # back-wall slot under the front crossmember, up the O5 bore through crossmember and deck,
        # beside the speaker cavity into the sensor trunk, then across to the C3 carrier header.
        _paint(_block(83.5, BALL_POD_X[0], NOSE_CABLE_RISER_XY[1] - 2.5, 3.0, 32.8, 34.9), "HARNESS_NOSE_J10_8_UNDER_CROSSMEMBER", "#44BDD0", 0.42),
        _paint(_z_cylinder(2.0, 34.9, DECK_Z + 2.0, *NOSE_CABLE_RISER_XY), "HARNESS_NOSE_J10_8_CROSSMEMBER_BORE", "#44BDD0", 0.42),
        _paint(_block(NOSE_CABLE_RISER_XY[0] - 3.0, NOSE_CABLE_RISER_XY[0] + 3.0, NOSE_CABLE_RISER_XY[1] - 3.0, NOSE_CABLE_RISER_XY[1] + 3.0, DECK_Z + 2.0, 78.0), "HARNESS_NOSE_J10_8_RISER", "#44BDD0", 0.42),
        _paint(_block(40.0, 46.0, -46.0, -30.0, 78.0, 84.0), "HARNESS_NOSE_J10_8_DROP_TO_C3", "#44BDD0", 0.42),
    ]
    # Rear TCRT J10-10 pigtail: up out of the keel top behind the rear
    # crossmember, a 30 mm slack loop (the keel and sensor drop for the J09
    # shims and service), zip-tied at the crossmember lug, up beside PCB-02, forward over
    # PCB-04 and under the compute tray, then out to the C3 carrier header.
    rx0, rx1, ry0, ry1 = REAR_TCRT_CABLE_RISER
    rz0, rz1 = REAR_TCRT_CABLE_RUN_Z
    parts += [
        _paint(_block(rx0, -49.0, ry1, 3.0, 35.0, 44.0), "HARNESS_REAR_TCRT_J10_10_SERVICE_LOOP", "#44BDD0", 0.42),
        _paint(_block(rx0, rx1, ry0, ry1, 35.0, rz1), "HARNESS_REAR_TCRT_J10_10_RISER", "#44BDD0", 0.42),
        _paint(_block(rx1, 27.0, ry0, ry1, rz0, rz1), "HARNESS_REAR_TCRT_J10_10_RUN_OVER_PCB04", "#44BDD0", 0.42),
        _paint(_block(21.0, 27.0, -49.4, ry0, rz0, rz1), "HARNESS_REAR_TCRT_J10_10_DROP_TO_C3", "#44BDD0", 0.42),
        _paint(_block(21.0, 27.0, -49.4, -44.0, rz1, 94.1), "HARNESS_REAR_TCRT_J10_10_RISE_TO_PLUG", "#44BDD0", 0.42),
    ]
    return Compound(label="HARNESS_ROUTES", children=parts)


MATED_POWER_PLUG_LENGTH = 12.0  # Micro-Fit receptacle housing beyond the header face (E)
MATED_POWER_PLUG_HEIGHT = 10.0  # (E)


def _yaw_junction_board():
    """PCB-08: clock-spring stator board with the body-side connectors."""
    x0, x1, y0, y1, _z0, _z1 = YAW_JUNCTION_BOX
    pz0, pz1 = YAW_JUNCTION_PLATE_Z
    parts = [_paint(_block(x0, x1, y0, y1, pz0, pz1), "YAW_JUNCTION_PCB08_BOARD", PCB_GREEN, 1.0)]
    # J8-1 Micro-Fit 3.0 2x3 right-angle on the -X edge, mating -X (D-039: was Micro-Fit+).
    w = connector_width("MF3", 6)
    yc = (YAW_JUNCTION_MF_PLUG_RESERVE[2] + YAW_JUNCTION_MF_PLUG_RESERVE[3]) / 2.0
    parts.append(_paint(_block(x0, x0 + 10.0, yc - w / 2.0, yc + w / 2.0, pz1, pz1 + MATED_POWER_PLUG_HEIGHT), "YAW_JUNCTION_J8_1_MICROFIT3_6P_RA_HEADER", "#2E3336", 1.0))
    parts.append(_paint(_block(x0 - MATED_POWER_PLUG_LENGTH, x0, yc - w / 2.0, yc + w / 2.0, pz1, pz1 + MATED_POWER_PLUG_HEIGHT), "YAW_JUNCTION_J8_1_MICROFIT3_6P_MATED_PLUG", "#3A4044", 1.0))
    for cid, n, gy0 in YAW_JUNCTION_GH:
        hdr = _place(_gh_header(n, f"YAW_JUNCTION_{_cid(cid)}_JST_GH_BM{n:02d}B_HEADER", top_entry=True), -10.0, gy0, pz1, ref={"X": "min", "Y": "min", "Z": "min"})
        b = hdr.bounding_box()
        parts.append(hdr)
        parts.append(_box(gh_plug_width(n), GH_PLUG_THICKNESS, GH_PLUG_PROUD, ((b.min.X + b.max.X) / 2.0, (b.min.Y + b.max.Y) / 2.0, b.max.Z + GH_PLUG_PROUD / 2.0), f"YAW_JUNCTION_{_cid(cid)}_GHR{n:02d}_MATED_PLUG", "#F4F1E6", 1.0))
    return Compound(label="YAW_JUNCTION_PCB08", children=parts)


def _c0_link_adapter():
    """PCB-09: 2 x 20 socket on the Pi header, strip over it, two THVD1451, GH headers."""
    z0, z1 = C0_LINK_ADAPTER_PLATE_Z
    sx0, sx1, sy0, sy1, _a, _b = C0_LINK_ADAPTER_STRIP
    bx0, bx1, by0, by1, _a, _b = C0_LINK_ADAPTER_BRIDGE
    wx0, wx1, wy0, wy1, _a, _b = C0_LINK_ADAPTER_BOX
    plate = _block(sx0, sx1, sy0, sy1, z0, z1) + _block(bx0, bx1, by0, by1, z0, z1) + _block(wx0, wx1, wy0, wy1, z0, z1)
    parts = [
        _paint(plate, "C0_LINK_ADAPTER_PCB09_BOARD", PCB_GREEN, 1.0),
        _paint(_block(*C0_GPIO_SOCKET), "C0_GPIO_2X20_SOCKET_BODY", "#2E3336", 1.0),
        # THVD1451D SOIC-14 (8.65 x 6.0 incl. leads x 1.75): head link on the bridge, base link on the wide part.
        _paint(_block(27.0, 35.65, 22.5, 28.5, z1, z1 + 1.75), "C0_THVD1451_HEAD_LINK_SOIC14", "#1E2426", 1.0),
        _paint(_block(27.0, 35.65, 30.0, 36.0, z1, z1 + 1.75), "C0_THVD1451_BASE_LINK_SOIC14", "#1E2426", 1.0),
    ]
    tops = (("J9-2", 6, 37.0, 30.0), ("J9-3", 10, 37.0, 36.5))  # id, circuits, x0, y0
    for cid, n, gx0, gy0 in tops:
        hdr = _place(_gh_header(n, f"C0_{_cid(cid)}_JST_GH_BM{n:02d}B_HEADER", top_entry=True), gx0, gy0, z1, ref={"X": "min", "Y": "min", "Z": "min"})
        b = hdr.bounding_box()
        parts.append(hdr)
        parts.append(_box(gh_plug_width(n), GH_PLUG_THICKNESS, GH_PLUG_PROUD, ((b.min.X + b.max.X) / 2.0, (b.min.Y + b.max.Y) / 2.0, b.max.Z + GH_PLUG_PROUD / 2.0), f"C0_{_cid(cid)}_GHR{n:02d}_MATED_PLUG", "#F4F1E6", 1.0))
    # J9-1 GH 6 side entry on the +Y edge, mating +Y (STEP -Y turned 180 deg about Z).
    hdr = _place(_gh_header(6, "C0_J9_1_JST_GH_SM06B_HEADER", [(Axis.Z, 180.0)]), 26.2, wy1, z1, ref={"X": "min", "Y": "max", "Z": "min"})
    b = hdr.bounding_box()
    parts.append(hdr)
    parts.append(_box(gh_plug_width(6), GH_PLUG_PROUD, GH_PLUG_THICKNESS, ((b.min.X + b.max.X) / 2.0, wy1 + GH_PLUG_PROUD / 2.0, z1 + GH_PLUG_THICKNESS / 2.0), "C0_J9_1_GHR06_MATED_PLUG", "#F4F1E6", 1.0))
    return Compound(label="C0_LINK_ADAPTER_PCB09", children=parts)


def _pcb05_connectors():
    """Side-entry GH headers and the Micro-Fit 3.0 power header on PCB-05's edges."""
    px, py, pz = PCB05_CENTER
    wx, wy, wz = PCB05_SIZE
    x0, x1, y0, y1 = px - wx / 2.0, px + wx / 2.0, py - wy / 2.0, py + wy / 2.0
    top = pz - wz / 2.0 + PCB05_BOARD_THICKNESS
    parts = []
    edges = {
        "PY": ([(Axis.Z, 180.0)], (("J5-2", 4, 46.0), ("J5-3", 4, 55.25), ("J5-6", 2, 64.5))),
        "NY": ([], (("J5-4", 4, 46.0), ("J5-5", 4, 55.25))),
    }
    for edge, (turns, row) in edges.items():
        sign = 1.0 if edge == "PY" else -1.0
        ey = y1 if edge == "PY" else y0
        for cid, n, hx0 in row:
            hdr = _place(_gh_header(n, f"PCB05_{_cid(cid)}_JST_GH_SM{n:02d}B_HEADER", turns), hx0, ey, top, ref={"X": "min", "Y": "max" if sign > 0 else "min", "Z": "min"})
            b = hdr.bounding_box()
            parts.append(hdr)
            parts.append(_box(gh_plug_width(n), GH_PLUG_PROUD, GH_PLUG_THICKNESS, ((b.min.X + b.max.X) / 2.0, ey + sign * GH_PLUG_PROUD / 2.0, top + GH_PLUG_THICKNESS / 2.0), f"PCB05_{_cid(cid)}_GHR{n:02d}_MATED_PLUG", "#F4F1E6", 1.0))
    # J5-1 host GH 10 on the rear edge, mating -X.
    hdr = _place(_gh_header(10, "PCB05_J5_1_JST_GH_SM10B_HEADER", [(Axis.Z, -90.0)]), x0, py, top, ref={"X": "min", "Y": "center", "Z": "min"})
    parts.append(hdr)
    parts.append(_box(GH_PLUG_PROUD, gh_plug_width(10), GH_PLUG_THICKNESS, (x0 - GH_PLUG_PROUD / 2.0, py, top + GH_PLUG_THICKNESS / 2.0), "PCB05_J5_1_GHR10_MATED_PLUG", "#F4F1E6", 1.0))
    # J5-7 PB-AUDIO-OUT: Micro-Fit 3.0 2x1 right-angle on the -Y edge.
    w = connector_width("MF3", 2)
    parts.append(_paint(_block(64.5, 64.5 + w, y0, y0 + 10.0, top, top + MATED_POWER_PLUG_HEIGHT), "PCB05_J5_7_MICROFIT3_2P_RA_HEADER", "#2E3336", 1.0))
    parts.append(_paint(_block(64.5, 64.5 + w, y0 - MATED_POWER_PLUG_LENGTH, y0, top, top + MATED_POWER_PLUG_HEIGHT), "PCB05_J5_7_MICROFIT3_2P_MATED_PLUG", "#3A4044", 1.0))
    return Compound(label="PCB05_CONNECTORS", children=parts)


def _edge_power_plugs():
    """Mated Micro-Fit plugs on the PCB-02/03/04 edges, spread inside each edge reserve."""
    boards = {"PCB03": PCB03_BOX, "PCB04": PCB04_BOX}
    parts = []
    for name, strip in CONNECTOR_EDGE_STRIPS.items():
        widths = [connector_width(fam, n) for _cid, fam, n, _w in strip["connectors"]]
        s0, s1 = strip["span"]
        pos = s0 + (s1 - s0 - sum(widths) - CONNECTOR_GAP * (len(widths) - 1)) / 2.0
        for (cid, fam, n, _what), w in zip(strip["connectors"], widths):
            label = f"{_cid(cid)}_{'MICROFIT_PLUS' if fam == 'MF+' else 'MICROFIT3'}_{n}P_MATED_PLUG"
            if name == "PCB02_NY":
                bx0 = PCB02_BOX[0] + PCB_THICKNESS
                box = (bx0, bx0 + MATED_POWER_PLUG_HEIGHT, PCB02_BOX[2] - MATED_POWER_PLUG_LENGTH, PCB02_BOX[2], pos, pos + w)
            else:
                b = boards[name[:5]]
                ztop = b[4] + PCB_THICKNESS
                if name.endswith("PY"):
                    box = (pos, pos + w, b[3], b[3] + MATED_POWER_PLUG_LENGTH, ztop, ztop + MATED_POWER_PLUG_HEIGHT)
                else:
                    box = (pos, pos + w, b[2] - MATED_POWER_PLUG_LENGTH, b[2], ztop, ztop + MATED_POWER_PLUG_HEIGHT)
            parts.append(_paint(_block(*box), label, "#3A4044", 1.0))
            pos += w + CONNECTOR_GAP
    # Motor pairs: Micro-Fit 3.0 1x2 wire-to-wire, mated (43640 plug + 43645 receptacle, E).
    x0, x1, y0, y1, z0, z1 = MOTOR_INLINE_RESERVE["L"]
    pairs = {"L": _block(x0 + 0.5, x0 + 19.5, y0 + 1.0, y0 + 8.0, z0 + 1.0, z0 + 11.0)}  # 19 x 7 x 10, along X
    x0, x1, y0, y1, z0, z1 = MOTOR_INLINE_RESERVE["R"]
    pairs["R"] = _block(x0, x1, y0 + 1.0, y0 + 20.0, z0 + 1.0, z0 + 11.0)  # 7 x 19 x 10, along Y
    for side, pair in pairs.items():
        parts.append(_paint(pair, f"MOTOR_{side}_MICROFIT3_1X2_WIRE_TO_WIRE_MATED_PAIR", "#3A4044", 1.0))
    return Compound(label="EDGE_AND_INLINE_POWER_PLUGS", children=parts)


def connectors_and_exits():
    """Mated-connector and cable-exit reserves (connector-schedule.md).

    Reserves are translucent keep-outs for the mated plug plus the lead's first
    bend; they touch their own board but must clear every real part. Labels
    ending in _OPEN are known clashes recorded for follow-up, not placements.
    """
    reserve = "#79C4CB"
    power = "#E7A95B"
    parts = []
    for name, strip in CONNECTOR_EDGE_STRIPS.items():
        ids = "_".join(c[0].replace("-", "") for c in strip["connectors"])
        parts.append(_paint(_block(*strip["box"]), f"{name}_EDGE_CONNECTORS_{ids}_RESERVE", power, 0.30))
    for name, layer in CONNECTOR_TOP_LAYERS.items():
        parts.append(_paint(_block(*layer["box"]), f"{name}_TOP_ENTRY_SIGNAL_PLUG_LAYER_RESERVE", reserve, 0.14))
    parts += [
        _paint(_block(*CHARGE_INLET_RECEPTACLE), "CHARGE_INLET_USBC_VERTICAL_RECEPTACLE_ENVELOPE", "#B7BFC0", 1.0),
        _paint(_block(*CHARGE_INLET_OUTSIDE_CORRIDOR), "CHARGE_INLET_OUTSIDE_PLUG_CORRIDOR_KEEP_OUT", reserve, 0.20),
        _paint(_block(*PI_POWER_PLUG_RESERVE), "PI5_POWER_USBC_RIGHT_ANGLE_PLUG_RESERVE", power, 0.35),
        _paint(_block(*PI_POWER_PIGTAIL_DROP), "PI5_POWER_PIGTAIL_DROP_RESERVE", power, 0.30),
        _paint(_block(*YAW_JUNCTION_BOX), "YAW_JUNCTION_PCB08_WITH_CONNECTORS_RESERVE", "#9566D9", 0.30),
        _paint(_block(*C0_LINK_ADAPTER_BOX), "C0_LINK_ADAPTER_PCB09_RESERVE", reserve, 0.30),
    ]
    parts += [
        _paint(_block(*MOTOR_INLINE_RESERVE[side]), f"MOTOR_{side}_INLINE_MICROFIT3_1X2_RESERVE", power, 0.30) for side in ("L", "R")
    ]
    parts += [
        _paint(_block(*C3_GH_PLUG_LAYER), "C3_CARRIER_TOP_ENTRY_SIGNAL_PLUG_LAYER_RESERVE", reserve, 0.14),
        _paint(_block(*C3_POWER_PLUG_RESERVE), "C3_CARRIER_EDGE_CONNECTOR_J101_RESERVE", power, 0.30),
        _paint(_block(*C3_DEVKIT_USB_CORRIDOR), "C3_DEVKITC_USB_SERVICE_CORRIDOR_KEEP_OUT", reserve, 0.12),
        _paint(_block(*PACK_DISCONNECT_SLIDE_PATH), "PACK_DISCONNECT_SERVICE_SLIDE_PATH_KEEP_OUT", reserve, 0.12),
        _paint(_block(*PACK_NTC_BREAK_RESERVE), "PACK_NTC_BREAK_JST_SM2_RESERVE", reserve, 0.30),
        _paint(_block(*BATBUS_SPLICE_RESERVE), "BATBUS_STAR_SPLICE_RESERVE", power, 0.30),
        _paint(_block(*PACK_NTC_BREAK_PAIR), "PACK_NTC_BREAK_JST_SM2_WIRE_TO_WIRE_MATED_PAIR", "#F4F1E6", 1.0),
        _paint(_block(*YAW_JUNCTION_MF_PLUG_RESERVE), "YAW_JUNCTION_J81_PLUG_RESERVE", power, 0.30),
        _paint(_block(*C0_LINK_ADAPTER_TOP_PLUGS), "C0_LINK_ADAPTER_TOP_ENTRY_PLUG_RESERVE", reserve, 0.20),
        _paint(_block(*C0_LINK_ADAPTER_SIDE_PLUG), "C0_LINK_ADAPTER_J91_PLUG_RESERVE", reserve, 0.20),
        _paint(_block(45.0, 75.0, 19.0, 28.0, 115.6, 120.0), "PCB05_PY_EDGE_PLUG_RESERVE", reserve, 0.20),
        _paint(_block(45.0, 75.0, -31.0, -19.0, 115.6, 125.6), "PCB05_NY_EDGE_PLUG_RESERVE", reserve, 0.20),
        _paint(_block(36.0, 45.0, -9.0, 9.0, 115.6, 120.0), "PCB05_REAR_EDGE_PLUG_RESERVE", reserve, 0.20),
    ]
    parts += [_yaw_junction_board(), _c0_link_adapter(), _pcb05_connectors(), _edge_power_plugs()]
    for name, (y, z) in BATBUS_SPLICE_YZ.items():
        splice = _axial_bore_x(BATBUS_SPLICE_RADIUS, BATBUS_SPLICE_X[0], BATBUS_SPLICE_X[1], y, z)
        parts.append(_paint(splice, f"BATBUS_{name}_BUTT_SPLICE_MATED_PAIR", "#C55842", 1.0))
    # GH plug and lead reserves in front of the IMU and microphone headers.
    ix, iy, iz = IMU_BOARD_CENTER
    top = iz + IMU_BOARD_SIZE[2] / 2.0
    w = connector_width("GH", 8)
    parts.append(_paint(_block(ix - IMU_BOARD_SIZE[0] / 2.0 - 9.0, ix - IMU_BOARD_SIZE[0] / 2.0, iy - w / 2.0, iy + w / 2.0, top, top + 4.5), "IMU_GH8_PLUG_RESERVE", reserve, 0.30))
    for x, y, z, name in MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0
        inboard = sign * (MIC_BOARD_OUTER_Y - MIC_BOARD_SIZE[1])
        bottom = z + 2.0 - MIC_BOARD_SIZE[2]
        w = connector_width("GH", 4)
        ys = sorted((inboard, inboard - sign * 4.5))
        parts.append(_paint(_block(x - w / 2.0, x + w / 2.0, ys[0], ys[1], bottom - 9.0, bottom), f"PDM_MIC_{name}_GH4_PLUG_RESERVE", reserve, 0.30))
    return Compound(label="CONNECTORS_AND_EXITS", children=parts)


def physics_overlays():
    props = mass_properties()
    cx, cy, cz = props["com_mm"]
    support_face = Plane.XY * Polygon(
        (WHEEL_CENTER_R[0], WHEEL_CENTER_R[1]),
        (BALL_CONTACT[0], BALL_CONTACT[1]),
        (WHEEL_CENTER_L[0], WHEEL_CENTER_L[1]),
        align=None,
    )
    support = _paint(extrude(support_face.moved(Location((0.0, 0.0, 0.4))), amount=0.8), "SUPPORT_POLYGON", "#D95FC5", 0.18)
    parts = [
        support,
        _sphere(7.0, (cx, cy, cz), "WHOLE_ROBOT_COM", "#F03C55", 0.80),
        _sphere(3.0, WHEEL_CENTER_L[:2] + (0.0,), "CONTACT_WHEEL_L", "#D95FC5", 0.8),
        _sphere(3.0, WHEEL_CENTER_R[:2] + (0.0,), "CONTACT_WHEEL_R", "#D95FC5", 0.8),
        _sphere(3.0, BALL_CONTACT, "CONTACT_BALL", "#D95FC5", 0.8),
        _triad(FRAMES["F_GROUND"], "AXES_GROUND", 20.0),
        _triad(FRAMES["F_HEAD_YAW"], "AXES_HEAD_YAW", 15.0),
        _cylinder(1.2, 194.0, (0.0, 0.0, AXLE_Z), "DRIVE_AXLE_AXIS", "#2266CC", 0.55, "y"),
        _cylinder(20.0, BALL_NATIVE_HEIGHT, (BALL_CONTACT[0], 0.0, BALL_NATIVE_HEIGHT / 2.0), "BALL_TRANSFER_SERVICE_KEEP_OUT", "#B35CD6", 0.12),
    ]
    return Compound(label="PHYSICS_OVERLAYS", children=parts)


def rp01_head_groups():
    source_head = _load_head_model().assembly()
    by_label = {child.label: child for child in source_head.children}
    # Split physical, harness and physics groups so Layout 02's viewer can
    # independently hide overlays while applying one shared yaw transform.
    head = Compound(
        label="RP01_HEAD_LAYOUT03_LIVE",
        children=[
            by_label["physical"],
            yaw_drive_moving_local(),
        ],
    )
    head = head.moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    harness = Compound(label="RP01_HEAD_HARNESS_LIVE", children=[by_label["harness"]]).moved(
        Location(HEAD_ORIGIN_IN_CHASSIS)
    )
    physics = Compound(label="RP01_HEAD_PHYSICS_LIVE", children=[by_label["physics"]]).moved(
        Location(HEAD_ORIGIN_IN_CHASSIS)
    )
    return head, harness, physics


def rp01_head_layout03():
    return rp01_head_groups()[0]


def _make_translucent(shape, alpha: float = 0.38, inherited_rgb=None):
    """Set one alpha across every leaf while retaining each part's color."""
    color = getattr(shape, "color", None)
    rgb = tuple(color)[:3] if color is not None else inherited_rgb
    children = list(shape.children) if getattr(shape, "children", None) else []
    if children:
        for child in children:
            _make_translucent(child, alpha, rgb)
    else:
        if rgb is None:
            rgb = (0.68, 0.72, 0.74)
        shape.color = Color(*rgb, alpha)
    return shape


def build_chassis_v1():
    """Chassis v1 review assembly, filtered from the Layout 02 model."""
    electronics_parts = {part.label: part for part in electronics().children}
    sensor_parts = {part.label: part for part in sensors().children}
    # CH-028 main-fuse holder envelope: chassis-owned (pack feed beside the tub).
    power_parts = {part.label: part for part in power_distribution_boards().children}
    assembly = Compound(label="CHASSIS_V1", children=[
        chassis_frame(),
        body_chassis_mount_hardware(),
        wheel_assembly("L"),
        wheel_assembly("R"),
        motor_envelope("L"),
        motor_envelope("R"),
        bearing_pair("L"),
        bearing_pair("R"),
        ball_transfer(),
        rear_skid_tcrt_module(),
        electronics_parts["BATTERY_2S1P_18650_PACK"],
        electronics_parts["ADAFRUIT_3297_DRV8833_LEFT"],
        electronics_parts["ADAFRUIT_3297_DRV8833_RIGHT"],
        electronics_parts["IMU_PCB07"],
        power_parts["PACK_ATOF_FUSE_HOLDER_ENVELOPE"],
        sensor_parts["GP2Y0A21YK0F_STEP"],
        sensor_parts["BALL_NOSE_CONCEALED_CONTACT_MODULE"],
    ])
    for part in assembly.children:
        # The frame and wheels overlap several surfaces in an isometric view.
        # Give them less opacity so their interiors remain visible in Solid mode.
        alpha = 0.30 if part.label in {"CHASSIS_PRIMARY_FRAME", "WHEEL_L", "WHEEL_R"} else 0.60
        _make_translucent(part, alpha)
    return assembly


def build_assembly():
    head, head_harness, head_physics = rp01_head_groups()
    asm = AssemblyHelper(LAYOUT_ID)
    asm.add(chassis_frame(), "CHASSIS_PRIMARY_FRAME")
    asm.add(body_primary_frame(), "BODY_PRIMARY_FRAME")
    asm.add(body_chassis_mount_hardware(), "BODY_CHASSIS_MOUNT_HARDWARE")
    asm.add(wheel_assembly("L"), "WHEEL_L")
    asm.add(wheel_assembly("R"), "WHEEL_R")
    asm.add(motor_envelope("L"), "MOTOR_L")
    asm.add(motor_envelope("R"), "MOTOR_R")
    asm.add(bearing_pair("L"), "BEARING_PAIR_L")
    asm.add(bearing_pair("R"), "BEARING_PAIR_R")
    asm.add(ball_transfer(), "BALL_TRANSFER")
    asm.add(rear_skid_tcrt_module(), "REAR_SKID_TCRT_MODULE")
    asm.add(electronics(), "BODY_ELECTRONICS")
    asm.add(sensors(), "BODY_SENSORS")
    asm.add(body_audio(), "BODY_AUDIO")
    asm.add(harness_routes(), "HARNESS_ROUTES")
    asm.add(connectors_and_exits(), "CONNECTORS_AND_EXITS")
    asm.add(body_shell(), "BODY_SHELL")
    asm.add(body_panels(), "BODY_PANELS")
    asm.add(panel_mount_hardware(), "PANEL_MOUNT_HARDWARE")
    asm.add(body_yaw_stage(), "BODY_YAW_STAGE")
    asm.add(head, "RP01_HEAD_LAYOUT03")
    asm.add(head_harness, "RP01_HEAD_HARNESS")
    asm.add(head_physics, "RP01_HEAD_PHYSICS")
    asm.add(physics_overlays(), "PHYSICS_OVERLAYS")
    return asm.build()
