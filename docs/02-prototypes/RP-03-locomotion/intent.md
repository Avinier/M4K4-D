# RP-03 Intent — Drive and Local Motion-Safety Rig

| Field | Value |
|---|---|
| Status | Design/gate intent current; Parts 1–5 are complete at design-definition level under `RP03-P1-REG-01` through `RP03-P5-REG-01`. Numeric thresholds, candidate freeze, purchase and every gate outcome remain open; no scored run executed |
| Owner | Project builder |
| Created | 2026-09-17 |
| Revised | 2026-09-18 |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.12 §RP-03 (stage 3); folder plan `plan.md` |
| Mechanical baseline inherited | `../../01-system/dimensional-baseline.md` v1.12 (Ø84, 170 mm track, 110 mm wheelbase, **ball transfer** + mandatory skid); SCOPE-09 v1.3; MEM-20260825-01/02; BD-08 |
| Electrical baseline inherited | `RP02-P3-REG-01/02` (C3 = ESP32-S3-DevKitC-1-N8); `compute-control-architecture.md` CA-03/11/12; `power-architecture.md` PA-11/13; `link-contract.md` v0.4 envelope |
| Ledger | `../../01-system/power-energy-ledger.md` — RP-03 populates `LG-04`/`LG-10`; `../../01-system/mass-envelope-ledger.md` — RP-03 populates the drive row. No second copy lives here |
| Feeds | ADR-04 (wheeled-drive and passive-support geometry, provisional); ADR-07 (obstacle and tabletop-edge sensing arrangement, provisional); ADR-06 *sizing* (drive `W` rows); ADR-03 (C3 half of RP02-G05); ADR-05 (measured base response model for RP-04) |
| Method | `../../intuition.md` §5.1 — intent before numbers, numbers before physics, physics before concepts, concepts before rig, rig before decision. Toolkit: `d_available > v·t_latency + v²/(2·a_brake) + d_margin` |

## 1. Why RP-03 exists

RP-01 is an object. RP-02 is a set of states and interfaces. **RP-03 is a vehicle plus a safety authority.** It is the first prototype that can destroy itself (a desk edge), the first with real inductive and regenerative load on the motor bus, and the first with a sensor inside the stop path.

The body is not a wagon that happens to carry an expressive head. Five base performances are Core (MEM-20260813-08): curious approach, dramatic turn-toward-caller, excited spin, small side-to-side, startle. Side-to-side is the highest-risk of those five because it is a reversal. Zero-velocity hold is not optional: a body that rolls when the head yaws reads as slop (MEM-20260812-08). Follow cannot exceed 0.5 m/s. Tabletop is stationary by default. None of those sentences is a motor SKU.

RP-03 exists to close two architecture decisions of different kinds. Mixing them in one file is how a chassis quietly chooses the sensors, or a ToF module quietly fixes the wheelbase. Geometry and sensing stay in separate documents with separate registration records.

| ADR | What must be true to close it | Where RP-03 produces that |
|---|---|---|
| **ADR-04** wheeled-drive and passive-support geometry | A chassis envelope with named wheel/caster/skid positions, a drivetrain class, and measured margin against caster lift, stopping distance, minimum controllable speed and reversal quality | `physics.md`; `concepts/`; `drivetrain-screen-01.md`; `gates.md` G01, G02, G06; measured CoM/stability in Phase B |
| **ADR-07** obstacle and tabletop-edge sensing arrangement | A sensing arrangement with coverage geometry, a controller priority order, and a message set that `subsystem-interfaces.md` can inherit; zero uncaught tabletop departures; zero harmful obstacle contact in the registered set | `physics.md` coverage; `sensing-screen-01.md`; `base-control-architecture.md`; `fault-matrix.md`; `gates.md` G03, G04, G05 |
| **ADR-06 sizing** (informed, not closed) | Drive `W` rows for `LG-04`/`LG-10` and the G02-invariant re-run obligation | Ledger refresh now as `E`; `W` in Phase B/C |
| **ADR-03** (informed) | C3 half of RP02-G05: loop rate, jitter, encoder capture, watchdog feed | `base-control-architecture.md`; Phase A bench |
| **ADR-05** (informed) | Measured base response model — onset latency, decel-through-zero, settle — for RP-04 composition | G06; Phase B profiles |

The split between ADR-04 and ADR-07 is the most important line in this folder. It is what stops a motor-driver HAT from choosing the cliff sensors, and what stops an `E`-class `a_tip ≈ 2.0 m/s²` from becoming a target the way the 250 g head did.

## 2. The two questions

A can-question is falsifiable but teaches nothing about margin. A how-question is the deliverable but has no failure mode. RP-03 carries both, and keeps them separate.

### 2.1 Design question — the deliverable

> What drive/support geometry, drivetrain class and local sensing arrangement lets a representative-mass Makad move expressively at low speed, reverse, turn, spin and stop stably on household floors — and what is the measured margin of that design against caster lift, stopping distance, minimum controllable speed, reversal quality and obstacle/edge coverage?

The answer is a geometry (chassis envelope with caster/skid/wheel positions and the tested CoM range), a drivetrain class with a named candidate, a sensing arrangement with coverage geometry, and a base control definition with a pin map and message set. "Margin" is a number per gate per load/floor case, not an adjective.

### 2.2 Gate question — the falsifier

> Can a candidate wheeled base with representative total mass move expressively at low speed, reverse, turn, spin and stop stably while local obstacle/edge sensing and controller limits prevent harmful or uncontrolled motion in the approved floor and tabletop permissions?

Verbatim from the plan. `Reject` is reachable from it. The 0.5 m/s follow ceiling, the tabletop-stationary default and CON-TBD-14 cannot be weakened; a miss forces a geometry, drivetrain or sensing change, never a threshold change. `Defer` is unavailable: floor locomotion, come/follow, obstacle handling, tabletop protection and the excited spin are all Core.

### 2.3 Which gates are which

| Character | Gates | What closes them |
|---|---|---|
| **Measurement** — the number and its headroom are the deliverable | G01 floor control, G02 speed boundary (regulation half), G06 expressive feasibility | Registered metric, frozen threshold, recorded margin across the floor/load matrix |
| **Verification** — a property holds or it does not | G02 (cannot-exceed half), G03 obstacle safety, G04 tabletop safety, G05 fault containment | Every registered case meets its preregistered policy with zero harmful contact, zero uncaught departures, zero unbounded fault outcomes |

G06 is the only gate with a judgement component ("sufficiently smooth onset and settling to proceed to coordination testing"). It is scored against a preregistered profile-quality metric plus a recorded builder judgement, and it hands RP-04 a measured base response model, not an adjective.

## 3. Traceability

| Kind | IDs |
|---|---|
| Success criteria | SC-11 floor locomotion; SC-12 obstacle handling; SC-13 tabletop protection; SC-15 controlled stop and failure; SC-16 physical robustness; SC-25 expressive spin |
| Open thresholds | SC-TBD-07 floor surfaces/speed/slope/stopping/stability; SC-TBD-08 obstacle set/speeds/clearance; SC-TBD-09 tabletop surface/edge geometry |
| Constraints | CON-09 floor primary, tabletop stationary by default; CON-14 300×205×180 mm; CON-19 single-room envelope and follow ≤ 0.5 m/s; CON-P02 accessible cutoff; CON-P05 estimates before CAD freeze |
| Open constraint | CON-TBD-14 tabletop calibration footprint — proposed in `physics.md`, registered at G04 freeze, not here |
| Scope | SCOPE-09 v1.3 two encoder wheels + **front ball transfer** + mandatory rear skid; caster is the RP-03 comparison swap |
| Architecture drivers | AD-04 safety survives high-level failure; AD-08 peak loads occur concurrently |
| ADRs | ADR-04, ADR-07 (close provisionally); ADR-06 sizing, ADR-03, ADR-05 (informed) |
| Operating modes | `OM-01` Floor; `OM-02` Tabletop inhibited-by-default; `OM-03` motion inhibited. `SD-03` app selection is a command, not the interlock |
| Owed cases | `CC-09`, `CC-09C`, `CC-09R`, `CC-10A/B/C`, `CC-11`, `CC-12C`, `CC-13D`, drive share of `CC-PEAK-01`/`ST-01` |
| Owed faults | `F-19`, `F-22`, `F-26` cross-listed; `F-12`/`F-13` scored under `CC-10A` when drive exists; `F-31…` owned here |
| Owed loads | `LP-04-OFF/PWRRESTORE/STEADY/LAUNCH/REV/BRAKE/SPIN/BLOCKEDREF`; `LP-10-OFF/BOOT/IDLE/MOTION/OBSTACLE/EDGE/FAULT` |

## 4. Inputs inherited — do not re-derive

Everything below is inherited. RP-03 measures against these values. A departure is a baseline revision, not an RP-03 finding.

| Input | Value | Source |
|---|---|---|
| Drive topology | Two independently powered encoder wheels + **front ball transfer** + **mandatory** rear anti-tip skid; holonomic and self-balancing rejected. Swivel caster is the comparison swap | dimensional baseline v1.12; SCOPE-09 v1.3; MEM-20260813-20; MEM-20260825-01; BD-08 |
| Wheels | Ø84 mm nominal (Ø80–85 acceptable), ~21 mm tread, moderate-grip rubber/TPU | dimensional baseline §Drive targets |
| Track / wheelbase | ~170 mm centre-to-centre; drive axle to **front-support** contact 105–115 mm, 110 mm target | same |
| Front support / skid | **Ø1" ball transfer** (V1); Ø25–32 mm swivel caster is the RP-03 comparison swap; skid ~70 mm behind axle, ≤14 mm above floor, generalized as `h/d < x_CoM/h_CoM` | same; MEM-20260825-02; BD-08 |
| Whole-robot CoM *target* | `x_CoM = +25 mm` forward of axle, `h_CoM = 124 mm`. **Flagged for recalculation under the Layout 03 head.** The 2.0 m/s² figure is a placement target, not a mass-roll-up result — see `physics.md` | dimensional baseline v1.8/v1.10 |
| Caster-lift planning value | `a_tip = g·x_CoM/h_CoM ≈ 1.98 m/s²` *at the target CoM*; +10 mm forward ≈ +0.8 m/s². Commanded forward acceleration stays below the *recomputed range* with a registered margin until RP-03 measures lift onset | same |
| Speed bands | Normal 0.15–0.40 m/s; fast expressive 0.40–0.60 m/s; maximum target 0.65–0.70 m/s; **follow ≤ 0.5 m/s cannot be weakened**; ~160–200 RPM unloaded design point | dimensional baseline; CON-19 |
| Yaw rates | Normal/fast 120–220°/s; 300°/s+ is drivetrain-dependent headroom, not a commanded rate | dimensional baseline |
| Household envelope | Single room; come from 1–2 m stopping 0.6–0.9 m from the person; follow ≤ ~3 m route with one gentle turn; tabletop stationary by default | CON-09, CON-19; Scenario 2 |
| Tabletop permission | Ordinary locomotion, come/follow and spin inhibited in `OM-02`; only an explicitly armed, minimum-speed, caught-fixture calibration motion inside a marked validated circular footprint (`CC-12C`); footprint geometry is CON-TBD-14 | `v1-scope.md`; RP-02 `state-register.md` `OM-02` |
| Mode selection | V1 floor/table mode is selected manually in the control app; session-scoped; boot/reset/app-link loss returns to `OM-03` | RP-02 SD-03; `F-17` |
| Base controller | **C3 = ESP32-S3-DevKitC-1-N8** (prototype board); later WROOM-1-N8 carrier only by controlled equivalence; N8R8 is not a silent substitute | `RP02-P3-REG-01/02`; CA-03 |
| C3 I/O budget | 27–37 signals gross; 28 assignable header GPIO (27 with RGB LED); **pin map is a hard pre-carrier gate and must retain ≥ 2 unassigned safe GPIO**; no safety input behind a GPIO expander; strapping GPIO0/3/45/46 excluded from safety outputs | `compute-control-architecture.md` §3 |
| C3 rates and priority | 500 Hz wheel loop target, 200 Hz hazard scan target, 100 Hz state / 20 Hz heartbeat; ≤ 50 ms detection-to-deceleration invariant; `CA-11` priority order | CA-11, CA-12; MEM-20260812-01 |
| C3 ownership | Wheel velocity loops, encoder capture, base IMU, cliff/bump/proximity, local stop/reflexes, acceleration/velocity envelope, odometry capture, command expiry, readiness. Never person choice or path intent | CA-03 |
| Motor energy path | `PB-MOTOR` → `PB-DRIVE` → `PB-DRIVE-L/R`, **separately observable**; signed regenerative current required; absent in off/boot/hard-stop/charging | `RP02-P2-REG-01` PA-13 |
| Base safety supply | `PB-SAFE-BASE` independent of C2's converter; off in charging | PA-11 |
| Mass rows owed | Drive 200–600 g; battery 150–500 g low and forward; whole-robot analytical minimum ≈ 1.65 kg; other-subsystem high rows ≈ 3.10 kg before the head | mass-envelope-ledger v0.14 |
| Head reaction torque | RP-01 paper yaw peak 0.1099 N·m at 90.5°/s; Layout 03 complete head ~499–524 g `E` at the 304 mm stack | `fullproofmath.md`; payload-mass-capture |
| Base performances | Curious approach; dramatic turn-toward-caller; excited spin; small side-to-side; startle. Side-to-side is highest risk | MEM-20260813-08 |
| Zero-velocity hold | Drive must resist head reaction torque at zero commanded velocity; free coasting reads as slop | MEM-20260812-08 |
| Base IMU | Rigid base mount, SPI + interrupt preferred; promoted toward required; head mounting excluded | MEM-20260812-02; CA I/O budget |
| Bench rules | E-stop on every motion rig, cutting the motor bus, verified each session; Korad KA3005D **5 A ceiling**; logic analyzer never on the motor rail; fall from desk is the #1 hardware-loss risk | `workbench.md` |
| Run identity | `RP03-<scope>-<class>-<UTC>-<seq>` | `run-record-convention.md` |

## 5. Character intent — the twelve base-motion panels

Numbers live in `storyboard.md`. This section is the audience read only. Each panel names the primitive it exercises so physics and gates can point here without inventing a thirteenth behaviour.

| Panel | Character read | Primitive it exercises | Owed case |
|---|---|---|---|
| `BM-00` | Off / inhibited rest: nothing moves, nothing rolls when nudged, nothing rolls when the head yaws **or** pitches | Passive holding, backdrivability, head-rocking rejection | `LP-04-OFF`, `CC-02F/T` |
| `BM-01` | Zero-velocity hold while the head performs: the body does not twitch against a yaw snap or a laugh-class pitch | Reaction-torque rejection at v=0 (yaw **and** pitch) | MEM-20260812-08; `CC-05` with drive armed |
| `BM-02` | Creep: the slowest deliberate motion that still reads as intent, not as a stall | Minimum controllable speed, encoder resolution | `LP-04-STEADY` low end |
| `BM-03` | Curious approach as a permission chain: accept a fresh stationary mark → align → travel only while stopping clearance exists → brake into 0.6–0.9 m → settle with no second creep | Align/arc, clearance-gated cruise, arrival settle | `CC-09C`, `CC-10A` |
| `BM-04` | Follow: steady walk-pace tracking with one gentle arc, no hunting | Speed regulation ≤ 0.5 m/s, arc geometry, straight-line drift | `CC-09` |
| `BM-05` | Dramatic turn-toward-caller: one decisive pivot that lands on heading | In-place rotation, yaw-rate profile, settle | `EV-04` base analogue |
| `BM-06` | Excited spin: full rotations that end crisply, upright, on the spot | High yaw rate, skid/caster behaviour during spin, settle | `CC-11`, SC-25 |
| `BM-07` | Small side-to-side wiggle: quick reversals of a few centimetres, symmetric, no lurch | Reversal deadband, decel-through-zero | MEM-20260813-08 highest risk; `LP-04-REV` |
| `BM-08` | Startle retreat: sharp reverse then freeze | Reverse launch, caster loading in reverse, hard settle | `EV-07` after `EV-12`; `LP-04-REV` |
| `BM-09` | Controlled brake from each speed band: stops as if it meant to | Stopping distance/time, overshoot/rollback | `EV-12`, `LP-04-BRAKE` |
| `BM-10` | Obstacle intervention: stops short of the thing, visibly, without slewing | Detection-to-decel, stopping clearance, false-inhibit | `CC-10C`, `EV-20` |
| `BM-11` | Tabletop calibration creep and edge stop: moves only when armed, stops well inside the marked circle | Edge detection coverage, calibration speed, footprint | `CC-12C`, `EV-21` |
| `BM-12` | Controlled cancel from any of the above: settles, never coasts | Online jerk-limited brake from arbitrary state | `EV-17`; RP-01 `HM-18` analogue |
| `BM-13` | Tabletop demonstration: head and face remain active, base stays still, ordinary locomotion rejected | Unarmed `OM-02` hold while `HM-*` runs. **Not** `BM-11` | `CC-02T`; BD-01 user-facing tabletop |
| `BM-14` | Physical stop: motor-bus cutoff while moving; coast vs commanded `BRAKE` as two distances; release does not restart | Hardware cutoff; fresh arm required | `F-12`/`F-13`/`F-41`; CON-P02 |

Never-lists live in the freezeable register `FS-01…11` in `storyboard.md` §5 (coast after cancel, tabletop motion without arm, uncaught departure, follow hunt, walking spin, unrequested second creep, restart on release, ordinary locomotion in unarmed `OM-02`, hold/vibration rock, reversal lurch, come overshoot). Do not keep a second prose list here.

## 6. Scope

### 6.1 RP-03 owns

- the **character and kinematic storyboard** (`storyboard.md`) for `BM-00…BM-14`, the operating-case grammar, the `FS-*` register, and the wheel-velocity profile library;
- the **physics envelope** (`physics.md`): stability as a range, traction/scrub, drivetrain demand, electrical class, stopping inequality, coverage geometry, CON-TBD-14 *proposal*;
- **≥ 2 competing concepts** (`concepts/`) differing on a first-order axis, with a filled comparison of `physics.md` quantities;
- the **drivetrain screen** (`drivetrain-screen-01.md`) `D01…` and the **sensing screen** (`sensing-screen-01.md`) `S01…` — neither is a freeze or a purchase;
- the **base control architecture** (`base-control-architecture.md`) `BC-01…`, C3 pin map v0.1, and the base message-set *draft* in the registered RP-02 envelope;
- the **fault-injection rows** `F-31…` (`fault-matrix.md`), cross-listing `F-19/F-22/F-26`;
- the **ugly chassis rig** (`rig.md`) and **gate candidate registrations** (`gates.md`) `RP03-P01…` and `RP03-G01…G06`;
- **populating** `LG-04`/`LG-10` and the drive mass row; **extending** RP-02's link contract and `CA-14` config source;
- the **ADR closure ladder** in `decision.md`.

### 6.2 RP-03 does not

- select the battery chemistry or pack (ADR-06 architecture is RP-02's; sizing follows RP-03's `W` rows);
- implement person perception, target continuity or following *policy* (RP-07);
- compose head–base performances or judge observer coherence (RP-04);
- close SC-14 or any integrated-droid requirement;
- produce final chassis CAD — `cad/base/` is a blockout for a selected concept only, and root `cad/` stays reserved for integrated CAD;
- authorize any purchase; a reference motor bought for Phase A is bench equipment until a freeze says otherwise;
- weaken the 0.5 m/s follow ceiling, the tabletop-stationary default, or the caster-lift margin rule;
- carry a second copy of geometry targets, mass rows, power rows, `OM/BS/EV/CC/LP` vocabulary, the C0↔MCU framing, `PA-13`, `F-19/22/26`, sourcing rows, bench rules, run identity, or the timebase.

## 7. Phase ladder

Phase is a status field per document, not a directory.

| Phase | Needs | Can produce | Cannot produce |
|---|---|---|---|
| **A — paper and on-hand hardware** | Parts 1–5 written; C3 DevKitC-1-N8; a driver evaluation board; one reference motor; Korad; logic analyzer | Registered `BC-*`, pin map, message-set draft; ledger `E` ranges; RP02-G05 C3 loop/jitter exploratory capture; encoder/watchdog bench validation; every gate registration candidate | Any `W` row; any stability, stopping or edge claim; anything on a chassis |
| **B — open chassis on the floor** | Workbench scored-test gate satisfied for this rig; implemented timebase and logging; E-stop on the motor bus; two candidate motors + wheels + caster + skid on the ballasted frame; marked course and surface set; external top-down video with a timing cue | G01, G02, G06 scored across the floor/load matrix; G03 for the registered obstacle set; G05 floor rows; per-motor `W` profiles for `LP-04-*` and `LP-10-*` within the 5 A ceiling; measured lift onset, skid contact and CoM sensitivity | Both-motor stall/reversal composites above 5 A; tabletop rows; `CC-PEAK-01` closure |
| **C — caught tabletop and onboard energy** | Catch fixture built and verified; battery gate satisfied and a candidate pack (shared with RP-02 Phase C); sensing candidates installed | G04 edge trials inside the caught footprint; G05 tabletop rows; both-motor transients and `CC-10A/B` regenerative `W` rows; CON-TBD-14 registration input; ADR-06 sizing input | SC-14; any come/follow with a real person (RP-07); composed performances (RP-04) |

## 8. Relationship to siblings

Circular, and named.

| Sibling | What RP-03 needs from it | What it needs from RP-03 | What can proceed now |
|---|---|---|---|
| **RP-01** | Layout 03 head `E` tree (~499–524 g) and yaw reaction 0.1099 N·m; complete-head `W` (M900) is *not* required for paper | Stability range with the heavier head; a body that holds still during `HM-*` | Paper physics at BD-05 corners; point `a_tip` waits on M900 |
| **RP-02** | C3 identity, `CA-*`, envelope, `OM/CC/LP/F-19/22/26`, `PB-DRIVE*`, Korad/E-stop rules | Pin map v0.1, driver/sensor interface, `BASE_*` draft (`link-contract.md` v0.5), `CA-14` config source, drive `E` then `W` | Part 4 defines messages here; RP-02 registers v0.5 there; byte layouts wait on Phase A measurement |
| **RP-04** | Nothing yet | Measured base response model from G06 | Composition stays RP-04's |
| **RP-07** | Nothing yet | Obstacle/edge *policy* with props; not real-person come/follow | Person-leg proxy is a prop, not a person |

## 9. Evidence rules carried in from day one

1. **Evidence classes** are the ledgers': `W` measured in the recorded state with a run ID; `D` manufacturer; `E` calculation, analogy or characterized substitute; `U` unknown, never zero.
2. **A substitute needs an equivalence record.** An electronic load reproduces a current-time trace, not inductive kick or regeneration; a bare motor on a stand reproduces torque/current, not traction, scrub or lift. No stability, stopping or edge claim from either.
3. **Thresholds freeze before data.** SC-TBD-07/08/09 and CON-TBD-14 get gate-registration records with a dated builder approval before any scored run; a change after results is a new gate version with a fresh test set.
4. **Transient claims need a transient instrument.** Detection-to-decel at 50 ms and reversal current spikes are not INA-at-10-Hz measurements; the run is exploratory until the bench resolves the threshold.
5. **No uncaught tabletop trial, ever.** Pilot or scored, a tabletop row without a verified catch fixture is invalid and is recorded as such.
6. **IDs are append-only.** `BM-`, `FS-`, `D`, `S`, `BC-`, `F-3x`, `BD-`, `RP03-P/G` and `RP03-P<n>-REG-<nn>` are never reused or renumbered.
7. **Failed and aborted runs stay cited.** A candidate rejected on the floor is a result, not an embarrassment.
8. **An `E` value is not a target.** `a_tip ≈ 2.0 m/s²`, the 200–600 g drive mass row and the 1.5–3 A per-motor class are all recomputed as ranges in `physics.md` before any candidate is screened against them.
