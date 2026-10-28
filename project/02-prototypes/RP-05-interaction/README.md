# RP-05 — Wake and interaction latency path

| Field | Value |
|---|---|
| Status | **Audio-path paper `RP05-A` 2026-09-21. Written, not registered.** `AR-*` exist; they are not design-definition until `BD-A01`…`A03` are accepted. No SKU. No engine. No implementation. No numeric gate. ADR-10/ADR-11 open |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-05 |
| Purpose | Later: close **ADR-10** (invocation/language/network) and a **provisional ADR-11** (astromech/Spotify playback path) after measured G01–G05. This slice only states what the audio system must satisfy before those selections |

RP-01 is an object. RP-02 is states, links, and firmware/process boundaries. RP-03 is a vehicle plus local safety. RP-04 is coordination. **RP-05 is the interaction path:** named wake, spoken request, services, and the audio channel those things travel through.

This first paper slice is **only the audio system**. Utterance corpus, wake-word/NLU engines, Spotify behaviour detail, `makad-audio` code, numeric `RP05-G01…G05` thresholds, acoustic matrix runs, and ADR conclusions are later slices.

## Start here

| Document | What it owns | Status |
|---|---|---|
| [Intent](intent.md) | Why this slice exists; design vs gate questions | Paper |
| [Inherited](inherited.md) | Pointers. Do not copy the sources | Paper |
| [Audio requirements](audio-requirements.md) | `AR-*` capture, playback, contamination, service contract | Written; **not locked** |
| [Audio path families](audio-path.md) | Codec/TDM vs USB vs split comparison against `AR-*` | Compared; no select |
| [Decision](decision.md) | `BD-A01`…`A03` **Proposed**; hardware/engine `BD-*` open | No registration |
| [Gates](gates.md) | Candidate *metrics* for the audio share of G01/G03/G04/G05 | Candidates only |

Namespaces: `AR-*` · `AP-*` · `BD-*` · `RP05-A` · `RP05-G`.

## What this slice does not do

- pick a microphone, codec, USB array, speaker, amplifier, or enclosure SKU;
- pick a wake-word or speech/NLU implementation;
- author astromech WAV/synth assets;
- implement `makad-audio`, logging, or any service;
- register trial counts, false-wake rates, latency ceilings, or coherence windows;
- import any archived pre-foundation audio draft as a frozen architecture;
- pull spatial hearing (`CAND-01` / ADR-13) into Core RP-05.

## Remaining slices

Paper content for `RP05-A` is complete as a proposal. `AR-*` stay writable until step 1.

1. Accept `BD-A01`…`A03` and register this design-definition slice.
2. Versioned utterance/intent corpus.
3. Wake, ASR, and NLU engine comparison.
4. Spotify and utility-service behaviour.
5. Audio-family/SKU selection.
6. `makad-audio` implementation.
7. Numeric G01–G05 registration.
8. Acoustic and end-to-end scored runs.

Do not treat this folder as ADR-11. Do not treat an RP-04 GPIO beep as acoustic evidence. Do not reopen `CA-06` UART reservations to steal GPIO18–21 without a cited change request.
