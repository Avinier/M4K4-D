Yes. This critique catches several genuine problems in v2.0. I would incorporate almost all of it.

There are **two places where I’d modify the critique rather than copy it literally**. First, adding bearings/a proper external load path does *not automatically* invalidate the actuator’s internal encoder; the problem arises when there is a belt, extra gear stage, linkage, compliant coupling, or other lost motion **downstream of that encoder**. Second, smart bus servos do not universally publish true continuous torque ratings. For example, ROBOTIS explicitly distinguishes stall from continuous output and recommends roughly 20% of stall torque as a general selection region for many DYNAMIXELs; Feetech’s STS3215 publishes stall torque plus telemetry but not necessarily a continuous torque rating. ([ROBOTIS e-Manual][1])

So the spec should handle both cases rather than silently mandate one brand/family.

# MAKAD — SPEC-02 v2.1

## Natural, Expressive Head Movement & Gaze System

**Status:** Revised working specification
**Supersedes:** SPEC-02 v2.0

All unaffected v2.0 requirements remain, but the following sections **replace or extend** their corresponding clauses.

---

# 1. Fundamental Neck Architecture

## C2-R01 — Three-axis intended architecture — MUST-HAVE DESIGN INTENT

Makad's neck shall be designed around three rotational axes:

[
\boxed{\text{Yaw + Pitch + Roll}}
]

with:

* **yaw** mandatory,
* **pitch** mandatory,
* **powered roll** the intended implementation.

A 2-DOF yaw/pitch neck remains an explicit fallback only if mechanical prototyping shows that roll produces disproportionate complexity, mass, backlash or packaging problems.

The mechanical design must therefore **reserve roll structurally from the beginning** rather than trying to retrofit it later.

---

## C2-R02 — Joint ordering — MUST-HAVE

The preferred serial kinematic order from body to head shall be:

[
\boxed{\text{Body → Yaw → Pitch → Roll → Head/Camera}}
]

The **roll joint should be the joint closest to the head**, so that its rotation is approximately about the head's own forward/optical axis.

This gives us the movement we actually mean by:

> “Makad tilts its face sideways inquisitively.”

Putting roll underneath other axes can cause the head to sweep through space rather than simply tilt about its own face axis.

A different joint order is permitted only if the kinematic design demonstrates equivalent behaviour.

---

# 2. Roll Range Is No Longer Arbitrarily Frozen

## C2-R03 — Perceptually determined roll range — MUST-HAVE

The final roll range shall **not yet be frozen at ±15° or ±20°**.

Instead, before neck CAD is finalized, we shall build a visual/mock mechanical test using Makad's approximate head shape and determine what amount of roll actually reads clearly as:

* curiosity,
* confusion,
* playful tilt,
* attentive listening.

Provisional engineering envelope:

**approximately ±15–25°.**

The final number shall be chosen from perceptual testing rather than aesthetics guessed from a specification sheet.

---

# 3. Smallest Physical Expressive Motion

This was missing and is necessary to make the backlash requirement meaningful.

## C2-R04 — Minimum intended physical neck motion — MUST-HAVE

For the first prototype, the smallest deliberate **physical neck movement** shall be defined as approximately:

[
\boxed{A_{min}=4^\circ}
]

of joint-angle change.

Movements smaller than approximately 4° should normally be handled through:

* animated eyes,
* timing,
* body animation,

unless prototype testing demonstrates that the neck can reliably produce smaller movements.

Typical subtle neck movements can therefore occupy roughly:

**4–10°.**

This value may later be reduced if the actuator/mechanism proves capable of it.

---

# 4. Backlash Requirement — REWRITTEN

## C2-R05 — Backlash relative to motion amplitude — MUST-HAVE

Total mechanical lost motion on reversal shall satisfy:

[
\boxed{
B \leq 0.25A_{min}
}
]

where:

* (B) = measured joint backlash,
* (A_{min}) = smallest intended physical expressive movement.

With:

[
A_{min}=4^\circ
]

the first-prototype requirement becomes:

[
\boxed{B\leq1^\circ}
]

### Target

[
\boxed{B\leq0.5^\circ}
]

This replaces the previous ≤2° requirement.

A joint with 2° backlash is not acceptable for a robot expected to execute reliable 4° micro-gestures.

---

## C2-R06 — Repeatability — TARGET

Joint-output repeatability shall target approximately:

[
\boxed{\pm0.5^\circ}
]

under repeatable loading.

Backlash, repeatability and encoder resolution shall be treated as separate properties rather than conflated.

---

# 5. Mass Properties — Expanded

## C2-R07 — Mass model — MUST-HAVE

Before actuator selection, the moving assembly shall have a mass model containing:

* component mass,
* approximate X/Y/Z position,
* which neck axes move that component.

This is important because the three actuators do **not necessarily rotate the same mass**.

For example, depending on architecture:

```text
Yaw moves:
head + roll mechanism + pitch mechanism

Pitch moves:
head + roll mechanism

Roll moves:
primarily head
```

The exact moving masses shall come from the final arrangement.

---

## C2-R08 — Centre of mass — MUST-HAVE

The combined centre of mass of every relevant moving subassembly shall be calculated.

Pitch and roll axes shall be positioned as close to their respective moving assembly COMs as mechanically practical.

---

# 6. Moment of Inertia — NEW MUST-HAVE

## C2-R09 — Rotational inertia calculation — MUST-HAVE

The rotational moment of inertia shall be calculated for each neck axis before final actuator sizing.

This is no longer merely something to “consider.”

CAD mass-property tools should be used once geometry is available.

At minimum we require:

[
I_{yaw},\quad I_{pitch},\quad I_{roll}
]

for the actual assemblies moved by each joint.

For intuitive approximation:

[
I \approx mk^2
]

where (k) is the radius of gyration.

For example, a hypothetical:

* 1 kg moving assembly,
* 60 mm radius of gyration,

gives:

[
I=1(0.06)^2
=0.0036\ kg,m^2
]

A fast expressive acceleration of:

[
70\ rad/s^2
]

would therefore require approximately:

[
\tau=I\alpha
]

[
\tau=0.0036(70)
]

[
\boxed{\tau\approx0.25,Nm}
]

from inertia alone.

That is especially important for yaw, where gravitational torque is normally small.

---

# 7. Design Angular Acceleration

## C2-R10 — Acceleration envelope — MUST-HAVE BEFORE ACTUATOR SELECTION

Motor sizing cannot use velocity alone.

Representative animation trajectories shall establish approximate peak angular accelerations.

Until actual character trajectories are prototyped, actuator screening shall consider approximately:

* **gentle/idle:** ~5–15 rad/s²
* **normal expressive:** ~15–30 rad/s²
* **fast recoil/attention:** up to approximately **50–70 rad/s²**

These are provisional engineering design cases, **not mandatory animation speeds**.

Before hardware is frozen, we should create representative motion curves and extract the actual:

[
\omega_{max}
]

and

[
\alpha_{max}
]

from them.

---

# 8. Torque Budget — REWRITTEN

## C2-R11 — Per-axis torque equation — MUST-HAVE

Every neck axis shall have its own torque budget.

Approximately:

[
\boxed{
\tau_{joint}
============

\tau_g
+
\tau_I
+
\tau_f
+
\tau_c
+
\tau_d
+
margin
}
]

where:

* (\tau_g) = gravitational torque,
* (\tau_I=I\alpha) = inertial torque,
* (\tau_f) = bearing/gear/friction torque,
* (\tau_c) = cable resistance,
* (\tau_d) = disturbances such as base acceleration.

---

### Pitch

Usually influenced strongly by:

[
gravity + inertia
]

---

### Roll

Influenced by:

[
gravity + inertia
]

depending on COM placement.

---

### Yaw

For a near-vertical yaw axis on a level robot:

[
\tau_g\approx0
]

so yaw sizing is principally:

[
\boxed{
\tau_{yaw}
\approx
I_{yaw}\alpha
+
friction
+
cable\ resistance
+
disturbances
+
margin
}
]

The previous generic “2× gravitational torque” rule therefore **shall not be applied to yaw**.

---

# 9. The 2× Rule — Demoted to Sanity Check

## C2-R12 — Gravity screening rule

The previous:

> 2× worst-case gravitational torque

rule is no longer an actuator-sizing requirement.

It may only be used as a **quick early sanity check for gravity-loaded axes**.

Final actuator sizing shall use the complete dynamic torque budget.

---

# 10. Stall Torque / Rated Torque — REWRITTEN

## C2-R13 — Torque-rating hierarchy — MUST-HAVE

Actuator selection shall follow this order:

**First preference:** manufacturer-provided continuous/rated operating torque.

**Second preference:** manufacturer torque-speed/current curves accompanied by thermal limits.

**Fallback:** stall torque with a conservative derating factor.

ROBOTIS itself recommends roughly **20% of published stall torque as a general operating selection region** for many DYNAMIXEL applications, which corresponds to approximately a 5× stall-to-design derating. ([ROBOTIS e-Manual][1])

Therefore, where no better continuous information exists, initial Makad sizing shall conservatively use approximately:

[
\boxed{
\tau_{design}\leq0.20\tau_{stall}
}
]

until physical thermal testing justifies something less conservative.

This is **not** a universal motor law; it is our fallback engineering rule.

---

## C2-R14 — Smart actuator architecture — TARGET / STRONGLY PREFERRED

Smart serial/bus actuators are strongly preferred because useful products can expose combinations of:

* position,
* velocity,
* current/load,
* voltage,
* temperature,
* faults.

Both DYNAMIXEL X-series devices and Feetech STS-series devices provide substantially richer telemetry than a basic PWM hobby servo. ([ROBOTIS e-Manual][2])

However, SPEC-02 still does **not mandate a particular brand**.

Equivalent sensing may be constructed externally if justified.

---

# 11. Where Position Feedback Is Measured

This is an important correction.

## C2-R15 — Actual joint pose shall be measurable — MUST-HAVE

The orientation used by:

* trajectory control,
* camera transforms,
* gaze control,

must represent the **physical head joint orientation**, not merely an upstream motor rotor position.

---

## C2-R16 — Joint-side encoder rule — MUST-HAVE WHEN TRANSMISSION EXISTS

If any of the following exists downstream of the actuator's internal position sensor:

* belt drive,
* external gear pair,
* linkage,
* compliant coupling,
* significant flexible printed structure,
* other mechanism capable of introducing lost motion,

then an independent **joint-output position sensor shall be used**.

Conceptually:

```text
motor encoder
     ↓
 gearbox / belt / linkage
     ↓
possible backlash
     ↓
JOINT ENCODER
     ↓
actual head pose
```

The gaze/perception transform shall use the joint-side value.

---

## C2-R17 — Direct-drive exception

If the actuator output is rigidly coupled directly to the actual joint axis and external bearings merely support the load without creating another kinematic transmission, the actuator's own output encoder may be sufficient.

Therefore:

> **proper bearings do not automatically require another encoder; downstream uncertainty does.**

---

## C2-R18 — Joint-side absolute sensing — TARGET

Joint-side **absolute magnetic angle sensing** is preferred where practical.

Sensors in the AS5600 class provide contactless 12-bit absolute angular sensing, illustrating the type of inexpensive technology suitable for this role. ([ams-osram][3])

Target joint-angle sensor resolution:

[
\boxed{\leq0.1^\circ}
]

Target calibrated joint-angle accuracy:

[
\boxed{\leq0.5^\circ}
]

Exact sensor remains unselected.

---

# 12. Camera Pose Truth

## C2-R19 — Perception uses best joint estimate — MUST-HAVE

Camera orientation shall be calculated using the **best available measured physical joint state**.

If external joint encoders exist, their readings shall take precedence over merely assuming:

```text
commanded servo angle = actual head angle
```

This is necessary because the camera is physically attached to the head.

---

# 13. Screen Eyes and the Mona Lisa Problem

The previous specification overestimated what eye-only gaze can communicate.

Flat portraits can produce viewpoint-robust gaze perception—the classic “Mona Lisa effect”—so a rendered pupil direction is not automatically a reliable 3-D pointing cue for observers standing at different angles. ([PubMed Central (PMC)][4])

Therefore:

## C2-R20 — Eyes-first ≠ eyes-only spatial pointing

The animated eyes shall primarily provide:

* anticipation,
* attention timing,
* emotion,
* local gaze cue,
* animation continuity.

For substantial spatial attention changes, **physical head orientation shall remain the primary unambiguous cue** that Makad is attending to a particular person or direction.

---

## C2-R21 — Eye-only comfort region — REWRITTEN

The eye-only tracking region shall be deliberately small.

Its final size shall be determined empirically rather than solely from camera geometry.

Initial prototype limit:

[
\boxed{\text{approximately }\pm3^\circ\text{ to }\pm5^\circ}
]

equivalent target displacement before the head begins following.

This value is provisional.

---

## C2-R22 — Eyes-first sequencing remains MUST-HAVE

The sequence:

```text
target appears
      ↓
eyes shift
      ↓
short anticipation interval
      ↓
head follows
      ↓
eyes recenter
```

remains important.

But its purpose is now explicitly understood as:

> **character animation and anticipatory signalling**

rather than assuming that animated eyes alone provide accurate physical gaze direction.

---

# 14. Screen-Gaze Perception Test — NEW

## C2-T01 — Off-axis gaze readability

Naive observers shall view Makad from approximately:

* centre,
* ~45° left,
* ~45° right.

With the physical head stationary, display:

* centre gaze,
* modest left gaze,
* modest right gaze.

Observers shall independently report where they believe Makad is attending.

The result shall be used to determine the actual allowable eye-only region.

If off-axis directional discrimination is poor, the software shall reduce the eye-only range rather than attempting to force a larger one.

This is a **calibration experiment**, not an assumption that the display must magically solve the Mona Lisa effect.

---

# 15. Nominal Interaction Pose

## C2-R23 — Expected duty-cycle pose — MUST-HAVE

Neck design shall distinguish:

1. mechanical worst-case pose,
2. **most common sustained operating pose**.

Because Makad is intended primarily as a desk companion, the typical interaction geometry shall be measured/modelled before final COM placement.

Likely variables include:

* desk height,
* Makad camera height,
* seated user eye height,
* interaction distance.

The resulting **nominal gaze pitch** shall become a design parameter.

---

## C2-R24 — COM bias priority

Ideal:

> place the pitch axis through the actual COM so gravitational torque remains very small throughout motion.

If packaging prevents this and a residual COM offset is unavoidable, the geometry should preferentially reduce gravitational torque around the **most frequently sustained interaction pose**, rather than blindly optimising the arbitrary “head perfectly level” pose.

---

# 16. Holding Torque and Servo Buzz

## C2-R25 — Reduced holding effort — MUST-HAVE CAPABILITY

The control architecture shall support reducing actuator effort in mechanically stable poses where safe.

Possible implementations include:

* reduced current limit,
* reduced torque limit,
* relaxed control gains,
* partial torque reduction,
* complete torque-off only if the mechanism cannot fall or drift dangerously.

Makad must **never simply disable torque if doing so allows its heavy head to collapse**.

COM balancing is therefore directly connected to acoustic quality and power consumption.

---

# 17. Acoustic Specification — NEW

These are provisional Makad design targets, not claimed industry standards.

Measurements shall be taken approximately **0.5 m from the robot**.

## C2-R26 — Static hold noise — TARGET

Stable head holding should add no more than approximately:

[
\boxed{+3\text{ to }+5\ dBA}
]

above ambient room noise.

Persistent audible servo buzzing is undesirable.

---

## C2-R27 — Normal motion noise — TARGET

Idle/tracking head motion should target approximately:

[
\boxed{\leq45\ dBA(A)}
]

at 0.5 m.

---

## C2-R28 — Fast expressive transient — TARGET

Brief fast gestures should target approximately:

[
\boxed{\leq50\ dBA(A)}
]

at 0.5 m.

These thresholds must be validated on the actuator mule; if unrealistic for the chosen cost/torque class, they may be explicitly revised rather than quietly ignored.

---

# 18. Degraded Modes — NEW

## C2-R29 — Perception failure — MUST-HAVE

If face/person perception disappears or crashes:

Makad shall:

* stop closed-loop person tracking,
* avoid uncontrolled searching,
* retain safe bounded head behaviour,
* transition to idle/reacquisition logic.

---

## C2-R30 — Actuator overtemperature/overcurrent — MUST-HAVE

If an actuator reports unsafe thermal/load conditions:

the system shall:

1. cancel high-energy gestures,
2. reduce demanded torque/speed,
3. return toward a safer/lower-load pose if feasible,
4. disable the affected axis if necessary,
5. report a fault to the behaviour system.

It shall not repeatedly retry the same damaging movement.

---

## C2-R31 — Joint-sensor failure — MUST-HAVE

If the controller cannot trust an axis's physical orientation:

* that axis shall enter a bounded safe mode,
* perception shall stop treating its camera transform as trustworthy,
* high-speed tracking shall cease.

---

## C2-R32 — Neck communication failure — MUST-HAVE

Loss of communication with the high-level controller shall trigger a defined timeout behaviour.

Depending on mechanical architecture, the low-level controller shall either:

* safely hold the current pose,
* move to a safe pose,
* or relax safely.

The response must be deterministic.

---

# 19. Base Coordination — Clarified

The wheeled base has **not actually been newly introduced by SPEC-02**; it is already part of Makad's frozen 20-point master functionality.

However, the previous version blurred subsystem responsibility.

## C2-R33 — Base coordination is an interface requirement

SPEC-02 must expose the coordinate/command interfaces necessary to coordinate with the mobile base.

It is **not responsible for designing the mobile base**.

Therefore:

```text
SPEC-02:
"What head orientation do I need?"

SPEC-16+:
"How does the base physically achieve its part?"
```

---

## C2-R34 — Base counter-motion — TARGET

Head lag/settling during acceleration remains a character-animation target.

It shall not be required for initial neck validation.

---

# 20. Quantitative Validation Infrastructure — NEW

## C2-R35 — Motion logging — MUST-HAVE

During validation, record at least:

* timestamp,
* commanded joint position,
* measured joint position,
* commanded velocity,
* measured/estimated velocity,
* target coordinates,
* relevant fault/current/temperature telemetry.

Target logging frequency:

[
\boxed{\geq100\ Hz}
]

where the hardware permits it.

---

## C2-R36 — High-speed video validation — MUST-HAVE METHOD

A high-frame-rate camera/phone may be used to independently measure:

* overshoot,
* settling,
* latency,
* backlash,
* visible jitter.

Approximately **240 fps** is sufficient for many Makad motion measurements.

This gives us an external truth source rather than believing our own controller logs.

---

# 21. Revised Acceptance Tests

## C2-T02 — Minimum-motion/backlash test

Command repeated:

[
+4^\circ \leftrightarrow -4^\circ
]

slow reversals.

Measure actual head orientation.

### Pass

Measured reversal lost motion:

[
\boxed{\leq1^\circ}
]

### Target

[
\leq0.5^\circ
]

---

## C2-T03 — Repeatability test

Approach a fixed commanded pose repeatedly from both directions.

### Target

Final physical joint pose repeatability:

[
\boxed{\pm0.5^\circ}
]

measured at the joint/head rather than inferred purely from commands.

---

## C2-T04 — Smooth trajectory test

Command a 10° movement at approximately 5°/s.

### Pass

* no uncommanded direction reversals,
* no obvious stick-slip event,
* RMS tracking error approximately ≤0.5° after calibration.

---

## C2-T05 — Step/attention response

Perform a representative approximately 30° attention shift.

Measure:

* reaction latency,
* peak velocity,
* overshoot,
* settling time.

Intentional animation overshoot shall be tagged separately from control error.

---

## C2-T06 — Stationary-target jitter

Track a stationary target.

After initial settling, record at least 30 seconds.

### Target

Per-axis RMS physical head-angle deviation:

[
\boxed{\leq0.5^\circ}
]

and peak-to-peak unintended motion:

[
\boxed{\leq1.5^\circ}
]

unless a deliberate idle/expressive motion occurs.

---

## C2-T07 — Moving-camera compensation

Keep the target stationary in the room.

Move Makad's head deliberately.

### Pass

The system does not enter self-excited oscillation by interpreting camera motion as equivalent target motion.

Joint logs, target estimates and external video shall be inspected.

---

# 22. The Missing Thesis Test — NEW

## C2-T08 — “Does it look like a character?” observer test

This directly evaluates the top-level requirement:

> Makad should not look like a pan/tilt security camera.

Create matched motion demonstrations using:

**A. baseline controller**

* direct target following,
* linear/simple trajectories,
* no eye lead,
* no anticipation/settling.

**B. Makad character controller**

* eye anticipation,
* smooth acceleration,
* head follow,
* expressive timing,
* appropriate settling.

Show randomized clips/live demonstrations to **at least 8–12 people who did not design the robot**.

Ask open-ended questions such as:

* “What does the robot seem to be doing?”
* “Which one feels more alive/intentional?”
* “What emotion/intention do you read?”
* “Does either motion remind you of a camera/gimbal rather than a character?”

### Target

At least approximately **80%** should prefer the Makad controller as more character-like/lifelike than the mechanical baseline.

The qualitative responses should also broadly match the intended behaviour.

This is not a scientific publication-scale user study; it is an engineering acceptance test for our fundamental design goal.

---

# 23. Roll Readability Test — NEW

## C2-T09 — Roll-angle selection

Using the representative Makad head shell, test several roll amplitudes, for example:

* 10°
* 15°
* 20°
* 25°

with naive observers.

Ask which reads clearly as a curious/listening tilt without becoming exaggerated.

The chosen range shall become the final roll specification **before neck CAD freeze**.

This resolves the concern that a large shell may visually swallow a 15° tilt.

---

# 24. Thermal Testing — REWRITTEN

## C2-T10 — Four-hour mixed-duty endurance

The previous 30-minute test is removed.

Run the finished neck for:

[
\boxed{\geq4\ hours}
]

using a representative mixture of:

* person tracking,
* idle movements,
* conversational gestures,
* periodic fast reactions.

Log temperature/current throughout.

---

## C2-T11 — Sustained nominal-gaze thermal test

Once our actual desk/user geometry determines the common sustained pitch pose, hold/track around that orientation for an extended test.

This is separate from the mechanical worst-case pose.

### Pass

No:

* thermal fault,
* progressive sag,
* unstable buzzing,
* unsafe temperature,
* controller derating severe enough to harm normal behaviour.

---

## C2-T12 — Worst-case load test

Worst-case gravitational orientation shall still be tested separately to ensure adequate mechanical margin.

But it is **not a substitute for the common-duty test**.

---

# 25. Cable-Flex Qualification — REWRITTEN

The 1,000-cycle requirement is deleted.

At one motion every 20 seconds, 1,000 cycles represents only about **5.6 hours** of use, so it tells us almost nothing about sustained desk operation.

## C2-T13 — Cable bench test

A dedicated fixture should exercise the actual:

* cable type,
* bend radius,
* routing,
* connector arrangement,

through representative neck motion.

### Minimum prototype validation

[
\boxed{50,000\ cycles}
]

### Target

[
\boxed{100,000\ cycles}
]

This does **not** need to consume 100,000 movements of the assembled robot; a bench fixture can cycle the harness continuously.

Inspect afterward for:

* conductor failure,
* insulation damage,
* abrasion,
* connector loosening,
* increased electrical resistance,
* intermittent signals.

---

# 26. Updated Gaze Architecture

The architecture is now explicitly:

```text
                    CAMERA
                       │
                       ↓
                PERCEPTION
                       │
                       ↓
                 TARGET TRACKER
                       │
                       ↓
                TARGET SELECTOR
                       │
                       ↓
               DESIRED ATTENTION
                       │
                       ↓
              ┌─────────────────┐
              │ GAZE CONTROLLER │
              └────────┬────────┘
                       │
          ┌────────────┼─────────────┐
          ↓            ↓             ↓
     SCREEN EYES    HEAD GOAL     BASE/BODY
          │            │
          │       MOTION PLANNER
          │            ↓
          │       TRAJECTORY
          │            ↓
          │      JOINT CONTROLLER
          │       ↓     ↓     ↓
          │      yaw  pitch  roll
          │       ↓     ↓     ↓
          │      ACTUATORS
          │            ↓
          │      JOINT ENCODERS
          │            │
          └────────────┼──────────────┐
                       ↓              │
                  CAMERA POSE         │
                       ↓              │
                   PERCEPTION ←───────┘
```

And the important conceptual change is:

[
\boxed{
\text{Eyes signal attention first;
head establishes physical gaze;
body/base handles large orientation changes.}
}
]

Not simply:

[
\text{Eyes → Head → Base}
]

as if all three were interchangeable pointing devices.

---

# 27. Updated MUST-HAVE / TARGET Split

### MUST-HAVE

* yaw + pitch
* architecture designed around roll
* yaw → pitch → roll kinematic intent
* smallest physical expressive movement defined
* ≤1° backlash at current 4° minimum-motion requirement
* mass model
* COM calculation
* **moment-of-inertia calculation**
* per-axis dynamic torque budget
* explicit yaw torque sizing
* conservative stall-torque derating when rated data unavailable
* actual physical joint pose available to control/perception
* joint-side encoder whenever downstream transmission introduces uncertainty
* moving-camera-aware perception
* rigid calibrated camera transform
* dedicated gaze controller
* eyes-first anticipation
* physically meaningful head orientation for larger gaze shifts
* empirical eye-only region
* reduced-hold strategy
* degraded modes
* 100 Hz-class validation logging
* quantitative motion tests
* four-hour endurance test
* ≥50k cable-cycle bench validation
* naive-observer character-motion test

### TARGET

* powered roll
* final empirically selected roll range
* ≤0.5° backlash
* ±0.5° joint repeatability
* external absolute encoder on every neck axis even where direct drive would technically permit using the actuator encoder
* smart bus actuator telemetry
* ≤45 dBA normal-motion target
* ≤50 dBA fast-motion target
* 100k cable-cycle validation
* refined eye/head perceptual calibration
* base counter-motion.

---

## One important result from this review

This critique has actually pushed us toward a much better engineering architecture.

We're no longer specifying:

> “three servos that move a cute head.”

We're specifying a **measured 3-axis camera-bearing mechanism** whose:

[
mass
\rightarrow COM
\rightarrow inertia
\rightarrow desired acceleration
\rightarrow torque
\rightarrow actuator
]

chain can actually be calculated, while the perception side uses:

[
camera
+
actual\ joint\ angles
\rightarrow
camera\ pose
\rightarrow
target\ direction
\rightarrow
gaze\ controller
]

and the animation side solves:

[
\text{“technically tracked”}
\neq
\text{“looks alive.”}
]

That is the version of **SPEC-02 I would carry forward now**. The two things deliberately left unfrozen are **the exact roll angle** and **the exact actuator/encoder architecture**; we now have concrete tests that will tell us those answers rather than choosing them by intuition.

[1]: https://emanual.robotis.com/docs/en/reference/dxl-selection-guide/?utm_source=chatgpt.com "DYNAMIXEL Selection Guide"
[2]: https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/?utm_source=chatgpt.com "XL330-M077-T"
[3]: https://ams-osram.com/de/products/boards-kits-accessories/boards/ams-as5600-so-evm-potuino-evaluation-board?utm_source=chatgpt.com "ams AS5600_SO_EVM_POTUINO Evaluation board Boards | ams OSRAM"
[4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6869588/?utm_source=chatgpt.com "The Mona Lisa effect: Neural correlates of centered and off‐centered gaze - PMC"
