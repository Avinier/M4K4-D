"""PCB-08 rev A two-layer board placement and hand routing.

Run after Nightly F8 transfers the schematic and the PCB editor is closed.
Coordinates are world X/Y mapped to KiCad (100 + X, 100 - Y), millimetres.
J3 is provisionally the outer FFC and J4 the inner FFC until the cassette
45-degree fold mock-up confirms cable order.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K  # noqa: E402

BOARD = HERE / "pcb-08-yaw-junction.kicad_pcb"
REPORT = HERE / "placement-drc.json"


def xy(world_x, world_y):
    return (round(100 + world_x, 4), round(100 - world_y, 4))


# Main plate (-22..10, -44..-23); extension (10..20, -42..-24.5).
OUTLINE_W = [(-22, -44), (10, -44), (10, -42), (20, -42),
             (20, -24.5), (10, -24.5), (10, -23), (-22, -23)]

# World centre of each transferred footprint and its KiCad rotation.
PLACE_W = {
    "J1": (-15.00, -36.515, 90),  # Micro-Fit RA overhang, clear GH courtyard
    "J2": (-4.625, -26.525, 180), # GH6 body centred on CAD mated-plug datum
    "J3": (17.60, -33.50, 90),    # outer FH34SRJ, mouth +X
    "J4": (7.76, -33.50, 90),     # inner FH34SRJ, mouth +X
    "J5": (-5.50, -40.69, 0),     # yaw servo, shifted +1.44 from CAD block
    "J6": (-4.00, -33.30, 0),     # W17 pads between J2 and J5
    "R1": (5.30, -24.50, 0),      # ground option above J4, beside J2
    "TP1": (2.50, -36.00, 0),
    "TP2": (0.00, -36.00, 0),
}


def drawing_box(name, x0, x1, y0, y1):
    a, b = xy(x0, y1), xy(x1, y0)
    return (f'\t(gr_rect (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) '
            f'(stroke (width 0.1) (type dash)) (fill none) '
            f'(layer "Dwgs.User") (uuid "{K.gen_uuid(name)}"))')


def setup(b):
    b.drop_generated()
    b.drop(lambda kind, raw: kind in ("gr_line", "gr_rect") and '(layer "Edge.Cuts")' in raw)
    pts = [xy(*p) for p in OUTLINE_W]
    pts.append(pts[0])
    b.add(*[K.edge_line(f"pcb08-edge-{i}", a, c, 0.05)
            for i, (a, c) in enumerate(zip(pts, pts[1:]))])
    # Drawings show the required open-actuator and straight-exit envelopes.
    # These are above the PCB, so copper underneath is allowed. A placement
    # rule area would also reject J4 itself; the fit script checks real parts.
    b.add(drawing_box("J4-open-actuator", 4.0, 5.86, -40, -27),
          drawing_box("J4-straight-exit", 9.66, 10.7, -40, -27))
    for ref, (wx, wy, rot) in PLACE_W.items():
        b.move(ref, *xy(wx, wy), rot)
    b.text = b.text.replace(
        '(footprint "Connector_Molex:Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal"',
        '(footprint "pcb08:Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal"')
    b._index()

    # Keep footprint identifiers on the assembly drawing. The inherited
    # Micro-Fit side-entry outline runs to the board edge, so its top silk
    # primitives belong on Fab as well.
    for ref in PLACE_W:
        for kind, start, end in b.items:
            raw = b.text[start:end]
            if kind == "footprint" and f'(property "Reference" "{ref}"' in raw:
                break
        else:
            raise KeyError(ref)
        raw = re.sub(r'(\(property "Reference" "[^"]+"\s+\(at [^)]*\)\s+\(layer )"F.SilkS"',
                     r'\1"F.Fab"', raw, count=1)
        if ref == "J1":
            raw = raw.replace('(layer "F.SilkS")', '(layer "F.Fab")')
        b.text = b.text[:start] + raw + b.text[end:]
        b._index()
    model_name = "Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
    for ref in ("J3", "J4"):
        for kind, start, end in b.items:
            raw = b.text[start:end]
            if kind == "footprint" and f'(property "Reference" "{ref}"' in raw:
                break
        else:
            raise KeyError(ref)
        if f"{model_name}.step" not in raw:
            model = (f'\n\t\t(model "${{KIPRJMOD}}/../../lib/fh34.pretty/{model_name}.step" '
                     '(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n')
            raw = raw[:raw.rfind(")")] + model + raw[raw.rfind(")"):]
            b.text = b.text[:start] + raw + b.text[end:]
            b._index()


def route_signals(b):
    """Hand-planned W24/W43 lanes, yaw branch and ground reference."""
    parts = []

    def track(name, layer, net, width, *points):
        parts.extend(K.track(name, points, width, layer, net))

    # J2's solder tab blocks the direct F.Cu lanes. Four B.Cu channels cross
    # underneath it, then stagger to vias left of J4's 0.5 mm-pitch pad row.
    signal_routes = (
        ("C0TX_P", 2, 2, "/C0TX_P", (97.25, 127.2), (104.7, 127.8),
         [(97.25, 127.2), (104.1, 127.2), (104.7, 127.8)],
         [(104.7, 127.8), (105.65, 128.75), (106.11, 128.75)]),
        ("C0TX_N", 3, 3, "/C0TX_N", (96.0, 128.3), (104.9, 129.1),
         [(96.0, 128.3), (104.1, 128.3), (104.9, 129.1)],
         [(104.9, 129.1), (105.05, 129.25), (106.11, 129.25)]),
        ("C2TX_N", 4, 5, "/C2TX_N", (94.75, 129.4), (104.0, 130.0),
         [(94.75, 129.4), (103.4, 129.4), (104.0, 130.0)],
         [(104.0, 130.0), (104.25, 130.25), (106.11, 130.25)]),
        ("C2TX_P", 5, 6, "/C2TX_P", (93.5, 130.5), (102.7, 131.4),
         [(93.5, 130.5), (101.8, 130.5), (102.7, 131.4)],
         [(102.7, 131.4), (103.35, 130.75), (106.11, 130.75)]),
    )
    for name, j2, j4, net, start_via, end_via, back, exit_f in signal_routes:
        src, dst = b.pad("J2", j2)["at"], b.pad("J4", j4)["at"]
        assert exit_f[-1] == dst
        parts.extend((K.via(f"{name}_J2", start_via, net),
                      K.via(f"{name}_J4", end_via, net)))
        track(f"{name}_J2_F", "F.Cu", net, 0.16, src, start_via)
        track(f"{name}_B", "B.Cu", net, 0.16, *back)
        track(f"{name}_J4_F", "F.Cu", net, 0.16, *exit_f)

    data = b.pad("J4", 8)["at"]
    tp = b.pad("TP1", 1)["at"]
    yaw_data = b.pad("J5", 3)["at"]
    track("SERVO_TO_TP", "F.Cu", "/SERVO_DATA", 0.2,
          data, (103.75, data[1]), (tp[0], 133.0), tp)
    track("SERVO_TO_YAW", "F.Cu", "/SERVO_DATA", 0.2,
          tp, (tp[0], 137.69), yaw_data)

    # W17 power: the 2.4 A allowance is short, with a broad back-copper run.
    track("YAW_RAIL", "B.Cu", "/+11V1_YAW", 0.8,
          b.pad("J6", 1)["at"], (96.5, 133.8), (96.5, 140.19), b.pad("J5", 2)["at"])
    track("YAW_RETURN", "F.Cu", "/GND_SIG", 0.8,
          b.pad("J6", 2)["at"], (100.6, 135.4),
          (94.5, 135.4), b.pad("J5", 1)["at"])

    # Link ground is separate until fitted R1. The resistor fits above J4,
    # allowing a short F.Cu route beside J2 rather than a long B.Cu barrier.
    j2_gnd = b.pad("J2", 1)["at"]
    r1_in = b.pad("R1", 1)["at"]
    track("LINK_GND_F", "F.Cu", "/LINK_GND", 0.2,
          j2_gnd, (98.575, 124.5), r1_in)

    for number in (1, 4, 7, 9):
        p = b.pad("J4", number)["at"]
        at = (107.3, p[1])
        parts.append(K.via(f"GND_SIG_J4_{number}", at, "/GND_SIG"))
        track(f"GND_SIG_J4_{number}", "F.Cu", "/GND_SIG", 0.16, p, at)
    for ref, via_at in (("TP2", (101.2, 136.0)), ("R1", (107.5, 123.9))):
        p = b.pad(ref, 1 if ref == "TP2" else 2)["at"]
        parts.append(K.via(f"GND_SIG_{ref}", via_at, "/GND_SIG"))
        if ref == "R1":
            track("GND_SIG_R1_F", "F.Cu", "/GND_SIG", 0.2,
                  p, (106.8125, 123.9), via_at)
        else:
            track(f"GND_SIG_{ref}_F", "F.Cu", "/GND_SIG", 0.2, p, via_at)
    track("GND_SIG_R1_TO_J4", "F.Cu", "/GND_SIG", 0.2,
          (107.5, 123.9), (107.3, 124.1), (107.3, 128.25))
    parts.append(K.pour("GND_SIG_B", "B.Cu", "/GND_SIG",
                        [xy(*p) for p in OUTLINE_W], clearance=0.2,
                        min_width=0.2, solid=True))
    b.add(*parts)


def route_power(b):
    """Hand-routed power pairs and F.Cu contact groups."""
    parts = []
    jp = b.pad("J1", 1)["at"][0]
    jr = b.pad("J1", 4)["at"][0]
    parts.extend(K.track("HEAD_POS_B",
                         [(jp, 136.515), (jp, 142.5),
                          (108.7, 142.5), (108.7, 131.8),
                          (111.0, 129.5)],
                         1.4, "B.Cu", "/+6V3_HEAD_PR"))
    parts.append(K.via("HEAD_POS_GROUP", (111.0, 129.5), "/+6V3_HEAD_PR", 0.8, 0.35))
    parts.extend(K.track("HEAD_RET_F",
                         [(jr, 136.515), (jr, 142.5),
                          (108.8, 142.5), (108.8, 141.0),
                          (110.9, 141.0), (110.9, 133.5)],
                         1.3, "F.Cu", "/GND_HEAD"))
    parts.append(K.pour("HEAD_POS_SEVEN", "F.Cu", "/+6V3_HEAD_PR",
                        [(110.7, 128.1), (116.4, 128.1),
                         (116.4, 131.4), (110.7, 131.4)],
                        clearance=0.16, min_width=0.2, solid=True))
    parts.append(K.pour("HEAD_RET_SEVEN", "F.Cu", "/GND_HEAD",
                        [(111.0, 131.6), (116.4, 131.6),
                         (116.4, 134.9), (111.0, 134.9)],
                        clearance=0.16, min_width=0.2, solid=True))
    # Copper fields parallel the hand-routed trunks. The J5 through-hole
    # row and the bottom board edge still create a narrow throat; the filled
    # geometry, not this polygon's nominal width, controls resistance.
    parts.append(K.pour("HEAD_POS_MAIN", "B.Cu", "/+6V3_HEAD_PR",
                        [(83.3, 134.5), (111.5, 134.5),
                         (111.5, 143.6), (83.3, 143.6)],
                        clearance=0.2, min_width=0.2, priority=1, solid=True))
    parts.append(K.pour("HEAD_RET_MAIN", "F.Cu", "/GND_HEAD",
                        [(86.0, 134.5), (112.0, 134.5),
                         (112.0, 143.6), (86.0, 143.6)],
                        clearance=0.2, min_width=0.2, solid=True))

    # Four narrow 5 V/return trunks use the upper B.Cu corridor. Their
    # descending legs are ordered right to left, so none crosses another
    # trunk's horizontal escape. Keep these returns distinct from GND_HEAD.
    power_lanes = (
        ("C2_POS", "/+5V_C2", 2, [(jp, 133.515), (83.7, 133.515-(jp-83.7)),
                                    (83.7, 125.0), (114.9, 125.0), (114.9, 135.5)],
         135.1, 135.9, 114.6),
        ("DISPLAY_POS", "/+5V_DISPLAY", 3,
         [(jp, 130.515), (jp, 125.4), (114.1, 125.4), (114.1, 137.5)],
         137.1, 137.9, 113.8),
        ("DISPLAY_RET", "/GND_DISPLAY", 6,
         [(jr, 130.515), (jr, 125.8), (113.3, 125.8), (113.3, 138.5)],
         138.1, 138.9, 113.0),
        ("C2_RET", "/GND_C2", 5,
         [(jr, 133.515), (91.5, 133.515-(91.5-jr)), (91.5, 126.2),
          (112.5, 126.2), (112.5, 136.5)],
         136.1, 136.9, 112.2),
    )
    for name, net, pin, points, y0, y1, x0 in power_lanes:
        assert points[0] == b.pad("J1", pin)["at"]
        parts.extend(K.track(name + "_B", points, 0.2, "B.Cu", net))
        parts.append(K.via(name + "_GROUP", points[-1], net))
        parts.append(K.pour(name + "_PAIR", "F.Cu", net,
                            [(x0, y0), (116.4, y0), (116.4, y1), (x0, y1)],
                            clearance=0.16, min_width=0.16, solid=True))
    b.add(*parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--no-drc", action="store_true")
    p.add_argument("--placement-only", action="store_true")
    args = p.parse_args()
    b = K.Board(BOARD)
    setup(b)
    if not args.placement_only:
        route_signals(b)
        route_power(b)
    b.save()
    print("Placed:", json.dumps({f["ref"]: [*f["at"], f["rot"]] for f in b.footprints()}, sort_keys=True))
    if not args.no_drc:
        result = K.drc(BOARD, REPORT, refill=not args.placement_only)
        print("DRC:", {k: v for k, v in result.items() if k != "report"})
        print(K.summary(result["report"], limit=80))


if __name__ == "__main__":
    main()
