"""Separate review view of the shared chassis-v1 frame print units.

Concept geometry only. Joint sizes and print fusion await the lab process and
the axle-carrier J04 handoff. Coordinates follow body_chassis_model.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

from build123d import Compound

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import body_chassis_model as M


PAINT = M._paint
FRAME_COLOR = "#86A1A8"
RAIL_COLOR = "#87949A"
CROSS_COLOR = "#C38A47"
HATCH_COLOR = "#707D82"
MOTOR_COLOR = "#B7BFC0"
B = M._block
BATTERY_COLOR = "#4A9B6A"


def rail_y(side: str) -> tuple[float, float]:
    sign = 1.0 if side == "L" else -1.0
    return tuple(sorted((sign * (RAIL_Y - RAIL_HALF_WIDTH), sign * (RAIL_Y + RAIL_HALF_WIDTH))))


def deck(region: str):
    """Review-view name for the shared chassis print unit."""
    label = "FS_DECK_REAR" if region == "REAR" else "FS_DECK_FRONT_BATTERY_TUB"
    return PAINT(M.frame_deck(region), label, FRAME_COLOR)


def rail(region: str, side: str):
    """Review-view name for the shared chassis rail geometry."""
    return PAINT(M.frame_rail(region, side), f"FS_RAIL_{side}_{region}", RAIL_COLOR)


def crossmember(region: str):
    """Review-view name for the shared chassis crossmember geometry."""
    return PAINT(M.frame_crossmember(region), f"FS_CROSSMEMBER_{region}", CROSS_COLOR)


def hatch():
    """Review-view name for the shared four-screw bottom hatch."""
    hatch_part = M.battery_tub(include_walls=False).children[0]
    return PAINT(hatch_part, "FS_BATTERY_HATCH_FOUR_M3", HATCH_COLOR)


def nonprint_context():
    """Motor and pack envelopes explain the two apparent top-view voids."""
    parts = []
    for side in ("L", "R"):
        sign = 1.0 if side == "L" else -1.0
        parts.append(M._cylinder(12.5, 60.0, (0.0, sign * 39.0, M.AXLE_Z),
                                 f"REFERENCE_ONLY_MOTOR_{side}_ENVELOPE", MOTOR_COLOR, 0.32, "y"))
    bx, by, bz = M.BATTERY_CENTER
    dx, dy, dz = M.BATTERY_SIZE
    parts.append(PAINT(B(bx - dx / 2, bx + dx / 2,
                         by - dy / 2, by + dy / 2,
                         bz - dz / 2, bz + dz / 2),
                       "REFERENCE_ONLY_BATTERY_ENVELOPE", BATTERY_COLOR, 0.28))
    for index, (x, y) in enumerate(M.BODY_MOUNT_POINTS, start=1):
        parts.append(M._cylinder(5.0, 18.0, (x, y, 43.0),
                                 f"REFERENCE_ONLY_BODY_M4_SOCKET_PATH_{index}",
                                 MOTOR_COLOR, 0.12))
    return parts


def gen_step():
    parts = [deck("REAR"), deck("FRONT")]
    parts += [rail(region, side) for region in ("REAR", "FRONT") for side in ("L", "R")]
    parts += [crossmember("REAR"), crossmember("FRONT"), hatch()]
    parts += nonprint_context()
    return {"shape": Compound(label="FRAME_SPLIT_STUDY_J04_OPEN", children=parts)}
