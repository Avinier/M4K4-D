# RP-01 Rig — Fixture, Instrumentation, Safety

| Field | Value |
|---|---|
| Status | Not started (blocked on Stage 0 workbench readiness + selected concept) |
| Authority | `workbench.md` scored-test readiness gate; `risk-prototype-plan.md` RP-01 rig requirements |
| Physical baseline | `material-finish-mass-decision.md`; representative planning load is ~490 g at 1.2 mm PLA **plus selected M008 C2 hardware**, pending exact module selection and the measured per-axis mass tree |

Requirements to satisfy (from the plan): rigid guarded bench fixture; adjustable ballast at representative head CoM; commanded + measured joint state on a monotonic clock; independent video with visible timing cue; safe physical stop; measure/derive joint angle, current, voltage, temperature, sound level at fixed position, structural deflection, camera image movement; cable behaviour across the workspace.

The fixture and ballast must represent the approximately **95 H × 150 W × 115 D mm nominal** complete head, validated within **90–100 H × 145–155 W × 110–120 D mm**, the current **~490 g `E` planning lower bound at 1.2 mm PLA** (approximately 472 g at 1.0 mm) **plus M008 C2 controller hardware**, selected no-touch Waveshare SKU 30493 display envelope/mass, selected visible-light Raspberry Pi Camera Module 3 Wide SC0874 envelope/mass, actual candidate-axis offsets, and CAD-derived CoM/inertia as soon as available. The 250 g system target is historical and must not be the representative scored ballast. Keep ballast adjustable for controlled sensitivity/overload checks, but record the nominal scored configuration explicitly and replace the planning load with the registered `W`/CAD per-axis tree when available. Microphones, speaker, battery and primary body electronics are not part of nominal moving-head ballast.

Design notes, deliberately ugly: the rig is a decision instrument, not a mini droid. Every hour spent making it pretty is an hour not spent measuring.

## Fixture

The fixture must support the same mechanism with adjustable ballast at the A0/A1/A2 gimbal-centre points defined in `physics.md`. Changing ballast must not change the bearing/yoke stiffness being compared. Provide:

- a body-fixed yaw mount and a 60 mm neck/head-intrusion clearance proxy;
- rising-yoke/ear-pivot clearance proxies for Concept A;
- a fixed **106.1 × 67.8 mm** selected-display volume/connector proxy for Waveshare no-touch SKU 30493, plus interchangeable roll-support inserts for a rear spaced-bearing cartridge, annular/perimeter support and displaced-axis comparison;
- a fixed **25 × 24 × 12.4 mm** camera/lens/connector proxy for selected visible-light Camera Module 3 Wide SC0874, positioned centrally with status-light and display-reflection clearances;
- an interchangeable depth blockout that directly compares the current 110–115 mm core depth against an approximately 90 mm alternative without changing the front display/camera datum;
- a demateable harness connector or defined separable cut plane at the physical yaw boundary so M020 and the complete M900 assembly can be weighed without cutting conductors;
- a rigid 50.0 mm output lever and dial-indicator access on every axis;
- a repeatable impact point and accelerometer/IMU mount for modal testing;
- interchangeable H1/H2/H3 complete harnesses from `../../01-system/head-harness-routing-study.md`, with adjustable but recordable yaw/pitch/roll guides, clamp coordinates, free lengths and connector-exit strain relief; the fixture must support separate controlled flex zones without requiring passive CSI connectors at every joint;
- physical stops beyond usable travel and a safe low-energy/unpowered test path.

Loaded reversal hysteresis and modal frequency may share this fixture but are **different measurements**: fixed-command quasi-static alternating output torque plus hold dwells for hysteresis/hunting, then a separate impact/tap and commanded-ring-down test for structural modes.

## Instrumentation

- Commanded and servo-reported joint position/current/voltage/temperature on the common monotonic timebase, synchronized with applied load and independent external angle.
- Dial indicator or equivalent independent displacement instrument at the 50.0 mm output radius for the `storyboard.md` reversal method.
- A **temporary bench-mounted** accelerometer/IMU sampled fast enough to identify the 25–40 Hz target modes; use **≥400 Hz** for the modal test rather than a default 104 Hz convenience configuration. Remove it after the measurement; it is not runtime head hardware.
- Servo encoders are the runtime RP-01 joint-angle source. Use a bench IMU/accelerometer only when it is useful for modal or backlash evidence, and record its fixture/head frame. When chassis/body disturbance is introduced later, use a base-frame IMU or rigid fixture attitude channel rather than mounting an IMU in the head.
- Independent video with a visible timing cue and, for combined reversals, an optical face-orientation marker.
- Inline rail current/voltage logging for peak and preregistered busy-minute RMS/thermal runs.
- Temperature sensors/readback on every actuator plus head electronics where fitted.
- Bidirectional force gauge for cable restoring torque and the quasi-static output-load method; record both load-sweep directions at matched force/torque points.
- Live selected-camera monitor logging frame sequence/timestamps, gaps/drops, capture/driver errors, visible corruption and device reset/re-enumeration where applicable while the harness moves; static continuity alone is insufficient.
- A calibrated 0.1 g-resolution scale with at least 1 kg capacity for the current mass model, checked near 10, 100 and 200 g according to `payload-mass-capture.md`.
- Temperature measurement inside the sealed-head proxy, at M010–M012 structural load paths and at every installed actuator/display heat source during sustained holds and busy-minute runs.
- Independent structural-deflection measurement for the provisional PLA creep dwell; log load, pose, time, temperature and residual deformation after unload.

Every instrument entry records sampling rate, calibration/check method, uncertainty and run-record channel name before scored use.

## Material and finish coupons

Before coating the head shell, print a **60 × 60 mm PLA finish coupon** with representative panel lines and three fastener wells. Weigh it bare, run the exact nine-step finish system in `material-finish-mass-decision.md`, allow at least 24 hours cure, then reweigh it. Record coating mass per unit area and a visual `PASS/ITERATE` judgement for texture scale, chipping and wash retention.

PLA structure remains provisional. Use representative M010–M012 coupons or the actual load path to run a preregistered sustained-load dwell at the worst credible parked pitch/roll condition and the measured sealed-head operating temperature. Register dwell duration, load/moment, allowable in-dwell deflection and residual deformation before inspecting results. A failure triggers a PETG or ASA structural reprint path; it does not silently change the skin material or the scored load.

## Readiness checklist state

*(mirror of the workbench gate items for this rig; all must pass before any scored run)*
