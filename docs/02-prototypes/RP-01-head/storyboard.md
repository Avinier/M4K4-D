# RP-01 Head Motion Storyboard

| Field | Value |
|---|---|
| Status | Provisional authored kinematics v0.2 — per-motion profiles assigned; design hypotheses, not registered gate thresholds |
| Owner | Project builder |
| Last updated | 2026-08-31 |
| Semantic source | `intent.md` |
| Load baseline | `material-finish-mass-decision.md`: approximately 490 g at 1.2 mm PLA is a pre-M008 lower bound; add required C2 hardware. Old 250 g / preliminary inertia and torque assumptions are invalid for feasibility sizing |
| Feeds | `physics.md`, `gates.md`, mechanism concept comparison and later motion firmware |

## 1. How to read this storyboard

This document translates the accepted character vocabulary in `intent.md` into poses, keyframes, angles and timing that a mechanism can be designed against. It deliberately starts each move with what the audience should read; numbers describe that performance rather than replace it.

The numbers are **authored targets** chosen from Makad's intended character, human head-gesture research and practical droid-performance references. They are not yet pass/fail thresholds. They must be reviewed by the builder, exercised in simulation or an acted mock-up, checked against the revised approximately 490 g pre-M008 lower bound **plus C2 hardware** and eventual per-axis mass tree, and frozen in `gates.md` before scored RP-01 runs. The kinematic targets remain authored intent; actuator feasibility, torque, current, thermal load and settling must be recomputed from the new mass/CoM/inertia evidence rather than inherited from the old 250 g baseline.

### Coordinate convention

All angles are robot-relative Euler-angle commands from the calibrated attentive pose:

| Axis | Zero | Negative | Positive |
|---|---|---|---|
| Pitch `P` | Face level/attentive | Chin/head up | Chin/head down |
| Yaw `Y` | Face forward | Turn toward robot-left | Turn toward robot-right |
| Roll `R` | Head level | Robot-left side rises | Robot-left side lowers |

`P0 Y0 R0` is neutral. A keyframe such as `P+18 Y0 R0` means 18° down from neutral. Direction signs are a documentation convention; firmware signs may differ but must expose this convention at its interface.

### Curve language

| Code | Shape | Character use |
|---|---|---|
| `SMOOTH` | Symmetric jerk-limited/minimum-jerk-like ease-in/ease-out | Sleep, sadness, search, affection |
| `SHARP→SOFT` | Fast readable stroke followed by a longer ease and settle | Wake, yes/no, startle, anger |
| `PULSE` | Small deliberately grouped reversals with unequal spacing/amplitude | Laugh |
| `WAVE` | Continuous rounded alternation; no hard corner at reversal | Indian head wobble |
| `TRACK` | Low-amplitude target-following correction with velocity/acceleration limiting | Person tracking |
| `HOLD` | Intentional stillness; no compulsory idle oscillation | Attention, curiosity, fear assessment, sadness |

Repeated gestures must not be equal-amplitude sine waves. Conversational nod research finds structure: the first cycle carries the greatest statement, later cycles decline, and the final cycle is especially small. The storyboards use that pattern so yes/no/laugh read as phrased actions rather than motor tests.

## 2. Design envelopes

Pitch and yaw are the two dominant expressive axes and are expected to carry roughly 80–90% of authored head activity. Roll is lower-duty and lower-range, but remains a powered Core axis and must support both slow holds and the medium-fast Indian head wobble. “Minimum viable” therefore means a credible **three-axis** expressive envelope, not a two-axis fallback.

### 2.1 Authored pose envelope

| Axis | Minimum viable authored envelope | Best-case authored envelope | Why |
|---|---:|---:|---|
| Pitch | `-12° … +28°` | `-18° … +35°` | Startle/upward attention through sleep/downward emotion |
| Yaw | `±35°` | `±50°` | Person search and attention without using base motion for every glance |
| Roll | `±10°` | `±14°` | Curious holds and a readable head wobble without dominating gaze |

### 2.2 Proposed usable mechanism travel

The mechanism needs clearance beyond the authored pose envelope so normal trajectories never use hard stops as motion limits.

| Axis | Minimum viable usable travel | Best-case usable travel | Design margin over authored pose |
|---|---:|---:|---:|
| Pitch | `-15° … +32°` | `-22° … +40°` | 3–5° each end |
| Yaw | `±40°` | `±55°` | 5° each end |
| Roll | `±12°` | `±18°` | 2–4° each end |

These are provisional **usable** ranges. Mechanical hard stops, cable limits and forbidden regions must sit beyond them with separately calculated margin.

### 2.3 Motion-quality envelope

| Class | Minimum viable | Best-case target |
|---|---|---|
| Slow smooth | 1.5–3.0 s complete phrase, no visible steps | Stable jerk-limited movement with nearly silent settle |
| Conversational | 0.6–1.2 s complete phrase | Clear initial stroke plus readable hold/settle |
| Fast sharp pitch/yaw | Primary statement within 250–350 ms; phrase within 1.0 s | Primary statement within 150–250 ms; phrase within 0.8–1.0 s |
| Roll wobble | `±8°`, rounded reversals, 1.0–1.3 s | `±12°`, rounded declining reversals, optional small yaw coupling, 0.9–1.2 s |
| Micro-motion | Intentional `≥4°`, 2 grouped pulses in 0.80 s | Intentional `2–5°`, 3 grouped pulses in a 0.68 s active window with low loaded hysteresis and no hold hunting |
| Controlled cancellation | No new expressive keyframe after cancellation; settle proposal ≤500 ms | Settle proposal ≤300 ms where the validated load permits |

“Fast sharp” never means a step command or maximum servo speed. It means a shaped stroke whose onset is legible, whose peak acceleration is bounded, and whose exit is slower than its entrance.

### 2.4 Candidate mechanical-quality requirements

These values are design inputs, not registered gates:

| Property at the head output | Minimum viable | Best-case target | Why |
|---|---:|---:|---|
| Complete-output loaded reversal hysteresis | `≤0.50°` | `≤0.25°` | A 2° tracking correction and the laugh's 2° reverse excursion must remain visibly intentional after gearbox lash, joints/linkages, compliance and closed-loop control behaviour |
| First loaded yaw/roll structural mode `f₁` | `≥25 Hz` screening target | `≥30 Hz` target | Separates these axes' first loaded modes from their authored reversal content and reduces visible ring-down risk |
| First loaded pitch structural mode `f₁` | `≥30 Hz` for the minimum-viable laugh | `≥40 Hz` for the unshaped best-case laugh | The best laugh contains a 100 ms pitch reversal, with characteristic content around 10 Hz and useful higher-frequency content |

Loaded hysteresis is measured at the head output under representative reversing load, in both sweep directions and on every axis; hold hunting is measured during a separate fixed-command dwell. An actuator's gear material, protocol or internal position readback is not proof of complete-output behaviour. The `f₁` targets are CAD/bench screening targets, not mathematical guarantees of 300 ms settling: damping, controller bandwidth and trajectory shaping must also be measured. A pitch result between 30 and 40 Hz does not automatically reject the mechanism, but the best-case laugh then requires validated input shaping or a slower trajectory whose speed/acceleration is re-derived and registered. Use an impact/tap test with an accelerometer, IMU or correlated acoustic measurement before control tuning, then confirm with commanded motion.

### 2.5 Candidate loaded-hysteresis and hold-hunting test

This is the runnable draft method to convert the output budget into evidence after `τ_peak,op` is available from the mass/CoM analysis:

1. Energize the complete head/neck assembly at a fixed mid-range command under representative head mass. Test neutral and the axis's worst registered off-neutral load pose.
2. Attach a rigid lever or use a rigid head feature at a measured radius `r = 50.0 mm` from the tested axis. Put a dial indicator tangent to the arc at the **head output**, not at the servo horn.
3. Apply a slow stepped triangular output-load cycle `+0.50·τ_peak,op → -0.50·τ_peak,op → +0.50·τ_peak,op` using a bidirectional calibrated force gauge and lever arm. Use the same registered load steps in both directions, allow each reading to settle and avoid exciting structural modes.
4. Precondition with 10 complete load cycles, then record 5 complete measured cycles per axis and pose. At every step log applied torque, independent tangential displacement, commanded position, servo-reported position, current and monotonic time.
5. Convert independent displacement to output angle with `θ_ext = x/r`. At each matched torque, calculate the separation between the increasing- and decreasing-load branches. Report the maximum branch separation, the settled command error at each endpoint and the time to re-settle after load reversal; do not substitute the positive-to-negative compliance span for hysteresis.
6. Candidate acceptance for maximum branch separation is `≤0.50°` minimum viable and `≤0.25°` best-case. At `r=50 mm`, those angular limits correspond to branch separations of `0.436 mm` and `0.218 mm`.
7. After the sweep, dwell at neutral and the registered gravity/preload holds without touching the rig. Record external-angle and current peak-to-peak/RMS behaviour plus any audible chatter. Freeze the dwell duration and hunting thresholds before scored testing.

The measurement intentionally includes gearbox backlash, servo control behaviour, horn/spline fit, screw-joint slip, linkage motion and printed/structural compliance across the complete transmission path. A servo-shaft or horn-only measurement is not admissible. Servo position readback is logged for correlation, but a 12-bit/revolution encoder is not the primary accept/reject instrument for the 0.25° target.

## 3. Storyboard panels

Times are measured from the start of the head phrase. `L` and `R` below are named yaw/roll directions rather than value signs where that is more readable. Eye/audio cues remain in `intent.md`; they do not change these head requirements.

### HM-00 — Powered-off rest

**Audience read:** M4 is off, physically quiet and safe—not actively frozen in an artificial pose.

| Version | Panels |
|---|---|
| Minimum viable | Motor power removed → mechanism remains supported or moves passively only within its validated safe-rest path → no cable pull or hard-stop impact. |
| Best case | Balanced/self-supported head remains near a visually acceptable rest pose without holding current, buzz or droop. |

This is a mechanical outcome, not an animated trajectory.

### HM-01 — Neutral attentive

**Audience read:** M4 is calmly available and looking forward; stillness feels intentional rather than dead.

`K0 HOLD: P0 Y0 R0`

No compulsory head loop is specified. Tracking and future eye animation may create aliveness; idle head motion must earn its place separately.

### HM-02 — Sleep

**Audience read:** attention gently drains away; the head tips forward into rest with a long, quiet ending.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 P0 Y0 R0` → `t3000 P+28 Y0 R0 HOLD` | One `MS7` segment; progressively slower final third |
| Best case | `t0 P0 Y0 R0` → `t2400 P+35 R+4 HOLD` | One coupled-axis `MS7` segment; very small asymmetry prevents a dead hinge-like look |

Interruption reverses smoothly from the current pose into wake or neutral; it does not jump to a stored angle.

### HM-03 — Wake rise

**Audience read:** M4 becomes alert quickly, rising with intention and finishing with a small living settle—not snapping upright like a switch.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | Start near `P+28` → `t700 P+4` → `t1000 P0 HOLD` | Fast middle, eased final 30% |
| Best case | Start near `P+35 R+4` → `t550 P+3 R+1` → `t700 P-3 R0` → `t850 P0 HOLD` | `SHARP→SOFT`; small upward overshoot then settle |

Wake completes within one second. If no person track exists, `HM-04` begins as a separate phrase after the awake state is reached.

### HM-04 — Search sweep

**Audience read:** M4 checks plausible directions, pausing to inspect rather than rotating continuously like a radar dish.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 Y0` → `t650 YL35 HOLD 200` → `t1650 YR35 HOLD 200` → `t2500 Y0` if unresolved | `SMOOTH`, sector pauses |
| Best case | `t0 Y0` → `t650 YL50 HOLD 200` → `t1900 YR50 HOLD 200` → `t2700 Y0` if unresolved | `SMOOTH`; optional `P±4` sector variation after perception geometry is known |

Acquisition interrupts the sweep immediately and blends into `HM-05`; it never completes stale search panels after finding the person.

### HM-05 — Acquire and track

**Audience read:** the first turn says “there you are”; subsequent corrections disappear into sustained attention.

| Version | Acquisition | Tracking correction |
|---|---|---|
| Minimum viable | Current pose → target yaw/pitch in 450–700 ms, then hold | 4° correction in 250–500 ms; no correction smaller than the proven reversal capability |
| Best case | Current pose → target yaw/pitch in 300–550 ms with soft settle | Intentional 2–4° correction in 180–400 ms; target noise filtered so the head does not chatter |

Tracking uses `TRACK`, not repeated point-to-point steps. Person loss freezes the last safe attention pose briefly, then hands control to search/loss behaviour.

### HM-06 — Yes

**Audience read:** the head tips decisively toward the person, rebounds, and settles. More emphatic agreement adds a second smaller cycle rather than repeating identical nods.

#### Soft yes

`t0 P0 → t250 P+12 → t480 P-5 → t700 P0 HOLD`

#### Emphatic yes — minimum viable

Exactly **two cycles** over 1.00 s: `t0 P0 → t205 P+14 → t451 P-6 → t677 P+11 → t890 P-4 → t1000 P0 HOLD`.

#### Emphatic yes — best case

Exactly **two cycles** over 0.90 s: `t0 P0 → t183 P+18 → t403 P-8 → t610 P+15 → t803 P-5 → t900 P0 HOLD`.

Curve: accented point-to-point minimum-jerk strokes. The downward statement leads. Best-case forward peaks decay `18° → 15°` (`0.83×`) and rebound peaks decay `8° → 5°` (`0.63×`). Segment durations are allocated approximately in proportion to `√Δθ`, keeping peak acceleration nearly uniform while preserving the complete 0.90 s phrase. The final move to neutral completes cycle two; it is not a third cycle.

### HM-07 — No

**Audience read:** a clear left-right refusal, strongest on the first full sweep and progressively smaller as the statement resolves.

#### Soft no

`t0 Y0 → t200 YL15 → t450 YR12 → t700 Y0 HOLD`

#### Emphatic no — minimum viable

Exactly **two cycles** over 1.00 s: `t0 Y0 → t180 YL16 → t434 YR16 → t672 YL12 → t873 YR8 → t1000 Y0 HOLD`.

#### Emphatic no — best case

Exactly **two cycles** over 0.95 s: `t0 Y0 → t165 YL22 → t398 YR22 → t620 YL18 → t819 YR14 → t950 Y0 HOLD`.

Curve: stitched minimum-jerk reversals. Best-case extrema use the explicit envelope `22°, 22°, 18°, 14°`, normalized as `1.00, 1.00, 0.82, 0.64`; nominal second-cycle amplitude is `0.73×` the first. Segment durations are allocated approximately in proportion to `√Δθ`, keeping peak acceleration near 82 rad/s² across launch, reversals and settle. This makes No more abrupt and energetic than Yes without introducing an acceleration discontinuity. The final return to neutral completes cycle two.

### HM-08 — Laugh

**Audience read:** several small forward chuckles arrive in irregular groups; the motion feels like laughter, not backlash or servo chatter.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 P0` → `t150 P+4` → `t280 P-1` → `t430 P+4` → `t580 P-1` → `t800 P0` | Two clear `PULSE` groups |
| Best case | `t0 P0` → `t110 P+5` → `t210 P-2` → `t330 P+6` → `t440 P-2` → `t570 P+4` → `t680 P0` → `t850 HOLD` | Exactly three unequal forward pulses during a 680 ms active window, followed by a 170 ms terminal hold/settle; 850 ms complete phrase |

This is the smallest-move and fast-reversal design case. The largest local acceleration case is currently the 7° reversal from `P+5°` to `P-2°` in 100 ms. High-frequency buzzing above the authored pulse rhythm is a failure, not extra expressiveness.

### HM-09 — Indian head wobble

**Audience read:** friendly acknowledgement through a continuous, fluid side-to-side tilt—neither the vertical “yes” nod nor the horizontal “no” shake.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 R0` → `t207 RL8` → `t499 RR8` → `t773 RL6` → `t1004 RR4` → `t1150 R0` | Stitched minimum-jerk roll wave; rounded declining reversals |
| Best case | `t0 R0` → `t189 RL12` → `t456 RR12` → `t711 RL10` → `t936 RR7` → `t1080 R0` | Same roll-dominant minimum-jerk wave; optional `Y±3°` approximately quarter-cycle out of phase to suggest a subtle horizontal figure-eight |

The optional yaw coupling is not part of the minimum mechanism requirement until observer comparison shows that it improves readability.

### HM-10 — Curious tilt

**Audience read:** the head tilts toward the subject, lifts slightly, and then becomes still—as if M4 is inspecting or thinking.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 P0 R0` → `t650 P-2 R+8 HOLD 600–1200` | Smooth entrance, long still hold |
| Best case | `t0 P0 R0` → `t450 P-4 R+12 HOLD 700–1500` | One `MS7` segment; faster first read with a very soft arrival |

Return to neutral takes 500–700 ms unless another semantic gesture begins from the tilted pose.

### HM-11A — Curious yes

**Audience read:** M4 keeps the curious tilt while agreeing; the nod occurs inside the tilted frame rather than erasing the emotion first.

| Version | Relative keyframes from curious hold |
|---|---|
| Minimum viable | Hold `R+8°` throughout: `t0 P-2° → t220 P+10° → t500 P-5° → t850 P-2°` |
| Best case | Hold `R+12°` throughout: `t0 P-4° → t180 P+12° → t400 P-7° → t620 P+8° → t900 P-4°` |

### HM-11B — Curious no

**Audience read:** M4 retains the tilted question while declining; the result must not collapse into a diagonal wobble.

| Version | Relative keyframes from curious hold |
|---|---|
| Minimum viable | Hold `R+8° P-2°`: `t0 Y0° → t200 YL13° → t500 YR13° → t850 Y0°` |
| Best case | Hold `R+12° P-4°`: `t0 Y0° → t180 YL18° → t430 YR18° → t680 YL12° → t950 Y0°` |

Both compound moves are cross-axis load, clearance and control cases for RP-01.

### HM-12 — Happy/excited

**Audience read:** a quick upward lift and small asymmetric flourish, then a buoyant hold; energetic but not a startle.

| Version | Keyframes |
|---|---|
| Minimum viable | `t0 P0 R0` → `t400 P-6 R+4` → `t650 P-3 R+2 HOLD` → optional return by `t900` |
| Best case | `t0 P0 R0` → `t280 P-10 R+6` → `t480 P-5 R-3` → `t700 P-3 R+2 HOLD` |

### HM-13 — Angry/irritated

**Audience read:** the head drives slightly forward/down, becomes very still, and delivers one restrained sharp correction. Tension comes from compression and timing, not frantic speed.

| Version | Keyframes |
|---|---|
| Minimum viable | `t0 P0` → `t400 P+7 HOLD 500` → return over 500 ms |
| Best case | `t0 P0` → `t250 P+10 HOLD 350` → one `Y±6°` correction over 220 ms → return/hold by `t950` |

The yaw correction is optional. It must not become a “no” phrase unless rejection is the intended meaning.

### HM-14 — Sad

**Audience read:** the head loses energy and droops slowly, ending asymmetrically and remaining there without restless motion.

| Version | Keyframes |
|---|---|
| Minimum viable | `t0 P0 R0` → `t2200 P+16 R+3 HOLD` as one `MS7` segment |
| Best case | `t0 P0 R0` → `t1800 P+22 R+4 HOLD` as one `MS7` segment |

Curve: `SMOOTH`, with silence/stillness after arrival. Recovery should be authored separately; sadness does not automatically bounce back.

### HM-15 — Fear/startle

**Audience read:** an immediate recoil away from a frontal stimulus, a frozen assessment, then a controlled recovery. The freeze is as important as the speed.

| Version | Keyframes | Curve |
|---|---|---|
| Minimum viable | `t0 P0 Y0 R0` → **250 ms outbound only** to `t250 P-10 Y±5 R±4` → hold until `t500` → recover by `t1200` | Sharp outbound stroke, hard perceptual hold, soft recovery |
| Best case | `t0 P0 Y0 R0` → **180 ms outbound only** to `t180 P-15 Y±8 R±6` → hold until `t430` → `t700 P-5 Y±3 R±2` → `t1000 P0 Y0 R0` | `SHARP→SOFT`; away-direction chosen from stimulus |

The 180 ms value never means out-and-return. Best-case recovery occupies 570 ms after the hold and is deliberately slower. Startle is the sharp multi-axis recoil case; it is not automatically the largest single-axis acceleration case.

### HM-16 — Confused/uncertain

**Audience read:** M4 starts to choose an interpretation, reverses, and holds unresolved. It must not read as categorical no.

| Version | Keyframes |
|---|---|
| Minimum viable | `t0 R0 P0` → `t500 R+6 P+2 HOLD 200` → `t1100 R-5 P+2 HOLD` → `t1800 R0 P0` |
| Best case | `t0 R0 P0` → `t400 R+8 P+3 HOLD 180` → `t1050 R-7 P+3 HOLD 220` → `t1600 R+4` → `t1900 R0 P0` |

### HM-17 — Affection/warm attention

**Audience read:** a small gentle lean toward the person followed by a comfortable unhurried hold.

| Version | Keyframes |
|---|---|
| Minimum viable | `t0 P0 R0` → `t850 P-2 R+5 HOLD 800–1500` |
| Best case | `t0 P0 R0` → `t650 P-3 R+8 HOLD 1000–2000` |

Curve: `SMOOTH`. The exit is at least 600 ms unless interrupted by a higher-priority intent.

### HM-18 — Controlled cancel and safe settle

**Audience read:** the current expression stops cleanly without completing stale beats or producing a violent jerk.

| Version | Panels |
|---|---|
| Minimum viable proposal | Cancellation accepted → no later authored keyframe begins → jerk/acceleration-limited deceleration → zero intentional velocity within 500 ms where physically safe → nearest valid hold. |
| Best-case proposal | Same sequence with zero intentional velocity within 300 ms where the validated load and current pose permit. |

These are storyboard proposals, not RP01-G01 thresholds. Emergency motor-power removal, feedback loss and controller failure have different physical behavior and must be registered separately after the mechanism is known.

## 4. Motion-profile assignments and kinematic export

### 4.1 Normalized profile library

For a rest-to-rest segment of displacement `Δθ`, duration `T` and normalized time `s=t/T`:

- `ω_peak = Cᵥ·Δθ/T`
- `α_peak = Cₐ·Δθ/T²`
- `j_peak = Cⱼ·Δθ/T³`

`k` in the earlier reviews is `Cₐ`. It is derived from the profile equation, not authored independently.

| Code | Normalized displacement `q(s)` | `Cᵥ` | `Cₐ = k` | `Cⱼ` | Endpoint/connection behavior |
|---|---|---:|---:|---:|---|
| `HOLD` | constant | 0 | 0 | 0 | No intentional motion |
| `MJ5` | `10s³-15s⁴+6s⁵` | 1.8750 | 5.7735 | 60.000 | Zero velocity and acceleration at both ends; finite nonzero endpoint jerk |
| `MS7` | `35s⁴-84s⁵+70s⁶-20s⁷` | 2.1875 | 7.5132 | 52.500 | Zero velocity, acceleration and jerk at both ends; higher mid-stroke speed/acceleration |
| `HC` | `(1-cos(πs))/2` | 1.5708 | 4.9348 | 15.503 | Reference candidate only; not assigned in V0.2 because a rest launch/settle needs a separately matched boundary law |
| `TRACK` | online jerk/acceleration-limited target filter | — | — | configured limit | Target can change during motion; no single rest-to-rest coefficient |
| `BRAKE` | online jerk-limited deceleration from current state | — | — | configured limit | Initial position, velocity and acceleration vary; no single `Δθ/T` coefficient |

`MS7` is used only where silent, exceptionally soft entry/exit matters more than peak acceleration. `HC` was evaluated for No and Wobble but rejected for V0.2: joining it to an `MJ5` launch would step acceleration at the first extremum, while beginning a pure sinusoid at neutral would require nonzero initial velocity. Stitched `MJ5` segments keep position, velocity and acceleration continuous at every authored reversal.

### 4.2 Per-motion authored profile ledger

| ID | Movement profile | `Cₐ = k` used | Why this motion law matches the performance |
|---|---|---:|---|
| `HM-00` | Passive/uncommanded rest | — | Power-off behavior is determined by balance, friction, brakes/stops and gravity, not a commanded trajectory |
| `HM-01` | `HOLD` | 0 | Attention is deliberate stillness; tracking is a separate state |
| `HM-02` | `MS7` sleep descent | 7.5132 | Zero velocity/acceleration/jerk at departure and rest suppresses a visible or audible final twitch during the long 2–3 s bow |
| `HM-03` | `MS7` primary wake rise + `MJ5` overshoot/settle | 7.5132 / 5.7735 | The main rise is clean and quiet; the small overshoot is a separate living punctuation rather than ringing |
| `HM-04` | `MJ5` sector-to-sector search turns + `HOLD` inspections | 5.7735 / 0 | Each direction is an intentional target acquisition with a complete pose and pause, not a scanner sine wave |
| `HM-05` | `TRACK` online filter; `MJ5` only as the registered 2° correction test proxy | — / 5.7735 proxy | Perception targets move and can be replaced mid-correction, so a fixed offline `k` would be dishonest |
| `HM-06` | Accented `MJ5` extrema-to-extrema nod strokes | 5.7735 per segment | Yes is phrased as two decisive downward statements with softer, smaller rebounds; segment timing—not a different equation—creates the accent |
| `HM-07` | Declining stitched `MJ5` reversal sequence | 5.7735 per segment | No remains a continuous lateral refusal, but its large, faster reversals create more energy than Yes without a hybrid-profile acceleration step |
| `HM-08` | Irregular `MJ5` pulse train | 5.7735 per segment | Laugh is a sequence of discrete chuckles with unequal spacing/amplitude, not a stationary-frequency oscillator |
| `HM-09` | Declining stitched `MJ5` roll wave; optional phase-shifted yaw | 5.7735 per segment | The cultural gesture remains even, continuous and rounded while every reversal is rest-to-rest and C²-continuous; a pure-roll minimum remains valid |
| `HM-10` | `MS7` curious tilt into `HOLD` | 7.5132 / 0 | Curiosity is read from a gentle establishment followed by processing stillness |
| `HM-11A` | `HM-06`-style `MJ5` nod strokes in a held roll frame | 5.7735 | Retains the authored yes rhythm while exposing combined-axis load |
| `HM-11B` | Stitched `MJ5` yaw reversals in a held roll frame | 5.7735 | Retains No's profile family without erasing the curious tilt |
| `HM-12` | `MJ5` multi-pose flourish + `HOLD` | 5.7735 / 0 | Happiness uses clear pose changes and an asymmetric flourish rather than sustained vibration |
| `HM-13` | Fast `MJ5` compression/correction + long `HOLD` | 5.7735 / 0 | Anger comes from a controlled strike and sustained tension; discontinuous commands would read as a control fault |
| `HM-14` | `MS7` droop into `HOLD` | 7.5132 / 0 | Sadness must lose energy continuously and arrive without bounce or endpoint jerk |
| `HM-15` | Single outbound `MJ5` recoil → `HOLD` freeze → slower `MJ5` recovery | 5.7735 / 0 / 5.7735 | Startle is one fast rest-to-rest escape stroke, not an oscillation; the freeze carries the perception |
| `HM-16` | Alternating `MJ5` tilt decisions separated by `HOLD`s | 5.7735 / 0 | Confusion is a sequence of tentative choices; its revised timing prevents the small third tilt from becoming the roll acceleration case |
| `HM-17` | `MS7` affectionate lean into `HOLD` | 7.5132 / 0 | Warmth benefits from the softest boundary conditions and a long comfortable still pose |
| `HM-18` | `BRAKE` from measured current state | — | Cancellation must respect current velocity/acceleration and configured limits; a rest-to-rest `k` cannot describe it |

These are authored V0.2 laws. Observer review can change a motion's profile, but that change also changes its coefficients and invalidates its previous kinematic/torque calculation.

### 4.3 Current per-axis controlling cases

Every launch, interior reversal and settle was evaluated. The old 110–120 ms Yes/No launches were removed because they—not the advertised peak-to-peak reversals—would have controlled acceleration.

| Axis | Requirement | Current controlling authored segment/profile | Current value |
|---|---|---|---:|
| Pitch | Peak speed | Yes, 26° in 0.220 s, `MJ5` | `222°/s` |
| Pitch | Peak acceleration | Laugh, 7° in 0.100 s, `MJ5` | `4,041°/s² = 70.5 rad/s²` |
| Yaw | Peak speed | No, 44° in 0.233 s, `MJ5` | `354°/s` |
| Yaw | Peak acceleration | No settle, 14° in 0.131 s, `MJ5`; all phrase segments are within 1% | `4,710°/s² = 82.2 rad/s²` |
| Roll | Peak speed | Wobble, 24° in 0.267 s, `MJ5` | `169°/s` |
| Roll | Peak acceleration | Wobble, 22° in 0.255 s, `MJ5`; all phrase segments are within 1% | `1,953°/s² = 34.1 rad/s²` |

Startle remains the simultaneous three-axis case: pitch `46.7 rad/s²`, yaw `24.9 rad/s²`, roll `18.7 rad/s²`. It does not control any individual axis under the current keyframes.

### 4.4 Rapid-expression profile-freedom envelope

Authored animation and mechanism sizing are separate. RP-01 provisionally permits later rapid-expression profiles up to `Cᵥ=2.0` and `Cₐ=2π=6.2832` without repeating actuator selection. This is a declared cycloidal-class envelope, not a claim that every S-curve lies below it. A later profile exceeding either coefficient, or shortening a segment, invalidates the corresponding axis sizing.

| Axis | Envelope-driving geometry/timing | `ω_peak` at `Cᵥ=2.0` | `α_peak` at `Cₐ=2π` |
|---|---|---:|---:|
| Pitch | Yes speed segment 26°/0.220 s; Laugh acceleration segment 7°/0.100 s | `236°/s` | `4,398°/s² = 76.8 rad/s²` |
| Yaw | Speed: 44°/0.233 s; acceleration: 14°/0.131 s | `378°/s` | `5,126°/s² = 89.5 rad/s²` |
| Roll | Speed: 24°/0.267 s; acceleration: 22°/0.255 s | `180°/s` | `2,126°/s² = 37.1 rad/s²` |

Slow `MS7` gestures have `Cᵥ=2.1875` and `Cₐ=7.5132`, but their much longer segment times are evaluated directly and remain below the rapid cases. The envelope is not a substitute for torque margin, RMS/thermal analysis, gravity load or the exported firmware trajectory.

## 5. Research rationale

- [Structure of nods in conversation](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0323448) — repeated nods have structured, declining cycle magnitudes rather than identical repetition.
- [Phonetic differences between affirmative and feedback nods](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0304040) — affirmative nods tend to be faster and larger than feedback nods; reported conversational nod durations vary substantially.
- [Kinematics and kinetics of vigorous head shaking](https://journals.humankinetics.com/view/journals/jab/31/3/article-p170.xml) — unconstrained vigorous human shaking spans roughly 20–91° total range and 1.9–4.7 Hz; Makad targets the lower/middle portion rather than copying human extremes.
- [Motion-capture profiles of shakes, nods and tilts](https://publications.rwth-aachen.de/record/571764) and [kinematic annotation of spontaneous head gestures](https://clp.ling.uni-potsdam.de/publications/Kousidis-2013-2.pdf) — natural gestures differ by axis, cyclicity, direction and connected sequencing; “oscillatory” is not one sufficient trajectory class.
- [BBC description of the Indian head wobble](https://www.bbc.com/travel/article/20180722-cracking-indias-mystifying-nod-code) — the gesture is continuous side-to-side tilt, smooth rather than firm/jerky, sometimes described as a horizontal figure-eight.
- [Analysis and generation of laughter motion in an android](https://www.cambridge.org/core/journals/apsipa-transactions-on-signal-and-information-processing/article/analysis-and-generation-of-laughter-motions-and-evaluation-in-an-android-robot/353D071416BDE0536FDB4E5B86696175) — laughter head motion benefits from its own timing model rather than a generic nod loop, and multimodal timing affects perceived naturalness.
- [Robot head-movement timing study](https://link.springer.com/article/10.1007/s12369-024-01196-0) — even minimal nod, shake and tilt movements materially affect perception; movement timing relative to communication changes naturalness.
- [Victor Navone on animating WALL-E](https://animatedviews.com/2008/wall-e-victor-navone-on-wall-e-and-cars-toon/) and [Angus MacLane on limited robot acting](https://variety.com/2008/digital/news/how-to-build-a-better-robot-1117987668/) — pose transition, timing, restraint and physiology-specific motion carry character.
- [BB-8 practical-effects interview](https://www.popsci.com/qa-how-to-create-robot-icon/) and [puppeteer movement-vocabulary interview](https://www.starwars.com/news/bb-8-and-porg-puppeteer-brian-herring-on-his-journey-to-the-last-jedi) — head pitch/lean changes perceived intent, while many fast/slow variants were physically tried before consistent character timing was selected.
- [Comparison of robotic motion laws](https://www.mdpi.com/2076-3417/13/9/5601) — velocity, acceleration and jerk coefficients belong to a named normalized law; trapezoidal, cycloidal and jerk-shaped profiles trade peak effort against derivative continuity and vibration.

## 6. Review and change rules

- Builder review may alter any angle or time before gate registration; changes must preserve the semantic read in `intent.md`.
- “Best case” is design headroom, not a hidden requirement. Failing it does not fail V1 when the minimum viable three-axis phrase remains readable and passes its later-approved gate.
- “Minimum viable” is not automatically a gate threshold. It becomes binding only when copied into a versioned gate-registration record and approved before scored data is inspected.
- Reference footage and human data justify starting hypotheses only. RP-01 measurement and observer review decide whether Makad's actual movement is safe, repeatable and readable.
- Any later head mass/CoM outside the RP-01 validated load envelope invalidates these mechanism conclusions and triggers representative-load retesting.
