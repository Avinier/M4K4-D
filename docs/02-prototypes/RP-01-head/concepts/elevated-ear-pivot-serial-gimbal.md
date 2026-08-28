# RP-01 Concept A — Elevated Ear-Pivot Serial Gimbal

| Field | Value |
|---|---|
| Status | **Candidate — not selected; dimensions, actuators and axis placement remain open** |
| Authored | 2026-08-27 |
| Joint order | Body-fixed yaw → pitch → head-fixed roll |
| Physical baseline | 100 H × 180 W × 130 D mm complete head; ~250 g moving-head target; 60 mm neck allocation |
| Feeds | `comparison.md`, `../physics.md`, `../gates.md`, `../rig.md`; later head blockout/CAD |

This note extracts only the credible topology from an unverified, generated-looking reference diagram. Its labels, scale, proportions, motor sizes and bearing sizes are not source data and must not enter CAD or the BOM.

## 1. Candidate topology

1. A **body-fixed yaw actuator** drives a compact yaw stage recessed into the body/head intrusion allowance.
2. A bearing or spaced-bearing shaft carries head weight and overturning moment independently of the yaw drive path.
3. A rising U-yoke terminates at two **double-supported pitch pivots** near ear-pod height.
4. The inner head cradle rolls about the face's forward axis. The roll axis is head-fixed and intersects, or nearly intersects, the pitch axis near the measured head CoM.
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

These are calculation points, not tolerances. With the earlier `m=0.193 kg` subassembly proxy, A1 produces only about `0.007–0.009 N·m` pitch gravity torque across `-22°…+40°`; the value must be recomputed from the actual mass blockout.

Use an iterative convergence loop:

`component envelopes/masses → initial 3D CoM → candidate gimbal centre → yoke/bearings/actuators → revised CoM → final candidate sweep`.

The ear line is a useful industrial-design datum, not a substitute for this loop. Human head/neck motion is distributed across joints; anatomy does not specify Makad's pivot coordinate.

## 3. Preload and backlash hypothesis

A small persistent output load can keep a geartrain on one tooth flank and reduce unloaded chatter. Perfect gravity cancellation minimizes thermal load but does not prove reversal performance. Conversely, a large below-CoM offset creates continuous current, heat and droop in long expressive holds.

The candidate approach is:

- use a small forward CoM offset for same-sign pitch preload if the complete-output test shows a benefit;
- keep roll close to balance and add a low-rate torsion/elastic bias only if measured roll reversal needs it;
- never claim that preload removes horn/spline slop, bracket compliance or structural modes;
- do not allocate the `≤0.25°` complete-output target as an unsupported `0.08° per serial stage` rule.

Measure each axis at the head output while the other axes are energized at representative poses. Add a combined-motion orientation-error case because serial-axis errors map through the mechanism Jacobian rather than simply adding as three identical scalar lash values.

## 4. Actuator placement and yaw inertia

The pitch actuator moves with yaw. Its lateral placement contributes `m_actuator·r²` to yaw inertia. Record that term explicitly, but do not assume a belt/gear relocation is automatically better: the offset transmission adds its own mass, compliance, preload and reversal loss.

Start with direct pitch actuation as close to the yaw axis as the ear/yoke layout permits. Introduce a centred belt/gear drive only if the measured/derived yaw torque, packaging or service path rejects the direct layout.

## 5. Load path and scale exclusions

The reference diagram's NEMA-style motors, external spur reduction and Lazy-Susan-scale turntable are not Makad parts. A credible implementation uses compact shafts/bearings sized for a ~250 g moving head and fits the 60 mm neck allocation through body/head intrusion.

Every candidate drawing must show:

- yaw axial and overturning load path;
- pitch support on both sides;
- roll support and drive reaction path;
- mechanical stops and unpowered path;
- actuator removal and bearing service without destroying the shell.

## 6. Cable route

The mechanical concept is incomplete without a harness model:

- keep the yaw centre hollow/open and route the bundle close to the yaw axis;
- approach pitch through the yoke and enter near an ear pivot;
- provide one deliberate downstream service loop for roll;
- provide stationary- and moving-side strain relief plus service connectors;
- avoid a slip ring at the current bounded yaw range;
- measure angle-dependent cable restoring torque, connector motion and endurance for both candidate camera-link architectures.

Cable torque is part of the slow-expression and static-hold load, not merely an integration note.

## 7. IMU roles

Do not use the head IMU as the only body-heading sensor.

| Location | Candidate responsibility |
|---|---|
| Head IMU | Actual face motion, settling, compliance/cable deflection, camera stabilization, pickup detection and RP-01 modal measurement |
| Body IMU | Chassis heading/attitude, caster/traction disturbance rejection, tip/pickup detection and locomotion control |

Joint encoders plus body attitude provide a kinematic head-pose estimate; the head IMU observes output motion that joint encoders cannot see after horns, brackets and compliant structure. Exact sensors and fusion remain RP-01/RP-02/RP-03 decisions.

## 8. Evidence required before selection

- sourced/weighed head blockout and revised 3D CoM/inertia;
- A0/A1/A2 torque, RMS/current and thermal comparison;
- complete-output reversal test per axis and a combined-motion orientation test;
- impact/tap modal test and commanded ring-down test on the same fixture as, but distinct from, the backlash test;
- measured cable restoring torque through the usable workspace;
- 60 mm neck/head-intrusion packaging proof;
- shell/frame/yoke/bearings/actuators mass roll-up;
- safe unpowered path and hard-stop/cable-clearance evidence.

Until these exist, Concept A is a credible proposal only.
