Yes — that correction makes sense. I made SPEC-04 a little too narrowly about the **input/listening pipeline**, when for Makad we should already specify the **physical audio hardware architecture**, because speaker location, mic location, AEC, and speech acquisition affect each other.

So I’d amend SPEC-04 in three concrete ways:

1. **Speaker is physically located in the body**, matching the visualization.
2. **Microphones get explicit physical placement**, rather than being left abstract.
3. **Speech recognition is explicitly part of the pipeline**, although SPEC-05 will still define its detailed latency/accuracy requirements.

### Speaker placement — freeze this

The **main speaker should be in the front of Makad's torso/body**, behind the speaker grille already present in the visual design.

So mechanically:

```text
         HEAD
    ┌─────────────┐
    │   SCREEN    │
    │             │
    └─────────────┘
       neck joint

    ┌─────────────┐
    │             │
    │  CAMERA /   │   ← depending final camera placement
    │  DETAILS    │
    │             │
    │  ▒▒▒▒▒▒▒▒   │
    │  SPEAKER    │   ← speaker grille
    │  ▒▒▒▒▒▒▒▒   │
    │             │
    │   MAKAD     │
    └─────────────┘
          BODY
```

That should become a **MUST-HAVE mechanical requirement** rather than something we reconsider later.

The reasons are also good mechanically: the body has much more internal depth for a proper speaker/enclosure, the speaker mass doesn't move with the neck, wiring is simpler, and the grille fits the industrial/droid aesthetic we're already using.

We should **not put the main speaker inside the moving head.**

### Microphones — I think the ears are the natural location

The visual design already gives Makad two side ears. That gives us a very convenient architecture:

```text
          MIC L                 MIC R
            ↓                     ↓
        ┌───────┐             ┌───────┐
       (  EAR   )─────────────(  EAR   )
        └───────┘   SCREEN    └───────┘
                   / FACE
```

So I would change the previous tentative language and make the **intended architecture two microphones, one associated with each side/ear region**.

Not necessarily literally buried inside the decorative ear—the CAD may put the MEMS mic a few millimetres inward with a proper acoustic port—but visually the microphone openings can be integrated into the ears.

This gives us:

* decent physical separation between microphones,
* left/right acoustic information,
* potential rough sound direction,
* better noise processing than one random body microphone,
* microphones physically farther from the body speaker,
* a very clean aesthetic because we don't need obvious microphone holes across the face.

So I'd change `C4-R09` from "1 minimum, 2+ target" to:

> **C4-R09 — Dual-microphone intended architecture — MUST-HAVE DESIGN INTENT**
> Makad shall be designed around two synchronized microphone channels positioned on opposite sides of the head/ear region. A single-microphone implementation may be used temporarily during early software bring-up, but the enclosure and electronics architecture shall reserve the dual-microphone configuration.

That is much more appropriate for the Makad we're actually designing.

---

## And yes: speech recognition absolutely belongs in the architecture

The complete chain should be thought about as:

```text
                  USER SPEAKS
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          LEFT MIC            RIGHT MIC
             │                   │
             └─────────┬─────────┘
                       ▼
               audio acquisition
                       │
                       ▼
             noise / echo handling
                       │
                       ▼
                     VAD
              "is someone speaking?"
                       │
                       ▼
              wake/address detection
                       │
                       ▼
             streaming speech audio
                       │
                       ▼
             ┌───────────────────┐
             │ SPEECH RECOGNITION│
             │       STT         │
             └─────────┬─────────┘
                       │
                       ▼
                   USER TEXT
                       │
                       ▼
              conversation system
                       │
                       ▼
                  RESPONSE TEXT
                       │
                       ▼
                      TTS
                       │
                       ▼
                BODY SPEAKER
```

So **speech recognition/STT is definitely part of Makad's audio/speech system**.

The only reason I separated it was specification cleanliness:

* **SPEC-04:** microphones + continuous listening + clean speech acquisition
* **SPEC-05:** speech → text, with actual STT model/architecture/latency/accuracy
* **SPEC-06:** LLM/conversation + response generation
* **SPEC-07:** speaker output, robot noises, TTS/audio personality

But these specs are **not pretending the systems are physically independent**.

In fact SPEC-04 must already say:

> The microphone subsystem shall produce audio suitable for low-latency streaming speech recognition.

And:

> The speech-recognition subsystem shall be able to begin processing an utterance before the user has finished speaking.

Then SPEC-05 tells us **exactly how good that needs to be.**

---

## One more important speaker requirement

Because the speaker is in the body and the microphones are around the head, our physical arrangement becomes roughly:

```text
             MIC L        MIC R
                \          /
                 \  HEAD  /
                  \______/

                    ||
                   NECK
                    ||

              ┌────────────┐
              │            │
              │            │
              │  SPEAKER   │
              │   ▒▒▒▒▒    │
              │            │
              └────────────┘
                   BODY
```

That's actually favorable.

We should explicitly require:

> **C4-R11A — Speaker/microphone physical separation — MUST-HAVE**
> The primary loudspeaker shall remain in the torso while the microphones remain in the upper head/ear region, maximizing physical separation available within Makad's geometry.

And the body speaker should have a **real acoustic cavity**, not just:

> speaker driver screwed directly against a decorative grille.

Later, during audio-output specification, we'll calculate:

* desired SPL,
* driver diameter,
* amplifier power,
* enclosure volume,
* grille open area,
* resonance,
* mounting.

We're not choosing those yet.

---

## So Makad's audio hardware is now conceptually

**Head / ears**

* 2 synchronized microphones
* left/right separation
* acoustic ports
* potentially rough sound direction

**Body**

* primary speaker
* visible integrated grille
* speaker enclosure/cavity
* amplifier/audio electronics where practical

**Compute**

* continuous audio capture
* AEC
* VAD
* wake/address detection
* streaming STT
* conversational processing
* TTS
* robot-sound playback

And critically:

[
\boxed{
\text{Mic → STT → intelligence → TTS/sound → speaker}
}
]

while simultaneously maintaining:

[
\boxed{
\text{speaker reference → AEC → microphone cleaning}
}
]

so Makad can eventually **hear us even while it is making noise itself.**

So yes: **speaker in the torso is now the intended physical design, dual microphones around the head/ears are the intended microphone design, and speech recognition is explicitly in the speech pipeline.**

With those amendments, I think **SPEC-04 is conceptually complete enough to critique/freeze before we move into SPEC-05**, where we'll tackle the actual low-latency speech-to-text requirements in detail.
