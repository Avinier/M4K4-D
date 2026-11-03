# PCB-12 — C2 head carrier

Castellated carrier for the ESP32-S3-Zero (C2): head link and display transceivers, Feetech servo bus, TPS3436 watchdog.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-086 in [BOM.csv](../../BOM.csv) |
| Location | Head, C2 tray |
| Specification | [feetech-link-contract.md](../feetech-link-contract.md) |
| CAD placeholder | [`layout_model.py`](../../03-head/v1/cad/layout_model.py) (only the ESP32-S3-Zero module is drawn) |
| CAD labels | `C2_ESP32_S3_Zero_23_5x18_footprint` |
| Final CAD | `Custom PCBs › PCB-12 C2 head controller` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Not started | — | — |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

**Set by other boards.** The watchdog is **TPS3436CCCBGDDFRQ1** ([D-068](../../decisions.md#d-068), with PCB-10): the `BD-10` CFDBE part cannot be bought. Same pinout C and DDF footprint; tWC 5 ms, tWO 15 ms at `SET[1:0]` = 00 (feed every 10 ms, late fault ≤ 22 ms), 500 ms startup, 200 ms assert. Source: Mouser India.

**D-082 fresh-arm output.** Allocate a C2 GPIO and a physical default-low driver for `ARM_REQ`. It passes through W43, PCB-14 and PCB-08 to `J8-5.8`/PCB-02 `J2-6.8`. It must issue a new edge only after C2 has checked local READY, charge absence, pack state, and the operator's arm action; boot, watchdog reset, return of a fault or an open wire must not create an arm edge. Freeze the GPIO and the exact W43 conductor with PCB-08 before layout, and bench the full yaw-cassette path.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.
