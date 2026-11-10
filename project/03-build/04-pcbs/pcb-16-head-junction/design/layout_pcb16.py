"""PCB-16 rev A: create, place and hand-route the head junction (D-103).

The board lies flat on the yaw disc's top (head-local Z -34.5), past the end of
the disc channel and beside the +Y yoke leg's foot. Seen from above (KiCad's top
view) in head-local mm:

    KiCad x = X + 142.4   (pitch-axis X -42.4 -> x 100)
    KiCad y = 150 - Y     (Y 50 -> y 100)

and the KiCad STEP (--user-origin 0x0mm) maps to head-local by X = x_step - 142.4,
Y = 150 + y_step, Z = -34.5 + z_step. check_pcb16_fit.py uses the same transform.

J1 (near, mouth -Y) takes the lower channel FFC, W43 signal; J2 (far, mouth -Y)
the upper, W42 power, reached by a raised run over J1 (PCB-08's stepped method).
Headless as PCB-12: `--create` builds the board from skeleton blocks swapped for
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

NAME = "pcb-16-head-junction"
BOARD = HERE / f"{NAME}.kicad_pcb"
REPORT = HERE / "placement-drc.json"
PCB08 = HERE.parents[1] / "pcb-08-yaw-junction" / "design" / "pcb-08-yaw-junction.kicad_pcb"
STOCK = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")
PROJECT_LIB = HERE.parents[1] / "lib"
THICKNESS = 0.8


def xy(x, y):
    """Head-local (X, Y) -> KiCad (x, y)."""
    return (round(x + 142.4, 4), round(150.0 - y, 4))


# Board on the disc top: X -49.5..-26, Y 35.5..54, stepped in to X -47.6 (from Y 47.7) beside the leg foot
# (whose flare reaches X -47.95 from Y 48.05 up at the disc), plus a tab to X -62.4 for Y 35.5..41, clear of the
# foot's M2 screw heads (from Y 46.97). Both ZIFs end before the leg's inner face.
OUTLINE_PTS = [(80.0, 114.5), (80.0, 109.0), (92.9, 109.0), (92.9, 102.3), (94.8, 102.3), (94.8, 96.0),
               (116.4, 96.0), (116.4, 114.5)]
HOLES = [(85.0, 111.8), (110.5, 98.0)]
HOLE_R, HEAD_KEEPOUT_R = 1.1, 2.0

PLACE = {   # ref: (x, y, rotation)
    "J1": (100.0, 112.1, 0),     # near FH34SRJ, W43 signal, mouth -Y (entry face Y 36.0)
    "J2": (100.0, 104.7, 0),     # far FH34SRJ, W42 power, mouth -Y (entry face Y 43.4, rear Y 47.2)
    "J3": (98.0, 98.05, 0),      # +6V3 / GND_HEAD AWG20 pads over J2's power contacts
    "J5": (102.75, 98.05, 0),    # +5V_C2 / GND_C2
    "J6": (105.75, 98.05, 0),    # +5V_DISPLAY / GND_DISPLAY
    "J4": (114.5, 107.0, 270),   # signal column: GND_SIG, C0TX+/-, C2TX-/+, SERVO_DATA x2
}
BARE = ("J3", "J4", "J5", "J6")


def sym_uuid(ref):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb16/" + ref))


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
                     lambda m: f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb16/fp/" + ref + "/" + str(next(ids)))}")', raw)
        blocks.append((ref, raw))
    BOARD.write_text(head + "\n".join(raw for _, raw in blocks) + "\n\t(embedded_fonts no)\n)\n")
    b = K.Board(BOARD)
    for ref, item in manifest.items():
        if ref.startswith("#"):
            continue
        lib, name = item["footprint"].split(":")
        if lib == "fh34":   # the skeleton is already PCB-08's placed FH34SRJ block
            continue
        lib_dir = PROJECT_LIB / f"{lib}.pretty" if lib in ("pcb16", "fh34") else STOCK / f"{lib}.pretty"
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
    pts = OUTLINE_PTS + [OUTLINE_PTS[0]]
    b.add(*[K.edge_line(f"pcb16-edge-{i}", a, c, 0.05) for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    for i, (hx, hy) in enumerate(HOLES):
        b.add(f'\t(gr_circle\n\t\t(center {hx} {hy})\n\t\t(end {hx + HOLE_R} {hy})\n\t\t(stroke\n\t\t\t(width 0.05)\n'
              f'\t\t\t(type default)\n\t\t)\n\t\t(fill no)\n\t\t(layer "Edge.Cuts")\n\t\t(uuid "{K.gen_uuid(f"pcb16-hole-{i}")}")\n\t)')
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
    b.add(f'\t(gr_text "PCB-16 A"\n\t\t(at 100 108.1 0)\n\t\t(layer "B.SilkS")\n\t\t(uuid "{K.gen_uuid("silk-id")}")\n'
          '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t\t(thickness 0.16)\n\t\t\t)\n\t\t\t(justify mirror)\n\t\t)\n\t)')


def route(b):
    """Power straight back from J2 into its pads; W43 lanes right through the band to J4."""
    parts = []
    P = lambda ref, n: tuple(b.pad(ref, n)["at"])

    def octo(pts):
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

    rear2 = 102.1   # J2 pad rear ends are at y 101.95
    # ---- W42 power (J2) straight back into the far-edge pads.
    parts.append(K.pour("HEAD_POS", "F.Cu", "/+6V3_HEAD_PR", [(94.5, 99.5), (98.0, 99.5), (98.0, 102.8), (94.5, 102.8)],
                        clearance=0.16, min_width=0.2, solid=True))
    parts.append(K.pour("HEAD_RET", "F.Cu", "/GND_HEAD", [(98.0, 99.5), (101.5, 99.5), (101.5, 102.8), (98.0, 102.8)],
                        clearance=0.16, min_width=0.2, solid=True))
    for name, net, (m_a, m_b), pad in (("C2P", "+5V_C2", (8, 7), P("J5", 1)), ("C2R", "GND_C2", (6, 5), P("J5", 2)),
                                       ("DSP", "+5V_DISPLAY", (4, 3), P("J6", 1)), ("DSR", "GND_DISPLAY", (2, 1), P("J6", 2))):
        a, c = P("J2", m_a), P("J2", m_b)
        xc = round((a[0] + c[0]) / 2, 4)
        t(name + "_BAR", net, 0.3, "F.Cu", (a[0], rear2), (c[0], rear2))
        t(name + "_A", net, 0.3, "F.Cu", a, (a[0], rear2))
        t(name + "_B", net, 0.3, "F.Cu", c, (c[0], rear2))
        t(name, net, 0.3, "F.Cu", (xc, rear2), (xc, 100.8), (pad[0], round(100.8 - abs(pad[0] - xc), 4)), pad)

    # ---- W43 signal (J1). GND_SIG contacts join under the ZIF body (Hirose allows traces there).
    g = [P("J1", m) for m in (22, 19, 16, 14)]
    bar = 111.4
    for k, gp in enumerate(g):
        t(f"GSIG_STUB_{k}", "GND_SIG", 0.2, "F.Cu", gp, (gp[0], bar))
    t("GSIG_BAR", "GND_SIG", 0.2, "F.Cu", (g[0][0], bar), (g[-1][0], bar))
    # Lanes: leftmost contact highest; each turns up at its column and lands on J4.
    lanes = (  # net, contact, lane y, turn x, J4 pad
        ("GND_SIG", 22, 107.3, 108.5, 1), ("C0TX_P", 21, 107.9, 109.1, 2), ("C0TX_N", 20, 108.3, 109.7, 3),
        ("C2TX_N", 18, 108.7, 110.3, 4), ("C2TX_P", 17, 109.1, 110.9, 5))
    for net, m, ly, tx, pin in lanes:
        sp, dp = P("J1", m), P("J4", pin)
        t(f"LANE_{m}", net, 0.2, "F.Cu", sp, (sp[0], ly + 0.3), (sp[0] + 0.3, ly), (tx, ly), (tx, dp[1]), dp)
    sd, d6, d7 = P("J1", 15), P("J4", 6), P("J4", 7)
    t("LANE_SD", "SERVO_DATA", 0.2, "F.Cu", sd, (sd[0], 109.5), (111.5, 109.5), (111.5, d7[1]), d7)
    t("LANE_SD6", "SERVO_DATA", 0.2, "F.Cu", (111.5, d6[1]), d6)
    b.add(*parts)


FAB = HERE.parent / "fab" / "revA"
STEP = HERE.parent / "cad" / f"{NAME}-revA.step"
ORIGIN = (80.0, 114.5)
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
