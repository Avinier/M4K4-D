# RP-04 Coordinated Performance Intent

| Field | Value |
|---|---|
| Status | Part 1 registered `RP04-P1-REG-01` 2026-09-21 — catalogue frozen at design-definition; backpropagation and architecture selection open |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-04; construction record [`plan.md`](plan.md) |
| Feeds | ADR-05; ADR-03/ADR-12 interface evidence; SC-01…05, SC-09/10/25; RP-05/RP-06/RP-07 handoffs |

## 1. Purpose

RP-04 produces a researched, scenario-derived, executable coordination architecture that converts semantic intent into synchronized, interruptible, observable, and safely degradable multi-controller performances.

That is broader than composing three attractive clips. It is also narrower than a middleware survey or a second electrical ICD.

Four concrete outputs:

1. A complete situation-to-runtime specification for the catalogue in [`situations.md`](situations.md).
2. A compared and selected coordination architecture (`runtime-architecture.md`, after research).
3. An executable reference runtime/simulator with replay and fault injection (`prototype/`), starting at P-01.
4. Quantitative conformance and human-observer evidence.

### 1.1 Controllers and C0 services

| Node | Role | RP-04 authors | RP-04 does not own |
|---|---|---|---|
| `C0` | Application computer | Composer, performance identity, C0 service event/action APIs, logging/trace correlation, audio as a scheduled channel | Raw device buses, hardware motor permission, cloud-as-safety |
| `C2` | Head-motion and safety | Selection and phasing of existing `HM-*`; cancel/degrade against C2 authority | Trajectories, limits, servo bus, automatic re-arm |
| `C3` | Base-motion and local safety | Selection and phasing of existing `BM-*` when eligible | Drive profiles, hazards, mode, inhibition |
| `D1` | Face/display renderer | Semantic `E-*` cue, phase, expiry, frame-flip onset | Artwork, raster path, display SKU |
| Status light | Typically C2 / head light | Semantic pattern role, phase, witness cue | Light SKU |
| Audio | C0 `makad-audio` | Semantic `A-*` cue, phase, callback evidence, silence/cancel | Samples, speaker, acoustic bar |

`C1` is not a node. Combining head motion with the display controller was rejected; D1 remains a renderer behind C2 (`CA-04`).

C0 processes from `CA-08`: `makad-core` (behaviour, action lifecycle, expression schedule, epoch), `makad-hwd` (MCU sessions, queues, evidence capture), `makad-perception` (observations), `makad-audio` (capture/playback timing), `makad-edge` (app/cloud). RP-04 specifies how they share intent, progress, cancellation, and traces over the already-chosen Unix-domain-socket IPC.

The base is a scored channel even when its correct contribution is `BM-01` or `BM-13` HOLD. “No locomotion” is an authored choice, not omission.

### 1.2 What “fast” means here

RP-01 and RP-03 own head trajectories, wheel velocity, acceleration, and physical settling. RP-04 consumes those measurements and sets software/perceptual budgets: cross-channel onset skew, scheduler jitter, command lead time, feedback age, cancellation propagation, state-transition deadlines, ACK/NACK latency, timebase uncertainty, queue/buffer bounds, CPU/memory/runtime margin, observer-perceptible delay.

## 2. Questions

**Design question.** What researched, scenario-derived coordination architecture converts semantic intent into synchronized, interruptible, observable, and safely degradable performances across C0, C2, C3, and D1 — and what software and perceptual timing budgets does that architecture impose?

**Gate question.** Can measured head and base controllers be composed, synchronized, interrupted, counter-moved and settled as one readable performance rather than as independent actuator commands?

The design question yields artifacts. The gate question can reject them.

## 3. Traceability

| Source | RP-04 obligation |
|---|---|
| AD-01 | One character, not a sequence of subsystem demonstrations |
| AD-03 | Head, body, and wheels support interruption, counter-motion, onset timing, and settle |
| AD-11 | Intent, scheduled cue, command, actual state, visible onset, and failure are correlated |
| ADR-03 | Preserve C0 semantic authority and C2/C3 local deterministic/safety authority |
| ADR-05 | Select a coordination architecture only after research, executable comparison, and measured evidence |
| ADR-12 | State the time/link/log requirements coordination actually needs; do not fork the ICD |
| `CA-07` | No ROS 2 / micro-ROS in the V1 safety path; local typed IPC on C0 |
| SC-01…05 | Character unity, integrated timing, display/head quality contribution, deliberate composition |
| SC-09/10 | Reusable bounded composition and at least three authored behaviours |
| SC-25 | Excited spin reads as a deliberate performance and settles safely |
| SC-TBD-01 | Freeze observer sample, questions, and pass rule before scored clips |
| SC-TBD-02 | Freeze consecutive-run count before G05 |
| SC-TBD-04 | Consume, never silently replace, RP-01 head-motion quality thresholds |

## 4. Catalogue bound

RP-04 owns exactly three scored performances, plus a small shared overlay set:

| ID | Intent | Required phase | Principal mechanical panels |
|---|---|---|---|
| `P-01` | Wake and attend | B; re-run in C | `HM-02→HM-03`, optional `HM-04→HM-05`; base HOLD |
| `P-02` | Curious acknowledge/orient | B without body pivot; full in C | `HM-10`, optional `HM-05`; optional `BM-05` |
| `P-03` | Excited spin and settle | C only | `HM-12`; `BM-06`; `HM-18`/`BM-12` on cancellation |

Overlays (`OX-*` in `situations.md`) are applied to those three. They are not a fourth performance and not a cartesian product of the RP-02 state register.

Idle aliveness, music vibe, come, and follow are later consumers of the same architecture.

## 5. Composition intent (semantic, pre-numeric)

- one channel anchors each beat; all channels do not start together merely because an intent arrived;
- attention is readable before large motion: eyes may lead head, and head may commit direction before base;
- channels may overlap and finish at different times, but follow-through resolves to one named end state;
- P-02 may hand yaw from head to base while the head counter-yaws to preserve world attention;
- P-03 uses a body-relative head flourish, not a fake world-gaze lock through two rotations;
- cancellation discards unstarted beats and reaches bounded holds;
- channel absence/inhibition produces a declared variant of the same intent rather than false success or deadlock;
- C2/C3 remain the legality and stop authority even when C0 still holds the score.

Exact offsets, tolerance windows, and settle bounds belong in `timing-budgets.md` and `gates.md`.

## 6. Independent-channel baseline

The baseline is the strongest honest naive implementation:

1. C0 issues the same semantic intent and the same eligible local panels as the composed variant.
2. Each channel begins as soon as it can after receipt.
3. There is no shared score, lead compensation, anticipation, cross-channel phase wait, counter-motion, or hand-off.
4. Each local controller still obeys its own limits, expiry, safety, and best local motion law.
5. Cancellation is issued to every channel but each settles independently.

If composition cannot beat this baseline, RP-04 has not shown value.

## 7. Design method

Scenario backpropagation is mandatory. Research fills four axes; lifecycle and supervision are shared. Part 3 shortlists at most three end-to-end bindings; Part 5 selects after the same P-01 spike. Remaining research is empirical HYBRID validation, not a new family. G03 questions live in `observer-protocol.md`; freeze N/pass with the gate, on real clips, in Part 6. Detail: [`plan.md`](plan.md) §5, [`situations.md`](situations.md), [`research/README.md`](research/README.md).

## 8. Evidence boundary

RP-04 needs both instruments:

- engineering evidence: source-stamped event log plus synchronized external video for onset, phase, interruption, and settle;
- perception evidence: preregistered randomized video comparison against the independent baseline.

Virtual-node tests can prove invariants, cancellation, denial, and replay. They cannot replace G03 or physical G01.

Every Phase A channel parameter is `E`. A latency or settle value becomes `W` only on the named physical executor, configuration, and run ID.

## 9. Phases

| Phase | RP-04 meaning |
|---|---|
| A | Paper, research, and an executable composer against virtual/modelled C2/C3/D1. No coherence claim |
| B | Face, light, audio stand-in, and executable head; base explicitly held/inhibited. P-01 is a real target |
| C | Same system on an RP-03-qualified base. Full P-02 hand-off/counter-motion and P-03 become eligible |

## 10. Non-goals

RP-04 does not:

- author final eye art or astromech samples;
- select status light, amplifier, speaker, motors, servos, or sensors;
- change `HM-*`/`BM-*` mechanism requirements without an iterate request to the owner;
- implement wake recognition, NLU, target tracking, come, or follow;
- reopen `CA-07` (no ROS 2 in the V1 safety path), differential UART, COBS/CRC, or C0 Unix-domain sockets unless a cited change request is issued;
- treat a composed fixed video, a composer dispatch timestamp, or an observer compliment as a gate pass;
- permit score completion after stop, inhibit, expiry, or a newer performance epoch;
- claim SC-01/SC-02 for the integrated robot;
- enumerate every theoretical operating-state combination.

## 11. Part-1 completion criteria

Part 1 is ready for registration only when:

- the builder accepts the C0/C2/C3/D1 boundary, five-channel scoring (audio on C0), exactly three performances plus the shared overlay set (including `OX-DENY(base)` mapping and the P-01-search `OX-PREEMPT` collision);
- each performance has composed, independent, cancellation, and denied/inhibited forms;
- `BD-01…BD-04` and `BD-07` are accepted 2026-09-21 (`decision.md`); `BD-05` superseded (no household observer panel); `BD-06` is deferred;
- [`interface-requirements.md`](interface-requirements.md) is acknowledged as an **issued** RP-02 request under `RP04-P1-REG-01`, not as accepted ICD fields;
- no prose in Part 1 is mistaken for a numeric gate freeze or an ADR-05 selection.
