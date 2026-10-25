# PCB-15 — Nose Hall carrier

DRV5055A3 Hall sensor with decoupling and output filter, for the ball-nose touch.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-064 in [BOM.csv](../../BOM.csv) |
| Location | Chassis nose, in the pod-seat slot |
| Specification | [nose-hall-board.md](../../01-chassis/v1/research/nose-hall-board.md)<br>[D-013](../../decisions.md#d-013), [D-057](../../decisions.md#d-057), [D-059](../../decisions.md#d-059) |
| CAD placeholder | `_nose_sensing_parts()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py); seat relief: `DROID_CUTS` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |
| CAD labels | `BALL_NOSE_HALL_CARRIER_PCB`, `BALL_NOSE_HALL_DRV5055A3_SOT23` |
| Final CAD | `Custom PCBs › PCB-15 nose Hall carrier` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | In progress: inputs frozen; envelope fixed by D-059; schematic drawn, ERC clean; layout next | [design/](design/) | 2026-10-14 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-14.

**Spec sources.** [nose-hall-board.md](../../01-chassis/v1/research/nose-hall-board.md) (parts, nets, placement, J10-8 pinout), [D-013](../../decisions.md#d-013), [D-057](../../decisions.md#d-057), the [DRV5055 datasheet](https://www.ti.com/lit/ds/symlink/drv5055.pdf). KiCad stock parts: symbol `Sensor_Magnetic:DRV5055A3xDBZxQ1`, footprints `Package_TO_SOT_SMD:SOT-23`, `Capacitor_SMD:C_0402_1005Metric`, `Resistor_SMD:R_0402_1005Metric`.

**Circuit.**

| Ref | Part | Pins and nets |
|---|---|---|
| U1 | DRV5055A3QDBZR, SOT-23 | 1 VCC → +3V3, 2 OUT → HALL_RAW, 3 GND → GND |
| C1 | 100 nF X7R 0402, 10 V | +3V3 to GND, at U1 (datasheet: ≥ 10 nF) |
| R1 | 1 kΩ 0402 | HALL_RAW to HALL_OUT |
| C2 | 100 nF 0402 | HALL_OUT to GND (R1 + C2: 1.6 kHz low-pass) |
| P1, P2, P3 | 0.8 × 1.2 mm wire pads, back face | +3V3, GND, HALL_OUT |

**Interface.** No connector: three wires of the J10-8 cable are soldered to P1–P3, which go to PCB-10 J10-8 pins 4 (+3V3), 2 (GND) and 5 (HALL_OUT, a C3 ADC input).

**Supply and protection.** +3V3 from PCB-10. The datasheet (SBAS640C) gives I<sub>CC</sub> 2 mA typical and 4 mA maximum at 3.3 V, and a 3.0–3.63 V supply range. The board has no polarity or ESD protection of its own: it is wired once and stays inside the pod. Detecting a broken or unplugged wire needs a defined bias on HALL_OUT at the C3 end (the spec's 2026-09-30 review gate). That bias belongs to PCB-10, not to this board.

**Envelope** (from the CAD source; both `body_v1_model.py` and `01-chassis/v1/cad/body_chassis_model.py` carry the same constants). Board-local coordinates: local Y = world Y − 7.0, local Z = world Z − 30.4. The front face points +X, towards the cap.

| Item | Value |
|---|---|
| Outline | 6.0 (Y) × 4.6 (Z) × 0.8 mm, world X 126.6–127.4, Y 7.0–13.0, Z 30.4–35.0 |
| Mounting | No holes. The board stands in a slot open at the top, 0.1 mm clearance per side, fixed with CA or hot glue |
| U1 | Front face, centred at local (3.0, 2.2), long axis along Y. Body 1.0 mm tall in CAD (1.12 max) |
| Front clear zone | Only the sensor notch: local Y 1.3–4.7, Z 0.8 up to the top edge |
| Back clear zone | Seat relief pocket ([D-059](../../decisions.md#d-059)): local Y 0.8–5.2, Z 0–4.6, parts at most 0.9 mm tall. It joins the lead groove (local Y 2.5–5.5, Z 3.1 up), where P1–P3 sit. C1, R1 and C2 go here |
| Everywhere else | 0.1 mm to the seat on each face: no parts. The board's ends bear on both slot walls |

**Gaps.**

1. **Closed by [D-059](../../decisions.md#d-059): no room for C1, R1 and C2.** On the front, U1's SOT-23 pads reach local Z 3.9, which leaves 0.7 mm under the top edge of the notch. An 0402 with its edge clearance does not fit there. The spec's C1 position, local Y 5.2, lies outside the notch (it ends at 4.7). On the back, R1 and C2 at local Z 1.0–2.0 are below the lead groove and face the seat wall 0.1 mm away. The CAD models the board as a plain block with only U1 on it, so no check could have caught this. D-059 adds the seat relief behind the board, and all three parts move to the back face.
2. Hall plate depth (0.65 mm) is not yet confirmed on TI's drawing. It moves the trip point, not the board.
3. The spec's last paragraph still calls Ø2 × 1 mm the baseline magnet, but its parts table and the CAD use Ø3 × 1.5 mm. This does not affect the board.
4. A 6.0 × 4.6 mm board is probably below JLCPCB's minimum size for assembly, so it will need a panel. Check this at DFM.

## Schematic

[`design/pcb-15-nose-hall.kicad_sch`](design/pcb-15-nose-hall.kicad_sch), with a PDF print, [`pcb-15-nose-hall-schematic.pdf`](design/pcb-15-nose-hall-schematic.pdf). Project footprint library `pcb15` ([`design/pcb15.pretty`](design/pcb15.pretty)) holds the wire pad `WirePad_0.8x1.2mm`. It is marked as left out of the BOM and the pick-and-place file, because it is bare copper.

**ERC** (`kicad-cli sch erc --severity-all`, 2026-10-14): 0 errors, 0 warnings.

**Check against the spec**, row by row, using the exported netlist:

| Spec row | Schematic | Result |
|---|---|---|
| +3V3: U1 pin 1 VCC, C1, wire pad 1 | `+3V3`: U1.1, C1.1, P1 | Match |
| GND: U1 pin 3, C1, C2, wire pad 2 | `GND`: U1.3, C1.2, C2.2, P2 | Match |
| HALL_OUT: U1 pin 2 through R1 to pad 3, C2 from pad 3 to GND | `HALL_RAW`: U1.2, R1.1. `HALL_OUT`: R1.2, C2.1, P3 | Match. `HALL_RAW` names the U1-to-R1 link the spec leaves unnamed |
| U1 DRV5055A3QDBZR, SOT-23, pins 1 VCC / 2 OUT / 3 GND | Stock KiCad symbol `DRV5055A3xDBZxQ1`, footprint `SOT-23`; pinout checked against datasheet Table 4-1 | Match |
| C1 100 nF X7R 0402 10 V, ≥ 10 nF | 100n X7R 10V, `C_0402_1005Metric` | Match (datasheet §7.4: ≥ 0.01 µF ceramic) |
| R1 1 kΩ 0402, C2 100 nF 0402: 1.6 kHz | 1k and 100n X7R 10V, 0402 | Match: 1/(2π · 1 kΩ · 100 nF) = 1.59 kHz |
| No capacitor directly on OUT | C2 sits behind R1 | Match (datasheet §7.1.3) |
| Wire pads 0.8 × 1.2 mm: +3V3, GND, OUT | P1, P2, P3 on `WirePad_0.8x1.2mm` | Match |

**Carry to PCB-10.** For wire-break detection, the datasheet (§7.1.4) puts a 20–100 kΩ pull-up from HALL_OUT to VCC at the receiving end, and reads a fault when the output is within 150 mV of either rail. At the 3 mm stop the field is far past the linear range, so the PCB-10 and firmware design must check that a pressed cap cannot read as a fault.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-14:** design started. Inputs frozen from the spec and the CAD source. Envelope gap 1 found: the seat leaves room only for U1 and the wire pads.
- **2026-10-14:** [D-059](../../decisions.md#d-059) taken (option A). A 0.9 mm relief pocket is cut from the seat behind the board, in `final/v1/cad` only. `check_pcb15_relief.py` passes, and both droid STEPs were rebuilt.
- **2026-10-14:** schematic drawn in KiCad 10 from the spec. ERC 0 errors, 0 warnings. The netlist matches the spec's net table row by row. Supply current confirmed from the datasheet (2 mA typ, 4 mA max).
