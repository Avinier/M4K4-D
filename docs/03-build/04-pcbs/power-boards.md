# Power boards — build deltas (PCB-01 to PCB-04)

| Field | Value |
|---|---|
| Status | Working design, 2026-10-03 ([D-038](../decisions.md#d-038)). No schematic, layout or bench result |
| Reference | [RP-02 board-specs.md](../../02-prototypes/RP-02-electrical/board-specs.md) v0.17 (read-only). Everything there stands unless this page changes it |
| Why this page exists | The RP-02 spec was written for a custom PCB-01, Pololu DRV8874 carriers and the Pololu #4804 motor. The build uses the bought TIFPS0629 ([D-019](../decisions.md#d-019)), Adafruit #3297 DRV8833 boards (D-019) and the MOT3001-6V230RPM ([D-003](../decisions.md#d-003)) |
| Evidence labels | `D` datasheet, `E` estimate, `U` unknown, `W` measured. No `W` value exists yet |

## 1. Build baseline that replaces RP-02 assumptions

| Item | RP-02 spec | Build |
|---|---|---|
| Pack protection | Custom PCB-01: S-8252AAC + BQ29200, published trips | Robocraze TIFPS0629 module, **no published trips** (CH-023); acceptance in §3 |
| Drive driver | 2 × Pololu 4035 DRV8874, VM 4.5–37 V, `CS` 1.13 V/A, 4.4 A limit | 2 × Adafruit #3297 DRV8833, both bridges paralleled per board (CH-017); §2 |
| Drive motor | Pololu #4804, 6 A extrapolated stall | MOT3001-6V230RPM, about 1.8 A stall at 6 V (`E`, D-003) |

## 2. PCB-03 drive feed for the DRV8833

### 2.1 Driver facts (`D`, TI SLVSAR1E and the Adafruit #3297 guide)

- VM recommended 2.7–10.8 V; **absolute maximum 11.8 V**; UVLO 2.6 V maximum.
- 1.5 A RMS / 2 A peak per bridge (PWP package); 3 A RMS / 4 A peak with the bridges paralleled.
- Chopping limit `I = VTRIP / R_SENSE`, `VTRIP` 160–240 mV. The #3297 fits 0.2 Ω sense resistors, so each bridge chops at 0.8–1.2 A and **each paralleled board at 1.6–2.4 A** (nominal 2 A, as the chassis BOM already says).
- Overcurrent trip 2 A minimum per bridge, then **automatic retry after 1.35 ms**. `nFAULT` is open drain and also asserts on UVLO and over-temperature.
- `nSLEEP` has an internal 500 kΩ pull-down (asleep by default), a 6.5 V clamp and **`VIH` 2.5 V minimum**. Wake takes up to 1 ms.
- The #3297 brings out `VM` (unprotected) and a terminal-block `Vmotor` behind "simple polarity protection".

### 2.2 Bus TVS: SMBJ10A → SMBJ8.5A

The RP-02 SMBJ10A (breakdown 11.1–12.3 V, clamp 17.0 V at 35.3 A) was checked against the DRV8874's 40 V rating. It starts conducting at or above the DRV8833's 11.8 V absolute maximum, so it protects nothing.

**Change: SMBJ8.5A** (600 W, unidirectional), cathode on the motor bus, load side of the gate. Its standoff is 8.5 V. Breakdown is 9.44 V minimum, with a maximum of 10.4–10.8 V depending on the maker. It clamps at 14.4 V at 41.7 A (`D`).

- **Normal operation.** The bus never exceeds the pack's 8.4 V: the charger cannot reach the bus (`CHARGE_ABSENT`), so the 8.455 V charger worst case does not apply. Leakage is at most 20 µA at 8.5 V (`D`, Littelfuse). That is at most 0.17 mW while armed, and nothing in `OFF` because the bus is dead.
- **Clamp at credible current.** The dynamic resistance is about (14.4 − 10.4) / 41.7 ≈ 0.1 Ω, so the clamp is about 10.9–11.3 V at 5 A (`E`). That leaves 0.5–0.9 V below 11.8 V, which is tight, so the bus capacitance must take most of the energy (next item).
- **Worst credible surge: both drivers released at the chopping limit** (permit loss, `nSLEEP` low). The winding inductance is `U`. At an assumed 3 mH per motor, the stored energy is 2 × ½ × 3 mH × 2.4² ≈ 17 mJ (`E`).
  - Into the 1000 µF bus, from 8.4 V: √(8.4² + 2 × 0.017 / 0.001) ≈ 10.2 V. The TVS barely conducts.
  - Into the 400 µF low case: about 12.5 V without the TVS, so the TVS is needed there.
  - **Keep at least 100 µF + 0.1 µF at each #3297 `VM`, as in the 1000 µF bus estimate.** Measure the winding inductance on receipt.
- The LTC4368 `OV` at 9.55 V rising (9.07 V release) sits below the DRV8833's 10.8 V: no change. LTC3119 `PVIN` (19 V maximum) is unaffected.

### 2.3 Power entry

Feed `PB-DRIVE-L/R` (W06/W07, J3-2/J3-3) to the #3297 **`VM` pin**, not the terminal-block `Vmotor`:

- The polarity device on `Vmotor` is unspecified (`U`). A series diode would block regeneration from returning through the bidirectional gate, and it would add drop.
- Polarity comes from the keyed Micro-Fit+.
- Solder the 100 µF + 0.1 µF at `VM`/`GND`.

### 2.4 Logic to C3 (J10-5 / J10-6, GH 6)

The registered C3 pin map (RP-03 `base-control-architecture.md` §3.2) is kept; no MCU pin is added.

| J10-5/6 pin | Signal | Rule |
|---|---|---|
| 1 | `SLP` | Both boards are driven from one **74LVC1G08 AND gate** on PCB-10: inputs C3 GPIO21 (`nSLEEP`) and `BASE_READY`, each with a 100 kΩ pull-down, powered from the carrier 3V3. **This replaces the series `BASE_READY` N-FET stages** (connector-schedule §3.3): a 3.3 V level passed through an N-FET reaches only about 3.3 V − `VGS(th)`, below the DRV8833's 2.5 V `VIH`. Unpowered, unplugged or not ready, the output stays low and the internal 500 kΩ keeps the driver asleep |
| 2 | `IN1` (`AIN1`+`BIN1` joined on the board) | GPIO11 (left) / GPIO12 (right), LEDC |
| 3 | `IN2` (`AIN2`+`BIN2` joined) | GPIO13 (left) / GPIO14 (right). **Was a DIR pin; it becomes a second LEDC output.** The DRV8833 has no PH/EN mode, and symmetric slow decay needs PWM on whichever input is not held high |
| 4 | `FLT` | Both boards wired-OR to GPIO9 with a 10 kΩ pull-up to 3V3 on PCB-10. Firmware **latches** any low: both inputs low, `nSLEEP` low, fresh arm required. This defeats the chip's 1.35 ms auto-retry, per the no-auto-retry policy |
| 5 | `GND` | Signal ground |
| 6 | spare | Not connected |

Drive modes: forward `IN1 = 1, IN2 = PWM` (slow decay); reverse `IN1 = PWM, IN2 = 1`; brake `1, 1`; coast `0, 0` only at standstill or before sleep.

**Speed clamp.** The 6 V winding on an 8.4 V bus overspeeds by 8.4 / 6 = 1.4×. C3 limits the effective duty to `6.0 V / V_bus` (71% at 8.4 V) and reads `V_bus` from the pack sense.

### 2.5 Current observation

The DRV8833 has no current output, and the #3297 sense nodes only carry the bridge's drive-phase current (unsigned). They are left on their 0.2 Ω resistors as the hardware limit and are not wired out.

- **Add one TI INA2181A2 on PCB-03 for both drive feeds.** It is the dual INA181, gain 50, with a separate `REF` pin per channel and 500 µA maximum supply (`D`). Each feed gets a 5 mΩ high-side shunt, so the output is 0.25 V/A around 1.25 V, spanning 0.75–1.75 V for −2…+2 A. Common mode is −0.2 to 26 V; offset is ±150 µV and gain error ±1% (`D`).
  - **Reference:** a TI REF3312 (1.25 V, ±0.15%, sources and sinks ±5 mA, 3.9 µA, `D`) drives both `REF` pins.
  - **Supply:** the amplifier and reference run from a local 3.3 V LDO (TLV75533P class) on the PCB-03 permit-chain 5 V (`PB-SAFE-C2`). The output cannot exceed 3.3 V, so a feed fault cannot overdrive the receiving ADC; on a 5 V supply it would pass 3.3 V above about 8.2 A. Nothing is drawn in `OFF`.
- The outputs go to test points and join the per-branch current set routed under RP-02 §8 (pins still open). They are not on C3: RP-03 keeps current sensing off the C3 MCU in v1.
- Shunt drop is 12.5 mV at 2.5 A.

This keeps the signed per-branch observation (`PA-08`) and the ledger's signed-regeneration measurement, which the DRV8874 `CS` used to provide.

### 2.6 Regeneration (replaces RP-02 §5.2.4 / §5.3 rule derivation)

The rule is unchanged: at most **3 A** into the bus (75% of the cell's 4 A charge maximum) and **zero below 0 °C**. The MOT3001 meets it with margin (`E`; winding R = 6 V / 1.8 A ≈ 3.33 Ω, unmeasured):

- **Slow-decay deceleration.** Synchronous PWM pumps current back into the bus at most `E_b² / (4 · V_bus · R)` per motor. The speed clamp keeps back-EMF `E_b ≤ 6 V`, so this is ≤ 36 / (4 × 8.4 × 3.33) ≈ **0.32 A** at a full pack and ≤ **0.45 A** at a 6.0 V bus. **Both motors: ≤ 0.9 A.**
- **Coast / body-diode path.** It only conducts when `E_b > V_bus + 2·V_f`. Returning 1.5 A per motor would need `E_b` ≈ 8.4 + 1.4 + 1.5 × 3.33 ≈ 14.8 V, which is 2.5× the clamped speed. Not credible by pushing the robot.
- **Brake (`1, 1`).** Shorts the winding; the energy stays in the motor and bridge.
- **Below 0 °C (pack NTC).** C3 decelerates by brake and coast only, with no synchronous decel PWM.

### 2.7 Brownout floor

`V_SRC_SAFE` 4.6 V came from the DRV8874's 4.5 V minimum. The DRV8833 runs to 2.7 V, so the floor is now set by the gate (4.0 V) and the Pi converter (4.26 V). The RP-02 §8.1 thresholds (`UV` 4.9 V, `ENERGY_OK` 5.7 V, soft critical 6.0 V) are unchanged.

## 3. PCB-01 = TIFPS0629: acceptance before cells are connected

The listing gives 20 A continuous discharge, 10 A charge, balancing, "charging voltage 8.4–9.0 V" and 48 × 20 mm, and **no trip points** (`D`, listing read 2026-10-03). Bench-measure every row on two units (one spare) with a programmable supply in place of the cells, and record the results as `W` in CH-023.

| Property | Accept | Reason |
|---|---|---|
| Overcharge trip, per cell | **4.275–4.35 V**, delay ≥ 0.5 s | Worst cell at end of default-mode charge is 4.250 V (RP-02 §3.3); the BQ29200 secondary is gone, so above 4.35 V reject the module or add a secondary |
| Over-discharge trip, per cell | **2.30–2.70 V**, delay ≥ 10 ms | The pack must cut out last. `ENERGY_OK` falls at 5.53 V minimum, so 2.765 V per cell less the 22.5 mV balance band. A typical 2.8–3.0 V generic trip would drop the Pi in a sag before the system's own stop |
| Discharge overcurrent, sustained | **≥ 20 A preferred; 15–20 A acceptable; < 15 A reject**, delay ≥ 5 ms | At ≥ 20 A the motor gate (13.3–20 A, about 8 µs) always opens first. 15–20 A overlaps the gate, as the RP-02 custom design also did. 15 A is about 1.5× the 10.2 A rebuilt peak (§4) |
| Short circuit | Trips at ≥ 40 A within ≤ 1 ms | The fuse is a wiring protector only |
| Series resistance | ≤ 30 mΩ at 5 A | Pack model allowance (2 · 22 + 30 + 10 mΩ) |
| Quiescent from the cells | **≤ 16 µA** keeps the 100 µA OFF maximum; ≤ 50 µA tolerable (§4) | OFF budget |
| Balancing | Starts only above 4.1 V per cell; record current and start mismatch | Balancing at low charge drains the pack |
| Release after over-discharge | Releases when the BQ25798 pre-charges (it holds about 2.5 V per cell at up to 100 mA for 1.5 s) | RP-02 §3.7 recovery path |
| Height including parts | ≤ 4.5 mm; replaces the 2.9 mm placeholder (D-026) | Tub clearance |
| Temperature input | Record; none expected | See below |

**Temperature.** The module is not expected to have an NTC input, so the RP-02 split stays:

- The AC72ABD (CH-024) sits in the cell-negative strap, bonded to a cell. It sits outside the module's current-sense path.
- The 103AT-2 (CH-025) goes to the BQ25798 `TS` input on PCB-02.
- The pack disconnect (CH-027) is 2-circuit power only, so the NTC needs its own 2-pin lead and disconnect (CH-025, still open).

## 4. Rebuilt numbers (`E`)

**Peak pack current at a 6.0 V pack, η 0.9** (`I = P / (η · V)`):

| Load | Pack current |
|---|---|
| Pi 5 (5.15 V × 2.4 A) | 2.3 A |
| Head (2 A allowance at 5 V) | 1.85 A |
| Display + audio crest + C2 + C3 | 2.0 A |
| Both drive boards at the nominal 2 A chopping limit (direct, no converter) | 4.0 A (4.8 A at the 2.4 A upper corner) |
| **Total** | **≈ 10.2 A** (11.0 A upper corner) |

This is below the RP-02 historical 11.7 A. The 15 A ATOF main fuse (CH-029) and the 3 mΩ gate shunt are unchanged.

**OFF budget with the module.**

| | Typical | Maximum |
|---|---|---|
| BQ25798 | 17 µA | 24 µA |
| LTC2954 | 6 µA | 12 µA |
| LTC4368 and its divider | 11 µA | 48 µA |
| TIFPS0629 | `U` | `U` |
| **Total** | **34 µA + module** | **84 µA + module** |

At a 16 µA module the maximum is 100 µA, which is 2.9% of 2.5 Ah per month. At a 50 µA module it is 134 µA, or 3.9% per month.

## 5. Open

- [ ] TIFPS0629 bench acceptance (§3) on two received units: trip thresholds, delays and release, quiescent current (completes the §4 OFF budget) and measured height (replaces D-026's 2.9 mm). Update CH-023 with the `W` values.
- [ ] MOT3001 winding resistance and inductance on receipt; recheck §2.2 and §2.6.
- [x] CAD labels: `J10-5`/`J10-6` carry the §2.4 mapping in `body_v1_model.py` and `body_chassis_model.py` (label strings only, no geometry).
- [x] SMBJ8.5A leakage (§2.2) and the current-monitor reference (§2.5) are now taken from the datasheets.
- [ ] Schematic: 74LVC1G08 placement on PCB-10; INA2181 output routing to the C2 ADC (RP-02 §8 pins still open).
- [ ] Pack NTC inline break beside `J-PK` (CH-025; RP-06 connector-schedule §5 item 1): choose the 2-circuit wire-to-wire part and add a CAD reserve, then run the targeted pack checks.
