# Makad Memory

A short chronological log of the project's turning points: changes of method,
authority or architecture that a newcomer needs in order to read the rest of the
repository. Detailed decisions belong in
[`project/03-build/decisions.md`](project/03-build/decisions.md); add an entry
here only when the way the project works changes.

Earlier logs are kept unchanged in [`archive/`](archive/).

## 2026-09-21: Development-method reset

`00-foundation` remains the product-intent authority. `01-system` and
`02-prototypes` become engineering reference. Design, sourcing, CAD, software
and hardware proceed together.

## 2026-09-28: `03-build` governs

All new decisions, part selections, BOM changes and CAD edits go in `03-build`,
logged in its `decisions.md` ledger with `BOM.csv` as the single parts register
([D-001](project/03-build/decisions.md#d-001)). The RP folders in
`02-prototypes` are read-only from here on.

## 2026-10-07: Feetech head actuators

The Dynamixel XC330 plan is replaced by Feetech bus servos: ST3215-HS on yaw and
STS3045M on pitch and roll ([D-046](project/03-build/decisions.md#d-046)–[D-049](project/03-build/decisions.md#d-049)).
The head and yaw stage were redesigned around them.

## 2026-10-14: Droid CAD edits only in `final/v1`

Subsystem `cad/` folders hold only their own parts. Every whole-robot change
(envelope fixes, cuts, bought-part STEPs, print fixes) is made in
`03-build/final/v1/cad/makad-v1.step.py` with its own targeted check.

## 2026-10-28: `docs/` renamed to `project/`; `04-print` added

All `docs/…` paths became `project/…`. `project/04-print` owns printing (lab,
workflow, coupons, STL exports) and never edits geometry.

## 2026-11-06: D-093 simplification

The custom charger, motor-gate, converter, audio, mic and IMU boards are replaced
by bought modules, with minimal safety and off-board charging
([D-093](project/03-build/decisions.md#d-093)). Modules were selected, placed in
CAD and entered in the BOM on 2026-11-07 (D-094–D-097); the harness went on
electrical HOLD (D-096). The custom boards left are PCB-08, 09, 10, 11,
12, 14 and 15, plus PCB-16 added by D-103.

## 2026-11-12: First deliveries

The first orders arrived (Pi 5, gearmotors, fasteners and others), recorded in
[`BOM-deliveries.md`](project/03-build/BOM-deliveries.md). The project moves from
CAD into receiving, measuring and bench testing.
