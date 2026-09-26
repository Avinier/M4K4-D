# RP-05 Decision Record — audio-path slice

| Field | Value |
|---|---|
| Status | Slice-boundary paper 2026-09-21. `BD-A01`…`A03` **Proposed**. `AR-*` written, **not locked**. Hardware family and SKUs: **working selection 2026-09-26** (`BD-A04`…`A06`). No engine. No ADR |
| Owner | Project builder |
| Created | 2026-09-21 |

## 1. Builder decisions

| ID | Decision needed | Answer | Status | Consequence |
|---|---|---|---|---|
| `BD-A01` | First RP-05 paper owns **audio path requirements only** | Accept: capture, playback, duplex/contamination, `makad-audio` contract. Corpus, engines, Spotify detail, implementation, numeric gates wait | **Proposed 2026-09-21** | Folder is `RP05-A`, not the full prototype |
| `BD-A02` | Spatial hearing in Core RP-05? | **No.** `CAND-01` / ADR-13 stay Candidate. Four body mics remain because of wake/capture/AEC geometry, not because DOA is required to pass RP-05 | **Proposed 2026-09-21** | spec-11 13° is not a Core gate |
| `BD-A03` | Does spec-11 ban USB? | **No.** USB families `AP-USB` / `AP-USB-IO` remain comparable. They lose only by failing `AR-*` (§3 of `audio-path.md`) | **Proposed 2026-09-21** | Codec/TDM is not pre-selected |
| `BD-A04` | Capture/playback family (`AP-*`) | **`AP-TDM`, realised as two I²S lanes on one Pi 5 `i2s0` clock**: 2 × ADAU7002 PDM→I²S on SDI0 (GPIO20) and SDI1 (GPIO22), MAX98357A on SDO0 (GPIO21), `AMP_SD` on GPIO23; 48 kHz. RP1 has no true TDM, so a 4-slot codec on one lane is not a path. Needs `CA-06` CR-01 (GPIO22/23) | **Working selection 2026-09-26** ([evidence](../RP-06-cad/peripheral-selection.md) §2); bench proof and dated builder acceptance remain | Unblocks `LG-07`/`LG-08`; `PB-AUDIO-IN` = Pi header 3.3 V sub-branch (RP-02 to confirm) |
| `BD-A05` | Microphone capsule SKU | **Infineon IM73D122V01** (73 dB(A) SNR, IP57, active and preferred), one per `PCB-06` board at the unchanged Layout 02 ports; bench article `KIT_IM73D122V01_FLEX` | **Working selection 2026-09-26** | Port coordinates stay the Layout 02 reservation (`AR-04`); board fixing to the body frame open |
| `BD-A06` | Speaker + amplifier SKU | **Visaton K 50 WP 8 Ω** (Ø50 × 18 mm, 48 g, 2 W) + **MAX98357A** (1.75 W into 8 Ω at 5 V, SD default off) on `PCB-05` | **Working selection 2026-09-26** | Fits the 50 mm / 18 mm driver reservation; RP-06 cut the sealed cavity from 34 to 20 mm because the old one ran through the compute tray and Pi 5 (`AR-31` envelope revision, `RP03-CAD-11`); low-frequency output to be measured |
| `BD-A07` | Wake-word / speech / NLU engines | — | **OPEN** | Later slice; `AR-24` |
| `BD-A08` | Astromech asset production | — | **OPEN** | IDs exist in RP-01; files do not |

`BD-A01`…`A03` are proposed scope decisions. The rest of this slice is written **as if** they will be accepted; that is not acceptance. `AR-*` become append-only design-definition only after a dated accept of those three and a registration ID in §3. Hardware `BD-A04`…`A08` stay open until a later slice with evidence.

## 2. What is not decided

- ADR-10, ADR-11, ADR-13
- any `RP05-G*` pass or numeric freeze
- purchase authorization
- ~~whether GPIO18–21 are used or left idle~~ (used, plus GPIO22/23 under `CA-06` CR-01; `BD-A04`, 2026-09-26)
- Spotify output device (local speaker vs Spotify Connect vs both) — later slice, constrained by `AR-36`

## 3. Registrations

**Empty.** No `RP05-P*-REG-*`. A review that the paper is complete is not a registration. Mint one only after the builder explicitly accepts `BD-A01`…`A03`.

## 4. Handoffs

| To | Handoff |
|---|---|
| RP-02 | `LG-07`/`LG-08` now have working parts (`BD-A04`…`A06`); confirm the `PB-AUDIO-IN` attribution to the Pi header 3.3 V and raise `CA-06` CR-01 (GPIO22 = I²S0 SDI1, GPIO23 = `AMP_SD`) |
| RP-04 | Continue using the timing stand-in; do not cite it as ADR-11 |
| RP-06 | Parts modelled in body Layout 02 (`RP03-CAD-11`); ports unchanged; cavity 34 → 20 mm and `PCB-05` moved above the Pi 5 (the old reservations overlapped it) |
| Later RP-05 | After this registration: corpus, engines, Spotify/utilities, family/SKU, `makad-audio`, numeric gates, scored runs |
