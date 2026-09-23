# RP-06 integrated body/chassis Layout 02 — CAD brief

- Model: labeled whole-body assembly combining the RP-03 body/chassis with the live RP-01 head Layout 03 source.
- Task: resolve the first-pass body/chassis attachment, fascia, service-panel, audio-packaging and yaw-yoke appearance questions without changing the frozen drivetrain or head axes.
- Units: millimetres.
- Chassis frame: origin at ground on the drive-axle line and robot center plane; `+X` forward, `+Y` robot-left, `+Z` up.
- Head dependency: compose `RP-06-cad/head/layout-03/layout_model.py` directly. Do not redraw or substitute an AABB.
- Head transform: Layout 03 head origin `(37.9645, 0, 200)` in the chassis frame, making its yaw datum `(0, 0, 140)`.
- Drivetrain: 170 mm track, 42 mm loaded radius/axle height, frozen two-wheel Concept A, and a fixed non-interchangeable 1-inch ball-transfer module at `X=110`.
- External body: compact faceted shell, pale upper body, a physical removable lower mobility fascia, enlarged octagonal front/rear service panels that repeat the shell silhouette, and a functional front speaker grille. Visual references control cosmetics only.
- Structure: independent chassis rails, body posts and cross-members; four M4 body/chassis through-bolts and two locating pins; four M3 lower-fascia fasteners; front/rear internal panel frames with fused bosses and four M3 fasteners per panel; a separately selectable rear module made of a compact faceted skid/TCRT keel under the rear crossmember (replaceable shoe/guards, TCRT cartridge) and a parked (not assembled) cosmetic telescoping stinger tail accessory for the rear service panel; compact fixed ball-transfer load collar and keeper clips with concealed tactile fascia; and the head-yaw load path.
- Audio: provisional 50 mm speaker basket, 44 mm cone, 34 mm acoustic-cavity reservation, amplifier envelope, and four body-mounted PDM microphone boards/ports. Exact parts remain unselected.
- Neck/yoke treatment: stationary annular neck cowl plus head-yaw-moving bridge fairing and lower-leg shrouds. Yaw/pitch datums and motion allocation remain unchanged.
- Internal packaging: exact downloaded Raspberry Pi 5 STEP; exact downloaded 608ZZ STEP pair; documented envelopes for motor, ball transfer, battery, cooler, drivers, DevKitC, power/safety, sensors, and cables when exact STEP is unavailable.
- Transparency: shell and panels carry intrinsic alpha; CAD Viewer controls independently hide shell, head, electronics, harness, and physics. Free-standing dimension bars are not part of the assembly.
- Assembly labels: every serviceable/fabricated/purchased group is independently selectable.
- Outputs: `body-chassis.step.py`, generated sibling `body-chassis.step`, parameter sidecar, dimensions/frames/mass JSON+Markdown, and diagnostic snapshots.
- Validation: generation, refs/facts/planes/positioning, solid validation, key frame measurements, deterministic source checks, opaque and transparent multi-view snapshots, and CAD Viewer handoff.
- Status: packaging-quality Layout 02, not fabrication release or structural certification.

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
| Body/chassis attachment | Four M4 through-bolts + two 4 mm locating pins |
| Service-panel land | 2 mm constant-width overlap (inward offset of the panel outline); four M3 screws per panel |
| Service-panel lower edge | Front Z = 58 mm (clears chassis deck and crossmember); rear Z = 42 mm |
| Service-panel edge alignment | Front and rear panel straight side edges are parallel to their shell end-profile side edges |
| Lower mobility fascia | Physical removable shell; four M3 side screws |
| Speaker | 50 mm basket / 44 mm cone, centered at `(72, 0, 99)` mm |
| Microphones | Four provisional body PDM ports; front/rear left/right |
| Front range sensor | Face at `(84, 38, 68)` mm, beside the battery and below the speaker grille, behind its own panel window |
| Visible body-shell height | 110 mm |
| Neutral physical height stack | 304 mm; 300 mm remains a rounded target |
| Rear skid-pad ground clearance | 3.5 mm nominal |
| TCRT optical-face ground clearance | 10 mm nominal; must be calibrated on the target floor set |
| TCRT protective-guard bottom | 7 mm |
| TCRT channels | Rear only; CAD-context decision pending propagation |
| Rear skid-pad center | `(−43, 0, 4.75)` mm; replaceable shoe 12 × 10 × 2.5 mm |
| Rear TCRT center | `(−70, 0, 13.5)` mm |
| Rear TCRT contact lookahead | 27 mm behind skid contact |
| Rear tail construction | Slate root hub + three telescoping eight-sided segments sweeping up 23°→37°→52° + 66° chisel tip; tip at X = −121, Z = 123 mm |
| Rear tail footprint | Planar radius 121.9 mm, inside the 128 mm ball-nose spin circle; top 123.4 mm, below the 140 mm body top |
| Rear tail finish | Opaque ivory `#E3DDC9` segments, `#707D82` hub, `#B88636` tip; no visible fasteners |
| Rear tail status | Parked accessory; `REAR_TAIL_ENABLED = False` |
| Rear keel finish | Translucent ivory `#E3DDC9`, alpha 0.34; cartridge, cable riser and M3 hardware visible |
| Rear module assembly group | `REAR_SKID_TCRT_MODULE` = `REAR_SKID_TCRT_KEEL` (+ `REAR_TAIL_STINGER` when enabled) |
| Tactile nose fascia | 42 mm wide; 3 mm nominal travel reserve |

## Assumptions still requiring measured closure

- exact GM25-370 rear cap, pigtail, and mounting-face details;
- exact custom wheel/hub/tread geometry beyond the frozen 84 × 24 mm envelope;
- exact battery and body power-module geometries from RP-02;
- exact ICM-42688-P breakout and selected TCRT5000 breakout/comparator and connector bodies; the modeled carrier is an adjustable guarded requirement envelope;
- rear-only cliff sensing intentionally provides no dedicated forward or lateral coverage; level-floor operating restrictions and later propagation are tracked by `RP03-CAD-01`;
- the skid/TCRT functions live in a faceted keel under the rear crossmember and the visible tail is purely cosmetic (amending `RP03-CAD-03`); exact cartridge details remain provisional until the selected breakout and connector are measured, and the tail's heat-set insert engagement in the hub is unverified;
- the prior exposed full-width bumper is removed; the compact ball-nose contact fascia has central-contact coverage only, pending propagation under `RP03-CAD-02`;
- exact speaker, amplifier, PDM microphone and acoustic-mesh parts, plus acoustic testing and isolation details;
- fastener thread engagement, inserts, sealing/gasket detail, tolerances, material/process selection and structural proof;
- RP-01 Layout 03 yaw-yoke legs and trial adapter remain inherited appearance/packaging geometry; the Layout 02 cladding changes perceived length only, and actuator substitution, load rating and fabrication detail are not finalized here.
