# PCB-12 — C2 head carrier

Castellated carrier for the ESP32-S3-Zero (C2): head-link and display transceivers and the Feetech servo bus. No watchdog since [D-093](../../decisions.md#d-093).

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

**[D-093](../../decisions.md#d-093) scope (2026-11-06).** Minimal safety: **no TPS3436 watchdog, no `ARM_REQ` output, no `C2_READY_H/L` pair** (PCB-03 and its permit chain are gone). The bought Waveshare ESP32 Servo Driver was checked and **does not fit** the head's C2 bay: it is 65 × 30 mm against the 18 × 23.5 mm vertical board envelope, and it carries a plain ESP32, not the S3 ([D-094](../../decisions.md#d-094)). So this carrier is designed. A custom carrier keeps the servo bus half-duplex interface, the RS-422 head link (J9-1 order per D-092) and the display link.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): watchdog, `ARM_REQ` and READY pair dropped; Waveshare ESP32 Servo Driver fit check comes first.
- **2026-11-07:** [D-094](../../decisions.md#d-094): Waveshare board doesn't fit the C2 bay; this stays a simplified custom carrier.
