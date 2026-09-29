"""Chassis v1 drive wheel: rim, printed TPU tyre, clamp ring and hub cap (D-005, D-008).

A PETG rim carries a printed TPU 95A chevron-tread tyre. The tyre is keyed to
12 ribs on the rim seat and clamped between an integral inboard lip and a
12-sided bolt-on outboard ring (6 x M3 button-head screws into heat-set
inserts), so it can be swapped with the wheel still on its stub.

The outboard face follows the droid's shell language (00-foundation vision:
rugged, visibly assembled; RP-01 D-07 stepped panels) after the builder's
reference image (D-008): six framed spokes with bevelled sides and a recessed
slot run from a hex hub to a bevelled inner ring; a removable faceted hex cap
(6 x M2 screws) covers the hub and the three D-007 wheel screws; the 12-sided beadlock
ring alternates screw flats with recessed vent slots and has chamfered
corners. Rim and ring light, cap dark: a two-tone print.

Frame: the wheel axis is Y through the origin and +Y is outboard. Chassis |Y|
is 85 + y (inner face y = -12 is |Y| 73, outer face y = +12 is |Y| 97), and
chassis Z is 42 + z. The envelope and the D-007 hub interface match
``../body_chassis_model.py``: Ø84 x 24; R18 pocket over the bearing housing to
y +8 (|Y| 93); a 4 mm web (y +8..+12) with a Ø10 bore on the stub spigot and
3 x Ø3.4 at R8 for the M3 x 6 button heads into the stub flange. Only the hub
cap and its screws stand proud of the outer face. The chassis model itself is
not changed by this file.

All dimensions are the assembled state. Print allowances are in README.md.
"""

from __future__ import annotations

import math

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, Plane, Polygon, RegularPolygon, extrude
from cadgen import srgb

FRAME_BLUE = "#86A1A8"  # PETG rim, same colour as the chassis frame
GUNMETAL = "#3A464D"  # dark PETG hub cap
RUBBER = "#2B3034"
STEEL = "#B7BFC0"
BRONZE = "#A7773E"

# Envelope and chassis interface (from body_chassis_model.py, |Y| - 85).
WHEEL_OD = 84.0
WHEEL_WIDTH = 24.0
Y_IN = -WHEEL_WIDTH / 2.0  # |Y| 73
Y_OUT = WHEEL_WIDTH / 2.0  # |Y| 97
BOSS_POCKET_RADIUS = 18.0  # WHEEL_POCKET_RADIUS: 2 mm radial to the D-007 bearing housing
BOSS_POCKET_FLOOR_Y = 8.0  # WHEEL_POCKET_FLOOR_Y |Y| 93; the stub flange (R12, y 6..8) turns inside
HUB_BORE_RADIUS = 5.0  # WHEEL_HUB_BORE_RADIUS: Ø10 H7 on the stub spigot
STUB_SPIGOT_Y = (8.0, 11.0)  # STUB_SPIGOT |Y| 93..96
STUB_FLANGE = dict(radius=12.0, y=(6.0, 8.0))
WHEEL_SCREW = dict(pcd_r=8.0, clear_radius=1.7, length=6.0, angles=(60.0, 300.0, 180.0))  # D-007 30/150/270 deg from +X
WHEEL_SCREW_HEAD = dict(radius=2.85, height=1.65)  # ISO 7380 M3, on the hub face

# Rim barrel, inner ring, spokes and hub.
RIM_BORE_RADIUS = 30.0  # open dish inside the barrel
FACE_Y = (5.0, Y_OUT)  # 7 mm deep spokes outside the pocket; 4 mm (y 8..12) inside it
INNER_RING_R = (26.0, RIM_BORE_RADIUS + 0.5)
INNER_RING_BEVEL = 1.5  # 45 deg on its inner face edge
SHADOW_GROOVE = dict(r=(29.5, 31.5), depth=1.0)  # between inner ring and clamp ring
SPOKE_COUNT = 6
SPOKE_WIDTH = 10.0  # root; face edges chamfered 1.5 x 1.5 down to 7
SPOKE_CHAMFER = 1.5
SPOKE_R = (12.0, 27.0)
SPOKE_SLOT = dict(width=3.0, depth=2.0, r=(16.0, 24.0))  # recessed slot; 2 mm floor where the spoke is only the 4 mm web
HUB_AF = 26.0  # hex hub and cap, flats toward the spokes
HUB_Y = (BOSS_POCKET_FLOOR_Y, Y_OUT)  # the D-007 4 mm web
CAP_Y = (Y_OUT, Y_OUT + 3.0)  # hex cap body, proud of the face
CAP_BOSS_AF = 16.0  # raised faceted centre on the cap
CAP_BOSS_Y = (CAP_Y[1], CAP_Y[1] + 1.0)
CAP_BOSS_CHAMFER = 1.0
CAP_RECESS = dict(radius=11.2, y=(Y_OUT, Y_OUT + 1.9))  # clears the three M3 heads (to R10.85, 1.65 tall)
CAP_SCREW_R = 12.9  # toward the hex corners, between spokes: head fully on the cap, clear of the boss
CAP_SCREW = dict(length=6.0, clear_radius=1.1, pilot_radius=0.8, head_radius=1.75, head_height=1.3)
CAP_PILOT_Y = (BOSS_POCKET_FLOOR_Y + 0.7, Y_OUT)  # M2 thread-forming into the hub, 0.7 mm skin to the pocket

# Tyre seat, lip and clamp ring.
SEAT_RADIUS = 37.0
LIP_RADIUS = 39.0  # inboard lip overlaps the tyre side by 2 mm
LIP_Y = (Y_IN, -10.0)
TYRE_Y = (-10.0, 9.0)
RING_Y = (9.0, Y_OUT)
SPIGOT_RADIUS = 31.5  # barrel spigot pilots the clamp ring
RING_BORE_RADIUS = 31.7  # 0.2 mm radial on the spigot
RING_SIDES = 12
RING_INRADIUS = 39.0  # flats cover the tyre side by 2 mm
RING_CORNER_CHAMFER = (40.4, 39.4)  # cone radius at y 11 and y 12: chamfers only the corners
RING_VENT = dict(width=9.0, depth=1.2, r=(35.5, 38.2))  # on the six flats between screws
RIB_COUNT = 12
RIB = dict(width=3.0, height=0.8)
KEYWAY = dict(width=3.4, height=1.0)  # tyre bore keyway: 0.2 side, 0.2 top clearance

# Chevron tread.
CARCASS_RADIUS = 40.5
CHEVRON_COUNT = 18
CHEVRON_WIDTH = 5.5  # normal to the bar
CHEVRON_ANGLE = 40.0  # bar angle from the axial direction; >= ~37 deg so each V overlaps the next on the contact line
CHEVRON_APEX_Y = (TYRE_Y[0] + TYRE_Y[1]) / 2.0

# Hardware.
SCREW_COUNT = 6
SCREW_PCD_RADIUS = 34.0
SCREW_CLEAR_RADIUS = 1.7
SCREW_LENGTH = 8.0  # ISO 7380 M3 x 8 button head
SCREW_HEAD = dict(radius=2.85, height=1.65)
INSERT = dict(hole_radius=2.0, bore_radius=1.5, length=4.0)
INSERT_HOLE_Y = (3.0, 9.0)  # 6 mm deep from the barrel face
INSERT_Y = (5.0, 9.0)


def _paint(shape, label, color, alpha=1.0):
    shape.label = label
    children = list(shape.children) if getattr(shape, "children", None) else []
    if children:
        for index, child in enumerate(children, start=1):
            _paint(child, child.label or f"{label}_{index:02}", color, alpha)
    else:
        shape.color = srgb(color, alpha)
    return shape


def _ycyl(radius, y0, y1):
    """Solid cylinder on the wheel axis spanning y0..y1 (measured, not centred)."""
    low, high = sorted((y0, y1))
    return Cylinder(radius, high - low, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(
        Axis.X, -90.0
    ).moved(Location((0.0, (low + high) / 2.0, 0.0)))


def _ring(r0, r1, y0, y1):
    return _ycyl(r1, y0, y1) - _ycyl(r0, y0, y1)


def _yprism(sides, inradius, y0, y1, rotation=0.0):
    """Regular polygon prism on the wheel axis, given its inradius (across flats / 2)."""
    circumradius = inradius / math.cos(math.pi / sides)
    plane = Plane.XZ.offset(-y0)  # XZ normal is -Y; offset(-y0) puts it at y = y0
    poly = RegularPolygon(circumradius, sides, rotation=rotation)
    solid = extrude(plane * poly, amount=y1 - y0, dir=(0.0, 1.0, 0.0))
    return solid


def _ycone(r0, r1, y0, y1):
    """Cone frustum on the wheel axis, radius r0 at y0 and r1 at y1."""
    cone = Cone(r0, r1, y1 - y0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.X, -90.0)
    return cone.moved(Location((0.0, (y0 + y1) / 2.0, 0.0)))


def _radial_prism(profile, r0, r1, angle):
    """Extrude a (tangential x, axial y) profile radially from r0 to r1, at `angle` deg about Y."""
    solid = extrude(Polygon(*profile, align=None), amount=r1 - r0)
    return solid.moved(Location((0.0, 0.0, r0))).rotate(Axis.Y, angle)


def _radial_box(width, y0, y1, r0, r1, angle):
    """Box `width` wide (tangential) from radius r0 to r1, at `angle` deg about Y (0 = +Z)."""
    box = Box(width, y1 - y0, r1 - r0).moved(Location((0.0, (y0 + y1) / 2.0, (r0 + r1) / 2.0)))
    return box.rotate(Axis.Y, angle)


def _at_pcd(shape, radius, angle):
    return shape.moved(Location((0.0, 0.0, radius))).rotate(Axis.Y, angle)


def _spoke_angles():
    return [i * 360.0 / SPOKE_COUNT for i in range(SPOKE_COUNT)]


def _screw_angles():
    # Between the spokes: rim inserts in plain barrel wall, cap screws at the hub hex corners.
    return [(i + 0.5) * 360.0 / SCREW_COUNT for i in range(SCREW_COUNT)]


def _spoke(angle):
    w, c = SPOKE_WIDTH / 2.0, SPOKE_CHAMFER
    y0, y1 = FACE_Y
    profile = [(-w, y0), (w, y0), (w, y1 - c), (w - c, y1), (-w + c, y1), (-w, y1 - c)]
    spoke = _radial_prism(profile, *SPOKE_R, angle)
    slot = _radial_box(SPOKE_SLOT["width"], y1 - SPOKE_SLOT["depth"], y1 + 1.0, *SPOKE_SLOT["r"], angle)
    return spoke - slot


def _face():
    ring = _ring(*INNER_RING_R, *FACE_Y)
    bevel = _ycone(INNER_RING_R[0], INNER_RING_R[0] + INNER_RING_BEVEL + 1.0, Y_OUT - INNER_RING_BEVEL, Y_OUT + 1.0)
    face = ring - bevel
    for angle in _spoke_angles():
        face = face + _spoke(angle)
    face = face + _yprism(6, HUB_AF / 2.0, *HUB_Y)
    face = face - _ycyl(BOSS_POCKET_RADIUS, FACE_Y[0] - 1.0, BOSS_POCKET_FLOOR_Y)
    face = face - _ycyl(HUB_BORE_RADIUS, HUB_Y[0] - 1.0, Y_OUT + 1.0)
    for angle in WHEEL_SCREW["angles"]:
        face = face - _at_pcd(_ycyl(WHEEL_SCREW["clear_radius"], HUB_Y[0] - 1.0, Y_OUT + 1.0), WHEEL_SCREW["pcd_r"], angle)
    for angle in _screw_angles():
        face = face - _at_pcd(_ycyl(CAP_SCREW["pilot_radius"], *CAP_PILOT_Y), CAP_SCREW_R, angle)
    return face


def rim():
    barrel = _ring(RIM_BORE_RADIUS, SEAT_RADIUS, LIP_Y[1], RING_Y[0])
    barrel = barrel + _ring(RIM_BORE_RADIUS, LIP_RADIUS, *LIP_Y)
    barrel = barrel + _ring(RIM_BORE_RADIUS, SPIGOT_RADIUS, *RING_Y)
    for i in range(RIB_COUNT):
        barrel = barrel + _radial_box(RIB["width"], *TYRE_Y, SEAT_RADIUS - 0.2, SEAT_RADIUS + RIB["height"], i * 360.0 / RIB_COUNT)
    body = barrel + _face()
    body = body - _ring(*SHADOW_GROOVE["r"], Y_OUT - SHADOW_GROOVE["depth"], Y_OUT + 1.0)
    for angle in _screw_angles():
        body = body - _at_pcd(_ycyl(INSERT["hole_radius"], *INSERT_HOLE_Y), SCREW_PCD_RADIUS, angle)
    return body


def clamp_ring():
    # A flat faces each screw, as on a beadlock ring.
    ring = _yprism(RING_SIDES, RING_INRADIUS, *RING_Y, rotation=180.0 / RING_SIDES) - _ycyl(RING_BORE_RADIUS, *RING_Y)
    ring = ring & (_ycyl(RING_CORNER_CHAMFER[0] + 1.0, RING_Y[0], Y_OUT - 1.0) + _ycone(*RING_CORNER_CHAMFER, Y_OUT - 1.0, Y_OUT))
    for angle in _screw_angles():
        ring = ring - _at_pcd(_ycyl(SCREW_CLEAR_RADIUS, RING_Y[0] - 1.0, RING_Y[1] + 1.0), SCREW_PCD_RADIUS, angle)
        vent = _radial_box(RING_VENT["width"], Y_OUT - RING_VENT["depth"], Y_OUT + 1.0, *RING_VENT["r"], angle - 30.0)
        ring = ring - vent
    return ring


def hub_cap():
    body = _yprism(6, HUB_AF / 2.0, *CAP_Y)
    boss = _yprism(6, CAP_BOSS_AF / 2.0, *CAP_BOSS_Y)
    circ = CAP_BOSS_AF / 2.0 / math.cos(math.pi / 6.0)
    boss = boss & _ycone(circ + 0.01, circ - CAP_BOSS_CHAMFER, *CAP_BOSS_Y)
    cap = body + boss - _ycyl(CAP_RECESS["radius"], *CAP_RECESS["y"])
    for angle in _screw_angles():
        cap = cap - _at_pcd(_ycyl(CAP_SCREW["clear_radius"], CAP_Y[0] - 1.0, CAP_Y[1] + 1.0), CAP_SCREW_R, angle)
    return cap


def _chevron(angle):
    """One V lug, apex on the tyre centre line, pointing toward +X at angle 0 (the top).

    On the left wheel (+Y outboard) that is forward: the apex leads at the top
    and trails at the contact patch, the tractor convention.
    """
    band_mid = (CARCASS_RADIUS + WHEEL_OD / 2.0) / 2.0
    length = 2.0 * (TYRE_Y[1] - TYRE_Y[0]) / math.cos(math.radians(CHEVRON_ANGLE))
    lug = None
    for y0, y1, tilt in ((TYRE_Y[0], CHEVRON_APEX_Y, -CHEVRON_ANGLE), (CHEVRON_APEX_Y, TYRE_Y[1], CHEVRON_ANGLE)):
        yc = (y0 + y1) / 2.0
        xc = (CHEVRON_APEX_Y - yc) * math.tan(math.radians(tilt))
        bar = Box(CHEVRON_WIDTH, length, 4.0).rotate(Axis.Z, tilt).moved(Location((xc, yc, band_mid)))
        half = _ring(CARCASS_RADIUS - 0.1, WHEEL_OD / 2.0, y0, y1) & bar
        lug = half if lug is None else lug + half
    return lug.rotate(Axis.Y, angle)


def tyre(hand: str = "L"):
    """Handed tyre. The right tyre is the left one mirrored, so on the robot both
    chevrons lead forward; the rim, ring and cap are symmetric and not handed."""
    if hand == "R":
        return tyre("L").mirror(Plane.YZ)
    carcass = _ring(SEAT_RADIUS, CARCASS_RADIUS, *TYRE_Y)
    for i in range(RIB_COUNT):
        carcass = carcass - _radial_box(
            KEYWAY["width"], TYRE_Y[0] - 1.0, TYRE_Y[1] + 1.0,
            SEAT_RADIUS - 0.5, SEAT_RADIUS + KEYWAY["height"], i * 360.0 / RIB_COUNT,
        )
    for i in range(CHEVRON_COUNT):
        carcass = carcass + _chevron(i * 360.0 / CHEVRON_COUNT)
    return carcass


def _hardware():
    """(suffix, shape, colour) for every purchased part on one wheel."""
    parts = []
    for n, angle in enumerate(_screw_angles(), start=1):
        head = _ycyl(SCREW_HEAD["radius"], Y_OUT, Y_OUT + SCREW_HEAD["height"])
        shank = _ycyl(1.5, Y_OUT - SCREW_LENGTH, Y_OUT)
        parts.append((f"RING_SCREW_M3X8_{n}", _at_pcd(head + shank, SCREW_PCD_RADIUS, angle), STEEL))
        # Melted-in insert: its knurl displaces into the 2.0 mm hole wall; shown at hole size.
        insert = _ycyl(INSERT["hole_radius"], *INSERT_Y) - _ycyl(INSERT["bore_radius"], *INSERT_Y)
        parts.append((f"RING_INSERT_M3_{n}", _at_pcd(insert, SCREW_PCD_RADIUS, angle), BRONZE))
        top = CAP_Y[1]
        # Thread-forming shank shown at the pilot size: its thread cuts into the pilot wall.
        shank = _ycyl(CAP_SCREW["pilot_radius"], top - CAP_SCREW["length"], top)
        cap_screw = _ycyl(CAP_SCREW["head_radius"], top, top + CAP_SCREW["head_height"]) + shank
        parts.append((f"CAP_SCREW_M2X6_{n}", _at_pcd(cap_screw, CAP_SCREW_R, angle), STEEL))
    for n, angle in enumerate(WHEEL_SCREW["angles"], start=1):
        # D-007 wheel-to-stub screw (CH-056); the suffix matches the chassis checks.
        head = _ycyl(WHEEL_SCREW_HEAD["radius"], Y_OUT, Y_OUT + WHEEL_SCREW_HEAD["height"])
        shank = _ycyl(1.5, Y_OUT - WHEEL_SCREW["length"], Y_OUT)
        parts.append((f"SCREW_M3X6_{n}", _at_pcd(head + shank, WHEEL_SCREW["pcd_r"], angle), STEEL))
    return parts


def parts(hand: str = "L"):
    """(suffix, shape, colour) for one wheel in its own frame; the rim comes first."""
    return [
        ("RIM_PETG", rim(), FRAME_BLUE),
        ("CLAMP_RING_PETG", clamp_ring(), FRAME_BLUE),
        ("HUB_CAP_PETG", hub_cap(), GUNMETAL),
        (f"TYRE_TPU95A_{hand}", tyre(hand), RUBBER),
        *_hardware(),
    ]


def wheel(name: str = "WHEEL", hand: str = "L"):
    return Compound(label=name, children=[_paint(shape, f"{name}_{suffix}", colour) for suffix, shape, colour in parts(hand)])


def mounted_leaves(side: str, track: float, axle_z: float):
    """Flat, labelled leaves of one wheel placed on the chassis (|Y| = track / 2 + y).

    The right wheel is the left wheel mirrored in the XZ plane: identical rim,
    ring, cap and hardware, and the handed right tyre.
    """
    leaves = []
    for suffix, shape, colour in parts("L"):
        if side == "R":
            shape = shape.mirror(Plane.XZ)
            suffix = suffix.replace("TYRE_TPU95A_L", "TYRE_TPU95A_R")
        placed = shape.moved(Location((0.0, (track / 2.0) * (1.0 if side == "L" else -1.0), axle_z)))
        leaves.append(_paint(placed, f"WHEEL_{side}_{suffix}", colour))
    return leaves


def pair(track: float = 170.0):
    """Left and right wheels as mounted, standing on the floor: both chevrons lead toward +X."""
    return Compound(label="WHEEL_PAIR", children=[
        Compound(label=f"WHEEL_{side}", children=mounted_leaves(side, track, WHEEL_OD / 2.0)) for side in ("L", "R")
    ])


def on_floor():
    """The wheel standing on the floor, axis at Z 42 as in the chassis."""
    return wheel().moved(Location((0.0, 0.0, WHEEL_OD / 2.0)))
