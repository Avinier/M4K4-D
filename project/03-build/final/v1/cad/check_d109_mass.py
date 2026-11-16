"""D-109 Level 6: routed body-harness mass replaces part of the body allowance; tipping bound.

The body register carries HARNESS_AND_FASTENERS 95 g at (20, 0, 88) for unmodelled
harness, connector tails, clips, panel screws and remaining fasteners. D-109 routes
the body wires (body-harness-lengths.json) and places connector/splice envelopes, so
that share of the allowance moves to its routed centroids. The rest stays as the
fastener/clip allowance. Tipping is screened against check_d107_mass's steel result
with a conservative stationary bound: a_tip ~ g*d/h, d = a*h/g, and
da/a <= |dxy|/d + dh/h (the worst direction taken). Masses are E.
"""

import json
import math
from pathlib import Path

import module_checks as C

HERE = Path(__file__).resolve().parent
ALLOWANCE = (95.0, (20.0, 0.0, 88.0))
# D-109 connector/splice parts not counted elsewhere (E). The hub v2 board is in check_d095_mass.
PARTS = {
    "D109_CHARGE_SPLICE_NEG_AWG16_ENVELOPE": 1.5, "D109_SHARED_5V_POS_SPLICE_ENVELOPE": 1.2,
    "D109_SHARED_5V_NEG_SPLICE_ENVELOPE": 1.2, "D109_W11_SS34_POTTED_JOINT_ENVELOPE": 0.8,
    "D109_J6_REAR_BREAK_MICROFIT3_1X6_MATED_ENVELOPE": 1.6,
    "D109_W27_FOUR_2X3_MIC_HEADERS_MATED_ENVELOPE": 2.4,
    "D109_W28_SPEAKER_INLINE_BREAK_ENVELOPE": 0.4,
}
TIES_G = 3.0                                   # ~15 x 2.5 mm ties and sleeve, at the wire centroid (E)
G = 9.81


def main():
    r = C.Report("check_d109_mass")
    lengths = json.loads((HERE / "body-harness-lengths.json").read_text())
    rows = [(w["label"], w["mass_g_E"], tuple(w["centroid"])) for w in lengths["wires"]]
    wire_g = sum(m for _, m, _ in rows)
    wc = tuple(sum(m * c[i] for _, m, c in rows) / wire_g for i in range(3))
    rows.append(("ties and sleeve", TIES_G, wc))
    import d109_body_parts as P
    entry = C.load_entry()
    for s in P.parts(entry._tag):
        b = C._box(s)
        rows.append((s.label, PARTS.get(s.label, 0.0), ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)))
    routed = sum(m for _, m, _ in rows)
    am, ac = ALLOWANCE
    left = am - routed
    r.check("routed body harness within the 95 g allowance", left >= 0, routed_g=round(routed, 1),
            allowance_left_for_fasteners_g=round(left, 1))
    # CoM shift of the whole robot when `routed` grams move from the allowance centroid to their own.
    base = json.loads((HERE / "check_d107_mass-report.json").read_text())
    steel = next(x for x in base["rows"] if x["check"] == "mass_and_tipping")["steel"]
    M, com, a = steel["mass_g"], steel["com_mm"], steel["worst_yaw_a_tip"]
    moment = [sum(m * (c[i] - ac[i]) for _, m, c in rows) for i in range(3)]
    d_com = [v / M for v in moment]
    h = com[2]
    d = a * h / G
    bound = math.hypot(d_com[0], d_com[1]) / d + max(d_com[2], 0.0) / h
    a_low = a * (1 - bound)
    margin = 100 * (a_low / 1.5823 - 1)
    # Informational: the decision uses the full sweep, MAKAD_D109_MASS=1 check_d107_mass.py
    # -> check_d107_mass_d109-report.json (steel 2.15 %, copper 3.72 % on 2026-11-15).
    r.check("tipping bound with routed body harness (informational)", True, d_com_mm=[round(v, 3) for v in d_com],
            d_equiv_mm=round(d, 2), a_tip_worst_bound=round(a_low, 4), margin_pct_bound=round(margin, 3),
            baseline_margin_pct=steel["margin_pct"],
            note="stationary bound, worst direction; not a re-run of the 1068120-pose sweep")
    r.check("mass rows", True, rows=[(n, round(m, 2), [round(v, 1) for v in c]) for n, m, c in rows])
    r.finish()


if __name__ == "__main__":
    main()
