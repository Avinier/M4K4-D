"""PCB-09 rev A layout, written headless into the .kicad_pcb (D-092).

Run from this folder with any Python 3 (no KiCad Python needed):

    python3 layout_pcb09.py            # rewrite set-up, placement and routing, then DRC
    python3 layout_pcb09.py --no-drc   # write only

The KiCad Nightly GUI is busy with PCB-02 in a parallel session, so this board
is edited as a file (tools/kfile.py) and checked with the Nightly kicad-cli. The
router is this file: every track, via and pour below is placed by hand, by
coordinate; nothing is autorouted (D-060). Rerunning drops everything this script
wrote before (kfile's generated-UUID namespace) and writes it again.

Board coordinates: KiCad x = world X + 104.7, KiCad y = 139 - world Y.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

BOARD = HERE / "pcb-09-c0-link-adapter.kicad_pcb"
LIB = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")

# ---------------------------------------------------------------- outline (D-074 + D-092 tabs and bay extension)
# Clockwise from the -X tab's top-left corner. The strip's +Y edge is y 116.6, the
# bridge and bay meet at y 116.5, the +X tab's -Y edge is y 121.8 (world Y 17.2).
OUTLINE = [
    (93.7, 116.6), (134.7, 116.6), (134.7, 100.0), (170.7, 100.0), (170.7, 116.5),
    (158.1, 116.5), (158.1, 121.8), (151.8, 121.8), (151.8, 122.7), (93.7, 122.7),
]
HOLES = {"H1": (96.9, 119.67), "H2": (154.9, 119.67)}   # Pi holes 3 and 4: world (-7.8, 19.33), (50.2, 19.33)
HOLE_KEEPOUT_R = 2.6     # M2.5 DIN 912 head and the Ø4.5 standoff face, plus 0.35
SOCKET_ONLY_B = [(93.7, 116.55), (158.1, 116.55), (158.1, 121.8), (151.8, 121.8), (151.8, 122.7), (93.7, 122.7)]

COPPER = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")

# ---------------------------------------------------------------- placement
# (x, y, rotation). Side is kept from the schematic transfer; U1 stays on B.
PLACE = {
    # F (top)
    "J2": (143.0, 103.6, 180),     # J9-1 head, side entry at the +Y edge; pins 5-2 over U1's 8-5
    "U1": (143.045, 112.0, 90),    # head THVD1451 on top: 1-4 face the strip, 8-5 face J2
    "C1": (139.4, 113.6, 90),      # U1 bypass, left of U1
    "J5": (153.7, 104.0, 0),       # J9-4 fan GH2 (D-092 amendment)
    "J4": (161.5, 111.3, 0),       # J9-3 audio, top entry; pads face the F audio band
    "J3": (164.5, 103.3, 0),       # J9-2 base, top entry; pads face U2's vias
    "TP3": (136.6, 110.4, 0),      # GND service pad (moved off the strip)
    "TP5": (136.6, 107.6, 0),      # 3V3
    "TP6": (148.6, 109.9, 0),      # 5V, on the 5V track
    # B (underside)
    "R3": (141.775, 106.0, 0),     # head receiver 120 R, over the A/B vias
    "R1": (145.3, 112.0, 180),     # HEAD_TX pull-up, under U1
    "U2": (164.5, 110.9, 90),      # base THVD1451; 5-8 face J3
    "R4": (165.77, 105.5, 180),    # base receiver 120 R, over the U2/J3 vias
    "R2": (160.8, 112.4, -90),     # BASE_TX pull-up; pad 2 (BASE_TX) faces the B band
    "C2": (168.4, 113.4, 90),      # U2 bypass
    "TP4": (169.6, 108.3, 0),      # isolated 5V_SENSE pad
    "Q1": (158.1, 108.4, 180),     # fan switch
    "R5": (159.0, 104.9, -90),     # FAN_EN 100 R; pad 1 on top
    "R6": (160.9, 106.4, 90),      # gate 100 k
    "D1": (153.7, 108.4, 0),       # fan flyback
    "C3": (150.4, 105.4, 90),      # fan 10 uF
    "C4": (152.4, 105.0, 90),      # fan 100 nF
}
TO_TOP = {"U1": ("Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm"), "C1": ("Capacitor_SMD.pretty", "C_0603_1608Metric")}


def setup_layers(b):
    """Two-layer file -> F / In1 / In2 / B with PCB-10's 1.6 mm stackup (D-092 item 6)."""
    if '"In1.Cu"' in b.text:
        return
    b.text = b.text.replace('\t\t(0 "F.Cu" signal)\n\t\t(2 "B.Cu" signal)\n',
                            '\t\t(0 "F.Cu" signal)\n\t\t(4 "In1.Cu" power)\n\t\t(6 "In2.Cu" signal)\n\t\t(2 "B.Cu" signal)\n', 1)
    src = (HERE.parents[1] / "pcb-10-c3-carrier" / "design" / "pcb-10-c3-carrier.kicad_pcb").read_text()
    stack = re.search(r"\t\t\(stackup\n.*?\n\t\t\)\n", src, re.S).group(0)
    b.text = b.text.replace("\t(setup\n", "\t(setup\n" + stack, 1)
    b._index()


def mounting_hole(ref, at):
    raw = (LIB / "MountingHole.pretty" / "MountingHole_2.7mm_M2.5.kicad_mod").read_text()
    raw = re.sub(r'^\(footprint "[^"]+"', '(footprint "MountingHole:MountingHole_2.7mm_M2.5"', raw)
    raw = re.sub(r"\n\t\(version \d+\)\n\t\(generator [^\n]+\)\n", "\n", raw)
    raw = raw.replace('\t(layer "F.Cu")\n',
                      f'\t(layer "F.Cu")\n\t(uuid "{K.gen_uuid(ref)}")\n'
                      f"\t(transform\n\t\t(translate {at[0]} {at[1]})\n\t\t(rotate 0)\n\t\t(scale 1 1)\n\t)\n", 1)
    raw = raw.replace('"REF**"', f'"{ref}"').replace('(layer "F.SilkS")\n\t\t(effects', '(layer "F.Fab")\n\t\t(effects', 1)
    raw = raw.replace("(attr exclude_from_pos_files exclude_from_bom)", "(attr board_only exclude_from_pos_files exclude_from_bom)")
    # Give every nested item a generated UUID so a rerun removes the footprint cleanly.
    count = iter(range(1000))
    raw = re.sub(r"\n(\t+)\(layer (\"[^\"]+\")\)\n(?!\t\(uuid)",
                 lambda m: f'\n{m.group(1)}(layer {m.group(2)})\n{m.group(1)}(uuid "{K.gen_uuid(ref + str(next(count)))}")\n', raw)
    return "\t" + raw.strip().replace("\n", "\n\t")


def board_setup(b):
    setup_layers(b)
    # Outline: the transfer's eight Edge.Cuts segments are replaced by the D-092 outline.
    b.drop(lambda k, raw: k == "gr_line" and '(layer "Edge.Cuts")' in raw)
    pts = OUTLINE + OUTLINE[:1]
    b.add(*[K.edge_line(f"edge{i}", a, c) for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    # The socket-only underside rule area now covers both tabs.
    b.drop(lambda k, raw: k == "zone" and '(name "SOCKET_ONLY_B")' in raw)
    b.add(K.keepout("SOCKET_ONLY_B", ["B.Cu"], SOCKET_ONLY_B, tracks=True, vias=True, pads=True, pour_ok=True, footprints=True)
)
    for ref, at in HOLES.items():
        b.add(mounting_hole(ref, at))
        b.add(K.keepout(f"{ref}_HEAD_AND_STANDOFF", list(COPPER), K.circle_pts(*at, HOLE_KEEPOUT_R),
                        tracks=False, vias=False, pads=True, pour_ok=False, footprints=True))
    b.drop(lambda k, raw: k == "gr_text" and "REVIEW - UNROUTED" in raw)


def placement(b):
    if "JST_XH_B2B-XH-A" in next(r for r in b.blocks("footprint") if '"Reference" "J5"' in r):
        K.replace_footprint(b, "J5", LIB / "Connector_JST.pretty", "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical")
    for ref, (lib, name) in TO_TOP.items():
        if b.fp(ref)["layer"] == "B.Cu":
            K.replace_footprint(b, ref, LIB / lib, name, side="F")
    for ref, (x, y, r) in PLACE.items():
        b.move(ref, x, y, r)


# ---------------------------------------------------------------- routing (by hand, D-060)
# Socket rows and the four lanes along the strip (KiCad y; see README "Layout").
YO, YI = 118.3983, 120.9383                  # outer (even) and inner (odd) rows
YA, YU, YL, YW = 117.145, 119.498, 119.838, 122.17


def px(k):
    """x of socket column k (pins 2k-1 inner, 2k outer)."""
    return round(101.77 + 2.54 * (k - 1), 4)


def pin(n):
    k = (n + 1) // 2
    return (px(k), YO if n % 2 == 0 else YI)


def gap(k):
    """x of the gap between columns k and k+1."""
    return round(px(k) + 1.27, 4)


# F audio band under J4's pads (0.16 mm tracks, 0.32 mm pitch), LRCLK on top.
BAND = {"LRCLK": 114.35, "BCLK": 114.67, "SDO0": 114.99, "SDI1": 115.31, "SDI0": 115.63, "AMP_SD": 115.95}
# B band to U2's 1-4 row.
BBAND = {"BASE_TX": 115.0, "BASE_RX": 115.32}

VIAS = {
    # name: (x, y, net)
    "V_HEAD_A": (141.14, 107.4, "/HEAD_C2TX_P"), "V_HEAD_B": (142.41, 107.4, "/HEAD_C2TX_N"),
    "V_HEAD_TX": (143.68, 112.0, "/HEAD_TX"),     # under U1's body, to R1
    "V_3V3_U1": (141.14, 116.4, "/+3V3_PI"), "V_3V3_R1": (147.4, 112.0, "/+3V3_PI"),
    "V_3V3_TP5": (137.9, 107.6, "/+3V3_PI"), "V_3V3_J4": (155.875, 111.75, "/+3V3_PI"),
    "V_3V3_R2": (159.7, 111.6, "/+3V3_PI"), "V_3V3_U2": (168.4, 115.3, "/+3V3_PI"),
    "V_5V_IN1": (144.95, 116.3, "/+5V_PI"), "V_5V_FAN": (152.2, 109.9, "/+5V_PI"),
    "V_FAN_SW": (154.325, 107.3, "/FAN_SW"),
    "V_BCLK": (148.76, 116.5, "/BCLK"), "V_SDI0": (152.6, 116.05, "/SDI0"), "V_AMP_SD": (153.8, 116.5, "/AMP_SD"),
    "V_5VSENSE": (167.125, 111.75, "/5V_SENSE_TP_ONLY"),
    "V_GND_C1": (139.4, 111.6, "/GND"), "V_GND_J2": (147.2, 106.9, "/GND"), "V_GND_J4": (158.375, 111.75, "/GND"),
    "V_GND_Q1": (158.0, 109.9, "/GND"), "V_GND_R6": (160.9, 104.2, "/GND"), "V_GND_C3C4": (149.2, 103.0, "/GND"),
"V_GND_C2": (169.4, 112.0, "/GND"),
}
for i, x in enumerate((162.595, 163.865, 165.135, 166.405)):       # U2 5-8 up to J3 2-5
    VIAS[f"V_BASE_{i + 5}"] = (x, 106.75, ("/BASE_C0TX_P", "/BASE_C0TX_N", "/BASE_C3TX_N", "/BASE_C3TX_P")[i])


def routes():
    """(name, layer, net, width, points)"""
    J4 = lambda k: (161.5 - 5.625 + 1.25 * (k - 1), 113.25)
    r = []
    add = lambda name, layer, net, w, *pts: r.append((name, layer, net, w, list(pts)))
    # --- F lanes: head link and audio
    add("HEAD_RX", "F.Cu", "/HEAD_RX", 0.2, pin(10), (px(5), YA), (142.41, YA), (142.41, 114.475))
    add("HEAD_TX", "F.Cu", "/HEAD_TX", 0.16, pin(8), (px(4), YU), (143.68, YU), (143.68, 114.475), (143.68, 112.0))
    add("LRCLK", "F.Cu", "/LRCLK", 0.16, pin(35), (px(18), YL), (gap(18), YL), (gap(18), BAND["LRCLK"]),
        (J4(2)[0], BAND["LRCLK"]), J4(2))
    add("SDO0", "F.Cu", "/SDO0", 0.16, pin(40), (px(20), BAND["SDO0"]), (J4(6)[0], BAND["SDO0"]), J4(6))
    add("SDI1", "F.Cu", "/SDI1", 0.16, pin(15), (px(8), YW), (151.4, YW), (151.4, BAND["SDI1"]),
        (J4(7)[0], BAND["SDI1"]), J4(7))
    add("BCLK_F", "F.Cu", "/BCLK", 0.16, VIAS["V_BCLK"][:2], (148.76, BAND["BCLK"]), (J4(4)[0], BAND["BCLK"]), J4(4))
    add("SDI0_F", "F.Cu", "/SDI0", 0.16, VIAS["V_SDI0"][:2], (152.6, BAND["SDI0"]), (J4(8)[0], BAND["SDI0"]), J4(8))
    add("AMP_SD_F", "F.Cu", "/AMP_SD", 0.16, VIAS["V_AMP_SD"][:2], (153.8, BAND["AMP_SD"]), (J4(9)[0], BAND["AMP_SD"]), J4(9))
    # head differential lines, straight from U1 8-5 to J2 5-2
    for net, x in (("/HEAD_C2TX_P", 141.14), ("/HEAD_C2TX_N", 142.41), ("/HEAD_C0TX_N", 143.68), ("/HEAD_C0TX_P", 144.95)):
        add("HEAD_DIFF" + net, "F.Cu", net, 0.2, (x, 109.525), (x, 105.45))
    # U1 supply and bypass
    add("U1_3V3", "F.Cu", "/+3V3_PI", 0.3, (139.4, 114.475), (141.14, 114.475), VIAS["V_3V3_U1"][:2])
    add("C1_GND", "F.Cu", "/GND", 0.3, (139.4, 112.825), VIAS["V_GND_C1"][:2])
    # 5V on F from the In1 via round U1 to J5 pin 1 (TP6 on it)
    add("5V_F", "F.Cu", "/+5V_PI", 0.4, VIAS["V_5V_IN1"][:2], (145.75, 116.3), (145.75, 109.9), (152.2, 109.9),
        (153.075, 109.025), (153.075, 105.95))
    add("FAN_SW_F", "F.Cu", "/FAN_SW", 0.3, (154.325, 105.95), VIAS["V_FAN_SW"][:2])
    # J4 supply, ground and isolated sense pins to their vias
    for k, v in ((1, "V_3V3_J4"), (3, "V_GND_J4"), (10, "V_5VSENSE")):
        add(f"J4_{k}", "F.Cu", VIAS[v][2], 0.25, J4(k), VIAS[v][:2])
    # J3 2-5 from the U2 vias; J3 pin 1 ground
    for i, x in enumerate((162.625, 163.875, 165.125, 166.375)):
        v = VIAS[f"V_BASE_{i + 5}"]
        add(f"J3_{i + 2}", "F.Cu", v[2], 0.2, v[:2], (v[0], 105.25))   # lands inside the 0.6 mm pad
    add("J2_1", "F.Cu", "/GND", 0.25, (146.125, 105.45), (146.125, 106.9), VIAS["V_GND_J2"][:2])
    add("TP5", "F.Cu", "/+3V3_PI", 0.3, (136.6, 107.6), VIAS["V_3V3_TP5"][:2])
    # I2C1 service pads in the strip
    add("SDA", "F.Cu", "/I2C1_SDA", 0.2, pin(3), (105.58, 119.6683))
    add("SCL", "F.Cu", "/I2C1_SCL", 0.2, pin(5), (108.12, 119.6683))
    # --- In2 lanes: three audio nets hop to F at their vias (In2 is the 3V3 plane elsewhere)
    add("BCLK_IN2", "In2.Cu", "/BCLK", 0.2, pin(12), (px(6), YA), (148.76, YA), VIAS["V_BCLK"][:2])
    add("SDI0_IN2", "In2.Cu", "/SDI0", 0.16, pin(38), (px(19), YU), (151.52, YU), (151.52, 116.05), VIAS["V_SDI0"][:2])
    add("AMP_SD_IN2", "In2.Cu", "/AMP_SD", 0.16, pin(16), (px(8), YL), (151.84, YL), (151.84, 116.95),
        (153.35, 116.95), VIAS["V_AMP_SD"][:2])
    add("3V3_LINK", "In2.Cu", "/+3V3_PI", 0.25, pin(1), (px(1), YW), (px(9), YW), pin(17))   # pins 1 and 17, same Pi rail
    # --- In1: 5V from pins 2/4 along the W lane (In1 is the GND plane elsewhere)
    add("5V_IN1", "In1.Cu", "/+5V_PI", 0.4, pin(4), (px(2), 119.6683), (gap(2), 119.6683), (gap(2), YW), (gap(17), YW),
        (gap(17), 117.57), VIAS["V_5V_IN1"][:2])
    # 3V3 from pin 1 along In1's A lane to U1's via (In2's strip copper is cut off by AMP_SD)
    add("3V3_IN1", "In1.Cu", "/+3V3_PI", 0.3, pin(1), (px(1), 119.6683), (gap(1), 119.6683), (gap(1), YA), (141.14, YA),
        VIAS["V_3V3_U1"][:2])
    # --- B lanes
    add("5V_LINK", "B.Cu", "/+5V_PI", 0.4, pin(2), (px(1), YA), (px(2), YA), pin(4))
    add("FAN_EN", "B.Cu", "/FAN_EN", 0.2, pin(18), (px(9), YA), (136.0, YA), (136.0, 110.8), (161.65, 110.8),
        (161.65, 103.4), (159.0, 103.4), (159.0, 104.075))
    add("BASE_TX", "B.Cu", "/BASE_TX", 0.16, pin(7), (px(4), YL), (gap(15), YL), (gap(15), BBAND["BASE_TX"]),
        (163.865, BBAND["BASE_TX"]), (163.865, 113.375))
    add("BASE_TX_R2", "B.Cu", "/BASE_TX", 0.16, (160.8, BBAND["BASE_TX"]), (160.8, 113.225))
    add("BASE_RX", "B.Cu", "/BASE_RX", 0.16, pin(29), (px(15), YW), (gap(18), YW), (gap(18), BBAND["BASE_RX"]),
        (165.135, BBAND["BASE_RX"]), (165.135, 113.375))
    # head side: diff lines to R3, HEAD_TX to R1, R1 supply
    add("R3_A", "B.Cu", "/HEAD_C2TX_P", 0.2, VIAS["V_HEAD_A"][:2], (141.14, 106.81), (140.95, 106.62), (140.95, 106.0))
    add("R3_B", "B.Cu", "/HEAD_C2TX_N", 0.2, VIAS["V_HEAD_B"][:2], (142.41, 106.19), (142.6, 106.0))
    add("R1_TX", "B.Cu", "/HEAD_TX", 0.2, VIAS["V_HEAD_TX"][:2], (144.475, 112.0))
    add("R1_3V3", "B.Cu", "/+3V3_PI", 0.3, (146.125, 112.0), VIAS["V_3V3_R1"][:2])
    # fan switch
    add("5V_B", "B.Cu", "/+5V_PI", 0.4, VIAS["V_5V_FAN"][:2], (152.2, 105.775), (152.4, 105.775))
    add("5V_C3", "B.Cu", "/+5V_PI", 0.4, (152.2, 106.35), (150.4, 106.35))
    add("FAN_SW_B", "B.Cu", "/FAN_SW", 0.3, VIAS["V_FAN_SW"][:2], (155.35, 108.325), (155.35, 108.4), (157.1625, 108.4))
    add("FAN_GATE", "B.Cu", "/FAN_GATE", 0.2, (159.0, 105.725), (159.0, 107.45))
    add("FAN_GATE_R6", "B.Cu", "/FAN_GATE", 0.2, (159.0, 106.5), (160.9, 106.5), (160.9, 107.225))
    add("Q1_GND", "B.Cu", "/GND", 0.3, (159.0375, 109.35), (158.4875, 109.9), VIAS["V_GND_Q1"][:2])
    add("R6_GND", "B.Cu", "/GND", 0.25, (160.9, 105.575), VIAS["V_GND_R6"][:2])
    add("C3C4_GND", "B.Cu", "/GND", 0.3, (150.4, 104.45), (150.4, 103.0), (152.4, 103.0), (152.4, 104.225))
    add("C3C4_GND_V", "B.Cu", "/GND", 0.3, (150.4, 103.0), VIAS["V_GND_C3C4"][:2])
    # base side
    for i, x in enumerate((162.595, 163.865, 165.135, 166.405)):
        v = VIAS[f"V_BASE_{i + 5}"]
        add(f"U2_{i + 5}", "B.Cu", v[2], 0.2, (x, 108.425), v[:2])
    add("R4_P", "B.Cu", "/BASE_C3TX_P", 0.2, VIAS["V_BASE_8"][:2], (166.405, 105.5), (166.595, 105.5))
    add("R4_N", "B.Cu", "/BASE_C3TX_N", 0.2, VIAS["V_BASE_7"][:2], (165.135, 105.5), (164.945, 105.5))
    add("U2_3V3", "B.Cu", "/+3V3_PI", 0.3, (166.405, 113.375), (167.2, 113.375), (168.0, 114.175), (168.4, 114.175),
        VIAS["V_3V3_U2"][:2])
    add("R2_3V3", "B.Cu", "/+3V3_PI", 0.3, (160.8, 111.6), VIAS["V_3V3_R2"][:2])
    add("C2_GND", "B.Cu", "/GND", 0.3, (168.4, 112.625), (168.775, 112.625), (169.4, 112.0))
    add("TP4", "B.Cu", "/5V_SENSE_TP_ONLY", 0.25, VIAS["V_5VSENSE"][:2], (167.125, 110.2), (169.025, 108.3), (169.6, 108.3))
    return r


def routing(b):
    items = []
    for name, layer, net, w, pts in routes():
        items += K.track(name, pts, w, layer, net)
    for name, (x, y, net) in VIAS.items():
        items.append(K.via(name, (x, y), net))
    outline = OUTLINE
    items.append(K.pour("GND_IN1", "In1.Cu", "/GND", outline, priority=1))
    items.append(K.pour("3V3_IN2", "In2.Cu", "/+3V3_PI", outline, priority=1))
    items.append(K.pour("GND_F", "F.Cu", "/GND", outline))
    items.append(K.pour("GND_B", "B.Cu", "/GND", outline))
    b.add(*items)


# ---------------------------------------------------------------- outputs
FAB = HERE.parent / "fab" / "revA"
STEP = HERE.parent / "cad" / "pcb-09-c0-link-adapter-revA.step"
ORIGIN = (93.7, 122.7)    # board bottom-left as seen from the top: every output uses it (PCB-11 trap)
COPPER_AND_FAB_LAYERS = "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"
MPN = {  # BOM part numbers; values come from the schematic
    "J1": ("SSW-120-01-T-D", "Samtec"), "J2": ("SM06B-GHS-TB(LF)(SN)", "JST"), "J3": ("BM06B-GHS-TBT(LF)(SN)(N)", "JST"),
    "J4": ("BM10B-GHS-TBT(LF)(SN)(N)", "JST"), "J5": ("BM02B-GHS-TBT(LF)(SN)(N)", "JST"),
    "U1": ("THVD1451DR", "Texas Instruments"), "U2": ("THVD1451DR", "Texas Instruments"),
    "Q1": ("AO3400A", "Alpha & Omega"), "D1": ("1N5819HW-7-F", "Diodes Inc."),
}


def set_origin(b):
    b.text = re.sub(r"\(aux_axis_origin [-\d.]+ [-\d.]+\)", f"(aux_axis_origin {ORIGIN[0]} {ORIGIN[1]})", b.text, count=1)
    b.text = re.sub(r"\(grid_origin [-\d.]+ [-\d.]+\)", f"(grid_origin {ORIGIN[0]} {ORIGIN[1]})", b.text, count=1)
    b._index()


def export():
    import csv
    import shutil
    import subprocess
    import zipfile
    run = lambda *a: subprocess.run([K.CLI, *a, str(BOARD)], check=True, capture_output=True, text=True)
    gerb = FAB / "gerbers"
    shutil.rmtree(gerb, ignore_errors=True)
    gerb.mkdir(parents=True)
    STEP.parent.mkdir(exist_ok=True)
    run("pcb", "export", "gerbers", "--layers", COPPER_AND_FAB_LAYERS, "--use-drill-file-origin", "-o", str(gerb) + "/")
    run("pcb", "export", "drill", "--format", "excellon", "--excellon-units", "mm", "--drill-origin", "plot",
        "--excellon-separate-th", "--generate-map", "--map-format", "pdf", "-o", str(gerb) + "/")
    pos = FAB / "pcb-09-c0-link-adapter-revA-pos.csv"
    run("pcb", "export", "pos", "--side", "both", "--format", "csv", "--units", "mm", "--use-drill-file-origin",
        "--exclude-dnp", "-o", str(pos))
    with open(pos) as f, open(FAB / "pcb-09-c0-link-adapter-revA-cpl-jlcpcb.csv", "w", newline="") as g:
        w = csv.writer(g)
        w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for row in csv.DictReader(f):
            w.writerow([row["Ref"], f"{float(row['PosX']):.4f}mm", f"{float(row['PosY']):.4f}mm",
                        "Top" if row["Side"] == "top" else "Bottom", f"{float(row['Rot']):g}"])
    b = K.Board(BOARD)
    groups = {}
    for raw in b.blocks("footprint"):
        n = K.parse(raw)
        attr = K.find(n, "attr") or []
        if "exclude_from_bom" in attr or "board_only" in attr:
            continue
        props = {p[1]: p[2] for p in K.find_all(n, "property")}
        ref = props["Reference"]
        key = (props["Value"], n[1], *MPN.get(ref, ("", "")))
        groups.setdefault(key, []).append(ref)
    natural = lambda r: (re.match(r"\D+", r).group(0), int(re.search(r"\d+", r).group(0)))
    with open(FAB / "pcb-09-c0-link-adapter-revA-bom.csv", "w", newline="") as g:
        w = csv.writer(g, quoting=csv.QUOTE_ALL)
        w.writerow(["Comment", "Designator", "Footprint", "Quantity", "MPN", "Manufacturer", "LCSC Part #"])
        for (val, fp, mpn, mfr), refs in sorted(groups.items(), key=lambda kv: natural(sorted(kv[1], key=natural)[0])):
            refs = sorted(refs, key=natural)
            w.writerow([val, ",".join(refs), fp, len(refs), mpn, mfr, ""])
    with zipfile.ZipFile(FAB / "pcb-09-c0-link-adapter-revA-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(gerb.iterdir()):
            if f.suffix != ".pdf":
                z.write(f, f.name)
    # --user-origin 0x0mm: STEP (X, Y) = (KiCad x, -y), so world X = Xs - 104.7, Y = 139 + Ys (pcb_integration.py).
    run("pcb", "export", "step", "--subst-models", "--force", "--user-origin", "0x0mm", "-o", str(STEP))
    print("exported", FAB, STEP)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-drc", action="store_true")
    ap.add_argument("--export", action="store_true", help="also write fab/revA and cad/ outputs")
    args = ap.parse_args()
    b = K.Board(BOARD)
    b.drop_generated()
    board_setup(b)
    placement(b)
    routing(b)
    set_origin(b)
    b.save()
    if args.no_drc:
        return
    r = K.drc(BOARD, HERE / "layout-drc.json")
    print(f"DRC: {r['violations']} violations, {r['unconnected']} unconnected, {r['parity']} parity")
    print(K.summary(r["report"]))
    if args.export:
        export()


if __name__ == "__main__":
    main()
