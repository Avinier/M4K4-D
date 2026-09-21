# RP-07 construction and evidence plan

| Field | Value |
|---|---|
| Status | Documentation plan complete; execution not started |
| Sequence rule | Increasing authority; a later phase cannot compensate for a missing earlier prerequisite |

## Part 1 — paper baseline

Deliverables:

- intent/inherited/decision records;
- perception and interface architecture;
- geometry/calibration plan;
- continuity and controller policies;
- safety/fault and compute plans;
- test matrix, gate sheets and evidence layout.

Exit: internal consistency review and builder acceptance of `BD-01…11`; register `RP07-P1…P5` as appropriate. This part is documentation only.

## Part 2 — corpus and replay harness

1. Define recording consent/retention and run manifest.
2. Calibrate the camera modes used for collection.
3. Record the factor matrix with motors inhibited.
4. Label people, visibility, anchors, range marks, occlusion and selection truth.
5. Build deterministic replay from frames + metadata + recorded head/base state.
6. Implement metrics before comparing candidates.

Exit: corpus/version hash and replay reproducibility report. Physical recording is mentioned here and remains unexecuted.

## Part 3 — perception bake-off

1. Implement replaceable detector/tracker/appearance backends.
2. Compare candidates on identical recordings.
3. Select by preregistered accuracy/continuity/latency/resource rule.
4. Freeze model/runtime/config hashes for live testing.
5. Record license and redistribution disposition.

Exit: implementation selection candidate for ADR-09; not yet validated for motion.

## Part 4 — live camera and geometry

1. Complete `CAL-01…07` as applicable.
2. Run Phase B with all motors inhibited.
3. Run compute coexistence and sustained thermal workload.
4. Characterize source timestamp, exposure/readout, motion timing and frame drops.
5. Revise uncertainty and validated operating envelope from measured data.

Exit: live observation contract demonstrated or iterate/reject.

## Part 5 — head-only attention

Prerequisites: RP-01 safe head operation, current calibration and valid timebase.

Run Phase C search, acquisition, tracking, face/body anchor, slew and counter-yaw-fixture cases. Close or revise the RP-04 `BD-08` proposal from timing evidence.

Exit: head attention works without base authority.

## Part 6 — guarded base precursor

Prerequisites:

- applicable RP-03 safety gates pass;
- workbench/floor readiness and E-stop verified;
- stopping/speed/CoM/config limits registered;
- C3 local sensors and expiry active;
- gates frozen for this phase.

Run surrogate target and alignment at minimum speed before a person stands in the approach path.

Exit: person-derived goals and C3 safety interaction are bounded.

## Part 7 — come

Execute `T07-E*` in increasing distance/angle/authority. Iterate controller and geometry using pilot-labelled runs. Freeze a fresh gate revision before the scored campaign.

Exit: `RP07-G03` outcome with complete evidence; no automatic promotion to follow.

## Part 8 — follow and adverse cases

Execute straight route, gentle turn, stop, occlusion, exit/re-entry, distractor and obstacle cases. Finish with safe applicable fault injections.

Exit: G02/G04/G05/G06 outcomes.

## Part 9 — scored closure

1. Confirm all gate sheets and revisions are frozen.
2. Run the scored matrix without tuning on its scored set.
3. Audit manifests, timing joins and deviations under G07.
4. Record gate outcomes as pass/iterate/reject.
5. Update ADR-09 and affected timing, power, thermal and architecture documents.
6. Preserve failed runs and anomalous observations.

## Dependency blockers

| Work | May proceed now on paper/replay | Physical blocker |
|---|---|---|
| Interfaces, replay, detector comparison | Yes | Selected camera/Pi needed for final performance |
| Live no-motion perception | Yes after hardware available | Camera/harness and calibration |
| Head-only tracking | No physical claim yet | RP-01 safe measured head |
| Base alignment/come/follow | No | RP-03 gates, C3 hardware/sensors, floor rig |
| Counter-yaw closure | Paper proposal now | C2/C3 state relay and measured timing |
| ADR-09 closure | No | All relevant RP07 gates |

## Documentation change control

- Semantic changes update `decision.md` with date/status/consequence.
- Registered IDs are append-only.
- A model/config/calibration/rig change creates a new run configuration.
- Physical results go in `evidence/`; they do not overwrite the test plan that preceded them.
- Unknown values remain `U`; absence of a measured fault is not proof of zero risk.

