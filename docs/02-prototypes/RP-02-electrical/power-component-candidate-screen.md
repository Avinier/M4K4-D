# RP-02 Power-Component Candidate Screen

| Field | Value |
|---|---|
| Status | **Accepted derived candidate screen v0.1, builder-reviewed 2026-09-16. No power component is selected and no purchase is authorized.** |
| Date | 2026-09-16 |
| Scope | Part-2 implementation candidates for conversion, protection, motor isolation/E-stop actuation, connectors, conductors and charging/power path |
| Inputs | `RP02-P2-REG-01`, `RP02-P2-REG-02`, `power-branch-contracts.md` v0.4 and `power-calculation-ledger.md` v0.1 |
| Evidence rule | Manufacturer documentation establishes `D`; distributor stock/price establishes only a dated sourcing snapshot; installed performance remains `W` |
| Excluded | Numeric brownout/restart thresholds and hold-up values (policy is now in `brownout-restart-contract.md` v0.1); exact pack chemistry, S-count and capacity; RP-03 drive hardware; final fuse ratings; purchase |

This screen asks a harder question than “is the headline current high enough?” A candidate survives only when its voltage window, loss, thermal behavior, fault response, reverse-energy behavior, configuration risk, documentation and physical implementation are compatible with the registered branch contract.

## 1. Outcome

The following parts or families are worth carrying into schematic and bench work:

| Function | Lead carried forward | Present disposition |
|---|---|---|
| `PB-COMPUTE` conversion | Murata `OKL-T/6-W12P-C`; `OKR-T/6-W12-C` as a through-hole comparison | **Lead, conditional** — correct 5.1 V programmability and 6 A class; low-line transient and thermal proof remain |
| `PB-SAFE-C2` production conversion | TI `TPS630701` fixed 5 V implementation | **Lead, conditional** — enable, power-good and load disconnect are stronger than a three-pin hobby module; requires a custom PCB |
| `PB-SAFE-C2` bench conversion | Pololu `S13V10F5` | **Bench-only lead** — wide-input fixed 5 V and 1 A class, but no enable, power-good or reverse protection |
| `PB-DISPLAY` bench conversion | Pololu `S13V15F5` | **Bench-only lead** — 1.5 A class with margin over the 0.70 A planning peak; same control limitations as above |
| High-current branch protection | TI `TPS25982` family | **Lead, conditional** — 2.7 mΩ typical path and programmable 2–15 A behavior; exact suffix, curve and location remain open |
| Low-current isolation/protection | TI `TPS25947` family | **Lead for C2/display/source ORing; rejected at 5 A compute output** |
| Replaceable source fuse | Littelfuse `ATOF 287` family plus a rating-compatible holder | **Lead family only** — rating waits on measured profiles and fault impedance |
| Physical E-stop operator | IDEC `XW1E-BV402M-R`, 40 mm mushroom, 2 NC | **Lead operator, conditional** — direct-opening/safety-lock evidence exists; it commands the motor switch and does not carry motor current |
| Motor-arm power switch/controller | ADI `LTC4368-1` plus external back-to-back MOSFETs | **Engineering lead, not a safety-rated subsystem** — permits bidirectional-current analysis; FET, shunt, thermal and regeneration proof remain |
| Retained pack disconnect | Anderson `SBS Mini` keyed housing/contact system | **Lead family, conditional** — touch-safe, keyed, high-cycle and ample current class; exact contact, gauge, colour and retention remain |
| Low-current internal connector | Molex `Micro-Fit 3.0` | **Lead for C2/display only** — exact circuit count, terminal and measured loop resistance required |
| High-current internal connector | Molex `Micro-Fit+` | **Lead family, conditional** — stronger current/contact-resistance class than standard Micro-Fit; exact configuration required |
| Charge inlet / PD negotiation | USB-C receptacle plus ST `STUSB4500QTR` | **Architecture lead** — standalone dead-battery PD sink; not a battery charger |
| Charger / NVDC power path | TI `BQ25798` | **Architecture lead** — preserves 1–4S Li-ion/Li-polymer/LiFePO4 admissibility; exact charge settings wait on the pack |

No moving-head power cable is selected. The electrically adequate industrial torsion-cable examples found are too heavy and bulky to assume into the head, while generic silicone wire has no defensible torsion-life specification. That is a real open item, not a sourcing omission.

## 2. Candidate namespace and dispositions

Candidate records use `PCD-<class>-<nn>`:

| Class | Function |
|---|---|
| `CVT` | DC/DC conversion |
| `PRO` | Fuse, e-fuse and branch protection |
| `EST` | E-stop operator and motor-arm switching |
| `CON` | Connector/interconnect |
| `CAB` | Conductor or moving cable |
| `CHG` | Charge inlet, negotiation and charger/power path |

Dispositions are deliberately weaker than selection:

| Disposition | Meaning |
|---|---|
| **Lead** | Best presently documented route into schematic/bench evaluation; not selected |
| **Conditional** | Admissible only if the stated evidence closes |
| **Bench-only** | Useful for characterization but missing an installed-product requirement |
| **Hold** | Potentially admissible, but an upstream decision is absent |
| **Reject** | Fails a current registered contract or lacks minimum engineering evidence for the stated use |

## 3. Screening gates

Every candidate is screened against all applicable gates below. A missing value is not a pass.

| Gate | Required question |
|---|---|
| Source/load window | Does the complete tolerance/temperature window cover the branch, including the historical 6.0–8.4 V 2S sensitivity where applicable? |
| Terminal margin | After converter tolerance, ripple, switches, protection, both contacts and both conductors, is the registered load-terminal envelope retained? |
| Continuous/transient capability | Are current, duration, repetition and thermal derating supported by curves rather than a single headline rating? |
| Fault containment | Is overload/short behavior known, including blanking, foldback, retry, latch, thermal shutdown and restoration? |
| Reverse energy | Can the part tolerate or deliberately block backfeed/regeneration without creating rail overvoltage or an unintended powered domain? |
| Default state | On loss of software, control power or wiring, does the hazardous path become or remain safe? |
| Configuration integrity | Are trim, NVM, firmware and part-suffix choices controlled and verifiable? |
| Physical implementation | Are PCB copper, thermal vias, capacitance/ESR, crimp tooling, strain relief and service geometry achievable? |
| Evidence quality | Is there an official datasheet/product specification with the necessary limits and curves? |
| Sourcing | Is the exact orderable part available from a traceable supplier, with a substitute strategy and no purchase implied? |

## 4. DC/DC converter candidates

### 4.1 `PB-COMPUTE`

The selected Raspberry Pi 5 requires a dedicated 5.1 V nominal branch capable of the 5 A interface case. The [Raspberry Pi 5 USB-PD paper](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf) confirms that Pi 5 requests only 5 V profiles, uses the optional 5 V/5 A PDO when present and otherwise assumes 5 V/3 A unless `PSU_MAX_CURRENT=5000` or `usb_max_current_enable=1` deliberately overrides negotiation. Therefore converter capability and Pi power-entry policy are separate decisions.

| ID | Candidate and `D` facts | Screen | Disposition |
|---|---|---|---|
| `PCD-CVT-01` | Murata [`OKL-T/6-W12P-C`](https://pim.murata.com/asset/pim4/nonIsolatedDCDCconverter/OKL-T6-W12_PDF_NONISOLATEDDCDCCONVERTER?lastModifiedDatetime=20250707193407): 4.5–14 V input, 0.591–5.5 V programmable output, 6 A/30 W, 20 mV p-p maximum listed ripple/noise, 91% minimum/93% typical efficiency at 12 V→5 V full load, positive enable | Fits 5.1 V and the historical 2S window. LGA module demands a custom carrier, output-trim tolerance control, specified capacitors and thermal layout. Must prove 6.0 V input, 5.1 V output, Pi workload/full-interface steps and enclosure temperature | **Lead, conditional** |
| `PCD-CVT-02` | Murata [`OKR-T/6-W12-C`](https://pim.murata.com/asset/pim4/nonIsolatedDCDCconverter/OKR-T6-W12_PDF_NONISOLATEDDCDCCONVERTER?lastModifiedDatetime=20250707193507): 4.5–14 V input, 0.591–6 V programmable output, 6 A/30 W, through-hole SIP | Electrically comparable and easier to rework on a prototype distribution board. Larger and less mechanically compact; the same low-line, output-capacitance and thermal tests apply | **Lead comparison, conditional** |
| `PCD-CVT-03` | Pololu [`D42V55F5`](https://www.pololu.com/product/5571): fixed 5 V; catalogued 6 A typical maximum is specified at 42 V input and the input-dependent graph governs | Practical prebuilt module, but it does not implement the registered 5.1 V converter target and low-line dropout/thermal behavior must be read at 6.0 V. It may characterize a restricted 3 A Pi configuration only if the power-entry policy is recorded | **Bench-only** |
| `PCD-CVT-04` | Pololu [`D42V55F5.3`](https://www.pololu.com/product/5572/specs): fixed 5.3 V nominal, 6 A class | Its ±3% output family tolerance can reach about 5.46 V before transient/ripple. No official Pi input-maximum proof was found that makes this safe | **Reject for direct Pi power** |
| `PCD-CVT-05` | Murata [`MYLSM00502ERPL`](https://www.murata.com/products/productdata/8807034880030/MYLSM00502ERPL.pdf): 4.5–17 V input, programmable through 5.25 V, 2.5 A output | Cannot satisfy the registered 5 A-capable interface | **Reject for `PB-COMPUTE`** |

`PCD-CVT-01` and `-02` satisfy the existing “two candidates minimum” requirement. `PCD-CVT-03` is not counted as an equivalent installed candidate because it changes the registered output and Pi power-entry assumptions.

### 4.2 Independent C2 and display conversion

| ID | Candidate and `D` facts | Screen | Disposition |
|---|---|---|---|
| `PCD-CVT-06` | TI [`TPS630701`](https://www.ti.com/product/TPS63070) fixed 5 V buck-boost family: 2–16 V after startup, 2 A class, 50 µA typical quiescent current, enable, power-good, load disconnect, soft start, overtemperature and input/output overvoltage protection | Best production-oriented common building block for two **separate** C2/display converters. The design still needs separate input protection, passives, PCB layout and a proof that the 1 A startup limit reaches regulation with each installed load/capacitance | **Lead, conditional** |
| `PCD-CVT-07` | Pololu [`S13V10F5`](https://www.pololu.com/product/4083): 2.8–22 V input, fixed 5 V ±3%, 1 A typical continuous, 85–95% typical efficiency | Covers C2's 0.5 A source-capability contract with margin. Three-pin module has no enable, power-good or reverse-input protection; 10–20 mA family no-load current is high relative to a safety-supervision branch | **Bench-only lead for `PB-SAFE-C2`** |
| `PCD-CVT-08` | Pololu [`S13V15F5`](https://www.pololu.com/product/4084): 2.8–22 V input, fixed 5 V ±3%, 1.5 A typical continuous, 85–95% typical efficiency, 2 A current limit | Covers the 0.70 A display planning peak with thermal margin for characterization. No enable, power-good or reverse protection; maximum output depends on input and cooling | **Bench-only lead for `PB-DISPLAY`** |
| `PCD-CVT-09` | Pololu [`S9V11E2A`](https://www.pololu.com/product/5719): adjustable 2.5–9 V output, potentiometer, enable | Electrical range is attractive but an exposed trim is an avoidable single-adjustment configuration hazard on the safety branch | **Reject for installed `PB-SAFE-C2`** |

Using the same converter IC on C2 and display does not merge the branches: they require separate devices, protection, returns and enable/control paths.

### 4.3 Head, drive and audio conversion

- No head-servo converter is led forward as an installed selection. If C01 is selected, `PCD-CVT-01/-02` are admissible 5 V/6 A bench sources only after regeneration/rail-rise testing; their datasheets do not establish an ability to sink servo regeneration.
- No drive converter is screenable until RP-03 defines driver voltage, signed current and braking behavior.
- No audio converter is screenable beyond a 5 V/5 W planning class until RP-05 selects the amplifier and records crest/RMS current. It must remain separately protected from compute and C2.

## 5. Protection and fuse candidates

### 5.1 Candidate register

| ID | Candidate and `D` facts | Appropriate use | Disposition |
|---|---|---|---|
| `PCD-PRO-01` | TI [`TPS25982`](https://www.ti.com/product/TPS25982): 2.7–24 V, 2.7 mΩ typical, adjustable 2–15 A threshold, circuit-breaker/current-limiter variants, adjustable blanking, <400 ns typical fast trip, current monitor, latch/retry suffixes | High-current compute/head-input or distribution branch where 2 A minimum limit is acceptable and reverse blocking is not required | **Lead, conditional** |
| `PCD-PRO-02` | TI [`TPS25947`](https://www.ti.com/product/TPS25947): 2.7–23 V, back-to-back FETs, 28.3 mΩ typical/45 mΩ maximum stated over operating conditions, 0.5–6 A threshold, true reverse-current blocking, soft start, current monitor, latch/retry variants | Low-current C2/display isolation, source ORing or charge-logic selection | **Lead for low current; reject on 5 A compute output** |
| `PCD-PRO-03` | Littelfuse [`ATOF 287`](https://www.littelfuse.com/assetdocs/littelfuse_datasheet_287_atof_r2.7.pdf?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40): 32 VDC, 1–40 A family, 1 kA interruption at 32 VDC, ISO 8820-3, -40 to 125 °C with temperature derating and time-current curves | Source-adjacent replaceable main fuse, with an exact holder and rating chosen from measured non-trip/fault cases | **Lead family, rating open** |
| `PCD-PRO-04` | Littelfuse [`451/453 Nano2`](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1): very-fast SMD family; 5 A part has 12.5 mΩ nominal cold resistance and 5.566 A²s nominal melting `I²t` | Low-energy PCB branches only after inrush overlay | **Hold; reject 5 A part as default compute protection** |

### 5.2 Drop and heat screen

These are arithmetic transforms of datasheet resistance, before PCB copper and self-heating:

| Device/current case | Voltage drop | Device heat | Finding |
|---|---:|---:|---|
| `TPS25947`, 0.50 A, 28.3 mΩ typical | 14.2 mV | 7.1 mW | Plausible on C2 |
| `TPS25947`, 0.70 A, 28.3 mΩ typical | 19.8 mV | 13.9 mW | Plausible on display |
| `TPS25947`, 5.00 A, 28.3 mΩ typical | 141.5 mV | 0.708 W | Fails the Pi branch's 100 mV steady allocation by itself |
| `TPS25947`, 5.00 A, 45 mΩ maximum | 225 mV | 1.125 W | Also exceeds the 200 mV transient allocation before wire/contact loss |
| `TPS25982`, 5.00 A, 2.7 mΩ typical | 13.5 mV | 67.5 mW | Electrically plausible; hot maximum resistance and PCB thermal proof still required |
| Nano2 5 A fuse, 5.00 A, 12.5 mΩ nominal cold | 62.5 mV | 0.313 W | Consumes 62.5% of the Pi steady allowance and has very-fast nuisance-trip risk |

The calculations reject use cases, not entire components. `TPS25947` remains a strong low-current part precisely because its reverse isolation and 0.5 A lower threshold are valuable where the current is small.

### 5.3 Coordination policy retained

- `ATOF` is a fuse **family**, not a chosen ampere value. At 65 °C, the manufacturer derating table permits only 4 A continuous through a 5 A fuse, 8 A through a 10 A fuse and 12 A through a 15 A fuse; final selection cannot be made from room-temperature labels.
- An e-fuse does not replace the source-adjacent fuse unless its failure mode, source fault withstand and PCB clearing path prove the same protection objective.
- Auto-retry is not the default on a hazardous or persistent short path. Latch-off is preferred until the later fault/recovery analysis proves bounded retry energy.
- Pack protection, main fuse, branch protection and converter limiting must be overlaid at the same minimum and maximum fault currents. Lower printed amperage is not selectivity evidence.

## 6. E-stop operator and motor-arm switching

| ID | Candidate and `D` facts | Screen | Disposition |
|---|---|---|---|
| `PCD-EST-01` | IDEC [`XW1E-BV402M-R`](https://www.idec.com/en-us/switches-indicator-lights/switches-pushbuttons/emergency-stop-switches/xw-22mm-estop/xw1e-bv402m-r): 22 mm panel, 40 mm non-illuminated mushroom, 2 NC, direct-opening operation to IEC 60947-5-5/IEC 60947-5-1 Annex K, safety-lock mechanism | One NC path commands the hardwired motor gate; the second supplies independent status/diagnostics or a second channel after wiring analysis. Panel access, ingress and exact low-voltage wetting/current remain to verify | **Lead operator, conditional** |
| `PCD-EST-02` | ADI [`LTC4368-1`](https://www.analog.com/en/products/ltc4368.html): 2.5–60 V operating controller, external back-to-back N-MOSFETs, +50 mV forward and -50 mV reverse breaker thresholds, adjustable UV/OV, latch/retry, shutdown and fault output | A local pull-down makes a broken/open NC E-stop loop deassert `SHDN`; system arm is a second hardware permission. External MOSFET SOA, shunt, turn-off, downstream discharge and regeneration remain design work | **Engineering lead, conditional** |
| `PCD-EST-03` | `LTC4368-2`, -3 mV reverse threshold | Diode-like reverse behavior can trip normal motor regeneration and strand energy on the motor rail | **Reject as the motor-bus default** |
| `PCD-EST-04` | `TPS25982` used alone as motor-arm switch | Low loss and strong forward fault response, but its present evidence does not establish the required bidirectional regeneration policy or off-state reverse isolation | **Hold, not sole E-stop gate** |

The E-stop contacts do **not** carry `PB-MOTOR`. They carry a low-energy, fail-open control loop. The power stage is normally off, requires both the closed E-stop loop and a fresh system-arm permission, and cannot re-arm merely because the mushroom is released. `brownout-restart-contract.md` fixes the release/restart policy; exact timing remains evidence-gated.

For scale only, a 3 mΩ `LTC4368-1` shunt would set approximately ±16.7 A nominal breaker thresholds from ±50 mV. At the historical 11.7 A source sensitivity it would drop 35.1 mV and dissipate 0.411 W. Tolerance, trip timing, actual credible current and regeneration decide the real value; 3 mΩ is not selected.

## 7. Connector candidates

| ID | Candidate and `D` facts | Intended interface | Disposition |
|---|---|---|---|
| `PCD-CON-01` | Anderson [`SBS Mini`](https://www.andersonpower.com/content/dam/app/ecommerce/product-pdfs/SBS-Mini/ds-sbsmini.pdf): touch-safe two-position keyed housings, 20–10 AWG contacts, up to 52 A depending contact/wire, 45 A at 72 V hot-plug class, 8,000 mating cycles listed for housing variants | Retained pack/service disconnect; use a dedicated colour/key and cable clamp | **Lead family, conditional** |
| `PCD-CON-02` | Molex [`Micro-Fit 3.0`](https://www.content.molex.com/dxdam/51/51a0d355-e3c6-469a-ad15-4585d36e4d38/987650-5984.pdf): up to 8.5 A depending terminal/configuration, 10 mΩ maximum contact resistance, positive latch, typical 30 mating cycles | C2, display and low-current internal branches; not a routine service connector | **Lead low-current family** |
| `PCD-CON-03` | Molex [`Micro-Fit+`](https://www.content.molex.com/dxresources/3735/37353d15-101d-40e0-926e-f134c113cad1.pdf): up to 13.5 A and 5 mΩ maximum initial contact-resistance class for the named power-terminal system, in 3 mm pitch | Compute/head trunk internal power where exact terminal/circuit derating and resistance pass | **Lead high-current family, conditional** |
| `PCD-CON-04` | JST [`VH`](https://order.jst-mfg.com/InternetShop/app/pdf_show.php?kbn=1&key=eVH.pdf): 3.96 mm wire-to-board, 10 A with AWG16 in the specified case | Stationary board power and rig alternatives | **Bench/stationary alternative** |
| `PCD-CON-05` | USB-C receptacle with controlled PD sink | `PB-CHARGE-IN` only | **Lead inlet architecture** |
| `PCD-CON-06` | Generic Dupont/friction header | Any installed power or moving harness | **Reject** |
| `PCD-CON-07` | Generic XT30 listings without a manufacturer-controlled product specification | Pack or motor disconnect | **Reject pending authoritative engineering data** |

Standard Micro-Fit illustrates why current rating alone is inadequate. If the 10 mΩ maximum applies to each mated positive and return contact, the connector loop can consume 20 mΩ: 100 mV and 0.50 W at 5 A. That is the complete Pi steady distribution allowance before wire, fuse, switch or PCB. Therefore standard Micro-Fit is not approved for the full-current Pi path from the family brochure alone. Micro-Fit+ remains conditional until the exact terminal/housing product specification is bound.

For comparison, two 5 mΩ Micro-Fit+ power contacts would consume 50 mV and 0.25 W at 5 A. That is materially better but still half the Pi steady allocation, so the exact contact system and installed four-wire resistance still decide the path.

The pack and charge interfaces must use physically different connector systems. Colour alone is not accepted as the only anti-mating control between battery and charger.

## 8. Conductors and moving cable

| ID | Candidate class | Screen | Disposition |
|---|---|---|---|
| `PCD-CAB-01` | Fixed body copper pair, AWG16 candidate | At a 1 m positive-plus-return loop and 60 °C copper, the existing ledger gives 76.4 mV/0.382 W at 5 A. It is the leading full-interface Pi/trunk gauge before device losses and installed length | **Conditional; gauge not selected** |
| `PCD-CAB-02` | Fixed/low-motion AWG24 candidate | Ledger gives 48.7 mV at 0.5 A and 68.2 mV at 0.7 A per 1 m hot loop; electrically plausible for C2/display | **Conditional; flex construction not selected** |
| `PCD-CAB-03` | igus [`chainflex CFROBOT`](https://www.igus.com/cables/robotic-cables) torsion cable family | Provides manufacturer torsion/bend-life data and is a useful qualification benchmark. Available constructions are comparatively bulky/heavy for the Makad head and do not establish installed mass acceptability | **Benchmark / Hold** |
| `PCD-CAB-04` | Generic high-strand-count silicone wire | Flexible and useful on a bench, but no controlled torsion-cycle, jacket-wear or conductor-fatigue specification was found | **Bench-only** |

The moving-yaw cable selection requires four inputs before any SKU can pass: installed bend/torsion geometry from RP-01, loop length, conductor allocation by branch, and cycle target/test. Electrical calculations alone cannot close it.

## 9. Charging and power-path candidates

### 9.1 Architecture carried forward

`certified external USB-C PD adapter → protected USB-C inlet → STUSB4500QTR PD sink → BQ25798 charger/NVDC path → protected pack`

The charger `SYS`/power-path output does not directly authorize normal robot operation. Separate hardware gating must make only `PB-CHARGE-LOGIC` reachable in `OM-06`; compute, camera, audio and motor branches remain off even when the charger can power a system with a depleted or absent pack.

| ID | Candidate and `D` facts | Screen | Disposition |
|---|---|---|---|
| `PCD-CHG-01` | ST [`STUSB4500QTR`](https://www.st.com/en/interfaces-and-transceivers/stusb4500.html): active QFN variant; standalone sink negotiation to 20 V/5 A, three NVM PDO profiles, dead-battery mode, VBUS monitoring/discharge and external PMOS drivers | Removes MCU dependency from establishing the input contract. NVM image, receptacle protection, cable/source capabilities and negotiated-power telemetry must be configuration controlled | **Lead PD sink** |
| `PCD-CHG-02` | TI [`BQ25798`](https://www.ti.com/product/BQ25798): 1–4 cells, Li-ion/Li-polymer/LiFePO4 listing, 3.6–24 V input, 5 A charge maximum, buck-boost, NVDC power path, BATFET, thermistor/thermal regulation, 16-bit ADC and IEC 62368-1 CB certification | Preserves the admissible battery envelope. It is USB-PD-compatible electrically but does not replace the PD contract controller. QFN layout, firmware defaults, pack thermistor, charge current and failure behavior require dedicated review | **Lead charger/power path, conditional** |
| `PCD-CHG-03` | TI `BQ25792`: similar 1–4S/5 A Li-ion/Li-polymer NVDC buck-boost charger | Viable if Li-ion/Li-polymer is selected, but does not preserve the same explicit LiFePO4 candidate envelope | **Conditional fallback after chemistry freeze** |
| `PCD-CHG-04` | TI `BQ25798EVM` or integrated PD/charger evaluation hardware | Useful to characterize charger behavior before committing a dense 4 mm QFN board | **Bench-only; not installed product** |
| `PCD-CHG-05` | Undocumented “USB-C trigger” plus generic charger module | Missing controlled PD, cell-count, thermal, load-sharing and failure evidence | **Reject** |

The external adapter itself remains open. Selection requires the eventual maximum charge power, Indian regulatory/plug requirements, cord geometry and the decision whether 15 V or 20 V is the preferred PDO. AC mains remains outside Makad.

## 10. Sourcing snapshot — 2026-09-16

Stock and price are volatile and do not upgrade technical evidence. Values below are only proof that lead parts are not paper-only unobtainium.

| Candidate | Dated supplier result | Replacement/sourcing risk |
|---|---|---|
| `PCD-CVT-01` `OKL-T/6-W12P-C` | [Mouser India](https://www.mouser.in/en/ProductDetail/Murata-Power-Solutions/OKL-T-6-W12P-C?qs=CxV9Ey7RZVdXGDAP%2FweYNg%3D%3D) showed 51 immediately dispatchable at about ₹580.51 each; search inventory views differed, so recheck at purchase | Medium: 26-week factory lead shown for replenishment; exact module is specialized |
| `PCD-PRO-01` `TPS25982` family | [Mouser India family result](https://www.mouser.in/c/semiconductors/power-management-ics/voltage-regulators-voltage-controllers/?series=TPS25982) showed `TPS259824ONRGET` at ₹404.40 and 5,331 in stock; suffix is not selected | Low–medium: multiple suffixes create configuration risk |
| `PCD-CHG-01` `STUSB4500QTR` | [Mouser India](https://www.mouser.in/en/ProductDetail/STMicroelectronics/STUSB4500QTR?qs=wUXugUrL1qyQbYMSzG1ujg%3D%3D) showed 10,789 in stock at ₹206.86 each | Low for IC; medium for correct NVM/tooling and USB-C layout |
| `PCD-CHG-02` `BQ25798RQMR` | [Mouser India](https://www.mouser.in/en/ProductDetail/Texas-Instruments/BQ25798RQMR?qs=ljCeji4nMDmr66dwAbNsCg%3D%3D) showed 12,583 in stock at ₹491.06 each | Low for IC availability; high implementation complexity |
| `PCD-CON-01` `SBS Mini` | [DigiKey India](https://www.digikey.in/en/products/detail/anderson-power-products-inc/B02265G1/10650609) listed keyed housings; contacts and clamp are separate order lines | Medium: exact colour/contact/crimp-tool bill must be built as one assembly |
| `PCD-CVT-07/-08` Pololu modules | Pololu lists active products and international distributor routes; no dependable domestic-stock result was accepted | Medium–high for quick India replacement; suitable for bench, not sole production plan |
| `PCD-EST-01` IDEC XW1E | Official family/SKU documentation found; India stock and landed price not verified | Medium until exact authorized distributor is bound |

Prices exclude GST/import/shipping unless the supplier page explicitly included them. They are not a budget update and do not authorize an order.

## 11. Explicit no-buy list from this screen

- Do not buy a generic “5 V 5 A buck” without low-line efficiency, transient, thermal and output-capacitance evidence.
- Do not buy `D42V55F5.3` for direct Pi power merely because 5.3 V appears to offset cable drop.
- Do not place `TPS25947` or a Nano2 5 A fuse in the full-current Pi output path without revising the registered drop budget through evidence.
- Do not route motor current through the panel E-stop contacts.
- Do not use `LTC4368-2` as the default motor gate while regeneration is credible.
- Do not use standard Micro-Fit, Dupont or undocumented XT30 assemblies as the retained pack connector.
- Do not use generic silicone wire as qualified moving-head cable.
- Do not treat `BQ25798` as a USB-C PD negotiator, or the `STUSB4500` as a battery charger.
- Do not purchase cells, pack, charger or adapter from this screen.

## 12. Evidence required before selection

| Candidate function | Required bench/design evidence |
|---|---|
| Compute converter | 6.0/7.2/8.4 V source sweep; Pi boot and workload steps; 5 A electronic-load step; ripple at Pi terminal; startup into installed capacitance; hot enclosure temperature; enable/off backfeed; selected Pi power-entry method |
| C2/display converter | Cold/hot startup, source transfer, minimum-load regulation, quiescent current, short/retry behavior, power-good timing and no cross-branch backfeed |
| e-fuse/branch protection | Exact suffix and resistor tolerances; inrush/non-trip overlay; hot on-resistance; min/max fault-current response; latch/retry energy; upstream selectivity |
| Main fuse/holder | Exact ATOF value and holder; ambient derating; crimp/holder resistance; remote minimum fault and source-near maximum fault; `I²t` path withstand |
| E-stop/motor gate | Broken-wire safe state; hardware arm truth table; full-current drop/heat; MOSFET SOA; regenerative current; F-12 assertion; downstream discharge; release cannot re-arm |
| Connectors | Exact terminal/housing pair; crimp cross-section/pull test; hot four-wire mated resistance; temperature rise at circuit count; vibration/flex/service cycling; anti-mating demonstration |
| Moving cable | Installed geometry and mass; resistance hot and after cycling; bend/torsion endurance with simultaneous power/data; insulation/jacket inspection |
| PD/charger path | PDO/NVM audit; wrong/weak adapter behavior; hot plug; pack absent/depleted; thermistor open/short; charge-current accuracy; `OM-06` exclusivity; source removal/return; thermal soak |

The later selection ADR must name the exact manufacturer part number, suffix, passive configuration, connector terminals, crimp tooling, firmware/NVM image, evidence run IDs and every rejected alternative affected by the decision.

## 13. Completion state

| Work item | Result |
|---|---|
| Requirement envelopes | Complete enough for current architecture and known loads; drive/head final envelopes remain honestly open |
| Manufacturer candidate discovery | Complete for compute/C2/display conversion, protection, E-stop operator/gate approach, main/branch connectors and charge path |
| Critical screening | Complete at `D/E` level, including explicit use-case rejections and quantitative loss checks |
| Availability snapshot | Complete for principal imported lead parts; local walk-in availability remains open |
| Component selection | **Not complete and not implied** |
| Purchase | **Not authorized** |
| Brownout/restart policy | Registered as `RP02-P2-REG-03` in `brownout-restart-contract.md` v1.0; numeric values remain open |
