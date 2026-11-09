"""Author PCB-14's schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-14-yaw-rotor-joiner"
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
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb14/"+key))


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
    # D-052/D-101: passive straight-through joiner. J1 (lower, mouth down)
    # takes the cassette FFC, J2 (upper, mouth up) the head FFC. Both sit on
    # the +Y face, so J2 is J1 turned 180 deg: the conductor at J1 contact n
    # lies straight above J2 contact 23-n. Nets are named by cassette
    # conductor (FFC01 = conductor 1, at -X), one design for W42/W43/CSI.
    zif = "fh34:Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
    net = lambda n: f"FFC{n:02d}"
    add("J1", "Connector_Generic:Conn_01x22", "LOWER_CASSETTE_FFC", zif, 76.2, 76.2,
        {str(n): net(n) for n in range(1, 23)})
    add("J2", "Connector_Generic:Conn_01x22", "UPPER_HEAD_FFC", zif, 177.8, 76.2,
        {str(m): net(23 - m) for m in range(1, 23)})
    top = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A4") '
    top += '(title_block (title "PCB-14 yaw rotor joiner (x3)") (date "2026-11-10") (rev "A") (company "Makad") (comment 1 "D-052 / D-101: straight-through, J1 n -> J2 23-n; FFC01 = cassette conductor 1 at -X"))'
    text = top+' (lib_symbols '+" ".join(dump(n) for n in defs.values())+') '
    text += " ".join(instances+wires+labels+ncs)
    for title, x, y in [("LOWER ZIF: CASSETTE FFC (mouth down, contact 1 at -X)", 50.8, 30.48),
                        ("UPPER ZIF: HEAD FFC (mouth up, contact 22 at -X)", 152.4, 30.48),
                        ("STRAIGHT-THROUGH: J1 n -> J2 23-n (one conductor, one X)", 50.8, 147.32),
                        ("0.5 A PER LANE (FH34SRJ rating); W42 power, W43 signal and CSI use this board", 50.8, 152.4)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += ' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE/(NAME+".kicad_sch")).write_text(text)
    (HERE/"circuit-manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
