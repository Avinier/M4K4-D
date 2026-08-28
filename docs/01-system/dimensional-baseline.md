# Makad V1 Dimensional and Packaging Baseline

| Field | Value |
|---|---|
| Status | **Current target baseline — supersedes earlier dimensional and packaging assumptions** |
| Version | 1.2 |
| Owner | Project builder |
| Approved | 2026-08-27 |
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
| Head size, including ears | **100 H × 180 W × 130 D mm** | Expressive without making the robot excessively top-heavy |
| Head core, excluding ears | **~100 H × 140–145 W × 125–130 D mm** | Packages the display, camera, brackets, and neck intrusion |
| Body-top / neck datum | **140 mm above ground** | Main vertical mechanical reference |
| Neck allocation | **60 mm vertical** | Packaging space for powered yaw, pitch, and roll |
| Drive wheels | **Ø84 mm nominal** | Mobility, proportions, and motor-speed compromise |
| Wheel track | **~170 mm centre-to-centre** | Lateral stability and expressive turning |
| Drive axle to front-caster contact | **~105–115 mm; 110 mm target** | Avoids an excessively short/wide chassis and reduces caster instability |

The baseline stack is geometrically consistent: the 140 mm ground-to-body-top datum, 60 mm neck allocation, and 100 mm head height produce the 300 mm overall-height target. The visible 35–45 mm neck is shorter because the mechanism intrudes into the body and head.

## Head and face

| Part / parameter | Final / target dimension | Design intent |
|---|---:|---|
| Face/display active area | **~95 W × 54 H mm** | Fits a common ~4.3-inch 16:9 display |
| Face opening / bezel | **~110–120 W × 60–65 H mm** | Leaves border and mounting room around the display |
| Ear pods | **~55–65 mm diameter; ~17–20 mm side protrusion each** | Exterior visual elements with no microphones/sensors; a mechanism candidate may use their internal volume for removable pitch-bearing covers, but only an inner frame/yoke may carry structural load |
| Head mass | **~250 g target** | Controls neck loads and whole-robot centre of mass |
| Preliminary head inertia | **~0.001 kg·m²** | Starting value for RP-01 neck-actuator calculations |
| Preliminary neck peak torque | **~0.2 N·m** | Early actuator-sizing estimate; CAD mass properties and RP-01 calculations determine the final value |
| Neck axes | **Powered yaw + pitch + roll** | Full expressive head motion |
| Camera | **One central head camera** | Simplifies gaze geometry |

The moving head contains the display, central camera, required brackets/structure, neck interfaces, and local wiring. The microphones, speaker, battery, and primary electronics are body-mounted and must not be added to RP-01 moving-head ballast unless the baseline is formally revised.

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
| Primary electronics | **Body-mounted** | Keeps the head light and centralizes power/control hardware |
| Rear skid | **Mandatory** | Protects sharp acceleration, braking, and turning cases |

## Compact handoff

Design around **300 H × 205 W × 180 D mm overall; 100 H × 180 W × 130 D mm head; Ø84 mm wheels; 170 mm track; and 110 mm drive-axle-to-front-caster wheelbase**, with a **~250 g moving head**, **60 mm three-axis neck allocation**, whole-robot CoM at approximately **25 mm forward of the axle and 124 mm high**, a **~70 mm rear skid no more than 14 mm above the floor**, and body-mounted audio, forward-low battery, and primary electronics.

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
