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

## Decision: turntable yaw stage at a 40 mm neck (rev B)

Rev A reached a 21 mm neck with a firmware roll/pitch envelope, giving up full combined motion, the mechanical head/body guarantee and Pi 5 cooler airflow. Rev B keeps all three and sets the neck to the minimum that allows them. A 58 mm variant was also built and checked; it recovers most of the finger gap and camera margin but was not kept:

- **Clearance rule** (checking floor): at least 4 mm at the hard stops, at least 2 mm with 1° of stop overtravel. The full-grid sweep is Z −26.3 (−27.7 with overtravel), so the disc top sits at **Z −30.5** (4.2 mm clear at the stops, 2.85 mm at overtravel).
- **Cooler rule:** keep body/chassis Layout 02's 10.5 mm of air above the Pi 5 cooler (Z 123 → 133.5). The yaw-stage stack of plate 4 + bearing 7 + disc 5 then puts the disc top 9.5 mm above the body top, so the body top is **Z −40**.
- **Result:** 40 mm neck, full roll ±18 / pitch −22…+40 in every combination, and the hard stops alone keep the head off the disc.
- **Straight legs don't work:** the face carrier swings under the pitch axis at chin-down, so the legs keep a short rearward knee.
- **Pitch axis is not moved for styling.** A0 is re-solved from the revised mass tree only.

## Accepted limits against Layout 03

- The minimum head-to-disc gap is 4 mm, below the 25 mm finger gap of EN ISO 13854, so there's a pinch zone. Layout 03 had one against its bridge too (5.6 mm).
- The yaw stage is inside the body, gear-driven and harder to service than an external spindle.
- The camera sees body geometry from 17.3° of chin-down at the worst roll and yaw (Layout 03: 23.6°).

## Validation

Iterate `motion_envelope.py --write` and `mass_layout.py --solve` to convergence, then run `check_layout.py` and `check_revision.py` on the full 7 × 8 roll × pitch grid. Relief cuts sample the full range densely. No servo freeze, cable qualification, structural or print claim.
