# PCB-03 — Motor gate and head 5 V rail

Motor gate, permit chain (0 Ω link, no E-stop loop), head 5 V rail and the DRV8833 drive feeds.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-042 in [BOM.csv](../../BOM.csv) |
| Location | Body, above the tub |
| Specification | [power-boards.md §2](../power-boards.md#2-pcb-03-drive-feed-for-the-drv8833) and [§4A](../power-boards.md#4a-feetech-actuator-rail-delta-d-046d-047-2026-10-07)<br>[RP-02 board-specs.md](../../../02-prototypes/RP-02-electrical/board-specs.md) (read-only reference)<br>[D-041](../../decisions.md#d-041) |
| CAD placeholder | `power_distribution_boards()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB03_MOTOR_GATE_AND_HEAD_RAIL` |
| Final CAD | `Custom PCBs › PCB-03 motor gate and head 5 V rail` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Not started | — | — |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

### Cross-board `ENERGY_OK` receiver requirement

PCB-03 must include a physical pull-down at the `ENERGY_OK` receiver so an open signal wire or a collapsed `+5V_C2` pull-up leaves the motor-permit chain inactive. Size it during PCB-03 design against PCB-02's pull-up, receiver threshold/leakage, harness leakage, and the asserted-high margin; do not rely on MCU internal pulls. Verify the receiver low state with the signal wire open and `+5V_C2` absent. This pull-down alone does **not** protect against PCB-02 comparator power loss while `+5V_C2` remains present; PCB-02 must resolve that failure path before its schematic is released.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.
