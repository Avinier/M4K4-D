# RP-03 Rig — Ugly Chassis, Instrumentation, Catch, Course

| Field | Value |
|---|---|
| Status | **Designed, not built.** Architecture and gate *candidates* reconciled to `RP03-P5-REG-01`; blocked on the `workbench.md` scored-test gate for anything powered on this chassis, on a named drivetrain/sensor freeze for scored G01–G06, and on the battery gate plus a verified catch fixture for Phase C |
| Owner | Project builder |
| Created | 2026-09-17 |
| Revised | 2026-09-19 |
| Authority | `../../01-system/workbench.md` scored-test gate, PSU rule, E-stop rule, battery gate; `../../01-system/risk-prototype-plan.md` v1.12 §RP-03 rig and measurements; folder `plan.md` §6 |
| Design it realises | `intent.md` vehicle-plus-safety-authority; `physics.md` v0.1 envelope (ranges, not a freeze); `storyboard.md` `BM-00…12`; interchangeable Concept A/B front support; C3 on the frame |
| Instrument rule | `workbench.md` item 6: an instrument on the bench must resolve the gate's threshold or the run is **exploratory-only**. If this bench cannot resolve 50 ms detection-to-deceleration, G03 latency and G05 local time-to-brake are exploratory-only |

The rig is a decision instrument, not a mini-droid. It is an open frame with adjustable support geometry, ballast that sets mass and both CoM coordinates independently, a protected motor tree, a sensor interposer, and a floor-marked course with a catch on the table. Every hour spent making it pretty is an hour not spent measuring lift onset.

## 1. Bench constraints that shape the rig

| Constraint | Consequence |
|---|---|
| **Korad KA3005D is 30 V / 5 A.** Physics `E` class is 1.5–3 A per motor; two motors at 2.5 A stall = 5.0 A at the ceiling, at 3.0 A = 6.0 A exceeds | Phase B stall/reversal characterisation is **per motor** (or needs a second source). Both-motor composites, `CC-10A/B` regenerative `W` rows and `CC-PEAK-01` drive share wait on a **Phase C pack**. No stall, lift or stopping claim from an electronic-load substitute |
| The Korad is linear CV/CC with a current limit that snaps to CC | Every new branch is first energized at a limit of expected draw + margin (`workbench.md` standing rule). Per-channel INA-class monitors stay on `PB-DRIVE-L/R` even when the Korad display is the cross-check |
| Oscilloscope deferred "until an analog problem appears" | Driver-rail spikes, regen polarity and brownout on `PB-DRIVE*` are millisecond events. Either the scope is un-deferred for Phase B motor work, or the INA-class monitors run at maximum conversion rate with the resolution **stated on the run record**, and any claim finer than that resolution is exploratory |
| Logic analyzer probes ≤ 5 V only | Fine for C3 GPIO, encoder, UART/TTL, watchdog feed/WDO, driver fault/enable and the status-light timing cue. **Never** on the motor rail |
| Hardware E-stop cuts the **motor bus**, not logic | Verified working *every session*. Assertion removes `PB-MOTOR` while C3 and `PB-SAFE-BASE` stay up. Release does not restore motion authorization or an old `BASE_GOAL` |
| No battery hardware until the written procedure, bag and balance charger exist | Phase A and B run on the Korad. Phase C pack work shares the RP-02 battery gate. The procedure is produced before first use and not edited during the session |
| **Fall from desk is the #1 hardware-loss risk** | Floor for G01/G02/G03/G06. Tabletop only inside a verified catch. **No uncaught tabletop trial**, pilot or scored. An uncaught row is invalid and is recorded as such |

## 2. Chassis

The fixture must reproduce inherited drive geometry without pretending to be a body shell. Changing ballast must **not** change frame stiffness or support geometry. Provide:

- an **open frame** carrying two Ø84 mm nominal drive wheels at **170 mm** track (centre-to-centre);
- an **adjustable axle-to-caster** mount spanning **105–115 mm** (110 mm target), lockable and readable to a millimetre;
- an **interchangeable front support**: **`D21` ball transfer (selected, BD-08)** or `D20` swivel caster (Ø25–32 mm class, comparison), swapped without changing the axle-to-contact number that was just set. Score `D21` on `S-LAM`/`S-RUG`; do not drop the caster swap;
- an **adjustable rear anti-tip skid**, reach **60–80 mm** behind the axle and height **8–16 mm** above the floor, lockable and readable. Do not freeze 14 mm / 70 mm — `physics.md` §2.7 fails that pair against every lumped Layout 03 CoM unless ballast restores `x`;
- **ballast that sets total mass AND both CoM coordinates independently** across BD-05: **1.65 kg** (ledger analytical low) and **3.10 kg + head** (other-subsystem high plus Layout 03 complete-head `E` ~499–524 g), at **both CoM extremes**. Independent means a forward/aft slide that moves `x_CoM` without a first-order change in `h_CoM`, and a vertical stack that moves `h_CoM` without a first-order change in `x_CoM`. Record `(M, x, h)` on every run;
- a **battery-mass dummy in a FORWARD bay** (low, ahead of the axle). **HIGH_AFT is a forbidden ballast case** — `physics.md` §2.2: pack CoM on or behind the axle reverses the sign of `a_tip` (`−0.111 m/s²` at the tabulated HIGH_AFT). The dummy cannot be parked over or behind the axle "because it fitted";
- a head-mass dummy at the 304 mm stack (~250–255 mm lumped CoM height) so BD-05 high corners include the Layout 03 head `E` tree. Complete-head `W` (M900) is not required for paper or for this fixture; a point `a_tip` still waits on M900;
- physical wheel stops / a floor catch for the chassis on the workbench so a runaway cannot walk off the desk during bring-up. Bench bring-up is not a tabletop trial.

Print versus buy for this frame is in `research.md` §1.5: print the open frame, clamps, ballast bay, skid carrier, bumper bar, sensor patches, and the 0–15 mm front-support adapters. Buy the encoder motors (import if needed), PU tread in the Ø80–85 band, 1″ POM ball, swivel caster article, 608s / D-inserts, and the stop-path sensors. Do not print a motor, a ball, a caster fork as the `D20` comparison, or a full FDM tyre as frozen `D10`.

Loaded reversal, spin scrub and lift-onset may share this frame but are **different measurements**: quasi-static `BM-07` reversals for deadband, `BM-06` for walk/scrub, then a separate commanded-accel ramp for caster-lift onset versus the `a_tip` computed from **that** ballast's `(x, h)`.

## 3. Motor domain

One protected tree with every node labelled by its registered `PB-*` key. The rig preserves `PA-13`; it does not imply that eventual circuits occupy one PCB.

| Position | Item | Notes |
|---|---|---|
| `PB-MOTOR` source fixture | Banana posts from the Korad, later the selected pack connector; removable isolation | Bench-supply and pack sources are mutually exclusive. Pack waits on the battery gate |
| System motor-arm | Normally-off switching fixture between operating source and E-stop | Drops `PB-MOTOR` in system `OFF`, boot inhibit and charge even when the mushroom is released |
| **Hardware E-stop** | Latching mushroom electrically dominant over the motor-arm command and in series with `PB-MOTOR` | Verified working *every session*; assertion removes drive energy while C3/`PB-SAFE-BASE` remain available |
| `PB-DRIVE` | Downstream of `PB-MOTOR`; common drive feed before the split | Scope point at the driver supply. Signed current observable |
| `PB-DRIVE-L` / `PB-DRIVE-R` | Independent protection/measurement positions, one per wheel | Per-channel **INA-class** high-side monitors. An unsigned sensor that folds regen into "less traction" is not compliant |
| Driver | Brushed H-bridge class with hardware fault output, per-channel current sense, logic-level enable that fails safe | Exact part is a Part 4 lead (`DRV8874` class), not a freeze. **Driver fault and enable brought to test points** |
| Return | Source-adjacent star; paired outgoing/return for each drive branch | Removable links permit return-drop measurement |
| Test points | Pre/post motor-arm and E-stop; driver supply; each load-end; fault; enable | Dual-labelled with `PB-*`. Logic-analyzer clips live only on the logic-level points |

Phase A may hang **one** reference motor (D02 class, bench equipment until a freeze) on a stand from this tree. A bare motor on a stand reproduces torque/current, **not** traction, scrub or lift. Equivalence is recorded on the run; no G01/G03/G04 claim from it.

## 4. Controller and sensor interposer

| Position | Item | Notes |
|---|---|---|
| C3 | **ESP32-S3-DevKitC-1-N8** on the frame | Prototype board per `RP02-P3-REG-01/02`. N8R8 is not a silent substitute. Later WROOM-1-N8 carrier only by controlled equivalence |
| Link | RP-02 differential-link breakout **or** bench TTL | TTL is bench-only. Production framing stays the registered COBS/CRC/session envelope |
| External window-watchdog | Fixture, one, TPS3436-Q1 family, exact suffix open | Feed only after a complete healthy safety loop. `F-26` lives here |
| Sensing header | Candidates plug here, not into ad-hoc Dupont sprawl | No safety input behind a GPIO expander. Strapping GPIO0/3/45/46 excluded from safety outputs |
| **SENSOR INTERPOSER** | Inline fixture that can **mask, freeze or corrupt one sensor** for `F-19`-class injections without touching wiring | Logged injection timestamp on the injecting device. One channel at a time unless a named campaign row says otherwise |
| Status-light timing cue | C3 GPIO / `LIGHT_STATE` analogue, in the top-down camera's view | Co-visible with the chassis for video-to-log alignment |
| `PB-SAFE-BASE` | Independent of C2's converter; off in charging | Sense wiring cannot back-power a de-energized branch |

Phase A may log a base IMU as a **bench instrument on the stand**. BD-03 working assumption: from Phase B the base IMU is **runtime hardware** on the rigid frame (MEM-20260812-02; CA reserves SPI+INT). Head mounting is excluded.

## 5. Instrumentation

Every instrument entry records sampling rate, calibration/check method, uncertainty and run-record channel name **before** scored use. A gate whose threshold the bench cannot resolve is marked exploratory-only until it can.

| Quantity | Instrument | Rate / resolution | Check method | Uncertainty (state before scored use) | Channel | Gate |
|---|---|---|---|---|---|---|
| Wheel encoder L/R | C3 PCNT (or equivalent) on the common timebase | Wheel-loop target 500 Hz; log ≥ 100 Hz cruise, ≥ 500 Hz around reversal/stop | Known-CPR rotation against a marked wheel and a tape distance on the floor | Candidate ±1 count plus timebase error; CPR is `U` until the encoder is named. Creep at 0.04 m/s is ~9.1 RPM — if the encoder cannot resolve it, G01 min-speed is exploratory | `n_L`, `n_R`, `v_enc` | G01, G02, G06 |
| Base IMU | Rigid-frame IMU, SPI+INT preferred | ≥ 100 Hz runtime log; ≥ 200 Hz for lift-onset / pickup | Static level vs a machinist's level or tilt indicator; 90° block check | Candidate pitch ±0.5° class until the SKU is named. Used for lift/tip/slip, not as a substitute for wheel odometry | `imu_axyz`, `imu_pitch` | G01 lift, G05 pickup |
| Rail / branch V/I | INA-class monitors on `PB-DRIVE-L/R` plus input; Korad display as cross-check | ≥ 1 kHz conversion around launch/reversal/brake; 10 Hz for energy | Session start: Korad CC at 0.5 A and 2 A vs INA | INA226-class ~±1 % of range + shunt tolerance, stated after the shunt is sized. Regen polarity must be visible as signed | `v_drive`, `i_L`, `i_R` | ledger `W`; G05 overcurrent |
| Driver supply transient | Scope at the driver supply test point; until un-deferred, INA at max rate with resolution stated | Scope ≥ 1 MS/s single-shot on stall/reversal trigger | Probe ×10 vs a known DC | If only 1 kHz INA: events shorter than ~2–3 ms are unresolved — those runs are exploratory for spike claims | `v_drv_min` | Phase B/C electrical |
| Motor / driver temperature | Thermocouple or thermistor on each gearbox housing and driver package | 1 Hz | Meter cross-check; ice-point if claimed absolute | ±2 °C class | `T_motor_L/R`, `T_drv` | thermal; stop on registered limit |
| Sound level | Sound-level meter at a **fixed** body-array-proxy position | Session note until the timebase exists; then on the common clock | Same position, same instrument, `BM-04` and `BM-06`, both load corners if BD-05 asks | Absolute dB is `U` without a calibrator; same-session relative is admissible for the `physics.md` §9 obligation. A quiet motor-on-a-stand is not the body-array number | `L_eq` | acoustic obligation, not a pass |
| External top-down video | Camera over a floor-marked course; C3 status-light timing cue in frame | **≥ 60 fps** for any 50 ms claim; 30 fps is **not** a 50 ms instrument (one frame = 33 ms) | Tape marks in view; light-edge vs log `t0` | 1 frame at 60 fps ≈ 17 ms; 50 ms detection-to-decel needs the GPIO path below, video as corroboration. 30 fps → G03 latency **exploratory-only** | `vid` | G01–G04, G06 |
| Detection-to-decel / time-to-brake | Logic analyzer on hazard-assert GPIO **and** driver-enable/PWM change, common timebase with encoders | Analyzer MHz-class; score the edge delta. Need ≤ 5 ms resolution to *resolve* a 50 ms gate | Session: toggle the cue GPIO and confirm the analyzer and log agree to < 1 ms | If this path is absent, G03 detection latency and G05 local time-to-brake are **exploratory-only**. Do not score 50 ms from 10 Hz INA or 30 fps video | `t_detect`, `t_decel`, `t_brake` | G03, G05 |
| Stopping / clearance distance | Tape and/or laser distance to floor marks and to the obstacle face | Event (start mark, stop mark, object face) | Laser vs tape at 0.5 m and 1.0 m this session | Tape ±2 mm class; laser ±1 mm class plus alignment. Subtract the stated uncertainty before claiming a millimetre gate | `d_stop`, `d_clear` | G01, G03, G04 |
| Caster-lift onset | Tilt indicator **or** IMU pitch, plus video of the caster patch | IMU ≥ 200 Hz around the accel ramp; video as witness | Zero on level floor; known wedge angle | Candidate ±0.5° pitch. Lift-onset `a` is commanded/measured body accel at first caster unload, compared to `a_tip = g·x/h` computed from **this** ballast's measured `(x, h)`, not from 1.98 m/s² | `pitch`, `a_lift` | G01 |
| CoM / mass of this ballast | Scale plus documented slide/stack positions | Once per ballast change | Scale check near 1 kg and 3 kg | Scale ±5 g class or better; `x,h` from the ballast map ±2 mm class until a measured hang/tilt CoM exists | `M`, `x_CoM`, `h_CoM` | every scored row |
| Link / arm / mode | `BASE_STATE` / `BASE_FAULT`, session/epoch, arm nonce | 20 Hz heartbeat plus event | Rejected-request log on an un-armed tabletop `BASE_GOAL` | Event-level; stale-command claims need this log, not video | `mode`, `arm`, `fault` | G04, G05 |
| Bench instrument MCU | Nano 33 BLE Sense or a second DevKitC reading INA/thermistors if C3 is the article under test | — | — | Bench equipment per `workbench.md`; not robot hardware | — | — |

**50 ms rule, restated.** CA-12's detection-to-deceleration invariant is 50 ms. Score it with a GPIO-class instrument. Physics' 35 ms paper sum is not evidence of 15 ms spare. If the bench cannot resolve 50 ms, that gate (or that metric) is exploratory-only.

## 6. Floor course and props

Working surface names pending BD-04 builder confirmation of the actual demo-room floors. Until named, use these as **working labels**, not a freeze of SC-TBD-07:

| Label | Role |
|---|---|
| Tile | Dry household tile |
| Wood / laminate | Dust and polish move μ |
| Thin rug | Pile can jam a caster or a ball transfer |
| Threshold strip | Geometric disturbance, not a μ problem |

Marked test area on each surface. Start/stop marks for each speed band used in G01/G02: **0.15**, **0.40**, **0.50 m/s** scored; **0.60 m/s** `BM-09` exploratory; **0.70 m/s** is a G02 cannot-exceed / drivetrain design point, **not** a commanded storyboard speed. Follow never authors past 0.50 m/s.

Obstacles (G03, BD-02 stop-only):

- person-leg proxy (prop, not a person — RP-07 owns real-person come/follow);
- furniture leg;
- cardboard box;
- cable / flat obstacle.

A 20 mm × 20 mm × 20 mm floor-level block in the caster shadow is the `physics.md` C12 blind-region failure mode; it is a coverage probe, not a G03 "pass by bumping".

## 7. Tabletop fixture (Phase C)

A **large table**. No uncaught trial.

| Item | Design | Notes |
|---|---|---|
| Marked circular footprint | **250 mm radius** (500 mm diameter) | `physics.md` §8 **CON-TBD-14 proposal, not registered**. Registration waits on G04 freeze. This is the marked validated circle, not "the robot may move 250 mm" |
| Calibration speed | 0.04–0.06 m/s (`BM-11`) | Ordinary come/follow/spin stay inhibited in `OM-02` |
| Catch | **Overhead tether primary** (BD-07 working assumption). Raised lip **secondary only if it sits below cliff FoV**. Lip-only is rejected as default because it can mask cliff sensing | Catch must prevent a fall **without sitting in the cliff sensors' view**. Physics proposal: catch outside ~300 mm radius |
| Edge-approach lanes | Several angles; physics proposal 0, 45, 90, 135, 180° relative to heading | Hits caster, wheel and skid as leading contact |
| Surfaces | Dark and glossy samples | Cliff failure mode, not an afterthought |
| Permission | Armed `CC-12C` only, inside the caught footprint | BD-01: V1 tabletop is fully stationary for users; `CC-12C` remains an **owed caught-fixture calibration case** for G04, not a user-facing V1 behaviour |

A tabletop row without "catch fixture verified this session" on the checklist is invalid.

## 8. Loads: real versus substitute

The plan permits characterized substitutes only where their equivalence is recorded.

| Load | Phase A | Phase B | Phase C | Equivalence |
|---|---|---|---|---|
| Drive motors | One D02-class reference unit on a **stand** | Two candidate motors + wheels + caster + skid on the ballasted frame | Same, plus both-motor transients on the pack | Stand: torque/current only — **no** traction, scrub, lift, stopping or edge claim |
| Electronic load on `PB-DRIVE*` | Optional current-time trace | Same | Prefer real motors | Reproduces current-time duty, **not** inductive kick or regeneration — no stall/lift/stop claim |
| C3 N8 | **Real** | Real | Real | DevKitC USB-UART draw is not the later carrier |
| Sensors | Header + interposer; may be absent | Candidates installed for G03/G05 floor rows | Installed for G04 | Masked/frozen/corrupt via interposer is the F-19 injection, not a wiring change |
| Pack | Absent — Korad | Absent — Korad; per-motor stall | Candidate pack after battery gate | Korad is not pack impedance |
| Head | Mass dummy | Mass dummy at stack | Same | Dummy is mass/CoM, not RP-01 motion |

**Rule:** a ledger row sourced from a substitute carries evidence class `E` with the substitute named, never `W`. No stability, stopping or edge claim from a stand or an electronic load.

## 9. Safety on this rig

- Hardware E-stop dominates the motor-arm path and removes only hazardous motor energy; verified each session.
- `OFF` is tested separately: a released E-stop must not leave `PB-MOTOR` energized when the system-power latch is off.
- Korad current limit set before every new branch is energized; Phase B stall/reversal **per motor**.
- Chassis restrained on the bench; floor for locomotion; tabletop only with a verified catch. Desk fall is the #1 hardware-loss risk.
- No pack work until the `workbench.md` battery gate is satisfied; bag, non-flammable surface, never unattended.
- Thermal limits registered before any sustained run; stop on smoke, odour, swelling, temperature beyond the registered limit, or repeated unexplained reset.
- Sensor interposer injections are named campaign rows with logged timestamps, not casual unplugging mid-run.

## 10. Readiness checklist state

*(mirror of the `workbench.md` scored-test gate for this rig, plus this-rig items; all must pass before any scored run)*

Workbench scored-test gate:

- [ ] E-stop verified working this session
- [ ] Current, velocity, acceleration and (where used) yaw-rate limits set for this specific test
- [ ] Rig clamped / robot physically cannot leave the test surface (floor course, or tabletop **inside the catch**)
- [ ] Firmware/software/config/rig revision recorded
- [ ] Logging confirmed writing with the run ID in the log
- [ ] The instrument on the bench resolves the registered threshold (or the run is labelled exploratory-only)

This-rig items:

- [ ] Motor-arm confirmed normally-off; Korad limit set; logic analyzer **not** on the motor rail
- [ ] Ballast `(M, x, h)` recorded; HIGH_AFT not fitted; battery dummy in the forward bay
- [ ] Support geometry recorded (axle-to-front-support, skid reach/height, ball vs caster article)
- [ ] Surface / obstacle / speed-band marks identified
- [ ] Timebase and status-light cue confirmed (or the run is exploratory for any 50 ms term)
- [ ] **Catch fixture verified this session** — required for **any** tabletop row; without it the row is invalid

Designed. Not built. No scored run.
