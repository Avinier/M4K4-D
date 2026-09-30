# Chassis v1 test system

**Status (2026-09-30):** plan only. No part is received, no fixture is built and no physical gate is passed. This is the test plan for the [v1 BOM](BOM.md) and [joint register](joint-register.md). It follows the release stages in [BOM § Release blockers by stage](BOM.md#release-blockers-by-stage).

The method is to test each subassembly as soon as it exists, then test the complete vehicle under progressively more realistic conditions. Measure each load path before it is buried in the full build, where a failure would be hard to diagnose.

## 0. Rules for every test

1. **Set the pass limit before running the test.** Base it on the required clearance and on whether any permanent movement is acceptable. Changing a limit after seeing the data creates a new gate version ([run-record convention](../../../01-system/run-record-convention.md)).
2. **Test to failure only on coupons or sacrificial assemblies.** Proof-load, without failing, the article that will be used.
3. **All numbers below are proposals.** The axle limits come from [axle-stack § 9](research/axle-stack.md#9-j04-carrier-and-test-plan). The floor-run matrix comes from the [RP-03 gate candidates](../../../02-prototypes/RP-03-locomotion/gates.md). Neither set is frozen or registered.
4. **Record the tested configuration** for every result: part revisions, print process, firmware commit, ballast (M, x, h) and instruments. Every result must say *which hardware passed, under which load and conditions, and with what measured margin*.
5. **Every powered session passes the [workbench scored-test gate](../../../01-system/workbench.md#scored-test-gate):**
   - E-stop verified this session;
   - limits set for this specific test;
   - article restrained;
   - revisions recorded;
   - logging confirmed as writing;
   - an instrument that can resolve the threshold.
6. **A test that still runs but leaves play behind is a finding, not a pass.**

## 1. Receiving inspection: establish the real baseline

Inspect and identify every purchased part and every print before assembly. For each item, record the supplier, lot, mass, key dimensions and any difference from CAD in the [project BOM](../../BOM.csv). Do not infer any of these from CAD or from stock listings.

| Item | BOM | Measure / check |
|---|---|---|
| MOT3001 gearmotor | CH-014 | Face screw pattern, pilot diameter, shaft diameter and D-flat, gearbox length, tapped depth, encoder PPR and direction, no-load current at 6.0 V. These are CAD assumptions until measured ([D-003](../../decisions.md#d-003)). |
| 688 ZZ bearing | CH-015 | Actual 8 × 16 × 5 dimensions, ZZ shields, free rotation, maker and lot, drawing and load data |
| Pololu #2691 caster | CH-016 | Three-hole flange pattern, 29 mm assembled height, ball swivel, screw access from below |
| Adafruit #3297 driver | CH-017 | Board outline and holes, current-limit setting as delivered, default-disabled state |
| Sharp GP2Y0A21 | CH-018 | Outline against the vendor STEP and [D-027](../../decisions.md#d-027), orientation of the lens and ear holes |
| DRV5055A3, magnet, springs | CH-019, CH-065, CH-066 | Magnet size and polarity; spring OD, free length and rate (predicted 0.18 N/mm; see [D-020](../../decisions.md#d-020)) |
| TCRT5000 lead | CH-020 | Lead length, sleeving, connector pinout ([rear-tcrt-lead](research/rear-tcrt-lead.md)) |
| 2S protection module | CH-023 | Real thickness (the CAD placeholder is 2.9 mm), footprint, thresholds, balancing, reset behaviour |
| 25R cells | CH-022 | Diameter (the CAD assumes 18.4 mm max), mass, open-circuit voltage. **Do not assemble the pack to answer a tub-fit question.** |
| Fasteners and inserts | CH-030 … CH-072 | Head seat, length and standard, especially the `OPEN` rows CH-030, CH-055 and CH-060 |
| Every print | CH-001 … CH-058 | Datums, hole and insert-bore diameters, flatness, visible defects. Record the print orientation. |

## 2. Coupons for uncertain interfaces

A failed coupon is a cheap design correction. For every accepted fit, record the printer, material, orientation and slicer settings so the result is reproducible.

| Coupon | Variants | Pass (proposed) | Source |
|---|---|---|---|
| Outer bearing seat | Ø15.90 / 15.95 / 16.00 / 16.05 / 16.10 mm | Free to light press, captured by the shoulder/cap, no race distortion. Record insertion force, drag and shield clearance. | axle-stack § 9.2 |
| Bearing inner ring on the stub, 100 N hold | Real bearings on the turned stub, k5 seat + Loctite 641 | 100 N outward for 10 s: <0.10 mm movement; free rotation after unloading. Test both sides. | axle-stack § 9.3 |
| M3 heat-set insert pull-out | CH-049, CH-054, CH-061, CH-033/063/067 | 100 N axial: no insert movement, no boss split, no permanent bore growth | axle-stack § 9.4 |
| J04 key to rail | One carrier plus two rail coupons | Key seats by hand; datum gap ≤0.10 mm; rails coplanar within 0.20 mm; full engagement without bottoming; no cracks or insert spin after 3 assembly cycles | axle-stack § 9.5 |
| Stub-to-wheel spigot | Spigot bore in the rim material | Fit and seating limit to be defined before the test | J03 |
| Tyre to rim | TPU 95A tyre on the rim with a clamp ring | Seating, clamp torque, no lift at the bead; limit to be defined | J14 |
| Thread-forming screws | M2 × 6, M2 × 8, M2 × 10 in the printed material | Drive and strip torque, repeat-removal count; limit to be defined | CH-059/062/069/070 |
| Inert battery pack | Dimensionally accurate dummy of the finished pack | Fits the tub and hatch with restraint; removal path is clear | J11A, J11B |

## 3. Fixtures and test system

Five fixtures cover most of the work. The [RP-03 rig](../../../02-prototypes/RP-03-locomotion/rig.md) already describes much of the instrumentation and the staged approach. Update its older part choices to the v1 BOM before reusing it.

| # | Fixture | Contents | Used for |
|---|---|---|---|
| F1 | **Coupon pull/fit fixture** | Guarded clamp, calibrated force gauge, calipers, pin gauges | Inserts, bearing seats, keys, 100 N hold |
| F2 | **Side-specific axle rig** | Real carrier, bearings, stub, motor and wheel; controlled radial and lateral loading; dial indicator on the axle datum and the tyre | Axle deflection, runout, endplay, proof load, powered reversals |
| F3 | **Ballasted open chassis** | Adjustable mass and height standing in for the body and head. Measure M and CoM (x, h) at each configuration (scale ±5 g class; x, h ±2 mm class). | Frame load and twist, caster lift, floor runs |
| F4 | **Instrumented drive bench** | Korad KA3005D (30 V / 5 A) with current limit, an independent E-stop that cuts **motor power only**, retained wiring, per-motor current (INA-class), encoder logs, motor and driver temperature, probes on driver enable/fault, logic analyzer on the hazard GPIO and driver enable (≤5 V only, never on the motor rail). **Per-bridge current:** a low-value shunt or clamp probe in each bridge's output leg, ahead of the paralleled junction. Without it, the split between bridges is **unverified**. **Rail transients:** an oscilloscope on the driver supply, or INA monitors at their maximum conversion rate with the resolution stated in the run record ([rig.md § 1](../../../02-prototypes/RP-03-locomotion/rig.md#1-bench-constraints-that-shape-the-rig)). | Commissioning, electrical and thermal tests, fault injection, timing |
| F5 | **Marked floor course** | Tile, laminate, thin rug, threshold strip, 2° slope board, start/stop marks, tape or laser distance, top-down video at ≥60 fps; overhead catch for any later tabletop-edge trial | Guarded floor runs, sensing, endurance |

The instrument table in [rig.md § 5](../../../02-prototypes/RP-03-locomotion/rig.md#5-instrumentation) is the reference for rates and uncertainty. **Timing rule:** a 50 ms detection-to-deceleration claim needs the logic-analyzer path. Video at 30 fps (33 ms per frame) cannot resolve it. Without the analyzer, timing results are exploratory only.

## 4. Assembly tests, in build order

| Assembly | Joints | Immediate checks | Stress / repeat check |
|---|---|---|---|
| **One axle, then the other** | J01, J02, J03, J04 | Bearing fit and drag; stub endplay; shaft alignment before and after tightening the floating motor; wheel runout; full-turn clearance | Service load 31 N radial + 8 N lateral: axle deflection ≤0.25 mm, clearance ≥1.5 mm. 2× proof (62 N, 16 N, 0.8 N·m): no crack or insert movement, residual set ≤0.10 mm. Powered: runout ≤0.30 mm TIR, endplay ≤0.10 mm, no-load current change ≤ max(0.05 A, 10 %), 200 low-speed reversals. Then inspect for set-screw shift, insert movement, cracks and changed drag. |
| **Wheel and tyre** | J14 | Left/right handedness; loaded radius; diameter match between sides; clamp seating; runout | Loaded rolling, hard turns, short controlled torque events. Mark the tyre against the rim to reveal creep. Recheck clamp screws and dimensions after running. |
| **Rails, carriers, decks, crossmembers** | J04, J05, J06, J16 | Keys seat without force; coplanarity; wheel-axis alignment; screw engagement; tool access | Load and twist the frame with representative body ballast. Measure deflection **under load** and residual set afterwards. Repeat after a warm dwell to expose print creep. |
| **Caster pod and nose** | J07A/B, J08A/B/C | Caster rolls freely; pod and lid come off with the intended tools; cap travels 3 mm and returns from partial presses | Representative front-support loads, threshold crossings, repeated cap presses and removals. Check snap fingers, spring seating, insert retention, and whether the caster or the housing strikes first. |
| **Rear keel** | J09A/B, J10A/B | Shoe and bezel retention; TCRT shim fit; protected lead route; removal sequence | Scrape and threshold passes, controlled rear skid contact, abrasion, repeated shoe replacement. Confirm the sensor and lead stay protected and serviceable. |
| **Body mount, ballast, hatch** | J11A/B, J12, J13 | Pin fit, foot contact, bolt and nut access, ballast bar seating, pack removal path | Shake and load with representative body/head mass. Check for loosening, print crushing, hatch retention and pack restraint. |

## 5. Rolling chassis, in this order

Each stage has its own scope, power source, the claim a pass allows, and an exit condition. A pass at one stage supports **only** that stage's claim.

| Stage | Scope | Power | Claim a pass allows | Exit condition |
|---|---|---|---|---|
| A | Unpowered rolling | None | Free rolling, clearances, no rub or snag | Every surface pushed; post-tightening clearances recorded |
| B1 | One motor, restrained | Korad, current-limited | Per-motor current, encoder, driver limit, stall/reversal/brake behaviour, driver temperature | Both sides characterised separately |
| B2 | Both motors, restrained, low load | Korad, combined limit below 5 A | Direction, encoder agreement, enable/disable, E-stop, low-speed turns | Low-load dual checks done with no supply current limit reached |
| C | Guarded floor runs | Korad on a retained tether, within the B1/B2 envelope | Rolling-chassis handling within the tested speed band | Floor matrix done at the envelope set in B |
| D1 | Sensor characterisation | Korad | Sensor signal and margin only; **no safety claim** | Nose, TCRT and A21 bench checks recorded |
| D2 | End-to-end obstacle stop | Korad, floor | Stop-only obstacle behaviour on the tested obstacles and speeds | G03-style matrix done ([§ 5 Stage D2](#stage-d2--end-to-end-obstacle-stop)) |
| D3 | Fault injection | Korad; bench, then floor | Safe-state response to the injected faults | Every fault row repeated in the required states |
| E | Tabletop edge | Korad inside a verified catch | **Exploratory only** with the current single cliff channel | See [Stage E](#stage-e--tabletop-edge-separate-prerequisites) |
| P | Composite load and regeneration | Qualified 2S pack ([§ 8](#8-battery-entry)) | Both-motor stall/launch, regenerative braking, drive current share | After pack qualification |

### Stage A — unpowered

Push the chassis across each surface. Check straight rolling, caster swivel, wheel rub, cable drag, snagging at the threshold and unexpected contact from the rear shoe. After the frame is fully tightened, re-measure wheel clearance and axle alignment.

### Stage B — restrained, on the bench supply

The Korad is limited to 5 A. Two motors stalling together can reach or exceed that ([rig.md § 1](../../../02-prototypes/RP-03-locomotion/rig.md#1-bench-constraints-that-shape-the-rig)). Stage B is therefore split. Composite and regenerative claims wait for Stage P.

**B1 — one motor at a time.** Disconnect or disable the other motor.

1. Establish no-load current, encoder direction and counts, the driver current limit, fault response and default-disabled behaviour.
2. Run these as **separate** cases:
   - low-speed starts;
   - stall/launch at the driver limit;
   - reversals;
   - commanded braking;
   - power-cut coast.
3. Log rail voltage and temperatures during sustained running.
4. Characterise the paralleled bridges on each board. Adafruit rates #3297 at 1.2 A per channel with a default current limit. TI says the achievable current depends on the board's thermal behaviour. Measure temperature and stall/launch/brake behaviour. Measure **current sharing only with the per-bridge measurement in F4**; otherwise record sharing as **unverified**. Treat 2 A as the nominal combined limit setting, not a continuous rating ([BOM](BOM.md), [Adafruit #3297](https://www.adafruit.com/product/3297), [TI DRV8833](https://www.ti.com/product/DRV8833)).
5. Driver-rail spikes and brownout are millisecond events. Claim them only from the F4 scope, or at the INA resolution stated in the run record. Anything finer is exploratory.

**B2 — both motors, low load only.** Set the Korad limit so the combined draw stays below 5 A with margin, using B1's measured per-motor currents. Permitted:

- direction and encoder agreement;
- enable/disable and E-stop;
- low-speed straight running and turns;
- gentle stops.

Not permitted on the supply: simultaneous stall, hard launches, fast reversals and regenerative braking with both motors. Those are Stage P.

### Stage C — guarded floor runs

Power comes from the Korad on a retained tether, within the speed and acceleration envelope set in B1/B2. Record the tether's drag. Use the measured ballast corners and increase speed gradually. Measure:

- minimum controllable speed and straight-line drift;
- turn behaviour;
- stopping distance (commanded brake) and cutoff-coast distance, as separate metrics;
- reverse settle;
- caster-lift onset, compared with a_tip = g·x/h from *this* ballast's measured x and h;
- rear skid contact, tyre slip and temperatures.

Repeat on every surface and on the 2° slope. The RP-03 G01/G02 candidates give the matrix and repetition counts (≥3 per surface × ballast corner). The selected motor runs a **reduced drive envelope**: estimated 0.47 m/s at the launch load ([D-003](../../decisions.md#d-003)). Do not treat the old 0.70 m/s design point as a measured capability. Set the speed bands from Stage B measurements. Hard stops and launches that approach the supply limit move to Stage P.

### Stage D1 — sensor characterisation

A pass here establishes signal and margin only. **It supports no obstacle, cliff or contact safety claim.**

- **Nose Hall:** log the output against nose displacement (dial indicator, 0–3 mm) and push force. Proposed pass: trip within 0.4–1.2 mm, release below trip. Also test:
  - partial presses;
  - pressed at boot;
  - missing and reversed magnet;
  - disconnected and shorted signal;
  - supply and ADC variation.

  See [nose-hall-board](research/nose-hall-board.md).
- **Rear TCRT:** sweep 8/10/12 mm heights (4/2/0 shims) over real dark and light floors and over a simulated edge. Proposed pass: the darkest floor gives ≥3× the cliff signal once R2 is set. Then:
  - repeat with the motors running;
  - check ambient light (phone torch and daylight: V_off stays above 2.5 V or the fault trips);
  - unplug J10-10 and confirm the stop.

  See [rear-tcrt-lead](research/rear-tcrt-lead.md).
- **Front range (A21):** blind zone below 100 mm, range on each surface, and sample timing on the logic analyzer.

### Stage D2 — end-to-end obstacle stop

This is the test that supports an obstacle claim. It measures the whole path: detection → controller → driver → deceleration → stopped clearance. It follows the [RP03-G03 candidate](../../../02-prototypes/RP-03-locomotion/gates.md#rp03-g03-obstacle-safety). Behaviour is **stop-only**; a swerve that clears the obstacle is not a pass.

| Field | Content |
|---|---|
| Obstacles | Person-leg proxy (a prop), furniture leg, cardboard box, cable/flat obstacle. The 20 × 20 × 20 mm floor-level block in the caster shadow is a **coverage probe**: record the result, and do not pass it by bumping into it. |
| Approach speeds | From the Stage C envelope. The G03 speeds (0.40 / 0.45 / 0.50 m/s) apply only if the measured envelope reaches them. |
| Surfaces | At least two floor surfaces |
| Repetitions | ≥5 per obstacle × approach speed |
| Metrics | Detection-to-deceleration latency (logic analyzer on hazard GPIO and driver enable); stopping clearance to the obstacle face (tape ±2 mm / laser ±1 mm, less uncertainty); heading held; harmful contacts; false stops on a clear course |
| Candidate limits | Latency ≤50 ms (exploratory without the analyzer path); clearance ≥50 mm; **0** harmful contacts; set the false-stop ceiling before the runs |

With the A21's 38.3 ± 9.6 ms cycle, a 50 ms latency is not expected to pass as designed ([§ 9](#9-holds-on-whole-robot-release)). Run D2 to measure the real margin. Do not claim obstacle safety until it passes.

### Stage D3 — fault injection

Inject sensor, controller and heartbeat faults **on the bench first**, then on the guarded floor. Candidate limits come from RP03-G05:

- local detection to brake ≤50 ms (analyzer path required, otherwise exploratory);
- heartbeat loss ≤200 ms;
- no stale command executed;
- a fresh arm required after recovery.

Run ≥5 repetitions per fault in ≥2 states. Tabletop fault rows belong to Stage E.

### Stage E — tabletop edge (separate prerequisites)

Tabletop trials are **not** a prerequisite for mechanical endurance (§ 7). They have their own entry conditions:

1. an overhead catch verified in this session; no uncaught trial, pilot or scored ([rig.md § 1](../../../02-prototypes/RP-03-locomotion/rig.md#1-bench-constraints-that-shape-the-rig));
2. command inhibit by default: un-armed and ordinary motion commands rejected and logged ([RP03-G04](../../../02-prototypes/RP-03-locomotion/gates.md#rp03-g04-tabletop-safety));
3. cliff sensing coverage decided ([§ 9](#9-holds-on-whole-robot-release)).

**With the current single rear cliff channel, every tabletop trial is exploratory.** Record it as such, and make no tabletop-safety claim from it.

### Stage P — composite load and regeneration

Stage P runs only on a qualified pack ([§ 8](#8-battery-entry)) or another qualified power setup able to absorb regeneration. It covers the cases excluded from B2 and C:

- both-motor stall and hard launch;
- fast reversals;
- regenerative braking and energy returned to the source;
- drive current share at full load.

## 6. Stress test catalogue

Every assembly test above belongs to one of these types. Use this table to choose the method, the article and what to record.

| Type | What it exposes | Method | Article | Record |
|---|---|---|---|---|
| **Static proof** | Yield, insert pull-out, permanent set | Hold at 2× service load (e.g. 62 N radial / 16 N lateral / 0.8 N·m on the axle) | Article for use | Deflection under load, residual set, cracks |
| **Test to failure** | Real margin, failure mode | Ramp the load until failure | Coupon or sacrificial only | Peak load, failure location, print orientation |
| **Cyclic / fatigue** | Loosening, fretting, snap-finger fatigue | 200 powered reversals; start/stop cycles; ≥ a defined count of cap presses; caster travel cycles | Article for use | Before/after runout, endplay, drag, witness marks |
| **Creep / thermal dwell** | Relaxation of printed parts under clamp or load | Hold the service load during a warm run or a heated dwell, then re-measure | Frame, axle, tyre clamp | Residual set, loss of screw preload, tyre creep marks |
| **Impact / shock** | Brittle cracks, pod and keel strength | Threshold crossings at speed, controlled skid strikes, front bumps within the rated envelope | Pod, keel, crossmembers | Strike order (caster or housing first), cracks, insert movement |
| **Shake / vibration** | Loosening, lead chafe, board retention | Shake with representative body/head mass; long runs over rough and rug surfaces | Body mount, hatch, J15B boards and cables | Screw witness marks, lead position, connector seating |
| **Abrasion / wear** | Wear life of the shoe and tyre | Scrape passes; pivots on high-grip floors | Wear shoe, TPU tyre | Mass and thickness loss per N passes |
| **Service cycling** | Strip-out, damage from handling | Remove and refit the wheel, shoe, TCRT, nose cap, lid and hatch | All service joints | Cycles to strip or damage, tool access |
| **Electrical / thermal** | Driver sharing, heating, supply sag, braking energy | Sustained runs, stall/launch, reversal and brake transients on the drive bench | Drivers, motors, supply rail | Current per motor; per-bridge current (else sharing is unverified); temperatures; minimum rail voltage; spikes only from a scope or at the stated INA resolution. Both-motor composite and regeneration cases only in Stage P. |
| **Environmental / optical** | Sensor false positives and negatives | Dark, light and glossy floors; ambient light; motor noise; different heights | Hall, TCRT, A21 | Signal margin, false-trip count |
| **Fault injection** | Safe-state behaviour | Unplug, short, freeze or corrupt a signal; kill the heartbeat; hold pressed at boot | Controller + sensors | Time to brake (analyzer), stale-command count, recovery path |

## 7. Endurance campaign

Mechanical endurance starts after Stages A–C pass, with the D1 checks relevant to the parts under test. It does **not** wait for Stage D2, D3 or E. Endurance blocks that need hard launches or both-motor reversals near the supply limit wait for Stage P. Repeat the stresses that could slowly change a printed or screwed assembly:

- drive and reversal cycles;
- stop/start cycles;
- pivots on high-grip flooring;
- threshold passes;
- a sustained warm run;
- cap presses and caster travel;
- service removal and refit of the wheel, shoe, sensor and hatch.

**Measure before and after each block:**

- runout and endplay;
- wheel clearance and frame alignment;
- screw witness marks and insert position;
- tyre/rim creep marks;
- no-load and running motor current.

Any change beyond the pre-set limit is a finding, even if the chassis still drives.

## 8. Battery entry

Run chassis commissioning on the bench supply with **inert battery ballast**. The protected 2S pack enters only after its own checks are defined and passed:

- assembly and cell spacing (>1 mm, [D-026](../../decisions.md#d-026));
- insulation and restraint;
- fuse and disconnect;
- protection-module thresholds;
- charging;
- thermal behaviour.

Follow the dated written procedure required by [workbench § Battery](../../../01-system/workbench.md#battery-deferred-then-respected). Pack operation raises new questions that the bench supply does not answer:

- 8.4 V at full charge versus a 6 V motor;
- braking energy returning to the pack;
- how the protection module reacts to regeneration.

## 9. Holds on whole-robot release

**Passes are scope-specific.** A coupon, joint, axle or rolling-chassis test passes on its own when it meets its pre-set limit on a recorded configuration. For example, the 100 N bearing hold can pass today. The holds below block **whole-robot, autonomous and tabletop release**, not component passes. Each pass states which holds it does not address.

| Hold | Blocks | Does not block |
|---|---|---|
| 1. Hatch/pack restraint and frame hardware | Final fabrication, battery operation | Coupons, axle rig, supply-powered rolling tests with inert ballast |
| 2. Print process | Releasing fits and per-part exports | Coupons to choose the process (record the process on every pass) |
| 3. Motor/driver envelope | Speed bands above the measured envelope | Stage B, which measures it |
| 4. Cliff coverage | Stage E scored trials, tabletop and autonomous release | Stages A–D, mechanical endurance |
| 5. A21 stop-path timing | Obstacle-safety claim (Stage D2 pass), autonomous release | Stage D1 characterisation; D2 runs as measurement |
| 6. Stale documents | Freezing numerical gates | Exploratory and pilot runs with the configuration recorded |

These are system-architecture decisions. A successful rolling test cannot validate them by default.

1. **Hatch and pack restraint** (J11A/B) and the remaining **frame hardware** (J05/J06/J16, J12, J13, J15B).
2. **Print process:** printer, material, orientation and settings for each part.
3. **Measured motor/driver envelope:** replaces the reduced-envelope estimate.
4. **Cliff sensing coverage:** the v1 CAD has **one** rear cliff channel. RP03-P07 asks for at least **three** look-down channels (front-support forward, reverse/skid, wheel-adjacent).
5. **Stop-path timing:** the A21's 38.3 ± 9.6 ms measurement cycle already exceeds the 50 ms budget at worst case once scan and control delay are added (see [BOM](BOM.md)). Autonomous stop-path release stays on hold.
6. **Stale documents:** some generated CAD summaries and research notes predate the 2026-09-30 BOM, notably the earlier nose parts and driver choices. Reconcile them and fix the **exact tested configuration and revision** before freezing numerical gates.

## 10. Recording results

- Use the [run-record convention](../../../01-system/run-record-convention.md) (`run.md` + `data/` + `derived/` + `media/`). Proposed location: `docs/03-build/01-chassis/v1/runs/<run-id>/`.
- Classify each run as `exploratory`, `pilot` or `scored`. Only runs against a registered gate are scored.
- Write measured values and pass/fail outcomes back to the [project BOM](../../BOM.csv) release-check columns and to the joint-register rows.

## 11. TODO

### Before parts arrive
- [ ] Choose the trial print process (printer, material, orientation) for coupons
- [ ] Write the pass limit for each joint with no proposed number yet (J03 spigot, J05/J06, J07–J10, J11–J16, tyre creep, thread-forming screws)
- [ ] Set cycle counts for the fatigue tests (cap presses, service cycles, threshold passes, endurance blocks)
- [ ] Update the RP-03 rig parts list to the v1 BOM (motor, drivers, caster, sensors)
- [ ] Decide the run-ID prefix for chassis v1 runs (the convention uses `RP<nn>`) and create `v1/runs/`
- [ ] Reconcile stale generated CAD summaries and research notes with the 2026-09-30 BOM
- [ ] Fix broken links in [BOM.md](BOM.md), which still points at `axle-stack.md` and `rear-tcrt-lead.md` in `v1/` rather than `research/`
- [ ] Build the dimensionally accurate inert battery pack

### Fixtures
- [ ] F1 coupon pull/fit fixture with a calibrated force gauge
- [ ] F2 side-specific axle rig with radial/lateral loading and a dial indicator
- [ ] F3 ballasted open chassis; ballast map with measured M, x, h
- [ ] F4 drive bench: current-limited supply, motor-only E-stop, INA current per motor, thermocouples, logic analyzer
- [ ] F4 per-bridge current measurement (shunt or clamp in each bridge leg), or accept sharing as unverified
- [ ] Decide scope vs stated-resolution INA for rail transients
- [ ] F5 floor course: tile, laminate, rug, threshold, 2° slope, marks, ≥60 fps overhead camera

### Receiving and coupons
- [ ] Receiving inspection of every purchased part (§ 1), recorded in BOM.csv
- [ ] Dimensional check of every print
- [ ] Bearing-seat coupon series; choose the fit
- [ ] 100 N inner-ring hold, left and right
- [ ] Insert pull-out coupons for each insert SKU
- [ ] J04 key/rail coupon, 3 assembly cycles
- [ ] Spigot, tyre-to-rim and thread-forming-screw coupons

### Assemblies
- [ ] Axle L: immediate checks → service load → 2× proof → 200 reversals
- [ ] Axle R: same sequence
- [ ] Wheel/tyre: handedness, radius match, runout, creep marks
- [ ] Frame: seating, coplanarity, loaded twist, warm-dwell residual set
- [ ] Caster pod and nose: loads, cap travel/return, removal cycles
- [ ] Rear keel: retention, shim fit, scrape/skid, shoe replacement
- [ ] Body mount, ballast and hatch: shake/load, loosening, pack removal

### Rolling chassis
- [ ] Stage A unpowered push tests on every surface
- [ ] Stage B1 single-motor commissioning, left and right; stall/reversal/brake; per-bridge sharing
- [ ] Stage B2 low-load dual-motor checks under a combined limit below 5 A
- [ ] Stage C guarded floor matrix within the B envelope, every surface × ballast corner, plus the 2° slope
- [ ] Stage D1 nose Hall bench item 19; TCRT bench item 20; A21 range and sample timing
- [ ] Stage D2 end-to-end obstacle stop matrix, including the 20 mm blind-region probe; set the false-stop ceiling first
- [ ] Stage D3 fault injection: bench → guarded floor
- [ ] Stage E tabletop trials inside a verified catch; exploratory while there is one cliff channel

### Endurance and battery
- [ ] Endurance blocks with before/after measurement sets
- [ ] Written battery procedure; pack assembly and qualification
- [ ] Stage P on a qualified pack: both-motor stall/launch, fast reversals, regenerative braking, 8.4 V control, protection interaction

### Decisions (see § 9)
- [ ] Hatch/pack restraint and frame hardware
- [ ] Print process frozen
- [ ] Motor/driver envelope measured and recorded
- [ ] Cliff coverage: one channel or three
- [ ] A21 stop-path timing resolved
