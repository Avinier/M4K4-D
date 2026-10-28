"""Focused body-frame review export with its assembled fasteners."""

from build123d import Compound
from cadgen import step

from body_v1_model import body_primary_frame, body_chassis_mount_hardware, body_frame_joint_hardware


@step(out="body-frame-v1.step")
def body_frame_v1():
    return Compound(label="BODY_FRAME_V1_FIT_REVIEW", children=[
        body_primary_frame(), body_chassis_mount_hardware(), body_frame_joint_hardware(),
    ])


if __name__ == "__main__":
    body_frame_v1()
