# Prototype open items

| Field | Value |
|---|---|
| Status | **Living index.** Not a competing decision, budget, CAD or gate record |
| Created | 2026-09-16 |
| Scope | Remaining work inside `docs/02-prototypes/` after RP-01 Layout 03 paper demand, RP-02 Parts 1–4 design-definition, RP-03 Parts 1–5, and RP-04 Phase A design-definition (`RP04-P1-REG-01`…`P6-REG-01`) |
| Rule | Canonical detail stays in the cited file. Close an item there first, then strike or rewrite the row here. An index line cannot freeze a SKU, promote `E` to `W`, or register a gate |

This file exists so an “intentionally open until the physical input exists” statement does not disappear into a local README. The latest RP-02 example is the same class of claim as the older RP-01 ones: **final wire, fuse, converter and pack ratings remain intentionally open until their required physical inputs exist.**

Closed work is listed only so it is not reopened by accident.

## How to read a row

| Column | Meaning |
|---|---|
| Item | What is still unresolved |
| Why it is open | Missing evidence, missing hardware, or an explicit later owner |
| Waiting on | The next real input, not a hoped-for conclusion |
| Home | Owning record |
| Blocks | What cannot honestly close until this row moves |

Evidence classes are unchanged: `W` measured on the named hardware, `D` manufacturer source, `E` estimate/substitute, `U` unknown/unselected and never zero.

---

## Shared blockers (all prototypes)

These sit above RP-01 through RP-04. Scored physical runs wait here even when paper work is live.

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Stage 0 workbench / powered-test gate | Tools are specified; the scored-test checklist is not satisfied | Arrival, acceptance tests, fixture E-stop/isolation, logging | `../../01-system/workbench.md`; RP-01 `rig.md`; RP-02 `RP-02-electrical/rig.md`; RP-03 `RP-03-locomotion/rig.md`; future RP-04 `rig.md` | Any scored RP01/RP02/RP03/RP04 run |
| Battery handling gate | Pack work is deferred until procedure, bag and charger exist | Written procedure + hardware | `../../01-system/workbench.md`; RP-02 Phase C | G03 rehearsal, charging G06, ADR-06 sizing |
| Monotonic timebase | Strategy written; not implemented or validated | `TIME_SYNC` on DevKitC-1, then G05 | `../../01-system/timebase.md`; `RP-02-electrical/link-contract.md` | First scored RP-01 run; ADR-12 |
| Purchase authorization | Selection ≠ buy | Explicit builder buy for each part | `../../01-system/candidate-sourcing-matrix.md`; each `decision.md` | Installed `W` rows |
| System numeric TBDs | Energy, thermal, acoustic and cost thresholds are not registered | SC-TBD-03/04/10/12, CON-TBD-13 and related brief rows | `../../01-system/system-design-brief.md`; RP-02 `gates.md` | G02 temperature, G03 reserve, later ADRs |
| Production camera interconnect | Module selected; moving CSI construction is not | Harness study + RP-01 live-signal work | `../../01-system/head-harness-routing-study.md`; camera study | RP01-G04 wiring; RP-02 `PB-CAMERA` ratings |

---

## RP-01 Head

**Current outcome:** ITERATE. Concept A and Layout 03 external rigid-body demand are retained. Paper approval, fabrication release, actuator freeze and scored gates remain OPEN.

### Mechanism and paper screen

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Actuator family / SKU | C01 (XC330-M288-T) is a named comparison only; paper approval OPEN | Close or bound P01–P08, then freeze | `RP-01-head/actuator-screen-01.md`; `gates.md` P01–P08; `decision.md` | PA-04 servo rail; Phase B real head load; ADR-02 |
| Actuator-internal inertia / acceleration current | Payload-side `Jα` is not complete electromechanical demand | Official rotor/gear inertia **or** unloaded-vs-loaded characterization | `fullproofmath.md` §12; `actuator-screen-01.md`; P03/P05 | Complete paper pass; operating current for RP-02 |
| Pitch-frame stiffness | Screen ~6–9 Hz vs 30/40 Hz laugh targets | Stiffen, then FEA or loaded tap / ring-down | `fullproofmath.md` §12; `gates.md` P07 | Pitch/roll C01 credibility; G03 modal cases |
| Roll-saddle stiffness | Screen ~21 Hz vs 25/30 Hz | Same as pitch | same | Roll wobble cases |
| Two retainer-screw collisions | Fasteners overlap rolling-cradle flange/ear stalk (~5.53 mm³ each) | Geometry fix + fastener-inclusive motion grid | `cad/head/layout-03/review/verification.md`; P08 | Fabrication; CAD freeze |
| Hard stops vs usable travel | CAD contact equals provisional usable limits; storyboard requires margin beyond | Move stops; check pin/load path (~30–35 MPa first-order shear is unresolved) | Layout 03 README; `storyboard.md`; P08 | Usable-range proof; G01 rest |
| Bearing SKU | Ø16.2 × 6.2 mm trial seats only | Select real bearing, then seat/preload/retention | Layout 03; `cad/head/decisions.md` HEAD-CAD-02 | Purchased-fit; P08 |
| Storyboard ↔ CAD/firmware signs | Yaw and roll positives oppose raw CAD right-hand; pitch agrees | Document multipliers at the public motion interface | `fullproofmath.md` §12; `gates.md` P08 | Signed load/firmware |
| Physical balance trim | A0 residuals are solver output, not millimetre fabrication | Measured trim/adjustment path | `fullproofmath.md` §12; HEAD-CAD-07 | Hold torque; candidate substitution |
| Bearing reactions, spindle bending, yaw-yoke stiffness | Not in the paper record | Calculation or representative test | `fullproofmath.md` §12 | Support-layout credibility |
| C01 5 V sag floor and speed-source conflict | Proposed 5 V; 3.7 V is a sensitivity endpoint; ROBOTIS 65 vs 81 rpm unresolved | Rail budget + labelled curve/source; later servo-terminal logging | P02; `actuator-screen-01.md` | Yaw envelope; PA-04 collapse |
| C01 thermal / RMS as measured | 0.186 N·m manufacturer estimate is a screen, not enclosure duty | Duty/ambient/mounting evidence | P04 | Family freeze |
| Faster yaw comparison (XC330-M181-T) | Named only if 5 V floor or speed conflict cannot be resolved | Same paper gates as C01 | `actuator-screen-01.md`; RP-02 candidate register | Optional family path |

### Mass, material, CAD and harness

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| M008 installed C2 mass | Board selected; assembly unweighed | Weigh board + mount + connectors + local harness | `payload-mass-capture.md`; CTRL-04 | Complete-head `W` (M900); physics tree lock |
| All accepted physical masses | Layout 03 is D/E | Per-part `W` after print/kit | `payload-mass-capture.md`; D-08 | Registered ballast; G02–G06 |
| M010–M012 PLA thermal/creep | Provisional by D-03 | Preregistered dwell at sealed-head temperature | `material-finish-mass-decision.md`; `rig.md` | Structural material; D-03 close |
| Finish-system coupon | Required before coating the shell | 60 × 60 mm nine-step coupon, ≥24 h, g/cm² + visual | `rig.md`; D-05 | M019a coating; G05 |
| Insert / internal fastener SKUs | Visible M2 locked; internals and inserts unselected | Trial coupon + SKU | HEAD-CAD-01; Layout 03 | Repeated service joints |
| Rolling-ear clearance / attachment geometry | Ownership locked; fit still to demonstrate | Combined-motion sweep | HEAD-CAD-03 | Cosmetic/service freeze |
| Depth challenge (110–115 vs ~90 mm) | Current core vs blockout | Choose before CAD freeze | `gates.md` candidate matrix | Shell mass/moment |
| CAD-04 / CAD-04a flashing paths | Requirements exist; sealed-head demonstration does not | Display and C2 USB/BOOT recovery with cover on | `cad/head/requirements.md` | G05/G06 service |
| CAD-05 yaw demate | Reserve modelled; connector/construction open | Selected connector + weigh-without-cut | requirements; harness study | M020/M900 |
| Live harness (H1/H2/H3) | Jackets illustrative; roll/pitch transitions open | Real cables, radii, CSI orientation, endurance | Layout 03 verification; harness study | G04 wiring; restoring torque |
| Camera FPC vs production interconnect | 200 mm sample is bench hardware | Production moving CSI | `payload-mass-capture.md` | Camera `W` and G04 |
| Optical certification | Flared aperture clears a conservative envelope | Entrance-pupil measurement | Layout 03 optics | Camera usability claim |
| Body integration / 304 mm stack | Head envelope only | RP-06 | Layout 03 README | System height |

### RP-01 process remaining

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Paper gates P01–P08 | Draft v0.2; builder freeze pending | Dated approval after blockers above | `RP-01-head/gates.md` | Honest C01 paper pass |
| Physical gates RP01-G01…G06 | None registered | Configuration, thresholds, instruments, repetitions, freeze **before** inspecting scored data | `gates.md`; `decision.md` | RP-01 closure |
| Rig | Not started | Workbench gate + named servo load + registered gates | `RP-01-head/rig.md` | Scored motion |
| Storyboard thresholds | Authored kinematics, not pass/fail | Builder review + `gates.md` freeze | `storyboard.md`; `intent.md` | G02/G03 cases |
| Eye/audio placeholders | RP-01 does not require them | RP-04 / later | `intent.md` | Coordination only |
| Passive rest / unpowered settle | SD-02 requires a safe down rest; gearbox ratio is not evidence | HM-00 measurement | `physics.md`; `gates.md`; RP-02 SD-02 | Sleep load model |
| Servo bus protocol, rate, homing | Follows family freeze | Selected SKU | CTRL-04; link-contract out-of-scope note | C2 firmware; G05 servo bus |
| Concept B | Explicitly waived 2026-09-09 | Do not reopen without a new decision | `decision.md` | — |

---

## RP-02 Electrical / control

**Current outcome:** Parts 1–4 are complete at design-definition level. Part 4 registers the C0↔C2 ICD definition as `RP02-P4-REG-01`, C0↔C3 `BASE_*` **semantics** as `RP02-P4-REG-02`, and coordination fields as `RP02-P4-REG-03` (2026-09-21). Exact byte layouts remain open. No gate passed, no ADR closed, no purchase authorized.

### Intentionally open until physical inputs exist

This is the class that prompted this index. Architecture and calculation method are in place; **ratings are not**.

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| **Final wire, fuse, converter and pack ratings** | Equations, sensitivity tables and `PCD-*` candidate screen exist; installed path, protection curves, converter maps and pack impedance do not | Candidate-screen evidence list, then one conditional term at a time | `RP-02-electrical/power-calculation-ledger.md` §8; `power-component-candidate-screen.md` §12 | G01; ADR-06 architecture evidence |
| Battery chemistry, S-count, pack construction | PA-03/04 and `PB-MAIN` admit the servo/drive outcome; 2S 6.0–8.4 V is an `E` planning case only | RP-01 family + RP-03 drive envelope + handling | `electrical-design-basis.md` §8; `decision.md` | Charge path; G03; ADR-06 sizing |
| Charger, adapter, keyed charge connector | STUSB4500QTR + BQ25798 is the screened architecture lead, not selected; adapter/settings/body inlet open; AC stays outside Makad | Chemistry, charge power, PDO and body layout | `power-component-candidate-screen.md` §9; `power-branch-contracts.md` `PB-CHARGE-*` | `CC-15`; G06 |
| Charge-insertion motor-arm timing | Conservative bench rule is immediate motor-arm removal; the selected circuit may instead allow a short supervised brake before `CHARGE` is accepted | Source-selector/charger circuit plus a registered stop timing | `power-implementation-basis.md` §8.4; `CC-15`; F-18 | Charge-mode G01/G04 configuration |
| Motor-arm, source-selector, E-stop switching devices | IDEC XW1E operator and LTC4368-1/external-FET approach are screened leads, not a selected safety subsystem | Fault-current, FET SOA, regeneration and interruption calc | `power-component-candidate-screen.md` §6; `power-architecture.md` PA-13/14 | G01 demonstration |
| Servo-rail conversion (direct vs motor-domain buck) | Coupled to family; C01 implies regulated 5 V from a 2S planning case | RP-01 freeze (PA-04) | `decision.md`; `power-implementation-basis.md` | Head conductor/fuse |
| Drive conversion and regeneration sink | RP-03 hardware absent | Drive `W` profiles | `PB-DRIVE*`; ledger `LG-04` | `CC-09/10/11`, `CC-PEAK-01`, G03 |
| Connector families, pinouts, shield terms, gauges | SBS Mini, Micro-Fit 3.0/Micro-Fit+ and gauge classes are screened; exact assemblies and moving cable are not selected | Path lengths, exact terminals and current/flex envelopes | `power-component-candidate-screen.md` §§7–8; `power-implementation-basis.md` §§3–5 | Harness buy; G01 |
| Branch-local capacitance / hold-up / UVLO numbers | `BR-*` policy and calculation method are issued; numeric inputs are not | Selected converter/controller minima, stop/gate/discharge timing and load/source transients | `brownout-restart-contract.md` §§4, 6, 9; G02 candidate | Reset immunity claims |
| Brownout thresholds, debounce and stable-clear dwell | Ownership/order are defined, but chemistry, path impedance, monitor accuracy and safe-stop reserve are not measured | Selected pack and power path plus `CC-13H/13D/14`, fast-collapse and rebound captures | `brownout-restart-contract.md` §§4, 8, 9 | `EN-02/03` scored configuration; ADR-06 low-energy evidence |
| Numeric `LP-*` waveforms | Vocabulary frozen; bindings wait on real or admissible substitutes | Frozen run configuration | `load-model.md`; `state-register.md` | Scored G02/G03 |
| Energy thresholds, grace, fixtures, rates | Explicitly approved as open | Freeze before the scored run that uses them | `state-register.md` “Approved open parameters” | Any scored RP-02 case |

### Selected but still open (do not treat as closed)

| Item | What is already true | What remains open | Home |
|---|---|---|---|
| Raspberry Pi 5 2 GB (`LG-01`) | Selected 2026-09-16 under `RP02-P2-REG-02`; 5.1 V nominal / 5 A-capable `PB-COMPUTE`; official Active Cooler selected under Part 3 | Purchase, power-entry/PD hardware, enclosure cooler validation, storage, workload `W` | `decision.md`; `power-implementation-basis.md`; `compute-control-component-screen.md` |
| C2 Waveshare ESP32-S3-Zero | Module and CTRL-01…06 locked | Installed power `W`, transceiver, pin map vs DevKitC-1, G05 loop/link | RP-01 decision; `load-model.md` |
| C3 ESP32-S3-DevKitC-1-N8 | Prototype board and ownership selected under `RP02-P3-REG-01/02`; N8 preserves GPIO35–37; **pin map v0.1 drafted** (`RP03-P4-REG-01`, ≥2 spare) | Purchase, driver/sensors (leads only), carrier, power `W`, G04/G05 | `compute-control-architecture.md` §3 v1.3; RP-03 `base-control-architecture.md` |
| Differential link + C2 display relay | Production physical/logical topology selected; THVD1451D SOIC is the current cost-down implementation lead; TTL bench-only, USB service-only | Exact THVD1451 suffix/package, protection/termination, carriers and G05 flex/noise evidence | `link-contract.md` v0.4; `compute-control-component-screen.md` v1.2 |
| External controller watchdog | TPS3436-Q1 window-watchdog family selected per C2/C3 | Exact timing/latch suffix and circuit from measured loop/boot windows; F-25/F-26 | `compute-control-architecture.md` CA-10; `compute-control-component-screen.md` |
| Display SKU 30493 | Selected; 5 V / 450 mA published `D` | Sample `W`, inrush, brightness, status light, charge-mode profile | ledger `LG-05`; `PB-DISPLAY` |
| Display onboard battery/charger path | Registered: do **not** feed the display’s single-cell charger from the robot pack; `PB-DISPLAY` enters through the documented 5 V input | Schematic review of whether unused onboard charge/battery circuitry needs physical disablement or may remain unconnected — this is a back-power / second-domain G01 item | `power-implementation-basis.md` §2.3 |
| Camera Module 3 Wide | Selected on CSI | Official/sample power, 22-to-15 CSI cable in the moving route, PDAF lock during gestures | camera study; `PB-CAMERA` |

### Still unselected hardware

| Item | Notes | Home |
|---|---|---|
| Status light | Display row selected; light is not | `LG-05` |
| Microphone front end (`LG-07`) | Pi 5 has no native 4-ch PDM; codec HAT vs USB array suggested only | `decision.md` candidate register |
| Speaker + amplifier (`LG-08`) | RP-05/06 | `PB-AUDIO-OUT` |
| Base motor driver and safety sensors (`LG-04/LG-10`) | C3 selected; **leads named** (D02, DRV8874-class, S01/S04/S06/S07) — not a freeze, not purchased | `PB-DRIVE*`; RP-03 screens |
| Pi storage exact SKU | Official Pi 32 GB A2 is the cost-down lead; SanDisk High Endurance 32 GB is the low-cost endurance comparison; official Pi 64 GB is capacity fallback; no selection | `compute-control-component-screen.md` `CCD-STO-*` |
| Differential transceiver/watchdog exact suffix and carriers | Families/topology selected; component suffixes and PCBs await measured conditions | `compute-control-component-screen.md` `CCD-LNK/WDG/HDL-*` |

### RP-02 process remaining

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Numeric G01–G06 registration | Candidate metrics only | Dated builder freeze before inspecting scored data | `RP-02-electrical/gates.md` | Any pass row in `decision.md` |
| Fault injection campaign | F-01…F-22 Part-1 plus F-23…F-30 Part-3 defined; none injected | Rig + G04 freeze | `fault-matrix.md` | ADR-03 / ADR-12 evidence |
| Distribution rig | Designed against registered architecture; not built | Instruments + Phase A/B hardware | `rig.md` | G01/G02/G04 |
| C0↔C2 wire codec (`link-contract.md` v1.0) | Part-4 registers **semantics** only (`RP02-P4-REG-01` plus `RP02-P4-REG-03` coordination fields). Exploratory layout revision 2 assigns candidate widths/type IDs and payload codecs (`phase-a/payloads.py`). Byte layouts, type numbers and numeric rates/timeouts are **not** G04/G05-registered. `EXP_ONLY_NOT_REGISTERED` | One registered schema, then TTL/differential implementation and G04/G05 freeze | `link-contract.md`; `phase-a/README.md` | ADR-12 |
| C3 drive message set | `BASE_*` **semantics** registered `RP02-P4-REG-02`. Candidate TTL/heartbeat/queue named and unregistered | Byte layouts after Phase A; measured timeouts | `link-contract.md` §v0.5; RP-03 `base-control-architecture.md` | Complete ADR-12; C3 G05 |
| C2/C3 board-role GPIO header and compiled hard maxima | C3 pin map v0.1 drafted; **`c3_board_role.h` generated** from v0.1 (`RP03-P4-REG-02`). C2 role map exists. Carrier PCB is not | Frozen board revisions; C2 generated header | `phase-a/c3_board_role.h`; `compute-control-architecture.md` v1.3; RP-03 pin map | Phase A firmware; arm-hash; G05; carrier |
| ADR-03 | Ownership fixed; evidence open | G05 on C2/C3 and G04 including authority-lease/external-watchdog paths with representative actuators | `decision.md` ladder | Controller backbone |
| ADR-12 | Open | Contract + G05 + `timebase.md` §6 | same | Internal comms |
| ADR-06 architecture | Topology/basis fixed; implementation pending | G01, chemistry, remaining power parts, RP-06 layout | same | Rails/isolation/policy |
| ADR-06 sizing | Expected after RP-03, not in stage 2 | Ledger `W` for every `LG`; G03 margin | same | Pack capacity |
| Phase A remaining | Part-4 definition, exploratory host codec/state model and unscored G01/G06 paper review are recorded. Host tests are not a scored G04/G05 run. No attached DevKitC serial device was available | Board-role GPIO header, ESP-IDF twin, TTL then differential loopback, edge-stamped timebase, immutable log ring / pre-run write check, exploratory injections. Do not score Phase A layouts as `RP02-P4-REG-01` | `RP-02-electrical/phase-a/README.md`; `intent.md` phase ladder | Unblocks RP-01 scored path |
| Phase B | Needs a named RP-01 servo load (C01 as reference is allowed; purchase ≠ family freeze) and the selected Pi 5 | Those parts on the bench | `intent.md` | G05 servo bus; head+compute G02 |
| Phase C | Battery gate | Pack + procedure | `intent.md` | G03 rehearsal |
| Drive-dependent cases | `CC-09/09C/09R`, `CC-10A/B/C`, `CC-11`, `CC-12C`, `CC-13D`, drive share of `CC-PEAK-01`/`ST-01` | RP-03 hardware | `gates.md` G02 note | Whole-robot peak claim |
| SC-14 20-minute Core | Not an RP-02 closure | Integrated droid | plan; G03 | CON-10 |

---

## RP-03 Locomotion

**Current outcome:** Parts 1–5 are complete at design-definition level (`RP03-P1-REG-01` … `RP03-P5-REG-01`, 2026-09-17). Brief-gap close 2026-09-18 issued `RP03-P1-REG-02` … `RP03-P4-REG-02`. **V1 front support is `D21` ball (BD-08, baseline v1.12, SCOPE-09 v1.3).** Concept A chassis/sensing retained. `D20` caster is the required swap. Set A / D02 / DRV8874-class / S01/S04/S06/S07 are leads, not a freeze. No purchase, no gate passed, no scored run. ADR-04 not closed.

### Intentionally open until physical inputs exist

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| `a_tip` as a measured number | Paper range 0.9–1.9 m/s² (and sign reversal if battery is on/behind the axle); 1.98 m/s² remains a placement target | BD-05 ballast on the rig; then M900 | `RP-03-locomotion/physics.md`; `dimensional-baseline.md` v1.11 | Point G01 lift-onset margin; dimensional-baseline revision if +25/124 is missed |
| Builder decisions `BD-01…08` | `BD-01…07` paper-confirmed 2026-09-18. **`BD-08` (2026-09-19): `D21` selected V1 support, `D20` required swap.** Still not a gate freeze | Dated freeze at G01–G06 registration; `D21` dent/jam/drag on `S-LAM`/`S-RUG` | `RP-03-locomotion/decision.md`; `dimensional-baseline.md` v1.12 | Frozen G01–G06 thresholds; ADR-04 support type |
| Concept / motor / sensor freeze | Screens complete; **Set A / Set B** packaged; leads named. Paper P01–P09 scored against the sets and remain OPEN | Paper P-gates close or bound, then freeze | `concepts/`; `drivetrain-screen-01.md` v0.2; `sensing-screen-01.md`; `gates.md` §4 | Purchase; `cad/base/` blockout |
| C3 pin map firmware/carrier | v0.1 drafted; ≥2 spare; RGB released; GPIO3 ESTOP input exception; **`c3_board_role.h` generated** from v0.1 | Frozen board revision; carrier PCB | `base-control-architecture.md`; `RP-02-electrical/phase-a/c3_board_role.h`; `compute-control-architecture.md` v1.3 | RP-02 carrier PCB; RP02-G05 C3 |
| `BASE_*` ICD | v0.5 **semantics** registered `RP02-P4-REG-02`. Candidate TTL 200 ms / `duration+250 ms`, heartbeat 150 ms, queue depth 2 named and unregistered | Byte layouts after Phase A; measured timeouts | `link-contract.md` §v0.5; `base-control-architecture.md` | Complete ADR-12; C3 G05 |
| `LG-04`/`LG-10` `W` rows | Ledger v0.15 is still `E`/`U`; heat duty and 6.0 vs 8.4 V note recorded | Phase B/C runs | `power-energy-ledger.md` | ADR-06 sizing; G02 invariant re-run |
| `cad/base/` blockout | Concept A is a working lead, not a freeze. Brief asked for CAD pass 1 now; folder policy still forbids it | Concept freeze **or** an explicit policy change. Datums: `research.md` §5 | `RP-03-locomotion/cad/README.md`; `RP-03-locomotion/research.md` | Integrated CAD input; ball/caster 360° sweep; 0–15 mm front-support shim |
| RP-03 part envelopes for CAD | First paper pass 2026-09-19. Remaining `U`: India D02 encoder suffix, caster trail, gearbox radial, SPI IMU module outline, loaded wheel radius | Remaining `U` in `research.md` §6; cost/stock only in the sourcing matrix | `RP-03-locomotion/research.md`; `candidate-sourcing-matrix.md` v0.31 | Honest CAD pass 1; wheel family A/B/C chosen before hub print |
| Acted 240 fps mock-up | `plan.md` required; not run. V0.1/v0.2 kinematics are paper hypotheses | Weighted-box / caster-push recording, or a storyboard revision against it | `storyboard.md` v0.2 change log | Confidence in come/wiggle timings |
| D02 stall-current `D` conflict | Oz 900 mA vs NFP ≤3 A, both manufacturer tables | Meter the purchased article (if bought as bench equipment) | `drivetrain-screen-01.md` P03 | Korad 5 A both-motor claim; driver-class confirmation |
| Analog-IR 0.70 m/s look-ahead | GP2Y 300 mm is tight against 289 mm `d_stop`; 2.0° downhill at 0.50 makes 221 mm | Caster-mount proof at 0.50; longer-range stop-path or slower 0.70 if G02 uses that band | `sensing-screen-01.md` P09; `physics.md` §6 and §10 | 0.70 m/s obstacle case; 0.50 downhill coverage |
| Drive mass row `W` | 200–600 g bound unchanged | Selected drivetrain weighed | `mass-envelope-ledger.md` | Whole-robot roll-up; RP-06 |
| CON-TBD-14 | 250 mm radius / 0.06 m/s / 40 mm margin **proposed** | G04 freeze then Phase C evidence | `physics.md` §8; `gates.md` G04 | SC-13; SC-TBD-09 |
| Both-motor stall/reversal transients | Korad 5 A ceiling | Phase C pack or second source | `physics.md` §5; `workbench.md` | `CC-PEAK-01`, `CC-10A/B` |
| Scored G01–G06 | Candidate registrations only; registered section empty. Cutoff-coast is now a candidate metric | Workbench gate, timebase, threshold freeze **before** data, rig built | `gates.md`; `rig.md` | ADR-04/ADR-07 |

---

## RP-04 Coordination

**Current outcome:** Phase A design-definition 2026-09-21 (`RP04-P1-REG-01`…`P6-REG-01`). Virtual composer **`CS-HYBRID`** with bounded wait language. TIME/PROG adapters retained. Architecture-family research **closed**. P-02 cue list **validated** (declarative). Exploratory packed layout revision 2 in RP-02 `phase-a/` (`BASE_STATE` 62 bytes, safety retained). `BD-05` household observer panel **superseded**. `BD-08` counter-yaw locus **open**. G03: tune on non-scored runs, freeze, then scored capture. IR wire semantics **accepted** `RP02-P4-REG-03`; packed layout **not** G04-registered. No physical gate. ADR-05 open. **RP-04 remains blocked on Phase B/C evidence.**

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Wake phase-gate / face-deny stall | **Virtual closed** (`any(face, light)` + `T-DEAD`). Physical cells unrun | Phase B `TR-P01-DEN-F` / `DEN-L` | `research/experiment-spec.md` §5; `p01_harness.py` | Honest G04 `W` |
| P-02 cue-list sufficiency | **Paper closed.** No executable spike | RP-03 base model, then P-02 harness | `situations.md` §12; `prototype/score.py` | Representation reopen only if discrete hand-off needs ad hoc runtime logic |
| `BD-08` counter-yaw locus | Primitive named on the behind-body list; owner and base-yaw source unset | Close before P-02 Phase C implementation | `decision.md`; `research/experiment-spec.md` §3 #7 | P-02 behind-body execution |
| Physical trial matrix | **Draft** preregistration. N, thresholds, injection magnitudes, selection rules unset | Freeze those in `gates.md` before scored data. Do not promise p99 until `n` supports it | `research/experiment-spec.md` §5 | G01–G05 |
| G03 N / pass / clip-selection / SC-TBD-01 | Draft questions exist; not registered | Non-scored engineering runs, then freeze N/pass/clip-selection in `gates.md`, then scored capture. No household panel (`BD-05`) | `observer-protocol.md`; `gates.md`; `research/experiment-spec.md` §§6–7 | RP04-G03; ADR-05 |
| Packed ICD / codec | Exploratory layout revision 2 assigns widths/type IDs and round-trips `TIME_MODEL_INVALID` / `LATE` / `STALE_EPOCH`. Not a registered ICD | RP-02 G04/G05 freeze | `link-contract.md` v0.6; `phase-a/schema.json` | Physical TIME tags; scored join-by-identity |
| `BASE_STATE` payload vs 64-byte candidate | **Exploratory resolve:** 62 bytes with identity, onset, `ctrl_state`, `mode`, `sensor_valid_mask`, `oldest_sensor_age_ms` retained. Do not drop safety fields | RP-03 sensor freeze, then RP-02 registered layout | `phase-a/payloads.py`; `link-contract.md` v0.6 | Registered base cue correlation |
| Source vs witnessed onset | Virtual nodes emit source onset only | Part 6 measurement defs; timebase; camera/mic | `timing-budgets.md`; `gates.md` G01 | G01 `W` |
| P-03 backpropagation | Stub | After P-01 Phase B | `situations.md` | Full P-03 spike |
| `BD-06` / G05 count | Deferred | Runtime cost, then freeze | `decision.md` | RP04-G05 |
| Phase B physical composition | No scored RP-01+D1+timebase co-rig | Upstream rigs | `gates.md`; RP-01 `rig.md` | Real P-01 G01/G02/G04 |
| Phase C | No RP-03 G06 base | RP-03 G01/G02/G06 | RP-03 `gates.md` | P-02/P-03; ADR-05 |
| Numeric G01–G05 | Candidates only | Freeze before scored data | `gates.md` | Any RP-04 pass |
| ADR-05 | Virtual select ≠ close | G01–G05 measured | `decision.md` | Coordination ADR |

---

## Circular dependencies (named, not stalled)

| Loop | What can proceed now | What must wait |
|---|---|---|
| RP-01 mass ↔ RP-02 rail | Layout 03 **paper demand** is complete without M008 `W`. RP-02 Phase A runs on paper and on-hand boards. | Complete-head `W` waits on M008. PA-04 **collapses only on family freeze**, not on a C01 purchase. |
| RP-01 P02 sag floor ↔ RP-02 servo rail | RP-02 records C01 5 V as a leading working assumption. | Loaded servo-terminal floor is a measured rail result. |
| RP-01 first scored run ↔ RP-02 timebase/G05 | Exploratory timing on DevKitC-1. | Scored RP-01 timestamps need implemented `timebase.md`. |
| G02 invariant ↔ later prototypes | Non-drive rehearsal can start when head+compute exist. | Drive, speaker and later loads force a re-run; they do not delay Phase A. |
| RP-03 scored runs ↔ RP-02 timebase/logging | Exploratory bench capture on C3 now | Scored G01–G06 need implemented `timebase.md` |
| RP-03 message set ↔ RP-02 link contract | `BASE_*` **semantics** registered (`RP02-P4-REG-02`) | Byte layouts wait on Phase A |
| RP-03 pin map ↔ RP-02 C3 carrier / `CA-14` | Pin map v0.1 on DevKitC, ≥2 spare; `c3_board_role.h` generated | Carrier PCB waits on a frozen map |
| RP-03 drive `W` ↔ ADR-06 sizing | `E` ranges in ledger v0.15 | Sizing waits on Phase B/C `W` |
| RP-03 stability ↔ RP-01 head mass | Range analysis with Layout 03 `E` tree | Point `a_tip` waits on M900; RP-03 scores at BD-05 corners |
| RP-04 coordination ↔ RP-02 byte layout | IR **semantics** accepted `RP02-P4-REG-03`; exploratory layout revision 2 packs identity, `start_at_us`, and NACK reasons | Registered layout; G04/G05; physical TIME |
| RP-04 scores ↔ observer protocol | Draft G03 questions + catalogue. Engineering-tune on non-scored runs | Freeze N/pass/clip-selection, then scored capture |
| RP-04 software budgets ↔ RP-01/RP-03 models | `E` budgets; virtual P-01 wait language closed | `W` G01; ADR-05 |
| RP-04 audio/eyes ↔ RP-06 | Semantic `A-*`/`E-*` timing | Quality/artwork |
| RP-04 architecture ↔ research | Family closed (`CS-HYBRID`); P-02 cue list validated; experiment spec software items closed | Physical G01–G05; `BD-08`; Phase B/C |

---

## Already closed — do not reopen from this index

| Closed | Record |
|---|---|
| Concept A path; Concept B waived | RP-01 `decision.md` |
| D-01…D-08 material/finish/mass policy (measured mass still open) | `material-finish-mass-decision.md` |
| CTRL-01…CTRL-06 C2 split and Zero module | RP-01 `decision.md` |
| Layout 03 **external rigid-body** demand and 1,560-case sensitivity | `fullproofmath.md` |
| Display SKU 30493; camera SC0874; C2 Zero; Pi 5 2 GB **selection** | studies + `RP02-P2-REG-02` |
| SD-01…SD-04; Part-1 states/cases/`MD-01` | `RP02-P1-REG-01` |
| `PA-01…16` and `PB-*` tree | `RP02-P2-REG-01` |
| Implementation-basis rules (not part ratings) | `RP02-P2-REG-02` |
| Calculation method for drop/loss/heat/energy/fuse coordination | `power-calculation-ledger.md` v0.1 |
| Manufacturer candidate discovery and `D/E` screen for conversion, protection, E-stop, connectors, cables and charging | `power-component-candidate-screen.md` v0.1; no selection or purchase implied |
| Brownout order, threshold ownership, fail-inactive reset defaults, fresh-intent recovery and sizing/verification method | `brownout-restart-contract.md` v1.0, `RP02-P2-REG-03`; numeric values remain open by design |
| `EDB-01…08` electrical-design-basis principles and first source/load contracts (numeric population still open) | `electrical-design-basis.md` |
| `CA-01…16` ownership, C3 N8 prototype class, Pi Active Cooler, differential production topology (suffixes, carriers, timeouts and evidence still open) | `RP02-P3-REG-01/02`; `compute-control-architecture.md` |
| C0↔C2 ICD **definition** — messages, framing method, expiry, heartbeat, two-phase arm, fresh-intent recovery (byte layout, numeric timing unregistered). C3 `BASE_*` **semantics** registered `RP02-P4-REG-02`. Coordination fields registered `RP02-P4-REG-03`; packed layouts still open | `RP02-P4-REG-01` / `RP02-P4-REG-02` / `RP02-P4-REG-03`; `link-contract.md` v0.6 |
| RP-03 Parts 1–5 design-definition (`BM-*`, physics range, Concept A working lead, pin map v0.1, gate *candidates*) | `RP03-P1-REG-01` … `RP03-P5-REG-01` |
| RP-03 brief-gap paper close (operating cases, BD-04 named surfaces, remaining physics, Set A/B, TTL candidates, cutoff metric, `CA-14` header) | `RP03-P1-REG-02` … `RP03-P4-REG-02`; `RP02-P4-REG-02` |
| RP-03 BD-08 V1 front support = `D21` ball; `D20` caster required swap; Concept A chassis retained | `decision.md` BD-08; `dimensional-baseline.md` v1.12; SCOPE-09 v1.3; not ADR-04 gate close |
| RP-04 Phase A design-definition (`P-01` sheets, HYBRID virtual select, gate candidates). Architecture-family research closed. Empirical spec paper-passed. Virtual wait language and P-02 cue list closed 2026-09-21. IR wire semantics accepted `RP02-P4-REG-03`. Exploratory layout revision 2 is a host reference, not G04. `BD-05` household observer panel superseded | `RP04-P1-REG-01`…`RP04-P6-REG-01`; `research/`; `decision.md`; `RP02-P4-REG-03`; `prototype/` |

---

## Maintenance

1. When a prototype document says something “remains open” or “intentionally open,” add or update a row here in the same edit if the item is still true at prototype-folder scope.
2. When the owning file closes the item, update this index in the same change.
3. Do not copy numeric budgets into this file. Point at `power-energy-ledger.md`, `payload-mass-capture.md` or the calculation ledger.
4. RP-03…RP-07 folders, when they exist, get their own sections rather than a second index.
