# RP-01 Intent — Motion Storyboard

| Field | Value |
|---|---|
| Status | Draft |
| Feeds | `physics.md` (α_peak, ranges), `gates.md` (registered motion cases), RP-01 procedure steps 3–5 |
| Method | Two passes, kept separate: authored intent first (no numbers), quantification second. See `docs/intuition.md` §5.1 steps 1–2. |

## Pass 1 — Authored moves (character terms, no numbers)

Name 8–12 moves. Describe what the move *is* and what it must *feel like*. Sources of truth: the two Core scenarios, the wake performance description, EVE/R2-D2/BB-8 reference. Do not write numbers here.

| # | Move | Description (feel, context, what it communicates) |
|---|---|---|
| 1 | Wake rise | From head-down idle to attentive, as one coordinated performance with eyes/LED/audio. Deliberate, not snappy — "waking up," not "switching on." |
| 2 | Startle | Fast recoil then freeze. The one genuinely violent move; intensity carried by eyes/head, per MEM-20260812-07 the base does not lead. |
| 3 | Curious tilt | Slow roll toward a speaker/object of interest. Reads as attention and processing. |
| 4 | Tracking correction | Small yaw/pitch adjustments holding gaze on a slowly moving person. Must be invisible as *motion* — only the sustained eye contact should register. |
| 5 | Idle micro-bob | Procedural low-amplitude aliveness while attentive. Never mechanical-looking repetition. |
| 6 | Acknowledge nod | Short pitch dip confirming a request. Crisp onset, clean settle. |
| 7 | Settle to rest | Return to safe head-down pose. Ease-out, no clunk at the end stop. |
| 8 | … | (fill: search sweep, excited follow-through after spin, recoil-and-return, sleep droop…) |

## Pass 2 — Quantification

One row per move from Pass 1. α_peak derives from amplitude + time-to-peak (for a smooth min-jerk-ish move, α_peak ≈ 2×amplitude/t_peak² is a serviceable first estimate). Record the source of every number — footage, human data, acted mockup — so a later revision knows what it's overturning.

| Move | Axis/axes | Amplitude (°) | Duration (ms) | Time-to-peak (ms) | ω_peak (°/s) | α_peak (°/s²) | Precision class (°) | Settle (ms, criterion) | Source |
|---|---|---|---|---|---|---|---|---|---|
| Wake rise | pitch+yaw | | | | | | | | |
| Startle | pitch(+roll) | | | | | | | | |
| Curious tilt | roll | | | | | | | | |
| Tracking correction | yaw, pitch | ~±4 | | | | | ≤0.5 repeatability, ≤1 reversal loss | | MEM-20260810-02 |
| Idle micro-bob | pitch | | | | | | | | |
| Acknowledge nod | pitch | | | | | | | | |
| Settle to rest | all | | | | | | | | |

### Derived envelope (fill after the table)

- Required range per axis: roll ± __°, pitch __° to __°, yaw ± __°
- Worst-case α_peak (sizing case, probably startle): __ °/s² on __ axis
- Smallest intentional move (backlash budget driver): __° on __ axis
- Hardest settle requirement: __ ms to within __° after __

## Notes / open questions

- Number sources still needed: frame-scrubbed reference clips, 240 fps acted mockup.
- These values are hypotheses; they become preregistered gate inputs in `gates.md` and are only revised via a new gate version, never silently.
