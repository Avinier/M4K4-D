# PCB-06 (×4) — PDM microphone board

One IM73D122 bottom-port PDM microphone per board; four boards form the array.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-005 in [BOM.csv](../../BOM.csv) |
| Location | Body shell bosses (front/rear, left/right) |
| Specification | [audiosystem.md §3](../../02-body/v1/research/audiosystem.md#3-pcb-06-mic-board--4), [§8](../../02-body/v1/research/audiosystem.md#8-speaker-cavity-and-mic-placement)<br>[D-037](../../decisions.md#d-037) |
| CAD placeholder | `_mic_board()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PDM_MIC_FRONT_L` … `PDM_MIC_REAR_R` |
| Final CAD | `Custom PCBs › PCB-06 PDM microphone boards x4` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

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
