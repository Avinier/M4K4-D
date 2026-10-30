"""Chassis primary frame for the print review: the three frame prints and every joint on them.

Left group, "1 assembled": the front module, rear module and battery hatch as they sit in the
robot, with the parts each frame joint holds (J04 carriers, J11A/J11B hatch and pack, J12 ballast,
J13 body bolts and pins, J15A IMU, J15B driver boards, the fuse holder). Right group, "2 exploded",
moved 260 mm along -Y: the same parts pulled apart along the direction each one is fitted, so
every insert, screw and seat can be seen. Printed frame parts are solid colours; bought parts
and the reviewed axle carriers are pale. Geometry is the final droid's, from makad-v1.step.py
(droid edits applied to the chassis tree), plus body v1's J13 hardware.
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

EXPLODE_Y = -260.0
PRINT = {
    "CHASSIS_FRAME_FRONT_MODULE": Color(0.36, 0.45, 0.52, 1.0),
    "CHASSIS_FRAME_REAR_MODULE": Color(0.62, 0.50, 0.36, 1.0),
    "BATTERY_TUB_BOTTOM_HATCH": Color(0.28, 0.33, 0.38, 1.0),
}
PALE = 0.35

# (group label, label prefixes, explode shift (x, y, z), pale)
GROUPS = [
    ("Front module (CH-001): deck, tub, front rails, crossmember, driver posts, fuse bracket",
     ("CHASSIS_FRAME_FRONT_MODULE",), (0.0, 0.0, 0.0), False),
    ("Rear module (CH-001): deck, rear rails, skid crossmember", ("CHASSIS_FRAME_REAR_MODULE",), (-35.0, 0.0, 0.0), False),
    ("J04 rail inserts, M3 x 6 in the rail ends (CH-061)", ("J04_RAIL_INSERT_M3_L_FRONT", "J04_RAIL_INSERT_M3_R_FRONT"),
     (0.0, 0.0, 0.0), False),
    ("J04 rail inserts, rear", ("J04_RAIL_INSERT_M3_L_REAR", "J04_RAIL_INSERT_M3_R_REAR"), (-35.0, 0.0, 0.0), False),
    ("J04 carrier L (reviewed with the axle) and its M3 x 8 screws",
     ("AXLE_MOTOR_CARRIER_L", "J04_CARRIER_SCREW_M3X8_L_"), (-17.0, 40.0, 0.0), True),
    ("J04 carrier R and its M3 x 8 screws", ("AXLE_MOTOR_CARRIER_R", "J04_CARRIER_SCREW_M3X8_R_"), (-17.0, -40.0, 0.0), True),
    ("J11A battery hatch (CH-011)", ("BATTERY_TUB_BOTTOM_HATCH",), (0.0, 0.0, -70.0), False),
    ("J11A hatch boss inserts, M3 x 6 (CH-077)", ("J11A_BOSS_INSERT_M3_",), (0.0, 0.0, 0.0), False),
    ("J11A hatch screws, M3 x 6 button (CH-076), from below", ("J11A_HATCH_SCREW_M3X6_",), (0.0, 0.0, -95.0), False),
    ("J11B pack, straps and foam: drop out with the hatch",
     ("BATTERY_CELL_", "BATTERY_END_STRAP_", "BATTERY_BMS_", "PACK_STRAP_", "PACK_FOAM_"), (0.0, 0.0, -70.0), True),
    ("J12 ballast bar (steel), fitted from below", ("BALLAST_STEEL_BAR",), (0.0, 0.0, -30.0), True),
    ("J12 ballast screws, M3 x 12 CSK from the deck top", ("BALLAST_M3_",), (0.0, 0.0, 30.0), True),
    ("J13 body bolts M4 x 12 and pins (body side)", ("BODY_CHASSIS_M4_SHANK_", "BODY_CHASSIS_M4_HEAD_", "BODY_CHASSIS_LOCATING_PIN_"),
     (0.0, 0.0, 45.0), True),
    ("J13 M4 x 8 deck inserts (CH-095, D-075)", ("J13_DECK_INSERT_",), (0.0, 0.0, 0.0), False),
    ("J13 front-left nut, in the body cassette", ("BODY_CHASSIS_M4_NUT_",), (0.0, 0.0, 20.0), True),
    ("J15A IMU board PCB-07 and its M2 x 5 screws", ("IMU_",), (0.0, 0.0, 30.0), True),
    ("J15B driver post inserts, M2.5 x 4 (CH-080, not bought)", ("DRIVER_POST_INSERT_M25_",), (0.0, 0.0, 0.0), False),
    ("J15B driver boards (Adafruit 3297) and M2.5 x 6 screws",
     ("DRV8833_", "DRIVER_SCREW_M25X6_"), (0.0, 0.0, 30.0), True),
    ("Fuse holder envelope on the D-032 bracket", ("PACK_ATOF_FUSE_HOLDER_ENVELOPE",), (0.0, 0.0, 30.0), True),
    ("Pod and keel inserts in the crossmembers (nose and keel reviews)",
     ("BALL_POD_HEATSET_INSERT_", "REAR_KEEL_HEATSET_INSERT_"), (0.0, 0.0, 0.0), False),
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
    leaves.update(_leaves(_robot._apply_droid_cuts(B.body_chassis_mount_hardware(), strict=False)))
    assembled = Compound(label="1 assembled", children=_group(leaves, False))
    exploded = Compound(label="2 exploded (260 mm to -Y)", children=_group(leaves, True))
    return {"shape": Compound(label="Chassis primary frame (print review)", children=[assembled, exploded])}
