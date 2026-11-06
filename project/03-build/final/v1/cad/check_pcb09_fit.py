"""PCB-09 rev A fit: place the KiCad board STEP where the droid CAD has the C0 link adapter and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees with the droid edits (about 1 min), not the head.

The STEP is exported with --user-origin 0x0mm, so (Xs, Ys) = (KiCad x, -y) and the core runs
Zs 0..core. pcb_integration.placements(9) moves it to the world (X = Xs - 104.7, Y = 139 + Ys),
centred in the 1.6 mm board on the standoffs (underside Z 106.45, D-092). check_pcb09_mount.py
owns the fixing and the socket stack; this script owns the real parts and their mated plugs.
The vendor Pi and Active Cooler are tested as their real solids (standalone vendor import).
"""

import argparse
import importlib.util
import json
import math
from pathlib import Path

from build123d import Box, Compound, Location
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common

import body_v1_model as B
import pcb_integration as P
from check_pcb05_mount import _box, _hit, _leaves
from check_pcb09_mount import _header_plastic_top, _hits, _vol

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB09_MOUNT

MIN_GAP = 0.2
REGION = (-20.0, 72.0, 5.0, 50.0, 85.0, 170.0)
OWN = ("C0_LINK_ADAPTER_PCB09/", "PCB09_M25", "C0_LINK_ADAPTER_PCB09_RESERVE", "C0_LINK_ADAPTER_TOP_ENTRY_PLUG_RESERVE",
       "C0_LINK_ADAPTER_J91_PLUG_RESERVE", "C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE")
SOFT = ("RESERVE", "KEEP_OUT", "HARNESS_")
# Drilled holes KiCad cuts from the core: 40 socket holes of 1.0 mm and the two 2.7 mm screw holes.
HOLES = math.pi / 4.0 * (40 * 1.0 ** 2 + 2 * 2.7 ** 2)
# Fitted after the bench-assembled tray (as check_compute_mount.py and check_pcb09_mount.py).
LATER = ("C3_", "BODY_FRAME_C3_", "HARNESS_", "SPEAKER_", "PCB05_", "RESERVE", "KEEP_OUT", "PLUG",
         "COMPUTE_TRAY", "PI5_", "PI5_VENDOR/", "C0_LINK_ADAPTER", "PCB09_")


class _Body:  # the plug helper reads the body model's GH plug sizes
    gh_plug_width = staticmethod(B.gh_plug_width)
    GH_PLUG_THICKNESS = B.GH_PLUG_THICKNESS
    GH_PLUG_PROUD = B.GH_PLUG_PROUD


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print("Building body and chassis with current droid edits...", flush=True)
    robot = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference(), entry.build_body_assembly()]), strict=False)
    reg = (REGION[0], REGION[2], REGION[4], REGION[1], REGION[3], REGION[5])
    parts = []
    for path, node, loc in _leaves(robot):
        if path[-1] == "C0_RASPBERRY_PI5_EXACT_STEP":
            continue
        raw = node.wrapped.Moved(loc.wrapped)
        if _hit(_box(raw), reg):
            parts.append(("/".join(path), raw, _box(raw)))
    pi = B.raspberry_pi5()
    pi_parts = [(f"PI5_VENDOR/{i}", s.wrapped, _box(s)) for i, s in enumerate(pi.solids()) if _hit(_box(s), reg)]
    parts += pi_parts
    get = lambda label: next(raw for p, raw, b in parts if p.endswith(label))

    (instance, loc), = P.placements(9, None, None)
    board = P.installed_board(9, instance, loc)
    real = [(c.label.split("__")[-1], c.wrapped, _box(c)) for c in board.children]
    core = next(r for r in real if r[0].endswith("_PCB"))
    comps = [r for r in real if not r[0].endswith("_PCB")]
    plugs = [(c.label, c.wrapped, _box(c)) for c in P.pcb09_mated_plugs(board, _Body)]
    out = []

    # 1. The core is the droid's board: same outline box, underside on the standoffs, same area less the holes.
    cb, pb = core[2], _box(get("C0_LINK_ADAPTER_PCB09_BOARD"))
    t = cb[5] - cb[2]
    off = max(abs(cb[i] - pb[i]) for i in (0, 1, 3, 4))
    under = cb[2] - (1.6 - t) / 2.0
    area = _vol(core[1], Box(200, 200, 50).moved(Location((20, 20, 107))).wrapped) / t
    cad = _vol(get("C0_LINK_ADAPTER_PCB09_BOARD"), Box(200, 200, 50).moved(Location((20, 20, 107))).wrapped) / 1.6
    ok = off < 0.01 and abs(under - (B.PI_PCB_TOP_Z + MNT["standoff"][1])) < 0.01 and abs(area + HOLES - cad) < 0.5
    out.append(("board on the droid board", ok,
                f"core X {cb[0]:.2f}..{cb[3]:.2f}, Y {cb[1]:.2f}..{cb[4]:.2f} (offset {off:.3f}); underside Z {under:.3f}; "
                f"area {area:.1f} + {HOLES:.1f} of holes against the droid's {cad:.1f} mm2"))

    # 2. The socket's model sits on the Pi header: XY on the header, bottom on its plastic.
    sock = next(r for r in comps if r[0] == "J1")
    header = [s for s in pi.solids() if abs((_box(s)[3] - _box(s)[0]) - 50.8) < 1e-3 and abs((_box(s)[4] - _box(s)[1]) - 5.0) < 1e-3][0]
    hb = _box(header)
    plastic, tip = _header_plastic_top(pi)
    sb = sock[2]
    dxy = max(abs((sb[0] + sb[3]) / 2 - (hb[0] + hb[3]) / 2), abs((sb[1] + sb[4]) / 2 - (hb[1] + hb[4]) / 2))
    seat = sb[2] - plastic
    # The mate: the socket model holds the Pi's pins, so it overlaps only the header solid. Everything else
    # on the Pi (and the cooler) must clear the socket model by MIN_GAP.
    mate = _vol(sock[1], header.wrapped)
    pins = len(header.solids()) and 40 * 0.64 * 0.64 * (tip - plastic)
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    rest = min((BRepExtrema_DistShapeShape(sock[1], r).Value() for p_, r, b in pi_parts
                if not p_.endswith("/" + str(list(pi.solids()).index(header))) and _hit(b, sb, 1.0)), default=99.0)
    ok = dxy < 0.05 and -0.1 <= seat <= 0.1 and rest >= MIN_GAP
    out.append(("socket on the Pi header", ok,
                f"socket model centre {dxy:.3f} mm off the header's; its bottom {seat:+.3f} mm from the plastic top "
                f"Z {plastic:.3f} (model 8.5 mm, SSW-120 8.51 mm); pin tips Z {tip:.3f}; overlap with the header solid "
                f"{mate:.1f} mm3 (40 pins of 0.64 x 0.64 over {tip - plastic:.2f} mm = {pins:.1f} mm3, plus the 0.03 mm seat); "
                f"nearest other Pi part {rest:.2f} mm"))

    # 3. Every real part clear of the droid by MIN_GAP. The socket meets the Pi header by design (2);
    #    the core and the socket clear the standoffs and screws (D-092 holes); reserves are reported.
    hard, soft = [], []
    for label, raw, box in [core, *comps]:
        grow = Box(box[3] - box[0] + 2 * MIN_GAP, box[4] - box[1] + 2 * MIN_GAP, box[5] - box[2] + 2 * MIN_GAP).moved(
            Location(((box[0] + box[3]) / 2, (box[1] + box[4]) / 2, (box[2] + box[5]) / 2)))
        skip = OWN + (("PI5_VENDOR/",) if label == "J1" else ())
        for name, v in _hits(grow, parts, skip):
            path = next(p for p, r, b in parts if p.split("/")[-1] == name or p.endswith(name))
            if any(s in path for s in SOFT):
                soft.append(f"{label}~{name}")
                continue
            # a box hit is only a candidate: confirm with the part's own solid grown by MIN_GAP via a distance test
            other = next(r for p, r, b in parts if p.endswith(name))
            from OCP.BRepExtrema import BRepExtrema_DistShapeShape
            d = BRepExtrema_DistShapeShape(raw, other)
            if d.IsDone() and d.Value() < MIN_GAP:
                hard.append(f"{label} {d.Value():.3f} to {name}")
    out.append((f"parts clear of the droid by {MIN_GAP} mm", not hard, "; ".join(hard[:6]) or "clear"))
    print("INFO  reserves near the real parts: " + ("; ".join(sorted(set(soft))[:8]) or "none"))

    # 4. The mated plugs, rebuilt on the real headers, clear the droid by MIN_GAP (reserves reported).
    rows, ok, info = [], True, []
    for label, raw, box in plugs:
        hits = _hits(Box(box[3] - box[0] + 2 * MIN_GAP, box[4] - box[1] + 2 * MIN_GAP, box[5] - box[2] + 2 * MIN_GAP).moved(
            Location(((box[0] + box[3]) / 2, (box[1] + box[4]) / 2, (box[2] + box[5]) / 2))), parts, OWN)
        h = [n for n, v in hits if not any(s in next(p for p, r, b in parts if p.endswith(n)) for s in SOFT)]
        info += [f"{label}~{n}" for n, v in hits if n not in h]
        ok &= not h
        rows.append(f"{label} X {box[0]:.1f}..{box[3]:.1f} Y {box[1]:.1f}..{box[4]:.1f} Z to {box[5]:.1f}: {h or 'clear'}")
    out.append(("mated plugs clear of the droid", ok, "; ".join(rows)))
    print("INFO  reserves near the plugs: " + ("; ".join(sorted(set(info))) or "none"))

    # 5. Bench assembly: the real parts (no plugs) slide in with the tray, 90 mm along -X at the 2 mm lift.
    lift, travel = B.TRAY_INSTALL_LIFT, 90.0
    rows, ok = [], True
    for label, raw, (x0, y0, z0, x1, y1, z1) in [core, *comps]:
        swept = Box(x1 - x0 + travel, y1 - y0, z1 - z0 + lift).moved(Location(((x0 + x1 + travel) / 2, (y0 + y1) / 2, (z0 + z1 + lift) / 2)))
        hits = _hits(swept, parts, LATER)
        if label.endswith("_PCB"):
            hits = []  # the L-shaped core is swept by its rectangles in check_pcb09_mount.py
        ok &= not hits
        if hits:
            rows.append(f"{label}: {hits}")
    out.append(("real parts slide in with the tray", ok, "; ".join(rows) or f"{len(comps)} parts' boxes swept clear"))

    failed = 0
    for name, ok, detail in out:
        failed += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    print(f"{len(out) - failed}/{len(out)} checks pass")
    if args.output:
        args.output.write_text(json.dumps([{"check": n, "pass": bool(o), "detail": d} for n, o, d in out], indent=1) + "\n")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
