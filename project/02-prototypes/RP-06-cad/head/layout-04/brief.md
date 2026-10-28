# Layout 04 construction brief

Revision of Layout 03 source, preserved in its own directory. Millimetres; origin front/bottom centre, +X face, +Y left, +Z up. Helmet, face, ears, C2 tray, camera, display, roll drive and pitch frame are unchanged Layout 03 geometry. Same text-to-cad 0.4.28 runtime and explicit R/P/Y transforms.

## Why Layout 04

In the integrated RP-06 body, Layout 03's 60 mm neck read as an over-long U-yoke. The body/chassis Layout 02 cowl and yaw-moving shrouds only filled that gap, and the result looked worse. A sweep of the Layout 03 head over the 56-pose roll × pitch grid split the 60 mm into three bands:

| Band (head Z) | Height | Driver |
|---|---:|---|
| −60…−36 | 24 mm | vertical yaw spindle and external yaw loop; no motion requirement |
| −36…−32 | 4 mm | bridge plate |
| −32…0 | 32 mm | combined roll/pitch sweep: worst −26.4 at roll ±18 / pitch −22 (rear-cover corner) |

Pure-axis sweeps are only 16.3 mm (pitch −22) and 13.8 mm (roll ±18). The combined corner case alone sets the leg length.

## Decision: turntable yaw stage at a 49.5 mm neck (rev D)

Rev A reached 21 mm with a firmware roll/pitch envelope but gave up full combined motion, the mechanical head/body guarantee and Pi 5 cooler airflow. Revs B (40 mm) and C (58 mm) kept those, but two RP-01 conflicts then surfaced: stops placed exactly at usable travel, and a 4.875:1 ring-gear yaw drive that no XC330 can run at peak yaw speed. Rev D fixes both:

- **Hard stops** sit 3° beyond usable travel: roll ±21, pitch −25/+43.
- **Clearance rule:** at least 4 mm at the stops and at least 2 mm with a further 1° of overtravel. The full stop-grid sweep is Z −30.3 (−31.5 with overtravel), so the disc top sits at **Z −34.5** (4.3 / 3.1 mm clear).
- **Cooler rule:** body/chassis Layout 02's 10.5 mm of air above the Pi 5 cooler. The RP-06 stack of plate 4 + bearing 7 + clamp 1 + 1:1 spur pair 5 puts the disc top 15 mm above the body top, so the body top is **Z −49.5**.
- **Yaw drive:** off-axis XC330-M181 through a 1:1 spur pair. It gives 2× speed margin at 5 V and passes at 3.7 V.
- **Straight legs don't work:** the face carrier swings under the pitch axis at chin-down, so the legs keep a short rearward knee.
- **Pitch axis is not moved for styling.** A0 is re-solved from the revised mass tree only.

## Accepted limits against Layout 03

- The head-to-disc gap bottoms out at 4.3 mm at the stops, below the 25 mm finger gap of EN ISO 13854. Layout 03 had a 5.6 mm pinch against its bridge.
- The yaw stage is inside the body, gear-driven and harder to service than an external spindle. The spur mesh adds backlash; preload or anti-backlash is open.
- The camera sees body geometry from about 21.5° of chin-down at the worst roll and yaw (Layout 03: 23.6°).

## Validation

Iterate `motion_envelope.py --write` and `mass_layout.py --solve` to convergence, then run `check_layout.py` and `check_revision.py` on the 7 × 8 roll × pitch grid out to the hard stops. Relief cuts sample the full stop range densely. No servo freeze, cable qualification, structural or print claim.
