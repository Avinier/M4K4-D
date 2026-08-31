# Makad — MEMORY.md

> **Append-only project decision log**  
> Reconstructed and initialized: **2026-08-13**

This file records the evolution of Makad: decisions, reversals, important technical discoveries, scope changes, and unresolved items.

It is intentionally different from `README.md`.

- `README.md` describes the **current project truth**.
- `MEMORY.md` records **how we got there**.

---

## Append-only rules

From this point onward:

1. **Do not delete old entries.**
2. **Do not edit an old decision to make history look cleaner.**
3. If a decision changes, append a new entry whose `Supersedes:` field names the old entry. **Never edit the superseded entry or its status.**
4. Corrections are appended as corrections; they do not rewrite the original entry.
5. New entries should contain:
   - date;
   - entry ID;
   - status/type;
   - decision/event;
   - reason;
   - consequences / affected specs;
   - exact requirement/test IDs when a canonical requirement is cited;
   - open follow-up if any.
6. Requirement documents remain the authoritative source for exact requirement wording.
7. This initial file is a chronological reconstruction from project discussions rather than a literal git log of every sentence ever written.
8. `MEMORY.md` contains dated entries only. Mutable current-state and open-question registers live in `README.md`.
9. Use `UNTRACED` rather than inventing a requirement ID when the canonical source is unavailable; the entry must name the follow-up OQ.

Recommended future entry format:

```md
### MEM-YYYYMMDD-NN — Short title
**Type:** DECISION | CHANGE | REVIEW FINDING | CORRECTION | OPEN | VALIDATION | BUILD  
**Status:** CURRENT | PROVISIONAL | RESOLVED  
**Supersedes:** MEM-YYYYMMDD-NN (only when applicable)  
**Requirements:** Cxx-Ryy, Cxx-Tyy (or `UNTRACED — OQ-21`)

What changed.

**Why**
- ...

**Consequences**
- ...

**Follow-up**
- ...
```

---

# Reconstructed history

## 2026-08-03

### MEM-20260803-01 — AURA direction begins collapsing into a smaller companion robot
**Type:** CHANGE  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The project had previously explored a broader embodied assistant concept, AURA, including camera perception, a robotic arm, pick-and-place, voice commands, user/object memory and assistive use cases.

The direction began shifting away from a manipulation-heavy assistant and toward a smaller companion robot where the hard problem would be expression, perception, interaction and hardware integration.

**Why**
- A 4–5 month beginner project needed a tighter physical scope.
- The desire was to learn real robotics/mechatronics rather than build another mostly-software AI demo.
- A small companion platform created room to go deeper on motion, audio, perception and embodiment.

**Consequences**
- Manipulation stopped being the defining project axis.
- The later Makad concept became the new project identity.

---

## 2026-08-07

### MEM-20260807-01 — Makad becomes the project
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Supersedes:** MEM-20260803-01

The desktop companion robot was named **Makad** (“monkey”).

The reference space became:

- small expressive desk robots;
- EVE-like expressive economy;
- Star Wars droids such as R2-D2 / BB-8 for character timing and mechanical personality;
- maker/open-source robot construction rather than sealed toy construction.

**Why**
- The project should be cute and characterful while still forcing difficult engineering.
- The physical build itself should teach robotics hardware fundamentals.

**Consequences**
- “Feeling alive” became a first-class design goal.
- The robot would be designed as a hackable platform rather than a fixed appliance.

---

### MEM-20260807-02 — Mechanical visual direction
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The shell direction was set toward:

- mechanical / droid-like;
- sharp-ish corners;
- pseudo sheet-metal panel language;
- 3D-printed screw-together construction;
- serviceable panels;
- visible camera;
- speaker area;
- `MAKAD` branding;
- monkey-like side-ear silhouette.

The side ears were retained because they gave Makad an identifiable character without forcing a literal monkey face.

**Why**
- The robot needed a distinctive identity.
- The design still had to be printable with limited CAD experience and a short build schedule.

**Consequences**
- Smooth sealed consumer-electronics styling became the wrong direction.
- Serviceability became part of the visual language.

---

### MEM-20260807-03 — Hardware first, software later
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The project explicitly chose to focus first on hardware/build fundamentals, using the mechanical/electrical platform as a later blank canvas for voice, CV, LLM/VLM and richer software.

**Why**
- The builder already had a stronger software/AI background.
- The learning objective required spending difficulty budget on unfamiliar hardware/mechatronics.

**Consequences**
- Early discussions moved toward mechanisms, loads, control, mounting and integration instead of immediately selecting AI models.

---

## 2026-08-08

### MEM-20260808-01 — Wheels become an official capability
**Type:** CHANGE  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

Mobility was added to Makad.

The desired feel was described with BB-8 as an expressive reference, but it was clarified that Makad would **not** copy BB-8’s spherical mechanism.

A conventional wheeled base became the direction.

**Why**
- Translational/body motion greatly increases character.
- A mobile base creates expressive possibilities such as turning toward someone, approach, hesitation, recoil and spin.

**Consequences**
- The project gained a major new mechatronics subsystem.
- Centre of mass, power, safety, wheel control, body geometry and audio vibration became cross-system problems.

---

### MEM-20260808-02 — Two driven wheels do not imply self-balancing
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The base direction became a differential drive with:

- two powered wheels;
- independent wheel control;
- a passive caster/support.

Makad is therefore statically supported and does not need inverted-pendulum balancing.

**Consequences**
- No self-balancing control problem is required for V1.
- The base can rotate near in place and execute expressive body yaw.

---

## 2026-08-09

### MEM-20260809-01 — Face identity freezes around eyes only
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

Makad’s display language was narrowed deliberately:

- eyes only;
- **no mouth**;
- simple circular eye identity;
- dot-matrix / phosphor / halftone / pixel-grid aesthetic;
- procedural/layered animation;
- roughly 30–60 fps acceptable.

**Why**
- EVE demonstrated that strong expression does not require a conventional face.
- A mouth would push Makad toward generic emoji/cartoon language rather than droid-like attention.

**Consequences**
- Later concept art showing a mouth is historical reference only and is non-canonical.
- Gaze/head/body coordination carries more expressive burden.

---

### MEM-20260809-02 — Expression parameters expand beyond circles moving on screen
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The face system was allowed to use richer parameters while preserving circular-eye identity, including:

- closure;
- blink;
- widening;
- squint;
- asymmetric lids;
- lid angles;
- nonuniform scale where necessary;
- position and brightness;
- sleep/wake behavior.

**Why**
- Pure x/y/radius control was insufficient for the intended emotional vocabulary.

**Consequences**
- The display system is a parameterized animation system, not a sprite player.

---

### MEM-20260809-03 — Head motion becomes an engineering subsystem, not a servo demo
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

Natural head movement was identified as central to Makad.

Desired motion included:

- yaw;
- pitch;
- possible roll;
- bobbing;
- small tracking corrections;
- expressive tilts;
- gaze-oriented motion;
- coordinated motion with eyes/body.

The discussion expanded into:

- servo horn loading;
- cantilever risk;
- actuator torque;
- gravitational/quasi-static torque;
- dynamic torque;
- backlash;
- closed-loop actuation;
- repeatability;
- mechanical support.

**Why**
- Several-degree expressive motions are visibly damaged by even small drivetrain slop.
- A top-heavy head makes casual actuator sizing risky.

**Consequences**
- Torque and backlash would be derived quantitatively.
- Head load should be structurally supported.
- Physical feedback matters.

---

### MEM-20260809-04 — Backlash becomes proportional to expressive scale
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

A conflict was identified between:

- small intended expressive moves;
- ~1°-class repeatability goals;
- permissive backlash values.

The project rejected treating “a few degrees of backlash” as acceptable simply because the joint still reaches large poses.

**Why**
- A 2° deadband is enormous if the intended expressive motion is only 4°.

**Consequences**
- Small-motion reversal tests became part of neck validation.
- Backlash became a character-quality metric.

---

### MEM-20260809-05 — 20-point functional list becomes source of truth
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The project froze a 20-point functionality list and stopped free-form feature accumulation.

The process became:

**functionality → requirements → subsystem specs → architecture → budgets → parts → BOM → CAD/build**

Every capability would be analyzed for:

- exact behavior;
- performance;
- mechanical implications;
- electronics;
- compute;
- software;
- interfaces;
- power;
- acceptance;
- MUST/TARGET/STRETCH status.

**Why**
- Component selection made independently per feature would create conflicts.
- Several capabilities share the same physical subsystems.

**Consequences**
- Exact parts would not be locked while walking through the 20 items one by one.
- Cross-subsystem consistency became mandatory.

---

## 2026-08-10

### MEM-20260810-01 — Neck spec hardens into measured camera-bearing architecture
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The neck work matured from “2–3 DOF expressive head” into a measured mechanism.

Carried-forward architecture:

- yaw + pitch MUST;
- architecture designed around roll;
- powered roll TARGET;
- yaw → pitch → roll kinematic intent;
- physical joint pose available to control/perception;
- camera transform derived from calibrated geometry + measured joints;
- mass, COM and moment of inertia calculated;
- dynamic torque sized per axis;
- degraded modes defined;
- motion logging and external video validation required.

**Consequences**
- Neck actuator and encoder choices remain downstream decisions.
- Perception cannot assume commanded angle equals true camera pose.

---

### MEM-20260810-02 — Small head-motion acceptance becomes quantitative
**Type:** VALIDATION  
**Status:** PROVISIONAL  
**Provenance:** RECONSTRUCTED

The neck validation direction included:

- repeated approximately `+4° ↔ -4°` reversal tests;
- ≤1° lost motion as an important current pass level;
- ≤0.5° stronger target;
- approximately ±0.5° physical repeatability target;
- slow trajectory smoothness tests;
- stationary-target jitter measurement;
- moving-camera compensation tests;
- ≥100 Hz-class telemetry where hardware permits;
- ~240 fps phone video as independent measurement.

**Why**
- Controller logs alone can hide physical backlash and flex.

---

### MEM-20260810-03 — Eyes/head/base attention model clarified
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The interaction model was corrected away from treating eyes, head and base as interchangeable orientation stages.

The intended perceptual sequence became:

**eyes signal attention first; head establishes physical gaze; body/base handles large orientation changes.**

**Consequences**
- A dedicated gaze controller became important.
- Base orientation must preserve rather than destroy the social signal of looking at someone.

---

### MEM-20260810-04 — Real-time speech remains, traditional conversation becomes optional
**Type:** CHANGE  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The project moved away from “Makad must converse like a normal English assistant.”

It retained:

- real-time speech input;
- low-latency turn handling;
- semantic understanding;
- ability to respond to useful commands/questions.

But Makad’s own primary voice became a droid-like channel rather than mandatory ordinary English speech.

**Why**
- Star Wars droid communication better matched the intended character.
- The project’s interesting engineering problem is embodied interaction, not another chatbot shell.

**Consequences**
- Speech recognition and semantic intent remain engineering requirements.
- Creative droid-language design was explicitly deferred.

---

### MEM-20260810-05 — Droid voice creates harder AEC requirements
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The review identified that tonal chirps/whistles can be poor excitation for adaptive echo cancellation.

The difficulty compounds when:

- Makad vocalizes often;
- head motion changes the acoustic path during sound;
- barge-in is required;
- output and motion are intentionally synchronized.

**Consequences**
- AEC is not merely “more important”; it is harder.
- The later sound vocabulary should include useful spectral diversity.
- Audio hardware geometry and motion coordination matter to the creative language.

---

### MEM-20260810-06 — Partial speech must not accidentally cause physical action
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

As speech began mapping into physical actions, a review flagged that partial/stale recognition results cannot be permitted to create irreversible motion.

**Consequences**
- Utterance/session IDs and cancellation semantics matter.
- Motion-producing actions require stronger confirmation/turn integrity than audio-only responses.
- A brief legible pre-action cue became an attractive repair/safety mechanism.

---

### MEM-20260810-07 — Visual tracking becomes layered temporal perception
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The perception stack was split so that raw detections do not directly control motion.

The tracking layer became responsible for:

- temporal tracks;
- attention selection;
- occlusion;
- loss;
- reacquisition;
- eye-line anchors;
- uncertainty;
- moving-camera compensation;
- timestamps;
- replayability;
- privacy boundaries.

**Consequences**
- Track ID is not human identity.
- Camera motion must be accounted for before interpreting image movement as person movement.

---

### MEM-20260810-08 — Moving-camera timing becomes explicit
**Type:** DECISION  
**Status:** PROVISIONAL  
**Provenance:** RECONSTRUCTED

The camera system was required to associate observations with **capture-time pose**, not whichever head angle happens to be current when software processes the frame.

Work included:

- time synchronization;
- rolling-shutter characterization;
- visual bearing uncertainty;
- active/idle perception modes;
- replay;
- false-lock tests involving screens/photos/mirrors.

**Consequences**
- Neck telemetry and perception timestamps are coupled system requirements.

---

## 2026-08-11

### MEM-20260811-01 — Audio/visual fusion proves two ear microphones are insufficient
**Type:** REVIEW FINDING  
**Status:** RESOLVED  
**Provenance:** RECONSTRUCTED  
**Resolved by:** MEM-20260811-02

The social-presence / fusion work exposed a structural problem with the earlier two-microphone ear-pod concept.

A two-mic single baseline has front/back ambiguity: a source behind the robot can produce the same inter-microphone timing as a different front bearing.

That can make an audio/visual association system confidently attach an off-camera speaker to the wrong visible person.

A directional-error analysis also produced an approximate need for acoustic uncertainty around the low-teens of degrees for the desired association performance.

**Consequences**
- The microphone-count question became architectural rather than cosmetic.
- A non-collinear 3+ mic array was required; four became the practical direction.

---

### MEM-20260811-02 — Four body-mounted MEMS microphones frozen for V1
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The microphone direction was frozen as:

- **4 MEMS microphones**;
- in the **body**;
- not in the head;
- not in the ear pods;
- non-collinear/wide array;
- rigid calibrated PCB/subframe;
- whole-array compliant isolation allowed;
- synchronized digital MEMS/PDM preferred;
- ear pods visual-only.

A directional uncertainty target around `σₐ ≤ 13°` was carried forward from the fusion requirements.

**Why**
- Front/back disambiguation.
- Better stable geometry.
- Better cross-modal association.

**Consequences**
- Old concept art showing “MIC LEFT / MIC RIGHT” ear pods is obsolete.
- Shell/CAD must preserve body-array geometry.

---

### MEM-20260811-03 — Shared capture/playback timing becomes an audio requirement
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The audio work required explicit timing for:

- microphone capture;
- audio playback;
- cross-modal fusion;
- echo cancellation;
- coordinated expressive timing.

An audio-visual synchronization target around the tens-of-milliseconds class was preferred, with exact values subject to validation.

**Consequences**
- The system cannot treat audio, camera and motion as independent asynchronous apps.

---

### MEM-20260811-04 — Presence reasoning gains ambiguity, freshness and session semantics
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The social-presence work identified multiple failure modes that had to become first-class states rather than hidden heuristics:

- multi-person handle swaps;
- “believed present but not currently observed”;
- stale bearing data;
- scene capacity saturation;
- ambiguous sound-person association;
- deterministic replay;
- event ordering;
- session lifetime;
- human head orientation / facing;
- addressing evidence.

**Consequences**
- Ambiguity/unknown are valid outputs.
- Presence handles are session-scoped, not biometric identity.
- Staleness must be visible to consumers.

---

### MEM-20260811-05 — Procedural aliveness is separated from authored performances
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED

The behavioural stack drew a hard boundary:

**Procedural aliveness** owns continuous/stochastic, low-amplitude “being alive.”

**Authored performances** own recognizable transients such as reactions, dramatic turns, approach, startle and other choreographed multi-channel gestures.

**Why**
- Mixing the two produces uncontrolled sequences and makes arbitration difficult.
- Procedural idle should remain generative and bounded rather than becoming a hidden animation library.

**Consequences**
- SPEC-12 and SPEC-13 have separate ownership.
- A prohibition on authored sequences applies to the procedural layer.

---

## 2026-08-12

### MEM-20260812-01 — Mobile-base safety review finds latency dominates stopping
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

A detailed SPEC-16 review showed that obstacle reaction latency can dominate physical braking distance across Makad’s expected speed envelope.

The key result was that bounding only a command-loss watchdog is not enough.

**Decision direction**
- obstacle/cliff safety must execute in the low-level real-time controller;
- it must be independent of the high-level process;
- detection-to-deceleration-command latency should be bounded around **≤50 ms**.

The stopping/detection inequality was reframed as:

`d_available > v * t_latency + v²/(2*a_brake) + d_margin`

**Consequences**
- Safe speed is heavily determined by the software/sensor path.
- Elevated-surface operation cannot blindly use the same speed as open floor operation.

---

### MEM-20260812-02 — IMU promoted from stretch toward MUST
**Type:** CHANGE  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

The mobile-base review rejected the claim that wheel encoder command-vs-measurement disagreement is sufficient to detect slip.

If a wheel spins on a slippery surface, the encoder may agree perfectly with the command while the robot does not move correctly.

The IMU was promoted because it helps detect:

- lift/pick-up;
- tip/fall;
- slip;
- stuck conditions;
- short-term yaw disagreement;
- odometry failure modes.

**Consequences**
- A low-cost 6-axis IMU is treated as architectural V1 equipment rather than sensor creep.

---

### MEM-20260812-03 — Base rotation turns body microphones into a rotating array
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

Mounting microphones in the body gave a stable array only while the body did not rotate.

Once Makad yaws:

- acoustic bearings exist in a rotating body frame;
- persistent sound tracks need body ego-motion compensation;
- locomotion must publish timestamped body yaw and yaw rate.

**Consequences**
- Audio now depends on locomotion state.
- Audio-visual fusion must eventually consume the compensated geometry.

---

### MEM-20260812-04 — Drive noise cannot be solved by beamforming alone
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

Gearmotor/motor vibration reaches multiple body microphones through the structure with nearly coherent timing.

This is not a normal far-field sound arriving from one direction.

**Consequences**
- Beamforming is not the primary cure.
- Mechanical isolation and/or motion inhibition are required.
- Drivetrain acoustic quality becomes relevant to audio quality.

---

### MEM-20260812-05 — Audio gains a locomotion-inhibit request
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

The architecture gained a motion-inhibit interface allowing audio/behaviour to suppress locomotion during active listening.

This is distinct from the safety inhibit.

**Why**
- Barge-in can happen precisely while an approach or other drive motion is loudest.
- Good hearing is more important than preserving every base gesture.

**Consequences**
- Base performances must degrade gracefully if motion is vetoed.
- Eyes/head/audio can continue carrying the interaction.

---

### MEM-20260812-06 — Expressive drive quality becomes a motor-selection criterion
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

Minimum controllable speed, reversal deadband and backlash were explicitly reframed as **expressive quality** criteria.

Makad’s characteristic small motions occur near zero speed with frequent reversals, exactly where geared drives look worst.

**Consequences**
- A motor that is fine for generic navigation may still be unacceptable for Makad.
- Hardware acceptance must include little wiggles and approach-hesitate-retreat sequences.

---

### MEM-20260812-07 — Blind fast reverse rejected
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

A conflict existed between expressive startle and drivetrain safety.

Resolution:

- startle begins with rapid **deceleration to stop**;
- eyes/head/audio carry the immediate intensity;
- any retreat happens afterward as a separate bounded reverse;
- no performance may request a fast blind reverse.

**Consequences**
- Performance authoring must respect low-level safety semantics.

---

### MEM-20260812-08 — Zero-velocity hold recognized as an expressive requirement
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

Head motion can apply reaction torque to the body.

If the drive coasts freely while commanded to remain still, the body may twitch opposite the head, which reads as mechanical slop rather than intentional aliveness.

**Consequences**
- The drive should resist reaction torque at zero commanded velocity.
- High gear reduction may help, but this must be validated rather than assumed.

---

### MEM-20260812-09 — Base footprint and rotation sweep become explicit mechanical concerns
**Type:** REVIEW FINDING  
**Status:** PROVISIONAL  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-20, OQ-21

For near-in-place turning, body footprint geometry matters.

A preferred design is for the base body footprint to remain within the circle swept around the drive-wheel axle midpoint.

The head may protrude beyond this protected floor-level region.

**Consequences**
- Head-height sweep may require its own documented limit or geometry constraint.
- Floor-level obstacle sensors cannot automatically protect protruding head geometry.

---

### MEM-20260812-10 — Low-level obstacle recovery is identified
**Type:** REVIEW FINDING  
**Status:** PROVISIONAL  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-11, OQ-21

Stopping at an obstacle is insufficient for autonomous low-level recovery.

A possible low-level sequence became:

1. stop;
2. bounded slow reverse;
3. turn;
4. resume.

Rear-space uncertainty remains important.

**Consequences**
- Recovery behavior must not depend entirely on high-level AI being alive.
- Rear sensing versus tightly bounded blind crawl remains a design decision.

---

### MEM-20260812-11 — SPEC-12 amended for the mobile base
**Type:** CHANGE  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

The procedural aliveness layer was extended to acknowledge that the base is now an available channel.

Important boundaries:

- procedural base motion is not navigation;
- it is not authored approach/retreat/spin performance;
- it may contribute only small micro-motion;
- the contribution is summed before SPEC-16 safety clamping;
- performance/navigation overrides it;
- active-listening inhibit suppresses it;
- sleep forces it to hard zero.

**Consequences**
- Procedural and performance ownership remain clean.

---

### MEM-20260812-12 — Continuous base drift rejected in favor of discrete micro-moves
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

SPEC-16’s expected minimum controllable speed made truly tiny continuous wheel drift unrealistic.

The base procedural layer therefore adopted a model analogous to saccade-and-dwell:

- brief motion above the validated controllable threshold;
- stop;
- stochastic dwell;
- another bounded micro-move.

**Why**
- Stiction/backlash/quantization make continuous sub-threshold motion look broken.

**Consequences**
- Procedural base aliveness is event-like at the physical wheel level even though it belongs to the procedural layer.

---

### MEM-20260812-13 — Procedural random walk must remain spatially bounded
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

Unlike eyes or neck, base position integrates over time.

An unbiased idle random walk would eventually move Makad across the table/floor.

**Consequences**
- Procedural base displacement needs either:
  - return-to-origin bias using odometry; or
  - a bounded net displacement window.
- Odometry drift means the origin itself is imperfect.

---

### MEM-20260812-14 — Proximity suppresses procedural base motion before safety catches it
**Type:** DECISION  
**Status:** CURRENT  
**Provenance:** RECONSTRUCTED  
**Requirements:** UNTRACED — OQ-21

A robot repeatedly twitching into the obstacle/cliff safety clamp looks malfunctioning even if it remains physically safe.

**Consequences**
- Procedural base motion should be disabled near obstacles/edges before the low-level safety clamp becomes the visible behavior.

---

## 2026-08-13

### MEM-20260813-01 — Mobile base becomes a full performance channel
**Type:** CHANGE  
**Status:** CURRENT

SPEC-13 was amended so the base can participate in authored multi-channel performances.

SPEC-16 continues to own:

- physical locomotion;
- low-level control;
- safety;
- clamping.

SPEC-13 owns:

- coordination;
- timing;
- expressive intent.

**Consequences**
- Behaviour can author body-scale motion without bypassing drive safety.

---

### MEM-20260813-02 — Base perceptible onset recognized as slower than other channels
**Type:** DECISION  
**Status:** PROVISIONAL

A geared differential-drive base may need roughly **150–400 ms** before commanded motion becomes visibly perceptible due to:

- stiction breakaway;
- motor/gear response;
- acceleration ramp;
- body inertia.

Exact values require bench testing.

**Consequences**
- The base cannot be assumed to start with display/audio/neck on the same clock edge.

---

### MEM-20260813-03 — Reaction-class performances must not lead with the base
**Type:** DECISION  
**Status:** CURRENT

For reactions such as:

- startle;
- surprise;
- orient-to-sound;

the leading edge should be:

1. display/audio;
2. neck;
3. base follow-through if appropriate.

**Why**
- Trying to make the base lead would create visibly late, mushy reactions.

**Interpretation**
- This delay is not a defect.
- Eyes/head reacting before the larger body is perceptually natural.

---

### MEM-20260813-04 — Base yaw compensation and acceleration expression are separated
**Type:** DECISION  
**Status:** CURRENT

Two different neck/base couplings were separated.

**Base yaw**
- requires geometric head yaw counter-rotation to preserve gaze;
- belongs to gaze;
- magnitude is determined by geometry.

**Base linear acceleration**
- may create expressive neck pitch;
- lean back on forward acceleration;
- pitch forward on braking;
- belongs to expressive coupling;
- magnitude is tunable.

**Why**
- Treating both as one generic “counter-move” risks breaking eye contact.

---

### MEM-20260813-05 — Planned motion can anticipate; external motion can only react
**Type:** DECISION  
**Status:** CURRENT

When SPEC-13 authors a base trajectory, it knows the motion before it starts.

Therefore expressive neck pitch can begin in anticipation.

For motion caused by:

- safety stop;
- obstacle recovery;
- external navigation command;

the neck only receives the signal reactively and may lag.

**Consequences**
- The two paths are allowed to look different.
- The system does not pretend reactive safety motion has cinematic anticipation.

---

### MEM-20260813-06 — Base veto degrades only the base track
**Type:** DECISION  
**Status:** CURRENT

When listening inhibit or safety prevents the base portion of a performance, the whole performance should not necessarily collapse.

**Consequences**
- Display, audio and neck can continue.
- Performance scheduling needs graceful partial-channel degradation.

---

### MEM-20260813-07 — Sustained sub-minimum-speed authored motion is non-conforming
**Type:** DECISION  
**Status:** CURRENT

Performance authors may not command sustained base velocity below the validated drivetrain minimum controllable speed.

Small expression must be encoded as discrete micro-moves separated by dwell.

**Consequences**
- The performance layer cannot wish away drivetrain physics.
- Hardware and authored motion are tested together.

---

### MEM-20260813-08 — Five base performances explicitly carried forward
**Type:** DECISION  
**Status:** CURRENT

The performance work currently contains/considers five key base behaviors:

1. curious approach;
2. dramatic turn-toward-caller;
3. excited spin;
4. small side-to-side;
5. startle.

The small side-to-side performance is considered highest-risk because it stresses reversal quality.

**Consequences**
- Shipping/acceptance of that performance is gated on real drivetrain testing.

---

### MEM-20260813-09 — Open mobile-base/performance follow-ups
**Type:** OPEN  
**Status:** CURRENT

The mutable follow-ups are owned by the README register. This entry records the open set by stable reference: **OQ-08, OQ-09, OQ-13, OQ-16, OQ-17 and OQ-18**.

---

### MEM-20260813-10 — README.md and MEMORY.md initialized
**Type:** DECISION  
**Status:** CURRENT

Two global project-context documents were introduced.

`README.md`
- current global project truth;
- project thesis;
- major frozen decisions;
- architecture;
- open work;
- document hierarchy.

`MEMORY.md`
- chronological append-only record;
- decisions and reversals remain visible;
- future changes are appended rather than rewriting history.

**Why**
- The project has accumulated enough interacting specifications that relying on conversation recall alone is unsafe.
- A clean global context and an immutable historical log serve different purposes.

**Consequences**
- Future subsystem work should consult the README for orientation and the canonical specs for exact requirements.
- New project-level decisions should append a MEMORY entry.

---

## 2026-08-13 — README reconciliation

### MEM-20260813-11 — Orientation and cross-spec gaps recorded
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Requirements:** C16-R74; C12-R18; C12-T11; remaining references `UNTRACED — OQ-21`

The README was reconciled against a detailed navigation and architecture review. The status map was moved beside the project definition, missing and retired spec numbers were recorded, pending amendment state was separated from project-level decisions, and derived constraints gained owner/validation fields.

The reconciliation also made explicit several previously scattered commitments:

- SPEC-03 is the body/base command surface while SPEC-16 owns drivetrain execution and safety;
- eyes, neck yaw and base yaw require one SPEC-13-owned gaze-distribution rule;
- procedural/performance/gaze contributions share one composition stage;
- planned acceleration-to-pitch coupling is commanded-trajectory feedforward, with inertial feedback necessarily reactive;
- the face uses continuous float-space geometry and per-cell coverage/brightness in a custom pupil-free renderer;
- procedural base aliveness is STRETCH and the display-only idle floor requires zero servo motion;
- acoustic prototype characterization gates CAD freeze, while a desktop simulator gates behaviour closure;
- retired SPEC-14/15/17/18/19 identifiers remain visible and SPEC-20 is not yet authored.

**Why**
- The former README described important architecture but did not reliably support navigation, status checking or amendment verification.
- Missing spec numbers and unlabeled provisional values could cause future work to route commands or treat requirements incorrectly.

**Consequences**
- `README.md` now separates established project truth, canonical-document verification, provisional values and open work.
- OQ-16 through OQ-21 track the newly surfaced decisions and restoration work.

**Follow-up**
- Restore the canonical spec documents and verify the pending-amendment column against their supersedes registers.

---

### MEM-20260813-12 — Decision-log governance corrected before further use
**Type:** CHANGE  
**Status:** CURRENT  
**Requirements:** Project-document governance

The initial reconstruction mixed immutable history with mutable registers and used metadata values outside its own declared schema. This bootstrap migration corrected the reconstructed metadata, marked all pre-2026-08-13 entries `RECONSTRUCTED`, moved the regress and OQ registers to README, and made supersession append-only.

From this entry onward, a superseding entry names the prior ID in `Supersedes:`; the prior entry never changes. Current-state and open-item lists are mutable only in README. MEMORY contains dated entries only.

**Consequences**
- MEM-20260803-01 carries its original `CURRENT` status; MEM-20260807-01 names it in `Supersedes:`.
- Future exact spec claims require requirement/test IDs or an explicit `UNTRACED — OQ-21` marker.
- Legacy type/status values were normalized once as part of the bootstrap migration; later corrections must be appended.

---

### MEM-20260813-13 — Schedule and “hardware first” are clarified
**Type:** CORRECTION  
**Status:** CURRENT  
**Supersedes:** MEM-20260807-03  
**Requirements:** Project scope/process

The 4–5 month figure belongs to the earlier AURA exploration; Makad’s current cut line is 3–4 months. “Hardware first” means the project spends its learning and difficulty budget on mechanics, electronics and integration. It does not mean parts selection precedes requirements.

MEM-20260809-05 governs sequencing: functionality → requirements → specs → architecture/budgets → parts → BOM → CAD/build.

---

### MEM-20260813-14 — SPEC-13 and SPEC-16 amendment application is unverified
**Type:** CORRECTION  
**Status:** PROVISIONAL  
**Supersedes:** MEM-20260813-01  
**Requirements:** UNTRACED — OQ-21

MEM-20260813-01 said the SPEC-13 base amendment was applied. The canonical specs are absent from this workspace, and the last available project state reports both the SPEC-13 work and the load-bearing SPEC-16 delta as drafted or pending verification. They must not be treated as landed merely because README/MEMORY describes their intended architecture.

**Follow-up**
- Restore the source specs, verify the deltas, then append either an application record with exact IDs or a rejection/replacement entry.

---

### MEM-20260813-15 — Affect state and authored performances remain distinct
**Type:** DECISION  
**Status:** CURRENT  
**Requirements:** UNTRACED — OQ-21

Affect state modulates generation and selection. An authored performance is a recognizable, time-bounded multi-channel act. The runtime architecture must not collapse them into a central `current_emotion` enum.

This is independent of the procedural-versus-authored ownership boundary in MEM-20260811-05.

---

### MEM-20260813-16 — SPEC-10 is protocol plus caller-driven registry
**Type:** DECISION  
**Status:** CURRENT  
**Requirements:** UNTRACED — OQ-19, OQ-21

SPEC-10 is not a frozen capability catalogue. It defines the VLM interaction protocol and a registry that begins empty, then grows only as concrete callers and contracts are authored. Whether a VLM belongs in V1 remains open.

---

### MEM-20260813-17 — Procedural math and stimulus stability corrections are carried forward
**Type:** REVIEW FINDING  
**Status:** CURRENT  
**Requirements:** C12-R18; C12-T11; remaining references `UNTRACED — OQ-21`

The SPEC-12 revision findings are:

- saturation awareness is evaluated in summed coordinates;
- gaze step amplitude is separate from maximum idle offset;
- `u = clamp(Σ w_c · h_c)`, with habituation gating the stimulus input;
- C12-R18 is scoped to the procedural layer;
- C12-T11 carries the baseline correction;
- stimulus classes are stable: absolute weights are never renormalized by class count, and new classes default to zero.

---

### MEM-20260813-18 — Perceived-time authoring separates compensation from intentional lag
**Type:** DECISION  
**Status:** PROVISIONAL  
**Requirements:** UNTRACED — OQ-13, OQ-21

Animation-derived onset offsets of 80–170 ms per faster expressive link unblock early authoring; geared-base visible onset remains provisionally 150–400 ms. Compensation removes variable system/mechanical lag so authors can still specify deliberate lag. Intentional lag is authored character timing; unintended lag is a defect.

---

### MEM-20260813-19 — Microphone-count derivation and clock requirement are sharpened
**Type:** CORRECTION  
**Status:** CURRENT  
**Supersedes:** MEM-20260811-01, MEM-20260811-03  
**Requirements:** UNTRACED — OQ-06, OQ-21

The complete microphone chain is: at least 90% audio/visual association at at least 40° source separation → acoustic uncertainty approximately σₐ ≤13–15° → at least four non-collinear microphones. Front/back ambiguity independently rules out one two-microphone baseline.

Capture and playback require a shared **word clock** or a demonstrably equivalent sample-synchronous clock domain, not merely “shared timing.”

---

### MEM-20260813-20 — Passive support is elevated and holonomic drive is rejected for V1
**Type:** DECISION  
**Status:** PROVISIONAL  
**Requirements:** UNTRACED — OQ-18, OQ-21

Caster/support type and placement are first-order expressive, acoustic and stability choices. A ball or dual support is preferred for frequent reversals, subject to testing. Holonomic drive is ruled out for V1 because its added rollers/contact events work against the fixed body microphone array and add complexity without enough expressive benefit.

---

### MEM-20260813-21 — Mutable registers move to README
**Type:** CHANGE  
**Status:** CURRENT  
**Requirements:** Project-document governance

The “do not accidentally regress” register and the OQ register now live only in README. MEMORY entries cite stable OQ IDs rather than restating mutable item text. The register set includes the no-`current_emotion` rule, perceived-time onset policy, SPEC-13 channel ownership, SPEC-13 supersedes ownership, the display-only V1 idle floor, SPEC-20 authorship, SPEC-07 audio representation, caster configuration, VLM scope, head-height sweep and canonical-spec restoration.

---

### MEM-20260813-22 — Reconciliation traceability and OQ mapping
**Type:** CORRECTION  
**Status:** CURRENT  
**Clarifies:** MEM-20260813-11  
**Requirements:** `UNTRACED — OQ-21`

MEM-20260813-11 is a project-level reconciliation record whose remaining `UNTRACED` requirement/test IDs cannot be verified while the canonical specs are unavailable; its cited IDs remain provisional until OQ-21 closes.

For current follow-up routing:

- **OQ-20** owns the unprotected head-height sweep limit;
- SPEC-13/SPEC-16 amendment application is included in **OQ-21**, alongside canonical-source restoration and traceability.

**Why**
- The canonical README register must remain the only mutable OQ map.
- Reusing OQ-20 for amendment verification would make historical references ambiguous.

**Consequences**
- Future MEMORY entries reference the OQ IDs in README §19.
- Amendment verification remains blocked on OQ-21.

**Follow-up**
- Close OQ-20 through head-sweep geometry/sensing work and OQ-21 by restoring and auditing the canonical specs.

---

### MEM-20260813-23 — Existing specsheets and visuals are exploratory starting material
**Type:** CORRECTION  
**Status:** CURRENT  
**Clarifies:** All reconstructed entries that describe specsheets or visual concepts as established project truth  
**Requirements:** Project-document governance

The current `specsheets/` documents were created to get the Makad project started. Much of their content is exploratory, over-specified or low-confidence material and **is not binding**. Their proposed architectures, requirements, numeric targets, priorities, interfaces and acceptance tests must not be treated as approved merely because they are written in specification form.

The existing visual renders are the closest thing to a starting anchor, but they are also **not a frozen design**. They capture a useful initial character and product direction; the visual design, proportions, mechanical form, component placement and details are expected to change substantially.

At this point, the genuinely established foundation is limited to the Makad concept, name, broad companion-robot intent and a provisional visual starting point. Future engineering and design decisions must be reconsidered deliberately rather than inherited automatically from the current specsheets or renders.

**Why**
- The documents were intended to begin exploration, not prematurely freeze the project.
- Specification-style wording creates a false impression of maturity and approval.
- The design and architecture should remain free to change as the actual V1 is defined.

**Consequences**
- Treat `specsheets/` as reference/archive material unless an item is explicitly reviewed and adopted later.
- Treat `visuals/` as inspiration and historical starting material, not engineering truth.
- The project should be described as early concept/exploration work rather than a completed requirements phase.
- New binding decisions must be recorded explicitly in later MEMORY entries.

**Follow-up**
- Establish a short, human-reviewed V1 foundation covering intended character, capabilities, learning goals, constraints and revised visual direction before freezing architecture or parts.

---

## 2026-08-14 — V1 foundation approval

### MEM-20260814-01 — Human-reviewed V1 foundation is approved
**Type:** DECISION
**Status:** CURRENT
**Clarifies:** MEM-20260813-23
**Requirements:** `docs/00-foundation/vision.md` v1.0; `v1-scope.md` v1.0; `constraints.md` v1.0; `success-criteria.md` v1.0; `core-interaction-scenarios.md` v1.0

The project builder approved the human-reviewed V1 foundation. Makad, technically M4K4-D and commonly M4, is a personal droid whose primary V1 objective is to feel alive. Its differentiator is coordinated expressiveness arising from understanding, visual/audio perception, display animation, astromech sound, status light, physical motion and timing.

The approved Core includes:

- yaw-and-pitch expressive head motion;
- an animated face and at least one controllable LED beside the head camera;
- natural-language understanding with authored non-English astromech output;
- person/face acquisition and sustained tracking;
- battery-powered wheeled floor locomotion;
- “come here” and pet-like “follow me” behaviour;
- collision/obstacle handling and tabletop edge/fall protection;
- time display, timers, alarms and Spotify playback with an expressive music state;
- modular, screw-together, rugged droid construction.

Powered neck roll remains a Target. Spatial/directional hearing remains a Candidate; Core come/follow may begin with wake detection followed by visual search. Detailed intent phrasing, astromech vocabulary, drive architecture, component selection and numeric validation thresholds remain later engineering decisions.

The V1 deadline is fixed at **5 December 2026**. The target budget is ₹40,000–₹50,000 with a stretch ceiling of ₹1,00,000. Final V1 must operate untethered from an onboard battery; cloud services are allowed.

**Why**
- The project now has a human-reviewed product identity, scope, constraints, success definition and two Core interaction scenarios.
- The approved scenarios translate “feel alive” into observable wake/social, utility, approach and following behaviour.
- This closes the foundation follow-up in MEM-20260813-23 and provides an authority above the exploratory specsheets.

**Consequences**
- The approved foundation documents govern V1 scope; existing `specsheets/` remain non-binding reference material unless later adopted explicitly.
- Architecture, prototypes, components, BOM and CAD must trace back to the approved Core or an explicit Target/Candidate.
- Following and sustained face tracking are Core completion requirements, not optional Targets.
- Detailed language design is deferred without weakening the approved interaction semantics.

**Follow-up**
- Reconcile `README.md` with the approved foundation.
- Define system architecture, engineering budgets and risk prototypes around the two Core scenarios.

---

### MEM-20260814-02 — README is reconciled with the approved foundation
**Type:** CHANGE
**Status:** CURRENT
**Supersedes:** The 2026-08-13 README status snapshot
**Requirements:** Approved `docs/00-foundation/` v1.0 documents

`README.md` was rewritten as a current orientation document derived from the approved foundation.

The former README treated exploratory specsheet architectures, numerical targets, interfaces and open-question registers as established project truth. It also described Makad as a desktop/nearby-floor platform, fixed differential drive and four-microphone spatial audio as V1 architecture, and left the newly approved status light, utilities, Spotify interaction and Core come/follow scenario absent or optional.

The reconciled README now records:

- M4K4-D's approved personal-droid identity and “feel alive” priority;
- the complete approved Core, powered-roll Target and spatial-hearing Candidate;
- floor-first and tabletop-stationary operating modes;
- the wake/social and come/follow scenarios;
- the 5 December 2026 deadline, budget, tool and environment constraints;
- current project maturity, risk-prototype work and open engineering decisions;
- foundation-first document authority, with `specsheets/` explicitly non-binding.

**Why**
- README is the project entry point and must not contradict the approved human-reviewed foundation.
- Removing false architectural certainty allows the next phase to select mechanisms and components from scenario-driven requirements.

**Consequences**
- README is again a trustworthy current overview.
- The old spec map, speculative numerical constraints and obsolete OQ register no longer appear as current authority.
- Historical decisions remain in `MEMORY.md`, and exploratory technical material remains available under `specsheets/`.

**Follow-up**
- Define the system architecture, engineering budgets and risk-prototype plan.

---

### MEM-20260814-03 — Powered roll, pitch and yaw are all Core
**Type:** CHANGE
**Status:** CURRENT
**Supersedes:** The powered-roll classification in MEM-20260814-01 and earlier provisional/Target records
**Requirements:** `docs/00-foundation/vision.md` v1.1; `v1-scope.md` v1.1; `success-criteria.md` v1.1; `core-interaction-scenarios.md` v1.1

The project builder promoted powered neck roll from Target to Core. Makad V1 now requires a powered three-axis head supporting roll, pitch and yaw. A two-axis yaw/pitch head is not a V1-complete fallback.

The exact joint order, actuator class, transmission, structural support, sensing, wiring, range and control implementation remain open engineering decisions. Representative prototyping must solve these decisions while preserving natural movement, camera stability, safe limits, serviceability and coordination with the body and wheels.

**Why**
- Three-axis physical expression is central to the intended character rather than optional polish.
- Natural head movement and head–body–wheel coordination are primary mechanical, firmware and robotics learning objectives.
- Treating roll as removable would direct early architecture and packaging toward the wrong mechanism.

**Consequences**
- Foundation documents, README, the system-design brief and the exploratory neck spec now classify powered roll/pitch/yaw consistently as Core.
- The three-axis head mechanism and motion firmware become the first risk prototype.
- Spatial hearing remains a Candidate; it is not coupled to roll's Core status.

**Follow-up**
- Define the three-axis prototype load, range hypotheses, mechanical concepts, measurement plan and safe bench fixture in `risk-prototype-plan.md`.

---

### MEM-20260814-04 — Mechanical/firmware priority and planning constraints are reset
**Type:** CHANGE
**Status:** CURRENT
**Supersedes:** The budget, runtime, prototype-order and project-framing parts of MEM-20260814-01 and MEM-20260814-02
**Requirements:** `docs/00-foundation/constraints.md` v1.1; `docs/01-system/system-design-brief.md` v0.2

No external rubric is part of the current Makad scope. Rubric-specific wording has been removed from the project corpus and does not define project purpose, constraints or success.

No fixed spend ceiling is currently approved. The project will first estimate the full sourced cost of candidate parts, prototype quantities, tools, fabrication, shipping, replacements and contingency. Architecture/component substitutions or scope cuts will then be considered from the complete cost picture rather than an invented ceiling.

The initial untethered mixed-duty runtime requirement is at least 20 minutes. The approved initial movement/interaction envelope is a short single-room household case: ordinary interaction at approximately 0.3–2.0 m, “come here” from approximately 1–2 m with a stop approximately 0.6–0.9 m from the person, and following for up to approximately 3 m at no more than approximately 0.5 m/s on a level floor with one gentle turn and representative obstacles.

Tabletop operation is stationary by default. Only explicitly enabled low-speed test/calibration movement is permitted inside a marked, validated circular footprint; come/follow and excited spin remain floor-only.

Reliable network/cloud access may be assumed for connected Core features. No duplicate offline language, time or Spotify implementation is required. Network loss still requires bounded visible failure/recovery, and physical stop, motion inhibition, obstacle/edge protection and controller failure handling remain locally effective.

Engineering work is reprioritized toward component sourcing, three-axis head mechanics and firmware, electrical/control infrastructure, locomotion, and natural head–body–wheel coordination before the lower-risk CV, audio-processing, interaction-latency and display work.

**Why**
- Mechanical motion quality, control firmware, coordinated movement and sourcing are the builder's highest-risk and highest-learning areas.
- The builder expects CV, audio software, interaction processing and display UI to be comparatively familiar work.
- Cost decisions are more useful after real candidate availability and full landed costs are visible.

**Consequences**
- Internal communication and external network are separate engineering budgets: the former covers onboard controller links/timebase/watchdogs; the latter covers Wi-Fi/internet/cloud dependency, latency, authentication and failure behaviour.
- Sourcing/availability is a first-class architecture budget and runs before and during every physical prototype.
- The system-design brief now orders prototypes: three-axis head; electrical/control and peak power; locomotion/safety; coordinated motion; wake/interaction; sourced layout; short household tracking/following.
- Physical size and mass remain open for a dedicated architecture/layout discussion.

**Follow-up**
- Establish access to the required electrical tools.
- Discuss preliminary physical size, mass and transport assumptions.
- Produce the risk-prototype plan using the revised order.

---

### MEM-20260814-05 — V1 system design brief is approved
**Type:** DECISION
**Status:** CURRENT
**Requirements:** `docs/01-system/system-design-brief.md` v1.0

The project builder approved the V1 system design brief. The approved baseline fixes the system boundary, whole-system responsibility model, architecture drivers, information classes, operating/failure dimensions, engineering-budget categories, thirteen-decision ADR register, seven-prototype portfolio and mechanical/firmware-first decision order.

Approval does not select processors, controllers, mechanisms, actuators, drive geometry, sensors, batteries, frameworks, protocols, dimensions, component suppliers or final numeric thresholds. Those choices remain evidence-dependent.

**Why**
- The brief accurately translates the approved product foundation into the engineering problem the system architecture must solve.
- It separates semantic behaviour, perception evidence, physical control and independent safety authority without prematurely fixing deployment technology.
- It makes three-axis head motion, natural head–body–wheel coordination, sourcing and bounded failure first-class architecture concerns.

**Consequences**
- `docs/01-system/system-design-brief.md` v1.0 is the authority for system-architecture work below the approved foundation.
- Architecture and final component decisions require the named budget, sourcing and prototype evidence.
- The seven risk prototypes may now be planned and executed in the approved order, with sourcing/layout work beginning alongside the first prototype.

**Follow-up**
- Review and approve `docs/01-system/risk-prototype-plan.md` before committing prototype hardware.
- Establish the electrical-tool access plan and preregister the first head-prototype thresholds.
- Begin provisional engineering budgets and candidate trade studies from measured prototype inputs.

---

## 2026-08-17 — Risk-prototype-plan approval

### MEM-20260817-01 — V1 risk-prototype plan is approved
**Type:** DECISION
**Status:** CURRENT
**Requirements:** `docs/01-system/risk-prototype-plan.md` v1.0

The project builder approved the V1 risk-prototype plan. The approved plan converts the seven-prototype portfolio into an evidence program with an explicit roadmap, dependency order, continuous sourcing/mass/data work, preregistered thresholds, minimum evidence packets, time boxes, pass/iterate/reject/defer outcomes, Core-failure handling, stop/escalation rules and decision closeout.

The approved order remains mechanical/firmware-first. Sourced component envelopes begin alongside RP-01 rather than waiting for RP-06's final closure. Evidence from RP-01 through RP-07 closes the architecture decisions and engineering budgets before final component selection, BOM commitment and integrated CAD freeze.

Approval does not adopt a component, supplier, mechanism, architecture option or final numeric threshold. It also does not approve the new `docs/01-system/workbench.md`, which remains a proposed downstream document. Powered scored tests remain blocked until an independently reviewed workbench/test-readiness setup satisfies the RP plan's safety, instrumentation, configuration and logging requirements.

**Why**
- The plan makes each risk prototype answer named ADR, success-criteria and budget questions.
- Preregistered gates and retained failed evidence prevent thresholds or conclusions from being rewritten after results are known.
- The roadmap preserves time for evidence-backed architecture, integration and validation before 5 December 2026.

**Consequences**
- `docs/01-system/risk-prototype-plan.md` v1.0 is now the authority for V1 risk-prototype sequencing and evidence governance.
- Core prototype failures require iteration, an alternative architecture or explicit scope review; they cannot be silently deferred.
- The workbench draft must be reviewed independently before it can unblock powered scored testing.

**Follow-up**
- Review and correct `docs/01-system/workbench.md`, then approve or replace its test-readiness gate.
- Establish the candidate sourcing matrix, mass/envelope ledger, monotonic-time strategy and run-ID convention.
- Register RP-01 numeric thresholds and select the first head-mechanism candidates.

---

### MEM-20260817-02 — Workbench sourcing and readiness baseline is approved
**Type:** DECISION
**Status:** CURRENT
**Supersedes:** The proposed/non-canonical workbench status recorded in MEM-20260817-01
**Requirements:** `docs/01-system/workbench.md` v1.0; `docs/01-system/risk-prototype-plan.md` v1.1

The project builder approved `docs/01-system/workbench.md` as Makad's initial Stage 0 workbench sourcing and powered-test-readiness baseline. The approved document identifies the initial tool classes and buy/defer order, current planning-price ranges, motion-rig stop approach, scored-test readiness checklist and deferred battery-work gate.

Approval makes the document canonical for Stage 0 planning. It does not mean that the tools have been purchased, that listed prices or stock are guaranteed, or that any workbench item is a final Makad component. Prices, availability and landed cost are checked again before purchase; final battery and system architecture decisions remain governed by their ADRs and prototype evidence.

**Why**
- The builder reviewed the workbench as a practical sourcing list and judged it sufficient to start Stage 0.
- The list converts the approved electrical-tool constraint into an actionable acquisition sequence.
- The readiness checklist gives RP-01 and later powered rigs a common start gate.

**Consequences**
- `docs/01-system/workbench.md` v1.0 is approved.
- `docs/01-system/risk-prototype-plan.md` v1.1 now treats the workbench gate as an approved dependency.
- Powered scored testing remains blocked until the listed readiness conditions are satisfied for the active rig; document approval alone does not satisfy them.

**Follow-up**
- Purchase or establish access to the buy-now tool set and record actual landed costs.
- Fit and verify the stop/isolation method on the first RP-01 motion rig.
- Continue the component sourcing matrix and mass/envelope ledger needed by RP-01 and RP-06.

---

## 2026-08-22 — Physical run identity and evidence storage

### MEM-20260822-01 — Every physical prototype execution receives an immutable run identity
**Type:** DECISION
**Status:** CURRENT
**Requirements:** `docs/01-system/run-record-convention.md` v1.0; `docs/02-prototypes/_templates/run-record.md`; `docs/01-system/risk-prototype-plan.md` v1.1; `docs/01-system/workbench.md` v1.0

The project builder adopted a common run-identity, configuration-identity, and evidence-storage convention for Makad's physical prototypes. Every bounded execution that energizes an actuator, applies representative electrical/mechanical load, or produces evidence used for an engineering decision receives one permanent run ID. Routine assembly, soldering, passive inspection, and unpowered fit checks do not require an ID unless their result will be cited.

The canonical format is:

```text
RP<prototype>-<gate-and-version-or-EXP>-<exploratory|pilot|scored>-<UTC allocation>-<sequence>
```

For example, `RP01-G03V1-scored-20260822T091530Z-01` identifies one scored execution of RP-01 against gate G03 version 1. Exploratory work uses `EXP-exploratory`; it does not bypass identity. One bounded arm/start-to-disarm/stop execution receives one ID. A retry, power cycle, changed controlled configuration, or repeated trial block receives a new ID. Preregistered repetitions or input sweeps may share one ID only when each trial and input value is recorded.

Run IDs are allocated before execution and are never renamed, reused, or deleted. Failed, invalid, unsafe, and aborted runs remain in the evidence history. The ID does not encode a result. Run validity and threshold result live in the run record; gate/prototype pass, iterate, reject, or defer decisions remain in the summary because several runs may contribute.

Each scored run records the repository and worktree state; firmware and software revisions; applied configuration and overrides; rig, ballast, geometry and sourced-part revisions; instruments; active safety/test limits; readiness checks; artifacts; and results. Large evidence stored outside Git is represented by a stable path or asset identifier, byte size, and SHA-256 hash.

The operational rule is: **no valid run ID plus no confirmed logger means no actuator enable.** Until a guarded launcher implements that interlock, the builder enforces it in the pre-arm bench workflow: create the run record, complete its pre-run fields, start logging, confirm a sample containing the ID, and show or announce the ID at the start of external video.

**Why**
- Physical iterations can otherwise mix data, video, firmware, settings, fixtures, or component substitutions and produce an apparently precise result that cannot be trusted or reproduced.
- Retaining unsuccessful executions prevents accidental cherry-picking and preserves the evidence behind later engineering decisions.
- A generated exploratory ID keeps the process lightweight enough to use during real bench work instead of restricting traceability to formal scored tests.

**Consequences**
- `docs/01-system/run-record-convention.md` v1.0 and its reusable template are the current authority for run identity, configuration identity, and evidence layout.
- The combined RP-01 readiness item is split truthfully: run identity/configuration/evidence storage are defined; the machine-readable log schema and monotonic time/video-synchronization methods remain open.
- Physical prototype evidence without a conforming run identity and record cannot support a scored gate, ADR, engineering-budget update, component selection, or CAD freeze.

**Follow-up**
- Implement a run generator that creates the ID, evidence directory, and prefilled run record.
- Implement a guarded launcher that validates the run record, proves logging is writing, propagates the ID into all logs, and only then permits actuator enable.
- Define and validate the machine-readable logging schema, monotonic timebase, and external-video synchronization method before the first powered scored run.

---

### MEM-20260822-02 — Canonical engineering intuition guide adopted for all phases
**Type:** DECISION
**Status:** CURRENT
**Requirements:** `docs/intuition.md` v1.0

The project builder adopted `docs/intuition.md` v1.0 as the canonical methodological guide spanning every phase: foundation (00), system (01), prototypes (02), architecture (03), BOM (04), and CAD/build. The guide generalizes one working model — retire uncertainty in order; never let a downstream artifact harden around an upstream guess — into per-phase reasoning, a six-step prototype loop (intent → quantification → paper physics → competing concepts → instrumented rig → closed decision), cross-phase invariants, and a catalogue of anti-patterns previously caught in this project's history.

The same decision fixes the prototype evidence layout as `docs/02-prototypes/RP-XX-<name>/` (number for run-ID traceability, name for readability) with a standard internal skeleton (intent, physics, concepts, rig, gates, runs, decision), and records the downstream layering: ADRs and budgets in a future `docs/03-architecture/`, final component selection in `docs/04-bom/`, and integrated CAD in `cad/` — none of which may contain committed content before their roadmap stage.

The guide's authority is methodological only. It cannot override the approved foundation documents, system design brief, risk-prototype plan, workbench baseline, or run-record convention; on any conflict, the phase document wins and the guide must be corrected.

**Why**
- The builder is learning mechatronics while executing an evidence-gated plan; a single document capturing *how to think* at each phase prevents re-deriving the method per prototype.
- Making the folder convention and layering explicit prevents part-shaped organization (head/body/wheels with per-part "final" CAD/BOM) from silently contradicting the approved single-freeze sequencing.

**Consequences**
- `docs/intuition.md` v1.0 is canonical for method; README links it under System engineering.
- Prototype evidence folders follow the RP-XX-name convention; "final" BOM/CAD artifacts are prohibited inside `docs/02-prototypes/`.

**Follow-up**
- Scaffold `docs/02-prototypes/RP-01-head/` and begin the motion storyboard.
- Correct the guide if any statement is found to conflict with an approved phase document.

---

### MEM-20260822-02 — Planning time boxes removed from the risk-prototype plan
**Type:** CHANGE
**Status:** CURRENT
**Supersedes:** The per-prototype time-box provisions recorded in MEM-20260817-01
**Requirements:** `docs/01-system/risk-prototype-plan.md` v1.2

The project builder removed the per-prototype "Planning time box" sections (the estimated focused-working-day counts for RP-01 through RP-07) from the risk-prototype plan. The plan is now v1.2.

The substantive non-calendar content formerly embedded in those sections is preserved as scope notes: RP-02's staged battery validation with the runtime gate remaining open, RP-05's deferral of detailed vocabulary and face/audio polish, and RP-06's continuous sourcing/envelope updates with evidence-dependent final closure.

The escalation function of time boxes is retained in calendar-free form: repeated iteration on the same gate requires a review of schedule effect and evidence that the remaining problem is localized. The Iterate gate outcome no longer references a time box.

**Why**
- The day-count estimates were invented precision from a builder with no prior mechatronics bench experience; they carried no evidence and conflicted with the plan's own "measure physics" principle.
- Unrealistic estimates create either false schedule confidence or pressure to rush gates.
- Iteration discipline is better enforced by the gate-review rule than by fictional calendars.

**Consequences**
- `risk-prototype-plan.md` v1.2 contains no calendar estimates; sequencing remains governed by the dependency/concurrency table.
- The 5 December 2026 deadline and all approved envelope/runtime limits are unchanged.
- Schedule risk is now managed by tracking actual prototype progress against the deadline rather than against per-prototype allocations.

**Follow-up**
- None beyond normal roadmap tracking.

---

## 2026-08-25 — Dimensional and packaging baseline

### MEM-20260825-01 — 300 mm Makad geometry and 250 g moving-head target adopted
**Type:** DECISION  
**Status:** PARTIALLY SUPERSEDED by MEM-20260830-01 for the head envelope; drive, mass and placement decisions remain current  
**Supersedes:** Earlier dimensional, head-ballast, microphone-placement, speaker-placement, and drive-geometry planning assumptions where they conflict  
**Requirements:** `docs/01-system/dimensional-baseline.md` v1.0; `docs/00-foundation/constraints.md` v1.2

The project builder adopted a current physical target of **300 H × 205 W × 180 D mm overall**, with a **100 H × 180 W × 130 D mm complete head**, **Ø84 mm nominal drive wheels**, **170 mm drive-wheel track**, and **110 mm drive-axle-to-front-caster contact spacing**. The vertical stack uses a 140 mm ground-to-body-top/neck datum, a 60 mm three-axis neck allocation, and a 100 mm head; actuator intrusion leaves approximately 35–45 mm of externally visible neck.

The moving-head target is now approximately **250 g**, with preliminary inertia approximately **0.001 kg·m²** and preliminary neck peak-torque estimate approximately **0.2 N·m**. These are starting inputs for RP-01, not substitutes for CAD-derived centre of mass/inertia, axis-specific torque calculations, or registered representative-load tests. The earlier 300–700 g RP-01 head-ballast range is superseded.

The drive baseline is two independently powered encoder-equipped wheels plus a front caster, with a mandatory rear anti-tip skid. Normal travel targets 0.15–0.40 m/s, fast expressive motion 0.40–0.60 m/s, and drivetrain capability up to approximately 0.65–0.70 m/s. The existing 0.5 m/s cap for person-following trials remains in force. The required wheel-speed point is approximately 160 RPM at 0.70 m/s, with 160–200 RPM unloaded used for drivetrain design.

Four PDM MEMS microphones, the speaker, battery, and primary electronics are body-mounted. Ear pods remain visual-only; the sole head sensor is the central camera alongside the display/status-light hardware.

**Why**
- The integrated proportions now have a coherent dimensional stack and stable differential-drive footprint.
- Moving audio/electronics mass out of the head protects the three-axis neck load and whole-robot centre of mass.
- A single authoritative baseline prevents RP-01, sourcing, RP-03, RP-06, and later CAD from hardening around incompatible assumptions.

**Consequences**
- `docs/01-system/dimensional-baseline.md` v1.0 is authoritative for dimensional, drive-geometry, moving-head-load, and component-placement targets.
- The mass/envelope ledger, candidate sourcing matrix, workbench framing, and RP-01 inputs now consume this baseline.
- Any packaging or prototype result that cannot meet it must request an explicit versioned baseline revision; it must not silently restore an older value.

**Follow-up**
- Produce the ~250 g head CAD mass blockout and replace preliminary CoM/inertia values before final RP-01 actuator selection.
- Validate drive stability, caster behaviour, braking, skid geometry, and speed control in RP-03.
- Validate the complete 300 × 205 × 180 mm sourced layout in RP-06 before integrated CAD freeze.

### MEM-20260825-02 — Battery sign, shell clearance, skid geometry, and acceleration stability corrected
**Type:** CORRECTION  
**Status:** CURRENT  
**Supersedes:** The battery-placement and unbounded skid/clearance implications in MEM-20260825-01  
**Requirements:** `docs/01-system/dimensional-baseline.md` v1.1; `docs/01-system/risk-prototype-plan.md` v1.3

The battery must be packaged **low and forward of the drive axle**, not near/behind it. Under forward acceleration, the inertial moment tends to rotate the body backward about the drive axle and lift the front caster. A forward longitudinal CoM supplies the opposing gravity moment; moving battery mass behind the axle would shrink that restoring arm.

The current whole-robot stability target is `x_CoM=+25 mm` forward of the drive axle and `h_CoM=124 mm` above the floor. The corresponding rigid-body front-caster lift threshold is:

`a_tip = g·x_CoM/h_CoM ≈ 9.81·25/124 = 1.98 m/s² ≈ 2.0 m/s²`.

This lies below the approximate 6 m/s² traction limit, so pitch stability—not available tire friction—governs forward expressive acceleration at the baseline CoM. At 124 mm CoM height, each additional 10 mm of forward CoM offset raises the theoretical threshold by approximately 0.79 m/s².

The 140 mm body-top datum and 105–115 mm visible body-shell height imply **25–35 mm main-shell ground clearance**. The previous 8–12 mm value was geometrically inconsistent and is superseded. The rear anti-tip skid is therefore a distinct lower protrusion. For skid height `h` above the floor and rearward reach `d`, contact must precede the CoM crossing the wheel support line: `h/d < x_CoM/h_CoM ≈ 0.20`. At the adopted `d≈70 mm`, the skid must be **no more than 14 mm above the floor**.

**Why**
- The previous battery sign reduced rather than improved forward-acceleration pitch stability.
- The previous clearance value did not close against the vertical datum and visible shell height.
- A mandatory skid without a height/reach relation could fail to contact before geometric tip-over.

**Consequences**
- `dimensional-baseline.md` v1.1 is the corrected authority.
- RP-03 must measure caster-lift onset and skid contact and register forward acceleration below the measured lift threshold with margin.
- The mass/envelope and sourcing ledgers now require a low, forward battery and the corrected skid envelope.

**Follow-up**
- Validate the integrated CoM from CAD and measured component masses.
- Recompute `a_tip` and `h/d` from the measured CoM before the first scored RP-03 acceleration run.

---

## 2026-08-30 — Display-derived head proportion revision

### MEM-20260830-01 — Head envelope rebuilt bottom-up from selected display and camera
**Type:** CORRECTION  
**Status:** CURRENT  
**Supersedes:** The 100 H × 180 W × 130 D mm complete-head and 140–145 mm core-width assumptions in MEM-20260825-01  
**Requirements:** `docs/01-system/dimensional-baseline.md` v1.7

The selected Waveshare ESP32-S3-LCD-4.3 no-touch module fixes a 106.1 W × 67.8 H mm hidden body around a 95.04 W × 53.86 H mm active image. Building outward from that real component produces an approximately **95 H × 125–130 W × 110–115 D mm core** and an approximately **95 H × 150 W × 115 D mm nominal complete head**, to be validated within **90–100 H × 145–155 W × 110–120 D mm**.

The optical aperture is now distinguished from its surround: approximately 94–95 W × 53–54 H mm clear aperture inside a roughly 110–115 W × 60–65 H mm bezel/window treatment. Compact 40–50 mm side pods may cover required pivots, but their width contribution is limited to approximately 8–12 mm per side and must remain inside the complete-head width band rather than being added afterward.

The approximately 95 mm head height plus the 140 mm body-top datum and 60 mm neck allocation gives a nominal 295 mm stack. The 300 mm overall height remains a rounded outer target and does not require inflating the head.

**Why**
- The earlier 180 mm width came from a top-down visual proportion and made the head, pods and yoke read too wide on a 300 mm robot.
- The selected display and camera now provide real package anchors for width and height.
- The previous 130 mm depth lacked a selected-component derivation; 110–120 mm is the active validation band until the roll support, connectors and cable service loops are blocked out.

**Consequences**
- RP-01 fixtures, ballast geometry, concept comparisons and swept-envelope work use the smaller v1.7 head envelope.
- Side pods integrate the mechanical pivots instead of becoming a second additive width allowance.
- RP-06 must validate the height/depth trade between the stacked camera, display PCB, rear connector clearance and roll support before CAD freeze.

---

## 2026-08-31 — RP-01 head material, finish and mass correction

### MEM-20260831-01 — RP-01 PLA/finish system locked and 250 g head target rejected
**Type:** DECISION + CORRECTION  
**Status:** CURRENT FOR RP-01; final Makad material and measured head mass remain open  
**Supersedes:** The approximately 250 g moving-head target, approximately 0.001 kg·m² preliminary inertia and approximately 0.2 N·m preliminary neck-torque sizing inputs in MEM-20260825-01 for RP-01 design and scored-load use  
**Requirements:** `docs/02-prototypes/RP-01-head/material-finish-mass-decision.md`; `docs/02-prototypes/RP-01-head/payload-mass-capture.md`

The project builder locked eight RP-01 build decisions: all printed structure and skin use PLA; PLA remains a prototype choice rather than the final Makad material; M010–M012 stay provisional until thermal/creep evidence closes; visible industrial-design fasteners are real M2 button-head screws; the full nine-step chipped-paint/weathering process is required; cosmetic seams are integral/faked except where service needs a real split; adjacent panel heights are modelled 0.3–0.5 mm apart; and the 250 g complete-head target is infeasible for this build.

The selected Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493 board fits the revised head envelope at 106.1 × 67.8 mm, but width is tight and the wider 110–115 mm window treatment requires a full-width opaque rear mask. The sealed head also requires a flashing/service path. A separable harness boundary at yaw is required so the moving harness and complete M900 head can be weighed without cutting conductors.

The current row-by-row planning model is approximately **490 g at 1.2 mm PLA walls** and approximately **472 g at 1.0 mm walls**. These are `D`/`E` planning values, not accepted measurements. `W` evidence remains the only source for the final mass roll-up. M019 is retired in favour of the irreversible M019a bare → M019b coated → M019c installed/finished sequence, and visible M2 hardware is separately owned by M021a.

**Why**
- Confirmed display geometry, printable shell area and the required finish/hardware stack independently make 250 g unattainable.
- PLA gives RP-01 the best stiffness/finish/iteration trade, while explicit provisional flags preserve an honest PETG/ASA fallback if sealed-head temperature or sustained-load creep fails.
- Integral cosmetic seams preserve monocoque stiffness and avoid approximately 28 g of unnecessary joint hardware.

**Consequences**
- RP-01 physics, rig ballast, concept comparison and gates use the approximately 490 g planning build-up until replaced by measured per-axis mass, CoM and inertia evidence.
- Any actuator conclusion based on the old mass, inertia or approximately 0.2 N·m estimate is reopened; the authored motion vocabulary remains intent, but torque-speed, current, thermal and settling feasibility must be recomputed.
- CAD must implement panel offsets, printable detail minima, full-width masking, display flashing access and the separable yaw-plane boundary.
- The system-level dimensional/mass baseline, neck torque model, actuator family screen and whole-robot CoM/tip model require controlled downstream revision.

---

## 2026-08-31 — RP-01 motion-controller and sensing boundary

### MEM-20260831-02 — ESP32-S3 motion firmware selected; Nano/IMU moved to bench work
**Type:** DECISION  
**Status:** CURRENT FOR RP-01  
**Supersedes:** The Nano 33 BLE Sense C1 installed-controller path and the runtime head-IMU assumptions in the prior control-topology study  
**Requirements:** `docs/01-system/control-topology-options.md` v0.7; `docs/02-prototypes/RP-01-head/payload-mass-capture.md`

RP-01 motion firmware is an **ESP32-S3** implementation from the start. The on-hand Arduino Nano 33 BLE Sense is now a bench instrument only: it is not installed in the head, does not enter the mass ledger, and does not create a second motion-firmware target. Its nRF52840 is BLE-only, not Wi-Fi.

The preferred C1 arrangement would have shared the selected display board's ESP32-S3 between rendering and local motion. Its mitigation is explicit: renderer/communications on Core 0, a high-priority motion task on Core 1, and IRAM-safe servo ISR work. Any future C1 consideration requires a same-chip timing comparison with rendering off and on.

The official Waveshare SKU 30493 carrier schematic closes the electrical gate first. The RGB565 panel and timing consume 20 GPIO; the remaining nets are assigned to SD, I²C/CH422G, RS-485, USB/CAN or USB-UART. The original future-ready screen needs ten clean native GPIO for SPI, half-duplex servo bus/direction, E-stop, fault and interrupt. Stationary RP-01 removes the runtime-IMU portion but still needs five clean motion/safety signals; the carrier plainly exposes only GPIO6. The CH422G expander is not an acceptable deterministic motion/safety substitute. **C1 is therefore unavailable on the selected carrier.** C2—a dedicated ESP32-S3 motion-controller module—becomes the active RP-01 implementation path, but its exact module remains unselected and no purchase is authorized.

Because the previous 490 g build-up carried M008 as zero while C1/C2 was unresolved, it is now a **pre-M008 lower bound**, not a complete C2-head prediction. Do not invent that module's mass: add it only after selecting and weighing the installed C2 module, mount, connectors and harness.

Stationary RP-01 uses servo encoders for runtime joint angle and has no installed IMU. A bench IMU may be used for backlash and resonance measurements. APDS-9960 auto-brightness/proximity-startle and PDM-mic early DOA work toward the 13° target are candidate bench experiments only. When locomotion arrives, the runtime IMU belongs on the base; a head-mounted IMU would require subtracting neck motion from commanded angles and reintroduce the SPEC-09 timing-skew problem.
