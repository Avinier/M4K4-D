# Charge path — PCB-13 inlet and the PCB-02 charger

| Field | Value |
|---|---|
| Status | Circuit closed on paper, 2026-10-04 ([D-040](../decisions.md#d-040)). No schematic capture, layout, NVM image or bench result. Every value below is `D` or arithmetic on `D` unless marked |
| Scope | Everything between the adapter and the pack's `BATBUS` entry: inlet, PD negotiation, input switch, charger, battery sense, pack temperature, status. The `OFF/OPERATE/CHARGE` latch, `SYS` gating and pack sensing on PCB-02 stay as RP-02 [board-specs.md §4.1–4.2](../../02-prototypes/RP-02-electrical/board-specs.md) |
| Supersedes | RP-02 board-specs §4.1 rows "Charge inlet" and "Input switch", and §4.5.1 values for `TS`, the `VBUS`/`PMID` capacitor voltage, `D+`/`D−` and `QON`. Everything else in §4 stands |
| Sources read | TI BQ25798 SLUSDV2C (June 2026); ST STUSB4500 DS12499 Rev 3; TI TVS2200 SLVSED5C; GCT USB4140 drawing (2024-08-29); Würth 74437346022; SEMITEC catalogue 129M (103AT table); ST ESDA25W and STL6P3LLH6 distributor summaries (ST's own PDFs did not download) |
| Evidence labels | `D` datasheet, `E` estimate, `U` unknown, `W` measured. No `W` value exists |

## 1. What changed

1. **The inlet is now its own board, PCB-13, on the rear panel.** Before, a vertical receptacle sat on PCB-02's back face. Three problems:
   - The sloped panel left its mouth 3.3 mm behind the panel's inner face, not the 1.05 mm the CAD comment said. A plug could seat only if its overmold went 5.7 mm into a 13.2 × 7.2 mm cut-out, with 0.35–0.43 mm a side against an untoleranced panel-to-board stack.
   - Every insertion and pull loaded PCB-02, which has no mounting in the CAD.
   - The receptacle's part number was open.

   PCB-13 carries the receptacle, its surge and ESD protection, the STUSB4500 and the input switch. Two screws hold it to a pad printed on the panel. The mouth is flush with a pocket that takes any compliant plug (§6).
2. **The charger straps change.**
   - `D+` is tied to `D−`.
   - `BATP` gets its 100 Ω sense lead. RP-02 omitted the pin.
   - The `TS` divider is retuned so charging stops inside the 25R's 0–50 °C surface window.
   - Every `VBUS`-side part is rated for 20 V, because a blank STUSB4500 asks for 20 V.
   - The VBUS TVS becomes a TVS2200, because the RP-02 ESDA25P35 clamps above the charger's 30 V absolute maximum.
3. **No architecture change.** The build is still USB-C PD into a host-less BQ25798 in default mode (`BD-09`, `BD-12`). The pack is the TIFPS0629 (D-019) behind the fuse-side splice (D-039).

## 2. Power path

```
 adapter ≥30 W PD (15 V) ─ C-to-C cable
   │
 PCB-13 (rear panel)                                          PCB-02 (frame)
 J1 USB4140 ─ VBUS ─┬─ D1 TVS2200 ─ C1 4.7 µF ─ Q1 P-FET ─ VSNK ─ W16 ─ J2-8 ─┬─ C 2×10 µF ─ BQ25798 VBUS=VAC1=VAC2
                    └─ U1 STUSB4500 VDD                    (VBUS_EN_SNK)        ├─ 100k/100k → Q_cp → CHARGE_ABSENT, Q_dis, Q_kill
 CC1/CC2 ─ D2 ESDA25W ─ U1 CC1/CC2 (dead-battery Rd)                            │
                                                         BQ25798 BAT ─ BATBUS-C ─ J2-1 ─ W03d ─ (+)splice ─ fuse ─ J-PK ─ pack
                                                         BQ25798 BATP ─ 100 Ω ─ Kelvin to J2-1 pin
                                                         BQ25798 TS ─ J2-7 ─ W02b ─ SM break ─ W02a ─ 103AT-2 on a cell
                                                         BQ25798 SYS ─ Q_sys ─ D_sys ─ C2/display OR node (RP-02, unchanged)
```

Nothing upstream of `VSNK` is live until a source attaches and a 9 V or 15 V contract exists. The STUSB4500 is powered from `VBUS` only, so the inlet draws nothing in `OFF`.

## 3. PCB-13 — charge inlet board

28 × 15 × 1.6 mm, two layers. The receptacle is the only part on the −X (panel) face; everything else is on +X, 2.0 mm maximum height. The two M2 holes are at Y ±11 on the receptacle's centre line.

| Ref | Part | Value / rating | Connection | Why |
|---|---|---|---|---|
| J1 | GCT **USB4140-GF-0170-C** | Vertical, 6-pin power-only, H 6.50 mm; 3 A on `VBUS`, 4.25 A on `GND`, 1.25 A on CC; 48 V; 5–20 N mating; 20k cycles; four 1.70 mm shell stakes (`D`) | A9/B9 `VBUS`, A12/B12 `GND`, A5 `CC1`, B5 `CC2`, shell to `GND` | Through-hole stakes carry the plug loads; no D+/D− to route; the 1.70 mm stake suits a 1.6 mm board |
| D1 | TI **TVS2200DRVR** | 22 V standoff, 24.6–27.6 V breakdown, 28 V maximum clamp at 40 A 8/20 µs, level-4 ESD (`D`) | `VBUS`–`GND` at J1 | Lets a 20 V source through and clamps below the BQ25798's 30 V `VBUS`/`VAC` absolute maximum. The ESDA25P35 cannot do both |
| D2 | ST **ESDA25W** | Dual, 24 V standoff, 25 V minimum breakdown, 65 pF, IEC 61000-4-2 level 4 (`D`, distributor) | `CC1`, `CC2` to `GND`, beside J1 | ST's own STUSB4500 reference part; the standoff is above the 22 V CC short-to-`VBUS` tolerance |
| C1 | 4.7 µF 50 V X7R 1206 | | `VBUS`–`GND` | ST reference value; inside the USB PD 1–10 µF pre-switch sink limit together with C2 |
| C2 | 1 µF 50 V X7R 0603 | | U1 `VDD` | |
| U1 | ST **STUSB4500QTR** | `VDD` 4.1–22 V, 28 V absolute maximum; CC 22 V tolerant (`D`) | `VDD` ← `VBUS`; `VSYS` → `GND`; `CC1DB`–`CC1`, `CC2DB`–`CC2` (dead battery) | A flat pack must still negotiate |
| C3, C4 | 1 µF 10 V 0402 | | `VREG_1V2`, `VREG_2V7` | Datasheet value |
| R1 | 1 kΩ 0603 | 20 mA at 20 V, below the 50 mA pin limit | `VBUS_VS_DISCH` → `VBUS` | Senses and discharges the receptacle side |
| R2 | 470 Ω 1206 anti-surge, ≥ 0.5 W (ERJ-P08 class) | 32 mA, 0.48 W at 15 V | `DISCH` → `VSNK` | Bleeds the PCB-02 input capacitors on detach. Also on during a PDO step-down, for up to 756 ms with the source still on |
| Q1 | ST **STL6P3LLH6** | −30 V, ±20 V `VGS`, 6 A, 30 mΩ maximum, PowerFLAT 3.3 × 3.3 (`D`, distributor) | Source on `VBUS`, drain on `VSNK` | ST reference part. Its body diode points `VSNK` → `VBUS`, so it blocks the 5 V before the contract |
| R3 | 100 kΩ | | Q1 gate–source | Holds Q1 off |
| R4 | 33 kΩ | | Q1 gate → U1 `VBUS_EN_SNK` | **Added.** With R3 it sets `VGS` = −0.75 × `VBUS`: −6.8 V at 9 V, −11.3 V at 15 V, −15.0 V at 20 V, −16.5 V at the TVS standoff. Directly driven, `VGS` would reach −20 V at a 20 V source |
| C5 | 100 nF 50 V | | Q1 gate–source | Soft turn-on: τ = (100 k ∥ 33 k) × 100 nF = 2.5 ms, so the PCB-02 input capacitors draw about 0.15 A |
| R5–R7 | 100 kΩ | | `ADDR0`, `ADDR1`, `RESET` to `GND` | Address 0x28; pads let the programming jig drive them |
| TP | Pads, 1.27 mm grid | | `VBUS`, `VSNK`, `CC1`, `CC2`, `SCL`, `SDA`, `RESET`, `ATTACH`, `POWER_OK2`, `GND` | NVM programming and bench probing. `ALERT`, `GPIO`, `POWER_OK3`, `A_B_SIDE`: no connection |
| W16 | 2 × AWG22, 150 mm, soldered at the +Y end of the +X face, tied through two slots | | `VSNK`, `GND` → Micro-Fit 3.0 2-way plug (43025 + 43030) | The live side has the female contacts. `VSNK` is dead unless a contract exists |

Layout:
- D1, D2 and C1 go within 3 mm of J1, with their ground straight to the stake pads.
- The shell stakes join a `GND` pour on both layers.
- `CC` traces stay short; there is no D+/D− trace.

## 4. PCB-02 — charger block

| Ref | Part | Value | Connection | Note |
|---|---|---|---|---|
| J2-8 | Micro-Fit 3.0 2-circuit right-angle header (43045-0200 class) | 5 A | Pin 1 `VSNK`, pin 2 `GND`. On the +Y edge, plug exits +Y | New. AWG22 matches the D-039 family rule |
| — | 2 × 10 µF **50 V** X7R 1206 + 100 nF | | BQ25798 `VBUS` | Was 25 V. A blank STUSB4500 negotiates 20 V |
| — | TVS2200 footprint, not fitted | | BQ25798 `VBUS` | Fit only if bench ringing at `VSNK` exceeds 26 V |
| U2 | TI **BQ25798RQMR** | Default mode, no host (`BD-09`) | — | |
| — | `VAC1`, `VAC2` → `VBUS`; `ACDRV1`, `ACDRV2` → `GND` | | | Datasheet rule with no input FETs (§7.3.5) |
| — | `PMID` 3 × 10 µF **50 V** 1206 + 100 nF | | | Was 25 V |
| L1 | Würth **74437346022** WE-LHMI | 2.2 µH ±20%; Isat 10 A (10% drop); IRP 7.7 A; 20 mΩ maximum; 7.3 × 6.6 × 3.0 mm (`D`) | `SW1`–`SW2` | Closes RP-02's open saturation item: 10 A against a 2.7 A peak (`E`) |
| — | `BTST1`, `BTST2` 47 nF 25 V | | | |
| — | `REGN` 4.7 µF 16 V | | | |
| — | `SYS` 5 × 10 µF 25 V; `BAT` 2 × 10 µF 25 V | | | |
| R10 | 100 Ω | | `BATP` → Kelvin trace to J2-1 pin 1 | **Added.** `BATP` is the voltage-regulation sense; the datasheet requires 100 Ω to pack positive |
| R11 | 8.2 kΩ 1% | | `PROG` → `GND` | 2S, 750 kHz: `VREG` 8.4 V, `ICHG` 1 A, `VSYSMIN` 7 V |
| R12, R13 | 10.0 kΩ / 6.8 kΩ 1% | | `REGN` → `ILIM_HIZ` → `GND` | Read once at power-up: 1.18–1.38 A at 15 V and 1.13–1.33 A at 9 V. The pin clamp is below the 1.5 A requested in every corner |
| R14 | **8.45 kΩ** 1% | | `REGN` → `TS` | Was 5.23 kΩ (§5.4) |
| R15 | **324 kΩ** 1% | | `TS` → `GND` | Was 30.1 kΩ |
| C10 | 10 nF | | `TS` → `GND` | The NTC lead is about 340 mm |
| J2-7 | GH 2-way | | `TS` and the BQ25798 ground pad | **Both NTC leads come to PCB-02.** A return on a cell or `B−` would sit behind the TIFPS0629's FETs and body diode. TS would then read cold and block the over-discharge recovery charge |
| R16 | 10 kΩ | | `CE` → `GND` | Charge enabled; never floating |
| — | `D+` shorted to `D−` at the pins | | | **Added.** It reads as a BC1.2 DCP (3.25 A), which the `ILIM_HIZ` clamp then limits. Floating lines can read as SDP (500 mA, about 7 W at 15 V) and starve the charge |
| — | `SDRV` 1 nF 50 V 0402 → `GND` | | | Datasheet rule with no ship FET |
| — | `QON` open + test pad | | | Internal 200 kΩ pull-up |
| — | `STAT` → J2-6 → C2 (10 kΩ pull-up there) | | | RP-02 unchanged |
| — | `INT`, `SCL`, `SDA` → bench header (no pull-ups on the board) | | | An I2C write starts the 40 s watchdog. After it the registers return to the defaults below |

Layout:
- The thermal pad gets a `GND` via array.
- Place the power loop (`VBUS`/`PMID` capacitors, L1, `SYS`/`BAT` capacitors) first.
- Keep `TS`, `BATP` and `ILIM_HIZ` off the switching nodes.

## 5. Numbers

### 5.1 Defaults the design relies on (`D`, SLUSDV2C)

| Item | Value | Note |
|---|---|---|
| Charge voltage | 8.4 V, accuracy −0.25/+0.65% → **8.379–8.455 V** (4.190–4.228 V per cell) | Inside the TIFPS0629 acceptance window (overcharge ≥ 4.275 V, [power-boards.md §3](power-boards.md#3-pcb-01--tifps0629-acceptance-before-cells-are-connected)); 47 mV margin per cell for balance error |
| Fast charge / pre-charge / termination | 1 A / 120 mA / 200 mA | Recharge at `VREG` − 200 mV |
| Safety timers | Fast 12 h (doubled in DPM), pre-charge 2 h, trickle 1 h | 2.5 Ah at 1 A needs about 3 h (`E`) |
| `VSYSMIN` | 7 V | `SYS` held at 7.2 V while the pack is below 7 V |
| `VAC_OVP` | **26 V** | The register field says "POR: 11b" (7 V), but the register reset value is 85h, which is 00b = 26 V. A 7 V OVP would block every 9 V and 15 V contract, so read REG10 on the bench before the first charge |
| `VBUS_OVP` | 25.2–26.2 V | |
| `VINDPM` | Measured no-load `VBUS` − 1.4 V | 13.6 V on a 15 V contract |
| JEITA | Below T2: `ICHG` × 20%. Above T3: `VREG` − 400 mV (8.0 V). Suspend outside T1–T5 | T2/T3 thresholds are 68.4% and 44.8% of `REGN` |

### 5.2 Adapter and input power

- **Load at 15 V.** The charge-mode load is the RP-02 figure: 8.5 W charging plus 3.2–4.7 W of `SYS` load. At about 93% (`E`) that is 12.6–14.2 W, or **0.84–0.95 A at 15 V**.
- **Input clamp.** 1.18–1.38 A at 15 V (IINDPM accuracy at 1 A: −12%/0%). The 15 V / 1.5 A request is never exceeded.
- **9 V fallback.** The clamp gives 1.0–1.33 A, or 9–12 W. The charge current dips about 0.2 A during a display peak.
- **Blank NVM.** A 20 V / 1 A contract with a clamp of up to 1.38 A. Source PDOs at ≥ 30 W offer ≥ 1.5 A at 20 V, so it works, but it is a bench-only state (§8).
- **Adapter.** USB-C PD, ≥ 30 W, with a 15 V ≥ 1.5 A PDO, BIS-registered, plus a 3 A C-to-C cable (BO-016). 5 V-only sources do nothing: `POWER_ONLY_ABOVE_5V`.

### 5.3 Voltage ratings on the `VBUS` side

| Node | Normal | Abnormal | Part limit |
|---|---|---|---|
| Receptacle `VBUS` | 5 → 15 V | 20 V (blank NVM); 28 V maximum clamp | TVS2200 22 V standoff; STUSB4500 `VDD` 28 V absolute maximum (clamp reaches it only at 35–40 A surge, 125 °C); Q1 30 V |
| Q1 `VGS` | −11.3 V | −15.0 V at 20 V | ±20 V |
| `VSNK` / BQ25798 `VBUS`, `PMID` | 15 V | 20 V | 30 V absolute maximum; capacitors 50 V |
| CC | 0–5.5 V | Short to `VBUS` in a damaged cable, 20 V | 22 V (STUSB4500); ESDA25W 24 V standoff |

### 5.4 Pack temperature window

The 25R charges at 0–50 °C surface or 0–45 °C ambient (RP-02 §3.6). The 103AT-2 sits on a cell surface. The `VT1`/`VT5` comparators are fixed ratios of `REGN`. Without a host, the window can be moved only by the divider.

The table runs every corner of:
- `VT1_RISE` 72.4–74.2%;
- `VT5_FALL` 33.7–34.7%;
- NTC R25 ±1% and B ±1%;
- resistors ±1%.

The 103AT values are from the catalogue table (0 °C 27.28 k, 50 °C 4.160 k, 60 °C 3.020 k). Script: [`ts.py`](#appendix-ts-divider-search).

| Divider | Charging stops below | Charging stops above | `ICHG` × 20% below | `VREG` − 0.4 V above |
|---|---|---|---|---|
| RP-02 5.23 k / 30.1 k | −3.5 to +2.9 °C | **58.5–62.2 °C** | 9.7 °C | 44.8 °C |
| **Build 8.45 k / 324 k** | **0.1–3.9 °C** | **46.4–49.5 °C** | 8.1 °C | 34.7 °C |

The RP-02 values let a cold pack charge below 0 °C and a hot one charge to 62 °C.

**Consequence.** Above about 35 °C on the cell, the charger stops at 8.0 V (about 4.0 V per cell). In a hot room the robot finishes at roughly 85–90% of capacity (`E`). That is the price of keeping 50 °C without a host; T3 cannot move independently of T5.

Open and short NTC both suspend charging:
- open: `TS` = 97% of `REGN`, reads cold;
- short: `TS` = 0, reads hot.

### 5.5 Pack-side checks

- **Battery sense.** `BATP` regulates at the PCB-02 entry. The fuse, splice, `J-PK` and the TIFPS0629 lie outside the sense, about 25–55 mΩ (D-039). At 1 A the cells therefore see 25–55 mV less than `VREG` during constant current. The charger reaches constant voltage early, which is the safe direction.
- **Charge current through the pack path.** The TIFPS0629 charge rating is 10 A and the 15 A ATOF fuse is unaffected. 1 A is below the 25R's 1.25 A standard charge.
- **Over-discharged pack.** Below 2.25 V (pack) the charger trickles 100 mA. Below `VBAT_LOWV` it pre-charges at 120 mA. The TIFPS0629 release under that current is a §3 acceptance row in power-boards.md.
- **Thermal.** At about 0.9 W loss (`E`) in the 4 × 4 QFN with a poured pad, the rise is about 25–30 °C. `TREG` is 120 °C.

## 6. The inlet on the panel

The CAD is in `body_v1_model.py`: `rear_panel_charge_inlet()`, `charge_inlet_pcb13()`, the `PCB02_PY` edge strip and the `CHARGE_INLET_*` constants. The check is [`check_charge_inlet.py`](../02-body/v1/cad/check_charge_inlet.py).

| Feature | Value |
|---|---|
| Axis | Horizontal (X), Y 0, Z 64. The facet behind it slopes 7° |
| Pocket | 13.4 × 7.6 mm, R 1.0 corners. Flat floor at X −61.6, 0.6 mm deep at its lower edge and 1.6 mm at its upper edge. A sharp-cornered 12.35 × 6.5 mm overmold (the USB Type-C maximum) clears it by 0.53/0.55 mm on the flats and 0.35 mm at the corners. R 1.5 corners would leave only 0.14 mm |
| Mouth | Flush with the pocket floor, so the overmold reaches the receptacle face and the plug seats fully |
| Through the panel | 9.50 × 3.80 mm hole round the 8.94 × 3.16 shell; 9.6 × 5.6 × 1.2 mm relief for the pads and stakes at the seat |
| Pad | Printed with the panel, Y ±15, Z 55.5–72.5, from the outer skin to the seat at X −55.1. Its bottom edge is 1.5 mm above the panel frame's flange |
| Fixing | Two M2 × 5 thread-forming screws (BO-013 family), heads on the board's +X face. Ø1.6 × 3.6 mm pilots give 3.4 mm of engagement and about 4 mm of print beyond each pilot |
| Load path | Plug → shell stakes → board → two screws 11 mm either side → pad → panel → four M3 panel screws → frame. PCB-02 carries none of it |
| Clearance to PCB-02 | 1.9 mm from the 2.0 mm parts envelope, 2.6 mm from the screw heads (check) |
| Service | Remove the four panel screws and slide the panel out along −X. Reach in and unplug `W16` at J2-8 on PCB-02's +Y edge, as for the E-stop leads. The inlet stays on the panel |

`check_charge_inlet.py` passes (results in [D-040](../decisions.md#d-040) and `02-body/v1/cad/generated/charge-inlet-fit.json`). Two planted clashes were caught: parts moved into PCB-02, and the pad dropped 2.5 mm onto the panel frame. The second shows that the pad's 1.5 mm margin to the frame is real.

## 7. Sequence and faults

**Plug-in.**
1. The source sees the Rd on CC (dead-battery mode works with a flat pack) and applies 5 V. Q1 stays off.
2. The STUSB4500 negotiates the 15 V PDO, or the 9 V one.
3. After `PS_RDY` it pulls `VBUS_EN_SNK` low and Q1 ramps in about 2.5 ms.
4. `VSNK` rises. `Q_cp` asserts `CHARGE_ABSENT` = false, so the motor gate opens and `Q_dis` blocks `OPERATE` after about 3 s (RP-02).
5. The BQ25798 powers up, reads `ILIM_HIZ` and `PROG`, runs DCD and BC1.2 (DCP), measures `VINDPM`, checks `TS` and starts pre-charge or fast charge.
6. `STAT` goes low (charging), high when done, and blinks 1 Hz on a fault.

**Unplug.** `VBUS` collapses and the STUSB4500 releases Q1. `DISCH` bleeds `VSNK` within milliseconds. `Q_cp` releases and `CHARGE_ABSENT` returns.

| Fault | Result |
|---|---|
| 5 V-only or legacy USB source | No contract above 5 V, so Q1 stays off and nothing charges. The robot shows no charge (`STAT` high, `VSNK` absent) |
| 9 V-only source | Charges with the input clamp at about 1.0–1.33 A |
| Blank or corrupt STUSB4500 NVM | Requests 20 V / 1 A and enables at 5 V as well. All parts tolerate it (§5.3). Caught by the read-back gate in §8 |
| `VAC_OVP` defaults to 7 V after all | No charge at 9 or 15 V. Seen at the first bench test; needs a part change or a bench-written register (40 s only), so stop and record |
| NTC open, shorted, or pack hot or cold | Charge suspended; `STAT` blinks |
| Pack unplugged at `J-PK` | No `TS` → no charge. `SYS` held at 7 V, so C2 and the display still run from the adapter (RP-02 §4.5 finding 4) |
| Cable pulled during charge | TVS2200 clamps the inductive kick at the receptacle |
| Metal object in the receptacle | Nothing is live: no source, no `VBUS`. The BQ25798's internal reverse blocking keeps the pack off `VSNK` (OTG is off by default) |
| Plug yanked sideways | Load goes into the panel and frame; worst case is a cracked pad or PCB-13 (a 4.5 g part), not PCB-02 |

## 8. STUSB4500 NVM image

Program before PCB-13 is fitted to the panel, on a jig powered by a PD source through J1. The STUSB4500 runs from `VBUS`. Use ST's STSW-STUSB002 tool or any I2C master at 3.3 V on the test pads, address 0x28. Then read back and compare every byte.

| Field | Value | Default (for comparison) |
|---|---|---|
| `SNK_PDO_NUMB` | 3 | 3 |
| PDO1 | 5 V, 1.5 A | 5 V, 1.5 A |
| PDO2 | **9 V, 1.5 A** | 15 V, 1.5 A |
| PDO3 (highest priority) | **15 V, 1.5 A** | 20 V, 1.0 A |
| `POWER_ONLY_ABOVE_5V` | **1** | 0 |
| `REQ_SRC_CURRENT` | 0 | 0 |
| `USB_COMM_CAPABLE` | 0 | 0 |
| `VBUS_DISCH_DISABLE` | 0 | 0 |
| `SHIFT_VBUS_HL/LL`, discharge times | Defaults (5–10% / 15%; 756 / 288 ms) | |
| `PWR_OK_CFG` | Default (configuration 2) | |

Release gate: the read-back matches, and a 15 V adapter gives `VSNK` = 15 V while a 5 V-only source gives `VSNK` = 0. Store the image file, its checksum and the read-back log with the board's serial number.

## 9. Bench tests (no cells first)

Order:
1. PCB-13 alone with a PD tester.
2. PCB-13 + PCB-02 with a programmable supply in place of the pack and a 10 kΩ resistor in place of the NTC.
3. The real pack, after the TIFPS0629 acceptance.

| # | Test | Pass |
|---|---|---|
| CP-01 | NVM read-back (§8) | Byte-identical |
| CP-02 | Adapter matrix: 5 V-only, 9 V-only, 15 V, 20 V-only PD, a BC1.2 DCP brick, a laptop USB-C port | `VSNK` live only on 9/15 V contracts; 15 V chosen when offered; a 20 V-only source gives no `VSNK` |
| CP-03 | Hot plug at 15 V, 20 cycles, scope on `VBUS` and `VSNK` | Peak < 26 V; Q1 `VGS` within ±20 V |
| CP-04 | REG10 read on the bench header (one read, no write) | `VAC_OVP` = 00b (26 V) |
| CP-05 | `D+`/`D−` detection: read `VBUS_STAT` | 0011 (DCP); `IINDPM` register equals the `ILIM` clamp |
| CP-06 | Input current at a 1.4 A load on `SYS`, 15 V and 9 V | ≤ 1.40 A at 15 V |
| CP-07 | Charge voltage into a 7.5 V supply-and-load emulating the pack, at 25 °C | Taper to `VREG` 8.379–8.455 V measured at J2-1 |
| CP-08 | `TS`: decade box at the 0, 3, 8, 35, 47, 50 °C resistances; open; short | Charging suspended below 0 °C and above 50 °C (by NTC resistance); open/short suspend |
| CP-09 | `STAT` states and the 1 Hz fault blink at C2 | As §7 |
| CP-10 | Unplug under charge; `DISCH` time | `VSNK` < 0.8 V within 100 ms |
| CP-11 | Thermal: 1 A charge plus 0.9 A `SYS`, 30 min, 25 °C ambient | BQ25798 case < 85 °C; L1 < 80 °C |
| CP-12 | Full charge of the real pack, 25R pair, from 6.4 V | Terminates; each cell 4.19–4.23 V after 30 min rest; time logged |
| CP-13 | Pull and wrench on a plugged cable: 20 N axial, 10 N side (`E` test loads) | No pad crack, no board movement, `VSNK` stays up |
| CP-14 | Mechanical: three overmold samples (slim, 12 × 6 class, chunky braided) | All seat fully; none rubs the pocket |

## 10. Open

Tracked in [open-items.md](open-items.md#charge-path-pcb-13-inlet-and-the-pcb-02-charger-d-040-charge-pathmd), CP-OI-01 to CP-OI-15: schematic and layout, ST datasheets, sourcing, the NVM jig, the `VAC_OVP` default, bench CP-01 to CP-14, the hot-room charge decision, PCB-02 mounting, the adapter, plug-fit and pull tests, the chassis-model copy, the STEP rebuild and PCB-02 area.

## Appendix: TS divider search

The divider in §5.4 came from an E96 search for the widest window that keeps every corner inside 0–50 °C. It interpolates ln R linearly in 1/T between the catalogue points and applies B ±1% about 25 °C. The script is kept at [`charge-path-ts.py`](charge-path-ts.py).
