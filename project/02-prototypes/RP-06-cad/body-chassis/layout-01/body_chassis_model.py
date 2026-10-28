"""RP-03 integrated body/chassis Layout 01.

Coordinate frame: millimetres; origin on ground at the drive-axle line and
robot centre plane; +X forward, +Y robot-left, +Z up.

The RP-01 Layout 03 head is composed from its live Python source. Purchased
STEP geometry is imported through cadgen.step_scene.import_step.
"""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cylinder,
    Location,
    Plane,
    Polygon,
    Sphere,
    extrude,
    loft,
)
from cadgen import srgb
from cadgen.assembly import AssemblyHelper
try:
    # text-to-cad 0.4.28 runtime: cached imported-STEP path.
    from cadgen.step_scene import import_step
except ImportError:  # repository's older CAD venv compatibility for report scripts
    from build123d import import_step


HERE = Path(__file__).resolve().parent
PURCHASED = HERE / "references" / "purchased"
HEAD_DIR = HERE.parents[2] / "head" / "layout-03"

HEAD_MODEL = None


def _load_head_model():
    """Load RP-01 Layout 03 lazily from source for the actual CAD build.

    Report/check scripts can import this module without paying the full head
    build dependency cost. During `gen`, the text-to-cad runtime supplies the
    current cached STEP importer required by Layout 03.
    """
    global HEAD_MODEL
    if HEAD_MODEL is not None:
        return HEAD_MODEL
    if str(HEAD_DIR) not in sys.path:
        sys.path.insert(0, str(HEAD_DIR))
    for module_name in (
        "layout_axes",
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

LAYOUT_ID = "RP03_BODY_CHASSIS_LAYOUT01"
LAYOUT_REV = "layout-01.5"

# Palette follows RP-01 Layout 03 so the whole robot reads as one assembly.
IVORY = "#E3DDC9"
SLATE = "#87949A"
SLATE_DARK = "#707D82"
FRAME_BLUE = "#86A1A8"
PANEL_WARM_GRAY = "#C5C0AD"
MOBILITY_GRAY = "#7E8B8F"
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
AXLE_CROSSMEMBER_WIDTH = 156.0
WHEEL_CENTER_L = (0.0, TRACK / 2.0, AXLE_Z)
WHEEL_CENTER_R = (0.0, -TRACK / 2.0, AXLE_Z)

BALL_CONTACT = (110.0, 0.0, 0.0)
BALL_DIAMETER = 25.4
BALL_HOUSING_WIDTH = 34.0
BALL_NATIVE_HEIGHT = 29.0
BALL_HOLE_RADIUS = 12.2
BALL_FLANGE_OD = 36.0
BALL_MOUNT_MODE = "FIXED_3HOLE_NON_INTERCHANGEABLE"
BALL_COLLAR_OUTER_RADIUS = 21.0
BALL_COLLAR_BORE_RADIUS = 17.25
BALL_COLLAR_Z0 = 23.0
BALL_COLLAR_HEIGHT = 6.0
BALL_RAIL_OFFSET_Y = 18.5
BALL_RAIL_END_X = 108.0
BALL_RAIL_END_Z = 27.5

BODY_X_REAR = -74.0
BODY_X_FRONT = 82.0
BODY_Z_BOTTOM = 30.0
BODY_Z_TOP = 140.0
BODY_WIDTH_LOWER = 174.0
BODY_WIDTH_UPPER = 148.0
SHELL_THICKNESS = 2.4

HEAD_YAW_DATUM = (0.0, 0.0, 140.0)
HEAD_ORIGIN_IN_CHASSIS = (37.9645316623177, 0.0, 200.0)
HEAD_LOCAL_YAW = (-37.9645316623177, 0.0, -60.0)
HEAD_LOCAL_COM = (-39.55188359184538, 0.7458558252366899, 40.295971393290785)
HEAD_MASS_G = 509.04
HEAD_CROWN_Z_LOCAL = 104.0
OVERALL_PHYSICAL_HEIGHT = HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_CROWN_Z_LOCAL
NECK_ALLOCATION = HEAD_ORIGIN_IN_CHASSIS[2] - BODY_Z_TOP

CHASSIS_RAIL_X0 = -62.0
CHASSIS_RAIL_X1 = 102.0
CHASSIS_RAIL_Y = 54.0
DECK_Z = 54.0

PI_CENTER = (6.0, 0.0, 102.0)
BATTERY_CENTER = (38.0, 0.0, 69.0)
DEVKIT_CENTER = (-24.0, 44.0, 84.0)
SKID_ROOT_DATUM = (-56.0, 0.0, 34.0)
SKID_SHOE_SIZE = (22.0, 16.0, 2.5)
SKID_SHOE_BOTTOM_Z = 3.5
SKID_PAD_CENTER = (-70.0, 0.0, SKID_SHOE_BOTTOM_Z + SKID_SHOE_SIZE[2] / 2.0)
TCRT_PACKAGE_SIZE = (10.2, 5.8, 7.0)
TCRT_OPTICAL_FACE_Z = 10.0
TCRT_GUARD_BOTTOM_Z = 7.0
TCRT_REAR_LOOKAHEAD = 27.0
TCRT_CHANNELS = ("REAR",)
TCRT_REAR_CENTER = (SKID_PAD_CENTER[0] - TCRT_REAR_LOOKAHEAD, 0.0, TCRT_OPTICAL_FACE_Z + TCRT_PACKAGE_SIZE[2] / 2.0)
REAR_TAIL_STYLE = "MULTI_LINK_FACETED_ARC"
REAR_TAIL_VISIBLE_COLOR = IVORY
REAR_TAIL_SHELL_ALPHA = 0.34
REAR_TAIL_WALL = 2.0
REAR_TAIL_STATIONS = (
    # x, half-width, lower-z, upper-z, corner chamfer
    (-52.0, 10.5, 28.0, 46.0, 2.2),  # crossmember root overlap
    (-61.0, 9.6, 21.0, 36.0, 2.0),   # first downward break
    (-69.0, 8.8, 10.0, 24.0, 1.8),   # approach to skid belly
    (-77.0, 8.0, 5.5, 18.0, 1.7),    # lowest belly station
    (-85.0, 7.4, 6.5, 19.0, 1.5),    # early rising shank
    (-92.0, 7.2, 8.0, 21.0, 1.4),    # sensor approach
    (-97.0, 7.5, 10.0, 22.5, 1.4),   # raised sensor centre
    (-103.0, 6.8, 12.0, 24.0, 1.2),  # cartridge departure
    (-109.0, 5.4, 15.5, 26.0, 1.0),  # first terminal link
    (-114.0, 3.5, 20.0, 27.0, 0.8),  # second terminal link
    (-118.0, 1.8, 24.5, 28.5, 0.5),  # compact faceted point
)
REAR_TAIL_INNER_STATIONS = (
    # The cavity begins after the load-bearing root and stops before the point.
    (-57.0, 7.7, 26.0, 39.0, 1.4),
    (-61.0, 7.6, 23.0, 34.0, 1.2),
    (-69.0, 6.8, 12.0, 22.0, 1.1),
    (-77.0, 6.0, 7.5, 16.0, 1.0),
    (-85.0, 5.4, 8.5, 17.0, 0.9),
    (-92.0, 5.2, 10.0, 19.0, 0.8),
    (-97.0, 5.5, 12.0, 20.5, 0.8),
    (-103.0, 4.8, 14.0, 22.0, 0.7),
    (-109.0, 3.4, 17.5, 24.0, 0.5),
)
REAR_TAIL_SENSOR_POCKET_X = (-103.0, -91.0)
REAR_TAIL_CAP_SIZE = (14.0, 15.0, 1.5)
REAR_TAIL_CAP_TOP_Z = 22.5
REAR_TAIL_GUARD_X = (-105.0, -90.0)
REAR_TAIL_GUARD_WIDTH = 2.5
REAR_TAIL_GUARD_HEIGHT = 2.5

TACTILE_NOSE_FACE_X = 123.5
TACTILE_NOSE_TRAVEL = 3.0


FRAMES = {
    "F_GROUND": (0.0, 0.0, 0.0),
    "F_AXLE": (0.0, 0.0, AXLE_Z),
    "F_WHEEL_L": WHEEL_CENTER_L,
    "F_WHEEL_R": WHEEL_CENTER_R,
    "F_BALL_TRANSFER": BALL_CONTACT,
    "F_BODY_BASE": (0.0, 0.0, BODY_Z_BOTTOM),
    "F_HEAD_YAW": HEAD_YAW_DATUM,
    "F_COMPUTE_TRAY": (PI_CENTER[0], PI_CENTER[1], 86.0),
    "F_POWER_BAY": BATTERY_CENTER,
    "F_SENSOR_FRONT": (78.0, 0.0, 82.0),
}


MASS_ROWS = [
    ("RP01_HEAD_LAYOUT03", HEAD_MASS_G, (
        HEAD_ORIGIN_IN_CHASSIS[0] + HEAD_LOCAL_COM[0],
        HEAD_ORIGIN_IN_CHASSIS[1] + HEAD_LOCAL_COM[1],
        HEAD_ORIGIN_IN_CHASSIS[2] + HEAD_LOCAL_COM[2],
    ), "RP-01 generated mass tree"),
    ("BODY_SHELL_AND_PANELS", 285.0, (4.0, 0.0, 96.0), "CAD estimate"),
    ("BODY_PRIMARY_FRAME", 310.0, (4.0, 0.0, 91.0), "CAD estimate"),
    ("CHASSIS_PRIMARY_FRAME", 230.0, (16.0, 0.0, 47.0), "CAD estimate"),
    ("WHEEL_L", 90.0, WHEEL_CENTER_L, "vendor/envelope"),
    ("WHEEL_R", 90.0, WHEEL_CENTER_R, "vendor/envelope"),
    ("MOTOR_L", 110.0, (0.0, 52.0, AXLE_Z), "vendor"),
    ("MOTOR_R", 110.0, (0.0, -52.0, AXLE_Z), "vendor"),
    ("BALL_TRANSFER", 16.5, (BALL_CONTACT[0], 0.0, 14.0), "vendor"),
    ("BATTERY", 280.0, BATTERY_CENTER, "RP-02 placeholder"),
    ("RASPBERRY_PI5_AND_COOLER", 76.0, PI_CENTER, "vendor + estimate"),
    ("CONTROL_POWER_SENSORS", 125.0, (6.0, 0.0, 80.0), "estimate; one rear TCRT channel"),
    ("HARNESS_AND_FASTENERS", 95.0, (4.0, 0.0, 88.0), "estimate"),
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


def ball_nose_fairing():
    """Close-fitting fixed shroud around the frozen ball-transfer flange."""
    outer = loft([
        _nose_profile(88.0, 26.0, 32.0, 49.0, 3.0),
        _nose_profile(104.0, 22.5, 29.0, 44.0, 3.0),
        _nose_profile(119.0, 20.5, 27.0, 39.5, 2.5),
    ], ruled=True)
    inner = loft([
        _nose_profile(90.4, 23.6, 34.4, 46.6, 2.2),
        _nose_profile(104.0, 20.1, 31.4, 41.6, 2.2),
        _nose_profile(116.6, 18.1, 29.4, 37.1, 1.8),
    ], ruled=True)
    fairing = outer - inner
    fairing = fairing - _block(85.0, 91.0, -24.0, 24.0, 35.0, 48.0)
    fairing = fairing - _vertical_bore(19.0, 22.0, 58.0, BALL_CONTACT[0], 0.0)
    return _paint(fairing, "BALL_COMPACT_FIXED_SHROUD", IVORY, 0.78)


def rear_skid_tcrt_module():
    """Selectable hollow rear-tail assembly with visible load and sensor paths."""
    outer = loft(
        [_nose_profile(x, half_width, z0, z1, chamfer) for x, half_width, z0, z1, chamfer in REAR_TAIL_STATIONS],
        ruled=True,
    )
    inner = loft(
        [_nose_profile(x, half_width, z0, z1, chamfer) for x, half_width, z0, z1, chamfer in REAR_TAIL_INNER_STATIONS],
        ruled=True,
    )

    # A central top/bottom service aperture exposes the cartridge while leaving
    # the translucent side walls continuous and structurally legible.
    pocket_x0, pocket_x1 = REAR_TAIL_SENSOR_POCKET_X
    sensor_pocket = _block(pocket_x0, pocket_x1, -4.0, 4.0, 6.5, 23.0)
    cable_tunnel = _block(pocket_x1 - 1.0, -74.0, -3.5, 3.5, 16.0, 20.5)
    shell = _paint(
        outer - [inner, sensor_pocket, cable_tunnel],
        "REAR_TAIL_TRANSLUCENT_HOLLOW_SHELL",
        REAR_TAIL_VISIBLE_COLOR,
        REAR_TAIL_SHELL_ALPHA,
    )

    # A narrow blue internal spine makes the load path from crossmember to skid
    # explicit. It stops before the service cartridge rather than obscuring it.
    spine_stations = (
        (-52.0, 3.6, 34.0, 40.0, 1.0),
        (-61.0, 3.2, 27.0, 32.0, 0.9),
        (-69.0, 3.0, 15.0, 19.5, 0.8),
        (-77.0, 2.7, 10.0, 14.0, 0.7),
        (-85.0, 2.5, 11.0, 14.5, 0.6),
        (-90.0, 2.3, 13.0, 16.2, 0.5),
    )
    spine = loft(
        [_nose_profile(x, half_width, z0, z1, chamfer) for x, half_width, z0, z1, chamfer in spine_stations],
        ruled=True,
    )
    spine = _paint(spine, "REAR_TAIL_INTERNAL_LOAD_SPINE", FRAME_BLUE, 1.0)

    # Chamfered replaceable shoe retains the original nominal skid datum and
    # remains lower than every part of the sensor cartridge.
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
    shoe = _paint(shoe, "REAR_TAIL_REPLACEABLE_WEAR_SHOE", IVORY, 1.0)

    # The low sacrificial lips are separate, replaceable pieces nested into the
    # shell side walls; they remain below the optical face but above the shoe.
    gx0, gx1 = REAR_TAIL_GUARD_X
    guard_length = gx1 - gx0
    guards = [
        _box(
            guard_length,
            REAR_TAIL_GUARD_WIDTH,
            REAR_TAIL_GUARD_HEIGHT,
            ((gx0 + gx1) / 2.0, sign * 6.35, TCRT_GUARD_BOTTOM_Z + REAR_TAIL_GUARD_HEIGHT / 2.0),
            f"REAR_TAIL_REPLACEABLE_GUARD_{side}",
            IVORY,
        )
        for sign, side in ((1.0, "L"), (-1.0, "R"))
    ]

    # A translucent flush cap keeps the package visible and serviceable.
    cap_x, cap_y, cap_z = REAR_TAIL_CAP_SIZE
    cap_chamfer = 1.5
    cx = TCRT_REAR_CENTER[0]
    cy = TCRT_REAR_CENTER[1]
    cap_face = Plane.XY * Polygon(
        (cx - cap_x / 2.0 + cap_chamfer, cy - cap_y / 2.0),
        (cx + cap_x / 2.0 - cap_chamfer, cy - cap_y / 2.0),
        (cx + cap_x / 2.0, cy - cap_y / 2.0 + cap_chamfer),
        (cx + cap_x / 2.0, cy + cap_y / 2.0 - cap_chamfer),
        (cx + cap_x / 2.0 - cap_chamfer, cy + cap_y / 2.0),
        (cx - cap_x / 2.0 + cap_chamfer, cy + cap_y / 2.0),
        (cx - cap_x / 2.0, cy + cap_y / 2.0 - cap_chamfer),
        (cx - cap_x / 2.0, cy - cap_y / 2.0 + cap_chamfer),
        align=None,
    )
    cap = extrude(cap_face.moved(Location((0.0, 0.0, REAR_TAIL_CAP_TOP_Z - cap_z))), amount=cap_z)
    cap = _paint(cap, "REAR_TAIL_TRANSLUCENT_SENSOR_CAP", IVORY, 0.52)

    cartridge = _tcrt_ski_cartridge("REAR", TCRT_REAR_CENTER)
    cable = _beam_xz(-91.0, 18.0, -76.0, 18.0, 4.5, 3.0, "TCRT_REAR_INTERNAL_CABLE_ROUTE", "#79C4CB")
    floor_interface = Compound(label="REAR_TAIL_FLOOR_INTERFACE", children=[shoe, *guards])
    internals = Compound(label="REAR_TAIL_VISIBLE_INTERNALS", children=[spine, cartridge, cable])
    return Compound(
        label="REAR_SKID_TCRT_MODULE",
        children=[shell, internals, floor_interface, cap],
    )


def rear_ski_keel():
    """Compatibility alias for checks/scripts written before Layout 01.4."""
    return rear_skid_tcrt_module()


def tactile_ball_nose():
    """Narrow hidden-contact fascia; replaces the exposed stance-wide bumper."""
    fascia = _box(2.5, 42.0, 16.0, (TACTILE_NOSE_FACE_X, 0.0, 37.0), "BALL_NOSE_TACTILE_FASCIA", IVORY)
    flexures = [
        _box(7.0, 3.0, 10.0, (119.0, sign * 17.0, 37.0), f"BALL_NOSE_FLEXURE_{side}", FRAME_BLUE)
        for sign, side in ((1.0, "L"), (-1.0, "R"))
    ]
    switch = _box(8.0, 12.0, 8.0, (116.0, 0.0, 37.0), "BALL_NOSE_HIDDEN_MICROSWITCH", "#7A4A21", 0.92)
    plunger = _cylinder(1.8, 5.0, (121.0, 0.0, 37.0), "BALL_NOSE_SWITCH_PLUNGER", STEEL, 1.0, "x")
    travel = _box(
        TACTILE_NOSE_TRAVEL,
        44.0,
        18.0,
        (TACTILE_NOSE_FACE_X - TACTILE_NOSE_TRAVEL / 2.0, 0.0, 37.0),
        "BALL_NOSE_3MM_TRAVEL_RESERVE",
        "#D95FC5",
        0.14,
    )
    return Compound(label="BALL_NOSE_CONCEALED_CONTACT_MODULE", children=[fascia, *flexures, switch, plunger, travel])


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


def _panel(x0, x1, width_bottom, width_top, z0, z1, label, color, alpha):
    lb = width_bottom / 2.0
    lt = width_top / 2.0
    points = [(-lb, z0), (lb, z0), (lt, z1), (-lt, z1)]
    face = (Plane.YZ * Polygon(*points, align=None)).moved(Location((x0, 0.0, 0.0)))
    return _paint(extrude(face, amount=x1 - x0), label, color, alpha)


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
            _body_profile(BODY_X_REAR, 0.0, 0.90),
            _body_profile(-58.0, 0.0, 1.00),
            _body_profile(60.0, 0.0, 1.00),
            _body_profile(BODY_X_FRONT, 0.0, 0.92),
        ],
        ruled=True,
    )
    inner = loft(
        [
            _body_profile(BODY_X_REAR + SHELL_THICKNESS, SHELL_THICKNESS, 0.90),
            _body_profile(-56.0, SHELL_THICKNESS, 1.00),
            _body_profile(58.0, SHELL_THICKNESS, 1.00),
            _body_profile(BODY_X_FRONT - SHELL_THICKNESS, SHELL_THICKNESS, 0.92),
        ],
        ruled=True,
    )
    shell = outer - inner
    front_opening = _block(77.0, 88.0, -57.0, 57.0, 43.0, 132.0)
    rear_opening = _block(-82.0, -68.0, -54.0, 54.0, 45.0, 132.0)
    shell = shell - [front_opening, rear_opening, *_wheel_well_tools()]
    return _paint(shell, "BODY_SHELL", IVORY, 0.28)


def body_panels():
    front = _panel(82.0, 84.4, 110.0, 92.0, 48.0, 130.0, "FRONT_SERVICE_PANEL", PANEL_WARM_GRAY, 0.84)
    rear = _panel(-76.4, -74.0, 104.0, 90.0, 48.0, 130.0, "REAR_SERVICE_PANEL", IVORY, 0.62)
    slats = []
    for index, y in enumerate((-38.0, -25.0, -12.0, 0.0, 12.0, 25.0, 38.0), start=1):
        slats.append(_box(2.2, 4.0, 50.0, (85.0, y, 88.0), f"FRONT_GRILLE_SLAT_{index}", SLATE, 0.88))
    top_badge = _box(2.0, 38.0, 4.0, (85.1, 0.0, 122.0), "FRONT_BADGE_LAND", AMBER, 0.92)
    wheel_arches = []
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        yc = sign * TRACK / 2.0
        pod_outer = _cylinder(52.0, 18.0, (0.0, yc, AXLE_Z), f"WHEEL_ARCH_OUTER_{side}", IVORY, 1.0, "y")
        pod_inner = _cylinder(46.0, 22.0, (0.0, yc, AXLE_Z), f"WHEEL_ARCH_INNER_{side}", IVORY, 1.0, "y")
        pod = pod_outer - pod_inner - _block(-58.0, 58.0, -105.0, 105.0, -10.0, AXLE_Z)
        pod = _paint(pod, f"WHEEL_ARCH_POD_{side}", IVORY, 0.72)

        outer_face_y = sign * (TRACK / 2.0 + WHEEL_WIDTH / 2.0 + 1.5)
        trim_outer = _cylinder(48.0, 3.0, (0.0, outer_face_y, AXLE_Z), f"WHEEL_ARCH_TRIM_OUTER_{side}", AMBER, 1.0, "y")
        trim_inner = _cylinder(44.0, 5.0, (0.0, outer_face_y, AXLE_Z), f"WHEEL_ARCH_TRIM_INNER_{side}", AMBER, 1.0, "y")
        trim = trim_outer - trim_inner - _block(-56.0, 56.0, -105.0, 105.0, -10.0, AXLE_Z)
        trim = _paint(trim, f"WHEEL_ARCH_UPPER_TRIM_{side}", AMBER, 0.92)
        wheel_arches.append(Compound(label=f"WHEEL_ARCH_{side}", children=[pod, trim]))
    return Compound(label="BODY_PANELS", children=[front, rear, *slats, top_badge, *wheel_arches])


def lower_mobility_belt():
    outer = _box(148.0, 178.0, 28.0, (8.0, 0.0, 45.0), "BELT_OUTER", MOBILITY_GRAY, 0.88)
    inner_tool = Box(143.0, 164.0, 23.0).moved(Location((8.0, 0.0, 46.5)))
    return _paint(outer - [inner_tool, *_wheel_well_tools()], "LOWER_MOBILITY_BELT", MOBILITY_GRAY, 0.88)


def chassis_frame():
    parts = [
        _box(CHASSIS_RAIL_X1 - CHASSIS_RAIL_X0, 8.0, 18.0, ((CHASSIS_RAIL_X0 + CHASSIS_RAIL_X1) / 2, CHASSIS_RAIL_Y, 44.0), "CHASSIS_RAIL_L", SLATE),
        _box(CHASSIS_RAIL_X1 - CHASSIS_RAIL_X0, 8.0, 18.0, ((CHASSIS_RAIL_X0 + CHASSIS_RAIL_X1) / 2, -CHASSIS_RAIL_Y, 44.0), "CHASSIS_RAIL_R", SLATE),
        _box(12.0, AXLE_CROSSMEMBER_WIDTH, 18.0, (0.0, 0.0, 44.0), "AXLE_CROSSMEMBER", FRAME_BLUE),
        _box(12.0, 116.0, 16.0, (90.0, 0.0, 43.0), "FRONT_CROSSMEMBER", FRAME_BLUE),
        _box(16.0, 116.0, 14.0, (-56.0, 0.0, 41.0), "REAR_SKID_CROSSMEMBER", FRAME_BLUE),
        _box(126.0, 112.0, 4.0, (22.0, 0.0, DECK_Z), "CHASSIS_DECK", FRAME_BLUE),
    ]

    # The wheel centres stay at the frozen 170 mm track.  These bored carrier
    # blocks extend the structural axle member out to the paired 608 bearings,
    # eliminating the previous unsupported gap between chassis and wheels.
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        carrier_y = sign * 71.0
        carrier = Box(34.0, 26.0, 34.0).moved(Location((0.0, carrier_y, AXLE_Z)))
        carrier = carrier - _cylinder(11.25, 32.0, (0.0, carrier_y, AXLE_Z), f"AXLE_CARRIER_BORE_{side}", "#FFFFFF", 1.0, "y")
        carrier = _paint(carrier, f"AXLE_BEARING_CARRIER_{side}", FRAME_BLUE, 1.0)
        upper_gusset = _beam_xz(-12.0, 53.0, 0.0, 58.0, 18.0, 5.0, f"AXLE_CARRIER_GUSSET_{side}", SLATE)
        upper_gusset = upper_gusset.moved(Location((0.0, sign * 65.0, 0.0)))
        parts.extend([carrier, upper_gusset])

    # Frozen, non-interchangeable ball-transfer nose. Compact angled rails
    # carry the ball reaction into the front crossmember. The fixed collar
    # supports the purchased flange from below; paired keeper clips capture
    # its top face so the module has an explicit load path in both directions.
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        rail = _beam_xz(88.0, 43.0, BALL_RAIL_END_X, BALL_RAIL_END_Z, 7.0, 7.0, f"BALL_NOSE_RAIL_{side}", SLATE)
        rail = rail.moved(Location((0.0, sign * BALL_RAIL_OFFSET_Y, 0.0)))
        parts.append(rail)
    collar = Cylinder(BALL_COLLAR_OUTER_RADIUS, BALL_COLLAR_HEIGHT).moved(Location((BALL_CONTACT[0], 0.0, BALL_COLLAR_Z0)))
    collar = collar - _vertical_bore(BALL_COLLAR_BORE_RADIUS, BALL_COLLAR_Z0 - 1.0, BALL_NATIVE_HEIGHT + 1.0, BALL_CONTACT[0], 0.0)
    posts = []
    caps = []
    for sign, side in ((1.0, "L"), (-1.0, "R")):
        posts.append(_box(9.0, 4.0, 8.0, (BALL_CONTACT[0], sign * 19.5, 29.0), f"BALL_COLLAR_POST_{side}", FRAME_BLUE))
        caps.append(_box(9.0, 8.0, 3.0, (BALL_CONTACT[0], sign * 17.5, 34.5), f"BALL_FLANGE_KEEPER_{side}", FRAME_BLUE))
    parts.append(Compound(label="BALL_FIXED_LOAD_COLLAR", children=[_paint(collar, "BALL_LOAD_COLLAR", FRAME_BLUE, 1.0), *posts, *caps]))
    parts.append(ball_nose_fairing())

    return Compound(label="CHASSIS_PRIMARY_FRAME", children=parts)


def body_primary_frame():
    parts = []
    for x in (-48.0, 48.0):
        for y in (-64.0, 64.0):
            parts.append(_box(10.0, 10.0, 96.0, (x, y, 85.0), f"BODY_POST_{'F' if x > 0 else 'R'}_{'L' if y > 0 else 'R'}", FRAME_BLUE))
    for z, label in ((40.0, "LOWER"), (132.0, "UPPER")):
        parts.extend([
            _box(112.0, 8.0, 8.0, (0.0, 64.0, z), f"BODY_{label}_RAIL_L", FRAME_BLUE),
            _box(112.0, 8.0, 8.0, (0.0, -64.0, z), f"BODY_{label}_RAIL_R", FRAME_BLUE),
            _box(8.0, 120.0, 8.0, (48.0, 0.0, z), f"BODY_{label}_CROSS_FRONT", FRAME_BLUE),
            _box(8.0, 120.0, 8.0, (-48.0, 0.0, z), f"BODY_{label}_CROSS_REAR", FRAME_BLUE),
        ])
    parts.extend([
        _box(10.0, 10.0, 88.0, (0.0, 31.0, 91.0), "HEAD_LOAD_POST_L", SLATE_DARK),
        _box(10.0, 10.0, 88.0, (0.0, -31.0, 91.0), "HEAD_LOAD_POST_R", SLATE_DARK),
        _box(72.0, 72.0, 5.0, (0.0, 0.0, 136.0), "HEAD_ADAPTER_PLATE", FRAME_BLUE),
        _cylinder(20.0, 8.0, HEAD_YAW_DATUM, "HEAD_YAW_COLLAR", STEEL, 1.0),
        _cylinder(6.0, 14.0, (0.0, 0.0, 145.0), "HEAD_CABLE_BORE_REFERENCE", AMBER, 0.40),
    ])
    return Compound(label="BODY_PRIMARY_FRAME", children=parts)


def wheel_assembly(side: str):
    sign = 1.0 if side == "L" else -1.0
    yc = sign * TRACK / 2.0
    tyre = _cylinder(WHEEL_OD / 2.0, WHEEL_WIDTH, (0.0, yc, AXLE_Z), f"WHEEL_{side}_TYRE", RUBBER, 1.0, "y")
    rim = _cylinder(WHEEL_OD / 2.0 - 5.0, WHEEL_WIDTH - 4.0, (0.0, yc, AXLE_Z), f"WHEEL_{side}_RIM", FRAME_BLUE, 1.0, "y")
    hub = _cylinder(14.0, 18.0, (0.0, yc - sign * 4.0, AXLE_Z), f"WHEEL_{side}_HUB", STEEL, 1.0, "y")
    return Compound(label=f"WHEEL_{side}", children=[tyre, rim, hub])


def motor_envelope(side: str):
    sign = 1.0 if side == "L" else -1.0
    face_y = sign * 69.0
    gearbox = _cylinder(12.5, 21.0, (0.0, face_y - sign * 10.5, AXLE_Z), f"MOTOR_{side}_GEARBOX", BRONZE, 1.0, "y")
    can = _cylinder(15.4, 32.0, (0.0, face_y - sign * (21.0 + 16.0), AXLE_Z), f"MOTOR_{side}_CAN", "#A8693D", 1.0, "y")
    encoder = _cylinder(14.0, 12.0, (0.0, face_y - sign * (21.0 + 32.0 + 6.0), AXLE_Z), f"MOTOR_{side}_ENCODER", SLATE_DARK, 1.0, "y")
    pigtail = _box(12.0, 20.0, 10.0, (8.0, sign * 22.0, 51.0), f"MOTOR_{side}_PIGTAIL_RESERVE", "#EF8A3D", 0.34)
    return Compound(label=f"MOTOR_{side}", children=[gearbox, can, encoder, pigtail])


def bearing_pair(side: str):
    source = import_step(str(PURCHASED / "bearing_608zz.step"))
    source = source.rotate(Axis.X, 90.0)
    sign = 1.0 if side == "L" else -1.0
    children = []
    for index, y_abs in enumerate((72.5, 80.0), start=1):
        bearing = _center_at(source, (0.0, sign * y_abs, AXLE_Z))
        bearing.label = f"BEARING_608ZZ_{side}_{index}"
        children.append(bearing)
    return Compound(label=f"BEARING_PAIR_{side}", children=children)


def ball_transfer():
    bx = BALL_CONTACT[0]
    ball_center_z = BALL_DIAMETER / 2.0
    ball = _sphere(BALL_DIAMETER / 2.0, (bx, 0.0, ball_center_z), "BALL_TRANSFER_POM_BALL", IVORY, 1.0)

    cup_outer = Cylinder(16.0, 13.0).moved(Location((bx, 0.0, 16.0)))
    cup_outer = cup_outer - Sphere(BALL_DIAMETER / 2.0 + 0.45).moved(Location((bx, 0.0, ball_center_z)))
    cup_outer = cup_outer - Cylinder(12.9, 16.0).moved(Location((bx, 0.0, 14.0)))
    cup = _paint(cup_outer, "BALL_TRANSFER_PURCHASED_HOUSING", SLATE, 1.0)

    lip = Cylinder(16.8, 3.0).moved(Location((bx, 0.0, 16.0)))
    lip = lip - Cylinder(13.05, 4.0).moved(Location((bx, 0.0, 15.5)))
    lip = _paint(lip, "BALL_TRANSFER_RETAINING_LIP", STEEL, 1.0)

    flange = Cylinder(BALL_FLANGE_OD / 2.0, 4.0).moved(Location((bx, 0.0, 29.0)))
    flange = flange - Cylinder(14.5, 6.0).moved(Location((bx, 0.0, 28.0)))
    for angle_deg in (90.0, 210.0, 330.0):
        angle = math.radians(angle_deg)
        hx = bx + BALL_HOLE_RADIUS * math.cos(angle)
        hy = BALL_HOLE_RADIUS * math.sin(angle)
        flange = flange - _vertical_bore(1.7, 28.0, 34.0, hx, hy)
    flange = _paint(flange, "BALL_TRANSFER_PURCHASED_3HOLE_FLANGE", BRONZE, 1.0)

    # Internal rollers and vendor fasteners are intentionally suppressed: the
    # purchased transfer is represented as one serviceable SKU envelope.
    return Compound(label="BALL_TRANSFER_PURCHASED_FIXED_MODULE", children=[ball, cup, lip, flange])


def raspberry_pi5():
    pi = import_step(str(PURCHASED / "raspberry_pi_5.step")).rotate(Axis.X, 90.0)
    pi = _center_at(pi, PI_CENTER)
    pi.label = "C0_RASPBERRY_PI5_EXACT_STEP"
    return pi


def electronics():
    battery = _box(75.0, 48.0, 24.0, BATTERY_CENTER, "BATTERY_RP02_ENVELOPE", "#3159B8", 0.72)
    battery_tray = _box(84.0, 58.0, 3.0, (BATTERY_CENTER[0], 0.0, 55.5), "BATTERY_TRAY", "#7A858B", 1.0)
    pi_tray = _box(108.0, 76.0, 3.0, (PI_CENTER[0], 0.0, 86.0), "COMPUTE_TRAY", "#7A858B", 1.0)
    cooler = _box(64.0, 44.0, 14.0, (PI_CENTER[0], PI_CENTER[1], 116.0), "PI5_ACTIVE_COOLER_ENVELOPE", "#7D878C", 0.78)
    devkit = _box(69.0, 25.4, 12.0, DEVKIT_CENTER, "C3_ESP32_S3_DEVKITC_N8", "#2D8C53", 0.86)
    driver_l = _box(20.0, 20.0, 12.0, (30.0, 40.0, 72.0), "DRV8874_LEFT_INSTALLED", "#3BAF69", 0.9)
    driver_r = _box(20.0, 20.0, 12.0, (30.0, -40.0, 72.0), "DRV8874_RIGHT_INSTALLED", "#3BAF69", 0.9)
    power = _box(48.0, 36.0, 18.0, (-35.0, -35.0, 75.0), "POWER_DISTRIBUTION_RP02_ENVELOPE", "#D38132", 0.74)
    safety = _box(42.0, 28.0, 14.0, (-34.0, 35.0, 75.0), "SAFETY_AND_WATCHDOG_ENVELOPE", "#C55842", 0.74)
    imu = _box(25.0, 25.0, 5.0, (0.0, 0.0, 60.0), "IMU_BREAKOUT_ENVELOPE", "#39BBD3", 0.80)
    return Compound(label="BODY_ELECTRONICS", children=[
        battery,
        battery_tray,
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
        _box(package_x, package_y, package_z, center, f"TCRT5000_{name}_PACKAGE_ENVELOPE", "#F5D142", 0.92),
        _box(11.5, 1.2, 7.5, (x, y - 4.45, z + 0.5), f"TCRT_{name}_INTERNAL_GUIDE_R", FRAME_BLUE, 1.0),
        _box(11.5, 1.2, 7.5, (x, y + 4.45, z + 0.5), f"TCRT_{name}_INTERNAL_GUIDE_L", FRAME_BLUE, 1.0),
        _box(11.0, 7.0, 1.0, (x, y, z + 4.25), f"TCRT_{name}_HEIGHT_SHIM", STEEL, 0.78),
        _box(12.0, 6.5, 4.0, (x + 11.0, y, z + 4.5), f"TCRT_{name}_INTERNAL_CONNECTOR_RESERVE", "#79C4CB", 0.18),
    ]
    return Compound(label=f"TCRT_{name}_REAR_TAIL_CARTRIDGE", children=parts)


def sensors():
    parts = [
        _box(30.0, 14.0, 14.0, (77.0, 0.0, 88.0), "GP2Y0A41SK0F_ENVELOPE", "#E7B62C", 0.85),
        _cylinder(1.2, 42.0, (100.0, 0.0, 88.0), "GP2Y_OPTICAL_AXIS", "#EE4B3B", 0.70, "x"),
        tactile_ball_nose(),
    ]
    return Compound(label="BODY_SENSORS", children=parts)


def harness_routes():
    # Routed-volume representation: orange high current, red motor power,
    # cyan signal, and violet head link. Volumes include bend/strain reserve.
    parts = [
        _box(76.0, 10.0, 10.0, (16.0, 0.0, 62.0), "HARNESS_BATTERY_TRUNK", "#F28C28", 0.42),
        _box(12.0, 92.0, 10.0, (8.0, 0.0, 70.0), "HARNESS_MOTOR_BRANCH", "#D94A3A", 0.42),
        _box(82.0, 8.0, 8.0, (30.0, 26.0, 82.0), "HARNESS_SIGNAL_TRUNK", "#2FAFC2", 0.42),
        _box(82.0, 8.0, 8.0, (30.0, -26.0, 82.0), "HARNESS_SENSOR_TRUNK", "#44BDD0", 0.42),
        _box(12.0, 12.0, 66.0, (0.0, 0.0, 111.0), "HARNESS_HEAD_VERTICAL", "#9566D9", 0.35),
        _cylinder(16.0, 18.0, (0.0, 0.0, 149.0), "HARNESS_HEAD_YAW_SERVICE_LOOP", "#9566D9", 0.20),
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


def rp01_head_layout03():
    source_head = _load_head_model().assembly()
    # Keep the live Layout03 physical, physics, and harness geometry, but omit
    # RP-01's inspection-only dimension bars from the integrated export.
    head = Compound(
        label="RP01_HEAD_LAYOUT03_LIVE",
        children=[child for child in source_head.children if child.label != "annotations"],
    )
    head = head.moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    return head


def build_assembly():
    asm = AssemblyHelper(LAYOUT_ID)
    asm.add(chassis_frame(), "CHASSIS_PRIMARY_FRAME")
    asm.add(body_primary_frame(), "BODY_PRIMARY_FRAME")
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
    asm.add(harness_routes(), "HARNESS_ROUTES")
    asm.add(body_shell(), "BODY_SHELL")
    asm.add(body_panels(), "BODY_PANELS")
    asm.add(lower_mobility_belt(), "LOWER_MOBILITY_BELT")
    asm.add(rp01_head_layout03(), "RP01_HEAD_LAYOUT03")
    asm.add(physics_overlays(), "PHYSICS_OVERLAYS")
    return asm.build()
