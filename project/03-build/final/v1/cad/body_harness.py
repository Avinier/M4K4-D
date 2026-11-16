"""D-109 Level 4: visible, nominal body-harness wires along the D109 route chains.

World mm. Each wire is one outer envelope (a pair or bundle as one tube) on the
centreline: start-endpoint mouth -> centres of the overlaps between consecutive
route boxes -> end-endpoint mouth. Not a cut length, bend or dress proof.
Lengths (centreline + allowances) go to body-harness-lengths.json via
write_lengths(). Shared corridors carry several envelopes on one centreline:
read those as one bundle.
"""

import json
from pathlib import Path

from build123d import Compound

import d109_routes as R
from chassis_harness import _tube

# chain -> (label, radius, colour, class, group, g/m)
WIRES = {
    "W03r": ("W03r_JBAT_TO_CHARGE_SPLICE_POS_AWG16", 1.0, "#cf413a", "power", "Rear-bay power", 14),
    "W03r-": ("W03r_JBAT_TO_CHARGE_SPLICE_NEG_AWG16", 1.0, "#30343a", "power", "Rear-bay power", 14),
    "W04": ("W04_CHARGE_SPLICES_TO_XT30_2XAWG16", 2.0, "#e07a3a", "power", "Rear panel", 28),
    "W05 M1": ("W05_POS_SPLICE_TO_M1_VIN_AWG16", 1.0, "#cf413a", "power", "Rear-bay power", 14),
    "W05 M6": ("W05_M1_VOUT_TO_M6_INPLUS_AWG16", 1.0, "#cf413a", "power", "Rear-bay power", 14),
    "W05 stars": ("W05_M6_INMINUS_TO_POS_STAR_AWG16", 1.0, "#cf413a", "power", "Rear-bay power", 14),
    "W05c": ("W05c_STARS_TO_JCHASSIS_2XAWG16", 2.0, "#a8322c", "power", "Rear-bay power", 28),
    "W05b M4": ("W05b_STARS_TO_M4_2XAWG18", 1.8, "#c25a3a", "power", "Tray 5 V", 18),
    "W05b M5": ("W05b_STARS_TO_M5_2XAWG18", 1.8, "#c25a3a", "power", "Tray 5 V", 18),
    "W10": ("W10_M4_TO_PI5_USBC_2XAWG18", 1.8, "#d98b3a", "power", "Tray 5 V", 18),
    "W05s": ("W05s_M5_TO_SHARED_5V_2XAWG18", 1.8, "#d98b3a", "power", "Tray 5 V", 18),
    "W11": ("W11_SHARED_5V_TO_SS34_2XAWG22", 1.3, "#e0a13a", "power", "Tray 5 V", 8),
    "W11 J10-1": ("W11_SS34_TO_C3_J10_1_2XAWG22", 1.3, "#e0a13a", "power", "Tray 5 V", 8),
    "W14": ("W14_SHARED_5V_TO_J8_1_4XAWG22", 1.8, "#e0a13a", "power", "Riser to PCB-08", 16),
    "W13": ("W13_JS18H_TO_J8_1_HEAD_6V3_2XAWG20", 1.6, "#d8a344", "power", "Riser to PCB-08", 12),
    "W17": ("W17_JS18Y_TO_PCB08_J6_YAW_11V1_2XAWG20", 1.6, "#a77ac4", "power", "Riser to PCB-08", 12),
    "W12": ("W12_SHARED_5V_TO_AMP_2XAWG22", 1.3, "#e0a13a", "power", "Audio", 8),
    "W24": ("W24_J9_1_TO_J8_4_GH6_CABLE", 1.3, "#71a4ca", "signal", "Compute signals", 7),
    "W25": ("W25_J10_2_TO_J9_2_GH6_CABLE", 1.3, "#6b86b9", "signal", "Compute signals", 7),
    "W41": ("W41_FAN_TO_J9_4_GH2_CABLE", 0.9, "#55a8a9", "signal", "Compute signals", 2.4),
    "J6 lead": ("J6_PCB09_TO_REAR_BREAK_GH6_CABLE", 1.3, "#65a7b5", "signal", "Compute signals", 7),
    "W44": ("W44_REAR_BREAK_TO_M6_4XAWG28", 1.0, "#65a7b5", "signal", "Rear panel", 4.8),
    "W40 sense": ("W40_REAR_BREAK_TO_BUTTON_BUFFER_2XAWG28", 0.8, "#9bba71", "signal", "Rear panel", 2.4),
    "W40 switch": ("W40_MUSHROOM_TO_BUTTON_BUFFER_2XAWG24", 0.9, "#9bba71", "signal", "Rear panel", 3.4),
    "W40 M1": ("W40_BUFFER_TO_M1_ON_OFF_3XAWG24", 1.0, "#9bba71", "signal", "Rear panel", 5.1),
    "W26": ("W26_J9_3_TO_HUB_GH10_CABLE", 1.6, "#8f7ac4", "audio", "Audio", 12),
    "W27 FL": ("W27_HUB_TO_MIC_FRONT_L_6XAWG28", 1.2, "#b48fd4", "audio", "Audio", 7.2),
    "W27 FR": ("W27_HUB_TO_MIC_FRONT_R_6XAWG28", 1.2, "#b48fd4", "audio", "Audio", 7.2),
    "W27 RL": ("W27_HUB_TO_MIC_REAR_L_6XAWG28", 1.2, "#b48fd4", "audio", "Audio", 7.2),
    "W27 RR": ("W27_HUB_TO_MIC_REAR_R_6XAWG28", 1.2, "#b48fd4", "audio", "Audio", 7.2),
    "W28": ("W28_AMP_TO_SPEAKER_TWISTED_2XAWG22", 1.3, "#c59bd7", "audio", "Audio", 8),
}
TERMINATION = 15.0           # per end: strip, crimp/solder, strain relief (E)
BODY_LIFT_SLACK = 40.0        # H-08 withdrawable slack at a body-lift plug end
SERVICE = {"W04": 52.4, "W27 FL": 40.0, "W27 FR": 40.0, "W27 RL": 40.0, "W27 RR": 40.0,
           "J6 lead": 30.0, "W17": 60.0}   # panel withdrawal; shell-lift plugging; tray slide; PCB-08 removal (E)


def _mid(b):
    return ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2)


def _clamp(p, b):
    return tuple(min(max(p[i], b[2 * i]), b[2 * i + 1]) for i in range(3))


def centreline(entry, ends, chain):
    a, names, z = R.CHAINS[chain]
    boxes = [R.box(entry, n) for n in names]
    pts = [_clamp(ends[a]["mouth"], boxes[0]) if a else _mid(boxes[0])]
    if a:
        pts.insert(0, ends[a]["mouth"])
    for p, q in zip(boxes, boxes[1:]):
        ov = tuple(v for i in range(3) for v in (max(p[2 * i], q[2 * i]), min(p[2 * i + 1], q[2 * i + 1])))
        pts.append(_mid(ov))
    pts += [_clamp(ends[z]["mouth"], boxes[-1]), ends[z]["mouth"]]
    out = []
    for p in pts:                      # drop repeats
        if not out or sum((p[i] - out[-1][i]) ** 2 for i in range(3)) > 1e-6:
            out.append(tuple(round(v, 3) for v in p))
    return out


def length(points):
    return sum(sum((b[i] - a[i]) ** 2 for i in range(3)) ** .5 for a, b in zip(points, points[1:]))


def paths(entry, ends):
    return {chain: centreline(entry, ends, chain) for chain in WIRES}


def cached_ends(path=Path(__file__).with_name("check_body_endpoints-report.json")):
    """Endpoints as last written by check_body_endpoints.py (re-run it after moving an endpoint)."""
    out = {}
    for row in json.loads(path.read_text())["rows"]:
        if row["check"].startswith("endpoint ") and row.get("box"):
            out[row["check"][9:]] = dict(mouth=tuple(row["mouth"]), box=tuple(row["box"]))
    return out


def build_body_harness(entry, ends=None):
    ends = ends or cached_ends()
    groups = {}
    for chain, pts in paths(entry, ends).items():
        label, r, colour, _, group, _ = WIRES[chain]
        groups.setdefault(group, []).append(entry._tag(_tube(pts, r), label, colour))
    return Compound(label="Body wires", children=[Compound(label=g, children=c) for g, c in groups.items()])


def write_lengths(entry, ends, path=Path(__file__).with_name("body-harness-lengths.json")):
    rows, total_g = [], 0.0
    for chain, pts in paths(entry, ends).items():
        label, _, _, cls, group, gpm = WIRES[chain]
        a, _, z = R.CHAINS[chain]
        cad = length(pts)
        slack = sum(BODY_LIFT_SLACK for e in (a, z) if e and e.endswith("_BODY")) + SERVICE.get(chain, 0.0)
        cut = cad + 2 * TERMINATION + slack
        mass = cut / 1000 * gpm
        total_g += mass
        mid = tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))
        rows.append(dict(chain=chain, label=label, cls=cls, group=group, cad_mm=round(cad, 1),
                         slack_mm=slack, cut_mm_E=round(cut), mass_g_E=round(mass, 2),
                         centroid=[round(v, 1) for v in mid]))
    doc = dict(note="E: CAD centreline + 2 x 15 mm terminations + body-lift/service slack; conductor mass only",
               total_conductor_g_E=round(total_g, 1), wires=rows)
    path.write_text(json.dumps(doc, indent=1) + "\n")
    return doc
