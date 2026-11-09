# Module selection (D-093 level 3)

| Field | Value |
|---|---|
| Status | **SELECTED, 2026-11-07** ([D-094](decisions.md#d-094), builder approved). **Not a purchase list yet**: each line has an acceptance state (§1). Not ordered. BOM rows follow at plan level 6 |
| Parent | [D-093](decisions.md#d-093), [simplification-plan.md](simplification-plan.md) §2, §3, §5 |
| Review | A second review (2026-11-07) corrected the M1 rating, the HP and ALV prices and the STEP note, and raised the open items in §3. Each claim was re-read on the vendor page before it was taken |
| Stock evidence | Retailer pages read 2026-11-06/07. A listing with "Add to Cart" counts as available; prices and stock are checked again at order. Fab.to.Lab is Pololu's listed India distributor |
| Evidence labels | `D` vendor data read, `E` estimate, `U` unknown until measured or chosen |

## 1. Selection

**Acceptance state:**
- **Accepted:** part and source settled.
- **Bench-gated:** chosen, but a named test must pass before it is accepted.
- **Source open:** the part type is chosen; the exact article or a seller in stock is not.

| # | Function (replaces) | Part | Key data (`D`) | Size, mounting | India source, price | Qty | State |
|---|---|---|---|---|---|---|---|
| M1 | On/off latch (PCB-02 `LTC2954`) | **Pololu #2813 Big Pushbutton Power Switch, HP** | 4.5–40 V; **"16 A, continuous at 12 V, without exceeding 150 °C"** (Pololu specs). A 150 °C board is not acceptable in a closed PETG body, so the usable rating is lower and set by test N1. OFF draw < 0.2 µA; ON, OFF and CTRL inputs (> 1 V pulse); press-to-on wiring (button to ground on the on-only connection) | 20.3 × 25.4 × 4 mm, 2.7 g; large power holes, 0.1″ side holes | Fab.to.Lab, **₹1,275** (₹848 MP base + ₹427 HP option), in stock | 1 | Bench-gated (N1) |
| M2 | Head pitch/roll 6.0 V (PCB-03 LTC3119 #1) | **Pololu #2572 S18V20ALV**, set to **6.0 V** ([D-100](decisions.md#d-100); was 5.5 V: the yaw FFC drop pulled the head terminals under N2's 5.23 V) | 2.9–32 V in, 4–12 V out; "about 2 A" when input is near output; Pololu says its plotted thermal limit cannot be sustained continuously. Demand: 2.8 A aligned-stall allowance | 21 × 43 × 10 mm; four M2 holes | Fab.to.Lab, **₹2,700** (₹2,454 base + ₹246 ALV option), in stock | 1 | Bench-gated (N2(b)) |
| M3 | Yaw 11.1 V (PCB-03 LTC3119 #2) | **Pololu #2572 S18V20ALV**, set to 11.1 V | As M2. 11.1 V leaves 1.5 V to the ST3215-HS 12.6 V maximum, but the 2.4 A locked rotor exceeds "about 2 A", and capacity at a 6 V pack is unproven (power-boards §4A already called 2 A a planning ceiling) | As M2 | As M2, ₹2,700 | 1 | Bench-gated (N3) |
| M4 | Pi 5 (PCB-04 compute branch) | **Pololu #4082 S13V30F5** (5 V buck-boost) | 2.8–22 V in, 5 V out; 3 A "where the input voltage is close to the output", otherwise limited by input and heat; reverse protection to 20 V. **Voltage margin open:** 5.0 V nominal against Raspberry Pi's 5.1 V supply spec, minus `W10` and USB-C contact drop | 22.9 × 22.9 × 9.7 mm; two M2 holes; **Pololu STEP available** | Fab.to.Lab, ₹1,143, in stock | 1 | Bench-gated (N12) |
| M5 | C3, amp, C2, display (PCB-04, four branches) | **Pololu #4082 S13V30F5** | As M4. Load ≈ 1.5 A average (`E`); peaks at a shared start-up and audio/display bursts unmeasured | As M4 | As M4 | 1 | Bench-gated (N2(c)) |
| M6 | Pack voltage and current (PCB-02 pack sense, PCB-03 INA2181) | **INA226 board; full-bus shunt value OPEN (CH-099)** | INA226 ±81.92 mV: R010 clips at ~8.2 A and dissipates 2.56 W at 16 A, so it is rejected for the full switched bus. A 5 mΩ ≥2 W shunt is a candidate (~16.4 A full scale, 1.28 W at 16 A), still with little range margin. Bus voltage remains usable independently. Select from measured peaks and thermal duty; calibrate | `U` | Ordered board's seller/article and shunt are unreported; inspect on receipt. If R010, use only on an isolated current-limited bench load, not the robot path. Source a suitable lower-value shunt/module after N1–N3 independent current-probe measurements | 1 | Shunt OPEN; electrical HOLD |
| M7 | Base IMU (PCB-07) | **Adafruit #4438 LSM6DSOX** | 3–5 V VIN; SPI on SCK/SDA(in)/DO(out)/CS, INT1, INT2: matches PCB-10 `J10-7` | About 25.6 × 17.8 mm (`U`, confirm); STEMMA QT | ThingBits ₹1,169 + GST (in stock); Fab.to.Lab ₹1,290; Mouser India | 1 | Accepted (outline to measure for the J15A adapter) |
| M8 | Speaker amp (PCB-05) | **SmartElex MAX98357A breakout** (BO-007, promoted) | Registered: 5 V, about 1.75 W into the 8 Ω BO-001, no MCLK, screw terminal. Keep BO-007's SD network check | Adafruit #3006 class | Robocraze ₹195, **in stock (123) on 2026-11-07**; the review saw "sold out", so recheck at order | 1 | Accepted |
| M9 | Mics (PCB-06 ×4) | **INMP441 I²S MEMS module** | I²S, L/R pin, 1.4 mA. Two per lane with **opposite L/R settings**: front pair SDI0, rear pair SDI1. **100 kΩ pull-down on each SD lane** (INMP441 datasheet) at the audio hub | Outline and port side `U` (measure on receipt) | RoboBazar ₹129 (in stock), Techiesms ₹150, MakerBazar ₹219, Robocraze, Probots | 4 + 1 spare | Bench-gated (N9/N11 four-channel capture) |
| M10 | Charger (PCB-02 BQ25798, PCB-13) | **ISDT PD60** | USB-C PD in (5–20 V); 60 W; 1–4S; LiPo mode = 4.20 V/cell (never LiHV); 1/2/3/6 A (use 1–2 A); balance lead; XT60 out | 56 × 85 × 21 mm (off-board) | **Availability open:** IndianRoboStore pre-order (₹1,525), Indian Hobby Center sold out, Zbotic page unreadable. Fallback: ToolkitRC M4 or a genuine SkyRC iMAX B6 class, both with a 4.20 V/cell Li mode | 1 | Source open |
| M11 | Charger supply | **USB-C PD adapter (BO-016)**: ≥ 30 W with a 15 V PDO, BIS-registered | 2S at 2 A is about 17 W. **No maker or model chosen yet** | — | Choose a specific BIS-registered article at order and confirm its PDO list | 1 | Source open |
| M12 | Charge and balance ports | XT30 female in a printed panel holder; JST-XH 3P balance lead in a printed slot; XT60→XT30 lead for the PD60 | Connector types only; exact articles, polarity marking and mating leads to choose | Panel and channel fit at level 4 | Generic hobby stock | 1 set | Source open (level 4) |
| M13 | Small parts | 2 × SMBJ8.5A + 2 × 100 µF ≥ 16 V + 2 × 0.1 µF at each #3297 `VM`; 1 × 3 A Schottky (SS34 class) in `W11`; perfboard audio hub (33–100 Ω clock resistors, 100 kΩ SD pull-downs) | The SMBJ8.5A clamps up to 14.4 V at 41.7 A, so the part alone does not keep `VM` under 11.8 V; the bulk capacitance does most of the work (power-boards §2.2). **N4 decides it.** The Schottky needs a loaded C3 voltage and back-feed check (N8) | — | Generic | 1 set | Recipe; bench-gated (N4, N8) |

**Two part types for all four rails.** S18V20ALV ×2 (head, yaw) and S13V30F5 ×2 (Pi, shared 5 V). One spare of each covers every rail.

**Rough cost** (`E`, ex-shipping, corrected): about ₹13,500–14,500 for M1–M10, plus small parts and one spare of each regulator (about ₹3,850).

## 2. What changed from the plan's first picks

| Item | Plan (§3) | Selected | Why |
|---|---|---|---|
| Pi supply | 5.1 V, ≥ 5 A buck (D24V50F5 class) | **S13V30F5, 5 V buck-boost** | The D24V50F5 needs **6 V minimum in** and drops **≈ 1.5 V at 5 A** (`D`), so it falls out of regulation before the 6.0 V low-battery stop. A Pi 5 on a non-PD supply **assumes 5 V / 3 A** and limits USB to 600 mA (Raspberry Pi RP-009856), so 5 A buys nothing. The buck-boost holds its output down to 2.8 V in. Its 5.0 V nominal is under the Pi's 5.1 V spec, so N12 checks the voltage at the Pi |
| Shared 5 V | 2.5–3 A buck (D36V28F5 class) | **S13V30F5** | Same part as the Pi; no dropout near 6 V; ₹1,143 against ₹1,798 |
| Power switch | MP or HP | **HP** | Twice the MP's rating and lower loss. Its 16 A figure is at a 150 °C board, so **R1 stays open as a thermal check (N1)** |
| PCB-12 (Q5) | Fit-check the Waveshare ESP32 Servo Driver | **Custom PCB-12** | The Waveshare board is **65 × 30 mm** (holes 58 × 23, Ø2.75), against the head's **18 × 23.5 mm** vertical C2 board plus a 7.4 mm parts reserve ([layout_model.py](03-head/v1/cad/layout_model.py)). It also carries a plain ESP32-WROOM-32, not the S3 |

## 3. Open before purchase or at level 4

The pass criteria for every N-test are in the plan's bench register ([simplification-plan.md §4.12](simplification-plan.md#412-tests)); this table only says which test or task closes each item.

| Item | Closes when |
|---|---|
| **M1 thermal** | N1 passes (closed body, 10 A for 10 s and a 30 min demo duty cycle, board < 70 °C) |
| **M2 head capacity** | N2(b) passes with the Feetech protection currents set. **No rated capacity fallback is chosen yet:** the S13V25F6 (6 V, 2.5 A, ₹1,553) is a voltage alternative, still below the 2.8 A aligned-stall figure, so it too depends on the servo current limits. If N2(b) fails, select a part rated ≥ 3 A at 6 V in (or split pitch and roll onto two S18V20ALVs, which changes the head trunk), by decision |
| **M3 yaw capacity** | N3 passes (sustained sweeps and a hard stop, at 6.0 V and 8.4 V packs) |
| **M4 Pi voltage** | N12 passes (≥ 4.90 V at the module unloaded, ≥ 4.80 V at the Pi through boot and stress, no throttling flag) |
| **M5 peaks** | N2(c) passes |
| **M13 `VM` and Schottky** | N4 and N8 pass |
| **M6 board** | Inspect the ordered article and its shunt/routing; R010 remains bench-only within verified limits. Measure N1–N3 peaks independently, select a full-bus shunt/module with range and thermal margin, and calibrate against a meter |
| **M10 charger** | A seller in stock, or the fallback charger chosen |
| **M11 adapter** | A specific BIS-registered adapter with its PDO list confirmed |
| **M12 ports** | CAD placed (D-095): XT30U female epoxied in a panel opening, the body-side lead's XHP-3 plug parked face-out in a slot, and a JST PA 3P wire-to-wire balance break (PAP-03V-S + PALR-03VF) in the pack channel. Exact articles, polarity marks and the XT60→XT30 lead still to buy |
| **Outlines** | M6 and M9 (and M8) measured on receipt; their CAD outlines are UNMEASURED envelopes in cradles or pockets with clearance (D-095). M7 is drawn from Adafruit's EAGLE board file (25.4 × 17.78, two Ø2.5 holes 20.32 apart) |
| **STEP models** | Closed (D-095): Pololu publishes STEPs for all three Pololu modules (S13V30F5 0J1808, S18V20x 0J1416, #2813 0J1405); they are in `final/v1/cad/purchased/`. The #2813 has no mounting holes, so it sits in a printed cradle |

## Sources

- Pololu [#2813 specs](https://www.pololu.com/product/2813/specs), [#2572 S18V20ALV](https://www.pololu.com/product/2572), [#4082 S13V30F5](https://www.pololu.com/product/4082) and [resources](https://www.pololu.com/product/4082/resources), [#2851 D24V50F5](https://www.pololu.com/product/2851), [#3782 D36V28F5](https://www.pololu.com/product/3782)
- Fab.to.Lab: [Big Pushbutton MP/HP](https://www.fabtolab.com/big-pushbutton-mp-hp), [S18V20 family](https://www.fabtolab.com/pololu-step-up-down), S13V search; read 2026-11-07
- [Raspberry Pi RP-009856, USB Power Delivery on Raspberry Pi 5](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf)
- [Adafruit LSM6DSOX pinouts](https://learn.adafruit.com/lsm6dsox-and-ism330dhc-6-dof-imu/pinouts); [ThingBits listing](https://legacy.thingbits.in/products/adafruit-lsm6dsox-6-dof-accelerometer-gyro-sensor-stemma-qt-qwiic)
- [Probots INA226 module](https://probots.co.in/ina226-power-monitoring-sensor-dc-voltage-and-current-module.html) (out of stock, 2026-11-07)
- [Robocraze SmartElex MAX98357A](https://robocraze.com/products/smartelex-max98357a-i2s-audio-breakout-amplifier-for-raspberry-pi-and-microcontrollers) (in stock, 2026-11-07)
- INMP441: [RoboBazar](https://robobazar.in/product/inmp441-mems-microphone-module-i2s/), [Robocraze](https://robocraze.com/products/inmp441-mems-high-precision-omnidirectional-microphone-module-i2s)
- ISDT PD60: [IndianRoboStore](https://indianrobostore.com/product/isdt-pd60-60w6a-portable-1-4s-li-po-balance-charger), [Indian Hobby Center](https://www.indianhobbycenter.com/products/isdt-pd60-60w-6a-portable-1-4s-li-po-balance-charger)
- [Waveshare Servo Driver with ESP32 docs](https://docs.waveshare.com/Servo_Driver_with_ESP32) (65 × 30 mm)
