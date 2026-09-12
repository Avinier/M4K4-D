# RP-02 — Electrical/Control Backbone

| Field | Value |
|---|---|
| Status | **Planning open, reconciled 2026-09-12.** No state registered, no gate registered, no run executed. Phase A work is live; Phase B waits on RP-01's servo selection and an SBC candidate; Phase C waits on the battery gate |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.11 §RP-02 |
| Purpose | Close **ADR-03** (controller backbone), **ADR-12** (internal communication and timebase) and the *architecture* half of **ADR-06** (battery, rails, isolation, low-energy policy); bound the *sizing* half |

RP-01 is an object. RP-02 is a set of states and interfaces: a tree of rails, three boards, a message contract across a moving joint, and a space of concurrent operating conditions. Every subsystem will work alone; AD-08 says the peaks happen together. RP-02 is the instrument that makes the coexistence failure visible before the enclosure exists.

## Start here

| Document | What it owns | Phase live |
|---|---|---|
| [Intent](intent.md) | The design question and the gate question, kept separate; traceability; inherited inputs; non-goals; the phase ladder | A |
| [State register](state-register.md) | The **proposed, unregistered** concurrent states `S00…S17` and exact 20-minute draft `MD-01` — RP-02's storyboard | A |
| [Power architecture](power-architecture.md) | Two-domain rail tree, layered protection, chemistry and pack-voltage comparison, brownout ordering, measurement points — `PA-01…PA-10`, evidence class `E` | A |
| [Link contract](link-contract.md) | SBC ↔ C2 ↔ display message set, framing, expiry, heartbeat, recovery semantics, bandwidth and timing candidates — v0.2, the artifact that outlives the prototype | A |
| [Fault matrix](fault-matrix.md) | `F-01…F-16` injected faults × inhibit / reject / expose / recover, with injection methods and evidence | A (rows), B (campaign) |
| [Rig](rig.md) | The distribution bench: fuses, INA-class monitors, E-stop, real-versus-substitute loads with equivalence records, procedures | A (design), B (build) |
| [Gates](gates.md) | Candidate registrations for G01/G04/G05/G06; what RP-02 records against the reshaped G02 invariant and the G03/SC-14 rehearsal | A (registration) |
| [Decision](decision.md) | Gate outcomes, the **ADR closure ladder** (ADR-06 split into architecture and sizing), candidate register with nothing selected | — |
| `runs/` | Run records per `../../01-system/run-record-convention.md` | — |

## Owned elsewhere — link, do not copy

| Subject | Home | Why it is not here |
|---|---|---|
| **Power / energy / thermal budget** | [`power-energy-ledger.md`](../../01-system/power-energy-ledger.md) | Serves every prototype that energizes anything, and the stage-6 `engineering-budgets.md`. Two budgets means one is wrong. RP-02 *populates* it |
| **Monotonic timebase** | [`timebase.md`](../../01-system/timebase.md) | A continuous-workstream deliverable; RP-01's first scored run needs it too. RP-02 *validates* it under G05 |
| Control topology, C1/C2, C2 module | [`control-topology-options.md`](../../01-system/control-topology-options.md) v0.10 | RP-02 closes this study into ADR-12; it does not fork it |
| Bench tools, PSU and E-stop rules, battery gate | [`workbench.md`](../../01-system/workbench.md) | Programme-wide |
| Candidate parts and cost range | [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md) | Programme-wide |
| Head harness partition and yaw boundary | [`head-harness-routing-study.md`](../../01-system/head-harness-routing-study.md) | Shared with RP-01 |
| Run identity | [`run-record-convention.md`](../../01-system/run-record-convention.md) | Programme-wide |

## Why the gates changed shape (plan v1.10)

G01, G04, G05 and G06 are properties — a fuse coordinates or it does not; a stale command is rejected or executed. They stay as pass/fail gates. G02 (peak coexistence) and G03 (runtime) are budgets: they need hardware that does not exist at stage 2, they reopen every time a subsystem arrives, and G03 duplicates SC-14. So G02 became a **standing invariant with a re-run rule** owned by the ledger, and G03 became an **early-warning rehearsal with recorded margin**, with the 20-minute requirement closing where it already lives — SC-14 at integration. The reasoning is in `intent.md` §2 and the amendment in the plan's approval note.

## Relationship to RP-01

Circular, and named: RP-01's mass cannot close until M008 is weighed, and C2's validity is RP02-G05; RP-01's first scored run needs RP-02's timebase; RP-01's servo family sets RP-02's servo rail. Resolution: RP-02 Phase A runs now and unblocks RP-01; RP-02's load-dependent gates follow RP-01's selections.

## What to do next, in order

1. Read `intent.md` §2 and approve or amend the design/gate split — everything below cites it.
2. Approve, adjust and **register** the state set and `MD-01` in `state-register.md`.
3. Seed `power-energy-ledger.md` `D` rows from datasheets: C2 (Espressif), display board (Waveshare wiki), SBC candidates, reference servo (ROBOTIS eManual). Replace planning ranges with sourced `D` values; keep `U` where no datasheet exists.
4. Implement `timebase.md` v0.2 §3 and `link-contract.md` v0.2 on the DevKitC-1 twin against a laptop; run the §6 offset-error measurement as `RP02-EXP-exploratory` runs. This is software and does not wait on any purchase.
5. Register G05 and G04 candidate thresholds (dated approval) before the first scored link/timing run.
6. Build the distribution board when the Korad, multimeter and logic analyzer arrive; run G01's review on it.
7. After RP-01 selects a servo family: collapse PA-04, give the ledger a servo-rail voltage, begin Phase B.

## Organization record — 2026-09-08

Created by builder direction after the RP-01 head reached its first packaging study and the C2 module was selected. The folder deliberately does not mirror `RP-01-head/`: there is no `physics.md` (the ledger is the model), no `storyboard.md` (the state register is its analogue), no `concepts/` or `cad/`. The power/energy ledger and timebase strategy were placed in `01-system/` under the same rule that kept the RP-01 CAD folder's sources in place — documents serving more than one consumer stay put and get linked.
