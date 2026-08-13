# MAKAD SPEC-01 v1.2 — Expressive Face & Display System

**Source capability:**  
**#1 — Makad will have a cute, expressive animated face on its screen.**

**Priority:** MUST-HAVE  
**Status:** Functional architecture frozen; hardware limits remain provisional until Capability #2 establishes the neck/head torque and mass budget.

**Primary related capabilities:** #2, #3, #8, #9, #11, #12, #13, #14, #17, #20

---

# 1. Functional Objective

Makad's display shall function primarily as its **face and emotional interface**.

The face shall not behave like a conventional GUI with facial graphics placed on it. The intended effect is that the eyes, physical head, body, sound and eventual locomotion appear to belong to **one animated character**.

The face must:

- remain visually alive while Makad is awake;
- react quickly to relevant events;
- support continuous gaze;
- support authored expressions without becoming a set of GIFs;
- preserve a highly recognizable visual identity;
- coordinate tightly with head/body motion;
- support utility GUI content on the same display;
- survive subsystem failures without exposing operating-system UI or destroying the character illusion.

The system shall therefore be engineered as a **real-time procedural character-animation framework**.

---

# 2. Core Visual Identity

## C1-R01 — Exactly two eyes

**MUST-HAVE**

Makad's face consists of:

**exactly two eyes.**

There shall be no permanent:

- mouth;
- nose;
- eyebrows;
- cheeks;
- lips;
- additional facial anatomy.

Expression must be created through the eyes and physical behaviour rather than by adding more facial features.

---

## C1-R02 — Circular eye identity

**MUST-HAVE**

The underlying graphical primitive representing each Makad eye shall be a **circle**.

Expressions may alter:

- position;
- gaze offset;
- apparent size;
- spacing;
- brightness;
- eyelid coverage;
- eyelid orientation;
- temporary squash/stretch;
- blink state.

The eye shall not routinely become:

- a heart;
- star;
- triangle;
- cross;
- icon;
- unrelated cartoon symbol.

A sleeping eye may collapse toward a narrow line because this is interpreted as the same eye closing.

The design principle remains:

> **Makad's eyes behave like persistent body parts, not interchangeable screen symbols.**

---

# 3. Controlled Squash & Stretch

## C1-R03 — Bounded deformation

**MUST-HAVE**

Although the underlying eye primitive is circular, limited anisotropic scaling shall be allowed.

Each eye therefore supports:

```text
scale_x
scale_y
```

This permits subtle:

- squash;
- stretch;
- anticipation;
- impact;
- surprise;
- settling.

The deformation must remain sufficiently restrained that the eye still reads as Makad's circular eye rather than morphing into an unrelated shape.

Large permanent ovoid or polygonal expressions are outside the intended visual language.

---

# 4. Eyelid Geometry

## C1-R04 — Independent eyelid masks

**MUST-HAVE**

A simple scalar `closure` is insufficient for Makad's intended expression range.

Each eye shall therefore be rendered through independently controllable upper and lower eyelid masks.

Conceptually:

```text
top_lid_position
top_lid_angle

bottom_lid_position
bottom_lid_angle
```

for each eye independently.

This allows:

- horizontal sleepy closure;
- angled annoyed closure;
- asymmetric questioning expressions;
- partial squints;
- different left/right lid attitudes;
- expressive blinking.

The underlying eye remains circular; expression is created by **revealing or obscuring portions of that circle**.

---

# 5. Core Eye Parameter Model

## C1-R05 — Parameterized eye pose

**MUST-HAVE**

Each eye shall expose approximately the following continuously variable parameters:

```text
EYE

center_x
center_y

radius

scale_x
scale_y

brightness

top_lid_position
top_lid_angle

bottom_lid_position
bottom_lid_angle
```

Derived convenience values such as:

```text
openness
blink_amount
squint
```

may exist, but should ultimately resolve into the lower-level geometry.

Left and right eyes must remain independently controllable.

This asymmetry is considered an important expressive tool.

---

# 6. Visual Design Language

## C1-R06 — Dot/phosphor identity

**MUST-HAVE**

Makad's display shall use a deliberately visible aesthetic inspired by:

- phosphor displays;
- dot-matrix displays;
- pixel grids;
- halftone patterns;
- retro electronic terminals;
- industrial/droid interfaces.

The aesthetic applies to:

1. the eyes;
2. animation;
3. utility GUI;
4. text and status graphics.

The display should look like a piece of Makad rather than like a modern tablet screen.

---

# 7. Software-Defined Dot Grid

## C1-R07 — Continuous geometry, discrete-looking phosphors

**MUST-HAVE**

Makad's animation geometry shall **not** operate directly on integer dot coordinates.

All eye and animation geometry shall be calculated in:

**continuous floating-point space.**

The phosphor grid is applied only during rendering.

Conceptually:

```text
Continuous eye geometry
        ↓
Continuous animation interpolation
        ↓
Virtual phosphor grid sampling
        ↓
Per-cell brightness / coverage
        ↓
Physical display
```

---

## C1-R08 — Phosphor cells are not binary

**MUST-HAVE**

Virtual phosphor cells shall support continuously variable intensity.

A dot shall not merely be:

```text
ON
OFF
```

Instead:

```text
intensity = 0.0 → 1.0
```

As an eye moves between dot locations, neighbouring dots should smoothly cross-fade according to geometric coverage.

Possible implementation techniques include:

- supersampling;
- signed-distance functions;
- smooth coverage masks;
- antialiased sampling.

This allows Makad to preserve the visible dot-grid aesthetic without creating stepper-motor-like eye motion.

---

## C1-R09 — Logical grid density

**MUST-HAVE**

The virtual grid must be dense enough that sub-cell interpolation produces visibly smooth gaze motion.

Initial design floor:

**≥64 virtual phosphor columns across the active face width.**

Preferred target:

**approximately 96+ columns**, if the desired dot size and physical display allow it.

The final density shall be confirmed visually during display prototyping rather than selected solely from this number.

---

# 8. Display Programmability

## C1-R10 — General-purpose framebuffer

**MUST-HAVE**

The display architecture must permit arbitrary programmatic rendering.

We must be able to easily:

- modify the face;
- add/remove expressions;
- add animation primitives;
- show text;
- create GUI pages;
- display timers;
- display status;
- create diagnostics;
- experiment rapidly.

Therefore the visual identity shall be implemented primarily in software rather than being dictated by specialized fixed-function display hardware.

---

## C1-R11 — No touchscreen dependency

Makad does not require touch input.

Touch shall not influence display selection unless it comes essentially free with an otherwise ideal display.

---

# 9. Colour Policy

## C1-R12 — Restricted face palette

**MUST-HAVE DESIGN RULE**

Makad's face shall use a **single primary phosphor identity hue** or a very tightly restricted near-monochrome palette.

The exact hue will be chosen during visual design.

Emotions shall **not** normally be encoded using:

```text
red = angry
blue = sad
green = happy
```

Makad's personality must come from motion and timing.

A full-colour physical panel may still be selected for flexibility, but this does not imply full-colour facial animation.

Rare colour deviations may later be deliberately authored for exceptional system/events, but shall not become the normal emotional vocabulary.

---

# 10. Character Animation Philosophy

Makad's visual inspiration is the **economy of expression** found in highly animated non-human characters such as EVE.

We are not copying the reference character's eye geometry.

Makad retains:

- circular base eyes;
- its phosphor-grid aesthetic;
- its mechanical/droid body;
- its own motion language.

The principle being borrowed is:

> **Simple geometry + exceptional gaze, timing, anticipation and physical motion can produce rich character expression.**

Therefore expressive quality should primarily emerge from:

- eyelid geometry;
- gaze;
- eye spacing;
- eye scale;
- brightness;
- asymmetry;
- timing;
- pauses;
- anticipation;
- head motion;
- body motion;
- sound.

---

# 11. Rendering Performance

## C1-R13 — Continuous real-time rendering

**MUST-HAVE**

Makad's renderer remains continuously resident while the robot is awake.

Minimum operating target:

**30 FPS**

Preferred final target:

**60 FPS**

A new process/application shall not be launched every time an expression changes.

---

## C1-R14 — Frame consistency

Average FPS alone is not an adequate performance measure.

### Minimum 30 FPS operating profile

- typical frame time: approximately ≤33 ms;
- p99 frame time should remain approximately ≤33 ms where practical;
- no normal animation frame should exceed approximately **50 ms**.

### 60 FPS target profile

- most frames should render within approximately **16.7 ms**;
- p99 target: **<20 ms**;
- no periodic large animation hitching.

A smooth stable 30 FPS implementation is preferable to a nominal 60 FPS renderer that periodically stalls for hundreds of milliseconds.

---

# 12. Three-Layer Character Model

Makad's animation framework shall contain three conceptual layers.

---

## Layer A — Character State

Provides the underlying base pose.

Examples:

```text
neutral
happy
excited
curious
surprised
confused
annoyed
attentive
thinking
sleepy
sleeping
waking
startled
```

States define base tendencies rather than complete animations.

---

## Layer B — Procedural Life

Adds bounded low-priority activity such as:

- spontaneous blinking;
- small gaze corrections;
- eye settling;
- subtle scale changes;
- small head corrections;
- environmental inspection.

These modifications exist **on top of the state**.

---

## Layer C — Choreographed Gestures

Authored temporal behaviours such as:

```text
notice_person
hear_name
startle
wake_up
investigate
lose_person
acknowledge
become_confused
fall_asleep
```

Gestures control selected channels for finite periods.

---

# 13. Arbitration Model

## C1-R15 — Explicit channel ownership

**MUST-HAVE**

The three animation layers shall not be allowed to write arbitrarily to the same variables.

The framework shall implement explicit per-channel arbitration.

Initial logical channels include:

```text
gaze
eye_position
eye_scale
eyelids
brightness

head_pose
body_pose

audio_expression

optional_future_channels
```

Locomotion may later register as an additional channel but is **not required by Capability #1**.

---

## C1-R16 — State provides the base pose

**MUST-HAVE**

Character state establishes the underlying/default parameter values for every channel.

Example:

```text
STATE = SLEEPY

base eyelid openness = low
base gaze activity = low
base brightness = slightly reduced
base movement energy = low
```

---

## C1-R17 — Procedural life is bounded/additive

**MUST-HAVE**

Procedural activity normally contributes small bounded offsets to the underlying pose.

Example:

```text
final gaze =
tracked gaze
+
small procedural gaze offset
```

Procedural animation may not completely override an important explicit target unless intentionally permitted.

---

## C1-R18 — Gesture channel leases

**MUST-HAVE**

A gesture may request temporary ownership of one or more named channels.

Conceptually:

```text
gesture.acquire(
    channels = [eyelids, eye_scale],
    priority = HIGH,
    duration = 400 ms,
    blend_in = ...,
    blend_out = ...
)
```

While a lease is active:

- the gesture controls those channels;
- unrelated channels remain available to other systems;
- ownership automatically expires;
- control blends back to the currently valid underlying value.

The framework must never return to a stale parameter snapshot captured before the gesture began.

---

## C1-R19 — Priority and interruption rules

**MUST-HAVE**

Higher-priority behaviours may pre-empt lower-priority behaviour.

Expected order conceptually:

```text
SYSTEM / FAULT / SAFETY
        ↓
HIGH-PRIORITY REACTION
        ↓
NORMAL GESTURE
        ↓
EXPLICIT ATTENTION / TRACKING
        ↓
PROCEDURAL LIFE
        ↓
BASE STATE
```

Actual priority numbers are implementation details.

Examples:

**Startle during blink**

The startle gesture may immediately acquire the eyelid channel and force the eyes open.

**State change during gesture**

The new state changes the underlying base pose while the gesture continues.

When the gesture releases control, it blends toward the **new** state.

**New high-priority gesture**

May cancel or crossfade an existing lower-priority gesture using the affected channels.

---

# 14. Expression Strength

## C1-R20 — Presentation strength

The semantic API may include:

```text
set_expression(name, strength)
```

where `strength` simply controls the amount of visual/motion blending applied.

This is **not** the same thing as implementing a continuous autonomous emotional model.

Therefore:

**Expression strength = core animation framework feature.**

**Continuous internal emotional psychology = STRETCH.**

This resolves the previous inconsistency.

---

# 15. Canonical Expression Library

## C1-R21 — Authored states

Makad shall provide at least:

1. Neutral
2. Happy
3. Excited
4. Curious
5. Surprised
6. Confused
7. Annoyed
8. Attentive/listening
9. Thinking
10. Sleepy
11. Sleeping
12. Waking
13. Startled

At least eight shall eventually be demonstrated as meaningfully distinguishable.

Lid orientation, asymmetry and subtle squash/stretch may be used while preserving circular eye identity.

---

# 16. Gaze Model

Because Makad has no pupils, visual gaze is primarily expressed by translating the eyes within the display.

This inherently limits the angular range that can be represented before physical head motion becomes necessary.

The software must explicitly account for this.

---

## C1-R22 — Body-relative attention target

**MUST-HAVE**

Higher-level perception shall not simply command:

```text
eyes_x = 20
```

Instead, the animation coordinator shall receive an **attention direction/target** relative to Makad's body or another explicitly named coordinate frame.

Conceptually:

```text
set_attention_target(
    bearing_yaw,
    bearing_pitch,
    frame = BODY
)
```

The exact API may later use a direction vector.

---

## C1-R23 — Head pose feedback

**MUST-HAVE DEPENDENCY**

The head subsystem shall eventually expose Makad's current estimated/measured:

```text
head_yaw
head_pitch
```

to the animation coordinator.

The face must use the **current head pose**, not merely the commanded pose.

---

## C1-R24 — Head-compensated fixation

**MUST-HAVE**

Desired eye offset shall be calculated approximately from:

```text
target direction
-
current head direction
=
required residual eye direction
```

As Makad's head rotates toward something:

**the eyes shall counter-move toward centre while maintaining fixation on the target.**

Conceptually:

```text
Target appears right

Eyes move right
      ↓
Head begins turning right
      ↓
Eyes gradually move back toward centre
      ↓
Head arrives
      ↓
Eyes are approximately centred while still looking at target
```

This VOR-like counter-motion is a core Makad character behaviour.

---

## C1-R25 — Eye travel limits

**MUST-HAVE**

The eye renderer shall define safe travel bounds.

If the required gaze direction exceeds what the screen can convincingly represent:

1. eyes move toward the allowed limit;
2. head begins following;
3. eye offset reduces as head orientation catches up.

Thus eye-first/head-second motion becomes both:

- an expressive technique; and
- part of the gaze geometry solution.

---

# 17. Eye/Head Attention Timing

## C1-R26 — Attention propagates outward

A typical attention sequence shall be:

```text
stimulus detected
      ↓
eye saccade
      ↓
short authored delay
      ↓
head movement
      ↓
body orientation if required
      ↓
future locomotion if required
```

The delays are behaviour-specific rather than globally fixed at 100 ms.

For some events they may be almost simultaneous.

For others, deliberate hesitation may communicate curiosity or uncertainty.

---

# 18. Blink System

## C1-R27 — Spontaneous and event-coupled blinking

**MUST-HAVE**

Blinks shall not occur only from a random timer.

Blink probability/timing should be influenced by events such as:

- significant gaze shifts;
- completion of some saccades;
- head-turn transitions;
- emotional/state transitions;
- waking/sleeping;
- conversational turn boundaries.

Makad still performs spontaneous blinks, but they should exist within the character's behaviour rather than being completely independent random events.

---

# 19. Long-Term Idle Behaviour

## C1-R28 — Slow behavioural drift

**MUST-HAVE**

Idle animation shall not consist solely of individual events triggered at randomized times.

The framework shall maintain at least one slowly changing internal **animation-drive variable**, conceptually:

```text
activity / arousal
```

with significant temporal momentum.

This variable may modulate:

- blink interval;
- saccade frequency;
- gaze dwell time;
- amount of micro-motion;
- inspection frequency;
- eye scale;
- movement energy.

The value should evolve over **tens of seconds to minutes**, not jitter frame-to-frame.

This produces periods where Makad feels:

- quietly settled;
- attentive;
- inquisitive;
- gradually sleepy;

rather than uniformly random.

This is an animation-control variable, not a full emotional-cognition model.

---

# 20. Speaking Behaviour

## C1-R29 — Visible speaking state

**MUST-HAVE**

Because Makad has no mouth, it must still visually communicate that **it** is currently speaking.

The eyes shall not simply remain frozen while audio plays.

Potential speaking animation signals include:

- extremely subtle radius modulation;
- subtle brightness modulation;
- changes in gaze stability;
- emphasis blinks;
- coordinated head micro-bobs;
- expression changes aligned with prosody.

If audio-driven modulation is used, it should respond to a smoothed **speech/prosody envelope**, not raw waveform oscillation.

The result must remain restrained enough that Makad's eyes do not resemble audio visualizers.

There is no lip synchronization requirement.

---

# 21. Multi-Channel Animation Architecture

Capability #1 shall assume an **extensible channel architecture**, not hard-code the existence of every future mechanical subsystem.

Core initial channels:

```text
FACE
HEAD
AUDIO
```

Future systems may register:

```text
BODY
LOCOMOTION
OTHER EXPRESSIVE ACTUATORS
```

Therefore Capability #1 defines the choreography framework and interfaces but does **not** freeze wheel/body timing tables before those systems exist.

---

# 22. Display Physical Requirements

Exact display hardware remains unfrozen, but several hardware constraints now exist before selection.

---

## C1-R30 — Face assembly mass budget

**PROVISIONAL HARD SELECTION GATE**

Until Capability #2 provides a proper neck torque/mass budget:

> **Panel + display driver electronics + immediate display mounting hardware should target ≤120 g total.**

A heavier candidate shall not be selected without explicit reconsideration during the head/neck torque calculation.

This limit may become stricter once Capability #2 is engineered.

Lower mass is strongly preferred because expressive head acceleration is more important than simply achieving static neck torque.

---

## C1-R31 — Centre of mass

**MUST-HAVE DESIGN CRITERION**

Display electronics and mounting hardware should be positioned as close as practical to the neck's rotational axes.

A light display mounted far forward may be mechanically worse than a slightly heavier assembly positioned nearer the pivot.

Component selection shall therefore consider:

```text
mass × distance from joint
```

rather than mass alone.

---

## C1-R32 — Moving cable mechanics

**MUST-HAVE**

Display selection shall consider the moving cable harness as part of the mechanical system.

The display connection must not:

- strongly resist neck motion;
- noticeably bias the head toward one direction;
- sharply limit yaw/pitch travel;
- repeatedly bend at an unsuitable rigid point;
- place unsupported strain on connectors.

Preference should be given to architectures allowing:

- low-flex-force cable;
- sensible strain relief;
- routing near joint neutral axes;
- suitable repeated-flex behaviour.

A convenient electrical interface is not automatically a good moving-head interface.

---

## C1-R33 — Wide viewing behaviour

**MUST-HAVE**

Makad's display must remain readable when viewed:

- from above;
- from the side;
- while Makad's head is tilted.

IPS/OLED-class viewing behaviour or equivalent is therefore strongly preferred.

Panel candidates showing major:

- contrast inversion;
- colour inversion;
- severe brightness loss;

at ordinary off-axis desktop viewing angles shall be rejected.

---

# 23. Screen Form

## C1-R34 — Mechanical droid bezel

Makad deliberately retains:

- substantial bezel;
- visible screws;
- layered printed structure;
- mechanical seams;
- recessed screen mounting.

No edge-to-edge consumer-electronics appearance is required.

---

## C1-R35 — Curved-display appearance

**TARGET**

CRT-like visual depth may be produced through:

- mechanical bezel geometry;
- recessed mounting;
- rounded opening;
- software barrel distortion;
- phosphor rendering.

---

## C1-R36 — Genuine curved panel

**STRETCH**

A physically curved/flexible display shall only be used if it satisfies:

- cost;
- mass;
- availability;
- aspect ratio;
- reliability;
- cable mechanics;
- mounting difficulty.

Makad V1 shall not depend on one.

---

# 24. Brightness & Ambient Conditions

## C1-R37 — Programmatic brightness

**MUST-HAVE**

Display brightness must be software controllable.

Makad should support at minimum:

```text
normal
dim
sleep/off
```

brightness behaviours.

---

## C1-R38 — Ambient-light adaptation

**TARGET**

Makad should eventually adapt its display brightness to ambient conditions.

The input may originate from:

- a dedicated ambient-light sensor; or
- another sufficiently reliable system-level estimate.

The exact sensing mechanism is not frozen under Capability #1.

The goal is to prevent an excessively bright face in dark rooms and permit time-of-day behaviour.

---

# 25. Boot, Shutdown & Failure Behaviour

## C1-R39 — No exposed operating-system UI

**MUST-HAVE**

Normal Makad operation shall never intentionally expose:

- Linux console text;
- desktop environment;
- generic boot logo;
- rainbow splash;
- application crash window;

on the face display.

Before the character renderer is ready, the preferred presentation is:

**dark/blank display.**

---

## C1-R40 — In-character boot

**TARGET**

Makad's normal startup should transition approximately:

```text
screen dark
   ↓
renderer ready
   ↓
sleeping/closed eyes appear
   ↓
wake animation
   ↓
idle
```

---

## C1-R41 — In-character shutdown

**TARGET**

Normal shutdown should allow:

```text
active face
   ↓
sleepy transition
   ↓
eyes close
   ↓
screen dims/off
```

where practical.

---

## C1-R42 — Degraded state

**MUST-HAVE**

Makad shall have an identifiable character-consistent degraded/fault presentation.

Examples:

```text
audio unavailable
camera unavailable
AI service unavailable
thermal issue
battery critically low
```

Diagnostic details may appear in the utility GUI, but normal face mode should not suddenly become a raw error console.

---

# 26. Face/Motion Watchdog Relationship

## C1-R43 — Renderer heartbeat

**MUST-HAVE INTERFACE**

The face renderer shall expose a health/heartbeat signal to the higher-level controller.

If facial rendering unexpectedly stalls while expressive mechanical motion continues, Makad immediately loses the intended character illusion.

Therefore the system architecture shall allow a renderer failure to cause expressive motion to:

- pause;
- settle;
- or enter another defined safe/degraded behaviour.

Exact safety behaviour belongs to the central behaviour/control specification.

---

## C1-R44 — System health input

The face controller shall also receive relevant subsystem-health information so it can enter:

```text
normal
degraded
fault
shutdown
```

presentation states.

---

# 27. Utility GUI Integration

## C1-R45 — Same programmable display

Makad must support:

```text
FACE
 ↓
UTILITY UI
 ↓
FACE
```

without restarting the primary robot stack.

---

## C1-R46 — Same visual renderer

**TARGET**

Utility content should pass through the same Makad display-language layer wherever practical.

Thus:

```text
BATTERY
TIMER
STATUS
DEBUG OVERLAY
```

can retain:

- phosphor dots;
- restricted palette;
- retro typography;
- Makad-specific graphics.

The GUI remains flexible despite the stylized presentation.

---

# 28. Semantic Animation Interface

Higher-level code should control **intent**, not pixels.

Conceptually:

```text
set_state(state)

set_expression(
    name,
    strength = 1.0
)

set_attention_target(
    target,
    frame
)

trigger_gesture(
    gesture,
    priority
)

set_speaking(active, prosody_data)

set_brightness(mode)

show_utility_ui(view)

restore_face()
```

Head pose feedback conceptually enters through:

```text
update_head_pose(
    yaw,
    pitch
)
```

The exact API will be chosen during software design.

---

# 29. Renderer Pipeline

Preferred architecture:

```text
PERCEPTION / CONVERSATION / EVENTS
                ↓
        BEHAVIOUR SYSTEM
                ↓
     CHARACTER COORDINATOR
                ↓
      CHANNEL ARBITRATOR
                ↓
 ┌──────────────┼───────────────┐
 ↓              ↓               ↓
State       Procedural       Gestures
pose           life          / leases
 └──────────────┼───────────────┘
                ↓
       Resolved Eye Pose
                ↓
  Continuous Geometry Renderer
                ↓
   Virtual Phosphor Sampling
                ↓
     Brightness/Coverage Grid
                ↓
       Physical Display
```

Future mechanical channels attach to the coordinator without changing the underlying face renderer.

---

# 30. Acceptance Tests

## TEST C1-A — Stability

Run the complete face subsystem for:

**≥30 minutes**

while representative background audio/CV workloads operate.

### PASS

No:

- crash;
- progressive slowdown;
- memory leak causing degradation;
- visible long-term instability.

---

## TEST C1-B — Frame consistency

Collect frame-time telemetry during realistic operation.

### PASS

For the minimum operating profile:

- approximately ≥30 FPS;
- no recurring large stalls;
- no normal frames above approximately 50 ms.

### TARGET

At 60 FPS:

- most frames ≤16.7 ms;
- p99 approximately <20 ms;
- no recurring long hitch.

---

## TEST C1-C — Sub-cell gaze motion

Move the commanded eye position slowly across less than one virtual phosphor-cell width.

### PASS

The physical display shows smooth intensity migration between dots rather than a sudden one-cell jump.

---

## TEST C1-D — Expression evaluation protocol

Test at least **8 core expressions**.

Participants:

**≥10 naive observers**

Protocol:

1. randomized presentation order;
2. balanced number of samples per state;
3. forced choice from the known expression labels;
4. collect a confusion matrix.

Run at least a **face-only** condition.

When head/body/audio become available, repeat with the combined character.

### INITIAL FACE-ONLY TARGET

Approximately:

**≥65% overall correct classification**

across eight balanced options.

Chance performance is only 12.5%, so this provides a meaningful margin.

### MULTIMODAL TARGET

Approximately:

**≥80%**

for the final combined Makad expression system.

The confusion matrix matters more than headline accuracy: repeatedly confusing the same two states indicates those states need redesign.

---

## TEST C1-E — Eye-first target acquisition

Introduce a target requiring both eye and head movement.

### PASS

Makad:

1. moves the eyes first where appropriate;
2. begins head movement;
3. counter-rotates the eyes as the head approaches the target;
4. ends with the target visually fixated.

---

## TEST C1-F — Fixation compensation

Command a stationary attention target.

Move Makad's head through a moderate yaw range.

### PASS

The eyes counter-move appropriately instead of remaining rigidly centred relative to the head.

---

## TEST C1-G — Layer arbitration

Simultaneously activate:

```text
tracked gaze
+
procedural blink
+
temporary gesture
+
state transition
```

### PASS

No parameter fights, abrupt unexplained jumps or permanently stuck channels occur.

Control returns smoothly after each temporary lease expires.

---

## TEST C1-H — Gesture interruption

Trigger a high-priority startle during another expression/blink.

### PASS

The high-priority gesture takes control of only the required channels and the system returns cleanly to the valid underlying state afterward.

---

## TEST C1-I — End-to-end reaction latency

Define start:

**behaviour event dispatch**

Define end:

**first physically visible changed frame on the actual display**

Suggested measurement:

- flash a GPIO-connected reference LED at event dispatch;
- record LED and Makad's screen together using a high-frame-rate camera;
- count frame difference.

### PASS

**<200 ms**

### TARGET

**≤100 ms**

The measurement includes:

- software;
- compositor/rendering;
- display transport;
- physical panel latency.

---

## TEST C1-J — Long idle observation

Observe Makad awake and idle for:

**≥15–20 minutes.**

### PASS

Makad does not exhibit:

- a recognizable short repeating loop;
- uniform random twitching;
- frozen periods inconsistent with state.

Activity should instead appear to drift naturally over longer timescales.

---

## TEST C1-K — Speaking state

Play several spoken responses.

### PASS

An observer can generally distinguish:

```text
Makad is speaking
```

from:

```text
Makad is silently listening
```

without requiring a mouth.

The speaking animation must remain subtle and character-consistent.

---

## TEST C1-L — Off-axis readability

Observe the final display from realistic:

- standing;
- seated;
- side;
- tilted-head;

positions.

### PASS

Eyes remain clearly visible with no severe inversion or loss of readability.

---

## TEST C1-M — Boot/fault presentation

Test:

```text
cold boot
renderer restart
camera failure
audio failure
normal shutdown
```

### PASS

No raw operating-system/application interface appears during normal expected behaviour.

Makad presents either:

- darkness;
- an in-character state;
- a controlled utility diagnostic view.

---

# 31. Scope Classification

## MUST-HAVE

- exactly two eyes;
- no mouth;
- circular base-eye identity;
- independent angled eyelids;
- bounded squash/stretch;
- left/right asymmetry;
- software-defined phosphor grid;
- continuous floating-point geometry;
- variable cell intensity/sub-cell motion;
- general-purpose programmable display;
- ≥30 FPS stable rendering;
- frame-time consistency;
- three-layer animation architecture;
- explicit channel arbitration;
- gesture leases and interruption rules;
- canonical expression library;
- smooth interpolation/easing;
- body-relative gaze target;
- measured/estimated head-pose input;
- head-compensated fixation;
- eye travel limits;
- event-coupled blinking;
- slow idle-state drift;
- visible speaking state;
- programmatic brightness;
- in-character degraded behaviour;
- renderer health interface;
- no touchscreen dependency;
- utility GUI switching.

---

## TARGET

- approximately 60 FPS;
- p99 frame time <20 ms at 60 FPS;
- <100 ms reaction latency;
- highly polished canonical animations;
- approximately 96+ virtual phosphor columns;
- ambient-light adaptation;
- refined speech/prosody animation;
- natural eye → head timing;
- long-term non-repetitive behaviour;
- in-character boot and shutdown;
- restricted phosphor palette across GUI;
- CRT-like screen presentation.

---

## STRETCH

- physically curved/flexible panel;
- sophisticated autonomous emotional-state model;
- advanced animation synthesis;
- dynamically generated complex gestures;
- unusual exceptional colour states;
- advanced CRT/phosphor simulation.

---

# 32. Explicitly Out of Scope

Capability #1 does not require:

- mouth animation;
- lip sync;
- pupils;
- human avatars;
- arbitrary symbolic eye shapes;
- photorealistic graphics;
- touchscreen input;
- high-end GPU rendering;
- frame-by-frame GIF libraries;
- full emotional colour coding;
- SLAM/world localization merely for gaze;
- physically curved display hardware;
- completed locomotion choreography.

---

# 33. Frozen Capability #1 Definition

**Makad shall use exactly two persistent circular eyes and no mouth or other permanent facial anatomy. Each eye is constructed from a circular base primitive rendered through independent position, radius, bounded squash/stretch, brightness and angled upper/lower eyelid masks. This preserves Makad's circular-eye identity while providing sufficient geometry for expressive states such as curiosity, annoyance, sleepiness, surprise and asymmetry.**

**All geometry shall be animated continuously in floating-point space and subsequently sampled onto a software-generated phosphor/dot grid whose individual cells support continuous brightness. The grid therefore provides a gritty dot-matrix appearance without sacrificing sub-cell motion, smooth gaze or arbitrary GUI programmability. At least 64 virtual columns across the active face shall be treated as an initial density floor, with approximately 96 or more preferred where visually appropriate.**

**Makad's Character Animation Framework shall consist of a base character state, bounded procedural-life modifiers and authored gestures. These layers shall not compete directly for variables: states establish base poses, procedural life contributes bounded offsets, and gestures obtain finite priority-controlled leases over named channels with explicit blend-in, blend-out and interruption rules. Higher-priority system/fault behaviour may pre-empt normal animation.**

**Gaze shall be represented as an attention direction relative to Makad's body rather than as direct eye-screen coordinates. The coordinator shall combine this target with measured/estimated head pose so that Makad's eyes initially acquire the target, the head subsequently follows, and the eyes counter-rotate toward centre as the neck turns while maintaining fixation. Eye travel limits shall explicitly trigger head-follow behaviour when the target exceeds the face's available gaze range.**

**Blinks shall be both spontaneous and event-coupled. Idle behaviour shall include slow internal activity drift over tens of seconds or minutes so Makad exhibits changing periods of attentiveness rather than merely randomized repetitive motion. Makad shall also have a dedicated speaking presentation, using restrained eye/head animation and optionally a smoothed speech-prosody envelope rather than a mouth or lip synchronization.**

**The face display shall be fully programmable, require no touchscreen, retain good off-axis viewing behaviour, support programmatic brightness and use a tightly restricted phosphor identity palette rather than encoding emotion primarily through colour. Until Capability #2 produces the final neck torque budget, the moving display/driver/immediate-mount assembly should target no more than approximately 120 g, with low mass, low moment arm and low-resistance moving cable routing treated as core component-selection criteria.**

**The display shall never intentionally reveal operating-system boot or crash interfaces during normal use. Boot, shutdown and degraded operation shall have controlled character-consistent presentations, and the renderer shall participate in the system watchdog architecture so a frozen face cannot continue indefinitely on an actively moving robot.**

**Capability #1 defines an extensible animation-channel architecture. Face, head and audio are immediately relevant; body and locomotion can later attach to the same coordinator without Capability #1 prematurely freezing choreography against mechanical systems that have not yet been built.**