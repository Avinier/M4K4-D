"""PCB-13 rev A fit: place the KiCad board STEP on the rear-panel inlet pad and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the body panels, shell, frames and electronics (about 6 min; the removal sweep
is most of it), with the D-069 pin relief from DROID_CUTS.

KiCad's STEP (exported with --user-origin 0x0mm) has (Xs, Ys) = (KiCad x, -y), the core
at Zs 0..1.51 and parts 0.085 mm off it; J1 sits on B (Zs < 0). The board is seen from its
F face, world +X (04-pcbs/pcb-13-charge-inlet/README.md, Board set-up): KiCad x = 114 + Y,
y = 171.5 - Z, so world Y = Xs - 114, Z = Ys + 171.5, X = Zs + the core's offset, with the
core centred on the CAD board's mid-plane (B face on the pad seat at X -55.1).
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Cylinder, Location, import_step
from OCP.gp import gp_Trsf
from OCP.TopLoc import TopLoc_Location

import body_v1_model as B
from check_pcb10_mount import _box

HERE = Path(__file__).resolve().parent
BOARD_STEP = HERE.parents[2] / "04-pcbs/pcb-13-charge-inlet/cad/pcb-13-charge-inlet-revA.step"
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

SEAT = B.CHARGE_INLET_BOARD_SEAT_X            # -55.1, board B face on the pad
F_FACE = SEAT + B.PCB_THICKNESS                # -53.5
FLOOR = B.CHARGE_INLET_POCKET_FLOOR_X          # -61.6, J1's mouth plane
PCB02_BACK = -49.6                             # PCB-02's bare -X face (lesson 1 survey)
J1 = "GCT_USB4140"
# Datasheet maximum heights above the F copper (mm); KiCad writes "." as "_" (match by prefix).
MAX_H = {"C_1206": 1.80,                        # Samsung CL31B475KBHNNNE: 1.6 +- 0.2
         "C_0603": 0.90, "C_0402": 0.55,        # CL10 0.8 +- 0.1; CL05 0.5 +- 0.05
         "R_1206": 0.65, "R_0805": 0.60, "R_0402": 0.40,  # Panasonic ERJ-P08 / ERJ-P06, 0402 chip
         "WSON-6": 0.80,                        # TI DRV0006A: 0.8 max
         "SOT-323": 1.10,                       # ST SOT323-3L: 1.1 max
         "QFN-24": 1.00,                        # ST QFN-24 A: 1.00 max
         "ST_PowerFLAT": 0.90}                  # ST DS9257 Table 7 A: 0.90 max
STAKE_ABOVE_F = 1.85 - 1.44 + 0.30              # GCT stake max past a -10 % board, plus a 0.3 fillet
LIMIT = 2.0                                     # F-face parts envelope (charge-path sec 3)
MIN_TO_PCB02 = 1.0


def board_parts():
    step = import_step(str(BOARD_STEP))
    raw = [(c.label, Compound(c.solids())) for c in step.children if c.solids()]
    core_box = _box(next(s for l, s in raw if l.endswith("_PCB")))
    core = core_box[5] - core_box[2]
    t = gp_Trsf()
    #           X = Zs + a                                       Y = Xs - 114        Z = Ys + 171.5
    t.SetValues(0, 0, 1, SEAT + (B.PCB_THICKNESS - core) / 2.0 - core_box[2], 1, 0, 0, -114.0, 0, 1, 0, 171.5)
    loc = TopLoc_Location(t)
    return [(l, Compound(s.wrapped.Moved(loc))) for l, s in raw], core


def leaves(shape):
    kids = getattr(shape, "children", None)
    return [x for k in kids for x in leaves(k)] if kids else [shape]


def vol(a, b):
    c = a & b
    return 0.0 if c is None or not c.solids() else c.volume


def main():
    ok = True

    def report(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}", flush=True)

    parts, core = board_parts()
    pcb = next(s for l, s in parts if l.endswith("_PCB"))
    j1 = next(s for l, s in parts if l.startswith(J1))
    fparts = [(l, s) for l, s in parts if not l.endswith("_PCB") and not l.startswith(J1)]

    # 1. Outline and holes against the CAD board.
    pb = _box(pcb)
    cad = B.PCB13_BOARD
    err = max(abs(pb[1] - cad[2]), abs(pb[4] - cad[3]), abs(pb[2] - cad[4]), abs(pb[5] - cad[5]))
    report("outline on the CAD board", err < 0.01, f"Y {pb[1]:.2f}..{pb[4]:.2f}, Z {pb[2]:.2f}..{pb[5]:.2f} (max error {err:.3f})")
    holes = [vol(pcb, Cylinder(0.9, 3.0, rotation=(0, 90, 0)).moved(Location(((SEAT + F_FACE) / 2.0, y, z))))
             for y, z in B.PCB13_SCREW_YZ]
    report("M2 holes at the CAD screw axes", max(holes) < 1e-6, f"core inside Ø1.8 probes: {[round(h, 4) for h in holes]} mm³")

    # 2. J1's mouth against the pocket floor.
    jb = _box(j1)
    report("J1 mouth at the pocket floor", abs(jb[0] - FLOOR) <= 0.15,
           f"X {jb[0]:.3f} vs floor {FLOOR} ({jb[0] - FLOOR:+.3f}; - = into the pocket)")

    # 3. J1 and the board against the rear panel with the D-069 relief.
    panels = entry._apply_droid_cuts(Compound(children=[B.body_panels()]), strict=False)
    rear = next(p for p in leaves(panels) if p.label == "REAR_SERVICE_PANEL_OCTAGONAL")
    report("J1 vs rear panel", vol(j1, rear) < 1e-4, f"overlap {vol(j1, rear):.4f} mm³, gap {j1.distance(rear):.3f} mm")
    report("board core vs rear panel", vol(pcb, rear) < 1e-4, f"overlap {vol(pcb, rear):.4f} mm³, gap {pcb.distance(rear):.3f} mm")
    hits = {l: round(vol(s, rear), 4) for l, s in fparts if vol(s, rear) > 1e-4}
    report("F parts vs rear panel", not hits, hits or "none")

    # 4. Heights on F: models and datasheet maxima, against 2.0 and PCB-02's back face.
    worst = []
    for l, s in fparts:
        bb = _box(s)
        model_h = bb[3] - F_FACE
        key = next((k for k in MAX_H if l.startswith(k)), None)
        assert key, f"no datasheet height for {l}"
        worst.append((max(model_h, MAX_H[key]), l, round(model_h, 3), MAX_H[key]))
    worst.sort(reverse=True)
    h, l, mh, dh = worst[0]
    report("tallest F part <= 2.0 mm", h <= LIMIT, f"{l}: model {mh}, datasheet max {dh}")
    report("F parts to PCB-02's back face", PCB02_BACK - (F_FACE + h) >= MIN_TO_PCB02,
           f"{PCB02_BACK - (F_FACE + h):.2f} mm at the datasheet maximum (>= {MIN_TO_PCB02})")
    tails = _box(j1)[3] - F_FACE
    report("J1 stake tails on F", STAKE_ABOVE_F <= LIMIT, f"model {tails:.2f} mm, worst {STAKE_ABOVE_F:.2f} mm with a fillet")

    # 5. The CAD screws (BO-017) against the real parts.
    screws = [p for p in leaves(B.charge_inlet_pcb13()) if "SCREW" in (p.label or "")]
    sh = {f"{l}:{sc.label}": round(vol(s, sc), 4) for l, s in parts for sc in screws if vol(s, sc) > 1e-4}
    report("screws vs board parts", not sh, sh or "none")

    # 6. Removal: the panel's inlet pad and the real board slide out along -X, 40 mm in 4 mm steps.
    shell = B.body_shell()
    frame = B.panel_internal_frame("REAR")
    elec = [p for p in leaves(B.electronics()) if not (p.label or "").startswith(("PCB13_", "ESTOP_XA1E_", "POWER_BUTTON_"))]
    near = [p for p in elec if _box(p)[0] < -40.0]
    pad, cuts = B.rear_panel_charge_inlet()
    pad = pad - cuts
    movers = [pad, pcb, j1] + [s for _, s in fparts]
    sweep = {}
    for step in range(1, 11):
        dx = -4.0 * step
        for m in movers:
            mm_ = m.moved(Location((dx, 0, 0)))
            for o in [shell, frame, *near]:
                ob, mb = _box(o), _box(mm_)
                if mb[3] <= ob[0] or ob[3] <= mb[0] or mb[4] <= ob[1] or ob[4] <= mb[1] or mb[5] <= ob[2] or ob[5] <= mb[2]:
                    continue
                v = vol(mm_, o)
                if v > 1e-3:
                    sweep[f"{dx:+.0f}:{getattr(o, 'label', '?')}"] = round(v, 3)
    report("removal sweep, 40 mm along -X", not sweep, sweep or "clear")

    print("ALL PASS" if ok else "FAILED")
    assert ok


if __name__ == "__main__":
    main()
