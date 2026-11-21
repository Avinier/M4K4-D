"""D-120 fabrication file: the turned roll hub collar (HD-004) from the droid geometry.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md
(a few seconds; the head parts are not built). Writes ../fab/HD-004_roll_hub_collar.step:
axis Z, the horn (flange) face at z 0 and the front end at z 12.5; the two radial
M3 set-screw holes on -Y (facing the drawing's front view). d120_collar_drawing.py makes the shop drawing from it.
The moved solid is checked against the head-frame solid (volume) and the frame
(extents) before it is written.
"""
from pathlib import Path
from build123d import Axis, Location, export_step
import d120_roll_horn_hub as D

OUT = Path(__file__).resolve().parent.parent / "fab" / "HD-004_roll_hub_collar.step"


def main():
    head = D.collar()
    local = head.moved(Location((-D.COLLAR_X[0], -D.Y, -D.Z))).rotate(Axis.Y, -90).rotate(Axis.Z, 180)   # head +X -> local +Z, set screws to -Y
    bb = local.bounding_box()
    length = D.COLLAR_X[1] - D.COLLAR_X[0]
    assert abs(local.volume - head.volume) < 1e-6, (local.volume, head.volume)
    assert abs(bb.min.Z) < 1e-6 and abs(bb.max.Z - length) < 1e-6, (bb.min.Z, bb.max.Z)
    assert abs(bb.max.X - D.COLLAR['flange_r']) < 1e-6 and abs(bb.min.Y + D.COLLAR['flange_r']) < 1e-6
    local.label = "HD-004_roll_hub_collar"
    export_step(local, str(OUT))
    print(f"wrote {OUT.name}: length {length:.2f}, volume {local.volume:.1f} mm3, mass {local.volume * D.COLLAR['density']:.2f} g")


if __name__ == "__main__":
    main()
