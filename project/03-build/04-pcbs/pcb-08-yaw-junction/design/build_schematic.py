"""Author PCB-08's schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-08-yaw-junction"
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
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb08/"+key))


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
    # D-093/D-100: passive stator junction. Head power pairs J8-1 -> J8-6,
    # RS-422 J8-4 -> J8-7, SERVO_DATA J8-7 -> J8-8, yaw rail W17 -> J8-8.
    # GND_SIG joins the C0 link GND (through R1), the J8-7 references and the
    # yaw servo ground; the three power returns stay separate (D-100 amendment).
    head, c2, disp = "+6V0_HEAD_PR", "+5V_C2", "+5V_DISPLAY"
    add("J1", "Connector_Generic:Conn_02x03_Top_Bottom", "J8-1_HEAD_POWER_MF3",
        "pcb08:Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal", 55.88, 76.2,
        {"1": head, "2": c2, "3": disp, "4": "GND_HEAD", "5": "GND_C2", "6": "GND_DISPLAY"})
    add("J2", "Connector_Generic:Conn_01x06", "J8-4_HEAD_LINK_W24",
        "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical", 55.88, 137.16,
        {"1": "LINK_GND", "2": "C0TX_P", "3": "C0TX_N", "4": "C2TX_N", "5": "C2TX_P"})
    add("R1", "Device:R", "0R", "Resistor_SMD:R_0805_2012Metric", 96.52, 167.64,
        {"1": "LINK_GND", "2": "GND_SIG"})
    zif = "fh34:Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
    power_map = {str(n): head for n in range(1, 8)}
    power_map.update({str(n): "GND_HEAD" for n in range(8, 15)})
    power_map.update({"15": c2, "16": c2, "17": "GND_C2", "18": "GND_C2",
                      "19": disp, "20": disp, "21": "GND_DISPLAY", "22": "GND_DISPLAY"})
    add("J3", "Connector_Generic:Conn_01x22", "J8-6_W42_POWER_FFC", zif, 190.5, 76.2, power_map)
    add("J4", "Connector_Generic:Conn_01x22", "J8-7_W43_SIGNAL_FFC", zif, 279.4, 76.2,
        {"1": "GND_SIG", "2": "C0TX_P", "3": "C0TX_N", "4": "GND_SIG", "5": "C2TX_N",
         "6": "C2TX_P", "7": "GND_SIG", "8": "SERVO_DATA", "9": "GND_SIG"})
    add("J5", "Connector_Generic:Conn_01x03", "J8-8_YAW_SERVO_5267",
        "Connector_Molex:Molex_SPOX_5267-03A_1x03_P2.50mm_Vertical", 368.3, 76.2,
        {"1": "GND_SIG", "2": "+11V1_YAW", "3": "SERVO_DATA"})
    add("J6", "Connector_Generic:Conn_01x02", "W17_YAW_RAIL_PADS",
        "Connector_Wire:SolderWire-0.5sqmm_1x02_P4.6mm_D0.9mm_OD2.1mm", 368.3, 121.92,
        {"1": "+11V1_YAW", "2": "GND_SIG"}, False)
    for n, net in enumerate(["SERVO_DATA", "GND_SIG"], 1):
        add(f"TP{n}", "Connector:TestPoint", net, "TestPoint:TestPoint_Pad_D1.0mm",
            355.6+25.4*(n-1), 167.64, {"1": net}, False)
    for n, net in enumerate([head, c2, disp, "GND_HEAD", "GND_C2", "GND_DISPLAY", "+11V1_YAW", "GND_SIG"], 1):
        add(f"#FLG0{n}", "power:PWR_FLAG", "PWR_FLAG", "", 40.64+25.4*(n-1), 218.44, {"1": net}, False)
    top = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A3") '
    top += '(title_block (title "PCB-08 yaw junction") (date "2026-11-09") (rev "A") (company "Makad") (comment 1 "D-093 / D-100: 6.0 V head 7+7; J8-7 signal-only; GND_SIG"))'
    text = top+' (lib_symbols '+" ".join(dump(n) for n in defs.values())+') '
    text += " ".join(instances+wires+labels+ncs)
    for title, x, y in [("HEAD POWER IN / W13 + W14", 30.48, 30.48), ("HEAD LINK / W24 (D-092 order)", 30.48, 121.92),
                        ("LINK GND -> GND_SIG: 0R, ferrite fallback", 76.2, 157.48),
                        ("W42 POWER FFC: 7+7 HEAD, 2+2 C2, 2+2 DISPLAY", 165.1, 30.48),
                        ("W43 SIGNAL FFC: NO POWER, 10-22 ISOLATED", 254, 30.48),
                        ("YAW SERVO / W15 + W17 RAIL", 342.9, 45.72), ("BENCH PADS", 342.9, 157.48)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += ' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE/(NAME+".kicad_sch")).write_text(text)
    (HERE/"circuit-manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
