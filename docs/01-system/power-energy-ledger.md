# Makad V1 Power / Energy / Thermal Ledger

| Field | Value |
|---|---|
| Status | **Living — Part-1 `CC/LP` vocabulary is registered under `RP02-P1-REG-01`, branch mapping/implementation under `RP02-P2-REG-01…03`, and compute/control identities under `RP02-P3-REG-01/02`; `LG-04`/`LG-10` envelopes refreshed from RP-03 `physics.md` as `E`/`U`. v0.15 records repeated-phrase heat duty and the 6.0 V vs 8.4 V drive note. Every numeric row remains `E`, `D`-cited or `U`. No `W` evidence exists.** |
| Version | 0.15 |
| Owner | Project builder |
| Created | 2026-09-08 |
| Last reviewed | 2026-09-18 |
| Governed by | `risk-prototype-plan.md` v1.12 §"Continuous sourcing and data workstream" (power/energy/thermal ledger deliverable) and §RP-02 (G02 invariant, G03 rehearsal) |
| Consumes | `docs/02-prototypes/RP-02-electrical/state-register.md` (states, `MD-01`); registered `docs/02-prototypes/RP-02-electrical/power-architecture.md` and `power-branch-contracts.md`; `mass-envelope-ledger.md` (battery mass row); `system-design-brief.md` §7 power/energy, thermal, internal-communication budgets |
| Feeds | RP-02 (rig sizing, G02 invariant, G03 rehearsal and `power-calculation-ledger.md`); RP-03 (drive rail); RP-06 (thermal/airflow, battery volume); ADR-06 sizing; stage-6 `engineering-budgets.md` |

This ledger is to power what `mass-envelope-ledger.md` is to mass: the single place where per-load-group current, energy and heat live, with an evidence class on every number, ranges instead of zeros for unknowns, a trip-wire that forces a design review, and a standing invariant that must be re-verified when anything changes. RP-02 creates and first populates it; every prototype that energizes anything updates it; nothing else may carry a competing budget.

**Every number in v0.1 is a planning envelope to size the RP-02 rig, not the robot's pack.** The 490 g lesson applies: an `E` value treated as a target becomes a target. These ranges exist so the trip-wire has something to evaluate and the rig has fuses of roughly the right decade — nothing more.

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
| `LG-03Y/P/R` | Head servos yaw / pitch / roll — **separately observable** | Hazardous motor / `EC-H` | `PB-HEAD-Y/P/R` via `PB-HEAD` | **Unselected.** First named paper candidate: XC330-M288-T (C01), 5 V class; paper OPEN |
| `LG-04` | Drive — two gearmotors + driver | Hazardous motor / `EC-H` | `PB-DRIVE` and `PB-DRIVE-L/R` | **Unselected** (RP-03) |
| `LG-05` | Display board (own ESP32-S3 + panel + backlight) + status light | Application / `EC-N` | `PB-DISPLAY` | SKU 30493 (selected); light unselected |
| `LG-06` | Camera | Application / `EC-N` | `PB-CAMERA`, downstream of selected SBC interface | Camera Module 3 Wide (selected) |
| `LG-07` | Microphones (4× PDM) + audio front end | Application / `EC-N` | `PB-AUDIO-IN`; source open | Unselected |
| `LG-08` | Speaker + amplifier | Application / `EC-N` | `PB-AUDIO-OUT` | Unselected |
| `LG-09` | Conversion and distribution losses | — | All `PB-*` paths | Derived: `i_in · v_in − Σ loads` |
| `LG-10` | Base MCU + safety sensing (obstacle/edge) | Safety supervision / `EC-S` | `PB-SAFE-BASE` | **C3 prototype selected:** ESP32-S3-DevKitC-1-N8; sensors, carrier and measured load remain RP-03/RP-02 inputs |

| Branch/source | Parent source | Domain | Notes |
|---|---|---|---|
| `PB-MAIN` | Battery pack through integral protection, removable isolation and main fuse | Source | Pack construction and voltage open under PA-03/04. Historical 2S, 6.0–8.4 V is an `E` planning case only. |
| `PB-CHARGE-IN` | External certified low-voltage adapter | Charge | Charger/adapter/connector unselected; AC mains remains outside Makad. |
| `PB-CHARGE-LOGIC` | Charger/load-sharing output | Charge | May feed only `PB-SAFE-C2` minimum supervision and `PB-DISPLAY` charge profile. |
| `PB-SAFE-C2` | Operating or restricted charge source through exclusive/bounded selection | Safety supervision | Own converter/protection/return; independent of display and base safety (`PA-11`). |
| `PB-SAFE-BASE` | Operating source | Safety supervision | Own converter/protection/return; off in charging (`PA-11`). |
| `PB-COMPUTE` | Operating source | Application | Own converter/failure branch (`PA-05`); registered 5.1 V nominal endpoint with 5 A interface capability for selected Raspberry Pi 5 2 GB. |
| `PB-DISPLAY` | Operating or restricted charge source | Application | Own converter/protection; independent of C2. |
| `PB-AUDIO-OUT` | Operating source | Application | Noisy/crest load separately contained. |
| `PB-CAMERA` | Selected SBC camera interface | Application | Downstream load remains separately attributable. |
| `PB-AUDIO-IN` | Operating source or compute downstream interface | Application | Source depends on RP-05 front-end selection. |
| `PB-MOTOR` | Battery through system motor-arm plus dominant E-stop | Hazardous motor | Cannot be sourced in system off, boot inhibit, hard stop or charging. |
| `PB-HEAD` / `PB-HEAD-Y/P/R` | `PB-MOTOR`, direct or converted | Hazardous motor | Voltage decided by RP-01 servo family; C01 makes regulated 5 V from a 2S planning case a leading assumption only. |
| `PB-DRIVE` / `PB-DRIVE-L/R` | `PB-MOTOR`, direct or converted | Hazardous motor | RP-03 selects and measures. |

## 3. Load-group ledger

Currents at the rail stated; power in W where the rail is open. "Transient" is the shape the rig must reproduce and the instrument must resolve.

| Code | Idle | Average working | Peak / transient | Transient character | Class | Basis | Measured by |
|---|---|---|---|---|---|---|---|
| `LG-01` SBC | 2.5–3 W | 4–8 W | 10–12 W workload estimate; **selected Pi 5 2 GB interface is registered at 5.1 V nominal / 5 A capability. Active cooler and a vent path are part of the load, and the fan is a noise source for `LG-07`.** | Sustained compute peaks under perception; USB/CSI inrush at boot; SD-card corruption on an unclean brownout makes the PA-07 soft-shutdown a requirement, not a nicety | `D` interface; `E` load | Raspberry Pi manufacturer power/voltage guidance is registered in `power-implementation-basis.md`; exact board/camera/audio workload remains unmeasured | RP-02 Phase B; RP-07 workload profiling |
| `LG-02` C2 | 0.2–0.4 W | 0.3–0.5 W | ≤ 1.5 W if Wi-Fi TX ever enabled (it should not be — wired link) | Boot inrush; negligible otherwise | `E` load; `D` input envelope | ESP32-S3 current remains an estimate until installed measurement. [Waveshare specifies 3.7–6 V external input at the 5 V pad and at least 500 mA source capability](https://docs.waveshare.com/ESP32-S3-Zero); that is a supply requirement, not measured draw. | RP-02 Phase A on the twin (note bridge current), then the Zero |
| `LG-03Y/P/R` servos | **sleep: torque off (`LP-03-OFF`, SD-02);** attentive hold 0.1–0.5 A each if gravity-loaded, lower if balanced | 0.3–0.8 A each during gestures | stall-class transient per unit at launch/reversal; **C01 XC330-M288-T eManual `D`: stall 1.80 A at 5.0 V, 1.34 A at 3.7 V, 2.15 A at 6.0 V**; operating current unmeasured | Launch/reversal/regenerative profiles | `U` (family), `D` C01 stall | RP-01 paper peaks 0.0953 / 0.0560 / 0.1099 N·m; sleep decision is not servo-family evidence | RP-01 busy-minute runs; RP-02 Phase B |
| `LG-04` drive | 0 (inhibited) | 2–8 W in motion for two small encoder gearmotors | 20–40 W for both at stall/reversal; 1.5–3 A per motor class | `LP-04-LAUNCH/REV/BRAKE`; signed regenerative current required (0.3–1.5 A class `E`, opposite polarity). Repeated `BM-06`/`BM-07` are the thermal duty, not the follow-minute RMS. Stop-on-temperature: gearbox housing 85 °C candidate / driver thermal flag, C3 inhibit. 6 V winding on 2S: 8.4 V overspeeds Ø84 past 0.70 m/s no-load — compiled clamp mandatory | `E` (class) | RP-03 `physics.md` v0.2 2026-09-18: mechanical floor 0.4–1.4 W; box heat 0.2–2.1 W at 40–70 % η; spin/wiggle are the rise. JGA25-class D02 is a **reference unit, not a freeze**. Korad 5 A: Phase B stall/reversal is **per-motor**; both-motor composites wait Phase C. NFP ≤3 A at 6 V scales to ≤4.2 A at 8.4 V | RP-03; substitute profile in RP-02 until then |
| `LG-05` display + light | 1–1.5 W (dimmed idle, `E`) | **2.25 W published board consumption (`D`)**; 1.5–3 W profile range retained | 3–3.5 W full-reference planning range (`E`) | Backlight step at wake; source-transfer/boot transient unmeasured | `D` board nominal; `E/U` profiles/light | [Waveshare documents selected SKU 30493 as Type-C 5 V, 450 mA and 0–65 °C](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3); status light and brightness/FPS profiles remain open. | RP-02 Phase A when the sample arrives |
| `LG-06` camera | 0.1–0.3 W (streaming idle) | 0.3–1.0 W | ≤ 1.5 W (autofocus actuator + full-rate capture) | AF motor steps; small | `U`; `E` range | No official power figure; community CM3 measurements 200–300 mA at 3.3 V | RP-02 Phase B on selected Raspberry Pi 5 2 GB |
| `LG-07` mics + front end | < 0.05 W | < 0.1 W | < 0.2 W (codec HAT) or ≤ 1 W (XMOS-class USB array with onboard DSP) | None material | `E` | PDM MEMS ≈ 1 mA each; codec/front end dominates. **A Pi-class SBC needs a 4-channel front end (2026-09-14 review); a USB-array option moves ~0.5–1 W onto `PB-COMPUTE` through the SBC's USB rail** | RP-05 |
| `LG-08` speaker + amp | 0.1–0.3 W (amp idle) | 0.5–1.5 W (chirps, speech-level music) | 3–5 W electrical at registered peak level | `LP-08-MUSIC` RMS plus separate `LP-08-CREST` transients | `U`; `E` range | Small class-D amp + 3 W speaker class | RP-05/RP-06; RP-02 Phase B with a candidate |
| `LG-09` losses | 10–15 % of load | 10–15 % | 15–20 % at peak (buck efficiency falls at high current) | Follows load | `E` | Typical buck-module efficiency 85–92 % at these currents | Derived from `i_in · v_in` minus Σ `W` rows |
| `LG-10` base MCU + safety sensing | 0.25–0.50 W | 0.4–0.8 W | ≤ 1.0 W if emitters pulsed; ≤ 1.2 W if ToF+IR continuous (flag) | Sensor emitter pulses | `U` | RP-03 `physics.md` / `sensing-screen-01.md`: C3 N8 + GPIO cliff + analog IR + SPI IMU. No `W`. Sensing SKU unselected | RP-03 |

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
- The former 25% additive-reserve/80% usable-depth example gives 8.28 Wh only with lossless conversion. Including the present 85–95% system-efficiency sensitivity gives **8.72–9.74 Wh** from the 5.3 Wh high case. This is corrected and derived in `../02-prototypes/RP-02-electrical/power-calculation-ledger.md`; it is not a pack selection.
- Servo and drive transients remain the largest unknowns. C01's 1.80 A at 5 V is stall `D`, not an operating profile; three-axis stall coincidence is stress/reference only.

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
- [ ] Servo family (RP-01) → servo rail voltage; per-unit stall/hold `D`; then `W` from the RP-01 busy-minute runs. C01 stall `D` is now cited; family freeze still required to collapse the rail.
- [x] Select SBC and register its input interface — Raspberry Pi 5 2 GB, `RP02-P2-REG-02`, 2026-09-16.
- [ ] Measure selected Raspberry Pi 5 2 GB as `W` under the RP-07 workload, including camera/audio peripherals, active cooler, boot and shutdown.
- [ ] Display sample → `W` idle/average/peak on the RP-02 rig.
- [ ] Pack-assembly internal resistance `D` for each candidate construction; `W` at `PB-MAIN` in Phase C.
- [ ] Register per-component undervoltage limits so the invariant's "rail excursion" term is testable.
- [ ] Drive `W` profiles from RP-03; until then `CC-09/09C/09R/10A/10B/10C/11/PEAK`, `CC-12C`, and the drive portion of `ST-01` use an explicit substitute record.
- [ ] Retire `LG-09` as a lump once per-branch `W` rows allow the residual to be attributed.

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
