"""Head v1 on body v1 and chassis v1 as built: every part opaque.

The inspection models draw the head skin, body shell and wheel-arch pods at
alpha 0.28 so the packaging reads through them. This entry is for judging the
robot's appearance: same geometry as head-v1-integrated.step.py, all colours
opaque, and space reservations, harness routes and physics overlays left out
because they are not parts.
"""

from pathlib import Path
import sys

from build123d import Color, Compound, Location
from layout_model import build_parts
from inspection_scene import parts_scene
import details, harness, mass_layout, motion_envelope, optics

HERE = Path(__file__).resolve().parent
BODY_CAD = HERE.parents[2] / "02-body" / "v1" / "cad"
if str(BODY_CAD) not in sys.path:
    sys.path.insert(0, str(BODY_CAD))

from body_v1_model import build_body_assembly, HEAD_ORIGIN_IN_CHASSIS, yaw_drive_moving_local

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
    head = Compound(label="Head v1", children=[
        *parts_scene(build_parts()).children,
        yaw_drive_moving_local(),
    ]).moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    robot = Compound(label="Head v1 on body v1 and chassis v1 (presentation)", children=[
        build_body_assembly(), head,
    ])
    return {"shape": _opaque(robot)}
