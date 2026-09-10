# Makad Monotonic Timebase and Synchronization Strategy

| Field | Value |
|---|---|
| Status | **Strategy documented; not implemented; not validated.** Validation is RP02-G05; RP-01's first scored run depends on it |
| Version | 0.1 |
| Owner | Project builder |
| Created | 2026-09-08 |
| Governed by | `risk-prototype-plan.md` v1.10 §"Continuous sourcing and data workstream" (monotonic event-time strategy deliverable) and §"Open inputs before RP-01 scored testing" |
| Grounding | `control-topology-options.md` v0.9 §5 (one master, timestamp-at-source, serial offset reconciliation; PTP overkill, NTP too coarse) |
| Consumes | `docs/02-prototypes/RP-02-electrical/link-contract.md` §4.4 `TIME_SYNC`; `run-record-convention.md` |
| Feeds | Every scored run's timestamps; RP-02 G05; RP-04 coordination; `subsystem-interfaces.md`; ADR-12 |

The moment there is more than one controller there is more than one clock. Independent oscillators drift at tens of ppm — a C2 crystal at 20 ppm is 1.2 ms per minute — so "the same instant" means something different on each board. AD-01 ("one character") and AD-11 ("diagnosable") both fail on unreconciled clocks: coordination looks laggy for reasons no one can find, and a combined-reversal analysis cannot say which axis moved first. This document fixes the method so that every RP-01…RP-07 timestamp is comparable.

## 1. Principles

1. **Monotonic, never wall-clock.** Every event timestamp is a monotonic counter in microseconds. Wall-clock (UTC) is recorded **once per run** in `run.md` for the run ID and for human correlation; it never appears inside event data. A wall-clock step (NTP, `date -s`) must have zero effect on any timestamp (`fault-matrix.md` F-15).
2. **Timestamp at the source.** A measurement is stamped where it is captured — the encoder read on C2, the frame capture on the SBC, the audio buffer callback — not when it arrives at the logger. Receipt time may be recorded *additionally* where latency itself is the quantity.
3. **One master; everyone else converts.** The master's monotonic clock is *the* timeline. Each MCU keeps its own free-running microsecond timer and converts to master time using a reconciled offset and rate. Raw local stamps are logged alongside converted ones so a bad reconciliation can be redone offline.
4. **Uncertainty is a logged quantity.** Every run records the achieved offset uncertainty; a scored gate whose threshold is finer than that uncertainty is not scorable (`workbench.md` item 6).
5. **The method must work with the tools in `workbench.md`**: a UART link, a logic analyzer, no PTP hardware.

## 2. Which node is master

**The body SBC's `CLOCK_MONOTONIC`** — a 64-bit nanosecond counter that survives NTP steps and is the natural home for the logger, video ingest and behaviour timeline.

Alternatives considered: making C2 the master (the most stable timer, the source of the safety-critical events) — rejected for V1 because every other producer (camera, audio, cloud round-trips, video) lives on the SBC side and would then need converting; and a GPS/PPS or RTC-disciplined master — unnecessary at Makad's scale. If a base MCU is added, it reconciles to the SBC exactly as C2 does.

Consequence: C2 and the display board each hold `(offset_us, rate_ppm, uncertainty_us, last_sync_ts)` and apply them to their own stamps before transmitting `capture_ts_us`; they also transmit the raw local stamp in debug builds.

## 3. Offset reconciliation over the serial link

The MultiSense/NTP-style four-timestamp exchange, carried by `TIME_SYNC_REQ` / `TIME_SYNC_RESP` in `link-contract.md` §4.4:

```
SBC sends  REQ  at t1 (master)
C2 receives REQ  at t2 (local)
C2 sends   RESP at t3 (local)          RESP carries t1, t2, t3
SBC receives RESP at t4 (master)

round_trip = (t4 − t1) − (t3 − t2)
offset     = ((t2 − t1) + (t3 − t4)) / 2      # local − master, assumes symmetric path
```

Rules that make this honest on a UART:

- **Stamp at the hardware edge**, not in application code: on C2, `t2` in the UART RX interrupt for the frame's first byte and `t3` immediately before the TX FIFO write; on the SBC, `t1`/`t4` as close to the syscall as the driver allows. The residual asymmetry is measured in §6, not assumed away.
- **Filter.** Keep the sample with the smallest `round_trip` in a sliding window (minimum-filter), then fit `offset(t) = a + b·t` over the window to estimate rate. Reject samples whose `round_trip` exceeds 2× the window minimum (a scheduling hiccup on the SBC, not a clock fact).
- **Rate.** 1–2 Hz sync is enough: at 20 ppm the drift between syncs is ≤ 20 µs, far inside the candidate 1 ms p95 budget, and the rate fit removes most of it anyway.
- **Report.** The filtered `offset_us`, `rate_ppm`, window minimum `round_trip` and a derived `uncertainty_us` (half the minimum round trip plus fit residual) travel in the next `TIME_SYNC_REQ` and are logged every sync.
- **Bootstrap.** Until the first three valid samples, C2 marks time `degraded` and uses local expiry for command validity (`link-contract.md` §5).

## 4. Rules for producers

| Producer | Stamps | Where |
|---|---|---|
| C2 | Encoder/servo telemetry read, trajectory sample, brake onset, fault detection, heartbeat send | Interrupt or tick handler; converted before send; raw local kept in debug |
| Display board | Face-state receipt, frame-flip (for RP-04's onset measurement) | Render loop |
| SBC perception | Frame *capture* time from the camera driver (V4L2/libcamera sensor timestamp, itself `CLOCK_MONOTONIC`), not frame-processed time | Driver callback |
| SBC audio | Buffer capture/playback callback time | ALSA/PortAudio callback |
| SBC behaviour | Intent issue, command send, cloud request/response | At the call site |
| Bench instrument MCU | INA226 samples, thermistors | Local timer, reconciled by the same §3 method over its own serial link |
| External video | See §5 | — |

**Never** reconstruct a stamp from a later one plus an assumed delay.

## 5. External video synchronization

Independent video is required where motion or perceived timing matters (plan, evidence packet item 6). The cue is the **status light**: `LIGHT_STATE` with `sync_ts_us` commands a distinctive pattern (candidate: three 50 ms flashes, 200 ms apart) at a master timestamp at the start and end of every run; the logged command time and the frame in which the first flash appears give the video-to-master offset to within one video frame (≈ 4 ms at 240 fps, 33 ms at 30 fps). Run ID is also shown or announced on camera at the start (`run-record-convention.md` bench workflow). Until the status light exists, an LED on the bench instrument MCU does the same job.

## 6. Validation method (RP02-G05)

The claim to prove: *a C2 event converted to master time lands within `X` of the true master time*. Measured independently of the link being validated:

1. C2 toggles a GPIO on every trajectory tick and logs each toggle's converted master stamp (`c2_tick`).
2. The SBC (or the bench MCU acting for it) drives a second GPIO at a scheduled master timestamp (`sync_edge`).
3. Both lines go to the **logic analyzer**, which sees the true relative timing of the edges at 24 MHz resolution.
4. The difference between the analyzer's measured edge separation and the separation implied by the logged stamps is the reconciliation error. Collect ≥ 10 min; report p50/p95/max, and the same after a deliberate SBC load spike and after a wall-clock step (F-15).

Candidate acceptance (registered in `RP-02-electrical/gates.md` G05): **p95 ≤ 1 ms**, max ≤ 5 ms, uncertainty self-report within 2× of the measured p95. Also record the round-trip p50/p95 and the residual path asymmetry so the §3 symmetric-path assumption is a measured quantity.

## 7. What this does not solve

- The **logging schema** (channel names, file format, the pre-run write check) — a separate open input in the plan.
- **Absolute** time accuracy — irrelevant; only relative alignment matters.
- Synchronization of a **third-party** device with no serial path (a phone camera) — handled by §5's visible cue only.
- Servo-internal timestamps — smart servos report state on request; the request time on C2 is the stamp.

## 8. Open items

- [ ] Implement §3 on the DevKitC-1 twin and a laptop; run the §6 measurement as `RP02-EXP-exploratory`.
- [ ] Decide the SBC-side stamping point once the SBC candidate and its UART driver are known; measure the syscall-to-wire latency.
- [ ] Register G05 timing thresholds.
- [ ] Extend to the display board and, later, a base MCU with no method change.
- [ ] Define the logging schema so converted and raw stamps are both retained.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-08 | 0.1 | Strategy documented from `control-topology-options.md` §5: SBC `CLOCK_MONOTONIC` master, timestamp-at-source rules per producer, four-timestamp serial reconciliation with minimum-filter and rate fit, status-light video cue, and a logic-analyzer validation method with candidate acceptance for RP02-G05. Not implemented. |
