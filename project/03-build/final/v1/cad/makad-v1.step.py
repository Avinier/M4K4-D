"""Makad v1, the whole robot: chassis v1, body v1 and head v1 from their live sources."""

from pathlib import Path
import importlib.util
import math
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


# D-069: PCB-13 pin relief in the rear-panel inlet pad, world frame. The body source's
# CHARGE_INLET_PIN_RELIEF (9.60 x 5.60 x 1.2) is cut from the seat at X -55.1 round the
# receptacle axis (Y 0, Z 64); this box widens it to 10.60 and runs 0.1 past the seat.
PCB13_RELIEF = (-56.3, -55.0, -5.3, 5.3, 61.2, 66.8)


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


# D-073: frame insert and screw pilots. The M3 x 6 inserts in hand (OnlyScrews, OD 4.4) sat in
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
    """D-073 world-frame (label, shape) cuts and adds on the two frame modules."""
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


# D-074: frame print orientation. The front module prints as it sits (tub bottom down), but its
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
    """D-074 world-frame (label, shape) adds: the front module's flat bottom, the rear deck plane."""
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


# D-075: J13 bolts into M4 heat-set inserts in the deck. The Ø10.4 nut sockets under the three
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
# D-076: the front-left J13 bolt (64, +48) goes in from below, and its Ø8 head overlapped the
# hatch edge (Y 46.5) by 2.5 mm, so the body could not come off with the hatch on. A Ø9.2 notch
# in the hatch edge, round the bolt axis, lets the head pass with 0.6 mm all round.
HATCH_NOTCH = (64.0, 48.0, 4.6, 29.0, 33.5)  # x, y, r, z0, z1


def j13_insert_edits():
    """D-075 (cuts, adds, inserts) for the three top-driven J13 points."""
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


# D-077: nose and keel pilots and shims. (1) The nine CNC Kitchen M3 x 5.7 positions take the M3 x 6
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
    # End cradles contact the real rounded TCRT case at its existing datum (D-077).
    cradle_x=((-59.8, -58.5), (-49.5, -48.2)),
    cradle_half_y=3.8, cradle_top=14.0, shim_window_x=(-59.9, -48.1),
    tongue_top=9.5,                             # shoe tongue Z 8.5 -> 9.5, straight sides at the top width
)


def nose_keel_edits():
    """D-077 (cuts, adds, removes, inserts) for the nose and keel."""
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
    # D-075: the plain nuts under the three top-driven J13 bolts; the bolts go into deck inserts.
    r"BODY_CHASSIS_M4_NUT_[123]",
    # D-077: the CNC Kitchen M3 x 5.7 insert models (OnlyScrews M3 x 6 below) and the 1.0 mm TCRT shims (1.2 mm below).
    *_NOSE_KEEL_REMOVES,
]
DROID_INSERTS = [
    (r"C3_CARRIER_PCB10_WITH_DEVKITC", pcb10_devkitc()),
    *[(r"C3_CARRIER_PCB10_WITH_DEVKITC", shape) for shape in pcb10_j10_1()],
    *_AXLE_SCREW_INSERTS,  # D-072: M3 x 16 housing screws
    *_J13_INSERTS,  # D-075: M4 x 8 deck inserts at the three top-driven J13 bolts
    *_NOSE_KEEL_INSERTS,  # D-077: M3 x 6 inserts in the pod seat and both crossmembers; 1.2 mm TCRT shims
]


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
    # D-068: PCB-10 header-row reliefs in the C3 carrier uprights.
    *_PCB10_CUTS,
    # D-069: the inlet pad's pin relief widens 9.60 -> 10.60 mm (Y +-5.30), so GCT's outer
    # USB4140 stake copper (Y +-4.87) and its fillets clear the PCB-13 seat; Z and depth unchanged.
    (r"REAR_SERVICE_PANEL_OCTAGONAL", PCB13_RELIEF),
    # D-070: hub-cap peg holes (taking the old pegs) and the column trimmed flush.
    *_WHEEL_CAP_CUTS,
    # D-071: stub flange Ø24 -> Ø21; set-screw key notch in the carrier hub.
    *_AXLE_CUTS,
    # D-073: J04 rail pilots run Ø4.0 to 7 mm deep; Ø1.6 IMU screw pilots through the front deck.
    *_FRAME_CUTS,
    # D-075: Ø5.5 x 9 M4 insert pilots from the deck top at the three top-driven J13 bolts.
    *_J13_CUTS,
    # D-076: hatch-edge notch so the front-left J13 bolt comes out from below with the hatch on.
    (r"BATTERY_TUB_BOTTOM_HATCH", _z_cyl(HATCH_NOTCH[2], HATCH_NOTCH[3], HATCH_NOTCH[4], HATCH_NOTCH[0], HATCH_NOTCH[1])),
    # D-077: relief over the caster insert under the GP2Y; keel pilots 7 mm deep; keel sensor flat to Z 12.4,
    # bezel pilot and pin hole deeper; shoe groove 1 mm deeper.
    *_NOSE_KEEL_CUTS,
]
DROID_ADDS = [
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
    # D-067: PCB-05 bosses under the frame, and the SMT spacers reflowed on the board.
    *[(r"BODY_FRAME_MAIN_PRINT", boss) for boss in _PCB05_BOSSES],
    *[(r"PCB05_AUDIO_FRONT_END_PCB", spacer) for spacer in _PCB05_SPACERS],
    # D-067 amended: the Micro-Fit 43650-0200 housing is 9.65 mm wide (Molex SD-43650-001), not the
    # placeholder's 7.26, and sits 1.5 mm further forward; header and plug grow to X 64.8-74.46, at
    # Molex's 6.98 mm mated height (the placeholder's 10 mm block is cut back in DROID_CUTS).
    (r"PCB05_J5_7_MICROFIT3_2P_RA_HEADER", (64.8, 74.46, -19.0, -9.0, 115.6, 122.6)),
    (r"PCB05_J5_7_MICROFIT3_2P_MATED_PLUG", (64.8, 74.46, -31.0, -19.0, 115.6, 122.6)),
    # D-070: hub holes filled and pegs on the hub; a boss round each cap hole.
    *_WHEEL_RIM_ADDS,
    *_WHEEL_CAP_ADDS,
    # D-071: housing screw holes Ø3.4 -> Ø3.2, so the housing refits where the motor was aligned.
    *_AXLE_ADDS,
    # D-073: frame insert pilots Ø4.3 -> Ø4.0 (J04 rail ends, J11A bosses), driver posts Ø3.9 -> Ø3.5.
    *_FRAME_ADDS,
    # D-074: the front module's rails, J13 ribs and crossmember down to the tub's Z 32 (prints tub
    # bottom down on one flat face); the rear crossmember strip behind the deck up to Z 56 (deck down).
    *_FRAME_PRINT_ADDS,
    # D-075: the three J13 nut sockets filled back to the rail, rib and deck (rear J04 key pockets kept).
    *_J13_ADDS,
    # D-077: the wear shoe's tongue 1 mm taller over its M2 pilot.
    *_NOSE_KEEL_ADDS,
]
DROID_MOVES = [
    # D-068 amended: C3 GH headers and plugs into the three proved rows; the J10-1 plug reserve down
    # with the real Micro-Fit (centre Z 89.5 -> 83.43).
    *pcb10_connector_moves(),
    (r"C3_CARRIER_EDGE_CONNECTOR_J101_RESERVE", (0.0, 0.0, -6.07)),
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
        kept = []
        for child in children:
            gone = [r for r in DROID_REMOVES if re.fullmatch(r, child.label or "")]
            for r in gone:
                hits["remove", r] += 1
            if not gone:
                kept.append(_cut_parts(child, here, hits))
        for pattern, shape in DROID_INSERTS:
            if re.fullmatch(pattern, node.label or ""):
                hits["insert", pattern] += 1
                kept.append(shape.moved(here.inverse()))
        if len(kept) == len(children) and all(k is c for k, c in zip(kept, children)):
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
