"""D-109 Level 5 service screens for the body harness. Geometric screens on the
route boxes and lengths, not cable dynamics. Rows:

- shell lift: each W27 hub-end plug can be drawn back along its route (section screen).
- tray slide (90 mm +X, 2 mm lift, front out): the tray + Pi sweep meets only route boxes
  of chains that are unplugged first (W10 at the Pi; J6 is pre-mated and travels).
- rear-panel withdrawal (40 mm -X): every lead to a panel part reaches its new position
  within CAD length + service allowance, or has a named break.
- body lift: every chain ending at a body-lift half carries >= 40 mm withdrawal slack.
- PCB-08 removal: W17 (soldered) reaches the board's withdrawn pad position from J-S18-Y.
"""

import json
import math
from pathlib import Path

import module_checks as C
import d109_routes as R

HERE = Path(__file__).resolve().parent
PLUG_SECTION = (5.6, 8.1)
TRAY_SWEEP = 90.0
PANEL_TRAVEL = 40.0
UNPLUG_BEFORE_TRAY = {"W10", "W24", "W25", "W26", "W41", "W28"}   # Pi USB-C; the four PCB-09 plugs (PCB-09 leaves with the tray); W28 goes with the speaker
TRAVELS_WITH_TRAY = {"J6 lead"}              # J6 pre-mated; the rear break is opened first
PANEL_PARTS = {"XT30": "W04", "MUSHROOM": "W40 switch"}
PANEL_BREAKS = {"W40 switch": "2-way header at the button buffer (unplug before withdrawing the panel)"}


def main():
    entry, _, leaves = C.droid_tree()
    r = C.Report("check_d109_service")
    ends = {row["check"][9:]: row for row in json.loads((HERE / "check_body_endpoints-report.json").read_text())["rows"]
            if row["check"].startswith("endpoint ")}
    lengths = {w["chain"]: w for w in json.loads((HERE / "body-harness-lengths.json").read_text())["wires"]}
    fixed = ("BODY_SHELL", "M9_", "HARNESS_", "D109_", "YAW_JUNCTION_")
    # shell lift: the hub-end plug (2x3 C-Grid III housing, E 5.6 x 8.1 section) must be
    # drawn back along the lead's route as the shell rises. Every route box on the way
    # must admit that section across its travel (two shorter sides >= 5.6 and >= 8.1).
    for chain in ("W27 FL", "W27 FR", "W27 RL", "W27 RR"):
        tight = []
        for n in R.CHAINS[chain][1]:
            b = R.box(entry, n)
            sides = sorted(b[2 * i + 1] - b[2 * i] for i in range(3))
            # the plug travels along the box's longest side; the other two are its section
            if not (sides[0] >= PLUG_SECTION[0] - 0.01 and sides[1] >= PLUG_SECTION[1] - 0.01):
                tight.append((n, [round(v, 1) for v in sides]))
        r.check(f"shell lift: {chain} plug draws back along its route", not tight, constrictions=tight,
                note="OPEN if failing: resolve in the D-037 shell mock-up (smaller plug, reroute, or wider gap)")
    # tray slide
    met = set()
    for label in ("COMPUTE_TRAY", "C0_RASPBERRY_PI5_EXACT_STEP"):
        t = C.find(leaves, label).box
        sweep = (t[0], t[1], t[2], t[3] + TRAY_SWEEP, t[4], t[5] + 2.0)
        met |= {c for c, (_, names, _) in R.CHAINS.items() for n in names if not n.startswith("D106:")
                and all(max(R.ROUTES[n][2 * i], sweep[i]) < min(R.ROUTES[n][2 * i + 1], sweep[i + 3]) for i in range(3))}
    met = sorted(met)
    bad = [c for c in met if c not in UNPLUG_BEFORE_TRAY | TRAVELS_WITH_TRAY]
    r.check("tray slide meets only unplugged or travelling leads", not bad, met=met, unexpected=bad)
    # rear-panel withdrawal
    for part, chain in PANEL_PARTS.items():
        a, names, z = R.CHAINS[chain]
        other = z if a == part else a
        p, q = ends[part]["mouth"], ends[other]["mouth"]
        moved = (p[0] - PANEL_TRAVEL, p[1], p[2])
        need = math.dist(moved, q)
        have = lengths[chain]["cad_mm"] + lengths[chain]["slack_mm"]
        ok = have >= need or chain in PANEL_BREAKS
        r.check(f"panel withdrawal: {chain}", ok, straight_after_mm=round(need, 1), cad_plus_service_mm=round(have, 1),
                via=PANEL_BREAKS.get(chain, "supported loop"))
    # body lift
    for chain, (a, _, z) in R.CHAINS.items():
        n = sum(1 for e in (a, z) if e and e.endswith("_BODY"))
        if n:
            r.check(f"body lift slack: {chain}", lengths[chain]["slack_mm"] >= 40.0 * n, slack_mm=lengths[chain]["slack_mm"])
    # PCB-08 removal: tilt front 15 deg, +Y 6, -X 60 (check_d107_body); pad moves about that much
    pad = ends["PCB08_J6_PADS"]["mouth"]
    out = (pad[0] - 60.0, pad[1] + 6.0, pad[2] + 34.0 * math.sin(math.radians(15)))
    js = ends["J_S18_Y_BODY"]["mouth"]
    need = math.dist(out, js) * 1.3   # 30 % for the riser path vs the straight line (E)
    have = lengths["W17"]["cad_mm"] + lengths["W17"]["slack_mm"]
    r.check("PCB-08 removal: W17 follows the board", have >= need, pad_out=[round(v, 1) for v in out],
            need_mm_E=round(need, 1), cad_plus_service_mm=round(have, 1),
            note="J-S18-Y unplugged on the deck, riser ties released first")
    r.finish()


if __name__ == "__main__":
    main()
