"""Declarative P-01 / P-02 cue lists and score-definition checks. Not G01."""
from __future__ import annotations

from wait_model import (
    ILLEGAL_WAIT_KINDS,
    KNOWN_CHANNELS,
    KNOWN_EVENT_KINDS,
    T_DEAD_US,
    Cue,
    Wait,
    WaitEvent,
)

FACE_LEAD_US = 100_000
HEAD_SCHEDULE_US = 250_000
SEARCH_SCHEDULE_US = 800_000

PROGRESS_THRESHOLDS = frozenset({"HM-03.rise_commit", "HM-10.curious_hold", "HM-05.lock", "BM-05.yaw_commit"})


def _evt(channel: str, kind: str, cue_id: str | None = None, threshold: str | None = None) -> WaitEvent:
    return WaitEvent(channel, kind, cue_id, threshold)


def _any(*events: WaitEvent, arm: int, outcome: str, fallback_deadline: int = T_DEAD_US) -> Wait:
    return Wait("any", events, deadline_us=fallback_deadline, on_deadline=outcome, arm_at_us=arm)  # type: ignore[arg-type]


def _all(*events: WaitEvent, arm: int, outcome: str, fallback_deadline: int = T_DEAD_US) -> Wait:
    return Wait("all", events, deadline_us=fallback_deadline, on_deadline=outcome, arm_at_us=arm)  # type: ignore[arg-type]


def _one(event: WaitEvent, arm: int, outcome: str, fallback_deadline: int = T_DEAD_US) -> Wait:
    return Wait("event", (event,), deadline_us=fallback_deadline, on_deadline=outcome, arm_at_us=arm)  # type: ignore[arg-type]


P01: tuple[Cue, ...] = (
    Cue("P01-C02", "face", "E-open", "time", FACE_LEAD_US, fallback="OX-DENY(face)"),
    Cue("P01-C02", "light", "wake", "time", FACE_LEAD_US, fallback="OX-DENY(light)"),
    Cue("P01-C02", "audio", "A-wake-rise", "time", FACE_LEAD_US, fallback="OX-DENY(audio)"),
    Cue(
        "P01-C03",
        "head",
        "HM-03",
        "progress",
        HEAD_SCHEDULE_US,
        wait=_any(
            _evt("face", "source_onset"),
            _evt("light", "source_onset"),
            arm=FACE_LEAD_US,
            outcome="degrade",
        ),
        fallback="OX-DELAY",
    ),
    Cue(
        "P01-C04",
        "head",
        "HM-04",
        "progress",
        SEARCH_SCHEDULE_US,
        wait=_all(
            _evt("head", "progress", "P01-C03", "HM-03.rise_commit"),
            _evt("perception", "target_decision"),
            arm=HEAD_SCHEDULE_US,
            outcome="deny",
        ),
        condition="no_target",
        fallback="OX-DENY(head)",
    ),
    Cue(
        "P01-C04",
        "head",
        "HM-05",
        "progress",
        SEARCH_SCHEDULE_US,
        wait=_all(
            _evt("head", "progress", "P01-C03", "HM-03.rise_commit"),
            _evt("perception", "target_decision", threshold=None),
            arm=HEAD_SCHEDULE_US,
            outcome="deny",
        ),
        condition="target",
        fallback="OX-DENY(head)",
    ),
    Cue(
        "P01-C05",
        "head",
        "HOLD",
        "progress",
        SEARCH_SCHEDULE_US + 400_000,
        wait=_one(_evt("head", "complete", "P01-C04"), arm=SEARCH_SCHEDULE_US, outcome="abort"),
        fallback="HM-18",
    ),
)

P02_IN_SECTOR: tuple[Cue, ...] = (
    Cue("P02-C01", "face", "E-gaze", "time", 0, fallback="OX-DENY(face)", condition="in_sector"),
    Cue("P02-C01", "light", "attentive", "time", 0, fallback="OX-DENY(light)", condition="in_sector"),
    Cue("P02-C01", "audio", "A-query-rise", "progress", 0,
        wait=_one(_evt("face", "source_onset"), arm=0, outcome="degrade"),
        fallback="OX-DENY(audio)", condition="in_sector"),
    Cue("P02-C01", "base", "BM-01", "time", 0, fallback="OX-INHIBIT-BASE", condition="in_sector"),
    Cue("P02-C02", "head", "HM-10", "progress", 0,
        wait=_one(_evt("face", "source_onset"), arm=0, outcome="degrade"),
        fallback="HM-18", condition="in_sector"),
    Cue("P02-C03", "face", "E-think", "progress", 0,
        wait=_one(_evt("head", "progress", "P02-C02", "HM-10.curious_hold"), arm=0, outcome="degrade"),
        fallback="OX-DENY(face)", condition="in_sector"),
    Cue("P02-C03", "head", "HOLD", "progress", 0,
        wait=_one(_evt("head", "complete", "P02-C02"), arm=0, outcome="abort"),
        fallback="HM-18", condition="in_sector"),
    Cue("P02-C04", "face", "E-gaze", "progress", 0,
        wait=_one(_evt("head", "complete", "P02-C03"), arm=0, outcome="degrade"),
        fallback="OX-DENY(face)", condition="in_sector"),
    Cue("P02-C04", "audio", "SILENCE", "progress", 0,
        wait=_one(_evt("audio", "complete", "P02-C01"), arm=0, outcome="degrade"),
        fallback="AudioStop", condition="in_sector"),
    Cue("P02-C04", "base", "BM-01", "progress", 0,
        wait=_one(_evt("head", "complete", "P02-C03"), arm=0, outcome="abort"),
        fallback="BM-01", condition="in_sector"),
)

P02_BEHIND_BODY: tuple[Cue, ...] = (
    Cue("P02-C01", "face", "E-gaze", "time", 0, fallback="OX-DENY(face)", condition="behind_body"),
    Cue("P02-C01", "light", "attentive", "time", 0, fallback="OX-DENY(light)", condition="behind_body"),
    Cue("P02-C01", "audio", "A-query-rise", "progress", 0,
        wait=_one(_evt("face", "source_onset"), arm=0, outcome="degrade"),
        fallback="OX-DENY(audio)", condition="behind_body"),
    Cue("P02-C02", "head", "HM-10", "progress", 0,
        wait=_one(_evt("face", "source_onset"), arm=0, outcome="degrade"),
        fallback="HM-18", condition="behind_body"),
    Cue(
        "P02-C03",
        "base",
        "BM-05",
        "progress",
        0,
        wait=_all(
            _evt("base", "eligible"),
            _evt("core", "target_decision"),
            arm=0,
            outcome="deny",
        ),
        fallback="OX-DENY(base)",
        condition="behind_body",
    ),
    Cue(
        "P02-C03",
        "head",
        "counter_yaw",
        "progress",
        0,
        wait=_all(
            _evt("base", "accept", "P02-C03"),
            _evt("base", "eligible"),
            arm=0,
            outcome="deny",
        ),
        fallback="HM-18",
        primitive="counter_yaw",
        condition="behind_body",
    ),
    Cue("P02-C04", "head", "HM-10", "progress", 0,
        wait=_one(_evt("base", "complete", "P02-C03"), arm=0, outcome="degrade"),
        fallback="HM-18", condition="behind_body"),
    Cue("P02-C04", "base", "BM-01", "progress", 0,
        wait=_one(_evt("base", "complete", "P02-C03"), arm=0, outcome="abort"),
        fallback="BM-12", condition="behind_body"),
    Cue("P02-C04", "face", "E-gaze", "progress", 0,
        wait=_one(_evt("base", "complete", "P02-C03"), arm=0, outcome="degrade"),
        fallback="OX-DENY(face)", condition="behind_body"),
    Cue("P02-C04", "audio", "SILENCE", "progress", 0,
        wait=_one(_evt("audio", "complete", "P02-C01"), arm=0, outcome="degrade"),
        fallback="AudioStop", condition="behind_body"),
)


def _perf_prefix(name: str) -> str:
    return name.split("-")[0]


def validate_score(name: str, cues: tuple[Cue, ...]) -> list[str]:
    errors: list[str] = []
    prefix = _perf_prefix(name.replace("_", "-"))
    seen: set[tuple[str, str, str | None]] = set()
    if not any(c.fallback for c in cues):
        errors.append("absent fallback behavior")
    for cue in cues:
        key = (cue.cue_id, cue.channel, cue.condition)
        if key in seen:
            errors.append(f"duplicate cue identity {key}")
        seen.add(key)
        if not cue.cue_id.startswith(prefix) and not cue.cue_id.startswith(name.split("_")[0]):
            pass
        if cue.channel not in KNOWN_CHANNELS:
            errors.append(f"unknown channel {cue.channel}")
        if cue.wait is None:
            continue
        if cue.fallback is None:
            errors.append(f"{cue.cue_id}/{cue.channel}: absent fallback behavior")
        external = False
        for spec in cue.wait.events:
            if spec.kind in ILLEGAL_WAIT_KINDS:
                errors.append(f"{cue.cue_id}: wait on {spec.kind} is not source onset")
            if spec.kind not in KNOWN_EVENT_KINDS:
                errors.append(f"{cue.cue_id}: unknown event name {spec.kind}")
            if spec.channel not in KNOWN_CHANNELS:
                errors.append(f"{cue.cue_id}: unknown channel {spec.channel}")
            if spec.kind == "progress" and not spec.threshold:
                errors.append(f"{cue.cue_id}: unqualified progress")
            if spec.kind == "progress" and spec.threshold and spec.threshold not in PROGRESS_THRESHOLDS:
                errors.append(f"{cue.cue_id}: unknown progress threshold {spec.threshold}")
            if spec.epoch not in (None, "current"):
                errors.append(f"{cue.cue_id}: illegal cross-epoch dependency {spec.epoch}")
            if spec.cue_id and not spec.cue_id.startswith(prefix) and spec.channel != "perception":
                other = spec.cue_id.split("-")[0]
                if other != prefix:
                    errors.append(f"{cue.cue_id}: illegal cross-epoch dependency on {spec.cue_id}")
            if spec.channel != cue.channel:
                external = True
        if external and cue.wait.deadline_us is None:
            errors.append(f"{cue.cue_id}/{cue.channel}: missing deadline on external wait")
        if external and cue.wait.on_deadline is None:
            errors.append(f"{cue.cue_id}/{cue.channel}: absent fallback behavior")
    if name.startswith("P02") or name.startswith("P-02"):
        if not any(c.primitive == "counter_yaw" for c in cues) and "behind" in name.lower():
            errors.append("behind-body score missing named counter_yaw primitive")
    return errors
