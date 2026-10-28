# RP-04 — Coordinated Performance Architecture

| Field | Value |
|---|---|
| Status | **Phase A design-definition 2026-09-21.** `RP04-P1-REG-01`…`P6-REG-01`. Virtual composer **`CS-HYBRID`** with bounded waits. P-02 cue list validated. Observer **draft, not frozen**. `BD-08` open. No physical gate. ADR-05 open. **Blocked on Phase B/C.** |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-04; [`plan.md`](plan.md) |
| Purpose | Close **ADR-05** provisionally after measured G01–G05. Phase A only selects the virtual trigger adapter |

RP-01 is an object. RP-02 is states, links, and firmware/process boundaries. RP-03 is a vehicle plus local safety. **RP-04 is the first predominantly software-architecture prototype.**

## Start here

| Document | What it owns | Phase |
|---|---|---|
| [Intent](intent.md) | Why; C0/C2/C3/D1; two questions | A registered |
| [Situations](situations.md) | Catalogue + P-01 §11 + P-02 §12 cue list | A registered; P-02 paper |
| [Interface requirements](interface-requirements.md) | **Accepted** as RP-02 semantics (`RP02-P4-REG-03`); exploratory packed layout rev 2 | Request closed; codec host-only |
| [Observer protocol](observer-protocol.md) | G03 questions. Real clips only | **Not frozen** |
| [Research](research/README.md) | Family closed (`CS-HYBRID`); remaining = physical `TR-*` | Virtual software closed |
| [Runtime](runtime-architecture.md) | Shared layer; HYBRID trigger + wait language | A |
| [Timing budgets](timing-budgets.md) | `E` split: `T-LEAD` / `T-BEAT` / `T-DEAD` | Not G01 |
| [Prototype](prototype/README.md) | Virtual P-01; HYBRID waits; P-02 validator | A |
| [Gates](gates.md) | Candidates only | Open |
| [Decision](decision.md) | `BD-*`, registrations, `CS-HYBRID` | — |
| [Plan](plan.md) | Construction record | — |
| [Open items](../openitems.md) | Remaining index | — |

Namespaces: `P-0x` · `OX-*` · `CS-TIME/PROG/HYBRID` · `IR-*` · `BD-*` · `RP04-P/G` · `T-P01-*`.

## Controllers

`C0` Pi · `C2` head+safety · `C3` base+safety · `D1` face. No `C1`. Audio on C0 as a scored channel.

## What to do next

1. Phase B when the RP-01 head, D1, timebase, and audio stand-in exist. Engineering-tune on non-scored runs; freeze G03; then scored clips. Physical `TR-P01-*` are not closed by the virtual suite.
2. Close `BD-08` before implementing counter-yaw. Do not execute P-02 until the RP-03 base model exists.
3. RP-02 G04/G05 still own registering the packed layout (exploratory revision 2 is a host reference).

Do not delete `prototype` TIME/PROG adapters (`EXPERIMENTAL.md`). Do not treat virtual onsets as G01 `W`. Do not reopen UART/COBS unless measured G05 shows both 921 600 and 460 800 fail. Do not claim RP-04 or ADR-05 closed.
