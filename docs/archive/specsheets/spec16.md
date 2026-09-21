# MAKAD — SPEC-16  
## Autonomous Differential-Drive Locomotion

**Status:** Revised engineering specification  
**Revision:** Safety-path, expressive-locomotion, IMU, audio-motion, sensing, caster, and surface amendments incorporated  
**Subsystem:** Mobile base / drive system

**Revision notation:** Existing text is preserved unless explicitly marked **AMENDED**. Newly appended requirements and tests are marked **NEW**. Existing requirement and test IDs are not renumbered.

---

# 1. Scope of this specification

SPEC-16 defines the engineering requirements for converting Makad from a stationary companion into a **stable, controllable, locally autonomous mobile robot**.

It covers:

- the two-wheel differential-drive architecture;
- the passive third support point;
- wheel/base geometry insofar as it affects locomotion;
- static and dynamic stability;
- wheel traction;
- translational and rotational performance;
- motor/gearbox sizing criteria;
- wheel encoders;
- wheel-speed control;
- differential-drive kinematics;
- wheel odometry;
- acceleration, braking and reversal behaviour;
- autonomous motion safety;
- authoritative short-range ToF/proximity collision sensing;
- obstacle/cliff interaction insofar as locomotion depends on it;
- low-level obstacle-recovery motion;
- person-following and body-orientation interfaces;
- IMU-supported motion-state and pickup/tip detection;
- motor electrical/power requirements;
- locomotion-related vibration and acoustic effects;
- locomotion/audio coordination;
- fault handling and motor inhibition;
- calibration and diagnostic outputs;
- interfaces to perception, head motion, audio, power and the later behaviour architecture.

This specification **does not** define:

- exact wheel diameter;
- exact track width;
- exact gearmotor;
- exact motor driver;
- exact ToF/proximity sensor model;
- exact caster model;
- final battery;
- global mapping or autonomous room navigation;
- SLAM;
- global path planning;
- person/face detection itself;
- final attention arbitration between face, head, audio and body;
- the exact high-level behaviour engine;
- the expressive motion library itself.

### Expressive-locomotion scope boundary — NEW

Locomotion is not treated only as transport. Whole-body approach, retreat, orientation, hesitation and small repositioning can carry social meaning that eyes and neck motion alone cannot.

However, the **authored expressive motion library** belongs to the expression/behaviour specification lineage, including SPEC-12 and its downstream integration work.

SPEC-16 owns only the locomotion-side interfaces and physical/control properties required for expressive motion to be executed safely and smoothly.

Mobility sophistication remains subordinate to Makad's central product objective of coordinated face, gaze, head, audio and whole-body aliveness.

---

# 2. Existing Makad decisions that constrain this spec

## 2.1 Drive architecture is fixed

Makad V1 will use:

**two independently driven wheels + one passive support element.**

The two powered wheels will be encoder-equipped and operated as a differential-drive pair.

This is not a two-wheeled self-balancing robot.

No active balancing controller, reaction wheel, spherical BB-8 mechanism or dynamically unstable chassis is required.

The current baseline remains a three-contact architecture.

A dual-caster alternative may be evaluated during CAD because it improves fore/aft tip margin, but selecting it would be an explicit architecture deviation rather than a silent change to the current decision.

---

## 2.2 Stability is mechanical

Makad will remain standing because its two wheel contact patches and passive caster create a **three-point support polygon**.

The chassis therefore has to be designed so that Makad's centre of mass remains safely inside that support polygon.

The high and movable head makes this particularly important.

---

## 2.3 Required motion behaviours

The base has to support at least:

- forward travel;
- backward travel;
- curved/arcing travel;
- near-zero-radius rotation;
- turning Makad's whole body toward a person;
- approaching a person;
- slowly following a person;
- backing away;
- local roaming;
- small repositioning movements.

Expressive motions such as cautious approaches, little retreats, wiggles or short body turns are allowed where they naturally fall out of the locomotion system, but they do not justify additional locomotion hardware.

---

## 2.4 Head motion remains separate from base motion

Makad has a mechanically actuated head.

The base therefore must not rotate every time Makad merely wants to look sideways.

The behaviour system will eventually choose between:

- eyes only;
- head motion;
- whole-body rotation;
- combinations of them.

SPEC-16 only provides the base capability needed for that coordination.

---

## 2.5 Person tracking already belongs upstream

The moving-camera/person-tracking work established elsewhere must generate calibrated target direction information.

Wheel control must **not use raw camera pixels, bounding-box centre coordinates or face detector coordinates directly**.

The mobile base consumes body-relative motion objectives generated from properly transformed perception information.

---

## 2.6 Perception range is not collision-safety range — AMENDED

Any coarse person-range estimate used by the visual tracking system may be sufficient for behaviours such as deciding whether Makad should move closer.

It is **not safety-grade obstacle ranging**.

The authoritative local collision-safety layer for SPEC-16 is therefore short-range **ToF/proximity sensing**, with the camera serving an advisory/contextual role only.

Camera perception may help classify what stopped Makad or provide behaviour context, but it may not by itself authorise a clear-path decision.

---

## 2.7 V1 does not require SLAM

The development path remains approximately:

**manual controlled movement → safe local autonomous movement → obstacle avoidance → person following → expressive/local roaming.**

Global mapping and SLAM are not prerequisites for SPEC-16 V1.

---

## 2.8 The body contains sensitive audio hardware — AMENDED

The accepted audio architecture uses four MEMS microphones in the body.

Drive motors, gearboxes and wheels are therefore potential sources of:

- structure-borne vibration;
- electrical interference;
- acoustic motor/gear noise.

In addition, once Makad rotates its body, the microphone array is no longer stationary in the external world frame.

Persistent DOA/source tracks therefore require body-yaw ego-motion information from SPEC-16.

---

# 3. Engineering reasoning / architecture

## 3.1 Why differential drive is appropriate

For wheel linear velocities \(v_R\) and \(v_L\), separated by wheel track \(b\):

\[
v=\frac{v_R+v_L}{2}
\]

\[
\omega=\frac{v_R-v_L}{b}
\]

where:

- \(v\) = base forward velocity;
- \(\omega\) = base yaw rate.

Therefore:

### Straight forward/backward

\[
v_R=v_L
\]

### Curved motion

\[
v_R\neq v_L
\]

### Near in-place rotation

\[
v_R=-v_L
\]

This gives all of Makad's intended planar movement with only two actuators.

---

## 3.2 Why the caster matters more than it appears

The caster is not merely something added to prevent Makad falling over.

Its position and type determine:

- support polygon;
- front/rear tip resistance;
- drive-wheel loading;
- traction;
- turning resistance;
- reversing behaviour;
- threshold traversal;
- vibration;
- acoustic character.

A swivel caster can produce a characteristic flip/jerk when motion reverses.

That is particularly relevant because frequent small reversals are expected in Makad's expressive motion.

Caster configuration is therefore a **CAD-time locomotion decision**, not a decorative afterthought.

---

## 3.3 Static stability

Let:

- \(d\) = shortest horizontal distance from the COM projection to a relevant tipping edge;
- \(h\) = COM height above the floor.

An approximate acceleration at which tipping begins is:

\[
a_{tip}\approx g\frac{d}{h}
\]

Makad's worst-case stability calculation must include:

- head yaw;
- head pitch;
- battery location;
- caster position;
- actual electronics/wiring;
- asymmetric internal mass.

---

## 3.4 Traction

For translational acceleration:

\[
F_{req}\approx ma+mgC_{rr}+mg\sin\theta
\]

For two similarly loaded drive wheels:

\[
\tau_{wheel}\approx\frac{F_{req}r}{2\eta}
\]

where:

- \(r\) = drive-wheel radius;
- \(\eta\) = drivetrain efficiency.

For yaw acceleration:

\[
M_z=I_z\alpha_z
\]

and approximately:

\[
F_{wheel}\approx\frac{M_z}{b}
\]

\[
\tau_{wheel,turn}\approx
\frac{I_z\alpha_zr}{b\eta}
\]

---

## 3.5 Traction may limit acceleration before torque does

Available drive force is approximately:

\[
F_{traction,max}=\mu N_{drive}
\]

A larger motor does not improve acceleration once wheel slip begins.

---

## 3.6 Speed philosophy — AMENDED

Makad is not intended to be a fast delivery robot.

Its locomotion exists primarily for:

- social positioning;
- following;
- whole-body orientation;
- retreat;
- expressive movement;
- local exploration.

A useful preliminary floor-operation design envelope remains approximately:

- **precision/crawl:** ~0.03–0.06 m/s;
- **ordinary autonomous motion:** ~0.10–0.25 m/s;
- **upper V1 floor-only region:** ~0.30–0.40 m/s;
- **ordinary body rotation:** roughly 45–120°/s.

Elevated-surface motion does **not** inherit the 0.30–0.40 m/s upper region.

Its speed is independently limited by available distance to an edge and the validated hazard-response path.

---

## 3.7 Safety latency dominates braking distance — AMENDED

The collision-safety relationship is:

\[
d_{available}>
v\,t_{latency}
+
\frac{v^2}{2a_{brake}}
+
d_{margin}
\]

where:

- \(d_{available}\) = validated free distance available to the safety system;
- \(t_{latency}\) = complete hazard-detection-to-deceleration latency;
- \(a_{brake}\) = validated achievable braking deceleration;
- \(d_{margin}\) = safety allowance for uncertainty and variation.

For an illustrative tip-limited braking value of approximately:

\[
a_{brake}\approx2\,m/s^2
\]

the relationship is approximately:

| Speed | Pure braking distance | Travel during 250 ms latency |
|---|---:|---:|
| 0.10 m/s | 0.25 cm | 2.5 cm |
| 0.25 m/s | 1.56 cm | 6.25 cm |
| 0.40 m/s | 4.0 cm | 10.0 cm |

Across the V1 envelope, latency travel is therefore roughly four times the ideal braking distance.

The important conclusion is:

> **For Makad's intended speeds, safe speed is primarily constrained by the sensing/software safety path rather than drivetrain braking capability.**

Therefore collision and cliff inhibition cannot depend on an arbitrarily delayed SBC behaviour pipeline.

---

## 3.8 Encoders are for control and relative motion—not magic localisation

Wheel encoders provide:

- direction;
- displacement;
- wheel speed;
- relative odometry.

They remain blind to several important physical states.

If a wheel is slipping, its encoder can agree perfectly with the commanded wheel velocity while the chassis fails to move as expected.

The IMU added by this revision therefore provides an independent motion/orientation source.

---

## 3.9 Closed-loop velocity control is necessary

The hierarchy remains:

**behaviour command**

→ desired base motion

→ expressive contribution

→ summed command

→ safety/limit clamp

→ differential-drive conversion

→ wheel targets

→ low-level wheel controllers

→ motor output

→ encoders/IMU feedback.

The **ordering is deliberate**.

Safety clamps act after expressive blending.

---

## 3.10 Near-in-place rotation and footprint geometry — AMENDED

A differential-drive robot normally sweeps a changing polygon during body rotation.

SPEC-16 now constrains the lower base footprint to lie within a circle centred on the drive-wheel axle midpoint.

This produces an orientation-invariant floor-level collision footprint.

The head remains an explicit exception because body rotation can swing the head/ears through an upper radius not covered by floor-level sensors.

---

## 3.11 Safety authority

High-level commands such as:

> follow person

or:

> perform curious approach

shall never override low-level safety.

The safety hierarchy is:

**high-level intent / expression**

→ motion blend

→ safety clamp/inhibit

→ drivetrain.

---

## 3.12 Authoritative obstacle sensing — NEW

Short-range **ToF/proximity sensing** is the authoritative local collision-safety layer.

The camera is advisory because camera-derived clearance generally passes through:

- image acquisition;
- detection;
- tracking;
- semantic processing;
- high-level compute scheduling.

Those latencies cannot be guaranteed tightly enough for the deterministic local inhibit required by SPEC-16.

The camera may still provide:

- obstacle class;
- semantic context;
- behavioural interpretation;
- recovery context.

It may **not** be the sole reason a region is considered safe to enter.

---

## 3.13 Obstacle recovery — NEW

A local obstacle encounter must not reduce Makad permanently to:

> detect → stop forever.

The default local recovery sequence is:

**stop → bounded retreat → turn → resume/re-evaluate.**

Because the retreat enters space that was not necessarily observed during the original forward approach, reverse movement is deliberately conservative.

Unless rear ToF coverage is installed and validated, the default retreat target begins at approximately:

\[
0.10\,m
\]

at crawl speed.

The value is **TARGET — provisional pending prototype geometry and stopping tests.**

Recovery itself belongs below the high-level behavioural process so that a temporary SBC/behaviour failure cannot strand the safety state midway through a manoeuvre.

---

## 3.14 Expressive command blending — NEW

The required command order is:

**behaviour intent**

\[
+
\]

**expressive motion contribution**

\[
\downarrow
\]

**summed \(v,\omega\) command**

\[
\downarrow
\]

**velocity / acceleration / obstacle / cliff safety clamp**

\[
\downarrow
\]

**differential-drive conversion**

\[
\downarrow
\]

**wheel velocity targets**

An implementation that clamps the behaviour command and then adds expressive velocity afterward is non-conforming.

Otherwise the expressive layer could accidentally restore velocity above a previously applied safety limit.

---

## 3.15 Startle behaviour — NEW

A startle motion may need to feel fast, but this does not justify a blind high-speed reverse.

The locomotion-side interpretation of startle is therefore:

**rapid controlled deceleration to zero.**

The immediate intensity is carried by:

- head recoil;
- eyes;
- audio;
- other expressive channels.

Any physical retreat occurs only afterward using normal bounded reverse behaviour and ordinary reverse safety rules.

---

## 3.16 Encoder resolution reference calculation — NEW

At:

\[
v=0.05\,m/s
\]

\[
r=0.03\,m
\]

\[
f_c=50\,Hz
\]

the wheel completes per control interval:

\[
\Delta n=
\frac{v}{2\pi r f_c}
\]

\[
\Delta n\approx
\frac{0.05}{2\pi(0.03)(50)}
\approx0.0053
\]

wheel revolutions.

For approximately ten encoder counts per interval:

\[
CPR_{wheel}\approx\frac{10}{0.0053}
\approx1900
\]

effective counts per wheel revolution.

A low-resolution motor-side quadrature encoder behind a high-ratio gearbox can therefore provide several thousand effective wheel counts/revolution.

For example, an approximately 11-cycle/rev quadrature encoder counted on four edges behind approximately 100:1 reduction corresponds to roughly:

\[
11\times4\times100\approx4400
\]

effective counts per wheel revolution.

The architectural consequence for V1 is that **motor-side encoding behind substantial reduction is preferred/required for the baseline drivetrain architecture**, and gearbox backlash/deadband becomes more important than raw count availability.

---

## 3.17 IMU role — NEW

A rigidly mounted six-axis IMU provides:

- pickup/lift detection;
- tip/fall orientation detection;
- yaw-rate observation;
- short-horizon heading assistance;
- encoder/IMU consistency checking;
- stuck/motion-anomaly evidence.

It does **not** make arbitrary sustained translational slip perfectly observable.

The correct claim is therefore motion-anomaly detection, not universal slip estimation.

---

## 3.18 Body rotation and audio — NEW

The microphone array remains mechanically rigid relative to the speaker and body, so its internal echo geometry remains comparatively stable.

However, the array rotates relative to the world.

A sound-source bearing measured at time \(t_0\) therefore requires timestamped body-yaw information if it is to remain meaningful during later body motion.

Structure-borne gearmotor vibration is a separate problem.

Because it can reach several capsules almost coherently and without the propagation structure of a far-field plane wave, beamforming is not a reliable primary mitigation.

The relevant mitigations are:

- mechanical isolation;
- drivetrain acoustic quality;
- motion inhibition during important listening intervals.

---

## 3.19 Zero-velocity hold — NEW

When Makad commands zero base velocity, the chassis must not behave as a free coasting platform.

Head yaw acceleration generates reaction torque on the body.

If the base yields visibly in the opposite direction, expressive head motion becomes physically incoherent.

The drivetrain therefore needs a defined stationary-hold behaviour.

---

# 4. Formal requirements

## 4.1 Fundamental architecture

### C16-R01 — MUST-HAVE
Makad V1 shall use exactly **two independently powered primary drive wheels** for planar locomotion.

### C16-R02 — MUST-HAVE
Both primary drive wheels shall provide encoder feedback sufficient to determine wheel displacement, velocity and direction.

### C16-R03 — MUST-HAVE
Makad shall use a passive third support point, such as an appropriate caster mechanism, creating mechanically stable three-point ground support.

### C16-R04 — MUST-HAVE
Makad shall not require active self-balancing to remain upright while stationary or moving within its validated operating envelope.

### C16-R05 — MUST-HAVE
The drivetrain shall permit:

- forward motion;
- reverse motion;
- differential-radius turns;
- near-in-place yaw rotation.

### C16-R06 — MUST-HAVE
Left and right wheel velocity shall be independently commandable in both directions.

### C16-R07 — MUST-HAVE
The drive geometry shall expose calibrated values for at least:

\[
r_L,\quad r_R,\quad b
\]

representing effective left/right wheel radii and effective wheel track.

Nominal CAD dimensions alone shall not be assumed equal to calibrated kinematic values.

---

## 4.2 Mechanical integration and stability

### C16-R08 — MUST-HAVE
The drive wheels and caster shall create a deterministic three-point support polygon without requiring four-point coplanarity or chassis flex to avoid rocking.

### C16-R09 — MUST-HAVE
The completed Makad COM projection shall remain within the support polygon throughout every permitted combination of:

- head yaw;
- head pitch;
- stationary base orientation;
- normal installed battery state;
- complete electronics/wiring configuration.

### C16-R10 — MUST-HAVE
The shortest COM-to-tipping-edge distance \(d_{min}\) and COM height \(h\) shall be determined from the assembled CAD mass model and validated on the physical robot.

### C16-R11 — MUST-HAVE
Maximum commanded translational and rotational accelerations shall be constrained using the measured or calculated worst-case tipping limit rather than being chosen independently of chassis geometry.

For fore/aft acceleration, the first-order relationship:

\[
a_{tip}\approx g\frac{d}{h}
\]

shall be evaluated.

### C16-R12 — TARGET
Normal operational acceleration shall retain approximately **2× margin to the experimentally established tipping acceleration** under the worst validated head pose and travel direction.

Final factor is subject to prototype validation.

### C16-R13 — MUST-HAVE
Drive-wheel normal loading shall be sufficient that required drive force remains below available wheel-floor traction throughout the validated acceleration envelope.

The design shall verify:

\[
F_{required}<\mu N_{drive}
\]

with an appropriate margin.

### C16-R14 — TARGET
Caster loading and location shall be chosen to minimise rolling resistance and caster instability while retaining adequate drive-wheel traction.

No universal caster weight percentage is frozen before the mass model exists.

### C16-R15 — MUST-HAVE
No permitted head position shall cause a powered wheel to unload sufficiently to create unreliable traction during normal operation.

### C16-R16 — MUST-HAVE
Wheel/caster mounts shall maintain wheel alignment sufficiently that structural flex is not the dominant source of straight-line tracking error.

### C16-R17 — TARGET
Ground clearance and caster/wheel geometry shall tolerate ordinary indoor floor joints and small discontinuities without the chassis bottoming out.

Maximum traversable discontinuity remains pending final wheel/caster geometry.

### C16-R18 — MUST-HAVE
The locomotion design shall avoid accessible wheel/body gaps that create an obvious finger, wire or clothing pinch/snare hazard during ordinary operation.

### C16-R19 — MUST-HAVE
Wheel guards, body panels or decorative structures shall not contact tyres throughout wheel runout, chassis flex and permitted assembly tolerances.

---

## 4.3 Drive sizing and performance

### C16-R20 — MUST-HAVE
Motor and gearbox sizing shall use calculated **wheel torque requirements** rather than selecting an actuator solely from advertised stall torque.

The translational sizing calculation shall include at minimum:

\[
F\approx ma+mgC_{rr}+mg\sin\theta
\]

followed by:

\[
\tau_{wheel}\approx\frac{Fr}{2\eta}
\]

or a more complete equivalent model.

### C16-R21 — MUST-HAVE
Rotational drivetrain sizing shall also evaluate complete-robot yaw inertia \(I_z\), desired yaw acceleration \(\alpha_z\), track width and wheel radius.

### C16-R22 — MUST-HAVE
Continuous operating torque and thermal limits shall be evaluated separately from short-duration peak/stall capability.

### C16-R23 — MUST-HAVE
The selected transmission shall support repeated forward/reverse operation without requiring abrupt motor reversal at full output.

### C16-R24 — TARGET — AMENDED
The mechanical/electrical drive system should support stable commanded translational motion at approximately **0.05 m/s or lower** so that Makad can perform short, cautious approaches and repositioning manoeuvres.

This minimum controllable speed is an **expressive-character acceptance criterion as well as a control criterion**.

A drivetrain that technically tracks average velocity but visibly produces repeated stop-jerk-move behaviour during hesitant approaches, cautious retreats or small body gestures shall not satisfy the intent of this requirement.

This remains a prototype-validation target because encoder resolution, gearbox stiction and motor control strongly influence it.

### C16-R25 — TARGET
A preliminary normal autonomous speed envelope of approximately **0.10–0.25 m/s** shall be used for motor and sensing architecture studies.

### C16-R26 — TARGET — AMENDED
The architecture should retain the capability for an upper V1 translational limit in approximately the **0.30–0.40 m/s** region **for floor-level operation only**, if stability and obstacle-sensing tests support it.

Makad is not required to operate at this speed autonomously.

Elevated-surface speed shall be independently constrained from measured usable approach distance, hazard latency and braking performance and shall not inherit this upper envelope.

### C16-R27 — TARGET
Normal body-yaw manoeuvres should support approximately **45–120°/s** so that a body-turn toward a person does not feel excessively slow.

Final maximum yaw velocity shall depend on tip margin, traction, camera operation and character animation.

### C16-R28 — MUST-HAVE
Maximum translational and angular velocities shall be software configurable and independently clampable.

### C16-R29 — MUST-HAVE
Acceleration and deceleration shall be bounded rather than allowing full-scale step changes in wheel velocity.

### C16-R30 — TARGET
The base controller should support configurable jerk/trajectory shaping where required to prevent visibly harsh starts, stops or reversals.

This shall not require a complex research-grade trajectory optimizer.

### C16-R31 — MUST-HAVE
A commanded change from forward motion to reverse motion shall pass through a controlled deceleration/near-zero-speed region rather than immediately commanding full opposite drive.

### C16-R32 — MUST-HAVE — AMENDED
Safe autonomous velocity shall satisfy:

\[
d_{available}>
v\,t_{latency}
+
\frac{v^2}{2a_{brake}}
+
d_{margin}
\]

where:

- \(d_{available}\) is the validated hazard-detection distance available in the commanded swept path;
- \(t_{latency}\) is worst-case end-to-end hazard-detection-to-deceleration latency;
- \(a_{brake}\) is validated achievable braking deceleration;
- \(d_{margin}\) is additional safety margin.

Maximum autonomous speed shall be reduced whenever this inequality cannot be satisfied.

---

## 4.4 Wheel sensing and calibration

### C16-R33 — MUST-HAVE
Each driven wheel shall provide independent encoder counts or equivalent wheel-motion measurements.

### C16-R34 — MUST-HAVE
The encoder system shall preserve rotation direction information.

### C16-R35 — MUST-HAVE — AMENDED
The baseline V1 drivetrain architecture shall use **motor-side encoding combined with sufficient gearbox reduction** to provide useful effective wheel-resolution for low-speed control.

For the current reference case:

- \(v=0.05\,m/s\);
- \(r=0.03\,m\);
- control rate = 50 Hz;

the wheel rotates approximately 0.0053 revolutions/control interval.

Approximately ten counts per control interval therefore corresponds to approximately **1900 effective counts per wheel revolution**.

An approximately 11-cycle/rev quadrature encoder counted on four edges behind approximately 100:1 reduction would provide approximately 4400 effective counts/revolution.

Exact encoder and reduction values remain component-selection decisions, but the architecture shall provide resolution in this practical regime.

Minimum controllable velocity and visible smoothness remain the acceptance criteria; raw encoder CPR alone is insufficient.

### C16-R36 — MUST-HAVE — AMENDED
Because the baseline encoder is motor-side of the gearbox, gearbox backlash/deadband shall be characterised during reversals because encoder motion may precede or differ from actual wheel motion.

This characterisation is an **expressive-quality criterion**, not only an odometry criterion.

The selected drivetrain shall permit small repeated directional changes, hesitant approaches and expressive wiggles without dominant visible deadband, stop-jerk motion or uncontrolled reversal delay.

For drivetrain selection, backlash/deadband is therefore expected to be more binding than raw encoder resolution once C16-R35 is satisfied.

### C16-R37 — MUST-HAVE
Wheel state measurements exposed beyond the low-level controller shall be timestamped.

### C16-R38 — MUST-HAVE
Makad shall provide a calibration procedure for effective:

- left wheel radius;
- right wheel radius;
- wheel track.

### C16-R39 — MUST-HAVE
Calibration constants shall be persistently stored rather than hard-coded throughout unrelated behaviour software.

### C16-R40 — TARGET
After calibration on the intended indoor surface, a commanded straight-line traverse of 1 m should achieve:

- longitudinal distance error ≤5%; and
- lateral deviation ≤50 mm

under controlled test conditions.

This is a TARGET for useful local odometry, not a safety or global-localisation claim.

### C16-R41 — TARGET
After calibration, encoder-based in-place turning should achieve a commanded 360° rotation with final heading error within approximately ±10° on a representative hard indoor surface.

This target exists to make short body-orientation/repositioning useful; long-term heading accuracy is not implied.

---

## 4.5 Low-level control

### C16-R42 — MUST-HAVE
Each drive wheel shall operate under closed-loop velocity control using its encoder feedback.

Open-loop PWM alone shall not constitute normal autonomous drive control.

### C16-R43 — MUST-HAVE
The low-level controller shall independently compensate for left/right motor and drivetrain differences rather than assuming equal PWM produces equal speed.

### C16-R44 — MUST-HAVE
The base-motion interface shall support a planar command equivalent to:

\[
(v,\omega)
\]

where:

- \(v\) = commanded forward velocity;
- \(\omega\) = commanded yaw velocity.

### C16-R45 — MUST-HAVE
The drive controller shall convert \(v,\omega\) into left/right wheel targets according to calibrated differential-drive geometry.

### C16-R46 — MUST-HAVE
If a requested \(v,\omega\) combination exceeds a wheel-speed or motor limit, the controller shall perform deterministic command saturation while preserving the intended curvature as closely as practical.

### C16-R47 — TARGET
The closed-loop wheel velocity/controller state should execute at **≥50 Hz**.

This corresponds to a ≤20 ms control interval and is sufficient as an initial V1 target for a slow indoor robot while remaining easy to implement on ordinary embedded hardware.

### C16-R48 — MUST-HAVE
High-level command interruption or loss shall cause the base controller to enter a controlled stop rather than indefinitely continuing the previous velocity command.

### C16-R49 — TARGET
The command watchdog should normally be configured to detect loss of active motion command within **≤250 ms**, subject to final communications architecture and stopping-distance analysis.

This watchdog is distinct from the much faster local hazard-response path defined later in this specification.

### C16-R50 — MUST-HAVE
On startup, reboot or communications reconnection, motor output shall default to a non-moving state.

### C16-R51 — MUST-HAVE
Makad shall provide a software-accessible **motor inhibit / motion disabled** state independent of normal behavioural velocity commands.

### C16-R52 — MUST-HAVE
There shall be a direct physical means of removing or disabling drive power without depending on the high-level software stack.

A normal accessible master/motor power mechanism can satisfy this; a large industrial emergency-stop assembly is not inherently required for Makad's scale.

---

## 4.6 Odometry

### C16-R53 — MUST-HAVE
The locomotion subsystem shall estimate relative planar wheel odometry comprising at least:

- \(x\);
- \(y\);
- yaw;
- translational velocity;
- angular velocity.

### C16-R54 — MUST-HAVE
Wheel odometry shall be explicitly treated as a **drifting relative estimate**, not absolute room localisation.

### C16-R55 — MUST-HAVE
Wheel odometry shall not be used as the sole evidence that the path ahead is collision-free.

### C16-R56 — TARGET
The odometry interface should expose an uncertainty, quality indicator or equivalent mechanism allowing higher-level software to recognise degraded confidence.

### C16-R57 — MUST-HAVE — STATUS CHANGED FROM STRETCH
Makad V1 shall include a rigidly mounted **6-axis IMU** providing accelerometer and gyroscope measurements.

The IMU shall support at least:

- pickup/lift detection;
- tip/fall orientation detection;
- short-term yaw-rate observation;
- encoder/IMU motion-consistency checking;
- stuck/motion-anomaly detection.

The IMU shall be available to improve short-term yaw estimation and may be fused with wheel odometry.

It shall not be claimed to make arbitrary sustained translational wheel slip fully observable.

---

## 4.7 Local autonomous safety

### C16-R58 — MUST-HAVE — AMENDED
Autonomous movement shall use **short-range ToF/proximity sensing as the authoritative local collision-safety layer** protecting the commanded direction and swept envelope of travel.

### C16-R59 — MUST-HAVE — AMENDED
The coarse range estimate associated with person tracking and camera-derived obstacle interpretation shall **not** be classified as the authoritative collision-safety distance signal.

Camera perception is advisory only for clear-path decisions.

Its legitimate roles include classification, semantic context and explanation of why a low-level safety stop occurred.

### C16-R60 — MUST-HAVE — AMENDED
Authoritative ToF/proximity coverage shall consider Makad's **swept body envelope**, not merely a ray through the centre of the robot.

Coverage shall include the hazards relevant to:

- forward translation;
- reverse translation;
- in-place rotation.

### C16-R61 — MUST-HAVE — AMENDED
Reverse autonomous movement shall use one of the following:

1. validated rearward ToF/proximity coverage; or
2. the bounded low-level recovery retreat defined in this specification.

Without validated rearward ToF coverage, normal-speed blind reversing is prohibited.

The default recovery retreat shall occur only at crawl speed and over a bounded distance before rotation/re-evaluation.

### C16-R62 — MUST-HAVE
Safe commanded speed shall decrease when the available obstacle-detection distance is insufficient to satisfy the stopping-distance inequality from C16-R32.

### C16-R63 — MUST-HAVE
A local collision-prevention stop/inhibit shall override ordinary commands such as:

- follow person;
- approach;
- roam;
- expressive reposition;
- body turn.

### C16-R64 — MUST-HAVE
Loss, invalidity or stale status of a safety-critical obstacle signal shall produce a defined degraded mode rather than silently being interpreted as "no obstacle."

### C16-R65 — TARGET
Contact/bump detection may be used as a last-resort collision layer, but shall not replace normal non-contact stopping where autonomous motion speed would make repeated collisions undesirable.

### C16-R66 — MUST-HAVE — AMENDED
If Makad is permitted to drive on a desk, table or other elevated surface, autonomous operation shall include validated edge/cliff protection integrated into the same low-level safety architecture.

The cliff-detection solution shall be validated across the **declared elevated-surface set**, including problematic dark/specular/transparent surfaces wherever those surfaces are claimed as supported.

A single optical reflectance modality shall not be assumed valid across unsupported surface classes without testing or compensating protection.

If validated cliff protection is not implemented, the autonomous operating domain shall be restricted to floor-level surfaces where falling from an edge is not credible.

### C16-R67 — MUST-HAVE
Locomotion faults shall cause safe stopping rather than uncontrolled continuation.

Relevant faults include at least:

- encoder failure/staleness;
- controller communication loss;
- motor-driver fault;
- persistent stall/overcurrent;
- contradictory wheel feedback.

---

## 4.8 Person following and perception interface

### C16-R68 — MUST-HAVE
Base steering toward a visually tracked person shall consume a **base/body-frame target direction or derived body-yaw objective**, not raw image coordinates.

### C16-R69 — MUST-HAVE
Camera/head pose compensation established by the perception subsystem shall be respected before target information is used for whole-body motion.

A head looking sideways must not be interpreted as the base itself being misaligned by an uncorrected camera pixel displacement.

### C16-R70 — MUST-HAVE
Person-following behaviour shall combine target-following commands with local locomotion safety constraints.

### C16-R71 — MUST-HAVE
Loss of the followed target shall not cause Makad to continue indefinitely along the last known trajectory.

The base shall slow/stop according to behaviour policy until target reacquisition or another deliberate command occurs.

### C16-R72 — MUST-HAVE
The person-following system may use non-safety coarse range information for social positioning, but collision avoidance shall retain independent authority.

### C16-R73 — TARGET
Person-following speed shall be intentionally lower than the maximum mechanical speed and suitable for Makad's companion behaviour.

Initial testing should therefore centre on approximately the normal 0.10–0.25 m/s region rather than attempting normal human walking speed.

### C16-R74 — MUST-HAVE
SPEC-16 shall expose body-rotation control suitable for higher-level behaviours such as "turn Makad's body toward this person" without requiring that SPEC-16 itself decide when eyes, head or body should move.

Final eye/head/body arbitration remains outside this specification.

---

## 4.9 Local roaming / navigation scope

### C16-R75 — MUST-HAVE
V1 autonomous roaming shall be implementable without SLAM or a persistent metric map.

### C16-R76 — MUST-HAVE
V1 roaming shall therefore be defined as **local reactive movement within an appropriate operating area**, including obstacle response and repositioning.

### C16-R77 — MUST-HAVE
Failure to implement SLAM shall not be treated as failure of SPEC-16.

### C16-R78 — STRETCH
Persistent mapping, global path planning and room-to-room autonomous navigation may later consume the same \(v,\omega\), odometry and safety interfaces.

They are explicitly outside the V1 acceptance boundary.

---

## 4.10 Power, motor electronics and thermal behaviour

### C16-R79 — MUST-HAVE
The complete power budget shall include simultaneous operation of both drive motors under expected peak acceleration/load.

### C16-R80 — MUST-HAVE
Motor-driver continuous and transient current capability shall be evaluated against the actual selected motors, including stall current.

### C16-R81 — MUST-HAVE
Motor current limiting/protection shall prevent a wheel jam from requiring the rest of Makad's electrical system to tolerate indefinite motor stall current.

### C16-R82 — MUST-HAVE
Drive-motor transients shall not cause the compute, microcontroller, display, camera or audio subsystem to reboot or enter undefined operation.

### C16-R83 — MUST-HAVE
Motor and logic power distribution shall include whatever rail separation, regulation, decoupling and grounding strategy is required to satisfy C16-R82.

Exact topology is deferred until the electrical architecture is designed.

### C16-R84 — MUST-HAVE
Battery placement shall be considered jointly with SPEC-16 stability calculations rather than optimised only for packaging convenience.

Where practical, heavier power components should contribute positively to low COM.

### C16-R85 — MUST-HAVE
Motor-driver and motor temperatures shall remain within component limits during the worst representative V1 movement duty cycle.

### C16-R86 — TARGET
A continuous mixed-motion endurance test of at least **15 minutes** without thermal shutdown or progressive drive degradation shall be used as an early subsystem target.

Longer whole-robot battery-runtime requirements belong to the system-level power budget.

---

## 4.11 Audio, camera and vibration interaction

### C16-R87 — MUST-HAVE — AMENDED
Drive motor/gearbox vibration shall be evaluated at the installed body microphone array rather than judged solely by whether the motors sound quiet externally.

Because structure-borne motor vibration may arrive at multiple capsules near-coherently and does not behave as a far-field directional source, **beamforming shall not be treated as the primary mitigation**.

Mitigation shall rely on drivetrain mechanical quality, mechanical isolation and/or locomotion inhibition during acoustically critical listening periods.

### C16-R88 — MUST-HAVE
Motor wiring, driver switching and grounding shall not introduce electrical interference that renders the body microphone array, camera or other sensors unreliable during movement.

### C16-R89 — MUST-HAVE — AMENDED
The locomotion subsystem shall expose timestamped state sufficient for other subsystems to know at least:

- whether the base is moving;
- commanded \(v,\omega\);
- measured wheel velocities;
- measured/estimated body yaw;
- measured/estimated yaw rate;
- significant motor/drive fault state;
- commanded translational acceleration for the upcoming control interval;
- commanded angular acceleration for the upcoming control interval.

The commanded acceleration values shall be published **at least one locomotion-control cycle ahead of their physical execution**, so head/expression systems can perform anticipatory counter-motion rather than purely reactive compensation.

### C16-R90 — TARGET — AMENDED
Audio processing may use wheel/base-motion state for quality gating, noise suppression or confidence reduction during acoustically difficult manoeuvres.

The system shall additionally support the listening-motion-inhibit interface defined later in this specification.

### C16-R91 — MUST-HAVE
Head/camera movement and base movement shall be allowed simultaneously; the locomotion subsystem shall not assume a stationary camera.

Capture-time pose handling remains the responsibility of the existing moving-camera perception architecture.

---

## 4.12 Diagnostics, assembly and maintainability

### C16-R92 — MUST-HAVE
Each drive motor/wheel assembly shall be replaceable without requiring destructive disassembly of the main chassis.

### C16-R93 — MUST-HAVE
Motor and encoder connections shall be keyed, labelled or otherwise designed to reduce accidental left/right/polarity mistakes during repeated disassembly.

### C16-R94 — MUST-HAVE
Encoder wiring and motor-power wiring shall receive appropriate strain relief.

### C16-R95 — MUST-HAVE
The system shall expose diagnostic values sufficient to inspect at least:

- commanded left/right speed;
- measured left/right speed;
- encoder counts;
- base \(v,\omega\);
- motor fault status;
- watchdog/motor inhibit status;
- odometry.

### C16-R96 — MUST-HAVE — AMENDED
Persistent inconsistency among:

- commanded wheel behaviour;
- encoder motion;
- IMU angular/orientation evidence;
- other available motion observations

shall be detectable as a **motion anomaly**.

This supports diagnosis of conditions including:

- wheel jams;
- disconnected encoders;
- certain slip conditions;
- robot pickup/lift;
- tipping;
- motor-driver faults.

Encoder agreement with command shall **not** be interpreted as proof that the chassis physically moved as commanded.

Arbitrary sustained translational slip is not claimed to be fully observable from wheel encoders and a 6-axis IMU alone.

### C16-R97 — TARGET
Development logging should allow locomotion tests to be replayed/analysed together with timestamps from perception and behaviour systems.

---

# 4.13 New requirements appended in this revision

### C16-R98 — MUST-HAVE — NEW
Obstacle and cliff inhibit decisions shall execute in the **low-level bounded-latency locomotion/safety controller or equivalent real-time path**, independent of the high-level behaviour/LLM process.

From availability of a valid low-level hazard observation to issuance of the deceleration/stop command shall not exceed:

\[
50\,ms
\]

under the validated V1 operating configuration.

### C16-R99 — MUST-HAVE — NEW
The complete hazard-response latency used in C16-R32 shall be measured and shall include, where applicable:

- sensor sampling/acquisition delay;
- sensor-internal processing;
- communication/transport;
- low-level safety evaluation;
- controller scheduling;
- motor-driver command delay;
- measurable onset of deceleration.

No unmeasured software stage may be omitted from the stopping-distance budget merely because it runs outside the drive controller.

### C16-R100 — MUST-HAVE — NEW
A clear-path authorisation for autonomous motion shall require valid authoritative short-range ToF/proximity safety information.

Camera-derived free-space interpretation shall not by itself authorise motion when the authoritative proximity layer is unavailable, stale or invalid.

### C16-R101 — MUST-HAVE — NEW
If authoritative ToF/proximity coverage is implemented using discrete rays or discrete sensing sectors rather than continuous coverage, the design shall document:

1. which parts of the C16-R60 swept envelope are directly protected;
2. which regions remain geometrically unprotected;
3. the compensating protection for each gap.

Valid compensating measures include:

- lower speed;
- bounded footprint geometry;
- physical contact detection;
- prohibited motion modes.

An undocumented sensing gap is non-conforming.

### C16-R102 — MUST-HAVE — NEW
The lower base footprint, including:

- body shell;
- driven wheels;
- caster swivel envelope;
- low-mounted protrusions

shall lie within a circle centred on the midpoint of the drive-wheel axle.

This circle defines the orientation-invariant floor-level collision footprint for in-place rotation.

### C16-R103 — MUST-HAVE — NEW
The head/ear assembly shall be evaluated separately from C16-R102.

Either:

1. the complete upper swept envelope during body rotation shall remain within the protected base collision circle; or
2. any head-height region outside that circle shall be explicitly documented as unprotected and assigned a validated reduced body-rotation speed/operating restriction.

Floor-level ToF coverage shall not be claimed to protect an unobserved head-height sweep.

### C16-R104 — MUST-HAVE — NEW
The low-level locomotion controller shall provide a local obstacle-recovery primitive implementing:

**stop → bounded retreat → turn → re-evaluate/resume as permitted.**

This primitive shall remain available even when the high-level behavioural process is unavailable.

Any new hazard encountered during recovery shall re-enter the safety-stop logic and may abort recovery.

### C16-R105 — TARGET — NEW
Where validated rearward ToF/proximity coverage is absent, the default low-level recovery retreat should initially be limited to approximately:

\[
0.10\,m
\]

at crawl speed.

This is **provisional pending prototype geometry, rear-clearance tests and stopping-distance measurements**.

Rotation shall occur before any subsequent normal translation.

### C16-R106 — MUST-HAVE — NEW
The locomotion command pipeline shall use the following ordering:

**behaviour intent**

→ **additive expressive contribution**

→ **summed \(v,\omega\)**

→ **safety, velocity and acceleration clamp**

→ **differential-drive conversion**

→ **wheel velocity targets**.

Safety clamping before expressive blending is non-conforming.

No expressive contribution may restore velocity, angular velocity or acceleration removed by a safety clamp.

### C16-R107 — TARGET — NEW
Motion-command timing jitter at the locomotion interface should remain small relative to the 20 ms nominal control interval implied by C16-R47.

Initial target:

\[
\pm5\,ms
\]

or better at the control-consumer boundary.

This is **provisional pending measurement** and shall be tightened or relaxed only based on visible-motion testing and actual controller architecture.

### C16-R108 — MUST-HAVE — NEW
An expressive startle command shall not request an uncontrolled rapid blind reverse.

The locomotion response shall first perform rapid but bounded **deceleration to zero**.

Any subsequent physical retreat shall obey:

- C16-R31 controlled reversal;
- C16-R61 reverse-safety constraints;
- normal acceleration and velocity limits.

### C16-R109 — MUST-HAVE — NEW
SPEC-16 shall expose a **listening-motion-inhibit request** distinct from the safety/motor inhibit of C16-R51.

An authorised audio/behaviour request shall be able to suppress nonessential base translation and rotation during acoustically critical periods such as:

- active listening;
- barge-in;
- source localisation.

Safety stops retain higher authority than listening requests.

### C16-R110 — MUST-HAVE — NEW
SPEC-16 shall publish timestamped body yaw and yaw-rate information with sufficient temporal alignment for the audio subsystem to transform direction-of-arrival observations from the rotating body frame.

SPEC-16 provides the motion state but does **not** perform audio DOA compensation itself.

This creates a new required interface for the downstream audio/audio-visual fusion architecture.

### C16-R111 — MUST-HAVE — NEW
Structure-borne drivetrain noise shall not rely on beamforming as its sole mitigation.

The implemented design shall include one or more of:

- mechanical motor/gear isolation;
- microphone mechanical isolation;
- lower-noise drivetrain selection;
- motion inhibition during acoustically critical capture.

### C16-R112 — MUST-HAVE — NEW
At zero commanded base velocity, the drivetrain shall provide sufficient stationary hold to resist ordinary reaction torque generated by permitted head/neck movement.

The hold mechanism may arise from:

- gearbox resistance;
- active motor control;
- driver brake mode;
- another validated mechanism.

The requirement is functional and does not prescribe a specific implementation.

### C16-R113 — TARGET — NEW
During CAD-time caster selection, the following configurations should be explicitly compared:

- single swivel caster;
- ball caster;
- dual fore/aft passive casters;
- low-friction skid.

Evaluation shall include:

- reversal jerk/swivel flip;
- acoustic noise;
- rolling resistance;
- threshold traversal;
- drive-wheel load fraction;
- tip margin;
- expressive-motion quality.

The dual-caster case is an **evaluation option only**. Selecting it would require an explicit revision of C16-R03/C16-R08 because it changes the current clean three-point support architecture.

### C16-R114 — MUST-HAVE — NEW
A declared V1 surface-validation set shall be established before drivetrain/component freeze and shall include at minimum:

- representative hard indoor floor;
- representative low-pile rug;
- a rug edge or floor threshold transition.

Wheel/caster selection and locomotion limits shall be validated against this declared set.

---

# 5. Interfaces and dependencies

## 5.1 Mechanical/body design — AMENDED

SPEC-16 requires the body design to provide:

- rigid left/right motor mounting;
- drive-wheel clearance;
- passive support/caster mounting;
- appropriate support polygon;
- adequate drive-wheel normal force;
- ground clearance;
- removable panels;
- low placement for heavy components where practical;
- a lower footprint contained within the C16-R102 collision circle;
- sufficient space/overhang for authoritative proximity sensors;
- sufficient forward/downward sensor lead distance if elevated-edge detection is supported;
- documented head-height swept envelope.

The body CAD cannot be frozen until wheel track, wheel diameter, passive-support geometry, sensing overhang and mass distribution have preliminary values.

If dual passive casters are chosen after the C16-R113 comparison, C16-R03/C16-R08 must be explicitly revised.

---

## 5.2 Head mechanism — AMENDED

The moving head changes:

- total COM;
- COM projection;
- yaw inertia;
- transient chassis loading;
- reaction torque applied to the base;
- upper swept collision envelope.

SPEC-16 requires the base to remain sufficiently stationary under zero-velocity head motion.

The head/body architecture must additionally resolve whether the head remains inside the protected collision cylinder or operates under a documented reduced rotation envelope.

---

## 5.3 Camera/perception — AMENDED

The visual system provides person/target information.

The interface remains:

**pixels → tracking/perception → geometrically transformed body-frame target → behaviour/controller → base**

not:

**pixel x-position → motor PWM.**

For collision safety:

**ToF/proximity safety state → low-level safety controller → motion inhibit/clamp**

is authoritative.

Camera perception is advisory and may classify or contextualise the obstacle after a stop.

---

## 5.4 Audio — AMENDED

The body microphone array requires:

- timestamped body yaw;
- timestamped yaw rate;
- commanded motion state;
- acceleration feedforward where useful;
- listening-motion-inhibit access.

Body rotation makes external-world DOA tracks time-varying.

The audio subsystem is responsible for compensating those tracks.

Drivetrain vibration must be addressed mechanically and behaviourally; beamforming alone is not sufficient for coherent structure-borne vibration.

---

## 5.5 Obstacle/safety sensing — AMENDED

The architecture is no longer deferred.

The authoritative local safety layer is:

**short-range ToF/proximity sensing → low-level bounded-latency safety evaluation → acceleration/velocity inhibit.**

Coverage must protect or explicitly account for:

- forward travel;
- reverse travel;
- in-place rotation;
- discrete sensing gaps;
- elevated edges where such operation is supported.

The high-level process does not own the final stop decision.

---

## 5.6 Behaviour architecture / SPEC-20 — AMENDED

SPEC-16 provides base-motion capability.

The later integrated behaviour layer decides:

- whether eyes, head or body orient;
- whether to follow;
- whether to approach;
- when to roam;
- what expressive motion contribution to request.

The expression system may contribute additive locomotion motion.

However, the sequence is always:

**behaviour + expression → safety clamp → drive.**

Startle does not override reversal safety.

Audio may request temporary motion inhibition.

---

## 5.7 Compute/control architecture — AMENDED

The low-level architecture must allocate:

- encoder acquisition;
- IMU acquisition;
- closed-loop wheel-speed control;
- low-level hazard evaluation;
- cliff evaluation where relevant;
- command watchdog;
- recovery primitive;
- odometry;
- motor inhibit;
- motion-state publication.

The ≤50 ms safety requirement strongly favours an MCU/local-controller execution path.

The exact controller device remains unfrozen.

---

## 5.8 Power

Motor choice cannot be separated from battery architecture.

The eventual electrical design must jointly consider:

\[
P_{compute}
+
P_{display}
+
P_{audio}
+
P_{head}
+
P_{drive}
+
P_{sensors}
\]

including simultaneous peaks.

---

## 5.9 New audio-visual fusion dependency

The downstream audio/audio-visual fusion architecture must now understand that acoustic bearing observations originate in a rotating body frame.

It shall eventually consume capture-time body yaw/yaw-rate information from SPEC-16 in the same conceptual manner that visual gaze/perception systems consume capture-time pose.

SPEC-16 does not define that fusion algorithm.

---

# 6. Quantities still requiring CAD / prototype / component validation

The obstacle-sensor **architecture** is now decided and is therefore removed from the unresolved list.

The exact ToF/proximity sensor model, placement count and final coverage geometry remain component/CAD variables.

| Quantity | Why unresolved | What determines it |
|---|---|---|
| Complete Makad mass \(m\) | CAD/BOM incomplete | Final build |
| COM position | Component layout incomplete | CAD mass properties + physical validation |
| COM height \(h\) | CAD incomplete | CAD/prototype |
| Support margin \(d\) | Passive-support geometry open | Base geometry |
| Wheel radius \(r\) | Part selection deferred | Torque, speed, packaging, **rug-edge/threshold traversal** |
| Wheel track \(b\) | Body CAD incomplete | Stability, width, turning geometry |
| Passive-support type | CAD comparison required | C16-R113 evaluation |
| Passive-support position | Requires COM geometry | Stability, traction, reversal |
| Drive-axle load fraction | Mass distribution unknown | Physical layout |
| Effective tyre friction \(\mu\) | Surface dependent | Declared V1 surface-set testing |
| Rolling resistance \(C_{rr}\) | Surface/caster dependent | Declared V1 surface-set testing |
| Maximum supported rug-edge/threshold height | Not yet measured | Wheel/caster prototype |
| Maximum supported floor gap/joint | Not yet measured | Prototype |
| Maximum supported slope | Not yet selected | Stability/traction tests |
| Complete yaw inertia \(I_z\) | CAD incomplete | CAD mass model |
| Gear ratio | Exact motor not selected | Torque/speed/backlash requirements |
| Encoder motor-shaft CPR | Exact motor not selected | C16-R35 architecture |
| Effective wheel CPR | Depends on encoder and ratio | Low-speed testing |
| Gearbox reversal deadband | Unknown | Prototype |
| Minimum stable expressive speed | Stiction/control dependent | Prototype |
| Zero-velocity head-reaction disturbance | Mechanism dependent | Integrated head/base test |
| Maximum floor translational speed | Safety envelope dependent | Stability + ToF + latency |
| Maximum elevated-surface speed | Edge-distance dependent | Cliff/latency testing |
| Maximum yaw rate | Stability/character/head sweep dependent | Prototype |
| Acceleration limit | COM dependent | Tip/slip tests |
| Braking deceleration | Motor/driver/floor dependent | Prototype |
| Complete safety-path latency | Hardware/software dependent | Instrumented measurement |
| Exact ToF/proximity sensor model | Component selection deferred | Range, FOV, latency, surface performance |
| Number/orientation of proximity sensors | CAD dependent | Swept-envelope coverage |
| Discrete-ray blind regions | Geometry unknown | Sensor layout |
| Required sensor overhang before wheel fall-line | Chassis dependent | Speed + latency + braking |
| Cliff sensing implementation | Exact hardware open | Declared elevated-surface set |
| Dark/specular/transparent elevated-surface support | Must be declared | Sensor validation |
| Base collision-circle radius | CAD incomplete | Full lower footprint |
| Head swept radius | CAD incomplete | Head/ear geometry |
| Recovery retreat distance | ~0.10 m initial target | Rear-clearance validation |
| Recovery turn angle/policy | Environment/controller dependent | Prototype testing |
| Command-path jitter | Not yet measured | Controller architecture |
| Motor acoustic noise | Unknown until drivetrain exists | Installed measurements |
| Drive-system peak power | Motor unknown | Component selection |
| Thermal duty cycle | Hardware unknown | Integrated testing |

### Removed from unresolved status

- Whether local autonomous collision safety uses ToF/proximity sensing: **resolved — YES**.
- Whether camera perception may independently authorise a clear path: **resolved — NO**.
- Whether an IMU is present: **resolved — YES, 6-axis minimum**.

---

# 7. Acceptance tests

## Existing tests

### C16-T01 — Architecture inspection
Verify physically that Makad has:

- two independently driven primary wheels;
- one passive support/caster;
- no active balancing requirement;
- encoder feedback on both driven axes.

**Pass:** architecture matches C16-R01–R04.

### C16-T02 — Differential-drive motion test
Command separately:

1. forward;
2. reverse;
3. left arc;
4. right arc;
5. clockwise near-in-place turn;
6. counter-clockwise near-in-place turn.

**Pass:** all six behaviours occur controllably.

### C16-T03 — Support-polygon CAD test
Evaluate COM projection for neutral and extreme permitted head poses.

**Pass:** COM remains inside the support polygon and minimum \(d\) is recorded.

### C16-T04 — Physical static-tip validation
Compare physical tip threshold to CAD prediction.

**Pass:** a conservative validated stability envelope can be established.

### C16-T05 — Dynamic stability test
Progressively increase forward, reverse and rotational acceleration.

**Pass:** selected operating limits retain specified stability margin.

### C16-T06 — Traction test
Perform representative acceleration and turning manoeuvres across the declared surface set.

**Pass:** sustained traction loss does not occur within the validated envelope.

### C16-T07 — Caster behaviour test
Perform repeated forward/reverse transitions, low-speed rotation and near-in-place turns.

**Pass:** passive-support behaviour does not create unacceptable hopping, unloading or stalls.

### C16-T08 — Low-speed controllability
Command progressively lower constant forward speeds.

**TARGET pass:** controllable near 0.05 m/s or below without repeated stop-go surging.

### C16-T09 — Maximum-speed characterisation
Measure actual steady translational speed versus command.

**Pass:** software clamp works.

### C16-T10 — Body-yaw performance
Command 30°, 60°, 90° and 180° turns.

**Pass:** controlled social body reorientation is possible.

### C16-T11 — Controlled reversal
Command forward travel followed by reverse.

**Pass:** velocity crosses through controlled near-zero motion.

### C16-T12 — Emergency/maximum braking characterisation — AMENDED
At several speeds, trigger authoritative ToF/proximity safety stops.

Measure:

- complete sensor-to-deceleration latency;
- deceleration onset;
- braking distance;
- total hazard-to-stop distance.

**Pass:** the measured result satisfies the C16-R32 model and supports a validated speed table.

### C16-T13 — Straight-line calibration test
Command 1 m travel.

**TARGET:** ≤5% distance error and ≤50 mm lateral deviation.

### C16-T14 — Rotation odometry test
Command a 360° in-place rotation.

**TARGET:** final heading error approximately ≤10°.

### C16-T15 — Wheel-controller disturbance test
Introduce changing wheel load/friction.

**Pass:** measured velocity recovers toward target.

### C16-T16 — Control-rate verification
Log controller timing.

**TARGET:** ≥50 Hz.

### C16-T17 — Command-watchdog test
Interrupt high-level commands.

**Pass:** controlled stop occurs automatically.

### C16-T18 — Startup safety test
Reboot controller/computer/communications.

**Pass:** no unintended motion.

### C16-T19 — Motor inhibit test
Activate software inhibit.

**Pass:** movement remains disabled until deliberate re-enable.

### C16-T20 — Stall/jam test
Safely restrain one wheel.

**Pass:** overcurrent/stall handling occurs without system damage/reboot.

### C16-T21 — Encoder failure test
Disconnect/freeze encoder feedback.

**Pass:** autonomous movement does not continue indefinitely.

### C16-T22 — Forward obstacle stopping — AMENDED
Approach an obstacle using the authoritative ToF/proximity layer.

**Pass:** Makad stops within the validated collision margin at each permitted speed.

### C16-T23 — Reverse obstacle protection — AMENDED
Test reverse behaviour using rear ToF coverage if fitted, and separately test bounded recovery retreat where rear coverage is absent.

**Pass:** C16-R61 behaviour is satisfied.

### C16-T24 — Rotational swept-envelope test — AMENDED
Place obstacles around the base collision circle and evaluate in-place rotation.

**Pass:** the lower base does not leave the C16-R102 collision envelope and sensor/control assumptions remain valid.

### C16-T25 — Safety override test
Command following/roaming while introducing an obstacle.

**Pass:** low-level safety overrides behavioural locomotion.

### C16-T26 — Stale safety-data test — AMENDED
Freeze or delay the authoritative ToF/proximity safety stream.

**Pass:** the system enters a defined degraded/stop state.

Camera free-space interpretation shall not restore movement.

### C16-T27 — Cliff/edge test — AMENDED
Required if elevated operation is supported.

Test representative allowed surfaces including the declared worst-case dark/specular/transparent cases.

**Pass:** edge detection and stopping remain valid across the supported set.

### C16-T28 — Person body-turn test
Vary person bearing and head yaw.

**Pass:** whole-body turn follows transformed body-frame information.

### C16-T29 — Target-loss test
Lose a followed target.

**Pass:** Makad slows/stops and does not continue indefinitely.

### C16-T30 — Following test
Perform slow controlled following.

**Pass:** no repeated oscillatory or excessive steering behaviour.

### C16-T31 — Local roaming test
Operate in a bounded test area without SLAM.

**Pass:** local reactive movement functions.

### C16-T32 — Power-transient test
Perform starts, stops, reversals and simultaneous head/base motion.

**Pass:** no unrelated subsystem resets.

### C16-T33 — Thermal endurance
Run representative locomotion for ≥15 minutes.

**TARGET:** no thermal shutdown or progressive degradation.

### C16-T34 — Audio interference test — AMENDED
Record body microphones during:

- motors disabled;
- straight driving;
- acceleration;
- rotation;
- passive-support reversal.

Evaluate structure-borne components in addition to airborne noise.

**Pass:** drive noise is characterised and the mitigation strategy does not depend on beamforming alone.

### C16-T35 — Electrical interference test
Compare sensor/audio/camera behaviour with motors off and active.

**Pass:** no significant corruption/reset attributable to drive electronics.

### C16-T36 — Serviceability test
Remove and reinstall each drive assembly.

**Pass:** non-destructive service and unambiguous reconnection.

### C16-T37 — Diagnostic logging test
Create speed mismatch, encoder interruption, watchdog stop and inhibit.

**Pass:** states appear in diagnostics.

---

## New acceptance tests appended in this revision

### C16-T38 — Safety-path latency test — NEW
Instrument an authoritative proximity detection event and the corresponding low-level deceleration command.

Repeat under representative high-level CPU load.

**Pass for C16-R98:** worst-case valid-detection-to-deceleration-command latency is ≤50 ms and remains independent of the high-level process.

### C16-T39 — End-to-end hazard latency budget test — NEW
Measure:

- sensor acquisition delay;
- processing;
- transport;
- safety-controller scheduling;
- motor command;
- physical deceleration onset.

**Pass for C16-R99:** all significant terms are measured/accounted for and the resulting \(t_{latency}\) is used in C16-R32.

### C16-T40 — Camera-authority firewall test — NEW
Make camera perception report an apparently clear path while the authoritative proximity layer is:

- invalid;
- stale;
- reporting obstacle.

**Pass for C16-R100:** camera output cannot independently enable forward motion.

### C16-T41 — Proximity-coverage mapping test — NEW
Map each sensor FOV/ray against the CAD swept envelope.

Identify all gaps.

**Pass for C16-R101:** every unprotected region has an explicit compensating speed, footprint, contact or prohibited-motion rule.

### C16-T42 — Base collision-circle CAD test — NEW
Rotate the complete lower base geometry 360° about the drive-axle midpoint in CAD.

**Pass for C16-R102:** all lower components remain inside the defined collision circle.

### C16-T43 — Upper swept-envelope test — NEW
Calculate and physically sanity-check the head/ear swept envelope during body rotation.

**Pass for C16-R103:** either the upper assembly remains inside the protected circle or the unprotected region and reduced operating limit are explicitly documented.

### C16-T44 — Low-level recovery test — NEW
Trigger a forward obstacle stop and observe:

**stop → retreat → turn → re-evaluate/resume.**

Repeat with the high-level behaviour process disabled.

Repeat with an obstacle present behind Makad during the retreat.

**Pass for C16-R104:** recovery remains low-level, does not require high-level availability, and a rear hazard causes a safe stop/abort rather than continued retreat.

### C16-T45 — Expressive/safety clamp ordering test — NEW
Inject:

- a behavioural forward command;
- a positive additive expressive velocity;
- a lower safety speed limit.

**Pass for C16-R106:** final wheel targets never exceed the post-blend safety clamp.

Repeat with angular velocity and acceleration constraints.

### C16-T46 — Command-jitter measurement — NEW
Measure arrival/execution interval variation for locomotion commands during a slow shaped expressive trajectory.

**TARGET for C16-R107:** approximately ±5 ms or better at the control-consumer boundary, pending final tuning.

### C16-T47 — Startle reversal test — NEW
While Makad moves forward, trigger the maximum permitted startle response.

**Pass for C16-R108:** the base performs rapid bounded deceleration to zero before any reverse motion; subsequent retreat obeys ordinary reverse limits.

### C16-T48 — Listening-motion-inhibit test — NEW
While Makad approaches a target, trigger an audio barge-in/listening request.

**Pass for C16-R109:** nonessential base motion decelerates/stops according to the listening policy while collision-safety authority remains active.

### C16-T49 — Audio ego-motion state test — NEW
Rotate Makad while logging audio timestamps and SPEC-16 body-yaw/yaw-rate output.

**Pass for C16-R110:** body orientation/rate is timestamped and temporally usable by the audio subsystem for rotating-frame compensation.

### C16-T50 — Structure-borne-noise mitigation test — NEW
Compare body-microphone recordings across at least two relevant states, such as:

- rigid motor mounting;
- chosen isolation/motion-inhibit strategy.

**Pass for C16-R111:** the implemented mitigation materially addresses coherent structure-borne contamination and does not rely solely on beamforming.

### C16-T51 — Zero-velocity hold test — NEW
Command zero base velocity and execute the most aggressive permitted head-yaw motion.

Measure unintended chassis displacement/yaw.

**Pass for C16-R112:** the base remains functionally stationary and does not visibly counter-twitch in a way that compromises the intended expressive motion.

Initial measurement targets may be established during prototype testing rather than frozen here.

### C16-T52 — Lift/pickup detection test — NEW
While Makad is moving or commanded to move, pick it up safely.

**Pass for C16-R57/C16-R96:** lift state is detected, drive motion is inhibited, odometry is marked invalid/degraded as appropriate, and replacing Makad on the surface does not automatically resume the prior motion command.

### C16-T53 — Tip/fall detection test — NEW
Place Makad in a safely restrained tipped orientation or simulate equivalent IMU orientation.

**Pass for C16-R57/C16-R96:** the abnormal orientation is detected and drive is inhibited until an explicit safe recovery/re-arm condition occurs.

### C16-T54 — Expressive micro-motion drivetrain test — NEW
Execute a scripted sequence containing:

1. small side-to-side body wiggles;
2. slow approach;
3. short hesitation;
4. controlled retreat;
5. repeated small reversals.

Record video and wheel/encoder logs.

**Pass for C16-R24/R35/R36:** movement is visibly smooth, repeatable and free of dominant stop-jerk-move behaviour or reversal deadband that destroys the intended gesture.

Failure is a **gearmotor/gearbox selection failure**, even if nominal top speed and torque requirements are met.

### C16-T55 — Surface-set test — NEW
Test the drivetrain on:

- representative hard floor;
- representative low-pile rug;
- the declared rug edge/floor threshold.

**Pass for C16-R114:** Makad retains required traction, control and clearance across the declared V1 set.

### C16-T56 — Caster configuration comparison — NEW
Before passive-support CAD freeze, prototype or fixture-test the practical candidate configurations from C16-R113 where feasible.

Compare:

- reversal jerk;
- noise;
- rolling resistance;
- threshold traversal;
- drive-wheel loading;
- stability.

**TARGET pass:** the selected configuration has documented tradeoffs and is justified for Makad's frequent expressive reversal duty.

---

# 8. Internal consistency / design review

## 8.1 The architecture remains sound

Two independently driven wheels remain the correct level of actuation complexity.

The revision does not add locomotion DOFs.

Most added complexity comes from making autonomous movement safe and expressive rather than from making the mechanism more elaborate.

---

## 8.2 The original safety analysis was latency-incomplete

This was the largest omission.

SPEC-16 previously calculated latency travel but failed to require a bounded hazard-response path.

At Makad's speeds, that is backwards: the drivetrain can brake quickly enough that software/sensor latency dominates.

The revised architecture therefore makes the local safety path a low-level bounded-latency function.

This is now a load-bearing requirement.

---

## 8.3 The camera cannot own clear-path authority

Using the camera for semantic obstacle understanding remains useful.

Using it as the only clear-path authority would reintroduce variable perception latency directly into the braking envelope.

That would undermine C16-R98.

The camera firewall is therefore intentional rather than redundant.

---

## 8.4 ToF/proximity coverage is still not magically continuous

Committing to ToF does not mean every centimetre around Makad is observed.

Discrete FOVs can leave gaps.

C16-R101 exists specifically to prevent the engineering team from drawing three sensor cones in CAD and calling the entire swept envelope "covered."

Any gap has to be paid for somewhere else.

---

## 8.5 The circular footprint is a high-leverage mechanical simplification

Constraining the lower chassis to a circle around the axle midpoint dramatically simplifies in-place-rotation safety.

It does not force Makad to look round.

Angular body panels can remain inside the virtual circle.

This is one of the cheapest requirements in the spec relative to the complexity it removes downstream.

---

## 8.6 The head remains the exception

The lower collision cylinder does not protect a wide head or ear assembly.

A floor-level proximity sensor may clear a mug base while the ear hits the mug higher up.

The revised spec therefore stops claiming complete collision coverage unless the upper envelope is genuinely inside the protected radius.

---

## 8.7 Recovery introduces a deliberate reverse-risk compromise

A robot that can only stop when obstructed is behaviorally brittle.

But blindly backing away introduces another hazard.

The bounded ~10 cm crawl retreat is therefore a compromise, not a claim that rear space is safe.

If rear ToF coverage later fits the BOM/CAD cleanly, the retreat envelope can become less restrictive.

Until then, it remains short and slow.

---

## 8.8 The IMU promotion is justified

An encoder cannot distinguish:

> wheel rotated

from:

> robot translated exactly as expected.

That distinction matters when:

- wheels slip;
- Makad is picked up;
- Makad tips;
- one wheel spins freely.

The six-axis IMU is consequently architecture-level value rather than sensor creep.

It still does not make arbitrary planar slip perfectly observable, and the requirements deliberately avoid claiming otherwise.

---

## 8.9 Near-zero motion is a product-quality issue

The most expressive locomotion motions occur where cheap gearmotors often behave worst:

- very low speed;
- reversal;
- gearbox deadband;
- stiction.

It is therefore possible for a drivetrain to pass top-speed and torque tests while failing Makad's actual purpose.

C16-T54 is intentionally a **component-selection gate**.

---

## 8.10 High gear reduction solves one problem and strengthens another

Motor-side encoding behind high reduction makes encoder count availability easy.

But that same gearbox can introduce:

- backlash;
- friction;
- audible gear noise;
- poor reversal feel.

Therefore the revision shifts attention from raw CPR toward drivetrain deadband and character.

That is the correct trade.

---

## 8.11 Zero-velocity behaviour had been underspecified

A head that turns while the body twitches oppositely will look mechanically cheap.

Stationary hold is therefore part of expressive quality.

The requirement is functional so we do not prematurely decide whether the eventual solution is active hold or simply a suitably resistant drivetrain.

---

## 8.12 Body microphones remain mechanically body-fixed but not world-fixed

The original microphone rationale is not completely reversed.

The speaker-to-microphone geometry remains rigid within the body.

What changes is the world frame:

DOA estimates rotate with Makad.

That creates a new ego-motion dependency for audio.

---

## 8.13 Beamforming cannot fix everything drive noise does

Motor/gear vibration conducted through the shell does not behave like a clean directional far-field source.

The array therefore cannot be expected to spatially null it reliably.

Mechanical isolation and motion scheduling are the correct primary tools.

---

## 8.14 Listening inhibit is a real cross-subsystem requirement

Barge-in during an approach is exactly the moment when:

- wheel acceleration may be high;
- gear noise is strong;
- microphone availability suddenly matters.

A one-directional base→audio state interface is therefore insufficient.

Audio/behaviour needs the ability to request a temporary quiet base.

---

## 8.15 Startle remains expressive without dangerous reversing

A physically fast retreat is not required for Makad to read as startled.

Rapid braking plus coordinated eyes/head/audio can carry the immediate perceptual event.

The subsequent retreat can be slower and safe.

This is a good example of cross-channel expression reducing mechanical risk rather than increasing it.

---

## 8.16 Elevated operation remains more expensive than floor operation

A tabletop gives much less usable stopping distance than a floor.

It also introduces sensor/material problems from:

- black surfaces;
- glossy surfaces;
- transparent surfaces;
- limited sensor overhang.

The upper floor speed target therefore cannot be reused on a desk.

This distinction is now explicit.

---

## 8.17 The elevated-operation fork must influence CAD before final software policy

Even if elevated roaming is eventually disabled, the chassis designer must know whether the design is expected to accommodate:

- downward sensors;
- forward sensor overhang;
- additional protective geometry.

Therefore this cannot wait until after CAD is finished.

---

## 8.18 Caster selection is now a character issue too

A swivel caster may be mechanically acceptable yet make every tiny reversal visibly kick.

That is especially damaging for Makad because frequent small reversals are part of the intended body language.

The passive support must therefore be judged by animation character as well as mechanics.

---

## 8.19 Dual caster remains only an evaluated alternative

A dual fore/aft caster arrangement may enlarge fore/aft support and help the high COM.

But it sacrifices the clean deterministic three-point contact that motivated the current architecture.

The revision therefore does **not** silently adopt it.

If testing shows it is substantially superior, C16-R03/R08 must be consciously reopened.

---

## 8.20 Locomotion's engineering spend needs a product-level justification

SPEC-16 is large because autonomous movement creates many failure modes, not because the drivetrain itself is mechanically complex.

The justification is:

> **Makad's locomotion exists primarily as a social-expression and proxemics channel. Whole-body approach, retreat, orientation, following and repositioning can communicate intent and personality in ways that eye and neck motion alone cannot. Mobility is justified only while it improves these behaviours; mapping, high speed, terrain capability and navigation sophistication remain subordinate to face, gaze, head motion, audio interaction and overall aliveness.**

That rule should guide later schedule tradeoffs.

---

# 9. Final decisions carried forward

## DECIDED

1. Makad V1 uses differential drive.

2. Two independently powered drive wheels are used.

3. Both drive wheels require encoder feedback.

4. Baseline passive support remains a single third contact.

5. Makad does not self-balance.

6. COM/support-polygon analysis remains mandatory.

7. Head pose and battery placement are included in stability analysis.

8. Motor sizing includes translation and yaw inertia.

9. Continuous and peak torque are distinguished.

10. Traction is explicitly checked.

11. Closed-loop wheel-speed control is mandatory.

12. Base commands use a \(v,\omega\) abstraction.

13. Acceleration and controlled reversal remain mandatory.

14. Wheel odometry is relative/drifting.

15. Motor-side encoding behind substantial gearbox reduction is the baseline architecture.

16. Approximately 1900 effective wheel counts/rev is the current reference-resolution regime for the 0.05 m/s, 30 mm-radius, 50 Hz example.

17. Gearbox backlash/deadband is a gearmotor-selection criterion.

18. A rigidly mounted 6-axis IMU is now **MUST-HAVE**.

19. Pickup/lift and tip/fall detection are required.

20. Encoder agreement does not prove physical chassis motion.

21. Short-range ToF/proximity sensing is the authoritative local collision-safety layer.

22. Camera perception is advisory only for clear-path decisions.

23. Camera may classify/contextualise obstacles but may not independently authorise motion.

24. ToF/proximity coverage must address forward, reverse and rotational swept envelopes.

25. Discrete coverage gaps require explicit compensation.

26. The lower base footprint must fit within a collision circle centred on the drive-axle midpoint.

27. Head-height swept envelope must be separately handled/documented.

28. Obstacle/cliff safety runs in a low-level high-level-independent path.

29. Valid hazard observation to deceleration command is bounded at ≤50 ms.

30. Complete end-to-end hazard latency must be measured.

31. Safe speed is constrained by available free distance, latency and braking performance.

32. The 0.30–0.40 m/s upper speed target is **floor-only**.

33. Elevated-surface speed is independently derived.

34. Local obstacle recovery implements stop → bounded retreat → turn → re-evaluate/resume.

35. Without rear ToF, recovery reverse is crawl-speed and short-distance only.

36. Approximately 10 cm is the initial recovery-distance TARGET.

37. Recovery remains available without the high-level process.

38. Behaviour and expressive locomotion commands are summed **before** safety clamping.

39. Expressive motion cannot restore velocity removed by the safety layer.

40. Startle locomotion means rapid controlled deceleration first, not blind fast reverse.

41. The locomotion interface publishes future commanded translational/angular acceleration for anticipatory expression coordination.

42. Command-path jitter is now an explicit quality parameter.

43. Audio may request a non-safety listening-motion inhibit.

44. Body yaw and yaw rate are published for rotating-frame audio compensation.

45. Structure-borne drivetrain noise cannot rely on beamforming alone.

46. Zero-commanded velocity includes stationary hold against ordinary head reaction torque.

47. The declared V1 surface set includes hard floor, low-pile rug and a rug/threshold transition.

48. Caster/passive-support configuration is an explicit CAD-time evaluation.

49. Dual caster is not adopted automatically; choosing it requires reopening the baseline three-point requirements.

50. V1 locomotion still does not require SLAM.

51. Mobility remains subordinate to Makad's expressive/social objective rather than navigation sophistication.

---

## PROVISIONAL / TARGET

- crawl motion: ~0.03–0.06 m/s;
- ordinary autonomous motion: ~0.10–0.25 m/s;
- floor-only upper region: ~0.30–0.40 m/s;
- normal body yaw: ~45–120°/s;
- controller rate: ≥50 Hz;
- high-level command watchdog: ≤250 ms;
- command jitter: initial ±5 ms target;
- recovery retreat: ~0.10 m target without rear ToF;
- straight 1 m odometry: ≤5% distance error / ≤50 mm lateral error;
- 360° turn: approximately ±10°;
- approximately 2× acceleration margin below experimentally established tipping threshold;
- ≥15 min representative drive thermal test.

---

## MUST BE RESOLVED BEFORE COMPONENT SELECTION / CAD FREEZE

- total mass;
- COM;
- wheel diameter;
- wheel track;
- exact passive-support type/location;
- whether single-caster baseline survives C16-R113 evaluation;
- tyre/surface traction;
- yaw inertia;
- final acceleration;
- braking performance;
- exact gearmotor;
- gearbox deadband;
- exact encoder;
- exact ToF/proximity sensor;
- ToF number/FOV/layout;
- sensor blind regions;
- sensor overhang;
- base collision radius;
- upper/head swept radius;
- declared elevated-surface operating set;
- elevated cliff modality;
- final recovery retreat distance;
- final command jitter;
- zero-velocity hold performance;
- drivetrain/microphone vibration behaviour;
- drive current/power architecture.

---

## EXPLICITLY DEFERRED

- exact gearmotor model;
- exact motor driver;
- exact wheels;
- exact passive-support component;
- exact ToF/proximity sensor model;
- exact cliff sensor model;
- persistent SLAM;
- global map;
- room-to-room navigation;
- global path planning;
- autonomous docking;
- research-grade slip estimation;
- suspension;
- active balancing;
- BB-8 spherical locomotion.

---

# 10. Revision changelog

## Requirements amended

- **C16-R24** — added expressive-character significance to minimum controllable speed.
- **C16-R26** — made 0.30–0.40 m/s upper envelope explicitly floor-only.
- **C16-R32** — repaired stopping equation and reformulated it as an available-distance inequality.
- **C16-R35** — resolved encoder architecture toward motor-side encoding + high reduction and added ~1900 effective CPR reference calculation.
- **C16-R36** — made backlash/deadband an expressive-quality and gearmotor-selection criterion.
- **C16-R49** — clarified that 250 ms is high-level command-loss watchdog latency, not collision-safety latency.
- **C16-R58** — committed authoritative safety sensing to short-range ToF/proximity.
- **C16-R59** — explicitly made camera/coarse visual range advisory only.
- **C16-R60** — tied ToF/proximity coverage to translation and rotational swept envelopes.
- **C16-R61** — resolved reverse safety around rear ToF or bounded recovery retreat.
- **C16-R66** — strengthened elevated cliff requirements and supported-surface validation.
- **C16-R87** — documented coherent structure-borne noise and rejected beamforming as sole mitigation.
- **C16-R89** — added body yaw/yaw rate and one-control-cycle-ahead commanded translational/angular acceleration.
- **C16-R90** — cross-referenced listening-motion inhibit.
- **C16-R96** — corrected false general slip-detection implication and changed it to multi-source motion-anomaly detection.

## Requirements changed status

- **C16-R57** — **STRETCH → MUST-HAVE**. Six-axis IMU is now mandatory.

No other existing requirement changed priority status.

## Requirements added

- **C16-R98** — ≤50 ms low-level hazard-detection-to-deceleration-command latency.
- **C16-R99** — full end-to-end hazard-latency accounting.
- **C16-R100** — ToF/proximity required for clear-path authorisation.
- **C16-R101** — discrete proximity-coverage gaps must be documented and compensated.
- **C16-R102** — lower base contained within axle-centred collision circle.
- **C16-R103** — head/ear upper swept-envelope handling.
- **C16-R104** — low-level stop-retreat-turn-recovery primitive.
- **C16-R105** — ~10 cm crawl-speed retreat initial TARGET without rear ToF.
- **C16-R106** — expressive blend before safety clamp.
- **C16-R107** — motion-command jitter TARGET.
- **C16-R108** — startle resolves to controlled stop before retreat.
- **C16-R109** — listening-motion-inhibit request.
- **C16-R110** — timestamped body yaw/yaw-rate interface for audio.
- **C16-R111** — mechanical/behavioural structure-borne-noise mitigation.
- **C16-R112** — zero-velocity stationary hold.
- **C16-R113** — caster/passive-support CAD comparison.
- **C16-R114** — declared hard-floor/rug/threshold surface-validation set.

## Tests amended

- **C16-T12** — now measures authoritative end-to-end hazard response.
- **C16-T22** — forward stopping explicitly uses authoritative proximity layer.
- **C16-T23** — reverse testing covers rear ToF and bounded retreat.
- **C16-T24** — rotation test aligned with collision-circle architecture.
- **C16-T26** — camera cannot override stale authoritative safety data.
- **C16-T27** — cliff validation expanded to declared surface set.
- **C16-T34** — explicitly evaluates coherent structure-borne noise.

## Tests added

- **C16-T38** — ≤50 ms low-level safety latency.
- **C16-T39** — full physical hazard-latency budget.
- **C16-T40** — camera-authority firewall.
- **C16-T41** — discrete ToF/proximity coverage-gap analysis.
- **C16-T42** — axle-centred base collision-circle validation.
- **C16-T43** — head-height swept-envelope validation.
- **C16-T44** — full stop-retreat-turn-recovery, including rear obstacle.
- **C16-T45** — expressive blend/safety-clamp ordering.
- **C16-T46** — command-jitter measurement.
- **C16-T47** — startle controlled-stop behaviour.
- **C16-T48** — listening-motion inhibit.
- **C16-T49** — audio ego-motion state timing.
- **C16-T50** — structure-borne-noise mitigation.
- **C16-T51** — zero-velocity hold under head slew.
- **C16-T52** — pickup/lift detection.
- **C16-T53** — tip/fall detection.
- **C16-T54** — expressive wiggle / hesitate / retreat drivetrain test.
- **C16-T55** — hard-floor/rug/threshold surface test.
- **C16-T56** — passive-support configuration comparison.

## Existing requirements/tests removed

**None.**

All original requirements **C16-R01 through C16-R97** remain present.

All original tests **C16-T01 through C16-T37** remain present.

New requirements append from **C16-R98 through C16-R114**.

New tests append from **C16-T38 through C16-T56**.