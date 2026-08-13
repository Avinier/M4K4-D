# Makad

> **Current project context for the Makad desktop companion robot**  
> Status snapshot: **2026-08-13**

Makad is a small, expressive, wheeled desktop/social companion robot being designed as a serious 3–4 month robotics build rather than a polished consumer product. The earlier AURA exploration used a 4–5 month estimate; 3–4 months is the current Makad scope, not a rewrite of that historical estimate.

The central idea is simple:

**Makad should feel alive before it feels useful.**

Its personality is carried through animated eyes, measured head motion, sound, attention, timing, procedural idle behaviour, authored performances, and a small differential-drive base. The project is deliberately using that expressive goal to force real engineering work across mechatronics, control, perception, audio, embedded systems, software architecture, integration, validation, and CAD.

Makad means **“monkey”**, and the visual language keeps a subtle monkey-like identity through the side-ear forms while otherwise leaning toward a compact Star Wars-style scout droid rather than a literal animal robot.

---

## 1. What Makad is

Makad V1 is intended to be a:

- small expressive companion robot;
- desktop / nearby-floor mobile platform rather than a humanoid;
- camera-equipped perceptual robot that can notice and track people;
- hearing-capable robot with spatial audio awareness;
- low-latency speech-aware system;
- droid-like vocal character whose primary expressive voice does **not** need to be ordinary English;
- physically expressive character using eyes, head/neck, audio, and wheels;
- procedural “alive while idle” system;
- authored performance system for deliberate reactions and gestures;
- differential-drive robot that can orient, approach, retreat cautiously, make small expressive turns/spins, and perform basic obstacle-safe movement;
- modular, screw-together, 3D-printable learning platform whose internals can be inspected and changed.

The goal is **not** merely to assemble features. The important product/interaction thesis is that perception, motion and sound must be coordinated tightly enough that Makad appears to attend, react and move with intent.

---

## 2. Status and spec map

This snapshot distinguishes project decisions from canonical-document application. The canonical spec files are not currently present in this workspace, so “established” below means established in the project record; it does not prove that every tracked amendment has been applied to its source document.

The apparent SPEC-03/SPEC-16 conflict is an ownership split: **SPEC-03 remains the body/base command surface referenced by callers; SPEC-16 owns differential-drive execution, low-level control, safety and the current implementation contract.** SPEC-13 routes expressive intent through the former and cannot bypass the latter.

| Spec | Current ownership / disposition | Project status | Pending amendment or verification |
|---|---|---|---|
| SPEC-01 | Expressive face/display lineage | Established | Consolidate continuous-geometry renderer commitments |
| SPEC-02 | Neck mechanics, sensing, motion control and camera-bearing geometry | Established | Actuator, encoder and powered-roll choices remain open |
| SPEC-03 | Body/base command surface | Established interface; implementation partly superseded by SPEC-16 | Verify explicit supersedes note in both documents |
| SPEC-04 | Microphone array and audio-input architecture | Established | Validate array geometry, isolation and shared-clock implementation |
| SPEC-05 | Real-time speech-input pipeline | Established | Hardware timing and barge-in validation remain |
| SPEC-06 | Semantic response/action layer | Established | Physical-action confirmation/cancellation integration remains |
| SPEC-07 | Output, vocalization and droid-language engineering boundary | Established | Decide fixed clips versus parameterized synthesis/time-stretching |
| SPEC-08 | Calibrated visual observation and moving-camera foundation | Established lineage | Camera/optics and rolling-shutter measurements remain |
| SPEC-09 | Temporal person/face tracking and attention selection | Established | Hardware/replay validation remains |
| SPEC-10 | VLM protocol and caller registry | Established architecture; registry intentionally starts empty | Decide whether V1 includes a VLM and add callers deliberately |
| SPEC-11 | Fused social presence and audio-visual association | Established | Validate derived acoustic-association constraint |
| SPEC-12 | Procedural idle/aliveness and shared motion-composition lineage | Established; base contribution is STRETCH | Extract shared composition stage instead of duplicating it |
| SPEC-13 | Authored performance scheduling and gaze/channel distribution | Established in project record | Verify canonical application of base participation, performance library, head counter-move and gaze-target distribution amendments |
| SPEC-14 | Retired: no-touchscreen constraint | Retired into constraint line | Keep this stub; no standalone spec |
| SPEC-15 | Retired: no-touchscreen constraint | Retired into constraint line | Keep this stub; no standalone spec |
| SPEC-16 | Differential-drive implementation, safety and locomotion interfaces | Established; amendment state not verifiable here | Canonical amendment was last reported drafted-not-applied; verify before treating it as landed |
| SPEC-17 | Retired: absorbed fully into SPEC-16 | Retired | Keep this stub; no separate ownership |
| SPEC-18 | Retired: interface moved to SPEC-16; motion-library lineage moved to SPEC-12 | Retired/split | Verify both supersedes references |
| SPEC-19 | Closed without a document | Closed | Keep this stub to prevent number reuse |
| SPEC-20 | High-level behaviour arbitration | Not yet authored | Assign authorship and define arbitration contract |

Exact requirement and test wording remains owned by the canonical specs and their supersedes registers.

---

## 3. Derived constraints and validation snapshot

| Constraint | Status | Owner | Validation state |
|---|---|---|---|
| Face animation at roughly **30–60 fps** | TARGET | SPEC-01 | Simulator/display validation pending |
| Neck reversal lost motion **≤1°**; **≤0.5°** stronger target | TARGET | SPEC-02 | Hardware fixture/video test pending |
| Neck physical repeatability about **±0.5°** | TARGET | SPEC-02 | Hardware validation pending |
| Microphone capture uses a **shared word clock / synchronized digital capture** | MUST | SPEC-04 | Committed architecture; implementation pending |
| At least **90%** audio/visual association at **≥40°** source separation implies roughly **σₐ ≤13–15°**, carried as **σₐ ≤13°**; this drives **≥4 non-collinear microphones** | Derived MUST | SPEC-04 + SPEC-11 | Array prototype characterization pending; front/back ambiguity is the secondary justification |
| Visual bearing error about **1.5° P95** | TARGET | SPEC-08/09 | Camera/optics validation pending |
| Obstacle/cliff detection to deceleration command **≤50 ms** | MUST | SPEC-16 | Low-level test pending |
| Animation-derived per-link onset offsets **80–170 ms** | PROVISIONAL authoring baseline | SPEC-13 | Makes onset measurement non-blocking; replace with measured distributions later |
| Geared-base perceptible onset roughly **150–400 ms** | PROVISIONAL | SPEC-13 + SPEC-16 | Drivetrain measurement pending |

Unmeasured values remain provisional. A number becomes “validated” only when its owner’s acceptance test passes on representative hardware.

---

## 4. V1 cut line, open decisions and ordering gates

The 3–4 month schedule is credible only with an explicit cut line.

### V1 cut line

- The minimum idle floor is **display-only blink + gaze drift, zero servo motion, and a physical power switch**.
- Yaw and pitch are MUST; powered roll remains TARGET.
- Procedural base aliveness is **STRETCH and marginal**: it ships only if safety, acoustics, low-speed quality and schedule all permit it.
- Authored base performances may ship selectively; hardware-sensitive side-to-side motion is gated on real reversal testing.
- VLM-backed behaviour, full-house navigation, manipulation, biometric identity and a touchscreen are outside the committed V1 floor.

### Decisions still open

The single canonical list is the **OQ register in §19**. The immediate blockers are OQ-17 (SPEC-07 audio representation), OQ-21 (restoring the canonical specs and traceability), and OQ-16 (SPEC-20 authorship).

### Ordering gates

1. Reconcile the supersedes map and close interface ownership.
2. Build the **desktop simulator** so SPEC-12/13 behaviour, composition and timing can close without hardware.
3. Freeze the system block architecture and high-/low-level compute split.
4. Establish preliminary body/head/base envelopes and microphone candidate geometries.
5. Perform **acoustic prototype characterization before CAD freeze**.
6. Close compute, power, peak-current, thermal and mechanical budgets.
7. Derive final component-selection criteria and BOM.
8. Freeze CAD only after the acoustic gate and placement constraints pass.
9. Prototype, measure onset/low-speed/reversal behaviour, and replace provisional timing values.
10. Integrate by subsystem and run the acceptance-test plan.

Animation-derived offsets of **80–170 ms per link** make physical onset measurement non-blocking for early performance authoring; measured channel distributions still replace them before final tuning.

---

## 5. What Makad is not

The current V1 scope explicitly does **not** require:

- arms or manipulation;
- walking legs;
- self-balancing;
- a BB-8 spherical drive mechanism;
- a holonomic/omnidirectional drive—the additional lateral and rotational motion modes create unnecessary command-allocation and ego-motion burden, and body rotation with the fixed microphone array directly degrades DOA evidence;
- full-house autonomous navigation;
- research-grade SLAM as a core deliverable;
- a traditional humanoid conversational assistant;
- a mouth on the face;
- biometric identity/re-identification as a core mechanism;
- a sealed appliance-like enclosure that prevents inspection;
- premature optimization around one exact SBC, motor, servo, microphone, display or battery before the system requirements are complete.

Utility-assistant features are intentionally secondary. They may be added where they strengthen the project, but they do not define Makad.

---

## 6. Project design philosophy

### 6.1 Expressiveness is a system property

Makad’s apparent aliveness should emerge from coordination across:

- **eyes/display** — fastest visible attention cue;
- **audio** — immediate reaction and character voice;
- **neck/head** — physical gaze, curiosity, recoil, nodding, tilting;
- **base** — body-scale orientation, approach, hesitation, spin and follow-through;
- **perception** — determines what Makad believes is happening;
- **behaviour** — decides which action/performance is appropriate;
- **procedural aliveness** — keeps the robot from feeling frozen between explicit events.

No single channel should try to carry all expression.

### 6.2 Requirements before parts

The agreed workflow is:

**desired functionality  
→ engineering requirements  
→ subsystem specifications  
→ cross-system architecture  
→ compute / power / mechanical budgets  
→ physical envelope  
→ exact component selection  
→ BOM  
→ CAD / prototype / integration**

The functional list is the source of truth. Exact parts are intentionally deferred until the coupled requirements are understood.

“Hardware first” describes where the project spends its difficulty and learning budget: unfamiliar mechanics, electronics and integration take priority over speculative AI features. It does **not** mean selecting parts before requirements. The ordering above governs sequencing.

### 6.3 Quantitative where physics matters

Requirements are expected to be measurable rather than aesthetic slogans.

Relevant specs should quantify or derive, where appropriate:

- torque;
- inertia;
- acceleration;
- backlash;
- repeatability;
- stiffness;
- sound level;
- microphone geometry;
- angular uncertainty;
- latency;
- frame rate;
- synchronization;
- wheel resolution;
- minimum controllable speed;
- braking distance;
- tip margin;
- power/current;
- thermal load;
- timing jitter;
- fault timeouts.

Unmeasured numbers must remain **PROVISIONAL / TARGET**, not become fake precision.

### 6.4 Every important MUST should be testable

Validation is expected to use realistic tools available during the build:

- controller logs;
- software replay;
- high-frame-rate phone video;
- rulers / fixtures;
- current and temperature telemetry;
- recorded audio;
- scripted motion sequences;
- endurance tests;
- naive-observer character tests;
- simple obstacle and edge test rigs.

---

## 7. Current visual and mechanical direction

Makad should look like a compact mechanical droid rather than a generic smooth consumer robot.

Current direction:

- angular / sharp-ish body language rather than fully rounded toy styling;
- metallic-sheet / bolted-panel feel, implemented realistically with 3D-printed parts;
- visible screws and serviceable panels;
- easy disassembly for electronics inspection;
- visible camera placement;
- integrated speaker area;
- `MAKAD` branding on the shell;
- side “ears” that provide the monkey-like silhouette;
- ears are **visual/mechanical forms**, not the microphone locations;
- body proportions must stay realistic for a beginner-friendly 3D-printed build;
- centre of mass and tip stability matter because the head is visually and mechanically top-heavy.

Older concept images are **reference art, not engineering truth**. Where concept art conflicts with a later subsystem decision, the subsystem specification wins.

---

## 8. Expressive face / display

The face is deliberately minimal.

### Frozen visual identity

- The face shows **eyes only**.
- Makad must **never display a mouth**.
- Each eye retains a simple circular identity.
- The rendering style should feel like a dot-matrix / phosphor / halftone / pixel-grid display rather than generic vector emoji art.
- The face should remain programmable and extensible.
- Roughly **30–60 fps** is acceptable for the animation layer.
- Expressions should be generated from parameters and layered animation rather than only one-off hard-coded frames.
- The current direction is a custom eye-rendering library, not a fixed clip library or generic UI animation package.
- Eye geometry is evaluated continuously in floating-point space and sampled into the dot grid; animation is not restricted to integer-cell jumps.

Eye geometry is evaluated continuously in float space. Each display cell receives brightness from geometric coverage rather than binary inside/outside occupancy; this prevents edge crawl and preserves smooth morphing at low resolution.

Makad will use a custom eye-rendering library rather than RoboEyes, Uncanny_Eyes or `esp32-eyes`. Those libraries are built around pupils, rounded rectangles or a different eye grammar; Makad needs solid, pupil-free glyphs whose boundaries, lids, scale and coverage can morph continuously while retaining the circular identity.

### Expressive vocabulary

The eye system must support enough control for states such as:

- blink;
- partial closure;
- squint;
- widening;
- look direction;
- sleep / wake;
- happiness;
- curiosity;
- confusion;
- annoyance;
- surprise;
- asymmetry where useful.

Additional parameters such as eyelid angles and nonuniform scaling are allowed as long as the basic circular-eye identity survives.

### Coordination principle

The eyes are not merely a decorative screen.

A key interaction model is:

**eyes signal attention first → head establishes physical gaze → base handles larger body orientation**

These are related channels, not interchangeable pointing mechanisms.

---

## 9. Neck / head motion

Head motion is one of Makad’s most important expressive mechanisms.

### Current architecture

- **Yaw and pitch are MUST-HAVE.**
- The mechanical architecture should be designed with roll in mind.
- **Powered roll is a TARGET**, not something that should endanger V1 completion.
- Kinematic intent is effectively **yaw → pitch → roll**, with roll closest to the head if implemented.
- Exact actuator and encoder architecture is not yet frozen.

### Mechanical/control principles

The neck must be treated as a measured camera-bearing mechanism, not “three hobby servos moving a cute head.”

Important carried-forward decisions include:

- head load must be carried structurally rather than hanging entirely from a servo horn;
- mass, centre of mass and moment of inertia must be modeled;
- actuator sizing must use the actual dynamic torque requirement;
- physical joint orientation must be available to control/perception;
- downstream transmission uncertainty may require joint-side sensing;
- closed-loop trajectory/velocity control is preferred over abrupt position jumps;
- small expressive motion makes backlash a character-quality problem, not merely a positioning problem;
- camera pose must be computed from calibrated geometry and measured joint state;
- perception must understand that the camera itself moves;
- the gaze controller is distinct from raw target tracking;
- degraded modes must exist for perception failure, sensor failure, actuator fault and communication loss.

### Important current validation targets

Examples already carried into the neck work include:

- about **≤1° reversal lost motion** at the current small-motion requirement;
- **≤0.5°** as a stronger target;
- about **±0.5° physical repeatability** as a target;
- quantitative tracking/jitter tests;
- high-rate logging around the 100 Hz class where hardware supports it;
- external high-speed video as an independent truth source;
- endurance and cable-cycle testing;
- normal-motion acoustic targets that remain provisional until actuator testing.

Exact final roll range, actuator family and encoder layout remain open pending mechanical work.

---

## 10. Audio input and spatial hearing

Makad V1 no longer uses the old “two microphones in the ears” concept.

### Frozen microphone direction

- **4 MEMS microphones**
- mounted in the **body**, not the moving head or ear pods;
- non-collinear, reasonably wide geometry;
- rigidly calibrated as one array/subframe;
- the array/subframe may be compliantly isolated as a whole from chassis vibration;
- synchronized digital capture on a **shared word clock is required**;
- ear pods remain visual-only.

This decision was driven partly by the audio-visual association requirements: a two-microphone single-baseline array has front/back ambiguity that can create confidently wrong speaker association.

### Spatial-audio requirements

The audio system must ultimately expose usable:

- direction-of-arrival estimates;
- uncertainty;
- capture timestamps;
- timing compatible with audio/visual association;
- shared capture/playback timing information where required.

The fusion requirement is at least **90% association at ≥40° source separation**. That derives an acoustic uncertainty bound of roughly **σₐ ≤13–15°**, carried conservatively as **σₐ ≤13°**, which in turn requires at least four non-collinear microphones. Front/back disambiguation is the second reason for the array, not the primary derivation.

### Mobile-base consequence

The body mic array is only stationary while the body is stationary.

Once Makad rotates:

- the acoustic frame rotates;
- persistent sound-source tracks require ego-motion compensation;
- the locomotion system must publish timestamped body yaw / yaw rate;
- motor/gearbox vibration becomes structure-borne array contamination.

This is a closed perception/action loop: the base channel’s own output degrades the acoustic evidence that may have commanded the rotation. Ego-motion compensation fixes frame rotation, but it does not remove structure-borne drive noise.

Structure-borne drive noise is not something a beamformer can simply “point away from.” Mitigation is primarily:

- mechanical isolation;
- motor/drivetrain quality;
- or temporarily inhibiting locomotion while listening.

Therefore the audio/behaviour system is allowed to request a **motion inhibit for active listening**, distinct from the locomotion safety inhibit.

---

## 11. Speech, conversation and Makad’s voice

The project changed direction away from requiring conventional English conversation as Makad’s defining interaction.

### Current goal

Makad should still have:

- real-time speech input capability;
- low-latency recognition/turn handling;
- ability to understand useful spoken intent;
- barge-in / interruption handling;
- safety rules preventing partial or stale recognition from causing unintended physical action.

Before interpreted speech can trigger consequential physical motion, Makad should emit a brief, legible pre-action cue and retain utterance/session cancellation integrity. The cue is a repair and safety mechanism, not permission for partial ASR output to actuate the robot.

But Makad’s own primary expressive output can be closer to a Star Wars droid:

- chirps;
- whistles;
- trills;
- tonal / synthetic vocalizations;
- coordinated eye/head/body performance.

The **creative language design is intentionally deferred**. The engineering system must support it without prematurely inventing the vocabulary.

### Important engineering consequence

A droid voice is not acoustically free.

Tonal output can be difficult for acoustic echo cancellation, especially when:

- Makad vocalizes frequently;
- the head moves during the vocalization;
- the speaker-to-microphone echo path changes;
- the vocal material is spectrally narrow.

The later creative sound vocabulary should therefore preserve enough spectral diversity for robust audio processing rather than being designed as pure whistles only.

---

## 12. Vision and person perception

Makad’s camera/perception stack is structured as layers rather than “camera box → servo.”

### Core separation

The system distinguishes:

1. calibrated image/camera observations;
2. temporal tracking;
3. attention/person selection;
4. scene/presence reasoning;
5. gaze control;
6. high-level behaviour.

The camera is mounted on a moving head, so camera pose is time-varying.

Important carried-forward principles include:

- calibrated camera geometry;
- capture-time head pose;
- moving-camera ego-motion compensation;
- timestamp discipline;
- rolling-shutter characterization where relevant;
- explicit uncertainty;
- temporal person/face tracks;
- occlusion/loss/reacquisition logic;
- attention selection separate from raw tracking;
- no assumption that a temporary track ID equals persistent human identity;
- privacy-conscious, session-bounded logic rather than biometric re-identification;
- offline replay and deterministic timestamp-based temporal logic;
- explicit handling of ambiguity and scene saturation rather than inventing facts.

A target around **1.5° P95 visual bearing error** and sub-second active acquisition/established-perception timing has been used in the visual tracking work, subject to validation.

---

## 13. Audio-visual fusion / social presence

Makad needs more than independent camera and microphone outputs.

The fused social scene should reason about things such as:

- who is currently observed;
- who is believed present but temporarily unobserved;
- which sound direction plausibly corresponds to which visible person;
- whether a speaker cannot be safely associated;
- human orientation toward Makad;
- addressing evidence;
- salience;
- entry / departure / occlusion;
- uncertainty and staleness.

Important design rules:

- ambiguity is a valid output;
- `UNASSOCIATED` is better than confidently attaching a sound to the wrong person;
- stale information must remain visibly stale;
- snapshots should be authoritative; events are hints;
- event timestamps, not loop tick counts, should drive temporal logic;
- presence/session handles are not biometric identity.

---

## 14. Behaviour architecture

Makad’s behaviour is intentionally layered.

### 14.1 Procedural aliveness — SPEC-12

Procedural aliveness owns:

- continuous/stochastic low-amplitude life;
- blinking;
- gaze drift / small attention changes;
- other bounded idle variation;
- low-amplitude base contribution under strict constraints, explicitly **STRETCH and marginal**.

It does **not** own authored dramatic sequences.

The procedural system uses a single arousal/integration model rather than separate unrelated intensity systems. Stimulus class is a stable enum: class weights are absolute, never renormalized when classes are added, and a new class defaults to zero contribution until intentionally configured.

The corrected SPEC-12 math direction is `u = clamp(Σ w_c · h_c)`, with habituation gating the stimulus input. Saturation awareness is evaluated in summed coordinates; gaze step amplitude is separate from maximum idle offset; C12-R18 applies only to the procedural layer; and C12-T11 carries the baseline correction. These references must be verified once the canonical spec is restored.

The guaranteed V1 idle floor is **display-only blink + gaze drift, zero servo motion, and a physical power switch**. Neck and base idle motion are additions above that floor, not prerequisites for a viable idle state.

### 14.2 Authored performances — SPEC-13

Authored performances own deliberate, recognizable transients such as:

- curious approach;
- dramatic turn toward caller;
- excited spin;
- small side-to-side body motion;
- startle response;
- other choreographed multi-channel gestures.

The performance layer coordinates channels in perceived time, accounting for different physical onset latencies.

### 14.3 High-level behaviour / arbitration — planned SPEC-20

The higher-level system chooses what Makad is doing and resolves:

- attention;
- interaction state;
- wake/addressing;
- performance selection;
- procedural versus deliberate behaviour;
- safety and inhibit interactions.

A runtime `current_emotion` enum is intentionally avoided as the central architecture. Affect state and performances remain distinct mechanisms.

Affect state modulates generation and selection; a performance is an authored, time-bounded act. Neither mechanism is a runtime “current emotion.”

SPEC-20 does not exist yet. Until it is authored, the items above are required ownership for the future arbitration layer, not an implemented contract.

### 14.4 Redundant gaze channels and shared composition

Eyes, neck yaw and base yaw all serve the same objective: putting a target on axis. They must not independently close the same error or they will fight. **SPEC-13 owns distribution of the gaze target across these channels** because SPEC-16 owns safe base execution but deliberately declines behavioural distribution.

The intended policy is still “eyes first, head next, base for larger body orientation,” but this is a control-allocation rule as well as an interaction aesthetic. The distributor must account for eye/head travel, preferred neutral zones, saturation, channel latency and base inhibits; only one layer owns the residual error passed downstream.

Procedural, performance, gaze and inertial contributions converge through one shared output/composition stage. It owns per-channel gains, summation, slew limiting, post-sum clamps and the single arousal integrator. This machinery is extracted from the SPEC-12/13 lineage and must not be reimplemented independently by each caller.

---

## 15. Mobile-base architecture and safety

Wheels are a first-class part of Makad. The base uses two independently driven, encoded wheels plus passive support for differential-drive forward/reverse motion, arc turns and near-in-place rotation. It is statically supported, not self-balancing. A ball or dual caster arrangement is preferred over an ordinary swivel caster for frequent expressive reversals, but final type and placement remain an open stability/drag decision.

The command path is:

**behaviour intent → procedural/performance contributions → summed `(v, ω)` → safety clamp → differential-drive conversion → wheel targets**

Safety clamps the final combined request. Obstacle and cliff inhibition execute in the low-level real-time path, independent of high-level behaviour, with **detection → deceleration command ≤50 ms** as the carried MUST. The sensing envelope must satisfy:

`d_available > v * t_latency + v² / (2 * a_brake) + d_margin`

A 6-axis IMU is MUST-HAVE because encoders alone cannot detect lift, tip/fall, slip, airborne wheel spin, several stuck conditions or short-term yaw disagreement. Floor and elevated-surface operation require different speed envelopes.

Active listening may inhibit locomotion when drive noise damages microphone performance. That veto suppresses only the base track; display, audio and neck continue. Startle begins with rapid deceleration to stop, carries immediate intensity through fast channels, and permits only a later separate bounded retreat—never a fast blind reverse.

At zero commanded velocity the drive must resist head-reaction torque well enough to prevent accidental-looking body twitch. The base footprint should stay inside the circle swept about the drive-wheel axle midpoint during near-in-place turns. The head may protrude, but floor-level sensors do not protect it; its height/sweep limit remains OQ-20. Low-level recovery, rear-space coverage and bounded blind crawl remain unresolved.

---

## 16. Base expression, timing and head coordination

The base is both transport and a body-scale expressive channel: orientation, approach, hesitation, cautious retreat, spin, side-to-side movement and startle follow-through. Its hardest motions occur near zero speed, where stiction, backlash, encoder quantization and reversal deadband are most visible. Minimum controllable speed and reversal quality are therefore character acceptance criteria, not merely drivetrain metrics.

Very small expression uses **discrete micro-moves above the validated controllable speed, separated by dwell**. Sustained sub-threshold crawling is non-conforming.

Procedural base behaviour is **STRETCH and marginal**. If enabled, it may contribute only bounded, non-goal-directed micro-motion before the SPEC-16 safety clamp. Navigation/performance wins conflicts; listening inhibit or sleep forces it to zero; proximity suppresses it before safety repeatedly catches it; and its integrated displacement must be bounded or biased toward an origin estimate. It must not become navigation, approach, retreat, sustained travel or a hidden performance system.

The five currently defined authored base performances are curious approach, dramatic turn toward caller, excited spin, small side-to-side motion and startle. Side-to-side is hardware-gated because it stresses reversals most severely.

The geared base has a provisional visible onset of **150–400 ms**, so reactions lead with display/audio, then neck, then base follow-through. Early authoring uses animation-derived **80–170 ms per-link offsets**; measured onset distributions replace these later. Timing is authored in perceived time: compensation removes variable system lag so an author can still request deliberate lag. Intentional and unintended lag are different mechanisms.

Two head/base couplings remain deliberately separate:

- **Base yaw compensation:** the gaze distributor commands geometric head counter-rotation to preserve fixation.
- **Linear-acceleration pitch:** expressive pitch uses **commanded trajectory acceleration as feedforward**, because the IMU arrives too late for anticipation. IMU/odometry may provide feedback correction and is the only path for safety- or externally-originated motion, where visible lag is accepted.

Using IMU acceleration as the primary planned-motion cue would wire the timing backward: commanded motion is knowable before it begins, while inertial feedback is necessarily reactive.

---

## 17. System-level interfaces that are now important

Cross-subsystem integration increasingly depends on timestamped, explicit interfaces.

Examples include:

- measured neck joint pose → camera transform;
- visual observations → temporal tracks;
- tracks → attention/gaze;
- audio DOA + uncertainty → fusion;
- body yaw/yaw-rate → audio ego-motion compensation;
- odometry/IMU → scene reasoning;
- behaviour/performance → expressive `(v, ω)` contribution;
- safety → final base clamp;
- audio/behaviour → locomotion listening inhibit;
- base acceleration → neck expressive pitch coupling;
- base yaw → geometric head counter-rotation;
- channel latency models → performance scheduler;
- faults/degraded state → behaviour arbitration.

The gaze-target distribution decision is traceable to **C16-R74**: SPEC-16 declines to own distribution across eyes, neck and base; SPEC-13 owns that distribution; planned SPEC-20 owns follow-versus-ignore and approach policy.

SPEC-10 is a protocol plus caller-driven registry, not a frozen capability catalogue. Its registry starts empty and grows only as real callers define supported contracts.

The architecture should prefer explicit state, timestamps, confidence and inhibition over hidden coupling.

---

## 18. Current “do not accidentally regress” register

When extending Makad, preserve these rules:

1. Previous accepted specs are constraints unless a real cross-system contradiction is found.
2. Contradictions are flagged and amended explicitly; they are not silently rewritten.
3. Existing requirement/test IDs survive tracked amendments.
4. New requirements append new IDs.
5. MUST / TARGET / STRETCH status is explicit.
6. Unmeasured numeric values are PROVISIONAL.
7. Every important new MUST gets an acceptance test.
8. Safety belongs in the low-level path where required.
9. Perception uncertainty must be representable.
10. A track ID / session handle is not a persistent real-world identity.
11. Behaviour does not directly spray raw servo angles or wheel PWM.
12. Safety clamps act after expressive contributions are summed.
13. Procedural idle and authored performance are different mechanisms.
14. Expressive timing is authored in perceived time with per-channel onset compensation.
15. Status/confidence is not the same thing as behavioural importance.
16. Exact parts are not selected until coupled requirements are sufficiently complete.
17. There is no central runtime `current_emotion` enum; affect state and authored performances are distinct mechanisms.
18. Timing is authored in perceived time with per-channel onset offsets; compensation preserves intentional lag.
19. SPEC-13 owns gaze/channel distribution, SPEC-16 declines it, and planned SPEC-20 owns follow/ignore and approach policy.
20. The supersedes register lives in SPEC-13; retired source specs retain one-line forwarding stubs.
21. The V1 idle floor is display-only blink plus gaze drift, with zero servo motion and a physical power switch.

---

## 19. Open-question register

This is the single canonical project-level open-item list. MEMORY entries reference these IDs rather than maintaining a second mutable register.

### OQ-01 — Final neck roll implementation
Powered roll must justify its mass, torque, wiring and schedule cost.

### OQ-02 — Neck actuator/encoder architecture
Freeze actuator class, transmission and joint-side sensing.

### OQ-03 — Final body/head CAD envelope
Reconcile display, camera, mics, speaker, neck, compute, battery, drive, sensing, service panels and centre of mass.

### OQ-04 — Final compute split
Freeze high-level SBC and low-level real-time controller responsibilities.

### OQ-05 — Power architecture
Close battery, regulation, peak motor/audio/compute current, thermal and runtime budgets together.

### OQ-06 — Acoustic validation
Measure four-mic DOA uncertainty, isolation, drive contamination and moving-path AEC.

### OQ-07 — Droid-language design
Author the vocabulary within spectral-diversity, timing and interruption constraints.

### OQ-08 — Moving-array ego-motion
Implement synchronized body/head compensation for audio and vision.

### OQ-09 — Final drivetrain
Select motor, reduction, wheel, encoder and driver against safety and expressive-quality tests.

### OQ-10 — Desk versus floor operating envelope
Define distinct speed, edge-sensing, braking-distance and recovery envelopes.

### OQ-11 — Rear recovery sensing
Resolve rear coverage versus tightly bounded crawl retreat.

### OQ-12 — Procedural-base usefulness under active listening
Measure whether the STRETCH layer executes often enough to justify itself.

### OQ-13 — Exact performance timing
Bench-measure per-channel onset distributions and replace provisional offsets.

### OQ-14 — Consolidated master engineering spec
Produce one cross-consistent architecture after canonical sources and traceability IDs are restored.

### OQ-15 — Exact BOM and build sequence
Defer until architecture, budgets and validation criteria are sufficiently closed.

### OQ-16 — SPEC-20 authorship
Author follow-versus-ignore, approach policy and the arbitration contract.

### OQ-17 — SPEC-07 audio representation
Choose fixed clips versus parameterized/time-stretchable synthesis; this blocks final performance authoring.

### OQ-18 — Caster configuration
Select and validate support geometry for reversal quality, stability, noise and swept footprint.

### OQ-19 — VLM decision
Decide whether a VLM belongs in V1, later scope or not at all.

### OQ-20 — Head-height sweep limit
Define the allowable protruding-head sweep that floor-level sensors cannot protect.

### OQ-21 — Canonical spec restoration and traceability
Restore the `SPEC-*` sources, verify requirement/test IDs, apply or reject the drafted SPEC-13 and SPEC-16 deltas, and close `UNTRACED` references in MEMORY.

---

## 20. Document hierarchy

Use the project documents with this intended precedence:

1. **Canonical subsystem specs** — exact engineering truth.
2. **SPEC-13 supersedes register** — explicit changes to those specs; each retired source retains a one-line forwarding stub.
3. **README.md** — current global context and orientation.
4. **MEMORY.md** — append-only historical decision log.
5. **Concept art / renders / informal discussion** — inspiration and history only.

If an old render says “2 ear microphones” but the current audio spec says “4 body microphones,” the audio spec wins.

If README and a canonical spec disagree, fix README; do not silently change the spec.

The canonical specs are absent from this workspace, so application status and exact requirement IDs cannot be audited here. Until OQ-21 closes, any claim that a delta is “applied” is provisional unless its source document is supplied.

---

## 21. One-sentence definition

**Makad is a small modular droid-like companion robot whose core engineering challenge is to make perception, eyes, sound, head motion and differential-drive body motion coordinate convincingly enough that the machine appears attentive, curious and alive.**
