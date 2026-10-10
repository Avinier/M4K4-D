"""Head turntable on the body yaw stage (D-044/D-048/D-052): review scene.

Parts come from the live sources: body_yaw_stage() and yaw_drive_moving_parts()
for the body side, the head v1 part cache for the disc, its three hub screws and
the head FFC stack. The frame is cropped to the yaw plate and servo pad. The
disc and the frame crop are translucent so the hub, rotor and PCB-14 boards
read through them. `exploded` lifts each install group along Z in the order
of the body CAD README's yaw-stage assembly steps; offsets are display only.
"""
import os
import sys

os.environ.setdefault("MAKAD_RELIEF_SERIAL", "1")

from build123d import Compound, Location

import body_v1_model as b

DISC_ALPHA = 0.25
FRAME_ALPHA = 0.3

# Group: (label, Z lift in the exploded view). Order follows assembly.
GROUPS = {
    "frame": ("0 Frame yaw plate and servo pad (cropped)", 0.0),
    "servo": ("1 ST3215-HS servo, mount screws, drive hub and shaft (from below)", 0.0),
    "stationary": ("2 Cartridge: housing, 61810-2Z bearing, clamp ring", 70.0),
    "hub": ("2a Hub and driven gear (drops in from the top)", 90.0),
    "rotor": ("2b Rotor, PCB-14 joiner boards, FFC inner ends (rise from below)", 45.0),
    "stator": ("2c FFC cassette stator and rolling loop (from below)", 25.0),
    "pinion": ("3 Scissor pinion and preload spring (drop onto the shaft)", 28.0),
    "disc": ("4 Head turntable disc, 3 x M3 to the hub, head FFCs", 115.0),
}


def _group_of(label):
    if label.startswith("YAW_FLANGE_M3X4_FRAME_INSERT"):
        return "frame"
    if label.startswith("YAW_DRIVE_SCISSOR_") or label.startswith("YAW_SCISSOR_PRELOAD"):
        return "pinion"
    if label.startswith(("YAW_DRIVE_HUB", "YAW_PINION_SHAFT", "YAW_SERVO_", "HS_", "ST3215")):
        return "servo"
    if label.startswith(("YAW_HUB_",)):
        return "hub"
    if label.startswith(("YAW_ROTOR_", "PCB14_")):
        return "rotor"
    if label.startswith(("YAW_FFC_CASSETTE_STATOR", "YAW_CASSETTE_", "YAW_FFC_ROLLING_LOOP")):
        return "stator"
    return "stationary"


def _leaves(shape):
    kids = list(shape.children) if getattr(shape, "children", None) else []
    if not kids:
        return [shape]
    out = []
    for k in kids:
        out += _leaves(k)
    return out


def _head_parts():
    if str(b.HEAD_DIR) not in sys.path:
        sys.path.insert(0, str(b.HEAD_DIR))
    from cad_cache import load_parts
    from harness import routes
    parts = load_parts(catalog=False)
    origin = Location(b.HEAD_ORIGIN_IN_CHASSIS)
    out = []
    disc = parts["yaw_turntable_disc_flush"]["shape"].moved(origin)
    out.append(b._paint(disc, "HEAD_TURNTABLE_DISC_TRANSLUCENT", "#647787", DISC_ALPHA))
    for name, d in parts.items():
        if name.startswith("yaw_disc_to_body_hub_M3x6_"):
            out.append(b._paint(d["shape"].moved(origin), name.upper(), "#B7BFC0", 1.0))
    jackets, _gaps = routes()
    for name, d in jackets.items():
        if name.startswith("yaw_FFC_x3_"):
            out.append(b._paint(d["shape"].moved(origin), "HEAD_" + name.upper(), "#D3A860", 0.8))
    return out


def _frame_crop():
    frame = next(p for p in _leaves(b.body_primary_frame()) if (p.label or "") == "BODY_FRAME_MAIN_PRINT")
    ax = b.BODY_AXIS_X
    window = b._block(ax - 46.0, ax + 46.0, -46.0, 52.0, 118.0, 142.0)
    crop = frame & window
    return b._paint(crop, "BODY_FRAME_YAW_PLATE_AND_SERVO_PAD_CROP", "#5B7FA6", FRAME_ALPHA)


def scene(exploded=False):
    groups = {k: [] for k in GROUPS}
    groups["frame"].append(_frame_crop())
    for p in _leaves(b.body_yaw_stage()) + _leaves(Compound(children=b.yaw_drive_moving_parts(0.0))):
        label = p.label or ""
        if label == "YAW_SERVO_ST3215_HS_STEP" or not label:
            label = "HS_SERVO_SOLID"
            p.label = label
        groups[_group_of(label)].append(p)
    groups["disc"] += _head_parts()
    children = []
    for key, (title, lift) in GROUPS.items():
        parts = groups[key]
        if not parts:
            continue
        g = Compound(label=title, children=parts)
        if exploded and lift:
            g = g.moved(Location((0.0, 0.0, lift)))
        children.append(g)
    title = "Yaw turntable on the body yaw stage" + (" (exploded in assembly order)" if exploded else "")
    return Compound(label=title, children=children)
