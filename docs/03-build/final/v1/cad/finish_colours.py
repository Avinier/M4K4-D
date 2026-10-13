"""Real finish colours for the presentation view (printguide.md §4).

The subsystem models colour parts so they can be told apart in inspection
views. The presentation view paints every part its real filament, paint or
hardware colour instead. RULES are matched in order against the leaf label,
then PATH_RULES against the group path above it; the first match wins. A leaf no rule
matches keeps its model colour: purchased parts (motors, servos, PCBs,
speaker, display, camera, button) are meant to fall through.
"""

import re

# printguide.md §4. Matte, clean base colours; weathering is not drawn.
PALETTE = {
    # Tuned by eye in the cadgen viewer, whose cool lighting adds blue and
    # removes yellow. Under neutral light (Fusion, real filament) four of them
    # need the values in NEUTRAL_LIGHT below to give the same look.
    "ivory": "#DDD4BA",          # ASA skins: body shell, arch pods, head (richer than the model's #E3DDC9)
    "taupe": "#A9A28E",          # ASA body service panels, rear TCRT keel
    "amber": "#B88636",          # accents
    "signal_amber": "#D39F36",   # power-button bezel
    "deep_slate": "#4F575B",     # frames, neck disc, ear centres
    "slate_blue": "#6F8189",     # wheel rims and clamp rings: deep slate, lighter
    "gunmetal": "#3A464D",       # hub caps
    "aluminium": "#9DA3A6",      # the real aluminium axle caps
    "carbon": "#2A2C2E",         # CF yoke legs
    "tyre_black": "#2B3034",     # TPU 95A
    "brass": "#C38A47",          # heat-set inserts
    "steel": "#B7BFC0",          # A2 stainless screws, nuts, shafts
}

# The same finishes under neutral light: the Fusion makad-v1 appearances and
# the values to match filament or paint to (printguide.md §4). Not used here.
NEUTRAL_LIGHT = {
    "ivory": "#DAD5C3",
    "taupe": "#9D9886",
    "deep_slate": "#34495C",
    "slate_blue": "#587A94",
}

# (pattern, palette name). Case-insensitive search on the leaf label first,
# then on its group path.
RULES = [
    # Skins: ASA, housing grain (printguide.md §3). Ivory shell, taupe panels.
    (r"^BODY_SHELL$", "ivory"),
    (r"^WHEEL_ARCH_POD_[LR]$", "ivory"),
    (r"^(FRONT|REAR)_SERVICE_PANEL", "taupe"),
    (r"^REAR_KEEL_FACETED_BODY$", "taupe"),
    (r"^REAR_TCRT_BEZEL_WITH_GUARDS$", "taupe"),
    (r"^BALL_NOSE_TOUCH_CAP$", "ivory"),
    (r"^front_bezel_integral_camera_crown$", "ivory"),
    (r"^main_octagonal_skin(_lower)?$", "ivory"),
    (r"^removable_octagonal_rear_cover$", "ivory"),
    (r"^ear_.*_hollow_removable_cap$", "ivory"),
    # Accents.
    (r"^REAR_PANEL_BUTTON_AMBER_BEZEL$", "signal_amber"),
    (r"^WHEEL_ARCH_UPPER_TRIM_[LR]$", "amber"),
    (r"_amber_inlay$", "amber"),
    (r"^yaw_yoke_spine_inlay", "amber"),
    # Metal casing: blue anodised look in the frame's blue family.
    (r"^WHEEL_[LR]_(RIM|CLAMP_RING)_PETG$", "slate_blue"),
    (r"^yaw_turntable_disc_flush$", "deep_slate"),
    (r"_dark_centre$", "deep_slate"),
    (r"^WHEEL_[LR]_HUB_CAP_PETG$", "gunmetal"),
    (r"^AXLE_BEARING_CAP_[LR]$", "aluminium"),  # the 1.2 mm aluminium cap (D-007)
    # Raw CF.
    (r"^yaw_yoke_leg", "carbon"),
    (r"^pitch_trunnion_retainer$", "carbon"),
    (r"^WHEEL_[LR]_TYRE_", "tyre_black"),
    # Hidden structure: deep slate PETG (chassis, body) and PLA (head).
    (r"^CHASSIS_FRAME_(FRONT|REAR)_MODULE$", "deep_slate"),
    (r"^AXLE_(BEARING_HOUSING|MOTOR_CARRIER)_[LR]$", "deep_slate"),
    (r"^BATTERY_TUB_BOTTOM_HATCH$", "deep_slate"),
    (r"^BALL_POD_(PRINTED_SEAT|SENSOR_LID)$", "deep_slate"),
    (r"^REAR_KEEL_REPLACEABLE_WEAR_SHOE$", "deep_slate"),
    (r"^REAR_TCRT_HEIGHT_SHIM", "deep_slate"),
    (r"^BODY_FRAME_(MAIN_PRINT|FRONT_LEFT_FOOT_CASSETTE|C3_CARRIER_UPRIGHT)", "deep_slate"),
    (r"^COMPUTE_TRAY$", "deep_slate"),
    (r"^YAW_(CARTRIDGE_HOUSING|BEARING_CLAMP_RING|FFC_CASSETTE_STATOR|DRIVE_HUB_ON_ST3215_HS_HORN"
     r"|DRIVE_SCISSOR_PINION_(FIXED|SPRUNG)_HALF|HUB_DRIVEN_GEAR_M1_Z37|ROTOR_CLAMP_DRUM_AND_STOP_DOG)$",
     "deep_slate"),
    (r"^connected_pitch_frame_roll_servo_saddle$", "deep_slate"),
    (r"^connected_rolling_cradle_flange_ear_stalks$", "deep_slate"),
    (r"^bearing_cartridge_trial$", "deep_slate"),
    (r"^roll_bearing_retainer", "deep_slate"),
    (r"^display_rear_frame$", "deep_slate"),
    (r"^CSI_roof_straight_exit_guide$", "deep_slate"),
    (r"^removable_camera_edge_bracket_trial$", "deep_slate"),
    (r"^C2_removable_open_rear_tray$", "deep_slate"),
    (r"_ridged_inner_mount$", "deep_slate"),
    # Hardware.
    (r"INSERT", "brass"),
    (r"^rear_pitch_trim_washer_stack", "brass"),
    (r"_hard_stop_pin$", "steel"),  # ISO 8734 steel dowels
]

# Matched against the group path ("/robot/group/subgroup") when no leaf rule hits.
PATH_RULES = [
    (r"/Fasteners$", "steel"),  # head screws and washers, drawn dark in the head model
]

_LEAF = [(re.compile(p, re.I), name) for p, name in RULES]
_PATH = [(re.compile(p, re.I), name) for p, name in PATH_RULES]


def finish_for(label, path=""):
    """Palette name for a leaf, or None to keep the model colour."""
    for pattern, name in _LEAF:
        if pattern.search(label or ""):
            return name
    for pattern, name in _PATH:
        if pattern.search(path or ""):
            return name
    return None


def rgb(name):
    """Linear RGB for a palette name, as cadgen.srgb() stores it in a Color."""
    h = PALETTE[name].lstrip("#")
    channels = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
