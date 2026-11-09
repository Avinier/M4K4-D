"""PCB-12 rev A: create, place and hand-route the two-layer 0.8 mm C2 carrier (D-102).

The board stands vertical in the head's roll-carried frame, in the old C2
tray's front-wall plane, component face toward -X (rear). Seen from that face
(KiCad's top view), world -Y is to the right and +Z is up; in head-local mm

    KiCad x = 71 - Y     (Y -29, the Zero's centre -> x 100)
    KiCad y = 139.75 - Z (Z 39.75, the Zero's centre -> y 100)

and the KiCad STEP (--user-origin 0x0mm) maps to head-local by Y = 71 - x_step,
Z = 139.75 + y_step, X = -24.2 - z_step (the component face is at X -25.0).
check_pcb12_fit.py uses the same transform.

Headless, as PCB-14: `--create` writes the board from a skeleton block per
symbol (PCB-08's FH34 block carrying this schematic's path and pad nets),
swapped for the library land pattern by kfile.replace_footprint; the Nightly
DRC then rewrites it in KiCad's own form. No autorouter: every track below
is placed by hand, octolinear.
"""

import argparse
import json
import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

NAME = "pcb-12-c2-head-carrier"
BOARD = HERE / f"{NAME}.kicad_pcb"
REPORT = HERE / "placement-drc.json"
PCB08 = HERE.parents[1] / "pcb-08-yaw-junction" / "design" / "pcb-08-yaw-junction.kicad_pcb"
STOCK = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")
PROJECT_LIB = HERE.parents[1] / "lib"
THICKNESS = 0.8


def xy(y, z):
    """Head-local (Y, Z) -> KiCad (x, y)."""
    return (round(71.0 - y, 4), round(139.75 - z, 4))


# Board Y -44..-14, Z 8..51.5 (D-102); M2 holes at Y -41.5/-16.5, Z 48.16 into
# new crossbar bosses, clear of the Zero's edge pads.
OUTLINE = (85.0, 88.25, 115.0, 131.75)
HOLES = [(87.5, 91.59), (112.5, 91.59)]
HOLE_R, HEAD_KEEPOUT_R = 1.1, 2.0

PLACE = {   # ref: (x, y, rotation); signals escape the Zero's outer pad ends into side strips
    "U1": (100.0, 100.0, 0),        # ESP32-S3-Zero, USB-C up (+Z), seat unchanged
    # display (left): U5 A/B straight down to J3
    "R9": (87.325, 102.5, 0),       # DISP_DE pull-down, on the DE lane in the left strip
    "U5": (90.0, 118.3, 270),
    "J3": (89.6, 128.0, 180),
    # middle column
    "C5": (94.1, 118.3, 90),        # U5 decoupling
    "R10": (94.1, 122.0, 90),       # GND_DISPLAY -> GND
    "C3": (96.9, 118.8, 90),        # U2 decoupling
    "C1": (96.9, 122.2, 90),        # +5V_C2 bulk 10u
    # head link (middle): U2 Y/Z/B/A straight down to J1 pins 5..2
    "R3": (99.5, 113.9, 0),         # LINK_TX pull-up, pad 2 on the LINK_TX track
    "U2": (101.05, 119.5, 270),
    "R2": (102.32, 123.95, 0),      # C0TX termination, inline on the pair
    "R1": (104.6, 123.2, 90),       # GND_SIG -> GND
    "J1": (100.4, 128.0, 180),
    # servo (right): inputs from the Zero's right pads, RX straight up into pad 10. J2 sits
    # above the board's low -Y corner, which the roll/pitch sweep reserves (check_pcb12_fit.py).
    "U4": (107.0, 114.6, 90),       # RX buffer, OE low: VCC/Y on top, /OE A GND below
    "U3": (112.0, 114.6, 270),      # TX buffer, OE high: OE A GND on top, VCC/Y below
    "R4": (109.5, 114.6, 270),      # 47R between them, DRV top -> DATA bottom
    "C4": (104.55, 113.6, 90),      # U3/U4 decoupling, beside U4's VCC
    "R5": (105.55, 119.9, 90),      # SERVO_DATA pull-up
    "J2": (109.8, 120.2, 180),      # pins up, toward the buffers
    "R7": (114.1, 120.0, 270),      # GND_HEAD_REF -> GND
    "R6": (112.95, 101.5, 90),      # SERVO_DIR pull-down, on the DIR lane
    "TP1": (113.6, 97.5, 0),        # GND
}
BARE = ("TP1",)


def sym_uuid(ref):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb12/" + ref))


def create():
    src = PCB08.read_text()
    head = src[:src.index("\t(footprint ")].replace("(thickness 1.6)", f"(thickness {THICKNESS})", 1)
    template = next(raw for raw in K.Board(PCB08).blocks("footprint") if '(property "Reference" "J3"' in raw)
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    blocks = []
    for ref, item in manifest.items():
        if ref.startswith("#"):
            continue
        raw = re.sub(r"\(rotate [-\d.]+\)", "(rotate 0)", template, count=1)
        raw = re.sub(r"(\(at [-\d.]+ [-\d.]+) 90\)", r"\1)", raw)
        raw = raw.replace('(property "Reference" "J3"', f'(property "Reference" "{ref}"', 1)
        raw = re.sub(r'\(property "Value" "[^"]*"', f'(property "Value" "{item["value"]}"', raw, count=1)
        raw = re.sub(r'\(path "/[^"]+"\)', f'(path "/{sym_uuid(ref)}")', raw, count=1)
        raw = raw.replace("pcb-08-yaw-junction.kicad_sch", f"{NAME}.kicad_sch")

        def pad_net(m):
            block = m.group(0)
            num = re.match(r'\t\t\(pad "(\d+)"', block).group(1)
            if num not in item["pins"]:
                return re.sub(r'\t\t\t\(net "[^"]*"\)\n', "", block, count=1)
            net = item["pins"][num]
            # No-connect pins get KiCad's own single-pad nets, as the netlist names them.
            name = f"/{net}" if net else f"unconnected-({ref}-Pin_{num}-Pad{num})"
            return re.sub(r'\(net "[^"]*"\)', f'(net "{name}")', block, count=1)
        raw = re.sub(r'\t\t\(pad "\d+".*?\n\t\t\)\n', pad_net, raw, flags=re.S)
        ids = iter(range(100000))
        raw = re.sub(r'\(uuid "[^"]+"\)',
                     lambda m: f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb12/fp/" + ref + "/" + str(next(ids)))}")', raw)
        blocks.append((ref, raw))
    BOARD.write_text(head + "\n".join(raw for _, raw in blocks) + "\n\t(embedded_fonts no)\n)\n")
    b = K.Board(BOARD)
    for ref, item in manifest.items():
        if ref.startswith("#"):
            continue
        lib, name = item["footprint"].split(":")
        lib_dir = PROJECT_LIB / f"{lib}.pretty" if lib == "pcb12" else STOCK / f"{lib}.pretty"
        K.replace_footprint(b, ref, lib_dir, name)
    for ref, item in manifest.items():
        if ref.startswith("#"):
            continue
        attrs = []
        if item.get("dnp"):
            attrs.append("dnp")
        if ref in BARE:
            attrs += ["exclude_from_pos_files", "exclude_from_bom"]
        if attrs:
            set_attr(b, ref, attrs)
    b.save()
    print("created", BOARD.name)


def block_of(b, ref):
    for kind, start, end in b.items:
        raw = b.text[start:end]
        if kind == "footprint" and f'(property "Reference" "{ref}"' in raw:
            return start, end, raw
    raise KeyError(ref)


def set_attr(b, ref, extra):
    start, end, raw = block_of(b, ref)
    m = re.search(r"\(attr ([^)]*)\)", raw)
    words = (m.group(1).split() if m else ["smd"])
    words += [w for w in extra if w not in words]
    new = f"(attr {' '.join(words)})"
    raw = raw.replace(m.group(0), new, 1) if m else raw.replace("\t\t(pad ", f"\t\t{new}\n\t\t(pad ", 1)
    b.text = b.text[:start] + raw + b.text[end:]
    b._index()


def setup(b):
    b.drop_generated()
    b.drop(lambda kind, raw: kind in ("gr_line", "gr_rect", "gr_circle", "gr_text") and
           ('(layer "Edge.Cuts")' in raw or "SilkS" in raw))
    x0, y0, x1, y1 = OUTLINE
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    b.add(*[K.edge_line(f"pcb12-edge-{i}", a, c, 0.05) for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    for i, (hx, hy) in enumerate(HOLES):
        b.add(f'\t(gr_circle\n\t\t(center {hx} {hy})\n\t\t(end {hx + HOLE_R} {hy})\n\t\t(stroke\n\t\t\t(width 0.05)\n'
              f'\t\t\t(type default)\n\t\t)\n\t\t(fill no)\n\t\t(layer "Edge.Cuts")\n\t\t(uuid "{K.gen_uuid(f"pcb12-hole-{i}")}")\n\t)')
        # The M2 button head bears on the component face: no copper under it.
        b.add(K.keepout(f"head-{i}", ["F.Cu"], K.circle_pts(hx, hy, HEAD_KEEPOUT_R, 24), tracks=False, vias=False,
                        pads=False, pour_ok=False, footprints=False))
    for ref, (x, y, rot) in PLACE.items():
        b.move(ref, x, y, rot)
    for ref in PLACE:   # references on the assembly drawing (JLCPCB minimum silk text is 1.0 mm)
        start, end, raw = block_of(b, ref)
        raw = re.sub(r'(\(property "Reference" "[^"]+"\s+\(at [^)]*\)\s+\(layer )"F.SilkS"', r'\1"F.Fab"', raw, count=1)
        b.text = b.text[:start] + raw + b.text[end:]
        b._index()
    b.add(f'\t(gr_text "PCB-12 A"\n\t\t(at 100 104.5 0)\n\t\t(layer "B.SilkS")\n\t\t(uuid "{K.gen_uuid("silk-id")}")\n'
          '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t\t(thickness 0.16)\n\t\t\t)\n\t\t\t(justify mirror)\n\t\t)\n\t)')


def route(b):
    """Hand-planned tracks (octolinear). Signals on F.Cu; +5V/+3V3 trunks and two crossings on B.Cu."""
    parts = []
    P = lambda ref, n: tuple(b.pad(ref, n)["at"])

    def octo(pts):
        """Split any non-octolinear leg into a straight run and an exact 45 deg leg at its end."""
        out = [pts[0]]
        for a, c in zip(pts, pts[1:]):
            dx, dy = c[0] - a[0], c[1] - a[1]
            if abs(dx) > 1e-6 and abs(dy) > 1e-6 and abs(abs(dx) - abs(dy)) > 1e-6:
                sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
                if abs(dy) > abs(dx):
                    out.append((round(a[0], 4), round(c[1] - sy * abs(dx), 4)))
                else:
                    out.append((round(c[0] - sx * abs(dy), 4), round(a[1], 4)))
            if abs(dx) > 1e-6 or abs(dy) > 1e-6:
                out.append(c)
        return out

    def t(name, net, width, layer, *pts):
        parts.extend(K.track(name, octo(list(pts)), width, layer, "/" + net))

    def v(name, net, at):
        parts.append(K.via(name, at, "/" + net))

    S = 0.2   # signal width
    # ---- Zero power: F stubs from the pads' inner ends to tented vias under the module.
    v5, vg, v3 = (93.35, 89.84), (93.35, 92.38), (93.35, 94.92)
    t("Z5V", "+5V_C2", 0.5, "F.Cu", P("U1", 1), v5)
    t("ZGND", "GND", 0.5, "F.Cu", P("U1", 2), vg)
    t("Z3V3", "+3V3", 0.4, "F.Cu", P("U1", 3), v3)
    for n, net, at in (("Z5V", "+5V_C2", v5), ("ZGND", "GND", vg), ("Z3V3", "+3V3", v3)):
        v(n, net, at)
    # +5V_C2: B.Cu down x 92.2 (under the left pads, outside the antenna keep-out) to J1 pin 6.
    v5b = (97.9, 124.4)
    t("5V_B", "+5V_C2", 0.5, "B.Cu", v5, (92.2, 90.99), (92.2, 123.9), (97.4, 123.9), v5b)
    v("5V_J1", "+5V_C2", v5b)
    t("5V_J1", "+5V_C2", 0.5, "F.Cu", v5b, P("J1", 6))
    t("5V_C1", "+5V_C2", 0.4, "F.Cu", v5b, (97.9, 123.975), (96.9, 122.975))
    # +3V3: B.Cu down x 92.9, across ky 115.0, branches to the parts' vias.
    vA, vC, vB, vU4 = (95.5, 119.075), (98.675, 115.0), (102.955, 115.0), (106.05, 112.0)
    vR5, vU3 = (106.0, 121.7), (114.2, 116.6)
    t("3V3_B", "+3V3", 0.3, "B.Cu", v3, (92.9, 95.37), (92.9, 115.0), (103.9, 115.0),
      (103.9, 121.7), vR5)
    t("3V3_B_A", "+3V3", 0.3, "B.Cu", (95.5, 115.0), vA)
    t("3V3_B_U4", "+3V3", 0.3, "B.Cu", (103.9, 115.0), (106.05, 112.85), vU4)
    t("3V3_B_U3", "+3V3", 0.3, "B.Cu", (103.9, 118.2), (112.6, 118.2), vU3)
    for n, at in (("A", vA), ("C", vC), ("B", vB), ("U4", vU4), ("R5", vR5), ("U3", vU3)):
        v("3V3_" + n, "+3V3", at)
    t("3V3_U5", "+3V3", 0.3, "F.Cu", (91.905, 120.3), (92.875, 120.3), P("C5", 1), vA)
    t("3V3_U5p", "+3V3", 0.3, "F.Cu", P("U5", 8), (91.905, 120.3))
    t("3V3_C3", "+3V3", 0.3, "F.Cu", vA, (96.0, 119.575), P("C3", 1))
    t("3V3_R3", "+3V3", 0.3, "F.Cu", P("R3", 1), vC)
    t("3V3_U2", "+3V3", 0.3, "F.Cu", vB, (102.955, 116.4))
    t("3V3_U4p", "+3V3", 0.3, "F.Cu", vU4, P("U4", 5))
    t("3V3_U3p", "+3V3", 0.3, "F.Cu", vU3, (113.55, 116.6), P("U3", 5))
    t("3V3_C4", "+3V3", 0.3, "F.Cu", vB, (103.53, 114.425), P("C4", 1))
    t("3V3_R5p", "+3V3", 0.3, "F.Cu", P("R5", 1), (105.55, 121.25), vR5)

    # ---- Left strip, outer to inner: DISP_TX 85.7, DISP_DE 86.5, DISP_RX 87.1, LINK_TX 87.7, LINK_RX 88.3.
    t("DISP_TX", "DISP_TX", S, "F.Cu", P("U1", 4), (85.7, 97.46), (85.7, 114.8), (85.9, 115.0), (88.095, 115.0))
    t("DISP_DE", "DISP_DE", S, "F.Cu", P("U1", 5), (86.5, 100.0), (86.5, 114.05), (86.8, 114.35),
      (90.635, 114.35), (90.635, 115.2))
    t("DISP_DE3", "DISP_DE", S, "F.Cu", (89.365, 114.35), (89.365, 115.2))
    t("DISP_RX", "DISP_RX", S, "F.Cu", P("U1", 7), (87.1, 105.08), (87.1, 113.45), (87.4, 113.75),
      (91.605, 113.75), (91.905, 114.05), (91.905, 115.2))
    t("LINK_TX", "LINK_TX", S, "F.Cu", P("U1", 8), (87.7, 107.62), (87.7, 112.85), (88.0, 113.15),
      (99.575, 113.15), P("R3", 2), (100.325, 116.4), (100.415, 116.49), (100.415, 117.025))
    t("LINK_RX", "LINK_RX", S, "F.Cu", P("U1", 9), (88.3, 110.16), (88.3, 112.25), (88.6, 112.55),
      (101.385, 112.55), (101.685, 112.85), (101.685, 117.025))
    # R9 GND to a via (B.Cu plane).
    vR9 = (88.9, 103.6)
    t("R9_GND", "GND", 0.3, "F.Cu", P("R9", 2), (88.15, 102.85), vR9)
    v("R9_GND", "GND", vR9)

    # ---- Display pair and ground bond.
    t("DISP_A", "DISP_A", S, "F.Cu", (89.365, 121.4), (89.365, 122.5), (88.35, 123.515), P("J3", 3))
    t("DISP_B", "DISP_B", S, "F.Cu", (90.635, 121.4), (90.635, 122.5), (89.6, 123.535), P("J3", 2))
    t("GND_DISP", "GND_DISPLAY", 0.3, "F.Cu", P("J3", 1), (90.85, 124.5), (92.525, 122.825), P("R10", 1))

    # ---- Head link pair: straight down to J1, termination inline on the pair.
    t("C2TX_P", "C2TX_P", S, "F.Cu", (99.145, 121.6), P("J1", 5))
    t("C2TX_N", "C2TX_N", S, "F.Cu", (100.415, 121.6), (100.415, 122.5), (100.4, 122.515), P("J1", 4))
    t("C0TX_N", "C0TX_N", S, "F.Cu", (101.685, 121.6), (101.685, 122.5), P("R2", 1))
    t("C0TX_P", "C0TX_P", S, "F.Cu", (102.955, 121.6), (102.955, 122.5), P("R2", 2))
    t("C0TX_N2", "C0TX_N", S, "F.Cu", P("R2", 1), (101.495, 124.5), P("J1", 3))
    t("C0TX_P2", "C0TX_P", S, "F.Cu", P("R2", 2), (103.145, 124.5), P("J1", 2))
    t("GND_SIG", "GND_SIG", 0.3, "F.Cu", P("J1", 1), (104.15, 124.575), P("R1", 1))

    # ---- Servo. RX straight up into pad 10; TX right then down into U3 A; DIR lane x 112.95.
    t("SERVO_RX", "SERVO_RX", S, "F.Cu", P("U4", 4), (107.95, 110.16))
    t("SERVO_TX", "SERVO_TX", S, "F.Cu", P("U1", 11), (112.0, 107.62), P("U3", 2))
    t("SERVO_DIR", "SERVO_DIR", S, "F.Cu", P("U1", 12), (112.95, 105.08), P("U3", 1))
    t("SERVO_DIR_R6", "SERVO_DIR", S, "F.Cu", (112.95, 105.08), P("R6", 1))
    vD, vD2 = (112.95, 111.2), (104.9, 116.0)
    v("DIR_1", "SERVO_DIR", vD)
    v("DIR_2", "SERVO_DIR", vD2)
    t("SERVO_DIR_B", "SERVO_DIR", S, "B.Cu", vD, (109.15, 115.0), (105.9, 115.0), vD2)
    t("SERVO_DIR_U4", "SERVO_DIR", S, "F.Cu", vD2, P("U4", 1))
    t("SERVO_DRV", "SERVO_DRV", S, "F.Cu", P("U3", 4), (110.45, 115.7375), (110.45, 114.4), P("R4", 1))
    t("SERVO_DATA", "SERVO_DATA", S, "F.Cu", P("R4", 2), (109.5, 116.9), (107.5, 116.9), (107.0, 116.4), P("U4", 2))
    t("SERVO_DATA_J2", "SERVO_DATA", S, "F.Cu", (109.5, 116.9), P("J2", 2))
    t("SERVO_DATA_R5", "SERVO_DATA", S, "F.Cu", (107.5, 116.9), (106.55, 116.9), (105.55, 117.9), P("R5", 2))
    t("GND_HEAD", "GND_HEAD_REF", 0.3, "F.Cu", P("J2", 1), (110.425, 117.3), (113.0, 117.3), (113.9, 118.2),
      P("R7", 1))
    # R6 GND to the plane.
    vR6 = (112.95, 99.6)
    t("R6_GND", "GND", 0.3, "F.Cu", P("R6", 2), vR6)
    v("R6_GND", "GND", vR6)

    # ---- Ground: B.Cu plane over the board, F.Cu pour round the parts (not under the module).
    x0, y0, x1, y1 = OUTLINE
    parts.append(K.pour("GND_B", "B.Cu", "/GND", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                        clearance=0.2, min_width=0.2, solid=True))
    parts.append(K.pour("GND_F", "F.Cu", "/GND",
                        [(x0, y0), (91.0, y0), (91.0, 111.9), (109.0, 111.9), (109.0, y0), (x1, y0), (x1, y1), (x0, y1)],
                        clearance=0.2, min_width=0.2, solid=True))
    # Stitching vias round the lower area.
    for i, at in enumerate([(95.5, 125.6), (106.9, 124.9), (112.0, 126.5), (86.0, 125.0),
                            (92.9, 126.9), (108.0, 127.0)]):
        v(f"STITCH_{i}", "GND", at)
    b.add(*parts)


FAB = HERE.parent / "fab" / "revA"
STEP = HERE.parent / "cad" / f"{NAME}-revA.step"
ORIGIN = (OUTLINE[0], OUTLINE[3])
LAYERS = "F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"


def set_origin(b):
    for key in ("aux_axis_origin", "grid_origin"):
        line = f"({key} {ORIGIN[0]} {ORIGIN[1]})"
        if f"({key} " in b.text:
            b.text = re.sub(rf"\({key} [-\d.]+ [-\d.]+\)", line, b.text, count=1)
        else:
            b.text = b.text.replace("\t(setup\n", f"\t(setup\n\t\t{line}\n", 1)
    b._index()


MPN = {
    "U1": ("ESP32-S3-Zero (SKU 25081, without header)", "Waveshare"), "U2": ("THVD1451DR", "TI"),
    "U5": ("THVD1450DR", "TI"), "U3": ("SN74LVC1G126DBVR", "TI"), "U4": ("SN74LVC1G125DBVR", "TI"),
    "J1": ("BM07B-GHS-TBT(LF)(SN)(N)", "JST"), "J2": ("BM02B-GHS-TBT(LF)(SN)(N)", "JST"),
    "J3": ("BM03B-GHS-TBT(LF)(SN)(N)", "JST"), "C1": ("CL21A106KPFNNNE", "Samsung"),
    "C3": ("CC0603KRX7R9BB104", "Yageo"), "C4": ("CC0603KRX7R9BB104", "Yageo"), "C5": ("CC0603KRX7R9BB104", "Yageo"),
    "R1": ("RC0603JR-070RL", "Yageo"), "R7": ("RC0603JR-070RL", "Yageo"), "R10": ("RC0603JR-070RL", "Yageo"),
    "R2": ("RC0603FR-07120RL", "Yageo"), "R3": ("RC0603FR-074K7L", "Yageo"), "R4": ("RC0603FR-0747RL", "Yageo"),
    "R5": ("RC0603FR-0710KL", "Yageo"), "R6": ("RC0603FR-0710KL", "Yageo"), "R9": ("RC0603FR-0710KL", "Yageo"),
}


def export():
    """Fab outputs and the board STEP, with PCB-08/14's conventions."""
    import csv
    import shutil
    import subprocess
    import zipfile
    run = lambda *a: subprocess.run([K.CLI, *a, str(BOARD)], check=True, capture_output=True, text=True)
    gerb = FAB / "gerbers"
    shutil.rmtree(gerb, ignore_errors=True)
    gerb.mkdir(parents=True)
    run("pcb", "export", "gerbers", "--layers", LAYERS, "--use-drill-file-origin", "-o", str(gerb) + "/")
    run("pcb", "export", "drill", "--format", "excellon", "--excellon-units", "mm", "--drill-origin", "plot",
        "--excellon-separate-th", "--generate-map", "--map-format", "pdf", "-o", str(gerb) + "/")
    pos = FAB / f"{NAME}-revA-pos.csv"
    run("pcb", "export", "pos", "--side", "both", "--format", "csv", "--units", "mm", "--use-drill-file-origin",
        "--exclude-dnp", "-o", str(pos))
    with open(pos) as f, open(FAB / f"{NAME}-revA-cpl-jlcpcb.csv", "w", newline="") as g:
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
        if "exclude_from_bom" in attr or "dnp" in attr:
            continue
        props = {p[1]: p[2] for p in K.find_all(n, "property")}
        ref = props["Reference"]
        groups.setdefault((props["Value"], n[1], *MPN[ref]), []).append(ref)
    natural = lambda r: (re.match(r"\D+", r).group(0), int(re.search(r"\d+", r).group(0)))
    with open(FAB / f"{NAME}-revA-bom.csv", "w", newline="") as g:
        w = csv.writer(g, quoting=csv.QUOTE_ALL)
        w.writerow(["Comment", "Designator", "Footprint", "Quantity", "MPN", "Manufacturer", "LCSC Part #"])
        for (val, fp, mpn, mfr), refs in sorted(groups.items(), key=lambda kv: natural(sorted(kv[1], key=natural)[0])):
            refs = sorted(refs, key=natural)
            w.writerow([val, ",".join(refs), fp, len(refs), mpn, mfr, ""])
    with zipfile.ZipFile(FAB / f"{NAME}-revA-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(gerb.iterdir()):
            if f.suffix != ".pdf":
                z.write(f, f.name)
    STEP.parent.mkdir(parents=True, exist_ok=True)
    run("pcb", "export", "step", "--subst-models", "--force", "--user-origin", "0x0mm", "-o", str(STEP))
    print("exported", FAB, STEP)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--create", action="store_true")
    p.add_argument("--placement-only", action="store_true")
    p.add_argument("--no-drc", action="store_true")
    p.add_argument("--export", action="store_true")
    args = p.parse_args()
    if args.create or not BOARD.exists():
        create()
    b = K.Board(BOARD)
    setup(b)
    set_origin(b)
    if not args.placement_only:
        route(b)
    b.save()
    pads = {f["ref"]: {p["num"]: p["at"] for p in f["pads"]} for f in b.footprints()}
    (HERE / "placement-readback.json").write_text(json.dumps(pads, indent=1) + "\n")
    if not args.no_drc:
        result = K.drc(BOARD, REPORT, refill=not args.placement_only)
        print("DRC:", {k: v for k, v in result.items() if k != "report"})
        print(K.summary(result["report"], limit=120))
        if args.export and result["violations"] == result["unconnected"] == result["parity"] == 0:
            export()


if __name__ == "__main__":
    main()
