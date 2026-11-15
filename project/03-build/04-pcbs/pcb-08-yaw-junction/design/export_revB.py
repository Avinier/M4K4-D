"""Reproducible rev B fabrication outputs; refuses electrical errors.

Library-copy warnings from Fab label/model edits remain explicitly reported.
"""
import json
import re
from pathlib import Path
from layout_pcb08 import K, HERE, BOARD
FAB=HERE.parent/"fab/revB"
STEP=HERE.parent/"cad/pcb-08-yaw-junction-revB.step"
LAYERS="F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"
MPN={"J1":("43045-0621","Molex"),"J3":("43045-0621","Molex"),
     "J2":("BM06B-GHS-TBT","JST"),"J4":("BM06B-GHS-TBT","JST"),
     "J5":("22-03-5035","Molex"),"R1":("RC0805JR-070RL","Yageo")}
def export():
    """Fab outputs and the board STEP, with PCB-09's conventions (layout_pcb09.export)."""
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
    pos = FAB / "pcb-08-yaw-junction-revB-pos.csv"
    run("pcb", "export", "pos", "--side", "both", "--format", "csv", "--units", "mm", "--use-drill-file-origin",
        "--exclude-dnp", "-o", str(pos))
    with open(pos) as f, open(FAB / "pcb-08-yaw-junction-revB-cpl-jlcpcb.csv", "w", newline="") as g:
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
        if "exclude_from_bom" in attr or "board_only" in attr or "dnp" in attr:
            continue
        props = {p[1]: p[2] for p in K.find_all(n, "property")}
        ref = props["Reference"]
        groups.setdefault((props["Value"], n[1], *MPN.get(ref, ("", ""))), []).append(ref)
    natural = lambda r: (re.match(r"\D+", r).group(0), int(re.search(r"\d+", r).group(0)))
    with open(FAB / "pcb-08-yaw-junction-revB-bom.csv", "w", newline="") as g:
        w = csv.writer(g, quoting=csv.QUOTE_ALL)
        w.writerow(["Comment", "Designator", "Footprint", "Quantity", "MPN", "Manufacturer", "LCSC Part #"])
        for (val, fp, mpn, mfr), refs in sorted(groups.items(), key=lambda kv: natural(sorted(kv[1], key=natural)[0])):
            refs = sorted(refs, key=natural)
            w.writerow([val, ",".join(refs), fp, len(refs), mpn, mfr, ""])
    with zipfile.ZipFile(FAB / "pcb-08-yaw-junction-revB-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(gerb.iterdir()):
            if f.suffix != ".pdf":
                z.write(f, f.name)
    # --user-origin 0x0mm: STEP (X, Y) = (KiCad x, -y); check_pcb08_step_fit.py maps it to world.
    run("pcb", "export", "step", "--subst-models", "--force", "--user-origin", "0x0mm", "-o", str(STEP))
    print("exported", FAB, STEP)


if __name__=="__main__":
    result=K.drc(BOARD,HERE/"placement-drc.json")
    errors=[r for key in ("violations","unconnected_items","schematic_parity") for r in result["report"].get(key,[]) if r.get("severity")=="error"]
    assert not errors,errors
    export()
    import subprocess
    for kind,args in (("netlist",[]),("pdf",[])):
        subprocess.run([K.CLI,"sch","export",kind,"-o",str(HERE/("pcb-08-yaw-junction.net" if kind=="netlist" else "pcb-08-yaw-junction-schematic.pdf")),str(HERE/"pcb-08-yaw-junction.kicad_sch")],check=True,capture_output=True)
