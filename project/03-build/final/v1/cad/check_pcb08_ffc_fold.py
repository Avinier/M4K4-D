"""PCB-08 W42/W43 fold prediction: cassette window -> two FH34SRJ mouths.

The two FFCs leave the BO-059 cassette's 300 deg window radially, on edge
(width vertical, Z 121.35..132.85, stacked through their thickness). They
reach PCB-08 flat, width along Y over contacts 1..22 (Y -28.25..-38.75),
travelling -X into J3 (outer, Z 114.1) and J4 (inner, raised over J3 at
Z 115.05, then the D-100 S-bend). The path, as one two-cable band:

1. 1.0 mm straight out of the window along the 300 deg radial.
2. On-edge curl, R 4 mm about Z, 30 deg clockwise to run -Y (a bend
   through the thickness, like the rolling loop).
3. -Y run at X 28.79 to the crease.
4. One creased 45 deg fold that turns the band straight down; the crease
   runs from (Y -27.75, top edge) to (Y -39.25, bottom edge) so the width
   lands on the contact span. The folded part lies on the +X side.
5. Short descent, then a curl about Y (R 3.5 mm at the band centre) that
   lays both cables flat travelling -X: the curl's outer layer ends lowest
   (J3), the inner one 0.95 mm higher (J4's raised run).
6. Flat runs into the mouths (J3) and over J3 to the S-bend (J4).

Checks: each solid clears the robot's parts and the CSI drop reserve; the
end Z values meet the stepped probe; and a frame calculation follows
conductor 1 from the cassette to both PCB-08 ZIFs and on through the D-052
drum-core fold to PCB-14's lower ZIF. Estimates (E): band spacing 0.95 mm,
FFC 0.3 mm, curl radii 3-4 mm (about 10x the FFC). Paper geometry, not a
physical cable.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
"""

import math

import numpy as np
from build123d import Box, Plane

import module_checks as C

AXIS_X = 16.0                          # BODY_AXIS_X
WALL_R = 23.5                          # cassette wall outer face
EXIT_DEG = 300.0
Z_LO, Z_HI = 121.35, 132.85            # YAW_FFC_BAND_Z: FFC width on edge
W_Y = (-39.25, -27.75)                 # 11.5 mm cable span over contacts 22..1
PAD1_Y, PAD22_Y = -28.25, -38.75       # J3/J4 contact positions (KiCad board)
LAYER, FFC_T = 0.95, 0.3               # centre spacing of the two cables, FFC thickness
BAND_T = LAYER + FFC_T
R_EDGE = 4.0                           # on-edge curl, band centreline
R_DOWN = 3.5                           # down-to-flat curl, band centreline
Z_OUTER, Z_INNER = 114.1, 115.05       # stepped probe: J3 mouth, J4 raised run
J3_MOUTH, J3_STIFF = 19.5, 1.0
J4_RAISED_FROM = 13.9                  # stepped probe after the 0.5 mm inward move
SKIP = ("YAW_JUNCTION",)


def seg(p0, p1, thick, height_axis, height):
    """Oriented box from p0 to p1 (3D), thickness across, extent along height_axis."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    length = float(np.linalg.norm(d))
    t = d / length
    h = np.array(height_axis, float)
    # Local X along the run, Y across the thickness, Z along the height axis.
    plane = Plane(origin=tuple((p0 + p1) / 2), x_dir=tuple(t), z_dir=tuple(h))
    return Box(length, thick, height).moved(plane.location)


def arc_xy(centre, r, a0, a1, z0, z1, thick, n=8):
    """On-edge curl about Z: polyline of boxes, vertical extent z0..z1."""
    out = []
    for k in range(n):
        u0 = math.radians(a0 + (a1 - a0) * k / n)
        u1 = math.radians(a0 + (a1 - a0) * (k + 1) / n)
        p0 = (centre[0] + r * math.cos(u0), centre[1] + r * math.sin(u0), (z0 + z1) / 2)
        p1 = (centre[0] + r * math.cos(u1), centre[1] + r * math.sin(u1), (z0 + z1) / 2)
        out.append(seg(p0, p1, thick, (0, 0, 1), z1 - z0))
    return out


def arc_xz(centre, r, a0, a1, y0, y1, thick, n=8):
    """Curl about Y in the XZ plane: polyline of boxes, width y0..y1."""
    out = []
    for k in range(n):
        u0 = math.radians(a0 + (a1 - a0) * k / n)
        u1 = math.radians(a0 + (a1 - a0) * (k + 1) / n)
        p0 = (centre[0] + r * math.cos(u0), (y0 + y1) / 2, centre[1] + r * math.sin(u0))
        p1 = (centre[0] + r * math.cos(u1), (y0 + y1) / 2, centre[1] + r * math.sin(u1))
        out.append(seg(p0, p1, thick, (0, 1, 0), y1 - y0))
    return out


def blk(x0, x1, y0, y1, z0, z1):
    return C.blk((x0, x1, y0, y1, z0, z1))


# --- frame calculation: conductor 1 -> 22 direction (w) along the cable ---

def reflect(v, c):
    c = c / np.linalg.norm(c)
    return 2 * np.dot(v, c) * c - v


def rot(axis, deg, v):
    a = np.array(axis, float) / np.linalg.norm(axis)
    th = math.radians(deg)
    return (v * math.cos(th) + np.cross(a, v) * math.sin(th) + a * np.dot(a, v) * (1 - math.cos(th)))


def pcb08_w(w0):
    """w at the PCB-08 mouths for a cassette w0 (both cables share the path)."""
    t = np.array([math.cos(math.radians(EXIT_DEG)), math.sin(math.radians(EXIT_DEG)), 0.0])
    w = np.array(w0, float)
    t, w = rot((0, 0, 1), -30, t), rot((0, 0, 1), -30, w)          # on-edge curl
    t_new = np.array([0, 0, -1.0])                                  # crease: -Y -> down
    c = t + t_new
    t, w = reflect(t, c), reflect(w, c)
    t, w = rot((0, 1, 0), 90, t), rot((0, 1, 0), 90, w)             # curl flat, -Z -> -X
    return t, w


def pcb14_w(w0):
    """w at PCB-14's lower ZIF: drum slit at 0 deg (travel -X), one 45 deg fold up (D-052)."""
    t, w = np.array([-1.0, 0, 0]), np.array(w0, float)
    c = t + np.array([0, 0, 1.0])
    return reflect(t, c), reflect(w, c)


def main():
    _entry, _tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_ffc_fold")

    # Geometry of the band centreline.
    u = np.array([math.cos(math.radians(EXIT_DEG)), math.sin(math.radians(EXIT_DEG))])
    p_win = np.array([AXIS_X, 0.0]) + WALL_R * u
    p_out = p_win + 1.0 * u
    right = np.array([u[1], -u[0]])                                 # clockwise side of the heading
    centre = p_out + R_EDGE * right
    a_start = math.degrees(math.atan2(*(p_out - centre)[::-1]))
    x_run = centre[0] + R_EDGE                                      # after 30 deg clockwise: heading -Y
    y_run0 = centre[1]
    x_down = x_run + BAND_T                                         # folded part on the +X side
    z_c = Z_OUTER + R_DOWN + LAYER / 2                              # outer layer radius R_DOWN + LAYER/2
    x_c = x_down - R_DOWN
    zm = (Z_LO + Z_HI) / 2

    solids = {
        "window_exit": [seg((*p_win, zm), (*p_out, zm), BAND_T, (0, 0, 1), Z_HI - Z_LO)],
        "on_edge_curl": arc_xy(centre, R_EDGE, a_start, a_start - 30, Z_LO, Z_HI, BAND_T),
        "minus_y_run": [blk(x_run - BAND_T / 2, x_run + BAND_T / 2, W_Y[0], y_run0, Z_LO, Z_HI)],
        "crease_and_descent": [blk(x_down - BAND_T / 2, x_down + BAND_T / 2, *W_Y, z_c, Z_HI)],
        "curl_to_flat": arc_xz((x_c, z_c), R_DOWN, 0, -90, *W_Y, BAND_T),
        "outer_flat_to_J3": [blk(J3_MOUTH + J3_STIFF, x_c, *W_Y, Z_OUTER - FFC_T / 2, Z_OUTER + FFC_T / 2)],
        "inner_raised_to_J4": [blk(J4_RAISED_FROM, x_c, *W_Y, Z_INNER - FFC_T / 2, Z_INNER + FFC_T / 2)],
    }
    csi = C.find(leaves, "HARNESS_CSI_FFC_DROP_TO_PI_CAM")
    for name, parts in solids.items():
        hits = [h for p in parts for h in C.clashes(p, leaves, skip=SKIP)]
        csi_v = sum(C.common(p, csi.shape) for p in parts)
        gap = min((C.min_gap(p, leaves, skip=SKIP + ("C0_RASPBERRY_PI5_EXACT_STEP",))) for p in parts)
        r.check(f"{name}_clear", not hits and csi_v < 1e-4, clashes=hits, csi_overlap_mm3=round(csi_v, 4),
                nearest_non_pi=gap[1], min_gap=round(gap[0], 3))

    # The droid CAD carries the path as reserves (makad-v1.step.py, replacing the
    # old HARNESS_YAW_FFC_TO_PCB08 box); every modelled solid past the window
    # must sit inside them.
    old_box = [lf.label for lf in leaves if lf.label == "HARNESS_YAW_FFC_TO_PCB08"]
    reserves = [C.find(leaves, "HARNESS_YAW_FFC_FOLD_" + k).box for k in ("RUN", "DESCENT", "CURL", "FLAT")]
    outside = []
    for name in ("minus_y_run", "crease_and_descent", "curl_to_flat", "outer_flat_to_J3", "inner_raised_to_J4"):
        for k, part in enumerate(solids[name]):
            b = C._box(part)
            if not any(all(b[i] >= rb[i] - 0.1 for i in range(3)) and all(b[i] <= rb[i] + 0.1 for i in range(3, 6))
                       for rb in reserves):
                outside.append((name, k, [round(v, 2) for v in b]))
    r.check("droid_reserves_carry_the_path", not old_box and not outside,
            old_reserve_left=old_box, solids_outside=outside, reserves=reserves)

    r.check("geometry", R_DOWN - LAYER / 2 >= 3.0 and R_EDGE - BAND_T / 2 >= 3.0 and x_c > J3_MOUTH + J3_STIFF,
            window_centre=[round(v, 3) for v in p_win], run_x=round(x_run, 3), descent_x=round(x_down, 3),
            curl_centre_xz=[round(x_c, 3), round(z_c, 3)], inner_curl_radius=round(R_DOWN - LAYER / 2, 3),
            flat_from_x=round(x_c, 3), note="outer layer -> J3 at Z 114.1, inner -> J4 raised run at Z 115.05")

    # Conductor 1 -> 22 at the mouths must point -Y (contact 1 at Y -28.25).
    need = np.array([0, np.sign(PAD22_Y - PAD1_Y), 0.0])
    results = {}
    for label, w0 in (("conductor 1 at the BOTTOM edge in the cassette", (0, 0, 1)),
                      ("conductor 1 at the TOP edge in the cassette", (0, 0, -1))):
        t, w = pcb08_w(w0)
        t14, w14 = pcb14_w(w0)
        results[label] = dict(pcb08_travel=np.round(t, 3).tolist(), pcb08_w=np.round(w, 3).tolist(),
                              pcb08_straight=bool(np.allclose(w, need)),
                              pcb14_travel=np.round(t14, 3).tolist(), pcb14_w=np.round(w14, 3).tolist())
    top = results["conductor 1 at the TOP edge in the cassette"]
    r.check("mirroring_resolved", top["pcb08_straight"]
            and not results["conductor 1 at the BOTTOM edge in the cassette"]["pcb08_straight"]
            and np.allclose(top["pcb08_travel"], [-1, 0, 0]),
            cases=results,
            rule="FFC conductor 1 at the TOP edge in the cassette -> PCB-08 contact n meets conductor n; "
                 "at PCB-14's lower ZIF (yaw 0) conductor 1 is then at the -X end (w points +X)")
    r.finish()


if __name__ == "__main__":
    main()
