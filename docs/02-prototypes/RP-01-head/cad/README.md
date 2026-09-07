# Makad CAD

This folder, `docs/02-prototypes/RP-01-head/cad/`, owns RP-01 CAD layout decisions, CAD-specific requirements and packaging notes. Current work is **head-layout preparation for RP-01**; integrated geometry, fit and actuator selection remain unvalidated. Creating this folder does not freeze CAD or start modeling.

## Start here

| Document | Purpose |
|---|---|
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
