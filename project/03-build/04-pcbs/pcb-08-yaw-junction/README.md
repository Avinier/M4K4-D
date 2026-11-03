# PCB-08 — Yaw junction

Stationary end of the clock spring: body-side power and signal connectors to the cassette FFCs (`J8-6`, `J8-7`).

**D-082 interface:** `J8-5` pin 8 is now `ARM_REQ` from C2, carried through the 22-pin W43 sideband FFC and PCB-14 to PCB-02 `J2-6` pin 8. It is a new active conductor, not a spare. Freeze its FFC pin and adjacent signal return at PCB-08/12 design; prove continuity and no cross-connection through both joiners and the yaw sweep before motor arming is allowed.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-083 in [BOM.csv](../../BOM.csv) |
| Location | Body, under the yaw adapter plate |
| Specification | [05-harness](../../05-harness/README.md)<br>[D-039](../../decisions.md#d-039), [D-044](../../decisions.md#d-044) |
| CAD placeholder | `_yaw_junction_board()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `YAW_JUNCTION_PCB08` |
| Final CAD | `Custom PCBs › PCB-08 yaw junction` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

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
