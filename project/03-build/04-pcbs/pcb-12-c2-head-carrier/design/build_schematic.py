"""Author PCB-12's schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-12-c2-head-carrier"
LIB = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/symbols")


class Atom(str):
    pass


def parse(text):
    stack, root = [], None
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text):
        if token == "(":
            node = []
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
        elif token == ")":
            stack.pop()
        else:
            stack[-1].append(json.loads(token) if token.startswith('"') else Atom(token))
    return root


def dump(node):
    if isinstance(node, list):
        return "("+" ".join(map(dump, node))+")"
    return str(node) if isinstance(node, Atom) else json.dumps(node)


def children(node, key):
    return [n for n in node if isinstance(n, list) and n and n[0] == key]


def child(node, key):
    return children(node, key)[0]


def uid(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb12/"+key))


libraries = {}


def symbol(libid):
    lib, name = libid.split(":")
    if lib not in libraries:
        libraries[lib] = parse((LIB/(lib+".kicad_sym")).read_text())
    own = copy.deepcopy(next(n for n in children(libraries[lib], "symbol") if n[1] == name))
    bases = children(own, "extends")
    if bases:
        base = symbol(lib+":"+bases[0][1])
        overrides = [n for n in own[2:] if isinstance(n, list) and n[0] != "extends"]
        own = copy.deepcopy(base)
        own[1] = name
        for override in overrides:
            key = override[:2] if override[0] == "property" else override[:1]
            own = [n for n in own if not (isinstance(n, list) and n[:len(key)] == key)]
            own.append(override)
        for n in children(own, "symbol"):
            n[1] = name+re.search(r"(_\d+_\d+)$", n[1]).group(1)
    return own


rootid = uid("root")
instances, wires, labels, ncs, defs, manifest = [], [], [], [], {}, {}


def add(ref, libid, value, footprint, x, y, nets, bom=True, dnp=False):
    lib = symbol(libid)
    lib[1] = libid
    defs[libid] = lib
    properties = []
    for k, v, dy in [("Reference", ref, -5.08), ("Value", value, -2.54),
                     ("Footprint", footprint, 0), ("Datasheet", "", 0)]:
        tx, ty = x+8, y+dy
        if ref == "J1" and k in ("Reference", "Value"):
            tx, ty = x-12.7, y+(-35.56 if k == "Reference" else -33.02)
        elif ref.startswith("U") and k in ("Reference", "Value"):
            tx, ty = x+12.7, y+(-22.86 if k == "Reference" else -20.32)
        properties.append(f'(property {json.dumps(k)} {json.dumps(v)} (at {tx} {ty} 0) '
                          f'(effects (font (size 1.0 1.0)) (justify left)'+(' (hide yes)' if k in ("Footprint", "Datasheet") else '')+'))')
    pinids = []
    pinmap = {}
    for unit in children(lib, "symbol"):
        for pin in children(unit, "pin"):
            number = child(pin, "number")[1]
            px, py, a = map(float, child(pin, "at")[1:4])
            px, py = round(x+px, 4), round(y-py, 4)
            net = nets.get(number)
            pinmap[number] = net
            pinids.append(f'(pin "{number}" (uuid "{uid(ref+"/pin/"+number)}"))')
            if net is None:
                ncs.append(f'(no_connect (at {px} {py}) (uuid "{uid(ref+"/nc/"+number)}"))')
                continue
            dx, dy = {0: (-5.08, 0), 180: (5.08, 0), 90: (0, 5.08), 270: (0, -5.08)}[int(a)]
            ex, ey = round(px+dx, 4), round(py+dy, 4)
            wires.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid "{uid(ref+"/wire/"+number)}"))')
            justify = "right" if dx < 0 else "left"
            labels.append(f'(label "{net}" (at {ex} {ey} 0) (effects (font (size 1 1)) (justify {justify} bottom)) (uuid "{uid(ref+"/label/"+number)}"))')
    instances.append(f'(symbol (lib_id "{libid}") (at {x} {y} 0) (unit 1) '
                     f'(in_bom {"yes" if bom else "no"}) (on_board yes) (dnp {"yes" if dnp else "no"}) '
                     f'(uuid "{uid(ref)}") '+" ".join(properties+pinids)+
                     f' (instances (project "{NAME}" (path "/{rootid}" (reference "{ref}") (unit 1)))))')
    manifest[ref] = {"value": value, "symbol": libid, "footprint": footprint, "pins": pinmap, "dnp": dnp}


if __name__ == "__main__":
    # D-093/D-100/D-102: C2 carrier. The ESP32-S3-Zero solders by its 18 edge
    # castellations; only pads whose position all pinout sources agree on are
    # used (5V, GND, 3V3, GPIO1/2/4/5/6 left row; GPIO7/8/9 right row).
    # Head link (RS-422, THVD1451 as PCB-09), servo bus (one-wire half duplex,
    # LVC1G126 TX / LVC1G125 RX buffers, one 10k pull-up to 3V3), display
    # (half-duplex RS-485, THVD1450). All head grounds join GND here through
    # 0 R links (D-100), so a ferrite or resistor can replace any one at bench.
    RFP, CFP = "Resistor_SMD:R_0603_1608Metric", "Capacitor_SMD:C_0603_1608Metric"
    zero = {"1": "+5V_C2", "2": "GND", "3": "+3V3", "4": "DISP_DE", "5": "DISP_RX", "7": "DISP_TX",
            "8": "LINK_TX", "9": "LINK_RX", "10": "SERVO_TX", "11": "SERVO_RX", "12": "SERVO_DIR"}
    add("U1", "Connector_Generic:Conn_01x18", "ESP32-S3-Zero", "pcb12:Waveshare_ESP32-S3-Zero_Castellated",
        55.88, 88.9, zero)
    add("J1", "Connector_Generic:Conn_01x07", "HEAD_LINK_C2_POWER",
        "Connector_JST:JST_GH_BM07B-GHS-TBT_1x07-1MP_P1.25mm_Vertical", 55.88, 160.02,
        {"1": "GND_SIG", "2": "C0TX_P", "3": "C0TX_N", "4": "C2TX_N", "5": "C2TX_P", "6": "+5V_C2", "7": "GND"})
    add("C1", "Device:C", "10u_10V", "Capacitor_SMD:C_0805_2012Metric", 25.4, 200.66, {"1": "+5V_C2", "2": "GND"})
    add("C2", "Device:C", "100n", CFP, 45.72, 200.66, {"1": "+5V_C2", "2": "GND"})
    add("R1", "Device:R", "0R", RFP, 76.2, 200.66, {"1": "GND_SIG", "2": "GND"})
    # Head link: receive C0TX (terminated here, as PCB-09 terminates C2TX), drive C2TX.
    add("U2", "Interface_UART:THVD1451D", "THVD1451DR", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 152.4, 76.2,
        {"1": "+3V3", "2": "LINK_RX", "3": "LINK_TX", "4": "GND", "5": "C2TX_P", "6": "C2TX_N", "7": "C0TX_N", "8": "C0TX_P"})
    add("R2", "Device:R", "120", RFP, 198.12, 101.6, {"1": "C0TX_P", "2": "C0TX_N"})
    add("R3", "Device:R", "4.7k", RFP, 114.3, 76.2, {"1": "+3V3", "2": "LINK_TX"})
    add("C3", "Device:C", "100n", CFP, 152.4, 116.84, {"1": "+3V3", "2": "GND"})
    # Servo bus: SERVO_DIR high transmits (U3 enabled), low receives (U4 enabled).
    add("U3", "74xGxx:74LVC1G126", "SN74LVC1G126DBVR", "Package_TO_SOT_SMD:SOT-23-5", 152.4, 162.56,
        {"1": "SERVO_DIR", "2": "SERVO_TX", "3": "GND", "4": "SERVO_DRV", "5": "+3V3"})
    add("U4", "74xGxx:74LVC1G125", "SN74LVC1G125DBVR", "Package_TO_SOT_SMD:SOT-23-5", 152.4, 203.2,
        {"1": "SERVO_DIR", "2": "SERVO_DATA", "3": "GND", "4": "SERVO_RX", "5": "+3V3"})
    add("R4", "Device:R", "47", RFP, 190.5, 162.56, {"1": "SERVO_DRV", "2": "SERVO_DATA"})
    add("R5", "Device:R", "10k", RFP, 213.36, 147.32, {"1": "+3V3", "2": "SERVO_DATA"})
    add("R6", "Device:R", "10k", RFP, 114.3, 182.88, {"1": "SERVO_DIR", "2": "GND"})
    add("C4", "Device:C", "100n", CFP, 190.5, 203.2, {"1": "+3V3", "2": "GND"})
    add("J2", "Connector_Generic:Conn_01x02", "SERVO_BUS",
        "Connector_JST:JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical", 251.46, 162.56,
        {"1": "GND_HEAD_REF", "2": "SERVO_DATA"})
    add("R7", "Device:R", "0R", RFP, 251.46, 190.5, {"1": "GND_HEAD_REF", "2": "GND"})
    # Display: D1's own half-duplex RS-485 port (RP-02 C2 relay); DE/RE together, low = receive.
    # Symbol: LTC2850xS8, the root of the THVD1450D -> MAX481E -> LTC2850xS8 chain
    # (same RO/~RE/DE/DI/GND/A/B/VCC pinout); the nested derived copy fails ERC's library match.
    add("U5", "Interface_UART:LTC2850xS8", "THVD1450DR", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", 279.4, 76.2,
        {"1": "DISP_RX", "2": "DISP_DE", "3": "DISP_DE", "4": "DISP_TX", "5": "GND", "6": "DISP_A", "7": "DISP_B", "8": "+3V3"})
    add("R8", "Device:R", "120", RFP, 325.12, 101.6, {"1": "DISP_A", "2": "DISP_B"}, dnp=True)
    add("R9", "Device:R", "10k", RFP, 241.3, 106.68, {"1": "DISP_DE", "2": "GND"})
    add("C5", "Device:C", "100n", CFP, 279.4, 116.84, {"1": "+3V3", "2": "GND"})
    add("J3", "Connector_Generic:Conn_01x03", "DISPLAY_RS485",
        "Connector_JST:JST_GH_BM03B-GHS-TBT_1x03-1MP_P1.25mm_Vertical", 363.22, 76.2,
        {"1": "GND_DISPLAY", "2": "DISP_A", "3": "DISP_B"})
    add("R10", "Device:R", "0R", RFP, 363.22, 106.68, {"1": "GND_DISPLAY", "2": "GND"})
    for n, net in enumerate(["SERVO_DATA", "GND"], 1):
        add(f"TP{n}", "Connector:TestPoint", net, "TestPoint:TestPoint_Pad_D1.0mm", 320.04 + 20.32 * (n - 1), 180.34, {"1": net}, False)
    for n, net in enumerate(["+5V_C2", "+3V3", "GND", "GND_SIG", "GND_HEAD_REF", "GND_DISPLAY"], 1):
        add(f"#FLG0{n}", "power:PWR_FLAG", "PWR_FLAG", "", 40.64 + 25.4 * (n - 1), 236.22, {"1": net}, False)
    top = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A3") '
    top += '(title_block (title "PCB-12 C2 head carrier") (date "2026-11-10") (rev "A") (company "Makad") (comment 1 "D-093 / D-100 / D-102: signals only; all head grounds join here"))'
    text = top + ' (lib_symbols ' + " ".join(dump(n) for n in defs.values()) + ') '
    text += " ".join(instances + wires + labels + ncs)
    for title, x, y in [("C2: ESP32-S3-Zero (castellated; agreed pads only)", 30.48, 45.72),
                        ("HEAD LINK J9-1 ORDER + C2 POWER (W43/W42 via head junction)", 30.48, 142.24),
                        ("RS-422: RX C0TX (120R here), TX C2TX", 127, 45.72),
                        ("SERVO BUS: DIR high = TX, one 10k pull-up to 3V3, no 12 V pull-up", 127, 142.24),
                        ("DISPLAY: half-duplex RS-485 to D1, 115200; R8 DNP", 254, 45.72),
                        ("GROUND BONDS (D-100): 0R links, ferrite fallback", 30.48, 220.98)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += ' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE / (NAME + ".kicad_sch")).write_text(text)
    (HERE / "circuit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
