"""Spawn-safe exact motion-grid worker for check_revision.py."""

import layout_model as model
from functools import lru_cache
from cad_cache import load_parts
from harness import routes
from inspection_scene import posed


_motion = None
_pairs = None
_jackets = None


@lru_cache(maxsize=8192)
def _bounds(shape):
    box = shape.bounding_box()
    return tuple(box.min), tuple(box.max)


def _overlap(a, b):
    amin, amax = _bounds(a)
    bmin, bmax = _bounds(b)
    if any(amax[i] <= bmin[i] + 1e-6 or bmax[i] <= amin[i] + 1e-6 for i in range(3)):
        return 0.0
    return sum(max(0, solid.volume) for solid in model.pieces(a.intersect(b)))


def initialize(pairs):
    global _motion, _pairs, _jackets
    parts = load_parts(catalog=False)
    _motion = {name: part for name, part in parts.items() if part["kind"] == "physical"}
    _pairs = pairs
    harness, _ = routes()
    _jackets = {name: part for name, part in harness.items() if part["kind"] == "jacket"}


def check_pose(pose):
    roll, pitch = pose
    shapes = {name: posed(part["shape"], part["frame"], roll, pitch, 0)
              for name, part in _motion.items()}
    hits, pinches = [], []
    for a, b in _pairs:
        volume = _overlap(shapes[a], shapes[b])
        if volume > 1e-4:
            hits.append(dict(roll=roll, pitch=pitch, a=a, b=b,
                             volume_mm3=round(volume, 5)))
    for name, part in _jackets.items():
        jacket = posed(part["shape"], part["frame"], roll, pitch, 0)
        for target, shape in shapes.items():
            volume = _overlap(jacket, shape)
            if volume > 1e-4:
                pinches.append(dict(roll=roll, pitch=pitch, branch=name, part=target,
                                    volume_mm3=round(volume, 5)))
    return hits, pinches
