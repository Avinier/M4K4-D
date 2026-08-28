# RP-01 Rig — Fixture, Instrumentation, Safety

| Field | Value |
|---|---|
| Status | Not started (blocked on Stage 0 workbench readiness + selected concept) |
| Authority | `workbench.md` scored-test readiness gate; `risk-prototype-plan.md` RP-01 rig requirements |
| Physical baseline | `../../01-system/dimensional-baseline.md`; representative moving-head target ~250 g |

Requirements to satisfy (from the plan): rigid guarded bench fixture; adjustable ballast at representative head CoM; commanded + measured joint state on a monotonic clock; independent video with visible timing cue; safe physical stop; measure/derive joint angle, current, voltage, temperature, sound level at fixed position, structural deflection, camera image movement; cable behaviour across the workspace.

The fixture and ballast must represent the **100 H × 180 W × 130 D mm** complete head, **~250 g** moving-head target, actual candidate-axis offsets, and CAD-derived CoM/inertia as soon as available. The old 300–700 g head range is not an active rig requirement. Keep ballast adjustable for controlled sensitivity/overload checks, but record the nominal scored configuration explicitly. Microphones, speaker, battery, and primary electronics are body-mounted and are not part of nominal moving-head ballast.

Design notes, deliberately ugly: the rig is a decision instrument, not a mini droid. Every hour spent making it pretty is an hour not spent measuring.

## Fixture

The fixture must support the same mechanism with adjustable ballast at the A0/A1/A2 gimbal-centre points defined in `physics.md`. Changing ballast must not change the bearing/yoke stiffness being compared. Provide:

- a body-fixed yaw mount and a 60 mm neck/head-intrusion clearance proxy;
- rising-yoke/ear-pivot clearance proxies for Concept A;
- a rigid 50.0 mm output lever and dial-indicator access on every axis;
- a repeatable impact point and accelerometer/IMU mount for modal testing;
- interchangeable complete harnesses routed through the candidate hollow/open yaw centre and pitch/roll service loops;
- physical stops beyond usable travel and a safe low-energy/unpowered test path.

Backlash and modal frequency may share this fixture but are **different measurements**: quasi-static alternating output torque for reversal loss, then a separate impact/tap and commanded-ring-down test for structural modes.

## Instrumentation

- Commanded and measured joint position/current/voltage/temperature on the common monotonic timebase.
- Dial indicator or equivalent independent displacement instrument at the 50.0 mm output radius for the `storyboard.md` reversal method.
- Head-mounted accelerometer/IMU sampled fast enough to identify the 25–40 Hz target modes; use **≥400 Hz** for the modal test rather than a default 104 Hz convenience configuration.
- Body-frame IMU or rigid fixture attitude channel whenever chassis/body disturbance is introduced. The head IMU is not the body-heading reference.
- Independent video with a visible timing cue and, for combined reversals, an optical face-orientation marker.
- Inline rail current/voltage logging for peak and preregistered busy-minute RMS/thermal runs.
- Temperature sensors/readback on every actuator plus head electronics where fitted.
- Force gauge for cable restoring torque and the quasi-static output-load method.

Every instrument entry records sampling rate, calibration/check method, uncertainty and run-record channel name before scored use.

## Readiness checklist state

*(mirror of the workbench gate items for this rig; all must pass before any scored run)*
