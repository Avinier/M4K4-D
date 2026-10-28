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
        "pitch_trunnion_D6x12_pin",
        "pitch_trunnion_bearing_MR106ZZ",
        "pitch_trunnion_retainer",
        "pitch_horn_25T_disc",
    )
    return {"shape": Compound(label="head_v1_yaw_yoke", children=[parts[name]["shape"] for name in names]
                      + [d["shape"] for name, d in parts.items() if name.startswith(("yaw_leg_to_disc_M2x6", "pitch_trunnion_retainer_M2x4"))])}
