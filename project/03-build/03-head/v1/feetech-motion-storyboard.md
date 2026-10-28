# Feetech pitch speed cap — build storyboard delta

2026-10-07. This is the build-specific change to the read-only [RP-01 storyboard](../../../02-prototypes/RP-01-head/storyboard.md). D-046 caps the **fastest pitch moves** at 70% of their previously authored segment speed. The same `MJ5` or `PULSE` shape is retained; stretching a segment's time by `1/0.70` makes both its peak speed 70% and its peak acceleration 49% of the original for an unchanged angle. The motor-side term can then be re-screened with the new 1:281 ratio and, after CAD refit, the actual head v1 mass tree.

## Changed keyframes

| Motion | Build keyframes (milliseconds; degrees) | Reason |
|---|---|---|
| `HM-08` laugh, minimum viable | **Unchanged**: `t0 P0 → t150 P+4 → t280 P-1 → t430 P+4 → t580 P-1 → t800 P0` | Its reversals are slower than the best-case 7°/100 ms design case; the cap is on the fastest segments |
| `HM-08` laugh, best case | `t0 P0 → t110 P+5 → t253 P-2 → t425 P+6 → t583 P-2 → t713 P+4 → t823 P0 → t993 HOLD` | Stretch the 7°/100 ms, 8°/120 ms and 8°/110 ms reversals to 143, 172 and 158 ms (rounded upward). Their speed ≤70% and acceleration ≤49% of the old segment; the other stroke times are retained. Complete phrase becomes 993 ms versus 850 ms, leaving only 7 ms against the old 1.00 s phrase screen |
| `HM-15` startle, minimum viable | `t0 P0 Y0 R0 → t358 P-10 Y±5 R±4 → hold to t608 → recover by t1308` | Stretch the coordinated outbound 250 ms to 358 ms so the pitch peak is ≤70%; hold stays 250 ms and recovery keeps its 700 ms duration. The 1.2 s original phrase screen is missed by 108 ms, so perceptual acceptance must be re-scored |
| `HM-15` startle, best case | `t0 P0 Y0 R0 → t258 P-15 Y±8 R±6 → hold to t508 → t778 P-5 Y±3 R±2 → t1078 P0 Y0 R0` | Stretch the coordinated outbound 180 ms to 258 ms (round up); preserve the 250 ms freeze and 570 ms recovery. The best-case 1.0 s phrase screen is missed by 78 ms |

The startle yaw and roll paths are stretched with pitch to preserve the simultaneous recoil pose. Their *individual* servo speeds also fall; this does not authorize changing the independent yaw/roll maximum-speed screens elsewhere. The 993 ms laugh is only a numerical re-authoring: B1 tracking, B4 reversal quality and a user-visible motion review decide whether it still reads as three irregular chuckles. The startle timing misses its previous duration target and needs a new storyboard acceptance decision before any claim of G02/G03 passage.

## Recalculation boundary

The old [fullproofmath §11.3](../../../02-prototypes/RP-01-head/fullproofmath.md) values are based on the prior head mass/inertia and original profiles. **Do not rescale its aggregate busy-minute RMS or P07 modes by 0.49.** Rebuild the per-segment trajectories above, re-run all retained physical-law cases and the combined load cases with `03-head/v1/cad/mass-placement.json` generated from the fitted STS3045M housings, then calculate the new busy-minute duty. Re-run the pitch-frame and roll-mount FEA with the new geometry and masses; the existing 41/84 Hz results do not include the new mount/horn interfaces. The actuator screen records the current provisional paper bounds and P01–P09 status.
