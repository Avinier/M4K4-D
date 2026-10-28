"""KiPy helpers for laying out a board in the running KiCad 10.99 nightly (D-060).

Proven on PCB-15 rev A (2026-10-25). Run with the KiPy venv:

    ~/.local/share/kipy/venv/bin/python -c "import sys; sys.path.insert(0, '<this folder>'); from kp import *; ..."

KiPy only answers once the board is open in the PCB editor (Update PCB from Schematic,
F8, is a GUI step for the builder). Known traps, handled here:
- flip_items() strips footprint 3D models: place() puts them back from the library.
- F8 drops a footprint's exclude-from-position-files flag: call exclude_from_pos() after it.
"""
import os
import re
import subprocess
from pathlib import Path

from kipy import KiCad
from kipy.board_types import Footprint3DModel, Track, Via
from kipy.geometry import Angle, Vector2, Vector3D
from kipy.proto.board.board_types_pb2 import BoardLayer as BL

CLI = "/Applications/KiCad-nightly/KiCad.app/Contents/MacOS/kicad-cli"
APP = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport")
GLOBAL_FP_TABLE = Path.home() / "Library/Preferences/kicad/10.99/fp-lib-table"
F, B = BL.BL_F_Cu, BL.BL_B_Cu

k = KiCad()
b = k.get_board()
mm = lambda v: round(v / 1e6, 4)


def design_dir():
    """Folder of the open board's project (or $PCB_DESIGN)."""
    if os.environ.get("PCB_DESIGN"):
        return Path(os.environ["PCB_DESIGN"])
    return Path(b.get_project().path)


def board_file():
    return design_dir() / b.name


def fps():
    return {fp.reference_field.text.value: fp for fp in b.get_footprints()}


def pads(ref):
    fp = fps()[ref]
    return {p.number: (p.net.name, mm(p.position.x), mm(p.position.y)) for p in fp.definition.pads}


def _lib_path(nickname):
    for table in (design_dir() / "fp-lib-table", GLOBAL_FP_TABLE):
        if table.exists():
            m = re.search(r'\(name "%s"\)\s*\(type "[^"]*"\)\s*\(uri "([^"]*)"' % re.escape(nickname), table.read_text())
            if m:
                uri = m.group(1).replace("${KIPRJMOD}", str(design_dir()))
                return Path(uri.replace("${KICAD10_FOOTPRINT_DIR}", str(APP / "footprints")))
    raise KeyError(nickname)


def library_models(fp):
    """(filename, offset, scale, rotate) of each 3D model in the footprint's library copy."""
    lib, name = fp.definition.id.library, fp.definition.id.name
    text = (_lib_path(lib) / f"{name}.kicad_mod").read_text()
    out = []
    for m in re.finditer(r'\(model "([^"]+)"', text):
        depth, i = 1, m.end()   # balance parentheses: models may be one line or several
        while depth:
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i]
        vec = lambda key: tuple(float(v) for v in re.search(r"\(%s\s*\(xyz ([^)]*)\)" % key, body).group(1).split())
        out.append((m.group(1), vec("offset"), vec("scale"), vec("rotate")))
    return out


def restore_models(ref):
    """Give a footprint back its library 3D models if the board copy has none."""
    fp = fps()[ref]
    if fp.definition.models:
        return False
    for filename, offset, scale, rotate in library_models(fp):
        m = Footprint3DModel()
        m.filename = filename
        m.offset = Vector3D.from_xyz(*offset)
        m.scale = Vector3D.from_xyz(*scale)
        m.rotation = Vector3D.from_xyz(*rotate)
        m.visible, m.opacity = True, 1.0
        fp.definition.add_item(m)
    b.update_items([fp])
    return True


def place(ref, x, y, rot=0.0, back=False):
    """Move a footprint (KiCad mm), turn it, put it on the front or back; returns its pads."""
    fp = fps()[ref]
    if back != (fp.layer == B):
        b.flip_items([fp])
        fp = fps()[ref]
    fp.position = Vector2.from_xy_mm(x, y)
    fp.orientation = Angle.from_degrees(rot)
    b.update_items([fp])
    restore_models(ref)
    return pads(ref)


def exclude_from_pos(*refs):
    """Keep bare-copper footprints (wire pads, test pads) out of the pick-and-place file."""
    all_fps = fps()
    upd = []
    for ref in refs:
        all_fps[ref].attributes.exclude_from_position_files = True
        upd.append(all_fps[ref])
    b.update_items(upd)


def refs_to_fab():
    """Move reference labels from silkscreen to the fab layers (small boards have no room)."""
    upd = []
    for fp in fps().values():
        f = fp.reference_field
        if f.layer in (BL.BL_F_SilkS, BL.BL_B_SilkS):
            f.layer = BL.BL_F_Fab if f.layer == BL.BL_F_SilkS else BL.BL_B_Fab
            upd.append(fp)
    if upd:
        b.update_items(upd)


def nets():
    return {n.name: n for n in b.get_nets()}


def track(net, layer, *pts, width=0.2):
    """Route a chain of segments; refuses anything but 0/45/90 degree segments (D-060)."""
    n = nets()[net]
    items = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        assert dx < 1e-6 or dy < 1e-6 or abs(dx - dy) < 1e-6, f"not octolinear: {(x0, y0)} -> {(x1, y1)}"
        t = Track()
        t.start, t.end = Vector2.from_xy_mm(x0, y0), Vector2.from_xy_mm(x1, y1)
        t.width, t.layer, t.net = int(width * 1e6), layer, n
        items.append(t)
    return b.create_items(items)


def via(net, x, y, d=0.67, drill=0.35):
    """Through via; the default is the fab-neutral minimum of D-062."""
    v = Via()
    v.position = Vector2.from_xy_mm(x, y)
    v.diameter, v.drill_diameter, v.net = int(d * 1e6), int(drill * 1e6), nets()[net]
    return b.create_items([v])


def save():
    b.save()


def model_path(filename):
    """A footprint model's file on disk, with KiCad's path variables resolved."""
    return Path(filename.replace("${KICAD10_3DMODEL_DIR}", str(APP / "3dmodels")).replace("${KIPRJMOD}", str(design_dir())))


def audit():
    """Footprints missing models (named, or named but not on disk), and bare-copper parts in the position file."""
    for ref, fp in sorted(fps().items()):
        lib = library_models(fp)
        lost = [m.filename for m in fp.definition.models if not model_path(m.filename).exists()]
        print(f"{ref:5} models {len(fp.definition.models)}/{len(lib)}"
              f"  pos-excluded {fp.attributes.exclude_from_position_files}"
              f"  bom-excluded {fp.attributes.exclude_from_bill_of_materials}"
              + (f"  MISSING FILE {lost}" if lost else ""))


def drc(out="/tmp/kp-drc.rpt"):
    """Nightly DRC with schematic parity on the saved board; returns the report's key lines."""
    subprocess.run([CLI, "pcb", "drc", "--schematic-parity", "--severity-all", "--format", "report", "-o", out,
                    str(board_file())], capture_output=True)
    keep = ("[", "    @", "    Rule", "** Found")
    return "\n".join(l for l in open(out).read().splitlines() if l.startswith(keep))


def remove_in(x0, y0, x1, y1, net=None):
    """Delete tracks and vias with both ends (or the via) inside a KiCad-mm box, optionally of one net."""
    inside = lambda p: x0 <= mm(p.x) <= x1 and y0 <= mm(p.y) <= y1
    gone = []
    for t in b.get_tracks():
        if (net is None or t.net.name == net) and inside(t.start) and inside(t.end):
            gone.append(t)
    for v in b.get_vias():
        if (net is None or v.net.name == net) and inside(v.position):
            gone.append(v)
    if gone:
        b.remove_items(gone)
    return len(gone)
