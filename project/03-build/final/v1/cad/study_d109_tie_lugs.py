"""D-109 B-05: find fused tie-lug positions on body prints beside the main route boxes.

For each listed route box, candidate 4 x 4 x 3 mm lugs (2.5 mm tie, CH-082) are placed
just outside each lateral face at several stations along the box. A lug is accepted when
it is embedded 0.3-2 mm into a body print (so it fuses), clears every other part and
module, and leaves the route box itself untouched. Writes d109-tie-lugs.json, read by
makad-v1.step.py. Lug geometry is E; printability is checked with the frame print.
"""

import json
from pathlib import Path

import module_checks as C
import d109_routes as R

HERE = Path(__file__).resolve().parent
PRINTS = ("BODY_FRAME_MAIN_PRINT", "REAR_BAY_MODULE_PLATE")   # not the tray: it slides out
WANT = ["T1_JBAT_AFT", "T1_M1_M6_FRONT", "T1_TO_STARS", "T2_W11_FWD", "T3_RISER",   # not T3_TO_PCB08_J6: a lug there blocks the J8-1 pull and PCB-08 removal (check_d107_body)
       
        "T4_W24_MINUS_Y", "T4_W25_CHANNEL", "T4_J6_AFT", "T5_RL_AFT", "T5_W12_PY_FWD", "T5_FL"]
LUG = (4.0, 4.0, 3.0)


def candidates(b):
    x0, x1, y0, y1, z0, z1 = b
    L = max(x1 - x0, y1 - y0, z1 - z0)
    axis = [x1 - x0, y1 - y0, z1 - z0].index(L)
    for t in (0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9):
        c = [x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t]
        for side in range(3):
            if side == axis:
                continue
            for sgn in (-1, 1):
                lo = [c[i] - LUG[i] / 2 for i in range(3)]
                hi = [c[i] + LUG[i] / 2 for i in range(3)]
                face = b[2 * side + (1 if sgn > 0 else 0)]
                lo[side], hi[side] = (face, face + LUG[side]) if sgn > 0 else (face - LUG[side], face)
                tunnel = 3 - axis - side    # tie passes along the third axis
                yield (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]), tunnel


def main():
    _, _, leaves = C.droid_tree()
    prints = [lf for lf in leaves if lf.label in PRINTS]
    others = [lf for lf in leaves if lf.label not in PRINTS and not lf.label.startswith(("HARNESS_", "M12_BALANCE_"))]
    found = {}
    for name in WANT:
        for lug, tunnel in candidates(R.ROUTES[name]):
            s = C.blk(lug)
            emb = sum(C.common(s, p.solid) for p in prints if C._hit(C._box(s), p.box))
            if not (0.3 * 16 <= emb <= 0.75 * 48):
                continue
            if C.clashes(s, others, min_vol=0.01, parts_only=False):
                continue
            if any(n != name and all(max(lug[2*i], R.ROUTES[n][2*i]) < min(lug[2*i+1], R.ROUTES[n][2*i+1]) for i in range(3))
                   for n in R.ROUTES):
                continue
            found[name] = dict(lug=[round(v, 2) for v in lug], tunnel_axis="XYZ"[tunnel], embedded_mm3=round(emb, 2))
            break
        print(name, found.get(name, "none"))
    (HERE / "d109-tie-lugs.json").write_text(json.dumps(found, indent=1) + "\n")


if __name__ == "__main__":
    main()
