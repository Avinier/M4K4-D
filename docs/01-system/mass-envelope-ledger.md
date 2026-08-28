# Makad V1 Mass / Envelope Ledger

| Field | Value |
|---|---|
| Status | **Living — dimensional baseline active; remaining mass values provisional.** |
| Version | 0.4 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-08-27 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 2) |
| Consumes | `dimensional-baseline.md`, foundation scale class (`workbench.md`), `system-design-brief.md` responsibility set |
| Feeds | RP-01 (representative head load), RP-06 (integrated layout), head-CAD, engineering budgets |

This ledger is the **head-CAD blocker** named in the plan. `dimensional-baseline.md` now supplies committed target geometry, component placement, and a ~250 g moving-head target. Other mass values remain first-pass planning estimates from the approved scale class — *table-liftable, one-person, single-room, follow ≤ 0.5 m/s* — not sourced measurements. They are replaced by measured values as RP-01…RP-07 close (decision-closeout step 6). Do not let a component's absence from a row mean it weighs nothing.

## Scale-class anchors (from approved foundation)

- One person places it on a large tabletop for demonstrations (SCOPE-11) → **table-liftable**.
- "Compact enough to remain approachable" without size minimization (vision).
- Single household room; following capped at **0.5 m/s** (CON-19).
- Powered three-axis head carrying the display, central camera, status light, structure, and local wiring (SCOPE-02/03/17, AD-02/AD-06).
- Two independently powered wheels, a front caster, and a mandatory rear anti-tip skid (`dimensional-baseline.md`).

Current target bounding box: **300 H × 205 W × 180 D mm**. RP-06 validates this baseline against sourced envelopes; it does not silently replace it.

## Mass ledger

Ranges carry the current uncertainty. "Basis" states where the number comes from so a later measurement can replace it cleanly.

| Subsystem | Low (g) | High (g) | Basis / assumption | Measured by |
|---|---:|---:|---|---|
| **Head** — shell, display + window, central camera, status light/optics, joint brackets, local wiring | 250 | 250 | Current **~250 g target**, not a tolerance band; microphones and speaker are body-mounted | RP-01 / RP-06 measured head |
| **Body** — main structure, outer shell, internal frame, service panels | 400 | 900 | Printed polymer enclosure at the envelope above, single-room duty | RP-06 |
| **Battery** — cells + holder/pack + protection | 150 | 500 | Low and forward of the drive axle; chemistry undecided (ADR-06) | RP-02 |
| **Drive** — motors, gearing, Ø84 mm wheels, front caster, mandatory rear skid, drive brackets | 200 | 600 | Two-wheel differential drive; 170 mm track, 110 mm axle-to-caster target, ~70 mm rear skid reach at ≤14 mm floor height | RP-03 |
| **Electronics** — compute board(s), motor/servo drivers, power distribution, regulators, connectors | 150 | 400 | SBC-class compute + driver boards per system-design-brief responsibilities | RP-02 |
| **Wiring** — harness, connectors, strain relief across joints | 60 | 180 | Three-axis moving head harness + base runs; unknown ≠ 0 | RP-01 / RP-02 |
| **Fasteners** — screws, heat-set inserts, brackets, adhesives | 40 | 120 | Repeated-service assembly (heat-set inserts) across head/body/base | RP-06 |
| **Structural / integration margin** (design reserve) | 150 | 400 | ~15–20% reserve against integration growth (AD-08 concurrent-load risk) | Retired as rows firm up |
| **TOTAL (rolled up)** | **1400** | **3350** | Sum using the 250 g head target in both columns; not a head tolerance claim | — |

The current first-pass whole-robot roll-up is **≈1.4–3.35 kg**, with substantial uncertainty outside the head target. If a later measured roll-up trends above ~4 kg, revisit `workbench.md` hazard notes (its own instruction).

## Head envelope detail (RP-01 / head-CAD input)

The head is the first mechanical risk (AD-02) and the CAD blocker, so it gets its own breakdown. Target dimensions come from `dimensional-baseline.md`; RP-06 validates packaging and RP-01 replaces preliminary load properties with CAD/measured values.

| Element | Envelope allowance | Notes |
|---|---|---|
| Complete head including ears | 100 H × 180 W × 130 D mm | Moving-head outer target |
| Head core excluding ears | ~100 H × 140–145 W × 125–130 D mm | Space for display, camera, brackets, and neck intrusion |
| Face display active area | ~95 W × 54 H mm (~4.3-inch 16:9) | Display target, not diagonal-only shorthand |
| Face opening / bezel | ~110–120 W × 60–65 H mm | Border and mounting room around display |
| Ear pods | ~55–65 mm diameter; ~17–20 mm side protrusion each | No microphones. Concept A may use removable ear shells as pitch-bearing covers; inner yoke/frame carries load and all bearing/yoke mass remains in the head roll-up. |
| Camera | one central small module, moves with head (AD-06) | FOV + calibration clearance reserved |
| Status light + optics | LED beside camera (SCOPE-17) | Placement coupled to camera per AD-06 |
| Roll/pitch/yaw mechanism | 3 axes in a 60 mm vertical neck allocation; joint order not selected | Concept A proposes body-fixed yaw → elevated ear-pivot pitch → head-fixed roll with the pitch/roll centre near the measured 3D CoM; ≥1 additional credible concept is still required. |
| Cable bundle + service clearance | bend radius across 3 moving axes | Cable movement is an RP-01 measured item |

**Representative RP-01 moving-head target: ~250 g**, with preliminary inertia **~0.001 kg·m²** and preliminary neck peak-torque estimate **~0.2 N·m**. The mass target supersedes the old 300–700 g ballast range. CAD-derived centre of mass/inertia and the axis-specific physics calculation must replace the preliminary estimates before final actuator selection; the scored rig load is registered from the representative as-built/CAD configuration.

Body packaging must separately reserve four PDM MEMS microphones, the speaker and its acoustic cavity, the battery **low and forward of the drive axle**, and primary electronics. Integrated layout targets `x_CoM=+25 mm` forward of the axle and `h_CoM=124 mm` above the floor; none of these body subsystems belongs in moving-head ballast under the current baseline.

## Open items

- [ ] Validate the 300 × 205 × 180 mm bounding box with sourced envelopes in RP-06; revise the baseline explicitly if it cannot be met.
- [ ] Produce a ~250 g head mass blockout and replace the preliminary CoM/inertia proxy with CAD mass properties before final RP-01 actuator selection.
- [ ] Include yoke, bearings, actuator offsets, ear bearing covers and complete harness in the blockout; iterate the A0/A1/A2 gimbal-centre points after their mass shifts the CoM.
- [ ] Replace battery row once chemistry is decided in ADR-06 (RP-02).
- [ ] Replace the drive mass range after RP-03 selects and measures the motors, transmissions, wheels, caster, skid, and brackets.
- [ ] Retire structural margin into real rows as subsystems firm up.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First-pass ledger created from approved scale class; all rows are ranges pending prototype measurement. |
| 2026-08-25 | 0.2 | Adopted the current dimensional/packaging baseline; replaced the 300–700 g head assumption with the ~250 g target; removed microphones and speaker from the moving head; updated drive geometry and roll-up. |
| 2026-08-25 | 0.3 | Corrected battery placement forward of axle and added the integrated CoM and bounded rear-skid geometry required by the acceleration-tip model. |
| 2026-08-27 | 0.4 | Added the elevated ear-pivot serial-gimbal candidate to the head blockout assumptions; clarified that ear shells may cover pivots but do not carry structure and that all mechanism/harness mass remains in the moving-head roll-up. |
