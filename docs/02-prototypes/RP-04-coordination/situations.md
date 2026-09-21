# RP-04 Situation Catalogue

| Field | Value |
|---|---|
| Status | Part 1 registered; Part 2 P-01 sheets filled 2026-09-21; P-02/P-03 backpropagation still stub |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Semantic source | [`intent.md`](intent.md) |
| Mechanical sources | RP-01 `storyboard.md` (`HM-*`); RP-03 `storyboard.md` (`BM-*`) |
| Visual/audio source | RP-01 `intent.md` (`E-*`, `A-*`) |

This file is the situation catalogue, not a second mechanical storyboard. It names what the audience should see, which inherited panels play, and which overlays every implementation must survive. It does not select a scheduler.

## 1. Catalogue bound

| Kind | IDs | Rule |
|---|---|---|
| Scored performances | `P-01`, `P-02`, `P-03` | Exactly these three. No idle, music, come, or follow score |
| Shared overlays | `OX-CANCEL`, `OX-PREEMPT`, `OX-SAFETY`, `OX-INHIBIT-BASE`, `OX-DENY`, `OX-DELAY`, `OX-STALE`, `OX-TIME`, `OX-RESTART` | Applied to the three performances as deltas. Not a cartesian product of `OM`/`CC`/`F` |

Any millisecond range in this file is an authored `E` hypothesis, not a pass threshold.

## 2. How to read a score

Each score starts with the audience read, then names eligible inherited panels. It does not redefine angles, velocities, limits, or local trajectory laws.

Relative timing is written around a semantic anchor:

- `lead`: visibly begins before the anchor;
- `with`: intended to share the same perceptual beat, after measured lead compensation;
- `follow`: begins after observable progress/onset, before the previous channel necessarily settles;
- `settle`: the named stable end state;
- `deny`: the logged branch when a channel is absent or inhibited.

## 3. Backpropagation sheet (Part 2 fills these)

Every catalogue row eventually carries this chain. P-01 is filled first and is the prototype vertical slice.

| Step | P-01 | P-02 | P-03 | Overlays |
|---|---|---|---|---|
| Observable character result | §5 | §6 | §7 | §8 |
| Semantic beats and phase relationships | drafted | drafted | drafted | drafted as deltas |
| Required state transitions | **§11** | stub | stub | **§11** |
| Commands, events, ACKs, feedback | **§11** | stub | stub | **§11** |
| Scheduling and timing guarantees | **§11** (`E`) | stub | stub | **§11** |
| Controller/process ownership | **§11** | inherit | inherit | **§11** |
| Fault and recovery behaviour | **§11** | drafted | drafted | **§11** |
| Executable tests and evidence | `T-P01-*` | later | later | `T-P01-*` |

## 4. Common run contract

Every run records:

| Field | Requirement |
|---|---|
| Identity | `run_id`, `perf_id`, monotonically increasing performance epoch, and `cue_id` per beat |
| Configuration | Score version; overlay IDs applied; channel availability; operating mode; controller/renderer/audio versions; architecture/budget versions |
| Start | Registered head/body pose, face/light/audio state, base mode and HOLD state |
| Events | Intent accept, planned cue, dispatch, receipt, local start, source onset, witnessed onset, completion/deny/fault |
| End | Head/base velocity and hold, face/light state, audio silence, no queued stale cues |
| Witness | Start/end video cue in frame; run ID shown or announced |

Composed and independent-baseline versions use the same start/end contract.

## 5. P-01 — Wake and attend

**Audience read:** M4 wakes as one organism, becomes visually alert, raises its head, and finds or clearly begins looking for the person. The stationary body reads as deliberate attention, not a missing actuator.

### Eligibility and inherited panels

| Channel | Executor | Normal contribution |
|---|---|---|
| Face | D1 via C2 | `E-sleep → E-open → E-neutral` or `E-gaze(target)`; `E-lost` only while target unresolved |
| Light | C2 | Registered wake/attention pattern; distinctive edge also supplies the external-video cue |
| Audio | C0 `makad-audio` | One `A-wake-rise`; optional sparse `A-query-rise` only if search remains unresolved |
| Head | C2 | `HM-02 → HM-03`; then `HM-05` if target is available, otherwise bounded `HM-04` |
| Base | C3 | Floor: `BM-01` HOLD. Tabletop: `BM-13` HOLD. Wake never authorizes locomotion |

### Composed score

| Beat | Anchor | Other channels | Completion condition |
|---|---|---|---|
| `P01-C01` accept wake | C0 intent accept | Allocate new performance epoch; verify base HOLD/mode; expire conflicting idle-only cues | Eligible-channel set is known and logged |
| `P01-C02` first sign of life | Face/light visible onset | `E-open` and light may lead head onset. `A-wake-rise` begins in the same perceptual beat | At least one visible cue actually starts; dispatch alone is insufficient |
| `P01-C03` rise | `HM-03` physical onset | Face continues opening; audio overlaps the rise and resolves no later than wake settle | Head reaches the inherited wake settle; no base motion |
| `P01-C04` acquire or search | Perception result / `HM-03` progress | With a fresh target, eyes lead `HM-05`. Without one, eyes indicate unresolved direction and `HM-04` begins | Target lock enters attentive state, or bounded search remains explicitly unresolved |
| `P01-C05` settle | Attention state | Face `E-gaze`/`E-neutral`; light attentive; audio silent; head hold or bounded search; base HOLD | No unrequested second wake cue; all completed cue IDs accounted for |

Initial hypothesis (not registered): face/light onset should lead head onset by an order of 80–170 ms, with audio placed by phrase shape rather than forced sample simultaneity.

### Independent baseline

At intent accept, C0 issues `E-open`, the wake light, `A-wake-rise`, and `HM-03` immediately and independently; base receives/maintains HOLD. Each executor starts when ready. Acquisition/search is issued independently on perception result. There is no lead compensation or shared completion rule.

### Cancellation and denial (see also §8)

| Case | Required result |
|---|---|
| Cancel during rise | `HM-18`; audio stops; face/light enter the declared bounded indication; base remains HOLD; no `HM-04/05` starts afterward |
| `OX-PREEMPT` during search | See §8.1. New epoch; search cues discarded; P-02 (or the named successor) starts clean |
| Base inhibited (`OX-INHIBIT-BASE`) | Normal P-01 variant. Log `BM-13`/inhibited HOLD; do not score base motion as expected |
| `OX-DENY(base)` | Same visible P-01 as HOLD if C3 never needed to move; log base unavailable. Not a locomotion claim |
| Face denied/stalled | Head/audio/light may complete the degraded wake; the run is a G04 face-denied case and is ineligible as normal G03 evidence |
| Audio denied | Visual/head wake proceeds with silence; never substitute spoken English |
| Head denied | Face/light/audio may issue one bounded wake/failure response; no search is claimed and no locomotion begins |
| Target unavailable | Search/lost state is honest; no `HM-05` or `E-gaze(target)` success is logged |

## 6. P-02 — Curious acknowledge and orient

**Audience read:** M4 notices a subject, commits its gaze, tilts with curiosity, and—only when the subject lies outside the head’s practical attention sector—hands the remaining turn to the body while keeping attention coherent.

This is the RP-04 hand-off and counter-motion case. It does not prove person tracking or following.

### Eligibility and inherited panels

| Channel | Executor | Normal contribution |
|---|---|---|
| Face | D1 via C2 | `E-gaze(target)` leads; then `E-wide` or `E-think`; one `E-blink` may punctuate the held thought |
| Light | C2 | Attentive/listening pattern; no repeated beat-per-axis animation |
| Audio | C0 | One `A-query-rise`; silence is allowed after the initial acknowledgement |
| Head | C2 | `HM-10` curious tilt, optionally composed with `HM-05` within validated travel |
| Base | C3 | `BM-01` HOLD for an in-sector target. Optional `BM-05` only for the declared behind-body case in Phase C |

### Composed score — in-sector target

| Beat | Anchor | Other channels | Completion condition |
|---|---|---|---|
| `P02-C01` notice | Face gaze onset | Light marks attention; audio may begin after gaze commitment | Gaze direction is visible and fresh |
| `P02-C02` inspect | `HM-10` physical onset | Gaze remains on target; `A-query-rise` overlaps the tilt rather than preceding an empty stare | Head reaches curious hold |
| `P02-C03` thought | Curious hold | Optional `E-think`/single blink; audio resolves to silence; base remains `BM-01` | Registered hold dwell completed or a new intent arrives |
| `P02-C04` settle | Head exit/next intent | Face returns to attentive gaze/neutral; light attentive; audio silent; base HOLD | No extra nod, chirp, or wheel twitch |

### Composed score — behind-body turn, Phase C only

1. Eyes/head make a bounded directional commitment without pretending the target is already centered.
2. `BM-05` begins only after C3 accepts the goal and all local safety/mode prerequisites are true.
3. As body yaw develops, C0 updates the head goal so head yaw opposes measured base yaw within RP-01 travel/velocity limits.
4. Near final body heading, head counter-yaw returns smoothly toward body neutral while eyes remain on the target.
5. Settle is `HM-10`/attentive hold plus `BM-01`, face attentive, light attentive, audio silent.

RP-04 may not command beyond RP-01’s validated usable travel to save the composition.

### Independent baseline

At intent accept, face, light, audio, `HM-10`, and—if the target case calls for it—`BM-05` are issued independently. Head and base each orient from their local goal without anticipation, phase wait, or counter-yaw.

### Cancellation and denial

| Case | Required result |
|---|---|
| Cancel during head-only reaction | `HM-18`; face/light bounded; audio silent; base remains HOLD |
| Cancel during body hand-off | `HM-18` and `BM-12` from measured states; discard the target remainder; no post-stop gaze snap |
| `OX-INHIBIT-BASE` | Use the head-domain variant within validated head travel. If the target cannot be represented, show `E-lost`/bounded failure |
| `OX-DENY(base)` | Same as head-domain P-02 if the turn never needed wheels; do not issue `BM-05`. If the behind-body case was required, the full P-02 is denied, not a fake completed orientation |
| Head denied | Base may not perform an expressive `BM-05` as if attention were intact |
| Face denied | Head/base may execute the engineering degradation case; clip is not normal observer evidence |
| Audio denied | Visual/motion score continues silently |

## 7. P-03 — Excited spin and settle

**Audience read:** M4 anticipates one joyful flourish, spins twice on the spot, and lands upright and quiet on the original heading. The head and face amplify the same excitement without pretending to hold world gaze through the spin.

### Eligibility and inherited panels

| Channel | Executor | Normal contribution |
|---|---|---|
| Face | D1 via C2 | `E-wide`, then restrained lively blink, then attentive/neutral |
| Light | C2 | One anticipation/accent pattern, then attentive; not a strobe per revolution |
| Audio | C0 | One `A-happy` phrase; no beep per revolution |
| Head | C2 | `HM-12` happy/excited flourish; `HM-18` on cancellation |
| Base | C3 | `BM-06` excited spin to its native HOLD; `BM-12` on cancellation |

### Composed score

| Beat | Anchor | Other channels | Completion condition |
|---|---|---|---|
| `P03-C01` anticipate | Face/head visible onset | `E-wide`, light accent, `A-happy`, and `HM-12` form one anticipatory beat while base remains HOLD | C3 eligibility/acceptance known before spin release |
| `P03-C02` launch | `BM-06` physical onset | Head continues a bounded body-relative flourish; face stays expressive; audio does not retrigger | Base spin onset witnessed; no translational launch |
| `P03-C03` sustain | Base progress | Head/face variation remains bounded and body-relative. No world-target counter-yaw and no per-revolution metronome | C3 enters authored deceleration |
| `P03-C04` land | Base HOLD/heading settle | Head follow-through may finish after base onset of settle but must not conceal instability; face/light resolve; audio ends | Head/base at named hold, audio silent, no residual roll or second cue |

The head flourish must be checked against the RP-03 CoM/head-pose corner used for `BM-06`.

### Independent baseline

At intent accept, `E-wide`, light, `A-happy`, `HM-12`, and `BM-06` are issued independently. Each starts and finishes under local timing. No anticipatory release condition or shared landing exists.

### Cancellation and denial

| Case | Required result |
|---|---|
| Cancel during anticipation before wheel onset | Discard `BM-06`; `HM-18`; audio stop; bounded face/light. Any wheel motion is a miss |
| Cancel during spin | C3 executes `BM-12`; C2 executes `HM-18`; no remaining revolution or celebratory tail completes |
| `OX-INHIBIT-BASE` | P-03 is denied. A head-only happy reaction may be emitted only under a different declared degraded cue; it does not pass P-03/G03 |
| `OX-DENY(base)` | Same as inhibit for P-03: the spin is denied. Do not rename a head-only flourish as P-03 success |
| Head denied | Base spin is suppressed for the normal score. A base-only spin is an engineering degradation trial, not normal coherence evidence |
| Face or audio denied | Remaining channels may execute the declared G04 variant; normal G03 requires all five channels present |
| C3 hazard during spin | `OX-SAFETY`. Local safety dominates. Other channels cancel/settle from feedback; no success/landing cue is issued |

## 8. Shared overlays

Apply these as named variants. Do not author a new performance per overlay.

| ID | Trigger | Required high-level result | First executor to honour it |
|---|---|---|---|
| `OX-CANCEL` | Explicit cancel of the current performance | Unstarted beats discarded; motion to local bounded stop/hold; audio silent; face/light bounded indication; no stale cue starts | C0 composer flushes epoch; C2/C3 execute local stop laws |
| `OX-PREEMPT` | Successor semantic intent while a performance is active. **Required collision:** §8.1 | Old epoch flushed; new performance is a new epoch; no leftover beat is stitched on | `makad-core` |
| `OX-SAFETY` | E-stop, heartbeat loss, controller fault, lease loss, C3 hazard | Motion controllers execute local bounded stop/inhibit; unstarted score discarded; fresh arm and new intent required | C2/C3 (and hardware gate) outrank C0 |
| `OX-INHIBIT-BASE` | Tabletop / `OM-02` / C3 mode inhibit (legal HOLD) | Base HOLD reported. P-01 remains valid; P-02 uses head-domain variant; P-03 is denied, not renamed success | C3 |
| `OX-DENY` | One channel absent, stalled, or NACKed without being a safety or mode-inhibit event | Remaining channels follow the declared denied-channel score; do not wait indefinitely or claim the cue occurred | Composer + owning executor |
| `OX-DELAY` | Channel onset beyond the phase window | Preregistered bounded-wait or degradation branch; logged | Composer |
| `OX-STALE` | Expired, out-of-order, or stale-epoch command | Executor rejects; composer treats the channel as denied for that cue | C2/C3/D1/audio at execution |
| `OX-TIME` | Time model untrusted or uncertainty too large | No scored coherence. Local expiry/safety continues; performance degrades or aborts | All timestamp producers |
| `OX-RESTART` | C0, C2, C3, or D1 restart mid-performance | No automatic resume of the old epoch; inhibit/idle/decay per `CA-09`/`CA-13`; new intent after recovery | Restarting node + `makad-hwd` |

`OX-DENY` is parameterized by channel (`face` / `audio` / `head` / `light` / `base`). It is still one overlay.

Base-unavailable mapping (do not double-count):

| Condition | Overlay |
|---|---|
| Tabletop, `OM-02`, or C3 reports inhibited HOLD | `OX-INHIBIT-BASE` |
| C3 absent, stalled, or NACK unavailable without a hazard/inhibit bit | `OX-DENY(base)` |
| Hazard, E-stop, heartbeat/lease loss, C3 fault during motion | `OX-SAFETY` |
| C3 restart | `OX-RESTART` (then inhibit until re-arm) |

For P-01, `OX-INHIBIT-BASE` and `OX-DENY(base)` are observationally the same HOLD; the log reason still differs. For P-03, both deny the spin.

### 8.1 `OX-PREEMPT` required collision — P-02 during P-01 search

This is the overlay that architecture work must implement. Other preemptions are the same algebra, not extra scores.

| Field | Value |
|---|---|
| Active performance | `P-01` in `P01-C04` search: `HM-04` in progress, face `E-lost` or unresolved, optional `A-query-rise`, base HOLD |
| Arriving intent | Fresh `P-02` curious acknowledge (target now known). Not a safety event and not `OX-CANCEL` from the operator |
| Who arbitrates | `makad-core`. Perception/edge may *propose*; they do not dispatch C2/C3 |
| Old epoch | Flushed. No further `HM-04`/`HM-05` from P-01. Audio stop. Face must not log search success. C3 keeps HOLD; no wheel resource to release |
| C2 | Cancel/preempt current head goal (`HM-18` or the registered preempt-to-new-goal path). Reject any in-flight P-01 cue with stale epoch (`OX-STALE` if it still arrives) |
| D1 / light | New `FACE_STATE` / light for P-02 `P02-C01`; no completion of the lost-search expression as a successful wake |
| `makad-hwd` | Drops queued P-01 outbound intent for that epoch; does not invent the successor |
| New epoch | New `perf_id` instance / `perf_epoch` for P-02. First legal cue is P-02’s gaze lead, not a stitched remainder of `HM-04` |
| Independent baseline | Same collision: both intents are issued; channels that already started P-01 search settle locally while P-02 commands also arrive. Composition must beat that mess on G03 later; G02 only needs a clean epoch cut |

Part 2 backpropagates this row into commands, ACKs, and tests. Part 5’s P-01 spike must inject it.

## 9. Comparison matrix required of every implementation

| Dimension | Composed variant | Independent baseline |
|---|---|---|
| Semantic intent and start pose | Identical | Identical |
| Eligible channels and local panels | Identical | Identical |
| Local safety/limits | Identical | Identical |
| Shared identity | Required | Logged for comparison even though no shared scheduling is used |
| Lead compensation | From measured software/physical models | None |
| Anticipation/hand-off/counter-motion | Per score | None |
| Overlay injection | Same event time/cause | Same event time/cause |
| Camera/framing/exposure/audio level | Identical registered setup | Identical registered setup |
| Clip labels | Hidden/randomized for observers | Hidden/randomized for observers |

## 10. Open Part-1 decisions

`decision.md` owns the answers:

- `BD-01`: approve the three-performance set, the overlay set, and prohibit a fourth scored performance;
- `BD-02`: approve the honest independent baseline;
- `BD-03`: approve audio as a timing channel with a stand-in allowed before ADR-11;
- `BD-04`: approve RP-04 ownership of `E-*` timing, not artwork;
- `BD-05`: split — ~6-person **pilot** on non-scored clips, then freeze instrument; scored G03 N is Part 6.

## 11. P-01 backpropagation (Part 2)

Filled 2026-09-21. P-02/P-03 remain stubs except `P02-C01` as the `OX-PREEMPT` successor. Millisecond values are `E` hypotheses, not gates. Event names are logical; packed wire encodings remain open after `RP02-P4-REG-03` semantics.

Shared action lifecycle on every cue: `dispatch` → `receipt` → `accept|deny` → `local_start` → `source_onset` → `progress` → `complete|abort`. Composer never treats `dispatch` as onset.

### 11.1 Happy path — composed P-01

| Beat | State transition | Commands / events | Timing guarantee (`E`) | Owner | Test |
|---|---|---|---|---|---|
| `P01-C01` | Idle → `perf_epoch=N` allocated; channel snapshot logged; C3 HOLD/mode checked | `IntentAccept(P-01)`; `AvailabilitySnapshot` | Snapshot before first cue; oldest feedback age recorded | `makad-core` | `T-P01-HAPPY` |
| `P01-C02` | Face `E-sleep→E-open`; light wake; audio `A-wake-rise` armed | `FACE_STATE`, `LIGHT_STATE`, `AudioPlay` with `perf_epoch/cue_id` | Face/light **lead** head. Hypothesis 80–170 ms world-onset lead. Audio in the same perceptual beat | D1 via C2; C2 light; `makad-audio` | `T-P01-HAPPY` |
| `P01-C03` | Head `HM-02→HM-03` | `HEAD_GOAL(HM-03)` | Starts after face **source_onset** or at compensated `start_at` (adapter-specific). Base never leaves HOLD | C2 | `T-P01-HAPPY` |
| `P01-C04` | Target? `HM-05`+`E-gaze` : `HM-04`+`E-lost` | `HEAD_GOAL(HM-04\|05)`; optional `A-query-rise` | Chain off `HM-03` progress/complete. No locomotion | C2; `makad-perception` proposes only | `T-P01-HAPPY` (search branch default in spikes) |
| `P01-C05` | Named settle; audio silent; no queued cues | Hold/idle goals; `AudioStop` if still playing | All motion HOLD; no second wake | all | `T-P01-HAPPY` |
| C3 throughout | `BM-01` or `BM-13` HOLD | `BASE_GOAL(HOLD)` or inhibit snapshot | Zero wheel onset | C3 | `T-P01-HAPPY` |

Independent baseline: same cues, each channel `dispatch` immediately at `P01-C01`; no lead, no wait. Logged for comparison, not a Part 5 pass criterion.

### 11.2 Overlay deltas (P-01)

| Overlay | Inject at | State / commands | Success criterion | Owner | Test |
|---|---|---|---|---|---|
| `OX-CANCEL` | During `P01-C03` rise | Flush epoch N; `HEAD_CANCEL`/`HM-18`; `AudioStop`; bounded face/light; C3 HOLD; **no** `HM-04/05` dispatch | No cue with epoch N after flush; no search start | `makad-core` + C2 | `T-P01-CANCEL` |
| `OX-PREEMPT` | During `P01-C04` search (`HM-04`) | §8.1: flush N; `makad-hwd` drops queue; C2 preempt; audio stop; epoch N+1 is `P-02` with first cue `P02-C01` gaze; no P-01 search success | New epoch; first post-preempt face cue is P-02 gaze; no `HM-04` complete-as-wake | `makad-core` | `T-P01-PREEMPT` |
| `OX-DENY(face)` | `P01-C02` D1 NACK/stall | Log deny; do not claim face onset; remaining channels may continue as G04 | No `source_onset` face event; run tagged denied | D1 + composer | `T-P01-DENY-FACE` |
| `OX-DENY(base)` vs `OX-INHIBIT-BASE` | At `P01-C01` | Inhibit: C3 HOLD + inhibit reason, P-01 still valid. Deny: C3 unavailable, same HOLD appearance, different reason enum | No wheel onset; reason distinguishes inhibit vs unavailable | C3 | mapping only; not a separate architecture axis |
| `OX-DELAY` | Head `source_onset` later than phase window after face onset | Composer takes bounded-wait then degrade/log `OX-DELAY`; must not silently score as composed | Delay event logged; later cues follow adapter rule (time continues / progress waits) | composer | `T-P01-DELAY` |
| `OX-STALE` | Cue for epoch N arrives after flush or with old epoch | Executor NACK `stale_epoch`; composer does not retry that cue | Rejected; no local_start | C2/C3/D1/audio | `T-P01-STALE` |
| `OX-TIME` | Time model invalid or `start_at` late vs `valid_until` | Scheduled execution **rejected** with distinguishable reason; must not silently run immediately. Progress-triggered cues may continue. No G01 score | Reject reason `time_model_invalid` or `late`; local expiry still applies | timestamp producers + composer | `T-P01-TIME` |
| `OX-RESTART` | C0 or virtual C2/C3/D1 restart mid-P-01 | Old epoch **must not resume**. C2/C3 inhibit; D1 idle/decay; `makad-hwd` new session. Fresh arm + new intent required | No cue from epoch N after restart; no auto-replay | restarting node + `hwd` | `T-P01-RESTART` |
| `OX-SAFETY` | Hazard / E-stop / lease loss during rise | Same score flush as cancel, but **stop authority is C2/C3 (and hardware gate)**, not a composer `HM-18` authored flourish. Composer inhibit/cancel is best-effort | Motion BRAKE/HOLD locally even if C0 is silent; no leftover score | C2/C3 first | delta vs `T-P01-CANCEL`; not a third composer path |

`OX-SAFETY` is not a prettier cancel. If C0 is wedged, C2/C3 still stop.

### 11.3 P-02 stub used by preempt

`P02-C01` after preempt: `FACE_STATE` gaze lead with **new** `perf_id`/`perf_epoch`. Head `HM-10` is not required in the P-01 spike if gaze dispatch proves the epoch cut. Full P-02 backpropagation waits.

