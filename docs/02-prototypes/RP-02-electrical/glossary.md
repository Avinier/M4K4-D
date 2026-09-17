# RP-02 Electrical/Control Glossary

| Field | Value |
|---|---|
| Status | **Living reader index.** Parts 1–3 retain their registered labels; Part-4 ICD definition is `RP02-P4-REG-01`. Byte layouts and C3 drive messages remain open. |
| Scope | RP-02-owned namespaces, labels and notation, plus externally owned identifiers commonly referenced by RP-02 |
| Rule | This glossary defines identifier meaning and points to the canonical source. Detailed behaviour, numeric values and acceptance thresholds remain in their owning documents. |

## 1. How to read an RP-02 identifier

An identifier's prefix says what kind of record it is. Its number identifies a stable record inside that namespace. Letter suffixes distinguish registered variants rather than informal subcases.

Examples:

- `OM-03` is an operating mode: motion inhibited.
- `CC-09C` is the registered come/approach qualification case.
- `LP-03-WAKE` is the wake load profile for load group `LG-03`.
- `F-12` is the E-stop-assertion fault-injection obligation.
- `RP02-G04` is the RP-02 fault-containment gate.

Compact notation used in the RP-02 documents:

| Notation | Meaning |
|---|---|
| `A + B` | Conditions coexist in one state vector. |
| `A/B` | The statement applies to either or all listed alternatives, as the surrounding row specifies; it does not create a new combined ID. |
| `A → B` | Ordered transition from A to B. |
| `AL[action]` | The lifecycle of one named action instance; several actions may have independent `AL` values. |
| `HL[*]` | Health is maintained separately for every applicable subsystem. |
| `xx` | Placeholder for one member of an identifier family, not a literal registered ID. |
| `OFF` | An implemented and verified unpowered/disabled state. Missing hardware or missing evidence is not `OFF`. |
| `η` | Efficiency at the stated input voltage, output load and temperature. |
| `I_RMS` | Root-mean-square current over the named thermal time window. |
| `I²t` | Time integral of squared current used to compare clearing stress with path withstand. |
| `DoD_usable` | Fraction of nominal pack energy permitted to be used by the applicable energy policy. |

## 2. RP-02 namespace registry

### 2.1 Registered Part-1 runtime namespaces

| Namespace | Name | What it identifies | Canonical source |
|---|---|---|---|
| `OM-*` | Operating mode | Local motion authority and operating permission | `state-register.md` §2 |
| `EN-*` | Energy state | Normal, low, critical or charging energy overlay | `state-register.md` §3.1 |
| `HL-*` | Health level | Per-subsystem availability and safety condition | `state-register.md` §3.2 |
| `PC-*` | Person continuity | Selected-person evidence and continuity state | `state-register.md` §3.3 |
| `AL-*` | Action lifecycle | Lifecycle of each long-running action instance | `state-register.md` §3.4 |
| `BS-*` | Behaviour state | Dwellable semantic behaviour of Makad | `state-register.md` §4 |
| `EV-*` | Transient event | Short ordered change overlaid on a behaviour state | `state-register.md` §5 |
| `CC-*` | Qualification case | Registered, credible concurrent state/load vector | `state-register.md` §7 |
| `CC-PEAK-*` | Credible peak case | Maximum credible alignment of operating profiles | `state-register.md` §7 |
| `ST-*` | Synthetic stress | Deliberately non-representative robustness alignment | `state-register.md` §7 |
| `MD-*` | Mixed-duty workload | Registered chronological endurance recipe | `state-register.md` §9 |
| `SD-*` | State decision | Builder-approved Part-1 operating-state decision | `state-register.md` §4 |

### 2.2 Load, evidence and qualification namespaces

| Namespace | Name | What it identifies | Canonical source |
|---|---|---|---|
| `LG-*` | Load group | Stable electrical accounting boundary | `load-model.md` §3 and `power-energy-ledger.md` §2 |
| `LP-<group>-<name>` | Load profile | Reproducible electrical/thermal demand for an `LG` boundary | `load-model.md` §4 |
| `TB-*` | Time-base class | Measurement window required to observe a profile | `load-model.md` §2 |
| `F-*` | Fault obligation | Reproducible injected fault and its inhibit/reject/expose/recover contract | `fault-matrix.md` §2 |
| `RP02-G*` | RP-02 gate | Protection, coexistence, runtime, containment, control or serviceability gate | `gates.md` |
| `RP02-P<n>-REG-<nn>` | Registration | Immutable approved baseline for one RP-02 part/revision | Registration section of the affected documents |

### 2.3 Part-2 design namespaces

| Namespace | Name | What it identifies | Current status |
|---|---|---|---|
| `EDB-*` | Electrical design-basis decision | Scope, conventions, invariants and completeness rules that architecture must satisfy | `electrical-design-basis.md`; `EDB-01…08` approved 2026-09-15 |
| `EC-*` | Electrical criticality class | Functional consequence of losing or disturbing a consumer; not a physical rail count | Approved as part of `EDB-05` |
| `PA-*` | Power-architecture decision | Registered topology/protection/energy choice and reopen condition | `power-architecture.md`; `PA-01…16` registered under `RP02-P2-REG-01` |
| `PB-*` | Physical power branch | Stable key for a source/distribution path and its branch-side `EDB-03` contract | `power-architecture.md`; registered under `RP02-P2-REG-01` |
| `PCD-<class>-<nn>` | Power-component candidate | One sourced conversion, protection, E-stop, connector, cable or charging candidate and its use-specific disposition | `power-component-candidate-screen.md`; derived, not registered or selected |
| `BR-*` | Brownout/reset/restart requirement | Registered energy-loss ordering, threshold ownership, reset default and fresh-intent recovery rule | `brownout-restart-contract.md`; registered under `RP02-P2-REG-03` |

### 2.4 Part-3 compute/control namespaces

| Namespace | Name | What it identifies | Current status |
|---|---|---|---|
| `CA-*` | Compute/control architecture rule | Processor ownership, link topology, runtime containment, watchdog, arm/recovery, configuration and service/logging rule | `compute-control-architecture.md`; `CA-01…16` registered under `RP02-P3-REG-01` |
| `CCD-<class>-<nn>` | Compute/control candidate | One sourced compute, controller, link, watchdog, carrier, middleware, IPC or supervision candidate and its disposition | `compute-control-component-screen.md`; selections/leads are stated per row and do not authorize purchase |
| `C0` | Application compute | Body-mounted Raspberry Pi 5 2 GB running the Linux application services and master monotonic clock | Selected under `RP02-P2-REG-02`; ownership fixed by `RP02-P3-REG-01` |
| `C2` | Head safety controller | Head-mounted Waveshare ESP32-S3-Zero owning head trajectories, limits, expiry, servo bus and head readiness | Selected before Part 3; ownership fixed by `RP02-P3-REG-01` |
| `C3` | Base safety controller | ESP32-S3 controller owning wheel loops, local hazards/reflexes, expiry, odometry capture and base readiness | Role fixed by `RP02-P3-REG-01`; prototype corrected to DevKitC-1-N8 by `RP02-P3-REG-02`; final carrier/pins wait on RP-03 |
| `D1` | Face renderer | Selected display board's ESP32-S3, receiving semantic face/light state through C2 | Hardware preselected; C2-relay role fixed by `RP02-P3-REG-01` |

## 3. Registered Part-1 labels

### 3.1 Operating modes — `OM-*`

| ID | Label | Short definition |
|---|---|---|
| `OM-01` | Floor | Base and head motion permitted inside validated envelopes after session-scoped local acceptance. |
| `OM-02` | Tabletop | Ordinary base motion inhibited; head motion permitted; only separately armed caught-fixture calibration may move the base. |
| `OM-03` | Motion inhibited | Base motion forbidden and no new head trajectory; default after boot, reset, stale authority or unsafe health. |
| `OM-04` | Hard stop | Hazardous motor domain physically unpowered while supervision remains alive. |
| `OM-05` | Bench/service | Only explicitly armed fixture-bound test channels may move. |
| `OM-06` | Charging | Motors, camera, ordinary SBC workload, microphones and audio off; charge display and minimum supervision remain. |

### 3.2 Energy states — `EN-*`

| ID | Label | Short definition |
|---|---|---|
| `EN-01` | Normal | All actions allowed by mode and health may operate. |
| `EN-02` | Low | Locomotion and new peak gestures rejected; active locomotion brakes; bounded indication remains. |
| `EN-03` | Critical | Enter motion inhibit, settle only if margin permits, persist reason and shut down. |
| `EN-04` | Charging | Requires `OM-06`; only the registered charging load set is permitted. |

### 3.3 Health levels — `HL-*`

| ID | Label | Short definition |
|---|---|---|
| `HL-01` | Available | Capability may be commanded normally. |
| `HL-02` | Degraded | Capability remains bounded with reduced margin or quality. |
| `HL-03` | Unavailable | Dependent behaviour is denied or stopped; unrelated safe channels may continue. |
| `HL-04` | Unsafe | Hazardous outputs are inhibited immediately; recovery requires fresh authorization. |

### 3.4 Person continuity — `PC-*`

| ID | Label | Short definition |
|---|---|---|
| `PC-00` | Not applicable | No person-dependent action is authorized. |
| `PC-01` | No candidate | Discovery may start; approach or follow is forbidden. |
| `PC-02` | Candidate, not selected | Attention may preview; locomotion toward the candidate is forbidden. |
| `PC-03` | Selected and fresh | Person-dependent actions may be authorized within other limits. |
| `PC-04` | Temporarily lost | Preserve identity, brake base motion and do not switch targets. |
| `PC-05` | Reacquiring | Search only for the same selected identity; base remains stopped. |
| `PC-06` | Lost/expired | Clear selection authority; a new candidate requires explicit selection. |

### 3.5 Per-action lifecycle — `AL-*`

| ID | Label | Short definition |
|---|---|---|
| `AL-00` | No instance | No action instance exists. |
| `AL-01` | Proposed | Intent exists but has no execution authority. |
| `AL-02` | Accepted | Authority and initial conditions are valid; work may be scheduled. |
| `AL-03` | Active | Current work is executing with a validity deadline and feedback. |
| `AL-04` | Cancelling | New output suppressed; physical work brakes/settles; late results cannot reactivate it. |
| `AL-05` | Completed | Completion recorded once; duplicates ignored. |
| `AL-06` | Failed | Failure exposed; retry requires a new action instance. |

### 3.6 Behaviour states — `BS-*`

| ID | Label |
|---|---|
| `BS-00` | Logic alive, motion inhibited |
| `BS-01` | Quiet idle/sleep |
| `BS-02` | Attentive idle/procedural aliveness |
| `BS-03` | Person search |
| `BS-04` | Person tracking/attention |
| `BS-05` | Spoken-input capture |
| `BS-06` | External-service wait |
| `BS-07` | Response/utility presentation |
| `BS-08` | Music playback/vibe |
| `BS-09` | Come/follow |
| `BS-10` | Bounded failure indication |
| `BS-11` | Charging display |

### 3.7 Transient events — `EV-*`

| ID | Label | ID | Label |
|---|---|---|---|
| `EV-01` | Cold boot/rail inrush | `EV-12` | Controlled brake/stop |
| `EV-02` | Enable handshake | `EV-13` | Excited spin |
| `EV-03` | Wake rise | `EV-14` | Orderly shutdown |
| `EV-04` | Search-sector turn | `EV-15` | E-stop assertion |
| `EV-05` | Acquire/orient | `EV-16` | E-stop release/motor restoration |
| `EV-06` | Authored head gesture | `EV-17` | Cancel/interrupt/return to idle |
| `EV-07` | Startle/recoil | `EV-18` | Selected-person evidence lost |
| `EV-08` | Utility/display transition | `EV-19` | Same-person reacquisition |
| `EV-09` | Alarm/timer annunciation | `EV-20` | Local obstacle intervention |
| `EV-10` | Base launch | `EV-21` | Tabletop edge intervention |
| `EV-11` | Base reversal | `EV-22` | Semantic rejection/clarification |

### 3.8 Qualification cases — `CC-*`

| ID | Label | ID | Label |
|---|---|---|---|
| `CC-01` | Cold boot and supervised inhibit | `CC-09` | Sustained follow |
| `CC-02F` | Floor quiet idle | `CC-09C` | Come/approach and stopping band |
| `CC-02T` | Tabletop quiet idle and drive inhibit | `CC-09R` | Loss, identity preservation and reacquisition |
| `CC-03` | Wake transition | `CC-10A` | Drive launch |
| `CC-03N` | Non-wake/false-trigger rejection | `CC-10B` | Reversal, brake and regeneration |
| `CC-04` | Search and acquisition | `CC-10C` | Obstacle intervention |
| `CC-05` | Authored expression/gesture | `CC-11` | Bounded excited spin |
| `CC-06` | Credible head-domain startle peak | `CC-12A` | Tabletop permitted behaviour |
| `CC-07A` | Spoken request capture | `CC-12B` | Tabletop forbidden-request rejection |
| `CC-07B` | External-service wait | `CC-12C` | Armed caught-fixture edge calibration |
| `CC-07C` | Response/utility/alarm | `CC-13H` | Low energy during head motion |
| `CC-07D` | Semantic rejection/honest failure | `CC-13D` | Low energy during locomotion |
| `CC-07E` | Cancellation and stale-result rejection | `CC-14` | Critical-energy controlled shutdown |
| `CC-08` | Music RMS, crests and concurrent expression | `CC-15` | Restricted visible charging |
| `CC-16` | Orderly normal shutdown | `CC-17` | Idle-aliveness dwell |
| `CC-18` | Degraded coordinated performance | `CC-PEAK-01` | Maximum credible whole-robot transient |

| ID | Label |
|---|---|
| `ST-01` | Synthetic alignment of startle, drive reversal, audio crest, display transition and perception; robustness only, never representative duty. |
| `MD-01` | Registered 20-minute representative mixed-duty workload, definition v0.2. |

### 3.9 Part-1 builder decisions — `SD-*`

| ID | Decision label |
|---|---|
| `SD-01` | Camera off in quiet sleep. |
| `SD-02` | Head-servo torque off in sleep; head rests down. |
| `SD-03` | V1 Floor/Table mode selected manually and accepted locally for the session. |
| `SD-04` | Display and minimum supervision remain on while charging; ordinary operation and motors remain off. |

## 4. Load and time labels

### 4.1 Load groups — `LG-*`

| ID | Load group |
|---|---|
| `LG-01` | Main Raspberry Pi 5 2 GB compute |
| `LG-02` | C2 controller and servo-bus transceiver |
| `LG-03Y` | Head yaw-servo load branch |
| `LG-03P` | Head pitch-servo load branch |
| `LG-03R` | Head roll-servo load branch |
| `LG-03Y/P/R` | Compact notation applying to all three separately observable head-servo load branches; not a fourth load group |
| `LG-04` | Drive motors and motor driver |
| `LG-05` | Display board and status light |
| `LG-06` | Camera |
| `LG-07` | Microphones and audio front end |
| `LG-08` | Speaker and amplifier |
| `LG-09` | Derived conversion/distribution loss; never a commanded load |
| `LG-10` | Base MCU and obstacle/edge safety sensing |

### 4.2 Time-base classes — `TB-*`

| ID | Window | Primary concern |
|---|---:|---|
| `TB-1` | ≤10 ms | Contact bounce, converter response, inrush edge and bus disturbance |
| `TB-2` | >10–500 ms | Servo/motor launch, reversal/brake, audio crest and brownout transient |
| `TB-3` | >0.5 s–5 min | RMS demand and component heating |
| `TB-4` | Full duty/endurance | Energy, reserve, heat soak, drift and repetitions |

### 4.3 Load profiles — `LP-*`

The middle number is the owning `LG` number. The suffix names the reproducible condition. Exact configuration, waveform and evidence are supplied by the run binding and ledger.

| Load group | Registered profile labels |
|---|---|
| `LG-01` | `LP-01-OFF`, `BOOT`, `IDLE`, `PERCEPTION`, `AUDIO`, `SERVICE`, `CANCEL`, `COEXIST`, `SHUTDOWN` |
| `LG-02` | `LP-02-OFF`, `BOOT`, `IDLE`, `TRAJ`, `LINKSTRESS`, `FAULT` |
| `LG-03Y/P/R` | `LP-03-OFF`, `PWRRESTORE`, `HOLD`, `SLEEP`, `WAKE`, `SEARCH`, `ORIENT`, `TRACK`, `GESTURE`, `MICRO`, `STARTLE`, `BRAKE`, `THERMAL`, `STALLREF` |
| `LG-04` | `LP-04-OFF`, `PWRRESTORE`, `STEADY`, `LAUNCH`, `REV`, `BRAKE`, `SPIN`, `BLOCKEDREF` |
| `LG-05` | `LP-05-OFF`, `BOOT`, `DIM`, `ACTIVE`, `WAKE`, `UTILITY`, `MUSIC`, `FAILURE`, `CHARGE`, `FULLREF` |
| `LG-06` | `LP-06-OFF`, `STREAM`, `TRACK`, `AF` |
| `LG-07` | `LP-07-OFF`, `LISTEN`, `CAPTURE`, `FAULT` |
| `LG-08` | `LP-08-OFF`, `IDLE`, `CHIRP`, `ALARM`, `MUSIC`, `CREST`, `SINEREF` |
| `LG-10` | `LP-10-OFF`, `BOOT`, `IDLE`, `MOTION`, `OBSTACLE`, `EDGE`, `FAULT` |

Suffix conventions:

| Suffix | Meaning |
|---|---|
| `OFF` | Verified removed/disabled electrical state |
| `BOOT` | Cold start through the group's ready or safely inhibited state |
| `IDLE` | Powered baseline without the group's active workload |
| `PWRRESTORE` | Power reapplied while local control remains inhibited |
| `BRAKE` | Controlled cancellation/deceleration profile |
| `FAULT` | Fault detection/reporting workload, not an assumed zero load |
| `*REF` | Bench reference or stress profile; not ordinary operation unless separately registered |

## 5. Fault labels — `F-*`

Every fault carries four obligations: **inhibit** affected hazardous output, **reject** obsolete work, **expose** health, and **recover** only from current authorized intent.

| ID | Fault | ID | Fault |
|---|---|---|---|
| `F-01` | Behaviour process loss | `F-12` | E-stop asserted mid-motion |
| `F-02` | Full SBC loss/reboot | `F-13` | E-stop released |
| `F-03` | Internal-link cable loss | `F-14` | Command flood/queue overflow |
| `F-04` | Internal-link corruption | `F-15` | SBC clock jump/time-sync corruption |
| `F-05` | Stale/late internal-link commands | `F-16` | Low/critical battery threshold crossing |
| `F-06` | C2 restart mid-gesture | `F-17` | Control-app session/link loss |
| `F-07` | Display-board restart | `F-18` | Charge-input or charger-status loss |
| `F-08` | Servo absent/bus fault | `F-19` | Safety sensor absent, stale or implausible |
| `F-09` | Camera absence | `F-20` | Provider/authentication/late-response failure |
| `F-10` | Network/cloud loss | `F-21` | Microphone/front-end absence |
| `F-11` | Single-subsystem brownout | `F-22` | Base-controller restart during motion |

## 6. Gate labels — `RP02-G*`

| ID | Gate | Character |
|---|---|---|
| `RP02-G01` | Protection | Verification of isolation, protection, sizing assumptions and bounded energy paths |
| `RP02-G02` | Peak coexistence | Rehearsal of the standing per-case rail/reset/data/thermal invariant |
| `RP02-G03` | Runtime | Candidate-pack rehearsal of `MD-01`; not integrated endurance closure |
| `RP02-G04` | Fault containment | Inhibit/reject/expose/recover verification with zero obsolete motion |
| `RP02-G05` | Control feasibility | Loop, link, timestamp and watchdog performance with margin |
| `RP02-G06` | Serviceability | Isolation, charging, pack removal, measurement and module-access paths |

## 7. Part-2 design-basis labels

### 7.1 Approved principles — `EDB-*`

| ID | Label | Definition |
|---|---|---|
| `EDB-01` | Scope boundary | Complete low-voltage system from battery/charge input to load terminals, including power-related control signals; AC mains excluded. |
| `EDB-02` | Sources of truth | Separates state/profile, numeric-ledger, design-basis, architecture and gate ownership. |
| `EDB-03` | Electrical requirement record | One normalized contract for every source interface, load boundary and physical distribution branch. |
| `EDB-04` | Electrical safety invariants | Safe boot, stop, recovery, containment, charging, connection and stored-energy rules. |
| `EDB-05` | Criticality classes | Functional failure criticality independent of the eventual number of physical rails. |
| `EDB-06` | Evidence versus decision status | Evidence quality and approval/selection/verification are independent axes. |
| `EDB-07` | Margin policy | Mechanism-specific margins reported at component terminals; no universal percentage. |
| `EDB-08` | Completion rule | Coverage, ownership, traceability and unknown-handling conditions for closing the design basis. |

### 7.2 Electrical criticality classes — `EC-*`

| ID | Label | Meaning |
|---|---|---|
| `EC-S` | Safety supervision | Must remain valid while hazardous energy is present or being removed; includes C2 and required power/E-stop sensing. |
| `EC-H` | Hazardous energy | Actuators and power stages capable of producing motion or force. |
| `EC-C` | Mission compute | Failure is tolerable only when local safety keeps all motion bounded. |
| `EC-N` | Non-hazardous/shedable | Display, camera, microphones, amplifier and lighting as applicable. |
| `EC-Q` | Charging supervision | Charger, pack monitor and minimum charging-status path. |

Criticality is not topology. Two classes may share an upstream source only if the later architecture proves the required fault containment. In particular, approval of `EDB-05` requires C2 safety supervision to be independent of the display failure branch.

### 7.3 Physical power branches — `PB-*`

These labels are registered under `RP02-P2-REG-01`.

| ID | Label |
|---|---|
| `PB-MAIN` | Protected battery operating source |
| `PB-CHARGE-IN` | Protected external low-voltage charge input |
| `PB-CHARGE-LOGIC` | Restricted charging source for C2/minimum supervision and display only |
| `PB-SAFE-C2` | Independent C2 safety-supervision branch |
| `PB-SAFE-BASE` | Independent base safety/sensing branch |
| `PB-COMPUTE` | Main SBC compute branch |
| `PB-DISPLAY` | Display/status branch |
| `PB-AUDIO-OUT` | Speaker/amplifier branch |
| `PB-CAMERA` | Camera branch downstream of the selected SBC interface |
| `PB-AUDIO-IN` | Microphone/front-end branch; source remains selection-dependent |
| `PB-MOTOR` | System-armed, hardware E-stop-gated motor-energy bus |
| `PB-HEAD` | Head-actuator upstream branch |
| `PB-HEAD-Y` | Yaw-servo branch |
| `PB-HEAD-P` | Pitch-servo branch |
| `PB-HEAD-R` | Roll-servo branch |
| `PB-HEAD-Y/P/R` | Compact notation applying to the three separate head-axis branches; not a fourth branch |
| `PB-DRIVE` | Drive-stage upstream branch |
| `PB-DRIVE-L` | Left drive output |
| `PB-DRIVE-R` | Right drive output |
| `PB-DRIVE-L/R` | Compact notation applying to both separate drive outputs; not a third output |

### 7.4 Power-architecture decisions — `PA-*`

These labels describe the registered `power-architecture.md` v0.2 baseline.

| ID | Label |
|---|---|
| `PA-01` | Four failure-consequence power domains |
| `PA-02` | Layered protection without a preselected device class |
| `PA-03` | Pack construction remains open and is evaluated as an assembly |
| `PA-04` | Pack and head-servo voltage remain coupled |
| `PA-05` | Dedicated compute converter and failure branch |
| `PA-06` | Three functional moving-harness paths across yaw |
| `PA-07` | Required safe brownout outcome; detailed `BR-*` policy issued, numeric thresholds deferred |
| `PA-08` | Architecture-level measurement points |
| `PA-09` | Restricted charging source cannot power ordinary operation |
| `PA-10` | Independent electrical observation for low/critical-energy policy |
| `PA-11` | Independent C2 and base-safety branches |
| `PA-12` | Separately containable application branches |
| `PA-13` | System-armed, E-stop-dominant hazardous motor-energy path |
| `PA-14` | Supervised `OFF/OPERATE/CHARGE` power-control function |
| `PA-15` | Common-reference star return with current-path separation |
| `PA-16` | Explicit partial-power and back-power cases |

### 7.5 Power-component candidates — `PCD-*`

`PCD-*` records are screening identities, not selected components. The middle class gives the component function:

| Class | Meaning |
|---|---|
| `PCD-CVT-*` | DC/DC converter candidate |
| `PCD-PRO-*` | Fuse, e-fuse or protection candidate |
| `PCD-EST-*` | E-stop operator or motor-arm switching candidate |
| `PCD-CON-*` | Connector/interconnect candidate |
| `PCD-CAB-*` | Conductor or moving-cable candidate |
| `PCD-CHG-*` | Charge-inlet, negotiation or charger/power-path candidate |

The associated screening dispositions are:

| Label | Meaning |
|---|---|
| `Lead` | Best presently documented route into schematic or bench evaluation; not selected |
| `Conditional` | Admissible only if the stated missing evidence closes |
| `Bench-only` | Useful for characterization but missing an installed-product requirement |
| `Hold` | Potentially admissible, but an upstream decision is absent |
| `Reject` | Fails a registered contract for the stated use or lacks minimum engineering evidence |

### 7.6 Brownout, reset and restart — `BR-*`

These labels define behavior and calculation ownership. They do not select a detector, converter, battery, threshold or capacitor.

| ID | Label |
|---|---|
| `BR-01` | Energy observation independent of the SBC |
| `BR-02` | Low energy cancels the active action and motor-enable epoch |
| `BR-03` | Critical energy reaches motor-safe state before unreliable control |
| `BR-04` | Fast collapse bypasses graceful compute sequencing |
| `BR-05` | Motor permission includes energy, E-stop, charge, arm and local-readiness terms |
| `BR-06` | Every controller or converter reset boots electrically inhibited |
| `BR-07` | Recovery consumes fresh mode/arm/enable/action intent |
| `BR-08` | Assertion and clearance use distinct proof and hysteresis |
| `BR-09` | Charge-source loss cannot restore ordinary operation |
| `BR-10` | Thresholds are calculated from selected hardware, then measured |

| Brownout label | Meaning |
|---|---|
| `ENERGY_OK` | Fail-inactive hardware/local proof that source and safety margins still permit motor authority; not a state-of-charge estimate |
| `MOTOR_PERMIT` | Physical permission formed from E-stop, system arm, charge absence, `ENERGY_OK` and installed-controller readiness; software cannot override a false term |
| Action/arm epoch | Session identity that makes pre-fault enables, goals and acknowledgements stale after energy loss, reset, E-stop or source transfer |
| Controlled depletion | Slow-enough loss that the registered `EN-02 → EN-03` stop and sign-off sequence remains credible |
| Fast collapse | Loss too fast or invalid to credit graceful sequencing; hardware/local motor inhibit acts immediately |

## 8. Evidence, decision and result labels

### 8.1 Evidence class

| Label | Meaning |
|---|---|
| `U` | Unknown or unselected; always non-zero unless a verified `OFF` state applies. |
| `E` | Estimate from calculation, analogy or characterized substitute; planning only. |
| `D` | Manufacturer datasheet or official documentation value; planning evidence. |
| `W` | Measured on the exact hardware in the exact recorded configuration, with a run ID and uncertainty. |

### 8.2 Decision status

| Label | Meaning |
|---|---|
| Proposed | Candidate requirement or design awaiting approval. |
| Approved requirement | Normative requirement accepted before scored evidence is inspected. |
| Selected design value | Architecture or component value chosen through the applicable decision process. |
| Verified result | Implemented value or property supported by registered evidence. |

Decision status never upgrades evidence class. A builder-approved estimate is still `E`.

### 8.3 Gate/ADR outcomes

| Label | Meaning |
|---|---|
| Pass | Registered criterion satisfied under the recorded configuration. |
| Iterate | Design changes and the affected evidence is rerun. |
| Reject | Candidate is removed from consideration for the stated reason. |
| Defer | Not available for a required Core outcome; an unmet Core gate must drive iteration or rejection. |

### 8.4 Power disposition

| Label | Meaning |
|---|---|
| `OFF` | Verified electrically removed or disabled at the stated boundary. |
| `INHIBITED` | Powered or power-capable, but hazardous output cannot be accepted; not equivalent to `OFF`. |
| `IDLE` | Powered and supervising without the active workload. |
| `ACTIVE` | Producing the named `LP-*` workload. |
| `SHED` | Deliberately removed by energy or thermal policy while higher-priority functions remain. |
| `SETTLE` | Temporary bounded actuator energy used only to reach a registered safe state. |
| `U` | Implementation or disposition unknown; not equivalent to `OFF`. |

## 9. Evidence-channel labels

| Label | Meaning |
|---|---|
| `V/I` | Load-end voltage and signed branch current |
| `RST` | Reset reason and reset count |
| `CRC` | Link integrity/error counters |
| `T` | Temperature at a named measurement point |
| `τ` | Timestamped latency, duration or jitter |
| `E` in an evidence-channel column | Integrated energy; distinct from evidence class `E`, which is identified explicitly as a class |
| `LOG` | Commands, acknowledgements, transitions, health and terminal state |

## 10. Protocol labels currently used by RP-02

These are interface labels from `link-contract.md`, not registered Part-1 state namespaces. Part 3 fixes their ownership and physical paths; Part 4 registers the C0↔C2 message set and safety semantics. Message-layout and numeric timing changes remain versioned in the ICD.

| Family | Labels |
|---|---|
| Session/authority | `HELLO`, `LIMITS_SET`, `HEAD_ENABLE`, `HEAD_INHIBIT` |
| Commands | `HEAD_GOAL`, `HEAD_CANCEL`, `FACE_STATE`, `LIGHT_STATE` |
| Feedback/health | `HEAD_STATE`, `HEARTBEAT`, `FAULT`, `ACK`, `NACK` |
| Time | `TIME_SYNC_REQ`, `TIME_SYNC_RESP` |
| Controller state | `inhibited`, `enabled`, `braking`, `fault` |
| Health encoding | `available`, `degraded`, `unavailable`, `unsafe` |
| Energy encoding | `normal`, `low`, `critical`, `charging` |
| Common `NACK` reasons | `EXPIRED`, `OUT_OF_LIMITS`, `INHIBITED`, `UNKNOWN_TYPE`, `BAD_CRC`, `QUEUE_FULL`, `NO_LIMITS`, `NONCE_REPLAY` |

## 11. Common electrical terms

| Term | Meaning in RP-02 |
|---|---|
| SBC / C0 | Body-mounted Raspberry Pi 5 Linux application computer responsible for high-level perception, behaviour, audio, UI, logging and the master timebase. |
| C2 | Independent ESP32-S3 head-motion/safety controller; owns trajectory limits, watchdog response and stale-command rejection for the head. |
| C3 / base MCU | Independent ESP32-S3 drive/base-safety controller; owns wheel loops, local hazards/reflexes, odometry capture, readiness and stale-command rejection for the base. |
| D1 | The selected display board's ESP32-S3 face renderer; owns LVGL/panel timing but no motion or safety authority. |
| Domain | Power/failure-containment region. A domain does not necessarily imply galvanic isolation. |
| Rail | Named regulated or direct electrical supply with a defined voltage envelope. |
| Branch | One protected/switched path from a distribution point to a load boundary. |
| Return | The complete current path back to the source; never assumed to be an ideal zero-voltage node. |
| BMS/PCM | Battery/pack protection electronics; exact functions must be stated rather than inferred from the name. |
| UVLO | Undervoltage lockout threshold and behaviour of a converter or load. |
| Brownout | Supply excursion that degrades or resets a powered device before orderly shutdown. |
| Inrush | Short startup current caused by input capacitance, converters, motors or load enable. |
| Regeneration | Reverse energy flow from a decelerating actuator into its rail/source. |
| Back-power | An unintended source energizing a supposedly isolated domain through signal, USB, programming, charger or protection paths. |
| Protection coordination | Curve- and impedance-based proof that operating profiles do not nuisance-trip and faults clear before protected paths overheat. |
| Selectivity | Required ordering in which a downstream protective element contains its branch fault before upstream/main protection acts. |
| E-stop | Latching physical action that removes hazardous motor-domain energy independently of high-level software. |
| Main isolation | Service/emergency disconnection of the onboard source from the complete robot, distinct from the motor-only E-stop. |
| Credible peak | Profile alignment allowed by actual registered behaviour, represented by `CC-PEAK-*`. |
| Synthetic stress | Intentionally non-behavioural simultaneous maxima, represented by `ST-*`. |
| Terminal margin | Voltage/current/thermal margin evaluated at the actual load terminals, including source, protection, connector, conductor and return losses. |

## 12. RP-02 execution phases

| Label | Meaning |
|---|---|
| Phase A | Controller/link and distribution preparation with bench supply and available low-power hardware; no battery requirement. |
| Phase B | Representative real head/compute/audio loads plus characterized substitutes where permitted; establishes load and coexistence evidence short of final drive/pack closure. |
| Phase C | Protected onboard-energy configuration after the written battery procedure and equipment gate; rehearses charging and `MD-01` energy margin. |

## 13. External namespaces referenced by RP-02

These identifiers are owned outside the RP-02 folder. This glossary explains why they appear but does not redefine them.

| Namespace | Meaning | Typical owner |
|---|---|---|
| `RP-*` | Risk prototype | `risk-prototype-plan.md` |
| `ADR-*` | Architecture decision record | system architecture decision set |
| `AD-*` | System architecture/design decision | `system-design-brief.md` or named system study |
| `SC-*` | Success criterion | foundation/system requirements |
| `SC-TBD-*` | Success threshold intentionally awaiting preregistration | system requirements and `gates.md` |
| `CON-*` | Project constraint | foundation/system requirements |
| `CON-P*` | Physical/safety constraint | system requirements |
| `SCOPE-*` | Approved product-scope statement | foundation scope documents |
| `HM-*` | RP-01 head-motion definition | `RP-01-head/intent.md` |
| `CAD-*` | Mechanical/CAD interface or gate | RP-01/RP-06 CAD records |
| `M*` | Mass-ledger item or assembly identifier | `mass-envelope-ledger.md` and RP-01 mass records |

## 14. Registration and change rule

- Registered Part-1 identifiers are append-only under `RP02-P1-REG-01`.
- A semantic change to a registered label requires a new ID or explicit supersession record.
- Proposed identifiers may change until registered, but their decision history must remain reviewable. `PA-*`/`PB-*` are append-only under `RP02-P2-REG-01`; `CA-*` is append-only under `RP02-P3-REG-01`.
- A new `EDB`, `EC`, `PA`, `CA`, candidate, load, case, profile, fault or gate label must be added here when introduced.
- Updating this glossary never by itself changes the canonical behaviour, numeric budget, component selection or gate threshold.
