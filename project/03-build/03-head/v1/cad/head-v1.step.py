"""Head v1 inspection assembly, adapted from RP-06 Layout 04."""

from layout_model import build_parts
from inspection_scene import parts_scene
import details, harness, mass_layout, motion_envelope, optics


def gen_step():
    return {"shape": parts_scene(build_parts())}
