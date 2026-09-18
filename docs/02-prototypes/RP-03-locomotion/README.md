# RP-03 — Drive and Local Motion-Safety Rig

| Field | Value |
|---|---|
| Status | **Parts 1–5 remain complete at design-definition level.** `RP03-P1-REG-01` … `RP03-P5-REG-01` (2026-09-17). Brief-gap close 2026-09-18 issued `RP03-P1-REG-02` … `RP03-P4-REG-02` (operating cases, remaining physics, complete drive sets, TTL/cutoff/`CA-14` header). Numeric thresholds, candidate freeze, purchase and scored evidence stay open. Phase A is live on paper; scored runs wait on the workbench gate, timebase, and this rig |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.12 §RP-03; folder construction record [`plan.md`](plan.md) |
| Purpose | Close **ADR-04** (wheeled-drive and passive-support geometry) and **ADR-07** (obstacle and tabletop-edge sensing) *provisionally*; supply the drive `W` rows that ADR-06 sizing waits on; freeze the C3 pin map, motor-driver/sensor interface and base message set that RP-02 left open; deliver the measured base model RP-04 composes against |

RP-01 is an object. RP-02 is a set of states and interfaces. **RP-03 is a vehicle plus a safety authority.** It is the first prototype that can destroy itself (a desk edge), the first with real inductive and regenerative load on the motor bus, and the first with a sensor inside the stop path.

## Start here

| Document | What it owns | Phase live |
|---|---|---|
| [Intent](intent.md) | Why RP-03 exists; the two questions kept separate; ADR table; inherited inputs; `BM-00…BM-14` character read; `FS-*`; non-goals; phase ladder; evidence rules | A |
| [Storyboard](storyboard.md) | Authored panels `BM-00…BM-14`; operating-case grammar; `FS-01…11`; wheel-velocity profile library; kinematic export | A |
| [Physics](physics.md) | `a_tip` as a **range**; four loading cases; head-pose CoM; slope 2.0°; heat; low-voltage; flutter; support triangle; CON-TBD-14 *proposal* | A |
| [Concepts](concepts/README.md) | Two competing concepts and the filled comparison. **Concept A is the working lead, not a freeze** | A |
| [Drivetrain screen](drivetrain-screen-01.md) | Complete **Set A / Set B**; `D01…` class rows; paper P01–P09 vs the sets. **Set A / D02 is a reference-unit lead, not a freeze** | A |
| [Sensing screen](sensing-screen-01.md) | `S01…` cliff/obstacle/bump/IMU; coverage/latency/C3 I/O. **S01/S04/S06/S07 are leads, not a freeze** | A |
| [Base control](base-control-architecture.md) | `BC-01…BC-10`; C3 pin map v0.1 (≥2 spare safe GPIO); `BASE_*` draft; candidate TTL | A |
| [Fault matrix](fault-matrix.md) | `F-31…F-45` plus cross-listed `F-19/F-22/F-26`; campaign order bench → floor → tabletop last | A (rows), B/C (campaign) |
| [Rig](rig.md) | Ugly chassis, ballast CoM, sensor interposer, catch fixture, course, readiness checklist | A (design), B (build) |
| [Gates](gates.md) | Paper `RP03-P01…P09` scored against the sets (OPEN); physical candidate `RP03-G01…G06` including cutoff-coast; **registered section empty** | A (candidate) |
| [Decision](decision.md) | Inherited locks; `BD-01…07` paper-confirmed 2026-09-18; Part registrations; ADR ladder; candidate register | — |
| [Folder plan](plan.md) | Construction record: layout, Part order, what each file may not contain | Retired into this README's organization record; file kept |
| [Prototype open items](../openitems.md) | Folder-wide remaining-open index | — |
| `cad/` | Blockout **after** a concept freeze. Working lead ≠ freeze. See [`cad/README.md`](cad/README.md) | — |
| `runs/` | Run records per [`run-record-convention.md`](../../01-system/run-record-convention.md) | — |

Namespaces (no glossary): `BM-` panels · `D` drivetrain · `S` sensing · `BC-` base-control rules · `F-3x` faults · `BD-` builder decisions · `RP03-P` paper gates · `RP03-G` physical gates · `RP03-P<n>-REG-<nn>` Part records.

## Owned elsewhere — link, do not copy

| Subject | Home | Why it is not here |
|---|---|---|
| Drive geometry targets | [`dimensional-baseline.md`](../../01-system/dimensional-baseline.md) | Programme-wide; RP-03 measures, does not re-derive |
| Drive / battery mass rows | [`mass-envelope-ledger.md`](../../01-system/mass-envelope-ledger.md) | RP-03 populates the drive row; physics did not move 200–600 g |
| `LG-04` / `LG-10` and G02 invariant | [`power-energy-ledger.md`](../../01-system/power-energy-ledger.md) | Two budgets means one is wrong |
| `OM/BS/EV/CC/LP`, `MD-01` | RP-02 [`state-register.md`](../RP-02-electrical/state-register.md), [`load-model.md`](../RP-02-electrical/load-model.md) | RP-03 extends; it does not fork |
| C0↔MCU framing, expiry, heartbeat, arm nonce | RP-02 [`link-contract.md`](../RP-02-electrical/link-contract.md) v0.4 C0↔C2 (`RP02-P4-REG-01`); v0.5 C0↔C3 **semantics** (`RP02-P4-REG-02`). Byte layouts stay open | Envelope lives there; payloads are defined here |
| `PA-13` motor authority, `PB-DRIVE*` | RP-02 [`power-architecture.md`](../RP-02-electrical/power-architecture.md) | Keys registered; drive `W` is RP-03's |
| `F-19` / `F-22` / `F-26` | RP-02 [`fault-matrix.md`](../RP-02-electrical/fault-matrix.md) | Cross-listed here, not renumbered |
| C3 I/O budget and `CA-*` | RP-02 [`compute-control-architecture.md`](../RP-02-electrical/compute-control-architecture.md) | Pin map v0.1 is the RP-03 fill of that budget |
| Sourcing rows | [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md) §Drive & base | Programme-wide |
| Bench, PSU, E-stop, battery gate | [`workbench.md`](../../01-system/workbench.md) | Programme-wide |
| Run identity | [`run-record-convention.md`](../../01-system/run-record-convention.md) | Programme-wide |
| Timebase | [`timebase.md`](../../01-system/timebase.md) | Scored G01–G06 need it implemented |

## The finding that must not become a target

`a_tip ≈ 2.0 m/s²` is a **placement target** at `x_CoM = +25 mm`, `h_CoM = 124 mm`. A lumped Layout 03 model does not hit it: `a_tip` lands about **0.9–1.9 m/s²** if the battery stays low and forward, and **changes sign** if the battery sits on or behind the axle. Storyboard `a_peak` 0.80–1.00 m/s² only has margin when ballast restores `x_CoM ≥ +20 mm`. If the target is missed, the dimensional baseline is revised — commanded acceleration is not quietly shrunk to hide it. Detail: [`physics.md`](physics.md) §2.

## What to do next, in order

1. Do not buy. Set A / `D02` / `DRV-B` / `S01` / `S04` / `S06` / `S07` are leads. A reference motor on the bench is equipment until a freeze says otherwise.
2. CAD pass 1 envelope/datum model is still deferred by folder policy (`cad/README.md`) while Concept A remains a lead — that is a remaining policy conflict with the brief, not closed here.
3. When a driver evaluation board and one reference motor are on the bench: Phase A C3 loop-rate, encoder capture and watchdog feed. Exploratory. Not a scored RP-03 run. Implement `timebase.md`.
4. Freeze G01–G06 numeric thresholds **before** inspecting scored data. Build the ugly chassis. Then Phase B on the floor, Phase C caught-tabletop last. The 240 fps acted mock-up in `plan.md` is still open.

Paper brief-gaps (operating cases, BD confirmation, remaining physics, TTL/cutoff/`CA-14`, complete drive sets) closed 2026-09-18 under `RP03-P1-REG-02` … `RP03-P4-REG-02`.

## Organization record — 2026-09-17

Created by builder direction after RP-01 Layout 03 paper demand and RP-02 Parts 1–4 were defined. The folder follows the RP-02 pattern (Part registrations, evidence classes, thresholds freeze before data) because RP-03's two closures are different kinds of object: ADR-04 closes into *geometry*, ADR-07 into *architecture*. Mixing them is how a chassis quietly chooses the sensors.

`plan.md` is the construction record. Parts 1–5 are now populated at design-definition level. This README is the start-here index; it is not canonical for any number, SKU, pin or threshold.
