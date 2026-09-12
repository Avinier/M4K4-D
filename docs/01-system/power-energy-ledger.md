# Makad V1 Power / Energy / Thermal Ledger

| Field | Value |
|---|---|
| Status | **Living — created 2026-09-08; every row is `E` or `U`. No `W` evidence exists.** |
| Version | 0.2 |
| Owner | Project builder |
| Created | 2026-09-08 |
| Last reviewed | 2026-09-12 |
| Governed by | `risk-prototype-plan.md` v1.11 §"Continuous sourcing and data workstream" (power/energy/thermal ledger deliverable) and §RP-02 (G02 invariant, G03 rehearsal) |
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
| `LG-01` | Main compute — Linux SBC | Logic | Buck A, 5 V | **Unselected** (Pi 4 / Pi 5 class candidates) |
| `LG-02` | Head motion controller C2 + servo-bus transceiver | Logic | Buck B, 5 V → on-board 3.3 V | Waveshare ESP32-S3-Zero (selected); DevKitC-1 twin on the bench |
| `LG-03Y/P/R` | Head servos yaw / pitch / roll — **separately observable** | Motor | Servo rail (voltage per PA-04) | **Unselected**; XC330 is a packaging reference only |
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
| Servo rail | Pack direct or motor-domain buck | Motor | Voltage decided by RP-01's servo family |
| Drive rail | Pack direct | Motor | RP-03 |

## 3. Load-group ledger

Currents at the rail stated; power in W where the rail is open. "Transient" is the shape the rig must reproduce and the instrument must resolve.

| Code | Idle | Average working | Peak / transient | Transient character | Class | Basis | Measured by |
|---|---|---|---|---|---|---|---|
| `LG-01` SBC | 2.5–3 W | 4–8 W | 10–12 W; supply requirement 5 V / 3–5 A per class | Sustained compute peaks under perception; USB/CSI inrush at boot | `E` (class) | Published Pi 4 / Pi 5 class figures; **record the exact datasheet row as `D` when a candidate is chosen** | RP-02 Phase B; RP-07 workload profiling |
| `LG-02` C2 | 0.2–0.4 W | 0.3–0.5 W | ≤ 1.5 W if Wi-Fi TX ever enabled (it should not be — wired link) | Boot inrush; negligible otherwise | `E` | ESP32-S3 dual-core active ≈ 60–110 mA at 3.3 V; Wi-Fi TX peak ≈ 300–400 mA — **verify against the Espressif ESP32-S3 datasheet current-consumption table and record as `D`** | RP-02 Phase A on the twin (note bridge current), then the Zero |
| `LG-03Y/P/R` servos | hold: 0.1–0.5 A each if gravity-loaded; ~0 if balanced (A0 target) | 0.3–0.8 A each during gestures | stall-class transient per unit at launch/reversal; **reference family XC330-M288: `D` ≈ 1.8 A at 5 V — verify against the ROBOTIS eManual**; other families 1–3 A | Launch inrush tens of ms; reversal spikes every stitched `MJ5` segment (HM-07 four in ~1 s); regenerative current on deceleration | `U` (family), `D` reference | RP-01 selection; candidate-specific Layout 03 mass/inertia tree decides how close to stall the gestures come | RP-01 busy-minute runs; RP-02 Phase B |
| `LG-04` drive | 0 (inhibited) | 3–8 W in motion for two small encoder gearmotors | 20–40 W for both at stall/reversal; 1.5–3 A per motor class | Stall inrush on every S10 reversal; regenerative on braking | `E` (class) | JGA25/N20-class encoder gearmotor figures; RP-03 selects | RP-03; substitute profile in RP-02 until then |
| `LG-05` display + light | 1–1.5 W (dimmed idle) | 1.5–3 W | 3–3.5 W (full backlight + ESP32-S3 rendering + light) | Backlight step at wake; small | `U`; `E` range | Sibling panel SKU 24159 is listed ≈ 1.2 W (`D`, display study); add ESP32-S3 + backlight driver losses. **Waveshare wiki value for SKU 30493 to be recorded as `D`; measure on the sample** | RP-02 Phase A when the sample arrives |
| `LG-06` camera | 0.1–0.3 W (streaming idle) | 0.3–1.0 W | ≤ 1.5 W (autofocus actuator + full-rate capture) | AF motor steps; small | `U`; `E` range | No official power figure; community CM3 measurements 200–300 mA at 3.3 V | RP-02 Phase B on the SBC candidate |
| `LG-07` mics + front end | < 0.05 W | < 0.1 W | < 0.2 W | None material | `E` | PDM MEMS ≈ 1 mA each; codec/front end dominates | RP-05 |
| `LG-08` speaker + amp | 0.1–0.3 W (amp idle) | 0.5–1.5 W (chirps, speech-level music) | 3–5 W electrical at registered peak level | Music transients; sustained in S09 | `U`; `E` range | Small class-D amp + 3 W speaker class | RP-05/RP-06; RP-02 Phase B with a candidate |
| `LG-09` losses | 10–15 % of load | 10–15 % | 15–20 % at peak (buck efficiency falls at high current) | Follows load | `E` | Typical buck-module efficiency 85–92 % at these currents | Derived from `i_in · v_in` minus Σ `W` rows |
| `LG-10` base MCU + safety sensing | 0.2–0.4 W | 0.3–0.6 W | ≤ 1 W (ToF/IR emitters) | Sensor emitter pulses | `U` | RP-03 | RP-03 |

## 4. State energy model — planning envelope

Per registered state in `state-register.md`, summed from §3 midpoints at the stated class. This is the `E_MD01` integration in `power-architecture.md` §2. **Illustrative only: no state is registered and no row is `W`.**

| State | Composition (dominant groups) | Power range (W) | `MD-01` duration | Energy range (Wh) |
|---|---|---|---|---|
| S02 quiet idle | SBC idle + display dim + servo hold or off | 4–8 | 4 min | 0.27–0.53 |
| S03 attentive idle | SBC avg + camera + display + small servo motion | 7–14 | 8 min 34 s | 1.00–2.00 |
| S04 wake ×6 | Three-axis launch + chirp + perception spin-up | 25–45 peak, ~1 s each | 6 s total | ~0.05 |
| S05 search | Yaw sweeps + camera + perception | 10–18 | ~6 s | ~0.03 |
| S06 gestures ×12 | Servo reversal bursts | 15–30, 1–2 s each | ~20 s | ~0.12 |
| S07 startle ×2 | Three-axis simultaneous peak + audio + display | 30–50 peak, <0.5 s | ~1 s | ~0.01 |
| S08 requests ×4 | SBC peak + audio + display utility view | 10–18 | ~40 s | ~0.15 |
| S09 music | Sustained audio peak + eyes + capture | 8–16 | 3 min | 0.40–0.80 |
| S10/S11 base motion | Drive avg + tracking compute + head corrections | 15–30 | 3 min | 0.75–1.50 |
| S12 spin ×1 | Drive sustained max + head + audio | 30–50 | ~3 s | ~0.04 |
| S15 shutdown | Descent + sign-off | 5–10 | ~10 s | ~0.02 |
| **`MD-01` total** | | **average ≈ 8.5–16 W** | **20 min** | **≈ 2.8–5.3 Wh** |
| **Composite peak (S13)** | S07 during S09 during S10 reversal, perception at S11 load | **≈ 40–70 W** → **5.5–9.5 A at 7.4 V**, 3.5–6.5 A at 11.1 V | instantaneous | — |

Consequences already visible from the envelope, all `E`:

- The composite peak exceeds the **Korad KA3005D's 5 A** at 2S voltage. S13 cannot be produced from the bench supply; `rig.md` §1 records this.
- Required pack energy at the top of the range with 25 % reserve and 80 % usable depth of discharge: `5.3 / 0.8 × 1.25 ≈ 8.3 Wh`. A 2S1P of ordinary 2.5 Ah 18650s is ≈ 18 Wh; a 2S 1500 mAh LiPo is ≈ 11 Wh. **Neither is a selection**; the point is that the trip-wire in §6 is not close to firing on the planning envelope, and the interesting risk is still the *peak*.
- Servo transients dominate the peak; the servo family selection in RP-01 is the largest single lever on the pack, the fuses and the conductor across the yaw boundary.

## 5. Coexistence invariant (the reshaped RP02-G02)

> Every registered state in `state-register.md` completes without unintended reset, unsafe motion, rail excursion outside registered component limits, data corruption, or thermal-limit violation.

**Re-run rule.** The invariant must be re-verified, and the verification recorded in `RP-02-electrical/decision.md` with run IDs, whenever any of the following occurs:

1. a load-group row changes evidence class (`U`→`E`, `E`→`W`, or a `W` value changes by more than its stated uncertainty);
2. a load group is added or a substitute is replaced by real hardware;
3. the servo rail voltage or the pack configuration changes;
4. a new state is registered, or `MD-01` is re-versioned;
5. any conductor, connector or fuse on the tree changes.

The record names which states were verified with which loads, which remain pending, and when the next re-run is due. "Verified in September on bench loads" is not verification in November with drive motors.

## 6. Trip-wire

Evaluated at every ledger revision; a trip forces a **mandatory design review** recorded in `MEMORY.md`, not a silent range adjustment.

| Trip | Condition | Review must consider |
|---|---|---|
| **T-1 Energy** | `E_MD01,high / (usable DoD · η_conv) · (1 + reserve)` exceeds the usable energy of the *largest* pack that fits the mass row's high bound (500 g) and the low-and-forward placement | Servo class, head mass, `MD-01` composition honesty, runtime target (CON-10 may rise, never fall) |
| **T-2 Peak** | Composite peak current at the pack exceeds the working-assumption pack's continuous rating, or the servo-rail drop at S07 exceeds the PA-06 limit with the largest credible conductor across the yaw boundary | Servo family, bulk capacitance, conductor gauge versus harness flex life, pack P-count |
| **T-3 Thermal** | Any regulator's steady-state dissipation at the S11 sustained average exceeds what a passive enclosure can shed at the SC-TBD-12 limit | Converter choice, airflow in RP-06, duty cycle |
| **T-4 Compute rail** | SBC rail minimum during S07 falls within 0.25 V of the SBC's undervoltage threshold on the planning model | PA-05 separation, converter transient response, bulk capacitance placement |

## 7. Open items

- [ ] Replace every `E`-class datasheet reference in §3 with a cited `D` row (Espressif, Waveshare, ROBOTIS, SBC vendor) — one afternoon, no purchase.
- [ ] Register the state set and `MD-01`; recompute §4 from registered durations.
- [ ] Servo family (RP-01) → servo rail voltage; per-unit stall/hold `D`; then `W` from the RP-01 busy-minute runs.
- [ ] SBC candidate → `D` row; then `W` under RP-07 workload.
- [ ] Display sample → `W` idle/average/peak on the RP-02 rig.
- [ ] Pack internal resistance `D` for the working-assumption cells; `W` in Phase C.
- [ ] Register per-component undervoltage limits so the invariant's "rail excursion" term is testable.
- [ ] Drive `W` rows from RP-03; until then the S10–S13 rows carry a named substitute.
- [ ] Retire `LG-09` as a lump once per-branch `W` rows allow the residual to be attributed.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-08 | 0.1 | Created under plan v1.10 as the canonical power/energy/thermal budget. Defined load groups `LG-01…LG-10` and rails, entered planning envelopes (`E`/`U`) for every group, computed an illustrative `MD-01` energy and composite-peak envelope, and adopted the coexistence invariant with its re-run rule and four trip-wires. No `W` evidence; no selection. |
| 2026-09-12 | 0.2 | Corrected proposed MD-01 to exactly 20 minutes by extending S03 to 8 min 34 s; recomputed the planning energy to ~2.8–5.3 Wh and top-of-range pack requirement to ~8.3 Wh. Clarified that S13 covers transient concurrency, not sustained/state-specific verification. No state or threshold registered. |
