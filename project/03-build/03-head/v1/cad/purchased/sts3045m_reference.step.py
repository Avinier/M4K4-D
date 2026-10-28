"""STS3045M envelope reference, mm; not a manufacturer STEP.

The dimensioned Feetech drawing in the user-supplied Evelta PDF (p. 6)
controls the case, mounting span, slot diameter and output shaft. Dimensioned
values are marked D. Values marked S are scaled from the same drawing (the
raster is anisotropic: 29.2 px/mm along the case, 24.2-24.8 px/mm across
it; the dimensioned features reproduce to <= 0.2 mm at those scales).
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
# S: the open slot neck in the top view is 2.4 mm wide, centred on each row.
SLOT_NECK_WIDTH = 2.4
SPLINE_DIAMETER = 5.9
SPLINE_TOP = 33.1
# S: the output boss under the spline is Ø10.4 x 0.3 in the top/side views.
BOSS_DIAMETER, BOSS_HEIGHT = 10.4, 0.3
# S: the lead exits the shaft-end face (-X), centred on the case width, as a
# 1.4 mm flange (6.0 wide x Z 0.9..4.9) plus a 2.1 mm nozzle (5.1 wide x Z
# 1.7..4.2), 3.5 mm proud in total (side and bottom views agree).
CABLE_FLANGE = (1.4, 6.0, 0.9, 4.9)
CABLE_NOZZLE = (2.1, 5.1, 1.7, 4.2)


def named(shape, label, color):
    shape.label, shape.color = label, srgb(color)
    return shape


def box_between(x0, x1, y0, y1, z0, z1):
    return Pos((x0+x1)/2, (y0+y1)/2, (z0+z1)/2) * Box(x1-x0, y1-y0, z1-z0)


def gen_step():
    x0, x1 = BODY_X_MIN, BODY_X_MIN + BODY_LENGTH
    case = box_between(x0, x1, -BODY_WIDTH/2, BODY_WIDTH/2, 0, BODY_HEIGHT)
    # The drawing shows four open-ended Ø4.2 mounting slots, two per ear.
    # Their round ends are dimensioned (D); the 2.4 mm necks run out to the
    # ear's outer edge (S). Tab-to-case fillets are omitted.
    ears = box_between(EAR_X_MIN, EAR_X_MAX, -BODY_WIDTH/2, BODY_WIDTH/2,
                       EAR_Z_MIN, EAR_Z_MAX)
    for x in MOUNT_X:
        for y in MOUNT_Y:
            ears -= Pos(x, y, (EAR_Z_MIN+EAR_Z_MAX)/2) * Cylinder(
                MOUNT_DIAMETER/2, EAR_Z_MAX-EAR_Z_MIN+0.2)
            outer = EAR_X_MIN-0.1 if x < 0 else EAR_X_MAX+0.1
            ears -= box_between(min(x, outer), max(x, outer),
                                y-SLOT_NECK_WIDTH/2, y+SLOT_NECK_WIDTH/2,
                                EAR_Z_MIN-0.1, EAR_Z_MAX+0.1)
    # Cylindrical spline envelope is for clearance only; tooth count and
    # screw-thread geometry are documented but not modeled as mating teeth.
    spline = Pos(0, 0, (BODY_HEIGHT+SPLINE_TOP)/2) * Cylinder(
        SPLINE_DIAMETER/2, SPLINE_TOP-BODY_HEIGHT)
    spline -= Pos(0, 0, SPLINE_TOP-1.5) * Cylinder(1.5, 3.2)
    boss = Pos(0, 0, BODY_HEIGHT+BOSS_HEIGHT/2) * Cylinder(
        BOSS_DIAMETER/2, BOSS_HEIGHT)
    # Rigid lead exit on the shaft-end face; the flexible 150 mm cable leaves
    # its tip along -X and needs its own routed clearance.
    fl, fw, fz0, fz1 = CABLE_FLANGE
    nl, nw, nz0, nz1 = CABLE_NOZZLE
    cable_stub = box_between(x0-fl, x0+0.01, -fw/2, fw/2, fz0, fz1)
    cable_stub += box_between(x0-fl-nl, x0-fl+0.01, -nw/2, nw/2, nz0, nz1)
    return Compound(label="STS3045M_REFERENCE_E_DRAWING_AND_PHOTOS", children=[
        named(case, "D_36x15x29p2_case", "#222428"),
        named(ears, "D_48p8_mount_span_four_open_D4p2_slots", "#27292D"),
        named(spline, "D_D5p9_25T_spline_envelope_M3_pilot", "#A8AAAB"),
        named(boss, "S_D10p4_output_boss", "#303238"),
        named(cable_stub, "S_shaft_end_cable_exit", "#1A1B1E"),
    ])
