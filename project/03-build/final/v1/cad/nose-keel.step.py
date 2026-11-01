"""Nose (ball transfer) and rear keel for the print review: their seven prints and every joint on them.

Left group, "1 assembled": the pod seat, sensor lid and touch cap on the front crossmember, and the
keel, wear shoe, TCRT bezel and shims under the rear crossmember, as they sit in the robot, with
the parts each joint holds (J07A caster, J07B pod screws, J08A range sensor, J08B Hall board,
magnet and springs, J08C lid screw; J09A keel screws, J09B TCRT, J10A shoe screw, J10B guard
lips). Right group, "2 exploded", moved 150 mm along -Y: the same parts pulled apart along the
direction each one is fitted, so every insert, screw and seat can be seen. The seven prints are
solid colours; bought parts and the frame modules (already reviewed) are pale. Geometry is the
final droid's, from makad-v1.step.py (droid edits applied to the chassis tree).
"""

from pathlib import Path
import importlib.util
import sys

from build123d import Color, Compound, Location


def _load(name, filename):
    # Load a sibling by path; registering it in sys.modules puts it in cadgen's source hash.
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_robot = _load("makad_v1_entry", "makad-v1.step.py")
import body_v1_model as B  # noqa: E402  (path set up by the entry)

EXPLODE_Y = -150.0
PRINT = {
    "BALL_POD_PRINTED_SEAT": Color(0.36, 0.45, 0.52, 1.0),
    "BALL_POD_SENSOR_LID": Color(0.46, 0.55, 0.62, 1.0),
    "BALL_NOSE_TOUCH_CAP": Color(0.86, 0.84, 0.76, 1.0),
    "REAR_KEEL_FACETED_BODY": Color(0.66, 0.63, 0.55, 1.0),
    "REAR_KEEL_REPLACEABLE_WEAR_SHOE": Color(0.28, 0.33, 0.38, 1.0),
    "REAR_TCRT_BEZEL_WITH_GUARDS": Color(0.55, 0.50, 0.40, 1.0),
    "REAR_TCRT_HEIGHT_SHIM_1": Color(0.40, 0.47, 0.52, 1.0),
    "REAR_TCRT_HEIGHT_SHIM_2": Color(0.40, 0.47, 0.52, 1.0),
}
PALE = 0.35
POD = (40.0, 0.0, 0.0)      # J07B: the pod comes off the crossmember face forward
KEEL = (0.0, 0.0, -40.0)    # J09A: the keel drops off the crossmember underside


def _at(base, dx=0.0, dy=0.0, dz=0.0):
    return (base[0] + dx, base[1] + dy, base[2] + dz)


# (group label, label prefixes, explode shift (x, y, z), pale)
GROUPS = [
    # Context, reviewed with the frame.
    ("Front module (CH-001, frame review): crossmember face and pod pilots", ("CHASSIS_FRAME_FRONT_MODULE",), (0.0, 0.0, 0.0), True),
    ("Rear module (CH-001, frame review): skid crossmember, keel pilots, tie lug", ("CHASSIS_FRAME_REAR_MODULE",), (0.0, 0.0, 0.0), True),
    # Nose.
    ("Pod seat (CH-002)", ("BALL_POD_PRINTED_SEAT",), POD, False),
    ("J07B pod inserts in the crossmember, M3 x 6 (CH-033)", ("BALL_POD_HEATSET_INSERT_",), (0.0, 0.0, 0.0), False),
    ("J07B pod screws, M3 x 8 button (CH-032), driven -X from the pocket", ("BALL_POD_M3_",), _at(POD, 22.0), True),
    ("J07A caster seat inserts, M3 x 6 (CH-063), pressed from the seat face", ("BALL_SEAT_HEATSET_INSERT_",), POD, False),
    ("J07A caster base (Pololu 2691), seats on the pod from below", ("BALL_TRANSFER_PURCHASED_3HOLE_FLANGE",), _at(POD, dz=-25.0), True),
    ("J07A caster screws, M3 x 8 button (CH-031), from below through the web", ("BALL_M3_",), _at(POD, dz=-45.0), True),
    ("J07A caster housing, ball and rollers: unsnap downward first",
     ("BALL_TRANSFER_PURCHASED_HOUSING", "BALL_TRANSFER_POM_BALL", "BALL_TRANSFER_ROLLER_"), _at(POD, dz=-70.0), True),
    ("J08A range sensor GP2Y0A21YK0F (CH-018) and its soldered J10-8 lead", ("GP2Y0A21YK0F_STEP", "GP2Y_J10_8_SOLDERED_LEAD"),
     _at(POD, dz=40.0), True),
    ("J08B Hall board PCB-15 (CH-064, CH-019): lifts out of its slot after the sensor", ("BALL_NOSE_HALL_",), _at(POD, dz=25.0), True),
    ("J08B return springs (CH-066)", ("BALL_NOSE_RETURN_SPRING_",), _at(POD, 12.0), True),
    ("J08B touch cap (CH-007), slides forward off the nose", ("BALL_NOSE_TOUCH_CAP",), _at(POD, 30.0), False),
    ("J08B cap magnet (CH-065), in the cap wall", ("BALL_NOSE_MAGNET_",), _at(POD, 30.0), True),
    ("J08C sensor lid (CH-003): 12 mm forward, then up", ("BALL_POD_SENSOR_LID",), _at(POD, 12.0, dz=60.0), False),
    ("J08C lid screw, M2 x 8 countersunk thread-forming (CH-062)", ("BALL_POD_LID_M2X8",), _at(POD, 12.0, dz=80.0), True),
    # Keel.
    ("Keel body (CH-008)", ("REAR_KEEL_FACETED_BODY",), KEEL, False),
    ("J09A keel inserts in the crossmember, M3 x 6 (CH-067)", ("REAR_KEEL_HEATSET_INSERT_",), (0.0, 0.0, 0.0), False),
    ("J09A keel screws, M3 x 30 socket head (CH-034), from below", ("REAR_KEEL_M3X30_",), _at(KEEL, dz=-45.0), True),
    ("J09B TCRT5000 and its soldered J10-10 lead (CH-020): down through the pocket",
     ("TCRT5000_REAR_", "TCRT_REAR_LEAD_", "TCRT_REAR_J10_10_"), _at(KEEL, dz=-12.0), True),
    ("J09B height shims (CH-068)", ("REAR_TCRT_HEIGHT_SHIM_",), _at(KEEL, dz=-24.0), False),
    ("J09B/J10B TCRT bezel with guard lips (CH-010)", ("REAR_TCRT_BEZEL_WITH_GUARDS",), _at(KEEL, dz=-34.0), False),
    ("J09B bezel screw, M2 x 10 thread-forming (CH-069), from below", ("REAR_TCRT_BEZEL_M2X10",), _at(KEEL, dz=-48.0), True),
    ("J10A wear shoe (CH-009), slides out forward", ("REAR_KEEL_REPLACEABLE_WEAR_SHOE",), _at(KEEL, 28.0), False),
    ("J10A shoe screw, M2 x 6 thread-forming (CH-070), from +Y", ("REAR_KEEL_SHOE_M2X6",), _at(KEEL, dy=18.0), True),
]


def _leaves(node, loc=Location(), out=None):
    """Every leaf with its world placement. OCC moves (_shifted) share geometry; build123d
    moved() on an attached leaf would deep-copy the whole tree."""
    out = {} if out is None else out
    kids = list(node.children) if getattr(node, "children", None) else []
    here = loc * node.location
    if kids:
        for kid in kids:
            _leaves(kid, here, out)
    else:
        out[node.label or ""] = (node, loc)
    return out


def _place(node, loc, shift, pale):
    part = _robot._shifted(node, Location(shift) * loc if shift else loc)
    part.label = node.label
    if node.label in PRINT:
        part.color = PRINT[node.label]
    else:
        c = tuple(node.color) if node.color is not None else (0.7, 0.7, 0.7, 1.0)
        part.color = Color(c[0], c[1], c[2], PALE if pale else c[3])
    return part


def _group(leaves, explode):
    groups = []
    for title, prefixes, shift, pale in GROUPS:
        picked = [(label, nl) for label, nl in leaves.items() if label.startswith(prefixes)]
        assert picked, f"no parts for {title}"
        move = (shift[0], shift[1] + EXPLODE_Y, shift[2]) if explode else None
        groups.append(Compound(label=title, children=[_place(n, l, move, pale) for _, (n, l) in sorted(picked)]))
    return groups


def gen_step():
    leaves = _leaves(_robot._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    assembled = Compound(label="1 assembled", children=_group(leaves, False))
    exploded = Compound(label="2 exploded (150 mm to -Y)", children=_group(leaves, True))
    return {"shape": Compound(label="Nose and rear keel (print review)", children=[assembled, exploded])}
