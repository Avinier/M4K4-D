"""Makad v1 as built: every part opaque, in its real finish colour.

The inspection models draw the head skin, body shell and wheel-arch pods at
alpha 0.28 so the packaging reads through them, and colour parts so they can
be told apart. This entry is for judging the robot's appearance: same geometry
as makad-v1.step.py, all colours opaque and replaced by the real filament,
paint or hardware colour from finish_colours.py (printguide.md §4), and space
reservations, harness routes and physics overlays left out because they are
not parts.
"""

from pathlib import Path
import importlib.util
import sys

from build123d import Color, Compound


def _load(name, filename):
    # Load a sibling by path; registering it in sys.modules puts it in cadgen's source hash.
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_robot = _load("makad_v1_entry", "makad-v1.step.py")
_finish = _load("makad_v1_finish_colours", "finish_colours.py")

# Leaf or group labels that are reservations or overlays, not parts.
NOT_PARTS = ("RESERVE", "OVERLAY", "PHYSICS", "HARNESS", "KEEP_OUT", "KEEPOUT", "SWEEP", "ENVELOPE_CHECK")


def _is_part(label):
    label = (label or "").upper()
    return not any(token in label for token in NOT_PARTS)


def _opaque(shape, inherited_rgb=None, path=""):
    """Drop non-part leaves; give the rest their finish colour at alpha 1.

    A leaf that no finish rule matches keeps its model colour.
    """
    color = getattr(shape, "color", None)
    rgb = tuple(color)[:3] if color is not None else inherited_rgb
    children = list(shape.children) if getattr(shape, "children", None) else []
    if children:
        here = f"{path}/{shape.label or ''}"
        kept = [_opaque(child, rgb, here) for child in children if _is_part(child.label)]
        kept = [child for child in kept if child is not None]
        if not kept:
            return None
        group = Compound(label=shape.label, children=kept)
        group.location = shape.location
        return group
    finish = _finish.finish_for(shape.label, path)
    if finish:
        rgb = _finish.rgb(finish)
    shape.color = Color(*(rgb or (0.68, 0.72, 0.74)), 1.0)
    return shape


def gen_step():
    return {"shape": _opaque(_robot.build_robot("Makad v1 (presentation)"))}
