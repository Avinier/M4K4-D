# RP-03 Fault-Injection Matrix

| Field | Value |
|---|---|
| Status | **v0.2 design definition.** Rows `F-31…F-45` are written in the RP-02 schema. `F-19`, `F-22` and `F-26` are cross-listed, not renumbered and not restated as RP-03-owned text. `BM-14` cutoff-coast is a G01 metric paired with `F-41`; it is not a `BRAKE` fail. No injection performed. Candidate G05 metrics are **not registered** |
| Owner | Project builder |
| Created | 2026-09-17 |
| Authority | `intent.md`; `base-control-architecture.md` `BC-01…10`; RP-02 `fault-matrix.md` schema and `F-19/F-22/F-26`; RP-02 `state-register.md` `OM-01/02/03`, `CC-12C`; `gates.md` G05 (candidate) |
| Required behaviours | System-design-brief §6 failure priorities; RP-02 `link-contract.md` §5 recovery grammar applied to `BASE_*`; `BC-04` fresh-arm |
| Success criteria | SC-15 controlled stop and failure; SC-12 obstacle handling; SC-13 tabletop protection |
| Feeds | RP-03 G05; ADR-07; RP-02 G04 on the inherited rows |

G05 requires four things of every injected fault, separately observable: **inhibit** the affected hazardous output, **reject obsolete** commands, **expose health** state, and **recover only from current authorized intent**. A base that brakes correctly and then resumes the interrupted follow on reconnect fails G05 the same way a head that resumes a gesture fails G04.

Inherited rows `F-19`, `F-22` and `F-26` remain owned by RP-02. This file adds the RP-03 injection method and the C3 observables. It does not issue a new ID for those faults.

## 1. Rules

1. **One fault at a time**, injected into a registered `CC-xx` case named in the row. The state vector supplies the hazard; the fault supplies the trigger.
2. **Every row names its injection method** and it must be reproducible on the RP-03 rig without special equipment beyond `rig.md`.
3. **Observables are logged, not watched.** Time-to-inhibit is measured from the injection timestamp to the first `BRAKE` sample in `BASE_STATE` / encoder trace, on the common timebase.
4. **Failed injections stay in the record.** A fault that produced unbounded wheel motion or an uncaught tabletop departure is the most valuable run RP-03 can produce.
5. **IDs are append-only.** `F-19/F-22/F-26` are never reused or renumbered here. `F-31…` are never reused.
6. **Unknown is inhibit** for stop-path channels (`BC-03`). ToF telemetry stale is the explicit exception (`F-44`): expose, do not inhibit on ToF alone while analog IR remains valid.
7. **No uncaught tabletop trial.** Caught-tabletop rows run last, and only after the catch fixture is verified.

## 2. Matrix

Columns: **Inhibit** — what must stop and by when (candidate). **Reject** — which obsolete commands must be refused. **Expose** — what the health/fault channel must show. **Recover** — the only permitted path back. **Evidence** — the logged observables that prove it.

### 2.1 Cross-listed from RP-02 (do not renumber)

Full inhibit / reject / expose / recover text lives in RP-02 `fault-matrix.md`. Each row below points at that text and names the RP-03 method and observables.

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-19** | Obstacle/edge safety sensor absent, stale or implausible | `CC-10C` floor obstacle and `CC-12C` caught tabletop edge | RP-02 text. RP-03 method: unplug one cliff or analog-IR channel at the interposer before boot; mask/freeze its update in firmware; inject out-of-range samples through the interposer. Per-channel splits are `F-31`/`F-32` | As RP-02: any motion requiring the missing coverage is inhibited or locally braked; other safe channels may remain | As RP-02 | As RP-02: named sensor/coverage `HL-03/04` plus reason and age. C3 also sets the corresponding `sensor_valid_mask` bit false and publishes age in `BASE_HAZARD` | As RP-02: restore valid evidence; remain inhibited until local readiness and a fresh action/enable | As RP-02, plus `BASE_HAZARD` ages, `BASE_STATE.sensor_valid_mask`, encoder trace, zero continuation into the uncovered region |
| **F-22** | Base-controller restart during motion | `CC-09/09C` and `CC-10A/B` | RP-02 text. RP-03 method: reset or task-watchdog stall C3 on this rig while C0 and C2 remain alive; replay the pre-reset `HELLO`/limits/`BASE_ENABLE` | As RP-02: driver hardware-safe; `nSLEEP` inactive; no stale wheel command after reboot | As RP-02: pre-reset wheel goals and the active follow/come instance | As RP-02: reset reason and unavailable/unsafe. C3 `HELLO` with reset reason; `BASE_FAULT` latched | As RP-02: handshake/limits/readiness → `OM-03`; new Floor selection/`BASE_ENABLE` and a new action instance | As RP-02, plus `nSLEEP`/PWM line trace, PCNT frozen-or-safe, zero post-reset wheel motion before fresh authorization |
| **F-26** | C3 external watchdog violation | `CC-09/10A` | RP-02 text. RP-03 method: stop the qualified `WDI` feed; separately generate an early feed outside the allowed window on the base carrier during motion | As RP-02: carrier-qualified `C3_READY` withdraws; driver safe within the (unregistered) bound | As RP-02: current and queued wheel intent | As RP-02: watchdog/reset cause and base unavailable/unsafe | As RP-02: C3 safe boot; fresh mode/handshake/arm/action | As RP-02: `WDI`/`WDO`/`C3_READY`/driver-enable and encoder trace. MCU GPIO map v0.1 has no dedicated READY pin; READY is the carrier output |

### 2.2 Stop-path sensors and drivetrain (bench-capable)

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-31** | Cliff channel absent, stale or implausible (per channel) | `CC-10C`; later `CC-12C` on the caught table | Unplug `CLIFF_FL` / `CLIFF_FR` / `CLIFF_REAR` one at a time at the interposer; freeze that channel's sample; inject a stuck-valid floor while the rig is walked off a marked edge replica on the bench (no live desk) | Motion that needs that leading contact inhibits or locally brakes. Other cliff channels remain. Unknown is inhibit (`BC-03`). One missing rear channel does not license reverse | `BASE_GOAL` whose coverage preconditions fail → `NACK(INHIBITED)` | `BASE_HAZARD.cliff_mask` + per-channel age; `BASE_FAULT` with channel id; `sensor_valid_mask` bit clear | Restore that channel; remain inhibited until readiness AND fresh `BASE_ENABLE` / action | Per-channel age log; which GPIO; detection-to-`BRAKE`; zero travel into the uncovered heading |
| **F-32** | Analog-IR obstacle absent, stale or implausible | `CC-10C` at registered approach speed | Unplug `OBST_IR`; hold ADC at rail or at a frozen mid-scale; inject an implausible step through the interposer | Obstacle-requiring motion inhibits or brakes. Cliff/bump remain. Do not substitute ToF | Goals that need the obstacle envelope → `NACK(INHIBITED)` | `obst_range_mm` unknown (not zero); age; `BASE_FAULT` | Restore valid analog IR; fresh arm | ADC/age log; brake onset; zero harmful contact with the registered prop |
| **F-33** | Bump stuck or open | `CC-10C` and idle `OM-01 + BS-01` | Short `BUMP` asserted; open the input; freeze asserted through the interposer | Stuck-asserted: treat as contact → `BRAKE`/inhibit. Open/stale: unknown → inhibit. Bump is last layer; this row does not waive `F-32` | New locomotion goals while the channel is invalid | Bump bit + age; stuck vs open distinguished in `detail` | Restore; remain inhibited; fresh arm | GPIO trace; no follow continuation into a stuck-assert; no ignore of open |
| **F-34** | Encoder disagreement L vs R vs IMU | `CC-09` cruise and `CC-11` spin on a stand, then guarded floor | Unplug one encoder; swap A/B on one wheel; hold PCNT; command a spin while IMU reports near-zero yaw (stand, wheels on) | Implausible odometry is a rank-3 hazard (`BC-04`): `BRAKE` then inhibit. Do not silently retarget from the “good” wheel | In-flight `BASE_GOAL`; follow/spin instance | Encoder/IMU disagreement flags in `BASE_HAZARD`; `BASE_FAULT`; `θ` health degraded/unavailable | Restore sensing; `OM-03`; fresh enable; new goal. Do not resume the spin | PCNT both wheels, IMU yaw, commanded `(v,ω)`, zero continued heading walk |
| **F-35** | Driver `nFAULT` / overcurrent | `LP-04-STEADY` on a stand; then `CC-10A` guarded | Assert `nFAULT` at GPIO9 (wired-OR); separately trip the evaluation-board OC / force a short within fixture limits on one channel | `nSLEEP` inactive; both wheels safe (wired-OR is one pin — do not keep the other wheel live) | Current and queued wheel goals | `BASE_FAULT` driver/nFAULT; motor-domain or driver-health unavailable | Clear the driver; remain inhibited; fresh `BASE_ENABLE` | `nFAULT`/`nSLEEP`/PWM/current (rig INA); zero post-fault PWM |
| **F-36** | Stall / blocked wheel | `LP-04-BLOCKEDREF` on a stand; `CC-09` guarded floor with a registered block | Lock one wheel against a fixture; separately raise rolling resistance past the registered stall proxy | Local `BRAKE`/inhibit within the (unregistered) bound; do not thermal-walk the driver | New launch/follow goals | Stall/blocked `BASE_FAULT`; current telemetry when the instrument exists | Remove the block; fresh arm. Do not resume the follow | Wheel vel vs command, current, time-to-inhibit; `LP-04-BLOCKEDREF` waveform id |
| **F-37** | Pickup / tip (IMU) | Guarded `CC-09`; bench tilt fixture first | Lift the rig at the shell; separately tilt past the (unregistered) tip proxy on a fixture with IMU mounted rigid to the base | Rank-3: `BRAKE`/inhibit. Wheels must not assist a carry | Come/follow/spin | IMU lift/tip flags + interrupt timestamp; `BASE_HAZARD` | Set down / level; remain inhibited; fresh arm | IMU INT timestamp vs `BRAKE`; encoder after lift = 0 commanded |
| **F-44** | ToF telemetry stale | `CC-10C` with analog IR still valid | Freeze or unplug the I²C ToF while `OBST_IR` continues to update inside its age bound | **Must not** be the only inhibit. Analog IR valid → obstacle stop-path remains that channel. If analog IR is *also* invalid, `F-32` owns inhibit | None on ToF-stale alone | ToF age/unavailable in telemetry; health `degraded`; not a stop-path `BASE_FAULT` that implies analog IR failed | Restore ToF; no re-arm required for this row alone | Analog-IR age stays valid; ToF age climbs; zero inhibit attributed only to ToF; G03 still uses analog IR |
| **F-45** | `BASE_GOAL` flood | `OM-01 + BS-02` attentive idle, then `CC-09` | C0 sends `BASE_GOAL` at a flood rate (F-14 analogue; candidate 2 kHz) | No motion artefact: current segment remains clean; C3 `NACK(QUEUE_FULL)` | Overflow frames | `degraded`; drop/high-water counter | Rate returns to normal; fresh arm only if a fault latched | Loop-jitter p99; `NACK(QUEUE_FULL)` count; wheel loop still meets `BC-01` |

### 2.3 Mode, link and energy (guarded floor)

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-38** | Mode-evidence loss (OM bit vs app) | `CC-09` Floor; rejection check in `CC-12B` | Contradict C3's latched `OM-01` against the app session (clear the local latch, inject Table while Floor goals continue, or drop mode evidence) | C3 resolves to `OM-03` (`BC-05`). Drive off | Floor locomotion goals; any `CC-12C_ARM` in the wrong mode | Mode-source unavailable; `BASE_STATE.mode = OM-03`; reason names evidence loss | Explicit new Floor/Table selection → readiness → fresh `BASE_ENABLE` → new goal. App selection is not the interlock | Mode bits vs app session; `nSLEEP`; zero motion in the contradiction window |
| **F-39** | App-link loss mid-follow | `CC-09`, then `CC-10B`; rejection in `CC-12B` | Cross-list **F-17**. Close the app / sever its control channel / disable its Wi-Fi while C0↔C3 remains alive | Local authority initiates `EV-12` and `OM-03`. No dependency on a remote stop frame | Current and queued behaviour/motion from the lost session | Mode-source/link health unavailable; reason identifies app-session loss | Reconnect → explicit new Floor selection → local readiness → fresh enable nonce → new behaviour request | Injection-to-brake; mode transition; zero post-reconnect motion before the complete fresh sequence |
| **F-40** | C0 loss mid-follow | `CC-09` / `CC-09C` | Open the C0↔C3 differential pair; separately reboot C0 while C3 and the motor domain remain | Heartbeat timeout → `BRAKE` then `OM-03`; queue flushed (`BC-07`). C3 must not treat C0 boot UART noise as `BASE_ENABLE` | Everything in flight, including old-session `BASE_GOAL` | `FAULT(HB_TIMEOUT)` analogue on this link; `last_rx_age` climbs; base unavailable | Reconnect → `HELLO` → limits → mode → `BASE_ENABLE` → new `BASE_GOAL`. Do not resume follow | Brake onset; outbox depth 0; first post-reconnect frame is `HELLO`; encoder after loss |
| **F-41** | E-stop mid-spin | `CC-11` (and `CC-10A` as F-12 already requires) | Cross-list **F-12/F-13**. Press the mushroom during `BM-06` / `EV-13`; then twist to release. **G01 also scores the same cutoff from straight `v` as `BM-14`**: two distances, commanded `BRAKE` vs cutoff-coast, same course, same ballast | Motor domain dead by hardware; C3 detects absence within one tick; `OM-04` electrically. Spin does not walk. **Release does not restore `PB-MOTOR` or re-enable** | Everything until a fresh arm/readiness/`BASE_ENABLE` sequence | Fault in heartbeat; motor-domain absent | As F-13: operator-initiated system arm, readiness, enable and a **new** action. Not a resumed spin | Motor rail to 0; logic flat; `nSLEEP`/PWM; zero motion ≥10 s after release while stale goals `NACK(INHIBITED)`. Log `d_coast` and `d_BRAKE` as the G01 pair; a longer coast is not `FS-01` |
| **F-42** | `EN-02` / `EN-03` mid-launch | `CC-10A` / `CC-13D`; `EN-03` under `CC-14` | Ramp energy through registered low then critical during `LP-04-LAUNCH` (RP-02 F-16 method on this rig) | `EN-02`: brake, reject new locomotion/peak. `EN-03`: `OM-03`, bounded settle only if margin permits, then `EV-14` | Goals violating `EN-02/03` → `NACK(INHIBITED)` | Energy state in `HEARTBEAT`; `BASE_FAULT` if latched | Fresh pack/charge → normal → fresh enable. No automatic resume of the launch | Threshold timestamps vs `BRAKE`; `nSLEEP`; zero relaunch on recovery |

### 2.4 Caught tabletop (last)

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-43** | `CC-12C` arm expiry on the table | `CC-12C` inside the verified catch, marked footprint | Let `CC-12C_ARM` expire at execution during the 0.06 m/s creep; separately send a `BASE_GOAL` after expiry; separately send come/follow/spin under a still-valid arm | Drive inhibits at expiry; edge sensing remains active. Speed never rises. Catch is the backstop, not the stop path | Post-expiry goals; come/follow/spin always (`BC-06`) | Arm-expired reason; `OM-02` still tabletop, drive-off; `NACK(INHIBITED)` / `NACK(EXPIRED)` | New `CC-12C_ARM` (new nonce) after readiness; or leave tabletop via `OM-03`. `BASE_ENABLE` alone is not enough | Arm timestamps vs encoder; speed ≤ clamp; zero uncaught travel; catch unused in a passing run |

## 3. Candidate G05 metrics (not registered)

These are campaign-planning numbers. They are not G05 thresholds and not a freeze. RP-02 G04 candidates remain the authority for `F-19/F-22/F-26` until those rows are scored there.

| Metric | Candidate | Applies to |
|---|---|---|
| Time from injection to `BRAKE` onset | ≤ 50 ms detection-to-deceleration invariant for locally detected stop-path faults (cliff, analog IR, bump, nFAULT, E-stop, IMU lift/tip); ≤ 200 ms for heartbeat/lease-mediated (C0 loss, app-link via F-17) | F-31, F-32, F-33, F-35, F-37, F-41; F-39, F-40 |
| Obsolete commands executed after any fault | **0** | All |
| Health / `BASE_HAZARD` correct | within 2 heartbeat periods (≤ 100 ms candidate) | All |
| Motion after recovery without a fresh `BASE_ENABLE` (and `CC-12C_ARM` where required) | **0** | All |
| Cutoff-coast vs commanded `BRAKE` (`BM-14`) | Two distances from the same `v`; coast finite; **0** restart on release (`FS-07`). Coast is **not** required to be ≤ `d_BRAKE` | F-41; G01 metric |
| ToF-only inhibit while analog IR valid | **0** | F-44 |
| Uncaught tabletop departure | **0**; a row without a verified catch is invalid | F-43, F-19 tabletop half, F-31 on table |
| `BASE_GOAL` flood: wheel-loop p99 | inside the (unregistered) G05 C3 jitter candidate | F-45 |
| Repetitions | 5 per row minimum; floor rows in at least two surfaces/load corners where the fault is meaningful; tabletop rows only on the caught fixture | All |

## 4. Campaign order

Increasing authority, and **never** a live desk before the catch exists:

1. **Bench-only, motors on a stand or wheels up.** Sensor mask via interposer (`F-31`, `F-32`, `F-33`, `F-44`), encoder unplug/swap (`F-34`), driver `nFAULT`/OC (`F-35`), flood (`F-45`). No chassis, no floor claim.
2. **Guarded floor, E-stop on the motor bus, workbench scored-test gate satisfied.** Stall/block (`F-36`), pickup/tip (`F-37`), mode-evidence (`F-38`), app-link mid-follow (`F-39`), C0 loss (`F-40`), `EN-02/03` mid-launch (`F-42`), E-stop mid-spin (`F-41`, also every session as F-12/F-13). Inherited `F-19` (floor half), `F-22`, `F-26` on this rig as RP-02 already ordered them.
3. **Caught tabletop last.** Catch fixture verified. `F-43`; `F-31`/`F-19` tabletop half; no pilot without the catch. Invalid if the catch is absent.

F-12/F-13 remain **every session** on any motion rig (`workbench.md`). F-41 is the spin-specific scoring of that pair, not a replacement. G01 records the same cutoff from straight-line `v` as `BM-14` (coast vs `BRAKE`); that pair is a floor-control metric, not a G05 substitute.

## 5. Registration record

| Registration | Date | Approved scope | Not yet registered |
|---|---|---|---|
| — | 2026-09-17 | None. This file is the Part-4 definition of `F-31…F-45` and the RP-03 methods for `F-19/F-22/F-26` | Builder approval `RP03-P4-REG-01`; injection fixtures; repetitions; numeric G05 thresholds; any scored run |

`F-19/F-22/F-26` registration remains `RP02-P1-REG-01` / `RP02-P3-REG-01`. This file does not re-register them.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-17 | 0.1 | First draft: cross-list `F-19/F-22/F-26`; add `F-31…F-45`; bench → guarded floor → caught-tabletop campaign order. Candidate G05 metrics listed and not registered. |
| 2026-09-18 | 0.2 | `BM-14` cutoff-coast paired with `F-41` and named as a G01 candidate metric distinct from commanded `BRAKE`. Release-does-not-restart remains `FS-07`. |
