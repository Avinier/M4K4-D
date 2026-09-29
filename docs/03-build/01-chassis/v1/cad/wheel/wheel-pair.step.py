"""Chassis v1 left and right drive wheels as mounted, with handed tyres (D-008, D-009)."""

from wheel_model import pair


def gen_step():
    return {"shape": pair()}
