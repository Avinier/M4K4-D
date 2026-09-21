"""Typed coordination payloads for exploratory layout revision 2.

Not a registered ICD. Envelope framing stays in codec.py. BASE_STATE is 62 bytes
with cue identity, onset, and safety/health fields retained; it fits the 64-byte
candidate. Do not drop those fields to make room.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import struct

CUE_IDENTITY = struct.Struct("<HIB")
HEAD_GOAL = struct.Struct("<HIBQHBBhhhHQB")
FACE_STATE = struct.Struct("<HIBQBbbBBBBQ")
LIGHT_STATE = struct.Struct("<HIBQBBHQ")
FACE_REPORT = struct.Struct("<HIBBQB")
LIGHT_REPORT = struct.Struct("<HIBBQB")
NACK = struct.Struct("<HHIBB")
BASE_GOAL = struct.Struct("<HIBQBhhhHQB")
BASE_STATE = struct.Struct("<HIBQQBhhiiiihhihhBBHH")

assert CUE_IDENTITY.size == 7
assert HEAD_GOAL.size == 36
assert BASE_STATE.size == 62
assert BASE_STATE.size <= 64
assert NACK.size == 10

# Numeric lateness window remains unregistered. Tests pass a value explicitly.
LATENESS_WINDOW_US_UNREGISTERED = None


class NackReason(IntEnum):
    OK = 0
    EXPIRED = 1
    OUT_OF_LIMITS = 2
    INHIBITED = 3
    UNKNOWN_TYPE = 4
    BAD_CRC = 5
    QUEUE_FULL = 6
    NO_LIMITS = 7
    NONCE_REPLAY = 8
    TIME_MODEL_INVALID = 9
    LATE = 10
    STALE_EPOCH = 11


@dataclass(frozen=True)
class CueIdentity:
    perf_id: int
    perf_epoch: int
    cue_id: int


@dataclass(frozen=True)
class HeadGoal:
    identity: CueIdentity
    start_at_us: int
    gesture_id: int
    segment: int
    profile: int
    yaw: int
    pitch: int
    roll: int
    duration_ms: int
    valid_until_us: int
    flags: int


@dataclass(frozen=True)
class BaseState:
    identity: CueIdentity
    capture_ts_us: int
    onset_ts_us: int
    progress: int
    v_mm_s: int
    omega_mrad_s: int
    x_mm: int
    y_mm: int
    theta_mrad: int
    wheel_l_pos_mrad: int
    wheel_l_vel_mrad_s: int
    wheel_l_cur_mA: int
    wheel_r_pos_mrad: int
    wheel_r_vel_mrad_s: int
    wheel_r_cur_mA: int
    ctrl_state: int
    mode: int
    sensor_valid_mask: int
    oldest_sensor_age_ms: int


@dataclass(frozen=True)
class Nack:
    for_seq: int
    identity: CueIdentity
    reason: NackReason


def pack_head_goal(g: HeadGoal) -> bytes:
    return HEAD_GOAL.pack(
        g.identity.perf_id, g.identity.perf_epoch, g.identity.cue_id,
        g.start_at_us, g.gesture_id, g.segment, g.profile,
        g.yaw, g.pitch, g.roll, g.duration_ms, g.valid_until_us, g.flags,
    )


def unpack_head_goal(raw: bytes) -> HeadGoal:
    (perf_id, perf_epoch, cue_id, start_at, gesture, segment, profile,
     yaw, pitch, roll, duration, valid_until, flags) = HEAD_GOAL.unpack(raw)
    return HeadGoal(
        CueIdentity(perf_id, perf_epoch, cue_id), start_at, gesture, segment,
        profile, yaw, pitch, roll, duration, valid_until, flags,
    )


def pack_base_state(s: BaseState) -> bytes:
    return BASE_STATE.pack(
        s.identity.perf_id, s.identity.perf_epoch, s.identity.cue_id,
        s.capture_ts_us, s.onset_ts_us, s.progress, s.v_mm_s, s.omega_mrad_s,
        s.x_mm, s.y_mm, s.theta_mrad, s.wheel_l_pos_mrad, s.wheel_l_vel_mrad_s,
        s.wheel_l_cur_mA, s.wheel_r_pos_mrad, s.wheel_r_vel_mrad_s,
        s.wheel_r_cur_mA, s.ctrl_state, s.mode, s.sensor_valid_mask,
        s.oldest_sensor_age_ms,
    )


def unpack_base_state(raw: bytes) -> BaseState:
    fields = BASE_STATE.unpack(raw)
    return BaseState(
        CueIdentity(fields[0], fields[1], fields[2]),
        *fields[3:],
    )


def pack_nack(n: Nack) -> bytes:
    return NACK.pack(n.for_seq, n.identity.perf_id, n.identity.perf_epoch, n.identity.cue_id, int(n.reason))


def unpack_nack(raw: bytes) -> Nack:
    for_seq, perf_id, perf_epoch, cue_id, reason = NACK.unpack(raw)
    return Nack(for_seq, CueIdentity(perf_id, perf_epoch, cue_id), NackReason(reason))


def command_nack(
    *,
    start_at_us: int,
    valid_until_us: int,
    now_us: int,
    time_model_valid: bool,
    cmd_epoch: int,
    current_epoch: int,
    lateness_window_us: int,
) -> NackReason | None:
    """Executor reject policy for scheduled cues. Window numeric is a caller argument."""
    if cmd_epoch < current_epoch:
        return NackReason.STALE_EPOCH
    if start_at_us and start_at_us > valid_until_us:
        return NackReason.EXPIRED
    if start_at_us and not time_model_valid:
        return NackReason.TIME_MODEL_INVALID
    if start_at_us and now_us > start_at_us + lateness_window_us:
        return NackReason.LATE
    if now_us > valid_until_us:
        return NackReason.EXPIRED
    return None
