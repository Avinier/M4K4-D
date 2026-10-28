# RP-02 Fault-Injection Matrix

| Field | Value |
|---|---|
| Status | **v0.3. `F-01…22` remain registered under Part 1; `F-23…30` are registered Part-3 extensions under `RP02-P3-REG-01`.** No injection performed and numeric G04 thresholds remain unregistered |
| Owner | Project builder |
| Created | 2026-09-08 |
| Authority | `../../01-system/risk-prototype-plan.md` v1.12 §RP-02; `compute-control-architecture.md` `CA-01…16`; RP02-G04 |
| Required behaviours | `../../01-system/system-design-brief.md` §6 failure priorities; `link-contract.md` §5; `compute-control-architecture.md` §5 |
| Success criteria | SC-15 controlled stop and failure; CON-11 and CON-P04 (safety independent of network) |
| Feeds | `gates.md` G04; ADR-03; ADR-12 |

G04 requires four things of every injected fault, and they are separately observable: **inhibit** the affected hazardous output, **reject obsolete** commands, **expose health** state, and **recover only from current authorized intent**. The last two are the ones that get skipped: a system that stops correctly but resumes the interrupted gesture on reconnect fails G04.

## 1. Rules

1. **One fault at a time**, injected into a registered `CC-xx` qualification case named in the row. The state vector supplies the hazard; the fault supplies the trigger.
2. **Every row names its injection method** and it must be reproducible on the rig without special equipment beyond `rig.md`.
3. **Observables are logged, not watched.** Time-to-inhibit is measured from the injection timestamp (logged on the injecting device) to the first `BRAKE` sample in `HEAD_STATE`, on the common timebase.
4. **Failed injections stay in the record.** A fault that produced unbounded motion is the most valuable run RP-02 can produce.
5. The registered rows are append-only; a changed injection method is a new version.

## 2. Matrix

Columns: **Inhibit** — what must stop and by when (candidate). **Reject** — which obsolete commands must be refused. **Expose** — what the health/fault channel must show. **Recover** — the only permitted path back. **Evidence** — the logged observables that prove it.

### 2.1 High-level compute

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-01** | Behaviour process loss (SBC alive, process dead) | `CC-05` mid-gesture | `kill -9 makad-core`; `makad-hwd` remains alive | Authority lease expires; `makad-hwd` sends inhibit once and stops valid session heartbeats; `BRAKE` within lease + heartbeat bound | Any goal queued under the dead boot/session epoch is never executed | systemd/core failure plus C2/C3 session/heartbeat fault | Core restart creates a new boot/session epoch → handshake/limits → new arm nonce → **new** goal. The interrupted gesture is not resumed | Lease trace, `HEAD_STATE`/base state brake onset, and zero executions of old epoch/sequence after recovery |
| **F-02** | SBC full loss / reboot | `CC-03` wake rise | Open `PB-COMPUTE` at the distribution board; separately, `reboot` | As F-01; additionally C2 must not misinterpret SBC boot-time UART noise as frames | All | As F-01; C2 may drive D1 to a bounded local link-loss indication before expiry-to-idle, but cannot retain motion authority | SBC boots to a supervisor that **does not auto-enable**; enable requires the documented start sequence (SC-18) | Brake onset; CRC-error counter during boot noise; no `HEAD_ENABLE` before operator action |

### 2.2 Internal link

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-03** | Link loss (cable) | `CC-04` yaw search sector | Open each C0↔C2 differential pair separately, then the complete yaw-boundary link (rig switches in series) | `BRAKE` within candidate ≤ 200 ms | Everything in flight | C2 `FAULT(HB_TIMEOUT)`; SBC `last_rx_age` climbs → head `unavailable` | Reconnect → both sides' queues are already flushed → fresh enable sequence | Brake onset; SBC outbox depth at reconnect = 0; first post-reconnect frame is `HELLO` |
| **F-04** | Link corruption | `CC-05` gesture at 921 600 baud | Inject noise: a rig MOSFET pulling RX low for 10–100 µs bursts; separately run the harness alongside an unshielded servo lead during `CC-06` | No inhibit for isolated errors; `degraded` above registered rate; `inhibited` above higher rate | Any CRC-failing frame — never act on partially valid data | `crc_err_count` in `HEARTBEAT`; `degraded` health | Error rate falls below threshold → `available`; if inhibited, fresh enable required | CRC counter versus injection log; zero `ACK(OK)` for corrupted frames; no `HEAD_STATE` glitch |
| **F-05** | Link staleness (SBC alive, sends late) | `CC-09` tracking corrections | SBC-side artificial delay of 300 ms; separately freeze the source used for `valid_until` | Heartbeat may stay fresh, but stale `TRACK` goals drop so the head holds instead of lag-following | Expired frames → `NACK(EXPIRED)`; burst → `FAULT(EXPIRED_BURST)` | `NACK` reasons; tracking `degraded` | Remove delay; fresh goals accepted; enable only if fault latched | NACK log; `HEAD_STATE` shows hold |
| **F-14** | Flood / queue overflow | `OM-01 + BS-02` attentive idle | SBC sends `HEAD_GOAL` at 2 kHz | C2 `NACK(QUEUE_FULL)`, current segment remains clean | Overflow frames | `degraded` | Rate returns to normal | Loop-jitter p99 stays inside G05 |
| **F-15** | Clock jump on SBC | `CC-07B` external-service wait | `date -s` a wall-clock step; separately corrupt one `TIME_SYNC_REQ` offset | None — monotonic time unaffected; if monotonic source jumps, C2 degrades and uses local expiry | Frames violating reconciliation window | Time fault detail | Sync converges | Offset trace; zero motion artefact |

### 2.3 Controllers

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-06** | C2 restart mid-gesture | `CC-06` startle outbound | Reset DevKitC; separately task-watchdog stall and `PB-SAFE-C2` brownout; replay the pre-reset C0 `HELLO`/limits/enable | No stale goal after reboot; boot is inhibited with no limits loaded; old handshake cannot satisfy the fresh C2 boot challenge. Servo hold/torque-off comes from RP-01 HM-00 | Pre-reset RAM and old session frames | `HELLO` with reset reason | Fresh challenge/limits/enable sequence | Reset reason; challenge changes; first post-boot bus frame is safe torque state, not goal |
| **F-07** | Display board restart | `CC-03` | Reset display board | No hazardous effect; **must not** affect C2 | Expired face state decays to idle | Display `HELLO` | Automatic | `HEAD_STATE` continuous through reset |
| **F-08** | Servo absent / bus fault | `CC-05` | Unplug one servo bus connector mid-gesture; separately short data briefly | Missing axis unavailable; other axes brake; head inhibited | Missing-axis goals | `FAULT(SERVO_SILENT, axis)` | Reconnect, remain inhibited, fresh enable | Per-axis flags; no remaining-axis runaway |
| **F-09** | Camera absence | `CC-09` tracking | Power off, unplug non-hot-pluggable CSI, then boot without camera | Head holds; base stops because track evidence is gone | New `TRACK` goals | Perception unavailable | Restore camera; behaviour reissues current intent | No goals after loss; head returns to `BS-02` |
| **F-19** | Obstacle/edge safety sensor absent, stale or implausible | `CC-10C` floor obstacle and `CC-12C` caught tabletop edge | Unplug one sensor before boot; mask/freeze its update; inject out-of-range samples through the RP-03 interposer | Any motion requiring the missing coverage is inhibited or locally braked; other safe channels may remain | Motion request whose safety preconditions are no longer satisfied | Named sensor/coverage `HL-03/04` plus reason and age | Restore valid evidence; remain inhibited until local readiness and a fresh action/enable | Sensor-age/validity log, detection-to-brake timing, zero continuation into the uncovered hazard region |
| **F-22** | Base-controller restart during motion | `CC-09/09C` and `CC-10A/B` | Reset or watchdog-stall selected C3 on the RP-03 rig while C0 and C2 remain alive | Driver enters its hardware-safe state; no stale wheel command after reboot; whole motion action is cancelled/inhibited | Pre-reset wheel goals and active follow/come action instance | Base reset reason and unavailable/unsafe health | Base handshake/limits/readiness → `OM-03`; new Floor selection/enable and a new action instance are required | Driver-enable/rail and encoder trace, reset reason, zero post-reset wheel motion before fresh authorization |

### 2.4 Network and energy

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-10** | Network / cloud loss | `CC-07B` | Disable Wi-Fi; separately black-hole endpoint | Nothing physical; request times out and is indicated in character | Late response discarded | Interaction degraded; utility returns to face | Network returns; next request works | Timeout histogram; zero late-response actions |
| **F-11** | Single-subsystem brownout | `CC-06`, then synthetic `ST-01` | Insert resistance in servo rail so it sags while logic holds | Under-performance detected; servo reset follows F-08 | — | Per-axis degraded; rail logged | Remove load; fresh enable if inhibited | Per-rail trace proves logic stayed flat |
| **F-16** | Low-battery threshold crossed during head motion or locomotion | `CC-05/09`, then `CC-13H/D` and `CC-14` | Ramp through registered low/critical thresholds | Critical: brake/settle then inhibit/shutdown. Low: `EN-02` rules | Goals violating `EN-02/03` → `NACK(INHIBITED)` | Energy state | Fresh pack/charge → normal → fresh enable | Threshold timestamps versus brake |
| **F-17** | Control-app link loss while Floor mode is active | `CC-09`, then `CC-10B`; rejection check in `CC-12B` | Close the app, sever its WebSocket/control channel and separately disable its Wi-Fi path while the SBC/C2 link remains alive | Local authority initiates `EV-12` and enters `OM-03`; no dependency on a remote stop message | Current and queued behaviour/motion commands from the lost session | Mode-source/link health unavailable; reason identifies app-session loss | Reconnect → explicit new Floor selection → local readiness → fresh enable nonce → new behaviour request | Injection-to-brake and stop timing; mode transition; zero post-reconnect motion before the complete fresh sequence |
| **F-18** | Charge-input or charger-status loss | `CC-15` | Remove the keyed low-voltage DC input; separately open/corrupt the charger-status/telemetry connection using the rig interposer | Charging stops or the selected charger enters its documented safe state; motor domain remains inhibited | Previous operating mode and all old motion intents | `EN-04` exits and charge health becomes unavailable/faulted; display indicates the bounded result if supervision remains powered | Restore valid charge source/status for charging, or remove charge mode into `OM-03`; operation still requires a fresh mode/enable sequence | Charge and pack `V/I/T`; motor-rail zero; status timestamps; zero automatic return to Floor/Table or old motion |
| **F-20** | External authentication/provider failure or late/duplicate response | `CC-07B/E` and `CC-08` | Use an invalid/expired test credential; return provider error; delay and replay a captured response with the same action ID | No physical safety dependency; pending expressive/utility action cancels or fails boundedly | Response for terminal/unknown action ID, duplicate completion and unauthorized retry | Integration `HL-02/03`, exact error class and `AL-06` | Correct credentials/provider health; next user request creates a new action ID | Action-lifecycle trace, duplicate/late execution count=0, bounded failure/return-to-face timing |
| **F-21** | Microphone/front-end absent or capture unavailable | `CC-07A` and sleep-listening check in `CC-02F/T` | Boot with front end disconnected; disable/corrupt the capture device while preserving SBC health | No wake/request action is accepted from absent audio; existing hazardous motion is unaffected by fabricated commands because none are produced | Transcript/intent derived from missing or stale audio | Audio-input `HL-03`; status/failure visible through legal channels | Restore device; health check; next fresh utterance may create a new request | Audio availability and frame-age log, accepted intents=0 while absent, bounded indication and clean recovery |

### 2.5 Physical stop

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-12** | E-stop asserted mid-motion | `CC-06` and `CC-10A` | Press mushroom during outbound stroke/launch | Motor domain dead by hardware; C2 detects absence within one tick and enters `OM-04`. Logic stays up | Everything | Fault in heartbeat/face if desired | See F-13 | Motor rail to 0; logic flat; heartbeat continues |
| **F-13** | E-stop released | after F-12 | Twist to release | **Nothing moves and `PB-MOTOR` does not return merely on release.** C2 remains `inhibited`, the motor-arm latch remains clear and local enables remain inactive | Any goal until a fresh arm/readiness/enable sequence | Release status is exposed, but motion authority remains invalid | Operator-initiated fresh system arm, controller readiness/enable and new action | Motor rail/arm/enable trace plus zero motion for ≥10 s after release while stale/old-session goals all `NACK(INHIBITED)` |

### 2.6 Part-3 compute/control extensions

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-23** | Behaviour authority wedged but PID alive | `CC-05` and `CC-09` | `SIGSTOP makad-core` or a test hook that stops its event-loop progress while the process remains present | Authority lease expires; `makad-hwd` sends inhibit once and stops valid session heartbeat; C2/C3 brake locally | All commands from the frozen epoch | Core service watchdog and MCU session fault | systemd restart → new epoch and complete fresh-arm sequence | Lease age, watchdog event, inhibit/brake timing, old-epoch execution count = 0 |
| **F-24** | Hardware daemon / serial progress wedged | `CC-05` and `CC-09` | `SIGSTOP makad-hwd`; separately block each serial worker | C2/C3 heartbeat expiry contains motion independently | In-flight/outbox frames | systemd watchdog; C0 endpoint unavailable; MCU heartbeat fault | Service restart → new link sessions, queues empty, fresh arm | UART line trace, MCU brake onset, outbox reset and no replay |
| **F-25** | C2 external watchdog violation | `CC-05` | Stop the qualified feed; separately generate an early feed outside the allowed window | Hardware-qualified `C2_READY` withdraws and head motor permission drops independent of ESP-IDF | Current and queued head intent | Watchdog/reset cause and C2 unavailable/unsafe | Clear according to final latch circuit; C2 safe boot; fresh handshake/arm | WDI/WDO/READY/motor-gate scope trace and reset reason |
| **F-26** | C3 external watchdog violation | `CC-09/10A` | As F-25 on the base carrier during motion | `C3_READY` withdraws and base driver enters safe state within registered bound | Current and queued wheel intent | Watchdog/reset cause and base unavailable/unsafe | C3 safe boot; fresh mode/handshake/arm/action | WDI/WDO/READY/driver-enable and encoder trace |
| **F-27** | Display relay flood or stuck local bus | `CC-03/05` | Flood face frames at source; hold the D1 RS-485 pair busy/short through the rig | No head-motion inhibit unless shared C2 health genuinely degrades; C2 control deadlines remain met | Excess face frames; latest-wins queue drops older state | Display degraded/unavailable and relay-drop counter | Clear bus; D1 handshake/idle; no C2 re-arm unless C2 itself faulted | C2 jitter, head-link CRC, relay queue high-water/drop count and D1 recovery |
| **F-28** | Differential-link wiring/termination fault | `CC-04/05` | Remove termination, reverse one pair, short A/B briefly and inject common-mode/noise within fixture limits | Isolated errors degrade; sustained registered error rate inhibits | CRC/sequence-invalid frames | Per-link CRC/sequence/line health | Restore wiring; inhibited link requires new session/arm | A/B waveforms, CRC/sequence counters and zero corrupted-command execution |
| **F-29** | Log partition full or storage stalls | `CC-PEAK-01` / `ST-01` rehearsal | Fill dedicated writable quota; throttle/block nonessential log sink | Motion is not extended; if authority loop loses its deadline, normal lease expiry contains it | New nonessential captures after quota fault | Storage/log health degraded; dropped-log counter | Free/replace storage; explicit service recovery; no motor auto-arm | Lease timing, MCU link timing, write latency, drop count and absence of reboot loop |
| **F-30** | Node reset sequence and compatibility mismatch | Relevant `CC` for C0, C2, C3, D1 | Reset each node alone; replay old HELLO/ACK and an old challenge echo; present mismatched contract/config hash | Affected subsystem stays inhibited; installed safety-controller reset withdraws motor permission per `BR-05` | Old session, incompatible version/hash and delayed ACK | Named reset reason / `CONTRACT_MISMATCH` / config mismatch | Correct version → new controller challenge → time/limits/readiness → fresh arm and new intent | Boot ordering, challenge/READY/motor gate, session IDs and zero pre-arm motion |

## 3. Candidate G04 thresholds (not registered)

| Metric | Candidate | Applies to |
|---|---|---|
| Time from injection to `BRAKE` onset | ≤ 200 ms (heartbeat/lease-mediated); ≤ 1 control tick (locally detected: motor domain, servo/safety sensor/base controller) | F-01…F-03, F-06, F-08, F-12, F-19, F-22…26 |
| Obsolete commands executed after any fault | **0** across the whole campaign | All |
| Health state correct in `HEARTBEAT` | within 2 heartbeat periods (≤ 100 ms) | All |
| Motion after any recovery without a fresh enable sequence | **0** | All |
| CRC/sequence error rate → `degraded` / `inhibited` | to be registered from the F-04/F-28 static, flexing and motor-noise harness measurements, not chosen in advance | F-04, F-28 |
| Repetitions | 5 per row minimum; every row in at least two different registered states where the fault is meaningful; charging-only F-18 instead uses two charger/source conditions | All |

## 4. Campaign order

Injections are ordered by increasing authority: F-15, F-14 and F-04 first; then F-27…29 on non-actuating/dummy loads; then F-05, F-07, F-10, F-20 and F-21; then F-17 and F-23/F-24; then F-01, F-02, F-03, F-06, F-08, F-25 and F-30 with representative servo load; then F-19, F-22 and F-26 on the guarded RP-03 rig; then F-11/F-16 supply ramps; then F-18 after the charge path exists. F-12/F-13 run **every session** and are additionally scored under `CC-06` and `CC-10A` when drive hardware exists.

## 5. Registration record

| Registration | Date | Approved scope | Not yet registered |
|---|---|---|---|
| `RP02-P1-REG-01` | 2026-09-15 | `F-01…F-22`, their primary cases, injection intents, inhibit/reject/expose/recover obligations and campaign ordering; explicit builder approval in the project conversation | Hardware-specific injection fixtures, repetitions/configurations and numeric G04 thresholds before scored runs |
| `RP02-P3-REG-01` | 2026-09-16 | `F-23…F-30` compute/control extensions: authority and hardware-daemon wedges, C2/C3 external watchdogs, display-relay isolation, differential-link faults, storage backpressure and node reset/version sequencing | Exact watchdog/link/storage hardware, injection fixture details and numeric timing/error thresholds before scored runs |

Part-2 implementation maintenance note, 2026-09-16: F-13 now reflects the stricter already-registered `PA-13`/implementation-basis rule that E-stop release cannot itself restore `PB-MOTOR`. This tightens the electrical implementation without weakening the Part-1 no-motion/fresh-authorization obligation. F-11/F-16 electrical ordering and reset/recovery details are owned by `brownout-restart-contract.md` v0.1; their numeric injection thresholds remain preregistered run values.
