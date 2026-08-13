# MAKAD — SPEC-20 v1.0
## Central Behaviour Executive, Attention Policy & Whole-Robot Arbitration

**Source capability:**  
**#20 — Makad will run all capabilities through one central behaviour system.**

**Status:** Final requirements-phase specification / system-integration freeze candidate  
**Subsystem:** High-level behaviour executive (the “brain”)  
**Primary dependencies:** SPEC-01 through SPEC-13 and SPEC-16  
**Retired numbering carried forward:** SPEC-14, SPEC-15 and SPEC-17–19 do not introduce separate runtime owners; their surviving constraints are inherited through the current project register.

---

# 1. Scope of this specification

SPEC-20 defines the high-level system that decides, at any given time:

- what Makad is attending to;
- whether a perceived person, sound or event should be ignored, acknowledged, inspected or engaged;
- whether Makad should remain idle, listen, respond, perform, orient, approach, follow, retreat, roam locally or stop;
- which authored performance or utility action is appropriate;
- which concurrent activities are compatible;
- which activity must yield when priorities, inhibits, faults or resource conflicts change;
- how an action is proposed, announced, committed, monitored, completed, cancelled or failed;
- how the robot degrades when perception, networking, reasoning, audio, display, neck or locomotion is unavailable.

It is the integration layer that turns independently capable subsystems into one robot.

The intended system chain is:

```text
timestamped observations + subsystem health + interaction context
                              │
                              ▼
                  authoritative world snapshot
                              │
                              ▼
                  behaviour candidate generation
                              │
                              ▼
             eligibility + priority + resource arbitration
                              │
                              ▼
               semantic intents / performance requests
                              │
                              ▼
       SPEC-01/12/13/16 and audio/utility execution layers
                              │
                              ▼
                   measured outcome + feedback
                              │
                              └──────────→ next snapshot
```

SPEC-20 covers:

- high-level operating and interaction state;
- typed event intake and authoritative-state consumption;
- attention-target selection and switching policy;
- behaviour candidate generation;
- arbitration and pre-emption;
- resource/channel lease requests;
- action transaction lifecycle;
- speech-, presence-, novelty- and fault-driven reactions;
- approach, follow, body-orientation and local-roaming policy;
- selection of SPEC-13 performances;
- enabling/suppressing SPEC-12 procedural life;
- listening-motion-inhibit policy;
- utility-task invocation and display handoff;
- short-lived interaction context needed for behaviour;
- affective modulation without a central `current_emotion` enum;
- fault response and graceful degradation;
- system-level timing instrumentation;
- behaviour logging, deterministic replay and validation hooks;
- interfaces required to close the sense → decide → act → observe loop.

SPEC-20 does **not** own:

- raw camera acquisition or calibration — SPEC-08;
- person/face detection and temporal tracking — SPEC-09;
- visual novelty or semantic inspection — SPEC-10;
- acoustic capture, VAD, STT, DOA or AEC — SPEC-04/05;
- low-level semantic interpretation of finalized speech — SPEC-06;
- droid sound generation or audio mixing — SPEC-07;
- procedural motion generation — SPEC-12;
- authored performance timing or gaze-channel distribution — SPEC-13;
- neck servo control — SPEC-02;
- wheel control, obstacle/cliff safety, motor inhibit or local recovery — SPEC-16;
- raw actuator angles, motor PWM or wheel-speed control;
- safety-grade collision clearance;
- full SLAM, maps or global path planning;
- biometric identity or persistent person recognition;
- unrestricted autonomous agency;
- a mandatory LLM, VLM or cloud dependency;
- the final set of utility-assistant features;
- exact SBC, MCU, middleware, behaviour-tree library or language selection.

The central boundary is:

> **SPEC-20 owns what Makad intends to do. It does not bypass the subsystems that own how the intent is rendered, controlled or made safe.**

---

# 2. Existing Makad decisions that constrain this spec

## 2.1 Makad is character-first

Makad must feel attentive and alive before it becomes a broad utility assistant. The brain must therefore protect:

- immediate visible acknowledgement;
- coherent attention;
- interruptibility;
- expressive timing;
- graceful uncertainty;
- idle aliveness;
- physical safety.

It must not sacrifice these for speculative general-purpose reasoning.

## 2.2 Expression is layered, not monolithic

The established expressive stack separates:

- **character/affect state** — slow modulation;
- **procedural aliveness** — bounded stochastic life, owned by SPEC-12;
- **authored performances** — recognizable time-bounded acts, owned by SPEC-13;
- **gaze distribution** — allocation of an authorised bearing across eyes, neck and base, owned by SPEC-13;
- **physical execution and safety** — owned by the channel subsystems.

SPEC-20 may select or modulate those mechanisms. It shall not recreate them.

## 2.3 There is no central `current_emotion` enum

Affect and performance are distinct:

- affect changes likelihood, strength, tempo and settling;
- a performance is a concrete act with a start, execution and end.

Makad shall not be architected around one mutually exclusive label such as `HAPPY`, `SAD` or `CURIOUS` that implicitly drives every subsystem.

## 2.4 Procedural idle and authored performances have separate owners

SPEC-12 owns low-amplitude procedural aliveness. SPEC-13 owns deliberate gestures. Suppressed procedural base events are discarded, not queued. The V1 idle floor is display-only blink and gaze drift with zero servo or wheel motion.

## 2.5 Attention selection and gaze realization are separate

SPEC-20 decides **whether and to whom** Makad attends.

Once a target/bearing is authorised, SPEC-13 decides **how** rendered eyes, neck yaw and base yaw share the gaze task under C13-R81–C13-R97.

SPEC-20 shall not run a second eye/head/base distribution controller.

## 2.6 The base is expressive but independently safety-limited

The base command path remains:

```text
behaviour intent
    + expressive/procedural contribution
    → summed (v, ω)
    → low-level safety clamp
    → differential-drive execution
```

Obstacle/cliff inhibition, motor watchdog, pickup/tip response and local stop/recovery remain below SPEC-20. Startle never authorises a blind fast reverse.

## 2.7 Listening can inhibit locomotion

The four-microphone array is body-mounted. Drive motion can rotate its reference frame and inject structure-borne noise. Audio/behaviour may therefore assert a listening-motion inhibit distinct from emergency or safety motor inhibit.

During that inhibit:

- base translation and rotation used only for expression, tracking or approach are unavailable;
- eyes and neck remain available within their validated envelopes;
- safety authority remains active;
- deferred base unwind follows SPEC-13 after release.

## 2.8 Speech is continuous, interruptible and action-safe

Inherited voice constraints include:

- visible speech acknowledgement at p95 ≤350 ms, with ≤250 ms TARGET;
- simple speech-end → droid-audio response at p95 ≤1.5 s, with ≤1.0 s TARGET;
- partial transcripts cannot authorise consequential motion;
- utterances have lifecycle IDs and cancellation;
- barge-in is detected without waiting for final transcription;
- ordinary speech-triggered locomotion uses a pre-action tell and cancellation interval;
- stop/cancel/inhibit bypasses that interval;
- core interaction remains usable without generative reasoning.

## 2.9 Perception exposes uncertainty, freshness and ambiguity

SPEC-20 shall consume typed, timestamped observations rather than infer truth from raw pixels, bounding boxes or audio buffers.

The existing perception lineage requires:

- session-scoped tracks/handles rather than identity;
- explicit staleness;
- uncertainty;
- `UNASSOCIATED`/ambiguous outcomes;
- capture-time geometry;
- authoritative snapshots, with events used as hints;
- offline replay.

## 2.10 The visual semantic path is optional and slow

SPEC-10 semantic inspection is trigger-driven, asynchronous and subordinate to real-time person tracking. It may return uncertainty or failure. Makad must be able to show “examining/thinking” immediately without pretending the semantic result is already known.

## 2.11 No touchscreen dependency

The animated face remains Makad’s default identity. Utility UI may temporarily take the display but no core behaviour may require touchscreen input.

## 2.12 Retired capabilities do not create missing runtime owners

The current project map retires SPEC-14/15/17/18 and closes SPEC-19 without a document. Their surviving obligations are routed as follows:

- utility/no-touchscreen constraint → SPEC-01 and SPEC-20;
- locomotion safety and obstacle response → SPEC-16;
- expressive locomotion generation → SPEC-12/13;
- perception-controlled follow/approach policy → SPEC-20, executed by SPEC-16.

## 2.13 Explicit cross-spec ownership resolution: audio-visual association

The available project record contains two historical statements:

1. SPEC-09 assigned eventual audio-visual association to SPEC-20 unless a dedicated fusion layer was established.
2. The later SPEC-11/current project register treats fused social presence and evidence-level audio-visual association as a dedicated perception responsibility.

This specification adopts the later split:

- **SPEC-11/fusion lineage owns evidence-level association**, including associated, unassociated and ambiguous hypotheses with uncertainty and freshness;
- **SPEC-20 owns the behavioural consequence**, including whether to switch attention, acknowledge, engage, clarify or do nothing.

This is an explicit resolution, not a silent reversal. SPEC-09’s old “SPEC-20 owns association” stub must be patched during master-spec consolidation.

---

# 3. Engineering reasoning / architecture

## 3.1 Why a single giant state machine is the wrong model

Makad can be simultaneously:

- awake;
- listening;
- looking at one person;
- running a blink generator;
- waiting for a semantic result;
- holding the base stationary due to audio inhibit;
- displaying a short acknowledgement;
- monitoring an action transaction.

Representing every combination as one mutually exclusive global state produces a combinatorial state explosion.

SPEC-20 shall instead use orthogonal state dimensions:

| Dimension | Examples | Owner |
|---|---|---|
| Operational health | booting, ready, degraded, faulted | SPEC-20 from subsystem health |
| Character availability | awake, drowsy, asleep | SPEC-20 policy |
| Interaction phase | unengaged, acknowledging, listening, interpreting, responding | SPEC-20 + voice lifecycle |
| Attention commitment | none, track/session handle, novelty bearing, sound bearing | SPEC-20 |
| Action transaction | proposed, pending, committed, executing, terminal | SPEC-20 |
| Performance execution | queued/active/settling | SPEC-13 feedback |
| Channel safety/availability | available, inhibited, faulted | owning subsystem |
| Affect/arousal modulation | bounded continuous variables | SPEC-12/shared composition lineage |

These dimensions may be implemented with statecharts, a behaviour tree plus blackboard, an event-driven executive or a small hybrid. The implementation technology remains open; the ownership and testable semantics do not.

## 3.2 Authoritative snapshots, not event-only truth

Events are useful for low-latency wake-up:

```text
SPEECH_STARTED
PERSON_ENTERED
TARGET_LOST
NOVELTY_CONFIRMED
OBSTACLE_STOPPED_BASE
```

But events can be delayed, duplicated, reordered or missed. Therefore each arbitration decision shall be made against an immutable, versioned world snapshot containing current state and freshness.

An event means:

> “Re-evaluate now.”

It does not mean:

> “Assume this historical statement remains true.”

## 3.3 Candidate-based arbitration

Each behaviour provider may propose a candidate with at least:

```text
candidate_id
behaviour_type
cause/correlation_id
priority_class
utility or preference within class
preconditions
freshness/expiry
required resources
optional resources
interruptibility
minimum/maximum useful duration where relevant
fallback if denied or pre-empted
semantic output intent
```

The arbiter filters candidates in this order:

```text
validity/freshness
    → safety and inhibit eligibility
    → preconditions
    → resource compatibility
    → priority partial order
    → hysteresis / continuation preference
    → utility or deterministic tie-break
```

This prevents one numeric “emotion score” from accidentally outranking stop, safety or listening requirements.

## 3.4 Priority is a partial order, not one magic score

The minimum required precedence is:

```text
LOW-LEVEL HARDWARE / COLLISION / CLIFF SAFETY VETO
                         ↓
SYSTEM STOP, CANCEL, SHUTDOWN OR FAULT CONTAINMENT
                         ↓
BARGE-IN, ACTIVE LISTENING AND REQUIRED AUDIO INHIBITS
                         ↓
COMMITTED USER INTERACTION / AUTHORISED ACTION
                         ↓
REACTIVE ATTENTION AND ESSENTIAL RESPONSE PERFORMANCE
                         ↓
VOLUNTARY PERFORMANCE, ROAMING OR OPTIONAL UTILITY WORK
                         ↓
PROCEDURAL IDLE CONTRIBUTIONS
```

Safety veto is not merely the highest-scoring behaviour. It remains independent authority below the high-level executive.

Compatible activities may run concurrently. For example, listening may coexist with eye fixation and blinking while base motion is inhibited.

## 3.5 Resource leases prevent hidden actuator fights

SPEC-20 requests semantic resources; it does not directly lock motors.

Minimum logical resources are:

| Resource | Typical exclusivity | Notes |
|---|---|---|
| Attention commitment | One primary target | Candidate tracks may remain observed |
| Gaze objective | One authorised spatial objective | Realized by SPEC-13 |
| Authored performance slot | Normally one foreground performance | SPEC-13 owns channel-level scheduling |
| Base travel intent | One goal-directed owner | Safety may always veto |
| Audio foreground output | Mixer/policy controlled | Listening/barge-in may duck/cancel |
| Display utility mode | Exclusive with face-as-primary view | Must return cleanly to face |
| Semantic-inspection request | Bounded queue | Does not block real-time executive |
| Consequential action transaction | Bounded concurrency; V1 may serialize | Stop/cancel remains global |

Procedural life is not represented as an ordinary foreground lease. It continues generating under SPEC-12 and is gated/composed by the established shared stage.

## 3.6 Semantic commands preserve subsystem ownership

Conforming outputs resemble:

```text
ATTEND(track_handle)
PLAY_PERFORMANCE("curious_ack", parameters)
REQUEST_BASE_APPROACH(target_handle, social_range_policy)
SET_LISTENING_MOTION_INHIBIT(true)
START_SEMANTIC_INSPECTION(region_handle)
SHOW_UTILITY_VIEW(task_handle)
CANCEL_ACTION(action_id)
```

Non-conforming outputs include:

```text
set_neck_servo(37°)
set_left_motor_pwm(180)
move_eye_pixels(+14)
ignore_obstacle_for_500ms
```

## 3.7 Attention policy needs commitment and hysteresis

Continuity is socially important. Makad should not flick between two faces because frame-by-frame confidence changes slightly.

The target policy therefore distinguishes:

- observed candidates;
- current committed target;
- addressing evidence;
- speaker-association evidence;
- explicit user/utility target request;
- target loss/occlusion;
- target abandonment;
- target replacement.

A target switch requires a meaningful reason, such as:

- the current target becomes invalid beyond its inherited loss tolerance;
- another person clearly addresses Makad;
- a supported command explicitly changes target;
- the current interaction ends and a more salient event persists;
- safety or fault response requires attention elsewhere.

One noisy frame, one uncertain DOA sample or a small score difference is insufficient.

## 3.8 Attend, orient, approach and follow are different commitments

These actions have increasing cost:

```text
eye acknowledgement
    < head attention
    < body orientation
    < approach/reposition
    < sustained following
```

Seeing a person does not automatically authorise following. Hearing a sound does not automatically authorise driving toward it.

V1 follow/approach requires:

- a currently valid social target;
- sufficient target freshness and geometry for the requested action;
- explicit behavioural eligibility (supported command, interaction policy or authored scenario);
- a valid locomotion-safety stream;
- no listening-motion inhibit that forbids the required base motion;
- continuous execution feedback;
- stop/slow behaviour on target loss or uncertainty growth.

Social distance bands and dwell times remain prototype-tuned TARGET quantities, not safety distances.

## 3.9 Consequential actions are transactions

Speech-triggered locomotion and other consequential actions shall use:

```text
PROPOSED
    → VALIDATED
    → ANNOUNCED / CANCELLABLE PENDING
    → COMMITTED
    → EXECUTING
    → COMPLETED
```

with terminal alternatives:

```text
CANCELLED | REJECTED | ABORTED | FAILED | TIMED_OUT
```

Every transition is associated with one action ID and originating cause/utterance ID. Late results for cancelled causes cannot resurrect the action.

STOP, cancel, inhibit and safety response bypass the normal pending delay.

## 3.10 Affect changes selection; it does not issue acts

The brain may maintain bounded modulators such as arousal, engagement or interaction momentum. Exact dimensions are not frozen.

They may influence:

- which compatible acknowledgement variant is selected;
- procedural amplitude within SPEC-12 limits;
- performance intensity within SPEC-13 limits;
- how quickly Makad settles toward idle;
- whether an optional social action is worth proposing.

They may not:

- bypass safety or confidence gates;
- replace the explicit interaction/action lifecycle;
- become an implicit actuator API;
- create a second arousal integrator competing with the shared SPEC-12/13 composition lineage.

## 3.11 Failure must reduce ambition, not produce nonsense

Examples:

| Failure | Required high-level response |
|---|---|
| Network/LLM unavailable | Retain deterministic local interactions and droid responses |
| VLM unavailable/slow | Cancel or report inspection uncertainty; continue tracking/listening |
| Camera unavailable | Stop visual following; permit audio-led acknowledgement without invented visual target |
| Audio input unavailable | Stop listening state; retain visual/procedural interaction |
| Neck unavailable | Use display gaze; do not repeatedly command failed neck |
| Display unavailable | Stop claiming visible acknowledgement; use audio/physical channels if safe |
| Base inhibited/faulted | Continue face/head interaction; do not queue travel for later burst |
| Behaviour process lost | Low-level base watchdog stops; safety/recovery remain independent |

## 3.12 Timing is end-to-end and measured

For speech acknowledgement:

\[
T_{ack}
=T_{detect}+T_{transport}+T_{snapshot}+T_{arb}+T_{dispatch}+T_{render}
\]

The inherited end-to-end limit is p95 ≤350 ms. Therefore the final internal arbitration allowance shall be derived from measured non-SPEC-20 terms:

\[
T_{arb,allow}
=350\text{ ms}
-\left(T_{detect}+T_{transport}+T_{snapshot}+T_{dispatch}+T_{render}\right)
\]

An initial **TARGET** is p95 ≤100 ms from receipt of a valid high-priority event to dispatch of the corresponding semantic response request, but this is an allocation to validate, not a claim about measured hardware.

Time-based behaviour must use monotonic timestamps/deadlines, not loop-tick counts.

## 3.13 The brain is not the safety controller

SPEC-20 may decide not to move. It may request stopping. It may interpret why a stop occurred.

It is not the final authority that makes movement safe.

The low-level system must still stop for obstacles, cliffs, communication loss, pickup/tip conditions and motor inhibit when SPEC-20 is delayed, deadlocked, overloaded or restarted.

## 3.14 Generative models are advisory workers

An LLM or VLM may propose:

- a communicative act;
- a utility result;
- a semantic interpretation;
- candidate parameters from an allow-list.

Its output must pass schema validation, freshness checks, capability allow-lists and normal action arbitration. It cannot acquire actuator resources, bypass the action transaction or write directly to channel controllers.

## 3.15 Replayability is required to debug emergence

Cross-system bugs often depend on ordering:

```text
person appears
→ sound begins
→ target switches
→ barge-in occurs
→ base inhibit arrives
→ performance is pre-empted
```

The behaviour layer therefore needs a decision journal containing inputs, snapshot revision, candidate set, rejections, winning intents, leases, action transitions and execution feedback. Random choices must be reproducible from logged seeds or selected outcomes.

Raw camera/audio storage is not required and remains governed by the existing privacy policies.

---

# 4. Formal requirements

## 4.1 Ownership and architecture

### C20-R01 — Central intent authority — MUST

All non-safety autonomous whole-robot behaviour shall pass through one logically central SPEC-20 authority before becoming a semantic attention, performance, utility or goal-directed locomotion intent.

Subsystem-local reflexes explicitly owned elsewhere—collision stop, cliff stop, watchdog stop, motor inhibit and bounded local recovery—are exempt and retain independent authority.

### C20-R02 — No direct actuation — MUST

SPEC-20 shall not output raw servo angles, eye pixels, motor PWM or unbounded wheel targets. Outputs shall use typed subsystem interfaces and preserve the receiving subsystem’s limits, composition and safety ownership.

### C20-R03 — Orthogonal runtime state — MUST

The architecture shall represent operational health, interaction phase, attention commitment, action lifecycle and performance execution as separable state dimensions rather than one exhaustive global enum.

### C20-R04 — Implementation replaceability — TARGET

Behaviour-tree, statechart, rule-engine or equivalent implementation details should be replaceable without changing externally visible typed contracts or acceptance scenarios.

### C20-R05 — Bounded high-level queues — MUST

Every event, worker-request and action queue shall have an explicit capacity and overload policy. Unbounded queues are prohibited.

### C20-R06 — Monotonic time semantics — MUST

Expiry, dwell, timeout, hysteresis and action deadlines shall use a common monotonic robot timebase. Loop iterations shall not be treated as elapsed time.

## 4.2 Input truth and context

### C20-R07 — Versioned authoritative snapshot — MUST

Every arbitration decision shall reference an immutable/versioned snapshot containing the relevant perception, interaction, subsystem-health, inhibit and execution state.

### C20-R08 — Events are hints — MUST

Events may trigger immediate reevaluation but shall not override contradictory newer authoritative state.

### C20-R09 — Freshness visibility — MUST

Inputs used for behaviour eligibility shall expose observation/effective time, receipt time where different, freshness/age and validity. Missing or stale data shall not be silently treated as current.

### C20-R10 — Uncertainty preservation — MUST

Unknown, ambiguous and unassociated perception results shall remain representable through arbitration and behaviour selection. SPEC-20 shall not fabricate a person, object identity, range or association to simplify logic.

### C20-R11 — Session-scoped people — MUST

Attention and interaction shall use session/track handles. SPEC-20 shall not infer persistent biometric identity from a temporary handle or retain identity across sessions without a future explicitly approved subsystem.

### C20-R12 — Bounded short-term interaction context — MUST

Conversation/interaction context shall have explicit session ownership, expiry/reset rules and maximum retained scope. It shall reset on session termination, explicit reset or invalidating restart.

## 4.3 Candidate generation and arbitration

### C20-R13 — Typed behaviour candidates — MUST

Each candidate shall declare cause, priority class, validity/expiry, preconditions, resource claims, interruptibility, semantic output and denial/pre-emption behaviour.

### C20-R14 — Eligibility before preference — MUST

Stale, unsafe, inhibited, unsupported or precondition-failing candidates shall be removed before utility/preference comparison.

### C20-R15 — Required precedence — MUST

The arbiter shall enforce the partial order in §3.4. No tuning weight or affect value may outrank stop/cancel, required listening inhibit or low-level safety veto.

### C20-R16 — Compatible concurrency — MUST

The executive shall permit compatible activities to coexist. It shall not stop blinking, eye fixation or safe listening posture merely because one foreground interaction is active.

### C20-R17 — Deterministic tie handling — MUST

Given identical snapshot, candidate set, configuration and random seed, arbitration results shall be reproducible. Equal-priority conflicts require a documented deterministic tie-break or logged randomized selection.

### C20-R18 — Continuation hysteresis — MUST

An active valid behaviour or target shall receive bounded continuation preference so small score fluctuations do not cause rapid switching. Hysteresis shall never block stop, cancel, safety or an invalidation condition.

### C20-R19 — Starvation visibility — TARGET

The system should detect/log candidates that remain eligible but repeatedly lose arbitration, enabling tuning of accidental starvation without promising that every optional candidate eventually runs.

### C20-R20 — Lease and denial feedback — MUST

Every requested logical resource shall return granted, denied, pre-empted, inhibited, faulted or completed state. SPEC-20 shall not assume that dispatch implies execution.

### C20-R21 — Clean pre-emption and handback — MUST

On pre-emption, the outgoing activity shall cancel/settle according to its declared policy. The successor and resumed lower layer shall start from current measured/execution state, not a stale pre-interruption command.

### C20-R22 — Suppressed idle is not backlogged — MUST

Procedural actions suppressed by sleep, performance ownership, navigation, listening inhibit or safety state shall be discarded in accordance with SPEC-12, not queued for later playback.

## 4.4 Attention and social engagement

### C20-R23 — One primary attention commitment — MUST

Makad shall expose at most one primary behaviourally committed attention target at a time, while allowing perception to maintain multiple candidates.

### C20-R24 — Target-switch evidence — MUST

A primary target switch shall require an explicit policy reason such as invalidation, persistent addressing/speaker evidence, supported command, interaction completion or higher-priority event. One noisy observation shall not be sufficient.

### C20-R25 — Ambiguous speaker behaviour — MUST

When audio-visual association is ambiguous or unassociated, SPEC-20 shall not bind the utterance to a visible person. It may hold current attention, use a non-person sound bearing, acknowledge generally or request clarification.

### C20-R26 — Attention ownership boundary — MUST

SPEC-20 shall output an authorised target handle/bearing and attention intent. SPEC-13 alone shall allocate that objective across eyes, neck and base.

### C20-R27 — Target loss policy — MUST

On target loss, SPEC-20 may retain attention only within inherited track/fusion freshness and occlusion rules. After invalidation it shall clear or deliberately replace the target; it shall not continue goal-directed locomotion on the last bearing.

### C20-R28 — Entry and departure reactions — MUST

Confirmed presence entry, departure and return events shall be eligible to cause bounded reactions. Repeated detector flicker or duplicate events shall be coalesced/debounced so Makad does not repeatedly greet or mourn one transition.

### C20-R29 — Addressing response — MUST

Strong evidence that a person is addressing Makad shall be able to interrupt voluntary idle and optional performances, establish/strengthen interaction engagement and request attention to the associated target when unambiguous.

### C20-R30 — Attention without locomotion — MUST

Every person/sound attention path shall have a non-locomoting fallback using available face, head and/or audio channels. Base motion is never required merely to acknowledge a person.

## 4.5 Speech, response and action transactions

### C20-R31 — Speech-start acknowledgement routing — MUST

On a valid speech-start event, SPEC-20 shall promptly request at least one available visible listening acknowledgement and update interaction state without waiting for final transcription.

The integrated C5 p95 ≤350 ms requirement remains authoritative.

### C20-R32 — High-priority dispatch instrumentation — MUST

The time from receipt of a valid high-priority event to dispatch of the corresponding semantic response shall be measured per event class.

Initial TARGET for speech-start acknowledgement dispatch is p95 ≤100 ms, subject to the derived end-to-end allocation in §3.12.

### C20-R33 — Partial-transcript firewall — MUST

Provisional speech hypotheses may prepare or animate listening but shall not commit consequential physical actions.

### C20-R34 — Causal turn integrity — MUST

Responses and actions derived from speech shall retain the originating utterance/session ID. Cancellation or supersession of that cause shall invalidate late downstream results.

### C20-R35 — Consequential action lifecycle — MUST

Voice-triggered locomotion and any other configured consequential action shall implement the transaction states in §3.9 with explicit terminal outcome.

### C20-R36 — Pre-action tell — MUST

Before ordinary speech-triggered locomotion commits, SPEC-20 shall request a clear acknowledgement/intent cue and a configurable cancellation interval consistent with C6-R17.

The inherited initial TARGET remains approximately 250–500 ms pending observer testing.

### C20-R37 — Stop/cancel fast path — MUST

Accepted stop, cancel or inhibit intents shall bypass the pre-action wait, cancel affected transactions and request the relevant subsystem stop/inhibit immediately. Low-level safety remains independent and faster where required.

### C20-R38 — Barge-in policy — MUST

Accepted barge-in shall pre-empt or duck non-critical output, inhibit incompatible motion where required, establish listening state and prevent cancelled response units/actions from restarting.

### C20-R39 — Response modality choice — MUST

The executive shall be able to choose among droid audio, face/head response, silent physical response, utility UI and optional TTS without assuming conventional spoken language is always necessary.

### C20-R40 — Core path without generative reasoning — MUST

Wake/address acknowledgement, stop/cancel, supported deterministic intents, basic reactions and local droid responses shall function when LLM/VLM/cloud workers are unavailable.

## 4.6 Performance, idle and affect

### C20-R41 — Performance selection boundary — MUST

SPEC-20 may select a named performance and bounded semantic parameters. SPEC-13 owns timeline authoring, latency compensation, channel composition, execution and settling.

### C20-R42 — Procedural-life continuity — MUST

When awake and not explicitly suppressed, SPEC-12 procedural aliveness shall remain enabled beneath foreground behaviour. Foreground activity may gate channels but shall not replace procedural generation with hand-written pseudo-idle sequences.

### C20-R43 — V1 idle floor — MUST

Makad shall retain a valid awake idle mode using display-only blink and gaze drift with zero neck/base motion. Failure or omission of mechanical idle shall not make idle non-functional.

### C20-R44 — Sleep-safe output — MUST

Sleep shall force procedural base gain to zero, prohibit voluntary roaming/performances unless part of a defined wake transition, and retain required health, wake and low-level safety monitoring.

### C20-R45 — No runtime emotion enum — MUST

No single mutually exclusive `current_emotion` field shall serve as the central behaviour architecture. Affect modulation and performance identity shall remain separately inspectable.

### C20-R46 — Bounded affect influence — MUST

Affect/arousal may influence eligible choices and bounded parameters only. It shall not modify hard limits, confidence validity, action authorization or priority precedence.

### C20-R47 — No duplicate composition engine — MUST

SPEC-20 shall use the shared SPEC-12/13 composition and arousal lineage rather than implement independent per-channel summation, clamping or a second competing arousal integrator.

## 4.7 Locomotion policy

### C20-R48 — Distinct locomotion intents — MUST

Body orientation, approach, retreat, follow, roam and expressive base performance shall be distinct semantic intents with distinct eligibility and cancellation policies.

### C20-R49 — No automatic follow from presence — MUST

Person presence alone shall not authorise approach or sustained following. Follow/approach requires an explicitly eligible supported behaviour or interaction.

### C20-R50 — Fresh target required for social travel — MUST

Goal-directed approach/follow shall require a valid current target and sufficiently fresh geometry for that behaviour. Target invalidation or stale geometry shall cause slow/stop and transaction reevaluation rather than extrapolated indefinite travel.

### C20-R51 — Safety-stream dependency — MUST

Autonomous travel candidates shall be ineligible when authoritative local safety sensing is invalid, except low-level stop/recovery behaviours explicitly owned by SPEC-16.

### C20-R52 — Safety outcome feedback — MUST

SPEC-20 shall consume base accepted/vetoed/stopped/recovering/fault state and shall not repeatedly reissue a blocked goal without a policy transition or materially changed conditions.

### C20-R53 — Listening-motion inhibit — MUST

SPEC-20 shall support assertion/release of the non-safety listening-motion inhibit. While asserted, incompatible base intents shall be withdrawn or denied, while gaze falls back to legal eye/neck behaviour under SPEC-13.

### C20-R54 — Social distance is not collision distance — MUST

Any desired approach/follow range shall be treated as a behaviour/proxemics parameter. It shall not substitute for SPEC-16 safety clearance or camera-independent obstacle sensing.

### C20-R55 — No V1 global-navigation dependency — MUST

Core behaviours shall not depend on SLAM, semantic maps or room-scale path planning. Local roaming, if shipped, shall remain bounded and subordinate to local safety.

## 4.8 Utility and semantic inspection

### C20-R56 — Utility caller registry — MUST

Only explicitly registered utility/semantic callers may invoke capabilities. Each caller shall define input contract, output contract, timeout, cancellation, privacy mode and behaviour on failure.

### C20-R57 — Utility display handoff — MUST

A utility view shall acquire the display through an explicit lease, preserve a safe character/interaction fallback and return cleanly to the face on completion, cancellation, timeout or fault.

### C20-R58 — Slow-worker isolation — MUST

VLM, LLM, network and utility workers shall run asynchronously and shall not block speech acknowledgement, arbitration, cancellation, safety feedback handling or display procedural life.

### C20-R59 — Structured untrusted output — MUST

Generative/remote outputs shall be parsed through a bounded schema and allow-list. Invalid, stale, oversized or unsupported output shall be rejected without partial execution.

### C20-R60 — Thinking is not knowing — MUST

SPEC-20 may trigger an immediate examining/thinking performance while semantic work runs, but shall not present a guessed semantic result as confirmed. Timeout, uncertain and failed outcomes require distinct behaviour.

## 4.9 Fault tolerance and lifecycle

### C20-R61 — Safe startup — MUST

During boot, restart or reconnection, SPEC-20 shall issue no autonomous locomotion until required health, calibration/configuration and authoritative safety readiness are valid. The base independently defaults non-moving.

### C20-R62 — Heartbeat/watchdog compatibility — MUST

SPEC-20 shall publish liveness suitable for subsystem watchdogs. Loss of that liveness shall not leave a stale motion command executing indefinitely.

### C20-R63 — Capability-aware degradation — MUST

Each subsystem capability shall expose available/degraded/unavailable state. Candidates requiring unavailable capabilities shall be rejected or replaced by a declared fallback rather than retried blindly.

### C20-R64 — Recovery handback — MUST

After low-level obstacle recovery, subsystem restart or performance pre-emption, SPEC-20 shall reevaluate from current snapshot and measured execution state. It shall not automatically resume a stale trajectory or command sequence.

### C20-R65 — Fault annunciation without false normality — MUST

When loss of an essential modality materially changes interaction, Makad shall expose a bounded user-visible indication where an available channel permits. It shall not continue behaving as though the failed evidence or actuator exists.

### C20-R66 — Restart-safe transient state — MUST

In-flight leases, pending actions, utterance-derived authorizations and old target commitments shall not silently survive a process restart unless persistence is explicitly designed, integrity-checked and safe. V1 default is to invalidate them.

## 4.10 Observability, replay and privacy

### C20-R67 — Decision journal — MUST

For every behaviour decision, logs shall identify:

- monotonic time;
- snapshot revision;
- triggering event/cause;
- eligible and rejected candidates with reason codes;
- winning intents and resource decisions;
- action/utterance/target handles;
- inhibit and safety feedback;
- execution outcome.

### C20-R68 — Cross-subsystem correlation — MUST

Correlation IDs and timestamps shall allow a visible/audible/physical reaction to be traced back through behaviour dispatch to its originating perception or interaction event.

### C20-R69 — Replayable temporal logic — MUST

Recorded structured inputs shall be replayable through SPEC-20 with deterministic timing semantics. Random selections shall record a seed or selected outcome.

### C20-R70 — Privacy-minimizing logs — MUST

Normal behaviour logs shall not require raw camera frames, raw microphone audio or unrestricted transcript retention. Handles and structured semantic events shall be used where sufficient.

### C20-R71 — Configuration provenance — MUST

Decision logs shall include behaviour/configuration version and relevant threshold set so a test can be reproduced after tuning changes.

### C20-R72 — Latency decomposition — MUST

The integrated system shall measure event time, SPEC-20 receipt time, decision time, dispatch time and observable output onset where available. Aggregate latency alone is insufficient for diagnosis.

## 4.11 Buildability and scope control

### C20-R73 — Data-driven behaviour definitions — TARGET

Priorities, thresholds, timeouts, allow-lists and performance mappings should be configurable and validated from data rather than scattered as code literals.

### C20-R74 — Minimal V1 behaviour repertoire — MUST PROCESS

Before implementation freeze, the team shall declare a finite V1 repertoire covering at least:

- awake idle;
- sleep/wake;
- speech acknowledgement/listening;
- simple supported response;
- person entry/attention;
- target loss/departure;
- stop/cancel;
- one safe attention-oriented body turn;
- one safe approach/follow or an explicit schedule cut;
- obstacle/fault reaction;
- utility-view handoff if any utility ships.

### C20-R75 — Optional-feature cut rule — MUST

VLM-backed behaviour, broad utility work, procedural base aliveness, unrestricted roaming and rich long-context conversation shall be cut before weakening core interruptibility, safety isolation, deterministic paths, observability or integrated acceptance tests.

### C20-R76 — Desktop simulation path — MUST

The behaviour executive shall be runnable against simulated/time-replayed subsystem interfaces so arbitration, action lifecycles and failure cases can be tested before complete robot hardware exists.

### C20-R77 — End-to-end scenario qualification — MUST

Release qualification shall include integrated multi-event scenarios, not only unit tests of individual rules.

---

# 5. Interfaces and dependencies

## 5.1 Minimum input contract

| Producer | SPEC-20 consumes | Important semantics |
|---|---|---|
| SPEC-01 display | availability, face/utility lease state, onset/completion/fault | Display acknowledgement cannot be assumed from command dispatch |
| SPEC-02 neck | availability, measured pose, limits, fault/thermal state | Pose feedback is authoritative |
| SPEC-04/05 audio input | speech start/end, VAD, barge-in, DOA + uncertainty, utterance lifecycle | Capture/effective timestamps required |
| SPEC-06 interpretation | finalized communicative act/action proposal, confidence/ambiguity, cause ID | Partials cannot authorise action |
| SPEC-07 audio output | playback availability, onset, cancellation, completion/fault | Foreground output remains interruptible |
| SPEC-08 camera | camera availability/health | Raw frames are not normal brain input |
| SPEC-09 tracking | candidate tracks, selected/default track, bearings, uncertainty, freshness, loss | Track handle is not identity |
| SPEC-10 semantics | novelty events, processing state, structured semantic result/failure | Asynchronous and optional |
| SPEC-11/fusion lineage | social snapshot, addressing evidence, AV association/ambiguity, presence lifecycle | Snapshot authoritative; association may be `UNASSOCIATED` |
| SPEC-12 | procedural availability/arousal/composition status | SPEC-20 gates/modulates; does not regenerate |
| SPEC-13 | performance/gaze request acceptance, lease status, execution/settle feedback | Owns channel realization |
| SPEC-16 | base readiness, safety validity, accepted/vetoed state, odometry/motion state, recovery/fault/inhibit | Safety feedback is authoritative |
| Utilities/workers | capability, progress, result, uncertainty, timeout/fault | Bounded structured contracts only |

## 5.2 Minimum output contract

| Consumer | SPEC-20 produces | Boundary |
|---|---|---|
| SPEC-01 | character-state/attention cues; utility-view lease request | No pixels or renderer bypass |
| SPEC-06/07 | communicative-act selection, droid/TTS request, cancel/duck | Mixer and synthesis remain downstream |
| SPEC-09/11 | target-selection hints/commitment feedback | No mutation of perception evidence |
| SPEC-10 | bounded semantic-inspection request/cancel | No continuous VLM loop |
| SPEC-12 | enable/gate and bounded affect/stimulus inputs | No scripted idle trajectory |
| SPEC-13 | authorised gaze objective; named performance request; cancel/pre-empt | No per-actuator trajectories |
| SPEC-16 | goal-directed base intent through owned interface; listening inhibit; cancel/stop request | Safety clamp remains final |
| Utility services | typed task request/cancel | No arbitrary tool execution from raw model text |

## 5.3 Required common envelope

Every asynchronous interface used for decisions shall support, where applicable:

```text
message_type
schema_version
source
sequence/revision
event/effective_time_monotonic
receipt_time_monotonic
correlation_id
entity/action/utterance handle
validity/freshness
confidence or uncertainty semantics
payload
```

Absence of a field shall be explicit rather than encoded as a plausible zero.

## 5.4 Safety ownership table

| Decision | Owner |
|---|---|
| Is the person/social event worth attending to? | SPEC-20 |
| Which target is behaviourally committed? | SPEC-20 |
| How eyes/neck/base share gaze? | SPEC-13 |
| Is an authored movement aesthetically/timingly composed? | SPEC-13 |
| Is requested base motion within normal kinematic limits? | SPEC-16 |
| Must base stop for obstacle/cliff/watchdog/tip? | SPEC-16 low-level path |
| May stopped/recovery motion resume as a social goal? | SPEC-20 after fresh reevaluation |
| Does speech meaning propose an action? | SPEC-06 |
| Is that proposal committed now? | SPEC-20 transaction/arbitration |
| May any model directly actuate hardware? | No |

## 5.5 Shared compute dependency

SPEC-20 requires enough high-level compute and memory headroom that:

- event intake and cancellation remain responsive under concurrent vision/audio work;
- slow workers cannot block the executive;
- logs are bounded;
- safety does not depend on that compute remaining responsive.

Exact process/container boundaries and IPC are deferred to system architecture selection.

## 5.6 Power and thermal dependency

SPEC-20 creates simultaneous-load cases, for example:

```text
camera + perception + display animation + droid audio
+ neck slew + base acceleration + network worker
```

The master power/thermal budget must qualify these integrated peaks. SPEC-20 may degrade optional workers or motion for thermal/power reasons, but shall not conceal brownouts as random behaviour failures.

---

# 6. Quantities still requiring CAD / prototype / component validation

The following remain explicit unresolved variables:

| Quantity | Why it matters | How it will be resolved |
|---|---|---|
| Arbitration/event-dispatch p95 and p99 | Closes visible acknowledgement budget | Instrumented desktop and integrated load tests |
| Maximum event/candidate/worker queue sizes | Prevents memory growth while preserving bursts | Stress/replay testing |
| Attention-switch hysteresis and dwell | Prevents gaze flicker without ignoring a new speaker | Two-/three-person observer trials |
| Presence entry/departure debounce | Prevents repeated greetings on detector flicker | Recorded/replayed doorway/occlusion scenarios |
| Lost-target hold duration | Trades continuity against stale fixation | Inherited perception timing + user observation |
| Listening-motion-inhibit engage/release timing | Affects audio quality and body unwind | Acoustic and integrated gaze tests |
| Pre-action cancellation interval | Balances legibility and sluggishness | Initial 250–500 ms TARGET; observer/action tests |
| Social approach/follow range bands | Proxemics, camera geometry and comfort | Physical trials; never used as collision clearance |
| Follow target-loss deceleration policy | Smoothness versus stale travel | SPEC-16 stopping envelope + perception loss tests |
| Local roaming boundary/dwell | Prevents purposeless travel | V1 repertoire decision and safety trials |
| Affect dimensions and decay | Influences character continuity | Simulator/observer evaluation; no mandatory emotion enum |
| Performance-selection repetition suppression | Prevents robotic looping | Long idle/interaction trials |
| Worker timeouts | Prevents LLM/VLM/utility stalls | Measured backend distributions and UX tests |
| Behaviour process CPU/memory budget | Protects audio, tracking and display | Representative compute coexistence profiling |
| Decision-log retention and rate | Debuggability versus storage/privacy | Stress test and privacy review |
| Restart/recovery timing | Determines visible fault behaviour | Target platform measurement |
| Utility repertoire | Prevents scope bloat | Explicit V1 cut decision |
| Whether approach/follow ships in V1 | Capability #19 was closed without its own sheet | Schedule and integrated safety gate |
| Whether a VLM ships | SPEC-10 path exists but caller registry may remain empty | V1 scope gate |

No unresolved value above authorises bypassing an inherited MUST.

---

# 7. Acceptance tests

## 7.1 Requirement-to-test traceability

The tests below intentionally validate groups of coupled requirements rather than creating 77 artificial one-line tests. This matrix is the minimum traceability set; a requirement may also be exercised by additional integrated tests.

| Test | Primary requirements exercised |
|---|---|
| C20-T01 | C20-R01–R04, C20-R47 |
| C20-T02 | C20-R61–R63, C20-R66 |
| C20-T03 | C20-R03, C20-R16, C20-R42–R44 |
| C20-T04 | C20-R13–R18, C20-R46 |
| C20-T05 | C20-R20–R21, C20-R26, C20-R41 |
| C20-T06 | C20-R22, C20-R42–R44 |
| C20-T07 | C20-R07–R10 |
| C20-T08 | C20-R05–R12, C20-R17, C20-R28 |
| C20-T09 | C20-R31–R32, C20-R72 |
| C20-T10 | C20-R33 |
| C20-T11 | C20-R34–R36 |
| C20-T12 | C20-R37 |
| C20-T13 | C20-R34, C20-R38 |
| C20-T14 | C20-R40, C20-R58, C20-R63 |
| C20-T15 | C20-R18, C20-R23–R24, C20-R29 |
| C20-T16 | C20-R10, C20-R25 |
| C20-T17 | C20-R02, C20-R26, C20-R47 |
| C20-T18 | C20-R27, C20-R48, C20-R50 |
| C20-T19 | C20-R30, C20-R49 |
| C20-T20 | C20-R01, C20-R51, C20-R61–R62, C20-R66 |
| C20-T21 | C20-R20, C20-R52, C20-R64 |
| C20-T22 | C20-R21, C20-R30, C20-R53 |
| C20-T23 | C20-R21, C20-R41–R42 |
| C20-T24 | C20-R45–R47 |
| C20-T25 | C20-R39, C20-R56–R57 |
| C20-T26 | C20-R05, C20-R58, C20-R60 |
| C20-T27 | C20-R56, C20-R59 |
| C20-T28 | C20-R63–R65 |
| C20-T29 | C20-R05, C20-R15, C20-R19 |
| C20-T30 | C20-R06–R08, C20-R17, C20-R67–R71 |
| C20-T31 | C20-R11–R12, C20-R70 |
| C20-T32 | C20-R15, C20-R28, C20-R39, C20-R48–R55, C20-R65, C20-R77 |
| C20-T33 | C20-R18, C20-R24, C20-R73–R75 |
| C20-T34 | C20-R19, C20-R32, C20-R58, C20-R72–R77 |

## 7.2 Test procedures

## C20-T01 — Ownership/static architecture audit

Inspect runtime dataflow and representative commands.

**Pass:** every non-safety autonomous act has a SPEC-20 cause/intent; SPEC-20 emits no raw motor PWM, servo angle or renderer pixels; low-level safety remains independently connected.

## C20-T02 — Safe boot and reconnect

Start the high-level process with subsystems appearing in different orders, then restart SPEC-20 while the base controller remains online.

**Pass:** no autonomous motion occurs before readiness; stale leases/actions are invalidated; base stays non-moving; a coherent ready/degraded state is eventually published.

## C20-T03 — Orthogonal concurrency

Run active listening while maintaining a target, blinking and awaiting an asynchronous semantic result.

**Pass:** compatible states coexist without a combinatorial/global-state failure; base inhibit does not unnecessarily suppress face or legal neck behaviour.

## C20-T04 — Priority partial-order matrix

Inject pairwise and multi-way conflicts among idle, optional performance, active response, listening/barge-in, stop/cancel and safety veto.

**Pass:** outcomes obey §3.4 in every case; affect/utility weights never outrank required precedence.

## C20-T05 — Lease conflict and handback

Start a base-owning authored performance, request gaze-distribution body yaw, then pre-empt the performance with barge-in and later release it.

**Pass:** only the permitted owner drives the base at each stage; handback begins from current measured state with no stale catch-up or discontinuity.

## C20-T06 — Suppressed procedural events

Enable procedural base generation while the base is suppressed by a performance, sleep and listening inhibit in separate runs. Release each condition.

**Pass:** suppressed micro-moves do not execute later as a burst; the display-only idle floor remains alive.

## C20-T07 — Authoritative snapshot over stale event

Deliver a delayed `PERSON_ENTERED` event after a newer snapshot shows no valid person.

**Pass:** reevaluation occurs but Makad does not greet, attend or move toward a nonexistent current target.

## C20-T08 — Out-of-order/duplicate event handling

Replay duplicated and reordered speech, entry, departure, target-loss and completion events with sequence/timestamps preserved.

**Pass:** no duplicated action, greeting or terminal transition occurs; current snapshot and IDs determine the result.

## C20-T09 — Speech-start visible acknowledgement

Use synchronized microphone waveform, event logs and video during representative CPU load.

**Pass:** physical speech onset → first visible listening acknowledgement satisfies inherited p95 ≤350 ms across the declared test set; SPEC-20 stage latency is separately reported.

**TARGET:** end-to-end p95 ≤250 ms and SPEC-20 receipt→dispatch p95 ≤100 ms, subject to final allocation.

## C20-T10 — Partial transcript firewall

Feed action-like partials that finalize to a different command, cancel, or no command.

**Pass:** listening animation/preparation may occur, but no consequential action reaches `COMMITTED` from a partial alone.

## C20-T11 — Pre-action transaction and cancellation

Issue a supported voice locomotion command. Observe the tell/pending interval; cancel within it in half the trials and allow commitment in the rest.

**Pass:** each action has one causal ID and legal state sequence; cancellation prevents motion; allowed trials move only after tell/pending and normal safety acceptance.

## C20-T12 — Stop/cancel bypass

Trigger stop during pending, executing and performance states.

**Pass:** stop does not wait through the pre-action interval; affected activities cancel; no late worker/utterance result restarts them.

## C20-T13 — Barge-in under multimodal output

Interrupt Makad while droid/TTS audio and a compatible performance are active.

**Pass:** barge-in enters listening, cancels/ducks output per audio policy, applies needed motion inhibit and leaves no queued response tail or stale action.

## C20-T14 — Core offline behaviour

Disable network, LLM and VLM workers.

**Pass:** awake idle, speech acknowledgement, stop/cancel, declared deterministic intents, basic person reaction and local droid response continue; failures are bounded and visible in health.

## C20-T15 — Two-person attention stability

Present two tracked people. Vary detection confidence slightly, then have the non-target clearly address Makad.

**Pass:** small confidence changes do not cause flicker; persistent unambiguous addressing can cause one deliberate switch; the switch reason is logged.

## C20-T16 — Ambiguous audio-visual association

Provide two plausible visual candidates and an association result marked ambiguous/unassociated.

**Pass:** SPEC-20 does not bind the utterance to either visible track; chosen general/hold/clarify behaviour remains consistent with policy.

## C20-T17 — Attention/gaze ownership boundary

Authorise several targets/bearings while instrumenting outputs.

**Pass:** SPEC-20 selects the objective; SPEC-13 alone produces eye/neck/base distribution; no second target-bearing→base controller exists in SPEC-20.

## C20-T18 — Target loss during follow/approach

During slow authorised social travel, occlude the target briefly, then invalidate it beyond the inherited loss rule.

**Pass:** brief loss behaves according to configured continuity; invalidation causes slow/stop and reevaluation; Makad never travels indefinitely on the last bearing.

## C20-T19 — Presence does not imply following

Introduce a person without a supported follow/approach trigger.

**Pass:** Makad may attend/react but does not begin goal-directed travel solely because a person exists.

## C20-T20 — Safety independence under brain failure

Command motion, then freeze/kill SPEC-20 while separately presenting an obstacle and exercising the command watchdog.

**Pass:** SPEC-16 stops within its own requirements; no high-level tick or response is required; restart does not resume stale motion.

## C20-T21 — Safety veto feedback loop

Request approach while an obstacle repeatedly vetoes motion.

**Pass:** SPEC-20 receives veto/recovery state, does not hammer the same blocked request indefinitely and reevaluates only after a defined state/condition change.

## C20-T22 — Listening-motion inhibit

Have an off-axis person speak while Makad is approaching or body-recentring.

**Pass:** incompatible base intent withdraws/stops; eyes/neck retain attention within limits; safety remains active; release produces SPEC-13’s slew-limited deferred unwind without snap.

## C20-T23 — Performance selection and pre-emption

Trigger an entry reaction, then barge-in, then allow the interaction to end.

**Pass:** SPEC-20 selects only named/valid performances; SPEC-13 executes them; barge-in pre-empts as declared; idle resumes without an abrupt pose reset.

## C20-T24 — No central emotion-state coupling

Inspect schemas/code and vary affect modulators while holding the same explicit action/performance.

**Pass:** no single `current_emotion` drives all subsystems; affect effects remain bounded; action lifecycle and safety decisions remain unchanged.

## C20-T25 — Utility display lifecycle

Start a utility view, then complete, cancel, time out and fault it in separate runs.

**Pass:** the display lease is explicit; each terminal path returns cleanly to the face; no touchscreen is required for core recovery.

## C20-T26 — Slow semantic worker isolation

Hold a VLM/LLM/utility worker indefinitely while generating speech-start, barge-in, stop, target change and idle animation traffic.

**Pass:** urgent behaviour remains responsive; queues remain bounded; the worker times out/cancels without blocking the executive.

## C20-T27 — Untrusted model-output firewall

Return malformed, stale, oversized and actuator-like model outputs.

**Pass:** all are rejected with reason codes; no partial action or resource acquisition occurs.

## C20-T28 — Capability degradation matrix

Individually fault camera, audio input, display, neck, audio output and base, then test representative behaviours.

**Pass:** dependent candidates become ineligible or use declared fallbacks; failed hardware is not repeatedly commanded; Makad does not invent missing evidence.

## C20-T29 — Queue-overload/backpressure

Flood each input with events faster than consumption while injecting stop/cancel and current authoritative snapshots.

**Pass:** memory remains bounded; overload policy is logged; stale/coalescible work is dropped before current critical work; stop/cancel remains serviceable.

## C20-T30 — Deterministic replay

Record a multi-person, speech, novelty, performance, inhibit and fault scenario. Replay structured inputs twice with the same configuration/seed.

**Pass:** decision/action transition sequence is identical except explicitly declared nondeterministic external completion timing; every difference is explainable from logs.

## C20-T31 — Privacy-default behaviour logging

Run normal interaction and inspect logs/storage.

**Pass:** decisions are diagnosable from structured records without default raw camera/audio retention; transcript/semantic retention follows declared policy.

## C20-T32 — End-to-end “one creature” scenario

Run this scripted scenario:

1. Makad idles visibly.
2. A person enters and is noticed.
3. A second person appears.
4. One person addresses Makad.
5. Makad attends and listens without unnecessary base noise.
6. Makad responds with coordinated face/audio/head behaviour.
7. A safe approach or body orientation is requested.
8. An obstacle vetoes motion.
9. The person interrupts/cancels.
10. The person leaves and Makad returns to idle.

**Pass:** no subsystem fights another; priorities and ownership match this spec; uncertainty is not hidden; motion remains safe; action cancellation works; the robot settles coherently rather than exposing disconnected demos.

## C20-T33 — Naïve-observer coherence test — TARGET

Show synchronized video of integrated scenarios to observers unfamiliar with the control architecture and ask them to identify what Makad was attending to and whether its response appeared intentional or contradictory.

**TARGET:** the final observer threshold and sample size shall be frozen before the character-quality gate; results must be reported by scenario rather than as one misleading pooled score.

## C20-T34 — Compute coexistence/endurance

Run the declared mixed-duty scenario for the same representative endurance window used by the integrated robot, including camera tracking, audio, display, periodic performance, utility worker load and locomotion where permitted.

**Pass:** no queue growth, deadlock, stale lease, unbounded latency drift, thermal-triggered unsafe behaviour or unrecovered worker failure occurs. Exact resource ceilings are recorded for component selection.

---

# 8. Internal consistency / design review

## 8.1 “One central system” must not become one blocking process

Logical central authority is required; a monolithic synchronous program is not. Slow perception, networking and generative workers would otherwise stall cancellation and reaction. The spec therefore centralizes decisions while allowing asynchronous workers and independent low-level safety.

## 8.2 Safety cannot be solved with behaviour priority

Assigning “obstacle avoidance = priority 100” inside SPEC-20 would fail if the process hangs. Collision/cliff stop remains a low-level veto. SPEC-20 observes it and decides what to do afterward.

## 8.3 Fixed priority alone would make Makad brittle

A total priority ladder tends to starve idle or causes interaction to oscillate. This spec uses a partial order for non-negotiable precedence, then eligibility, leases, hysteresis and deterministic preference within compatible classes.

## 8.4 One active behaviour is too restrictive

Listening, gaze, blinking and semantic work must coexist. A single global “current behaviour” would suppress normal life or create hundreds of combined states. Orthogonal state and resources are necessary, but the V1 resource set should remain small.

## 8.5 The arbitration system can itself become project bloat

The robot does not need a research-grade planner, reinforcement learner or distributed multi-agent architecture. A typed event/snapshot executive, small candidate registry, explicit resources and deterministic tests are sufficient for V1.

## 8.6 Affect can quietly become the forbidden emotion enum

Renaming `current_emotion` to one categorical “mood” would not solve the problem. Affect must remain bounded modulation; concrete acts remain performances/action transactions.

## 8.7 Audio-visual ownership was genuinely inconsistent

SPEC-09’s earlier stub gave SPEC-20 association ownership. Later SPEC-11/current-state material establishes a dedicated fusion lineage. This spec resolves the mismatch by separating evidence association from behavioural consequence. The master consolidation must patch SPEC-09 rather than leave both statements live.

## 8.8 SPEC-19 being closed leaves a traceability hole

Person-following policy is real even though no standalone SPEC-19 file exists. SPEC-20 now owns authorization/continuation policy and SPEC-16 owns execution/safety. This must be reflected in the eventual master traceability matrix.

## 8.9 A fresh target bearing is not enough to approach safely

Social perception range is not collision range. Even a perfectly tracked face cannot see chair legs or cliffs reliably enough. SPEC-16 safety readiness therefore gates travel independently.

## 8.10 Listening and whole-body orientation are in real tension

The body-mounted array benefits from a quiet stationary base, while natural interaction benefits from facing the speaker. The least-destructive solution is eyes/head during capture and deferred base unwind after inhibit release—not forcing simultaneous rotation.

## 8.11 Hysteresis can preserve the wrong target

Target continuation improves character continuity but must yield to invalidation, clear addressing, stop/fault and interaction end. Its dwell/thresholds remain prototype values, and logs must show why a switch did or did not occur.

## 8.12 “Thinking” animation risks deceptive certainty

An immediate examining state is useful latency masking. It cannot imply that the object has been recognized. Structured processing/success/uncertain/failure outcomes remain distinct.

## 8.13 Replay without raw media has limits

Structured replay validates arbitration, not perception algorithms. Perception owners retain their own privacy-controlled replay methods. SPEC-20 needs only the structured outputs it actually consumed.

## 8.14 Internal p95 values do not add cleanly

The 100 ms arbitration figure is an initial allocation. The authoritative acceptance metric is inherited end-to-end visible/audio timing, measured directly. Percentiles shall not be arithmetically summed as if they were worst-case bounds.

## 8.15 Resume-after-interrupt is a common hidden bug

Blindly resuming the previous sequence after obstacle recovery, barge-in or restart can be unsafe and visually absurd. Every handback reevaluates current state; it is not a stack-pop back to stale intent.

## 8.16 Exact utility tasks remain intentionally unfrozen

Freezing a large assistant catalogue here would inflate integration and cloud dependencies. The caller registry lets useful tasks be added only when each has a real contract and failure path.

## 8.17 V1 breadth must be cut before integration quality

If schedule pressure appears, cut VLM, broad utilities, procedural wheel life, rich roaming and conversation depth. Do not cut stop/cancel integrity, safety isolation, visible acknowledgement, decision logging or integrated scenarios.

## 8.18 The present spec set is not fully canonicalized

Some available files are tracked amendments and SPEC-14/15/17–19 are retired/closed. SPEC-20 is written against the latest current project register plus the requirements actually present. Master consolidation still needs a supersedes/traceability audit; this document does not pretend missing base text was inspected.

---

# 9. Final decisions carried forward

## DECIDED — MUST-HAVE

1. SPEC-20 is Makad’s logically central **high-level intent and arbitration authority**.
2. Low-level safety, watchdogs and bounded recovery remain independent of SPEC-20.
3. SPEC-20 produces semantic intents, never raw actuator commands.
4. Runtime state is orthogonal; there is no giant global state or central `current_emotion` enum.
5. Decisions use versioned authoritative snapshots; events trigger reevaluation but are not truth by themselves.
6. Inputs preserve timestamp, freshness, uncertainty and ambiguity.
7. Behaviour candidates declare validity, resource needs, interruptibility and fallback.
8. Safety/stop/listening precedence cannot be overridden by a tuning score or affect.
9. Compatible behaviours can run concurrently through explicit logical resources.
10. Attention has one primary committed target, with hysteresis and explicit switch reasons.
11. SPEC-20 owns target/engagement choice; SPEC-13 owns eye→neck→base gaze distribution.
12. Evidence-level audio-visual association is assigned to the SPEC-11 fusion lineage; SPEC-20 owns its behavioural consequence.
13. Presence alone does not authorise approach or follow.
14. Follow/approach requires fresh target state, explicit behavioural eligibility and valid SPEC-16 safety readiness.
15. Partial transcripts cannot commit consequential actions.
16. Consequential actions have IDs, pre-action tell/cancellation and explicit terminal outcomes.
17. Stop/cancel/inhibit bypass normal pre-action delay.
18. Core interaction works without LLM, VLM or cloud access.
19. Procedural life remains SPEC-12-owned; authored performances and gaze realization remain SPEC-13-owned.
20. Suppressed procedural base events are discarded rather than queued.
21. The V1 idle floor remains display-only blink + gaze drift with zero mechanical motion.
22. Utility views acquire/release the display explicitly and always return to the face.
23. Slow/untrusted workers are asynchronous, bounded, schema-validated and unable to actuate hardware directly.
24. Faults remove candidate eligibility and cause declared fallbacks; failed capabilities are not imagined.
25. Process restart invalidates transient action authority by default.
26. Decision logging, correlation, deterministic replay and configuration provenance are required.
27. Integrated multi-event scenario testing is required before release.

## TARGET / PROVISIONAL

- SPEC-20 receipt → high-priority semantic dispatch p95 ≤100 ms as an initial allocation.
- Final attention-switch hysteresis/dwell.
- Final entry/departure debounce.
- Final lost-target hold timing.
- Final 250–500 ms pre-action cancellation interval within the inherited range.
- Social approach/follow distance bands.
- Affect dimensions and decay.
- Performance repetition suppression.
- Queue capacities, worker timeouts and compute budgets.
- Naïve-observer coherence threshold.
- Data-driven behaviour configuration.

## EXPLICITLY DEFERRED

- exact behaviour-tree/statechart/rule-engine library;
- exact SBC/MCU and process topology;
- exact middleware/IPC;
- exact LLM, VLM, STT or TTS providers;
- broad utility catalogue;
- persistent person identity or long-term social memory;
- global SLAM/navigation;
- unrestricted autonomous planning;
- final component BOM;
- final affect model;
- whether optional VLM, rich follow, roaming and procedural base life ship in V1.

## CROSS-SPEC PATCHES REQUIRED DURING MASTER CONSOLIDATION

1. Patch SPEC-09’s historical audio-visual-association ownership stub to the SPEC-11-evidence / SPEC-20-consequence split.
2. Add a traceability stub recording that closed SPEC-19 policy is now split between SPEC-20 and SPEC-16.
3. Verify the tracked SPEC-12, SPEC-13 and SPEC-16 amendments against their missing/earlier canonical bases.
4. Close project OQ-16 as authored by this document after review acceptance.
5. Carry the complete sense → decide → act → observe latency and resource budgets into the master engineering specification.

---

# SPEC-20 final design principle

> **Makad’s brain does not animate every motor itself. It maintains a truthful, uncertainty-aware view of the current situation; chooses one coherent set of compatible intentions; gives each specialized subsystem a typed request; observes what actually happened; and yields immediately to interruption, inhibition, failure and low-level safety. That separation is what allows the face, voice, head and wheels to feel like one creature without becoming one unsafe monolith.**
