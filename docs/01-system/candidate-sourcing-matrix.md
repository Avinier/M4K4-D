# Makad V1 Candidate Sourcing Matrix

| Field | Value |
|---|---|
| Status | **Living. Face display and head camera selected; remaining rows are candidates unless explicitly marked otherwise.** |
| Version | 0.16 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-09-02 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 1) |
| Feeds | First project cost range (CON-TBD-13), RP-01…RP-07 inputs, later BOM |

The current dimensional baseline selects the two-powered-wheel/front-caster/rear-skid topology and major packaging targets. The project builder has additionally selected the **Waveshare ESP32-S3-LCD-4.3, no-touch, SKU 30493** as the V1 face display, the **Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, order code SC0874** as the V1 head camera, and **C2: a separate ESP32-S3 motion-controller module** for RP-01. C1 is closed and rejected on the selected display carrier's GPIO budget. The exact C2 module, motor, actuator, battery, framework, production camera interconnect and supplier remain open. Every other purchasable row remains a candidate chosen to bound specification, availability and landed cost. Prices/stock are Mumbai planning estimates and **must be re-checked immediately before purchase** (same rule as `workbench.md`). Bench tooling is not repeated here — it lives in `workbench.md`.

Columns follow the plan's required fields (line 102): spec, supplier, availability, lead time, substitute, quantity, landed cost, replacement risk, required tools, fabrication dependency.

## Compute & control

The RP-01 head-controller split is selected: the display carrier renders the face and a separate ESP32-S3 executes head trajectories and owns motion safety. Exact modules, the wider SBC/base topology, bus implementation and timebase remain subject to RP-02 → ADR-06/ADR-12. Rows below are candidates unless explicitly marked selected.

| Component | Candidate spec | Supplier (candidate) | Avail. | Lead | Substitute | Qty | Landed ₹ (est.) | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Main compute (SBC) | SBC-class board, USB/CSI camera, GPIO, enough for perception loop | Robu.in / local | Common | 0–3 d | Alt SBC / SBC+MCU split | 1 | 4,000–9,000 | Med (chip cycles) | — | Case/mount printed |
| **Head motion controller — C2 SELECTED** | **One dedicated ESP32-S3 module.** C1/shared-display control is rejected on SKU 30493's GPIO budget. The exact module remains unselected and **buy nothing now**. | TBD | No purchase | — | ESP32-S3 module with verified native GPIO budget | 1 | TBD | Med until module/pinout/fault tests close | Logic analyzer/current logger | Own installed module, mount, connectors and harness in M008; see `control-topology-options.md` §6.1 |
| Runtime head IMU | **Not installed for stationary RP-01.** Servo encoders provide joint angle; an IMU is bench-only for backlash/resonance when useful. | — | No purchase | — | — | 0 | 0 | None | Nano/bench instrumentation | Excluded from moving-head mass ledger |
| Real-time controller (MCU) — base/drive | Servo/motor timing + limits + watchdog; prefer same family as head MCU | Elegoo kit / Robu | On hand | 0 | On-SBC RT thread | 1 | 0–800 | Low | — | — |
| Base-frame IMU | 6-axis gyro/accelerometer for later chassis heading/attitude, caster/traction disturbance and tip/pickup detection; head mounting is excluded because subtracting neck motion reintroduces the SPEC-09 timing-skew problem | On-hand board if suitable / Robu | Deferred | — | Same family as selected base controller where practical | 0–1 | TBD | Low | — | Rigid base/controller mount; feeds RP-03, not moving-head ballast |
| Internal link | UART/USB serial (Vector-style) for SBC↔MCU; CAN only if a 3rd distributed node earns it | on-board | On hand | 0 | I²C local-only / CAN later | 1 | 0–500 | Low | Soldering | Harness |
| Motor/servo driver | Drives base motors + head servos, current sense preferred | Robu / Zbotic | Common | 0–3 d | Separate ESC + servo rail | 1–2 | 500–2,000 | Low | Soldering | Wiring harness |

## Head (RP-01 / RP-06)

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| **Face display — SELECTED** | **Waveshare ESP32-S3-LCD-4.3 no-touch, SKU 30493**; 800×480 IPS, integrated ESP32-S3/LVGL renderer, ~106.1×67.8 mm. Exact module is locked; alternatives require recorded hard-failure change control. See `display-candidate-study.md` and `display-shopping-brief.md`. | Supplier not locked; Hubtronics India is the verified lead | ₹3,065 incl. GST and two units shown in stock on 2026-08-29; reconfirm before payment | Domestic shipping estimate to be confirmed | Contingency references only: Waveshare 43H-800480-IPS no-touch DSI SKU 24159; DWIN DMG80480T043_09WN | 1 sample; second only after acceptance | **3,065 verified lead; planning allowance 3,000–4,600** | Med until actual mass, repeat stock, optical result and sustained animation test close | Current logger, scale, temperature/frame-time logging, smoked-window samples | ~106 × 68 mm hidden body behind a ~94–95 × 53–54 mm optical aperture and ~110–115 × 60–65 mm bezel/window treatment; listed 118 g is not accepted as installed mass until sample is weighed |
| Smoked face window | Acrylic/PC with ~94–95 W × 53–54 H mm optical aperture inside a ~110–115 W × 60–65 H mm bezel/window treatment, hiding display edges | Local acrylic | Common | 0–2 d | Tint film over clear panel | 1 | 200–800 | Low | Cutting | Laser/print fit |
| **Camera — SELECTED** | **Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, order code SC0874**; IMX708, 11.9 MP, 120° diagonal / 102° horizontal / 67° vertical, autofocus, HDR, 25 × 24 × 12.4 mm, MIPI CSI-2. Exact module is locked; see `camera-candidate-study.md`. | Supplier not locked; ElectroPi and Silverline are current leads | ElectroPi listed 62 units and Silverline listed in stock on 2026-08-29; reconfirm | Domestic dispatch estimate to be confirmed | Contingency only: Arducam B031202 after recorded change control | 1 sample; second only after acceptance | **3,088–3,210 verified listings; planning allowance 3,000–4,500** | Med until actual mass, SBC compatibility, image/latency and moving-interconnect tests close | Camera calibration target, live frame/error/latency logger, axis-conditioned cable endurance fixture, scale | Central lens/LED/display clearance; complete module, mount, connector and three-axis moving-link mass/CoM. Supplied 200 mm FPC is bench-usable only until the H1/H2/H3 evidence in `head-harness-routing-study.md` selects a production interconnect |
| Status light | Addressable LED beside camera (SCOPE-17) | Elegoo / Robu | On hand | 0 | Single-colour LED + driver | 1+ | 100–500 | Low | Soldering | Optic/diffuser |
| Head actuators (roll/pitch/yaw) | Smart servos/geared motors + feedback sized from the **~490 g pre-M008 lower bound plus C2 hardware** and the eventual per-axis mass/inertia tree; Concept A uses body-fixed yaw and moving pitch/roll, with candidate selection gated by transient torque-speed plus busy-minute RMS/current/thermal evidence | Robu / Zbotic / MG Super Labs | Mixed; re-check exact SKU | 0–10 d | Feetech STS class ↔ DYNAMIXEL XL/XC class | 3+ plus one bench sample where needed | 3,000–34,000 | Med–High (exact SKU/cost) | Current/voltage logging, output indicator | 60 mm neck allocation, near-CoM gimbal centre, direct actuation first |
| Head joint structure | Compact yaw load-bearing shaft/bearing, rising pitch yoke with double ear pivots, and an unresolved display-clear roll support; compare rear spaced-bearing cartridge, annular/perimeter support and displaced roll axis. Ear shells are removable covers, not the structural load path | Local bearing supplier / fabricated parts | Common classes, exact sizes TBD | 0–7 d | Small radial/angular-contact pair ↔ suitable compact supported shaft/ring | set | 500–3,000 | Med until roll load path closes | Printer/machining/measurement | Concept A section blockout; must prove display clearance, overhung moment/deflection, mass and 60 mm fit before CAD freeze |
| Body microphone array | 4 synchronized PDM MEMS microphones, non-collinear/wide rigid body geometry | Robu | Common | 0–3 d | Alternate synchronized digital MEMS array | 4 | 800–2,400 | Med | Soldering | Body PCB/subframe + acoustic ports; none in ears/head |

## Drive & base (RP-03)

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Drive motors | Independently controlled geared motors with encoders; design around 160–200 wheel RPM unloaded for ~0.70 m/s capability; follow trials remain ≤0.5 m/s | Robu / Zbotic | Common | 0–5 d | Alternate encoder gearmotor | 2 | 600–3,000 | Med | — | 170 mm track, wheel + bracket |
| Wheels + front caster + rear skid | Ø84 × ~21 mm moderate-grip rubber/TPU drive wheels (Ø80–85 acceptable), ~Ø30 mm front caster, mandatory anti-tip skid | Robu / local | Common | 0–3 d | In-range wheel/caster alternatives | 2+1+1 | 300–1,200 | Low | — | 110 mm axle-to-caster target; skid ~70 mm behind axle and ≤14 mm above floor |
| Motion safety / limits | E-stop already in `workbench.md` bench scope | — | — | — | — | 1 | (see workbench) | Low | — | Motor-rail wiring |

## Audio & power

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Speaker + amp | Body-mounted character voice with useful enclosure cavity | Robu / Lamington Rd | Common | 0–5 d | Different driver size | 1 | 300–1,500 | Low | Soldering | Body enclosure/baffle |
| Battery / cells | Chemistry undecided — ADR-06 (18650 holder vs LiPo pouch); package low and forward of drive axle | Robu / local | Common | 0–5 d | 18650 ↔ LiPo | 1 pack | 500–2,500 | Med (safety) | LiPo bag/charger | Pack + holder must help reach `x_CoM=+25 mm`, `h_CoM=124 mm` |
| Power distribution / regulation | Feeds concurrent peak loads (AD-08), brownout-safe | Robu | Common | 0–3 d | Buck modules ↔ integrated PDB | 1 | 400–1,500 | Low | Soldering | Harness |

## Structure & fasteners

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Printed polymer stock | PLA/PETG for shells & brackets (material choice deferred) | Local filament | Common | 0–2 d | PLA ↔ PETG ↔ ABS/ASA | as needed | 800–2,500 | Low | 3D printer | Print time |
| Heat-set inserts + screws | M3 inserts for repeated service assembly | Robu / local | Common | 0–3 d | Self-tapping (worse for service) | set | 300–1,000 | Low | Soldering iron tip | Boss design |
| Other bearings / pivots | Base and non-head joints as needed; Concept A head bearings are counted in the dedicated head-joint row above | Robu / local | Common | 0–5 d | Bushings ↔ ball bearings | few | 200–1,000 | Low | — | Joint design |

## First project cost range (CON-TBD-13)

Rolled up from the candidate ranges above (**components only — excludes the `workbench.md` bench tooling of ₹10k–25k**):

| Bound | Estimate |
|---|---:|
| Low (frugal/Feetech-class path, on-hand reuse, selected IPS sample included) | **≈ ₹16,000–20,000** |
| High (premium three-DYNAMIXEL head path, selected IPS display included) | **≈ ₹75,000–80,000** |

This is a **planning envelope to gate procurement decisions**, not a budget commitment. The selected display can now be included from the verified ₹3,065 India lead, with allowance for freight and price movement. Stock and freight still require reconfirmation immediately before purchase.

## Open items

- [ ] Verify local stock/price for the "Now" candidates by walking Lamington Road once (per workbench sourcing note).
- [ ] Confirm Hubtronics physically holds the selected no-touch SKU 30493, obtain one sample and run the geometry/mass/animation/power/window validation before freezing the head CAD.
- [ ] Add and source a credible Concept B before RP-01 fabrication; Concept A alone does not satisfy the ≥2-concept rule.
- [ ] Resolve battery chemistry candidate (ADR-06) before any pack purchase.
- [ ] Attach a verified source + one acceptable substitute to each architecture-critical row (RP06-G05 gate).
- [ ] Promote selected rows into a later `hardware/bom/` roll-up once ADRs close.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First-pass candidate matrix + first project cost range created; no selections made. |
| 2026-08-27 | 0.4 | Added separate body-IMU path and expanded the head mechanism/actuator rows for the elevated ear-pivot serial-gimbal candidate; no component selected. |
| 2026-08-28 | 0.5 | Split the head node into C1 Nano and C2 display-MCU candidates, added the external head-IMU path, and made the roll-support/display conflict an explicit sourcing and blockout dependency. |
| 2026-08-29 | 0.6 | Replaced the generic display row with exact AMOLED leads, recorded the discontinued AUO lineage and lack of India-stock modules, added the one-off controller cost allowance, and linked the focused display study. |
| 2026-08-29 | 0.7 | Demoted all exact AMOLED names to unverified overseas RFQ references, marked the display path procurement-blocked, withdrew unsupported price/lead-time estimates, and excluded the display from the project cost range. |
| 2026-08-29 | 0.8 | Added the directly orderable 4.39-inch 600-nit DMKDO04301ACA/SD5207 family as the primary sample direction, retained controller integration as the blocker, and linked a reusable shopping brief with ecommerce and Mumbai leads. |
| 2026-08-29 | 0.9 | Dropped the AMOLED requirement by project decision, adopted the India-stock IPS direction, made the no-touch Waveshare ESP32-S3-LCD-4.3 the first prototype candidate, and restored a display-inclusive planning range. |
| 2026-08-29 | 0.10 | Project builder selected and locked Waveshare no-touch SKU 30493 as the V1 face display; retained supplier choice and measured integration evidence as open items. |
| 2026-08-29 | 0.11 | Added the exact head-camera shortlist and preferred Camera Module 3 Wide first-sample direction; kept camera and interface unselected pending body-SBC compatibility and CSI-versus-USB moving-harness evidence. |
| 2026-08-29 | 0.12 | Project builder selected and locked the visible-light Raspberry Pi Camera Module 3 Wide, order code SC0874; retained supplier, body SBC and production moving interconnect as separate decisions and converted the seven camera conditions into acceptance/change-control evidence. |
| 2026-08-29 | 0.13 | Added the source-grounded H1/H2/H3 moving-link study and axis-conditioned live-signal endurance direction; no production harness selected. |
| 2026-08-30 | 0.14 | Propagated the display-derived optical aperture and bezel/window geometry from dimensional baseline v1.7; no component selection changed. |
| 2026-08-31 | 0.15 | Selected ESP32-S3 as the RP-01 motion-firmware class, made a dedicated module conditional on C1, recorded C1's carrier-GPIO block, moved Nano 33 BLE Sense and IMU use to bench equipment, and deferred all new controller/IMU purchases. |
| 2026-09-02 | 0.16 | Closed the C1/C2 fork: rejected C1 on selected-carrier GPIO evidence, selected one dedicated ESP32-S3 C2 motion controller, retained the exact module and purchase as open, and replaced the stale 250 g actuator-sizing input with the ~490 g pre-M008 lower bound plus C2. |
