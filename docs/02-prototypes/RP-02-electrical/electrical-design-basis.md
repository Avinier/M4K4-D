# RP-02 Electrical Design Basis

| Field | Value |
|---|---|
| Status | **Approved electrical-design-basis baseline.** `EDB-01…08` were builder-approved 2026-09-15 and the `EDB-03` source/load contracts were builder-approved 2026-09-16. `RP02-P2-REG-01` supplies stable `PB-*` keys; `RP02-P2-REG-02` supplies implementation targets and the Raspberry Pi 5 2 GB selection; `RP02-P3-REG-01/02` supplies the selected cooler/C3 identities without changing numeric load evidence; branch-side contracts are issued in `power-branch-contracts.md`. |
| Owner | Project builder |
| Created | 2026-09-15 |
| Authority | `state-register.md`, `state-coverage-matrix.md`, `load-model.md`, `fault-matrix.md`, `../../01-system/power-energy-ledger.md`, `../../01-system/risk-prototype-plan.md` §RP-02 |
| Vocabulary | `glossary.md` |
| Numeric source of truth | `../../01-system/power-energy-ledger.md`; this document does not carry a competing current, voltage, power, energy or temperature budget |
| Feeds | `power-architecture.md`, ADR-06 architecture, sourcing requirements, `rig.md`, `gates.md` G01/G02/G03/G06 |

This document defines what the electrical system must be designed against. It sits between the registered operating/load model and the physical power topology:

`Part-1 state/case/profile → EDB load requirement → approved branch topology → selected hardware → measured qualification`

Approval of a requirement does not select hardware and does not upgrade its evidence class.

## 1. Approved design-basis principles

### `EDB-01` — Scope boundary

RP-02 Part 2 covers the complete low-voltage system from the onboard battery terminals and external low-voltage charging connector through protection, isolation, switching, conversion, distribution, returns, harnesses and measurement, ending at every load's electrical terminals.

Power-related control signals are in scope: hardware driver enable, E-stop state sensing, rail-present/power-good, charger and pack status, and controlled-shutdown requests. AC mains, the detailed SBC↔C2 command protocol, actuator internals, exact pack capacity and integrated endurance closure are out of scope. The external certified AC/DC adapter is an input requirement; AC mains does not enter Makad.

### `EDB-02` — Sources of truth

| Subject | Owner |
|---|---|
| Operating states, concurrency, events, faults and `MD-01` | Registered Part-1 documents |
| `LP-*` profiles and `TB-*` measurement classes | `load-model.md` |
| Current, voltage, power, energy, loss and temperature values | `../../01-system/power-energy-ledger.md` |
| Electrical requirements, assumptions and calculation conventions | This document |
| Physical topology and architecture choices | `power-architecture.md` |
| Registered acceptance thresholds | `gates.md` |

### `EDB-03` — Electrical requirement record

Every source interface, `LG-*` load boundary and later physical distribution branch receives a normalized electrical contract. §2 defines the schema; §§4–5 contain the first load/source-side issue. Unknowns stay `U`, name their owner and state what they block.

### `EDB-04` — Electrical safety invariants

1. No boot, reset, reconnection, charging transition or power restoration may energize an actuator without fresh local authorization.
2. Loss of the SBC must not remove the controller responsible for preventing uncontrolled motion.
3. E-stop removes hazardous actuator energy independently of SBC software while preserving safety supervision and diagnosis.
4. Removing or restoring a source cannot replay stored motion.
5. A display, audio, camera or SBC branch fault must not energize a hazardous branch or destabilize safety supervision.
6. A hazardous-branch fault must be contained as locally as the architecture permits and must not silently reset safety supervision.
7. Charging mode hardware-inhibits all actuator energy.
8. Service, programming and external-data connections must not back-power an isolated or stopped domain.
9. Connector separation, partial mating or incorrect mating must not create uncontrolled hazardous energy.
10. Stored and regenerated energy are sources and remain in the safety analysis after the upstream source is opened.

### `EDB-05` — Electrical criticality classes

| Class | Meaning | Current load bindings |
|---|---|---|
| `EC-S` | Safety supervision required while hazardous energy is present or being removed | `LG-02`; `LG-10` when base motion/safety is active |
| `EC-H` | Hazardous-energy load capable of motion or force | `LG-03Y/P/R`, `LG-04` |
| `EC-C` | Mission compute whose failure must be contained locally | `LG-01` |
| `EC-N` | Non-hazardous/shedable functionality | `LG-05`, `LG-06`, `LG-07`, `LG-08` |
| `EC-Q` | Charging and minimum pack supervision | Charger/power path and required charge/pack telemetry; later branch contract |

`LG-09` is a derived loss boundary, not a consumer class. Criticality is not physical topology: sharing an upstream source is permitted only when the architecture proves the required fault containment. C2 safety supervision must be independent of the display failure branch.

### `EDB-06` — Evidence versus decision status

Every value carries an evidence class (`U/E/D/W`) and an independent decision status (proposed, approved requirement, selected design value or verified result). Approval never upgrades evidence. Substitute-load results remain `E` even if precisely measured.

### `EDB-07` — Margin policy

There is no universal percentage. Continuous current, transient response, terminal voltage, conversion thermal capacity, conductor heating, protection coordination, energy reserve, timing and instrument resolution receive separately justified margins. Margin is evaluated at the component terminal under the applicable registered condition. Numeric margins are registered before scored evidence is inspected.

### `EDB-08` — Completion rule

The design basis closes when every source and load has a contract; every relevant `CC`, `LP` and `F` maps to an electrical requirement; every unknown has an owner and consequence; credible and synthetic demands remain separate; and architecture, sourcing and qualification can consume the result without redefining it.

## 2. `EDB-03` record method

### 2.1 Three linked record layers

| Layer | Key | Purpose | Creation point |
|---|---|---|---|
| Source-side contract | Descriptive boundary plus registered `PB-MAIN`/charge paths | Defines what the pack or charge input can supply, absorb, block and report | §5 and `power-branch-contracts.md` |
| Load-side contract | Existing `LG-*` ID | Defines what the consumer requires or can return at its electrical terminal | Now; §4 |
| Branch-side contract | Approved topology branch ID | Defines what one physical path must deliver after aggregating its permitted concurrent loads | When the domain/rail topology is approved |

No additional namespace is needed for source/load contracts. Branch IDs will be introduced only with the topology they identify and then added to `glossary.md`.

### 2.2 Required fields

| Group | Required fields |
|---|---|
| Identity | `LG`, boundary, owner, selected configuration, `EC` class |
| Supply | Nominal/permitted terminal voltage, ripple/noise, undervoltage and overvoltage behaviour |
| Demand | Mean/RMS, peak/percentile, peak width, slew, repetition, duty and recovery |
| Bidirectional effects | Inrush, reverse current, regeneration and rail-overvoltage behaviour |
| State behaviour | `OFF`, idle, active, inhibit, startup, shutdown and power-restoration behaviour |
| Physical path | Positive feed, complete return, connector/harness constraints and moving-boundary status |
| Control/protection | Enable default, switching, current limiting, fault containment, back-power prevention and required sensing |
| Traceability | Applicable `LP`, `CC`, `F`, gate and safety invariant |
| Evidence | `U/E/D/W`, source/revision, uncertainty or tolerance, run ID when `W` |
| Dependency | Open input, owner, and the architecture/sizing/test decision it blocks |

### 2.3 Composition and aggregation rules

1. Load contracts describe individual boundaries; branch contracts aggregate only loads physically fed by that branch.
2. A branch demand is evaluated separately for every registered `CC-*` that can energize it. Independent nameplate maxima are not automatically simultaneous.
3. `CC-PEAK-01` defines the credible whole-robot peak. `ST-01` remains a separately labelled robustness vector.
4. `MD-01` supplies the chronological energy workload; it does not replace state-specific thermal and transient cases.
5. Signed current is retained through braking/regeneration analysis. Negative current is not converted to zero before source and overvoltage checks.
6. Yaw, pitch and roll remain separate through voltage-drop, protection and fault analysis even if they later share an upstream converter.
7. Voltage and margin are evaluated at the load terminal using the complete positive and return path.
8. A substitute reproduces only the named characteristics in its equivalence record. An electronic-load drive substitute cannot close inductive/regenerative behaviour.
9. A missing device, missing measurement or unselected component is `U`, never `OFF` and never zero demand.
10. All numeric fields link to a ledger revision; this document records the requirement and evidence state, not a copied value.

### 2.4 Power-disposition labels

These labels are used in requirement records and the later state-to-branch matrix:

| Label | Meaning |
|---|---|
| `OFF` | Verified electrically removed/disabled at the stated boundary |
| `INHIBITED` | Powered or power-capable but hazardous output cannot be accepted; not equivalent to `OFF` |
| `IDLE` | Powered and supervising without the active workload |
| `ACTIVE` | Producing the named `LP-*` workload |
| `SHED` | Deliberately removed by energy/thermal policy while higher-priority functions remain |
| `SETTLE` | Temporary bounded actuator energy used only to reach a registered safe state |
| `U` | Implementation or disposition not yet known |

## 3. Cross-cutting state requirements

This is a requirements map, not the final rail-switching implementation.

| Condition | Safety supervision | Head actuator energy | Drive actuator energy | Compute/UI/sensing | Required terminal result |
|---|---|---|---|---|---|
| Cold boot, `CC-01` | `ACTIVE` through inhibited self-check | `OFF` | `OFF` | Required boot profiles only | No actuator energy before local readiness and fresh enable |
| Quiet sleep, `CC-02F/T` | `IDLE` | `OFF`/torque unavailable | `OFF` | Registered listening + dim face; camera off | Missing hardware is not counted as the required `OFF` proof |
| Floor operation, `OM-01` | `ACTIVE` | `ACTIVE` only for authorized head profiles | `ACTIVE` only for authorized base profiles | By current `CC/LP` | Every active load remains inside its terminal contract |
| Tabletop operation, `OM-02` | `ACTIVE` | Authorized head profiles permitted | `INHIBITED`; only `CC-12C` may arm bounded caught-fixture motion | By current `CC/LP` | Drive rejection is independent of app/network continuity |
| Motion inhibited, `OM-03` | `ACTIVE` | `INHIBITED`; `SETTLE` only when explicitly permitted and margin exists | `OFF` or hardware-disabled | Diagnosis may remain | No new or stored motion executes |
| Hard stop, `OM-04` | `ACTIVE` | `OFF` | `OFF` | Legal diagnosis/indication may remain | Hazardous rail removal is independent of SBC software |
| Bench/service, `OM-05` | `ACTIVE` | Only explicitly armed fixture channel | Only explicitly armed fixture channel | As registered for the run | Unarmed channels remain inhibited/off |
| Charging, `CC-15` | Minimum required supervision `IDLE` | `OFF` | `OFF` | Charge display active; ordinary SBC/camera/mics/audio/base sensing off | Charger/status loss cannot restore a previous operating mode |
| Low energy, `EN-02` | `ACTIVE` | Brake active peak motion; deny new peak gestures | Brake; deny new locomotion | Bounded indication at reduced demand | Voltage recovery alone does not resume work |
| Critical energy, `EN-03` | Alive long enough to execute registered policy | `SETTLE` only if margin permits, then `OFF` | Brake then `OFF` | Persist reason and shut down | Orderly terminal state precedes uncontrolled collapse |
| E-stop restoration, `EV-16` | `ACTIVE` with fault/recovery state | Power may return only into `INHIBITED` | Power may return only into `INHIBITED` | Diagnosis remains | Zero stored motion; fresh complete enable sequence required |
| Final shutdown, `CC-16` | Active through sign-off, then `OFF` | `OFF` | `OFF` | All groups reach registered `OFF` | Isolation state is observable and no back-power path remains |

## 4. Load-side electrical requirement register

Every numeric entry below intentionally points to the ledger. A later `D` or `W` update changes the evidence row without silently changing the approved requirement.

### `LG-01` — Main Linux SBC compute

| Field | Requirement |
|---|---|
| Boundary / class | SBC input power connector or header, including the board-side input protection; `EC-C` |
| Configuration | **Selected Raspberry Pi 5 2 GB under `RP02-P2-REG-02`; official Pi 5 Active Cooler selected under `RP02-P3-REG-01`.** Purchase, storage and power-entry hardware remain open; final enclosure airflow/acoustics remain evidence items. |
| Supply contract | Registered 5.1 V nominal `PB-COMPUTE` endpoint with 5 A interface capability. Manufacturer guidance establishes a stable 5 V-class input, reliable operation above 4.8 V and low-voltage indication around 4.63 V (`D`). Final input method, tolerance/ripple behavior, reset behavior and clean-shutdown implementation remain open. |
| Profiles / cases | All `LP-01-*`; active in `CC-01…14`, `CC-17/18`, `CC-PEAK-01`, `ST-01` and `MD-01` as bound by `load-model.md`; `LP-01-OFF` in `CC-15` and after `CC-16`. |
| Demand characterization | Boot inrush; idle; perception, audio, service and coexistence mean/RMS; peak width and slew; shutdown energy/time. Values stay in the ledger. |
| State behavior | Cold boot cannot authorize motion. Full loss/reset follows F-02. Orderly shutdown must finish before input removal when energy permits. |
| Protection / containment | Own protected supply branch. Its overload, reset or input short must not reset C2 safety supervision or energize motors. Input back-power through USB, GPIO/UART, camera or programming paths must be blocked or explicitly bounded. |
| Measurement | Input `V/I` at SBC terminal; undervoltage and reset logs; input/board temperature; synchronized event windows for boot and `CC-PEAK-01`. |
| Fault trace | `F-01`, `F-02`, `F-10`, `F-15`, `F-17`, `F-20`; G02/G03/G04 |
| Open dependencies | Exact power-entry/PD-current method; RP-07 workload; storage configuration; final-body Active Cooler airflow/acoustic validation; audio-front-end choice if USB-powered. Blocks converter selection, measured margin and thermal release. |

### `LG-02` — C2 safety controller and servo-bus transceiver

| Field | Requirement |
|---|---|
| Boundary / class | Input to installed C2 module plus required bus transceiver; `EC-S` |
| Configuration | Waveshare ESP32-S3-Zero selected; DevKitC-1-N8R8 is the bench twin. Installed transceiver and input path remain open. |
| Supply contract | Independent `PB-SAFE-C2`, not the display branch. Waveshare documents 3.7–6 V external input at the pad marked 5 V and at least 500 mA source capability (`D`). Installed transceiver/sensing demand, reset threshold and hold-up requirement remain open. |
| Profiles / cases | `LP-02-BOOT/IDLE/TRAJ/LINKSTRESS/FAULT`; alive in every condition while motor energy is present or being removed; `LP-02-IDLE` during `CC-15`; `OFF` only after final shutdown. |
| Demand characterization | Boot inrush, idle/supervision, trajectory/bus workload, link stress and fault handling. Installed Wi-Fi/BT transmission is not a credible profile and remains disabled. |
| State behavior | Boots inhibited with no accepted limits or goals. Any reset, E-stop, motor-domain restoration or link recovery leaves it inhibited and flushes obsolete work. |
| Protection / containment | Display, SBC, servo and drive disturbances must not reset C2. Supply or signal backfeed must not keep an uncommanded partial state alive. Safety rail must expose power-good or an equivalent diagnosable condition. |
| Measurement | Terminal `V/I`; reset reason; brownout/watchdog flags; loop/jitter; rail-present/E-stop sense; transceiver and regulator temperature. |
| Fault trace | `F-01…06`, `F-08`, `F-11…17`; G02/G04/G05 |
| Open dependencies | Exact transceiver, power entry, converter/source selector, reset threshold and required hold-up interval. Independent safety-rail topology is fixed by `RP02-P2-REG-01`; remaining inputs block rating, capacitance and brownout closure. |

### `LG-03Y/P/R` — Head-servo branches

| Field | Requirement |
|---|---|
| Boundary / class | Separate load-end power boundary for yaw, pitch and roll; `EC-H` |
| Configuration | Servo family unselected; XC330-M288-T C01 remains a paper reference only. |
| Supply contract | Rail voltage and loaded terminal floor are `U` pending RP-01 family selection. Each axis retains its own positive/return-path and protection accounting through analysis. |
| Profiles / cases | All `LP-03-*`; applicable `CC-03…06`, optional `CC-08`, tracking/come/follow cases, `CC-11…14`, `CC-16…18`, `CC-PEAK-01`, `ST-01` and `MD-01`. |
| Demand characterization | Per-axis hold/RMS, trajectory peaks, simultaneous alignment, peak width/slew, restrained reference, power-restoration inrush and signed braking/regeneration. Stall `D` is a protection reference, not an operating profile. |
| State behavior | Torque/power unavailable in quiet sleep, hard stop and charging. Power restoration enters inhibited state with zero stored motion. Safe settle is permitted only by the registered state policy. |
| Protection / containment | E-stop removes every head-actuator energy path. One-axis short/absence must not create remaining-axis runaway or reset C2. Bulk energy, discharge and restoration inrush must meet the later stored-energy requirement. Protection device class remains open. |
| Physical path | Moving yaw-boundary power, return and bus route; load-end voltage is measured after every connector and flex conductor. Signal return and high-current return must be explicitly designed. |
| Measurement | Per-axis signed current, servo-terminal voltage, temperature and position/state telemetry; rail maximum/minimum during motion/restoration. |
| Fault trace | `F-03/04`, `F-06`, `F-08`, `F-11…13`, `F-16`; G01/G02/G04/G05/G06 |
| Open dependencies | RP-01 servo selection and real waveforms, allowable sag floor, connector/flex geometry and bus implementation. Blocks rail voltage, converter/direct-feed choice, gauge, protection and capacitance. |

### `LG-04` — Drive motors and motor driver

| Field | Requirement |
|---|---|
| Boundary / class | Driver supply plus separately observable left/right motor outputs as required for qualification; `EC-H` |
| Configuration | Unselected; RP-03 owns motor, driver and representative motion profiles. |
| Supply contract | Input range, driver UVLO/OVLO, logic-versus-power supply behavior and safe enable state are `U`. |
| Profiles / cases | `LP-04-OFF/PWRRESTORE/STEADY/LAUNCH/REV/BRAKE/SPIN/BLOCKEDREF`; drive-dependent `CC-09…14`, `CC-PEAK-01`, `ST-01`, `MD-01`; off elsewhere except caught-fixture `CC-12C`. |
| Demand characterization | Two-channel continuous/RMS demand; launch, reversal, braking and blocked-reference peaks; signed regenerative current and rail rise; mechanical-load and surface dependence. |
| State behavior | Hardware-disabled at boot, tabletop ordinary operation, motion inhibit, hard stop and charging. Restoration enters inhibited state; no stored wheel goal or action survives. |
| Protection / containment | E-stop removes drive-stage hazardous energy independent of SBC. Base-controller reset or missing safety evidence forces hardware-safe driver state. Regeneration must have an explicit admissible sink/clamp behavior. |
| Measurement | Driver-input and per-channel signed `V/I` where practical; motor/driver/connector temperatures; enable/rail state; encoder/stop trace. |
| Fault trace | `F-12/13`, `F-16/17`, `F-19`, `F-22`; G01/G02/G03/G04 |
| Open dependencies | All RP-03 hardware and `W` profiles. An electronic-load substitute may size forward current but cannot close inductive/regenerative or safe-disable behavior. |

### `LG-05` — Display board and status light

| Field | Requirement |
|---|---|
| Boundary / class | Display/status branch input after its branch protection; `EC-N` |
| Configuration | Waveshare no-touch SKU 30493 selected; status light and final input connector open. |
| Supply contract | Waveshare documents Type-C 5 V, 450 mA nominal and 0–65 °C for selected SKU 30493 (`D`). Inrush, tolerance/ripple sensitivity, brightness/FPS profiles and status-light demand require sample `W`. Display remains on `PB-DISPLAY`, independent of C2 safety supervision. |
| Profiles / cases | All `LP-05-*`; dim/active in ordinary states, charge profile in `CC-15`, `OFF` only at final shutdown; case bindings per `load-model.md`. |
| Demand characterization | Board boot/assets, backlight step, idle/active/utility/music/charge RMS, full-brightness reference and status-light transients. |
| State behavior | May fail dark or reset without hazardous effect. Expired state decays safely. Charging display must not require SBC power. Final shutdown proves true electrical `OFF`, not a black image. |
| Protection / containment | Display short, reboot or backlight transient must not reset C2 or energize motors. UART/programming/USB paths must not back-power the safety, compute or stopped display branch. |
| Physical path | Independent `PB-DISPLAY` feed/return and semantic link cross the yaw boundary; a common connector shell is permitted only if contacts and protection retain branch independence from `PB-SAFE-C2`. |
| Measurement | Terminal `V/I`; boot/wake current; brightness/FPS configuration; board/backlight/connector temperature; reset log. |
| Fault trace | `F-07`, `F-13`, `F-18`; G01/G02/G04/G06 |
| Open dependencies | Sample measurements, light selection, brightness bounds, source selector/input connector and SBC-direct versus C2-relay link choice. Blocks final branch rating and charging thermal model. |

### `LG-06` — Camera

| Field | Requirement |
|---|---|
| Boundary / class | Camera power at the SBC camera connector plus the camera module; `EC-N` |
| Configuration | Raspberry Pi Camera Module 3 Wide selected. |
| Supply contract | Supplied through the SBC camera interface; exact voltage/current/sequence and port protection require official SBC/camera `D` and integrated `W`. Its demand is attributed to both `LG-06` and the supplying compute branch without double-counting. |
| Profiles / cases | `LP-06-OFF/STREAM/TRACK/AF`; off in quiet sleep and charging; active only in cases named by `load-model.md`. |
| Demand characterization | Stream RMS, autofocus transient, startup sequence and correlated SBC compute demand. |
| State behavior | Absence or loss removes track evidence and causes dependent head/base behavior to hold or brake; it does not fabricate a valid track. Non-hot-pluggable handling follows the selected interface requirements. |
| Protection / containment | Camera/cable fault must not reset C2 or energize motors. CSI shield/return and connector path must not become an unintended power return. |
| Measurement | Supplying-rail delta and, where instrumentable, camera-branch `V/I`; stream mode, AF event and SBC reset/undervoltage logs. |
| Fault trace | `F-09`; G02/G04 |
| Open dependencies | Selected Pi 5 camera-interface configuration, official/sample power figures and exact harness. Blocks measured compute-branch demand and camera wake model. |

### `LG-07` — Microphones and audio front end

| Field | Requirement |
|---|---|
| Boundary / class | Complete synchronized microphone/front-end input, whether locally powered or through SBC USB/I2S; `EC-N` |
| Configuration | Unselected; direct multichannel front end and USB-array classes remain candidates. |
| Supply contract | Voltage, quiescent/active demand and powering location are `U`. If powered through the SBC, demand is attributed without double-counting and USB back-power behavior is explicit. |
| Profiles / cases | `LP-07-OFF/LISTEN/CAPTURE/FAULT`; listen during registered quiet/awake states, capture during requests/music as bound, off while charging and after shutdown. |
| Demand characterization | Continuous listen RMS, capture/interface demand, USB/DSP startup if applicable, emitter/clock coupling and fault-detection workload. |
| State behavior | Missing/stale audio produces no wake, transcript or intent. Power restoration accepts only fresh audio. |
| Protection / containment | Audio-input fault or USB connection must not reset C2, energize motors or back-power the SBC when compute is off. |
| Measurement | Front-end or supplying-branch `V/I`; device availability/frame age; configuration and temperature where relevant. |
| Fault trace | `F-21`; G02/G04 |
| Open dependencies | RP-05 front-end selection and SBC interface. Blocks branch placement, compute-rail demand and back-power design. |

### `LG-08` — Speaker and amplifier

| Field | Requirement |
|---|---|
| Boundary / class | Amplifier power input and stated speaker load/gain; `EC-N` |
| Configuration | Unselected. |
| Supply contract | Rail source, voltage range, quiescent demand, crest demand and enable/mute behavior are `U`. Noisy load must not share a failure path with C2; compute coupling must be bounded by later architecture and measurement. |
| Profiles / cases | `LP-08-OFF/IDLE/CHIRP/ALARM/MUSIC/CREST/SINEREF`; case binding per `load-model.md`; off while charging and after shutdown. |
| Demand characterization | Enabled-silent current, authored RMS, crest width/repetition, alarm duty, startup/pop transient and fixed-load reference. |
| State behavior | Safety may pre-empt audio. Mute/off transition cannot delay hazardous stopping. Restored audio does not replay a cancelled annunciation or action. |
| Protection / containment | Amplifier short/overload and supply noise must not reset C2, corrupt internal control or energize motors. Speaker output is not used as proof of electrical safety state. |
| Measurement | Input signed `V/I`, amplifier/speaker temperature, audio file/gain/load and synchronized crest captures. |
| Fault trace | `F-10`, `F-20`; G01/G02/G03 |
| Open dependencies | RP-05/RP-06 amplifier, speaker, authored levels and acoustic/thermal envelope. Blocks rail selection, protection and thermal sizing. |

### `LG-09` — Conversion and distribution losses

| Field | Requirement |
|---|---|
| Boundary / class | Derived residual between source input power and synchronized load-boundary powers; no `EC` class |
| Configuration | Initially an `E` planning allowance; later attributed to named converters, protection, conductors and connectors. |
| Supply contract | Not a physical rail and never commanded. Sign and uncertainty must be preserved; unexplained negative or implausible residual is a data-quality finding. |
| Demand characterization | `P_source − ΣP_load` with aligned timestamps and declared coverage. Thermal loss is assigned to physical components as evidence matures. |
| Measurement | Source `V/I`, synchronized branch `V/I`, instrument uncertainty and sampling alignment. |
| Gate trace | G02/G03 |
| Open dependencies | Complete branch instrumentation and selected architecture. Retire the blanket percentage when losses can be physically attributed. |

### `LG-10` — Base MCU and obstacle/edge safety sensing

| Field | Requirement |
|---|---|
| Boundary / class | Base local controller plus required obstacle/edge sensing and interfaces; `EC-S` whenever its safety coverage is a motion precondition |
| Configuration | **ESP32-S3-DevKitC-1-N8 selected as the C3 prototype board under `RP02-P3-REG-02`.** It preserves GPIO35–37; RP-03 owns the motor driver, sensors, final pin map and update schedule; a later WROOM-1-N8 carrier requires controlled equivalence. |
| Supply contract | Exact voltage, UVLO/reset behavior, sensor emitter pulses and independence from drive-stage disturbances are `U`. It must remain valid while base hazardous energy is present or being removed. |
| Profiles / cases | `LP-10-OFF/BOOT/IDLE/MOTION/OBSTACLE/EDGE/FAULT`; active for drive/tabletop calibration cases; off during charging and after final shutdown. |
| Demand characterization | Boot, idle sensing, active control, emitter pulse alignment, obstacle/edge maximum schedule and fault-processing demand. |
| State behavior | Boots with driver inhibited. Reset, absent/stale sensor evidence or control-app authority loss produces the registered local stop/inhibit and no stale wheel command after recovery. |
| Protection / containment | Drive-stage, sensor and SBC faults must not defeat hardware-safe driver state. Its supply may share an upstream safety source only if local branch protection and common-impedance analysis preserve independence. |
| Measurement | Terminal `V/I`; controller reset reason; sensor validity/age; driver-enable state; detection-to-brake trace and temperature. |
| Fault trace | `F-17`, `F-19`, `F-22`, `F-24`, `F-26`, `F-28`, `F-30`; G01/G02/G04/G05 |
| Open dependencies | RP-03 motor-driver/sensor set, final C3 carrier/pin map and measured load. Blocks final safety-rail rating, drive-enable circuit and base fault qualification. |

## 5. Source-side electrical requirements

Source interfaces are not forced into the `LG-*` consumer namespace. Their stable physical IDs and any new Part-2 charge profiles will be issued with the approved topology. This closes the requirement gap deliberately left by the Part-1 `CC-15` row without altering the registered Part-1 vocabulary.

### Onboard battery/pack interface

| Field | Requirement |
|---|---|
| Boundary / class | Pack output terminals through pack-integral protection as selected; source feeding all robot domains; pack monitoring contributes to `EC-Q` and safety policy |
| Configuration | Chemistry, series/parallel count, cell form, protection construction and service model unselected in the registered basis. **Working selection 2026-09-24 (builder direction, not registered): 2S1P Li-ion NMC 18650 pack, two Samsung INR18650-25R cells + 2S 20 A balanced BMS, retained module with the SBS Mini lead.** Every contract row below still needs the measured values. |
| Source contract | Full/nominal/depleted loaded voltage, permitted continuous/pulse current, pulse duration/recovery, internal impedance across state-of-charge/temperature/age, allowable reverse charge/regeneration, disconnect behavior and fault-current capability are all required; values remain `U/E/D/W` in the ledger. |
| State behavior | Supplies untethered operation; supports `EN-02/03` detection above loss of controllability; cannot restore stored motion after replacement/reconnection; charging behavior follows `CC-15`. |
| Protection / containment | Cell/pack protection functions and trip/recovery behavior must be enumerated, not inferred from “BMS/PCM.” A main fuse remains required unless the selected architecture proves an equivalent bounded path. Pack removal/isolation cannot be bypassed through charger, USB, programming or signal returns. |
| Bidirectional effects | Must explicitly accept, limit or reject drive/head regeneration. An opened BMS or full pack must not leave regenerative energy without a safe destination. |
| Measurement | Pack-terminal signed `V/I`, temperature at defined points, protection state, loaded internal-resistance evidence and charge/discharge energy. |
| Trace | `CC-13H/D`, `CC-14`, `CC-15`, `MD-01`; `F-11`, `F-16`, `F-18`; G01/G02/G03/G06 |
| Open dependencies | Servo/drive profiles, chemistry and pack construction, regeneration envelope, body mass/volume and service path. Exact capacity remains outside Part-2 architecture closure. |

### External low-voltage charge input and onboard charge/power path

| Field | Requirement |
|---|---|
| Boundary / class | Keyed external low-voltage connector through input protection, chemistry-specific charger/load sharing and pack connection; `EC-Q` |
| Configuration | External certified AC/DC adapter and onboard charger/power-path hardware unselected; AC mains remains outside Makad. |
| Input contract | Adapter voltage/current/tolerance, connector polarity, insertion/removal transient, inrush, reverse-polarity behavior and source current limit are `U` until topology and chemistry selection. |
| Output/load contract | Correct chemistry/S-count charge algorithm; documented behavior with the registered display plus minimum supervision load; explicit pack-present, pack-absent, full, fault and input-loss behavior. |
| State behavior | Accepted charge input enters `OM-06 + EN-04`; motors remain hardware-inhibited; SBC, camera, microphones, ordinary audio and base sensing are off; display and minimum supervision remain. Charge removal/completion/fault cannot restore Floor/Table or old motion. |
| Protection / containment | No charger-to-motor bypass, no backfeed to the adapter, no signal/USB bypass around main isolation, and no unsupported termination behavior under system load. Stored input/output capacitance and hot-plug energy must be bounded. |
| Thermal requirement | Charger, pack, connector and display/minimum-supervision heat are evaluated together under `CC-15`; thresholds remain preregistration items. |
| Measurement | Input and pack signed `V/I`, charger/status state, pack/charger/connector temperatures, motor-rail absence and display/supervision logs. |
| Trace | `CC-15`; `F-18`; G01/G02/G04/G06 |
| Open dependencies | Chemistry/S-count, pack interface, charge-status owner, display charge demand and body connector/service layout. `PB-CHARGE-IN` and `PB-CHARGE-LOGIC` now hold the implementation-dependent charger/power-path requirements. |

## 6. Required physical branch boundaries before topology selection

The next architecture subpart must account for every function below. This list does not prescribe converter count, grounding topology or component choice.

| Required boundary | Loads/functions | Non-negotiable requirement |
|---|---|---|
| Source and main isolation | Pack to complete robot | One accessible isolation action; no unprotected downstream path before branch protection |
| Charge input/power path | External low-voltage input, charger, pack and charge load | Keyed/polarity-safe; no AC inside; explicit load sharing, backfeed and pack-present/absent behavior |
| Safety supervision | `LG-02`, later applicable `LG-10`, E-stop/rail/pack sensing | Independent of display and hazardous-load failure branches; valid while actuator energy is removed |
| Mission compute | `LG-01` and attached loads as selected | Reset/short cannot reset safety supervision; clean power-down behavior defined |
| Display/status | `LG-05` | Independent failure containment from C2; available in charging mode without SBC |
| Camera/audio input | `LG-06/07` | Shed/off states implementable; no signal-cable back-power |
| Audio output | `LG-08` | Noise/crest contained; mute/off independent of stopping authority |
| Head actuator feed | `LG-03Y/P/R` | E-stop-controlled; per-axis observability and fault containment; moving-path drop and return explicit |
| Drive actuator feed | `LG-04` | E-stop-controlled; safe hardware enable; regenerative path explicit |
| Base safety/control | `LG-10` | Supply and hardware enable remain valid through drive stopping; off in charging |
| Measurement/telemetry | Source, rail and load-end points | Does not create an unprotected or back-power path |

## 7. Coverage audit

| Check | Result |
|---|---|
| Pack and charge source interfaces | **Covered:** `PB-MAIN`, `PB-CHARGE-IN` and `PB-CHARGE-LOGIC` are registered; numeric source profiles and hardware behavior remain open |
| Every registered `LG` has a load-side contract | **Covered:** `LG-01…10`, with Y/P/R retained separately and `LG-09` treated as derived |
| Every registered `LP` has an owning contract | **Covered by family:** exact profile definitions remain in `load-model.md` |
| Credible versus synthetic concurrency | **Separated:** `CC-PEAK-01` versus `ST-01` |
| Mixed-duty energy | **Bound:** `MD-01`; numeric energy remains in ledger |
| E-stop and restoration | **Bound:** `EDB-04`, cross-cutting table, `LG-02/03/04/10` |
| Charging | **Bound at requirement level:** implementation awaits topology/pack/charger decisions |
| Returns, regeneration, stored energy and back-power | **Required:** implementation and calculations await later subparts |
| Independent C2 safety supply | **Approved requirement:** converter/branch implementation awaits topology |
| Physical branch contracts | **Issued:** `power-branch-contracts.md` uses `PB-*` keys registered under `RP02-P2-REG-01`; numeric population remains evidence-dependent |
| Numeric acceptance thresholds | **Open:** register in `gates.md` before scored evidence |

## 8. Remaining implementation and sizing inputs after `RP02-P2-REG-01`

The approved architecture resolved the domain, energy-route, return, charge-permission and branch-containment questions exposed by `EDB-03`. The following are inputs to later Part-2 subparts, not omissions in the load or branch contracts:

1. battery chemistry, series/parallel count, retained pack construction and admissible source envelope;
2. charger/load-sharing implementation, including pack-present/absent and reverse-current behavior;
3. system-power latch, source-selection, motor-arm and E-stop switching implementations;
4. servo and drive voltage/conversion choices plus regeneration and stored-energy handling;
5. protection device classes, ratings and time-current/energy coordination;
6. converter ratings, transient response, efficiency, thermal limits and startup behavior;
7. conductor sizes, connector families, pin assignments, shield terminations and harness derating;
8. numeric population and selection evidence for the issued branch-side `EDB-03` records;
9. environmental assumptions and mechanism-specific margins;
10. final numeric thresholds, instruments and test configurations before scored qualification.

## 9. Approval and revision record

| Date | Scope | Approval/evidence |
|---|---|---|
| 2026-09-15 | `EDB-01…08` principles | Explicit builder approval in the project conversation: “i approve these principles, good foundation” |
| 2026-09-16 | `EDB-03` schema, cross-cutting requirements and first source/load-side register | Explicit builder approval in the project conversation: “cool i approve, now continue”; no new behavior, component selection, numeric threshold or evidence-class promotion |
| 2026-09-16 | Part-3 identity reconciliation | Consumed `RP02-P3-REG-01` selected Active Cooler and C3 prototype identity without changing any `EDB-*` rule or promoting a numeric load/evidence class |
| 2026-09-16 | C3 suffix correction | Consumed `RP02-P3-REG-02`: N8 supersedes N8R8 for C3 to preserve GPIO35–37; no `EDB-*` or load evidence changed |
