# RP-01 first actuator paper screen — XC330-M288-T

Date: 2026-09-13. Revision: v0.2. Status: **preliminary external-load screen only; complete paper approval OPEN**.

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

The completed calculation says how hard the head asks each servo to work. It asks relatively modest torque while moving quickly, and persistent imbalance/cable bias can dominate heating. The outstanding work is evidence about how the selected servo behaves at our voltage, duty and mounting, followed by physical motion quality.

To close the paper screen, obtain or measure actuator-internal acceleration evidence, stiffen and re-evaluate the affected structure, obtain voltage-labelled output curves including the registered sag floor, resolve the 65/81 rpm discrepancy, document continuous-duty applicability or an explicit provisional thermal-test basis, and apply the [paper gates](gates.md#paper-screen-gates--v02-draft-2026-09-13). Rerun the payload model whenever the structure, bearing/stop arrangement, axis trim or candidate geometry changes.
