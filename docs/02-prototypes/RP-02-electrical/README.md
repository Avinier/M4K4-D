# RP-02 — Electrical/Control Backbone

| Field | Value |
|---|---|
| Status | **Parts 1–4 are complete at design-definition level.** Part 4 is `RP02-P4-REG-01` (C0↔C2) plus `RP02-P4-REG-02` (`BASE_*`) plus `RP02-P4-REG-03` (cue identity / `start_at_us` / onset reports / extra `NACK` values, 2026-09-21). Byte layouts, numeric timeouts, remaining component suffixes, purchase and scored evidence stay open. Phase A is live |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.12 §RP-02 |
| Purpose | Close **ADR-03** (controller backbone), **ADR-12** (internal communication and timebase) and the *architecture* half of **ADR-06** (battery, rails, isolation, low-energy policy); bound the *sizing* half |

RP-01 is an object. RP-02 is a set of states and interfaces: a tree of rails, four compute/control roles, message contracts across noisy and moving boundaries, and a space of concurrent operating conditions. Every subsystem will work alone; AD-08 says the peaks happen together. RP-02 is the instrument that makes the coexistence failure visible before the enclosure exists.

## Start here

| Document | What it owns | Phase live |
|---|---|---|
| [Glossary](glossary.md) | Reader index for every RP-02 namespace, registered Part-1 label, Part-2 `EDB/EC/PA/PB/PCD/BR` label, evidence/status label, protocol label and common notation | A |
| [Electrical design basis](electrical-design-basis.md) | Approved `EDB-01…08`; normalized `EDB-03` source/load contracts, composition rules, branch-boundary requirements and open dependencies | A |
| [Power branch contracts](power-branch-contracts.md) | Branch-side `EDB-03` contracts for every registered `PB-*` path, aggregation equations and calculation-readiness register | A |
| [Power implementation basis](power-implementation-basis.md) | Registered voltage-domain, return, connector, conductor, protection, capacitance and circuit-sequencing rules beneath the topology; selects Raspberry Pi 5 2 GB | A |
| [Power calculation ledger](power-calculation-ledger.md) | Derived voltage-drop, conductor/contact heat, converter-loss, source-current, `MD-01` energy and fuse-coordination calculations; final ratings remain evidence-dependent | A |
| [Power-component candidate screen](power-component-candidate-screen.md) | Manufacturer-sourced `PCD-*` converter, protection, E-stop, connector, cable and charging candidates; quantitative rejection logic and dated India sourcing snapshot; no selection or purchase | A |
| [Brownout, reset and restart contract](brownout-restart-contract.md) | Registered `BR-*` slow-depletion/fast-collapse policy, threshold ownership, fail-inactive motor permission, reset defaults, fresh-intent recovery, sizing equations and verification contract; numeric values remain evidence-gated | A |
| [Compute/control architecture](compute-control-architecture.md) | Registered `CA-01…16`: node ownership, selected base controller class, differential links, C2 display relay, process boundaries, authority leases, watchdog hierarchy, boot/arm/update/logging and new fault obligations | A |
| [Compute/control component screen](compute-control-component-screen.md) | `CCD-*` exact selections, implementation leads, rejections, dated India sourcing snapshot and receiving tests; purchase remains separately authorized | A |
| [Operating situations](operating-situations.md) | Reader-first audited umbrella map: every situation with its `OM/EN/BS/PC/AL/HL/EV`, loads, cases, faults and evidence | A |
| [Intent](intent.md) | The design question and the gate question, kept separate; traceability; inherited inputs; non-goals; the phase ladder | A |
| [State register](state-register.md) | Orthogonal mode, energy, behaviour, person-continuity, action-lifecycle and health dimensions; events, qualification cases, forbidden concurrency and `MD-01` | A |
| [State coverage matrix](state-coverage-matrix.md) | Requirement → runtime vector → qualification case → load profiles → rules/faults → evidence | A |
| [Load model](load-model.md) | Named per-load profiles, time-scale classes, aggregation rules and measurement dependencies; contains no competing numeric budget | A |
| [Power architecture](power-architecture.md) | Registered Part-2 domain/rail baseline: safety, application, motor and charge paths; independent C2/base safety branches; return topology; power-state matrix; registered `PB-*` keys | A |
| [Link contract](link-contract.md) | Registered Part-4 C0↔C2 definition (`RP02-P4-REG-01`), C0↔C3 `BASE_*` (`RP02-P4-REG-02`), coordination fields (`RP02-P4-REG-03`). Byte layouts, type numbers, baud and measured timeouts remain open | A |
| [Phase A reference](phase-a/README.md) | Exploratory single-schema C0/C2 frame codecs, host safety/time model, board-role reservations and logging record; not scored or flashed | A |
| [Candidate circuits and paper review](phase-a/candidate-circuits-review.md) | Candidate compute/C2/display, E-stop and link circuits plus unscored G01/G06 walk | A |
| [Fault matrix](fault-matrix.md) | `F-01…F-30` injected faults × inhibit / reject / expose / recover, including Part-3 process, watchdog, relay, differential-link, storage and reset cases | A (rows), B (campaign) |
| [Rig](rig.md) | The distribution bench: fuses, INA-class monitors, E-stop, real-versus-substitute loads with equivalence records, procedures | A (design), B (build) |
| [Gates](gates.md) | Candidate registrations for G01/G04/G05/G06; what RP-02 records against the reshaped G02 invariant and the G03/SC-14 rehearsal | A (registration) |
| [Decision](decision.md) | Gate outcomes, the **ADR closure ladder** (ADR-06 split into architecture and sizing), selected Pi 5 record and remaining candidate register | — |
| [Prototype open items](../openitems.md) | Folder-wide remaining-open index; ratings, SKUs and gates stay in their owning files | — |
| `runs/` | Run records per `../../01-system/run-record-convention.md` | — |

## Owned elsewhere — link, do not copy

| Subject | Home | Why it is not here |
|---|---|---|
| **Power / energy / thermal budget** | [`power-energy-ledger.md`](../../01-system/power-energy-ledger.md) | Serves every prototype that energizes anything. Two budgets means one is wrong. RP-02 *populates* it |
| **Monotonic timebase** | [`timebase.md`](../../01-system/timebase.md) | A continuous-workstream deliverable; RP-01's first scored run needs it too. RP-02 *validates* it under G05 |
| System control-topology study | [`control-topology-options.md`](../../01-system/control-topology-options.md) v0.14 | Part 3 consumes and closes its ownership/link choices at design level; physical evidence still closes ADR-03/ADR-12 |
| Bench tools, PSU and E-stop rules, battery gate | [`workbench.md`](../../01-system/workbench.md) | Programme-wide |
| Candidate parts and cost range | [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md) | Programme-wide |
| Head harness partition and yaw boundary | [`head-harness-routing-study.md`](../../01-system/head-harness-routing-study.md) | Shared with RP-01 |
| Run identity | [`run-record-convention.md`](../../01-system/run-record-convention.md) | Programme-wide |

## Why the gates changed shape (plan v1.10)

G01, G04, G05 and G06 are properties — a fuse coordinates or it does not; a stale command is rejected or executed. They stay as pass/fail gates. G02 (peak coexistence) and G03 (runtime) are budgets: they need hardware that does not exist at stage 2, they reopen every time a subsystem arrives, and G03 duplicates SC-14. So G02 became a **standing invariant with a re-run rule** owned by the ledger, and G03 became an **early-warning rehearsal with recorded margin**, with the 20-minute requirement closing where it already lives — SC-14 at integration. The reasoning is in `intent.md` §2 and the amendment in the plan's approval note.

## Relationship to RP-01

Circular, and named — but the two closures are different objects. RP-01's **complete-head `W` mass** (M900) cannot close while M008 is `U`; that is unchanged. Layout 03 **paper demand** does not wait on that weigh-in: it is complete as of 2026-09-13 (`fullproofmath.md`), using the 20 g `E` C2 case plus 10/20/35 g sensitivity. C2's timing and electrical validity is still RP02-G05; RP-01's first scored run still needs RP-02's timebase. The servo **family** is still unselected and still sets the servo rail, but RP-01 now has a named paper candidate — XC330-M288-T (C01), proposed 5 V, paper approval OPEN — which is a leading PA-04 working assumption, not a collapse. Resolution: RP-02 Phase A runs now and unblocks RP-01; Phase B may use C01 as a named reference load without treating a purchase as a family freeze; load-dependent gates that need the frozen rail follow selection.

## What to do next, in order

1. Implement the C0/C2 shared schema, board-role pin maps and authority-lease state machines from the registered Part-4 definition, including `RP02-P4-REG-03` cue identity / `start_at_us` / `FACE_REPORT` / `LIGHT_REPORT` / extra `NACK` values. C3 `BASE_*` **semantics** are registered (`RP02-P4-REG-02`); byte layouts and the candidate TTL/heartbeat/queue numbers stay unregistered until Phase A measures them. The C3 board-role header is `phase-a/c3_board_role.h`. No hardware purchase is required for codec/unit simulation.
2. Implement `timebase.md` and `link-contract.md` v0.6 on the DevKitC-1 twin, first TTL loopback and then THVD1451 differential breakout pairs; exploratory timing runs do not wait on carrier PCBs.
3. Freeze the first executable case configurations and register G05/G04 numeric thresholds before scored link/watchdog work, including `F-23…30`.
4. Convert the surviving `PCD-*`/`CCD-*` leads into reviewed candidate circuits and bench configurations; choose exact transceiver/watchdog suffixes only from the measured timing and harness conditions.
5. Build the distribution/link rig when the required instruments arrive and run G01 review plus differential-link/watchdog pilot injections.
6. After RP-01 selects a servo family, collapse PA-04/servo transceiver and begin scored Phase B. RP-03 supplies the motor-driver/sensor pin freeze and representative drive load; C01 remains a reference, not a freeze.

## Organization record — 2026-09-08

Created by builder direction after the RP-01 head reached its first packaging study and the C2 module was selected. The folder deliberately does not mirror `RP-01-head/`: there is no `physics.md` (the ledger is the model), no `storyboard.md` (the state register is its analogue), no `concepts/` or `cad/`. The power/energy ledger and timebase strategy were placed in `01-system/` under the same rule that kept the RP-01 CAD folder's sources in place — documents serving more than one consumer stay put and get linked.

Reconciled 2026-09-13 to RP-01 Layout 03 paper demand and C01 (XC330-M288-T) without selecting a servo family or collapsing PA-04.
