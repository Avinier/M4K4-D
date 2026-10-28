"""Phase A reference safety state machines; not a motor-control firmware."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from secrets import token_bytes


class Motion(Enum):
    INHIBITED = "inhibited"
    ENABLED = "enabled"
    BRAKING = "braking"


@dataclass
class AuthorityLease:
    """C0 core -> hardware daemon; renewal must come from action-loop progress."""

    ttl_us: int
    boot_uuid: bytes | None = None
    epoch: int = 0
    deadline_us: int = 0
    valid: bool = False

    def renew(self, boot_uuid: bytes, epoch: int, now_us: int, action_loop_advanced: bool) -> bool:
        if len(boot_uuid) != 16 or not action_loop_advanced or epoch <= 0:
            return False
        if self.valid and (boot_uuid != self.boot_uuid or epoch != self.epoch):
            self.valid = False
        self.boot_uuid, self.epoch = boot_uuid, epoch
        self.deadline_us = now_us + self.ttl_us
        self.valid = True
        return True

    def alive(self, now_us: int) -> bool:
        return self.valid and now_us <= self.deadline_us

    def expire(self) -> None:
        self.valid = False


@dataclass
class HeadController:
    heartbeat_timeout_us: int
    boot_challenge: bytes = field(default_factory=lambda: token_bytes(16))
    state: Motion = Motion.INHIBITED
    boot_uuid: bytes | None = None
    epoch: int = 0
    limits_acked: bool = False
    last_heartbeat_us: int | None = None
    motor_present: bool = False
    fault_latched: bool = False
    last_nonce: int | None = None
    arm_seq: int | None = None
    last_seq: int | None = None
    pending_goals: list[tuple[int, int]] = field(default_factory=list)

    def reset(self, reboot: bool = False) -> None:
        self.state = Motion.INHIBITED
        self.boot_uuid = None
        self.epoch = 0
        self.limits_acked = False
        self.last_heartbeat_us = None
        self.fault_latched = False
        self.arm_seq = None
        self.last_seq = None
        self.pending_goals.clear()
        if reboot:
            self.boot_challenge = token_bytes(16)
        # last_nonce survives a link reset; a new C2 challenge protects a cold boot.

    def new_session(self, boot_uuid: bytes, epoch: int, echoed_challenge: bytes) -> bool:
        if len(boot_uuid) != 16 or epoch <= 0 or echoed_challenge != self.boot_challenge:
            return False
        if boot_uuid == self.boot_uuid and epoch <= self.epoch:
            return False
        self.reset()
        self.boot_uuid, self.epoch = boot_uuid, epoch
        return True

    def _context(self, boot_uuid: bytes, epoch: int, seq: int) -> bool:
        return (boot_uuid == self.boot_uuid and epoch == self.epoch
                and (self.last_seq is None or seq > self.last_seq))

    def heartbeat(self, boot_uuid: bytes, epoch: int, seq: int, now_us: int) -> bool:
        if not self._context(boot_uuid, epoch, seq):
            return False
        self.last_seq, self.last_heartbeat_us = seq, now_us
        return True

    def set_limits(self, boot_uuid: bytes, epoch: int, seq: int, within_hard_limits: bool) -> bool:
        if not self._context(boot_uuid, epoch, seq) or not within_hard_limits:
            return False
        self.last_seq, self.limits_acked = seq, True
        return True

    def enable(self, boot_uuid: bytes, epoch: int, seq: int, nonce: int, now_us: int) -> bool:
        if (not self._context(boot_uuid, epoch, seq) or not self.limits_acked
                or not self.motor_present or self.fault_latched
                or self.last_heartbeat_us is None
                or now_us - self.last_heartbeat_us > self.heartbeat_timeout_us
                or nonce == self.last_nonce):
            return False
        self.last_seq, self.last_nonce, self.arm_seq = seq, nonce, seq
        self.state = Motion.ENABLED
        return True

    def goal(self, boot_uuid: bytes, epoch: int, seq: int, valid_until_us: int,
             now_master_us: int) -> bool:
        if (not self._context(boot_uuid, epoch, seq) or self.state != Motion.ENABLED
                or self.arm_seq is None or seq <= self.arm_seq
                or now_master_us > valid_until_us):
            return False
        self.last_seq = seq
        self.pending_goals[:] = [(seq, valid_until_us)]  # latest wins
        return True

    def execute(self, now_master_us: int) -> bool:
        if self.state != Motion.ENABLED or not self.pending_goals:
            return False
        _, expiry = self.pending_goals.pop()
        return now_master_us <= expiry

    def tick(self, now_us: int) -> None:
        if self.state == Motion.ENABLED and (self.last_heartbeat_us is None
                or now_us - self.last_heartbeat_us > self.heartbeat_timeout_us):
            self.inhibit(latch_fault=True)

    def inhibit(self, latch_fault: bool = False) -> None:
        if self.state == Motion.ENABLED:
            self.state = Motion.BRAKING
        else:
            self.state = Motion.INHIBITED
        self.pending_goals.clear()
        self.limits_acked = False
        self.arm_seq = None
        self.fault_latched |= latch_fault

    def brake_complete(self) -> None:
        self.state = Motion.INHIBITED

    def estop(self) -> None:
        self.motor_present = False
        self.inhibit(latch_fault=True)
        # The hardware gate has removed motor energy; do not wait for powered braking.
        self.state = Motion.INHIBITED

    def clear_fault(self) -> None:
        if self.state == Motion.INHIBITED:
            self.fault_latched = False


@dataclass(frozen=True)
class TimeSample:
    t1_master_us: int
    t2_local_us: int
    t3_local_us: int
    t4_master_us: int

    @property
    def round_trip_us(self) -> int:
        return (self.t4_master_us - self.t1_master_us) - (self.t3_local_us - self.t2_local_us)

    @property
    def local_minus_master_us(self) -> float:
        return ((self.t2_local_us - self.t1_master_us)
                + (self.t3_local_us - self.t4_master_us)) / 2


@dataclass
class TimeModel:
    offset_at_ref_us: float
    rate_ppb: float
    model_ref_local_us: int
    uncertainty_us: float
    valid: bool

    def to_master(self, local_us: int) -> float:
        if not self.valid:
            raise ValueError("time model not valid")
        offset = self.offset_at_ref_us + self.rate_ppb * (local_us - self.model_ref_local_us) / 1e9
        return local_us - offset


def fit_time_model(samples: list[TimeSample]) -> TimeModel:
    valid = [s for s in samples if s.round_trip_us >= 0]
    if len(valid) < 3:
        return TimeModel(0, 0, 0, float("inf"), False)
    minimum = min(s.round_trip_us for s in valid)
    keep = [s for s in valid if s.round_trip_us <= 2 * minimum]
    if len(keep) < 3:
        return TimeModel(0, 0, 0, float("inf"), False)
    xs = [(s.t2_local_us + s.t3_local_us) / 2 for s in keep]
    ys = [s.local_minus_master_us for s in keep]
    ref = int(sum(xs) / len(xs))
    x = [v - ref for v in xs]
    mean_x, mean_y = sum(x) / len(x), sum(ys) / len(ys)
    denom = sum((v - mean_x) ** 2 for v in x)
    slope = sum((xv - mean_x) * (yv - mean_y) for xv, yv in zip(x, ys)) / denom if denom else 0
    offset = mean_y - slope * mean_x
    residual = max(abs(y - (offset + slope * xv)) for xv, y in zip(x, ys))
    return TimeModel(offset, slope * 1e9, ref, minimum / 2 + residual, True)
