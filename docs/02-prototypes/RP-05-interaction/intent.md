# RP-05 Interaction Intent — Audio-path slice

| Field | Value |
|---|---|
| Status | Audio-path paper 2026-09-21. Content complete as a proposal. **Not a registration.** `AR-*` not locked. Not an ADR |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-05 |
| Slice | `RP05-A` — audio system requirements |
| Feeds | ADR-11 (provisional audio/playback path); informs ADR-10 capture/onset evidence; `LG-07`/`LG-08` and `PB-AUDIO-*` still wait on a later selection |

## 1. Why RP-05 exists

The Core encounter is already storyboarded. Scenario 1 is approved. Wake is a coordinated performance (`P-01`). Action lifecycle, interaction states, and C0 process isolation already exist. What does not exist is the path that carries sound into that architecture and sound back out of it.

RP-05 exists to close two architecture decisions of different kinds:

| ADR | What must be true to close it | Where this folder will produce that |
|---|---|---|
| **ADR-10** invocation/language path and external-network behaviour | Approved name forms and Core requests travel a representative microphone → wake → transcript/NLU → behaviour path with measured reliability, latency, ambiguity, cancellation, and bounded service failure | Later slices: utterance set, engines, services, G01–G04 |
| **ADR-11** astromech audio and Spotify playback path | Capture and playback coexist; authored sounds and music share one interruptible output path; contamination and echo are bounded; onset is observable | This slice states the requirements; a later acoustic prototype supplies evidence |

Mixing them in one implementation pass is how a USB headset quietly chooses the wake engine, or a speaker SKU quietly freezes false-wake policy. This slice keeps the audio channel as its own object.

## 2. The two questions

The governing plan asks only the full can-question. This slice splits it the same way RP-02/RP-03/RP-04 do.

### 2.1 Design question — this slice's deliverable

> What must the body-mounted capture path, wake front end, speech-capture path, speaker/amplifier/enclosure, astromech playback path, and `makad-audio` service satisfy so named wake and Core playback can travel the already-chosen C0 architecture — without selecting parts, engines, or assets?

The answer is [`audio-requirements.md`](audio-requirements.md) plus a compared, **unselected** set of path families in [`audio-path.md`](audio-path.md).

### 2.2 Gate question — not this slice

> Can all approved invocation forms and Core semantic requests travel through representative microphone, network/cloud, behaviour and expression paths with acceptable reliability and perceived timing, explicit ambiguity/cancellation, and bounded service failure?

That is verbatim from the governing plan. It remains reachable. This paper cannot pass or fail it.

## 3. Traceability

| Kind | IDs this slice consumes |
|---|---|
| Architecture drivers | AD-09 cloud bounded; AD-11 failures diagnosable |
| ADRs | ADR-11 (this slice informs); ADR-10 (later); ADR-12 timebase/logging; ADR-13 **not** Core |
| Success | SC-05, SC-07, SC-21, SC-23 (audio share); SC-02 as the later integrated bar |
| Open thresholds | SC-TBD-13, SC-TBD-15, SC-TBD-17, SC-TBD-19 remain unregistered |
| Constraints | CON-11 safety independent of network; CON-13 recording permitted; CON-P03 cloud may be required; CON-P04 explicit timeouts |
| Scope | SCOPE-06 astromech output; SCOPE-16 named wake; SCOPE-19 music; CAND-01 spatial hearing **out of this slice** |

## 4. What “audio system” means here

The governing plan's audio bullet, restated as five objects this slice must specify:

| Object | Must exist as a requirement | Must not be faked by |
|---|---|---|
| Four body-mounted microphones | Placement, sync, listen/capture/off/fault, Pi 5 front-end necessity | A headset, a laptop mic, or ear-pod capsules |
| Wake front end and speech capture | Always-on listen in registered sleep; request capture after accept; no intent from stale/missing audio | Treating wake-word engine choice as the capture architecture |
| Speaker, amplifier, enclosure | Body-mounted output, independent `PB-AUDIO-OUT`, CAD envelope as reservation | A GPIO beep, a phone speaker, or head-mounted driver |
| Astromech playback | Named `A-*` primitives, cue identity, cancel/silence, no English character TTS | Diagnostic speech, a single canned beep for every state |
| Echo / self-noise / contamination | Simultaneous capture+playback; speaker, cooler, head servos, drive as named interferers | Datasheet SNR in a quiet room |

## 5. Evidence boundary

Every value in this slice is `U` or inherited `E`. Nothing here is `W`. A later acoustic rig may promote a row; this paper cannot.

RP-04 `BD-03` already allows an audio **timing** stand-in before ADR-11. That stand-in can prove scheduling, identity, stop, and underrun. It cannot prove loudness, intelligibility, false-wake under playback, or enclosure vibration.

## 6. Non-goals of `RP05-A`

This slice does not:

- author the versioned intent/utterance set, paraphrase matrix, or speaker/distance/noise matrix;
- select wake-word, ASR, or NLU implementations;
- select microphone, codec, USB array, speaker, amplifier, or mesh SKUs;
- produce astromech sound assets or a final vocabulary recording;
- implement `makad-audio`, time/timer/alarm, Spotify, or display utility states;
- register `RP05-G01…G05` numeric thresholds;
- close ADR-10 or ADR-11;
- require direction-of-arrival for Core wake or come/follow (`CAND-01` stays Candidate);
- reopen `CA-07` (no ROS 2 in the V1 safety path), UART/COBS, or C0 Unix-domain sockets;
- treat `specsheets/spec11.md` “no USB array” as a project lock.

## 7. Completion criteria for this paper

**Content (met as a proposal, 2026-09-21):** capture, playback, simultaneous-use, contamination, and `makad-audio` contracts exist as `AR-*` IDs; inherited locks are cited rather than restated; path families are compared with no winner; no prose claims a SKU freeze, gate pass, or ADR.

**Registration (not met):** `BD-A01…A03` remain Proposed. `AR-*` are not design-definition until those three are explicitly accepted and §3 of `decision.md` carries a registration ID. Hardware/engine `BD-*` stay open either way.
