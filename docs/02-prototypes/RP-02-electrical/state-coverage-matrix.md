# RP-02 State / Case / Load / Evidence Coverage Matrix

| Field | Value |
|---|---|
| Status | **Registered Part-1 coverage baseline v0.2 — builder-approved 2026-09-15; run-specific configurations and open numeric thresholds remain to be frozen before scoring** |
| Owner | Project builder |
| Created | 2026-09-15 |
| Sources | All `../../00-foundation/*.md`; `../../01-system/system-design-brief.md`; `../../01-system/risk-prototype-plan.md`; `state-register.md` v0.4; `load-model.md` v0.3; `fault-matrix.md`; `gates.md` |
| Purpose | Prove that every required operating condition has a legal state vector, reproducible loads, safety/fault expectations and named evidence |

## 1. Coverage rules

1. Do not enumerate the Cartesian product. Select combinations that cover an approved behaviour, a boundary/transition, a credible concurrent peak, a sustained thermal/energy condition, an inhibit, or a recovery obligation.
2. Unless a row says otherwise, baseline health is `HL-01 Available`, energy is `EN-01 Normal`, person continuity is `PC-00/01` when no person is engaged, and no long-running action exists (`AL-00`).
3. A fault row changes only the named health/energy input. The underlying `CC` remains the reproducible load and hazard context.
4. `OFF` is a measured or electrically verified profile, not a missing estimate. Any required load without a valid `LP` or substitute record keeps the case exploratory.
5. Every case records initial vector, trigger, terminal vector, exact profile revisions, duration/repetitions, firmware/configuration, instrument rates and gate results in its run record.
6. Passing one case proves only that vector and revision. `gates.md` defines which changes require re-running it.

## 2. Functional and transition coverage

Abbreviations in the evidence column: `V/I` load-end voltage and branch current; `RST` reset reasons/count; `CRC` link counters; `T` temperatures; `τ` timestamped latency/jitter; `E` integrated energy; `LOG` commands, transitions, health and terminal state.

| Case | Requirement / observable outcome | Initial vector and trigger | Required load profiles | Mandatory rule and terminal vector | Fault overlays | Evidence / gates |
|---|---|---|---|---|---|---|
| `CC-01` | AD-04, SC-18: deterministic cold start with no motion | Off → `OM-03 + EN-01 + BS-00 + PC-00 + AL-00`; `EV-01`, then `EV-02` | `LP-01/02/05/10-BOOT`; `LP-03/04-OFF` | Limits and mode precede fresh enable; stored goals execute zero times; terminal `OM-03 + BS-00` until explicitly enabled | `F-02` reboot sub-run | `V/I`, inrush, `RST`, startup `τ`, enable/`NACK` `LOG`; G02/G04/G05 |
| `CC-02F`, `CC-02T` | Scenario 1 starting state; SD-01/02: quiet sleep in both placement modes | `OM-01` or `OM-02` + `BS-01`; dwell | `LP-01-IDLE`, `LP-02-IDLE`, `LP-03/04-OFF`, `LP-05-DIM`, `LP-06-OFF`, `LP-07-LISTEN`, `LP-08-IDLE`, `LP-10-IDLE` | Camera remains off; head is passively down with torque off; no base motion; terminal state unchanged until wake | — | Sustained `V/I/T/E`; camera-stream and servo-torque evidence; G02/G03 |
| `CC-03` | Scenario 1 Wake; coordinated response without premature search | `BS-01 + PC-01/02 + AL[wake]=AL-02` → `EV-03` | `LP-01-PERCEPTION`, `LP-02-TRAJ`, `LP-03-WAKE`, `LP-05-WAKE`, `LP-06-TRACK`, `LP-07-LISTEN`, `LP-08-CHIRP` | Camera start is included in latency; search waits for wake completion; wake ends `AL-05`; terminal `BS-04 + PC-03` if selected, otherwise `BS-03 + PC-01/02` | `F-02`, `F-07` | Transient `V/I`, wake/acquire `τ`, pose/display/light/audio alignment, `RST/CRC`; G02/G04/G05 |
| `CC-03N` | SC-TBD-15/RP05: rejected invocation and false-wake tolerance | `BS-01`; non-wake/negative utterance set | `CC-02F/T` baseline remains unchanged | No `EV-03`, camera start, servo torque or drive command; terminal remains `BS-01` | Audio-front-end degradation when available | False-wake/reject log and unchanged load/state trace; RP05-G01, RP02-G02 |
| `CC-04` | Scenario 1/2: visual search, select, acquire and orient | `BS-03 + PC-01/02 + AL[search]=AL-03`; `EV-04`, then `EV-05` | `LP-01-PERCEPTION`, `LP-02-TRAJ`, `LP-03-SEARCH/ORIENT`, `LP-05-ACTIVE`, `LP-06-TRACK`, `LP-07-LISTEN` | Selection creates `PC-03`; acquisition cancels remaining sectors; no base search; timeout ends `PC-06 + AL-06 + BS-10/02` | `F-03`, `F-09` | Sector/acquisition `τ`, identity/selection log, per-axis state, `V/I/CRC`; G02/G04/G05, RP07-G01/02 |
| `CC-05` | Scenario 1 social expression; every representative RP-01 motion is electrically bounded | `BS-02/04/07/08 + AL[performance]=AL-03`; `EV-06` | Awake baseline + exact `LP-03-GESTURE` or `LP-03-MICRO`; display/light/audio profile used by that authored motion | Limits and safe stop pre-empt expression; settle then `AL-05`; cancel uses `AL-04`; no queued replay | `F-01`, `F-04`, `F-08`, `F-16` | Per-axis `V/I/T`, trajectory error, `τ`, `RST/CRC`, terminal `LOG`; G02/G04/G05 |
| `CC-06` | HM-15/AD-08: credible worst head-domain startle | `BS-02/04/08`; `EV-07`; base already stopped | `LP-01-COEXIST`, `LP-02-TRAJ`, `LP-03-STARTLE`, `LP-04-OFF`, `LP-05-WAKE`, `LP-06-TRACK`, `LP-08-CHIRP` | If propulsion was active, `EV-12` must complete before physical recoil; finish in bounded attentive/failure state | `F-06`, `F-11`, `F-12/F-13` | Oscilloscope `V/I`, onset/order `τ`, `RST/CRC`, rail isolation and terminal `LOG`; G02/G04/G05 |
| `CC-07A` | Scenario 1: capture a spoken request without implying success | `BS-04/02`; `AL[request]=AL-01 → AL-02`; enter `BS-05` | `LP-01-AUDIO`, `LP-02-IDLE/TRAJ`, `LP-03-HOLD/TRACK`, `LP-05-ACTIVE`, `LP-06-TRACK`, `LP-07-CAPTURE`, `LP-08-IDLE` | Capture timeout/cancel is explicit; terminal `BS-06`, `BS-10` or attentive state with action lifecycle recorded | — | Audio/interaction `V/I/T`, phase-boundary and acceptance/rejection `τ/LOG`; G02/G05, RP05-G02/03 |
| `CC-07B` | AD-09, CON-11/P04: bounded external-service wait | `BS-06 + AL[request]=AL-03`; request dispatched | `LP-01-SERVICE`, `LP-02-IDLE`, `LP-03-HOLD`, `LP-05-ACTIVE`, `LP-06-TRACK`, `LP-07-LISTEN`, `LP-08-IDLE` | Timeout sets `AL-06`; late result cannot revive it; terminal `BS-07`, `BS-10` or attentive state | `F-10`, `F-15`, `F-20` | Request/timeout/auth/late-result `LOG`, network-independent safety, `V/I/T`; G02/G04/G05, RP05-G03/04 |
| `CC-07C` | Scenario 1 utilities: time, timer, alarm and response lifecycle | `BS-07`; `AL[action]=AL-03`; `EV-08` or `EV-09` | `LP-01-IDLE`, `LP-02-IDLE/TRAJ`, optional `LP-03-GESTURE`, `LP-05-UTILITY`, `LP-08-CHIRP/ALARM` | Timer/alarm may remain active while face returns; completion is once-only `AL-05`; safety pre-empts | `F-07` | Display/audio lifecycle, simultaneous-event handling and terminal `τ/LOG`; G02/G04, RP05-G03 |
| `CC-07D` | Scenario 1/RP05: ambiguity, unsupported intent or denial produces honest clarification | `BS-05/06 + AL-01/02`; `EV-22` | `LP-01-AUDIO/SERVICE`, `LP-05-FAILURE`, optional `LP-08-CHIRP`; no new motor profile | No hazardous command; terminal `AL-06 + BS-10/02/04`; no false success | `F-10/20` variants | Semantic result, zero physical command, visible/audible failure and return `LOG`; G04, RP05-G02/04 |
| `CC-07E` | SDB/RP05: pending/active cancellation and late/duplicate suppression | Utility, Spotify or performance at `AL-02/03`; `EV-17`; then inject late/duplicate result | `LP-01-CANCEL`, applicable `LP-03/04-BRAKE`, bounded display/audio return | `AL-04 → AL-05/06`; old result executes zero times; retry is a new action ID | `F-10`, `F-15`, `F-20` | Cancel latency, output suppression, action IDs, terminal state; G04/G05, RP05-G03 |
| `CC-08` | Scenario 1/SCOPE-19: three-minute music state with character response | `BS-08 + AL[Spotify]=AL-03`; registered excerpt, gain, speaker and display settings | `LP-01-AUDIO`, `LP-02-IDLE/TRAJ`, optional `LP-03-MICRO`, `LP-05-MUSIC`, `LP-07-CAPTURE`, `LP-08-MUSIC` plus recorded `LP-08-CREST` | RMS determines energy/heat; crests remain transients; stop/end/failure sets `AL-04/05/06`; base motion not implied | `F-10`, `F-20` service/auth variants | `V/I/T/E`, RMS/crest correlation, cancel/terminal `LOG`; G02/G03/G04, RP05-G03/04 |
| `CC-09` | Scenario 2: sustained person following with awareness | `OM-01 + BS-09 + PC-03 + AL[follow]=AL-03`; steady segment | `LP-01-PERCEPTION`, `LP-02-TRAJ`, `LP-03-TRACK`, `LP-04-STEADY`, `LP-05-ACTIVE`, `LP-06-TRACK`, `LP-07-LISTEN`, `LP-08-IDLE`, `LP-10-MOTION` | Target evidence and local safety stay valid; loss/obstacle/stop initiates local brake; no blind continuation | `F-05`, `F-09`, `F-17`, `F-19` | Sustained `V/I/T/E`, tracking/stop `τ`, identity, health and terminal `LOG`; G02/G03/G04/G05, RP07-G04/05 |
| `CC-09C` | Scenario 2/RP07: “come here” approach and completion | `OM-01 + BS-09 + PC-03 + AL[come]=AL-03`; start 1–2 m away | Search/orient if required, then `CC-09` baseline with launch and brake profiles | Approach without harmful contact; settle in 0.6–0.9 m band; action becomes `AL-05`, then attentive | `F-09/17/19` variants | Start/stop distance, speed, identity continuity, brake/settle and terminal `LOG`; G02/G04/G05, RP07-G03 |
| `CC-09R` | Scenario 2/RP07: temporary loss, reacquisition and distractor rejection | `CC-09`; `EV-18` causes `PC-03 → PC-04/05`; `EV-19` or expiry follows | `CC-09` → `LP-04-BRAKE`; perception + stopped search/orient profiles | Preserve identity; never silently switch; resume only on same-person `PC-03` and current authorization; otherwise `PC-06 + AL-06` | `F-05`, `F-09` | Loss-to-stop, reacquisition time, identity switches=0, observation age and terminal `LOG`; G04/G05, RP07-G02/05 |
| `CC-10A` | Scenario 2: start from rest inside drive envelope | `CC-09/09C`; `EV-10` | Follow/come baseline + `LP-04-LAUNCH` | Local safety and fresh floor permission precede torque; terminal returns to active action or controlled stop | `F-12/F-13` | Drive and rail transient `V/I`, launch/stop `τ`, no stale restart; G01/G02/G04 |
| `CC-10B` | Scenario 2: reversal, braking and regeneration | `CC-09/09C`; `EV-11` and/or `EV-12` | Follow/come baseline + `LP-04-REV/BRAKE` | Decelerate through zero before opposite torque; startle recoil waits for completed stop; terminal active action, attentive or `OM-03` | `F-05`, `F-09`, `F-17` | Signed branch/source `V/I`, rail max/min, brake latency, terminal `LOG`; G02/G04/G05 |
| `CC-10C` | SCOPE-12/SC-12: local obstacle stop or proven redirect | `CC-09/09C`; representative obstacle triggers `EV-20` | Baseline + `LP-10-OBSTACLE` + `LP-04-BRAKE` or registered redirect | Local safety clamps before behaviour/network response; no harmful contact; continue only under current safe evidence | `F-19` safety-sensor loss | Detection/stop latency and clearance, contact policy, local clamp and terminal `LOG`; G04, RP03-G03/RP07-G05/06 |
| `CC-11` | Scenario 2/SCOPE-21: one bounded excited spin | `OM-01 + BS-02/04`; `EV-13` | `LP-01-PERCEPTION`, `LP-02-IDLE/TRAJ`, `LP-03-HOLD`, `LP-04-SPIN`, `LP-05-ACTIVE`, optional `LP-08-CHIRP`, `LP-10-MOTION` | Explicit finite action; forbidden in tabletop; complete settle precedes any next base action | `F-12/F-13` | Peak and action-window `V/I`, settle `τ`, stability/terminal `LOG`; G02/G04 |
| `CC-12A` | Tabletop permits social/utility behaviour while drive remains electrically inhibited | `OM-02 + BS-02/04/07/08`; worst registered non-drive variant | Corresponding `CC-05/07C/08` profiles + verified `LP-04-OFF` | No ordinary drive torque regardless of app/network behaviour; head remains inside validated envelope | `F-14` link-flood sub-run | Drive-enable/rail evidence, non-drive `V/I/T`, rejected base command `LOG`; G01/G02/G04 |
| `CC-12B` | Explicit tabletop drive/spin-request rejection | `OM-02 + BS-02`; inject come/follow and spin requests | `LP-01-IDLE`, `LP-02-IDLE`, `LP-03-HOLD`, `LP-04-OFF`, `LP-05-ACTIVE`, `LP-10-IDLE` | Requests are rejected; mode does not change; terminal remains `OM-02`, with zero base motion | `F-17` after rejection | `NACK(INHIBITED)`, drive rail/current and terminal `LOG`; G01/G04 |
| `CC-12C` | SCOPE-11/SC-13: explicitly armed tabletop calibration motion remains edge-safe | `OM-02`; caught fixture; separate calibration authorization; `EV-21` | `LP-10-EDGE`, minimum-speed drive profile and `LP-04-BRAKE` | Stops inside registered circular footprint; edge-sensor uncertainty/loss inhibits; never grants ordinary come/follow/spin | `F-19` | Edge coverage, detection/stop distance, drive inhibit and caught-surface result; G01/G04, RP03-G04 |
| `CC-16` | SC-18: orderly normal shutdown is reproducible | Any safe non-hard-stop state; `EV-14` | Starting profiles → optional `LP-03-SLEEP` → `LP-01-SHUTDOWN` → `LP-01/02/03/04/05/06/07/08/10-OFF` | Cancel → brake/settle → inhibit → persist logs → sign-off → logic off; no truncated log or residual motion | Power removal at each registered phase as exploratory sub-runs | Shutdown order `τ`, persisted `LOG`, rail fall, final zero-current evidence; G02/G04/G05 |
| `CC-17` | SCOPE-07/SC-09: powered but unengaged idle feels alive without constant motion | `OM-01/02 + BS-02`; timed dwell; no user request | Sparse registered `LP-03-MICRO` duty, `LP-05-DIM/ACTIVE`, listening and camera/perception baseline | Bounded variation with settled holds; no locomotion; remains interruptible and returns to stable attentive/quiet idle | One expressive-channel denial feeds `CC-18` | Dwell `V/I/T/E`, event frequency, settled fraction and behaviour log; G02/G03, RP04-G03/04 |
| `CC-18` | AD-01/RP04: coordinated performance degrades honestly when one channel is denied | Wake, acknowledge/curious or spin performance; one eligible display/light/audio/head/base channel `HL-03` or mode-inhibited | Registered performance baseline with denied channel off/inhibited; remaining legal profiles retain composition | Safety denial always wins; performance completes/fails honestly without blocking whole system or claiming unavailable output | `F-07/08/09/12/19/21` as applicable | Cross-channel onset, interruption/settle, completion/failure and observer judgement; G04/G05, RP04-G02/04 |

## 3. Energy, charging and protection coverage

| Case | Requirement / observable outcome | Initial vector and trigger | Required load profiles | Mandatory rule and terminal vector | Fault overlays | Evidence / gates |
|---|---|---|---|---|---|---|
| `CC-13H` | SC-TBD-10: low-energy policy during head expression | `EN-01 + CC-05`; cross into `EN-02` | `CC-05` profiles followed by brake/hold and bounded display/audio indication | Reject new peak gesture/locomotion; active head motion brakes; no automatic replay after voltage recovery | `F-16` | Loaded threshold, `V/I`, brake/`NACK` `τ`, terminal `LOG`; G02/G04 |
| `CC-13D` | SC-TBD-10: low-energy policy during locomotion | `EN-01 + CC-09/09C`; cross into `EN-02` | Active locomotion profiles + `LP-04-BRAKE`; expression retained at bounded load | Base brakes; action becomes `AL-04/06`; new locomotion/peak gestures rejected; terminal attentive or `OM-03` | `F-16` | Loaded threshold, signed `V/I`, stop `τ`, reserve and terminal `LOG`; G02/G04 |
| `CC-14` | SC-15/SC-TBD-10: critical energy remains controlled above rail collapse | Largest allowed sustained case; cross `EN-02 → EN-03` | Starting profiles → `LP-03-BRAKE`, `LP-04-BRAKE`, then `CC-16` shutdown profiles | No new motor goal; bounded settle only if margin permits; terminal off, never uncontrolled brownout/restart | `F-16` | Rail margin to UVLO, brake/shutdown order, `RST`, persisted reason; G02/G04 |
| `CC-15` | SD-04/AD-10/G06: safe visible charging without tethered operation | Charge input accepted → `OM-06 + EN-04 + BS-11` | Part-2 charger/power-path profile; `LP-01-OFF`, `LP-02-IDLE`, `LP-03/04-OFF`, `LP-05-CHARGE`, `LP-06/07/08-OFF`, `LP-10-OFF` | Motor domain hardware-inhibited; AC remains outside Makad; removal/completion/fault cannot restore an old operating mode | `F-18`, later pack-temperature/BMS faults when interfaces are selected | Charge/battery `V/I/T`, motor-rail zero, display/health `LOG`, removal/recovery; G01/G02/G04/G06 |

## 4. Peak, stress and endurance coverage

| Case | Requirement / observable outcome | Composition | Rule | Evidence / gates |
|---|---|---|---|---|
| `CC-PEAK-01` | AD-08/G02: highest currently credible whole-robot electrical transient | `CC-10B` reversal/brake + tracking compute/camera + active face + base safety + ordinary head correction + one registered acknowledgement crest | It must be behaviourally reachable. It excludes head startle because recoil waits for base stop. | Oscilloscope rail minima/maxima, signed branch currents, `RST/CRC`, timing and fuse non-trip; G01/G02/G05 |
| `ST-01` | Robustness bound, not a user-visible operating claim | Synthetic alignment of head startle, drive reversal, display transition, perception peak and audio crest | May test coupling, brownout order and fuse margin; may not enter `MD-01` energy proportions or be called “representative.” | Same transient evidence as `CC-PEAK-01`, explicitly labelled stress; G01/G02 |
| `MD-01` | CON-10/SC-14 rehearsal: representative twenty-minute mixed duty | Chronological recipe in `state-register.md` §9 covering boot, sleep, wake, search, idle aliveness, interaction lifecycle, music, come, follow, loss/reacquisition, obstacle stop, spin and shutdown | Frozen workload revision; no padding with undefined “average” current; RP-02 rehearses but integrated robot closes SC-14 | Input and per-group `E`, temperatures, resets, reserve and terminal state; G02/G03 |

## 5. Namespace coverage audit

| Namespace | Covered identifiers | Coverage vehicle | Gap rule |
|---|---|---|---|
| Operating modes | `OM-01` | `CC-02F`, `CC-09…11`, `CC-13D` | Floor permission must be fresh and local |
|  | `OM-02` | `CC-02T`, `CC-12A/B/C` | Permitted non-drive use, rejected ordinary drive and caught edge intervention are required |
|  | `OM-03` | `CC-01`, fault terminal states, `CC-14` | Every reset/link-loss/recovery path returns here before motion |
|  | `OM-04` | `F-12/F-13` over `CC-06/10A/11` | Hard stop is a fault/protection overlay, not a behavioural workload |
|  | `OM-05` | Every Phase-A/B rig run; G01/G06 procedures | Bench/service is a controlled test permission and fixture condition, not a Core behaviour |
|  | `OM-06` | `CC-15` | Charging never coexists with operating motion |
| Energy | `EN-01…04` | Baseline cases; `CC-13H/D`; `CC-14`; `CC-15` | Thresholds remain unregistered until frozen before scored data |
| Person continuity | `PC-00…06` | `CC-01/03/04/09/09C/09R`; `CC-10C` | Selection, temporary loss, same-person reacquisition and expiry are observable; identity never switches silently |
| Action lifecycle | `AL-00…06` per action | `CC-03/05/07A…E/08/09/09C/09R/11/16/18` | Pending, active, cancelling, completed and failed are distinct; late/duplicate output cannot reactivate terminal work |
| Behaviour | `BS-00…09`, `BS-11` | Directly covered by `CC-01…12`, `CC-15…18` | Each dwellable state needs at least one sustained or transition case |
|  | `BS-10` | `CC-07D`, terminal/visible response in fault sub-runs and timeout/loss variants | Failure indication must never substitute for hazardous-output inhibition |
| Events | `EV-01…14`, `EV-17…22` | `CC-01`, `CC-03…18` as mapped | Event order, action ID and completion are logged |
|  | `EV-15/16` | `F-12/F-13` | Release proves zero motion and fresh-enable requirement |
| Health | `HL-01` | All non-fault baselines | Availability is not inferred from missing errors |
|  | `HL-02` | `F-04`, `F-05`, `F-11` | Degradation threshold and permitted reduced capability must be logged |
|  | `HL-03` | `F-01/02/03/08/09/10/17…21` as applicable | Dependent behaviour stops; unrelated safe channels may remain |
|  | `HL-04` | `F-06/11/12/16/19/22` unsafe variants | Hazardous outputs inhibit and recovery requires fresh authority |

## 6. Registration completeness checklist

The registered Part-1 baseline is complete because:

- every row above is approved, amended or explicitly declared out of scope;
- every referenced `LP` exists in `load-model.md`, including a verified `OFF` definition where required;
- each relevant fault has at least one primary case and the campaign satisfies the cross-state repetition rule;
- every Core scenario step traces to at least one case and observable terminal state;
- `PC-01…06` and per-action `AL-01…06` transitions are observable in logs rather than inferred from `BS`;
- the approved negative/boundary situations—false wake, ambiguity, pending/active cancellation, late/duplicate result, target loss/distractor, obstacle, tabletop edge and channel denial—each retain an explicit case;
- `CC-PEAK-01` remains reachable and distinct from `ST-01`;
- `MD-01` totals exactly twenty minutes and references only approved cases/profiles;
- each gate names which cases it consumes; and
- the builder records revision, date and approval before scored results are inspected.

## 7. Registration record

| Registration | Date | Approved scope | Evidence state |
|---|---|---|---|
| `RP02-P1-REG-01` | 2026-09-15 | Every row and gap rule in v0.2, including negative/boundary cases, `CC-PEAK-01`, `ST-01` and `MD-01`; explicit builder approval in the project conversation | Coverage frozen; no case has yet passed a scored run |
