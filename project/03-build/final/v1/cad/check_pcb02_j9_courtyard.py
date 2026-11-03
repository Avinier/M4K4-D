"""Check the D-041 J2-9 GH2 courtyard against the PCB-02 upper +Y mount.

This is a planar pre-layout gate. The board-local transform is Y/Z in the
robot frame. The GH2 horizontal footprint's F.CrtYd spans 6.96 x 6.40 mm;
its mating face on F.Fab is 2.45 mm from the footprint origin. D-084: the
stock mount tabs reach 2.70 mm, so the face sits 0.55 mm inboard of the
board's +Y edge (Y=25.0 mm) to keep tab copper 0.3 mm from the edge; the
builder accepted the resulting 0.3 mm courtyard-to-keepout margin. A populated
STEP and full DRC remain required before release.
"""

import ast
from math import hypot
from pathlib import Path


BOARD_EDGE_Y = 25.0
J9_CENTER_Z = 88.6
J9_FACE_OFFSET = 2.45
J9_FACE_INSET = 0.55  # D-084: tab copper 0.3 mm from the edge
J9_COURTYARD_DEPTH = 6.40
J9_COURTYARD_WIDTH = 6.96
MOUNT_Z = 91.5
KEEP_OUT_R = 3.5


def gap(hole_y: float, inset: float = J9_FACE_INSET) -> float:
    """Signed distance from circular mount keepout to J9 courtyard rectangle."""
    origin_y = BOARD_EDGE_Y - inset - J9_FACE_OFFSET
    lo_y = origin_y - J9_COURTYARD_DEPTH / 2
    hi_y = origin_y + J9_COURTYARD_DEPTH / 2
    lo_z = J9_CENTER_Z - J9_COURTYARD_WIDTH / 2
    hi_z = J9_CENTER_Z + J9_COURTYARD_WIDTH / 2
    dy = max(lo_y - hole_y, 0.0, hole_y - hi_y)
    dz = max(lo_z - MOUNT_Z, 0.0, MOUNT_Z - hi_z)
    return hypot(dy, dz) - KEEP_OUT_R


if __name__ == "__main__":
    current = gap(20.5)
    model = ast.parse((Path(__file__).parent / "makad-v1.step.py").read_text())
    mount = next(n.value for n in model.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "PCB02_MOUNT" for t in n.targets))
    holes = ast.literal_eval(next(k.value for k in mount.keywords if k.arg == "holes"))
    upper_positive_holes = [y for y, z in holes if y > 0 and z == MOUNT_Z]
    assert len(upper_positive_holes) == 1, "expected one upper +Y mounting hole"
    actual_y = upper_positive_holes[0]
    candidate = gap(actual_y)
    print(f"Current Y=20.5, Z=91.5: keepout-to-J9 gap {current:+.2f} mm")
    print(f"CAD mount Y={actual_y:.1f}, Z=91.5: keepout-to-J9 gap {candidate:+.2f} mm")
    assert current < 0, "expected collision was not reproduced"
    assert candidate >= 0.3 - 1e-9, "J9 courtyard lacks the D-084 0.3 mm margin"
