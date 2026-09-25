# RP-01 Decision

| Field | Value |
|---|---|
| Status | **Mechanism path: Concept A for RP-01; Concept B explicitly waived. Material/finish, C2 controller-boundary and C2 module decisions locked. Working actuator family `ACT-01` (2026-09-25): XC330-M181-T yaw, XC330-M288-T pitch/roll at 5 V; its paper items are bounded, and bench evidence, structural and CAD/hardware blockers remain. Paper approval, fabrication release, actuator freeze and scored gates remain OPEN.** |
| Revised | 2026-09-25 |
| Question | Can a manufacturable powered roll/pitch/yaw mechanism carry a representative Makad head while producing safe, repeatable, quiet-enough and characterful motion with acceptable range, reversal, settling, camera behaviour, wiring movement, calibration, and controller failure handling? |
| Feeds | ADR-02 (head mechanism), ADR-03 (controller), ADR-08, ADR-12; mass/power/acoustic budget rows |
| Rule | A failed Core three-axis gate cannot become a two-axis fallback without reopening approved V1 scope. Failed runs stay cited here. |
| Physical constraint | Selected concept must fit the current envelope/placement baseline, revised head-load lower bound, selected C2 controller boundary and RP-01 material/finish decisions. |
| Remaining-open index | Folder-wide list lives in [`../openitems.md`](../openitems.md). This file remains the RP-01 decision record. |

## Locked RP-01 sub-decisions

`material-finish-mass-decision.md` locks the following for the RP-01 build without selecting a neck mechanism:

| Decision | Locked RP-01 input |
|---|---|
| D-01 | Print RP-01 structure and skin in PLA. |
| D-02 | Do not promote PLA to the final Makad material decision from this prototype alone. |
| D-03 | Keep M010–M012 flagged provisional until RP-01 thermal/creep evidence closes. |
| D-04 | Use real visible M2 button-head fasteners and own them separately in M021a. |
| D-05 | Apply the complete nine-step finish system after a weighed 60 × 60 mm coupon validates coating mass and scale. |
| D-06 | Keep cosmetic seams integral; create real splits only for demonstrated assembly/service access. |
| D-07 | Model 0.3–0.5 mm panel height offsets in CAD. |
| D-08 | The old 250 g target is infeasible. For current screening use the active layout's nominal D/E tree (Layout 04, revised 2026-09-25: ~370/464/588 g roll/pitch/yaw; Layout 03 was ~362/436/509 g) at M008=20 g, retain 10/20/35 g C2 sensitivity, and substitute each servo candidate before selection; physical M008/M900 remain unweighed. |

The same record makes the full-width opaque window mask, display flashing path and separable yaw-plane harness boundary mandatory CAD requirements. Any departure from D-01…D-08 requires an explicit superseding decision and propagation through the mass register, physics, rig and gates.

These decisions do not close the final Makad production material, measured head mass or neck mechanism.

### Locked controller and sensing boundary

| Decision | Locked RP-01 input |
|---|---|
| CTRL-01 | Motion firmware targets ESP32-S3 from the start. The Nano 33 BLE Sense is bench equipment only. |
| CTRL-02 | **C1 is closed and rejected for selected display carrier SKU 30493. C2 is selected:** one separate ESP32-S3 motion-controller module is installed and owned by M008. |
| CTRL-03 | The display carrier's ESP32-S3 owns eye rendering/display communication. The C2 ESP32-S3 executes synchronized yaw/pitch/roll trajectories and owns the smart-servo bus, limits, watchdog, E-stop/fault handling and command expiry. Smart servos retain only their local inner motor-control loops. |
| CTRL-04 | **The exact C2 module is selected: Waveshare ESP32-S3-Zero** (ESP32-S3FH4R2, 4 MB flash / 2 MB PSRAM, headerless castellated, 23.5 × 18 mm, 19 exposed GPIO). Servo family, electrical interface, bus update rate and purchase authorization remain open. C1 may reopen only through display-carrier change control or evidence that the received carrier materially differs from the official schematic. |
| CTRL-05 | RP-01 has no runtime head IMU. Servo encoders provide runtime joint angle; temporary bench IMU measurements do not enter the installed mass ledger. |
| CTRL-06 | Motion firmware is developed on a bench **ESP32-S3-DevKitC-1-N8R8**. That board is bench equipment under `workbench.md`: it is not installed, not in the mass ledger or BOM, and does not create a second firmware target. Only the board-pin mapping differs between it and the installed Zero, and it lives in one configuration header. |

Three constraints follow from the selected module and bind the pin assignment and CAD:

- **E-stop, fault and any other safe-at-boot signal must not use GPIO0, GPIO3, GPIO45 or GPIO46** — these are ESP32-S3 strapping pins and are not deterministic through reset.
- **GPIO21 carries the board's WS2812 LED** and is excluded from the motion/safety assignment.
- **The Zero has no USB-to-UART bridge.** Flashing uses native USB with BOOT held, so the sealed head needs a C2 flashing path as well as the display one; see CAD-04a.

The module selection is a screen against pin budget, volume and sourcing. It does not close RP02-G05: measured loop, link and timestamp performance remain required evidence. Single-source risk on the Zero is accepted with the DevKitC-1 recorded as the repackaging fallback.

Any controller-boundary change must supersede CTRL-01…CTRL-06 and propagate through `control-topology-options.md`, M008, firmware interfaces, physics, rig and gates.

### Working actuator family

| Decision | Working RP-01 input |
|---|---|
| ACT-01 | **ROBOTIS XC330 at a regulated 5.0 V: XC330-M181-T (180.62:1) for yaw, XC330-M288-T (288.35:1) for pitch and roll.** Dynamixel Protocol 2.0 on a TTL half-duplex multidrop bus from C2. Dated 2026-09-25. |

Basis:

- **Yaw is M181** because Layout 04 moved the yaw servo into the body and drives the disc through a 1:1 spur pair. The M181's 129 rpm no-load (95 rpm at 3.7 V) covers the 63 rpm yaw envelope, where the M288 (59 rpm at 3.7 V) failed. Pitch and roll keep the M288's higher torque at lower speed.
- **The supply stays 5 V.** RP-02 accepted this family as `BA-03` (`../RP-02-electrical/board-specs.md` §1.1) and built `PB-HEAD` around it: an `LTC3119` buck-boost regulating 5.0 V through the whole 2S pack window, with per-axis Current Limits, a latching trunk protector and a 5.74 V clamp (`BD-04`, `BD-05`, `BD-13`, `BD-14`). The minimum servo-terminal voltage in normal operation is 4.74 V (`E`); 3.7 V is a fault case only.
- **Alternatives rejected for V1.** A 7.4 V-class servo (e.g. Feetech STS3215) has an 8.4 V maximum that the default-mode charger's 8.455 V worst case exceeds with no trim, drops yaw speed near a flat pack, and would change the bus to Feetech TTL. A 12 V class forces a 3S pack and reopens `PCB-01`, `PCB-02`, the charger and the battery tub. Either reopens `ACT-01` only through a superseding decision here and in RP-02.
- **Paper screen.** With actuator-internal inertia bounded, every axis clears the moving torque–speed curve at 4.74 V and ROBOTIS's continuous-torque estimate by 2.5× or more. After the 2026-09-25 head structure revision raised the yaw inertia by 19%, yaw has the least margin: 8% on the curve, and about 0.87 A against its 0.9 A Current Limit at the high internal-inertia bound. That makes bench test B1 the first to run ([actuator-screen-01.md §Paper-closure pass](actuator-screen-01.md#paper-closure-pass--v03-2026-09-25); `gates.md` v0.3).

`ACT-01` is a working choice, like `BA-03` on the RP-02 side. **It does not freeze the family, pass P01–P09 or authorize a production purchase.** One M181-T and one M288-T may be bought for bench tests B1–B5. The freeze needs:

1. bench tests B1–B5: measured internal inertia, a speed–torque sweep on the real rail, thermal in a representative enclosure, reversal lash, and terminal voltage under three-axis motion;
2. P07 structure: stiffened in CAD 2026-09-25 (frame FEA about 41 Hz pitch, 84 Hz roll mount); still to be verified by a loaded tap/ring-down test (B6), which includes the servo's own compliance;
3. P08 and P09 hardware: the CAD items (fasteners, stops, 696-2Z bearing, sign mapping, trim seats, yaw scissor pinion) were done 2026-09-25; purchased-part trial fits, stop impact and measured lash (B4) remain;
4. dated builder approval of the paper gates, then the family freeze.

Once frozen, the family fixes the C2 servo-bus protocol and electrical interface (CTRL-04); bus rate and homing remain firmware items. Any change to `ACT-01` must propagate through `actuator-screen-01.md`, `gates.md`, the RP-06 head mass tree and RP-02 `PB-HEAD`.

## First-layout CAD decisions

The fitting discussion is recorded in [head/decisions.md](../RP-06-cad/head/decisions.md), dated 2026-09-07. It fixes the first layout's rib/backplate construction and service splits, coaxial direct roll trial, external yaw service loop beside a solid spindle, and rolling-cradle C2 placement. The builder selected both rounded cosmetic ears attached to the rolling face/cradle, so they move with yaw, pitch and roll. Mounting geometry and support clearance remain to be demonstrated.

These are working layout inputs, not scored outcomes or a final mechanism/actuator selection. The [CAD requirements](../RP-06-cad/head/requirements.md) retain CAD-01…CAD-06, and [packaging estimates](../RP-06-cad/head/packaging-estimates.md) distinguish sourced envelopes from unverified fit allowances.

The [pre-layout brief](../RP-06-cad/head/pre-layout-brief.md) inventories existing mass/geometry evidence and prepares the internal arrangement before the first CAD blockout. Candidate pivot coordinates will be evaluated in that layout rather than selected from appearance alone.

The builder selected **A0 as the first-layout balance target** in [HEAD-CAD-07](../RP-06-cad/head/decisions.md#head-cad-07--a0-balance-target). Derive the pitch pivot coordinates from the estimated pitch-carried CoM and keep roll near its own carried CoM. A1/A2 remain fallback comparisons; achieved balance, final mechanism acceptance and actuator selection remain open.

## Gate outcomes

| Gate | Outcome | Evidence (run IDs) | Notes |
|---|---|---|---|
| RP01-G01 Safety | | | |
| RP01-G02 Three-axis Core | | | |
| RP01-G03 Motion quality | | | |
| RP01-G04 Integration | | | |
| RP01-G05 Buildability | | | |
| RP01-G06 Evidence | | | |

## Candidate register

| Candidate | Status | What is fixed for comparison | What remains open |
|---|---|---|---|
| A — elevated ear-pivot serial gimbal | **RP-01 implementation path; not gate-selected** | Body-fixed yaw; yaw→pitch→head-fixed-roll order; independent yaw load bearing; pitch pivots associated with the ear-pod locations; selected Waveshare no-touch SKU 30493 display envelope; RP-01 PLA/finish decisions; first-layout coaxial roll, face-attached rolling ears and external yaw cable loop per the CAD register | Verify the stiffened pitch frame and roll mount under load (frame FEA passes; tap test B6); measure actuator-internal inertia (bounded on paper; B1); purchased-part trial fits for the 696-2Z bearings, stop dowels, inserts and servo case screws; stop impact; measured balance trim through the ear and rear-cover seats; complete fit and rolling-ear clearance; per-axis `W` mass tree; voltage/thermal/hysteresis/creep evidence (B2–B5); yaw scissor-pinion lash (P09, B4); freeze of the `ACT-01` working family and scored gate results. CAD blockers from the 2026-09-13 audit (screw collisions, stop placement, bearing SKU, sign multipliers, trim path) were closed 2026-09-25 |
| B | **Not authored; comparison waived 2026-09-09** | Builder directed RP-01 to proceed on A only. Parallel/B will not be developed for this prototype. | Entire concept — closed without a counterpart |

Concept A's source diagram is not a specification. Only the topology extracted into `concepts/elevated-ear-pivot-serial-gimbal.md` is admitted. On 2026-09-09 the builder waived authoring Concept B so remaining time goes to detailing A (Layout 03). This does not pass RP-01 gates or freeze a servo family. The 2026-09-13 C01 screen (`actuator-screen-01.md`) only shows that the external payload demand looks plausible against retained XC330 data; it is not a complete paper pass or freeze.

## Conclusion

**Current outcome: ITERATE — RP-01 remains open.** Retain Concept A, the verified external rigid-body workbook and the `ACT-01` working family. Revise/verify the structural and hardware items recorded in `fullproofmath.md` §12 and `gates.md` P07–P09, replace the paper bound on actuator-internal demand with bench tests B1–B5, then rerun the affected screen before freezing the actuator or registering scored physical runs.
