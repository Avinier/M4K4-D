# Makad V1 Mass / Envelope Ledger

| Field | Value |
|---|---|
| Status | **Living — dimensional baseline active; remaining mass values provisional.** |
| Version | 0.13 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-09-12 |
| Governed by | `risk-prototype-plan.md` §"Continuous sourcing and data workstream" (deliverable 2) |
| Consumes | `dimensional-baseline.md`, foundation scale class (`workbench.md`), `system-design-brief.md` responsibility set |
| Feeds | RP-01 (representative head load), RP-06 (integrated layout), head-CAD, engineering budgets |

This ledger is the canonical system mass/envelope roll-up. `dimensional-baseline.md` supplies committed target geometry and component placement; RP-01 now supplies a **Layout 03 D/E tree** with a nominal ~509 g complete head at M008=20 g and a ~499–524 g C2 sensitivity. It is not an accepted complete-head mass, and it already contains two 23 g XC330-size reference packages that must be replaced per servo candidate. Other mass values remain first-pass planning estimates from the approved scale class — *table-liftable, one-person, single-room, follow ≤ 0.5 m/s* — not sourced measurements. They are replaced by measured values as RP-01…RP-07 close (decision-closeout step 6). Do not let a component's absence from a row mean it weighs nothing.

## Scale-class anchors (from approved foundation)

- One person places it on a large tabletop for demonstrations (SCOPE-11) → **table-liftable**.
- "Compact enough to remain approachable" without size minimization (vision).
- Single household room; following capped at **0.5 m/s** (CON-19).
- Powered three-axis head carrying the display, any unavoidable lightweight display/head-node electronics, central camera, status light, structure, and local wiring (SCOPE-02/03/17, AD-02/AD-06). RP-01 has no installed runtime head IMU; bench instrumentation is not robot mass.
- Two independently powered wheels, a front caster, and a mandatory rear anti-tip skid (`dimensional-baseline.md`).

Current target bounding box: **300 H × 205 W × 180 D mm**. RP-06 validates this baseline against sourced envelopes; it does not silently replace it.

## Mass ledger

Ranges carry the current uncertainty. "Basis" states where the number comes from so a later measurement can replace it cleanly.

| Subsystem | Low (g) | High (g) | Basis / assumption | Measured by |
|---|---:|---:|---|---|
| **Head** — shell, display + window, display renderer, separate C2 motion controller, central camera, status light/optics, moving actuator/bearing portions, joint structure, connectors and local wiring | `499 E` | TBD | Layout 03 analytical sweep is ~499/509/524 g at M008=10/20/35 g; 509 g is nominal, not measured. The selected Waveshare ESP32-S3-Zero installed assembly remains `U`, and servo candidates can exceed the XC330-size reference masses already included. Replace with candidate-specific trees and ultimately M900. Main Linux SBC, microphones, speaker and bench Nano/DevKitC-1/IMU are body-mounted or excluded. | RP-01 / RP-06 measured head |
| **Body** — main structure, outer shell, internal frame, service panels | 400 | 900 | Printed polymer enclosure at the envelope above, single-room duty | RP-06 |
| **Battery** — cells + holder/pack + protection | 150 | 500 | Low and forward of the drive axle; chemistry undecided (ADR-06) | RP-02 |
| **Drive** — motors, gearing, Ø84 mm wheels, front caster, mandatory rear skid, drive brackets | 200 | 600 | Two-wheel differential drive; 170 mm track, 110 mm axle-to-caster target, ~70 mm rear skid reach at ≤14 mm floor height | RP-03 |
| **Electronics** — compute board(s), motor/servo drivers, power distribution, regulators, connectors | 150 | 400 | SBC-class compute + driver boards per system-design-brief responsibilities | RP-02 |
| **Wiring** — harness, connectors, strain relief across joints | 60 | 180 | Three-axis moving head harness + base runs; unknown ≠ 0 | RP-01 / RP-02 |
| **Fasteners** — screws, heat-set inserts, brackets, adhesives | 40 | 120 | Repeated-service assembly (heat-set inserts) across head/body/base | RP-06 |
| **Structural / integration margin** (design reserve) | 150 | 400 | ~15–20% reserve against integration growth (AD-08 concurrent-load risk) | Retired as rows firm up |
| **TOTAL (rolled up)** | **~1649** | **`3100 + M_head`** | Non-head low planning rows plus the 499 g analytical head case; final upper head mass remains open and this is not a tolerance claim | — |

The current first-pass whole-robot roll-up has a **minimum analytical value of approximately 1.65 kg** using the 499 g head sensitivity case. Its upper bound remains open until the complete head mass `M_head` and candidate servo set are established; the other subsystem high rows sum to approximately 3.10 kg before the head. If a later measured roll-up trends above ~4 kg, revisit `workbench.md` hazard notes (its own instruction).

## Head envelope detail (RP-01 / head-CAD input)

The head is the first mechanical risk (AD-02) and the CAD blocker, so it gets its own breakdown. Target dimensions come from `dimensional-baseline.md`; RP-06 validates packaging and RP-01 replaces preliminary load properties with CAD/measured values.

| Element | Envelope allowance | Notes |
|---|---|---|
| Complete head including integrated side pods/pivots | **104 H × 150 W × 115 D mm — Layout 03** | Current moving-head planning envelope from selected component geometry; manufacturing and RP-06 integrated fit remain open |
| Head core excluding crown/side pods | **86 H × 130 W × 115 D mm — Layout 03** | Space for display, camera, brackets, lightweight electronics, connector/service clearance and neck intrusion |
| Face display active area | 95.04 W × 53.86 H mm nominal (4.3-inch 800×480 IPS) | Selected no-touch Waveshare ESP32-S3-LCD-4.3, SKU 30493 |
| Face aperture / bezel | ~94–95 W × 53–54 H mm optical aperture within ~110–115 W × 60–65 H mm bezel/window treatment; ≥68 mm hidden module clearance | Selected module body is approximately 106.1 × 67.8 mm; listed 118 g is an unverified product value, not yet a mass-ledger measurement |
| Integrated side pods / pivot covers | Layout 03 Ø60 mm hollow rolling ears; complete width 150 mm | No microphones. Ears attach to the rolling face; inner yoke/frame carries joint loads and all bearing/yoke mass remains in the head roll-up. |
| Camera | selected Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, SC0874; 25 W × 24 H × 12.4 D mm | Moves with head (AD-06). Seller-reported mass is not accepted; weigh module, connector retention, mount and the moving portion of the selected interconnect separately. |
| Status light + optics | LED beside camera (SCOPE-17) | Placement coupled to camera per AD-06 |
| Roll/pitch/yaw mechanism | 3 axes in a 60 mm vertical neck allocation; **body yaw → elevated pitch → coaxial supported roll** is the RP-01 path | Layout 03 models Concept A with A0 estimated balance and an XC330-size packaging reference. Concept B is waived; servo SKU, purchased interfaces and physical evidence remain open. |
| Cable bundle + service clearance | bend radius across 3 moving axes | Cable movement is an RP-01 measured item |

**Representative RP-01 planning load: nominal ~509 g complete at M008=20 g, with ~499–524 g C2 sensitivity in the current Layout 03 D/E tree.** M008 remains `U` as physical evidence, and the tree's XC330-size servo references must be substituted per candidate. This is not a target or accepted measurement. The former ~250 g target, generic ~0.001 kg·m² inertia proxy and ~0.2 N·m neck-torque estimate are obsolete for RP-01 sizing. Candidate-specific centre of mass/inertia and axis calculations precede actuator selection; the scored rig load is registered from the representative as-built/CAD configuration.

Body packaging must separately reserve four PDM MEMS microphones, the speaker and its acoustic cavity, the battery **low and forward of the drive axle**, and primary electronics. Integrated layout targets `x_CoM=+25 mm` forward of the axle and `h_CoM=124 mm` above the floor; none of these body subsystems belongs in moving-head ballast under the current baseline.

## Open items

- [ ] Validate the 300 × 205 × 180 mm bounding box with sourced envelopes in RP-06; revise the baseline explicitly if it cannot be met.
- [x] Produce a complete Layout 03 D/E per-axis blockout including yoke, bearing, reference-actuator, ear and harness allowances.
- [ ] Replace the reference actuators with every screened servo candidate and rerun mass, CoM, inertia and A0 sensitivity before selection.
- [ ] Weigh the selected SKU 30493 sample without packaging and with its installed mount/harness; replace the 118 g listing evidence in the RP-01 model.
- [ ] Weigh the selected Camera Module 3 Wide SC0874 sample, connector retention, mount and moving interconnect separately; record their CoM coordinates and per-axis downstream membership.
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
| 2026-08-28 | 0.5 | Kept near-CoM roll as a gravity target while making a display-clear support/load-path blockout mandatory before Concept A can be selected. |
| 2026-08-29 | 0.6 | Propagated the display-study clarification that every unavoidable head-local display controller, head node, head IMU, connector, mount and local harness segment counts inside the unchanged ~250 g target. |
| 2026-08-29 | 0.7 | Added the adopted IPS prototype envelope and made its unverified 118 g listing value an immediate RP-01 measurement gate rather than a mass assumption. |
| 2026-08-29 | 0.8 | Replaced the rank-1 candidate wording with the locked SKU 30493 display baseline; actual module and installed masses remain required measurements. |
| 2026-08-29 | 0.9 | Replaced the generic camera allowance with the locked visible-light Raspberry Pi Camera Module 3 Wide SC0874 envelope; left installed module/mount/interconnect masses as required measurements. |
| 2026-08-30 | 0.10 | Propagated the display-derived 95 × 150 × 115 mm nominal complete-head envelope, smaller core, optical-aperture distinction and integrated-pivot side-pod width limit from dimensional baseline v1.7. |
| 2026-09-02 | 0.11 | Replaced the obsolete 250 g system head row with the ~490 g pre-M008 lower bound plus required C2 hardware, reopened the whole-robot upper roll-up, and retired the preliminary inertia/torque values from RP-01 sizing. |
| 2026-09-07 | 0.12 | Recorded the selected C2 module (Waveshare ESP32-S3-Zero) against the head row while keeping M008 unknown until the installed assembly is weighed, and excluded the ESP32-S3-DevKitC-1 bench twin from the ledger. Roll-up values unchanged. |
| 2026-09-12 | 0.13 | Propagated Layout 03's 104 × 150 × 115 mm envelope and provisional 362/436/509 g per-axis tree. Kept M008 physically unknown, retained the 10/20/35 g analytical sensitivity and made candidate-specific servo substitution explicit. No W evidence added. |
