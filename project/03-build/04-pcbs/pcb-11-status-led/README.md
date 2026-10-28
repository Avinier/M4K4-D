# PCB-11 — Status LED carrier

WS2812B-2020 status LED on a 5 × 5 × 0.8 mm board behind the crown diffuser.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-085 in [BOM.csv](../../BOM.csv) |
| Location | Head crown |
| Specification | [RP-06 peripheral-selection.md §3](../../../02-prototypes/RP-06-cad/peripheral-selection.md#3-status-light--ws2812b-2020-behind-the-existing-light-pipe), RP-06 head `HEAD-CAD-12`<br>[D-065](../../decisions.md#d-065) (socket, LED part, C1 and R1) |
| CAD placeholder | [`layout_model.py`](../../03-head/v1/cad/layout_model.py) (the CAD label still reads `PCB08`); socket: `PCB11_SOCKET` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |
| CAD labels | `status_LED_PCB08_carrier_5x5`, `status_LED_WS2812B_2020` |
| Final CAD | `Custom PCBs › PCB-11 status LED carrier` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Done: rev A.** Schematic, layout, fab outputs and board STEP; the envelope change has its decision ([D-065](../../decisions.md#d-065)) and the fit check passes | [design/](design/), [fab/revA/](fab/revA/README.md), [cad/](cad/) | 2026-10-26 |
| 2. Procure | Waits for the design batch ([D-064](../../decisions.md#d-064)) | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-25.

**Spec sources.** [peripheral-selection.md §3](../../../02-prototypes/RP-06-cad/peripheral-selection.md#3-status-light--ws2812b-2020-behind-the-existing-light-pipe) (part, carrier, light pipe, driver, wiring), RP-06 head `HEAD-CAD-12`, BOM row CH-085. Datasheets: [Worldsemi WS2812B-2020-V6](https://addressable.wiki/datasheets/worldsemi/ws2812b-2020-v6-c52917434.pdf) (the LCSC C52917434 copy; Worldsemi's own V1.2 of 2026-03-18 matches it), and the [D1 schematic](https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3/manual/ESP32-S3-Touch-LCD-4.3-Sch.pdf) (Waveshare ESP32-S3-LCD-4.3, which shares the touch board's schematic). KiCad stock parts: symbol `LED:WS2812B-2020`, footprints `LED_SMD:LED_WS2812B-2020_PLCC4_2.0x2.0mm`, `Capacitor_SMD:C_0402_1005Metric`, `Resistor_SMD:R_0402_1005Metric`.

**Circuit** (C1 and R1 added by [D-065](../../decisions.md#d-065)).

| Ref | Part | Pins and nets |
|---|---|---|
| LED1 | Worldsemi WS2812B-2020-V6 (3.3–5.3 V) | 1 DO → not connected, 2 GND → GND, 3 DI → LED_DIN, 4 VDD → +3V3 |
| C1 | 100 nF X7R 0402, 10 V | +3V3 to GND, on the back behind LED1, one via from each LED pin (datasheet application circuit) |
| R1 | 330 Ω 0402, 1 % | DIN (from the wire) to LED_DIN, on the back between P3 and LED1's DI via |
| P1, P2, P3 | Wire pads for AWG30 PTFE, back face, right half (u 2.3–5.0) | +3V3, GND, DIN |

The LED's reference is **LED1**, not KiCad's default D1, because D1 is the face controller's name in this project (RP-04).

**Pinout check.** Datasheet V6 pin table: 1 DO, 2 GND, 3 DI, 4 VDD. KiCad's symbol has 1 DOUT, 2 VSS, 3 DIN, 4 VDD, a match. The stock footprint's pads (0.7 × 0.7 mm at x ± 0.915, y ± 0.55) are the datasheet's recommended land pattern: 0.7 mm pads, 1.13 mm apart across the body and 0.40 mm apart along it. The footprint is the datasheet's top view turned 180°, with the same pin order around the body. The V6 also accepts data on either DI or DO, and survives reversed supply.

**Interface.** No connector: three AWG30 PTFE wires are soldered to P1–P3 and run to D1's `Sensor AD` header, J6 on the Waveshare schematic (2.0 mm pitch, 3 pins): **pin 1 3V3, pin 2 GND, pin 3 AD = GPIO6**. GPIO6 runs straight from the ESP32-S3 module to J6 with no filter or divider on it, so an 800 kbit/s data stream passes cleanly. Firmware sends it with the RMT peripheral ([peripheral-selection.md §3](../../../02-prototypes/RP-06-cad/peripheral-selection.md#3-status-light--ws2812b-2020-behind-the-existing-light-pipe)). The housing (PH2.0 in the spec, HY2.0 in Waveshare's guide) is a harness item for [05-harness](../../05-harness/README.md): check it on the received board.

**Supply and protection.** +3V3 comes from D1's own 3.3 V regulator through J6, so the LED and its data source share one supply. The V6 datasheet gives 3.3–5.3 V, 12 mA per colour (36 mA white), < 1 µA idle, and V<sub>IH</sub> 0.55 × VDD (1.8 V at 3.3 V), so a 3.3 V GPIO drives it with no level shifter. A 3.3 V supply is the bottom of the V6's range: brightness and colour at 3.3 V stay the G03 bench item. The board has no ESD or polarity parts. It sits inside the head and is wired once, and the V6 survives reversed supply.

**Sourcing** (2026-10-26, [D-065](../../decisions.md#d-065)). Only the **V6** is used: it is rated from 3.3 V. Worldsemi moved all WS2812B production to V6 on 2025-09-30, with the same package and pinout.

| Route | Source | State on 2026-10-26 |
|---|---|---|
| Fab assembly (JLCPCB PCBA) | LCSC/JLCPCB **C52917434** | 783k in stock, US$0.09 each in 5s, JLCPCB extended part |
| India, no import | **Hubtronics** (Pune), SKU 07957, ₹10 incl. GST | Listed, 0 in stock. Send an RFQ before procurement; a listing can return to stock |
| Not usable | Pre-V6 WS2812B-2020 (LCSC C965555), stocked in India by Robu, Evelta, Hubtronics (6,952), Quartz Components (2,277), Punoscho (2,965), Sharvi | Same footprint and pinout, but rated **3.7–5.3 V**. On D1's 3.3 V it runs out of spec. Using it would need a 5 V feed to the crown, which is a new decision |

TME lists the V6 on its India site but ships from Poland, so it is an import.

**Envelope** (head frame R, measured on the built `layout_model.build_parts()` solids, 2026-10-25). Board-local coordinates, looking at the front face from +X: u = world Y − 12.7 (right), v = world Z − 89.3 (up). The front face points +X, into the light pipe.

| Item | Value |
|---|---|
| Outline | 5.0 × 5.0 × 0.8 mm, world X −8.0…−7.2, Y 12.7…17.7, Z 89.3…94.3 |
| LED | Front face, centred at local (2.5, 2.5). Package 2.0 × 2.0 × 0.84 mm (± 0.15). Its top at X −6.36 leaves 1.36 mm of air to the light pipe |
| Light pipe | Ø3.4 × 2.9 mm, X −5.0…−2.1, on the LED axis |
| Front clear zone | 2.2 mm deep up to the light pipe, 5.2 mm deep beside it, up to the crown front wall at X −2 |
| Back, u 0–2.3 (Y 12.7–15.0) | **0.6 mm** of air to the camera bracket's front lip (`removable_camera_edge_bracket_trial`, X −8.6), all heights v 0–5 |
| Back, u 2.3–5.0 (Y 15.0–17.7) | Open back to the skin at X −34.8 |
| Top right corner (u 5, v 5) | 0.49 mm to the crown's sloped side wall |
| Left and bottom edges | Nothing within 5.5 mm |
| Mounting | **Socket fused inside the crown** ([D-065](../../decisions.md#d-065)). The pocket is X −8.1…−7.2 with 0.1 mm per side, and the board's front edge rests on a 0.5 mm shoulder (local u, v 0–0.5 and 4.5–5). The front cavity, u, v 0.5–4.5, is 1.8 mm deep to the pipe's stop lip at X −5.4. The board goes in from behind before the camera bracket and is glued at its edges |
| Front parts | Inside u, v 0.5–4.5 only (the shoulder ring is part-free). Only LED1 goes there (0.99 mm max, 0.81 mm to the lip). The 0402s fit by height but not by footprint area beside the centred LED, so C1 and R1 are on the back (D-065, amended at layout) |

**Gaps.**

1. **Closed by [D-065](../../decisions.md#d-065): nothing held the board or the light pipe.** The board is a free block in the crown cavity, 0.49 mm from the crown wall and 0.6 mm from the camera bracket. The light pipe is not in its bore either. The crown front wall is only X −2…0 thick, the Ø3.6 bore is cut through that wall, and the pipe sits behind it at X −5.0…−2.1, 0.14 mm from the wall and touching nothing. The spec says the pipe is "UV-bonded in the Ø3.6 crown bore", but the drawn bore is 2 mm long, and the pipe is 2.9 mm long and not in it. D-065 fuses a socket into the crown that holds both. [`check_pcb11_socket.py`](../../final/v1/cad/check_pcb11_socket.py) passes.
2. **Closed by D-065: the spec's back pads couldn't all sit on the back.** The spec puts the three wire pads on the back and turns the wires 90° within 2 mm. The camera bracket's lip covers the back's left half (u 0–2.3) at 0.6 mm, which leaves no room for a solder joint and AWG30 PTFE (about 0.5 mm OD). The pads and wire exit must go in the right half (u 2.3–5.0), where the back is open. No part may sit on the back's left half.
3. **Closed by D-065 (C1 added): C1 was left out because of an old datasheet claim.** The spec says the LED has a "built-in capacitor". The V6 datasheet's front page still says "no external components (including capacitors) are required", but its revision log adds a 100 nF VDD capacitor to the application circuit (V1.1, 2025-12-01; V1.2, 2026-03-18). Here the supply runs through a long, thin AWG30 wire (the route to D1 isn't drawn yet; probably 0.1–0.2 m), and the LED switches up to 36 mA at its 2 kHz PWM. A local 100 nF keeps that pulse off the wire.
4. **Closed by D-065 (R1 = 330 Ω): no series resistor on DIN in the spec.** Adafruit's guide for these LEDs puts a few hundred ohms in series with the data line at the LED end. It limits current into the LED's input clamp if the LED loses power while GPIO6 is high (a broken 3V3 wire), and it slows the edge a little. With 15 pF of input capacitance, 330 Ω gives a 5 ns time constant, far below the 220 ns shortest pulse. It costs one 0402.
5. **Closed by D-065 (BOM fixed): wrong LCSC number in the BOM.** CH-085 names LCSC C965555, the older WS2812B-2020. Its datasheet (V1.3) gives a 3.7–5.3 V supply, so it is not specified at 3.3 V. The V6 the spec selected is **LCSC C52917434** (JLCPCB extended part; LCSC stock 786,685 on 2026-10-25, US$0.09 each in 5s). See *Sourcing* above.
6. **Closed 2026-10-26 (project model in `design/pcb11.3dshapes/`): no 3D model for the LED in KiCad.** The stock footprint points to `LED_WS2812B-2020_PLCC4_2.0x2.0mm.step`, which the nightly doesn't ship. Without it the board STEP has no LED. The project footprint `pcb11:LED_WS2812B-2020-V6` now points at a project model built from the datasheet dimensions.
7. The CAD labels still read `PCB08` (the RP-06 name). Rename them in stage 3 together with the `CUSTOM_PCBS` pattern in `makad-v1.step.py`.
8. A 5 × 5 mm board is below every fab's assembly minimum, so it is panelised, as PCB-15 is.

### Mounting and wire side: decided

[D-065](../../decisions.md#d-065), option A (builder, 2026-10-26). Of the options in the decision (A, the socket; B, a sleeve with the board glued to its end; C, glue by hand), A is the only one that locates the LED on the pipe axis and holds the light pipe. At layout, C1 and R1 moved to the back's right half: they don't fit beside the centred LED (see [Layout](#layout)). Assembly order: light pipe from the front onto the lip, then PCB-11 from behind, then the camera and its bracket. The ivory ASA walls (0.8–1.3 mm) may let light through. If the G03 bench shows a halo on the crown, paint the cavity matte black.

## Schematic

[`design/pcb-11-status-led.kicad_sch`](design/pcb-11-status-led.kicad_sch), with a PDF print, [`pcb-11-status-led-schematic.pdf`](design/pcb-11-status-led-schematic.pdf). The design folder was written for the KiCad 10.99 nightly, so it may not open in 10.0.6.

**Project set-up.**

| File | Holds |
|---|---|
| `pcb-11-status-led.kicad_pro` | PCB-15's project, renamed. Its board minimums and default net class are already the fab-neutral values (gap and track 0.16, via 0.67/0.35, edge 0.3, hole spacing 0.31); PCB-15's still holds the older JLCPCB-only values |
| `pcb-11-status-led.kicad_dru` | The fab-neutral rules ([D-062](../../decisions.md#d-062)), copied from PCB-15 |
| `fp-lib-table`, `pcb11.pretty/` | Project library `pcb11`. `LED_WS2812B-2020-V6` is KiCad's stock `LED_WS2812B-2020_PLCC4_2.0x2.0mm` land pattern with a project 3D model; `WirePad_0.8x1.2mm` is PCB-15's wire pad, marked left out of the BOM and the position file |
| `pcb11.3dshapes/LED_WS2812B-2020-V6.step` | The LED body from the V6 datasheet: 2.2 × 2.0 mm base 0.28 mm tall, 2.0 × 2.0 mm lens to 0.84 mm. KiCad's library has no model for this package (gap 6, closed) |

**Parts and fields.** LED1 uses the stock symbol `LED:WS2812B-2020` and carries `MPN` WS2812B-2020-V6, `Manufacturer` Worldsemi, `LCSC` C52917434, and the V6 datasheet link. The passives get their MPNs at procure, as PCB-15's did. P1–P3 use `Connector:TestPoint`, marked not in the BOM. `PWR_FLAG` sits on +3V3 and GND, which enter through wire pads. DOUT has a no-connect flag.

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-26): 0 errors, 0 warnings. KiCad skips its footprint-filter check by default. The stock symbol's filter (`LED*WS2812*-2020_PLCC4*`) doesn't match the project footprint's name; that is expected.

**Check against the spec**, row by row, using the exported netlist:

| Spec row ([Inputs](#inputs), D-065) | Netlist | Result |
|---|---|---|
| +3V3: LED VDD (pin 4), C1, wire pad P1 | `+3V3`: LED1.4, C1.1, P1.1 | Match |
| GND: LED GND (pin 2), C1, wire pad P2 | `GND`: LED1.2, C1.2, P2.1 | Match |
| DIN: wire pad P3 to R1 | `/DIN`: P3.1, R1.1 | Match |
| R1 to the LED's DI (pin 3) | `/LED_DIN`: R1.2, LED1.3 | Match. `LED_DIN` names the R1-to-LED link |
| DO (pin 1) not connected | `unconnected-(LED1-DOUT-Pad1)`, no-connect flag | Match |
| LED1 WS2812B-2020-V6, pins 1 DO / 2 GND / 3 DI / 4 VDD | Stock symbol pins 1 DOUT / 2 VSS / 3 DIN / 4 VDD; footprint `pcb11:LED_WS2812B-2020-V6` | Match (datasheet V6 pin table) |
| C1 100 nF X7R 0402 10 V | `100n X7R 10V`, `C_0402_1005Metric` | Match |
| R1 330 Ω 0402 | `330`, `R_0402_1005Metric` | Match |
| Three wire pads, not in the BOM | P1–P3 on `pcb11:WirePad_0.8x1.2mm`, `in_bom no` | Match |

## Layout

KiCad 10.99 nightly, laid out by hand through KiPy, with no autorouter ([D-060](../../decisions.md#d-060), [layout rules](../README.md#layout-rules)).

**Board set-up** (`design/pcb-11-status-led.kicad_pcb`, written before any part was placed):

| Item | Value | Why |
|---|---|---|
| Outline | KiCad x 100–105, y 100–105 | Board-local u = x − 100 (world Y − 12.7), v = 105 − y (world Z − 89.3), viewed from the front (+X). The aux and grid origins sit at local (0, 0), so the position file reads in board-local u, v |
| Faces | F.Cu is the front, towards the light pipe: LED1, C1 and R1. B.Cu is the back: P1–P3 | D-065 |
| Stackup | 0.8 mm: 35 µm copper, 0.71 mm FR4 core, mask, HASL lead-free | Spec; same as PCB-15 |
| Rules | Fab-neutral ([D-062](../../decisions.md#d-062)) in the `.kicad_pro` and `design/pcb-11-status-led.kicad_dru` | Any of JLCPCB, PCBWay or Lion Circuits MII can make it |
| Socket keep-outs | Rule areas forbid footprints on F.Cu on the socket shoulder, local 0–0.5 mm all round (`FRONT_SHOULDER_T/B/L/R`). On B.Cu they forbid footprints on the left half, u 0–2.3, behind the camera bracket lip (`BACK_BRACKET`). Tracks and vias are allowed in both | DRC then checks the D-065 envelope on every run |
| Drawings | The shoulder's inner edge (`Socket.Shoulder`), the bracket shadow (`Bracket.Lip`), and the Ø3.4 pipe and Ø2.6 lip window (`Light.Pipe`), on user layers | Orientation while placing |

**DRC on the empty board** (nightly, 2026-10-26): 0 violations. On a scratch copy, a 0402 placed in the front shoulder and another behind the bracket were each flagged by their keep-out. A third, on the back's right half, was not. So the rule areas work.

**Placement** (2026-10-26, through KiPy, one functional group at a time). KiCad coordinates, mm:

| Part | Side | Position, rotation | Notes |
|---|---|---|---|
| LED1 | Front | (102.5, 102.5), 0° | Centred on the pipe axis. Pins: 1 DOUT (101.585, 101.95), 2 GND (101.585, 103.05), 3 DI (103.415, 103.05), 4 VDD (103.415, 101.95) |
| P1, P2, P3 | Back | (104.2, 101.0 / 102.5 / 104.0) | +3V3, GND, DIN, in a column at the right edge. Pads 0.4 mm from the edges and 0.3 mm apart |
| C1 | Back | (102.95, 101.75), 270° | +3V3 pad up (y 101.27), GND pad down (102.23), level with P1 and P2 |
| R1 | Back | (102.95, 103.75), 90° | LED_DIN pad up (103.24), DIN pad down (104.26), level with P3 |

**Why C1 and R1 are on the back.** Inside the 4.0 × 4.0 mm shoulder ring, the centred LED's courtyard (3.04 × 2.50 mm, KiCad stock) leaves strips 0.75 mm tall above and below it. An 0402's courtyard is 0.92–0.94 mm tall, so neither fits on the front. The builder chose the back's right half over narrowing the socket shoulder ([D-065](../../decisions.md#d-065), amended at layout). C1 and R1 stand upright 0.38 mm left of the wire pads' column, and their courtyards stay right of the `BACK_BRACKET` keep-out (x ≥ 102.3).

**Routing** (by hand through KiPy, no autorouter). All tracks are 0.2 mm, the largest current being 36 mA at full white. Every segment is horizontal, vertical or 45°.

| Net | Front | Via, 0.67/0.35 mm | Back |
|---|---|---|---|
| +3V3 | LED pin 4 straight up, then left | (102.0, 100.8), above the LED | Via to C1 pin 1, then on to P1 |
| GND | LED pin 2 down, then 45° down-left | (100.8, 104.2), bottom left | Via up the left side to C1 pin 2, then on to P2 |
| LED_DIN | LED pin 3 down, 45°, then left | (101.9, 104.2), below the LED | Via 45° up-right to R1 pin 2 |
| DIN | — | — | R1 pin 1 to P3 |

Beside the LED there is no room for a via: the 0.31 mm via spacing and the 0.3 mm edge rule leave a negative gap. So all three vias sit in the strips above and below it. Two of them lie partly on the front shoulder, where tracks and tented vias are allowed. The back's left half, behind the camera bracket, carries only the GND track and two vias, which are flat.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, fab-neutral `.kicad_dru` in place, 2026-10-26): 0 errors, 0 unconnected pads, 0 schematic-parity issues, 0 keep-out hits. On a scratch copy with the via-hole minimum raised to 0.4 mm, all three vias were flagged, so the rules file is enforced. Two warnings remain, `lib_footprint_mismatch` on C1 and R1. They are the cosmetic kind PCB-15 found: the parts are rotated and flipped, and their reference labels were moved to the fab layers. Both 0402s and LED1 kept their 3D models (`audit()`: 1/1 each).

Reference labels moved from silkscreen to the fab layers (`refs_to_fab()`). The stock footprints still carry 0.12 mm silkscreen outlines, below the fab-neutral 0.16 mm line, as on PCB-15. The fab set leaves silkscreen out (below).

## Checks and outputs (rev A)

- **ERC** 0 errors, 0 warnings. **DRC** with schematic parity: 0 errors, 0 unconnected, and the 2 cosmetic warnings above. **`audit()`**: LED1, C1 and R1 each have their 3D model. P1–P3 are left out of the BOM and the position file.
- **Board STEP:** [`cad/pcb-11-status-led-revA.step`](cad/pcb-11-status-led-revA.step). It lists the board, LED1 (the project model's base and lens), C1 and R1. The board core runs Z 0–0.71 and the parts sit 0.085 mm off it. LED1's model is 0.84 mm tall; KiCad's 0402 models are 0.5 mm (C) and 0.35 mm (R).
- **Outputs:** [`fab/revA/`](fab/revA/README.md) holds Gerber X2 and Excellon drill, both from the board-local origin, the placement file in KiCad and JLCPCB CPL formats, the fab BOM with LCSC numbers, a Gerber zip and the order parameters. The set has no silkscreen.
- **Fit in the robot:** [`final/v1/cad/check_pcb11_fit.py`](../../final/v1/cad/check_pcb11_fit.py) places the STEP in the D-065 socket, with the front copper on the shoulder at head X −7.2. **PASS:**

  | Check | Result |
  |---|---|
  | Board in the pocket | Core X −7.945…−7.235, centred on the pipe axis; no clash; 0.100 mm from each pocket wall |
  | LED1 | On the pipe axis (offset 0.000, 0.000). Model top X −6.31, which leaves 0.91 mm to the lip and 1.31 mm to the pipe. Real maximum (0.99 mm part plus solder) X −6.16: 0.76 mm to the lip |
  | Back parts | C1 0.41 mm and R1 0.46 mm from the camera bracket, the nearest part. Both start at Y 15.40, beside the bracket lip, which ends at Y 15.0. A 0.55 mm maximum 0402 stops at X −8.58, short of the lip's plane at −8.6 |
  | Everything else | Camera 2.13 mm, skin 6.13 mm |

  `check_pcb11_socket.py` (D-065) also still passes.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-25:** design started. Inputs frozen from the spec, the V6 datasheet, D1's schematic and the head CAD. Gaps found: nothing holds the board or the light pipe; the camera bracket sits 0.6 mm behind half of the back face; the V6 datasheet now asks for a 100 nF VDD capacitor; the BOM names the pre-V6 LED (C965555).
- **2026-10-26:** [D-065](../../decisions.md#d-065) taken (option A). A socket fused inside the crown holds the board and the light pipe (`DROID_ADDS`, [`check_pcb11_socket.py`](../../final/v1/cad/check_pcb11_socket.py) PASS). C1 (100 nF) and R1 (330 Ω) added. LED part pinned to the V6 (C52917434). In India only Hubtronics lists it, with 0 in stock, so RFQ at procure. BOM, register, head BOM and sourcing matrix updated.
- **2026-10-26:** schematic drawn for the KiCad 10.99 nightly: LED1, C1, R1 and P1–P3, project footprint library `pcb11` with a datasheet-sized LED model. ERC 0 errors, 0 warnings. The netlist matches the spec row by row.
- **2026-10-26:** board set up for layout: 5 × 5 mm outline, 0.8 mm stackup, fab-neutral rules, socket keep-outs (front shoulder, back bracket side). DRC on the empty board: 0 violations. The keep-outs were proven on a scratch copy.
- **2026-10-26:** placed and routed by hand through KiPy on the nightly. C1 and R1 do not fit beside the centred LED (courtyards), so the builder moved them to the back's right half ([D-065](../../decisions.md#d-065) amended). Three vias, all 0.2 mm tracks. DRC 0 errors, 0 unconnected, parity clean; 2 cosmetic `lib_footprint_mismatch` warnings. The wire pads' position-file flag was set again after F8.
- **2026-10-26:** lesson 5. Models audited; board STEP exported with parts; new fit check `final/v1/cad/check_pcb11_fit.py` PASS (LED on axis, 0.76 mm to the lip at worst, back parts 0.41 mm from the bracket). Rev A outputs exported to `fab/revA/`: one origin throughout, no silkscreen. Stage 1 done.
