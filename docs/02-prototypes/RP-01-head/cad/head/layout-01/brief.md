# Layout 01 — component packaging study

Status: **proposed study geometry; not fabrication CAD or an approved fit**.

Develop the selected A0, rolling-ear, direct-coaxial architecture into a reviewable arrangement. Retain the main 130 W × 95 H × 115 D mm body and 150 mm neutral width including cosmetic ears. Trial a local trapezoidal crown up to Z=109 mm, 58 mm wide at its base and 38 mm at its top. Crown depth starts at 24 mm. These are proposed dimensions, not new locked requirements.

Units are mm. Origin is the centre of the front bottom edge of the main head. +X is forward, +Y robot-left, +Z up. Main front plane X=0; rear plane X=−115; main side planes Y=±65; bottom Z=0. Use labelled closed solids for purchased components, reserved spaces and indicative supporting members. Reservation solids do not imply material or mass. Simplified skins and supports are packaging boundaries, with no fabrication hole patterns or bearing fits implied.

Place the display at Z=9…77 using a conservative 106.1 × 68 mm union envelope for the selected non-touch board/glass. Reserve 18 mm total front stack including window, display and rear projections. Place the 25 × 24 mm camera board above it with at least 4 mm separation. Import the exact wide-camera model and manufacturer X330 geometry after inspecting their coordinate frames. Keep exact-model placement separate from connector/service reserves.

Reserve a removable 35 W × 25 H × 15 D mm C2 pocket behind the display, offset laterally to clear the spindle. C2 remains unselected; this is an available volume, not a verified board fit. The rolling backplate feeds an independent rear spindle, two bearing locations 22 mm apart, a short coupling, and a pitch-frame-mounted X330 reference servo. Reserve a side pocket for the yaw-yoke-mounted pitch servo. Neither servo is selected for purchase by this study.

Derive provisional A0 coordinates from an explicit spatial allocation of the existing mass rows, replacing the old 35 g actuator allowance and making unknown controller mass explicit. Separate yaw-only, pitch-carried and roll-carried membership. Sensitivity values are assumptions, not weighed masses. Do not claim a final inertia, torque or servo pass from this packaging work.

Check front/crown dimensions, longitudinal stack, component overlap and representative roll/pitch sweeps. Inspect hidden side/bottom openings required by the stationary support frame. If the rolling shell/support arrangement has unresolved interference, report it prominently and retain a proposed relief envelope; do not silently reduce motion or change ear attachment. Exact bend radii, optical pupil/aperture clearance, powered thermal behaviour and structural performance remain later checks.

Outputs in this folder: `head-layout.step.py` and sibling STEP; imported reference parts with source provenance; reproducible spatial/mass analysis; a findings report; CAD front/side/isometric/section snapshots. Validate named solids and positions using CAD inspection; review primary CAD snapshots and provide CAD Viewer links.
