# RP-01 Decision

| Field | Value |
|---|---|
| Status | Open |
| Question | Can a manufacturable powered roll/pitch/yaw mechanism carry a representative Makad head while producing safe, repeatable, quiet-enough and characterful motion with acceptable range, reversal, settling, camera behaviour, wiring movement, calibration, and controller failure handling? |
| Feeds | ADR-02 (head mechanism), ADR-03 (controller), ADR-08, ADR-12; mass/power/acoustic budget rows |
| Rule | A failed Core three-axis gate cannot become a two-axis fallback without reopening approved V1 scope. Failed runs stay cited here. |
| Physical constraint | Selected concept must fit `../../01-system/dimensional-baseline.md`, or the conclusion must request and justify a baseline revision. |

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
| A — elevated ear-pivot serial gimbal | **Credible candidate; not selected** | Body-fixed yaw; yaw→pitch→head-fixed-roll order; independent yaw load bearing; pitch pivots associated with the ear-pod locations; planned axial harness route; selected Waveshare no-touch SKU 30493 display envelope | Exact pitch height and A0/A1/A2 point; selected-display-clear roll-axis/support layout and resulting CoM; per-axis mass tree; actuator family, bearing sizes, direct/belt drive, preload, yoke geometry, mass/thermal/cost and scored gate results |
| B | **Required; not authored** | Must satisfy the same physical baseline and evidence rules | Entire concept |

Concept A's source diagram is not a specification. Only the topology extracted into `concepts/elevated-ear-pivot-serial-gimbal.md` is admitted for comparison; its generated-looking labels, proportions and NEMA/Lazy-Susan-scale hardware are excluded.

## Conclusion

*(pass / iterate / reject, selected concept, controller requirements, budget updates, downstream assumptions changed)*
