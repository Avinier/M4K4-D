Yes. Below is the **patched final Spec 3**, with the review incorporated and the earlier contradictions removed. I’m treating this as the version we carry forward into the master Makad spec.

# MAKAD SPEC 3 — Whole-Body Physical Expression & Motion Coordination

**Capability:** #3 — Makad will use its entire upper body for physical expression
**Subsystem:** Physical expression / motion composition
**Status:** **FINAL for requirements phase**
**Upstream dependencies:** Spec 1 — Face/Expression System; Spec 2 — Head/Neck Motion System
**Downstream dependencies:** Specs 9, 12, 13, 16, 17, 18, 19, 20

---

# 3.1 Purpose

Makad shall communicate physical character through coordinated motion of its:

* head/neck;
* rigid upper body;
* optional torso articulation;
* wheeled base.

Physical expression shall reinforce the animated face rather than merely move hardware.

Examples include:

* attentive/perked posture;
* curiosity;
* recoil/startle;
* excitement;
* hesitation;
* relaxation;
* anticipation before movement;
* apparent inertia while accelerating/braking;
* overshoot and settling.

The design objective is:

> **Makad should appear to possess mass, posture and intention rather than looking like a screen mounted rigidly on a wheeled box.**

---

# 3.2 Scope decision

Makad V1 **MUST** support whole-robot expressive motion through coordinated head/neck and wheeled-base movement.

A separately actuated torso-pitch joint is **TARGET**, not a V1 MUST.

This is a deliberate capability trade-off.

Head pitch, torso pitch and translation are not equivalent:

```text
HEAD PITCH
    ↓
 "looking"


TORSO PITCH
    ↓
 "leaning / postural interest"


BASE TRANSLATION
    ↓
 "approaching / retreating"
```

Therefore torso pitch is being **deferred, not declared unnecessary**.

To prevent this TARGET from becoming impossible later, V1 shall preserve the necessary structural interface for it.

---

# 3.3 Mechanical architecture

### C3-R01 — Physical-expression channels — **MUST**

V1 shall support expressive physical motion using at minimum:

* Spec-2 head/neck motion;
* differential-drive base motion;
* coordinated timing between them.

---

### C3-R02 — Powered torso pitch — **TARGET**

Makad should include one independently actuated **body-pitch DOF** between the mobile base and rigid upper body if CAD, stability, packaging, power and project schedule permit.

No powered torso yaw or torso roll is required for V1.

---

### C3-R03 — Torso upgrade interface — **MUST**

Even if the torso-pitch actuator is omitted from the first build, the body-to-base architecture shall preserve a practical upgrade path for one.

Before detailed structural CAD is frozen, the design shall reserve:

* a removable structural body-to-base interface;
* a defined load-bearing fastener pattern;
* sufficient width/clearance for a horizontal pitch axis;
* bearing/support volume;
* actuator/transmission volume;
* cable pass-through;
* cable service-loop volume;
* shell clearance for the intended movement.

No permanently mounted battery, PCB, structural brace or enclosure feature shall make the reserved articulation envelope unusable.

---

### C3-R04 — Modular replacement principle — **TARGET**

The preferred architecture shall permit a rigid spacer/interface module to be replaced later by a powered pitch module without redesigning the complete upper body or mobile base.

Conceptually:

```text
INITIAL

 UPPER BODY
      │
 ┌────┴────┐
 │  RIGID  │
 │INTERFACE│
 └────┬────┘
      │
     BASE
```

later:

```text
 UPPER BODY
      │
   ●─────●
     \ /
    PITCH
    MODULE
      │
     BASE
```

---

# 3.4 Conditional torso-pitch specification

The following requirements apply **if the powered torso-pitch TARGET is implemented.**

### C3-R05 — Usable travel

Total usable expressive pitch:

**≥12°**

with at least:

**5° in either direction from neutral.**

---

### C3-R06 — Preferred travel — **TARGET**

Preferred design range:

**approximately ±8–10° around neutral.**

Large angular travel is not a goal by itself.

---

### C3-R07 — Minimum intentional gesture amplitude

The smallest intentional reversible torso gesture shall initially be approximately:

**4°**

until prototype animation testing demonstrates a useful reason to require smaller torso movements.

Subtle 1–2° motion should primarily be handled by the head/eyes.

---

### C3-R08 — Structural joint support

The upper body shall not be supported solely by an actuator horn/output shaft.

The pitch joint shall have an independent load path through:

* bearings;
* bushings;
* supported shaft structures;

or equivalent.

---

### C3-R09 — Double-supported axis — **TARGET**

The torso pitch axis should preferably be structurally supported at two separated locations.

---

### C3-R10 — Hard and software travel limits

The joint shall include physical travel limits preventing:

* shell collision;
* actuator overtravel;
* cable crushing;
* structural interference.

Normal software limits shall remain inside physical hard-stop limits.

---

### C3-R11 — Known joint state

After startup, the body joint shall establish a reliable known position before expressive commands are permitted.

---

### C3-R12 — Body-position feedback

Requested and measured torso position shall be represented separately.

Open-loop timing-based torso control is unacceptable.

---

# 3.5 Mass, centre of mass and inertia

### C3-R13 — Moving-mass model — **MUST if torso pitch is implemented**

CAD shall provide:

* moving upper-body mass;
* pitch-axis location;
* moving-body COM relative to the pitch axis;
* total robot COM at neutral;
* total robot COM at permitted forward extreme;
* total robot COM at permitted backward extreme.

---

### C3-R14 — Moment of inertia — **MUST if torso pitch is implemented**

The moving upper-body moment of inertia around the torso-pitch axis shall be extracted from CAD or otherwise calculated.

It shall not remain qualitative.

---

### C3-R15 — Gravity torque calculation

Gravitational load shall be calculated using the actual geometry:

[
\tau_g = mgr\sin(\theta)
]

where (r) represents the relevant COM offset from the pivot.

---

### C3-R16 — Dynamic torque sizing

Torso actuator/transmission sizing shall consider:

[
\tau_{req}
==========

I\alpha
+
\tau_g
+
\tau_{friction}
+
\tau_{cable}
]

rather than gravitational holding torque alone.

---

### C3-R17 — Continuous vs peak load

Continuous thermal/holding requirements and transient dynamic torque requirements shall be evaluated separately when actuator data permits.

Advertised stall torque alone shall not be used for selection.

---

### C3-R18 — COM-conscious pivot placement — **TARGET**

The torso-pitch axis should be located reasonably close to the moving upper-body COM when compatible with:

* visual proportions;
* packaging;
* structural requirements;
* required motion appearance.

---

# 3.6 Static and dynamic stability

Makad is **not a balancing robot**.

Its wheel/caster support geometry shall provide passive static stability.

### C3-R19 — Static stability — **MUST**

For every permitted static head/body configuration, the projected total COM shall remain safely inside the support polygon.

---

### C3-R20 — Dynamic stability — **MUST**

Stability analysis shall include combinations of:

* head motion;
* optional torso lean;
* forward acceleration;
* forward braking;
* reverse acceleration/braking;
* turning.

Subsystems shall not be assessed only in isolation.

---

### C3-R21 — Motion-dependent articulation envelope — **TARGET**

If torso pitch is installed, its permitted travel should be dynamically reduced during aggressive locomotion where necessary.

For example:

```text
STATIONARY
    ↓
full torso envelope

SLOW DRIVE
    ↓
moderately restricted

HARD ACCELERATION / BRAKING
    ↓
more restricted
```

---

### C3-R22 — No intentional near-tipping behaviour — **MUST**

Makad shall not intentionally rely on:

* wheel lifting;
* caster lifting;
* dynamic balancing;
* operation near the tipping boundary

as part of expressive motion.

---

# 3.7 Operating environment assumptions

The addition of locomotion requires the operating environment to be frozen at a useful level.

### C3-R23 — Primary operating environment — **MUST**

Makad V1 shall be designed primarily for:

> **dry, level indoor floors.**

Primary expected surfaces include:

* tile;
* laminate/wood;
* vinyl;
* polished hard flooring.

---

### C3-R24 — Secondary surfaces — **TARGET**

Makad should tolerate where practical:

* small floor seams;
* minor surface irregularities;
* low-pile carpet.

---

### C3-R25 — Out of scope

V1 is not required to traverse:

* stairs;
* thick carpet;
* rug fringes;
* large thresholds;
* wet surfaces;
* outdoor terrain.

---

# 3.8 Support geometry assumption

### C3-R26 — Caster position — **MUST / system-level decision**

The baseline V1 drive geometry shall place the passive caster **ahead of the differential-drive axle**.

Exact caster offset remains subject to CAD and COM analysis.

This decision prioritizes support during forward braking, expected to be the more common higher-energy motion condition.

---

### C3-R27 — Reverse-motion envelope — **MUST**

Unless stability testing later demonstrates equivalent margins, reverse movement shall use lower:

* maximum speed;
* acceleration;
* deceleration

than forward locomotion.

---

# 3.9 Motion trajectory quality

### C3-R28 — Trajectory-based control — **MUST**

Head/body/base expressive motion shall not be generated using abrupt target-position jumps.

Trajectories shall control at minimum:

* position;
* velocity;
* acceleration.

Jerk-limited motion is preferred.

Suitable implementations include:

* S-curves;
* quintic interpolation;
* equivalent smooth motion profiles.

---

### C3-R29 — Gesture timing variation — **MUST**

A physical displacement shall be reusable at different temporal profiles.

For example:

```text
slow motion      → cautious / curious
medium motion    → attentive
fast recoil      → startled
```

Emotion shall not be encoded solely through target position.

---

### C3-R30 — Typical expressive timing — **TARGET**

Typical head/body expressive transitions should normally occur over approximately:

**250 ms – 1.5 s**

depending on behaviour.

---

### C3-R31 — Fast physical reaction — **TARGET**

Where mechanics and stability permit, the primary motion of a strong recoil/startle gesture should occur within approximately:

**≤300 ms.**

---

# 3.10 Locomotion-induced character motion

This is a core V1 feature.

### C3-R32 — Inertial character response — **MUST**

Significant base acceleration, braking and rotation shall be capable of producing coordinated head/body motion that communicates apparent inertia.

The motion shall be intentionally animated rather than resulting from uncontrolled structural wobble.

At minimum, the system shall support:

* relative backward head/body lag during forward acceleration;
* relative forward dip during forward braking;
* corresponding reversed responses during reverse movement;
* rotational lag/settling during significant turns;
* controlled overshoot;
* controlled settling.

---

### C3-R33 — Motion-intensity scaling — **MUST**

Counter-motion amplitude and timing shall scale with base-motion intensity.

```text
tiny reposition
      ↓
minimal reaction

normal travel
      ↓
subtle reaction

strong start / stop
      ↓
clearly visible reaction
```

---

### C3-R34 — Anticipation — **MUST**

The animation system shall support character motion **before** a planned base action.

Example braking sequence:

```text
anticipatory brace
       ↓
braking begins
       ↓
forward inertial dip
       ↓
small rebound
       ↓
settle
```

Anticipation shall not depend solely on sensing physical acceleration after it occurs.

---

# 3.11 Feedforward architecture

### C3-R35 — Planned-trajectory feedforward — **MUST**

The expressive motion composer shall receive the planned base trajectory, or an equivalent future velocity/acceleration schedule, **before the corresponding locomotion executes**.

Conceptually:

```text
        BEHAVIOUR REQUEST
               │
               ↓
        BASE TRAJECTORY
           PLANNER
               │
        planned v(t), a(t)
               │
        ┌──────┴───────┐
        ↓              ↓
 WHEEL CONTROL   MOTION COMPOSER
        │              │
      WHEELS       HEAD / BODY
        │              │
        └──────┬───────┘
               ↓
        MEASURED STATE
   encoders / IMU / joints
               │
               ↓
          CORRECTION
```

---

### C3-R36 — Feedforward vs feedback — **MUST**

Planned trajectory data shall provide **anticipation/feedforward**.

Measured data such as:

* wheel encoder velocity;
* odometry;
* IMU acceleration;
* joint position;

shall be used for **feedback and correction**.

Reactive sensing alone shall not be responsible for authored anticipation.

---

# 3.12 Emotion-dependent locomotion

### C3-R37 — Motion-style parameterization — **MUST**

The same physical drive/head system shall support different behavioural motion styles through software parameters.

At minimum, style shall be capable of modifying:

* acceleration;
* deceleration;
* anticipation magnitude;
* relative head/body lag;
* overshoot;
* settle duration.

---

### C3-R38 — Distinct locomotion personalities — **MUST**

V1 shall demonstrate at least **three clearly different motion styles**.

For example:

| Style    | Locomotion      | Physical response                         |
| -------- | --------------- | ----------------------------------------- |
| Curious  | gentle approach | attentive forward-biased posture          |
| Excited  | faster start    | larger lag/rebound and shorter settle     |
| Cautious | slow movement   | restrained movement and minimal overshoot |

Final emotion naming remains part of behaviour design.

---

# 3.13 Motion composition architecture

### C3-R39 — Layered composition — **MUST**

Joint/base commands shall be produced through a shared motion-composition system rather than independent subsystems directly commanding hardware.

Conceptually:

```text
calibration / neutral
        +
emotional posture
        +
active gesture
        +
locomotion response
        +
tracking correction
        ↓
safety / stability limiter
        ↓
final trajectories
```

---

### C3-R40 — Single control authority — **MUST**

Multiple behavioural subsystems shall not simultaneously fight for direct control of a given actuator.

The motion composer shall arbitrate and combine valid influences.

---

### C3-R41 — Safety authority — **MUST**

Mechanical and stability limits shall override requested emotional animation.

A requested gesture may therefore be:

* reduced;
* delayed;
* modified;
* cancelled

if current robot state makes the original request unsafe.

---

# 3.14 Persistent posture

### C3-R42 — Posture offsets — **TARGET**

The system should support persistent emotional/postural offsets separate from temporary gestures.

For example:

```text
baseline neutral       0°
interested posture    +2°
temporary gesture     +4°
                     ----
current requested     +6°
```

After the gesture completes, Makad may return to the emotional posture rather than geometrical zero.

---

# 3.15 Head/body/base coordination

### C3-R43 — Coordinated animation — **MUST**

Spec-1 face animation, Spec-2 head motion and Spec-3 physical motion shall be synchronizable on a shared timeline.

Example:

```text
0 ms      eyes orient
60 ms     head starts
160 ms    base begins subtle approach
200 ms    head settles into curiosity pose
350 ms    tiny overshoot
500 ms    settle
```

Exact timing is behaviour content rather than a hard requirement.

---

### C3-R44 — Gaze preservation during body/base motion — **TARGET**

During visual tracking, the head-control system should compensate for known base/body movement sufficiently to maintain attention on the target.

---

### C3-R45 — Dynamic transform awareness — **MUST**

Measured physical joint states shall be available to later perception/tracking systems.

The robot's transform hierarchy shall represent the actual physical architecture, for example:

```text
world / odom
     │
    base
     │
 optional torso_pitch
     │
    neck
     │
    head
     │
   camera
```

---

# 3.16 Structural dynamic behaviour

### C3-R46 — Controlled motion vs structural wobble — **MUST**

Expressive overshoot and settling shall be generated deliberately in software.

Uncontrolled flexing or ringing of the:

* chassis;
* neck;
* head mount;
* torso mechanism

shall not be treated as acceptable character motion.

---

### C3-R47 — Structural resonance separation — **MUST**

The first significant flexible structural resonance of the assembled head/neck/body system shall be sufficiently separated from the dominant expressive-motion excitation bandwidth.

Normal trajectory excitation should remain approximately:

[
f_{animation,max}
\le
\frac{1}{3}
f_{structural,1}
]

where practical.

---

### C3-R48 — Structural frequency — **TARGET**

Target first significant neck/head structural mode:

**approximately ≥15–20 Hz**

subject to prototype measurement.

If the system fails to provide adequate dynamic separation, corrective action may include:

* increasing structural stiffness;
* reducing head mass;
* changing geometry;
* reducing commanded acceleration;
* reducing commanded jerk.

Increasing actuator torque alone shall not be considered sufficient.

---

# 3.17 Backlash and repeatability

### C3-R49 — Backlash requirement — **MUST for torso articulation**

Mechanical output backlash shall satisfy:

[
Backlash
\le
0.25 A_{min}
]

For the current 4° minimum torso gesture:

[
Backlash \le 1^\circ
]

---

### C3-R50 — Repeatability — **TARGET**

Repeated physical posture commands should reproduce orientation to approximately:

**±1° or better.**

---

# 3.18 Interruption and preemption

### C3-R51 — Interruptible motion — **MUST**

Expressive movements shall be interruptible by higher-priority behaviour.

For example:

> idle rocking → person speaks → idle trajectory transitions immediately toward attentive behaviour.

The controller shall not need to finish an entire irrelevant animation first.

---

### C3-R52 — Continuous preemption — **MUST**

A new trajectory shall begin from the **current measured physical state**.

Interrupting an animation shall not produce discontinuous commanded jumps.

---

# 3.19 Fault handling

### C3-R53 — Motion obstruction detection — **MUST where supported**

For powered expressive joints, the system shall detect significant discrepancies between commanded and actual motion using available:

* position;
* velocity;
* current/load;
* timing

information.

---

### C3-R54 — Safe motion fault — **MUST**

Detected obstruction or actuator fault shall cause the controller to:

1. terminate escalating motion effort;
2. cancel the active gesture;
3. enter the safest reachable state;
4. report the fault to the central behaviour system.

---

### C3-R55 — Power-loss mechanical behaviour — **MUST if torso articulation is fitted**

Loss of actuator power shall not allow the upper body to fall violently through its entire range.

Appropriate techniques may include:

* transmission friction;
* damping;
* counterbalance;
* geometry;
* passive mechanical restraint.

---

# 3.20 Wiring and serviceability

### C3-R56 — Moving harnesses — **MUST**

Any wiring crossing an expressive joint shall explicitly account for:

* minimum bend radius;
* repeated flexing;
* full range of motion;
* strain relief;
* snag avoidance;
* connector loading.

Wiring shall never function as an unintended mechanical stop.

---

### C3-R57 — Serviceable motion mechanisms — **TARGET**

Expressive actuators/joints should be replaceable without complete destruction of Makad's enclosure.

---

### C3-R58 — Motion-joint endurance — **TARGET**

Prototype:

**≥1,000 representative cycles**

Finished mechanism:

**≥5,000 representative cycles**

without unacceptable:

* wiring damage;
* connector loosening;
* structural loosening;
* backlash increase;
* actuator faults.

---

# 3.21 Enclosure / neck cross-cutting requirement

Makad's angular/faceted industrial design belongs primarily to a later enclosure/industrial-design specification.

However, Spec 3 establishes the following integration requirement.

### C3-R59 — Full-motion enclosure clearance — **MUST**

Final enclosure geometry shall preserve the complete motion range established by the motion specifications.

Clearance verification shall use compound extreme configurations, including where applicable:

* maximum yaw + pitch;
* maximum yaw + roll/tilt;
* maximum pitch + torso pitch;
* motion while cables and covers are installed.

---

### C3-R60 — No accidental exposed-motion gaps — **TARGET**

Moving interfaces should use deliberate mechanical treatments such as:

* recessed joint cavities;
* overlapping collars;
* nested panels;
* flexible covers;

or equivalent.

Extreme poses should not expose wiring or internals through accidental-looking enclosure gaps.

---

### C3-R61 — Industrial design shall not reduce ROM — **MUST**

Visual enclosure decisions shall not silently reduce already-approved mechanical ranges of motion.

Any required reduction shall be explicitly returned to the relevant motion spec for approval.

---

# 3.22 Locomotion acoustics dependency

### C3-R62 — Audio compatibility during motion — **MUST**

Normal locomotion and expressive motion shall not make Makad's voice-input system unusable at its specified interaction distance.

The exact speech/audio acceptance metric will be defined in Spec 4.

This requirement shall influence later selection/design of:

* drive motors;
* gearboxes;
* wheel material;
* motor mounting;
* chassis stiffness/damping;
* PWM/control strategy.

---

# 3.23 Odometry dependency

### C3-R63 — Wheel odometry — **MUST / system-level dependency**

The locomotion system shall provide differential wheel odometry sufficient to estimate:

* wheel velocity;
* linear base velocity;
* angular base velocity;
* incremental displacement.

This is required for both locomotion control and comparison between planned and actual character movement.

It does **not** imply full SLAM.

---

# 3.24 Charging/interface dependency

### C3-R64 — Manual charging — **MUST / system-level**

Makad shall provide an externally accessible safe charging interface.

---

### C3-R65 — Dock-ready rear region — **MUST**

Before enclosure geometry is frozen, a lower rear region shall be reserved so a future charging dock can physically interface with the robot.

The region should remain compatible with future:

* charging contacts;
* alignment features;
* docking guides;
* visual/sensor targets.

---

### C3-R66 — Autonomous docking — **STRETCH**

Automatic charger detection, approach, alignment and connection are not required for V1.

---

# 3.25 Cliff-safety dependency

### C3-R67 — Drop-off protection — **MUST / owned by Spec 18**

Because Makad is an autonomous floor robot, the future collision/environmental-sensing system shall include protection against significant downward drop-offs such as stairs.

This also provides secondary protection if Makad is operated on an elevated surface.

---

# 3.26 Required physical-expression repertoire

### C3-R68 — Physical behaviours — **MUST**

V1 shall demonstrate at least five distinguishable physical motion patterns, including equivalents of:

1. attentive/perked response;
2. startled recoil;
3. controlled relaxation/settle;
4. excited physical response;
5. hesitation/curiosity movement.

They do not have to be identifiable with the screen disabled.

Their physical contribution must simply be visibly meaningful to the complete expression.

---

### C3-R69 — Multimodal emotional behaviours — **MUST**

At least three behaviours shall combine:

**face + head + physical locomotion/body response.**

For example:

**Curiosity**

```text
eyes orient
    ↓
head tilts
    ↓
subtle forward movement / optional torso lean
    ↓
settle
```

**Surprise**

```text
eyes widen
    ↓
head recoils
    ↓
base retreats slightly
    ↓
head rebounds
    ↓
settle
```

**Excitement**

```text
face perks
    ↓
quick short roll
    ↓
head lags
    ↓
small overshoot
    ↓
springy settle
```

---

# 3.27 Acceptance tests

## AT-C3-01 — Expressive repertoire

Execute the five required physical behaviours repeatedly.

**PASS:** all five contain deliberate and materially different physical motion.

---

## AT-C3-02 — Multimodal coordination

Execute at least three coordinated face/head/body/base expressions.

**PASS:** timing is intentionally synchronized rather than independent subsystem triggering.

---

## AT-C3-03 — Smooth trajectory

Execute slow, normal and fast representative movements.

**PASS:**

* no visible position stepping;
* no discontinuous command jumps;
* no uncontrolled oscillation;
* no abrupt unintended stop.

---

## AT-C3-04 — Preemption

Start an idle expressive trajectory and interrupt it midway with a higher-priority attentive command.

**PASS:** Makad transitions from its current physical state without completing the irrelevant original animation and without visible discontinuity.

---

## AT-C3-05 — Feedforward anticipation

Command a planned braking or start manoeuvre containing an anticipatory character animation.

**PASS:** the anticipatory motion begins according to the planned timeline **before physical acceleration feedback alone could have triggered it**.

---

## AT-C3-06 — Counter-motion scaling

Execute at least three base-motion intensities.

**PASS:** character counter-motion scales meaningfully with locomotion intensity rather than using an identical response.

---

## AT-C3-07 — Motion-style variation

Execute the same broad locomotion action using at least three behavioural styles.

**PASS:** they differ visibly through trajectory parameters without requiring different hardware.

---

## AT-C3-08 — Counter-motion settling

Using the standardized hard-braking profile later defined by Spec 16:

After the authored settle phase completes:

**MUST:**

* final head orientation reaches within approximately **±1°** of intended pose within **500 ms**;
* subsequent uncommanded oscillation remains below approximately **1° peak-to-peak**.

**TARGET:**

* ≤0.5° residual oscillation;
* settled within approximately 300 ms.

---

## AT-C3-09 — Structural resonance

Measure the dominant flexible response of the assembled head/neck/body structure using an appropriate test method.

**PASS:** normal expressive trajectories maintain acceptable separation from the significant structural resonance according to C3-R47.

**TARGET:** first significant mode approximately ≥15–20 Hz.

---

## AT-C3-10 — Dynamic stability

Execute the final standardized Spec-16 combinations of:

* forward acceleration;
* forward braking;
* reverse movement;
* turning;
* representative head movement;
* maximum permitted torso lean if installed.

**PASS:** no:

* wheel lift;
* caster lift beyond harmless transient contact variation;
* tipping tendency;
* unstable oscillation.

---

## AT-C3-11 — Neck/enclosure interference

With final shell/covers/wiring installed, move through all required individual and compound joint extremes.

**PASS:**

* no collision;
* no cable pinch;
* no unexpected ROM loss;
* no wire acting as travel stop.

---

## AT-C3-12 — Locomotion/audio compatibility

Run Makad at the normal drive condition later defined by Spec 16 while performing the Spec-4 voice-input acceptance test.

**PASS:** speech interaction remains within the required Spec-4 performance envelope.

---

## AT-C3-13 — Torso upgrade provision

Before final chassis CAD sign-off, inspect the reserved body-to-base interface.

**PASS:** the reserved:

* fastener interface;
* pivot volume;
* actuator/transmission volume;
* cable routing;
* shell clearance

can reasonably accommodate the planned 1-DOF torso-pitch module without major chassis redesign.

---

### Additional tests if torso pitch is installed

## AT-C3-14 — Torso range

**PASS:**

* ≥12° total usable travel;
* ≥5° each side of neutral.

---

## AT-C3-15 — Torso backlash

Approach the same output pose from opposing directions.

[
Backlash \le 25%A_{min}
]

At current (A_{min}=4°):

**PASS: ≤1°**

---

## AT-C3-16 — Torso repeatability

Repeatedly command selected forward, neutral and backward poses.

**TARGET:** approximately ±1° final orientation repeatability or better.

---

## AT-C3-17 — Torso obstruction

Prevent motion under controlled conditions.

**PASS:** controller detects abnormal movement/loading and prevents indefinite high actuator effort.

---

## AT-C3-18 — Torso endurance

Prototype:

**1,000 cycles**

Target mechanism:

**5,000 cycles**

**PASS:** no unacceptable mechanical, electrical or wiring degradation.

---

# 3.28 Scope table

| Requirement                                 | Scope                |
| ------------------------------------------- | -------------------- |
| Coordinated head + base physical expression | **MUST**             |
| Planned-trajectory feedforward              | **MUST**             |
| Anticipation before base movement           | **MUST**             |
| Acceleration/braking counter-motion         | **MUST**             |
| Controlled overshoot and settling           | **MUST**             |
| Emotion-dependent motion styles             | **MUST**             |
| Motion-intensity scaling                    | **MUST**             |
| Unified motion composer                     | **MUST**             |
| Preemptible trajectories                    | **MUST**             |
| Structural resonance separation             | **MUST**             |
| Dynamic stability validation                | **MUST**             |
| Full enclosure/neck clearance               | **MUST**             |
| Differential wheel odometry                 | **MUST**             |
| Indoor-floor design assumption              | **MUST**             |
| Front passive caster baseline               | **MUST**             |
| Reverse speed/acceleration restriction      | **MUST**             |
| Audio compatibility while driving           | **MUST**             |
| Manual charging                             | **MUST**             |
| Dock-ready rear mechanical zone             | **MUST**             |
| Cliff/drop-off protection                   | **MUST**             |
| Torso-pivot-compatible base interface       | **MUST**             |
| Powered torso pitch                         | **TARGET**           |
| ~±8–10° torso range                         | **TARGET**           |
| ~±1° torso repeatability                    | **TARGET**           |
| Persistent expressive posture offsets       | **TARGET**           |
| Camera/gaze compensation during body motion | **TARGET**           |
| ≥15–20 Hz first significant structural mode | **TARGET**           |
| 5,000-cycle torso mechanism endurance       | **TARGET**           |
| Autonomous charging dock                    | **STRETCH**          |
| Powered torso roll                          | **STRETCH / not V1** |
| Powered torso yaw                           | **STRETCH / not V1** |
| Dynamic balancing                           | **OUT OF SCOPE**     |
| Deliberate wheel lifting                    | **OUT OF SCOPE**     |

---

# 3.29 System decisions created by Spec 3

These are now considered **locked assumptions for later specs unless testing forces revision**.

### SD-C3-01 — Operating environment

Makad is primarily an **indoor floor robot**, not a table-roaming robot.

### SD-C3-02 — Drive geometry

Baseline architecture:

**two encoder-equipped driven wheels + passive front caster.**

### SD-C3-03 — Torso architecture

Powered torso pitch remains desirable but is **TARGET**.

The chassis must nevertheless preserve its mechanical upgrade path.

### SD-C3-04 — Motion architecture

Character motion uses both:

**planned-motion feedforward + measured-state feedback.**

### SD-C3-05 — Character locomotion

Acceleration, braking and turning are expressive animation inputs, not merely transportation events.

### SD-C3-06 — Charging

Manual charging is required.

Mechanical provision for a future charging dock is required.

Autonomous docking is not.

### SD-C3-07 — Navigation boundary

Wheel odometry is required.

Full SLAM is not implied.

---

# 3.30 Cross-spec industrial-design note

The reference Makad body establishes a design-language requirement that will be formally owned by the later chassis/enclosure specification:

> **Makad shall use an angular, faceted, mechanically assembled droid-like enclosure language rather than a simple rectangular box, cylinder, or smooth consumer-electronics shell.**

The exact number and angles of facets are **not** prescribed.

The eventual enclosure spec must reconcile this design language with:

* FDM manufacturing;
* panel alignment;
* serviceability;
* fastener placement;
* camera/audio openings;
* wheel clearance;
* charging/docking geometry;
* neck ROM;
* moving-joint gaps.

---

# Final Spec 3 outcome

The important architectural picture is now:

```text
                   FACE / EYES
                       │
                       ↓
                ┌─────────────┐
                │    HEAD     │
                └──────┬──────┘
                       │
                 SPEC 2 NECK
                       │
              ┌────────┴────────┐
              │ FACETED RIGID   │
              │   UPPER BODY    │
              └────────┬────────┘
                       │
          ┌────────────┴────────────┐
          │ BODY-TO-BASE INTERFACE  │
          │                         │
          │ rigid in base V1        │
          │ pitch-capable by design │
          └────────────┬────────────┘
                       │
              DIFFERENTIAL BASE

            DRIVE WHEEL       DRIVE WHEEL
                 O──────────────O
                        \
                         o
                   FRONT CASTER
```

Controlled by:

```text
                     BEHAVIOUR
                         │
                         ↓
                 MOTION COMPOSER
                         │
       planned base trajectory/feedforward
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
        FACE            HEAD           BASE
          ↑              ↑              ↑
          └────── measured feedback ────┘

        anticipation → action → lag →
        overshoot → controlled settle
```

That is the **final Spec 3** I would carry forward.

The major thing we deliberately did **not** decide is whether the torso actuator actually gets installed. Everything else now ensures that if we later decide it is worth the extra complexity, we haven't already designed ourselves into a corner.
