# RP-05 audio requirements

| Field | Value |
|---|---|
| Status | Paper `RP05-A`. `AR-*` are **written, not locked**. They are not design-definition until `BD-A01`…`A03` are accepted. Not measured bars |
| Owner | Project builder |
| Created | 2026-09-21 |
| Consumes | [`inherited.md`](inherited.md), [`intent.md`](intent.md) |
| Feeds | [`audio-path.md`](audio-path.md) comparison; later SKU/engine slices; RP-02 `LG-07`/`LG-08` selection; RP-06 fit |

Until registration, these IDs may still be edited in place. Append-only / supersession rules start only after `BD-A01`…`A03` are accepted. Numeric loudness, false-wake rate, SNR, and latency ceilings are **not** in this file.

## 1. Capture array

| ID | Requirement |
|---|---|
| `AR-01` | Primary capture is **four** digital MEMS microphones on the body. The count is already locked in the dimensional baseline; this row consumes it. Capsule SKU is not selected. |
| `AR-02` | No microphone in the head, neck, or ear pods. Ear pods stay visual/mechanical. |
| `AR-03` | The four channels are captured as one synchronized array: shared start, defined channel map (`FRONT_L`, `FRONT_R`, `REAR_L`, `REAR_R` per Layout 02), and a reconstructable sample-time relationship among channels. Four independent unsynchronized gadgets do not satisfy this. |
| `AR-04` | Geometry is non-collinear and wide on the body. Layout 02 port coordinates are the current reservation. Moving a port is an RP-06/CAD change, not an RP-05 prose change. |
| `AR-05` | A Raspberry Pi 5 has no native four-channel PDM capture. V1 therefore includes an explicit **front end** (codec/TDM, USB array, or another family that meets these `AR-*`). Direct four-wire PDM into C0 GPIO is not a path. |
| `AR-06` | If the selected path uses I²S/TDM, it consumes the `CA-06` GPIO18–21 reservation. It does not steal UART0 (GPIO14/15) or UART2 (GPIO4/5). A HAT/carrier that collides with those UARTs is non-compliant until a cited `CA-06` change request exists. |
| `AR-07` | Microphone reference/return is not an audio-output or motor return (`PB-AUDIO-IN`). USB/I²S/backfeed must not power an off SBC or a safety branch. |

PDM remains the **preferred capsule interface** (dimensional baseline, sourcing matrix). The front-end **host** interface is the open `AP-*` choice.

## 2. Listen, capture, fault, off

These names already exist as `LP-07-*`. This slice states the interaction contract those profiles must support.

| ID | Requirement |
|---|---|
| `AR-10` | `LP-07-LISTEN` is the named-wake listening profile. It runs in registered quiet sleep and ordinary awake listening (`CC-02F/T`, wake, social). Camera-off and head-torque-off in quiet sleep are RP-02 policy; listening must not require them to be on. |
| `AR-11` | `LP-07-CAPTURE` is the request-capture profile after an accepted invocation or during registered music/request cases. Listen→capture is a `makad-audio` mode change, not a new process with actuator rights. |
| `AR-12` | `LP-07-OFF` is required in charging and final shutdown. No wake, transcript, or intent is generated from an off or unpowered front end. |
| `AR-13` | `LP-07-FAULT` is distinguishable from silence. Missing device, stuck clock, all-zero frames, or stale frame-age (`F-21`) produce **no** wake and **no** request accept. Health is logged. Hazardous motion is not commanded because no intent is produced. |
| `AR-14` | After fault or power restore, only **fresh** audio may create a new invocation or request. Buffered pre-fault samples are discarded. |
| `AR-15` | A rejected invocation (wrong name, below-threshold, or `CC-03N` non-wake trial) leaves the sleeping/idle operating vector unchanged: no `P-01`, no camera start, no head rise, no astromech, no status-light wake. The audio service may log a reject. It must not emit `AudioPlay` or an intent-accept. |
| `AR-16` | Wake detection is a **proposal** to `makad-core`. `makad-audio` does not dispatch `HEAD_GOAL`, face, light, or base. |

## 3. Wake front end vs speech capture

| ID | Requirement |
|---|---|
| `AR-20` | The listen path can run continuously in `LP-07-LISTEN` without opening a cloud session and without starting the camera. Cloud NLU is `makad-edge` after a local accept. |
| `AR-21` | The three approved name forms are in-scope stimuli. Pronunciation, speaker, distance, household noise, mechanism noise, and M4's own playback are in-scope **later test conditions**, not reasons to drop a name form. |
| `AR-22` | Speech capture after accept must yield a bounded audio segment (or streaming equivalent) that `makad-edge` can transcribe. End-of-utterance, timeout, and `EV-17` cancel are observable. Exact ASR engine is out of this slice. |
| `AR-23` | Capture timestamps follow `timebase.md`: master-monotonic microseconds after reconciliation, raw local time retained. Wall-clock step must not invent an invocation (`IR-13` class). |
| `AR-24` | Engine choice (on-device wake word, cloud wake, hybrid) is **not** made here. Any engine must consume `AR-03` channels or a documented mixdown of them, and must obey `AR-15`/`AR-16`. |

## 4. Playback chain

| ID | Requirement |
|---|---|
| `AR-30` | Playback is body-mounted: speaker, amplifier, cavity, and grille. The head is not the loudspeaker. |
| `AR-31` | Layout 02's 50 mm basket / 44 mm cone / 34 mm cavity / front grille / amplifier envelope is a **reservation**. Fitting a part that needs a different envelope is RP-06 work, not a silent RP-05 resize. |
| `AR-32` | Electrical identity is `LG-08` on `PB-AUDIO-OUT`: independent switching/protection from C2/C3 motor energy; speaker current does not flow through compute/safety references. |
| `AR-33` | Profiles `LP-08-OFF/IDLE/CHIRP/ALARM/MUSIC` must be expressible. `LP-08-CREST` and `LP-08-SINEREF` are bench/characterization, not character cues. |
| `AR-34` | Character playback is named RP-01 primitives (`A-wake-rise`, `A-query-rise`, `A-affirm`, `A-reject`, `A-laugh`, `A-happy`, `A-sad`, `A-angry`, `A-startle`, `A-relief`, `A-confused`, `A-affection`, `A-sleep-fall`, `A-fail`). Silence is a legal cue. English TTS, recorded human speech, or copied R2-D2 lines are not the in-character voice (SCOPE-06, SC-07). |
| `AR-35` | Diagnostic tones, host beep, and development prompts are permitted on a debug path. They do not satisfy SC-07 and must not be what `P-01` plays in a scored run. |
| `AR-36` | Spotify/music, when present, shares this same analog output path (ADR-11). Supported Spotify request types, device, auth, and retries are a later slice. This slice only requires that music is `LP-08-MUSIC` on the same speaker, interruptible by `AR-40`. |
| `AR-37` | Authored playback level is a later registered gain/file pair. This paper does not set SPL. |

## 5. Onset, stop, cancel, degrade

| ID | Requirement |
|---|---|
| `AR-40` | `AudioPlay` / `AudioStop` carry `perf_id`, `perf_epoch`, and `cue_id` (IR-01). Stop completion is a distinct event. |
| `AR-41` | Audio `source_onset` is the playback callback or device timestamp of the first submitted/played buffer (IR-06). Dispatch time is not onset. |
| `AR-42` | After cancel, higher-priority intent, reconnect, or C0 restart, a stale epoch cannot start or continue playback (IR-02). Restored output does not replay a cancelled chirp, alarm, or track (`PB-AUDIO-OUT`). |
| `AR-43` | Safety/E-stop/inhibit must not wait for a sample to finish. Mute/off is deterministic. Audio is not proof of a safe electrical state. |
| `AR-44` | Underrun, missing device, and decoder failure are machine-readable outcomes (IR-09: unavailable/degraded, audio underrun). The composer takes the registered `OX-DENY(audio)` branch. Absence of sound is not logged as success. |
| `AR-45` | `A-fail` is the only character motif for user-facing audio failure. It must not be confusable with `A-affirm` or `A-wake-rise`. Asset production is later; the ID and the non-confusion rule are now. |

## 6. Simultaneous capture and playback

| ID | Requirement |
|---|---|
| `AR-50` | Capture and playback operate at the same time in registered cases: wake listen during idle amp (`LP-07-LISTEN` + `LP-08-IDLE`), wake or barge-in during music (`LP-07-CAPTURE`/`LISTEN` + `LP-08-MUSIC`), chirp during listen (`LP-08-CHIRP` + `LP-07-LISTEN`). A path that must mute the mics to play, or mute the speaker to listen, cannot close ADR-11. |
| `AR-51` | The selected path must make the temporal relationship between captured mic samples and transmitted speaker samples recoverable (common or coherently disciplined clocks, or an equivalent documented timestamp model with bounded uncertainty). Unbounded independent drift is not acceptable if echo cancellation or playback-aware wake is required — and `AR-50` requires at least one of those. |
| `AR-52` | Primary speaker and array are both body-fixed, so head pose is not a variable in the loudspeaker-to-microphone echo path. Room change, body yaw, and speaker nonlinearity remain. |
| `AR-53` | M4's own astromech and music must not be accepted as a named wake (`AR-15` during self-playback). How that is achieved (AEC, barge-in gate, echo reference, energy gate) is an implementation choice scored later. The requirement is the false-wake behaviour. |
| `AR-54` | USB is **not banned**. A USB family must still meet `AR-03`, `AR-07`, `AR-50`, and `AR-51`. Failure to prove clock/echo adequacy is how that family loses, not a specsheet sentence. |

## 7. Contamination and packaging

Named interferers. Limits are later measured bars, not numbers in this paper.

| ID | Interferer | Requirement |
|---|---|---|
| `AR-60` | Loudspeaker | Structure-borne and airborne coupling into the four ports is a first-class measurement, not a surprise at RP-06. Isolation and grille design are RP-06/CAD; this slice requires the measurement obligation. |
| `AR-61` | Pi 5 Active Cooler | Fan is a documented `LG-01` noise source for `LG-07`. Ports stay away from cooler exhaust (sourcing matrix). A path that only works with the cooler unplugged is not ADR-11 evidence. |
| `AR-62` | Head servos | Body mounting exists to reduce neck-servo contamination relative to ear/head mics. Residual servo noise during `HM-03`/`HM-04` is still in the later acoustic matrix. |
| `AR-63` | Drive motors / wheel impacts / body resonance | Listen and capture quality may degrade while the base is in motion. Quality/availability must be **gated**, not silently trusted. Precise directional hearing during locomotion is not a Core requirement. |
| `AR-64` | Rigid array geometry | Final V1 prefers a common rigid PCB or equivalently rigid calibrated subassembly so port geometry stays calibrated. Breakout boards are allowed on the bench. |
| `AR-65` | Service | Speaker, amplifier, and microphone front end are named high-risk modules for SC-17-class access: replaceable without destroying the shell or unrelated assemblies. Exact procedure is RP-06. |

## 8. `makad-audio` service contract

Semantic contract on the already-chosen C0 Unix-domain IPC (`CA-07`/`CA-08`). Not a protobuf schema. Not code.

| ID | Requirement |
|---|---|
| `AR-70` | `makad-audio` is the only C0 owner of the capture device, the playback device, the wake front end, and astromech/music rendering. Other services request play/stop and subscribe to proposals/events. |
| `AR-71` | It has **no** direct actuator access. It cannot send `HEAD_GOAL`, `BASE_GOAL`, `FACE_STATE`, or `LIGHT_STATE`. |
| `AR-72` | Audio-channel death or restart degrades independently. `makad-core`/`makad-hwd` continue; the composer takes `OX-DENY(audio)`. Loss of audio is not a motor-inhibit by itself. |
| `AR-73` | Minimum event surface: device availability/frame-age; listen/capture/off/fault mode; wake proposal (name-form ID, confidence/quality if the engine supplies one, timestamp); wake reject; capture start/end; `AudioPlay` accept/deny; `source_onset`; progress/complete; `AudioStop` complete; underrun; stale-epoch reject. |
| `AR-74` | Join keys are `perf_epoch` + `cue_id` + channel, plus C0 boot/session for capture events that have no performance yet (sleep listen). Clock proximity is not the join key. |
| `AR-75` | Bounded logging (`CA-16`). Audio samples are not a required runtime log payload. If raw audio is retained for a scored run, it is an explicit capture config, not the default black box. |
| `AR-76` | An RP-04 timing stand-in (GPIO beep, host beep, virtual callback) may implement `AR-40`…`AR-44` and `AR-73` play/stop events. It does not implement `AR-01`…`AR-07`, `AR-50`…`AR-53`, or `AR-60`…`AR-63`, and cannot be cited as ADR-11 evidence. |

## 9. Explicitly out of this file

| Topic | Where it lives |
|---|---|
| Phrase list, paraphrases, unsupported/ambiguous cases | Later RP-05 corpus slice |
| Wake-word / ASR / NLU product choice | Later engine slice |
| Spotify request types, auth, device, timeouts | Later service slice; SC-TBD-17 |
| Astromech WAV/synth assets and observer comprehension bar | Later; SC-TBD-13 |
| DOA bearing/uncertainty API | ADR-13 / CAND-01, not Core |
| Numeric G01–G05 | [`gates.md`](gates.md) candidates; freeze only before scored data |
| Power numbers | `power-energy-ledger.md` `LG-07`/`LG-08` `E` rows |
