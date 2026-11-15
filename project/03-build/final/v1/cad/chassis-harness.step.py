"""Focused review of the chassis wires installed by makad-v1.step.py."""

import module_checks
from chassis_harness import build_chassis_harness


def gen_step():
    return {"shape": build_chassis_harness(module_checks.load_entry())}
