"""Source-built frame variant with XC330 pad removed and HS cradle joined."""
from build123d import Compound
import body_v1_model as b
from feetech_yaw_cradle import parts


def gen_step():
    mount=parts()
    frame=b.body_primary_frame()-b._block(*b.YAW_SERVO_BRACKET)
    frame+=mount['cradle']
    frame.label='BODY_FRAME_FEETECH_YAW_CANDIDATE'
    return Compound(label='FEETECH_YAW_FRAME_CANDIDATE_NOT_RELEASED',
                    children=[frame,mount['strap']])
