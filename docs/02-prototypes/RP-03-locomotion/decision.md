# RP-03 Decision

| Field | Value |
|---|---|
| Status | **Open — no gate outcome, no ADR closed, no purchase authorized.** Parts 1–5 remain complete at **design-definition** level under `RP03-P1-REG-01` … `RP03-P5-REG-01`. Brief-gap close 2026-09-18 issued `RP03-P1-REG-02` … `RP03-P4-REG-02`. Numeric thresholds, candidate freeze and every gate outcome remain open; no scored run executed |
| Created | 2026-09-17 |
| Revised | 2026-09-19 |
| Design question | What drive/support geometry, drivetrain class and local sensing arrangement lets a representative-mass Makad move expressively at low speed, reverse, turn, spin and stop stably on household floors — and what is the measured margin of that design against caster lift, stopping distance, minimum controllable speed, reversal quality and obstacle/edge coverage? |
| Gate question | Can a candidate wheeled base with representative total mass move expressively at low speed, reverse, turn, spin and stop stably while local obstacle/edge sensing and controller limits prevent harmful or uncontrolled motion in the approved floor and tabletop permissions? |
| Feeds | ADR-04, ADR-07 (close provisionally, later); ADR-06 *sizing*; ADR-03 (C3 half of RP02-G05); ADR-05 (measured base model for RP-04) |
| Rule | A miss on follow ≤ 0.5 m/s, the tabletop-stationary default, or caster-lift margin is an `iterate` on geometry/drivetrain/sensing or a `reject` of a candidate — never a threshold change. `Defer` is unavailable for Core outcomes. Failed and aborted runs stay cited here |
| Remaining-open index | Folder-wide list lives in [`../openitems.md`](../openitems.md). This file remains the RP-03 decision record |

## Inherited locked decisions

Nothing in RP-03 reopens these; RP-03 measures them.

| Decision | Locked input | Source |
|---|---|---|
| Drive topology | Two independently powered encoder wheels + **front ball transfer** + **mandatory** rear anti-tip skid; holonomic and self-balancing rejected. Swivel caster is the RP-03 comparison swap | dimensional baseline v1.12; SCOPE-09 v1.3; MEM-20260813-20; BD-08 |
| Geometry targets | Ø84 mm wheels, 170 mm track, axle-to-caster 105–115 mm (110 mm target) | dimensional baseline v1.10 |
| Base controller | **C3 = ESP32-S3-DevKitC-1-N8** (prototype board); N8R8 is not a silent substitute; later WROOM-1-N8 carrier only by controlled equivalence | `RP02-P3-REG-01/02`; CA-03 |
| Operating modes | `OM-01` Floor; `OM-02` Tabletop inhibited-by-default; `OM-03` motion inhibited. `SD-03` app selection is a command, not the interlock | RP-02 `state-register.md`; SD-03 |
| Follow ceiling | **≤ 0.50 m/s**; cannot be weakened | CON-19 |
| Tabletop default | Ordinary locomotion, come/follow and spin inhibited in `OM-02` | CON-09; `v1-scope.md` |
| Motor energy path | `PB-MOTOR` → `PB-DRIVE` → `PB-DRIVE-L/R`, separately observable; absent in off/boot/hard-stop/charging | `RP02-P2-REG-01` PA-13 |
| Bench PSU | Korad KA3005D 30 V / 5 A; current limit before first power-up | `workbench.md` |
| E-stop | Cuts the **motor bus**, not logic; verified each session | `workbench.md`; PA-13 |

## Inherited paper state — not locked

These are current inputs. They are not SKU freezes, purchases, or `W` mass.

| Input | Current value | Source |
|---|---|---|
| Layout 03 complete head | ~499–524 g `E` at M008 = 10/20/35 g; **`W` (M900) does not exist**. Point `a_tip` waits on it | RP-01 `fullproofmath.md`; payload-mass-capture |
| Head servo family | C01 XC330-M288-T is a comparison candidate; paper approval OPEN; **not a family freeze** | RP-01 `actuator-screen-01.md`; RP-02 decision |
| Pack / chemistry | 2S-class 6.0–8.4 V is an `E` planning case; chemistry, S-count and construction open | RP-02 ADR-06; `power-architecture.md` |
| Timebase | `timebase.md` strategy written; **not implemented or validated**. Scored G01–G06 need it; Phase A exploratory capture may proceed without it | `timebase.md`; RP-02 Phase A |
| Caster-lift planning value | `a_tip ≈ 1.98 m/s²` is a **placement target** at `x = +25 mm`, `h = 124 mm`, not a Layout 03 roll-up | dimensional baseline; `physics.md` §2 |

## Builder decisions BD-01…BD-08 — paper-confirmed 2026-09-18; BD-08 added 2026-09-19

Recorded 2026-09-17 as working assumptions so Part 5 could be written. **Paper-confirmed 2026-09-18** as the brief-gap close: the rows below are the dated builder position for G01–G06 *candidate* conditions. They are **not** a gate freeze, not a purchase, and not SC-TBD-07/08/09 registration. A revision **before** gate freeze is a row edit with a new date. A revision **after** freeze is a new gate version. **BD-08** (2026-09-19) is the **selected V1 front-support type** on the Concept A chassis. It is not ADR-04 gate closure, not a Concept B freeze, and not a purchase. `dimensional-baseline.md` v1.12 and SCOPE-09 v1.3 record the type.

| ID | Paper-confirmed position (2026-09-18) | Why it is not a freeze | Consequence for RP-03 |
|---|---|---|---|
| **BD-01** | **V1 tabletop is fully stationary for users.** `BM-13` is the user-facing case. `CC-12C` / `BM-11` remains an **owed caught-fixture calibration case** for G04, not a user-facing V1 behaviour | CON-09 permits either. Builder may still grant armed creep as a V1 service mode | G04 includes inhibit/reject **and** the armed-creep edge trial. Do not tell a user the droid walks on a table |
| **BD-02** | **V1 obstacle policy = stop-only** | Redirect doubles the G03 matrix; `EV-20` allows stop | G03 is stop-short, heading held, no slew-as-path. Redirect is out of V1 |
| **BD-03** | **Base IMU is runtime hardware**, installed from **Phase B**. RP-03 Phase A may log it as a **bench instrument on the stand** | Could have remained bench-only; that would leave pickup/tip/slip without a runtime owner | `LG-10`, pin map and G05 pickup rows assume the IMU is on the frame from Phase B |
| **BD-04** | Named demo-room surface set below. Working labels tile / wood / rug / threshold are **retired** | SC-TBD-07 still registers at G01 freeze. If the physical room differs, rename **before** freeze | G01/G03 use `S-TILE` / `S-LAM` / `S-RUG` / `S-THR`. Slope is a G01 *condition*, not a fifth floor |
| **BD-05** | **Four-corner ballast** plus **head-pose CoM extras**. Mass: 1.65 kg and 3.10 kg+head, both settable CoM extremes. Head-pose: `HP-PITCH-FWD`, `HP-PITCH-AFT`, `HP-YAW-L`, `HP-YAW-R` on top of `HP-NEUTRAL`. A mass dummy at 304 mm is **not** enough | Could wait on M900 and narrow; that would hide Layout 03 CoM *and* pose risk | Rig sets `M`, `x` and `h` independently, and can hold a Layout 03 pose (or a geometrically equivalent dummy). `HIGH_AFT` is forbidden, not a corner |
| **BD-06** | Cannot-exceed test limit = **0.70 m/s** (top of the max target band). Follow ceiling remains **0.50 m/s** | Dimensional baseline gives a range, not a limit | G02 clamp tests 0.70. Follow cannot be authored or weakened to 0.70 |
| **BD-07** | **Overhead tether primary** catch; raised lip **only if it sits below cliff FoV**. Lip-only is **rejected as default** because it can mask cliff sensing | Plan allowed either; lip-in-FoV would fake G04 | `rig.md` §7. Catch verified each tabletop session |
| **BD-08** | **Selected V1 front support is `D21` Ø1" ball transfer.** Recorded in `dimensional-baseline.md` v1.12 and SCOPE-09 v1.3. `D20` swivel caster remains the **required** comparison swap on the same mount. Concept B's in-WB motors, perimeter ring, and bump-only stop path are **not** taken | Not a gate freeze, not a purchase, not ADR-04 closure. Dent/jam/drag on `S-LAM`/`S-RUG` can still reject the ball and iterate to the caster swap | Rig and Set A score `D21`. Analog-IR stop-path and three look-downs stay. A miss is iterate/reject of `D21`, not a threshold change |

### BD-04 named surfaces (demo-room class, 2026-09-18)

These are the articles SC-TBD-07 will freeze against, unless the physical room forces a rename before G01 freeze. μ bands stay `E` in `physics.md`.

| ID | Article | What it is | Why it is in the set |
|---|---|---|---|
| `S-TILE` | 600 × 600 mm vitrified ceramic tile, grouted, dry | Living-area hard floor, grout pitch disturbance, moderate specular | Dominant household hard floor; analog-IR and cliff albedo corner when dirty |
| `S-LAM` | 8 mm laminate wood-look plank, click-lock, dry | Lower μ band, polish/dust, dent risk for `D21` | Second hard floor; `BM-07` heading-glitch and `D21` dent inspection |
| `S-RUG` | Thin woven cotton or jute area rug, pile height **< 8 mm**, laid on `S-TILE` | Soft, higher μ, caster/ball jam, stick-slip at creep | SC-TBD-07 rug class without shag that would be an obstacle |
| `S-THR` | Aluminum door-threshold strip, **6–8 mm rise over 30–40 mm run** | Geometric step, not a μ band | Threshold tolerance in SC-TBD-07; treated as a pitch disturbance / obstacle |

Allowed indoor **slope** (SC-TBD-07 grade, not a floor ID): **2.0° (3.5 %) continuous, dry**, as a G01 condition on `S-TILE` or `S-LAM` (a marked ramp board is admissible). `physics.md` §10 computes climb torque, downhill brake and tip-on-slope. Steeper household ramps are out of V1.

### BD-05 head-pose CoM extras

Layout 03 authored best-case poses (`RP-01` `storyboard.md`): pitch **−18°…+35°**, yaw **±50°**. Usable mechanism travel is wider (`−22°…+40°`, yaw `±55°`) and is **not** used as a CoM corner — do not ballast past the authored pose.

Pitch axis height `E` ≈ 200 mm from the floor (140 mm body + 60 mm neck allocation). Head CoM in the lumped model sits at `h ≈ 250–255 mm`, so the pitch lever is **≈ 50–55 mm**. Yaw rotates that same offset about vertical.

| Extra | Pose | First-order CoM move (`E`, NOM head 509 g, lever 52 mm) | What it does to `a_tip` |
|---|---|---|---|
| `HP-NEUTRAL` | yaw 0, pitch 0 | The §2 lumped head at `x = +5 mm`, `h = 252 mm` | Baseline of the §2 RANGE |
| `HP-PITCH-FWD` | pitch **+35°** (nose down) | `Δx ≈ +52 sin 35° = +30 mm` on the head lump; `Δh ≈ −52 (1 − cos 35°) = −8 mm`. Whole-robot NOM: `Δx_CoM ≈ +6.0 mm`, `Δh_CoM ≈ −1.6 mm` | **Helps** forward-launch `a_tip` (more +x, slightly lower h) |
| `HP-PITCH-AFT` | pitch **−18°** (look up) | `Δx ≈ −52 sin 18° = −16 mm` on the head; `Δh ≈ −52 (1 − cos 18°) = −3 mm`. NOM: `Δx_CoM ≈ −3.2 mm`, `Δh_CoM ≈ −0.5 mm` | **Hurts** forward-launch `a_tip`. Score `BM-07` here |
| `HP-YAW-L` / `HP-YAW-R` | yaw **±50°**, pitch 0 | Head `x` offset of +5 mm rotates: `Δx = 5 (cos 50° − 1) = −1.8 mm`, `Δy = 5 sin 50° = ±3.8 mm` on the head. NOM `Δx_CoM ≈ −0.4 mm`, lateral `Δy_CoM ≈ ±0.8 mm` | Almost negligible on `a_tip`. Lateral CoM is a spin/walk term, not a caster-lift term |

Numbers are `E` from the lumped model, not CAD CoMs and not M900. Detail in `physics.md` §2.8. The rig must be able to hold these poses, or an equivalent dummy with the same `(m, x, y, h)`.

A mass dummy at 304 mm with the head in one pose is **not** BD-05.

### BD-08 — ball transfer selected as V1 front support (2026-09-19)

Builder direction: the V1 front support **is** the Ø1" ball transfer. That is a **support-type selection**, recorded in the dimensional baseline and SCOPE-09. It is not a concept freeze, not a purchase, and not a G01 pass.

| Taken | Not taken |
|---|---|
| `D21` as the V1 front support on the interchangeable mount | Concept B as the working-lead *vehicle* |
| No-trail `BM-07` as the installed hypothesis | Inboard motors / axle coupling |
| Dent inspection after every `S-LAM` session; cup-clean as scheduled service | Perimeter cliff ring as the installed map |
| `D20` caster kept on the same mount as the **comparison** | Bumper-only obstacle stop; ToF as the sole inhibitor |

Paper still does not prove dent/drag/jam. ADR-04 still closes only after G01/G02/G06 plus measured lift. If `D21` fails those rows, iterate to the caster swap — do not silently keep a failed ball.

## Part registrations

Each record freezes **design-definition** only. None is a purchase. None is a gate pass. Date of all five: **2026-09-17**.

### RP03-P1-REG-01 — intent and storyboard

| | |
|---|---|
| Frozen at design-definition | `intent.md`: why RP-03 exists; the two questions; ADR split (04 geometry / 07 sensing); twelve `BM-00…12` character panels; inherited-inputs table; phase ladder; evidence rules. `storyboard.md` v0.1: authored kinematics, profile library (`LAUNCH`/`CRUISE`/`DECEL0`/`PIVOT`/`ARC`/`SPIN`/`WIGGLE`/`BRAKE`/`HOLD`), per-panel export, controlling cases |
| Remains open | Pass/fail thresholds; motor SKU; tabletop footprint radius; any gate outcome |
| Not | Purchase. Gate pass. Freeze of storyboard numbers as scored thresholds |

### RP03-P2-REG-01 — physics envelope

| | |
|---|---|
| Frozen at design-definition | `physics.md` v0.1: `a_tip` as a **RANGE** (~0.9–1.9 m/s² under Layout 03 lumps; **negative** at HIGH_AFT — forbidden); four loading cases; traction/scrub; drivetrain demand; Korad 5 A consequence; stopping table at `t = 50 ms`; coverage geometry (minimum three look-downs); **CON-TBD-14 proposal** (250 mm radius, not registered); `LG-04`/`LG-10` **`E` refresh request** (drive average 2–8 W; `LG-10` remains `U`). **Drive mass bound 200–600 g unchanged** |
| Remains open | A point `a_tip`; measured CoM; motor/sensor/caster SKU; CON-TBD-14 registration; ledger `W`; any gate pass |
| Not | Purchase. Treating 1.98 m/s² as a roll-up result. Editing the mass ledger bound |

### RP03-P3-REG-01 — concepts and screens

| | |
|---|---|
| Frozen at design-definition | Competing concepts written and compared against the `physics.md` envelope; drivetrain screen `D01…` and sensing screen `S01…` complete as **screens**. **Concept A is the working lead, not a freeze.** **D02 JGA25-370 6 V 176 RPM is a reference unit, not a freeze.** **S01 / S04 / S06 / S07 are leads, not a freeze** |
| Remains open | Concept freeze; motor freeze; sensor freeze; paper P01–P09 passage; purchase of any screened part |
| Not | Purchase. Winner-by-HAT-pins. Paper PASS |

### RP03-P4-REG-01 — base control and interface

| | |
|---|---|
| Frozen at design-definition | `BC-01…10`; C3 **pin map v0.1** (retains **≥ 2 spare** safe GPIO); `BASE_*` draft (`BASE_LIMITS_SET`, `BASE_ENABLE`, `BASE_GOAL`, `BASE_STATE`, `BASE_FAULT`, hazard telemetry) in the registered RP-02 envelope. **Unblocks RP-02 C3 items** marked as waiting on RP-03 |
| Remains open | **Byte layouts** and type numbers; numeric timeouts; firmware; `link-contract.md` v0.5 registration on the RP-02 side; physical tests |
| Not | Purchase. RP02-G05 pass. Carrier PCB |

### RP03-P1-REG-02 — storyboard operating cases (2026-09-18)

| | |
|---|---|
| Frozen at design-definition | `storyboard.md` v0.2: operating-case grammar on `BM-00…14`; `BM-03` permission chain; `BM-13` tabletop demonstration (not `BM-11`); `BM-14` physical-stop; head-rocking (pitch 0.0953 N·m and yaw 0.1099 N·m) on `BM-00/01`; `FS-01…11` freezeable never-list. `intent.md` character table extended |
| Remains open | Pass/fail thresholds; the 240 fps acted mock-up; motor SKU; tabletop footprint radius; any gate outcome |
| Not | Purchase. Gate pass. Freeze of `FS-*` as scored thresholds (they freeze with G01–G06) |

### RP03-P2-REG-02 — remaining physics (2026-09-18)

| | |
|---|---|
| Frozen at design-definition | `physics.md` v0.2: allowed indoor slope 2.0°; climb/downhill/tip-on-slope; repeated-phrase heat and stop-on-temperature obligation; wheel torque/speed at 6.0 V vs 8.4 V; caster flutter / starting force / 360° envelope as screen axes; support-triangle load share under spin and reverse; head-pose CoM extras; `LG-04`/`LG-10` change-log row in the programme ledger |
| Remains open | A point `a_tip`; measured CoM; motor/sensor/caster SKU; CON-TBD-14 registration; ledger `W`; any gate pass |
| Not | Purchase. Treating 2.0° as a measured floor. Editing the mass ledger bound |

### RP03-P3-REG-02 — complete drive sets (2026-09-18)

| | |
|---|---|
| Frozen at design-definition | Two complete drive sets in `drivetrain-screen-01.md` v0.2 (Set A = D02 6 V path; Set B = D03 6 V comparison), each motor+gearbox+encoder+wheel+driver+supply interface+mount. Paper P01–P09 scored against the *sets*. Gearbox backlash/efficiency/shaft load, wheel loaded-radius/runout/retention, caster trail/start/flutter/360°, driver brake/coast/regen as named rows. Matrix snapshot 2026-09-18 |
| Remains open | Concept freeze; motor freeze; sensor freeze; purchase of any screened part. Paper P-gates remain OPEN as registrations even where a set PASSes on paper |
| Not | Purchase. Winner. Paper PASS as a freeze |

### RP03-P4-REG-02 — TTL candidates, cutoff metric, CA-14 header (2026-09-18)

| | |
|---|---|
| Frozen at design-definition | Candidate `BASE_GOAL` `cmd_ttl`, heartbeat timeout and queue depth in `base-control-architecture.md` and `link-contract.md` v0.5 (**unregistered numbers**, Phase A still measures them). Cutoff-coast as a distinct G01/G05 candidate metric beside commanded `BRAKE`. C3 board-role header generated from pin map v0.1 (`RP-02-electrical/phase-a/c3_board_role.h`). RP-02 issued `RP02-P4-REG-02` for v0.5 *semantics* |
| Remains open | Byte layouts and type numbers; measured timeouts; carrier PCB; firmware; physical tests |
| Not | Purchase. RP02-G05 pass. Numeric TTL freeze |

### RP03-P5-REG-01 — rig and gate candidates

| | |
|---|---|
| Frozen at design-definition | `rig.md` **designed** (not built): bench constraints, chassis, motor domain, C3 + interposer, instruments with rate/check/uncertainty, BD-04 course, Phase C catch. `gates.md` **candidate** registrations P01–P09 and G01–G06 using the eight plan fields |
| Remains open | **Registered gates empty.** Builder freeze of any threshold. Rig fabrication. Any scored run |
| Not | Purchase. Gate pass. CON-TBD-14 registration. Fabrication release |

## Gate outcomes

| Gate | Outcome | Evidence (run IDs) | Notes |
|---|---|---|---|
| RP03-P01 Torque | **OPEN** | | Paper. Not frozen, not passed |
| RP03-P02 Speed | **OPEN** | | Paper |
| RP03-P03 Current / 5 A | **OPEN** | | Paper |
| RP03-P04 Encoder / creep | **OPEN** | | Paper |
| RP03-P05 Backdrivability | **OPEN** | | Paper |
| RP03-P06 Mass | **OPEN** | | Paper |
| RP03-P07 Coverage / latency | **OPEN** | | Paper |
| RP03-P08 Pin map spare GPIO | **OPEN** | | Paper |
| RP03-P09 Analog-IR 0.50 vs 0.70 HOLD | **OPEN** | | Paper |
| RP03-G01 Floor control | **OPEN** | | Measurement; BD-04 × BD-05; lift vs `a_tip` range |
| RP03-G02 Speed boundary | **OPEN** | | Regulation ≤ 0.50; clamp at 0.70; follow cap cannot be weakened |
| RP03-G03 Obstacle safety | **OPEN** | | Verification; stop-only; 50 ms exploratory unless GPIO path live |
| RP03-G04 Tabletop safety | **OPEN** | | Verification; inhibit + owed `CC-12C` creep; no uncaught trial |
| RP03-G05 Fault containment | **OPEN** | | Verification; bench → floor → tabletop last |
| RP03-G06 Expressive feasibility | **OPEN** | | Measurement + recorded judgement; base model for RP-04 |

## ADR closure ladder

This is the folder's purpose. Each row closes independently and says what it is waiting on.

| ADR | Closes when | Waiting on | Status |
|---|---|---|---|
| **ADR-04** wheeled-drive and passive-support geometry | G01, G02 and G06 plus **measured** stability (lift onset vs computed `a_tip` at BD-05 corners; skid inequality at the scored ballast) | Scored floor matrix; CoM `W` of the ballast articles; drivetrain freeze after P01–P06; **`D21` dent/jam/drag vs `D20` swap** | Open — envelope, Concept A chassis, **D21 selected** (BD-08 / baseline v1.12). Not a gate close |
| **ADR-07** obstacle and tabletop-edge sensing | G03, G04 and G05 plus **coverage** evidence (three look-downs, look-ahead at 0.50 m/s, dark/glossy, interposer campaign) | Sensing freeze after P07/P09; catch fixture; CON-TBD-14 registration at G04 freeze | Open — arrangement on paper, not proven |
| **ADR-06 sizing** | Drive `W` rows for `LG-04`/`LG-10` and the G02-invariant re-run obligation raised in the ledger | Phase B/C measured profiles; battery gate; both-motor transients | Open — `E` refresh requested; **expected to close after RP-03 `W`, not from this paper** |
| **ADR-03** C3 half | RP02-G05 with margin on the C3 wheel loop, encoder capture, hazard scan and watchdog feed | RP02-G05 freeze and evidence; pin map implemented; driver/sensor on the bench | Open — board identity locked; timing unmeasured |
| **ADR-05** | G06 measured base response model (onset latency, decel-through-zero, settle) handed to RP-04 | Scored G06 profiles, not adjectives | Open — no model yet |

## Candidate register

Candidates are recorded so selection happens from evidence. **None of these rows is a freeze. None is purchased. A reference unit on the bench is equipment until a freeze says otherwise.**

| Decision | Candidates | What is fixed for comparison | What decides it |
|---|---|---|---|
| Chassis / support concept | **Selected: Concept A chassis/sensing + `D21` ball.** Concept B remains the comparison vehicle (in-WB motors, ring, bump-only stop). `D20` caster is the required swap | Inherited topology; Ø84 / 170 mm / 105–115 mm; skid adjustable 60–80 × 8–16 mm; forward battery bay; HIGH_AFT forbidden; analog-IR in the stop path; baseline v1.12 | G01/G02/G06 + measured lift/scrub/`BM-07` **and** `D21` dent/jam/drag on `S-LAM`/`S-RUG`. Not ADR-04 gate close |
| Drive motor | **Set A / D02 JGA25-370 6 V 176 RPM — reference unit, not a freeze.** Set B / D03 remains the comparison. Other `D01…` rows remain admissible | Paper P01–P06 against the *set*; Ø84 4 mm D-hub; 160–200 RPM design window; 1.5–3 A class; 0.70 clamp mandatory at 8.4 V | P01–P06 then scored G01/G02/G06. **This row is not selected** |
| Motor driver | **DRV8874 class — lead, not a freeze.** Brushed H-bridge, per-channel current sense, hardware fault, fail-safe enable | `PB-DRIVE-L/R` separately observable; signed regen; fault/enable on test points | Phase A/B `W` plus G05 driver-fault rows |
| Sensing leads | **S01, S04, S06, S07 — leads, not a freeze.** Arrangement screened against coverage/latency (P07) and analog-IR 0.50 vs 0.70 HOLD (P09) | Minimum three look-downs; no stop-path on an expander; dark/glossy in G04 | G03/G04/G05. A driver board's cliff pins do not pick this row |
| Base IMU | Runtime from Phase B (BD-03 working assumption); Phase A may log as bench instrument | SPI+INT reserved on the pin map; rigid base mount; not in the head | G01 lift / G05 pickup. SKU open |
| Catch fixture | Overhead tether primary (BD-07 working assumption) | Must not sit in cliff FoV | G04 session check. Not a product part |

## Conclusion

*(per ADR: pass / iterate / reject; selected candidates; budget rows updated with measured value, uncertainty and margin; downstream assumptions changed; re-run obligations created)*

No paper gate passed. No physical gate passed. No purchase authorized. **V1 front support is `D21` (BD-08, baseline v1.12, SCOPE-09 v1.3).** Set A / Concept A chassis / D02 / DRV8874-class and S01/S04/S06/S07 remain leads. `D20` is the comparison swap, not waived. ADR-04 is not closed. Parts 1–5 are design-definition; the 2026-09-18 brief-gap close (`RP03-P1-REG-02` … `RP03-P4-REG-02`) filled operating cases, remaining physics, complete drive sets, TTL candidates, cutoff-coast, and the `CA-14` header. Phase A bench work on C3 may begin when the driver evaluation board and reference motor are on the bench; it is not a scored RP-03 run. CAD pass 1 and the 240 fps mock-up remain open.
