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
| 1. Design | Inputs in progress | PCB-08/12 sideband reference and provisional rail map recorded; no KiCad revision | 2026-11-09 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Fill this in when design starts: spec sources, pinout, supply and protection, CAD envelope.

**[D-093](../../decisions.md#d-093) scope (2026-11-06).** Minimal safety: **no TPS3436 watchdog, no `ARM_REQ` output, no `C2_READY_H/L` pair** (PCB-03 and its permit chain are gone). The bought Waveshare ESP32 Servo Driver was checked and **does not fit** the head's C2 bay: it is 65 × 30 mm against the 18 × 23.5 mm vertical board envelope, and it carries a plain ESP32, not the S3 ([D-094](../../decisions.md#d-094)). So this carrier is designed. A custom carrier keeps the servo bus half-duplex interface, the RS-422 head link (J9-1 order per D-092) and the display link.

**Shared PCB-08/12 interface input (2026-11-09; not yet a schematic).** PCB-08 proposes W43/J8-7 pins 1/4/7/9 as the `J8-4` pin-1 C0 link GND reference; 2/3 `C0TX+/−`; 5/6 `C2TX−/+`; 8 `SERVO_DATA`. Its separate `J8-1` head, C2 and display returns are not shorted on PCB-08. The provisional head-rail drop fix uses W43 pins 10–15 as `GND_HEAD` and 16–21 as `+5V5_HEAD_PR`, with 22 isolated, in addition to W42's 7+7 head conductors; M2 would move from 5.5 to 6.0 V only after the cable and N2 checks. PCB-12 must bond the W43 reference to its logic GND near the RS-422/servo interface or explicitly redesign the common-mode reference. Since the supplies meet upstream at a star, the proposed bond can carry unwanted parallel return current; measure that current and the C0↔C2 common-mode voltage under load. Preserve all names, polarities and pin numbering across PCB-14's 1:1 joiner. [PCB-08 input and drop screen](../pcb-08-yaw-junction/README.md#design-inputs-2026-11-09-preliminary).

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): watchdog, `ARM_REQ` and READY pair dropped; Waveshare ESP32 Servo Driver fit check comes first.
- **2026-11-07:** [D-094](../../decisions.md#d-094): Waveshare board doesn't fit the C2 bay; this stays a simplified custom carrier.
- **2026-11-09:** PCB-08/12 W43 candidate interface and return-current measurement gate recorded before either schematic is frozen.
