"""Makad v1 as built: every part opaque.

The inspection models draw the head skin, body shell and wheel-arch pods at
alpha 0.28 so the packaging reads through them. This entry is for judging the
robot's appearance: same geometry as makad-v1.step.py, all colours opaque, and
space reservations, harness routes and physics overlays left out because they
are not parts.
"""

from pathlib import Path
import importlib.util
import sys

from build123d import Color, Compound

# Load the sibling entry by path; its file name is not an importable module name.
# Registering it in sys.modules puts it in cadgen's source hash.
_spec = importlib.util.spec_from_file_location(
    "makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
_robot = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _robot
_spec.loader.exec_module(_robot)

# Leaf or group labels that are reservations or overlays, not parts.
NOT_PARTS = ("RESERVE", "OVERLAY", "PHYSICS", "HARNESS", "KEEP_OUT", "KEEPOUT", "SWEEP", "ENVELOPE_CHECK")


def _is_part(label):
    label = (label or "").upper()
    return not any(token in label for token in NOT_PARTS)


def _opaque(shape, inherited_rgb=None):
    """Drop non-part leaves and set alpha 1 on the rest, keeping each colour."""
    color = getattr(shape, "color", None)
    rgb = tuple(color)[:3] if color is not None else inherited_rgb
    children = list(shape.children) if getattr(shape, "children", None) else []
    if children:
        kept = [_opaque(child, rgb) for child in children if _is_part(child.label)]
        kept = [child for child in kept if child is not None]
        if not kept:
            return None
        group = Compound(label=shape.label, children=kept)
        group.location = shape.location
        return group
    shape.color = Color(*(rgb or (0.68, 0.72, 0.74)), 1.0)
    return shape


def gen_step():
    return {"shape": _opaque(_robot.build_robot("Makad v1 (presentation)"))}
