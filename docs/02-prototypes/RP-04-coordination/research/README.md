# RP-04 mechanism comparison

| Field | Value |
|---|---|
| Status | **`RP04-P3-REG-01` shortlist; `RP04-P5-REG-01` selected `CS-HYBRID` (virtual).** TIME/PROG frozen as evidence. ADR-05 open |
| Owner | Project builder |
| Part | 3 shortlist; Part 5 selects |
| Bound | `BD-07` |

`CA-07` already excludes ROS 2 / micro-ROS from the V1 safety path. Adjacent practice is evidence about mechanisms, not a product shortlist.

## 1. Decision axes (not alternatives)

| Axis | Choice for Phase A | Shared vs compared |
|---|---|---|
| Score representation | **Versioned cue list** with optional per-cue trigger tag. Graph/statechart is **not** a competing trigger; it remains an open representation option if a cue list cannot express P-02 hand-off later | Representation axis. Not spiked as `CS-GRAPH` |
| Trigger mechanism | Compared: scheduled time vs progress/event vs **bounded** per-edge choice | Compared |
| Action lifecycle | Goal → accept/deny → start → feedback → succeed/abort/expire | **Shared** |
| Supervision | `makad-core` arbitrates intent; C2/C3 legally refuse and stop; lease loss kills the epoch (`CA-01/09/11`) | **Shared** |

A supervisory graph used with either trigger would make “hybrid wins” a tautology. **Do not spike a graph as a third trigger.**

## 2. Trigger adapters (spike set)

Decided before code:

| ID | Binding | What the adapter does |
|---|---|---|
| `CS-TIME` | Shared runtime + scheduled-time edges | Dispatch at `start_at − lead`. Models `start_at_us` (now on the ICD as `RP02-P4-REG-03`; packed layout still open) |
| `CS-PROG` | Shared runtime + progress/event edges | Next cue on named `source_onset` / `progress` / `complete` |
| `CS-HYBRID` | Shared runtime + **explicit per-cue** trigger (`time` **or** `progress`) | P-01: C02 time-lead for face/light; C03/C04 progress-chained to head |

`CS-HYBRID` is not an unbounded event graph. Each cue names exactly one trigger kind.

## 3. Predeclared selection rule (before any spike)

Recorded here so Part 5 cannot invent a prettier rule after seeing logs.

1. Every candidate **must** pass shared invariants: epoch flush, no claimed onset on deny, P-01 base HOLD, replay, stale reject, preempt epoch cut.
2. Then compare **identical** P-01 injections: delay robustness (`OX-DELAY`), time-model / late schedule (`OX-TIME`), stuck/missing progress, restart/no-resume (`OX-RESTART`), plus interruption (`OX-CANCEL` / `OX-PREEMPT`), required contract changes (does TIME need IR-03?), traceability, implementation complexity.
3. Select only after those injections.
4. **Demo smoothness is not a criterion.**
5. RP-02 rejection of scheduled start **penalizes or drops TIME**; it does not veto a virtual run already performed.

## 4. Paper matrix (P-01)

| Situation | `CS-TIME` | `CS-PROG` | `CS-HYBRID` |
|---|---|---|---|
| Happy P-01 HOLD | Aligns if leads are right; Linux jitter is the risk | Robust to latency; slow head delays audio/face follow-through | Face/light can still lead; head chains on progress |
| `OX-DELAY` late head | Later time cues still fire → likely desync | Waits → character stays together, may feel slow | Head-chained cues wait; time-tagged cues do not |
| `OX-TIME` invalid/late | Scheduled cues **must** NACK; empty performance unless fallback | Unaffected | Time-tagged cues NACK; progress cues continue |
| Stuck progress | Continues on the clock | **Hangs** until timeout/degrade | Only progress-tagged cues hang |
| `OX-PREEMPT` | Flush + new schedule | Flush + new first event | Same shared supervisor |
| `OX-RESTART` | Shared: no resume | Shared | Shared |
| IR-03 `start_at_us` | **Needs** the field (or equivalent) for a fair physical TIME | Not required | Needs it only for time-tagged cues |
| Spike cost | One dispatch clock | One wait table | Cue tag + both paths |

Shortlist: **all three** adapters. Part 5 ran them. **Selected `CS-HYBRID`** (virtual). See `decision.md` `RP04-P5-REG-01` and `prototype/README.md`.

## 5. Non-goals

No middleware catalogue. No ROS. No treating lifecycle/supervision as competing products. No ADR-05 from this note.
