"""D-107 Level 2 study, stage 2: the head umbilical's free span over the motion envelope.

Read-only; edits nothing. Needs __cadgen__/umbilical-study.npz from study_umbilical_geometry.py.
Runs on numpy/scipy/matplotlib alone (the legacy runtime has them).

The hose is a bending rod of fixed length, clamped in position and direction at the body's
exit-hood mouth and at the head's cuff mouth, with its own weight. Twist is free (the wires
lie loose in the hose), so the energy is bending + weight. For each configuration (body exit,
head entry point, cuff heading, hood tilt, length) and each pose of yaw x pitch x roll to the
hard stops, it finds the lowest-energy shape by continuation from the neighbouring pose and
reports:

- the smallest bend radius;
- how far the hose reaches behind the body exit, and sideways;
- the force and the yaw and pitch torques the hose puts on the head;
- the clearance from the hose surface to the body parts and to the yaw-, pitch- and
  roll-carried head parts (surface samples, KD-trees), away from its two clamps. A soft
  contact penalty keeps the hose from passing through parts, so a small clearance means
  the hose is resting on that part.

Usage:
    python study_umbilical_span.py --screen        coarse poses, every configuration
    python study_umbilical_span.py --full KEY ...  full pose grid for the named configurations
    python study_umbilical_span.py --plot KEY      pictures of one configuration
    python study_umbilical_span.py --neck DX L R   centre route: full pitch x roll grid and its picture
    python study_umbilical_span.py --record        every case head-umbilical-plan.md section 11 quotes

Everything here is an estimate (E): the stiffness and weight are assumed until the hang test
(T1) measures them, contact is a soft penalty without friction, and the clamps are points
with a fixed heading, not printed bell mouths.
"""

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree

HERE = Path(__file__).resolve().parent
NPZ = HERE / "__cadgen__" / "umbilical-study.npz"
REPORT = HERE / "study_umbilical_span-report.json"

YAW_STOP, PITCH_STOP, ROLL_STOP = 61.0, (-25.0, 43.0), 21.0
HOSE_R = 5.0                    # hose outside radius, mm (E: 10 mm conduit)
EI_LIMIT = 24000.0              # N mm^2: plan 3.1 stiffness ceiling
EI_CASES = (6000.0, 12000.0, 24000.0)
Q = 1.0e-3                      # N/mm: about 0.1 g/mm of hose plus bundle (E)
N_SEG = 48
CLAMP_SKIP = 18.0               # mm of hose at each clamp left out of the clearance to its own mount
YAW_TORQUE_LIMIT = 50.0         # N mm (0.05 N m)

# Body exits: hood-mouth centre (world) for the free span's start.
EXITS = {
    "A": dict(p=(-54.0, 0.0, 155.0), note="centre panel notch; hood mouth behind the disc rim at disc-top height"),
    "B": dict(p=(-54.0, -18.0, 155.0), note="off-centre panel notch on the PCB-08 side (-Y)"),
    "C": dict(p=(-36.0, -58.0, 146.0), note="rear deck corner (-Y)"),
}
# Head entries: the hole through the rear cover, head-local in the roll frame. The cover's outer
# face is X -115. The cuff is an elbow: its centre stands ELBOW_OUT behind the face and its
# mouth CUFF_OUT further back along the hose heading.
ELBOW_OUT, CUFF_OUT = 9.0, 8.0
ENTRIES = {
    "top": dict(y=-1.0, z=76.0, note="above the roll servo, between the trim stacks; nothing behind the cover"),
    "mid": dict(y=-16.0, z=48.0, note="beside the roll servo at roll-axis height; 20 mm pocket to the saddle"),
    "low": dict(y=-16.0, z=32.0, note="beside the roll servo, low; 20 mm pocket to the saddle"),
}
CUFF_HEADINGS = (-30.0, 0.0, 30.0, 60.0, 90.0)   # hose travel direction at the cuff: deg above +X in the head's X-Z plane
HOOD_TILTS = (0.0, 30.0)                   # hood mouth leaning rearward from vertical, deg


def rot(axis, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return {"x": np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            "y": np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            "z": np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]


class Head:
    """Head-frame transforms. CAD angles: right-hand about +Z (yaw), +Y (pitch), +X (roll)."""

    def __init__(self, npz):
        self.o = npz["origin"]
        self.pa, self.ra = npz["pitch_axis"], npz["roll_axis"]
        self.ya = np.array([float(npz["yaw_axis_x"][0]), 0.0, 0.0])

    def mats(self, yaw, pitch, roll):
        return rot("z", yaw), rot("y", pitch), rot("x", roll)

    def to_world(self, p, frame, yaw, pitch, roll):
        """Head-local points riding `frame` (R, P or Y) to world."""
        Rz, Ry, Rx = self.mats(yaw, pitch, roll)
        p = np.atleast_2d(np.asarray(p, float))
        if frame == "R":
            p = self.ra + (p - self.ra) @ Rx.T
        if frame in ("R", "P"):
            p = self.pa + (p - self.pa) @ Ry.T
        p = self.ya + (p - self.ya) @ Rz.T
        return p + self.o

    def to_frame(self, w, frame, yaw, pitch, roll):
        """World points into the head-local coordinates of `frame`."""
        Rz, Ry, Rx = self.mats(yaw, pitch, roll)
        p = np.atleast_2d(np.asarray(w, float)) - self.o
        p = self.ya + (p - self.ya) @ Rz
        if frame in ("R", "P"):
            p = self.pa + (p - self.pa) @ Ry
        if frame == "R":
            p = self.ra + (p - self.ra) @ Rx
        return p

    def vec_to_world(self, v, frame, yaw, pitch, roll):
        """Row vectors expressed in `frame` coordinates, turned into world directions."""
        Rz, Ry, Rx = self.mats(yaw, pitch, roll)
        v = np.atleast_2d(v)
        if frame == "R":
            v = v @ Rx.T
        if frame in ("R", "P"):
            v = v @ Ry.T
        return v @ Rz.T

    def dir_world(self, d, yaw, pitch, roll):
        Rz, Ry, Rx = self.mats(yaw, pitch, roll)
        return Rz @ Ry @ Rx @ np.asarray(d, float)


# ---------------------------------------------------------------- rod

def energy(xfree, x, free, l, ei, q, ks, contact=None):
    x = x.copy()
    x[free] = xfree.reshape(-1, 3)
    e = np.diff(x, axis=0)
    ln = np.linalg.norm(e, axis=1)
    t = e / ln[:, None]
    cosang = np.einsum("ij,ij->i", t[:-1], t[1:])
    eb = ei / l * np.sum(1.0 - cosang)
    es = 0.5 * ks * np.sum((ln - l) ** 2)
    eg = q * l * np.sum(0.5 * (x[:-1, 2] + x[1:, 2]))
    # gradient with respect to edges, then vertices
    nb = np.zeros_like(t)
    nb[:-1] += t[1:]
    nb[1:] += t[:-1]
    ge = -(ei / l) * (nb - t * np.einsum("ij,ij->i", t, nb)[:, None]) / ln[:, None] + ks * (ln - l)[:, None] * t
    g = np.zeros_like(x)
    g[1:] += ge
    g[:-1] -= ge
    g[:-1, 2] += 0.5 * q * l
    g[1:, 2] += 0.5 * q * l
    ec = 0.0
    if contact is not None:
        ec, gc = contact(x)
        g = g + gc
    return eb + es + eg + ec, g


def bezier_guess(p0, d0, p1, d1, length, n):
    """Cubic Bezier from p0 along d0 into p1 along d1 with arc length `length`, at n+1 points."""
    def curve(a):
        s = np.linspace(0, 1, 400)[:, None]
        c0, c1, c2, c3 = p0, p0 + a * d0, p1 - a * d1, p1
        return (1 - s) ** 3 * c0 + 3 * (1 - s) ** 2 * s * c1 + 3 * (1 - s) * s ** 2 * c2 + s ** 3 * c3
    lo, hi = 1.0, 3.0 * length
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        pts = curve(mid)
        if np.sum(np.linalg.norm(np.diff(pts, axis=0), axis=1)) < length:
            lo = mid
        else:
            hi = mid
    pts = curve(0.5 * (lo + hi))
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    target = np.linspace(0, s[-1], n + 1)
    return np.stack([np.interp(target, s, pts[:, k]) for k in range(3)], axis=1)


def solve(x0, p0, d0, p1, d1, length, ei, q=Q, n=N_SEG, contact=None):
    """Equilibrium vertices (n+1, 3) and the full energy gradient (reactions on the clamped vertices)."""
    l = length / n
    x = x0.copy()
    x[0], x[1], x[-2], x[-1] = p0, p0 + l * d0, p1 - l * d1, p1
    free = np.zeros(n + 1, bool)
    free[2:-2] = True
    ks = 50.0 * ei / l ** 3      # stretch penalty: segment length error stays under 0.05 %
    res = minimize(lambda v: _fg(v, x, free, l, ei, q, ks, contact), x[free].ravel(), jac=True, method="BFGS",
                   options=dict(maxiter=6000, gtol=2e-5) if contact is None else dict(maxiter=500, gtol=5e-4))
    x[free] = res.x.reshape(-1, 3)
    _, g = energy(res.x, x, free, l, ei, q, ks, contact)
    return x, g, float(np.abs(g[free]).max())


def _fg(v, x, free, l, ei, q, ks, contact=None):
    f, g = energy(v, x, free, l, ei, q, ks, contact)
    return f, g[free].ravel()


def carry(x_prev, p0, p1_old, p1_new):
    """Previous shape with its head end moved: the shift fades linearly along the hose."""
    s = np.linspace(0, 1, len(x_prev))[:, None]
    return x_prev + s * (p1_new - p1_old)


def bend_radius(x):
    e = np.diff(x, axis=0)
    ln = np.linalg.norm(e, axis=1)
    t = e / ln[:, None]
    cosang = np.clip(np.einsum("ij,ij->i", t[:-1], t[1:]), -1, 1)
    kappa = 2.0 * np.tan(0.5 * np.arccos(cosang)) / (0.5 * (ln[:-1] + ln[1:]))
    return 1.0 / max(kappa.max(), 1e-9)


# ---------------------------------------------------------------- configurations and poses

def config_key(exit_name, entry, heading, tilt, length):
    return f"{exit_name}-{entry}-h{heading:+.0f}-t{tilt:.0f}-L{length:.0f}"


def pose_order(yaws, pitches, rolls):
    """Poses ordered so each one neighbours an earlier one: pitch out from 0, roll out from 0, yaw out from 0."""
    def outward(vals):
        vals = sorted(vals, key=abs)
        return vals
    order = []
    for q in outward(pitches):
        for r in outward(rolls):
            for y in outward(yaws):
                order.append((y, q, r))
    return order


def neighbour(pose, done, steps):
    """The solved pose to start from: one step back toward 0 on yaw, else roll, else pitch."""
    y, q, r = pose
    def back(v, vals):
        vals = sorted(vals, key=abs)
        same = [u for u in vals if (u > 0) == (v > 0) and abs(u) < abs(v)] or [0.0]
        return max(same, key=abs) if v != 0 else 0.0
    for cand in ((back(y, steps[0]), q, r), (y, q, back(r, steps[2])), (y, back(q, steps[1]), r)):
        if cand != pose and cand in done:
            return cand
    return None


CONTACT_GAP = HOSE_R + 2.0     # the hose centre is pushed out to this distance from any part, mm
CONTACT_K = 0.4                 # N/mm
CONTACT_SKIP = 5                # vertices at each clamp left free of contact (inside the hood and cuff)


def make_contact(head, trees, pose):
    """Soft contact: a penalty that keeps the hose centre CONTACT_GAP off the sampled part surfaces."""
    y, q, r = pose

    def contact(x):
        g = np.zeros_like(x)
        e = 0.0
        sel = np.zeros(len(x), bool)
        sel[CONTACT_SKIP:-CONTACT_SKIP] = True
        for frame in ("body", "Y", "P", "R"):
            pts = x[sel] if frame == "body" else head.to_frame(x[sel], frame, y, q, r)
            d, idx = trees[frame].query(pts)
            pen = np.clip(CONTACT_GAP - d, 0.0, None)
            if not pen.any():
                continue
            away = (pts - trees[frame].data[idx]) / np.maximum(d, 1e-6)[:, None]
            gf = -CONTACT_K * pen[:, None] * away
            if frame != "body":
                gf = head.vec_to_world(gf, frame, y, q, r)
            g[sel] += gf
            e += 0.5 * CONTACT_K * float(np.sum(pen ** 2))
        return e, g
    return contact


def touches(head, trees, pose, x):
    """True when the free shape comes inside the contact gap of any part (clamp ends left out)."""
    y, q, r = pose
    mid = x[CONTACT_SKIP:-CONTACT_SKIP]
    for frame in ("body", "Y", "P", "R"):
        pts = mid if frame == "body" else head.to_frame(mid, frame, y, q, r)
        if trees[frame].query(pts)[0].min() < CONTACT_GAP:
            return True
    return False


def solve_checked(head, trees, pose, guess, p0, d0, p1, d1, length, ei, q, contact):
    """Free equilibrium first; the contact solve (about 50 times slower) only when the free shape touches."""
    x, g, resid = solve(guess, p0, d0, p1, d1, length, ei, q=q)
    if contact and touches(head, trees, pose, x):
        x, g, resid = solve(x, p0, d0, p1, d1, length, ei, q=q, contact=make_contact(head, trees, pose))
    return x, g, resid


def cuff_mouth(en, d_local):
    """Cuff mouth centre, head-local: the elbow centre behind the cover hole, then back along the heading."""
    return np.array([-115.0 - ELBOW_OUT, en["y"], en["z"]]) - CUFF_OUT * np.asarray(d_local)


def run_config(head, trees, exit_name, entry, heading, tilt, length, ei, poses, steps, keep_shapes=False, contact=True):
    ex, en = EXITS[exit_name], ENTRIES[entry]
    p0 = np.array(ex["p"], float)
    d0 = np.array([-math.sin(math.radians(tilt)), 0.0, math.cos(math.radians(tilt))])
    d_local = np.array([math.cos(math.radians(heading)), 0.0, math.sin(math.radians(heading))])
    mouth = cuff_mouth(en, d_local)
    done, rows, shapes = {}, [], {}
    for pose in poses:
        y, q, r = pose
        p1 = head.to_world(mouth, "R", y, q, r)[0]
        d1 = head.dir_world(d_local, y, q, r)
        chord = float(np.linalg.norm(p1 - p0))
        if chord > 0.97 * length:
            rows.append(dict(pose=pose, chord=chord, taut=True))
            continue
        nb = neighbour(pose, done, steps)
        if nb is None:
            guess = bezier_guess(p0, d0, p1, d1, length, N_SEG)
        else:
            guess = carry(done[nb][0], p0, done[nb][1], p1)
        x, g, resid = solve_checked(head, trees, pose, guess, p0, d0, p1, d1, length, ei, Q, contact)
        done[pose] = (x, p1)
        f_head = -(g[-1] + g[-2])
        arm = np.stack([x[-1], x[-2]]) - (head.o + head.ya)
        tz = float(np.sum(np.cross(arm, -g[-2:][::-1])[:, 2]))
        pitch_dir = head.dir_world((0, 1, 0), y, 0, 0)
        arm_p = np.stack([x[-1], x[-2]]) - (head.o + head.ya + np.array([0, 0, head.pa[2]]))
        tp = float(np.sum(np.cross(arm_p, -g[-2:][::-1]) @ pitch_dir))
        s = np.linspace(0, length, len(x))
        clr = {}
        body_part = s > CLAMP_SKIP
        clr["body"] = float(trees["body"].query(x[body_part])[0].min() - HOSE_R)
        for frame in ("Y", "P", "R"):
            sel = (s < length - CLAMP_SKIP) if frame == "R" else np.ones(len(x), bool)
            pts = head.to_frame(x[sel], frame, y, q, r)
            clr[frame] = float(trees[frame].query(pts)[0].min() - HOSE_R)
        rows.append(dict(pose=pose, chord=chord, taut=False, r_min=bend_radius(x), resid=resid,
                         reach_back=float(p0[0] - x[:, 0].min()), x_min=float(x[:, 0].min()),
                         z_max=float(x[:, 2].max()), y_span=float(np.abs(x[:, 1]).max()),
                         f_side=float(np.hypot(f_head[0], f_head[1])), tau_yaw=tz, tau_pitch=tp, clear=clr))
        if keep_shapes:
            shapes[pose] = x
    return rows, shapes


# ---------------------------------------------------------------- centre (neck) route, plan fallback F2

NECK_ANCHOR_Z = 13.0       # head-local Z of the clamp inside the head, under the pitch frame's underside (Z 16.8)
NECK_OPENING = (30.0, 20.0)  # half-length (X) and half-width (Y) of belly skin left out of the contact cloud, mm


def neck_trees(npz, head, opening=None):
    """KD-trees for the neck route: the belly skin round the opening is left out of the roll cloud.

    `opening` is (x0, x1, y0, y1) relative to the yaw axis line, head-local; default the centred NECK_OPENING."""
    R = npz["head_R"]
    px = head.ya[0]
    x0, x1, y0, y1 = opening or (-NECK_OPENING[0], NECK_OPENING[0], -NECK_OPENING[1], NECK_OPENING[1])
    hole = (R[:, 0] - px > x0) & (R[:, 0] - px < x1) & (R[:, 1] > y0) & (R[:, 1] < y1) & (R[:, 2] < 3.0)
    return dict(body=cKDTree(npz["body"]), Y=cKDTree(npz["head_Y"]), P=cKDTree(npz["head_P"]), R=cKDTree(R[~hole]))


def run_neck(head, trees, dx, length, ei, radius, poses, keep_shapes=False, anchor=None, heading=None):
    """The bundle from the yaw disc's bore top, straight up, to a clamp in the head's roll frame.

    On the yaw axis the lower end neither moves nor turns with yaw, so yaw only twists the bundle
    and the shape depends on pitch and roll alone."""
    global HOSE_R, CONTACT_GAP
    keep = HOSE_R, CONTACT_GAP
    HOSE_R, CONTACT_GAP = radius, radius + 1.5
    px = head.ya[0]
    p0 = head.o + np.array([px, 0.0, -34.5 - 3.0])          # 3 mm down the bore: the bell mouth's throat
    d0 = np.array([0.0, 0.0, 1.0])
    # default: clamp on the yaw axis line, bundle arriving straight up; `anchor` (head-local, roll
    # frame) and `heading` (the bundle's travel direction into the clamp) override it
    anchor = np.array([px + dx, 0.0, NECK_ANCHOR_Z]) if anchor is None else np.asarray(anchor, float)
    d_local = np.array([0.0, 0.0, 1.0]) if heading is None else np.asarray(heading, float) / np.linalg.norm(heading)
    done, rows, shapes = {}, [], {}
    steps = (sorted({p[0] for p in poses}), sorted({p[1] for p in poses}), sorted({p[2] for p in poses}))
    try:
        for pose in poses:
            y, q, r = pose
            p1 = head.to_world(anchor, "R", y, q, r)[0]
            d1 = head.dir_world(d_local, y, q, r)
            chord = float(np.linalg.norm(p1 - p0))
            if chord > 0.985 * length:
                rows.append(dict(pose=pose, chord=chord, taut=True))
                continue
            nb = neighbour(pose, done, steps)
            guess = bezier_guess(p0, d0, p1, d1, length, N_SEG) if nb is None else carry(done[nb][0], p0, done[nb][1], p1)
            x, g, resid = solve_checked(head, trees, pose, guess, p0, d0, p1, d1, length, ei, 3.0e-4, True)
            done[pose] = (x, p1)
            f_head = -(g[-1] + g[-2])
            pitch_dir = head.dir_world((0, 1, 0), y, 0, 0)
            arm_p = np.stack([x[-1], x[-2]]) - (head.o + np.array([px, 0.0, head.pa[2]]))
            tp = float(np.sum(np.cross(arm_p, -g[-2:][::-1]) @ pitch_dir))
            local = head.to_frame(x, "R", y, q, r)
            # where the bundle crosses the belly skin (head-local Z 0..1), for the opening's size
            cross = local[(local[:, 2] > -1.5) & (local[:, 2] < 2.5)]
            clr = {}
            for frame in ("Y", "P", "R"):
                sel = np.ones(len(x), bool)
                sel[:CONTACT_SKIP] = frame != "Y"
                sel[-CONTACT_SKIP:] = frame == "Y"
                pts = head.to_frame(x[sel], frame, y, q, r)
                clr[frame] = float(trees[frame].query(pts)[0].min() - radius)
            rows.append(dict(pose=pose, chord=chord, taut=False, r_min=bend_radius(x), resid=resid,
                             reach_back=float(np.hypot(x[:, 0] - p0[0], x[:, 1] - p0[1]).max()), x_min=0.0,
                             z_max=float(x[:, 2].max()), y_span=float(np.abs(x[:, 1]).max()),
                             f_side=float(np.hypot(f_head[0], f_head[1])), tau_yaw=0.0, tau_pitch=tp,
                             clear=dict(body=99.0, **clr),
                             cross=[float(cross[:, 0].min() - px), float(cross[:, 0].max() - px),
                                    float(cross[:, 1].min()), float(cross[:, 1].max())] if len(cross) else None))
            if keep_shapes:
                shapes[pose] = x
    finally:
        HOSE_R, CONTACT_GAP = keep
    return rows, shapes


def summarise(rows):
    ok = [r for r in rows if not r["taut"]]
    out = dict(poses=len(rows), taut=sum(r["taut"] for r in rows), chord_max=max(r["chord"] for r in rows),
               chord_min=min(r["chord"] for r in rows))
    if not ok:
        return out
    def worst(key, fn, sub=None):
        r = fn(ok, key=(lambda r: r[key] if sub is None else r[key][sub]))
        return (round(r[key] if sub is None else r[key][sub], 2), r["pose"])
    out.update(r_min=worst("r_min", min), reach_back_max=worst("reach_back", max), z_max=worst("z_max", max),
               y_span_max=worst("y_span", max), f_side_max=worst("f_side", max),
               tau_yaw_max=max(((round(abs(r["tau_yaw"]), 1), r["pose"]) for r in ok), key=lambda v: v[0]),
               tau_pitch_max=max(((round(abs(r["tau_pitch"]), 1), r["pose"]) for r in ok), key=lambda v: v[0]),
               clear_body=worst("clear", min, "body"), clear_yaw=worst("clear", min, "Y"),
               clear_pitch=worst("clear", min, "P"), clear_roll=worst("clear", min, "R"),
               resid_max=round(max(r["resid"] for r in ok), 5))
    neutral = next((r for r in ok if tuple(r["pose"]) == (0.0, 0.0, 0.0)), None)
    if neutral:
        out["neutral"] = dict(r_min=round(neutral["r_min"], 1), reach_back=round(neutral["reach_back"], 1),
                              z_max=round(neutral["z_max"], 1), chord=round(neutral["chord"], 1))
    return out


def grids(kind):
    if kind == "screen":
        return ((-YAW_STOP, -30.0, 0.0, 30.0, YAW_STOP), (PITCH_STOP[0], 0.0, 20.0, PITCH_STOP[1]), (-ROLL_STOP, 0.0, ROLL_STOP))
    yaws = tuple(np.round(np.linspace(-YAW_STOP, YAW_STOP, 13), 3))
    pitches = (-25.0, -17.0, -8.5, 0.0, 8.5, 17.0, 26.0, 34.5, 43.0)
    rolls = (-21.0, -10.5, 0.0, 10.5, 21.0)
    return yaws, pitches, rolls


def load():
    npz = np.load(NPZ)
    head = Head(npz)
    trees = dict(body=cKDTree(npz["body"]), Y=cKDTree(npz["head_Y"]), P=cKDTree(npz["head_P"]), R=cKDTree(npz["head_R"]))
    return npz, head, trees


def parse_key(key):
    parts = key.split("-")
    ex, en = parts[0], parts[1]
    rest = key[len(ex) + len(en) + 2:]
    h = float(rest.split("-t")[0][1:])
    t = float(rest.split("-t")[1].split("-L")[0])
    l = float(rest.split("-L")[1])
    return ex, en, h, t, l


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen", action="store_true")
    ap.add_argument("--full", nargs="*")
    ap.add_argument("--plot")
    ap.add_argument("--ei", type=float, default=12000.0)
    ap.add_argument("--exits", nargs="*", default=["A", "C"], help="exits to screen (B behaves as A shifted 18 mm)")
    ap.add_argument("--neck", nargs=3, type=float, metavar=("DX", "LENGTH", "RADIUS"),
                    help="centre route: solve the full pitch x roll grid and plot it")
    ap.add_argument("--record", action="store_true",
                    help="re-run every case quoted in head-umbilical-plan.md section 11 into the report (about 30 min)")
    args = ap.parse_args()
    npz, head, trees = load()
    report = json.loads(REPORT.read_text()) if REPORT.exists() else dict(script="study_umbilical_span")
    report["assumptions"] = dict(hose_radius_mm=HOSE_R, q_N_per_mm=Q, ei_limit=EI_LIMIT, segments=N_SEG,
                                 clamp_skip_mm=CLAMP_SKIP, cuff_out_mm=CUFF_OUT, elbow_out_mm=ELBOW_OUT,
                                 stops=dict(yaw=YAW_STOP, pitch=PITCH_STOP, roll=ROLL_STOP))

    if args.screen:
        steps = grids("screen")
        poses = pose_order(*steps)
        out = {}
        for ex, en, h, t in itertools.product(args.exits, ENTRIES, CUFF_HEADINGS, HOOD_TILTS):
            # the longest chord sets the length: 10 % margin (plan 3.1), rounded up to 5 mm
            p0 = np.array(EXITS[ex]["p"])
            d_local = np.array([math.cos(math.radians(h)), 0.0, math.sin(math.radians(h))])
            mouth = cuff_mouth(ENTRIES[en], d_local)
            full = pose_order(*grids("full"))
            chord = max(float(np.linalg.norm(head.to_world(mouth, "R", *p)[0] - p0)) for p in full)
            length = 5.0 * math.ceil(1.10 * chord / 5.0)
            key = config_key(ex, en, h, t, length)
            rows, _ = run_config(head, trees, ex, en, h, t, length, args.ei, poses, steps)
            out[key] = summarise(rows)
            s = out[key]
            print(key, "chord", round(s["chord_min"]), round(s["chord_max"]), "rmin", s.get("r_min"), "back", s.get("reach_back_max"),
                  "tyaw", s.get("tau_yaw_max"), "clr b/Y/P/R", s.get("clear_body"), s.get("clear_yaw"), s.get("clear_pitch"), s.get("clear_roll"),
                  flush=True)
        report["screen"] = dict(ei=args.ei, poses=len(poses), configs=out)

    if args.full:
        steps = grids("full")
        poses = pose_order(*steps)
        report.setdefault("full", {})
        for key in args.full:
            ex, en, h, t, length = parse_key(key)
            for ei in EI_CASES:
                rows, _ = run_config(head, trees, ex, en, h, t, length, ei, poses, steps)
                s = summarise(rows)
                report["full"].setdefault(key, {})[f"EI {ei:.0f}"] = s
                print(key, "EI", ei, json.dumps(s), flush=True)

    REPORT.write_text(json.dumps(report, indent=1, default=lambda v: v.tolist() if hasattr(v, "tolist") else v) + "\n")

    if args.plot:
        plot(args.plot, npz, head, trees, args.ei)

    if args.record:
        record(npz, head, trees)

    if args.neck:
        dx, length, radius = args.neck
        pitches = (-25.0, -17.0, -8.5, 0.0, 8.5, 17.0, 26.0, 34.5, 43.0)
        rolls = (-21.0, -10.5, 0.0, 10.5, 21.0)
        poses = pose_order((0.0,), pitches, rolls)
        ntrees = neck_trees(npz, head)
        report = json.loads(REPORT.read_text()) if REPORT.exists() else dict(script="study_umbilical_span")
        report.setdefault("neck", {})
        shapes = {}
        for ei in (2000.0, 8000.0):
            rows, sh = run_neck(head, ntrees, dx, length, ei, radius, poses, keep_shapes=True)
            summ = summarise(rows)
            cr = [r["cross"] for r in rows if not r["taut"] and r["cross"]]
            summ["belly_crossing_envelope_local"] = ([min(c[0] for c in cr), max(c[1] for c in cr),
                                                      min(c[2] for c in cr), max(c[3] for c in cr)] if cr else None)
            report["neck"][f"dx{dx:+.0f}-L{length:.0f}-r{radius:.1f}-EI{ei:.0f}"] = summ
            print("neck", dx, length, radius, ei, json.dumps(summ), flush=True)
            if ei == 2000.0:
                shapes = sh
        REPORT.write_text(json.dumps(report, indent=1, default=lambda v: v.tolist() if hasattr(v, "tolist") else v) + "\n")
        plot_neck(npz, head, shapes, dx, length, radius)


def plot(key, npz, head, trees, ei):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ex, en, h, t, length = parse_key(key)
    steps = grids("screen")
    rows, shapes = run_config(head, trees, ex, en, h, t, length, ei, pose_order(*steps), steps, keep_shapes=True)
    views = [("Neutral", (0.0, 0.0, 0.0)), ("Chin up 25", (0.0, -25.0, 0.0)), ("Chin down 43", (0.0, 43.0, 0.0)),
             ("Yaw 61", (61.0, 0.0, 0.0)), ("Yaw 61, chin down 43", (61.0, 43.0, 0.0)), ("Yaw -61, chin up 25", (-61.0, -25.0, 0.0))]
    body = npz["body"]
    rng = np.random.default_rng(0)
    def thin(p, k):
        return p if len(p) <= k else p[rng.choice(len(p), k, replace=False)]
    fig, axes = plt.subplots(2, len(views), figsize=(4.2 * len(views), 9.5), constrained_layout=True)
    for col, (title, pose) in enumerate(views):
        cloud = [thin(body, 60000)]
        for frame, name in (("Y", "head_Y"), ("P", "head_P"), ("R", "head_R")):
            cloud.append(head.to_world(thin(npz[name], 60000), frame, *pose))
        cloud = np.vstack(cloud)
        for row, (a, b, la, lb) in enumerate(((0, 2, "X, mm (rear to the left)", "Z, mm"), (1, 2, "Y, mm (seen from behind)", "Z, mm"))):
            ax = axes[row, col]
            ax.scatter(cloud[:, a], cloud[:, b], s=0.05, c="#9aa3ad", linewidths=0)
            if pose in shapes:
                x = shapes[pose]
                ax.plot(x[:, a], x[:, b], color="#c0392b", lw=5.5, solid_capstyle="round")
                ax.plot(x[[0, -1], a], x[[0, -1], b], "o", color="#1f2d3a", ms=5)
            ax.set_aspect("equal")
            ax.set_xlim((-150, 110) if a == 0 else (-120, 120))
            ax.set_ylim(60, 310)
            ax.set_xlabel(la)
            ax.set_ylabel(lb)
            if row == 0:
                r = next((r for r in rows if tuple(r["pose"]) == pose and not r["taut"]), None)
                ax.set_title(title + ("" if r is None else f"\nbend radius {r['r_min']:.0f} mm, {r['reach_back']:.0f} mm behind the exit"), fontsize=10)
    fig.suptitle(f"Head umbilical, solved hose shape (estimate): {key}, EI {ei:.0f} N mm2, hose 10 mm", fontsize=12)
    out = HERE / "snapshots" / f"umbilical-loop-{key}.png"
    fig.savefig(out, dpi=110)
    print("wrote", out)


# Cases quoted in head-umbilical-plan.md section 11.
RECORD_REAR = [("A", "top", 0.0, 0.0), ("A", "top", 30.0, 0.0), ("A", "mid", 60.0, 0.0)]
RECORD_REAR_SLACK = (1.15, 1.30)
RECORD_REAR_EI = (3000.0, 12000.0)
RECORD_NECK_DIRS = {"fwd": ((1, 0), (1, 0, 0)), "aft": ((-1, 0), (-1, 0, 0)), "side-Y": ((0, -1), (0, -1, 0)),
                    "fwd-side": ((0.7071, -0.7071), (1, -1, 0))}
RECORD_NECK_OFFSETS = (20.0, 30.0)
RECORD_NECK_Z = 6.0
RECORD_NECK_SLACK = (1.12, 1.30)


def _length(head, p0, mouth_local, poses, slack):
    chord = max(float(np.linalg.norm(head.to_world(mouth_local, "R", *p)[0] - p0)) for p in poses)
    return 5.0 * math.ceil(slack * chord / 5.0)


def record(npz, head, trees):
    """Every case section 11 quotes, written to the report: rear set-ups and centre-route clamp layouts."""
    report = json.loads(REPORT.read_text()) if REPORT.exists() else dict(script="study_umbilical_span")
    full = pose_order(*grids("full"))
    steps = grids("screen")
    screen = pose_order(*steps)
    rear = {}
    for ex, en, h, t in RECORD_REAR:
        p0 = np.array(EXITS[ex]["p"])
        d_local = np.array([math.cos(math.radians(h)), 0.0, math.sin(math.radians(h))])
        mouth = cuff_mouth(ENTRIES[en], d_local)
        for slack in RECORD_REAR_SLACK:
            length = _length(head, p0, mouth, full, slack)
            for ei in RECORD_REAR_EI:
                rows, _ = run_config(head, trees, ex, en, h, t, length, ei, screen, steps)
                key = f"{config_key(ex, en, h, t, length)} EI {ei:.0f}"
                rear[key] = dict(slack=slack, **summarise(rows))
                print("rear", key, json.dumps(rear[key], default=float), flush=True)
    report["rear_record"] = dict(poses=len(screen), grid="screen (yaw 5 x pitch 4 x roll 3)", cases=rear)
    REPORT.write_text(json.dumps(report, indent=1, default=lambda v: v.tolist() if hasattr(v, "tolist") else v) + "\n")

    pitches = (-25.0, -17.0, -8.5, 0.0, 8.5, 17.0, 26.0, 34.5, 43.0)
    rolls = (-21.0, -10.5, 0.0, 10.5, 21.0)
    poses = pose_order((0.0,), pitches, rolls)
    px = head.ya[0]
    p0 = head.o + np.array([px, 0.0, -37.5])
    wide = neck_trees(npz, head, opening=(-60.0, 60.0, -50.0, 50.0))
    clamps = {}
    for name, ((ux, uy), hd) in RECORD_NECK_DIRS.items():
        for off in RECORD_NECK_OFFSETS:
            anchor = np.array([px + ux * off, uy * off, RECORD_NECK_Z])
            for slack in RECORD_NECK_SLACK:
                length = _length(head, p0, anchor, poses, slack)
                rows, _ = run_neck(head, wide, 0.0, length, 2000.0, 3.5, poses, anchor=anchor, heading=hd)
                summ = summarise(rows)
                cr = [r["cross"] for r in rows if not r["taut"] and r["cross"]]
                summ["belly_crossing_envelope_local"] = ([min(c[0] for c in cr), max(c[1] for c in cr),
                                                          min(c[2] for c in cr), max(c[3] for c in cr)] if cr else None)
                key = f"{name} off{off:.0f} z{RECORD_NECK_Z:.0f} L{length:.0f} EI2000"
                clamps[key] = summ
                print("neck", key, json.dumps(summ, default=float), flush=True)
                report["neck_clamp_record"] = dict(poses=len(poses), cases=clamps)
                REPORT.write_text(json.dumps(report, indent=1, default=lambda v: v.tolist() if hasattr(v, "tolist") else v) + "\n")


def plot_neck(npz, head, shapes, dx, length, radius):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    views = [("Neutral", (0.0, 0.0, 0.0)), ("Chin up 25", (0.0, -25.0, 0.0)), ("Chin down 43", (0.0, 43.0, 0.0)),
             ("Chin down 43, roll 21", (0.0, 43.0, 21.0)), ("Chin up 25, roll -21", (0.0, -25.0, -21.0))]
    rng = np.random.default_rng(0)
    px = head.ya[0] + head.o[0]
    fig, axes = plt.subplots(2, len(views), figsize=(4.0 * len(views), 8.5), constrained_layout=True)
    for col, (title, pose) in enumerate(views):
        cloud = []
        for frame, name in (("Y", "head_Y"), ("P", "head_P"), ("R", "head_R")):
            pts = npz[name]
            pts = pts[rng.choice(len(pts), min(len(pts), 120000), replace=False)]
            w = head.to_world(pts, frame, *pose)
            cloud.append(w[np.abs(w[:, 1]) < 4.0] if True else w)
        cloud_xz = np.vstack(cloud)
        cloud_yz = []
        for frame, name in (("Y", "head_Y"), ("P", "head_P"), ("R", "head_R")):
            pts = npz[name]
            pts = pts[rng.choice(len(pts), min(len(pts), 120000), replace=False)]
            w = head.to_world(pts, frame, *pose)
            cloud_yz.append(w[np.abs(w[:, 0] - px) < 4.0])
        cloud_yz = np.vstack(cloud_yz)
        for row, (cl, a, la) in enumerate(((cloud_xz, 0, "X, mm (section at Y 0)"), (cloud_yz, 1, "Y, mm (section through the yaw axis)"))):
            ax = axes[row, col]
            ax.scatter(cl[:, a], cl[:, 2], s=0.15, c="#9aa3ad", linewidths=0)
            if pose in shapes:
                x = shapes[pose]
                ax.plot(x[:, a], x[:, 2], color="#c0392b", lw=2 * radius * 0.9, solid_capstyle="round", alpha=0.85)
            ax.set_aspect("equal")
            c = px if a == 0 else 0.0
            ax.set_xlim(c - 60, c + 60)
            ax.set_ylim(140, 250)
            ax.set_xlabel(la)
            ax.set_ylabel("Z, mm")
            if row == 0:
                ax.set_title(title, fontsize=10)
    fig.suptitle(f"Centre route (estimate): bundle from the disc bore to a clamp in the head, {length:.0f} mm, "
                 f"bundle {2 * radius:.0f} mm, EI 2000 N mm2", fontsize=11)
    out = HERE / "snapshots" / f"umbilical-neck-dx{dx:+.0f}-L{length:.0f}.png"
    fig.savefig(out, dpi=110)
    print("wrote", out)


if __name__ == "__main__":
    main()
