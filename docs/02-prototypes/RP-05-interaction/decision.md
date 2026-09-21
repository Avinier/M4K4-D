# RP-05 Decision Record — audio-path slice

| Field | Value |
|---|---|
| Status | Slice-boundary paper 2026-09-21. `BD-A01`…`A03` **Proposed**. `AR-*` written, **not locked**. No hardware family. No engine. No ADR |
| Owner | Project builder |
| Created | 2026-09-21 |

## 1. Builder decisions

| ID | Decision needed | Answer | Status | Consequence |
|---|---|---|---|---|
| `BD-A01` | First RP-05 paper owns **audio path requirements only** | Accept: capture, playback, duplex/contamination, `makad-audio` contract. Corpus, engines, Spotify detail, implementation, numeric gates wait | **Proposed 2026-09-21** | Folder is `RP05-A`, not the full prototype |
| `BD-A02` | Spatial hearing in Core RP-05? | **No.** `CAND-01` / ADR-13 stay Candidate. Four body mics remain because of wake/capture/AEC geometry, not because DOA is required to pass RP-05 | **Proposed 2026-09-21** | spec-11 13° is not a Core gate |
| `BD-A03` | Does spec-11 ban USB? | **No.** USB families `AP-USB` / `AP-USB-IO` remain comparable. They lose only by failing `AR-*` (§3 of `audio-path.md`) | **Proposed 2026-09-21** | Codec/TDM is not pre-selected |
| `BD-A04` | Capture/playback family (`AP-*`) | — | **OPEN** | Blocks `LG-07`/`LG-08` selection, `PB-AUDIO-IN` source, GPIO vs USB |
| `BD-A05` | Microphone capsule SKU | — | **OPEN** | Blocks CAD port freeze beyond Layout 02 reservation |
| `BD-A06` | Speaker + amplifier SKU | — | **OPEN** | Blocks cavity/grille/amp envelope freeze; RP-06 |
| `BD-A07` | Wake-word / speech / NLU engines | — | **OPEN** | Later slice; `AR-24` |
| `BD-A08` | Astromech asset production | — | **OPEN** | IDs exist in RP-01; files do not |

`BD-A01`…`A03` are proposed scope decisions. The rest of this slice is written **as if** they will be accepted; that is not acceptance. `AR-*` become append-only design-definition only after a dated accept of those three and a registration ID in §3. Hardware `BD-A04`…`A08` stay open until a later slice with evidence.

## 2. What is not decided

- ADR-10, ADR-11, ADR-13
- any `RP05-G*` pass or numeric freeze
- purchase authorization
- whether GPIO18–21 are used or left idle
- Spotify output device (local speaker vs Spotify Connect vs both) — later slice, constrained by `AR-36`

## 3. Registrations

**Empty.** No `RP05-P*-REG-*`. A review that the paper is complete is not a registration. Mint one only after the builder explicitly accepts `BD-A01`…`A03`.

## 4. Handoffs

| To | Handoff |
|---|---|
| RP-02 | Keep `LG-07`/`LG-08` unselected; home of the remaining choice is this folder's `BD-A04` |
| RP-04 | Continue using the timing stand-in; do not cite it as ADR-11 |
| RP-06 | Envelopes unchanged; audio SKUs still `U` |
| Later RP-05 | After this registration: corpus, engines, Spotify/utilities, family/SKU, `makad-audio`, numeric gates, scored runs |
