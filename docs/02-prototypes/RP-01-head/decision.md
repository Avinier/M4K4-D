# RP-01 Decision

| Field | Value |
|---|---|
| Status | **Mechanism decision open; material/mass and C2 controller-boundary decisions locked** |
| Revised | 2026-09-02 |
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
| CTRL-04 | The exact C2 module, servo family, electrical interface, bus update rate and purchase remain open. C1 may reopen only through display-carrier change control or evidence that the received carrier materially differs from the official schematic. |
| CTRL-05 | RP-01 has no runtime head IMU. Servo encoders provide runtime joint angle; temporary bench IMU measurements do not enter the installed mass ledger. |

Any controller-boundary change must supersede CTRL-01…CTRL-05 and propagate through `control-topology-options.md`, M008, firmware interfaces, physics, rig and gates.

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
| A — elevated ear-pivot serial gimbal | **Credible candidate; not selected** | Body-fixed yaw; yaw→pitch→head-fixed-roll order; independent yaw load bearing; pitch pivots associated with the ear-pod locations; planned axial harness route; selected Waveshare no-touch SKU 30493 display envelope; RP-01 PLA/finish decisions | Exact pitch height and A0/A1/A2 point; selected-display-clear roll-axis/support layout and resulting CoM; 110–115 mm versus ~90 mm depth; per-axis mass tree around the ~490 g pre-M008 lower bound plus the required C2 controller; actuator family, bearing sizes, direct/belt drive, preload, yoke geometry, PLA thermal/creep result, mass/thermal/cost and scored gate results |
| B | **Required; not authored** | Must satisfy the same physical baseline and evidence rules | Entire concept |

Concept A's source diagram is not a specification. Only the topology extracted into `concepts/elevated-ear-pivot-serial-gimbal.md` is admitted for comparison; its generated-looking labels, proportions and NEMA/Lazy-Susan-scale hardware are excluded.

## Conclusion

*(pass / iterate / reject, selected concept, controller requirements, budget updates, downstream assumptions changed)*
