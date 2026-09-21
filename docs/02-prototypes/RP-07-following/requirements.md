# RP-07 requirements

| Field | Value |
|---|---|
| Status | RP-07 paper requirements. `MUST` states architecture intent; numeric `TARGET` values remain unregistered until the gate freeze |
| Authority | Approved foundation and RP-01…RP-04 records only |

This document owns RP-07 perception and following requirements. It does not inherit requirements from exploratory or archived specification material.

## 1. Detection and observations

| ID | Level | Requirement |
|---|---|---|
| `R07-01` | MUST | Detect person candidates within the registered RP-07 lighting, distance, pose and FOV envelope. |
| `R07-02` | MUST | Every observation carries effective capture time, publish time, frame/session identity and age. |
| `R07-03` | MUST | Separate person existence, track association, selected-person match, bearing uncertainty and range uncertainty. |
| `R07-04` | MUST | Represent at least two simultaneous people as distinct candidate tracks; three is the paper target. |
| `R07-05` | MUST | Associate face/landmark evidence with a person track; loss of the face alone does not imply loss of the person. |
| `R07-06` | MUST | Treat raw images, detector boxes and tracker IDs as perception evidence, never direct motor commands. |
| `R07-07` | TARGET | Confirm a qualifying active-mode person candidate within 250 ms. |
| `R07-08` | TARGET | Refresh the active person detector at ≥10 Hz under representative load. |
| `R07-09` | TARGET | Publish selected-target state at ≥15 Hz, aiming toward 30 Hz when the measured pipeline permits. |

## 2. Selection and continuity

| ID | Level | Requirement |
|---|---|---|
| `R07-10` | MUST | Distinguish candidates from the selected person. Candidate presence never authorizes locomotion. |
| `R07-11` | MUST | `makad-core` owns selection UUID and epoch; perception only proposes evidence. |
| `R07-12` | MUST | Retain the current valid selection despite a distractor becoming larger, more central or more confidently detected. |
| `R07-13` | MUST | Never silently replace a lost or ambiguous selected person. A replacement requires a new explicit selection epoch. |
| `R07-14` | MUST | On selected-person evidence loss, brake first and preserve identity only for a bounded stopped grace interval. |
| `R07-15` | MUST | Reacquisition requires registered spatial, appearance, plausibility, ambiguity-margin and persistence evidence. |
| `R07-16` | MUST | A rejected or uncertain reacquisition results in continued stop or explicit loss, never forced selection. |
| `R07-17` | TARGET | Begin pilots with 0.3–0.7 s stopped identity grace; freeze the final value from pilot variance before scoring. |

## 3. Geometry and timing

| ID | Level | Requirement |
|---|---|---|
| `R07-20` | MUST | Calibrate camera intrinsics/distortion and full camera→head→body transforms, including translation. |
| `R07-21` | MUST | Use measured head/base state corresponding to effective capture time; commanded pose is not a substitute. |
| `R07-22` | MUST | Compensate known camera motion before interpreting image displacement as person motion. |
| `R07-23` | MUST | Characterize rolling-shutter/readout effects over the claimed head-motion envelope. |
| `R07-24` | MUST | Publish body-frame bearing and uncertainty; publish coarse range only when a named cue is valid. |
| `R07-25` | MUST | Treat camera-derived range as approximate behavioural data, never collision-safety distance. |
| `R07-26` | TARGET | Established effective-capture-to-target-publication latency ≤100 ms P95 under representative load. |
| `R07-27` | TARGET | Absolute body-bearing error ≤1.5° P95; ≤3° is the paper minimum-acceptable V1 direction pending registration. |
| `R07-28` | TARGET | Settled stationary bearing jitter ≤0.5° RMS per relevant axis. |

## 4. Come and follow

| ID | Level | Requirement |
|---|---|---|
| `R07-30` | MUST | Search/acquire may begin visually after invocation; spatial hearing is not required. |
| `R07-31` | MUST | Come starts in the approved approximately 1–2 m case and settles in the approved approximately 0.6–0.9 m band. |
| `R07-32` | MUST | Follow operates only on the approved marked indoor route no longer than approximately 3 m and never above 0.5 m/s. |
| `R07-33` | MUST | Forward motion requires fresh selected-person bearing, usable coarse range, current action authority and C3 clearance/readiness. |
| `R07-34` | MUST | Range/bearing uncertainty and observation age reduce or inhibit motion; they never increase authority. |
| `R07-35` | MUST | Target loss, stale/frozen frames, invalid calibration, missing pose, overload or link failure produces bounded brake/stop/failure. |
| `R07-36` | MUST | Come/follow completion requires measured stop/settle, not merely a transient perception sample. |

## 5. Safety and permissions

| ID | Level | Requirement |
|---|---|---|
| `R07-40` | MUST | C3 obstacle, cliff, readiness, expiry and stop authority overrides all person-following goals. |
| `R07-41` | MUST | Tabletop, inhibited, hard-stop and charging modes reject ordinary come/follow. |
| `R07-42` | MUST | Restoring perception, clearance, a controller or a link never resumes an old action automatically. |
| `R07-43` | MUST | Perception has no actuator device access and cannot bypass `makad-core`, C2 or C3. |
| `R07-44` | MUST | Silent target switches, blind continuation, stale-goal execution, unauthorized tabletop motion and automatic old-action resume each have a required scored count of zero. |

## 6. Compute, replay and privacy

| ID | Level | Requirement |
|---|---|---|
| `R07-50` | MUST | Meet mandatory perception/control timing under representative simultaneous camera, UI, audio, core, link and logging load. |
| `R07-51` | MUST | Use bounded queues and drop obsolete frames rather than accumulating latency. |
| `R07-52` | MUST | Expose per-stage latency, dropped frames, CPU, memory, temperature, throttling and health. |
| `R07-53` | MUST | Support replay from frames, source metadata, calibration and recorded joint/base states. |
| `R07-54` | MUST | Normal operation does not persist raw video merely because tracking is active. |
| `R07-55` | MUST | Session-local appearance evidence expires with the selection/session and is not named biometric identity. |
| `R07-56` | MUST | Scored runs carry immutable software/model/configuration/calibration/rig revisions and joinable external video. |

## 7. Registration boundary

The numeric targets in `R07-07…09`, `R07-17`, and `R07-26…28` are engineering starting points. They become pass/fail thresholds only when copied into a complete `gates.md` registration with conditions, repetitions, instruments, uncertainty, freeze date and builder approval before scored data are inspected.

