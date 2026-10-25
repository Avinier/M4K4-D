# PCB-13 — Charge inlet

USB-C inlet: GCT USB4140, STUSB4500 PD sink, TVS2200/ESDA25W protection and the input P-FET.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-015 in [BOM.csv](../../BOM.csv) |
| Location | Body, rear-panel pad (comes off with the panel) |
| Specification | [charge-path.md §3](../charge-path.md#3-pcb-13--charge-inlet-board), [§6](../charge-path.md#6-the-inlet-on-the-panel), [§8](../charge-path.md#8-stusb4500-nvm-image)<br>[open items](../open-items.md) CP-OI-01, CP-OI-03 to CP-OI-05<br>[D-040](../../decisions.md#d-040) |
| CAD placeholder | `charge_inlet_pcb13()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `CHARGE_INLET_PCB13` |
| Final CAD | `Custom PCBs › PCB-13 charge inlet` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

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
