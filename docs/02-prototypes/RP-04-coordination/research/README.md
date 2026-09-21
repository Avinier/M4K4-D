# RP-04 research

| Field | Value |
|---|---|
| Status | **Family closed. Literature supports the selected TIME/PROG/HYBRID taxonomy.** Virtual wait language and P-02 cue list closed. Remaining = physical HYBRID validation. ADR-05 open |
| Owner | Project builder |
| Bound | `BD-07`; [`literature.md`](literature.md); [`experiment-spec.md`](experiment-spec.md) compact statement |

There is no `research.md` at the RP-04 root. This folder is the research record.

## Compact statement

> Test whether a bounded HYBRID cue list—using scheduled time only for authored perceptual lead and measured source/progress events for causal phase advancement—can execute P-01 and P-02 on physical controllers with bounded interruption, honest degradation, reproducible settling, and better observer-rated unity than independent dispatch. Reopen score representation only if P-02’s discrete hand-off cannot be expressed without ad hoc runtime logic; treat continuous counter-yaw as an executor/control-contract question, not evidence for a graph by itself.

Do not add architecture-family or middleware research. The 2026-09-21 Exa pass **supports the selected taxonomy**; it did not reopen the family.

## Files

| File | What it owns | Status |
|---|---|---|
| [Literature](literature.md) | Four axes from adjacent practice; timing split; interruption; observer | **Pass 2026-09-21.** Supports taxonomy. Not G01 |
| [Trigger comparison](trigger-comparison.md) | TIME / PROG / HYBRID; axes; selection rule; virtual winner | **Closed** `RP04-P3-REG-01` / `P5-REG-01`. Literature-grounded |
| [Experiment spec](experiment-spec.md) | Wake phase gates, P-02 cue-list criterion, falsifiers, trial matrix, G03 endpoints, ablation | Virtual software closed; physical `TR-*` open |

## Already decided (do not re-research)

- Four axes: only **trigger** was compared. Lifecycle and supervision are shared. Graph is representation, not a third trigger. Literature **supports** TIME / PROG / mixed lists (QLab/MSC/Timeline/BML). Makad’s exact-one-trigger rule is ours.
- Virtual winner: **`CS-HYBRID`**. TIME/PROG retained as evidence (`prototype/EXPERIMENTAL.md`). Exa redo **kept** this.
- Catalogue: P-01…P-03 plus overlays. Honest independent baseline. Audio/eyes as timing channels.
- Counter-yaw is an executor primitive (Disney joystick; Haru VOM). P-03 abandons world-gaze lock. **`BD-08`** (where it runs, who supplies base yaw) is open until implementation.
- Wake wait: **`any(face, light)` + `T-DEAD`**. Implemented in the HYBRID harness.
- P-02 discrete list: written and validated. No graph. No executable spike until RP-03.
- `T-DEAD` is 300 ms from that wait’s intended start, not 300 ms stacked after `T-BEAT`.

## Remaining questions (empirical)

1. On measured controllers, do G01–G05 and the primary G03 endpoint hold — and if “better,” was it timing, counter-motion, or choreography?
2. Close `BD-08` before implementing `counter_yaw`. Physical `TR-P01-*` / `TR-P02-*` are not satisfied by the virtual suite.

Detail and falsifiers: [`experiment-spec.md`](experiment-spec.md). Axes and numbers: [`literature.md`](literature.md).
