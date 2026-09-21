# RP-07 gate registration workbook

| Field | Value |
|---|---|
| Status | **Candidate sheets complete. Registered numeric section empty. No scored run.** |
| Governing gates | `RP07-G01…G07` from `risk-prototype-plan.md` |

## 1. Registration rule

Before the first scored run, every gate receives:

- exact metric and computation;
- pass threshold/range;
- rationale and source;
- controlled conditions and exclusions;
- repetitions and aggregation;
- instruments, calibration and uncertainty;
- software/model/calibration/rig revisions;
- freeze date and builder approval.

Pilots are retained and labelled. A threshold change after viewing scored results creates a new gate version and fresh test set.

## 2. `RP07-G01` — acquisition

| Field | Candidate content |
|---|---|
| Metric | Confirmed-candidate success/latency; detection recall/false positives; geometry validity by distance/light/pose/FOV |
| Candidate direction | Active acquisition ≤250 ms; initial test direction ≥18/20 valid trials; active detector target ≥10 Hz. These are RP-07 paper candidates, not inherited or frozen values |
| Conditions | Registered nominal envelope plus declared adverse strata; motors inhibited for perception score |
| Repetitions | **OPEN** beyond inherited test direction; stratified, not one pooled total |
| Instruments | Camera metadata, annotations, replay/live logs, synchronized video where live |
| Freeze | **EMPTY** |

## 3. `RP07-G02` — continuity

| Field | Candidate content |
|---|---|
| Metric | Silent selected-person switches; fragmentation; correct reacquisition/rejection/unknown; loss/reacquisition time |
| Non-negotiable | Silent switches = **0** in every scored case |
| Candidate policy | 0.3–0.7 s stopped identity grace; multi-observation confirmation; exact values open |
| Conditions | Occlusion, exit/re-entry, crossing and similar distractor, head/base motion, capacity overflow |
| Repetitions | **OPEN** |
| Freeze | **EMPTY** |

## 4. `RP07-G03` — come

| Field | Candidate content |
|---|---|
| Metric | Final person range, measured speed, contact, overshoot, settle dwell, action outcome, loss/obstacle stop |
| Existing boundary | Start approximately 1–2 m; settle 0.6–0.9 m; no harmful contact |
| Open | Pass rate, dwell, speed schedule, maximum overshoot, range uncertainty, stop margin |
| Conditions | Distances, bearing, lighting, target small motion, loss and obstacle |
| Repetitions | **OPEN** |
| Freeze | **EMPTY** |

## 5. `RP07-G04` — follow

| Field | Candidate content |
|---|---|
| Metric | Route completion; target distance error/distribution; speed; stability; continuity; safety interventions |
| Existing boundary | Route ≤approximately 3 m; speed ≤0.5 m/s; one gentle turn |
| Open | Setpoint/band, pass rate, oscillation/stability limits, allowable interventions |
| Conditions | Straight, turn, stop, partial/complete occlusion, exit/re-entry, distractor, obstacle |
| Repetitions | **OPEN** |
| Freeze | **EMPTY** |

## 6. `RP07-G05` — stale and fault safety

| Field | Candidate content |
|---|---|
| Metric | Fault/loss-to-zero-goal, fault/loss-to-deceleration, measured stop, stale command execution count, unintended resume count |
| Non-negotiable | Blind continuation = 0; stale replay/resume = 0 |
| Candidate freshness | Fresh ≤150 ms; no new acceleration beyond; zero forward goal by 250 ms—pilot only |
| Conditions | `F07-01…20` as applicable; worst registered speed/load |
| Open | Physical stop time/distance and percentile/repetition |
| Freeze | **EMPTY** |

## 7. `RP07-G06` — permissions and local authority

| Field | Candidate content |
|---|---|
| Metric | Unauthorized wheel command/motion count; C3 override success; fresh-arm requirement after clearing |
| Non-negotiable | Ordinary tabletop come/follow motion = 0; safety override failures = 0; automatic old-action resume = 0 |
| Conditions | Tabletop request; mode switch during action; obstacle/cliff/link/controller conflicts |
| Repetitions | Every registered conflict case, count **OPEN** |
| Freeze | **EMPTY** |

## 8. `RP07-G07` — evidence

| Field | Candidate content |
|---|---|
| Metric | Runs with complete immutable manifest and joinable camera→decision→goal→safety→motion→video timeline |
| Candidate threshold | 100% scored runs explainable; no unexplained time segment or missing revision |
| Conditions | All G01…G06 scored runs |
| Instruments | Project monotonic timebase, ring log, hashes, external timing cue/video |
| Freeze | **EMPTY** |

## 9. Supporting inherited compute/geometry checks

These may become sub-gates or mandatory conditions during registration:

- selected-target publication ≥15 Hz;
- established capture-to-publication latency ≤100 ms P95;
- bearing error target ≤1.5° P95, minimum acceptable V1 ≤3°;
- no OOM, no swap in scored interaction, recorded memory margin;
- no thermal throttling in representative enclosure/load;
- RP02 peak-coexistence invariant rerun with the RP-07 workload;
- calibrated source/joint/base time alignment sufficient for claimed motion accuracy.

## 10. Registered thresholds and outcomes

**EMPTY.**

Do not enter PASS/FAIL until the builder freezes the complete sheets and scored evidence exists.
