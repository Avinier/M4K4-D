"""Complete head v1 on the latest body v1 and chassis v1."""

from pathlib import Path
import sys

from build123d import Compound, Location
from layout_model import build_parts
from inspection_scene import parts_scene
import details, harness, mass_layout, motion_envelope, optics

HERE = Path(__file__).resolve().parent
BODY_CAD = HERE.parents[2] / "02-body" / "v1" / "cad"
if str(BODY_CAD) not in sys.path:
    sys.path.insert(0, str(BODY_CAD))

from body_v1_model import build_body_assembly, HEAD_ORIGIN_IN_CHASSIS, yaw_drive_moving_local


def gen_step():
    head = Compound(label="Head v1", children=[
        *parts_scene(build_parts()).children,
        yaw_drive_moving_local(),
    ]).moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    return {"shape": Compound(label="Head v1 on body v1 and chassis v1", children=[
        build_body_assembly(), head,
    ])}
