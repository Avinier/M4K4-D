# RP-04 gates (candidates)

| Field | Value |
|---|---|
| Status | **Candidates only.** No numeric freeze. No scored run. G03 N not registered |
| Owner | Project builder |
| Part | 6 paper |
| Registration | `RP04-P6-REG-01` 2026-09-21 design-definition of *metrics*, not thresholds |

Observer instrument is still a **draft**; scored G03 waits on pilot → freeze → Part 6 N/pass.

## Candidate physical / software gates

| Gate | Character | Metric (not yet threshold) | Conditions |
|---|---|---|---|
| RP04-G01 Timing | Measurement | Source vs witnessed onset, phase error, interrupt latency, settle; software jitter and feedback age | Timebase valid; eyes in frame; engineering LED cropped from observer exports |
| RP04-G02 Bounded interruption | Verification | `OX-CANCEL`, `OX-PREEMPT` §8.1, `OX-SAFETY`, `OX-STALE`, `OX-RESTART`: no stale cue, no auto-resume | Same start pose; local C2/C3 stop |
| RP04-G03 Coherence | Judgement | Frozen instrument vs honest baseline | **After** observer freeze; N/pass in a later registration, not the 6-person pilot |
| RP04-G04 Degradation | Verification | `OX-DENY`, `OX-INHIBIT-BASE`, `OX-DELAY`, `OX-TIME`: honest log, no false success | One representative deny, not a cartesian product |
| RP04-G05 Reproducibility | Verification | Consecutive runs from documented startup | Waits `BD-06` |

Registered section: **empty**.

Phase B/C still wait on RP-01 rig, D1, timebase, RP-03 G06. Virtual spikes are not G01 `W`.
