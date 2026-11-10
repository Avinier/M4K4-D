"""Author PCB-16's schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-16-head-junction"
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
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb16/"+key))


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
    # D-103: passive head junction on the yaw disc. W42 (power) and W43 (signal)
    # head FFCs arrive with conductor 1 at -X; the ZIFs' contact 1 is at +X, so
    # contact m carries conductor 23-m (named by conductor, as PCB-08's J8-6/J8-7).
    zif = "fh34:Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
    head, c2, disp = "+6V3_HEAD_PR", "+5V_C2", "+5V_DISPLAY"
    w42 = {**{n: head for n in range(1, 8)}, **{n: "GND_HEAD" for n in range(8, 15)},
           15: c2, 16: c2, 17: "GND_C2", 18: "GND_C2", 19: disp, 20: disp, 21: "GND_DISPLAY", 22: "GND_DISPLAY"}
    w43 = {1: "GND_SIG", 2: "C0TX_P", 3: "C0TX_N", 4: "GND_SIG", 5: "C2TX_N", 6: "C2TX_P", 7: "GND_SIG",
           8: "SERVO_DATA", 9: "GND_SIG"}
    # Near ZIF J1 takes the lower FFC in the channel, W43 (signal); far ZIF J2 the upper, W42 (power).
    add("J1", "Connector_Generic:Conn_01x22", "W43_HEAD_SIGNAL_FFC", zif, 50.8, 76.2,
        {str(23 - n): net for n, net in w43.items()})
    add("J2", "Connector_Generic:Conn_01x22", "W42_HEAD_POWER_FFC", zif, 127.0, 76.2,
        {str(23 - n): net for n, net in w42.items()})
    pads = "pcb16:"
    # Wire pads sit where their nets are. PCB-12 J1 lead: wires 1-5 -> J4 1-5, wires 6-7 -> J5.
    # PCB-12 J2 lead: GND_HEAD -> J3 pad 2 (shared with the servo AWG20), SERVO_DATA -> J4 pad 6.
    # Servo bundle: +6V3 -> J3 pad 1, GND_HEAD -> J3 pad 2, SERVO_DATA -> J4 pad 7.
    add("J3", "Connector_Generic:Conn_01x02", "HEAD_POWER_PADS", pads + "WirePads_Power_1x02_P3.5mm", 203.2, 60.96,
        {"1": head, "2": "GND_HEAD"}, False)
    add("J4", "Connector_Generic:Conn_01x07", "SIGNAL_PADS", pads + "WirePads_1x07_P1.5mm", 203.2, 101.6,
        {"1": "GND_SIG", "2": "C0TX_P", "3": "C0TX_N", "4": "C2TX_N", "5": "C2TX_P", "6": "SERVO_DATA", "7": "SERVO_DATA"}, False)
    add("J5", "Connector_Generic:Conn_01x02", "C2_POWER_PADS", pads + "WirePads_1x02_P1.5mm", 203.2, 142.24,
        {"1": c2, "2": "GND_C2"}, False)
    add("J6", "Connector_Generic:Conn_01x02", "DISPLAY_POWER_PADS", pads + "WirePads_1x02_P1.5mm", 254.0, 60.96,
        {"1": disp, "2": "GND_DISPLAY"}, False)
    for n, net in enumerate([head, "GND_HEAD", c2, "GND_C2", disp, "GND_DISPLAY", "GND_SIG"], 1):
        add(f"#FLG0{n}", "power:PWR_FLAG", "PWR_FLAG", "", 40.64 + 25.4 * (n - 1), 180.34, {"1": net}, False)
    top = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A3") '
    top += '(title_block (title "PCB-16 head junction") (date "2026-11-10") (rev "A") (company "Makad") (comment 1 "D-103: yaw-disc FFC-to-wire break; contact m = conductor 23-m"))'
    text = top + ' (lib_symbols ' + " ".join(dump(n) for n in defs.values()) + ') '
    text += " ".join(instances + wires + labels + ncs)
    for title, x, y in [("W42 POWER FFC (contact m = conductor 23-m)", 25.4, 30.48),
                        ("W43 SIGNAL FFC (contact m = conductor 23-m; conductors 10-22 isolated)", 101.6, 30.48),
                        ("WIRE PADS: servo bundle, PCB-12 J1/J2 leads, display power (bare copper)", 177.8, 30.48),
                        ("GROUNDS STAY SEPARATE HERE; PCB-12 BONDS THEM (D-100)", 25.4, 165.1)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += ' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE / (NAME + ".kicad_sch")).write_text(text)
    (HERE / "circuit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
