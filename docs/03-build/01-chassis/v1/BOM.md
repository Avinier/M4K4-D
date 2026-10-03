# Chassis v1 bill of materials — working snapshot

Reviewed 2026-09-30 from the [project BOM](../../BOM.csv) for **one rolling chassis**. Quantities are installed quantities, with no spare or scrap allowance. This is a procurement and design worklist, **not a released order or fabrication package**. `DESIGN` means custom geometry exists; `CANDIDATE` means a part family or SKU is proposed; `SELECTED` means the build choice is settled, with receipt and test checks tracked separately; `HOLD` means do not order or fabricate until the blocker is resolved; `OPEN` means the design still needs a choice before release. No row is marked received or measured.

The model basis is [chassis-v1.step.py](cad/chassis-v1.step.py) and [body_chassis_model.py](cad/body_chassis_model.py). Its scoped export includes the frame, wheels, motors, bearings, ball caster, battery pack, drivers, IMU, front range sensor, nose contact, and rear keel. The CAD README describes the [scope and exclusions](cad/README.md). The project BOM carries the detailed specification, source, and release check for every ID below. Shared electrical parts are counted once in that project BOM; the separate section below records whole-robot integration dependencies and does not imply that every board is needed for a bench rolling test.

## Fabricated and custom parts

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-001 | Structural frame design set | 1 set | DESIGN |
| CH-002 | Printed caster and sensor mount pod (not the caster) | 1 | DESIGN |
| CH-003 | Ball pod sensor lid (rear tongue + one M2 screw, D-011) | 1 | DESIGN |
| CH-004 | Wheel rim, six framed spokes ([D-008](../../decisions.md#d-008)) | 2 | DESIGN |
| CH-005 | Tyre: printed TPU 95A chevron, clamped; one left, one right ([D-009](../../decisions.md#d-009)) | 2 | DESIGN |
| CH-058 | Wheel hub cap, dark PETG ([D-008](../../decisions.md#d-008)) | 2 | DESIGN |
| CH-007 | Touch cap with two snap fingers and magnet pocket (D-011, D-013) | 1 | DESIGN |
| CH-008 | Rear skid and TCRT keel ([D-014](../../decisions.md#d-014)) | 1 | DESIGN |
| CH-009 | Replaceable dovetail wear shoe, PETG recommended ([D-017](../../decisions.md#d-017)) | 1 | DESIGN |
| CH-010 | TCRT bezel with both guard lips, PETG recommended (D-014, D-017) | 1 | DESIGN |
| CH-068 | 1 mm TCRT height shim, two fitted for the nominal Z 10 (D-014) | 2 | DESIGN |
| CH-011 | Battery tub bottom hatch: four M3 screws, two strap slots ([D-030](../../decisions.md#d-030)) | 1 | DESIGN |
| CH-012 | Turned steel stub: bearing seats, D-shaft bore, flange and spigot with an M3 tapped end for the hub cap ([D-007](../../decisions.md#d-007), [D-033](../../decisions.md#d-033)) | 2 | DESIGN |
| CH-013 | 9 × 60 × 19 mm steel ballast bar | 1 | DESIGN |
| CH-051 | Printed bearing housing ([D-007](../../decisions.md#d-007)) | 2 | DESIGN |
| CH-052 | 1.2 mm aluminium bearing retaining cap | 2 | DESIGN |

`CH-001` is a **design set** of five prints ([D-033](../../decisions.md#d-033)): two one-piece frame modules, two keyed plate-and-cheek carriers and the hatch. The front module is the front deck with its battery tub, both front rails and the front crossmember; the rear module is the rear deck, both rear rails and the rear skid crossmember. The carriers join the two modules through J04 (M3 screws into inserts in the rail ends). D-033 removed the J05/J06 tongue joints and the J16 deck screws; the IDs CH-073, CH-074 and CH-075 are retired and must not be reused. The material/process, calibrated fits and physical strength still need proof. The bezel and wear shoe have defined retention and service paths under D-014; their physical retention and floor tests remain open. The wheel is designed in the standalone [wheel CAD](cad/wheel/README.md) ([D-005](../../decisions.md#d-005), [D-008](../../decisions.md#d-008)): a printed TPU tyre clamped by CH-048/CH-049, and a hub cap (CH-058) held by one central screw (CH-059, D-033) over the D-007 wheel screws. The spin index (formerly CH-006) is removed. The O-ring fallback is recorded in D-005, with no BOM row. The hatch is held by four CH-076 screws into CH-077 inserts in the tub bosses. It also carries the pack: two CH-078 straps loop under it and over the cells, so hatch and pack come out together ([D-030](../../decisions.md#d-030)).

The purchased **Pololu #2691 caster** is a separate row (CH-016). It includes the 1-inch / 25.4 mm plastic ball, plastic rollers, and two-piece housing. The custom printed pod seats its three-hole flange on the chassis crossmember and provides the pocket for the front range sensor; it is a mount, not a second ball or replacement caster. Pololu lists a 29 mm assembled height and says this caster is intended as a third support for differential-drive robots up to about 10 lb. The CAD mass register estimates the complete robot at 2.55 kg (5.6 lb) and assigns about 18% of static weight to the ball, roughly 0.45 kg. That makes the size/load choice plausible for static support. Pololu gives general guidance, not a load rating; the printed pod strength, impacts, floor gaps, and threshold climbing still need physical tests. [CAD mass estimate](cad/generated/mass-properties.md) · [Pololu #2691 specs](https://www.pololu.com/product/2691/specs) · [dimension drawing](https://www.pololu.com/file/0J895/2691-dimensions.pdf).

## Purchased and electrical items

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-014 | [ThinkRobotics MOT3001-6V230RPM encoder gearmotor](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors) ([D-003](../../decisions.md#d-003)) | 2 | SELECTED |
| CH-015 | [OnlyScrews 688 ZZ bearing](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5), 8 × 16 × 5 (D-012) | 4 | CANDIDATE; page reports in stock |
| CH-016 | [Pololu #2691 1-inch plastic ball with plastic rollers](https://www.mgsuperlabs.co.in/estore/Pololu-Ball-Caster-with-1-Plastic-Ball) (not #2692) | 1 | SELECTED |
| CH-017 | [Adafruit #3297 DRV8833 breakout](https://www.adafruit.com/product/3297); one board per motor, both bridges paralleled within each board | 2 | SELECTED |
| CH-018 | [Robocraze Sharp GP2Y0A21YK0F](https://robocraze.com/products/robocraze-sharp-gp2y0a21yk0f-distance-sensor) | 1 | SELECTED |
| CH-019 | [TI DRV5055A3QDBZR bare linear Hall sensor](https://evelta.com/drv5055a3qdbzr-ratiometric-linear-hall-effect-sensor-with-analog-output-sot-23-3/) ([datasheet](https://www.ti.com/lit/ds/symlink/drv5055.pdf)) | 1 | SELECTED |
| CH-064 | Custom nose Hall carrier, 6.0 × 4.6 × 0.8 mm, for TI DRV5055A3 and filter | 1 | DESIGN |
| CH-065 | N35 Ø3 × 1.5 mm cap magnet | 1 | SELECTED |
| CH-066 | [Industrybuying RS PRO 821245 stainless compression spring](https://www.industrybuying.com/compression-spring-rs-pro-OFF.STO.223805403), pack of 10 listing; OD 2.75 × 0.25 wire × 15.7 free, 0.18 N/mm | 2 | SELECTED |
| CH-020 | Vishay TCRT5000 bare sensor with a soldered 350 mm GH4 lead to J10-10 ([spec](research/rear-tcrt-lead.md), D-016/D-021) | 1 assembly | SELECTED |
| CH-021 | Proposed ICM-42688-P custom PCB-07; [Robokits MPU6050 ₹173 bench alternative](https://robokits.co.in/sensors/accelerometer-and-magnetometer/triple-axis-accelerometer-gyro-mpu-6050-breakout) | 1 assembly | HOLD on final runtime interface/mount |
| CH-022 | Samsung INR18650-25R cell, finalized by builder | 2 | SELECTED |
| CH-023 | [Robocraze balanced 2S protection module TIFPS0629](https://robocraze.com/products/2-string-20a-lithium-battery-protection-module-balanced-version) | 1 assembly | SELECTED |
| CH-024 | Bourns AC72ABD resettable thermal breaker | 1 | HOLD |
| CH-025 | SEMITEC 103AT-2 10 kΩ NTC thermistor | 1 | HOLD |
| CH-026 | Cell straps, insulation, heat-shrink sleeve, and AWG16 pack leads | 1 lot | HOLD |
| CH-027 | Micro-Fit+ 1×2 pack disconnect with terminals | 1 pair | HOLD |
| CH-028 | ATOF main fuse holder | 1 | HOLD |
| CH-029 | ATOF fuse: final rating open; [5 A 0287005.PXCN test candidate](https://in.element14.com/littelfuse/0287005-pxcn/automotive-fuse-5a-32v/dp/2137127) | 1 | HOLD on final rating |

The nose cap uses a selected Ø3 × 1.5 mm N35 magnet and TI linear Hall sensor under D-013. Cap movement changes the analog voltage; firmware detects contact before the 3 mm mechanical stop. The former side-actuated tact switch is superseded. **CH-064 remains a tiny custom carrier**, because the bare SOT-23 sensor and its filter need a mechanically located, wired assembly in the 6.0 × 4.6 × 0.8 mm nose slot. A bench adapter can prove the circuit, but it does not replace the final nose carrier. PCB layout, startup/fault diagnostics, calibrated contact thresholds and physical fit remain release gates.

The motor-driver selection is two Adafruit #3297 boards, one per motor, with both DRV8833 bridges on each board paralleled to share that motor load. This is a reasonable test choice for the selected 6 V motor at its stated running load, conditional on current-sharing, temperature, stall/launch and braking tests. Treat 2 A as the nominal combined current-limit setting, not an unconditional continuous board rating. Do not connect outputs from separate driver boards together.

The selected A21 sensor has a 100 mm minimum range and a 38.3 ± 9.6 ms measurement cycle. At the worst-case cycle, it exceeds the existing 50 ms stop-path budget once scan and control-loop delays are included. Keep the user's sensor selection and hold autonomous stop-path release until timing and stopping distance are reworked and demonstrated. The CAD now uses the vendor STEP, checked against the Sharp outline drawing, with the mounting ears trimmed and the lead soldered ([D-027](../../decisions.md#d-027)). Check the received unit against it.

The selected Robocraze 2S balanced protection module is intended for purchase. Its listed 48 × 20 mm footprint does not confirm the model's provisional 2.9 mm thickness. Check received dimensions, protection thresholds, balancing, reset behavior, current/thermal limits, wiring and regeneration interaction before use with cells. Selection does not mean ordered, received or qualified.

The builder selected two Industrybuying RS PRO 821245 springs from a pack-of-10 listing for CH-066. Their 2.75 mm OD fits the existing spring pockets, but the 15.7 mm free length creates a predicted 2.41 N pair preload at the current 9 mm rest gap and 3.49 N at the 6 mm full-travel gap. Measure actual force, check spring stability/return and prove cap push force and snap-hook retention before declaring the nose mechanism passed. See [D-020](../../decisions.md#d-020).

The battery parts have separate functions: two 18650 cells store energy; PCB-01 protects the pack electrically; the **AC72ABD** is a resettable, cell-mounted thermal/current breaker that opens the pack circuit on excessive heat or current (72 °C ± 5 °C trip); the **103AT-2** is a temperature sensor mounted against a cell and wired to the charger’s temperature input so charging can respond to cell temperature. It does not interrupt current by itself. The AC72ABD has reset and leakage behaviour to account for; its upper trip tolerance is 77 °C, so a nominal 72 °C label does not establish the assembled cell-temperature limit. Bourns describes the AC part as a mini-breaker; SEMITEC lists the 103AT-2 as a 10 kΩ thermistor. [Bourns AC series datasheet](https://bourns.com/docs/product-datasheets/ac.pdf) · [SEMITEC AT thermistors](https://www.semitec.co.jp/products/thermistor_at/).

The selected Samsung cells form a **2S1P pack: 7.2 V nominal, 8.4 V full, 2500 mAh, about 18 Wh**. They are rated 20 A continuous per cell (8C), which is not a released assembled-pack rating. The CAD now spaces the cells at a 19.5 mm pitch, leaving 1.1 mm between them at the 18.4 mm maximum diameter; Samsung recommends more than 1 mm ([D-026](../../decisions.md#d-026)). The pack builder must hold that gap with a spacer or holder. The PCB-01 height in CAD is still a 2.9 mm placeholder until the module is measured. Pack construction remains open.

The cell straps connect the cells in the 2S series arrangement; insulation separates conductive tabs and cell surfaces to prevent shorts; the heat-shrink sleeve holds and protects the pack assembly; AWG16 leads carry pack power to the disconnect. The CAD mass estimate includes these as a roughly 11 g pack-build allowance, not as a finished purchased pack. The pack construction and electrical checks remain open.

**ATOF** is Littelfuse’s automotive blade-fuse family. The proposed 15 A ATOF fuse (CH-029) and its holder (CH-028) protect the pack feed against overcurrent. Electrically, the fuse goes after the pack disconnect and before PCB-02, close to the battery source. No ATO fuse fits the 11.3 mm channel beside the tub, so the holder is the Littelfuse 0FHA0001ZXJ inline type (30 × 10 × 26 mm with the fuse). It sits above the channel at X 52–82, Y 39–49, Z 73–99, about 25 mm over the pack disconnect, on a printed bracket from the front deck. The fuse loads from the top ([D-032](../../decisions.md#d-032)). That keeps it source-adjacent, as `board-specs.md` requires (PA-02). PCB-02 sits about 100 mm away on the rear panel, so it is not used. An India source for the holder is still open. The available 5 A 0287005.PXCN is a chassis-test candidate, not a finalized whole-robot replacement; BF-013A blade compatibility remains unverified. Account for the fuse’s 18.8 mm overall height including blades. [Littelfuse ATOF datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40). **Scope:** chassis v1 owns CH-028/CH-029 and the `PACK_ATOF_FUSE_HOLDER_ENVELOPE` CAD envelope; the chassis v1 CAD view includes it and the body v1 view filters it out, so it is counted once.

The drive gearmotor is the **ThinkRobotics MOT3001-6V230RPM** ([product page](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors); pick the 6V / 230RPM variant) (a generic JGA25-370, 6 V, about 26:1, 11 PPR Hall encoder, ₹1,180), chosen on cost and in-India availability in [decision D-003](../../decisions.md#d-003). It does **not** meet the RP-03 0.70 m/s heavy-launch gate: estimated 0.47 m/s at the launch load and about 0.20 N·m stall. Chassis v1 therefore runs a reduced drive envelope until bench measurements set it. The screw pattern, tapped depth and gearbox length in the CAD are assumptions until a unit is measured. Fallbacks are the Pololu #4803 and the DFRobot FIT0521. The battery board and other custom electronics are proposed envelopes, not released boards. Their separate design work belongs in [04-custom-pcb](../../04-custom-pcb/README.md).

The canonical [project BOM](../../BOM.csv) and this chassis snapshot are the source of truth for procurement status, supplier links, quantities and release checks. Availability observations are dated; no order or receipt is inferred.

## Fasteners and locating hardware

| ID | Joint hardware | Qty | State |
|---|---|---:|---|
| CH-030 | [ISO 7380 M3 × 6 button-head motor face screw](https://onlyscrews.in/products/hex-allen-button-head-m3-x-6-screw-pack-of-20) (D-030) | 4 | CANDIDATE |
| CH-031 | [ISO 7380 M3 × 8 caster screw, from below (D-011)](https://onlyscrews.in/products/hex-allen-button-head-m3-x-8-screw-pack-of-20) | 3 | CANDIDATE |
| CH-032 | [ISO 7380 M3 × 8 pod-to-crossmember screw (D-011)](https://onlyscrews.in/products/hex-allen-button-head-m3-x-8-screw-pack-of-20) | 2 | CANDIDATE |
| CH-033 | CNC Kitchen M3 × 5.7 front-crossmember insert for ball pod (D-011) | 2 | CANDIDATE |
| CH-034 | [ISO 4762 M3 × 30 rear keel screw (D-014)](https://onlyscrews.in/products/m3-x-30mm-hex-allen-socket-head-ss-304-screw-dia-3mm-length-30mm) | 4 | CANDIDATE |
| CH-035 | [M4 × 12 hex-socket button-head SS304 screw](https://onlyscrews.in/products/hex-allen-button-head-m4-x-12-screw-pack-of-20), reported available | 4 | CANDIDATE |
| CH-036 | [M4 SS304 plain hex nut](https://onlyscrews.in/products/m4-nut-ss-304), accessible from below | 4 | CANDIDATE |
| CH-037 | [Ø4 × 8 mm hardened body locating pin](https://onlyscrews.in/products/m4-x-8mm-hard-dowel-pins-dia-4mm-length-8mm) | 2 | CANDIDATE |
| CH-038 | [M3 × 12 Phillips CSK mild-steel black-oxide ballast screw](https://onlyscrews.in/products/m3-x-12mm-phillips-countersunk-csk-mild-steel-black-oxide-screw-dia-3mm-length-12mm) | 2 | CANDIDATE |
| CH-039 | M2 × 5 IMU screw | 2 | CANDIDATE |
| CH-048 | [ISO 7380 M3 × 8 tyre clamp-ring screw](https://onlyscrews.in/products/hex-allen-button-head-m3-x-8-screw-pack-of-20) | 12 | CANDIDATE |
| CH-049 | [M3 × ~4 mm rim heat-set insert](https://onlyscrews.in/products/m3-x-4mm-3d-printing-brass-threaded-inserts-dia-3mm-length-4mm) | 12 | CANDIDATE |
| CH-053 | ISO 7380 M3 × 18 bearing housing and cap screw | 8 | CANDIDATE |
| CH-054 | [M3 × 4 mm motor plate heat-set insert](https://onlyscrews.in/products/m3-x-4mm-3d-printing-brass-threaded-inserts-dia-3mm-length-4mm) | 8 | CANDIDATE |
| CH-055 | [ISO 4029 M3 × 3 cup-point set screw, SS304](https://onlyscrews.in/products/m3-x-3mm-grub-screw-ss304-dia-3mm-length-3mm), faced to 2.5 mm (D-030) | 2 | CANDIDATE |
| CH-056 | [ISO 7380 M3 × 6 wheel-to-stub screw](https://onlyscrews.in/products/hex-allen-button-head-m3-x-6-screw-pack-of-20) | 6 | CANDIDATE |
| CH-057 | [Loctite 222 and 641](https://onlyscrews.in/products/loctite%C2%AE-222-low-strength-thread-sealant-50-ml) | 1 lot | CANDIDATE |
| CH-059 | [ISO 7380 M3 × 10 central hub-cap screw into the tapped stub end](https://onlyscrews.in/products/hex-allen-button-head-m3-x-10-screw-pack-of-20) (D-033; was 12 × M2 × 6) | 2 | CANDIDATE |
| CH-060 | [ISO 7380 M3 × 8 button-head J04 carrier-to-rail screw](https://onlyscrews.in/products/hex-allen-button-head-m3-x-8-screw-pack-of-20) (D-030) | 8 | CANDIDATE |
| CH-061 | [M3, 6 mm axial heat-set J04 rail insert](https://onlyscrews.in/products/m3-x-6mm-3d-printing-brass-threaded-inserts-dia-3mm-length-6mm) | 8 | CANDIDATE |
| CH-062 | M2 × 8 countersunk thread-forming pod lid screw (D-011) | 1 | CANDIDATE |
| CH-063 | CNC Kitchen M3 × 5.7 pod-seat insert for caster (D-011) | 3 | CANDIDATE |
| CH-067 | CNC Kitchen M3 × 5.7 rear-crossmember insert for the keel (D-014) | 4 | CANDIDATE |
| CH-069 | M2 × 10 thread-forming TCRT bezel screw (D-014) | 1 | CANDIDATE |
| CH-070 | M2 × 6 thread-forming wear-shoe screw (D-014) | 1 | CANDIDATE |
| CH-072 | 2.5 × 100 mm nylon zip tie, J10-10 strain relief (D-014) | 1 | CANDIDATE |
| CH-076 | [ISO 7380 M3 × 6 J11A hatch screw](https://onlyscrews.in/products/hex-allen-button-head-m3-x-6-screw-pack-of-20) (D-030) | 4 | CANDIDATE |
| CH-077 | [M3 × 6 frame heat-set insert](https://onlyscrews.in/products/m3-x-6mm-3d-printing-brass-threaded-inserts-dia-3mm-length-6mm), as CH-061: J11A bosses (D-030; the J05/J06/J16 inserts were removed by D-033) | 4 | CANDIDATE |
| CH-078 | 10 mm hook-and-loop pack strap, J11B (D-030) | 2 | CANDIDATE |
| CH-079 | 1.5 mm closed-cell foam cell-end pad, J11B (D-030) | 2 | CANDIDATE |
| CH-080 | M2.5 × 4 heat-set insert in the driver posts, J15B (D-030) | 4 | CANDIDATE |
| CH-081 | M2.5 × 6 low-head driver screw, J15B (D-030) | 4 | CANDIDATE |
| CH-082 | 2.5 × 100 mm nylon zip tie, motor-lead strain relief, J15B (D-030) | 2 | CANDIDATE |

Supplier leads, stock observations, dimensions, standards, materials and fit qualifications are recorded in the fastener rows of the [project BOM](../../BOM.csv).

[D-030](../../decisions.md#d-030) replaces the three unsourceable sizes with stocked standard parts. The DIN 7984 low heads (CH-030, CH-060) become ISO 7380 button heads, with the same 2 mm key and length. The J04 cheek recess widens to Ø5.9 for the Ø5.7 head. The M3 × 2.5 set screw (CH-055) is not a standard length. It becomes a stocked ISO 4029 M3 × 3, faced down 0.5 mm at the hex end. Unmodified, it would stand 0.5 mm proud and sweep only 1.07 mm past the face-screw heads. Faced to 2.5 mm it sits flush and clears them by 1.54 mm.

D-030 also added all the hardware for J05, J06, J16, J11A and J15B; [D-033](../../decisions.md#d-033) later deleted the J05, J06 and J16 hardware by printing each end of the frame as one module. The frame uses one insert article throughout, the CH-061/CH-077 M3 × 6. There are no washers: the button heads seat directly on the printed faces, which keeps the modeled engagement. The OnlyScrews M3 washer (Ø7 × 0.5) can be added later if the stacks are rechecked. All the new screws and inserts have OnlyScrews listings. The strap and foam (CH-078, CH-079) still need a source.

**J13 clamp stack (D-030):** the stack stays M4 × 12 button head, 4 mm body foot, 4 mm deck and a plain M4 nut, with no washer. That leaves 0.8 mm of thread past the nut, more than one 0.7 mm pitch. Loctite 222 (CH-057) on the nut thread is the locking method. A Nyloc would need a longer bolt, and the slim-socket access path was chosen for a plain nut. Head seat, pin fits, nut access and lift-off are still to be checked on received parts. CH-035 and CH-038 lengths are derived from the current modeled joint stacks and still need received-hardware checks. The pictured mixed M3/M4/M5 Phillips-CSK assortment includes M3 × 12 screws, a possible CH-038 source, but its material/grade and head-seat dimensions are not identified in the image. Its M4 × 12 screws are countersunk and do not replace CH-035's button-head screws. Counts above come from modeled positions; heads and shanks in the CAD are one screw each. The axle-stack hardware specifications (CH-053 to CH-057) are defined in [D-007](../../decisions.md#d-007) and the [axle stack](research/axle-stack.md), but the parts are not yet proven on a coupon or the axle rig.

## Full-system electrical parts outside the chassis v1 CAD

These rows describe the **full-system electrical architecture** shown in whole-robot CAD and the electrical plan. PCB-02, PCB-03, PCB-04 and PCB-10 are excluded from [the chassis v1 scoped export](cad/README.md), and are not all prerequisites for a supply-powered chassis bench test. The selected Adafruit driver boards and a temporary controller/harness can support that earlier test if current limits, encoder interface, default disable, physical stop and braking/transient behavior are verified. Keep these shared board rows for full-system integration; their presence here does not make them a chassis-test fabrication requirement. See the test-stage summary below and the release checks in the project BOM.

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-040 | Full-system wiring set | 1 set | HOLD |
| CH-041 | Charge and system power PCB-02 | 1 assembly | HOLD |
| CH-042 | Motor gate and distribution PCB-03 | 1 assembly | HOLD |
| CH-043 | Branch converter PCB-04 | 1 assembly | HOLD |
| CH-044 | C3 carrier PCB-10 | 1 assembly | HOLD |
| CH-045 | ESP32-S3-DevKitC-1-N8 | 1 | CANDIDATE |
| CH-046 | ~~IDEC XA1E-BV3U02KT-R E-stop~~: no E-stop; the rear mushroom is the momentary power button BO-018 ([D-041](../../decisions.md#d-041)) | — | SUPERSEDED |
| CH-047 | C3 carrier M2.5 screw and insert | 4 sets | HOLD |

`PCB-02` manages charge and system power; `PCB-03` provides motor gating and power distribution; `PCB-04` supplies protected voltage rails; `PCB-10` carries the C3 controller. The separate ESP32-S3 DevKit and the rear power button are part of that integrated electrical system; there is no E-stop ([D-041](../../decisions.md#d-041)). The [connector and wire schedule](../../../02-prototypes/RP-06-cad/connector-schedule.md) describes the full-system harness, not a minimal bench harness. Board positions appear in the full Layout 02 model, but not in the chassis v1 filtered STEP. Body and head mass stand-ins are test fixtures and are excluded from installed quantities.

## Release blockers by stage

Pololu #4804 is not the chosen caster and is not a current blocker; the selected caster is #2691. No physical PASS is recorded. Remaining blockers are stage-specific: final joint/fabrication details, purchased-part measurement, nose/rear physical proof, controlled driver commissioning, A21 stop-path timing and range validation, and protected-pack qualification before battery operation.

1. **Provisional coupons and fit prints:** proceed under D-005 with documented motor/interface assumptions and replaceable parts. Choose a trial print process and obtain the hardware relevant to each coupon. Selected parts may be bought to resolve receiving and test gates.
2. **Final fabrication:** frame, hatch, pack-restraint and driver-mount hardware are defined by D-030. Their coupons, pull-out tests and dry runs remain, along with the J13 pin fits on received parts. Release the turned stub drawing/quote, exact unmatched fasteners, print split/material/settings, calibrated fits, per-part exports and assembly/service instructions. Nose and rear retention architecture is defined; its physical proof remains open. Reconcile the Samsung cell spacing and finished-pack envelope before releasing the battery enclosure.
3. **Controlled powered tests:** receive and characterize the selected MOT3001 motors; verify the documented 6 V bench rig, deliberate driver limits, encoder/logic interfaces, retained harness, default disable, physical stop and braking/transient handling. Use secured inert pack/body/head ballast when the cells are disconnected. Record axle fit/retention/runout, loaded clearance, traction, turns, support behaviour, braking/tipping and temperature against defined limits.
4. **Contact/cliff/IMU and autonomous claims:** qualify actual nose springs/magnet/Hall carrier, startup and wire-fault handling, ADC calibration, front-range timing/blind zone, bare-TCRT real-floor/ambient response and motor noise. Resolve the budget IMU runtime interface and mount if adopted. Final PCB-10 fabrication may wait when equivalent temporary interfaces are used; later boards require their own integration checks.
5. **Battery and full-system operation:** qualify the protected 2S pack, insulation/restraint, disconnect/fuse/holder, thermal and charging behaviour, 8.4 V versus 6 V motor control and protection/regeneration interaction. Release only the custom boards/harness actually used in that scope. Their pending design does not block an independent supply-powered test.
6. **Current verification and evidence:** on 2026-10-02 the full `check_layout.py` (119/119), `wheel/check_wheel_on_chassis.py` (6/6), `check_frame_fasteners.py`, `check_battery_ballast.py` and `check_nose_joints.py` all pass against the current source (D-031). Rerun them after any further CAD change. Record the revision, failures/exceptions and physical test results before release. Update supplier/order/receipt/measurements in the project BOM; do not infer any from CAD or stock listings.
