"""D-107 Level 2 study, stage 1: geometry for the head umbilical (read-only; edits nothing).

Builds the head parts (03-head/v1/cad, catalog off, as the head sources describe them: the
D-051 pivot and the solid -Y leg, without the D-103/104/105 droid edits that D-107 removes)
and the chassis + body droid tree, then writes:

- __cadgen__/umbilical-study.npz: surface samples of every head part by frame (Y yaw-carried,
  P pitch, R roll; head-local mm) and of the body parts near the rear top (world mm), for the
  cable solver's clearance pass (study_umbilical_span.py);
- study_umbilical_geometry-report.json: material profiles along rays through
  * the three body exits of head-umbilical-plan.md section 3.2 (A centre notch, B off-centre
    panel notch, C rear deck corner), and
  * the head's rear cover above and beside the roll servo, with the pitch-frame parts
    turned to roll 0, +-10.5 and +-21 deg as the roll frame sees them.

Run from this folder with the legacy runtime, MAKAD_RELIEF_SERIAL=1 and PYTHONPATH
03-head/v1/cad first, then 02-body/v1/cad. About 4 min.
"""

import json
import math
from pathlib import Path

import numpy as np
from build123d import Axis

import module_checks as C

HERE = Path(__file__).resolve().parent
OUT = HERE / "__cadgen__" / "umbilical-study.npz"
SAMPLE_MM = 1.2


def sample(shape, spacing=SAMPLE_MM):
    """Points on a shape's surface about `spacing` apart (tessellation vertices plus triangle fill)."""
    verts, tris = shape.tessellate(0.2, 0.5)
    V = np.array([[v.X, v.Y, v.Z] for v in verts], float).reshape(-1, 3)
    T = np.array(tris, int).reshape(-1, 3)
    if len(T) == 0:
        return V
    out = [V]
    A, B, D = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    for a, b, d in zip(A, B, D):
        longest = max(np.linalg.norm(b - a), np.linalg.norm(d - a), np.linalg.norm(d - b))
        k = int(math.ceil(longest / spacing))
        if k <= 1:
            out.append(((a + b + d) / 3)[None])
            continue
        u, v = np.meshgrid(np.arange(k + 1), np.arange(k + 1))
        keep = (u + v) <= k
        u, v = u[keep] / k, v[keep] / k
        out.append(a + np.outer(u, b - a) + np.outer(v, d - a))
    return np.vstack(out)


def profile(solids, origin, direction, t_max):
    """[(label, t0, t1)] material intervals along a ray, nearest first, within 0..t_max."""
    rows = []
    for label, solid in solids:
        try:
            for t0, t1 in C.ray(solid, origin, direction):
                if t1 > 0 and t0 < t_max:
                    rows.append((label, round(max(t0, 0.0), 2), round(min(t1, t_max), 2)))
        except Exception as exc:   # shell-only vendor leaves have no closed solid to classify
            rows.append((label + " (ray failed: %s)" % type(exc).__name__, None, None))
    return sorted(rows, key=lambda r: (r[1] is None, r[1]))


def on_line(box, origin, direction, t_max, pad=0.5):
    """True when a bounding box (x0, y0, z0, x1, y1, z1) meets the ray segment."""
    o, d = np.array(origin, float), np.array(direction, float)
    lo, hi = np.array(box[:3]) - pad, np.array(box[3:]) + pad
    t0, t1 = 0.0, t_max
    for k in range(3):
        if abs(d[k]) < 1e-9:
            if o[k] < lo[k] or o[k] > hi[k]:
                return False
            continue
        a, b = (lo[k] - o[k]) / d[k], (hi[k] - o[k]) / d[k]
        t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
    return t0 <= t1


def main():
    entry = C.load_entry()
    import layout_model as m
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    origin = np.array(entry.HEAD_ORIGIN_IN_CHASSIS, float)
    report = dict(script="study_umbilical_geometry", head_origin_world=[round(v, 4) for v in origin],
                  pitch_axis=[m.PITCH_AXIS.position.X, 0.0, m.PITCH_AXIS.position.Z],
                  roll_axis=[0.0, m.ROLL_AXIS.position.Y, m.ROLL_AXIS.position.Z],
                  yaw_axis_x=m.YAW_AXIS.position.X)

    # ---- head: samples by frame, and the named rear parts' boxes
    head = {n: (d["shape"], d["frame"]) for n, d in parts.items() if d["kind"] == "physical"}
    clouds = {"Y": [], "P": [], "R": []}
    for name, (shape, frame) in head.items():
        try:
            clouds[frame if frame in clouds else "Y"].append(sample(shape))
        except Exception as exc:
            print("sample failed", name, exc)
    clouds = {f: np.vstack(v) for f, v in clouds.items()}
    C.log("head sampled: " + ", ".join(f"{f} {len(v)}" for f, v in clouds.items()))
    rear = ("removable_octagonal_rear_cover", "roll_STS3045M_reference", "rear_pitch_trim_washer_stack_max_-30",
            "rear_pitch_trim_washer_stack_max_+30", "connected_pitch_frame_roll_servo_saddle", "main_octagonal_skin",
            "main_octagonal_skin_lower", "rear_M2x6_3", "rear_M2x6_4")
    report["head_rear_boxes_local"] = {n: [round(v, 2) for v in C._box(head[n][0])] for n in rear}

    # ---- rear cover: what a hole through the cover meets, as the roll frame sees it
    r_solids = [(n, s) for n, (s, f) in head.items() if f == "R"]
    p_near = [(n, s) for n, (s, f) in head.items() if f == "P" and C._box(s)[0] < -70.0]
    cover_rows = []
    for roll in (0.0, 10.5, -10.5, 21.0, -21.0):
        # R-fixed view: the pitch-frame parts appear turned by -roll about the roll axis
        p_turned = [(n, s.rotate(m.ROLL_AXIS, -roll)) for n, s in p_near] if roll else p_near
        for y in (-25.0, -21.0, -17.0, -13.0, -7.0, -1.0, 5.0, 11.0, 15.0, 19.0, 23.0):
            for z in np.arange(26.0, 84.1, 2.0):
                o, d, t_max = (-130.0, y, float(z)), (1.0, 0.0, 0.0), 60.0
                near = [(n, s) for n, s in (r_solids if roll == 0.0 else []) + p_turned
                        if on_line(C._box(s), o, d, t_max)]
                rows = profile(near, o, d, t_max)
                cover_rows.append(dict(roll=roll, y=y, z=float(z),
                                       hits=[(n, None if a is None else round(-130.0 + a, 2), None if b is None else round(-130.0 + b, 2))
                                             for n, a, b in rows]))
    report["rear_cover_rays_local_x"] = cover_rows
    C.log("rear cover rays done")

    # ---- body: droid tree, exit rays and samples near the rear top
    entry, tree, leaves = C.droid_tree(entry)
    solids = [lf for lf in leaves if C.is_part(lf.path) and not lf.vendor]
    exits = []
    for name, y in (("A centre", 0.0), ("B +Y", 18.0), ("B -Y", -18.0), ("B +Y 24", 24.0), ("B -Y 24", -24.0)):
        for z in np.arange(116.0, 140.1, 1.0):
            o, d, t_max = (-80.0, y, float(z)), (1.0, 0.0, 0.0), 70.0
            near = [("/".join(lf.path[-2:]), lf.shape) for lf in solids if on_line(lf.box, o, d, t_max)]
            exits.append(dict(exit=name, y=y, z=float(z),
                              hits=[(n, None if a is None else round(-80.0 + a, 2), None if b is None else round(-80.0 + b, 2))
                                    for n, a, b in profile(near, o, d, t_max)]))
    for sy in (1.0, -1.0):
        for x in (-41.0, -38.0, -35.0, -32.0, -29.0):
            for ya in (52.0, 56.0, 60.0, 63.0):
                o, d, t_max = (x, sy * ya, 160.0), (0.0, 0.0, -1.0), 60.0
                near = [("/".join(lf.path[-2:]), lf.shape) for lf in solids if on_line(lf.box, o, d, t_max)]
                exits.append(dict(exit="C deck %s" % ("+Y" if sy > 0 else "-Y"), x=x, y=sy * ya,
                                  hits=[(n, None if a is None else round(160.0 - a, 2), None if b is None else round(160.0 - b, 2))
                                        for n, a, b in profile(near, o, d, t_max)]))
    report["exit_rays_world"] = exits
    C.log("exit rays done")

    # parts with anything behind X 5 and above Z 85: what a hose behind the body could touch
    body_pts, labels = [], []
    for lf in solids:
        b = lf.box
        if b[0] > 5.0 or b[5] < 85.0:
            continue
        try:
            pts = sample(lf.shape)
        except Exception as exc:
            print("sample failed", lf.label, exc)
            continue
        pts = pts[(pts[:, 0] < 5.0) & (pts[:, 2] > 85.0)]
        if len(pts):
            body_pts.append(pts)
            labels.append((lf.label, len(pts)))
    body = np.vstack(body_pts)
    C.log(f"body sampled: {len(body)} points from {len(labels)} parts")
    report["body_parts_sampled"] = labels

    OUT.parent.mkdir(exist_ok=True)
    np.savez_compressed(OUT, head_Y=clouds["Y"], head_P=clouds["P"], head_R=clouds["R"], body=body,
                        origin=origin, pitch_axis=np.array(report["pitch_axis"]), roll_axis=np.array(report["roll_axis"]),
                        yaw_axis_x=np.array([report["yaw_axis_x"]]))
    (HERE / "study_umbilical_geometry-report.json").write_text(json.dumps(report, indent=1) + "\n")
    C.log("written " + OUT.name)


if __name__ == "__main__":
    main()
