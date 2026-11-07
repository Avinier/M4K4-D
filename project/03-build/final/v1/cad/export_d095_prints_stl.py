"""Export the three D-095 module-mount prints to 04-print in print orientation, with checks.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 1 min.
CH-106 tub-bay plate and CH-107 IMU adapter (chassis side) go to 04-print/01-chassis/stl; CH-108
rear-bay plate (body side) goes to 04-print/02-body/stl. All three print flat without supports:
the tub plate and IMU adapter bottom down as they sit; the rear-bay plate on its back (-X) face,
counterbores on the bed, arms and cradles up. For each STL the script checks the mesh is closed,
its volume matches the B-rep, it sits on the bed at the origin, and every through hole and pilot
is open on a ray along its axis; then it writes or updates the manifest row.
"""

import json
from pathlib import Path

import numpy as np
from build123d import Axis, export_stl

import module_checks as C
from export_chassis_front_stl import mesh_closed, mesh_volume, ray_z_hits, read_stl

PRINT = C.HERE.parents[2].parent / "04-print"


def parts(entry):
    tb, imu, rb = entry.TUB_BAY, entry.IMU, entry.REAR_BAY
    top = tb["plate"][5]
    tub_holes = [("fix", x, y, tb["plate"][4], top) for x, y in (*tb["fix_rear"], *tb["fix_front"])]
    tub_pilots = [("pilot", x, y, top + tb["boss"][1] - tb["pilot"][1] + 0.2, top + tb["boss"][1] - 0.2) for x, y in entry.tub_bosses()]
    itop = imu["adapter"][5]
    hx = imu["board_x1"] - imu["holes_v"]
    imu_holes = [("j15a", x, y, imu["adapter"][4], itop) for x, y in imu["j15a"]]
    imu_pilots = [("pilot", hx, u - imu["board"][0] / 2.0, imu["adapter"][4] + 0.4, itop + imu["boss"][1] - 0.2) for u in imu["holes_u"]]
    # Rear plate: the M3 screw holes run along X; after the -90 deg turn about Y they are vertical.
    rear_holes = [("m3", y, z, rb["plate"][0], rb["arm_x"][1]) for y, z in rb["screw_yz"]]
    return [
        dict(bom="CH-106", label="TUB_BAY_MODULE_PLATE", folder="01-chassis", turn=None, bed="-Z",
             holes=tub_holes + tub_pilots, material="PETG deep slate"),
        dict(bom="CH-107", label="IMU_ADAPTER_LSM6DSOX", folder="01-chassis", turn=None, bed="-Z",
             holes=imu_holes + imu_pilots, material="PETG deep slate"),
        dict(bom="CH-108", label="REAR_BAY_MODULE_PLATE", folder="02-body", turn=-90.0, bed="-X",
             holes=rear_holes, material="PETG deep slate"),
    ]


def main():
    entry, tree, leaves = C.droid_tree()
    r = C.Report("export_d095_prints_stl")
    summary = {}
    for p in parts(entry):
        shape = C.find(leaves, p["label"]).shape
        vol_brep = C.volume(shape)
        oriented = shape.rotate(Axis.Y, p["turn"]) if p["turn"] else shape
        bb = C._box(oriented)
        shift = np.array([-bb[0], -bb[1], -bb[2]])
        out_dir = PRINT / p["folder"] / "stl"
        out_dir.mkdir(parents=True, exist_ok=True)
        name = f"{p['bom']}_{p['label']}.stl"
        export_stl(C.moved(oriented, tuple(shift)), str(out_dir / name), tolerance=0.01, angular_tolerance=0.2)
        tri = read_stl(out_dir / name)
        lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
        open_edges, degenerate = mesh_closed(tri)
        vol_mesh = mesh_volume(tri)
        r.check(f"{p['bom']}_mesh_closed", open_edges == 0, open_edges=open_edges, degenerate_dropped=degenerate, triangles=len(tri))
        r.check(f"{p['bom']}_volume_matches_brep", abs(vol_mesh - vol_brep) / vol_brep < 0.002, mesh_mm3=vol_mesh, brep_mm3=vol_brep)
        r.check(f"{p['bom']}_on_bed_at_origin", np.allclose(lo, 0.0, atol=0.01), size=list(hi - lo))

        # Holes: a ray along each axis finds no mesh crossing inside the open band.
        for kind, a, b, z0, z1 in p["holes"]:
            if p["turn"]:          # rear plate: world (x along the hole, y=a, z=b) -> print (x'=-z, y'=y, z'=x)
                px, py = -b + shift[0], a + shift[1]
                band = (z0 + shift[2], z1 + shift[2])
            else:
                px, py = a + shift[0], b + shift[1]
                band = (z0 + shift[2], z1 + shift[2])
            hits = ray_z_hits(tri, px, py)
            inside = [z for z in hits if band[0] + 0.05 < z < band[1] - 0.05]
            r.check(f"{p['bom']}_{kind}_open_{a:+.1f}_{b:+.1f}", not inside, crossings_in_band=inside, band=list(band))

        # Manifest row (new or updated).
        mf = out_dir / "manifest.json"
        rows = json.loads(mf.read_text()) if mf.exists() else []
        row = next((x for x in rows if x["cad_label"] == p["label"]), None)
        if row is None:
            row = dict(file=name, bom=p["bom"], cad_label=p["label"], quantity=1, material=p["material"], bed_down=p["bed"])
            rows.append(row)
        row.update(size_mm=[round(float(v), 1) for v in (hi - lo)], volume_mm3=round(vol_mesh, 3),
                   source="final/v1/cad/export_d095_prints_stl.py (D-095 print; exported 2026-11-07)")
        mf.write_text(json.dumps(rows, indent=2) + "\n")
        summary[p["bom"]] = dict(file=f"{p['folder']}/stl/{name}", size=row["size_mm"], volume=row["volume_mm3"], triangles=len(tri))
    print(json.dumps(summary, indent=1))
    r.finish()


if __name__ == "__main__":
    main()
