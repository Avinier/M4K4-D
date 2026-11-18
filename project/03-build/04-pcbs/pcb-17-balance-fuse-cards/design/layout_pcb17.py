"""PCB-17 rev A: create, place and hand-route the CH-103 balance-tap fuse cards (D-116).

Two 0.8 mm cards in one board file; at procure they are panelised with PCB-11
and PCB-15 (same 0.8 mm stackup). Each card lies component side up on the
PCB-01 (HW-391) BMS under a CH-106 relief. KiCad (x, y down) to droid CAD:

    card A (BM, +Y end):        X = x - 59.0,  Y = 124.0 - y
    card B (B-/B+, -Y end):     X = x - 70.7,  Y = 86.0 - y

so each card's cell pads face its BMS pad end (card A y 100 = Y 24; card B
y 110 = Y -24). Board Z 0 is the card's underside on the BMS (droid Z 54.2).
Headless as PCB-16: `--create` builds the board from skeleton blocks swapped for
the library land patterns. No autorouter; every track is placed by hand.
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

NAME = "pcb-17-balance-fuse-cards"
BOARD = HERE / f"{NAME}.kicad_pcb"
REPORT = HERE / "placement-drc.json"
TEMPLATE = HERE.parents[1] / "pcb-16-head-junction" / "design" / "pcb-16-head-junction.kicad_pcb"
STOCK = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")
PROJECT_LIB = HERE.parents[1] / "lib"
THICKNESS = 0.8

OUTLINES = {"A": [(100.0, 100.0), (106.0, 100.0), (106.0, 109.0), (100.0, 109.0)],
            "B": [(110.0, 100.0), (119.5, 100.0), (119.5, 110.0), (110.0, 110.0)]}
PLACE = {   # ref: (x, y, rotation); fuse pad 1 (cell) toward the BMS pad end
    "J1": (103.0, 101.15, 0), "F1": (103.0, 104.5, 270), "J2": (103.0, 107.85, 0),
    "J3": (112.7, 108.85, 0), "F2": (112.7, 105.0, 90), "J4": (112.7, 101.15, 0),
    "J5": (116.7, 108.85, 0), "F3": (116.7, 105.0, 90), "J6": (116.7, 101.15, 0),
}
BARE = ("J1", "J2", "J3", "J4", "J5", "J6")
SILK = [("BM", 105.0, 104.5, 90, "F.SilkS"), ("B-", 110.85, 105.0, 90, "F.SilkS"), ("B+", 118.65, 105.0, 90, "F.SilkS"),
        ("17A", 103.0, 104.5, 90, "B.SilkS"), ("17B", 114.75, 105.0, 90, "B.SilkS")]


def sym_uuid(ref):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb17/" + ref))


def create():
    src = TEMPLATE.read_text()
    head = src[:src.index("\t(footprint ")].replace("(thickness 1.6)", f"(thickness {THICKNESS})", 1)
    template = next(raw for raw in K.Board(TEMPLATE).blocks("footprint") if '(property "Reference" "J3"' in raw)
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
        raw = raw.replace("pcb-16-head-junction.kicad_sch", f"{NAME}.kicad_sch")

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
                     lambda m: f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb17/fp/" + ref + "/" + str(next(ids)))}")', raw)
        blocks.append((ref, raw))
    BOARD.write_text(head + "\n".join(raw for _, raw in blocks) + "\n\t(embedded_fonts no)\n)\n")
    b = K.Board(BOARD)
    for ref, item in manifest.items():
        if ref.startswith("#"):
            continue
        lib, name = item["footprint"].split(":")
        lib_dir = PROJECT_LIB / f"{lib}.pretty" if lib == "pcb17" else STOCK / f"{lib}.pretty"
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
    for card, pts in OUTLINES.items():
        pts = pts + [pts[0]]
        b.add(*[K.edge_line(f"pcb17-edge-{card}-{i}", a, c, 0.05) for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    for ref, (x, y, rot) in PLACE.items():
        b.move(ref, x, y, rot)
    for ref in PLACE:   # references on the assembly drawing only; the cards are too small for 1 mm silk refs
        start, end, raw = block_of(b, ref)
        raw = re.sub(r'(\(property "Reference" "[^"]+"\s+\(at [^)]*\)\s+\(layer )"F.SilkS"', r'\1"F.Fab"', raw, count=1)
        b.text = b.text[:start] + raw + b.text[end:]
        b._index()
    for text, x, y, rot, layer in SILK:
        mirror = "\n\t\t\t(justify mirror)" if layer.startswith("B.") else ""
        b.add(f'\t(gr_text "{text}"\n\t\t(at {x} {y} {rot})\n\t\t(layer "{layer}")\n\t\t(uuid "{K.gen_uuid("silk-" + text)}")\n'
              f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t\t(thickness 0.16)\n\t\t\t){mirror}\n\t\t)\n\t)')


def route(b):
    """Each wire pad straight into its fuse land: 0.8 mm tracks, one column per tap."""
    parts = []
    P = lambda ref, n: tuple(b.pad(ref, n)["at"])
    for tap, f, jc, jo in (("BM", "F1", "J1", "J2"), ("BMINUS", "F2", "J3", "J4"), ("BPLUS", "F3", "J5", "J6")):
        parts.extend(K.track(f"{tap}_CELL", [P(jc, 1), P(f, 1)], 0.8, "F.Cu", f"/{tap}_CELL"))
        parts.extend(K.track(f"{tap}_FUSED", [P(f, 2), P(jo, 1)], 0.8, "F.Cu", f"/{tap}_FUSED"))
    b.add(*parts)


FAB = HERE.parent / "fab" / "revA"
STEP = HERE.parent / "cad" / f"{NAME}-revA.step"
ORIGIN = (100.0, 110.0)
LAYERS = "F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"


def set_origin(b):
    for key in ("aux_axis_origin", "grid_origin"):
        line = f"({key} {ORIGIN[0]} {ORIGIN[1]})"
        if f"({key} " in b.text:
            b.text = re.sub(rf"\({key} [-\d.]+ [-\d.]+\)", line, b.text, count=1)
        else:
            b.text = b.text.replace("\t(setup\n", f"\t(setup\n\t\t{line}\n", 1)
    b._index()


MPN = {"J1": ("FH34SRJ-22S-0.5SH(99)", "Hirose"), "J2": ("FH34SRJ-22S-0.5SH(99)", "Hirose")}


MPN = {f: ("0466001.NRHF", "Littelfuse") for f in ("F1", "F2", "F3")}


def export():
    """Fab outputs and the board STEP, with PCB-16's conventions."""
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
