# RP-03 CAD decisions

Recorded: **2026-09-20**. Scope: active body/chassis CAD iteration only.

This is the CAD-local decision register, following the RP-01 head CAD pattern. A
choice marked **fixed in CAD context** governs the active model and its generated
checks, but is not yet a permanent RP-03 architecture decision. Once the body and
chassis CAD is accepted, each retained choice must be propagated deliberately to
`decision.md`, `research.md`, operating constraints, controls and test documents.

## Decision register

| ID | Status | Choice |
|---|---|---|
| `RP03-CAD-01` | **Fixed in CAD context — pending permanent propagation** | Reduce the ground-reflectance architecture from three TCRT5000 channels to one guarded rear channel. Remove the front and lateral TCRT packages, mounts, booms and cable reserves from Layout 01. |

## RP03-CAD-01 — Rear-only ground-reflectance channel

M4's current intended work environment is a continuous, level indoor floor. Broad
cliff/edge detection is not a primary work function for this MVP, and three exposed
low-clearance sensor carriers add packaging, wiring, calibration and snag complexity.
The active CAD therefore retains only the rear look-down channel, where chassis
motion is least observable by the forward/head camera.

The retained rear channel remains on the skid-side carrier with its optical face
nominally 5 mm above the floor, sacrificial rails beginning at 2.5 mm, and its sample
patch 40 mm behind the nominal skid contact. The selected breakout/comparator PCB,
connector, actual adjustment range and calibrated threshold remain open.

This choice intentionally removes any CAD or safety claim for dedicated forward or
lateral cliff detection. Camera perception may provide forward warning but is not
treated here as an independent low-level stop channel. Until permanent propagation
and testing, the implied operating constraints are:

- continuous, level indoor floors only;
- no autonomous operation near open stairs, platforms or loading edges;
- reverse travel kept slow and bounded;
- an unknown or failed rear-floor reading inhibits reverse motion;
- no claim of cliff protection during forward travel or pivoting.

Revisit this decision if M4's operating environment includes unguarded drops, if
unrestricted pivoting near edges becomes required, or if tests show the rear TCRT is
unreliable on the target dark/glossy floor set.

## Propagation hold

Do not edit the permanent RP-03 documents merely because this geometry now exists.
When Layout 01 is accepted, propagate the retained choice and its consequences as one
reviewed change set: sensor/BOM count, GPIO allocation, electrical stop path, motion
restrictions, receiving/calibration tests and safety claims.
