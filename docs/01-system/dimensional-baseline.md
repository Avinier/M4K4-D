# Makad V1 Dimensional and Packaging Baseline

| Field | Value |
|---|---|
| Status | **Current target baseline — supersedes earlier dimensional and packaging assumptions** |
| Version | 1.10 |
| Owner | Project builder |
| Approved / revised | 2026-08-30 / 2026-09-12 |
| Feeds | Mass/envelope ledger, RP-01 head, RP-03 drive, RP-06 layout, sourcing, integrated CAD |

## Authority and interpretation

This document is the current source of truth for Makad's dimensional, drive-geometry, moving-head-load, and major component-placement targets. It overrides earlier working envelopes, ballast ranges, microphone counts/locations, speaker placement, and other planning values wherever they conflict.

- Dimensions are stated as **height × width × depth** unless a row labels its axes differently.
- `~` and stated ranges are design targets, not manufacturing tolerances.
- The final CAD must remain centred on the baseline values below. A conflict discovered during packaging or prototype validation is resolved by an explicit baseline revision, not by silently retaining an older value.
- The **110 mm wheelbase target** means drive-axle centreline to front-caster ground contact; it is not a second powered-axle spacing.
- The **140 mm body-top/neck datum** is measured from the ground. It is not the visible body-shell height.
- Longitudinal centre-of-mass coordinates use the drive axle as `x=0`, with positive `x` forward. CoM height is measured upward from the floor.

## Primary CAD baseline

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Overall Makad size | **300 H × 205 W × 180 D mm** | Keeps the 30 cm target while providing enough chassis depth for stable differential drive |
| Head size, including camera crown and side pods | **104 H × 150 W × 115 D mm — RP-01 Layout 03 planning envelope** | Current 1:1 packaging direction around selected display/camera/C2 envelopes; supersedes Layout 02's 102 mm height and the earlier 95 mm nominal / 90–100 mm band. Manufacturing tolerances and integrated fit remain open. |
| Head core, excluding crown and side pods | **86 H × 130 W × 115 D mm — RP-01 Layout 03** | Main core retained while the crown rises to 104 mm and the stern tapers to 104 mm width. See the [layout and validation boundaries](../02-prototypes/RP-01-head/cad/head/layout-03/README.md). |
| Body-top / neck datum | **140 mm above ground** | Main vertical mechanical reference |
| Neck allocation | **60 mm vertical** | Packaging space for powered yaw, pitch, and roll |
| Drive wheels | **Ø84 mm nominal** | Mobility, proportions, and motor-speed compromise |
| Wheel track | **~170 mm centre-to-centre** | Lateral stability and expressive turning |
| Drive axle to front-caster contact | **~105–115 mm; 110 mm target** | Avoids an excessively short/wide chassis and reduces caster instability |

The Layout 03 neutral stack is 140 mm ground-to-body-top + 60 mm neck allocation + 104 mm crown-inclusive head = **304 mm** if those datums are retained. The **300 mm overall height remains a rounded outer target, not a passed envelope**; RP-06 must explicitly accept the 304 mm stack or recover 4 mm through the actual body/neck mounting datums. The visible 35–45 mm neck is shorter because the mechanism intrudes into the body and head.

## Head and face

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Face/display active area | **95.04 W × 53.86 H mm nominal** | Fixed by the selected no-touch Waveshare ESP32-S3-LCD-4.3, SKU 30493 |
| Face optical aperture and bezel | **Layout 03: 99 W × 58 H mm opening, four 3 mm corner clips; 110 W × 64 H mm masked window** | Active pixels remain 95.04 × 53.86 mm. The revised flared camera aperture clears the conservative FOV envelope in sampled CAD checks; optical certification remains open. |
| Integrated cosmetic ear covers | **Layout 03: Ø60 mm, hollow; 150 mm complete width** | Ears attach to and roll with the face. Cosmetic shells carry their own loads; the separate pitch/yaw structure carries joint loads. |
| Head mass | **Nominal Layout 03 D/E tree: ~509 g complete at M008=20 g; M008 sensitivity gives ~499–524 g; measured total TBD** | The nominal tree includes two 23 g XC330-size servo references, not selected servos. Recalculate per candidate and replace with the M900 reading and measured per-axis tree. |
| Head inertia | **Layout 03 D/E: ~0.000656 / 0.000728 / 0.001080 kg·m² roll / pitch / yaw at nominal M008=20 g** | Candidate-screening input only; replace servo references per candidate and confirm from the as-built mass tree. The former generic ~0.001 proxy remains inadmissible. |
| Neck torque | **TBD per axis from the registered load and trajectories** | The former ~0.2 N·m estimate is historical only and must not select actuators |
| Neck axes | **Powered yaw + pitch + roll** | Full expressive head motion |
| Camera | **One central Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, SC0874; 25 W × 24 H × 12.4 D mm module envelope** | Selected 120° diagonal / approximately 102° horizontal FOV simplifies acquisition and gaze geometry; connector, mount and moving-link clearance remain RP-01/RP-06 validation items |

The moving head contains the selected display/renderer board, the required separate C2 ESP32-S3 motion controller, central camera, required brackets/structure, moving actuator and bearing portions, neck interfaces, and local wiring. **All installed items count in M900 and the per-axis mass tree.** Layout 03's ~509 g nominal result is a `D/E` calculation using M008=20 g and XC330-size servo references; it is not a target or accepted measurement. Keep M008 at `U` in the physical register and retain its 10/20/35 g analytical sensitivity until weighed. RP-01 has no runtime head IMU; its Nano/IMU bench instruments are excluded. The microphones, speaker, battery, main Linux SBC and other primary electronics are body-mounted and must not be added to RP-01 moving-head ballast unless the baseline is formally revised.

## Body, neck, and support geometry

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Visible body shell height | **~105–115 mm** | Distinct from the 140 mm ground-to-body-top datum |
| Visible body width | **~175–185 mm** | Visually narrower than the full wheel/body stance |
| Visible body depth | **~150–160 mm** | Compact appearance while the mechanical footprint extends farther |
| Visible neck height | **~35–45 mm** | Actuators overlap into the body and head instead of stacking externally |
| Overall width across wheel/body structure | **~195–205 mm** | Planted appearance and stability |
| Axle height | **~42 mm** | Half the nominal Ø84 mm wheel diameter |
| Front caster | **Ø25–32 mm; ~30 mm target** | Compact passive third support point |
| Main body-shell ground clearance | **~25–35 mm** | Closes the 140 mm datum minus the 105–115 mm visible shell height |
| Rear anti-tip skid reach | **~70 mm behind the drive axle** | Catches backward pitch caused by forward acceleration |
| Rear anti-tip skid height above floor | **≤14 mm at 70 mm reach** | Must hang below the shell; contact occurs before the CoM crosses the drive-wheel support line |

The skid is a separate lower protrusion, not flush with the main shell. For a different rearward reach `d`, its floor height `h` must satisfy **`h/d < x_CoM/h_CoM ≈ 25/124 ≈ 0.20`**. The nominal `d=70 mm` therefore requires `h≤14 mm`; the inequality must be recomputed if the measured integrated CoM changes.

## Drive targets

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Drive architecture | **Two independently powered wheels + front caster** | Forward/reverse motion, arcs, pivots, and in-place rotation |
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
| Longitudinal whole-robot CoM target | **`x_CoM = +25 mm` forward of drive axle** | Forward offset supplies the gravity restoring arm against backward tip during forward acceleration |
| Whole-robot CoM height target | **`h_CoM = 124 mm` above floor** | Baseline vertical lever arm for acceleration stability |
| Theoretical front-caster lift threshold | **~2.0 m/s² forward acceleration** | `a_tip = g·x_CoM/h_CoM ≈ 9.81·25/124 = 1.98 m/s²`; tipping governs before the ~6 m/s² traction estimate |
| CoM sensitivity | **Each +10 mm forward raises `a_tip` by ~0.8 m/s²** | `Δa_tip = g·10/124 ≈ 0.79 m/s²` at the target CoM height |

The existing **0.5 m/s maximum for person-following trials remains a behavioural safety/validation limit**. It does not conflict with the higher drivetrain capability target, which exists for bounded expressive moves and engineering headroom.

Until RP-03 measures lift onset and dynamic compliance, commanded forward acceleration must remain below the theoretical 2.0 m/s² caster-lift threshold with a registered safety margin. A higher expressive acceleration requires a validated forward CoM shift, lower CoM, or support-geometry revision; tire traction alone does not justify it.

## Component placement

| Subsystem | Baseline placement / count | Reason |
|---|---|---|
| Microphones | **Four PDM MEMS microphones in the body** | Wider stable array baseline and less neck-servo noise |
| Ear microphones | **None** | Ear pods remain free of acoustic/electronic function; concealed mechanical access is permitted as a candidate, not selected here |
| Speaker | **Body-mounted** | More acoustic cavity volume and less moving-head mass |
| Battery | **Low and forward of the drive axle** | Lowers `h_CoM` and increases the forward restoring arm `x_CoM`; behind-axle placement would reduce forward-acceleration tip resistance |
| Primary electronics | **Body-mounted main Linux SBC and power hardware; selected display ESP32-S3 plus one separate C2 ESP32-S3 motion controller move with the head** | Display and motion roles are physically separated on RP-01; every head-local board, connector, mount and harness segment counts in M900 |
| Rear skid | **Mandatory** | Protects sharp acceleration, braking, and turning cases |

## Compact handoff

Design around **300 H × 205 W × 180 D mm overall as a rounded target; RP-01 Layout 03 head 104 H × 150 W × 115 D mm including crown (86 mm main core); Ø84 mm wheels; 170 mm track; and 110 mm drive-axle-to-front-caster wheelbase**, with a **nominal ~509 g Layout 03 D/E head tree at M008=20 g and ~499–524 g C2 sensitivity before candidate-specific servo substitution**, **60 mm three-axis neck allocation**, whole-robot CoM targets initially at approximately **25 mm forward of the axle and 124 mm high but requiring revision under the heavier head**, a **~70 mm rear skid no more than 14 mm above the floor**, and body-mounted audio, forward-low battery, and main Linux compute. The neutral vertical stack is 304 mm; RP-06 must accept it or recover 4 mm. The CAD-volume/allowance tree is working evidence, not a measured replacement for M900.

## Change control

- RP-01 replaces the preliminary head inertia and torque estimates with CAD-derived mass properties and axis-specific calculations, then validates them with the representative rig.
- RP-03 validates traction, support geometry, stability, encoder control, speed, braking, caster behaviour, and the mandatory rear skid.
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
