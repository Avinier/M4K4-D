"""D-067: measure the PCB-05 fixing that DROID_CUTS/ADDS make: spacers, frame bosses, bores, screws.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees (about 1 min), not the head.

PCB-05 hangs from the frame on three 8 mm M2 SMT spacers (Wurth 9774080243R) reflowed on
its top face. ISO 7380 M2 screws go down from above through the front upper cross rail
(two, into counterbores under the yaw housing seat) and the yaw plate (one). The board
goes in after the compute tray and PCB-09: it slides in from the front 1 mm low, over the
Pi's USB jacks, then lifts onto the bosses. The yaw cartridge, shell, panels, speaker and
head come later. The vendor Pi and cooler leaves are tested as their boxes.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Cylinder, Location
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

import body_v1_model as B

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB05_MOUNT

VENDOR = ("C0_RASPBERRY_PI5_EXACT_STEP", "PI5_ACTIVE_COOLER_STEP")
LATER = ("BODY_SHELL", "BODY_PANELS", "PANEL_MOUNT_HARDWARE", "SPEAKER_", "BODY_YAW_STAGE", "YAW_", "HARNESS_",
         "PDM_MIC_", "WHEEL_ARCH")
OWN = ("PCB05_",)
HEAD = (3.5 / 2.0, 1.1)        # ISO 7380 M2: dk 3.5, k 1.1
SHANK = 1.0
TOOL_R = {"rear": 1.5, "front": 2.5}  # 1.3 mm hex key in a Ø3 sweep; Ø5 over the open plate
PAD_R = 5.3 / 2.0              # Wurth suggested solder ring
MIN_GAP = 0.3
REGION = (20.0, 130.0, -45.0, 45.0, 95.0, 230.0)  # board, its 40 mm install slide and the driver paths


def _box(shape):
    b = Bnd_Box()
    BRepBndLib.Add_s(shape.wrapped if hasattr(shape, "wrapped") else shape, b, False)
    return b.Get()


def _hit(a, b, pad=0.0):
    return not (a[3] + pad <= b[0] or b[3] + pad <= a[0] or a[4] + pad <= b[1] or
                b[4] + pad <= a[1] or a[5] + pad <= b[2] or b[5] + pad <= a[2])


def _leaves(node, loc=Location(), path=()):
    here = loc * node.location
    kids = list(node.children) if getattr(node, "children", None) else []
    name = path + (node.label or "?",)
    if not kids or any(v in (node.label or "") for v in VENDOR):
        yield name, node, loc
        return
    for kid in kids:
        yield from _leaves(kid, here, name)


def _cyl(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def _vol(shape):
    return sum(s.volume for s in shape.solids()) if shape is not None else 0.0


def main():
    import time
    t0 = time.time()
    log = lambda msg: print(f"... {msg} ({time.time() - t0:.0f} s)", flush=True)
    before = Compound(children=[entry.chassis_v1_reference(), entry.build_body_assembly()])
    log("built")
    frame0 = next(n.moved(l) for p, n, l in _leaves(before) if p[-1] == "BODY_FRAME_MAIN_PRINT")
    robot = entry._apply_droid_cuts(before, strict=False)
    log("droid edits applied")
    parts = []   # (label path, shape or None for vendor, box); only parts whose box meets REGION
    reg = (REGION[0], REGION[2], REGION[4], REGION[1], REGION[3], REGION[5])
    for path, node, loc in _leaves(robot):
        vendor = any(v in path[-1] for v in VENDOR)
        box = _box(node.wrapped.Moved(loc.wrapped))
        if _hit(box, reg):
            parts.append(("/".join(path[1:]), None if vendor else node.moved(loc), box))
    log(f"{len(parts)} parts near the board")
    get = lambda label: next(s for p, s, b in parts if p.endswith(label))
    frame, pcb = get("BODY_FRAME_MAIN_PRINT"), get("PCB05_AUDIO_FRONT_END_PCB")
    # Distance queries against the whole frame print are slow; the sweeps use its piece near the board.
    near_frame = frame & entry._cut_box(20.0, 130.0, -45.0, 45.0, 100.0, 140.0)
    parts = [(p, near_frame if p.endswith("BODY_FRAME_MAIN_PRINT") and s is not None else s, b) for p, s, b in parts]
    housing = get("YAW_CARTRIDGE_HOUSING")
    top = MNT["board_top"] + MNT["spacer"][2]
    out = []

    # 1. The bosses join the frame print, which stays one solid. Volumes are compared in a
    # Ø10 zone round each point (the whole print's volume integral is too coarse), with the
    # cuts fused first so a bore and its counterbore are not counted twice.
    rows, ok = [], len(frame.solids()) == len(frame0.solids()) == 1
    cuts = entry._PCB05_CUTS[0].fuse(*entry._PCB05_CUTS[1:])
    for i, ((x, y), roof) in enumerate(zip(MNT["points"], MNT["boss"][1])):
        zone = _cyl(5.0, MNT["board_top"], 145.0, x, y)
        grow = _vol(frame & zone) - _vol(frame0 & zone)
        boss = _vol(_cyl(MNT["boss"][0], top, roof, x, y) - _cyl(MNT["bore"], top - 0.1, roof + 0.1, x, y))
        cut = _vol(frame0 & cuts & zone)
        ok &= abs(grow - (boss - cut)) < 0.05
        rows.append(f"P{i + 1}: {grow:+.2f} mm3 = boss {boss:.2f} - cut {cut:.2f}")
    out.append(("bosses fused to the frame", ok, f"frame solids {len(frame0.solids())} -> {len(frame.solids())}; " + "; ".join(rows)))

    log('2.')
    # 2. Each bore is open and has at least 1 mm of print round it, bottom of the boss to the head seat.
    rows, ok = [], True
    for i, ((x, y), seat) in enumerate(zip(MNT["points"], (s for _, s in MNT["screws"]))):
        open_ = _vol(frame & _cyl(MNT["bore"] - 0.01, top, seat, x, y))
        ring = _cyl(MNT["bore"] + 1.0, top + 0.05, seat - 0.05, x, y) - _cyl(MNT["bore"], top, seat, x, y)
        missing = ring.volume - _vol(ring & frame)
        ok &= open_ < 1e-3 and missing < 0.05
        rows.append(f"P{i + 1} ({x}, {y}): print in bore {open_:.3f} mm3, missing from the 1 mm wall {missing:.3f} mm3, "
                    f"length {seat - top:.1f}")
    out.append(("bores open, 1 mm walls", ok, "; ".join(rows)))

    log('3.')
    # 3. Screws: heads seated, rear heads under the housing seat, thread engagement in the spacer.
    rows, ok = [], True
    for i, ((x, y), (length, seat)) in enumerate(zip(MNT["points"], MNT["screws"])):
        head = _cyl(HEAD[0], seat, seat + HEAD[1], x, y)
        tip = seat - length
        engage = top - max(tip, MNT["board_top"])
        ok &= engage >= 3.0 and tip > MNT["board_top"] and _vol(head & frame) < 1e-3
        line = f"P{i + 1}: M2 x {length:.0f}, head Z {seat:.1f}-{seat + HEAD[1]:.1f}, tip Z {tip:.1f}, {engage:.1f} mm in the spacer"
        if i < 2:
            gap = head.distance(housing)
            r = ((x - B.BODY_AXIS_X) ** 2 + y ** 2) ** 0.5 + MNT["cbore"][0]
            seat_r = B.YAW_PLATE_POCKET[0]
            ok &= gap >= MIN_GAP and r <= seat_r - 0.2
            line += f", {gap:.2f} under the yaw housing; counterbore edge R{r:.2f} inside the R{seat_r} seat"
        rows.append(line)
    out.append(("screws seated and engaged", ok, "; ".join(rows)))

    log('4.')
    # 4. Spacers and their solder rings clear of the edge connectors on the board.
    conns = [(p, s) for p, s, b in parts if "PCB05_J5_" in p and "PLUG" not in p]
    rows, ok = [], True
    for i, (x, y) in enumerate(MNT["points"]):
        body = _cyl(MNT["spacer"][0], MNT["board_top"], top, x, y)
        pad = _cyl(PAD_R, MNT["board_top"], MNT["board_top"] + 0.05, x, y)
        d_body = min((body.distance(s), p.split("/")[-1]) for p, s in conns)
        d_pad = min((pad.distance(s), p.split("/")[-1]) for p, s in conns)
        ok &= d_body[0] >= MIN_GAP and d_pad[0] >= 0.2
        rows.append(f"P{i + 1}: spacer {d_body[0]:.2f} to {d_body[1]}, Ø5.3 ring {d_pad[0]:.2f} to {d_pad[1]}")
    out.append(("spacers clear of the J5 connectors", ok, "; ".join(rows)))

    log('5.')
    # 5. Spacers, bosses and screws clear of every other part (the board's own parts excepted).
    hardware = []
    for i, ((x, y), roof, (length, seat)) in enumerate(zip(MNT["points"], MNT["boss"][1], MNT["screws"])):
        hardware += [(f"P{i + 1} spacer", _cyl(MNT["spacer"][0], MNT["board_top"], top, x, y)),
                     (f"P{i + 1} boss", _cyl(MNT["boss"][0], top, roof - 0.01, x, y)),
                     (f"P{i + 1} screw head", _cyl(HEAD[0], seat, seat + HEAD[1], x, y))]
    rows, worst = [], (99.0, "")
    for name, h in hardware:
        hb = _box(h)
        for p, s, b in parts:
            if any(o in p for o in OWN) or p.endswith("BODY_FRAME_MAIN_PRINT") or not _hit(hb, b, 3.0):
                continue
            if "RESERVE" in p or "KEEP_OUT" in p:
                continue
            d = (max(b[0] - hb[3], hb[0] - b[3], b[1] - hb[4], hb[1] - b[4], b[2] - hb[5], hb[2] - b[5], 0.0)
                 if s is None else h.distance(s))
            if d < worst[0]:
                worst = (d, f"{name} to {p.split('/')[-1]}")
    out.append(("fixings clear of other parts", worst[0] >= MIN_GAP, f"nearest {worst[1]} {worst[0]:.2f}"))

    log('6.')
    # 6. Install path: board, spacers and J5 headers from 40 mm in front, 1 mm low, then up 1 mm.
    movers = [pcb] + [s for p, s in conns]
    fixed = [(p, s, b) for p, s, b in parts if not any(t in p for t in LATER + OWN)
             and "RESERVE" not in p and "KEEP_OUT" not in p]
    worst, hits = (99.0, ""), []
    steps = [(dx, -1.0) for dx in range(40, -1, -2)] + [(0, -0.5)]
    for dx, dz in steps:
        for m in movers:
            mm = m.moved(Location((dx, 0, dz)))
            mb = _box(mm)
            for p, s, b in fixed:
                if not _hit(mb, b, 2.0):
                    continue
                if s is None:
                    d = max(b[0] - mb[3], mb[0] - b[3], b[1] - mb[4], mb[1] - b[4], b[2] - mb[5], mb[2] - b[5], 0.0)
                else:
                    d = mm.distance(s)
                if d < worst[0]:
                    worst = (d, f"+{dx} mm, dz {dz}: {p.split('/')[-1]}")
                if d < 1e-6:
                    hits.append(worst[1])
    out.append(("slides in from the front, 1 mm low", not hits and worst[0] >= 0.2,
                f"nearest {worst[1]} {worst[0]:.2f}" + (f"; hits {sorted(set(hits))[:4]}" if hits else "")))

    log('7.')
    # 7. Driver paths from above at install time (no yaw cartridge, shell or head yet).
    rows, ok = [], True
    for i, ((x, y), (length, seat)) in enumerate(zip(MNT["points"], MNT["screws"])):
        r = TOOL_R["rear" if i < 2 else "front"]
        path = _cyl(r, seat + HEAD[1], 220.0, x, y)
        pb = _box(path)
        near = min(((path.distance(s) if s is not None else 0.0), p.split("/")[-1])
                   for p, s, b in fixed if _hit(pb, b, 1.0)) if any(_hit(pb, b, 1.0) for p, s, b in fixed) else (99.0, "none")
        later = sorted({p.split("/")[-1] for p, s, b in parts if any(t in p for t in LATER) and _hit(pb, b)
                        and (s is None or path.distance(s) < 1e-6)})
        ok &= near[0] >= 0.2
        rows.append(f"P{i + 1} Ø{2 * r:.0f}: nearest {near[1]} {near[0]:.2f}; covered later by {later or 'nothing in the body'}")
    out.append(("driver paths open from above", ok, "; ".join(rows)))

    allok = True
    for name, passed, detail in out:
        allok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
