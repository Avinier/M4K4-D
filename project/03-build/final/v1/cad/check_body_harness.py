"""D-109 Level 5: visible body wires at neutral.

Rows: each wire vs the assembly (endpoint parts allowed); B-09 segregation of
signal/audio vs power (>= 5 mm surface gap, E) except wires that share a route
box by design; bend sanity (no turn sharper than 120 deg between segments);
then writes body-harness-lengths.json.
"""

import math
import re

import module_checks as C
import body_harness as H
import d109_routes as R
from body_harness_endpoints import ENDPOINTS, resolve

SEGREGATION = 5.0
# B-09 named crossings: logic wires that pass power by design (not audio/RS-422).
NAMED_CROSSINGS = {("W40 M1", "W05 stars")}   # M1 control tail beside the M6-to-star lead at the M1 face
IGNORE = ("HARNESS_", "M12_BALANCE_", "YAW_JUNCTION_", "C0_LINK_ADAPTER_TOP_ENTRY_PLUG_RESERVE",
          "C0_LINK_ADAPTER_J91_PLUG_RESERVE", "C3_CARRIER_TOP_ENTRY_SIGNAL_PLUG_LAYER_RESERVE",
          "CHARGE_SPLICE_AND_LEADS_RESERVE")


# Parts that belong to an endpoint but are not matched by its label regex.
EXTRA_ENDPOINT_PARTS = {
    "PCB08_J6_PADS": r"PCB08_MAIN_06__pcb-08-yaw-junction_PCB",   # W17 is soldered to J6 pads on this board
    "J9_1": r"C0_LINK_ADAPTER_PCB09_RESERVE", "J9_2": r"C0_LINK_ADAPTER_PCB09_RESERVE",
    "J9_3": r"C0_LINK_ADAPTER_PCB09_RESERVE", "J9_4": r"C0_LINK_ADAPTER_PCB09_RESERVE",   # the endpoint board's own reserve
}
# Keep-outs a lead may enter only within TERMINAL_ZONE of that endpoint's mouth, to reach
# terminals that sit inside them; the rest of the wire must stay out.
ENDPOINT_KEEPOUTS = {
    "MUSHROOM": "POWER_BUTTON_MUSHROOM_BEHIND_PANEL_KEEP_OUT",   # NO screw terminals sit inside it
    "SPEAKER": "SPEAKER_ACOUSTIC_CAVITY_KEEP_OUT",               # speaker tabs sit inside it
}
TERMINAL_ZONE = 6.0


def trim(points, length, from_end):
    """The polyline without its first (from_end=False) or last `length` mm."""
    p = [list(q) for q in (reversed(points) if from_end else points)]
    while length > 0 and len(p) > 1:
        d = math.dist(p[0], p[1])
        if d <= length:
            p.pop(0); length -= d
        else:
            p[0] = [p[0][i] + (p[1][i] - p[0][i]) * length / d for i in range(3)]; length = 0
    return list(reversed(p)) if from_end else p


def turn_deg(a, b, c):
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]
    nu, nv = math.dist(a, b), math.dist(b, c)
    if nu < 1e-6 or nv < 1e-6:
        return 0.0
    return math.degrees(math.acos(max(-1, min(1, sum(u[i] * v[i] for i in range(3)) / nu / nv))))


def main():
    entry, _, leaves = C.droid_tree()
    ends = resolve(leaves)
    r = C.Report("check_body_harness")
    paths = H.paths(entry, ends)
    tubes = {}
    for chain, pts in paths.items():
        label, rad, _, cls, _, _ = H.WIRES[chain]
        tubes[chain] = H._tube(pts, rad)
        a, names, z = R.CHAINS[chain]
        allowed = {lf.label for e in (a, z) if e in ENDPOINTS for lf in leaves
                   if re.fullmatch(ENDPOINTS[e][0], lf.label)}
        allowed |= {lf.label for e in (a, z) if e in EXTRA_ENDPOINT_PARTS for lf in leaves
                    if re.fullmatch(EXTRA_ENDPOINT_PARTS[e], lf.label)}
        # piecewise: a Boolean on the whole tube compound misses about half of real hits (2026-11-17)
        hits = [h for h in C.piece_clashes(tubes[chain], leaves, min_vol=0.05, parts_only=False)
                if h[0] not in allowed and not h[0].startswith(IGNORE) and not h[0].startswith("D109_")]
        zone = {}
        for e, from_end in ((a, False), (z, True)):
            if e in ENDPOINT_KEEPOUTS:
                core = H._tube(trim(pts, TERMINAL_ZONE, from_end), rad)
                lab = ENDPOINT_KEEPOUTS[e]
                zone[lab] = round(sum(v for l, v in C.piece_clashes(core, leaves, min_vol=0.05, parts_only=False) if l == lab), 3)
        hits = [h for h in hits if h[0] not in zone or zone[h[0]] > 0.05]
        r.check(f"{chain} vs assembly", not hits, hits=hits[:6],
                keepout_beyond_terminal_zone_mm3=zone or None)
        worst = max((turn_deg(*pts[i:i + 3]) for i in range(len(pts) - 2)), default=0.0)
        r.check(f"{chain} no reversal", worst <= 120.0, worst_turn_deg=round(worst, 1))
    def module(e):
        return e.split("_")[0] if e else None

    def shared(p, q):
        """Same route box, or both end on the same module (e.g. M6 I2C and M6 power)."""
        ep = {module(e) for e in (R.CHAINS[p][0], R.CHAINS[p][2])}
        eq = {module(e) for e in (R.CHAINS[q][0], R.CHAINS[q][2])}
        return bool(set(R.CHAINS[p][1]) & set(R.CHAINS[q][1])) or bool((ep & eq) - {None}) \
            or (p, q) in NAMED_CROSSINGS
    for p in paths:
        if H.WIRES[p][3] == "power":
            continue
        near = []
        for q in paths:
            if H.WIRES[q][3] != "power" or shared(p, q):
                continue
            if C._hit(C._box(tubes[p]), C._box(tubes[q]), SEGREGATION):
                d = 0.0 if C.piece_common(tubes[p], tubes[q]) > 0.05 else C.distance(tubes[p], tubes[q])
                if d < SEGREGATION:
                    near.append((q, round(d, 2)))
        r.check(f"{p} segregated from power", not near, near=near)
    doc = H.write_lengths(entry, ends)
    r.check("lengths written", True, total_conductor_g_E=doc["total_conductor_g_E"], wires=len(doc["wires"]))
    r.finish()


if __name__ == "__main__":
    main()
