# RP-04 software and perceptual timing budgets

| Field | Value |
|---|---|
| Status | Part 4 `E` placeholders `RP04-P4-REG-01`. **Not G01.** Re-run when RP-01/RP-03 hand off `W` |
| Owner | Project builder |

RP-01/RP-03 own actuator speed and physical settle. This file owns software/perceptual budgets. Unknown is never zero.

## 1. Event classes (do not collapse)

| Stamp | Meaning | Not |
|---|---|---|
| Dispatch | Composer sent the cue | Onset |
| Receipt / accept | Executor validated | Onset |
| Local start | Trajectory tick 0 / render queued / audio device start | World onset |
| Source onset | Frame-flip callback, audio device callback, encoder/light sense at the source | Photons in the room / acoustic onset at the mic |
| Witnessed onset | External video or room mic vs lighting cue | Composer log |

Photon vs frame-flip, room sound vs callback, requested light `sync_ts` vs LED transition: **Part 6 / G01 measurement definitions.** Phase A virtual nodes emit **source onset** only.

## 2. Phase A `E` planning values (not pass thresholds)

| Quantity | P-01 planning `E` | Re-run when |
|---|---|---|
| Face/light lead of head | 80–170 ms class (`intuition.md`) | Measured D1 + C2 |
| Composer jitter | tens of ms on Linux | Pi 5 load trace |
| Phase window for “same beat” | 150 ms after intended relation | Observer pilot + G01 |
| Bounded wait before `OX-DELAY` | 300 ms past window | Part 5 default 300_000 µs |
| Cancel / preempt propagation | < one cue duration | Virtual now; C2/C3 `W` later |
| ACK/NACK | link RTT | RP-02 G05 |
| Timebase uncertainty | must resolve the window or run is exploratory | `timebase.md` |
| Progress stuck timeout | 2 s then degrade | spike constant |

CPU/memory margin on Pi 5 2 GB: not measured. Harness is not a load claim.

## 3. Adapter notes (not a freeze)

TIME needs commanded lead ≈ native latency. PROG needs progress that actually arrives. HYBRID uses time only on tagged cues (P-01 face/light lead).
