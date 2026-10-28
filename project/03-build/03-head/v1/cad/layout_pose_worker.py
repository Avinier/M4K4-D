"""Spawn-safe exact layout pair sweep."""

from functools import lru_cache

import layout_model as model
from cad_cache import load_parts


_parts = None
_pairs = None
_external = None


@lru_cache(maxsize=4096)
def _bounds(shape):
    box = shape.bounding_box()
    return tuple(box.min), tuple(box.max)


def _overlap(a, b):
    amin, amax = _bounds(a)
    bmin, bmax = _bounds(b)
    if any(amax[i] <= bmin[i] + 1e-7 or bmax[i] <= amin[i] + 1e-7
           for i in range(3)):
        return 0.0
    return sum(max(0, shape.volume) for shape in model.pieces(a.intersect(b)))


def _pose(shape, frame, roll, pitch):
    if frame == "R":
        shape = shape.rotate(model.ROLL_AXIS, roll)
    if frame in "RP":
        shape = shape.rotate(model.PITCH_AXIS, pitch)
    return shape


def initialize(pairs, external):
    global _parts, _pairs, _external
    _parts = load_parts(catalog=False)
    _pairs = pairs
    _external = external


def check_pose(angles):
    roll, pitch = angles
    needed = {name for pair in _pairs for name in pair} | set(_external)
    posed = {name: _pose(_parts[name]["shape"], _parts[name]["frame"], roll, pitch)
             for name in needed}
    hits = []
    for a, b in _pairs:
        volume = _overlap(posed[a], posed[b])
        if volume > 1e-4:
            hits.append(dict(roll=roll, pitch=pitch, a=a, b=b,
                             volume_mm3=round(volume, 4)))
    minz = min(_bounds(posed[name])[0][2] for name in _external)
    return hits, minz
