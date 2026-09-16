# RP-02 Power Branch Contract Register

| Field | Value |
|---|---|
| Status | **Accepted derived branch-side `EDB-03` issue v0.4, builder-reviewed 2026-09-16.** Uses branch keys registered under `RP02-P2-REG-01`, consumes implementation baseline `RP02-P2-REG-02`, and points to the v0.1 calculation issue. It adds no energy route or other component selection; numeric evidence remains ledger-owned. |
| Created | 2026-09-16 |
| Authority | Approved `electrical-design-basis.md`; registered `power-architecture.md` v0.2; registered Part-1 `CC/LP/F` baseline |
| Numeric source | Inputs: `../../01-system/power-energy-ledger.md`; derivations: `power-calculation-ledger.md` |
| Purpose | Define the electrical contract each registered `PB-*` path must eventually satisfy and identify which inputs block calculation, sourcing or qualification |

## 1. Contract rules

1. A branch ID names one intentional energy path. Signal pins, shields, test equipment and programming connections may not create unnamed parallel paths.
2. Source and load boundaries include both positive and return paths.
3. Branch envelopes are calculated per registered `CC-*`; independent maxima are aligned only in `ST-01`.
4. Protection, connector and conductor ratings are not inferred from average power.
5. `OFF` is demonstrated at the stated load boundary; an open upstream switch does not prove absence of downstream stored or backfed energy.
6. A branch with any unresolved non-zero load, loss, source impedance or protection behavior remains `U` for the affected calculation.
7. Every selected part or measured waveform re-evaluates the applicable branch and its upstream parents.

## 2. Source and charging branches

### `PB-MAIN` — Protected battery operating source

| Field | Contract |
|---|---|
| Source/destination | Pack-integral protection and removable pack connector through the adjacent main fuse to the battery source node feeding system-power control and motor-arm input |
| Loads/classes | Parent of all `EC-S`, `EC-C`, `EC-N` operating loads and `EC-H` motor loads; also interfaces with the charger battery port |
| Permitted states | Present with a connected pack in `OFF`, `OPERATE` and supported charging states; downstream system and motor branches enforce their own permissions |
| Electrical envelope | Full-to-depleted loaded pack voltage; total registered operating current; credible/source peak from `CC-PEAK-01`; synthetic bound from `ST-01`; regeneration; fault current; all values ledger-owned |
| Default/switching | Pack removal opens the source. System `OFF` opens all RP-02 load paths downstream except documented pack/charger quiescent behavior. |
| Protection | Pack-integral protection plus adjacent main fuse; main protection must coordinate with downstream branches without depending on software |
| Return | Pack return enters the central 0 V distribution node through the selected measurement arrangement; no structure/shield return |
| Measurement | Pack-terminal signed `V/I`, main-source voltage after fuse/connector, pack temperature/protection state and connector/fuse temperature |
| Trace | All operating `CC`; `CC-13H/D`, `CC-14`, `MD-01`, `CC-PEAK-01`, `ST-01`; F-11/F-16/F-18; G01/G02/G03/G06 |
| Open inputs | Pack architecture, internal resistance versus state/age/temperature, regeneration acceptance, fault-current limit, connector/fuse and all downstream case aggregates |

### `PB-CHARGE-IN` — Protected external low-voltage input

| Field | Contract |
|---|---|
| Source/destination | Certified external AC/DC adapter output through keyed robot inlet and input protection to the onboard charger/power path |
| Loads/classes | Charger input, pack charging and restricted charge-logic output; `EC-Q` |
| Permitted states | Physically absent in untethered operation; accepted only into `OM-06/EN-04`; insertion during operation invokes the registered bounded-entry policy before charging is accepted |
| Electrical envelope | Adapter voltage/current/tolerance, hot-plug inrush, charger demand, charge-display/minimum-supervision load and fault current; all `U` pending chemistry/topology implementation |
| Default/switching | No connector means no intentional input energy. Incorrect/reversed/partial mating cannot energize an uncontrolled path. |
| Protection | Keying, reverse-polarity/backfeed control, input-current/fault containment and strain relief; exact mechanisms open |
| Return | Charge return joins only at the approved charger/source node; it cannot bypass pack isolation or become a motor return |
| Measurement | Input signed `V/I`, inlet voltage, insertion/removal timestamps and connector/charger temperature |
| Trace | `CC-15`, F-18; G01/G02/G04/G06 |
| Open inputs | Adapter/charger/connector/chemistry selection, pack-present behavior, input limits and insertion policy timing |

### `PB-CHARGE-LOGIC` — Restricted charging logic source

| Field | Contract |
|---|---|
| Source/destination | Supported system/load-sharing output of the charger/power path to the C2 and display source selectors only |
| Loads/classes | `PB-SAFE-C2` minimum supervision and `PB-DISPLAY` charge profile; `EC-Q` supplying `EC-S/EC-N` |
| Permitted states | `CHARGE` only; cannot source compute, base safety, audio, camera, microphones or any motor-energy branch |
| Electrical envelope | Sum of `LP-02-IDLE`, required charge/pack supervision and `LP-05-CHARGE`, plus conversion loss and transition/inrush; numeric result `U` until charger/display/C2 paths are bound |
| Default/switching | Source selector rejects reverse flow and prevents charge logic from reaching the operating or motor bus. Charger/status loss produces bounded fault state. |
| Protection | Own current limit/branch protection appropriate to C2 and display downstream branches; one display fault cannot collapse C2 |
| Return | Returns to the charger/source star node; display current does not flow through the C2 return |
| Measurement | Charge-logic source `V/I`, C2/display terminal voltages, transition minimum/maximum and temperatures |
| Trace | `CC-15`, F-07/F-18; G01/G02/G04/G06 |
| Open inputs | Charger load-sharing implementation, source selector, display charge demand, minimum-supervision contents and battery-present behavior |

## 3. Safety-supervision branches

### `PB-SAFE-C2` — Independent C2 safety supervision

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` in `OPERATE` or `PB-CHARGE-LOGIC` in `CHARGE`, through an exclusive/bounded source selector, dedicated converter, protection and paired conductors to `LG-02` |
| Loads/classes | C2, servo-bus transceiver and assigned pack/E-stop/rail sensing; `EC-S` |
| Permitted states | Boot, all operating/inhibited/hard-stop states, low/critical state until terminal shutdown, and minimum charging supervision; `OFF` only after final sign-off or source isolation |
| Electrical envelope | `LP-02-BOOT/IDLE/TRAJ/LINKSTRESS/FAULT` plus assigned sensors. Exact terminal range, reset threshold, transient and hold-up are `U/D` pending source registration. |
| Default/switching | Boot/reset always inhibited. Source transfer may reset only if the resulting state remains safe and observable; seamless transfer is not assumed. |
| Protection | Dedicated converter and branch protection. Display, SBC, base safety and both motor paths cannot trip/reset it through a downstream shared device. |
| Return | Dedicated paired return to central 0 V node; servo-bus signal reference carries no servo power current |
| Measurement | Source/load terminal `V/I`, power-good, reset reason, C2/transceiver temperature and `TB-1/2` transition captures |
| Trace | `CC-01…18`, `CC-PEAK-01`, `ST-01`, `MD-01`; F-01…08/F-11…18; G01/G02/G04/G05 |
| Open inputs | C2 board/transceiver `D/W`, assigned sensors, converter/source selector, hold-up/UVLO requirements and input-source envelopes |

### `PB-SAFE-BASE` — Independent base safety supervision

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` operating source through dedicated converter, protection and paired conductors to `LG-10` |
| Loads/classes | Base MCU and motion-critical obstacle/edge sensing; `EC-S` when its evidence is a motion precondition |
| Permitted states | Boot/operate and tabletop safety/calibration as required; remains valid while base motor energy is present or being removed; off in `CHARGE` and after final shutdown |
| Electrical envelope | `LP-10-BOOT/IDLE/MOTION/OBSTACLE/EDGE/FAULT`; sensor emitter pulse alignment included; values `U` until RP-03 |
| Default/switching | Boot/reset holds drive disabled. App/SBC loss, controller reset or missing safety evidence cannot leave the driver enabled. |
| Protection | Dedicated converter/branch independent of C2 and drive power stage; its short/reset cannot disturb C2 safety supervision |
| Return | Dedicated paired return to central 0 V node; no motor current in sensor/controller references |
| Measurement | Terminal `V/I`, power-good/reset reason, sensor-age/validity, driver-enable state and temperatures |
| Trace | Drive/tabletop cases; F-17/F-19/F-22; G01/G02/G04/G05 |
| Open inputs | Entire RP-03 controller/sensor configuration, supply/UVLO, driver-enable implementation and measured profiles |

## 4. Application branches

### `PB-COMPUTE` — Main compute

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` operating source through dedicated switch/protection/converter to `LG-01`; selected camera/audio-input loads may be downstream |
| Loads/classes | SBC `EC-C`; downstream `LG-06/07` remain separately attributable |
| Permitted states | Boot and ordinary operating cases; may be shed only by registered policy; off in charging and final shutdown |
| Electrical envelope | Registered 5.1 V nominal endpoint and 5 A interface capability for selected Raspberry Pi 5 2 GB; per `LP-01-*` and attached-load profiles. Workload current, inrush, ripple response and exact undervoltage margin remain `E/U/W`. |
| Default/switching | Cold start cannot authorize motion. Controlled shutdown precedes branch opening when energy permits. Restart enters motion inhibit. |
| Protection | Dedicated converter/branch; no downstream application or SBC input fault resets safety branches; programming/USB/CSI/UART back-power prevented |
| Return | Paired return to application distribution/star; audio/display currents do not daisy-chain through it |
| Measurement | SBC-terminal and converter-input `V/I`, power-good/undervoltage/reset logs and regulator/board temperature |
| Trace | Applicable `CC-01…14/17/18`, peaks and `MD-01`; F-01/F-02/F-10/F-15/F-17/F-20; G01/G02/G03/G04 |
| Open inputs | Power-entry/PD-current implementation, RP-07 workload, downstream camera/microphone arrangement, converter and clean-shutdown/latch behavior |

### `PB-DISPLAY` — Display and status

| Field | Contract |
|---|---|
| Source/destination | Operating or restricted charge source through bounded selector, dedicated protection/conversion and head harness to `LG-05` |
| Loads/classes | Display board and status light; `EC-N` |
| Permitted states | Dim/active/utility/music/failure profiles in operation; `LP-05-CHARGE` in charging; off after final shutdown |
| Electrical envelope | Manufacturer-backed 5 V, 450 mA nominal board point (`D`) plus `LP-05-*`, including unmeasured boot/wake inrush, brightness profiles, status light and full-reference stress (`U/E/W`). |
| Default/switching | May reset/darken without hazardous effect. Expired semantic state decays safely. Charge display operates without SBC. |
| Protection | Independent from C2. Display short/inrush cannot reset C2 or reach motor path; UART/programming paths cannot back-power either side. |
| Return | Dedicated paired head return; not shared as C2 or servo load conductor |
| Measurement | Source/load `V/I`, reset/status, brightness/FPS, board/backlight/connector temperatures and wake/transfer transients |
| Trace | Display-bound cases, `CC-15`, peaks and `MD-01`; F-07/F-13/F-18; G01/G02/G04/G06 |
| Open inputs | Sample power data, status light, source selector, connector/harness and charging brightness/profile |

### `PB-AUDIO-OUT` — Amplifier and speaker

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` operating source through independent switching/protection and selected conversion to `LG-08` |
| Loads/classes | Amplifier/speaker; `EC-N` |
| Permitted states | Registered chirp/alarm/music/idle cases; off in charging and final shutdown; safety pre-emption cannot wait on audio completion |
| Electrical envelope | Quiescent, authored RMS, crest width/repetition, alarm duty and startup/pop transient; all `U/E` until RP-05/06 candidate and levels |
| Default/switching | Mute/off must be deterministic. Restoration cannot replay cancelled audio/action. |
| Protection | Short/overload/noise cannot reset safety branches or corrupt control; branch combination with compute/display requires later evidence and explicit supersession |
| Return | Paired return to application star; speaker current does not flow through compute/safety references |
| Measurement | Input `V/I`, amplifier/speaker temperature, file/gain/load and synchronized crest captures |
| Trace | `CC-03/06/07C/08/17/18`, peaks and `MD-01`; F-10/F-20; G01/G02/G03 |
| Open inputs | Amplifier/speaker/rail selection, acoustic level, efficiency, thermal boundary and noise result |

### `PB-CAMERA` — Camera downstream path

| Field | Contract |
|---|---|
| Source/destination | Selected SBC camera connector/rail through controlled-impedance harness to `LG-06` |
| Loads/classes | Camera Module 3 Wide; `EC-N`, operationally required for tracking cases |
| Permitted states | Stream/track/AF profiles only; stream disabled in quiet sleep and charging; off after shutdown |
| Electrical envelope | Camera/interface voltage/sequence, stream RMS, AF and startup transient; `U` until official/integrated evidence |
| Default/switching | Loss invalidates track evidence and stops dependent motion; non-hot-pluggable behavior follows selected interface |
| Protection | Camera/cable fault cannot back-power compute or safety/motor branches; CSI shield is not a power return |
| Return | Vendor-defined camera/CSI reference and shield path, bounded relative to compute return |
| Measurement | Separately instrumented where practical; otherwise synchronized compute-branch delta with declared uncertainty |
| Trace | Camera/tracking cases; F-09; G02/G04 |
| Open inputs | SBC/interface selection, exact cable, vendor sequence/current and measurement feasibility |

### `PB-AUDIO-IN` — Microphone/front-end path

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` application source or `PB-COMPUTE` downstream interface, determined by RP-05 selection, to `LG-07` |
| Loads/classes | Microphones/front end; `EC-N` |
| Permitted states | Listen/capture/fault profiles in registered cases; off during charging and final shutdown |
| Electrical envelope | Quiescent/listen/capture, interface/DSP startup and any USB burst; `U/E` pending front-end selection |
| Default/switching | Missing/stale input produces no wake/intent; restoration accepts only fresh audio |
| Protection | No USB/I2S/backfeed path may power an off SBC or safety branch; interface noise cannot corrupt motor-control links |
| Return | Paired/local return according to selected interface; microphone reference is not an audio-output or motor return |
| Measurement | Direct branch `V/I` where separate, otherwise compute-source delta; availability/frame-age logs |
| Trace | `CC-02F/T`, request/music cases; F-21; G02/G04 |
| Open inputs | RP-05 selection, SBC interface, power location, synchronized channel requirements and back-power behavior |

## 5. Hazardous motor branches

### `PB-MOTOR` — System-armed, E-stop-gated motor-energy bus

| Field | Contract |
|---|---|
| Source/destination | `PB-MAIN` battery source through system motor-arm gate and dominant hardware E-stop switching function to `PB-HEAD` and `PB-DRIVE` |
| Loads/classes | Parent of all `EC-H` head and drive energy paths |
| Permitted states | Absent in system `OFF`, boot inhibit, hard stop and charging; available only after `OPERATE`, E-stop release and required local readiness; availability never equals motion authorization |
| Electrical envelope | Aggregate aligned head/drive current, conversion inrush, regeneration/rail rise, stored energy and fault current; credible peak `CC-PEAK-01`, separate `ST-01` |
| Default/switching | Motor-arm and E-stop are series permissions. Either open removes upstream motor energy. Restoration leaves all controllers/drivers inhibited. |
| Protection | Main/branch coordination; selected E-stop device must interrupt the DC fault/load class or command a de-energize-to-open power device with bounded failure behavior |
| Return | High-current head/drive returns go independently to central source return; E-stop need not interrupt return unless selected safety analysis requires it |
| Measurement | Bus `V/I`, motor-arm/E-stop states, downstream discharge time, switching temperature and transition capture |
| Trace | All motor cases; F-11…13/F-16/F-22; G01/G02/G04/G06 |
| Open inputs | Head/drive waveforms, gate/E-stop implementation, stored-energy limit, regeneration sink and protection/fault-current calculations |

### `PB-HEAD` — Head-actuator upstream

| Field | Contract |
|---|---|
| Source/destination | `PB-MOTOR` through selected direct feed or high-current conversion to three head-axis branches |
| Loads/classes | `LG-03Y/P/R`; `EC-H` |
| Permitted states | Authorized head-motion/hold cases only; torque unavailable in quiet sleep, hard stop and charging; settle only where registered |
| Electrical envelope | Aligned per-axis RMS/peaks, restoration inrush, braking/regeneration, converter loss/thermal and terminal-drop demand; `U/D` until RP-01 selection/measurement |
| Default/switching | Converter/direct path cannot power servos at system boot. Restoration occurs with C2 inhibited and zero stored goal. |
| Protection | Upstream protection plus selected per-axis containment; one-axis fault must not cause remaining-axis runaway or reset C2 |
| Return | Dedicated paired feed/return across yaw boundary; C2/bus reference carries no actuator return current |
| Measurement | Upstream signed `V/I`, converter temperature and per-axis load-end observations |
| Trace | Head-motion cases, peaks and `MD-01`; F-06/F-08/F-11…13/F-16; G01/G02/G04/G05/G06 |
| Open inputs | Servo family/rail, converter/direct choice, bus, moving harness, allowed sag and all real profiles |

### `PB-HEAD-Y/P/R` — Individual head-axis branches

| Field | Contract |
|---|---|
| Source/destination | `PB-HEAD` distribution point through each axis's selected containment/interconnect to its servo terminal |
| Loads/classes | `LG-03Y`, `LG-03P`, `LG-03R`; each `EC-H` |
| Permitted states | Axis-specific bound `LP-03-*`; all three separately remain `OFF`/torque unavailable where required |
| Electrical envelope | Per-axis hold/RMS/peak/width/slew/inrush/regeneration/stall-reference; no combined-axis averaging before protection/drop analysis |
| Default/switching | An absent/silent axis cannot be energized by stale goal after reconnection; other axes execute bounded brake/inhibit policy |
| Protection | Protection class/value open. Per-axis observability is mandatory; independent fuse/PTC is not presumed until drop/clearing analysis. |
| Return/interconnect | Each terminal calculation includes positive and return conductors, contacts and moving-harness resistance |
| Measurement | Per-axis signed current, load-terminal voltage, temperature and position/health telemetry |
| Trace | Applicable head cases; F-08/F-11/F-13; G01/G02/G04/G05 |
| Open inputs | Exact servo `D/W`, conductor/connector geometry, branch protection and admissible terminal margin |

### `PB-DRIVE` — Drive-stage upstream

| Field | Contract |
|---|---|
| Source/destination | `PB-MOTOR` through direct/conversion path to selected motor driver and left/right outputs |
| Loads/classes | `LG-04` driver and motors; `EC-H` |
| Permitted states | Floor locomotion and caught `CC-12C` calibration only; off/inhibited in tabletop ordinary operation, motion inhibit, hard stop, charging and final off |
| Electrical envelope | Driver quiescent/control load plus steady, launch, reversal, brake, spin and blocked-reference waveforms; signed regeneration; entirely `U/E` pending RP-03 |
| Default/switching | Hardware driver enable defaults inactive and remains inactive across base reset, missing sensor evidence, app loss and power restoration |
| Protection | Drive fault cannot reset base/C2 safety supplies; regeneration has explicit sink/clamp behavior for full/disconnected pack cases |
| Return | Driver/motor high-current return directly to central source node, separate from base-safety return |
| Measurement | Driver-input signed `V/I`, enable/rail state, temperature and per-channel current where required |
| Trace | `CC-09…14`, peaks and `MD-01`; F-12/F-13/F-16/F-17/F-19/F-22; G01/G02/G03/G04 |
| Open inputs | Entire RP-03 motor/driver/control/mechanical load and regenerative evidence |

### `PB-DRIVE-L/R` — Individual drive outputs

| Field | Contract |
|---|---|
| Source/destination | Motor-driver output stages and wiring to left/right motors |
| Loads/classes | Left and right portions of `LG-04`; `EC-H` |
| Permitted states | Exact RP-03 wheel commands within a legal `PB-DRIVE` state |
| Electrical envelope | Signed phase/output current, PWM/commutation conditions, launch/reversal/brake/stall reference and wiring loss; `U` |
| Default/switching | Driver disable produces selected safe output state; controller reset cannot leave one wheel commanded |
| Protection | Channel fault containment and upstream coordination defined after driver selection; one channel fault cannot command the other |
| Return/interconnect | Motor leads/returns sized and routed as a high-current/noise path, separate from encoders/safety references |
| Measurement | Per-channel current/voltage where instrumentable, encoder response and motor/wire/connector temperature |
| Trace | Drive cases; F-22 and future RP-03 motor faults; G01/G02/G04 |
| Open inputs | Driver topology, motors, PWM/control method, harness and RP-03 stopping/regeneration requirements |

## 6. Calculation model

For branch `b` in registered case `c`, the calculation preserves the aligned waveform:

`i_b,c(t) = Σ i_load,c(t) + i_branch-loss,c(t)`

For a converting branch:

`P_in,b,c(t) = P_out,b,c(t) / η_b(V_in, I_out, T)`

For a terminal path:

`V_terminal,c(t) = V_source,c(t) − i_b,c(t)·(R_positive + R_return) − ΣV_device-drop,c(t)`

For an interval:

`E_b,c = ∫ v_b,c(t)·i_b,c(t) dt`

Rules:

- `CC-PEAK-01` uses registered credible onset alignment.
- `ST-01` deliberately aligns its synthetic profiles and is reported separately.
- RMS/mean over the appropriate `TB-3/4` window drives thermal work; the largest sample does not.
- Reverse current remains signed through pack, converter, driver and overvoltage checks.
- Component-terminal margin is calculated after source, protection, switch, connector, conductor and return losses.
- An `E` planning range cannot close a rating or gate; it can identify an infeasible candidate or the required sourcing envelope.

## 7. Current calculation readiness

| Branch | Current evidence state | What can be calculated now | Principal blocker |
|---|---|---|---|
| `PB-MAIN` | System case totals `E/U` | Coarse rig/source envelope and dependency sensitivity | Real head/drive/compute/audio profiles and pack impedance |
| `PB-CHARGE-IN/LOGIC` | `U` | Required equations and measured channels only | Charger, chemistry, charge display and supervision implementation |
| `PB-SAFE-C2` | Input range/source capability `D`; load profiles `E`, sensing/transceiver partly `U` | Preliminary 5 V endpoint/path comparison; no hold-up margin | Installed-board/transceiver `W`, reset threshold and converter/source selector |
| `PB-SAFE-BASE` | `U/E` | Planning class only | RP-03 |
| `PB-COMPUTE` | Raspberry Pi 5 2 GB selected; input interface `D`, workload `E` | 5.1 V/5 A path, connector and converter candidate screening | Exact power entry and workload `W` |
| `PB-DISPLAY` | Selected board 5 V/450 mA nominal `D`; profiles `U/E` | 5 V endpoint, conductor and instrument planning | Sample `W`, inrush, brightness, status light and charge profile |
| `PB-AUDIO-OUT` | `U/E` | Candidate class only | RP-05/06 hardware and authored level |
| `PB-CAMERA` | Selected device, demand `U/E` | Correlated measurement plan | SBC integration and official/sample evidence |
| `PB-AUDIO-IN` | `U/E` | Alternative source-path comparison | RP-05 front-end choice |
| `PB-MOTOR` / `PB-HEAD` | Servo family `U`, C01 stall `D` | Sensitivity/reference bound only | RP-01 family and `W` waveforms |
| `PB-HEAD-Y/P/R` | C01 stall `D`; operating profiles `U` | Per-axis reference fault bound | RP-01 selection/measurements and harness |
| `PB-DRIVE` / `PB-DRIVE-L/R` | Class estimate `E`; real system `U` | Substitute forward-current rig envelope only | RP-03 real drive and regenerative profiles |

### 7.1 Provisional arithmetic from the current ledger

These are transparent consequences of the existing `E/D` planning rows, not new source facts or ratings. Ranges use independent endpoints only where stated; they do not assert that those endpoints coexist in a credible `CC-*` case.

| Branch observation | Arithmetic | Derived planning result | Use and limit |
|---|---|---:|---|
| `PB-COMPUTE` selected-Pi workload current estimate | `(10…12 W) / 5.1 V` | `1.96…2.35 A` peak-load estimate | Useful for instrument range and candidate screening only. The registered 5.1 V nominal / 5 A interface capability is not measured consumption. |
| `PB-DISPLAY` candidate 5 V peak current | `(3.0…3.5 W) / 5 V` | `0.60…0.70 A` | Sample/official data, brightness and source-transfer inrush remain open. |
| C01 single-axis stall reference | `5 V × 1.80 A` | `9.0 W` per axis | `D` reference for protected bench stress; not an operating profile or selected servo. |
| C01 three-axis coincident stall reference | `3 × 1.80 A`; `5 V × 5.40 A` | `5.40 A`, `27.0 W` at head terminals | Synthetic/fault reference only. It cannot set a fuse, converter or conductor rating without duration, source/path impedance and protection behavior. |
| Historical 2S `ST-01` source-equivalent current | `40 W / 8.4 V` to `70 W / 6.0 V` | `4.8…11.7 A` idealized | Explains why a 5 A bench supply cannot cover the full historical stress envelope. Conversion loss, source sag and revised profile alignment can only be resolved after branch binding. |
| `MD-01` average power cross-check | `(2.6…5.3 Wh) / (20/60 h)` | `7.8…15.9 W` | Agrees with the ledger within rounding; no pack capacity follows until usable-energy, reserve, aging, temperature and drive evidence are registered. |

No generic safety factor is applied to these numbers. Protection clearing, transient delivery, conductor heating, converter thermal rating and energy capacity use different mechanisms and later calculations.

No branch is yet eligible for a final conductor, protection, converter or connector rating. That is an evidence finding, not a failure of this contract issue.

## 8. Reopen and maintenance rule

Re-evaluate a branch and every upstream parent when:

- an attached `LG` changes hardware or evidence class;
- a `CC`, `LP`, `ST` or `MD` definition changes;
- the source/return path, connector, conductor, protection or switch changes;
- a source/charger/pack voltage or impedance changes;
- a load moves between direct and downstream powering;
- a measured transient exceeds its registered envelope;
- a new back-power, regenerative or partial-power path is discovered.
