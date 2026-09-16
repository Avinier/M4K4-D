# Prototype open items

| Field | Value |
|---|---|
| Status | **Living index.** Not a competing decision, budget, CAD or gate record |
| Created | 2026-09-16 |
| Scope | Remaining work inside `docs/02-prototypes/` after RP-01 Layout 03 paper demand and RP-02 Part-1 / Part-2 registrations |
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

## Shared blockers (both prototypes)

These sit above RP-01 and RP-02. Scored physical runs wait here even when paper work is live.

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Stage 0 workbench / powered-test gate | Tools are specified; the scored-test checklist is not satisfied | Arrival, acceptance tests, fixture E-stop/isolation, logging | `../../01-system/workbench.md`; RP-01 `rig.md`; RP-02 `RP-02-electrical/rig.md` | Any scored RP01/RP02 run |
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

**Current outcome:** Part 1 registered (`RP02-P1-REG-01`); all seven Part-2 power-architecture subparts complete at design-definition level; topology registered (`RP02-P2-REG-01`); implementation basis and Raspberry Pi 5 2 GB selected (`RP02-P2-REG-02`); `BR-*` brownout/reset/restart policy registered (`RP02-P2-REG-03`). No gate passed, no ADR closed, no purchase authorized.

### Intentionally open until physical inputs exist

This is the class that prompted this index. Architecture and calculation method are in place; **ratings are not**.

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| **Final wire, fuse, converter and pack ratings** | Equations, sensitivity tables and `PCD-*` candidate screen exist; installed path, protection curves, converter maps and pack impedance do not | Candidate-screen evidence list, then one conditional term at a time | `RP-02-electrical/power-calculation-ledger.md` §8; `power-component-candidate-screen.md` §12 | G01; ADR-06 architecture evidence |
| Battery chemistry, S-count, pack construction | PA-03/04 and `PB-MAIN` admit the servo/drive outcome; 2S 6.0–8.4 V is an `E` planning case only | RP-01 family + RP-03 drive envelope + handling | `electrical-design-basis.md` §8; `decision.md` | Charge path; G03; ADR-06 sizing |
| Charger, adapter, keyed charge connector | STUSB4500QTR + BQ25798 is the screened architecture lead, not selected; adapter/settings/body inlet open; AC stays outside Makad | Chemistry, charge power, PDO and body layout | `power-component-candidate-screen.md` §9; `power-branch-contracts.md` `PB-CHARGE-*` | `CC-15`; G06 |
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
| Raspberry Pi 5 2 GB (`LG-01`) | Selected 2026-09-16 under `RP02-P2-REG-02`; 5.1 V nominal / 5 A-capable `PB-COMPUTE` | Purchase, power-entry/PD hardware, active cooler validation, storage, workload `W` | `decision.md`; `power-implementation-basis.md` |
| C2 Waveshare ESP32-S3-Zero | Module and CTRL-01…06 locked | Installed power `W`, transceiver, pin map vs DevKitC-1, G05 loop/link | RP-01 decision; `load-model.md` |
| Display SKU 30493 | Selected; 5 V / 450 mA published `D` | Sample `W`, inrush, brightness, status light, charge-mode profile | ledger `LG-05`; `PB-DISPLAY` |
| Camera Module 3 Wide | Selected on CSI | Official/sample power, 22-to-15 CSI cable in the moving route, PDAF lock during gestures | camera study; `PB-CAMERA` |

### Still unselected hardware

| Item | Notes | Home |
|---|---|---|
| Status light | Display row selected; light is not | `LG-05` |
| Microphone front end (`LG-07`) | Pi 5 has no native 4-ch PDM; codec HAT vs USB array suggested only | `decision.md` candidate register |
| Speaker + amplifier (`LG-08`) | RP-05/06 | `PB-AUDIO-OUT` |
| Base/drive MCU and sensors (`LG-10`) | Prefer C2 family; RP-03 | `PB-SAFE-BASE` |
| Link transport vs C2-as-face-relay | UART 921 600 primary; USB-CDC fallback; in-head relay not adopted | `link-contract.md` v0.2 |

### RP-02 process remaining

| Item | Why it is open | Waiting on | Home | Blocks |
|---|---|---|---|---|
| Numeric G01–G06 registration | Candidate metrics only | Dated builder freeze before inspecting scored data | `RP-02-electrical/gates.md` | Any pass row in `decision.md` |
| Fault injection campaign | F-01…F-22 defined; none injected | Rig + G04 freeze | `fault-matrix.md` | ADR-03 / ADR-12 evidence |
| Distribution rig | Designed against registered architecture; not built | Instruments + Phase A/B hardware | `rig.md` | G01/G02/G04 |
| `link-contract.md` v1.0 | v0.2 draft; field sizes/rates candidate | Implement both ends + G05 | `link-contract.md` | ADR-12 |
| ADR-03 | Open | G05 on Zero (or twin with pin-map note) **and** G04 on real servos | `decision.md` ladder | Controller backbone |
| ADR-12 | Open | Contract + G05 + `timebase.md` §6 | same | Internal comms |
| ADR-06 architecture | Topology/basis fixed; implementation pending | G01, chemistry, remaining power parts, RP-06 layout | same | Rails/isolation/policy |
| ADR-06 sizing | Expected after RP-03, not in stage 2 | Ledger `W` for every `LG`; G03 margin | same | Pack capacity |
| Phase A remaining | Paper/on-hand; loopback and DevKitC-1 timing do not wait on buys | Timebase + link on twin; G01/G06 paper review | `intent.md` phase ladder | Unblocks RP-01 scored path |
| Phase B | Needs a named RP-01 servo load (C01 as reference is allowed; purchase ≠ family freeze) and the selected Pi 5 | Those parts on the bench | `intent.md` | G05 servo bus; head+compute G02 |
| Phase C | Battery gate | Pack + procedure | `intent.md` | G03 rehearsal |
| Drive-dependent cases | `CC-09/09C/09R`, `CC-10A/B/C`, `CC-11`, `CC-12C`, `CC-13D`, drive share of `CC-PEAK-01`/`ST-01` | RP-03 hardware | `gates.md` G02 note | Whole-robot peak claim |
| SC-14 20-minute Core | Not an RP-02 closure | Integrated droid | plan; G03 | CON-10 |

---

## Circular dependencies (named, not stalled)

| Loop | What can proceed now | What must wait |
|---|---|---|
| RP-01 mass ↔ RP-02 rail | Layout 03 **paper demand** is complete without M008 `W`. RP-02 Phase A runs on paper and on-hand boards. | Complete-head `W` waits on M008. PA-04 **collapses only on family freeze**, not on a C01 purchase. |
| RP-01 P02 sag floor ↔ RP-02 servo rail | RP-02 records C01 5 V as a leading working assumption. | Loaded servo-terminal floor is a measured rail result. |
| RP-01 first scored run ↔ RP-02 timebase/G05 | Exploratory timing on DevKitC-1. | Scored RP-01 timestamps need implemented `timebase.md`. |
| G02 invariant ↔ later prototypes | Non-drive rehearsal can start when head+compute exist. | Drive, speaker and later loads force a re-run; they do not delay Phase A. |

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

---

## Maintenance

1. When a prototype document says something “remains open” or “intentionally open,” add or update a row here in the same edit if the item is still true at prototype-folder scope.
2. When the owning file closes the item, update this index in the same change.
3. Do not copy numeric budgets into this file. Point at `power-energy-ledger.md`, `payload-mass-capture.md` or the calculation ledger.
4. RP-03…RP-07 folders, when they exist, get their own sections rather than a second index.
