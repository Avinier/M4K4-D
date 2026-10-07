"""Storyboard <-> CAD sign multipliers at the public motion interface.

Storyboard signs are the external command convention (`storyboard.md`):
pitch + is chin down, yaw + is robot-right, roll + lowers the robot-left side.
CAD angles are right-hand rotations about +Y (pitch), +Z (yaw) and +X (roll) in
head coordinates: +X forward (face), +Y robot-left, +Z up.

    cad_angle = SIGN[axis] * storyboard_angle

The multipliers are derived here from the geometry, not typed in: each axis
rotates a probe point by a small positive CAD angle and reads which way it went.
`python motion_signs.py` checks them and writes motion-signs.json; it exits
non-zero if the derivation disagrees with SIGN.
"""
import json, math, sys
from pathlib import Path

HERE = Path(__file__).parent
SIGN = {'pitch': 1, 'yaw': -1, 'roll': -1}


def _rotate(p, axis, deg):
    """Right-hand rotation of point p about the head's +X/+Y/+Z axis."""
    x, y, z = p; c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    if axis == 'x': return (x, c * y - s * z, s * y + c * z)
    if axis == 'y': return (c * x + s * z, y, -s * x + c * z)
    return (c * x - s * y, s * x + c * y, z)


def derive():
    d = 5.0
    # Pitch: the chin (front, +X) must drop (-Z) for storyboard +.
    chin = _rotate((1, 0, 0), 'y', d)
    # Yaw: the face (+X) must swing toward robot-right (-Y) for storyboard +.
    face = _rotate((1, 0, 0), 'z', d)
    # Roll: the robot-left side (+Y) must lower (-Z) for storyboard +.
    left = _rotate((0, 1, 0), 'x', d)
    return {
        'pitch': 1 if chin[2] < 0 else -1,
        'yaw': 1 if face[1] < 0 else -1,
        'roll': 1 if left[2] < 0 else -1,
    }


if __name__ == '__main__':
    derived = derive()
    ok = derived == SIGN
    result = dict(
        convention='cad_angle = sign * storyboard_angle; head frame +X forward, +Y robot-left, +Z up; CAD angles right-hand about +Y pitch, +Z yaw, +X roll',
        storyboard_positive={'pitch': 'chin down', 'yaw': 'robot-right', 'roll': 'robot-left side lowers'},
        sign=SIGN, derived_from_geometry=derived, passed=ok,
        consumers=['C2 motion firmware public command interface', 'signed gravity/cable/asymmetric-pose screens', 'viewer pose sliders (raw CAD angles)'],
    )
    (HERE / 'motion-signs.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if ok else 1)
