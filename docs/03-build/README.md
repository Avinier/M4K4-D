# 03 — Build

Turn the [prototype decisions](../02-prototypes/) into parts that can be printed, assembled, measured, and revised. This phase is complete when the built robot passes its integration tests, not when the CAD looks finished.

## Governing context

**From 2026-09-28, `03-build/` governs.** Record every new decision, part selection, BOM change, and CAD edit here, in the subsystem and version folder it belongs to. For example, chassis CAD belongs in [`01-chassis/v1/cad/`](01-chassis/v1/cad/) and chassis part choices belong in [`01-chassis/v1/`](01-chassis/v1/) and [`BOM.csv`](BOM.csv). Log every such decision or change as an entry in the central ledger, [`decisions.md`](decisions.md).

[`02-prototypes/`](../02-prototypes/) and its RP folders, including RP-03 locomotion and RP-06 CAD, are **read-only reference**. Link to them for earlier research, gates, and evidence. Do not add decisions to them or edit their CAD. Where an RP document disagrees with `03-build/`, `03-build/` wins.

Before detailing chassis v1, check and freeze the whole-robot spatial baseline: envelopes, datums, key clearances, mass/centre-of-mass assumptions, and subsystem interfaces. Fabrication details remain revisable.

The [project BOM](BOM.csv) is the single parts register. The [chassis v1 BOM](01-chassis/v1/BOM.md) is its dated working snapshot for one chassis; it is not yet a fabrication release.

In the register, `DESIGN` means custom geometry exists, `CANDIDATE` means a part or family is proposed, `SELECTED` means the build choice is settled with receiving and physical verification still separate, `OPEN` means the design needs a choice before release, and `HOLD` means do not order or fabricate until its blocker is resolved. `supplier_candidate` is a lead to verify, not a stock claim. Update `procurement` and `received_measurements` with order and caliper evidence; do not infer receipt from CAD or an old availability check. Refresh a version snapshot deliberately after a BOM change.

## Build order

1. [Chassis and locomotion](01-chassis/) — wheels, drive, supports, and the body mounting interface. Test it with representative body and head mass and centre of mass.
2. [Body](02-body/) — load-bearing frame, packaging, power and wiring, access, cooling, and the head support. Recheck its effect on the chassis.
3. [Head](03-head/) — build and test the mechanism on its real body support. Part selection and isolated joint tests can start earlier.
4. [Full droid](fulldroid/) — assemble the subsystems and rerun whole-robot motion, power, thermal, fault, and interaction tests.

Custom schematic, layout and board validation work has a separate [04-pcbs work area](04-pcbs/README.md), which also holds the build deltas to the RP-02 power-board specs. Its unreleased assemblies do not universally block isolated chassis fit or controlled external-supply tests.

Work can overlap. Freeze only the interfaces needed for the next release; record changes that affect another subsystem. The integrated [Layout 02 CAD](../02-prototypes/RP-06-cad/body-chassis/layout-02/) is the starting geometry, not a fabrication release or physical proof.

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
