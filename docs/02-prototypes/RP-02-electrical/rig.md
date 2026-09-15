# RP-02 Rig — Distribution Bench, Instrumentation, Substitutes

| Field | Value |
|---|---|
| Status | Not built. Design proposed; blocked on `workbench.md` tool arrival for anything powered, on a named RP-01 servo load for Phase B (C01 as reference unit, or later selected family), on the battery gate for Phase C |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-13 |
| Authority | `../../01-system/workbench.md` scored-test gate, PSU rule, E-stop rule, battery gate; `../../01-system/risk-prototype-plan.md` v1.12 §RP-02 rig and measurements |
| Design it realises | `power-architecture.md` §1 two-domain tree, on a bench, ugly |
| Instrument rule | `workbench.md` item 6: an instrument on the bench must resolve the gate's threshold or the run is exploratory |

Deliberately ugly, per `intuition.md`: the rig is a decision instrument. It is a plywood board with a fused distribution tree, a row of current monitors, an E-stop in the motor bus, and a place to plug real loads in as they arrive and substitutes in until they do.

## 1. Bench constraints that shape the rig

| Constraint | Consequence |
|---|---|
| **Korad KA3005D is 30 V / 5 A.** The ledger's old `E` synthetic composite at 7.4 V is 5.5–9.5 A | Per-profile characterization is fine. Full `ST-01` may exceed the supply; run only the largest recorded vector, then repeat from a protected Phase-C source. `CC-PEAK-01` is evaluated separately as the credible peak |
| The Korad is linear CV/CC with a current limit that snaps to CC | Every new branch is first energized at a limit of expected draw + margin (`workbench.md` standing rule). The CC snap is also a useful **brownout injector** for F-11 and F-16 |
| Oscilloscope deferred "until an analog problem appears" | G02's rail-excursion term is a millisecond event. Either the scope is un-deferred for Phase B, or the INA-class monitors run at their maximum conversion rate with the MCU brownout flags as the coarse indicator, and G02 rehearsals are labelled by the resolution they achieved |
| Logic analyzer probes ≤ 5 V only | Fine for UART/servo-bus decode and for the GPIO edge co-timestamping in `timebase.md` §6. **Never** on the servo or drive rail |
| No battery hardware until the written procedure, bag and balance charger exist | Phase A and B run on bench supply; G03 is a Phase C rehearsal |

## 2. Distribution board

One board, two domains, physically separated by a visible line.

| Position | Item | Notes |
|---|---|---|
| Input | Banana posts from the Korad, later XT60 from the pack; **main isolation XT60** that can be yanked | The same connector position the robot will use, so G06 review is of the real gesture |
| Main fuse holder | Blade or glass, value from the ledger | Start absurdly conservative and raise with evidence |
| Logic domain bus bar | Feeds Buck A (compute), Buck B (head logic), audio rail | Each buck on a 2.54 mm header so modules can be swapped without rewiring |
| **E-stop** | Latching mushroom in series with the motor domain bus bar | Verified working *every session* per the scored-test gate; F-12/F-13 |
| Motor domain bus bar | Servo rail regulator socket (PA-04: populated or bridged), drive rail | The socket makes "regulated from 2S" versus "direct" a plug change |
| Per-branch fuses | Polyfuse holders on Y, P, R, drive L/R, compute buck input | Values from the ledger; polyfuse drop measured during `CC-06` (PA-02 reopen condition) |
| Per-branch monitors | INA226-class high-side monitors on every branch, addressable over I²C; a shunt + scope point on the servo rail for transients | Logged by the **bench instrument MCU** (§4) |
| Test points | Voltage at the *load end* of every branch (PA-06: drop is measured at the servo connector, not the bus bar) | Labelled with the ledger's `LG-xx` codes |
| Yaw-boundary connector | The candidate demateable connector for the head branches, in line, so its drop and mating behaviour are measured from Phase B | CAD-05 |
| Sense line | Motor-domain-present signal to C2 | Required by PA-01 / `link-contract.md` F-12 |

## 3. Loads: real versus substitute

The plan permits "characterized electronic/dynamic substitutes only where their equivalence is recorded." Equivalence means writing down what the substitute reproduces and what it does not.

| Load group | Phase A | Phase B | Phase C | Equivalence record required |
|---|---|---|---|---|
| LG-01 SBC | Laptop over USB-serial standing in for the SBC **for link work only** — not an electrical load | SBC candidate, real | Real | Phase A: the laptop reproduces protocol behaviour, not power draw or boot timing; no ledger row from it |
| LG-02 C2 | **Real** — DevKitC-1-N8R8 twin, then the Zero when purchased | Real | Real | None needed; note that the DevKitC's USB-UART bridge adds ~10–20 mA the Zero does not have |
| LG-03 servos Y/P/R | Absent, or C01 (XC330-M288-T) as a named reference unit — not a family freeze | RP-01's selected family, three units, mounted on the RP-01 rig or a dummy inertia; C01 remains admissible as the reference until that freeze | Real | If a resistor/electronic load is ever used: it reproduces average current only; **it does not reproduce stall inrush, inductive kick, regenerative current on deceleration, or bus telemetry** — no G02 claim from it. C01 eManual stall is 1.80 A at 5.0 V (`D`); operating current during Layout 03 peaks is unmeasured |
| LG-04 drive | Absent | Programmable electronic load stepping a recorded profile, **or** two gearmotors of the RP-03 candidate class on a brake | RP-03 hardware if it exists | Electronic load reproduces current-time duty but not inductive/regenerative behaviour — acceptable for energy, not `CC-10A/B` transient closure |
| LG-05 display + light | **Real** when the SKU 30493 sample arrives; a 5 V resistive dummy before that | Real | Real | Dummy: average only |
| LG-06 camera | Absent | Real on the SBC candidate | Real | — |
| LG-07 mics / audio front end | Absent (negligible current) | Candidate front end | Real | — |
| LG-08 speaker + amp | Absent | Candidate class-D amp and speaker with a chirp/music file at registered level | Real | A resistor across the amp output reproduces electrical load at a fixed level; it does not reproduce the speaker's impedance versus frequency — record the level and file used |
| LG-10 base MCU / safety sensing | Absent | Absent unless RP-03 has started | RP-03 | — |

**Rule:** a ledger row sourced from a substitute carries evidence class `E` with the substitute named, never `W`.

## 4. Instrumentation

| Quantity | Instrument | Rate / resolution | Channel name | Gate |
|---|---|---|---|---|
| Branch current (all `LG-xx`) | INA226-class monitors, 16-bit, shunt sized per branch | up to ~2.8 kHz conversion; log at ≥ 1 kHz for peaks, 10 Hz for energy | `i_LGxx` | G02 invariant, ledger `W` rows, G03 |
| Servo-rail transient minimum | Oscilloscope on servo-rail load-end test point; until then INA226 at max rate with resolution stated | scope: ≥1 MS/s, single-shot on `CC-06`/`ST-01` trigger | `v_srv_min` | G02 rail-excursion term |
| Compute-rail minimum during head/whole-robot peaks | Same, second channel | — | `v_cmp_min` | PA-05 verification |
| Pack / supply voltage and current | INA226 at the input + the Korad's own display for cross-check | 1 kHz | `v_in`, `i_in` | G03; conversion-loss residual |
| Regulator, wire and connector temperature | Thermocouple or thermistor on each buck, the servo-rail conductor at the yaw connector, the connector body | 1 Hz | `T_<point>` | G02 thermal term; SC-TBD-12 |
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
3. For `CC-03/05/06`: trigger the exact gesture from the SBC via `HEAD_GOAL`; capture servo-rail and compute-rail minima.
4. Repeat with added servo-rail bulk capacitance to quantify PA-05/PA-07.
5. Report per case: profile revisions, composite waveform, per-rail minimum/maximum, component-limit margin, reset/error count and thermal trajectory.

### 5.3 Brownout ordering (PA-07 verification)

Under `CC-PEAK-01`, then the largest admissible `ST-01` vector, ramp the source down at the registered rate. Record when servo tracking degrades, C2 reports degraded, each rail reaches its limit, the SBC reports undervoltage and any reset occurs. A PA-07 ordering violation is a design finding.

### 5.4 Fault campaign (G04)

Per `fault-matrix.md` §4 order, each row in ≥ 2 registered states, ≥ 5 repetitions, with injection timestamps logged on the injecting device.

### 5.5 Runtime rehearsal (Phase C, G03)

The frozen `MD-01` on the candidate pack, per-group logging at 10 Hz for energy and 1 kHz windows around peaks, pack voltage/current continuously. Result: energy consumed, pack state at end, reserve remaining, margin against the 20-minute floor and the SC-TBD-10 reserve. Recorded as a rehearsal of SC-14, not its closure.

## 6. Safety on this rig

- E-stop in the motor domain only; verified each session.
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
