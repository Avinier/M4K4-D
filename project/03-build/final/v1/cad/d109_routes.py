"""D-109 Level 3: body-harness route reserves (world boxes x0, x1, y0, y1, z0, z1).

Same method as D106_ROUTES: a box round each bundle with bend room; each chain
is a list of boxes whose neighbours overlap, from one endpoint
(body_harness_endpoints) to another. "D106:<name>" reuses a chassis box.
Checked by check_d109_routes.py. All `E`.
"""

ROUTES = {
    # T1 rear bay: W03r, W04, W05, W05c body half
    "T1_JBAT_AFT": (-42.0, -19.5, -31.0, -26.0, 72.0, 76.0),
    "T1_POS_SPLICE_SIDE": (-45.0, -40.0, -33.0, -28.5, 72.0, 88.0),
    "T1_SPLICE_TO_XT30": (-42.0, -38.0, -28.5, -13.0, 71.2, 76.0),
    "T1_XT30_UP": (-43.5, -38.0, -16.0, -13.0, 61.5, 75.2),
    "T1_XT30_LOW": (-45.5, -38.0, -16.0, -3.0, 61.5, 70.5),         # under the rear-plate cradle (Z 70.7)
    "T1_M1_M6_FRONT": (-42.0, -37.5, -30.0, 3.0, 76.0, 92.0),
    "T1_M1_M6_GAP": (-44.4, -37.5, -1.6, 3.0, 76.0, 90.0),
    "T1_TO_STARS": (-37.5, -24.0, -14.0, 13.4, 77.5, 82.0),          # frame member at Y >= 13.5
    "T1_STARS_TO_JCH": (-27.5, -20.0, 12.0, 26.0, 71.0, 77.5),
    # T2 tray feed: W05b, W05s, W11
    "T2_STARS_FWD": (-22.0, -19.0, -14.0, 13.4, 71.0, 79.0),
    "T2_M5_TO_S5": (-19.0, 6.0, -46.0, -35.2, 74.5, 80.0),
    "T2_W10_FROM_M4": (3.86, 10.0, -3.3, 21.7, 72.0, 84.4),
    "T2_W10_TO_DROP": (-3.0, 10.0, -46.0, -39.0, 80.5, 84.4),
    "T2_W10_TRAY_DROP": (-3.0, 3.0, -46.0, -39.0, 77.0, 92.2),        # the old Pi pigtail passage through the tray
    "T2_W11_UP_FROM_SS34": (3.0, 21.0, -41.5, -35.5, 78.5, 84.4),
    "T2_W11_FWD": (3.0, 60.0, -46.0, -38.0, 80.0, 84.4),             # over the right motor inline pair (Z 80), under the tray
    "T2_W11_DROP": (56.0, 60.0, -46.5, -38.0, 74.5, 84.4),           # between the inline pair (X 56) and the tray column (X 60)
    "T2_W11_UNDER_J10_1": (56.0, 68.0, -56.0, -46.5, 74.5, 77.8),    # under the plug and its lead reserve (Z 77.9)
    "T2_W11_REAR_UP": (68.0, 74.0, -56.0, -46.5, 74.5, 77.8),        # up into J10-1's lead reserve behind the plug
    # T3 -Y riser: W13, W14, W17 (behind the tray's rear edge, X -35.5)
    "T3_JS18_AFT": (-45.0, -12.0, -46.0, -38.0, 70.0, 75.0),
    "T3_S5_TO_RISER": (-45.0, -18.0, -46.0, -38.0, 74.5, 80.0),
    "T3_RISER": (-45.0, -40.0, -46.0, -38.0, 70.0, 117.5),         # shell above Z 117.8
    "T3_TO_J8_1": (-45.0, -32.42, -41.0, -29.0, 114.0, 117.5),
    "T3_TO_PCB08_J6": (-45.0, -3.5, -45.4, -42.9, 115.0, 117.5),
    "T3_J6_PAD_DROP": (-8.5, -3.5, -45.4, -42.9, 113.6, 117.5),
    # T4 compute: W24, W25, W41, J6 lead
    "T4_W24_UP": (33.0, 40.0, 36.5, 42.2, 112.3, 117.5),
    "T4_W24_MINUS_Y": (27.5, 35.5, -11.5, 42.2, 112.5, 117.5),       # between the yaw servo (X 26.1) and J9-4 (X 37); over the Pi
    "T4_W24_ACROSS_X": (-8.7, 35.5, -11.5, -6.0, 112.5, 116.0),      # +Y of the D-107 camera mount (Y -12); under the HDMI pairs (Z 116.6)
    "T4_W24_TO_J8_4": (-8.7, 0.0, -22.7, -6.0, 114.0, 122.6),
    "T4_W25_J10_2_UP": (-3.4, 5.4, -52.6, -49.4, 88.5, 98.5),
    "T4_W25_CHANNEL": (-3.4, 57.0, -52.6, -48.0, 95.3, 98.5),       # DevKitC pins hang to Z 98.6,        # over the GH plugs (Z 95.2), under the DevKitC (97.6)
    "T4_W25_RISE": (53.0, 57.0, -52.6, -49.5, 95.3, 121.0),          # outboard of the Pi camera FPC (Y -48),
    "T4_W25_TO_FRONT": (53.0, 65.0, -52.6, -49.5, 118.5, 121.0),
    "T45_FRONT_RIGHT_CORRIDOR": (61.5, 65.0, -50.0, 41.0, 117.0, 125.0),  # +X of the B0091 HDMI parts, over its board
    "T4_W25_TO_J9_2": (52.0, 65.0, 24.0, 30.0, 115.45, 121.0),
    "T4_W41_A": (32.5, 39.0, 58.9, 68.9, 118.0, 124.0),
    "T4_W41_B": (33.0, 39.0, 28.0, 58.9, 118.0, 124.0),
    "T4_J6_RISE": (70.5, 73.5, 29.5, 32.5, 115.5, 119.5),
    "T4_J6_SHIFT": (70.5, 73.5, 18.5, 32.5, 116.0, 119.5),
    "T4_J6_AFT": (-44.0, 73.5, 18.5, 21.5, 116.0, 119.5),
    "T4_J6_DROP": (-44.0, -38.0, 18.5, 24.0, 101.0, 119.5),
    # T5 audio: W26, W27 x4, W28, W12
    "T5_W26_UP": (54.0, 58.0, 30.5, 35.5, 115.45, 125.5),
    "T5_W26_OVER": (54.0, 64.8, 30.5, 50.0, 122.5, 125.5),
    # W27 free tails (F2 fix): the leads are dressed on the shell skin (study_d109_mic_leads.py)
    # to exits in the open front; only these tails move relative to the shell. Each box admits
    # the 2x3 plug section (5.6 x 8.1, E) across its travel.
    "T5_TAIL_IN_PY": (74.5, 80.1, 58.0, 74.0, 100.0, 110.0),        # from the +Y skin exits inboard, low
    "T5_TAIL_IN_NY": (74.5, 80.1, -74.0, -58.0, 100.0, 110.0),
    "T5_TAIL_UP_NY": (74.5, 80.1, -64.5, -56.0, 100.0, 132.0),       # inside the narrowing skin; 8.5 wide for the plug
    "T5_TAIL_CROSS_HIGH": (74.5, 80.1, -64.5, 62.0, 123.5, 132.0),   # over the Pi/PCB-09 (X 78) and the amp terminal (Z 121.4); shell front wall at X 80.2
    "T5_TAIL_UP": (74.5, 80.1, 53.2, 62.0, 106.0, 132.0),           # +Y of the amp terminal (Y 53)
    "T5_TAIL_OVER_HUB": (53.6, 80.1, 41.0, 58.5, 123.5, 132.0),     # over the hub bracket and amp; frame lip at X < 53.5
    "T5_TAIL_DOWN": (53.6, 62.0, 41.0, 58.5, 110.0, 132.0),         # down to the hub headers' mouths
    "T5_W28_A": (79.9, 84.0, 34.0, 53.0, 104.0, 119.0),
    "T5_W28_B": (78.0, 81.9, 10.0, 36.0, 100.0, 106.0),
    "T5_W12_CROSS": (5.5, 10.0, -46.0, 30.0, 78.0, 84.4),            # under the tray to beyond its +Y edge (23.5)
    "T5_W12_UNDER_PY": (4.0, 32.0, 24.0, 30.0, 78.0, 84.4),          # under the yaw servo (Z 84.6)
    "T5_W12_PY_RISE": (27.0, 32.0, 23.6, 32.0, 78.0, 100.0),          # +X of the yaw servo
    "T5_W12_PY_FWD": (27.0, 72.0, 26.0, 32.0, 95.0, 100.0),          # under PCB-09 (Z 106.4)
    "T5_W12_JOG": (70.0, 80.5, 26.0, 38.5, 95.0, 103.0),
    "T5_W12_TO_AMP": (72.3, 80.5, 38.0, 46.0, 99.5, 103.0),          # over the fuse holder (Z 99)
    "T5_W12_AMP_PINS": (71.6, 72.3, 42.7, 46.0, 100.0, 103.0),
    # T6 rear panel and control: W40, W44 tails; mushroom keep-out is X -50..-26, Y +-11, Z 94.5-116.5
    "T6_BREAK_TO_M6": (-43.6, -38.0, 14.0, 24.5, 90.5, 94.0),
    "T6_BREAK_FWD": (-35.5, -22.0, 14.0, 18.0, 100.0, 105.0),
    "T6_PASS_KEEPOUT": (-26.0, -22.0, -18.5, 18.0, 100.0, 105.0),
    "T6_TO_BUFFER": (-43.5, -22.0, -18.5, -11.5, 100.0, 105.0),
    "T6_MUSHROOM_TO_BUFFER": (-43.5, -30.0, -13.0, -11.0, 96.5, 104.0),   # above the tray rear edge plus its 2 mm lift,
    "T6_BUFFER_TO_M1": (-42.0, -36.5, -18.5, -11.5, 92.0, 94.0),
}

# chain: (start endpoint, [boxes], end endpoint)
CHAINS = {
    "W03r": ("J_BAT_BODY", ["D106:J_BAT_BODY_EXIT", "T1_JBAT_AFT", "T1_POS_SPLICE_SIDE"], "CHARGE_SPLICE_POS"),
    "W03r-": ("J_BAT_BODY", ["D106:J_BAT_BODY_EXIT", "T1_JBAT_AFT"], "CHARGE_SPLICE_NEG"),
    "W04": ("CHARGE_SPLICE_POS", ["T1_POS_SPLICE_SIDE", "T1_SPLICE_TO_XT30", "T1_XT30_UP", "T1_XT30_LOW"], "XT30"),
    "W05 M1": ("CHARGE_SPLICE_POS", ["T1_POS_SPLICE_SIDE", "T1_M1_M6_FRONT"], "M1"),
    "W05 M6": ("M1", ["T1_M1_M6_FRONT", "T1_M1_M6_GAP"], "M6"),
    "W05 stars": ("M6", ["T1_M1_M6_GAP", "T1_TO_STARS"], "STAR_POS"),
    "W05c": ("STAR_NEG", ["T1_STARS_TO_JCH", "D106:J_CHASSIS_BODY_EXIT"], "J_CHASSIS_BODY"),
    "W05b M4": ("STAR_NEG", ["T2_STARS_FWD"], "M4"),
    "W05b M5": ("STAR_NEG", ["T2_STARS_FWD"], "M5"),
    "W10": ("M4", ["T2_W10_FROM_M4", "T5_W12_CROSS", "T2_W10_TO_DROP", "T2_W10_TRAY_DROP"], "PI_USBC"),
    "W05s": ("M5", ["T2_M5_TO_S5"], "SHARED_5V_POS"),
    "W11": ("SHARED_5V_POS", ["T2_M5_TO_S5"], "SS34"),
    "W11 J10-1": ("SS34", ["T2_W11_UP_FROM_SS34", "T2_W11_FWD", "T2_W11_DROP", "T2_W11_UNDER_J10_1", "T2_W11_REAR_UP"], "J10_1"),
    "W14": ("SHARED_5V_POS", ["T2_M5_TO_S5", "T3_S5_TO_RISER", "T3_RISER", "T3_TO_J8_1"], "J8_1"),
    "W13": ("J_S18_H_BODY", ["D106:JS18_BODY_LEADS", "T3_JS18_AFT", "T3_RISER", "T3_TO_J8_1"], "J8_1"),
    "W17": ("J_S18_Y_BODY", ["D106:JS18_BODY_LEADS", "T3_JS18_AFT", "T3_RISER", "T3_TO_PCB08_J6", "T3_J6_PAD_DROP"], "PCB08_J6_PADS"),
    "W24": ("J9_1", ["T4_W24_UP", "T4_W24_MINUS_Y", "T4_W24_ACROSS_X", "T4_W24_TO_J8_4"], "J8_4"),
    "W25": ("J10_2", ["T4_W25_J10_2_UP", "T4_W25_CHANNEL", "T4_W25_RISE", "T4_W25_TO_FRONT",
                      "T45_FRONT_RIGHT_CORRIDOR", "T4_W25_TO_J9_2"], "J9_2"),
    "W41": ("FAN", ["T4_W41_A", "T4_W41_B"], "J9_4"),
    "J6 lead": (None, ["T4_J6_RISE", "T4_J6_SHIFT", "T4_J6_AFT", "T4_J6_DROP"], "REAR_BREAK"),
    "W44": ("REAR_BREAK", ["T6_BREAK_TO_M6"], "M6"),
    "W40 sense": ("REAR_BREAK", ["T6_BREAK_FWD", "T6_PASS_KEEPOUT", "T6_TO_BUFFER"], "BUTTON_BUFFER"),
    "W40 switch": ("MUSHROOM", ["T6_MUSHROOM_TO_BUFFER"], "BUTTON_BUFFER"),
    "W40 M1": ("BUTTON_BUFFER", ["T6_BUFFER_TO_M1"], "M1"),
    "W26": ("J9_3", ["T5_W26_UP", "T5_W26_OVER"], "HUB_W26_PADS"),
    "W27 FL": ("HUB_MIC_HEADERS", ["T5_TAIL_DOWN", "T5_TAIL_OVER_HUB", "T5_TAIL_UP", "T5_TAIL_IN_PY"], "SKIN_EXIT_FRONT_L"),
    "W27 FR": ("HUB_MIC_HEADERS", ["T5_TAIL_DOWN", "T5_TAIL_OVER_HUB", "T5_TAIL_CROSS_HIGH", "T5_TAIL_UP_NY", "T5_TAIL_IN_NY"], "SKIN_EXIT_FRONT_R"),
    "W27 RL": ("HUB_MIC_HEADERS", ["T5_TAIL_DOWN", "T5_TAIL_OVER_HUB", "T5_TAIL_UP", "T5_TAIL_IN_PY"], "SKIN_EXIT_REAR_L"),
    "W27 RR": ("HUB_MIC_HEADERS", ["T5_TAIL_DOWN", "T5_TAIL_OVER_HUB", "T5_TAIL_CROSS_HIGH", "T5_TAIL_UP_NY", "T5_TAIL_IN_NY"], "SKIN_EXIT_REAR_R"),
    "W28": ("AMP_TERMINAL", ["T5_W28_A", "T5_W28_B"], "SPEAKER"),
    "W12": ("SHARED_5V_POS", ["T2_M5_TO_S5", "T5_W12_CROSS", "T5_W12_UNDER_PY", "T5_W12_PY_RISE", "T5_W12_PY_FWD",
                              "T5_W12_JOG", "T5_W12_TO_AMP", "T5_W12_AMP_PINS"], "AMP"),
}


def box(entry, name):
    return entry.D106_ROUTES[name[5:]] if name.startswith("D106:") else ROUTES[name]
