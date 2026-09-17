# RP-03 Base Motion Storyboard

| Field | Value |
|---|---|
| Status | Provisional authored kinematics v0.1 — design hypotheses, not registered gate thresholds |
| Owner | Project builder |
| Created | 2026-09-17 |
| Last updated | 2026-09-17 |
| Semantic source | `intent.md` |
| Inherited geometry | Track `b = 170 mm`, wheel Ø84 mm (`r = 42 mm`). Conversion constants for `v,ω →` wheel RPM; not a SKU |
| Feeds | `physics.md`, `gates.md`, firmware profile library |

## 1. How to read this storyboard

This document translates the accepted character vocabulary in `intent.md` into body-frame speeds, yaws, keyframes and timing that a drivetrain can be designed against. It deliberately starts each move with what the audience should read; numbers describe that performance rather than replace it.

The numbers are **authored targets** chosen from Makad's intended character, human walk-pace (follow ≤ 0.5 m/s is slower than a walk) and the dimensional-baseline speed/yaw bands. They are not yet pass/fail thresholds. They must be reviewed by the builder, exercised in simulation or an acted mock-up, checked against the Layout 03 `a_tip` RANGE in `physics.md`, and frozen in `gates.md` before scored RP-03 runs. The kinematic targets remain authored intent; traction, caster lift, scrub, current, thermal load and settling must be computed from the current mass/CoM evidence rather than inherited from a placement-target `a_tip`.

This file does not assign a pass threshold, name a motor, or set the tabletop footprint radius. Those belong to `physics.md` (proposal) and `gates.md` (freeze).

### Coordinate convention

All commands are robot-relative in the floor plane:

| Quantity | Zero | Negative | Positive |
|---|---|---|---|
| Body `x` | No forward travel | Reverse (away from the caster) | Forward of the drive axle (caster direction) |
| Body `y` | On the sagittal plane | Toward robot-right | Toward robot-left |
| Yaw | Heading held | CW viewed from above (turn toward robot-right) | CCW viewed from above (turn toward robot-left) |
| Wheel RPM | That wheel at rest | That wheel drives the body `−x` | That wheel drives the body `+x` |

Track `b = 170 mm` and wheel Ø84 mm (`r = 42 mm`) are **inherited geometry** for converting `v,ω` into wheel RPM. They are not a SKU.

Differential:

- `v_L = v − ω b/2`
- `v_R = v + ω b/2`

`ω` in SI (rad/s) in that pair. A keyframe such as `t400 v=0.20` means 0.20 m/s forward at `t = 400 ms`. Yaw is written in °/s in the panels (`ω=180`) and converted in the export tables. Report both body and wheel numbers in those tables.

### Curve language

These names are the base analogue of RP-01's `MJ5` / `MS7` / `BRAKE`. Firmware exports this library, not a nameless trapezoid.

| Code | Shape | Character use |
|---|---|---|
| `LAUNCH` | Jerk-limited accel from rest to a cruise; onset legible, peak acceleration bounded | Creep, come, follow, startle reverse |
| `CRUISE` | Constant body speed; heading held unless an `ARC` is specified | Creep, come mid-phrase, follow |
| `DECEL0` | Shaped decel through zero with no dwell at `v=0` | Wiggle reversals |
| `PIVOT` | In-place yaw, `v≈0`, shaped `ω` | Dramatic turn-toward-caller |
| `ARC` | Constant-radius coupled `v,ω`; `ω = v/R` | Follow's gentle turn |
| `SPIN` | High in-place yaw, multiple rotations, `v≈0` | Excited spin |
| `WIGGLE` | Declining rest-to-rest reversals along `x`, symmetric, through zero | Side-to-side |
| `BRAKE` | Online jerk-limited deceleration from the current `(v,ω)` | Controlled stop, obstacle, cancel |
| `HOLD` | Intentional stillness; commanded `v*=0`, `ω*=0` | Rest, freeze, attention, inhibited tabletop |

A dramatic pivot never means a step yaw command. A wiggle never means a bang-bang reverse. Both mean a shaped stroke whose onset is legible, whose peak acceleration is bounded, and whose exit is a settle rather than a bounce. Repeated reversals must not be equal-amplitude square waves. The first cycle carries the greatest statement; later cycles decline, as RP-01's laugh does.

## 2. Design envelopes

“Minimum viable” is a credible floor-locomotion envelope that still reads as the twelve panels in `intent.md`. “Best case” is design headroom, not a hidden requirement.

### 2.1 Speed envelope

| Class | Minimum viable | Best-case authored envelope | Why |
|---|---:|---:|---|
| Creep | `0.04 m/s` | `0.08 m/s` | Slowest deliberate motion that still reads as intent |
| Come cruise | `0.20 m/s` | `0.30 m/s` | Curious approach; `BM-03` sits inside this band |
| Follow | `0.35 m/s` | `0.45 m/s` | Walk-pace tracking. Hard cap `0.50 m/s` is inherited (CON-19) and is **not** authored past here |
| Fast expressive | `0.50 m/s` | `0.60 m/s` | Envelope only. G02 cannot-exceed is `BD-06`, not this file. `0.70 m/s` is a drivetrain design point, not a commanded storyboard speed |

Follow ≤ 0.5 m/s is slower than a typical adult walk. That is the character: the body attends, it does not chase.

### 2.2 Yaw envelope

| Class | Minimum viable | Best-case authored envelope | Why |
|---|---:|---:|---|
| Pivot | `120 °/s` | `180 °/s` | One decisive turn-toward-caller; `BM-05` uses the upper part of this band |
| Spin | `180 °/s` | `220 °/s` | Excited full rotations. `300 °/s` is drivetrain-dependent headroom and is **never** commanded in these panels |

### 2.3 Acceleration, settle and reversal quality

| Class | Minimum viable | Best-case target | Why |
|---|---|---|---|
| Authored `a_peak` | `0.80 m/s²` | `1.00 m/s²` | `BM-07` and `BM-08` control this. The value sits **below** the `1.98 m/s²` placement-target `a_tip` and **must be re-checked** against `physics.md`'s RANGE. This file does not claim margin |
| Settle to hold after last command | `≤ 350 ms` | `≤ 250 ms` | Stillness that reads as a decision, not a coast |
| Reversal deadband | A visible stop of `≤ 80 ms` at zero is a failure of `BM-07` | Same quality, tighter through-zero | Quality hypothesis, **not** a gate. `DECEL0` must not pause |

“Fast” never means a step command or an unbounded current spike. It means a shaped stroke whose peak acceleration stays inside this envelope until `physics.md` says otherwise.

## 3. Storyboard panels

Times are measured from the start of the base phrase. `L` and `R` below are the left and right drive wheels. Eye, audio and person-perception cues remain in `intent.md`; they do not change these base requirements. Head phrases `HM-*` may run concurrently; they do not authorize body roll.

Keyframes use `v` in m/s, `ω` in °/s, `x` in mm from the phrase origin. Curve names are the §1 library.

### BM-00 — Off / inhibited rest

**Audience read:** M4 is off or motion-inhibited, physically quiet and safe—not actively frozen in an artificial pose, and not a wagon that rolls when touched.

| Version | Panels | Curve |
|---|---|---|
| Minimum viable | Motor power removed or drive inhibited → `v=0 ω=0`. A nudge of ~2 N at the shell must not produce a visible roll. An `HM-*` head reaction must not roll the body. | `HOLD` (uncommanded) |
| Best case | Same stillness without a slow creep-out, a caster wander, or an audible residual drive. | `HOLD` |

This is a mechanical / inhibit outcome, not an animated trajectory. Interruption is energize-and-arm into `BM-01`; it is not a stored goal.

Never: freewheel.

### BM-01 — Zero-velocity hold, drive armed

**Audience read:** the body is calmly available and still; stillness feels intentional rather than parked-in-neutral. The head may perform; the base does not twitch against it.

`K0 HOLD: v=0 ω=0` with motors enabled at `v*=0`.

The hold must reject the inherited RP-01 paper yaw peak of `0.1099 N·m`. That figure is an inherited paper peak, not a BM-authored number.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | Armed `v*=0 ω*=0` through a representative `HM-*` yaw snap; no visible body yaw, walk or roll | `HOLD` |
| Best case | Same rejection without a visible twitch, a walk of the contact patches, or audible hunting | `HOLD` |

Interruption is a valid motion goal or a cancel into inhibit; it does not “help” the hold by pulsing the wheels.

Never: twitch, walk, audible hunting.

### BM-02 — Creep

**Audience read:** the slowest deliberate motion that still reads as intent—not as a stall that suddenly breaks free.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0` → `t200 v=0.04 CRUISE` for 400 mm / 10 s → `t10200 v=0.04` → `t10400 v=0 HOLD`. `a = 0.20 m/s²` | `LAUNCH` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0` → `t400 v=0.08 CRUISE` for 400 mm / 5 s → `t5400 v=0.08` → `t5800 v=0 HOLD`. `a = 0.20 m/s²` | Same family; quieter settle |

The encoder must resolve this speed. This file does not name a CPR.

Interruption from creep is `BM-12`; it does not jump to come/follow speed.

Never: stall-then-jump; audible cogging that reads as a limp.

### BM-03 — Curious approach

**Audience read:** M4 starts about 1.5 m from the person-mark, comes forward in two hesitant steps, and settles in the 0.6–0.9 m band—not a single continuous roll-in to the person's feet.

Travel is ~0.75 m (stop ~0.75 m from the mark). Phrase: launch → cruise → pause 400 ms → cruise → decel to rest. Total 4–6 s. `a_peak = 0.40 m/s²`. Two-step hesitate.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0` → `t500 v=0.20` → `t1800 v=0.20` → `t2300 v=0 HOLD 400` → `t2700 v=0` → `t3200 v=0.20` → `t4500 v=0.20` → `t5000 v=0 HOLD`. ~0.72 m in ~5.0 s | `LAUNCH` → `CRUISE` → `HOLD` → `LAUNCH` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0` → `t550 v=0.22` → `t1700 v=0.22` → `t2250 v=0 HOLD 400` → `t2650 v=0` → `t3200 v=0.22` → `t4350 v=0.22` → `t4900 v=0 HOLD`. ~0.75 m in ~4.9 s | Same two-step; faster first read, very soft arrival |

Come-cruise envelope headroom to `0.30 m/s` is not used in this phrase; `0.22 m/s` is the authored curious pace.

Interruption (person motion, cancel, hazard) does not complete the second step from a stored range. It brakes from the current `v`.

Never: a single continuous roll-in; overshoot into the person's feet.

### BM-04 — Follow

**Audience read:** steady walk-pace tracking along a 3.0 m route with one gentle 45° arc of radius ~1.2 m; heading corrections disappear into the path rather than reading as indecision.

Regulation: stay ≤ `0.50 m/s` always (inherited cap). `a = 0.35 m/s²`. Duration ~8–10 s. Arc length ≈ 0.94 m; `ω ≈ v/R` so ~19 °/s at 0.40 m/s and ~21 °/s at 0.45 m/s.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t1150 v=0.40` → `t3500` enter `ARC R≈1.2 ω≈+19` → `t5850` exit `ARC ω=0` → `t7500 v=0.40` → `t8650 v=0 HOLD`. Route 3.0 m in ~8.7 s | `LAUNCH` → `CRUISE` → `ARC` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t1300 v=0.45` → `t3300` enter `ARC R≈1.2 ω≈+21` → `t5400` exit `ARC ω=0` → `t6700 v=0.45` → `t8000 v=0 HOLD`. Route 3.0 m in ~8.0 s | Same family; less launch time in the phrase, still ≤ `0.50` |

No hunting: heading wobble that reads as indecision is a failure of this phrase, not extra life.

Interruption is a replaced follow goal (latest-wins cruise) or `BM-10` / `BM-12`. It never finishes a stale arc after the route is cancelled.

Never: exceed `0.50 m/s`; cut the corner of the arc with a pivot.

### BM-05 — Dramatic turn-toward-caller

**Audience read:** one decisive in-place pivot that lands on heading—as if M4 heard its name—not a walk-while-turning and not a spin.

In-place pivot `180°`. Time-to-peak ~250 ms. Settle ≤ 300 ms. Wheel `v` at `180 °/s` = `0.267 m/s` (`ω b/2`).

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t250 ω=140` → `t1260 ω=140` → `t1560 ω=0 HOLD`. `v` held ~0 throughout | `PIVOT` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t250 ω=180` → `t975 ω=180` → `t1275 ω=0 HOLD`. `α_peak`: `180 °/s` in `0.25 s` → `720 °/s² = 12.6 rad/s²` | `PIVOT` → `HOLD` |

Interruption during the pivot is `BM-12` from the current `ω`; it does not complete the 180° from a stored heading unless that heading is still the live goal.

Never: walk-while-turning (`v_body` must stay ~0); overshoot > 10° without a corrective settle.

### BM-06 — Excited spin

**Audience read:** two full rotations on the spot that end crisply, upright, on the original heading—not a travelling top and not a move that keeps going after the stop.

Two revolutions (`720°`), end on original heading ±10° authored (the scored threshold is later). Duration ~3.5–5 s including settle. Wheel `v` at `220 °/s` = `0.326 m/s`.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t250 ω=180` → `t3975 ω=180` → `t4275 ω=0 HOLD`. ~4.3 s including settle | `SPIN` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t250 ω=220` → `t3250 ω=220` → `t3550 ω=0 HOLD`. ~3.6 s including settle | `SPIN` → `HOLD` |

`300 °/s` is not used. Translation of more than ~30 mm is a walk, not a spin.

Interruption is `BM-12`; the remaining revolutions are discarded.

Never: translate more than ~30 mm (walk); tip; continue after the stop command.

### BM-07 — Side-to-side wiggle

**Audience read:** several small forward-back chuckles of the body, strongest first, declining like a laugh—not a shove, not a stall at mid-stroke, not a caster that steers a new heading.

This is the **highest-risk** Core base performance: a reversal. ±40 mm (minimum viable) / ±30 mm (best case; smaller is harder) along `x`, three cycles, declining amplitude. Half-cycle `T = 0.50 s`, so `a_peak ~ 0.80–1.00 m/s²` under min-jerk. Symmetric. Decel through zero with no visible deadband.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 x=0` → `t250 x=+40` → `t500 x=0` → `t750 x=-40` → `t1000 x=0` → `t1250 x=+32` → `t1500 x=0` → `t1750 x=-32` → `t2000 x=0` → `t2250 x=+20` → `t2500 x=0` → `t2750 x=-16` → `t3000 x=0 HOLD`. `a_peak = 0.80 m/s²` | `WIGGLE` (`DECEL0` at every zero crossing) |
| Best case | `t0 x=0` → `t250 x=+30` → `t500 x=0` → `t750 x=-30` → `t1000 x=0` → `t1250 x=+24` → `t1500 x=0` → `t1750 x=-24` → `t2000 x=0` → `t2250 x=+16` → `t2500 x=0` → `t2750 x=-12` → `t3000 x=0 HOLD`. `a_peak = 1.00 m/s²` | Same declining `WIGGLE`; tighter deadband |

A visible stop of ≤ 80 ms at zero is a failure of `BM-07`. That is a quality hypothesis, not a gate.

Interruption is `BM-12` from the current `v`; it does not finish the remaining pulses.

Never: a lurch that reads as a shove; a pause at zero that reads as a stall; caster-steer heading change > 5° per cycle.

### BM-08 — Startle retreat

**Audience read:** an immediate reverse away from a frontal surprise, then a frozen assessment. The freeze is as important as the speed.

Reverse 150 mm (minimum viable) / 200 mm (best case), then freeze `HOLD`. Time-to-peak ~200 ms. Reverse launch loads the caster. `a_peak = 0.80 / 1.00 m/s²`.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0` → `t200 v=-0.16` → `t940 v=-0.16` → `t1140 v=0 HOLD`. ~150 mm reverse, then freeze | `LAUNCH` (reverse) → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0` → `t200 v=-0.20` → `t1000 v=-0.20` → `t1200 v=0 HOLD`. ~200 mm reverse, then freeze | Same family; sharper onset at `a_peak = 1.00 m/s²` |

The 200 ms value is outbound-to-peak, not out-and-return.

Interruption after freeze is a new phrase from rest; the retreat does not bounce forward to “recover” unless a later phrase says so.

Never: a forward hop first; a tip onto the caster; continued roll after freeze.

### BM-09 — Controlled brake

**Audience read:** from each speed band, M4 stops as if it meant to—not as if it ran out of road.

Brake from `0.15`, `0.40`, `0.50` m/s, and from `0.60` m/s as an **unscored exploratory**. Do not author `0.70` as a commanded storyboard speed; `0.70` is a drivetrain design point. Overshoot < 20 mm authored. Rollback after stop is a failure. `BRAKE` profile.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | From each scored `v`: `BRAKE` at `a_peak = 0.80 m/s²` to `v=0 HOLD`. Implied ideal stop `d = v²/(2a)` ≈ 14 / 100 / 156 mm from 0.15 / 0.40 / 0.50. Exploratory 0.60 ≈ 225 mm, not scored here | `BRAKE` → `HOLD` |
| Best case | Same entries at `a_peak = 1.00 m/s²`. Implied ideal stop ≈ 11 / 80 / 125 mm from 0.15 / 0.40 / 0.50. Exploratory 0.60 ≈ 180 mm, not scored here | `BRAKE` → `HOLD` |

Those distances are kinematic implications of the authored `a_peak`, not registered stopping gates.

Interruption is already the brake; a second cancel does not replay the previous cruise.

Never: a stop that overshoots as if surprised; rollback after `v=0`; coast.

### BM-10 — Obstacle intervention

**Audience read:** from a follow cruise, a person-leg proxy appears and M4 stops short of it, visibly, without slewing—as if it noticed, not as if it chose a new path.

Detection-to-decel ≤ 50 ms is an inherited invariant (CA-12), not a BM invention. Clearance is a G03 number, not here: this panel authors “stops short, visibly, without slewing.” V1 is stop-only; redirect is `BD-02`.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | During `BM-04` cruise at `v=0.40`: proxy appears → detection-to-decel ≤ 50 ms → `BRAKE` to `v=0 HOLD`, short of the object, heading held | `BRAKE` → `HOLD` |
| Best case | During `BM-04` cruise at `v=0.45`: same intervention; stop reads as a decision rather than a skid | `BRAKE` → `HOLD` |

Interruption *is* the intervention. The follow route is discarded; it is not finished after the object is cleared unless a new goal says so.

Never: swerve as if it chose a path; clip the object; spin in place as a panic.

### BM-11 — Tabletop calibration creep

**Audience read:** on the table, nothing moves unless it is explicitly armed; when armed, a slow creep stays inside a marked circle and stops well inside the mark if an edge appears.

`ONLY` when armed. `v = 0.04 / 0.06 m/s`. The circle radius is a `physics.md` proposal (CON-TBD-14); this file does not set it. Ordinary come/follow/spin stay inhibited.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | Armed only: `t0 v=0` → `t200 v=0.04 CRUISE` inside the marked circle. Edge appearance → `BRAKE` → `HOLD` well inside the mark | `LAUNCH` → `CRUISE` / `BRAKE` → `HOLD` |
| Best case | Armed only: `t0 v=0` → `t300 v=0.06 CRUISE` inside the marked circle. Same edge stop, cleaner settle | Same family |

The catch fixture is a rig rule, not a performance.

Interruption: disarm, inhibit, expiry or edge detection hands immediately to `BRAKE` then `HOLD`. Come/follow/spin commands are rejected.

Never: motion without arm; come/follow/spin; an uncaught departure.

### BM-12 — Controlled cancel

**Audience read:** the current motion stops cleanly without completing stale beats or producing a violent jerk—the body analogue of `HM-18`.

Jerk-limited `BRAKE` from arbitrary `(v,ω)`. Settle, never coast.

| Version | Panels | Curve |
|---|---|---|
| Minimum viable proposal | Cancel accepted → no later authored keyframe begins → jerk/acceleration-limited deceleration from the measured state → zero intentional velocity within 350 ms where physically safe → `HOLD` | `BRAKE` → `HOLD` |
| Best-case proposal | Same sequence with zero intentional velocity within 250 ms where the validated load and current `(v,ω)` permit | `BRAKE` → `HOLD` |

These are storyboard proposals, not RP03-G01 thresholds. Emergency motor-power removal, feedback loss and controller failure have different physical behaviour and must be registered separately after the drivetrain is known.

Never: a stored goal replayed after cancel; a coast.

## 4. Motion-profile assignments and kinematic export

### 4.1 Normalized profile library

Body coordinates. Wheel speeds follow `v_L = v − ω b/2`, `v_R = v + ω b/2` with `b = 0.170 m`. Wheel RPM uses `r = 0.042 m`, circumference `2πr = 0.2639 m`: `n = v_wheel / 0.2639 × 60`.

For a trapezoid **launch** from rest to commanded `v` over duration `T` with limit `a_max`:

- `v_peak = min(v, a_max T)`
- `t_acc = v_peak / a_max`
- `a_peak = a_max` when `t_acc ≤ T`, else the move cannot reach `v` and `v_peak = a_max T`

For a rest-to-rest **brake** from `v` with the same `a_max`: `t_stop = v / a_max`, `d = v² / (2 a_max)` (ideal, no latency).

| Code | Body law | Peaks | Endpoint / connection |
|---|---|---|---|
| `HOLD` | `v=0`, `ω=0` | all zero | No intentional motion |
| `LAUNCH` | Jerk-limited ramp to `v*` (or `ω*` on a pivot/spin) | `v_peak = min(v*, a_max T)`, `a_peak = a_max` | Zero velocity at start; hands to `CRUISE` or `HOLD` |
| `CRUISE` | Constant `v*`, `ω=0` | `a=0`, `α=0` | Holds heading |
| `ARC` | Constant `v*`, `ω = v*/R` | `v_L = v*(1 − b/(2R))`, `v_R = v*(1 + b/(2R))` for yaw+ | No pivot shortcut |
| `PIVOT` | `v=0`, trapezoid/jerk-limited `ω` | `ω_peak = min(ω*, α_max T)`, `v_L = −ω b/2`, `v_R = +ω b/2` | Body translation ~0 |
| `SPIN` | `PIVOT` at higher `ω`, multiple revolutions | same wheel pair; `ω_peak` from `BM-06` | End on commanded heading |
| `DECEL0` | Shaped reversal through `v=0` | `a_peak` bounded; `t_dwell at 0 = 0` | C¹ velocity through zero |
| `WIGGLE` | Declining rest-to-rest `x` strokes, `DECEL0` at each zero | For min-jerk stroke `Δx` in `T`: `v_peak = 1.875 Δx/T`, `a_peak = 5.7735 Δx/T²`. Authored `T = 0.50 s` half-cycle, `a_peak` held to `0.80–1.00 m/s²` | First cycle largest; no pause at zero |
| `BRAKE` | Online jerk-limited stop from current `(v,ω)` | configured `a_max`, `α_max`; no single `Δx/T` coefficient | Initial state varies; no stored-goal replay |

`LAUNCH` / `PIVOT` / `SPIN` use a jerk-limited S-curve rather than a raw trapezoid so endpoint acceleration is not a step. Coefficients may follow RP-01's `MJ5` (`Cᵥ = 1.875`, `Cₐ = 5.7735`) on rest-to-rest segments; the **exported names** remain this library.

### 4.2 Per-motion authored profile ledger

Values are the panel's **best-case** command unless a range is shown. `t_settle` is after the last motion command. Wheel RPM is at the stated body `v_peak` or, for pivot/spin, at `|ω| b/2`.

| Panel | profile | `v_peak` | `a_peak` | `ω_peak` | `α_peak` | `t_settle` | notes |
|---|---|---:|---:|---:|---:|---:|---|
| `BM-00` | `HOLD` | 0 | 0 | 0 | 0 | — | Unpowered / inhibited. ~2 N nudge must not roll |
| `BM-01` | `HOLD` | 0 | 0 | 0 | 0 | — | Armed `v*=0`. Reject 0.1099 N·m inherited peak |
| `BM-02` | `LAUNCH`+`CRUISE` | 0.04 / 0.08 | 0.20 | 0 | 0 | ≤350 / ≤250 ms | 400 mm creep. Wheel 9.1 / 18.2 RPM |
| `BM-03` | `LAUNCH`+`CRUISE`+`HOLD` | 0.20 / 0.22 | 0.40 | 0 | 0 | phrase end `HOLD` | Two-step; 4–6 s; wheel 45.5 / 50.0 RPM |
| `BM-04` | `LAUNCH`+`CRUISE`+`ARC` | 0.40 / 0.45 | 0.35 | ~19 / ~21 °/s | small (`v/R`) | ≤350 / ≤250 ms | Cap 0.50 inherited. Wheel 90.9 / 102.3 RPM; arc `v_L,v_R` ≈ 0.372/0.428 and 0.418/0.482 |
| `BM-05` | `PIVOT` | ~0 body | ~0 body | 140 / 180 °/s | 560 / 720 °/s² (9.8 / 12.6 rad/s²) | ≤300 ms | Wheel 0.207 / 0.267 m/s → 47.2 / 60.7 RPM |
| `BM-06` | `SPIN` | ~0 body | ~0 body | 180 / 220 °/s | 720 / 880 °/s² if 250 ms launch | ≤350 / ≤250 ms | `720°`; wheel 0.267 / 0.326 m/s → 60.7 / 74.2 RPM |
| `BM-07` | `WIGGLE` | ~0.15 | 0.80 / 1.00 | ~0 | ~0 | ≤350 / ≤250 ms | ±40 / ±30 mm, 3 declining cycles, `DECEL0` |
| `BM-08` | reverse `LAUNCH`+`HOLD` | −0.16 / −0.20 | 0.80 / 1.00 | 0 | 0 | freeze | 150 / 200 mm; caster loaded in reverse |
| `BM-09` | `BRAKE` | from 0.15 / 0.40 / 0.50 (0.60 exploratory) | 0.80 / 1.00 | 0 | 0 | ≤350 / ≤250 ms | Overshoot < 20 mm authored. Wheel from 34.1 / 90.9 / 113.7 (136.4 exploratory) RPM |
| `BM-10` | `BRAKE` | from `BM-04` cruise | `BRAKE` limited | heading held | ~0 | ≤350 / ≤250 ms | Detection-to-decel ≤ 50 ms inherited. No clearance number here |
| `BM-11` | `LAUNCH`+`CRUISE` | 0.04 / 0.06 | low, inside creep `a` | 0 | 0 | `BRAKE` at edge | Armed only. Radius not set. Wheel 9.1 / 13.6 RPM |
| `BM-12` | `BRAKE` | arbitrary | configured limit | arbitrary | configured limit | ≤350 / ≤250 ms | `HM-18` analogue; no stored-goal replay |

Wheel RPM at body `v_peak` (`r = 0.042`, circ `= 0.2639`):

| Body `v` (m/s) | Wheel RPM |
|---:|---:|
| 0.04 | 9.1 |
| 0.06 | 13.6 |
| 0.08 | 18.2 |
| 0.15 | 34.1 |
| 0.22 | 50.0 |
| 0.40 | 90.9 |
| 0.45 | 102.3 |
| 0.50 | 113.7 |
| 0.60 | 136.4 |

| Body `ω` | Wheel `v` (`ω b/2`) | Wheel RPM |
|---|---:|---:|
| Pivot / spin `180 °/s` | 0.267 m/s | 60.7 |
| Spin `220 °/s` | 0.326 m/s | 74.2 |

These are authored V0.1 laws. Observer review can change a motion's profile, but that change also changes its peaks and invalidates its previous kinematic / torque calculation.

### 4.3 Controlling cases

Every launch, interior reversal and settle was evaluated against the envelopes in §2.

| Requirement | Controlling authored panel | Current value |
|---|---|---|
| `a_peak` | `BM-07` (and `BM-08` at the same `a`) | `0.80 / 1.00 m/s²` |
| `ω_peak` | `BM-06` | `220 °/s` commanded; `300 °/s` never commanded |
| `v_peak` commanded | `BM-04` | `0.45 m/s` (cap `0.50` inherited) |
| Min speed | `BM-02` | `0.04 m/s` |
| Reverse quality | `BM-07` | `DECEL0`; ≤ 80 ms visible deadband is a failure hypothesis |
| Hold | `BM-00` / `BM-01` | `v*=0` including `0.1099 N·m` rejection |
| Stopping | `BM-09` / `BM-10` / `BM-12` | `BRAKE`; overshoot < 20 mm authored on `BM-09` |
| Coverage | `BM-10` / `BM-11` | Stop-short / edge-inside-mark; no clearance or radius here |
| `α_peak` (pivot) | `BM-05` | `720 °/s² = 12.6 rad/s²` at `180 °/s` in `0.25 s` |

`BM-04` at `0.45 m/s` is the fastest **commanded character** cruise. Fast-expressive `0.60 m/s` appears only as an unscored `BM-09` exploratory entry. G02 cannot-exceed remains `BD-06`.

### 4.4 Envelope vs physics

These numbers are hypotheses. `physics.md` will say whether authored `a_peak = 1.00 m/s²` still has margin against the Layout 03 `a_tip` RANGE. If it does not, the storyboard is revised, or the CoM placement is restored — the follow cap is not.

This file claims no margin against `1.98 m/s²`. That figure is a placement target, not a mass-roll-up result.

## 5. Review and change rules

- Builder review may alter any speed, yaw or time before gate registration; changes must preserve the semantic read in `intent.md`.
- “Best case” is design headroom, not a hidden requirement. Failing it does not fail V1 when the minimum viable phrase remains readable and passes its later-approved gate.
- “Minimum viable” is not automatically a gate threshold. It becomes binding only when copied into a versioned gate-registration record and approved before scored data is inspected.
- Reference footage and human walk-pace data justify starting hypotheses only. RP-03 measurement and observer review decide whether Makad's actual movement is safe, repeatable and readable.
- Do not assign a pass threshold, name a motor, or set the tabletop footprint radius in this file. `physics.md` proposes; `gates.md` freezes.
- Any later whole-robot mass/CoM outside the range `physics.md` uses to evaluate `a_tip` invalidates the acceleration envelope in §2.3 until that RANGE is recomputed and this storyboard is re-checked.
