# RP-07 decision record

| Field | Value |
|---|---|
| Status | **Paper decisions proposed 2026-09-21. No gate registration or pass. ADR-09 open.** |
| Owner | Project builder |
| Created | 2026-09-21 |

## 1. Paper decisions

| ID | Decision | Paper answer | Status | Reopen condition |
|---|---|---|---|---|
| `BD-01` | Overall perception family | `PS-HYBRID-01` layered detector + temporal association + selected-target update/prediction + sparse appearance evidence | **PROPOSED** | Replay benchmark cannot meet continuity/latency |
| `BD-02` | Primary evidence | Whole-person detection; face/landmarks are associated auxiliary evidence | **PROPOSED** | Person detector fails the registered geometry matrix |
| `BD-03` | Identity policy | Short-session selected-target continuity only; no named/biometric identity | **PROPOSED** | Core scope changes |
| `BD-04` | Selection owner | `makad-core`; perception proposes candidates and never authorizes locomotion | **PROPOSED** | Compute architecture changes |
| `BD-05` | No-silent-switch | Selected target is pinned; ambiguity/loss stops; replacement requires explicit new selection | **PROPOSED** | Never relaxed by tuning |
| `BD-06` | Range strategy | Ground-plane/visible-joint geometry when observable; selected-person apparent-width/scale fallback; uncertainty always published | **PROPOSED** | Physical range error cannot support control |
| `BD-07` | Loss motion | Base brakes on loss; V1 reacquisition occurs stationary | **PROPOSED** | A later separately scored policy proves moving reacquisition safe |
| `BD-08` | Counter-yaw closure proposal | Core authorizes base turn; C3 owns base motion/yaw; `makad-hwd` relays timestamped yaw/rate to C2; C2 owns counter-yaw/recentering execution | **PROPOSED; must also close RP-04 BD-08** | Measured relay/jitter or C2 interface fails |
| `BD-09` | Compute placement | All perception on Pi 5 2 GB initially; active cooler; accelerator only after measured failure | **PROPOSED** | Representative workload misses compute gates |
| `BD-10` | Middleware | Existing UDS + packed MCU links; no ROS 2 in V1 safety/control path | **INHERITED** | `CA-07` change control |
| `BD-11` | Physical authority ladder | Replay → live/no motion → head only → guarded low-speed → come → follow → adverse/fault | **PROPOSED** | Never bypassed for schedule |

## 2. Implementation candidates still to select by replay

| Function | Lead | Required comparison | Selection evidence |
|---|---|---|---|
| Person detector | Nano-class detector in NCNN at measured resolution | MobileNet-SSD/TFLite or equivalent low-cost baseline | Recall/false positives, P95 latency, memory, heat, small-person performance |
| Multi-person association | ByteTrack-like confidence-aware association | Appearance-assisted alternative | ID switches and fragmentation on Makad corpus |
| Selected-target fast update | Kinematic prediction plus lightweight image-space update | Detector-only publication and one lightweight SOT/optical-flow candidate | Drift, failure indication, update rate, CPU |
| Appearance descriptor | Mobile/edge person descriptor run sparsely | Handcrafted colour/shape baseline and no-appearance baseline | Distractor/re-entry accuracy, compute, storage/privacy |
| Face/landmark backend | Lightweight face detector/landmarks when face pixels permit | Body-anchor fallback | Anchor accuracy and incremental load |

Names above are experiment families, not frozen libraries or licenses. Exact repository, model revision, weights hash, input resolution, runtime, quantization, and license must be recorded before implementation freeze.

## 3. Registration ladder

| Registration | Content | Current state |
|---|---|---|
| `RP07-P1-REG-01` | Intent, inherited map, architecture and interfaces | **DRAFT** |
| `RP07-P2-REG-01` | Geometry, calibration, timing semantics | **DRAFT** |
| `RP07-P3-REG-01` | Continuity and behaviour/control policies | **DRAFT** |
| `RP07-P4-REG-01` | Safety/fault matrix and compute acceptance | **DRAFT** |
| `RP07-P5-REG-01` | Test matrix and evidence layout | **DRAFT** |
| `RP07-P6-REG-01` | Numeric RP07-G01…G07 thresholds frozen before scored runs | **EMPTY** |

The user request to prepare documentation authorizes the paper package. It does not convert proposed technical choices into builder-approved registrations or measured decisions.

## 4. ADR-09 ladder

ADR-09 remains open until:

1. a model/runtime/configuration wins replay and live-no-motion comparison;
2. calibrated geometry meets bearing/range needs;
3. target selection and distractor cases demonstrate zero silent switches;
4. Pi coexistence meets latency/memory/thermal limits;
5. guarded come/follow and fault campaigns pass;
6. all conclusion rows cite immutable evidence manifests.

