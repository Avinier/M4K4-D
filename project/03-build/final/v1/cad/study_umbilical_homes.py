"""D-107 centre route, read-only survey: where the bundle and the camera-link boards can live.

Edits nothing. Builds the head parts (03-head/v1/cad, catalog off) and the chassis + body
droid tree, samples every part's surface with its label, and reports:

1. the yaw-axis column: every body part within 14 mm of the yaw axis from Z 90 to 160
   (what the bundle passes on its way down the bore), and the parts near PCB-08;
2. the head's underside round the bundle's entry (roll- and pitch-frame parts near the
   opening and the clamp found by study_umbilical_span.py --neck);
3. free slabs for the Arducam U6248 boards:
   - receiver (UC-892, Pi-HAT size, E) anywhere inside the body;
   - transmitter (UC-891, E) inside the head's roll frame, free over roll +-21 deg against
     the pitch-frame parts and over the whole envelope against the yaw-carried parts.
   A slab is free when no surface sample of any part lies in it on a 2 mm grid, and it is
   enclosed by parts in at least five of six directions (so it is inside, not outside).
   The best body candidates are then checked exactly (world-frame boolean, vendor STEPs
   as boxes).

Board sizes are estimates from Arducam's photographs and one reseller figure; the received
boards decide. Run from this folder with the legacy runtime, MAKAD_RELIEF_SERIAL=1 and
PYTHONPATH 03-head/v1/cad first, then 02-body/v1/cad. About 5 min.
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

import module_checks as C
from study_umbilical_geometry import sample
from study_umbilical_span import Head

HERE = Path(__file__).resolve().parent
OUT = HERE / "__cadgen__" / "umbilical-homes.npz"
GRID = 2.0

# (name, (a, b, c) mm) slabs to place; E dimensions
RX_SLABS = [("receiver with jack and mated plug", (65.0, 56.0, 18.0)),
            ("receiver, jack removed, cable soldered", (65.0, 56.0, 7.0))]
TX_SLABS = [("transmitter with jack and mated plug", (25.0, 62.0, 16.0)),
            ("transmitter, jack removed, cable soldered", (25.0, 40.0, 6.0))]
PI_CAMERA_SOCKET_HINT = "CAM"      # label fragment; falls back to the Pi's box centre
NECK_CLAMP = (-50.4, 0.0, 13.0)    # head-local: clamp from the --neck study (8 mm behind the yaw axis)
NECK_OPENING = (-58.0, -38.0, -9.0, 8.0)   # head-local x0, x1, y0, y1 of the underside opening (E)
PCB12_KEEP = (-34.0, -24.0, -44.0, -14.0, 8.0, 51.5)   # PCB-12 with mated plugs (D-102), head-local


def box_points(b, spacing=GRID / 2):
    """Points filling a box (x0, x1, y0, y1, z0, z1)."""
    ax = [np.arange(b[2 * k], b[2 * k + 1] + 1e-6, spacing) for k in range(3)]
    return np.stack(np.meshgrid(*ax, indexing="ij"), -1).reshape(-1, 3)


class Grid:
    def __init__(self, lo, hi):
        self.lo = np.array(lo, float)
        self.shape = tuple(int(math.ceil((h - l) / GRID)) for l, h in zip(lo, hi))
        self.occ = np.zeros(self.shape, bool)

    def mark(self, pts):
        i = np.floor((pts - self.lo) / GRID).astype(int)
        ok = np.all((i >= 0) & (i < np.array(self.shape)), axis=1)
        i = i[ok]
        self.occ[i[:, 0], i[:, 1], i[:, 2]] = True

    def centre(self, idx):
        return self.lo + (np.array(idx) + 0.5) * GRID

    def enclosed(self):
        """Voxels with an occupied voxel beyond them in at least five of the six axis directions."""
        n = np.zeros(self.shape, np.int8)
        for ax in range(3):
            fwd = np.maximum.accumulate(self.occ, axis=ax)
            back = np.flip(np.maximum.accumulate(np.flip(self.occ, axis=ax), axis=ax), axis=ax)
            n += fwd.astype(np.int8) + back.astype(np.int8)
        return n >= 5

    def slabs(self, dims, region=None):
        """Feasible slab centres for every axis order of dims: [(order, centre xyz, clearance mm)]."""
        free = ~self.occ & self.enclosed()
        edt = ndimage.distance_transform_edt(~self.occ) * GRID
        out = []
        seen = set()
        for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            d = tuple(dims[k] for k in order)
            if d in seen:
                continue
            seen.add(d)
            size = tuple(max(1, int(math.ceil(v / GRID))) for v in d)
            ok = ndimage.minimum_filter(free.astype(np.uint8), size=size, mode="constant", cval=0).astype(bool)
            # minimum_filter's footprint is centred with the extra voxel on the low side for even sizes
            idx = np.argwhere(ok)
            if region is not None and len(idx):
                c = self.lo + (idx + 0.5) * GRID
                keep = np.all((c >= np.array(region[0::2])) & (c <= np.array(region[1::2])), axis=1)
                idx = idx[keep]
            for i in idx:
                out.append((d, self.centre(i), float(edt[tuple(i)])))
        return out


def summarise_slabs(found, labelled, target, top=6):
    """Group feasible centres by slab orientation; report count, the roomiest and the nearest to target."""
    tree, names, lab = labelled
    rows = []
    for d in sorted({f[0] for f in found}):
        sub = [f for f in found if f[0] == d]
        cen = np.array([f[1] for f in sub])
        clr = np.array([f[2] for f in sub])
        dist = np.linalg.norm(cen - np.array(target), axis=1)
        picks = list(np.argsort(-clr)[:top // 2]) + list(np.argsort(dist)[:top // 2])
        cands = []
        for k in dict.fromkeys(picks):
            c = cen[k]
            half = np.array(d) / 2.0
            faces = [c + half * np.array(s) for s in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
            near = sorted({names[lab[j]] for j in tree.query(np.array(faces))[1]})
            cands.append(dict(centre=[round(float(v), 1) for v in c], clearance_at_centre=round(float(clr[k]), 1),
                              to_target=round(float(dist[k]), 1), neighbours=near[:6]))
        rows.append(dict(slab_xyz=list(d), feasible_centres=len(sub),
                         span=[[round(float(cen[:, k].min()), 1), round(float(cen[:, k].max()), 1)] for k in range(3)],
                         candidates=cands))
    return rows


def main():
    entry = C.load_entry()
    import layout_model as m
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    report = dict(script="study_umbilical_homes", grid_mm=GRID)

    # ---------------- head: labelled samples by frame
    hp, hl, hf, hnames = [], [], [], []
    for name, d in parts.items():
        if d["kind"] != "physical":
            continue
        try:
            pts = sample(d["shape"], 1.5)
        except Exception as exc:
            print("sample failed", name, exc)
            continue
        hnames.append(name)
        hp.append(pts)
        hl.append(np.full(len(pts), len(hnames) - 1))
        hf.append(np.full(len(pts), "YPR".index(d["frame"]) if d["frame"] in "YPR" else 0))
    hp, hl, hf = np.vstack(hp), np.concatenate(hl), np.concatenate(hf)
    C.log(f"head sampled: {len(hp)} points, {len(hnames)} parts")

    class Npz(dict):
        pass
    head = Head(dict(origin=np.array(entry.HEAD_ORIGIN_IN_CHASSIS, float),
                     pitch_axis=np.array([m.PITCH_AXIS.position.X, 0.0, m.PITCH_AXIS.position.Z]),
                     roll_axis=np.array([0.0, m.ROLL_AXIS.position.Y, m.ROLL_AXIS.position.Z]),
                     yaw_axis_x=np.array([m.YAW_AXIS.position.X])))

    # 2. underside round the entry
    x0, x1, y0, y1 = NECK_OPENING
    near = (hp[:, 0] > x0 - 14) & (hp[:, 0] < x1 + 14) & (np.abs(hp[:, 1]) < 24) & (hp[:, 2] > -1.5) & (hp[:, 2] < 24)
    rows = []
    for k in np.unique(hl[near]):
        p = hp[near & (hl == k)]
        rows.append(dict(part=hnames[k], frame="YPR"[hf[hl == k][0]], points=len(p),
                         x=[round(float(p[:, 0].min()), 1), round(float(p[:, 0].max()), 1)],
                         y=[round(float(p[:, 1].min()), 1), round(float(p[:, 1].max()), 1)],
                         z=[round(float(p[:, 2].min()), 1), round(float(p[:, 2].max()), 1)],
                         to_clamp=round(float(np.linalg.norm(p - np.array(NECK_CLAMP), axis=1).min()), 1)))
    report["head_underside_parts"] = sorted(rows, key=lambda r: r["to_clamp"])
    inside = (hp[:, 0] > x0) & (hp[:, 0] < x1) & (hp[:, 1] > y0) & (hp[:, 1] < y1) & (hp[:, 2] < 16)
    report["opening_cuts"] = [dict(part=hnames[k], z=[round(float(hp[inside & (hl == k)][:, 2].min()), 1),
                                                      round(float(hp[inside & (hl == k)][:, 2].max()), 1)])
                              for k in np.unique(hl[inside])]
    cam = [n for n in hnames if "camera" in n.lower() or "csi" in n.lower()]
    report["camera_parts"] = {n: [round(float(v), 1) for v in C._box(parts[n]["shape"])] for n in cam}

    # 3b. transmitter in the roll frame
    g = Grid((-118.0, -68.0, -2.0), (-2.0, 68.0, 108.0))
    R, P, Y = hp[hf == 2], hp[hf == 1], hp[hf == 0]
    g.mark(R)
    for roll in np.arange(-21.0, 21.01, 3.5):
        g.mark(head.to_frame(head.to_world(P, "P", 0.0, 0.0, 0.0), "R", 0.0, 0.0, roll))
    for q in np.arange(-25.0, 43.01, 6.8):
        for roll in (-21.0, -10.5, 0.0, 10.5, 21.0):
            g.mark(head.to_frame(head.to_world(Y, "Y", 0.0, 0.0, 0.0), "R", 0.0, q, roll))
    g.mark(box_points(PCB12_KEEP))
    g.mark(box_points((x0 - 4, x1 + 4, y0 - 4, y1 + 4, 0.0, 18.0)))     # the bundle's entry and clamp
    htree = (cKDTree(hp), hnames, hl)
    cam_target = None
    if cam:
        b = C._box(parts[cam[0]]["shape"])
        cam_target = ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)
    report["transmitter_in_head_roll_frame"] = {
        name: summarise_slabs(g.slabs(dims), htree, cam_target or (-20.0, 0.0, 90.0)) for name, dims in TX_SLABS}
    C.log("head slabs done")

    # ---------------- body
    entry, tree, leaves = C.droid_tree(entry)
    bp, bl, bnames = [], [], []
    bgrid = Grid((-64.0, -94.0, 28.0), (104.0, 94.0, 144.0))
    for lf in leaves:
        if not C.is_part(lf.path):
            continue
        b = lf.box
        if lf.vendor:
            pts = box_points((b[0], b[3], b[1], b[4], b[2], b[5]))
        else:
            try:
                pts = sample(lf.shape, 1.5)
            except Exception as exc:
                print("sample failed", lf.label, exc)
                continue
        if not len(pts):
            continue
        bnames.append("/".join(lf.path[-2:]))
        bp.append(pts)
        bl.append(np.full(len(pts), len(bnames) - 1))
    bp, bl = np.vstack(bp), np.concatenate(bl)
    bgrid.mark(bp)
    C.log(f"body sampled: {len(bp)} points, {len(bnames)} parts")

    # 1. yaw-axis column and the PCB-08 neighbourhood
    ax_x = float(entry.HEAD_ORIGIN_IN_CHASSIS[0] + m.YAW_AXIS.position.X)
    rad = np.hypot(bp[:, 0] - ax_x, bp[:, 1])
    col = (rad < 14.0) & (bp[:, 2] > 90.0) & (bp[:, 2] < 160.0)
    rows = []
    for k in np.unique(bl[col]):
        sel = col & (bl == k)
        rows.append(dict(part=bnames[k], z=[round(float(bp[sel][:, 2].min()), 1), round(float(bp[sel][:, 2].max()), 1)],
                         r_min=round(float(rad[sel].min()), 1)))
    report["yaw_axis_x"] = ax_x
    report["yaw_axis_column"] = sorted(rows, key=lambda r: -r["z"][1])
    reg = (bp[:, 0] > -30) & (bp[:, 0] < 30) & (bp[:, 1] > -50) & (bp[:, 1] < 12) & (bp[:, 2] > 108) & (bp[:, 2] < 136)
    rows = []
    for k in np.unique(bl[reg]):
        p = bp[reg & (bl == k)]
        rows.append(dict(part=bnames[k], x=[round(float(p[:, 0].min()), 1), round(float(p[:, 0].max()), 1)],
                         y=[round(float(p[:, 1].min()), 1), round(float(p[:, 1].max()), 1)],
                         z=[round(float(p[:, 2].min()), 1), round(float(p[:, 2].max()), 1)]))
    report["axis_to_pcb08_region"] = rows

    # 3a. receiver in the body
    pi = [lf for lf in leaves if "RASPBERRY_PI5" in "/".join(lf.path)]
    target = (0.0, 0.0, 100.0)
    if pi:
        b = pi[0].box
        target = ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)
        report["pi_box"] = [round(float(v), 1) for v in b]
    btree = (cKDTree(bp), bnames, bl)
    region = (-46.0, 86.0, -62.0, 62.0, 58.0, 137.0)
    solids = [lf for lf in leaves if C.is_part(lf.path)]
    rx = {}
    for name, dims in RX_SLABS:
        rows = summarise_slabs(bgrid.slabs(dims, region), btree, target)
        for row in rows:
            for cand in row["candidates"]:
                c, d = cand["centre"], row["slab_xyz"]
                # exact check with a 1 mm shrink: voxel edges overstate the slab by up to a cell
                box = C.blk((c[0] - d[0] / 2 + 1, c[0] + d[0] / 2 - 1, c[1] - d[1] / 2 + 1, c[1] + d[1] / 2 - 1,
                             c[2] - d[2] / 2 + 1, c[2] + d[2] / 2 - 1))
                cand["exact_clashes"] = C.clashes(box, solids)[:5]
        rx[name] = rows
    report["receiver_in_body"] = rx
    C.log("body slabs done")

    OUT.parent.mkdir(exist_ok=True)
    np.savez_compressed(OUT, head_pts=hp, head_label=hl, head_frame=hf, head_names=np.array(hnames),
                        body_pts=bp, body_label=bl, body_names=np.array(bnames))
    (HERE / "study_umbilical_homes-report.json").write_text(json.dumps(report, indent=1) + "\n")
    C.log("written")


if __name__ == "__main__":
    main()
