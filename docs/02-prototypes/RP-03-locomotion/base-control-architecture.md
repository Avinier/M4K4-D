# RP-03 Part 4 — Base Control Architecture

| Field | Value |
|---|---|
| Status | **Design definition v0.2.** Rules `BC-01…BC-10` and pin map v0.1 are written against Espressif ESP32-S3-DevKitC-1-N8. Candidate `cmd_ttl` / heartbeat / queue depth named 2026-09-18 and **unregistered**. Byte layouts, message type numbers and baud remain **OPEN**. `BASE_*` semantics are accepted by RP-02 as `RP02-P4-REG-02`; they are not a byte-layout freeze |
| Owner | Project builder |
| Created | 2026-09-17 |
| Consumes | `intent.md`; `storyboard.md` profile library; `physics.md` §6 latency / §7 coverage and the `a_tip` RANGE; RP-02 `compute-control-architecture.md` `CA-03/11/12/14` and §3 I/O; RP-02 `link-contract.md` v0.4 envelope (`RP02-P4-REG-01`); RP-02 `state-register.md` `OM-01/02/03`, `SD-03`, `CC-12C` |
| Closes at design level | C3 loop ownership, hazard-fusion policy, `CA-11` as concrete state, local mode/arm/expiry/readiness, pin map v0.1 against the I/O budget, `BASE_*` message-set *draft* |
| Does not close | ADR-03/ADR-07; motor/driver/sensor SKU; carrier schematic; watchdog window; byte layouts; numeric TTL/heartbeat/age bounds; G05 evidence; purchase |

Part 4 does not ask which HAT has the most pins. It asks **which loop is allowed to decide what, what survives when C0 is silent or lying, and what GPIO evidence proves that C3 can own the stop path on the selected DevKit without hiding a safety input behind an expander**. This document is the C3 ownership map. `link-contract.md` remains the framing ICD; the power documents remain the rail authority; `physics.md` remains the RANGE, not a compiled target.

## 1. Decision in one view

```text
C0 Raspberry Pi 5  —  semantic BASE_GOAL, BASE_ENABLE, CC-12C_ARM, HEARTBEAT
         |
         +==== full-duplex differential UART (same COBS/CRC/session/expiry envelope)
         |
C3 ESP32-S3-DevKitC-1-N8
   wheel velocity loops @ 500 Hz target
   hazard fusion @ 200 Hz target
   BASE_STATE @ 100 Hz; HEARTBEAT @ 20 Hz
   cliff GPIO · analog-IR obstacle · bump · IMU SPI+INT · encoder PCNT · driver nFAULT
         |
         +-- LEDC PWM + DIR  -->  PB-DRIVE-L / PB-DRIVE-R  (SKU open)
         +-- nSLEEP fail-safe pull-down to inhibit
         +-- WDI to carrier window watchdog
         +-- carrier-qualified C3_READY (not a unique MCU GPIO)

E-stop + ENERGY_OK + MOTOR_PRESENT + C2_READY + C3_READY + SYSTEM_ARM -> hardware motor gate
```

C3 is the only owner of base PWM/direction, encoder capture, local hazard fusion and the acceleration/velocity envelope (`CA-02`, `CA-03`). C0 emits semantic, expiring goals. Following, person choice and path intent stay on C0; they never enter a motor-current or hazard-stop loop (`CA-01`).

The prototype board is DevKitC-1-N8 because C3 needs no PSRAM and the N8 module preserves GPIO35–37 for IMU SPI (`CA-03`, `RP02-P3-REG-02`). N8R8 is not a silent substitute. A later WROOM-1-N8 carrier is a packaging change, not an architecture change, provided it preserves firmware, pins by logical role, external watchdog, debug access and qualification results.

## 2. Architecture rules (`BC-*`)

### `BC-01` — Wheel loops

C3 runs an independent **velocity loop per wheel**. The storyboard profile library is the feed-forward: `LAUNCH`, `CRUISE`, `DECEL0`, `PIVOT`, `ARC`, `SPIN`, `WIGGLE`, `BRAKE`, `HOLD`. C0 names a profile and a body-frame `(v, ω)` segment; C3 instantiates the shaped stroke. The SBC never streams PWM, joint increments or unnamed trapezoids.

Encoder capture is on the ESP32-S3 **PCNT** units (quadrature A/B, left and right). The wheel-loop design rate is **500 Hz target** (`CA-12`). Motor-driver and encoder evidence may revise the rate upward or downward; the ≤ 50 ms detection-to-deceleration invariant does not move (`physics.md` §6 scores with `t_latency = 50 ms`, not the 35 ms paper sum).

Zero-velocity `HOLD` is a closed loop at `v*=0`, `ω*=0`, not a coast. It must reject the inherited RP-01 paper yaw peak of 0.1099 N·m (MEM-20260812-08). A body that rolls when the head yaws is a `BC-01` miss, not an RP-04 composition miss.

### `BC-02` — Odometry

C3 publishes timestamped body `v`, `ω`, `x`, `y`, `θ` at **100 Hz** in `BASE_STATE`. `capture_ts_us` is the encoder-read time on C3's clock, converted per `timebase.md` after offset reconciliation.

Yaw is published because body rotation turns the microphone array into a rotating frame (MEM-20260812-03). RP-05 consumes that yaw; C3 does not own beamforming. Wheel odometry is the heading source unless a fusion is explicitly declared under `BC-10`.

### `BC-03` — Hazard fusion

Every safety sensor has a **per-channel age bound**. A sample older than its bound is **unknown**. Unknown is **inhibit**, never “last known good” and never zero.

Stop-path bits, all local to C3, no USB sensor, no GPIO expander:

| Channel | Electrical | Role in the stop path |
|---|---|---|
| Cliff GPIO (`CLIFF_FL/FR/REAR`) | Digital look-down, three channels covering caster-forward, reverse/skid and wheel-adjacent (`physics.md` §7.5) | Coverage bit; any channel absent/stale/implausible inhibits motion that needs that contact |
| Analog IR obstacle | ADC1 | Obstacle envelope bit; look-ahead is screened against `d_stop` at the leading contact, not against a SKU range |
| Bump | Digital | Last layer, not the first; do not close G03 on bump-only at follow speed |
| IMU lift / tip | SPI + interrupt | Pickup and tip bits; rigid base mount |
| Encoder implausible | PCNT vs commanded / vs IMU | Disagreement is a hazard, not a filter to ignore |
| Driver `nFAULT` | Wired-OR input | Hardware fault is inhibit; do not poll it away |

If a ToF module is present on I²C it is **telemetry**. It is never the sole stop-path obstacle bit. Analog IR remaining valid with ToF stale is a degraded exposure, not an automatic inhibit (`F-44`). A ToF that is the only obstacle evidence is an architecture miss, not a firmware workaround.

Hazard scan/fusion design rate is **200 Hz target** (`CA-12`). No single sensor age may silently exceed its bound. Numeric age bounds are OPEN until Phase A measures them.

### `BC-04` — `CA-11` priority as concrete state

C3 holds exactly one active inhibit class. Highest first:

| Rank | Class | Concrete C3 state |
|---|---|---|
| 1 | Hardware E-stop / motor-gate loss | `ESTOP_N` asserted or motor domain absent → driver inhibited, `nSLEEP` inactive, `OM-04` electrically / `OM-03` in firmware after release |
| 2 | Energy or controller-readiness loss | `ENERGY_OK` false, `MOTOR_PRESENT` false, watchdog-not-good, or `C3_READY` withdrawn by the carrier |
| 3 | Cliff, pickup/tip, encoder implausibility, driver fault, registered obstacle envelope | Local `BRAKE` then inhibit; `BASE_HAZARD` / `BASE_FAULT` latched |
| 4 | Command expiry / C0 session loss | Heartbeat or `valid_until_us` fail at execution; queue flushed |
| 5 | Explicit base inhibit / cancel | `BASE_INHIBIT` / `BASE_CANCEL`; settle under `BRAKE` |
| 6 | Valid authored / follow command | `BASE_GOAL` in `OM-01` after `BASE_ENABLE` |
| 7 | Procedural micro-motion | Armed `CC-12C` creep only, in `OM-02`, under `CC-12C_ARM` |

A higher-priority condition clamps, brakes or rejects a lower one. **Clearing a condition reports availability and does not resume old intent.** Queues are already flushed. Resume requires a fresh arm (`BASE_ENABLE` with a new nonce, and a new `BASE_GOAL`; tabletop additionally requires a new `CC-12C_ARM`). Create 3's local reflex/stale-velocity behaviour is the precedent; Makad keeps the stricter fresh-arm rule (`CA-11`).

### `BC-05` — Operating mode is local to C3

`OM-01` Floor, `OM-02` Tabletop inhibited-by-default, and `OM-03` motion inhibited are **latched on C3**. `SD-03` app selection (Floor / Table in the control app) is an **input** to that latch, not the interlock. The app cannot energize motors. Missing or contradictory mode evidence resolves to `OM-03` (`state-register.md` permission invariants).

Boot, reset, C0 link loss, app-link loss (`F-17` / `F-39`) and heartbeat timeout all enter **`OM-03`**. Releasing E-stop, restoring a rail or receiving a delayed ACK never jumps to `OM-01` or `OM-02`. Ordinary come / follow / spin are never granted in `OM-02`. The only `OM-02` motion is the separately armed `CC-12C` case (`BC-06`).

### `BC-06` — `CC-12C` calibration arming

Tabletop calibration is a **separate nonce** with its **own expiry** and a **speed clamp to `BM-11` 0.06 m/s**. `BASE_ENABLE` does not imply `CC-12C_ARM`. `CC-12C_ARM` never grants come, follow or spin.

Unarmed `OM-02` is **drive-off**: `nSLEEP` inactive, wheel commands held at inhibit, `BASE_GOAL` with any locomotion profile `NACK(INHIBITED)`. An expired calibration arm is inhibit, not a slow coast to the mark (`F-43`). The caught fixture and CON-TBD-14 footprint are G04/G04-freeze items; C3 enforces the speed clamp and edge inhibit regardless of whether BD-01 later removes moving tabletop from V1.

### `BC-07` — Command expiry and bounded queues

Expiry is evaluated at **execution**, not at receipt — same rule as `HEAD_GOAL`. `now_master_us > valid_until_us` → discard with `NACK(EXPIRED)`.

The motion queue is **latest-wins** and **fixed-capacity**. There is no unbounded FIFO in the wheel path (`CA-12`). Overflow → `NACK(QUEUE_FULL)`. A goal that arrives while inhibited, unarmed, or in the wrong mode → `NACK(INHIBITED)`. The reason set mirrors `HEAD_*`: `OK` / `EXPIRED` / `OUT_OF_LIMITS` / `INHIBITED` / `UNKNOWN_TYPE` / `BAD_CRC` / `QUEUE_FULL` / `NO_LIMITS` / `NONCE_REPLAY`.

Numeric `cmd_ttl`, heartbeat timeout and queue depth are **candidates** (2026-09-18). They stay **unregistered** until Phase A measures them. They are no longer "unanswered."

| Quantity | Candidate | Why this number | Registered? |
|---|---|---|---|
| `BASE_GOAL` `cmd_ttl` for streamed cruise / follow | **200 ms** | Latest-wins follow is a 20 Hz-class stream. 200 ms is four missed frames, analogous to the head `TRACK` 100 ms but slower because a base cruise is not a 7° laugh pulse | No |
| `BASE_GOAL` `cmd_ttl` for authored one-shot (`PIVOT`, `SPIN`, `WIGGLE`, come step, `BRAKE`) | **`duration_ms + 250 ms`** | Same shape as `HEAD_GOAL` authored segments | No |
| `HOLD` | Heartbeat-supervised, not a short TTL | A still body must not expire into coast. Heartbeat loss already `BRAKE`s (`BC-04` rank 4) | No |
| `CC-12C_ARM` expiry | **5 s** candidate, plus the speed clamp 0.06 m/s | Tabletop arm is a short lease. Expiry is inhibit, not a slow coast to the mark (`F-43`) | No |
| Heartbeat timeout | **150 ms** (three missed at 20 Hz) | Same candidate as C0↔C2. `BRAKE` onset within one tick after timeout; rest follows the bounded `BRAKE` | No |
| Motion queue depth | **2** | One executing segment + one pre-empting successor. Overflow → `NACK(QUEUE_FULL)`. Not an unbounded FIFO | No |

C3 does not inherit the head numbers as registered. Soft `cmd_ttl` in `BASE_LIMITS_SET` may only **tighten** the compiled candidate. A prototype codec must declare the revision; it cannot be scored as this contract.

### `BC-08` — Readiness

C3 readiness is the **AND** of:

1. external window-watchdog good (feed is `WDI`; qualified READY is a **carrier** function — `CA-10`, §3 I/O);
2. driver present (`MOTOR_PRESENT` independent of `ENERGY_OK`, per PA);
3. sensors valid (every stop-path channel inside its age bound; unknown is not valid);
4. mode valid (`OM-01` or armed `OM-02`; else `OM-03`).

Any term false withdraws motion permission. **Fresh-arm is required after any inhibit.** Restoring a sensor, a rail, a heartbeat or a watchdog output reports availability; it does not re-enable.

`C3_READY` is not a raw MCU GPIO-high. The carrier ANDs watchdog-good with the other hardware-qualification terms and pulls inactive when C3 is unpowered, resetting or disconnected. Debuggers that disable ESP-IDF watchdogs do not disable the external device.

### `BC-09` — Accel / vel envelope

Two limit layers (`CA-14`):

- **Compiled hard maxima** live in C3 firmware generated from the versioned config source. Soft limits in `BASE_LIMITS_SET` **may only tighten** those maxima. A hash mismatch blocks arm.
- Hard `a_max` is compiled from the `physics.md` `a_tip` **RANGE**, not from the 2.0 m/s² placement target. The 2.0 m/s² figure is a CoM-placement target, not a mass-roll-up result, and is not a compiled limit.

Until CoM is measured, the conservative compiled default is **`a_max` ≤ 0.80 m/s²** (storyboard minimum-viable `a_peak`). That default is change-controlled when ballast proves `x_CoM`. RP-03 does not quietly raise compiled acceleration toward 2.0 because a concept only exists at the placement target, and does not quietly shrink a measured-CoM envelope to hide a miss — the RANGE moves by baseline revision.

Follow ≤ 0.5 m/s cannot be weakened (CON-19). Soft limits may set a lower follow cap; they may not raise it. Yaw `wmax` soft-limits the storyboard bands; 300 °/s is drivetrain headroom and is never a commanded rate.

### `BC-10` — IMU

The base IMU is **SPI + interrupt**, rigidly mounted to the base, capture timestamped at the interrupt. It is used for **slip, lift, tip and odometry-failure** detection.

It is **not** a heading-gyro substitute for wheel odometry unless a fusion is declared, versioned in the config source and reported in `HELLO`. Head-mounting the IMU is excluded (MEM-20260812-02). Absence of a declared fusion means `BASE_STATE.θ` is wheel odometry and IMU flags are hazard bits only.

BD-03 (runtime IMU vs bench instrument) is still a builder decision. This pin map **reserves** the SPI+INT interface so a later runtime installation is not a pin-map break. Removing the IMU from the stop path is a change-controlled `BC-03` revision, not a silent SKU drop.

## 3. Pin map v0.1 — ESP32-S3-DevKitC-1-N8

v0.1 is a **pre-carrier gate** against `compute-control-architecture.md` §3. It is not a freeze of driver or sensor SKUs. Failing the map moves to a WROOM-1-N8 carrier or changes the interface through change control; it never falls back to N8R8.

### 3.1 Reservations (inherited)

| GPIO | Rule |
|---|---|
| 0, 45, 46 | Strapping. **No safety OUTPUTS.** Left unassigned |
| 3 | Strapping. **No safety OUTPUTS.** Documented **input-only exception** for `ESTOP_N` (see §3.3) |
| 19, 20 | Native USB. Reserved |
| 43, 44 | USB-UART. Reserved for C3 service access in the body (`CA-15`) |
| Board RGB LED on 48 | **Released.** The DevKit LED is not retained, so GPIO48 is available as `WDI`. Assignable header count is therefore 28, not 27 |
| 35, 36, 37 | Preserved by the N8 module (not N8R8). Assigned to IMU SPI |

N8 DevKitC exposes 36 header GPIO before reservations. Avoiding strapping GPIO0/3/45/46 for safety-critical *outputs* and reserving GPIO19/20 plus GPIO43/44 leaves **28 ordinarily assignable** header GPIO once the RGB LED is released. Safety-critical inputs are not placed behind a GPIO expander.

### 3.2 Assignment

| Signal | GPIO | Peripheral | Direction | Notes |
|---|---:|---|---|---|
| `ENC_L_A` | 4 | PCNT | Input | Quadrature left A |
| `ENC_L_B` | 5 | PCNT | Input | Quadrature left B |
| `ENC_R_A` | 6 | PCNT | Input | Quadrature right A |
| `ENC_R_B` | 7 | PCNT | Input | Quadrature right B |
| `PWM_L` | 11 | LEDC | Output | Left motor command |
| `PWM_R` | 12 | LEDC | Output | Right motor command |
| `DIR_L` | 13 | GPIO | Output | Left direction / PH |
| `DIR_R` | 14 | GPIO | Output | Right direction / PH |
| `nSLEEP` / ENABLE | 21 | GPIO | Output | Fail-safe **pull-down to inhibit**; inactive at reset |
| `nFAULT` | 9 | GPIO | Input | Wired-OR driver fault |
| `CLIFF_FL` | 15 | GPIO | Input | Caster-forward look-down |
| `CLIFF_FR` | 16 | GPIO | Input | Wheel-adjacent / second forward look-down |
| `CLIFF_REAR` | 8 | GPIO | Input | Reverse / skid look-down |
| `OBST_IR` | 1 | ADC1 | Analog in | Stop-path obstacle. Not ToF |
| `BUMP` | 47 | GPIO | Input | Last-layer contact |
| `ESTOP_N` | 3 | GPIO | Input | See §3.3 |
| `ENERGY_OK` | 39 | GPIO | Input | Independent of motor-present |
| `MOTOR_PRESENT` | 40 | GPIO | Input | Independent of `ENERGY_OK` (PA). Not merged onto the energy sense |
| `IMU_MOSI` | 35 | SPI | Output | Base IMU |
| `IMU_MISO` | 36 | SPI | Input | |
| `IMU_SCLK` | 37 | SPI | Output | |
| `IMU_CS` | 41 | GPIO | Output | |
| `IMU_INT` | 42 | GPIO | Input | Capture timestamp at interrupt |
| C0 UART1 TX | 17 | UART1 | Output | Behind differential transceiver; TTL is bench-only |
| C0 UART1 RX | 18 | UART1 | Input | |
| `WDI` | 48 | GPIO | Output | Window-watchdog feed; edge after one complete healthy safety-loop cycle |

**26 MCU GPIO used.** `C3_READY` is **not** a unique MCU pin: the carrier generates the hardware-qualified READY from `WDI` plus the other qualification terms (`CA-10`; §3 I/O “READY / watchdog feed / debug are carrier functions”). Dropping a dedicated `C3_READY` GPIO is what keeps two-plus safe spares on this DevKit.

**ISENSE is not on the MCU in v0.1.** Driver current is a Phase B instrument (INA on the rig) until a spare is committed. A later DRV8874-class `IPROPI` may land on spare GPIO2 or GPIO10 through change control; it does not steal a stop-path pin to make the count look comfortable.

### 3.3 GPIO3 `ESTOP_N` — input-only strapping exception

GPIO3 is a strapping pin. `CA` §3 excludes GPIO0/3/45/46 from **safety-critical outputs**. Using GPIO3 as `ESTOP_N` **input** is the documented exception that frees GPIO38 as a spare. Firmware treats it as input-only for the life of this map: no output drive, no nSLEEP/PWM/DIR/WDI alias, no accidental output configuration in boot or panic paths. GPIO0/45/46 remain unused.

### 3.4 Spare and budget proof

Assignable header GPIO with RGB released: **28** (strapping 0/3/45/46 and USB 19/20/43/44 excluded).

| Bucket | GPIOs | Count |
|---|---|---:|
| Used from the 28 assignable | 1, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 21, 35, 36, 37, 39, 40, 41, 42, 47, 48 | 25 |
| Used from strapping as input exception | 3 (`ESTOP_N`) | 1 |
| **MCU GPIO used** | | **26** |
| Safe unassigned (assignable, not USB, not strapping, not WDI) | **2, 10, 38** | **3** |

The pre-carrier gate is **≥ 2 unassigned safe GPIO** after all direct safety inputs, watchdog and debug reservations. v0.1 retains **three**: GPIO2, GPIO10, GPIO38. GPIO46 remains unused strapping and is not counted as a spare.

If a future SKU requires `IPROPI`, a second analog obstacle, or a ToF reset line, it consumes a named spare through change control and re-proves the ≥ 2 rule. It does not reclaim GPIO48 from `WDI` or hide the new input behind an expander.

## 4. `BASE_*` message-set draft

Same envelope as the registered C0↔C2 contract: **COBS**, **CRC-16/CCITT**, session (C0 boot identity + epoch + C3 boot challenge), `src_ts_us`, explicit expiry, fresh-arm nonce. Physical layer is the independent C0↔C3 differential UART (`CA-05`).

This is a **draft**. Byte layouts, field widths, type numbers, baud and numeric timeouts are **not registered**. RP-02 `link-contract.md` carries the same text as a v0.5 **proposal**; `RP02-P4-REG-02` is not issued. C3 controller selection (`RP02-P3-REG-01/02`) does not define drive messages.

`HELLO`, `HEARTBEAT`, `TIME_SYNC_REQ` / `TIME_SYNC_RESP`, and `ACK` / `NACK` are the same types as the head link, on this independent session. `ACK` / `NACK` reasons are the `HEAD_*` set (`BC-07`).

Types below are grouped like `HEAD_*`. `→` C0 to C3; `←` C3 to C0. Payload columns name semantics, not wire widths.

### 4.1 Session and authorization

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `BASE_LIMITS_SET` | → | Per wheel: `vmin`, `vmax`, `amax`, `imax`; yaw `wmax`; `cmd_ttl`; `heartbeat_timeout` | Must be acknowledged before `BASE_ENABLE`. Values are clamped to C3's compiled hard maxima (`BC-09` / `CA-14`); the clamped set is echoed in the `ACK` |
| `BASE_ENABLE` | → | Fresh arm nonce | `inhibited → enabled` **only if** limits are set, heartbeat is fresh, no fault is latched, motor domain is present, and mode is valid (`OM-01`, or `OM-02` which still does not grant locomotion). Bound to the current C3 boot challenge, C0 boot identity and epoch. Does **not** grant `CC-12C` |
| `BASE_INHIBIT` | → | `reason` | Initiate `BRAKE` immediately, then `OM-03` / inhibited when the bounded trajectory reaches rest. Idempotent |
| `CC-12C_ARM` | → | Separate nonce + expiry + speed clamp | Arms minimum-speed calibration motion in `OM-02` only. Clamp is `BM-11` 0.06 m/s. Never implied by `BASE_ENABLE`. Never grants come / follow / spin. Expiry at execution |

### 4.2 Commands (bounded, expiring)

| Type | Dir | Payload | Semantics |
|---|---|---|---|
| `BASE_GOAL` | → | `profile_id` (`LAUNCH` / `CRUISE` / `DECEL0` / `PIVOT` / `ARC` / `SPIN` / `WIGGLE` / `BRAKE` / `HOLD`) · `v`, `ω` · `duration_ms` · `valid_until_us` · `flags` (hold-after, interruptible) | **One segment.** C3 instantiates the profile law; C0 never streams intermediate wheel points. Latest-wins if a newer valid goal arrives (`BC-07`) |
| `BASE_CANCEL` | → | settle / `BRAKE` law | Reject queued segments; current motion decelerates under `BRAKE`. `BM-12` analogue of `HEAD_CANCEL` |

**Expiry rule.** C3 evaluates `now_master_us > valid_until_us` at *execution*. Expired command → `NACK(EXPIRED)`. A burst after reconnect is rejected frame by frame. Candidate TTLs (2026-09-18, **unregistered**): streamed cruise/follow **200 ms**; authored one-shot **`duration_ms + 250 ms`**; `HOLD` is heartbeat-supervised; queue depth **2**; heartbeat timeout **150 ms**. Head candidates in `link-contract.md` §4.2 are not imported as registered C3 numbers.

### 4.3 Feedback and health

| Type | Dir | Payload | Rate (candidate) |
|---|---|---|---|
| `BASE_STATE` | ← | `capture_ts_us`; body `v`, `ω`, `x`, `y`, `θ`; per-wheel pos / vel / cur; `ctrl_state` (`inhibited` / `enabled` / `braking` / `fault`); `mode` (`OM-01/02/03`); `sensor_valid_mask`; `oldest_sensor_age_ms` | 100 Hz. Yaw is the mic-array frame (`BC-02`) |
| `BASE_HAZARD` | ← | `cliff_mask`; `obst_range_mm`; `bump`; IMU flags (lift / tip / slip); per-channel ages | Event, and latched summary with heartbeat while any bit is active. Unknown channels are represented, never zeroed |
| `BASE_FAULT` | ← | `code`, `detail`, `ts`, `latched` | Event, retransmitted with every `HEARTBEAT` while latched. Codes include the `HEAD_*` set plus base-named `F-31…` identities when those rows fire |
| `HEARTBEAT` | ↔ | Same fields as the head contract | 20 Hz each way, this link |
| `ACK` / `NACK` | ← | `for_seq` · `reason` as `HEAD_*` | Per command frame |

A missing field means unknown, not zero. Health is an enum, never a boolean.

## 5. Rates inherited, not re-registered

| Function | Design rate | Deadline rule | Source |
|---|---:|---|---|
| Wheel control | 500 Hz target | Evidence may revise; ≤ 50 ms detection-to-deceleration stays | `CA-12`; `physics.md` §6 |
| Hazard scan / fusion | 200 Hz target | No sensor age silently past its bound | `CA-12`; `BC-03` |
| `BASE_STATE` | 100 Hz | `capture_ts_us` at encoder read | `CA-12`; `BC-02` |
| `HEARTBEAT` | 20 Hz | Faults transmit immediately and remain latched | `CA-12`; envelope |
| Watchdog window | OPEN | Registered from measured worst-case loop time, not a round number | `CA-10` |

Paper latency sum in `physics.md` §6.1 is 35 ms `E`. Scoring uses **50 ms**. A later measured sum that exceeds 50 ms changes the sensing or the loop, not the invariant.

## 6. What is fixed here and what remains evidence-gated

**Written by this file (design definition, not a Part-4 registration until the builder issues `RP03-P4-REG-01`):** `BC-01…BC-10`; pin map v0.1 against DevKitC-1-N8 with three safe spares; `BASE_*` draft in the registered envelope; `CC-12C_ARM` as a separate nonce; unknown-is-inhibit; fresh-arm after every inhibit; compiled `a_max` default ≤ 0.80 m/s² until measured CoM.

**Still open without weakening the rules:** driver and sensor SKUs; `IPROPI` / ISENSE landing; ToF as optional telemetry; exact RS-422 suffix on this link (implementation lead remains THVD1451D); external-watchdog suffix/window/latch; byte layouts and type numbers; **measured** TTL/heartbeat/sensor-age and watchdog windows (candidates exist, 2026-09-18); G05 / RP02-G05 C3 loop-jitter evidence; purchase.

**Owned elsewhere — link, do not copy:** C0↔C2 registered message set (`RP02-P4-REG-01`); C0↔C3 `BASE_*` semantics (`RP02-P4-REG-02`); `PA-13` motor-domain authority; `OM/CC/LP` vocabulary; `F-19/F-22/F-26` text (cross-listed in `fault-matrix.md`); coverage millimetres (`physics.md` §7).

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-17 | 0.1 | First draft: `BC-01…BC-10`, DevKitC-1-N8 pin map v0.1 (RGB released; `C3_READY` carrier-qualified; GPIO3 ESTOP input exception; three safe spares), `BASE_*` message-set draft in the RP-02 envelope. Byte layouts, SKUs and numeric timeouts open. Not a registration. |
| 2026-09-18 | 0.2 | Candidate `cmd_ttl` / heartbeat / queue depth named and kept unregistered. Cutoff-coast pointed at G01/G05 (`BM-14`). CA-14 board-role header generated from pin map v0.1. `RP02-P4-REG-02` accepts v0.5 semantics. |
