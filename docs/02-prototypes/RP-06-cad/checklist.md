# RP-06 closure checklist

| Field | Value |
|---|---|
| Status | **Living.** CAD/paper ~75–85% of the packaging question; physical validation 0% |
| Owner | Project builder |
| Created | 2026-09-21 |
| Governing plan | [`risk-prototype-plan.md`](../../01-system/risk-prototype-plan.md) v1.15 §RP-06 |
| Working CAD | [Layout 03](head/layout-03/README.md); [body/chassis Layout 02](body-chassis/layout-02/README.md) |

This is the compact remaining-work list. Canonical numbers stay in the cited files. Checking a row here does not freeze a SKU, promote `E` to `W`, or register a gate.

Evidence classes are unchanged: `W` measured on the named hardware, `D` manufacturer source, `E` estimate/substitute, `U` unknown/unselected and never zero. CAD overlays are `D/E` working evidence, not `W`.

## How to use this file

1. Phase A (now): replace envelopes with sourced geometry; keep every checkbox honest.
2. Physical mock-up: run the plan's mock-up procedure against the current **~499–524 g / nominal 509 g** head baseline, not 250 g.
3. Register `RP06-G01`…`G06` numeric thresholds **before** inspecting scored data.
4. Keep binding envelopes in this CAD tree, the dimensional baseline, and the mass ledger.

---

## 0. Locked inputs (do not re-shop)

| Input | Current value | Status |
|---|---|---|
| Head mass | **~499–524 g complete D/E; nominal 509 g at M008=20 g** | Use. Former ~250 g target is historical only |
| Head inertia | Layout 03 D/E ~0.000656 / 0.000728 / 0.001080 kg·m² roll / pitch / yaw at M008=20 g | Screening input; replace servo references per candidate |
| Head envelope | 104 × 150 × 115 mm complete; 86 × 130 × 115 mm core | Planning geometry |
| Robot envelope | 300 × 205 × 180 mm rounded target; **304 mm** current neutral stack | Accept 304 mm or recover 4 mm under G01 |
| Placement | 140 mm body-top datum; 60 mm neck; body mics/speaker/battery/C0 | Locked |
| Whole-robot CoM target | `x = +25 mm`, `h = 124 mm` | Placement target. Layout 02 currently +20.6 / 105.8 mm: +20.2 / 103.7 after the 16 mm body shift (`RP03-CAD-06`), +18.8 / 107.9 with the lighter 2S1P pack (`RP03-CAD-07`), restored by an 81.6 g ballast bar (`RP03-CAD-08`) |
| Display | SKU **30493** | Locked; optical/animation tests remain |
| Camera | **SC0874** | Locked; FOV/interconnect/contamination tests remain |
| C0 / cooler / C2 / C3 proto | Pi 5 2 GB; official Active Cooler; ESP32-S3-Zero; DevKitC-1-N8 | Locked at stated layer |
| Drive | Two-wheel differential; Ø1″ ball; rear skid | Topology locked; SKUs open |

M008 remains physically `U`. The nominal tree still carries two 23 g XC330-size housings; substitute any non-C01 servo before treating 509 g as the installed dummy.

---

## 1. Integrated packaging — G01, G04

CAD already: live head import; selected two-wheel / ball / skid; chassis and shell; a drivetrain that can turn (`RP03-CAD-05`); service panels; Pi 5, battery tub, power, drivers, C3, IMU envelopes; wiring trunks; mass/CoM overlays; deterministic checks.

| # | Item | CAD/paper | Physical | Remaining |
|---|---|---|---|---|
| P-01 | Fit **actual** sourced articles, not only envelopes (display, camera, Pi 5, cooler, C2, C3, battery, drivers, speaker, mics, fasteners) | Partial — vendor STEP where downloaded; else envelopes | Open | Replace each envelope as the sample arrives; record SKU vs solid |
| P-02 | 300 × 205 × 180 mm box vs sourced layout | Layout 02 body 174 mm lower width, 110 mm visible height, 30 mm clearance | Open | Pass in-box or revise the baseline explicitly |
| P-03 | **304 mm stack: accept or recover 4 mm** through body/neck datums | Documented 304 mm; 300 mm still a rounded target | Open | Named decision in the baseline, not a quiet trim |
| P-04 | Whole-robot CoM vs +25 / 124 mm | Layout 02 generated **X = +18.77 mm, Z = 105.05 mm, 2568 g modeled** with the RP-02 power boards (a_tip 1.75 m/s², x/h 0.179 vs 0.202); the builder accepted this as the working baseline on 2026-09-25 (`RP03-CAD-09`) and the `physics.md` §2.5 check is re-based to a_tip ≥ 1.582 m/s² | Open (baseline revised) | Replace the register with a weighed robot (`W`); re-check the head-pose corners at the real head mass. Do not shrink `a_tip` to hide a miss |
| P-05 | Battery low and **forward** of the axle | CAD 2S1P 18650 pack (`RP03-CAD-07`) in a chassis tub at X = +46.7, Z = 43.9 mm, bottom hatch | Open | Measured pack (BMS thickness, mass), lead and connector; hatch fastening, retention and tub-to-body harness; HIGH_AFT remains forbidden |
| P-06 | Harness trunks, service loops, body-side yaw anchor | Reservations exist; production construction `U` | Open | Close with the harness study; body-side yaw clamp is RP-06 |
| P-07 | Fastener / insert SKUs across head, body, chassis | Visible M2 locked on the head; internals `U` | Open | Trial coupon + landed row; populate the fastener mass row |
| P-08 | Installed head mass / CoM / inertia vs RP-01 envelope | Nominal 509 g D/E tree | Open | M900 `W`; dummy must sit in 499–524 g until then |

- [ ] P-01 sourced-part fit, not envelope-only
- [ ] P-02 bounding box held or baseline revised
- [ ] P-03 304 mm accepted or 4 mm recovered
- [ ] P-04 CoM hit or baseline revised
- [ ] P-05 forward-low battery on the installed pack
- [ ] P-06 body-side yaw anchor and trunks
- [ ] P-07 fastener SKUs and mass row
- [ ] P-08 M900 / dummy inside the current head tree

---

## 2. Head integration — G01, G04, G06

CAD already: display envelope; camera envelope and flared aperture; C2 pocket/tray; yaw/pitch/roll; camera crown; window; connector/harness reservations; preliminary mass/inertia tree; paper service sequence.

| # | Item | CAD/paper | Physical | Remaining |
|---|---|---|---|---|
| H-01 | Display SKU 30493 in the carrier, non-contact mount, connector clearance | Envelope + Layout 03 aperture 99 × 58 mm, window 110 × 64 mm | Open | Weigh installed module; confirm hidden 106.1 × 67.8 mm clearance on the article |
| H-02 | Smoked window + black mask + air gap | Window/mask solids exist | Open | Start at **60–70% visible-transmission** neutral smoke ([display study](../../01-system/display-candidate-study.md)) |
| H-03 | Camera SC0874, aperture, crown, moving interconnect | Flared aperture clears a conservative FOV envelope; 200 mm FPC is bench-only | Open | Entrance-pupil measurement; H1/H2/H3 production route |
| H-04 | Status light + optics beside camera | LED branch is a keep-out pending the on-hand package | Open | Select optic; prove no destructive crown clash |
| H-05 | C2 Zero in the rolling-cradle tray; USB/BOOT service | Pocket and lift path authored | Open | Installed M008 `W`; flashing with cover on (CAD-04 / CAD-04a) |
| H-06 | Servos, bearings, structure, cables, connectors | Trial Ø16.2 × 6.2 mm seats; two retainer-screw collisions still open | Open | Bearing SKU; collision repair is an RP-01 blocker that RP-06 must not paper over |
| H-07 | Final installed head mass and CoM | D/E tree 362/436/509 g roll/pitch/yaw at M008=20 g | Open | Per-axis `W` after print/kit; dummy = current tree, not 250 g |

- [ ] H-01 display installed and weighed
- [ ] H-02 smoked window stack chosen
- [ ] H-03 camera + production moving interconnect
- [ ] H-04 status-light package fits
- [ ] H-05 C2 installed mass and service
- [ ] H-06 bearings/servos/cables on purchased hardware
- [ ] H-07 installed head mass/CoM `W`

---

## 3. Display validation — G02, G03

Do not reopen SKU 30493 except under the display study's hard-failure rule. Suggested refresh gate from the 2026-09-14 review: **≥30 fps sustained, no tearing, UART receiver active** — register before scoring.

| # | Item | Remaining |
|---|---|---|
| D-01 | Face legibility at registered angles and distances | Mock-up through the actual window; household distances |
| D-02 | Household lighting (dim-room and daylight-room) | Display-study acceptance test steps 6+ |
| D-03 | Smoked-window transmission vs 300-nit-class panel | 60 / 70 / clear samples; mask must hide the dark panel rectangle |
| D-04 | Sustained animation, 30 minutes, representative eyes | Frame rate, spikes, board temperature |
| D-05 | No unacceptable tearing or stalls with UART receiver **active** | Idle vs active frame-time; do not discover the ceiling in scored G02 |

- [ ] D-01 legibility matrix
- [ ] D-02 lighting matrix
- [ ] D-03 window transmission chosen
- [ ] D-04 30-minute animation
- [ ] D-05 UART-active, no tearing/stalls

---

## 4. Camera validation — G02, G03, G04

Module locked. Host is Pi 5. Production moving interconnect is not selected. Use the [camera study](../../01-system/camera-candidate-study.md) acceptance list and the [harness endurance method](../../01-system/head-harness-routing-study.md).

| # | Item | Remaining |
|---|---|---|
| C-01 | FOV and occlusion over head motion | Conservative CAD envelope is not optical certification |
| C-02 | Detection/tracking geometry at 0.6, 0.9, 1, 2, 3 m | RP-07 consumes this; RP-06 supplies installed geometry |
| C-03 | Calibration stability through roll/pitch/yaw | Repeat after motion and after service |
| C-04 | Focus / exposure / PDAF lock during gestures | Lock lens position in software during head moves |
| C-05 | Display and status-light contamination | On/off matrix against the camera |
| C-06 | Cable motion and live-stream endurance | H1/H2/H3; live CSI/errors, not continuity-only; supplied 200 mm FPC is bench-only |

- [ ] C-01 FOV/occlusion through workspace
- [ ] C-02 test-distance geometry
- [ ] C-03 calibration stability
- [ ] C-04 focus/exposure behaviour
- [ ] C-05 optical contamination
- [ ] C-06 live-stream endurance on the installed route

---

## 5. Audio integration — G03

Placement locked; SKUs wait on RP-05 `BD-A05` / `BD-A06` then an RP-06 port freeze. `AR-*` requirements live in [`RP-05-interaction/audio-requirements.md`](../RP-05-interaction/audio-requirements.md). Layout 02 allocates a 50 mm basket / 44 mm cone, amplifier envelope, 34 mm cavity, and four PDM ports at FRONT_L/R and REAR_L/R. Pi 5 has no native 4-channel PDM; the front end remains an `AP-*` family choice, not a SKU.

| # | Item | Remaining |
|---|---|---|
| A-01 | Speaker output and enclosure vibration | Installed driver + cavity; no rattling panels or mobility fascia |
| A-02 | Microphone geometry and capture | Four-port baseline vs selected boards; array rigidity |
| A-03 | Self-noise: speaker, cooler, drive, head | Inhibit/isolation; beamforming does not cancel coherent structure noise |
| A-04 | Acoustic compatibility with the body structure | Grille, cavity, and shell as one enclosure; ports away from cooler exhaust |

- [ ] A-01 speaker / vibration
- [ ] A-02 mic geometry on selected boards
- [ ] A-03 self-noise matrix
- [ ] A-04 body-structure acoustics

---

## 6. Thermal integration — G01, ledger T-3

| # | Item | Remaining |
|---|---|---|
| T-01 | Pi 5 Active Cooler airflow in the closed body | Intake/exhaust path, dust, service access |
| T-02 | Converter, driver, display, battery heat | Spacing vs Layout 02 electronics packing; T-3 trip-wire |
| T-03 | Closed-body operating temperature | SC-TBD-12 once registered; sealed-head PLA dwell is RP-01 D-03 |
| T-04 | Acoustic effect of the cooler on the four body mics | Capture with cooler on/off against A-03 |

- [ ] T-01 cooler airflow
- [ ] T-02 heat-source spacing
- [ ] T-03 closed-body temperature
- [ ] T-04 cooler vs microphones

---

## 7. Serviceability — G06

Paper sequences exist (Layout 03 head; Layout 02 panels, fascia, Pi access). G06 requires a **timed, non-destructive** demonstration on the article.

Named high-risk modules: display, camera, C2 tray, production camera interconnect, Pi 5 + cooler, battery pack, speaker/amp, a head servo, a body microphone board.

| # | Item | Remaining |
|---|---|---|
| S-01 | Assembly order from documentation | Written, then performed once on the mock-up |
| S-02 | Connector access at extrema and at rest | Yaw demate (CAD-05); C2 USB/BOOT; CSI ZIF; pack disconnect |
| S-03 | Replacement of each named high-risk module | No destructive disassembly; no removal of unrelated structure |
| S-04 | Tools and service time | Record tool list and minutes; compare to a registered G06 bar |
| S-05 | Head sequence still valid after body integration | Layout 03 rear-cover / front-carrier / ear-cap / servo-strap order |

- [ ] S-01 assembly order
- [ ] S-02 connector access
- [ ] S-03 high-risk replacements
- [ ] S-04 tools and time
- [ ] S-05 no destructive disassembly

---

## 8. Sourcing closure — G05

Canonical rows: [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md). RP-06 does not duplicate them. Every architecture-critical part needs a verified source, complete landed cost, and one acceptable substitute **or** an explicitly accepted single-source risk. Recheck price/stock before payment.

| Class | Locked / lead | Still open for G05 |
|---|---|---|
| Display, camera, C2, Pi 5, Active Cooler, C3 proto | Selected at stated layer | Sample receipt, repeat stock, landed cost on the paid invoice |
| Smoked window, status light, speaker, mics, mic front end | Candidates / unselected | Exact SKU, availability, lead, substitute |
| Servos, bearings, battery, drivers, production CSI, inserts | Unselected or paper-only | Do not treat C01 / D02 / DRV-B as a freeze |
| Structure / print stock | PLA for RP-01; body material open | Fabrication process and tools per row |

For each architecture-critical row:

- [ ] Exact source and part identity confirmed on the article / invoice
- [ ] Availability and lead time rechecked
- [ ] Landed cost (unit + shipping + GST + tools + spares)
- [ ] Substitute named, or single-source risk accepted in writing
- [ ] Required fabrication process and tools recorded

CON-TBD-13 (first complete project cost range) is fed by this audit; RP-06 does not invent a ceiling.

---

## Gate map

| Gate | Checklist IDs | Pass sense |
|---|---|---|
| **RP06-G01** Physical viability | P-*, H-*, T-01/T-02, S-01 | One layout fits Core head functions with assembly, motion, connector, cooling and service clearances plus explicit margin |
| **RP06-G02** Perception/display | D-01…D-05, C-01…C-04 | Face legibility and camera coverage pass the registered environment/geometry matrix through the head workspace |
| **RP06-G03** Optical/acoustic | D-03, C-05, A-*, T-04 | Status light and display do not unacceptably corrupt camera evidence; speaker/mechanism and mic capture meet the registered bars |
| **RP06-G04** Dynamic compatibility | P-04, P-08, H-07, C-06 | Measured/estimated mass and CoM stay inside the RP-01 envelope, or RP-01 is rerun with the revised load. Dummy uses **499–524 g / 509 g**, never 250 g |
| **RP06-G05** Sourcing | §8 | Architecture-critical parts: verified source, landed cost, substitute or accepted single-source risk |
| **RP06-G06** Serviceability | S-* | Named high-risk replacements without destructive disassembly or unrelated structural removal |

Numeric thresholds, lighting/distance matrix, cycle-life, service-time bar and acoustic bars are **not** registered by this checklist.

---

## Export (only after gates)

| Destination | What RP-06 may write |
|---|---|
| `dimensional-baseline.md` | Explicit revision if 304 mm, box, or +25/124 cannot be met |
| `mass-envelope-ledger.md` | Body, fastener, and measured-head rows |
| `candidate-sourcing-matrix.md` | Rechecked G05 fields |
| Next head-CAD iteration | Installed articles, window, interconnect, service proven on the mock-up |
| ADR-01 / ADR-08 / ADR-11 | Provisional layout and sourcing strategy around the locked display |

Do not export a second mass target. Do not reopen display or camera selection except under their recorded hard-failure rules.
