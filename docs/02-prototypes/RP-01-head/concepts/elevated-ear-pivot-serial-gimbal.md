# RP-01 Concept A — Elevated Ear-Pivot Serial Gimbal

| Field | Value |
|---|---|
| Status | **Candidate — not selected; dimensions, actuators and axis placement remain open** |
| Authored | 2026-08-27 |
| Joint order | Body-fixed yaw → pitch → head-fixed roll |
| Physical baseline | ~95 H × 150 W × 115 D mm nominal complete head within a 90–100 H × 145–155 W × 110–120 D mm validation band; `../material-finish-mass-decision.md` provisional ~490 g at 1.2 mm PLA; 60 mm neck allocation |
| Feeds | `comparison.md`, `../physics.md`, `../gates.md`, `../rig.md`; later head blockout/CAD |

This note extracts only the credible topology from an unverified, generated-looking reference diagram. Its labels, scale, proportions, motor sizes and bearing sizes are not source data and must not enter CAD or the BOM.

## 1. Candidate topology

1. A **body-fixed yaw actuator** drives a compact yaw stage recessed into the body/head intrusion allowance.
2. A bearing or spaced-bearing shaft carries head weight and overturning moment independently of the yaw drive path.
3. A rising U-yoke terminates at two **double-supported pitch pivots** near ear-pod height.
4. The inner head cradle rolls about the face's forward axis. A roll axis intersecting, or nearly intersecting, the pitch axis near the measured head CoM is the gravity target, **not yet a credible support layout**; the bearing/shaft arrangement must first clear the display and camera and carry the overhung moment.
5. Ear pods remain microphone-free. Under this concept their removable cosmetic shells may hide pitch bearings and service access; the inner yoke/frame carries structural load.

This serial order means a roll remains a face-relative tilt after yaw and pitch. Firmware must still use rotation matrices/quaternions rather than add Euler angles, but the physical order matches Makad's authored semantic axes. Gimbal lock at pitch ±90° lies well beyond the proposed `-22°…+40°` best-case travel.

## 2. Axis-to-CoM definition and candidate sweep

For pitch, define `x` as the CoM's forward offset from the pitch axis and `z` as the CoM's upward offset from the pitch axis. The gravity term is

`τ_g,pitch = m·g·(x·cos θ + z·sin θ)`.

For roll, use the equivalent lateral and vertical CoM offsets about the face-forward axis. An axis below the CoM creates an inverted-pendulum term whose magnitude grows away from neutral. Therefore **pitch-axis height alone is not the design variable**: the pitch–roll gimbal centre must be located relative to the complete 3D CoM.

Evaluate at least these blockout candidates before detailed CAD:

| Candidate | CoM relative to pitch axis | Purpose |
|---|---:|---|
| A0 gravity-null | `x=0 mm`, `z=0 mm` | Minimum ideal gravity torque; exposes unloaded reversal behaviour |
| A1 light preload | `x=+5 mm`, `z=0 mm` | CoM slightly forward of axis, keeping a small same-sign pitch load across the usable range |
| A2 packaging compromise | `x=+5 mm`, `z=+10 mm` | Allows practical structure while bounding added holding torque |

These are calculation points, not tolerances. With the current `m=0.490 kg` provisional complete-head planning case, A1 produces approximately `0.0184–0.0240 N·m` simple pitch gravity torque across `-22°…+40°`. This is a sensitivity calculation only: pitch does not necessarily carry the complete head, and actuator sizing also requires the actual downstream inertia, speed, friction/cable terms and coupling.

Do not apply one mass blindly to all three axes. Register the actual moving set downstream of each joint: yaw carries the complete moving yaw output; pitch carries the pitch-and-roll output; roll carries only its cradle and payload. Until those as-built/CAD sets exist, show the `~490 g` provisional build-up and its row assumptions alongside every lighter downstream proxy so a favorable blockout cannot silently under-size an actuator.

Use an iterative convergence loop:

`component envelopes/masses → initial 3D CoM → candidate gimbal centre → yoke/bearings/actuators → revised CoM → final candidate sweep`.

The ear line is a useful industrial-design datum, not a substitute for this loop. Human head/neck motion is distributed across joints; anatomy does not specify Makad's pivot coordinate.

## 3. Preload and backlash hypothesis

A small persistent output load can keep a geartrain on one tooth flank and reduce unloaded chatter. Perfect gravity cancellation minimizes thermal load but does not prove reversal performance. Conversely, a large below-CoM offset creates continuous current, heat and droop in long expressive holds.

The candidate approach is:

- use a small forward CoM offset for same-sign pitch preload if the complete-output test shows a benefit;
- keep roll close to balance and add a low-rate torsion/elastic bias only if measured roll reversal needs it; any ordinary torsion spring must be pre-wound with its free angle outside usable travel so its torque does not cross zero in the workspace;
- compare the spring's angle-dependent holding current and thermal cost with constant-force/cam or other bias arrangements; do not assume a dead weight or magnetic detent is constant-torque in the assembled three-axis geometry;
- never claim that preload removes horn/spline slop, bracket compliance or structural modes;
- do not allocate the `≤0.25°` complete-output target as an unsupported `0.08° per serial stage` rule.

Measure each axis at the head output while the other axes are energized at representative poses. At a fixed command, sweep a specified reversing output load and record applied torque, independent external angle, servo-reported position, current and time. Report the load–position hysteresis and reversal delay, then dwell at representative holds and check external-angle/current peak-to-peak motion for hunting or limit cycling. Add a combined-motion orientation-error case because serial-axis errors map through the mechanism Jacobian rather than simply adding as three identical scalar lash values.

## 4. Actuator placement and yaw inertia

The pitch actuator moves with yaw. Its lateral placement contributes `m_actuator·r²` to yaw inertia. Record that term explicitly, but do not assume a belt/gear relocation is automatically better: the offset transmission adds its own mass, compliance, preload and reversal loss.

Start with direct pitch actuation as close to the yaw axis as the ear/yoke layout permits. Introduce a centred belt/gear drive only if the measured/derived yaw torque, packaging or service path rejects the direct layout.

## 5. Load path and scale exclusions

The reference diagram's NEMA-style motors, external spur reduction and Lazy-Susan-scale turntable are not Makad parts. A credible implementation uses compact shafts/bearings sized from the revised ~490 g planning build-up and later measured per-axis tree, and fits the 60 mm neck allocation through body/head intrusion.

Every candidate drawing must show:

- yaw axial and overturning load path;
- pitch support on both sides;
- roll support and drive reaction path;
- mechanical stops and unpowered path;
- actuator removal and bearing service without destroying the shell.

### Roll-support feasibility blocker

Before Concept A can be selected, a section through the face, selected no-touch Waveshare SKU 30493 module/connector envelope, camera, CoM and roll axis must compare at least:

- a compact rear coaxial bearing cartridge, recording the remaining overhung head moment even if two bearings are used;
- an annular/perimeter support that leaves the face opening clear, including its mass, diameter, cost and service path;
- a displaced/lowered roll axis, including the restored vertical CoM offset, gravity torque and thermal penalty.

“Double-supported” is not a substitute for this load-path proof: record bearing spacing, shaft/frame reactions, deflection at the display, and which structure actually closes the moment. The current 110–115 mm nominal head-core depth, selected approximately 106.1 × 67.8 mm module body, approximately 94–95 × 53–54 mm optical aperture and 110–115 × 60–65 mm bezel/window treatment are the controlling package, not dimensions from the generated reference.

The board fits, but width is tight: after nominal walls and clearance, only about 5–8 mm per side remains. Do not assume substantial side ribs or side-mounted hardware fit. Depth is the opposite problem; compare the current 110–115 mm core with an approximately 90 mm blockout because reduced depth lowers shell mass and pitch moment arm.

The front assembly must include an opaque rear mask across the full window width and a display flashing/service path. The shell/structure is provisional PLA for RP-01; cosmetic seams remain integral, while real splits are limited to service access. CAD must model 0.3–0.5 mm panel height offsets and the minimum feature sizes in `../material-finish-mass-decision.md` without weakening the yoke or monocoque load path.

## 6. Cable route

The mechanical concept is incomplete without a harness model. Apply the evidence and H1/H2/H3 candidates in `../../../01-system/head-harness-routing-study.md`:

- partition camera CSI, display/head-node, servo power/bus and local sensor/light branches instead of forcing one cable construction across every circuit;
- keep the yaw centre hollow/open, route each moving branch close to the yaw axis and give yaw a controlled loop/helical section;
- fix the downstream orientation at the yoke, approach pitch near an ear pivot and guide a predominantly single-plane rolling bend;
- fix orientation again before a deliberate short roll loop or purpose-designed torsion section;
- provide stationary- and moving-side strain relief plus service connectors only where access and signal integrity justify them;
- provide a demateable connector or defined separable cut plane at the yaw boundary so M020 and the complete moving M900 assembly can be weighed and serviced without cutting conductors;
- treat “one mechanical flex zone per degree of freedom” as the routing objective, but do not add passive connectors to the MIPI CSI path at every joint without lane-rate evidence;
- avoid a slip ring at the current bounded yaw range;
- measure angle-dependent cable restoring torque, connector motion and live-camera endurance for H1 continuous guided FPC, H2 active bridge/high-flex round link and H3 external diagnostic bypass.

Cable torque is part of the slow-expression and static-hold load, not merely an integration note. Clamp coordinates, free lengths, installed radii and connector-exit lengths are controlled configuration dimensions.

## 7. IMU roles

Do not use the head IMU as the only body-heading sensor.

| Location | Candidate responsibility |
|---|---|
| Head IMU | Actual face motion, settling, compliance/cable deflection, camera stabilization, pickup detection and RP-01 modal measurement |
| Body IMU | Chassis heading/attitude, caster/traction disturbance rejection, tip/pickup detection and locomotion control |

Joint encoders plus body attitude provide a kinematic head-pose estimate; the head IMU observes output motion that joint encoders cannot see after horns, brackets and compliant structure. Exact sensors and fusion remain RP-01/RP-02/RP-03 decisions.

## 8. Evidence required before selection

- sourced/weighed head blockout and revised 3D CoM/inertia;
- per-axis downstream moving-mass sets plus the current `~490 g` provisional complete-head build-up and all row assumptions;
- A0/A1/A2 torque, RMS/current and thermal comparison;
- complete-output loaded hysteresis and hold-hunting test per axis, plus a combined-motion orientation test;
- display-clear roll-support section and load-path comparison;
- impact/tap modal test and commanded ring-down test on the same fixture as, but distinct from, the loaded-hysteresis/hold-hunting test;
- measured cable restoring torque through the usable workspace;
- 60 mm neck/head-intrusion packaging proof;
- shell/frame/yoke/bearings/actuators mass roll-up;
- PLA structural temperature/creep evidence and a recorded PETG/ASA fallback if it fails;
- full-width window mask, display flashing access and yaw-plane connector/service proof;
- safe unpowered path and hard-stop/cable-clearance evidence.

Until these exist, Concept A is a credible proposal only.
