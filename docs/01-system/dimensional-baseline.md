# Makad V1 Dimensional and Packaging Baseline

| Field | Value |
|---|---|
| Status | **Current target baseline — supersedes earlier dimensional and packaging assumptions** |
| Version | 1.13 |
| Owner | Project builder |
| Approved / revised | 2026-08-30 / 2026-09-26 |
| Feeds | Mass/envelope ledger, RP-01 head, RP-03 drive, RP-06 layout, sourcing |

## Authority and interpretation

This document is the current source of truth for Makad's dimensional, drive-geometry, moving-head-load, and major component-placement targets. It overrides earlier working envelopes, ballast ranges, microphone counts/locations, speaker placement, and other planning values wherever they conflict.

- Dimensions are stated as **height × width × depth** unless a row labels its axes differently.
- `~` and stated ranges are design targets, not manufacturing tolerances.
- The final CAD must remain centred on the baseline values below. A conflict discovered during packaging or prototype validation is resolved by an explicit baseline revision, not by silently retaining an older value.
- The **110 mm wheelbase target** means drive-axle centreline to **front-support ground contact** (ball transfer); it is not a second powered-axle spacing.
- The **140 mm body-top/neck datum** is measured from the ground. It is not the visible body-shell height.
- Longitudinal centre-of-mass coordinates use the drive axle as `x=0`, with positive `x` forward. CoM height is measured upward from the floor.

## Primary CAD baseline

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Overall Makad size | **300 H × 205 W × 180 D mm** | Keeps the 30 cm target while providing enough chassis depth for stable differential drive |
| Head size, including camera crown and side pods | **104 H × 150 W × 115 D mm — RP-01 Layout 04 working envelope** | Current 1:1 packaging direction around selected display/camera/C2 envelopes. Manufacturing tolerances and integrated fit remain open. |
| Head core, excluding crown and side pods | **86 H × 130 W × 115 D mm — RP-01 Layout 04** | Main core retained while the crown rises to 104 mm and the stern tapers to 104 mm width. See the [layout and validation boundaries](../02-prototypes/RP-06-cad/head/layout-04/README.md). |
| Body-top / neck datum | **140 mm above ground** | Main vertical mechanical reference |
| Neck allocation | **49.5 mm vertical** | Layout 04 turntable neck; powered yaw, pitch, and roll remain |
| Drive wheels | **Ø84 mm nominal** | Mobility, proportions, and motor-speed compromise |
| Wheel track | **~170 mm centre-to-centre** | Lateral stability and expressive turning |
| Drive axle to front-support contact | **~105–115 mm; 110 mm target** | Avoids an excessively short/wide chassis; contact is the ball patch, not a caster fork |

The Layout 04 neutral stack is 140 mm ground-to-body-top + 49.5 mm neck allocation + 104 mm crown-inclusive head = **293.5 mm**. It clears the rounded 300 mm outer target in CAD by 6.5 mm; sourced-part fit and physical measurement remain open. The visible neck is shorter than its allocation because the mechanism intrudes into the body and head.

## Head and face

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Face/display active area | **95.04 W × 53.86 H mm nominal** | Fixed by the selected no-touch Waveshare ESP32-S3-LCD-4.3, SKU 30493 |
| Face optical aperture and bezel | **Layout 04: 99 W × 58 H mm opening, four 3 mm corner clips; 110 W × 64 H mm masked window** | Active pixels remain 95.04 × 53.86 mm. The revised flared camera aperture clears the conservative FOV envelope in sampled CAD checks; optical certification remains open. |
| Integrated cosmetic ear covers | **Layout 04: Ø60 mm, hollow; 150 mm complete width** | Ears attach to and roll with the face. Cosmetic shells carry their own loads; the separate pitch/yaw structure carries joint loads. |
| Head mass | **Layout 04 D/E yaw-carried tree: ~588 g; measured total TBD** | Working XC330-M181 yaw / XC330-M288 pitch and roll references and revised structure; replace with M900 and a measured per-axis tree. Layout 03's 499–524 g range is historical. |
| Head inertia | **Layout 04 D/E: ~0.000675 / 0.000779 / 0.001282 kg·m² roll / pitch / yaw** | Candidate-screening input only; confirm from the as-built mass tree and actual actuators. |
| Neck torque | **TBD per axis from the registered load and trajectories** | The former ~0.2 N·m estimate is historical only and must not select actuators |
| Neck axes | **Powered yaw + pitch + roll** | Full expressive head motion |
| Camera | **One central Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, SC0874; 25 W × 24 H × 12.4 D mm module envelope** | Selected 120° diagonal / approximately 102° horizontal FOV simplifies acquisition and gaze geometry; connector, mount and moving-link clearance remain RP-01/RP-06 validation items |

The moving head contains the selected display/renderer board, the required separate C2 ESP32-S3 motion controller, central camera, required brackets/structure, moving actuator and bearing portions, neck interfaces, and local wiring. **All installed items count in M900 and the per-axis mass tree.** Layout 04's ~588 g result is `D/E`, not an accepted measurement. Keep M008 at `U` in the physical register until weighed. RP-01 has no runtime head IMU; its Nano/IMU bench instruments are excluded. The microphones, speaker, battery, main Linux SBC and other primary electronics are body-mounted and must not be added to RP-01 moving-head ballast unless the baseline is formally revised.

## Body, neck, and support geometry

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Visible body shell height | **~105–115 mm** | Distinct from the 140 mm ground-to-body-top datum |
| Visible body width | **~175–185 mm** | Visually narrower than the full wheel/body stance |
| Visible body depth | **~150–160 mm** | Compact appearance while the mechanical footprint extends farther |
| Visible neck height | **~35–45 mm** | Actuators overlap into the body and head instead of stacking externally |
| Overall width across wheel/body structure | **~195–205 mm** | Planted appearance and stability |
| Axle height | **~42 mm** | Half the nominal Ø84 mm wheel diameter |
| Front support | **Ø1 inch (25.4 mm) ball transfer** | Compact passive third support; no trail. Ø25–32 mm swivel caster is the RP-03 **comparison swap only**, not the V1 target |
| Main body-shell ground clearance | **~25–35 mm** | Closes the 140 mm datum minus the 105–115 mm visible shell height |
| Rear anti-tip skid reach | **27 mm behind the drive axle in Layout 02** | Current CAD contact datum after `RP03-CAD-06`; physical lift-onset proof remains open |
| Rear anti-tip skid height above floor | **3.5 mm at 27 mm reach in Layout 02** | Must contact before the CoM crosses the drive-wheel support line; verify on the physical rig |

The skid is a separate lower protrusion, not flush with the main shell. Its floor height `h` and rearward reach `d` must satisfy **`h/d < x_CoM/h_CoM`** at the measured integrated CoM. The current CAD has `h/d = 3.5/27 ≈ 0.130`; its hand-kept 2,551.9 g register has `x_CoM/h_CoM = 19.46/107.27 ≈ 0.181`. The physical rig must verify the ordering. The older 70 mm / 14 mm pair is superseded.

## Drive targets

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Drive architecture | **Two independently powered wheels + front ball transfer** | Forward/reverse motion, arcs, pivots, and in-place rotation. Rear anti-tip skid remains mandatory |
| Drive encoders | **One per drive wheel** | Closed-loop speed and controlled turns |
| Acceptable drive-wheel range | **Ø80–85 mm** | Practical sourcing without redesign |
| Drive-wheel tread width | **~20–22 mm; 21 mm nominal** | Grip without excessive turn scrub |
| Tire type | **Moderate-grip rubber or TPU** | Traction with controlled differential-turn scrub |
| Normal travel speed | **~0.15–0.40 m/s** | Primary social/indoor range |
| Fast expressive speed | **~0.40–0.60 m/s** | Quick retreats, approaches, and energetic motions |
| Maximum target speed | **~0.65–0.70 m/s** | Swift without becoming RC-car-like |
| Required wheel speed | **~160 RPM at 0.70 m/s; design around 160–200 RPM unloaded** | Derived from the Ø84 mm wheel circumference |
| Normal / fast yaw rate | **~120–220°/s** | Convincing snap turns and expressive body motion |
| Maximum theoretical spin capability | **300°/s+ possible, drivetrain-dependent** | Headroom; not a normal commanded rate |
| Longitudinal whole-robot CoM | **Current Layout 02 register `x_CoM = +19.46 mm` (`E`); measured value TBD** | Includes the 81.6 g `RP03-CAD-08` ballast bar. The earlier +25 mm target is superseded by `RP03-CAD-09` for this layout |
| Whole-robot CoM height | **Current Layout 02 register `h_CoM = 107.27 mm` (`E`); measured value TBD** | The earlier 124 mm planning height is historical, not an accepted measurement |
| Forward-launch front-support lift screen | **`a_tip = g·x_CoM/h_CoM ≥ 1.582 m/s²` (`E` until weighed)** | `RP03-CAD-09` retains the physics margin encoded by the former +20 mm line at 124 mm. Current register gives about 1.78 m/s²; physical lift onset and head-pose corners remain open |
| CoM sensitivity | **Each +10 mm forward raises `a_tip` by ~0.91 m/s² at the current register height** | `Δa_tip = g·10/107.27 ≈ 0.91 m/s²`; recompute at measured height |

The existing **0.5 m/s maximum for person-following trials remains a behavioural safety/validation limit**. It does not conflict with the higher drivetrain capability target, which exists for bounded expressive moves and engineering headroom.

Until RP-03 measures lift onset and dynamic compliance, commanded forward acceleration must remain below the measured lift threshold with a registered safety margin; the current 1.78 m/s² value is a hand-kept estimate, not permission to raise the command limit. A higher expressive acceleration requires a validated forward CoM shift, lower CoM, or support-geometry revision; tire traction alone does not justify it. Battery-on-or-behind-axle (RP-03 `HIGH_AFT`) is a forbidden placement: `a_tip` changes sign. The older +25 / 124 mm and 1.98 m/s² figures remain planning history, not the accepted Layout 02 baseline.

## Component placement

| Subsystem | Baseline placement / count | Reason |
|---|---|---|
| Microphones | **Four PDM MEMS microphones in the body** | Wider stable array baseline and less neck-servo noise |
| Ear microphones | **None** | Ear pods remain free of acoustic/electronic function; concealed mechanical access is permitted as a candidate, not selected here |
| Speaker | **Body-mounted** | More acoustic cavity volume and less moving-head mass |
| Battery | **Low and forward of the drive axle** | Lowers `h_CoM` and increases the forward restoring arm `x_CoM`; behind-axle placement would reduce forward-acceleration tip resistance |
| Primary electronics | **Body-mounted Raspberry Pi 5 2 GB and power hardware; selected display ESP32-S3 plus one separate C2 ESP32-S3 motion controller move with the head** | Pi 5 selected under `RP02-P2-REG-02`; display and motion roles are physically separated on RP-01; every head-local board, connector, mount and harness segment counts in M900 |
| Rear skid | **Mandatory** | Protects sharp acceleration, braking, and turning cases |

## Compact handoff

Design around **300 H × 205 W × 180 D mm overall as a rounded target; RP-01 Layout 04 head 104 H × 150 W × 115 D mm including crown (86 mm main core); Ø84 mm wheels; 170 mm track; and 110 mm drive-axle-to-front-support (ball) wheelbase**, with a **~588 g Layout 04 D/E yaw-carried head tree**, **49.5 mm three-axis neck allocation**, the current hand-kept whole-robot CoM at **x +19.46 / h 107.27 mm** with the retained 81.6 g ballast bar, a **27 mm rear-skid reach at 3.5 mm height**, and body-mounted audio, forward-low battery, and main Linux compute. The neutral CAD stack is **293.5 mm**. These CAD/register values are working evidence, not measured replacements for M900 or the physical lift-onset gate.

## Change control

- RP-01 replaces the preliminary head inertia and torque estimates with CAD-derived mass properties and axis-specific calculations, then validates them with the representative rig.
- RP-03 validates traction, support geometry, stability, encoder control, speed, braking, ball-transfer behaviour (dent/jam/drag), the caster comparison swap, and the mandatory rear skid.
- RP-06 validates integrated packaging and visible proportions against sourced components.
- Any required departure is recorded here with a version increment and propagated to affected prototype inputs before CAD freeze.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-25 | 1.0 | Adopted the dimensional, moving-head, drive, and component-placement target set. |
| 2026-08-25 | 1.1 | Corrected battery placement to forward of axle; reconciled shell clearance to 25–35 mm; bounded the separate rear skid at ~70 mm reach and ≤14 mm height; added whole-robot CoM and forward-acceleration tip limits. |
| 2026-08-27 | 1.2 | Clarified that ear pods have no microphone/sensor role but may conceal removable pitch-bearing access in a mechanism candidate; structural loads must remain on an inner frame/yoke. No mechanism selected. |
| 2026-08-29 | 1.3 | Clarified the body-mounted-primary-electronics rule after the display study: any unavoidable display controller, head node, head IMU, connectors and mounts are permitted only as lightweight head electronics and count inside the unchanged ~250 g moving-head target. |
| 2026-08-29 | 1.4 | Propagated the 4.3-inch 800×480 IPS decision and distinguished the 60–65 mm visible opening from the approximately 68 mm hidden module-body clearance required by the first prototype candidate. |
| 2026-08-29 | 1.5 | Locked the face geometry to the selected no-touch Waveshare ESP32-S3-LCD-4.3, SKU 30493, while retaining physical-sample verification of the complete hidden envelope. |
| 2026-08-29 | 1.6 | Locked the central head-camera envelope to the visible-light Raspberry Pi Camera Module 3 Wide, order code SC0874; retained mount, installed mass and production moving-interconnect validation. |
| 2026-08-30 | 1.7 | Rebuilt the head envelope bottom-up from the selected 106.1 × 67.8 mm display and 25 × 24 × 12.4 mm camera. Replaced the 180 mm concept-art width with a 150 mm nominal complete width, reduced nominal depth to 115 mm, separated the optical aperture from bezel/window size, and required side pods to integrate rather than add width beyond the mechanical pivots. |
| 2026-09-02 | 1.8 | Rejected the obsolete 250 g head target and preliminary inertia/torque sizing inputs; adopted the ~490 g pre-M008 lower bound plus the selected separate C2 ESP32-S3 controller, and flagged whole-robot CoM/tip targets for recalculation under the heavier head. |
| 2026-09-08 | 1.9 | Builder approved the Layout 02 appearance revision and 1:1 component method. Recorded 86 mm main shell, 102 mm crown-inclusive height, 150 mm width, 115 mm depth, Ø60 mm rolling ears and 99 × 58 mm minimally clipped aperture. Explicitly replaces the earlier head-height/pod targets for RP-01 and exposes the 302 mm neutral stack; integrated fit and measured mass remain open. |
| 2026-09-12 | 1.10 | Adopted Layout 03 as the planning geometry: 104 × 150 × 115 mm complete head, 86 × 130 × 115 mm core and 304 mm provisional stack. Recorded the nominal 362/436/509 g and inertia tree at M008=20 g while retaining M008 uncertainty and candidate-specific servo recalculation. No fabrication release, measured-mass acceptance or gate pass. |
| 2026-09-17 | 1.11 | Consumed RP-03 `physics.md`: retained the +25 / 124 mm CoM **target** and the 1.98 m/s² figure as the value *at that target*; recorded that Layout 03 lumped roll-up does not automatically hit it (`a_tip` about 0.9–1.9 m/s² with battery forward; sign reversal if battery is on/behind the axle). No geometry target changed. No gate pass. |
| 2026-09-19 | 1.12 | Builder selected the **Ø1 inch ball transfer** as the V1 front support (`RP-03` BD-08). Wheelbase remains 110 mm to **front-support contact**. Swivel caster is the RP-03 comparison swap only. Not a gate pass, not a purchase, not ADR-04 closure. |
| 2026-09-26 | 1.13 | Propagated RP-06 head Layout 04 and `RP03-CAD-06/09`: 49.5 mm neck, 293.5 mm neutral CAD stack, ~588 g `D/E` head tree, 27 mm / 3.5 mm rear-skid contact, and the accepted `a_tip ≥ 1.582 m/s²` screen. The current 2,551.9 g hand-kept register includes the 81.6 g `RP03-CAD-08` bar; physical CoM and lift onset remain open. The +25 / 124 mm and 304 mm figures are historical planning values. |
