# RP-04 shared runtime architecture

| Field | Value |
|---|---|
| Status | Part 4 design-definition `RP04-P4-REG-01`. Trigger **`CS-HYBRID`** after `RP04-P5-REG-01`. Not firmware |
| Owner | Project builder |
| Consumes | `CA-01…16`; [`situations.md`](situations.md) §11; [`research/trigger-comparison.md`](research/trigger-comparison.md); [`research/literature.md`](research/literature.md); remaining: [`research/experiment-spec.md`](research/experiment-spec.md) |

This document is the **shared** layer. `CS-TIME` / `CS-PROG` / `CS-HYBRID` are adapters on top. C2/C3 remain legality and stop authority.

## 1. Ownership

| Node / service | May | Must not |
|---|---|---|
| `makad-core` | Allocate `perf_id`/`perf_epoch`; pick score; arbitrate `OX-PREEMPT`; flush epoch; compose cues | Stream PWM; overrule inhibit; invent MCU legality |
| `makad-hwd` | Frame, queue (latest-wins), session, evidence | Invent the next beat; renew lease without core progress |
| `makad-audio` | Play/stop with cue identity; callback onset | Command motion |
| `makad-perception` | Propose target / uncertainty | Dispatch C2/C3 |
| `makad-edge` | Propose app/cloud intent | Dispatch motion |
| C2 | Head trajectory, limits, expiry, D1 relay, light; NACK stale/illegal | Choose the next semantic performance |
| C3 | Wheels, HOLD, inhibit, hazards | Follow or spin because the score is pretty |
| D1 | Frame flip, idle on expiry | Motion or behaviour |

## 2. Action lifecycle (shared)

Every cue:

`dispatch → receipt → accept|deny → local_start → source_onset → progress → complete|abort`

`dispatch` is not onset. `source_onset` is not witnessed photons/sound (Part 6).

Cancellation: core flushes epoch; hwd drops that epoch’s queue; executors abort **current** cue of that epoch and reject later ones (`OX-STALE`).

## 3. Arbitration (`OX-PREEMPT` §8.1)

`makad-core` only. Perception/edge propose. On P-02 during P-01 search: flush N, stop audio, C2 preempt `HM-04`, D1 must not log search success, C3 HOLD, epoch N+1 starts at `P02-C01` gaze.

## 4. Recovery

| Overlay | Shared behaviour |
|---|---|
| `OX-TIME` | Do not execute scheduled work. Distinguishable NACK. Progress-triggered work may continue. No G01 |
| `OX-RESTART` | New session. Old epoch **must not resume**. Inhibit / face idle. Fresh arm + new intent (`CA-13`) |
| `OX-SAFETY` | C2/C3 (and gate) stop first. Core flush is best-effort. Not an authored `HM-18` flourish |

## 5. Trigger adapters

Part 5 selected **`CS-HYBRID`** for the virtual composer: each cue names `time` or `progress`. Progress waits use the bounded language in `prototype/wait_model.py` (`event` / `any` / `all`, named thresholds, `T-DEAD` outcomes degrade/deny/abort). `CS-TIME` / `CS-PROG` remain in [`prototype/EXPERIMENTAL.md`](prototype/EXPERIMENTAL.md). Physical time tags use `start_at_us` from `RP02-P4-REG-03`; exploratory packed layout revision 2 lives in RP-02 `phase-a/` and is not a G04/G05 registration.

## 6. Logging

Join by `perf_epoch` + `cue_id` + channel, not by clock proximity. Bounded ring (`CA-16`).
