# RP-02 Power Implementation Basis — Voltage, Interconnect, Protection, Capacitance and Sequence

| Field | Value |
|---|---|
| Status | **Registered implementation-basis v1.0 under `RP02-P2-REG-02`, builder-approved 2026-09-16.** Derived beneath architecture `RP02-P2-REG-01`; selects Raspberry Pi 5 2 GB as `LG-01` but no converter, protection, connector, conductor, capacitor, charger or pack. |
| Created | 2026-09-16 |
| Scope | The second power-architecture pointer: voltage domains, grounding implementation, connector requirements, provisional conductor sizing, protection coordination, E-stop implementation requirements, bulk-capacitance policy and circuit-level power sequencing |
| Excluded | Numeric brownout thresholds, debounce/dwell, hold-up capacitance and motor-bus discharge time; policy and calculation method are issued separately in `brownout-restart-contract.md` v0.1. Final pack capacity remains reserved for RP-03 drive evidence and integrated endurance |
| Numeric source | `../../01-system/power-energy-ledger.md`; branch obligations in `power-branch-contracts.md` |
| Evidence rule | Manufacturer limits are `D`; arithmetic from `D/E` inputs retains the weakest input class. Registered design allocations are not qualification gates unless they are also copied into `gates.md` with the required registration fields. |

This document translates the registered functional topology into implementable electrical requirements. “5 V” below names a voltage class, not permission to join branches: `PB-SAFE-C2`, `PB-COMPUTE`, `PB-DISPLAY` and a possible 5 V `PB-HEAD` remain independently converted/protected where required by `PA-05`, `PA-11` and `PA-12`.

## 1. Inputs already fixed

- Four failure-consequence domains and the complete `PB-*` energy tree are registered under `RP02-P2-REG-01`.
- C2 and future base safety use independent supply/protection paths.
- The motor source is battery-only and lies behind the system motor-arm gate and dominant hardware E-stop.
- `OFF`, `OPERATE` and `CHARGE` are distinct electrical configurations.
- Charge mode may energize only C2/minimum supervision and display.
- Returns are common-reference/star-routed with paired conductors and no actuator current in signal/safety returns.
- Pack construction, drive, servo family, charger, converter and protection implementations remain open. Raspberry Pi 5 2 GB is selected as the SBC; workload draw and power-entry implementation remain open.

## 2. Voltage-domain implementation

### 2.1 Registered rule

Use independently generated **5 V-class endpoint supplies** where the selected hardware supports them, while keeping the protected pack bus native and leaving motor conversion family-dependent. Do not distribute a robot-wide 3.3 V rail: 3.3 V remains board-local except for explicitly current-limited interface references.

This yields fewer nominal voltage classes without merging failure branches.

### 2.2 Branch voltage table

| Branch | Endpoint / analysis case | Source evidence / reasoning | Status and constraint |
|---|---:|---|---|
| `PB-MAIN` | Pack-native | Historical analysis case is 2S Li-ion, approximately 6.0–8.4 V loaded/full; pack and chemistry are not selected | `E/U`. Architecture must admit the servo/drive outcome rather than freeze 2S now. |
| `PB-CHARGE-IN` | Charger-dependent | Adapter voltage must cover the selected chemistry/S-count, charger headroom and restricted load while keeping AC outside Makad | `U`; cannot close before pack/charger choice. |
| `PB-CHARGE-LOGIC` | **5 V class registered** | C2 and display are both compatible with 5 V-class endpoints, but remain downstream of independent selectors/protection | Charger power-path must support the complete charge-mode load. |
| `PB-SAFE-C2` | **5.0 V nominal registered** | Waveshare specifies 3.7–6 V external input at the pad marked 5 V and at least 500 mA supply capability | `D` interface; transceiver/sensing addition and acceptable terminal tolerance remain `U/W`. |
| `PB-SAFE-BASE` | 5 V service class proposed, local logic regulation | Common MCU/sensor integration case; RP-03 has not selected the controller or sensors | `E/U`; independent converter remains mandatory even if its nominal voltage matches C2. |
| `PB-COMPUTE` | **5.1 V nominal registered for selected Raspberry Pi 5 2 GB** | Raspberry Pi specifies a stable 5 V rail and recommends 5 V/5 A capability with the expanded USB allocation; reliable-operation guidance says stay above 4.8 V | `D` interface. Exact input connector/PD-current advertisement and workload `W` remain open. |
| `PB-DISPLAY` | **5.0 V nominal registered** | Selected Waveshare SKU 30493 is documented as Type-C 5 V, 450 mA nominal, 0–65 °C | `D` interface. The ledger's 0.60–0.70 A peak planning range remains until sample measurement. |
| `PB-CAMERA` | SBC camera-interface rails | Camera Module 3 generates/uses its module rails through the CSI connector; it is not a separately distributed robot voltage domain | `D/U`; selected SBC/interface owns sequencing and cable pinout. |
| `PB-AUDIO-IN` | 5 V USB or board-local 3.3 V candidate | Depends on USB-array versus codec/front-end selection | `U`; no shared 3.3 V distribution assumption. |
| `PB-AUDIO-OUT` | 5 V class leading case | Present planning load is a small class-D amplifier; output power and speaker remain open | `E/U`; noise and crest evidence decide whether a different rail is warranted. |
| `PB-MOTOR` | Pack-native switched bus | Keeps the E-stop path independent of application conversion | Registered topology; numeric range follows pack choice. |
| `PB-HEAD` | **5.0 V only in the C01 case** | ROBOTIS specifies XC330-M288-T input 3.7–6.0 V, recommends 5.0 V and gives 1.80 A stall reference at 5 V | `D` reference, not family selection. A 2S pack cannot directly feed this 6.0 V-maximum servo. |
| `PB-DRIVE` | Pack-native or converted | Driver/motor absent until RP-03 | `U`; must retain signed regeneration behavior. |

Primary sources:

- [Waveshare ESP32-S3-Zero documentation](https://docs.waveshare.com/ESP32-S3-Zero)
- [Waveshare ESP32-S3-LCD-4.3 / SKU 30493 documentation](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3)
- [ROBOTIS XC330-M288-T e-Manual](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)
- [Raspberry Pi 5 power documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply)
- [Raspberry Pi voltage-monitoring guidance](https://www.raspberrypi.com/documentation/computers/config_txt.html#monitoring-voltage)
- [Raspberry Pi Camera Module 3 product information](https://pip.raspberrypi.com/categories/786-raspberry-pi-camera-module-3)

### 2.3 Selected-display battery interface disposition

SKU 30493 includes its own single-cell battery/charge circuitry. The registered Makad implementation does **not** connect the central robot pack to that battery input and does not count the display's onboard charger as the system charger. `PB-DISPLAY` enters through the documented 5 V input path. This avoids an uncontrolled second battery domain, charger conflict and an unnamed back-power route. The final schematic review must determine whether the unused onboard battery/charge path needs physical disablement or whether leaving it unconnected is sufficient.

## 3. Ground and return implementation

`PA-15` already fixes the topology. Implementation must satisfy all of the following:

1. Put the primary 0 V star at the protected source/distribution entry, after any current-sense arrangement whose offset has been analyzed.
2. Route positive and return together for every branch. The return conductor receives the same connector, flex and thermal scrutiny as the positive conductor.
3. Give `PB-SAFE-C2`, `PB-SAFE-BASE`, `PB-COMPUTE`, `PB-DISPLAY`, `PB-AUDIO-OUT`, `PB-HEAD` and `PB-DRIVE` independent returns to their distribution point.
4. Keep `PB-HEAD` and `PB-DRIVE` current out of UART, encoder, CSI shield, USB shield, chassis and safety-sensor references.
5. Join non-isolated signal references at the interface endpoints without creating a parallel power return. Each link's reference-current path must be drawable on the schematic.
6. Treat programming USB, bench instruments and the external charger as temporary or permanent ground connections in the partial-power matrix; no cable may defeat system `OFF` or back-power an unpowered controller.
7. Terminate the CSI shield and any later cable shield according to the selected interface/cable design; there is no universal “ground both ends” rule in this baseline.
8. Do not use structure, bearings, fasteners or cable shields as intentional load-current conductors.

Required evidence is source-to-load positive drop, load-to-source return drop and signal-reference offset during `CC-06`, `CC-PEAK-01` and applicable drive cases.

## 4. Connector requirements

Exact installed families remain unselected. `power-component-candidate-screen.md` now records sourced `PCD-CON-*` leads and exclusions; the following interfaces remain distinct selection problems whose exact terminals and assemblies still require the current, packaging and physical evidence shown:

| Interface | Mandatory properties | Selection blocker |
|---|---|---|
| Retained pack/service disconnect | Polarized, finger-safe against accidental short, mechanically retained against vibration, one-action isolation, rated for source fault/non-trip envelope, pack-first/last mating behavior documented | Pack current, chemistry, fault current, placement and service geometry |
| Charge inlet | Different and non-mateable with pack/motor connectors; keyed, strain-relieved, touch-safe, reverse/backfeed protected, insertion detectable before motor operation is permitted | Charger/adapter voltage/current and body panel |
| `PB-COMPUTE` | Rated for full selected SBC interface current at the allowed terminal drop; positive retention; no reliance on loose friction headers | SBC and power-entry method |
| `PB-SAFE-C2` and `PB-DISPLAY` yaw service boundary | Separate protected contacts and returns even if housed in one multiway shell; positive latch; low mass; suitable flex-tail strain relief | Installed path, contact resistance, cycle/service target |
| `PB-HEAD` upstream | Contacts and return sized for aligned three-axis transient, temperature and repeated motion; servo bus pins cannot carry motor return | Servo family/current and harness route |
| `PB-HEAD-Y/P/R` | Family-compatible locking connection, individually observable and serviceable; contact rating/temperature covers branch protection | Servo selection and physical chain topology |
| `PB-DRIVE` / `L/R` | Polarized, retained, noise-aware routing; driver-output contact and wire withstand covers brake/reversal/stall reference | RP-03 hardware and PWM/current behavior |
| Low-level signals | Reference included; voltage-compatible; pin order chosen so partial mating cannot apply power through a signal pin | Interface/connector selection |

Rules:

- Dupont-style loose friction jumpers are bench-only and forbidden in the installed moving or power harness.
- Connector current ratings are accepted only at the actual contact count, wire gauge, ambient, housing and temperature-rise condition.
- Parallel contacts are credited only if the manufacturer permits them and current-sharing failure is analyzed.
- Every connector drop allocation includes both power and return contacts.
- A combined shell does not combine the branch identities or their protection.

## 5. Conductor and voltage-drop basis

### 5.1 Calculation

For copper loop length `L_loop` and conductor resistance per metre `R20`:

`R_loop(T) = L_loop · R20 · [1 + 0.00393 · (T − 20 °C)]`

`V_drop = I(t) · R_loop(T) + ΣV_contact(t) + ΣV_protection(t)`

`P_wire,RMS = I_RMS² · R_loop(T)`

The installed cable manufacturer's maximum conductor resistance replaces the ideal table below. Flex construction, strand count, bundling, jacket temperature, airflow and motion life can force a larger conductor even when voltage drop passes.

### 5.2 Copper reference table at 20 °C

| Gauge | Approximate copper resistance | Increase at 60 °C |
|---:|---:|---:|
| AWG 16 | 13.2 mΩ/m | ×1.157 |
| AWG 18 | 21.0 mΩ/m | ×1.157 |
| AWG 20 | 33.3 mΩ/m | ×1.157 |
| AWG 22 | 53.0 mΩ/m | ×1.157 |
| AWG 24 | 84.2 mΩ/m | ×1.157 |
| AWG 26 | 134 mΩ/m | ×1.157 |
| AWG 28 | 213 mΩ/m | ×1.157 |

`L_loop` is the total positive-plus-return copper length. Contact, fuse/e-fuse, switch and PCB losses are additional.

### 5.3 Normalized planning calculations

These calculations use one metre of total copper loop at 20 °C so they remain useful before CAD supplies exact installed lengths.

| Path case | Current basis | Gauge case | Wire drop per 1 m loop | Wire heat per 1 m loop | Interpretation |
|---|---:|---:|---:|---:|---|
| `PB-COMPUTE` full Pi 5 interface | 5.0 A `D` capability | AWG 18 | 105 mV | 0.525 W | Meets a 150 mV wire-only allocation at 20 °C; little room for temperature/contacts |
| Same | 5.0 A | AWG 16 | 66.0 mV | 0.330 W | More credible if full 5 A capability and a long body route are retained |
| `PB-SAFE-C2` source capability | 0.50 A minimum `D` | AWG 24 | 42.1 mV | 0.021 W | Transceiver/sensors and actual flex resistance still add |
| `PB-DISPLAY` planning peak | 0.70 A `E` | AWG 24 | 58.9 mV | 0.041 W | Candidate starting point; wake/source-transfer capture remains required |
| C01 three-axis common head trunk | 5.40 A stall-reference `D` | AWG 18 | 113.4 mV | 0.612 W | Only 36.6 mV remains inside a 150 mV/3% total allocation before contacts and protection |
| Same | 5.40 A | AWG 16 | 71.3 mV | 0.385 W | Better planning case for the common trunk, still not a final flex-wire choice |
| One C01 axis branch | 1.80 A stall-reference `D` | AWG 22 | 95.4 mV | 0.172 W | Leaves little total-drop margin after contacts/protection |
| Same | 1.80 A | AWG 20 | 59.9 mV | 0.108 W | More robust reference case if each axis carries its own full loop |

At 60 °C, multiply both the listed wire drop and heat by approximately 1.157 before considering further self-heating. These rows do not establish ampacity: insulation temperature, bundling and upstream clearing energy are separate checks.

### 5.4 Registered implementation targets

| Endpoint | Registered total distribution allocation | Reason |
|---|---:|---|
| `PB-SAFE-C2` | ≤150 mV from converter output to board input during valid operation | Keeps the 5 V-class safety branch comfortably inside the board's 3.7–6 V input while reserving converter transient margin |
| `PB-DISPLAY` | ≤150 mV from converter output to board input | 3% of 5 V; keeps connector/harness heating observable and bounded |
| `PB-COMPUTE` Pi 5 case | ≤100 mV steady wire/contact drop and ≤200 mV transient total drop from regulated 5.1 V output to board terminal | Preserves the documented >4.8 V reliable-operation guidance after converter tolerance/ripple is included |
| `PB-HEAD-Y/P/R` C01 case | ≤150 mV from head-converter output to each servo terminal during `CC-06` | Retains the existing unregistered 3% G02 candidate; stall reference is reported separately |
| `PB-MAIN`, `PB-DRIVE`, other motor families | Mechanism-specific; not yet assigned | Requires pack/driver/motor and safe-stop evidence |

These allocations are registered design constraints under `RP02-P2-REG-02`, not qualification gates. A later gate may tighten them but cannot silently weaken them.

## 6. Protection and coordination basis

### 6.1 Required protection zones

1. Pack-integral protection bounds cell/pack abuse according to the selected assembly.
2. Source-adjacent main protection bounds the wiring from retained pack connector to downstream distribution.
3. Each independent converter/input branch has protection that prevents its fault from collapsing safety supervision or overheating its conductors.
4. `PB-HEAD-Y/P/R` and `PB-DRIVE-L/R` retain individual observation and a selected containment mechanism; a resettable fuse is not assumed.
5. Converter/driver current limit is credited only after its retry, foldback, latch and thermal behavior are documented.
6. E-stop and motor-arm switching withstand the motor-source load, fault, inrush and regenerative conditions; logic-rated switch contacts are insufficient evidence.

### 6.2 Current evidence available for non-trip screening

| Branch | Present evidence | What may be screened now | Why a rating cannot close |
|---|---|---|---|
| `PB-SAFE-C2` | Board source capability ≥0.50 A `D`; installed peripherals `U` | Instrument/current-limit decade | Actual peak, converter inrush and sensors/transceiver |
| `PB-DISPLAY` | 0.45 A nominal `D`; 0.60–0.70 A peak `E` | Approximately 1 A-class candidate search | Sample boot/wake/current-limit behavior and charge-source transfer |
| `PB-COMPUTE` | Selected Pi 5 interface up to 5 A `D`; workload peak 2.0–2.4 A `E` | 5.1 V/5 A-capable converter/interconnect search | Peripherals, boot, PD/input method and measured workload |
| `PB-HEAD-Y/P/R` | C01 1.80 A/axis stall reference at 5 V `D` | Shunt/instrument and connector screening | Operating waveform/duration, selected servo, internal limit and fault policy |
| `PB-HEAD` | 5.40 A three-axis stall coincidence `D` synthetic reference | Common-trunk/source sensitivity | Credible alignment, converter limit/transient and branch clearing behavior |
| `PB-DRIVE` | 20–40 W class peak `E` | Bench-source decade only | Entire RP-03 implementation and regeneration |
| `PB-MAIN` | Historical `ST-01` source-equivalent 4.8–11.7 A `E` | Bench/connector measurement range | Pack, real credible peak, drive, source impedance and downstream selectivity |

### 6.3 Coordination calculation to populate per candidate

For every protective device, record:

- maximum continuous/RMS current and thermal window;
- credible peak amplitude, duration and repetition;
- synthetic/fault reference kept separate from credible operation;
- minimum and maximum available fault current at the branch end, including pack/path impedance;
- device voltage drop and heating in normal operation;
- trip/current-limit time at minimum fault current;
- wire/contact `I²t` or thermal withstand through clearing;
- upstream device response to the same fault;
- retry/latch/reset behavior and whether restoration can restart hazardous output.

Selectivity passes only when the downstream fault is contained without losing a required safety branch, or when an explicitly analyzed common shutdown is the safer outcome. “Branch fuse rating is lower than main fuse rating” is not coordination proof.

## 7. Bulk-capacitance basis

Bulk capacitance has four distinct jobs: converter-loop stability, load-edge current, bounded ride-through and noise containment. One capacitor cannot be credited for all four without analysis.

For a constant-current approximation:

`C_required = I · Δt / ΔV`

Stored energy is:

`E_cap = ½ · C · V²`

Examples show why capacitance cannot compensate for an undersized source:

| Example | Arithmetic | Result |
|---|---|---:|
| Hold 1 A for 1 ms with 0.1 V droop | `1 × 0.001 / 0.1` | 10,000 µF |
| Hold a 5 A compute edge for 1 ms with 0.2 V droop | `5 × 0.001 / 0.2` | 25,000 µF |
| Hold the C01 three-axis 5.4 A reference for 10 ms with 0.15 V droop | `5.4 × 0.010 / 0.15` | 360,000 µF |
| Energy in 4,700 µF at 5 V | `½ × 0.0047 × 5²` | 0.059 J |
| Energy in 10,000 µF at 5 V | `½ × 0.010 × 5²` | 0.125 J |

Implementation rules:

- Obey every selected converter's permitted output capacitance, ESR and startup/inrush constraints.
- Keep branch-local bulk downstream of its branch protection; do not bridge independent safety/application branches with a capacitor.
- Audio bulk stays on `PB-AUDIO-OUT`; it cannot source compute or safety through a shared rail.
- Any capacitance downstream of motor-arm/E-stop is hazardous stored energy for F-12 and must meet the later discharge-time requirement.
- Do not add a large capacitor at `PB-HEAD` until converter stability, connector hot-plug, servo regeneration and E-stop discharge are jointly evaluated.
- The rig may sweep 0/470/1,000/2,200/4,700 µF at one branch at a time for sensitivity; the run records ESR, voltage rating, precharge state, inrush and discharge. This is characterization, not selection.
- Safety-controller ride-through uses the timing and capacitance method in `brownout-restart-contract.md` §6; the numeric result still waits for selected controllers/converters and measured gate/discharge timing. Only vendor decoupling and converter-required capacitance are assumed now.

## 8. Circuit-level power sequence

No exact delay is implied. Every transition advances on explicit power-good/state evidence or ends in inhibit; elapsed-time thresholds are registered later.

### 8.1 `OFF` → `OPERATE`

| Order | Required event | Branch result |
|---:|---|---|
| 1 | Connected pack passes local protection/voltage plausibility; charge input absent | `PB-MAIN` available; every downstream controlled branch remains off |
| 2 | User requests operate; system-power latch closes non-hazardous operating source | Safety converters start first; motor-arm stays open |
| 3 | C2 and base controller, if fitted, boot with hardware enables inactive | `PB-SAFE-C2`/`PB-SAFE-BASE` valid; all motion inhibited |
| 4 | Display and compute branches start; camera/audio remain profile-controlled | Application health may become available; cannot authorize motion by itself |
| 5 | C2 receives valid limits/handshake; local safety inputs and mode are current | Motor-arm becomes eligible, not automatically commanded |
| 6 | Fresh local arm request closes system motor-arm only if charge absent and no fault is latched | `PB-MOTOR` may become present through a released E-stop; controllers remain inhibited until fresh enable |
| 7 | Fresh per-controller enable and fresh action intent arrive | Only authorized head/drive outputs activate |

### 8.2 Orderly shutdown

1. Reject new motion/peak work and cancel active actions.
2. Brake/settle only as allowed by the current energy and fault state.
3. Open the system motor-arm and verify `PB-MOTOR` absent or discharged to the later registered limit.
4. Persist fault/shutdown reason; stop camera/audio/display workloads; allow SBC log flush.
5. Open application branches after their shutdown acknowledgement or timeout.
6. C2 performs final sign-off and releases the system-power latch.
7. Verify no programming, signal or charge cable leaves an unintended downstream branch powered.

### 8.3 E-stop assertion and release

- Assertion directly opens the hardware E-stop stage in `PB-MOTOR`; no SBC or firmware action is required for energy removal.
- C2/base safety remain powered, detect motor-domain loss, clear/expire pending motion and enter inhibited state.
- E-stop assertion also clears the system motor-arm latch. Physical E-stop release alone cannot restore `PB-MOTOR`; a fresh local arm action is required.
- Any later proposal allowing motor power to return solely on E-stop release would supersede this baseline and requires explicit builder approval plus F-12/F-13 re-analysis.
- Stored-energy discharge and exact stop/collapse timing are governed by `brownout-restart-contract.md`; their numeric values remain evidence-gated.

### 8.4 Charge insertion and `CHARGE`

1. Charge-present detection is hardware-visible to the system-power function and makes motor-arm closure impossible.
2. If inserted during operation, new actions are rejected and the system reaches the registered bounded terminal state; the motor-arm opens before charge mode is accepted.
3. Compute, base safety, audio, camera and microphones turn off.
4. The source selectors permit `PB-CHARGE-LOGIC` to feed only `PB-SAFE-C2` minimum supervision and `PB-DISPLAY`.
5. The charger begins only when pack presence/chemistry/temperature conditions defined by the selected charger are valid.
6. Charge removal enters motion-inhibited `OFF` or a fresh `OPERATE` boot sequence; it never returns to the prior action.

The selected circuit must define whether charge insertion causes immediate hardware motor cut or permits a short supervised brake before the motor-arm opens. Until that timing is registered, the conservative bench behavior is immediate motor-arm removal.

## 9. Registration record

| Field | Registered value |
|---|---|
| Registration | `RP02-P2-REG-02` |
| Date | 2026-09-16 |
| Builder approval | Explicit approval in the project conversation: “Pi 5 is selected so dw on that, all else is adopted” |
| Selected component | Raspberry Pi 5 2 GB as `LG-01`; selection does not authorize purchase and does not promote workload estimates to `W` |
| Relationship | Extends `RP02-P2-REG-01`; changes no registered `PA-*` or `PB-*` identifier or allowed energy route |
| Reopen rule | A different SBC/platform, distributed 3.3 V rail, use of the display battery input, weakened return/connector/protection rule, changed terminal-drop target, cross-branch bulk path, E-stop release restoring motor power, or charge source reaching motor-arm authority requires explicit supersession |

The registration freezes these implementation principles:

1. Use separate 5 V-class endpoint supplies for C2 and display; use an independent 5.1 V-class compute branch for selected Raspberry Pi 5 2 GB; do not distribute a robot-wide 3.3 V rail.
2. Treat the selected display's onboard single-cell battery/charger path as unused by Makad; feed it from `PB-DISPLAY` through the documented 5 V input.
3. The grounding, connector and conductor-calculation rules in §§3–5 form the implementation baseline; exact connector families, path lengths and gauges remain open.
4. The registered terminal-drop allocations in §5.4 are design targets pending gate registration.
5. The protection hierarchy/coordination method in §6 is adopted without selecting fuse/e-fuse values yet.
6. The branch-local capacitance policy and sensitivity sweep in §7 are adopted; final C2 hold-up and motor-bus discharge values remain evidence-gated under `brownout-restart-contract.md`.
7. The power sequence in §8 is adopted, including E-stop assertion clearing the system motor-arm latch and charge presence preventing motor-arm closure in hardware.

This registration selects the SBC platform/SKU only. It does not select or authorize purchase of the pack, servo, drive, charger, converter, connector, conductor, fuse, e-fuse or capacitor, and it does not register a numeric brownout threshold.
