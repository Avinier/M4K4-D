# PCB-02 — Charger, latch and pack sense

BQ25798 2S charger, on/off latch, pack sense, `ENERGY_OK` and the power-button input `J2-9`.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-041 in [BOM.csv](../../BOM.csv) |
| Location | Body, behind the rear panel (vertical) |
| Specification | [charge-path.md §4](../charge-path.md#4-pcb-02--charger-block)<br>[power-boards.md §6](../power-boards.md#6-pcb-02-power-button-input-d-041)<br>[RP-02 board-specs.md](../../../02-prototypes/RP-02-electrical/board-specs.md) (read-only reference)<br>[open items](../open-items.md) CP-OI-02, CP-OI-09, CP-OI-15<br>[D-040](../../decisions.md#d-040), [D-041](../../decisions.md#d-041) |
| CAD placeholder | `power_distribution_boards()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB02_CHARGE_AND_SYSTEM_POWER` |
| Final CAD | `Custom PCBs › PCB-02 charger, latch and pack sense` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

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
