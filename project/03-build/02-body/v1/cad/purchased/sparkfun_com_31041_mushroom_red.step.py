"""Photo-derived envelope for SparkFun COM-31041 / Tanotis 7447052877909.

This is a placement and clearance reference, not a manufacturer drawing.
Millimetres. The switch axis is Z; the gasket's panel-contact face is Z=0,
with the actuator toward +Z and the terminals toward -Z. The nut is shown
partway along the barrel, as in the supplied photographs.
"""

from math import sqrt

from build123d import Box, Compound, Cylinder, Pos, RegularPolygon, Sphere, Torus, extrude
from cadgen import srgb

# Published: nominal 16 mm panel-mount threaded body. All remaining dimensions
# are estimates scaled from the supplied photographs (including the US quarter).
HEAD_D = 25.2
HEAD_RIM_Z = 8.20
HEAD_EDGE_BOTTOM_Z = 6.20
HEAD_CROWN_H = 0.80
STEM_D = 10.5
COLLAR_D = 18.4
BARREL_D = 15.6
BARREL_BOTTOM_Z = -14.2
NUT_AF = 20.0
NUT_BOTTOM_Z = -6.0
NUT_H = 2.6
TERMINAL_PITCH = 8.8
TERMINAL_BOTTOM_Z = -22.8

RED = srgb("#B70A28")
CHROME = srgb("#C6C8C7")
NUT_METAL = srgb("#ABA497")
BLUE = srgb("#087DB0")
SCREW = srgb("#C9BEA4")
GASKET = srgb("#343E42")


def _cylinder(diameter, z0, z1, name, color):
    shape = Pos(0, 0, (z0 + z1) / 2) * Cylinder(diameter / 2, z1 - z0)
    shape.label, shape.color = name, color
    return shape


def gen_step():
    parts = []

    # The crown is a shallow spherical cap; its large radius makes the face
    # nearly flat, matching the side and straight-on product photographs.
    head_radius = HEAD_D / 2
    sphere_radius = (head_radius**2 + HEAD_CROWN_H**2) / (2 * HEAD_CROWN_H)
    sphere_center_z = HEAD_RIM_Z - (sphere_radius - HEAD_CROWN_H)
    cap = (Pos(0, 0, sphere_center_z) * Sphere(sphere_radius)) & (
        Pos(0, 0, HEAD_RIM_Z + HEAD_CROWN_H / 2)
        * Box(HEAD_D + 2, HEAD_D + 2, HEAD_CROWN_H)
    )
    head = _cylinder(HEAD_D, HEAD_EDGE_BOTTOM_Z, HEAD_RIM_Z,
                     "red_mushroom_head", RED) + cap
    head.label, head.color = "red_mushroom_head", RED
    parts.append(head)
    parts.append(_cylinder(STEM_D, 4.10, HEAD_EDGE_BOTTOM_Z,
                           "red_actuator_stem", RED))
    parts.append(_cylinder(COLLAR_D, 0.75, 4.10, "front_chrome_bezel", CHROME))

    # Simplified cosmetic thread crests, not a screw-thread specification.
    barrel = _cylinder(BARREL_D, BARREL_BOTTOM_Z, 0,
                       "m16_nominal_threaded_barrel", CHROME)
    for i in range(7):
        z = -13.15 + i * 1.35
        barrel = barrel + Pos(0, 0, z) * Torus(BARREL_D / 2 - 0.02, 0.27)
    barrel.label, barrel.color = "m16_nominal_threaded_barrel", CHROME
    parts.append(barrel)

    gasket = _cylinder(18.1, 0, 0.75, "front_rubber_gasket", GASKET)
    gasket -= _cylinder(15.8, -0.2, 0.95, "tool", GASKET)
    gasket.label, gasket.color = "front_rubber_gasket", GASKET
    parts.append(gasket)

    nut = extrude(RegularPolygon(NUT_AF / sqrt(3), 6), amount=NUT_H)
    nut = Pos(0, 0, NUT_BOTTOM_Z) * nut
    nut -= _cylinder(15.9, NUT_BOTTOM_Z - 0.2,
                     NUT_BOTTOM_Z + NUT_H + 0.2, "tool", NUT_METAL)
    nut.label, nut.color = "hex_locknut_20_af_estimated", NUT_METAL
    parts.append(nut)

    parts.append(_cylinder(15.4, -16.2, BARREL_BOTTOM_Z,
                           "rear_chrome_shell", CHROME))
    parts.append(_cylinder(14.2, -18.0, -16.2,
                           "blue_switch_insulator", BLUE))
    for sign, name in ((-1, "left"), (1, "right")):
        x = sign * TERMINAL_PITCH / 2
        lug = Pos(x, 0, -20.3) * Box(3.0, 4.2, 5.0)
        lug.label, lug.color = f"{name}_screw_terminal_lug", CHROME
        parts.append(lug)
        screw = Pos(x, 0, TERMINAL_BOTTOM_Z - 0.5) * Cylinder(1.55, 1.0)
        screw.label, screw.color = f"{name}_terminal_screw_head", SCREW
        parts.append(screw)

    return Compound(label="sparkfun_COM_31041_red_mushroom_pushbutton",
                    children=parts)
