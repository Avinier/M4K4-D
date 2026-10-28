# PCB-10 — C3 controller carrier

Carrier for the C3 DevKitC: watchdog, READY, sleep gate, Hall and TCRT circuits.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-044 in [BOM.csv](../../BOM.csv) |
| Location | Body, −Y side wall |
| Specification | [RP-06 connector-schedule.md](../../../02-prototypes/RP-06-cad/connector-schedule.md)<br>[power-boards.md §2.4](../power-boards.md#24-logic-to-c3-j10-5--j10-6-gh-6)<br>[D-068](../../decisions.md#d-068) (mounting, DevKitC, watchdog, transceiver) |
| CAD placeholder | `c3_carrier()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `C3_CARRIER_PCB10_WITH_DEVKITC` |
| Final CAD | `Custom PCBs › PCB-10 C3 controller carrier` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Done: rev A** (lesson 5). DRC 0 errors, 0 unconnected, parity clean; fit in the robot 7/7; fab outputs in [`fab/revA/`](fab/revA/README.md); inputs frozen with [D-068](../../decisions.md#d-068) | [`check_pcb10_mount.py`](../../final/v1/cad/check_pcb10_mount.py) 9/9, [`check_pcb10_fit.py`](../../final/v1/cad/check_pcb10_fit.py) 7/7 | 2026-10-28 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-27 with [D-068](../../decisions.md#d-068): the builder left gaps 1–4 to the recommended options, asked for the genuine Espressif board only, and for the watchdog from the next best source.

**Spec sources.**

- RP-06 [connector-schedule.md](../../../02-prototypes/RP-06-cad/connector-schedule.md) `CN-06` and §3.3 (read-only): board, mounting, header rows.
- RP-02 [board-specs.md §7](../../../02-prototypes/RP-02-electrical/board-specs.md#7-safety-carrier-watchdog-block-c2-and-c3-carriers--decided-2026-09-25-bd-10) (`BD-10`, watchdog and READY) and §8 (inter-board signals); [compute-control-architecture.md](../../../02-prototypes/RP-02-electrical/compute-control-architecture.md) `CA-03`, `CA-05`, `CA-06`, `CA-10` and §3 (C3 I/O budget).
- RP-03 [base-control-architecture.md §3](../../../02-prototypes/RP-03-locomotion/base-control-architecture.md#3-pin-map-v01--esp32-s3-devkitc-1-n8) (pin map v0.1).
- [power-boards.md §2.4](../power-boards.md#24-logic-to-c3-j10-5--j10-6-gh-6) (`J10-5`/`J10-6`, AND gate, `FLT`) and §6 (D-041: no E-stop, `J10-11` not fitted).
- [D-013](../../decisions.md#d-013) and [nose-hall-board.md](../../01-chassis/v1/research/nose-hall-board.md) (`J10-8`); [D-016](../../decisions.md#d-016)/[D-021](../../decisions.md#d-021) and [rear-tcrt-lead.md](../../01-chassis/v1/research/rear-tcrt-lead.md) (`J10-10` and its circuit); [D-039](../../decisions.md#d-039) and [05-harness §5](../../05-harness/README.md#5-pinouts) (pinouts; encoders on the carrier 3V3); [D-048](../../decisions.md#d-048) (row repack).
- BOM rows CH-044 (this board) and CH-045 (DevKitC-1-N8).
- CAD: `C3_*` constants and `c3_carrier()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py), measured in the built body (*Envelope*).

**Datasheets read.** Espressif [ESP32-S3-DevKitC-1 v1.1 user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html), [dimension drawing](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.pdf) and [schematic](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf); TI [THVD1451](https://www.ti.com/lit/ds/symlink/thvd1451.pdf) (SLLSEY3E), [TPS3436-Q1](https://www.ti.com/lit/ds/symlink/tps3436-q1.pdf) (SLVSGF1A), [SN74LVC1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf), [SN74LVC1G11](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf), [DRV5055](https://www.ti.com/lit/ds/symlink/drv5055.pdf); Sharp [GP2Y0A21YK0F](https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf); AOS AO3400A (LCSC C20917 page); ThinkRobotics [MOT3001 page](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors).

### The DevKitC as built

The CAD's DevKitC (`ESP32-S3-WROOM-1_devkit_2xUSBC_c.step`, a FreeCAD model of a generic board) is **not** Espressif's DevKitC-1 v1.1:

| | CAD STEP | Espressif v1.1 (drawing) |
|---|---|---|
| Board width | 28.3 mm | **25.40 mm** |
| Header row spacing | 25.4 mm | **22.86 mm** (pins 1.27 mm in from each long edge) |
| Pins | 2 × 22, 2.54 mm pitch | Same |
| Antenna end past pin 1 | 8.2 mm | about 7.9 mm (module overhangs the board end by about 6.4 mm) |
| USB end past pin 22 | 2.6 mm | **8.0 mm** (two USB-C) |
| Pins modelled | No, only the 44 pad holes | — |
| Bottom side | Flat | Flat; header plastic 2.5 mm; USB shell legs and solder joints not dimensioned (`U`) |

The carrier footprint uses the v1.1 drawing. Keeping the CAD's pin columns and row centre: pins at X −8.49 + 2.54 k (k 0…21), **J1 row at Z 98.92, J3 row at Z 121.78**, board Z 97.65–123.05. Pin 1 of both rows is at the antenna end, X 44.85; the USB ports face −X with their fronts at about **X −16.5**, 2.5 mm past the carrier's −X edge and inside the service corridor. Seen from the component side with the antenna up, J1 is on the left, the `UART` port bottom-left and the `USB` port bottom-right. In the robot that puts J1 low, J3 high, the UART port at about Z 103 and the native USB port at about Z 117.

Header pins (user guide, v1.1):

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J1 | 3V3 | 3V3 | RST (EN) | 4 | 5 | 6 | 7 | 15 | 16 | 17 | 18 | 8 | 3 | 46 | 9 | 10 | 11 | 12 | 13 | 14 | 5V | G |
| J3 | G | 43 TX | 44 RX | 1 | 2 | 42 | 41 | 40 | 39 | 38 | 37 | 36 | 35 | 0 | 45 | 48 | 47 | 21 | 20 | 19 | G | G |

Two facts the pin map v0.1 did not have:

- **On v1.1 the RGB LED is on GPIO38**, not GPIO48 (v1.0 had it on 48). So GPIO48 is free for `WDI` on v1.1, and GPIO38 drives the LED's data input, so it is not a clean spare. On a v1.0 board `WDI` would also clock the LED: harmless flicker, no fault.
- **The 5V header pin is `VCC_5V`, downstream of the USB diodes** (1N5819 from each USB `VBUS`). A service USB cable therefore powers the carrier's 5 V net, and through `J10-1` it back-feeds `W11` into PCB-04's `PB-SAFE-BASE` output and the GP2Y. See gap 4.

GPIO35–37 are free on the N8 module (they go to octal PSRAM only on R8 variants, `CA-03`).

### GPIO map (v0.3, set at layout)

v0.2 (D-068) assigned the pins by function; v0.3 reassigns them at placement (lesson 4, 2026-10-28) so that every track runs from its DevKitC pin to its connector without crossing another. The bottom pin row (J1, nearest the connectors) feeds the connectors in their left-to-right order; the top row (J3) carries the signals that go further down (row B and C connectors) and the watchdog cluster. The roles are unchanged and every rule still holds: no strapping or USB pins, the three analog inputs on ADC1, `MCU_RDY`/`WDI`/`NSLEEP` on plain GPIO, LEDC, PCNT, UART1 and the IMU's SPI through the GPIO matrix (the IMU runs at 10 MHz or less).

| Function | GPIO | DevKitC pin | Carrier net / connector | v0.2 |
|---|---:|---|---|---:|
| `TCRT_LED_EN` | 4 | J1-4 | Q1 gate (100 kΩ pull-down) | 47 |
| `TCRT_ADC` (ADC1_CH4) | 5 | J1-5 | R37 1 kΩ from `TCRT_OUT`, `J10-10` pin 3 | 8 |
| `ENC_R_A`, `ENC_R_B` | 6, 7 | J1-6, J1-7 | `J10-4` pins 3, 4 | 6, 7 |
| `ENC_L_A`, `ENC_L_B` | 15, 16 | J1-8, J1-9 | `J10-3` pins 3, 4 | 4, 5 |
| `MOTOR_PRESENT` | 17 | J1-10 | `J10-12` pin 3 (1 kΩ, 100 kΩ pull-down) | 40 |
| `nFAULT` | 18 | J1-11 | `FLT` (`J10-5`/`J10-6` pin 4) through 1 kΩ, 10 kΩ pull-up | 9 |
| IMU `SCLK` | 8 | J1-12 | `J10-7` pin 3 | 37 |
| IMU `MOSI`, `MISO` | 9, 10 | J1-15, J1-16 | `J10-7` pins 4, 5 | 35, 36 |
| IMU `CS`, `INT1` | 11, 12 | J1-17, J1-18 | `J10-7` pins 6, 7 (CS 10 kΩ pull-up) | 41, 42 |
| C0 link `RX`, `TX` (UART1) | 13, 14 | J1-19, J1-20 | THVD1451 `R`, `D` | 18, 17 |
| `GP2Y_VO` (ADC1_CH0) | 1 | J3-4 | `J10-8` pin 3 through the 10k/22k divider | 1 |
| `HALL_OUT` (ADC1_CH1) | 2 | J3-5 | `J10-8` pin 5 (1 kΩ, 1 MΩ open-wire pull-down) | 10 |
| `IN1_R`, `IN2_R` (LEDC) | 42, 41 | J3-6, J3-7 | `J10-6` pins 2, 3 | 12, 14 |
| `IN1_L`, `IN2_L` (LEDC) | 37, 36 | J3-11, J3-12 | `J10-5` pins 2, 3 | 11, 13 |
| `WDI` | 48 | J3-16 | TPS3436 `WDI`, 10 kΩ pull-up | 48 |
| `MCU_RDY` | 47 | J3-17 | READY gate input, pull-down | 2 |
| `nSLEEP` | 21 | J3-18 | Sleep gate U4 input A, 100 kΩ pull-down | 21 |
| IMU `INT2` | — | — | `J10-7` pin 8: not connected (PCB-07 is HOLD) | — |
| Unused | 0, 3, 45, 46 (strapping); 19, 20, 43, 44 (USB) | | Not connected | |
| Spare | **35, 39, 40**; 38 drives the v1.1 RGB LED | J3-13, J3-9, J3-8; J3-10 | Not connected | 15, 16, 39 |

**Budget.** 24 of the 28 assignable GPIO are used, as in v0.2. Unassigned and safe: **35, 39, 40**, plus 38 behind the board LED, so the `CA` §3 gate of at least two safe spares holds. ADC1 left free: GPIO6–10 are used digitally but stay ADC1-capable. `ENERGY_OK` (v0.1 GPIO39) still has no cable to C3; `ESTOP_N` (GPIO3) was deleted by D-041. The firmware's `c3_board_role.h` (RP-02 phase A) still has v0.1 and is regenerated from this table when the board is released (`CA-14`).

### Circuit

| Block | Parts | Rules |
|---|---|---|
| DevKitC | U1 ESP32-S3-DevKitC-1-N8 (CH-045), soldered through its 2 × 22 headers | 5V pin from `J10-1` (gap 4); 3V3 pins feed the carrier's 3.3 V logic; EN (J1-3) pulled low by the watchdog |
| Base link (`CA-05`) | U2 THVD1451 (or gap 3), 120 Ω across the receiver `A`/`B`, 0.1 µF at `VCC` | Full duplex, 921.6 kbaud. Open, short and idle fail-safe in the part, so no bias resistors. PCB-10 terminates its own receiver; PCB-09 terminates its own |
| Watchdog (`BD-10`, D-068) | U3 **TPS3436CCCBGDDFRQ1**, pinout C, SOT-23-8 (DDF) | `SET0`, `SET1` to GND: tWC 5 ms, tWO 15 ms, so feed every 10 ms (window 5.5–18 ms, late fault ≤ 22 ms); 500 ms startup delay (first edge from early boot), 200 ms `WDO` assert. `WDI` from GPIO48 with 10 kΩ pull-up. `WDO` open drain, 10 kΩ pull-up, to DevKitC EN and the READY gate. `WD-EN` pulled high; service jumper `JP_SVC` to GND disables the watchdog and forces READY low. `MR`: see gap 7. 0.1 µF at `VDD` (datasheet) |
| READY (`BD-10`, `BC-08`) | U5 74LVC1G11 (3-input AND) | `C3_READY = WDO ∧ WD-EN ∧ MCU_RDY`. `MCU_RDY` (GPIO2) has a 10 kΩ pull-down. Output through ≥ 1 kΩ to `J10-12` pin 2 (`BASE_READY` at PCB-03) and to U4 |
| Sleep gate (power-boards §2.4) | U4 74LVC1G08 | `SLP = nSLEEP ∧ C3_READY`, each input with 100 kΩ to GND, output to `J10-5`/`J10-6` pin 1. Replaces the N-FET stages (`VIH` 2.5 V) |
| Driver fault | R | `FLT` wired-OR, 10 kΩ to 3V3 at GPIO9 |
| Rear TCRT ([rear-tcrt-lead.md](../../01-chassis/v1/research/rear-tcrt-lead.md)) | R 100 Ω (LED), Q1 AO3400A, R 100 kΩ gate pull-down, R 10 kΩ load (bench value), C 1 nF | As specified there; plus ≥ 1 kΩ series into GPIO8 (harness rule) |
| Nose (`J10-8`) | 10 µF + 0.1 µF on +5V; series ≥ 1 kΩ into GPIO1 and GPIO10; a defined bias on `HALL_OUT` | GP2Y `Vo` reaches 0.55 + 2.15 = **2.70 V maximum at 10 cm** and more nearer (abs. max `Vcc` + 0.3 V): divider or series resistor at lesson 2. An unplugged Hall line needs a pull (nose-hall-board.md review gate): 1 MΩ to GND reads an open wire as 0 V |
| Encoders | 33–100 Ω series on A/B; pull-up footprints | MOT3001 encoder runs on 3.3–5 V with digital outputs (vendor page). Output type unknown, so fit-optional pull-ups |
| IMU (`J10-7`) | 33–100 Ω series on SCLK, MOSI, MISO, CS | PCB-07 is HOLD |
| Inputs from other boards | ≥ 1 kΩ series and 100 kΩ pull-down on `MOTOR_PRESENT` | Fail-inactive; harness rule `PA-11.6` |
| Test points | Every rail, both link pairs, `WDI`, `WDO`, `C3_READY`, `SLP`, `FLT` | Not under the DevKitC: they would be unreachable once it is soldered |

**Supply.** 5 V comes in on `J10-1` (`PB-SAFE-BASE`, Micro-Fit 3.0, from PCB-04 `J4-4`). The 3.3 V logic comes from the DevKitC's own SGM2212-3.3 (800 mA).

| 3.3 V load | Current (`D` datasheet, `E` estimate) |
|---|---|
| THVD1451: quiescent 3 mA maximum, plus the driver into 120 Ω (about 2 V / 120 Ω) | ≈ 20 mA (`E`) |
| DRV5055 Hall (PCB-15) | 2 mA typical, 4 mA maximum at 3.3 V (`D`) |
| TCRT LED, pulsed at a few % duty | 20 mA peak (`E`) |
| Two encoders | `U`; about 10 mA each assumed |
| IMU, gates, watchdog | < 2 mA |
| **Carrier total** | ≈ 65 mA peak, well inside the LDO beside the ESP32-S3's own draw |

The GP2Y takes 30 mA average, 40 mA maximum (`D`) from the 5 V net.

**Every IC against its datasheet.**

| Ref | Part | Package | Pins (datasheet) | KiCad stock |
|---|---|---|---|---|
| U2 | THVD1451DR | SOIC-8 (D) | 1 VCC, 2 R, 3 D, 4 GND, 5 Y, 6 Z, 7 B, 8 A (Pin Functions, full-duplex devices) | Symbol `Interface_UART:THVD1451D`; footprint SOIC-8 |
| U2 alt. | THVD1451DRBR | VSON-8 (DRB) 3 × 3 | Same numbers, plus a thermal pad to GND | Footprint DFN-8-1EP 3×3 |
| U2 alt. | MAX3490EESA+ (ADI) | SOIC-8 | Same as THVD1451 D (industry-standard full-duplex pinout); 3.0–3.6 V, 12 Mbps, open-input fail-safe only | Symbol in `Interface_UART` |
| U3 | TPS3436CCCBGDDFRQ1 (D-068; CFDBE unobtainable) | SOT-23-8 thin (DDF) | Pinout C: 1 SET0, 2 MR, 3 WDI, 4 GND, 5 SET1, 6 WD-EN, 7 WDO, 8 VDD (Fig. 6-3, Table 6-1). VDD 1.04–6.0 V | **No symbol** (only TPS3430): a project symbol. Footprint `Texas_DDF0008A_SOT-8_1.6x2.9mm_P0.65mm` |
| U4 | SN74LVC1G08DBVR | SOT-23-5 | 1 A, 2 B, 3 GND, 4 Y, 5 VCC. `Ioff`: inputs safe unpowered | `74xGxx:74LVC1G08` |
| U5 | SN74LVC1G11DBVR | SOT-23-6 | 1 A, 2 GND, 3 B, 4 Y, 5 VCC, 6 C | `74xGxx:74LVC1G11` |
| Q1 | AO3400A | SOT-23 | 1 G, 2 S, 3 D; `VGS(th)` 1.45 V max | `Transistor_FET:AO3400A` |

Connectors: `JST_GH_BM0nB-GHS-TBT` (top entry) and `Molex_Micro-Fit_3.0_43650-0200_1x02_P3.00mm_Horizontal` are stock footprints. The DevKitC needs a project footprint (2 × 22 PTH, 2.54 mm pitch, rows 22.86 mm apart) and a v1.1 3D model built from the drawing.

### Connectors and who owns each pin order

Ten GH headers and one Micro-Fit, as in the CAD (`C3_GH_ROWS`): row Z 86 `J10-2`, `J10-5`, `J10-6`, `J10-8`; row Z 92 `J10-7`, `J10-3`, `J10-4`, `J10-10`, `J10-12`; `J10-1` right-angle on the +X edge. `J10-9` (merged into `J10-8`) and `J10-11` (D-041) do not exist.

| Conn. | Pins, 1 → n | Order owned by |
|---|---|---|
| `J10-1` (MF3 1×2) | +5V (`PB-SAFE-BASE`), GND | 05-harness §5.1 (D-039), mates PCB-04 `J4-4` |
| **`J10-2`** (GH6) | GND, `C0TX+`, `C0TX−`, `C3TX−`, `C3TX+`, spare (reordered at layout) | **Set here (below)**; PCB-09 `J9-2` follows |
| `J10-3`/`J10-4` (GH4) | GND, +3V3_ENC, ENC_A, ENC_B | 05-harness §5.2 (D-039); single-ended lead re-crimped on the motor |
| `J10-5`/`J10-6` (GH6) | SLP, IN1, IN2, FLT, GND, spare | power-boards §2.4 (fixed) |
| `J10-7` (GH8) | +3V3, GND, SCLK, MOSI, MISO, CS, INT1, INT2 | 05-harness §5.2; PCB-07 follows when it leaves HOLD |
| **`J10-8`** (GH5) | +5V, GND, GP2Y_VO, +3V3, HALL_OUT | **Set here (below)**; PCB-15 pads fixed (rev A) |
| **`J10-10`** (GH4) | LED_A, LED_K, TCRT_OUT, GND | **Set here (below)**; the TCRT lead follows |
| `J10-12` (GH4) | GND, C3_READY, MOTOR_PRESENT, GND | 05-harness §5.2, mates PCB-03 `J3-9` |

**`J10-2`, base link (set by PCB-10).** The harness table named the pairs `TX±`/`RX±` at both ends of one row, and that only works with a crossed cable. The pairs are named by direction instead, so the cable is straight:

| Pin | Net | At PCB-10 (THVD1451) | At PCB-09 `J9-2` |
|---:|---|---|---|
| 1 | GND | Signal reference | Signal reference |
| 2 | `C0TX+` | A (receiver) + 120 Ω | Y (driver) |
| 3 | `C0TX−` | B | Z |
| 4 | `C3TX−` | Z | B |
| 5 | `C3TX+` | Y (driver, non-inverting) | A (receiver) + 120 Ω |

**Reordered at layout (2026-10-28).** The first order (C3 pair on 2–3, C0 pair on 4–5) made the pairs cross between U2 and J2. This one is U2's own pin order seen from J2, so the four tracks run straight with no vias. The cable is still 1:1 and the pairs still adjacent, so nothing else changes.
| 6 | spare | Not connected | Not connected |

`W25` is wired 1:1 (pin n to pin n), with 2–3 and 4–5 twisted. Each pair sits next to the other, and GND is on pin 1, as 05-harness §5.2 asks. PCB-09's `J9-1` head link may use the same rule; that is PCB-09's to decide.

**`J10-8`, nose (set by PCB-10, unchanged).** 1 +5V, 2 GND, 3 GP2Y_VO, 4 +3V3, 5 HALL_OUT. Ends: GP2Y S3B-PH pins 1 Vo, 2 GND, 3 Vcc (datasheet) go to `J10-8` 3, 2, 1. PCB-15 P1 +3V3, P2 GND, P3 HALL_OUT go to 4, 2, 5. The GND conductor splits near the nose to both sensors. **Why keep this order:** +5V sits only beside GND, so a short or mis-crimp can't put 5 V on a 3.3 V ADC pin. The cost is that `HALL_OUT` sits beside its own +3V3 rather than GND, which is acceptable for a slow, filtered signal. The other orders tried put +5V beside an ADC input or GP2Y_VO (which carries LED-pulse noise) beside HALL_OUT.

**`J10-10`, rear TCRT (set by PCB-10, unchanged).** 1 LED_A, 2 LED_K, 3 TCRT_OUT, 4 GND, as rear-tcrt-lead.md wires the sensor (A, K, C, E). The LED current loop is on adjacent pins, `TCRT_OUT` is beside its return, and LED_A carries only the 100 Ω-limited 3.3 V.

### Envelope

Measured 2026-10-27 in the built body v1 CAD (`body_v1_model.py` with the legacy 0.4.28 runtime): carrier compound, frame, shell (and its 0–125 mm lowering path), panels, compute tray and hardware, mic boards, connector and harness reserves. The DevKitC and Pi STEPs are swept as boxes. None of the `final/v1/cad` droid edits touch this area. **F** is the +Y face (DevKitC, headers, plugs), **B** the −Y face toward the wall.

| Item | Value |
|---|---|
| Board | 70 × 43.5 × 1.6 mm in the CAD: X −14…56, Z 82…125.5, Y −58.4 (B) … −56.8 (F). **Grown to Z 76 (70 × 49.5), notched over the DRV8833 terminal block, at board set-up** (D-068 amended, *Board set-up*) |
| Mounting | Four M2.5 at (X, Z) (−8, 86), (−8, 116), (24, 86), (24, 116), into heat-set inserts in two printed uprights (X −12…−4 and 20…28, Y −66…−58.4, Z 69…126). Heads Ø4.5 × 1.8 on F |
| F, under the DevKitC | 2.5 mm to the DevKitC's bottom (header plastic). Between the header rows: X −9.9…46.4, Z 100.2…120.5 |
| F, under the module overhang | X 46.7…53, 4.15 mm to the module |
| F, GH band | Z 82…95.2; headers 4.2 mm tall, mated plugs to Y −49.4 (7.4 mm). Free corners: X −14…−4.5 (beside the screw at (−8, 86)) and X 48.5…56 below `J10-1` |
| F, beyond the plugs | Nothing in the board's X/Z span up to Y −40, except reserves: the Pi USB-C plug (X −6…6, Z 92–100, from Y −47.8, 1 mm off the DevKitC's top) and the harness drops |
| B, over the uprights | **0 mm**: the uprights bear on the board, X −12…−4 and 20…28, full height |
| B, elsewhere | 12.7 mm of air to the shell (Y −71.1), installed and while it is lowered. Nearest: FRONT_R mic screw heads at Y −69.0 (**10.6 mm**, X 52–56, Z ≥ 111) and the mic lead reserves at Y −69.3 (X 38–51.5, Z ≥ 116; X −14…−6, Z ≥ 106) |
| Top edge | **0.5 mm** under a frame lug (X 45.5…53.5, Z 126); no other frame in the board's Y band |
| Bottom edge | 12 mm to the lower rail (Z 70) |
| −X edge | 13 mm to the frame post (X −27, Y ≤ −58, outboard of the board). The USB service corridor (X −40…−11.5) is clear |
| +X edge | `J10-1` plug to X 68; the tray's front screw column at Y −45 is 1.8 mm above the plug |

**Height and area budget** (0.5 mm margin):

| Zone | Max part height | Area |
|---|---|---|
| F, under the DevKitC | **2.0 mm** (SOIC-8 1.75, SOT-23-5/6 1.45, DDF 1.1, 0603 0.95; screw heads 1.8). DevKitC bottom protrusions `U` | ≈ 56 × 20 mm. The circuit needs about 200 mm² of courtyards (five ICs at 12–35 mm² each, about 35 passives at 1–2 mm²), so it fits several times over |
| F, under the module | 3.6 mm | 6 × 18 mm |
| F, GH band | Free corners only | ≈ 9 × 13 and 7 × 3 mm |
| B, off the uprights | **10 mm** (set by FRONT_R's mic screw heads, 10.6 mm away) | The whole face less the two 8 mm strips |
| B, over the uprights | Nothing: no parts and no through-hole tails | 2 × (8 × 43.5) mm |

**Checks the CAD does not make, found here:**

- **DevKitC pin tails hit the uprights** (fixed by D-068). Neither model has header pins. A standard 2.54 mm header leaves about 6 mm of pin below the plastic, so 4 mm or more sticks out of B. Pins at X −8.49, −5.95 and −3.41 (upright 1) and 19.45, 21.99, 24.53 and 27.07 (upright 2) land on or at the edge of the uprights, in both rows: 14 joints.
- **The two upper screws are under the DevKitC** (fixed by D-068). The heads at Z 116 sit inside the DevKitC's outline (board Z 97.65–123.05, X −9.9…46.4). Once the DevKitC is soldered on, no driver reaches them, so the "one replaceable module" (`CN-06`) cannot be screwed in.
- **The real DevKitC differs from the CAD** (table above): narrower, with USB fronts 5.4 mm further −X.
- `HARNESS_REAR_TCRT_J10_10_RISE_TO_PLUG` (X 21–27) still lands at `J10-3`'s position; `J10-10` moved to X 37.75–46 in D-048. A harness-reserve label, not a board issue.

### Sourcing (2026-10-27)

| Part | India (element14 India counts, D-066) | LCSC / JLCPCB |
|---|---|---|
| THVD1451DR (SOIC-8) | **None**: element14 India does not list the THVD1451 family. Evelta not readable | C2671319, **0 stock** (pre-order, about US$1.79) |
| THVD1451DRBR (VSON-8) | None | **C2671344, 14,379 in stock**, US$2.69 each (extended) |
| MAX3490EESA+ (SOIC-8, pin-compatible) | **element14 India 2518822**, ₹1,002 each (stock not shown) | — |
| TPS3436CFDBEDDFRQ1 | **None** in India; TI store out of stock; **Mouser 0** | **None** at LCSC or JLCPCB |
| **TPS3436CCCBGDDFRQ1 (chosen, D-068)** | **Mouser India** (595-S3436CCCBGDDFRQ1): 1,710 in stock, US$3.25 each, billed in INR by Mouser Electronics (India). DDP (Mouser pays duty) on a GST business invoice; FCA (duty and GST at delivery) on a standard invoice. DigiKey (8,239) does not ship to India (builder) | None |
| SN74LVC1G08DBVR | element14 India 3120596, 4,892 (UK stock), ₹11.70 | C7666, 208,992 |
| SN74LVC1G11DBVR | element14 India 3006613, 1,008 (UK stock), ₹31.20 | C22046, 9,895 |
| AO3400A | Common (Robu and others); not checked by part number | C20917 (basic part) |
| ESP32-S3-DevKitC-1-N8, genuine Espressif v1.1 (D-068) | Tech Depot ₹2,273.70 (GST invoice, in stock), Sharvi ₹1,678.45 + GST, Compoindia ₹2,410 + GST. element14 India does not list it | — |

India-held window watchdogs on element14 (TPS3813K33, MAX6323) have windows of hundreds of ms, against `BD-10`'s 44 ms late-fault limit. They are not drop-ins.

### Gaps

**Decided by [D-068](../../decisions.md#d-068)** (2026-10-27):

1. **Mounting: two screws and two hooks.** The upper screws are deleted. Each upright gets a hook over the board's top edge and a relief under both header rows (CAD in `final/v1/cad`, measured by `check_pcb10_mount.py`). The module goes in 2 mm low, slides up under the hooks, and the two Z 86 screws fix it. Pin tails are clipped to 1.5 mm. It goes on before the compute tray; with the tray in there is still 17 mm of driver reach for service.
2. **Watchdog: TPS3436CCCBGDDFRQ1** from Mouser India (the `BD-10` fallback; same pinout and footprint). Feed every 10 ms; first edge within 500 ms of power-up. PCB-12 takes the same part.
3. **Link transceiver: SOIC-8 footprint** for THVD1451DR (Mouser India) or MAX3490EESA+ (element14 India), with the MAX3490's idle-bias footprints fitted only with it.
4. **USB back-feed: Schottky** from `J10-1` to the DevKitC 5V pin.

**Adopted with D-068 (values at lesson 2):**

5. GPIO map v0.2: `HALL_OUT` on GPIO10, `TCRT_LED_EN` on GPIO47, IMU `INT2` not connected, GPIO38 left to the v1.1 LED. Superseded at layout by v0.3 (*GPIO map*).
6. `J10-2`, `J10-8`, `J10-10` orders above. Recorded at PCB-09 and in 05-harness §5.2.
7. `MR`: no safety-converter power-good reaches C3 (`PG_BASE` goes to PCB-02 on `W20`). Pull `MR` up to 3V3 (its test point was dropped at layout: a static pull-up). The watchdog then starts with the DevKitC's 3.3 V.
8. GP2Y bypass: Sharp asks for ≥ 10 µF "near this product", but its end of `W34` is wires soldered to the S3B-PH pins (D-027). Its LED pulses return on the same GND wire as the Hall, which offsets the Hall reading (`E`: a 300 mA pulse × about 75 mΩ of AWG30 ≈ 22 mV ≈ 1.5 mT, an eighth of the 12 mT trip). Proposed: 10 µF at `J10-8` on PCB-10, a 10 µF 0805 tacked across the S3B-PH pins, and Hall sampling between GP2Y pulses. Bench item 19 measures it.
9. GP2Y `Vo` scaling into GPIO1 (series resistor or divider), and the `HALL_OUT` open-wire pull (1 MΩ to GND): values at lesson 2.
10. `JP_SVC` must be reachable with the module fitted, so not under the DevKitC: a 2-pin header or solder jumper in the GH band's free corner.
11. DevKitC revision: confirm v1.1 (GPIO38 LED) on the received board and measure the bottom-side protrusions (USB shell legs, header joints) against the 2.0 mm under-board limit.
12. CAD: the body source keeps the clone DevKitC and four screws (subsystem sources are not edited); the final CAD replaces them (D-068 `DROID_REMOVES`/`DROID_INSERTS`). Espressif's footprint (`espressif/kicad-libraries`, `ESP32-S3-DevKitC`) is the DevKitC footprint, with the drill opened to about 1.0 mm for 0.64 mm square pins.
13. **Stage 3 harness:** the v1.1 board's UART USB-C touches `HARNESS_HEAD_RISER_LOWER` (0.5 × 0.6 mm), and that reserve already crosses the USB service corridor. Re-route the head riser.

## Schematic

[`design/pcb-10-c3-carrier.kicad_sch`](design/pcb-10-c3-carrier.kicad_sch), with a PDF print, [`pcb-10-c3-carrier-schematic.pdf`](design/pcb-10-c3-carrier-schematic.pdf). One A2 sheet, written for the KiCad 10.99 nightly. As on PCB-05, every pin end carries a short wire and a local label, and nets join by label name; the notes are in one column at the right.

**Project set-up.**

| File | Holds |
|---|---|
| `pcb-10-c3-carrier.kicad_pro` | PCB-06's project, renamed: the fab-neutral board minimums and default net class |
| `pcb-10-c3-carrier.kicad_dru` | The fab-neutral rules ([D-062](../../decisions.md#d-062)), copied from PCB-15 |
| `sym-lib-table`, `pcb10.kicad_sym` | Project symbol library `pcb10`. **`ESP32-S3-DevKitC`** is Espressif's own symbol (`espressif/kicad-libraries`, `Espressif.kicad_sym`), with only its footprint field changed. Pads 1–22 are J1 pins 1–22; pads 23–44 are J3 pins 22–1 (pad *n* = J3 pin 45 − *n*), as Espressif's footprint numbers them. **`TPS3436CCCBGDDFRQ1`** is new (KiCad has only the TPS3430): pinout C from SLVSGF1A Fig. 6-3 and Table 6-1, `WDO` typed open collector. **`AO3400A`** is KiCad's `Q_NMOS_GSD` body with AO3400A's fields: the stock AO3400A is a derived symbol (the playbook's ERC library-mismatch trap) |
| `fp-lib-table`, `pcb10.pretty/` | **`ESP32-S3-DevKitC-1_v1.1_1.0mm`**: Espressif's `ESP32-S3-DevKitC` pad positions (2 × 22 at 2.54 mm, rows 22.86 mm apart), with holes opened from 0.8 to **1.0 mm** for the pre-soldered 0.64 mm square pins (0.9 mm diagonal) and pads grown to 1.7 × 2.0 mm (0.35 mm ring). F.Fab draws the v1.1 board and module from Espressif's drawing. The courtyard covers only the two header-plastic rows, because parts may sit in the 2.5 mm gap under the board; lesson 3 sets that height limit as a rule area |
| Stock parts | THVD1451D (`Interface_UART`), 74LVC1G08 and 74LVC1G11 (`74xGxx`), all checked against the datasheet pinouts in *Inputs*; JST GH `BM0nB-GHS-TBT` top entry; Molex `43650-0200` right angle; SOD-123, SOT-23/-5/-6, `Texas_DDF0008A`, SOIC-8; 0402/0603/0805 passives; `TestPoint_Pad_D1.0mm`; `MountingHole_2.7mm_M2.5`; 2.00 mm 1 × 2 header for `JP_SVC` |

KiCad ships no 3D model for the DDF package (`Texas_DDF0008A…`) or the Micro-Fit, and none exists for the DevKitC. They get project models at lesson 5, so the board STEP shows them (the PCB-11 trap).

**Circuit** (references as drawn):

| Ref | Part | Nets |
|---|---|---|
| U1 | Espressif ESP32-S3-DevKitC-1-N8 v1.1 (CH-045) | GPIO map v0.3 (set at layout). 3V3 (pads 1, 2) is the carrier's `+3V3`; 5V (21) on `+5V_DK`; RST/EN (3) on `WDO`; G (22, 23, 24, 44). Unused pads 13, 14, 25, 26, 30, 31, 32, 35, 36, 37, 42, 43 carry no-connect flags. Not in the position file: hand-soldered after PCBA, tails clipped to 1.5 mm |
| J1 (`J10-1`) | Molex 43650-0200, W11 | 1 `+5V_IN`, 2 GND |
| D1 | B5819W Schottky, SOD-123 (LCSC C8598) | `+5V_IN` → `+5V_DK` (D-068 E) |
| C1, C2 / C3, C4 | 10 µF 0805 + 100 nF | `+5V_IN` / `+3V3` bulk |
| U3 | TPS3436CCCBGDDFRQ1 | `WDI` (3) ← GPIO48, `MR` (2), `WD_EN` (6), SET0 (1) and SET1 (5) to GND, `WDO` (7), VDD (8) `+3V3`; C5 100 nF |
| R1–R4 | 10 kΩ | Pull-ups on `WDI`, `WDO`, `WD_EN`, `MR` (board-specs §7; `MR` per gap 7) |
| JP1 | 2.00 mm 1 × 2 header | `JP_SVC`: `WD_EN` to GND = watchdog off and READY low |
| U5 | 74LVC1G11 | `READY` = `WDO` (A) ∧ `WD_EN` (B) ∧ `MCU_RDY` (C); C6 100 nF; R5 10 kΩ pull-down on `MCU_RDY` (GPIO2) |
| R6 | 1 kΩ | `READY` → `C3_READY` (`J10-12` pin 2) |
| U4 | 74LVC1G08 | `SLP` = `NSLEEP` (GPIO21) ∧ `READY`; C7 100 nF; R7, R8 100 kΩ pull-downs on both inputs (power-boards §2.4) |
| R9, R10 | 1 kΩ | `SLP` → `SLP_L` (`J10-5` pin 1), `SLP_R` (`J10-6` pin 1) |
| J5, J6 (`J10-5/6`) | BM06B-GHS-TBT | 1 SLP, 2 IN1, 3 IN2, 4 `FLT`, 5 GND, 6 no connect |
| R11–R14 | 100 Ω | GPIO11/12 → `IN1_L/R`, GPIO13/14 → `IN2_L/R` |
| R15, R16 | 10 kΩ, 1 kΩ | `FLT` pull-up; `FLT` → `NFAULT` (GPIO9) |
| J2 (`J10-2`) | BM06B-GHS-TBT | 1 GND, 2 `C0TX_P`, 3 `C0TX_N`, 4 `C3TX_N`, 5 `C3TX_P`, 6 no connect (reordered at layout) |
| U2 | THVD1451DR (alternate MAX3490EESA+) | D (3) ← `UART_TX` GPIO17, R (2) → `UART_RX` GPIO18, Y/Z (5/6) → `C3TX_P/N`, A/B (8/7) ← `C0TX_P/N`; C8 100 nF |
| R17 | 120 Ω | Across `C0TX_P/N`: this end's receiver termination |
| R18, R19 | 560 Ω, DNP | Idle bias `C0TX_P` to 3V3 and `C0TX_N` to GND, fitted only with the MAX3490 (about 0.32 V across 120 Ω) |
| J3, J4 (`J10-3/4`) | BM04B-GHS-TBT | 1 GND, 2 `+3V3`, 3 A, 4 B |
| R20–R23; R24–R27 | 100 Ω; 10 kΩ DNP | Encoder series into GPIO4–7; pull-ups to 3V3 until the encoder output type is known |
| J7 (`J10-7`) | BM08B-GHS-TBT | 1 `+3V3`, 2 GND, 3 SCLK, 4 MOSI, 5 MISO, 6 CS, 7 INT1, 8 (INT2) no connect |
| R28–R31; R32; R33 | 33 Ω; 1 kΩ; 10 kΩ | SPI series (GPIO37, 35, 36, 41); INT1 into GPIO42; CS pull-up so the IMU is deselected at boot |
| J10 (`J10-10`) | BM04B-GHS-TBT | 1 `LED_A`, 2 `LED_K`, 3 `TCRT_OUT`, 4 GND |
| R34, Q1, R35 | 100 Ω 0603, AO3400A, 100 kΩ | LED from 3V3, low-side switch on GPIO47, gate pull-down (rear-tcrt-lead.md R1, Q1, R3) |
| R36, C9, R37 | 10 kΩ 0603 (bench value), 1 nF, 1 kΩ | `TCRT_OUT` load and fail-safe pull-up (R2), ADC filter (C3), series into GPIO8 |
| J8 (`J10-8`) | BM05B-GHS-TBT | 1 `+5V_IN`, 2 GND, 3 `GP2Y_VO`, 4 `+3V3`, 5 `HALL_OUT` |
| C10 | 10 µF 0805 | `+5V_IN` at J8 pin 1 (GP2Y bypass, gap 8) |
| R38, R39, C11 | 10 kΩ, 22 kΩ, 100 nF | `GP2Y_VO` → `GP2Y_ADC` (GPIO1): × 0.69, so 2.70 V at 10 cm reads 1.86 V and a 5 V fault 3.44 V (under the S3's 3.6 V). The GP2Y updates every ~38 ms, so the 0.7 ms filter costs nothing (gap 9) |
| R40, R41, C12 | 1 MΩ, 1 kΩ, 1 nF | `HALL_OUT` open-wire pull-down (reads 0 V = fault), series and sample cap into GPIO10 (gap 9) |
| J12 (`J10-12`) | BM04B-GHS-TBT | 1 GND, 2 `C3_READY`, 3 `MOTOR_PRESENT`, 4 GND |
| R42, R43 | 1 kΩ, 100 kΩ | `MOTOR_PRESENT` series into GPIO40, pull-down (fail-inactive) |
| TP1–TP4, TP9–TP12 | Ø1.0 pads, not in the BOM | `+5V_IN`, `+5V_DK`, `+3V3`, GND, `WDI`, `WDO`, `C3_READY`, `SLP`. Placed outside the DevKitC's shadow (lesson 1). Cut at layout (2026-10-28) from 15: the RS-422 pairs are probed on U2's pins, FLT on R16, WD_EN on JP1; MR is a static pull-up; TP11 moved from `READY` to `C3_READY`, the signal PCB-03 actually sees |
| H1, H2 | Ø2.7 mm holes | The two lower M2.5 screws (D-068 A); no net |

`PWR_FLAG` sits on `+5V_IN` (enters on J1), `+5V_DK` (the diode's output), `+3V3` (the DevKitC's regulator, whose pins Espressif types as power inputs) and GND. Unfitted parts carry KiCad's DNP flag.

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-28): **0 errors, 0 warnings.**

**Check against the inputs**, row by row, from the exported netlist:

| Input (lesson 1, D-068) | Netlist | Result |
|---|---|---|
| GPIO map v0.3 (re-checked after each layout change) | `TCRT_LED_EN` U1.4, `TCRT_ADC` U1.5, `ENC_R_A/B` U1.6/7, `ENC_L_A/B` U1.8/9, `MOTOR_PRESENT_MCU` U1.10, `NFAULT` U1.11, `IMU_SCLK_MCU` U1.12, `IMU_MOSI/MISO/CS/INT1_MCU` U1.15–18, `UART_RX/TX` U1.19/20, `NSLEEP` U1.27, `MCU_RDY` U1.28, `WDI` U1.29, `IN2_L/IN1_L_MCU` U1.33/34, `IN2_R/IN1_R_MCU` U1.38/39, `HALL_ADC` U1.40, `GP2Y_ADC` U1.41 | Match |
| Unused pins open | U1 8, 9, 13, 14, 25, 26, 30, 31, 35, 36, 42, 43 unconnected (GPIO15, 16, 3, 46, 19, 20, 45, 0, 38, 39, 44, 43) | Match |
| 5 V in, back-feed diode | `+5V_IN`: J1.1, D1.2 (A), C1, C2, C10, J8.1, TP1. `+5V_DK`: D1.1 (K), U1.21, TP2 | Match |
| Watchdog pinout C, SET 00 | `WDI` U3.3, R1, U1.29, TP9. `WDO` U3.7, R2, U1.3 (EN), U5.1, TP10. `WD_EN` U3.6, R3, JP1.1, U5.3. `MR` U3.2, R4. U3.1, U3.5, U3.4 on GND | Match |
| READY = WDO ∧ WD-EN ∧ MCU_RDY; 1k out | `MCU_RDY` U5.6, R5, U1.40. `READY` U5.4, R6, R8, U4.2. `C3_READY` R6, J12.2, TP11 | Match |
| SLP = NSLEEP ∧ READY, pulled down | `NSLEEP` U1.27, R7, U4.1. `SLP` U4.4, R9, R10, TP12 → `SLP_L` J5.1, `SLP_R` J6.1 | Match |
| `FLT` wired-OR, 10k pull-up, GPIO9 | `FLT` J5.4, J6.4, R15, R16. `NFAULT` R16, U1.15 | Match |
| `J10-2` by direction, 120 Ω at this receiver | `C3TX_P/N` U2.5/6 → J2.5/4. `C0TX_P/N` J2.2/3 → U2.8/7, R17 across, R18/R19 (DNP). J2.6 open (order as reordered at layout) | Match |
| `J10-8` order; nose circuits | J8.1 `+5V_IN`, J8.2 GND, J8.3 `GP2Y_VO` → R38 → `GP2Y_ADC` (R39, C11), J8.4 `+3V3`, J8.5 `HALL_OUT` (R40) → R41 → `HALL_ADC` (C12) | Match |
| `J10-10` order; TCRT circuit | J10.1 `LED_A` ← R34 ← `+3V3`. J10.2 `LED_K` → Q1.3 (D); Q1.1 (G) `TCRT_LED_EN` with R35; Q1.2 (S) GND. J10.3 `TCRT_OUT` R36, C9, R37 → `TCRT_ADC` | Match |
| `J10-3/4`, `J10-5/6`, `J10-7`, `J10-12` orders | J3/J4 1 GND, 2 `+3V3`, 3 A, 4 B. J5/J6 1 SLP, 2 IN1, 3 IN2, 4 FLT, 5 GND, 6 open. J7 1 `+3V3`, 2 GND, 3–7 SCLK, MOSI, MISO, CS, INT1, 8 open. J12 1 GND, 2 `C3_READY`, 3 `MOTOR_PRESENT`, 4 GND | Match |
| One ground; every GH mounting pad on GND | `GND`: U1.22/23/24/44, U2–U5 grounds, J1.2, every J pin and MP named GND, JP1.2, Q1.2, all pull-downs and capacitors | Match |
| `+3V3` from the DevKitC | `+3V3`: U1.1/2, U2–U5 VCC, C3–C8, J3.2, J4.2, J7.1, J8.4, all pull-ups, R34, R36, TP3 | Match |
| Fixings no net | H1, H2 have no pins | Match |

## Board set-up

[`design/pcb-10-c3-carrier.kicad_pcb`](design/pcb-10-c3-carrier.kicad_pcb), no parts yet (they arrive with F8 at lesson 4).

**Coordinates.** The board is seen from its F face, the DevKitC side, which faces the robot's inside (world +Y). World +X is then to the left. KiCad x = 156 − X, y = 225.5 − Z. Board-local xb = x − 100 (= 56 − X) and yb = 149.5 − y (= Z − 76), with the aux and grid origins at local (0, 0), the bottom-left corner in KiCad's view. KiCad's STEP puts the F face at +Z, which becomes world +Y.

**The connectors didn't fit: [D-068](../../decisions.md#d-068) amended.** Placed at the CAD positions on a scratch board, the real footprints gave **23 courtyard overlaps** in KiCad DRC:
- the CAD's two GH rows are 6 mm apart, but a GH courtyard is 6.6 mm deep;
- neighbours in each row overlap by 0.2–0.7 mm;
- the real Micro-Fit (9.65 × 9.9 mm, Molex SD-43650-001) lands on `J10-8`, `J10-10` and `J10-12`, where the CAD had a 7.26 mm block.

It is the PCB-05 lesson again: placeholder bodies are not footprints. Fixes:

- **The board grows 6 mm down, to Z 76** (70 × 49.5 mm), for a third connector row. Courtyard bands: A Z 89.85–96.45 (`J10-7`, `J10-3`, `J10-4`, `J10-10`), B 83.15–89.75 with the two screws (`J10-2`, `J10-5`, `J10-6`), C 76.3–82.9 (`J10-12`, `J10-8`). `J10-1`, still the right-angle Micro-Fit mating +X at the front edge, spans B and C.
- **Notched over the right DRV8833's terminal block** (chassis; X 43.5–50.5, top Z 76.1, 0.11 mm in front of the board plane), which the first try ran into in the 2 mm-low install position: the bottom edge steps up to Z 79 over X 42.5–51, `J10-1` rises 1.8 mm (housing Z 78.6–88.26) and `J10-8`/`J10-12` move about 2 mm toward −X.
- The scratch-board DRC of the final arrangement: **no courtyard, edge or copper violations** (only the scratch board's library-link and silkscreen-thickness flags).
- The CAD follows in `final/v1/cad` (`PCB10_GH`, `PCB10_J10_1`, `PCB10_BOARD_GROWTH`; `DROID_ADDS`, `DROID_MOVES`, `DROID_REMOVES`/`INSERTS`). **`check_pcb10_mount.py`: 9/9 pass**, including the grown board 0.52 mm from the terminal block, `J10-1` 0.7 mm above it, the slide and approach clear, and the screws reachable.

| Connector | Footprint origin (KiCad) | Rot. | Courtyard band |
|---|---|---|---|
| `J10-7` BM08B | (142.87, 132.35) | 0 | A |
| `J10-3`, `J10-4`, `J10-10` BM04B | (130.81 / 121.27 / 111.71, 132.35) | 0 | A |
| `J10-2`, `J10-5`, `J10-6` BM06B | (154.97 / 142.91 / 122.97, 139.05) | 0 | B |
| `J10-12` BM04B, `J10-8` BM05B | (130.0 / 119.0, 145.9) | 0 | C |
| `J10-1` Micro-Fit 43650-0200 | (108.92, 143.57) | 90 | B + C, mates +X |
| H1, H2 M2.5 | (164.0 / 132.0, 139.5) | — | B |
| U1 DevKitC | pad 1 at (111.147, 126.58) | 90 | J1 row low, J3 high |

**Set-up.**

| Item | Value |
|---|---|
| Outline | `Edge.Cuts` polygon: x 100–170, y 100–149.5, notch x 105–113.5 up to y 146.5 |
| Stackup | **4 layers since placement** (D-068 amended; see *Layout*): PCB-05's, 1.6 mm, 1 oz outer, 0.5 oz inner. Set up first as PCB-06's 2 layers |
| Rules | `pcb-10-c3-carrier.kicad_dru`: the fab-neutral set, copied from PCB-15 |
| `UPRIGHT_1/2_B_NO_PARTS` | B.Cu rule areas over the printed uprights (x 160–168 and 128–136, full height): no footprints. Pads stay allowed: the DevKitC's pins go into the uprights' header-row reliefs, and the screws go through |
| `HOOK_1/2_F_NO_PARTS` | F.Cu rule areas under the hooks' lips (same x, Z 123.6 to the top edge): no footprints, no pads |
| User.1 `Connectors.Placed` | The proved connector courtyards and screw holes, with each footprint's origin, to place against at lesson 4 |
| User.2 `DevKitC.Shadow` | The v1.1 board and the module overhang: **parts under it ≤ 2.0 mm, no test points**. KiCad has no height rule; the lesson 5 fit check measures it |
| User.3 `Frame.Uprights` | Uprights, hooks and the header-row reliefs |
| User.4 `Back.Ceiling` | 10 mm of air behind the board; the Micro-Fit's 1.6 mm tails and 3.3 mm peg come through |
| User.5 `Edges` | The frame lug 0.5 mm above the top edge; the notch; `J10-1` mating at the +X edge |

**DRC** (nightly `kicad-cli pcb drc --severity-all`, 2026-10-28): empty board **0 violations**. **Rule areas proved** on a scratch copy with its own `.kicad_pro`/`.kicad_dru` (the PCB-06 trap): an 0402 on B over upright 1 is flagged (`UPRIGHT_1_B_NO_PARTS`); one under hook 2 is flagged with both pads (`HOOK_2_F_NO_PARTS`); one in open space is not; a 0.12 mm track is flagged by the custom rule (`fab-neutral track width`).

**3D models** (the gap from lesson 2):

| Part | Model | Check |
|---|---|---|
| U3 TPS3436 (DDF0008A) | Project footprint `pcb10:Texas_DDF0008A_SOT-8_1.6x2.9mm_P0.65mm`: the stock land pattern pointing at KiCad's `TSOT-23-8.step` (KiCad ships none for DDF0008A) | Against TI drawing 4222047/E: body 2.86 (2.85–2.95), width about 1.5–1.6 (1.55–1.65), lead span 2.80 (2.65–2.95), leads 0.30 (0.22–0.38), pitch 0.65. Height 0.95 against TI's **1.1 max**: the fit check uses 1.1. Leads land at ±1.225 mm inside the ±1.3 mm pads in a scratch STEP |
| J10-1 Micro-Fit 43650-0200 | Project footprint `pcb10:Molex_Micro-Fit_3.0_43650-0200_1x02_P3.00mm_Horizontal` with `pcb10.3dshapes/Molex_Micro-Fit_3.0_43650-0200_full_tails.step`, built from Molex SD-43650-001: housing 9.65 × 9.90 × 6.98 (solid), 0.64 mm pins with the full **3.18 mm tails** (not clipped as on PCB-05: 10 mm of air behind this board), Ø3 peg 3.3 mm long (`E`, drawing text) | In a scratch STEP the pins sit on both pads, the peg on its hole, and the housing on the footprint's fab outline |
| U1 DevKitC | `pcb10.3dshapes/ESP32-S3-DevKitC-1_v1.1.step`, built at lesson 5 from `pcb10_devkitc()`, the same code as the robot CAD, moved into the footprint frame: (X, Y, Z) → (Z − 98.92, X − 44.853, Y + 56.8), pad 1 at the origin | Its pins land on pads 1–22 at x 0 and 23–44 at x 22.86; the fit check finds it on the CAD's DevKitC to 0.000 mm |

## Layout

### Four layers (decision at placement)

On two layers PCB-10 would not route. Under the DevKitC, every net from the top header row (motor IN lines, GP2Y, Hall, watchdog) has to cross every net from the bottom row on its way down to the connector rows, and each THT gap is 0.54 mm wide, room for one 0.2 mm track per layer. That leaves no room for ground. **Taken 2026-10-28 by the builder: four layers** ([D-068](../../decisions.md#d-068) amended): F.Cu parts and signals, In1.Cu solid GND (`GND_IN1`), In2.Cu the +3V3 plane (`P3V3_IN2`), B.Cu signals with no parts. It's PCB-05's stackup: 1.6 mm, 35 µm outer and 15 µm inner copper.

**Placement** (KiPy, KiCad coordinates; connectors, holes and U1 as in *Board set-up*):

| Group | Parts and positions | Why there |
|---|---|---|
| Bottom-row band | One series resistor flat over each DevKitC pin it serves, at y 124.4 (R37, R22, R23, R20, R21, R42, R16, R28–R32); pull-ups and pull-downs above them at y 122.6 (R24–R27, R43, R15, R33) | Each MCU end drops straight onto its pin, and each connector end leaves through the gap beside it. This is what GPIO map v0.3 is built around |
| Top-row band | R38, R41, R12, R14, R11, R13, R7 at y 105.8; C11, R39, C12, R40 below | The same idea for the top row |
| TCRT | R34 (112.42, 118.0), Q1 (117.9, 120.5), R35, R36, C9 by pins 1–5 | The LED switch and the receiver load sit next to the pins and J10-10 |
| Watchdog and READY gate | U3 (148, 114), U5 (154, 114), U4 (160.6, 114) left to right in signal order, with C5–C7 above, R4 (MR), R1/R5/R7 under pins 29/28/27, R8 and R6 below | WDO → U5 → U4 → SLP flows left to right; nothing doubles back |
| Supply | D1, C1, C2, C10 and TP1 by `J10-1`; C3/C4 on DevKitC pins 1/2 | |
| RS-422 | U2 (160, 146.1) 180° under `J10-2`; R17 across the C0 pair; R18/R19 (DNP bias) beside them | U2's bus pins face `J10-2` in its own order (which is why `J10-2` was reordered) |
| Test points | TP1–TP4 (rails) on the left edge, TP9 (WDI) above the top row, TP10 (WDO) left edge, TP11 (C3_READY), TP12 (SLP) on their tracks below the DevKitC, JP1 + R3 (WD_EN) right | Nothing to probe under the DevKitC. RS-422 is probed on U2's SOIC pins, FLT on R16 or `J10-5` pin 4. TP5–TP8 and TP13–TP15 were dropped |

### Routing (lesson 4)

Routed by hand through KiPy, 2026-10-28; every segment 0°, 45° or 90° (D-060). Track widths: 0.2 mm signals, 0.25 mm ground and +3V3 stubs, 0.4 mm the DevKitC 3V3 pins, 0.5 mm `+5V_IN`, 0.8 mm `+5V_DK`.

| Layer | Carries |
|---|---|
| F.Cu | All parts. The bottom-row band (each resistor's drop onto its pin, then down its gap to the connector), the encoder, TCRT and IMU fans into row A, the FLT channel at y 135.7 between rows A and B, `SLP_R`'s channel at y 142.45 between rows B and C, the watchdog cluster, RS-422 from U2 to `J10-2`, `+5V_IN` |
| In1.Cu | **Solid GND, no tracks.** One polygon over the whole board |
| In2.Cu | +3V3 plane, plus three slow, static nets as tracks: `WDO` (y 112.25 across under the DevKitC, then down to pin 3), `C3_READY` (TP11 → `J10-12` pin 2) and `SLP` (TP12 → R9/R10). The plane still fills as one polygon |
| B.Cu | The six top-row descents (GP2Y_VO, HALL_OUT, IN1/2_R, IN1/2_L), each in its own gap; `WDI`, `NSLEEP`, `WD_EN`; UART RX/TX from pins 19/20 under U2; `MOTOR_PRESENT` to row C; `+5V_DK` round the top and left edges to D1 |

**What this board teaches** (new since PCB-05):

- **Use each layer for what it's good at.** Ground is one unbroken plane (In1), so every ground pad, shell pad and decoupler gets its own via straight into it, and every signal on F has its return path directly underneath. The +3V3 plane can carry a few tracks, but only for nets that change rarely (a watchdog output, a readiness flag, a sleep line). Each track cuts a slot in the plane, but these nets carry almost no edges, and the plane stays joined around both ends of every slot. The fast nets (SPI at 33 Ω, UART, RS-422) stay on F/B over the solid ground.
- **THT header rows are fences.** The DevKitC's two rows are 22 pins each at 2.54 mm pitch with 2.0 mm pads, so each gap holds one 0.2 mm track per layer. The pin map (v0.3) and the resistor positions were chosen together so that each gap carries at most one net on F and one on B, and no two nets need the same gap.
- **Order is a topology problem.** Where two nets have to swap left-right order between their source and their connector, they must cross, and a crossing costs a via. Three of these were solved by moving parts instead: `J10-2` reordered to U2's pin order, so the pairs never cross; the IMU staircase, where the net that shifts furthest turns first; and TCRT, where `LED_K` and `TCRT_OUT` run as nested 45° lines past `J10-10`'s shell pad (0.28 mm clearance at the corner). Where a crossing can't be avoided (C3_READY and MOTOR_PRESENT both heading for `J10-12`), one net changes layer.
- **Power takes the long way when the short way is full.** `+5V_DK` (D1 → DevKitC 5V pin, up to about 0.5 A) has no room through the middle, so it runs on B round the board edges: about 190 mm at 0.8 mm, roughly 0.12 Ω, so 60 mV at 0.5 A. The DevKitC's 3.3 V regulator has plenty of headroom after D1's 0.4 V.
- **Via spacing is copper to copper.** A via (Ø0.67) next to a 0.2 mm track needs its centre 0.745 mm from the track's centreline (0.335 + 0.31 + 0.1). That is why most plane vias sit off-axis from their pads: they had to clear a B or In2 line running under them.

Totals: 610 mm of track on F.Cu, 121 mm on In2, 469 mm on B.Cu; 96 vias, all 0.67/0.35.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, fab-neutral `.kicad_dru`, 2026-10-28): **0 errors, 0 unconnected pads, 0 schematic-parity issues**, no keep-out, courtyard or clearance hits, first time through. Both planes refilled before the check and fill as one polygon each. What remains:
- 57 `lib_footprint_mismatch` warnings, the 1 nm round-off on parts that were turned during placement;
- 4 `silk_edge_clearance` warnings on J1's housing outline, which overhangs the +X edge by design so the plug can mate (the fab clips silkscreen at the edge).

Reference labels are on the fab layers (`refs_to_fab()`). `audit()`: every part has its 3D model except U1, whose model is built at lesson 5. TP1–TP4 and TP9–TP12 are out of the BOM and position file, and so is U1 (the DevKitC is hand-soldered after assembly, not placed by the fab).

## Checks and outputs (rev A)

- **ERC** 0 errors, 0 warnings. **DRC** with schematic parity: 0 errors, 0 unconnected, plus the cosmetic warnings explained under Routing. **`audit()`**: every part that is placed has its 3D model, U1 included; TP1–TP4, TP9–TP12 and the holes are out of the position file.
- **DevKitC model:** built from `pcb10_devkitc()` in `final/v1/cad/makad-v1.step.py`, so the board STEP and the robot CAD can't disagree about the DevKitC. Only a rotation and a shift into the footprint's frame (pad 1 at the origin, Z up from the F face) separate the two.
- **Board STEP:** [`cad/pcb-10-c3-carrier-revA.step`](cad/pcb-10-c3-carrier-revA.step) (`--user-origin 0x0mm`): the board and all 73 modelled parts, unfitted ones included (the worst case for fit). The core runs Z 0–1.516, and parts sit 0.04 mm proud of the copper.
- **Outputs:** [`fab/revA/`](fab/revA/README.md): Gerber X2 for the four copper layers, both masks, front paste and silkscreen; Excellon drill (plated: 96 vias, the DevKitC's 44 holes, JP1, the Micro-Fit; non-plated: the two screw holes and the Micro-Fit's peg); the BOM and placement (66 parts each, U1 and the unfitted parts out) in KiCad and JLCPCB CPL formats; a Gerber zip and the order parameters. Everything is from the board-local origin, and vias are tented both sides.
- **Fit in the robot:** [`final/v1/cad/check_pcb10_fit.py`](../../final/v1/cad/check_pcb10_fit.py) places the STEP where the droid CAD has the carrier (droid edits applied) and measures the real parts against the chassis and body (about 6 min). **PASS, 7/7:**

  | Check | Result |
  |---|---|
  | Board | Core on the CAD board to 0.000 mm, F face at Y −56.800; area 3383.8 mm² plus 55.7 of drilled holes against the CAD's 3439.5, so the notch matches |
  | DevKitC | On the CAD's DevKitC to 0.000 mm, 0.043 higher (KiCad's part offset); pin tails to Y −59.86 |
  | Connectors | All ten (`J10-1` … `J10-12`) on the CAD headers to 0.00 mm, tops 0.04 higher, so the CAD's mated plugs and harness reserves stand as drawn |
  | Under the DevKitC | 49 parts. Tallest by datasheet: U4/U5 (SOT-23-5/6) **1.45 max** (KiCad's models 1.59), C1/C3 0805 1.45, Q1 1.45; U3 TPS3436 1.10. All ≤ 2.0 (D-068 B), so at least **0.91 mm** to the DevKitC's underside even with KiCad's tall models. The nearest model to the DevKitC itself is 0.56 mm away |
  | Clear of the droid | Nearest: the board edge **0.50** to the frame; the notch **0.53** to the right DRV8833's terminal block; `J10-8` 1.74 to it; D1 2.00 to the compute tray |
  | Behind the board | Micro-Fit tails to Y −60.06, **6.10** from the frame; DevKitC tails 3.90; JP1's 14.35 from the shell |
  | Install | The 2 mm slide up under the hooks is clear; the approach toward the wall is clear for 5.0 mm (2.5 needed), then the DevKitC meets the yaw junction board, PCB-08 |

  Reserves touched at 0.00, by design, as with the CAD carrier: the DevKitC against its own USB service corridor and the head-riser harness route, and the GH headers against the plug-layer reserve their plugs fill. `check_pcb10_mount.py` owns the uprights, hooks, reliefs and screws, and passed 9/9 at set-up; this board changes none of them.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-27:** design started (lesson 1). Inputs drafted from the sources above and measured in the body CAD. Found the upper mounting screws under the DevKitC, the DevKitC pin tails on the uprights, the CAD DevKitC's 25.4 mm rows (v1.1 is 22.86 mm), the v1.1 LED on GPIO38 and the USB back-feed through `VCC_5V`. `J10-2` named by direction for a straight `W25`; `J10-8` and `J10-10` kept. Gaps 1–4 raised for the builder.
- **2026-10-27:** inputs frozen with [D-068](../../decisions.md#d-068): two screws and two edge hooks with pin-tail reliefs (CAD in `final/v1/cad`, `check_pcb10_mount.py` 8/8 pass), the Espressif v1.1 DevKitC in the final CAD, TPS3436CCCBG from Mouser India, SOIC-8 transceiver footprint, Schottky against USB back-feed.
- **2026-10-28:** schematic drawn (lesson 2): Espressif's DevKitC symbol, a new TPS3436CCCBG symbol, a flattened AO3400A, and a DevKitC footprint from Espressif's pads with 1.0 mm holes. ERC 0 errors, 0 warnings; netlist checked row by row against the inputs.
- **2026-10-28:** board set up (lesson 3). The real connector footprints gave 23 courtyard overlaps at the CAD positions: the board grows 6 mm down for a third row, notched over the right DRV8833's terminal block, with `J10-1` at its real size (D-068 amended; `check_pcb10_mount.py` 9/9). Rule areas over the uprights and under the hooks, proved on a scratch copy. 3D models: TSOT-23-8 for the DDF watchdog, a full-tail Micro-Fit from Molex's drawing; both checked against their pads in a STEP.
- **2026-10-28:** placement (lesson 4, part 1). Connectors, holes and DevKitC on their proved origins; every part placed with DRC clean (no courtyard, edge or parity errors). Layout-driven changes: `J10-2` reordered to U2's own pin order (pairs run straight), and the GPIO map reassigned to **v0.3** so each track runs to its connector without crossings (both recorded above and at PCB-09 / 05-harness). Routing in progress.
- **2026-10-28:** routed (lesson 4, part 2) on four layers: In1 solid GND, In2 +3V3 with WDO, C3_READY and SLP as tracks, B for the top-row descents, UART and `+5V_DK` round the edges. Test points cut to the rails plus WDI, WDO, C3_READY and SLP (TP11 retargeted from READY to C3_READY). DRC 0 errors, 0 unconnected, parity clean.
- **2026-10-28:** rev A design complete (lesson 5). DevKitC 3D model from `pcb10_devkitc()`; board STEP; `check_pcb10_fit.py` 7/7; fab outputs in `fab/revA/`. The first fit run failed on the script, not the board: KiCad writes model names with `_` for `.`, and the STEP cuts holes from the core.
