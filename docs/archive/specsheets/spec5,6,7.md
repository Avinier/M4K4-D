# MAKAD — COMBINED SPECIFICATION 05–07 v1.1
## Real-Time Voice Interaction, Speech Understanding, Response Intelligence & Droid Vocalization

**Status:** Revised engineering specification after design review  
**Subsystem grouping:** Voice Interaction Stack  
**Covers:** SPEC-05 + SPEC-06 + SPEC-07  
**Supersedes:** Combined SPEC-05–07 v1.0

---

# DESIGN INTENT

Makad shall not be designed primarily as a conventional English-speaking voice assistant.

The intended interaction model is:

```text
HUMAN SPEECH
      ↓
Makad understands meaning
      ↓
Makad selects an intent / action / emotion
      ↓
Makad responds through:
    • droid vocalization
    • face
    • head/body movement
    • locomotion where appropriate
    • optional human-language TTS
```

Makad may therefore possess **asymmetric linguistic capability**:

\[
\boxed{
\text{Human natural language}
\rightarrow
\text{Makad semantic representation}
\rightarrow
\text{Makad droid language / behaviour}
}
\]

Makad can understand considerably more linguistic information than it needs to express verbally.

That is intentional.

---

# PRIORITY OF THE THREE CAPABILITIES

## SPEC-05 — MUST-HAVE

### Real-time human speech understanding

Makad must:

- detect intentional speech,
- identify turn boundaries,
- process speech incrementally,
- understand natural paraphrased speech,
- remain interruptible,
- operate while the robot itself produces noise and audio.

---

# SPEC-06 — MUST-HAVE CORE + TARGET CONVERSATIONALITY

### Response interpretation and interaction intelligence

Makad must translate user input and robot context into the correct:

- communicative response,
- physical behaviour request,
- droid vocal response,
- optional spoken-language response.

Traditional unrestricted English conversation is **not required**.

Short contextually consistent droid-style back-and-forth interaction is a:

\[
\boxed{\text{TARGET}}
\]

---

# SPEC-07 — MUST-HAVE VOCAL ENGINE + TARGET DROID LANGUAGE

Makad must possess a controllable expressive electronic voice.

A systematic droid language capable of supporting recognizable recurring meanings is:

\[
\boxed{\text{TARGET}}
\]

The actual vocabulary and creative language design are intentionally deferred.

---

# 1. SCOPE OF THIS SPECIFICATION

This specification covers the processing chain beginning with usable audio from SPEC-04 and ending with communicative output requests to the speaker, display and behaviour systems.

```text
SPEC-04 AUDIO
     │
     ▼
┌─────────────────────────┐
│ SPEECH FRONT END        │
│                         │
│ VAD                     │
│ pre-roll                │
│ interaction gating      │
│ endpoint detection      │
└────────────┬────────────┘
             │
             ▼
       STREAMING STT
             │
       ┌─────┴─────┐
       ▼           ▼
    PARTIAL       FINAL
       │           │
       └─────┬─────┘
             ▼
      INTERACTION ENGINE
             │
      semantic response
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
  DROID     TTS     PHYSICAL
  VOICE             RESPONSE
     │       │        │
     └───────┼────────┘
             ▼
      CHOREOGRAPHER
             │
     ┌───────┼─────────────┐
     ▼       ▼             ▼
   AUDIO    FACE       HEAD/BODY/WHEELS
```

---

## This specification DOES cover

- VAD,
- speech onset detection,
- turn segmentation,
- pre-roll,
- streaming STT,
- transcript lifecycle,
- interruption/barge-in,
- recognition cancellation,
- semantic intent extraction,
- response selection,
- contextual short-term interaction state,
- human-language TTS pathway,
- droid-vocalization rendering,
- vocalization timing,
- audio/motion synchronization,
- voice-engine parameter requirements,
- acoustic interaction with Makad's own speaker and mechanics,
- correctness metrics,
- latency metrics,
- degraded modes.

---

## This specification DOES NOT define

- microphone model,
- microphone-array geometry,
- loudspeaker model,
- amplifier model,
- exact SBC,
- exact STT model/provider,
- exact LLM,
- exact TTS model/provider,
- final Makad vocabulary,
- final droid-language grammar,
- final voice personality,
- locomotion safety implementation,
- final central behaviour architecture.

---

# 2. EXISTING MAKAD DECISIONS THAT CONSTRAIN THIS SPEC

## 2.1 Physical audio belongs to SPEC-04

SPEC-04 owns:

- microphones,
- speaker,
- audio acquisition,
- microphone mounting,
- speaker mounting,
- audio electronics,
- acoustic echo-control front end.

SPEC-05 consumes that audio.

---

## 2.2 Speaker remains in the body

Makad's principal speaker is intended to be located in the torso/body.

The microphones therefore receive:

\[
m(t)=u(t)+h(t)*p(t)+n(t)
\]

where:

- \(u(t)\) = human speech,
- \(p(t)\) = Makad's own playback,
- \(h(t)\) = speaker-to-microphone acoustic path,
- \(n(t)\) = environmental + mechanical noise.

This makes self-audio rejection an architectural requirement.

---

## 2.3 Makad moves while interacting

Voice interaction must remain usable during:

- head holding,
- head tracking,
- expressive head movement,
- body movement,
- eventually wheel motion.

External servo-noise measurements alone are therefore insufficient.

What ultimately matters is:

> **mechanical/acoustic contamination at the actual microphone capsules.**

---

## 2.4 Makad's expressive channels are multimodal

Makad already communicates through:

- eyes,
- head posture,
- movement,
- audio.

Speech onset should therefore immediately influence character behaviour even before the user has been fully understood.

---

## 2.5 Speech shall never directly drive actuators

The prohibited architecture is:

```text
STT
 ↓
motor command
```

The required architecture is:

```text
STT
 ↓
semantic intent
 ↓
behaviour request
 ↓
behaviour / safety arbitration
 ↓
motion subsystem
```

---

## 2.6 Traditional English conversation is no longer a V1 requirement

Makad is not required to answer every sentence using spoken English.

Its normal personality should be capable of responding primarily through:

- droid vocalizations,
- motion,
- expression.

---

## 2.7 Human-language TTS remains supported

Removing English conversation as the personality goal does **not** justify removing TTS capability.

TTS remains useful for:

- exact information,
- debugging,
- demonstrations,
- accessibility,
- selected behaviours.

---

# 3. ENGINEERING REASONING / ARCHITECTURE

# 3.1 The droid pivot changes the latency architecture fundamentally

A conventional voice pipeline often looks like:

```text
speech
 ↓
STT
 ↓
large language model
 ↓
sentence generation
 ↓
TTS
 ↓
audio
```

Two highly variable stages occur after understanding:

- response-language generation,
- speech synthesis.

Makad's normal pathway can instead be:

```text
speech
 ↓
meaning
 ↓
ACKNOWLEDGE / CONFUSED / HAPPY / QUESTION / etc.
 ↓
local vocal recipe
```

Therefore the droid design is not merely an aesthetic choice.

It creates an engineering advantage:

\[
\boxed{
T_{generation}+T_{TTS}
\text{ can disappear from the normal response path}
}
\]

Makad can consequently feel faster without requiring a dramatically faster language model.

---

# 3.2 Makad should react before understanding completes

Three different milestones must exist:

```text
SPEECH DETECTED

UTTERANCE TRANSCRIBED

UTTERANCE UNDERSTOOD
```

They should not be collapsed into one event.

Speech detection can immediately produce:

```text
LISTENING
```

behaviour.

Full transcription may follow hundreds of milliseconds later.

Semantic interpretation comes afterward.

---

# 3.3 Aliveness-critical latency

The visible response to speech is as important as transcript latency.

Makad should not:

```text
human begins speaking
...
robot remains motionless
...
STT finishes
...
Makad suddenly reacts
```

Instead:

```text
human begins speaking
       │
       ├──── fast face response
       │
       ├──── attention/head preparation
       │
       └──── STT continues concurrently
```

---

# 3.4 Continuously listening ≠ continuously running heavyweight STT

Makad shall continuously run only the lightweight front end required for detecting candidate interaction.

```text
continuous audio
      ↓
VAD / interaction gating
      ↓
candidate speech
      ↓
streaming STT session opens
```

This reduces:

- idle compute,
- idle network traffic,
- power,
- privacy exposure,
- unnecessary recognition requests.

---

# 3.5 Pre-roll remains mandatory

VAD identifies speech only after speech starts.

A rolling audio buffer is therefore required.

For 16 kHz 16-bit mono:

\[
M=f_sBt
\]

For:

\[
f_s=16000
\]

\[
B=2\ bytes/sample
\]

\[
t=0.5s
\]

\[
M=16\,kB
\]

Therefore hundreds of milliseconds of pre-roll are essentially negligible in memory terms.

---

# 3.6 Recognition success must no longer be judged primarily by WER

This architecture introduces a critical distinction.

Suppose the user says:

> “Makad, c'mere.”

and STT outputs:

> “Makad come here.”

WER is non-zero.

But the intended action is still perfectly understood.

Conversely:

> “come here”

being transcribed as:

> “come hear”

may have a small textual error but could still confuse a badly designed command system.

Therefore:

\[
\boxed{
\text{END-TO-END INTENT CORRECTNESS}
}
\]

is the primary functional metric.

WER remains useful for diagnosing STT quality.

---

# 3.7 Natural paraphrases matter more than fixed command words

Makad should not require users to memorize exact grammar such as:

```text
MAKAD FORWARD

MAKAD STOP

MAKAD APPROACH
```

It should accept natural variants such as:

```text
come here

come over here

Makad, c'mere

can you come here?

over here, Makad
```

Therefore V1 MUST support **paraphrase robustness**.

Fully unrestricted open-vocabulary recognition remains desirable but is no longer the metric that defines success.

---

# 3.8 Final transcripts remain authoritative

Partial STT hypotheses can change.

Example:

```text
"turn to the..."

"turn to the li..."

"turn to the right"
```

Therefore:

\[
\boxed{
\text{PARTIAL TRANSCRIPT}
\neq
\text{ACTION AUTHORIZATION}
}
\]

Partial results may trigger:

- listening animation,
- speculative response preparation,
- display/debug information.

They shall not initiate consequential physical behaviour.

---

# 3.9 Recognition cancellation is required

Each STT turn needs an explicit lifecycle:

```text
CREATED
  ↓
STREAMING
  ↓
ENDING
  ↓
FINAL
```

or:

```text
STREAMING
  ↓
CANCELLED
```

Cancellation must:

- terminate processing where possible,
- mark all future responses from that session stale,
- flush transient state,
- prevent stale transcript delivery into the next interaction.

Utterance IDs alone are insufficient.

---

# 3.10 Endpointing needs its own budget

The relevant transcription latency is:

\[
T_{final}
=
T_{endpoint}
+
T_{STT-finalization}
+
T_{handoff}
\]

A fast recognizer does not help if endpointing waits excessively.

---

# 3.11 Corrected response-latency budget

For a simple local droid response:

\[
T_{response}
=
T_{endpoint}
+
T_{STT-finalize}
+
T_{speech-handoff}
+
T_{intent}
+
T_{audio-start}
+
T_{integration-margin}
\]

Engineering allocation:

| Stage | MUST budget | TARGET budget |
|---|---:|---:|
| Endpoint after actual speech end | 600 ms | 350 ms |
| STT finalization after endpoint | 300 ms | 250 ms |
| Transcript handoff | 100 ms | 50 ms |
| Simple intent selection | 250 ms | 150 ms |
| Local droid playback start | 100 ms | 50 ms |
| IPC/scheduling/integration margin | 150 ms | 100 ms |
| **TOTAL DESIGN ALLOCATION** | **1500 ms** | **900 ms** |

Therefore:

\[
\boxed{
T_{user-end\rightarrow droid-audio}
\leq1.5s\ MUST
}
\]

and:

\[
\boxed{
\leq1.0s\ TARGET
}
\]

The TARGET budget contains approximately 100 ms of actual design margin rather than requiring every subsystem to hit its individual target perfectly simultaneously.

The component numbers are **engineering allocations**; system p95 must still be measured directly because statistical percentiles do not literally add.

---

# 3.12 Endpointing must be adaptive where useful

A single silence timer creates a trade-off:

```text
short timer
→ fast
→ interrupts hesitant speech

long timer
→ tolerant
→ feels slow
```

Therefore simple VAD endpointing is acceptable initially, but the architecture should permit additional cues such as:

- recognizer endpoint signals,
- recent VAD history,
- linguistic completion,
- interaction state.

---

# 3.13 Droid audio makes the echo problem harder

Makad's primary output may contain:

- whistles,
- chirps,
- narrow tonal components,
- rapid modulation.

AEC must therefore not be validated only with ordinary human-language TTS.

Furthermore Makad may intentionally move its head while vocalizing, changing:

\[
h(t)
\]

the acoustic path between speaker and microphones.

Consequently barge-in validation must include:

```text
droid vocalization
+
head movement
+
human interruption
```

simultaneously.

---

# 3.14 Do not prematurely force every Makad sound to be broadband

It would be a mistake to conclude:

> “Every droid word must contain broadband noise.”

That may unnecessarily destroy the desired character voice.

Instead:

1. the voice engine must be **capable** of adding spectrally diverse components;
2. the echo system must be tested using the intended worst-case tonal vocalizations;
3. a final vocal recipe cannot be accepted if it causes unacceptable self-trigger/barge-in performance.

Thus acoustic constraints influence language design without dictating it prematurely.

---

# 3.15 Mechanical noise must be specified at the microphones

The existing external robot-noise requirement cannot alone guarantee speech quality.

Sound measured 0.5 m from Makad is not equivalent to what:

- a head-mounted microphone,
- physically attached to vibrating structure,

actually receives.

Therefore define:

\[
L_{speech,mic}
\]

as user speech level measured at the microphone signal under nominal interaction geometry.

Define:

\[
L_{self,mic}
\]

as robot mechanical self-noise at the same microphone.

Prototype STT testing shall determine the minimum speech/self-noise margin:

\[
\Delta_{min}
\]

for which the required intent accuracy remains satisfied.

Then the mechanical requirement becomes:

\[
\boxed{
L_{self,mic}
\leq
L_{speech,mic}-\Delta_{min}
}
\]

This derived numerical threshold shall later be handed back to SPEC-02/03.

This is more meaningful than inventing a microphone noise level before the microphone and recognizer exist.

---

# 3.16 Separate response meaning from output rendering

SPEC-06 shall generate an abstract object conceptually similar to:

```text
communicative_act:
    intent: ACKNOWLEDGE
    affect: HAPPY
    intensity: 0.5
    urgency: LOW
    preferred_modality: DROID
```

SPEC-07 renders that meaning.

This decouples:

- intelligence,
- robot behaviour,
- creative voice design.

---

# 3.17 Correctness must be measured at the semantic layer

A labelled speech-intent test corpus shall therefore exist.

Example semantic classes might include:

```text
ATTENTION

ACKNOWLEDGE

AFFIRM

REJECT

APPROACH_REQUEST

STOP_REQUEST

GREETING

CONFUSION

QUESTION

WARNING
```

The final class set may change.

For every class the test corpus must contain multiple natural paraphrases.

---

# 3.18 Confidently wrong recognition needs a repair path

Low confidence is easy:

```text
"I'm not sure"
→ confusion chirp
```

Confidently wrong interpretation is harder.

For consequential physical actions, Makad therefore needs a **pre-action tell**.

Example:

```text
human:
"come here"

Makad:
[acknowledgement chirp]
[turns toward human]
     ↓
short cancellable pending state
     ↓
wheels begin
```

This gives the human:

- legibility,
- an opportunity to interrupt,
- a visible indication of what Makad thinks it is doing.

---

# 3.19 Stop/inhibition commands are exceptions

A command interpreted as:

```text
STOP
```

shall not wait through an acknowledgement delay before stopping.

The repair channel applies primarily to initiating consequential actions, not inhibiting them.

---

# 3.20 Droid vocalizations need perceptual testing

A parameterized synthesizer can produce thousands of sounds.

That does not mean the sounds communicate anything.

Therefore the TARGET droid-language capability is not complete until human listeners can distinguish core recurring meanings at a rate substantially above chance.

---

# 3.21 Voice-engine design should follow perceptual prototyping

Before freezing the embedded vocal-engine parameter set, perform lightweight experiments using:

- DAW software,
- Python audio generation,
- desktop speakers/headphones.

Experiment with:

- pitch,
- contour,
- rhythm,
- duration,
- timbre,
- modulation,
- broadband components.

Then test what listeners actually perceive.

Only afterward freeze which dimensions deserve implementation in Makad's production voice engine.

---

# 3.22 Audio/motion synchronization requires lead compensation

An audio command may become audible in approximately tens of milliseconds.

A servo command may need:

- communication delay,
- internal controller delay,
- acceleration,
- mechanical rise time

before visible motion begins.

Therefore:

```text
send audio command
+
send servo command
simultaneously
```

does not guarantee perceptually simultaneous output.

The choreography system needs output-specific timing compensation.

Conceptually:

```text
t = -Δmotor     motor command
t = 0           intended visible motion onset
t ≈ 0           intended sound onset
```

---

# 3.23 Low-latency audio requires a warm playback path

Opening/closing the operating-system audio device for every chirp is unacceptable.

The playback architecture shall therefore remain:

- persistently initialized,
- appropriately buffered,
- ready for immediate playback.

Power management may idle the amplifier where useful, but wake-up latency must remain inside the audio-start budget.

---

# 3.24 Droid and TTS interruption should not sound identical

Hard-cutting a word in human TTS can sound natural when interrupted.

Hard-cutting a 300 ms electronic chirp halfway through can sound like an audio glitch.

Therefore barge-in policy should distinguish:

### TTS / long vocalization

Cancel/duck aggressively.

### Very short atomic droid unit

The system may finish the current unit if it can complete almost immediately, while preventing subsequent units.

Human listening begins immediately regardless.

### Safety-critical interruption

Cancel immediately.

---

# 4. FORMAL REQUIREMENTS

# SPEC-05 — HUMAN SPEECH PERCEPTION

## C5-R01 — Continuous input audio — MUST

Consume continuous timestamped audio from SPEC-04 whenever interaction is enabled.

---

## C5-R02 — Lightweight continuous speech front end — MUST

Continuous interaction availability shall not require continuous heavyweight STT execution.

---

## C5-R03 — Audio pre-roll — MUST

Maintain at least approximately:

\[
300ms
\]

of preceding audio.

### TARGET

\[
500ms
\]

unless prototype testing supports another value.

---

## C5-R04 — Hands-free normal operation — MUST

Normal voice interaction shall require neither:

- push-to-talk,
- keyboard input,
- manual start recording,
- manual stop recording.

Debug controls are permitted.

---

## C5-R05 — Context-capable interaction gating — MUST

Interaction gating shall be capable of considering additional context such as:

- current engagement state,
- visible person state,
- whether Makad is currently speaking,
- recent interaction history.

A wake word shall not be the only possible interaction mechanism.

---

## C5-R06 — Streaming audio transport — MUST

Audio chunking shall contribute no more than approximately:

\[
100ms
\]

of inherent buffering delay.

### TARGET

Typical:

\[
20-50ms
\]

where practical.

---

## C5-R07 — Streaming recognition — MUST

Recognition shall begin while speech is still being received rather than waiting for a complete recording.

---

## C5-R08 — User speech-start event — MUST

Publish:

```text
USER_SPEECH_STARTED
```

within:

\[
p95\leq250ms
\]

of physical speech onset.

### TARGET

\[
p95\leq150ms
\]

---

## C5-R09 — Visible listening responsiveness — MUST INTERFACE

From physical speech onset until Makad exhibits at least one visible listening acknowledgement:

\[
\boxed{p95\leq350ms}
\]

### TARGET

\[
\boxed{p95\leq250ms}
\]

The response may be produced through the face before the head has physically begun moving.

---

## C5-R10 — Head attention onset — TARGET INTERFACE

Where a listening behaviour includes head movement, visible mechanical motion should begin within approximately:

\[
p95\leq500ms\ MUST\ design\ envelope
\]

with:

\[
p95\leq350ms\ TARGET
\]

from physical human speech onset.

Final ownership is shared with the head/behaviour specifications.

---

## C5-R11 — Partial transcript support — MUST

The streaming recognizer shall expose partial results where supported.

---

## C5-R12 — Transcript lifecycle marking — MUST

Each transcript update shall explicitly identify itself as:

- partial,
- final,
- cancelled,
- failed.

---

## C5-R13 — Final transcript authority — MUST

Partial transcripts shall not directly authorize:

- locomotion,
- consequential physical actions,
- persistent state changes.

Finalized interpretation shall be required unless another subsystem explicitly defines a safe speculative behaviour.

---

## C5-R14 — Natural paraphrase robustness — MUST

Users shall not be required to speak one exact memorized command phrase for each core interaction.

---

## C5-R15 — Open-vocabulary transcription — TARGET

A general open-vocabulary recognizer is preferred where compute/power/network budgets support it.

It shall not be retained as a mandatory architectural cost if a simpler approach can satisfy all Makad paraphrase, intent and expansion requirements during benchmarking.

---

## C5-R16 — Short-utterance handling — MUST

Very short utterances such as functional equivalents of:

```text
yes
no
stop
wait
hello
Makad
```

shall be supported.

---

## C5-R17 — First partial latency — TARGET

For representative utterances long enough to produce meaningful streaming output:

\[
\leq700ms
\]

from speech detection to first useful partial result.

---

## C5-R18 — Endpoint budget — MUST

Under nominal test conditions:

\[
\boxed{
T_{actual\ speech\ end\rightarrow endpoint}
\leq600ms\ p95
}
\]

### TARGET

For clearly completed speech:

\[
\leq350ms\ p95
\]

---

## C5-R19 — Endpoint configuration — MUST

Endpoint/hangover parameters shall remain configurable.

---

## C5-R20 — Multi-cue endpointing — TARGET

The architecture should allow endpoint decisions to combine:

- VAD,
- recognizer signals,
- recent speech timing,
- linguistic completion,
- interaction state.

---

## C5-R21 — STT finalization budget — MUST

After endpoint declaration, final recognition shall become available within:

\[
p95\leq300ms
\]

under nominal conditions.

### TARGET

\[
p95\leq250ms
\]

---

## C5-R22 — Transcript handoff budget — MUST

Final transcript/recognition-result handoff into SPEC-06 shall contribute:

\[
p95\leq100ms
\]

### TARGET

\[
\leq50ms
\]

---

## C5-R23 — Recognition accuracy is language-conditioned — MUST PROCESS

No final WER acceptance number shall be considered frozen until:

- V1 input language(s),
- expected accents,
- interaction geometry,
- test corpus

have been frozen.

---

## C5-R24 — Diagnostic WER — TARGET

Initial engineering target on the frozen nominal corpus:

\[
WER\leq15\%
\]

with:

\[
WER\leq10\%
\]

as a stronger target.

WER is diagnostic rather than the primary end-to-end success metric.

---

## C5-R25 — Short-phrase recognition — TARGET

On the finalized short-phrase test corpus:

\[
\geq90\%
\]

correct transcription/semantic preservation should be achieved.

---

## C5-R26 — Robot self-noise testing — MUST

Recognition shall be characterized with:

- head holding,
- normal head movement,
- expressive head movement,
- display active,
- audio active,
- wheel motion when available.

---

## C5-R27 — Microphone-capsule self-noise requirement — MUST-BE-DERIVED

The final mechanical-noise requirement shall be determined from:

\[
L_{self,mic}
\leq
L_{speech,mic}-\Delta_{min}
\]

where \(\Delta_{min}\) is determined experimentally from the minimum speech/self-noise margin that preserves the required end-to-end intent performance.

This result shall become a constraint on SPEC-02/03.

---

## C5-R28 — Playback rejection — MUST

Makad's own speaker output shall not normally create a new human interaction event.

---

## C5-R29 — Playback-reference input — MUST

The echo-control path shall receive a reference corresponding to the actual digitally mixed output sent toward the speaker.

---

## C5-R30 — Droid-vocal AEC validation — MUST

AEC/barge-in shall be tested not only with TTS but with representative:

- narrow tonal chirps,
- trills,
- whistles,
- broadband/mixed sounds,
- multi-unit sequences.

---

## C5-R31 — Moving-echo-path validation — MUST

Barge-in shall be validated while Makad produces audio and simultaneously performs representative head movement.

---

## C5-R32 — Barge-in — MUST

Genuine human speech during Makad playback shall generate:

```text
USER_BARGE_IN
```

without waiting for final transcription.

---

## C5-R33 — Barge-in latency — MUST

\[
p95\leq250ms
\]

from physical human speech onset during Makad playback to barge-in event.

---

## C5-R34 — Recognition turn cancellation — MUST

An in-flight recognition session shall be explicitly cancellable.

Cancellation shall:

- mark the utterance invalid,
- prevent future late results from being consumed,
- clear transient state,
- allow a clean next turn.

---

## C5-R35 — Utterance identity — MUST

Every recognition turn shall carry a unique ID.

---

## C5-R36 — Language set freeze before backend selection — MUST PROCESS

Final STT selection shall not occur until the intended V1 human-input language/accent requirements have been frozen.

---

## C5-R37 — Backend abstraction — MUST

Makad's behaviour layer shall not be hard-wired to one STT provider/model.

---

## C5-R38 — Compute isolation — MUST

STT shall not stall:

- motor safety,
- face rendering,
- control loops,
- camera operation,
- essential behaviour processing.

---

## C5-R39 — Resource profiling — MUST

Candidate recognition systems shall be measured for:

- CPU,
- accelerator load,
- RAM,
- latency,
- power,
- temperature,
- network use.

---

## C5-R40 — Remote-failure handling — MUST-IF-REMOTE

Remote recognition failure shall produce a deterministic error rather than indefinite listening.

---

## C5-R41 — Encrypted transport — MUST-IF-REMOTE

If raw or processed user audio leaves Makad, transport shall use an encrypted channel appropriate to the chosen service/protocol.

Provider-side retention shall be reviewed before selection.

---

## C5-R42 — Recognition uncertainty — MUST

Low-confidence/ambiguous recognition shall be exposed to SPEC-06 rather than converted into invented certainty.

---

## C5-R43 — Transient audio retention — MUST

Normal always-listening operation shall not imply permanent continuous audio recording.

---

## C5-R44 — Multi-speaker diarization — STRETCH

Speaker identification/diarization is not required for V1.

---

## C5-R45 — Simultaneous human speakers — STRETCH

Reliable transcription of two people talking simultaneously is not required for V1.

---

## C5-R46 — Automatic multilingual/code-switch speech — STRETCH

Code-switching/multilingual recognition is not a mandatory feature unless explicitly brought into the frozen V1 language scope.

---

# SPEC-06 — INTERACTION INTERPRETATION & RESPONSE SELECTION

## C6-R01 — Finalized recognition input — MUST

SPEC-06 shall consume finalized recognition/semantic results and associated metadata.

---

## C6-R02 — Context availability — MUST

Response selection shall be capable of considering:

- recent interaction,
- current behaviour,
- speaking/listening state,
- perception state,
- relevant motion state.

---

## C6-R03 — Communicative-act abstraction — MUST

Response semantics shall be represented independently of audio assets.

---

## C6-R04 — Minimum semantic repertoire — MUST

The architecture shall support functional classes equivalent to:

- acknowledgement,
- affirmation,
- rejection,
- confusion,
- greeting,
- question/curiosity,
- excitement,
- warning,
- completion,
- failure.

The final vocabulary is not yet fixed.

---

## C6-R05 — Semantic/rendering separation — MUST

Changing Makad's voice or language shall not require rewriting speech understanding or core motion logic.

---

## C6-R06 — Deterministic fast path — MUST

Common low-complexity interaction classes shall be processable without invoking a heavyweight generative model.

---

## C6-R07 — Simple intent-selection latency — MUST

\[
p95\leq250ms
\]

after finalized recognition arrives.

### TARGET

\[
p95\leq150ms
\]

---

## C6-R08 — End-to-end simple response latency — MUST

From actual end of user speech to first audible local droid response:

\[
\boxed{p95\leq1.5s}
\]

### TARGET

\[
\boxed{p95\leq1.0s}
\]

---

## C6-R09 — Intent test corpus — MUST

A labelled interaction corpus shall be created containing:

- multiple semantic classes,
- multiple natural paraphrases,
- multiple speakers,
- negative/out-of-domain speech,
- ambiguous cases.

Training/development examples shall be separated from final held-out acceptance examples where learned models are involved.

---

## C6-R10 — End-to-end intent correctness — MUST

On the frozen nominal held-out test corpus:

\[
\boxed{
Macro\ F1\geq0.90
}
\]

for core supported interaction intents.

### TARGET

\[
\boxed{
Macro\ F1\geq0.95
}
\]

This metric includes errors arising anywhere in:

```text
audio
→ STT
→ interpretation
```

and therefore predicts real interaction quality better than WER alone.

---

## C6-R11 — Intent confusion reporting — MUST

Acceptance testing shall produce a confusion matrix.

Overall accuracy alone is insufficient.

---

## C6-R12 — Action-intent precision — MUST

For intents that initiate consequential physical motion:

\[
\boxed{
precision\geq95\%
}
\]

on the nominal held-out corpus.

### TARGET

\[
\boxed{
precision\geq98\%
}
\]

If this cannot be achieved, the response policy shall require clarification/confirmation rather than automatic action.

---

## C6-R13 — Out-of-domain false-action rejection — MUST

A dedicated negative corpus shall contain speech that should **not** initiate robot motion.

False physical-action initiation shall remain sufficiently low to pass the behaviour safety review.

### Initial quantitative TARGET

No more than:

\[
2/100
\]

negative test utterances may incorrectly produce a consequential action request.

Final threshold may be tightened after prototype results.

---

## C6-R14 — Partial transcripts cannot authorize actions — MUST

SPEC-06 shall reject consequential action requests derived exclusively from provisional transcript hypotheses.

---

## C6-R15 — Low-confidence ambiguity response — MUST

Uncertain interpretation shall produce a safe response such as:

- confusion,
- request for repetition,
- no-action state.

---

## C6-R16 — Confidently-wrong repair channel — MUST

Speech-initiated consequential actions shall support a human-readable pending/repair state before irreversible commitment.

---

## C6-R17 — Pre-action tell for locomotion — MUST

Before a normal voice-initiated locomotion action begins, Makad shall provide an acknowledgement/intent cue through one or more of:

- face,
- head,
- droid vocalization.

A short configurable cancellation interval shall exist.

### Initial TARGET

Approximately:

\[
250-500ms
\]

with final timing set by user testing.

---

## C6-R18 — Stop/inhibition exception — MUST

Commands interpreted as:

- stop,
- cancel,
- inhibit

shall not wait through the normal pre-action delay before taking effect.

---

## C6-R19 — Action cancellation — MUST

During the pending pre-action state, barge-in/cancel input shall be capable of preventing action commitment.

---

## C6-R20 — Safety arbitration — MUST

Voice understanding shall never override:

- collision constraints,
- wheel safety,
- joint limits,
- emergency stop,
- system inhibition.

---

## C6-R21 — Traditional open-ended spoken conversation — NOT MUST

Makad V1 is not required to behave as an unrestricted English conversational agent.

---

## C6-R22 — Short contextual droid conversation — TARGET

Makad should maintain sufficient short-term context to produce coherent short back-and-forth droid-style interactions.

---

## C6-R23 — Short-term context lifecycle — TARGET

Interaction context should survive nearby conversational turns but expire/reset under defined disengagement conditions.

---

## C6-R24 — Context reset — MUST

Context shall not remain indefinitely stale.

---

## C6-R25 — LLM independence — MUST

Core voice interaction shall continue functioning when optional generative reasoning is unavailable.

---

## C6-R26 — Generative reasoning — TARGET

A language model may enrich ambiguous/open-ended interactions where the latency/resource cost is justified.

---

## C6-R27 — TTS pathway — MUST

Makad shall retain the engineering ability to convert generated text into human-language speech.

---

## C6-R28 — Streaming TTS — TARGET

Where supported, long human-language replies should begin output before the entire response waveform has been generated.

---

## C6-R29 — TTS first-audio latency — TARGET

After response text becomes available:

\[
p95\leq800ms
\]

to first audible speech.

Stronger target:

\[
\leq500ms
\]

where practical.

---

## C6-R30 — TTS interruptibility — MUST

Human-language speech output shall be cancellable by an accepted barge-in.

---

## C6-R31 — Droid response as first-class modality — MUST

Droid vocalization shall not be treated as a decorative secondary sound effect.

---

## C6-R32 — Silent physical response — MUST

The behaviour system may deliberately answer using only:

- eyes,
- head,
- body,
- locomotion.

Audio shall not be mandatory for every turn.

---

## C6-R33 — Multimodal response composition — TARGET

One communicative act should be able to coordinate:

```text
voice
+
face
+
head
+
body
```

as a single performance.

---

## C6-R34 — Interpretation failure response — MUST

Higher-level reasoning failure shall produce a defined local fallback rather than freezing the robot.

---

# SPEC-07 — DROID VOCALIZATION ENGINE

## C7-R01 — Independent droid audio modality — MUST

Makad shall possess a vocalization path independent from human-language TTS.

---

## C7-R02 — Local core voice — MUST

Core vocal responses shall function without:

- cloud connectivity,
- remote TTS,
- LLM access.

---

## C7-R03 — Prototype-before-freeze — MUST PROCESS

The final droid voice-engine parameter set shall not be frozen before desktop perceptual experiments are performed.

---

## C7-R04 — Minimum controllable dimensions — MUST

The prototype/production architecture shall at minimum permit control of:

- duration,
- level/amplitude,
- temporal sequencing,
- pitch or source-frequency behaviour.

---

## C7-R05 — Extended dimensions — PROTOTYPE-GATED TARGET

Candidate dimensions include:

- pitch contour,
- modulation rate,
- modulation depth,
- timbre/filtering,
- attack/decay,
- tonal/noise ratio,
- rhythm,
- inter-token gap.

Only dimensions shown to create useful perceptual or acoustic value need be carried into the final embedded engine.

---

## C7-R06 — Hybrid architecture — TARGET

Preferred architecture:

\[
\text{reusable primitives}
+
\text{procedural modification}
+
\text{sequencing}
\]

unless experimentation demonstrates a simpler architecture is sufficient.

---

## C7-R07 — Multi-unit utterances — MUST

A Makad vocal response may contain multiple timed sound units.

---

## C7-R08 — Data-driven recipes — MUST

Communicative meanings shall map to configurable sound recipes rather than scattered hard-coded audio logic.

---

## C7-R09 — Creative replaceability — MUST

The final Makad vocabulary shall be replaceable without modifying:

- STT,
- intent logic,
- motor control.

---

## C7-R10 — Controlled variation — MUST

Multiple variants of one communicative category shall be possible.

---

## C7-R11 — Bounded variation — MUST

Procedural variation shall remain inside limits preventing:

- excessive loudness,
- excessive duration,
- unusable frequencies,
- clipping,
- loss of recognizable identity.

---

## C7-R12 — Spectral-diversity capability — MUST

The vocal engine shall be capable of including controlled spectrally diverse/broadband components in addition to tonal components when required by:

- character design,
- AEC stability,
- barge-in performance.

This does **not** require every Makad vocalization to be broadband.

---

## C7-R13 — Recipe acoustic qualification — MUST-BEFORE-LANGUAGE-FREEZE

No final recurring Makad vocal token shall be approved if it creates unacceptable:

- self-triggering,
- AEC degradation,
- barge-in failure

under the defined integrated audio test.

---

## C7-R14 — Low-latency local audio path — MUST

For already available local droid output:

\[
p95\leq100ms
\]

from software vocalization command to audible playback onset.

### TARGET

\[
p95\leq50ms
\]

---

## C7-R15 — Persistently initialized playback — MUST

Normal droid playback shall not repeatedly incur cold audio-device initialization.

The playback device/path shall remain ready for low-latency output.

---

## C7-R16 — Buffer configuration — MUST

Audio buffering shall be configured so the C7-R14 latency requirement remains achievable without unacceptable underruns.

Exact platform/backend remains unfrozen.

---

## C7-R17 — Amplifier wake behaviour — MUST INTERFACE

Any amplifier power-saving mode shall either:

- maintain wake-up time inside C7-R14,
- or be pre-woken before scheduled vocal output.

---

## C7-R18 — Playback cancellation — MUST

Long droid sequences shall be cancellable.

---

## C7-R19 — Unit-aware barge-in — TARGET

If interruption occurs during a very short atomic droid sound whose remaining duration is negligible, the system may finish the current unit while preventing subsequent units.

Long sequences and TTS should be cancelled/ducked immediately.

Safety-critical interruption shall always pre-empt immediately.

---

## C7-R20 — Cancellation fade — TARGET

Where immediate truncation would sound like an audio fault, cancellation may apply a very short controlled fade while remaining inside the behaviour interruption budget.

---

## C7-R21 — Audio mixer — MUST

The system shall centrally manage at least:

- droid voice,
- TTS,
- required system audio.

---

## C7-R22 — Priority/pre-emption — MUST

The mixer shall support defined priority relationships.

Listening/barge-in has priority over non-critical output.

---

## C7-R23 — Digital headroom — MUST

Layered vocal synthesis shall not cause uncontrolled digital clipping.

---

## C7-R24 — Speaker-aware synthesis — MUST

Final recipes shall remain within frequency regions that the actual speaker/enclosure can reproduce usefully.

Exact limits remain pending measurement.

---

## C7-R25 — Playback reference fidelity — MUST

AEC shall receive the actual post-mix digital playback reference.

---

## C7-R26 — Shared timing model — MUST

Audio, face and motion choreography shall operate within a common timestamp/scheduling system.

---

## C7-R27 — Scheduled choreography — MUST

The system shall support scheduling output events at intended presentation times rather than merely issuing simultaneous commands.

---

## C7-R28 — Per-output latency compensation — MUST

Known delays between:

- command dispatch,
- audio onset,
- face-frame update,
- servo visible motion

shall be measurable and compensable.

---

## C7-R29 — Cross-modal onset alignment — MUST

For deliberately synchronized behaviours:

\[
\leq100ms
\]

relative perceived onset mismatch.

### TARGET

\[
\leq50ms
\]

---

## C7-R30 — Mid-vocalization cues — TARGET

Longer vocal sequences should expose internal event points for choreography.

---

## C7-R31 — Local fallback vocabulary — MUST

At minimum locally available vocal responses shall cover functional equivalents of:

- acknowledgement,
- uncertainty/failure,
- warning/attention.

---

## C7-R32 — Semantic consistency support — TARGET

The software shall support recurring sound motifs maintaining recurring meanings.

---

## C7-R33 — Droid conversation sequencing — TARGET

Makad shall be capable of constructing multi-token responses from recurring vocal elements.

---

## C7-R34 — Naïve-listener comprehensibility gate — MUST-BEFORE-TARGET-LANGUAGE-COMPLETE

Before claiming the droid-language TARGET is achieved, a set of approximately 6–8 core communicative meanings shall be tested with listeners who were not involved in designing the sounds.

Listeners shall hear the sounds without behavioural context and select the intended meaning from the defined choices.

Initial acceptance target:

\[
\boxed{\geq70\%\ overall}
\]

with no core class below approximately:

\[
\boxed{50\%}
\]

correct identification.

### Strong TARGET

\[
\geq80\%
\]

overall.

A confusion matrix shall be recorded.

These numbers may be revisited after the first perceptual experiment, but the requirement that the language be empirically distinguishable shall remain.

---

## C7-R35 — Contextual legibility test — TARGET

The final language shall also be tested together with:

- face,
- head,
- interaction context.

Contextual performance should exceed isolated-audio performance rather than contradict it.

---

## C7-R36 — Final vocabulary design — DEFERRED

This specification does not yet define:

- Makad “yes,”
- Makad “no,”
- greeting token,
- question form,
- phonetic inventory,
- signature motifs,
- grammar,
- language personality.

---

# 5. INTERFACES AND DEPENDENCIES

# SPEC-04 → SPEC-05

Required:

```text
timestamped microphone audio
audio health
AEC/echo-controlled stream
playback reference integration
```

---

# SPEC-05 → SPEC-06

Required events/data:

```text
USER_SPEECH_STARTED
USER_SPEECH_ENDED
PARTIAL_TRANSCRIPT
FINAL_TRANSCRIPT
UTTERANCE_CANCELLED
STT_FAILURE
USER_BARGE_IN
confidence/status metadata
```

---

# SPEC-06 → CENTRAL BEHAVIOUR

Possible outputs:

```text
COMMUNICATIVE_ACT

ACTION_PENDING

ACTION_REQUEST

ACTION_CANCEL

NO_ACTION

FAILURE_RESPONSE
```

---

# SPEC-06 → SPEC-07

Example:

```text
intent = CONFUSED
affect = CURIOUS
intensity = 0.4
preferred_modality = DROID
```

---

# SPEC-07 → SPEC-04

Required:

```text
post-mix playback reference
requested output level
playback state
```

---

# SPEC-07 → FACE/HEAD/BODY

Required only as choreography events/timestamps.

SPEC-07 shall not command servo positions itself.

---

# SPEC-02/03 → SPEC-05

Mechanical prototype testing must eventually provide:

- microphone-capsule self-noise,
- vibration-induced audio contamination,
- motion-state timing.

The derived microphone noise requirement must then be reflected back into mechanical acceptance criteria.

---

# CENTRAL BEHAVIOUR → SPEC-06/07

The behaviour layer controls:

- whether a vocal response is appropriate,
- whether an action is safe,
- whether a pending action commits,
- audio pre-emption,
- cancellation.

---

# 6. QUANTITIES REQUIRING PROTOTYPE / COMPONENT VALIDATION

## Speech front end

- VAD implementation,
- interaction-gating strategy,
- exact pre-roll,
- chunk size.

---

## Endpointing

Need empirical curve:

\[
T_{endpoint}
\quad vs \quad
P_{false-split}
\]

before freeze.

---

## Supported human input languages

Must be explicitly frozen before STT backend selection.

---

## STT backend

Still open:

- local,
- cloud,
- hybrid,
- exact model/provider.

---

## WER

Current 15% figure is a provisional engineering target only.

Target accent/language corpus must be measured first.

---

## End-to-end intent performance

Requires a Makad-specific labelled test set.

This should be created **before hardware completion**.

---

## Mechanical self-noise

Need actual:

\[
L_{speech,mic}
\]

\[
L_{self,mic}
\]

and SNR degradation testing.

---

## AEC

Need characterization across:

- TTS,
- tonal chirp,
- trill,
- broadband/mixed droid output,
- moving head.

---

## Droid voice dimensions

Pitch/modulation/filter/rhythm parameters are not yet frozen.

They must first undergo laptop perceptual prototyping.

---

## Audio latency

Need actual OS/audio-backend measurement.

---

## Servo timing

Need empirical:

```text
servo command timestamp
→
first visible movement
```

for each major actuator class.

---

## Choreography compensation

Per-output delay values remain pending real hardware.

---

## Pre-action cancellation window

Initial exploration:

\[
250-500ms
\]

Final choice requires interaction testing.

---

# 7. ACCEPTANCE TESTS

# SPEC-05 TESTS

## C5-T01 — Speech-start event latency

At least 50 trials.

### PASS

\[
p95\leq250ms
\]

---

## C5-T02 — Visible listening latency

Use synchronized microphone waveform + video/software logs.

Measure:

```text
physical speech onset
→
first visible Makad acknowledgement
```

### PASS

\[
p95\leq350ms
\]

### TARGET

\[
p95\leq250ms
\]

---

## C5-T03 — Head-attention timing

For behaviours requiring head response, measure physical motion onset.

Record separately from face response.

---

## C5-T04 — Pre-roll retention

Test words with abrupt initial phonemes.

### PASS

No systematic beginning truncation.

---

## C5-T05 — Streaming partial recognition

Verify meaningful partial output before utterance completion on sufficiently long test speech.

---

## C5-T06 — Endpoint trade-off sweep

Test natural sentences containing internal pauses approximately around:

- 200 ms,
- 400 ms,
- 600 ms,
- 800 ms,
- 1000 ms.

Plot:

\[
false\ splits
\]

against:

\[
endpoint\ latency
\]

before freezing endpoint parameters.

---

## C5-T07 — STT finalization timing

Measure:

```text
endpoint declared
→
final recognition available
```

### PASS

\[
p95\leq300ms
\]

---

## C5-T08 — Frozen-language corpus WER

Once language/accent requirements exist, compute WER.

Use primarily as diagnostics and backend comparison.

---

## C5-T09 — Short-phrase test

Evaluate future core short-interaction phrases across multiple speakers.

---

## C5-T10 — Mechanical self-noise test

Measure audio directly at Makad's microphone input while:

1. stationary,
2. head holding,
3. normal head movement,
4. expressive head movement,
5. wheels active when available.

Measure:

- level/spectrum,
- STT degradation,
- intent degradation.

Use results to derive:

\[
\Delta_{min}
\]

and the final SPEC-02/03 noise constraint.

---

## C5-T11 — Self-playback false-trigger test

Run representative Makad audio with no human speech.

Test:

- tonal chirps,
- whistles,
- trills,
- broadband/mixed recipes,
- TTS.

No feedback loop is permitted.

---

## C5-T12 — Stationary barge-in test

At least 20 human interruptions during robot playback.

### PASS

At least:

\[
18/20
\]

correctly detected.

---

## C5-T13 — Moving-head barge-in test

Repeat barge-in testing while Makad performs representative head motion.

This test is mandatory before full-duplex interaction is considered complete.

---

## C5-T14 — Turn-cancellation test

Start recognition.

Cancel it before finalization.

Artificially allow the backend to later return a transcript.

### PASS

The stale transcript is discarded and cannot affect the following turn.

---

## C5-T15 — Rapid turn-isolation test

Use:

```text
utterance A
short pause
utterance B
```

while injecting processing delays.

### PASS

No cross-turn contamination.

---

## C5-T16 — Network failure test — IF REMOTE

Interrupt network during a recognition turn.

### PASS

Makad enters defined degraded behaviour rather than hanging.

---

## C5-T17 — Resource-contention test

Simultaneously run:

- STT,
- camera,
- face animation,
- head motion,
- audio.

Check:

- timing,
- memory,
- temperature,
- frame loss,
- control starvation.

---

# SPEC-06 TESTS

## C6-T01 — Intent corpus construction

Create labelled natural-language/paraphrase corpus for each supported semantic class.

Include negative examples.

---

## C6-T02 — Held-out intent evaluation

Evaluate complete:

```text
microphone audio
→
final Makad intent
```

pipeline.

### PASS

\[
Macro\ F1\geq0.90
\]

### TARGET

\[
\geq0.95
\]

---

## C6-T03 — Confusion matrix review

Inspect which classes are mistaken for one another.

Any high-risk confusion must be explicitly resolved before acceptance.

---

## C6-T04 — Consequential-action precision

Evaluate action-triggering intents.

### PASS

\[
precision\geq95\%
\]

### TARGET

\[
\geq98\%
\]

---

## C6-T05 — Negative speech test

Use at least approximately 100 phrases that should not initiate consequential movement.

Record false action requests.

---

## C6-T06 — Natural paraphrase test

For each important intent test multiple formulations such as:

```text
come here
come over here
over here
can you come here
Makad, c'mere
```

The test is failed if success depends on memorizing one exact command form.

---

## C6-T07 — Simple response latency

Measure:

```text
final recognition
→
communicative act
```

### PASS

\[
p95\leq250ms
\]

---

## C6-T08 — Full simple interaction latency

Measure:

```text
actual human speech end
→
first audible local Makad reply
```

### PASS

\[
p95\leq1.5s
\]

### TARGET

\[
p95\leq1.0s
\]

---

## C6-T09 — Low-confidence repair test

Provide intentionally degraded/ambiguous audio.

### PASS

No unsafe arbitrary action occurs.

---

## C6-T10 — Confidently-wrong repair test

Inject an intentionally incorrect but high-confidence semantic result for a locomotion command.

Verify:

```text
ACTION_PENDING
→
acknowledgement cue
→
cancellation window
```

exists before motion commitment.

---

## C6-T11 — Pre-action cancellation

During the pending interval, say:

> “stop”

or trigger another accepted cancel input.

### PASS

Locomotion does not begin.

---

## C6-T12 — Stop-priority test

While moving or pending movement, issue the configured stop interaction.

### PASS

No acknowledgement delay prevents timely inhibition.

---

## C6-T13 — No-LLM fallback

Disable optional generative reasoning.

### PASS

Makad retains:

- basic speech understanding,
- supported intent recognition,
- droid responses,
- safety behaviour.

---

## C6-T14 — Short contextual interaction — TARGET

Test several scripted but naturally phrased short back-and-forth interactions.

Makad should preserve immediate conversational context.

---

## C6-T15 — Context-expiry test

Allow the session to expire/disengage.

### PASS

Old conversational state no longer contaminates the next interaction.

---

## C6-T16 — TTS capability

Send arbitrary test text.

### PASS

Human-language speech can be produced.

---

## C6-T17 — TTS barge-in

Interrupt Makad while it speaks.

### PASS

TTS stops/ducks according to barge-in policy.

---

# SPEC-07 TESTS

## C7-T01 — Desktop expressive-dimension experiment

Before final engine implementation, generate candidate sounds while varying:

- pitch,
- contour,
- modulation,
- rhythm,
- duration,
- timbre,
- noise mixture.

Document which dimensions materially affect human perception.

This test is a **design input**, not final language creation.

---

## C7-T02 — Parameter-set reduction review

After C7-T01, remove synthesis dimensions that add substantial complexity without measurable expressive value.

The embedded engine shall not be more complex than necessary.

---

## C7-T03 — Local playback latency

At least 100 trials.

Measure:

```text
vocal command
→
actual audio onset
```

### PASS

\[
p95\leq100ms
\]

### TARGET

\[
p95\leq50ms
\]

---

## C7-T04 — Cold/warm audio test

Verify that normal playback does not unexpectedly incur device-startup latency.

Test amplifier wake mode separately if used.

---

## C7-T05 — Buffer-underrun stress test

Play representative rapid and layered sound sequences while the rest of the robot compute stack operates.

### PASS

No audible underruns/glitches during the defined stress trial.

---

## C7-T06 — Parameter bounds test

Sweep all allowed production parameter extremes.

### PASS

No:

- clipping,
- invalid frequency output,
- runaway duration,
- crash.

---

## C7-T07 — Multi-unit sequence

Render a multi-element response with timed gaps.

Verify ordering and timing.

---

## C7-T08 — Variation test

Trigger one semantic response repeatedly.

### PASS

Multiple recognizable variants can be generated.

---

## C7-T09 — Spectral/AEC compatibility test

For candidate recurring vocal recipes, measure:

- self-trigger rate,
- barge-in accuracy,
- echo residual behaviour

for tonal and mixed-spectrum variants.

No recurring language token may be frozen before passing integrated audio qualification.

---

## C7-T10 — Hard cancellation

Cancel:

- long droid sequence,
- TTS,
- non-critical audio.

Verify playback terminates reliably.

---

## C7-T11 — Unit-aware interruption

Interrupt during:

1. short atomic chirp,
2. long trill,
3. multi-unit phrase.

Verify the policy avoids unnecessary glitch-like truncation while still giving listening priority.

---

## C7-T12 — Playback-reference test

Compare the reference provided to AEC against actual mixer output.

---

## C7-T13 — Audio/motion synchronization calibration

For each relevant output channel measure:

```text
command
→
physical/perceptual onset
```

including:

- audio,
- display change,
- head motion.

Store resulting latency offsets.

---

## C7-T14 — Lead-compensated choreography

Create a test behaviour where sound and visible motion should begin together.

Commands shall be scheduled with measured compensation.

### PASS

\[
\leq100ms
\]

perceived/recorded onset mismatch.

### TARGET

\[
\leq50ms
\]

---

## C7-T15 — Naïve-listener core-meaning test — FUTURE LANGUAGE PHASE

After candidate Makad vocabulary exists:

1. recruit listeners who did not design it;
2. play isolated vocalizations;
3. provide the intended 6–8 meaning choices;
4. collect classifications.

### Initial PASS criterion

\[
\geq70\%
\]

overall.

No core class should fall below approximately:

\[
50\%
\]

### TARGET

\[
\geq80\%
\]

overall.

Record confusion matrix.

---

## C7-T16 — Contextual comprehension test — TARGET

Repeat language-recognition testing with:

- face expression,
- head movement,
- realistic interaction context.

Context should improve interpretation and must not systematically imply a meaning opposite to the vocalization.

---

## C7-T17 — Offline fallback

Disconnect external services.

### PASS

Core locally stored/generated droid reactions remain functional.

---

# 8. INTERNAL CONSISTENCY / DESIGN REVIEW

# Review 1 — The previous merge dropped safety-critical speech lifecycle requirements

Corrected.

Restored explicitly:

- hands-free operation,
- context-aware interaction gating,
- final-transcript authority,
- STT turn cancellation,
- language freeze before backend selection,
- remote encryption.

Also restored explicit exclusions for:

- diarization,
- overlapping speakers,
- multilingual/code-switch behaviour.

---

# Review 2 — Partial transcripts became more dangerous after SPEC-06 gained action capability

Correct.

The pipeline now has an explicit rule:

\[
\boxed{
\text{partial transcript}
\not\rightarrow
\text{consequential action}
}
\]

---

# Review 3 — Utterance IDs do not replace cancellation

Correct.

IDs identify stale results.

Cancellation prevents them from remaining semantically active.

Both are required.

---

# Review 4 — AEC is both more important AND more difficult after the droid pivot

Correct.

It must now cope with:

- frequent robot vocalization,
- tonal sounds,
- changing acoustic path,
- simultaneous head movement,
- barge-in during playback.

This is now reflected in mandatory integrated tests.

---

# Review 5 — We should not prematurely dictate the creative spectrum

Also correct.

Rather than mandate that all Makad speech contain noise/broadband energy, the engine is required to:

- support spectral diversity,
- expose it to sound designers,
- qualify each important recurring sound against AEC/barge-in tests.

That preserves creative freedom.

---

# Review 6 — WER alone measures the wrong thing

Corrected.

Primary acceptance metric is now:

\[
\boxed{
\text{END-TO-END INTENT MACRO-F1}
}
\]

WER remains a diagnostic metric.

---

# Review 7 — SPEC-06 previously had speed requirements but no correctness requirements

Corrected.

Added:

- labelled corpus,
- held-out evaluation,
- Macro F1,
- confusion matrix,
- action precision,
- negative/out-of-domain test.

---

# Review 8 — SPEC-07 previously tested software capability, not communication

Corrected.

The eventual droid-language TARGET now requires a naïve-listener semantic identification test.

A robot whose sound engine works perfectly but communicates nothing cannot pass the language target.

---

# Review 9 — The old latency targets did not mathematically close

Corrected.

The target budget now allocates approximately:

\[
900ms
\]

against a:

\[
1000ms
\]

end-to-end TARGET.

The MUST budget closes at:

\[
1500ms
\]

against the:

\[
1500ms
\]

MUST ceiling.

Further tuning should ideally create more MUST margin during prototype work.

---

# Review 10 — Endpoint target still contains tension

A real trade-off remains.

The target:

\[
350ms
\]

endpoint budget may not be achievable for all hesitant speech without false splits.

Therefore it is explicitly qualified:

> **for clearly completed speech**

while the overall MUST allows:

\[
600ms
\]

p95.

Adaptive endpointing remains TARGET.

---

# Review 11 — Servo noise cannot be specified only in external dBA

Corrected.

The final requirement shall be derived from actual microphone-domain measurements and required recognition performance.

---

# Review 12 — Visible reaction latency was previously unspecified

Corrected.

At least one visible listening acknowledgement now has:

\[
p95\leq350ms
\]

MUST and:

\[
p95\leq250ms
\]

TARGET.

---

# Review 13 — Synchronization requires lead compensation

Corrected.

Scheduled choreography plus empirically measured output latency is now a MUST.

---

# Review 14 — Low-latency audio needs an intentional software path

Corrected.

The architecture now requires:

- warm/persistent playback,
- controlled buffering,
- amplifier wake management.

Exact Linux audio subsystem remains unfrozen.

---

# Review 15 — Droid and TTS barge-in should not necessarily behave identically

Corrected.

Long outputs remain aggressively interruptible.

Short atomic vocal units may complete naturally where that does not impede listening or safety.

---

# Review 16 — Confidently-wrong intent needs a repair mechanism

Corrected.

Speech-triggered locomotion now contains:

```text
ACTION_PENDING
↓
visible/audible tell
↓
cancellation interval
↓
ACTION_COMMIT
```

except stop/inhibition operations.

---

# Review 17 — Open-vocabulary STT may be unnecessary architectural baggage

Partially accepted.

The actual functional requirement is now:

\[
\boxed{\text{natural paraphrase robustness}}
\]

Open-vocabulary STT is TARGET rather than sacred architecture.

If benchmarking later demonstrates that a smaller speech solution satisfies the actual interaction corpus with materially better latency/power/privacy, it may win.

---

# Review 18 — WER cannot be frozen before language/accent requirements

Corrected.

The 15% figure is now explicitly provisional until the corpus is representative of the actual intended users.

---

# Review 19 — Perceptual experiments should precede voice-engine freeze

Correct.

New sequence:

```text
cheap desktop sound experiments
        ↓
naïve perceptual feedback
        ↓
identify useful expressive dimensions
        ↓
freeze production voice-engine requirements
        ↓
implement embedded engine
        ↓
creative Makad-language design
```

The creative language itself remains deferred.

---

# 9. FINAL DECISIONS CARRIED FORWARD

## DEFINITIVELY DECIDED

### Speech input

Makad shall support:

```text
continuous listening
→ interaction detection
→ pre-roll
→ streaming recognition
→ finalized semantic interpretation
```

without push-to-talk during ordinary use.

---

### Human speech onset

Makad must visibly acknowledge human speech rapidly.

At least one visible listening response:

\[
\boxed{p95\leq350ms}
\]

TARGET:

\[
\boxed{p95\leq250ms}
\]

---

### Real response latency

For simple droid interaction:

\[
\boxed{
speech\ end
\rightarrow
Makad\ audio
\leq1.5s\ p95
}
\]

TARGET:

\[
\boxed{
\leq1.0s
}
\]

---

### Partials

Partial transcripts are provisional.

They cannot authorize consequential motion.

---

### Turn lifecycle

Recognition sessions require:

- IDs,
- cancellation,
- stale-result rejection,
- reset.

---

### Interaction correctness

The main performance metric is no longer WER.

It is:

\[
\boxed{
\text{end-to-end intent correctness}
}
\]

with:

\[
Macro\ F1\geq0.90
\]

as the initial MUST acceptance threshold for core supported intents.

---

### Natural language input

Users shall be able to use natural paraphrases.

Fixed exact command grammar is insufficient.

---

### Open-vocabulary STT

Preferred but no longer automatically mandatory if a smaller system demonstrably satisfies Makad's real interaction requirements better.

---

### Voice output

Makad's primary personality output is:

\[
\boxed{\text{DROID VOCALIZATION}}
\]

not traditional English conversation.

---

### Human-language speech

Real-time TTS remains supported but is not the default personality requirement.

---

### Droid vocal engine

It shall support:

- multiple reusable units,
- controlled parameter variation,
- sequencing,
- low-latency playback,
- local/offline reactions,
- AEC-compatible playback reference.

---

### Spectral/AEC constraint

Makad's sound designer receives a real acoustic constraint:

> final recurring language tokens must not break self-audio rejection or barge-in.

But no requirement currently dictates that every vocalization must be broadband.

---

### Droid language

A consistent droid-language system remains:

\[
\boxed{\text{TARGET}}
\]

not a V1 critical-path requirement.

---

### Droid-language success must be measurable

The TARGET will not be considered achieved merely because the engine can generate sounds.

Naïve human listeners must demonstrate that recurring core meanings are actually distinguishable.

---

### Creative language design

Still explicitly deferred.

We are building:

> **the instrument**

before composing:

> **the language.**

---

### Perceptual prototyping comes before production engine freeze

We should test candidate sound dimensions cheaply on a laptop before deciding which synthesis features deserve implementation.

---

### Physical action repair channel

Speech-triggered locomotion shall have:

```text
acknowledgement / pre-action tell
→ short cancellation window
→ action
```

while STOP/inhibition bypasses the delay.

---

### Choreography

Audio, face and mechanical movement require:

- common timestamps,
- latency measurement,
- lead compensation.

Simultaneous command dispatch is not sufficient.

---

# REMAINS PROVISIONAL

- actual microphone system,
- final VAD,
- endpoint algorithm,
- exact endpoint timing,
- STT backend,
- local/cloud/hybrid STT,
- V1 input language(s),
- WER acceptance level,
- exact intent implementation,
- use and size of an LLM,
- context duration,
- TTS backend,
- exact audio backend,
- amplifier wake strategy,
- final AEC implementation,
- actual microphone-domain self-noise threshold,
- final vocal-synthesis dimensions,
- final droid-language comprehension threshold after first prototype experiment.

---

# EXPLICITLY DEFERRED

- multi-speaker diarization,
- simultaneous-speaker understanding,
- mandatory multilingual/code-switch speech,
- unrestricted English conversation,
- long-term conversational memory,
- final Makad vocabulary,
- final Makad phonetics,
- grammar,
- signature sounds,
- emotional syntax,
- language personality.

---

# PRE-HARDWARE VALIDATION GATE

A useful consequence of this revision is that several load-bearing assumptions **do not need the robot to exist**.

Before freezing STT or vocal-engine architecture, we should be able to answer on a laptop:

```text
1. How fast are candidate streaming STT systems?

2. What endpoint settings give acceptable
   pause tolerance vs response speed?

3. How accurately does the complete
   audio → intent pipeline classify natural paraphrases?

4. Does cancellation cleanly isolate rapid turns?

5. Which audio dimensions actually communicate
   different meanings to human listeners?

6. Which candidate droid sounds are easy/hard
   for echo cancellation and barge-in?
```

Those experiments should happen **before** we commit the corresponding architecture to the BOM or embedded software stack.

---

# FINAL VOICE-STACK ARCHITECTURE

```text
                            HUMAN
                              │
                              ▼
┌────────────────────────────────────────────────────┐
│ SPEC-04 — PHYSICAL AUDIO                           │
│                                                    │
│ microphones                                       │
│ DSP                                               │
│ echo management                                   │
└───────────────────────┬────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ SPEC-05 — HEARING                                  │
│                                                    │
│ interaction gating                                │
│ VAD                                               │
│ pre-roll                                          │
│ streaming recognition                             │
│ endpointing                                       │
│ turn lifecycle/cancellation                       │
│ barge-in                                          │
└───────────────────────┬────────────────────────────┘
                        │
                        ▼
                FINAL USER MEANING
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ SPEC-06 — UNDERSTANDING / RESPONSE                 │
│                                                    │
│ natural paraphrase interpretation                 │
│ context                                           │
│ intent correctness                                │
│ ambiguity handling                                │
│ action pending/repair                             │
│ safety-aware behaviour request                    │
│ optional generative reasoning                     │
└───────────────────────┬────────────────────────────┘
                        │
                 COMMUNICATIVE ACT
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
┌────────────────┐ ┌───────────┐ ┌──────────────┐
│ SPEC-07        │ │ HUMAN TTS │ │ PHYSICAL     │
│ DROID VOICE    │ │           │ │ RESPONSE     │
│                │ │ optional  │ │              │
│ primitives     │ │           │ │ eyes         │
│ synthesis      │ │           │ │ head         │
│ sequencing     │ │           │ │ body         │
│ variation      │ │           │ │ wheels       │
└───────┬────────┘ └─────┬─────┘ └───────┬──────┘
        │                │               │
        └────────────────┼───────────────┘
                         ▼
┌────────────────────────────────────────────────────┐
│ RESPONSE CHOREOGRAPHY                              │
│                                                    │
│ shared timeline                                   │
│ measured output delays                            │
│ lead compensation                                 │
│ pre-emption                                       │
│ barge-in                                          │
└───────────────────────┬────────────────────────────┘
                        │
                        ▼
                     MAKAD
```

The architecture can therefore now be summarized more precisely as:

\[
\boxed{
\text{Makad hears humans as language,
understands them as meaning,
and responds as a droid.}
}
\]

And the engineering thesis behind the decision is:

\[
\boxed{
\text{do not spend variable latency generating language
when the character can communicate the required meaning directly.}
}
\]

That is the version of **SPEC-05/06/07** I would now carry into the master Makad engineering specification.