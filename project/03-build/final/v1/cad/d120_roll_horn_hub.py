"""D-120: roll output, Probots 25T disc horn + turned aluminium hub collar.

Replaces the goBILDA 4001-0025-0006 clamping coupler (HD-004), which cannot be
bought in India, in the same 17 mm between the roll servo's spline face and
the bearing cartridge. Head frame (R, roll axis +X); shapes here are head-local
and the droid entry moves them by HEAD_ORIGIN_IN_CHASSIS.

- Horn: the same Probots 25T aluminium disc horn as the pitch output (HD-002,
  `E` listing values in feetech.HORN): hub on the spline 0.3 mm off the boss,
  exactly where the coupler's spline face was, so the spline engagement (3.3)
  and the ISO 4762 M3 x 5 centre screw (head on the web at the old coupler
  floor, X -78.1, 3.8 mm into the output) are unchanged.
- Collar (turned 6061): Ø20 x 4 flange on the horn disc, Ø12 x 8.5 shaft,
  Ø6 H7 bore through (the M3 centre-screw head, Ø5.5, passes through it).
  Four M2 tapped holes on the horn's Ø14 PCD; two radial M3 tapped holes
  from +Y for set screws.
- Horn to collar: four ISO 7380 M2 x 6 button heads from the servo side
  through the horn's M3 tapped holes (M2 passes M3's minor diameter freely)
  into the flange: 2 mm horn + 4 mm flange. M3 heads (Ø5.5-5.7) at r 7 would
  overlap the horn's own Ø10 hub; the Ø3.5 M2 head clears it, and front-driven
  screws would sit under the collar's shaft. Assemble horn and collar on the
  bench, then press them onto the spline and drive the centre screw down the bore.
- Collar to spindle: two ISO 4029 M3 x 3 cup points from +Y (the old clamp
  screw's access direction, open at neutral) on a 0.5 mm flat ground on the
  spindle's rear end (M016), facing +Y at neutral roll. Roll zero is trimmed
  by the servo offset: the spline indexes in 14.4 deg steps and the flat fixes
  the collar to the spindle.
"""
import math
from build123d import Location
import feetech as fe
import layout_model as m

Y, Z = m.ROLL_Y, m.ROLL_Z
H = fe.HORN
HORN_HUB_X = fe.COUPLER_SPLINE_FACE_X                 # -82.6: hub face, 0.3 off the boss
HORN_DISC_X = (HORN_HUB_X + H['hub_t'], HORN_HUB_X + H['hub_t'] + H['disc_t'])   # (-80.1, -78.1)
COLLAR = dict(flange_r=10., flange_t=4., shaft_r=6., bore_r=3.0, front_x=fe.COUPLER_FRONT_X,
              m2_tap_r=1.0, m3_tap_r=1.5, set_x=(-72.3, -68.4), density=2.70e-3)
COLLAR_X = (HORN_DISC_X[1], COLLAR['front_x'])          # (-78.1, -65.6)
FLANGE_FRONT_X = COLLAR_X[0] + COLLAR['flange_t']       # -74.1
SPINDLE_FLAT = dict(depth=.5, x=(fe.SPINDLE_X[0] - .1, -66.0))   # +Y side; ends 0.4 inside the collar, 2.9 short of the rear bearing (X-63.1)
M2X6 = 6.
SET_LEN = 3.


def _hole_yz(deg):
    a = math.radians(deg)
    return Y + H['pcd_r'] * math.cos(a), Z + H['pcd_r'] * math.sin(a)


def horn():
    """Probots 25T disc horn on the roll spline (same model as the pitch horn)."""
    x0, (d0, d1) = HORN_HUB_X, HORN_DISC_X
    s = m.axial(H['hub_r'], H['hub_t'], ((x0 + d0) / 2, Y, Z)) + m.axial(H['disc_r'], H['disc_t'], ((d0 + d1) / 2, Y, Z))
    bore = d1 - H['web'] - x0
    s = s - m.axial(H['bore_r'], bore + .2, (x0 + bore / 2 - .1, Y, Z))
    s = s - m.axial(H['screw_r'], H['web'] + .2, (d1 - H['web'] / 2, Y, Z))
    for deg in H['holes_deg']:
        y, z = _hole_yz(deg)
        s = s - m.axial(1.5, H['disc_t'] + .2, ((d0 + d1) / 2, y, z))
    return s


def collar():
    c = COLLAR
    x0, x1 = COLLAR_X
    s = m.axial(c['flange_r'], c['flange_t'], ((x0 + FLANGE_FRONT_X) / 2, Y, Z))
    s = s + m.axial(c['shaft_r'], x1 - FLANGE_FRONT_X + .01, ((FLANGE_FRONT_X + x1) / 2 - .005, Y, Z))
    s = s - m.axial(c['bore_r'], x1 - x0 + .2, ((x0 + x1) / 2, Y, Z))
    for deg in H['holes_deg']:
        y, z = _hole_yz(deg)
        s = s - m.axial(c['m2_tap_r'], c['flange_t'] + .2, ((x0 + FLANGE_FRONT_X) / 2, y, z))
    for x in c['set_x']:
        y0, y1 = 1.5, c['shaft_r'] + .2              # drilled and tapped through into the bore
        s = s - m.axial(c['m3_tap_r'], y1 - y0, (x, Y + (y0 + y1) / 2, Z), 'y')
    return s


def horn_screws():
    """ISO 7380 M2 x 6 from the servo side, heads on the horn disc's back face."""
    out = {}
    for deg in H['holes_deg']:
        y, z = _hole_yz(deg)
        out[deg] = m.button_screw(HORN_DISC_X[0], y, z, 'x', -1, M2X6)
    return out


def set_screws():
    """ISO 4029 M3 x 3 cup points from +Y, tips on the spindle flat."""
    tip = Y + 3. - SPINDLE_FLAT['depth']
    return [m.axial(1.5, SET_LEN, (x, tip + SET_LEN / 2, Z), 'y') for x in COLLAR['set_x']]


def spindle_flat_tool():
    """Head-frame cut: 0.5 mm flat on the spindle's +Y side over the collar zone."""
    x0, x1 = SPINDLE_FLAT['x']
    return m.block(x0, x1, Y + 3. - SPINDLE_FLAT['depth'], Y + 3.5, Z - 3.5, Z + 3.5)


REMOVES = [r"roll_coupler_goBILDA_4001_0025_0006", r"roll_coupler_clamp_M4x10"]


def cuts(entry):
    loc = Location(entry.HEAD_ORIGIN_IN_CHASSIS)
    return [(r"rolling_spindle_6mm", spindle_flat_tool().moved(loc))]


def inserts(entry):
    paint, loc = entry._tag, Location(entry.HEAD_ORIGIN_IN_CHASSIS)
    out = [('Roll assembly', paint(horn().moved(loc), 'D120_ROLL_HORN_25T_PROBOTS', '#b7bfc0')),
           ('Roll assembly', paint(collar().moved(loc), 'D120_ROLL_HUB_COLLAR_6061', '#9aa3a6'))]
    out += [('Fasteners', paint(s.moved(loc), f'D120_ROLL_HORN_TO_HUB_M2X6_{deg:g}', '#555b5a'))
            for deg, s in horn_screws().items()]
    out += [('Fasteners', paint(s.moved(loc), f'D120_ROLL_HUB_SET_M3X3_{i}', '#555b5a'))
            for i, s in enumerate(set_screws(), 1)]
    return out
