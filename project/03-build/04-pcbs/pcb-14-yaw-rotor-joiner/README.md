# PCB-14 (×3) — Yaw rotor joiner

Straight 1:1 22-pin 0.5 mm FFC joiner with two ZIFs, passing the cassette FFCs through the rotating yaw hub. Three boards use six ZIFs; PCB-08 uses two more of the same family (HOLD: full connector/cable fit).

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-062 in [BOM.csv](../../BOM.csv) |
| Location | Body, inside the rotating yaw hub |
| Specification | [02-body/v1/BOM.md](../../02-body/v1/BOM.md)<br>[D-052](../../decisions.md#d-052) |
| CAD placeholder | `_yaw_joiner_parts()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB14_JOINER_BOARD_1` … `_3` and their ZIFs |
| Final CAD | `Custom PCBs › PCB-14 yaw rotor joiners x3` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Inputs in progress | Shared PCB-08/14 FH34SRJ candidate; no KiCad revision yet | 2026-11-09 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

The D-052 envelope is **height out from the 0.8 mm board ≤ 2.0 mm; insertion depth along the board ≤ 5.2 mm**. FH12-22S-0.5SH(55) is 6.4 mm deep and fails. FH34SRJ-22S-0.5SH(99) is the active shared PCB-08/14 candidate: 13 mm long, 3.8 mm deep, 1.0 mm high, 0.3 ± 0.03 mm FFC/FPC and 0.5 A/contact. [Hirose part and specification](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Mouser India listing](https://www.mouser.in/en/ProductDetail/Hirose-Connector/FH34SRJ-22S-0.5SH99). Its body is smaller in all three dimensions than the existing 16 × 5.2 × 2.0 mm CAD reserve at the same centre; that passes only a bounding-box screen. Its actual pad/courtyard footprint, actuator-open access and both head/cassette cable exits must fit all three rotor positions. Keep the 1:1 pin numbering, verify the top/bottom contact-side and the physical mirroring of every cable, especially CSI.

The BO-050 CSI cable is described as a Pi 5 camera cable, but the usual official camera lead is 15-to-22 standard-mini. This joiner requires **22-to-22 mini-mini** on the cassette section. Raspberry Pi documents a mini-mini 200 mm product, but its end stiffener thickness and exact order code are not yet verified against FH34SRJ. Its published **standard-mini display** drawing gives 0.309 ± 0.05 mm at the 22-way end, a wider tolerance than FH34SRJ's 0.30 ± 0.03 mm acceptance; that drawing cannot qualify the different mini-mini cable. [Raspberry Pi mini-mini declaration](https://pip-assets.raspberrypi.com/categories/907-approvals/documents/RP-005161-CF/Mini_-_Mini_EU_DoC_Cam_Display); [standard-mini drawing](https://pip-assets.raspberrypi.com/categories/903-flexible-printed-circuit-fpc-cable-for-display-and-camera/documents/RP-008145-DS-1-mini-display-cable-200mm-reference-drawing.pdf); [official camera installation guidance](https://www.raspberrypi.com/documentation/accessories/camera-software.html).

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-09:** FH12 depth exceeds D-052's reserve. FH34SRJ is the shared eight-connector candidate; India listing found. Exact CSI mini-mini cable and real three-board actuator/cable fit remain open.
