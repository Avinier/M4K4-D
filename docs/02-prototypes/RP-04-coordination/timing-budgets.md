# RP-04 software and perceptual timing budgets

| Field | Value |
|---|---|
| Status | Part 4 `E` placeholders `RP04-P4-REG-01`. Literature split `T-LEAD` / `T-BEAT` / `T-DEAD`. **Not G01.** Re-run when RP-01/RP-03 hand off `W` |
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

These are three different quantities. Do not register one number for all three. Citations: [`research/literature.md`](research/literature.md) §3.

| ID | Quantity | P-01 planning `E` | Literature class | Re-run when |
|---|---|---|---|---|
| `T-LEAD` | Face/light **before** head onset | 80–170 ms (`intuition.md`); motor band 80–150 | Eye→head lag ~150 ms reactive / ~30 ms predictive (Sidenmark 2019). **Not** AV fusion | Measured D1 + C2 |
| `T-BEAT` | Same-beat **tolerance** around intended coincidence | 150 ms after intended relation; tighten toward 80–100 ms for a hard transient | Flash+beep ~±40 ms; speech TBW ~200 ms; ITU detectability +45/−125 ms | G01; G03 on real clips |
| `T-DEAD` | Hang ceiling before `OX-DELAY` | **300 ms from that wait’s intended start** (`300_000` µs). Not stacked after `T-BEAT`. Not “300 ms past the 150 ms window” | Independent engineering overlay. Perception “still together” is `T-BEAT` | Virtual wait-language; then C2/C3 `W` |

Clocks do not share an origin by accident:

```text
wait's intended start
  |-- T-BEAT (150 ms): still the same beat if the other channel lands here
  |-------- T-DEAD (300 ms): if the named progress event has not arrived, OX-DELAY
```

The Phase A harness logs `OX-DELAY` when observed face→head skew exceeds `PHASE_WINDOW_US` (150 ms) on the delayed-head injection (`T-BEAT` screen). HYBRID progress waits use `deadline_us = T-DEAD` from the wait’s intended start.
| — | Composer jitter | tens of ms on Linux | — | Pi 5 load trace |
| — | Cancel / preempt propagation | < one cue duration; literature wrap ≲ 200–720 ms then new epoch | Chao / barge-in craft, not a face-lead | Virtual now; C2/C3 `W` later |
| — | ACK/NACK | link RTT | — | RP-02 G05 |
| — | Timebase uncertainty | must resolve `T-BEAT` or run is exploratory | Uncalibrated display/audio paths already 20–150+ ms | `timebase.md` |
| — | Progress stuck timeout | 2 s then degrade | — | spike constant |
| — | Head→base (large look) | later than `T-LEAD`; human torso lag ~300–550 ms | Sidenmark 2019; not a P-01 HOLD number | Phase C P-02 |

CPU/memory margin on Pi 5 2 GB: not measured. Harness is not a load claim. Audio by phrase shape, not forced sample simultaneity (speech TBW is wider and asymmetric). G01 stamps **witnessed** onset.

## 3. Adapter notes (not a freeze)

TIME needs commanded lead ≈ native latency (`T-LEAD` compensation). PROG needs progress that actually arrives. HYBRID uses time only on tagged cues (P-01 face/light lead).
