# Makad V1 Power / Energy / Thermal Ledger

| Field | Value |
|---|---|
| Status | **Living — Part-1 `CC/LP` vocabulary registered under `RP02-P1-REG-01`; every numeric row remains `E`, `D`-cited or `U`. No `W` evidence exists.** |
| Version | 0.7 |
| Owner | Project builder |
| Created | 2026-09-08 |
| Last reviewed | 2026-09-15 |
| Governed by | `risk-prototype-plan.md` v1.12 §"Continuous sourcing and data workstream" (power/energy/thermal ledger deliverable) and §RP-02 (G02 invariant, G03 rehearsal) |
| Consumes | `docs/02-prototypes/RP-02-electrical/state-register.md` (states, `MD-01`); `docs/02-prototypes/RP-02-electrical/power-architecture.md` (rails); `mass-envelope-ledger.md` (battery mass row); `system-design-brief.md` §7 power/energy, thermal, internal-communication budgets |
| Feeds | RP-02 (rig sizing, G02 invariant, G03 rehearsal); RP-03 (drive rail); RP-06 (thermal/airflow, battery volume); ADR-06 sizing; stage-6 `engineering-budgets.md` |

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

| Code | Load group | Domain (PA-01) | Rail | Selected hardware |
|---|---|---|---|---|
| `LG-01` | Main compute — Linux SBC | Logic | Buck A, 5 V | **Unselected.** Suggested lead candidate from the 2026-09-14 review: Raspberry Pi 5 2 GB (5 V / 5 A class); Pi 4 class cost-dominated |
| `LG-02` | Head motion controller C2 + servo-bus transceiver | Logic | Buck B, 5 V → on-board 3.3 V | Waveshare ESP32-S3-Zero (selected); DevKitC-1 twin on the bench |
| `LG-03Y/P/R` | Head servos yaw / pitch / roll — **separately observable** | Motor | Servo rail (voltage per PA-04) | **Unselected.** First named paper candidate: XC330-M288-T (C01), 5 V class; paper OPEN |
| `LG-04` | Drive — two gearmotors + driver | Motor | Drive rail | **Unselected** (RP-03) |
| `LG-05` | Display board (own ESP32-S3 + panel + backlight) + status light | Logic | Buck B, 5 V | SKU 30493 (selected); light unselected |
| `LG-06` | Camera | Logic | via SBC camera connector | Camera Module 3 Wide (selected) |
| `LG-07` | Microphones (4× PDM) + audio front end | Logic | Buck A or SBC 3.3 V | Unselected |
| `LG-08` | Speaker + amplifier | Logic (hazard-free) | Audio rail | Unselected |
| `LG-09` | Conversion and distribution losses | — | All | Derived: `i_in · v_in − Σ loads` |
| `LG-10` | Base MCU + safety sensing (obstacle/edge) | Logic | Buck B or own | Unselected (RP-03) |

| Rail | Source | Domain | Notes |
|---|---|---|---|
| Pack | Battery, chemistry and S-count open (PA-03/04) | — | Working assumption for rig design: 2S, 6.0–8.4 V |
| Buck A — compute 5 V | Pack | Logic | Own converter, never shared with the motor domain (PA-05) |
| Buck B — head-logic 5 V | Pack | Logic | Crosses the yaw boundary on the head-logic branch |
| Audio rail | Pack or Buck A | Logic | Noisy load kept off the compute converter if measurements say so |
| Servo rail | Pack direct or motor-domain buck | Motor | Voltage decided by RP-01's servo family. C01 makes regulated 5 V from 2S the leading working assumption |
| Drive rail | Pack direct | Motor | RP-03 |

## 3. Load-group ledger

Currents at the rail stated; power in W where the rail is open. "Transient" is the shape the rig must reproduce and the instrument must resolve.

| Code | Idle | Average working | Peak / transient | Transient character | Class | Basis | Measured by |
|---|---|---|---|---|---|---|---|
| `LG-01` SBC | 2.5–3 W | 4–8 W | 10–12 W; supply requirement 5 V / 3–5 A per class; **Pi 5 class (suggested candidate) is 5 V / 5 A and throttles above ~80 °C — active cooler and a vent path are part of the load, and the fan is a noise source for `LG-07`** | Sustained compute peaks under perception; USB/CSI inrush at boot; SD-card corruption on an unclean brownout makes the PA-07 soft-shutdown a requirement, not a nicety | `E` (class) | Published Pi 4 / Pi 5 class figures; **record the exact datasheet row (supply, undervoltage warning threshold for T-4) as `D` when a candidate is chosen** | RP-02 Phase B; RP-07 workload profiling |
| `LG-02` C2 | 0.2–0.4 W | 0.3–0.5 W | ≤ 1.5 W if Wi-Fi TX ever enabled (it should not be — wired link) | Boot inrush; negligible otherwise | `E` | ESP32-S3 dual-core active ≈ 60–110 mA at 3.3 V; Wi-Fi TX peak ≈ 300–400 mA — **verify against the Espressif ESP32-S3 datasheet current-consumption table and record as `D`** | RP-02 Phase A on the twin (note bridge current), then the Zero |
| `LG-03Y/P/R` servos | **sleep: torque off (`LP-03-OFF`, SD-02);** attentive hold 0.1–0.5 A each if gravity-loaded, lower if balanced | 0.3–0.8 A each during gestures | stall-class transient per unit at launch/reversal; **C01 XC330-M288-T eManual `D`: stall 1.80 A at 5.0 V, 1.34 A at 3.7 V, 2.15 A at 6.0 V**; operating current unmeasured | Launch/reversal/regenerative profiles | `U` (family), `D` C01 stall | RP-01 paper peaks 0.0953 / 0.0560 / 0.1099 N·m; sleep decision is not servo-family evidence | RP-01 busy-minute runs; RP-02 Phase B |
| `LG-04` drive | 0 (inhibited) | 3–8 W in motion for two small encoder gearmotors | 20–40 W for both at stall/reversal; 1.5–3 A per motor class | `LP-04-LAUNCH/REV/BRAKE`; signed regenerative current required | `E` (class) | JGA25/N20-class encoder gearmotor figures; RP-03 selects | RP-03; substitute profile in RP-02 until then |
| `LG-05` display + light | 1–1.5 W (dimmed idle) | 1.5–3 W | 3–3.5 W (full backlight + ESP32-S3 rendering + light) | Backlight step at wake; small | `U`; `E` range | Sibling panel SKU 24159 is listed ≈ 1.2 W (`D`, display study); add ESP32-S3 + backlight driver losses. **Waveshare wiki value for SKU 30493 to be recorded as `D`; measure on the sample** | RP-02 Phase A when the sample arrives |
| `LG-06` camera | 0.1–0.3 W (streaming idle) | 0.3–1.0 W | ≤ 1.5 W (autofocus actuator + full-rate capture) | AF motor steps; small | `U`; `E` range | No official power figure; community CM3 measurements 200–300 mA at 3.3 V | RP-02 Phase B on the SBC candidate |
| `LG-07` mics + front end | < 0.05 W | < 0.1 W | < 0.2 W (codec HAT) or ≤ 1 W (XMOS-class USB array with onboard DSP) | None material | `E` | PDM MEMS ≈ 1 mA each; codec/front end dominates. **A Pi-class SBC needs a 4-channel front end (2026-09-14 review); the USB-array option moves ~0.5–1 W onto Buck A via the SBC's USB rail** | RP-05 |
| `LG-08` speaker + amp | 0.1–0.3 W (amp idle) | 0.5–1.5 W (chirps, speech-level music) | 3–5 W electrical at registered peak level | `LP-08-MUSIC` RMS plus separate `LP-08-CREST` transients | `U`; `E` range | Small class-D amp + 3 W speaker class | RP-05/RP-06; RP-02 Phase B with a candidate |
| `LG-09` losses | 10–15 % of load | 10–15 % | 15–20 % at peak (buck efficiency falls at high current) | Follows load | `E` | Typical buck-module efficiency 85–92 % at these currents | Derived from `i_in · v_in` minus Σ `W` rows |
| `LG-10` base MCU + safety sensing | 0.2–0.4 W | 0.3–0.6 W | ≤ 1 W (ToF/IR emitters) | Sensor emitter pulses | `U` | RP-03 | RP-03 |

## 4. Qualification-case energy model — planning envelope

The state model now separates modes (`OM`), behaviours (`BS`), events (`EV`), qualification cases (`CC`) and synthetic stress (`ST`). Named profiles live in `RP-02-electrical/load-model.md`. This remains a coarse `E` envelope: nothing is registered and no row is `W`.

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
| **Draft `MD-01` v0.2** | Chronological recipe in state register | **average `E` ≈7.7–15.9 W** | **20 min** | **`E` ≈2.6–5.3 Wh** |
| **`CC-PEAK-01` credible peak** | Drive reversal/brake + tracking/camera + ordinary head correction + audio crest + face/safety | `U`; rebuild from aligned profiles | transient | — |
| **`ST-01` synthetic stress** | Aligns startle, drive reversal, audio crest, display transition and perception | Historical `E` ≈40–70 W pending rebuild | transient | — |

Consequences already visible from the envelope, all `E`:

- Historical `ST-01` could exceed the **Korad KA3005D's 5 A** at 2S. Phase B records the largest safe vector; full alignment waits on a protected suitable source.
- The prior 25% reserve/80% usable-depth example still gives ~8.3 Wh from the 5.3 Wh high case. It is not a pack selection.
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
- [ ] SBC candidate → `D` row; then `W` under RP-07 workload.
- [ ] Display sample → `W` idle/average/peak on the RP-02 rig.
- [ ] Pack internal resistance `D` for the working-assumption cells; `W` in Phase C.
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
