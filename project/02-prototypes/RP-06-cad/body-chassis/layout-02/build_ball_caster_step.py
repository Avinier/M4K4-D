"""Author the Pololu 1" ball caster (item 2691, plastic rollers; 2692 is the same envelope
with 3x7x3 mm bearings) as a STEP in its installed orientation.

Sources: Pololu drawing 2691-dimensions.pdf (base O34, holes O3.2 on a 12.2 mm-side
triangle = O14.08 bolt circle, 29 mm overall, 8.8 mm base, O7 x 8 rollers, 3 mm pins).
The 3/8" `Pololu Ball Caster.STEP` reference is the structural template only: its ball
is 9.5 mm, so it cannot be scaled to this part.

Frame: ball contact at the origin, +Z up, mounting face (flange top) at Z 29, ball
centre at Z 12.7. Run with the text-to-cad 0.4.28 runtime:
    python build_ball_caster_step.py
"""
import math
from pathlib import Path

from build123d import Axis, Box, Compound, Cylinder, Location, Plane, Polygon, Sphere, export_step, revolve
from build123d import Align

OUT = Path(__file__).resolve().parent.parent / "layout-01" / "references" / "purchased" / "pololu_ball_caster_1in_2691.step"

BALL_R = 12.7
BALL_Z = BALL_R
TOTAL_H = 29.0
BASE_R, BASE_H = 17.0, 8.8
SHELL_R = 14.25  # drum radius (the revolved profile adds 0.35 at the base joint)
SHELL_Z0 = 8.5
BASE_Z0 = TOTAL_H - BASE_H  # 20.2
HOLE_R, HOLE_BC_R = 1.6, 12.2 / math.sqrt(3.0)  # side of the hole triangle 12.2 mm
ROLLER_R, ROLLER_L = 3.5, 8.0
ROLLER_ELEV_DEG = 55.0  # polar angle from +Z at the ball centre: puts the rollers flush at the shell/base joint


def cyl(r, z0, z1, x=0.0, y=0.0):
    return Cylinder(r, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))


def box_at(radial0, radial1, tang, z0, z1, az_deg):
    """Box spanning radial0..radial1 from the axis, `tang` wide, at azimuth az_deg."""
    b = Box(radial1 - radial0, tang, z1 - z0).moved(Location(((radial0 + radial1) / 2.0, 0.0, (z0 + z1) / 2.0)))
    return b.rotate(Axis.Z, az_deg)


def build():
    ball_c = Location((0.0, 0.0, BALL_Z))
    ball = Sphere(BALL_R).moved(ball_c)
    cavity = Sphere(BALL_R + 0.2).moved(ball_c)

    d = BALL_R + ROLLER_R
    pol = math.radians(ROLLER_ELEV_DEG)
    roller_z = BALL_Z + d * math.cos(pol)
    roller_r = d * math.sin(pol)
    roller_az = [60.0 + 120.0 * k for k in range(3)]
    win_z0, win_z1 = roller_z - ROLLER_R - 0.3, roller_z + ROLLER_R + 0.3

    base = cyl(BASE_R, BASE_Z0, TOTAL_H) - cavity
    for k in range(3):
        a = math.radians(120.0 * k)
        base = base - cyl(HOLE_R, BASE_Z0 - 1.0, TOTAL_H + 1.0, HOLE_BC_R * math.cos(a), HOLE_BC_R * math.sin(a))
    for az in roller_az:
        base = base - box_at(8.0, BASE_R + 1.0, ROLLER_L + 0.6, win_z0, win_z1, az)  # roller windows
    base = base - box_at(BASE_R - 4.5, BASE_R + 1.0, 8.0, TOTAL_H - 3.0, TOTAL_H + 0.1, 90.0)  # snap-tab relief on the mounting rim

    rollers = []
    for az in roller_az:
        a = math.radians(az)
        r = Cylinder(ROLLER_R, ROLLER_L).rotate(Axis.Y, 90.0).rotate(Axis.Z, az + 90.0)
        rollers.append(r.moved(Location((roller_r * math.cos(a), roller_r * math.sin(a), roller_z))))

    # Shell: revolved dome shoulder (thin lip on the ball, rounding out to the drum), then the
    # ball cavity, roller windows and three shallow snap slits.
    rim = BALL_R + 0.2 + 0.0
    a_r, b_z = 1.7, 5.0
    top = SHELL_Z0 + b_z
    pts = [(0.0, SHELL_Z0), (12.9, SHELL_Z0)]
    for i in range(1, 40):
        t = math.radians(90.0 * i / 39.0)
        pts.append((12.9 + a_r * math.sin(t), top - b_z * math.cos(t)))
    pts += [(SHELL_R + 0.35, BASE_Z0), (0.0, BASE_Z0)]
    shell = revolve(Plane.XZ * Polygon(*pts, align=None), axis=Axis.Z) - cavity
    for az in roller_az:
        shell = shell - box_at(8.0, SHELL_R + 2.0, ROLLER_L + 0.6, win_z0, BASE_Z0 + 0.01, az)
    for az in (30.0, 150.0, 270.0):
        shell = shell - box_at(SHELL_R - 0.5, SHELL_R + 1.0, 0.8, top + 1.0, BASE_Z0 - 0.8, az)

    ball.label = "BALL_TRANSFER_POM_BALL"
    base.label = "BALL_TRANSFER_PURCHASED_3HOLE_FLANGE"
    shell.label = "BALL_TRANSFER_PURCHASED_HOUSING"
    for k, r in enumerate(rollers, start=1):
        r.label = f"BALL_TRANSFER_ROLLER_{k}"
    return Compound(label="POLOLU_BALL_CASTER_1IN_2691", children=[ball, base, shell, *rollers])


if __name__ == "__main__":
    part = build()
    b = part.bounding_box()
    print("bbox X[%.2f,%.2f] Y[%.2f,%.2f] Z[%.2f,%.2f]" % (b.min.X, b.max.X, b.min.Y, b.max.Y, b.min.Z, b.max.Z))
    export_step(part, str(OUT))
    print("wrote", OUT)
