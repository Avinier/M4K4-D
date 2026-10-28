"""Chassis v1 drive wheel: PETG rim, printed TPU chevron tyre, clamp ring (D-004, D-005)."""

from wheel_model import on_floor


def gen_step():
    return {"shape": on_floor()}
