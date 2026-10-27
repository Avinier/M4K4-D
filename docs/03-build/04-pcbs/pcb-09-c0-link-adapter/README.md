# PCB-09 — C0 link adapter

Pi-header board: 2 × RS-422 (THVD1451), audio pass-through and the enclosure-fan switch `J9-4`.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-084 in [BOM.csv](../../BOM.csv) |
| Location | Body, on the Pi header |
| Specification | [audiosystem.md §4](../../02-body/v1/research/audiosystem.md#4-audio-functions-on-the-shared-boards)<br>[D-042](../../decisions.md#d-042) |
| CAD placeholder | `_c0_link_adapter()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `C0_LINK_ADAPTER_PCB09` |
| Final CAD | `Custom PCBs › PCB-09 C0 link adapter` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Not started | — | — |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

**Set by PCB-05.** `J9-3` (audio, `W26` to PCB-05 `J5-1`) carries signals only: GPIO18 BCLK, GPIO19 LRCLK, GPIO20 SDI0, GPIO22 SDI1, GPIO21 SDO0, GPIO23 `AMP_SD`, the Pi's 3V3, two GND and one spare, and **no 5 V** ([D-067](../../decisions.md#d-067), PCB-05 2026-10-27; `CA-06` CR-01 accepted there). Pin order, set by the PCB-05 schematic (2026-10-27): **1 3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 spare (5V_SENSE)** (reordered 2026-10-27 at PCB-05 routing, D-067); W26 is wired 1:1. Route the spare pin to a test pad: PCB-05 carries an unfitted 5V-present divider on it, which a later `CA-06` change could bring to a Pi GPIO.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.
