# 04 — Custom PCB work

This folder owns future schematic, layout, fabrication and electrical-validation work for the robot's custom boards. It is a work area, not a fabrication release. Current part records remain in the [project BOM](../BOM.csv); all selections and changes belong in the [build decisions](../decisions.md).

| Board | Current purpose | Work still required |
|---|---|---|
| PCB-01 | Proposed 2S pack protection | Decide custom versus qualified purchased protection; specify cell monitoring, fault limits and pack construction |
| PCB-02 | Charging and system power | Schematic, charger/NTC integration, power-path and protection validation |
| PCB-03 | Motor gating and distribution | Schematic, disable/fault behaviour, current and braking validation |
| PCB-04 | Branch voltage conversion | Rail/current requirements, schematic and load/thermal validation |
| PCB-07 | Proposed base IMU carrier | Decide sensor and SPI versus I²C interface; retail budget breakout changes mount and wiring |
| PCB-10 | C3 controller carrier | Schematic/layout, J10-8 Hall analog pin changes, J10-10 bare TCRT LED/load circuit |
| CH-064 | Tiny nose Hall carrier | Routable 6 × 4.6 × 0.8 mm assembly, fabrication files, mounting and measured diagnostics |

The current board outlines are packaging assumptions. No Gerbers, completed schematic or passed board tests are implied by their CAD envelopes.

Basic chassis fit and controlled motor tests can use a regulated bench supply, development controller, driver carriers and temporary harness. Hall and bare-TCRT circuits can be prototyped separately. Full custom-board fabrication is not a prerequisite for those tests. Battery-powered operation and integrated sensor/control tests retain their specific protection, interface and validation requirements.

Before releasing any board, record its exact revision, schematic/BOM/layout, connector pinout, protection and enable behaviour, mounting dimensions, fabrication/assembly outputs and measured electrical results. Update affected chassis geometry and the canonical BOM when an interface changes.
