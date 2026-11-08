"""Headless .kicad_pcb editing for the KiCad 10.99 Nightly file format (D-092).

The file-based counterpart of kp.py, for a board that cannot be open in the
Nightly GUI (another session has the GUI). It reads footprints and pads, moves
footprints, and adds or replaces tracks, vias, zones and outline segments.
Nothing is autorouted: callers give every track's coordinates. Then
`drc()` runs the Nightly kicad-cli with --refill-zones --save-board and
--schematic-parity, which also rewrites the file in KiCad's own form.

Items this module writes get UUIDs in the "0909c0de-" namespace, derived from
a caller-chosen name, so a script can rerun: `drop_generated()` removes them
all first. Everything else in the file is kept verbatim.

Coordinates are KiCad board millimetres (y down).
"""

import json
import math
import re
import subprocess
import uuid
from pathlib import Path

CLI = "/Applications/KiCad-nightly/KiCad.app/Contents/MacOS/kicad-cli"
GEN = "0909c0de"
_NS = uuid.UUID("0909c0de-0000-4000-8000-000000000000")


def gen_uuid(name):
    u = str(uuid.uuid5(_NS, name))
    return GEN + u[8:]


# ---------------------------------------------------------------- s-expressions

_TOKEN = re.compile(r'\s*(?:(\()|(\))|("(?:[^"\\]|\\.)*")|([^\s()"]+))')


def parse(text):
    """Nested lists of atoms (quoted strings keep no quotes)."""
    stack, cur, pos = [], [], 0
    while True:
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            break
        pos = m.end()
        if m.group(1):
            stack.append(cur)
            cur = []
        elif m.group(2):
            done, cur = cur, stack.pop()
            cur.append(done)
        elif m.group(3):
            cur.append(m.group(3)[1:-1].replace('\\"', '"'))
        else:
            cur.append(m.group(4))
    return cur[0] if len(cur) == 1 else cur


def find(node, key):
    return next((c for c in node if isinstance(c, list) and c and c[0] == key), None)


def find_all(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def _blocks(text):
    """Top-level items of (kicad_pcb ...): list of [start, end) spans, by balanced parentheses."""
    spans, depth, start, quoted, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if quoted:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
            if depth == 2:
                start = i
        elif ch == ")":
            if depth == 2:
                spans.append((start, i + 1))
            depth -= 1
    return spans


# ---------------------------------------------------------------- board

class Board:
    def __init__(self, path):
        self.path = Path(path)
        self.reload()

    def reload(self):
        self.text = self.path.read_text()
        self._index()

    def _index(self):
        self.items = []  # (kind, start, end)
        for s, e in _blocks(self.text):
            kind = re.match(r"\((\S+)", self.text[s:e]).group(1)
            self.items.append((kind, s, e))

    def blocks(self, kind=None):
        return [self.text[s:e] for k, s, e in self.items if kind is None or k == kind]

    # -- footprints
    def footprints(self):
        out = []
        for raw in self.blocks("footprint"):
            node = parse(raw)
            ref = next(p[2] for p in find_all(node, "property") if p[1] == "Reference")
            tr = find(node, "transform")
            x, y = map(float, find(tr, "translate")[1:3])
            rot = float(find(tr, "rotate")[1]) if find(tr, "rotate") else 0.0
            layer = find(node, "layer")[1]
            attr = find(node, "attr")
            pads = []
            for p in find_all(node, "pad"):
                at = find(p, "at")
                px, py = float(at[1]), float(at[2])
                prot = float(at[3]) if len(at) > 3 else 0.0
                net = find(p, "net")
                size = tuple(map(float, find(p, "size")[1:3]))
                drill = find(p, "drill")
                a = math.radians(rot)
                ax = x + px * math.cos(a) + py * math.sin(a)
                ay = y - px * math.sin(a) + py * math.cos(a)
                pads.append(dict(num=p[1], kind=p[2], shape=p[3], net=net[1] if net else None,
                                 at=(round(ax, 6), round(ay, 6)), size=size, rot=(rot + prot) % 360,
                                 layers=find(p, "layers")[1:], drill=float(drill[1]) if drill and len(drill) > 1 and drill[1] != "oval" else None))
            out.append(dict(ref=ref, lib=node[1], layer=layer, at=(x, y), rot=rot,
                            attr=attr[1:] if attr else [], pads=pads))
        return out

    def fp(self, ref):
        return next(f for f in self.footprints() if f["ref"] == ref)

    def pad(self, ref, num):
        return next(p for p in self.fp(ref)["pads"] if p["num"] == str(num))

    def nets(self):
        out = {}
        for f in self.footprints():
            for p in f["pads"]:
                if p["net"]:
                    out.setdefault(p["net"], []).append((f["ref"], p["num"], p["at"], f["layer"], p["kind"]))
        return out

    def move(self, ref, x, y, rot=None):
        """Set a footprint's translate (and rotate); keeps its side and pads."""
        for k, s, e in self.items:
            if k != "footprint":
                continue
            raw = self.text[s:e]
            if not re.search(r'\(property "Reference" "%s"' % re.escape(ref), raw):
                continue
            new = re.sub(r"\(translate [-\d.]+ [-\d.]+\)", f"(translate {x:.4f} {y:.4f})", raw, count=1)
            if rot is not None:
                old = float(re.search(r"\(rotate ([-\d.]+)\)", raw).group(1))
                new = re.sub(r"\(rotate [-\d.]+\)", f"(rotate {rot:g})", new, count=1)
                delta = rot - old
                if abs(delta) > 1e-9:
                    # Pad and text angles in this format are absolute: turn them with the footprint.
                    def turn(m):
                        a = (float(m.group(3) or 0.0) + delta) % 360.0
                        a = 0.0 if abs(a) < 1e-9 or abs(a - 360) < 1e-9 else a
                        return f"{m.group(1)}(at {m.group(2)} {a:g})"
                    new = re.sub(r"(\(pad [^\n]*\n\t+)\(at ([-\d.]+ [-\d.]+)(?: ([-\d.]+))?\)", turn, new)
            self.text = self.text[:s] + new + self.text[e:]
            self._index()
            return
        raise KeyError(ref)

    # -- generated items
    def drop(self, pred):
        keep, pos, out = 0, 0, []
        for k, s, e in self.items:
            if pred(k, self.text[s:e]):
                # remove the item and its leading whitespace
                ws = s
                while ws > 0 and self.text[ws - 1] in " \t\n":
                    ws -= 1
                out.append(self.text[pos:ws])
                pos = e
            else:
                keep += 1
        out.append(self.text[pos:])
        self.text = "".join(out)
        self._index()

    def drop_generated(self):
        """Remove every item this module wrote (its own UUID namespace)."""
        self.drop(lambda k, raw: f'(uuid "{GEN}' in raw)

    def add(self, *raws):
        end = self.text.rstrip().rfind(")")
        self.text = self.text[:end].rstrip("\n") + "\n" + "\n".join(raws) + "\n" + self.text[end:]
        self._index()

    def save(self):
        self.path.write_text(self.text)

    def set_pad_nets(self, ref, nets):
        """Update transferred pads when the schematic adds nets to an existing part."""
        for kind, start, end in self.items:
            raw = self.text[start:end]
            if kind == "footprint" and re.search(r'\(property "Reference" "%s"' % re.escape(ref), raw):
                break
        else:
            raise KeyError(ref)

        def update(match):
            pad = match.group(0)
            number = re.match(r'\t\t\(pad "([^"]+)"', pad).group(1)
            if number not in nets:
                return pad
            net = nets[number]
            if re.search(r'\(net "[^"]*"\)', pad):
                pad = re.sub(r'\(net "[^"]*"\)', f'(net "{net}")', pad, count=1)
                if not net.startswith("unconnected-"):
                    pad = pad.replace("passive+no_connect", "passive")
                return pad
            return pad.replace("\n\t\t)", f'\n\t\t\t(net "{net}")\n\t\t)', 1)

        new = re.sub(r'\t\t\(pad .*?\n\t\t\)', update, raw, flags=re.S)
        self.text = self.text[:start] + new + self.text[end:]
        self._index()

    def clone_footprint(self, source_ref, ref, value, symbol_uuid, nets, dnp=False):
        """Clone a same-footprint, same-side part with fresh generated UUIDs."""
        raw = next((raw for raw in self.blocks("footprint")
                    if re.search(r'\(property "Reference" "%s"' % re.escape(source_ref), raw)), None)
        if raw is None:
            raise KeyError(source_ref)
        raw = raw.replace(f'(property "Reference" "{source_ref}"',
                          f'(property "Reference" "{ref}"', 1)
        raw = re.sub(r'\(property "Value" "[^"]*"',
                     f'(property "Value" "{value}"', raw, count=1)
        raw = re.sub(r'\(path "/[^"]+"\)', f'(path "/{symbol_uuid}")', raw, count=1)
        ids = iter(range(10000))
        raw = re.sub(r'\(uuid "[^"]+"\)',
                     lambda m: f'(uuid "{gen_uuid(ref + "/" + str(next(ids)))}")', raw)
        if dnp:
            raw = raw.replace('(attr smd)', '(attr smd dnp)', 1)
        self.add(raw)
        self.set_pad_nets(ref, nets)


# ---------------------------------------------------------------- item text

def _f(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def segment(name, a, b, width, layer, net):
    return (f'\t(segment\n\t\t(start {_f(a[0])} {_f(a[1])})\n\t\t(end {_f(b[0])} {_f(b[1])})\n'
            f'\t\t(width {_f(width)})\n\t\t(layer "{layer}")\n\t\t(net "{net}")\n'
            f'\t\t(uuid "{gen_uuid(name)}")\n\t)')


def track(name, points, width, layer, net):
    """A polyline of segments; every leg must be octolinear (0/45/90 deg)."""
    out = []
    for i, (a, b) in enumerate(zip(points, points[1:])):
        dx, dy = b[0] - a[0], b[1] - a[1]
        assert abs(dx) < 1e-6 or abs(dy) < 1e-6 or abs(abs(dx) - abs(dy)) < 1e-6, (name, i, a, b)
        out.append(segment(f"{name}#{i}", a, b, width, layer, net))
    return out


def via(name, at, net, size=0.67, drill=0.35):
    return (f'\t(via\n\t\t(at {_f(at[0])} {_f(at[1])})\n\t\t(size {_f(size)})\n\t\t(drill {_f(drill)})\n'
            f'\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "{net}")\n\t\t(uuid "{gen_uuid(name)}")\n\t)')


def edge_line(name, a, b, width=0.1):
    return (f'\t(gr_line\n\t\t(start {_f(a[0])} {_f(a[1])})\n\t\t(end {_f(b[0])} {_f(b[1])})\n'
            f'\t\t(stroke\n\t\t\t(width {_f(width)})\n\t\t\t(type default)\n\t\t)\n\t\t(layer "Edge.Cuts")\n'
            f'\t\t(uuid "{gen_uuid(name)}")\n\t)')


def _pts(points):
    return "\n".join(f"\t\t\t\t(xy {_f(x)} {_f(y)})" for x, y in points)


def pour(name, layer, net, points, clearance=0.2, min_width=0.2, priority=0, thermal=(0.3, 0.3), solid=False):
    connect = "\t\t(connect_pads yes\n" if solid else "\t\t(connect_pads\n"
    return (f'\t(zone\n\t\t(net "{net}")\n\t\t(layer "{layer}")\n\t\t(uuid "{gen_uuid(name)}")\n'
            f'\t\t(name "{name}")\n\t\t(hatch edge 0.5)\n' + (f"\t\t(priority {priority})\n" if priority else "") +
            connect + f"\t\t\t(clearance {_f(clearance)})\n\t\t)\n\t\t(min_thickness {_f(min_width)})\n"
            f"\t\t(filled_areas_thickness no)\n\t\t(fill yes\n\t\t\t(thermal_gap {_f(thermal[0])})\n"
            f"\t\t\t(thermal_bridge_width {_f(thermal[1])})\n\t\t\t(island_removal_mode 0)\n"
            f"\t\t)\n\t\t(polygon\n\t\t\t(pts\n{_pts(points)}\n\t\t\t)\n\t\t)\n\t)")


def keepout(name, layers, points, tracks=False, vias=False, pads=False, pour_ok=False, footprints=True):
    allow = lambda ok: "allowed" if ok else "not_allowed"
    lay = " ".join(f'"{l}"' for l in layers)
    return (f'\t(zone\n\t\t(layers {lay})\n\t\t(uuid "{gen_uuid(name)}")\n\t\t(name "{name}")\n'
            f"\t\t(hatch edge 0.5)\n\t\t(connect_pads\n\t\t\t(clearance 0)\n\t\t)\n\t\t(min_thickness 0.25)\n"
            f"\t\t(keepout\n\t\t\t(tracks {allow(tracks)})\n\t\t\t(vias {allow(vias)})\n\t\t\t(pads {allow(pads)})\n"
            f"\t\t\t(copperpour {allow(pour_ok)})\n\t\t\t(footprints {allow(footprints)})\n\t\t)\n"
            f'\t\t(placement\n\t\t\t(enabled no)\n\t\t\t(sheetname "")\n\t\t)\n'
            f"\t\t(fill\n\t\t\t(thermal_gap 0.5)\n\t\t\t(thermal_bridge_width 0.5)\n\t\t\t(island_removal_mode 0)\n\t\t)\n"
            f"\t\t(polygon\n\t\t\t(pts\n{_pts(points)}\n\t\t\t)\n\t\t)\n\t)")


def circle_pts(cx, cy, r, n=24):
    return [(round(cx + r * math.cos(2 * math.pi * k / n), 4), round(cy + r * math.sin(2 * math.pi * k / n), 4)) for k in range(n)]


# ---------------------------------------------------------------- checks

def drc(path, out_json, refill=True):
    """Nightly DRC with schematic parity; refills zones and saves the board when refill is set."""
    cmd = [CLI, "pcb", "drc", "--schematic-parity", "--severity-all", "--format", "json", "--units", "mm",
           "-o", str(out_json)]
    if refill:
        cmd += ["--refill-zones", "--save-board"]
    subprocess.run(cmd + [str(path)], check=True, capture_output=True, text=True)
    report = json.loads(Path(out_json).read_text())
    count = lambda key: len(report.get(key, []))
    return dict(violations=count("violations"), unconnected=count("unconnected_items"),
                parity=count("schematic_parity"), report=report)


def summary(report, limit=40):
    lines = []
    for key in ("violations", "unconnected_items", "schematic_parity"):
        for v in report.get(key, [])[:limit]:
            items = "; ".join(f"{i.get('description', '')} @({i['pos']['x']:.3f},{i['pos']['y']:.3f})" for i in v.get("items", []))
            lines.append(f"{key[:5]} {v.get('severity', '')[:4]} {v.get('type')}: {items}")
    return "\n".join(lines)


# ---------------------------------------------------------------- footprint swap

def replace_footprint(b, ref, lib_dir, name, side=None):
    """Swap ref's footprint for the library's `name`, keeping uuid, schematic path,
    Reference/Value text, position and each pad's net/pinfunction/pintype by pad number.

    side=None keeps a top-side part on top. side="F" also moves a bottom-side part to the
    top: the library land pattern is a top-side one, so it is used as it is (no mirroring)."""
    for k, s, e in b.items:
        raw = b.text[s:e]
        if k == "footprint" and re.search(r'\(property "Reference" "%s"' % re.escape(ref), raw):
            break
    else:
        raise KeyError(ref)
    node = parse(raw)
    old_pads = {p[1]: p for p in find_all(node, "pad")}
    lib = (Path(lib_dir) / f"{name}.kicad_mod").read_text()
    lib = re.sub(r"\n\t\(version \d+\)\n\t\(generator [^\n]+\)\n", "\n", lib)
    lib = re.sub(r'^\(footprint "[^"]+"', f'(footprint "{Path(lib_dir).stem}:{name}"', lib)
    head = re.search(r'\t\t\(layer "[^"]+"\)\n\t\t\(uuid "[^"]+"\)\n\t\t\(transform\n.*?\n\t\t\)\n', raw, re.S).group(0)
    if side == "F":
        head = re.sub(r'\(layer "B\.Cu"\)', '(layer "F.Cu")', head, count=1)
    elif '(layer "B.Cu")' in head:
        raise ValueError(f"{ref} is on B.Cu; a library land pattern needs side='F' or a flip")
    if side == "F":
        raw = raw.replace('(layer "B.Fab")', '(layer "F.Fab")').replace('(layer "B.SilkS")', '(layer "F.SilkS")')
        raw = re.sub(r"\(justify[^)]*mirror[^)]*\)", "", raw)
    keep = "".join(m.group(0) for m in re.finditer(
        r'\t\t\(property "(?:Reference|Value|Datasheet|Description)".*?\n\t\t\)\n|\t\t\(path [^\n]+\n|\t\t\(sheetname [^\n]+\n|\t\t\(sheetfile [^\n]+\n', raw, re.S))
    lib = "\t" + lib.strip().replace("\n", "\n\t")
    lib = re.sub(r'\t\t\(layer "F.Cu"\)\n', head.replace("\t\t", "\t\t", 1), lib, count=1)
    # library properties: drop Reference/Value/KiLib ones, insert the board's own
    lib = re.sub(r'\t\t\(property "(?:Reference|Value|Datasheet|Description)".*?\n\t\t\)\n', "", lib, flags=re.S)
    lib = lib.replace("\t\t(attr", keep + "\t\t(attr", 1)

    def pad_fix(m):
        block = m.group(0)
        num = re.match(r'\t\t\(pad "([^"]*)"', block).group(1)
        old = old_pads.get(num)
        if not old or not find(old, "net"):
            return block
        extra = f'\t\t\t(net "{find(old, "net")[1]}")\n'
        for key in ("pinfunction", "pintype"):
            v = find(old, key)
            if v:
                extra += f'\t\t\t({key} "{v[1]}")\n'
        return block[:-4] + extra + block[-4:]
    lib = re.sub(r'\t\t\(pad .*?\n\t\t\)\n', pad_fix, lib, flags=re.S)
    b.text = b.text[:s] + lib.lstrip("\t") + b.text[e:]
    b._index()
