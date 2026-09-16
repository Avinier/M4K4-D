# RP-02 Power Calculation Ledger — Drop, Loss, Heat, Energy and Protection Coordination

| Field | Value |
|---|---|
| Status | **Accepted derived calculation issue v0.1, builder-reviewed 2026-09-16.** The equations and arithmetic are complete for presently bounded inputs; no final conductor, connector, converter, fuse, charger or pack is selected and no numeric gate is registered. |
| Created | 2026-09-16 |
| Scope | The fourth power-architecture pointer: voltage drop, energy, converter loss, heat, conductor heating and fuse/protection coordination |
| Authority | Registered topology `RP02-P2-REG-01` and implementation basis `RP02-P2-REG-02` |
| Canonical load input | `../../01-system/power-energy-ledger.md` v0.11; this document derives from it and does not establish a competing load budget |
| Recompute rule | Any change to a source, `LG`, `PB`, voltage, case/profile, path resistance, component or evidence class makes the affected row stale until recalculated |

This issue answers everything that can honestly be calculated before installed path lengths, converter efficiency maps, protection curves, pack impedance and drive/servo measurements exist. A conditional result is still useful; an invented point value is not.

## 1. Calculation boundary and present inputs

| Branch/case | Electrical input used | Evidence | What the number means |
|---|---:|---|---|
| `PB-COMPUTE`, selected Pi workload | 5.1 V; 10–12 W, therefore 1.96–2.35 A | Voltage/interface `D` and registered; workload `E` | Candidate-loss and thermal operating sweep |
| `PB-COMPUTE`, full interface | 5.1 V × 5 A = 25.5 W | Interface capability `D` | Interconnect/converter capability screen; not claimed consumption |
| `PB-DISPLAY`, documented nominal | 5.0 V × 0.45 A = 2.25 W | `D` | Published board point; status light and profile behavior excluded |
| `PB-DISPLAY`, planning peak | 5.0 V × 0.60–0.70 A = 3.0–3.5 W | `E` | Wake/full-reference screen pending sample capture |
| `PB-SAFE-C2`, upper working estimate | 5.0 V; 0.2–0.5 W, therefore 0.04–0.10 A | Load `E` | Current estimate before transceiver/sensing measurement |
| `PB-SAFE-C2`, documented supply capability | 5.0 V × 0.50 A = 2.5 W | Input/source requirement `D` | Conservative supply-path screen; not board consumption |
| One C01 head-axis reference | 5.0 V × 1.80 A = 9.0 W | `D`; candidate only | Stall reference, not an operating profile or selected servo |
| Three C01 axes aligned | 5.0 V × 5.40 A = 27.0 W | Derived from `D`; synthetic | Fault/stress reference, not `CC-PEAK-01` |
| `PB-AUDIO-OUT` high planning case | 5 W | `E` | Candidate-class sweep only |
| `PB-DRIVE` high planning case | 40 W | `E` | Candidate-class sweep; voltage/current/regeneration unresolved |
| `PB-MAIN` historical source case | 6.0 / 7.2 / 8.4 V | `E` | 2S sensitivity only; no chemistry or pack selection |
| `MD-01` load energy | 2.6–5.3 Wh over 20 min | `E` | Current registered workload with planning loads |
| System-efficiency sensitivity | 85 / 90 / 92 / 95% | `E` analysis cases | Not converter evidence or a minimum-efficiency decision |
| Capacity-policy sensitivity | 80% usable depth; 25% additive reserve | `E` candidate inputs | Not registered thresholds; used only to expose the energy transformation |

Camera and any USB microphone front end may be downstream of `PB-COMPUTE`. Aggregate source calculations count their power once: either inside measured compute-branch input or as a separately measured downstream term, never both.

## 2. Equations and evidence propagation

For a copper loop at temperature `T`:

`R_loop(T) = L_loop · R20 · [1 + 0.00393 · (T − 20 °C)]`

`V_terminal = V_converter − I_peak·R_loop(T) − ΣV_contact − ΣV_protection − ΣV_switch`

`P_wire = I_RMS²·R_loop(T)`

For a converting branch:

`P_loss,converter = P_out·(1/η − 1)`

`I_in = P_out/(V_in·η)`

For an interval:

`E_load = ∫V_load(t)·I_load(t)dt`

`E_source = E_load/η_system`

For the present additive-reserve convention:

`E_pack,nominal,min = E_load·(1 + r_reserve)/(DoD_usable·η_system)`

For a fault-path sensitivity:

`I_fault,min = V_source,min/R_path,max`

`I_fault,max = V_source,max/R_path,min`

An output derived from mixed evidence inherits the weakest input class. Thus every numeric result below remains `E` unless it is purely a transform of `D` values and is explicitly labelled otherwise. Approval of arithmetic does not promote it to `W`.

## 3. Voltage drop and conductor heating

### 3.1 One-metre loop comparison

`L_loop = 1.000 m` means positive plus return copper, not one metre each. The 60 °C column applies the registered copper coefficient (×1.1572); contacts and protection remain excluded.

| Path screen | Current | Gauge | Drop at 20 °C | Drop at 60 °C | Heat at 20 °C | Heat at 60 °C |
|---|---:|---:|---:|---:|---:|---:|
| `PB-COMPUTE` full interface | 5.0 A | AWG 16 | 66.0 mV | 76.4 mV | 0.330 W | 0.382 W |
| Same | 5.0 A | AWG 18 | 105.0 mV | 121.5 mV | 0.525 W | 0.608 W |
| `PB-DISPLAY` planning peak | 0.70 A | AWG 24 | 58.9 mV | 68.2 mV | 0.041 W | 0.048 W |
| Same | 0.70 A | AWG 26 | 93.8 mV | 108.5 mV | 0.066 W | 0.076 W |
| `PB-SAFE-C2` capability screen | 0.50 A | AWG 24 | 42.1 mV | 48.7 mV | 0.021 W | 0.024 W |
| Same | 0.50 A | AWG 26 | 67.0 mV | 77.5 mV | 0.034 W | 0.039 W |
| C01 three-axis trunk reference | 5.40 A | AWG 16 | 71.3 mV | 82.5 mV | 0.385 W | 0.445 W |
| Same | 5.40 A | AWG 18 | 113.4 mV | 131.2 mV | 0.612 W | 0.709 W |
| Same | 5.40 A | AWG 20 | 179.8 mV | 208.1 mV | 0.971 W | 1.124 W |
| One C01 axis reference | 1.80 A | AWG 20 | 59.9 mV | 69.4 mV | 0.108 W | 0.125 W |
| Same | 1.80 A | AWG 22 | 95.4 mV | 110.4 mV | 0.172 W | 0.199 W |
| Same | 1.80 A | AWG 24 | 151.6 mV | 175.4 mV | 0.273 W | 0.316 W |

These heat values are electrical dissipation, not temperature rise or ampacity proof. Insulation class, bundling, flex construction, airflow, termination and upstream clearing energy remain separate.

### 3.2 Absolute loop-length ceilings

The following is the **mathematical maximum loop length if wire consumes the entire registered distribution-drop allocation**. Real allowable length is always shorter because contacts, protection, switches and PCB copper also consume the allocation:

`L_loop,max = (V_allocation − V_devices)/(I·R_per_m(T))`

The table temporarily sets `V_devices = 0` only to expose the hard ceiling.

| Path screen | Allocation/current | Gauge | Ceiling at 20 °C | Ceiling at 60 °C | Finding |
|---|---:|---:|---:|---:|---|
| `PB-COMPUTE`, stricter steady target | 100 mV / 5.0 A | AWG 16 | 1.515 m | 1.309 m | Candidate remains possible pending device-drop budget |
| Same | 100 mV / 5.0 A | AWG 18 | 0.952 m | 0.823 m | One-metre loop already fails the steady target at 20 °C |
| `PB-DISPLAY` | 150 mV / 0.70 A | AWG 24 | 2.545 m | 2.199 m | Geometry, flex life and contacts will dominate before this ceiling |
| Same | 150 mV / 0.70 A | AWG 26 | 1.599 m | 1.382 m | Retains less device/contact margin |
| `PB-SAFE-C2` capability screen | 150 mV / 0.50 A | AWG 24 | 3.563 m | 3.079 m | Electrical drop alone is unlikely to govern a robot-scale run |
| Same | 150 mV / 0.50 A | AWG 26 | 2.239 m | 1.935 m | Flex/termination evidence still required |
| C01 three-axis trunk reference | 150 mV / 5.40 A | AWG 16 | 2.104 m | 1.819 m | Best of these three drop screens |
| Same | 150 mV / 5.40 A | AWG 18 | 1.323 m | 1.143 m | Leaves limited allowance for a long moving route plus contacts |
| Same | 150 mV / 5.40 A | AWG 20 | 0.834 m | 0.721 m | One-metre loop fails even before contacts |
| One C01 axis reference | 150 mV / 1.80 A | AWG 20 | 2.503 m | 2.163 m | Candidate remains possible pending flex/ampacity checks |
| Same | 150 mV / 1.80 A | AWG 22 | 1.572 m | 1.359 m | Candidate remains conditional |
| Same | 150 mV / 1.80 A | AWG 24 | 0.990 m | 0.855 m | One-metre loop fails at 20 °C before contacts |

No gauge is selected by this table. CAD must provide installed positive and return lengths; connector and protection candidates must provide worst-case hot resistance/drop.

### 3.3 Contact/protection resistance penalty

Every 10 mΩ of aggregate series resistance in the complete positive-plus-return path consumes:

| Path screen | Current | Additional drop | Additional heat |
|---|---:|---:|---:|
| `PB-COMPUTE` full interface | 5.0 A | 50 mV | 0.250 W |
| `PB-DISPLAY` planning peak | 0.70 A | 7 mV | 0.0049 W |
| `PB-SAFE-C2` capability screen | 0.50 A | 5 mV | 0.0025 W |
| C01 head trunk reference | 5.40 A | 54 mV | 0.292 W |
| One C01 axis reference | 1.80 A | 18 mV | 0.032 W |

This is why headline connector current ratings are insufficient: 10 mΩ would consume half of the Pi branch's 100 mV steady allocation at 5 A and over one third of the C01 trunk's 150 mV allocation at 5.4 A.

## 4. Converter loss and source-current sensitivity

### 4.1 Dissipation versus efficiency

| Output case | `P_out` | Loss at 85% | Loss at 90% | Loss at 92% | Loss at 95% |
|---|---:|---:|---:|---:|---:|
| C2 upper working estimate | 0.50 W | 0.088 W | 0.056 W | 0.043 W | 0.026 W |
| C2 capability screen | 2.50 W | 0.441 W | 0.278 W | 0.217 W | 0.132 W |
| Display documented nominal | 2.25 W | 0.397 W | 0.250 W | 0.196 W | 0.118 W |
| Display planning peak | 3.50 W | 0.618 W | 0.389 W | 0.304 W | 0.184 W |
| Pi workload high case | 12.0 W | 2.118 W | 1.333 W | 1.043 W | 0.632 W |
| Pi full-interface screen | 25.5 W | 4.500 W | 2.833 W | 2.217 W | 1.342 W |
| Audio-output planning high | 5.0 W | 0.882 W | 0.556 W | 0.435 W | 0.263 W |
| C01 three-axis reference | 27.0 W | 4.765 W | 3.000 W | 2.348 W | 1.421 W |
| Drive planning high | 40.0 W | 7.059 W | 4.444 W | 3.478 W | 2.105 W |

Efficiency is a surface `η(V_in, I_out, T)`, not a single marketing value. A candidate must supply the relevant curve or be measured at low, representative and peak load. Thermal qualification uses the worst sustained loss, not the smallest cell in this table.

### 4.2 Input current at 90% efficiency in the historical 2S source case

| Output case | At 6.0 V input | At 7.2 V input | At 8.4 V input |
|---|---:|---:|---:|
| C2 capability screen, 2.5 W | 0.463 A | 0.386 A | 0.331 A |
| Display planning peak, 3.5 W | 0.648 A | 0.540 A | 0.463 A |
| Pi workload high, 12 W | 2.222 A | 1.852 A | 1.587 A |
| Pi full-interface screen, 25.5 W | 4.722 A | 3.935 A | 3.373 A |
| Audio-output planning high, 5 W | 0.926 A | 0.772 A | 0.661 A |
| C01 three-axis reference, 27 W | 5.000 A | 4.167 A | 3.571 A |
| Drive planning high, 40 W | 7.407 A | 6.173 A | 5.291 A |

Rows are intentionally not summed: several are interface/stress screens rather than credible simultaneous operating loads. `CC-PEAK-01` must be rebuilt from measured, time-aligned profiles. The table does show that source-side protection and wiring cannot be sized by adding nominal output currents, and that a 5 A bench source cannot reproduce the drive high case at any of the three source voltages.

### 4.3 Worked distribution-heat examples

These examples use one metre loop, 60 °C copper, 10 mΩ aggregate contacts/protection, and 90% conversion efficiency. They exclude switch/PCB loss and do not imply installed length.

| Case | Converter loss | Wire heat | 10 mΩ heat | Partial distribution heat |
|---|---:|---:|---:|---:|
| Pi workload high: 12 W, 2.35 A, AWG 18 | 1.333 W | 0.135 W | 0.055 W | **1.523 W** |
| Display planning peak: 3.5 W, 0.70 A, AWG 24 | 0.389 W | 0.048 W | 0.005 W | **0.442 W** |
| C2 capability screen: 2.5 W, 0.50 A, AWG 24 | 0.278 W | 0.024 W | 0.003 W | **0.305 W** |
| C01 three-axis reference: 27 W, 5.40 A, AWG 16 | 3.000 W | 0.445 W | 0.292 W | **3.737 W** |

The C2 and C01 rows are capability/stress screens, not predicted sustained temperatures. Candidate temperature rise still requires topology-specific thermal resistance, airflow, copper area, enclosure ambient and duration.

## 5. `MD-01` energy and nominal-pack sensitivity

### 5.1 Source energy before capacity reserve

| System conversion efficiency | Source energy for 2.6 Wh low case | Source energy for 5.3 Wh high case |
|---:|---:|---:|
| 85% | 3.06 Wh | 6.24 Wh |
| 90% | 2.89 Wh | 5.89 Wh |
| 92% | 2.83 Wh | 5.76 Wh |
| 95% | 2.74 Wh | 5.58 Wh |

### 5.2 Nominal energy with 80% usable depth and 25% additive reserve

| System conversion efficiency | Nominal low-case requirement | Nominal high-case requirement |
|---:|---:|---:|
| 85% | 4.78 Wh | 9.74 Wh |
| 90% | 4.51 Wh | 9.20 Wh |
| 92% | 4.42 Wh | 9.00 Wh |
| 95% | 4.28 Wh | 8.72 Wh |

The former 8.28 Wh high-case example is the **lossless-conversion** result: `5.3 Wh × 1.25 / 0.80`. It is not sufficient when converter/distribution loss is included. At the present 85–95% sensitivity, the corresponding high-case nominal envelope is 8.72–9.74 Wh. This remains a planning envelope, not the battery requirement or selection.

The present load-energy range implies 7.8–15.9 W average over 20 minutes. Every additional 1 W of true average load sustained for the full workload adds 0.333 Wh at the loads and, at 90% system efficiency with the same depth/reserve convention, 0.579 Wh to nominal pack energy. This is the direct recalculation rule if the selected Pi memory SKU or its measured workload changes.

## 6. Fuse and protection coordination

### 6.1 What the current numbers do and do not bound

| Branch | Present non-trip input | Current numeric conclusion | Missing before selection |
|---|---|---|---|
| `PB-COMPUTE` | 1.96–2.35 A workload `E`; 5 A interface capability `D` | Protection/interconnect must support the selected input method and measured boot/workload without nuisance action | Boot/inrush waveform, PD/header method, candidate curve/drop, wire/contact path and fault current |
| `PB-DISPLAY` | 0.45 A nominal `D`; 0.60–0.70 A peak `E` | Approximately 1 A-class devices may be searched, but no fuse value is justified | Sample boot/wake/source-transfer waveform, status light, hot resistance and fault behavior |
| `PB-SAFE-C2` | 0.04–0.10 A working `E`; 0.50 A supply capability `D` | The 0.50 A figure must not be mistaken for consumption or a fuse rating | Installed transceiver/sensors, inrush, converter current limit and safe fault containment |
| `PB-HEAD-Y/P/R` | 1.80 A per-axis C01 stall `D` | Candidate curves must distinguish admissible launch/reversal from a sustained jam; 1.8 A alone cannot set a fuse | Selected servo, operating waveform, internal limiting, harness and required clearing behavior |
| `PB-HEAD` | 5.40 A synthetic C01 alignment | Defines a measurement/source stress decade only | Credible `CC-06` waveform, selected family, converter limit/retry and per-axis containment |
| `PB-DRIVE` | 20–40 W class `E` | No current rating follows while voltage, driver and regeneration are open | Complete RP-03 hardware and signed waveforms |
| `PB-MAIN` | 4.8–11.7 A historical source-equivalent `E` | Instrument/source range only | Pack min/max impedance, credible aligned peak, branch selectivity and wire/connector withstand |

### 6.2 Fault-current sensitivity for the historical 2S voltage only

This table evaluates `I = V/R`; the resistances are deliberately hypothetical total source-plus-path values. It demonstrates the information required from a pack/branch, not expected Makad fault current.

| Total source-plus-path resistance | At 6.0 V | At 8.4 V |
|---:|---:|---:|
| 50 mΩ | 120 A | 168 A |
| 100 mΩ | 60 A | 84 A |
| 200 mΩ | 30 A | 42 A |
| 500 mΩ | 12 A | 16.8 A |
| 1.0 Ω | 6 A | 8.4 A |

A high-resistance end-of-branch fault can be harder for a fuse to clear than a low-resistance source fault. Coordination therefore uses both `I_fault,min` at the remote hot path and `I_fault,max` at the source-near cold path.

### 6.3 Required coordination calculation for every candidate

1. Overlay the measured `I(t)` operating/inrush envelope on the candidate's minimum-time trip/current-limit curve at maximum operating temperature. Every valid profile must remain in the non-trip region.
2. Calculate `I_fault,min` and `I_fault,max` from pack/source and path impedance tolerances.
3. Obtain worst-tolerance, temperature-adjusted clearing/current-limit behavior across that fault range; a nominal fuse label is not a curve.
4. Integrate clearing stress: `I²t_clear = ∫i²dt`; compare it with conductor, contact, switch and PCB withstand at the installed thermal condition.
5. Compare downstream and upstream curves at the **same** fault current. Where selectivity is required, the branch device must contain the fault before main/pack protection acts.
6. For e-fuses/converters, record foldback, hiccup, retry, latch, reverse-current and thermal-shutdown behavior. Repeated retry energy must be included.
7. Verify terminal voltage drop in normal operation and the safe terminal state after protection acts.
8. Repeat on the physical rig using a current-limited fault fixture; never prove pack short-circuit behavior by applying an uncontrolled short.

No final fuse or e-fuse rating is calculable from present data. That is the correct result of the coordination calculation: device curves, path impedance and `W` waveforms are mandatory inputs.

## 7. Thermal accounting

For each populated branch and `TB-3/TB-4` interval:

`P_heat,total = P_converter + I_RMS²R_wire + I_RMS²R_contacts + Σ(V_drop,device·I_mean) + P_load,dissipated`

Candidate temperature rise may be estimated only with a topology-appropriate thermal model:

`ΔT ≈ P_heat·θ` for a validated lumped steady-state case, or the candidate's transient thermal impedance for time-varying loads.

Required thermal rows are:

| Location | Driving profile | Required input/result |
|---|---|---|
| Compute converter and input connection | Pi boot, perception/audio coexistence, `MD-01` | Efficiency map, RMS/peak current, board/case temperature and connector rise |
| C2 independent supply | Charge and operate source transfer, controller fault workload | Low-load efficiency, selector/drop heat and continuous safety availability |
| Display converter/head connector | Charge display, wake/full-reference and `MD-01` | Brightness-dependent input, source transfer and moving-contact rise |
| Head converter/trunk/axes | `CC-05`, `CC-06`, hold and thermal profile | Selected servo RMS/peak/regeneration, flex resistance and converter transient thermal response |
| Drive stage/branches | Launch, reversal, brake, spin and sustained follow | Signed input/output RMS, switching loss, motor/wire heat and regenerative energy |
| Main protection/isolation/E-stop | Credible whole-system cases and fault clearing | Continuous drop, transient/clearing energy and contact temperature |

Peak samples determine drop and electrical stress; RMS over the correct interval determines heating; `MD-01` determines heat soak and energy. These quantities are not interchangeable.

## 8. Completion state of this pointer

| Work item | State after v0.1 | Remaining evidence |
|---|---|---|
| Voltage-drop equations and allocations | Complete | Installed lengths and device drops populate final rows |
| Known-branch conductor sensitivity | Complete for Pi, display, C2 and C01 reference | Exact cable/flex construction, gauge and temperature validation |
| Converter-loss calculation | Complete as an efficiency/load sweep | Candidate efficiency surfaces and thermal implementation |
| Source-current transformation | Complete for the historical 2S sensitivity | Selected source voltage/impedance and credible aligned profiles |
| `MD-01` energy transformation | Complete for current 2.6–5.3 Wh `E` input | Per-profile `W`, RP-03 drive and integrated endurance |
| Conductor/contact heating | Complete parametrically | Installed resistance, RMS waveforms, bundling and ambient |
| Fuse/protection coordination method | Complete | Candidate curves, min/max fault current, path withstand and physical verification |
| Final component ratings | Intentionally open | Required upstream selections and `W/D` evidence; tracked in [`../openitems.md`](../openitems.md) |

The next update replaces one conditional term at a time. It must not overwrite assumptions silently: input revision, evidence class, formula, result and affected upstream branches are recorded together.

## 9. Calculation QA record

| Check | Result |
|---|---|
| Units | Voltage in V, current in A, resistance in Ω, power in W, energy in Wh; mV/mΩ converted explicitly |
| Copper temperature factor | `1 + 0.00393·(60−20) = 1.1572` |
| Pi workload current | `10/5.1 = 1.96 A`; `12/5.1 = 2.35 A` |
| C01 aligned reference | `3·1.80 = 5.40 A`; `5·5.40 = 27.0 W` |
| `MD-01` average | `2.6/(1/3) = 7.8 W`; `5.3/(1/3) = 15.9 W` |
| Lossless high pack example | `5.3·1.25/0.8 = 8.28125 Wh` |
| 90%-efficient high pack example | `5.3·1.25/(0.8·0.9) = 9.201 Wh` |
| Independent arithmetic check | Tables regenerated with a local calculation script on 2026-09-16; rounded only for presentation |
