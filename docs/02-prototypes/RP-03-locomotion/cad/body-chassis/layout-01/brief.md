# RP-03 integrated body/chassis Layout 01 — CAD brief

- Model: labeled whole-body assembly combining the RP-03 body/chassis with the live RP-01 head Layout 03 source.
- Task: replace the base-only envelope rig as the active CAD path.
- Units: millimetres.
- Chassis frame: origin at ground on the drive-axle line and robot center plane; `+X` forward, `+Y` robot-left, `+Z` up.
- Head dependency: compose `RP-01-head/cad/head/layout-03/layout_model.py` directly. Do not redraw or substitute an AABB.
- Head transform: Layout 03 head origin `(37.9645, 0, 200)` in the chassis frame, making its yaw datum `(0, 0, 140)`.
- Drivetrain: 170 mm track, 42 mm loaded radius/axle height, frozen two-wheel Concept A, and a fixed non-interchangeable 1-inch ball-transfer module at `X=110`.
- External body: compact faceted shell, pale upper body, dark lower mobility belt, front service/grille motif. Visual references control cosmetics only.
- Structure: independent chassis rails, body posts, cross-members, body/chassis mounts, a separately selectable eleven-station hollow faceted rear-tail module with visible internal load spine, replaceable shoe/guards and flush TCRT cartridge, compact fixed ball-transfer load collar and keeper clips with concealed tactile fascia, and head-yaw load path.
- Internal packaging: exact downloaded Raspberry Pi 5 STEP; exact downloaded 608ZZ STEP pair; documented envelopes for motor, ball transfer, battery, cooler, drivers, DevKitC, power/safety, sensors, and cables when exact STEP is unavailable.
- Transparency: shell and panels carry intrinsic alpha; CAD Viewer controls independently hide shell, head, electronics, harness, and physics. Free-standing dimension bars are not part of the assembly.
- Assembly labels: every serviceable/fabricated/purchased group is independently selectable.
- Outputs: `body-chassis.step.py`, generated sibling `body-chassis.step`, parameter sidecar, dimensions/frames/mass JSON+Markdown, and diagnostic snapshots.
- Validation: generation, refs/facts/planes/positioning, solid validation, key frame measurements, deterministic source checks, opaque and transparent multi-view snapshots, and CAD Viewer handoff.
- Status: packaging-quality Layout 01, not fabrication release or structural certification.

## Primary dimensions

| Parameter | Value |
|---|---:|
| Wheel track | 170 mm |
| Wheel OD / width | 84 / 24 mm |
| Axle height | 42 mm |
| Front ball contact | `(110, 0, 0)` mm |
| Body shell X range | −74 to +82 mm |
| Body shell Z range | 30 to 140 mm |
| Body width | 174 mm lower / 148 mm upper |
| Head-yaw body datum | `(0, 0, 140)` mm |
| Shell nominal thickness | 2.4 mm |
| Visible body-shell height | 110 mm |
| Neutral physical height stack | 304 mm; 300 mm remains a rounded target |
| Rear skid-pad ground clearance | 3.5 mm nominal |
| TCRT optical-face ground clearance | 10 mm nominal; must be calibrated on the target floor set |
| TCRT protective-guard bottom | 7 mm |
| TCRT channels | Rear only; CAD-context decision pending propagation |
| Rear TCRT center | `(−97, 0, 13.5)` mm |
| Rear TCRT contact lookahead | 27 mm behind skid contact |
| Rear tail construction | Eleven straight ruled stations; no spline; tighter rise and pointed tip at X = −118 mm |
| Rear tail visible finish | Translucent RP-01 Layout 03 ivory `#E3DDC9`, alpha 0.34 |
| Rear tail assembly group | `REAR_SKID_TCRT_MODULE`; hollow shell with visible spine, cartridge and cable path |
| Tactile nose fascia | 42 mm wide; 3 mm nominal travel reserve |

## Assumptions still requiring measured closure

- exact GM25-370 rear cap, pigtail, and mounting-face details;
- exact custom wheel/hub/tread geometry beyond the frozen 84 × 24 mm envelope;
- exact battery and body power-module geometries from RP-02;
- exact ICM-42688-P breakout and selected TCRT5000 breakout/comparator and connector bodies; the modeled carrier is an adjustable guarded requirement envelope;
- rear-only cliff sensing intentionally provides no dedicated forward or lateral coverage; level-floor operating restrictions and later propagation are tracked by `RP03-CAD-01`;
- the skid/TCRT packaging is consolidated into a separate hollow faceted-tail assembly under `RP03-CAD-03`; its eleven straight ruled links, translucent shell and visible internal spine/cartridge make packaging review possible, while exact cartridge details remain provisional until the selected breakout and connector are measured;
- the prior exposed full-width bumper is removed; the compact ball-nose contact fascia has central-contact coverage only, pending propagation under `RP03-CAD-02`;
- final body-shell split, fastening, tolerances, and fabrication process.
- RP-01 Layout 03 yaw-yoke legs and trial adapter remain inherited appearance/packaging geometry; actuator substitution, load rating and fabrication detail are not finalized here.
