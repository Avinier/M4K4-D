# RP-01 first actuator paper screen — XC330-M288-T

Date: 2026-09-13. Revision: v0.3 (2026-09-25, [paper-closure pass](#paper-closure-pass--v03-2026-09-25) appended). Status: **paper items bounded for the working family (M181 yaw, M288 pitch/roll; `ACT-01` in `decision.md`); bench evidence, structure and CAD items OPEN; complete paper approval OPEN**.

The first named candidate is ROBOTIS **XC330-M288-T**, SKU **902-0173-000**, evaluated at each output axis with direct 1:1 transmission. Its payload-side torque numbers are encouraging, but pitch/roll are not yet cleared as complete mechanism candidates: actuator-internal acceleration demand is unknown and the current structure fails the preliminary stiffness-risk screen. Yaw is additionally voltage-sensitive. This record does not select a production SKU, authorize purchase/fabrication or close RP-01.

## Demand and configuration

Demand comes from [fullproofmath.md §11.3](fullproofmath.md#mechanical-sensitivity-run--2026-09-13) and its linked `layout03-paper-model.xlsx`. The existing 1,560-case calculation is accepted as the **external rigid-body/payload** input to this screen. Values below omit the torque/current required to accelerate the actuator's own rotor and gear train; they are not complete actuator transient demand. They use the model's physical-law controllers; the separate demand-aligned bound remains separately reported, not relabelled as measured cable behaviour.

| Axis | Worst peak, N·m | Speed at that peak | Worst busy-minute RMS, N·m | Independent rapid speed envelope |
|---|---:|---:|---:|---:|
| Pitch | 0.095289 | 57.8°/s = 9.633 rpm | 0.049164 | 236°/s = 39.333 rpm |
| Roll | 0.055991 | 70.2°/s = 11.700 rpm | 0.031431 | 180°/s = 30.000 rpm |
| Yaw | 0.109917 | 90.5°/s = 15.083 rpm | 0.024952 | 378°/s = 63.000 rpm |

Peak torque, peak speed and RMS may come from different cases. Check all operating points, not just these three torque peaks. A rectangle using maximum torque and maximum speed together is a conservative preliminary test; failing that rectangle does not itself fail an actual trajectory.

## Missing internal acceleration demand

The manufacturer performance curve is a steady-state output curve. It does not by itself quantify the extra current required to accelerate the XC330 rotor and gear train during the authored reversals. The current workbook contains payload inertia only.

For the nominal M288 ratio `N=288`, the pitch payload referred to the motor is approximately:

`J_pitch/N² = 8.78×10⁻⁹ kg·m² = 0.0878 g·cm²`.

That is a comparison threshold, not the XC330 rotor inertia. No supported rotor/gear inertia was retained, so neither the size of the correction nor a claimed 2–4× multiplier is accepted. Close this item with official internal-inertia data or a controlled unloaded-versus-loaded acceleration/current characterization. Until then, the transient result remains OPEN even where the payload point lies under the plotted curve.

## Structural dependency

The current pitch frame screens near 6–9 Hz under a simplified PLA-member estimate, versus the 30/40 Hz targets, and the open roll saddle screens near 21 Hz versus 25/30 Hz. These are risk estimates rather than FEA or measured modes, but they prevent this actuator record from declaring the complete mechanism credible. The structure must be stiffened and then verified under representative load; a torque margin cannot compensate for a resonant load path near the laugh content.

The [Layout-03 mass model](../RP-06-cad/head/layout-03/mass_layout.py) already assigns 23 g to each moving XC330 housing. The roll housing belongs to P, and the pitch housing to Y. Their modelled intrinsic inertias use oriented 29 × 20 × 34 and 34 × 29 × 20 mm packaging boxes, respectively. Roll housing centre is `(-92, roll_y, roll_z-7.5)` mm; pitch housing centre is `(pitch_x-7.5, 32, pitch_z)` mm. With the current solved datums these are approximately `(-92,-1.105,39.419)` and `(-45.465,32,45.553)` mm.

The [assembly source](../RP-06-cad/head/layout-03/layout_model.py) uses the existing `xc330.stp` reference. Substituting this candidate's documented housing mass therefore adds **zero mass** to the current paper tree. Horns, hubs, bearing portions and harness already have separate owners. The body-fixed yaw housing is outside the moving-head tree. Matching mass and external envelope does not validate the assumed internal CoM/inertia or detailed mounting fit; these remain E-grade and require installed-part verification.

## Manufacturer evidence and voltage cases

[ROBOTIS e-manual](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/) documents 23 g, a 20 × 34 × 26 mm body, and a 3.7–6.0 V operating range, with 5.0 V recommended. Published endpoints are:

| Supply | Stall torque | No-load speed | Role in this screen |
|---|---:|---:|---|
| 5.0 V | 0.93 N·m | 81 rpm | Proposed nominal bench supply; not an actual measured rail |
| 3.7 V | 0.69 N·m | 59 rpm | Severe low-voltage sensitivity at a documented endpoint; not predicted sag |

The actual regulator, minimum voltage at each servo during concurrent motion, wiring drop and transient overvoltage remain unregistered. A different sag floor needs its own supported curve; do not silently interpolate the endpoints into a claimed measured curve.

The [manufacturer performance graph](https://emanual.robotis.com/assets/images/dxl/x/x330/xc330-m288_performance_graph.png) was visually inspected. Around 0.12 N·m it shows approximately 68 rpm. Thus all three reported peak-torque points lie well below the plotted moving-performance trace. The graph also appears above the conservative maximum-torque/maximum-speed corners, although yaw has the least speed clearance. **The image itself does not label voltage or test duration.** Its nominal interpretation is provisional; it does not establish either a sagged-voltage curve or continuous thermal capability. Four-quadrant/braking behaviour and control limits still need coverage.

There is a source discrepancy: [ROBOTIS America's product page](https://robotis.us/products/dynamixel-xc330-m288-t) lists 65 rpm, while the e-manual lists 81 rpm at 5 V. This review uses the voltage-specific e-manual for endpoint arithmetic but leaves the conflict open. It matters particularly for yaw. Do not turn this screen into purchasing approval until the exact SKU/firmware/test conditions are reconciled.

## Numerical endpoint diagnostic — not a performance curve

For audit only, `tau_proxy = tau_stall × (1 - rpm/rpm_no_load)`. This model is not manufacturer test data or a pass threshold.

| Axis | 5 V proxy torque at its peak-torque speed | 3.7 V proxy torque at that speed | 5 V proxy torque at independent speed envelope |
|---|---:|---:|---:|
| Pitch | 0.8194 N·m | 0.5773 N·m | 0.4784 N·m |
| Roll | 0.7957 N·m | 0.5532 N·m | 0.5856 N·m |
| Yaw | 0.7568 N·m | 0.5136 N·m | 0.2067 N·m |

These numbers explain why the torque peaks look easy yet voltage still matters. At 3.7 V, the yaw speed envelope is **63 rpm > 59 rpm no-load**: M288 fails that specific full-envelope/voltage combination irrespective of its low-speed torque. This is not a rejection at a well-regulated 5 V and is not an assertion that the planned rail will sag to 3.7 V. Pitch and roll clear the no-load necessary condition at 3.7 V; loaded passage remains open.

## RMS and thermal evidence

ROBOTIS America publishes **0.186 N·m estimated continuous torque at 5 V**, explicitly derived from 20% of stall. This is a manufacturer estimate, not an independently measured continuous rating under Makad's enclosure, mounting and duty conditions. The [global product specification](https://en.robotis.com/shop_en/item.php?it_id=902-0173-000) leaves continuous-operation fields unspecified.

| Axis | Screened RMS | Manufacturer estimate / demand |
|---|---:|---:|
| Pitch | 0.049164 N·m | 3.78× |
| Roll | 0.031431 N·m | 5.92× |
| Yaw | 0.024952 N·m | 7.45× |

All three clear that **estimated 5 V thermal screen**. No ratio here is a validated safety factor. There is no justified 3.7 V continuous curve in the retrieved evidence, and the 5 V estimate must not be scaled automatically. Do not convert output RMS torque to measured motor heating using stall torque/current alone. One busy minute defines duty; repeating that duty until thermal behaviour is established is a separate rig task.

## Paper conclusion and next evidence

**All axes: retain XC330-M288-T only as a named comparison candidate. The external-load points are encouraging, but complete transient acceptance is OPEN because actuator-internal acceleration demand is unknown. Pitch/roll additionally depend on structural redesign/verification. Yaw is conditional at proposed 5 V and fails the full rapid envelope at the 3.7 V sensitivity endpoint.** A faster XC330-M181-T is a reasonable yaw comparison if the rail floor or speed-source conflict cannot be resolved; it has not been passed by this record.

**Layout 04 yaw update, 2026-09-23.** [Layout 04](../RP-06-cad/head/layout-04/README.md) puts the yaw servo off-axis beside the body's Pi cooler and couples it through a **1:1 spur pair**, so the direct-1:1 assumption above still holds at the output. The yaw candidate becomes the **XC330-M181-T**: no-load 129 rpm at 5.0 V and 95 rpm at 3.7 V against the 63 rpm rapid envelope, with 0.60 N·m stall at 5.0 V against a yaw peak of about 0.12 N·m once Layout 04's +9% yaw inertia is applied. This clears the M288's 3.7 V yaw speed failure. M288 remains the pitch/roll comparison candidate. The spur mesh adds backlash that counts against the ≤0.25° complete-output target and needs preload or an anti-backlash gear. The transient, internal-inertia and thermal items above remain OPEN for M181 as well.

The completed calculation says how hard the head asks each servo to work. It asks relatively modest torque while moving quickly, and persistent imbalance/cable bias can dominate heating. The outstanding work is evidence about how the selected servo behaves at our voltage, duty and mounting, followed by physical motion quality.

To close the paper screen, obtain or measure actuator-internal acceleration evidence, stiffen and re-evaluate the affected structure, obtain voltage-labelled output curves including the registered sag floor, resolve the 65/81 rpm discrepancy, document continuous-duty applicability or an explicit provisional thermal-test basis, and apply the [paper gates](gates.md#paper-screen-gates--v02-draft-2026-09-13). Rerun the payload model whenever the structure, bearing/stop arrangement, axis trim or candidate geometry changes.

## Paper-closure pass — v0.3, 2026-09-25

Scope: the working family recorded as `ACT-01` in [`decision.md`](decision.md) — **XC330-M181-T for yaw (through the Layout 04 1:1 spur pair), XC330-M288-T for pitch and roll**, on the 5.0 V `PB-HEAD` rail of RP-02 `board-specs.md` §5.4. This pass closes or bounds every item that needs no hardware. It does not freeze the family, pass a paper gate or authorize a purchase. Grades: `D` sourced, `E` estimate, `U` unknown.

### Sources retrieved

| Fact | Value | Grade / source |
|---|---|---|
| Motor | Coreless DC, both models | `D`, ROBOTIS e-manual [M288](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/), [M181](https://emanual.robotis.com/docs/en/dxl/x/xc330-m181/) |
| Gear ratio | M288 288.35:1; M181 180.62:1 | `D`, same |
| M181 stall / no-load | 0.52 N·m, 1.34 A, 95 rpm at 3.7 V; 0.60 N·m, 1.80 A, 129 rpm at 5.0 V; 0.66 N·m, 2.15 A, 155 rpm at 6.0 V | `D`, same |
| Position sensor | AS5601 12-bit absolute, 360°, i.e. on the output (0.088°/count) | `D`, same |
| Backlash | Not published ("Backlash: NA") | `D` that it is absent; [ROBOTIS America M288](https://robotis.us/products/dynamixel-xc330-m288-t), [M181](https://robotis.us/products/dynamixel-xc330-m181-t) |
| Continuous torque | M288 0.186 N·m, M181 0.12 N·m, both "20% of stall" estimates at 5 V | `D` that ROBOTIS states them; `E` as capability |
| M181 no-load speed on the US page | 129 rpm, agrees with the e-manual | `D` |
| Performance-graph conditions | "Measured under conditions simulating a gradually increasing load … real world performance will generally be closer to the performance graph, not the rated stall torque." Voltage is not printed | `D`, e-manual note |
| Rotor inertia, reference coreless motors | Faulhaber 1016 SR 0.12 g·cm² (2.1–2.3 mNm stall); 1024 SR 0.11–0.12 g·cm² (4.3–5.1 mNm); 1224 SR 0.18 g·cm² (5.3–5.4 mNm); 1219 G 0.11–0.14 g·cm² | `D` for those motors, [Faulhaber datasheets](https://www.faulhaber.com/fileadmin/Import/Media/EN_1224_SR_FMM.pdf) |

### P02 — curve provenance and minimum voltage

- **Graph voltage is 5.0 V by consistency (`E`).** The M288 graph runs to 1.75 A, above the 1.34 A stall current at 3.7 V, and shows 73 rpm at 0.06 N·m, which fits 81 rpm no-load at 5.0 V and not 97 rpm at 6.0 V. The M181 graph shows 108 rpm at 0.078 N·m, above its 95 rpm no-load at 3.7 V and well under 155 rpm at 6.0 V. The graph is used from here on as the 5.0 V moving curve, per ROBOTIS's own note that it is the realistic curve.
- **Minimum servo-terminal voltage in normal operation: 4.74 V (`E`).** The `LTC3119` head rail regulates 4.891–5.109 V worst case (`board-specs.md` §5.4.2 feedback row) through the whole pack window, and the registered drop from converter to servo terminal is ≤ 150 mV. 3.7 V is reached only in the F-11 overload fault, where the servos are meant to shut down. **This retires the 3.7 V sensitivity endpoint as a design case.**
- **Derate at 4.74 V (`E`).** Interpolating the published no-load endpoints gives 76.6 rpm (M288) and 122.2 rpm (M181), 0.946–0.947 of the 5.0 V value. Graph speeds are scaled by 0.946 below; no other curve scaling is applied.
- **The 65 / 81 rpm conflict is non-controlling.** ROBOTIS America's 65 rpm for the M288 is below the graph's own 73 rpm at light load and is not explained. Pitch and roll clear their envelopes even with a 65 rpm no-load line (below), and yaw no longer uses the M288. The conflict stays recorded but no longer blocks a decision.

### P03 / P05 — actuator-internal inertia, bounded

No XC330 rotor or gear inertia is published. The two models share one motor: both draw 1.80 A at 5 V stall and both reach about 23,300 motor rpm no-load (81 × 288.35 ≈ 129 × 180.62). Their output stall torque divided by ratio is 3.2–3.3 mNm, so the motor is a coreless of roughly 4–5.5 mNm stall. The comparable Ø10–12 mm Faulhaber coreless motors carry 0.11–0.18 g·cm². Adding pinion and first-stage gear gives the bound used here:

**`J_motor-side` = 0.11 g·cm² (low) to 0.25 g·cm² (high), `E`.** Reflected to the output as `J_motor-side × N²`. The spur pair, horn and later gear stages are small against this and are left to the ±bound.

| Axis | Servo | Reflected `J_eq`, 10⁻³ kg·m² | vs carried load | Internal peak `J_eq·α` | Total peak (external worst + internal) | Moving capability at the envelope speed, 4.74 V | Result |
|---|---|---:|---:|---:|---:|---:|---|
| Pitch | M288 | 0.92–2.08 | 1.3–2.9× | 0.065–0.147 N·m | ≤ 0.160–0.242 N·m | about 0.39 N·m at 41.6 rpm graph (0.37 N·m even on a straight line to 65 rpm no-load at 5.0 V) | Clears, 0.15 N·m margin at the high bound |
| Roll | M288 | 0.92–2.08 | 1.4–3.2× | 0.031–0.071 N·m | ≤ 0.087–0.127 N·m | about 0.47 N·m at 31.7 rpm graph | Clears |
| Yaw | M181 | 0.36–0.82 | 0.3–0.8× | 0.030–0.067 N·m | ≤ 0.149–0.187 N·m | about 0.215 N·m at 66.5 rpm graph | **Clears, 0.028 N·m (15%) at the high bound; the tightest axis** |

Method: this is the conservative rectangle — worst external peak plus the internal term at peak acceleration, set against the curve at the axis's maximum speed, each taken from different cases. Internal torque is proportional to `α`, so it peaks exactly where the payload's dynamic torque peaks. Yaw external demand includes Layout 04's +9% inertia (0.1099 → 0.1198 N·m). Graph readings are visual (`E`, about ±0.01 N·m).

Findings:

- **The internal term is large on pitch and roll** (the M288's high ratio): it matches or exceeds the carried head. The earlier unaccepted "2–4×" guess was the right order; on the high bound it is 2.9–3.2× the carried inertia. Every axis still clears the moving curve at 4.74 V.
- **Yaw has the least margin.** M181's lower ratio keeps its internal term small, but its speed demand sits further down its curve.
- **Current at those points (graph current, `E`):** pitch about 0.63 A, roll about 0.43 A, yaw about 0.82 A at the high bound (about 0.48 / 0.37 / 0.68 A at the low bound). The graph current is well above torque ÷ stall-`K` (0.3–0.45 A appears even at light load), so RP-02 `board-specs.md` §5.4.1's torque-derived 0.62 A sum understates the rail load. Coincident high-bound peaks sum to about 1.9 A against the 2 A `PB-HEAD` design allowance, and **yaw's 0.82 A sits about 10% under its `BD-13` Current Limit of 0.9 A**. The Current Limit could clip a legitimate yaw transient; RP-02 should review it (see `openitems.md`).
- **Braking.** The stored energy at peak speed is small (yaw about 0.04 J, pitch about 0.02 J at the high bound, `E`), inside what the `PB-HEAD` 5.74 V clamp is sized for.

P05 moves from `U` to a sourced `E` bound. P03 closes on paper for this family. A measured value (bench test B1 below) replaces the bound before the gate freeze.

### P04 — RMS with internal inertia

The nominal A0 busy-minute RMS (`fullproofmath.md` §11.3, zero bias) is almost purely `J_load·α`, which yields the RMS acceleration per axis: pitch 10.7, roll 4.7, yaw 13.6 rad/s². Since internal torque is `J_eq·α` in phase with the payload's dynamic torque, adding `J_eq × α_RMS` to the worst screened RMS is an upper bound:

| Axis | Worst RMS, external | + internal (high bound) | Total ≤ | ROBOTIS 20%-of-stall estimate | Ratio |
|---|---:|---:|---:|---:|---:|
| Pitch (M288) | 0.0492 | 0.0222 | 0.071 N·m | 0.186 | 2.6× |
| Roll (M288) | 0.0314 | 0.0098 | 0.041 N·m | 0.186 | 4.5× |
| Yaw (M181) | 0.0272 (×1.09) | 0.0111 | 0.038 N·m | 0.12 | 3.1× |

All three clear the manufacturer estimate with internal inertia included. This remains an **estimate screen**: thermal passage in the sealed head needs bench test B3.

### P08 addition — transmission lash

The complete-output hysteresis target is `≤0.50°` minimum viable, `≤0.25°` best case (`storyboard.md`). XC330 backlash is unpublished. The servo's encoder is on its output shaft, so its own gear lash sits inside its position loop, but the **Layout 04 yaw spur pair is outside the loop**: any mesh lash there appears one-for-one at the head. A plain printed or module-0.5 spur mesh can plausibly reach several tenths of a degree by itself (`E`), using the whole best-case budget. The yaw pair therefore needs an anti-backlash gear (split scissor gear) or a spring-preloaded centre distance. This is recorded as proposed gate P09 in `gates.md`; the gear choice belongs to the RP-06 head CAD.

### What stays open, and the measurement that closes each

| ID | Bench test | Closes |
|---|---|---|
| B1 | One M288 and one M181, output free then with a known flywheel: step the goal current, log position and present current, fit reflected inertia and friction | P03/P05 bound → measured `J_eq`; confirms or revises the 1.9 A head-rail and 0.9 A yaw-limit findings |
| B2 | Speed–torque sweep on the real `LTC3119` rail at 5.0 V and at 4.74 V, with a brake or torque arm | P02 graph voltage and derate; retires the 65 / 81 rpm conflict |
| B3 | Repeat the BC-60 busy minute inside a representative head enclosure; log current, input voltage and servo temperature to a pre-registered equilibrium criterion | P04 thermal |
| B4 | Loaded reversal hysteresis at the servo horn, then through the yaw spur pair | P09 lash budget |
| B5 | Servo-terminal voltage logging during simultaneous three-axis motion (`HM-15` startle) | P02 minimum-voltage claim |

A one-off bench purchase of one M181-T and one M288-T for B1–B5 is allowed without freezing the family (`openitems.md`, Phase B).

### Update after the head structure revision, 2026-09-25

Head Layout 04 was revised the same day for the CAD blockers (stiffened pitch frame, torsion box, trim seats, official servo mass properties; see its README). The carried inertias rose to **0.000675 / 0.000779 / 0.001282 kg·m²** roll / pitch / yaw: +3 / +7 / +19 % against the Layout 03 workbook values, with yaw including Layout 04's turntable. Scaling each whole worst external peak and RMS by that ratio (conservative, since the bias terms do not scale) and adding the high-bound internal term:

| Axis | Total peak ≤ | Moving capability, 4.74 V | Margin | Total RMS ≤ | vs ROBOTIS 20%-of-stall estimate |
|---|---:|---:|---:|---:|---:|
| Pitch (M288) | 0.249 N·m | 0.39 N·m | 36 % | 0.075 N·m | 2.5× |
| Roll (M288) | 0.129 N·m | 0.47 N·m | 73 % | 0.042 N·m | 4.4× |
| Yaw (M181) | 0.198 N·m | 0.215 N·m | **8 %** | 0.041 N·m | 2.9× |

Every axis still clears. **Yaw is now tight, at 8 %** of the moving curve on the high internal-inertia bound. At the graph, its current is about **0.87 A, 3 % under its 0.9 A `BD-13` Current Limit**, and the coincident high-bound sum is about 1.96 A against the 2 A `PB-HEAD` allowance. B1 (measured internal inertia) is therefore the first bench test to run. If it lands near the high bound, raise the yaw Current Limit or trim the yaw trajectory. The workbook itself should be rerun with the Layout 04 tree rather than scaled.
