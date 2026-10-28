"""Check head v1 datums and the three-screw disc interface against body v1."""

import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BODY_CAD = HERE.parents[2] / "02-body" / "v1" / "cad"
sys.path.insert(0, str(BODY_CAD))

import body_v1_model as body
import layout_model as head


def near(a, b, tolerance=1e-6):
    return math.isclose(a, b, abs_tol=tolerance)


def check():
    origin = body.HEAD_ORIGIN_IN_CHASSIS
    yaw_local = (head.PITCH_X, 0.0, head.BODY_TOP_Z)
    yaw_world = [origin[i] + yaw_local[i] for i in range(3)]
    disc_top = origin[2] + head.YAW_DISC_TOP_Z
    disc_bottom = disc_top - head.YAW_DISC_PLATE
    body_bosses = [body._yaw_polar(body.YAW_HUB_BOSS_R, deg) for deg in body.YAW_HUB_BOSS_DEG]
    head_holes = [
        (origin[0] + head.PITCH_X + head.YAW_HUB_BOLT_R * math.cos(math.radians(deg)),
         origin[1] + head.YAW_HUB_BOLT_R * math.sin(math.radians(deg)))
        for deg in head.YAW_HUB_BOLT_DEG
    ]
    alignment = [math.dist(hole, boss) for hole, boss in zip(head_holes, body_bosses)]
    pinion_outer_r = body.YAW_GEAR_MODULE * (body.YAW_GEAR_TEETH / 2 + 1)
    pinion_dx, pinion_dy = body.YAW_PINION_CENTER
    bolt_to_pinion_gap = min(
        math.hypot(
            head.YAW_HUB_BOLT_R * math.cos(math.radians(deg + yaw)) - pinion_dx,
            head.YAW_HUB_BOLT_R * math.sin(math.radians(deg + yaw)) - pinion_dy,
        ) - pinion_outer_r - 1.5
        for yaw in range(-62, 63)
        for deg in head.YAW_HUB_BOLT_DEG
    )
    result = {
        "yaw_datum_world_mm": yaw_world,
        "body_yaw_datum_mm": body.HEAD_YAW_DATUM,
        "head_disc_top_world_mm": disc_top,
        "body_disc_top_mm": body.YAW_DISC_TOP_Z,
        "disc_bottom_world_mm": disc_bottom,
        "hub_top_mm": body.YAW_GEAR_Z[1],
        "head_hole_to_body_boss_error_mm": alignment,
        "bolt_shaft_to_pinion_outer_gap_full_yaw_mm": bolt_to_pinion_gap,
        "screw_head_below_disc_top_mm": head.YAW_HUB_BOLT_RECESS - 1.65,
        "screw_insert_engagement_mm": 6.0 - (head.YAW_DISC_PLATE - head.YAW_HUB_BOLT_RECESS),
        "swept_head_to_disc_gap_mm": head.SWEEP_FLOOR_Z - head.YAW_DISC_TOP_Z,
        "head_crown_world_mm": origin[2] + head.CROWN_H,
    }
    assert all(near(a, b) for a, b in zip(yaw_world, body.HEAD_YAW_DATUM))
    assert near(disc_top, body.YAW_DISC_TOP_Z)
    assert near(disc_bottom, body.YAW_GEAR_Z[1])
    assert max(alignment) < 1e-6
    assert bolt_to_pinion_gap > 1.0
    assert head.YAW_HUB_BOLT_CLEARANCE_R >= 1.7
    assert result["screw_head_below_disc_top_mm"] > 0
    assert 3.5 < result["screw_insert_engagement_mm"] < 4.0
    assert result["swept_head_to_disc_gap_mm"] >= 4.0
    (HERE / "generated" / "integration-fit.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
