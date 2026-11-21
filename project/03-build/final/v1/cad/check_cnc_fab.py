"""Checks the CNC fabrication pack in ../fab/ against the droid geometry.

For every machined part the droid carries, the part as the droid draws it is taken
from the built trees, moved into the fab frame and compared with the fab source:

- CH-013 ballast bar and BO-047 pinion shaft (with its D-125 flat): chassis + body
  droid tree (module_checks.droid_tree) against export_cnc_fab's nominal() shapes;
- CH-012 stub and CH-052 cap: the same tree against the STEPs on disk
  (export_axle_fab frame);
- HD-009 pivot pin and HD-034 roll spindle (with the D-120 rear flat): the head
  parts (layout_model.build_parts, catalog off) against nominal();
- HD-004 collar: d120_roll_horn_hub.collar() against the STEP on disk.

"Same" means the symmetric difference is under 0.01 mm3. It then checks that each
export_cnc_fab STEP on disk is the current build (volume), and that every part the
pack lists has a STEP and a drawing (the DXF for CH-052 too).

Run from this folder with the legacy runtime: MAKAD_RELIEF_SERIAL=1,
PYTHONPATH=../../../03-head/v1/cad:../../../02-body/v1/cad:. (about 5 min).
Writes check_cnc_fab-report.json.
"""
from pathlib import Path

from build123d import Axis, Location, import_step

import module_checks as C
import export_cnc_fab as F

FAB = Path(__file__).resolve().parent.parent / "fab"
TOL = 1e-2
PACK = {   # part -> files the shop needs
    "CH-012_stub": [".step", "_drawing.pdf"],
    "CH-013_ballast_bar": [".step", "_drawing.pdf"],
    "CH-052_cap": [".step", ".dxf", "_drawing.pdf"],
    "BO-047_pinion_shaft": [".step", "_drawing.pdf"],
    "BO-046_fixed_pinion_half": [".step", ".dxf", "_drawing.pdf"],   # droid match in check_d125_pinion_dbore
    "HD-004_roll_hub_collar": [".step", "_drawing.pdf"],
    "HD-009_pivot_pin": [".step", "_drawing.pdf"],
    "HD-034_roll_spindle": [".step", "_drawing.pdf"],
}


def symdiff(a, b):
    c = C.common(a, b)
    return a.volume + b.volume - 2 * c, c


def by_bbox(shape):
    """Centre X/Y on the axis, bottom at z 0 (parts whose fab frame is the world frame shifted)."""
    bb = shape.bounding_box()
    c = bb.center()
    return shape.moved(Location((-c.X, -c.Y, -bb.min.Z)))


def step(name):
    s = import_step(str(FAB / f"{name}.step"))
    sol = s.solids()
    assert len(sol) == 1, (name, len(sol))
    return sol[0]


def main():
    r = C.Report("check_cnc_fab")

    # --- Pack completeness -------------------------------------------------
    missing = [f"{p}{ext}" for p, exts in PACK.items() for ext in exts if not (FAB / f"{p}{ext}").exists()]
    r.check("pack_files_present", not missing, missing=missing, parts=len(PACK))

    # --- export_cnc_fab STEPs are the current build --------------------------
    for name, (build, _) in F.PARTS.items():
        on_disk, now = step(name), build()
        d, _ = symdiff(on_disk, now)
        r.check(f"{name}_step_is_current", d < TOL, symdiff_mm3=d, volume=now.volume)

    # --- Chassis + body droid tree -----------------------------------------
    entry, _, leaves = C.droid_tree(with_modules=False, revb_pcb08=False)
    bar = by_bbox(C.find(leaves, "BALLAST_STEEL_BAR").shape.rotate(Axis.Z, 90))   # droid Y -> fab X
    d, _ = symdiff(bar, F.ballast_bar(nominal=True))
    r.check("CH-013_matches_droid_bar", d < TOL, symdiff_mm3=d, droid_volume=bar.volume)
    import d125_pinion_dbore as P125   # the flat moves the bbox centre, so place it on its axis
    shaft = C.find(leaves, "YAW_PINION_SHAFT_D5_STEEL").shape.moved(Location((-P125.PX, -P125.PY, -P125.Z0)))
    d, _ = symdiff(shaft, F.pinion_shaft(nominal=True))
    r.check("BO-047_matches_droid_shaft_with_d125_flat", d < TOL, symdiff_mm3=d, droid_volume=shaft.volume)

    # CH-012 / CH-052: same frame as export_axle_fab.to_local.
    for label, y0, name in (("WHEEL_L_STUB_SHAFT_8MM", 73.0, "CH-012_stub"), ("AXLE_BEARING_CAP_L", 86.51, "CH-052_cap")):
        w = C.find(leaves, label).shape
        local = w.moved(Location((0.0, -y0, -42.0))).rotate(Axis.X, 90.0)
        d, _ = symdiff(local, step(name))
        r.check(f"{name}_step_matches_droid", d < TOL, symdiff_mm3=d, volume=local.volume)
    C.log("chassis/body parts compared")

    # --- Head parts --------------------------------------------------------
    import layout_model as m
    import d120_roll_horn_hub as D
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    sp = parts["rolling_spindle_6mm"]["shape"] - D.spindle_flat_tool()
    sp = sp.moved(Location((-F._sx0, -m.ROLL_Y, -m.ROLL_Z))).rotate(Axis.Y, -90).rotate(Axis.Z, 90)
    d, _ = symdiff(sp, F.roll_spindle(nominal=True))
    r.check("HD-034_matches_droid_spindle_with_d120_flat", d < TOL, symdiff_mm3=d, droid_volume=sp.volume)
    pin = parts["pitch_trunnion_D6x12_pin"]["shape"]
    pin = pin.moved(Location((-m.PITCH_X, -F._t["pin_y"][1], -m.PITCH_Z))).rotate(Axis.X, -90).rotate(Axis.Z, 180)
    d, _ = symdiff(pin, F.pivot_pin(nominal=True))
    r.check("HD-009_matches_droid_pin", d < TOL, symdiff_mm3=d, droid_volume=pin.volume)
    col = D.collar().moved(Location((-D.COLLAR_X[0], -D.Y, -D.Z))).rotate(Axis.Y, -90).rotate(Axis.Z, 180)
    d, _ = symdiff(col, step("HD-004_roll_hub_collar"))
    r.check("HD-004_step_matches_d120_collar", d < TOL, symdiff_mm3=d, volume=col.volume)

    # --- Facts the drawings rely on ----------------------------------------
    ok, rows = F.self_checks()
    r.check("fab_interface_facts", ok, **rows)
    r.finish()


if __name__ == "__main__":
    main()
