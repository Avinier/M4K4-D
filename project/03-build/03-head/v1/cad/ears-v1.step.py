"""Focused head-v1 ear assembly with both caps, inlays and service hardware."""

from build123d import Compound
from layout_model import build_parts
import details, harness, inspection_scene, mass_layout, motion_envelope, optics


def gen_step():
    parts = build_parts(catalog=False)
    sides = []
    for sign in (-1, 1):
        prefix = f"ear_{sign}_"
        names = [name for name in parts if name.startswith(prefix)]
        sides.append(Compound(label=f"ear_{sign}",
                              children=[parts[name]["shape"] for name in names]))
    sides.append(parts["connected_rolling_cradle_flange_ear_stalks"]["shape"])
    return {"shape": Compound(label="head_v1_ears", children=sides)}
