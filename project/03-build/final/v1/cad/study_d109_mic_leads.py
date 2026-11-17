"""D-109 F2 fix: shell-dressed W27 mic leads.

Each mic lead is clipped to the shell's inner skin and rides with the shell. It
leaves the mic pigtail down the board's inboard face (a notch in the boss), out under the board to its run height (front 103, -Y rear 106; the +Y rear lead rises outboard of the upper rail and runs over the fan at 135), runs forward along the skin
(|Y| = skin - GAP - r) to the open front (X_FRONT, no frame there), where a free
tail leaves the skin. The tail is the only part that moves relative to the shell: it
passes over the hub bracket and drops to the hub v2 headers (d109_routes T5_TAIL_*).

Skin positions come from rays against BODY_SHELL at each station. Writes
d109-mic-leads.json: per mic, the shell-dressed polyline and clip positions.
"""

import json
from pathlib import Path

import module_checks as C

HERE = Path(__file__).resolve().parent

X_FRONT = 77.5          # skin exit, in the open front (no frame at X 74-81)
R = 1.2                 # six-core AWG28 outer envelope (E)
GAP = 0.7
Z_TOP = 140.0           # the shell lifts vertically: frame above the lead matters too
# pigtail x, side, pigtail top Z, Z below the board (exit down its inboard face in a boss notch), run Z
MICS = {"FRONT_L": (44.0, 1, 125.0, 109.5, 103.0), "FRONT_R": (44.0, -1, 125.0, 109.5, 103.0),
        "REAR_L": (-12.0, 1, 115.0, None, None),      # over the fan collar (Z 127.8) to X 36.5, then down to Z 106
        "REAR_R": (-12.0, -1, 115.0, 99.5, 106.0)}    # under the front bosses (Z 108.4), over FRONT_R
INBOARD = 69.6          # |Y| of the exit run down the board's inboard face (board 71.3)
DX = 5.5                # exit run offset along +X, clear of the board's M2 screws/washers on x0
RISE_Y = 69.8           # |Y| of the REAR_L rise and over-collar run (2026-11-17, was 70.9)
# REAR_L over the fan (2026-11-17 review fix). The +Y skin between X 1 and 34 carries the
# fan grille and its collar ring (R 16.5 about X 17.5, Z 110, inboard edge |Y| 70.5); below
# Z 93 is the wheel-arch pod; above Z 126 the upper side rail stands at |Y| 68. The only
# shell-carried path is over the ring top (Z 126.5) between the rail and the skin (|Y| ~71.9
# at Z 127.8), where the collar's 45 deg print peak stood to |Y| 70.5 at X 10-24. The old run
# sat at |Y| 68.6 there (0.6 mm into the rail) and dropped diagonally through the skin.
# Now: lead centre Z 127.8 (bottom 126.6, over the ring), |Y| 69.8 (0.6 mm to the rail,
# ~0.85 mm to the skin), with the print peak cut back to |Y| 71.6 over X 9-26, Z 126.55-129.1
# (COLLAR_PEAK_NOTCH, a droid cut on BODY_SHELL; the ring itself is not cut). The lead then
# descends at X 36.5 (outside the ring) following the skin, and runs forward at Z 106.
Z_OVER = 127.8
X_DROP = 36.5
COLLAR_PEAK_NOTCH = (9.0, 26.0, 69.0, 71.6, 126.55, 129.1)   # x0, x1, |y|0, |y|1, z0, z1


def skin_y(shell, x, z, sgn):
    hits = [t for t in C.ray(shell, (x, 0.0, z), (0, sgn, 0)) if t[1] > 0]
    return hits[0][0] if hits else None


def frame_y(fixed, x, z, sgn):
    best = 0.0
    for lf in fixed:
        b = lf.box
        if b[0] - 0.1 <= x <= b[3] + 0.1 and b[2] - 0.1 <= z <= b[5] + 0.1 and (b[4] > 0 if sgn > 0 else b[1] < 0):
            for t0, t1 in C.ray(lf.solid, (x, 0.0, z), (0, sgn, 0)):
                if t1 > 0:
                    best = max(best, t1)
    return best


def band(shell, fixed, x, z, sgn):
    """(lead |Y|, clearance) at station x, height z: skin over z +- (R+0.3), frame over z-R-0.3 .. Z_TOP."""
    zs = [z - R - 0.3, z, z + R + 0.3]
    sk = [skin_y(shell, x, zz, sgn) for zz in zs]
    if None in sk:
        return None, -1
    fr = max(frame_y(fixed, x, zz, sgn) for zz in [z - R - 0.3 + k for k in range(0, int(Z_TOP - z) + 2, 1)])
    y = min(sk) - GAP - R
    return y, (y - R) - fr


def main():
    _, _, leaves = C.droid_tree()
    shell = C.find(leaves, "BODY_SHELL").shape
    fixed = [lf for lf in leaves if not lf.label.startswith(("BODY_SHELL", "M9_", "HARNESS_", "D109_"))
             and not any(k in lf.label for k in ("RESERVE", "KEEP_OUT", "ENVELOPE"))]
    out = {}
    for name, (x0, sgn, ztop, zb, zr) in MICS.items():
        if zb is None:
            # REAR_L: rise beside the mic, run over the fan collar ring, descend at X_DROP, run forward.
            pts = [(x0, sgn * 70.8, ztop), (x0 + DX, sgn * RISE_Y, ztop + 1.0), (x0 + DX, sgn * RISE_Y, Z_OVER)]
            pts += [(x, sgn * RISE_Y, Z_OVER) for x in [x0 + DX + 4.0 + 4.0 * i for i in range(int((X_DROP - x0 - DX - 4.0) / 4.0) + 1)]
                    if x < X_DROP] + [(X_DROP, sgn * RISE_Y, Z_OVER)]
            worst = min(skin_y(shell, x, z, sgn) - RISE_Y - R for x, _, z in pts[2:] for z in (Z_OVER,)
                        if not (COLLAR_PEAK_NOTCH[0] <= x <= COLLAR_PEAK_NOTCH[1]))
            worst = min(worst, RISE_Y - R - max(frame_y(fixed, x, zz, sgn) for x, _, _ in pts[2:]
                                                 for zz in [Z_OVER - R - 0.3 + k for k in range(int(Z_TOP - Z_OVER) + 2)]))
            for z in [Z_OVER - 2.0 * k for k in range(1, int((Z_OVER - 106.0) / 2.0) + 1)] + [106.0]:
                y, c = band(shell, fixed, X_DROP, z, sgn)
                pts.append((X_DROP, sgn * y, z))
                worst = min(worst, c)
            stations = [X_DROP + 2.0 * i for i in range(1, int((X_FRONT - X_DROP) / 2.0) + 1)] + [X_FRONT]
            zr = 106.0
        else:
            pts = [(x0, sgn * 70.8, ztop), (x0 + DX, sgn * INBOARD, ztop), (x0 + DX, sgn * INBOARD, zb)]
            stations = [x0 + DX + i * 2.0 for i in range(2, int((X_FRONT - x0 - DX) / 2.0) + 1)] + [X_FRONT]
            worst = 99.0
        for x in stations:
            best = None
            for dz in (0, 0.5, -0.5, 1, -1, 1.5, -1.5, 2, -2, 3, -3):
                y, c = band(shell, fixed, x, zr + dz, sgn)
                if y is not None and c >= GAP:
                    best = (sgn * y, zr + dz, c)
                    break
            if best is None:
                y, c = band(shell, fixed, x, zr, sgn)
                best = (sgn * (y or 70.0), zr, c)
            worst = min(worst, best[2])
            pts.append((x, best[0], best[1]))
        notch = [(x0, sgn * 70.8, ztop), (x0 + DX, sgn * RISE_Y, ztop + 1.0), (x0 + DX, sgn * RISE_Y, Z_OVER)] if zb is None else pts[:5]
        run = pts[2:-1]
        clips = [p for p in run[::3] if not (zb is None and COLLAR_PEAK_NOTCH[0] - 1 <= p[0] <= COLLAR_PEAK_NOTCH[1] + 1)
                 and not (zb is None and p[0] == X_DROP and p[2] < Z_OVER and p[2] > 106.0)] if zb is None else pts[4:-1:6]
        out[name] = dict(points=[[round(v, 2) for v in p] for p in pts],
                         clips=[[round(v, 2) for v in p] for p in clips],
                         notch=[[round(v, 2) for v in p] for p in notch],
                         skin_exit=[round(v, 2) for v in pts[-1]], min_frame_clearance=round(worst, 2),
                         shell_cuts=[[COLLAR_PEAK_NOTCH[0], COLLAR_PEAK_NOTCH[1], *sorted((sgn * COLLAR_PEAK_NOTCH[2], sgn * COLLAR_PEAK_NOTCH[3])),
                                      COLLAR_PEAK_NOTCH[4], COLLAR_PEAK_NOTCH[5]]] if zb is None else [])
        print(name, len(pts), "points; exit", out[name]["skin_exit"], "min clearance", round(worst, 2))
    (HERE / "d109-mic-leads.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
