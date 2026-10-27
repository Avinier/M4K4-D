"""Makad v1, the whole robot: chassis v1, body v1 and head v1 from their live sources."""

from pathlib import Path
import re
import sys

from build123d import Box, Compound, Cylinder, Location, Plane, Polygon, Shape, extrude

BUILD = Path(__file__).resolve().parents[3]
HEAD_CAD = BUILD / "03-head" / "v1" / "cad"
BODY_CAD = BUILD / "02-body" / "v1" / "cad"


def _use_subsystem_paths():
    """Put head then body CAD first on sys.path; head names win over body ones."""
    for path in (str(BODY_CAD), str(HEAD_CAD)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)


_use_subsystem_paths()
import layout_model
from layout_model import build_parts
from inspection_scene import parts_scene
import details, harness, mass_layout, motion_envelope, optics
from body_v1_model import (build_body_assembly, chassis_v1_reference,
                           HEAD_ORIGIN_IN_CHASSIS, yaw_drive_moving_local)


def build_robot(label="Makad v1"):
    # cadgen restores sys.path after loading the entry, but the head source
    # imports cad_cache, relief_worker and run_checks lazily inside build_parts().
    _use_subsystem_paths()
    head = Compound(label="Head v1", children=[
        *parts_scene(build_parts()).children,
        yaw_drive_moving_local(),
    ]).moved(Location(HEAD_ORIGIN_IN_CHASSIS))
    robot = Compound(label=label, children=[
        chassis_v1_reference(), build_body_assembly(), head,
    ])
    return _group_custom_pcbs(_apply_droid_cuts(robot))


# Droid-level CAD changes. From 2026-10-14 the droid's CAD changes are made in
# this folder, not in the subsystem sources (04-pcbs/README.md#rules), so the
# subsystem checks do not see them. Each DROID_CUTS entry cuts a world-frame box
# (x0, x1, y0, y1, z0, z1) from every part whose label fully matches; each
# DROID_ADDS entry unions one in (a box, or a world-frame shape); each DROID_MOVES
# entry shifts every matching part by a world-frame (dx, dy, dz).


# D-065: PCB-11 status-LED socket, fused into the inside of the bezel's crown. Head
# frame R, mm; at the neutral pose the head frame is the world frame shifted by
# HEAD_ORIGIN_IN_CHASSIS. The board (5 x 5 x 0.8) goes into the pocket from behind and
# rests on a 0.5 mm shoulder round its front edge; the light pipe goes in from the front
# through the crown bore and stops on the lip. check_pcb11_socket.py measures it.
PCB11_SOCKET = dict(
    board=(-8.0, -7.2, 12.7, 17.7, 89.3, 94.3),    # the CAD board, PCB-11 README envelope
    outer=(-8.0, -1.9, 11.8, 18.6, 88.4, 95.2),    # 0.8 mm walls; 0.1 into the crown front wall
    pocket=(-8.1, -7.2, 12.6, 17.8, 89.2, 94.4),   # board + 0.1 per side, open at the back
    cavity=(-7.25, -5.4, 13.2, 17.2, 89.8, 93.8),  # front-part space; board local u, v 0.5-4.5
    lip=(1.3, -5.4, -5.0),                         # pipe stop: r, X range (Ø2.6 window)
    bore=(1.8, -5.0, -1.85),                       # pipe bore r, X range; joins the crown bore
)


def _x_cylinder(r, x0, x1):
    y, z = layout_model.LED_Y, layout_model.LED_Z
    return layout_model.axial(r, x1 - x0, ((x0 + x1) / 2.0, y, z))


def pcb11_socket_local():
    """The D-065 socket in head frame R, clipped to the crown's outer surface."""
    s = PCB11_SOCKET
    crown = extrude(Plane.YZ * Polygon(*layout_model.CROWN_OUTER, align=None), amount=24).moved(Location((-24, 0, 0)))
    socket = layout_model.block(*s["outer"]) & crown
    socket = socket - layout_model.block(*s["pocket"]) - layout_model.block(*s["cavity"])
    socket = socket - _x_cylinder(s["lip"][0], s["lip"][1] - 0.05, s["lip"][2] + 0.05)
    return socket - _x_cylinder(s["bore"][0], s["bore"][1], s["bore"][2])


# D-067 (amended at placement): PCB-05 hangs from the frame on three Wurth 9774080243R M2
# SMT spacers (8 mm, reflowed on its top face), one ISO 7380 M2 screw each, driven from
# above after the compute tray and PCB-09 are in. World mm. The rear screw passes the
# front upper cross rail (Z 126-135.5) and seats in a counterbore under the yaw housing
# seat (Z 135.5, R36.6 about the yaw axis); the front two pass the yaw plate (Z 134-138),
# open above. The rear corners hold no second spacer: J5-1 and the J5-2/J5-4 footprints
# leave 4.3 mm there for a 5.8 mm courtyard.
# Printed bosses on the frame meet the spacer tops. check_pcb05_mount.py measures it.
PCB05_MOUNT = dict(
    points=((48.5, 9.8), (61.3, 9.8), (61.3, -9.8)),
    rear=1,                              # the first `rear` points are under the cross rail
    board_top=115.6,
    spacer=(2.175, 0.8, 8.0),            # outer r, modelled bore r (M2 thread), length
    boss=(3.5, (126.0, 134.0, 134.0)),   # r, frame underside above each point
    bore=1.2,                            # M2 clearance, Ø2.4
    cbore=(2.0, 134.0, 135.6),           # rear only: r, floor Z, open into the housing seat
    screws=((16.0, 134.0), (20.0, 138.0), (20.0, 138.0)),  # length, head seat Z
)


def _z_cyl(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


def pcb05_mount_parts():
    """D-067 world-frame shapes: spacers on the board, bosses and bores in the frame."""
    m = PCB05_MOUNT
    sr, sb, sl = m["spacer"]
    top = m["board_top"] + sl
    spacers, bosses, bores = [], [], []
    for (x, y), roof in zip(m["points"], m["boss"][1]):
        spacers.append(_z_cyl(sr, m["board_top"], top, x, y) - _z_cyl(sb, m["board_top"] - 0.1, top + 0.1, x, y))
        bosses.append(_z_cyl(m["boss"][0], top, roof, x, y) - _z_cyl(m["bore"], top - 0.1, roof + 0.1, x, y))
        bores.append(_z_cyl(m["bore"], roof - 0.1, 138.1, x, y))
    cbores = [_z_cyl(m["cbore"][0], m["cbore"][1], m["cbore"][2], x, y) for x, y in m["points"][:m["rear"]]]
    return spacers, bosses, bores + cbores


_PCB05_SPACERS, _PCB05_BOSSES, _PCB05_CUTS = pcb05_mount_parts()


DROID_CUTS = [
    # D-059: PCB-15 component relief behind the nose Hall board, open at the top and
    # into the lead groove. D-063 deepens it 0.4 mm (to 1.3 mm) with the board.
    (r"BALL_POD_PRINTED_SEAT", (125.3, 126.6, 7.8, 12.2, 30.3, 35.01)),
    # D-063: the slot's back wall moves 0.4 mm back (X 126.5 -> 126.1); the board's
    # ends (local Y 0-0.8, 5.2-6.0) bear on it.
    (r"BALL_POD_PRINTED_SEAT", (126.1, 126.5, 6.9, 13.1, 30.3, 35.01)),
    # D-067: M2 clearance bores through the cross rail and yaw plate, rear counterbores.
    *[(r"BODY_FRAME_MAIN_PRINT", cut) for cut in _PCB05_CUTS],
    # D-067 amended: the J5-7 placeholder is 10 mm tall; the mated Micro-Fit is 6.98 (Molex), so
    # the block stops at Z 122.6, 1.0 mm under the front -Y boss (Z 123.6).
    (r"PCB05_J5_7_MICROFIT3_2P_(RA_HEADER|MATED_PLUG)", (60.0, 80.0, -35.0, -5.0, 122.6, 130.0)),
]
DROID_ADDS = [
    # D-063: the slot's front wall moves 0.4 mm back too (X 127.5 -> 127.1), beside the
    # sensor notch (Y 8.3-11.7), so the slot stays 1.0 mm wide and locates the board.
    (r"BALL_POD_PRINTED_SEAT", (127.1, 127.5, 6.9, 8.3, 30.3, 35.0)),
    (r"BALL_POD_PRINTED_SEAT", (127.1, 127.5, 11.7, 13.1, 30.3, 35.0)),
    # D-065: PCB-11 socket and light-pipe sleeve inside the crown.
    (r"front_bezel_integral_camera_crown", pcb11_socket_local().moved(Location(HEAD_ORIGIN_IN_CHASSIS))),
    # D-067: PCB-05 bosses under the frame, and the SMT spacers reflowed on the board.
    *[(r"BODY_FRAME_MAIN_PRINT", boss) for boss in _PCB05_BOSSES],
    *[(r"PCB05_AUDIO_FRONT_END_PCB", spacer) for spacer in _PCB05_SPACERS],
    # D-067 amended: the Micro-Fit 43650-0200 housing is 9.65 mm wide (Molex SD-43650-001), not the
    # placeholder's 7.26, and sits 1.5 mm further forward; header and plug grow to X 64.8-74.46, at
    # Molex's 6.98 mm mated height (the placeholder's 10 mm block is cut back in DROID_CUTS).
    (r"PCB05_J5_7_MICROFIT3_2P_RA_HEADER", (64.8, 74.46, -19.0, -9.0, 115.6, 122.6)),
    (r"PCB05_J5_7_MICROFIT3_2P_MATED_PLUG", (64.8, 74.46, -31.0, -19.0, 115.6, 122.6)),
]
DROID_MOVES = [
    # D-067 amended: J5-1 slides 2 mm toward -Y so the rear spacer fits between it and J5-2;
    # J5-2/J5-4 and J5-6 move 0.225 mm apart (their footprint courtyards touched).
    (r"PCB05_J5_1_(JST_GH_SM10B_HEADER|GHR10_MATED_PLUG)|PCB05_REAR_EDGE_PLUG_RESERVE", (0.0, -2.0, 0.0)),
    (r"PCB05_J5_[24]_(JST_GH_SM04B_HEADER|GHR04_MATED_PLUG)", (-0.225, 0.0, 0.0)),
    (r"PCB05_J5_6_(JST_GH_SM02B_HEADER|GHR02_MATED_PLUG)", (0.225, 0.0, 0.0)),
    # D-063: PCB-15 sits 0.4 mm further back (X 126.2-127.0), so U1 clears the magnet
    # at the cap's 3 mm stop.
    (r"BALL_NOSE_HALL_(CARRIER_PCB|DRV5055A3_SOT23)", (-0.4, 0.0, 0.0)),
]


def _cut_box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))


def _tool(value):
    return value if isinstance(value, Shape) else _cut_box(*value)


def _cut_parts(node, parent_location, hits):
    children = list(node.children) if getattr(node, "children", None) else []
    if children:
        here = parent_location * node.location
        kept = [_cut_parts(child, here, hits) for child in children]
        if all(k is c for k, c in zip(kept, children)):
            return node
        return _relabel(node.label, kept, node.location, node.color)
    label = node.label or ""
    edits = [(kind, entry) for kind, table in (("cut", DROID_CUTS), ("add", DROID_ADDS), ("move", DROID_MOVES))
             for entry in table if re.fullmatch(entry[0], label)]
    if not edits:
        return node
    part = node
    for kind, (_, value) in edits:
        hits[kind, value] += 1
        if kind == "cut":
            part = part - _tool(value).moved(parent_location.inverse())
        elif kind == "add":
            part = part + _tool(value).moved(parent_location.inverse())
        else:  # world-frame shift of a part placed under parent_location
            part = part.moved(parent_location.inverse() * Location(value) * parent_location)
    part.label, part.color = node.label, node.color
    return part


def _apply_droid_cuts(robot, strict=True):
    """Apply DROID_CUTS, DROID_ADDS and DROID_MOVES; every entry must hit a part.

    strict=False is for check scripts that build one subsystem tree: entries for
    parts outside it are skipped.
    """
    tables = (("cut", DROID_CUTS), ("add", DROID_ADDS), ("move", DROID_MOVES))
    hits = {(kind, value): 0 for kind, table in tables for _, value in table}
    robot = _cut_parts(robot, Location(), hits)
    missing = [pattern for kind, table in tables for pattern, value in table if not hits[kind, value]]
    assert not (strict and missing), f"droid change labels not found: {missing}"
    return robot


# Custom boards (04-pcbs/README.md register), pulled out of the subsystem trees
# into one "Custom PCBs" group so they can be shown or isolated together.
# Each pattern must fully match the label of a node in the subsystem tree; the
# node moves whole, keeping its global placement. PCB-01 is a bought BMS
# (Robocraze TIFPS0629, D-019) and stays on the pack.
CUSTOM_PCBS = [
    ("PCB-02 charger, latch and pack sense", r"PCB02_CHARGE_AND_SYSTEM_POWER"),
    ("PCB-03 motor gate and head 5 V rail", r"PCB03_MOTOR_GATE_AND_HEAD_RAIL"),
    ("PCB-04 branch converters", r"PCB04_BRANCH_CONVERTERS"),
    ("PCB-05 audio front end", r"PCB05_AUDIO_FRONT_END|PCB05_CONNECTORS"),
    ("PCB-06 PDM microphone boards x4", r"PDM_MIC_(FRONT|REAR)_[LR]"),
    ("PCB-07 base IMU", r"IMU_PCB07"),
    ("PCB-08 yaw junction", r"YAW_JUNCTION_PCB08"),
    ("PCB-09 C0 link adapter", r"C0_LINK_ADAPTER_PCB09"),
    ("PCB-10 C3 controller carrier", r"C3_CARRIER_PCB10_WITH_DEVKITC"),
    ("PCB-11 status LED carrier", r"status_LED_(PCB08_carrier_5x5|WS2812B_2020)"),
    # Only the ESP32-S3-Zero module is drawn; the carrier board is not modelled yet.
    ("PCB-12 C2 head controller", r"C2_ESP32_S3_Zero_23_5x18_footprint"),
    ("PCB-13 charge inlet", r"CHARGE_INLET_PCB13"),
    ("PCB-14 yaw rotor joiners x3", r"PCB14_JOINER_(BOARD|LOWER_ZIF|UPPER_ZIF)_[1-3]"),
    ("PCB-15 nose Hall carrier", r"BALL_NOSE_HALL_(CARRIER_PCB|DRV5055A3_SOT23)"),
]
# Printed frame parts inside a board group stay where they are.
STAYS_IN_PLACE = re.compile(r"BODY_FRAME_\w+")
_PCB_RULES = [(name, re.compile(pattern)) for name, pattern in CUSTOM_PCBS]


def _board_group(label):
    return next((name for name, rule in _PCB_RULES if rule.fullmatch(label or "")), None)


def _relabel(label, children, location, color=None):
    group = Compound(label=label, children=children)
    group.location = location
    if color is not None:
        group.color = color
    return group


def _pull_pcbs(node, parent_location, found):
    """Return node without its board parts (None if nothing is left); collect them in found."""
    here = parent_location * node.location
    children = list(node.children) if getattr(node, "children", None) else []
    board = _board_group(node.label)
    if board:
        stays = [c for c in children if STAYS_IN_PLACE.fullmatch(c.label or "")]
        if not stays:
            node.location = here
            found[board].append(node)
            return None
        moved = [c for c in children if all(c is not s for s in stays)]
        found[board].append(_relabel(node.label, moved, here))
        return _relabel(node.label, stays, node.location)
    if not children:
        return node
    kept = [_pull_pcbs(child, here, found) for child in children]
    if all(k is c for k, c in zip(kept, children)):
        return node
    kept = [k for k in kept if k is not None]
    return _relabel(node.label, kept, node.location, node.color) if kept else None


def _group_custom_pcbs(robot):
    found = {name: [] for name, _ in CUSTOM_PCBS}
    rest = _pull_pcbs(robot, Location(), found)
    missing = [name for name, parts in found.items() if not parts]
    assert not missing, f"custom PCB labels not found in the subsystem trees: {missing}"
    pcbs = Compound(label="Custom PCBs", children=[
        Compound(label=name, children=parts) for name, parts in found.items()
    ])
    return _relabel(robot.label, [*rest.children, pcbs], robot.location)


def gen_step():
    return {"shape": build_robot()}
