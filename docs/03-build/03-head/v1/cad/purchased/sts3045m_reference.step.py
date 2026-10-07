"""STS3045M envelope reference, mm; not a manufacturer STEP.

The dimensioned Feetech drawing in the user-supplied Evelta PDF (p. 6)
controls the case, mounting span, slot diameter and output shaft. Small boss,
case split and cable-stub details are visual estimates from the supplied photos.
Local origin is the output axis at the bottom plane of the case; +Z is the
shaft direction. Use the physical sample to confirm all mount coordinates.
"""

from build123d import Box, Compound, Cylinder, Pos
from cadgen import srgb

BODY_LENGTH = 36.0
BODY_WIDTH = 15.0
BODY_HEIGHT = 29.2
BODY_X_MIN = -12.0  # shaft is 6 mm off the case centre along its long axis
EAR_X_MIN, EAR_X_MAX = -18.4, 30.4
EAR_Z_MIN, EAR_Z_MAX = 19.7, 21.7
MOUNT_X = (-15.3, 27.3)
MOUNT_Y = (-3.75, 3.75)
MOUNT_DIAMETER = 4.2
SPLINE_DIAMETER = 5.9
SPLINE_TOP = 33.1


def named(shape, label, color):
    shape.label, shape.color = label, srgb(color)
    return shape


def box_between(x0, x1, y0, y1, z0, z1):
    return Pos((x0+x1)/2, (y0+y1)/2, (z0+z1)/2) * Box(x1-x0, y1-y0, z1-z0)


def gen_step():
    x0, x1 = BODY_X_MIN, BODY_X_MIN + BODY_LENGTH
    case = box_between(x0, x1, -BODY_WIDTH/2, BODY_WIDTH/2, 0, BODY_HEIGHT)
    # The drawing shows four open-ended Ø4.2 mounting slots, two per ear.
    # Their round ends are dimensioned; the narrow straight entrances extend
    # to the outside edges. Tab-to-case fillets are omitted.
    ears = box_between(EAR_X_MIN, EAR_X_MAX, -BODY_WIDTH/2, BODY_WIDTH/2,
                       EAR_Z_MIN, EAR_Z_MAX)
    for x in MOUNT_X:
        for y in MOUNT_Y:
            ears -= Pos(x, y, (EAR_Z_MIN+EAR_Z_MAX)/2) * Cylinder(
                MOUNT_DIAMETER/2, EAR_Z_MAX-EAR_Z_MIN+0.2)
            outer = EAR_X_MIN-0.1 if x < 0 else EAR_X_MAX+0.1
            ears -= box_between(min(x, outer), max(x, outer),
                                y-MOUNT_DIAMETER/2, y+MOUNT_DIAMETER/2,
                                EAR_Z_MIN-0.1, EAR_Z_MAX+0.1)
    # Cylindrical spline envelope is for clearance only; tooth count and
    # screw-thread geometry are documented but not modeled as mating teeth.
    spline = Pos(0, 0, (BODY_HEIGHT+SPLINE_TOP)/2) * Cylinder(
        SPLINE_DIAMETER/2, SPLINE_TOP-BODY_HEIGHT)
    spline -= Pos(0, 0, SPLINE_TOP-1.5) * Cylinder(1.5, 3.2)
    boss = Pos(0, 0, BODY_HEIGHT+0.15) * Cylinder(4.75, 0.3)
    # Short lead exit is intentionally an estimated visual feature; the
    # flexible 150 mm cable is excluded from rigid-fit checks.
    cable_stub = box_between(x0-1.4, x0+0.6, -9.5, -7.5, 3.0, 5.5)
    return Compound(label="STS3045M_REFERENCE_E_DRAWING_AND_PHOTOS", children=[
        named(case, "D_36x15x29p2_case", "#222428"),
        named(ears, "D_48p8_mount_span_four_open_D4p2_slots", "#27292D"),
        named(spline, "D_D5p9_25T_spline_envelope_M3_pilot", "#A8AAAB"),
        named(boss, "E_output_boss", "#303238"),
        named(cable_stub, "E_cable_exit_stub", "#1A1B1E"),
    ])
