# RP-04 Coordination Interface Requirements

| Field | Value |
|---|---|
| Status | Early cross-prototype request v0.4 — **semantics accepted** `RP02-P4-REG-03` 2026-09-21 (`link-contract.md` v0.6). Exploratory packed layout revision 2 is a host reference, not a registered wire layout. Audio onset (IR-06) and composer snapshot (IR-10) stay on C0 |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Consumes | [`intent.md`](intent.md), [`situations.md`](situations.md), RP-02 `link-contract.md` v0.6, `compute-control-architecture.md`, `../../01-system/timebase.md` v0.2 |
| Feeds | RP-02 exact byte-layout/schema work; later RP-04 runtime architecture, G01/G02/G04 |

## 1. Purpose and boundary

RP-04 owns **coordination middleware** above already-decided transports:

| Already decided (do not reopen here) | Authority |
|---|---|
| No ROS 2 or micro-ROS in the V1 safety path | `CA-07` |
| Differential UART C0↔C2 and C0↔C3 | `CA-05` |
| C2 relays semantic face/light to D1 | `CA-04` |
| Framed semantic MCU messages; COBS/CRC/session/expiry | `link-contract.md` |
| C0 service split; Unix-domain sockets for local IPC | `CA-07`, `CA-08` |
| Latest-wins control queues; faults latched; arm requires ACK | `CA-12` |

This file states required **semantics** for performance identity, scheduled onset (as a comparison option), executor events, denial reasons, and joined logs. RP-02 remains the owner of the link contract, field widths/order, codec schema, rates, queues, and registration.

If Part 2/3 prove an inherited decision inadequate for a Core situation, RP-04 issues a dated change request with the situation ID and evidence. It does not fork a second ICD.

What RP-04 still has to decide locally (not in this RP-02 request): performance representation, C0 event/action API, scheduler/executor, cancellation protocol among `makad-*` services, correlation/tracing, score loading/versioning/replay.

## 2. Mandatory performance correlation

### IR-01 — performance identity

Every expressive command and corresponding state/onset/failure record must carry or be losslessly associated with:

- `perf_id`: identifies one semantic performance definition/version;
- `perf_epoch`: monotonically increasing instance identity within the active C0 boot/session, so a reused `perf_id` cannot join to an earlier run;
- `cue_id`: identifies the beat/cue inside that performance.

The exact widths are an RP-02 layout decision. A 16-bit `perf_id` and 8-bit `cue_id` alone are insufficient as instance identity if IDs are reused; the active C0 boot UUID/session epoch plus a performance epoch may provide uniqueness.

Required coverage:

| Surface | Required association |
|---|---|
| `HEAD_GOAL`, `HEAD_CANCEL`, `HEAD_STATE`, head ACK/NACK/fault | Performance instance and cue/segment |
| `BASE_GOAL`, base cancel/inhibit, `BASE_STATE`, base ACK/NACK/hazard/fault | Performance instance and cue/profile |
| `FACE_STATE` and renderer frame-flip feedback | Performance instance and cue/expression transition |
| `LIGHT_STATE` and actual light-onset feedback | Performance instance and cue/pattern transition |
| C0 audio request, callback, stop/underrun | Performance instance and cue/audio primitive |
| Composer and C0-service logs | Score version, intended anchor/phase, dispatch and branch decision |

Clock alignment alone is not an admissible join key.

### IR-02 — stale-epoch rejection

After cancel, higher-priority intent, reconnect, or C0 restart, an old performance instance cannot start a new cue. Executors must reject or discard stale identity under the existing session/epoch and bounded-queue rules. A new performance is a new epoch, not a continuation with the same cue IDs.

## 3. Optional scheduled execution support

### IR-03 — `start_at_us` semantic

RP-02 should reserve an optional master-monotonic `start_at_us` so a time-triggered or hybrid family can be compared honestly on `HEAD_GOAL`, `BASE_GOAL`, and `FACE_STATE`; equivalent scheduled semantics are required for light and C0 audio even if they do not traverse the same wire.

- `0` means execute as soon as accepted under current immediate semantics.
- Non-zero means do not begin before that master timestamp.
- Expiry is checked at execution, not only receipt. `start_at_us > valid_until_us` is rejected.
- Local safety, mode, limit, and inhibit checks remain authoritative at execution.
- If the time model is invalid or its uncertainty exceeds the registered bound, the executor must reject scheduled execution with a distinguishable reason; it must not silently execute immediately.
- Late arrival uses a registered policy: reject as late, or execute only inside a registered lateness window. This is never an implicit choice.

Adding the field does not select a time-triggered scheduler. Omitting it would silently remove TIME-tagged cues from a **physical** comparison. Phase A **already modelled** `start_at_us` in `prototype/`; RP-02 rejection penalizes physical TIME tags and does not require deleting that evidence.

## 4. Onset and completion observability

### IR-04 — executor events

For each cue, expose separate source-stamped events when applicable:

1. command receipt and validation result;
2. local execution start;
3. first actuator/renderer/audio output onset observable at the source;
4. progress or meaningful phase transition;
5. completion and settled/hold state;
6. deny, expiry, inhibit, cancel, fault, or progress-stuck reason.

Existing `HEAD_STATE.gesture_id/segment/progress` is a starting point. Equivalent base progress and face/light/audio onset/completion evidence are required for progress-triggered scheduling and diagnosis.

### IR-05 — face onset

D1 reports the frame-flip timestamp for the first frame that visibly represents the requested `FACE_STATE`, correlated to the performance/cue. Receipt or render-queue insertion is not face onset.

### IR-06 — audio onset

C0 records the playback callback/device timestamp for the first submitted/played buffer, the completion callback, stop completion, and underrun. The score-request timestamp is not audio onset.

### IR-07 — light onset

The status-light executor reports or instrumentally verifies the actual output-transition timestamp. `LIGHT_STATE.sync_ts_us` is the requested synchronization time; it is not proof the LED changed then.

### IR-08 — motion onset and settle

Head/base state identifies first physical motion above the preregistered onset criterion and entry to the local settled/HOLD criterion. RP-04 may derive these offline from high-rate state only if raw source samples and criterion/version are retained.

## 5. Denial and degradation observability

### IR-09 — machine-readable outcome

Every cue outcome must distinguish at least:

- accepted/scheduled;
- started;
- completed/settled;
- cancelled;
- expired;
- late;
- inhibited by operating mode;
- unavailable/degraded;
- out of limits;
- queue full;
- time model invalid;
- superseded/stale performance epoch;
- progress stuck;
- renderer stall or audio underrun;
- safety/hazard stop.

RP-02 may map these into shared and subsystem-specific reason enums. A boolean success flag is insufficient for G02/G04.

### IR-10 — availability snapshot

At performance acceptance, the composer logs the availability/health/mode of all five channels and the oldest feedback age used to make the branch decision. A later denial is a new event, not a rewrite of the initial snapshot.

## 6. Timebase requirements

### IR-11 — timestamp form

All event timestamps follow `timebase.md`: master-monotonic microseconds after reconciliation, with raw local time and model version/uncertainty retained where the producer has a separate clock.

### IR-12 — uncertainty gates scoring

Every RP-04 run records achieved uncertainty per producer. If the uncertainty cannot resolve the registered onset/phase window, the run is exploratory. The composer may still operate safely; the evidence cannot score G01.

### IR-13 — wall-clock independence

A wall-clock step cannot move a scheduled cue, alter expiry, or join performance events. `F-15` remains the validation case.

## 7. Minimum joined log record

The eventual logging schema needs a row/event representation equivalent to:

| Field group | Required content |
|---|---|
| Run/config | `run_id`, config hashes, score/architecture/budget/gate versions, phase, channel availability, overlay IDs |
| Identity | C0 boot/session/epoch, `perf_id`, performance instance/epoch, `cue_id`, channel, C0 service |
| Intent/plan | semantic intent, anchor, intended relation or scheduled master time, permitted branch |
| Transport | source timestamp, sequence, dispatch, receipt, ACK/NACK, expiry |
| Execution | local start, source onset, progress, completion, settle, cancellation |
| Time quality | raw local timestamp, converted timestamp, model reference/version, uncertainty |
| Outcome | completed/denied/degraded/fault reason; final state/velocity where applicable |
| Witness | external-video cue association and frame/offset record |

File format is not selected here. The schema must support bounded runtime logging and post-run export without becoming a dependency for local safety (`CA-16`).

## 8. RP-02 disposition (`RP02-P4-REG-03`)

| Request | Disposition |
|---|---|
| Cue identity on head/base/face/light command, state, ACK | **Accepted** on the wire |
| Stale-epoch reject | **Accepted** — `NACK(STALE_EPOCH)` |
| Distinct invalid-time / late | **Accepted** — `NACK(TIME_MODEL_INVALID)` / `NACK(LATE)` in existing `u8` |
| Optional `start_at_us` | **Accepted** (0 = immediate). Lateness window numeric still open |
| Face / light source onset | **Accepted** — `FACE_REPORT` / `LIGHT_REPORT` |
| Head/base motion onset | **Accepted** — `onset_ts_us` on `HEAD_STATE` / `BASE_STATE` |
| Audio onset | **Not a wire field** — C0 `makad-audio` (IR-06) |
| Composer availability snapshot | **Not a wire field** — C0 log (IR-10) |
| UART / COBS / session | **Unchanged** |
| Packed widths, type numbers, `BASE_STATE` vs 64 B, lateness ms | **Exploratory layout revision 2** in RP-02 `phase-a/` (`schema.json`, `payloads.py`). `BASE_STATE` is 62 bytes with identity, onset, and safety fields retained. Lateness window numeric still open. Not G04/G05 registered |

Phase A virtual `start_at` evidence is unchanged. Physical TIME tags now have a semantic home; they still need a codec revision and G05.

## 9. Acceptance test obligations created by the interface

- replay an old performance epoch after cancel/reconnect and prove rejection;
- send a scheduled cue with invalid time model and prove distinguishable rejection;
- send a cue after `start_at_us` and across `valid_until_us` under the registered lateness rule;
- stall the renderer, underrun audio, inhibit C3, and stick head/base progress; prove the composer takes the registered degradation branch;
- correlate command, executor onset, and external-video onset without using timestamp proximity as the primary identity;
- run the wall-clock-step case without scheduled or expiring cue displacement;
- restart C0 or an MCU mid-performance (`OX-RESTART`) and prove the old epoch cannot resume.
