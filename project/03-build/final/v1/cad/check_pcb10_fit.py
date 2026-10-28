"""PCB-10 rev A fit: place the KiCad board STEP where the droid CAD has the C3 carrier and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees with the droid edits (about 3 min), not the head.

KiCad's STEP (exported with --user-origin 0x0mm) has (Xs, Ys) = (KiCad x, -y), the core at
Zs 0..core and parts about 0.04 mm proud of the copper. The board is seen from its F face, the
DevKitC side, which faces world +Y (04-pcbs/pcb-10-c3-carrier/README.md, Board set-up):
world X = 156 - Xs, Z = 225.5 + Ys, Y = Zs + the core's underside (the board's B face at Y -58.4).
check_pcb10_mount.py owns the fixing (uprights, hooks, reliefs, screws, the CAD DevKitC); this
script owns the real parts. The vendor Pi and cooler are tested as their boxes.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, import_step
from OCP.gp import gp_Trsf
from OCP.TopLoc import TopLoc_Location

from check_pcb10_mount import CARRIER, RESERVE, UPRIGHT, VENDOR, _blk, _box, _hit, _leaves, _place, _vol

HERE = Path(__file__).resolve().parent
BOARD_STEP = HERE.parents[2] / "04-pcbs/pcb-10-c3-carrier/cad/pcb-10-c3-carrier-revA.step"
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB10_MOUNT

BOARD = 1.6
MIN_GAP = 0.3
REGION = (-45.0, 80.0, -80.0, -25.0, 60.0, 140.0)
DEVKITC = "ESP32-S3-DevKitC-1_v1"                 # KiCad writes the model name with "_" for "."
CONN = ("JST_GH_", "Molex_Micro-Fit")
# Datasheet maximum heights above the board face (mm) for parts under the DevKitC (D-068 B: <= 2.0).
# The DevKitC's underside is 2.5 mm up (its header plastic).
MAX_H = {"TSOT-23-8": 1.10,                 # TPS3436 DDF0008A, TI 4222047/E: 1.1 max (model 0.95)
         "SOT-23-6": 1.45, "SOT-23-5": 1.45,  # 74LVC1G11 / 74LVC1G08 DBV, TI: 1.45 max
         "SOT-23": 1.45,                     # AO3400A: 1.45 max (AOS SOT-23 outline)
         "C_0805": 1.45, "C_0402": 0.55, "R_0402": 0.40, "R_0603": 0.55, "D_SOD-123": 1.35}
SHADOW_LIMIT = 2.0
# Holes KiCad cuts from the core (the CAD board has none): DevKitC 44 x 1.0, JP1 2 x 0.8, Micro-Fit
# 2 x 1.02 and its 3.0 peg, the two 2.7 screw holes. Vias are not cut.
HOLES = 3.14159265 / 4.0 * (44 * 1.0 ** 2 + 2 * 0.8 ** 2 + 2 * 1.02 ** 2 + 3.0 ** 2 + 2 * 2.7 ** 2)


def _gap(a, a_box, s, s_box, near=0.5):
    """Box gap (a lower bound) when it is already large; exact distance only when it is small."""
    g = max(s_box[0] - a_box[3], a_box[0] - s_box[3], s_box[1] - a_box[4], a_box[1] - s_box[4],
            s_box[2] - a_box[5], a_box[2] - s_box[5], 0.0)
    if s is None or g >= near:
        return g
    return a.distance(s)


def board_parts():
    """The STEP's core and parts, moved into the world: [(label, shape, box)]."""
    step = import_step(str(BOARD_STEP))
    raw = [(c.label, Compound(c.solids())) for c in step.children if c.solids()]
    core_box = _box(next(s for l, s in raw if l.endswith("_PCB")))
    core = core_box[5] - core_box[2]
    t = gp_Trsf()
    #           X = 156 - Xs                Y = Zs + core underside                        Z = 225.5 + Ys
    t.SetValues(-1, 0, 0, 156.0, 0, 0, 1, MNT["board"][2] + (BOARD - core) / 2.0 - core_box[2], 0, 1, 0, 225.5)
    loc = TopLoc_Location(t)
    out = []
    for l, s in raw:
        m = Compound(s.wrapped.Moved(loc))
        out.append((l, m, _box(m)))
    return out, core


def main():
    import time
    t0 = time.time()
    log = lambda msg: print(f"... {msg} ({time.time() - t0:.0f} s)", flush=True)
    tree = entry._apply_droid_cuts(Compound(children=[entry.build_body_assembly(), entry.chassis_v1_reference()]), strict=False)
    reg = (*REGION[0::2], *REGION[1::2])
    every = [(path, _place(node, loc)) for path, node, loc in _leaves(tree)
             if node.wrapped is not None and not node.wrapped.IsNull()]
    near = []
    for p, s in every:
        b = _box(s)
        if _hit(b, reg):
            if any(v in "/".join(p) for v in VENDOR):
                s = _blk(b)
            near.append((p, s, b))
    own = {p[-1]: (s, b) for p, s, b in near if CARRIER in "/".join(p)}
    others = [(p[-1], s, b) for p, s, b in near if CARRIER not in "/".join(p)]
    # The frame is one big print: keep only its part near the board, so distances stay quick.
    others = [(l, s & entry._cut_box(*REGION) if l.endswith("BODY_FRAME_MAIN_PRINT") else s, b) for l, s, b in others]
    others = [(l, s, _box(s)) for l, s, b in others]
    log(f"droid built: {len(own)} carrier parts, {len(others)} others near the board")

    real, core_t = board_parts()
    core = next(r for r in real if r[0].endswith("_PCB"))
    comps = [r for r in real if not r[0].endswith("_PCB")]
    log(f"board STEP: core {core_t:.3f} mm and {len(comps)} parts")
    face = MNT["board"][3]                         # F face, world Y
    out = []

    # 1. The core is the CAD board (grown and notched, D-068 amended): same outline box and faces.
    cb, pb = core[2], own["C3_CARRIER_PCB10_BOARD"][1]
    d = max(abs(cb[i] - pb[i]) for i in (0, 2, 3, 5))
    top = cb[4] + (BOARD - core_t) / 2.0
    vol = _vol(core[1]) / core_t, _vol(own["C3_CARRIER_PCB10_BOARD"][0]) / BOARD
    out.append(("board on the CAD board", d < 0.01 and abs(top - face) < 0.01 and abs(vol[0] + HOLES - vol[1]) < 0.5,
                f"core X {cb[0]:.2f}..{cb[3]:.2f}, Z {cb[2]:.2f}..{cb[5]:.2f} (offset {d:.3f}); F face Y {top:.3f}; "
                f"area {vol[0]:.1f} + {HOLES:.1f} of holes against the CAD's {vol[1]:.1f} mm2 (notched)"))

    # 2. The DevKitC model is the CAD's DevKitC (both from pcb10_devkitc()), parts lifted by KiCad's offset only.
    dk = [r for r in comps if r[0].startswith(DEVKITC)]
    rows, ok = [], len(dk) == 1
    if dk:
        db = dk[0][2]
        cad_parts = [b for l, (s, b) in own.items() if l.startswith("C3_DEVKITC_V11_") and "PINS" not in l]
        cad = (min(b[0] for b in cad_parts), min(b[1] for b in cad_parts), min(b[2] for b in cad_parts),
               max(b[3] for b in cad_parts), max(b[4] for b in cad_parts), max(b[5] for b in cad_parts))
        lift = db[4] - cad[4]
        off = max(abs(db[i] - cad[i]) for i in (0, 2, 3, 5))
        ok &= off < 0.01 and 0.0 <= lift < 0.1
        rows.append(f"X {db[0]:.2f}..{db[3]:.2f}, Z {db[2]:.2f}..{db[5]:.2f} (offset {off:.3f}), top Y {db[4]:.2f}, "
                    f"{lift:+.3f} above the CAD's (KiCad's part offset); pin tails to Y {db[1]:.2f}")
    out.append(("DevKitC on the CAD DevKitC", ok, "; ".join(rows) or "no DevKitC model in the STEP"))

    # 3. Connectors on the CAD headers (PCB10_GH, PCB10_J10_1): centre within 0.3 mm, top within 0.5 mm.
    heads = {l: b for l, (s, b) in own.items() if l.endswith("_HEADER") and l.startswith("C3_J10_")}
    rows, ok, used = [], True, set()
    for l, s, b in sorted(comps, key=lambda r: r[2][0]):
        if not l.startswith(CONN):
            continue
        c = ((b[0] + b[3]) / 2.0, (b[2] + b[5]) / 2.0)
        name, h = min(heads.items(), key=lambda kv: ((kv[1][0] + kv[1][3]) / 2.0 - c[0]) ** 2 + ((kv[1][2] + kv[1][5]) / 2.0 - c[1]) ** 2)
        used.add(name)
        dx, dz = c[0] - (h[0] + h[3]) / 2.0, c[1] - (h[2] + h[5]) / 2.0
        if "Micro-Fit" in l:                        # mates +X: the mating face and its height off the board
            dx, dtop = b[3] - h[3], b[4] - h[4]
            ok &= -0.5 <= dx <= 0.01 and abs(dz) <= 0.3 and abs(dtop) <= 0.5
        else:
            dtop = b[4] - h[4]
            ok &= abs(dx) <= 0.3 and abs(dz) <= 0.3 and abs(dtop) <= 0.5
        rows.append(f"{name.split('_')[1]}-{name.split('_')[2]} {dx:+.2f}/{dz:+.2f}, top {dtop:+.2f}")
    ok &= used == set(heads)
    out.append(("connectors on the CAD headers", ok, "; ".join(rows) + (f"; unmatched {sorted(set(heads) - used)}" if used != set(heads) else "")))

    # 4. Under the DevKitC: every part's datasheet maximum <= 2.0 mm (D-068 B) and its model clear of the DevKitC.
    shadow = (db[0], db[2], db[3], db[5]) if dk else None
    rows, ok, worst = [], bool(dk), []
    dkshape = dk[0][1] if dk else None
    for l, s, b in comps:
        if l.startswith((DEVKITC,) + CONN) or not shadow:
            continue
        if b[3] <= shadow[0] or b[0] >= shadow[2] or b[5] <= shadow[1] or b[2] >= shadow[3]:
            continue
        key = next((k for k in MAX_H if l.startswith(k)), None)
        h_model = b[4] - face
        h_max = MAX_H.get(key, h_model)
        worst.append((h_max, h_model, l))
        ok &= key is not None and h_max <= SHADOW_LIMIT and h_model <= SHADOW_LIMIT
    worst.sort(reverse=True)
    gap = min(_gap(s, b, dkshape, dk[0][2], near=1.0) for l, s, b in comps if not l.startswith((DEVKITC,) + CONN)
              and _hit(b, dk[0][2], 1.0)) if dk else 0.0
    ok &= gap >= MIN_GAP
    out.append(("parts under the DevKitC <= 2.0 mm", ok,
                f"{len(worst)} parts; tallest " + ", ".join(f"{l} {hm:.2f} max (model {hh:.2f})" for hm, hh, l in worst[:4])
                + f"; nearest model to the DevKitC {gap:.2f} mm (its underside {2.5:.1f} mm up)"))
    log("4.")

    # 5. Every real part clear of the droid. The core bears on the uprights by design; the DevKitC pin
    #    tails sit in the uprights' reliefs (check_pcb10_mount.py). The CAD's mated plugs stand on
    #    the real headers (J10-1's plug against the board edge), so neither headers nor the core are
    #    tested against plugs.
    plugs = [(l, s, b) for l, (s, b) in own.items() if "MATED_PLUG" in l]
    fixed = [(l, s, b) for l, s, b in others if not any(r in l for r in RESERVE)]
    reserves = [(l, s, b) for l, s, b in others if any(r in l for r in RESERVE)]
    hard, soft = [], []
    for l, s, b in [core, *comps]:
        for o, os_, ob in fixed + ([] if l.startswith(CONN) or l == core[0] else plugs):
            if (l == core[0] and o.startswith(UPRIGHT)) or not _hit(b, ob, 3.0):
                continue
            hard.append((_gap(s, b, os_, ob), l, o))
        for o, os_, ob in reserves:
            if _hit(b, ob, 3.0):
                soft.append((_gap(s, b, os_, ob), l, o))
    hard.sort()
    soft.sort()
    out.append(("parts clear of the droid", not hard or hard[0][0] >= MIN_GAP,
                "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in hard[:4]) or "nothing within 3 mm"))
    print("INFO  reserves near the board: " + ("; ".join(f"{l} {d:.2f} to {o}" for d, l, o in soft[:4]) or "none"))
    log("5.")

    # 6. Behind the board (B face, 10 mm of air): the Micro-Fit tails and peg, JP1's and the DevKitC's pins.
    back = MNT["board"][2]
    below = []
    for l, s, b in comps:
        if b[1] >= back - 0.01:
            continue
        low = s & entry._cut_box(b[0] - 1.0, b[3] + 1.0, b[1] - 1.0, back, b[2] - 1.0, b[5] + 1.0)
        lb = _box(low)
        d = min(((_gap(low, lb, os_, ob), o) for o, os_, ob in fixed if _hit(lb, ob, 3.0) and not o.startswith(UPRIGHT)),
                default=(99.0, "nothing within 3 mm"))
        below.append((d[0], f"{l} to Y {lb[1]:.2f}", d[1]))
    below.sort()
    out.append(("behind the board", not below or below[0][0] >= MIN_GAP,
                "; ".join(f"{l}: {d:.2f} to {o}" for d, l, o in below[:3]) or "nothing through the board"))

    # 7. Install with the real parts (no plugs or screws): toward the wall at the low position (2 mm
    #    down), then the 2 mm slide up under the hooks, as check_pcb10_mount.py does with the CAD.
    ups = [(l, s, b) for l, s, b in others if l.startswith(UPRIGHT)]
    walls = fixed + ups
    module = [core, *comps]
    slide = MNT["slide"]

    def clashes_at(dy, dz):
        found = {}
        for l, s, b in module:
            mb = (b[0], b[1] + dy, b[2] + dz, b[3], b[4] + dy, b[5] + dz)
            moved = None
            for o, os_, ob in walls:
                if not _hit(mb, ob):
                    continue
                if l == core[0] and o.startswith(UPRIGHT) and dy == 0.0:
                    continue                       # the board bears on the uprights
                moved = moved or s.moved(Location((0.0, dy, dz)))
                v = _vol(moved & os_)
                if v > 1e-4:
                    found[f"{l}/{o}"] = max(v, found.get(f"{l}/{o}", 0.0))
        return found

    hits = {}
    for f in (1.0, 0.75, 0.5, 0.25, 0.0):
        hits.update(clashes_at(0.0, -slide * f))
    depth, stop = None, {}
    for dy in [k * 0.5 for k in range(1, 61)]:
        stop = clashes_at(dy, -slide)
        if stop:
            break
        depth = dy
    out.append(("install: approach and slide", not hits and depth is not None and depth >= 2.5,
                ("slide clear" if not hits else "slide hits " + "; ".join(sorted(hits)[:4]))
                + f"; approach clear to {depth} mm out" + ("" if not stop else ", then " + "; ".join(sorted(stop)[:3]))))
    log("7.")

    allok = True
    for name, passed, detail in out:
        allok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
