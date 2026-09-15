# RP-02 Operating-State and Concurrency Register

| Field | Value |
|---|---|
| Status | **Registered Part-1 baseline v0.4 — builder-approved 2026-09-15. IDs, policies, cases and `MD-01` definition are frozen; run-specific hardware/configuration and open numeric thresholds remain to be registered before scored runs.** |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-15 |
| Authority | `../../01-system/risk-prototype-plan.md` v1.12 §RP-02; `../../01-system/power-energy-ledger.md` coexistence invariant |
| Load-profile source | `load-model.md`; numeric current, energy and heat remain exclusively in `../../01-system/power-energy-ledger.md` |
| Behaviour sources | `../RP-01-head/intent.md` HM-00…HM-18; `../../00-foundation/core-interaction-scenarios.md`; `../../01-system/system-design-brief.md` §6 |

This register defines the conditions the electrical/control backbone must survive. It separates seven things that the unregistered v0.1 draft mixed together:

1. **operating permissions** — what motion is allowed;
2. **energy and health overlays** — constraints that coexist with behaviour;
3. **person continuity** — no candidate, candidate, selected, temporarily lost, reacquiring or lost;
4. **per-action lifecycle** — proposed, accepted, active, cancelling, completed or failed;
5. **behavioural operating states** — what Makad does for a sustained interval;
6. **transient events** — short electrical/mechanical changes superimposed on a state;
7. **qualification cases** — exact combinations exercised on the rig.

Makad is never represented by one giant enum. A testable condition is:

`<operating mode, energy state, behaviour state, person continuity, per-action lifecycle, per-subsystem health, zero or more active events>`.

Only the qualification cases in §7 select meaningful vectors from that space.

## 1. Governance rules

1. **The Part-1 baseline below is registered.** §11 records the exact revision, approved identifier families and builder approval before scored data exist.
2. **Registered IDs are now append-only.** A semantic change creates a new ID or document revision with an explicit supersession record. The old `S00…S17` proposals were never registered, so v0.2 retired them without superseding evidence; §10 retains a crosswalk.
3. **Every state and event traces to a Core scenario, safety requirement or RP-01 motion.** Untraceable stress belongs under `ST-xx`, not in the operating model.
4. **Load letters are forbidden as definitions.** `Idle`, `average` and `peak` are summaries, not reproducible profiles. Cases cite named `LP-xx-*` profiles from `load-model.md`.
5. **Transitions are scored.** Brownouts, inrush and stale work usually occur while entering or leaving a state.
6. **Faults are overlays, not states.** `fault-matrix.md` injects one fault into a qualification case.
7. **Unknown hardware remains non-zero.** A missing current, duration or limit is `U`; it is never treated as zero for sizing.
8. **Registration freezes `MD-01`.** A later change creates `MD-02`; it never silently edits the workload used by earlier evidence.

## 2. Operating modes and permissions

These define authority, not a particular electrical load.

| ID | Mode | Base motion | Head motion | Entry / exit rule | Source |
|---|---|---|---|---|---|
| `OM-01` | Floor | Allowed inside validated envelope | Allowed | Builder selects **Floor mode** in the control app for the current session; local controller accepts/latches it only after safety readiness; boot/reset/app-link loss resolves to `OM-03` | SCOPE-09/10/12/20/21; CON-09/19; SD-03 |
| `OM-02` | Tabletop | **Inhibited by default**; separately armed calibration motion may be added later | Allowed inside validated head envelope | Builder selects **Table mode** in the control app; local controller enforces drive inhibit independently of later app/network health | SCOPE-11; AD-07; SD-03 |
| `OM-03` | Motion inhibited | Forbidden | No new trajectory; only registered safe-settle action when motor power remains | Default after boot, reset, stale heartbeat, critical energy or unsafe health; fresh enable nonce required to leave | AD-04; SC-15 |
| `OM-04` | Hard stop | Physically unpowered | Physically unpowered | E-stop removes motor domain while logic stays powered; release returns to `OM-03`, never directly to `OM-01/02` | CON-P02; PA-01; F-12/F-13 |
| `OM-05` | Bench/service | Only explicitly armed test channel | Only explicitly armed axes | Fixture, session E-stop check and recorded run configuration required | `workbench.md`; RP02-G01 |
| `OM-06` | Charging | Forbidden | Forbidden; head rests down with torque off | Charge input present; display and minimum charge supervision stay on, while camera, ordinary SBC workload, microphones/audio and motor domain are off | CON-TBD-09; PA-09; SD-04 |

### Permission invariants

- `OM-03`, `OM-04` and `OM-06` cannot coexist with any drive profile other than `LP-04-OFF`. `OM-02` has the same rule during ordinary operation; its only exception is the separately armed, minimum-speed, caught-fixture calibration case `CC-12C`, which never grants ordinary come/follow/spin authority.
- Releasing E-stop, reconnecting a cable, replacing a battery or recovering a controller always enters `OM-03`.
- `OM-01/02` require current mode evidence; missing or contradictory evidence resolves to `OM-03`.
- App selection is a command to the local authority, not the safety interlock itself. Floor permission is session-scoped and is never restored automatically after boot, reset or link loss.
- Expression never overrides a permission mode. Eyes/audio may communicate an inhibit while motors remain disabled.

## 3. Energy, health, continuity and action overlays

### 3.1 Energy

| ID | State | Required policy |
|---|---|---|
| `EN-01` | Normal | All actions permitted by operating mode and current health. |
| `EN-02` | Low | New locomotion and peak gestures rejected; active locomotion brakes; display/audio remain available at bounded levels; no automatic resumption after recovery. Threshold remains open under SC-TBD-10. |
| `EN-03` | Critical | Enter `OM-03`, perform a bounded settle only if margin permits, persist the reason, then execute `EV-14`. Threshold must be above uncontrolled rail collapse. |
| `EN-04` | Charging | Requires `OM-06`; local display shows charging state from minimum charge supervision. Camera, ordinary interaction compute, audio and both motor branches remain off. |

### 3.2 Per-subsystem health

| ID | Meaning | Consequence |
|---|---|---|
| `HL-01` | Available | Profile may be commanded normally. |
| `HL-02` | Degraded | Capability remains bounded but reports reduced quality or margin. |
| `HL-03` | Unavailable | Dependent behaviour is denied/stopped; unrelated safe channels may continue. |
| `HL-04` | Unsafe | Hazardous outputs are inhibited immediately; fresh enable required after recovery. |

### 3.3 Person continuity

`PC` is independent of behaviour. A timer can remain active with no selected person; a selected person can become temporarily lost while `BS-09` is braking. Identity/track evidence is timestamped and never inferred from a behavioural label.

| ID | Meaning | Required policy |
|---|---|---|
| `PC-00` | Not applicable | No person-dependent action is authorized. |
| `PC-01` | No candidate | Search may be proposed; approach/follow is forbidden. |
| `PC-02` | Candidate, not selected | Attention may preview a candidate; locomotion toward that person is forbidden. |
| `PC-03` | Selected and fresh | Person-dependent attention/come/follow may be authorized within mode and safety limits. |
| `PC-04` | Temporarily lost | Preserve selected identity for the registered grace interval; brake base motion and do not switch targets. |
| `PC-05` | Reacquiring | Bounded search for the same selected identity; base remains stopped unless a later RP-07 policy explicitly proves otherwise. |
| `PC-06` | Lost / selection expired | Clear selected authority; enter bounded failure/attentive state. A new candidate requires explicit selection. |

### 3.4 Per-action lifecycle

`AL` is maintained **per long-running action**, so a timer can remain active while music or attention changes. It applies to performances, time/timer/alarm requests, Spotify playback, come and follow.

| ID | Meaning | Required policy |
|---|---|---|
| `AL-00` | Not applicable / no instance | No action instance exists. |
| `AL-01` | Proposed | Intent exists but has not received permission/resources; no physical execution. |
| `AL-02` | Accepted | Authority and initial conditions are valid; execution may be scheduled. |
| `AL-03` | Active | Current work is executing with a live validity deadline and observable feedback. |
| `AL-04` | Cancelling | New output is suppressed; current physical work brakes/settles; late results cannot reactivate it. |
| `AL-05` | Completed | Completion is recorded once; duplicate completion is ignored. |
| `AL-06` | Failed | Failure reason is exposed; no false success; retry creates a new action instance. |

## 4. Behavioural operating states

These are dwellable semantic states. Short movements and power steps are in §5.

| ID | State | Entry | Exit / timeout | Normally active groups | Hazard | Source |
|---|---|---|---|---|---|---|
| `BS-00` | Logic alive, motion inhibited | Boot reaches supervision or recovery returns to inhibit | Fresh handshake/enable, hard stop or shutdown | LG-01/02/05/06/07/10 as configured; LG-03/04 off | None; proves diagnosis while motion is dead | SC-15/18 |
| `BS-01` | Quiet idle / sleep | Commanded sleep completes with head down | Wake, failure indication, low/critical energy or shutdown | Wake listening, dim face and health; **camera off; all head-servo torque off** | None from actuators; passive rest must be mechanically safe | SCOPE-07/16; HM-00/02; SD-01/02 |
| `BS-02` | Attentive idle / procedural aliveness | Wake/acquisition completes or action settles | Request, search, music, locomotion, sleep or fault | Camera/perception idle, animated face, listening, small bounded head corrections | Low-energy head motion | HM-01; SC-09 |
| `BS-03` | Person search | `PC-01/02` discovery or `PC-04/05` same-person reacquisition | `PC-03`, cancellation, expiry to `PC-06` or registered timeout | Perception, camera, face, listening and search-sector events | Head sweep; base search not implied | HM-04; Scenario 2; RP07 |
| `BS-04` | Person tracking / attention | `PC-03` selected and fresh | `PC-04/06`, cancellation, request, sleep or fault | Tracking compute/camera plus online head corrections | Sustained small head motion | HM-05; SC-08; RP07 |
| `BS-05` | Spoken-input capture | Wake/attention valid and capture begins | End-of-utterance, cancel or capture timeout | Mics, SBC audio/interaction, attentive face/head | Attentive corrections only | SC-05/06/22/23 |
| `BS-06` | External-service wait | Valid request reaches `AL-03` with external work pending | Response, `AL-04` cancellation or timeout to `AL-06` | SBC/network; bounded face/head that do not fabricate success | Attentive hold only | CON-11; CON-P04; RP05 |
| `BS-07` | Response / utility presentation | Valid result, clarification or timer/alarm event | `AL-05/06`, `AL-04` cancellation, display timeout or fault | Utility/face display, astromech audio, optional bounded gesture | Head motion if authored | Scenario 1 utilities; RP05 |
| `BS-08` | Music playback / vibe | Playback reaches `AL-03` | `AL-04/05/06`, low energy or safety pre-emption | Audio RMS, face animation, capture, optional small head motion | Sustained heat/audio; **base motion not implied** | SCOPE-19; SC-23; RP05 |
| `BS-09` | Come/follow | `OM-01`, `PC-03`, local safety ready and action `AL-02/03` | `AL-04/05/06`, `PC-04/06`, obstacle/safety inhibit or low energy | Tracking, drive, base safety, head corrections, status outputs | Sustained base/head motion | SCOPE-20; Scenario 2; RP07 |
| `BS-10` | Bounded failure indication | A capability fails or hazardous action is already inhibited | Acknowledgement, timeout, recovery to current intent, sleep or shutdown | Legal expressive channels only | None; never claims success | SDB failure priorities |
| `BS-11` | Charging display | `OM-06 + EN-04` accepted | Charge removed, complete, faulted or power-down requested | Display + minimum charge/pack supervision only | No motor hazard; charge/battery thermal hazard remains | SD-04; PA-09 |

### Builder state decisions — 2026-09-15

| ID | Decision | Consequence / remaining evidence |
|---|---|---|
| `SD-01` | Camera does not stream while M4 is asleep. | `BS-01` binds `LP-06-OFF`; wake-to-first-usable-track latency must include camera start and be measured later. |
| `SD-02` | All head-servo torque is off in sleep and the head rests down. | `BS-01` binds `LP-03-OFF`, not a hold-current estimate. RP-01 must prove the passive rest has no damaging fall, cable pull or hard-stop impact. |
| `SD-03` | V1 floor/table mode is selected manually in the Makad control app/web app. | Makeshift V1 evidence is an explicit, session-scoped operator command accepted by local control. Boot/reset/app-link loss returns to `OM-03`; the app cannot directly energize motors. Later automatic placement evidence may supersede this. |
| `SD-04` | The display remains on while charging. | `OM-06` keeps display + minimum charge supervision alive; motors, camera, normal interaction/audio and ordinary SBC workload stay off. Exact charger/power-path hardware belongs to Part 2. |

## 5. Transient events

An event overlays a behavioural state and has an exact onset, duration and completion/failure result in a qualification case.

| ID | Event | Allowed state(s) | Required ordering | Dominant profiles | Source |
|---|---|---|---|---|---|
| `EV-01` | Cold boot / rail inrush | Power-off → `BS-00` | Motors stay inhibited until limits, mode and fresh enable are accepted | `LP-01/02/05/10-BOOT` | SC-18 |
| `EV-02` | Enable handshake | `BS-00` | `HELLO → LIMITS_SET → mode valid → fresh ENABLE`; stored goals never execute | Logic/link; motors off until completion | AD-04 |
| `EV-03` | Wake rise | `BS-01` → `BS-02/03/04` | Display/audio may lead; camera/perception may run; **search sweep waits for wake completion** | `LP-03-WAKE`, `LP-05-WAKE`, `LP-08-CHIRP`, possible perception | HM-03; Scenario 1 |
| `EV-04` | Search-sector turn | `BS-03` | Gaze cue → sector move → hold; acquisition cancels remaining sectors | `LP-03-SEARCH`, perception/camera | HM-04 |
| `EV-05` | Acquire/orient | `BS-03` → `BS-04` | One decisive orient, then online corrections | `LP-03-ORIENT`, then `LP-03-TRACK` | HM-05 |
| `EV-06` | Authored head gesture | `BS-02/04/07/08` | Exact RP-01 trajectory and repetitions; safe stop pre-empts | `LP-03-GESTURE/MICRO` | HM-06…14/16/17 |
| `EV-07` | Startle/recoil | `BS-02/04/08`; during `BS-09` only after `EV-12` confirms stop | Eyes/audio may react immediately; **head recoil waits for base stop if propulsion was active** | `LP-03-STARTLE`, display/audio transient | HM-15; stability priority |
| `EV-08` | Utility/display transition | `BS-05/06` → `BS-07` | Bounded lifecycle; returns to face on completion/failure | `LP-05-UTILITY`, optional chirp | SC-22 |
| `EV-09` | Alarm/timer annunciation | Any safe non-shutdown state → `BS-07` | Safety pre-empts; cancellation explicit | `LP-05-UTILITY`, `LP-08-ALARM` | SC-22 |
| `EV-10` | Base launch | `BS-09` in `OM-01` | Local safety ready; acceleration inside RP-03 envelope | `LP-04-LAUNCH`, `LP-10-MOTION` | SC-11/24 |
| `EV-11` | Base reversal | `BS-09` in `OM-01` | Decelerate through zero before opposite torque | `LP-04-REV`, `LP-10-MOTION` | RP-03 |
| `EV-12` | Controlled brake/stop | `BS-09` or any active base action | Highest authority short of hard stop; completes before startle recoil/recovery | `LP-04-BRAKE`, `LP-10-MOTION` | SC-15 |
| `EV-13` | Excited spin | `BS-02/04` in `OM-01` | Explicit bounded action; no tabletop; settles before another base action | `LP-04-SPIN`, face, optional chirp | SCOPE-21; SC-25 |
| `EV-14` | Orderly shutdown | Any non-hard-stop state → off | Cancel → brake/settle → motor inhibit → persist logs → sign-off → logic off | `LP-03-SLEEP`, audio, falling logic profiles | HM-02; SC-18 |
| `EV-15` | E-stop assertion | Any motion → `OM-04` | Hardware motor-domain removal dominates choreography | Motor profiles collapse; logic continues | F-12 |
| `EV-16` | E-stop release / motor restoration | `OM-04` → `OM-03/BS-00` | No motion; stale queues flushed; fresh enable required | `LP-03/04-PWRRESTORE` | F-13 |
| `EV-17` | Cancel / interrupt / return-to-idle | Any `AL-02/03` action | Set `AL-04`; suppress new output, brake/settle physical channels, discard late/duplicate results, then record `AL-05/06` | Applicable `LP-03/04-BRAKE`, display/audio return, service work cancelled | SC-10; RP04/05 |
| `EV-18` | Selected-person evidence lost | `BS-04/09 + PC-03` | Set `PC-04`; base begins `EV-12`; preserve identity during grace period and never switch silently | Perception/search + `LP-04-BRAKE` if moving | SC-08/24; RP07 |
| `EV-19` | Same-person reacquisition | `PC-04/05` | Confirm same selected identity with fresh evidence before `PC-03`; new person requires a new selection | `LP-01-PERCEPTION`, `LP-03-SEARCH/ORIENT/TRACK`; drive remains stopped until authorized | Scenario 2; RP07 |
| `EV-20` | Local obstacle intervention | Any active base action | Local safety clamps drive before behaviour/network response; stop or redirect only inside registered RP-03 policy | `LP-04-BRAKE` or registered redirect + `LP-10-OBSTACLE` | SCOPE-12; SC-12; RP03/07 |
| `EV-21` | Tabletop edge intervention | Explicitly armed calibration motion in `OM-02` | Local edge authority stops inside caught/validated footprint; missing edge evidence inhibits motion | `LP-04-BRAKE`, `LP-10-EDGE` | SCOPE-11; SC-13; RP03 |
| `EV-22` | Semantic rejection / clarification | `BS-05/06` with ambiguous, unsupported or denied intent | No hazardous command is issued; expose clarification/failure without claiming success | `LP-01-AUDIO/SERVICE`, `LP-05-UTILITY`, optional `LP-08-CHIRP`; motors unchanged/off as required | Scenario 1 failure semantics; RP05 |

## 6. Transition contract

| From | Trigger | Intermediate requirement | To |
|---|---|---|---|
| Off | Power applied | `EV-01`; motors inhibited | `OM-03 + BS-00` |
| `BS-00` | Fresh enable with valid mode/limits | `EV-02`; queues empty | `BS-01/02` in `OM-01/02` |
| `BS-01` | Named wake accepted | `EV-03`; search waits for wake completion | `BS-04 + PC-03` if selection is fresh, else `BS-03 + PC-01/02` |
| `BS-01` | Non-wake or rejected invocation | No state-changing event or motor command | `BS-01` |
| `BS-03` | Person acquired and selected | `EV-05`; `PC-02 → PC-03` | `BS-04` |
| `BS-04` | Spoken request | `AL-01 → AL-02`; capture, external wait and response remain separate | `BS-05 → BS-06 → BS-07 → BS-04/02` with `AL-05/06` |
| `BS-04` | Come/follow | Mode, `PC-03`, local safety and action acceptance valid | `BS-09 + AL-03` |
| Any active action | Stop/cancel/higher-priority intent | `EV-17`; action becomes `AL-04` and physical channels brake/settle | `AL-05/06` plus current legal `BS` |
| `BS-04/09 + PC-03` | Selected-person evidence lost | `EV-18`; base stop precedes reacquisition movement | `PC-04`, then `PC-05 + BS-03` or `PC-06 + BS-10/02` |
| `PC-04/05` | Same person reacquired | `EV-19`; identity and freshness verified | `PC-03 + BS-04`; follow needs current `AL` authorization before motion |
| Any active base action | Obstacle detected | `EV-20`; local safety owns clamp | stopped/redirected within policy, or `OM-03 + BS-10` |
| `OM-02` calibration motion | Edge detected or edge sensing unavailable | `EV-21`; local edge authority owns stop | `OM-02` with drive inhibited, or `OM-03` |
| Any motion | E-stop | `EV-15` | `OM-04` |
| `OM-04` | E-stop release | `EV-16`; queues flushed | `OM-03 + BS-00` |
| Any | Critical energy | Stop/settle if available, then `EV-14` | Off |

## 7. Qualification concurrency cases

These exact vectors drive the G02 invariant. Registration attaches a hardware/configuration revision.

| ID | Vector / case | Concurrent intent | Purpose / credibility |
|---|---|---|---|
| `CC-01` | `OM-03 + EN-01 + BS-00` after `EV-01` | Logic boots/supervises; motors off | Required startup/inrush case |
| `CC-02F` | `OM-01 + BS-01` | Listening + dim face + health; camera off and head servos torque-off | Floor-mode quiet-idle / energy floor |
| `CC-02T` | `OM-02 + BS-01` | Same electrical intent as `CC-02F`, with drive inhibit independently verified | Tabletop quiet-idle / permission proof |
| `CC-03` | `BS-02/04 + EV-03` | Wake head + display + chirp + camera/perception | Core wake; 10 transient repetitions |
| `CC-03N` | `OM-01/02 + BS-01`; non-wake and false-trigger trial set | Listening/dim-face baseline remains unchanged; no head/camera/drive transition | RP05 invocation rejection/false-wake state proof |
| `CC-04` | `BS-03 + EV-04/05` | Perception/camera + sector turns + acquisition orient | Core search/acquire |
| `CC-05` | `BS-02/04/07/08 + EV-06` | Exact gesture plus awake baseline | Core expression; each RP-01 representative motion |
| `CC-06` | `BS-02/04/08 + EV-07` | Startle + display/audio; drive off | Credible worst head-domain transient |
| `CC-07A` | `BS-05` | Audio capture + interaction + attentive face/track | Core request capture |
| `CC-07B` | `BS-06` | Network/SBC wait + bounded face/hold | Core external-service wait |
| `CC-07C` | `BS-07 + EV-08/09` | Utility display + chirp/alarm + optional gesture | Core response |
| `CC-07D` | `BS-05/06 + EV-22` | Ambiguous/unsupported/denied intent produces clarification or bounded failure; no physical command | Semantic rejection / honest-failure proof |
| `CC-07E` | Any pending/active utility, Spotify or performance action + `EV-17` | Cancel during pending and active work; late/duplicate result injected after cancellation | Per-action lifecycle and stale-result proof |
| `CC-08` | `BS-08` | Audio **RMS** with crest events + face + capture + small head motion | Core music; 3 min thermal/energy |
| `CC-09` | `OM-01 + BS-09 + PC-03 + AL[follow]=AL-03` | Tracking + steady drive + safety sensing + head correction | Core sustained follow |
| `CC-09C` | `OM-01 + BS-09 + PC-03 + AL[come]=AL-03` | Search/orient as needed, approach from 1–2 m, brake and settle in 0.6–0.9 m band | Core come/approach completion proof |
| `CC-09R` | `CC-09 + EV-18/19` | Temporary occlusion, target exit/re-entry and distractor; brake, preserve identity, reacquire or fail | Continuity/no-silent-switch proof |
| `CC-10A` | `CC-09/09C + EV-10` | Follow/come baseline + drive launch | Credible drive transient |
| `CC-10B` | `CC-09/09C + EV-11/12` | Follow/come baseline + reversal/brake/regeneration | Credible drive transient |
| `CC-10C` | `CC-09/09C + EV-20` | Representative obstacle at registered approach speed; local stop or proven redirect | Obstacle safety proof |
| `CC-11` | `OM-01 + BS-02/04 + EV-13` | Spin + face + optional chirp + ordinary head hold | Core spin |
| `CC-12A` | `OM-02 + BS-02/04/07/08` | Worst registered permitted non-drive behaviour while drive-off is verified | Tabletop permitted-behaviour proof |
| `CC-12B` | `OM-02 + BS-02`; come/follow and spin requests injected | Requests rejected with zero base motion and no mode change | Tabletop forbidden-request proof |
| `CC-12C` | `OM-02` + explicitly armed low-speed calibration motion + `EV-21` | Edge sensing and local stop remain active inside caught/validated footprint | Tabletop edge-protection proof |
| `CC-13H` | `EN-02` crossed during `CC-05` | New peak gestures rejected; active head motion brakes; bounded expression remains | Head-domain low-energy proof |
| `CC-13D` | `EN-02` crossed during `CC-09/09C` | Base brakes; new locomotion/peak gestures rejected; bounded expression remains | Drive-domain low-energy proof |
| `CC-14` | `EN-03` crossed under largest allowed sustained load | Controlled brake/settle/shutdown before rail collapse | Critical-energy proof |
| `CC-15` | `OM-06 + EN-04 + BS-11` | Charger/power-path + display + minimum supervision; camera/SBC interaction/audio/motors off | Charging/service/thermal proof |
| `CC-16` | Any safe non-hard-stop state + `EV-14` | Cancel, brake/settle, inhibit, persist logs, sign off and remove logic power | Orderly normal-shutdown proof |
| `CC-17` | `OM-01/02 + BS-02`; timed dwell with no person request | Bounded, non-repetitive face/status/head aliveness separated by settled holds | SC-09 idle-aliveness thermal/behaviour proof |
| `CC-18` | Wake/acknowledge/spin performance with one eligible expressive channel unavailable or denied | Composer produces an honest bounded variant; safety denial never blocks stopping | RP04 degraded-composition proof |

### Maximum credible and synthetic peak cases

| ID | Definition | May prove | May not prove |
|---|---|---|---|
| `CC-PEAK-01` | `CC-10B` reversal/brake while tracking compute/camera, face, safety sensing, ordinary head corrections and one acknowledgement audio crest are active | Highest currently credible whole-robot transient, pending real RP-03/audio profiles | Head-startle concurrency; recoil waits for base stop |
| `ST-01` | Synthetic alignment of head startle, drive reversal, audio crest, display transition and perception peak | Robustness, fuse non-trip margin, rail coupling and brownout order | Representative operation or an energy-duty proportion |

`ST-01` replaces the old draft `S13` claim. It is valuable but honestly labelled: firmware should prevent that exact behavioural combination. If the 5 A supply cannot produce it, record the largest vector and repeat in Phase C from a protected candidate source.

## 8. Forbidden concurrency

| Combination | Rule | Reason |
|---|---|---|
| Any ordinary drive profile with `OM-02`, or any drive profile with `OM-03/04/06` | Forbidden; only the separately armed, minimum-speed, caught-fixture `CC-12C` may move in `OM-02` | Permission dominates behaviour; calibration authority never becomes ordinary locomotion authority |
| Head recoil while drive torque remains commanded | Forbidden; `EV-12` first | Stability and bounded contact over expression |
| New peak gesture/locomotion in `EN-02` | Forbidden | Preserve reserve and avoid threshold oscillation |
| Any new motor goal in `EN-03` | Forbidden | Only stop/settle/shutdown legal |
| Search sweep before wake completion | Forbidden | Wake and search are distinct semantics |
| Stored goal after reset/reconnect/E-stop release | Forbidden | Recovery only from fresh intent |
| Silent selected-person switch after temporary loss or distractor appearance | Forbidden; `PC-04/05` preserves identity until reacquired or `PC-06` expires it | Seeing a new person is not authority to follow them |
| Output or motion from an `AL-04/05/06` action instance | Forbidden | Cancelled, completed and failed work is terminal; retry creates a new action instance |
| Excited spin in tabletop mode | Forbidden | Approved scope rule |
| Operating motion while charging | Forbidden by `SD-04`; `OM-06` hardware-inhibits the motor domain | Charging is a restricted display/supervision state, not tethered operation |

## 9. `MD-01` — representative 20-minute mixed-duty cycle, registered definition v0.2

This is a chronological recipe, not durations padded to reach twenty minutes. It includes startup/shutdown, both Core scenarios, meaningful idle, three minutes of music and three minutes of locomotion behaviour. Events overlay their interval and add no elapsed time.

| Time | Duration | Case / behaviour | Embedded events and purpose |
|---|---:|---|---|
| 00:00–00:20 | 0:20 | `CC-01` | Cold start, inhibited self-check and inrush |
| 00:20–02:20 | 2:00 | `CC-02F` | Quiet idle; camera off, servos torque-off, head passively down |
| 02:20–02:40 | 0:20 | `CC-03 → CC-04` | Wake, search if needed, acquire, greeting |
| 02:40–04:40 | 2:00 | `CC-17` with two `CC-05` events | Attentive/idle aliveness; two gestures separated by settled holds |
| 04:40–05:40 | 1:00 | `CC-07A/B/C/E` | Time, a two-minute timer, an alarm scheduled inside this cycle, and Spotify-start; per-action lifecycle logged separately |
| 05:40–08:40 | 3:00 | `CC-08` | Registered music file/level; timer `EV-09` fires and is cancelled; two small gestures and one `CC-06` startle with drive off |
| 08:40–10:40 | 2:00 | `CC-02F` | Second quiet-idle interval |
| 10:40–11:10 | 0:30 | `CC-03 → CC-04` | Wake, search/acquire and come acknowledgement |
| 11:10–12:10 | 1:00 | `CC-09C/10A/10B` | Come: ≥2 launches/stops; finish in 0.6–0.9 m band |
| 12:10–14:10 | 2:00 | `CC-09/09R/10A/10B/10C` | Follow: ≥4 more launches/reversals, one obstacle intervention, one short loss/reacquisition |
| 14:10–14:25 | 0:15 | `CC-11` | One bounded spin; interval includes complete settle, not 15 s peak drive |
| 14:25–18:50 | 4:25 | `CC-17` with `CC-07C/E` and six `CC-05` events | Attentive/social dwell; scheduled alarm `EV-09` fires and is cancelled; six gestures distributed across settled holds |
| 18:50–19:50 | 1:00 | `CC-02F` | Final rest and post-duty thermal observation |
| 19:50–20:00 | 0:10 | `CC-16 / EV-14` | Cancel, settle, inhibit, persist logs, sign off, rails down |
| **Total** | **20:00** | | |

### Run-specific freeze fields

The workload sequence and duration are registered here. Before any scored execution, its run registration must additionally freeze the exact firmware/config and ledger revision; servo/reference load and voltage; real/substitute drive record; music file, gain, speaker load and display brightness; route/surface/obstacle script; event timestamps; measurement rates; and starting pack, usable-depth and reserve definitions.

`MD-01` is representative, not the only stress test. Invocation negatives (`CC-03N`), clarification (`CC-07D`), tabletop edge (`CC-12C`), degraded composition (`CC-18`), `CC-06`, `CC-PEAK-01`, `ST-01`, repeated gesture thermal blocks and fault tests run separately.

## 10. Crosswalk from unregistered v0.1 `Sxx`

| Old | v0.2 disposition |
|---|---|
| `S00` | `OM-04`, exercised by `EV-15/16` |
| `S01` | `EV-01` / `CC-01` |
| `S02` | `BS-01` / `CC-02F/T` |
| `S03` | `BS-02` |
| `S04` | `EV-03` / `CC-03` |
| `S05` | `BS-03 + EV-04/05` / `CC-04` |
| `S06` | `EV-06` / `CC-05` |
| `S07` | `EV-07` / `CC-06` |
| `S08` | Split into `BS-05/06/07` and `CC-07A/B/C` |
| `S09` | `BS-08` / `CC-08`; RMS and crest separated |
| `S10` | Split into `EV-10/11/12` and `CC-10A/B` |
| `S11` | `BS-09` / `CC-09` |
| `S12` | `EV-13` / `CC-11` |
| `S13` | Split into credible `CC-PEAK-01` and synthetic `ST-01` |
| `S14` | `EN-02` / `CC-13H/D` |
| `S15` | `EV-14` / `CC-16` |
| `S16` | Split into `EN-03/CC-14` and `OM-06 + EN-04/CC-15` |
| `S17` | `OM-02` / `CC-12A/B` |

## 11. Registration record

| Field | Registered value |
|---|---|
| Registration | `RP02-P1-REG-01` |
| Date | 2026-09-15 |
| Builder approval | Explicit approval in the project conversation: “i think we should approve everything now” |
| State-register revision | v0.4 |
| Registered runtime families | `OM-01…06`; `EN-01…04`; `HL-01…04`; `PC-00…06`; per-action `AL-00…06`; `BS-00…11`; `EV-01…22` |
| Registered qualification families | `CC-01…18` including every lettered variant listed in §7; `CC-PEAK-01`; `ST-01` |
| Registered workload | `MD-01` definition v0.2, exactly 20:00 |
| Registered companion revisions | `operating-situations.md` v0.2; `state-coverage-matrix.md` v0.2; `load-model.md` v0.3; `fault-matrix.md` v0.2; `power-energy-ledger.md` v0.7 planning envelope |
| Approved open parameters | Numeric energy thresholds, grace periods, trajectories, hardware/configuration, route/obstacle fixtures, measurement rates and final gate thresholds remain explicitly open and must be frozen before their scored runs |
| Evidence state | No scored run and no measured `W` evidence yet; registration freezes what will be tested, not whether it passes |
