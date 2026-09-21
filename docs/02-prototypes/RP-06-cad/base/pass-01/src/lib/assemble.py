"""Place the Concept A envelope. `support` is `ball` or `caster`."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen.assembly import AssemblyHelper

from lib import params as P
from lib import parts as F
from lib import shapes as S
from lib.frames import frames
from lib.mass import mass_rows, physics

from adapter_ball import adapter_ball
from adapter_caster import adapter_caster
from axle_frame import axle_frame
from ballast_bay import ballast_bay
from ball_transfer import ball_transfer
from front_mount import front_mount
from head_lump import head_lump
from hub_carrier import hub_carrier
from motor import motor
from motor_clamp import motor_clamp
from skid_carrier import skid_carrier
from swivel_caster import swivel_caster
from wheel import wheel


def _add(asm, shape, name):
    return asm.add(shape, name)


def build_base(support="ball"):
    fr = frames(support)
    xc = P.FRONT_CONTACT_X
    asm = AssemblyHelper("RP03_BASE_PASS1")

    _add(asm, axle_frame(), "R_FRM_AXLE_FRAME")
    _add(asm, ballast_bay(), "R_BAY_BALLAST_BAY")

    # Drive: gearbox outboard, encoder inboard. Motor local +Z = shaft/outboard.
    y_face_l = P.WHEEL_Y_L - P.WHEEL_WIDTH / 2 - 2.0
    y_face_r = P.WHEEL_Y_R + P.WHEEL_WIDTH / 2 + 2.0
    _add(asm, bd.Pos(0, y_face_l, P.H_AXLE) * bd.Rot(-90, 0, 0) * motor(), "MOTOR_L")
    _add(asm, bd.Pos(0, y_face_r, P.H_AXLE) * bd.Rot(90, 0, 0) * motor(), "MOTOR_R")
    _add(asm, bd.Pos(0, y_face_l - 10, P.H_AXLE) * bd.Rot(-90, 0, 0) * motor_clamp(), "R_CLP_MOTOR_CLAMP_L")
    _add(asm, bd.Pos(0, y_face_r + 10, P.H_AXLE) * bd.Rot(90, 0, 0) * motor_clamp(), "R_CLP_MOTOR_CLAMP_R")
    _add(asm, bd.Pos(*fr["F_WHEEL_L"]) * bd.Rot(-90, 0, 0) * wheel(), "WHEEL_L")
    _add(asm, bd.Pos(*fr["F_WHEEL_R"]) * bd.Rot(90, 0, 0) * wheel(), "WHEEL_R")
    _add(asm, bd.Pos(0, y_face_l + 8, P.H_AXLE) * bd.Rot(-90, 0, 0) * hub_carrier(), "HUB_L")
    _add(asm, bd.Pos(0, y_face_r - 8, P.H_AXLE) * bd.Rot(90, 0, 0) * hub_carrier(), "HUB_R")

    # Front support — one mount, shim, selected article. Other adapter still present as a spare on the deck.
    _add(asm, bd.Pos(xc, 0, P.H_AXLE) * front_mount(), "R_MNT_MOUNT")
    shim_h = P.BALL_SHIM if support == "ball" else P.CASTER_SHIM
    _add(asm, bd.Pos(xc, 0, P.H_AXLE) * F.shim_stack(shim_h), "SHIM")
    if support == "ball":
        _add(asm, bd.Pos(xc, 0, P.BALL_NATIVE_H + 2) * adapter_ball(), "R_ADP_BALL")
        _add(asm, bd.Pos(xc, 0, 0) * ball_transfer(), "BALL_TRANSFER")
        _add(asm, bd.Pos(xc, 55, P.H_AXLE) * adapter_caster(), "R_ADP_CAS_SPARE")
        _add(asm, bd.Pos(xc, 0, 0) * F.sweep_keepout("ball"), "SWEEP_BALL")
    else:
        _add(asm, bd.Pos(xc, 0, P.CASTER_NATIVE_H + 2) * adapter_caster(), "R_ADP_CAS")
        _add(asm, bd.Pos(xc, 0, 0) * swivel_caster(), "SWIVEL_CASTER")
        _add(asm, bd.Pos(xc, 55, P.H_AXLE) * adapter_ball(), "R_ADP_BALL_SPARE")
        _add(asm, bd.Pos(xc, 0, 0) * F.sweep_keepout("caster"), "SWEEP_CASTER")

    # Rear skid
    _add(asm, bd.Pos(-P.SKID_REACH, 0, 0) * skid_carrier(), "R_SKID_CARRIER")
    _add(asm, bd.Pos(-P.SKID_REACH, 0, P.SKID_HEIGHT) * F.skid_pad(), "SKID_PAD")

    # Sensing from contact datums
    _add(asm, bd.Pos(*fr["F_CLIFF_F"]) * F.tcrt(), "CLIFF_F")
    _add(asm, bd.Pos(*fr["F_CLIFF_L"]) * F.tcrt(), "CLIFF_L")
    _add(asm, bd.Pos(*fr["F_CLIFF_R"]) * F.tcrt(), "CLIFF_R")
    _add(asm, bd.Pos(*fr["F_IR_OPTICAL"]) * F.gp2y(), "IR_FRONT")
    _add(asm, bd.Pos(*fr["F_BUMPER"]) * F.bumper_bar(), "BUMPER_BAR")
    _add(asm, bd.Pos(fr["F_BUMPER"][0], 90, 28) * F.bumper_switch(), "SWITCH_L")
    _add(asm, bd.Pos(fr["F_BUMPER"][0], -90, 28) * F.bumper_switch(), "SWITCH_R")
    _add(asm, bd.Pos(*fr["F_IMU"]) * F.imu_breakout(), "IMU_BASE")

    # Body electronics — all x>0 for the pack
    _add(asm, bd.Pos(48, 28, 72) * bd.Rot(0, 0, 90) * F.c3_devkit(), "C3_DEVKIT")
    _add(asm, bd.Pos(32, 16, 52) * F.driver(), "DRIVER_L")
    _add(asm, bd.Pos(32, -16, 52) * F.driver(), "DRIVER_R")
    _add(asm, bd.Pos(P.BATTERY_X, 0, P.BATTERY_Z) * F.battery_dummy(), "BATTERY_OR_DUMMY")
    _add(asm, bd.Pos(P.BALLAST_X, 0, P.BALLAST_Z) * F.ballast_lump(), "BALLAST")
    _add(asm, F.neck_trunk(), "NECK_TRUNK_VOID")
    _add(asm, F.harness_volumes(), "HARNESS_TRUNK")
    _add(asm, bd.Pos(*P.HEAD_ORIGIN_IN_CHASSIS) * head_lump(), "RP01_HEAD_LUMP")

    # Rig-only
    _add(asm, bd.Pos(20, 0, 148) * F.status_light(), "R_CUE_STATUS_LIGHT")
    _add(asm, bd.Pos(40, -40, 62) * F.sensor_interposer(), "R_INT_SENSOR_INTERPOSER")
    _add(asm, bd.Pos(18, P.WHEEL_Y_L, 6) * F.wheel_chock(), "R_CHK_CHOCK_L")
    _add(asm, bd.Pos(18, P.WHEEL_Y_R, 6) * F.wheel_chock(), "R_CHK_CHOCK_R")

    # Datums
    for name, xyz in fr.items():
        if name.startswith("F_") and isinstance(xyz, tuple):
            _add(asm, S.triad(xyz, name), f"DATUM_{name}")

    # CoM marker from the mass register (paper)
    rows = mass_rows(support)
    phys = physics(rows, support)
    cx, cy, cz = phys["com_mm"]
    _add(asm, S.sphere(8, "COM_SCORED", "#F43F5E", (cx, cy, cz), 0.6), "COM_SCORED")

    return asm.build()
