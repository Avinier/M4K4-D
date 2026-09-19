I read the foundation, the risk-prototype plan, and all three existing prototype folders. Here is how I would build RP-04.

The short version. Copy the RP-03 folder pattern exactly, but change what the folder is about. RP-01 is an object, RP-02 is a set of states and interfaces, RP-03 is a vehicle plus a safety authority. RP-04 is a scheduler plus a perception instrument. It buys nothing and builds no mechanism, and its hardest gate is judged by human observers rather than by a meter. Write the construction record first, then the Parts in order, then the start-here index last. That sequence worked for RP-03 and there is no reason to invent a new one.

Three things that make RP-04 different from its siblings

The rig it is supposed to use does not exist, and naming that is the plan's first job. The risk-prototype plan tells RP-04 to compose the measured head and base controllers. Neither measurement exists. RP-01 has no rig and no actuator freeze, RP-03 has no chassis, the monotonic timebase is written but not implemented, and Stage 0 is not closed. A folder written as "wait for those" stays empty past 5 December. So the phase ladder has to name what paper and software can produce today, the way RP-03 named its circular dependencies instead of stalling on them. There is real work available now, and some of it is on a deadline that runs ahead of RP-04's own stage.

The channel set is wider than head, body and wheels. SC-05 asks that display, head, sound and base express one intent. That is five channels across four controllers: head motion and status light on C2, face on the display renderer, astromech audio on the Pi, base motion on C3. Eyes are the most legible channel Makad has, so a coherence gate scored without them measures the wrong thing. The open-items index already hands the eye and audio placeholders from RP-01 forward to RP-04, so picking them up is the documented handoff rather than scope creep.

The composer and the rating instrument must not be written by the same pass. RP-03's best structural decision was splitting geometry from sensing so a chassis could not quietly choose its sensors. The RP-04 equivalent is splitting the engineering from the human-subjects work. An observer protocol designed after the composer exists gets written to confirm it. The threshold behind SC-TBD-01 has to be frozen before any composed performance is tuned against a score.

The folder and the Part order

I would open the construction record against four failure modes, all visible in this repository's history:

- The composer becomes a puppet track. A fixed keyframe timeline demos beautifully and collapses the first time latency varies. SC-01 and SC-02 explicitly reject a sequence of rescued subsystem demos.
- The observer protocol becomes a compliment machine. Unblinded, small panel, leading questions, builder in the room.
- Timing gets measured on the composer's own clock. A scheduler log saying it dispatched at zero is not evidence that the head moved. Every onset needs the external video witness and the status-light cue.
- Estimated response models harden into truth. This is the same class as the head-mass estimate that became a target. Every Phase A parameter carries a re-run obligation when measured models arrive.

┌─────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│              File               │                                                    What it owns                                                     │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ plan.md                         │ Construction record, failure modes, Part order. Retires into the index.                                             │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ intent.md                       │ Why RP-04 exists, the two questions, traceability, inherited inputs, non-goals, phase ladder, evidence rules.       │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ performances.md                 │ The authored multi-channel scores. Storyboard analogue. Compositions of existing head and base panels plus face,    │
│                                 │ light and audio cues.                                                                                               │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ timing-model.md                 │ The physics analogue: per-channel chain from decision to visible onset, jitter budget, perceptual tolerance         │
│                                 │ windows, interruption budget, settle defined per channel.                                                           │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ concepts/                       │ At least two scheduling architectures differing on where phase authority lives, plus the filled comparison.         │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ composition-rules.md            │ Anchors, lead compensation, anticipation, overlap, follow-through, counter-motion, hand-off, settle.                │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ interruption-and-degradation.md │ The cross-channel algebra behind two gates: what the other four channels do when one is pre-empted, denied or       │
│                                 │ absent.                                                                                                             │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ observer-protocol.md            │ Blinded rating instrument, the independent-channel baseline definition, sample and questions. Kept separate on      │
│                                 │ purpose.                                                                                                            │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ interface-requirements.md       │ What composition needs from the link contract, the timebase and the log schema.                                     │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ fault-matrix.md                 │ New rows in the RP-02 schema: delayed channel, denied channel, expiry mid-performance, out-of-order arrival, clock  │
│                                 │ step, renderer stall.                                                                                               │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ rig.md                          │ The composition bench, video witness, timing cue, replay harness, readiness checklist.                              │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ gates.md                        │ Paper gates plus the five physical gate candidate registrations.                                                    │
├─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ decision.md                     │ Builder decisions, Part registration records, the ADR-05 ladder.                                                    │
└─────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

No cad/ directory. RP-04 has no geometry.

Six Parts, in dependency order: intent and performances, then the timing model, then concepts and the interface requirements that fall out of them, then composition rules with interruption and degradation and the fault rows, then the observer protocol, then rig, gates and phases. The observer protocol can run in parallel with the middle Parts because it depends only on the authored performances.

The phase ladder is where the schedule unlocks. Phase A is paper plus an offline composer running against modelled channels, which produces no coherence claim at all. Phase B is head-domain composition on the RP-01 rig with the base explicitly absent, which is a legitimate degradation configuration rather than a fudge. The wake and attend performance in Scenario 1 has a stationary base anyway, so Phase B is the real thing for it rather than a substitute. Phase C is the full composition, where the excited turn and spin performance, counter-motion and base interruption live.

Decisions I would need from you first

One of these has a deadline earlier than RP-04's own stage. The head command message carries a duration and an expiry but no scheduled start time, and head feedback already publishes gesture progress. So cue chaining off upstream progress is supported by the current contract and absolute scheduled onset is not. There is also no identifier that spans channels, which means a five-channel performance cannot be joined in the logs by anything except clock alignment. Both are answerable on paper now, and RP-02 needs the answer before it freezes byte layouts.

The rest:

- The independent-channel baseline. The honest version is each channel doing its own best local behaviour with no shared schedule. A deliberately bad straw man inflates the coherence gate.
- The observer panel. Who rates, whether blinding is feasible in a household, and what counts as the required improvement.
- Astromech audio as a scored channel, given that the speaker and amplifier are unselected and ADR-11 is untouched.
- Whether RP-04 authors the eye vocabulary or defers it to RP-05 and RP-06.
- The exact three performances and which existing head and base panels each one composes.