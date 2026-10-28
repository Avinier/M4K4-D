"""Photo-derived 5 V 3010 hydraulic fan, for body-v1 fit and visual review.

The measured catalogue envelope is 30 x 30 x 10 mm. Local XY is the fan face,
local Z runs from the mounting face (0) to the intake face (10). The 900 mm
flexible USB lead is deliberately represented by a short exit stub: its routed
path and USB plug are installation-dependent, and body v1 uses a cut/reterminated
two-wire W41 lead instead. No manufacturer drawing was available. Millimetres.
"""

from build123d import Axis, Box, Compound, Cylinder, Polygon, Pos, extrude, fillet
from cadgen import srgb

SIZE = 30.0
THICKNESS = 10.0
CORNER_RADIUS = 2.0  # estimated from photos
OPENING_DIAMETER = 27.6  # estimated
HOLE_PITCH = 24.0  # existing body-v1 pattern; verify on purchased sample
HOLE_DIAMETER = 2.7  # estimated through-hole
HUB_DIAMETER = 14.0  # estimated from photos
BLADE_COUNT = 7

BLACK = srgb("#202226")
ROTOR = srgb("#17191C")
LABEL = srgb("#E9E9E7")
WIRE = srgb("#353739")


def _named(shape, name, color):
    shape.label, shape.color = name, color
    return shape


def _disk(radius, z0, z1):
    return Pos(0, 0, (z0 + z1) / 2) * Cylinder(radius, z1 - z0)


def _bezier(a, control, b, steps=8):
    """Sample a quadratic planform curve for a closed blade sketch."""
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * control[0] + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * control[1] + t * t * b[1])
            for t in (i / steps for i in range(steps + 1))]


def gen_step():
    frame = Box(SIZE, SIZE, THICKNESS)
    frame = fillet(frame.edges().filter_by(Axis.Z), CORNER_RADIUS)
    frame = Pos(0, 0, THICKNESS / 2) * frame
    frame -= _disk(OPENING_DIAMETER / 2, -0.1, THICKNESS + 0.1)
    for x in (-HOLE_PITCH / 2, HOLE_PITCH / 2):
        for y in (-HOLE_PITCH / 2, HOLE_PITCH / 2):
            frame -= Pos(x, y, THICKNESS / 2) * Cylinder(HOLE_DIAMETER / 2, THICKNESS + 0.2)

    # Rear three-spoke support and stationary motor cup. The rotor is a separate
    # group; no bearing detail or blade section is asserted by the photographs.
    rear_cup = _disk(HUB_DIAMETER / 2 + 0.8, 0.8, 3.0)
    for angle in (0, 120, 240):
        spoke = Pos(10.0, 0, 1.4) * Box(9.0, 2.2, 2.8)
        rear_cup += spoke.rotate(Axis.Z, angle)

    hub = _disk(HUB_DIAMETER / 2, 3.0, 8.6)
    # A tapered, swept planform gives the seven curved vanes visible in all
    # three reference views. Blade thickness and pitch are visual estimates.
    blades = []
    outline = (_bezier((6.2, -1.1), (9.9, -4.0), (13.1, -2.2))[:-1]
               + _bezier((13.1, -2.2), (13.8, 0.4), (11.7, 1.5))[:-1]
               + _bezier((11.7, 1.5), (8.3, 3.3), (6.2, 1.2))[:-1]
               + [(6.2, 1.2)])
    for index in range(BLADE_COUNT):
        blade = Pos(0, 0, 4.2) * extrude(Polygon(*outline, align=None), amount=2.3)
        blade = blade.rotate(Axis.Z, index * 360.0 / BLADE_COUNT)
        blades.append(_named(blade, f"curved_rotor_blade_{index + 1}", ROTOR))

    # Thin round label on the visible hub; this face is the intake side.
    sticker = _disk(6.7, 8.6, 8.7)
    # Short factory strain-relief/lead exit; full 900 mm cable is not a rigid
    # fan feature and is omitted from the mounting STEP.
    stub = Pos(9.5, -16.5, 2.0) * Box(2.0, 8.0, 2.0)

    return Compound(label="DC5V_3010_HYDRAULIC_USB_FAN", children=[
        _named(frame, "black_30mm_frame_four_mounting_holes", BLACK),
        _named(rear_cup, "rear_three_spoke_motor_support", BLACK),
        _named(hub, "rotor_hub", ROTOR),
        *blades,
        _named(sticker, "hub_label_disk", LABEL),
        _named(stub, "two_wire_exit_stub", WIRE),
    ])
