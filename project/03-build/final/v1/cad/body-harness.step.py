"""Focused review of the D-109 body wires installed by makad-v1.step.py."""

import module_checks
from body_harness import build_body_harness


def gen_step():
    return {"shape": build_body_harness(module_checks.load_entry())}
