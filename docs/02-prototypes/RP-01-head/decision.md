# RP-01 Decision

| Field | Value |
|---|---|
| Status | **Mechanism decision open; material/finish/mass decisions D-01…D-08 locked** |
| Revised | 2026-08-31 |
| Question | Can a manufacturable powered roll/pitch/yaw mechanism carry a representative Makad head while producing safe, repeatable, quiet-enough and characterful motion with acceptable range, reversal, settling, camera behaviour, wiring movement, calibration, and controller failure handling? |
| Feeds | ADR-02 (head mechanism), ADR-03 (controller), ADR-08, ADR-12; mass/power/acoustic budget rows |
| Rule | A failed Core three-axis gate cannot become a two-axis fallback without reopening approved V1 scope. Failed runs stay cited here. |
| Physical constraint | Selected concept must fit the current envelope/placement baseline and the RP-01 material/finish decisions; the conclusion must carry the required system head-mass revision. |

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

These decisions do not close the final Makad production material, measured head mass, neck mechanism or system-level baseline revision.

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
