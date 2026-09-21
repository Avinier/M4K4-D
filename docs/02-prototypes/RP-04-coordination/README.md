# RP-04 — Coordinated Performance Architecture

| Field | Value |
|---|---|
| Status | **Phase A design-definition 2026-09-21.** `RP04-P1-REG-01`…`P6-REG-01`. Virtual composer **`CS-HYBRID`**. Observer **draft, not frozen**. No physical gate. ADR-05 open |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-04; [`plan.md`](plan.md) |
| Purpose | Close **ADR-05** provisionally after measured G01–G05. Phase A only selects the virtual trigger adapter |

RP-01 is an object. RP-02 is states, links, and firmware/process boundaries. RP-03 is a vehicle plus local safety. **RP-04 is the first predominantly software-architecture prototype.**

## Start here

| Document | What it owns | Phase |
|---|---|---|
| [Intent](intent.md) | Why; C0/C2/C3/D1; two questions | A registered |
| [Situations](situations.md) | Catalogue + P-01 §11 sheets | A registered |
| [Interface requirements](interface-requirements.md) | **Accepted** as RP-02 semantics (`RP02-P4-REG-03`); not packed ICD | Request closed |
| [Observer protocol](observer-protocol.md) | Draft + pilot procedure | **Not frozen** |
| [Research](research/README.md) | Axes, TIME/PROG/HYBRID, selection rule | Shortlist + virtual select |
| [Runtime](runtime-architecture.md) | Shared layer; HYBRID trigger note | A |
| [Timing budgets](timing-budgets.md) | `E` software/perceptual | Not G01 |
| [Prototype](prototype/README.md) | Virtual P-01; 9 tests pass | A |
| [Gates](gates.md) | Candidates only | Open |
| [Decision](decision.md) | `BD-*`, registrations, `CS-HYBRID` | — |
| [Plan](plan.md) | Construction record | — |
| [Open items](../openitems.md) | Remaining index | — |

Namespaces: `P-0x` · `OX-*` · `CS-TIME/PROG/HYBRID` · `IR-*` · `BD-*` · `RP04-P/G` · `T-P01-*`.

## Controllers

`C0` Pi · `C2` head+safety · `C3` base+safety · `D1` face. No `C1`. Audio on C0 as a scored channel.

## What to do next

1. Household **pilot** of `observer-protocol.md` (~6, non-scored), then freeze the instrument.
2. RP-02: coordination **semantics** are accepted (`RP02-P4-REG-03`). Remaining work is packed layout / codec, not a new bus.
3. Phase B when the RP-01 head, D1, timebase, and audio stand-in exist.

Do not delete `prototype` TIME/PROG adapters (`EXPERIMENTAL.md`). Do not treat virtual onsets as G01 `W`. Do not reopen UART/COBS unless measured G05 shows both 921 600 and 460 800 fail.
