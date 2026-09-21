"""Named chassis frames. All coordinates in the axle-origin chassis frame."""

from __future__ import annotations

from lib import params as P


def frames(support="ball"):
    """Return {name: (x, y, z)} for the displayed pose.

    `support` is `ball` or `caster`. Contact x is identical. Trail is U and
    only shifts the caster swivel axis, not F_FRONT_CONTACT.
    """
    x_c = P.FRONT_CONTACT_X
    shim = P.BALL_SHIM if support == "ball" else P.CASTER_SHIM
    trail = P.CASTER_TRAIL_DISPLAY if support == "caster" else 0.0
    return {
        "F_GROUND": (0.0, 0.0, 0.0),
        "F_AXLE": (0.0, 0.0, P.H_AXLE),
        "F_WHEEL_L": (0.0, P.WHEEL_Y_L, P.H_AXLE),
        "F_WHEEL_R": (0.0, P.WHEEL_Y_R, P.H_AXLE),
        "F_FRONT_CONTACT": (x_c, 0.0, 0.0),
        "F_MOUNT_FRONT": (x_c, 0.0, P.H_AXLE),  # deck height; shim hangs below
        "F_SKID_CONTACT": (-P.SKID_REACH, 0.0, 0.0),
        "F_CLIFF_F": (x_c + P.CLIFF_F_LEAD, 0.0, P.CLIFF_STANDOFF),
        "F_CLIFF_L": (25.0, P.WHEEL_Y_L - P.WHEEL_WIDTH / 2 - 8.0, P.CLIFF_STANDOFF),
        "F_CLIFF_R": (-P.SKID_REACH, 0.0, P.CLIFF_STANDOFF),  # rides the skid
        "F_IR_OPTICAL": (x_c, 0.0, 28.0),
        "F_BUMPER": (x_c + 28.0, 0.0, 28.0),
        "F_IMU": (15.0, 0.0, 58.0),
        "F_BAY": (P.BALLAST_X, 0.0, P.BALLAST_Z),
        "F_NECK": P.F_NECK,
        "F_BODY": (40.0, 0.0, 70.0),
        "F_SWIVEL": (x_c + trail, 0.0, P.CASTER_NATIVE_H / 2) if support == "caster" else None,
        "shim_mm": shim,
        "trail_mm_U": trail,
    }
