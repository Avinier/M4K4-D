# Makad: Feetech yaw servo integration (D-048)

Oct 7, 2026 · @Aditya

> **Review correction (2026-10-08):** The initial four case-mount screw axes
> missed the corresponding official STEP holes by 0.8 mm. The yaw CAD now
> follows the STEP axes and its checker no longer waives a mount-screw/case
> collision. The earlier 0.120 mm³ Pi USB-C plug reserve clash is clear after
> specifying a ≤13 mm down-exit plug envelope; a matching physical plug must
> still be selected and measured. The proposed
> 0.30 N·m yaw ceiling is not implemented or bench-calibrated, and its own
> PETG tooth estimate exceeds the 15 MPa screen flag. The 2026-10-08 shell-fit
> output is clean; received-part checks remain open. The corrected yaw-stage CAD rerun passes;
> read the earlier "every targeted check passes" statement with the remaining
> connector and torque limits below.

## Summary

The Feetech yaw servo (Waveshare ST3215-HS) has a viable body v1 CAD placement without raising the shell. The current mass-only estimate uses no extra ballast. Its mounting, connector and torque limits remain open as noted above. It was recorded as decision D-048 on 2026-10-07.

- **Actuator set:** two Feetech STS3045M on head pitch and roll (D-046) and one ST3215-HS on body yaw (D-047). Together they cost about ₹9.4k, against about ₹34k for the original XC330 set.
- **How it fits:** the servo hangs horn-up on the existing yaw pinion, 7.6 mm lower than the XC330 sat, clamped to a ring built into the frame. The Raspberry Pi, its cooler, the compute tray bosses and PCB-09 moved 10 mm forward and 6 mm toward −Y to make room.
- **Tipping:** the forward move recovers the stability the heavier Feetech servos cost. The forward tip limit is 1.621 m/s² with the Feetech head, against a 1.582 minimum.
- **One error found and fixed:** two sessions' fit screens had placed the servo's 3D model 25.5 mm away from its real output shaft. The live model now uses the axis from Waveshare's drawing.
- **Not yet proven:** nothing has been bought or built. The received servo's dimensions, backlash and side-load endurance, a matching Pi power plug and the head re-balance remain open.

## Background: why these servos

The servos were chosen on a budget of ₹20–25k for three. The ROBOTIS XC330 working family (RP-01 `ACT-01`) cost about ₹11.5k each. Each axis has a different main demand: yaw needs speed, pitch needs torque, and roll should be light.

| Axis | Carries | Top speed | Peak torque (incl. servo inertia, high bound) | Chosen servo | Decision |
| --- | --- | --- | --- | --- | --- |
| Yaw (in body) | 618 g head + pitch/roll stages | 63 rpm | about 0.22 N·m incl. scissor-mesh drag | Waveshare ST3215-HS, 12 V, 2.0 N·m, 106 rpm, 68 g | D-047 |
| Pitch | roll servo + head, 482 g | 39.3 rpm, capped to 27.5 rpm (70%) | 0.249 N·m at full speed, about 0.145 at 70% | Feetech STS3045M, 0.59 N·m at 6 V, 75 rpm, 34.8 g | D-046 |
| Roll | head only, 376 g | 30 rpm | 0.129 N·m | Feetech STS3045M | D-046 |

- **Pitch and roll (STS3045M, ₹3,661 each at Evelta).** It has metal gears, a coreless motor and a stated 0.20 N·m continuous rating, 2.6× the pitch RMS demand. On the paper screen it clears roll at full speed (about 1.8×) and pitch with the fastest moves capped at 70% (about 1.7×). Its 4.8 V minimum forced the head rail up from 5.0 to 5.5 V.
- **Yaw (ST3215-HS, about ₹2,050 at ThinkRobotics, pre-order).** Speed is yaw's first priority. The XC330-M181 had only 8% margin before the D-044 gear train's drag, and the HS has roughly 3×. It also keeps the robot on one bus protocol. It needs a 12 V yaw-only rail on PCB-03, which stays out of the cable cassette.
- **Rejected:**
  - XL430-W250 and AX-12A: they need 9–12 V, weigh 55–57 g and are too big for the head.
  - STS3215 and ST3215 standard: 0.6–1.3° measured backlash, and too slow for yaw.
  - STS3250: kept as the yaw fallback if the HS backlash fails bench test B4.
  - XL330: kept as the Dynamixel alternative for pitch and roll.

## The problem: space and tipping

The ST3215-HS did not fit where the XC330 was. Even if it had, the Feetech servos left the robot exactly on its tipping limit.

- **Space.** The yaw servo hangs under the yaw plate, directly over the Pi 5, its Active Cooler and PCB-09 (which sits on the Pi's GPIO header). The HS case is 45.2 × 24.7 × 35 mm, about twice the XC330's volume. At the old position it hit the PCB-09 strip, the GPIO socket and the Pi.
- **Tipping.** The forward tip limit is a\_tip = g · CoM x / CoM z, and must stay at or above 1.582 m/s². The Feetech set adds about 69 g, high up and rearward of the robot's CoM. With no layout change, a\_tip fell from 1.663 to exactly 1.582.

| Option tried | Result | Why rejected |
| --- | --- | --- |
| Move the pinion around the R37 gear circle | Every position hits the Pi or cooler | The Pi fills the whole footprint under the yaw circle |
| Raise the body top to clear the Pi | Needs +15.5 mm; a\_tip falls to 1.500 | Fails tipping; would need about +38 g ballast and a taller shell |
| Remove or reshape the ballast | Frees space only in the nose, far from the yaw bay | Without it a\_tip falls to about 1.39 |
| Fall back to the XC330-M181 on yaw | Fits; a\_tip about 1.616 | Kept as the D-047 fallback; the builder chose to make Feetech work |
| **Shift the compute stack, keep the servo on the pinion** | **Fits; a\_tip 1.621** | **Chosen (D-048)** |

## Error found: the servo model's axis

The ST3215-HS 3D model's output axis is 25.5 mm from its origin, and both sessions' first fit screens missed it. Waveshare's 2D drawing (`ST3215-2D.zip`) puts the Ø19.2 horn 10.11 mm from the case end. In the STEP, after the −90° turn about X, that is local X −25.5.

- **What was wrong:** `check_feetech_yaw_fit.py`, `check_feetech_yaw_relocation.py`, `check_feetech_yaw_compute_shift.py` and `feetech_yaw_cradle.py` put the STEP origin on the pinion. The four Ø2.5 holes they took for case screws are the horn's holes, on a 7.11 mm radius.
- **Why the conclusion survived:** turned 180° about the true axis, the case fills almost the same box: X −19.1…26.1 against −19.6…25.6 before. The "shift the Pi −6 mm in Y" layout still held. The trial cradle and every gap figure from those scripts did not.
- **What the drawing added:** both bus plugs sit in a recess on the horn face, so horn-up mounting needs about 10 mm of plug room above the case. The mounting holes are Ø1.6 × 2.8 mm deep, in a step 2.58 mm below the case top. The drawing and the STEP disagree on their position by 0.8 mm.
- **Now:** the servo is placed only through `yaw_servo_st3215_hs()` in `body_v1_model.py`. The old fit report carries a "superseded" banner, and a memory note records the offset.

## Design (D-048)

The servo keeps the D-044 gear train untouched. Everything else moved around it.

**Yaw servo and mount**

| Item | Design | Constant / function |
| --- | --- | --- |
| Placement | Horn up on the pinion axis (16, 37); case runs −X; overall STEP maximum Z 122.4, 7.6 mm below the old top datum (not the case seating face) | `yaw_servo_st3215_hs()`, `YAW_SERVO_DROP` |
| Why 7.6 mm | Room for the horn-face plugs under the plate; the bottom idler disc stays above the PCB-03/04 plug layers (Z 84.3) |  |
| Mount | Frame-integral clamp ring with four ×4.8 pillars seated on the corner-hole step; two side walls up to the pad under the plate | `_yaw_servo_mount()` |
| Fasteners | 4 × M2 × 8 from above into the corner holes (about 1.9 mm thread); driver holes through pad and plate | `YAW_SERVO_MOUNT_SCREWS`, BO-061 |
| Plug access | Window X −15.6…4.9, Y 28.8…45.2 over the plug recess, open to −X for the W15 cable | `YAW_SERVO_PLUG_WINDOW` |
| Drive hub | r 8.8 from the horn face (Z 121.85) to Z 136.2; Ø12.4 pocket over the horn centre boss; four horn screws at 7.11 mm radius from 10.1° | BO-056 |
| Proposed torque ceiling | 0.30 N·m CAD stress assumption; no firmware limit or delivered torque verified. The 1.96 N·m stall is far above the printed tooth screen | `YAW_SERVO_TORQUE_LIMIT_NM` |

**Compute stack (+10 mm X, −6 mm Y, `COMPUTE_SHIFT_X/Y`)**

- **Moved together:** the Pi 5, the Active Cooler, the four tray bosses and inserts, the push-pin keep-outs, PCB-09 with all its parts and plug reserves, J9-4, and the Pi USB-C plug reserve. The power pigtail drop moves in X only.
- **−6 mm Y** clears the Pi's GPIO edge from the servo case (1.9 mm gap). **+10 mm X** moves about 112 g forward to recover the tip margin.

**Tray (BO-033)**

- The +Y edge stops at Y 23.5, 1.1 mm inboard of the servo, so the tray still slides in from the front.
- The front edge grows to X 80.5.
- The front screw moves to (64, −41.5) on a new −Y ear; its frame column extends to Y −45.
- The rear +Y screw, block and column move to (−24, 17.5); the old corner would have swept under the servo.
- The vent row at Y 21 is dropped. The print is now 20.58 g, was 23.1 g.

**Boards and harness (paper only)**

- **C3 carrier PCB-10:** the Z 92 GH header row restarts at X 6.5, right of the moved USB-C plug: J10-7, J10-3, J10-4, J10-10, J10-12. The unused spare J10-11 loses its header.
- **PCB-04:** its top-entry plug reserve now starts at X −14, so J4-6 must sit forward of that.
- **Harness:** the `HARNESS_SIGNAL_TRUNK` reserve moves 4 mm toward −Y, clear of the servo's bottom disc.

## Verification

The original targeted body scripts passed their own assertions. The review found a mount-hole error that their yaw checker waived, plus a connector clash and under-tray wiring-reserve overlaps outside the compute check's pass criteria. The corrected yaw and compute runs must be read with those limits. These are geometry and mass screens on purchased STEPs, not physical tests.

| Check | Original reported result | Scope of that run |
| --- | --- | --- |
| `check_yaw_stage.py` | ALL PASS | No stage, sweep (±61°), cartridge-lowering, pinion-drop or moving-part clashes. Frame is one solid. Mesh gap 0.072 mm; pinion 0.6 mm over the hub shoulder; cassette 13.0 mm over the cooler. Mass row matches |
| `check_compute_mount.py` | ALL PASS | Pi bosses, inserts, screw heads, push-pin clearance, tray-screw driver paths, front-slide install sweep |
| `check_cooling_path.py` | ALL PASS | Fan intake, grille and air path with the moved cooler |
| `check_body_frame_fit.py` | Clean | Frame vs chassis, joint hardware, lift, cassette slide, tool paths |
| `check_body_panel_fit.py` | Clean | Panel frames, inserts, screws |
| `check_mic_mounts.py` | ok | Mic boards and ports clear |
| `check_charge_inlet.py`, `check_power_button.py` | ALL PASS | Rear-panel parts unaffected |
| `check_body_layout.py` | ok | Mass register, CoM and tip screens (after the one-line `HEAD_V1` key fix that D-045 recorded) |
| `check_shell_frame_fit.py` | Clean (2026-10-08 output) | Shell lowered over the new frame and compute stack at the checker's sampled positions |
| Chassis `check_layout.py` | Not run | Whole-robot chassis layout |

The original yaw check reported both hub and case-mount screw intersections as engagement. That waiver was wrong for the case screws and has been removed. The corrected screw axes have zero case-solid intersection in a separate exact-solid check, and the full corrected yaw-stage rerun reports all four hole-axis offsets as zero and passes its assertions.

The first revised `check_compute_mount.py` rerun failed its new fixed-part gate: the earlier Pi power-plug reserve intersected the C3 DevKitC STEP by 0.120 mm³. The down-exit, ≤13 mm plug envelope now clears it and the compute checker passes, but a matching purchasable plug has not been identified. Its tray retention, driver and slide-in checks remain clear. Current cooling-path, body-frame-fit and full shell/frame lowering outputs are clean. Under-tray harness-reserve intersections remain informational.

## Mass and stability

With the Feetech head, the robot's forward tip limit is 1.621 m/s², 2.5% above the 1.582 minimum. The chosen +10 mm Pi shift earns that margin back; lifting the body would have lost it.

&#91;embedded content: check\_body\_layout.py mass register + feetech-mass-whatif.json head, computed 2026-10-07; Pi shift stops at +15 mm (speaker basket beyond)\]

| Mass row | Before | After D-048 |
| --- | --- | --- |
| `BODY_YAW_STAGE` | 150.3 g at (14.81, 7.81, 136.22) | 199.4 g at (11.62, 15.0, 126.86) |
| `BODY_PRIMARY_FRAME` | 169.18 g | 172.59 g (+3.4 g mount, column, block) |
| `COMPUTE_TRAY_AND_PI_FIXINGS` | 29.5 g | 27.07 g at (21.16, −10.44, 86.98) |
| Whole robot, current head tree (XC330 rows) |  | 2,586.4 g; a\_tip 1.667, worst head pose 1.663 |
| Whole robot, STS3045M head what-if |  | 2,610 g; a\_tip 1.621 |

The 95 g harness allowance must stay forward of X −4.0 mm. The worst-head-pose figure for the Feetech head waits on the head re-balance.

## Risks and open items

The largest risk is side load on the yaw servo's output shaft, which no vendor rates.

| Risk | Size | Mitigation | Closed by |
| --- | --- | --- | --- |
| Side load on the HS output | 0.355 N·m at 13.3 N peak (XC330 layout: about 0.2); lever grew to 26.6 mm with the 7.6 mm drop | Support bearing for the hub in the pad, with a compliant coupling to the pinion | Bench B1/B4 plus endurance with the pinion fitted |
| HS backlash | Unmeasured; the STS3215 family measured 0.6–1.3° | Dead zone to 1 count; swap to the STS3250 (same rail and protocol) if over about 0.5° loaded | Bench B4, external angle reference |
| Tip margin with the Feetech head | 1.621 vs 1.582 (2.5%); head-pose bound needs the head re-balance | Keep the harness centroid forward of X −4.0; more ballast if needed | Head A0 re-solve, then re-run the tip screen |
| Model vs received part | Corner holes differ 0.8 mm between drawing and STEP; one invalid STEP solid | Measure before printing the mount | Received HS |
| Mount thread | About 1.9 mm of M2 thread in the case corner holes | Confirm depth and material; longer screw if deeper | Received HS |
| Servo service | Two mount screws sit under the cartridge flange | Accept for v1, or move the ring screws outward in a later revision | Assembly trial |
| Tight gaps | Tray to servo 1.1 mm; Pi to tray rim 1.17 mm in plan; ring to cassette 0.8 mm | Printed fit coupon | Print and fit |

**Also open:**

- the 12 V yaw converter on PCB-03 (schematic, 56 × 44 mm placement, braking clamp);
- the W15 cable route from the plug window to `J3-5`;
- the Feetech driver and protection in C2 firmware;
- the STS3045M head mounts and FEA (D-046);
- the mic noise check with the HS running (AR-61).

## Next steps and files changed

Buy the test servos first: every remaining number depends on measured parts.

- [ ] Order one ST3215-HS (pre-order), one STS3045M, a Feetech USB bus adapter and a 12 V bench supply
- [ ] Measure the received HS: horn-axis offset, corner holes and depth, horn thread, plug height with cables
- [ ] Bench B4 (backlash) and B1 (margin and current) on both servos; side-load endurance with the pinion fitted
- [ ] Review the shell-fit result when the 70-minute run finishes
- [ ] Refit the STS3045M head mounts, re-solve the head balance, re-run the tip screen
- [ ] Design the 12 V yaw converter on PCB-03 and route W15
- [ ] Commit D-048 separately from the other sessions' uncommitted work

| File | Change |
| --- | --- |
| `02-body/v1/cad/body_v1_model.py` | HS placement and mount, drive hub, compute shift, tray, PCB-09, C3 header row, PCB-04 plug reserve, trunk reserve, mass rows |
| `02-body/v1/cad/check_yaw_stage.py` | HS labels and mass, screw engagement reported as info |
| `02-body/v1/cad/check_body_layout.py` | Head mass-row key `HEAD_V1` (pre-existing break) |
| `decisions.md` | D-048 entry and index row |
| `BOM.csv`, `02-body/v1/BOM.md`, `03-head/v1/BOM.md` | BO-033, BO-043, BO-056, BO-061 |
| `02-body/v1/cad/README.md` | New section on the Feetech yaw servo and compute shift |
| `02-body/v1/cad/feetech-yaw-fit.md`, `feetech-migration-status.md` | Superseded banner; status rows 3.1 and 3.2 |
