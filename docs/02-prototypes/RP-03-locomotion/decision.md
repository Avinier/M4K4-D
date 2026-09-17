# RP-03 Decision

| Field | Value |
|---|---|
| Status | **Open — no gate outcome, no ADR closed, no purchase authorized.** Parts 1–5 are complete at **design-definition** level under `RP03-P1-REG-01` through `RP03-P5-REG-01`. Numeric thresholds, candidate freeze and every gate outcome remain open; no scored run executed |
| Created | 2026-09-17 |
| Revised | 2026-09-17 |
| Design question | What drive/support geometry, drivetrain class and local sensing arrangement lets a representative-mass Makad move expressively at low speed, reverse, turn, spin and stop stably on household floors — and what is the measured margin of that design against caster lift, stopping distance, minimum controllable speed, reversal quality and obstacle/edge coverage? |
| Gate question | Can a candidate wheeled base with representative total mass move expressively at low speed, reverse, turn, spin and stop stably while local obstacle/edge sensing and controller limits prevent harmful or uncontrolled motion in the approved floor and tabletop permissions? |
| Feeds | ADR-04, ADR-07 (close provisionally, later); ADR-06 *sizing*; ADR-03 (C3 half of RP02-G05); ADR-05 (measured base model for RP-04) |
| Rule | A miss on follow ≤ 0.5 m/s, the tabletop-stationary default, or caster-lift margin is an `iterate` on geometry/drivetrain/sensing or a `reject` of a candidate — never a threshold change. `Defer` is unavailable for Core outcomes. Failed and aborted runs stay cited here |
| Remaining-open index | Folder-wide list lives in [`../openitems.md`](../openitems.md). This file remains the RP-03 decision record |

## Inherited locked decisions

Nothing in RP-03 reopens these; RP-03 measures them.

| Decision | Locked input | Source |
|---|---|---|
| Drive topology | Two independently powered encoder wheels + front caster + **mandatory** rear anti-tip skid; holonomic and self-balancing rejected | dimensional baseline v1.10; SCOPE-09; MEM-20260813-20 |
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

## Builder decisions BD-01…BD-07 — working assumptions, 2026-09-17

Recorded so Part 5 (`rig.md`, `gates.md`) can be written. They are **working assumptions**, not locked product decisions. The builder may revise any row **before gate freeze**. A revision after freeze is a new gate version.

| ID | Working assumption (recommended) | Why it is not locked | Consequence for RP-03 |
|---|---|---|---|
| **BD-01** | **V1 tabletop is fully stationary for users.** `CC-12C` remains an **owed caught-fixture calibration case** for G04, not a user-facing V1 behaviour | CON-09 permits either. Builder may still grant armed creep as a V1 service mode | G04 includes inhibit/reject **and** the armed-creep edge trial. Do not tell a user the droid walks on a table |
| **BD-02** | **V1 obstacle policy = stop-only** | Redirect doubles the G03 matrix; `EV-20` allows stop | G03 is stop-short, heading held, no slew-as-path. Redirect is out of V1 |
| **BD-03** | **Base IMU is runtime hardware**, installed from **Phase B** (MEM-20260812-02; CA reserves SPI+INT). RP-03 Phase A may log it as a **bench instrument on the stand** | Could have remained bench-only; that would leave pickup/tip/slip without a runtime owner | `LG-10`, pin map and G05 pickup rows assume the IMU is on the frame from Phase B |
| **BD-04** | Surface set = **tile, wood/laminate, thin rug, threshold strip**, pending the builder naming the actual demo-room floors | SC-TBD-07 needs named surfaces; only the builder knows the room | G01/G03 use these as working labels until renamed. Not a freeze of SC-TBD-07 |
| **BD-05** | **Four-corner ballast**: 1.65 kg and 3.10 kg+head, **both CoM extremes**. Honest default | Could wait on M900 and narrow; that would hide Layout 03 CoM risk | Rig sets `M`, `x` and `h` independently. HIGH_AFT is forbidden, not a corner |
| **BD-06** | Cannot-exceed test limit = **0.70 m/s** (top of the max target band). Follow ceiling remains **0.50 m/s** | Dimensional baseline gives a range, not a limit | G02 clamp tests 0.70. Follow cannot be authored or weakened to 0.70 |
| **BD-07** | **Overhead tether primary** catch; raised lip **only if it sits below cliff FoV**. Lip-only is **rejected as default** because it can mask cliff sensing | Plan allowed either; lip-in-FoV would fake G04 | `rig.md` §7. Catch verified each tabletop session |

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
| **ADR-04** wheeled-drive and passive-support geometry | G01, G02 and G06 plus **measured** stability (lift onset vs computed `a_tip` at BD-05 corners; skid inequality at the scored ballast) | Scored floor matrix; CoM `W` of the ballast articles; drivetrain freeze after P01–P06 | Open — envelope and working Concept A lead only |
| **ADR-07** obstacle and tabletop-edge sensing | G03, G04 and G05 plus **coverage** evidence (three look-downs, look-ahead at 0.50 m/s, dark/glossy, interposer campaign) | Sensing freeze after P07/P09; catch fixture; CON-TBD-14 registration at G04 freeze | Open — arrangement on paper, not proven |
| **ADR-06 sizing** | Drive `W` rows for `LG-04`/`LG-10` and the G02-invariant re-run obligation raised in the ledger | Phase B/C measured profiles; battery gate; both-motor transients | Open — `E` refresh requested; **expected to close after RP-03 `W`, not from this paper** |
| **ADR-03** C3 half | RP02-G05 with margin on the C3 wheel loop, encoder capture, hazard scan and watchdog feed | RP02-G05 freeze and evidence; pin map implemented; driver/sensor on the bench | Open — board identity locked; timing unmeasured |
| **ADR-05** | G06 measured base response model (onset latency, decel-through-zero, settle) handed to RP-04 | Scored G06 profiles, not adjectives | Open — no model yet |

## Candidate register

Candidates are recorded so selection happens from evidence. **None of these rows is a freeze. None is purchased. A reference unit on the bench is equipment until a freeze says otherwise.**

| Decision | Candidates | What is fixed for comparison | What decides it |
|---|---|---|---|
| Chassis / support concept | **Concept A — working lead, not a freeze.** Concept B remains the comparison (front support and sensing arrangement differ on first-order axes in `physics.md` §10) | Inherited topology; Ø84 / 170 mm / 105–115 mm; skid adjustable 60–80 × 8–16 mm; forward battery bay; HIGH_AFT forbidden | G01/G02/G06 + measured lift/scrub/`BM-07` heading glitch. Interchangeable caster / ball transfer on the rig |
| Drive motor | **D02 JGA25-370 6 V 176 RPM — reference unit, not a freeze.** Other `D01…` rows remain admissible | Paper P01–P06; Ø84 wheel; 160–200 RPM design window; 1.5–3 A class | P01–P06 then scored G01/G02/G06. **This row is not selected** |
| Motor driver | **DRV8874 class — lead, not a freeze.** Brushed H-bridge, per-channel current sense, hardware fault, fail-safe enable | `PB-DRIVE-L/R` separately observable; signed regen; fault/enable on test points | Phase A/B `W` plus G05 driver-fault rows |
| Sensing leads | **S01, S04, S06, S07 — leads, not a freeze.** Arrangement screened against coverage/latency (P07) and analog-IR 0.50 vs 0.70 HOLD (P09) | Minimum three look-downs; no stop-path on an expander; dark/glossy in G04 | G03/G04/G05. A driver board's cliff pins do not pick this row |
| Base IMU | Runtime from Phase B (BD-03 working assumption); Phase A may log as bench instrument | SPI+INT reserved on the pin map; rigid base mount; not in the head | G01 lift / G05 pickup. SKU open |
| Catch fixture | Overhead tether primary (BD-07 working assumption) | Must not sit in cliff FoV | G04 session check. Not a product part |

## Conclusion

*(per ADR: pass / iterate / reject; selected candidates; budget rows updated with measured value, uncertainty and margin; downstream assumptions changed; re-run obligations created)*

No paper gate passed. No physical gate passed. No purchase authorized. Concept A, D02, DRV8874-class and S01/S04/S06/S07 remain leads and a reference unit. Parts 1–5 are design-definition only. Phase A bench work on C3 may begin when the driver evaluation board and reference motor are on the bench; it is not a scored RP-03 run.
