# 04 — PCBs

This folder holds the schematic, layout, fabrication and electrical-validation work for the robot's custom boards. It is a work area, not a fabrication release. Part records stay in the [project BOM](../BOM.csv); every selection and change goes in the [build decisions](../decisions.md). It replaces the former `04-custom-pcb/` folder ([D-038](../decisions.md#d-038)).

## Board register

| ID | Board | Location | BOM | Status | Work still required |
|---|---|---|---|---|---|
| PCB-01 | 2S pack protection | Chassis tub, on the pack | CH-023 | **Bought:** Robocraze TIFPS0629 ([D-019](../decisions.md#d-019)); the RP-02 custom design is reference only | Bench acceptance before cells: [power-boards.md §3](power-boards.md#3-pcb-01--tifps0629-acceptance-before-cells-are-connected) |
| PCB-02 | Charger (BQ25798), on/off latch, pack sense, `ENERGY_OK` | Body, behind the rear panel (vertical) | CH-041 | Spec; charger block closed in [charge-path.md](charge-path.md) ([D-040](../decisions.md#d-040)); power-button input `J2-9` and the press → `SYSTEM_ARM` reset in [power-boards.md §6](power-boards.md#6-pcb-02-power-button-input-d-041) ([D-041](../decisions.md#d-041)) | Schematic; latch tests; power-button bench PB-01 to PB-06; charge bench CP-04 to CP-12; mounting (none in CAD yet) |
| PCB-03 | Motor gate, permit chain, head 5 V rail, drive feeds | Body, above the tub | CH-042 | Spec, with [build deltas](power-boards.md#2-pcb-03-drive-feed-for-the-drv8833); no E-stop loop: `J3-7` deleted, 0 Ω link in the permit chain (D-041) | Schematic; truth table, fault, inrush, regeneration tests |
| PCB-04 | Five branch converters (C2, base, Pi, display, audio) | Body, under the compute tray | CH-043 | Spec | Schematic; start-up, hold-up, breaker and back-feed tests |
| PCB-05 | Audio front end (MAX98357A, 2 × ADAU7002) | Body, above the Pi | BO-002 | Spec | Schematic and layout |
| PCB-06 ×4 | PDM microphone board | Body shell bosses | BO-005 | Spec | Layout; array tap and noise tests |
| PCB-07 | Base IMU (ICM-42688-P) | Chassis | CH-021 | HOLD | Sensor and SPI vs I²C interface |
| PCB-08 | Yaw junction (clock-spring stationary end) | Body, under the yaw adapter plate | CH-083 | Spec | Schematic; clock-spring flex pin order. Body-side pinout and the mating rule: [05-harness](../05-harness/README.md) (D-039) |
| PCB-09 | C0 link adapter (2 × RS-422, audio pass-through, enclosure-fan switch `J9-4`) | Body, on the Pi header | CH-084 | Spec; fan switch added ([D-042](../decisions.md#d-042)): Pi GPIO24 → logic-level N-MOSFET low side, XH2.54-2P `J9-4` | Schematic; bench fit beside the yaw servo; GPIO24 needs a `CA-06` change request (CR-02) |
| PCB-10 | C3 controller carrier (watchdog, READY, sleep gate, Hall and TCRT circuits) | Body, −Y side wall | CH-044 | Spec | J10-8 Hall and J10-10 TCRT changes; [J10-5/6 driver mapping](power-boards.md#24-logic-to-c3-j10-5--j10-6-gh-6) |
| PCB-11 | Status LED carrier (WS2812B-2020) | Head crown | CH-085 | Spec | Brightness and stray-light bench |
| PCB-12 | C2 head carrier (ESP32-S3-Zero, transceivers, TPS3436 watchdog) | Head | CH-086 | Lead design | Schematic; head pocket fit |
| CH-064 | Nose Hall carrier (DRV5055) | Chassis nose | CH-064 | Spec | Layout of the 6 × 4.6 × 0.8 mm board |
| PCB-13 | Charge inlet: GCT USB4140, TVS2200, ESDA25W, STUSB4500, input P-FET | Body, rear-panel pad (comes off with the panel) | BO-015 | Spec and CAD ([charge-path.md §3, §6](charge-path.md), [D-040](../decisions.md#d-040)) | Schematic and layout; NVM image and read-back; CP-01 to CP-03, CP-13, CP-14 |

Power-board specification: the RP-02 [board-specs.md](../../02-prototypes/RP-02-electrical/board-specs.md) is the read-only reference, and [power-boards.md](power-boards.md) holds what the build changes. The charge path, from the USB-C inlet to the pack entry, is in [charge-path.md](charge-path.md). Open board work without another home is tracked in [open-items.md](open-items.md).

## Rules

The board outlines in CAD are packaging assumptions. They imply no Gerbers, completed schematic or passed board test.

Basic chassis fit and controlled motor tests can use a regulated bench supply, a development controller, driver boards and a temporary harness. Hall and bare-TCRT circuits can be prototyped separately. Full custom-board fabrication is not a prerequisite for those tests. Battery-powered and integrated sensor/control tests keep their protection, interface and validation requirements.

Before releasing any board, record:

- its exact revision, schematic, BOM and layout;
- connector pinout, protection and enable behaviour;
- mounting dimensions and fabrication/assembly outputs;
- measured electrical results.

When an interface changes, update the affected CAD and the canonical BOM.
