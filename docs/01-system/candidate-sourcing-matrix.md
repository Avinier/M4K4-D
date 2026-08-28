# Makad V1 Candidate Sourcing Matrix

| Field | Value |
|---|---|
| Status | **Living — first pass.** Candidates only; **no component is selected.** |
| Version | 0.4 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-08-27 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 1) |
| Feeds | First project cost range (CON-TBD-13), RP-01…RP-07 inputs, later BOM |

The current dimensional baseline selects the two-powered-wheel/front-caster/rear-skid topology and major packaging targets, but it **does not select a processor, exact motor, camera module, actuator, battery, framework, or supplier**. Every purchasable row here is therefore a **candidate**, chosen to bound specification, availability, and landed cost so prototypes can start and a first cost range can exist. Selection happens only through the ADRs as prototype evidence closes (decision-closeout). Prices/stock are Mumbai planning estimates and **must be re-checked immediately before purchase** (same rule as `workbench.md`). Bench tooling is not repeated here — it lives in `workbench.md`.

Columns follow the plan's required fields (line 102): spec, supplier, availability, lead time, substitute, quantity, landed cost, replacement risk, required tools, fabrication dependency.

## Compute & control

Topology (SBC + MCU split, compute placement, bus, timebase) is a provisional option study in `control-topology-options.md`, resolved by RP-02 → ADR-06/ADR-12. Rows below are candidates for that topology, not selections.

| Component | Candidate spec | Supplier (candidate) | Avail. | Lead | Substitute | Qty | Landed ₹ (est.) | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Main compute (SBC) | SBC-class board, USB/CSI camera, GPIO, enough for perception loop | Robu.in / local | Common | 0–3 d | Alt SBC / SBC+MCU split | 1 | 4,000–9,000 | Med (chip cycles) | — | Case/mount printed |
| Head-aggregation MCU | **Arduino Nano 33 BLE Sense** (nRF52840 M4F) — 3-axis servo loop + limits/watchdog, onboard IMU for head-pose feedback, drives LED; onboard mic is not part of the body-array architecture; 18×45 mm, 3.3 V | On hand | On hand | 0 | Same-family MCU for head/base parity | 1 | 0 (owned) | Low | — | Head board/mount; see `control-topology-options.md` §6 |
| Real-time controller (MCU) — base/drive | Servo/motor timing + limits + watchdog; prefer same family as head MCU | Elegoo kit / Robu | On hand | 0 | On-SBC RT thread | 1 | 0–800 | Low | — | — |
| Body-frame IMU | 6-axis gyro/accelerometer for chassis heading/attitude, caster/traction disturbance and tip/pickup detection; independent of the head IMU | On-hand board if suitable / Robu | TBD | 0–5 d | Same sensor family as registered head/base controller where practical | 1 | 0–800 | Low | — | Rigid base/controller mount; feeds RP-03, not moving-head ballast |
| Internal link | UART/USB serial (Vector-style) for SBC↔MCU; CAN only if a 3rd distributed node earns it | on-board | On hand | 0 | I²C local-only / CAN later | 1 | 0–500 | Low | Soldering | Harness |
| Motor/servo driver | Drives base motors + head servos, current sense preferred | Robu / Zbotic | Common | 0–3 d | Separate ESC + servo rail | 1–2 | 500–2,000 | Low | Soldering | Wiring harness |

## Head (RP-01 / RP-06)

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Face display | ~4.3" 16:9, ~95 × 54 mm active area, decent viewing angle, driver available | Robu / Lamington Rd | Common | 0–5 d | Different module fitting the active-area/bezel envelope | 1 | 1,200–4,000 | Med | — | 110–120 W × 60–65 H mm opening + shell fit |
| Smoked face window | Acrylic/PC fitting ~110–120 W × 60–65 H mm opening, hides display edges | Local acrylic | Common | 0–2 d | Tint film over clear panel | 1 | 200–800 | Low | Cutting | Laser/print fit |
| Camera | Head-mounted, moves with head (AD-06), calibratable | Robu | Common | 0–5 d | USB webcam module | 1 | 800–3,000 | Med | — | Mount + FOV clearance |
| Status light | Addressable LED beside camera (SCOPE-17) | Elegoo / Robu | On hand | 0 | Single-colour LED + driver | 1+ | 100–500 | Low | Soldering | Optic/diffuser |
| Head actuators (roll/pitch/yaw) | Smart servos/geared motors + feedback for ~250 g head; Concept A uses body-fixed yaw and moving pitch/roll, with candidate selection gated by transient torque-speed plus busy-minute RMS/current/thermal evidence | Robu / Zbotic / MG Super Labs | Mixed; re-check exact SKU | 0–10 d | Feetech STS class ↔ DYNAMIXEL XL/XC class | 3+ plus one bench sample where needed | 3,000–34,000 | Med–High (exact SKU/cost) | Current/voltage logging, output indicator | 60 mm neck allocation, near-CoM gimbal centre, direct actuation first |
| Head joint structure | Compact yaw load-bearing shaft/bearing, rising pitch yoke with double ear pivots, supported inner roll cradle; ear shells are removable covers, not the structural load path | Local bearing supplier / fabricated parts | Common classes, exact sizes TBD | 0–7 d | Small radial/angular-contact pair ↔ suitable compact supported shaft | set | 500–3,000 | Low–Med | Printer/machining/measurement | Concept A blockout; must prove mass and 60 mm fit before CAD freeze |
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
| Low (frugal/Feetech-class path, on-hand reuse) | **≈ ₹15,000–20,000** |
| High (premium three-DYNAMIXEL head path plus current row maxima) | **≈ ₹70,000–75,000** |

This is a **planning envelope to gate procurement decisions**, not a budget commitment. The much wider upper bound is driven primarily by the current ₹30k–34k three-DYNAMIXEL head-actuator path; it is not the expected cost of the Feetech candidate. The range tightens as the actuator branch and ADRs close.

## Open items

- [ ] Verify local stock/price for the "Now" candidates by walking Lamington Road once (per workbench sourcing note).
- [ ] Add and source a credible Concept B before RP-01 fabrication; Concept A alone does not satisfy the ≥2-concept rule.
- [ ] Resolve battery chemistry candidate (ADR-06) before any pack purchase.
- [ ] Attach a verified source + one acceptable substitute to each architecture-critical row (RP06-G05 gate).
- [ ] Promote selected rows into a later `hardware/bom/` roll-up once ADRs close.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First-pass candidate matrix + first project cost range created; no selections made. |
| 2026-08-27 | 0.4 | Added separate body-IMU path and expanded the head mechanism/actuator rows for the elevated ear-pivot serial-gimbal candidate; no component selected. |
