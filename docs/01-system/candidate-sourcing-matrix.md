# Makad V1 Candidate Sourcing Matrix

| Field | Value |
|---|---|
| Status | **Living — first pass.** Candidates only; **no component is selected.** |
| Version | 0.1 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-08-17 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 1) |
| Feeds | First project cost range (CON-TBD-13), RP-01…RP-07 inputs, later BOM |

The approved foundation **does not select a drive type, processor, camera, actuator, battery, framework, or supplier** (`system-design-brief.md`). Every row here is therefore a **candidate**, chosen to bound specification, availability, and landed cost so prototypes can start and a first cost range can exist. Selection happens only through the ADRs as prototype evidence closes (decision-closeout). Prices/stock are Mumbai planning estimates and **must be re-checked immediately before purchase** (same rule as `workbench.md`). Bench tooling is not repeated here — it lives in `workbench.md`.

Columns follow the plan's required fields (line 102): spec, supplier, availability, lead time, substitute, quantity, landed cost, replacement risk, required tools, fabrication dependency.

## Compute & control

Topology (SBC + MCU split, compute placement, bus, timebase) is a provisional option study in `control-topology-options.md`, resolved by RP-02 → ADR-06/ADR-12. Rows below are candidates for that topology, not selections.

| Component | Candidate spec | Supplier (candidate) | Avail. | Lead | Substitute | Qty | Landed ₹ (est.) | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Main compute (SBC) | SBC-class board, USB/CSI camera, GPIO, enough for perception loop | Robu.in / local | Common | 0–3 d | Alt SBC / SBC+MCU split | 1 | 4,000–9,000 | Med (chip cycles) | — | Case/mount printed |
| Head-aggregation MCU | **Arduino Nano 33 BLE Sense** (nRF52840 M4F) — 3-axis servo loop + limits/watchdog, onboard IMU for head-pose feedback, onboard PDM mic, drives LED; 18×45 mm, 3.3 V | On hand | On hand | 0 | Same-family MCU for head/base parity | 1 | 0 (owned) | Low | — | Head board/mount; see `control-topology-options.md` §6 |
| Real-time controller (MCU) — base/drive | Servo/motor timing + limits + watchdog; prefer same family as head MCU | Elegoo kit / Robu | On hand | 0 | On-SBC RT thread | 1 | 0–800 | Low | — | — |
| Internal link | UART/USB serial (Vector-style) for SBC↔MCU; CAN only if a 3rd distributed node earns it | on-board | On hand | 0 | I²C local-only / CAN later | 1 | 0–500 | Low | Soldering | Harness |
| Motor/servo driver | Drives base motors + head servos, current sense preferred | Robu / Zbotic | Common | 0–3 d | Separate ESC + servo rail | 1–2 | 500–2,000 | Low | Soldering | Wiring harness |

## Head (RP-01 / RP-06)

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Face display | ~3–5" LCD/round, decent viewing angle, driver available | Robu / Lamington Rd | Common | 0–5 d | Different size/round vs rect | 1 | 1,200–4,000 | Med | — | Window + shell fit |
| Smoked face window | Acrylic/PC, hides display edges | Local acrylic | Common | 0–2 d | Tint film over clear panel | 1 | 200–800 | Low | Cutting | Laser/print fit |
| Camera | Head-mounted, moves with head (AD-06), calibratable | Robu | Common | 0–5 d | USB webcam module | 1 | 800–3,000 | Med | — | Mount + FOV clearance |
| Status light | Addressable LED beside camera (SCOPE-17) | Elegoo / Robu | On hand | 0 | Single-colour LED + driver | 1+ | 100–500 | Low | Soldering | Optic/diffuser |
| Head actuators (roll/pitch/yaw) | Servos/geared motors + feedback, sized to 300–700 g head | Robu / Zbotic | Common | 0–5 d | Digital servo ↔ stepper+gear | 3+ | 900–4,500 | Med | — | Joint brackets, ≥2 concepts |
| Microphone(s) | 1–2 capsules, usable stream | Robu | Common | 0–3 d | I2S mic vs USB mic | 1–2 | 200–1,200 | Low | Soldering | Head/body port |

## Drive & base (RP-03)

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Drive motors | Geared, regulate ≤0.5 m/s, architecture deferred (SCOPE-09) | Robu / Zbotic | Common | 0–5 d | DC-gear ↔ stepper | 2 | 600–3,000 | Med | — | Wheel + bracket |
| Wheels + caster/idler | Traction on floor, low speed | Robu / local | Common | 0–3 d | Various dia/tread | 2+1 | 300–1,200 | Low | — | Hub fit |
| Motion safety / limits | E-stop already in `workbench.md` bench scope | — | — | — | — | 1 | (see workbench) | Low | — | Motor-rail wiring |

## Audio & power

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Speaker + amp | Character voice, enclosure allowance (may be body-mounted) | Robu / Lamington Rd | Common | 0–5 d | Different driver size | 1 | 300–1,500 | Low | Soldering | Enclosure/baffle |
| Battery / cells | Chemistry undecided — ADR-06 (18650 holder vs LiPo pouch) | Robu / local | Common | 0–5 d | 18650 ↔ LiPo | 1 pack | 500–2,500 | Med (safety) | LiPo bag/charger | Pack + holder design |
| Power distribution / regulation | Feeds concurrent peak loads (AD-08), brownout-safe | Robu | Common | 0–3 d | Buck modules ↔ integrated PDB | 1 | 400–1,500 | Low | Soldering | Harness |

## Structure & fasteners

| Component | Candidate spec | Supplier | Avail. | Lead | Substitute | Qty | Landed ₹ | Replacement risk | Required tools | Fab dependency |
|---|---|---|---|---|---|---:|---:|---|---|---|
| Printed polymer stock | PLA/PETG for shells & brackets (material choice deferred) | Local filament | Common | 0–2 d | PLA ↔ PETG ↔ ABS/ASA | as needed | 800–2,500 | Low | 3D printer | Print time |
| Heat-set inserts + screws | M3 inserts for repeated service assembly | Robu / local | Common | 0–3 d | Self-tapping (worse for service) | set | 300–1,000 | Low | Soldering iron tip | Boss design |
| Bearings / pivots | Head joints & base as needed | Robu / local | Common | 0–5 d | Bushings ↔ ball bearings | few | 200–1,000 | Low | — | Joint design |

## First project cost range (CON-TBD-13)

Rolled up from the candidate ranges above (**components only — excludes the `workbench.md` bench tooling of ₹10k–25k**):

| Bound | Estimate |
|---|---:|
| Low (frugal, substitutes, on-hand reuse) | **≈ ₹17,000** |
| High (headroom, spares, better parts) | **≈ ₹49,000** |

This is a **planning envelope to gate procurement decisions**, not a budget commitment. It tightens as ADRs close and rows move from candidate to selected.

## Open items

- [ ] Verify local stock/price for the "Now" candidates by walking Lamington Road once (per workbench sourcing note).
- [ ] Add ≥2 head-mechanism actuation concepts as distinct candidate rows before RP-01 fabrication.
- [ ] Resolve battery chemistry candidate (ADR-06) before any pack purchase.
- [ ] Attach a verified source + one acceptable substitute to each architecture-critical row (RP06-G05 gate).
- [ ] Promote selected rows into a later `hardware/bom/` roll-up once ADRs close.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First-pass candidate matrix + first project cost range created; no selections made. |
