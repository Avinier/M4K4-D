# 03 — Build decision ledger

The central record of every decision and change made during the build phase. Newest entries go at the bottom. Each entry states what was decided, why, what changed (docs, BOM, CAD), what is still unverified, and the next action. Supersede an entry with a new one instead of rewriting it.

`02-prototypes/` is read-only reference ([D-001](#d-001)); earlier RP decisions are linked, not copied or edited.

| ID | Date | Area | Decision | Status |
|---|---|---|---|---|
| [D-001](#d-001) | 2026-09-28 | Governance | `03-build/` governs; `02-prototypes/` is read-only reference | ACTIVE |
| [D-002](#d-002) | 2026-09-28 | Chassis / drive | DFRobot FIT0521 as drive gearmotor | SUPERSEDED by D-003 |
| [D-003](#d-003) | 2026-09-28 | Chassis / drive | Drive gearmotor: ThinkRobotics MOT3001-6V230RPM, with a reduced drive envelope | ACTIVE; inventory/workflow corrected by D-005 |
| [D-004](#d-004) | 2026-09-29 | Chassis / wheels | Wheel rim and tyre: six-spoke PETG rim with a clamped TPU tyre (A) or three O-rings (B) | SUPERSEDED by D-005 |
| [D-005](#d-005) | 2026-09-29 | Chassis / wheels | Wheel: TPU chevron tyre on a restyled clamped rim; O-rings as fallback only; spin index removed | ACTIVE for tyre, retention and fallback; face styling superseded by D-006 |
| [D-006](#d-006) | 2026-09-29 | Chassis / wheels | Wheel face: five swept blade spokes after builder references; round 5-screw clamp ring | SUPERSEDED by D-008 |
| [D-005](#d-005) | 2026-09-29 | Chassis / motor interface | No motor on hand; proceed with documented assumptions and replaceable interface | ACTIVE |
| [D-007](#d-007) | 2026-09-29 | Chassis / axle | Axle stack architecture: turned steel stub, paired bearings, set-screw motor coupling, floating motor | ACTIVE for architecture; bearing selection superseded by D-012; HOLD on quote, coupons, rig and motor receipt |
| [D-008](#d-008) | 2026-09-29 | Chassis / wheels | Wheel face: six framed spokes, 12-sided vented beadlock ring and a proud hex hub cap, after the builder's reference; hub on the D-007 interface | ACTIVE, HOLD with D-005 and D-007 |
| [D-009](#d-009) | 2026-09-29 | Chassis / wheels | Handed left/right tyres; D-008 wheel merged into chassis-v1 as the single wheel source | ACTIVE; full `check_layout.py` rerun pending |
| [D-010](#d-010) | 2026-09-29 | Chassis / axle/frame | Keyed single-print motor carriers join to split rails through J04 | ACTIVE for J04; bearing selection superseded by D-012; HOLD on fit coupons, full clearance rerun and physical rig |
| [D-011](#d-011) | 2026-09-30 | Chassis / nose (J07, J08) | Ball-transfer nose closed in CAD: caster screwed from below into seat inserts, sliding snap-retained touch cap on a constant nose, ESE22MV21 switch, screwed lid, J10-8 cable exit | ACTIVE; switch superseded by D-013; HOLD on received-caster measurement, coupons and physical tests |
| [D-012](#d-012) | 2026-09-30 | Chassis / axle | Select 688 ZZ, 8 × 16 × 5, from the OnlyScrews listing; revise paired-bearing seats | ACTIVE; HOLD on supplier stock/lot evidence, drawing/load data, fit coupons, clearance rerun and retention test |
| [D-013](#d-013) | 2026-09-30 | Chassis / nose (J08) | Nose contact sensing: DRV5055 linear Hall sensor and cap magnet, firmware trip at about 0.7 mm; replaces the D-011 ESE22MV21 switch; cap return springs | ACTIVE; HOLD on bench trip-point check and the PCB-10 J10-8 pin change |
| [D-014](#d-014) | 2026-09-30 | Chassis / rear keel (J09, J10) | Rear TCRT keel closed in CAD: M3 × 30 into crossmember inserts, bezel-and-shim TCRT retention with ±2 mm height, dovetail shoe, J10-10 disconnect at the keel with a route behind the crossmember | ACTIVE; HOLD on CH-020 breakout, CH-009/CH-010 materials, coupons and physical tests |
| [D-015](#d-015) | 2026-09-30 | Chassis / rear TCRT (CH-020, J09B) | Custom passive TCRT board that floats on the seated sensor; J10-10 becomes +3V3, GND, TCRT_OUT (ADC), LED_EN | SUPERSEDED by D-016 |
| [D-016](#d-016) | 2026-09-30 | Chassis / rear TCRT (CH-020, J09B) | No board: TCRT soldered to a GH4 lead that plugs into C3 J10-10; LED switch and load on PCB-10 | ACTIVE; HOLD on the PCB-10 J10-10 change and bench item 20 |
| [D-017](#d-017) | 2026-09-30 | Chassis / rear keel wear parts (CH-009, CH-010) | Recommendation: PETG for the wear shoe and the TCRT bezel; UHMW-PE tape on the shoe as an optional upgrade | RECOMMENDED; confirm after the item 20–22 tests |
| [D-020](#d-020) | 2026-09-30 | Chassis / nose springs (CH-066) | Industrybuying RS PRO 821245 selected for purchase; retain 9/6 mm installed gaps pending force and guidance tests | SELECTED; higher preload, cap force, buckling and hook retention unverified |
| [D-021](#d-021) | 2026-09-30 | Chassis / rear floor sensor (CH-020) | Bare Vishay TCRT5000 selected; Robu comparator module excluded from the designed keel interface | SENSOR SELECTED; supplier provenance, assembly fit and floor/cliff validation open |
| [D-022](#d-022) | 2026-09-30 | Chassis / fastener sourcing | Use best available supplier candidates after OnlyScrews checks; define J12/J13 nominal screw stacks | Superseded in part by D-023 |
| [D-023](#d-023) | 2026-09-30 | Chassis / fastener availability update | CH-035 and CH-038 reported available; CH-030/055/060 remain unsourced | Superseded in part by D-024 |
| [D-024](#d-024) | 2026-09-30 | Chassis / remaining fastener source leads | ACME low-head screw family and Dalloyed grub-screw family added as Indian quote/sample leads | OPEN; exact size/stock still to confirm |
| [D-025](#d-025) | 2026-09-30 | Chassis / mixed CSK fastener assortment | Mixed M3/M4/M5 kit may cover CH-038; M4 CSK does not fit CH-035 | CANDIDATE; kit source/material and fit unverified |
| [D-026](#d-026) | 2026-09-30 | Chassis / battery and ballast CAD (CH-022, CH-038, J12) | BOM and CAD reconciled: 1.1 mm cell gap, countersunk CH-038 seat, 350 mm TCRT mass note; chassis-v1.step rebuilt | ACTIVE; PCB-01 height, received-screw fit and full `check_layout.py` rerun open |
| [D-027](#d-027) | 2026-09-30 | Chassis / purchased-part models (CH-017, CH-018; J08A/J08C) | Vendor STEP for the A21 and a board-file STEP for the #3297 replace boxes; A21 ears trimmed, lead soldered, nose lid/cap reworked for the real package | ACTIVE; received-unit fit, ear trim and lead strain relief open |
| [D-028](#d-028) | 2026-10-01 | Chassis / battery tub interfaces (J11A, CN-05) | Shell opening sized to the hatch; front hatch bosses moved onto the tub front wall; bosses cut to Z 39.5 and the pack disconnect lifted 3 mm; IMU screw overlap recorded as accepted | ACTIVE; `check_layout.py` 116/119 (three D-027 failures open); boss and insert fit unproven |
| [D-029](#d-029) | 2026-10-01 | Chassis / nose lid (J08) | GP2Y soldered-lead reserve 3.0 to 2.0 mm, so the lid hump (top Z 57.6) clears the front panel's lift-off path | ACTIVE; lead bend in 2 mm to confirm at assembly |
| [D-030](#d-030) | 2026-10-01 | Chassis / frame fasteners, pack restraint, driver mounts (J05, J06, J11A, J11B, J12, J13, J15B, J16; CH-030, CH-055, CH-060) | J05/J06 inserts moved into the rail tongues; all frame, hatch and driver hardware modeled and added (CH-073–CH-082); pack strapped to the hatch; DIN 7984 → ISO 7380; set screw = M3 × 3 faced to 2.5 | ACTIVE; HOLD on coupons, strap/foam source and physical tests |
| [D-031](#d-031) | 2026-10-02 | Chassis / driver boards (J15B), inline motor pairs, motor face screws | #3297 boards turned long side along Y at X 38.5–56.3, posts at X 41.05; inline pairs re-placed; face-screw heads modelled as ISO 7380 domes; `check_layout.py` 119/119 | ACTIVE; supersedes the D-030 J15B layout; post coupon and received-board fit open |
| [D-032](#d-032) | 2026-10-02 | Chassis / main fuse holder (CH-028) | Inline Littelfuse 0FHA0001ZXJ ATO holder on a printed front-deck bracket above the +Y channel; the old channel envelope could not hold any ATO fuse | ACTIVE; CH-028 HOLD for an India source |
| [D-033](#d-033) | 2026-10-02 | Chassis / frame print units and hub cap (J03, J05, J06, J16; CH-001, CH-012, CH-058, CH-059, CH-073–CH-075, CH-077) | Each frame end printed as one module (deck + rails + crossmember), removing J05/J06/J16 and ten screws and inserts; hub cap held by one central M3 into the tapped stub end instead of six M2 | ACTIVE; HOLD on module print orientation, junction coupons and cap retention; full `check_layout.py` not rerun |
| [D-034](#d-034) | 2026-10-03 | Body / audio speaker (BO-001; BO-002–BO-006 registered) | Speaker: Visaton K 50 WP 8 Ω (art. 2915), element14 India 1683894; body audio chain entered in the project BOM | ACTIVE; speaker SELECTED, not ordered; HOLD on received-part measurement and bench listen |
| [D-035](#d-035) | 2026-10-03 | Body / audio bench amplifier (BO-007) | SmartElex MAX98357A I²S breakout (Robocraze) as the bench amplifier until PCB-05 exists | ACTIVE; SELECTED, not ordered; bench only |
| [D-036](#d-036) | 2026-10-03 | Body / audio microphones (BO-012, BO-005) | Mic IC: Infineon IM73D122V01XTMA1, element14 India 4125831; four-mic array (two per ADAU7002 lane), not six | ACTIVE; SELECTED, not ordered; HOLD on PCB-06 layout and the array tap test |
| [D-037](#d-037) | 2026-10-03 | Body / microphone mounting (BO-005, BO-006, BO-013, BO-014) | Mic boards mount on gasketed shell bosses with two M2 thread-forming screws and a soldered GH lead, not on the frame | ACTIVE; DESIGN; HOLD on boss coupon and PCB-06 layout |
| [D-038](#d-038) | 2026-10-03 | Power boards (PCB-01, PCB-03, PCB-10; CH-017, CH-023, CH-041–CH-043; CH-083–CH-086 registered) | PCB-03 drive feed re-specified for the DRV8833: SMBJ8.5A bus TVS, VM entry, AND-gate sleep, latched FLT, INA181 feed monitors; TIFPS0629 bench acceptance window; 04-pcbs home and board register; PCB-12 assigned to the C2 head carrier | ACTIVE; DESIGN; HOLD on TIFPS0629 bench acceptance and MOT3001 winding R/L |

Status words: `ACTIVE` is in force, `SUPERSEDED` names its replacement, and `HOLD` names the evidence that must arrive before dependent work is released.

---

## D-001

**2026-09-28 · Governance · ACTIVE**

**Decision:** from this date, `docs/03-build/` is the governing context. Every new decision, part selection, BOM change and CAD edit is recorded in `03-build/`, in the subsystem and version folder it belongs to, and logged in this ledger. `docs/02-prototypes/` (all RPs, including RP-03 locomotion and RP-06 CAD) is read-only reference. Where an RP document disagrees with `03-build/`, `03-build/` wins.

**Changed:** [README.md § Governing context](README.md#governing-context).

**Note:** chassis v1 CAD still reads purchased STEPs and the Layout 04 head from `02-prototypes/RP-06-cad` by path ([cad/README.md](01-chassis/v1/cad/README.md)). Reading them is allowed; moving or copying them is a `03-build/` change and gets its own entry.

---

## D-002

**2026-09-28 · Chassis / drive (CH-014) · SUPERSEDED by [D-003](#d-003)**

DFRobot FIT0521 (6 V, 34:1, 3.2 A stall) was briefly the working choice on budget. It was dropped the same day: TME India had stock, but DigiKey quoted a lead time of about 9 weeks, and the builder chose the in-India ThinkRobotics part instead. Its CAD and BOM changes were replaced by D-003.

---

## D-003

**2026-09-28 · Chassis / drive (CH-014) · ACTIVE, HOLD on receipt measurements**

**Decision:** the chassis v1 drive gearmotor is the **ThinkRobotics MOT3001-6V230RPM**, "25mm DC Metal Encoder Gearmotor", 6 V / 230 rpm variant, ₹1,179.99, in stock ([product page](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors)). It is a generic JGA25-370 with an 11 PPR Hall encoder on the motor shaft. It replaces the Pololu #4804 (about ₹5,956 in India) and the FIT0521 (D-002), and was chosen by the builder on cost and in-India availability.

**Performance accepted:** this motor **does not meet** the RP-03 drive gate ([gearmotor-sku-decision.md](../02-prototypes/RP-03-locomotion/gearmotor-sku-decision.md)): at least 159.2 rpm at 0.110 N·m (0.70 m/s heavy launch on the Ø84 wheel), and at least 0.220 N·m stall. ThinkRobotics does not tabulate the 230 rpm variant. The figures below are linear-motor estimates (`E`) from the family data: about a 6,000 rpm base, 1.8 A stall at 6 V, and stall torque about 0.08 kg·cm per unit of ratio. They imply about 26:1 and about 2.1 kg·cm stall.

| Case, 6 V motor | Speed at 0.110 N·m heavy launch | Speed at 0.063 N·m nominal load | Stall torque |
|---|---:|---:|---:|
| 6.0 V at motor | about 107 rpm (0.47 m/s) | about 160 rpm (0.70 m/s) | about 0.20 N·m (fails ≥0.22) |
| 5.3 V at motor (nearly empty pack) | about 80 rpm (0.35 m/s) | about 133 rpm (0.58 m/s) | about 0.18 N·m |

**Consequence:** plan chassis v1 around a **reduced drive envelope** until measured: about 0.5 m/s cruise at nominal load, gentler launch and acceleration limits, and a stall margin below the 2× rule. Heavy-mass launch, threshold climbing and slope hold at full ballast are the tests most likely to fail. The 0.70 m/s RP-03 target is not claimed for v1. Good side effects: 1.8 A stall suits the DRV8874 and the 5 A bench supply, and 11 × 26 × 4 ≈ 1,140 encoder counts per wheel revolution is enough for creep and hold.

**Motor availability:** no motor is currently on hand. A MOT3001-**6V170RPM** was considered as a possible lower-speed bench stand-in, but it has not been procured and is not available for fit, encoder or firmware tests. The selected MOT3001-6V230RPM units also remain to be ordered.

**CAD changed** ([body_chassis_model.py](01-chassis/v1/cad/body_chassis_model.py)):

- The motor is modelled parametrically from the ThinkRobotics/JGA25 drawing (no vendor STEP): Ø25 gearbox (21 mm assumed; the drawing gives 19–27 mm by ratio), Ø24.4 × 31 mm can, encoder board with a rearward 6-pin connector, Ø7 × 2.5 bushing boss, and a Ø4 D-shaft 12.0 mm from the faceplate (was 12.5 on the #4804) with an 8 mm flat. Faceplate to encoder end is about 61 mm (was 66.5).
- Axle flange, 2 mm diaphragm, 608 pair and stub shaft are unchanged. The shaft engages the stub for 8.0 mm (was 8.5).
- Face screws keep 2 × ISO 10642 M3 × 8 at ±8.5 mm. That pattern and the 5 mm tapped depth are **assumptions**; the drawing does not give them.
- The motor pigtail reserve is extended rearward to X −21 to meet the connector.
- Mass register: MOTOR_L/R 101 g at |Y| 39.2 → 110 g at |Y| 40.2. The 110 g is the NFP-JGA25-370-EN figure for this platform; ThinkRobotics lists a 130 g shipping weight. Weigh on receipt.
- Check results: _pending the full rerun_.

**BOM changed:** CH-014 in [BOM.csv](BOM.csv) and [01-chassis/v1/BOM.md](01-chassis/v1/BOM.md).

**Release holds and next actions:**

1. Order two MOT3001-6V230RPM plus one spare.
2. When a motor is received, measure face hole spacing, thread and depth; gearbox length; shaft protrusion and D-flat; connector position and cable exit; and mass. Verify those measurements against the CAD assumptions and update the model if anything differs.
3. Bench test on a current-limited supply: no-load speed and current at 6.0 V and 5.3 V to confirm the winding and ratio; speed under a known 0.063 N·m and 0.110 N·m load; encoder counts per output revolution; a brief current-limited stall. Record the measured drive envelope here and set the firmware speed and acceleration limits from it.
4. Run the chassis heavy-launch, threshold and slope-hold tests at representative ballast early. If they fail, open a new entry. Fallbacks, in order: Pololu #4803 (₹5,956, passes with margin) or FIT0521 (TME India).

---

## D-004

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-006, J14) · SUPERSEDED by [D-005](#d-005)**

**Decision:** the drive wheel is a PETG six-spoke rim carrying one of two tyres. The builder asked for a rugged look, a simple build, and one printed and one non-printed rubber option. A later entry picks one variant from test results.

- **Variant A, printed:** a TPU 95A tyre with two staggered rows of lugs. It is keyed to 12 ribs on the rim seat and clamped between an integral inboard lip and a bolt-on outboard ring by 6 × ISO 7380 M3 × 8 screws into heat-set inserts. The tyre can be changed without removing the wheel.
- **Variant B, bought:** three 70 × 5 mm NBR 70A O-rings stretched 5.7% into grooves on a one-piece rim. No hardware.
- **Spin index:** a paint-filled notch in one spoke instead of a separate inlay.

**Why:**

- **A smooth ring on a smooth rim was never a joint.** Positive keying plus side clamping (A), or a stretched seal in a groove (B), are the simplest retention methods that don't rely on glue.
- **The clamp ring makes the tyre serviceable in place** (CON-P01).
- **O-rings need no flexible printing at all.** They cover the case where the lab can't print TPU.

**CAD added:** the standalone [wheel CAD](01-chassis/v1/cad/wheel/README.md) (`wheel_model.py`, three STEP entries, `check_wheel.py`, 26/26 measured checks passing). It keeps the chassis Ø84 × 24 envelope, the R18 boss pocket and the Ø8 stub bore. **The chassis model and `chassis-v1.step` are not changed**, and still show the placeholder tyre. Mass at solid density: A 90.0 g, B 80.8 g, against 89 g in the chassis register.

**BOM changed:** CH-004/005/006 set to DESIGN. Added CH-048 (screws), CH-049 (inserts) and CH-050 (O-rings); only the chosen variant's hardware is bought.

**Unverified:** TPU print allowances (bore Ø73.6, width 19.3), O-ring cord thinning (estimated OD 83.7), loaded radius, grip, creep at stall, left/right OD match and runout. The stub-to-hub torque joint (J03) is still open; the R4 bore is a placeholder.

**Next actions:**

1. Confirm whether the 3D lab can print TPU 95A. If not, variant B is the only option.
2. Print one rim of each variant plus the tyre coupon. Measure loaded radius at about 1 kg, μ on S-TILE/S-LAM/S-RUG, stall-torque creep and runout.
3. Choose the variant in a new entry. Then port it into `wheel_assembly()` in the chassis model, replace `loaded_radius_matches_axle_height` with the measured radius, and rerun the chassis checks.

---

## D-005

**2026-09-29 · Chassis / motor interface · ACTIVE**

**Correction:** the builder has **no motor on hand**. A 6V170RPM unit had been mentioned as a possible bench stand-in, but it was not purchased or available for measurement. The 6V230RPM motor selection and reduced drive-envelope estimate remain the working choice; all motor fit and performance checks await receipt of hardware.

**Design direction:** continue chassis engineering from the supplier drawing and clearly labeled CAD assumptions. Put the uncertain face-hole/pilot/shaft interface in replaceable or adjustable parts so a mismatch does not force a complete frame reprint. The [motor interface sheet](01-chassis/v1/research/motor-interface-sheet.md) is parked, and the [mechanical checklist](01-chassis/v1/research/engineering-checklist.md) no longer includes a motor-measurement task.

**Limit:** an assumed interface can support a provisional CAD and fit print, but it is not evidence of physical motor fit, safe shaft coupling, or drive performance. Those remain unverified until actual hardware is assembled and tested. No motor-dependent part is marked physically passed by this decision.

**Next:** engineer the frame split and replaceable carrier/plate (J04/J01), then revise the axle stack and wheel hub with explicit assumption ranges and service access.

---

## D-005

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-006, CH-050, J14) · ACTIVE, HOLD on lab TPU capability and grip/retention tests**

**Decision:** the builder chose the printed TPU tyre from D-004. It is the only modelled wheel. Three further changes come with it:

- **Tread:** the plain lugs are replaced by a chevron tread: 18 V-lugs 1.5 mm tall, bars at 40° to the axle, apexes on the tyre centre line. Below about 37°, the Vs leave gaps on the contact line and the wheel bumps 18 times per revolution; the check caught 18 of 72 angles open at 30°.
- **Outboard face, restyled to the droid's shell language** ([vision](../00-foundation/vision.md#character-and-visual-direction), RP-01 D-07 stepped panels):
  - six windows in a 1.5 mm stepped surround, leaving stepped spokes 10 mm wide at the root with a 6 mm crest;
  - a two-step hex hub;
  - a 12-sided beadlock-style clamp ring with a flat facing each screw.
- **Spin index removed:** no notch, no paint and no part. CH-006 is deleted.

Retention is unchanged from D-004: 12 seat ribs, an inboard lip, and a clamp ring with 6 × M3 × 8 button heads into heat-set inserts.

**Fallback, recorded here only (not modelled, no BOM row):** if the 3D lab can't print TPU 95A, use a one-piece PETG rim with three grooves, 5.4 mm wide and 2 mm deep, with a Ø74 bottom and Ø78 lands, at y −7.1 / 0 / +7.1 mm. Fit three **70 × 5 mm NBR 70 Shore A O-rings**, stretched 5.7%; the cord is 36% seated and about 83.7 mm OD mounted. No hardware; the O-rings roll off to replace them. If they creep in the groove, put a drop of CA glue in each groove. D-004 checked this geometry (all 12 O-ring check rows passed).

**CAD changed:** in the [wheel CAD](01-chassis/v1/cad/wheel/README.md), the O-ring model, the variants entry and the index were removed. The single entry is now `wheel.step.py`, and `check_wheel.py` passes 18/18. The checks now also cover spoke section, clamp-ring corners, hub cap and chevron contact continuity. Mass at solid density is 93.7 g per wheel, against 89 g in the register. The chassis model is still not changed.

**BOM changed:** CH-004 and CH-005 re-specified. CH-006 and CH-050 deleted. CH-048 and CH-049 are no longer marked as variant-only.

**Next actions:**

1. Confirm the lab can print TPU 95A (direct-drive extruder).
2. Print a rim, a clamp ring and a tyre coupon. Measure fit, loaded radius at about 1 kg, μ on S-TILE/S-LAM/S-RUG, stall creep and runout.
3. Port the wheel into `wheel_assembly()` in the chassis model. At the same time: remove the placeholder index inlay, update the mass register (+4.7 g per wheel) and the loaded-radius check, and rerun the chassis checks.

---

## D-006

**2026-09-29 · Chassis / wheels (CH-004, CH-048, CH-049) · SUPERSEDED by [D-008](#d-008)**

**Decision:** the builder found D-005's six stepped spokes too plain and supplied three reference wheels: automotive five-spoke rotor designs with swept, faceted, two-tone blades. The rim face now follows them:

- **Blades:** five blades, each leaving a whole flat of a pentagon hub. The straight leading edge sweeps 30°; the trailing edge kinks at R20 and flares, so each blade covers 48° at the rim and leaves a 24° window.
- **Two-level face:** each blade face is split by a ridge. The leading band stays at full height, and the trailing flank slopes 15° down, to about 4.3 mm at the flare corner. This gives two tones under light, and takes a two-tone paint finish if wanted.
- **Details:** a through-slot in each flare, and a round cap on the hub.
- **Clamp ring:** round, not 12-sided, so the face reads as one clean lip as in the references. It now uses **5** M3 button heads, one mid-window, matching the five blades.

Tyre, tread, rib keying and the O-ring fallback are unchanged from D-005.

**Why the numbers:**

- **15° flank, not 20°:** the wider flare would otherwise fall below 2.5 mm at its trailing corner.
- **Five screws still clamp the full bead:** the ring covers the tyre side by 2 mm all round.

**CAD changed:** `wheel_model.py` and `check_wheel.py` in the [wheel CAD](01-chassis/v1/cad/wheel/README.md). The spoke checks now cover the blade solid on its ridge, flank thickness ≥ 2.5 mm (measured 4.3) and the leading band at full height. **20/20 pass.** Mass at solid density is **88.5 g per wheel**, against 89 g in the register, so the D-005 register update is no longer needed. The chassis model is not changed.

**Print impact:** the rim still prints outer face down, because the hub cannot float over the inboard dish. The 15° flanks are then shallow overhangs and need tree supports.

**BOM changed:** CH-004 and CH-005 re-specified; CH-048 and CH-049 quantities go from 12 to 10.

---

## D-007

**2026-09-29 · Chassis / axle (CH-012, CH-015, CH-030, CH-051–CH-057; J01, J02, J03) · ACTIVE, HOLD on shop quote, fit coupons, axle rig and motor receipt**

**Decision:** the builder accepted the [axle stack](01-chassis/v1/research/axle-stack.md) architecture and its three choices: the bearing change, the turned one-piece stub, and designing around an absent motor. Per side, the stack is:

- **Stub.** One turned EN8 part carries torque and locates the wheel. It has Ø8 k5 bearing seats, a Ø4.05 bore on the motor's D-shaft (8 mm engagement), a DIN 916 M3 × 2.5 set screw on the flat, a Ø24 flange with three tapped M3, and a Ø10 spigot that centres the wheel.
- **Bearings.** Two **MR148ZZ** (8 × 14 × 4) in a bolt-on printed housing, held between a housing shoulder and a 1.2 mm aluminium cap. Four M3 × 18 screws pass through cap and housing into heat-set inserts in a 5 mm motor plate.
- **Motor alignment.** The motor floats on 0.3 mm of clearance at its pilot and face screws. The face screws are tightened last, through key slots, once the motor has aligned itself to the stub.
- **Wheel.** Three M3 × 6 screws through the web into the stub flange. Removing the wheel needs only those three screws.

**Why:**

- **The modelled stack was not buildable** ([axle-stack.md §1](01-chassis/v1/research/axle-stack.md#1-why-the-previous-stack-could-not-be-built-as-modelled)): no torque path motor → stub → wheel, no bearing retention, an over-constrained motor, and screw heads buried behind the bearings.
- **608ZZ does not fit.** A 608 pair is 14 mm wide, so it cannot sit inside the fixed Ø84 × 24 wheel together with a coupling and a flange.
- **A 678ZZ is not a substitute.** It is 8 × 12 × 3.5, not 8 × 14 × 4.

**Review holds from the proposal, and how the model now answers them:**

1. **Bearing designation** → MR148ZZ, not 678ZZ. CH-015 still needs the exact supplier article and drawing.
2. **Set screw breaking out of the stub end** → the stub now starts at |Y| 73 (1.5 mm off the motor pilot, in a 2.5 mm plate recess). The hole at 75.7 leaves 1.2 mm of steel to the end and 1.3 mm to the bearing seat. The M3 × 2.5 cup point sits flush with the Ø8.
3. **Edge margins** → four cap screws on the diagonals at R 12. The insert is ≥ 4.5 mm from the plate edges. The housing is Ø32, leaving 2.3 mm of wall outside each hole. The face-screw key paths now open into the bearing bore as slots at 0°/180°, instead of leaving a 0.2 mm skin. The slots sit off the vertical load line.
4. **Outward thrust on the inner rings** → still a k5 press fit plus Loctite 641; there is no room for a circlip. Required: 100 N outward hold, about 4× the load of lifting the robot by one wheel. Over 2 × π × 8 × 4 mm² of seat, that is 0.5 N/mm², far below any retaining compound's rated shear. **Not proven**: the axle rig includes a 100 N outward pull test.
5. **Screw-tip clash** → the wheel screws are M3 × 6, flush at the flange's inner face. A new check sweeps each rotating screw as a full ring: all are ≥ 1.55 mm clear.
6. **Fits** → all remain provisional until coupons (housing bore, spigot bore, inserts) and a quote.
7. **Shop quote** → still needed before ordering.
8. **Alignment proof** → axle-rig items: runout, drag and no-load current before and after tightening the face screws.

**Motor assumptions carried** ([D-005 motor interface](#d-005)): M3 face holes at ±8.5 mm, 5 mm deep; Ø7 × 2.5 pilot; Ø4 shaft 12 mm long with an 8 mm flat. The motor plate is the only part that encodes the face pattern. If the received motor differs, reprint the plate (or the carrier, J04). The stub's bore and set-screw position are the only turned features that depend on the shaft.

**CAD changed** ([body_chassis_model.py](01-chassis/v1/cad/body_chassis_model.py)):

- The flange/boss/diaphragm is replaced by `AXLE_MOTOR_PLATE`, `AXLE_BEARING_HOUSING` and `AXLE_BEARING_CAP`, plus the cap screws and inserts.
- New stub, set screw and wheel screws. The 608 STEP is replaced by parametric MR148 rings.
- The wheel pocket floor moves to |Y| 93, and the hub bore is Ø10 with 3 × Ø3.4 holes at PCD 16.
- Checks: `motor_face_joint_is_engaged` now requires ≥ 6 mm of shaft engagement. New checks: `axle_stack_is_retained`, `rotating_screws_swept_clear`, `bearing_model_is_mr148zz`. The old boss and 608 checks are removed.
- Mass register: frame +20.9 g, wheels −1.7 g each, axle row 64.4 → 44.0 g; all at the axle line.
- Check results: _pending the full rerun_.

**Interface for the standalone wheel CAD** ([D-005](#d-005)/[D-006](#d-006), [wheel model](01-chassis/v1/cad/wheel/README.md)): the wheel must now take the stub, not an Ø8 bore.

- Pocket R 18 to |Y| 93 (the web runs 93–97).
- Ø10 H7 bore through the web.
- 3 × Ø3.4 holes at PCD 16, clocked 30°/150°/270°.
- A flat seat for three ISO 7380 heads (Ø5.7) on the outer hub face.

The wheel model has not been changed by this entry.

**BOM changed:** CH-012 re-specified and set to DESIGN. CH-015 changed 608ZZ → MR148ZZ. CH-030 changed ISO 10642 M3 × 8 → DIN 7984 M3 × 6. Added CH-051 (housing), CH-052 (cap), CH-053 (M3 × 18 ×8), CH-054 (inserts ×8), CH-055 (set screws), CH-056 (M3 × 6 wheel screws ×6), CH-057 (Loctite 222/641).

**Next actions:**

1. Dimensioned stub drawing, then a quote from a local turning shop.
2. Print coupons: MR148 bore Ø13.90–14.10 in 0.05 mm steps; spigot bore Ø9.9–10.1; M3 × 4 insert holes; a plate section with counterbores.
3. Port the stub interface into the wheel model.
4. J04: the motor carrier and frame split.
5. Axle rig on receipt of the motor, with limits set before testing: runout ≤ 0.3 mm TIR, end play ≤ 0.1 mm, 100 N outward hold, drag and current before and after face-screw tightening, 200 reversals with set-screw paint marks.

---

## D-008

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-048, CH-049, CH-058, CH-059; J14) · ACTIVE, HOLD with D-005 and D-007**

**Decision:** the builder chose this face over D-006's five-blade design. Two sessions had been restyling the wheel in parallel. D-006 was logged, but the CAD on disk became this design, and the builder confirmed this one. The design follows the builder's reference image: a 12-sided bolted beadlock, framed spokes, and a screwed hex hub cap. The tyre, chevron tread, rib keying and O-ring fallback are unchanged from D-005.

- **Spokes:** six framed spokes, 10 mm at the root, chamfered 1.5 × 1.5 to a 7 mm face, each with a recessed slot 3 mm wide and 2 mm deep. They run from a 26 mm hex hub, flats facing the spokes, to an inner ring with a 45° inner bevel. A 1 mm shadow groove sits between the inner ring and the clamp ring.
- **Clamp ring:** 12 sides, with six M3 × 8 screw flats (CH-048/049 back to 12 per robot) alternating with six recessed vent slots. The corners are chamfered and the flats are not.
- **Hub on the D-007 interface:**
  - the R18 pocket floor is at |Y| 93, over the bearing housing;
  - the web is 4 mm, with a Ø10 H7 bore on the stub spigot;
  - three Ø3.4 holes at PCD 16 (30/150/270° from +X) take the D-007 M3 × 6 button heads (CH-056) into the stub flange.

  Inside the pocket the spokes shrink to the 4 mm web, and the slot floor there is 2 mm.
- **Hub cap (new CH-058, CH-059):** a dark PETG hex cap, 26 mm across flats, with a faceted 16 mm boss. It stands 3 mm proud of the face (4.3 mm including screw heads), and a 1.9 mm-deep underside recess covers the three wheel screws. It is held by 6 × M2 × 6 thread-forming screws with 3 mm engagement. To remove the wheel: cap off, three M3 screws out, pull the wheel off the spigot.
- **Two-tone print:** rim and ring in light PETG, cap in dark PETG.

**Trade-offs:**

- The cap puts the hub 4.3 mm outboard of the wheel face, so the robot is **202.6 mm wide**, against the 205 mm target. Nothing on the chassis sits outboard of the hub.
- The rim and hub are 94.6 g per wheel at solid density, against 88.5 g for D-006 and 89 g in the register. The register needs +5.6 g per wheel when the wheel is ported into the chassis.

**CAD changed:** [wheel_model.py](01-chassis/v1/cad/wheel/wheel_model.py) and `check_wheel.py`. The checks add the D-007 pocket and turning flange clearance, the spigot bore, the 1.3 mm wall from bore to screw hole (D-007 geometry), wheel screws seated and ending at the flange face, the cap covering bore and screws, cap-screw engagement and seating, and a ≥ 0.5 mm cap wall (0.6). **23/23 pass.** The chassis model is still not changed; its `wheel_assembly()` keeps the D-007 plain rim.

**BOM changed:** CH-004 and CH-005 re-specified; CH-048/049 back to 12; CH-058 (hub cap) and CH-059 (M2 × 6 screws, 12) added.

**Records note:** the ledger has two entries numbered D-005, "Chassis / wheels" and "Chassis / motor interface", so `#d-005` links resolve to the first. Renumbering one is left to the builder, because D-007 links to the motor-interface D-005.

**Next actions:** the D-005 coupon adds the cap fit, the M2 pilot and strip torque, and the cap recess over real M3 heads. Port the wheel into `wheel_assembly()` together with the D-005/D-007 follow-ups: mass register, loaded radius, and the rotating-screw sweep, which must now include the cap.

---

## D-009

**2026-09-29 · Chassis / wheels (CH-005, J14) · ACTIVE; full `check_layout.py` rerun pending**

**Decision:** the builder asked for a second tyre and for the D-008 wheel to be merged into the chassis-v1 CAD.

- **Handed tyres.** The right wheel is the left one turned round. With identical tyres, the right chevrons would point backward relative to travel. The right tyre is now the left one **mirrored**, so on the robot both chevrons lead forward, apex at the top toward +X (tractor convention). The chevron was flipped to lead forward on the left as well. Rim, clamp ring, hub cap and hardware are symmetric and identical on both sides. CH-005 becomes one left and one right tyre; they are not interchangeable.
- **Merged into chassis-v1.** [`wheel/wheel_model.py`](01-chassis/v1/cad/wheel/wheel_model.py) is now the single source for the wheel. `wheel_assembly()` in [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py) places its `mounted_leaves(side, …)` and keeps D-007's stub and set screw. A new `_check_wheel_interface()` stops the build if the wheel's hub constants drift from the D-007 ones: pocket, bore, spigot, flange, and screw PCD, length, head and angles. The placeholder tyre and rim and the spin-index inlay (and its constants) are gone.

**Checks:**

- **Wheel alone:** `check_wheel.py` 24/24. New: `both_tyres_lead_forward_when_mounted` measures +7.0 mm on each side, and an un-mirrored right tyre reads −7.0, so the check discriminates.
- **Wheel on the chassis:** the new targeted script [`check_wheel_on_chassis.py`](01-chassis/v1/cad/wheel/check_wheel_on_chassis.py). `check_layout.py` assumes an axisymmetric wheel and treats its solids as the swept volume, which is no longer true. So every rotating part except the rim and the (axisymmetric) stub is swept as a revolved envelope, and the rim is turned through its 60° period in 5° steps. **All clear of the 1.5 mm running gap:**
  - rim ≥ 3.05 mm through 60°, to the bearing cap;
  - tyre 3.6 mm to the wheel-arch trim;
  - hub cap, ring screws and cap screws are further away;
  - the tightest are D-007's own parts: stub 1.5 mm to the bearing cap, set screw 1.53 mm, wheel screws 1.65 mm.

  Wheel on stub: 3 screws, 2.0 mm of thread each in the flange, no internal overlaps.
- **`check_layout.py`:** its `rotating_screws_swept_clear` count goes 8 → 32. The full run was **stopped at 42 minutes by the builder's choice** (normally about 10 min; the lugged tyre slows its whole-robot boolean sweeps). **It has not been rerun**, so its other wheel-dependent rows (track from the rim centre, loaded radius, connector/power clash maps) are unverified. Rerun it with the frame-split work.

**Mass register:** WHEEL_L/R 87.3 → 92.5 g (the wheel without the D-007 screws, which are counted with the axle), CoM kept on the wheel centre (in fact about 1 mm outboard).

**Not updated:** `body-chassis.step` (whole robot, gitignored, about 0.5 GB) still shows the old wheel until it is regenerated. `chassis-v1.step` is rebuilt.

**Next:** rerun `check_layout.py` in full; the D-005/D-008 print coupons; print one tyre of each hand.

---

## D-010

**2026-09-29 · Chassis / axle and frame (CH-001, CH-015, CH-060, CH-061; J02, J04) · ACTIVE; HOLD on printer/material coupons, clearance rerun and axle rig**

**Decision:** select the manufacturer article NMB L-1480ZZ (8 × 14 × 4 mm, MR148ZZ size) and define J04 as a removable, keyed carrier-to-rail joint. Use one printed carrier per motor side, combining the 5 mm motor plate and its front/rear cheeks; keep the bearing housing and retaining cap separate. Each carrier keys into the front and rear rail ends and clamps with two DIN 7984 M3 × 8 screws at each end, into 6 mm M3 heat-set inserts in the rails.

**Why:** this creates a modeled structural load path from the bearing housing through the motor plate/cheeks into both longitudinal rails while retaining independent wheel axles. The crossmembers span left-to-right at the front and rear; there is no axle shaft across the centreline. Keys set the carrier position so the screws clamp rather than locate it.

**CAD changed:** `body_chassis_model.py` fuses each motor plate with its two cheeks into `AXLE_MOTOR_CARRIER_L/R`; rail ends now contain 2.0 × 3.0 × 2.5 mm keys/pockets, two axial insert bores and tip relief per end. The model includes the eight J04 screws/inserts. `check_layout.py` now measures the gearbox seat and bearing housing against the carrier label. The README, checklist, axle-stack plan and BOM were updated.

**Nominal joint:** key pocket has 0.2 mm per-side and 0.7 mm end clearance; screw axes are at Z 38/48 mm, Y ±54 mm front and ±58.5 mm rear. Rail insert pilot is Ø4.3 × 6 mm. These are coupon starting values, not final process compensation.

**Bearing source:** NMB's [official L-1480ZZ page](https://nmbtc.com/parts/l-1480zz/) confirms the 8 × 14 × 4 mm article, 819 N dynamic rating and 386 N static rating. Official CAD is offered through PARTcommunity; retrieving its drawing/CAD and confirming the supply lot remain release actions. Ratings are catalog values and do not certify the printed housing, axle arrangement or retaining-compound joint.

**Verification:** a focused source-geometry check found no positive-volume intersection across the carrier, rail, screw and insert solids. This does not prove strength, print fit or fatigue. The latest wheel-on-chassis sweep was attempted but interrupted after several minutes before it produced results; the pre-J04 D-009 sweep remains the last complete nominal result. Full `check_layout.py` remains pending.

**Physical pass targets:** axle datum deflection ≤0.25 mm under 31 N radial and 8 N lateral service loads; ≥1.5 mm running gap at those loads using measured print stack; proof at 62 N, 16 N and 0.8 N·m with no cracks/insert movement and ≤0.10 mm residual set. Each insert coupon must hold 100 N axially. Axle rig limits remain runout ≤0.30 mm TIR, end play ≤0.10 mm, 100 N inner-ring retention for 10 s with <0.10 mm movement, current change within max(0.05 A, 10%) after face-screw tightening, and 200 low-speed reversals.

**Next:** retrieve the NMB technical drawing/CAD and confirm a lot; print bearing, insert and J04 key coupons after printer/material selection; rerun the current wheel sweep and full layout checks; build the side-specific axle rig when the real motor and turned stub are available. No physical test has passed yet.

---

## D-011

**2026-09-30 · Chassis / nose (CH-002, CH-003, CH-007, CH-019, CH-031–033, CH-062–064; J07, J08) · ACTIVE; HOLD on received caster, coupons and physical tests**

**Decision:** close the ball-transfer section's blocking CAD items from the printability and service-access review in one change, in [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py). The [joint register](01-chassis/v1/joint-register.md) J07/J08 entries carry the details.

**Changes, by the builder's to-do numbering:**

1. **Caster fastening (J07A).** The three M3 screws used to end 3 mm into Ø3.2 clearance holes and held nothing.
   - Pololu's drawing 2691 shows a 2.7 mm web with Ø6.3 counterbores from the ball side. The imported STEP lacked them, and the model now cuts them.
   - The screws are now 3 × ISO 7380 M3 × 8 (CH-031), driven from below into 3 × CNC Kitchen M3 × 5.7 inserts (CH-063). The inserts go in Ø4.0 bores in a pod seat thickened from 3 to 6 mm.
   - Result: 5.3 mm of thread engagement, and the heads sit 0.43 mm off the ball.
   - The GP2Y now rests on the seat top (Z 35), so its rails are gone. No reclocking was needed.
   - The old `ball_screws_engage_flange` check is replaced by `ball_screws_thread_into_seat_inserts`. It needs ≥ 4.5 mm of shank inside a coaxial insert that sits in the seat.
2. **Touch cap (J08B).** The cap could only travel about 0.7 mm before it jammed on the raked prow, so the 3 mm switch travel was not real.
   - The nose is now a constant octagonal section from X 122.5 to the face. The cap's 0.5 mm running gap is now true: it measured 0.41 mm before.
   - The 0.5 mm flexures are replaced by two 2.0 × 16.5 mm vertical snap fingers with 0.8 mm hooks in flank slots, at about 2.2 % strain for a 1 mm spread.
   - The cap slides 3.0 mm and stops on the pod face. It slides off forward.
3. **Pod sliver.** The 0.40 mm skin sat at the ear slot's front end, where the old taper began at the slot.
   - The belt now holds full width to X 121.0, and a chamfer wedge outside the ear window is removed.
   - The slot's outer edge cannot move in to Y 21.5: the GP2Y ear flange measures ±22.25 mm, and the slot must stay full height so the sensor can lift out.
   - The same pass found an older open slit: the 15.5 mm pocket broke through the upper chamfer at Z 47–49 behind the belt, X 95–109. The pocket now narrows at 45° above the pod screw heads, to |Y| 12.3.
4. **Lid retention (J08C).**
   - A rear tongue drops into a pod-wall groove that is open forward.
   - The shell band sits 0.5 mm over the lid.
   - One M2 × 8 countersunk thread-forming screw (CH-062) goes into a pod boss at (124.6, −11.8).
   - Official removal: cap off, screw out, slide the lid 11 mm forward, lift.
5. **Cable exit.** The J10-8 route is modelled as harness reserves:
   - a round-cornered 6 × 3 mm slot at Z 32–35 through the pod back wall, with a 1 mm flared mouth;
   - a floor trough, plus a groove for the switch pair;
   - a run under the crossmember;
   - a new Ø5 bore through the crossmember and deck at (86, −31);
   - a riser beside the speaker cavity into the sensor trunk, and a drop to C3 J10-8 below the compute tray.

   No grommet.
6. **Switch (CH-019).** Panasonic ESE22MV21 detector switch: 4.25 mm full travel, 290 mN max ([datasheet](https://industrial.panasonic.com/cdbs/www-data/pdf/ATB0000/ATB0000C12.pdf)). It sits on an 8 × 6 × 0.8 carrier board (CH-064) in a floor recess. The lever tip sits 0.2 mm off the cap at rest. Tact switches were rejected because their travel is well under 1 mm.
7. **Cap clearance.** Fixed by the constant nose (item 2): the running clearance measures 0.50 mm.
8. **Inserts (CH-033, CH-063).** CNC Kitchen M3 × 5.7 standard, Ø4.0 hole and Ø4.6 knurl ([source](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)). The Ø4.0 bores now give 0.3 mm/side of interference; before, the modelled insert equalled the bore. The crossmember pod screws (CH-032) become ISO 7380 M3 × 8 with 5 mm of engagement.

**Verification (2026-09-30):**

- **Full `check_layout.py`: not rerun, by the builder's choice.** Its saved report still dates from 27 Sep, and the D-009/D-010 reruns also remain pending.
- **Nose checks:** the new [`check_nose_joints.py`](01-chassis/v1/cad/check_nose_joints.py) runs the J07/J08 rows of `check_layout.py` on the nose parts in about 30 s. All 12 pass:
  - thread engagement;
  - insert interference;
  - flange seat;
  - no nose clashes;
  - travel reserve clear;
  - 3 mm cap sweep with the hard stop and forward retention;
  - 0.50 mm running clearance;
  - nose width 40.6 mm;
  - shell notch clear;
  - CoM margin.

  `check_layout.py` itself parses but has not been run end to end with the new rows.
- **Service sweeps, body on:** [`check_nose_service.py`](01-chassis/v1/cad/check_nose_service.py) → [`nose-service.md`](01-chassis/v1/cad/generated/nose-service.md). Clear:
  - caster housing, ball, screws and base from below, with nothing else removed;
  - the three hex-key paths;
  - cap forward;
  - lid forward, then up;
  - sensor and switch up;
  - lid-screw driver;
  - every J10-8 reserve.

  The first run found three problems, all fixed and re-swept: the sensor was trapped by the new neck, the lid hit the front panel when lifted after 8 mm, and the cable drop hit the compute tray.
- **Printability** (DfAM tool, 4000 samples):
  - Pod: minimum wall 1.3 mm, was 0.40; 3.2 % support area printed seat face down.
  - Cap: 0.94 mm, the same bottom edge as before; 2.8 % support nose face down.
  - Lid: 3.4 % support on its side, against 41 % flat. Its lowest samples, 0.3–0.6 mm, are 45° knife edges along the split line through the chamfer, as before; they are edges, not skins.
- **Mass register** (hand-kept):
  - `BALL_NOSE_POD_SENSOR_CAP`: 15.9 → 18.7 g at (111.4, 0, 37.9), measured from the solids.
  - `CHASSIS_PRIMARY_FRAME`: −0.3 g for the bore.
  - Whole robot: 2590.1 g, CoM X +19.30 / Z 106.28 mm. a_tip is 1.78 against the 1.58 minimum, so the margin line passes (equivalent to X ≥ 17.1 mm at this height).
- **Exports:** `chassis-v1.step` is rebuilt. `body-chassis.step` is not regenerated.

**Still unverified:**

- the received #2691 web, counterbore, hole diameter and housing;
- insert pull-out in the pod seat and crossmember;
- the switch's ON point and force against the cap;
- snap-finger fatigue;
- lid screw strip torque;
- static load at 2.55 kg, drop and threshold climbing (set the pass numbers before testing);
- the timed body-on service dry run for the caster swap and the sensor swap;
- the J07B L-key reach at the dry run (about 12 mm to the GP2Y).

**Next:** measure the caster on receipt; print the pod, lid and cap in the stated orientations; run insert coupons, then the load, cap and service tests; write the caster and sensor service procedures from the dry run.

---

## D-012

**2026-09-30 · Chassis / axle (CH-015, CH-051; J02) · ACTIVE; HOLD on supplier availability, lot verification, drawing/load data, fit coupons, clearance rerun and retention test**

**Decision:** select the **688 ZZ, 8 × 16 × 5 mm** double-metal-shielded chrome-steel bearing listed by [OnlyScrews](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5) as the chassis design article. This supersedes the NMB L-1480ZZ/MR148ZZ selection in D-007/D-010; the axle-stack architecture, Ø8 stub and wheel interface remain. Use two bearings per side, four total.

**Reason:** the user selected a locally listed, standard 8 mm-bore bearing family after the previously selected L-1480ZZ could not be procured. The 688 ZZ uses the same 8 mm bore but has a larger 16 mm OD and 5 mm width, so its seat and positions must be changed in the CAD.

**Supplier evidence and procurement hold:** the listing gives ID 8 mm, OD 16 mm, width 5 mm, ZZ shields and chrome steel. It does not identify a manufacturer or publish a drawing, internal-clearance class or load ratings. At review, the page shows “Sold out” in its purchase panel while also displaying “In stock” in its descriptive copy. Treat current stock as unavailable/unconfirmed; obtain a confirmed orderable lot and preserve its markings and manufacturer data before physical qualification. No load rating is inferred from the page's generic claims.

**CAD change:** `body_chassis_model.py` now models 688 ZZ rings, OD radius 8 mm and 5 mm width. The pair occupies |Y| 76.51–81.51 and 81.51–86.51; the 0.01 mm inboard datum offset avoids a degenerate mirrored housing boolean. The Ø16 outer seat is coupon-tuned; bearings stand 0.16 mm proud of the housing's 86.35 mm outboard face for cap retention. The stub shoulder and wheel positions stay fixed. The set-screw station remains |Y| 74.8, giving 0.46 mm nominal from the Ø2.5 tap drill to the first bearing face. Verify this narrow land on the stub drawing and part. CAD checks assert the selected bearing and seat dimensions. Supplier STEP/drawing is unavailable, so the rings remain parametric placeholders.

**Fit and proof gates:** coupon the printed seat Ø15.90–16.10 mm in 0.05 mm steps; verify the actual Ø8 k5 shaft fit, race drag, shield clearance, runout and endplay with delivered bearings. Retain the inner rings by k5 plus Loctite 641 and pass the 100 N outward-hold test for 10 s with <0.10 mm movement. Rerun wheel-to-chassis clearance and full `check_layout.py`; inspect the nominal 0.46 mm edge clearance from set-screw tap drill to first bearing face on the turned-stub drawing. No physical fit, load or retention test has passed.

**Next:** monitor/order from the selected listing when available or obtain the same specified article from a confirmed supplier; request manufacturer, internal-clearance class, drawing and load data; then print fit coupons and run the motor-independent retention fixture. Motor-dependent axle testing remains separately blocked on motor receipt.

---

## D-013

**2026-09-30 · Chassis / nose (CH-007, CH-019, CH-064, CH-065, CH-066; J08B) · ACTIVE; HOLD on bench trip-point check and the PCB-10 J10-8 pin change**

**Decision:** replace the D-011 nose switch with contactless sensing. A TI DRV5055A3 linear Hall sensor on a small board in the pod seat reads a Ø2 × 1 N35 magnet in the touch cap, and the C3 firmware sets the trip point. Two small compression springs return the cap. Details: [nose-hall-board.md](01-chassis/v1/research/nose-hall-board.md).

**Why:** D-011 misread the Panasonic ESE22MV21 drawing. The "4.25 mm (2.05 mm)" figure means a full travel of **2.05 mm**; 4.25 is a height. The switch turns on at 1.5 ± 0.3 mm. A rigid 3 mm cap therefore either misses the switch or crushes it, with 0.25 mm of worst-case margin. Other options were considered and rejected:

- **DRV5033AJ Hall switch:** its worst-case thresholds (operate 3–12 mT, release 1–5 mT) need a 12:1 field ratio across the stroke. A small magnet over 3 mm gives about 7:1.
- **DRV5032ZE:** 20 Hz sampling, up to 75 ms latency.
- **Omron D2F hinge lever:** operating position tolerance of ±1.5 mm.
- **Foam pad, or a 2 mm stroke:** these depend on material properties or print tolerances.

The linear sensor with a boot-calibrated threshold has none of these limits. It also has no mechanical wear.

**CAD** ([`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py)):

- **Hall board:** 6.0 × 4.6 × 0.8 mm, standing in an open-top slot at X 126.6–127.4. The SOT-23 sensor sits in a notch through the seat's front face, centred at (Y 10, Z 32.6).
- **Magnet:** in a pocket in the cap wall, below the window slit. It clears the sensor by 3.1 mm at rest and 0.1 mm at the 3 mm stop.
- **Springs:** two spring pockets, Ø3.3 × 6 mm at Y ±3, Z 32.
- **Removed:** the D-011 floor recess, switch and lever.
- **Lead groove:** extended to the board.
- **Checks:** `check_layout.py` and `check_nose_joints.py` now check the magnet against the sensor at the stop, and treat the springs as compressible.

**Trip point** (on-axis field of the magnet, Hall plate 0.65 mm under the package top, still to confirm):

- 7.3 mT at rest, 15.7 mT at 1 mm, saturated at the stop.
- Firmware trips at rest + 5 mT and releases at rest + 3 mT.
- Trip is 0.71 mm of cap travel nominal, 0.50–0.95 mm over ±0.4 mm of gap and ±5 % Br. Release is at 0.48 mm.

**Interface change:** J10-8 becomes +5V, GND, GP2Y_VO, +3V3, HALL_OUT. The PCB-10 carrier must bring +3V3 and an ADC-capable pin to J10-8 in place of the switch pair.

**BOM:**

- CH-019 → DRV5055A3QDBZR.
- CH-064 → Hall board.
- New: CH-065 magnet, CH-066 return springs (2).
- CH-007 gains the magnet pocket.

The mass row is unchanged at about 0.3 g for the sensing parts.

**Verification (2026-09-30):**

- `check_nose_joints.py`: 12/12 pass. Magnet gap is 3.1 mm at rest and 0.1 mm at the stop, with no hits.
- `check_nose_service.py`: the Hall board lifts out once the cap and lid are off, and the cap slides off forward. The tool paths and the whole J10-8 route are clear. See [nose-service.md](01-chassis/v1/cad/generated/nose-service.md).
- `chassis-v1.step` is rebuilt.
- Full `check_layout.py` has not been run, by the builder's choice.

**Open:**

- the bench trip point (pass: 0.4–1.2 mm against a dial indicator);
- the spring rate, and whether the cap returns to its hooks from any position;
- the Hall plate depth from TI's package drawing;
- the PCB-10 J10-8 pin change and the C3 firmware threshold;
- magnet polarity at assembly.

---

## D-014

**2026-09-30 · Chassis / rear keel (CH-008, CH-009, CH-010, CH-020, CH-034, CH-067 to CH-072; J09A/B, J10A/B) · ACTIVE; HOLD on the CH-020 breakout, CH-009/CH-010 materials, coupons and physical tests**

**Decision:** close the rear TCRT keel's attachment, cartridge, cable and wear-part joints in CAD (to-do sections A–D). Joint details are in the [joint register](01-chassis/v1/joint-register.md#j09a--rear-keel-to-rear-crossmember).

**Why:** the keel screws ran into solid crossmember plastic, and the TCRT had no retention. The cable's Ø6 holes would not pass the 6.5 mm GH plug, and the old riser clipped them. The height shim overlapped the leads, and the shoe and guards were only fused to the keel.

**CAD** ([`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py)):

- **J09A, keel to crossmember:**
  - Four ISO 4762 M3 × 30 screws go into CNC Kitchen M3 × 5.7 inserts, fitted from below. Engagement is 5.5 / 5.7 mm; the insert length caps it below the 6–8 mm first asked for.
  - The rear pair moves from X −45.5 to −44.0. At −45.5 the insert left 0.2 mm of wall to the crossmember's rear face; the wall is now 1.7 mm (2.2 mm at the front face).
  - The counterbores are Ø6.5, and the crossmember's Ø6 cable bore is closed.
- **J09B, TCRT to keel:**
  - The pocket is open below the keel. The TCRT sits face down on the 0.6 mm end ledges of a printed bezel.
  - The leads go into a pass-through socket on the breakout, which sits in an open-top cavity behind the crossmember.
  - The height is set by 1 mm shims between the bezel and the keel belly (Z 12): two shims give Z 10, and zero to four give 12 to 8.
  - One M2 × 10 and a moulded pin fix the bezel. The old steel shim that overlapped the leads is removed.
- **Keel section:** the sensor flat widens to a 9.5 mm half-width, and a station at X −46 keeps the belly flat over the shim stack. The pocket wall at the chamfered edge goes from about 1.6 to 3.9 mm (to-do 15). The keel still has 1.0 mm of clearance in the 10.5 mm shell slot.
- **J10A, wear shoe:** it has a 2.5 mm dovetail tongue in a groove open at the front, held by one M2 × 6 thread-forming screw across the tongue.
- **J10B, guards:** both guard lips are now part of the bezel.
- **J10-10 cable:**
  - The disconnect is a top-entry GH4 on the breakout, so the keel comes off with four screws and one plug.
  - The cable leaves upward behind the crossmember, in the 7.6 mm gap to the shell wall, so neither the crossmember nor the deck needs a hole.
  - `harness_routes()` gains a 30 mm slack loop, a riser beside PCB-02 and a run over PCB-04, under the compute tray, to C3 J10-10.
  - A zip tie through a new lug on the crossmember's rear face gives the strain relief.
- **Breakout (CH-020):** still unselected. It is modelled as a 12.3 × 13 mm custom-PCB reserve; the 32 × 14 mm LM393 module does not fit.

**Mass:** REAR_SKID_KEEL goes from 12.0 g at (−39.9, 0, 20.4) to 19.6 g at (−40.2, 0, 22.4), with volumes measured from the solids. The model now reports 2605.1 g with the CoM at (19.07, 0.16, 105.87). The margin line needs X ≥ 17.08.

**BOM:** CH-008, CH-009, CH-010 (now one bezel), CH-020 and CH-034 are updated. New rows: CH-067 inserts (4), CH-068 shims (2), CH-069 to CH-071 M2 screws, CH-072 zip tie.

**Verification (2026-09-30):**

- New `cad/check_rear_keel.py` (about 2 min): 21 of 21 checks pass. It writes [rear-keel-checks.json](01-chassis/v1/cad/generated/rear-keel-checks.json). It covers:
  - no clashes in the keel stack;
  - screws in clear holes, with at least 5 mm of engagement;
  - hex-key paths from below;
  - shims clear of the TCRT;
  - the ±2 mm range;
  - sensor swap from below with the keel on;
  - the shoe sliding out forward;
  - the keel dropping 30 mm;
  - the board lifting out;
  - the J10-10 route clear of the frame, shell, electronics, body frame, panels, audio and sensors.
- `check_layout.py` keel rows are updated: the count-only screw row is replaced, and the shoe/guard backing rows follow the new parts. The pitch order (shoe 6.05°, guards 6.49°, keel 8.97°, sensor 10.43°), backing and CoM rows were run on their own and pass.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- to-do 8: select the CH-020 breakout and socket;
- to-do 12: choose the wear-shoe and bezel materials;
- E (print orientation and exports) and the rest of F;
- G (optical height on real floors, service timing, tip order).

---

## D-015

**2026-09-30 · Chassis / rear TCRT (CH-020, CH-071; J09B) · SUPERSEDED by [D-016](#d-016)**

**Decision:** CH-020 is a custom passive board. Its spec was removed by D-016. The TCRT5000 plugs into two 1 × 2 female headers underneath the board, and a top-entry GH4 on top is the J10-10 disconnect. The board has no comparator: the C3 node pulses the LED through a MOSFET and reads the phototransistor on an ADC1 pin. It subtracts ambient light, and any fault reads as a cliff.

**Why:** the builder asked for an off-the-shelf board first, and none fits the keel cavity of about 13 × 14.8 mm:

- the LM393 modules are 35 × 10 mm;
- the Soldered breakout is 22 × 22 mm;
- the Pololu QTR-1A fits, but carries a QRE1113 rated to 6 mm, against our 10 mm optical height, and cannot be swapped from below.

**Changes to D-014:**

- **Floating board:** the TCRT5000's standard 3.5 mm leads cannot stay engaged over ±2 mm in a socket on a fixed board. The board now rides on the fully seated sensor and moves with the shims (Z 20–25.6). A ledge at Z 19.8 only catches it while the sensor is out. The M2 × 5 board screw (CH-071) is dropped.
- **Socket:** the datasheet lead pitch is 5.5 × 2.54 mm, so the D-014 4-way block becomes two 1 × 2 strips, with the package's mounting clips between them.
- **Board size:** the GH4 moves to +Y 4.6 to clear the strips' solder joints. The board grows to 14.2 mm in Y, and the cavity to ±7.4 (keel side wall 2.1 mm).

**Interface change:** J10-10 changes from 5 V / GND / analog / digital to +3V3 / GND / TCRT_OUT / LED_EN. PCB-10 must provide an ADC1 pin with a 100 kΩ pull-up (fail-safe when unplugged) and a spare GPIO.

**CAD:** in `body_chassis_model.py`:

- the board, the two header strips and the moved GH4 are modelled;
- the cavity is widened and has a new ledge;
- the J10-10 service loop is widened to Y +7;
- the REAR_SKID_KEEL row goes from 19.6 to 19.4 g, without the M2 × 5 screw.

**Verification (2026-09-30):**

- `check_rear_keel.py` passes 23 of 23. The new rows cover:
  - the sensor stack clearing the keel at both ends of the J09 range;
  - the board sitting 0.2 mm above the ledge at the lowest setting;
  - the board riding on the seated sensor.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- confirm the emitter end against the placed STEP;
- check JST's BM04B land pattern against the 14.2 mm board edge;
- confirm a 5.0 mm dual-leaf header part;
- make the PCB-10 J10-10 change;
- bench item 20, which sets R2 and checks the fail-safe.

---

## D-016

**2026-09-30 · Chassis / rear TCRT (CH-020; J09B) · ACTIVE; HOLD on the PCB-10 J10-10 change and bench item 20**

**Decision:** there is no board in the keel. The TCRT5000's legs are soldered to a JST GH 4-way pre-crimped lead (AWG28, 350 mm) under heat-shrink, and the lead plugs into C3 J10-10. The LED resistor, the LED switch MOSFET, the gate pull-down and the phototransistor load/pull-up go on PCB-10. Spec: [rear-tcrt-lead.md](01-chassis/v1/research/rear-tcrt-lead.md). Supersedes [D-015](#d-015).

**Why:** the builder asked why a board was needed. Electrically it isn't: the D-015 board only carried a connector and a socket. The builder chose the simpler build over the two things the board gave:

- **Keel removal** now needs the sensor pulled out first, and J10-10 unplugged at PCB-10.
- **A sensor swap** replaces the sensor and its lead together.

**Changes from D-015:**

- **Keel:** the board cavity and ledge are removed, and the sensor pocket runs straight out through the keel top. This restores the full side walls. Keel body 14.64 cm³; the REAR_SKID_KEEL row is now 20.0 g at (−40.5, 0, 22.7).
- **CAD:** a heat-shrink joint envelope and the lead are modelled, and the slack loop goes back to Y −26 to 3.
- **J10-10:** pins are LED_A, LED_K, TCRT_OUT and GND. It is still a GH 4-way header, now wired to the PCB-10 circuit in the spec.
- **Fail-safe:** an open lead or dead LED reads high through the PCB-10 pull-up, which is a cliff.

**BOM:** CH-020 becomes the sensor and lead (CANDIDATE). CH-071 stays DROPPED.

**Verification (2026-09-30):**

- `check_rear_keel.py` passes 20 of 20.
- The new rows cover:
  - the sensor and lead dropping out below with the keel on;
  - the lead leaving through the keel top without touching it;
  - the stack clearing the keel across the J09 range.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- the PCB-10 J10-10 circuit;
- bench item 20 (sets R2, includes a motors-running pickup check);
- the joint sleeve fitting the 7.6 mm pocket on the real part.

---

## D-017

**2026-09-30 · Chassis / rear keel wear parts (CH-009, CH-010; J10A/B) · RECOMMENDED; confirm after the physical tests**

**Recommendation:** print the wear shoe and the TCRT bezel (with its guard lips) in **PETG**. The builder asked for a recommendation and delegated the choice.

**Why PETG over PLA:**

- **Impact:** the 1.5 mm guard lips and the shoe take floor strikes on a tip. PETG bends where PLA snaps.
- **Screws:** both parts carry thread-forming M2 screws (CH-069, CH-070), and PLA tends to crack around them.
- **Heat:** PLA softens around 55–60 °C and creeps under the screw clamp; PETG holds to about 75 °C.
- **Same print:** the keel is already a PETG candidate, so all the keel parts print in one material.
- TPU is excluded: its friction would grab the floor.

**Optional upgrade, not modelled:** if the shoe wears fast or drags on carpet or tile, add UHMW-PE tape (about 0.25 mm) to its sole, and thin the shoe by the same amount so the floor clearance and tip order stay unchanged. Nylon (PA) is the better printed wear material, if a printer that can run it becomes available.

**Changed:** CH-009 goes from OPEN to DESIGN, and CH-010's release check names PETG. J10A and J10B record the material. No CAD change.

**Open:** retention, abrasion, floor-strike and snag tests (items 21–22); revisit after the tests.

---

## D-018

**2026-09-30 · Chassis procurement and release scope · ACTIVE; receiving, fabrication and physical validation remain open**

**Decision:** record the user's settled **Pololu #2691 plastic-roller caster** and **Samsung INR18650-25R cells** as SELECTED. Correct the current motor row to SELECTED under D-003/D-005; purchasing the motor enables its receiving and load checks. SELECTED does not mean ordered, received, fitted or passed. Supplier-page stock and physical release checks are separate fields.

The canonical [BOM](BOM.csv) and [chassis snapshot](01-chassis/v1/BOM.md) contain the current supplier candidates, exact-match qualifications, and release checks.

**Recommendations, not new installed substitutions:** retain two DRV8874 carriers and the Sharp A41 for the current design; reject the OD8/free15/wire1 return spring; sample MISUMI C-UR3-10 if its quote is acceptable; buy the bare TCRT specified by D-016; consider Robokits MPU6050 for budget bench use. Ø3 × 1.5 mm N35, the purchased balanced 2S module and 5 A ATOF are conditional alternatives. Magnet pocket/threshold, IMU interface/mount, protection thickness and fuse/holder/current requirements must be resolved before adopting those changes. BF-013A compatibility is not established. No corresponding CAD substitution was made.

**Sourcing correction:** OnlyScrews BB688ZZ now shows in stock, superseding D-012's dated sold-out observation. Its maker/grade/load evidence, received fit and retention remain open. Common matched-size hardware and dowel links are recorded; DIN 7984 low heads, M3 × 18 button heads, M3 × 2.5 cup-point set screws, plastic thread-forming screws, selected 5.7 mm inserts and Loctite 641 retain exact-source work. Nearby articles are not approved substitutions.

**Test scope:** regulated supply-powered chassis tests may use a documented development controller, driver carriers, temporary harness and relevant sensor circuits before final system PCB fabrication. Verify intentional voltage/current limits, encoder logic, default disable, physical stop and braking/transient behaviour. Keep cells disconnected and use secured inert ballast for that scope. Battery-powered tests retain protected-pack construction, fuse/disconnect, thermal/charging and 8.4 V motor-control gates.

**Genuine new findings:** Samsung recommends >1 mm cell spacing against the current 0.2 mm CAD gap. The nose Hall note now treats trip values as predictions and records startup-pressed, missing-magnet and wire-break checks; shared 3.3 V supply does not make the ESP32-S3 ADC ratiometric. Define and verify diagnostic bias, ADC calibration and contact thresholds before functional release. These documentation corrections do not claim implementation or a passed test.

**Release audit:** nose/rear joint architecture is defined under D-011/D-013/D-014/D-016, while physical proof is open. Remaining detail gaps include J05/J06/J16, J11A/B, J12/J13 and J15A/B; purchased interfaces/stub drawing and print/process release are also pending. The saved full-layout baseline predates current source/checker changes. Stage gates are summarized in the chassis BOM; #4804 is superseded, not a current variant blocker.

**Custom PCB work:** a separate [04-custom-pcb folder](04-pcbs/README.md) (renamed `04-pcbs/` in D-038) now records the unreleased board work packages. No schematic, Gerbers or fabricated-board result is implied. Pre-existing edits to the chassis checker and engineering checklist were preserved. A malformed comma-delimited CH-012 release-check field was repaired while updating the BOM; installed quantities are unchanged.

**Verification:** thirteen review reports produced; supplier observations and documentation audited. No hardware purchase, receipt, CAD regeneration or physical PASS was performed in this review. Final CAD checks require the compatible pinned runtime and the release revision.

## D-019

**2026-09-30 · Chassis user selections: drivers, front range, nose magnet and pack protection · SELECTED; receiving and system validation open**

**Selected by the builder:** two Adafruit #3297 DRV8833 boards, one per motor, with both bridges paralleled within each individual board; Sharp GP2Y0A21YK0F from Robocraze; N35 Ø3 × 1.5 mm nose magnet; and Robocraze TIFPS0629 balanced 2S protection module, which the builder intends to buy. The builder reports the Sharp sensor is in stock and the only possible source/choice. These selections supersede prior alternatives and recommendations recorded in D-018 and the point reports.

**CH-064 conclusion:** retain the 6.0 × 4.6 × 0.8 mm custom nose Hall carrier. Its job is to hold the bare TI DRV5055A3, decoupling/filter parts and three-wire interface in the seat's specific slot. An adapter board can test the circuit on a bench but cannot satisfy the installed envelope. Layout/fabrication and contact/fault validation remain open.

**Engineering gates:** Adafruit/TI documentation supports the proposed bridge-parallel arrangement, but not an unconditional chassis current or thermal pass. Commission at a regulated 6 V supply with measured motor current, board temperature and braking/transient checks. The A21's 100 mm minimum range and 38.3 ± 9.6 ms measurement cycle do not satisfy the existing 50 ms stop-path budget once scan/control delay is included; revise and demonstrate the system timing/stopping distance while retaining the selected sensor. Measure actual A21 mounting datums before fit release. The 3 mm magnet changes the CAD pocket; check cap wall, pole, air gap and calibrated contact trip on the physical assembly. Robocraze's module listing gives a 48 × 20 mm footprint but does not establish its thickness or protection behavior; measure and qualify the received board before connecting cells. SELECTED or intended to buy does not mean ordered, received, fitted or passed.

**CAD and BOM:** update the source model, CAD checker names and project/chassis BOM to these choices. The model represents the A21 and Adafruit boards as nominal envelopes until received parts are measured. Generated STEP and reports are stale until the pinned compatible CAD runtime is restored and the affected checks are rerun. The 2.9 mm BMS height remains an unverified legacy placeholder, not a measured module dimension.

## D-020

**2026-09-30 · Chassis / nose return springs (CH-066) · SELECTED for purchase; installed behavior unverified**

**Decision:** the builder selected the Industrybuying listing for RS PRO 821245 stainless compression springs (pack of 10), with two required for the chassis. Published listing/datasheet values are OD 2.75 mm, 0.25 mm wire, 15.7 mm free length, 0.18 N/mm rate and 5 mm minimum working length. The builder said they are getting them; an order or receipt is not recorded.

**Geometry and force:** OD fits the current Ø3.3 mm pockets. Leave the seat floor and 9 mm rest / 6 mm full-travel gaps unchanged for the sample test. At those gaps, nominal pair force is approximately 2.41 N at rest, 2.67 N near the 0.71 mm Hall trip and 3.49 N at the 3 mm stop. At the stop, nominal length is 1 mm above the catalog minimum working length; tolerate as a limit to verify, not a proven coil-bind margin. The free spring is 15.7 mm and the seated gap is much shorter, so check seating, unsupported coil behavior/buckling, cap push force, return from intermediate positions and printed snap-hook retention. High force may make the nose less compliant than planned.

**CAD/BOM:** CH-066 is now SELECTED and the source spring envelope uses the actual 2.75 mm OD and 15.7 mm free-length data. The displayed model remains in its installed 9/6 mm envelope. No seat-floor redesign is made before sample measurements. Generated STEP and check reports remain stale pending the compatible pinned CAD runtime. Keep nose release gated on actual load and 3 mm stroke tests.

## D-021

**2026-09-30 · Chassis / rear floor sensor (CH-020) · SENSOR TYPE SELECTED; sourcing and physical validation open**

**Decision:** use a **bare Vishay TCRT5000 reflective sensor with its four individual leads** in the rear keel assembly. Solder the specified 350 mm AWG28 JST GH4 lead to the sensor under heat-shrink and connect it to J10-10. Do not use the Robu TCRT5000 IR Reflex Tracking Sensor Module (SKU 699619) as CH-020: it is a 5 V comparator/digital-output PCB with a different mechanical and electrical interface. D-016's no-board-in-the-keel design remains in force.

**Reason:** the bare sensor is the part envelope and pin-level interface specified by the existing keel CAD and D-016 lead assembly. The Robu module listing describes a 35 × 10 mm PCB and digital comparator output; it cannot fit the 7.6 mm sensor service pocket or connect directly to the four-wire analog/LED-drive interface.

**Procurement distinction:** the sensor type is settled, but no supplier order or receipt is recorded. The Robocraze pack-of-five listing remains a sourcing candidate; confirm that delivered parts are separate four-lead TCRT5000 packages and verify Vishay manufacturer provenance before representing them as genuine Vishay parts. A seller's generic TCRT5000 listing alone does not establish that provenance.

**Release checks remain open:** receive and measure the part, assemble and fit the sleeved lead in the real keel, then complete the documented 8/10/12 mm floor/edge, ambient-light, motor-running-noise and unplugged-fault checks. Selection does not mean the optical cliff function has passed; the nominal 10 mm floor gap remains a test risk because the datasheet's peak response is at 2.5 mm.

## D-022

**2026-09-30 · Chassis / fastener sourcing and J12/J13 stacks · CANDIDATES; supplier confirmation and fit qualification open**

**Decision:** when OnlyScrews did not show a suitable exact item, record the best next-source candidate or a supplier quote request in the canonical BOM. Do not represent a family listing or a near size as confirmed stock or a drop-in part.

**Joint stack candidates:** J12 / CH-038 uses an M3 × 12 hex-socket countersunk screw candidate, based on the modeled 4 mm deck and 8 mm tapped engagement. J13 / CH-035–037 uses M4 × 12 button-head bolts, accessible plain M4 hex nuts and the existing Ø4 × 8 dowel candidate. The modeled J13 stack is 11.2 mm, leaving 0.8 mm nominal bolt projection without washers. The BOM and [joint register](01-chassis/v1/joint-register.md) now record these choices and the needed seat, engagement, clearance, access and fit checks.

**Other source decisions:** seek DIN 7984 low-head screws from Royal Fasteners; use the Desertcart M3 × 5.7 × 4.6 insert variant only if the exact option is confirmed and coupons pass; use JCPlas B4B66/B4B67 plastic thread-formers as quote/sample candidates for M2 joints; use UAVstore's M3 × 18 button screw option as a sample candidate; and ask Royal Fasteners whether it can supply the still-unconfirmed M3 × 2.5 DIN 916 cup-point set screw. Industrybuying's Loctite 641 is the source candidate for bearing retention, separate from Loctite 222 threadlocker. Probots is the primary candidate for exact 2.5 × 100 mm cable ties, with RoboComp as a backup. CH-061 remains an OnlyScrews candidate with a marginal 0.05 mm nominal radial interference in its current pilot and requires a coupon.

**Status and limits:** source pages and stock were reviewed on 2026-09-30; availability may change. No suppliers were contacted and no fasteners ordered or received. CH-030/060 exact stock and head dimensions, CH-055's 2.5 mm availability, plastic-screw geometry/pilot, and all physical fit/proof checks remain open. No CAD geometry changed under this decision.


## D-023

**2026-09-30 · Chassis / fastener availability update · CH-035 and CH-038 reported available; CH-030/055/060 unsourced**

**Builder-reported availability:** CH-035, M4 × 12 mm hex-socket button-head SS304, is available from OnlyScrews. CH-038, M3 × 12 mm Phillips CSK mild-steel black-oxide, is available. The CH-038 product URL was not supplied, and the previously inspected OnlyScrews page showed a different SS304 item with conflicting stock text; confirm the received part's identity and countersink fit. Neither report records an order or receipt.

**Open sourcing:** the builder could not find a buyable match from the Royal Fasteners leads. CH-030 DIN 7984 M3 × 6 low head, CH-060 DIN 7984 M3 × 8 low head, and CH-055 DIN 916 M3 × 2.5 cup-point remain unsourced. No near-size substitute is approved.

**Image kit:** the pictured assortment contains M5 screws, M5 washers and M5 nuts. It does not match the chassis fastener sizes and is not needed for the listed M3/M4 joints; do not buy it for this BOM.

**Changed:** updated the BOM availability notes, chassis snapshot and fastener sourcing review. No CAD change. J12/J13 received-part fit checks remain open.


## D-024

**2026-09-30 · Chassis / remaining fastener source leads · OPEN; exact size and availability to confirm**

**New leads:** for CH-030 DIN 7984 M3 × 6 and CH-060 DIN 7984 M3 × 8, request exact standard/length and samples from ACME Fasteners through its [TradeIndia low-head socket screw listing](https://www.tradeindia.com/products/low-head-socket-cap-screw-din-7984-or-din-6912-5649111.html). The page is marked in stock and says samples are available, but it does not show the exact M3 lengths or clarify whether its inventory is DIN 7984 versus DIN 6912. Confirm dimensions and standard before treating it as a match.

For CH-055 DIN 916 / ISO 4029 M3 × 2.5 cup-point, [Dalloyed Fasteners](https://www.dalloyedfasteners.com/grub-screw.html) is an Indian manufacturer lead for the ISO 4029/DIN 916 family and M3 grub screws. Its published page does not list a buyable M3 × 2.5 item; ask whether it can supply this short length and provide a sample. The M3 × 3 OnlyScrews item remains an unapproved alternate because it is 0.5 mm longer.

**Changed:** BOM and sourcing review now record the new supplier leads. No supplier was contacted and no purchase or physical fit is recorded. The three exact fastener rows remain open pending source confirmation and received-part fit.

## D-025

**2026-09-30 · Chassis / mixed Phillips-CSK fastener assortment · CANDIDATE; source and fit unverified**

**Correction:** the later assortment image contains M3, M4 and M5 Phillips countersunk screws, plus matching M3/M4/M5 nuts and washers; it is not an M5-only kit. The M3 × 12 compartment is a possible source for CH-038, pending seller confirmation of material/grade and measured countersink dimensions. The M4 × 12 compartment is countersunk and does not replace the selected M4 × 12 button-head candidate for CH-035. The earlier separate image was an M5 button-head assortment and does not match the chassis fastener sizes.

**Changed:** clarified the chassis BOM and fastener sourcing review. No kit link, purchase, receipt or fit check is recorded.

## D-026

**2026-09-30 · Chassis / battery and ballast CAD (CH-022, CH-038, J12) · ACTIVE; PCB-01 height and received-part fit open**

**Why:** an audit found the CAD out of step with the BOM. The two 25R cells were 0.2 mm apart, but the BOM notes Samsung asks for more than 1 mm. CH-038 is a countersunk screw, but the CAD modeled a cylinder head in a flat counterbore. The TCRT mass note said ~300 mm, but CH-020 specifies a 350 mm lead. `chassis-v1.step` also predated the latest source edits.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Cells:** `BATTERY_CELL_PITCH` went from 18.6 to 19.5 mm, giving a 1.1 mm gap at the 18.4 mm maximum cell diameter. The pack envelope grows to 38.5 × 67.0 × 23.5 mm. The tub front wall stays at X 67, so the rear wall moves 0.9 mm back to X 24.0 and the pack centre to X 46.25. The hatch, deck opening and shell floor opening follow from the same constants.
- **CH-038 / J12:** the ISO 7046-1 M3 × 12 head is modeled as a 90° cone to the Ø5.5 rim with k 1.65. It sits in a 90° deck countersink, Ø6.5 at the deck top, 0.1 mm below flush. The bar's tapped holes deepen from 8 to 9 mm, giving 8.1 mm engagement with 0.9 mm tip clearance; before, the tip reached the hole floor. The screw mass now comes from the modeled head.
- **TCRT mass note** now says 350 mm (CH-020). The mass is unchanged.

**Mass register:** the ballast row went from 81.6 to 81.1 g (lighter CSK heads, deeper holes). The battery row centroid moves −0.45 mm in X. Total mass went from 2605.5 to 2605.0 g and CoM X from +19.05 to +19.03 mm (h 105.87 mm). a_tip is 1.763 m/s², against a 1.582 minimum. Measured printed-volume changes (hatch +126, tub walls +52, front deck −134, shell −162 mm³) come to less than 0.2 g, so those rows were not edited.

**Checks:** the new `cad/check_battery_ballast.py` (about 10 min) passes all ten rows and writes `generated/battery-ballast-checks.json`. Those rows cover pack clashes, cell gap, tub margins (1.8 mm front/rear, 1.5 mm side), ballast clashes, head seat, screw length, tip clearance and the CoM margin line. It reports four overlaps as OPEN. They are identical, or differ only by the lengthened hatch, in a copy of the model with this change reversed:
- **Hatch flange × shell floor:** 1689 mm³ (1665 mm³ before). The flange is wider than the shell opening. This is a real, unresolved interface issue that the Sep 27 saved report does not show.
- **Front deck × shell:** 39 mm³.
- **Front deck × power-board proposal envelopes:** 178 mm³.
- **Front deck × IMU screws:** 25 mm³, by design.

The full `check_layout.py` was not rerun. `chassis-v1.step` was rebuilt from the current source. Its product list also reflects earlier source changes: the DRV8833 and GP2Y0A21 envelopes and the Ø3 × 1.5 magnet.

**Changed docs:** the chassis BOM battery note, the CH-022 and CH-038 rows in `BOM.csv`, joint-register J12 and the CAD README.

**Open:** the PCB-01 height is still a 2.9 mm placeholder, pending measurement. The pack build must hold the 1.1 mm cell gap. The received CH-038 head angle and diameter must be checked against the seat. The hatch/shell interface is unresolved. A full `check_layout.py` rerun is needed before release.

## D-027

**2026-09-30 · Chassis / purchased-part models (CH-017, CH-018; J08A, J08C) · ACTIVE; received-unit fit open**

**Why:** the builder asked why the Adafruit driver was only a box, and for other boxed modules to be found and fixed. Two purchased modules in the chassis v1 export were boxes: the Adafruit #3297 driver and the GP2Y0A21YK0F.

**Sources** (details in [purchased/README.md](01-chassis/v1/cad/purchased/README.md)):
- **step.parts:** has neither part (searched 2026-09-30).
- **Sharp:** a community STEP of the A21 sits byte-identical in two unrelated GitHub repositories. It matches the Sharp datasheet outline (E4-A00201EN) to 0.05 mm.
- **Adafruit:** no STEP exists. `purchased/adafruit_3297_drv8833.py` builds one from Adafruit's own Eagle board file: outline, corner radii, holes and part placements. Package bodies are nominal, and the terminal-block height is estimated.

**What the real sensor showed:** the model had the package wrong, and Layout 02 had it wrong with the A41 STEP too. It read the connector as the lens face, so the A41 in Layout 02 was looking upward.
- The lenses and the Ø3.2 ear holes face the same way.
- The package is 13.5 mm deep along the optical axis, and 18.9 mm tall because the connector sits on one edge.
- The ears span 44.5 mm, but the pod is 35 mm wide.

**Builder decisions (2026-09-30):** trim both ears to the 29.5 mm body and clamp the body between seat and lid. Solder the J10-8 wires to the S3B-PH pins, with no plug.

**Changed in CAD (`body_chassis_model.py`):**
- **Sensor:** the STEP (ears trimmed in the model) sits lenses +X, connector up, face at X 128, on the Z 35 seat. The optical axis moves from Z 40.3 to Z 41.5 (lens 6.5 above the body bottom), and the window follows.
- **Pod:** the nose top rises from Z 49 to Z 51. The lid underside is level at Z 49 all the way to the face, replacing the step down over a "lens hood". The front pocket is ±15.0, up from ±14.0. The lid screw moves to (111.8, −11.8), behind the sensor, from (124.6, −11.8), which was inside the real sensor.
- **Lid hump:** the lid has a hump over the header and a 3 mm soldered-lead reserve, 1.2 mm walls, top at Z 58.6. It runs 11.5 mm rearward so the D-011 11 mm forward slide still works, and it gives the lead a path back and down behind the sensor.
- **Cap:** the cap has a top notch so the hump clears its 3 mm travel. The ear slots stay, now vestigial.
- **Drivers:** the #3297 boards lie flat at Z 66 with their long side along X and the terminal block forward, 10.1 mm tall. They are centred 1.5 mm further back, at X 44.5. The real PCB corner otherwise reaches 0.7 mm into the front body-mount doglegs; the old box overlapped them by about 20 mm³.

**Mass:** the nose row goes from 18.7 to 18.9 g (measured pod/lid/cap volume +0.27 cm³). The driver row moves to X 44.5. The register total is 2605.2 g, with CoM (+19.03, 0.16, 105.86) and a_tip 1.763 m/s² against 1.582.

**Checks:**
- `check_nose_joints.py`: all 12 rows pass.
- Nose clash sweep: pod, lid, sensor, cap at rest and at 3 mm, against the body, frame, electronics and harness. Only the designed insert interference shows, and the optical axis is unobstructed. The sensor has 0.5 mm to the lid and 0.5 mm to the cap at full travel.
- Driver sweep: no clashes, 0.8 mm to the dogleg.
- `check_nose_service.py` subset C: cap, lid, sensor and lid-screw paths are clear.
  - `hall_board_up` now needs the sensor removed first (the sweep was updated); the old order hit the sensor at 3 mm.
  - The subset run overwrote the full report, so I restored the committed full report and merged the rerun rows (§) into it.
- `chassis-v1.step` rebuilt. The full `check_layout.py` was not rerun.

**Changed docs:** `purchased/` with its README, the CH-018 row in `BOM.csv`, the chassis BOM A21 note, joint-register J08A/J08C (J08A still named the A41), the CAD README and `check_layout.py` labels.

**Still boxes:** the PCB-01 protection module has no drawing or model and an unmeasured height. The custom boards (PCB-07, the Hall carrier, the power-board proposals) are the project's own designs.

**Open:** check the received A21 and #3297 against the STEPs; ear-trim quality; soldered-lead strain relief; hump and cap-notch print and dust ingress; bench-check the stop-path timing (unchanged).

## D-028

**2026-10-01 · Chassis / battery tub interfaces (J11A, CN-05) · ACTIVE; boss and insert fit unproven**

**Why:** `check_battery_ballast.py` (D-026) reported four overlaps as OPEN. The builder asked for the hatch, deck and power-envelope overlaps to be fixed, and the IMU one recorded as accepted.

**Root causes:**
- **Hatch × shell (1689 mm³):** the hatch lies inside the shell floor's thickness (Z 30.5–32.0 in a Z 30.0–32.4 floor). The floor opening was the tub plus 1 mm, but the hatch flange is wider, so its screw holes sat in shell material.
- **Front deck × shell (39 mm³):** four 0.4 mm slivers where the tub screw bosses (from Z 32) entered the shell floor outside the opening.
- **Front deck × power envelopes (178 mm³):** the CN-05 fuse-holder and disconnect-pair envelopes share the 11.3 mm channel between the tub's +Y wall and the rail with the +Y bosses. Neither envelope can move sideways. Raising the fuse would hit body-mount nut 4 (Z 48.8).
- **Front deck × IMU (25.133 mm³):** exactly the two M2 shanks, 4 mm into the deck (2·π·1²·4), by design.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Shell opening:** now the hatch outline plus `BATTERY_HATCH_GAP` 0.5 mm, from new `BATTERY_HATCH_X` / `BATTERY_HATCH_HALF_Y` constants shared with the hatch.
- **Bosses:** one constant, `TUB_BOSS_XY`, now used by both the tub and the front deck print. The rear pair stays at (28, ±39.5). The front pair moves from (64, ±39.5) onto the front wall's face at (71.5, ±34.35), midway between the ballast bar (|Y| 30) and the fuse holder (Y 38.7). All four stop at `TUB_BOSS_TOP_Z` 39.5, 1 mm over the unchanged Ø4.3 × 7 insert pilots (was Z 41).
- **Hatch:** grows forward from X 71 to X 75 to carry the front screws, leaving 3.5 mm to the edge (M3 washer radius). Its Y extent is unchanged.
- **Pack interface (CN-05):** the disconnect pair, its tub-wall service window and slide path move from Z 37–47 to Z 40–50, clear of the rear +Y boss. The fuse holder is unchanged.

**Mass register (measured against the committed model):** shell −4.04 cm³, so `BODY_SHELL_AND_PANELS` goes from 290.4 to 285.6 g. Frame +0.29 cm³ at 0.571 g/cm³, so `CHASSIS_PRIMARY_FRAME` goes from 206.8 to 207.0 g. The register total is 2600.6 g, CoM (+19.03, 0.16, 105.88), a_tip 1.763 m/s² against 1.582.

**Checks:**
- `check_battery_ballast.py`: all ten rows pass with no OPEN overlaps. The IMU overlap is in a new ACCEPTED list and passes only at 25.133 mm³. Hatch/shell or deck/shell overlaps now fail instead of being reported.
- Pack-interface sweep (pair, fuse, slide path against the whole model): no clashes. The window still opens through the wall.
- `chassis-v1.step` and `body-chassis.step` rebuilt.
- Full `check_layout.py`: 116 of 119 rows pass, in 14 min. All the tub, hatch, ballast, pack-disconnect and IMU rows pass. The window reads Z 40–50. The three failures are listed under **Found, not changed**.
- **`check_layout.py` repaired so it completes** (first full run since Sep 27). Under the substitute runtime (OCC 7.9.3), whole-compound booleans against the C3/DevKitC compound ran away: the J33/J34 reserve reached 133 GB and macOS killed the run at about 37 min, twice.
  - `_boxes_meet` now also needs a leaf of each compound to meet. That only drops pairs whose overlap must be zero.
  - The C3 carrier's own plug reserves are skipped against the C3 compound before the boolean; their results were already discarded.
  - The IMU deck row picked the first `CHASSIS_DECK_WITH_BODY_INTERFACE`, which since the frame split is the rear print. It now picks the print the IMU screws are in, and reads 12.566 mm³ per shank.

**Found, not changed** (the three failing `check_layout.py` rows, all outside this change and likely from D-027):
- `connector_reserves_clear_of_real_hardware`: the PCB-03 J31/J32 and J33/J34 edge-connector reserves overlap the #3297 driver boards by 140 mm³ each.
- `connector_bodies_clear_of_hardware_and_each_other`: the J3_1 and J3_4 mated Micro-Fit plugs overlap the driver boards by 82 and 89 mm³.
- `front_panel_lifts_off_forward`: the front panel's removal path hits `BALL_POD` by 171 mm³, which points to the D-027 nose rework (nose top Z 49 to 51).

**Changed docs and scripts:** the CAD README, joint-register J11A, `check_battery_ballast.py`, `check_layout.py`, and the regenerated `generated/checks.md` and `checks.json`.

**Open:** boss print quality with a 1 mm roof over the inserts; front-boss access with the ballast bar fitted; the J11A screw and insert BOM rows (unchanged); the three D-027 `check_layout.py` failures above.

## D-030

**2026-10-01 · Chassis / frame fasteners, pack restraint and driver mounts (J05, J06, J11A, J11B, J12, J13, J15B, J16; CH-011, CH-030, CH-038, CH-055, CH-060) · ACTIVE; coupons, strap/foam source and physical tests open**

**Why:** the joint register still had open items: J05/J06 crossmembers and J16 deck-to-rail; J11A hatch screws and inserts with no BOM IDs and CH-011 OPEN; no J11B pack restraint; the J12 ballast screw, J13 clamp stack, and J15B board mounts and cable restraint; and CH-030, CH-055 and CH-060 with no exact source. The builder chose (2026-10-01):
- CAD, BOM and docs together;
- standard stocked screws in place of the three odd sizes;
- the pack strapped to the hatch;
- printed posts for the drivers.

D-029 is reserved by a parallel session (lid hump), so this is D-030.

**Found:** the J05/J06 receivers could not be assembled. Each rail's Ø4.3 insert pilot sat behind a Ø3.4 bore through the tongue, so the insert could not be pressed in. The J16 screws at (70, ±54) and (−25, ±58.5) sat under the body M4 feet. On the #3297 boards, the plated holes lie along one long edge. The left board's holes were over the battery opening, and the right board's were on a body foot.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **One frame insert:** M3 × 6, OD 4.4, in a Ø4.3 pilot with a Ø3.4 tip relief: CH-077, the same article as CH-061. Button heads seat straight on the printed faces, with no washers.
- **J05/J06:** the inserts are pressed into the rail tongues' end faces. The tongues widen from ±3.2 to ±4.0 (1.85 mm of wall round the insert), and the pockets to ±4.2. The rear rail ends widen to X −23.
  - J05: ISO 7380 M3 × 16 from X +92 (CH-073);
  - J06: ISO 7380 M3 × 20 from X −48 (CH-074);
  - both have 6 mm of thread.
- **J16:** ISO 7380 M3 × 10 (CH-075) into inserts flush with the rail tops, 6 mm of thread. The axes are (30, ±54), (77.5, ±54) and (−27.5, ±61), each with a deck ear. Off the body feet, the heads clear by 0.65 and 1.15 mm.
- **J11A:** ISO 7380 M3 × 6 (CH-076) through the hatch into boss inserts, 4.5 mm of thread. CH-011 becomes DESIGN.
- **J11B:** two 10 × 1.2 mm hook-and-loop straps (CH-078) at Y ±29 loop under the hatch, through four hatch slots and over the cell tops, clear of the BMS. Two 1.5 mm foam pads (CH-079) sit on the Y-end walls; the +Y pad stops short of the service window. Pack and hatch drop out together.
- **J15B:** the left board is turned 180° (terminal block now rearward) so both sets of holes are outboard. Both boards move 5 mm back to X 39.5. They sit on four Ø7 × 10 posts on the front deck with M2.5 × 4 inserts (CH-080) and M2.5 × 6 screws (CH-081). A tie bridge on each side at X 19–24 takes a motor-lead tie (CH-082). The `HARNESS_MOTOR_BRANCH` reserve moves to run between the posts.
- **J01/J04:** DIN 7984 low heads become ISO 7380 button heads of the same length and key (CH-030, CH-060). The J04 recess goes from R2.9 to R2.95 for the Ø5.7 head.
- **CH-055:** M3 × 2.5 is not a standard ISO 4029 length. The builder approved a stocked M3 × 3 faced down 0.5 mm at the hex end, so the model stays at 2.5.
  - An unmodified M3 × 3 swept only **1.07 mm** past the face-screw heads (rule ≥ 1.5).
  - Faced to 2.5 it sweeps **1.54 mm** (the old DIN heads gave 1.56).
  - A plate-recess and housing-cavity enlargement tried for the M3 × 3 was reverted.
- **J12:** the CH-038 source is the OnlyScrews M3 × 12 Phillips CSK, mild steel, black oxide, matching the builder's report. No geometry change.
- **J13:** the stack stays M4 × 12, plain nut, no washer, leaving 0.8 mm past the nut. Loctite 222 (CH-057) on the nut is the locking method. No geometry change.

**Mass register:**
- `CHASSIS_PRIMARY_FRAME` goes from 207.0 to 229.1 g at (18.14, 0, 46.64):
  - +21.4 g of new hardware, measured from the solids;
  - +0.7 g for the measured +1.24 cm³ of printed volume.
- New `BATTERY_RESTRAINT` row: 3.4 g.
- The driver row follows `DRIVER_CENTER_X` to X 39.5.
- The total goes from 2600.6 to **2626.1 g**, CoM (+19.15, 0.16, 105.30).

**Checks:**
- New `cad/check_frame_fasteners.py` (about 20 min): all nine rows pass. It writes `generated/frame-fastener-checks.json`.
  - No clashes between the changed or new solids and the whole model. The only overlaps are the designed ones already recorded: insert knurls, motor-face threads and IMU shanks.
  - Thread engagement: M3 ≥ 4.5 mm, M2.5 4 mm.
  - Every insert can be pressed in from a free face.
  - The set screw clears by ≥ 1.5 mm, turned about the axle in 3° steps.
  - Heads sit on their seats; the boards sit on their posts.
  - Straps and foam touch the pack without overlap; the pack cartridge drops 60 mm clear.
- `wheel/check_wheel_on_chassis.py`: 6 of 6 rows pass (16 min). Its swept-ring envelope put the set screw 1.378 mm from the button heads. That ring puts the screw's maximum radius along its whole length, so the set screw is now swept by rotation, as above.
- `check_battery_ballast.py`: all ten rows pass. The straps and foam add no overlaps. a_tip is 1.784 m/s², against a 1.582 minimum (was 1.763).
- `chassis-v1.step` rebuilt. The full `check_layout.py` was not rerun; its set-screw label and harness note were updated.

**Changed docs:** the joint register (J01, J03, J04, J05, J06, J11A, J11B, J12, J13, J15B, J16, release actions), `BOM.csv`, the chassis `BOM.md`, the CAD and frame-split READMEs, `research/axle-stack.md` and the engineering checklist.
- `BOM.csv` rows: CH-011, CH-030, CH-036, CH-038, CH-055, CH-057 and CH-060 updated; CH-073 to CH-082 added.
- The CH-030, CH-035 and CH-038 rows had unquoted commas that spilled into extra columns; they are repaired.

**Open:**
- coupons: tongue inserts (1.85 mm walls), tub-boss inserts (1.35 mm walls), driver posts;
- strap and foam source; strap ≤ 1.5 mm thick; pack shock/inversion test;
- facing the M3 × 3 set screws (cup intact, hex depth for the 1.5 mm key);
- M2.5 head diameter;
- tool access with the body on and lifted;
- the driver move against the PCB-03 connector reserves that D-028 found failing in `check_layout.py`.

## D-029

**2026-10-01 · Chassis / nose lid (J08) · ACTIVE; lead bend to confirm at assembly**

**Why:** `check_layout.py` row `front_panel_lifts_off_forward` failed after D-027. The lid's lead hump reached Z 58.6, but the front panel's bottom edge is Z 58.0, and the panel slides forward over the nose to come off (171 mm³ against `BALL_POD`).

**Changed:** `FRONT_RANGE_LEAD_RESERVE_H` goes from 3.0 to 2.0 mm, so the hump top drops from Z 58.6 to Z 57.6, 0.4 mm under the panel's path. The 3.0 mm was a D-027 modelling allowance, not a builder decision. 2.0 mm still leaves room for a 90° bend in the AWG30 J10-8 lead (about 0.5 mm OD) at the solder joint. The cap's top notch follows the hump. The lid loses 0.077 cm³ (about 0.04 g), so the nose mass row is unchanged.

**Checks:** `check_nose_joints.py` 12/12; `front_panel_lifts_off_forward` passes in the full `check_layout.py` (see D-031).

**Changed docs:** joint-register J08 lid note.

**Open:** confirm the soldered lead bends within 2 mm above the S3B-PH pins.

## D-031

**2026-10-02 · Chassis / driver boards (J15B), inline motor pairs, motor face screws · ACTIVE; supersedes the D-030 J15B layout**

**Why:** the full `check_layout.py` failed four rows after D-030:
- **Driver boards:** the #3297 boards overlapped the PCB-03 J31–J34 edge-connector reserves (up to 598 mm³) and the mated Micro-Fit+ plugs (up to 328 mm³). With the long side along X, a board needs 25.4 mm, but only 21 mm is free between the plugs (X 37) and the body-mount doglegs (X 58). D-030's 5 mm rearward move made it worse, and its posts and M2.5 screws also sat in the plug reserves.
- **`rotating_screws_swept_clear`:** the axle set screw passed 1.4 mm from the motor face-screw head, against a 1.5 mm minimum. The model drew the D-030 ISO 7380 head as a full-radius cylinder.
- **IMU row:** it read the deck top from the deck's bounding box, which the D-030 driver posts now raise to Z 66.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Driver boards (J15B):** both turned 180° from the STEP, long side along Y, at X 38.5–56.3, |Y| 31.3–56.9 (`DRIVER_CENTER_X` 47.4, `DRIVER_Y` 44.2). The hole edge faces rearward on both. The terminal block is inboard on the left board and outboard on the right. The four D-030 posts, inserts and screws move to (41.05, ±34.04) and (41.05, ±54.36): through the plated holes (checked), 0.5 mm off the PCB-03 edge and behind the body M4 feet (X 54, which rule out front-edge posts).
- **Inline motor pairs:** the reserves are now set per side (`MOTOR_INLINE_RESERVE`). The left pair stays along X over its board, raised 0.6 mm to clear the M2.5 heads (Z 69.1). The right pair stands along Y at X 50.9–57.9, between the outboard terminal block (0.4 mm) and the dogleg.
- **Motor-lead harness branch:** narrows to 7 mm and runs across the deck at X 30–37, behind the posts and clear of the IMU.
- **Motor face screws:** the heads are modelled as an ISO 7380 spherical cap (dk 5.7, k 1.65) instead of a cylinder. The set-screw sweep clears again.
- **Mass register:** the driver row follows `DRIVER_CENTER_X`. Total 2626.1 g, CoM (+19.17, 0.16, 105.30), a_tip 1.786 m/s² against 1.582.

**Changed in `check_layout.py`:** the IMU row takes the deck top from `DECK_Z + 2`.

**Checks:**
- Full `check_layout.py`: **119/119 pass** (16 min).
- `check_frame_fasteners.py`: 9/9. `check_battery_ballast.py`: all pass. `check_nose_joints.py`: 12/12.
- Driver sweep (boards, posts, inserts, screws, harness branch and inline pairs against the whole model): no clashes. The closest gaps are 0.4 mm (right terminal block to its inline reserve) and 0.5 mm (inner posts to PCB-03).
- `chassis-v1.step` and `body-chassis.step` rebuilt.

**Changed docs:** joint-register J15B.

**Open:** post coupon (unchanged from D-030); the right board's outboard terminal block needs a lead path to its inline pair; confirm board hole positions on a received board; tug and vibration tests (D-030).

## D-032

**2026-10-02 · Chassis / main fuse holder (CH-028, CH-029) · ACTIVE; CH-028 stays HOLD for an India source**

**Why:** CH-028 was HOLD because the CAD (an envelope in the +Y channel beside the tub) and the BOM note (a PCB-mount holder on PCB-02) disagreed. `RP-02-electrical/board-specs.md` places the pack interface tile **beside the battery tub** (or on PCB-03's front edge) and requires the main fuse to be source-adjacent (PA-02). PCB-02 is on the rear panel, about 100 mm from the pack, so it is ruled out. The builder chose an inline holder beside the tub.

**Found:** the D-028 channel envelope (24 × 10 × 10 mm) could never hold an ATO fuse. The fuse alone is 19.1 × 5.1 × 18.8 mm with its blades. The channel is 11.3 × 19.6 mm, so no ATO holder fits there in any orientation. A free-space search for the holder (30 × 10 × 26 mm, all six orientations, 0.5 mm clearance) found room only above the deck. The builder chose the spot above the +Y channel, on a deck bracket.

**Changed in `body_chassis_model.py`:**
- **Holder:** `PACK_FUSE_HOLDER_BOX` is now the Littelfuse 0FHA0001ZXJ inline ATO holder (16 AWG leads, 20 A at 32 VDC, 30 × 10 × 26 mm with the fuse, per the Littelfuse catalog). It sits at X 52–82, Y 39–49, Z 73–99: wire axis along X, fuse loading from the top, about 25 mm above the disconnect pair.
- **Bracket:** on the front deck print, a 6 × 8 mm column at X 75–81 (in front of the body M4 foot, 1.0 mm clear) and a 2 mm shelf under the holder (`FUSE_BRACKET_COLUMN`, `FUSE_BRACKET_SHELF`).
- **Bosses:** the front tub bosses no longer take their Y from the fuse box. It is fixed at 34.35 (unchanged).
- **Mass register:** frame +0.8 g (bracket 1.32 cm³ at 0.571 g/cm³), now 229.9 g. The pack-interface row follows the holder box. Total 2626.9 g, CoM (+19.19, 0.17, 105.43), a_tip 1.786 m/s² against 1.582.

**Changed in `check_layout.py`:** in the power running-gap sweep, the holder's contact with its own bracket shelf counts as mounted, like the E-stop on its well.

**Checks:**
- Full `check_layout.py`: 119/119.
- `check_battery_ballast.py`: all pass. `check_frame_fasteners.py`: 9/9.
- Holder and bracket sweep against the whole model: no clashes; 0.5 mm to the left inline motor-pair reserve, 1.0 mm from the column to the M4 foot.
- STEPs rebuilt.

**Changed docs:** `BOM.csv` CH-028 row, the chassis `BOM.md` fuse paragraph, the CAD README.

**Open:** an India source for 0FHA0001ZXJ or an equivalent inline ATO holder; check the received body against the envelope; confirm 16 AWG leads for the 15 A fuse; how the holder is tied to the shelf; bracket print. Fuse access needs the body off.

## D-033

**2026-10-02 · Chassis / frame print units and hub cap (CH-001, CH-012, CH-058, CH-059, CH-073–CH-075, CH-077; J03, J05, J06, J16) · ACTIVE; HOLD on printer/orientation review, junction coupons and a cap retention test**

**Decision:** the builder asked to implement the fastener review. Two of its recommendations are adopted:

- **Frame modules.** Each end of the frame is one print: deck, both rails and crossmember. J05, J06 and J16 are deleted, with their ten M3 screws (CH-073, CH-074, CH-075) and ten of the fourteen CH-077 inserts. The two modules join only through the two J04 carriers, which stay removable.
- **Hub cap.** One central ISO 7380 M3 × 10 per cap, into a tapped hole in the steel stub's spigot end, replaces the six M2 × 6 thread-forming screws (CH-059 goes from 12 to 2).

The review's other proposals are not adopted here. They need physical evidence first: a screwless nose lid, stretch-fit tyres or fewer ring screws, integrated carriers, a two-screw keel, and a hinged hatch. Everything else keeps its hardware.

**Why:**

- The frame split had no printer or service reason. The frame-split study kept the rails and crossmembers separate only so their joints could be reviewed. No service step removes a rail from its deck or crossmember.
- The split was also defective. `frame_deck("REAR")` was three solids: its two J16 screw pads sat 1.00 mm off the deck plate, so the rear J16 screws clamped detached pads onto the rails, not the deck.
- The J05/J06 tongues carried inserts in 1.85 mm walls, an open coupon risk. Fusing removes them.
- The six cap screws only retain a cosmetic cover. One screw keeps the cap removable for wheel service.

**CAD changed:**

- [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py):
  - New `frame_module(region)` gives `CHASSIS_FRAME_FRONT_MODULE` and `CHASSIS_FRAME_REAR_MODULE`. They replace the labels `CHASSIS_RAIL_*`, `FRONT_CROSSMEMBER`, `REAR_SKID_CROSSMEMBER` and `CHASSIS_DECK_WITH_BODY_INTERFACE`.
  - The tongues, pockets, J05/J06/J16 screw and insert bores, the J16 deck ears and the J05/J06/J16 hardware are removed, along with their constants.
  - Where the deck covers a crossmember, the crossmember rises to the deck underside (`FRAME_MODULE_FILLS`): front Z 51 → 52, rear Z 48 → 52 at X −41 to −32. The J10-8 cable bore is recut through the front fill.
  - The rear rails keep their widened end as a gusset into the crossmember.
  - J04 receivers, keys, body-nut socket paths, tub, bosses, posts, the D-032 fuse bracket, pod inserts, keel inserts and the cable-tie lug are unchanged.
  - Stub: `STUB_CAP_TAP` adds an M3 tapped hole in the spigot end, 8 mm of thread and a 9.5 mm drill, which leaves 4.5 mm of steel to the D-shaft bore. `_check_wheel_interface()` now also checks the tap.
- [`wheel/wheel_model.py`](01-chassis/v1/cad/wheel/wheel_model.py):
  - The cap has a central Ø3.4 hole and a Ø6.2 counterbore. The head sits 0.25 mm under the boss top, so the robot is 202.0 mm wide (was 202.6).
  - A Ø9 column under the head stops 0.65 mm inside the wheel-screw heads and 0.6 mm above the spigot tip.
  - Two Ø1.8 × 1.5 mm pegs at R12.2 (30°/210°) sit in Ø2.1 × 1.8 mm hub holes and clock the cap. The six M2 pilots are gone.
- `frame-split.step.py` now shows the two modules and the hatch.

**Counts:** screws 90 → **70** (−10 frame, −12 M2 cap screws, +2 central cap screws), inserts 55 → **45**. Frame prints 11 → 5: two modules, two carriers, the hatch.

**Mass register:**
- `CHASSIS_PRIMARY_FRAME` goes from 229.9 to **219.1 g**, CoM (17.71, 0.15, 46.73):
  - −10.7 g for the ten screws and −3.8 g for the ten inserts, measured from the solids at 7.9/8.5 g/cm³;
  - +3.7 g for the measured +6.52 cm³ of printed volume at 0.571 g/cm³ (fills, filled bores and pockets).
- `AXLE_BEARINGS_AND_STUB_SHAFTS` goes from 51.4 to 50.4 g, for the two tapped holes.
- `WHEEL_L/R` stays at 92.5 g: `check_wheel.py` gives 92.5 g with the M3 × 10 in place of six M2 × 6.
- Register total 2626.9 → **2615.1 g**, CoM (+19.15, 0.17, 105.69); a_tip 1.778 m/s² against the 1.582 minimum.

**Checks (2026-10-02):**
- `check_frame_fasteners.py`: **9/9**. The new row `frame_modules_are_single_prints` replaces `tongue_fit`: each module is one solid (front 75.84 cm³, 75 × 128 × 41 mm; rear 50.37 cm³, 34 × 132 × 22 mm), no J05/J06/J16 hardware or split part remains, and the rear deck plate fills both rear-rail probes. No new clashes; the accepted overlaps are the existing insert knurls, motor-face threads and IMU shanks, now against the module labels. The run used the patched model before the mass rows changed; the rows do not affect geometry.
- `check_nose_joints.py` 12/12, `check_rear_keel.py` 21/21, `check_battery_ballast.py` all pass (no new tub clashes with the fused front module).
- `wheel/check_wheel.py` **25/25**. New rows: cap-screw engagement in the stub (6.9 mm), head seated and recessed (0.25 mm), column clearances (0.65 mm to the wheel-screw heads, 0.6 mm to the spigot), and pegs in the hub holes (1.38 mm wall to the hex). The pocket keep-out row now excludes the cap screw, which runs into the stub on the axle line, like the wheel screws.
- `wheel/check_wheel_on_chassis.py` **6/6**. The central screw sweeps 3.67 mm clear of the bearing cap and meets the tapped stub with no overlap.
- `check_layout.py` full run: **119/119 pass** (~4.6 min). The first run failed only `rotating_screws_swept_clear`, whose expected screw count still assumed six cap screws per wheel. Every gap passed (minimum 1.64 mm against 1.5 mm; the cap screw is 3.67 mm clear). The count is now `2 × (1 + 3 + 6 + 1)`. The updated frame label lookups (crossmembers, nose inserts, fuse holder, IMU deck) are exercised and pass. Chassis front is now X 92.0 (was 93.65) because the J16 ears are gone.
- `chassis-v1.step`, `frame-split.step`, `wheel.step`, `wheel-pair.step` and the local `body-chassis.step` rebuilt; `write_outputs.py` reports regenerated. Those reports also pick up earlier stale values (688 ZZ positions, the A21 sensor and the battery X).

**Changed docs:** joint register (J03, J05, J06, J16, summary, release actions), chassis `BOM.md`, `BOM.csv`, the CAD, wheel and frame-split READMEs, the engineering checklist and the fastener review's status line.

**BOM changed:**
- CH-001 is re-specified as two frame modules, two carriers, the tub and the hatch.
- CH-012 gains the spigot-end tap.
- CH-058 and CH-059 are re-specified: CH-059 is ISO 7380 M3 × 10, 2 each.
- CH-077 goes from 14 to 4 (J11A only).
- CH-073, CH-074 and CH-075 are retired; do not reuse the IDs.

**Open:**
- Printer and orientation review for each module. The front module has features above and below the deck (driver posts and fuse bracket above; rails and tub below). The rear module prints deck-down.
- Junction coupons: rail-to-crossmember and crossmember-to-deck under caster and skid loads.
- Deck coplanarity across the motor bay through the J04 carriers.
- Cap retention and peg fit on a coupon. Tapped-hole depth on the stub drawing.
- Physical retention of the remaining joints, as before.

## D-034

**2026-10-03 · Body / audio speaker (BO-001; BO-002–BO-006 registered) · ACTIVE; speaker SELECTED, not ordered; HOLD on received-part measurement and bench listen**

**Decision:** the builder locked the body speaker as the **Visaton K 50 WP – 8 Ω (art. 2915)**, bought from [element14 India, order code 1683894](https://in.element14.com/visaton/2915/speaker-k-50-wp-8-ohms/dp/1683894). The body audio chain from the RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2 is entered in the project BOM as BO-001 to BO-006. Only the speaker is selected. The amplifier, front end, mic boards and cables stay `CANDIDATE` or `HOLD`.

**Why:**

- It is the driver the CAD already carries: Ø50 × 18 mm, Ø46 cutout, 48 g, behind the front-panel grille with a sealed Ø54 back cavity (X 77–92.5). No geometry or mass change.
- 8 Ω and 2 W rated / 3 W max match the MAX98357A on the 5 V `PB-AUDIO-OUT` branch (1.75 W, about 0.7 A peak, under the 2.0 A e-fuse).
- Of the 50 mm Visaton drivers it has the widest range (180 Hz–17 kHz, fs 300 Hz) and the lowest price seen (about €5.74 in the EU).
- Alternatives compared on 2026-10-03:
  - **K 50 (2901, metal basket):** 250 Hz–10 kHz, fs 400–500 Hz, and it cost more. Kept as the fallback if 2915 is unavailable.
  - **K 28 GI (2830):** 0.5 W, 450–7000 Hz, fs 730 Hz. Too quiet and thin as the only speaker, and the MAX98357A could overdrive it.
  - **Local generic 50 mm 8 Ω (for example Robomart, ₹174):** cheaper, but with no datasheet, so depth and resonance are unknown until measured. Most local "2-inch full-range" units are Ø52–55 mm and 25–45 mm deep, too big for the front cup and cavity.

**BOM changed:** [`BOM.csv`](BOM.csv) gains the `body` owner and rows BO-001 to BO-006: the speaker (`SELECTED`), PCB-05, the MAX98357A, 2 × ADAU7002, 4 × PCB-06 mic boards with IM73D122V01, and the W12/W26–W28 audio cable set. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) is the body v1 snapshot.

**CAD:** no change. `body_v1_model.py` already models the K 50 WP outline (`SPEAKER_*`), and the `BODY_AUDIO` mass row (60 g) already counts it at 48 g.

**Unverified:**

- element14 India price and stock for 1683894 were not read; check them at order.
- Received outline, depth and mass against Ø50 × 18 mm and 48 g.
- Low-end response in the 15.5 mm sealed cavity, and speaker-to-mic coupling (RP-05 `AR-60`).
- Flange bond and grille seal method.

**Next:** order BO-001 with a MAX98357A bench breakout. Caliper and weigh the speaker, update `BODY_AUDIO`, and bench-listen to the character cues and a music clip at a capped gain.

## D-035

**2026-10-03 · Body / audio bench amplifier (BO-007) · ACTIVE; SELECTED, not ordered; bench only**

**Decision:** the builder selected the [SmartElex MAX98357A I²S breakout from Robocraze](https://robocraze.com/products/smartelex-max98357a-i2s-audio-breakout-amplifier-for-raspberry-pi-and-microcontrollers) (₹195, 78 in stock on 2026-10-03) as the bench amplifier. It is BO-007, qty 2 (one spare). It drives the BO-001 speaker until PCB-05 exists. The installed amplifier is still the MAX98357AETE+T on PCB-05 (BO-003, `CANDIDATE`).

**Why:**

- It has the same chip as BO-003, so the i2s0 overlay, wiring and software carry over to PCB-05 unchanged.
- It is the "Adafruit #3006-class breakout" that the [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.7 and D-034 name for Phase A, and it is in stock in India.

**Bench wiring:** BCLK → GPIO18, LRC → GPIO19, DIN → GPIO21 (SDO0), SD → GPIO23 (`AMP_SD`), VIN → 5 V, GND → GND. The speaker goes on the screw terminal. Leave GAIN open to start.

**Differences from PCB-05 (accepted for the bench):**

- **Not off by default.** The listing publishes no schematic. If the board follows Adafruit's layout, SD has a 1 MΩ pull-up to VIN, so the amp is on at power-up. A 100 kΩ pull-down against that gives about 0.45 V, which is (L+R)/2 mode, not shutdown (< 0.16 V). Fit about 10 kΩ from SD to GND if off-at-boot is wanted. GPIO23 high (3.3 V) selects the left channel.
- **No 100 Ω series resistors** on BCLK, LRC or DIN. Do not stream into it while it is unpowered.
- **Screw terminal, not JST GH**, and no mounting in the CAD. It is not an installed article.

**BOM changed:** [`BOM.csv`](BOM.csv) gains BO-007. BO-003's release check now points at it. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) lists it under bench articles.

**CAD:** no change.

**Unverified:** the SD pull-up value and the default gain on the received board; its outline; the listing's stock and price at order.

**Next:** order BO-007 with BO-001. Check the SD network on receipt, then run the bench listen and the Pi 5 two-lane capture-plus-playback test.

## D-036

**2026-10-03 · Body / audio microphones (BO-012, BO-005) · ACTIVE; SELECTED, not ordered; HOLD on PCB-06 layout and the array tap test**

**Decision:** the builder locked the body microphone as the **Infineon IM73D122V01XTMA1** (PDM, PG-LLGA-5-4, bottom port), bought from [element14 India, order code 4125831](https://in.element14.com/infineon/im73d122v01xtma1/mems-microphone-pdm-122db-pg-llga/dp/4125831). It is the new row BO-012: four installed, one on each BO-005 (PCB-06) board. Buy six (two reflow spares). The array stays at **four mics**: FRONT_L/R and REAR_L/R.

**Why this mic:**

- **73 dB(A) SNR** (about 21 dBA self-noise). Cheap PDM mics are about 64 dB (about 30 dBA). The difference shows in a quiet room at 2–3 m, which is the quiet-sleep wake-word case (RP-05 `audio-path.md` rule 2), when the Pi cooler is likely off. With the fan or motors running, their noise dominates and the gap narrows.
- Bottom port, which the PCB-06 design needs (mic on the inboard face, listening through a Ø0.8 mm hole). Matched to ±1 dB, 122 dB SPL overload, IP57. Runs in its high-performance clock window at the 3.072 MHz the ADAU7002 gives at 48 kHz.
- It is the part the RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.2 named, so the CAD (`MIC_PACKAGE_SIZE` 4 × 3 × 1.2) and the `BODY_AUDIO` mass row need no change.
- Cost: six cost about ₹1,500–2,000. A cheaper mic would save about ₹1,200–1,700 of the ₹6,500–11,000 audio estimate; the builder kept the SNR.
- Availability: the builder saw 9,000+ in stock at element14 India. The 45-week figure on the page is Infineon's factory lead time for orders beyond that stock. JLCPCB (C5563886) showed 0 stock, so the mics go to JLCPCB as consigned parts or are reflowed by hand.

**Alternatives:**

- **MEMSensing MSM261D3526Z1CM:** PDM, bottom port, 64 dB SNR, 3.5 × 2.65 mm. The cheaper fallback; PCB-06 is not laid out, so the footprint change would be free. Not the **MSM261D3526H1CPM**, which is top port.
- **Infineon IM69D128S:** 69 dB SNR at a similar price. No gain.
- **IM69D130:** not for new designs.

**Why four, not six:** RP-05 `AR-01` asks for four synchronised body mics at the existing ports. Each ADAU7002 carries one stereo pair on one Pi 5 capture lane, so four mics use SDI0/SDI1 (GPIO20/22). Six would need a third ADAU7002, a third lane (GPIO24, another `CA-06` change), two more PCB-06 boards and shell ports, and new placement checks. A ±70 mm four-mic rectangle already supports direction finding and beamforming.

**BOM changed:** [`BOM.csv`](BOM.csv) gains BO-012 (`SELECTED`); BO-005's supplier column points to it. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) lists BO-012.

**CAD:** no change.

**Unverified:** element14 price and stock at order; the received package against 4 × 3 × 1.2 mm; PCB-06 layout; channel order and L/R convention by the array tap test.

**Next:** order six with BO-001 and BO-007. Store them sealed. Lay out PCB-06 around the PG-LLGA-5-4 land pattern.

**Array checks (added 2026-10-03, builder review of the side-only layout):** the four side ports stay. The array is centred on the yaw axis (X 16), 76 × 140 mm, and keeps the mics away from the forward speaker. Three checks are added to the BOM release checks:

- **Calibration (BO-012):** the body shadows the far-side mics above about 1.5–2 kHz (`E`), so free-field DOA is biased. Each robot gets a spin-in-place calibration: loudspeaker at 1 m, chirp every 10° as the base rotates, measured responses stored for DOA and beamforming.
- **Noise (BO-005):** FRONT_L and REAR_L are about 30 mm from the yaw-servo envelope; the −Y pair is far from it. Before ordering PCB-06, run the yaw servo and the cooler at full speed and compare left and right channels. If the +Y pair is worse, isolate the board mounts rather than move the ports. Confirm the cooler exhaust does not reach the front ports (`AR-61`).
- **Port seal (BO-005):** the boot must seal between the board and the shell skin.

## D-037

**2026-10-03 · Body / microphone mounting (BO-005, BO-006; BO-013, BO-014 new) · ACTIVE; DESIGN in CAD, checks green; HOLD on a printed boss coupon and the PCB-06 layout**

**Decision:** the four PCB-06 mic boards mount on the **shell**, not the body frame.
- Each board lands on a printed boss on the inner skin, coaxial with its side port.
- A closed-cell foam gasket ring in a pocket round the port seals it.
- Two M2 × 4 thread-forming screws clamp it.
- The side-entry GH header is dropped. Each board carries a soldered, pre-crimped GH 4-way lead that plugs into PCB-05 after the shell is lowered.

This replaces "screwed to the body frame" in BO-005 and RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.7. It also replaces the GH header at the mic end of W27 in the RP-06 [connector schedule](../02-prototypes/RP-06-cad/connector-schedule.md).

**Why:**

- **Nothing held the boards.** The CAD had no fixing. There is also no frame material at the ports: between the lower rail (Z 69) and the upper rail (Z 126) the frame side is open, apart from the corner posts about 5 mm from each board.
- **A frame-mounted board cannot seal to the shell.** The shell lowers vertically, so a boot between board and skin would be wiped sideways as the shell drops. The old Ø6 × 5 boot also overlapped the leaning skin unevenly: 26 mm³ at the front ports, 2.4 mm³ at the rear. No check covered it, because the mics were outside `check_shell_frame_fit.py`.
- **On the shell, port and seat are one print.** They stay coaxial with no frame-to-shell tolerance between them. The screws compress the gasket squarely to a hard stop, so the seal does not depend on how the shell lands.
- **The array stays rigid.** All four mics are fixed to one part (RP-05 `AR-64`), and the D-036 spin calibration absorbs print tolerance. The boards also come off the frame that carries the yaw servo (the D-036 noise concern).
- **The header had to go.** The boards ride down with the shell past the frame's upper side rails (|Y| ≤ 68). The 4.25 mm GH header would hit them. With a soldered lead, the inboard-most part is a screw head at |Y| 69.0, 1.0 mm clear.

**Geometry** (`body_v1_model.py`: `MIC_*` constants, `_mic_boss`, `_mic_boss_cuts`, `_mic_board`):

| Item | Value |
|---|---|
| PCB-06 | 12 × 14 × 1.0 mm (was 12 × 9.5). IM73D122 on the inboard face, on the port axis, over a Ø0.8 hole. Ø2.2 screw holes 5 mm above and below the port. Four lead pads beside the mic |
| Boss | 16 × 17 mm flat seat at \|Y\| 71.3, filled out to the sloped skin. Its upper face rises at 45°, because the shell prints roof-down. Depth from seat to inner skin is 2.5 mm at the front port axis and 3.7 mm at the rear |
| Gasket | Ø6.5/Ø2.0 × 1.0 mm closed-cell foam in a Ø7.0 × 0.7 mm pocket. The board lands on the seat, so compression is 30% |
| Port | Ø2.0 through boss and skin (was Ø3.0 through the skin). Skin-to-mic chain is 5.9 mm front and 7.1 mm rear. Helmholtz estimate 13–23 kHz for a 1–3 mm³ mic front chamber (`E`) |
| Screws | M2 × 4 pan head, thread-forming, into Ø1.6 × 3.3 mm blind pilots: 3.0 mm engagement, at least 0.98 mm of skin left beyond each pilot (front top screws) |
| Lead | 4 × AWG28 lying flat on the inboard face, leaving toward the body centre. About 150 mm front and 200 mm rear (`E`). The +Y boards plug into `J5-2`/`J5-3`, the −Y boards into `J5-4`/`J5-5` |

**Assembly:** on the bench, stick a gasket to each board and screw the boards to the loose shell, in the same step as the wheel-arch pods. Leave the leads hanging free. Lower the shell. With the front panel and speaker still off, plug the leads in through the front service aperture. Unplug them before lifting the shell off.

**BOM changed:** [`BOM.csv`](BOM.csv):
- **BO-005:** respecified (shell-mounted, 12 × 14 mm, no header, DATA series resistor).
- **BO-006:** W27 becomes four pre-crimped GH leads soldered at PCB-06.
- **BO-013 (new):** M2 × 4 thread-forming screw, 8 off, `CANDIDATE`. Same family and pilot qualification as CH-039.
- **BO-014 (new):** mic port gasket, 4 off, `CANDIDATE`.

[`02-body/v1/BOM.md`](02-body/v1/BOM.md) is updated to match.

**CAD and checks:**
- The shell gains the four bosses, and the boot and port placeholders are removed.
- New [`check_mic_mounts.py`](02-body/v1/cad/check_mic_mounts.py): 15/15 checks pass (16/16 after the vendor-STEP addendum below), written to `generated/mic-mount-fit.json`. It covers seat, gasket, sound path, port, screw depth, rail clearance, and clashes against the shell, each other and every body and chassis part.
- `check_shell_frame_fit.py` lowers the 32 mic parts with the shell, against PCB-05 and its edge connectors added to the fixed parts. Result: no overlaps (29 min; 69 min after the vendor-STEP addendum, still clean).
- `check_body_layout.py`: 14/14 checks pass.

**Mass:**
- `BODY_SHELL_AND_PANELS`: 246.7 → 250.7 g at (19.8, 0, 93.5).
- `BODY_AUDIO`: 60 → 61 g at (74.5, 0, 102.1).
- Whole robot: 2,423.1 → 2,428.1 g, CoM (+18.47, +0.24, 106.01) mm.
- Neutral a_tip: 1.711 → 1.709 m/s². Head-pose bound: 1.708 → 1.706 m/s². Paper screen: 1.582.
- Propagated to `01-system/dimensional-baseline.md` v1.15 and `mass-envelope-ledger.md` v0.19.

**Not changed:** the chassis v1 model's legacy copy of the body (`01-chassis/v1/cad/body_chassis_model.py`) and its `check_layout.py` mic checks still describe the old frame-side boards. Chassis v1 does not fabricate the body.

**Unverified:**

- Print: a side-wall coupon with one boss. Check seat flatness, the Ø1.6 pilots drilled to 3.3 mm, no witness mark on the outer skin over the pilots, and the roof-down 45° boss face.
- Seal: a tap test with the port taped and open, and gasket compression set after a week clamped. The gasket material and source are open.
- The thread-forming screw itself (CH-039 qualification) and repeated-service strip resistance.
- Reaching and mating the four GH plugs at PCB-05 through the front aperture, and the lead lengths. The leads are not routed in CAD.
- PDM over a 200 mm AWG28 lead: CLK and DATA integrity at 3.072 MHz. Termination is set in the PCB-05/06 layouts.
- The mic front-chamber volume behind the resonance estimate.

**Next:** print the boss coupon with the next shell test print, lay out PCB-06 to the 12 × 14 outline (everything inboard within 1.3 mm of the board), and pick and punch a gasket sample.

**Vendor STEP (added 2026-10-03, builder review):** the mic package was a 4 × 3 × 1.2 mm placeholder box. It is now Infineon's own PG-LLGA-5-4 STEP, downloaded from the Infineon package page into [`02-body/v1/cad/purchased/`](02-body/v1/cad/purchased/README.md) with its SHA-256.
- The body measures 4 × 3 × 1.30 mm; the datasheet gives 1.2 ± 0.1 mm.
- **The sound port is 0.68 mm off the package centre** along the 4 mm side, away from pins 1–4 (datasheet Fig. 12/13). The placeholder had it at the centre.
- The package is now placed by its port, which sits on the port axis and the Ø0.8 PCB hole. The body extends 2.68 mm toward the frame post and 1.32 mm toward the lead pads.
- `check_mic_mounts.py` now checks the port position and the vendor outline: 16/16 pass.
- **PCB-06 layout:** use the Fig. 13 land pattern with the PCB hole at the port, not at the package centre. Everything inboard must stay within 1.3 mm of the board face.

## D-038

**2026-10-03 · Power boards (PCB-01, PCB-03, PCB-10; CH-017, CH-023, CH-041–CH-043; CH-083–CH-086 new) · ACTIVE; DESIGN; HOLD on TIFPS0629 bench acceptance and MOT3001 winding R/L**

**Why:** the whole-system power review found that the RP-02 power-board spec still assumes the custom PCB-01, Pololu DRV8874 carriers and the Pololu #4804 motor. The build uses the bought TIFPS0629 (D-019), Adafruit #3297 DRV8833 boards (D-019) and the MOT3001-6V230RPM (D-003). RP-02 is read-only, so the build deltas now live in [04-pcbs/power-boards.md](04-pcbs/power-boards.md).

**Decisions:**

- **Motor-bus TVS: SMBJ8.5A replaces SMBJ10A.** The DRV8833's `VM` absolute maximum is 11.8 V (TI SLVSAR1E). The SMBJ10A's 11.1–12.3 V breakdown and 17 V clamp do not protect it. The SMBJ8.5A breaks down at 9.44 V minimum and clamps at about 10.9–11.3 V at 5 A (`E`). The bus never exceeds the 8.4 V pack because the charger is cut off by `CHARGE_ABSENT`. Each #3297 keeps at least 100 µF + 0.1 µF at `VM`.
- **Power entry:** `PB-DRIVE-L/R` lands on the #3297 `VM` pin, not on the polarity-protected `Vmotor` terminal, which could block regeneration.
- **Sleep gate:**
  - A 74LVC1G08 on PCB-10 drives both `SLP` pins from C3 GPIO21 AND `BASE_READY`.
  - It replaces the series N-FET stages. A 3.3 V signal passed through an N-FET falls below the DRV8833's 2.5 V `nSLEEP` `VIH`.
- **Fault:** both `FLT` pins are wired-OR to GPIO9. Firmware latches any fault and requires a fresh arm, which defeats the chip's 1.35 ms auto-retry.
- **Inputs:** GPIO13/14 change from DIR to a second LEDC output (`IN2`), so both directions run in slow decay. Brake is `1, 1`. C3 caps the duty at `6.0 V / V_bus` (71% at 8.4 V).
- **Current observation:** two bidirectional INA181A2 monitors (5 mΩ, 0.25 V/A around 1.25 V) on the PCB-03 drive feeds. They replace the DRV8874 `CS` signal. No C3 pin is added.
- **Hardware limit:** the fitted 0.2 Ω sense resistors chop each board at 1.6–2.4 A.
- **Regeneration:** the 3 A / zero-below-0 °C rule holds with margin. Slow-decay deceleration returns at most `E_b² / (4 · V_bus · R)` ≈ 0.32–0.45 A per motor (`E`). Below 0 °C, C3 stops by brake and coast only.
- **PCB-01 acceptance:** the TIFPS0629 publishes no trip points, so it must pass a bench window before cells are connected:
  - overcharge 4.275–4.35 V per cell;
  - over-discharge 2.30–2.70 V per cell, so the pack cuts out after `ENERGY_OK`;
  - discharge overcurrent ≥ 15 A, ≥ 20 A preferred, so the motor gate opens first;
  - short-circuit trip ≤ 1 ms, ≤ 30 mΩ series resistance, ≤ 16 µA quiescent, ≤ 4.5 mm height.

  The AC72ABD and 103AT-2 stay separate from the module.
- **Folder:** `04-custom-pcb/` is replaced by [04-pcbs/](04-pcbs/README.md), with a register of every board.
- **New BOM rows:** PCB-08 (CH-083), PCB-09 (CH-084), PCB-11 (CH-085) and **PCB-12**, a new ID for the C2 head carrier (RP-02 `CCD-HDL-02`, CH-086).

**Recomputed (`E`):**

- Peak pack current at a 6.0 V pack is about 10.2 A (11.0 A at the upper chopping corner), below the historical 11.7 A. The 15 A main fuse and 3 mΩ gate shunt stand.
- The OFF budget is 34–84 µA plus the module.
- `V_SRC_SAFE` no longer comes from the driver (DRV8833 runs to 2.7 V). The brownout thresholds are unchanged.

**BOM changed:**

- CH-017 and CH-023 release checks.
- CH-041–CH-043 now point to `04-pcbs/power-boards.md`; CH-042 lists the new parts.
- BO-002's folder reference.
- CH-083–CH-086 added.

**CAD:** not changed. `body_v1_model.py` has uncommitted edits from other work. The J10-5/J10-6 labels ("mapping TBD") take the power-boards §2.4 mapping at the next body CAD edit. The RP-06 connector schedule (W06/W07, W32/W33, §3.3) is superseded by power-boards §2.3–2.4 where they differ.

**Open:**

- TIFPS0629 bench acceptance on two received units.
- MOT3001 winding resistance and inductance on receipt, then recheck the TVS and regeneration numbers.
- NTC lead and disconnect (CH-025).

**Update 2026-10-03 (same day):** paper items closed.
- SMBJ8.5A leakage is at most 20 µA at 8.5 V (Littelfuse).
- The drive-feed monitors are one INA2181A2 (dual, separate `REF` pins) with a REF3312 1.25 V reference, fed from a local 3.3 V LDO so the output cannot exceed 3.3 V.
- The `J10-5`/`J10-6` labels in `body_v1_model.py` and `body_chassis_model.py` carry the mapping (strings only, no geometry).
- The temporary `power-review-todo.md` is deleted. Its remaining bench items are tracked in [power-boards.md §5](04-pcbs/power-boards.md#5-open) and CH-023.
