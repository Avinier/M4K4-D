# RP-04 trigger comparison (closed)

| Field | Value |
|---|---|
| Status | **Closed 2026-09-21.** `RP04-P3-REG-01` shortlist; `RP04-P5-REG-01` selected `CS-HYBRID` (virtual). Literature pass **confirms**. TIME/PROG retained as evidence. Not ADR-05 |
| Owner | Project builder |
| Bound | `BD-07` |
| Literature | [`literature.md`](literature.md) — Exa redo 2026-09-21 |
| Remaining work | [`experiment-spec.md`](experiment-spec.md) — empirical HYBRID validation, not a new family |

This file is the architecture-family result. Do not reopen TIME vs PROG vs HYBRID unless a falsifier in `experiment-spec.md` fires. Do not add middleware, ROS, or a graph-as-trigger spike.

`CA-07` already excludes ROS 2 / micro-ROS from the V1 safety path. Adjacent practice names mechanisms, not products. The first close had no cited survey; the Exa pass filled that. **It did not change the winner.**

## 1. Decision axes (not alternatives)

| Axis | Choice for Phase A | Shared vs compared |
|---|---|---|
| Score representation | **Versioned cue list** with optional per-cue trigger tag. Graph/statechart is **not** a competing trigger; it remains an open representation option if a cue list cannot express P-02 hand-off later | Representation axis. Not spiked as `CS-GRAPH` |
| Trigger mechanism | Compared: scheduled time vs progress/event vs **bounded** per-cue choice | Compared. **Winner: HYBRID (virtual)** |
| Action lifecycle | Goal → accept/deny → start → feedback → succeed/abort/expire | **Shared** |
| Supervision | `makad-core` arbitrates intent; C2/C3 legally refuse and stop; lease loss kills the epoch (`CA-01/09/11`) | **Shared** |

A supervisory graph used with either trigger would make “hybrid wins” a tautology. **Do not spike a graph as a third trigger.**

## 2. Trigger adapters

| ID | Binding | What the adapter does |
|---|---|---|
| `CS-TIME` | Shared runtime + scheduled-time edges | Dispatch at `start_at − lead`. `start_at_us` is now ICD semantics (`RP02-P4-REG-03`); packed layout still open |
| `CS-PROG` | Shared runtime + progress/event edges | Next cue on named `source_onset` / `progress` / `complete` |
| `CS-HYBRID` | Shared runtime + **explicit per-cue** trigger (`time` **or** `progress`) | P-01: C02 time-lead for face/light/audio; C03/C04 progress-chained to head |

`CS-HYBRID` is not an unbounded event graph. Each cue names exactly one trigger kind.

## 3. Predeclared selection rule (already applied)

Recorded so Part 5 could not invent a prettier rule after seeing logs.

1. Every candidate **must** pass shared invariants: epoch flush, no claimed onset on deny, P-01 base HOLD, replay, stale reject, preempt epoch cut.
2. Then compare **identical** P-01 injections: delay (`OX-DELAY`), invalid/late time (`OX-TIME`), stuck progress, restart/no-resume (`OX-RESTART`), interruption (`OX-CANCEL` / `OX-PREEMPT`), required contract changes, traceability, implementation complexity.
3. Select only after those injections.
4. **Demo smoothness is not a criterion.**
5. Missing `start_at_us` on the wire **penalized physical TIME** at selection time. `RP02-P4-REG-03` later accepted the semantic. That does not unwind the virtual result. `OX-TIME` still wipes TIME-only scores.

## 4. Paper matrix and spike result (P-01)

| Situation | `CS-TIME` | `CS-PROG` | `CS-HYBRID` |
|---|---|---|---|
| Happy P-01 HOLD | Aligns if leads are right; Linux jitter is the risk | Robust to latency; slow head delays audio/face follow-through | Face/light can still lead; head chains on progress |
| `OX-DELAY` late head | Later time cues still fire → likely desync | Waits → character stays together, may feel slow | Head-chained cues wait; time-tagged cues do not |
| `OX-TIME` invalid/late | Scheduled cues **must** NACK; empty performance unless fallback | Unaffected | Time-tagged cues NACK; progress cues continue |
| Stuck progress | Continues on the clock | **Hangs** until timeout/degrade | Only progress-tagged cues hang |
| `OX-PREEMPT` | Flush + new schedule | Flush + new first event | Same shared supervisor |
| `OX-RESTART` | Shared: no resume | Shared | Shared |
| `start_at_us` | Needed for physical TIME tags | Not required | Needed only for time-tagged cues |
| Spike cost | One dispatch clock | One wait table | Cue tag + both paths |

Nine tests in `prototype/test_p01_spikes.py` **pass**. Discriminating: invalid time NACKs TIME and HYBRID time-tags, not PROG; stuck head progress blocks PROG/HYBRID `P01-C04`, not TIME; restart does not resume epoch 1.

**Selected `CS-HYBRID`** for the live virtual composer: P-01 needs an authored face/light lead (time) and a head chain (progress). PROG cannot express the lead without becoming HYBRID. TIME still wipes the score on `OX-TIME`. TIME/PROG stay in `prototype/` (`EXPERIMENTAL.md`).

## 5. Literature grounding (Exa 2026-09-21)

Detail and citations: [`literature.md`](literature.md). Compact:

| Claim | Adjacent evidence | Consequence |
|---|---|---|
| Three trigger kinds, not one clock | QLab mixes GO, timecode, auto-follow, auto-continue on one list. MSC GO vs TIMED_GO. Unity/Unreal time keys vs notifies. BML planning + event sync | **Supports the selected taxonomy.** Makad’s rule: each cue names exactly one kind. Do not claim those tools *are* `CS-HYBRID` |
| TIME cannot certify physical completion | QLab: “you don't necessarily know the amount of time that will elapse between cues.” Clock drop → freewheel 0–2 s then stop/pause/keep | `OX-TIME` still wipes time-tagged cues |
| PROG hangs on a missing event | QLab auto-follow waits for complete; ABL/Quadrant wait-forever without a deadline | Deadline is part of HYBRID, not a new family |
| Cue list is the score | Lighting/QLab/Timeline/Vector clips | Graph only if P-02 *discrete* hand-off needs score mutation |
| Counter-yaw is not a trigger | Disney body-yaw ↔ inverse head yaw; Haru VOM; Unity blend parameters | Executor primitive. `BD-08` must name owner and yaw source before implementation. A graph cannot fix a slow C0 loop |

Lifecycle and supervision stay shared: Chao start/keep/stop; ROS 2 action states as **names only**; Jibo same-layer reject; panic then second-panic hard stop.

## 6. Non-goals (still)

No middleware catalogue. No ROS. No treating lifecycle/supervision as competing products. No ADR-05 from this file.
