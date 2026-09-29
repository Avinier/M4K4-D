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

**Design direction:** continue chassis engineering from the supplier drawing and clearly labeled CAD assumptions. Put the uncertain face-hole/pilot/shaft interface in replaceable or adjustable parts so a mismatch does not force a complete frame reprint. The [motor interface sheet](01-chassis/v1/motor-interface-sheet.md) is parked, and the [mechanical checklist](01-chassis/v1/engineering-checklist.md) no longer includes a motor-measurement task.

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

**Decision:** the builder accepted the [axle stack](01-chassis/v1/axle-stack.md) architecture and its three choices: the bearing change, the turned one-piece stub, and designing around an absent motor. Per side, the stack is:

- **Stub.** One turned EN8 part carries torque and locates the wheel. It has Ø8 k5 bearing seats, a Ø4.05 bore on the motor's D-shaft (8 mm engagement), a DIN 916 M3 × 2.5 set screw on the flat, a Ø24 flange with three tapped M3, and a Ø10 spigot that centres the wheel.
- **Bearings.** Two **MR148ZZ** (8 × 14 × 4) in a bolt-on printed housing, held between a housing shoulder and a 1.2 mm aluminium cap. Four M3 × 18 screws pass through cap and housing into heat-set inserts in a 5 mm motor plate.
- **Motor alignment.** The motor floats on 0.3 mm of clearance at its pilot and face screws. The face screws are tightened last, through key slots, once the motor has aligned itself to the stub.
- **Wheel.** Three M3 × 6 screws through the web into the stub flange. Removing the wheel needs only those three screws.

**Why:**

- **The modelled stack was not buildable** ([axle-stack.md §1](01-chassis/v1/axle-stack.md#1-why-the-current-stack-cannot-be-built-as-modelled)): no torque path motor → stub → wheel, no bearing retention, an over-constrained motor, and screw heads buried behind the bearings.
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

**CAD change:** `body_chassis_model.py` now models 688 ZZ rings, OD radius 8 mm and 5 mm width. The pair is seated at |Y| 76.5–81.5 and 81.5–86.5; housing shoulder moves inboard to |Y| 76.5, preserving the outer cap, stub shoulder, flange and wheel positions. The outer seat is Ø16 × 10 mm. The set-screw station moves to |Y| 74.8 so its Ø2.5 tap-drill edge nominally clears the first bearing face by 0.45 mm; verify this narrow land on the stub drawing and part. CAD checks were updated to assert the selected bearing and seat dimensions. Supplier STEP/drawing is not available, so the rings remain parametric placeholders.

**Fit and proof gates:** coupon the printed seat Ø15.90–16.10 mm in 0.05 mm steps; verify the actual Ø8 k5 shaft fit, race drag, shield clearance, runout and endplay with delivered bearings. Retain the inner rings by k5 plus Loctite 641 and pass the 100 N outward-hold test for 10 s with <0.10 mm movement. Rerun wheel-to-chassis clearance and full `check_layout.py`; inspect the nominal 0.45 mm edge clearance from set-screw tap drill to first bearing face on the turned-stub drawing. No physical fit, load or retention test has passed.

**Next:** monitor/order from the selected listing when available or obtain the same specified article from a confirmed supplier; request manufacturer, internal-clearance class, drawing and load data; then print fit coupons and run the motor-independent retention fixture. Motor-dependent axle testing remains separately blocked on motor receipt.

---

## D-013

**2026-09-30 · Chassis / nose (CH-007, CH-019, CH-064, CH-065, CH-066; J08B) · ACTIVE; HOLD on bench trip-point check and the PCB-10 J10-8 pin change**

**Decision:** replace the D-011 nose switch with contactless sensing. A TI DRV5055A3 linear Hall sensor on a small board in the pod seat reads a Ø2 × 1 N35 magnet in the touch cap, and the C3 firmware sets the trip point. Two small compression springs return the cap. Details: [nose-hall-board.md](01-chassis/v1/nose-hall-board.md).

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
