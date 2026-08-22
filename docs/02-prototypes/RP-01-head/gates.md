# RP-01 Gate Registrations

| Field | Value |
|---|---|
| Status | Not started (thresholds come from `intent.md` + `physics.md`; freeze before first scored run) |
| Authority | Gate definitions and registration-record fields: `risk-prototype-plan.md` §RP-01. This file holds the registered numeric versions. |

Gates to register (from the plan):

- **RP01-G01 Safety** — bounded state for every injected stop/timeout/feedback-loss/restart case
- **RP01-G02 Three-axis Core** — roll, pitch, yaw each execute registered authored-motion cases under representative load
- **RP01-G03 Motion quality** — range, tracking, repeatability, reversal, overshoot, settling, noise, vibration, cross-axis
- **RP01-G04 Integration** — camera calibratable/usable, wiring survives endurance, safe unpowered state
- **RP01-G05 Buildability** — credible fabrication/assembly/calibration/service/sourcing path with complete cost range
- **RP01-G06 Evidence** — commands, state, current/voltage, faults, video correlatable per run

Each registration uses the plan's required fields: Gate ID, Metric, Threshold, Rationale, Conditions, Repetitions, Instrument, Freeze record (date + builder approval **before** scored data is inspected). Threshold changes after results create a new gate version with a documented reason and fresh test set — never an edit.

## Registered gates

*(none yet)*
