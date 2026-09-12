# RP-02 Fault-Injection Matrix

| Field | Value |
|---|---|
| Status | **Rows proposed; no injection performed; no threshold registered** |
| Owner | Project builder |
| Created | 2026-09-08 |
| Authority | `../../01-system/risk-prototype-plan.md` v1.11 §RP-02 (inject "high-level process loss, internal-link loss/corruption or staleness, controller restart, sensor absence, network loss, and one allowed subsystem brownout at a time"); RP02-G04 |
| Required behaviours | `../../01-system/system-design-brief.md` §6 failure priorities; `link-contract.md` §5 |
| Success criteria | SC-15 controlled stop and failure; CON-11 and CON-P04 (safety independent of network) |
| Feeds | `gates.md` G04; ADR-03; ADR-12 |

G04 requires four things of every injected fault, and they are separately observable: **inhibit** the affected hazardous output, **reject obsolete** commands, **expose health** state, and **recover only from current authorized intent**. The last two are the ones that get skipped: a system that stops correctly but resumes the interrupted gesture on reconnect fails G04.

## 1. Rules

1. **One fault at a time**, injected into a *registered state* named in the row. The state supplies the hazard; the fault supplies the trigger.
2. **Every row names its injection method** and it must be reproducible on the rig without special equipment beyond `rig.md`.
3. **Observables are logged, not watched.** Time-to-inhibit is measured from the injection timestamp (logged on the injecting device) to the first `BRAKE` sample in `HEAD_STATE`, on the common timebase.
4. **Failed injections stay in the record.** A fault that produced unbounded motion is the most valuable run RP-02 can produce.
5. Rows are append-only once registered; a changed injection method is a new version.

## 2. Matrix

Columns: **Inhibit** — what must stop and by when (candidate). **Reject** — which obsolete commands must be refused. **Expose** — what the health/fault channel must show. **Recover** — the only permitted path back. **Evidence** — the logged observables that prove it.

### 2.1 High-level compute

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-01** | Behaviour process loss (SBC alive, process dead) | S06 mid-gesture | `kill -9` the process that owns the heartbeat | `BRAKE` within heartbeat timeout + 1 tick (candidate ≤ 200 ms) | Any `HEAD_GOAL` queued in the dead process is never executed | C2 `FAULT(HB_TIMEOUT)`; SBC supervisor marks head `unavailable` | Process restart → `HELLO` → `LIMITS_SET` → `HEAD_ENABLE`(new nonce) → **new** goal. The interrupted gesture is not resumed | `HEAD_STATE` trace showing brake onset; ACK/NACK log showing zero executions of pre-fault seq numbers after recovery |
| **F-02** | SBC full loss / reboot | S04 wake rise | Cut Buck A (SBC rail) at the distribution board; separately, `reboot` | As F-01; additionally C2 must not misinterpret SBC boot-time UART noise as frames | All | As F-01; C2 heartbeat continues to display board so the face can show a fault expression if RP-04 later wants it | SBC boots to a supervisor that **does not auto-enable**; enable requires the documented start sequence (SC-18) | Brake onset; CRC-error counter during boot noise; no `HEAD_ENABLE` before operator action |

### 2.2 Internal link

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-03** | Link loss (cable) | S05 yaw sweep | Pull the yaw-boundary connector's UART pair (or a rig switch in series) | `BRAKE` within candidate ≤ 200 ms | Everything in flight | C2 `FAULT(HB_TIMEOUT)`; SBC `last_rx_age` climbs → head `unavailable` | Reconnect → both sides' queues are already flushed → fresh enable sequence | Brake onset; SBC outbox depth at reconnect = 0; first post-reconnect frame is `HELLO` |
| **F-04** | Link corruption | S06 gesture burst at 921 600 baud | Inject noise: a rig MOSFET pulling the RX line low for 10–100 µs bursts at random intervals; separately, run the harness alongside an unshielded servo lead at S07 | No inhibit for isolated errors; `degraded` above the registered error rate; `inhibited` above the higher rate | Any frame failing CRC — **never** act on a partially valid frame | `crc_err_count` in `HEARTBEAT`; `degraded` health | Error rate falls below threshold → `available`; if `inhibited` was reached, fresh enable required | CRC counter versus injection log; zero `ACK(OK)` for corrupted frames; `HEAD_STATE` shows no glitch on corrupted `HEAD_GOAL` |
| **F-05** | Link staleness (SBC alive, sends late) | S11 `TRACK` corrections | SBC-side artificial delay of 300 ms on the outbox; separately, freeze the SBC clock source used for `valid_until` | Nothing to inhibit if heartbeat is fresh; **but** every stale `TRACK` goal is dropped so the head holds rather than chases old targets | All frames with `valid_until_us < now` → `NACK(EXPIRED)`; a burst → `FAULT(EXPIRED_BURST)` | `NACK` reasons; SBC sees its own goals rejected and marks tracking `degraded` | Delay removed → goals accepted again; no enable sequence needed unless `EXPIRED_BURST` latched | NACK log; `HEAD_STATE` shows hold, not lag-following |
| **F-14** | Flood / queue overflow | S03 | SBC sends `HEAD_GOAL` at 2 kHz | C2 `NACK(QUEUE_FULL)`, keeps executing the current segment cleanly | Overflow frames | `degraded` | Rate returns to normal | Loop-jitter p99 in `HEARTBEAT` stays within the G05 bound during the flood |
| **F-15** | Clock jump on SBC | S08 during a cloud round-trip | `date -s` a wall-clock step; separately, corrupt one `TIME_SYNC_REQ` offset | None — monotonic time must be unaffected; if the master's monotonic source itself jumps (bug), C2 marks time `degraded` and uses local expiry | Frames whose `src_ts_us` violates the reconciliation window | `degraded` with a time-fault detail | Sync converges → `available` | Offset estimate trace before/after; zero motion artefact |

### 2.3 Controllers

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-06** | C2 restart mid-gesture | S07 startle outbound | Press reset on the DevKitC-1 twin; separately, trigger the task watchdog with a deliberate stall; separately, brown out only the head-logic rail | Servos must not receive a stale goal on reboot; boot state is `inhibited` with **no limits loaded**. What the servos do while C2 is down (hold / torque-off) is the RP-01 HM-00 result, recorded here, not decided here | Anything in RAM before the reset | `HELLO` with reset reason; `BROWNOUT_RESET` flag when applicable | Fresh enable sequence from the SBC | Reset-reason register logged; first bus frame after reboot is torque-state per HM-00, not a goal |
| **F-07** | Display board restart | S04 | Reset the display board | None hazardous — the face goes dark then returns to idle. **Must not** affect C2 (separate board, separate UART, separate 5 V branch fuse) | Expired `FACE_STATE` decays to idle | SBC sees display `HELLO` again | Automatic — the face is not a hazardous output | `HEAD_STATE` continuous through the display reset; proves the C1-rejection reasoning physically |
| **F-08** | Servo absent / bus fault | S06 | Unplug one servo's bus connector mid-burst; separately, short the bus data line briefly | That axis `unavailable`; the other two complete `BRAKE`; head `inhibited` | Goals for the missing axis | `FAULT(SERVO_SILENT, axis)` | Servo reconnected → still `inhibited` → fresh enable | Per-axis flags in `HEAD_STATE`; no runaway on the remaining axes |
| **F-09** | Camera absence | S11 tracking | Unplug CSI at the head end (power off first — CSI is not hot-pluggable) then power on without camera | None on the head; base motion (when present) must stop because tracking evidence is gone (SC-15) | `TRACK` goals stop being generated | Perception `unavailable`; head falls to attentive idle | Camera restored → perception `available` → behaviour re-issues intent | Behaviour log: no `TRACK` goals after loss; head holds last safe pose then returns to S03 |

### 2.4 Network and energy

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-10** | Network / cloud loss | S08 mid-request | Disable Wi-Fi; separately, black-hole the cloud endpoint so the request hangs | **Nothing physical** — CON-11: local motion safety is independent of the network. The pending request times out per SC-TBD-14 and is indicated in character | Late cloud responses after timeout are discarded, never acted on | Interaction `degraded`; utility view returns to face | Network returns → next request works; nothing to re-enable | Timeout latency histogram; zero actions from post-timeout responses; head/base unaffected |
| **F-11** | Single-subsystem brownout | S07 startle at S13 composite load | Rig: insert series resistance in the servo rail only, so it sags below the servo's minimum while logic rails hold | Servos under-perform → C2 sees tracking error and current anomaly → reports; if a servo resets, F-08 path | — | `degraded` per axis; rail voltage in the run log | Load removed → servo recovers → fresh enable if it reached `inhibited` | Per-rail voltage trace proving the **logic rails did not dip** (PA-05/PA-07 verification) |
| **F-16** | Low-battery threshold crossed mid-gesture | S06 | Rig supply ramped through the registered `low` and `critical` thresholds under load | At `critical`: `BRAKE` to rest pose, then `inhibited` (S16). At `low`: registered inhibitions of S14 apply | New goals that violate S14 inhibitions → `NACK(INHIBITED)` | Energy state in `HEARTBEAT` | Charging or a fresh pack → normal → fresh enable | Threshold crossing timestamps versus brake onset |

### 2.5 Physical stop

| ID | Fault | Injected into | Method | Inhibit | Reject | Expose | Recover | Evidence |
|---|---|---|---|---|---|---|---|---|
| **F-12** | E-stop asserted mid-motion | S07 | Press the mushroom during the outbound stroke | Motor domain dead by hardware; C2 detects `motor_domain=absent` within one tick, latches `FAULT(MOTOR_DOMAIN_LOST)`, state `inhibited`. **Logic domain stays up** (PA-01) | Everything | Fault visible on the face if RP-04 wants it; in `HEARTBEAT` regardless | See F-13 | Servo rail trace to 0 V; head-logic and compute rails flat; `HEARTBEAT` continues |
| **F-13** | E-stop released | after F-12 | Twist to release | **Nothing moves.** Servos regain power but C2 is `inhibited` with the fault latched; servos boot into their own power-on state, which must be torque-off or hold — never a stored goal | Any goal until re-enabled | Fault clears only on explicit `HEAD_INHIBIT`+`HEAD_ENABLE` sequence | Operator-initiated fresh enable | Zero motion for ≥10 s after release with the SBC actively sending goals — the goals must all `NACK(INHIBITED)` |

## 3. Candidate G04 thresholds (not registered)

| Metric | Candidate | Applies to |
|---|---|---|
| Time from injection to `BRAKE` onset | ≤ 200 ms (heartbeat-mediated); ≤ 1 control tick (locally detected: motor domain, servo silent) | F-01…F-03, F-06, F-08, F-12 |
| Obsolete commands executed after any fault | **0** across the whole campaign | All |
| Health state correct in `HEARTBEAT` | within 2 heartbeat periods (≤ 100 ms) | All |
| Motion after any recovery without a fresh enable sequence | **0** | All |
| CRC error rate → `degraded` / `inhibited` | to be registered from the F-04 harness measurement, not chosen in advance | F-04 |
| Repetitions | 5 per row minimum; every row in at least two different registered states | All |

## 4. Campaign order

Injections are ordered by increasing authority, as RP-07 does: F-15, F-14, F-04 first (no motion consequence); then F-05, F-07, F-10 (bounded, no hardware risk); then F-01, F-02, F-03, F-06, F-08 with servos under representative load; then F-11, F-16 with the supply ramps; F-12/F-13 are run **every session** as the `workbench.md` E-stop check and additionally scored once under S07.

## 5. Registration record

*(none yet)*
