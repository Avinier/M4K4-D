# RP-03 Sensing Candidate Screen — S01…

| Field | Value |
|---|---|
| Status | **Paper screen complete v0.1. No sensor selected. No freeze. No purchase.** Stop-path leads are classes with mandatory trials, not SKUs |
| Date | 2026-09-17 |
| Scope | Named cliff / obstacle / bump / IMU rows `S01…` screened against `physics.md` §6–7 coverage and the 50 ms invariant, and against the C3 I/O budget. Bus sharing is allowed for **telemetry**, never for a stop-path input |
| Inputs | `physics.md` stopping table and leading-contact geometry; `storyboard.md` `BM-10`/`BM-11`; `concepts/` (A: 3 look-downs + analog-IR stop-path; B: ring + ToF telemetry); C3 = ESP32-S3-DevKitC-1-N8 (`RP02-P3-REG-02`); CA-11/12 |
| Evidence | Manufacturer datasheets `D`. India Robu / Zbotic 2026-09-17 snapshot is availability, not a rating. Prices ranges `E`. Exact stock `U` |
| Excluded | A sensor chosen because a driver board has the pins; a GPIO expander in the stop path; a freeze of age bounds; purchase |

Dark or glossy tabletop is the cliff **failure mode to test**, not an afterthought. A paper PASS that has not named that trial is not a PASS.

## 1. Envelope this screen is scored against

Copied, not re-derived. Score with **`t_latency = 50 ms`** (CA-12 invariant), not the optimistic 35 ms sum (`physics.md` §6.1).

### 1.1 Stopping distances (`physics.md` §6.2)

`a_brake = 1.20 m/s²` authored; `d_margin = 50 mm` floor; 40 mm tabletop.

| `v` (m/s) | `d_stop` (mm) | What the sensor must do |
|---:|---:|---|
| 0.05–0.06 calibration | **45–54** floor; **~44** tabletop | Cliff look-ahead **~40 mm before each leading contact** |
| 0.50 follow cap | **179** | Obstacle look-ahead from **caster/ball contact** ≥ 179 mm (axle-mounted needs +110 → 289 mm — do not credit) |
| 0.70 design point | **289** | From contact ≥ 289 mm. Axle-mounted ≥ 399 mm |

### 1.2 Leading contacts (`physics.md` §7.1)

| Direction | Leading contact | Offset |
|---|---|---|
| Forward | Caster / ball | **110 mm** ahead of axle |
| Lateral / pivot | Wheels | **0 mm** ahead, **85 mm** off centre; stance sweep ~102 mm |
| Reverse | Skid | **70 mm** behind axle |

Minimum look-downs: **three** (caster-forward, reverse/skid, one lateral). A perimeter ring is Concept B, not a requirement of this screen. A single forward cliff is not enough.

Blind-region: 20 mm square × 20 mm tall in the front-support shadow. Bumper is **last** layer. Do not close G03 with bump-only at follow speed.

### 1.3 Age bounds (`E`, not registered)

Unknown = inhibit. These are hypotheses for Part 4 fusion, not G05 thresholds.

| Channel | Bound `E` | Basis |
|---|---:|---|
| Cliff GPIO | **10 ms** | Digital/phototransistor sample; faster than analog IR; do not score the whole invariant at 1 ms |
| Analog IR | **25 ms** | One Sharp cycle 16.5 ± 3.7 ms `D` + scan |
| Bump | **5 ms** | Mechanical + GPIO; last layer |
| IMU sample | **10 ms** | Data-ready INT, not a UART angle packet |
| ToF (telemetry) | 20–50 ms | Must **not** be treated as the stop-path sample age |

### 1.4 C3 I/O budget check

Prototype board: ESP32-S3-DevKitC-1-N8. Pin map is a hard pre-carrier gate and must retain **≥ 2 unassigned safe GPIO**. No safety input behind a GPIO expander. Strapping GPIO0/3/45/46 excluded from safety outputs.

**Concept A working-lead set (this screen's lead combination):**

| Signal | Count | Stop-path? |
|---|---:|---|
| Cliff GPIO (3 look-downs) | 3 | Yes |
| Analog obstacle (ADC) | 1 | Yes |
| Bump GPIO | 1 | Yes |
| IMU SPI (CS, SCLK, MOSI, MISO) + INT1 | 5 | Slip/lift; not a cliff substitute |
| Driver nFAULT × 2 | 2 | Fault |
| Driver enable (fail-safe inhibit) | 1 | Arm |
| **Subtotal named here** | **13** | — |

Fits the planned Part 4 map against ~28 assignable header GPIO with **≥ 2 spare**, provided encoder A/B × 2 (4), PWM/PH × 2, and link/watchdog/READY still leave two free. That arithmetic is repeated in Part 4; this screen only claims the **sensing slice** does not, by itself, blow the budget.

ToF I2C is **extra telemetry** if GPIO remains ≥ 2 spare. It does not replace a cliff GPIO.

Concept B's 4+ cliff GPIO **plus** the same bump/IMU/nFAULT/enable set spends the spare. That is a Part 4 / carrier problem, not a license for an expander.

## 2. Outcome (not a selection)

| Function | Lead carried forward | Disposition |
|---|---|---|
| GPIO cliff | TCRT5000-class look-down (`S01`) | **Lead** for GPIO cliff **with a mandatory dark+glossy trial**. Failure mode is reflectivity, not geometry |
| GPIO cliff comparison | QRE1113 (`S02`) | **Comparison**. Tighter geometry (~1 mm mirror `D`) |
| Downward ToF as cliff | VL53L0X (`S03`) | **Reject as sole stop-path cliff** (bus + surface + latency) |
| Obstacle stop-path | GP2Y0A41SK0F analog IR (`S04`) | **Lead** obstacle stop-path on ADC. **PASS** at 0.50 if caster-mounted. **HOLD** at the 0.70 design point (289 vs 300 mm max) |
| Forward ToF | VL53L1X (`S05`) | **Conditional** telemetry / redundant look-ahead. **Not** sole stop-path |
| Bump | Miniature lever / microswitch spanning stance (`S06`) | **Lead** bump, last layer, direct GPIO |
| Base IMU | ICM-42688-P SPI + INT1 (`S07`) | **Lead** IMU. UART-MCU modules (Robu 601N1 class) are **not** the same article — reject UART-angle-output as the stop-path IMU |
| IMU fallback | MPU-6500 module (`S08`) | **Fallback only if SPI+INT is actually wired**. Many India boards are I2C-only |

## 3. Disposition vocabulary

| Label | Meaning |
|---|---|
| **Lead** | Best current implementation candidate for that function; not frozen, not purchased |
| **Conditional** | Admissible if the stated restriction holds (telemetry only, SPI actually wired, …) |
| **Comparison** | Kept to falsify the lead's geometry or interface |
| **Fallback** | Change-controlled substitute after the lead fails a stated criterion |
| **Reject** | Violates a stop-path, latency, or coverage rule for the stated use |

## 4. Candidate register

### 4.1 `S01` — TCRT5000 look-down cliff

**`D`:** Vishay TCRT5000 / TCRT5000L, [datasheet](https://www.vishay.com/docs/83760/tcrt5000.pdf). Phototransistor, emitter **950 nm** (peak λ typically 940 nm at `IF = 100 mA`). Peak operating distance **2.5 mm**; useful range **0.2–15 mm** (relative collector current > 20 %). Package 10.2 × 5.8 × 7 mm. Emitter test conditions include `IF = 10–60 mA`. GPIO analog or digital (comparator / ADC / digital with a threshold).

**Stop-path:** **OK** — native GPIO, no bus, sample age bound 10 ms `E`.

**Coverage:** A look-down does not *range* 40 mm; it reports floor-present at a patch **placed** ~40 mm before the contact. Mounting geometry is the coverage. Three channels at caster / skid / one wheel-adjacent match Concept A and `physics.md` §7.5.

**Failure mode (mandatory trial):** measures **reflectivity**, not geometry. **Glossy black can look like floor; matte white can look like a drop.** Dark and glossy tabletop samples are the cliff failure mode (`physics.md` §7.5, CON-TBD-14 proposal). A PASS without that trial is not a PASS.

**Emitter current:** ~10–60 mA `D` class. Three channels pulsed at 200 Hz hazard scan must stay inside `LG-10` (still `U` until bench). Continuous-on three emitters is a flag against `PB-SAFE-BASE` and the ≤ 1 W ledger line.

**India snapshot 2026-09-17.** TCRT5000 is India-common (Robu / generic). Price band `E` ₹10–50. Stock `U`.

**Disposition: Lead for GPIO cliff, with a mandatory dark+glossy trial.** Not a SKU freeze (TCRT5000 vs TCRT5000L vs a comparator breakout).

### 4.2 `S02` — QRE1113 look-down

**`D`:** onsemi QRE1113, [datasheet](https://www.onsemi.com/pdf/datasheet/qre1113-d.pdf). Phototransistor. **Designed / specified at d = 1 mm** on an aluminium-alloy mirror. Rise/fall ~20 µs. SparkFun analog breakout states optimal ~3 mm — that is a module, not the die spec.

**Stop-path:** OK on GPIO, same as `S01`.

**Coverage:** Even **tighter** geometry than TCRT's 2.5 mm peak / 15 mm useful. Harder to place ~40 mm look-ahead with a 1 mm design distance; easier to bury in a carrier that sits 1–3 mm off the floor. Dark/glossy failure mode unchanged.

**Disposition: Comparison.** Use if the caster carrier cannot give TCRT a stable 2–8 mm standoff. Not the lead.

### 4.3 `S03` — VL53L0X downward as cliff

**`D`:** ST VL53L0X, [datasheet](https://www.st.com/resource/en/datasheet/vl53l0x.pdf). I2C. Absolute ranging; default timing budget ~30 ms; high-speed example **20 ms**; high-accuracy **200 ms**. Indoor typical to ~1.2 m; outdoor / dark / cover-glass dependent. ST's own tables split white/grey and indoor/outdoor.

**Reject reasons, together:**

1. **Bus.** I2C is allowed for telemetry, **never** as the sole stop-path cliff. A stuck bus, address clash, or 100 ms timeout is a motion-safety fault that is harder than a GPIO pin.
2. **Surface.** Dark/glossy/sun are documented ToF failure modes. Using ToF *as the cliff* on a glossy table is the CON-TBD-14 trial stacked on the worst sensor for it.
3. **Latency.** 20–50 ms sample already consumes the 50 ms invariant before C3 scan, wheel loop and driver (5+2+8 ms). Score with 50 ms; do not claim the 8 ms minimum period is the stop-path age.

**Disposition: Reject as sole stop-path cliff.** A downward VL53L0X may still log height as telemetry. It does not count as one of the three required look-down **channels**.

### 4.4 `S04` — GP2Y0A41SK0F analog IR (obstacle stop-path)

**`D`:** Sharp GP2Y0A41SK0F, [datasheet](https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a41sk_e.pdf). Analog voltage, triangulation (less colour-sensitive than TCRT). Range **4–30 cm**. Measuring cycle **16.5 ± 3.7 ms**. `Icc` **12 mA typ, 22 mA max**. Vcc 4.5–5.5 V. First output unstable up to 5.0 ms after a measurement begins.

**Stop-path:** **OK on ADC.** Direct analog into C3 (or a 5 V-tolerant path with a documented divider). No I2C. No expander. Age bound 25 ms `E` (one cycle + scan). Still score the invariant at 50 ms.

**Coverage from caster contact:**

| Band | Need | 300 mm max `D` | Result |
|---|---:|---|---|
| Follow 0.50 m/s | **179 mm** | 300 mm | **PASS if caster-mounted**. Axle-mounted needs 289 mm from axle = 179+110 — still inside 300 mm but **do not** credit axle mount as caster look-ahead; a body-axis ToF/IR on the axle does not see the caster-shadow cube |
| Design 0.70 m/s | **289 mm** | 300 mm | **TIGHT — P-gate HOLD** for the 0.70 design point. 11 mm of paper room is not a margin. Follow cap stays 0.50 |
| Calibration 0.06 m/s | ~40 mm (cliff job) | This part is the **obstacle** layer, not the look-down | Do not use GP2Y as a cliff |

**Blind-region:** GP2Y minimum 40 mm. Objects closer than 4 cm can read ambiguously (classic Sharp near-side lobe). Bumper covers the last centimetres. Caster-shadow 20 mm cube remains a bump / look-down problem, not this sensor's.

**India snapshot 2026-09-17.** Sharp analog IR / GP2Y0A41 class on Robu. Price band `E` ₹300–800. Exact suffix / genuine Sharp vs clone **`U`**. Reconfirm marking before any later buy.

**Disposition: Lead obstacle stop-path.** Caster-mounted. HOLD for 0.70. Not a freeze of Sharp vs a later analog-IR sibling in the same 4–30 cm class.

### 4.5 `S05` — VL53L1X forward ToF (telemetry)

**`D`:** ST VL53L1X, [datasheet](https://www.st.com/resource/en/datasheet/vl53l1x.pdf). Longer-range ToF than L0X (up to 400 cm / 50 Hz class on the ST page), I2C, programmable RoI. Typical timing budgets 20–50 ms class (exact budget is firmware). Range can exceed 289 mm on paper. Still I2C; still not a GPIO stop-path.

**Stop-path:** **No**, as sole obstacle inhibitor. Same three rejectors as `S03` (bus, surface, latency), slightly less damning on range.

**Use:** Redundant look-ahead, logging, Concept B's telemetry identity, optional extra on Concept A **if GPIO spare remains ≥ 2** (I2C does not spend GPIO beyond the shared bus, already budgeted or not in Part 4).

**Disposition: Conditional telemetry.** Not sole stop-path. Not a reason to omit `S04` on Concept A.

### 4.6 `S06` — Miniature lever / microswitch bumper

**Class `E`/`D`:** SPDT microswitch or a spanning lever that closes a GPIO to the safe (inhibit-asserting) level on any contact across the 205 mm stance. Direct GPIO. Last layer.

**Stop-path:** **OK.** Age bound 5 ms `E`. Mechanical travel and mounting height `U` until the rig. Must not be the *first* layer at follow speed (`physics.md` §7.4).

**Coverage:** Contact at the bumper, not 179 mm ahead. Owns the caster-shadow cube and the furniture-leg shoulder if the bar actually spans the stance through a pivot. A single centre button is not a spanning bumper.

**India snapshot 2026-09-17.** Microswitches are commodity. Price band `E` ₹20–100. Stock `U`. Lever geometry is printed, not a SKU.

**Disposition: Lead bump.** Last layer. Direct GPIO.

### 4.7 `S07` — ICM-42688-P 6-axis SPI + INT1 (IMU lead)

**`D`:** TDK InvenSense ICM-42688-P, [datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf). 6-axis. Host interface I3C / I2C / **SPI up to 24 MHz**. INT1 / INT2 programmable (data-ready). Gyro ±15.6…2000 dps; accel ±2…16 g. This **matches CA**: rigid base mount, SPI + interrupt preferred (MEM-20260812-02).

**Stop-path role:** Slip / lift / tip / odometry-failure **detection**, not a cliff and not an obstacle ranger. Data-ready INT keeps sample age ~10 ms `E` if the ISR actually reads. A polled I2C IMU at 20 Hz is a different article.

**India snapshot 2026-09-17.**

- [Robu 601N1-ICM42688](https://robu.in/product/601n1-icm42688-42688-acceleration-gyroscope-sensor/) — module with **onboard MCU**, **UART angle output**, also claims I2C/SPI. 3–5 V, ~8 mA, 21 × 21 mm.
- Zbotic / other India listings carry “ICM-42688” as a class. Exact stock `U`. Price band `E` ₹400–1 500.

**Interface screen (do not skip):** UART-MCU modules that emit a fused angle string are **not** the ICM-42688-P SPI part. They add a second processor, an unknown latency, and a parser in the path. **Reject UART-angle-output as the stop-path IMU.** SPI+INT on the **bare** (or transparently wired) ICM-42688-P is the lead. A 601N1 may be bench telemetry; it is not the CA IMU until someone proves the SPI pins are the silicon's SPI and INT1 is the silicon's INT1, with the MCU held in reset or absent.

**Disposition: Lead IMU** = SPI + INT1 to the silicon. Screen the **interface**, not the marketing name.

### 4.8 `S08` — MPU-6500 module (fallback)

**`D`:** InvenSense MPU-6500 silicon supports SPI and I2C. **Many India breakout boards are I2C-only** despite that (no CS/INT brought out, or INT tied to an onboard regulator LED).

**Disposition: Fallback only if SPI+INT is actually wired** on the purchased board, verified with a continuity/photograph receiving check. Otherwise reject for the base IMU. Do not “just use I2C” to save pins — I2C IMU is telemetry, not the CA preference, and must not be the only lift detector.

## 5. Combination vs concepts

| Need | Concept A (working lead) | Concept B (comparison) |
|---|---|---|
| Cliffs | `S01` × 3 (caster, skid, one lateral). Dark+glossy trial on all three headings | `S01` × 4+ ring. Same trial. GPIO spare at risk |
| Obstacle stop-path | **`S04` caster-mounted** | Bumper `S06` only — **G03 hole at 0.50**. `S05` telemetry does not close it |
| Bump | `S06` last layer | `S06` last **and** only obstacle stop-path |
| IMU | `S07` SPI+INT | Same |
| ToF | Optional `S05` if spare GPIO/bus exists | Identity of the comparison; still not stop-path |
| Expander | **Never** | **Never** |

A driver HAT with “ToF cliff” headers is not a candidate in either column.

## 6. `LG-10` note (still `U`)

`physics.md` §5.3 proposed idle 0.25–0.50 W, average 0.4–0.8 W, peak ≤ 1.0 W pulsed / **≤ 1.2 W continuous as a flag**. This screen does not invent a `W`. Three TCRT emitters at 20 mA pulsed + one GP2Y at 12 mA + ICM-42688 at < 1 mA + C3 is plausible inside the flag if emitters are pulsed; continuous ToF + IR + emitters is the 1.2 W flag. Meter on the bench. Unknown emitter-off leakage is not zero.

## 7. India snapshot (ranges `E`, stock `U`)

Dated **2026-09-17**. Robu / Zbotic as class.

| Row | Class signal | Price band `E` | Stock |
|---|---|---|---|
| TCRT5000 | Commodity IR reflectance | ₹10–50 | `U` |
| QRE1113 | Less common than TCRT | ₹20–150 | `U` |
| VL53L0X / L1X module | “GY-VL53” class | ₹200–700 | `U` |
| GP2Y0A41SK0F | Sharp analog IR class | ₹300–800 | `U` |
| Microswitch | Commodity | ₹20–100 | `U` |
| ICM-42688 module | Robu 601N1 class / Zbotic ICM-42688 class | ₹400–1 500 | `U` |
| MPU-6500 module | Commodity 6-axis | ₹150–500 | `U` |

Not a budget. Genuine Sharp / TDK vs silkscreen clones is `U` until receiving inspection.

## 8. Explicit no-buy / no-wire list

1. Any stop-path sensor **behind a GPIO expander** or I2C-only.
2. **VL53L0X as the sole cliff** (`S03` reject).
3. **VL53L1X as the sole obstacle inhibitor** (`S05` telemetry only).
4. **UART-angle ICM-42688 modules** (601N1 class) as the stop-path IMU.
5. **I2C-only MPU-6500 boards** as the CA IMU.
6. A **single forward cliff** pretending to cover reverse and pivot.
7. **Bump-only** as G03 at follow speed.
8. A motor-driver HAT whose included sensors would freeze ADR-07.
9. Age bounds treated as registered G05 numbers (they are `E`).
10. Purchase of a “complete cliff ring PCB” that hides channels behind a PCA9555.

Permissible later as **bench equipment** if the builder separately authorizes: three TCRT5000 (or carriers), one GP2Y0A41SK0F, two microswitches, one **SPI-wired** ICM-42688-P breakout (not UART-MCU), one VL53L1X for telemetry experiments. That authorization is not this document.

## 9. Completion state

**Screen complete. No freeze.**

Lead combination for Concept A's sensing slice: `S01` × 3 + `S04` + `S06` + `S07`, with dark+glossy as a mandatory cliff trial and `S04` HOLD at 0.70. Concept B remains the ring + ToF-telemetry comparison and is not waived. Part 4 owns the pin map, the age-bound registration, and the fusion rule “unknown = inhibit.”
