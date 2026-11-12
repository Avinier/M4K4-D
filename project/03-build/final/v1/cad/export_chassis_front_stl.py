"""Export CH-001 CHASSIS_FRAME_FRONT_MODULE to 04-print with every droid edit (D-095 and D-106 included).

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 1 min.
D-095 added the balance-lead Ø5 deck hole and the tub-bay plate's insert pilots (two M3 x 4 in the
deck strip, two M3 x 6 in the front crossmember). D-106 added the harness features: the W03a deck
slot, the J10-8 tunnel and notch under the crossmember, the fuse-holder tie tunnel through the
bracket column and two deck tie lugs. The script checks the D-095 features in the B-rep
(check_d106_harness.py checks the D-106 ones), writes the STL in print orientation (tub bottom down,
as it sits, D-076; min corner at the origin, as the 2026-11-01 package), then re-checks the mesh:
closed (every edge in exactly two triangles), volume against the B-rep, the hole, pilots, slot and
tunnels open on rays along their axes. It updates the manifest row and prints a JSON summary.
"""

import json
import struct
from pathlib import Path

import numpy as np
from build123d import export_stl

import module_checks as C

LABEL = "CHASSIS_FRAME_FRONT_MODULE"
OUT = C.HERE.parents[2].parent / "04-print" / "01-chassis" / "stl"
FILE = "CH-001_CHASSIS_FRAME_FRONT_MODULE.stl"


def read_stl(path):
    b = path.read_bytes()
    n = struct.unpack("<I", b[80:84])[0]
    a = np.frombuffer(b[84:84 + n * 50], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    return a["v"].reshape(-1, 3, 3).astype(float)


def mesh_closed(tri):
    """(non-manifold edge count, degenerate triangles dropped) after welding vertices at 1e-4 mm."""
    q = np.round(tri.reshape(-1, 3), 4)
    _, idx = np.unique(q, axis=0, return_inverse=True)
    f = idx.reshape(-1, 3)
    keep = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
    f = f[keep]
    e = np.sort(np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
    _, counts = np.unique(e, axis=0, return_counts=True)
    return int((counts != 2).sum()), int((~keep).sum())


def mesh_volume(tri):
    return float(np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6.0)


def ray_z_hits(tri, x, y):
    """Z values where the vertical line at (x, y) crosses the mesh (Moller-Trumbore on +Z)."""
    return ray_hits(tri, (x, y, -1000.0), 2)


def ray_hits(tri, origin, axis):
    """Coordinates along `axis` (0 X, 1 Y, 2 Z) where the line through origin parallel to it crosses the mesh."""
    o = np.array(origin, dtype=float)
    o[axis] = -1000.0
    d = np.zeros(3)
    d[axis] = 1.0
    e1, e2 = tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]
    p = np.cross(d, e2)
    det = np.einsum("ij,ij->i", e1, p)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = o - tri[:, 0]
    u = np.einsum("ij,ij->i", s, p) * inv
    q = np.cross(s, e1)
    v = (q @ d) * inv
    t = np.einsum("ij,ij->i", e2, q) * inv
    m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
    return sorted(set(np.round(o[axis] + t[m], 3)))


def main():
    entry, tree, leaves = C.droid_tree(with_modules=False)
    r = C.Report("export_chassis_front_stl")
    shape = C.find(leaves, LABEL).shape
    bb = C._box(shape)
    shift = (-bb[0], -bb[1], -bb[2])

    # 1. D-095 features in the B-rep (world frame).
    hx, hy, hr = entry.BALANCE["deck_hole"]
    holes = C.ray(shape, (hx, hy, 0.0), (0, 0, 1))
    wall = C.ray(shape, (hx + hr + 1.2, hy, 0.0), (0, 0, 1))
    r.check("brep_balance_hole_open", not any(56.0 > a > 50.0 or 56.0 > b > 50.0 for a, b in holes) and bool(wall),
            material_on_axis=holes, material_beside=wall)
    tb = entry.TUB_BAY
    deck_top = tb["plate"][4]                 # the plate sits on the deck top, Z 56.0
    probe = tb["pilot_r"] + 0.8
    sides = ((probe, 0.0), (-probe, 0.0), (0.0, probe), (0.0, -probe))

    def covered(intervals, z0, z1):
        return any(a <= z0 + 1e-6 and b >= z1 - 1e-6 for a, b in intervals)

    for tag, pts, ins in (("deck_strip_M3x4", tb["fix_rear"], tb["insert_rear"]), ("crossmember_M3x6", tb["fix_front"], tb["insert_front"])):
        z0, z1 = deck_top - ins[2] + 0.2, deck_top - 0.2
        for x, y in pts:
            on_axis = C.ray(shape, (x, y, 0.0), (0, 0, 1))
            axis_open = not any(b > z0 and a < z1 for a, b in on_axis)
            walls = [covered(C.ray(shape, (x + dx, y + dy, 0.0), (0, 0, 1)), z0, z1) for dx, dy in sides]
            r.check(f"brep_pilot_{tag}_{y:+.0f}", axis_open and all(walls),
                    axis_material=on_axis, walls_cover_insert_depth=walls, band=[z0, z1])

    # 2. Export in print orientation.
    placed = C.moved(shape, shift)
    path = OUT / FILE
    export_stl(placed, str(path), tolerance=0.01, angular_tolerance=0.2)
    tri = read_stl(path)
    lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
    vol_mesh, vol_brep = mesh_volume(tri), C.volume(shape)
    open_edges, degenerate = mesh_closed(tri)
    r.check("mesh_closed", open_edges == 0, open_edges=open_edges, degenerate_dropped=degenerate, triangles=len(tri))
    r.check("mesh_volume_matches_brep", abs(vol_mesh - vol_brep) / vol_brep < 0.002, mesh_mm3=vol_mesh, brep_mm3=vol_brep)
    r.check("mesh_on_bed_at_origin", np.allclose(lo, 0.0, atol=0.01), min=list(lo), size=list(hi - lo))

    # 3. The same features on the mesh.
    hits = ray_z_hits(tri, hx + shift[0], hy + shift[1])
    deck = [z for z in hits if 50.0 + shift[2] < z < 56.5 + shift[2]]
    r.check("mesh_balance_hole_open", not deck, crossings_in_deck_band=deck)
    for (x, y), ins in [(p, tb["insert_rear"]) for p in tb["fix_rear"]] + [(p, tb["insert_front"]) for p in tb["fix_front"]]:
        z0, z1 = deck_top - ins[2] + 0.2 + shift[2], deck_top - 0.2 + shift[2]
        axis = ray_z_hits(tri, x + shift[0], y + shift[1])
        axis_open = not any(z0 < z < z1 for z in axis)
        walls = []
        for dx, dy in sides:
            zs = ray_z_hits(tri, x + dx + shift[0], y + dy + shift[1])
            walls.append(any(a <= z0 and b >= z1 for a, b in zip(zs[0::2], zs[1::2])))
        r.check(f"mesh_pilot_open_{x:+.0f}_{y:+.0f}", axis_open and all(walls), axis_crossings=axis, walls_cover_insert_depth=walls)

    # D-106 features on the mesh: no crossing inside each opening along its axis.
    sx, sy, sz = shift

    def open_on(name, origin, axis, a, b):
        p = [origin[0] + sx, origin[1] + sy, origin[2] + sz]
        lo_, hi_ = a + shift[axis], b + shift[axis]
        hits = [c for c in ray_hits(tri, p, axis) if lo_ + 0.05 < c < hi_ - 0.05]
        r.check(f"mesh_d106_{name}_open", not hits, crossings=hits)

    x0, x1, y0, y1, z0, z1 = entry.D106["pack_slot"]
    open_on("pack_slot", ((x0 + x1) / 2, (y0 + y1) / 2, 0.0), 2, 50.0, 57.0)
    x0, x1, y0, y1, z0, z1 = entry.D106_NOSE["tunnel"]
    open_on("nose_tunnel", ((x0 + x1) / 2, 0.0, (z0 + z1) / 2), 1, y0, y1)
    open_on("nose_notch", (0.0, 0.0, 34.5), 0, (x0 + x1) / 2, 92.0)
    open_on("nose_bore", (86.0, -31.0, 0.0), 2, z0, 56.0)
    x0, x1, y0, y1, z0, z1 = entry.D106["column_tunnel"]
    open_on("fuse_column_tunnel", ((x0 + x1) / 2, 0.0, (z0 + z1) / 2), 1, y0, y1)
    t = entry.D106["lug_tunnel"][1]
    for x0, x1, y0, y1 in entry.D106["deck_lugs"]:
        open_on(f"lug_tunnel_{(x0 + x1) / 2:+.0f}", ((x0 + x1) / 2, 0.0, 56.0 + t / 2), 1, y0, y1)

    # 4. Manifest row.
    mf = OUT / "manifest.json"
    rows = json.loads(mf.read_text())
    row = next(x for x in rows if x["cad_label"] == LABEL)
    old = dict(row)
    row["size_mm"] = [round(float(v), 1) for v in (hi - lo)]
    row["volume_mm3"] = round(vol_mesh, 3)
    row["source"] = "final/v1/cad/export_chassis_front_stl.py (D-095 and D-106 features; regenerated 2026-11-13)"
    mf.write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(dict(old=dict(size=old["size_mm"], volume=old["volume_mm3"]), new=dict(size=row["size_mm"], volume=row["volume_mm3"], triangles=len(tri))), indent=1))
    r.finish()


if __name__ == "__main__":
    main()
