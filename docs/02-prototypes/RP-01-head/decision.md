# RP-01 Decision

| Field | Value |
|---|---|
| Status | **Mechanism path: Concept A for RP-01; Concept B not authored. Material/mass, C2 controller-boundary and C2 module decisions locked. Actuator family and scored gates still open.** |
| Revised | 2026-09-09 |
| Question | Can a manufacturable powered roll/pitch/yaw mechanism carry a representative Makad head while producing safe, repeatable, quiet-enough and characterful motion with acceptable range, reversal, settling, camera behaviour, wiring movement, calibration, and controller failure handling? |
| Feeds | ADR-02 (head mechanism), ADR-03 (controller), ADR-08, ADR-12; mass/power/acoustic budget rows |
| Rule | A failed Core three-axis gate cannot become a two-axis fallback without reopening approved V1 scope. Failed runs stay cited here. |
| Physical constraint | Selected concept must fit the current envelope/placement baseline, revised head-load lower bound, selected C2 controller boundary and RP-01 material/finish decisions. |

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
| D-08 | Use the approximately 490 g 1.2 mm-wall **pre-M008 lower bound**, then add the required C2 controller hardware for RP-01 sizing; the old 250 g target is infeasible for this build. |

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

## First-layout CAD decisions

The fitting discussion is recorded in [cad/head/decisions.md](cad/head/decisions.md), dated 2026-09-07. It fixes the first layout's rib/backplate construction and service splits, coaxial direct roll trial, external yaw service loop beside a solid spindle, and rolling-cradle C2 placement. The builder selected both rounded cosmetic ears attached to the rolling face/cradle, so they move with yaw, pitch and roll. Mounting geometry and support clearance remain to be demonstrated.

These are working layout inputs, not scored outcomes or a final mechanism/actuator selection. The [CAD requirements](cad/head/requirements.md) retain CAD-01…CAD-06, and [packaging estimates](cad/head/packaging-estimates.md) distinguish sourced envelopes from unverified fit allowances.

The [pre-layout brief](cad/head/pre-layout-brief.md) inventories existing mass/geometry evidence and prepares the internal arrangement before the first CAD blockout. Candidate pivot coordinates will be evaluated in that layout rather than selected from appearance alone.

The builder selected **A0 as the first-layout balance target** in [HEAD-CAD-07](cad/head/decisions.md#head-cad-07--a0-balance-target). Derive the pitch pivot coordinates from the estimated pitch-carried CoM and keep roll near its own carried CoM. A1/A2 remain fallback comparisons; achieved balance, final mechanism acceptance and actuator selection remain open.

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
| A — elevated ear-pivot serial gimbal | **RP-01 implementation path; not gate-selected** | Body-fixed yaw; yaw→pitch→head-fixed-roll order; independent yaw load bearing; pitch pivots associated with the ear-pod locations; selected Waveshare no-touch SKU 30493 display envelope; RP-01 PLA/finish decisions; first-layout coaxial roll, face-attached rolling ears and external yaw cable loop per the CAD register | Exact pitch coordinates to achieve selected A0; complete fit; rolling-ear clearance (no shroud); per-axis mass tree; actuator family, bearing SKUs, validated drive arrangement, PLA thermal/creep, scored gate results |
| B | **Not authored; comparison waived 2026-09-09** | Builder directed RP-01 to proceed on A only. Parallel/B will not be developed for this prototype. | Entire concept — closed without a counterpart |

Concept A's source diagram is not a specification. Only the topology extracted into `concepts/elevated-ear-pivot-serial-gimbal.md` is admitted. On 2026-09-09 the builder waived authoring Concept B so remaining time goes to detailing A (Layout 03). This does not pass RP-01 gates or freeze a servo family.

## Conclusion

*(pass / iterate / reject, selected concept, controller requirements, budget updates, downstream assumptions changed)*
