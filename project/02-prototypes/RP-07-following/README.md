# RP-07 — Person tracking and short household following

| Field | Value |
|---|---|
| Status | **Documentation baseline complete 2026-09-21. Paper architecture and test programme only. No camera recording, implementation, physical motion, scored run, gate pass, or ADR closure.** |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-07 |
| Primary decision | ADR-09 — person acquisition, continuity, localization, and following architecture |
| Depends on | Approved foundation; selected camera/system records; RP-01 head; RP-02 states/time/power; RP-03 base and local safety; RP-04 coordination |

RP-07 asks whether Makad can acquire, select, retain, lose, reacquire, approach, and follow one person inside the approved single-room envelope without moving on stale or ambiguous evidence.

This folder is intentionally a **complete paper prototype**. It specifies the implementation and evidence required later. It does not fabricate camera recordings, human-subject trials, motor tests, timings, thermal results, or safety outcomes.

## Start here

| Document | Owns |
|---|---|
| [Intent](intent.md) | Decision question, scope, completion boundary |
| [Inherited](inherited.md) | Exact upstream contracts; conflicts and precedence |
| [Requirements](requirements.md) | RP-07-owned perception, continuity, geometry, compute and control requirements |
| [Decision](decision.md) | Paper selections, open decisions, registration ladder |
| [Perception architecture](perception-architecture.md) | Capture, detection, tracking, appearance, face evidence, publication |
| [Interfaces](interfaces.md) | Typed observation, selection, goal, and feedback contracts |
| [Geometry and calibration](geometry-calibration.md) | Intrinsics, transforms, timestamps, bearing/range, uncertainty |
| [Target continuity](target-continuity.md) | Candidate/selection/loss/reacquisition and no-silent-switch policy |
| [Behaviour control](behaviour-control.md) | Search, head/base handoff, come, follow, braking, settling |
| [Safety and faults](safety-fault-matrix.md) | Authority order, stale/frozen evidence, injected failures |
| [Timing and compute](timing-compute.md) | Pi 5 workload, rates, latency, memory, thermal and fallback ladder |
| [Test matrix](test-matrix.md) | Recorded replay, live-no-motion, head-only, floor, distractor and fault cases |
| [Gates](gates.md) | RP07-G01…G07 candidate registration sheets and evidence rules |
| [Plan](plan.md) | Documentation-to-evidence execution sequence |
| [Evidence index](evidence/README.md) | Future run layout; presently empty by design |

Namespaces: `RP07-P*` paper registrations · `PS-*` perception stacks · `TM-*` target modes · `RC-*` range cues · `FC-*` following-control policies · `T07-*` tests · `F07-*` faults · `RP07-G*` gates.

## Paper conclusion

The implementation lead is `PS-HYBRID-01`:

1. Picamera2/libcamera acquisition from the locked Camera Module 3 Wide;
2. whole-person detection at a measured active cadence;
3. detection-based multi-person association;
4. an explicitly pinned selected-target identity owned by `makad-core`;
5. lightweight selected-target updates/prediction between detector refreshes;
6. appearance evidence used principally for selection and reacquisition, not biometric identity;
7. face/landmark evidence used for social gaze when available, never as the only long-range person evidence;
8. calibrated camera/head/body transforms and coarse, uncertainty-bearing range;
9. semantic, expiring come/follow goals from C0; C3 retains wheel and local-safety authority.

The lead is accepted for implementation comparison, not validated. The detector, tracker, appearance model, inference resolution, and exact rates remain benchmark selections.

## Hard boundaries

- Perception never commands motors.
- A candidate is not a selected person.
- A tracker ID is not durable human identity.
- Appearance matching is short-session continuity, not named or biometric recognition.
- Coarse visual range is never collision-safety distance.
- Loss or ambiguity brakes first; identity may be remembered while motion is stopped.
- Clearing an obstacle, link, or perception fault never resumes old motion.
- Tabletop mode rejects ordinary come and follow.
- RP-07 does not pass until representative physical evidence exists.

## Work that remains physical

The following are specified here but deliberately unperformed: camera calibration; recording the validation corpus; Pi 5 benchmarking; head-motion timing alignment; rolling-shutter characterization; live tracking; guarded base motion; come/follow trials; obstacle and cliff conflicts; injected faults; joined external video; and scored RP07-G01…G07 campaigns.
