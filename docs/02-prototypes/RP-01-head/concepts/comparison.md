# RP-01 Mechanism Concepts — Comparison

| Field | Value |
|---|---|
| Status | Concept A is the RP-01 path; Concept B will not be authored (builder, 2026-09-09). No scored mechanism selection. |
| Rule | Minimum two credible concepts unless the builder closes one path first. Concept B waived 2026-09-09. |
| Physical baseline | ~95 × 150 × 115 mm nominal complete head within a 90–100 × 145–155 × 110–120 mm validation band; `../material-finish-mass-decision.md` provisional ~490 g pre-M008 lower bound at 1.2 mm PLA plus required C2 hardware; 60 mm neck allocation |

Credibility checklist per concept: load path (no bare servo-horn cantilever), actuator class with a sourcing path, cable route, service/assembly story, physics numbers clearing `intent.md` requirements with margin.

First-layout construction and fitting choices are recorded in [head CAD decisions](../cad/head/decisions.md). Both cosmetic ears attach to the rolling face/cradle. Concept B was waived on 2026-09-09; gate outcomes remain open.

| Criterion | Concept A: elevated ear-pivot serial gimbal | Concept B |
|---|---|---|
| Joint order (e.g. yaw→pitch→roll) | Body-fixed yaw → pitch → head-fixed roll. This matches intrinsic face motion and keeps the Euler singularity far outside Makad's pitch range. | Not authored. Builder waived the comparison on 2026-09-09. |
| Fits 60 mm neck allocation and head intrusion envelope | Candidate only. Yaw bearing/drive must recess into the body/head and the pitch yoke must rise beside the head; generated-reference proportions are explicitly rejected. Compare the current 110–115 mm core depth with an approximately 90 mm blockout before CAD freeze. | |
| Actuation class per axis | Body-fixed yaw actuator; direct pitch and roll actuation first. Feetech/DYNAMIXEL classes remain candidates, not selections. A belt/gear offset is added only if packaging or quantified yaw inertia earns its backlash/compliance cost. | |
| Support/bearing scheme (where does the load actually go?) | Compact yaw shaft/bearing carries axial and overturning load independently of the yaw drive. Pitch is double-supported near the ear-pod locations. Near-CoM roll is a gravity target, not yet a support solution: compare a rear spaced-bearing cartridge, face-clear annular/perimeter support and displaced axis around the selected Waveshare no-touch SKU 30493 envelope, including connector/service clearance and overhung moment. Cosmetic ear shells cover rather than carry pivots. | |
| τ_peak margin per axis (from physics.md) | Pending the per-axis downstream mass tree around the current ~490 g `E` pre-M008 lower bound **plus C2**, candidate gimbal-centre sweep and separate transient/RMS screen in `physics.md`. Old 250 g / 0.2 N·m conclusions are inadmissible. A low-axis inverted-pendulum arrangement is not the reference geometry. | |
| Reflected inertia ratio (or UNCOMPUTABLE) | UNCOMPUTABLE until exact actuators publish rotor inertia or the rig measures response. Include lateral pitch-actuator `m·r²` in yaw inertia before adding an offset transmission. | |
| f_n estimate | Pending yoke/cradle stiffness. Screen pitch ≥30 Hz minimum / ≥40 Hz unshaped best case; yaw/roll ≥25/30 Hz per `gates.md`. | |
| Loaded hysteresis / hold stability (geartrain, spline, horn, structure, controller) | Unknown. Do not divide the complete-output 0.25° target equally by three stages. At a fixed command, measure external angle versus reversing output load, reversal delay and hold hunting/current at representative poses; add a combined-orientation case. Small designed preload is a candidate mitigation, not a specification. | |
| Cable route through the workspace | First layout: external guided yaw loop beside a solid spindle; branches approach each joint near its axis; pitch loop enters near an ear pivot; one controlled downstream roll loop; no slip ring for current ±55° yaw. Hollow-centre routing remains a comparison option. Measure restoring torque and endurance. | |
| Sourcing: availability, landed cost, lead time, substitute | Pending candidate-matrix expansion and re-check before purchase. Large Lazy-Susan/NEMA-scale hardware is excluded by moving-mass and 60 mm packaging constraints, not used as a sourcing reference. | |
| Fabrication/assembly/calibration/service story | Rising provisional-PLA U-yoke, removable face-attached rolling cosmetic ears with clearance around the pitch supports, independently replaceable actuators, accessible harness connectors, yaw-plane demateable mass boundary, display flashing access, axis-zero registration and complete-output calibration. Cosmetic seams stay integral; only required service splits are real. Detailed CAD waits for the CoM/axis convergence loop and PLA thermal/creep evidence. | |
| Failure/safe-rest behaviour (unpowered pose?) | Near-CoM axes reduce uncontrolled gravity fall; small preload/counterbalance may bias a safe direction. Stops and cable loops must bound the unpowered path. Final behaviour is a rig result. | |
| Verdict | **RP-01 path; advance Layout 03 detailing and rig screening. Not gate-selected.** Full note: [`elevated-ear-pivot-serial-gimbal.md`](elevated-ear-pivot-serial-gimbal.md). | **Waived; will not be authored for RP-01.** |

Sketches and per-concept notes as separate files in this folder.
