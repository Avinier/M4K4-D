"""One independent relief pose, using exact BReps from the parent build."""

from cad_cache import _decode
from layout_model import PITCH_AXIS, ROLL_AXIS, pieces


TARGETS = (
    "main_octagonal_skin", "ear_-1_ridged_inner_mount",
    "ear_1_ridged_inner_mount", "ear_-1_hollow_removable_cap",
    "ear_1_hollow_removable_cap", "connected_rolling_cradle_flange_ear_stalks",
)
SUPPORTS = ("yaw_yoke_leg_-55", "yaw_yoke_leg_55", "yaw_turntable_disc_flush")
_shapes = None
_bounds = None


def initialize(encoded):
    global _shapes, _bounds
    _shapes = {name: _decode(raw) for name, raw in encoded.items()}
    _bounds = {}
    for name in TARGETS:
        box = _shapes[name].bounding_box()
        _bounds[name] = tuple(box.min), tuple(box.max)


def sample_bounds(pose):
    roll, pitch = pose
    result = {}
    for support_name in SUPPORTS:
        tool = _shapes[support_name].rotate(PITCH_AXIS, -pitch).rotate(ROLL_AXIS, -roll)
        box = tool.bounding_box()
        tmin, tmax = tuple(box.min), tuple(box.max)
        for name in TARGETS:
            smin, smax = _bounds[name]
            if any(smax[i] < tmin[i] or tmax[i] < smin[i] for i in range(3)):
                continue
            boxes = []
            for piece in pieces(_shapes[name].intersect(tool)):
                if piece.volume > 1e-5:
                    bounds = piece.bounding_box()
                    boxes.append((tuple(bounds.min), tuple(bounds.max)))
            if boxes:
                result[name, support_name] = boxes
    return result
