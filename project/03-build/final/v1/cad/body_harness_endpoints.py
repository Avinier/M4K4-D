"""D-109 Level 0: every body-harness endpoint, resolved from the live droid tree.

Each endpoint is a label regex (must match exactly one leaf, or the first of a
named group for multi-leaf parts) and the world direction a wire leaves the
part in (its plug's rear / pad edge). Later D-109 scripts read endpoints from
here, never from copied coordinates. PCB-08's D-107 mated plugs are built by
pcb_integration rather than the droid tree, so they come from FIXED (the
check_d107_body report bounds); refresh them if PCB-08 moves.
"""

import re

# name: (label regex, exit direction, wires)
ENDPOINTS = {
    # PCB-08 rev B mated plugs (module_checks swaps rev B into the droid tree, D-109)
    "J8_1": (r"D107_PCB08_J8_1_MATED_PLUG_E", (-1, 0, 0), "W13 W14"),
    "J8_4": (r"D107_PCB08_J8_4_MATED_PLUG_E", (0, 0, 1), "W24"),
    "J8_8": (r"D107_PCB08_J8_8_MATED_PLUG_E", (0, 0, 1), "W15"),
    "J8_9": (r"D107_PCB08_J8_9_MATED_PLUG_E", (1, 0, 0), "W47"),
    "J8_10": (r"D107_PCB08_J8_10_MATED_PLUG_E", (0, 0, 1), "W47"),
    "PCB08_BOARD": (r"PCB08_MAIN_06__pcb-08-yaw-junction_PCB", (0, 0, 1), "-"),
    # rear-bay power
    "J_BAT_BODY": (r"J_BAT_MICROFIT_PLUS_1X2_RECEPTACLE_HALF", (-1, 0, 0), "W03r"),
    "J_CHASSIS_BODY": (r"J_CHASSIS_MICROFIT_PLUS_1X2_RECEPTACLE_HALF", (-1, 0, 0), "W05c"),
    "J_S18_H_BODY": (r"J_S18_H_MICROFIT3_1X2_RECEPTACLE_HALF", (-1, 0, 0), "W13"),
    "J_S18_Y_BODY": (r"J_S18_Y_MICROFIT3_1X2_RECEPTACLE_HALF", (-1, 0, 0), "W17"),
    "CHARGE_SPLICE_POS": (r"CHARGE_SPLICE_HEATSHRUNK_AWG16", (0, 0, 1), "W03r W04 W05"),
    "STAR_POS": (r"SWITCHED_STAR_POS_AWG16_SPLICE", (0, 1, 0), "W05 W05c W05b"),
    "STAR_NEG": (r"SWITCHED_STAR_NEG_AWG16_SPLICE", (0, 1, 0), "W05 W05c W05b"),
    "M1": (r"M1_POLOLU_2813_PUSHBUTTON_POWER_SWITCH_HP_STEP", (0, 1, 0), "W05 W40"),
    "M6": (r"M6_INA226_PARTS_ENVELOPE_UNMEASURED", (1, 0, 0), "W05 W44"),   # pads on the parts side
    "BUTTON_BUFFER": (r"M1_REAR_BUTTON_BUFFER_CAD_RESERVE", (1, 0, 0), "W40 J6"),
    "XT30": (r"M12_XT30U_FEMALE_CHARGE_PORT", (1, 0, 0), "W04"),
    "MUSHROOM": (r"POWER_BUTTON_MUSHROOM_(LEFT|RIGHT)_TERMINAL_SCREW_HEAD", (1, 0, 0), "W40"),   # the two NO terminals, not the whole button (2026-11-17)
    # tray
    "M4": (r"M4_POLOLU_4082_S13V30F5_\w+_STEP", (0, 0, -1), "W05b W10|W05s"),
    "M5": (r"M5_POLOLU_4082_S13V30F5_\w+_STEP", (0, 0, -1), "W05b W05s|W10"),
    "PI_USBC": (r"PI5_POWER_USBC_RIGHT_ANGLE_PLUG_RESERVE", (0, 0, -1), "W10"),
    "J10_1": (r"C3_J10_1_MICROFIT3_2P_MATED_PLUG|C3_CARRIER_EDGE_CONNECTOR_J101_RESERVE", (1, 0, 0), "W11"),   # the "J101" box is J10-1's own plug/lead reserve (C3_POWER_PLUG_RESERVE)
    "J10_2": (r"\w*J10_2\w*MATED_PLUG\w*", (0, 0, 1), "W25"),
    # compute
    "J9_1": (r"C0_\w*J9_1\w*", (0, 1, 0), "W24"),   # SM06B side-entry: the mated plug and its lead face +Y (2026-11-17)
    "J9_2": (r"C0_\w*J9_2\w*", (0, 0, 1), "W25"),
    "J9_3": (r"C0_\w*J9_3\w*", (0, 0, 1), "W26"),
    "J9_4": (r"C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE", (0, 0, 1), "W41"),
    "FAN": (r"ENCLOSURE_FAN_3010\w*", (1, 0, 0), "W41"),
    # audio
    "HUB_MIC_HEADERS": (r"D109_W27_FOUR_2X3_MIC_HEADERS_MATED_ENVELOPE", (-1, 0, 0), "W27"),
    "HUB_W26_PADS": (r"D109_AUDIO_HUB_V2_PERFBOARD", (0, 0, 1), "W26"),
    "SPEAKER_BREAK": (r"D109_W28_SPEAKER_INLINE_BREAK_ENVELOPE", (1, 0, 0), "W28"),
    # D-109 Level 2 parts
    "CHARGE_SPLICE_NEG": (r"D109_CHARGE_SPLICE_NEG_AWG16_ENVELOPE", (0, 0, 1), "W03r W04 W05"),
    "SHARED_5V_POS": (r"D109_SHARED_5V_POS_SPLICE_ENVELOPE", (1, 0, 0), "W05s W11 W12 W14"),
    "SHARED_5V_NEG": (r"D109_SHARED_5V_NEG_SPLICE_ENVELOPE", (1, 0, 0), "W05s W11 W12 W14"),
    "SS34": (r"D109_W11_SS34_POTTED_JOINT_ENVELOPE", (0, 0, 1), "W11"),
    "REAR_BREAK": (r"D109_J6_REAR_BREAK_MICROFIT3_1X6_MATED_ENVELOPE", (0, -1, 0), "J6 W40 W44"),
    "AMP": (r"M8_\w*BOARD\w*", (0, 0, -1), "W12"),
    "AMP_TERMINAL": (r"M8_SPEAKER_SCREW_TERMINAL_UNMEASURED", (1, 0, 0), "W28"),
    "SPEAKER": (r"SPEAKER_K50WP_MAGNET", (-1, 0, 0), "W28"),
    "MIC_FRONT_L": (r"M9_INMP441_FRONT_L_PIGTAIL_RESERVE", (0, -1, 0), "W27"),
    "MIC_FRONT_R": (r"M9_INMP441_FRONT_R_PIGTAIL_RESERVE", (0, 1, 0), "W27"),
    "MIC_REAR_L": (r"M9_INMP441_REAR_L_PIGTAIL_RESERVE", (0, -1, 0), "W27"),
    "MIC_REAR_R": (r"M9_INMP441_REAR_R_PIGTAIL_RESERVE", (0, 1, 0), "W27"),
}

# PCB-08 rev B J6 bare pads (no solid in the board STEP).
FIXED = {
    # J6 bare pads at layout_pcb08.py PLACE (91.5, 144) -> world about (-6, -43.4): KiCad x - 97.5, 100.6 - KiCad y (from J3/J5)
    "PCB08_J6_PADS": ((-8.5, -45.0, 112.035, -3.5, -42.0, 113.565), (0, 0, 1), "W17"),
}


# W27 skin exits (shell-dressed leads, study_d109_mic_leads.py): 3 mm cubes at the exit points.
def _skin_exits():
    import json
    from pathlib import Path
    path = Path(__file__).resolve().with_name("d109-mic-leads.json")
    if not path.exists():
        return {}
    out = {}
    for name, d in json.loads(path.read_text()).items():
        x, y, z = d["skin_exit"]
        out[f"SKIN_EXIT_{name}"] = ((x - 1.5, y - 1.5, z - 1.5, x + 1.5, y + 1.5, z + 1.5), (1, 0, 0), "W27")
    return out


FIXED.update(_skin_exits())


def mouth(box, direction):
    """Centre of the box face the wire leaves through."""
    x0, y0, z0, x1, y1, z1 = box
    c = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]
    lo, hi = (x0, y0, z0), (x1, y1, z1)
    for i, d in enumerate(direction):
        if d:
            c[i] = hi[i] if d > 0 else lo[i]
    return tuple(round(v, 3) for v in c)


def resolve(leaves):
    """{name: dict(label, box, mouth, direction, wires)}; missing endpoints get box None."""
    out = {}
    for name, (pattern, d, wires) in ENDPOINTS.items():
        hits = [lf for lf in leaves if re.fullmatch(pattern, lf.label)]
        if not hits:
            out[name] = dict(label=pattern, box=None, mouth=None, direction=d, wires=wires, matches=0)
            continue
        boxes = [lf.box for lf in hits]
        box = tuple(min(b[i] for b in boxes) for i in range(3)) + tuple(max(b[i] for b in boxes) for i in range(3, 6))
        out[name] = dict(label=hits[0].label, box=box, mouth=mouth(box, d), direction=d, wires=wires, matches=len(hits))
    for name, (box, d, wires) in FIXED.items():
        out[name] = dict(label=f"FIXED:{name}", box=box, mouth=mouth(box, d), direction=d, wires=wires, matches=1)
    return out
