"""PCB-05 rev A fit: place the KiCad board STEP where the droid CAD has the board and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees with the droid edits (about 1 min), not the head.

KiCad's STEP has (X, Y) = (KiCad x, -y), the core at Z 0..1.516 (35 um copper and about 7 um
of mask each side make the 1.6 mm board) and parts 0.085 above the core. World X = x - 55,
Y = 119 - y (04-pcbs/pcb-05-audio-front-end/README.md), and the board's top face is Z 115.6
(PCB05_MOUNT), so the core's underside lands at Z 114.042. The vendor Pi and cooler leaves
are tested as their boxes. check_pcb05_mount.py owns the fixing (bosses, bores, screws); this
script owns the real parts.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, import_step

from check_pcb05_mount import LATER, VENDOR, _box, _hit, _leaves

HERE = Path(__file__).resolve().parent
BOARD_STEP = HERE.parents[2] / "04-pcbs/pcb-05-audio-front-end/cad/pcb-05-audio-front-end-revA.step"
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB05_MOUNT

BOARD = 1.6
CORE = 1.516
PLACE = Location((-55.0, 119.0, MNT["board_top"] - BOARD + (BOARD - CORE) / 2.0))
MIN_GAP = 0.3
REGION = (20.0, 130.0, -45.0, 45.0, 95.0, 230.0)
# Connector models (footprint name) and the CAD header each one stands for, found by position.
CONN = ("JST_GH_", "Molex_Micro-Fit")
SPACER = "Mounting_Wuerth"


def gap_or_distance(a, a_box, s, s_box, near=0.5):
    """Box gap (a lower bound) when it is already large; exact distance only when it is small."""
    g = max(s_box[0] - a_box[3], a_box[0] - s_box[3], s_box[1] - a_box[4], a_box[1] - s_box[4],
            s_box[2] - a_box[5], a_box[2] - s_box[5], 0.0)
    if s is None or g >= near:
        return g
    return a.distance(s)


def main():
    import time
    t0 = time.time()
    log = lambda msg: print(f"... {msg} ({time.time() - t0:.0f} s)", flush=True)
    robot = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference(), entry.build_body_assembly()]), strict=False)
    reg = (REGION[0], REGION[2], REGION[4], REGION[1], REGION[3], REGION[5])
    parts = []
    for path, node, loc in _leaves(robot):
        box = _box(node.wrapped.Moved(loc.wrapped))
        if _hit(box, reg):
            vendor = any(v in path[-1] for v in VENDOR)
            parts.append(("/".join(path[1:]), None if vendor else node.moved(loc), box))
    near_frame = next(s for p, s, b in parts if p.endswith("BODY_FRAME_MAIN_PRINT")) & entry._cut_box(20.0, 130.0, -45.0, 45.0, 100.0, 140.0)
    parts = [(p, near_frame if p.endswith("BODY_FRAME_MAIN_PRINT") else s, b) for p, s, b in parts]
    log(f"droid built, {len(parts)} parts near the board")
    cad = {p.split("/")[-1]: (s, b) for p, s, b in parts if "PCB05_" in p}
    others = [(p, s, b) for p, s, b in parts if "PCB05_" not in p]

    step = import_step(str(BOARD_STEP))
    real = []
    for c in step.children:
        if c.solids():
            shape = Compound(c.solids()).moved(PLACE)
            real.append((c.label, shape, _box(shape)))
    core = next((l, s, b) for l, s, b in real if l.endswith("_PCB"))
    comps = [(l, s, b) for l, s, b in real if not l.endswith("_PCB")]
    log(f"board STEP: core and {len(comps)} parts")
    out = []

    # 1. The core is the CAD board: same outline, top face at Z 115.6 (to the copper and mask).
    cb, pb = core[2], cad["PCB05_AUDIO_FRONT_END_PCB"][1]
    d = [cb[i] - pb[i] for i in (0, 1, 3, 4)]
    top = cb[5] + (BOARD - CORE) / 2.0
    out.append(("board on the CAD board", max(map(abs, d)) < 0.01 and abs(top - MNT["board_top"]) < 0.01,
                f"core X {cb[0]:.2f}..{cb[3]:.2f}, Y {cb[1]:.2f}..{cb[4]:.2f} (offsets {max(map(abs, d)):.3f}); top face Z {top:.3f}"))

    # 2. Spacers on the D-067 points (amended at placement) and up to the boss undersides.
    sp = sorted(((b[0] + b[3]) / 2.0, (b[1] + b[4]) / 2.0, b[5]) for l, s, b in comps if l.startswith(SPACER))
    rows, ok = [], len(sp) == len(MNT["points"])
    for (x, y) in MNT["points"]:
        best = min(sp, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)
        off = ((best[0] - x) ** 2 + (best[1] - y) ** 2) ** 0.5
        ok &= off < 0.01 and abs(best[2] - (MNT["board_top"] + MNT["spacer"][2])) < 0.1
        rows.append(f"({x}, {y}) off {off:.3f}, top Z {best[2]:.3f}")
    out.append(("spacers on the fixing points", ok, "; ".join(rows) + " (KiCad sets parts 0.04 proud of the copper)"))

    # 3. Connectors against the CAD headers: the same side span, and the mating face at or inside
    #    the CAD face, so plug and lead stay within the CAD's plug and edge reserves.
    headers = {k: b for k, (s, b) in cad.items() if k.endswith("_HEADER")}
    rows, ok = [], True
    for l, s, b in comps:
        if not l.startswith(CONN):
            continue
        c = ((b[0] + b[3]) / 2.0, (b[1] + b[4]) / 2.0)
        name, h = min(headers.items(), key=lambda kv: ((kv[1][0] + kv[1][3]) / 2.0 - c[0]) ** 2 + ((kv[1][1] + kv[1][4]) / 2.0 - c[1]) ** 2)
        if h[0] <= 45.0 + 0.01:            # J5-1, mates -X
            face, cad_face, span = b[0] - h[0], 0.0, ((b[1] + b[4]) - (h[1] + h[4])) / 2.0
        elif h[4] >= 19.0 - 0.01:          # +Y edge
            face, cad_face, span = h[4] - b[4], 0.0, ((b[0] + b[3]) - (h[0] + h[3])) / 2.0
        else:                              # -Y edge
            face, cad_face, span = b[1] - h[1], 0.0, ((b[0] + b[3]) - (h[0] + h[3])) / 2.0
        ok &= -0.01 <= face <= 1.0 and abs(span) <= 0.3
        rows.append(f"{name.split('_')[1]}_{name.split('_')[2]}: face {face:.2f} inside the CAD face, centre {span:+.2f} along the edge")
    out.append(("connectors on the CAD headers", ok, "; ".join(sorted(rows))))

    # 4. The parts (not spacers or connectors) inside the CAD's parts reserve.
    rb = cad["PCB05_AUDIO_FRONT_END_PARTS_RESERVE"][1]
    tall = max((b[5], l) for l, s, b in comps if not l.startswith(CONN + (SPACER,)))
    out_ = [l for l, s, b in comps if not l.startswith(CONN + (SPACER,)) and
            (b[0] < rb[0] - 0.01 or b[3] > rb[3] + 0.01 or b[1] < rb[1] - 0.01 or b[4] > rb[4] + 0.01 or b[5] > rb[5] + 0.01)]
    out.append(("parts inside the CAD reserve", not out_,
                f"tallest {tall[1]} to Z {tall[0]:.2f} against the reserve's {rb[5]:.2f}" + (f"; outside {out_}" if out_ else "")))
    log("4.")

    # 5. Every real part clear of every other part of the droid (the shell, cartridge and panels too).
    #    Spacer tops meet the frame bosses by design (check_pcb05_mount.py).
    rows, worst, below = [], [], []
    for l, s, b in [core, *comps]:
        best = (99.0, "")
        for p, o, ob in others:
            if not _hit(b, ob, 3.0):
                continue
            if l.startswith(SPACER) and p.endswith("BODY_FRAME_MAIN_PRINT"):
                continue
            d = gap_or_distance(s, b, o, ob)
            if d < best[0]:
                best = (d, p.split("/")[-1])
        worst.append((best[0], l, best[1]))
        # Below the board: the core's underside, and only what pokes through it (J7's clipped tails and peg).
        bottom = MNT["board_top"] - BOARD
        if l.endswith("_PCB"):
            below.append((best[0], l, best[1]))
        elif b[2] < bottom - 0.01:
            low = s & entry._cut_box(b[0] - 1.0, b[3] + 1.0, b[1] - 1.0, b[4] + 1.0, b[2] - 1.0, bottom)
            lb = _box(low)
            d = min(((gap_or_distance(low, lb, o, ob), p.split("/")[-1]) for p, o, ob in others if _hit(lb, ob, 3.0)),
                    default=(99.0, "nothing within 3 mm"))
            below.append((d[0], f"{l} below the board", d[1]))
    worst.sort()
    reserves = [w for w in worst if "RESERVE" in w[2] or "KEEP_OUT" in w[2]]
    solid = [w for w in worst if w not in reserves]
    out.append(("parts clear of the droid", solid[0][0] >= MIN_GAP,
                "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in solid[:4])))
    out.append(("parts clear of the other reserves", not reserves or reserves[0][0] >= 0.0 + 1e-6,
                "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in reserves[:3]) or "none within 3 mm"))
    out.append(("under the board", min(below)[0] >= 0.5,   # decision H's margin over the USB jacks
                "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in sorted(below)[:3])))
    log("5.")

    # 6. Install path with the real parts: from 40 mm in front, 1 mm low, then up (as the mount check).
    fixed = [(p, s, b) for p, s, b in others if not any(t in p for t in LATER) and "RESERVE" not in p and "KEEP_OUT" not in p]
    movers = [core, *comps]
    best, hits = (99.0, ""), []
    for dx, dz in [(dx, -1.0) for dx in range(40, -1, -2)] + [(0, -0.5)]:
        for l, s, b in movers:
            mb = (b[0] + dx, b[1], b[2] + dz, b[3] + dx, b[4], b[5] + dz)
            moved = None
            for p, o, ob in fixed:
                if not _hit(mb, ob, 2.0):
                    continue
                g = gap_or_distance(None, mb, None, ob)
                if g < 0.5 and o is not None:
                    moved = moved or s.moved(Location((dx, 0, dz)))
                    g = moved.distance(o)
                if g < best[0]:
                    best = (g, f"{l} at +{dx}, dz {dz} to {p.split('/')[-1]}")
                if g < 1e-6:
                    hits.append(best[1])
    out.append(("slides in from the front, 1 mm low", not hits and best[0] >= 0.2,
                f"nearest {best[1]} {best[0]:.2f}" + (f"; hits {sorted(set(hits))[:4]}" if hits else "")))

    allok = True
    for name, passed, detail in out:
        allok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
