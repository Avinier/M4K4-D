# RP-04 Coordination Decision Record

| Field | Value |
|---|---|
| Status | Parts 1–6 **design-definition** registered 2026-09-21. Virtual adapter **`CS-HYBRID`** selected for the harness only. Observer **not frozen**. No physical gate. ADR-05 open |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21. `BD-05` superseded same day: no household observer panel |
| Construction record | [`plan.md`](plan.md) |

## 1. Builder decisions

| ID | Decision needed | Answer | Status | Consequence |
|---|---|---|---|---|
| `BD-01` | Three performances + overlays | Accept `P-01…P-03`; no fourth | **ACCEPTED 2026-09-21** | Catalogue frozen |
| `BD-02` | Honest independent baseline | Accept | **ACCEPTED 2026-09-21** | G03 comparison |
| `BD-03` | Audio timing channel | Accept stand-in | **ACCEPTED 2026-09-21** | Timing only |
| `BD-04` | Eye timing | Accept `E-*` timing | **ACCEPTED 2026-09-21** | Face in G03 |
| `BD-05` | Household / mock-video observer panel | **Rejected** (builder decision, not a literature finding). G03 is real Phase B/C clips only. Sequence: non-scored engineering tuning → freeze N/pass/clip-selection in `gates.md` → scored capture | **SUPERSEDED 2026-09-21** | No instrument-debug panel |
| `BD-06` | Consecutive-run count | After G05 cost | **DEFERRED** | G05 numeric |
| `BD-07` | Comparison budget | TIME/PROG/HYBRID; graph = representation axis | **ACCEPTED 2026-09-21** | Spikes done |
| `BD-08` | Counter-yaw primitive: where it runs, who supplies base yaw | Open. Must close before P-02 Phase C implementation. Graph cannot fix a slow C0-mediated yaw loop | **OPEN** | Executor contract, not representation |

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
| Frozen at design-definition | `intent.md`; `situations.md` catalogue; `BD-01…04/07`. `BD-05` superseded. `BD-08` open |
| Wire semantics | `interface-requirements.md` IR-01/02/03/05/07/08 + command NACKs accepted `RP02-P4-REG-03`. Exploratory packed layout revision 2 is a host reference |
| Not | Wire freeze. Gate pass. ADR-05 |

### RP04-P2-REG-01 — P-01 backpropagation (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `situations.md` §11 P-01 happy path and overlay deltas; §12 P-02 cue list (declarative, validator-backed) |
| Draft only | [`observer-protocol.md`](observer-protocol.md) v0.4. Questions only. **Not frozen.** G03 sequence: non-scored engineering tuning → freeze → scored capture |
| Not | G03. P-03 full sheets. Executable P-02 spike |

### RP04-P3-REG-01 — shortlist (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | Axes; spike set TIME/PROG/HYBRID; graph is representation not trigger; **predeclared selection rule** in `research/trigger-comparison.md` |
| Remaining research | [`research/literature.md`](research/literature.md) **supports the selected taxonomy** (2026-09-21); exact-one-trigger is Makad’s. Empirical: [`research/experiment-spec.md`](research/experiment-spec.md) |
| Not | ADR-05. Architecture freeze before spikes |

### RP04-P4-REG-01 — shared runtime (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `runtime-architecture.md` shared ownership/lifecycle/arbitration/recovery; `timing-budgets.md` `E` placeholders |
| Not | Trigger freeze (done in P5). G01 numbers |

### RP04-P5-REG-01 — virtual spikes (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `prototype/test_p01_spikes.py` shared + discriminating tests **pass**. Live adapter **`CS-HYBRID`**. TIME/PROG **retained** (`prototype/EXPERIMENTAL.md`) |
| Evidence | Discriminating: invalid time NACKs TIME and HYBRID time-tags, not PROG; stuck progress blocks PROG/HYBRID `P01-C04`, not TIME; restart no epoch-1 resume. 2026-09-21 extension: HYBRID `any(face, light)` + `T-DEAD`; named `HM-03.rise_commit`; P-02 validator |
| Not | ADR-05. G01 `W`. G03. Deleting loser adapters |

### RP04-P6-REG-01 — gate candidates (2026-09-21)

| | |
|---|---|
| Frozen at design-definition | `gates.md` metric list G01–G05 |
| Remains open | All thresholds; G03 N/pass/clip-selection (real clips); `BD-06`; `BD-08`; registered gate section empty |
| Not | Gate pass |

## 3. RP-02 interface disposition

**Semantics accepted `RP02-P4-REG-03` 2026-09-21.** Cue identity, optional `start_at_us`, `FACE_REPORT`/`LIGHT_REPORT`, `NACK(TIME_MODEL_INVALID|LATE|STALE_EPOCH)`. UART/COBS retained. Exploratory packed layout revision 2 assigns candidate widths and proves `BASE_STATE` at 62 bytes with safety fields retained. Lateness window numeric and G04/G05 registration remain open. Audio onset stays on C0. Virtual TIME evidence is unchanged. Rejection of a later registered layout would not unwind the virtual spikes.

## 4. Gate outcomes

All **NOT REGISTERED**.

## 5. ADR-05 ladder

**OPEN.** `CS-HYBRID` is the Phase A harness selection only. Close requires G01–G05 on measured executors.

## 6. Phase A architecture note

`runtime-architecture.md` trigger: **HYBRID** (per-cue `time` or `progress` — Makad’s exact-one-trigger rule). Not a general graph. Literature supports the taxonomy; it does not claim identity with QLab or BML.
