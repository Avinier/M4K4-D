# RP-07 geometry and calibration

| Field | Value |
|---|---|
| Status | Procedure complete on paper; all numeric calibration results `U` |

## 1. Required frames

```text
I: image pixels
C: optical camera frame
H: rigid head frame
N: neck/body reference frame
B: base frame
O: local odometry frame
```

Use the project-wide handedness and sign convention. Every transform record names parent/child frames, units, calibration revision and uncertainty.

The observation-time chain is:

```text
pixel → calibrated ray C
      → T_H_C
      → T_N_H(q_roll,q_pitch,q_yaw at capture)
      → T_B_N
      → optional T_O_B(base pose at capture)
```

Full rotation and translation are required. Rotation-only treatment is inadmissible at close range.

## 2. Calibration artefacts

| ID | Artefact | Method | Physical evidence required |
|---|---|---|---|
| `CAL-01` | Intrinsics/distortion for each used mode/crop | Printed target across central/peripheral FOV | Images, target dimensions, reprojection residuals |
| `CAL-02` | Camera-to-head rigid transform | CAD prior plus measured target/fixture solve | Fixture record, transform and covariance |
| `CAL-03` | Head joint zeros/axes and head-to-body transform | RP-01 calibration plus surveyed camera target | Joint logs and external measurement |
| `CAL-04` | Camera↔joint timestamp mapping | Repeated visible/electrical motion event | ≥100 samples, offset, P95 residual, outliers |
| `CAL-05` | Rolling-shutter/readout model | Stationary calibrated target during known head rates | Error versus row/rate/exposure |
| `CAL-06` | Base yaw/odometry alignment | Marked floor heading and controlled turns | Encoder/IMU/external heading comparison |
| `CAL-07` | Range-cue calibration | Marked person/target distances and poses | Error/bias by cue, range and visibility |

Any relevant mechanical, focus, sensor mode, crop, mount, joint-zero, firmware or camera replacement invalidates the affected calibration.

## 3. Effective capture time

Carry `SensorTimestamp`, exposure time and frame duration. The implementation must document whether its effective time refers to start, midpoint or another modeled instant and how rolling-shutter row time affects the chosen anchor.

For observed angular rate `ω`, the inherited alignment condition remains:

```text
|Δt|95 × |ω| ≤ 0.3°
```

When that cannot be met, widen bearing uncertainty or exclude the motion interval from high-accuracy tracking. Do not silently reuse the settled-head uncertainty.

## 4. Bearing

Undistort the selected anchor, form a unit camera ray and transform it with measured head/base pose at effective capture time. The output includes angle and uncertainty. Raw box centre never directly becomes a servo command.

Anchor preference:

1. calibrated eye-region/face landmark anchor;
2. calibrated face-box fallback;
3. stable upper-body/head estimate;
4. person-box control point for follow geometry only.

Transitions use hysteresis so intermittent face evidence does not create gaze jumps.

## 5. Range cues

| ID | Cue | Valid when | Known failure |
|---|---|---|---|
| `RC-01` | Ground-plane ray through foot/lower-body contact | Ground and lower body visible; calibrated pitch/height | Occlusion, crop, non-level floor, wrong foot point |
| `RC-02` | Visible-joint/known-height prior | Required joints visible and target-specific or population prior accepted | Pose error and human-size variation |
| `RC-03` | Selected-person apparent width/scale | Clean selection samples exist; torso/shoulders visible | Pose, clothing, yaw and arm variation |
| `RC-04` | Temporal size/radial trend | Track stable over time | Gives change more reliably than absolute range |
| `RC-05` | Non-safety external range association | Future sensor ray can be associated without ambiguity | Range may hit another object/person |

Use cue availability and quality to fuse a coarse estimate. `range_sigma_m` must grow when cues disagree, visibility degrades, calibration is stale, or the person is near an image edge.

## 6. Control eligibility

| Geometry state | Head attention | Base alignment | Forward come/follow |
|---|---|---|---|
| Fresh bearing, no range | Allowed within uncertainty | Allowed if C3 safe | Forbidden |
| Fresh bearing + valid coarse range | Allowed | Allowed | Eligible within registered uncertainty |
| Prediction inside brief gap | Bounded/slow; uncertainty grows | No new acceleration | No forward motion after freshness boundary |
| Stale pose or calibration | Inhibit | Inhibit | Inhibit |

## 7. Validation outputs

Report bearing and range error by distance, FOV sector, person pose, head pose/rate, base motion, lighting, anchor/cue, and occlusion. Summary percentiles without those strata are insufficient for selection.

