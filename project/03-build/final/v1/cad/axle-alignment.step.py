"""Left axle stack, D-071: the motor-alignment step beside the finished stack.

Left group, "1 align": carrier, motor, housing, cap and housing screws with the printed
alignment plug (CH-089, orange) in the bearing seat, and the two 2 mm keys (steel rods)
reaching the motor face screws through the cap, housing slots and the plug's notches.
Right group, "2 built", moved 70 mm along +X: the same housing refitted with the bearings
and the Ø21-flange stub, as it runs. Wheel off in both. Geometry is the final droid's,
from makad-v1.step.py (droid edits applied to the chassis tree).
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

ALIGN = ("AXLE_MOTOR_CARRIER_L", "AXLE_BEARING_HOUSING_L", "AXLE_BEARING_CAP_L", "AXLE_CAP_SCREW_M3X16_L_",
         "AXLE_PLATE_INSERT_M3_L_", "AXLE_MOTOR_SCREW_M3X6_L_", "MOTOR_L_MOT3001", "MOTOR_L_OUTPUT_SHAFT")
BUILT = ALIGN + ("BEARING_688ZZ_L_", "WHEEL_L_STUB_SHAFT_8MM", "WHEEL_L_SET_SCREW")


def _leaves(node, loc=Location(), out=None):
    out = [] if out is None else out
    kids = list(node.children) if getattr(node, "children", None) else []
    here = loc * node.location
    if kids:
        for kid in kids:
            _leaves(kid, here, out)
    else:
        placed = node.moved(loc)
        placed.label, placed.color = node.label, node.color
        out.append(placed)
    return out


def _pick(parts, prefixes, shift=None):
    picked = []
    for part in parts:
        if (part.label or "").startswith(prefixes):
            moved = part.moved(Location(shift)) if shift else part
            moved.label, moved.color = part.label, part.color
            picked.append(moved)
    return picked


def gen_step():
    parts = _leaves(_robot._apply_droid_cuts(B.chassis_v1_reference(), strict=False))
    plug = _robot.axle_alignment_plug(1)
    plug.color = Color(0.86, 0.52, 0.14, 1.0)
    keys = []
    for n, x in enumerate((-_robot.AXLE_FIX["key_x"], _robot.AXLE_FIX["key_x"]), start=1):
        key = _robot._axle_cyl(1, 1.0, 73.5, 115.0, x, 0.0)
        key.label, key.color = f"HEX_KEY_2MM_{n}", Color(0.72, 0.75, 0.75, 1.0)
        keys.append(key)
    align = Compound(label="1 align: plug in, face screws tightened", children=_pick(parts, ALIGN) + [plug] + keys)
    built = Compound(label="2 built: bearings and stub in", children=_pick(parts, BUILT, (70.0, 0.0, 0.0)))
    return {"shape": Compound(label="Axle stack L (D-071)", children=[align, built])}
