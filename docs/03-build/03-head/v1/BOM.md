# Head v1 bill of materials — working inventory

Started 2026-10-07 for **one head**. Quantities are installed quantities, with no spare or scrap allowance unless a row says otherwise. This is a procurement and design worklist, not a release BOM.

The [project BOM](../../BOM.csv) carries the specification, source and release check for every ID below. The model basis is the [head v1 CAD](cad/README.md); its [mass tree](cad/mass-placement.json) is where the `M0xx` allowance IDs come from.

**Counting boundary:** everything that moves with the head above the yaw disc: the pitch and roll actuators, the printed shell, frames and ears, the display, camera, C2 and LED, and the head-side harness and hardware. The yaw servo, bearing cartridge, gears and FFC cassette are body parts ([body BOM](../../02-body/v1/BOM.md#body-side-yaw-stage-and-shared-board-interfaces), D-044).

## Actuators

| ID | Part | Qty | State |
|---|---|---:|---|
| HD-001 | **Feetech STS3045M** pitch and roll servo: 4.8–7.4 V, 0.59 N·m stall / 0.20 N·m rated and 75 rpm no-load at 6 V, 34.8 g, 36 × 15 × 29.2 mm, 1:281 gears, 25T/Ø5.9 mm output, coreless, 12-bit magnetic encoder, Feetech half-duplex TTL ([D-046](../../decisions.md#d-046), [build screen](feetech-actuator-screen.md)) | 2 | CANDIDATE, first choice |
| HD-002 | Pitch output horn: 25T aluminium Ø20 disc, 4 × M3 on Ø14 PCD (`E` listing values), screwed to the +Y yoke leg ([D-049](../../decisions.md#d-049)) | 1 | HOLD: measure before printing the leg |
| HD-003 | Output centre screws, ISO 4762 M3 × 5 (coupler floor and horn web into the servo output) | 2 | CANDIDATE |
| HD-004 | Roll output coupler, goBILDA 4001-0025-0006 (25T spline to Ø6 clamping bore) | 1 | CANDIDATE; spline fit on the received servo |
| HD-005 | Horn-to-leg screws, ISO 7380 M3 × 6 | 4 | CANDIDATE |
| HD-006 | Servo ear screws, ISO 7380 M2 × 6, into M2 × 3 inserts | 8 | CANDIDATE |
| HD-007 | Servo ear washers, ISO 7089 M2.5 (Ø6 × 0.5) | 8 | CANDIDATE |

## Pitch pivot and yoke joints

| ID | Part | Qty | State |
|---|---|---:|---|
| HD-008 | MR106ZZ bearing (6 × 10 × 3) in the −Y yoke leg: the passive pitch pivot ([D-051](../../decisions.md#d-051)) | 1 | CANDIDATE |
| HD-009 | Ø6 h6 steel D-shaft pin, cut to 11.5 mm: through the bearing into a D-bore on the pitch frame's −Y boss | 1 | CANDIDATE |
| HD-010 | Pivot retainer screws, ISO 7380 M2 × 4, into two M2 × 3 inserts in the −Y leg pad; heads flush with the leg face | 2 | CANDIDATE |
| HD-011 | Yoke leg to disc screws, ISO 7380 M2 × 6, from each plinth's inner face into M2 × 3 inserts in the disc keys | 4 | CANDIDATE |

**Why ([D-051](../../decisions.md#d-051)).** The −Y pivot was a Ø8 pin, loose in Ø8.4 holes, 1.5 mm into the leg and not retained; the legs had no joint to the disc. The pivot now runs on a bearing captured inside the 6 mm leg pad by a printed 1.0 mm retainer, because nothing can stand proud of the leg's outer face: the skin passes it at 0.98 mm. Each leg's plinth now sits over a key on the disc and is held by two screws from its inner face, because the disc underside must stay flat over the yaw pinion. The retainer plate and the keys are prints (M011-Y, M012); the six M2 × 3 inserts are the head's standard OD 3.6 article.

**Why the STS3045M ([D-046](../../decisions.md#d-046)).** It costs ₹3,661 including GST at [Evelta](https://evelta.com/sts3045m-6v-6kg-cm-360deg-metal-gear-digital-servo-motor/), with 5 in stock on 2026-10-07: about a third of an XC330. On paper it clears roll at full speed (about 1.8×) and pitch with the fastest moves capped at 70% speed (about 1.7×). Its rated 0.20 N·m continuous torque is 2.6× the pitch RMS demand. Its metal gears suit pitch's constant gravity load. Margins are estimates at the 5.23 V worst servo terminal of the proposed 5.5 V head rail; bench B1 replaces them.

**Ranked fallbacks.** None is registered; each would need its own decision.

| Rank | Part | Use if | Cost and catch |
|---|---|---|---|
| 2 | ROBOTIS XL330-M288-T (18 g, 0.52 N·m, 103 rpm at 5 V) | B4 lash or the Feetech protocol fails | About $24 in the US; India price unconfirmed. Plastic gears; pitch continuous torque only about 1.4×. Drop-in to the current XC330 mounts and the Dynamixel bus |
| 3 | ROBOTIS XC330-M288-T (RP-01 `ACT-01`, 23 g, 0.93 N·m, 81 rpm at 5 V) | B1 fails on pitch at 70% speed | ₹11,459 at MG Super Labs, out of stock 2026-10-07. Pitch at full speed (36% margin). Matches the current CAD |

Ruled out for the head: XL430-W250 and AX-12A (9–12 V, 55–57 g, too large); Waveshare ST3215 and STS3215 (about 55 g, 0.6–1.3° lash); Feetech STS3250 (12 V, 74.5 g).

**What the STS3045M changes**

- **Head rail.** Its 4.8 V minimum is above the rail's 4.74 V worst-case servo terminal. Raise `PB-HEAD` to 5.5 V and move the 5.74 V clamp to about 5.9 V (D-046).
- **CAD ([D-049](../../decisions.md#d-049), done).** Roll: the servo bolts by its ears to a plate behind the torsion box and drives the Ø6 spindle through the goBILDA coupler; the rear bearing moved forward. Pitch: the servo rides on the pitch frame (collar and floor) and its horn is screwed to the +Y yoke leg, which was widened and must be printed in a CF-filled filament. Rear trim moved to two seats on the cover.
- **Mass.** Both servos are pitch-carried (34.8 g each). Yaw-carried head mass is 648.5 g (+44.2 g on the committed source); the A0 axes are re-solved.
- **Firmware and protection.** C2's servo driver and the RP-02 `BD-13` per-axis protection move from Dynamixel to Feetech registers.
- **Motion.** The fastest pitch moves (laugh reversal, startle) are capped at 70% speed and must be re-screened (gate P07).

## Yaw servo (body part)

The yaw servo sits in the body and is counted in the [body BOM](../../02-body/v1/BOM.md#body-side-yaw-stage-and-shared-board-interfaces). It is listed here to show the full actuator set.

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-043 | **Waveshare ST3215-HS** yaw servo: 6–12.6 V, 20 kg·cm (about 2.0 N·m) stall and 0.094 s/60° (106 rpm) no-load at 12 V, 2.4 A stall, 240 mA no-load, 68 g, about 45 × 25 × 35 mm (`E`, STS3215-class case), metal gears, 360° magnetic encoder, Feetech serial bus; on a 12 V yaw-only rail on PCB-03 ([D-047](../../decisions.md#d-047)) | 1 | CANDIDATE, first choice; integrated in the body CAD (D-048) |

**Why the ST3215-HS ([D-047](../../decisions.md#d-047)).** Yaw's first priority is speed while accelerating the head's 0.0013 kg·m², and it is the tightest axis on paper. The HS has roughly 40% or more margin at 63 rpm, against about 16–27% for the XC330-M181 on the 5.5 V rail. It speaks the same Feetech protocol as HD-001, so the robot runs one servo protocol. It costs ₹2,050 at [ThinkRobotics](https://thinkrobotics.com/products/st3215-hs) (pre-order on 2026-10-07; regular ₹3,000), or $21.99 at [Waveshare](https://www.waveshare.com/product/robotics/motors-servos/motors/st3215-hs-servo-motor.htm).

**Ranked fallbacks**

| Rank | Part | Use if | Cost and catch |
|---|---|---|---|
| 2 | Feetech STS3250 (12 V, 4.9 N·m, 75 rpm, 74.5 g, steel gears) | B4 lash on the HS is over about 0.5° loaded | ₹6,100 at Evelta, in stock. Best measured lash (0.13° unloaded / 0.33° loaded). Speed margin only about 6–14%. Same rail and protocol; similar size class, to confirm |
| 3 | ROBOTIS XC330-M181-T (the D-044 servo) | No Feetech case fits the yaw bay | ₹11,459. Fits the current bay. Adds Dynamixel as a second protocol |

**What the ST3215-HS changes**

- **Rail.** A second `LTC3119` on PCB-03 boosting to 12 V for yaw only. It gives about 2 A from a low pack (`E`), below the 2.4 A stall, so the servo's protection current is set under it. Nothing new crosses the cable cassette.
- **Yaw bay ([D-048](../../decisions.md#d-048)).** Done in the body CAD: the servo hangs horn-up on the pinion axis, 7.6 mm lower, on a frame clamp ring; the Pi, cooler and PCB-09 moved +10 mm X and −6 mm Y to make room and to recover the tip margin (a_tip 1.621 with the STS3045M head). The longer lever puts about 0.36 N·m of side load on the servo output (bench check).
- **Lash.** Unmeasured for the HS; the STS3215 family measured 0.6–1.3°. The scissor pinion removes only the mesh lash, so bench B4 decides between the HS and the STS3250.

**Actuator set cost:** about ₹9.4k (2 × STS3045M + ST3215-HS), or about ₹13.4k with the STS3250 on yaw.

## Registered head electronics

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-085 | Status LED carrier PCB-11 (WS2812B-2020 behind the crown light pipe) | 1 | Working selection |
| CH-086 | C2 head carrier PCB-12 (ESP32-S3-Zero, head link and display transceivers, servo-bus interface, watchdog) | 1 | HOLD |

PCB-12's servo-bus interface must carry the Feetech protocol for HD-001 (D-046).

## Not yet registered

These parts are in the head CAD and mass tree but have no BOM row yet. The `M0xx` IDs are mass-tree allowances, not BOM IDs.

| Mass row | Part | Mass basis |
|---|---|---|
| M002 | Waveshare 4.3 inch display and retention (non-touch variant) | 133 g allowance |
| M003 | Display window and full-width mask | 15 g allowance |
| M005, M006 | Raspberry Pi Camera Module 3 Wide, bracket, CSI cable and strain relief | 10 g + 8 g |
| M007 | Addressable LED, installed (with CH-085) | 5 g |
| M008 | C2: Waveshare ESP32-S3-Zero on CH-086 | 20 g, installed mass unknown |
| M019a | Prints: front bezel and camera crown, octagonal skin, removable rear cover, two ears (inner mount, removable cap, amber inlay, dark centre) | CAD volume, PLA |
| M010, M011, M012 | Prints: rolling cradle and ear stalks, roll bearing cartridge (trial), pitch frame and roll saddle, yaw yoke legs, yaw turntable disc, CSI exit guide | CAD volume, PLA |
| M016–M018 | Roll and pitch bearings and shafts | 6 + 8 + 8 g allowances |
| M016 | Ø6 × 34.6 steel roll spindle (was 32 mm) | Modelled, 7.7 g |
| M021a, M021 | Fasteners: ear M2 screws, front M2 × 10 (6), rear M2 × 6 (4), hidden hardware; see `cad/generated/fastener-stack.json` | Modelled |
| M022 | Trim: tungsten ear slugs, brass rear-cover washers | 9.4 g nominal |
| M020 | Non-camera head harness | 15 g allowance |

## Next actions

1. **Order one STS3045M and one ST3215-HS** for the bench (the HS is a pre-order) and get Feetech's datasheet drawing, gear ratio and protection registers.
2. **Measure the received HS** against the D-048 model: horn-axis offset, corner holes (drawing and STEP differ 0.8 mm), horn thread, plug height with cables.
3. **Bench B1:** one STS3045M against a pitch mock-up (0.00079 kg·m², real CoM offset) at 5.23 V on the 70% trajectory; log current and position.
4. **Bench B4:** loaded and unloaded lash on both servos (the HS result picks between it and the STS3250) with an external angle reference, dead-zone registers at minimum.
5. **Received-part checks for D-049:** measure the pitch horn (HD-002) before printing the +Y leg, try the goBILDA coupler (HD-004) on the servo spline, and print a modulus coupon of the CF leg filament (≥ 4.5 GPa along the layers).
6. **Rails:** record the 5.5 V head setpoint, the clamp change and the 12 V yaw rail in `04-pcbs/power-boards.md`.
7. **Order the second STS3045M** once B1 and B4 pass.
8. **Register the head parts above** as HD rows as their selections firm up.
