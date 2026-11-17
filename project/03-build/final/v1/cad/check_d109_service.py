"""D-109 Level 5 service screens for the body harness. Geometric screens on the
route boxes and lengths, not cable dynamics. Rows:

- shell lift: each W27 hub-end plug can be drawn back along its route (section screen).
- tray slide (90 mm +X, 2 mm lift, front out): as built it is blocked (C3 headers, M5); in the
  service state (body off the chassis, C3 carrier out, M4/M5 detached from below) it clears, and
  it meets only route boxes of leads unplugged first (W10 at the Pi; J6 is pre-mated and travels).
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
TRAY_RIDERS = ("COMPUTE_TRAY", "C0_", "PI5_", "PCB09_", "PI_")   # move with the tray (Pi, cooler, PCB-09)
MODULE_FIXINGS = ("M4_M2X4_BOARD_SCREW", "M5_M2X4_BOARD_SCREW", "M4_M2X5_FF_ROUND_STANDOFF",
                  "M5_M2X5_FF_ROUND_STANDOFF", "M4_M2X5_TRAY_SCREW", "M5_M2X5_TRAY_SCREW")   # removed from below
LIFTS_ASIDE = ("J_S18_Y_MICROFIT3_1X2_RECEPTACLE_HALF", "J_S18_H_MICROFIT3_1X2_RECEPTACLE_HALF")   # body halves hang on their leads
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
    # tray slide (rewritten 2026-11-17). M4/M5 hang 5 mm under the tray on F-F standoffs and the
    # tray's -Y edge passes the C3 J10 headers, so the old row (tray and Pi boxes vs route boxes only)
    # could not see the real blockers. Rows: (a) as built, the first part contact of the tray-riding
    # parts (records why the service state below is needed); (b) the M2x4 board screws are reachable
    # from below with the body lifted off the chassis; (c) in the service state (C3 carrier out, tray
    # M3 screws out, M4/M5 board screws and standoffs out, modules left hanging on their leads) the
    # tray and every non-vendor rider sweep 90 mm (+2 mm lift) clear of fixed parts; (d) the route
    # boxes the sweep meets belong only to leads unplugged first or travelling with the tray.
    parts = [lf for lf in leaves if C.is_part(lf.path)]
    removed_first = ("BODY_SHELL", "FRONT_SERVICE_PANEL", "REAR_SERVICE_PANEL", "SPEAKER", "M9_", "M8_",
                     "C3_", "TRAY_M3X8_SCREW_")
    riders = [lf for lf in parts if lf.label.startswith(TRAY_RIDERS) and not lf.vendor
              and "MATED_PLUG" not in lf.label]   # W24/W25/W26/W41 plugs are pulled first
    module_fixings = [lf for lf in parts if lf.label.startswith(MODULE_FIXINGS)]
    fixed = [lf for lf in parts if not lf.label.startswith(TRAY_RIDERS) and lf not in module_fixings
             and not lf.label.startswith(removed_first)]

    def first_contact(subjects, pool, step=3):
        for dx in range(0, int(TRAY_SWEEP) + 1, step):
            for lf in subjects:
                hits = C.clashes(C.moved(lf.shape, (dx, 0, 2.0)), pool, min_vol=0.05)
                if hits:
                    return (dx, lf.label, hits[:3])
        return None

    as_built = first_contact([*riders, *module_fixings], [lf for lf in parts if lf not in riders and lf not in module_fixings])
    r.check("tray slide as built is blocked (why the service state is needed)", as_built is not None, first_contact=as_built,
            note="C3 J10 headers meet the tray edge; M5 and its standoffs meet the frame near 57 mm")
    reach = []
    for lf in parts:
        if lf.label.startswith(("M4_M2X4_BOARD_SCREW", "M5_M2X4_BOARD_SCREW")):
            b = lf.box
            x, y = (b[0] + b[3]) / 2, (b[1] + b[4]) / 2
            tool = C.blk((x - 1.5, x + 1.5, y - 1.5, y + 1.5, b[2] - 40.0, b[2] - 0.05))
            hits = [h for h in C.clashes(tool, parts, min_vol=0.01)
                    if "CHASSIS_V1_REFERENCE" not in "/".join(next(l.path for l in leaves if l.label == h[0])).upper()
                    and not h[0].startswith(LIFTS_ASIDE)]
            reach.append((lf.label, hits[:3]))
    r.check("M4/M5 board screws reachable from below, body lifted off the chassis", all(not h for _, h in reach),
            screws=reach, tool="3 mm driver, 40 mm straight", lifts_aside=list(LIFTS_ASIDE))
    service = first_contact(riders, fixed)
    r.check("tray slide in the service state clears every fixed part", service is None, first_contact=service,
            riders=len(riders), state="C3 carrier out; tray M3x8 out; M4/M5 M2x4 and standoffs out, modules on their leads",
            note="vendor Pi/cooler are checked by 02-body check_compute_mount.py (D-042 insertion sweep); not swept here")
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
