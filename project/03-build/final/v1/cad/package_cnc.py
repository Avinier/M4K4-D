"""Copies the CNC fabrication pack from ../fab/ to 04-print/04-cnc/upload/, one folder per
part, plus one zip of the lot and a manifest with SHA-256 hashes.

../fab/ is the source; upload/ is a copy for sending to shops and is never edited.
Run after export_cnc_fab.py, cnc_drawings.py (and export_axle_fab.py /
export_d120_fab.py when those parts change); `--check` reports any upload file that
differs from fab/ without copying. Plain Python, no CAD runtime needed.
"""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAB = HERE.parent / "fab"
UPLOAD = HERE.parents[3] / "04-print" / "04-cnc" / "upload"
ZIP = UPLOAD / "makad-cnc-pack-revA.zip"

PACK = {   # part folder -> process; files are every fab/<part>* file
    "CH-012_stub": "CNC turning (EN8)",
    "CH-013_ballast_bar": "CNC milling (C110 copper)",
    "CH-052_cap": "Fibre laser / waterjet (1.2 mm aluminium)",
    "BO-047_pinion_shaft": "Cut to length (from 5 mm D-shaft stock)",
    "BO-046_fixed_pinion_half": "Wire EDM / fibre laser (2 mm 7075-T6 plate)",
    "HD-004_roll_hub_collar": "CNC turning (6061 aluminium)",
    "HD-009_pivot_pin": "Cut + surface grind (from Ø6 h6 rod)",
    "HD-034_roll_spindle": "Cut + surface grind (from Ø6 h6 rod)",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(part):
    out = sorted(p for p in FAB.glob(f"{part}*") if p.suffix in (".step", ".pdf", ".dxf"))
    assert any(p.suffix == ".step" for p in out) and any(p.suffix == ".pdf" for p in out), (part, out)
    return out


def check():
    bad = []
    for part in PACK:
        for src in files(part):
            dst = UPLOAD / part / src.name
            if not dst.exists() or sha(dst) != sha(src):
                bad.append(str(dst.relative_to(UPLOAD)))
    print("upload/ matches fab/" if not bad else "stale or missing in upload/: " + ", ".join(bad))
    return not bad


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    UPLOAD.mkdir(parents=True, exist_ok=True)
    manifest = {"source": "project/03-build/final/v1/fab", "parts": {}}
    for part, process in PACK.items():
        d = UPLOAD / part
        if d.exists():
            shutil.rmtree(d)
        d.mkdir()
        manifest["parts"][part] = {"process": process, "files": {}}
        for src in files(part):
            shutil.copy2(src, d / src.name)
            manifest["parts"][part]["files"][src.name] = sha(src)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for part in PACK:
            for f in sorted((UPLOAD / part).iterdir()):
                z.write(f, f"{part}/{f.name}")
    (UPLOAD / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    n = sum(len(v["files"]) for v in manifest["parts"].values())
    print(f"copied {n} files for {len(PACK)} parts to {UPLOAD}; zip {ZIP.name} ({ZIP.stat().st_size / 1024:.0f} KB)")
    check()


if __name__ == "__main__":
    main()
