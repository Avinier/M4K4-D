"""Author PCB-17's schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-17-balance-fuse-cards"
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
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb17/"+key))


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
    # D-116: CH-103 balance-tap fuses. Card A (BM) sits at the HW-391's +Y end,
    # card B (B-, B+) at its -Y end. Each fuse joins a cell-side wire pad to a
    # protected wire pad; nothing else is on either card.
    fuse, pad = "Fuse:Fuse_1206_3216Metric", "pcb17:WirePad_1x01_2.5x1.5mm"
    col = 0
    for tap, f, jc, jo in (("BM", "F1", "J1", "J2"), ("BMINUS", "F2", "J3", "J4"), ("BPLUS", "F3", "J5", "J6")):
        x = 50.8 + 76.2 * col
        add(jc, "Connector_Generic:Conn_01x01", f"{tap}_CELL_PAD", pad, x, 76.2, {"1": f"{tap}_CELL"}, False)
        add(f, "Device:Fuse", "0466001.NRHF 1A", fuse, x + 25.4, 76.2, {"1": f"{tap}_CELL", "2": f"{tap}_FUSED"})
        add(jo, "Connector_Generic:Conn_01x01", f"{tap}_FUSED_PAD", pad, x + 50.8, 76.2, {"1": f"{tap}_FUSED"}, False)
        col += 1
    for n, net in enumerate(["BM_CELL", "BMINUS_CELL", "BPLUS_CELL"], 1):
        add(f"#FLG0{n}", "power:PWR_FLAG", "PWR_FLAG", "", 50.8 + 76.2 * (n - 1), 127.0, {"1": net}, False)
    top = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A3") '
    top += '(title_block (title "PCB-17 balance-tap fuse cards") (date "2026-11-18") (rev "A") (company "Makad") (comment 1 "D-116: card A = F1 (BM), card B = F2 (B-), F3 (B+); 1 A very-fast per tap"))'
    text = top + ' (lib_symbols ' + " ".join(dump(n) for n in defs.values()) + ') '
    text += " ".join(instances + wires + labels + ncs)
    for title, x, y in [("CARD A: BM tap (HW-391 4.2V pad end)", 25.4, 30.48),
                        ("CARD B: B- and B+ taps (HW-391 0V / 8.4V pad end)", 101.6, 30.48),
                        ("Taps bypass PCB-01 and the 15 A fuse: these fuses are their only short protection (D-111)", 25.4, 165.1)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += ' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE / (NAME + ".kicad_sch")).write_text(text)
    (HERE / "circuit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
