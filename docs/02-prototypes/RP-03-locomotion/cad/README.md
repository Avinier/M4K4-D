# RP-03 body and chassis CAD

This directory owns the integrated RP-03 whole-body CAD. The active model is
[`body-chassis/layout-02/`](body-chassis/layout-02/). It combines the frozen Concept A
locomotion layout and ball transfer with a structural chassis, serviceable body,
internal RP-02 packaging, harness reservations, physics overlays, and the actual
RP-01 Layout 03 head source.

The earlier [`base/pass-01/`](base/pass-01/) model is retained as historical envelope
work only. Its purple head lump, caster comparison, and open-SKU assumptions are not
the current architecture.

CAD-first choices that are not yet propagated into permanent RP-03 requirements are
recorded in [`decisions.md`](decisions.md).

## Active model

| Item | Current CAD state |
|---|---|
| Locomotion | Frozen Concept A: two powered wheels at 170 mm track plus a fixed, non-interchangeable front ball-transfer module |
| Head | Live import of RP-01 Layout 03 source; yaw datum at chassis `(0, 0, 140)` mm |
| Body/chassis | Independent bolted frame, fixed ball-transfer nose, connected rear skid, translucent 110 mm outer shell, matched trapezoidal service panels, and removable lower mobility fascia |
| Audio | Functional front grille over a provisional 50 mm speaker package; four body PDM microphone ports and amplifier envelope |
| Internal packaging | Compute, storage/cooling allowance, battery, motor drivers, power/safety, controller, IMU and sensor envelopes |
| Wiring | Main power/data trunks and service-loop keep-outs are selectable review geometry |
| Purchased CAD | Exact Raspberry Pi 5 and 608ZZ STEP articles; other articles remain explicitly labelled envelopes where no trustworthy STEP was found |
| Physics | Generated mass register, whole-robot CoM, contact/support overlay, axes, and deterministic geometry checks |
| Review | Clean exterior, shell-hidden internal, physics, and head-yaw views plus interactive CAD Viewer controls |
| Release state | Packaging-quality Layout 02; not fabrication release or structural certification |

Open the active model documentation at
[`body-chassis/layout-02/README.md`](body-chassis/layout-02/README.md). The buildable
source is [`body-chassis/layout-02/body-chassis.step.py`](body-chassis/layout-02/body-chassis.step.py).

## Authority and workflow

Inputs are consumed in this order:

1. frozen architectural decisions in [`../decision.md`](../decision.md);
2. SKU identities, procurement status, and source confidence in [`../research.md`](../research.md);
3. locomotion calculations and test cases in [`../physics.md`](../physics.md);
4. the RP-01 Layout 03 source and its yaw interface;
5. RP-02 electrical architecture, power branches, link contracts, and measured hardware;
6. manufacturer drawings or exact in-hand measurements;
7. clearly marked CAD envelopes where exact geometry is unavailable.

CAD changes are made and reviewed in this active layout first, following the same
pattern as RP-01 head Layout 03: centralized source parameters, generated dimensions
and mass properties, deterministic checks, and saved review views. After a value is
accepted, it is propagated to the affected Markdown specifications. A provisional CAD
value must not silently become a project-wide requirement.

Cosmetic reference images inform only the faceted body language, panel treatment,
colour split, and silhouette. They do not override the frozen architecture, package,
datums, contacts, or service clearances.

## Required closure before fabrication

- measure the exact custom wheel, hub, tread and motor articles;
- replace remaining motor, ball-transfer, battery, power-module, sensor-board and
  connector envelopes with vendor or measured geometry;
- close RP-02 connector orientation, bend-radius and demate-volume requirements;
- finish shell splits, fastening, tolerances, wall strategy and manufacturing process;
- weigh fabricated/custom items and regenerate mass, CoM and stability results;
- run interference, steering/yaw, service-removal, cable-strain and DfAM checks;
- obtain mechanical review for the chassis, head load path and impact cases.

The complete requirement and acceptance checklist is
[`body-chassis-plan.md`](body-chassis-plan.md).
