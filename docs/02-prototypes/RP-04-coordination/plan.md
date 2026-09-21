# RP-04 — Coordinated Performance Construction Record

| Field | Value |
|---|---|
| Status | Construction record v0.6. Phase A design-definition registered `RP04-P1-REG-01`…`P6-REG-01`. Virtual `CS-HYBRID` wait language and P-02 cue list closed 2026-09-21. Exploratory RP-02 layout revision 2. `BD-05` household observer panel superseded. G03 waits on real clips. RP-04 **blocked on Phase B/C** |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.12 §RP-04 |
| Inputs | RP-01/RP-02/RP-03 registered design definitions |
| Exit | Provisional ADR-05 selection backed by a selected coordination architecture, executable conformance evidence, measured software/perceptual timing, interruption/degradation evidence, and a preregistered observer comparison |

This is the construction record. It is not the start-here index and does not report completion. Durable orientation lives in [`README.md`](README.md).

RP-01 is an object. RP-02 is a set of states, links, and firmware/process boundaries. RP-03 is a vehicle plus a local safety authority. **RP-04 is the first predominantly software-architecture prototype.** Its experimental object is coordination: converting semantic intent into synchronized, interruptible, observable, and safely degradable multi-controller performances. It still cannot pass on an offline scheduler alone.

## 1. The two questions

### Design question — the deliverable

> What researched, scenario-derived coordination architecture converts semantic intent into synchronized, interruptible, observable, and safely degradable performances across C0, C2, C3, and D1 — and what software and perceptual timing budgets does that architecture impose?

The answer is four artifacts: a situation-to-runtime specification, a compared and selected coordination architecture, an executable reference runtime/simulator with replay and fault injection, and quantitative conformance plus observer evidence. A fixed keyframe video is not an answer.

### Gate question — the falsifier

> Can measured head and base controllers be composed, synchronized, interrupted, counter-moved and settled as one readable performance rather than as independent actuator commands?

This is verbatim from the governing plan. `Reject` must remain reachable. A miss changes the architecture, score, contract, or a sibling handoff; it never changes the observer sheet after results are visible.

## 2. Failure modes this folder is designed against

| Failure mode | Protection in this folder |
|---|---|
| Sibling-derived document pile | Internal organization is software-shaped: situations, research, runtime, contracts, prototype, validation. Governance (status, evidence class, decisions, gates, run IDs) stays project-wide |
| Puppet track | Situations backpropagate to lifecycle, cancellation, and expiry. Concepts differ on phase authority and are compared under delay, denial, and restart |
| Reopening RP-02 transports | RP-02 owns ROS exclusion, UART, framing, C0 Unix-domain sockets, and MCU session/expiry. RP-04 owns coordination middleware above those transports. Inadequacy becomes a cited change request, not a silent fork |
| Middleware survey | Time-boxed comparison of at most three viable mechanism families against Makad situations. Product names are evidence, not selections |
| Compliment machine | Observer protocol is separate from composer design, uses randomized labelled-hidden video pairs, and freezes before tuning |
| Self-certified timing | Composer dispatch logs are not physical-onset evidence. Source stamps and synchronized external video are required for scored onsets |
| Estimates becoming actuator targets | RP-01/RP-03 own physical speed and settle. RP-04 consumes those models and owns software/perceptual budgets. Every Phase A value is `E` with a re-run obligation |
| Combinatorial state explosion | Three performances plus a small shared overlay set. Not every theoretical `OM`/`CC`/`F` combination |
| Offline-only pass | Virtual C2/C3/D1 nodes can prove invariants. G01/G03 still need controller response, visible/acoustic onset, and observers |

## 3. Active controllers — do not revive `C1`

The rejected idea of combining head motion with the display controller is not in this architecture. The map is RP-02 `compute-control-architecture.md`.

| Node | Hardware (selected) | RP-04 relationship |
|---|---|---|
| `C0` | Raspberry Pi 5 2 GB | Application computer. Hosts composer, behaviour/action lifecycle, audio, logging, master monotonic time, and C0 service IPC |
| `C2` | Waveshare ESP32-S3-Zero | Head-motion and safety controller. Trajectories, limits, expiry, servo bus, C2 readiness, relay of face/light to D1 |
| `C3` | ESP32-S3-DevKitC-1-N8 (prototype class) | Base-motion and local-safety controller. Wheels, hazards, envelope, odometry, expiry, C3 readiness |
| `D1` | Waveshare ESP32-S3-LCD-4.3 SKU 30493 | Face/display renderer. Local assets, frame flip, expiry-to-idle. No motion or behavioural authority |

Audio executes on C0 (`makad-audio`) but is a first-class scheduled output channel in every score.

C0 internal services inherited from `CA-08` and not re-derived here: `makad-core`, `makad-hwd`, `makad-perception`, `makad-audio`, `makad-edge`. RP-04 defines how they exchange intent, progress, cancellation, and traces. It does not invent a fifth MCU.

## 4. Inherited authority — consume, do not reopen casually

| Inherited fact | Authority | RP-04 consequence |
|---|---|---|
| Linux expresses intent; C2/C3 enforce physics | `CA-01` | Composer never streams raw PWM or participates in the stop path |
| One owner per actuator bus; D1 owns pixels | `CA-02` | RP-04 sends semantic cues |
| Base safety is a separate MCU | `CA-03` | Composer cannot override inhibit |
| Head has one body ingress; C2 relays D1 | `CA-04` | Face/light commands go C0→C2→D1 |
| Differential UART; COBS/CRC/session/expiry | `CA-05`; `link-contract.md` | Transports stay RP-02. RP-04 may request fields |
| No ROS 2 / micro-ROS in the V1 safety path | `CA-07` | Coordination middleware is local typed IPC plus framed MCU messages |
| C0 Unix-domain sockets; bounded services | `CA-07`, `CA-08` | RP-04 specifies event/action APIs on that IPC, not a new bus |
| Authority is a renewable lease | `CA-09` | Performance epoch dies with lease loss |
| Local reflexes outrank remote intent | `CA-11` | Safety authority stays on C2/C3 |
| Head and base panels already exist | RP-01/RP-03 `storyboard.md` | RP-04 composes `HM-*` and `BM-*` |
| Eye/audio semantic placeholders exist | RP-01 `intent.md` | RP-04 owns their timing, not art or acoustics |
| Timebase method defined, not implemented | `../../01-system/timebase.md` | No scored onset evidence until validated |
| Exact RP-02 byte layouts remain open | `link-contract.md` | Identity, onset feedback, and denial reasons must be requested before freeze |

RP-04 does not select actuators, drivetrain, face art, status-light hardware, speaker/amplifier, wake-word path, person-tracking policy, or following behaviour. It does not close SC-01/SC-02 for the integrated droid.

RP-04 **does** decide the coordination layer above those transports: performance representation, event/action API, scheduler/executor model, lifecycle and cancellation, correlation/tracing, how C0 services communicate intent and progress, how physical feedback advances or aborts a performance, and how scores are loaded, versioned, validated, and replayed.

If scenario analysis shows an RP-02 decision cannot meet a Core situation, RP-04 issues a change request with evidence. It does not silently replace the ICD.

## 5. Method — scenario backpropagation

Architecture is not selected first. For every catalogue situation:

```text
observable character result
    ↓
semantic beats and phase relationships
    ↓
required state transitions
    ↓
commands, events, acknowledgements, feedback
    ↓
scheduling and timing guarantees
    ↓
controller/process ownership
    ↓
fault and recovery behaviour
    ↓
executable tests and evidence
```

Source material: RP-01 and RP-03 storyboards; Core interaction scenarios; RP-02 state register and operating situations; link/timebase contracts; safety and recovery rules; display, audio, wake, tracking, and later interaction requirements from `01-system`.

Research precedes **shortlist**. Adjacent fields feed four *axes* (score representation, trigger, action lifecycle, supervision). Lifecycle and supervision are shared; they are not competing families. At most three end-to-end *bindings* of the compared axes are shortlisted in Part 3 and selected in Part 5 after the same P-01 spike. Detail: [`research/README.md`](research/README.md).

## 6. Owned files

Software-shaped. Project-wide governance is retained. There is no `cad/` directory.

| Path | What it owns | Part |
|---|---|---|
| `plan.md` | This construction record | — |
| `README.md` | Start-here index | last |
| `intent.md` | Purpose, controllers, two questions, non-goals, method | 1 |
| `situations.md` | P-01…P-03 plus shared overlays; backpropagation sheets | 1–2 |
| `research/` | Closed TIME/PROG/HYBRID; [literature](research/literature.md) grounds the axes; remaining empirical HYBRID spec | 3 closed; literature 2026-09-21; remaining `experiment-spec.md` |
| `runtime-architecture.md` | Shared ownership, lifecycle, arbitration, cancellation, recovery; selected binding recorded after Part 5 | 4, amended at 5 |
| `interface-requirements.md` | Coordination needs on RP-02 wire/timebase/logs; change-request only | 1 early / 4 |
| `timing-budgets.md` | Software/perceptual budgets: skew, jitter, lead, feedback age, cancel propagation, CPU/memory margin | 4 |
| `prototype/` | Same P-01 spike per shortlisted binding; then the selected composer | 5 |
| `observer-protocol.md` | G03 questions. Real clips only; freeze with the gate | 6 |
| `gates.md` | Paper gates and RP04-G01…G05 candidates | 6 |
| `decision.md` | Builder decisions, Part registrations, ADR-05 ladder | ongoing |
| `runs/` | Run records | evidence |

Names retained from the v0.1 draft only where they still match: `interface-requirements.md`, `decision.md`, `gates.md`, `observer-protocol.md`. Retired as folder drivers: a mechanics-style `timing-model.md` analogue of `physics.md`, a split `composition-rules.md` vs `interruption-and-degradation.md` vs `fault-matrix.md` vs `rig.md`. Those concerns fold into situations, runtime architecture, prototype, and gates.

## 7. Identifier and ownership rules

- `P-01…P-03`: scored performances.
- `OX-*`: shared interruption/failure overlays, not extra performances.
- `CS-*`: trigger adapters `CS-TIME`, `CS-PROG`, `CS-HYBRID`. Graph/statechart is a score-representation axis, not a third trigger.
- `IR-*`: interface/change-request items toward RP-02.
- `BD-*`: builder decisions local to RP-04.
- `RP04-P<n>-REG-<nn>` and `RP04-G<n>-REG-<nn>`: append-only Part and gate registrations.
- `HM-*`, `BM-*`, `E-*`, `A-*`, `OM-*`, `BS-*`, `EV-*`, `CC-*`, `LP-*`, `CA-*`, `F-*` remain owned by their source documents.

## 8. Six Parts in dependency order

### Part 1 — Intent and situation catalogue

Writes `intent.md`, `situations.md` (scores + overlay set), open `BD-*`, and the early RP-02 request in `interface-requirements.md`.

Must not choose a scheduler, add a fourth scored performance, register timing thresholds, or claim readability.

### Part 2 — Scenario backpropagation

Fills the chain in §5 for P-01 completely, then P-02/P-03 and each overlay as deltas, including the concrete `OX-PREEMPT` collision. Ownership and test obligations fall out of the sheets. P-01 is the vertical-slice target.

Drafts `observer-protocol.md` questions. Does **not** run a household or mock-video panel (`BD-05`, builder decision). G03 freeze is Part 6, on real clips, **after** non-scored engineering tuning. Engineering LED must be cropped from rated clips.

Must not convert 80–170 ms from `intuition.md` into a pass threshold, infer physical onset from dispatch, or tune a composer against a **frozen** observer sheet. Non-scored engineering runs may change the composer before freeze.

### Part 3 — Mechanism shortlist

Time-boxed research. Fill the four axes. Compare at most three **end-to-end bindings** against the filled situations. Shortlist; do not select.

Must not treat timeline, action lifecycle, and supervision as competing products, survey every framework, or treat ROS 2 as automatically appropriate (`CA-07`).

### Part 4 — Shared runtime, contracts, budgets

Writes `runtime-architecture.md` for the **shared** layer (ownership, action lifecycle, arbitration, cancellation, recovery) and `timing-budgets.md`. Completes `interface-requirements.md` if Part 2/3 prove a missing field. Candidate-specific trigger/score notes stay open until Part 5.

Must not let C0 overrule C2/C3 safety or let a channel invent the next semantic beat.

### Part 5 — Executable spikes and selection

The same small P-01 spike on virtual C2/C3/D1/audio for each shortlisted binding: replay, delay, `OX-CANCEL`, `OX-PREEMPT`, `OX-DENY`, `OX-STALE`. Then select. Record the winner in `decision.md` and amend `runtime-architecture.md`. Machine invariants can close here; observer coherence cannot.

Do not build three frameworks.

### Part 6 — Validation, scoring, gates, decision

Collect, score, and analyze observer clips against the drafted instrument.

```text
engineering tuning on non-scored runs
  → freeze questions, N, pass rule, and clip-selection rule
  → capture scored runs
  → select clips by the frozen rule
  → observer scoring
```

No household or mock-video panel (`BD-05`). G01…G05 candidates, Phase B/C physical evidence, ADR-05 ladder. Numeric gates freeze before scored data. Do not promise p99 unless frozen `n` supports it.

## 9. Phase ladder

Phase is a status field, not a directory.

| Phase | Needs | Can produce | Cannot produce |
|---|---|---|---|
| **A — paper, research, virtual nodes** | Parts 1–5 defined; modelled/virtual C2/C3/D1; no claim that models are measured | Situation sheets; interface request; mechanism comparison; P-01 replay/fault harness; invariant tests | `W` timing, observer coherence, gate pass, ADR-05 close |
| **B — head-domain composition** | Executable RP-01 head; D1; light/bench LED; audio stand-in; timebase/logging; base explicitly inhibited | Real P-01; P-02 without body pivot; non-base G01/G02/G04; G03 clips of that hardware | P-03, live counter-motion, base timing, SC-07 acoustic quality |
| **C — full composition** | RP-03 G01/G02/G06-qualified base and measured response model; integrated head; same witness/logging | Full P-02, P-03, G01…G05, provisional ADR-05 | Person following, integrated SC-01/02, speaker selection |

Phase A is real work. Scored physical G01/G03 wait on sibling controllers, as the governing plan requires. Paper, research, contracts, and the virtual P-01 slice do not wait.

## 10. Named circularities

| Loop | What proceeds now | What waits |
|---|---|---|
| RP-04 coordination ↔ RP-02 byte layout | Require shared `perf_id`/`cue_id`, denial reasons, onset feedback, and optional scheduled start now. Exploratory packed layout revision 2 exists in RP-02 `phase-a/` | Exact registered widths/order and G04/G05 codec qualification wait on RP-02 review and Phase A/B measurement |
| RP-04 software budgets ↔ RP-01/RP-03 measured models | Backpropagate perceptual targets; mark physical segments `E` | `W` compensation, G01, and ADR-05 wait on measured head/base onset and settle |
| Observer protocol ↔ working composer | Draft G03 questions from the catalogue now. Engineering-tune on non-scored runs | Freeze N/pass/clip-selection, then scored capture; no mock-video panel (`BD-05`) |
| Audio timing ↔ unselected audio hardware | Timestamped stand-in proves scheduling and denial | SC-07 quality and ADR-11 wait on RP-05/RP-06 |
| Eye timing ↔ unfinished artwork | Semantic `E-*` and frame-flip onset | Final appearance waits on RP-06 |
| Architecture selection ↔ research | Charter axes and three bindings now | Part 3 shortlists; Part 5 selects after spikes; ADR-05 still needs physical G01/G03 |

## 11. Evidence rules

1. Evidence classes remain `W` measured on the named configuration, `D` manufacturer, `E` estimate/substitute, and `U` unknown. Unknown is never zero.
2. Dispatch, receipt, local start, source onset, and witnessed onset are different events.
3. A virtual-node pass proves invariants and degradation branches. It does not prove observer coherence or physical onset.
4. A substitute needs an equivalence statement. A GPIO beep can establish audio timing, not audio quality.
5. The same semantic intent, eligible channels, start pose, framing, and exposure are used for composed and independent-baseline clips.
6. Thresholds and observer wording freeze before scored evidence.
7. Safety authority remains local. A denied channel is evidence, not permission to retry around the inhibit.
8. Failed, aborted, degraded, and rejected runs remain in the record.
9. No coherence gate may omit the face/eyes merely because final artwork is unfinished.
10. RP-04 timing targets are end-to-end software and perceptual: cross-channel onset skew, scheduler jitter, command lead time, feedback age, cancellation propagation, state-transition deadlines, ACK/NACK latency, timebase uncertainty, queue bounds, CPU/memory/runtime margin, observer-perceptible delay. Actuator speed and physical settle remain RP-01/RP-03.

## 12. Current execution order

1. Phase B when sibling rigs exist. Non-scored engineering runs, then G03 freeze, then scored clips. Physical `TR-P01-*` in `research/experiment-spec.md` are not closed by the virtual suite.
2. Close `BD-08` before implementing counter-yaw. Executable P-02 after the RP-03 base model.
3. Packed ICD remains exploratory layout revision 2 until RP-02 registers byte layouts under G04/G05.

Virtual software already done (do not reopen): HYBRID `any(face, light)` + `T-DEAD`; P-02 cue list + validator; TIME/PROG frozen evidence.

## 13. Historical notes in this folder

Early drafts copied the RP-03 document pattern. Useful material kept in this file and the live docs: five-channel scope, honest independent baseline, onset-vs-dispatch discipline, observer separation, P-01…P-03 scores. **Folder method is this file.**
