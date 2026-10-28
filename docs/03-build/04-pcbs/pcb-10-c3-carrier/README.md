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
| 1. Design | **In progress: schematic done, ERC clean**; board set-up next. Inputs frozen with [D-068](../../decisions.md#d-068) | [`check_pcb10_mount.py`](../../final/v1/cad/check_pcb10_mount.py) 8/8 pass | 2026-10-27 |
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

### GPIO map (build v0.2, D-068)

Pin map v0.1 (RP-03 §3.2) plus the changes since: power-boards §2.4 (D-038), D-013, D-016, D-041 and board-specs §7. Strapping pins 0/45/46 and USB 19/20/43/44 stay unconnected on the carrier.

| Function | GPIO | DevKitC pin | Carrier net / connector | Change from v0.1 |
|---|---:|---|---|---|
| `ENC_L_A`, `ENC_L_B` | 4, 5 | J1-4, J1-5 | `J10-3` pins 3, 4 | — |
| `ENC_R_A`, `ENC_R_B` | 6, 7 | J1-6, J1-7 | `J10-4` pins 3, 4 | — |
| `IN1_L`, `IN1_R` (LEDC) | 11, 12 | J1-17, J1-18 | `J10-5`/`J10-6` pin 2 | Was `PWM_L/R` (D-038) |
| `IN2_L`, `IN2_R` (LEDC) | 13, 14 | J1-19, J1-20 | `J10-5`/`J10-6` pin 3 | Was `DIR_L/R`; now a second LEDC output (D-038) |
| `nSLEEP` | 21 | J3-18 | AND gate U4 input A | Now gated with `C3_READY` (D-038) |
| `nFAULT` | 9 | J1-15 | `J10-5`/`J10-6` pin 4, wired-OR, 10 kΩ pull-up | — |
| `GP2Y_VO` (ADC1_CH0) | 1 | J3-4 | `J10-8` pin 3 | Was `OBST_IR`; same pin |
| `HALL_OUT` (ADC1_CH9) | 10 | J1-16 | `J10-8` pin 5 | **New** (D-013; was the touch switch on `BUMP`). Takes spare 10, an ADC1 pin |
| `TCRT_OUT` (ADC1_CH7) | 8 | J1-12 | `J10-10` pin 3 | Was `CLIFF_REAR` digital; same pin, now analog (D-016) |
| `TCRT_LED_EN` | 47 | J3-17 | Q1 gate | **New** (D-016). Takes `BUMP`'s pin, freed by D-013 |
| IMU `MOSI`, `MISO`, `SCLK` | 35, 36, 37 | J3-13, J3-12, J3-11 | `J10-7` pins 4, 5, 3 | — |
| IMU `CS`, `INT1` | 41, 42 | J3-7, J3-6 | `J10-7` pins 6, 7 | — |
| IMU `INT2` | — | — | `J10-7` pin 8: not connected | v0.1 has one IMU interrupt. PCB-07 is HOLD |
| C0 link `TX`, `RX` (UART1) | 17, 18 | J1-10, J1-11 | THVD1451 `D`, `R` | — |
| `WDI` | 48 | J3-16 | TPS3436 `WDI`, 10 kΩ pull-up | — (free on v1.1, see above) |
| `MCU_RDY` | 2 | J3-5 | READY gate input, 10 kΩ pull-down | Takes spare 2 (board-specs §7, `BD-10`) |
| `MOTOR_PRESENT` | 40 | J3-8 | `J10-12` pin 3 | — |
| `ENERGY_OK` | 39 | J3-9 | Not connected | **No cable brings it to C3 in the build** (`J10-12` has only `C3_READY` and `MOTOR_PRESENT`). Kept reserved |
| `ESTOP_N` | 3 | J1-13 | Not connected | Deleted by D-041. GPIO3 is unassigned strapping again |
| `CLIFF_FL`, `CLIFF_FR` | 15, 16 | J1-8, J1-9 | Not connected | No front cliff hardware in v1 (testsystem §9 hold) |
| Board RGB LED | 38 | J3-10 | Not connected | On the v1.1 board |

**Budget.** 24 of the 28 assignable GPIO are used. Unassigned and safe: **15, 16, 39** (39 while no `ENERGY_OK` cable exists), plus 38 behind the board LED. The `CA` §3 gate of at least two safe spares holds. ADC1 pins are now all used except GPIO3 (strapping), so any future analog look-down channel needs change control. The firmware's `c3_board_role.h` (RP-02 phase A) still has v0.1 and is regenerated from this table when the map is accepted (`CA-14`).

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
| **`J10-2`** (GH6) | GND, `C3TX+`, `C3TX−`, `C0TX+`, `C0TX−`, spare | **Set here (below)**; PCB-09 `J9-2` follows |
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
| 2 | `C3TX+` | Y (driver, non-inverting) | A (receiver) + 120 Ω |
| 3 | `C3TX−` | Z | B |
| 4 | `C0TX+` | A (receiver) + 120 Ω | Y (driver) |
| 5 | `C0TX−` | B | Z |
| 6 | spare | Not connected | Not connected |

`W25` is wired 1:1 (pin n to pin n), with 2–3 and 4–5 twisted. Each pair sits next to the other, and GND is on pin 1, as 05-harness §5.2 asks. PCB-09's `J9-1` head link may use the same rule; that is PCB-09's to decide.

**`J10-8`, nose (set by PCB-10, unchanged).** 1 +5V, 2 GND, 3 GP2Y_VO, 4 +3V3, 5 HALL_OUT. Ends: GP2Y S3B-PH pins 1 Vo, 2 GND, 3 Vcc (datasheet) go to `J10-8` 3, 2, 1. PCB-15 P1 +3V3, P2 GND, P3 HALL_OUT go to 4, 2, 5. The GND conductor splits near the nose to both sensors. **Why keep this order:** +5V sits only beside GND, so a short or mis-crimp can't put 5 V on a 3.3 V ADC pin. The cost is that `HALL_OUT` sits beside its own +3V3 rather than GND, which is acceptable for a slow, filtered signal. The other orders tried put +5V beside an ADC input or GP2Y_VO (which carries LED-pulse noise) beside HALL_OUT.

**`J10-10`, rear TCRT (set by PCB-10, unchanged).** 1 LED_A, 2 LED_K, 3 TCRT_OUT, 4 GND, as rear-tcrt-lead.md wires the sensor (A, K, C, E). The LED current loop is on adjacent pins, `TCRT_OUT` is beside its return, and LED_A carries only the 100 Ω-limited 3.3 V.

### Envelope

Measured 2026-10-27 in the built body v1 CAD (`body_v1_model.py` with the legacy 0.4.28 runtime): carrier compound, frame, shell (and its 0–125 mm lowering path), panels, compute tray and hardware, mic boards, connector and harness reserves. The DevKitC and Pi STEPs are swept as boxes. None of the `final/v1/cad` droid edits touch this area. **F** is the +Y face (DevKitC, headers, plugs), **B** the −Y face toward the wall.

| Item | Value |
|---|---|
| Board | 70 × 43.5 × 1.6 mm: X −14…56, Z 82…125.5, Y −58.4 (B) … −56.8 (F) |
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

5. GPIO map v0.2 above: `HALL_OUT` on GPIO10, `TCRT_LED_EN` on GPIO47, IMU `INT2` not connected, GPIO38 left to the v1.1 LED.
6. `J10-2`, `J10-8`, `J10-10` orders above. Recorded at PCB-09 and in 05-harness §5.2.
7. `MR`: no safety-converter power-good reaches C3 (`PG_BASE` goes to PCB-02 on `W20`). Pull `MR` up to 3V3 with a test point. The watchdog then starts with the DevKitC's 3.3 V.
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
| U1 | Espressif ESP32-S3-DevKitC-1-N8 v1.1 (CH-045) | GPIO map v0.2. 3V3 (pads 1, 2) is the carrier's `+3V3`; 5V (21) on `+5V_DK`; RST/EN (3) on `WDO`; G (22, 23, 24, 44). Unused pads 8, 9, 13, 14, 25, 26, 30, 31, 35, 36, 42, 43 carry no-connect flags. Not in the position file: hand-soldered after PCBA, tails clipped to 1.5 mm |
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
| J2 (`J10-2`) | BM06B-GHS-TBT | 1 GND, 2 `C3TX_P`, 3 `C3TX_N`, 4 `C0TX_P`, 5 `C0TX_N`, 6 no connect |
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
| TP1–TP15 | Ø1.0 pads, not in the BOM | `+5V_IN`, `+5V_DK`, `+3V3`, GND, `C3TX_P/N`, `C0TX_P/N`, `WDI`, `WDO`, `READY`, `SLP`, `FLT`, `MR`, `WD_EN`. Placed outside the DevKitC's shadow (lesson 1) |
| H1, H2 | Ø2.7 mm holes | The two lower M2.5 screws (D-068 A); no net |

`PWR_FLAG` sits on `+5V_IN` (enters on J1), `+5V_DK` (the diode's output), `+3V3` (the DevKitC's regulator, whose pins Espressif types as power inputs) and GND. Unfitted parts carry KiCad's DNP flag.

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-28): **0 errors, 0 warnings.**

**Check against the inputs**, row by row, from the exported netlist:

| Input (lesson 1, D-068) | Netlist | Result |
|---|---|---|
| GPIO map v0.2 | `ENC_L_A/B` U1.4/5, `ENC_R_A/B` U1.6/7, `UART_TX/RX` U1.10/11, `TCRT_ADC` U1.12 (GPIO8), `NFAULT` U1.15, `HALL_ADC` U1.16 (GPIO10), `IN1_L/R` U1.17/18, `IN2_L/R` U1.19/20, `NSLEEP` U1.27 (GPIO21), `TCRT_LED_EN` U1.28 (GPIO47), `WDI` U1.29 (GPIO48), IMU MOSI/MISO/SCLK U1.32/33/34 (GPIO35/36/37), `MOTOR_PRESENT_MCU` U1.37 (GPIO40), `IMU_CS_MCU` U1.38 (GPIO41), `IMU_INT1_MCU` U1.39 (GPIO42), `MCU_RDY` U1.40 (GPIO2), `GP2Y_ADC` U1.41 (GPIO1) | Match |
| Unused pins open | U1 8, 9, 13, 14, 25, 26, 30, 31, 35, 36, 42, 43 unconnected (GPIO15, 16, 3, 46, 19, 20, 45, 0, 38, 39, 44, 43) | Match |
| 5 V in, back-feed diode | `+5V_IN`: J1.1, D1.2 (A), C1, C2, C10, J8.1, TP1. `+5V_DK`: D1.1 (K), U1.21, TP2 | Match |
| Watchdog pinout C, SET 00 | `WDI` U3.3, R1, U1.29, TP9. `WDO` U3.7, R2, U1.3 (EN), U5.1, TP10. `WD_EN` U3.6, R3, JP1.1, U5.3, TP15. `MR` U3.2, R4, TP14. U3.1, U3.5, U3.4 on GND | Match |
| READY = WDO ∧ WD-EN ∧ MCU_RDY; 1k out | `MCU_RDY` U5.6, R5, U1.40. `READY` U5.4, R6, R8, U4.2, TP11. `C3_READY` R6, J12.2 | Match |
| SLP = NSLEEP ∧ READY, pulled down | `NSLEEP` U1.27, R7, U4.1. `SLP` U4.4, R9, R10, TP12 → `SLP_L` J5.1, `SLP_R` J6.1 | Match |
| `FLT` wired-OR, 10k pull-up, GPIO9 | `FLT` J5.4, J6.4, R15, R16, TP13. `NFAULT` R16, U1.15 | Match |
| `J10-2` by direction, 120 Ω at this receiver | `C3TX_P/N` U2.5/6 → J2.2/3. `C0TX_P/N` J2.4/5 → U2.8/7, R17 across, R18/R19 (DNP). J2.6 open | Match |
| `J10-8` order; nose circuits | J8.1 `+5V_IN`, J8.2 GND, J8.3 `GP2Y_VO` → R38 → `GP2Y_ADC` (R39, C11), J8.4 `+3V3`, J8.5 `HALL_OUT` (R40) → R41 → `HALL_ADC` (C12) | Match |
| `J10-10` order; TCRT circuit | J10.1 `LED_A` ← R34 ← `+3V3`. J10.2 `LED_K` → Q1.3 (D); Q1.1 (G) `TCRT_LED_EN` with R35; Q1.2 (S) GND. J10.3 `TCRT_OUT` R36, C9, R37 → `TCRT_ADC` | Match |
| `J10-3/4`, `J10-5/6`, `J10-7`, `J10-12` orders | J3/J4 1 GND, 2 `+3V3`, 3 A, 4 B. J5/J6 1 SLP, 2 IN1, 3 IN2, 4 FLT, 5 GND, 6 open. J7 1 `+3V3`, 2 GND, 3–7 SCLK, MOSI, MISO, CS, INT1, 8 open. J12 1 GND, 2 `C3_READY`, 3 `MOTOR_PRESENT`, 4 GND | Match |
| One ground; every GH mounting pad on GND | `GND`: U1.22/23/24/44, U2–U5 grounds, J1.2, every J pin and MP named GND, JP1.2, Q1.2, all pull-downs and capacitors | Match |
| `+3V3` from the DevKitC | `+3V3`: U1.1/2, U2–U5 VCC, C3–C8, J3.2, J4.2, J7.1, J8.4, all pull-ups, R34, R36, TP3 | Match |
| Fixings no net | H1, H2 have no pins | Match |

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-27:** design started (lesson 1). Inputs drafted from the sources above and measured in the body CAD. Found the upper mounting screws under the DevKitC, the DevKitC pin tails on the uprights, the CAD DevKitC's 25.4 mm rows (v1.1 is 22.86 mm), the v1.1 LED on GPIO38 and the USB back-feed through `VCC_5V`. `J10-2` named by direction for a straight `W25`; `J10-8` and `J10-10` kept. Gaps 1–4 raised for the builder.
- **2026-10-27:** inputs frozen with [D-068](../../decisions.md#d-068): two screws and two edge hooks with pin-tail reliefs (CAD in `final/v1/cad`, `check_pcb10_mount.py` 8/8 pass), the Espressif v1.1 DevKitC in the final CAD, TPS3436CCCBG from Mouser India, SOIC-8 transceiver footprint, Schottky against USB back-feed.
- **2026-10-28:** schematic drawn (lesson 2): Espressif's DevKitC symbol, a new TPS3436CCCBG symbol, a flattened AO3400A, and a DevKitC footprint from Espressif's pads with 1.0 mm holes. ERC 0 errors, 0 warnings; netlist checked row by row against the inputs.
