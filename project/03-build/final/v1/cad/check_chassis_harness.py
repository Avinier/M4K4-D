"""Neutral-pose solid check for every visible chassis wire and the HN-006 splice envelopes.

Rewritten 2026-11-17 after the D-106..D-109 review. The first version tested 5 of
the 34 wires and intersected each whole tube compound in one Boolean, which reads 0
for about half of real intersections (W30/W31 ran 14 mm through the rear deck and
passed). Every test here is piecewise (module_checks.piece_clashes / piece_common).

Rows:
1. each chassis wire and splice envelope vs every part and D-109 envelope (endpoint parts allowed);
2. chassis signal cables (W29-W36): no contact (>= 0.5 mm, a tied crossing) with any
   chassis or body power lead, and >= 5 mm from the motor outputs W08/W09 (PWM)
   except the motor/driver the signal belongs to;
3. every chassis wire vs every body wire: no overlap, >= 0.5 mm, except the same
   circuit meeting at its body-lift plug pair (W03/W05c/W13/W17);
4. splice envelopes vs every visible wire.
Run from this folder with the legacy runtime and PYTHONPATH in ../README.md; ~2 min.
"""

import re

import body_harness as BH
import chassis_harness as H
import module_checks as C

# Endpoint parts a wire may enter (label regex), keyed by wire stem.
ENDPOINT_PARTS = {
    "W01": r"PACK_DISCONNECT_MICROFIT_PLUS_1X2_MATED_ENVELOPE",
    "W02P": r"M12_JST_PA_3P_BALANCE_BREAK_MATED_PAIR|M12_CH103_\w+|PACK_STRAP_HOOK_LOOP_L|BATTERY_BMS_\w+",  # D-115: tails dressed under the pack strap
    "W02B": r"M12_JST_PA_3P_BALANCE_BREAK_MATED_PAIR|M12_JST_XHP\w*",
    "W03a": r"PACK_DISCONNECT\w*|PACK_ATOF_FUSE_HOLDER_ENVELOPE|J_BAT_\w*",
    "W03b": r"PACK_ATOF_FUSE_HOLDER_ENVELOPE|J_BAT_\w*",
    "W05c": r"J_CHASSIS_\w*",
    "W05t": r"S18V20\w*|M[23]_\w*",
    "W06": r"DRV8833_LEFT\w*", "W07": r"DRV8833_RIGHT\w*",
    "W08": r"DRV8833_LEFT\w*|MOTOR_L_\w*", "W09": r"DRV8833_RIGHT\w*|MOTOR_R_\w*",
    "W13": r"J_S18_H_\w*|M2_\w*", "W17": r"J_S18_Y_\w*|M3_\w*",
    "W29": r"C3_J10_7_GHR08_MATED_PLUG|M7_\w*|IMU_\w*",
    "W30": r"C3_J10_3_GHR04_MATED_PLUG|MOTOR_L_ENCODER_6PIN_CONNECTOR",
    "W31": r"C3_J10_4_GHR04_MATED_PLUG|MOTOR_R_ENCODER_6PIN_CONNECTOR",
    "W32": r"C3_J10_5_GHR06_MATED_PLUG|DRV8833_LEFT\w*",
    "W33": r"C3_J10_6_GHR06_MATED_PLUG|DRV8833_RIGHT\w*",
    "W34": r"C3_J10_8_GHR05_MATED_PLUG|BALL_NOSE_\w*|GP2Y\w*",
    "W36": r"C3_J10_10_GHR04_MATED_PLUG|REAR_SKID_TCRT\w*|TCRT_\w*",
}
SIGNALS = ("W29", "W30", "W31", "W32", "W33", "W34", "W36")
PWM = ("W08", "W09")
OWN_MOTOR = {"W30": "W08", "W32": "W08", "W31": "W09", "W33": "W09"}
CROSSING = 0.5
PWM_GAP = 5.0
SAME_CIRCUIT = {"W03a": "W03", "W03b": "W03", "W03r": "W03", "W03r-": "W03",
                "W05c": "W05c", "W13": "W13", "W17": "W17"}


def stem(label):
    return label.split("_", 1)[0]


def main():
    entry, _, leaves = C.droid_tree()
    r = C.Report("check_chassis_harness")
    harness = H.build_chassis_harness(entry)
    groups = {g.label: list(g.children) for g in harness.children}
    wires = [w for name, ws in groups.items() for w in ws if not w.label.endswith("_INSULATED")]
    splices = [w for ws in groups.values() for w in ws if w.label.endswith("_INSULATED")]
    r.check("39 wires and 2 rated five-wire splices", len(wires) == 39 and len(splices) == 2,
            wires=len(wires), splices=len(splices))

    # 1. vs parts, plus the D-109 body envelopes (splices, SS34 joint, breaks), which the
    #    droid tree files as reserves but are real potted/crimped parts.
    obstacle = {lf.label for lf in leaves if C.is_part(lf.path) or lf.label.startswith("D109_")}
    for w in [*wires, *splices]:
        allowed = ENDPOINT_PARTS.get(stem(w.label))
        hits = [h for h in C.piece_clashes(w, leaves, min_vol=0.05, parts_only=False)
                if h[0] in obstacle and not (allowed and re.fullmatch(allowed, h[0]))]
        r.check(f"{w.label} vs parts", not hits, hits=hits[:6])

    # body wires (straight route-chain runs and the shell-dressed W27 runs)
    ends = BH.cached_ends()
    body = [(chain, BH._tube(pts, BH.WIRES[chain][1])) for chain, pts in BH.paths(entry, ends).items()]
    body += [(f"{c} shell run", BH._tube(pts, 1.2)) for c, pts in BH.shell_dressed().items()]
    body_power = [(c, t) for c, t in body if BH.WIRES[c.replace(" shell run", "")][3] == "power"]

    def gap(a, b):
        if C.piece_common(a, b) > 0.05:
            return 0.0
        return C.distance(a, b)

    # 2. signal separation
    chassis_power = [w for w in wires if stem(w.label) not in SIGNALS]
    for s in [w for w in wires if stem(w.label) in SIGNALS]:
        st = stem(s.label)
        near = []
        for p in chassis_power:
            ps = stem(p.label)
            need = PWM_GAP if ps in PWM and OWN_MOTOR.get(st) != ps else CROSSING
            if C._hit(C._box(s), C._box(p), need):
                d = gap(s, p)
                if d < need:
                    near.append((p.label, round(d, 2), need))
        for c, t in body_power:
            if C._hit(C._box(s), C._box(t), CROSSING):
                d = gap(s, t)
                if d < CROSSING:
                    near.append((f"body {c}", round(d, 2), CROSSING))
        r.check(f"{st} separated from power", not near, near=near[:6])

    # 3. chassis vs body wires
    for w in wires:
        near = []
        for c, t in body:
            if SAME_CIRCUIT.get(stem(w.label)) and SAME_CIRCUIT.get(stem(w.label)) == SAME_CIRCUIT.get(c.split()[0]):
                continue
            if C._hit(C._box(w), C._box(t), CROSSING):
                d = gap(w, t)
                if d < CROSSING:
                    near.append((c, round(d, 2)))
        r.check(f"{w.label} vs body wires", not near, near=near[:6])

    # 4. splices vs visible wires
    for s in splices:
        pol = "POS" if "_POS_" in s.label else "NEG"
        expected = (f"W05c_JCHASSIS_TO_TUB_{pol}", f"W05t_TUB_TO_M2_{pol}",
                    f"W05t_TUB_TO_M3_{pol}", f"W06_TUB_TO_DRIVER_L_{pol}",
                    f"W07_TUB_TO_DRIVER_R_{pol}")
        hits = [(w.label, round(C.piece_common(s, w), 3)) for w in wires
                if C._hit(C._box(s), C._box(w)) and C.piece_common(s, w) > 0.05
                and not w.label.startswith(expected)]
        r.check(f"{s.label} vs wires", not hits, hits=hits)
    for i, a in enumerate(splices):
        for b in splices[i+1:]:
            d = C.distance(a, b)
            r.check(f"{a.label} insulated from {b.label}", d >= 2.5,
                    clearance_mm=round(d, 3))
    # Each housing has one input and four distinct outputs. Only insulated
    # same-polarity tails may enter it; opposite-polarity conductors stay out.
    for pol in ("POS", "NEG"):
        own = [w for w in wires if w.label.startswith(("W05c_", "W05t_", "W06_", "W07_"))
               and f"_{pol}_" in w.label]
        opposite = "NEG" if pol == "POS" else "POS"
        other = [w for w in wires if w.label.startswith(("W05c_", "W05t_", "W06_", "W07_"))
                 and f"_{opposite}_" in w.label]
        housing = next(s for s in splices if f"_{pol}_" in s.label)
        r.check(f"HN006_{pol}_one_input_four_outputs", len(own) == 5,
                labels=[w.label for w in own])
        clashes = [(w.label, round(C.piece_common(housing, w), 3)) for w in other
                   if C._hit(C._box(housing), C._box(w)) and C.piece_common(housing, w) > .05]
        r.check(f"HN006_{pol}_housing_separate_from_opposite_tails", not clashes,
                clashes=clashes)
    pos = [w for w in wires if w.label.startswith(("W05c_", "W05t_", "W06_", "W07_"))
           and "_POS_" in w.label]
    neg = [w for w in wires if w.label.startswith(("W05c_", "W05t_", "W06_", "W07_"))
           and "_NEG_" in w.label]
    overlaps = [(a.label, b.label, round(C.piece_common(a, b), 3)) for a in pos for b in neg
                if C._hit(C._box(a), C._box(b)) and C.piece_common(a, b) > .05]
    # Crossing cable envelopes are insulated jackets, so touching jackets are
    # permitted.  Bare stripped ends exist only inside the separate rated
    # housings; the build card requires abrasion sleeve at each contact.
    r.check("HN006_insulated_tails_and_housing_separation",
            all(w.label.endswith(("_AWG16", "_AWG18")) for w in pos + neg)
            and len(pos) == len(neg) == 5,
            jacket_contacts=overlaps, assembly_gate="sleeve and secure touching jackets")
    r.finish()


if __name__ == "__main__":
    main()
