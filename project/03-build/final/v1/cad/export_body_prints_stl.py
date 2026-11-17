"""Export body frame, tray and enclosure prints from the final droid geometry."""

import json
from pathlib import Path

import numpy as np
from build123d import Axis, export_stl

import module_checks as C
from export_chassis_front_stl import mesh_closed, mesh_volume, read_stl


OUT = C.HERE.parents[2].parent / "04-print" / "02-body"
PARTS = (
    ("BO-025", "BODY_FRAME_MAIN_PRINT", "PETG, Sunlu grey", None, "Bottom (-Z)", "Frame feet, yaw plate, inserts and shell joints"),
    ("BO-026", "BODY_FRAME_FRONT_LEFT_FOOT_CASSETTE", "PETG, Sunlu grey", None, "Bottom (-Z)", "Captive M4 nut, slide and side screws"),
    ("BO-033", "COMPUTE_TRAY", "PETG, Sunlu grey", None, "Bottom (-Z)", "Pi and cooler clearance, three tray supports"),
    ("BO-019", "BODY_SHELL", "ASA, white; ivory finish", None, "Open rim (-Z)", "Shell lowering, microphone bosses, arch seats and panel openings"),
    ("BO-020", "FRONT_SERVICE_PANEL_EXPOSED_SPEAKER", "ASA, white; taupe finish", ("Y", 90), "Outer face (+X)", "Speaker cup, gasket land and panel fasteners"),
    ("BO-021", "REAR_SERVICE_PANEL_OCTAGONAL", "ASA, white; taupe finish", ("Y", -90), "Outer face (-X)", "XT30/XH port fit, button well and removal"),
    ("BO-008", "WHEEL_ARCH_POD_L", "ASA, white; ivory finish", ("X", -90), "Outer face (+Y)", "Top Ø4.10 pilot, inserts, tyre running gap"),
    ("BO-008", "WHEEL_ARCH_POD_R", "ASA, white; ivory finish", ("X", 90), "Outer face (-Y)", "Top Ø4.10 pilot, inserts, tyre running gap"),
    ("BO-009", "WHEEL_ARCH_UPPER_TRIM_L", "ASA, white; amber finish", ("X", -90), "Outer face (+Y)", "Glue land and tyre radial gap"),
    ("BO-009", "WHEEL_ARCH_UPPER_TRIM_R", "ASA, white; amber finish", ("X", 90), "Outer face (-Y)", "Glue land and tyre radial gap"),
)


def main():
    _, _, leaves = C.droid_tree()
    report = C.Report("export_body_prints_stl")
    out = OUT / "stl"
    cards = OUT / "cards"
    out.mkdir(parents=True, exist_ok=True)
    cards.mkdir(parents=True, exist_ok=True)
    manifest = []
    for bom, label, material, turn, bed, critical in PARTS:
        shape = C.find(leaves, label).shape
        if turn:
            axis = Axis.X if turn[0] == "X" else Axis.Y
            shape = shape.rotate(axis, turn[1])
        bb = C._box(shape)
        oriented = C.moved(shape, (-bb[0], -bb[1], -bb[2]))
        target = out / f"{bom}_{label}.stl"
        export_stl(oriented, str(target), tolerance=.003, angular_tolerance=.08)
        # Curved B-rep bounds can be loose; place the actual mesh on the bed.
        import struct
        data = bytearray(target.read_bytes())
        tri = read_stl(target)
        shift = tri.reshape(-1, 3).min(0)
        for i in range(struct.unpack_from('<I', data, 80)[0]):
            for j in range(3):
                off = 84 + 50*i + 12 + 12*j
                xyz = struct.unpack_from('<3f', data, off)
                struct.pack_into('<3f', data, off, *(xyz[k]-shift[k] for k in range(3)))
        target.write_bytes(data)
        triangles = read_stl(target)
        lo = triangles.reshape(-1, 3).min(0)
        hi = triangles.reshape(-1, 3).max(0)
        open_edges, degenerate = mesh_closed(triangles)
        v_mesh = mesh_volume(triangles)
        v_cad = C.volume(shape)
        report.check(f"{label}_closed", open_edges == 0, open_edges=open_edges,
                     degenerate_dropped=degenerate, triangles=len(triangles))
        report.check(f"{label}_volume", abs(v_mesh-v_cad)/v_cad < .002,
                     mesh_mm3=round(v_mesh, 2), cad_mm3=round(v_cad, 2))
        report.check(f"{label}_bed", np.allclose(lo, 0, atol=.02), low_mm=lo.tolist())
        size = [round(float(v), 2) for v in hi-lo]
        manifest.append(dict(file=target.name, bom=bom, cad_label=label, quantity=1,
                             material=material, bed_down=bed, size_mm=size,
                             volume_mm3=round(v_mesh, 2),
                             source="final/v1/cad/export_body_prints_stl.py"))
        (cards / f"{bom}_{label}.md").write_text(
            f"# {bom} — {label}\n\n"
            f"- Source: `03-build/final/v1/cad/makad-v1.step.py`, exported by `export_body_prints_stl.py`.\n"
            f"- STL: [`../stl/{target.name}`](../stl/{target.name}); one piece.\n"
            f"- Material and finish: {material}.\n"
            f"- Bed face: {bed}; mesh origin at bed corner, size {size} mm.\n"
            f"- Volume: {v_mesh:.1f} mm³; watertight mesh and CAD-volume match checked.\n"
            f"- First-part checks: {critical}.\n"
            f"- Slicer gate: review supports, wall widths, shrink compensation and machine fit before sending to the lab.\n"
            f"- Assembly gate: verify the received hardware and the actual printed fits; this STL is not a measured part.\n")
    manifest_path = out / "manifest.json"
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    old = [row for row in old if row.get("bom") not in {p[0] for p in PARTS}]
    manifest_path.write_text(json.dumps(old + manifest, indent=2) + "\n")
    report.finish()


if __name__ == "__main__":
    main()
