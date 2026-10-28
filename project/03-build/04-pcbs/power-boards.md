# Power boards — build deltas (PCB-01 to PCB-04)

| Field | Value |
|---|---|
| Status | Working design, 2026-10-03 ([D-038](../decisions.md#d-038)). No schematic, layout or bench result |
| Reference | [RP-02 board-specs.md](../../02-prototypes/RP-02-electrical/board-specs.md) v0.17 (read-only). Everything there stands unless this page changes it |
| Why this page exists | The RP-02 spec was written for a custom PCB-01, Pololu DRV8874 carriers and the Pololu #4804 motor. The build uses the bought TIFPS0629 ([D-019](../decisions.md#d-019)), Adafruit #3297 DRV8833 boards (D-019) and the MOT3001-6V230RPM ([D-003](../decisions.md#d-003)) |
| Evidence labels | `D` datasheet, `E` estimate, `U` unknown, `W` measured. No `W` value exists yet |
| Charge path | PCB-02's charger block and the new PCB-13 inlet are in [charge-path.md](charge-path.md) ([D-040](../decisions.md#d-040)) |
| Power button | The rear mushroom is the `LTC2954` `PB` input and a hardware motor stop; there is no E-stop. `J2-9`, the arm-latch reset and the permit-chain change are in [§6](#6-pcb-02-power-button-input-d-041) ([D-041](../decisions.md#d-041)) |

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
- The pack disconnect (CH-027) is 2-circuit power only, so the NTC has its own 2-pin lead and a JST SM 2-way break in the +Y channel ([D-039](../decisions.md#d-039), [05-harness](../05-harness/README.md)).

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

## 4A. Feetech actuator rail delta (D-046/D-047, 2026-10-07)

This build delta supersedes the **XC330-only loads and settings** in read-only RP-02 §5.4. The companion [actuator screen](../03-head/v1/feetech-actuator-screen.md) records the sourced servo values and open P01–P09 gates. Values below are paper design targets, not a schematic sign-off or measured converter capability.

| Rail | Load and limit | Design consequence |
|---|---|---|
| `PB-HEAD-PR` | Two STS3045Ms at 5.5 V setpoint; 1.4 A stall each at their **6 V datasheet point** (`D`), so 2.8 A is a conservative aligned-fault allowance until measured at 5.5 V | It feeds **pitch and roll only**. `PB-SAFE-C2` and `PB-DISPLAY` remain separate PCB-04 branches, although their conductors share `J8-1`/`W42`. Remove yaw from the old 5 V head-rail budget |
| `PB-YAW-12` | One ST3215-HS, 12 V target at its terminals, 240 mA no-load running and 2.4 A locked-rotor at 12 V (`D`) | Add a **second** LTC3119 on PCB-03, upstream latching input protector, local output bulk and active braking clamp; do not route its 12 V through the yaw FFC cassette |

**Head setpoint.** Keeping the 102 kΩ lower feedback resistor and using approximately 604 kΩ above `FB` gives `0.795 × (1 + 604/102) = 5.50 V` nominal. Applying the old ±2.18% converter-output tolerance gives 5.38–5.62 V, then the registered 150 mV maximum drop gives **5.23 V minimum at a servo terminal**. Re-derive the resistor-tolerance corner and compensation in the schematic; this arithmetic is a target. Move the old 5.74 V regeneration clamp to approximately **5.9 V**, with the entire clamp-tolerance band above the 5.62 V output high corner and below the STS3045M 7.4 V ceiling. Verify transient overshoot on both terminal points, not only at PCB-03. Retain the forced-PWM / zero-reverse-current assumption; the LTC3119 is not an energy sink.

**Yaw converter capability.** A 2.0 A yaw output is 24 W. At 5.4 V pack input and an assumed 88% efficiency it draws `24/(5.4×0.88)=5.05 A`; 2.4 A locked rotor requires **6.06 A** before inductor ripple. Against the LTC3119's fixed 7–8 A *inductor peak* limit, 2 A is a planning ceiling, not a guaranteed low-pack continuous output. At 2 A, the converter loses about `24×(1/0.88−1)=3.27 W`, considerably above the old head rail's roughly 1 W at 2 A. The second converter needs its own thermal copper, inductor saturation check, load-step compensation, minimum-input current test and PCB-03 56 × 44 mm placement check. A 2.4 A motor stall is beyond the planning ceiling: set the Feetech protection-current register below a **bench-verified** input/current/thermal limit and keep the hardware input protector latching. Do not infer the permissible register count from this power estimate alone.

**Yaw braking.** The 12 V rail cannot accept sustained reverse current from the servo. Size a local clamp and dump path after measuring the servo's deceleration energy and converter overshoot. The 12.6 V servo maximum leaves only 0.6 V above nominal, so clamp tolerance, regulation high corner, harness drop and TVS dynamic resistance must be solved together. Until that circuit is validated, do not tie the yaw rail to the head clamp or claim an exact clamp threshold.

**11.1 V candidate setpoint.** Reducing the yaw rail from 12.0 to 11.1 V would leave 1.5 V nominal to the 12.6 V servo maximum. With the inherited ±2.18% output tolerance, the high corner is about 11.34 V, leaving 1.26 V before braking-clamp tolerance; the 12 V design leaves only 0.34 V at its high corner. This is a useful clamp-design candidate, not a selected rail or a validated brake circuit. Scaling both published 12 V torque and speed endpoints linearly and retaining the unvalidated 0.86 graph factor gives about **2.53×** yaw torque margin at 11.1 V nominal against the current 0.22 N·m demand, and about **2.28×** at a 10.71 V terminal low corner (±2.18% and 150 mV assumed drop). The suggested 2.8× does not follow from that same proxy. New mount mass and the actual HS curve may reduce these margins. At 11.1 V, 2.0 A output is 22.2 W, about 4.67 A from a 5.4 V pack at 88% efficiency; treating the 12 V 2.4 A stall current as a conservative load gives 5.61 A. Decide the setpoint with B1/B2 torque-speed data and a measured braking transient.

**Overload and observation.** A single stalled head servo draws up to 1.4 A at the 6 V reference, leaving 1.4 A for the other on the 2.8 A synthetic head allowance. The old 4 A `HEAD_OC` threshold is above both head-servo stalls and therefore cannot detect this fault by itself; retune only after B1 current traces establish legitimate coincident peaks. The old `INA180A2` 10 mΩ / gain-50 head monitor yields 0.5 V/A and 1.4 V at 2.8 A, so its analog range is adequate on a 3.3 V ADC, but its comparator threshold and shunt power must be recalculated. **Yaw needs a separate 12 V branch monitor**; the old pitch/roll-plus-yaw grouping and Dynamixel Current Limit settings no longer apply. At 5.4 V input, simultaneous 2.8 A head stall and 2 A yaw output would demand about `(5.5×2.8 + 12×2)/(5.4×0.88) = 8.29 A` from the pack before drives, Pi or display. The 15 A main fuse remains a wiring protector, not a servo stall limiter. Check the upstream gate and pack sag against this combined fault during B5.

**Runtime delta.** When yaw actually runs unloaded at 240 mA, it takes 2.88 W at 12 V; at 88% conversion efficiency that is 3.27 W from the pack, or about 0.61 A at a 5.4 V pack. This is a duty-dependent addition to the energy ledger, not a continuous sleep load. The old 5 V yaw servo demand leaves the head rail, so a net runtime figure needs the motion-duty timeline and measured currents on all three axes. Record a revised Wh budget before claiming the 9.2 Wh mission target.

**Protection model.** The Feetech register plan, command-age latch and absence of a direct Dynamixel Bus Watchdog equivalent are in the actuator screen. The old RP-02 BD-13 five-layer argument is retired for these selected servos. Hardware permit, input protector, converter limit and current observation still exist, but servo unload and firmware response must be characterized as a new fault chain at B5.

## 5. Open

- [ ] TIFPS0629 bench acceptance (§3) on two received units: trip thresholds, delays and release, quiescent current (completes the §4 OFF budget) and measured height (replaces D-026's 2.9 mm). Update CH-023 with the `W` values.
- [ ] MOT3001 winding resistance and inductance on receipt; recheck §2.2 and §2.6.
- [x] CAD labels: `J10-5`/`J10-6` carry the §2.4 mapping in `body_v1_model.py` and `body_chassis_model.py` (label strings only, no geometry).
- [x] SMBJ8.5A leakage (§2.2) and the current-monitor reference (§2.5) are now taken from the datasheets.
- [ ] Schematic: 74LVC1G08 placement on PCB-10; INA2181 output routing to the C2 ADC (RP-02 §8 pins still open).
- [x] Pack NTC inline break beside `J-PK` (CH-025): JST SM 2-way pair in the +Y channel, CAD reserve added, `check_harness.py` ALL PASS ([D-039](../decisions.md#d-039)).
- [ ] PCB-02/PCB-03 feed entry changed by [D-039](../decisions.md#d-039): `BATBUS` reaches `J3-1` and `J2-1` separately from a star splice beside the fuse, and `J2-2` is deleted. Pinouts for every board connector are in [05-harness §5](../05-harness/README.md#5-pinouts); carry them into the schematics.
- [ ] Power button (§6, [D-041](../decisions.md#d-041)): add `J2-9`, `R_WET` and the `INT` → `SYSTEM_ARM` reset to the PCB-02 schematic, and the 0 Ω link in place of the E-stop loop to PCB-03; delete `J3-7`. Bench PB-01 to PB-06.

## 6. PCB-02 power-button input ([D-041](../decisions.md#d-041))

The red mushroom on the rear panel is the power button. **There is no E-stop.** The button is the `PB` input of the RP-02 `LTC2954-2` latch (board-specs §4.1–4.2). The latch, its `ONT`/`PDT` capacitors, `KILL`/`INT` and the charge-time blocks are unchanged. This section lists what the build changes.

**Button (BO-018).** A 16 mm momentary red mushroom pushbutton, 1NO, silver-alloy contacts. It replaces the IDEC XA1E-BV3U02KT-R, which is a push-lock, turn-reset E-stop with two NC contacts. That part cannot drive a latch that needs a momentary NO contact. The replacement must fit the existing well: Ø16.2 cut-out, 2 mm floor, mushroom Ø30 or less and 20.6 mm or less above the floor, 23.9 mm or less behind it.

**`J2-9`.** A side-entry GH2 (SM02B-GHS-TB) on PCB-02's +Y edge, centred at Z 88.6, above `J2-8`. The plug exits +Y.

| Pin | Net | On PCB-02 |
|---|---|---|
| 1 | `PB_SW` | 5.1 kΩ to `LTC2954` `PB`, 0.1 µF at `PB` (RP-02 values). **Add `R_WET` 10 kΩ from the latch `VIN` (`BATBUS`) to `PB_SW`** |
| 2 | GND | Signal ground at the latch |

**Why `R_WET`.** The `PB` pin has an internal 100 kΩ pull-up to 1.9 V, so a press passes about 19 µA (`D`, LTC2954 datasheet). That is a dry circuit for silver contacts. A 10 kΩ pull-up to `VIN` raises the press current to 0.84 mA at 8.4 V. It draws nothing while the button is released, because the contact is open. The datasheet recommends a 10 kΩ pull-up to `VIN` against board leakage (Fig. 9), and `PB` accepts up to 26.4 V "without consuming extra current" (`D`). The `OFF` budget is unchanged.

**The press is also a hardware motor stop.** `INT` (open drain) also resets the `SYSTEM_ARM` latch on PCB-02. RP-02 cleared that latch on an E-stop assertion; the button press takes that place. A press in `OPERATE` therefore opens `Q_ARM` in the permit chain, and the `LTC4368` cuts the motor and head bus through its fast `UV` pull-down. No firmware is involved. The arm latch never re-arms on release (RP-02 F-13), so motion resumes only after a fresh arm request from C2.

**Permit chain.** The E-stop NC contact at the head of the RP-02 chain (board-specs §5.2.3) is replaced by a fitted 0 Ω link on PCB-03. The chain becomes `5 V → 470 Ω → Q_ARM → Q_CHG → Q_EN → Q_C2H → Q_C2L → Q_BASE → PERMIT`. `MOTOR_PERMIT` loses its `E_STOP_OK` term (`BR-05`).

**Connectors removed:**
- PCB-03 `J3-7` and the `W22` lead (the E-stop loop and status).
- `W38` and C3 `J10-11` (the E-stop status to C3) are not fitted.
- The `E_STOP_STATUS` pin on `J3-8` is spare.

**Press behaviour** (`ONT` 82 nF, `PDT` 0.82 µF, RP-02):

| Action | Result |
|---|---|
| Hold about 0.5 s in `OFF` | `EN` asserts and `OPBUS` comes up |
| Any press in `OPERATE` | After 32 ms `INT` goes low and stays low while held. The motor and head bus cut at once (hardware, above). **C2 firmware starts an orderly shutdown only if `INT_PB` stays low for 1 s or more**; a shorter press only stops motion |
| Hold about 5.2 s | The latch releases `EN` itself, even if C2 is hung |
| Any press in `CHARGE` | Nothing. `Q_kill` holds `KILL` low (RP-02) |

The button has no light. The head display shows the power state.

**Bench (before the panel is fitted):**

| # | Test | Pass |
|---|---|---|
| PB-01 | Contact current on press, at `J2-9` pin 1 | 0.8–0.9 mA at 8.4 V |
| PB-02 | Turn-on hold time, 20 presses each at 0.3 s and 0.8 s | 0.3 s never turns on; 0.8 s always does (`tDB,ON` + `tONT` ≈ 0.56 s, `E`) |
| PB-03 | Press while the drive and head are moving, with C2 halted | Motor bus off within 50 ms of the press; no re-arm on release |
| PB-04 | Firmware filter: 0.2 s and 1.5 s presses in `OPERATE` | 0.2 s stops motion only; 1.5 s gives an orderly shutdown |
| PB-05 | 5.2 s force-off with C2 halted | `OPBUS` drops |
| PB-06 | ESD on the mushroom and bezel, ±8 kV air, in `OFF` and `OPERATE` | No turn-on, no shutdown, no latch-up |
