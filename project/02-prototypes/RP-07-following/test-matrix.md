# RP-07 test matrix

| Field | Value |
|---|---|
| Status | Complete test design; all execution/result cells `NOT RUN` |
| Rule | Pilot data may tune methods and estimate variance; scored thresholds freeze before scored trials |

## 1. Controlled factors

Each run selects and records a value from every applicable factor.

| Factor | Required levels/direction |
|---|---|
| Distance | 0.6, 0.9, 1, 2 and 3 m where geometry permits |
| Horizontal sector | Centre, intermediate left/right, useful-FOV edge |
| Vertical geometry | Standing, seated/crouched if in scope, camera/head pitch cases |
| Lighting | Registered bright, ordinary, dim household; backlight case |
| Appearance | Light/dark clothing, pattern, outer layer, skin-tone/face-accessory coverage |
| Pose/view | Front, side, back, walking toward/away/across |
| Head state | Settled; small tracking motion; registered search slew |
| Base state | Stopped; straight; gentle turn; braking |
| People | Target alone; target + distractor; similar-looking distractor |
| Visibility | Full; upper body; partial occlusion; complete temporary occlusion; exit/re-entry |
| System load | Perception only; representative integrated load; peak registered concurrency |

Exact lux, ambient, floor, clothing articles, subjects/test material and repetitions are filled at gate registration.

## 2. Phase A — offline and synthetic, no motion authority

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-A01` | Coordinate/ray unit vectors | Signs, frames and units match convention | NOT RUN |
| `T07-A02` | Recorded acquisition matrix | Candidate latency/recall/false positives reported by stratum | NOT RUN |
| `T07-A03` | Empty-room/media/mirror sequences | False locks characterized; no safety use | NOT RUN |
| `T07-A04` | Detector backend comparison | Same corpus/config accounting; winner by predeclared rule | NOT RUN |
| `T07-A05` | Multi-person association | Fragmentation and ID switches measured | NOT RUN |
| `T07-A06` | Selected-person lock | Distractor never silently replaces target | NOT RUN |
| `T07-A07` | Occlusion/re-entry | Same-person accept/reject/unknown behavior recorded | NOT RUN |
| `T07-A08` | Stale/frozen/out-of-order frames | Freshness/fault states and zero-goal timing correct | NOT RUN |
| `T07-A09` | Recorded head/base pose replay | Ego-motion compensation and uncertainty checked | NOT RUN |
| `T07-A10` | Range-cue replay | Error/bias/uncertainty coverage by cue and distance | NOT RUN |
| `T07-A11` | Deterministic replay repeat | Outputs within declared reproducibility tolerance | NOT RUN |
| `T07-A12` | IPC fuzz/invalid values | Consumers reject wrong epoch, NaN, stale and invalid geometry | NOT RUN |

## 3. Phase B — live camera, motors inhibited

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-B01` | Camera modes/focus/exposure | Selected mode and policy documented | NOT RUN |
| `T07-B02` | Intrinsic/extrinsic calibration | Residuals and uncertainty recorded | NOT RUN |
| `T07-B03` | Camera↔joint time alignment | Mean, P95, outliers and angular implication recorded | NOT RUN |
| `T07-B04` | Rolling shutter/head motion fixture | Validated motion envelope or explicit degradation | NOT RUN |
| `T07-B05` | Live acquisition matrix | Inherited acquisition/rate gates measured | NOT RUN |
| `T07-B06` | Live distractor/occlusion | No silent switches; loss/reacquisition trace | NOT RUN |
| `T07-B07` | Representative compute coexistence | Latency/rate/memory/thermal acceptance | NOT RUN |
| `T07-B08` | Camera/process restart | Session invalidation and bounded recovery | NOT RUN |
| `T07-B09` | Privacy/default operation | No unrequested persistent raw frames | NOT RUN |

## 4. Phase C — head only

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-C01` | Search sectors | Coverage, limits, interruption and timeout correct | NOT RUN |
| `T07-C02` | Acquire/orient | Smooth orient; no raw-box twitch; timing joinable | NOT RUN |
| `T07-C03` | Stationary target tracking | Bearing error/jitter and head settling pass | NOT RUN |
| `T07-C04` | Moving person | Sustained target updates without self-excited oscillation | NOT RUN |
| `T07-C05` | Face loss/body continuity | Anchor hysteresis prevents jumps | NOT RUN |
| `T07-C06` | Large head slew | Predicted/degraded behavior bounded; no false confidence | NOT RUN |
| `T07-C07` | Base-yaw relay fixture/simulation | C2 counter-yaw primitive meets timing or safely degrades | NOT RUN |

## 5. Phase D — guarded minimum-speed base

Prerequisites: applicable RP-03 gates, workbench readiness, Floor mode, physical E-stop, registered ballast/CoM, stopping limits and caught/guarded setup.

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-D01` | Fresh target alignment only | Base turns inside limits; head counter-yaw coordinated | BLOCKED / NOT RUN |
| `T07-D02` | Observation loss during alignment | Brake/stop within bound; no resume | BLOCKED / NOT RUN |
| `T07-D03` | Low-speed straight approach to marked surrogate | Range/control/stopping pipeline proven before person | BLOCKED / NOT RUN |
| `T07-D04` | Local obstacle conflict | C3 clamp wins and action reports safety stop | BLOCKED / NOT RUN |
| `T07-D05` | Tabletop denial | No ordinary base motion; denial logged | BLOCKED / NOT RUN |

## 6. Phase E — come

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-E01` | 1 m frontal come | Settle 0.6–0.9 m without contact/creep | BLOCKED / NOT RUN |
| `T07-E02` | 2 m frontal come | Same plus speed/stopping margin | BLOCKED / NOT RUN |
| `T07-E03` | Off-axis come | Align/arc policy remains stable | BLOCKED / NOT RUN |
| `T07-E04` | Target moves slightly during approach | Bounded response; no overshoot/contact | BLOCKED / NOT RUN |
| `T07-E05` | Target lost during approach | Immediate bounded brake then stationary reacquisition/failure | BLOCKED / NOT RUN |
| `T07-E06` | Obstacle introduced | C3 intervention; no automatic resume | BLOCKED / NOT RUN |

## 7. Phase F — follow

| ID | Case | Required result | Status |
|---|---|---|---|
| `T07-F01` | Straight ≤3 m route | Distance/speed/stability within registered bands | BLOCKED / NOT RUN |
| `T07-F02` | Gentle turn | Head/base handoff and distance stable | BLOCKED / NOT RUN |
| `T07-F03` | Temporary partial occlusion | Continuity without switch; motion eligibility obeyed | BLOCKED / NOT RUN |
| `T07-F04` | Complete brief occlusion | Brake first; stationary same-person reacquisition only | BLOCKED / NOT RUN |
| `T07-F05` | Target exit/re-entry | Stop; accept same target or fail honestly | BLOCKED / NOT RUN |
| `T07-F06` | Distractor crossing | Zero silent switches | BLOCKED / NOT RUN |
| `T07-F07` | Target stops/approaches robot | Smooth stop; no reverse/oscillation/contact | BLOCKED / NOT RUN |
| `T07-F08` | Obstacle/furniture conflict | Local safety wins; action terminal semantics correct | BLOCKED / NOT RUN |

## 8. Phase G — injected system faults

Execute `F07-01…20` first without motion, then only the safe relevant subset on the guarded physical rig. Each run records fault onset, first affected observation/goal, C3 reaction, measured motion, terminal state and whether a fresh action was required afterward.

## 9. Recording and instrumentation

- camera requests and metadata;
- detections/tracks/appearance decisions and selected UUID;
- calibration and configuration/model hashes;
- head commands/measured joints;
- base goals, C3 clamp/fault and measured odometry;
- CPU, memory, temperatures, clocks, fan, power where instrumented;
- external fixed video with visible timing cue and route marks;
- run manifest, deviations and operator annotations.

Human-subject recordings require explicit engineering-recording mode, local storage policy and deletion/retention record.

