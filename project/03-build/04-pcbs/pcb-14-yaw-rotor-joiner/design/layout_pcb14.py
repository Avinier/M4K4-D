"""PCB-14 rev A: create, place and hand-route the two-layer 0.8 mm joiner board.

One design, built three times (D-052, D-101). The board stands vertical in the
yaw rotor with its component face toward +Y. Seen from that face (KiCad's
top view), world +X is to the left and +Z is up, so

    KiCad x = 116 - world X     (yaw axis X 16 -> x 100)
    KiCad y = 242.3 - world Z   (board centre Z 142.3 -> y 100)

and the KiCad STEP (--user-origin 0x0mm) maps to world by X = 116 - x_step,
Z = 242.3 + y_step, Y = board back face + z_step. check_pcb14_fit.py uses
the same transform.

There are only two footprints, so the board is written headless (no F8):
`--create` builds the .kicad_pcb from PCB-08's board header and its placed
FH34SRJ block, with this schematic's symbol paths and pad nets, and the
Nightly DRC then rewrites it in KiCad's own form. J1 is the lower ZIF,
mouth down (rotation 0, contact 1 at world -X); J2 is the upper ZIF, mouth
up (rotation 180, contact 1 at world +X). Contact n of J1 lies straight
under contact 23-n of J2, so each lane is one straight F.Cu track.
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

NAME = "pcb-14-yaw-rotor-joiner"
BOARD = HERE / f"{NAME}.kicad_pcb"
REPORT = HERE / "placement-drc.json"
PCB08 = HERE.parents[1] / "pcb-08-yaw-junction" / "design" / "pcb-08-yaw-junction.kicad_pcb"
THICKNESS = 0.8          # D-052
AXIS_X, CENTRE_Z = 16.0, 142.3


def xy(world_x, world_z):
    return (round(116.0 - world_x, 4), round(242.3 - world_z, 4))


# Board, world X relative to the axis and Z: body |x| <= 7.25 over Z 133.9..150.7
# (narrowed from D-052's 8.5 so the corners keep >= 1.2 mm to the disc's R10.5
# bore at the D-101 pitch); tabs to |x| 13.6 over Z 137.4..143.0 into the posts.
BODY_HX, TAB_HX = 7.25, 13.6
Z0, Z1, TAB_Z0, TAB_Z1 = 133.9, 150.7, 137.4, 143.0
OUTLINE_W = [(-BODY_HX, Z1), (BODY_HX, Z1), (BODY_HX, TAB_Z1), (TAB_HX, TAB_Z1),
             (TAB_HX, TAB_Z0), (BODY_HX, TAB_Z0), (BODY_HX, Z0), (-BODY_HX, Z0),
             (-BODY_HX, TAB_Z0), (-TAB_HX, TAB_Z0), (-TAB_HX, TAB_Z1), (-BODY_HX, TAB_Z1)]

# ZIF origins: the solder-tab copper (footprint local y +2.05) keeps 0.35 mm
# to the board edge, so the mouths are at Z 134.40 (lower) and 150.20 (upper).
PLACE = {
    "J1": (xy(AXIS_X, 136.30), 0),     # lower, mouth down: cassette FFC
    "J2": (xy(AXIS_X, 148.30), 180),   # upper, mouth up: head FFC
}
LANE_W = 0.3   # pad width; 0.2 mm gap at 0.5 mm pitch; 0.5 A per lane (FH34SRJ rating)


def sym_uuid(ref):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb14/" + ref))


def create():
    """Write a fresh board: PCB-08's header (0.8 mm) and two FH34SRJ blocks."""
    src = PCB08.read_text()
    head = src[:src.index("\t(footprint ")]
    head = head.replace("(thickness 1.6)", f"(thickness {THICKNESS})", 1)
    b8 = K.Board(PCB08)
    template = next(raw for raw in b8.blocks("footprint") if '(property "Reference" "J3"' in raw)
    manifest = json.loads((HERE / "circuit-manifest.json").read_text())
    blocks = []
    for ref, ((x, y), rot) in PLACE.items():
        raw = template
        raw = re.sub(r"\(translate [-\d.]+ [-\d.]+\)", f"(translate {x} {y})", raw, count=1)
        raw = re.sub(r"\(rotate [-\d.]+\)", f"(rotate {rot})", raw, count=1)
        raw = raw.replace('(property "Reference" "J3"', f'(property "Reference" "{ref}"', 1)
        raw = re.sub(r'\(property "Value" "[^"]*"', f'(property "Value" "{manifest[ref]["value"]}"', raw, count=1)
        raw = re.sub(r'\(path "/[^"]+"\)', f'(path "/{sym_uuid(ref)}")', raw, count=1)
        raw = raw.replace("pcb-08-yaw-junction.kicad_sch", f"{NAME}.kicad_sch")
        # Nightly pad angles are absolute: the template is at 90 deg.
        raw = re.sub(r"(\(at [-\d.]+ [-\d.]+) 90\)", rf"\1 {rot})", raw)

        def pad_net(m):
            block = m.group(0)
            num = re.match(r'\t\t\(pad "(\d+)"', block).group(1)
            net = manifest[ref]["pins"][num]
            return re.sub(r'\(net "[^"]*"\)', f'(net "/{net}")', block, count=1)
        raw = re.sub(r'\t\t\(pad "\d+".*?\n\t\t\)\n', pad_net, raw, flags=re.S)
        # Plain uuid5s: kfile's own namespace marks items drop_generated() removes.
        ids = iter(range(100000))
        raw = re.sub(r'\(uuid "[^"]+"\)', lambda m: f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb14/fp/" + ref + "/" + str(next(ids)))}")', raw)
        blocks.append(raw)
    BOARD.write_text(head + "\n".join(blocks) + "\n\t(embedded_fonts no)\n)\n")
    print("created", BOARD.name)


def silk_text(name, text, at, layer="F.SilkS", size=1.0, angle=0):
    mirror = " (justify mirror)" if layer.startswith("B.") else ""
    return (f'\t(gr_text "{text}"\n\t\t(at {at[0]} {at[1]} {angle})\n\t\t(layer "{layer}")\n'
            f'\t\t(uuid "{K.gen_uuid(name)}")\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size {size} {size})\n'
            f'\t\t\t\t(thickness 0.16)\n\t\t\t)\n\t\t\t{mirror.strip() or "(justify)"}\n\t\t)\n\t)')


def setup(b):
    b.drop_generated()
    b.drop(lambda kind, raw: kind in ("gr_line", "gr_rect", "gr_text") and
           ('(layer "Edge.Cuts")' in raw or "SilkS" in raw))
    pts = [xy(AXIS_X + x, z) for x, z in OUTLINE_W]
    pts.append(pts[0])
    b.add(*[K.edge_line(f"pcb14-edge-{i}", a, c, 0.05) for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    for ref, ((x, y), rot) in PLACE.items():
        b.move(ref, x, y, rot)
    # Conductor 1 sits at -X (KiCad +x) on both ZIFs: lower contact 1, upper contact 22.
    l1 = b.pad("J1", 1)["at"]
    u22 = b.pad("J2", 22)["at"]
    b.add(silk_text("silk-1", "1", (round(l1[0] + 1.05, 3), round(l1[1] - 1.25, 3))),
          silk_text("silk-22", "22", (round(u22[0] + 1.05, 3), round(u22[1] + 1.6, 3)), angle=90),
          silk_text("silk-id", "PCB-14 A", xy(AXIS_X, CENTRE_Z), layer="B.SilkS"))


def route(b):
    """22 straight F.Cu lanes: J1 contact n up to J2 contact 23-n."""
    parts = []
    for n in range(1, 23):
        lo, up = b.pad("J1", n), b.pad("J2", 23 - n)
        assert abs(lo["at"][0] - up["at"][0]) < 1e-6, (n, lo["at"], up["at"])
        net = f"/FFC{n:02d}"
        parts.extend(K.track(f"LANE_{n:02d}", [lo["at"], up["at"]], LANE_W, "F.Cu", net))
    b.add(*parts)


FAB = HERE.parent / "fab" / "revA"
STEP = HERE.parent / "cad" / f"{NAME}-revA.step"
ORIGIN = xy(AXIS_X + TAB_HX, Z0)   # bottom-left seen from the component face: aux and grid origin
LAYERS = "F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"
MPN = {"J1": ("FH34SRJ-22S-0.5SH(99)", "Hirose"), "J2": ("FH34SRJ-22S-0.5SH(99)", "Hirose")}


def set_origin(b):
    for key in ("aux_axis_origin", "grid_origin"):
        line = f"({key} {ORIGIN[0]} {ORIGIN[1]})"
        if f"({key} " in b.text:
            b.text = re.sub(rf"\({key} [-\d.]+ [-\d.]+\)", line, b.text, count=1)
        else:
            b.text = b.text.replace("\t(setup\n", f"\t(setup\n\t\t{line}\n", 1)
    b._index()


def export():
    """Fab outputs and the board STEP, with PCB-08's conventions (layout_pcb08.export)."""
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
        props = {p[1]: p[2] for p in K.find_all(n, "property")}
        ref = props["Reference"]
        groups.setdefault((n[1], *MPN[ref]), []).append(ref)
    with open(FAB / f"{NAME}-revA-bom.csv", "w", newline="") as g:
        w = csv.writer(g, quoting=csv.QUOTE_ALL)
        w.writerow(["Comment", "Designator", "Footprint", "Quantity", "MPN", "Manufacturer", "LCSC Part #"])
        for (fp, mpn, mfr), refs in groups.items():
            w.writerow(["FH34SRJ-22S ZIF", ",".join(sorted(refs)), fp, len(refs), mpn, mfr, ""])
    with zipfile.ZipFile(FAB / f"{NAME}-revA-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(gerb.iterdir()):
            if f.suffix != ".pdf":
                z.write(f, f.name)
    STEP.parent.mkdir(parents=True, exist_ok=True)
    run("pcb", "export", "step", "--subst-models", "--force", "--user-origin", "0x0mm", "-o", str(STEP))
    print("exported", FAB, STEP)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--create", action="store_true", help="write a fresh board from the schematic manifest")
    p.add_argument("--no-drc", action="store_true")
    p.add_argument("--export", action="store_true", help="write fab/revA and the board STEP after DRC")
    args = p.parse_args()
    if args.create or not BOARD.exists():
        create()
    b = K.Board(BOARD)
    setup(b)
    set_origin(b)
    route(b)
    b.save()
    print("Placed:", json.dumps({f["ref"]: [*f["at"], f["rot"]] for f in b.footprints()}, sort_keys=True))
    if not args.no_drc:
        result = K.drc(BOARD, REPORT, refill=True)
        print("DRC:", {k: v for k, v in result.items() if k != "report"})
        print(K.summary(result["report"], limit=80))
        if args.export and result["violations"] == result["unconnected"] == result["parity"] == 0:
            export()


if __name__ == "__main__":
    main()
