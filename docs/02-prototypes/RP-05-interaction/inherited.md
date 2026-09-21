# RP-05 inherited authority — consume, do not copy

| Field | Value |
|---|---|
| Status | Pointer index for `RP05-A`. Not a second source of truth |
| Created | 2026-09-21 |

If a cited file changes, this index is wrong until updated. Do not paste budgets, pin maps, CAD numbers, or cue lists into RP-05 documents.

## 1. Already locked in other records

These facts are locked by the cited authorities, not by `AR-*`. `AR-*` only consume them, and only after `RP05-A` is registered.

| Fact | Authority | RP-05 consequence |
|---|---|---|
| Named wake forms `M4`, `M4K4`, `Makad` | `../../00-foundation/core-interaction-scenarios.md`; SCOPE-16 | Capture/wake must accept all three; engine remains open |
| Character output is authored astromech, not English TTS | SCOPE-06; SC-07; RP-01 `intent.md` §3.2 | Playback path carries `A-*`, never ordinary speech as the in-character voice |
| Four PDM MEMS mics, body-mounted; none in ears/head | `../../01-system/dimensional-baseline.md`; sourcing matrix | Placement is a lock; interface/front end is not |
| Speaker body-mounted | same | Head is not an acoustic cavity |
| Pi 5 2 GB is C0 | `RP02-P2-REG-02` | No native 4-channel PDM; a front end is mandatory |
| GPIO18–21 reserved for audio TDM/I²S | `CA-06` | UART0/UART2 stay on GPIO14/15 and GPIO4/5 |
| `makad-audio` owns capture/playback/wake front end/astromech timing; no actuator access | `CA-08` | Process isolation and independent degrade |
| `PB-AUDIO-IN` / `PB-AUDIO-OUT`, `LG-07` / `LG-08`, `LP-07-*` / `LP-08-*` | RP-02 power/load | Profiles exist; ratings `U/E` until a candidate |
| Missing/stale audio produces no wake/intent | `LG-07`; `F-21` | Restoration accepts only fresh audio |
| Mute/off cannot delay stop; restore cannot replay cancelled audio | `LG-08`; `PB-AUDIO-OUT` | Safety pre-empts playback |
| Audio onset is C0 callback evidence, not a UART field | RP-04 IR-06; `RP02-P4-REG-03` | `makad-audio` logs `source_onset` |
| Cue identity, stale-epoch reject, underrun as a deny reason | IR-01, IR-02, IR-09 | Playback is a scored channel |
| `A-*` primitive names | RP-01 `intent.md` | This slice consumes the names; it does not author samples |
| `P-01` arms `A-wake-rise`; optional sparse `A-query-rise` | RP-04 `situations.md` §11 | Timing owned by RP-04; acoustics owned here later |
| Audio timing stand-in allowed before ADR-11 | RP-04 `BD-03` | Stand-in ≠ ADR-11 evidence |
| Quiet-sleep listen; camera/head motion off by policy | RP-02 operating situations `CC-02F`; `CC-03N` | False wake must not change the sleeping state |
| Charging: mics and ordinary audio off | `PB-AUDIO-*`; `OM-06` | No listen, no playback in charge |
| Spatial hearing is Candidate | CAND-01; ADR-13; SC non-Core list | Four mics may later serve it; Core RP-05 must not require DOA |
| Recording/cloud use permitted | CON-13 | No project-level mic prohibition |

## 2. CAD reservations — envelopes, not parts

| Reservation | Authority | Still open |
|---|---|---|
| Four provisional PDM ports `FRONT_L/R`, `REAR_L/R` at Layout 02 coordinates | RP-03 body/chassis Layout 02 generated dimensions | Exact capsules, mesh, port acoustics |
| Speaker 50 mm basket / 44 mm cone at `(72, 0, 99)` mm; 34 mm cavity; front grille | Layout 02 brief | SKU, amp, mesh, vibration isolation |
| Amplifier envelope in the body | same | Rail, mute GPIO, connector |
| Ports away from SBC cooler exhaust | sourcing matrix; `CCD-CLG-01` | Measured fan contamination |

RP-06 owns whether the sourced parts still fit. This slice must not shrink or grow those envelopes in prose.

## 3. Later RP-05 slices — do not start them here

| Later object | Already specified elsewhere | Still missing |
|---|---|---|
| Utterance / paraphrase / cancel / unsupported set | Scenario examples only | Versioned corpus |
| Wake-word / ASR / NLU engines | SCOPE-16 “technology open” | Selection |
| Intent dispatch, timers, Spotify, display utilities | RP-02 `BS-05…08`, `AL-*`, `CC-07*`, `CC-08` | Implementation and Spotify detail |
| Numeric `RP05-G01…G05` | Plan lists *candidate* gates | Trial counts, rates, latencies |
| Monotonic joined log | `timebase.md`; RP-04 IR-11…13 | Implementation and validation |
| Evidence packet / ADR close | Plan exit decision | Measured runs |

## 4. Exploratory input — not inherited lock

Archived pre-foundation audio drafts have no authority in RP-05. The current dimensional baseline independently reserves a body four-microphone geometry. **USB vs codec/TDM remains an open RP-02/RP-05 comparison.** Spatial hearing remains a Candidate and has no inherited numeric direction-of-arrival gate. Do not use archived material to close ADR-11.
