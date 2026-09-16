# RP-02 Brownout, Reset and Restart Contract

| Field | Value |
|---|---|
| Status | **Registered brownout/reset/restart baseline v1.0 under `RP02-P2-REG-03`, builder-approved 2026-09-16.** Part-2 subpart 7 is complete at policy/calculation-method level; numeric thresholds remain evidence-gated. |
| Date | 2026-09-16 |
| Scope | Loaded-source observation, intended brownout order, threshold ownership, fast-collapse behavior, controller reset defaults, source restoration and recovery from fresh intent |
| Inherits | `RP02-P1-REG-01`, `RP02-P2-REG-01`, `RP02-P2-REG-02`; especially `EN-02/03`, `OM-03/04/06`, `PA-07/10/13/14`, `EDB-04` and F-02/F-06/F-07/F-11/F-13/F-16/F-18/F-22 |
| Does not select | Battery chemistry/S-count, voltage thresholds, comparator/monitor, capacitance, converter UVLO, delay, fuse, pack capacity or purchase |
| Completion rule | Every energy-loss rate follows one of the paths below; hazardous authority disappears before control becomes unreliable; no voltage recovery, reset or reconnection can replay motion |

Brownout is not defined as “the Pi reports low voltage.” It is the system condition in which one or more source/branch margins are being consumed and the robot must reach a safe, diagnosable terminal state before the controllers responsible for that state become unreliable.

## 1. Required outcome

The intended functional order is:

`detect loaded-source margin loss → reject new peaks → shed non-safety demand while braking/cancelling motion → remove motor authority → shut compute down when time permits → retain safety supervision through motor-energy confirmation/sign-off → logic off`

Load shedding and controlled stopping may overlap. What is ordered absolutely is that no new hazardous demand is admitted after detection, motor permission becomes inactive before safety control becomes unreliable, and safety supervision outlives hazardous motor energy.

Natural rail collapse is never the actuator-stop mechanism. The implementation acts early enough that the motor gate and local driver enables become inactive while C2/base safety are still operating validly. Pack protection remains the last-resort cell/pack safeguard, not the normal robot shutdown threshold.

Two paths are mandatory:

| Path | Trigger character | Required response |
|---|---|---|
| Controlled depletion | Loaded voltage/energy crosses registered thresholds slowly enough to retain bounded control | Execute the complete `EN-02 → EN-03 → EV-14` sequence |
| Fast collapse/fault | Source or required rail falls too quickly, power-good disappears, or calculated orderly-stop margin is no longer credible | Immediately withdraw hardware motor permission and local driver enables; graceful compute shutdown is optional, safety is not |

## 2. `BR-*` requirements

### `BR-01` — Energy observation is independent of the SBC

1. Loaded pack/source voltage and the safety-critical rail-present/power-good indications reach C2 or equivalent minimum supervision without requiring a healthy SBC.
2. Open-circuit pack voltage does not assert `EN-01`; the decision uses loaded voltage plus current/context or a conservative loaded equivalent.
3. The SBC may contribute coulomb/energy estimates, but its estimate cannot suppress a local low-voltage or invalid-rail observation.
4. The monitor path has a defined invalid/disconnected result. Invalid safety-energy evidence resolves to inhibit, never “normal.”

### `BR-02` — Low energy is an action-cancelling state

On confirmed `EN-02` entry:

1. Reject new locomotion, startle/peak gestures and any new load-enable that worsens the deficit.
2. Cancel the active motor action instances; base motion brakes and active head motion brakes/settles within the then-valid margin.
3. Clear the motor-enable/action epoch so recovered voltage cannot resume the interrupted command.
4. Preserve only bounded indication and the compute/sensing needed to finish the stop and expose the reason.
5. Mode evidence may remain current, but motion requires a fresh motor-arm/enable and a new action instance after stable `EN-01` recovery.

### `BR-03` — Critical energy precedes unreliable control

On confirmed `EN-03` entry:

1. Enter `OM-03`; reject every new motor goal.
2. Immediately shed camera, audio output/input and other `EC-N` loads; reduce display to bounded critical indication. This happens in parallel with, and may not delay, the controlled stop.
3. Execute bounded braking/settling only if the safety supervisor still proves the required source/rail margin. Otherwise use the fast-collapse path.
4. Open the system motor-arm gate and deassert local head/drive enables no later than the registered stop deadline.
5. Confirm motor-bus absence/discharge to the later registered safe level, or record that the confirmation channel itself became invalid and keep the gate commanded open.
6. Switch the remaining indication off. Ask the SBC to persist the terminal reason and shut down only if the remaining voltage/energy budget proves that the request can finish. SBC shutdown is not allowed to delay motor-energy removal.
7. C2/base safety stay valid through motor-energy sign-off, persist their reset/fault context, then release the system-power latch or tolerate final source collapse with all hardware enables inactive.

### `BR-04` — Fast collapse bypasses graceful sequencing

A fast-collapse condition exists when any of the following occurs:

- a required safety-rail power-good becomes invalid;
- source `dV/dt` or step loss exceeds the preregistered orderly-stop envelope;
- the calculated stop reserve is no longer present;
- C2/base energy observation is absent, implausible or stale while motor energy is present;
- hardware UVLO/brownout indication asserts before the software critical sequence completes.

The response is immediate hardware/local inhibit: withdraw `ENERGY_OK`, open the motor-arm path, deassert driver/servo enables and let controllers reset only after the hazardous permission is already inactive. Logging and display are best effort on this path.

### `BR-05` — Motor permission contains energy and readiness

The implemented motor permission is equivalent to:

`MOTOR_PERMIT = E_STOP_OK ∧ SYSTEM_ARM ∧ CHARGE_ABSENT ∧ ENERGY_OK ∧ C2_READY ∧ BASE_READY(if installed)`

Requirements:

- every term is fail-inactive at its receiving hardware boundary;
- loss/reset of either installed safety controller withdraws its readiness term;
- a physically absent base branch may be bypassed only by a recorded prototype configuration in which no drive power stage is installed;
- SBC health is not a direct hardware permission, but heartbeat/session loss makes local controllers withdraw current action authority and leads to motor inhibit;
- a software command cannot override `E_STOP_OK`, `CHARGE_ABSENT`, `ENERGY_OK` or missing local readiness.

### `BR-06` — Every reset boots inhibited

| Reset/loss | Required electrical result | First legal recovered state |
|---|---|---|
| SBC process/full reset | C2/base expire commands and brake; compute noise cannot form a valid enable | `OM-03`, local controllers inhibited |
| C2 reset/brownout | C2-ready and head enable inactive in hardware; the system motor permit opens if C2 is installed | `OM-03`, no limits/goals accepted yet |
| Base-controller reset/brownout | Base-ready and driver enable inactive in hardware; system motor permit opens | `OM-03`, drive unavailable |
| Display reset/brownout | Display may darken/reboot; C2 and motor permissions are unaffected | Previous safe system state, with display health degraded until fresh state arrives |
| Compute converter reset | No change can energize motors; any compute-dependent action cancels | `OM-03` for motion authority |
| Safety converter reset | Its readiness drops before/with reset and cannot be reconstructed from stale GPIO state | `OM-03`; full safety handshake required |
| Pack removal/protector cutoff | Motor and system-power paths lose source; no back-power route sustains a partial state | Final `OFF` |

Boot firmware must set output latches and pin muxes so enables remain inactive before application initialization. “Firmware will quickly turn it off” is not an accepted reset default.

### `BR-07` — Recovery consumes fresh intent

Any `EN-03`, safety-controller reset, motor-bus loss, battery removal/reconnection, E-stop cycle, charge-mode transition or source-selector reset invalidates:

- operating-mode selection where Part 1 requires session reacceptance;
- system-arm and per-controller enable nonces;
- current/queued action IDs and trajectory segments;
- pre-fault limits if the reset controller cannot prove they belong to the new boot/session;
- acknowledgements or frames from the previous power epoch.

Recovery requires, in order:

1. source within the registered clear envelope for the registered stable dwell;
2. all required safety rails power-good and reset reasons captured;
3. C2/base self-check, local sensor validity and inhibited outputs;
4. new boot/session identity and empty command queues;
5. explicit current Floor/Table selection where required;
6. fresh limits/readiness handshake;
7. deliberate new system-arm and per-controller enable;
8. a new action instance created from current user/behaviour intent.

Voltage recovery alone can move the energy estimate from `EN-02/03` toward available; it cannot execute steps 5–8.

### `BR-08` — Assertion and clearance use different proof

- Low/critical assertion uses the conservative loaded condition and a debounce short enough to preserve stop reserve.
- Clearance uses a higher voltage/energy threshold, longer stability dwell and no active peak load; the difference is true hysteresis, not only filtering.
- A transient that does not assert `EN-02` is still logged if it consumes the registered rail margin.
- Repeated threshold crossings inside one session latch a degraded energy/pack-health condition and may require service rather than endless stop/re-arm cycles.
- A converter's built-in UVLO is a last local boundary, not the system low-energy policy.

### `BR-09` — Charge-source loss never becomes operation

During `OM-06/EN-04`, `PB-MOTOR`, compute and ordinary application loads are already off.

- If charge input disappears while the pack can support charge supervision, expose F-18 and remain inhibited.
- If the pack is absent/depleted, C2/display may reset or switch off; no orderly operating transition is assumed.
- Restoring charge input resumes only the validated charge-mode sequence.
- Removing the charge source can enter final `OFF` or a fresh `OPERATE` boot; it cannot restore the pre-charge mode, system arm or action.

### `BR-10` — Thresholds are calculated and then measured

No numeric low/critical threshold is valid until all of these inputs are bound:

- selected pack chemistry, series count, protection thresholds and internal resistance versus state, age and temperature;
- minimum converter input/output operating and UVLO/restart envelopes with tolerance;
- safety-controller and motor-driver valid operating minima;
- installed source/return/contact/protection resistance;
- worst credible stop/settle current and duration, including regeneration behavior;
- monitor accuracy, sample rate, filter/debounce and end-to-end reaction time;
- source decay rate and step size used by the qualification case;
- energy needed for local inhibit/sign-off and, separately, optional SBC shutdown.

## 3. Threshold ownership

| Layer | Owns | Must not be used as |
|---|---|---|
| Cell/pack protection | Cell over/undervoltage, overcurrent, temperature and last-resort pack isolation | Normal `EN-02/03` policy or routine system shutdown |
| Main source monitor / C2 minimum supervision | Loaded-source validity, `EN-02/03`, `ENERGY_OK` and source-fault exposure | Sole pack state-of-charge estimator |
| C2 local brownout/PG | Head safety-rail validity, C2 reset reason and head enable default | Permission to keep motors active after source-energy invalidity |
| Base MCU local brownout/PG | Base safety-rail validity, driver-enable default and F-22 exposure | Substitute for system loaded-source policy |
| SBC | Orderly application shutdown, rich telemetry and coulomb/energy estimate | Sole low-energy detector or hardware motor interlock |
| Converter/driver UVLO | Local prevention of undefined operation | First intended system response |
| Charger/power path | Charge-source limits, pack charging, temperature and source-transfer behavior | Authority to restore `OPERATE` or motor permission |

## 4. Symbolic threshold and reserve calculation

### 4.1 Source-equivalent operating floor

For every converted safety-relevant branch `j`, first determine the converter-input floor that still guarantees its terminal minimum, then add the worst upstream source-path drop:

`V_CONV_IN_REQ,j = f_inv_converter,j(V_TERM_MIN,j, I_j, T, tolerance)`

`V_SRC_REQ,j = V_CONV_IN_REQ,j + V_UPSTREAM_PATH_DROP,j`

For a direct/unregulated branch, use `V_SRC_REQ,j = V_TERM_MIN,j + V_PATH_DROP,j`. Do not move an input-path drop through a converter as though it were an output-voltage term.

The safety-control source floor is:

`V_SRC_SAFE = max(V_SRC_REQ,C2, V_SRC_REQ,BASE, V_SRC_REQ,driver-control, ...)`

The critical assertion must include measurement, detection and stop-transient margin:

`V_CRIT_ASSERT ≥ V_SRC_SAFE + ΔV_measure + ΔV_path-step + |dV_SRC/dt|_max·(t_detect + t_inhibit) + ΔV_stop-sag`

This voltage condition is necessary but not sufficient. The remaining usable energy at assertion must also pass:

`E_REMAIN_CRIT ≥ E_brake/settle + E_local-signoff + E_required-logic + E_margin`

Optional SBC orderly-shutdown energy is reported separately. If it is not available, the response still passes when motor energy is safely removed and the SBC loss is exposed on the next boot.

### 4.2 Required ordering

At the declared worst source/load/temperature condition:

1. `EN-02` asserts with enough margin to brake active motion and reject additional demand.
2. `EN-03` asserts before `V_SRC_SAFE` plus the complete reaction/stop margin is consumed.
3. Software-requested motor-arm removal occurs before the hard `ENERGY_OK`/power-good boundary.
4. The hard boundary removes motor permission before any safety controller or motor driver enters an undefined/restarting region.
5. Application rails may be intentionally shed at or after `EN-03`; their natural reset thresholds do not define the safety order.
6. Pack protection cutoff occurs only after robot motor authority is already absent in the tested path.

The ordering is evaluated in time as well as voltage. Threshold voltage alone is inadequate when source impedance or `dV/dt` is high.

### 4.3 Hysteresis and debounce constraints

Use separate assert/clear values:

`V_LOW_CLEAR > V_LOW_ASSERT > V_CRIT_ASSERT`

and independently:

`V_CRIT_CLEAR > V_CRIT_ASSERT`

subject to the chemistry-specific discharge/recovery mapping. In addition:

- `t_CRIT_ASSERT` must be shorter than the remaining safe reaction window;
- `t_LOW_ASSERT` may reject valid `TB-1` spikes but cannot mask repeated `TB-2` sag;
- clear dwell must exceed the longest tested load-release rebound that would otherwise chatter the state;
- the registered state machine must define priority across overlapping hysteresis bands; non-overlap (`V_LOW_ASSERT > V_CRIT_CLEAR`) is preferred but is not assumed before source evidence exists;
- clearing never restores the previous action or arm epoch.

Exact values remain `U` until the selected source and representative loads produce `D/W` inputs.

## 5. Intended branch order

| Stage | Safety branches | Motor domain | Compute | Display | Camera/audio/mics | Required evidence |
|---|---|---|---|---|---|---|
| Normal `EN-01` | Valid and observing | Current authorized state | Active by case | Active by case | Active by case | All margins positive |
| Low `EN-02` | Remain valid | Brake/cancel; no new peaks or locomotion | Retained for coordination; peak workload denied | Bounded/reduced | Shed or bounded as policy requires | Loaded threshold timestamp precedes stop action |
| Critical `EN-03` | Remain valid through sign-off | Settle only with proven margin; then gate/driver off | Orderly shutdown only inside remaining budget | Critical indication then off | Off first | Motor permission absent before safety invalidity |
| Motor-safe/sign-off | C2/base remain valid | `OFF`, discharge observed | May be shutting down/off | Off | Off | Gate state plus bus voltage/current |
| Final `OFF` | Off after sign-off/latch release | Off | Off | Off | Off | No phantom/back-power source |
| Fast collapse | May reset only after readiness/enable has failed inactive | Immediate gate/driver off | Best effort / may reset | May reset | Off/unknown | Hardware timing proves motor permission disappears first |

This is a functional priority order. It does not require every regulated rail to fall in the same physical voltage sequence; independent converters may hold or collapse differently.

## 6. Hold-up and discharge calculations

Safety hold-up covers only the interval that must remain valid after the upstream source becomes inadequate:

`t_HOLD_SAFE ≥ t_detect,max + t_inhibit,max + t_gate-open,max + t_motor-safe-confirm,max + t_local-signoff,max + t_margin`

For a branch-local capacitor feeding an approximately constant-power load:

`C_MIN = 2·P_LOAD·t_HOLD_SAFE / (V_HIGH² − V_LOW²)`

For a constant-current approximation over a small voltage change:

`C_MIN = I_LOAD·t_HOLD_SAFE / ΔV`

`P_LOAD` and `I_LOAD` are the capacitor-side worst-case demands, including any downstream conversion/control losses over the hold-up interval; using only endpoint output power would under-size the store.

The selected value must then include capacitance tolerance, DC-bias loss, ESR/ESL, temperature/ageing, converter stability and startup/inrush. Capacitance cannot bridge safety and application branches.

Motor-bus stored energy remains hazardous after the gate opens:

`E_STORED = ½·C_MOTOR·V_MOTOR² + E_mechanical/regenerative`

For a verified passive discharge resistance after every regenerative/mechanical source has been isolated, the capacitive decay is:

`t_DISCHARGE = R_EQ·C_MOTOR·ln(V_INITIAL / V_SAFE)`

or, for a required maximum time:

`R_EQ ≤ t_DISCHARGE,max / [C_MOTOR·ln(V_INITIAL / V_SAFE)]`

Check initial resistor/switch power `P_INITIAL = V_INITIAL² / R_EQ`, pulse energy and repetitive thermal duty. The RC result is not valid while a motor or moving mechanism can regenerate into the bus; that case needs the measured signed-current/mechanical decay model.

The discharge path is sized so the motor bus reaches the registered safe voltage/energy before recovery is allowed, without exceeding resistor/switch thermal or fault ratings. A motor's uncontrolled coast or a weak reset loop is not credited as discharge.

## 7. Restart and source-transfer truth table

| Event | May logic restart automatically? | May motor power return automatically? | May motion resume automatically? |
|---|---|---|---|
| `EN-02` clears | Yes, affected non-hazardous loads may be restored by policy after stable dwell | No; fresh arm/enable required | No; new action required |
| `EN-03` clears / battery replaced | Safety and application boot sequence may start | No | No; explicit mode, arm, enable and new action |
| C2/base reset | Controller may reboot | No; readiness is absent | No |
| SBC reset | SBC may reboot | Motor gate remains governed locally and inhibited by expired authority | No |
| Display reset | Yes | Unaffected | Existing motor action is not created or altered by display recovery |
| E-stop release | Safety logic stays/restarts as designed | Only after a new system-arm action | No |
| Charge input restored | Charge supervision may restart | No, hardware-inhibited in `OM-06` | No |
| Charge removed | Fresh `OFF` or `OPERATE` boot may begin | No until complete operating sequence | No |
| Link reconnect | Yes | No direct effect | No; new session/enable/action as applicable |

## 8. Verification contract

### 8.1 Preregister before each scored configuration

- exact pack/bench-source configuration, source resistance and current limit;
- `V_LOW_ASSERT/CLEAR`, `V_CRIT_ASSERT/CLEAR`, debounce and stable-clear dwell;
- hard `ENERGY_OK`, converter UVLO/restart and power-good thresholds with tolerance;
- slow-ramp and fast-collapse injection waveforms/rates;
- load/case binding and allowed brake/settle action;
- motor-bus safe-voltage/energy and maximum discharge time;
- required C2/base hold-up interval and the capacitor value/tolerance under test;
- instrument bandwidth, channel timing skew and uncertainty.

### 8.2 Required runs

1. Slow source ramp through `EN-02` during `CC-13H` and `CC-13D`.
2. Continue through `EN-03` during `CC-14` under the largest then-valid sustained load.
3. Repeat with the largest admissible `CC-PEAK-01`, then `ST-01`, without calling synthetic alignment representative duty.
4. Apply a fast source step/collapse that invalidates the orderly-stop envelope; verify `BR-04` hardware behavior.
5. Brown out each branch independently: compute, display, C2, base safety, head/drive source as available.
6. Restore source just below/above each clear threshold to test hysteresis and chatter.
7. Cycle battery/bench source removal and reconnection, C2/base resets, E-stop and charge insertion/removal.
8. Inject back-power attempts through USB, UART/programming and charge connections while target branches are off.

### 8.3 Pass conditions

- zero motor command or enable after its authority/epoch becomes invalid;
- zero automatic motion after voltage recovery, reset, reconnection or E-stop release;
- motor permission and local driver enables become inactive before their controllers leave valid operation;
- `EN-02/03`, reason, reset source and branch health are exposed whenever logging survives;
- slow-path terminal order matches §5; fast path matches `BR-04`;
- C2/display, C2/base and safety/application fault containment matches `PA-11/12`;
- motor-bus discharge and safety hold-up meet their preregistered thresholds in every repetition;
- pack protection is not the normal element that stops motion;
- no back-power sustains a forbidden partial state.

Per F-11/F-16 and G04, use at least five repetitions per injected fault/configuration in at least two applicable states. A threshold may be tuned during exploratory work, but it is frozen before the scored runs whose evidence it judges.

## 9. Values intentionally open

| Value | Why it remains open | Owner/input that closes it |
|---|---|---|
| `V_LOW_ASSERT/CLEAR` | Chemistry and loaded sag not selected/measured | Pack `D/W`, complete operating paths |
| `V_CRIT_ASSERT/CLEAR` | Stop reserve and safety-source floor not measured | C2/base/driver minima plus worst valid stop profile |
| Debounce and stable-clear dwell | Must distinguish legitimate transients from depletion without masking `TB-2` sag | Source/load captures and monitor implementation |
| Hard `ENERGY_OK` threshold | Comparator/monitor and motor driver/gate implementation open | Selected motor-arm circuit and RP-03 |
| C2/base hold-up | Reset thresholds, action times and installed loads open | Converter/controller `D/W`, gate/discharge timing |
| SBC shutdown budget | Storage/workload and Pi power-entry path open | RP-07 and selected storage |
| Motor-bus safe voltage/discharge time | Driver, motors, capacitance and mechanics open | RP-01/RP-03 implementation and hazard test |
| Repeat-crossing/service policy | Pack ageing signature not measured | Phase-C pack evidence |

These are not omissions from the design-definition subpart. The contract states the equations, ownership, ordering, safe defaults, evidence and freeze rule needed to derive them honestly.

## 10. Completion state

| Item | Result |
|---|---|
| Intended brownout order | Complete |
| Slow-depletion and fast-collapse paths | Complete |
| Threshold ownership | Complete |
| Reset-safe defaults | Complete |
| Fresh-intent/restart sequence | Complete |
| Threshold and hold-up calculation method | Complete |
| Verification contract | Complete |
| Numeric thresholds/capacitance/discharge time | Intentionally open pending selected hardware and `D/W` evidence |
| Registration | Complete under `RP02-P2-REG-03` |

## 11. Registration record

| Field | Registered value |
|---|---|
| Registration | `RP02-P2-REG-03` |
| Date | 2026-09-16 |
| Approval | Builder explicitly approved the complete reviewed Part-2 work in the project conversation |
| Frozen scope | `BR-01…10`; controlled-depletion and fast-collapse paths; threshold ownership; fail-inactive `MOTOR_PERMIT` composition; reset defaults; fresh-intent recovery; symbolic threshold, hold-up and discharge methods; branch priority; restart/source-transfer truth table; verification contract |
| Not registered | Numeric voltage/energy thresholds, debounce/dwell, capacitance, discharge time, timing deadlines, component/SKU selection, battery chemistry/S-count/capacity, purchase, run configuration, gate threshold or measured result |
| Change rule | Any policy relaxation, new automatic restart path, removal of a fail-inactive permission term or material calculation-method change requires a superseding registration. Populating evidence-gated numeric fields does not rewrite this baseline; values are preregistered with their scored configuration. |
