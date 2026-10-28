# RP-07 intent

| Field | Value |
|---|---|
| Status | Documentation baseline; no evidence |
| Owner | Project builder |
| Created | 2026-09-21 |
| Governing plan | `../../01-system/risk-prototype-plan.md` §RP-07 |
| Feeds | ADR-09; ADR-05/07/12 integration; SC-08/11/12/15/24 |

## 1. Decision question

> Can Makad acquire, select, retain, lose, reacquire, approach, and follow one person within the approved household envelope while respecting observation freshness, moving-camera geometry, stopping distance, obstacles, mode permissions, and local safety?

The deliverable is not a compelling demo. It is an auditable answer, including bounded failure.

## 2. Design question

What detector/tracker/appearance/geometry/control split can meet the RP-07 requirements on the selected Pi 5 2 GB and Camera Module 3 Wide while leaving wheel safety on C3?

## 3. Gate question

Does that split pass RP07-G01…G07 over preregistered acquisition, continuity, come, follow, stale/fault, permission, and evidence cases without harmful contact, silent target switching, blind continuation, or unexplained timing?

## 4. Approved envelope

| Quantity | Boundary |
|---|---|
| Environment | One ordinary indoor household room |
| Route | Marked route no longer than approximately 3 m; one gentle turn |
| Follow speed | No greater than 0.5 m/s; initial powered trials lower |
| Come start | Approximately 1–2 m |
| Come settle band | Approximately 0.6–0.9 m |
| Initial acquisition | Visual search after invocation is sufficient; spatial hearing not required |
| People | Selected target plus at least one distractor in continuity cases |
| Safety | C3 obstacle/cliff/stop authority always outranks C0 following |

## 5. Core outcomes

1. A visible person becomes a candidate, not motion authority.
2. A deliberate selection produces one pinned short-session target.
3. Fresh observations yield timestamped bearing, coarse range, and uncertainty.
4. Head attention remains smooth while base motion is independently authorized.
5. Come settles in the approved band.
6. Follow maintains a registered distance over the bounded route.
7. Target loss, stale data, ambiguity, overload, or fault produces a bounded stop.
8. Reacquisition restores the same selected target or fails honestly.

## 6. Non-goals

- named-person recognition, biometric enrollment, or household-member database;
- general crowd navigation;
- multi-room following, stairs, doors, elevators, outdoor use, or unmarked public spaces;
- safety-grade depth from the RGB camera;
- SLAM or global navigation;
- autonomous selection of a replacement person;
- following while the selected person is visually absent;
- production certification or a claim of ISO 13482 compliance;
- replacing RP-03 obstacle/cliff sensing with camera detections.

## 7. Completion definition

### Documentation complete

This folder contains an inherited-contract map, paper architecture, explicit interfaces, calibration procedure, continuity policy, behaviour/control definition, fault matrix, compute plan, complete test matrix, gate sheets, and evidence layout.

### Prototype complete

Only after:

- the selected camera and Pi workload are measured;
- software and configuration revisions are frozen for each run;
- all gate thresholds are registered before scored data;
- physical runs and joined logs/video exist;
- RP07-G01…G07 each has a recorded pass/iterate/reject result;
- ADR-09 is updated from cited evidence.

No wording in this folder converts documentation completion into prototype completion.
