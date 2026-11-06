"""D-092: measure PCB-09's HAT-style fixing: socket stack, standoffs, screws and outline tabs.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees (about 1 min), not the head.

PCB-09 plugs onto the Pi 5 header through a Samtec SSW-120-01-T-D socket on its underside
and sits on two M2.5 x 11 mm round male-female standoffs at the Pi's header-side holes
(3 and 4). The standoffs replace the Pi's M2.5 x 6 screws there; M2.5 x 5 socket-head
screws go down through the board into them. Two outline tabs reach the holes. The vendor
Pi and Active Cooler are tested as their real solids (the standalone vendor import, as in
check_pcb09_inputs.py), the rest as built.
"""

import argparse
import importlib.util
import json
import math
from pathlib import Path

from build123d import Box, Compound, Cylinder, Location, RegularPolygon, extrude, Plane
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

import body_v1_model as B
from module_checks import _box, _hit, _leaves

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB09_MOUNT

SOCKET = dict(mpn="SSW-120-01-T-D", insulator=8.51, insertion=(3.68, 6.35))  # Samtec SSW TH catalog page
STACK_TOL = 0.05        # socket stack vs standoff height
MIN_GAP = 0.2           # tab, standoff and head to anything else
NPTH_R, WEB = 1.35, 0.5  # Ø2.7 M2.5 clearance hole; minimum FR4 web to the edge
OWN = ("C0_LINK_ADAPTER_PCB09/", "PCB09_", "C0_LINK_ADAPTER_PCB09_RESERVE", "C0_LINK_ADAPTER_TOP_ENTRY_PLUG_RESERVE",
       "C0_LINK_ADAPTER_J91_PLUG_RESERVE", "C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE")
VENDOR = "C0_RASPBERRY_PI5_EXACT_STEP"
REGION = (-20.0, 70.0, 5.0, 45.0, 85.0, 170.0)


def _vol(a, b):
    common = BRepAlgoAPI_Common(a, b)
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(common.Shape(), props)
    return props.Mass()


def _cyl(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def _hits(shape, parts, skip=()):
    bb = _box(shape)
    out = []
    for path, raw, box in parts:
        if any(s in path for s in skip) or not _hit(box, bb):
            continue
        v = _vol(raw, shape.wrapped)
        if v > 1e-6:
            out.append((path.split("/")[-1], round(v, 4)))
    return out


def _header_plastic_top(pi):
    """Top of the Pi header's plastic: the 50.8 x 5 mm solid's cross-section drops at it."""
    header = [s for s in pi.solids() if abs((_box(s)[3] - _box(s)[0]) - 50.8) < 1e-3 and abs((_box(s)[4] - _box(s)[1]) - 5.0) < 1e-3]
    assert len(header) == 1, "Pi vendor header changed; re-establish the datum"
    hb = _box(header[0])
    full = 50.8 * 5.0 * 0.02
    lo, hi = hb[2] + 0.5, hb[5] - 0.5
    for _ in range(30):
        m = (lo + hi) / 2.0
        slab = Box(60.0, 8.0, 0.02).moved(Location(((hb[0] + hb[3]) / 2.0, (hb[1] + hb[4]) / 2.0, m)))
        if _vol(header[0].wrapped, slab.wrapped) > 0.9 * full:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2.0, hb[5]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print("Building body and chassis with current droid edits...", flush=True)
    robot = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference(), entry.build_body_assembly()]), strict=False)
    reg = (REGION[0], REGION[2], REGION[4], REGION[1], REGION[3], REGION[5])
    parts, labels = [], []
    for path, node, loc in _leaves(robot):
        name = "/".join(path)
        labels.append(path[-1])
        if path[-1] == VENDOR:
            continue
        raw = node.wrapped.Moved(loc.wrapped)
        box = _box(raw)
        if _hit(box, reg):
            parts.append((name, raw, box))
    pi = B.raspberry_pi5()
    parts += [(f"PI5_VENDOR/{i}", s.wrapped, _box(s)) for i, s in enumerate(pi.solids()) if _hit(_box(s), reg)]
    get = lambda label: next(raw for p, raw, b in parts if p.endswith(label))
    out = []

    # 1. Stack: the socket on the Pi header's plastic lands where the standoffs put the board.
    plastic, tip = _header_plastic_top(pi)
    r, height, thread, bore = MNT["standoff"]
    under = B.PI_PCB_TOP_Z + height
    core = _box(get("C0_LINK_ADAPTER_PCB09_BOARD"))
    stack = plastic + SOCKET["insulator"]
    insertion = tip - plastic
    ok = (abs(stack - under) <= STACK_TOL and abs(core[2] - under) < 1e-6 and abs(core[5] - core[2] - B.PCB_THICKNESS) < 1e-6
          and SOCKET["insertion"][0] <= insertion <= SOCKET["insertion"][1])
    out.append(("socket stack meets the standoffs", ok,
                f"Pi top {B.PI_PCB_TOP_Z:.3f} + {height} = {under:.3f}; header plastic top {plastic:.3f} + {SOCKET['mpn']} "
                f"{SOCKET['insulator']} = {stack:.3f} (diff {stack - under:+.3f}); board core Z {core[2]:.3f}-{core[5]:.3f}; "
                f"pin insertion {insertion:.2f} mm in the {SOCKET['insertion'][0]}-{SOCKET['insertion'][1]} range"))

    # 2. The two header-side Pi screws are gone and the standoffs stand on their inserts.
    rows, ok = [], all(f"PI5_M25X6_SCREW_{k}" in labels for k in (1, 2))
    for k, (x, y) in MNT["holes"]:
        ins = _box(get(f"PI5_M25_INSERT_{k}"))
        sb = _box(get(f"PCB09_M25X11_ROUND_STANDOFF_{k}"))
        off = math.dist(((ins[0] + ins[3]) / 2, (ins[1] + ins[4]) / 2), ((sb[0] + sb[3]) / 2, (sb[1] + sb[4]) / 2))
        engage = min(ins[5], B.PI_PCB_TOP_Z) - max(ins[2], B.PI_PCB_TOP_Z - thread)
        gone = f"PI5_M25X6_SCREW_{k}" not in labels
        ok &= gone and off < 1e-6 and abs(sb[5] - under) < 1e-6 and engage >= 3.0
        rows.append(f"hole {k} ({x}, {y}): screw removed {gone}, standoff axis {off:.4f} off the insert, "
                    f"top Z {sb[5]:.3f}, {engage:.2f} mm of thread in the insert")
    out.append(("standoffs replace Pi screws 3 and 4", ok, "; ".join(rows)))

    # 3. Each hole has board round it: the Ø2.7 hole plus a 0.5 mm web inside the tab.
    rows, ok = [], True
    rects = [(x0, x1, y0, y1) for x0, x1, y0, y1 in MNT["tabs"]]
    for (k, (x, y)), (x0, x1, y0, y1) in zip(MNT["holes"], rects):
        web = min(x - x0, x1 - x, y - y0, y1 - y) - NPTH_R
        slab = _cyl(NPTH_R + WEB, under + 0.1, under + 1.5, x, y)
        inside = _vol(get("C0_LINK_ADAPTER_PCB09_BOARD"), slab.wrapped) / slab.volume
        ok &= web >= WEB and inside > 0.999
        rows.append(f"hole {k}: web {web:.2f} mm to the nearest tab edge, {inside * 100:.1f} % of the Ø{2 * (NPTH_R + WEB):.1f} disc on the board")
    out.append(("tabs carry the holes", ok, "; ".join(rows)))

    # 4. Tabs, standoffs and screw heads clear everything else by MIN_GAP (grown shapes).
    head_r, head_h, _ = MNT["screw"]
    over = under + B.PCB_THICKNESS
    rows, ok = [], True
    for k, (x, y) in MNT["holes"]:
        shapes = {"standoff": _cyl(r + MIN_GAP, B.PI_PCB_TOP_Z + 0.01, under - 0.01, x, y),
                  "screw head": _cyl(head_r + MIN_GAP, over + 0.01, over + head_h + MIN_GAP, x, y)}
        for what, shape in shapes.items():
            hits = _hits(shape, parts, OWN)
            ok &= not hits
            rows.append(f"hole {k} {what}: {hits or 'clear'}")
    for i, (x0, x1, y0, y1) in enumerate(MNT["tabs"], start=1):
        g = MIN_GAP
        tab = Box(x1 - x0 + 2 * g, y1 - y0 + 2 * g, B.PCB_THICKNESS + 2 * g).moved(
            Location(((x0 + x1) / 2, (y0 + y1) / 2, under + B.PCB_THICKNESS / 2)))
        hits = _hits(tab, parts, OWN + ("PCB09_M25",))
        ok &= not hits
        rows.append(f"tab {i} grown {g} mm: {hits or 'clear'}")
    out.append((f"mount clears its neighbours by {MIN_GAP} mm", ok, "; ".join(rows)))

    # 5. Planted cases: a 5 mm A/F hex standoff at hole 4 and the +X tab at the bridge's Y 16.3 hit the cooler.
    x, y = dict(MNT["holes"])[4]
    hexa = extrude(RegularPolygon(5.0 / math.sqrt(3.0), 6, rotation=90),  # a corner toward the cooler
                   height - 0.02).moved(Location((x, y, B.PI_PCB_TOP_Z + 0.01)))
    x0, x1, _, y1 = MNT["tabs"][1]
    low = Box(x1 - x0, y1 - 16.3, B.PCB_THICKNESS).moved(Location(((x0 + x1) / 2, (16.3 + y1) / 2, under + B.PCB_THICKNESS / 2)))
    a, b = _hits(hexa, parts, OWN), _hits(low, parts, OWN + ("PCB09_M25",))
    ok = any("COOLER" in n for n, v in a) and any("COOLER" in n for n, v in b)
    out.append(("planted cases fail", ok, f"hex standoff at hole 4: {a}; +X tab down to Y 16.3: {b}"))

    # 6. Bench assembly: PCB-09 is screwed to the standoffs with the Pi on the tray, before the tray
    # goes in (the frame's cross rail is 15.4 mm over hole 4's screw head: no driver fits). The
    # unit then slides in along -X from 90 mm out, 2 mm high (D-042), and drops. Each PCB-09 part
    # sweeps as its box over the whole path; the parts that go in later are left out, as in
    # check_compute_mount.py. Until the KiCad board replaces the placeholder, two envelopes stand
    # for its parts: top side to 7.0 mm (above the GH headers' 4.25 mm), underside to the SOIC's 1.75 mm.
    lift, travel = B.TRAY_INSTALL_LIFT, 90.0
    wx0, wx1, wy0, wy1 = 36.0, 66.0, 22.5, 39.0
    ex0, ex1, ey0, ey1 = MNT["bay_extension"]
    movers = [(p.split("/")[-1], _box(raw)) for p, raw, box in parts
              if ("C0_LINK_ADAPTER_PCB09/" in p or "PCB09_M25" in p) and "MATED_PLUG" not in p
              and not p.endswith("C0_LINK_ADAPTER_PCB09_BOARD")]
    # The board is an L: sweep its rectangles, not its bounding box.
    rects = [(-4.7, 36.0, 16.3, 22.4), (36.0, 47.1, 16.3, 22.5), (wx0, wx1, wy0, wy1), *MNT["tabs"], MNT["bay_extension"]]
    movers += [(f"BOARD_RECT_{i}", (x0, y0, under, x1, y1, over)) for i, (x0, x1, y0, y1) in enumerate(rects, start=1)]
    movers += [("TOP_PARTS_ENVELOPE", (ex0, wy0, over, wx1, wy1, over + 7.0)),
               ("UNDERSIDE_PARTS_ENVELOPE", (ex0, wy0, under - 1.75, wx1, wy1, under))]
    later = ("C3_", "BODY_FRAME_C3_", "HARNESS_", "SPEAKER_", "PCB05_", "RESERVE", "KEEP_OUT", "PLUG",
             "COMPUTE_TRAY", "PI5_", "PI5_VENDOR/", "C0_LINK_ADAPTER", "PCB09_")
    rows, ok = [], True
    for name, (x0, y0, z0, x1, y1, z1) in movers:
        swept = Box(x1 - x0 + travel, y1 - y0, z1 - z0 + lift).moved(
            Location(((x0 + x1 + travel) / 2, (y0 + y1) / 2, (z0 + z1 + lift) / 2)))
        hits = _hits(swept, parts, later)
        ok &= not hits
        if hits:
            rows.append(f"{name}: {hits}")
    out.append(("bench-assembled unit slides in", ok, f"{len(movers)} PCB-09 boxes swept +{travel:.0f} mm X, "
                f"{lift} mm lift: " + ("; ".join(rows) or "clear")))

    # 7. Driver column above each screw in place (information for service: what must come off first).
    rows = []
    for k, (x, y) in MNT["holes"]:
        column = _cyl(2.5, over + head_h + 0.05, REGION[5], x, y)
        bb = _box(column)
        hits = []
        for path, raw, box in parts:
            if any(s in path for s in OWN) or not _hit(box, bb):
                continue
            if _vol(raw, column.wrapped) > 1e-6:
                hits.append((round(_box(BRepAlgoAPI_Common(raw, column.wrapped).Shape())[2], 2), path.split("/")[-1]))
        rows.append(f"hole {k}: {sorted(hits) or 'open to Z %.0f' % REGION[5]}")
    out.append(("driver column above each screw (information)", True, "; ".join(rows)))

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
