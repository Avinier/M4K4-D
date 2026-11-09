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

**Shared PCB-08/12 interface input ([D-100](../../decisions.md#d-100), 2026-11-09; not yet a schematic).** W43/`J8-7` is **signal-only**: pins 1/4/7/9 `GND_SIG`, 2/3 `C0TX+/−`, 5/6 `C2TX−/+`, 8 `SERVO_DATA`, 10–22 isolated. On PCB-08, `GND_SIG` joins the C0 link GND (`J8-4` pin 1) and the yaw servo ground (`J8-8` pin 1 / W17), so `SERVO_DATA` has its return beside it. W42/`J8-6` carries the head pitch/roll rail (now **6.3 V**, M2 per D-100 amendment) on 7 + 7 conductors and the C2 and display pairs on 2 + 2 each; those returns arrive as separate named nets. **PCB-12 must bond `GND_SIG` to its C2 logic ground near the RS-422 receiver and the servo-bus driver**, where all head grounds join. The resulting ground loop through W17, W24 and the star is accepted; measure W24 GND current at yaw stall and the C0↔C2 common-mode voltage under load. The 13/13 map (W43 10–21 as head power) is D-100's fallback only. Preserve all names, polarities and pin numbering across PCB-14's 1:1 joiner. [PCB-08 inputs](../pcb-08-yaw-junction/README.md#design-inputs-2026-11-09-preliminary).

**Head FFC orientation from PCB-14 ([D-101](../../decisions.md#d-101), 2026-11-10).** PCB-14 is a straight-through joiner: each conductor keeps its X, so the three head FFCs continue the cassette FFCs conductor for conductor. Conductor *n* of a head FFC is conductor *n* of its cassette FFC, which is contact *n* of `J8-6`/`J8-7` at PCB-08. Each head FFC leaves PCB-14's upper ZIF with **conductor 1 on its −X edge** (upper contact 22). Lying flat in the disc channel and travelling +Y at yaw 0, conductor 1 is on the −X side. Follow that edge through the still-unrouted riser up the +Y leg to set the contact-1 end of PCB-12's receiving ZIFs; dual contacts do not undo a mirror. The CSI head run is a Raspberry Pi standard-mini cable, not part of PCB-12, and goes into PCB-14 with its pin-1 conductor at −X.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): watchdog, `ARM_REQ` and READY pair dropped; Waveshare ESP32 Servo Driver fit check comes first.
- **2026-11-07:** [D-094](../../decisions.md#d-094): Waveshare board doesn't fit the C2 bay; this stays a simplified custom carrier.
- **2026-11-09:** PCB-08/12 W43 candidate interface and return-current measurement gate recorded before either schematic is frozen.
- **2026-11-09:** interface updated for D-100: J8-7 signal-only with `GND_SIG` (C0 link GND + yaw servo ground on PCB-08); bond to C2 logic ground here; head rail 6.3 V after the routed-board amendment.
- **2026-11-10:** PCB-14 rev A ([D-101](../../decisions.md#d-101)): head FFC conductor 1 arrives on the −X edge (straight-through joiner); recorded as an input.
