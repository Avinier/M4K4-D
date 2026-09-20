"""Buildable STEP entry for RP-03 integrated body/chassis Layout 02."""

from body_chassis_model import build_assembly


def gen_step():
    return {"shape": build_assembly(), "params": "body-chassis.params.js"}
