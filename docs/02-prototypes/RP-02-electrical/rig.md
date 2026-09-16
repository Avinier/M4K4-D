# RP-02 Rig — Distribution Bench, Instrumentation, Substitutes

| Field | Value |
|---|---|
| Status | Not built. Architecture and implementation basis reconciled to `RP02-P2-REG-01/02`; blocked on `workbench.md` tool arrival for anything powered, on a named RP-01 servo load for Phase B (C01 as reference unit, or later selected family), and on the battery gate for Phase C |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-16 |
| Authority | `../../01-system/workbench.md` scored-test gate, PSU rule, E-stop rule, battery gate; `../../01-system/risk-prototype-plan.md` v1.12 §RP-02 rig and measurements |
| Design it realises | `power-architecture.md` registered four-domain/`PB-*` topology plus the registered implementation rules in `power-implementation-basis.md`, with measurement ranges derived in `power-calculation-ledger.md`, on a bench, ugly |
| Instrument rule | `workbench.md` item 6: an instrument on the bench must resolve the gate's threshold or the run is exploratory |

Deliberately ugly, per `intuition.md`: the rig is a decision instrument. It is a plywood board with a protected distribution tree, a row of current monitors, explicit system motor-arm and E-stop stages, and a place to plug real loads in as they arrive and substitutes in until they do.

## 1. Bench constraints that shape the rig

| Constraint | Consequence |
|---|---|
| **Korad KA3005D is 30 V / 5 A.** The ledger's old `E` synthetic composite at 7.4 V is 5.5–9.5 A | Per-profile characterization is fine. Full `ST-01` may exceed the supply; run only the largest recorded vector, then repeat from a protected Phase-C source. `CC-PEAK-01` is evaluated separately as the credible peak |
| The Korad is linear CV/CC with a current limit that snaps to CC | Every new branch is first energized at a limit of expected draw + margin (`workbench.md` standing rule). The CC snap is also a useful **brownout injector** for F-11 and F-16 |
| Oscilloscope deferred "until an analog problem appears" | G02's rail-excursion term is a millisecond event. Either the scope is un-deferred for Phase B, or the INA-class monitors run at their maximum conversion rate with the MCU brownout flags as the coarse indicator, and G02 rehearsals are labelled by the resolution they achieved |
| Logic analyzer probes ≤ 5 V only | Fine for UART/servo-bus decode and for the GPIO edge co-timestamping in `timebase.md` §6. **Never** on the servo or drive rail |
| No battery hardware until the written procedure, bag and balance charger exist | Phase A and B run on bench supply; G03 is a Phase C rehearsal |

## 2. Distribution board

One board with the four `PA-01` failure-consequence domains physically separated and every node labelled by its registered `PB-*` key. The rig preserves the architecture's source-selection and return paths; it does not imply that all eventual circuits occupy one PCB.

| Position | Item | Notes |
|---|---|---|
| `PB-MAIN` source fixture | Banana posts from the Korad, later the selected pack connector; removable main isolation and a replaceable protection position | Uses the intended isolation gesture for G06. Bench-supply and pack sources are mutually exclusive |
| `PB-CHARGE-IN` fixture | Separate protected low-voltage input position plus charger/load-sharing socket | Cannot be jumpered to the operating or motor buses; supports pack-present/absent and backfeed tests |
| Source/state panel | Keyed `OFF/OPERATE/CHARGE` selection, operating-source latch fixture and visible state indication | Implements `PA-14`; invalid source combinations are physically prevented |
| Safety domain | Independent sockets and protection positions for `PB-SAFE-C2` and `PB-SAFE-BASE` | No shared regulator fault; charge source may reach C2 only through the bounded selector; base safety is off in charge |
| Application domain | Separate sockets/protection positions for `PB-COMPUTE`, `PB-DISPLAY`, `PB-AUDIO-OUT`, and source-dependent `PB-CAMERA`/`PB-AUDIO-IN` | Converter modules can be swapped without changing branch identity; display alone may receive the restricted charge source |
| System motor-arm | Normally-off switching fixture between operating source and E-stop | Drops `PB-MOTOR` in system `OFF`, boot inhibit and charge even when the mushroom is released |
| **Hardware E-stop** | Latching mushroom electrically dominant over the motor-arm command and in series with `PB-MOTOR` | Verified working *every session*; assertion removes head and drive energy while supervision remains available; F-12/F-13 |
| Hazardous motor domain | `PB-HEAD` and `PB-DRIVE` sockets downstream of `PB-MOTOR`; direct-feed/converter positions as required | Makes a later direct-versus-converted choice a module change without bypassing arm/E-stop authority |
| Final branches | Independent protection/measurement positions for `PB-HEAD-Y/P/R` and `PB-DRIVE-L/R` | Protection technology remains open; each path is observable and fault-injectable |
| Return star | Source-adjacent star with paired outgoing/return paths for safety, application, head and drive branches | No daisy-chain through application or actuator loads; removable links permit return-drop measurement |
| Per-branch monitors | INA226-class high-side monitors or range-appropriate shunts on each `PB-*` branch; scope points on compute, safety and motor load ends | Exact device/range is selected only after the contract is numerically populated; logged by the bench instrument MCU (§4) |
| Test points | Source and load-end voltage on every populated branch; return-drop points; pre/post motor-arm and E-stop points | Dual-labelled with `PB-*` and owning `LG-*`; head-axis drop is measured at each servo connector |
| Yaw-boundary connector | The candidate demateable connector for the head branches, in line, so its drop and mating behaviour are measured from Phase B | CAD-05 |
| Sense lines | Independently derived motor-energy-present, operating-source, charge-source and pack-state signals to the appropriate supervisor | Sense wiring cannot back-power a de-energized branch; required by `PA-10`, `PA-13`, `PA-14` and F-12/F-18 |

## 3. Loads: real versus substitute

The plan permits "characterized electronic/dynamic substitutes only where their equivalence is recorded." Equivalence means writing down what the substitute reproduces and what it does not.

| Load group | Phase A | Phase B | Phase C | Equivalence record required |
|---|---|---|---|---|
| LG-01 Raspberry Pi 5 2 GB | Laptop over USB-serial standing in for the SBC **for link work only** — not an electrical load | Selected Pi 5 with active cooler and intended storage/peripherals | Same selected configuration | Phase A: the laptop reproduces protocol behaviour, not power draw or boot timing; no ledger row from it |
| LG-02 C2 | **Real** — DevKitC-1-N8R8 twin, then the Zero when purchased | Real | Real | None needed; note that the DevKitC's USB-UART bridge adds ~10–20 mA the Zero does not have |
| LG-03 servos Y/P/R | Absent, or C01 (XC330-M288-T) as a named reference unit — not a family freeze | RP-01's selected family, three units, mounted on the RP-01 rig or a dummy inertia; C01 remains admissible as the reference until that freeze | Real | If a resistor/electronic load is ever used: it reproduces average current only; **it does not reproduce stall inrush, inductive kick, regenerative current on deceleration, or bus telemetry** — no G02 claim from it. C01 eManual stall is 1.80 A at 5.0 V (`D`); operating current during Layout 03 peaks is unmeasured |
| LG-04 drive | Absent | Programmable electronic load stepping a recorded profile, **or** two gearmotors of the RP-03 candidate class on a brake | RP-03 hardware if it exists | Electronic load reproduces current-time duty but not inductive/regenerative behaviour — acceptable for energy, not `CC-10A/B` transient closure |
| LG-05 display + light | **Real** when the SKU 30493 sample arrives; a 5 V resistive dummy before that | Real | Real | Dummy: average only |
| LG-06 camera | Absent | Real on selected Raspberry Pi 5 2 GB | Real | — |
| LG-07 mics / audio front end | Absent (negligible current) | Candidate front end | Real | — |
| LG-08 speaker + amp | Absent | Candidate class-D amp and speaker with a chirp/music file at registered level | Real | A resistor across the amp output reproduces electrical load at a fixed level; it does not reproduce the speaker's impedance versus frequency — record the level and file used |
| LG-10 base MCU / safety sensing | Absent | Absent unless RP-03 has started | RP-03 | — |

**Rule:** a ledger row sourced from a substitute carries evidence class `E` with the substitute named, never `W`.

## 4. Instrumentation

| Quantity | Instrument | Rate / resolution | Channel name | Gate |
|---|---|---|---|---|
| Branch current (all `LG-xx`) | INA226-class monitors, 16-bit, shunt sized per branch | up to ~2.8 kHz conversion; log at ≥ 1 kHz for peaks, 10 Hz for energy | `i_LGxx` | G02 invariant, ledger `W` rows, G03 |
| Head-axis transient minimum | Oscilloscope on the active `PB-HEAD-Y/P/R` load-end test point; until then INA-class monitor at maximum rate with resolution stated | scope: ≥1 MS/s, single-shot on `CC-06`/`ST-01` trigger | `v_head_<axis>_min` | G02 rail-excursion term |
| Compute and safety minima during head/whole-robot peaks | Scope at `PB-COMPUTE` and then `PB-SAFE-C2`/`PB-SAFE-BASE` load ends | — | `v_compute_min`, `v_safe_c2_min`, `v_safe_base_min` | PA-05/PA-11 verification |
| Pack / supply voltage and current | INA226 at the input + the Korad's own display for cross-check | 1 kHz | `v_in`, `i_in` | G03; conversion-loss residual |
| Converter, conductor and connector temperature | Thermocouple or thermistor on each populated converter/protection device, the head conductor at the yaw connector, and the connector body | 1 Hz | `T_<point>` | G02 thermal term; SC-TBD-12 |
| Reset / brownout events | MCU reset-reason registers read at boot and logged; SBC `dmesg`/journal | event | `evt_reset_<board>` | G02, G04 |
| Link errors | `crc_err_count`, `NACK` reasons, `last_rx_age` from `HEARTBEAT` | 20 Hz | `link_*` | G04, G05 |
| Loop timing on C2 | `loop_jitter_us_p99` self-report **plus** a GPIO toggled per tick, captured by the logic analyzer for an independent measurement | tick rate | `c2_tick` | G05 |
| Timestamp reconciliation | GPIO edge commanded at a master timestamp, captured on the analyzer alongside `c2_tick` (`timebase.md` §6) | event | `sync_edge` | G05 |
| Bench instrument MCU | The Nano 33 BLE Sense or a second DevKitC-1 reading the INA226 chain and thermistors, streaming CSV with run ID and master time | — | — | Bench equipment per `workbench.md`; not robot hardware |

Every instrument entry gets sampling rate, calibration/check method, uncertainty and run-record channel name **before** scored use. The INA226 shunts are checked against the Korad's CC readout at 0.5 A and 2 A at session start.

## 5. Procedures

### 5.1 Per-group characterization (Phase A/B, exploratory → ledger rows)

1. Branch alone on the Korad, current limit set; execute its named `LP-xx-*` profiles from `load-model.md`, including the required transient and sustained windows.
2. Enter the row in the ledger as `W` with run ID, conditions and the firmware/config identity.

### 5.2 Coexistence rehearsal (Phase B/C, pilot → scored against the G02 invariant)

1. Verify E-stop; set limits for this test; confirm logging; allocate the run ID.
2. Bring up the registered `CC-xx` case one group/profile at a time; log the composite and exact event alignment.
3. For `CC-03/05/06`: trigger the exact gesture from the SBC via `HEAD_GOAL`; capture `PB-HEAD-Y/P/R`, `PB-COMPUTE` and `PB-SAFE-C2` load-end minima.
4. Repeat with controlled head-branch bulk capacitance to quantify transient sensitivity and feed the numeric brownout/hold-up calculation. Capacitance is not selected by this experiment alone.
5. Report per case: profile revisions, composite waveform, per-rail minimum/maximum, component-limit margin, reset/error count and thermal trajectory.

### 5.3 Brownout ordering (PA-07 verification)

Use the preregistered source/load/threshold configuration from `brownout-restart-contract.md` §8; do not tune thresholds inside a scored run.

1. Under `CC-13H` and `CC-13D`, ramp the source slowly through `EN-02`; verify new peaks are rejected, the active action/arm epoch is cancelled and motion reaches its bounded stop.
2. Continue the slow path through `EN-03/CC-14`; verify non-safety loads shed, motor permission and local enables become inactive before any safety controller becomes unreliable, motor-bus discharge is confirmed and SBC shutdown never delays the safe state.
3. Repeat with the largest then-admissible `CC-PEAK-01`, then `ST-01`, while recording that synthetic alignment is a stress case rather than representative duty.
4. Apply the preregistered fast step/collapse; verify `ENERGY_OK`/local readiness fail inactive and hardware/local motor inhibit acts without waiting for the SBC or graceful shutdown.
5. Restore source around both clear thresholds, then cycle C2/base/SBC reset, battery reconnection, E-stop and charge insertion/removal; verify zero old action replay and that motion requires a fresh mode/arm/enable/action sequence.

Capture source and branch voltages, source current, `ENERGY_OK`, motor-arm gate, local driver enables, controller reset/PG, motor-bus voltage and event timestamps on one time-correlated record. A `PA-07`/`BR-*` ordering violation is a design finding, not permission to relax a threshold after seeing the data.

### 5.4 Fault campaign (G04)

Per `fault-matrix.md` §4 order, each row in ≥ 2 registered states, ≥ 5 repetitions, with injection timestamps logged on the injecting device.

### 5.5 Runtime rehearsal (Phase C, G03)

The frozen `MD-01` on the candidate pack, per-group logging at 10 Hz for energy and 1 kHz windows around peaks, pack voltage/current continuously. Result: energy consumed, pack state at end, reserve remaining, margin against the 20-minute floor and the SC-TBD-10 reserve. Recorded as a rehearsal of SC-14, not its closure.

## 6. Safety on this rig

- The hardware E-stop dominates the motor-arm path and removes only hazardous motor energy; verified each session.
- `OFF` is tested separately: a released E-stop must not leave `PB-MOTOR` energized when the system-power latch is off.
- Korad current limit set before every new branch is energized.
- Servos under test are mounted on the RP-01 rig or clamped with a dummy inertia — never loose on the bench.
- No pack work until the `workbench.md` battery gate is satisfied; the written procedure is produced before first use and not edited during the session; bag, non-flammable surface, never unattended.
- Thermal limits registered before any sustained run; stop on smoke, odour, swelling, temperature beyond the registered limit, or repeated unexplained reset (portfolio stop rules).

## 7. Readiness checklist state

*(mirror of the `workbench.md` scored-test gate for this rig; all must pass before any scored run)*

- [ ] E-stop verified working this session
- [ ] Current, voltage, temperature and timeout limits set for this specific test
- [ ] Servos/loads restrained
- [ ] Firmware/software/config/rig revision recorded
- [ ] Logging confirmed writing with the run ID in the log
- [ ] The transient instrument on the bench resolves the registered rail-excursion threshold (or the run is exploratory)
