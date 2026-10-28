# RP-02 Load Model — Profiles, Time Scales and Evidence Contract

| Field | Value |
|---|---|
| Status | **Registered Part-1 profile vocabulary v0.3 — builder-approved 2026-09-15; numeric waveform bindings remain open until real or admissible substitute loads are frozen for a run.** |
| Owner | Project builder |
| Created / revised | 2026-09-14 / 2026-09-16 |
| Authority | `state-register.md`; `../../01-system/system-design-brief.md` AD-08 and §7; `intent.md` |
| Numeric source of truth | `../../01-system/power-energy-ledger.md` — all current, power, energy, loss and temperature values live there |
| Evidence classes | `W` exact measured hardware/run; `D` manufacturer source; `E` estimate or substitute; `U` unknown/unselected, never zero |

This file defines **what waveform or duty a state asks each load group to produce**. It does not repeat amperes or watts. A qualification case cites profile IDs from here; its run configuration binds them to hardware and the canonical ledger supplies the numeric envelope.

## 1. Required fields for every scored profile

| Field | Meaning |
|---|---|
| ID/revision | Stable identity; changes after registration create a new revision |
| Hardware/config | Exact SKU, firmware, rail, voltage, gain/brightness/trajectory and fixture |
| Preconditions | Temperature, state of charge, prior hold and enable state |
| Trigger/termination | Reproducible start; completion, timeout or cancellation |
| Mean and RMS | Sustained electrical/thermal demand |
| Peak and percentile | Maximum plus distribution across repetitions |
| Peak duration/slew | Width and rise/fall rate |
| Repetition/duty | Events per interval and recovery time |
| Regeneration/inrush | Signed current or rail overvoltage where relevant |
| Limits | Rail, current, temperature and abort conditions |
| Evidence | `U/E/D/W`, source/run ID, uncertainty and instrument rate |

## 2. Time-scale classes

| Class | Window | Primary concern | Minimum method |
|---|---:|---|---|
| `TB-1` | ≤10 ms | Contact bounce, converter response, inrush edge, bus disturbance | Oscilloscope/equivalent transient capture |
| `TB-2` | >10–500 ms | Servo/motor launch, reversal/brake, audio crest, brownout | Triggered load-end voltage/current plus reset/fault logs |
| `TB-3` | >0.5 s–5 min | RMS current and regulator/motor/amp heat | Synchronized branch power ≥10 Hz, temperature ≥1 Hz; faster event windows |
| `TB-4` | Full duty/endurance | Energy, reserve, heat soak, drift and repetitions | Input-energy integration plus branch totals, temperatures and event counts |

A profile may occupy several classes: music has `TB-2` crests inside a `TB-3` RMS condition.

## 3. Load-group boundary

| Group | Boundary | Selection state |
|---|---|---|
| `LG-01` | Body Raspberry Pi 5 2 GB | Selected under `RP02-P2-REG-02`; exact workload, storage, cooling and power-entry configuration unmeasured |
| `LG-02` | C2 + servo-bus transceiver | ESP32-S3-Zero selected; installed power unmeasured |
| `LG-03Y/P/R` | Head servo branches, separately observable | Family unselected; C01 is paper comparison only |
| `LG-04` | Drive motors + driver | Unselected; RP-03 owns real profiles |
| `LG-05` | Display + status light | Display selected; light working-selected 2026-09-26: WS2812B-2020 on D1 3.3 V, ≤ 36 mA full white (`D`) ([selection](../RP-06-cad/peripheral-selection.md) §3) |
| `LG-06` | Camera via SBC port | Camera Module 3 Wide selected; current unmeasured |
| `LG-07` | Mics + audio front end | Working-selected 2026-09-26: 4 × IM73D122V01 + 2 × ADAU7002 from the Pi header 3.3 V, ≈ 20 mW `E` (RP-05 `BD-A04`/`A05`) |
| `LG-08` | Speaker + amplifier | Working-selected 2026-09-26: MAX98357A + Visaton K 50 WP 8 Ω on `PB-AUDIO-OUT` 5 V; idle ≈ 14 mW, peak ≈ 2.1 W `E` (RP-05 `BD-A06`) |
| `LG-09` | Conversion/distribution loss | Derived residual; never commanded |
| `LG-10` | Selected ESP32-S3-DevKitC-1-N8 C3 prototype + obstacle/edge sensing | Controller identity fixed by `RP02-P3-REG-01/02`; RP-03 owns sensor binding and measured profiles |

## 4. Named profiles

### `LG-01` main compute

| ID | Condition | Class / closure |
|---|---|---|
| `LP-01-OFF` | Rail physically removed | Verify physical zero; missing hardware is not off |
| `LP-01-BOOT` | Cold power through services/supervisor ready | TB-1/2/3; SBC `D`, then cold-start `W` distribution |
| `LP-01-IDLE` | Services/logging/network alive; no active perception/NLU burst | TB-3; candidate `D`, then `W` |
| `LP-01-PERCEPTION` | Camera + representative person detection/tracking | TB-2/3; RP-07 workload and `W` |
| `LP-01-AUDIO` | Wake/request capture and interaction processing | TB-2/3; RP-05/RP-07 |
| `LP-01-SERVICE` | One registered external request in flight, including network, timeout and response parsing | TB-3/4; endpoint/timeout/retry policy stated |
| `LP-01-CANCEL` | Cancel, duplicate/late-result rejection and return-to-idle processing | TB-2/3; exact action type and cancellation phase stated |
| `LP-01-COEXIST` | Credible perception + audio + behaviour + logging/network | TB-2/3; not a synthetic CPU maximum |
| `LP-01-SHUTDOWN` | Log flush and orderly power-down | TB-2/3; `W` shutdown runs |

### `LG-02` C2 controller

| ID | Condition | Class / closure |
|---|---|---|
| `LP-02-OFF` | C2 logic rail physically removed | Verify final shutdown only; not valid for charging when C2 is minimum supervisor |
| `LP-02-BOOT` | Reset/boot inhibited through handshake | TB-1/2; DevKitC first, Zero later; bridge overhead separate |
| `LP-02-IDLE` | Link/heartbeat/health, no trajectory | TB-3; Espressif `D`, exact-board `W` |
| `LP-02-TRAJ` | Candidate 200 Hz loop, 3-axis sync write/read | TB-2/3; G05 |
| `LP-02-LINKSTRESS` | Maximum admissible frames/CRC/queue rejection while loop active | TB-2/3; G05/F-04/F-14 |
| `LP-02-FAULT` | Watchdog/fault processing and health while inhibited | TB-2/3; G04 |

Installed C2 Wi-Fi is disabled; Wi-Fi transmit is not a credible profile.

### `LG-03Y/P/R` head servos

| ID | Condition | Class / binding |
|---|---|---|
| `LP-03-OFF` | Motor rail absent / torque unavailable | Hard-stop, charging, inhibited |
| `LP-03-PWRRESTORE` | Rail reapplied while C2 inhibited | TB-1/2; zero stored motion; capture inrush |
| `LP-03-HOLD` | Attentive hold at registered pose | TB-3/4; **not used during sleep** |
| `LP-03-SLEEP` | HM-02 descent to rest | TB-2/3; trajectory/end support stated |
| `LP-03-WAKE` | HM-03 three-axis rise | TB-2; storyboard variant stated |
| `LP-03-SEARCH` | HM-04 sector sweeps/holds | TB-2/3; angles, pauses, count |
| `LP-03-ORIENT` | HM-05 decisive acquisition orient | TB-2; start/target pose |
| `LP-03-TRACK` | Online small yaw/pitch corrections | TB-2/3; distribution, rate, deadband |
| `LP-03-GESTURE` | HM-06/07/09/11 stitched reversals | TB-2/3; exact motion ID |
| `LP-03-MICRO` | HM-08 quick laugh pulses | TB-2/3; distinct backlash workload |
| `LP-03-STARTLE` | HM-15 simultaneous recoil/stop | TB-2; 180–250 ms candidate window |
| `LP-03-BRAKE` | HM-18 cancellation to bounded hold | TB-2; starting motion stated |
| `LP-03-THERMAL` | Registered busy minute repeated | TB-3/4; RP-01 sequence/limits |
| `LP-03-STALLREF` | Current-limited restrained stall reference | TB-2; bench protection only, never behaviour |

C01's 1.80 A at 5 V is stall `D`, not an operating peak. Family, rail, internal-acceleration current and physical profiles remain open.

### `LG-04` drive

| ID | Condition | Class / binding |
|---|---|---|
| `LP-04-OFF` | Driver disabled or motor domain absent | Independently verify for tabletop/inhibit/charging |
| `LP-04-PWRRESTORE` | Rail reapplied while base control inhibited | TB-1/2; zero stored motion; capture inrush |
| `LP-04-STEADY` | Representative low-speed straight/turn following | TB-3; mass, surface and speed stated |
| `LP-04-LAUNCH` | Start from rest inside RP-03 envelope | TB-2; channels separate |
| `LP-04-REV` | Decelerate through zero and reverse | TB-2; signed current/rail maximum |
| `LP-04-BRAKE` | Stop from registered speed | TB-2; latency/regeneration |
| `LP-04-SPIN` | Excited spin plus complete settle | TB-2/3; peak interval separate from action |
| `LP-04-BLOCKEDREF` | Current-limited blocked-wheel reference | TB-2; stress only |

An electronic-load substitute can reproduce a current-time trace but cannot prove inductive/regenerative behaviour; it remains `E`.

### `LG-05` display/status light

| ID | Condition | Class / binding |
|---|---|---|
| `LP-05-OFF` | Display logic and backlight rails removed | Verify final shutdown; distinct from a black frame |
| `LP-05-BOOT` | Board boot, assets and backlight enable | TB-1/2; firmware/brightness |
| `LP-05-DIM` | Quiet animated face at idle brightness | TB-3/4 |
| `LP-05-ACTIVE` | Animated face at normal brightness/FPS | TB-3 |
| `LP-05-WAKE` | Backlight/face/status-light transition | TB-1/2; step captured |
| `LP-05-UTILITY` | Time/timer/alarm/Spotify view | TB-2/3 |
| `LP-05-MUSIC` | Registered eye-vibe animation | TB-3; actual animation |
| `LP-05-FAILURE` | Bounded clarification/failure face plus camera-side status-light indication | TB-2/3; never used as proof that the hazardous output stopped |
| `LP-05-CHARGE` | Local charging/status display at bounded brightness | TB-3/4; display-local assets plus minimum charge telemetry, no SBC renderer |
| `LP-05-FULLREF` | Full-brightness worst-pattern reference | TB-3; stress only unless UI uses it |

### `LG-06` camera

| ID | Condition | Class / binding |
|---|---|---|
| `LP-06-OFF` | Stream disabled | Required in quiet sleep and charging |
| `LP-06-STREAM` | Household-light stream at registered mode | TB-3/4; resolution/FPS/exposure |
| `LP-06-TRACK` | Stream during tracking workload | TB-2/3; correlate SBC power |
| `LP-06-AF` | Autofocus travel/refocus | TB-2; focus mode/target change |

### `LG-07` microphones/front end

| ID | Condition | Class / binding |
|---|---|---|
| `LP-07-OFF` | Microphones/front end unpowered or explicitly disabled | Required while charging; verify the implemented isolation state |
| `LP-07-LISTEN` | Continuous named-wake listening | TB-3/4; channel count/rate/interface |
| `LP-07-CAPTURE` | Full request-capture/processing path | TB-2/3 |
| `LP-07-FAULT` | Missing sensor detection | TB-2; not a zero-power assumption |

### `LG-08` speaker/amplifier

| ID | Condition | Class / binding |
|---|---|---|
| `LP-08-OFF` | Amplifier disabled | True shutdown only |
| `LP-08-IDLE` | Amplifier enabled, silent | TB-3/4; quiescent draw |
| `LP-08-CHIRP` | Registered acknowledgement/startle file | TB-2; file/gain/load |
| `LP-08-ALARM` | Registered timer/alarm pattern | TB-2/3; repetition/cancel |
| `LP-08-MUSIC` | Three-minute registered excerpt | TB-3; RMS and temperature |
| `LP-08-CREST` | Highest crest in registered material | TB-2; waveform, not “sustained peak” |
| `LP-08-SINEREF` | Fixed-tone/resistive-load reference | TB-2/3; bench stress only |

### `LG-10` base MCU/safety sensing

| ID | Condition | Class / binding |
|---|---|---|
| `LP-10-OFF` | Base controller and sensor rail removed | Required while charging and after final shutdown |
| `LP-10-BOOT` | MCU/sensors boot, driver inhibited | TB-1/2; exact RP-03 sensor set |
| `LP-10-IDLE` | Health and edge/obstacle sensing stopped | TB-3/4; emitter schedule |
| `LP-10-MOTION` | Encoder/control/safety at active rates | TB-2/3 |
| `LP-10-OBSTACLE` | Maximum registered obstacle-sensor schedule plus local clamp/stop processing | TB-2/3; obstacle geometry and approach speed stated |
| `LP-10-EDGE` | Maximum edge-sensor schedule | TB-2/3; tabletop proof |
| `LP-10-FAULT` | Sensor-fault processing | TB-2; observable without motion |

## 5. Minimum profile binding by case

| Case | Required dominant profiles |
|---|---|
| `CC-01` | `LP-01/02/05/10-BOOT`; `LP-03/04-OFF` |
| `CC-02F/T` | `LP-01-IDLE`, `LP-02-IDLE`, `LP-03/04-OFF`, `LP-05-DIM`, `LP-06-OFF`, `LP-07-LISTEN`, `LP-08-IDLE`, `LP-10-IDLE`; `CC-02T` additionally verifies drive inhibit |
| `CC-03` | `LP-03-WAKE`, `LP-05-WAKE`, `LP-08-CHIRP`, `LP-01-PERCEPTION`, `LP-06-TRACK` |
| `CC-03N` | `CC-02F/T` baseline remains unchanged; non-wake stimuli must not start any wake/motor profile |
| `CC-04` | `LP-01-PERCEPTION`, `LP-03-SEARCH/ORIENT`, `LP-05-ACTIVE`, `LP-06-TRACK` |
| `CC-05` | Exact `LP-03-GESTURE/MICRO` plus awake baseline |
| `CC-06` | `LP-03-STARTLE`, `LP-05-WAKE`, `LP-08-CHIRP`; `LP-04-OFF` |
| `CC-07A/B/C` | Capture; bounded external wait; response/annunciation profiles respectively |
| `CC-07D` | `LP-01-AUDIO/SERVICE`, `LP-05-FAILURE`, optional `LP-08-CHIRP`; no new motor profile |
| `CC-07E` | Starting action profiles → `LP-01-CANCEL`, applicable `LP-03/04-BRAKE`, then legal attentive/off profiles |
| `CC-08` | `LP-08-MUSIC` + recorded crest, `LP-05-MUSIC`, `LP-07-CAPTURE`, optional head motion |
| `CC-09` | `LP-01-PERCEPTION`, `LP-03-TRACK`, `LP-04-STEADY`, `LP-06-TRACK`, `LP-10-MOTION` |
| `CC-09C` | Search/orient as needed, then `CC-09` drive baseline + `LP-04-BRAKE` at the stopping band |
| `CC-09R` | `CC-09` → `LP-04-BRAKE`; `LP-01-PERCEPTION` + `LP-03-SEARCH/ORIENT` while stopped; resume only after fresh authorization |
| `CC-10A/B` | `CC-09/09C` plus `LP-04-LAUNCH` or `LP-04-REV/BRAKE` |
| `CC-10C` | `CC-09/09C` plus `LP-10-OBSTACLE` and `LP-04-BRAKE` or a separately registered redirect profile |
| `CC-11` | `LP-04-SPIN`, `LP-10-MOTION`, `LP-05-ACTIVE`, optional chirp |
| `CC-12A` | Worst permitted non-drive `CC-05/07C/08` variant plus verified `LP-04-OFF` |
| `CC-12B` | Attentive baseline plus `LP-04-OFF`; rejected drive/spin requests are logged stimuli, not load profiles |
| `CC-12C` | `LP-10-EDGE` plus explicitly armed minimum-speed drive and `LP-04-BRAKE`; caught tabletop fixture required |
| `CC-13H/D`, `CC-14` | Starting case followed by low/critical policy and applicable brake profiles |
| `CC-15` | Charger/power-path profile added in Part 2; `LP-01-OFF`, `LP-02-IDLE`, `LP-03/04-OFF`, `LP-05-CHARGE`, `LP-06/07/08-OFF`, `LP-10-OFF` |
| `CC-16` | Starting profiles → `LP-03-SLEEP`, `LP-01-SHUTDOWN`, then `LP-01/02/03/04/05/06/07/08/10-OFF` |
| `CC-17` | `LP-01-IDLE`, `LP-02-IDLE/TRAJ`, `LP-03-HOLD/MICRO` at registered sparse duty, `LP-05-DIM/ACTIVE`, `LP-06-STREAM`, `LP-07-LISTEN`, `LP-08-IDLE`, `LP-10-IDLE` |
| `CC-18` | Registered performance baseline with one eligible channel replaced by its `OFF`, inhibited or fault profile; remaining legal profiles stay synchronized |
| `CC-PEAK-01` | `LP-01-COEXIST`, head track, drive reversal/brake, active face/camera, audio crest, base safety |
| `ST-01` | `LP-01-COEXIST`, head startle, drive reversal, display wake, audio crest, base safety |

## 6. Aggregation rules

1. Sum only profiles permitted concurrently by `state-register.md`.
2. Preserve axes/branches until after voltage-drop and fuse analysis.
3. Use signed source current for braking/regeneration; record rail maximum and minimum.
4. Use registered waveform alignment. Adding independent maxima is an `ST` stress bound, not an operational prediction.
5. Thermal uses RMS/mean over stated duty, not the highest sample.
6. Energy uses measured `v(t)·i(t)`; nominal voltage × nameplate current is only `E`.
7. `LG-09 = input power − aligned load powers`; it stops being a blanket percentage once `W` data exist.
8. Margin is reported at component terminals, not only the distribution board.

## 7. Measurement dependency register

| Priority | Unknown | Why it blocks | Owner |
|---|---|---|---|
| P0 | Servo family/rail/current waveforms | Largest head transient, converter and harness | RP-01/RP-02 |
| P0 | SBC boot/perception/coexistence | Compute rail and sustained heat | RP-02/RP-07 |
| P0 | Drive launch/reversal/brake/regeneration | Whole-robot peak and brownout order | RP-03 |
| P1 | Display boot/dim/active/wake/music | Known hardware; cheap early `W` evidence | RP-02/RP-04 |
| P1 | Camera stream/AF and wake-from-off latency | Perception load and consequence of SD-01 | RP-02/RP-07 |
| P1 | Audio idle/RMS/crest at authored level | Sustained heat and transient overlap | RP-05/RP-06 |
| P1 | Base MCU/sensor-emitter duty | Logic load/tabletop proof | RP-03 |
| P2 | Pack/charger profile | `CC-15` and runtime rehearsal | RP-02 Phase C |

## 8. Registration record

| Field | Registered value |
|---|---|
| Registration | `RP02-P1-REG-01` |
| Date / approval | 2026-09-15; explicit builder approval in the project conversation |
| Revision | v0.3 |
| Scope | Every `LP-01-*` through `LP-08-*` and `LP-10-*` profile defined in §§3–4, their time-scale classes, case bindings and aggregation rules |
| Numeric status | Waveform values remain `U`, `E`, `D` or later `W` as recorded in the system ledger; approval does not promote estimates to measurements |
| Scored-run condition | Each required profile must have a frozen real-load record or admissible substitute-equivalence record before its case can be scored |

Post-registration implementation note, 2026-09-16: `RP02-P3-REG-01/02` selected the ESP32-S3-DevKitC-1-N8 as the current C3 prototype board, correcting the initial N8R8 suffix to preserve GPIO35–37. This binds the controller identity behind `LG-10` but does not alter any registered `LP-10-*` semantics, select the safety sensors or promote a numeric waveform.
