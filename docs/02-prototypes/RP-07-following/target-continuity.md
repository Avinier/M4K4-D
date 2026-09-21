# RP-07 target continuity and selection

| Field | Value |
|---|---|
| Status | Paper policy; grace/search/confirmation numbers remain preregistration candidates |

## 1. Two identities

- **Track ID:** short-lived perception association within one camera/perception session.
- **Selection UUID:** behaviour-owned identity of the person deliberately selected for the current interaction/action.

They may map one-to-one while tracking is clean. Reacquisition may attach a new track ID to the same selection UUID only after the policy below accepts it.

## 2. State mapping

RP-07 uses the inherited `PC-01…PC-06` states:

```text
PC-01 no candidate
  → PC-02 candidate
  → explicit valid selection
  → PC-03 selected/fresh
  → evidence loss
  → PC-04 temporarily lost + immediate base brake
  → PC-05 stationary same-person reacquisition
  → PC-03 on confirmed match
  → PC-06 on expiry/rejection
```

No path exists from a different candidate directly to the existing `PC-03` selection.

## 3. Candidate confirmation

A candidate is confirmed only after bounded temporal evidence establishes a real, current person rather than a one-frame detection. Confirmation uses detection persistence, image quality and plausible geometry. Printed/displayed faces and mirrors remain documented false-lock cases, not safety proof.

## 4. Selection policy

Selection occurs only while stationary unless a later test explicitly allows otherwise. Preferred interaction flow:

1. invocation/action requests acquisition;
2. bounded head search produces candidate set;
3. if one unambiguous candidate occupies the acquisition region, core may select it under the approved interaction rule;
4. if candidates are ambiguous, Makad asks for clarification or waits; base remains stopped;
5. selection UUID and initial appearance/scale gallery are created;
6. come/follow is separately accepted only from fresh `PC-03`.

The RP-07 optical-axis fallback is acceptable for attention. A locomotion action uses the stricter unambiguous-selection rule in this document.

## 5. No-silent-switch invariant

While selection UUID `S` is valid:

- a new track cannot inherit `S` because it is larger, nearer the centre, or higher confidence;
- a track-capacity overflow cannot evict `S` merely to admit a new candidate;
- geometric proximity alone cannot reassign `S` after an occlusion involving multiple people;
- a failed reacquisition leaves `S` lost; it does not choose the “best available” person;
- explicit operator/behaviour reselection creates a new selection epoch and action authorization.

The gate metric for silent switches is exactly zero.

## 6. Reacquisition evidence

Each candidate receives independent terms:

| Term | Question |
|---|---|
| temporal/spatial | Is it consistent with the last known target state and elapsed time? |
| appearance | Does it match the selected session gallery better than distractors? |
| scale/range | Is its observed scale/range physically plausible? |
| continuity | Was it associated through part of the occlusion? |
| ambiguity margin | Is the best candidate sufficiently better than the runner-up? |
| persistence | Does the decision repeat across the registered confirmation interval? |

Acceptance requires all mandatory terms and a registered ambiguity margin. Low-quality evidence produces `UNKNOWN`, never a forced yes/no match.

## 7. Initial timing candidates

These are pilot starting points, not frozen gate thresholds:

| Quantity | Candidate |
|---|---:|
| Fresh for locomotion | Observation age ≤150 ms |
| Degraded/no new acceleration | >150 ms |
| Zero forward intent | By 250 ms without a qualifying observation |
| Identity grace while stopped | Within inherited 0.3–0.7 s band |
| Reacquisition confirmation | At least 3 consistent observations spanning ≥200 ms |
| Maximum same-person search | Pilot 3 s; register after variance is measured |

Command expiry and C3 heartbeat limits may be tighter and always dominate.

## 8. Gallery/privacy lifecycle

- Session-local crops/descriptors require an explicit active selection.
- Raw frames are not persistently written in normal operation.
- Engineering recordings are explicit, local by default, and listed in the evidence manifest.
- Selection clear, session expiry, or privacy reset removes the in-memory gallery.
- Logs retain numeric decisions and hashes, not unnecessary face crops.

## 9. Required continuity cases

- face turns away while body remains visible;
- partial and full temporary occlusion;
- target exits and re-enters;
- distractor crosses in front;
- distractor becomes larger/central/higher confidence;
- visually similar clothing;
- target changes pose or turns from front to back;
- head/base motion during target motion;
- stale track-selection command;
- camera/perception restart;
- track-capacity overflow;
- target and distractor re-enter together.
