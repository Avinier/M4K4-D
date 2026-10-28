# Makad Internal Link Contract — SBC ↔ C2 ↔ Display

| Field | Value |
|---|---|
| Status | **Part-4 C0↔C2 definition baseline `RP02-P4-REG-01` (2026-09-17).** C0↔C3 `BASE_*` **semantics** `RP02-P4-REG-02` (2026-09-18). Coordination fields **`RP02-P4-REG-03`** (2026-09-21, v0.6): cue identity, optional `start_at_us`, face/light source-onset reports, extra `NACK` values. Exact byte layouts, type numbers, baud and measured timeouts remain open on both links; THVD1451D is an implementation lead |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-21 |
| Authority | `compute-control-architecture.md` `CA-01…16`; `../../01-system/control-topology-options.md` §3, §7 (framed serial, semantic command surface); `../../01-system/system-design-brief.md` §5 information contracts and contract rules 1–5; §6 state dimensions and failure priorities |
| Timebase | `../../01-system/timebase.md` — all timestamps in this contract are master-monotonic microseconds after offset reconciliation |
| Feeds | ADR-12; `fault-matrix.md`; `gates.md` G04/G05 |
| Not in scope | The servo bus protocol (RP-01 family freeze decides Dynamixel 2.0 / Feetech / other; C01 would be Dynamixel Protocol 2.0 TTL, 3.3 V logic 5 V compatible); display asset transfer; any wireless path |

This is the artifact RP-02 produces that outlives it. `RP02-P4-REG-01` registers the **definition** of the C0↔C2 message set, COBS-delimited/CRC-protected framing method, source stamps, explicit expiry, heartbeat supervision, two-phase arm and fresh-intent recovery. It does not register numeric timing or a wire-compatible codec. Changes to these semantics need a new registration and fault review; byte-layout revisions remain versioned here and are qualified under G04/G05.

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
| SBC ↔ C2 | UART framing over **full-duplex differential RS-422/RS-485 signalling**, two twisted pairs plus registered common reference; THVD1451D SOIC implementation lead at each end. Direct TTL is bench-only; native USB is service-only | 921 600 baud candidate (115 200 is ~11.5 kB/s and too tight against §6) | Preserves the simple UART software model while hardening the motor-adjacent moving harness; full duplex avoids direction turnaround and collisions; native USB stays free for flashing (CAD-04a) |
| C2 ↔ display ESP32-S3 | C2 relays the same framed semantic messages over the display carrier's head-local half-duplex RS-485 path | 115 200 baud initial; face-state traffic is small | One body ingress and one head-local clock model; display traffic has lower queue priority than motion/link health |
| C2 ↔ servos | **Out of scope here** — half-duplex TTL or RS-485 per servo family. C01 (XC330-M288-T) would be TTL Dynamixel 2.0 | family-defined | Owned by RP-01's actuator selection; C2 keeps the transceiver external (bus-neutrality, control study §6.3). C01 does not freeze the transceiver |

The baseline has **one logical head link** across the yaw boundary through the demateable connector: two differential pairs plus common reference accompany `PB-SAFE-C2`; the display receives its semantic state from C2 locally and retains its separate `PB-DISPLAY` supply. No signal path may back-power another branch. Together with camera CSI and hazardous `PB-HEAD` conductors, these remain separate functional moving-harness paths under `PA-06`. Signal integrity across the flexing harness is a G05 measurement (frame CRC/sequence-error rate per hour under `CC-04` search sweeps and representative motor noise).

C2's relay queue is fixed-capacity and lower priority than head control, heartbeat, time sync and faults. `FACE_STATE` is latest-wins; asset transfer is forbidden while motion is enabled. A C2 reset makes D1 expire to idle and boots C2 inhibited. `F-27` proves that a stuck/flooded display path cannot perturb the C2 control deadline.

The base controller C3 uses the same COBS/CRC/session/time/expiry envelope over an independent differential UART. Base message types are deliberately not invented here before RP-03 freezes motor/sensor semantics; they must preserve the same fresh-arm, bounded-queue and no-replay rules.

## 3. Framing

| Layer | Choice | Reason |
|---|---|---|
| Byte framing | **COBS** with `0x00` delimiter | Resynchronizes after any corruption without a length pre-read; trivial on an MCU |
| Integrity | **CRC-16/CCITT** over header + payload, before COBS | Detects the bit-flips an unshielded UART across a servo harness will see (F-04) |
| Header | Candidate fields: `ver`, `type`, `seq`, `src_ts_us`, `len`; authorization context additionally includes C0 boot identity and session epoch | `seq` detects loss and duplicates; `src_ts_us` is stamped *at the producer*. The listed field widths/order are candidates, not registered byte layout. C2 must bind every motion command to the active boot/epoch, whether carried in the eventual header or an authenticated session context |
| Encoding | Little-endian packed structs; fixed-point where noted | No parsing ambiguity; no allocation on C2 |
| Max frame | 64 bytes payload candidate | The older 13-byte header gives ~81 wire bytes, but the exploratory envelope carrying C0 boot UUID and epoch is up to 101 wire bytes (~1.10 ms at 921 600 baud, 10 UART bits/byte). Recalculate from the final layout before G05; neither size is registered |

## 4. Message set

Types are grouped by the five information kinds in SDB §5. `→` SBC to controller; `←` controller to SBC.

### 4.1 Session and authorization

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `HELLO` | ↔ | `fw_hash`, `contract_ver`, `board_id`, `capabilities`; C2 also supplies a fresh boot challenge that C0 echoes in session establishment (exact field layout open) | First frame after either side (re)starts. Mismatched `contract_ver` → controller stays `inhibited` and reports `FAULT(CONTRACT_MISMATCH)`. Old C0 `HELLO`/limits/enable frames from before a C2 reboot must not establish a new session |
| `LIMITS_SET` | → | per axis: `min:i16` · `max:i16` (0.01°) · `vmax:u16` (°/s) · `amax:u16` (°/s²) · `imax:u16` (mA) · `tmax:u8` (°C); `cmd_ttl_default_ms:u16`; `heartbeat_timeout_ms:u16` | Must be acknowledged before `HEAD_ENABLE` is accepted. Values are clamped to C2's compiled hard limits; the clamped set is echoed in the `ACK` |
| `HEAD_ENABLE` | → | fresh arm nonce (candidate `u32`) | Transitions C2 `inhibited → enabled` **only if** limits are set, heartbeat is fresh, no fault is latched and the motor domain is present. It is bound to the current C2 boot challenge, C0 boot identity and epoch; a nonce alone cannot prevent replay across a C2 cold reset |
| `HEAD_INHIBIT` | → | `reason:u8` | Initiate `BRAKE` immediately, then enter `inhibited` when the registered bounded trajectory reaches rest. Idempotent |

Cue identity (both links, candidate packing `perf_id:u16` · `perf_epoch:u32` · `cue_id:u8`, **not** a registered layout): joins command, ACK, state and onset without using clock proximity. `perf_epoch` is the performance instance; it is not the C0 boot/session epoch. A new intent is a new `perf_epoch`.

Optional `start_at_us` (candidate `u64`, 0 = execute when accepted): do not begin before that master timestamp. `start_at_us > valid_until_us` → `NACK(EXPIRED)`. Non-zero `start_at_us` with an invalid or over-bound time model → `NACK(TIME_MODEL_INVALID)` — never silent immediate run. Arrival after `start_at_us` uses a **registered lateness window** (numeric still open): inside the window, execute; outside → `NACK(LATE)`. Immediate cues (`start_at_us = 0`) keep today's expiry-only rule.

### 4.2 Commands (bounded, expiring)

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `HEAD_GOAL` | → | cue identity · `start_at_us` · `gesture_id:u16` · `segment:u8` · `profile:u8` (`MJ5`/`MS7`/`TRACK`/`BRAKE`) · `yaw,pitch,roll:i16` (0.01°) · `duration_ms:u16` · `valid_until_us:u64` · `flags:u8` (hold-after, interruptible) | One authored segment. C2 instantiates the profile law itself; the SBC never streams intermediate points for authored gestures. For `TRACK`, `HEAD_GOAL` carries the current filtered target and is re-sent at the tracking rate |
| `HEAD_CANCEL` | → | cue identity · `gesture_id:u16` or `0xFFFF` all · `settle:u8` (BRAKE law index) | HM-18 controlled cancel of that performance instance (or all if `gesture_id` is all). Rejects any queued segment of that gesture; current motion decelerates under `BRAKE` |
| `FACE_STATE` | → display | cue identity · `start_at_us` · `expression:u8` · params: gaze `x,y:i8` · lids `l,r:u8` · `blink:u8` · `brightness:u8` · `utility_view:u8` · `valid_until_us:u64` | Semantic face; the renderer owns pixels and animation. An expired `FACE_STATE` decays to the renderer's idle, never freezes |
| `LIGHT_STATE` | → head | cue identity · `start_at_us` · `pattern:u8` · `intensity:u8` · `period_ms:u16` · `sync_ts_us:u64` | Status light beside the camera. `sync_ts_us` is the **requested** video timing cue (`timebase.md` §5), not proof the LED changed |

**Expiry rule.** C2 evaluates `now_master_us > valid_until_us` at *execution*, not at receipt. An expired command is discarded with `NACK(EXPIRED)`. Candidate defaults: `TRACK` goals 100 ms; authored segments `duration_ms + 250 ms`; `FACE_STATE` 2 s. These are G04/G05 registration items.

Stale identity: if `perf_epoch` is older than the executor's current instance for that channel, or belongs to a dead C0 session, `NACK(STALE_EPOCH)` and do not start the cue.

### 4.3 Feedback and health

| Type | Dir | Payload | Rate (candidate) |
|---|---|---|---|
| `HEAD_STATE` | ← | cue identity · `capture_ts_us:u64` · `onset_ts_us:u64` (0 until first motion above the onset criterion) · per axis `pos:i16` (0.01°) · `vel:i16` · `cur:i16` (mA) · `temp:u8` · `servo_flags:u8`; `gesture_id:u16` · `segment:u8` · `progress:u8`; `ctrl_state:u8` (`inhibited/enabled/braking/fault`) | 100 Hz; `capture_ts_us` is the encoder read time on C2's clock, converted per `timebase.md` |
| `FACE_REPORT` | ← | cue identity · `expression:u8` · `flip_ts_us:u64` · `outcome:u8` | Event: D1 frame-flip of the first frame that represents that `FACE_STATE`. Receipt or render-queue insertion is not onset. C2 relays |
| `LIGHT_REPORT` | ← | cue identity · `pattern:u8` · `onset_ts_us:u64` · `outcome:u8` | Event: actual light-output transition. `LIGHT_STATE.sync_ts_us` is not this stamp |
| `HEARTBEAT` | ↔ | `health:u8` (`available/degraded/unavailable/unsafe`) · `energy:u8` (`normal/low/critical/charging`) · `motor_domain:u8` (present/absent) · `last_rx_age_ms:u16` · `loop_jitter_us_p99:u16` · `crc_err_count:u16` | 20 Hz each way. C2's heartbeat carries its own timing self-report so G05 has continuous evidence, not only a bench measurement. Channel absence is `health`, not a new `NACK` value |
| `FAULT` | ← | `code:u16` · `axis:u8` · `detail:u32` · `ts_us:u64` · `latched:u8` | Event, retransmitted with every `HEARTBEAT` while latched. Codes include `HB_TIMEOUT`, `EXPIRED_BURST`, `LIMIT_HIT`, `SERVO_OVERCURRENT`, `SERVO_OVERTEMP`, `SERVO_SILENT`, `MOTOR_DOMAIN_LOST`, `CONTRACT_MISMATCH`, `BROWNOUT_RESET`. Progress-stuck is a `FAULT` / state condition, not a command `NACK` |
| `ACK` / `NACK` | ← | `for_seq:u16` · cue identity when the command carried one · `reason:u8` (`OK` / `EXPIRED` / `OUT_OF_LIMITS` / `INHIBITED` / `UNKNOWN_TYPE` / `BAD_CRC` / `QUEUE_FULL` / `NO_LIMITS` / `NONCE_REPLAY` / `TIME_MODEL_INVALID` / `LATE` / `STALE_EPOCH`) | Per command frame. New values occupy the existing `u8`; they do not widen the field |

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
| Scheduled cue (`start_at_us ≠ 0`) while time model invalid or uncertainty over bound | `NACK(TIME_MODEL_INVALID)`. Do not execute immediately | RP-04 `OX-TIME`; G04 |
| Scheduled cue arrives after `start_at_us` outside the lateness window | `NACK(LATE)`. Distinct from `EXPIRED` | RP-04 `OX-DELAY`; G04. Window numeric open |
| Command `perf_epoch` older than the current instance, or from a dead session | `NACK(STALE_EPOCH)`. No local start | RP-04 `OX-STALE` / `OX-RESTART`; G04 |
| `src_ts_us` jumps backwards or ahead beyond the reconciliation window | Treat the sender's time as untrusted: `degraded`, use local expiry until sync recovers. This is not a scheduled-cue NACK; refuse new `start_at_us ≠ 0` with `TIME_MODEL_INVALID` until sync recovers | F-15 |
| C2 itself resets (watchdog, brownout, manual) | Boot into `inhibited` with no limits; servos receive torque-off or hold per the RP-01 HM-00 result; `HELLO` with `BROWNOUT_RESET` flag if the reset reason says so | F-06 |
| Motor domain absent (E-stop asserted) while `enabled` | `FAULT(MOTOR_DOMAIN_LOST)`, state `inhibited`; **release of the E-stop does not re-enable** | F-12, F-13 |
| Servo silent on the bus for N polls | That axis `unavailable`; other axes complete their `BRAKE`; whole head `inhibited` until re-enabled | F-08 |
| Energy `critical` reported by the SBC, or pack telemetry on C2 crosses the registered threshold | `BRAKE` to the registered rest pose (HM-02 descent if energy allows), then `inhibited` | F-16 |

The SBC side mirrors: on link-down it **drops its outbox**, marks head `unavailable` in situation state, and the behaviour authority must re-issue intent, not replay it. Long-running actions (following) treat head `unavailable` as a bounded-stop condition per SC-15.

## 6. Bandwidth estimate (candidate, for the baud decision)

The table below predates the explicit boot UUID/epoch envelope and uses a 13-byte header. It is a historical lower-bound screen, **not** a G05 bandwidth result. The final byte layout must be budgeted again with its actual message sizes and bursts.

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

- Exact byte layouts and message type numbers — pinned after the first C0/C2 implementation and SBC-side codec are generated from one schema file (one source, two targets). Any exploratory codec must declare its layout revision and cannot be scored as this registered definition.
- Authentication — none on a wired internal link; the nonce guards against replay, not adversaries.
- Display asset upload — a bulk-transfer mode with its own flow control, designed when face assets exist.
- Base/drive MCU messages — C3 `BASE_*` **semantics** are registered under `RP02-P4-REG-02` (v0.5). Byte layouts, type numbers, baud and numeric timeouts stay open.

## Part-4 registration — 2026-09-17

`RP02-P4-REG-01` freezes the definition baseline in §§1–5: semantic commands; the C0↔C2 message set; C2 relay of face/light state; source stamps; explicit expiry checked at execution; C0 session/epoch plus a fresh C2 boot challenge and arm nonce; limits acknowledged before enable; heartbeat loss causing bounded brake and queue flush; and reconnect/reset/E-stop recovery requiring a new limits/enable/goal sequence. The physical topology remains governed by `RP02-P3-REG-01`. The C2 challenge must change on every reset and cannot be inferred from old wire traffic; its generation and retained replay window need implementation review.

The candidate byte widths, type numbers, baud/rates/timeouts, transceiver suffix and measured G04/G05 outcomes are **not** registered by `RP02-P4-REG-01`. C3 `BASE_*` **semantics** are registered separately under `RP02-P4-REG-02` below. A physical or scored implementation requires byte layouts to be versioned and preregistered. No ADR or gate closes here.

## v0.5 — C0↔C3 `BASE_*` semantics (`RP02-P4-REG-02`, 2026-09-18)

**Accepted as the C0↔C3 definition baseline for message types, expiry, fresh-arm, `CC-12C_ARM`, unknown-is-inhibit and no-replay recovery.** Same relationship to byte layout that `RP02-P4-REG-01` has for C0↔C2: semantics are registered; layouts, type numbers, baud and measured timeouts are not.

Origin: RP-03 Part 4 (`base-control-architecture.md`). Envelope: COBS, CRC-16/CCITT, session / C0 boot identity / epoch / C3 boot challenge, `src_ts_us`, explicit expiry, fresh-arm nonce, independent C0↔C3 differential UART. Motor/driver/sensor SKUs are not frozen by naming these types.

`HELLO`, `HEARTBEAT`, `TIME_SYNC_REQ` / `TIME_SYNC_RESP`, and `ACK` / `NACK` are the same types as the head link, on this independent session. `ACK` / `NACK` reasons follow §4.3, including `TIME_MODEL_INVALID` / `LATE` / `STALE_EPOCH`. Authority stays `CA-09` / `CA-13`: clearing an inhibit reports availability and does not resume old intent. Cue identity and `start_at_us` on `BASE_GOAL` / `BASE_CANCEL` / `BASE_STATE` match the head rules.

`→` C0 to C3; `←` C3 to C0. Payload columns name semantics, not wire widths.

### Session and authorization

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `BASE_LIMITS_SET` | → | Per wheel: `vmin`, `vmax`, `amax`, `imax`; yaw `wmax`; `cmd_ttl`; `heartbeat_timeout` | Must be acknowledged before `BASE_ENABLE`. Values are clamped to C3 compiled hard maxima (`CA-14`); the clamped set is echoed in the `ACK` |
| `BASE_ENABLE` | → | Fresh arm nonce | `inhibited → enabled` **only if** limits are set, heartbeat is fresh, no fault is latched, motor domain is present, and mode is valid. Bound to the current C3 boot challenge, C0 boot identity and epoch. Does **not** grant `CC-12C` |
| `BASE_INHIBIT` | → | `reason` | Initiate `BRAKE` immediately, then inhibited when the bounded trajectory reaches rest. Idempotent |
| `CC-12C_ARM` | → | Separate nonce + expiry + speed clamp | Arms minimum-speed tabletop calibration in `OM-02` only. Clamp is storyboard `BM-11` 0.06 m/s. Never implied by `BASE_ENABLE`. Never grants come / follow / spin |

### Commands (bounded, expiring)

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `BASE_GOAL` | → | cue identity · `start_at_us` · `profile_id` (`LAUNCH` / `CRUISE` / `DECEL0` / `PIVOT` / `ARC` / `SPIN` / `WIGGLE` / `BRAKE` / `HOLD`) · `v`, `ω` · `duration_ms` · `valid_until_us` · `flags` (hold-after, interruptible) | One segment. C3 instantiates the profile law. Latest-wins bounded queue. Expiry checked at **execution** |
| `BASE_CANCEL` | → | cue identity · settle / `BRAKE` law | Reject queued segments of that instance; current motion decelerates under `BRAKE` |

**Candidate timeouts (unregistered — Phase A measures, G04/G05 freeze):**

| Quantity | Candidate | Why |
|---|---|---|
| Streamed cruise / follow `cmd_ttl` | **200 ms** | Latest-wins follow; four missed 20 Hz-class frames. Not the head `TRACK` 100 ms |
| Authored one-shot `cmd_ttl` | **`duration_ms + 250 ms`** | Same shape as `HEAD_GOAL` authored segments |
| `HOLD` | Heartbeat-supervised | Must not expire into coast |
| `CC-12C_ARM` expiry | **5 s** plus 0.06 m/s clamp | Short lease; expiry is inhibit, not a coast to the mark |
| Heartbeat timeout | **150 ms** (three missed at 20 Hz) | Same candidate as C0↔C2. `BRAKE` onset within one tick |
| Motion queue depth | **2** | Executing + one successor. Overflow `NACK(QUEUE_FULL)` |

### Feedback and health

| Type | Dir | Payload | Rate (candidate) |
|---|---|---|---|
| `BASE_STATE` | ← | cue identity · `capture_ts_us` · `onset_ts_us` (0 until first motion above criterion) · `progress`; body `v`, `ω`, `x`, `y`, `θ`; per-wheel pos / vel / cur; `ctrl_state`; `mode`; `sensor_valid_mask`; `oldest_sensor_age_ms` | 100 Hz candidate. Yaw is published for the mic-array frame (MEM-20260812-03). **Payload vs 64 B is unregistered:** identity + onset must be counted in the packed layout; if it will not fit, raise max payload — do not drop safety/hazard fields |
| `BASE_HAZARD` | ← | `cliff_mask`; `obst_range_mm`; `bump`; IMU flags (lift / tip / slip); per-channel ages | Event; latched summary while any bit is active. Unknown is representable, never zeroed. ToF, if present, is telemetry and not the sole obstacle bit |
| `BASE_FAULT` | ← | `code`, `detail`, `ts`, `latched` | Event, retransmitted with every `HEARTBEAT` while latched |
| `HEARTBEAT` | ↔ | Same fields as §4.3 | 20 Hz each way on this link (candidate) |
| `ACK` / `NACK` | ← | `for_seq` · `reason` as §4.3 | Per command frame |

### `RP02-P4-REG-02` — 2026-09-18

Registers the C0↔C3 **definition** in this section: semantic `BASE_*` types; `CC-12C_ARM` as a separate nonce; expiry at execution; latest-wins bounded queue; fresh-arm after inhibit; unknown sensor is inhibit; E-stop / cutoff release does not resume. It does **not** register byte layouts, type numbers, baud, the candidate TTL/heartbeat/queue numbers above, firmware, a gate outcome or ADR closure. A prototype codec must declare its layout revision and cannot be scored as this registration.

The generated C3 board-role header from pin map v0.1 lives at `phase-a/c3_board_role.h`. It is a `CA-14` config-source start from v0.1, not a carrier freeze.

## v0.6 — coordination semantics (`RP02-P4-REG-03`, 2026-09-21)

Disposes RP-04 `interface-requirements.md` IR-01, IR-02, IR-03, IR-05, IR-07, IR-08 (motion onset stamp), and the command-reject subset of IR-09. UART, COBS/CRC, session/expiry/heartbeat, and the 64-byte payload *candidate* are unchanged (`CA-05`).

| Accepted on the wire | Not a wire change |
|---|---|
| Cue identity on head/base/face/light commands, cancels, state, ACK, and reports | C0 audio onset (IR-06) — `makad-audio` logs only |
| `start_at_us` on `HEAD_GOAL` / `BASE_GOAL` / `FACE_STATE` / `LIGHT_STATE` | Composer availability snapshot (IR-10) |
| `FACE_REPORT` / `LIGHT_REPORT` source onset | Byte layouts, type numbers, lateness-window milliseconds |
| `NACK` values `TIME_MODEL_INVALID`, `LATE`, `STALE_EPOCH` in the existing `u8` | `PROGRESS_STUCK` as NACK — stays `FAULT`/state. Unavailable/degraded stay `HEARTBEAT.health` |

### `RP02-P4-REG-03` — 2026-09-21

Registers the **semantics** in this revision. It does **not** register packed widths, type numbers, baud, the lateness window, `BASE_STATE` packed size, firmware, a gate outcome or ADR closure. Exploratory codecs must bump layout revision before they carry these fields on the bench.

Exploratory host layout **revision 2** (`phase-a/schema.json`, `phase-a/payloads.py`, 2026-09-21) assigns candidate type IDs (`FACE_REPORT=16` … `CC_12C_ARM=26`), cue-identity packing `perf_id:u16 · perf_epoch:u32 · cue_id:u8`, `NACK` reasons `TIME_MODEL_INVALID=9`, `LATE=10`, `STALE_EPOCH=11`, and a 62-byte `BASE_STATE` that keeps identity, `onset_ts_us`, `ctrl_state`, `mode`, `sensor_valid_mask`, and `oldest_sensor_age_ms`. It fits the 64-byte payload candidate without dropping safety fields. The lateness-window millisecond value remains unregistered. This revision is `EXP_ONLY_NOT_REGISTERED` and cannot be scored as `RP02-P4-REG-03`.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-08 | 0.1 | First draft: transports, COBS+CRC-16 framing, message set across session/command/feedback/time, watchdog and recovery semantics, bandwidth estimate, candidate timing requirements for G05. No field layout frozen; nothing registered. |
| 2026-09-12 | 0.2 | Added the complete offset/rate/reference/uncertainty model to TIME_SYNC_REQ so C2 can perform the conversion required by timebase v0.2. Corrected heartbeat failure semantics to BRAKE onset within one tick after timeout; rest completion follows the bounded BRAKE trajectory. Nothing registered. |
| 2026-09-13 | 0.2 | No framing change. Recorded C01 (XC330-M288-T) as the named RP-01 paper candidate implying Dynamixel 2.0 TTL if selected; family remains unselected. |
| 2026-09-14 | 0.2 | No framing change. Recorded the C2-relay alternative for the display link as under consideration (MEM-20260914-01); baseline remains two SBC-originated UART pairs. |
| 2026-09-16 | 0.3 | Registered the C2-relay topology and full-duplex differential SBC↔C2 physical layer under `RP02-P3-REG-01`; direct TTL became bench-only and USB became service-only. Added relay isolation and C3 inheritance rules. Message framing and candidate timing values remain unvalidated. |
| 2026-09-16 | 0.4 | Cost-down sourcing review replaced the MAX3490E implementation lead with THVD1451D SOIC. The registered differential topology, framing and candidate timing remain unchanged and unvalidated. |
| 2026-09-17 | 0.4 definition baseline | `RP02-P4-REG-01` registered message/recovery semantics while keeping byte layouts, C3 messages, timing numbers and evidence open. Reconciled authorization context with `CA-09`. |
| 2026-09-17 | 0.5 proposal (unregistered) | `BASE_*` draft from RP-03 Part 4; byte layouts still open; not `RP02-P4-REG-02`. Registered C0↔C2 text in §§1–5 unchanged. |
| 2026-09-18 | 0.5 semantics registered | `RP02-P4-REG-02` accepts C0↔C3 `BASE_*` types, `CC-12C_ARM`, expiry/fresh-arm/unknown-is-inhibit. Candidate TTL/heartbeat/queue named and kept unregistered. Byte layouts still open. C0↔C2 `RP02-P4-REG-01` unchanged. |
| 2026-09-21 | 0.6 semantics registered | `RP02-P4-REG-03` accepts cue identity, optional `start_at_us`, `FACE_REPORT`/`LIGHT_REPORT`, and `NACK` `TIME_MODEL_INVALID`/`LATE`/`STALE_EPOCH`. No transport change. Byte layouts still open. |
| 2026-09-21 | 0.6 exploratory layout 2 | Host codec bumped to layout revision 2. Candidate widths/type IDs and `BASE_STATE` 62-byte pack live in `phase-a/`. Not a new Part-4 registration. Lateness ms still open. |
