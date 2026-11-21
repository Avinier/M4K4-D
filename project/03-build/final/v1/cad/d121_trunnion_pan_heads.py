"""D-121: HD-010 pitch-pivot retainer screws become M2 x 3 Phillips pan heads.

M2 hex-socket button heads (ISO 7380, Ø3.5 x 1.1) cannot be bought by the
builder; the available article is an M2 machine screw with a Phillips pan head
(ISO 7045 class: dk <= 4.0, k <= 1.6). The D-051 retainer heads finish at the
-Y leg's outer face (Y -58.0), which the skin passes at 0.98 mm at the roll
stops, so a taller head may not stand proud. Instead of moving the bearing
seat, each of the retainer plate's two screw lugs gets a 0.4 mm deep, R2.6
counterbore from its top face: the head seats 0.4 mm lower and a k 1.6 head
finishes 0.1 mm under the leg face. The plate keeps 0.6 mm under each head
(three 0.2 mm layers) and its full 1.0 mm over the bearing's outer ring: the
cut stays 5.9 mm from the pivot axis, outside the MR106ZZ (R5.0).

Length: an M2 x 4 seated 0.4 mm lower would reach the insert pocket's floor
(0.0 mm, and its +/-0.24 length tolerance could bottom it), so the screw is
M2 x 3: 2.4 mm in the 3 mm insert (the head's minimum engagement, 1.2 d) and
1.0 mm short of the pocket floor.

Head frame (R/Y, neutral pose); the droid entry moves shapes by
HEAD_ORIGIN_IN_CHASSIS. HD-006/HD-011/HD-032 also take pan heads (M2 x 6, the
builder's article) but keep their button-head models: fit checks on received parts.
"""
from build123d import Axis, Cylinder, Location
import feetech as fe
import layout_model as m

T = fe.TRUNNION
FLOOR_Y = T['recess_floor_y']                  # -55.7: bearing outer ring / plate inner face
PLATE_TOP_Y = FLOOR_Y - T['plate_t']           # -56.7: the plate's outer face
LEG_FACE_Y = -(fe.LEG_INNER_Y + 6)             # -58.0
CB_DEPTH = .4
CB_R = T['lug_r'] + T['recess_clear']          # 2.6: the whole lug top, no printed sliver
SEAT_Y = PLATE_TOP_Y + CB_DEPTH                # -56.3
PAN = dict(dk=4.0, k=1.6)                      # ISO 7045 M2 maxima
SCREW_LEN = 3.                                 # M2 x 3 (D-051 had M2 x 4)


def pan_screw(x, z):
    """M2 x 3 pan head envelope: Ø4.0 x 1.6 cylinder head (outward -Y), Ø2 shank."""
    head = Cylinder(PAN['dk'] / 2, PAN['k']).moved(Location((0, 0, PAN['k'] / 2)))
    shank = Cylinder(1, SCREW_LEN).moved(Location((0, 0, -SCREW_LEN / 2)))
    s = (head + shank).rotate(Axis.X, 90)      # local +Z -> world -Y, as button_screw(..., 'y', -1)
    return s.moved(Location((x, SEAT_Y, z)))


def counterbore_tool():
    tool = None
    for x, z in m.trunnion_screw_points():
        c = m.yspan(CB_R, PLATE_TOP_Y - .2, SEAT_Y, x, z)
        tool = c if tool is None else tool + c
    return tool


def screws():
    return {deg: pan_screw(x, z) for (x, z), deg in zip(m.trunnion_screw_points(), T['screw_deg'])}


REMOVES = [r"pitch_trunnion_retainer_M2x4_(240|300)"]


def cuts(entry):
    loc = Location(entry.HEAD_ORIGIN_IN_CHASSIS)
    return [(r"pitch_trunnion_retainer", counterbore_tool().moved(loc))]


def inserts(entry):
    paint, loc = entry._tag, Location(entry.HEAD_ORIGIN_IN_CHASSIS)
    return [('Fasteners', paint(s.moved(loc), f'D121_TRUNNION_RETAINER_M2X3_PAN_{deg:g}', '#555b5a'))
            for deg, s in screws().items()]
