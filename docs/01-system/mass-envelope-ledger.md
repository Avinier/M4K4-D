# Makad V1 Mass / Envelope Ledger

| Field | Value |
|---|---|
| Status | **Living — first pass.** Not a selection; not binding. |
| Version | 0.1 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-08-17 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 2) |
| Consumes | Foundation scale class (`workbench.md`), `system-design-brief.md` responsibility set |
| Feeds | RP-01 (representative head load), RP-06 (integrated layout), head-CAD, engineering budgets |

This ledger is the **head-CAD blocker** named in the plan. Every unknown is expressed as a **range, never zero**. Numbers here are first-pass planning estimates from the approved scale class — *table-liftable, one-person, single-room, follow ≤ 0.5 m/s* — not sourced measurements. They are replaced by measured values as RP-01…RP-07 close (decision-closeout step 6). Do not treat any figure as a committed spec, and do not let a component's absence from a row mean it weighs nothing.

## Scale-class anchors (from approved foundation)

- One person places it on a large tabletop for demonstrations (SCOPE-11) → **table-liftable**.
- "Compact enough to remain approachable" without size minimization (vision).
- Single household room; following capped at **0.5 m/s** (CON-19).
- Powered three-axis head carrying display + camera + status light + audio allowance (SCOPE-02/03/17, AD-02/AD-06).
- Wheeled base, drive architecture deferred (SCOPE-09).

Working envelope target (bounding box, **assumption pending RP-06**): height **300–450 mm**, footprint **Ø/□ 180–280 mm**. These bound the ledger; they are not a design commitment.

## Mass ledger

Ranges carry the current uncertainty. "Basis" states where the number comes from so a later measurement can replace it cleanly.

| Subsystem | Low (g) | High (g) | Basis / assumption | Measured by |
|---|---:|---:|---|---|
| **Head** — shell, display + window, camera, status light/optics, mic(s), speaker allowance if head-mounted, joint brackets, local wiring | 300 | 700 | Small SBC-class face display (~3–5"), single camera, hobby-servo-driven gimbal, printed shell | RP-01 / RP-06 measured head |
| **Body** — main structure, outer shell, internal frame, service panels | 400 | 900 | Printed polymer enclosure at the envelope above, single-room duty | RP-06 |
| **Battery** — cells + holder/pack + protection | 150 | 500 | SBC + small servos + audio, single-room session; chemistry undecided (ADR-06) | RP-02 |
| **Drive** — motors, gearing, wheels, caster/idler, drive brackets | 200 | 600 | Differential-drive candidate at ≤0.5 m/s; architecture deferred (SCOPE-09) | RP-03 |
| **Electronics** — compute board(s), motor/servo drivers, power distribution, regulators, connectors | 150 | 400 | SBC-class compute + driver boards per system-design-brief responsibilities | RP-02 |
| **Wiring** — harness, connectors, strain relief across joints | 60 | 180 | Three-axis moving head harness + base runs; unknown ≠ 0 | RP-01 / RP-02 |
| **Fasteners** — screws, heat-set inserts, brackets, adhesives | 40 | 120 | Repeated-service assembly (heat-set inserts) across head/body/base | RP-06 |
| **Structural / integration margin** (design reserve) | 150 | 400 | ~15–20% reserve against integration growth (AD-08 concurrent-load risk) | Retired as rows firm up |
| **TOTAL (rolled up)** | **1450** | **3800** | Sum of ranges above | — |

First-pass whole-robot mass sits at **≈1.5–3.8 kg** — comfortably inside the table-liftable class the workbench hazard notes assume. If a later measured roll-up trends above ~4 kg, revisit `workbench.md` hazard notes (its own instruction).

## Head envelope detail (RP-01 / head-CAD input)

The head is the first mechanical risk (AD-02) and the CAD blocker, so it gets its own envelope breakdown. All values **assumption, pending RP-06 mock-up**.

| Element | Envelope allowance | Notes |
|---|---|---|
| Face display + window | ~3–5" active area + bezel + smoked window offset | Window hides display edges (character requirement) |
| Camera | small module, moves with head (AD-06) | FOV + calibration clearance reserved |
| Status light + optics | LED beside camera (SCOPE-17) | Placement coupled to camera per AD-06 |
| Microphone(s) | 1–2 capsules | Position TBD; spatial hearing is Candidate, not Core |
| Speaker / enclosure allowance | reserve even if body-mounted | May relocate to body; allowance kept so it is not forgotten |
| Roll/pitch/yaw mechanism | 3 axes, joint order undecided | ≥2 joint-order concepts required before fabrication (plan) |
| Cable bundle + service clearance | bend radius across 3 moving axes | Cable movement is an RP-01 measured item |

**Representative head mass range for RP-01 ballast: 300–700 g**, centre-of-mass and inertia proxy to be set from the RP-06 mock-up before scored RP-01 runs (plan, RP-01 Inputs).

## Open items

- [ ] Fix the working bounding box after RP-06 phase-A sourced envelopes.
- [ ] Narrow head mass range and set centre-of-mass / inertia proxy from the RP-06 mock-up (unblocks RP-01 scored runs).
- [ ] Replace battery row once chemistry is decided in ADR-06 (RP-02).
- [ ] Replace drive row once drive architecture is chosen (RP-03).
- [ ] Retire structural margin into real rows as subsystems firm up.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First-pass ledger created from approved scale class; all rows are ranges pending prototype measurement. |
