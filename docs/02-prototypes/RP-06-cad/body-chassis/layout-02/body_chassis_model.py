"""RP-03 integrated body/chassis Layout 02.

Coordinate frame: millimetres; origin on ground at the drive-axle line and
robot centre plane; +X forward, +Y robot-left, +Z up.

The RP-01 Layout 04 head is composed from its live Python source; its yaw
datum, A0, mass and turntable size are read from that layout's generated files. Purchased
STEP geometry is imported through cadgen.step_scene.import_step.
"""

from __future__ import annotations

import importlib
import json
import math
import sys
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cone,
    Cylinder,
    Kind,
    Location,
    Plane,
    Polygon,
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
PURCHASED = HERE.parent / "layout-01" / "references" / "purchased"
# `HERE` is .../RP-06-cad/body-chassis/layout-02; the head layouts are
# siblings of body-chassis under the same RP-06 CAD root.
HEAD_DIR = HERE.parents[1] / "head" / "layout-04"

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
# gearmotor's output face bolts to a square face flange; a round boss carries
# the 608 pair and reaches into a pocket in the dished wheel, so nothing
# stationary sits inside the wheel's swept volume. An 8 mm stub shaft runs in
# the bearings, takes the motor's 4 mm D-shaft in a bore at its inboard end
# and is fixed to the wheel web at its outboard end. There is no axle
# crossmember: coaxial motors fill the axle line, so cheek plates carry each
# rail round its gearbox to the flange instead.
MOTOR_FACE_Y = 69.0
MOTOR_SHAFT_RADIUS = 2.0
MOTOR_SHAFT_LENGTH = 9.5  # JGA25-370 D-shaft past the face; measure the selected unit
AXLE_FLANGE_Y = (MOTOR_FACE_Y, 71.0)
AXLE_FLANGE_HALF_X = 17.0
AXLE_FLANGE_Z = (27.0, 57.0)
AXLE_BOSS_RADIUS = 15.0  # 608 OD 22 in an 11.25 bore, ~3.75 mm wall
AXLE_BOSS_END_Y = 86.0
AXLE_BORE_RADIUS = 11.25
BEARING_608_Y = (74.0, 81.5)  # bearing centres; inner races on the stub
WHEEL_POCKET_RADIUS = 18.0  # 3 mm radial running gap to the boss
WHEEL_POCKET_FLOOR_Y = 88.0  # 2 mm end gap past the boss
WHEEL_HUB_BORE_RADIUS = 4.0
STUB_SHAFT_RADIUS = 4.0
STUB_SHAFT_Y = (70.5, 95.0)  # 1.5 mm off the motor face
AXLE_CHEEK_X = (13.5, 17.0)  # |X| span; 1 mm off the gearbox, clear of the can
AXLE_CHEEK_Y = (50.0, MOTOR_FACE_Y)  # rail inner face to the flange
MOTOR_RELIEF_HALF_X = 17.0  # deck relief and shell-floor slot over the motors
WHEEL_RUNNING_CLEARANCE_MIN = 1.5
WHEEL_INDEX_R = (6.0, 35.0)  # radial span of the outer-face spin index, inside the tyre
WHEEL_INDEX_WIDTH = 4.0
WHEEL_INDEX_DEPTH = 0.8  # flush inlay: cut into the rim face, no added width

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
BALL_POD_SEAT_THICKNESS = 3.0
BALL_POD_LID_Z = (49.0, 51.0)  # lid bottom, lid top over the sensor belt (the lid rakes down ahead of it)
# Prow plan: (x, half width, top Z, upper chamfer). Straight through the shell notch, swelling to
# 49 mm across the GP2Y's mounting belt (x 111.8-119.4), sweeping in to a 36 mm nose that rakes down to the face.
# The touch hood starts ahead of the belt (x 124), so the hood itself stays under 42 mm wide.
BALL_POD_STATIONS = (
    (92.0, 17.5, 51.0, 6.0),
    (104.0, 17.5, 51.0, 6.0),
    (110.5, 24.5, 51.0, 9.0),
    (119.8, 24.5, 51.0, 9.0),
    (123.5, 17.8, 49.6, 7.0),
    (126.0, 17.8, 48.2, 7.0),
    (128.5, 16.0, 47.0, 6.5),
)
# Lid underside in XZ: level over the belt, stepping down over the lens hood.
BALL_POD_LID_UNDERSIDE = ((80.0, 49.0), (119.8, 49.0), (121.6, 46.8), (129.0, 44.9))
BALL_POD_EAR_SLOT = (111.4, 119.8, 14.6, 22.9)  # x0, x1, |y| inner, |y| outer: the sensor's belt
BALL_POD_POCKET = (BALL_POD_X[0] + 3.0, 15.5)  # pocket rear x, half-width; open front and top
BALL_POD_SCREWS_YZ = ((10.0, 42.0), (-10.0, 42.0))  # M3 into crossmember inserts, driven from the pocket

# Body placement (RP03-CAD-06). Every body-side part (shell, panels, body
# frame, electronics, audio, harness, yaw stage and head) sits BODY_SHIFT_X
# forward of the drive axle; the drivetrain, ball, chassis and keel do not
# move. This carries ~1.96 kg forward and brings the whole-robot CoM from
# x +9.4 to about +21 mm (x/h ~0.20). Body-side X values below are written as
# their pre-shift value + BODY_SHIFT_X; BODY_AXIS_X is the body/yaw centre.
BODY_SHIFT_X = 16.0
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

# Provisional audio packaging. These are requirement envelopes pending the
# RP-05/RP-06 driver, amplifier, PDM microphone and front-end selections.
SPEAKER_CENTER = (72.0 + BODY_SHIFT_X, 0.0, 99.0)
SPEAKER_CONE_DIAMETER = 44.0
SPEAKER_BASKET_DIAMETER = 50.0
SPEAKER_DEPTH = 18.0
SPEAKER_CAVITY_DEPTH = 34.0
# The GP2Y sits on the centreline in the ball pod, its face ahead of the ball
# contact, and looks forward through a window in the touch cap. RP-03
# physics.md §6 credits look-ahead from the leading (ball) contact, so a face
# ahead of it is credited and a face behind it is charged.
FRONT_RANGE_SENSOR_Y = 0.0
FRONT_RANGE_SENSOR_BOTTOM_Z = 35.0  # rests on pod rails just above the ball-screw heads
FRONT_RANGE_SENSOR_Z = 40.3  # optical axis: lens centre (STEP Z 5.3 above the seating plane)
# Sharp STEP: 29.6 wide x 11.5 tall body with a 7.2 mm-deep belt out to 44.4 mm wide x 13.5 tall
# (STEP y -3.6..3.6); lens hood 6.4 mm ahead of the body's front face. Depth is to the lens tip.
FRONT_RANGE_SENSOR_SIZE = (18.9, 29.6, 11.5)
FRONT_RANGE_SENSOR_FACE_X = 128.0  # lens tip, 0.5 mm inside the pod front face
FRONT_RANGE_BELT_X = (111.8, 119.4)  # world x of the belt (STEP y -3.6..3.6 -> lens tip - 12.4 + y)
FRONT_RANGE_BODY_FRONT_X = 122.1  # low front section (STEP y -6.5: Z 0-7.2) starts here
FRONT_RANGE_WINDOW_SIZE = (27.0, 10.5)  # visor slit in the cap: width, height (full-round ends)
FRONT_RANGE_CONNECTOR_DEPTH = 6.5
FRONT_RANGE_MAX_MM = 300.0  # GP2Y0A41SK0F rated range 40-300 mm
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
YAW_SERVO_ENVELOPE = (-10.0 + BODY_AXIS_X, 10.0 + BODY_AXIS_X, 29.0, 55.0, 99.0, 133.0)
YAW_OPENING_RADIUS = 45.0
# RP-01 actuator screen: peak yaw 378 deg/s = 63 rpm at the output. XC330-M181
# no-load speed 95 / 129 rpm at 3.7 / 5.0 V (ROBOTIS e-manual).
YAW_PEAK_OUTPUT_RPM = 63.0
YAW_SERVO_NO_LOAD_RPM = {"3.7V": 95.0, "5.0V": 129.0}

PI_CENTER = (6.0 + BODY_SHIFT_X, 0.0, 102.0)
# Pi 5 cooler-post holes (STEP PCB), from the Pi's bounding-box corner: 58 x 37 mm apart.
PI_COOLER_HOLE_A = (PI_CENTER[0] - 45.0 + 5.25, PI_CENTER[1] - 28.8 + 11.1)
DEVKIT_CENTER = (-24.0 + BODY_SHIFT_X, 44.0, 84.0)
# Battery (RP03-CAD-06; RP03-CAD-07 for the pack): low in a chassis tub under
# the deck, forward of the motors, long side across the robot. It sits under the
# deck top and drops out downward through a bottom hatch; the shell floor is
# open under it. The pack is the RP-02 working selection of 2026-09-24: a 2S1P
# of two Samsung INR18650-25R cells lying side by side with a 2S 20 A balanced
# BMS board on top. Cell and BMS sizes are datasheet/listing values, not a
# vendor STEP; the BMS thickness is unverified.
BATTERY_CELL_DIAMETER = 18.4  # 25R body max 18.33 +/- 0.07 plus sleeve
BATTERY_CELL_LENGTH = 65.0  # 25R height 64.85 +/- 0.15 mm
BATTERY_CELL_PITCH = 18.6  # 0.2 mm sleeve gap between the two cells
BATTERY_END_STRAP_T = 1.0  # nickel strap, insulation cap and solder at each cell end
BATTERY_BMS_SIZE = (20.0, 48.0, 4.5)  # 2S 20 A balanced module: 48 x 20 mm listed, thickness assumed
BATTERY_WRAP_T = 0.3  # heat-shrink sleeve under the cells and over the BMS
BATTERY_SIZE = (
    BATTERY_CELL_PITCH + BATTERY_CELL_DIAMETER + 2.0 * BATTERY_WRAP_T,
    BATTERY_CELL_LENGTH + 2.0 * BATTERY_END_STRAP_T,
    BATTERY_CELL_DIAMETER + BATTERY_BMS_SIZE[2] + 3.0 * BATTERY_WRAP_T,
)  # 37.6 x 67.0 x 23.5 mm envelope
BATTERY_TUB_FLOOR_Z = (30.5, 32.0)
BATTERY_TUB_WALL = 1.5
BATTERY_TUB_CLEARANCE = 1.5  # foam/retention gap between the pack and each tub wall
BATTERY_TUB_FRONT_X = 67.0  # front wall inner face; the pack sits against the front of the tub
BATTERY_TUB_X = (
    BATTERY_TUB_FRONT_X - BATTERY_SIZE[0] - 2.0 * BATTERY_TUB_CLEARANCE - BATTERY_TUB_WALL,
    BATTERY_TUB_FRONT_X,
)  # rear wall outer face, front wall inner face
BATTERY_TUB_HALF_Y = BATTERY_SIZE[1] / 2.0 + BATTERY_TUB_CLEARANCE + BATTERY_TUB_WALL
BATTERY_CENTER = (
    BATTERY_TUB_FRONT_X - BATTERY_TUB_CLEARANCE - BATTERY_SIZE[0] / 2.0,
    0.0,
    BATTERY_TUB_FLOOR_Z[1] + BATTERY_SIZE[2] / 2.0,
)  # X 27.9-65.5, Z 32-55.5
# Ballast (RP03-CAD-08): a mild-steel bar clamped under the deck between the
# battery tub's front wall and the front crossmember, hung from two M3
# countersunk-style screws from the deck top. It restores the register CoM to
# the physics.md 2.5 line after the lighter RP03-CAD-07 pack.
BALLAST_X = (69.5, 78.5)  # 1.0 mm off the tub front wall (X 68.5), 1.5 mm off the crossmember (X 80)
BALLAST_HALF_Y = 30.0
BALLAST_Z = (33.0, 52.0)  # top face against the deck underside (Z 52)
BALLAST_SCREW_Y = (-20.0, 20.0)
BALLAST_SCREW_X = 74.0
BALLAST_DENSITY_G_CM3 = 7.85
BALLAST_SCREW_HEAD_Z = (54.1, 56.0)  # 1.9 mm head sunk in a counterbore in the 4 mm deck
BALLAST_SCREW_THREAD_DEPTH = 8.0
BALLAST_BAR_G = (
    (BALLAST_X[1] - BALLAST_X[0]) * 2.0 * BALLAST_HALF_Y * (BALLAST_Z[1] - BALLAST_Z[0])
    - 2.0 * math.pi * 1.5**2 * BALLAST_SCREW_THREAD_DEPTH
) / 1000.0 * BALLAST_DENSITY_G_CM3
BALLAST_SCREWS_G = 2.0 * math.pi * (2.9**2 * 1.9 + 1.5**2 * (2.0 + BALLAST_SCREW_THREAD_DEPTH)) / 1000.0 * BALLAST_DENSITY_G_CM3
# Floor-contact functions live in a compact faceted keel bolted under the rear
# crossmember, so the visible tail is free to be purely cosmetic. The rear
# crossmember and keel move forward with the body's rear wall (RP03-CAD-06).
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
    (-64.0 + REAR_CHASSIS_SHIFT_X, 8.5, TCRT_OPTICAL_FACE_Z, REAR_KEEL_TOP_Z, 1.8),       # sensor flat
    (-78.0 + REAR_CHASSIS_SHIFT_X, 8.5, TCRT_OPTICAL_FACE_Z, 26.0, 1.6),
    (-83.0 + REAR_CHASSIS_SHIFT_X, 3.0, 14.0, 20.0, 0.8),                   # sharp heel
)
REAR_KEEL_SCREWS_X = (-52.5 + REAR_CHASSIS_SHIFT_X, -61.5 + REAR_CHASSIS_SHIFT_X)  # forward pair counterbores clear the shoe
REAR_KEEL_SHELL_SLOT = (-73.0 + REAR_CHASSIS_SHIFT_X, -40.0 + REAR_CHASSIS_SHIFT_X, 10.5)  # x0, x1, half-width of the floor pass-through
REAR_KEEL_GUARD_X = (TCRT_REAR_CENTER[0] - 8.0, TCRT_REAR_CENTER[0] + 7.0)
REAR_KEEL_GUARD_WIDTH = 2.5
REAR_KEEL_GUARD_HEIGHT = TCRT_OPTICAL_FACE_Z - TCRT_GUARD_BOTTOM_Z + 0.5  # 0.5 mm seated in the keel

# Cosmetic tail: a short, static, hard-surface stinger. A slate root hub on the
# rear service panel carries three telescoping ivory segments and an amber
# chisel tip. Every section repeats the body's eight-sided end profile; each
# segment starts smaller than its predecessor ends, so the joints read as
# nested sleeves, and each one sweeps further upward. Each joint is
# (x, z, section width, section height); the tail stays inside the
# spin-in-place circle already set by the ball nose and below the body top.
# Parked accessory: the geometry stays defined and checked, but is left out of
# the assembly (and the rear panel carries no tail bores) until re-enabled.
REAR_TAIL_ENABLED = False
REAR_TAIL_STYLE = "FACETED_TELESCOPING_STINGER"
REAR_TAIL_VISIBLE_COLOR = IVORY
REAR_TAIL_HUB_COLOR = SLATE_DARK
REAR_TAIL_TIP_COLOR = AMBER
REAR_TAIL_ALPHA = 1.0
REAR_TAIL_ROOT_FACE_X = -78.4 + BODY_SHIFT_X  # outer face of the root flange
REAR_TAIL_ROOT_Z = 92.0
REAR_TAIL_HUB = (-87.0 + BODY_SHIFT_X, (26.0, 22.0), (23.0, 19.5))  # hub end x, root and end section (w, h)
REAR_TAIL_JOINTS = (
    (-87.0 + BODY_SHIFT_X, REAR_TAIL_ROOT_Z, 19.0, 16.0),  # leaves the hub, 23 deg upsweep
    (-100.0 + BODY_SHIFT_X, 97.5, 15.5, 13.0),             # 37 deg
    (-110.0 + BODY_SHIFT_X, 105.0, 12.5, 10.5),            # 52 deg
    (-117.0 + BODY_SHIFT_X, 114.0, 9.5, 8.0),              # amber tip segment starts, 66 deg
)
REAR_TAIL_TIP = (-121.0 + BODY_SHIFT_X, 123.0)
REAR_TAIL_TIP_SECTION = (4.0, 2.0)  # blunt chisel, not a needle point
REAR_TAIL_SEGMENT_END_SCALE = 0.94  # each sleeve narrows slightly toward its end
REAR_TAIL_ROOT_FLANGE = (30.0, 26.0, 2.0)  # width, height, thickness on the rear panel
# Four M3 screws are driven from inside the body, through the backer, panel
# and flange, into heat-set inserts in the hub: no fastener heads show outside.
REAR_TAIL_ROOT_SCREWS = ((-8.0, 86.0), (8.0, 86.0), (-5.0, 97.5), (5.0, 97.5))
REAR_TAIL_INSERT = (2.0, 6.0)  # heat-set insert pocket radius and depth
# The keel is translucent ivory so the TCRT cartridge, cable riser and M3
# hardware inside it stay visible for packaging review.
REAR_KEEL_COLOR = IVORY
REAR_KEEL_ALPHA = 0.34

# Touch cap: an octagonal hood on compliant side arms over the pod front,
# open at the bottom and rear; the cap travels rearward onto a lid-mounted
# side-actuated tact switch. It stops at the pod seat (Z 29), just below the
# sensor window: the lower skirt over the ball housing was cut 2026-09-24
# (RP03-CAD-04), so floor-level objects below the GP2Y beam are no longer
# caught by contact and meet the purchased ball housing first.
TACTILE_NOSE_TRAVEL = 3.0
TACTILE_CAP_INNER_X = BALL_POD_X[1] + TACTILE_NOSE_TRAVEL
TACTILE_CAP_WALL = 2.0
TACTILE_NOSE_FACE_X = TACTILE_CAP_INNER_X + TACTILE_CAP_WALL
TACTILE_CAP_ARM_X0 = 124.0
TACTILE_CAP_CLEARANCE = 0.5  # to the pod sides; ~0.55 normal on the chamfers
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
    ("BODY_SHELL_AND_PANELS", 290.4, (4.0 + BODY_SHIFT_X, 0.0, 96.0), "Layout 02 CAD estimate; +15 g for the internal panel frames (+15.6 cm3 net printed volume, near-solid 2.4 mm walls); -27.2 g for the -22.7 cm3 of shell floor opened over the motors, battery hatch and pod tongue (RP03-CAD-05/06) at ~1.2 g/cm3; +2.6 g for the ~0.9 cm2 x 2.4 mm of shell floor returned when the battery opening shrank to the 2S1P pack tub (RP03-CAD-07)"),
    ("BODY_PRIMARY_FRAME", 335.0, (4.0 + BODY_SHIFT_X, 0.0, 94.0), "Layout 02 CAD estimate incl. mounts"),
    ("CHASSIS_PRIMARY_FRAME", 172.1, (19.8, 0.0, 47.4), "front crossmember moved 13 mm forward to X 80-92, rails and deck extended to X 92 (+2.1 g, +3.3 g), battery-tub front wall added (+1.3 g); before that CAD estimate; 219.8 g before RP03-CAD-05/06, then -53.3 g for the net -93.3 cm3 printed volume at ~45% effective PETG density: axle crossmember and square carriers/gussets removed, flange bosses and gearbox cheeks added, rails split and shortened to X -46, deck opened over the motors and battery, rear crossmember moved 16 mm forward, 11.2 cm3 battery tub added; -1.2 g for the -2.1 cm3 smaller battery tub (RP03-CAD-07)"),
    ("WHEEL_L", 90.0, WHEEL_CENTER_L, "custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately"),
    ("WHEEL_R", 90.0, WHEEL_CENTER_R, "custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately"),
    ("AXLE_BEARINGS_AND_STUB_SHAFTS", 65.4, (0.0, 0.0, AXLE_Z), "E: four 608ZZ at ~12 g (not in the register before 2026-09-24) + two 8 mm steel stub shafts at ~8.7 g; symmetric about the centre plane"),
    ("MOTOR_L", 110.0, (0.0, 52.0, AXLE_Z), "vendor"),
    ("MOTOR_R", 110.0, (0.0, -52.0, AXLE_Z), "vendor"),
    ("BALL_TRANSFER", 16.5, (BALL_CONTACT[0], 0.0, 14.0), "vendor"),
    ("BALLAST_STEEL_BAR", round(BALLAST_BAR_G + BALLAST_SCREWS_G, 1), (sum(BALLAST_X) / 2.0, 0.0, sum(BALLAST_Z) / 2.0), "E: mild-steel bar 9 x 60 x 19 mm at 7.85 g/cm3 (less two M3 tapped holes) + two M3 screws; sized so the register CoM clears the physics.md 2.5 line after the 110 g pack (RP03-CAD-08)"),
    ("BATTERY", 110.0, BATTERY_CENTER, "E: 2 x Samsung INR18650-25R (45 g max each) + 2S 20 A balanced BMS (~8 g) + sleeve, straps and leads (~12 g); working selection, no purchase or measured mass; was a 280 g RP-02 placeholder"),
    ("RASPBERRY_PI5_AND_COOLER", 76.0, PI_CENTER, "vendor + estimate"),
    ("CONTROL_POWER_SENSORS", 121.5, (6.0 + BODY_SHIFT_X, 0.0, 80.0), "estimate; one rear TCRT channel; GP2Y (3.5 g) moved to BALL_NOSE_POD_SENSOR_CAP"),
    ("BALL_NOSE_POD_SENSOR_CAP", 15.9, (110.5, 0.0, 41.2), "CAD volume: raked prow pod + lid 11.8 cm3 (X 92-128.5) and touch hood 1.8 cm3 (2026-09-24 prow rework) at ~45% effective PETG density (6.8 + 1.0 g); 5 M3 screws + 2 heat-set inserts 4.6 g; GP2Y0A41SK0F 3.5 g E"),
    ("BODY_AUDIO", 90.0, (48.0 + BODY_SHIFT_X, 0.0, 102.0), "speaker, amplifier and four microphones; CAD estimate"),
    ("HARNESS_AND_FASTENERS", 95.0, (4.0 + BODY_SHIFT_X, 0.0, 88.0), "estimate"),
    ("BODY_YAW_STAGE", 88.0, (BODY_AXIS_X, 13.5, 134.3), "E: 50 g thin-section bearing placeholder + 23 g XC330-M181 + 2 x 6 g 1:1 spur gears + 2 g clamp ring + 1 g coupling shaft; no SKU"),
    ("REAR_SKID_KEEL", 12.0, (-55.9 + REAR_CHASSIS_SHIFT_X, 0.0, 20.4), "CAD volume: 15.4 cm3 keel body at ~45% effective PETG density, 12x10 mm shoe, guards, 4 M3 screws"),
]
if REAR_TAIL_ENABLED:
    MASS_ROWS.append(("REAR_TAIL_STINGER", 10.0, (-93.5 + BODY_SHIFT_X, 0.0, 95.9), "CAD volume: 10.4 cm3 printed segments/hub/flange + 2.2 cm3 backer at ~45% effective PETG density, 4 M3 screws + heat-set inserts"))


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


def _purchased_step(filename, label, rotations=()):
    """Import a vendor STEP from the purchased folder and apply (axis, deg) turns."""
    part = import_step(str(PURCHASED / filename))
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


def _beam_xz(x0, z0, x1, z1, width, thickness, label, color):
    """Rectangular structural member centred between two XZ datum points."""
    dx = x1 - x0
    dz = z1 - z0
    length = math.hypot(dx, dz)
    angle = math.degrees(math.atan2(-dz, dx))
    beam = Box(length, width, thickness).rotate(Axis.Y, angle)
    beam = beam.moved(Location(((x0 + x1) / 2.0, 0.0, (z0 + z1) / 2.0)))
    return _paint(beam, label, color, 1.0)


def _vertical_bore(radius, z0, z1, x, y):
    return Cylinder(radius, z1 - z0).moved(Location((x, y, z0)))


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
    pod = pod - _block(pocket_x0, FRONT_RANGE_BODY_FRONT_X + 0.2, -pocket_hw, pocket_hw, floor_z, BALL_POD_LID_Z[1] + 1.0)
    # Ahead of the sensor body only the lens hood and the tact switch need room.
    pod = pod - _block(FRONT_RANGE_BODY_FRONT_X, x1 + 1.0, -14.0, 14.0, floor_z, BALL_POD_LID_Z[1] + 1.0)
    # The sensor's belt (44 mm across, x 111.8-119.4) sits in side slots under the lid.
    ex0, ex1, ey0, ey1 = BALL_POD_EAR_SLOT
    for sign in (1.0, -1.0):
        pod = pod - _block(ex0, ex1, *sorted((sign * ey0, sign * ey1)), FRONT_RANGE_SENSOR_BOTTOM_Z, BALL_POD_LID_Z[0])
    # Two rails carry the GP2Y body just above the ball-screw heads.
    sensor_x0 = FRONT_RANGE_SENSOR_FACE_X - FRONT_RANGE_SENSOR_SIZE[0]
    for sign in (1.0, -1.0):
        pod = pod + _block(sensor_x0, FRONT_RANGE_BODY_FRONT_X - 0.6, *sorted((sign * 10.5, sign * pocket_hw)), floor_z, FRONT_RANGE_SENSOR_BOTTOM_Z)
    for x, y in ball_screw_points():
        pod = pod - _z_cylinder(1.65, z0 - 1.0, floor_z + 1.0, x, y)
    for y, z in BALL_POD_SCREWS_YZ:
        pod = pod - _axial_bore_x(1.65, x0 - 1.0, pocket_x0 + 1.0, y, z)
    return _paint(pod, "BALL_POD_PRINTED_SEAT", SLATE, 1.0)


def ball_pod_lid():
    lid = _ball_pod_solid() - _lid_below()
    return _paint(lid, "BALL_POD_SENSOR_LID", SLATE, 1.0)


def _tactile_switch_block(grow=0.0):
    # Side-actuated micro tact switch (~6 x 6 x 3.5 mm) on the pod floor, off the sensor's lens line.
    x1 = 128.1
    z0 = BALL_POD_Z0 + BALL_POD_SEAT_THICKNESS
    return _block(x1 - 6.0 - grow, x1 + grow, 7.0 - grow, 13.0 + grow, z0, z0 + 3.5 + grow)


def ball_pod_hardware():
    floor_z = BALL_POD_Z0 + BALL_POD_SEAT_THICKNESS
    parts = []
    for index, (x, y) in enumerate(ball_screw_points(), start=1):
        parts.append(_paint(_z_cylinder(2.8, floor_z, floor_z + 1.8, x, y), f"BALL_M3_HEAD_{index}", STEEL, 1.0))
        parts.append(_paint(_z_cylinder(1.35, BALL_POD_Z0 - 3.0, floor_z, x, y), f"BALL_M3_SHANK_{index}", STEEL, 1.0))
    pocket_x0 = BALL_POD_POCKET[0]
    for index, (y, z) in enumerate(BALL_POD_SCREWS_YZ, start=1):
        parts.append(_cylinder(2.8, 1.8, (pocket_x0 + 0.9, y, z), f"BALL_POD_M3_HEAD_{index}", STEEL, 1.0, "x"))
        parts.append(_cylinder(1.35, 9.0, (pocket_x0 - 4.5, y, z), f"BALL_POD_M3_SHANK_{index}", STEEL, 1.0, "x"))
        parts.append(_cylinder(2.0, 6.0, (BALL_POD_X[0] - 3.0, y, z), f"BALL_POD_HEATSET_INSERT_{index}", BRONZE, 1.0, "x"))
    return Compound(label="BALL_POD_HARDWARE", children=parts)


def _tail_section(point, direction, width, height):
    """Eight-sided tail section echoing the body end profile, narrower on top."""
    x, z = point
    dx, dz = direction
    plane = Plane(origin=(x, 0.0, z), x_dir=(0.0, -1.0, 0.0), z_dir=(dx, 0.0, dz))
    lower = width / 2.0
    upper = 0.78 * lower
    lower_corner = 0.22 * min(width, height)
    upper_corner = 0.30 * min(width, height)
    h = height / 2.0
    points = [
        (-lower + lower_corner, -h),
        (lower - lower_corner, -h),
        (lower, -h + lower_corner),
        (upper, h - upper_corner),
        (upper - upper_corner, h),
        (-upper + upper_corner, h),
        (-upper, h - upper_corner),
        (-lower, -h + lower_corner),
    ]
    return plane * Polygon(*points, align=None)


def _unit_xz(a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dz)
    return dx / length, dz / length


def _tail_mitre_directions():
    """Per-joint section normals: -X at the hub face, bisectors inside, axis at the tip."""
    points = [joint[:2] for joint in REAR_TAIL_JOINTS] + [REAR_TAIL_TIP]
    segments = [_unit_xz(points[i], points[i + 1]) for i in range(len(points) - 1)]
    mitres = [(-1.0, 0.0)]  # first section lies flat on the hub end face
    for before, after in zip(segments, segments[1:]):
        bx, bz = before[0] + after[0], before[1] + after[1]
        length = math.hypot(bx, bz)
        mitres.append((bx / length, bz / length))
    return segments, mitres


def rear_tail_segment_sizes():
    """(start width, end width) of each segment, root to tip."""
    joints = REAR_TAIL_JOINTS
    sizes = [(w, w * REAR_TAIL_SEGMENT_END_SCALE) for _x, _z, w, _h in joints[:-1]]
    sizes.append((joints[-1][2], REAR_TAIL_TIP_SECTION[0]))
    return sizes


def rear_tail_segments():
    """Telescoping mitred sleeves plus the amber chisel tip."""
    segments = []
    joints = REAR_TAIL_JOINTS
    directions, mitres = _tail_mitre_directions()
    for index, (x0, z0, w0, h0) in enumerate(joints):
        if index + 1 < len(joints):
            x1, z1 = joints[index + 1][:2]
            end = ((x1, z1), mitres[index + 1], w0 * REAR_TAIL_SEGMENT_END_SCALE, h0 * REAR_TAIL_SEGMENT_END_SCALE)
            label, color = f"REAR_TAIL_SEGMENT_{index + 1:02}", REAR_TAIL_VISIBLE_COLOR
        else:
            end = (REAR_TAIL_TIP, directions[-1], *REAR_TAIL_TIP_SECTION)
            label, color = "REAR_TAIL_CHISEL_TIP", REAR_TAIL_TIP_COLOR
        segment = loft([_tail_section((x0, z0), mitres[index], w0, h0), _tail_section(*end)], ruled=True)
        segments.append(_paint(segment, label, color, REAR_TAIL_ALPHA))
    return Compound(label="REAR_TAIL_SEGMENTS", children=segments)


def rear_tail_root_screw_points():
    return list(REAR_TAIL_ROOT_SCREWS)


def rear_tail_root_mount():
    """Slate hub on a slim flange, clamped from inside the body through an inner backer."""
    width, height, thickness = REAR_TAIL_ROOT_FLANGE
    zc = REAR_TAIL_ROOT_Z
    panel_face_x = BODY_X_REAR - SHELL_THICKNESS
    flange = loft(
        [
            _tail_section((panel_face_x, zc), (-1.0, 0.0), width, height),
            _tail_section((REAR_TAIL_ROOT_FACE_X, zc), (-1.0, 0.0), width, height),
        ],
        ruled=True,
    )
    backer = _panel_solid(BODY_X_REAR, BODY_X_REAR + SHELL_THICKNESS, width + 4.0, width, zc - height / 2.0 - 2.0, zc + height / 2.0 + 2.0, 4.0, 4.0)
    hub_x1, hub_root, hub_end = REAR_TAIL_HUB
    hub = loft(
        [
            _tail_section((REAR_TAIL_ROOT_FACE_X, zc), (-1.0, 0.0), *hub_root),
            _tail_section((hub_x1, zc), (-1.0, 0.0), *hub_end),
        ],
        ruled=True,
    )
    insert_radius, insert_depth = REAR_TAIL_INSERT
    screws = []
    for index, (y, z) in enumerate(rear_tail_root_screw_points(), start=1):
        flange = flange - _axial_bore_x(1.65, REAR_TAIL_ROOT_FACE_X - 1.0, panel_face_x + 1.0, y, z)
        hub = hub - _axial_bore_x(insert_radius, REAR_TAIL_ROOT_FACE_X - insert_depth, REAR_TAIL_ROOT_FACE_X + 1.0, y, z)
        backer = backer - _axial_bore_x(1.65, BODY_X_REAR - 1.0, BODY_X_REAR + 4.0, y, z)
        backer_inner_x = BODY_X_REAR + SHELL_THICKNESS
        head = _cylinder(2.8, 1.8, (backer_inner_x + 0.9, y, z), f"REAR_TAIL_ROOT_M3_HEAD_{index}", STEEL, 1.0, "x")
        shank_x1 = REAR_TAIL_ROOT_FACE_X - insert_depth + 1.0
        shank = _cylinder(1.35, backer_inner_x - shank_x1, ((backer_inner_x + shank_x1) / 2.0, y, z), f"REAR_TAIL_ROOT_M3_SHANK_{index}", STEEL, 1.0, "x")
        screws.extend([head, shank])
    return Compound(
        label="REAR_TAIL_ROOT_MOUNT",
        children=[
            _paint(hub, "REAR_TAIL_ROOT_HUB", REAR_TAIL_HUB_COLOR, 1.0),
            _paint(flange, "REAR_TAIL_ROOT_FLANGE", REAR_TAIL_HUB_COLOR, 1.0),
            _paint(backer, "REAR_TAIL_ROOT_INNER_BACKER", SLATE, 1.0),
            *screws,
        ],
    )


def rear_skid_tcrt_keel():
    """Compact faceted keel under the rear crossmember: skid shoe + TCRT."""
    tx, ty, tz = TCRT_REAR_CENTER
    keel = loft(
        [_nose_profile(x, half_width, z0, z1, chamfer) for x, half_width, z0, z1, chamfer in REAR_KEEL_STATIONS],
        ruled=True,
    )
    px, py, pz = TCRT_PACKAGE_SIZE
    sensor_pocket = _block(tx - 6.0, tx + 6.0, -5.1, 5.1, TCRT_OPTICAL_FACE_Z - 1.0, TCRT_OPTICAL_FACE_Z + 10.8)  # 10.5 mm real part incl. leads
    connector_channel = _block(tx + 4.0, tx + 17.0, -3.5, 3.5, tz + 2.0, tz + 7.0)
    cable_x = tx + 13.0
    cable_bore = _vertical_bore(3.0, tz + 2.0, REAR_KEEL_TOP_Z + 1.0, cable_x, 0.0)
    screw_bores = []
    screws = []
    screw_points = [(x, sign * 5.5) for x in REAR_KEEL_SCREWS_X for sign in (1.0, -1.0)]
    for index, (x, y) in enumerate(screw_points, start=1):
        screw_bores.append(_vertical_bore(1.7, 0.0, REAR_KEEL_TOP_Z + 1.0, x, y))
        forward_pair = x > -54.0 + REAR_CHASSIS_SHIFT_X
        screw_bores.append(_vertical_bore(2.9, 0.0, SKID_SHOE_BOTTOM_Z + 2.5 + 3.0 if forward_pair else 12.0, x, y))
        head_z0 = SKID_SHOE_BOTTOM_Z + 2.5 + 1.0 if forward_pair else 10.0
        screws.append(_paint(Cylinder(2.8, 1.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, head_z0))), f"REAR_KEEL_M3_HEAD_{index}", STEEL, 1.0))
        screws.append(_paint(Cylinder(1.35, 44.0 - head_z0 - 1.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, head_z0 + 1.8))), f"REAR_KEEL_M3_SHANK_{index}", STEEL, 1.0))
    keel = _paint(
        keel - [sensor_pocket, connector_channel, cable_bore, *screw_bores],
        "REAR_KEEL_FACETED_BODY",
        REAR_KEEL_COLOR,
        REAR_KEEL_ALPHA,
    )

    # Replaceable wear shoe, fully backed by the flat keel belly, just ahead
    # of the recessed forward keel screws.
    sx, sy, sz = SKID_SHOE_SIZE
    x0 = SKID_PAD_CENTER[0] - sx / 2.0
    x1 = SKID_PAD_CENTER[0] + sx / 2.0
    y0 = -sy / 2.0
    y1 = sy / 2.0
    c = 2.5
    shoe_face = Plane.XY * Polygon(
        (x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c),
        (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c),
        align=None,
    )
    shoe = extrude(shoe_face.moved(Location((0.0, 0.0, SKID_SHOE_BOTTOM_Z))), amount=sz)
    shoe = _paint(shoe, "REAR_KEEL_REPLACEABLE_WEAR_SHOE", IVORY, 1.0)

    # Replaceable guard lips seat 0.5 mm into the flat sensor belly along
    # their full length, below the optical face and above the shoe.
    gx0, gx1 = REAR_KEEL_GUARD_X
    guards = [
        _box(
            gx1 - gx0,
            REAR_KEEL_GUARD_WIDTH,
            REAR_KEEL_GUARD_HEIGHT,
            ((gx0 + gx1) / 2.0, sign * 5.6, TCRT_GUARD_BOTTOM_Z + REAR_KEEL_GUARD_HEIGHT / 2.0),
            f"REAR_KEEL_REPLACEABLE_GUARD_{side}",
            IVORY,
        )
        for sign, side in ((1.0, "L"), (-1.0, "R"))
    ]

    cartridge = _tcrt_ski_cartridge("REAR", TCRT_REAR_CENTER)
    cable = _box(4.5, 4.5, 49.0 - (tz + 2.5), (cable_x, 0.0, (tz + 2.5 + 49.0) / 2.0), "TCRT_REAR_CABLE_RISER", "#79C4CB", 0.9)
    floor_interface = Compound(label="REAR_KEEL_FLOOR_INTERFACE", children=[shoe, *guards])
    hardware = Compound(label="REAR_KEEL_M3_HARDWARE", children=screws)
    return Compound(
        label="REAR_SKID_TCRT_KEEL",
        children=[keel, floor_interface, cartridge, cable, hardware],
    )


def rear_tail():
    return Compound(label="REAR_TAIL_STINGER", children=[rear_tail_segments(), rear_tail_root_mount()])


def rear_skid_tcrt_module():
    """Selectable rear group: the under-body skid/TCRT keel, plus the stinger tail when enabled."""
    children = [rear_tail()] if REAR_TAIL_ENABLED else []
    return Compound(label="REAR_SKID_TCRT_MODULE", children=[*children, rear_skid_tcrt_keel()])


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
    """Raked touch hood over the prow front: pod seat up to the lid, with a visor-slit window."""
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
    cap = _paint(cap, "BALL_NOSE_TOUCH_CAP", IVORY, TACTILE_CAP_ALPHA)
    # Compliant anchors tie each side arm to the pod; they are the cap's only support.
    hw_rear = _station_at(arm_x0)[1]  # constant from x 123.5 to 126, so the anchors sit flush
    flexures = [
        _paint(
            _block(arm_x0, BALL_POD_STATIONS[-2][0], *sorted((sign * hw_rear, sign * (hw_rear + gap))), 33.5, 40.5),
            f"BALL_NOSE_FLEXURE_{side}",
            FRAME_BLUE,
            1.0,
        )
        for sign, side in ((1.0, "L"), (-1.0, "R"))
    ]
    switch = _paint(_tactile_switch_block(), "BALL_NOSE_TACT_SWITCH", "#7A4A21", 0.92)
    sb = _tactile_switch_block().bounding_box()
    plunger_x0 = sb.max.X
    plunger = _cylinder(1.0, inner_x - plunger_x0, ((plunger_x0 + inner_x) / 2.0, sb.center().Y, sb.center().Z), "BALL_NOSE_SWITCH_PLUNGER", STEEL, 1.0, "x")
    travel = _paint(
        extrude(_pod_face(front[0], *front[1:], grow=gap), amount=inner_x - front[0]),
        "BALL_NOSE_3MM_TRAVEL_RESERVE",
        "#D95FC5",
        0.14,
    )
    travel = travel & _block(BALL_POD_X[1], inner_x + 1.0, -60.0, 60.0, BALL_POD_Z0 - 2.0, 80.0)
    return Compound(label="BALL_NOSE_CONCEALED_CONTACT_MODULE", children=[cap, *flexures, switch, plunger, travel])


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
    # The coaxial motors hang below the floor plane (can bottom Z 26.6); a
    # slot across the axle joins the two wheel wells so the body lowers over
    # them. The battery tub's bottom hatch shows through its own opening.
    motor_slot = _block(-MOTOR_RELIEF_HALF_X, MOTOR_RELIEF_HALF_X, -MOTOR_FACE_Y - 1.0, MOTOR_FACE_Y + 1.0, *floor_z)
    battery_opening = _block(
        BATTERY_TUB_X[0] - 1.0, BATTERY_TUB_X[1] + BATTERY_TUB_WALL + 1.0, -BATTERY_TUB_HALF_Y - 1.0, BATTERY_TUB_HALF_Y + 1.0, *floor_z
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
        for y, z in (*REAR_PANEL_FASTENERS, *(rear_tail_root_screw_points() if REAR_TAIL_ENABLED else ()))
    ]
    rear = _paint(
        rear_raw - rear_bores,
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
    return Compound(label="BODY_PANELS", children=[front, rear, top_badge, *wheel_arches])


def panel_mount_hardware():
    """Internal panel frames with fused bosses, and front-access M3 screws.

    Each frame sits behind the shell end wall, laps PANEL_FRAME_OUTSET past
    the panel outline and reaches PANEL_FRAME_FLANGE inside it. Its bosses
    stand forward through the shell opening to the panel's inner face.
    """
    speaker_keep_out = _cylinder(
        SPEAKER_BASKET_DIAMETER / 2.0 + 2.0,
        SPEAKER_CAVITY_DEPTH,
        (SPEAKER_CENTER[0] - 8.0, SPEAKER_CENTER[1], SPEAKER_CENTER[2]),
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
    bms = _box(*BATTERY_BMS_SIZE, (bx, by, bms_z0 + BATTERY_BMS_SIZE[2] / 2.0), "BATTERY_BMS_2S_20A_BALANCED", "#1E6B45", 1.0)
    return Compound(label="BATTERY_2S1P_18650_PACK", children=[*cells, *straps, bms])


def ballast_bar():
    """Steel bar under the deck, ahead of the battery tub (RP03-CAD-08)."""
    bar = _block(*BALLAST_X, -BALLAST_HALF_Y, BALLAST_HALF_Y, *BALLAST_Z)
    for y in BALLAST_SCREW_Y:
        bar = bar - _z_cylinder(1.5, BALLAST_Z[1] - BALLAST_SCREW_THREAD_DEPTH, BALLAST_Z[1] + 0.5, BALLAST_SCREW_X, y)
    parts = [_paint(bar, "BALLAST_STEEL_BAR", STEEL, 1.0)]
    for tag, y in zip(("L", "R"), BALLAST_SCREW_Y):
        parts.append(_paint(_z_cylinder(2.9, *BALLAST_SCREW_HEAD_Z, BALLAST_SCREW_X, y), f"BALLAST_M3_HEAD_{tag}", STEEL, 1.0))
        parts.append(_paint(_z_cylinder(1.5, BALLAST_Z[1] - BALLAST_SCREW_THREAD_DEPTH, BALLAST_SCREW_HEAD_Z[0], BALLAST_SCREW_X, y), f"BALLAST_M3_SHANK_{tag}", STEEL, 1.0))
    return Compound(label="BALLAST_BAR", children=parts)


def battery_tub():
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
    hatch = _paint(_block(x0, x1, -hw, hw, fz0, fz1), "BATTERY_TUB_BOTTOM_HATCH", SLATE, 1.0)
    walls = _block(x0, x0 + w, -hw, hw, fz1, top) + _block(x1, x1 + w, -hw, hw, fz1, top)
    for sign in (1.0, -1.0):
        walls = walls + _block(x0 + w, x1 + w, *sorted((sign * (hw - w), sign * hw)), fz1, top)
    return Compound(label="BATTERY_TUB", children=[hatch, _paint(walls, "BATTERY_TUB_WALLS", FRAME_BLUE, 1.0)])


def chassis_frame():
    # The deck, rails and front crossmember stop inside the shell's front
    # wall; only the ball pod's tongue passes the front face. The deck is two
    # plates either side of a relief over the coaxial motors (can tops at
    # Z 57.4 stand above the deck plane), and the front plate is open over
    # the battery, which sits flush with the deck top.
    relief = MOTOR_RELIEF_HALF_X
    deck_x0, deck_x1 = -41.0, CHASSIS_RAIL_X1
    deck = _block(deck_x0, -relief, -56.0, 56.0, DECK_Z - 2.0, DECK_Z + 2.0) + _block(
        relief, deck_x1, -56.0, 56.0, DECK_Z - 2.0, DECK_Z + 2.0
    )
    bx, by, _bz = BATTERY_CENTER
    bdx, bdy, _bdz = BATTERY_SIZE
    deck = deck - _block(bx - bdx / 2.0 - 0.5, bx + bdx / 2.0 + 0.5, by - bdy / 2.0 - 0.5, by + bdy / 2.0 + 0.5, DECK_Z - 3.0, DECK_Z + 3.0)
    for x, y in BODY_MOUNT_POINTS:
        deck = deck - _z_cylinder(BODY_MOUNT_CLEARANCE_RADIUS, DECK_Z - 3.0, DECK_Z + 3.0, x, y)
    for x, y in BODY_LOCATING_POINTS:
        deck = deck - _z_cylinder(2.05, DECK_Z - 3.0, DECK_Z + 3.0, x, y)
    for y in BALLAST_SCREW_Y:
        deck = deck - _z_cylinder(1.7, DECK_Z - 3.0, DECK_Z + 3.0, BALLAST_SCREW_X, y)
        deck = deck - _z_cylinder(3.2, BALLAST_SCREW_HEAD_Z[0] - 0.1, DECK_Z + 3.0, BALLAST_SCREW_X, y)
    deck = _paint(deck, "CHASSIS_DECK_WITH_BODY_INTERFACE", FRAME_BLUE, 1.0)
    rail_parts = []
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        # Each rail stops short of the gearbox; cheek plates carry it round
        # to the axle flange on both sides of the motor.
        for x0, x1, part in ((CHASSIS_RAIL_X0, -relief, "REAR"), (relief, CHASSIS_RAIL_X1, "FRONT")):
            rail_parts.append(_paint(
                _block(x0, x1, *sorted((sign * (CHASSIS_RAIL_Y - 4.0), sign * (CHASSIS_RAIL_Y + 4.0))), 35.0, 53.0),
                f"CHASSIS_RAIL_{side}_{part}",
                SLATE,
                1.0,
            ))
    parts = [
        *rail_parts,
        _paint(
            _block(*FRONT_CROSSMEMBER_X, -58.0, 58.0, 35.0, 51.0)
            - [_axial_bore_x(2.0, BALL_POD_X[0] - 6.0, BALL_POD_X[0] + 1.0, y, z) for y, z in BALL_POD_SCREWS_YZ],
            "FRONT_CROSSMEMBER",
            FRAME_BLUE,
            1.0,
        ),
        _paint(
            Box(16.0, 116.0, 14.0).moved(Location((SKID_ROOT_DATUM[0], 0.0, 41.0)))
            - _vertical_bore(3.0, 33.0, 49.0, TCRT_REAR_CENTER[0] + 13.0, 0.0),
            "REAR_SKID_CROSSMEMBER",
            FRAME_BLUE,
            1.0,
        ),
        deck,
        battery_tub(),
        ballast_bar(),
    ]

    # Axle stack (RP03-CAD-05). The wheel centres stay at the frozen 170 mm
    # track. Each gearmotor bolts its output face to a flange; the flange's
    # round boss carries the 608 pair and reaches into the dished wheel's
    # pocket without touching it. Cheek plates tie the flange to both halves
    # of the rail, clear of the gearbox.
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        fy0, fy1 = AXLE_FLANGE_Y
        flange = _block(-AXLE_FLANGE_HALF_X, AXLE_FLANGE_HALF_X, *sorted((sign * fy0, sign * fy1)), *AXLE_FLANGE_Z)
        boss_length = AXLE_BOSS_END_Y - fy1
        boss = _cylinder(AXLE_BOSS_RADIUS, boss_length, (0.0, sign * (fy1 + boss_length / 2.0), AXLE_Z), "BOSS", FRAME_BLUE, 1.0, "y")
        bore = _axial_bore_y(AXLE_BORE_RADIUS, sign * (fy0 - 1.0), sign * (AXLE_BOSS_END_Y + 1.0), 0.0, AXLE_Z)
        parts.append(_paint(flange + boss - bore, f"AXLE_MOTOR_FLANGE_BEARING_BOSS_{side}", FRAME_BLUE, 1.0))
        for x_sign in (1.0, -1.0):
            cheek = _block(
                *sorted((x_sign * AXLE_CHEEK_X[0], x_sign * AXLE_CHEEK_X[1])),
                *sorted((sign * AXLE_CHEEK_Y[0], sign * AXLE_CHEEK_Y[1])),
                35.0,
                53.0,
            )
            parts.append(_paint(cheek, f"AXLE_CHEEK_{side}_{'FRONT' if x_sign > 0 else 'REAR'}", SLATE, 1.0))

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
        pad = pad - _vertical_bore(
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
        locator = locator - _vertical_bore(2.05, 55.0, 62.0, x, y)
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


def wheel_assembly(side: str):
    """Dished Ø84 x 24 wheel on an 8 mm stub shaft (RP03-CAD-05).

    The inner face is pocketed so the stationary bearing boss sits inside
    the wheel's envelope without touching it; the web carries the stub.
    """
    sign = 1.0 if side == "L" else -1.0
    yc = sign * TRACK / 2.0
    outer_face = TRACK / 2.0 + WHEEL_WIDTH / 2.0
    tyre = _cylinder(WHEEL_OD / 2.0, WHEEL_WIDTH, (0.0, yc, AXLE_Z), "TYRE", RUBBER, 1.0, "y") - _cylinder(
        WHEEL_OD / 2.0 - 5.0, WHEEL_WIDTH + 2.0, (0.0, yc, AXLE_Z), "TYRE_BORE", RUBBER, 1.0, "y"
    )
    rim = _cylinder(WHEEL_OD / 2.0 - 5.0, WHEEL_WIDTH, (0.0, yc, AXLE_Z), "RIM", FRAME_BLUE, 1.0, "y")
    pocket = _axial_bore_y(WHEEL_POCKET_RADIUS, sign * (WHEEL_INNER_FACE_Y - 1.0), sign * WHEEL_POCKET_FLOOR_Y, 0.0, AXLE_Z)
    hub_bore = _axial_bore_y(WHEEL_HUB_BORE_RADIUS, sign * (WHEEL_POCKET_FLOOR_Y - 1.0), sign * STUB_SHAFT_Y[1], 0.0, AXLE_Z)
    rim = rim - [pocket, hub_bore]
    # Flush radial index inlay on the outer face so wheel rotation reads in review.
    face_y = sorted((sign * (outer_face - WHEEL_INDEX_DEPTH), sign * outer_face))
    index = _block(-WHEEL_INDEX_WIDTH / 2.0, WHEEL_INDEX_WIDTH / 2.0, *face_y, AXLE_Z + WHEEL_INDEX_R[0], AXLE_Z + WHEEL_INDEX_R[1])
    rim = rim - index
    sy0, sy1 = STUB_SHAFT_Y
    stub = _cylinder(STUB_SHAFT_RADIUS, sy1 - sy0, (0.0, sign * (sy0 + sy1) / 2.0, AXLE_Z), "STUB", STEEL, 1.0, "y")
    shaft_end = MOTOR_FACE_Y + MOTOR_SHAFT_LENGTH
    stub = stub - _axial_bore_y(MOTOR_SHAFT_RADIUS, sign * (sy0 - 1.0), sign * (shaft_end + 0.5), 0.0, AXLE_Z)
    return Compound(label=f"WHEEL_{side}", children=[
        _paint(tyre, f"WHEEL_{side}_TYRE", RUBBER, 1.0),
        _paint(rim, f"WHEEL_{side}_DISHED_RIM_AND_WEB", FRAME_BLUE, 1.0),
        _paint(stub, f"WHEEL_{side}_STUB_SHAFT_8MM", STEEL, 1.0),
        _paint(index, f"WHEEL_{side}_SPIN_INDEX_INLAY", AMBER, 1.0),
    ])


def motor_envelope(side: str):
    sign = 1.0 if side == "L" else -1.0
    face_y = sign * MOTOR_FACE_Y
    gearbox = _cylinder(12.5, 21.0, (0.0, face_y - sign * 10.5, AXLE_Z), f"MOTOR_{side}_GEARBOX", BRONZE, 1.0, "y")
    can = _cylinder(15.4, 32.0, (0.0, face_y - sign * (21.0 + 16.0), AXLE_Z), f"MOTOR_{side}_CAN", "#A8693D", 1.0, "y")
    encoder = _cylinder(14.0, 12.0, (0.0, face_y - sign * (21.0 + 32.0 + 6.0), AXLE_Z), f"MOTOR_{side}_ENCODER", SLATE_DARK, 1.0, "y")
    shaft = _cylinder(
        MOTOR_SHAFT_RADIUS, MOTOR_SHAFT_LENGTH, (0.0, face_y + sign * MOTOR_SHAFT_LENGTH / 2.0, AXLE_Z),
        f"MOTOR_{side}_OUTPUT_SHAFT", STEEL, 1.0, "y",
    )
    # Encoder leads leave the rear end; the reserve sits over the encoder,
    # behind the axle, in the deck's motor relief.
    pigtail = _paint(
        _block(-13.0, -1.0, *sorted((sign * 6.0, sign * 18.0)), 56.5, 62.5),
        f"MOTOR_{side}_PIGTAIL_RESERVE",
        "#EF8A3D",
        0.34,
    )
    return Compound(label=f"MOTOR_{side}", children=[gearbox, can, encoder, shaft, pigtail])


def bearing_pair(side: str):
    source = import_step(str(PURCHASED / "bearing_608zz.step"))
    source = source.rotate(Axis.X, 90.0)
    sign = 1.0 if side == "L" else -1.0
    children = []
    for index, y_abs in enumerate(BEARING_608_Y, start=1):
        bearing = _center_at(source, (0.0, sign * y_abs, AXLE_Z))
        bearing.label = f"BEARING_608ZZ_{side}_{index}"
        children.append(bearing)
    return Compound(label=f"BEARING_PAIR_{side}", children=children)


def ball_transfer():
    """Pololu 1" ball caster (2691) from its STEP, ball contact on BALL_CONTACT."""
    part = import_step(str(PURCHASED / BALL_CASTER_STEP))
    part = part.moved(Location((BALL_CONTACT[0], BALL_CONTACT[1], BALL_CONTACT[2])))
    # STEP export order: ball, base (flange), shell (housing), three rollers. Flatten after the
    # move so every solid carries its world placement.
    ball, base, shell, *rollers = list(part.solids())
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
    # DevKitC: -90 deg about Z puts the USB end at the rear (-X); board bottom
    # sits on the old envelope floor (Z 78).
    devkit = _purchased_step("ESP32-S3-WROOM-1_devkit_2xUSBC_c.step", "C3_ESP32_S3_DEVKITC_STEP", [(Axis.Z, -90.0)])
    devkit = _place(devkit, DEVKIT_CENTER[0], DEVKIT_CENTER[1], DEVKIT_CENTER[2] - 6.0, ref={"Z": "min"})
    # Pololu carrier lies flat; bottom on the old 12 mm envelope floor (Z 66).
    drivers = []
    for side, y in (("LEFT", 40.0), ("RIGHT", -40.0)):
        drv = _purchased_step("pololu_drv8874_carrier.step", f"DRV8874_{side}_INSTALLED")
        drivers.append(_place(drv, 30.0 + BODY_SHIFT_X, y, 66.0, ref={"Z": "min"}))
    driver_l, driver_r = drivers
    power = _box(48.0, 36.0, 18.0, (-35.0 + BODY_SHIFT_X, -35.0, 75.0), "POWER_DISTRIBUTION_RP02_ENVELOPE", "#D38132", 0.74)
    safety = _box(42.0, 28.0, 14.0, (-34.0 + BODY_SHIFT_X, 35.0, 75.0), "SAFETY_AND_WATCHDOG_ENVELOPE", "#C55842", 0.74)
    imu = _box(25.0, 25.0, 5.0, (BODY_AXIS_X, 0.0, 60.0), "IMU_BREAKOUT_ENVELOPE", "#39BBD3", 0.80)
    return Compound(label="BODY_ELECTRONICS", children=[
        battery,
        pi_tray,
        raspberry_pi5(),
        cooler,
        devkit,
        driver_l,
        driver_r,
        power,
        safety,
        imu,
    ])


def _tcrt_ski_cartridge(name, center):
    """Compact sensor cartridge hidden inside the faceted rear tail."""
    x, y, z = center
    package_x, package_y, package_z = TCRT_PACKAGE_SIZE
    parts = [
        # Optical face down (flip 180 deg about X); face plane at TCRT_OPTICAL_FACE_Z, leads point up into the cartridge.
        _place(
            _purchased_step("vishay_tcrt5000.step", f"TCRT5000_{name}_STEP", [(Axis.X, 180.0)]),
            x, y, TCRT_OPTICAL_FACE_Z, ref={"Z": "min"},
        ),
        _box(11.5, 1.2, 7.5, (x, y - 4.45, z + 0.5), f"TCRT_{name}_INTERNAL_GUIDE_R", FRAME_BLUE, 1.0),
        _box(11.5, 1.2, 7.5, (x, y + 4.45, z + 0.5), f"TCRT_{name}_INTERNAL_GUIDE_L", FRAME_BLUE, 1.0),
        _box(11.0, 7.0, 1.0, (x, y, z + 4.25), f"TCRT_{name}_HEIGHT_SHIM", STEEL, 0.78),
        _box(12.0, 6.5, 4.0, (x + 11.0, y, z + 4.5), f"TCRT_{name}_INTERNAL_CONNECTOR_RESERVE", "#79C4CB", 0.18),
    ]
    return Compound(label=f"TCRT_{name}_REAR_TAIL_CARTRIDGE", children=parts)


def sensors():
    depth = FRONT_RANGE_SENSOR_SIZE[0]
    body_x0 = FRONT_RANGE_SENSOR_FACE_X - depth
    connector_x0 = body_x0 - FRONT_RANGE_CONNECTOR_DEPTH
    parts = [
        # STEP lenses face -Y; +90 deg about Z points them along +X. Lens tip on FACE_X.
        _place(
            _purchased_step("sharp_gp2y0a41sk0f.step", "GP2Y0A41SK0F_STEP", [(Axis.Z, 90.0)]),
            FRONT_RANGE_SENSOR_FACE_X, FRONT_RANGE_SENSOR_Y, FRONT_RANGE_SENSOR_BOTTOM_Z, ref={"X": "max", "Z": "min"},
        ),
        _paint(
            _block(connector_x0, body_x0, -5.0, 5.0, FRONT_RANGE_SENSOR_Z - 4.0, FRONT_RANGE_SENSOR_Z + 5.0),
            "GP2Y_CONNECTOR_RESERVE",
            "#79C4CB",
            0.30,
        ),
        _cylinder(1.2, 42.0, (FRONT_RANGE_SENSOR_FACE_X + 21.0, FRONT_RANGE_SENSOR_Y, FRONT_RANGE_SENSOR_Z), "GP2Y_OPTICAL_AXIS", "#EE4B3B", 0.70, "x"),
        tactile_ball_nose(),
    ]
    return Compound(label="BODY_SENSORS", children=parts)


def body_audio():
    """Provisional speaker, amplifier, and four body-microphone envelopes."""
    sx, sy, sz = SPEAKER_CENTER
    cavity = _cylinder(
        SPEAKER_BASKET_DIAMETER / 2.0 + 2.0,
        SPEAKER_CAVITY_DEPTH,
        (sx - 8.0, sy, sz),
        "SPEAKER_ACOUSTIC_CAVITY_KEEP_OUT",
        "#59B7D6",
        0.16,
        "x",
    )
    basket = _cylinder(
        SPEAKER_BASKET_DIAMETER / 2.0,
        SPEAKER_DEPTH,
        SPEAKER_CENTER,
        "SPEAKER_50MM_BASKET_ENVELOPE",
        SLATE_DARK,
        0.92,
        "x",
    )
    cone = _cylinder(
        SPEAKER_CONE_DIAMETER / 2.0,
        2.0,
        (BODY_X_FRONT - 1.5, sy, sz),  # 0.5 mm behind the front panel's inner face
        "SPEAKER_44MM_CONE",
        "#252B2E",
        1.0,
        "x",
    )
    magnet = _cylinder(14.0, 10.0, (58.0 + BODY_SHIFT_X, sy, sz), "SPEAKER_MAGNET_ENVELOPE", BRONZE, 1.0, "x")
    amplifier = _box(38.0, 30.0, 9.0, (33.0 + BODY_SHIFT_X, 0.0, 103.0), "SPEAKER_AMPLIFIER_ENVELOPE", PCB_GREEN, 0.86)
    parts = [cavity, basket, cone, magnet, amplifier]
    for x, y, z, name in MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0
        board = _box(12.0, 2.0, 8.0, (x, sign * 70.0, z), f"PDM_MIC_{name}_BOARD_ENVELOPE", PCB_GREEN, 0.94)
        port = _cylinder(1.25, 8.0, (x, sign * 74.0, z), f"PDM_MIC_{name}_ACOUSTIC_PORT", "#252B2E", 1.0, "y")
        boot = _cylinder(3.0, 5.0, (x, sign * 72.5, z), f"PDM_MIC_{name}_PORT_BOOT", RUBBER, 0.90, "y")
        parts.extend([board, port, boot])
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
    pinion = Cylinder(YAW_GEAR_OUTER_RADIUS, gear_z[1] - gear_z[0]).moved(Location((px, py, sum(gear_z) / 2.0)))
    shaft = Cylinder(2.5, gear_z[0] - z1).moved(Location((px, py, (gear_z[0] + z1) / 2.0)))
    return Compound(label="BODY_YAW_STAGE", children=[
        _paint(_ring(*YAW_BEARING_RADII, *YAW_BEARING_Z), "YAW_THIN_SECTION_BEARING_ENVELOPE", STEEL, 0.9),
        _paint(pinion, "YAW_DRIVE_SPUR_1TO1", STEEL, 1.0),
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
        _box(76.0, 10.0, 10.0, (16.0 + BODY_SHIFT_X, 0.0, 62.0), "HARNESS_BATTERY_TRUNK", "#F28C28", 0.42),
        _box(12.0, 92.0, 10.0, (8.0 + BODY_SHIFT_X, 0.0, 70.0), "HARNESS_MOTOR_BRANCH", "#D94A3A", 0.42),
        _box(82.0, 8.0, 8.0, (30.0 + BODY_SHIFT_X, 26.0, 82.0), "HARNESS_SIGNAL_TRUNK", "#2FAFC2", 0.42),
        _box(82.0, 8.0, 8.0, (30.0 + BODY_SHIFT_X, -26.0, 82.0), "HARNESS_SENSOR_TRUNK", "#44BDD0", 0.42),
        _box(12.0, 12.0, YAW_PLATE_Z[0] - 78.0, (BODY_AXIS_X, 0.0, (YAW_PLATE_Z[0] + 78.0) / 2.0), "HARNESS_HEAD_VERTICAL", "#9566D9", 0.35),
        # Flat clock-spring loop under the disc takes the ±55° yaw twist.
        _paint(_ring(*YAW_CLOCKSPRING_RADII, *YAW_BEARING_Z), "HARNESS_HEAD_YAW_CLOCKSPRING_RESERVE", "#9566D9", 0.20),
    ]
    return Compound(label="HARNESS_ROUTES", children=parts)


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
    asm.add(body_shell(), "BODY_SHELL")
    asm.add(body_panels(), "BODY_PANELS")
    asm.add(panel_mount_hardware(), "PANEL_MOUNT_HARDWARE")
    asm.add(body_yaw_stage(), "BODY_YAW_STAGE")
    asm.add(head, "RP01_HEAD_LAYOUT03")
    asm.add(head_harness, "RP01_HEAD_HARNESS")
    asm.add(head_physics, "RP01_HEAD_PHYSICS")
    asm.add(physics_overlays(), "PHYSICS_OVERLAYS")
    return asm.build()
