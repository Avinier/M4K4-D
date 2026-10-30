# PCB-04 — Branch converters

Five branch converters: C2, base, Pi, display and audio.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-043 in [BOM.csv](../../BOM.csv) |
| Location | Body, under the compute tray |
| Specification | [power-boards.md](../power-boards.md)<br>[RP-02 board-specs.md](../../../02-prototypes/RP-02-electrical/board-specs.md) (read-only reference) |
| CAD placeholder | `power_distribution_boards()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB04_BRANCH_CONVERTERS` |
| Final CAD | `Custom PCBs › PCB-04 branch converters` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Not started | — | — |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

- **Underside keep-out over the motor cables** ([D-072](../../decisions.md#d-072), 2026-10-30). The board's underside (Z 63.0) sits 0.5 mm above both motors' cable reserves, `MOTOR_[LR]_PIGTAIL_RESERVE` (X −21 to −1, \|Y\| 6–18, Z 56.5–62.5), where each encoder cable bends up out of its plug. No THT tails or bottom-side parts over those two areas (Micro-Fit THT tails stand 1.6 mm below a board), or raise the board.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.
