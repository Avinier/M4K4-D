# RP-02 Custom Power and Safety Board Specifications

| Field | Value |
|---|---|
| Status | **Working design direction, v0.17 as of 2026-09-25 (builder direction: custom PCBs). Not registered, no schematic, no purchase authorized. Every board has decisions, part numbers and datasheet-derived values; nothing is bench-proved.** Derived from `RP02-P2-REG-01…03`, `power-component-candidate-screen.md` and `power-implementation-basis.md`. It records working selections (§1) for what those documents left open, groups the registered functions into boards, and states what each board must do and prove; none of it is registered |
| Owner | Project builder |
| Authority | `power-architecture.md` (`PA-01…16`, `PB-*`), `power-implementation-basis.md`, `brownout-restart-contract.md` (`BR-*`), `compute-control-component-screen.md` (`CCD-*`) |
| Feeds | Schematic capture, RP-06 body/chassis CAD volumes, G01, G04, G06 |
| Evidence labels | `D` manufacturer-documented, `E` estimate/target, `U` unknown, `W` measured. A value without a label is arithmetic on the cited inputs |

Nothing here changes a registered rule. Where a board decision conflicts with `PA-*`, `PA-*` wins and this file is corrected.

## 1. Working decisions recorded with this spec (2026-09-24)

These are builder-directed working choices, in the same standing as the battery working selection in `power-architecture.md` §`PA-03`. They can be superseded without reopening `PA-01…16`.

| ID | Decision | Reason | Reopens if |
|---|---|---|---|
| `BD-01` | **Custom PCBs** for pack protection, power path, motor gate/head rail and branch converters. Breakout modules remain bench-only | Builder direction. Also the only route to the enable, power-good, latch and load-disconnect behavior the candidate screen requires (`PCD-CVT-06`, `PCD-PRO-*`, `PCD-EST-02` are all IC-level parts) | — |
| `BD-02` | **Drive stage is fed directly from `PB-MOTOR` at pack-native voltage; no drive converter.** One DRV8874 per motor, as already modelled (Pololu 4035 carriers stay purchased modules for V1). Gearmotor is a 6 V-class variant, recommended 34–35:1 in the 8500 rpm family (about 211 rpm loaded at 6.0 V for the 159 rpm needed on an 84 mm wheel, 1.33× margin; the 6000 rpm 35:1 fails loaded; SKU still to be pinned); C3 firmware clamps duty to about `V_rated / V_bat`, and the driver current limit is set in hardware | 2S is 6.0–8.4 V. Removes a converter and keeps regeneration returning to the pack through a bidirectional gate | RP-03 selects another motor voltage class or measured speed at the 6.0 V floor misses the 0.70 m/s target on the 84 mm wheel |
| `BD-03` | **Pack protection is a custom pack-end board (`PCB-01`), not a generic 2S module** | Every generic 2S 20 A listing examined (Robocraze, Calcutta Electronics, Robu) omits the overcharge threshold, protection IC, board thickness and NTC support; `PA-02` requires the pack's protection functions to be enumerated | The builder prefers a named commercial 2S PCM that publishes a datasheet meeting `PCB-01` §3 |
| `BD-04` | **Head rail is a 5.0 V wide-input synchronous buck-boost on `PB-MOTOR` (`PB-HEAD`) while the RP-01 family is the C01/M181 case; a plain buck is rejected.** `PCB-03` reserves a footprint-compatible alternative for a 7.4 V-class servo direct feed | `power-implementation-basis.md` §2.2: XC330-M288-T is 3.7–6.0 V, so 2S cannot feed it directly. The Murata OKL-T/6-W12 buck cannot regulate 5 V below about 6.3 V input (§5.4), which the 2S pack passes under load. RP-01 has **not** frozen a family. A 7.4 V STS3215 variant (C046: 5–8.4 V) would be direct-fed; a 12 V variant would force 3S and reopen the pack | RP-01 freezes a family: fill in only the applicable §5.4 branch |
| `BD-05` | **`LTC3119` (ADI, 18 V / 5 A buck-boost) on both `PB-HEAD` and `PB-COMPUTE`; `TPS55288` is the fallback** | Hardware-only enable and configuration, stated 5 A at Vin > 6 V and 3 A at 3.6 V, one family (§5.4.2). `TPS55288` cannot start without an I2C write and its natural master is across the moving joint | Bench shows thermal or current shortfall, or regeneration cannot be clamped |
| `BD-06` | **`PCB-01` protection: primary `S-8252AAC-M6T1U` (ABLIC, 4.300 V) + secondary overvoltage and balancing `BQ29200DRBR` (TI, 4.35 V) + two low-side N-FETs + a thermal cutoff. Revised 2026-09-25 from `S-8252AAO` + `bq29209` with an 8.30 V charger, which needed an I2C master the design does not have** | The only combination found that gives published thresholds, cell balancing and a secondary path on two series cells (§3.1–3.6), matched to the charger's default 8.4 V | Bench injection shows a threshold or timing failure, or the builder prefers a named commercial 2S protection module |
| `BD-07` | **Motor gate: `LTC4368-1`, 3 mΩ Kelvin shunt, two Nexperia `PSMN1R0-30YLE` FETs (30 V, LFPAK56; about 3.8 mΩ typical hot for the pair), `RETRY` grounded (latch), permit chain drives the `UV` pin, `SHDN` driven by `SYSTEM_ARM` with a 0.8 ms re-arm pulse (§5.2.7); Bourns `CSS2H-2512K-3L00FE` shunt, `SMBJ10A` bus TVS, 22 Ω discharge** | Forward trip 13.3–20.0 A, above the 11.7 A historical peak and below the pack's typical trips (the windows overlap, §5.2.4); `SHDN` turn-off is too slow (about 90 µA into the gate) so the E-stop acts through `UV` (§5.2) | Measured `CC-PEAK-01` exceeds about 12 A, the FET safe-operating-area or turn-on into a short fails, or the latch does not clear on re-arm |
| `BD-08` | **`PCB-01` details: FETs two Nexperia `PSMN1R5-30YLC` (LFPAK56; alternate `EFC4C002NL`; `EFC3J018NUZ` rejected for its ±8 V operating gate limit) with a Vishay `WSK2512` 5 mΩ Kelvin shunt in the `VM`–`VSS` loop; `MMBT3906` gate-discharge assist on both gates; `CB_EN` from a `BZX84-C6V8` Zener and `MMBT3904`; over-temperature by a Bourns `AC72ABD` thermal cutoff in the cell strap plus a SEMITEC `103AT-2` NTC (no comparator)** | Discharge overcurrent window 17.7–25.3 A with the shunt (FETs alone would trip at 30–80 A); the comparator would add tens of µA of standby drain; every number is on a datasheet (§3.4–3.6) | The FET or shunt cannot be sourced in India, the trip window proves too wide on the bench, or the cell datasheet's temperature limit changes |
| `BD-09` | **`PCB-02` charger runs in `BQ25798` power-up default mode with no host: 8.4 V, 1 A, JEITA on a 103AT-2, hardware `CE`, `ILIM_HIZ`, `STAT`, `INT`; `SYS` gated by adapter-present; I2C to a bench header only** | The datasheet documents autonomous default-mode charging; a body-side I2C master would need a `PA-09` amendment, and C2 is across the yaw joint (§4.5) | Default-mode charging fails bench proof, the charge-voltage margin proves inadequate, or a supervisor is later wanted for telemetry |
| `BD-10` | **Watchdog: one TI `TPS3436CFDBEDDFRQ1` per C2 and C3 carrier (10 ms window, ratio 4, 20 ms feed, 10 s startup, 50 ms non-latched reset); READY is a hardware AND of `WDO`, `WD-EN` and `MCU_RDY`; C2's READY crosses the joint as a complementary pair** | Datasheet-verified window (feed window 11–36 ms) that suits the 5 ms and 2 ms control loops; latch would not enforce fresh arm (§7) | Measured loop jitter or boot time breaks the window, or the part is unobtainable (`CCCBGD` fallback) |
| `BD-11` | **`PCB-04` low-power branches: `TPS630701RNMR` converters (C2, base, display), each behind `TPS259474LRPWR` latch-off e-fuses at 2.0 A; `SYS` gated by a `TPS22810DBVR` load switch; C2 and base start independently and display/compute/audio enable from a one-shot latch set by `PG_C2`** | The `TPS259474L` is the only `TPS25947` variant that latches; 2.0 A avoids nuisance trips on the converter's 1 A start-up input limit and the 0.5–0.7 A input at the sag; a live "C2 first" dependency would violate `PA-11` (§6) | Bench shows breaker/ORing/start-up faults, or RP-05 or RP-03 changes the loads |
| `BD-12` | **`PCB-02` details: `PROG` 8.2 kΩ (2S, 750 kHz), 2.2 µH inductor (Isat ≥ 4 A), `ILIM_HIZ` 10 kΩ/6.8 kΩ (1.08–1.38 A), `TS` 5.23 kΩ/30.1 kΩ; `STUSB4500` PDOs 5/9/15 V at 1.5 A with `POWER_ONLY_ABOVE_5V`; `LTC2954-2` latch with a C2-rail `KILL` node and adapter-present hard block; `OPBUS`-derived pack sense with a hardware `ENERGY_OK`; adapter class ≥ 30 W offering 15 V ≥ 1.5 A** | Datasheet-derived (§4.1, §4.2, §4.5.1); the 512 ms `LTC2954` `KILL` blanking cannot be met by an ESP32-S3 C2 booting, and a button press in `CHARGE` would otherwise latch `OPERATE` on unplug | Bench shows default-mode charging, latch or adapter-compatibility faults |
| `BD-13` | **Head per-axis protection: servo Current Limit in Operating Mode 5 (yaw 0.9 A, pitch 0.8 A, roll 0.6 A, sum 2.3 A), Shutdown 0x35, voltage limits 3.7–6.0 V, Bus Watchdog 100 ms, latching `TPS259824ONRGE` trunk at about 7 A, `INA180A2` body-side monitors with a hardware `HEAD_OC`, clamp at 5.74 V with a 27 Ω / 2 W dump** | ROBOTIS e-manuals: the Current Limit default (2,352 mA) is above stall and applies only in Current-based Position mode (§5.4.3) | Bench shows the limits do not hold a stalled servo, or RP-01 picks the STS3215 |
| `BD-14` | **`LTC3119` rail design: `RT` 162 kΩ (494 kHz), Coilcraft `XAL5030-332ME` 3.3 µH, forced PWM, `RZ` 95.3 kΩ / `CP1` 240 pF, latching `TPS259824ONRGE` (7 A) ahead of each rail, head clamp TL431 + PNP at 5.74 V with a 27 Ω / 2 W dump; compute setpoint 5.15 V recommended** | Datasheet-derived (§5.4.2); the `TPS259824` 16.9 V variant avoids a trip in normal charging; 5.10 V fails the Pi's 200 mV transient allowance in the worst corner | Bench shows thermal or current shortfall, or the setpoint change is refused at registration |

## 1.1 Builder acceptances (2026-09-25)

The builder accepted the recommendations listed in the reviews of 2026-09-25 ("yes i accept everything"). They are recorded here as **working decisions**. Two touch registered baselines (`PB-COMPUTE` 5.1 V in `power-implementation-basis.md`, the `PA-14` `OFF` wording); changing those needs an explicit supersession record (`RP02-P2-REG-*`) that has **not** been written, so the registered text is unchanged.

| ID | Accepted | Consequence and what is still open |
|---|---|---|
| `BA-01` | Pi supply setpoint **5.15 V** (619 k / 113 k) instead of 5.10 V | Passes both the 100 mV steady and 200 mV transient allowances (§5.4.2). Registered 5.1 V stays until superseded |
| `BA-02` | `OFF` draw of about 43 µA typical, up to about 100 µA, with the charger, latch and gate controller on the pack | The `PA-14` wording ("`OFF` has only the pack protection path") still needs confirming at registration; no battery-disconnect switch is built |
| `BA-03` | Servo family stays XC330 at 5 V (M181 yaw, M288 pitch and roll); STS3215 is not pursued unless RP-01 reopens | Removes the 8.4 V-versus-charger conflict from the working design; RP-01 still owns the freeze |
| `BA-04` | Drive-motor target: 34–35:1, 8500 rpm class, 6 V (about 211 rpm loaded at 6.0 V for the 159 rpm needed on an 84 mm wheel) | The exact SKU (stall current 0.9 A vs 2.6 A, shaft length) is still to be pinned before purchase |
| `BA-05` | Camera cable: the PCN-36 revision of the 15-to-22-pin cable (11.5 mm wide) | Bend life in the clock spring is undocumented |
| `BA-06` | **Centre-of-mass baseline revised** from +25 / 124 mm to the layout-02 result, x +18.77 / h 105.05 mm, with no added ballast | Tip acceleration `g·x/h` falls from about 1.91 to 1.75 m/s². The CAD check `com_forward_of_physics_margin_line` is re-based from "x ≥ +20 mm" to the a_tip 1.582 m/s² that line encodes at h = 124 mm (`RP03-CAD-09`); it passes, 108/108 checks pass, and the worst head pose is about 1.44 m/s² against the authored `a_peak` 1.00 (`E`) |
| `BA-07` | `PCB-03` and `PCB-04` stay at their layout-02 positions; the hold-up capacitors are chosen for height (the bay has zero slack) | If the 3.3 mF per node does not fit, the 1.68 mF minimum (37.5 ms) is the fallback and the hold-up time must be re-verified. The harness placeholders that pass through the boards must be re-planned |
| `BA-08` | The pack interface (SBS Mini pair and ATOF holder) needs a serviceable place that keeps the main fuse source-adjacent | Recommended: the front edge of the `PCB-03` region above the tub. The SBS Mini pair (13 mm wide) does not fit the 11.3 mm channel under the deck; not yet modelled |
| `BA-09` | The brownout proposals in §8.1 are the working numbers | Still resting on estimated pack resistance and a generic voltage curve; registration and measurement remain |

## 2. Board set

| ID | Board | Owns (`PB-*` / function) | Sits where (proposal, `E`) | Size (`E`, from the part inventory; not layouts) |
|---|---|---|---|---|
| `PCB-01` | Pack protection board | Pack-integral protection, balancing, pack temperature; `PA-02` first layer | On the pack, in the chassis tub | 48 × 20 mm, **2.9 mm total thickness** (parts 1.3 mm), under the 4.5 mm limit |
| `PCB-02` | Charge and system-power board | `PB-CHARGE-IN`, `PB-CHARGE-LOGIC`, `PA-14` latch, source selection, pack sensing | **Vertical on the rear-panel frame**, X −50…−36, Z 58…94, USB-C inlet at its lower edge | **50 × 36 mm** without the pack interface (60 × 40 with it), parts to 11.6 mm |
| — | Pack interface tile (SBS Mini + ATOF holder) | Main fuse and pack connector | **Beside the battery tub**, X 26…56, Y 34…60, Z 58…72, or on the front edge of `PCB-03` | about 30 × 26 × 14 mm; keeps the main fuse source-adjacent (`PA-02`) |
| `PCB-03` | Motor gate and head/drive distribution board | `PB-MOTOR`, `PB-HEAD`, `PB-DRIVE` distribution | Above the tub, X 24…68, Y ±28, Z 60…74 | **56 × 44 mm**, parts to about 12 mm |
| `PCB-04` | Branch converter board | `PB-SAFE-C2`, `PB-SAFE-BASE`, `PB-COMPUTE`, `PB-DISPLAY`, `PB-AUDIO-OUT` | Centre under the compute tray, X −30…40, Y ±22, Z 60…77 | **70 × 44 mm**, parts to about 14 mm (the 3.3 mF hold-up capacitors set the height; the sizing assumed 1 mF, so recheck) |
| — | Safety-carrier watchdog block | External window watchdog and hardware `READY` | On each C2 and C3 carrier | Within the carrier |
| — | E-stop (IDEC `XA1E-BV3U02KT-R`, Ø16 unibody, 2NC; was XW1E-BV402M-R until 2026-09-25) | Hardware E-stop operator | Rear panel, on the floor of an 8 mm octagonal well: Ø16.2 mm cut-out, keep-out X −50.4…−26.5, Y ±11, Z 94.5…116.5 (23.9 mm behind the floor) | Mushroom Ø29 mm, 12.6 mm proud of the panel, 14 g (`D`, XA datasheet) |

Total board footprint is about 7300 mm² against 2900 mm² reserved by the placeholder envelopes (2.5–2.8×). Positions are a proposal that has not been through an interference sweep. The CAD replaces the `CONTROL_POWER_SENSORS` mass row (121.5 g): the new rows total about 111 g plus 40 g for the E-stop, and the register CoM moves from x +20.6 to about +19.1 mm (target +25). Two boards may merge if CAD shows a single carrier fits better; the **functions and separations** in §3–§7 may not.

Inter-board connectors are Micro-Fit+ for power and Micro-Fit 3.0 for low-current signals (`PCD-CON-03/02`, leads, exact terminals open). **The pack connector is Anderson SBS Mini (`PCD-CON-01`): housing `B02265G1` (red) on both halves, silver-plated open-barrel contacts `261G3-LPBK` on AWG14 fine-strand silicone leads of 150 mm (about 2.9 mΩ hot for the loop), 0.75 mΩ per mated contact, 41 A (12 AWG) / 31 A (14 AWG) UL rating, UL hot-plug 45 A at 72 V DC; crimp tool part number to be confirmed.** The charge inlet is USB-C (`PCD-CON-05`). Pack and charge connectors must be physically non-mateable. The main fuse is a Littelfuse **ATOF 15 A** (`0287015.L`, 32 V, 340 A²s, 12 A at 65 °C, 4.8 mΩ cold) in an ATO FLR PCB holder (`178.6165.0001`, 22.5 A continuous) on `PCB-02`.

## 3. `PCB-01` — Pack protection board

**Purpose.** Bound cell and pack abuse for the 2S1P Samsung INR18650-25R pack. It travels with the cells, so it protects them when the pack is out of the robot. It is the first layer of `PA-02`; it is not the main fuse and not branch protection.

**Cell facts (`D`, from `power-component-candidate-screen.md` §9.2).** Charge 4.20 ± 0.05 V (standard 1.25 A, maximum 4 A), cut-off 2.5 V, 20 A continuous discharge, DC impedance typically 22 mΩ (30 mΩ maximum) per cell (`D`, Samsung SDI, §3.7).

| Requirement | Target | Basis |
|---|---|---|
| Overcharge protection | Primary trip 4.300 V nominal (4.275–4.325 V), secondary 4.35 V (4.326–4.374 V), per cell; charger left at its 8.4 V default (§3.3, §4.5) | Revised 2026-09-25: the lowest standard trip that clears the default-mode charger and the balance band is 4.300 V. Worst cell in normal charging reaches 4.25 V, inside the cell's limit; the trips sit 25–125 mV above it and act only when the charger and balancer have failed |
| Over-discharge protection | Per-cell trip 2.400 V nominal (2.35–2.45 V), 128 ms delay, release 3.000 V; the system's own `EN-03` critical threshold must act above it | The system must stop first (`BR-08/10`); the BMS is the last resort, not the low-battery policy. The trip sits 50–150 mV below the cell's 2.5 V cut-off; accepted for the same reason |
| Overcurrent / short-circuit | Two thresholds with documented delays (§3.4): discharge overcurrent 0.200 V across a 5 mΩ shunt plus the FETs (17.7–25.3 A window) for 8 ms, load short 0.500 V for 280 µs; above the credible peak (historical 11.7 A `E`, 59% of one cell's 20 A) and below what the cells and traces can take | Ledger §5.3 |
| Charge overcurrent | Far backstop only (16.8–26.5 A, §3.4); normal charge is limited by the `BQ25798` (1 A default) and regeneration by the gate's reverse trip and the drive stage | The cells' maximum charge current is 4 A (§3.7); the gate's reverse trip and this trip are both far above it |
| Balancing | Per-cell, automatic, enabled only in the upper part of the charge range; about 10 mA, starting at 17–45 mV mismatch (§3.5) | Cell mismatch on a 2S pack |
| Temperature | 103AT-2 NTC on the cell surface to a pack-connector pin for the charger, plus a Bourns `AC72ABD` thermal cutoff in the cell strap (§3.6) | `BQ25798` thermistor input needs it; neither protector IC has a temperature input |
| Series path | Back-to-back N-FETs in the **low side** (the S-8252 is a low-side protector); ground shift analyzed in §3.4 | `PA-15`: about 0.16 V at 11.7 A and about 0.28 V at 20 A (14 mΩ typical hot) between cell negative and the star |
| On-resistance | Total added series resistance ≤ 14 mΩ hot (shunt 5, FETs up to 5.7 hot, thermal cutoff up to 2 = 12.7 mΩ) | Inside the ledger's 30 mΩ BMS allowance (`2·22 + 30 + 10 = 84 mΩ` pack model); each extra mΩ costs 11.7 mV at peak |
| Self-consumption | Documented quiescent current from the cells | Sets shelf discharge; feeds the `OFF` budget |
| Fault latching | After a short-circuit trip, restoration behavior documented (auto-release vs needs charger) | `PA-02`: retry behavior must be enumerated |
| Pack connector | SBS Mini pack-side housing, keyed; sense/NTC wiring on a separate small connector or contacts | `PCD-CON-01` |
| Physical | Cell tabs / strips spot-welded per the battery procedure in `workbench.md`; board retained mechanically, not only by leads | Vibration |
| Height | ≤ 4.5 mm over the pack, including FETs and connector shroud | CAD tub clearance |

### 3.1 IC selection — decided 2026-09-24, revised 2026-09-25 (`BD-06`)

Datasheets read: ABLIC S-8252 Series (Rev.4.0_00), TI bq29209/bq29200 (SLUSA52C), TI BQ25798 (for the charge stack). Nothing here is bench-proved.

**Decision `BD-06` (revised 2026-09-25): primary protection `S-8252AAC-M6T1U` (ABLIC, 2-cell, SOT-23-6, 4.300 V overcharge) plus secondary overvoltage and balancing `BQ29200DRBR` (TI, 3 × 3 mm VSON-8, 4.35 V), two low-side N-FETs, and a thermal cutoff.** The first selection (`S-8252AAO`, 4.250 V, with the 4.30 V `bq29209` and an 8.30 V charger) is withdrawn: it assumed an I2C-trimmed charge voltage that the design cannot supply (§4.5). No single 2S IC found covers protection, balancing and temperature, so the function is split across two ICs and a thermal cutoff.

| Candidate | What it does | Verdict |
|---|---|---|
| **ABLIC S-8252 family** (`D`) | 2-serial-cell primary protector: overcharge, overdischarge, discharge overcurrent, load short, optional charge overcurrent; thresholds fixed by suffix; high-accuracy detection (±25 mV over −10 to +60 °C on overcharge); delays set internally; 8 µA operating, 0.1 µA power-down; VM and CO pins rated 28 V; SOT-23-6 or SNT-6A | **Selected as the primary.** No balancing and no temperature input |
| **TI bq29209 / bq29200** (`D`) | Secondary overvoltage only (4.30 V / 4.35 V) with automatic cell balancing (internal up to 15 mA, `CB_EN` pin), ±10 mV at 25 °C, 3 µA, VSON 3 × 3 mm | **Selected as the secondary and balancer** (`bq29200`, 4.35 V; the 4.30 V `bq29209` would overlap the primary's window). It cannot be the only protection: it has no undervoltage or overcurrent function, and 4.35 V is above the cell's 4.25 V |
| Other S-8252 suffixes | Same silicon, other thresholds (below) | AAC chosen; the alternatives are listed in §3.2 |
| TI BQ77915 / BQ7791502 | 3-series and up | Rejected: not 2S |
| ABLIC S-8232, S-8242B, S-82A2 | Other ABLIC families that surfaced in the search | Not evaluated |
| Gauge-plus-protector ICs (Maxim MAX173xx class) | Integrated protector, gauge, balancing, temperature | Not evaluated; NVM configuration and I2C add a firmware and configuration-integrity dependency to a board whose purpose is to work without firmware |
| Generic 2S protection modules | Unpublished thresholds | Rejected (`BD-03`) |

### 3.2 S-8252 suffix choice (revised 2026-09-25)

Criteria: overcharge 4.300 V (the lowest that clears the default-mode charger, §3.3), overdischarge near 2.5 V, 0 V battery charge inhibited, charge overcurrent function available, power-down available, the standard 1.0 s / 128 ms / 8 ms / 280 µs / 8 ms delay set. The relevant standard SOT-23-6 suffixes (`D`, Table 2):

| Suffix | Overcharge det / rel | Overdischarge det / rel | Discharge OC | Short | Charge OC | 0 V charge | Delay set | Result |
|---|---|---|---|---|---|---|---|---|
| **AAC** | **4.300 / 4.100 V** | **2.400 / 3.000 V** | **0.200 V** | 0.500 V | −0.200 V | **Inhibited** | (1) | **Selected** |
| AAO | 4.250 / 4.100 V | 2.500 / 3.000 V | 0.200 V | 0.500 V | −0.100 V | Inhibited | (1) | First choice, withdrawn: its lowest trip (4.225 V) sits below the worst cell at the default charge voltage |
| AAZ, ACF | 4.225 / 4.075 V | 2.400 / 2.900 V | 0.150 / 0.190 V | 0.500 V | −0.150 / −0.100 V | Inhibited | (1) / (5) | Same overcharge problem |
| AAQ | 4.300 / 4.100 V | 2.600 / 3.000 V | 0.400 V | 0.500 V | −0.400 V | Inhibited | (1) | Overdischarge 2.6 V fits better, but 0.400 V discharge overcurrent needs about 17 mΩ of shunt plus FETs and the extra dissipation |
| AAG, ACA | 4.300 / 4.150 V | 2.800 V | 0.150 V | 0.500 V | −0.150 V | **Enabled** | (1) / (5) | 0 V charge enabled and 2.8 V overdischarge |
| AAY | 4.250 / 4.050 V | 3.000 / 3.200 V | 0.150 V | 0.500 V | −0.050 V | Inhibited | (2) | Overdischarge at 3.0 V would trip inside the ledger's near-empty sag (2.7–2.85 V per cell at 11.7 A) |
| ACY | 4.250 / 4.050 V | 2.000 / 2.500 V | 0.200 V | 0.500 V | −0.100 V | Inhibited | (7) | Overdischarge 2.0 V is below the cell's 2.5 V cut-off |

The AAC's overdischarge trip is 2.400 V (2.35–2.45 V), 50–150 mV below the cell's 2.5 V cut-off. It is a last resort behind the system's own low-battery policy, so it is accepted. The datasheet says other suffixes need ABLIC's sales representatives, so a custom variant is not assumed.

### 3.3 Overvoltage threshold stack (revised 2026-09-25)

The charger runs in its power-up default mode with no host (§4.5), so `VREG` is 8.4 V.

| Level | Value | Basis |
|---|---|---|
| Cell charge limit | 4.20 ± 0.05 V (maximum 4.25 V) | Samsung 25R (`D`) |
| Charger regulation, `BQ25798` default 8.4 V | −0.25% to +0.65% over −40 to 85 °C, so 8.379–8.455 V, or 4.190–4.227 V per cell on average | `BQ25798` datasheet, `VREG_ACC` for `VREG` 8.4 V (`D`). |
| Balancer band | Mismatch starts at 17–45 mV (30 mV typical), so a cell can sit up to 22.5 mV above the pair mean before it acts | `bq29200` (`D`) |
| Worst cell at the end of charge | 4.227 + 0.0225 ≈ 4.250 V, the cell's own limit | Arithmetic |
| Primary overcharge trip, `S-8252AAC` | 4.300 V ± 20 mV at 25 °C, ± 25 mV from −10 to +60 °C, so 4.275–4.325 V; delay 1.0 s ± 20%; release 4.100 V | `D` |
| Margin between the worst cell and the lowest primary trip | 25 mV | Arithmetic |
| Secondary overvoltage, `bq29200` | 4.35 V ± 10 mV at 25 °C, ± 0.4 mV/°C drift from 0 to 60 °C, hysteresis 0.3 V, delay about 9 s per µF of `CCD` (0.1 µF gives about 0.9 s) | `D`; the 4.326–4.374 V window is my arithmetic. Its lower edge (4.326 V) is 1 mV above the primary's upper edge (4.325 V) |

**Why 4.300 V and not 4.250 V.** With the charger at its default the worst cell can reach the cell's 4.25 V limit in normal charging, so a primary whose lowest trip is 4.225 V (the 4.250 V `S-8252AAO`) could nuisance-trip at the top of charge. The 4.300 V variant clears it by 25 mV. The cost is that, in a charger or balancer fault, a cell can be held up to 25–75 mV above its stated limit before the primary acts, and up to about 125 mV before the secondary; this is the usual protector practice for 4.2 V cells, but it is less conservative than the first choice (`S-8252AAO`).

### 3.4 Current protection, shunt and FETs — revised 2026-09-25 (`BD-08`)

The S-8252 senses current as the voltage from `VM` to `VSS`, which is the FET pair's on-resistance plus any resistor in that path. The FETs alone would trip at 30–80 A, so a 5 mΩ Kelvin shunt is added inside the sense loop.

**Parts (`BD-08`).**
- **FETs: two Nexperia `PSMN1R5-30YLC` (LFPAK56)**, 30 V, `RDSon` at 4.5 V typical 1.65 mΩ, maximum 2.05 mΩ (3.4 mΩ at 150 °C), VGS(th) 1.05–1.95 V, VGS ±20 V, Ciss 4044 pF, Qg 30 nC (4.5 V) (`D`). Drains joined on one copper island; hand-solderable. Alternate: onsemi `EFC4C002NL` (WLCSP8 6.0 × 2.5 mm, 1.25 mm bump pitch, ENIG required at JLCPCB, not hand-solderable).
- **`EFC3J018NUZ` is rejected:** its maximum operating gate-source voltage is ±8 V, below the 8.4–8.6 V gate drive of a full pack.
- **Shunt: Vishay `WSK2512` 0.005 Ω ±1%, 4-terminal**, 1.0 W at 70 °C, TCR ±35 ppm/°C. 0.68 W at 11.7 A; 2 W for the 8 ms at 20 A is inside its 5× overload rating.
- **External circuit (`D`, S-8252 datasheet Table 11):** R1 = R2 = 470 Ω, C1 = C2 = 0.1 µF, R3 (`VM`) = 2 kΩ; no gate resistors in the datasheet. Provide a `VM`–`VSS` test pad pair for the first-connection case.

| Item | Value (`E`, arithmetic on datasheet values) |
|---|---|
| Sense-path resistance | Shunt 5.0 mΩ + pair 3.30 (25 °C typical, the datasheet gives no minimum) to 4.10 (25 °C max) to 5.74 (about 100 °C max) to 6.80 (150 °C max): 8.3 / 9.1 / 10.7 / 11.8 mΩ |
| Discharge overcurrent trip, 0.200 ± 0.010 V, 8 ms | **17.7–25.3 A** (0.19 V ÷ 10.74 mΩ to 0.21 V ÷ 8.30 mΩ); typical 24.1 A at 25 °C; 16.1 A at Tj 150 °C |
| Load short trip, 0.500 ± 0.100 V, 280 µs | 37–72 A; typical 60 A at 25 °C |
| Charge overcurrent trip, −0.200 ± 0.020 V, 8 ms | 16.8–26.5 A; typical 24.1 A. Far above the cells' 4 A maximum charge, so it does not protect against regeneration (§5.2.4 and §5.3 requirement on the drive stage) |
| Available pack short current | 147 A at 25 °C (57 mΩ at the pack terminals); about 70 A for a cold, aged pack with hot FETs. The 280 µs short detection acts above 37–72 A depending on the corner; between about 18 and 72 A the 8 ms overcurrent detection acts |
| Let-through | 147 A × 280 µs ≈ 6 A²s; 60 A × 8 ms ≈ 29 A²s; both far below the ATOF 15 A's 340 A²s |
| Ground shift (`PA-15`) | About 0.16 V between the cell negative and the star at 11.7 A (strap + thermal cutoff + `PCB-01` 14 mΩ typical hot) |
| Dissipation | Shunt 0.68 W at 11.7 A; FET pair about 0.63 W, about 0.3 W each |
| Series resistance budget | Shunt 5 + FETs up to 5.7 hot + thermal cutoff up to 2 = about 13 mΩ worst, inside the ledger's 30 mΩ BMS allowance |
| Layer order | The `LTC4368-1` gate (13.3–20.0 A, about 8 µs) acts first above its threshold. The pack's 17.7–25.3 A window overlaps the gate's, so a sustained 18–19 A in the low-gate/low-pack corner opens the pack after 8 ms in place of the gate. Same result: motor power removed |

**Gate discharge assist.** The S-8252 output pull-down is 5–20 kΩ (`D`). With Ciss 4044 pF that alone gives τ ≈ 81 µs (about 240 µs for 3τ), which consumes the 280 µs short-circuit budget. Add a `MMBT3906` PNP on each gate (emitter on the gate, collector on that FET's source, base through about 1 kΩ to the IC output; hFE ≥ 60–100 at 10–50 mA, `D`). Base current `(Vgs − 0.7) / (1 kΩ + 20 kΩ)` ≈ 0.2 mA at 5 V gives about 20 mA of discharge current, so about 1.5 µs for 30 nC (about 0.8 µs at 8.4 V). Turn-on stays on the IC's own drive.

### 3.5 Balancing (`bq29200`)

- Automatic, voltage-based. It starts at 17–45 mV mismatch and stops at 0 mV, loading the higher cell. Internal balancing handles up to 15 mA; a 10 mA setting uses `RCB = 100 Ω`, `RCB1 = 260 Ω`, `RCB2 = 160 Ω`, `RVD = 100 Ω` (the datasheet's example configuration).
- Recommended for cell voltages 3–4.2 V and `VDD` 6.0–8.4 V, calibrated at 7.6 V. **Pull `CB_EN` high (disabled) below the top of charge** to avoid discharging the cells at low state of charge; enable it from about 7.0–7.8 V pack with the Zener circuit below.
- Populate the delay capacitor `CCD` before connecting the cells, and connect the cells in the order ground, `VC1`, `VC2` (`D`).
- **Secondary action.** The `bq29200` `OUT` pin goes high on overvoltage. It drives an NPN or N-FET from the charge-FET gate (`CO` net) to its source, so it forces the charge FET off independently of the S-8252 (the assist PNP in §3.4 is not in that path). A chemical fuse is the alternative but is irreversible; not chosen.
- **`CB_EN` circuit (`BD-08`).** `CB_EN` is active low (below 1 V enables, above 2.2 V disables, absolute maximum 16 V, `D`). Pull it to `VDD` through 100 kΩ (disabled by default). An `MMBT3904` NPN (hFE ≥ 100 at 10 mA, `D`) pulls it low when a **`BZX84-C6V8`** Zener (VZ 6.4–7.2 V at 5 mA, IR ≤ 2 µA at 4 V, `D`) from `PACK+` conducts through a 220 kΩ base resistor. Balancing engages from about 7.0–7.8 V pack (Zener VZ plus 0.6 V), inside the datasheet's 6.0–8.4 V window. Standby cost is up to about `(8.4 − 6.4 − 0.6) / 220 kΩ ≈ 6.4 µA` at a full pack plus Zener leakage between 4 V and 6.4 V, for which the datasheet gives only a typical graph (**U**; bench-measure at 6.0, 6.4 and 7.0 V). The NPN needs to sink only about 84 µA (100 kΩ at 8.4 V).

### 3.6 Over-temperature cut-out — revised 2026-09-25 (`BD-08`)

**Decision: a Bourns `AC72ABD` resettable thermal cutoff in the cell-negative strap, bonded to a cell, plus the SEMITEC `103AT-2` (10 kΩ ± 1%, B = 3435 K) NTC to the pack connector for the charger. No comparator.**
- **Why 72 °C and not 77 °C.** The Samsung 25R specification (`D`) gives discharge −20 to 75 °C *surface* in one revision and −20 to 60 °C *ambient* in a later one, and charge 0–50 °C surface or 0–45 °C ambient. `AC72ABD` trips at 72 ± 5 °C (67–77 °C); `AC77ABD` (72–82 °C) could stay closed to 82 °C, above the 75 °C figure.
- **Why not a comparator.** A ratiometric NTC divider on the pack draws about 40 µA with a 100 kΩ NTC at 8.4 V, against the roughly 7–16 µA the two protection ICs already take.
- **`AC72ABD` facts (`D`, Bourns datasheet).** Trip 72 ± 5 °C; reset ≥ 40 °C; contact rating 9 V DC / 35 A (6000 cycles); 28 V DC / 35 A (100 cycles); **maximum breaking current 5 V DC / 80 A** (100 cycles; an older mirror says 60 A); minimum holding voltage 3.5 V; **leakage up to 200 mA when tripped**; resistance ≤ 2 mΩ (1 mΩ typical); −30 to 100 °C. Availability: DigiKey `AC77ABD-ND` shows 2670 in stock at US$1.92 (the 72 °C variant was seen only at a broker); India: DigiKey India ships, but no `.in` product page was seen.
- **Placement.** In the cell-negative strap, outside the `VM`–`VSS` sense loop, so it does not shift the overcurrent trips. Bond to a cell with thermal adhesive, not to the board.
- **Limits to accept.** The 9 V contact rating leaves 0.4–0.6 V over a full pack; the part cannot be reused on 3S. Shorts above the 80 A breaking rating (the pack can reach about 147 A) are cleared by the S-8252 at 280 µs and by the ATOF fuse before the thermal cutoff is asked to break them.

### 3.7 Integration and open checks

- **Overdischarge recovery (`BQ25798`, `D`).** The `BQ25798` datasheet describes this case: with the pack protector open it regulates the battery pin to about 2.5 V per cell for 1.5 s with up to 100 mA "as it tries to close the battery pack protector FET", then moves to pre-charge (default 120 mA, from `VBAT_SHORTZ` 2.25 V) and fast charge above `VBAT_LOWV` (15 / 63 / 68 / 72.5% of `VREG`, for example 5.29 V at 63% of the 8.4 V default). Charge current reaches the cells through the discharge FET body diode. The S-8252AAC releases at 3.000 ± 0.1 V per cell (about 6.0 V pack), above the pre-charge threshold. **Bench-test the recovery from a tripped pack.** `VBAT_LOWV` and pre-charge current stay at their defaults (§4.5).
- **Cell-connection filters.** `RIN` 100 Ω–1 kΩ with `CIN` 0.01–0.1 µF on each `bq29200` sense input (`D`), and equivalent filtering on the S-8252 `VC`.
- **0 V charge inhibit:** the S-8252AAC inhibits charging below about 0.4–1.1 V per cell; a deeply discharged pack needs to be recharged by other means.
- **Sourcing (`E`, not authorized).** `S-8252AAC` and `bq29200` are aggregator-only so far. Confirmed this session: `PSMN1R5-30YLC` at DigiKey and Mouser (stock and price snapshots, dates unclear), `EFC4C002NL` at JLCPCB (9 in stock) and DigiKey (reel only), `WSK2512` from Vishay (reseller stock not checked), `MMBT3904/3906` and `BZX84-C6V8` from Nexperia, `AC77ABD` at DigiKey and Mouser. **No India distributor listing was confirmed for any of them**; check DigiKey India and Mouser India before committing.
- **Cell data (`D`, Samsung SDI).** Maximum charge 4 A; DC impedance typical 22 mΩ (30 mΩ max); discharge 20 A continuous; standard charge 1.25 A and cut-off 2.5 V confirmed.

**Design-integrity rules.**
- Every protection function is verified by injection on the bench before a pack is built: overcharge, over-discharge, both overcurrent levels, short, over-temperature and cell imbalance.
- Do not put pack-integral protection on `PCB-02`: it must stay with the cells.
- Solo-builder risk: an in-house Li-ion pack needs the written battery procedure and equipment `workbench.md` requires. If that is not in place, a pack builder or a commercial protection module is the fallback.

## 4. `PCB-02` — Charge and system-power board

**Purpose.** Implement `PA-09` (restricted charge source) and `PA-14` (true `OFF/OPERATE/CHARGE`), and provide the pack observation that reaches C2 independently of the SBC (`PA-10`).

### 4.1 Function blocks

| Block | Content | Rule it implements |
|---|---|---|
| Charge inlet | USB-C receptacle; `ESDA25P35`-class 25 V TVS on VBUS (ST reference design, `D`; part datasheet not read, `U`); `STUSB4500QTR` PD sink with **dead-battery mode** (CC1DB/CC2DB tied to CC1/CC2); supplied **from VBUS only** (VDD pin), so it draws nothing when unplugged | `PA-09.1–2`, `PCD-CHG-01` |
| Input switch | P-channel FET (ST reference part `STL6P3LLH6`, `D` as the part in ST's minimal schematic, ratings `U`) driven by `VBUS_EN_SNK` (high-voltage open drain) with 100 kΩ gate pull-up and 100 nF gate capacitor (ST Figure 9, `D`); `POWER_ONLY_ABOVE_5V = 1`, so it closes only after an explicit 9 V or 15 V contract | `PA-09.1` |
| Charger / power path | `BQ25798RQMR` in **power-up default mode** (§4.5); `VAC1 = VAC2 = VBUS`, `ACDRV1 = ACDRV2 = GND` (no ACFET or RBFET, `D` datasheet §7.3.5); `SDRV` to GND through 1 nF 50 V 0402 (ship FET not fitted, `D`); `QON` unconnected (`U`, confirm on the bench); `D+`/`D−` unconnected (`U`, confirm poor-source detection completes) | `PCD-CHG-02` |
| Charge-present detect | `VSNK` (the post-switch VBUS net) through 100 kΩ/100 kΩ to the gate of a 2N7002-class N-FET `Q_cp`. `Q_cp` pulls `CHG_PRES_N` low. Passive and independent of every logic rail | `PA-09.6`, `BR-05` `CHARGE_ABSENT` |
| System-power latch | `LTC2954ITS8-2` (or DDB-2) push-button on/off controller, `EN` (active low) driving the gate of the operating-source P-FET (§4.2) | `PA-14` |
| Operating-source switch | P-FET (30 V, ≤ 25 mΩ at −4.5 V, ≥ 6 A) source on `BATBUS`, drain on `OPBUS`; gate node with 1 MΩ pull-up to source and 100 kΩ to the `LTC2954` `EN`; 47 nF gate-source capacitor for soft start (τ ≈ 4.7 ms with the 100 kΩ, inrush ≈ 0.4 A into an assumed 500 µF, `E`) | `PA-14` |
| Adapter-present hard block | P-FET `Q_dis` (source `BATBUS`, drain on the operating-source gate node) turned on by `Q_cp2` through an RC (1 MΩ, 4.7 µF, about 3 s, `E`); forces the operating switch off regardless of `EN` when an adapter is valid | `PA-09.5`, `PA-14` |
| Charge-logic selector | `SYS` → gated P-FET `Q_sys` (source `SYS`, drain to a Schottky `D_sys`, enabled only when `VSNK` is valid) → **Schottky OR** with `OPBUS` (Schottky, 3 A / 40 V class, about 0.45 V drop, `E`) feeding only the C2 and display converter inputs. **No net from `PB-CHARGE-LOGIC` reaches `PCB-03`** | `PA-09.3–4` |
| Pack sensing | Divider from **`OPBUS`** (not `BATBUS`, so it costs nothing in `OFF`): 33 kΩ / 16.2 kΩ to the C2 ADC as `V_PACK_ANA` (8.6 V → 2.83 V), 100 nF at the C2 end; plus the `ENERGY_OK` comparator (§4.2) | `PA-10`, `BR-05` |
| Main fuse | Source-adjacent `ATOF` holder between the pack connector and `BATBUS` | `PCD-PRO-03` |

### 4.2 Modes and `OFF` budget

| Mode | Powered | Must be true |
|---|---|---|
| `OFF` | `PCB-01`, the `BQ25798` in battery-only mode, the `LTC2954` | No 5 V, no logic, no motor rail; `STUSB4500` draws nothing (VBUS-powered); `OPBUS` open; the `BATFET` feeds `SYS` but `Q_sys` is open so nothing is fed from it |
| `OPERATE` | `OPBUS` through the operating switch; motor path only through `PCB-03` | Boot begins motion-inhibited; the button is the only turn-on path |
| `CHARGE` | Adapter valid: `Q_sys` closes, `SYS` feeds the OR node, C2 and display converters only | `Q_dis` forces the operating switch off after about 3 s (motor gate is cut at once by `CHARGE_ABSENT`); `KILL` is forced low so a button press cannot latch `OPERATE` |

**`OFF` budget (`E`, from datasheet typical/maximum values):**

| Item | Typical | Maximum | Basis |
|---|---:|---:|---|
| `S-8252AAC` | 4 µA | 8 µA | `D` (`PCB-01`) |
| `bq29200` | 3 µA | 3 µA | `D` "ICC < 3 µA" |
| `CB_EN` Zener/NPN | 2 µA | 5 µA | `E` (`PCB-01` §3.5) |
| `BQ25798` battery-only, ADC off | 17 µA | 24 µA | `D` `IQ_BAT_ON` |
| `LTC2954` | 6 µA | 12 µA | `D` `IIN` |
| `STUSB4500`, gates, dividers | 0 | 0 | VBUS-powered / fed only when an adapter or `OPBUS` is present |
| `LTC4368-1` and its `UV`/`OV` divider (`PCB-03` §5.2.3) | 11 µA | 48 µA | `D`/`E` |
| **Total** | **43 µA** | **100 µA** | about 1.2% (typical) to 2.8% (maximum) of the 2.5 Ah pack per month |

This supersedes the earlier estimates; it does not meet the `PA-14` wording (`OFF` has only the pack protection path). Recommendation stands: accept the charger's, the latch's and the gate controller's draw as part of the pack and charge path, and confirm the `PA-14` wording at registration; a battery-disconnect switch is the fallback.

**Latch behavior (`D`, LTC2954 datasheet):** 2.7–26.4 V input, 6 µA typical; `EN` (−2 variant, active low, 33 V rating) drives the P-FET gate; turn-on when `PB` is held low for the ONT time; **512 ms blanking** after `EN` asserts during which `KILL` must be brought high or `EN` releases; `INT` (open drain) is the debounced power-down request; `KILL` (0.6 V threshold, 30 mV hysteresis) releases `EN` when forced low; holding `PB` for 64 ms plus the PDT time force-releases `EN` even if the MCU is dead.
- `ONT` capacitor 82 nF: `tONT ≈ 82 nF / 1.56×10⁻⁴ µF/ms + 1 ≈ 0.53 s`. `PDT` capacitor 0.82 µF: forced power-down about 5.2 s. `PB`: 5.1 kΩ series and 0.1 µF (datasheet's recommendation).
- **`KILL` node:** pull-up to the C2 branch 5 V (`+5V_C2`) through 100 kΩ, 1 MΩ to ground, C2 open-drain output pulls it low to shut down. **This removes the 512 ms blanking problem**: C2 (an ESP32-S3) cannot be relied on to boot and drive `KILL` high inside 512 ms, but the C2 converter starts as soon as `OPBUS` is up, and its rail raises `KILL`. If C2 hangs the button force-off still works; if the C2 rail dies, `KILL` falls and power is released.
- **`INT`:** open drain, pulled up on the C2 carrier to 3.3 V; C2 begins orderly shutdown then releases `KILL`.
- **Charge insertion:** `Q_kill` (gate from `VSNK` divider) forces `KILL` low whenever an adapter is valid, so a press cannot latch `EN`; `Q_dis` blocks the switch regardless.

**`ENERGY_OK` comparator (`E`, values are placeholders for the `EN-02/03` registration):**
- Supply from the C2 branch through a local 3.3 V LDO (no robot-wide 3.3 V rail); reference-in-package nano-power comparator class, open-drain output pulled to `+5V_C2` (so a dead logic supply reads inactive).
- **Falling threshold 5.7 V (5.53–5.87 V) on `OPBUS`, rising 6.4 V, 1.0 ms fall debounce and at least 100 ms rise dwell** (§8.1 proposal; divider and positive-feedback values to be recomputed for these thresholds). `OPBUS`-derived, so it costs nothing in `OFF` and includes the fuse and switch drop, which is the loaded voltage that matters.
- **Analog vs digital to C2:** `V_PACK_ANA` goes across the joint as a slow analog level (33 k/16.2 k divider, source impedance about 11 kΩ, 100 nF at C2) because `EN-02/03` are millisecond-class policies. `ENERGY_OK` is the hardware term for `MOTOR_PERMIT`. A digital multi-threshold sideband was rejected for adding comparators with no gain. Route with a signal-ground conductor.

### 4.3 Requirements

- **Back-power cases.** All `PA-16` cases are analyzed on this board: pack removed, pack installed with charge absent, charge inserted in `OFF`, charge inserted during operation, charge with pack absent (allowed only if the selected `BQ25798` configuration supports it), and partially mated pack connector.
- **Charge insertion during motion.** The default bench behavior is immediate motor-arm removal (`power-implementation-basis.md` §8.4) until the brake-first timing is registered.
- **Loss of charger status.** Corrupt or absent charger status cannot enable motors or restore a prior mode (`PA-09.7`, F-18).
- **Adapter.** External certified USB-C PD adapter only; AC mains never enters Makad. The preferred PDO (15 V vs 20 V) is open and follows the maximum charge power.
- **Layout.** `BQ25798` is a 4 mm QFN; place its power stage, capacitors and thermistor return first. Keep the charge loop away from the ADC and comparator traces.
- **Test points.** `BATBUS`, `OPBUS`, `CHGBUS`, `VBUS`, `HOLD`, latch state, charge-present, `ENERGY_OK`, and a shunt-referenced current point.

### 4.4 Evidence required

PDO/NVM audit; wrong or weak adapter behavior and adapter classes (9 V-only, 15 V, 20 V-only, 5 V-only); hot plug (VBUS ringing, TVS); pack absent or depleted; thermistor open and short; charge-current accuracy; `OM-06` exclusivity; source removal and return; thermal soak. For §4.5: one complete charge cycle from the defaults; `STAT` states including the fault blink; charger start with no host and with the bench header connected; the 40 s watchdog return to defaults; `SYS` gating (no `PB-CHARGE-LOGIC` voltage in `OFF` and `OPERATE`); adapter insertion and removal in `OFF`, `OPERATE` and `CHARGE`; a button press with an adapter attached; a hung C2 (button force-off); and `OFF` current at 3.7 V and 8.4 V.

### 4.5 Charger control without a host — decided 2026-09-25 (`BD-09`)

**Question.** The `BQ25798` is I2C-controlled, and the registered charge mode (`PA-09`) powers only C2 and the display. C2 is across the yaw joint from the charger, so there is no body-side I2C master. What does the charger need a host for?

**Finding (`D`, `BQ25798` datasheet Rev. C, June 2026).**
- **It does not need one.** The device is "a host controlled charger, but it can operate in default mode without host management", autonomously completing a charge cycle (§7.3.9.1, §7.4.1). After power-on reset it starts in default mode with the watchdog expired and all registers at their defaults.
- **Defaults for a 2S pack** (`PROG` pin resistor selects 2S): `VREG` 8.4 V, fast charge 1 A, pre-charge 120 mA, trickle 100 mA (fixed), termination 200 mA, recharge 200 mV below `VREG`, JEITA temperature profile, safety timers 1 h trickle / 2 h pre-charge / 12 h fast charge, `VSYSMIN` 7 V, ADC disabled. At the end of a timer, charging stops and the converter keeps supplying `SYS`.
- **A host is needed only to change those**, chiefly `VREG` (to trim it below 8.4 V) and `VBAT_LOWV`. Any I2C write moves the charger to host mode with a 40 s watchdog; if the host stops servicing it, the registers return to the defaults.
- **A thermistor is mandatory** in default mode: a missing thermistor is a `TS` fault and charging is disabled.

**Options.**

| Option | Result |
|---|---|
| I2C across the yaw joint from C2 | Rejected: a fast bus over the flex cable, C2 only just alive in charge, and the same joint problem as the `TPS55288` |
| A supervisor MCU on `PCB-02` in the charge domain | Rejected for V1: needs an amendment to `PA-09` (the restricted charge source may power only C2 and the display), adds firmware to the charge path, and buys only a trimmed charge voltage and telemetry |
| **Default mode, no host** | **Selected (`BD-09`)** |

**Decision `BD-09`: the charger runs in power-up default mode.** The consequences:
- **Charge voltage is 8.4 V** (8.379–8.455 V). The `PCB-01` protector was changed to match (§3.2–3.3, `BD-06` revised): primary `S-8252AAC` 4.300 V and secondary `bq29200` 4.35 V.
- **Hardware pins carry everything else:** `PROG` (2S resistor), `CE` (tie to a defined level, never floating), `ILIM_HIZ` (a divider setting the input current limit as `1 V + 0.8 Ω × IINDPM`, `D`; 10 kΩ / 6.8 kΩ, §4.5.1), `TS` (103AT-2), `STAT` and `INT`.
- **Status to C2:** `STAT` is open-drain (low charging, high complete or disabled, 1 Hz blink on a fault). Pull it up to C2's logic rail through 10 kΩ and read it as a static sideband line across the joint, with a `VBUS`-present line, for the charge display (`CC-15`). No fast bus crosses the joint.
- **I2C pins** go to a three-pin bench header with pull-ups fitted only there. Any bench write puts the charger in host mode for 40 s and then the defaults return.
- **No `PA-09` amendment.** C2 remains the only controller in `CHARGE`.
- **Lost by not having a host:** a trimmed charge voltage, charge-current derating and the charger's ADC telemetry. Pack voltage, current and temperature for C2 come from `PCB-02` analog sensing (§4.1).

**Findings from reading the datasheet that change other requirements:**
1. **`SYS` is live from the battery** in battery-only mode (the `BATFET` connects `SYS` to `BAT`). If `SYS` fed `PB-CHARGE-LOGIC` directly, C2 and the display converters would be powered from the pack in `OFF` and `OPERATE`. The gate on `SYS` in §4.1 (enabled only when `VBUS` is valid) is required.
2. **`VSYSMIN` is 7 V for 2S.** With an adapter present and the pack below 7 V, `SYS` is held at 7 V and the charge current is limited to 2 A (`D`). The `TPS630701` (2–16 V input) converters accept this.
3. **Battery-only quiescent draw.** With the ADC off (its reset state) the charger takes 17 µA typical and 24 µA maximum from the battery at 8 V (`D`, 540 µA if the ADC is on). Added to `PCB-01` (about 7–16 µA), the latch (about 1–2 µA) and the motor-gate controller with its `UV`/`OV` divider (about 11 µA typical, 48 µA maximum, `PCB-03` §5.2.3), `OFF` costs about 43 µA typical and up to about 100 µA maximum with the latch and gate controller included (§4.2, `E`), about 1.2–2.8% of the 2.5 Ah pack per month; the typical figure is below cell self-discharge, the maximum is comparable to it. This does not meet `PA-14`'s wording that `OFF` has only the pack protection path. **Either accept the charger's 17–24 µA as part of the pack and charge path and confirm the `PA-14` wording at registration, or add a battery-disconnect switch that closes only with an adapter; I take the first.**
4. **Pack absent.** With no pack, charging is disabled (missing thermistor) and `SYS` is regulated at `VSYSMIN`, so C2 and the display are powered from the adapter. That is a capability, not an assumed operating mode (`PA-09.8`).
5. **Trickle recovery from a tripped pack** works with defaults (§3.7), to be proved on the bench.


#### 4.5.1 Charger passives, straps and adapter (added 2026-09-25)

**Charger passives and straps (`D` datasheet unless marked):**

| Item | Value | Basis |
|---|---|---|
| `PROG` | **8.2 kΩ ±1%** to GND: 2S at 750 kHz, pairs with the 2.2 µH inductor (6.04 kΩ is 2S at 1.5 MHz with 1 µH) | Table 7-1 |
| Inductor | **2.2 µH, 750 kHz option.** Datasheet's own part: Würth `WE-LHMI 74437346022` (saturation current `U`, datasheet not read). Ripple at the worst case (15 V in, 8.4 V out, D ≈ 0.56): `ΔI = (15 − 8.4) × 0.56 / (2.2 µH × 750 kHz) ≈ 2.2 A p-p`, so peak inductor current is `ICHG 1 A + SYS load 0.6 A + 1.1 A ≈ 2.7 A` (`E`). The datasheet requires `Isat` above input or charge current plus half the ripple and at least 2 A for PFM pulses; **choose Isat ≥ 4 A** | §8.2.2.2 |
| Capacitors | `VBUS` 2 × 10 µF + 0.1 µF (25 V X7R, since 15 V is negotiated); `PMID` 3 × 10 µF + 0.1 µF (25 V); `SYS` 5 × 10 µF (16 V; 6 µF effective minimum); `BAT` 2 × 10 µF (16 V; 3 µF effective minimum); `REGN` 4.7 µF (10 V); `BTST1`/`BTST2` 47 nF (10 V or higher) | Design tables, §8.2 |
| `ILIM_HIZ` | `REGN` → 10 kΩ → pin → 6.8 kΩ → GND. `V ≈ 0.405 × REGN`; `REGN` is 4.6–5.2 V over VBUS 5–15 V, so the pin reads 1.86–2.10 V and the clamp is `(V − 1 V)/0.8 Ω`, **1.08–1.38 A** (`E`). The clamp stays below the 1.5 A negotiated current in every corner | Eq. (1), §7.3.4.3; `REGN` table |
| `TS` | `REGN` → `RT1` 5.23 kΩ → `TS`; `RT2` 30.1 kΩ from `TS` to GND; the pack's 103AT-2 NTC in parallel with `RT2` (datasheet's own values are 5.24 kΩ / 30.31 kΩ for T1 = 0 °C, T5 = 60 °C). With the 103AT-2 at 27.28 kΩ (0 °C) and 3.02 kΩ (60 °C; my recollection of the table, `U`), the divider gives 73.2% and 34.4% of `REGN`, inside the `VT1_RISE` (72.4–74.2%) and `VT5_FALL` (33.7–34.7%) windows | §7.3.9.5 |
| Pack NTC wiring | 103AT-2 on a cell surface (`PCB-01`), two wires to a small keyed 2-pin latching connector beside the SBS Mini; the return goes to pack negative (`P−`), so the 0.16 V ground shift at 11.7 A is irrelevant at the 1 A charge current (about 14 mV, 0.3% of `REGN`) | `E` |
| `CE` | 10 kΩ to GND through a 0 Ω link; charging is enabled by default, and it must not float | Pin table |
| `STAT` | Open drain to the C2 carrier, pulled up to 3.3 V there (10 kΩ); 1 kΩ series and 100 pF at C2. Low = charging, high = complete or disabled, blinking 1 Hz = fault | Pin table |
| `INT` | No connection (test header) | Pin table |
| `VSYSMIN` | Held at 7.12–7.52 V (7.2 V typical) when an adapter is present and the pack is below 7 V; charge current limited to 2 A in that regime | Electrical table; §7.3.9.2 |

**`STUSB4500` configuration (`D`; ST minimal-implementation schematic, Fig. 9):**

| Item | Value |
|---|---|
| Supply | `VDD` from VBUS (4.1–22 V); `VSYS` not connected. Idle sink current about 115–160 µA with an attached source, none when unplugged |
| Dead battery | `CC1DB`–`CC1`, `CC2DB`–`CC2` |
| PDO profile | `PDO1` 5 V / 1.5 A (fixed voltage); **`PDO2` 9 V / 1.5 A; `PDO3` 15 V / 1.5 A**; `POWER_ONLY_ABOVE_5V = 1`; `REQ_SRC_CURRENT = 0`; three PDOs; `PWR_OK` configuration left at its default |
| Power path | `VBUS_EN_SNK` → 100 kΩ pull-up to `VBUS` and the P-FET gate, 100 nF gate capacitor |
| Discharge | `VBUS_VS_DISCH` through 1 kΩ (max 50 mA); `DISCH` to a discharge resistor (max 500 mA); discharge times left at NVM defaults (756 ms / 288 ms) |
| Decoupling | `VREG_1V2` and `VREG_2V7` 1 µF each; VBUS TVS 25 V class |
| NVM | Programmed once at the bench over I2C (an `ADDR0`/`ADDR1` selected address, ST's tool). It runs standalone afterwards. The NVM image is configuration-controlled; verify by read-back |
| Why not `PDO` above 15 V | 20 V adds buck ratio and loss with no benefit at about 14 W |

**Adapter selection (`E`, and `U` for regulatory details):**

| Item | Value |
|---|---|
| Charger output at 1 A | `1 A × 8.455 V ≈ 8.5 W` |
| `SYS` load in `CHARGE` | C2 0.1 A + display 0.45 A (0.70 A peak) at 5 V = 2.75 W (4.0 W), 3.2 W (4.7 W) through the 85%-efficient converters |
| Total at the charger output | 11.7 W typical, 13.2 W peak |
| Input power at 93% (`E`; the datasheet efficiency figure was not read) | 12.6 W typical, 14.2 W peak |
| Input current | 15 V: 0.84 / 0.95 A. 9 V: 1.40 / 1.58 A |
| Class | **USB-C PD adapter of at least 30 W offering a 15 V profile at 1.5 A or more** (a common 5 / 9 / 15 / 20 V, 30 W adapter gives 22.5 W at 15 V/1.5 A, 1.6× margin). A 20 W adapter without a 15 V profile falls back to 9 V/1.5 A: the input clamp trims charge current by about 0.2 A during a display peak, which is acceptable |
| Not accepted | 5 V-only sources (`POWER_ONLY_ABOVE_5V` keeps the path open) |
| Regulatory | India BIS registration for the adapter (IT-equipment power adapter, IS 13252 (Part 1); `U`, confirm the current standard and CRS registration number on the label), Indian-socket plug, certified cable |

**Findings:**
1. **The `LTC2954` 512 ms `KILL` blanking cannot be met by an ESP32-S3 C2.** Fixed by the `KILL` node that the C2 branch rail raises and the C2 open-drain pulls low.
2. **A button press in `CHARGE` would latch `EN` and power `OPBUS` on unplug** unless `KILL` is forced low and the operating switch is hard-blocked. Both are added.
3. **A `CHARGE_ABSENT` derived from the C2 rail would disable the power button in `OFF`.** The `Q_dis`/`Q_kill` blocks are therefore driven from `VSNK`, not from any logic rail.
4. **The `SYS` gate needs a series Schottky.** With only the P-FET, its body diode would let the OR node feed `SYS`.

## 5. `PCB-03` — Motor gate and head/drive distribution board

**Purpose.** Implement `PA-13`: battery-only motor energy that appears only when **both** the system motor-arm and the hardware E-stop loop permit it, then split it into the head rail and drive feed with per-branch observation. This is the highest-consequence board; keep its logic simple and its default state open.

### 5.1 Motor permission

The registered permission is `MOTOR_PERMIT = E_STOP_OK ∧ SYSTEM_ARM ∧ CHARGE_ABSENT ∧ ENERGY_OK ∧ C2_READY ∧ BASE_READY(if installed)` (`brownout-restart-contract.md` `BR-05`). Every term is fail-inactive at its receiving boundary.

| Input | Source | Board treatment |
|---|---|---|
| `E_STOP_OK` | IDEC XA1E NC loop (`PCD-EST-01` family change, see §2) | Low-energy series loop in the permit chain (§5.2.3) with a local pull-down so an open or broken wire deasserts. It acts on the gate's **UV pin** (fast turn-off), not on `SHDN` (slow, §5.2.2). The second NC contact goes to C2 as independent status. **The E-stop contacts never carry motor current** |
| `SYSTEM_ARM` | `PCB-02` latch and C2 fresh-arm request | Latched, **cleared by E-stop assertion and by the loss of any other permit term** (a `UV` fault recovers on its own after 32 ms, so the arm latch, not the LTC4368, must force a fresh arm); release alone cannot re-arm (F-13, `power-implementation-basis.md` §8.3) |
| `CHARGE_ABSENT` | `PCB-02` charge-present detect | Hardware, not software |
| `ENERGY_OK` | `PCB-02` comparator | Hardware; its falling threshold (5.7 V, minimum 5.53 V) must sit above the LTC4368 `UV` release maximum (5.36 V) so `ENERGY_OK` acts first |
| `C2_READY_H`/`C2_READY_L` (complementary pair), `C3_READY` (`BASE_READY`) | Watchdog blocks on the C2/C3 carriers (§7) | Hardware-qualified, fail-inactive |

### 5.2 Gate — sized 2026-09-25 (`BD-07`)

`LTC4368-1` datasheet (Rev. C) read in full; every `D` below is from it. This is an engineering design, not a safety-rated subsystem (`PCD-EST-02`), and nothing is bench-proved.

**Decision `BD-07`: `LTC4368-1` (bidirectional, −50 mV reverse) with a 3 mΩ shunt, two back-to-back N-FETs, `RETRY` grounded (latch-off), permit applied to the `UV` pin, and `SHDN` driven by `SYSTEM_ARM`.**

#### 5.2.1 Device facts that shape the design (`D`)

| Fact | Value | Consequence |
|---|---|---|
| Operating input | 2.5–60 V; `VIN(UVLO)` 1.8–2.4 V | Covers the whole pack window |
| Forward trip | `ΔVSENSE,F` = 50 mV (40–60 mV) with `VOUT = VIN`; 40–60 mV at `VOUT` 0.5 V; **30–70 mV at `VOUT` 0 V** | Trip current is `ΔV / R`; a short at start-up trips at a looser threshold |
| Reverse trip (`-1`) | −50 mV (−42 to −58 mV) | Same order as forward: the regeneration allowance equals the forward limit |
| Overcurrent turn-off | Propagation 3–18 µs (8 µs typical) with a 2.2 nF gate; 60 mA (30–90 mA) fast pull-down | Fast |
| `UV`/`OV` turn-off | Comparator 1–2 µs, then 60 mA fast pull-down: 2–6 µs with a 2.2 nF gate | Fast |
| **`SHDN` turn-off** | **90 µA (40–160 µA) slow pull-down: 150–575 µs with a 2.2 nF gate** | About 7× slower for a 15 nF gate pair (estimate: about 1–2 ms). **Not suitable as the E-stop path** |
| Gate drive `GATE − VOUT` | 3–5.5 V at `VIN` 2.5 V; 7.2–10.8 V at 5 V; 10–13.1 V at 12 V or more | At the pack window 5.4–8.6 V the worst case is about 7.2–8.6 V, so the FETs must be fully enhanced at about 7 V |
| Gate pull-up | 35 µA (20–60 µA) | Sets turn-on slew and inrush (§5.2.5) |
| Turn-on delays | 32 ms (22–45 ms) after any `UV`/`OV` fault clears; 0.8 ms (0.4–1.4 ms) out of `SHDN` | The re-arm path is slow by 32 ms whenever `UV` was the cause |
| Forward overcurrent handling | `RETRY` grounded latches off; toggling `SHDN` low then high (15 µs up to `tLOWPWR` 20–48 ms) resets it; a capacitor on `RETRY` gives 5.5 ms/nF auto-retry instead | Latch is available, matching the no-auto-retry policy |
| Reverse overcurrent handling | Re-enables when `VOUT` falls 75–125 mV (20–125 mV for `VIN` under 6 V) below `VIN`; the comparators need `VOUT` above 2.2 V | The reverse trip self-recovers, unlike the forward latch |
| `FAULT` | High-voltage open-drain (rated to 80 V), low on any voltage or current fault, in shutdown, or below `VIN(UVLO)` | Usable as a gate-state input to C2 |
| Supply current | 30–100 µA operating (80 µA typical), 5–25 µA shutdown | Small; shutdown draw adds to the `OFF` budget |

#### 5.2.2 Why the E-stop acts through `UV`, not `SHDN`

`SHDN` is the datasheet's "slow, controlled" shutdown. The `UV` and `OV` comparators fire the 60 mA fast pull-down. A permit that drops through `SHDN` would leave the motor bus energised for a millisecond or more with two low-`Rds` FETs (about 15 nF gate charge at 90 µA) and would also let a shorted-out `SHDN` driver defeat the stop. **The permit therefore forces the `UV` node below its 0.5 V threshold.** `SHDN` is driven by `SYSTEM_ARM` (`PCB-02` latch) for the low-power state and to clear the forward-overcurrent latch; when `SYSTEM_ARM` clears on E-stop assertion, `SHDN` falls, and a fresh local arm raises it, which is the required fresh re-arm (F-13).
- The candidate screen's note that a broken E-stop loop deasserts `SHDN` (`power-component-candidate-screen.md` §6) is superseded by this: the loop acts on `UV`.
- **To confirm at the bench:** whether a `SHDN`-low period longer than `tLOWPWR` also clears the forward latch. The datasheet's timing figure only shows clearing for pulses shorter than `tLOWPWR`, so the E-stop-then-re-arm path must be shown to reset the latch, or the arm sequence needs a short deliberate `SHDN` pulse.

#### 5.2.3 Permit chain (hardware, no firmware)

`MOTOR_PERMIT` is a series chain of small switches from a low-power pull-up, so the permit node is high only when every term is true and any dead or missing signal opens the chain. The chain runs from the 5 V of `PB-SAFE-C2` (5.0 V nominal, `D`, `power-implementation-basis.md` §2.2), which is up in `OPERATE` and `CHARGE`.

`5 V (PB-SAFE-C2) → R_pu 470 Ω → E-stop NC contact 1 → Q_ARM → Q_CHG → Q_EN → Q_C2H → Q_C2L → Q_BASE (or jumper) → PERMIT node → R_pd 1 kΩ → 0 V`

- **Devices.** Each `Q` is a small-signal logic-level N-FET (BSS138 or 2N7002 class, `VGS(th)` at most 1.5 V, to verify at schematic) whose gate is its term signal (`SYSTEM_ARM`, `CHARGE_ABSENT`, `ENERGY_OK`, `C2_READY_H`, `BASE_READY`, all 3.3 V logic); `Q_C2L` is a P-FET on the active-low `C2_READY_L`, so a stuck wire cannot assert the C2 term (§7). Six stages add about 18 Ω (E).
- **Loop current (`E_STOP_OK`).** With 470 Ω in, 1 kΩ to ground and the chain, the loop current is `5 V / (0.47 + 1 + 0.018 kΩ) ≈ 3.4 mA` and the permit node sits at about 3.4 V (E). That meets the XA (and XW1E) "minimum applicable load 5 V, 1 mA" (`D`, reference value) with a factor of 3.4 and gives the permit node headroom over `Q_P`'s gate threshold. Contact 2 goes to C2 as status through its own 1 kΩ pull-up, not into this chain. The loop supply must be 5 V: 3.3 V is below the contact's reference test voltage.
- **`Q_P`, `Q_UV`, `Q_dis` default-on network.** `PERMIT` drives the gate of `Q_P` (N-FET). Two default-on nodes are pulled high by resistors and pulled low by `Q_P`:
  - `N1`: 470 kΩ to `VIN` (pack side, `BATBUS`), gate of `Q_UV`, whose drain is the LTC4368 `UV` pin and whose source is ground.
  - `N2`: 470 kΩ to `VOUT` (motor bus), gate of `Q_dis` (§5.2.6).
  - `PERMIT` high: `Q_P` on, `N1` and `N2` low, `Q_UV` and `Q_dis` off, so the divider sets `UV` normally and the bus is not discharged. `PERMIT` low, permit logic unpowered, or any wire open: `Q_P` off, `N1`/`N2` high, `Q_UV` on (holds `UV` below 0.5 V, gate off in about 2–6 µs plus the FET gate time, §5.2.5) and `Q_dis` on. Both pull-ups draw current only while `Q_P` conducts, about `8.4 V / 470 kΩ = 18 µA` each while armed (E), and nothing in `OFF`.
  - `Q_UV` leakage matters: the divider's Thevenin resistance at `UV` is about 270 kΩ, so 100 nA of leakage would move the threshold by about 27 mV at the pin (about 270 mV at `VIN`, 5%). Use a part whose leakage at `VDS` ≤ 0.5 V is far below 10 nA and confirm it (`U`).
- **Base jumper.** Without a base controller fit a jumper across the `Q_BASE` stage; a missing jumper leaves the gate off.
- **Truth table.** All six permit terms true (E-stop loop closed, `SYSTEM_ARM`, `CHARGE_ABSENT`, `ENERGY_OK`, both C2 lines in their asserted state, `BASE_READY` or its jumper) → gate on. Any term false, open, or its supply lost → gate off, fast, through `UV`.

**UV/OV divider (LTC4368 three-step procedure, `D`; values updated 2026-09-25 from the brownout proposals, §8.1).** Choose `VOS(UV)` = 3 mV and `IUV` = 10 nA (leakage): `R1 + R2 = 3 mV / 10 nA = 300 kΩ`. For `UV` falling at **4.9 V**: `R3 = 300 kΩ × (4.9 − 0.5) / 0.5 = 2.64 MΩ`. For `OV` rising at **9.55 V**: `R1 = (300 kΩ + 2.64 MΩ) / 9.55 × 0.5 = 154 kΩ`, `R2 = 300 − 154 = 147 kΩ` (E96). Divider order: `R3` from `VIN` to `UV`, `R2` from `UV` to `OV`, `R1` from `OV` to ground (`D`, LTC4368 Fig. 4). This replaces the 5.0 V placeholder, whose worst-case release left only 0.06 V of margin below `ENERGY_OK`.
- **Hysteresis.** `UV` has 25 mV at the pin (20–32 mV): release at 5.15 V (maximum 5.36 V). `OV` releases at 9.07 V.
- **Tolerance.** Comparator ±1.5% (492.5–507.5 mV) plus 1% resistors plus 3 mV of leakage offset gives a falling threshold of about 4.75–5.05 V (E).
- **Standby.** `8.4 V / 3.0 MΩ = 2.8 µA` from the pack in every state (E).
- **Behavior near the threshold.** If the pack sags to 4.9 V under load the gate opens, the pack recovers, and the gate returns 32 ms after `VIN` exceeds the release (`D`), which can cycle at roughly 40–100 ms (E). The threshold order in §8.1 puts the firmware and `ENERGY_OK` thresholds above the `UV` release so load is shed first, and a permit-term loss must clear `SYSTEM_ARM`.

#### 5.2.4 Shunt and overcurrent sizing

Forward trip is `ΔV / R`. Bounds are set by the credible source peak (historical 4.8–11.7 A `E`, `power-branch-contracts.md`), the wiring and connector current limits, the pack's own trips (`PCB-01` §3.4, a 17.7–25.3 A window) and the LTC4368's ±20% comparator tolerance.

| Shunt | Forward trip (40 / 50 / 60 mV) | Reverse trip (42 / 50 / 58 mV) | Drop and power at 11.7 A | Verdict |
|---|---|---|---|---|
| 4 mΩ | 10.0 / 12.5 / 15.0 A | 10.5 / 12.5 / 14.5 A | 46.8 mV, 0.548 W | Lower corner (10.0 A) is below the 11.7 A historical peak: rejected |
| **3 mΩ** | **13.3 / 16.7 / 20.0 A** | **14.0 / 16.7 / 19.3 A** | **35.1 mV, 0.411 W** | **Selected** |
| 2 mΩ | 20 / 25 / 30 A | 21 / 25 / 29 A | 23.4 mV, 0.274 W | Upper corner above the pack's trips and the cells' 20 A: rejected |

- **3 mΩ ±1% shunt, at least 2 W: Bourns `CSS2H-2512K-3L00FE`** (4 W, TCR ±75 ppm/°C, `D`). It has two terminals, so Kelvin sensing is by trace routing from the inner pad edges; the Vishay `WSK2512` is true four-terminal but only about 1 W. The `SENSE` and `VOUT` traces go only to the shunt (`D`, layout rule).
- The lower corner (13.3 A) leaves 14% over the historical 11.7 A peak. That peak is `E` and not a credible aligned peak (`CC-PEAK-01` is unmeasured). **If measurement shows a higher credible peak, the trip must be raised or the peak reduced by firmware, not accepted as a nuisance-trip rate.**
- **Layer order (`E`).**

| Layer | Trip | Time |
|---|---|---|
| `LTC4368-1` forward | 13.3–20.0 A (10–23 A at a start-up short) | about 8 µs |
| `LTC4368-1` reverse | 14.0–19.3 A into the pack | about 8 µs |
| `PCB-01` discharge overcurrent | 17.7–25.3 A (typical 24.1 A at 25 °C) | 8 ms |
| `PCB-01` short | 37–72 A (typical 60 A at 25 °C) | 280 µs |
| `ATOF` main fuse | 15 A (`0287015.L`, 340 A²s, 12 A at 65 °C); clears a 30 A fault in 0.15–5 s and a 147 A short in about 16 ms | Seconds for a low overload |

The gate is the first electronic layer at room temperature and cold. **The two windows overlap** (gate 13.3–20.0 A against the pack 17.7–25.3 A), so in the corner where the pack trips low and the gate trips high, a sustained 17.7–20 A would open the pack after 8 ms instead of the gate. The `ATOF` family clears a low overload only in seconds, so it is a wiring protector, not selective against the gate.
- **Regeneration limit.** With `-1` the gate lets 14.0–19.3 A flow *into* the pack. The pack's own charge overcurrent (16.8–26.5 A, typical 24.1 A, `PCB-01` §3.4) is above the gate's reverse trip, so neither limits regeneration. The cells' maximum charge current is **4 A** (Samsung 25R, rapid charge), so **the drive stage must hold regeneration into the bus to ≤ 3 A (75% of the cell limit) and to zero below 0 °C**, which nothing enforces yet. Regeneration is bounded in practice by the drive motors' short-circuit current and the DRV8874 current limit, not by the gate: set the driver current limit and the C3 braking limit accordingly; the gate's reverse trip is a last resort.

#### 5.2.5 FETs, gate slew and inrush

**Selection: two Nexperia PSMN1R0-30YLE (30 V, LFPAK56), common source, per the LTC4368 back-to-back arrangement.** Fallback PSMN1R2-30YLD (30 V, 1.2 mΩ typ, 1.6 mΩ max at 4.5 V, 2.64 mΩ max at 150 °C, Ciss 4616 pF typ, QG 68 nC quoted for the higher drive; no hot-swap SOA claim).

| Item | Value |
|---|---|
| Voltage | 30 V rating against a 8.6 V pack plus ringing (L·di/dt at 20 A through 300 nH in 1 µs is about 6 V) (`D`/`E`) |
| Gate drive available | LTC4368 `GATE − VOUT` is 7.2–10.8 V at `VIN` = 5 V and 10–13.1 V at 12 V (`D`); at the pack's 5.4–8.6 V it is about 7.6 V minimum (E). The FET's 7 V rows apply |
| `RDSon`, each | 7 V: typ 1.17, max 1.55 mΩ (25 °C); max 2.9 mΩ at 150 °C (`D`). Typical at about 125 °C is about 1.9 mΩ (E); the datasheet maximum at 150 °C exceeds the 2 mΩ target |
| Pair, hot | About 3.8 mΩ typical, 5.8 mΩ at the datasheet maximum (E) |
| Path budget | 3 mΩ shunt + 3.8 mΩ typical FETs = 6.8 mΩ (8.8 mΩ maximum hot): 80 mV and 0.93 W at 11.7 A typical, 103 mV and 1.2 W at the maximum (E) |
| `Ciss` / gate charge | Pair `Ciss` 5.9 / 9.9 / 14.8 nF (min / typ / max); `QG(4.5 V)` 30 / 66 / 108 nC (`D`, ×2) |
| Fast turn-off | `C × ΔV / I` = 10 nF × 8 V / 60 mA ≈ 1.3 µs typical, 15 nF × 8 V / 30 mA ≈ 4 µs worst, on top of the 2–6 µs propagation delay (`D`/`E`) |
| Slow turn-off (SHDN only) | 10 nF × 8 V / 90 µA ≈ 0.9 ms typical, up to about 3 ms (E). Not used for the E-stop |

**Motor-bus capacitance (assumption, `E`): 1000 µF, range 400–1500 µF.** Basis: two 330 µF polymer bulk capacitors on `PCB-03` (660 µF), about 100 µF near each DRV8874 carrier (200 µF; the Pololu page gives no carrier bulk value, `U`), the `LTC3119` head converter input (about 100 µF bulk plus 2 × 22 µF ceramic, derated to about 30 µF effective at 8 V; the datasheet asks 10 µF or more, `D`), and about 10 µF of other ceramics.

**Inrush.** `IINRUSH = COUT / CGATE × IGATE(UP)` with `IGATE(UP)` 35 µA (20–60 µA, `D`). Target about 2 A (15% of the 13.3 A minimum forward trip):
- `CGATE = 35 µA × 1000 µF / 2 A = 17.5 nF`, **use 18 nF** (X7R, 25 V) **in series with `RGATE` = 22 kΩ** from the `GATE` node to ground, following the datasheet application circuits (Fig. 2 and Fig. 7: 22 kΩ, 2.2–3.3 nF; the 22 kΩ keeps `CGATE` from slowing the fast pull-down; confirm the topology against those figures at schematic, `U`).
- Inrush: 1.94 A nominal, 1.1–3.3 A across the pull-up spread; for 1500 µF, 2.9 A nominal, up to 5 A. Add about 0.3 A of turn-on load (E): 3.6–5.3 A, far below the 13.3 A minimum forward trip (`D`/`E`).
- Ramp: slew `35 µA / 18 nF = 1.94 V/ms`, so about 4.3 ms to 8.4 V (2.5–7.6 ms across the pull-up spread).

**SOA checks (`D` figure, read ±30%; `E` arithmetic).**
- **Inrush into the bus:** 3.3 A worst at up to 8.4 V for about 3–8 ms, 28 W peak decaying. The PSMN1R0-30YLE SOA at `VDS` ≈ 8–10 V, 25 °C, allows about 30 A at 10 ms and about 65 A at 1 ms; at 125 °C roughly 60% of that. Margin about 6× or better. Energy in the load-side FET is about `½ C V² = 35 mJ` (1000 µF at 8.4 V), `Zth` far below its limit.
- **Turn-on into a hard short:** the forward threshold at `VOUT` = 0 V is 30–70 mV (`D`), so 10–23.3 A trip at 3 mΩ. Worst pulse: 8.4 V × 23.3 A ≈ 196 W for the 18 µs maximum propagation (`D`) plus about 4 µs of gate discharge ≈ 22 µs, ≈ 4.3 mJ. The SOA at 10 µs, 10 V is about 300 A, at 100 µs about 150 A (read off the plot), so the margin is over 10× at 23 A.
- **Steady:** 16.7 A nominal trip × 3.8 mΩ hot ≈ 1.1 W in the pair, easily inside `Rth(j-a)` 42 K/W on a good pour (E).
- **Not covered:** a repeated fault every 32 ms cannot occur because the forward fault latches; a UV/OV chatter cycle does not involve overcurrent.

**Shunt.** Bourns CSS2H-2512K-3L00FE (3 mΩ ±1%, 4 W, TCR ±75 ppm/°C, AEC-Q200, 6.35 × 3.05 mm, `D`).
- Dissipation: 0.41 W at 11.7 A, 0.84 W at the 16.7 A trip, 1.2 W at the 20 A upper corner for microseconds (E).
- Layout: the LTC4368 `SENSE` and `VOUT` traces run only to the inner edges of the two shunt pads, as a differential pair, with no other connection (`D`, datasheet layout rule); load current enters and leaves through the outer copper. Keep `VIN` to the FET drain short, keep the gate trace short and the number of components on `GATE` minimal, and place the `VOUT` ceramics next to the load-side FET (`D`).
- TCR: 100 °C of self-heating shifts the trip by 0.75% (E).

#### 5.2.6 Stored energy and bus protection

**Bus TVS: SMBJ10A**, cathode to the motor bus, on the load side of the gate.
- Clamp ratings (`D`): VRWM 10 V, VBR 11.1–12.3 V at 1 mA, VC 17.0 V maximum at 35.3 A, leakage 5 µA maximum at 10 V (Littelfuse; ST quotes 0.2 µA typical, 10 µA maximum at VRM).
- Against the parts on the bus: the LTC3119 `PVIN` absolute maximum is 19 V (`D`), so the 17 V clamp leaves 2 V; the DRV8874 `VM` absolute maximum is 40 V and its operating range 4.5–37 V (`D`), the FETs are 30 V, and the LTC4368 `VOUT`/`SENSE` are rated 80 V.
- At 8.6 V pack maximum the standoff (10 V) leaves 1.4 V, so leakage is small. At lower surge currents the clamp is well under 17 V: the ST data sheet gives a dynamic resistance of 0.127 Ω, about 14 V at 10 A (E).
- Regeneration: a 600 W (10/1000 µs) device absorbs the small head and wheel back-EMF pulses (E). A sustained clamp condition means the gate is open and the bus is floating, which is a fault to report through `FAULT`.

**Stored-energy discharge (fail-safe, F-12).** The bus holds `½ C V²` = 35 mJ (1000 µF at 8.4 V; 53 mJ at 1500 µF).
- `Q_dis`: 30 V logic-level N-FET (AO3400A class, to verify) across a **22 Ω, 2 W** pulse-rated resistor from the bus to ground. Its gate is `N2`, the default-on node from §5.2.3 (470 kΩ to `VOUT`, pulled down by `Q_P` while permit holds).
- Peak `8.6² / 22 = 3.4 W` for a few milliseconds, `τ = 22 Ω × 1000 µF = 22 ms`, to 1 V from 8.4 V in `2.13 τ` ≈ 47 ms (E, load-free bus; the head converter and drivers speed it up).
- Since `N2` is pulled up from the **bus**, not the pack, the discharge FET is off whenever the bus is already dead and draws nothing in `OFF` (E).
- The discharge time is a placeholder (registered value open in `brownout-restart-contract.md`); change `R` to scale it (`τ = R × C`).

#### 5.2.7 Latch clear and re-arm

**Datasheet position (`D`, LTC4368 Rev. C).** With `RETRY` grounded a forward overcurrent fault latches the FETs off. "The external MOSFETs are kept in the off condition until the SHDN input pin is toggled low then high (`tCLEAR` pulse width < `tLOWPWR`)" (Fig. 9). `tCLEAR` (minimum SHDN pulse to clear) is 15 µs; `tLOWPWR` (delay from turn-off to low-power operation) is 20 / 32 / 48 ms; coming out of shutdown takes `tSTART` 0.4 / 0.8 / 1.4 ms; then the 32 ms (22–45 ms) gate turn-on delay. **The datasheet does not say whether a SHDN-low period longer than `tLOWPWR` also clears the latch (`U`).**

**Design that is safe either way.** Drive `SHDN` high by `SYSTEM_ARM` (through 10 kΩ) so the part sleeps when disarmed, and add a hardware pulse that pulls `SHDN` low for about 0.8 ms roughly 4 ms **after** `SYSTEM_ARM` rises. By then the part is out of shutdown (`tSTART` ≤ 1.4 ms), so this is a genuine low-then-high toggle of about 0.8 ms, inside the 15 µs to 20 ms window. If the latch was already cleared the pulse is harmless.
- Delay stage: `SYSTEM_ARM` → 47 kΩ / 100 nF → half of a dual Schmitt inverter (74LVC2G14 class), giving an output edge about 3.1–4.0 ms after `SYSTEM_ARM` rises (E, supply 3.3 V, threshold 1.6–1.9 V). A second inverter restores polarity.
- Pulse stage: 47 nF coupling capacitor, 22 kΩ to ground, into the gate of an N-FET `Q_clr` whose drain is the `SHDN` node. The decaying gate spike keeps `Q_clr` on for about `0.79 × 22 kΩ × 47 nF ≈ 0.8 ms` (E). A small diode across the 22 kΩ clips the negative spike when `SYSTEM_ARM` falls.
- Sequence to bus energized: about `4 ms + 0.8 ms + 1.4 ms + 32 ms + ramp (5 ms) ≈ 43 ms` after `SYSTEM_ARM` rises (E).
- **Confirm at the bench:** clear after a long SHDN-low (to learn the answer to the open question) and after the 0.8 ms pulse.

### 5.3 Drive feed (`PB-DRIVE`)

Pack-native from `PB-MOTOR` per `BD-02`, for two Pololu 4035 DRV8874 carriers.

**Carrier facts (`D`, Pololu 4035 page and specs).**
- Motor supply 4.5–37 V (the pack window fits); continuous 2.1 A per channel, peak 4.4 A default (with 5 V on `SLEEP`; the DRV8874 itself allows 6 A peak and about 6 A overcurrent, TI); current sense 1.13 V/A; logic 1.8–5.5 V; size 0.6 × 0.7 in.
- On board: the DRV8874 (HTSSOP), a reverse-voltage-protection MOSFET (the `VM` pin is after it; its drop is not published, `U`), `VREF` pulled up to `SLEEP` through 10 kΩ, `CS` pulled down through 2.49 kΩ (sets the 4.4 A limit), `IMODE` pulled down through 20 kΩ (cycle-by-cycle chopping, automatic overcurrent retry). Bulk capacitance is not stated (`U`).
- Pins: `VIN`, `GND`, `OUT1`, `OUT2`, `SLEEP`, `EN/IN1`, `PH/IN2`, `PMODE`, `IMODE`, `VREF`, `CS`, `FAULT`.
- **Current limit.** Lower it with a resistor from `VREF` to ground or an external `VREF`; raise it with a resistor from `CS` to ground; grounding `CS` disables chopping (the 6 A overcurrent protection remains). Set it to the chosen motor's rated stall current once the 6 V gearmotor variant is known (`U`).
- **Regeneration and braking.** The Pololu page is silent. From the TI data sheet: in slow-decay brake both low-side FETs are on and the motor's energy dissipates in the motor and bridge; in coast the current recirculates through the body diodes, which returns it to the supply. Rule (E): stop with brake, not coast, to keep regeneration off the bus; the drive stage must still assume up to the motor's short-circuit current can return through the gate (§5.2.4 regeneration limit).

**Connection.** Two short paired supply conductors from `PCB-03` to each carrier (Micro-Fit+, `PCD-CON-03`), with about 100 µF and a 0.1 µF ceramic placed at each carrier's `VIN` (assumption included in the 1000 µF above), and `OUT1/OUT2` to the motor. Per-motor observation for C3: `CS` (1.13 V/A) to a C3 ADC input and `FAULT` (open-drain) to a C3 input with a pull-up. `SLEEP` is driven by C3 through one more series N-FET stage driven by `BASE_READY`, so a lost or reset C3 sleeps the driver in hardware. Nothing on this feed may block reverse current; the bidirectional gate is why. **Hard requirement (from the cells' 4 A charge limit):** C3 braking policy and the DRV8874 current limit must keep regeneration into the bus at or below 3 A and at zero below 0 °C.

### 5.4 Head rail (`PB-HEAD`)

**Case C01/M181 (default, matches the registered `PB-HEAD` row).** A 5.0 V converter from `PB-MOTOR` feeding yaw, pitch and roll.

| Item | Value / rule | Basis |
|---|---|---|
| Servo terminal | 5.0 V nominal within 3.7–6.0 V; per-axis drop ≤ 150 mV from converter output to servo terminal during `CC-06` | `PB-HEAD` row; `power-implementation-basis.md` §5.4 |
| Per-axis current | 1.80 A stall at 5 V for both the XC330-M288-T and the M181-T (`D`, ROBOTIS e-manuals) | Ledger; §5.4.3 |
| Aligned stall | 3 × 1.80 = 5.40 A synthetic stress, 27 W; not `CC-PEAK-01` | Ledger |
| Converter | **`LTC3119` wide-input synchronous buck-boost (`BD-05`), not a buck.** `PCD-CVT-01/-02` Murata OKL/OKR are not admissible for `PB-HEAD` | §5.4.1–5.4.2 |
| Regeneration | The `LTC3119` does not sink reverse current (zero-current detection), so an active clamp at 5.74 V (§5.4.2) bounds the rise; the clamp also helps the E-stop discharge | `LTC3119` datasheet; §5.4.2 |
| Bulk capacitance | Do not add large capacitance until converter stability, hot-plug, regeneration and E-stop discharge are evaluated together | `power-implementation-basis.md` §7 |
| Per-axis observation | Shunt monitor per servo, source-end current and load-terminal voltage sense | `PA-08` |
| Per-axis containment | **Decided (`BD-13`).** Five layers: per-axis servo Current Limit in Current-based Position Control Mode (yaw 0.9 A, pitch 0.8 A, roll 0.6 A, sum 2.3 A, ceiling 4 A); servo self-protection (Shutdown 0x35, Voltage Limits 3.7–6.0 V, Bus Watchdog 100 ms); the `LTC3119` current limit; a latching `TPS259824ONRGE` on the trunk at about 7 A; and independent `INA180` shunt monitors on the pitch-and-roll trunk and the yaw branch with a hardware `HEAD_OC` flag | XC330 e-manuals (`D`); §5.4.3 |

#### 5.4.1 Head-rail headroom — resolved 2026-09-24

**Finding (`D`, Murata OKL-T/6-W12/W5 datasheet, "Voltage Range Graph", "these limits apply at all output currents").** For a 5.0–5.1 V output the lower input limit is about **6.3–6.4 V** (graph read, ±0.2 V). It is flat at 4.5 V up to 3.63 V output and rises to about 7 V at 5.5 V output. So the OKL buck cannot regulate 5 V from the 6.0 V low line, and cannot at all from the 5.4–5.7 V near-empty sag in the ledger §5.3. The earlier "dropout is unknown" worry was worse than assumed: it is not a matter of a few hundred millivolts of headroom, the buck is out of range.

Two datasheet inconsistencies should be settled at the bench and not relied on: the OKL "low line" input-current row (6.2 V, 5 V out, 6 A → 4.54 A) implies 30 W out from 28 W in, and it conflicts with the voltage-range graph; and the OKL has 11 A current-limit inception with **hiccup auto-retry** on a short, which is the retry behavior `power-component-candidate-screen.md` §5.3 says not to default to on a persistent-fault path.

**The head rail's credible load is small (`E`, arithmetic on registered inputs).** The stall 1.80 A/axis (`D`, M181 and M288 at 5 V) is a fault case. The controlling torque peaks (`../RP-01-head/actuator-screen-01.md`: pitch 0.0953, roll 0.0560, yaw 0.1099 N·m) at the 5 V torque constants `K = stall torque / stall current` give:

| Axis | Servo | `K` (N·m/A) | Peak torque | Torque-derived current |
|---|---|---:|---:|---:|
| Yaw | M181 | 0.60 / 1.80 = 0.333 | 0.1099 | 0.33 A |
| Pitch | M288 | 0.93 / 1.80 = 0.517 | 0.0953 | 0.18 A |
| Roll | M288 | 0.93 / 1.80 = 0.517 | 0.0560 | 0.11 A |
| Sum, if coincident | | | | **0.62 A** |

Friction, internal acceleration (unknown per the screen) and idle current sit on top, so a head-rail **design allowance of 2 A** (about 3× the torque-derived sum, 10 W) and a **stall envelope of 5.4 A** (3 × 1.80 A, synthetic) are used. At 6.0 V in and 90% efficiency the design allowance draws only about 1.85 A from the pack, so the head is a small contributor to the pack sag; the sag comes from the whole system.

**Options and result.**

| Option | Result |
|---|---|
| Keep a buck and raise the `EN-02/03` floor so the loaded pack never falls below about 6.6 V (6.4 V limit + margin) | At the ledger's 80–100 mΩ pack and a 4.8 A credible source current the drop is 0.38–0.48 V, so the pack must stay above about 7.0–7.1 V open circuit (about 3.5 V/cell). That strands roughly a quarter of the capacity (`E`) and leaves less reserve, in the cold and when aged, against the 9.2 Wh requirement. **Rejected** as the only defence |
| Lower the head rail toward 4.5 V to buy headroom | Cuts speed and torque (M181: 129 rpm at 5.0 V, 95 rpm at 3.7 V) and still leaves the buck only about 5.7 V. **Rejected** |
| **Wide-input synchronous buck-boost** | Regulates through the whole pack window and through the sag. **Selected.** Costs some efficiency and needs a converter that is verified for the output current and for regeneration |

**Head-converter requirements.**
- Input 4.5–8.6 V minimum operating, regulating down to the `EN-03` cut-off threshold, with the converter's own UVLO set below that threshold as a last resort.
- Output 5.0 V within the servo 3.7–6.0 V window, ≥ 3 A continuous, with the 5.4 A stall envelope bounded by the servo current limits (§5.4.2).
- Enabled only by `MOTOR_PERMIT` through a **hardware** enable pin, so the converter is off whenever the gate is open, without depending on firmware or a bus.
- Persistent-fault behavior: latch-off, supplied by an upstream latching protector if the converter has none.
- Regeneration bounded below 6.0 V (servo maximum) by a clamp if the converter cannot sink it.

#### 5.4.2 Buck-boost selection — decided 2026-09-24 (`BD-05`)

Both candidates were read from their datasheets (TI SLVSF01B and ADI 3119fb, retrieved 2026-09-24).

| | ADI `LTC3119` | TI `TPS55288` |
|---|---|---|
| Input | 2.5–18 V, runs down to 0.25 V after start-up (`D`) | 2.7–36 V, VIN UVLO about 3 V (`D`) |
| 5 V output current | **5 A for Vin > 6 V; 3 A at Vin = 3.6 V** (`D`, front page); no figure at 5.4 V (see below) | Not stated for 5 V out from a 5.4 V input |
| Power switches | Four N-channel, 30 mΩ each (`D`) | Boost side 7.1 / 7.6 mΩ (`D`); buck side not extracted |
| Current limit | Fixed inductor limit 7–8 A (`D`); not adjustable | Average inductor limit set by `RILIM` (about 16.5 A at 20 kΩ, 5.5 A at 60 kΩ, `D`); output limit up to 6.35 A in 50 mA steps by I2C |
| Configuration | Analog only: `FB` divider, `RT`, `RUN` | I2C registers; **`OE` resets to 0, so the output stays off until a master writes it** (`D`); `MODE` resistor sets I2C address, VCC and PFM |
| Enable | `RUN` pin comparator, 1.205 V, programmable UVLO, hardware only | `EN/UVLO` pin **and** the `OE` register bit |
| Short circuit | "Output short-circuit protection"; no hiccup or latch documented | Hiccup on by default (76 ms off), can be disabled; no latch |
| Reverse current | Zero-current detection, discontinuous mode; **does not sink** (`D`) | In FPWM the inductor current reverses and power flows output to input (`D`); the magnitude is not specified |
| Output monitoring | `PGOOD` open-drain | ±5% output-current monitor and status register |
| Output overvoltage | None listed | 22.5–24.5 V, useless as a 6 V servo guard |
| Quiescent | 31 µA sleep, 3 µA shutdown | 1.3 mA |
| Package | 28-lead 4 × 5 mm QFN or 28-lead enhanced TSSOP, θJA 21–22 °C/W | 4.0 × 3.5 mm VQFN-HR (Hotrod) |

**Decision `BD-05`: `LTC3119` for both `PB-HEAD` and `PB-COMPUTE` in V1, in the TSSOP-28 package.** `TPS55288` is the recorded fallback.
- **No firmware in the permission chain.** `PB-HEAD` is enabled by a hardware pin from `MOTOR_PERMIT`; `PB-COMPUTE` needs no I2C master. A `TPS55288` cannot start without a bus write, and the natural I2C master (C2) is on the far side of the moving joint from the converters.
- **Stated current margin.** 5 A at Vin > 6 V and 3 A at 3.6 V are datasheet claims against the 2–2.4 A Pi workload and the 2 A head allowance.
- **One part, one family** for two rails, and a TSSOP that can be hand-reflowed.
- **What it costs.** Higher switch resistance (30 mΩ ×4), no adjustable limit, no sinking, no latch. Each is covered below.

**Fallback triggers** (move a rail to `TPS55288`): the `LTC3119` heats beyond its limit at the bench, its output current at 5.4 V Vin falls short of ≥ 3 A, or the head rail's regeneration cannot be bounded by a clamp.

**Component design of the two `LTC3119` rails (2026-09-25, `D` from the ADI 3119fb, TI TPS25982 and Coilcraft XAL50xx datasheets; arithmetic `E`).**

| Item | `PB-HEAD` | `PB-COMPUTE` |
|---|---|---|
| Protector | `TPS259824ONRGE`, `RILIM` 211 Ω (7.0 A nominal, about 6.2–7.8 A over temperature), `CITIMER` 4.7 nF (2.2 ms), `RETRY_DLY` to ground (latch-off), `CdVdt` 3.3 nF, `RIMON` 1.00 kΩ, `EN/UVLO` from a 280 k / 100 k divider on the bus | same, `CITIMER` 22 nF (10 ms), `EN/UVLO` from the sequence enable with a 100 kΩ pull-down |
| Converter | `LTC3119` TSSOP-28, `RT` 162 kΩ (494 kHz), forced PWM, `MPPC` and `SVCC` to `VCC` | same |
| Inductor | Coilcraft `XAL5030-332ME`, 3.3 µH, `Isat` 8.7 A, DCR 21–23 mΩ | same |
| Output | 220 µF polymer + 3 × 22 µF ceramic, about 290 µF; 22 µF at the head end | same |
| Input | 2 × 10 µF + 1 µF ceramic + 47 µF polymer | same |
| Feedback | 536 k + 3.48 k / 102 k: 5.000 V, 4.891–5.109 V worst case | 552.4 k / 102 k: 5.100 V, 4.989–5.212 V (5.15 V recommended: 619 k / 113 k, 5.038–5.262 V) |
| Compensation | `RZ` 95.3 kΩ, `CP1` 240 pF (datasheet start 100 kΩ / 560 pF), confirm by load step | same |
| Regeneration | TL431 + PNP clamp at 5.74 V, 27 Ω 2 W dump | none |
| `RUN` UVLO | 280 k / 100 k: 4.58 V rising, 4.17 V falling | same |

**Capability (E).** 91–89% efficiency at 2 A and 90–88% at 3 A from 5.4–7.4 V; loss 1.0–1.2 W at 2 A and 1.7–2.1 W at 3 A; about 25–35 °C rise at 2 A and 45–65 °C at 3 A on a good board, so 3 A continuous is marginal at 8.4 V in and sustained 4 A or the 5.4 A stall cannot be supplied at low input (the rail sags and the servos reset, F-11); the firmware current limits and the latching protector are the containment. The datasheet guarantees ≥ 3 A at 5.4 V by its own statements (5 A above 6 V, 3 A at 3.6 V); the output-current curve itself was unreadable.

Chain for each rail: source (`PB-MOTOR` for the head, `OPBUS` for the Pi) → latching `TPS259824ONRGE` (7 A) → `LTC3119` → output, with the clamp on the head rail only. The bootstrapping of `VCC` from `VOUT` was rejected: the datasheet's forcing window (4.2–5.5 V) is exceeded by a 5.8 V regeneration rise, and on the Pi rail it gains nothing (55 mW against 66 mW).

**Compute setpoint.** The 5.10 V rail's worst-case low is 4.989 V at the converter: it passes the 100 mV steady allowance but fails the 200 mV transient one (4.789 V against 4.8 V). 5.15 V (619 k / 113 k) passes both, so it is the recommendation; the change from 5.10 V is a registration decision and is left open.

**Consequence for `PB-COMPUTE`.** The same Murata voltage-range graph applies to the compute lead `PCD-CVT-01`: 5.1 V out needs about 6.4 V in, so it does not hold the 6.0 V low line either (candidate-screen addendum §4.4). §6 is updated to the `LTC3119`.

#### 5.4.3 Per-axis protection and servo configuration — decided 2026-09-25 (`BD-13`)

Facts are from the ROBOTIS XC330-M288-T and M181-T e-manuals (`D`).
- **Defaults limit nothing.** Current Limit defaults to 2,352 mA against a 1.80 A stall at 5 V, and it applies only in Torque Control and Current-based Position Control modes (the default Operating Mode is plain Position Control). C2 therefore programs Operating Mode 5 and Current Limit (yaw 0.9 A, pitch 0.8 A, roll 0.6 A, sum 2.3 A) before torque enable and reads them back. At those limits the torque margin over the actuator-screen peaks is 2.7× (yaw, 0.30 N·m against 0.1099), 4.3× (pitch) and 5.5× (roll), using Kt at 5 V (M181 0.333, M288 0.517 N·m/A).
- **Servo self-protection:** `Shutdown = 0x35` (the default 0x34 omits input-voltage error even though the manual lists it as default), `Max Voltage Limit` 6.0 V, `Min Voltage Limit` 3.7 V, `Bus Watchdog` 100 ms. A tripped servo needs a Reboot, sent by C2 only after a fresh arm. Startup torque is off by default.
- **Rail overload (F-11).** Three stalled servos are roughly resistive (2.78 Ω each at 5 V). With the `LTC3119` limited to about 4.5 A the rail falls to about 4.2 V (about 3.7 V at 4.0 A), near the servos' 3.7 V rated minimum, so an overload ends as servo shutdowns latched until Reboot, not as a converter collapse. This is a fault outcome.
- **Trunk protector and monitors.** A latching `TPS259824ONRGE` (about 7 A, above the roughly 5.7 A converter input at a 5.4 A stall) ahead of the converter; `INA180A2` analog shunt monitors (10 mΩ; ±1% gain error, ±150 µV offset at 0 V common mode, `D`) on the pitch-and-roll trunk and the yaw branch, on the body side, no I2C across the joint; a comparator sets `HEAD_OC` at about 4 A for more than 10 ms. Per-axis observation is each servo's Present Current (`D`, measured at its input).
- **Regeneration.** Passive back-drive returns about zero (back-EMF at peak speeds is below the 5 V rail); active braking is bounded at about 1.3 W (peak torque × peak speed, all three at once, E). Active clamp at 5.74 V (TL431 plus PNP) with a 27 Ω, 2 W dump (§5.4.2).
- **Joint conductors.** Four added AWG28 conductors: servo-bus `DATA`, a shared signal reference, `HEAD_OC`, `HEAD_PGOOD`.
- **If RP-01 selects the STS3215 7.4 V (C046)**, see the 7.4 V case below.

**Case 7.4 V-class servo (if RP-01 picks e.g. STS3215 C046, `D`: 5–8.4 V input, 6 V and 7.4 V rated points).** No head converter (the `LTC3119` head rail goes); feed directly from `PB-MOTOR`, per-axis observation unchanged. Stall is 2.6 A at 6 V and 3.3 A at 7.4 V per axis (9.9 A aligned; rated 1.1 A), and the trunk protector moves to about 12–14 A. **Conflict, not resolved here:** the servo's 8.4 V maximum is 0.65% below the charger's default-mode worst case (8.455 V) and there is no charger trim, so a fully charged pack exceeds it (§10). Yaw speed falls below 63 rpm near a 5 V pack. The bus becomes Feetech half-duplex TTL, not Dynamixel 2.0 (`link-contract.md`). A 12 V variant would force a 3S pack and reopen `PCB-01`, `PCB-02` and the tub.

### 5.5 Requirements common to the board

- **Layout.** Motor return goes straight back to the star point; it never passes through a signal or safety return (`PA-15.3–4`). Use heavy copper for the gate, shunt and drive feed (2 oz outer is a starting point, `E`), and keep the E-stop and `ENERGY_OK` traces out of the switching loop.
- **Connectors.** Micro-Fit+ for the head trunk and drive feed at the exact terminal and circuit derating; servo bus pins can never carry motor return.
- **Test points.** `PB-MOTOR`, `PB-HEAD`, per-axis current and voltage, `PB-DRIVE`, gate state, `MOTOR_PERMIT`, and each input term.
- **Evidence required.** Broken-wire safe state, hardware truth table, full-current drop and heat, FET SOA, regenerative current, F-12 assertion, downstream discharge, and release cannot re-arm.

## 6. `PCB-04` — Branch converter board

**Purpose.** Give each non-motor branch its own converter, protection and enable so that no branch failure resets another (`PA-05`, `PA-11`, `PA-12`). Every branch keeps its own paired return to the star; nothing is chained. Datasheets read 2026-09-25: TI TPS63070 family (which contains `TPS630701`), TI TPS25947, TI TPS22810, TI TPS2120/2121.

| Branch | Converter | Protection and source | Enable / status | Load |
|---|---|---|---|---|
| `PB-SAFE-C2` | `TPS630701RNMR` fixed 5 V buck-boost (`PCD-CVT-06`) | Two `TPS259474LRPWR` circuit-breaker latch-off e-fuses ORed at the converter input: `C2A` from `OPBUS`, `C2B` from gated `SYS` (§6.3); `RILM` 1.65 kΩ (2.0 A), `ITIMER` 4.7 nF | E-fuse `PG` → `EN`; `PG_C2` to the sequencing latch and the C2 brownout input; powered in `OPERATE` and `CHARGE` | 0.04–0.10 A working `E`, 0.50 A capability `D` |
| `PB-SAFE-BASE` | Second `TPS630701`, independent of C2 | `TPS259474LRPWR` from `OPBUS` only (off in `CHARGE`); same values | E-fuse `PG` → `EN`; `PG_BASE` to RP-03 | About 0.5 A `E` (RP-03 open) |
| `PB-COMPUTE` | **`LTC3119` (`BD-05`), 5.1 V (5.15 V recommended), 5 A for Vin > 6 V and ≥ 3 A at the sag floor (§5.4.2).** `PCD-CVT-01/-02` Murata OKL/OKR are demoted: they cannot regulate 5.1 V below about 6.4 V input (§5.4.1). `TPS55288` is the fallback | Latching `TPS259824ONRGE` (7 A, 10 ms blanking; **not** `TPS25947`, which drops 141.5 mV at 5 A), §5.4.2 | Enable from the sequencing latch into the protector `EN/UVLO` with a 100 kΩ pull-down; off in `CHARGE` and final `OFF` | Pi 5 up to 5 A interface, workload peak 2.0–2.4 A `E` |
| `PB-DISPLAY` | Third `TPS630701`, 1.0 µH inductor | Two `TPS259474LRPWR`: `DISA` from `OPBUS`, `DISB` from gated `SYS`; `RILM` 1.65 kΩ | E-fuse `PG` AND sequencing latch → `EN`; dual source | 0.45 A nominal `D`, 0.60–0.70 A peak `E` |
| `PB-AUDIO-OUT` | **Unselected.** Provisionally a `TPS630701` in forced-PWM mode (§6.5) | `TPS259474LRPWR`, `RILM` 1.65 kΩ, from `OPBUS` only | Sequencing latch → `EN`; off in `CHARGE` | Planning 5 V / 5 W class `E`; RP-05 open |

### 6.1 Device facts (`D`) and the naming
`TPS630701` is the fixed-5 V member of the `TPS63070` family (orderable `TPS630701RNMR`). It regulates 2.0–16 V in, 2 A out in buck mode and in boost mode at 4 V in, ±1% (PWM), 54 µA typ quiescent, load disconnect in shutdown, no output discharge, `EN` 0.8 V, `PG` open-drain. Its current limit is an *input* limit of 3.05–4.15 A; while `PG` is low the input limit drops to about 1 A ("typically"). Output capacitance total ≤ 470 µF (15 µF minimum), input hold-up capacitance has no maximum. The `TPS259474LRPWR` (`TPS25947` circuit-breaker, latch-off) is the only variant that latches on persistent overcurrent; it has true reverse-current blocking (block at −29 mV, re-enable at +104 mV), `ILIM = 3334/RILM`, 428 µA typ (610 µA max) quiescent, and a `PG` output asserted high when the path is on.

### 6.2 Current limits, blanking, inrush and hold-up
- **`ILIM` 2.0 A (1.80–2.20 A) for C2, base, display and audio.** 1.0 A would sit on the converter's own ~1 A start-up limit and nuisance-trip; 0.5 A is below the 0.51–0.72 A running input current at the 5.4 V sag. A converter-output short is cleared by the breaker before the converter's own limit acts.
- `ITIMER` 4.7 nF (2.4–6.8 ms). `IMON` 0.30 V/A at 1.65 kΩ: test points only, not across the yaw joint.
- **Hold-up: 3.3 mF on each of the C2 and base converter inputs, downstream of the e-fuse** (proposal from the brownout method, §8.1; the earlier 1 mF placeholder holds only 22 ms against a 25 ms soft path), with reverse blocking keeping it from discharging into a collapsing `OPBUS`. Inrush: `CdVdt` of about 13 nF for a 0.5 A inrush so the 2.0 A e-fuse does not trip during the roughly 14 ms charge. The value stays `U` until `t_HOLD_SAFE` and the load are measured (`brownout-restart-contract.md` §6). No hold-up capacitance on a converter output.
- Voltage drops (`§9.2` cable data plus Micro-Fit 3.0 at 10 mΩ per contact): C2 97 mV at 0.5 A, display 137 mV at 1.0 A, both inside the 150 mV allocation (display margin 13 mV).

### 6.3 Charge-mode source selection and the `SYS` gate
- In battery-only mode `SYS` is live from the battery, so anything fed from `SYS` needs an adapter-present gate. One `TPS22810DBVR` load switch (2.7–18 V, 2 A, 0.5 µA typ shutdown) between `SYS` and the node feeding `C2B` and `DISB`, enabled from `VBUS` so that no adapter means off. Using the e-fuses' own `EN` instead would add 8.8 µA typ (57 µA max) to `OFF`.
- OPBUS-side e-fuses leak 4.86 µA typ each into `OPBUS` in `CHARGE` (`OUT` above `IN`): fit a bleed resistor of about 47 kΩ on `OPBUS`.
- `TPS2121` power-MUX was rejected for the safety branches: minimum current limit 1 A and no latching breaker.

### 6.4 Sequencing and independence
Start: each OPBUS-side e-fuse charges its own capacitor; its `PG` (`PGTH` divider, rising about 3.4 V, falling about 3.05 V) enables its converter through a divider held at or below 5 V. `U_C2` and `U_BASE` start independently. The display, compute and audio enables are AND-ed with a `PCB-02` sequencing latch **set once by `PG_C2` and cleared only when `OPBUS` drops**, so a later C2 reset never turns off an application rail and never touches the base branch (`PA-11`). E-fuse reverse blocking and the converters' load disconnect prevent branch-to-branch back-feed; signals into unpowered domains stay high-impedance (`PA-11`.6).

### 6.5 Audio (provisional, unselected)
`TPS630701` in forced PWM (PS/SYNC low) to avoid audible-band ripple, `TPS259474LRPWR` at 2.0 A, `OPBUS` only. A 5 W class-D load draws about 1.0 A average at 5.4 V in and 2.0 A only at crests. **RP-05 must supply:** amplifier part; supply range and absolute maximum; RMS and crest current at the speaker; idle and shutdown current; power-up and power-down pop behavior; mute pin default (must default off); logic level and enable source; EMI needs; whether it takes the 5 V rail directly; and the microphone-side supply-ripple budget.

### 6.6 Other requirements (unchanged and additions)
- Same converter IC on C2, base and display does not merge them: separate devices, protection, returns, capacitors and enables.
- `PB-COMPUTE`: ≤ 100 mV steady and ≤ 200 mV transient drop to the Pi terminal, 5.1 V nominal, > 4.8 V reliable-operation guidance; power-entry method is a separate decision; no back-power of a powered-down Pi through USB, UART or CSI.
- Startup into installed capacitance: about 0.4–1.0 ms for C2 and display at 5.4 V in (`E`); measure the start-up input limit maximum.
- Display converter stability: 1.0 µH (right-half-plane zero 341 kHz at 3.0 V in with 1.2 µH, below the 400 kHz guideline) or extra output capacitance.
- Keep the noisy compute and audio converters away from the C2 and base converters and their sense lines.
- Test points: every input, output, `PG` and `IMON`; shunt point per branch.
- Evidence: cold/hot start-up, ORing transfer with 3.3 mF on each input, minimum-load regulation, quiescent current, short/breaker latch (including OPBUS dip seen by the other safety branch), `PG` timing, no cross-branch backfeed, `OFF` and `CHARGE` leakage with the `SYS` gate; for compute the sweep already listed.

## 7. Safety-carrier watchdog block (C2 and C3 carriers) — decided 2026-09-25 (`BD-10`)

**Decision `BD-10`: one TI `TPS3436CFDBEDDFRQ1` window watchdog per controller carrier** (`CCD-WDG-01`; pinout C, open drain, 10 s startup delay, 10 ms close window, ratio 4, 50 ms assert; released orderable, `D`). Datasheet SLVSGF1A read in full. Nothing is bench-proved.

| Item | Rule |
|---|---|
| Window | `tWC` 10 ms ±10%, `tWO` = 3 × `tWC` (`SET` low): guaranteed feed window **11–36 ms**; late-fault detection at most **44 ms** after the last edge (`D`/`E`) |
| Feed | Falling edge on `WDI` (C3 `GPIO48`), **every 20 ms**, from the safety-loop task only, after N consecutive healthy cycles (fresh inputs, valid config and heartbeat state, output readback, completed transaction, period in bound). Software refuses to feed within 12 ms of the last edge. `WDI` has a 10 kΩ pull-up |
| Reset | `WDO` (10 kΩ pull-up) pulls the MCU `EN` low for 50 ms. **Non-latched**: the datasheet latch releases on any `WDI` edge, so it would not enforce fresh arm |
| Startup | 10 s startup delay; the first valid `WDI` edge must arrive inside it (assumed boot ≤ 3 s, `E`); a hung boot resets every ≈ 10 s with READY low |
| `WD-EN` | Tied high; not connected to an MCU pin. Service jumper `JP_SVC` disables the watchdog **and forces READY low** |
| `MR` | Safety-converter power-good: a converter fault resets the MCU and drops READY (`BR-06`) |
| READY | `READY = WDO_high ∧ WD_EN_high ∧ MCU_RDY` (3-input AND on the carrier 3.3 V); `MCU_RDY` has a 10 kΩ pull-down and is set only after boot, hash check, first `WDI` edge and a healthy loop. `PCB-03` inputs have pull-downs. **C2 crosses the yaw joint as a complementary pair `C2_READY_H` / `C2_READY_L`** so a stuck-at wire fault cannot assert READY; `C3_READY` is single-ended |
| C3 pin | `GPIO2 = MCU_RDY` by change control; spares GPIO10 and GPIO38 remain (≥ 2, `CA-14`) |
| Fresh arm | Any permit-term loss, including READY, clears `SYSTEM_ARM` (`PCB-02`/`PCB-03`); a watchdog reset never resumes an old arm |
| Reset reason | NVS unclean-restart cookie; watchdog, brownout and power reset are indistinguishable in software (`E`) |
| Residual | A controller that feeds correctly but skips loop health is not caught by the device; an AND-gate stuck-high fault is caught only by injection (F-25/F-26) |
| Tests | F-25 and F-26 (early feed, absent feed, late feed, `JP_SVC`, `C2_READY` stuck faults, `PG` fall, debugger attached), evidence list below |

**Truth table.**

| Condition | `WDO` | `WD-EN` | `MCU_RDY` | `MR` (PG) | READY | Result |
|---|:-:|:-:|:-:|:-:|:-:|---|
| Healthy, fed every 20 ms | high | high | 1 | high | **1** | Permit term satisfied |
| Feed early (< 11 ms) or late/absent (> 44 ms) | low 50 ms | high | any | high | 0 | MCU reset, permit opens, `SYSTEM_ARM` cleared |
| Boot: no first edge within 10 s | low 50 ms | high | 0 | high | 0 | Reset loop, safe |
| MCU unpowered, reset or hung | any | high | 0 (pull-down) | high | 0 | Safe |
| `JP_SVC` fitted | high | low | any | high | 0 | Watchdog disabled, no motor authority |
| Safety converter `PG` falls | low | high | any | low | 0 | Reset with the converter |
| Feeds correctly but skips loop health | high | high | 1 | high | **1** | Not caught by this device (the feed-only-when-healthy rule and the C0 heartbeat) |
| AND gate stuck high | | | | | 1 | Residual; caught only by F-25/F-26 injection and, for C2, the complementary pair |

**Fallback and rejected variants.** `CCCBGD` (5 ms window, 500 ms startup, 200 ms assert) is the fallback and needs a 10 ms feed and a first edge inside 500 ms. Rejected: `CCCACD` (window only 5.5–9 ms), `CABFDD` (±20% timing), the capacitor-programmed pinout B parts, latched output `J`, and push-pull outputs (none released). **Sourcing:** the TI store showed the parts out of stock on 2026-09-25 and no India listing was found; check DigiKey India and Mouser India.

**Bench evidence.** Measured loop periods and jitter at the feed point, `tWC`/`tWO` corners over temperature and supply on five units, boot time to the first `WDI` edge, latency from the last edge to permit open, and the F-25/F-26 injections.

## 8. Inter-board signals

Signals cross `PCB-02`, `PCB-03`, `PCB-04` and the two carriers. Every hardware permission is fail-inactive.

| Signal | From → to | Type | Default |
|---|---|---|---|
| `BATBUS` | `PCB-02` → `PCB-03` | Power, paired | Present with pack |
| `OPBUS` | `PCB-02` → `PCB-04` | Power, paired | Off in `OFF` |
| `CHGBUS` | `PCB-02` → C2 and display converter inputs on `PCB-04` | Power, restricted | Off unless `CHARGE` |
| `PB-MOTOR` | `PCB-03` → head rail and drive feed | Power | Off |
| `PWR_BTN`, `HOLD` | button / C2 ↔ `PCB-02` | Logic | Off |
| `CHARGE_ABSENT` | `PCB-02` → `PCB-03` | Logic | Inactive |
| `ENERGY_OK` | `PCB-02` → `PCB-03`, C2 | Logic | Inactive |
| `E_STOP_OK`, `E_STOP_STATUS` | XA1E → `PCB-03`, C2 | Loop / logic | Inactive when open |
| `SYSTEM_ARM` | C2 → `PCB-03` (latched) | Logic | Inactive |
| `C2_READY_H`, `C2_READY_L` | C2 carrier → `PCB-03`, across the yaw joint as a complementary pair | Logic | Inactive |
| `C3_READY` (`BASE_READY`) | C3 carrier → `PCB-03` | Logic | Inactive |
| `MOTOR_PRESENT` | `PCB-03` → C2, C3 | Logic (observation) | Inactive |
| `EN_*`, `PG_*` | `PCB-02` / C2 ↔ `PCB-04` | Logic | Disabled |
| `V_PACK`, `I_PACK`, per-branch current | `PCB-02/03/04` → C2 ADC | Analog | — |
| `STAT` | `PCB-02` → C2 | Open drain, pulled up at C2 (3.3 V) | High |
| `INT_PB` | `LTC2954` → C2 | Open drain, pulled up at C2 (3.3 V) | High |
| `KILL` | C2 → `LTC2954` | Open drain; node pulled up by `+5V_C2` | High only when the C2 rail is up |
| `V_PACK_ANA` | `PCB-02` → C2 ADC | Analog, 33 k / 16.2 k, signal ground conductor | 0 V |
| `CHG_ABSENT_3V3` | `PCB-02` → C2 | Divider 33 k / 68 k from the 5 V node | Low |
| `+5V_C2` | `PB-SAFE-C2` → `PCB-02` | Logic supply for pull-ups and the comparator | Off |

A signal crossing into an unpowered domain must be high-impedance or otherwise bounded so it cannot back-power that domain (`PA-11.6`). Keep signal pin order so a partially mated connector cannot apply power through a signal pin.

### 8.1 Brownout proposals (2026-09-25; proposals only, evidence-gated by `brownout-restart-contract.md` §9)

**Basis.** Pack resistance cases (`R_src`, to `VIN`): A 71.5 mΩ (25 °C, fresh), B 115.5 mΩ (0 °C), C 93.5 mΩ (aged), D 159.5 mΩ (cold and aged, design corner); cold ×2.0 and aged +50% are estimates (`E`). The `PCB-01` path (about 13 mΩ hot, §3.4) replaces the ledger's 30 mΩ BMS allowance. OCV(SOC) is a generic NMC curve (`U`).

**`V_SRC_SAFE` = 4.6 V** (DRV8874 4.5 V + 0.12 V path); `V_SRC_REQ`: `LTC3119` head 4.03 V, Pi branch 4.26 V (converter floor 4.0 V, which is the 3.6 V datasheet point plus 0.4 V because the 5.4 V curve is not stated), `TPS630701` C2 and C3 2.52 V (3.02 V restart), gate 4.0 V.

**Soft thresholds (C2 firmware, current-compensated):** `V_CRIT_ASSERT = max(4.75 V + 9 A·R̂, 6.0 V)` (6.0 V for A/B/C, 6.19 V for D); `V_CRIT_CLEAR` +0.4 V (5 s, no peak load); `V_LOW_ASSERT` = `V_CRIT_ASSERT` + 0.5 V (6.50 / 6.69 V); `V_LOW_CLEAR` +0.4 V (10 s). Debounce 10 ms critical, 50 ms low. The 6.0 V floor keeps the soft critical assertion above the hardware `ENERGY_OK` maximum (5.87 V). Steady current admitted at full charge, `(8.4 − V_LOW_ASSERT)/R_src`, is 26.6 A (A), 16.5 A (B), 20.3 A (C) and 10.7 A (D): the historical 11.7 A peak is not admitted in the cold-and-aged corner.

**Hardware thresholds:** `ENERGY_OK` falls at 5.7 V (5.53–5.87 V), rises at 6.4 V, 1.0 ms fall debounce, ≥ 100 ms rise dwell. `LTC4368` `UV` 4.9 V falling, 5.15 V release (max 5.36 V); `R3` = 2.64 MΩ, `R1` = 154 kΩ, `R2` = 147 kΩ (`OV` 9.55 V). Order: soft `V_CRIT` (6.0 V) > `ENERGY_OK` max (5.87 V) > `ENERGY_OK` min (5.53 V) > `UV` release max (5.36 V) > `UV` min (4.75 V) > `V_SRC_SAFE` (4.6 V).

**Timing (E):** hard path 1.2 ms (1.1 ms detect + 25 µs gate), soft path about 25 ms; head stop 150 ms, base stop 500 ms; discharge to 3.0 V in 50 ms and to 1.0 V in 100 ms (22 Ω meets it up to 1500 µF); sign-off 60 ms; SBC halt 8–12 s (`U`), total ≤ 20 s at about 9 W (0.05 Wh).

**Hold-up:** 3.3 mF on each C2 and C3 converter input (1.68 mF minimum for 37.5 ms), with `CdVdt` about 13 nF for a 0.5 A inrush so the e-fuse does not trip during start-up; the 1 mF placeholder holds only 22 ms.

**Energy:** with these thresholds the usable load-side energy is 14.4–15.6 Wh (1.1 A) and 13.3–15.3 Wh (2.2 A) in all corners, above the ledger's 12.96 Wh; only corner D at 4.8 A falls to 8.9 Wh (loss 4.0 Wh), still 1.35× the 6.6 Wh load-side requirement (5.3 Wh × 1.25 reserve). The reserve below `V_CRIT_ASSERT` is 0.18–1.02 Wh against a 0.05 Wh shutdown.

**Values each board's comparators and dividers should use (proposals).**

| Board | Item | Value |
|---|---|---|
| `PCB-01` | none (cell-level trips fixed by the ICs: over-discharge 2.35–2.45 V per cell) | — |
| `PCB-02` | `ENERGY_OK` comparator | fall 5.7 V, rise 6.4 V, fall debounce 1.0 ms, rise dwell ≥ 100 ms |
| `PCB-02` | pack-voltage sense to C2 (ADC) | ratio for 0–9 V into 3.1 V (about 0.34), 1% resistors, RC 8 ms; accuracy target ±2% (`U`) |
| `PCB-03` | `LTC4368` `UV` falling / release | 4.9 V / 5.15 V (max 5.36 V); `R3` 2.64 MΩ, `R1`+`R2` = 154 kΩ + 147 kΩ |
| `PCB-03` | `LTC4368` `OV` rising / release | 9.55 V / 9.07 V |
| `PCB-03` | bus discharge `R_dis` | 22 Ω (≤ 31 Ω for 1500 µF); gate-off default on |
| `PCB-04` | C2 and C3 converter-input hold-up | 3.3 mF each, `CdVdt` ≈ 13 nF |
| `PCB-04` | `TPS630701` `EN` UVLO (if used) | run ≥ 2.5 V, restart ≥ 3.0 V |
| C2/C3 firmware | `V_CRIT_ASSERT/CLEAR`, `V_LOW_ASSERT/CLEAR` | 6.00/6.40, 6.50/6.90 V (D: 6.19/6.59, 6.69/7.09), formula in `brownout-restart-contract.md` §4 |
| C2/C3 firmware | debounce, dwell | 10 ms / 5 s (crit), 50 ms / 10 s (low), 3 low crossings latch "degraded" |
| C2/C3 firmware | SBC shutdown rule | request only if `E_reserve_est ≥ 0.1 Wh` |

**Consequences.** The cold-and-aged corner (159.5 mΩ) cannot admit the historical 11.7 A peak even at full charge (10.7 A limit), a design outcome to carry into `CC-PEAK-01` planning. The energy table rests on a generic NMC voltage-versus-charge curve, the largest uncertainty; it must be replaced with a measured 25R curve. The margin model assumes 9 A of load steps (`E`); measuring the real step size and source resistance at 0 °C and aged (Phase C) is what unfreezes the thresholds.

## 9. Moving yaw cable — average-to-worst-case sizing

**Scope.** The bundle that crosses the yaw joint between the body (`PCB-03/04`, Pi, yaw servo) and the head (C2, pitch and roll servos, display, camera). Layout 04 puts the yaw servo in the body, so **yaw servo power does not cross**; the pitch and roll servos, C2, the display and the sensing and link conductors do. The registered functional paths (`PA-06`) are actuator, application/safety and camera. All figures are `E` and use the registered inputs cited; the qualification test in §9.5, not this arithmetic, decides the cable.

**Inputs.** Authored yaw pose envelope ±35° (min viable) to ±50° (best) and usable mechanism travel ±40° to ±55° (`../RP-01-head/storyboard.md`, `physics.md`). Peak yaw speed need 63 rpm (about 378°/s). The body-side clock-spring reserve takes the yaw twist, and the branch drops through a Ø14 mm disc bore (`../RP-06-cad/head/layout-04/README.md`). A 1 m loop length in the ledger means 1 m of positive plus return conductor in total.

### 9.1 Load cases

| Group | Conductors | Average (attentive, gestures) | Design (credible peak) | Worst (fault, before clearing) |
|---|---|---|---|---|
| Pitch and roll power | 5 V pair from `PB-HEAD` | about 0.15 A: two servos idle at about 17–20 mA each (M181 17 mA `D`) plus small moves | 1.0 A: torque-derived 0.29 A (0.18 + 0.11) with about 3× for friction and internal acceleration (unknown per the screen) | 3.6 A: both M288 stalled at 1.80 A each (`D`), limited by the servo current limit and `PB-HEAD` protection |
| C2 feed | 5 V pair, `PB-SAFE-C2` | 0.06 A | 0.25 A with transceivers and sensors | 0.5 A supply capability (`D`, not a consumption figure); a limiter would clip at about 1 A |
| Display feed | 5 V pair, `PB-DISPLAY` | 0.30 A dimmed | 0.70 A (registered planning peak) | 1.0 A converter limit |
| Links and sideband | 2 differential UART pairs, servo-bus data and reference, `C2_READY_H`/`_L`, `E_STOP_STATUS`, `MOTOR_PRESENT`, `HEAD_OC`, `HEAD_PGOOD`, `STAT`, `INT_PB`, `KILL`, `V_PACK_ANA`, `CHG_ABSENT_3V3` and a signal ground (about 14–20 AWG28 conductors in all; idle servo current 17 mA) | mA | mA | mA |
| Camera | CSI, controlled impedance | — | — | — |

### 9.2 Conductor sizing

Fine-strand copper, 60 °C hot resistance (`R20 × 1.157`), assumed **1.0 m total loop** for the whole run from the source board to the load (0.4 m fixed + 0.6 m through the joint). Two mated connector pairs are budgeted at about 40 mV at the power-branch current (Micro-Fit+ at 5 mΩ per contact, `PCD-CON-03`, exact terminal open). The registered allowance is ≤ 150 mV from converter output to servo terminal (`power-implementation-basis.md` §5.4).

| Gauge | Hot mΩ per m of loop | Pitch + roll power: average / design / worst | C2 feed | Display feed |
|---|---:|---|---|---|
| AWG20 | 38.5 | 6 mV / 39 mV / 139 mV | — | — |
| AWG22 | 61.2 | 9 mV / **61 mV** / 220 mV | — | — |
| AWG24 | 97.4 | 15 mV / 97 mV / 351 mV | — | 29 / **68** / 97 mV |
| AWG26 | 154.8 | — | 9 / **39** / 77 mV | — |
| AWG28 | 246 | signal conductors only | | |

- **Pitch and roll power: AWG22-equivalent** (about 0.33 mm²). At the design case it drops 61 mV, leaving margin under the 110 mV left after connectors. AWG24 passes with no margin (97 mV) and is rejected. Two AWG26 in parallel per polarity is the fallback if AWG22 is too stiff (about 77 mΩ per m hot).
- **C2 feed: AWG26**, **display feed: AWG24.** Both pass the design and worst cases with margin.
- **Worst-case heating.** 3.6 A on the AWG22 pair dissipates about 0.79 W over the whole 1 m, about 0.48 W of it in the 0.6 m through the joint, for the seconds until the servo limit or protection acts. Average and design dissipation are 1 mW and 61 mW, so temperature is not the constraint; drop and flex life are.
- The worst-case drop exceeds 150 mV. That is acceptable: the registered allowance applies to `CC-06`, and stall is reported separately (`power-implementation-basis.md` §5.4).

### 9.3 Mechanical cases

| Case | Yaw excursion | Speed | Cycle count (`E`, assumption to confirm) |
|---|---|---|---|
| Average | ±15° (authored "no" and "curious" gestures reach ±13–22°) | moderate | 6 reversals/min × 4 h/day ≈ 1,440/day ≈ 0.5 M/yr, about 1.6 M over a 3-year life |
| Design | ±40° (minimum-viable usable travel) | search sweeps | 10⁵ over the life |
| Worst | ±55° (best-case usable travel) plus about 5° over-travel to the stops | 63 rpm peak (about 378°/s), hard reversals | 10⁴ hard-reversal cycles, in one campaign |

**Why the joint needs a clock spring, not a twisted bundle.** For a straight bundle of radius `r` twisted `θ` over free length `L`, the outer-conductor strain is about `ε ≈ r·θ/L`. With `r = 3 mm`:

| Yaw excursion | `ε` at L = 60 mm | `L` needed for ε ≤ 1% |
|---|---:|---:|
| ±15° | 1.3% | 79 mm |
| ±40° | 3.5% | 209 mm |
| ±55° | 4.8% | 288 mm |

A 60 mm free span cannot survive the worst case, and 288 mm is not available in the disc. The twist must be taken in bending, as the body-side clock-spring reserve already intends: for a flat conductor of thickness `t` coiled at radius `R`, `ε ≈ t/(2R)`, for example 0.33% at t = 0.1 mm and R = 15 mm. ±55° is only about 0.3 turn each side, so the reserve needs little length; its limit is the bore and the coil radius, not the angle. Keep the 1% strain target (`E`, typical flex-cable practice) as the acceptance rule until the test says otherwise.

### 9.4 Cable decisions

| Item | Direction |
|---|---|
| Power conductors | Fine-strand silicone-jacketed, AWG22 / 26 / 24 as above, wrapped as a coil, not a straight twist. igus CFROBOT is the benchmark, not the part (`PCD-CAB-03`); generic silicone stays bench-only until §9.5 passes |
| Signal conductors | AWG28 twisted pairs for the two differential UART pairs; the servo bus and sideband lines as a separate small twisted bundle so servo return never shares a signal conductor (`PA-06`) |
| Camera | CSI FFC or FPC in its own clock-spring layer with a bend radius set from the strain rule above. **Verified:** the Camera Module 3's 15-pin FFC is 16.0 mm wide and does not pass the Ø14 mm bore flat; the PCN-36 revision of the Raspberry Pi 15-to-22-pin cable is 11.5 mm wide for most of its length and passes with 1.25 mm per side, so order that revision. Bench the maximum CSI length and any flex-induced errors |
| Bore fill | Round conductors in the list above total about 12 mm² of copper-plus-jacket (roughly 19 mm² with packing) against a 154 mm² Ø14 bore, so the bore is not full; the FFC width is the constraint |
| Returns | Return conductors are as scrutinized as the positive ones (`power-implementation-basis.md` §3, item 2); shield and CSI drain are not power returns |

### 9.5 Qualification proposal

1. Build the trunk to the chosen gauge and strand count with the intended connectors, mass and routing.
2. Measure hot loop resistance before, during (at intervals) and after.
3. Cycle: 10⁶ at ±15° and 10⁵ at ±40°, then 10⁴ at ±55° plus over-travel at 378°/s, with the head powered and moving, at the 60 °C bundle temperature.
4. Run the links continuously: CSI frame errors, UART CRC counts, servo bus errors, and the `C2_READY` line, all logged against cycle count.
5. Inspect the jackets and the conductors after the test; the pass rule is ≤ 5% loop-resistance rise, no link errors attributable to the cable, and no visible wear-through.

Cycle counts, life target and the 3-year assumption are placeholders for the builder to set.

## 10. Open items

**Summary (2026-09-25).** Every board has decisions, part numbers and datasheet-derived values. What remains is of five kinds; the tables below are the detailed list, deduplicated and grouped.

| Kind | What |
|---|---|
| **Decisions** | Pi setpoint 5.10 V versus the recommended 5.15 V; the `PA-14` wording for the 43–100 µA `OFF` draw; RP-01 servo family (XC330 5 V, or STS3215 with its 8.4 V-versus-charger conflict); drive-motor SKU; CAD placement; registration of the brownout thresholds; purchase authorization |
| **Bench proofs** | `LTC3119` current and thermal; `PCB-01` trip window and recovery; charger default-mode cycle; gate SOA and latch clear; watchdog timing; power-latch boot; head-rail clamp and servo limits under stall; pack resistance cold and aged; a measured 25R voltage curve |
| **Not selected** | Audio amplifier (RP-05); small-signal parts named from memory; the comparator parts for `ENERGY_OK` and `HEAD_OC`; the DRV8874 current-limit resistor |
| **CAD** | Board volumes, main-fuse tile, rear-panel E-stop, CoM |
| **Sourcing** | No India distributor listing was confirmed for any part; several are stock-limited at TI |

**Cross-board requirements created along the way.** `SYSTEM_ARM` clears on any permit-term loss; drive-stage regeneration held to 3 A and zero below 0 °C; `C2_READY` crosses the joint as a complementary pair; `SYS` gated by adapter-present; `ENERGY_OK` above the `UV` release.

**Decision-level conflicts found in the consistency review (not resolved here).**
1. **STS3215 versus the charger:** the servo's 8.4 V maximum is below the default-mode charger's 8.455 V worst case, with no trim available (§5.4.3).
2. **`OFF` draw versus `PA-14`:** 43 µA typical and 100 µA maximum against "pack protection path only" (§4.2).
3. **Pi setpoint:** 5.10 V (registered nominal) fails the 200 mV transient allowance in the worst corner; 5.15 V passes (§5.4.2).
4. **Pack-resistance definitions differ across sections:** 57 mΩ at the pack terminals (§3.4 short-circuit current), 71.5–159.5 mΩ source cases to `VIN` (§8.1), and the ledger's 84 mΩ. They describe different points in the path but are not reconciled in one table.
5. **Gate and pack overcurrent windows overlap** (13.3–20.0 A against 17.7–25.3 A, §5.2.4), so a sustained 17.7–20 A can open the pack instead of the gate.

### 10.1 Power and protection (`PCB-01`, `PCB-03`, `PCB-04`)

| Item | Kind | Blocks |
|---|---|---|
| `LTC3119`: read the "Maximum Output Current vs Input Voltage" curve (G51) from a downloaded PDF and measure output current at 5.4 V; efficiency and temperature rise at 2 A and 3 A from 5.4–8.4 V; load step (0.4–4 A) to fix `RZ`/`CP1` (95.3 kΩ / 240 pF are computed); no-load PWM input current (PWM versus a mode pin for sleep); beat frequency with the audio front end | Bench | `PCB-03`, `PCB-04` |
| Compute setpoint: 5.10 V fails the 200 mV transient allowance in the worst corner; decide 5.15 V or remote sense; confirm the Pi's upper input limit | Decision | `PCB-04`, registration |
| Head-rail clamp (TL431 + PNP, 5.74 V, 27 Ω / 2 W): build and test for stability, dump power and threshold; measure the real regeneration power; servo internal capacitance and hot-plug at the head connector | Bench | `PCB-03` |
| `TPS259824` latch reset path on E-stop and re-arm: confirm the bus falling below the `EN/UVLO` threshold clears the latch and re-arms cleanly with the LTC4368's own latch | Bench | `PCB-03` |
| Per-axis protection (`BD-13`): verify Current Limit in Operating Mode 5 holds a stalled servo to its limit, read the Overload and Electrical Shock thresholds, confirm connector and pinout; choose the `HEAD_OC` comparator part | Bench, select | `PCB-03`, C2 firmware |
| RP-01 servo family freeze (both branches in §5.4.3); if STS3215 C046: the 8.4 V maximum conflict, a 3 A-class trunk and thicker gauge | Decision | `PCB-03` §5.4 |
| Gate: `Q_UV` leakage effect on the `UV` threshold; small-signal FET and inverter part numbers (BSS138 / AO3400A / 74LVC2G14 classes named from memory); whether a long `SHDN`-low clears the forward latch and that the 0.8 ms pulse does; gate-FET SOA at 125 °C on the real layout; real motor-bus capacitance (assumed 1000 µF) and `CGATE` re-trim; discharge resistor and time; the CGATE/RGATE connection against the LTC4368 figure; DRV8874 carrier reverse-FET drop, bulk capacitance and current-limit resistor (the Pololu page quotes both 3.5 A and 4.4 A) | Bench, select | `PCB-03` |
| Drive-stage regeneration limit ≤ 3 A and zero below 0 °C: DRV8874 current limit and C3 braking policy (hard requirement from the 4 A cell charge limit) | Requirement | `PCB-03` §5.3, RP-03 |
| Drive motor: pin the SKU (34–35:1, 8500 rpm class, 6 V); stall current (0.9 A versus 2.6 A) and shaft length (9.5 versus 10–12 mm) differ by source | Decision | `BD-02` |
| `PCB-01`: bench-measure the trip window (17.7–25.3 A predicted) with real FETs and shunt, the Zener leakage at 6.0 / 6.4 / 7.0 V, recovery from a tripped pack with the `BQ25798`, and the first-connection procedure; confirm the FET `RDSon` production spread (no datasheet minimum) | Bench | `PCB-01` schematic |
| Cells: CID/PTC and gentle-rate cycle life (not in the text found); charge and discharge temperature reading (surface versus ambient) to fix the thermal-cutoff trip; cell strap thickness, spot-welder route and the written battery procedure (`workbench.md`); `EFC4C002NL` package thickness and gate charge if the compact alternate is ever used | Select | Pack fabrication (deferred) |
| `PCB-04` low-power branches: measured `TPS630701` start-up input-limit maximum, breaker latch with the resulting `OPBUS` dip, ORing overlap with 3.3 mF on each input, `PG`/`EN` divider thresholds, display-converter inductor and ripple | Bench | `PCB-04` |
| `PB-AUDIO-OUT`: amplifier selection and the RP-05 supply items in §6.5 | Select | `PCB-04`, RP-05 |
| Hold-up terms `t_detect`, `t_inhibit`, `t_gate-open`, `t_motor-safe-confirm`, `t_local-signoff`, `t_margin`, and the source-floor `V_HIGH`/`V_LOW` for C2 and base; the 3.3 mF value is a proposal | Bench | `PCB-04`, `brownout-restart-contract.md` |
| Brownout proposals (§8.1): measured pack resistance cold and aged, real load-step size, a measured 25R OCV curve, the Pi shutdown time, registration of the thresholds; the `ENERGY_OK` divider values for 5.7 V / 6.4 V and the comparator part | Bench, decision | `PCB-02`, `PCB-03`, `PCB-04`, `brownout-restart-contract.md` |

### 10.2 Charge and system power (`PCB-02`)

| Item | Kind | Blocks |
|---|---|---|
| `BQ25798`: bench-confirm default-mode charging with `D+`/`D−` unconnected, `QON` floating and the `ILIM_HIZ` clamp of 1.08–1.38 A; the JEITA T2/T3 defaults; the charge-efficiency figure; the 103AT-2 60 °C resistance; the Würth `74437346022` saturation current; the `STL6P3LLH6` and `ESDA25P35` datasheets | Bench | `PCB-02` |
| `STUSB4500`: NVM image and read-back, adapter compatibility (9 V-only fallback), `POWER_ONLY_ABOVE_5V` behavior with real adapters | Bench | `PCB-02` |
| Latch: verify the `KILL` node during a slow C2 boot, a `PB` press in `CHARGE` (no `OPBUS`), unplug after a blocked press, and the 3 s `Q_dis` delay | Bench | `PCB-02` |
| `SYS` gate: `TPS22810` `EN/UVLO` thresholds and the `VBUS`-valid divider, the `OPBUS` bleed resistor, and confirmation that grounding the `TPS25947` OVLO pin disables it; sequencing latch on `PCB-02` (set by `PG_C2`, cleared when `OPBUS` drops) and the wiring of `PG_C2`/`PG_BASE` to RP-03 and the C2 brownout input | Bench | `PCB-02`, `PCB-04` |
| `PA-14` wording for the 43–100 µA `OFF` draw (§4.2) | Decision | Registration |

### 10.3 Watchdog and yaw joint

| Item | Kind | Blocks |
|---|---|---|
| Watchdog: ESP32-S3-Zero reset (`EN`) access on the C2 carrier (`U`); measured boot time and loop periods; the residual skipped-loop and AND-stuck-high faults; the extra `C2_READY_L` yaw-cable conductor; the permit chain's `Q_P` gate margin (it runs from the 5 V C2 branch) | Bench | §7, `PCB-03` |
| `PCB-02`/`PCB-03`: `SYSTEM_ARM` cleared on any permit-term loss (not only E-stop) | Requirement | `PCB-02`, `PCB-03` |
| Yaw cable: loop length and cycle targets; qualification run; order the PCN-36 (11.5 mm) 15→22 cable, since the 16 mm FFC does not pass the Ø14 mm bore | Bench, purchase | Head trunk, connectors |

### 10.4 CAD and sourcing

| Item | Kind | Blocks |
|---|---|---|
| Board footprints are estimates from an unlaid-out part inventory; the 2.5–2.8× footprint increase over the placeholders must be closed in CAD (`PCB-03` against the DRV carriers by 3 mm, `PCB-04` against the harness volumes, `PCB-02` against the rear-panel bosses) | CAD | RP-06 volumes |
| Main fuse is not source-adjacent if `PCB-02` sits at the rear: move the SBS Mini and ATOF holder to a pack-interface tile or onto `PCB-03` | CAD | `PA-02`, `PCB-02` |
| E-stop on the rear panel: 48 mm depth leaves 6 mm of overlap with the Pi region at Z 93–109; the Ø40 head at Z 112 overhangs the rear-panel top (Z ≈ 128) by 4 mm | CAD | RP-06 rear panel |
| CoM: the boards plus the E-stop move x from +20.6 to about +19.1 (target +25), widening the open CoM gap | CAD | TODO CoM item |
| Sourcing: no India distributor listing was confirmed for `S-8252AAC`, `bq29200`, `PSMN1R5-30YLC`, `PSMN1R0-30YLE`, `WSK2512`, `AC72ABD`, `103AT-2`, `TPS630701RNMR`, `TPS259474LRPWR`, `TPS22810DBVR`, `TPS3436CFDBEDDFRQ1` (or the `CCCBGD` fallback), the SBS Mini contacts and the ATO FLR holder (100-pack); `TPS259474L` and the watchdog are stock-limited at TI; SBS Mini crimp tool part number; fuse-holder contact resistance | Sourcing | Purchase (not authorized) |

## 11. Change log

| Date | Revision | Change |
|---|---|---|
| 2026-09-25 | v0.19 | `BA-06` updated: the CoM physics margin was re-evaluated and the CAD check re-based (`RP03-CAD-09`); registration draft `registration-draft-reg-04.md` written (not registered). |
| 2026-09-25 | v0.18 | Builder acceptances recorded (§1.1, `BA-01…09`): Pi setpoint 5.15 V, `OFF` draw, XC330 family, drive-motor target, PCN-36 cable, revised CoM baseline, bay and fuse-tile approach, brownout proposals. Registered baselines are unchanged. |
| 2026-09-25 | v0.17 | Consistency review: corrected stale values and orphan text (BD-02 wheel, BD-07 pack-trip wording, cell facts and the 4 A charge limit, ground shift 0.16 V, `PCB-01` series budget 12.7 mΩ, `bq29209/bq29200` name slip, `AAO` remnants, short-trip lower bound 37 A, gate-assist time at 8.4 V, `CB_EN` threshold, operating-switch τ 4.7 ms, 8.30 V remnants in §4.5, `ILIM_HIZ` value, permit chain C2 complementary pair and truth table, 3.1–4.0 ms delay stage, `TPS25982` versus `TPS259824ONRGE`, head clamp 5.74 V, M181 stall, STS3215 branch merged into one paragraph); merged duplicate paragraphs (secondary action, evidence, regeneration limit); removed internal workstream references; regrouped and deduplicated the open items and listed five decision-level conflicts. |
| 2026-09-25 | v0.16 | Sizing merged (from WS-H): board footprints and placement proposal, mass rows, drive-motor recommendation (34–35:1, 8500 rpm class), CSI PCN-36 cable; superseded open items removed; stale values corrected. |
| 2026-09-25 | v0.15 | Cells and pack closed (from WS-E): Samsung 25R facts (4 A max charge, 22 mΩ), `EFC3J018NUZ` rejected (±8 V operating gate limit), FETs two `PSMN1R5-30YLC`, `WSK2512` shunt, `AC72ABD` thermal cutoff, S-8252 external circuit, recomputed windows (17.7–25.3 A), SBS Mini `B02265G1` and ATOF 15 A; new hard regeneration limit (≤ 3 A, zero below 0 °C) on the drive stage. |
| 2026-09-25 | v0.14 | Brownout proposals merged (from WS-G, §8.1): `V_SRC_SAFE` 4.6 V, soft thresholds, `ENERGY_OK` 5.7/6.4 V, LTC4368 `UV` 4.9 V and `OV` 9.55 V with new divider values, hold-up 3.3 mF with `CdVdt` about 13 nF, discharge candidates, energy sensitivity. |
| 2026-09-25 | v0.13 | `LTC3119` rails closed (from WS-B1, `BD-14`): component values, protectors, thermal/current bounds, head clamp; compute setpoint finding (5.10 V fails the transient allowance; 5.15 V recommended). |
| 2026-09-25 | v0.12 | Head per-axis protection closed (from WS-C2, `BD-13`, §5.4.3): servo limits and shutdown settings, trunk latch, body-side shunt monitors, regeneration clamp; STS3215 branch carried with its 8.4 V versus charger-worst-case conflict; yaw-cable sideband list extended. |
| 2026-09-25 | v0.11 | `PCB-02` details closed (from WS-D, `BD-12`): charger straps and passives, `STUSB4500` configuration, adapter class, `LTC2954` power latch with `KILL` and adapter-present blocks, `SYS` gate with Schottky OR, pack sense and `ENERGY_OK`, `OFF` budget rebuilt (43 µA typical, 100 µA maximum). |
| 2026-09-25 | v0.10 | `PCB-04` low-power branches closed (from WS-B2, `BD-11`): `TPS630701`/`TPS259474L` per branch at 2.0 A, hold-up 1 mF placeholders, `TPS22810` `SYS` gate, sequencing latch instead of a live C2-first dependency, audio provisional spec. |
| 2026-09-25 | v0.9 | Motor gate closed (from WS-C1): FETs `PSMN1R0-30YLE`, shunt `CSS2H-2512K-3L00FE`, `SMBJ10A` TVS, permit chain values and default-on network, UV/OV divider values, re-arm pulse (§5.2.7), 1000 µF-based inrush and SOA, discharge circuit, DRV8874 carrier facts; `OFF` budget raised; `SYSTEM_ARM` clears on any permit-term loss. |
| 2026-09-25 | v0.8 | Watchdog block closed (`BD-10`): `TPS3436CFDBEDDFRQ1`, window, feed, reset, READY AND, complementary C2 pair, fresh-arm requirement, truth table (from the WS-A workstream). |
| 2026-09-25 | v0.7 | `PCB-02` I2C question resolved (`BD-09`): the `BQ25798` runs in autonomous default mode with no host. `PCB-01` protector revised to `S-8252AAC` 4.300 V + `bq29200` 4.35 V to match the default 8.4 V charge voltage (withdrawing the 8.30 V setting and `S-8252AAO`). Added the `SYS` gate, revised the `OFF` quiescent estimate to 30–40 µA, corrected the `VREG` accuracy row. |
| 2026-09-25 | v0.6 | `PCB-01` details closed (`BD-08`): `EFC3J018NUZ` FETs with a 5 mΩ sense shunt (overcurrent window 17.7–25.3 A), PNP gate-discharge assist, `CB_EN` Zener circuit, thermal cutoff in place of a comparator, recovery from an open protector via the `BQ25798` trickle mode. Found that the 8.30 V charge setting needs an I2C master that the registered charge mode does not provide. |
| 2026-09-25 | v0.5 | Motor gate sized (`BD-07`): `LTC4368-1`, 3 mΩ shunt, latch-off, E-stop through the `UV` pin (not `SHDN`), permit chain, inrush, stored-energy discharge and layer order. Corrected §5.1 accordingly. |
| 2026-09-24 | v0.4 | `PCB-01` protector decided (`BD-06`): S-8252AAO primary, bq29209 secondary and balancer, low-side FETs, discrete over-temperature cut-out. Charger regulation set to 8.30 V (4.15 V per cell). Overcharge and overdischarge requirement rows revised to the datasheet tolerances. |
| 2026-09-24 | v0.3 | Buck-boost part decided (`BD-05`): `LTC3119` on `PB-HEAD` and `PB-COMPUTE`, `TPS55288` as fallback, from both datasheets (§5.4.2). Added acceptance requirements, a head-rail clamp, a latching protector ahead of each converter and per-servo current limits. |
| 2026-09-24 | v0.2 | Head-rail headroom resolved: Murata OKL buck cannot regulate 5 V below about 6.3–6.4 V input (datasheet voltage-range graph); `PB-HEAD` and `PB-COMPUTE` move to a wide-input buck-boost; credible head load derived (0.62 A torque-derived, 2 A allowance, 5.4 A stall envelope). Added §9 moving yaw cable average-to-worst-case sizing. |
| 2026-09-24 | v0.1 | Initial per-board specification: custom PCB direction (`BD-01`), drive feed (`BD-02`), custom pack-end protection (`BD-03`), head-rail cases (`BD-04`), `PCB-01…04` and the watchdog block. Not registered. |
