# Feetech actuator bench gates B1–B6

Execution waits for one STS3045M, one ST3215-HS, a compatible Feetech USB
adapter, a current-limited 12 V source, the 5.5 V head source and the actual
horns. Use independent terminal-voltage and current measurements; log the
servo's reported position, speed, voltage, temperature and error bits with
time stamps. Record model/firmware IDs and the memory-table revision before
writing EEPROM. The [bus contract](../../04-pcbs/feetech-link-contract.md)
defines the intended IDs and fault handling.

| Gate | Setup and run | Acceptance evidence |
|---|---|---|
| B1 loaded motion | Support a pitch mock-up with the final A0 CoM, measured inertia and horn. Run every revised [storyboard](feetech-motion-storyboard.md) segment at the **minimum measured 5.23 V terminal** and the 5.62 V high corner. Repeat pitch and roll with final fitted geometry. | Time-aligned commanded/actual angle, position error, current and rail sag through the laugh reversal and startle; no skip, reset, stop strike or lost goal. Compare peak and RMS with the final load and power budgets. |
| B2 moving curve | Sweep speed and load at 5.23 V / 5.62 V for STS3045M and at the worst achieved yaw-terminal voltage / 12 V target for HS. Include warm and cold runs and the actual chosen torque cap. | Measured torque–speed points exceed every final per-sample `Jα + gravity + friction + cable` demand with the project margin; replace the provisional straight-line/0.86 proxy. |
| B3 heat | Run the final busy-minute and hold mix repeatedly inside a representative closed head, with thermal equilibrium or a clearly trending failure. | Current, case and ambient temperature curves plus servo error bits. No thermal trip, loss of position or rail derating; show head voltage and the validated register limit at equilibrium. |
| B4 backlash | With torque applied, reverse known loads at the output horn and again at each final head axis; measure both directions at several angles. Test HS with its final scissor pinion/preload. | Report gearbox, horn/coupling and whole-output lost motion separately. Whole-output lash must clear the 0.5° minimum viable budget; otherwise evaluate the D-047 STS3250 fallback. |
| B5 rail and bus faults | Use all three servos on the mixed 5.5/12 V bus. Apply a single stall, both-head load, yaw load, missing reply, duplicate ID, stuck data line, lost C2 commands, power cycling and yaw braking from maximum authored speed. | Oscilloscope traces of both rails, bus data, `MOTOR_PERMIT`, current monitor and clamp. The latch removes power/torque on the specified command-age fault; no 12 V data pull-up, unpowered backfeed, converter overvoltage or unintended re-arm. Set current/time/voltage register values from these traces. |
| B6 combined modes | Play every authored BC-60/MV-60 scene and the simultaneous startle with the fitted mass tree; log all three axes and supply branches. | No missed motion deadline or unsafe combined rail demand. Record the actual busy-minute Wh and RMS torque/current for runtime and P04/P07 screens. |

Archive raw logs beside a run sheet giving date, servo serial numbers,
firmware, horn, supply, fixture mass/CoM/inertia, register readback, ambient
temperature and calibration. A test cannot close a gate when that setup does
not match the fitted head/body design. Nothing on this page is a measured
result yet.
