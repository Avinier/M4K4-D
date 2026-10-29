"""PCB-13 pin relief (D-069): GCT's USB4140 land pattern against the rear-panel inlet pad.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the body panels only, with the droid edits (about 10 s).

The board's -X face seats on the printed pad at X -55.1, so only J1's land pattern may
meet the panel, and only inside the pin relief. Probes are GCT's recommended layout
(drawing A3, 29/08/24, sheet 2) at the seat: plated stake rings, SMT pads and their
solder fillets, both ways up (the pad row's side is set at layout). The same probes
against the panel without the D-069 cut must hit: that is the planted clash.
"""

import importlib.util
from pathlib import Path

from build123d import Box, Compound, Location

import body_v1_model as B

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

SEAT = B.CHARGE_INLET_BOARD_SEAT_X
CY, CZ = B.CHARGE_INLET_CENTER_YZ
MIN_WALL = 0.3                      # relief wall to copper, for the solder fillet
# (y, z, width Y, height Z) in J1's frame; z = 0 on the shell centre line, +z toward the SMT pads.
LAND = {
    "outer_stake_rings": [(s * 4.32, 0.0, 1.10, 1.50) for s in (-1, 1)],
    "inner_stake_rings": [(s * 2.30, -1.43, 1.60, 1.10) for s in (-1, 1)],
    "smt_pads": [(x, 1.20, w, 2.00) for x, w in ((-2.75, 0.80), (-1.52, 0.76), (-0.50, 0.70),
                                                  (0.50, 0.70), (1.52, 0.76), (2.75, 0.80))],
}


def _rear(panels):
    return next(p for p in panels.children if p.label == "REAR_SERVICE_PANEL_OCTAGONAL")


def _probes(thick, grow=0.0, flip=1):
    out = []
    for name, rects in LAND.items():
        for y, z, w, h in rects:
            box = Box(thick, w + 2 * grow, h + 2 * grow).moved(Location((SEAT - thick / 2.0, CY + y, CZ + flip * z)))
            out.append((name, box))
    return out


def _overlap(panel, probes):
    total = {}
    for name, box in probes:
        common = box & panel
        v = common.volume if common is not None and common.solids() else 0.0
        total[name] = round(total.get(name, 0.0) + v, 4)
    return total


def main():
    raw = B.body_panels()
    cut = entry._apply_droid_cuts(Compound(children=[raw]), strict=False)
    before = _rear(raw)
    after = _rear(next(iter(cut.children)))
    board = next(p for p in B.charge_inlet_pcb13().children if p.label == "PCB13_CHARGE_INLET_PCB")
    ok = True

    def report(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}", flush=True)

    report("panel stays one print", len(after.solids()) == 1, f"{len(after.solids())} solid(s)")
    removed = before.volume - after.volume
    expect = 2 * 0.5 * 5.6 * 1.2       # two 0.5 mm strips beside the old relief, 5.6 tall, 1.2 deep
    report("only the relief strips removed", abs(removed - expect) < 0.05, f"{removed:.3f} mm3 (expect {expect:.2f})")

    for flip in (1, -1):
        side = "pads +Z" if flip > 0 else "pads -Z"
        for thick in (0.05, 0.3):
            hits = _overlap(after, _probes(thick, flip=flip))
            report(f"land pattern clear, {side}, {thick} mm", not any(hits.values()), hits)
        copper = Compound(children=[b for _, b in _probes(0.05, flip=flip)])
        wall = copper.distance(after)
        report(f"relief wall to copper, {side}", wall >= MIN_WALL - 1e-3, f"{wall:.3f} mm (>= {MIN_WALL})")
        planted = _overlap(before, _probes(0.05, flip=flip))
        report(f"planted: old 9.60 relief caught, {side}", planted["outer_stake_rings"] > 0, planted)

    report("board still seats", board.distance(after) < 0.01, f"{board.distance(after):.3f} mm")
    common = board & after
    v = common.volume if common is not None and common.solids() else 0.0
    report("board vs panel", v < 1e-3, f"{v:.4f} mm3")
    pilot_wall = min(abs(y) for y, _ in B.PCB13_SCREW_YZ) - 0.8 - entry.PCB13_RELIEF[3]
    report("print between relief and screw pilots", pilot_wall >= 3.0, f"{pilot_wall:.2f} mm")
    print("ALL PASS" if ok else "FAILED")
    assert ok


if __name__ == "__main__":
    main()
