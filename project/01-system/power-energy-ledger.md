# Makad V1 Power / Energy / Thermal Ledger

> **Peak budget HOLD (D-096, 2026-11-07).** The [harness](../03-build/05-harness/README.md#6-electrical-and-mass-estimates) screens about **16 A coincident demand** at low pack. This is not an accepted peak budget. N1–N3 and servo current limits must be measured; M6 shunt full-scale remains CH-099 OPEN. The load-energy estimate below remains a planning screen.

| Field | Value |
|---|---|
| Status | **Living — D-093/D-096 build topology applied. Energy remains a `D/E` planning screen; peak current is HOLD pending N1–N3 and CH-099. No `W` evidence exists.** |
| Version | 0.16 |
| Owner | Project builder |
| Created | 2026-09-08 |
| Last reviewed | 2026-11-07 |
| Governed by | `risk-prototype-plan.md` v1.12 §"Continuous sourcing and data workstream" (power/energy/thermal ledger deliverable) and §RP-02 (G02 invariant, G03 rehearsal) |
| Consumes | `../02-prototypes/RP-02-electrical/state-register.md` (`MD-01` duty recipe only); [D-093](../03-build/decisions.md#d-093), [D-096](../03-build/decisions.md#d-096) and the [build harness](../03-build/05-harness/README.md); `mass-envelope-ledger.md` (battery mass row) |
| Feeds | RP-02 (rig sizing, G02 invariant, G03 rehearsal and `power-calculation-ledger.md`); RP-03 (drive rail); RP-06 (thermal/airflow, battery volume); ADR-06 sizing |

This ledger is to power what `mass-envelope-ledger.md` is to mass: the place where per-load-group current, energy and heat live, with evidence classes and ranges for unknowns. RP-02 supplied the historical duty recipe; the D-093/D-096 build tree below governs the present hardware. Each energized prototype updates the measured rows.

**Load numbers are planning envelopes, not accepted pack or component limits.** The 490 g lesson applies: an `E` value treated as a target becomes a target.

## 1. Evidence classes

Identical to `payload-mass-capture.md`:

- `W` — measured on the bench in the exact recorded state, with a run ID.
- `D` — manufacturer datasheet or official documentation value; planning only.
- `E` — estimate from calculation, class analogy or a characterized substitute (substitute named); planning only, as a range.
- `U` — unknown or unselected; an open non-zero item, never entered as zero.

A row sourced from a substitute load is `E` even if it was measured. Only `W` rows from real hardware feed ADR-06 sizing.

## 2. Load groups and rails

Load-group codes are defined here once; `state-register.md`, `rig.md` and run-record channels reference them.

| Code | Load group | Domain (`PA-01`) | Registered branch | Selected hardware |
|---|---|---|---|---|
| `LG-01` | Main compute — Linux SBC | Application / `EC-C` | `PB-COMPUTE` | **Selected 2026-09-16:** Raspberry Pi 5 2 GB plus official Active Cooler; purchase, storage, input hardware, enclosure cooling/acoustics and workload measurement remain open |
| `LG-02` | Head motion controller C2 + servo-bus transceiver | Safety supervision / `EC-S` | `PB-SAFE-C2` | Waveshare ESP32-S3-Zero (selected); DevKitC-1 twin on the bench |
| `LG-03Y/P/R` | Head servos yaw / pitch / roll — separately observable | Hazardous motor / `EC-H` | `PB-HEAD-Y` and `PB-HEAD-P/R` | ST3215-HS yaw on M3 11.1 V; 2 × STS3045M pitch/roll on M2 5.5 V ([D-047](../03-build/decisions.md#d-047) as amended by D-093 Q8, [D-049](../03-build/decisions.md#d-049)); physical limits open |
| `LG-04` | Drive — two gearmotors + drivers | Hazardous motor / `EC-H` | `PB-DRIVE-L/R` | 2 × MOT3001 with Adafruit #3297 DRV8833 ([D-003](../03-build/decisions.md#d-003)) |
| `LG-05` | Display board (own ESP32-S3 + panel + backlight) + status light | Application / `EC-N` | `PB-DISPLAY` | SKU 30493 (selected); light unselected |
| `LG-06` | Camera | Application / `EC-N` | `PB-CAMERA`, downstream of selected SBC interface | Camera Module 3 Wide (selected) |
| `LG-07` | Four I²S microphones + audio hub | Application / `EC-N` | `PB-AUDIO-IN` from Pi 3V3 | 4 × INMP441 breakouts (M9), front pair SDI0 and rear pair SDI1 through audio hub |
| `LG-08` | Speaker + amplifier | Application / `EC-N` | `PB-AUDIO-OUT` from M5 | MAX98357A breakout (M8, BO-007 promoted) |
| `LG-09` | Conversion and distribution losses | — | All `PB-*` paths | Derived: `i_in · v_in − Σ loads` |
| `LG-10` | Base MCU + safety sensing (obstacle/edge) | Safety supervision / `EC-S` | `PB-SAFE-BASE` | C3 ESP32-S3-DevKitC-1-N8 on PCB-10, fed by M5 through W11 Schottky; sensors and measured load remain open |

| Branch/source | Parent source | Domain | Notes |
|---|---|---|---|
| `PB-MAIN` | 2S1P Samsung 25R pack → TIFPS0629 → 15 A fuse → J-PK | Source | D-026/D-019; ~18 Wh nominal, 6.0–8.4 V operating screen. External 2S balance charging through rear XT30 and XH ports only with robot OFF. |
| `PB-CHARGE-IN` | **Retired by D-093** | Historical charge | No onboard charger input branch. |
| `PB-CHARGE-LOGIC` | **Retired by D-093** | Historical charge | No load-sharing or charge-powered branch. |
| `PB-SWITCHED` | `PB-MAIN` → M1 #2813 HP pushbutton switch → M6 INA226 shunt → positive/negative stars | Switched source | [D-096 harness](../03-build/05-harness/README.md); N1 and CH-099 open. |
| `PB-SAFE-C2` | `PB-SWITCHED` → shared M5 S13V30F5 5 V | Safety supervision | Same M5 source as C3, display and amp; no independent protection. |
| `PB-SAFE-BASE` | `PB-SWITCHED` → shared M5 → W11 Schottky → C3 on PCB-10 | Safety supervision | N8 checks voltage and USB back-feed. |
| `PB-COMPUTE` | `PB-SWITCHED` → M4 S13V30F5 | Application | **5.0 V** Pi rail; N12 gates acceptance at the Pi. Pi under-voltage flag spans about 4.63–4.86 V. |
| `PB-DISPLAY` | `PB-SWITCHED` → shared M5 | Application | No independent converter/protection. |
| `PB-AUDIO-OUT` | `PB-SWITCHED` → shared M5 | Application | MAX98357A breakout; crest and shared-rail startup tested at N2. |
| `PB-CAMERA` | Selected SBC camera interface | Application | Downstream load remains separately attributable. |
| `PB-AUDIO-IN` | Pi 3V3 through audio hub | Application | Four M9 I²S breakouts on SDI0/SDI1. |
| `PB-MOTOR` | `PB-SWITCHED` | Hazardous motor | No arm latch or E-stop. PCB-10 watchdog + AND gate controls DRV8833 `nSLEEP`; D-041 mushroom drives M1. |
| `PB-HEAD-P/R` | `PB-SWITCHED` → M2 S18V20ALV 5.5 V | Hazardous motor | Pitch/roll STS3045M; current limit and N2 capacity open. |
| `PB-HEAD-Y` | `PB-SWITCHED` → M3 S18V20ALV 11.1 V → PCB-08 → W15 | Hazardous motor | ST3215-HS; current set below measured module capability and N3 requires <12.6 V at servo terminals on hard stop. |
| `PB-DRIVE-L/R` | Directly from `PB-SWITCHED` | Hazardous motor | Each #3297 `VM` has SMBJ8.5A + 100 µF + 0.1 µF; N4 screens regen. |

## 3. Load-group ledger

Currents at the rail stated; power in W where the rail is open. "Transient" is the shape the rig must reproduce and the instrument must resolve.

| Code | Idle | Average working | Peak / transient | Transient character | Class | Basis | Measured by |
|---|---|---|---|---|---|---|---|
| `LG-01` SBC | 2.5–3 W | 4–8 W | 10–12 W workload estimate; M4 is a **5.0 V** supply, accepted only after N12 | Sustained compute peaks under perception; USB/CSI inrush; firmware orderly shutdown before pack trip | `D` interface; `E` load | Pi 5 2 GB and active cooler; exact workload unmeasured; [N12](../03-build/simplification-plan.md#412-tests) verifies ≥4.80 V at Pi | RP-07 workload profiling and N12 |
| `LG-02` C2 | 0.2–0.4 W | 0.3–0.5 W | ≤ 1.5 W if Wi-Fi TX ever enabled (it should not be — wired link) | Boot inrush; negligible otherwise | `E` load; `D` input envelope | ESP32-S3 current remains an estimate until installed measurement. [Waveshare specifies 3.7–6 V external input at the 5 V pad and at least 500 mA source capability](https://docs.waveshare.com/ESP32-S3-Zero); that is a supply requirement, not measured draw. | RP-02 Phase A on the twin (note bridge current), then the Zero |
| `LG-03Y/P/R` servos | Sleep: torque off; attentive hold estimate 0.1–0.5 A each | 0.3–0.8 A each during gestures (`E`) | Stall/reversal transient; **coincident peak HOLD** pending measured Feetech limits and N2/N3 | Launch/reversal/regenerative profiles | `E/U` | 2 × STS3045M at 5.5 V; ST3215-HS at 11.1 V; no installed current profile yet | N2/N3 and busy-minute runs |
| `LG-04` drive | 0 (inhibited) | 2–8 W in motion for two selected MOT3001 gearmotors (`E`) | Stall/reversal transient; **coincident switched-bus peak HOLD** (D-096) | Launch/reversal/brake and signed regeneration; measure N4 with both #3297 boards | `E/U` working envelope | 2 × selected MOT3001 with Adafruit #3297 DRV8833 (D-003); the older JGA25/NFP class screen is historical. | RP-03/N4 and D-096 N1 |
| `LG-05` display + light | 1–1.5 W (dimmed idle, `E`) | **2.25 W published board consumption (`D`)**; 1.5–3 W profile range retained | 3–3.5 W full-reference planning range (`E`) | Backlight step at wake; source-transfer/boot transient unmeasured | `D` board nominal; `E/U` profiles/light | [Waveshare documents selected SKU 30493 as Type-C 5 V, 450 mA and 0–65 °C](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3); status light and brightness/FPS profiles remain open. | RP-02 Phase A when the sample arrives |
| `LG-06` camera | 0.1–0.3 W (streaming idle) | 0.3–1.0 W | ≤ 1.5 W (autofocus actuator + full-rate capture) | AF motor steps; small | `U`; `E` range | No official power figure; community CM3 measurements 200–300 mA at 3.3 V | RP-02 Phase B on selected Raspberry Pi 5 2 GB |
| `LG-07` four INMP441 I²S breakouts + hub | <0.05 W | <0.1 W | <0.2 W (`E` screen) | Clock and capture activity | `E/U` | Pi 3V3 supplies M9 ×4; actual board draw and audio-hub loss unmeasured | N9/N11 |
| `LG-08` speaker + MAX98357A breakout | 0.1–0.3 W | 0.5–1.5 W | 3–5 W electrical at registered peak level | `LP-08-MUSIC` RMS plus separate `LP-08-CREST` transients | `E` range | M8 on shared M5 5 V; measure with actual speaker/duty | N2/N9 |
| `LG-09` conversion and distribution losses | Rail-specific | Rail-specific | **Peak HOLD** | Follows each rail and current through M1/M6 | `D/E/U` | See efficiency and I²R method below; no generic buck percentage | N1–N3 and input/output power logs |
| `LG-10` base MCU + safety sensing | 0.25–0.50 W | 0.4–0.8 W | ≤ 1.0 W if emitters pulsed; ≤ 1.2 W if ToF+IR continuous (flag) | Sensor emitter pulses | `U` | RP-03 `physics.md` / `sensing-screen-01.md`: C3 N8 + GPIO cliff + analog IR + SPI IMU. No `W`. Sensing SKU unselected | RP-03 |

### OFF draw and shelf screen

With M1 OFF, only the TIFPS0629 pack-protection electronics and M1 receive pack power. Pololu publishes **<0.2 µA** OFF for the #2813 HP ([manufacturer comparison](https://www.pololu.com/product/2813)); the TIFPS0629 seller publishes no quiescent-current specification, so its draw is `U`, **not a datasheet value**. The existing [PCB-01 acceptance](../03-build/04-pcbs/power-boards.md#3-pcb-01--tifps0629-acceptance-before-cells-are-connected) requires ≤16 µA from the cells. N1(d) measures the assembled OFF current, including the protection board.

At the **16 µA acceptance ceiling plus 0.2 µA M1**, a nominal full 2.5 Ah 25R pack has 2.5 Ah / 0.0162 mA ≈ **6,430 days** of *electronics-only* drain. At a measured 50 µA protection-board draw, the same arithmetic gives ≈2,075 days. Neither is a storage-life claim: cell self-discharge, imbalance, temperature and protection trip dominate long before then. Record measured OFF current and set a practical storage/recharge interval from pack tests.

### LG-09 conversion and series losses

For each `MD-01` interval, use `P_in = P_5V,M4/η_S13 + P_5V,M5/η_S13 + P_5.5V,M2/η_S18 + P_11.1V,M3/η_S18 + P_drive`; sum `P_out(1/η−1)` as conversion heat. Pololu's [S13V30F5 curves](https://www.pololu.com/product/4082) span **85–95% typical** across input and load, and its [S18V20ALV curves](https://www.pololu.com/product/2572) span **80–90% typical**. The published graphs do not identify Makad's as-built average rail currents, so **6.0, 7.4 and 8.4 V point efficiencies remain `U`** until each rail's average load is measured; do not manufacture a point estimate from the family range. At each of those three inputs, log M4/M5 and M2/M3 input/output power at the measured `MD-01` average, then read/interpolate the corresponding curve and replace `U` with `W`.

Series loss is additional: `P_M1 = I_bus² R_M1(V)` and `P_M6 = I_bus² R_shunt`, with harness/contact loss measured separately. Pololu publishes **13 mΩ at 4.5 V and 8.6 mΩ at 10 V** for M1 HP ([#2813 comparison](https://www.pololu.com/product/2813)); interpolation gives about 11.8/10.7/9.9 mΩ at 6.0/7.4/8.4 V (`E`, temperature dependent). An R010 M6 would add 10 mΩ, but **CH-099 shunt full-scale is OPEN**; this resistance is a scenario, not the selected design. At 1 A bus current these two scenario losses are about 22/21/20 mW; actual loss scales with the interval's mean-square current and must be logged at N1.

## 4. Qualification-case energy model — planning envelope

The state model now separates modes (`OM`), behaviours (`BS`), events (`EV`), qualification cases (`CC`) and synthetic stress (`ST`). Named profiles live in `RP-02-electrical/load-model.md`. The case/profile vocabulary is registered under `RP02-P1-REG-01`, but this remains a coarse `E` numeric envelope and no row is `W`. In this issue, §4 power/energy is the sum at load terminals and excludes `LG-09`; source and nominal-pack transformations apply efficiency exactly once in `power-calculation-ledger.md`.

| State | Composition (dominant groups) | Power range (W) | `MD-01` duration | Energy range (Wh) |
|---|---|---|---|---|
| `CC-01` boot/inhibit | Board inrush/startup; motors off | `U/E` | 20 s | ~0.05–0.11 |
| `CC-02F/T` quiet idle | SBC wake listening + dim face + health; camera off and head torque off; tabletop variant additionally verifies drive inhibit | 4–8 | 5 min | 0.33–0.67 |
| `BS-02/04 + CC-05` attentive/social | Camera/display/listening + sparse gestures | 7–14 baseline | 6 min 25 s + events | ~0.75–1.55 |
| `CC-03/04` wake/search/acquire | Head motion + display/chirp + perception/camera | 10–45 profile-dependent | 50 s sequence | ~0.10–0.25 |
| `CC-07A/B/C` request phases | Capture, service wait and response are sequential | 7–18 by phase | 1 min | 0.12–0.30 |
| `CC-08` music | Audio RMS/crests + eye animation + capture + small head motion | 8–16 | 3 min | 0.40–0.80 |
| `CC-09/09C/09R/10A/10B/10C` come/follow | Drive + tracking + head correction + safety; includes stopping-band, continuity and obstacle interventions | 15–30 | 3 min | 0.75–1.50 |
| `CC-11` spin/settle | Short drive peak inside complete action | 30–50 during peak | 15 s action | ~0.04–0.12 |
| `CC-16 / EV-14` shutdown | Descent, sign-off and log flush | 5–10 | 10 s | ~0.02 |
| **Registered `MD-01` v0.2** | Chronological recipe in state register | **average `E` ≈7.8–15.9 W** | **20 min** | **`E` ≈2.6–5.3 Wh** |
| **`CC-PEAK-01` credible peak** | Drive reversal/brake + tracking/camera + ordinary head correction + audio crest + face/safety | `U`; rebuild from aligned profiles | transient | — |
| **`ST-01` synthetic stress** | Aligns startle, drive reversal, audio crest, display transition and perception | Historical `E` ≈40–70 W pending rebuild | transient | — |

Consequences already visible from the envelope, all `E`:

- Historical `ST-01` could exceed the **Korad KA3005D's 5 A** at 2S. Phase B records the largest safe vector; full alignment waits on a protected suitable source.
- **D-093/D-096 runtime recheck:** `MD-01` remains ~2.6–5.3 Wh **at loads** for 20 min. Conservatively putting all loads through the published Pololu efficiency envelope (80–95%; actual drive bypasses converters) gives **~2.74–6.63 Wh from the pack**, before M1/M6/wire losses. At 2S1P 25R ~18 Wh nominal and the earlier illustrative 80% usable-depth assumption, **14.4 Wh** is available. The high case uses ~46% of that energy. Retaining the earlier 25% additive reserve gives a **~8.28 Wh** high-case planning requirement, leaving ~6.12 Wh margin against 14.4 Wh. The 20-minute verdict therefore remains positive **on paper**, conditional on measured duty, low-voltage cutoff, converter points and pack energy; the reserve itself is not an approved target. The prior 85–95% sensitivity omitted the S18V20's 80–90% range and the Pi now runs from M4 at 5.0 V.
- Servo and drive transients remain the largest unknowns. The [D-096](../03-build/decisions.md#d-096) ~16 A low-pack screen is a HOLD, not an accepted peak. Do not enter a coincident-current total until N1/N2/N3, servo protection limits and CH-099 shunt full-scale are measured.

## 5. Coexistence invariant (the reshaped RP02-G02)

> Every registered state in `state-register.md` completes without unintended reset, unsafe motion, rail excursion outside registered component limits, data corruption, or thermal-limit violation.

**Re-run rule.** The invariant must be re-verified, and the verification recorded in `RP-02-electrical/decision.md` with run IDs, whenever any of the following occurs:

1. a load-group row changes evidence class (`U`→`E`, `E`→`W`, or a `W` value changes by more than its stated uncertainty);
2. a load group is added or a substitute is replaced by real hardware;
3. the servo rail voltage or the pack configuration changes;
4. a mode/state/event/case/profile is registered or revised, or `MD-01` is re-versioned;
5. any conductor, connector or fuse on the tree changes.

The record names which states were verified with which loads, which remain pending, and when the next re-run is due. "Verified in September on bench loads" is not verification in November with drive motors.

## 6. Trip-wire

Evaluated at every ledger revision; a trip forces a **mandatory design review** recorded in `MEMORY.md`, not a silent range adjustment.

| Trip | Condition | Review must consider |
|---|---|---|
| **T-1 Energy** | `E_MD01,high / (usable DoD · η_conv) · (1 + reserve)` exceeds the usable energy of the *largest* pack that fits the mass row's high bound (500 g) and the low-and-forward placement | Servo class, head mass, `MD-01` composition honesty, runtime target (CON-10 may rise, never fall) |
| **T-2 Peak** | `CC-PEAK-01` exceeds source capability, or servo-terminal drop during `CC-06` exceeds PA-06 with the largest credible flex conductor | Servo/drive family, capacitance, flex life versus gauge, pack P-count |
| **T-3 Thermal** | Regulator dissipation under `CC-08/09` and `MD-01` exceeds passive capability at SC-TBD-12 | Converter, RP-06 airflow, duty |
| **T-4 Compute rail** | SBC rail during `CC-06/CC-PEAK-01/ST-01` falls within 0.25 V of its undervoltage threshold | PA-05 separation, transient response, capacitance |

## 7. Open items

- [ ] Replace every `E`-class datasheet reference in §3 with a cited `D` row (Espressif, Waveshare, ROBOTIS, SBC vendor) — one afternoon, no purchase.
- [x] Register the `OM/EN/BS/PC/AL/HL/EV/CC/LP` set and `MD-01` definition — `RP02-P1-REG-01`, 2026-09-15.
- [ ] Recompute §4 from run-bound profiles once the required real loads or admissible substitutes are frozen; registration did not convert `U/E/D` values into `W` evidence.
- [ ] Measure the selected Feetech servo hold, busy-minute and protection-limit currents on M2/M3 (N2/N3), then replace the `E/U` row.
- [x] Select SBC and register its input interface — Raspberry Pi 5 2 GB, `RP02-P2-REG-02`, 2026-09-16.
- [ ] Measure selected Raspberry Pi 5 2 GB as `W` under the RP-07 workload, including camera/audio peripherals, active cooler, boot and shutdown.
- [ ] Display sample → `W` idle/average/peak on the RP-02 rig.
- [ ] Pack-assembly internal resistance `D` for each candidate construction; `W` at `PB-MAIN` in Phase C.
- [ ] Register per-component undervoltage limits so the invariant's "rail excursion" term is testable.
- [ ] Drive `W` profiles from RP-03; until then `CC-09/09C/09R/10A/10B/10C/11/PEAK`, `CC-12C`, and the drive portion of `ST-01` use an explicit substitute record.
- [ ] Measure each rail's average input/output power at 6.0, 7.4 and 8.4 V; replace the `U` efficiency points and attribute `LG-09` per branch.
- [ ] Close D-096 electrical HOLD: N1–N3 coincident demand, servo limits, CH-099 M6 shunt full-scale and body-lift harness ratings before accepting a peak budget.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-08 | 0.1 | Created under plan v1.10 as the canonical power/energy/thermal budget. Defined load groups `LG-01…LG-10` and rails, entered planning envelopes (`E`/`U`) for every group, computed an illustrative `MD-01` energy and composite-peak envelope, and adopted the coexistence invariant with its re-run rule and four trip-wires. No `W` evidence; no selection. |
| 2026-09-12 | 0.2 | Corrected proposed MD-01 to exactly 20 minutes by extending S03 to 8 min 34 s; recomputed the planning energy to ~2.8–5.3 Wh and top-of-range pack requirement to ~8.3 Wh. Clarified that S13 covers transient concurrency, not sustained/state-specific verification. No state or threshold registered. |
| 2026-09-13 | 0.3 | Consumed RP-01 C01 paper screen (XC330-M288-T): cited eManual stall `D` 1.80 A at 5.0 V; recorded Layout 03 paper peaks; 5 V regulated-from-2S is the leading rail working assumption. Family remains unselected; no `W` row. |
| 2026-09-14 | 0.4 | Component review (MEM-20260914-01): noted Raspberry Pi 5 2 GB as the suggested, unselected `LG-01` candidate with its 5 V / 5 A, thermal, fan-noise and clean-shutdown consequences; widened the `LG-07` peak for a USB-array front end. No class change, no `W` row, no selection. |
| 2026-09-14 | 0.5 | Adopted the refactored Part-1 state/load vocabulary: modes/behaviours/events, named profiles, credible `CC-PEAK-01` versus synthetic `ST-01`, and chronological `MD-01` v0.2. Re-keyed the illustrative model without creating `W` evidence or registering a case/profile. |
| 2026-09-15 | 0.6 | Reconciled the energy model with the complete foundation/system situation audit: distinguished come, follow, target-continuity and obstacle cases; named `CC-16` as the shutdown case; and added `PC`, per-action `AL` and `HL` to the registration dependency. The numerical envelope is unchanged and remains `E`; no case/profile is registered. |
| 2026-09-15 | 0.7 | Recorded `RP02-P1-REG-01`: the state/case/profile vocabulary and `MD-01` definition are now the approved baseline. Planning numbers retain their existing evidence classes; no numeric value was promoted to `W`, and the ledger must still be recomputed after run-specific load binding. |
| 2026-09-16 | 0.8 | Consumed `RP02-P2-REG-01`: mapped every `LG` to the registered `PB-*` topology and replaced the former generic rail table with physical source/branch paths. Numerical envelopes and evidence classes are unchanged. |
| 2026-09-16 | 0.9 | Added manufacturer-backed input evidence for C2 and selected display while drafting the power implementation basis. Promoted only the published display 5 V/450 mA nominal point to `D`; load-profile ranges remain `E/U` and no component rating or gate changed. |
| 2026-09-16 | 0.10 | Consumed `RP02-P2-REG-02`: selected Raspberry Pi 5 2 GB as `LG-01`, registered its 5.1 V nominal/5 A-capable `PB-COMPUTE` interface, and retained all workload values as `E` pending exact-hardware `W` runs. Selection is not purchase authorization. |
| 2026-09-16 | 0.11 | Added the derived `power-calculation-ledger.md` feed and corrected the high `MD-01` nominal-pack sensitivity: 8.28 Wh is the lossless-conversion result; including 85–95% efficiency yields 8.72–9.74 Wh. Also corrected the displayed low-case average from 7.7 W to 7.8 W. No load input, pack selection, evidence class or gate changed. |
| 2026-09-16 | 0.12 | Consumed `RP02-P3-REG-01`: recorded the selected official Pi 5 Active Cooler and ESP32-S3-DevKitC-1-N8R8 C3 prototype identity. Numeric envelopes remain `E/U`; sensors, storage, carriers, purchases and all `W` evidence remain open. |
| 2026-09-16 | 0.13 | Consumed `RP02-P3-REG-02`: corrected the C3 prototype suffix to N8 to preserve GPIO35–37. No numeric envelope or evidence class changed. |
| 2026-09-17 | 0.14 | Consumed RP-03 `physics.md` (`RP03-P2-REG-01`): refreshed `LG-04` average to 2–8 W and recorded signed regen 0.3–1.5 A class plus the Korad 5 A per-motor Phase B rule; widened `LG-10` idle/average slightly and flagged continuous-emitter peak. Class remains `E`/`U`. No `W` row, no motor freeze, no purchase. |
| 2026-09-18 | 0.15 | Consumed RP-03 `physics.md` v0.2 (`RP03-P2-REG-02`): recorded repeated-phrase heat duty (spin/wiggle, not follow-minute RMS), stop-on-temperature inhibit, and the 6.0 V vs 8.4 V drive note (6 V winding overspeeds at 8.4 V; NFP stall current scales). `LG-04` 2–8 W band **unchanged**. No `W` row, no motor freeze, no purchase. |
| 2026-11-07 | 0.16 | Applied D-093/D-096 load groups and switched-bus tree; retired charge branches; added OFF and rail-loss screens; rechecked 20-minute `MD-01` against ~18 Wh nominal 25R pack. Peak-current acceptance remains HOLD pending N1–N3 and CH-099. No `W` evidence added. |
