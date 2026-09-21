# RP-04 Coordination Decision Record

| Field | Value |
|---|---|
| Status | Parts 1–6 **design-definition** registered 2026-09-21. Virtual adapter **`CS-HYBRID`** selected for the harness only. Observer **not frozen**. No physical gate. ADR-05 open |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| Construction record | [`plan.md`](plan.md) |

## 1. Builder decisions

| ID | Decision needed | Answer | Status | Consequence |
|---|---|---|---|---|
| `BD-01` | Three performances + overlays | Accept `P-01…P-03`; no fourth | **ACCEPTED 2026-09-21** | Catalogue frozen |
| `BD-02` | Honest independent baseline | Accept | **ACCEPTED 2026-09-21** | G03 comparison |
| `BD-03` | Audio timing channel | Accept stand-in | **ACCEPTED 2026-09-21** | Timing only |
| `BD-04` | Eye timing | Accept `E-*` timing | **ACCEPTED 2026-09-21** | Face in G03 |
| `BD-05` | Pilot vs scored panel | Pilot ~6 non-scored; G03 N later | **ACCEPTED 2026-09-21** | Freeze waits on pilot |
| `BD-06` | Consecutive-run count | After G05 cost | **DEFERRED** | G05 numeric |
| `BD-07` | Comparison budget | TIME/PROG/HYBRID; graph = representation axis | **ACCEPTED 2026-09-21** | Spikes done |

## 2. Part registrations

| Part | Registration | Status |
|---|---|---|
| 1 | `RP04-P1-REG-01` | REGISTERED |
| 2 | `RP04-P2-REG-01` | REGISTERED (sheets). Observer **draft** |
| 3 | `RP04-P3-REG-01` | REGISTERED shortlist + selection rule |
| 4 | `RP04-P4-REG-01` | REGISTERED shared runtime + `E` budgets |
| 5 | `RP04-P5-REG-01` | REGISTERED spikes; **`CS-HYBRID` virtual select** |
| 6 | `RP04-P6-REG-01` | REGISTERED gate *candidates* only |

### RP04-P1-REG-01 — intent and catalogue (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `intent.md`; `situations.md` catalogue; `BD-01…05/07` |
| Wire semantics | `interface-requirements.md` IR-01/02/03/05/07/08 + command NACKs accepted `RP02-P4-REG-03`. Packed layout still open |
| Not | Wire freeze. Gate pass. ADR-05 |

### RP04-P2-REG-01 — P-01 backpropagation (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `situations.md` §11 P-01 happy path and overlay deltas (`OX-CANCEL`, `OX-PREEMPT`, `OX-DENY`, `OX-DELAY`, `OX-STALE`, `OX-TIME`, `OX-RESTART`, `OX-SAFETY` delta) with test IDs |
| Draft only | [`observer-protocol.md`](observer-protocol.md) v0.1. **Pilot not run. Not frozen.** Composer must not be tuned against it |
| Not | G03. Observer freeze. P-02/P-03 full sheets |

### RP04-P3-REG-01 — shortlist (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | Axes; spike set TIME/PROG/HYBRID; graph is representation not trigger; **predeclared selection rule** in `research/README.md` |
| Not | ADR-05. Architecture freeze before spikes |

### RP04-P4-REG-01 — shared runtime (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `runtime-architecture.md` shared ownership/lifecycle/arbitration/recovery; `timing-budgets.md` `E` placeholders |
| Not | Trigger freeze (done in P5). G01 numbers |

### RP04-P5-REG-01 — virtual spikes (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `prototype/test_p01_spikes.py` 9 tests **pass**. Live adapter **`CS-HYBRID`**. TIME/PROG **retained** (`prototype/EXPERIMENTAL.md`) |
| Evidence | Discriminating: invalid time NACKs TIME and HYBRID time-tags, not PROG; stuck progress blocks PROG/HYBRID `P01-C04`, not TIME; restart no epoch-1 resume |
| Not | ADR-05. G01 `W`. G03. Deleting loser adapters |

### RP04-P6-REG-01 — gate candidates (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `gates.md` metric list G01–G05 |
| Remains open | All thresholds; G03 N; `BD-06`; registered gate section empty |
| Not | Gate pass |

## 3. RP-02 interface disposition

**Semantics accepted `RP02-P4-REG-03` 2026-09-21.** Cue identity, optional `start_at_us`, `FACE_REPORT`/`LIGHT_REPORT`, `NACK(TIME_MODEL_INVALID|LATE|STALE_EPOCH)`. UART/COBS retained. Packed layouts, lateness window, and `BASE_STATE` size remain open. Audio onset stays on C0. Virtual TIME evidence is unchanged. Rejection of a later packed layout would not unwind the virtual spikes.

## 4. Gate outcomes

All **NOT REGISTERED**.

## 5. ADR-05 ladder

**OPEN.** `CS-HYBRID` is the Phase A harness selection only. Close requires G01–G05 on measured executors.

## 6. Phase A architecture note

`runtime-architecture.md` trigger: **HYBRID** (per-cue `time` or `progress`). Not a general graph.
