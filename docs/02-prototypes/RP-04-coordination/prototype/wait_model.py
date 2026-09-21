"""Bounded wait language for HYBRID scores. TIME ignores waits; PROG uses satisfaction only."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

WaitMode = Literal["event", "any", "all"]
WaitOutcome = Literal["degrade", "deny", "abort"]

KNOWN_EVENT_KINDS = frozenset(
    {
        "source_onset",
        "accept",
        "complete",
        "eligible",
        "progress",
        "target_decision",
        "deny",
    }
)
ILLEGAL_WAIT_KINDS = frozenset({"dispatch", "receipt", "local_start", "witnessed_onset"})
KNOWN_CHANNELS = frozenset({"face", "light", "audio", "head", "base", "perception", "core"})
T_DEAD_US = 300_000


@dataclass(frozen=True)
class WaitEvent:
    channel: str
    kind: str
    cue_id: str | None = None
    threshold: str | None = None
    epoch: str | None = None

    def matches(self, event_kind: str, channel: str, cue_id: str, reason: str, epoch: int, current_epoch: int) -> bool:
        if epoch != current_epoch:
            return False
        if event_kind != self.kind or channel != self.channel:
            return False
        if self.cue_id is not None and cue_id != self.cue_id:
            return False
        if self.kind == "progress":
            return bool(self.threshold) and reason == self.threshold
        return True


@dataclass(frozen=True)
class Wait:
    mode: WaitMode
    events: tuple[WaitEvent, ...]
    deadline_us: int | None = None
    on_deadline: WaitOutcome | None = None
    arm_at_us: int = 0

    def __post_init__(self) -> None:
        if not self.events:
            raise ValueError("wait must name at least one event")
        if self.mode == "event" and len(self.events) != 1:
            raise ValueError("mode=event requires exactly one event")
        if self.mode in ("any", "all") and len(self.events) < 2:
            raise ValueError(f"mode={self.mode} requires at least two events")


@dataclass(frozen=True)
class Cue:
    cue_id: str
    channel: str
    panel: str
    trigger: Literal["time", "progress"]
    start_at: int
    wait: Wait | None = None
    condition: str | None = None
    fallback: str | None = None
    primitive: str | None = None


class LogLike:
    kind: str
    channel: str
    cue_id: str
    reason: str
    epoch: int


def event_satisfied(spec: WaitEvent, log: Sequence[LogLike], current_epoch: int) -> bool:
    return any(
        spec.matches(e.kind, e.channel, e.cue_id, e.reason, e.epoch, current_epoch)
        for e in log
    )


def event_impossible(spec: WaitEvent, unavailable: Iterable[str], log: Sequence[LogLike], current_epoch: int) -> bool:
    if spec.channel in unavailable:
        return True
    return any(
        e.kind == "deny" and e.channel == spec.channel and e.epoch == current_epoch
        and (spec.cue_id is None or e.cue_id == spec.cue_id)
        for e in log
    )


def wait_satisfied(wait: Wait, log: Sequence[LogLike], current_epoch: int) -> bool:
    hits = [event_satisfied(spec, log, current_epoch) for spec in wait.events]
    if wait.mode == "all":
        return all(hits)
    return any(hits)


def wait_impossible(wait: Wait, log: Sequence[LogLike], unavailable: Iterable[str], current_epoch: int) -> bool:
    flags = [event_impossible(spec, unavailable, log, current_epoch) for spec in wait.events]
    if wait.mode == "all":
        return any(flags) and not wait_satisfied(wait, log, current_epoch)
    return all(flags) and not wait_satisfied(wait, log, current_epoch)


def wait_outcome(
    wait: Wait | None,
    *,
    log: Sequence[LogLike],
    unavailable: Iterable[str],
    current_epoch: int,
    now_us: int,
    apply_deadline: bool,
) -> Literal["ready", "waiting", "degrade", "deny", "abort"]:
    if wait is None:
        return "ready"
    if wait_satisfied(wait, log, current_epoch):
        return "ready"
    if apply_deadline and wait_impossible(wait, log, unavailable, current_epoch):
        return wait.on_deadline or "deny"
    if apply_deadline and wait.deadline_us is not None and now_us >= wait.arm_at_us + wait.deadline_us:
        return wait.on_deadline or "deny"
    return "waiting"
