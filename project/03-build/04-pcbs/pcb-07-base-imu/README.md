# PCB-07 — Base IMU

> **Superseded by [D-093](../../decisions.md#d-093) (2026-11-06).** Replaced by a bought SPI 6-axis IMU breakout at 3.3 V that matches PCB-10's `J10-7` pinout (+3V3, GND, SCLK, MOSI, MISO, CS, INT1, INT2), on a printed adapter on the existing J15A holes. Nothing here is built or ordered; the folder is kept as the record.

ICM-42688-P IMU for the base (HOLD: sensor and SPI vs I²C interface).

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-021 in [BOM.csv](../../BOM.csv) |
| Location | Chassis deck crossbar |
| Specification | [RP-06 peripheral-selection.md](../../../02-prototypes/RP-06-cad/peripheral-selection.md) |
| CAD placeholder | `imu_board()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `IMU_PCB07` |
| Final CAD | `Custom PCBs › PCB-07 base IMU` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Not started | — | — |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** superseded by [D-093](../../decisions.md#d-093) while on HOLD: bought SPI IMU breakout on `J10-7`, printed adapter on J15A.
