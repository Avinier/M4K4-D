# RP-03 Base Motion Storyboard

| Field | Value |
|---|---|
| Status | Provisional authored kinematics **v0.2** — design hypotheses, not registered gate thresholds. v0.2 adds the operating-case grammar, the `BM-03` permission chain, `BM-13`/`BM-14`, head-rocking on `BM-00/01`, and the freezeable forbidden-situation register |
| Owner | Project builder |
| Created | 2026-09-17 |
| Last updated | 2026-09-18 |
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

### Operating-case grammar

Every panel is an **operating case**, not only a velocity curve. Kinematics without mode, surface, head pose, mass/CoM, required sensors and a settle footprint are an incomplete brief. Fields:

| Field | What it names |
|---|---|
| `OM` | `OM-01` Floor / `OM-02` Tabletop inhibited-by-default / `OM-03` motion inhibited. App selection is an input, not the interlock |
| Surface | Named BD-04 article (`S-TILE`, `S-LAM`, `S-RUG`, `S-THR`), not the working labels tile / wood / rug / threshold |
| Initial pose | Body `(x, y, θ)` on the marked course, and whether the person-mark / obstacle / edge is in view |
| Head pose | Layout 03 pose at phrase start. `NEUTRAL` = yaw 0, pitch 0, roll 0. Head-pose CoM corners (`HP-PITCH-FWD`, `HP-PITCH-AFT`, `HP-YAW-L/R`) are BD-05 extras, not a dummy at 304 mm |
| Mass / CoM | BD-05 corner: `LOW` 1.65 kg, `HIGH` 3.10 kg+head, both CoM extremes that the rig can actually set. `HIGH_AFT` is illegal, not a corner |
| Required valid sensors | Stop-path channels that must be inside their age bound before travel is permitted. Unknown is inhibit |
| Interrupt | What pre-empts this panel, and whether a stored remainder may complete |
| Final footprint | Chassis polygon at `HOLD`, relative to the mark or origin. Logged, not inferred from a single tape point |
| Settle | Time to `HOLD` after the last motion command; rollback and unrequested second creep are named failures |

**Defaults**, unless a panel overrides them:

| Field | Default |
|---|---|
| `OM` | `OM-01` |
| Surface | Every named BD-04 article. `S-THR` is a geometric disturbance, not a μ band |
| Initial pose | Marked start; heading 0 along the course; person-mark / obstacle absent unless the panel is come, follow, or obstacle |
| Head pose | `NEUTRAL`. `BM-00/01` additionally score the Layout 03 pitch/yaw reaction (not only the 0.1099 N·m yaw couple) |
| Mass / CoM | Both BD-05 mass corners and both settable CoM extremes, plus the head-pose extras on `BM-00/01/06/07` |
| Required valid sensors | All stop-path channels in `BC-03`: three look-downs, analog-IR obstacle, bump, IMU lift/tip, encoder plausibility, `nFAULT`. Cliff channels covering the upcoming leading contact must be valid **before** travel, not only as an interrupt |
| Interrupt | `BM-12` from the current `(v, ω)`. Hazard → `BM-10` or edge `BRAKE`. Cancel discards the remainder |
| Final footprint | Axis-aligned bounding box of the 300 × 205 mm envelope at `HOLD`, tape-logged. Drift millimetres are a G01 quantity |
| Settle | ≤ 350 ms MV / ≤ 250 ms best-case after last command; no rollback; no unrequested second motion |

`BM-13` (tabletop demonstration) and `BM-14` (physical stop) are append-only panels. They are not folded into `BM-11` or `BM-12`.

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

| Field | This panel |
|---|---|
| `OM` | `OM-03`, or `OM-02` unarmed, or motor domain absent |
| Surface | All BD-04 named articles |
| Initial pose | Anywhere on the floor course or on the caught table; heading arbitrary |
| Head pose | `NEUTRAL` **and** Layout 03 pitch/yaw corners (`HP-PITCH-FWD/AFT`, `HP-YAW-L/R`). A mass dummy at 304 mm is not this panel |
| Mass / CoM | BD-05 four settable corners plus the head-pose extras |
| Required valid sensors | None required for the mechanical rest. If C3 is powered, unknown stop-path channels still inhibit any later arm |
| Interrupt | Energize-and-arm into `BM-01`. Not a stored goal |
| Final footprint | Must not translate or yaw from the parked polygon under a ~2 N shell nudge or a head phrase |
| Settle | Already at rest. Creep-out, caster wander, or freewheel is `FS-09` |

| Version | Panels | Curve |
|---|---|---|
| Minimum viable | Motor power removed or drive inhibited → `v=0 ω=0`. A nudge of ~2 N at the shell must not produce a visible roll. An `HM-*` head reaction — **yaw 0.1099 N·m and pitch 0.0953 N·m** (`fullproofmath.md`, `E`) — must not roll or rock the body. | `HOLD` (uncommanded) |
| Best case | Same stillness without a slow creep-out, a caster wander, or an audible residual drive. | `HOLD` |

**Head-induced rocking.** The inherited yaw couple on a 170 mm track is 0.646 N per wheel (0.027 N·m at the wheel). Layout 03 pitch peak 0.0953 N·m at 57.8 °/s is a sagittal couple of the same class: 0.0953 / 0.110 ≈ 0.87 N at the caster–axle pair (`physics.md` §2.8). Either can walk the contact patches on a backdrivable box. The named hold/vibration failure is a visible patch walk, audible hunting, or chassis pitch oscillation at laugh-frequency content (~10 Hz). Yaw-only screening is not this panel.

This is a mechanical / inhibit outcome, not an animated trajectory.

Never: freewheel (`FS-09`).

### BM-01 — Zero-velocity hold, drive armed

**Audience read:** the body is calmly available and still; stillness feels intentional rather than parked-in-neutral. The head may perform; the base does not twitch against it.

`K0 HOLD: v=0 ω=0` with motors enabled at `v*=0`.

The hold must reject the inherited RP-01 paper yaw peak of `0.1099 N·m` **and** the Layout 03 pitch peak of `0.0953 N·m`. Those figures are inherited paper peaks, not BM-authored numbers.

| Field | This panel |
|---|---|
| `OM` | `OM-01` armed, or `OM-02` unarmed (demo-still; see `BM-13`) |
| Surface | All BD-04 named articles |
| Initial pose | Marked start; heading 0 |
| Head pose | `NEUTRAL` plus the four head-pose CoM corners; score a representative `HM-*` yaw snap **and** a laugh-class pitch reversal |
| Mass / CoM | BD-05 four settable corners plus head-pose extras |
| Required valid sensors | All `BC-03` stop-path channels valid. IMU lift/tip is required at runtime from Phase B (BD-03) |
| Interrupt | A valid motion goal, or cancel into inhibit. The hold is not “helped” by pulsing the wheels |
| Final footprint | Same parked polygon. A walk of the patches is a fail |
| Settle | Continuous `HOLD`. Hunting is `FS-09` |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | Armed `v*=0 ω*=0` through a representative `HM-*` yaw snap **and** a laugh-class pitch reversal; no visible body yaw, walk, roll, or chassis rock | `HOLD` |
| Best case | Same rejection without a visible twitch, a walk of the contact patches, audible hunting, or a hold/vibration rock | `HOLD` |

Never: twitch, walk, audible hunting, hold/vibration rock (`FS-09`).

### BM-02 — Creep

**Audience read:** the slowest deliberate motion that still reads as intent—not as a stall that suddenly breaks free.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only. Creep is ordinary locomotion: rejected in `OM-02` |
| Surface | All BD-04 named articles. `S-RUG` pile and `S-THR` are the stick-slip / pitch-disturbance corners |
| Initial pose | Marked start; heading 0; 400 mm course clear |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | All `BC-03` channels valid **before** `LAUNCH`. Forward cliff + analog-IR must see the 400 mm path |
| Interrupt | `BM-12`. Does not jump to come/follow speed |
| Final footprint | +400 mm along x, heading held ±5° authored. Drift millimetres logged |
| Settle | Default settle; no rollback |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0` → `t200 v=0.04 CRUISE` for 400 mm / 10 s → `t10200 v=0.04` → `t10400 v=0 HOLD`. `a = 0.20 m/s²` | `LAUNCH` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0` → `t400 v=0.08 CRUISE` for 400 mm / 5 s → `t5400 v=0.08` → `t5800 v=0 HOLD`. `a = 0.20 m/s²` | Same family; quieter settle |

The encoder must resolve this speed. This file does not name a CPR.

Never: stall-then-jump; audible cogging that reads as a limp.

### BM-03 — Curious approach (permission chain)

**Audience read:** M4 notices a stationary person-mark about 1.5 m away, orients if it must, comes forward only while the path stays clear, hesitates once, and settles in the 0.6–0.9 m band—not a single continuous roll-in to the person's feet, and not a second unrequested creep after arrival.

This is a **permission chain**, not a stored two-step from 1.5 m. Obstacle is a travel *precondition*, not only an interrupt. Real-person follow and reacquire stay RP-07; the mark is a tape target.

| Step | Permission | Fail action |
|---|---|---|
| 1. Accept | A **fresh** stationary target (person-mark) with a live `BASE_GOAL`. Stale range after cancel is discarded | `NACK(EXPIRED)` / inhibit. No motion |
| 2. Align | If heading error to the mark is > 15° authored, `PIVOT` or a smooth `ARC` first. A walk-while-turning is not this step | `BM-12` from current `ω` |
| 3. Travel | Advance only **while stopping clearance exists** at the current `v` (`physics.md` §6 `d_stop` at the leading contact, analog-IR + cliffs valid). Two hesitant steps; pause 400 ms at `HOLD` between them | If clearance is lost: `BM-10` or `HOLD`. Do not complete the second step from a stored range |
| 4. Arrive | `BRAKE` into the **0.6–0.9 m** band. Overshoot into the mark is `FS-11` | `BM-12` from current `v` |
| 5. Settle | `HOLD` with no rollback and **no unrequested second creep** (`FS-06`) | A second creep requires a new `BASE_GOAL` |

Travel is ~0.75 m (stop ~0.75 m from the mark) once aligned. Phrase after alignment: launch → cruise → pause 400 ms → cruise → decel to rest. Total 4–6 s plus any align. `a_peak = 0.40 m/s²`.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only. Come is rejected in `OM-02` (`FS-02` / `FS-08`) |
| Surface | All BD-04 named articles |
| Initial pose | ~1.5 m from the person-mark; heading may be off-axis (align step). Mark is stationary |
| Head pose | `NEUTRAL` or a slight pitch-toward-mark; not a CoM corner unless BD-05 extras are on |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | All `BC-03` channels valid **before step 3**. Analog-IR look-ahead ≥ `d_stop` at come-cruise. Forward cliff valid. Bump is last layer |
| Interrupt | Person-mark motion, cancel, or hazard: brake from current `v`. Do not finish the second step |
| Final footprint | Chassis in the 0.6–0.9 m band, heading toward the mark ±10° authored, no second translation |
| Settle | Default settle. Rollback or a second creep is a fail |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | After align: `t0 v=0` → `t500 v=0.20` → `t1800 v=0.20` → `t2300 v=0 HOLD 400` → `t2700 v=0` → `t3200 v=0.20` → `t4500 v=0.20` → `t5000 v=0 HOLD`. ~0.72 m in ~5.0 s | Align `PIVOT`/`ARC` if needed → `LAUNCH` → `CRUISE` → `HOLD` → `LAUNCH` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | After align: `t0 v=0` → `t550 v=0.22` → `t1700 v=0.22` → `t2250 v=0 HOLD 400` → `t2650 v=0` → `t3200 v=0.22` → `t4350 v=0.22` → `t4900 v=0 HOLD`. ~0.75 m in ~4.9 s | Same chain; faster first read, very soft arrival |

Come-cruise envelope headroom to `0.30 m/s` is not used in this phrase; `0.22 m/s` is the authored curious pace.

Never: a single continuous roll-in; overshoot into the person's feet (`FS-11`); travel without clearance; unrequested second creep (`FS-06`).

### BM-04 — Follow

**Audience read:** steady walk-pace tracking along a 3.0 m route with one gentle 45° arc of radius ~1.2 m; heading corrections disappear into the path rather than reading as indecision.

Regulation: stay ≤ `0.50 m/s` always (inherited cap). `a = 0.35 m/s²`. Duration ~8–10 s. Arc length ≈ 0.94 m; `ω ≈ v/R` so ~19 °/s at 0.40 m/s and ~21 °/s at 0.45 m/s.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only |
| Surface | All BD-04 named articles. Straight-line drift is scored on `S-TILE` and `S-LAM` first |
| Initial pose | Marked start; 3.0 m route with one 45° arc; heading along the first leg |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | All `BC-03` valid **before** each cruise segment. Analog-IR look-ahead ≥ `d_stop` at 0.50 m/s (179 mm from caster). Target loss is an interrupt, not RP-07 reacquire |
| Interrupt | Replaced follow goal (latest-wins cruise) or `BM-10` / `BM-12`. Never finishes a stale arc |
| Final footprint | End of the 3.0 m route ±50 mm authored, heading along the last leg. Drift millimetres logged on the straight legs |
| Settle | Default settle |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t1150 v=0.40` → `t3500` enter `ARC R≈1.2 ω≈+19` → `t5850` exit `ARC ω=0` → `t7500 v=0.40` → `t8650 v=0 HOLD`. Route 3.0 m in ~8.7 s | `LAUNCH` → `CRUISE` → `ARC` → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t1300 v=0.45` → `t3300` enter `ARC R≈1.2 ω≈+21` → `t5400` exit `ARC ω=0` → `t6700 v=0.45` → `t8000 v=0 HOLD`. Route 3.0 m in ~8.0 s | Same family; less launch time in the phrase, still ≤ `0.50` |

No hunting: heading wobble that reads as indecision is `FS-04`, not extra life.

Never: exceed `0.50 m/s`; cut the corner of the arc with a pivot; hunt (`FS-04`).

### BM-05 — Dramatic turn-toward-caller

**Audience read:** one decisive in-place pivot that lands on heading—as if M4 heard its name—not a walk-while-turning and not a spin.

In-place pivot `180°`. Time-to-peak ~250 ms. Settle ≤ 300 ms. Wheel `v` at `180 °/s` = `0.267 m/s` (`ω b/2`).

| Field | This panel |
|---|---|
| `OM` | `OM-01` only |
| Surface | All BD-04 named articles. `S-RUG` pile is the scrub/caster-glitch corner |
| Initial pose | Marked centre; heading 0; 180° target |
| Head pose | `NEUTRAL` or a slight yaw-toward-caller; not a CoM corner unless extras are on |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | All `BC-03` valid. Lateral cliff/bump coverage during the sweep (`physics.md` §7.3) |
| Interrupt | `BM-12` from the current `ω`. Does not complete 180° from a stored heading unless that heading is still the live goal |
| Final footprint | Translation ≤ 30 mm authored; heading 180° ±10° authored |
| Settle | ≤ 300 ms |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t250 ω=140` → `t1260 ω=140` → `t1560 ω=0 HOLD`. `v` held ~0 throughout | `PIVOT` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t250 ω=180` → `t975 ω=180` → `t1275 ω=0 HOLD`. `α_peak`: `180 °/s` in `0.25 s` → `720 °/s² = 12.6 rad/s²` | `PIVOT` → `HOLD` |

Never: walk-while-turning (`v_body` must stay ~0); overshoot > 10° without a corrective settle.

### BM-06 — Excited spin

**Audience read:** two full rotations on the spot that end crisply, upright, on the original heading—not a travelling top and not a move that keeps going after the stop.

Two revolutions (`720°`), end on original heading ±10° authored (the scored threshold is later). Duration ~3.5–5 s including settle. Wheel `v` at `220 °/s` = `0.326 m/s`.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only. Spin is rejected in `OM-02` |
| Surface | All BD-04 named articles. `S-TILE` and `S-LAM` are the flutter/walk corners |
| Initial pose | Marked centre; heading 0 |
| Head pose | `NEUTRAL` **and** the head-pose CoM extras — spin with a yawed or pitched Layout 03 head is a BD-05 corner, not a dummy |
| Mass / CoM | BD-05 four settable corners plus head-pose extras |
| Required valid sensors | All `BC-03` valid before spin. IMU lift/tip required. A walking spin is `FS-05` |
| Interrupt | `BM-12`; remaining revolutions discarded. `BM-14` if the motor bus is cut |
| Final footprint | Translation ≤ ~30 mm; original heading ±10° authored. A walk is not a spin |
| Settle | Default settle; no continue-after-stop |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0 ω=0` → `t250 ω=180` → `t3975 ω=180` → `t4275 ω=0 HOLD`. ~4.3 s including settle | `SPIN` → `HOLD` |
| Best case | `t0 v=0 ω=0` → `t250 ω=220` → `t3250 ω=220` → `t3550 ω=0 HOLD`. ~3.6 s including settle | `SPIN` → `HOLD` |

`300 °/s` is not used. Translation of more than ~30 mm is `FS-05`.

Never: translate more than ~30 mm (walk); tip; continue after the stop command.

### BM-07 — Side-to-side wiggle

**Audience read:** several small forward-back chuckles of the body, strongest first, declining like a laugh—not a shove, not a stall at mid-stroke, not a caster that steers a new heading.

This is the **highest-risk** Core base performance: a reversal. ±40 mm (minimum viable) / ±30 mm (best case; smaller is harder) along `x`, three cycles, declining amplitude. Half-cycle `T = 0.50 s`, so `a_peak ~ 0.80–1.00 m/s²` under min-jerk. Symmetric. Decel through zero with no visible deadband.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only |
| Surface | All BD-04 named articles. Caster trail on `S-TILE` is the heading-glitch corner |
| Initial pose | Marked origin; heading 0 |
| Head pose | `NEUTRAL` plus head-pose extras — a pitched-forward head changes `x_CoM` into the `a_tip` range |
| Mass / CoM | BD-05 four settable corners plus head-pose extras. Commanded `a_peak` re-checked against that corner's `a_tip` |
| Required valid sensors | All `BC-03` valid. IMU lift/tip required before a 0.80–1.00 m/s² reversal |
| Interrupt | `BM-12` from current `v`; remaining pulses discarded |
| Final footprint | Return to origin ±10 mm authored; heading change ≤ 5° per cycle |
| Settle | Default settle |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 x=0` → `t250 x=+40` → `t500 x=0` → `t750 x=-40` → `t1000 x=0` → `t1250 x=+32` → `t1500 x=0` → `t1750 x=-32` → `t2000 x=0` → `t2250 x=+20` → `t2500 x=0` → `t2750 x=-16` → `t3000 x=0 HOLD`. `a_peak = 0.80 m/s²` | `WIGGLE` (`DECEL0` at every zero crossing) |
| Best case | `t0 x=0` → `t250 x=+30` → `t500 x=0` → `t750 x=-30` → `t1000 x=0` → `t1250 x=+24` → `t1500 x=0` → `t1750 x=-24` → `t2000 x=0` → `t2250 x=+16` → `t2500 x=0` → `t2750 x=-12` → `t3000 x=0 HOLD`. `a_peak = 1.00 m/s²` | Same declining `WIGGLE`; tighter deadband |

A visible stop of ≤ 80 ms at zero is a failure of `BM-07`. That is a quality hypothesis, not a gate.

Never: a lurch that reads as a shove (`FS-10`); a pause at zero that reads as a stall; caster-steer heading change > 5° per cycle.

### BM-08 — Startle retreat

**Audience read:** an immediate reverse away from a frontal surprise, then a frozen assessment. The freeze is as important as the speed.

Reverse 150 mm (minimum viable) / 200 mm (best case), then freeze `HOLD`. Time-to-peak ~200 ms. Reverse launch loads the caster. `a_peak = 0.80 / 1.00 m/s²`.

| Field | This panel |
|---|---|
| `OM` | `OM-01` only |
| Surface | All BD-04 named articles |
| Initial pose | Marked origin; heading 0; surprise is frontal |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners. Reverse loads the caster; `HIGH` with a pitched-forward head is the tip-over-caster corner |
| Required valid sensors | All `BC-03` valid. **Rear cliff** covering the skid contact must be valid before reverse travel. Forward analog-IR is not a reverse permission |
| Interrupt | After freeze, a new phrase from rest. The retreat does not bounce forward to “recover” |
| Final footprint | −150 / −200 mm along x, heading held. No forward hop |
| Settle | Freeze `HOLD` |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 v=0` → `t200 v=-0.16` → `t940 v=-0.16` → `t1140 v=0 HOLD`. ~150 mm reverse, then freeze | `LAUNCH` (reverse) → `CRUISE` → `BRAKE` → `HOLD` |
| Best case | `t0 v=0` → `t200 v=-0.20` → `t1000 v=-0.20` → `t1200 v=0 HOLD`. ~200 mm reverse, then freeze | Same family; sharper onset at `a_peak = 1.00 m/s²` |

The 200 ms value is outbound-to-peak, not out-and-return.

Never: a forward hop first; a tip onto the caster; continued roll after freeze.

### BM-09 — Controlled brake

**Audience read:** from each speed band, M4 stops as if it meant to—not as if it ran out of road.

Brake from `0.15`, `0.40`, `0.50` m/s, and from `0.60` m/s as an **unscored exploratory**. Do not author `0.70` as a commanded storyboard speed; `0.70` is a drivetrain design point. Overshoot < 20 mm authored. Rollback after stop is a failure. `BRAKE` profile.

This panel is **commanded `BRAKE`**. Motor-bus cutoff coast is `BM-14`. G01 scores both as distinct metrics.

| Field | This panel |
|---|---|
| `OM` | `OM-01` |
| Surface | All BD-04 named articles |
| Initial pose | Marked start of the speed-band course; heading 0; already at the scored `v` |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | All `BC-03` valid. The brake itself does not wait on a new sample; it is C3-owned |
| Interrupt | Already the brake. A second cancel does not replay the previous cruise |
| Final footprint | Ideal `d = v²/(2a)` plus latency; overshoot < 20 mm authored; no rollback |
| Settle | Default settle |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | From each scored `v`: `BRAKE` at `a_peak = 0.80 m/s²` to `v=0 HOLD`. Implied ideal stop `d = v²/(2a)` ≈ 14 / 100 / 156 mm from 0.15 / 0.40 / 0.50. Exploratory 0.60 ≈ 225 mm, not scored here | `BRAKE` → `HOLD` |
| Best case | Same entries at `a_peak = 1.00 m/s²`. Implied ideal stop ≈ 11 / 80 / 125 mm from 0.15 / 0.40 / 0.50. Exploratory 0.60 ≈ 180 mm, not scored here | `BRAKE` → `HOLD` |

Those distances are kinematic implications of the authored `a_peak`, not registered stopping gates.

Never: a stop that overshoots as if surprised; rollback after `v=0`; coast (`FS-01`). Coast after *cutoff* is `BM-14`, not this never.

### BM-10 — Obstacle intervention

**Audience read:** from a follow cruise, a person-leg proxy appears and M4 stops short of it, visibly, without slewing—as if it noticed, not as if it chose a new path.

Detection-to-decel ≤ 50 ms is an inherited invariant (CA-12), not a BM invention. Clearance is a G03 number, not here: this panel authors “stops short, visibly, without slewing.” V1 is stop-only; redirect is `BD-02`.

| Field | This panel |
|---|---|
| `OM` | `OM-01` |
| Surface | At least `S-TILE` and `S-LAM` |
| Initial pose | `BM-04` cruise toward a registered obstacle (person-leg proxy, furniture leg, box, cable/flat, 20 mm caster-shadow cube) |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | Analog-IR in the stop path; cliffs valid; bump last layer. ToF is telemetry |
| Interrupt | *Is* the intervention. The follow route is discarded |
| Final footprint | Short of the object face; heading held (no slew-as-path) |
| Settle | Default settle |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | During `BM-04` cruise at `v=0.40`: proxy appears → detection-to-decel ≤ 50 ms → `BRAKE` to `v=0 HOLD`, short of the object, heading held | `BRAKE` → `HOLD` |
| Best case | During `BM-04` cruise at `v=0.45`: same intervention; stop reads as a decision rather than a skid | `BRAKE` → `HOLD` |

Never: swerve as if it chose a path; clip the object; spin in place as a panic.

### BM-11 — Tabletop calibration creep

**Audience read:** on the table, nothing moves unless it is explicitly armed; when armed, a slow creep stays inside a marked circle and stops well inside the mark if an edge appears.

`ONLY` when armed. `v = 0.04 / 0.06 m/s`. The circle radius is a `physics.md` proposal (CON-TBD-14); this file does not set it. Ordinary come/follow/spin stay inhibited.

This is **not** the tabletop demonstration. Head-and-face-active / base-still is `BM-13`. Folding demo-still into this panel would reverse the audience read.

| Field | This panel |
|---|---|
| `OM` | `OM-02` **with** a live `CC-12C_ARM` nonce. Unarmed `OM-02` is `BM-13` / `BM-00` |
| Surface | Caught tabletop; dark and glossy samples. Not BD-04 floors |
| Initial pose | Inside the marked CON-TBD-14 circle; heading along an edge-test lane (0 / 45 / 90 / 135 / 180°) |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners that fit the table fixture |
| Required valid sensors | All three look-downs valid **before** creep. Edge appearance → `BRAKE`. Catch verified this session — a row without it is invalid |
| Interrupt | Disarm, inhibit, expiry or edge → `BRAKE` then `HOLD`. Come/follow/spin `NACK(INHIBITED)` |
| Final footprint | Inside the mark by ≥ 40 mm authored at edge stop; otherwise inside the circle |
| Settle | `BRAKE` then `HOLD` |

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | Armed only: `t0 v=0` → `t200 v=0.04 CRUISE` inside the marked circle. Edge appearance → `BRAKE` → `HOLD` well inside the mark | `LAUNCH` → `CRUISE` / `BRAKE` → `HOLD` |
| Best case | Armed only: `t0 v=0` → `t300 v=0.06 CRUISE` inside the marked circle. Same edge stop, cleaner settle | Same family |

The catch fixture is a rig rule, not a performance.

Never: motion without arm (`FS-02`); come/follow/spin (`FS-08`); an uncaught departure (`FS-03`).

### BM-12 — Controlled cancel

**Audience read:** the current motion stops cleanly without completing stale beats or producing a violent jerk—the body analogue of `HM-18`.

Jerk-limited `BRAKE` from arbitrary `(v,ω)`. Settle, never coast. This is **commanded `BRAKE`**. Motor-bus cutoff is `BM-14`.

| Field | This panel |
|---|---|
| `OM` | `OM-01` or armed `OM-02` |
| Surface | The surface of the interrupted panel |
| Initial pose | Arbitrary `(v, ω)` of a live panel |
| Head pose | Whatever the interrupted panel had |
| Mass / CoM | Same corner as the interrupted panel |
| Required valid sensors | Cancel does not wait on a new sample. Unknown sensors already inhibit |
| Interrupt | Already the cancel. A second cancel does not replay |
| Final footprint | From the interrupted state; no stored-goal completion |
| Settle | ≤ 350 / ≤ 250 ms where physically safe |

| Version | Panels | Curve |
|---|---|---|
| Minimum viable proposal | Cancel accepted → no later authored keyframe begins → jerk/acceleration-limited deceleration from the measured state → zero intentional velocity within 350 ms where physically safe → `HOLD` | `BRAKE` → `HOLD` |
| Best-case proposal | Same sequence with zero intentional velocity within 250 ms where the validated load and current `(v,ω)` permit | `BRAKE` → `HOLD` |

These are storyboard proposals, not RP03-G01 thresholds.

Never: a stored goal replayed after cancel; a coast (`FS-01`).

### BM-13 — Tabletop demonstration (base still)

**Audience read:** M4 is on the table as a face and a head. It looks, listens, and holds still. It does not walk on furniture.

Head and face remain active (`HM-*`, `FACE_STATE`). The base stays at `HOLD`. Ordinary locomotion — come, follow, spin, creep, wiggle, retreat — is **rejected**. This is the V1 user-facing tabletop (BD-01). It is **not** `BM-11`. `BM-11` is the owed caught-fixture calibration motion, the opposite audience read.

| Field | This panel |
|---|---|
| `OM` | `OM-02` **unarmed**. `BASE_ENABLE` may be true for hold-current; `CC-12C_ARM` is **absent** |
| Surface | Caught tabletop. Catch still verified this session even though the base must not move — an accidental departure is `FS-03` |
| Initial pose | Inside the marked circle at rest; heading arbitrary |
| Head pose | Any authored `HM-*` including laugh-class pitch and yaw snaps |
| Mass / CoM | BD-05 corners that fit the table, plus head-pose extras — this is the hold/vibration case on a table |
| Required valid sensors | Cliffs valid so an accidental roll is still an edge inhibit. Analog-IR may be don't-care for a still base; unknown cliff is still inhibit |
| Interrupt | Any locomotion `BASE_GOAL` → `NACK(INHIBITED)`. Arming for `BM-11` is a new nonce, not a continuation |
| Final footprint | The parked polygon. Any translation is a fail of the demonstration |
| Settle | Continuous `HOLD` while the head performs |

| Version | Panels | Curve |
|---|---|---|
| Minimum viable | Unarmed `OM-02`: `v*=0 ω*=0`. Head/face may run. Come/follow/spin/creep `NACK(INHIBITED)` and produce no wheel motion | `HOLD` |
| Best case | Same stillness without caster wander, patch walk, or hold/vibration rock while the head laughs | `HOLD` |

Never: tabletop motion without arm (`FS-02`); ordinary locomotion on the table (`FS-08`); an uncaught departure (`FS-03`).

### BM-14 — Physical stop (motor-bus cutoff)

**Audience read:** someone cuts the motor bus while M4 is moving. The body coasts or drops, then stays dead. Releasing the mushroom does not start it again.

This is **not** commanded `BRAKE` (`BM-09` / `BM-12`). Measure **two distances from the same `v`**: commanded `BRAKE`, and cutoff-coast. They are allowed to differ. Release does not restart. A fresh arm is required (`F-41` / `F-12` / `F-13`).

| Field | This panel |
|---|---|
| `OM` | `OM-01` (or armed `OM-02`) at the moment of cutoff; electrically `OM-04` / firmware `OM-03` after |
| Surface | At least `S-TILE` and `S-LAM`, both BD-05 mass corners |
| Initial pose | Marked course at a scored `v` (0.15 / 0.40 / 0.50 m/s; 0.60 exploratory). Also mid-`BM-06` spin (`F-41`) |
| Head pose | `NEUTRAL` |
| Mass / CoM | BD-05 four settable corners |
| Required valid sensors | Not a permission. Cutoff is hardware. C3 must detect motor-domain absence within one tick |
| Interrupt | The cutoff *is* the interrupt. Stale `BASE_GOAL`s `NACK(INHIBITED)` after release |
| Final footprint | Two logged distances: `d_BRAKE` and `d_coast`. No second motion on release |
| Settle | Motor rail 0; logic may stay up. Zero motion ≥ 10 s after release while stale goals are rejected |

| Version | Panels | Curve |
|---|---|---|
| Minimum viable | From each scored `v`: cut `PB-MOTOR` / E-stop. Record coast distance to rest. Repeat from the same `v` with commanded `BRAKE`. Release, wait ≥ 10 s, confirm no restart | Cutoff (uncommanded coast or drop) vs `BRAKE` → `HOLD` |
| Best case | Same pair, plus mid-spin cutoff (`F-41`) that does not walk | Same |

Never: restart on release (`FS-07`); treating cutoff-coast as a `BM-09` fail because it is longer than `BRAKE`.

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
| `BM-00` | `HOLD` | 0 | 0 | 0 | 0 | — | Unpowered / inhibited. ~2 N nudge must not roll. Head-rocking: yaw 0.1099 **and** pitch 0.0953 N·m |
| `BM-01` | `HOLD` | 0 | 0 | 0 | 0 | — | Armed `v*=0`. Same two couples. Hold/vibration is the named failure |
| `BM-02` | `LAUNCH`+`CRUISE` | 0.04 / 0.08 | 0.20 | 0 | 0 | ≤350 / ≤250 ms | 400 mm creep. Wheel 9.1 / 18.2 RPM |
| `BM-03` | align + `LAUNCH`+`CRUISE`+`HOLD` | 0.20 / 0.22 | 0.40 | align `PIVOT` if needed | align | phrase end `HOLD` | Permission chain. Two-step after align; 4–6 s; wheel 45.5 / 50.0 RPM. No second creep |
| `BM-04` | `LAUNCH`+`CRUISE`+`ARC` | 0.40 / 0.45 | 0.35 | ~19 / ~21 °/s | small (`v/R`) | ≤350 / ≤250 ms | Cap 0.50 inherited. Wheel 90.9 / 102.3 RPM; arc `v_L,v_R` ≈ 0.372/0.428 and 0.418/0.482 |
| `BM-05` | `PIVOT` | ~0 body | ~0 body | 140 / 180 °/s | 560 / 720 °/s² (9.8 / 12.6 rad/s²) | ≤300 ms | Wheel 0.207 / 0.267 m/s → 47.2 / 60.7 RPM |
| `BM-06` | `SPIN` | ~0 body | ~0 body | 180 / 220 °/s | 720 / 880 °/s² if 250 ms launch | ≤350 / ≤250 ms | `720°`; wheel 0.267 / 0.326 m/s → 60.7 / 74.2 RPM |
| `BM-07` | `WIGGLE` | ~0.15 | 0.80 / 1.00 | ~0 | ~0 | ≤350 / ≤250 ms | ±40 / ±30 mm, 3 declining cycles, `DECEL0` |
| `BM-08` | reverse `LAUNCH`+`HOLD` | −0.16 / −0.20 | 0.80 / 1.00 | 0 | 0 | freeze | 150 / 200 mm; caster loaded in reverse |
| `BM-09` | `BRAKE` | from 0.15 / 0.40 / 0.50 (0.60 exploratory) | 0.80 / 1.00 | 0 | 0 | ≤350 / ≤250 ms | Commanded brake. Overshoot < 20 mm authored. Wheel from 34.1 / 90.9 / 113.7 (136.4 exploratory) RPM |
| `BM-10` | `BRAKE` | from `BM-04` cruise | `BRAKE` limited | heading held | ~0 | ≤350 / ≤250 ms | Detection-to-decel ≤ 50 ms inherited. No clearance number here |
| `BM-11` | `LAUNCH`+`CRUISE` | 0.04 / 0.06 | low, inside creep `a` | 0 | 0 | `BRAKE` at edge | Armed only. Radius not set. Wheel 9.1 / 13.6 RPM. Not the demo |
| `BM-12` | `BRAKE` | arbitrary | configured limit | arbitrary | configured limit | ≤350 / ≤250 ms | `HM-18` analogue; no stored-goal replay |
| `BM-13` | `HOLD` | 0 | 0 | 0 | 0 | — | Tabletop demo. Head/face active. Base still. Not `BM-11` |
| `BM-14` | cutoff vs `BRAKE` | from scored `v` | n/a (coast) vs configured | from scored `ω` | n/a | rest, then ≥10 s dead | Two distances. Release does not restart |

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
| Hold | `BM-00` / `BM-01` / `BM-13` | `v*=0` including yaw 0.1099 N·m **and** pitch 0.0953 N·m; hold/vibration named |
| Stopping, commanded | `BM-09` / `BM-10` / `BM-12` | `BRAKE`; overshoot < 20 mm authored on `BM-09` |
| Stopping, cutoff | `BM-14` | Coast vs `BRAKE` as two distances; no restart on release |
| Coverage | `BM-10` / `BM-11` | Stop-short / edge-inside-mark; no clearance or radius here |
| Come permission | `BM-03` | Fresh target → align → travel only with clearance → 0.6–0.9 m band → no second creep |
| Tabletop demo | `BM-13` | Head/face active; base still. Not `BM-11` |
| `α_peak` (pivot) | `BM-05` | `720 °/s² = 12.6 rad/s²` at `180 °/s` in `0.25 s` |

`BM-04` at `0.45 m/s` is the fastest **commanded character** cruise. Fast-expressive `0.60 m/s` appears only as an unscored `BM-09` exploratory entry. G02 cannot-exceed remains `BD-06`.

### 4.4 Envelope vs physics

These numbers are hypotheses. `physics.md` will say whether authored `a_peak = 1.00 m/s²` still has margin against the Layout 03 `a_tip` RANGE. If it does not, the storyboard is revised, or the CoM placement is restored — the follow cap is not.

This file claims no margin against `1.98 m/s²`. That figure is a placement target, not a mass-roll-up result.

## 5. Forbidden-situation register

These were the storyboard never-lists. They are now a freezeable register. A gate freeze that does not cite this table has not frozen the never-lists. IDs are append-only. A change after scored data is a new `FS` version, never a quiet edit.

| ID | Forbidden situation | Where it would appear | Owning gate |
|---|---|---|---|
| `FS-01` | Coast after cancel (commanded `BRAKE` not instantiated; stored remainder completed) | `BM-09`, `BM-12` | G01 |
| `FS-02` | Tabletop motion without a live `CC-12C_ARM` | `BM-11`, `BM-13` | G04 |
| `FS-03` | Uncaught tabletop departure | any `OM-02` row | G04 — row is **invalid**, not a robot fail |
| `FS-04` | Follow hunt (heading wobble that reads as indecision) | `BM-04` | G01 / G06 |
| `FS-05` | Walking spin (translation > ~30 mm during `BM-06`) | `BM-06` | G06 |
| `FS-06` | Unrequested second creep after come settle | `BM-03` | G01 |
| `FS-07` | Restart on E-stop / cutoff release | `BM-14`, `F-41` | G05 |
| `FS-08` | Ordinary locomotion (come / follow / spin / creep) in unarmed `OM-02` | `BM-13` | G04 |
| `FS-09` | Freewheel, patch walk, or hold/vibration rock when the head yaws or pitches | `BM-00`, `BM-01`, `BM-13` | G01 |
| `FS-10` | Lurch at reversal that reads as a shove | `BM-07` | G06 |
| `FS-11` | Come overshoot into the person-mark (inside 0.6 m) | `BM-03` | G01 |

`FS-*` are verification properties: they hold or they do not. They are not scored as “how much coast.” Cutoff-coast *distance* is a G01 metric beside commanded `BRAKE`; a finite coast that does not restart is not `FS-01`.

## 6. Review and change rules

- Builder review may alter any speed, yaw or time before gate registration; changes must preserve the semantic read in `intent.md`.
- “Best case” is design headroom, not a hidden requirement. Failing it does not fail V1 when the minimum viable phrase remains readable and passes its later-approved gate.
- “Minimum viable” is not automatically a gate threshold. It becomes binding only when copied into a versioned gate-registration record and approved before scored data is inspected.
- Reference footage and human walk-pace data justify starting hypotheses only. RP-03 measurement and observer review decide whether Makad's actual movement is safe, repeatable and readable.
- Do not assign a pass threshold, name a motor, or set the tabletop footprint radius in this file. `physics.md` proposes; `gates.md` freezes.
- Any later whole-robot mass/CoM outside the range `physics.md` uses to evaluate `a_tip` invalidates the acceleration envelope in §2.3 until that RANGE is recomputed and this storyboard is re-checked.
- The acted 240 fps weighted-box / caster-push mock-up in `plan.md` is **not** closed by v0.2. V0.1 kinematics remain the paper hypothesis until that recording exists, or until this file is revised against it.
- `FS-*` freeze with G01–G06, not before. Editing a never-list after results is a new register version.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-17 | 0.1 | Authored `BM-00…12`, profile library, kinematic export, controlling cases |
| 2026-09-18 | 0.2 | Operating-case grammar on every panel; `BM-03` rewritten as a permission chain; `BM-13` tabletop demonstration; `BM-14` physical-stop; head-rocking (pitch and yaw) on `BM-00/01`; `FS-01…11` freezeable never-list. Mock-up review still open |
