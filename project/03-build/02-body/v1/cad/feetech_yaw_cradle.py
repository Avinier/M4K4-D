"""Provisional frame-integral cradle for the original-height ST3215-HS.

This uses the purchased STEP envelope and a shifted Pi/PCB-09 layout. The
clamp screw pattern, print strength and assembly path are not released.
"""
from build123d import Compound
import body_v1_model as b


def parts():
    # 0.2 mm below the STEP base; apply a measured compressible liner in build.
    floor = b._block(-23.0, 29.0, 24.0, 52.4, 89.0, 92.0)
    left = b._block(-23.0, -21.0, 24.0, 52.4, 91.9, 131.0)
    right = b._block(27.0, 29.0, 24.0, 52.4, 91.9, 131.0)
    back = b._block(-23.0, 29.0, 50.4, 52.4, 91.9, 124.0)
    # Two ribs merge into the existing fan web above its R14 opening. This
    # makes the cradle part of the printed body frame. The front retainer is
    # still a location placeholder; its fasteners and insertion path are open.
    arms = [b._block(x0, x1, 51.8, 57.2, 123.8, 131.0)
            for x0, x1 in ((2.0, 8.0), (24.0, 30.0))]
    cradle = floor + left + right + back
    for arm in arms:
        cradle += arm
    # Removable stainless front retaining band; 1 mm in Y, 8 mm in Z.
    strap = b._block(-22.0, 28.0, 22.9, 23.9, 102.0, 110.0)
    cradle.label = 'ST3215_HS_FRAME_INTEGRAL_CRADLE_PETG'
    strap.label = 'ST3215_HS_FRONT_RETAINER_STEEL'
    return {'cradle':cradle,'strap':strap}


def assembly():
    return Compound(label='ST3215_HS_TRIAL_MOUNT',children=list(parts().values()))
