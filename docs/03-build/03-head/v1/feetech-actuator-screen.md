# Feetech actuator migration screen — working paper record

2026-10-07. This is the build delta to the read-only [RP-01 actuator screen](../../../02-prototypes/RP-01-head/actuator-screen-01.md) and [paper gates](../../../02-prototypes/RP-01-head/gates.md). It covers D-046 pitch/roll and D-047 yaw. **No complete P01–P09 pass or fabrication release is claimed.** `D` is vendor data, `E` is an estimate, `U` is unknown, and `W` would be a measurement; there is no `W` result yet.

## Source facts and corrected inputs

| Item | STS3045M pitch/roll | ST3215-HS yaw |
|---|---|---|
| Supply and nominal endpoint | 4.8–7.4 V; 6 V: 0.588 N·m stall, 75 rpm no-load, 1.4 A stall, 0.196 N·m / 450 mA rated (`D`) | 6–12.6 V; 12 V: 1.96 N·m stall, 106 rpm no-load, 2.4 A locked rotor, 240 mA running without load (`D`) |
| Mass / envelope | 34.8 ± 1 g; 36 × 15 × 29.2 mm case; mounting ears 48.8 mm span (`D`) | 68 g; 45.22 × 35 × 24.72 mm nominal; named sourced STEP bounding box 45.2234 × 37.8 × 24.7234 mm including protrusions (`D/E`, [local STEP](../../02-body/v1/cad/purchased/waveshare_feetech_st3215_hs_servo.step)) |
| Output | 25T / Ø5.9 mm spline, M3 × 6 horn screw; 1:281 reduction; ≤0.5° stated gearbox backlash (`D`) | 4096 steps/revolution; gear ratio and output shaft radial-load rating still `U` |
| Signal | Half-duplex TTL, signal high 2–5 V and low 0–0.45 V (`D`) | Feetech ST-series half-duplex TTL, 1 Mbps factory example (`D`); mixed-supply bus electrical tolerance needs bench proof |

The [STS3045M specification](https://pages.switch-science.com/comparison/files/feetech/serial-sts/STS3045M_datasheet.pdf) supplies the ratio, output and mounting drawing (pages 4, 6 and 8). The [Feetech product page](https://www.feetechrc.com/6v-6-kgcm-aluminum-shell-hollow-cup-metal-tooth-360-degree-magnetic-coding-single-axis-ttl-serial-port-actuator.html) gives a 4.8 V minimum. The PDF table says 4.0 V; this screen uses the stricter 4.8 V until the exact received revision is identified. Its accessories table says “No Accessories” while the package photograph shows horns and screws: purchase horns and M3 × 6 screws separately unless the supplier confirms the delivered kit. The [Waveshare ST3215-HS page](https://www.waveshare.com/wiki/ST3215-HS_Servo_Motor) provides the yaw figures and [official STEP archive](https://files.waveshare.com/upload/5/59/ST3215-3D.zip). The local STEP came from that archive, SHA-256 `58e38e4dc49f97df738c5f229f9aa8a7dce64a0a1d01335486a52d53e6017e8a`; one main-case solid has invalid topology in the official file, so it is a packaging reference pending repair/physical confirmation. No exact STS3045M STEP appeared in the step.parts catalog; STS3045 and STS3046 are distinct models and are not substituted.

## Torque–speed calculation at the terminals

The proposed 5.5 V head setpoint and legacy ±2.18% feedback tolerance give 5.38–5.62 V at PCB-03; subtracting the registered 150 mV wiring drop gives **5.23 V minimum at a head servo**. The 12 V yaw figure is a *target at the servo*, pending converter and cable-drop design. The table uses the diagnostic straight line `T = T_stall(1 − rpm/rpm_0)` times the legacy 0.86 graph/proxy factor for the head. Voltage scaling of both STS3045M endpoints from 6 V is an `E` assumption, **not** a vendor curve at 5.23 V. The 0.86 factor is from the XC330 and is not validated for Feetech.

| Axis and motion | Speed used | Proxy capability | Legacy-tree demand | Result |
|---|---:|---:|---:|---|
| Pitch, 70% rapid cap | 27.5 rpm | 0.255 N·m at 5.23 V (`E`) | about 0.145 N·m (`E`, D-046, before head re-fit) | 1.76× *provisional* |
| Roll, 100% rapid | 30.0 rpm | 0.239 N·m at 5.23 V (`E`) | about 0.129 N·m (`E`, D-046, before head re-fit) | 1.85× *provisional* |
| Yaw, 100% rapid | 63.0 rpm | 0.684 N·m at 12 V (`E`, same unvalidated 0.86 factor) | about 0.22 N·m (`E`, D-047, before head re-fit) | 3.1× *provisional* |

The old RP-01 motor-side inertia estimate was 0.11–0.25 g·cm², not a measured Feetech rotor value. Using the **published STS3045M 281:1 ratio** reflects that range to `J_eq = J_motor × 281² = 0.000869–0.001974 kg·m²` at each head output. This is slightly below the old XC330-M288 0.00092–0.00208 kg·m² range; it does **not** justify reusing the old total load. A focused [34.8 g case-box what-if](cad/generated/feetech-mass-whatif.json) changes the unchanged-structure pitch mass from 470.29 to **482.09 g** and pitch inertia from 0.0007872 to **0.0008344 kg·m²**, while yaw-carried mass rises from 594.03 to **617.63 g** and yaw inertia from 0.0012958 to **0.0013579 kg·m²**; roll inertia is unchanged because both servos are outside the rolling frame. These `E` values exclude new mounts, horns, cable, balance and A0 re-solve. The ST3215-HS ratio remains unknown, so its internal-inertia term cannot yet be bounded in the same way. Recompute every trajectory from the head v1 mass tree and the fitted axes, then compare every point with a measured Feetech torque–speed curve at 5.23 V / 12 V. Do not use the three worst-case corners above as a substitute for that overlay.

**Thermal.** The STS3045M's 0.196 N·m *rated torque at 6 V* exceeds the provisional 0.075 N·m pitch RMS by 2.6×. The new mass tree, slower storyboard duty, 5.23 V rating and sealed-head temperature have not been resolved. Bench B3 must run repeated busy minutes to temperature equilibrium, with servo-terminal voltage, current, case temperature and ambient logged. The 240 mA HS no-load running current is 2.88 W at 12 V and belongs in the battery budget whenever yaw is active; it is not an always-on quiescent current.

## P01–P09 migration status

| Gate | Current build status and closing evidence |
|---|---|
| P01 mass/configuration | **OPEN.** The drawing-based STS3045M STEP and unchanged-structure mass sensitivity are available; live head CAD still carries two 23 g XC330 rows. Redesign mounts, solve the mass tree and hand its output to body v1. The 68 g yaw STEP is available, but not installed in the body model. |
| P02 rail/curve | **OPEN.** 5.23–5.62 V head-terminal estimate and 12 V yaw target documented; need loaded terminal logs and servo-specific moving curves. |
| P03 transient | **OPEN.** Proxies above are encouraging but use old mass/axes, unknown HS internal inertia and unvalidated curves. Re-run full §11.3 cases after the CAD fit. |
| P04 continuous/thermal | **OPEN.** 6 V rated-torque screen only; bench B3 needed in the enclosed head. |
| P05 uncertainty/coverage | **OPEN.** Head motor-side inertia is an `E` range reflected through 281:1; HS inertia, real cable load and cross-axis cases remain unknown. |
| P06 decision/rig handoff | **CONDITIONAL RIG CANDIDATE.** B1 (loaded speed/current), B2 (torque–speed at actual terminals), B3 (thermal), B4 (loaded lash), B5 (rail/bus fault), B6 (loaded modes) remain. |
| P07 structural dynamics | **OPEN.** Old 41 Hz pitch-frame and 84 Hz roll-mount FEA do not cover the new saddle, horn and joints. Re-run the RP-06 method, then loaded tap/ring-down; minimum ≥30 Hz pitch and ≥25 Hz roll. The 70% pitch trajectory reduces forcing frequency but does not replace modal evidence. |
| P08 CAD/hardware | **OPEN.** The [neutral-pose fit](cad/feetech-head-fit.md) finds specific cover, trim, strap, cradle, trunnion and adapter clashes. New ear slots, horn, screws, stops, sweep, access and side load need a refitted model and received-part check. |
| P09 complete-output lash | **OPEN.** STS3045M claims ≤0.5° gearbox backlash, already at the minimum viable whole-output budget. The HS plus scissor mesh must be measured at both horn and head axis under load; B4 decides the HS/STS3250 fallback. |

## Firmware and protection contract to implement

Feetech's [magnetic encoder protocol](https://www.feetechrc.com/Data/feetechrc/upload/file/20240702/%E8%88%B5%E6%9C%BA%E5%8D%8F%E8%AE%AE%E6%89%8B%E5%86%8C-%E7%A3%81%E7%BC%96%E7%A0%81%E7%89%88%E6%9C%AC.pdf) uses `FF FF ID LENGTH INSTRUCTION PARAMETERS CHECKSUM`, checksum `~sum(ID…parameters)`, and little-endian two-byte fields. The [official magnetic memory table](https://www.feetechrc.com/en/letter-of-agreement.html) (linked XLSX) identifies the fields below. Check the exact received firmware's table before committing EEPROM values.

| Address | Field | Proposed build rule |
|---:|---|---|
| 5, 6 | ID, baud | Program each servo alone: yaw 1, pitch 2, roll 3; baud code 0 = 1 Mbps. Read back, then connect the shared bus. |
| 9–12 | min/max position | Home mechanically with torque off; yaw centre 2048, then limits **1388–2708** for ±58° (`58×4096/360≈660` counts). Confirm direction and horn zero before writing. |
| 13–15 | max temperature, max/min voltage | Model-specific limits; head 70 °C factory reference and 4.8–7.4 V operation, yaw 6–12.6 V. Verify unit 0.1 V and protection action. |
| 16–17, 48–49 | maximum torque, running torque limit | 0–1000 corresponds to 0–100% of stall. Start with torque off, then tune a per-axis cap from measured B1 current/trajectory; no XC330 ampere limits are copied. |
| 19, 28–29, 35–36, 38 | unload-condition bits; protection current (6.5 mA/count); overload time/threshold; overcurrent time | Enable voltage, encoder, temperature, current and overload fault bits after confirming the installed servo firmware. Protection time counts 10 ms; default 200 = 2 s is too long to count as the only fast containment. |
| 26–27, 33, 40 | two dead zones; operating mode; torque enable | Set both dead zones to **1 count** initially (0.0879°); zero is permitted in the table but may chatter. Position mode 0; write torque enable only after configuration/limits readback. On fault or stale commands, send torque-off and remove the hardware permit. |

There is no direct Feetech counterpart to Dynamixel Current-based Position Mode 5, `Shutdown=0x35`, or its 100 ms Bus Watchdog. C2 must enforce a command-age deadline and servo-error polling; PCB-03's permit and latching trunk protection remain independent. An overload can recover on a new position command according to the STS3045M datasheet, so firmware must latch the fault and withhold new goals until a fresh arm. The actual unload-condition mask and current threshold are a commissioning result, not a paper default.
