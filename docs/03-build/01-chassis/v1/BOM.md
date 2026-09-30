# Chassis v1 bill of materials — working snapshot

Captured 2026-09-28 from the [project BOM](../../BOM.csv) for **one rolling chassis**. Quantities are installed quantities, with no spare or scrap allowance. This is a procurement and design worklist, **not a released order or fabrication package**. `DESIGN` means custom geometry exists; `CANDIDATE` means a part family or SKU is proposed; `HOLD` means do not order or fabricate until the blocker is resolved; `OPEN` means the design still needs a choice before release. No row is marked received or measured.

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
| CH-011 | Battery tub bottom hatch | 1 | OPEN |
| CH-012 | Turned steel stub: bearing seats, D-shaft bore, flange and spigot ([D-007](../../decisions.md#d-007)) | 2 | DESIGN |
| CH-013 | 9 × 60 × 19 mm steel ballast bar | 1 | DESIGN |
| CH-051 | Printed bearing housing ([D-007](../../decisions.md#d-007)) | 2 | DESIGN |
| CH-052 | 1.2 mm aluminium bearing retaining cap | 2 | DESIGN |

`CH-001` is a **design set**, not a claim that all frame parts are one print. The main CAD now models two deck prints, four rails, two crossmembers, the tub/hatch, and one keyed plate-and-cheek carrier per side. J04 uses separate rail modules with M3 inserts and screws; the material/process, calibrated fits and physical strength still need proof. The guards and wear shoe are modeled as separate objects but have no attachment detail. The wheel is designed in the standalone [wheel CAD](cad/wheel/README.md) ([D-005](../../decisions.md#d-005), [D-008](../../decisions.md#d-008)): a printed TPU tyre clamped by CH-048/CH-049, and a hub cap (CH-058, CH-059) over the D-007 wheel screws. The spin index (formerly CH-006) is removed. The O-ring fallback is recorded in D-005, with no BOM row. The hatch has no retention hardware; its eventual screws or latch must be added to this BOM.

The purchased **Pololu #2691 caster** is a separate row (CH-016). It includes the 1-inch / 25.4 mm plastic ball, plastic rollers, and two-piece housing. The custom printed pod seats its three-hole flange on the chassis crossmember and provides the pocket for the front range sensor; it is a mount, not a second ball or replacement caster. Pololu lists a 29 mm assembled height and says this caster is intended as a third support for differential-drive robots up to about 10 lb. The CAD mass register estimates the complete robot at 2.55 kg (5.6 lb) and assigns about 18% of static weight to the ball, roughly 0.45 kg. That makes the size/load choice plausible for static support. Pololu gives general guidance, not a load rating; the printed pod strength, impacts, floor gaps, and threshold climbing still need physical tests. [CAD mass estimate](cad/generated/mass-properties.md) · [Pololu #2691 specs](https://www.pololu.com/product/2691/specs) · [dimension drawing](https://www.pololu.com/file/0J895/2691-dimensions.pdf).

## Purchased and electrical items

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-014 | [ThinkRobotics MOT3001-6V230RPM encoder gearmotor](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors) ([D-003](../../decisions.md#d-003)) | 2 | HOLD |
| CH-015 | [OnlyScrews 688 ZZ bearing](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5), 8 × 16 × 5 (D-012) | 4 | CANDIDATE; listing says sold out |
| CH-016 | Pololu #2691 1-inch plastic ball with plastic rollers (not #2692) | 1 | CANDIDATE |
| CH-017 | Pololu #4035 DRV8874 carrier | 2 | CANDIDATE |
| CH-018 | Sharp GP2Y0A41SK0F front range sensor | 1 | CANDIDATE |
| CH-019 | TI DRV5055A3 linear Hall sensor (D-013) | 1 | CANDIDATE |
| CH-064 | Nose Hall board, 6.0 × 4.6 × 0.8 mm | 1 | DESIGN |
| CH-065 | N35 Ø2 × 1 mm cap magnet | 1 | CANDIDATE |
| CH-066 | Ø3 × 10 mm cap return spring | 2 | CANDIDATE |
| CH-020 | Rear TCRT5000 with a soldered 350 mm GH4 lead to J10-10 ([spec](rear-tcrt-lead.md), D-016) | 1 assembly | CANDIDATE |
| CH-021 | ICM-42688-P base IMU PCB-07 | 1 assembly | HOLD |
| CH-022 | Samsung INR18650-25R cell | 2 | CANDIDATE |
| CH-023 | Pack protection PCB-01 | 1 assembly | HOLD |
| CH-024 | Bourns AC72ABD resettable thermal breaker | 1 | HOLD |
| CH-025 | SEMITEC 103AT-2 10 kΩ NTC thermistor | 1 | HOLD |
| CH-026 | Cell straps, insulation, heat-shrink sleeve, and AWG16 pack leads | 1 lot | HOLD |
| CH-027 | Micro-Fit+ 1×2 pack disconnect with terminals | 1 pair | HOLD |
| CH-028 | ATOF main fuse holder | 1 | HOLD |
| CH-029 | ATOF 15 A main fuse | 1 | HOLD |

The tact switch is a small button mounted sideways inside the pod. When the flexible nose cap is pushed rearward by contact, it presses the switch plunger; the CAD reserves 3 mm of cap travel. Its exact switch and actuation force are not selected, so contact behaviour is still open.

The battery parts are different functions: two 18650 cells store energy; PCB-01 protects the pack electrically; the **AC72ABD** is a resettable, cell-mounted thermal/current breaker that opens the pack circuit on excessive heat or current (72 °C ± 5 °C trip); the **103AT-2** is a temperature sensor mounted against a cell and wired to the charger’s temperature input so charging can respond to cell temperature. It does not interrupt current by itself. Bourns describes the AC part as a mini-breaker; SEMITEC lists the 103AT-2 as a 10 kΩ thermistor. [Bourns AC series datasheet](https://bourns.com/docs/product-datasheets/ac.pdf) · [SEMITEC AT thermistors](https://www.semitec.co.jp/products/thermistor_at/).

The cell straps connect the cells in the 2S series arrangement; insulation separates conductive tabs and cell surfaces to prevent shorts; the heat-shrink sleeve holds and protects the pack assembly; AWG16 leads carry pack power to the disconnect. The CAD mass estimate includes these as a roughly 11 g pack-build allowance, not as a finished purchased pack. The pack construction and electrical checks remain open.

**ATOF** is Littelfuse’s automotive blade-fuse family. The proposed 15 A ATOF fuse (CH-029) and its holder (CH-028) protect the pack feed against overcurrent. Electrically, the fuse goes after the pack disconnect and before PCB-02, close to the battery source. The current CAD reserves a holder envelope in the +Y channel beside the tub (X 51–75 mm); the electrical spec describes a PCB-mount holder on PCB-02. Those placement descriptions do not yet agree, so the exact holder mounting and service method are still open. [Littelfuse ATOF datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40).

The drive gearmotor is the **ThinkRobotics MOT3001-6V230RPM** ([product page](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors); pick the 6V / 230RPM variant) (a generic JGA25-370, 6 V, about 26:1, 11 PPR Hall encoder, ₹1,180), chosen on cost and in-India availability in [decision D-003](../../decisions.md#d-003). It does **not** meet the RP-03 0.70 m/s heavy-launch gate: estimated 0.47 m/s at the launch load and about 0.20 N·m stall. Chassis v1 therefore runs a reduced drive envelope until bench measurements set it. The screw pattern, tapped depth and gearbox length in the CAD are assumptions until a unit is measured. Fallbacks are the Pololu #4803 and the DFRobot FIT0521. The battery board and other custom electronics are proposed envelopes, not released boards.

## Fasteners and locating hardware

| ID | Joint hardware | Qty | State |
|---|---|---:|---|
| CH-030 | DIN 7984 M3 × 6 low-head motor face screw | 4 | CANDIDATE |
| CH-031 | ISO 7380 M3 × 8 caster screw, from below (D-011) | 3 | CANDIDATE |
| CH-032 | ISO 7380 M3 × 8 pod-to-crossmember screw (D-011) | 2 | CANDIDATE |
| CH-033 | CNC Kitchen M3 × 5.7 front-crossmember insert for ball pod (D-011) | 2 | CANDIDATE |
| CH-034 | ISO 4762 M3 × 30 rear keel screw (D-014) | 4 | CANDIDATE |
| CH-035 | M4 body to chassis through bolt, length open | 4 | HOLD |
| CH-036 | M4 body to chassis nut | 4 | HOLD |
| CH-037 | Ø4 × 8 mm body locating pin | 2 | HOLD |
| CH-038 | M3 ballast mounting screw, length open | 2 | HOLD |
| CH-039 | M2 × 5 IMU screw | 2 | CANDIDATE |
| CH-048 | ISO 7380 M3 × 8 tyre clamp-ring screw | 12 | CANDIDATE |
| CH-049 | M3 × ~4 mm rim heat-set insert | 12 | CANDIDATE |
| CH-053 | ISO 7380 M3 × 18 bearing housing and cap screw | 8 | CANDIDATE |
| CH-054 | M3 × 4 mm motor plate heat-set insert | 8 | CANDIDATE |
| CH-055 | DIN 916 M3 × 2.5 cup-point stub set screw | 2 | CANDIDATE |
| CH-056 | ISO 7380 M3 × 6 wheel-to-stub screw | 6 | CANDIDATE |
| CH-057 | Loctite 222 and 641 | 1 lot | CANDIDATE |
| CH-059 | M2 × 6 thread-forming hub cap screw | 12 | CANDIDATE |
| CH-060 | DIN 7984 M3 × 8 low-head J04 carrier-to-rail screw | 8 | CANDIDATE |
| CH-061 | M3, 6 mm axial heat-set J04 rail insert | 8 | CANDIDATE |
| CH-062 | M2 × 8 countersunk thread-forming pod lid screw (D-011) | 1 | CANDIDATE |
| CH-063 | CNC Kitchen M3 × 5.7 pod-seat insert for caster (D-011) | 3 | CANDIDATE |
| CH-067 | CNC Kitchen M3 × 5.7 rear-crossmember insert for the keel (D-014) | 4 | CANDIDATE |
| CH-069 | M2 × 10 thread-forming TCRT bezel screw (D-014) | 1 | CANDIDATE |
| CH-070 | M2 × 6 thread-forming wear-shoe screw (D-014) | 1 | CANDIDATE |
| CH-072 | 2.5 mm zip tie, J10-10 strain relief (D-014) | 1 | CANDIDATE |

Counts above come from modeled positions; heads and shanks in the CAD are one screw each. Choose exact fasteners, receivers, engagement, and tool access after the printed joint stack is defined. The axle-stack hardware (CH-053 to CH-057) is selected in [D-007](../../decisions.md#d-007) and the [axle stack](axle-stack.md), but it is not yet proven on a coupon or the axle rig.

## Full-system electrical parts outside the chassis v1 CAD

These rows were included as if all were required for a powered chassis test. That was too broad. They are the **full-system electrical architecture** shown in the whole-robot CAD and electrical plan; they are excluded from [the chassis v1 scoped export](cad/README.md), and are not all prerequisites for a bench motor/rolling test. A temporary current-limited supply, a test controller, the two included DRV8874 carriers, and a simple test harness may be enough for that test, but the exact bench setup has not been specified. Keep the shared board rows in the project register for full integration; do not treat them as parts to print with or procure specifically for the chassis until the chosen test setup requires them.

| ID | Part | Qty | State |
|---|---|---:|---|
| CH-040 | Full-system wiring set | 1 set | HOLD |
| CH-041 | Charge and system power PCB-02 | 1 assembly | HOLD |
| CH-042 | Motor gate and distribution PCB-03 | 1 assembly | HOLD |
| CH-043 | Branch converter PCB-04 | 1 assembly | HOLD |
| CH-044 | C3 carrier PCB-10 | 1 assembly | HOLD |
| CH-045 | ESP32-S3-DevKitC-1-N8 | 1 | CANDIDATE |
| CH-046 | IDEC XA1E-BV3U02KT-R E-stop | 1 | CANDIDATE |
| CH-047 | C3 carrier M2.5 screw and insert | 4 sets | HOLD |

`PCB-02` manages charge and system power; `PCB-03` provides motor gating and power distribution; `PCB-04` supplies protected voltage rails; `PCB-10` carries the C3 controller. The separate ESP32-S3 DevKit and E-stop are part of that integrated electrical system. The [connector and wire schedule](../../../02-prototypes/RP-06-cad/connector-schedule.md) describes the full-system harness, not a minimal bench harness. Board positions appear in the full Layout 02 model, but not in the chassis v1 filtered STEP. Body and head mass stand-ins are test fixtures and are excluded from installed quantities.

## Release blockers

1. For provisional CAD and fit prints, document the supplier-derived motor assumptions and keep the motor plate/coupling replaceable under [D-005](../../decisions.md#d-005); no motor is currently on hand. Before a powered rolling chassis is marked passed, assemble the selected MOT3001-6V230RPM units, confirm physical fit and run the [D-003](../../decisions.md#d-003) bench tests to set the drive envelope. Verify other purchased interfaces against their actual parts as they become available; update dependent geometry if a fit fails.
2. Resolve every load-bearing joint: print split/material, wheel and stub retention, bearing preload, body M4 clamp stack, caster and pod screw engagement, keel receiver, hatch retention, and wear-piece attachment. Add any resulting parts to the project BOM and refresh this snapshot.
3. Release the custom PCBs and harness from electrical schematics, layouts, exact connector part numbers, pinouts, and bench checks. Specify a safe pack builder and electrical test.
4. Rerun chassis-specific CAD and physical fit checks, then set and pass the [build tests](../../README.md). Record supplier, order, receipt, measured dimensions, and any approved substitute in the project BOM before marking this snapshot released.
