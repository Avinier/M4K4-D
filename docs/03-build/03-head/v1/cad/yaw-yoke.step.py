"""Compact inspection view of the head v1 yaw fork and turntable."""

from build123d import Compound
from layout_model import build_parts
import details, harness, inspection_scene, mass_layout, motion_envelope, optics


def gen_step():
    parts = build_parts(catalog=False)
    names = (
        "yaw_turntable_disc_flush",
        "yaw_yoke_leg_-55",
        "yaw_yoke_leg_55",
        "yaw_yoke_spine_inlay_-55",
        "yaw_yoke_spine_inlay_55",
        "pitch_trunnion_-49",
        "pitch_trunnion_49",
    )
    return {"shape": Compound(label="head_v1_yaw_yoke", children=[parts[name]["shape"] for name in names])}
