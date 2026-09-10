# Makad CAD

This folder, `docs/02-prototypes/RP-01-head/cad/`, owns RP-01 CAD layout decisions, CAD-specific requirements and packaging notes. **Layout 03 is the current detailed 1:1 packaging revision**, built on Layout 02 and preserving it as history. It adds deeper helmet shoulders and a 104 mm wide tapered stern, a 3 mm camera/display gap, removable C2 tray with PCB keepers, camera PCB edge clamp, trial insert/bearing/coupling/stop details, and independent physics/harness/annotation groups. The crown is 104 mm (+2 mm); the provisional robot stack is 304 mm. Sampled geometry checks pass, but cable-flex transitions and remaining hardware-specific fits (display, servo, shaft) remain open; CAD is not frozen.

## Start here

| Document | Purpose |
|---|---|
| [Current Layout 03](head/layout-03/README.md) | Tapered head, service details, STEP, motion/optical checks, independent inspection groups and revised mass/A0 |
| [Layout 03 verification](head/layout-03/review/verification.md) | Final checks, service paths, snapshots and explicit remaining gaps |
| [Preserved Layout 02](head/layout-02/README.md) | Previous head layout and its original verification |
| [Layout 02 dimensions](head/layout-02/dimensions.md) | Generated bounding boxes, axis datums and yoke-length segments for the current model |
| [Layout 03 brief](head/layout-03-brief.md) | Builder direction implemented in Layout 03; hardware-specific limitations remain explicit |
| [Layout 01 study](head/layout-01/README.md) | Proposed crown, internal arrangement, A0 coordinates, STEP review and explicitly bounded validation |
| [Layout 02 exterior brief](head/layout-02-brief.md) | Approved inputs behind the current CAD revision |
| [Head decisions](head/decisions.md) | Agreed choices for the first layout, reasons, open decisions and conditions for revision |
| [Head CAD requirements](head/requirements.md) | Existing CAD-01…CAD-06 requirements, relocated here with their original IDs and authority preserved |
| [Head packaging estimates](head/packaging-estimates.md) | Component envelope references, the provisional roll depth stack and missing fit checks |
| [Head pre-layout brief](head/pre-layout-brief.md) | Existing mass/geometry evidence, servo references and a proposed internal arrangement before modeling |

New CAD-only Markdown belongs here. Keep future head layout files alongside these notes in `head/`, with their revision and evidence status stated. A concept layout is working evidence; integrated CAD freeze still follows the project's [engineering process](../../../intuition.md#8-cad-and-build-transcription-freeze-and-change-control).

## Source documents

These documents serve more than CAD and remain in their existing locations. Link to them rather than maintain a second dimensional baseline, mass ledger or prototype decision record.

| Subject | Source |
|---|---|
| Droid character, modularity and serviceability | [Vision](../../../00-foundation/vision.md), [constraints](../../../00-foundation/constraints.md), [success criteria](../../../00-foundation/success-criteria.md) |
| Dimensions and placement | [Dimensional baseline](../../../01-system/dimensional-baseline.md) |
| Mass ownership and evidence | [System mass ledger](../../../01-system/mass-envelope-ledger.md), [RP-01 mass capture](../payload-mass-capture.md) |
| Component candidates | [Sourcing matrix](../../../01-system/candidate-sourcing-matrix.md), [display study](../../../01-system/display-candidate-study.md), [camera study](../../../01-system/camera-candidate-study.md) |
| Materials and weathered finish | [RP-01 material/finish/mass decision](../material-finish-mass-decision.md) |
| Mechanism research and alternatives | [Servo mechanism recommendation](../concepts/servo-mechanism-recommendation.md), [Concept A](../concepts/elevated-ear-pivot-serial-gimbal.md), [comparison](../concepts/comparison.md) |
| Wiring and controller architecture | [Harness routing study](../../../01-system/head-harness-routing-study.md), [control topology](../../../01-system/control-topology-options.md) |
| Motion targets and mechanism acceptance | [Storyboard](../storyboard.md), [physics](../physics.md), [gates](../gates.md), [RP-01 decision](../decision.md) |

## Visual references

Use the [head concept](../../../../visuals/head/pass1.png), [parts illustration](../../../../visuals/head/pass1-parts.png), [mechanism perspective](../../../../visuals/mvp-after-head-servo-archv2-iteration-01-perspective-cutaway.png) and [side section](../../../../visuals/mvp-after-head-servo-archv2-iteration-02-side-section.png) for appearance and discussion. Their labels, proportions, ear attachment and clearances are not manufacturing specifications. Current choices come from the head decision register above.

The builder has now selected ears that move with the face. The older mechanism illustrations' “ear covers stay with yoke” labels are superseded; retain the illustrations as historical references, not current ear-attachment instructions.

## Organization record — 2026-09-07

No existing complete Markdown document was exclusively CAD-focused: the nearest matches also own system requirements, prototype evidence, material/finish decisions or sourcing research. Those documents remain linked above. The CAD-only requirements section was relocated from the material/finish/mass record to `head/requirements.md`; its former heading remains as a forwarding link. The discussion's layout decisions and estimates are now recorded here separately from final mechanism acceptance.

The builder clarified that this folder belongs inside RP-01 and moved it there from the repository root. Incoming links and this folder's source/visual references were updated to match. The root-level `cad/` remains reserved for later integrated CAD in the repository roadmap.
