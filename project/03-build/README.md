# 03 — Build

Turn the [prototype decisions](../02-prototypes/) into parts that can be printed, assembled, measured, and revised. This phase is complete when the built robot passes its integration tests, not when the CAD looks finished.

## Status (2026-11-12)

The build follows the [D-093](decisions.md#d-093) simplification: bought power modules replace the charger, motor-gate, converter, audio, mic and IMU boards. Progress by level is in the [simplification plan §7](simplification-plan.md#7-levels-of-work).

- **Modules** selected ([D-094](decisions.md#d-094), [module-selection.md](module-selection.md)) and **ordered 2026-11-08**; each still has a bench gate (N1–N12).
- **Droid CAD** for the modules, ports and mounts is done ([D-095](decisions.md#d-095)); the chassis front module and the D-095 mount prints are re-exported to [04-print](../04-print/01-chassis/README.md) ([D-099](decisions.md#d-099)).
- **Harness** topology is documented, but [05-harness](05-harness/README.md) is on **electrical HOLD** ([D-096](decisions.md#d-096)): the ~16 A low-pack coincident load exceeds the contact and shunt allowances. Do not cut wire or build the charge/power path yet.
- **Custom boards** ([04-pcbs](04-pcbs/README.md)): PCB-09 rev B routed; PCB-08, PCB-12, PCB-14 and PCB-16 are rev A drafts (do not order). The head wiring route is set by [D-104](decisions.md#d-104) (hollow −Y trunnion) and [D-105](decisions.md#d-105) (camera ribbon loop).
- **BOM**: [BOM.csv](BOM.csv) is reconciled to D-093–D-097; the subsystem BOM snapshots still predate D-093.

## Where things are

| Record | Holds |
|---|---|
| [decisions.md](decisions.md) | The ledger: every decision, part selection, BOM change and CAD edit |
| [BOM.csv](BOM.csv) | The single parts register |
| [BOM-deliveries.md](BOM-deliveries.md) | What has physically arrived, mapped to BOM rows, with problems found |
| [TODO.md](TODO.md) | Open ordering, receiving and release actions |
| [simplification-plan.md](simplification-plan.md) | The D-093 change map, levels of work and bench register (N-tests) |
| [module-selection.md](module-selection.md) | Bought modules (M1–M13) and their acceptance gates |
| [01-chassis](01-chassis/), [02-body](02-body/), [03-head](03-head/) | Subsystem specs, BOM snapshots and subsystem-only CAD |
| [04-pcbs](04-pcbs/README.md) | Custom board register, design workflow and playbook |
| [04-software](04-software/firmware-requirements.md) | Firmware requirements (low-battery stop, button-off, servo limits, mics) |
| [05-harness](05-harness/README.md) | Connectors, cables, pinouts and service breaks |
| [final/v1](final/v1/README.md) | The whole-robot CAD and its checks, plus the [print guide](final/v1/printguide.md) |

Printing (lab, workflow, coupons, per-part print settings) is in [04-print](../04-print/README.md).

## Governing context

**From 2026-09-28, `03-build/` governs.** Record every new decision, part selection, BOM change and CAD edit here, in the subsystem and version folder it belongs to, and log it in [`decisions.md`](decisions.md).

[`02-prototypes/`](../02-prototypes/) and its RP folders, including RP-03 locomotion and RP-06 CAD, are **read-only reference**. Link to them for earlier research, gates and evidence; do not add decisions to them or edit their CAD. Where an RP document disagrees with `03-build/`, `03-build/` wins.

Each subsystem's `cad/` holds only that subsystem. The whole robot is in [`final/v1/cad/`](final/v1/README.md), and droid-level changes (envelope fixes, cuts, bought-part STEPs) go there with a targeted check.

## BOM conventions

[BOM.csv](BOM.csv) is the single parts register. Subsystem `BOM.md` files are dated working snapshots, not fabrication releases; refresh them deliberately after a BOM change.

In the register, `DESIGN` means custom geometry exists, `CANDIDATE` means a part or family is proposed, `SELECTED` means the build choice is settled with receiving and physical verification still separate, `OPEN` means the design needs a choice before release, and `HOLD` means do not order or fabricate until its blocker is resolved. `SUPERSEDED` rows are kept for history. `supplier_candidate` is a lead to verify, not a stock claim. Update `procurement` and `received_measurements` with order and caliper evidence; do not infer receipt from CAD or an old availability check.

## Build order

1. [Chassis and locomotion](01-chassis/): wheels, drive, supports and the body mounting interface. Test with representative body and head mass and centre of mass.
2. [Body](02-body/): load-bearing frame, packaging, power and wiring, access, cooling and the head support. Recheck its effect on the chassis.
3. [Head](03-head/): build and test the mechanism on its real body support. Part selection and isolated joint tests can start earlier.
4. [Full droid](final/v1/README.md): assemble the subsystems and rerun whole-robot motion, power, thermal, fault and interaction tests.

Work can overlap. Freeze only the interfaces needed for the next release, and record changes that affect another subsystem. Unreleased custom boards do not block isolated chassis fit or controlled external-supply tests.

## What a version means

`v1`, `v2`, `v3`, and later folders are **build iterations**. Each version aims to produce a **print-ready build release** for its defined scope, followed by a physical build and test. A version is not called production-ready before its printed article passes its tests.

Each release needs only these records:

1. **Scope and interfaces** — parts included, assumed loads and mass, dimensions that other subsystems depend on, and known exclusions.
2. **BOM and procurement** — exact purchased parts, quantities, sources, status, and measured dimensions. Keep one project BOM; capture the version's exact BOM as a release snapshot so subsystem lists cannot silently diverge.
3. **Fabrication package** — source CAD and revision, printable exports, material, printer/process settings, orientation, supports, tolerances, inserts, and assembly instructions. Measure received hardware and correct dependent CAD before releasing custom parts.
4. **Test plan and evidence** — focused stress-test research, expected loads, measurable pass/fail criteria set before scored tests, test setup, results, photos/logs, and failures. Mark unrun tests **OPEN**, not passed.
5. **Exit decision** — `PASS`, `ITERATE`, or `HOLD`, with the evidence and the specific change needed. A failed or improved design becomes the next version; a passing subsystem can move forward while its shared interfaces remain tracked.

For the chassis, test at least fit and retention, loaded stiffness, wheel runout, traction and turning, braking and tipping, support/skid behaviour, motor temperature, and service access. Use representative worst-case body/head ballast until those assemblies exist. Reuse the [RP-03 locomotion gates](../02-prototypes/RP-03-locomotion/gates.md) and [RP-06 open items](../02-prototypes/RP-06-cad/TODO.md) as inputs; register relevant numeric limits and test conditions before scoring a run.

The working loop is **select → order → measure → update CAD → release → print/assemble → test → record → iterate or lock**. `LOCKED` means the built article passed its defined tests and its interfaces are controlled. A CAD check or paper calculation alone does not lock a part.

## Documentation rule

Keep these pages shorter and more decisive than [02-prototypes](../02-prototypes/). Link to existing research instead of copying it. State the current decision, revision, evidence, open risk, and next action; remove abandoned options from the active build instructions. Do not call estimates measurements or let a later CAD edit silently change a released version.
