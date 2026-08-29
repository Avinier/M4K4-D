# RP-01 Mechanism Concepts — Comparison

| Field | Value |
|---|---|
| Status | In progress — Concept A authored as a candidate; Concept B remains open; no mechanism selected |
| Rule | Minimum two credible concepts unless calculation/sourcing eliminates one first (RP plan open input). Sketches and napkin geometry — not CAD. |
| Physical baseline | `../../../01-system/dimensional-baseline.md`: 100 × 180 × 130 mm complete head, ~250 g target, 60 mm neck allocation |

Credibility checklist per concept: load path (no bare servo-horn cantilever), actuator class with a sourcing path, cable route, service/assembly story, physics numbers clearing `intent.md` requirements with margin.

| Criterion | Concept A: elevated ear-pivot serial gimbal | Concept B: open |
|---|---|---|
| Joint order (e.g. yaw→pitch→roll) | Body-fixed yaw → pitch → head-fixed roll. This matches intrinsic face motion and keeps the Euler singularity far outside Makad's pitch range. | |
| Fits 60 mm neck allocation and head intrusion envelope | Candidate only. Yaw bearing/drive must recess into the body/head and the pitch yoke must rise beside the head; generated-reference proportions are explicitly rejected. | |
| Actuation class per axis | Body-fixed yaw actuator; direct pitch and roll actuation first. Feetech/DYNAMIXEL classes remain candidates, not selections. A belt/gear offset is added only if packaging or quantified yaw inertia earns its backlash/compliance cost. | |
| Support/bearing scheme (where does the load actually go?) | Compact yaw shaft/bearing carries axial and overturning load independently of the yaw drive. Pitch is double-supported near the ear-pod locations. Near-CoM roll is a gravity target, not yet a support solution: compare a rear spaced-bearing cartridge, face-clear annular/perimeter support and displaced axis around the selected Waveshare no-touch SKU 30493 envelope, including connector/service clearance and overhung moment. Cosmetic ear shells cover rather than carry pivots. | |
| τ_peak margin per axis (from physics.md) | Pending the per-axis downstream mass tree, 250 g complete-head sensitivity bound, candidate gimbal-centre sweep and separate transient/RMS screen in `physics.md`. A low-axis inverted-pendulum arrangement is not the reference geometry. | |
| Reflected inertia ratio (or UNCOMPUTABLE) | UNCOMPUTABLE until exact actuators publish rotor inertia or the rig measures response. Include lateral pitch-actuator `m·r²` in yaw inertia before adding an offset transmission. | |
| f_n estimate | Pending yoke/cradle stiffness. Screen pitch ≥30 Hz minimum / ≥40 Hz unshaped best case; yaw/roll ≥25/30 Hz per `gates.md`. | |
| Loaded hysteresis / hold stability (geartrain, spline, horn, structure, controller) | Unknown. Do not divide the complete-output 0.25° target equally by three stages. At a fixed command, measure external angle versus reversing output load, reversal delay and hold hunting/current at representative poses; add a combined-orientation case. Small designed preload is a candidate mitigation, not a specification. | |
| Cable route through the workspace | Open/hollow yaw centre; bundle approaches each joint near its axis; pitch loop enters near an ear pivot; one controlled downstream roll loop; no slip ring for current ±55° yaw. Measure restoring torque and endurance. | |
| Sourcing: availability, landed cost, lead time, substitute | Pending candidate-matrix expansion and re-check before purchase. Large Lazy-Susan/NEMA-scale hardware is excluded by moving-mass and 60 mm packaging constraints, not used as a sourcing reference. | |
| Fabrication/assembly/calibration/service story | Rising U-yoke, removable ear bearing covers, independently replaceable actuators, accessible harness connectors, axis-zero registration and complete-output calibration. Detailed CAD waits for the CoM/axis convergence loop. | |
| Failure/safe-rest behaviour (unpowered pose?) | Near-CoM axes reduce uncontrolled gravity fall; small preload/counterbalance may bias a safe direction. Stops and cable loops must bound the unpowered path. Final behaviour is a rig result. | |
| Verdict | **Credible candidate; advance to mass blockout and rig screening, not selected.** Full note: [`elevated-ear-pivot-serial-gimbal.md`](elevated-ear-pivot-serial-gimbal.md). | |

Sketches and per-concept notes as separate files in this folder.
