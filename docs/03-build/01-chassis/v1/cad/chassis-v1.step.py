"""Build the chassis v1 scope extracted from the Layout 02 source."""

from body_chassis_model import build_chassis_v1


def gen_step():
    return {"shape": build_chassis_v1()}
