"""Makad v1, the whole robot: chassis v1, body v1 and head v1 from their live sources."""

from pathlib import Path
import importlib.util
import math
import re
import sys

from build123d import Axis, Box, Compound, Cylinder, Location, Plane, Polygon, Shape, extrude

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
import body_v1_model as _body
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
    # Apply legacy mount edits before replacing their board placeholders. Existing
    # subsystem fit checks intentionally still exercise _apply_droid_cuts alone.
    if str(Path(__file__).resolve().parent) not in sys.path:   # cadgen restores sys.path after loading
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from pcb_integration import replace_completed_boards
    robot = replace_completed_boards(_group_custom_pcbs(_apply_droid_cuts(robot)),
                                     _body, HEAD_ORIGIN_IN_CHASSIS)
    # D-095: the D-093 bought modules, one group each, beside the custom PCBs.
    return _relabel(robot.label, [*robot.children, bought_modules()], robot.location)


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


def _z_cyl(r, z0, z1, x, y):
    return Cylinder(r, z1 - z0).moved(Location((x, y, (z0 + z1) / 2.0)))


# D-068: PCB-10 C3 carrier mounting and the Espressif DevKitC. World frame, mm. The carrier
# (X -14..56, Y -58.4..-56.8, Z 82..125.5) keeps its two lower M2.5 screws (Z 86); the two
# upper ones sat under the DevKitC, where no driver reaches, and are deleted. Instead each
# printed upright gets a hook over the board's top edge: the module goes in 2 mm low,
# slides up under the hooks, and the lower screws fix it. Each upright also gets a relief
# under both header rows for the DevKitC pin tails (clipped to 1.5 mm), long enough for the
# 2 mm slide. The subsystem's DevKitC is a generic board's STEP (rows 25.4 mm apart); it is
# replaced by Espressif's ESP32-S3-DevKitC-1 v1.1, built from Espressif's dimension drawing
# (DXF_ESP32-S3-DevKitC-1_V1.1_20220429; Espressif publishes no 3D model): rows 22.86 mm apart,
# keeping the subsystem's pin columns. check_pcb10_mount.py measures all of it.
PCB10_MOUNT = dict(
    uprights=((-12.0, -4.0), (20.0, 28.0)),   # X spans (C3_CARRIER_UPRIGHTS)
    board=(-14.0, 56.0, -58.4, -56.8, 82.0, 125.5),
    slide=2.0,                                # install drop below the final position
    relief=(3.0, 3.7, 1.75),                  # depth into the upright; below and above each row
    lip=(0.1, 1.7, 123.6),                    # gap to the board face, thickness, lip bottom Z
    bridge=(-60.0, 0.1, 128.0),               # Y of the rail's inboard face, gap over the edge, top Z
    pin1_x=44.853, pitch=2.54, pins=22,       # J1-1/J3-1 at the antenna end (+X)
    rows=(98.92, 121.78),                     # J1 (3V3 ... 5V, G), J3 (G, TX ... G)
    header=2.5, pcb=1.6, tail=1.5, pin=0.64,  # plastic, DevKitC board, clipped tail, pin square
)


def _blk(x0, x1, y0, y1, z0, z1, label=None):
    shape = Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))
    if label:
        shape.label = label
    return shape


def pcb10_upright_edits():
    """D-068 world-frame boxes: header-row reliefs cut from, and edge hooks added to, each upright."""
    m = PCB10_MOUNT
    face, front, top = m["board"][2], m["board"][3], m["board"][5]
    depth, below, above = m["relief"]
    gap, thick, lip_z = m["lip"]
    rail_y, over, roof = m["bridge"]
    cuts, adds = [], []
    for k, (x0, x1) in enumerate(m["uprights"], start=1):
        label = rf"BODY_FRAME_C3_CARRIER_UPRIGHT_{k}"
        cuts += [(label, (x0, x1, face - depth, face, z - below, z + above)) for z in m["rows"]]
        adds += [(label, (x0, x1, front + gap, front + gap + thick, lip_z, top + over)),   # lip on F
                 (label, (x0, x1, rail_y, front + gap + thick, top + over, roof))]          # bridge over the edge
    return cuts, adds


def pcb10_devkitc():
    """Espressif ESP32-S3-DevKitC-1 v1.1 (N8) as soldered on PCB-10, from Espressif's drawing."""
    m = PCB10_MOUNT
    p1, pitch, n = m["pin1_x"], m["pitch"], m["pins"]
    p22 = p1 - pitch * (n - 1)
    y0 = m["board"][3] + m["header"]          # DevKitC underside
    y1 = y0 + m["pcb"]                        # its component face
    zc = sum(m["rows"]) / 2.0
    parts = [
        _blk(p22 - 8.0, p1 + 1.4, y0, y1, zc - 12.7, zc + 12.7, "C3_DEVKITC_V11_PCB"),            # 62.74 x 25.40
        _blk(p1 + 1.4 + 6.4 - 25.5, p1 + 1.4 + 6.4, y1, y1 + 3.1, zc - 9.0, zc + 9.0,
             "C3_DEVKITC_V11_ESP32_S3_WROOM_1_N8"),                                              # 25.5 x 18 x 3.1
    ]
    for name, dz in (("UART", 5.7), ("USB", 19.4)):                                              # from the J1 edge
        z = zc - 12.7 + dz
        parts.append(_blk(p22 - 8.0, p22 - 8.0 + 7.35, y1, y1 + 3.26, z - 4.47, z + 4.47, f"C3_DEVKITC_V11_USB_C_{name}"))
    for row, z in zip(("J1", "J3"), m["rows"]):
        parts.append(_blk(p22 - pitch / 2.0, p1 + pitch / 2.0, m["board"][3], y0, z - 1.27, z + 1.27,
                          f"C3_DEVKITC_V11_HEADER_{row}"))
        tails = [_blk(p1 - k * pitch - m["pin"] / 2.0, p1 - k * pitch + m["pin"] / 2.0,
                      m["board"][2] - m["tail"], y1 + 1.0, z - m["pin"] / 2.0, z + m["pin"] / 2.0) for k in range(n)]
        parts.append(Compound(label=f"C3_DEVKITC_V11_PINS_{row}", children=tails))
    return Compound(label="C3_ESP32_S3_DEVKITC_1_V11_ESPRESSIF", children=parts)


# D-068 amended (lesson 3, board set-up): the real connector footprints don't fit the CAD's two
# rows 6 mm apart (GH courtyards are 6.6 mm deep; the real Micro-Fit is 9.65 x 9.9 mm, not the
# 7.26 mm placeholder): 23 courtyard overlaps on a scratch board. The board grows 6 mm down
# (Z 76..125.5, 70 x 49.5) and the connectors go in three rows, courtyard bands A Z 89.85-96.45,
# B 83.15-89.75 (with the screws), C 76.3-82.9; J10-1 spans B and C at the +X edge. The right
# DRV8833's terminal block (chassis, X 43.5-50.5, top Z 76.1) sits 0.11 mm in front of the board
# plane, so the bottom edge is notched over it (X 42.5-51 up to Z 79) and J10-1 rises 1.8 mm: the
# 2 mm-low install position clears it. Body centres (X, Z) of each GH header, from the PCB-10
# placement proved by KiCad DRC.
PCB10_GH = {"J10-7": (13.13, 93.15), "J10-3": (25.19, 93.15), "J10-4": (34.73, 93.15), "J10-10": (44.29, 93.15),
            "J10-2": (1.03, 86.45), "J10-5": (13.09, 86.45), "J10-6": (33.03, 86.45),
            "J10-12": (26.0, 79.6), "J10-8": (37.0, 79.6)}
PCB10_J10_1 = dict(header=(46.1, 56.0, -56.8, -49.82, 78.6, 88.255),   # Molex SD-43650-001: 9.65 x 9.90 x 6.98
                   plug=(56.0, 68.0, -56.8, -46.8, 78.6, 88.255))
PCB10_BOARD_GROWTH = [(-14.0, 42.5, -58.4, -56.8, 76.0, 82.01), (51.0, 56.0, -58.4, -56.8, 76.0, 82.01),
                      (42.5, 51.0, -58.4, -56.8, 79.0, 82.01)]          # notched over the terminal block

# Integration follow-up, 2026-11-01 (D-068): JP1's two tails were not in the
# DevKitC-row reliefs. Clear its entire bbox plus 0.3 mm, swept 2 mm down.
# Same 3 mm depth as the existing row relief; leaves 4.6 mm of upright behind
# it and at least 1.92 mm at the sides. No released PCB geometry changes.
PCB10_JP1_RELIEF = (-8.52, -5.92, -61.4, -58.4, 89.2, 95.8)



def pcb10_connector_moves():
    """DROID_MOVES for the C3 GH headers and their mated plugs, from C3_GH_ROWS to PCB10_GH."""
    from body_v1_model import C3_GH_ROWS
    moves = []
    for z_old, row in C3_GH_ROWS.items():
        for cid, n, x0 in row:
            x_old = x0 + (1.25 * (n - 1) + 4.5) / 2.0      # header body width (BM0nB-GHS-TBT)
            x_new, z_new = PCB10_GH[cid]
            tag = cid.replace("-", "_")
            moves.append((rf"C3_{tag}_(JST_GH_BM{n:02d}B_HEADER|GHR{n:02d}_MATED_PLUG)",
                          (round(x_new - x_old, 3), 0.0, round(z_new - z_old, 3))))
    return moves


def pcb10_j10_1():
    m = PCB10_J10_1
    return [_blk(*m["header"], "C3_J10_1_MICROFIT3_2P_RA_HEADER"), _blk(*m["plug"], "C3_J10_1_MICROFIT3_2P_MATED_PLUG")]


_PCB10_CUTS, _PCB10_ADDS = pcb10_upright_edits()


# D-070: wheel print fixes. Wheel frame as in wheel_model.py (axis Y, +y outboard); on the
# droid X = x, Z = 42 + z and Y = +-(85 + y), the right wheel being the left mirrored in XZ.
# (1) The hub cap's two clocking pegs move onto the hub, so the cap's underside is flat at
# y 12 and it prints underside down with no supports. Each Ø2.1 x 1.8 hub hole is filled
# and carries a Ø1.8 x 1.5 peg. The cap gets the Ø2.1 x 1.8 holes, each in a Ø3.7 boss
# because a bare hole would break 0.05 mm into the R11.2 screw-head recess, and its centre
# column is trimmed flush (it stood 0.4 mm into the hub bore). (2) The TPU tyre is printed
# in its free state, Ø73.6 bore and 19.3 mm wide, so it stretches 0.54 % onto the Ø74 seat
# and the ring squeezes it 0.3 mm; the assembly keeps the fitted state (PRINT_STATES).
# check_wheel_print.py measures both.
WHEEL_PEGS = dict(
    r=12.2, angles=(30.0, 210.0),       # wheel_model CAP_PEG: toward two hex corners
    face=12.0,                          # hub face = cap underside (wheel_model Y_OUT)
    peg=0.9, peg_len=1.5,               # Ø1.8 x 1.5 peg, now on the hub
    hole=1.05, depth=1.8, fill=1.1,     # Ø2.1 x 1.8 hole, now in the cap; hub hole fill
    boss=1.85, recess_top=13.9,         # boss round each cap hole, up to the recess roof
    column=(4.6, 11.5),                 # cut radius and bottom: trims the cap column to y 12
)
WHEEL_TYRE_PRINT = dict(seat_radius=36.8, y=(-10.15, 9.15))  # assembled: R37, y -10..9
_WHEEL_HALF_TRACK, _WHEEL_AXLE_Z = 85.0, 42.0


def _wheel_cyl(side, r, y0, y1, x=0.0, z=0.0):
    """World cylinder on the wheel axis (side +1 left, -1 right) over wheel-frame y0..y1, at (x, z)."""
    a, b = sorted(side * (_WHEEL_HALF_TRACK + y) for y in (y0, y1))
    return Cylinder(r, b - a, rotation=(90, 0, 0)).moved(Location((x, (a + b) / 2.0, _WHEEL_AXLE_Z + z)))


def wheel_peg_edits():
    """D-070 world-frame (label, shape) lists for both wheels: rim adds, cap cuts, cap adds."""
    m = WHEEL_PEGS
    rim_adds, cap_cuts, cap_adds = [], [], []
    for side, tag in ((1, "L"), (-1, "R")):
        rim, cap = rf"WHEEL_{tag}_RIM_PETG", rf"WHEEL_{tag}_HUB_CAP_PETG"
        cap_cuts.append((cap, _wheel_cyl(side, m["column"][0], m["column"][1], m["face"])))
        for angle in m["angles"]:
            x, z = m["r"] * math.sin(math.radians(angle)), m["r"] * math.cos(math.radians(angle))
            rim_adds.append((rim, _wheel_cyl(side, m["fill"], m["face"] - m["depth"] - 0.1, m["face"], x, z)
                             + _wheel_cyl(side, m["peg"], m["face"], m["face"] + m["peg_len"], x, z)))
            # Cuts run before adds, so the hole is cut first (taking the old peg with it)
            # and the boss is added with its own hole.
            hole_top = m["face"] + m["depth"]
            cap_cuts.append((cap, _wheel_cyl(side, m["hole"], m["face"] - m["peg_len"] - 0.1, hole_top, x, z)))
            cap_adds.append((cap, _wheel_cyl(side, m["boss"], m["face"], m["recess_top"], x, z)
                             - _wheel_cyl(side, m["hole"], m["face"] - 0.1, hole_top, x, z)))
    return rim_adds, cap_cuts, cap_adds


_WHEEL_RIM_ADDS, _WHEEL_CAP_CUTS, _WHEEL_CAP_ADDS = wheel_peg_edits()


def _wheel_model():
    """A private copy of the chassis wheel source, so print-state parameters can be set on it."""
    path = BUILD / "01-chassis" / "v1" / "cad" / "wheel" / "wheel_model.py"
    spec = importlib.util.spec_from_file_location("makad_v1_wheel_print_state", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wheel_tyre_print():
    """D-070: the tyre as printed (free state), in the wheel frame. One part serves both
    sides: the right tyre is the left one turned over, so this is the left tyre."""
    W = _wheel_model()
    W.SEAT_RADIUS, W.TYRE_Y = WHEEL_TYRE_PRINT["seat_radius"], WHEEL_TYRE_PRINT["y"]
    return W.tyre("L")


# Parts printed in another state than the assembly shows: label pattern -> function
# returning the print-state part in its own frame. The STL export uses it for those labels.
PRINT_STATES = [
    (r"WHEEL_[LR]_TYRE_TPU95A_[LR]", wheel_tyre_print),  # D-070
]


# D-071: axle-stack assembly fixes, both sides. The axle is the line X 0, Z 42; |Y| runs
# outboard, and the right side is the left mirrored in XZ.
# (A) The stub flange shrinks from Ø24 to Ø21. At Ø24 it covered half the socket of each
#     housing screw (R12), 1.6 mm in front of the heads, so the housing could not be bolted
#     on with the stub inside it. Ø21 leaves a 2 mm key 0.35 mm clear and 1.0 mm of steel
#     outside the wheel-screw threads.
# (B) The motor face screws cannot be reached once the bearings and stub are in: both
#     bearings (R8) and the flange sit across the key path at R8.5. So the motor is
#     aligned with a printed tool, the alignment plug (CH-089), in the housing's bearing
#     seat. Housing, plug and cap go on, the plug's bore takes the motor shaft, and the face
#     screws are tightened through the key slots and the plug's notches. The housing then
#     comes off for the bearings and stub; its four screw holes close from Ø3.4 to Ø3.2, so
#     it goes back where the motor was aligned to it.
# (C) A notch in the carrier hub over the set screw: the 1.5 mm key grazed it by 0.07 mm.
# check_axle_stack.py measures all of it.
AXLE_FIX = dict(
    flange=(10.5, 91.0, 93.0),                  # radius (was 12.0), |Y| span
    housing_hole=(1.6, 74.0, 86.35),            # radius (was 1.7), |Y| span of the housing
    screw_r=12.0, screw_angles=(45.0, 135.0, 225.0, 315.0),  # housing screws, deg in XZ from +X
    key_x=8.5,                                  # face screws at X +-8.5 on the axle line
    # D-072: the body was R7.9 (0.10 radial in the seat), which let the plug set the motor up
    # to 0.125 mm off the bearing axis. It is now a close sliding fit, printed after the seat
    # is tuned to the real bearings; see ALIGN_BUDGET.
    plug_body=(7.98, 76.6, 86.4),               # radius, |Y|: in the Ø16 seat, under the cap
    plug_nose=(6.1, 74.1, 76.6),                # in the housing's Ø12.5 inboard cavity
    plug_bore=2.025,                            # Ø4.05, as the stub: 6.9 mm on the shaft
    plug_notch=(7.2, 1.4),                      # cut outside R7.2 within +-1.4 of each key axis
    set_notch=(1.5, 73.5, 45.0, 59.0),          # half width X, |Y| from (to the face), Z span
    # D-072: ISO 7380 M3 x 16 housing screws (were M3 x 18): length, head seat |Y| (cap top),
    # head radius and height. The tip moves from |Y| 69.71 to 71.71.
    cap_screw=(16.0, 87.71, 2.85, 1.65),
)


def _axle_cyl(side, r, a0, a1, x=0.0, z=0.0):
    """World cylinder along Y over |Y| a0..a1 on one side (+1 left, -1 right), at (x, Z 42 + z)."""
    lo, hi = sorted((side * a0, side * a1))
    return Cylinder(r, hi - lo, rotation=(90, 0, 0)).moved(Location((x, (lo + hi) / 2.0, _WHEEL_AXLE_Z + z)))


def axle_edits():
    """D-071 world-frame (label, shape) lists for both sides: cuts and adds."""
    m = AXLE_FIX
    cuts, adds = [], []
    for side, tag in ((1, "L"), (-1, "R")):
        r, a0, a1 = m["flange"]
        cuts.append((rf"WHEEL_{tag}_STUB_SHAFT_8MM", _axle_cyl(side, 13.0, a0 - 0.1, a1 + 0.1) - _axle_cyl(side, r, a0 - 0.2, a1 + 0.2)))
        hole, h0, h1 = m["housing_hole"]
        for angle in m["screw_angles"]:
            x, z = m["screw_r"] * math.cos(math.radians(angle)), m["screw_r"] * math.sin(math.radians(angle))
            adds.append((rf"AXLE_BEARING_HOUSING_{tag}", _axle_cyl(side, 1.75, h0, h1, x, z) - _axle_cyl(side, hole, h0 - 0.1, h1 + 0.1, x, z)))
        w, y0, z0, z1 = m["set_notch"]
        lo, hi = sorted((side * y0, side * 74.01))
        cuts.append((rf"AXLE_MOTOR_CARRIER_{tag}", (-w, w, lo, hi, z0, z1)))
    return cuts, adds


_AXLE_CUTS, _AXLE_ADDS = axle_edits()


# D-075: frame insert and screw pilots. The M3 x 6 inserts in hand (OnlyScrews, OD 4.4) sat in
# Ø4.3 pilots, 0.05 mm of bite a side; every other M3 insert in the robot uses Ø4.0. The M2.5 x 4
# (OD 3.9) sat in Ø3.9, no bite at all; it gets OD - 0.4 like the M3s. The IMU's thread-forming
# M2 x 5 had no pilot in the deck. Rings fill the old pilots down to the new diameter.
FRAME_FIX = dict(
    insert_r=2.0,                               # M3 x 6 pilot Ø4.0 (was Ø4.3)
    j04_y=dict(FRONT=54.0, REAR=58.5), j04_z=(38.0, 48.0),
    j04_x=(17.0, 23.1, 24.0),                   # |X|: rail face, old pilot end, new pilot end (7 mm)
    boss_xy=((28.0, -39.5), (28.0, 39.5), (71.5, -34.35), (71.5, 34.35)), boss_z=(32.0, 38.5),
    post_r=1.75, post_xy=((41.05, 34.04), (41.05, 54.36), (41.05, -34.04), (41.05, -54.36)),
    post_z=(61.9, 66.0),                        # M2.5 x 4 pilot Ø3.5 (was Ø3.9), 4.1 deep
    imu_r=0.8, imu_xy=((22.0, 7.5), (22.0, -7.5)), imu_z=(51.9, 56.1),  # M2 thread-forming, Ø1.6 through the deck
)


def _x_cyl(r, x0, x1, y, z):
    return Cylinder(r, x1 - x0, rotation=(0, 90, 0)).moved(Location(((x0 + x1) / 2.0, y, z)))


def frame_pilot_edits():
    """D-075 world-frame (label, shape) cuts and adds on the two frame modules."""
    m, r = FRAME_FIX, FRAME_FIX["insert_r"]
    cuts, adds = [], []
    for region, sx in (("FRONT", 1.0), ("REAR", -1.0)):
        label = rf"CHASSIS_FRAME_{region}_MODULE"
        face, old, new = m["j04_x"]
        for sy in (1.0, -1.0):
            for z in m["j04_z"]:
                y = sy * m["j04_y"][region]
                lo, hi = sorted((sx * face, sx * old))
                adds.append((label, _x_cyl(2.2, lo, hi, y, z) - _x_cyl(r, lo - 0.1, hi + 0.1, y, z)))
                lo, hi = sorted((sx * (old - 0.05), sx * new))
                cuts.append((label, _x_cyl(r, lo, hi, y, z)))
    front = r"CHASSIS_FRAME_FRONT_MODULE"
    z0, z1 = m["boss_z"]
    for x, y in m["boss_xy"]:
        adds.append((front, _z_cyl(2.2, z0, z1, x, y) - _z_cyl(r, z0 - 0.1, z1 + 0.1, x, y)))
    z0, z1 = m["post_z"]
    for x, y in m["post_xy"]:
        adds.append((front, _z_cyl(1.98, z0, z1, x, y) - _z_cyl(m["post_r"], z0 - 0.1, z1 + 0.1, x, y)))
    z0, z1 = m["imu_z"]
    for x, y in m["imu_xy"]:
        cuts.append((front, _z_cyl(m["imu_r"], z0, z1, x, y)))
    return cuts, adds


_FRAME_CUTS, _FRAME_ADDS = frame_pilot_edits()


# D-076: frame print orientation. The front module prints as it sits (tub bottom down), but its
# rails, J13 ribs and crossmember stopped at Z 35, 3 mm above the tub's Z 32: 2588 mm2 of floating
# underside on 477 mm2 of bed. They now run down to Z 32. The J13 nut sockets and the J10-8 bore
# stay open; the crossmember fill stops 1.5 mm short of its front face (shell 2.2 mm away). The rear
# module prints deck down; the crossmember strip behind the deck (X -48 to -41) stopped at Z 48,
# a 7 mm ledge 8 mm off the bed, and now rises to the deck top (Z 56; body frame and PCB-02 2.0 mm
# away, shell 2.6 mm).
FRAME_PRINT = dict(
    front_floor=32.0, front_old=35.0,
    front_fill=((17.0, 80.0, 50.0, 58.0), (57.5, 70.5, 58.0, 64.0), (80.0, 90.5, -62.0, 62.0)),  # x0, x1, |y|/y spans
    j13_sockets=((64.0, 48.0), (64.0, -48.0)), j13_socket_r=5.2,
    nose_bore=(86.0, -31.0, 2.5),
    rear_fill=(-48.0, -41.0, -66.0, 66.0, 48.0, 56.0),
)


def frame_print_edits():
    """D-076 world-frame (label, shape) adds: the front module's flat bottom, the rear deck plane."""
    from build123d import Box
    p = FRAME_PRINT
    z0, z1 = p["front_floor"], p["front_old"] + 0.01

    def box(x0, x1, y0, y1, za, zb):
        return Box(x1 - x0, y1 - y0, zb - za).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (za + zb) / 2.0)))

    fill = None
    for x0, x1, y0, y1 in p["front_fill"]:
        spans = ((y0, y1),) if y0 < 0 else ((y0, y1), (-y1, -y0))
        for a, b in spans:
            fill = box(x0, x1, a, b, z0, z1) if fill is None else fill + box(x0, x1, a, b, z0, z1)
    for x, y in p["j13_sockets"]:
        fill = fill - _z_cyl(p["j13_socket_r"], z0 - 1.0, z1 + 1.0, x, y)
    x, y, r = p["nose_bore"]
    fill = fill - _z_cyl(r, z0 - 1.0, z1 + 1.0, x, y)
    return [(r"CHASSIS_FRAME_FRONT_MODULE", fill), (r"CHASSIS_FRAME_REAR_MODULE", box(*p["rear_fill"]))]


_FRAME_PRINT_ADDS = frame_print_edits()


# D-077: J13 bolts into M4 heat-set inserts in the deck. The Ø10.4 nut sockets under the three
# top-driven bolts let a socket hold the plain nut from below, but at the rear (X -22) the socket
# overlaps the J04 key pocket at the rail end: the key had 6 % of its inner wall, and with the
# carriers on, the key tongue stands in the socket so the nut can't be held. The sockets are filled
# back to the rail, rib and deck they were cut from, the rear key pockets re-cut, and an OnlyScrews
# M4 x 8 insert (OD 5.9) goes into a Ø5.5 x 9 pilot from the deck top, flush. The M4 x 12 bolt keeps
# 6 mm of thread and stops 3 mm above the pilot bottom. The front-left bolt (64, +48) is driven from
# below into the body cassette's nut and keeps its socket.
J13_FIX = dict(
    points=((-22.0, -48.0), (-22.0, 48.0), (64.0, -48.0)), socket_r=5.2,
    pilot_r=2.75, pilot_z=(47.0, 56.0), insert=(2.95, 2.0, 48.0, 56.0),  # OD/2, ID/2, Z span
    deck_slab=(51.9, 53.1),                     # the socket ran 1 mm into the deck underside
    # Material each socket was cut from: (x0, x1, |y0|, |y1|, z0, z1) per region.
    envelope=dict(FRONT=((17.0, 80.0, 50.0, 58.0, 32.0, 52.0), (57.5, 70.5, 52.0, 64.0, 32.0, 51.0)),
                  REAR=((-32.0, -17.0, 50.0, 58.0, 35.0, 52.0), (-28.5, -17.0, 52.0, 64.0, 35.0, 51.0),
                        (-32.0, -23.0, 50.0, 66.0, 35.0, 52.0))),
    rear_key=(-20.2, -17.0, 50.3, 52.7, 41.3, 44.7),  # J04 key pocket, |Y|
    # The old socket ran past the rail's inner face, so half the pilot below the deck stood in air.
    # A 45° cone boss under the deck closes it: R 3.95 (1.2 mm wall) at the pilot floor, Z 47,
    # widening to R 8.95 at the deck underside, apex at Z 43.05 so it prints without support.
    boss=(47.0, 3.95, 52.0),
    boss_x=dict(FRONT=(17.0, 80.0), REAR=(-41.0, -17.0)),
    # The rear-right boss reaches the rear locating pin's Ø4.1 hole (-27, -42); it stays through.
    pin_holes=((-27.0, -42.0, 2.05), (59.0, 42.0, 2.05)),
)
# D-078: the front-left J13 bolt (64, +48) goes in from below, and its Ø8 head overlapped the
# hatch edge (Y 46.5) by 2.5 mm, so the body could not come off with the hatch on. A Ø9.2 notch
# in the hatch edge, round the bolt axis, lets the head pass with 0.6 mm all round.
HATCH_NOTCH = (64.0, 48.0, 4.6, 29.0, 33.5)  # x, y, r, z0, z1


def j13_insert_edits():
    """D-077 (cuts, adds, inserts) for the three top-driven J13 points."""
    from build123d import Align, Box, Cone
    m = J13_FIX

    def box(x0, x1, y0, y1, z0, z1):
        return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))

    cuts, adds, inserts = [], [], []
    for k, (x, y) in enumerate(m["points"], start=1):
        region = "FRONT" if x > 0 else "REAR"
        label = rf"CHASSIS_FRAME_{region}_MODULE"
        sy = 1.0 if y > 0 else -1.0
        env = None
        for x0, x1, a, b, z0, z1 in m["envelope"][region]:
            piece = box(x0, x1, *sorted((sy * a, sy * b)), z0, z1)
            env = piece if env is None else env + piece
        sx0, sx1 = (17.0, 92.0) if region == "FRONT" else (-41.0, -17.0)
        env = env + box(sx0, sx1, -56.0, 56.0, *m["deck_slab"])
        fill = _z_cyl(m["socket_r"] + 0.05, 31.0, m["deck_slab"][1], x, y) & env
        zf, rf, zt = m["boss"]
        r_top, apex = rf + (zt - zf), zf - rf
        cone = Cone(0.0, r_top, zt + 0.05 - apex, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, apex)))
        fill = fill + (cone & box(*m["boss_x"][region], y - 10.0, y + 10.0, apex - 1.0, zt + 0.05))
        fill = fill - _z_cyl(m["pilot_r"], m["pilot_z"][0], m["pilot_z"][1] + 1.0, x, y)
        for px, py, pr in m["pin_holes"]:
            fill = fill - _z_cyl(pr, 30.0, 57.0, px, py)
        if region == "REAR":
            kx0, kx1, ka, kb, kz0, kz1 = m["rear_key"]
            fill = fill - box(kx0, kx1, *sorted((sy * ka, sy * kb)), kz0, kz1)
        adds.append((label, fill))
        cuts.append((label, _z_cyl(m["pilot_r"], m["pilot_z"][0], m["pilot_z"][1] + 0.1, x, y)))
        r_out, r_in, z0, z1 = m["insert"]
        ring = _z_cyl(r_out, z0, z1, x, y) - _z_cyl(r_in, z0 - 0.1, z1 + 0.1, x, y)
        inserts.append((r"CHASSIS_PRIMARY_FRAME", _body._paint(ring, f"J13_DECK_INSERT_M4X8_{k}", _body.BRONZE, 1.0)))
    return cuts, adds, inserts


_J13_CUTS, _J13_ADDS, _J13_INSERTS = j13_insert_edits()


def _shifted(part, location):
    """part.moved(location) without build123d's deepcopy: on a leaf still in the tree it
    copies the whole assembly through the parent link, about 5 s per move on the body
    alone and past 90 GB with the head (2026-10-29). The OCC move shares the geometry."""
    from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
    from OCP.TopoDS import TopoDS
    from build123d import Solid
    shape = part.wrapped.Moved(location.wrapped)
    if shape.ShapeType() == TopAbs_SOLID:
        return Solid(TopoDS.Solid_s(shape))
    if shape.ShapeType() == TopAbs_COMPOUND:
        return Compound(TopoDS.Compound_s(shape))
    return part.moved(location)


def _chassis_model():
    """A private copy of the chassis source, for its nose and keel constants."""
    path = BUILD / "01-chassis" / "v1" / "cad" / "body_chassis_model.py"
    spec = importlib.util.spec_from_file_location("makad_v1_chassis_constants", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# D-079: nose and keel pilots and shims. (1) The nine CNC Kitchen M3 x 5.7 positions take the M3 x 6
# in hand (OnlyScrews, OD 4.4) in their Ø4.0 bores. The caster seat is 6.0 mm, so the insert fills it:
# its bores stay through, the flange bears on the insert ends at the seat face, and under the GP2Y
# (insert 1) a Ø5.0 x 0.5 relief in the pocket floor takes the plastic pushed out at the top. The
# crossmember pod pilots are already 7 mm. The keel pilots in the rear crossmember run 6.5 -> 7.0 mm
# (insert + 1). (2) The TCRT shims grow 1.0 -> 1.2 mm (the lab's minimum wall) and the keel's sensor
# flat is recessed 0.4 mm under the bezel (belly Z 12 -> 12.4), so two shims still set the optical
# face at Z 10 and the guard lips at Z 7 (builder, 2026-11-01). The bezel's M2 pilot and pin hole run
# 1 mm past the screw tip and pin top at zero shims. (3) The wear shoe's M2 pilot had 0.45 mm of
# tongue above it: the tongue grows 1 mm straight up (Z 8.5 -> 9.5), the keel groove with it.
# (4) Contoured TCRT end cradles close the real case-to-ledge gap without moving the sensor.
NOSE_KEEL_FIX = dict(
    insert=(2.2, 1.25, 6.0),                    # M3 x 6: OD/2, modelled ID/2, length
    seat_z=29.0, seat_relief=(2.5, 34.5, 35.1), # insert 1 relief: r, Z span (floor Z 35)
    pod_x=92.0, keel_z=34.0,
    keel_pilot=(2.0, 40.4, 41.0),               # r, old bottom, new bottom (7 mm from Z 34)
    shim_t=1.2, belly=12.4,
    flat_recess=(-61.6, -47.4, 11.9, 12.4),     # x0, x1, z0, z1 under the bezel and shims (full keel width)
    bezel_pilot=(0.8, 20.4, 21.9), pin_hole=(1.0, 18.4, 19.4),
    # End cradles contact the real rounded TCRT case at its existing datum (D-079).
    cradle_x=((-59.8, -58.5), (-49.5, -48.2)),
    cradle_half_y=3.8, cradle_top=14.0, shim_window_x=(-59.9, -48.1),
    tongue_top=9.5,                             # shoe tongue Z 8.5 -> 9.5, straight sides at the top width
)


def nose_keel_edits():
    """D-079 (cuts, adds, removes, inserts) for the nose and keel."""
    M, m = _chassis_model(), NOSE_KEEL_FIX
    r_out, r_in, length = m["insert"]
    cuts, adds, inserts = [], [], []

    def ring(shape_out, shape_in, label):
        return _body._paint(shape_out - shape_in, label, _body.BRONZE, 1.0)

    # (1) Inserts: M3 x 6 models in place of the M3 x 5.7 ones (same labels).
    z0 = m["seat_z"]
    for k, (x, y) in enumerate(M.ball_screw_points(), start=1):
        inserts.append((r"BALL_POD_HARDWARE", ring(_z_cyl(r_out, z0, z0 + length, x, y), _z_cyl(r_in, z0 - 0.1, z0 + length + 0.1, x, y),
                                                   f"BALL_SEAT_HEATSET_INSERT_{k}")))
    r, rz0, rz1 = m["seat_relief"]
    x, y = M.ball_screw_points()[0]
    cuts.append((r"BALL_POD_PRINTED_SEAT", _z_cyl(r, rz0, rz1, x, y)))
    x1 = m["pod_x"]
    for k, (y, z) in enumerate(M.BALL_POD_SCREWS_YZ, start=1):
        inserts.append((r"BALL_POD_HARDWARE", ring(_x_cyl(r_out, x1 - length, x1, y, z), _x_cyl(r_in, x1 - length - 0.1, x1 + 0.1, y, z),
                                                   f"BALL_POD_HEATSET_INSERT_{k}")))
    z0 = m["keel_z"]
    pr, old, new = m["keel_pilot"]
    for k, (x, y) in enumerate(M.rear_keel_screw_points(), start=1):
        inserts.append((r"REAR_CROSSMEMBER_KEEL_INSERTS", ring(_z_cyl(r_out, z0, z0 + length, x, y),
                                                               _z_cyl(r_in, z0 - 0.1, z0 + length + 0.1, x, y), f"REAR_KEEL_HEATSET_INSERT_{k}")))
        cuts.append((r"CHASSIS_FRAME_REAR_MODULE", _z_cyl(pr, old - 0.05, new, x, y)))

    # (2) Shims 1.2 mm on a sensor flat raised to Z 12.4: two shims keep the face at Z 10.
    keel = r"REAR_KEEL_FACETED_BODY"
    fx0, fx1, fz0, fz1 = m["flat_recess"]
    cuts.append((keel, _blk(fx0, fx1, -12.0, 12.0, fz0, fz1)))
    (sx, sy), (px, py) = M.REAR_TCRT_FIX_POINTS
    for (r, a, b), (x, y) in ((m["bezel_pilot"], (sx, sy)), (m["pin_hole"], (px, py))):
        cuts.append((keel, _z_cyl(r, a - 0.05, b, x, y)))
    bx0, bx1 = M.REAR_TCRT_BEZEL_X
    hy, t = M.REAR_TCRT_BEZEL_HALF_Y, m["shim_t"]
    _, _, wy0, wy1 = M.REAR_TCRT_POCKET
    wx0, wx1 = m["shim_window_x"]
    face = m["belly"] - M.REAR_TCRT_SHIMS_NOMINAL * t
    for k in range(M.REAR_TCRT_SHIMS_NOMINAL):
        za = face + k * t
        shim = _blk(bx0, bx1, -hy, hy, za, za + t) - _blk(wx0, wx1, wy0, wy1, za - 1.0, za + t + 1.0)
        for x, y in M.REAR_TCRT_FIX_POINTS:
            shim = shim - _z_cyl(1.1, za - 1.0, za + t + 1.0, x, y)
        inserts.append((r"REAR_KEEL_FLOOR_INTERFACE", _body._paint(shim, f"REAR_TCRT_HEIGHT_SHIM_{k + 1}", _body.STEEL, 0.78)))

    # The old ledges sit ~4 mm below the rounded case: the bounding-box datum is
    # the projecting optical baffle, not a flat package bottom. Contoured end
    # cradles hold the actual vendor case without moving the sensor or obscuring
    # the 9 mm optical window. Widen the shim window and clear the keel for the
    # zero-shim (highest) stack as well as the nominal two-shim stack.
    sensor = _shifted(M._tcrt_ski_cartridge("REAR", M.TCRT_REAR_CENTER).children[0], Location())
    for xa, xb in m["cradle_x"]:
        pad = _blk(xa, xb, -m["cradle_half_y"], m["cradle_half_y"], face - 0.1, m["cradle_top"])
        adds.append((r"REAR_TCRT_BEZEL_WITH_GUARDS", pad - sensor))
        cuts.append((keel, _blk(xa - 0.1, xb + 0.1, -3.9, 3.9,
                               m["belly"] - 0.1, m["cradle_top"] + 2 * t + 0.1)))

    # (3) Shoe tongue 1 mm taller, straight-sided at its top half-width; the keel groove follows.
    w0, w1, h = M.REAR_KEEL_SHOE_TONGUE
    gc = M.REAR_KEEL_SHOE_GROOVE_CLEARANCE
    sx_, _, sz_ = M.SKID_SHOE_SIZE
    shoe_x0 = M.SKID_PAD_CENTER[0] - sx_ / 2.0
    shoe_x1 = M.SKID_PAD_CENTER[0] + sx_ / 2.0
    top = M.SKID_SHOE_BOTTOM_Z + sz_ + h
    adds.append((r"REAR_KEEL_REPLACEABLE_WEAR_SHOE", _blk(shoe_x0 + 1.0, shoe_x1, -w1, w1, top - 0.01, m["tongue_top"])))
    cuts.append((keel, _blk(shoe_x0 + 1.0 - gc, shoe_x1 + 8.0, -(w1 + gc), w1 + gc, top + gc - 0.05, m["tongue_top"] + gc)))
    # The subsystem ear-trim boolean leaves invalid topology on the GP2Y STEP.
    # Heal this inspection solid at the same placement, with unchanged bounds.
    gp2y = _shifted(M._gp2y_package(), Location()).fix()
    inserts.append((r"CHASSIS_V1_REFERENCE", _body._paint(gp2y, "GP2Y0A21YK0F_STEP", "#252525", 1.0)))
    # build_chassis_v1 filters out this existing D-027 inspection reserve.
    # Restore it so the final-tree service checks include the soldered lead.
    lead = next(p for p in M.sensors().children if p.label == "GP2Y_J10_8_SOLDERED_LEAD_RESERVE")
    inserts.append((r"CHASSIS_V1_REFERENCE", _body._paint(_shifted(lead, Location()), lead.label, "#79C4CB", 0.30)))
    removes = [r"BALL_SEAT_HEATSET_INSERT_[123]", r"BALL_POD_HEATSET_INSERT_[12]", r"REAR_KEEL_HEATSET_INSERT_[1-4]",
               r"REAR_TCRT_HEIGHT_SHIM_[12]", r"GP2Y0A21YK0F_STEP"]
    return cuts, adds, removes, inserts


_NOSE_KEEL_CUTS, _NOSE_KEEL_ADDS, _NOSE_KEEL_REMOVES, _NOSE_KEEL_INSERTS = nose_keel_edits()


# D-072: the M3 x 18 housing screws ended 0.2 mm short of the bottom of their blind holes,
# 0.51 mm above the gearbox face. ISO 7380's length tolerance on 18 mm is +-0.35 (js15), so a
# long screw could bottom out before its head clamped the cap, and push the skin onto the
# gearbox. M3 x 16 ends 2.2 mm short of the hole bottom and keeps 2.29 mm in the 4 mm insert.
def axle_cap_screws():
    """D-072 (group pattern, labelled world-frame screw) inserts: four M3 x 16 per side."""
    length, seat, head_r, head_h = AXLE_FIX["cap_screw"]
    out = []
    for side, tag in ((1, "L"), (-1, "R")):
        for index, angle in enumerate(AXLE_FIX["screw_angles"], start=1):
            x = AXLE_FIX["screw_r"] * math.cos(math.radians(angle))
            z = AXLE_FIX["screw_r"] * math.sin(math.radians(angle))
            screw = _axle_cyl(side, head_r, seat, seat + head_h, x, z) + _axle_cyl(side, 1.5, seat - length, seat, x, z)
            out.append((rf"AXLE_HOUSING_HARDWARE_{tag}",
                        _body._paint(screw, f"AXLE_CAP_SCREW_M3X16_{tag}_{index}", _body.STEEL, 1.0)))
    return out


_AXLE_SCREW_INSERTS = axle_cap_screws()


def axle_alignment_plug(side=1):
    """D-071 tool CH-089, placed in the left (or right) housing as it is used, world frame."""
    m = AXLE_FIX
    plug = _axle_cyl(side, *m["plug_body"]) + _axle_cyl(side, *m["plug_nose"])
    plug = plug - _axle_cyl(side, m["plug_bore"], m["plug_nose"][1] - 1.0, m["plug_body"][2] + 1.0)
    r, half = m["plug_notch"]
    lo, hi = sorted((side * (m["plug_nose"][1] - 1.0), side * (m["plug_body"][2] + 1.0)))
    for sx in (1, -1):
        x0, x1 = sorted((sx * r, sx * 9.0))
        plug = plug - _cut_box(x0, x1, lo, hi, _WHEEL_AXLE_Z - half, _WHEEL_AXLE_Z + half)
    plug.label = "AXLE_ALIGNMENT_PLUG"
    return plug


# D-072: how far off the bearing axis the alignment leaves the motor shaft, mm radial. The
# plug sets the shaft within (seat - body) + (bore - shaft) of the housing's axis wherever the
# housing sat. At the refit the housing screws are left loose and the stub is turned so the
# housing moves onto the shaft within its hole float; that takes up the refit error, but in
# the worst case (the housing sat at the edge of its float at the alignment step) not the
# plug's own error. So the plug's error is what the gearbox shaft is forced through. The
# budget is the stub bore's own clearance on the shaft (Ø4.05 H8 on Ø4: 0.025 to 0.034
# radial), which the set screw already pushes the shaft across when it is tightened.
ALIGN_BUDGET = dict(
    seat_r=8.0,                # housing bearing seat, tuned to the bearings' Ø16 OD
    shaft_r=2.0,               # motor shaft, Ø4
    housing_float=(1.6, 1.49),  # Ø3.2 hole, M3 6g major max Ø2.98: the least float
    limit=0.05,                # mm radial
)


# D-092: PCB-09 sits on two M2.5 x 11 mm round male-female standoffs at the Pi's header-side
# holes (Pi holes 3 and 4), as a HAT does: the Pi header's 2.5 mm plastic plus Samtec
# SSW-120-01-T-D's 8.51 mm insulator is 11.01 mm. The standoffs take the place of the Pi's
# M2.5 x 6 screws there (a 6 mm male thread into the same tray inserts); M2.5 x 5 socket-head
# screws hold the board. The board rises 0.05 mm onto them (Z 106.45-108.05), and two outline
# tabs reach the holes. The +X tab's -Y edge stays 0.37 mm off the Active Cooler, and a hex
# standoff would hit the cooler there, so they are round. check_pcb09_mount.py measures it.
PCB09_MOUNT = dict(
    holes=((3, _body.PI_MOUNT_HOLES[2]), (4, _body.PI_MOUNT_HOLES[3])),
    standoff=(2.25, 11.0, 6.0, 5.0),   # body radius, height, male thread length, female bore depth
    screw=(2.25, 2.5, 5.0),            # DIN 912 M2.5 head radius, head height, length
    lift=0.05,                         # placeholder board Z 106.4 -> 106.45
    tabs=((-11.0, -4.7, 16.3, 22.4), (47.1, 53.4, 17.2, 22.5)),  # world XY, on the board's Z
    # D-092 amendment: the connector bay grows 6 mm toward -X (X 30-36), from the strip's
    # +Y edge to the bay's, so the strip's nets have a 17 mm path into it.
    bay_extension=(30.0, 36.0, 22.4, 39.0),
)


def pcb09_mount_parts():
    """D-092 world-frame standoffs and screws, labelled, for DROID_INSERTS."""
    m = PCB09_MOUNT
    r, height, thread, bore = m["standoff"]
    head_r, head_h, length = m["screw"]
    top = _body.PI_PCB_TOP_Z
    under = top + height
    over = under + _body.PCB_THICKNESS
    parts = []
    for k, (x, y) in m["holes"]:
        stand = (_z_cyl(r, top, under, x, y) + _z_cyl(1.25, top - thread, top, x, y)
                 - _z_cyl(1.25, under - bore, under + 0.1, x, y))
        screw = _z_cyl(1.25, over - length, over, x, y) + _z_cyl(head_r, over, over + head_h, x, y)
        parts += [_body._paint(stand, f"PCB09_M25X11_ROUND_STANDOFF_{k}", _body.BRONZE, 1.0),
                  _body._paint(screw, f"PCB09_M25X5_SOCKET_SCREW_{k}", _body.STEEL, 1.0)]
    return parts


PCB09_MOVED = r"C0_(LINK_ADAPTER_PCB09_BOARD|GPIO_2X20_SOCKET_BODY|THVD1451_\w+|J9_\d_\w+)"


# D-095 (D-093 plan level 4): the bought modules of D-093/D-094 replace PCB-02, 03, 04, 05, 06,
# 07 and PCB-13 in the droid. World frame, mm. Pololu STEPs (S13V30F5, S18V20x, #2813) are in
# purchased/; the INA226, MAX98357A, INMP441 and LSM6DSOX outlines are drawn from vendor drawings
# or listings with a clearance margin and are UNMEASURED until the parts arrive (labels carry
# "UNMEASURED"). Boards without mounting holes sit in printed cradles: a rim 0.25 mm clear of the
# board, open on the wire edge, with 1.5 mm pads under the corners for the solder tails, the board
# held on the pads with VHB foam (E). Check scripts: check_bay_rear/tub/tray.py,
# check_rear_panel_ports.py, check_balance_channel.py, check_mic_bosses.py, check_amp_mount.py,
# check_imu_adapter.py and check_d095_mass.py.
PURCHASED = Path(__file__).resolve().with_name("purchased")
VENDOR_STEPS = {
    "S13V30F5": "5v-step-up-step-down-voltage-regulator-s13v30f5.step",     # Pololu 0J1808
    "S18V20X": "s18v20x-step-up-step-down-voltage-regulator.step",          # Pololu 0J1416
    "PSW_2813": "big-pushbutton-power-switch-with-reverse-voltage-protection.step",  # Pololu 0J1405
}
# Mounting holes in each STEP's own frame (board underside on z 0), from the STEP's Ø2.18 bores.
VENDOR_HOLES = {
    "S13V30F5": ((2.16, 2.16), (20.7, 2.16)),
    "S18V20X": ((2.16, 2.16), (2.16, 18.8), (41.02, 2.16), (41.02, 18.8)),
    "PSW_2813": (),                      # no mounting holes: the four Ø2.18 are its power terminals
}
PCB_T = 1.57                             # Pololu board thickness
M2_HEAD = (1.9, 1.3)                     # pan/button head radius, height (BO-013 family)
M3_BUTTON = (2.85, 1.65)                 # ISO 7380 M3 head radius, height (as D-072)

# Tub bay (was PCB-03, above the battery tub): one printed plate on the deck carries both
# S18V20ALVs (M2 head 5.5 V, M3 yaw 11.1 V), long axis along Y, terminals at the Y ends.
TUB_BAY = dict(
    plate=(30.0, 85.0, -28.0, 28.0, 56.0, 58.5),          # body over the tub opening
    arms=((18.5, 30.01, 21.0, 28.0),),                     # x0, x1, |y0|, |y1|: back to the rear deck strip
    modules=(("M2", 31.5), ("M3", 54.5)),                  # module X min; board Y -21.59..21.59
    boss=(2.5, 2.5),                                       # radius, height on the plate
    pilot=(0.8, 4.5),                                      # Ø1.6 M2 thread-forming pilot, depth from the boss top
    screw_len=5.0,                                         # M2 x 5 thread-forming, 3.4 mm engagement
    fix_rear=((21.0, 24.5), (21.0, -24.5)),                # M3 x 6 into M3 x 4 inserts through the 4 mm deck
    fix_front=((83.0, 20.0), (83.0, -20.0)),               # M3 x 8 into M3 x 6 inserts in the front crossmember
    insert_rear=(2.2, 1.25, 4.0), insert_front=(2.2, 1.25, 6.0),  # OD/2, modelled ID/2, length (in hand)
    pilot_r=2.0, plate_hole=1.7,
    ballast_relief=(3.4, 0.6),                             # Ø6.8 x 0.6 under the plate over the ballast CSK heads
)
TUB_BOARD_Z = TUB_BAY["plate"][5] + TUB_BAY["boss"][1]   # S18V20 underside, Z 61.0

# Tray bay (was PCB-04, under the compute tray): the two S13V30F5s (M4 Pi, M5 shared 5 V) hang
# from the tray, components down, on M2 x 5 F-F round standoffs; M2 x 5 from the tray top, M2 x 4
# from below. Both stay above Z 69.9, 7 mm over the motor cable reserves (D-072 keep-out).
TRAY_BAY = dict(
    tray_z=84.5, standoff=(1.85, 5.0),                     # tray underside; standoff radius, length
    modules=(("M4", (-19.0, 21.66), (1, 0, 0)),            # origin X, Y; local x direction (holes on Y 19.5)
             ("M5", (3.86, -35.16), (-1, 0, 0))),          # holes on Y -33.0
    hole_r=1.2, top_screw=5.0, bottom_screw=4.0,
)
TRAY_BOARD_TOP = TRAY_BAY["tray_z"] - TRAY_BAY["standoff"][1]   # Z 79.5

# Rear bay (was PCB-02, behind the rear panel): a printed plate in PCB-02's plane carries the power
# switch (M1) and the INA226 monitor (M6) in cradles on its +X face; two legs and arms bolt to the
# rear lower cross rail (X -36 face) with M3 x 16 into M3 x 6 inserts. The charge splice is tied
# beside its -Y edge.
REAR_BAY = dict(
    plate=(-49.6, -47.6, -27.0, 28.0, 70.0, 93.0),
    legs=((-26.0, -16.5), (16.5, 26.0)), leg_z=(60.3, 70.01),
    arms=((-25.5, -16.5), (16.5, 25.5)), arm_x=(-47.61, -36.0), arm_z=(60.3, 71.0),
    screw_yz=((-21.0, 65.5), (21.0, 65.5)), screw_len=16.0,
    cbore=(3.2, -45.6), clear_r=1.7,                       # counterbore radius, head seat X; shank clearance
    rail_face=-36.0, rail_pilot=(2.0, 6.7), insert=(2.2, 1.25, 6.0),
)
CRADLE = dict(rim=1.2, gap=0.25, pad=1.5, pad_size=3.0, lip=0.8)
REAR_SWITCH = dict(y0=-27.0, z_top=92.5)                  # board Y -27..-1.6, Z 72.18..92.5, terminals toward +Y
INA226_BOARD = (25.5, 20.5, 1.6, 3.0)                     # UNMEASURED: Y, Z, thickness, parts height (+X)
INA226_AT = (1.0, 72.0)                                    # board Y min, Z min
CHARGE_SPLICE = dict(axis=(-45.6, -34.0), r=3.5, z=(62.0, 88.0),
                     reserve=(-49.6, -41.6, -38.0, -30.0, 60.0, 90.0))

# Rear panel (D-093 Q7): the PCB-13 pad keeps its outline; the USB-C pocket, receptacle hole, pin
# relief and screw pilots are filled, and an XT30 charge port and a JST-XH 3P balance port go in.
# XT30U female (AMASS) 10.2 x 5.2, 16 long with solder cups (E), epoxied in a 0.2 mm-clear hole,
# mouth 0.5 mm inside the outer face. The balance port is the body-side lead's XHP-3 plug parked in
# a slot, face out; the charger's balance lead plugs onto it. Polarity marks are printed on the
# panel at the print stage.
PORTS = dict(
    xt30=dict(yz=(-8.0, 64.0), body=(10.2, 5.2, 16.0), clear=0.2),
    xh=dict(yz=(8.5, 64.0), body=(9.9, 5.75, 9.8), clear=0.2),
    face_x=-62.0, recess=0.5,                              # mouth plane: outer skin ~X -62.2..-63.2 here
    corridor=(30.0, 14.0, 10.0),                           # mating plug and lead outside: length, Y, Z
    skin_x=-63.4,                                          # the corridor starts outside the sloped skin
)

# Balance lead (D-093 R3). The pack-side 3 x AWG24 lead leaves the cells with W01, through the
# +Y tub window, and breaks at a JST PA 2.0 mm wire-to-wire pair (PAP-03V-S 8.0 x 5.8 D, PALR-03VF
# 7.4 x 6.3 E; 3 A, locking) lying in the channel where the NTC break was, 8.0 wide turned along
# Z (6.3 across Y). It slides back to the window like J-PK (pack out). The body-side lead loops
# back along the channel's outer wall, rises through a Ø5 hole in the deck, runs aft under the
# left driver and the cross rail, and ends in the XHP-3 balance port.
BALANCE = dict(
    pair=(54.0, 74.0, 41.0, 47.3, 41.0, 49.0),            # mated PA pair, X 20 (E)
    pack_lead=((44.0, 49.0, 34.1, 37.2, 40.6, 44.4), (44.0, 54.0, 37.2, 39.3, 40.6, 44.4)),
    body_lead=((50.5, 76.5, 47.5, 49.4, 42.0, 46.0),      # loop back along the channel wall
               (50.3, 53.7, 45.7, 49.1, 42.0, 60.0),      # rise through the deck hole
               (14.0, 54.0, 44.5, 48.5, 56.5, 60.0),      # aft under the left driver
               (14.0, 18.0, 33.0, 48.5, 56.5, 60.0),      # jog inboard of the body side rail
               (-47.0, 18.0, 33.0, 38.5, 56.5, 60.0),     # under the cross rail, inboard of the frame's lower side rail
               (-47.0, -40.0, 8.5, 38.5, 56.5, 60.0),     # across the rear deck
               (-51.7, -45.0, 4.0, 13.0, 56.5, 66.0)),    # up to the port's rear
    deck_hole=(52.0, 47.4, 2.5),                           # x, y, r through the front deck
)

# Microphones (D-093 Q6): four INMP441 modules at the four D-037 port axes. UNMEASURED module:
# 14 x 14 x 1.6 board, port on its centre, INMP441 4.72 x 3.76 x 1.0 inboard over the port. The
# board sits 1.6 mm deep in a 15 x 15 pocket in a larger boss (its inboard face flush with the old
# seat at |Y| 71.3, so nothing passes |Y| 68.5); a foam gasket ring in the pocket floor seals the
# port; two M2 x 4 thread-forming screws (as PCB-06) with Ø6 DIN 9021 washers beside the board clamp its edges.
MIC = dict(
    board=(14.0, 14.0, 1.6), pocket=(15.0, 15.0), seat=71.3,
    package=(4.72, 3.76, 1.0),
    boss_half=(11.6, 9.6),
    gasket=(3.25, 1.0, 0.7), gasket_pocket=3.5,           # OD/2, ID/2, compressed thickness; pocket radius
    screw_u=8.9, screw_len=4.0, pilot=(0.8, 4.0), washer=(3.0, 0.5),    # DIN 9021 M2 washer Ø6 x 0.5
    pigtail=(1.0, 2.0, 10.0),                              # thickness, half height, run past the board edge
)
MIC_FLOOR = MIC["seat"] + MIC["board"][2]                  # |Y| 72.9

# Amplifier (M8) and audio hub (M13): a printed bracket fused to the frame's front +Y post, the amp
# (UNMEASURED, Adafruit #3006 class 17.8 x 19.4) in a cradle on its +X face facing the speaker, the
# perfboard hub on its -X face on two M2 x 4 thread-forming screws (holes drilled by the builder).
AMP = dict(
    bracket=(66.3, 68.3, 39.5, 59.6, 100.0, 123.0),
    board=(17.8, 19.4, 1.6), at=(40.6, 102.0),             # Y, Z, thickness; board Y min, Z min
    parts=3.0, terminal=(7.0, 7.6, 8.5),                   # chip/passives height; screw terminal Y, Z, height (E)
)
HUB = dict(board=(18.5, 22.0, 1.6), at=(40.0, 100.5), boss=(2.5, 1.5), parts=5.0, screw=4.0,
           holes=((2.5, 11.0), (16.0, 11.0)))              # local (y, z) of the two drilled holes

# IMU (M7): Adafruit #4438 LSM6DSOX (Adafruit EAGLE board: 25.4 x 17.78, two Ø2.5 holes 20.32
# apart on one long edge, SH4 STEMMA connectors on the short edges) on a printed adapter screwed to
# the deck at the existing J15A M2 pilots (22, +-7.5). Long axis along Y; the chip lands 0.1 mm
# from PCB-07's, and the board stays behind the tub-bay plate (X 30) so either can go on first.
IMU = dict(
    adapter=(12.0, 29.5, -13.0, 13.0, 56.0, 58.0),
    board=(25.4, 17.78, 1.6), board_x1=29.78, boss=(2.5, 2.0),
    holes_v=15.24, holes_u=(2.54, 22.86), chip=(12.7, 8.89, 2.5, 3.0, 0.86),
    sh4=(6.0, 4.25, 2.95),                                 # JST SH 4P side entry: width, depth, height (E)
    j15a=((22.0, 7.5), (22.0, -7.5)), j15a_screw=6.0,
)
IMU_BOARD_Z = IMU["adapter"][5] + IMU["boss"][1]           # Z 60.0

# PCB-08 (D-093): the W23a/W23b sideband headers J8-3 and J8-5 go; the yaw servo plug moves here
# from PCB-03 J3-5: a Feetech 5264-3P (2.5 mm) top-entry header where J8-3 was, mated plug above.
PCB08_SERVO = dict(header=(-9.5, 0.4, -42.6, -36.85, 113.6, 119.6),
                   plug=(-9.0, -0.1, -42.2, -37.25, 116.6, 126.0))


def _place(shape, location):
    """A free shape at a world location, sharing its OCC geometry."""
    return _shifted(shape, location)


def _tag(shape, label, color, alpha=1.0):
    return _body._paint(shape, label, color, alpha)


_VENDOR_CACHE = {}


def vendor_solid(key):
    """One Pololu STEP as one solid or compound in its own frame (board underside on z 0)."""
    if key not in _VENDOR_CACHE:
        from cadgen.step_scene import import_step
        solids = list(import_step(str(PURCHASED / VENDOR_STEPS[key])).solids())
        _VENDOR_CACHE[key] = solids[0] if len(solids) == 1 else Compound(solids)
    return _VENDOR_CACHE[key]


def _frame(origin, x_dir, z_dir):
    return Location(Plane(origin=origin, x_dir=x_dir, z_dir=z_dir))


def tub_module_frames():
    """(name, Location) of the two S18V20ALVs: local x along +Y, local y along -X, board on Z 61."""
    y0 = -43.18 / 2.0
    return [(name, _frame((x0 + 20.96, y0, TUB_BOARD_Z), (0, 1, 0), (0, 0, 1))) for name, x0 in TUB_BAY["modules"]]


def tray_module_frames():
    """(name, Location) of the two S13V30F5s hanging under the tray, components down."""
    return [(name, _frame((x, y, TRAY_BOARD_TOP), xd, (0, 0, -1))) for name, (x, y), xd in TRAY_BAY["modules"]]


def _world(loc, x, y, z=0.0):
    p = loc * Location((x, y, z))
    return tuple(p.position)


def tub_bosses():
    """World (x, y) of the eight S18V20 hole bosses."""
    return [_world(loc, x, y)[:2] for _, loc in tub_module_frames() for x, y in VENDOR_HOLES["S18V20X"]]


def tray_holes():
    """World (x, y) of the four S13V30F5 standoffs."""
    return [_world(loc, x, y)[:2] for _, loc in tray_module_frames() for x, y in VENDOR_HOLES["S13V30F5"]]


def tub_bay_plate():
    """The tub-bay plate (one print, PETG), with its bosses and pilots."""
    m = TUB_BAY
    plate = _blk(*m["plate"])
    for x0, x1, a, b in m["arms"]:
        for sy in (1, -1):
            plate = plate + _blk(x0, x1, *sorted((sy * a, sy * b)), m["plate"][4], m["plate"][5])
    top = m["plate"][5]
    for x, y in tub_bosses():
        plate = plate + _z_cyl(m["boss"][0], top - 0.01, top + m["boss"][1], x, y)
    for x, y in tub_bosses():
        plate = plate - _z_cyl(m["pilot"][0], top + m["boss"][1] - m["pilot"][1], top + m["boss"][1] + 0.1, x, y)
    for x, y in (*m["fix_rear"], *m["fix_front"]):
        plate = plate - _z_cyl(m["plate_hole"], m["plate"][4] - 0.1, top + 0.1, x, y)
    # The ballast bar's M3 countersunk heads (CH-038) sit only 0.1 mm under the deck top.
    r, depth = m["ballast_relief"]
    for y in (-20.0, 20.0):
        plate = plate - _z_cyl(r, m["plate"][4] - 0.1, m["plate"][4] + depth, 74.0, y)
    return _tag(plate, "TUB_BAY_MODULE_PLATE", "#4F575B")


def tub_bay_hardware():
    """The plate's four M3 screws and the four inserts in the deck."""
    m, out = TUB_BAY, []
    z0, top = m["plate"][4], m["plate"][5]
    for k, ((x, y), length, ins) in enumerate([*[(p, 6.0, m["insert_rear"]) for p in m["fix_rear"]],
                                                *[(p, 8.0, m["insert_front"]) for p in m["fix_front"]]], start=1):
        screw = _z_cyl(M3_BUTTON[0], top, top + M3_BUTTON[1], x, y) + _z_cyl(1.5, top - length, top, x, y)
        out.append(_tag(screw, f"TUB_BAY_PLATE_M3X{int(length)}_SCREW_{k}", _body.STEEL))
        r_out, r_in, l = ins
        ring = _z_cyl(r_out, z0 - l, z0, x, y) - _z_cyl(r_in, z0 - l - 0.1, z0 + 0.1, x, y)
        out.append(_tag(ring, f"TUB_BAY_DECK_INSERT_M3X{int(l)}_{k}", _body.BRONZE))
    return out


def tub_bay_deck_pilots():
    """CHASSIS_FRAME_FRONT_MODULE cuts: Ø4.0 insert pilots for the plate screws."""
    m, z0 = TUB_BAY, TUB_BAY["plate"][4]
    out = [_z_cyl(m["pilot_r"], z0 - m["insert_rear"][2] - 0.1, z0 + 0.1, x, y) for x, y in m["fix_rear"]]
    out += [_z_cyl(m["pilot_r"], z0 - m["insert_front"][2] - 0.6, z0 + 0.1, x, y) for x, y in m["fix_front"]]
    return out


def tub_modules():
    """M2 and M3 groups: each S18V20ALV and its four M2 x 5 screws."""
    groups = []
    for (name, loc), what in zip(tub_module_frames(), ("5V5_HEAD", "11V1_YAW")):
        board_top = TUB_BOARD_Z + PCB_T
        parts = [_tag(_place(vendor_solid("S18V20X"), loc), f"{name}_POLOLU_2572_S18V20ALV_{what}_STEP", "#2D6B3F")]
        for k, (lx, ly) in enumerate(VENDOR_HOLES["S18V20X"], start=1):
            x, y, _ = _world(loc, lx, ly)
            screw = _z_cyl(M2_HEAD[0], board_top, board_top + M2_HEAD[1], x, y) + _z_cyl(0.75, board_top - TUB_BAY["screw_len"], board_top, x, y)
            parts.append(_tag(screw, f"{name}_M2X5_THREAD_FORMING_SCREW_{k}", _body.STEEL))
        groups.append(parts)
    return groups


def tray_modules():
    """M4 and M5 groups: each S13V30F5 with two standoffs and four screws."""
    m, groups = TRAY_BAY, []
    for (name, loc), what in zip(tray_module_frames(), ("PI5", "SHARED_5V")):
        parts = [_tag(_place(vendor_solid("S13V30F5"), loc), f"{name}_POLOLU_4082_S13V30F5_{what}_STEP", "#2D6B3F")]
        r, length = m["standoff"]
        for k, (lx, ly) in enumerate(VENDOR_HOLES["S13V30F5"], start=1):
            x, y, _ = _world(loc, lx, ly)
            stand = _z_cyl(r, TRAY_BOARD_TOP, m["tray_z"], x, y) - _z_cyl(0.8, TRAY_BOARD_TOP - 0.1, m["tray_z"] + 0.1, x, y)
            tray_top = m["tray_z"] + 3.0
            top = _z_cyl(M2_HEAD[0], tray_top, tray_top + M2_HEAD[1], x, y) + _z_cyl(0.8, tray_top - m["top_screw"], tray_top, x, y)
            under = TRAY_BOARD_TOP - PCB_T
            bottom = _z_cyl(M2_HEAD[0], under - M2_HEAD[1], under, x, y) + _z_cyl(0.8, under, under + m["bottom_screw"], x, y)
            parts += [_tag(stand, f"{name}_M2X5_FF_ROUND_STANDOFF_{k}", _body.BRONZE),
                      _tag(top, f"{name}_M2X5_TRAY_SCREW_{k}", _body.STEEL),
                      _tag(bottom, f"{name}_M2X4_BOARD_SCREW_{k}", _body.STEEL)]
        groups.append(parts)
    return groups


def tray_holes_cuts():
    """COMPUTE_TRAY cuts: Ø2.4 through holes for the standoff screws."""
    z = TRAY_BAY["tray_z"]
    return [_z_cyl(TRAY_BAY["hole_r"], z - 0.1, z + 3.1, x, y) for x, y in tray_holes()]


def _cradle_x(face_x, sign, y0, y1, z0, z1, open_edge):
    """A cradle on a plate face normal to X, opening toward sign*X, for a board spanning y0..y1, z0..z1.

    open_edge is one of '+y', '-y', '+z', '-z' (the wire edge, left open).
    """
    c = CRADLE
    g, rim, pad = c["gap"], c["rim"], c["pad"]
    depth = pad + PCB_T + c["lip"]
    xa, xb = sorted((face_x - sign * 0.01, face_x + sign * depth))
    outer = _blk(xa, xb, y0 - g - rim, y1 + g + rim, z0 - g - rim, z1 + g + rim)
    inner = _blk(xa - 1.0, xb + 1.0, y0 - g, y1 + g, z0 - g, z1 + g)
    frame = outer - inner
    cut = {"+y": (y1 - 1.0, y1 + 5.0, z0 + 2.0, z1 - 2.0), "-y": (y0 - 5.0, y0 + 1.0, z0 + 2.0, z1 - 2.0),
           "+z": (y0 + 2.0, y1 - 2.0, z1 - 1.0, z1 + 5.0), "-z": (y0 + 2.0, y1 - 2.0, z0 - 5.0, z0 + 1.0)}[open_edge]
    frame = frame - _blk(xa - 1.0, xb + 1.0, *cut)
    pa, pb = sorted((face_x - sign * 0.01, face_x + sign * pad))
    s = c["pad_size"]
    for y, z in ((y0, z0), (y1 - s, z0), (y0, z1 - s), (y1 - s, z1 - s)):
        frame = frame + _blk(pa, pb, y, y + s, z, z + s)
    return frame


def _switch_frame():
    """#2813 STEP frame on the rear plate: local x down (-Z), local y along +Y, components +X."""
    face = REAR_BAY["plate"][1] + CRADLE["pad"]
    return _frame((face, REAR_SWITCH["y0"], REAR_SWITCH["z_top"]), (0, 0, -1), (1, 0, 0))


def rear_bay_plate():
    """The rear-bay plate with legs, rail arms, counterbored screw holes and two cradles."""
    m = REAR_BAY
    x0, x1 = m["plate"][0], m["plate"][1]
    plate = _blk(*m["plate"])
    for ya, yb in m["legs"]:
        plate = plate + _blk(x0, x1, ya, yb, *m["leg_z"])
    for ya, yb in m["arms"]:
        plate = plate + _blk(*m["arm_x"], ya, yb, *m["arm_z"])
    face = x1
    sy0, zt = REAR_SWITCH["y0"], REAR_SWITCH["z_top"]
    plate = plate + _cradle_x(face, 1, sy0, sy0 + 25.4, zt - 20.32, zt, "+y")
    iy, iz = INA226_AT
    w, h = INA226_BOARD[0], INA226_BOARD[1]
    plate = plate + _cradle_x(face, 1, iy, iy + w, iz, iz + h, "-y")
    cr, seat = m["cbore"]
    for y, z in m["screw_yz"]:
        plate = plate - _x_cyl(cr, x0 - 0.1, seat, y, z) - _x_cyl(m["clear_r"], seat - 0.1, m["arm_x"][1] + 0.1, y, z)
    return _tag(plate, "REAR_BAY_MODULE_PLATE", "#4F575B")


def rear_bay_hardware():
    m, out = REAR_BAY, []
    seat = m["cbore"][1]
    for k, (y, z) in enumerate(m["screw_yz"], start=1):
        screw = _x_cyl(M3_BUTTON[0], seat - M3_BUTTON[1], seat, y, z) + _x_cyl(1.5, seat, seat + m["screw_len"], y, z)
        out.append(_tag(screw, f"REAR_BAY_PLATE_M3X16_SCREW_{k}", _body.STEEL))
        r_out, r_in, l = m["insert"]
        f = m["rail_face"]
        ring = _x_cyl(r_out, f, f + l, y, z) - _x_cyl(r_in, f - 0.1, f + l + 0.1, y, z)
        out.append(_tag(ring, f"REAR_BAY_RAIL_INSERT_M3X6_{k}", _body.BRONZE))
    return out


def rear_bay_rail_pilots():
    m = REAR_BAY
    r, depth = m["rail_pilot"]
    return [_x_cyl(r, m["rail_face"] - 0.05, m["rail_face"] + depth, y, z) for y, z in m["screw_yz"]]


def rear_modules():
    """M1 (switch) and M6 (INA226) groups, and the charge splice."""
    switch = [_tag(_place(vendor_solid("PSW_2813"), _switch_frame()), "M1_POLOLU_2813_PUSHBUTTON_POWER_SWITCH_HP_STEP", "#2D6B3F")]
    iy, iz = INA226_AT
    w, h, t, parts = INA226_BOARD
    bx = REAR_BAY["plate"][1] + CRADLE["pad"]
    ina = [_tag(_blk(bx, bx + t, iy, iy + w, iz, iz + h), "M6_INA226_R010_BOARD_UNMEASURED", _body.PCB_GREEN),
           _tag(_blk(bx + t, bx + t + parts, iy + 2.0, iy + w - 2.0, iz + 2.0, iz + h - 2.0), "M6_INA226_PARTS_ENVELOPE_UNMEASURED", "#D38132", 0.55)]
    s = CHARGE_SPLICE
    splice = [_tag(_z_cyl(s["r"], *s["z"], *s["axis"]), "CHARGE_SPLICE_HEATSHRUNK_AWG16", "#202020"),
              _tag(_blk(*s["reserve"]), "CHARGE_SPLICE_AND_LEADS_RESERVE", "#E7A95B", 0.25)]
    return switch, ina, splice


def _port_box(port, extra=0.0, x1=None):
    p = PORTS[port]
    (y, z), (w, h, length) = p["yz"], p["body"]
    mouth = PORTS["face_x"] + PORTS["recess"]
    return _blk(mouth - extra, (mouth + length if x1 is None else x1) + extra, y - w / 2 - extra, y + w / 2 + extra, z - h / 2 - extra, z + h / 2 + extra)


def rear_panel_port_cuts():
    """REAR_SERVICE_PANEL_OCTAGONAL cuts: the XT30 hole and the XH slot, through the pad and skin."""
    out = []
    for k in ("xt30", "xh"):
        (y, z), (w, h, _), c = PORTS[k]["yz"], PORTS[k]["body"], PORTS[k]["clear"]
        out.append(_blk(-66.0, -50.0, y - w / 2 - c, y + w / 2 + c, z - h / 2 - c, z + h / 2 + c))
    return out


def rear_panel_fill():
    """REAR_SERVICE_PANEL_OCTAGONAL add: the PCB-13 pocket, hole, relief and pilots filled, ports kept open."""
    pad, cuts = _body.rear_panel_charge_inlet()
    fill = pad & cuts
    for tool in rear_panel_port_cuts():
        fill = fill - tool
    return fill


def port_parts():
    """M12 parts: XT30 female, parked XHP-3 plug, PA break, and the lead and corridor reserves."""
    out = [_tag(_port_box("xt30"), "M12_XT30U_FEMALE_CHARGE_PORT", "#E5C34B"),
           _tag(_port_box("xh"), "M12_JST_XHP_3_BALANCE_PORT_PLUG", "#F4F1E6"),
           _tag(_blk(*BALANCE["pair"]), "M12_JST_PA_3P_BALANCE_BREAK_MATED_PAIR", "#F4F1E6")]
    length, w, h = PORTS["corridor"]
    mouth = PORTS["face_x"] + PORTS["recess"]
    for k in ("xt30", "xh"):
        y, z = PORTS[k]["yz"]
        skin = PORTS["skin_x"]
        out.append(_tag(_blk(skin - length, skin, y - w / 2, y + w / 2, z - h / 2, z + h / 2),
                        f"M12_{k.upper()}_MATING_PLUG_CORRIDOR_KEEP_OUT", "#79C4CB", 0.15))
    for k, box in enumerate(BALANCE["pack_lead"], start=1):
        out.append(_tag(_blk(*box), f"M12_BALANCE_PACK_LEAD_RESERVE_{k}", "#44BDD0", 0.42))
    for k, box in enumerate(BALANCE["body_lead"], start=1):
        out.append(_tag(_blk(*box), f"M12_BALANCE_BODY_LEAD_RESERVE_{k}", "#44BDD0", 0.42))
    return out


def balance_deck_hole():
    x, y, r = BALANCE["deck_hole"]
    return _z_cyl(r, 50.0, 58.0, x, y)


def mic_boss_tools():
    """(cuts, adds) on BODY_SHELL for the four INMP441 bosses (cuts run before adds)."""
    m = MIC
    outer = _body._shell_outer()
    cuts, adds = [], []
    hx, hz = m["boss_half"]
    pw, ph = m["pocket"]
    for x, y, z, _name in _body.MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0

        def bore(r, a, b, xx=x, zz=z):
            return _body._axial_bore_y(r, sign * a, sign * b, xx, zz)

        far = 85.0
        f = m["seat"]
        pts = [(f, z - hz), (far, z - hz), (far, z + hz + (far - f)), (f, z + hz)]
        boss = extrude((Plane.YZ * Polygon(*pts, align=None)).moved(Location((x - hx, 0.0, 0.0))), amount=2.0 * hx)
        if sign < 0:
            boss = boss.mirror(Plane.XZ)
        boss = boss & outer
        pocket = _blk(x - pw / 2, x + pw / 2, *sorted((sign * (f - 0.1), sign * MIC_FLOOR)), z - ph / 2, z + ph / 2)
        gasket = bore(m["gasket_pocket"], MIC_FLOOR - 0.1, MIC_FLOOR + m["gasket"][2])
        port = bore(_body.MIC_PORT_RADIUS, f - 0.1, 90.0)
        pilots = [bore(m["pilot"][0], f - 0.1, f + m["pilot"][1], x + du) for du in (-m["screw_u"], m["screw_u"])]
        voids = [pocket, gasket, port, *pilots]
        cuts += [pocket, gasket, *pilots]
        for v in voids:
            boss = boss - v
        adds.append(boss)
    return cuts, adds


def mic_modules():
    """M9: four INMP441 modules with gasket, two M2 x 4 screws and washers, and a soldered pigtail."""
    m, groups = MIC, []
    bw, bh, bt = m["board"]
    for x, y, z, name in _body.MICROPHONE_PORTS:
        sign = 1.0 if y > 0.0 else -1.0
        centre = -1.0 if x > _body.BODY_AXIS_X else 1.0
        f = m["seat"]

        def ys(a, b):
            return sorted((sign * a, sign * b))

        def bore(r, a, b, xx=x, zz=z):
            return _body._axial_bore_y(r, sign * a, sign * b, xx, zz)

        board = _blk(x - bw / 2, x + bw / 2, *ys(f, MIC_FLOOR), z - bh / 2, z + bh / 2) - bore(0.4, f - 0.5, MIC_FLOOR + 0.5)
        pw, pz, pt = m["package"]
        mic = _blk(x - pw / 2, x + pw / 2, *ys(f - pt, f), z - pz / 2, z + pz / 2)
        go, gi, gt = m["gasket"]
        gasket = bore(go, MIC_FLOOR, MIC_FLOOR + gt) - bore(gi, MIC_FLOOR - 0.1, MIC_FLOOR + gt + 0.1)
        parts = [_tag(board, f"M9_INMP441_{name}_BOARD_UNMEASURED", _body.PCB_GREEN, 0.94),
                 _tag(mic, f"M9_INMP441_{name}_MIC_PACKAGE", "#C9CDD0"),
                 _tag(gasket, f"M9_INMP441_{name}_GASKET", _body.RUBBER, 0.9)]
        wr, wt = m["washer"]
        for k, du in enumerate((-m["screw_u"], m["screw_u"]), start=1):
            xx = x + du
            washer = bore(wr, f - wt, f, xx) - bore(1.1, f - wt - 0.1, f + 0.1, xx)
            screw = bore(M2_HEAD[0], f - wt - M2_HEAD[1], f - wt, xx) + bore(0.75, f - wt, f - wt + m["screw_len"], xx)
            parts += [_tag(washer, f"M9_INMP441_{name}_M2_WASHER_{k}", _body.STEEL),
                      _tag(screw, f"M9_INMP441_{name}_M2X4_SCREW_{k}", _body.STEEL)]
        t, hv, run = m["pigtail"]
        xs = sorted((x + centre * 3.0, x + centre * (bw / 2 + run)))
        parts.append(_tag(_blk(*xs, *ys(f - t, f), z + bh / 2 - 2.0 * hv, z + bh / 2), f"M9_INMP441_{name}_PIGTAIL_RESERVE", "#F4F1E6", 0.6))
        groups.append((name, parts))
    return groups


def amp_bracket():
    """BODY_FRAME_MAIN_PRINT add: the bracket on the front +Y post, the amp cradle and the hub bosses."""
    a, h = AMP, HUB
    x0, x1, y0, y1, z0, z1 = a["bracket"]
    shape = _blk(*a["bracket"])
    ay, az = a["at"]
    bw, bh, _ = a["board"]
    shape = shape + _cradle_x(x1, 1, ay, ay + bw, az, az + bh, "-z")
    hy, hz = h["at"]
    r, ht = h["boss"]
    for u, v in h["holes"]:
        shape = shape + _x_cyl(r, x0 - ht, x0 + 0.01, hy + u, hz + v) - _x_cyl(0.8, x0 - ht - 0.1, x0 + 1.5, hy + u, hz + v)
    return shape


def amp_parts():
    """M8 amp and M13 hub groups."""
    a, h = AMP, HUB
    x1 = a["bracket"][1] + CRADLE["pad"]
    ay, az = a["at"]
    bw, bh, bt = a["board"]
    tw, tz, th = a["terminal"]
    amp = [_tag(_blk(x1, x1 + bt, ay, ay + bw, az, az + bh), "M8_MAX98357A_BOARD_UNMEASURED", _body.PCB_GREEN),
           _tag(_blk(x1 + bt, x1 + bt + a["parts"], ay + 2.0, ay + bw - 2.0, az + 4.0, az + bh - tz - 1.0), "M8_MAX98357A_PARTS_ENVELOPE_UNMEASURED", "#D38132", 0.55),
           _tag(_blk(x1 + bt, x1 + bt + th, ay + (bw - tw) / 2, ay + (bw + tw) / 2, az + bh - tz, az + bh), "M8_SPEAKER_SCREW_TERMINAL_UNMEASURED", "#2E7D4F")]
    hx1 = a["bracket"][0] - h["boss"][1]
    hw, hh, ht = h["board"]
    hy, hz = h["at"]
    hub = [_tag(_blk(hx1 - ht, hx1, hy, hy + hw, hz, hz + hh), "M13_AUDIO_HUB_PERFBOARD", "#C8A060"),
           _tag(_blk(hx1 - ht - h["parts"], hx1 - ht, hy + 1.0, hy + hw - 1.0, hz + 1.0, hz + hh - 4.0), "M13_AUDIO_HUB_PARTS_ENVELOPE", "#D38132", 0.55)]
    for k, (u, v) in enumerate(h["holes"], start=1):
        screw = _x_cyl(M2_HEAD[0], hx1 - ht - M2_HEAD[1], hx1 - ht, hy + u, hz + v) + _x_cyl(0.75, hx1 - ht, hx1 - ht + h["screw"], hy + u, hz + v)
        hub.append(_tag(screw, f"M13_AUDIO_HUB_M2X4_SCREW_{k}", _body.STEEL))
    return amp, hub


def imu_adapter():
    """The printed LSM6DSOX adapter on the J15A pilots, with its two board bosses."""
    m = IMU
    shape = _blk(*m["adapter"])
    top = m["adapter"][5]
    x1 = m["board_x1"]
    bw = m["board"][0]
    hx = x1 - m["holes_v"]
    for u in m["holes_u"]:
        y = u - bw / 2.0
        shape = shape + _z_cyl(m["boss"][0], top - 0.01, top + m["boss"][1], hx, y)
        shape = shape - _z_cyl(0.8, m["adapter"][4] + 0.2, top + m["boss"][1] + 0.1, hx, y)
    for x, y in m["j15a"]:
        shape = shape - _z_cyl(1.1, m["adapter"][4] - 0.1, top + 0.1, x, y)
    return _tag(shape, "IMU_ADAPTER_LSM6DSOX", "#4F575B")


def imu_parts():
    """M7: the LSM6DSOX board, chip, two SH4 connectors, two board screws, two J15A screws."""
    m = IMU
    bw, bv, bt = m["board"]
    x1, z = m["board_x1"], IMU_BOARD_Z
    hx = x1 - m["holes_v"]
    board = _blk(x1 - bv, x1, -bw / 2, bw / 2, z, z + bt)
    for u in m["holes_u"]:
        board = board - _z_cyl(1.25, z - 0.1, z + bt + 0.1, hx, u - bw / 2)
    cu, cv, cw, cl, ch = m["chip"]
    chip = _blk(x1 - cv - cl / 2, x1 - cv + cl / 2, cu - bw / 2 - cw / 2, cu - bw / 2 + cw / 2, z + bt, z + bt + ch)
    parts = [_tag(board, "M7_ADAFRUIT_4438_LSM6DSOX_BOARD", "#1D3F8A"), _tag(chip, "M7_LSM6DSOX_LGA14", "#202020")]
    sw, sd, sh = m["sh4"]
    for k, sy in enumerate((-1, 1), start=1):
        ya, yb = sorted((sy * bw / 2, sy * (bw / 2 - sd)))
        parts.append(_tag(_blk(x1 - 8.89 - sw / 2, x1 - 8.89 + sw / 2, ya, yb, z + bt, z + bt + sh), f"M7_STEMMA_QT_SH4_{k}", "#F4F1E6"))
    top = z + bt
    for k, u in enumerate(m["holes_u"], start=1):
        y = u - bw / 2
        screw = _z_cyl(M2_HEAD[0], top, top + M2_HEAD[1], hx, y) + _z_cyl(0.75, top - 5.0, top, hx, y)
        parts.append(_tag(screw, f"M7_M2X5_THREAD_FORMING_SCREW_{k}", _body.STEEL))
    at = m["adapter"][5]
    for k, (x, y) in enumerate(m["j15a"], start=1):
        screw = _z_cyl(M2_HEAD[0], at, at + M2_HEAD[1], x, y) + _z_cyl(0.75, at - m["j15a_screw"], at, x, y)
        parts.append(_tag(screw, f"M7_J15A_M2X6_THREAD_FORMING_SCREW_{k}", _body.STEEL))
    return parts


def pcb08_servo_plug():
    return [_tag(_blk(*PCB08_SERVO["header"]), "YAW_JUNCTION_J8_8_FEETECH_5264_3P_HEADER", "#F4F1E6"),
            _tag(_blk(*PCB08_SERVO["plug"]), "YAW_JUNCTION_J8_8_YAW_SERVO_5264_3P_MATED_PLUG", "#F4F1E6")]


def bought_modules():
    """The 'Bought modules' group: one subgroup per D-094 module (M1-M9, M12, M13)."""
    (m2, m3), (m4, m5) = tub_modules(), tray_modules()
    switch, ina, splice = rear_modules()
    amp, hub = amp_parts()
    mics = [part for _, parts in mic_modules() for part in parts]
    groups = [
        ("M1 power switch, Pololu #2813 HP", switch),
        ("M2 head 5.5 V, Pololu S18V20ALV", m2),
        ("M3 yaw 11.1 V, Pololu S18V20ALV", m3),
        ("M4 Pi 5 V, Pololu S13V30F5", m4),
        ("M5 shared 5 V, Pololu S13V30F5", m5),
        ("M6 INA226 monitor (unmeasured)", ina),
        ("M7 IMU, Adafruit #4438 LSM6DSOX", imu_parts()),
        ("M8 amplifier, MAX98357A breakout (unmeasured)", amp),
        ("M9 microphones, INMP441 x4 (unmeasured)", mics),
        ("M12 charge and balance ports, charge splice", [*port_parts(), *splice]),
        ("M13 audio hub, perfboard", hub),
    ]
    return Compound(label="Bought modules", children=[Compound(label=name, children=parts) for name, parts in groups])


_MIC_CUTS, _MIC_ADDS = mic_boss_tools()


# Printed tools, not robot parts: (BOM ID, label, function giving the tool in the world frame).
PRINT_TOOLS = [
    ("CH-089", "AXLE_ALIGNMENT_PLUG", axle_alignment_plug),  # D-071
]
# Parts dropped whole (label fully matched, leaf or group), and parts inserted, world frame,
# as new children of the group whose label fully matches.
DROID_REMOVES = [
    # D-068: the generic DevKitC STEP and its header blocks; the two upper screws.
    r"C3_ESP32_S3_DEVKITC_STEP", r"C3_DEVKIT_HEADER_ROW_[12]", r"C3_CARRIER_M25_SCREW_(HEAD|SHANK)_[24]",
    # D-068 amended: the 7.26 mm Micro-Fit placeholder blocks, replaced by the real housing below.
    r"C3_J10_1_MICROFIT3_2P_(RA_HEADER|MATED_PLUG)",
    # D-072: the M3 x 18 housing screws, replaced by M3 x 16 below.
    r"AXLE_CAP_SCREW_M3X18_[LR]_[1-4]",
    # D-077: the plain nuts under the three top-driven J13 bolts; the bolts go into deck inserts.
    r"BODY_CHASSIS_M4_NUT_[123]",
    # D-079: the CNC Kitchen M3 x 5.7 insert models (OnlyScrews M3 x 6 below) and the 1.0 mm TCRT shims (1.2 mm below).
    *_NOSE_KEEL_REMOVES,
    # D-092: the Pi's header-side M2.5 x 6 screws, replaced by PCB-09's standoffs below.
    r"PI5_M25X6_SCREW_[34]",
    # D-095 (D-093): the dropped boards' placeholders with their plugs and reserves (PCB-02, 03, 04,
    # 05, 06 x4, 07, 13 and the W16 inlet lead), and PCB-08's J8-3/J8-5 sideband headers.
    r"PCB0[2345]_\w+", r"J[234]_\d_(MICROFIT\w+|GHR\d\d_MATED_PLUG)", r"CHARGE_INLET_\w+", r"PDM_MIC_(FRONT|REAR)_[LR]", r"IMU_PCB07",
    r"YAW_JUNCTION_J8_[35]_\w+",
]
DROID_INSERTS = [
    (r"C3_CARRIER_PCB10_WITH_DEVKITC", pcb10_devkitc()),
    *[(r"C3_CARRIER_PCB10_WITH_DEVKITC", shape) for shape in pcb10_j10_1()],
    *_AXLE_SCREW_INSERTS,  # D-072: M3 x 16 housing screws
    *_J13_INSERTS,  # D-077: M4 x 8 deck inserts at the three top-driven J13 bolts
    *_NOSE_KEEL_INSERTS,  # D-079: M3 x 6 inserts in the pod seat and both crossmembers; 1.2 mm TCRT shims
    *[(r"C0_LINK_ADAPTER_PCB09", part) for part in pcb09_mount_parts()],  # D-092: standoffs and screws
    # D-095: the tub-bay plate and the IMU adapter (chassis prints), the rear-bay plate (body print),
    # their fixings, and PCB-08's yaw servo plug. The modules themselves are in "Bought modules".
    (r"CHASSIS_PRIMARY_FRAME", tub_bay_plate()),
    *[(r"CHASSIS_PRIMARY_FRAME", part) for part in tub_bay_hardware()],
    (r"CHASSIS_PRIMARY_FRAME", imu_adapter()),
    (r"BODY_PRIMARY_FRAME", rear_bay_plate()),
    *[(r"BODY_PRIMARY_FRAME", part) for part in rear_bay_hardware()],
    *[(r"YAW_JUNCTION_PCB08", part) for part in pcb08_servo_plug()],
]


DROID_CUTS = [
    # D-059: PCB-15 component relief behind the nose Hall board, open at the top and
    # into the lead groove. D-063 deepens it 0.4 mm (to 1.3 mm) with the board.
    (r"BALL_POD_PRINTED_SEAT", (125.3, 126.6, 7.8, 12.2, 30.3, 35.01)),
    # D-063: the slot's back wall moves 0.4 mm back (X 126.5 -> 126.1); the board's
    # ends (local Y 0-0.8, 5.2-6.0) bear on it.
    (r"BALL_POD_PRINTED_SEAT", (126.1, 126.5, 6.9, 13.1, 30.3, 35.01)),
    # D-068: PCB-10 header-row reliefs in the C3 carrier uprights.
    *_PCB10_CUTS,
    (r"BODY_FRAME_C3_CARRIER_UPRIGHT_1", PCB10_JP1_RELIEF),
    # D-070: hub-cap peg holes (taking the old pegs) and the column trimmed flush.
    *_WHEEL_CAP_CUTS,
    # D-071: stub flange Ø24 -> Ø21; set-screw key notch in the carrier hub.
    *_AXLE_CUTS,
    # D-075: J04 rail pilots run Ø4.0 to 7 mm deep; Ø1.6 IMU screw pilots through the front deck.
    *_FRAME_CUTS,
    # D-077: Ø5.5 x 9 M4 insert pilots from the deck top at the three top-driven J13 bolts.
    *_J13_CUTS,
    # D-078: hatch-edge notch so the front-left J13 bolt comes out from below with the hatch on.
    (r"BATTERY_TUB_BOTTOM_HATCH", _z_cyl(HATCH_NOTCH[2], HATCH_NOTCH[3], HATCH_NOTCH[4], HATCH_NOTCH[0], HATCH_NOTCH[1])),
    # D-079: relief over the caster insert under the GP2Y; keel pilots 7 mm deep; keel sensor flat to Z 12.4,
    # bezel pilot and pin hole deeper; shoe groove 1 mm deeper.
    *_NOSE_KEEL_CUTS,
    # D-095: tub-plate insert pilots and the balance-lead hole in the front deck; rear-bay insert pilots in
    # the cross rail; standoff holes in the tray; XT30 and XH openings in the rear panel; INMP441 pockets.
    *[(r"CHASSIS_FRAME_FRONT_MODULE", tool) for tool in tub_bay_deck_pilots()],
    (r"CHASSIS_FRAME_FRONT_MODULE", balance_deck_hole()),
    *[(r"BODY_FRAME_MAIN_PRINT", tool) for tool in rear_bay_rail_pilots()],
    *[(r"COMPUTE_TRAY", tool) for tool in tray_holes_cuts()],
    *[(r"REAR_SERVICE_PANEL_OCTAGONAL", tool) for tool in rear_panel_port_cuts()],
    *[(r"BODY_SHELL", tool) for tool in _MIC_CUTS],
]
DROID_ADDS = [
    # D-074: PCB-09's strip must carry both rows of socket copper plus edge margin.
    # Grow only its +Y edge (20.9 -> 22.4); bridge, bay and board Z stay fixed.
    (r"C0_LINK_ADAPTER_PCB09_BOARD", (-4.7, 36.0, 20.9, 22.4, 106.4, 108.0)),
    # D-092: tabs out to the Pi's header-side holes, at the placeholder's Z (lifted with it below).
    *[(r"C0_LINK_ADAPTER_PCB09_BOARD", (x0, x1, y0, y1, 106.4, 108.0))
      for x0, x1, y0, y1 in (*PCB09_MOUNT["tabs"], PCB09_MOUNT["bay_extension"])],
    # D-068: PCB-10 top-edge hooks on the C3 carrier uprights.
    *_PCB10_ADDS,
    # D-068 amended: the carrier grows 6 mm down for a third connector row; the plug-layer reserve follows.
    *[(r"C3_CARRIER_PCB10_BOARD", b) for b in PCB10_BOARD_GROWTH],
    *[(r"C3_CARRIER_TOP_ENTRY_SIGNAL_PLUG_LAYER_RESERVE", (x0, x1, -56.8, -46.0, max(z0, 76.2), z1))
      for x0, x1, _, _, z0, z1 in PCB10_BOARD_GROWTH],
    # D-063: the slot's front wall moves 0.4 mm back too (X 127.5 -> 127.1), beside the
    # sensor notch (Y 8.3-11.7), so the slot stays 1.0 mm wide and locates the board.
    (r"BALL_POD_PRINTED_SEAT", (127.1, 127.5, 6.9, 8.3, 30.3, 35.0)),
    (r"BALL_POD_PRINTED_SEAT", (127.1, 127.5, 11.7, 13.1, 30.3, 35.0)),
    # D-065: PCB-11 socket and light-pipe sleeve inside the crown.
    (r"front_bezel_integral_camera_crown", pcb11_socket_local().moved(Location(HEAD_ORIGIN_IN_CHASSIS))),
    # D-070: hub holes filled and pegs on the hub; a boss round each cap hole.
    *_WHEEL_RIM_ADDS,
    *_WHEEL_CAP_ADDS,
    # D-071: housing screw holes Ø3.4 -> Ø3.2, so the housing refits where the motor was aligned.
    *_AXLE_ADDS,
    # D-075: frame insert pilots Ø4.3 -> Ø4.0 (J04 rail ends, J11A bosses), driver posts Ø3.9 -> Ø3.5.
    *_FRAME_ADDS,
    # D-076: the front module's rails, J13 ribs and crossmember down to the tub's Z 32 (prints tub
    # bottom down on one flat face); the rear crossmember strip behind the deck up to Z 56 (deck down).
    *_FRAME_PRINT_ADDS,
    # D-077: the three J13 nut sockets filled back to the rail, rib and deck (rear J04 key pockets kept).
    *_J13_ADDS,
    # D-079: the wear shoe's tongue 1 mm taller over its M2 pilot.
    *_NOSE_KEEL_ADDS,
    # D-095: the PCB-13 pocket, hole, relief and pilots filled round the new ports; the INMP441 bosses
    # (built with their own voids, so the cuts above stay open); the amp bracket on the front +Y post.
    (r"REAR_SERVICE_PANEL_OCTAGONAL", rear_panel_fill()),
    *[(r"BODY_SHELL", tool) for tool in _MIC_ADDS],
    (r"BODY_FRAME_MAIN_PRINT", amp_bracket()),
]
DROID_MOVES = [
    # D-068 amended: C3 GH headers and plugs into the three proved rows; the J10-1 plug reserve down
    # with the real Micro-Fit (centre Z 89.5 -> 83.43).
    *pcb10_connector_moves(),
    (r"C3_CARRIER_EDGE_CONNECTOR_J101_RESERVE", (0.0, 0.0, -6.07)),
    # D-063: PCB-15 sits 0.4 mm further back (X 126.2-127.0), so U1 clears the magnet
    # at the cap's 3 mm stop.
    (r"BALL_NOSE_HALL_(CARRIER_PCB|DRV5055A3_SOT23)", (-0.4, 0.0, 0.0)),
    # D-092: PCB-09 and its placeholder parts rise 0.05 mm onto the 11 mm standoffs.
    (PCB09_MOVED, (0.0, 0.0, PCB09_MOUNT["lift"])),
]


def _cut_box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))


def _tool(value):
    return value if isinstance(value, Shape) else _cut_box(*value)



def _cut_parts(node, parent_location, hits):
    children = list(node.children) if getattr(node, "children", None) else []
    if children:
        here = parent_location * node.location
        kept = []
        for child in children:
            gone = [r for r in DROID_REMOVES if re.fullmatch(r, child.label or "")]
            for r in gone:
                hits["remove", r] += 1
            if not gone:
                kept.append(_cut_parts(child, here, hits))
        kept = [k for k in kept if k is not None]   # D-095: a group emptied by removals goes too
        for pattern, shape in DROID_INSERTS:
            if re.fullmatch(pattern, node.label or ""):
                hits["insert", pattern] += 1
                kept.append(shape.moved(here.inverse()))
        if len(kept) == len(children) and all(k is c for k, c in zip(kept, children)):
            return node
        if not kept:
            return None
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
            part = _shifted(part, parent_location.inverse() * Location(value) * parent_location)
    part.label, part.color = node.label, node.color
    return part


def _apply_droid_cuts(robot, strict=True):
    """Apply DROID_CUTS, DROID_ADDS, DROID_MOVES, DROID_REMOVES and DROID_INSERTS; every entry must hit.

    strict=False is for check scripts that build one subsystem tree: entries for
    parts outside it are skipped.
    """
    tables = (("cut", DROID_CUTS), ("add", DROID_ADDS), ("move", DROID_MOVES))
    hits = {(kind, value): 0 for kind, table in tables for _, value in table}
    hits.update({("remove", r): 0 for r in DROID_REMOVES})
    hits.update({("insert", r): 0 for r, _ in DROID_INSERTS})
    robot = _cut_parts(robot, Location(), hits)
    missing = [pattern for kind, table in tables for pattern, value in table if not hits[kind, value]]
    missing += [r for r in DROID_REMOVES if not hits["remove", r]]
    missing += [r for r, _ in DROID_INSERTS if not hits["insert", r]]
    assert not (strict and missing), f"droid change labels not found: {missing}"
    return robot


# Custom boards (04-pcbs/README.md register), pulled out of the subsystem trees
# into one "Custom PCBs" group so they can be shown or isolated together.
# Each pattern must fully match the label of a node in the subsystem tree; the
# node moves whole, keeping its global placement. PCB-01 is a bought BMS
# (Robocraze TIFPS0629, D-019) and stays on the pack. D-093 replaced PCB-02 to 07 and
# deleted PCB-13; their bought modules are in the "Bought modules" group (D-095).
CUSTOM_PCBS = [
    ("PCB-08 yaw junction", r"YAW_JUNCTION_PCB08"),
    ("PCB-09 C0 link adapter", r"C0_LINK_ADAPTER_PCB09"),
    ("PCB-10 C3 controller carrier", r"C3_CARRIER_PCB10_WITH_DEVKITC"),
    ("PCB-11 status LED carrier", r"status_LED_(PCB08_carrier_5x5|WS2812B_2020)"),
    # Only the ESP32-S3-Zero module is drawn; the carrier board is not modelled yet.
    ("PCB-12 C2 head controller", r"C2_ESP32_S3_Zero_23_5x18_footprint"),
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
