# RP-03 Gate Registrations

| Field | Value |
|---|---|
| Status | **Paper gates RP03-P01…P09 drafted 2026-09-17; scored against Set A/B in §4 on 2026-09-18; all OPEN — not frozen, not passed.** Physical candidate registrations RP03-G01…G06 complete as *candidates* (cutoff-coast and 2.0° slope named); **no numeric gate is registered in §3 and no scored run exists** |
| Authority | Gate definitions and registration fields: `../../01-system/risk-prototype-plan.md` v1.12 §RP-03; folder `plan.md` §7. This file holds the registered numeric versions **when they exist** |
| Sources for thresholds | `intent.md`; `storyboard.md` v0.2 (authored kinematics, not pass/fail); `physics.md` v0.2 ranges; `drivetrain-screen-01.md` v0.3 drive sets; `sensing-screen-01.md`; `base-control-architecture.md`; `fault-matrix.md`; `rig.md`; BD-01…BD-08 in `decision.md` |
| Rule | Registration uses the plan's eight fields — **Gate ID, Metric, Threshold, Rationale, Conditions, Repetitions, Instrument, Freeze record** (date + builder approval **before** scored data is inspected). A threshold change after results is a new gate version with a documented reason and a fresh test set, never an edit |
| Instrument rule | `workbench.md` item 6 and `rig.md` §5: if the bench cannot resolve the threshold, that metric is **exploratory-only**. 50 ms detection-to-deceleration is the standing example |

## 1. Paper-screen gates — draft 2026-09-17, all OPEN

These are candidate-screen definitions, not scored RP03-G01…G06 outcomes. They match the drivetrain screen (P01–P06) and the sensing/control screens (P07–P09). Paper comparisons already observed are exploratory findings, not retrospective registered passes. Missing evidence returns OPEN, never PASS. No purchase, fabrication release or physical gate pass is implied.

Common freeze record: builder freeze approval = **pending**. Author/date = this draft, 2026-09-17.

### RP03-P01 Torque margin

| Field | Content |
|---|---|
| Gate ID | RP03-P01 |
| Metric | Wheel-torque capability of the named drivetrain candidate versus `physics.md` §4.2 demand at BD-05 corners, including rolling resistance (`C_rr = 0.025` `E`) |
| Threshold | Nonnegative paper margin at low/min-viable (`1.65 kg`, `a = 0.80 m/s²` → `τ_wheel ≈ 0.036 N·m` `E`), mid/best-case (`2.40 kg`, `a = 1.00` → `≈ 0.063 N·m`), and high/sensitivity (`3.624 kg`, `a = 1.20` → `≈ 0.110 N·m`), after recorded D-curve and gearbox-efficiency (40–70 % `E`) uncertainty. `BM-01` hold `0.027 N·m` `E` from the 0.1099 N·m yaw reaction is a **static** requirement, not a substitute for launch |
| Rationale | A candidate that only clears hold will stall a launch; one sized only on launch may roll at `v*=0`. Do not screen against a single `a_tip ≈ 2.0 m/s²` |
| Conditions | Named candidate, named voltage, manufacturer curve provenance declared (RP-01 P02 analogue). `a_peak` screened against the `a_tip` **range**, not 1.98 m/s² |
| Repetitions | Once per candidate revision |
| Instrument | Manufacturer `D` curves + `physics.md` calculation. Uncertainty: D-data class plus E envelope; not `W` |
| Freeze record | Pending. **OPEN** — not frozen, not passed. D02 is a reference unit, not a P01 pass |

### RP03-P02 Speed at the design point

| Field | Content |
|---|---|
| Gate ID | RP03-P02 |
| Metric | Loaded wheel speed at the 0.70 m/s design point and at `BM-02` creep |
| Threshold | Output in the 160–200 RPM unloaded design window at 0.70 m/s (`physics.md` G14; 159.2 RPM kinematic). Creep 0.04 m/s → 9.1 RPM must be commanded and, on paper, reachable without a stall-then-jump. `300 °/s` is never a commanded storyboard rate |
| Rationale | `ω_peak` at 220 °/s is only 74 RPM and does **not** size no-load RPM. Creep and the 0.70 band do |
| Conditions | Named gearbox ratio and motor no-load window (15:1–90:1 class screen). Voltage declared |
| Repetitions | Once per candidate revision |
| Instrument | Nameplate `D` + kinematic conversion (`r = 0.042 m`). Uncertainty: unloaded vs loaded is `U` until Phase A stand work |
| Freeze record | Pending. **OPEN** |

### RP03-P03 Current class versus 5 A

| Field | Content |
|---|---|
| Gate ID | RP03-P03 |
| Metric | Per-motor stall/launch/reversal current and both-motor composite versus `PB-DRIVE*` observability and the Korad 5 A ceiling |
| Threshold | Per-motor class remains **1.5–3 A** `E`. Composite stall 3–6 A. Two motors at 2.5 A = 5.0 A at the KA3005D ceiling; at 3.0 A = 6.0 A **exceeds**. Signed regen 0.3–1.5 A class, opposite traction, separately observable on L and R |
| Rationale | Phase B stall/reversal is **per motor**; both-motor composites wait Phase C pack. A candidate that only fits the Korad as a pair-at-stall has not been screened |
| Conditions | Named driver class (current sense per channel, fault, fail-safe enable). 2S-class 6.0–8.4 V is RP-02's `E` planning case, not a pack freeze |
| Repetitions | Once per candidate/driver pair |
| Instrument | Manufacturer stall `D` at declared voltage. Uncertainty: stall `D` is often optimistic; bench `W` is Phase A/B |
| Freeze record | Pending. **OPEN**. No purchase |

### RP03-P04 Encoder versus creep

| Field | Content |
|---|---|
| Gate ID | RP03-P04 |
| Metric | Encoder resolution and sample path versus `BM-02` minimum controllable speed 0.04 m/s (~9.1 RPM) |
| Threshold | Paper path must resolve 0.04 m/s at the wheel-loop rate without relying on an unstated CPR. If CPR/`Δt` cannot distinguish creep from stall, the candidate HOLDs for G01 min-speed |
| Rationale | Creep that is a stall-then-jump fails the audience read. Encoder capture is C3-owned (PCNT) |
| Conditions | Named encoder type and CPR; C3 pin map v0.1 has the capture pins |
| Repetitions | Once per encoder option |
| Instrument | CPR `D` + `v = n · circ`. Uncertainty: quantization vs loop jitter is `E` until Phase A |
| Freeze record | Pending. **OPEN** |

### RP03-P05 Backdrivability and hold

| Field | Content |
|---|---|
| Gate ID | RP03-P05 |
| Metric | How `BM-00` (unpowered/inhibited rest) and `BM-01` (armed `v*=0` against 0.1099 N·m) are achieved: ratio, active hold, or brake |
| Threshold | Named option, with idle-energy and acoustic cost stated. High-ratio N20-class (~150:1) may hold unpowered and fights service push. JGA25-class ~20–50:1 is backdrivable — `BM-00` needs active hold or a brake; `BM-01` needs current at `v = 0`. A brake must still fit the 200–600 g drive row and `PA-13` fail-safe. Do not pick in this paper gate; do not leave the option unnamed |
| Rationale | Free coasting reads as slop (MEM-20260812-08). Gearbox ratio alone is not `BM-00` evidence |
| Conditions | Same candidate as P01–P04. `LP-04-OFF` vs armed hold distinguished |
| Repetitions | Once per candidate |
| Instrument | Class statement from `physics.md` §4.6 + manufacturer reduction `D`. Uncertainty: residual friction is `U` |
| Freeze record | Pending. **OPEN**. D02 as reference unit does not freeze the hold option |

### RP03-P06 Drive mass

| Field | Content |
|---|---|
| Gate ID | RP03-P06 |
| Metric | Candidate drivetrain mass (motors, gearboxes, wheels, encoder, mounts, driver share owned by drive) versus the ledger drive row |
| Threshold | Fits **200–600 g** `E`. Physics does **not** move this bound. A brake, if chosen later, still has to fit inside it |
| Rationale | The 250 g-head error was an `E` treated as a target. Do not "save" mass by deleting the skid or the forward battery bay |
| Conditions | Named BOM of the drive row; no silent omission of wheels or mounts |
| Repetitions | Once per candidate revision |
| Instrument | Manufacturer `D` masses + allowance `E`. Uncertainty: `D` vs installed `W` |
| Freeze record | Pending. **OPEN**. Drive mass bound unchanged |

### RP03-P07 Coverage and latency

| Field | Content |
|---|---|
| Gate ID | RP03-P07 |
| Metric | Obstacle/edge coverage geometry and stop-path latency versus `physics.md` §6–7 and CA-12 |
| Threshold | Look-ahead at the **leading contact** exceeds `d_stop` minus mounting offset (`d_stop` at 0.50 m/s = 179 mm, at 0.05 m/s ≈ 45–54 mm). Minimum **three look-down channels** (front-support-forward, reverse/skid, wheel-adjacent). Lateral/pivot coverage at 220 °/s is a ~120 mm-class hole if only body-axis forward sensing exists. Blind-region 20 mm cube in the front-support shadow is not closed by bump-only at follow speed. Latency **scored at `t = 50 ms`**, not the 35 ms optimistic sum |
| Rationale | ADR-07 is an arrangement, not a SKU. A driver HAT with cliff pins must not choose this geometry |
| Conditions | Named `S*` set against C3 I/O budget; no stop-path input behind a GPIO expander; dark/glossy called out as the cliff failure mode |
| Repetitions | Once per sensing arrangement revision |
| Instrument | `physics.md` tables + manufacturer FoV/range/latency `D`. Uncertainty: sample-age 20 ms `E`; digital-cliff 1–5 ms is **not** the bound |
| Freeze record | Pending. **OPEN**. S01/S04/S06/S07 are leads, not a pass |

### RP03-P08 C3 pin map, spare GPIO

| Field | Content |
|---|---|
| Gate ID | RP03-P08 |
| Metric | Pin map v0.1 against the DevKitC-1-N8 header and `compute-control-architecture.md` §3 |
| Threshold | **≥ 2 unassigned safe GPIO** after safety, watchdog, debug and RGB-LED reservations. Strapping GPIO0/3/45/46 excluded from safety outputs. No safety input behind a GPIO expander. N8R8 is not a silent substitute (octal PSRAM consumes GPIO35–37) |
| Rationale | The pin map is a hard pre-carrier gate. Failing it moves to a WROOM-1-N8 carrier or changes the interface through change control |
| Conditions | Map includes encoder, driver fault/enable, IMU SPI+INT, cliff/obstacle/bump, link, watchdog feed, status-light cue |
| Repetitions | Once per map revision |
| Instrument | Header audit vs the I/O budget table. Uncertainty: none if the count is a physical pin count |
| Freeze record | Pending. **OPEN**. Map v0.1 is a design-definition artefact, not a G05 pass |

### RP03-P09 Analog-IR look-ahead at 0.50 m/s versus 0.70 HOLD

| Field | Content |
|---|---|
| Gate ID | RP03-P09 |
| Metric | Analog-IR (or equivalent stop-path rangefinder) look-ahead at the **follow ceiling** versus the 0.70 m/s design-point distance |
| Threshold | At **0.50 m/s** on the level, look-ahead at front-support contact must exceed **179 mm** (`physics.md` §6.2: `t = 50 ms`, `a_brake = 1.20 m/s²`, `d_margin = 50 mm`). An axle-mounted sensor is charged the extra 110 mm (289 mm). **2.0° downhill at 0.50 m/s** raises `d_stop` to **221 mm** (`physics.md` §10.2) — a coverage corner, HOLD until ball-mount geometry is proved. **0.70 m/s** (`d_stop = 289 mm` from front contact, 399 mm from axle) is **HOLD** for analog-IR coverage: analog-IR is not required to close 0.70 as a commanded V1 case. G02 cannot-exceed still tests the 0.70 clamp; follow **cannot** be weakened to 0.70 to make analog-IR look sufficient |
| Rationale | Follow ≤ 0.50 is inherited (CON-19). Treating 0.70 as a commanded coverage requirement would quietly enlarge V1 speed |
| Conditions | Named stop-path sensor class; ToF-as-telemetry is a different architecture and does not satisfy this row by existing on the same board |
| Repetitions | Once per sensing lead |
| Instrument | Range `D` at the relevant albedo/ambient + mounting geometry `E`. Uncertainty: dark/glossy and sunlit tile are the failure mode; manufacturer indoor range is not that test |
| Freeze record | Pending. **OPEN**. Not a sensor freeze, not a G03 pass |

## 2. Physical candidate registrations — not registered

Every number below is a **candidate** awaiting a dated builder approval. Registering one means copying its row into §3 with the freeze record filled in. Thresholds are **not frozen**. Storyboard minimum-viable numbers become binding only when copied here and approved before scored data is inspected.

Instrument uncertainty is restated per gate. A metric the bench cannot resolve is exploratory-only (`rig.md` §5).

### RP03-G01 Floor control

Plan mapping: `BM-02/03/04/05/08/09/12` across BD-04 surfaces × BD-05 corners; lift onset vs `a_tip` margin. Closes toward ADR-04.

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G01 |
| Metric | (1) Minimum controllable speed. (2) Stopping distance from each scored band, overshoot/rollback — **commanded `BRAKE`**. (3) **Cutoff-coast distance** from the same `v`, same surface, same ballast (`BM-14`): a distinct metric, not a `BRAKE` fail. (4) Lift-onset body accel versus `a_tip = g·x/h` computed from **this** ballast's measured `(x, h)`. (5) Reverse settle (`BM-08`) without caster-over tip. Also: `BM-03` permission chain, `BM-04` arc without hunting, `BM-05` in-place pivot, `BM-12` cancel-to-HOLD, `BM-13` tabletop-demo stillness (G04 also scores this). Straight-line drift millimetres and final chassis footprint polygon are logged |
| Threshold | **Candidates, not frozen.** Min speed ≤ **0.04 m/s** on every named BD-04 article (`S-TILE` / `S-LAM` / `S-RUG` / `S-THR`) at both BD-05 mass corners and the head-pose extras. Stopping, commanded: measured `d_BRAKE` ≤ physics table at that `v` **plus stated instrument uncertainty**, no rollback after `v=0`; 0.15 / 0.40 / 0.50 m/s scored, 0.60 exploratory, 0.70 not a commanded storyboard speed. Stopping, cutoff: `d_coast` **recorded**; finite; no restart on release (`FS-07`). Cutoff-coast is **not** required to be ≤ `d_BRAKE`. Lift: commanded scored `a_peak` stays below measured `a_lift` at that corner; **do not use 1.98 m/s² as the threshold**. Reverse: `BM-08` reaches HOLD without tip onto the caster. 2.0° slope is a G01 *condition* on `S-TILE` or `S-LAM` (`physics.md` §10). Margin is reported per surface × corner × head-pose, not as an adjective |
| Rationale | Floor locomotion is Core (SC-11). Caster lift is a ballast/placement fact. An `E` `a_tip` is not a target |
| Conditions | Open chassis on the **floor**; workbench scored-test gate; E-stop on the motor bus; ballast `(M, x, h)` recorded; HIGH_AFT forbidden; support geometry recorded; timebase implemented for scored (not exploratory) rows; per-motor Korad discipline. Head motion for `BM-01` may be a recorded torque substitute until RP-01 hardware exists — equivalence required. `BM-14` cutoff rows use the same course as `BM-09`. 2.0° ramp board is a condition, not a fifth floor |
| Repetitions | ≥ 3 per surface × BD-05 corner for min-speed, stop, and lift-onset; ≥ 3 `BM-08` and `BM-12` per corner on the controlling surface |
| Instrument | Encoders, tape/laser (`±2 mm` tape / `±1 mm` laser class), IMU/tilt for lift (`±0.5°` pitch class), top-down video, INA-class V/I. Uncertainty subtracted before a millimetre claim. Stand-motor or electronic load: **no G01 claim** |
| Freeze record | Pending. Not registered |

### RP03-G02 Speed boundary

Plan mapping: regulation error in the ≤ 0.50 m/s band; hard clamp at BD-06 under a deliberately excessive `BASE_GOAL`. Follow cap cannot be weakened.

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G02 |
| Metric | (1) **Regulation:** follow-band speed error at `BM-04` cruise. (2) **Cannot-exceed (verification):** measured `v` under an excessive `BASE_GOAL` |
| Threshold | **Candidates, not frozen.** Regulation: commanded **and** measured `v ≤ 0.50 m/s` in every sample of a follow run (binary inherited cap). Candidate p95 `|v_meas − v*| ≤ 0.05 m/s` at `BM-04` cruise — proposal only. Cannot-exceed: under `BASE_GOAL` requesting **> 0.70 m/s**, measured `v` **never exceeds 0.70 m/s** (BD-06 = top of the max target band). The 0.70 clamp is a test limit, **not** permission to follow at 0.70. Follow ceiling remains 0.50 and cannot be weakened |
| Rationale | CON-19. G02's verification half has no "almost" |
| Conditions | Floor; BD-04 surfaces at least tile and wood/laminate; both BD-05 mass corners; `F-14`-style flood on `BASE_GOAL` for the clamp half; firmware identity recorded |
| Repetitions | ≥ 3 follow cruises per surface × corner; ≥ 5 excessive-goal clamp trials |
| Instrument | Encoders on the common timebase; video corroboration. Speed uncertainty: encoder ±1 count plus timebase; state the m/s equivalent at the named CPR before scoring. If encoder creep-resolution fails P04, regulation at 0.04 m/s is exploratory |
| Freeze record | Pending. Not registered |

### RP03-G03 Obstacle safety

Plan mapping: `BM-10` per obstacle × approach speed; detection latency; stopping clearance; false-inhibit rate. **V1 stop-only (BD-02).** Redirect doubles this matrix and is not V1.

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G03 |
| Metric | Detection-to-deceleration latency; stopping clearance to the object face; heading hold (no slew as a path choice); false-inhibit rate on a clear course |
| Threshold | **Candidates, not frozen.** Latency ≤ **50 ms** (CA-12 invariant) — **exploratory-only unless the GPIO analyzer path in `rig.md` §5 is live**. 30 fps video cannot resolve this. Clearance: stop short by ≥ **50 mm** candidate (`physics.md` C07) minus instrument uncertainty; **0** harmful contacts in the registered set. False-inhibit: rate **recorded**; ceiling frozen at registration, not invented after a noisy run. V1 policy = **stop-only**; a swerve that clears the object is not a G03 pass |
| Rationale | SC-12 / SC-TBD-08; `EV-20` allows stop; BD-02 chooses stop. Bump-only at follow speed does not close the caster-shadow hole |
| Conditions | Floor; obstacles = person-leg proxy, furniture leg, cardboard box, cable/flat; approach from `BM-04` cruise at 0.40 / 0.45 m/s (and 0.50 cap). Person-leg proxy is a prop (RP-07 owns real people). Blind-region 20 mm cube is a coverage probe, not waived |
| Repetitions | ≥ 5 per obstacle × approach speed on at least two BD-04 surfaces |
| Instrument | Logic analyzer on hazard GPIO + driver-enable (latency); tape/laser (clearance, ±2 / ±1 mm class); video; `BASE_FAULT`/`BASE_STATE`. If 50 ms is unresolved, latency is exploratory; clearance may still be scored |
| Freeze record | Pending. Not registered |

### RP03-G04 Tabletop safety

Plan mapping: inhibit-by-default + rejected-request proof; `BM-11` edge trials inside the caught footprint. BD-01: `CC-12C` remains a **caught-fixture calibration case**, not a user-facing V1 behaviour; G04 **still includes the armed-creep trial because `CC-12C` is owed**. CON-09 permits either product policy. **No uncaught trial.**

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G04 |
| Metric | (1) `OM-02` inhibit-by-default: ordinary come/follow/spin **rejected**, logged, no motion — **`BM-13` is the user-facing still case**. (2) Un-armed `BASE_GOAL` rejected. (3) Armed `CC-12C` creep at 0.04–0.06 m/s stays inside the marked circle and `BRAKE`s well inside the mark on edge appearance (`BM-11`, owed, not the demo). (4) Zero uncaught departures |
| Threshold | **Candidates, not frozen.** **0** motions without a valid arm nonce. **0** come/follow/spin executions in `OM-02`. Armed creep: stop **≥ 40 mm inside the mark** candidate (`physics.md` C08) minus uncertainty. **0** falls. Footprint geometry is the CON-TBD-14 **proposal** (250 mm radius) until G04 freeze registers it. Dark and glossy samples included |
| Rationale | SC-13 / SC-TBD-09. V1 users see a stationary tabletop (BD-01); the owed calibration case still has to be true on the fixture or the sensing arrangement is unproven |
| Conditions | Catch fixture **verified this session** (BD-07: overhead tether primary; lip only if below FoV). Edge lanes at several angles (proposal 0/45/90/135/180°). Boot/reset/app-link loss returns to `OM-03`. A row without the catch is **invalid**, not a fail of the robot |
| Repetitions | Inhibit/reject: ≥ 5 per forbidden command class. Armed-creep edge: ≥ 3 per heading × dark/glossy. Pickup/unrested catch checks are session, not repetitions of the robot |
| Instrument | Mode/arm log; tape/laser to the mark; cliff channels; video; catch as a **safety device**, not a sensor. Latency to edge-stop: 50 ms instrument rule applies; else exploratory |
| Freeze record | Pending. Not registered. CON-TBD-14 not registered |

### RP03-G05 Fault containment

Plan mapping: `F-19`, `F-22`, `F-26`, `F-31…` campaign; time-to-brake; zero stale resumption; fresh-arm. Order: **bench, then floor, then tabletop last**.

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G05 |
| Metric | Time-to-brake from injection timestamp; obsolete-command count after recovery; fresh-arm requirement; health/fault exposure |
| Threshold | **Candidates, not frozen.** Local detection (`F-19` interposer mask/freeze/corrupt): time-to-brake ≤ **50 ms** — **exploratory-only without the GPIO path**. Heartbeat-mediated (C0/C3 loss, `F-22`): ≤ **200 ms** (SC-15 / RP-02 G04 analogue). **0** obsolete `BASE_GOAL`s executed. **0** motion after recovery without a fresh mode/arm/enable/action sequence. `F-26` window-watchdog violation inhibits without waiting for Linux. `F-12`/`F-13` scored under `CC-10A` when drive exists. Tabletop rows only inside the catch |
| Rationale | AD-04: safety survives high-level failure. Unknown sensor is inhibit |
| Conditions | Interposer injections without touching wiring. Campaign order **bench (stand) → guarded floor → caught tabletop last**. ≥ 2 registered states per row. Firmware identity recorded |
| Repetitions | ≥ 5 per row in ≥ 2 states (RP-02 G04 analogue) |
| Instrument | Injector timestamp, logic analyzer, `BASE_FAULT`, motor-arm/enable probes, encoder halt. Uncertainty: analyzer < 1 ms class if connected; else exploratory for 50 ms terms |
| Freeze record | Pending. Not registered |

### RP03-G06 Expressive feasibility

Plan mapping: `BM-05/06/07` onset/settle plus recorded builder judgement; at least one stable turn/spin/reversal profile. Hands RP-04 a **measured base model**, not an adjective.

| Field | Candidate content |
|---|---|
| Gate ID | RP03-G06 |
| Metric | Onset latency (command-to-motion); settle-to-HOLD after last command; heading/position overshoot; walk during spin; reversal deadband; **recorded builder judgement** that the phrase is readable enough to proceed to coordination testing |
| Threshold | **Candidates, not frozen.** Settle ≤ **350 ms** MV / ≤ **250 ms** best-case (storyboard hypotheses). `BM-06`: translation ≤ ~30 mm authored (a walk is a fail of spin). `BM-07`: a visible stop of ≤ 80 ms at zero is a **quality hypothesis**, not a gate, until copied into the freeze. At least **one** stable turn (`BM-05`), spin (`BM-06`) and reversal (`BM-07`) profile exported with measured onset, `a`/`α`, settle, and current. Judgement is recorded on the run record as `PROCEED` / `ITERATE` with a sentence; it cannot pass G06 alone |
| Rationale | ADR-05 input. RP-04 composes against numbers. Side-to-side is the highest-risk Core base performance |
| Conditions | Floor; both BD-05 mass corners; controlling surface plus one more; commanded `a_peak` re-checked against measured `a_lift` at that corner before scoring `BM-07`/`BM-08`-class accel. If lift onset sits below authored `a_peak`, the storyboard is revised or ballast restores `x` — the follow cap is not weakened |
| Repetitions | ≥ 5 per panel (`BM-05/06/07`) per corner on the controlling surface |
| Instrument | Encoders, IMU, video with timing cue, INA-class current, sound at the fixed position (`physics.md` §9). Time uncertainty: timebase; 30 fps video is not a 50 ms instrument and is weak for 80 ms deadband — use encoders |
| Freeze record | Pending. Not registered. No base model handed to RP-04 until scored |

## 3. Registered gates

*(none yet)*

## 4. Paper scores against complete drive sets — 2026-09-18, all OPEN

These are builder paper scores of P01–P09 against **Set A** and **Set B** in `drivetrain-screen-01.md` v0.2. They are **not** a freeze, **not** a purchase, and **not** a §3 registration. Missing evidence returns OPEN/HOLD, never PASS. A later freeze copies a row into §3 with a dated approval **before** scored data.

| Gate | Set A (D02 6 V + D10 4 mm + **D21** + dual DRV8874 + 2S direct) | Set B (D03 6 V 1:45 + same wheel/ball/driver/supply/mount) |
|---|---|---|
| P01 Torque | **PASS on paper** (Oz stall 0.490 and NFP 0.441 ≥ 0.220; rated ≥ 0.063). 6.0 V under sag still ≥ 0.220 on Oz | **PASS on paper** (Oz stall 0.589 ≥ 0.220; rated 0.108 ≥ 0.063) |
| P02 Speed | **PASS on paper** at 6 V 176 RPM. **HOLD** at 8.4 V (no-load 1.08 m/s) unless the 0.70 compiled clamp is on — the clamp is mandatory, not optional | **HOLD** — 133 RPM / 0.585 m/s at 6 V is below 160 and below 0.70, still above follow 0.50 |
| P03 Current / 5 A | **HOLD** — Oz 900 mA vs NFP ≤ 3 A at 6 V; NFP ≤ 4.2 A at 8.4 V. Do not average. Meter the article | **HOLD** — same stall-current `D` conflict |
| P04 Encoder / creep | **PASS on paper** (11 PPR × 35:1 ≈ 385 CPR, 0.69 mm/count, ~58 c/s at 0.04 m/s) | **PASS on paper** (11 PPR × 45:1 ≈ 495 CPR) |
| P05 Backdrivability | **Named, not picked** — 35:1 backdrivable; `BM-00` needs active hold or a brake; `BM-01` needs current at `v*=0` | Same class, slightly more residual friction `E` |
| P06 Mass | **PASS on paper** — two motors ~220 g + wheels/ball/skid/brackets/two DRV8874 → 350–500 g `E` inside 200–600 g | Same mount; 45:1 box is not a mass break |
| P07 Coverage / latency | **PASS on paper for the arrangement** (three look-downs + analog-IR + bump + IMU). Not a SKU pass. 2.0° downhill at 0.50 m/s makes `d_stop` 221 mm vs 179 mm level — coverage corner, not a P07 fail of the count | Same arrangement |
| P08 Pin map spare GPIO | **PASS on paper** — v0.1 retains three safe spares; header generated. Not a G05 pass | Same map |
| P09 Analog-IR 0.50 vs 0.70 | **PASS on paper at 0.50** if mounted at front-support contact (179 mm). **HOLD at 0.70** (289 mm) and **HOLD at 0.50 downhill 2°** (221 mm) until mounting geometry is proved | Same |

Set A is the **reference-unit lead**, not a freeze. Set B stays the comparison. Neither row is purchased.
