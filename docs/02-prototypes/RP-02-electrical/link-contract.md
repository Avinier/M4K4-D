# Makad Internal Link Contract — SBC ↔ C2 ↔ Display

| Field | Value |
|---|---|
| Status | **v0.2 draft.** Interface specification, not evidence. Field sizes, rates and timeouts marked *candidate* are proposals for G05/G04 registration |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-12 |
| Authority | `../../01-system/control-topology-options.md` v0.10 §3, §7 (UART/USB serial, semantic command surface); `../../01-system/system-design-brief.md` §5 information contracts and contract rules 1–5; §6 state dimensions and failure priorities |
| Timebase | `../../01-system/timebase.md` — all timestamps in this contract are master-monotonic microseconds after offset reconciliation |
| Feeds | ADR-12; `subsystem-interfaces.md` at stage 6; `fault-matrix.md`; `gates.md` G04/G05 |
| Not in scope | The servo bus protocol (RP-01 servo selection decides Dynamixel 2.0 / Feetech / other); display asset transfer; any wireless path |

This is the artifact RP-02 produces that outlives it. It is versioned as a specification: a change is a new minor version with a changelog line; a breaking change is a new major version and a `fault-matrix.md` re-run.

## 1. Principles carried in from the design brief

1. **Semantic, not raw.** The SBC sends *what it wants* — a head goal with a profile law, a face state, a cancel — never PWM, joint increments or raster frames. Controllers enforce physics (SDB §4 behaviour authority row).
2. **Every time-sensitive message is timestamped at source** in master time (contract rule 1), and every command carries an explicit **expiry** (rule 4).
3. **Unknown, stale, unavailable are representable** (rule 2). Health is an enum, never a boolean; a missing field means unknown, not zero.
4. **No replay after restart or reconnect** (rules 4, 5). Both ends drop their queues on link-down; recovery requires a fresh authorization.
5. **Bounded queues** (rule 5). A recovered subsystem never executes an old burst.
6. **Safety semantics live on C2.** The SBC being busy, rebooting or lying about time cannot produce motion; only its *silence* produces an inhibit, and only its *fresh explicit intent* produces a resume.

## 2. Physical links

| Link | Transport | Candidate rate | Why |
|---|---|---|---|
| SBC ↔ C2 | 3.3 V TTL UART, full duplex, no flow control; **USB-CDC on the Zero's native USB is the fallback** if UART throughput or the flashing path makes it preferable | 921 600 baud candidate (115 200 is ~11.5 kB/s and too tight against §6) | Two boards, one enclosure, permanent wire: the openvmp "dumb serial relay" test says serial. UART keeps native USB free for flashing (CAD-04a) |
| SBC ↔ display ESP32-S3 | Same framing over a second UART | 115 200–921 600; face-state traffic is small | Same code path on the SBC; the display board's GPIO budget (RS-485 or UART pins per the schematic audit) decides the physical pair |
| C2 ↔ servos | **Out of scope here** — half-duplex TTL or RS-485 per servo family | family-defined | Owned by RP-01's actuator selection; C2 keeps the transceiver external (bus-neutrality, control study §6.3) |

Both UART links cross the yaw boundary on the head-logic branch (PA-06) through the demateable connector. Signal integrity across the flexing harness is a G05 measurement (frame CRC error rate per hour under S05 sweeps).

## 3. Framing

| Layer | Choice | Reason |
|---|---|---|
| Byte framing | **COBS** with `0x00` delimiter | Resynchronizes after any corruption without a length pre-read; trivial on an MCU |
| Integrity | **CRC-16/CCITT** over header + payload, before COBS | Detects the bit-flips an unshielded UART across a servo harness will see (F-04) |
| Header | `ver:u8` · `type:u8` · `seq:u16` · `src_ts_us:u64` · `len:u8` | `seq` detects loss and duplicates; `src_ts_us` is the stamp *at the producer*, never at receipt |
| Encoding | Little-endian packed structs; fixed-point where noted | No parsing ambiguity; no allocation on C2 |
| Max frame | 64 bytes payload candidate | A full 64-byte payload is about 81 bytes on wire after the 13-byte header, CRC, COBS overhead and delimiter: ~0.88 ms at 921 600 baud, still below one 5 ms control tick |

## 4. Message set

Types are grouped by the five information kinds in SDB §5. `→` SBC to controller; `←` controller to SBC.

### 4.1 Session and authorization

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `HELLO` | ↔ | `fw_hash:u32` · `contract_ver:u16` · `board_id:u8` · `capabilities:u16` | First frame after either side (re)starts. Mismatched `contract_ver` → controller stays `inhibited` and reports `FAULT(CONTRACT_MISMATCH)` |
| `LIMITS_SET` | → | per axis: `min:i16` · `max:i16` (0.01°) · `vmax:u16` (°/s) · `amax:u16` (°/s²) · `imax:u16` (mA) · `tmax:u8` (°C); `cmd_ttl_default_ms:u16`; `heartbeat_timeout_ms:u16` | Must be acknowledged before `HEAD_ENABLE` is accepted. Values are clamped to C2's compiled hard limits; the clamped set is echoed in the `ACK` |
| `HEAD_ENABLE` | → | `nonce:u32` | Transitions C2 `inhibited → enabled` **only if** limits are set, heartbeat is fresh, no fault is latched and the motor domain is present. The nonce prevents a stale frame from re-enabling after a restart |
| `HEAD_INHIBIT` | → | `reason:u8` | Initiate `BRAKE` immediately, then enter `inhibited` when the registered bounded trajectory reaches rest. Idempotent |

### 4.2 Commands (bounded, expiring)

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `HEAD_GOAL` | → | `gesture_id:u16` · `segment:u8` · `profile:u8` (`MJ5`/`MS7`/`TRACK`/`BRAKE`) · `yaw,pitch,roll:i16` (0.01°) · `duration_ms:u16` · `valid_until_us:u64` · `flags:u8` (hold-after, interruptible) | One authored segment. C2 instantiates the profile law itself; the SBC never streams intermediate points for authored gestures. For `TRACK`, `HEAD_GOAL` carries the current filtered target and is re-sent at the tracking rate |
| `HEAD_CANCEL` | → | `gesture_id:u16` or `0xFFFF` all · `settle:u8` (BRAKE law index) | HM-18 controlled cancel. Rejects any queued segment of that gesture; current motion decelerates under `BRAKE` |
| `FACE_STATE` | → display | `expression:u8` · params: gaze `x,y:i8` · lids `l,r:u8` · `blink:u8` · `brightness:u8` · `utility_view:u8` · `valid_until_us:u64` | Semantic face; the renderer owns pixels and animation. An expired `FACE_STATE` decays to the renderer's idle, never freezes |
| `LIGHT_STATE` | → head | `pattern:u8` · `intensity:u8` · `period_ms:u16` · `sync_ts_us:u64` | Status light beside the camera. `sync_ts_us` lets the light double as the **video timing cue** (`timebase.md` §5) |

**Expiry rule.** C2 evaluates `now_master_us > valid_until_us` at *execution*, not at receipt. An expired command is discarded with `NACK(EXPIRED)`. Candidate defaults: `TRACK` goals 100 ms; authored segments `duration_ms + 250 ms`; `FACE_STATE` 2 s. These are G04/G05 registration items.

### 4.3 Feedback and health

| Type | Dir | Payload | Rate (candidate) |
|---|---|---|---|
| `HEAD_STATE` | ← | `capture_ts_us:u64` · per axis `pos:i16` (0.01°) · `vel:i16` · `cur:i16` (mA) · `temp:u8` · `servo_flags:u8`; `gesture_id:u16` · `segment:u8` · `progress:u8`; `ctrl_state:u8` (`inhibited/enabled/braking/fault`) | 100 Hz; `capture_ts_us` is the encoder read time on C2's clock, converted per `timebase.md` |
| `HEARTBEAT` | ↔ | `health:u8` (`available/degraded/unavailable/unsafe`) · `energy:u8` (`normal/low/critical/charging`) · `motor_domain:u8` (present/absent) · `last_rx_age_ms:u16` · `loop_jitter_us_p99:u16` · `crc_err_count:u16` | 20 Hz each way. C2's heartbeat carries its own timing self-report so G05 has continuous evidence, not only a bench measurement |
| `FAULT` | ← | `code:u16` · `axis:u8` · `detail:u32` · `ts_us:u64` · `latched:u8` | Event, retransmitted with every `HEARTBEAT` while latched. Codes include `HB_TIMEOUT`, `EXPIRED_BURST`, `LIMIT_HIT`, `SERVO_OVERCURRENT`, `SERVO_OVERTEMP`, `SERVO_SILENT`, `MOTOR_DOMAIN_LOST`, `CONTRACT_MISMATCH`, `BROWNOUT_RESET` |
| `ACK` / `NACK` | ← | `for_seq:u16` · `reason:u8` (`OK/EXPIRED/OUT_OF_LIMITS/INHIBITED/UNKNOWN_TYPE/BAD_CRC/QUEUE_FULL/NO_LIMITS/NONCE_REPLAY`) | Per command frame |

### 4.4 Time

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `TIME_SYNC_REQ` | → | `t1_master_us:u64` · `model_valid:u8` · `offset_at_ref_us:i64` · `rate_ppb:i32` · `model_ref_local_us:u64` · `uncertainty_us:u32` | Sent at 1–2 Hz. C2 stamps receipt `t2` and transmit `t3` on its local clock. The model fields carry the previous filtered fit; they are ignored until `model_valid=1` |
| `TIME_SYNC_RESP` | ← | `t1:u64` · `t2_local_us:u64` · `t3_local_us:u64` | SBC stamps `t4` at receipt and updates the offset/rate fit per `timebase.md` §3. The next `TIME_SYNC_REQ` carries the complete model (`offset_at_ref_us`, `rate_ppb`, `model_ref_local_us`, `uncertainty_us`) so C2 can convert its own `capture_ts_us` |

## 5. Watchdog and recovery semantics

These are the G04 behaviours, stated as contract so they can be tested rather than hoped for.

| Condition on C2 | Required behaviour | Fault case |
|---|---|---|
| No valid `HEARTBEAT` from SBC for `heartbeat_timeout_ms` (candidate **150 ms**, i.e. three missed at 20 Hz) | **Initiate** `BRAKE` no later than one control tick after timeout; state becomes `braking` then `inhibited` on completion; `FAULT(HB_TIMEOUT)` latched; **queue flushed**. Time to rest is bounded by the registered BRAKE trajectory, not one tick | F-01, F-02, F-03 |
| Heartbeats resume | Stay `inhibited`. Report. **Do not resume the interrupted gesture.** Resume only on a fresh `LIMITS_SET` → `HEAD_ENABLE` with a new nonce and a *new* `HEAD_GOAL` | "Recover only from current authorized intent" |
| Frame fails CRC | Discard; increment `crc_err_count`; no state change. Above a registered rate per second → `degraded`; above a higher rate → `inhibited` | F-04 |
| Command arrives with `valid_until_us` in the past | `NACK(EXPIRED)`. A burst of expired commands after reconnect (queue drain on the SBC side) is **rejected frame by frame**; `FAULT(EXPIRED_BURST)` if more than N in one tick | F-05 |
| `src_ts_us` jumps backwards or ahead beyond the reconciliation window | Treat the sender's time as untrusted: `degraded`, use local expiry until sync recovers | F-15 |
| C2 itself resets (watchdog, brownout, manual) | Boot into `inhibited` with no limits; servos receive torque-off or hold per the RP-01 HM-00 result; `HELLO` with `BROWNOUT_RESET` flag if the reset reason says so | F-06 |
| Motor domain absent (E-stop asserted) while `enabled` | `FAULT(MOTOR_DOMAIN_LOST)`, state `inhibited`; **release of the E-stop does not re-enable** | F-12, F-13 |
| Servo silent on the bus for N polls | That axis `unavailable`; other axes complete their `BRAKE`; whole head `inhibited` until re-enabled | F-08 |
| Energy `critical` reported by the SBC, or pack telemetry on C2 crosses the registered threshold | `BRAKE` to the registered rest pose (HM-02 descent if energy allows), then `inhibited` | F-16 |

The SBC side mirrors: on link-down it **drops its outbox**, marks head `unavailable` in situation state, and the behaviour authority must re-issue intent, not replay it. Long-running actions (following) treat head `unavailable` as a bounded-stop condition per SC-15.

## 6. Bandwidth estimate (candidate, for the baud decision)

| Stream | Bytes/frame (incl. 13-byte header, 2-byte CRC, COBS overhead and delimiter) | Rate | kbit/s |
|---|---|---|---|
| `HEAD_STATE` | ~46 | 100 Hz | ~37 |
| `HEARTBEAT` ×2 | ~22 each | 20 Hz each | ~7 |
| `HEAD_GOAL` (`TRACK`) | ~32 | 50 Hz | ~13 |
| `TIME_SYNC` pair | ~50 + ~41 | 2 Hz | <2 |
| `ACK`/`NACK` | ~14 | ≤50 Hz | ~6 |
| **Total** | | | **~64 kbit/s** |

115 200 baud (~92 kbit/s usable) fits on paper with no margin and no room for burst logging; **921 600 baud is the candidate** and gives ~10× headroom. If the flex harness cannot carry 921 600 cleanly (G05 CRC-error measurement), 460 800 is the fallback before considering USB-CDC.

## 7. Timing requirements this contract implies (candidates for G05)

| Quantity | Candidate | Why this number |
|---|---|---|
| C2 trajectory sample rate | ≥ 200 Hz | HM-08 laugh pulses are 7° in 100 ms; 200 Hz gives 20 samples per pulse. RP-01 `physics.md` peak accelerations (4 000–4 700 °/s²) need dense sampling to keep the `MJ5` shape |
| Servo bus update rate | ≥ 100 Hz sync write/read for three axes | Family-dependent; Dynamixel 2.0 at 1 Mbps supports this comfortably |
| C2 loop jitter | p99 ≤ 10 % of the loop period | Jitter shows up as trajectory roughness — an expressive-quality metric (invariant 6) |
| Link round-trip p95 | ≤ 5 ms | Keeps `TRACK` corrections from feeling laggy; RP-05 will tighten |
| Timestamp reconciliation error p95 | ≤ 1 ms | The RP-01 combined-reversal analysis needs per-axis events aligned better than one sample |
| Heartbeat timeout → motion inhibited | ≤ 200 ms from last valid heartbeat to `BRAKE` onset | Three missed heartbeats plus one tick; SC-15 bounded state |

## 8. What is deliberately not specified yet

- Exact byte layouts — pinned when the first firmware implements this v0.2 draft and the SBC-side codec is generated from one schema file (one source, two targets).
- Authentication — none on a wired internal link; the nonce guards against replay, not adversaries.
- Display asset upload — a bulk-transfer mode with its own flow control, designed when face assets exist.
- Base/drive MCU messages — added when RP-03 selects a base controller; they inherit this framing and the same expiry/heartbeat rules.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-08 | 0.1 | First draft: transports, COBS+CRC-16 framing, message set across session/command/feedback/time, watchdog and recovery semantics, bandwidth estimate, candidate timing requirements for G05. No field layout frozen; nothing registered. |
| 2026-09-12 | 0.2 | Added the complete offset/rate/reference/uncertainty model to TIME_SYNC_REQ so C2 can perform the conversion required by timebase v0.2. Corrected heartbeat failure semantics to BRAKE onset within one tick after timeout; rest completion follows the bounded BRAKE trajectory. Nothing registered. |
