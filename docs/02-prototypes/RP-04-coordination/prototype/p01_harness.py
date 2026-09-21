"""Phase A virtual P-01 composer. Not G01/G03. Not UART/ROS.

TIME and PROG adapters are frozen evidence. Live maintenance is HYBRID only:
bounded any/all/threshold waits with deadlines. Dispatch/receipt are never onset.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from score import FACE_LEAD_US, P01
from wait_model import Cue, wait_outcome

Adapter = Literal["TIME", "PROG", "HYBRID"]
Trigger = Literal["time", "progress"]

PHASE_WINDOW_US = 150_000
STEP_US = 10_000
PROGRESS_REASON = {
    "P01-C03": "HM-03.rise_commit",
    "P02-C02": "HM-10.curious_hold",
}


@dataclass
class Event:
    t: int
    kind: str
    channel: str
    epoch: int
    cue_id: str
    reason: str = ""


@dataclass
class Node:
    delay_us: int = 20_000
    deny: bool = False
    stuck: bool = False
    dead: bool = False
    epoch: int = 0
    onset_at: dict[str, int] = field(default_factory=dict)
    progress_at: dict[str, int] = field(default_factory=dict)
    complete_at: dict[str, int] = field(default_factory=dict)

    def restart(self) -> None:
        self.dead = True
        self.onset_at.clear()
        self.progress_at.clear()
        self.complete_at.clear()

    def accept(self, epoch: int, cue_id: str, t: int) -> str:
        if self.dead:
            return "dead"
        if epoch < self.epoch:
            return "stale_epoch"
        if self.deny:
            return "denied"
        self.epoch = epoch
        if self.stuck:
            return "accepted_stuck"
        self.onset_at[cue_id] = t + self.delay_us
        self.progress_at[cue_id] = t + self.delay_us + 50_000
        self.complete_at[cue_id] = t + self.delay_us + 200_000
        return "accepted"


class Sim:
    def __init__(self, adapter: Adapter, inject: str = "happy") -> None:
        self.adapter = adapter
        self.inject = inject
        self.t = 0
        self.epoch = 1
        self.log: list[Event] = []
        self.time_ok = inject != "time_invalid"
        self.nodes = {
            "face": Node(20_000, deny=inject in ("deny_face", "deny_visible")),
            "light": Node(10_000, deny=inject in ("deny_light", "deny_visible")),
            "audio": Node(10_000),
            "head": Node(80_000, stuck=inject == "stuck_progress"),
            "base": Node(0),
        }
        if inject == "cancel_wait":
            self.nodes["face"].delay_us = 2_000_000
            self.nodes["light"].delay_us = 2_000_000
        if inject == "delay_head":
            self.nodes["head"].delay_us = 500_000
        self.dispatched: set[tuple[int, str, str, str | None]] = set()
        self.flushed = False
        self.preempted = False
        self.base_motion = False
        self.p02_gaze = False
        self.search_success = False
        self.injected = False
        self.decision_emitted = False
        self.unavailable: set[str] = set()
        self._wait_branch: dict[tuple[int, str, str, str | None], str] = {}

    def emit(self, kind: str, channel: str, cue_id: str, reason: str = "", epoch: int | None = None) -> None:
        self.log.append(Event(self.t, kind, channel, self.epoch if epoch is None else epoch, cue_id, reason))

    def trig(self, cue: Cue) -> Trigger:
        if self.adapter == "TIME":
            return "time"
        if self.adapter == "PROG":
            return "progress"
        return cue.trigger

    def flush(self, reason: str) -> None:
        old = self.epoch
        self.emit("epoch_flush", "core", "", reason)
        self.epoch = old + 1
        for n in self.nodes.values():
            n.epoch = self.epoch
        self.flushed = True

    def target_reason(self) -> str | None:
        for e in reversed(self.log):
            if e.kind == "target_decision" and e.epoch == self.epoch:
                return e.reason
        return None

    def cue_allowed(self, cue: Cue) -> bool:
        if cue.condition in (None, "in_sector", "behind_body"):
            return True
        if cue.condition in ("target", "no_target"):
            decision = self.target_reason() or "no_target"
            return cue.condition == decision
        return True

    def ready(self, cue: Cue) -> bool:
        key = (self.epoch, cue.cue_id, cue.channel, cue.condition)
        if key in self.dispatched or self.flushed or not self.cue_allowed(cue):
            return False
        trig = self.trig(cue)
        if trig == "time":
            if not self.time_ok:
                return self.t >= min(cue.start_at, FACE_LEAD_US)
            return self.t >= cue.start_at
        outcome = wait_outcome(
            cue.wait,
            log=self.log,
            unavailable=self.unavailable,
            current_epoch=self.epoch,
            now_us=self.t,
            apply_deadline=self.adapter == "HYBRID",
        )
        if outcome == "ready":
            return True
        if outcome == "waiting":
            return False
        self._wait_branch[key] = outcome
        return True

    def dispatch_cue(self, cue: Cue) -> None:
        key = (self.epoch, cue.cue_id, cue.channel, cue.condition)
        deadline_out = self._wait_branch.pop(key, None)
        if deadline_out in ("deny", "abort"):
            self.emit(deadline_out, cue.channel, cue.cue_id, "OX-DELAY")
            self.dispatched.add(key)
            return
        if deadline_out == "degrade":
            self.emit("delay", cue.channel, cue.cue_id, "OX-DELAY")
        if self.trig(cue) == "time" and not self.time_ok:
            self.emit("deny", cue.channel, cue.cue_id, "time_model_invalid")
            self.dispatched.add(key)
            return
        self.emit("dispatch", cue.channel, cue.cue_id)
        result = self.nodes[cue.channel].accept(self.epoch, cue.cue_id, self.t)
        self.emit("receipt", cue.channel, cue.cue_id)
        if result == "accepted":
            self.emit("accept", cue.channel, cue.cue_id)
        elif result == "accepted_stuck":
            self.emit("accept", cue.channel, cue.cue_id, "stuck")
        else:
            self.emit("deny", cue.channel, cue.cue_id, result)
            self.unavailable.add(cue.channel)
        self.dispatched.add(key)
        if cue.channel == "base" and cue.panel not in ("HOLD", "BM-01", "BM-13"):
            self.base_motion = True
        if cue.panel == "HM-05":
            self.search_success = True

    def tick_onsets(self) -> None:
        for name, node in self.nodes.items():
            if node.stuck or node.dead:
                continue
            for cid, ot in list(node.onset_at.items()):
                if ot == self.t:
                    self.emit("source_onset", name, cid)
            for cid, pt in list(node.progress_at.items()):
                if pt == self.t:
                    self.emit("progress", name, cid, PROGRESS_REASON.get(cid, ""))
            for cid, ct in list(node.complete_at.items()):
                if ct == self.t:
                    self.emit("complete", name, cid)

    def maybe_perception(self) -> None:
        if self.decision_emitted or self.flushed:
            return
        if not any(e.kind == "progress" and e.reason == "HM-03.rise_commit" and e.epoch == self.epoch for e in self.log):
            return
        reason = "target" if self.inject == "target" else "no_target"
        self.emit("target_decision", "perception", "P01-C04", reason)
        self.decision_emitted = True

    def maybe_inject(self) -> None:
        if self.injected:
            return
        if self.inject == "cancel" and self.t == 400_000:
            self.flush("OX-CANCEL")
            self.injected = True
        elif self.inject == "cancel_wait" and self.t == 200_000:
            self.flush("OX-CANCEL")
            self.injected = True
        elif self.inject == "preempt" and self.t == 1_000_000:
            self.flush("OX-PREEMPT")
            self.emit("dispatch", "face", "P02-C01")
            r = self.nodes["face"].accept(self.epoch, "P02-C01", self.t)
            self.emit("receipt", "face", "P02-C01")
            if r == "accepted":
                self.emit("accept", "face", "P02-C01")
            self.p02_gaze = True
            self.preempted = True
            self.injected = True
        elif self.inject == "restart" and self.t == 400_000:
            self.nodes["head"].restart()
            self.emit("restart", "head", "", "OX-RESTART")
            self.flush("OX-RESTART")
            self.injected = True
        elif self.inject == "stale" and self.t == 500_000:
            old = self.epoch
            self.flush("OX-CANCEL")
            result = self.nodes["head"].accept(old, "P01-C04", self.t)
            self.emit("deny", "head", "P01-C04", result)
            self.injected = True

    def run(self, until: int = 3_000_000) -> list[Event]:
        self.emit("intent_accept", "core", "P01-C01")
        self.emit("accept", "base", "HOLD")
        while self.t <= until:
            self.maybe_inject()
            self.tick_onsets()
            self.maybe_perception()
            if not self.flushed:
                for cue in P01:
                    if self.ready(cue):
                        self.dispatch_cue(cue)
            if self.inject == "delay_head" and not any(e.kind == "delay" for e in self.log):
                faces = [e.t for e in self.log if e.kind == "source_onset" and e.channel == "face"]
                heads = [e.t for e in self.log if e.kind == "source_onset" and e.channel == "head"]
                if faces and heads and heads[0] - faces[0] > PHASE_WINDOW_US:
                    self.emit("delay", "head", "P01-C03", "OX-DELAY")
            self.t += STEP_US
        return self.log


def kinds(log: list[Event], kind: str, channel: str | None = None) -> list[Event]:
    return [e for e in log if e.kind == kind and (channel is None or e.channel == channel)]


def replay_ok(adapter: Adapter, inject: str = "happy") -> bool:
    sig = lambda s: [(e.kind, e.channel, e.cue_id, e.reason, e.epoch) for e in s]
    return sig(Sim(adapter, inject).run()) == sig(Sim(adapter, inject).run())
