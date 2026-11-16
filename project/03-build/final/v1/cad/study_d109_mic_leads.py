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
        "REAR_L": (-12.0, 1, 115.0, None, None),      # over the fan collar (Z 126) to X 33, then down to Z 106
        "REAR_R": (-12.0, -1, 115.0, 99.5, 106.0)}    # under the front bosses (Z 108.4), over FRONT_R
INBOARD = 69.6          # |Y| of the exit run down the board's inboard face (board 71.3)
DX = 5.5                # exit run offset along +X, clear of the board's M2 screws/washers on x0
RISE_Y = 70.9           # |Y| of an upward exit past the upper rail (|Y| 68, skin 72.8 at Z 126)


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
            # rise outboard of the rail, then step inboard only once above the rail top (Z 133.6)
            # Crossing the upper rail is impossible here (its top corner and the skin shoulder
            # overlap in Z). Stay outboard of it: rise to Z 126 (skin 72.8, rail |Y| 68), run over
            # the fan collar (top Z 124, fan frame |Y| 68.9) to X 33, drop past the fan to Z 106.
            pts = [(x0, sgn * 70.8, ztop), (x0 + DX, sgn * RISE_Y, ztop + 1.0), (x0 + DX, sgn * RISE_Y, 126.6)]
        else:
            pts = [(x0, sgn * 70.8, ztop), (x0 + DX, sgn * INBOARD, ztop), (x0 + DX, sgn * INBOARD, zb)]
        stations = [x0 + DX + i * 2.0 for i in range(3 if zb is None else 2, int((X_FRONT - x0 - DX) / 2.0) + 1)] + [X_FRONT]
        worst = 99.0
        for x in stations:
            if zb is None:
                zr = 126.6 if x <= 33.0 else 106.0   # over the fan frame top (Z 125)
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
        out[name] = dict(points=[[round(v, 2) for v in p] for p in pts],
                         clips=[[round(v, 2) for v in p] for p in pts[4:-1:6] if not (zb is None and 1.0 < p[0] < 34.0)],  # none over the fan frame
                         notch=[[round(v, 2) for v in p] for p in pts[:5]],
                         skin_exit=[round(v, 2) for v in pts[-1]], min_frame_clearance=round(worst, 2))
        print(name, len(pts), "points; exit", out[name]["skin_exit"], "min clearance", round(worst, 2))
    (HERE / "d109-mic-leads.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
