"""Makad v1, the whole robot: chassis v1, body v1 and head v1 from their live sources."""

from pathlib import Path
import re
import sys

from build123d import Box, Compound, Location

BUILD = Path(__file__).resolve().parents[3]
HEAD_CAD = BUILD / "03-head" / "v1" / "cad"
BODY_CAD = BUILD / "02-body" / "v1" / "cad"


def _use_subsystem_paths():
    """Put head then body CAD first on sys.path; head names win over body ones."""
    for path in (str(BODY_CAD), str(HEAD_CAD)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)


_use_subsystem_paths()
from layout_model import build_parts
from inspection_scene import parts_scene
import details, harness, mass_layout, motion_envelope, optics
from body_v1_model import (build_body_assembly, chassis_v1_reference,
                           HEAD_ORIGIN_IN_CHASSIS, yaw_drive_moving_local)


def build_robot(label="Makad v1"):
    # cadgen restores sys.path after loading the entry, but the head source
    # imports cad_cache, relief_worker and run_checks lazily inside build_parts().
    _use_subsystem_paths()
    head = Compound(label="Head v1", children=[
        *parts_scene(build_parts()).children,
        yaw_drive_moving_local(),
    ]).moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    robot = Compound(label=label, children=[
        chassis_v1_reference(), build_body_assembly(), head,
    ])
    return _group_custom_pcbs(_apply_droid_cuts(robot))


# Droid-level CAD changes. From 2026-10-14 the droid's CAD changes are made in
# this folder, not in the subsystem sources (04-pcbs/README.md#rules), so the
# subsystem checks do not see them. Each entry cuts a world-frame box
# (x0, x1, y0, y1, z0, z1) from every part whose label fully matches.
DROID_CUTS = [
    # D-059: PCB-15 component relief behind the nose Hall board, 0.9 mm deep, open at
    # the top and into the lead groove. The board's ends (local Y 0-0.8, 5.2-6.0)
    # still bear on the slot's back wall.
    (r"BALL_POD_PRINTED_SEAT", (125.7, 126.6, 7.8, 12.2, 30.3, 35.01)),
]


def _cut_box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))


def _cut_parts(node, parent_location, hits):
    children = list(node.children) if getattr(node, "children", None) else []
    if children:
        here = parent_location * node.location
        kept = [_cut_parts(child, here, hits) for child in children]
        if all(k is c for k, c in zip(kept, children)):
            return node
        return _relabel(node.label, kept, node.location, node.color)
    cuts = [box for pattern, box in DROID_CUTS if re.fullmatch(pattern, node.label or "")]
    if not cuts:
        return node
    part = node
    for box in cuts:
        hits[box] += 1
        part = part - _cut_box(*box).moved(parent_location.inverse())
    part.label, part.color = node.label, node.color
    return part


def _apply_droid_cuts(robot):
    hits = {box: 0 for _, box in DROID_CUTS}
    robot = _cut_parts(robot, Location(), hits)
    missing = [pattern for pattern, box in DROID_CUTS if not hits[box]]
    assert not missing, f"droid cut labels not found: {missing}"
    return robot


# Custom boards (04-pcbs/README.md register), pulled out of the subsystem trees
# into one "Custom PCBs" group so they can be shown or isolated together.
# Each pattern must fully match the label of a node in the subsystem tree; the
# node moves whole, keeping its global placement. PCB-01 is a bought BMS
# (Robocraze TIFPS0629, D-019) and stays on the pack.
CUSTOM_PCBS = [
    ("PCB-02 charger, latch and pack sense", r"PCB02_CHARGE_AND_SYSTEM_POWER"),
    ("PCB-03 motor gate and head 5 V rail", r"PCB03_MOTOR_GATE_AND_HEAD_RAIL"),
    ("PCB-04 branch converters", r"PCB04_BRANCH_CONVERTERS"),
    ("PCB-05 audio front end", r"PCB05_AUDIO_FRONT_END|PCB05_CONNECTORS"),
    ("PCB-06 PDM microphone boards x4", r"PDM_MIC_(FRONT|REAR)_[LR]"),
    ("PCB-07 base IMU", r"IMU_PCB07"),
    ("PCB-08 yaw junction", r"YAW_JUNCTION_PCB08"),
    ("PCB-09 C0 link adapter", r"C0_LINK_ADAPTER_PCB09"),
    ("PCB-10 C3 controller carrier", r"C3_CARRIER_PCB10_WITH_DEVKITC"),
    ("PCB-11 status LED carrier", r"status_LED_(PCB08_carrier_5x5|WS2812B_2020)"),
    # Only the ESP32-S3-Zero module is drawn; the carrier board is not modelled yet.
    ("PCB-12 C2 head controller", r"C2_ESP32_S3_Zero_23_5x18_footprint"),
    ("PCB-13 charge inlet", r"CHARGE_INLET_PCB13"),
    ("PCB-14 yaw rotor joiners x3", r"PCB14_JOINER_(BOARD|LOWER_ZIF|UPPER_ZIF)_[1-3]"),
    ("PCB-15 nose Hall carrier", r"BALL_NOSE_HALL_(CARRIER_PCB|DRV5055A3_SOT23)"),
]
# Printed frame parts inside a board group stay where they are.
STAYS_IN_PLACE = re.compile(r"BODY_FRAME_\w+")
_PCB_RULES = [(name, re.compile(pattern)) for name, pattern in CUSTOM_PCBS]


def _board_group(label):
    return next((name for name, rule in _PCB_RULES if rule.fullmatch(label or "")), None)


def _relabel(label, children, location, color=None):
    group = Compound(label=label, children=children)
    group.location = location
    if color is not None:
        group.color = color
    return group


def _pull_pcbs(node, parent_location, found):
    """Return node without its board parts (None if nothing is left); collect them in found."""
    here = parent_location * node.location
    children = list(node.children) if getattr(node, "children", None) else []
    board = _board_group(node.label)
    if board:
        stays = [c for c in children if STAYS_IN_PLACE.fullmatch(c.label or "")]
        if not stays:
            node.location = here
            found[board].append(node)
            return None
        moved = [c for c in children if all(c is not s for s in stays)]
        found[board].append(_relabel(node.label, moved, here))
        return _relabel(node.label, stays, node.location)
    if not children:
        return node
    kept = [_pull_pcbs(child, here, found) for child in children]
    if all(k is c for k, c in zip(kept, children)):
        return node
    kept = [k for k in kept if k is not None]
    return _relabel(node.label, kept, node.location, node.color) if kept else None


def _group_custom_pcbs(robot):
    found = {name: [] for name, _ in CUSTOM_PCBS}
    rest = _pull_pcbs(robot, Location(), found)
    missing = [name for name, parts in found.items() if not parts]
    assert not missing, f"custom PCB labels not found in the subsystem trees: {missing}"
    pcbs = Compound(label="Custom PCBs", children=[
        Compound(label=name, children=parts) for name, parts in found.items()
    ])
    return _relabel(robot.label, [*rest.children, pcbs], robot.location)


def gen_step():
    return {"shape": build_robot()}
