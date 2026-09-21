"""Envelope factories. Part-local origins documented per function."""

from __future__ import annotations

from cadgen import build123d as bd

from lib import params as P
from lib import shapes as S


def motor_keepout():
    """Origin at gearbox face centre. +Z along shaft (outboard). Encoder −Z."""
    gb = S.cyl(P.MOTOR_GB_D / 2, P.MOTOR_GB_L, "gearbox", "#C2410C",
               (0, 0, -P.MOTOR_GB_L / 2))
    can = S.cyl(P.MOTOR_CAN_D / 2, P.MOTOR_CAN_L, "can", "#9A3412",
                (0, 0, -P.MOTOR_GB_L - P.MOTOR_CAN_L / 2))
    enc = S.cyl(P.MOTOR_KEEPOUT_D / 2, P.MOTOR_ENC_L, "encoder_cap", "#7C2D12",
                (0, 0, -P.MOTOR_GB_L - P.MOTOR_CAN_L - P.MOTOR_ENC_L / 2))
    shaft = S.cyl(P.SHAFT_D / 2, P.SHAFT_LEN, "d_shaft", "#A8A29E",
                  (0, 0, P.SHAFT_LEN / 2))
    # two M3 face lands at 19 mm E
    s = P.MOTOR_FACE_M3 / 2
    pin1 = S.cyl(1.5, 3, "m3_face_a", "#57534E", (s, 0, 1.5))
    pin2 = S.cyl(1.5, 3, "m3_face_b", "#57534E", (-s, 0, 1.5))
    pig = S.box(8, 8, P.MOTOR_PIGTAIL_L, "pigtail_keepout", "#F97316",
                (0, 10, -P.MOTOR_GB_L - P.MOTOR_CAN_L - P.MOTOR_ENC_L - 8), 0.45)
    ko = S.cyl(P.MOTOR_KEEPOUT_D / 2, P.MOTOR_KEEPOUT_L, "keepout_cyl", "#FB923C",
               (0, 0, -P.MOTOR_KEEPOUT_L / 2 + 5), alpha=0.12)
    return bd.Compound(children=[gb, can, enc, shaft, pin1, pin2, pig, ko])


def wheel_family_c():
    """Origin at wheel centre. Axis = local +Z (rotated to +Y in assembly)."""
    tyre = S.cyl(P.WHEEL_OD / 2, P.WHEEL_WIDTH, "tyre", "#1C1917")
    bore = S.cyl(P.HUB_BORE / 2 + 0.2, P.WHEEL_WIDTH + 1, "bore_608", "#44403C")
    # envelope: tyre with visible 608 bore (don't boolean — keep both as children)
    rim = S.cyl(P.WHEEL_OD / 2 - 4, P.WHEEL_WIDTH - 4, "rim", "#292524")
    return bd.Compound(children=[tyre, rim, bore])


def hub_carrier():
    """Printed 608 carrier. Origin at inner 608 centre. +Z toward wheel."""
    body = S.box(28, 28, 16, "carrier", "#A8A29E")
    b1 = S.cyl(P.BEARING_OD / 2, P.BEARING_B, "608_a", "#D6D3D1", (0, 0, 4))
    b2 = S.cyl(P.BEARING_OD / 2, P.BEARING_B, "608_b", "#D6D3D1", (0, 0, -4))
    return bd.Compound(children=[body, b1, b2])


def motor_clamp():
    """Axle-centred saddle. Origin at motor axis. +Z outboard."""
    saddle = S.box(36, 22, 28, "saddle", "#78716C", (0, 0, -8))
    cap = S.box(36, 10, 12, "clamp_cap", "#57534E", (0, 14, -8))
    return bd.Compound(children=[saddle, cap])


def axle_frame():
    """Open frame. Origin = chassis origin (floor, axle contact, y=0)."""
    # two side rails, above ground-clearance band
    y = 48.0
    z = (P.GROUND_CLEARANCE_MIN + P.SHELL_CLEARANCE) / 2 + 4  # ~31
    rail_l = S.box(150, P.RAIL_T, 18, "rail_L", "#57534E", (20, y, z))
    rail_r = S.box(150, P.RAIL_T, 18, "rail_R", "#57534E", (20, -y, z))
    axle_beam = S.box(18, 110, 16, "axle_beam", "#44403C", (0, 0, P.H_AXLE))
    front_beam = S.box(14, 70, 14, "front_beam", "#44403C", (P.FRONT_CONTACT_X - 8, 0, P.H_AXLE - 4))
    rear_beam = S.box(14, 50, 12, "rear_beam", "#44403C", (-40, 0, P.H_AXLE - 6))
    # bulkhead at x=0 so a pack cannot sit on/behind the axle
    wall = S.box(8, 90, 36, "aft_bulkhead", "#292524", (-4, 0, 28))
    deck = S.box(90, 80, 4, "forward_deck", "#78716C", (50, 0, P.DECK_Z))
    return bd.Compound(children=[rail_l, rail_r, axle_beam, front_beam, rear_beam, wall, deck])


def ballast_bay():
    """Forward-only pocket. Origin at chassis origin. Cavity exists only for x>0."""
    tray = S.box(80, 50, 3, "tray", "#A8A29E", (55, 0, 14))
    wall_l = S.box(80, 3, 22, "bay_wall_L", "#A8A29E", (55, 25, 24))
    wall_r = S.box(80, 3, 22, "bay_wall_R", "#A8A29E", (55, -25, 24))
    # x-slide rails (independent of h-stack)
    rail = S.box(70, 6, 4, "x_slide", "#78716C", (55, 0, 18))
    return bd.Compound(children=[tray, wall_l, wall_r, rail])


def ballast_lump():
    return S.box(*P.BALLAST_BODY, "ballast", "#1E3A8A", (0, 0, 0))


def battery_dummy():
    return S.box(*P.BATTERY_BODY, "battery_dummy", "#1D4ED8", (0, 0, 0))


def front_mount():
    """Shared mount. Origin at F_MOUNT_FRONT (contact x, deck z). +Z up."""
    plate = S.box(40, 44, 6, "mount_plate", "#D6D3D1", (0, 0, -3))
    # slot allowing 105–115 contact x (10 mm travel) — modelled as a 12 mm slot
    slot = S.box(14, 8, 8, "reach_slot", "#44403C", (0, 0, -3))
    scale = S.box(4, 20, P.SHIM_MAX + 2, "mm_scale", "#E7E5E4", (18, 0, -P.SHIM_MAX / 2 - 4))
    return bd.Compound(children=[plate, slot, scale])


def shim_stack(height):
    h = max(height, 1.0)
    return S.box(32, 36, h, "shim_stack", "#FDE68A", (0, 0, -h / 2))


def adapter_ball():
    """Pololu 3-hole plate. Origin at hole-pattern centre, top face z=0, +Z up."""
    import math
    plate = S.box(28, 28, 4, "adp_ball_plate", "#86EFAC", (0, 0, -2))
    r = P.BALL_PCD / 2
    holes = []
    for i, ang in enumerate((90, 210, 330)):
        x = r * math.cos(math.radians(ang))
        y = r * math.sin(math.radians(ang))
        holes.append(S.cyl(1.6, 5, f"m3_{i}", "#14532D", (x, y, -2)))
    return bd.Compound(children=[plate, *holes])


def adapter_caster():
    """33×38 plate, holes 30×23. Origin at plate centre, top z=0."""
    plate = S.box(P.CASTER_PLATE[0], P.CASTER_PLATE[1], 4, "adp_cas_plate", "#93C5FD", (0, 0, -2))
    hx, hy = P.CASTER_HOLES[0] / 2, P.CASTER_HOLES[1] / 2
    holes = [S.cyl(2.25, 5, f"m4_{i}", "#1E3A8A", (sx * hx, sy * hy, -2))
             for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1)))]
    return bd.Compound(children=[plate, *holes])


def ball_transfer():
    """Origin at ground contact. +Z up. Housing sits on the ball."""
    ball = S.sphere(P.BALL_D / 2, "pom_ball", "#F5F5F4", (0, 0, P.BALL_D / 2))
    cup_z = P.BALL_NATIVE_H - 6
    cup = S.cyl(P.BALL_HOUSING_D / 2, 12, "housing", "#A8A29E", (0, 0, cup_z))
    return bd.Compound(children=[ball, cup])


def swivel_caster():
    """Origin at ground contact. Swivel axis at +x = trail (U). +Z up."""
    trail = P.CASTER_TRAIL_DISPLAY
    wheel = S.cyl(P.CASTER_WHEEL_D / 2, P.CASTER_WHEEL_W, "cas_wheel", "#0F172A",
                  (0, 0, P.CASTER_WHEEL_D / 2), "y")
    fork = S.box(10, 18, 20, "fork", "#334155", (trail * 0.3, 0, 22))
    plate = S.box(P.CASTER_PLATE[0], P.CASTER_PLATE[1], 3, "swivel_plate", "#64748B",
                  (trail, 0, P.CASTER_NATIVE_H - 1.5))
    stem = S.cyl(4, P.CASTER_NATIVE_H - P.CASTER_WHEEL_D / 2, "stem", "#475569",
                 (trail, 0, (P.CASTER_NATIVE_H + P.CASTER_WHEEL_D / 2) / 2))
    return bd.Compound(children=[wheel, fork, plate, stem])


def sweep_keepout(kind="ball"):
    """360° occupancy ghost. Origin at front contact. Sits on z=0."""
    if kind == "ball":
        h = P.BALL_NATIVE_H
        return S.cyl(P.BALL_HOUSING_D / 2 + 4, h,
                     "sweep_ball_360", "#C026D3", (0, 0, h / 2), alpha=0.12)
    r = P.CASTER_TRAIL_MAX + P.CASTER_WHEEL_D / 2 + 8
    h = P.CASTER_NATIVE_H
    return S.cyl(r, h, "sweep_caster_360", "#7C3AED",
                 (P.CASTER_TRAIL_DISPLAY, 0, h / 2), alpha=0.10)


def skid_carrier():
    """Origin at F_SKID_CONTACT. Reach/height are assembly placements."""
    arm = S.box(28, 16, 8, "skid_arm", "#B91C1C", (10, 0, P.SKID_HEIGHT + 6))
    scale = S.box(P.SKID_REACH_MAX - P.SKID_REACH_MIN + 4, 4, 3, "reach_scale",
                  "#FECACA", (0, 12, P.SKID_HEIGHT + 10))
    return bd.Compound(children=[arm, scale])


def skid_pad():
    dx, dy, dz = P.SKID_PAD
    return S.box(dx, dy, dz, "skid_pad", "#7F1D1D", (0, 0, dz / 2))


def tcrt():
    dx, dy, dz = P.CLIFF_BODY
    return S.box(dx, dy, dz, "tcrt5000", "#FACC15", (0, 0, dz / 2))


def gp2y():
    dx, dy, dz = P.IR_BODY
    body = S.box(dx, dy, dz, "gp2y_body", "#CA8A04", (0, 0, 0))
    oa = S.cyl(1.2, 20, "optical_axis", "#EF4444", (10, 0, 0), "x")
    return bd.Compound(children=[body, oa])


def bumper_bar():
    return S.box(*P.BUMPER_BAR, "bumper_bar", "#F59E0B", (0, 0, 0))


def bumper_switch():
    return S.box(*P.SWITCH_BODY, "microswitch", "#78350F", (0, 0, 0))


def imu_breakout():
    return S.box(*P.IMU_BODY, "imu_module_U", "#22D3EE", (0, 0, 0))


def c3_devkit():
    dx, dy, dz = P.C3_BOARD
    board = S.box(dx, dy, dz, "devkitc", "#166534", (0, 0, 0))
    usb = S.box(P.C3_USB_KEEP, 8, 6, "usb_keepout_U", "#86EFAC", (dx / 2 + P.C3_USB_KEEP / 2, 0, 0), 0.5)
    return bd.Compound(children=[board, usb])


def driver():
    return S.box(*P.DRV_INSTALLED, "drv8874_installed", "#4ADE80", (0, 0, 0))


def neck_trunk():
    return S.cyl(14, 70, "neck_trunk_void", "#A16207", (0, 0, 105), alpha=0.35)


def harness_volumes():
    mtr = S.box(12, 40, 10, "harness_motor", "#A8A29E", (8, 0, 58), 0.4)
    neck = S.box(10, 10, 50, "harness_neck", "#A8A29E", (8, 0, 100), 0.4)
    sense = S.box(50, 8, 8, "harness_sense", "#A8A29E", (60, 0, 40), 0.4)
    return bd.Compound(children=[mtr, neck, sense])


def head_lump():
    """Layout 03 AABB lump. Origin = head-local origin (front/bottom centre)."""
    dx, dy, dz = P.HEAD_BBOX
    # head-local: x -115..0, y ±75, z -60..104
    body = S.box(dx, dy, 104, "head_envelope", "#7C3AED", (-dx / 2, 0, 52), 0.28)
    neck = S.box(40, 116, 60, "neck_allocation", "#6D28D9", (-38, 0, -30), 0.22)
    com = S.sphere(6, "head_com", "#F5D0FE", P.HEAD_LOCAL_COM)
    yaw = S.cyl(4, 2, "yaw_demate", "#FBBF24", (-37.965, 0, -60))
    return bd.Compound(children=[body, neck, com, yaw])


def status_light():
    return S.cyl(6, 8, "status_cue", "#F472B6", (0, 0, 4))


def wheel_chock():
    return S.box(20, 30, 12, "chock", "#57534E", (0, 0, 6))


def sensor_interposer():
    return S.box(40, 20, 4, "interposer", "#FB7185", (0, 0, 0))
