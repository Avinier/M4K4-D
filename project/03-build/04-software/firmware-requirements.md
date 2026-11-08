# Firmware requirements from D-093 to D-096 (plan level 8)

| Field | Value |
|---|---|
| Status | **Requirements, 2026-11-07.** No firmware written. Each row names the controller, the requirement, where it comes from and the bench test that proves it |
| Why | [D-093](../decisions.md#d-093) moved protection jobs from hardware into firmware: there is no permit chain, `ENERGY_OK` comparator, `LTC2954` interrupt or sequencing latch any more |
| Controllers | **C0** Raspberry Pi 5 (body); **C2** ESP32-S3-Zero on PCB-12 (head); **C3** ESP32-S3 DevKitC on PCB-10 (base) |
| Tests | N-numbers are the bench register in [simplification-plan.md §4.12](../simplification-plan.md#412-tests) |

## 1. Power and battery (C0)

| ID | Requirement | Source | Proved by |
|---|---|---|---|
| FW-P1 | Read the INA226 (M6) at address 0x40 on the PCB-09 `i2c-gpio` bus (draft: SDA GPIO16, SCL GPIO26; bus number set on the deployed image). Use its **bus voltage under load** as the battery measure, not an open-circuit estimate | D-094 M6, D-096, D-098 amendment | N6 |
| FW-P2 | **Low-battery stop:** at a loaded bus voltage of 6.0 V (threshold to re-register after N6), command C2 and C3 to stop all motion and hold torque off | RP-02 §8.1 soft-critical, D-093 | N6 |
| FW-P3 | **Low-battery shutdown:** after FW-P2, shut the Pi down cleanly, then turn M1 off (FW-P5) before the TIFPS0629 under-voltage trip. Filter for load peaks: a coincident stall can pull each cell about 0.35 V below its resting voltage (cell resistance only), so no shutdown on a single sample | D-096 duration screen | N6 with a peak-load pulse at the 6.0 V point |
| FW-P4 | **Power button:** a press while on (sensed through a qualified high-impedance interface, never the M1 ON pad directly) starts an orderly shutdown. Candidate kernel mechanism: `dtoverlay=gpio-shutdown,gpio_pin=12,...`; set the active level to match the measured rear buffer | D-093 Q1, D-096 `W40` | N1(a) |
| FW-P5 | **Power off:** after shutdown, pulse M1's OFF input (> 1 V); never drive M1 ON from a GPIO. Candidate kernel mechanism: `dtoverlay=gpio-poweroff,gpiopin=13,...`, which must assert only at the end of shutdown | D-094 M1, D-096 | N1(a) |
| FW-P6 | Leave the Pi in its non-PD 5 V / 3 A mode: do **not** set `PSU_MAX_CURRENT` or `usb_max_current_enable`. USB peripherals stay within 600 mA | D-094 M4, Raspberry Pi RP-009856 | N12 |
| FW-P7 | Log `vcgencmd get_throttled` at boot and during operation; report any under-voltage flag | D-094 M4 | N12(c) |
| FW-P8 | No sequencing logic: every rail comes up together. Each controller must tolerate the others starting in any order | D-093 | N7 |
| FW-P9 | Charging happens only in `OFF`. Firmware cannot see the charger; the operating rule is in the user notes | D-093 | N5 |

**Board interface selected; physical wiring blocked.** [D-098](../decisions.md#d-098), amended after the failed long-route study, keeps button sense on GPIO12 (header pin 32) and M1 OFF on GPIO13 (pin 33), but moves the INA226 to a software I²C bus near the connector bay. The draft schematic uses GPIO16 (pin 36) for SDA and GPIO26 (pin 37) for SCL, with two 4.7 kΩ pull-ups to Pi 3.3 V. Pi I²C1 pins 3/5 retain only their rev A TP1/TP2 service pads. PCB-09 rev B must provide an accessible, mechanically supported six-wire harness termination. GPIO12 sees only the qualified 0–3.3 V output of the button-sense interface; GPIO13's inactive boot/halt state and M1 OFF drive must be proved. FW-P1, FW-P4 and FW-P5 can be specified, but their harness build waits for the rev B board and N1 evidence.

Candidate configuration: `dtoverlay=i2c-gpio,i2c_gpio_sda=16,i2c_gpio_scl=26,bus=<n>`, with the INA226 bound through the `ina2xx` driver. Verify parameter names, the chosen free bus number, pin ownership and the device at `0x40` on the **actual Pi 5 image** before release; this repository has not checked that image.

The two overlay names and parameters above are implementation candidates, **not verified on the deployed Pi 5 image**. Before enabling them, inspect the actual image's overlay files/help and merged device tree; then scope GPIO12 and GPIO13 through cold boot, warm reboot and halt, including with M1 connected. Do not substitute a userspace shutdown pulse for the end-of-shutdown OFF requirement.

## 2. Servos (C2)

| ID | Requirement | Source | Proved by |
|---|---|---|---|
| FW-S1 | **Current cap from the first instant:** set each Feetech servo's **max-torque (torque-limit) register**, which limits PWM duty and so caps stall current immediately. Candidates: about 1.0 A per head servo and about 1.5 A for yaw; final values from measured current waveforms | D-096 duration screen | N2(b), N3 with current waveforms |
| FW-S2 | Also set protection current and protection time as a backstop. Protection current alone trips only after its time, so it cannot cap the first pulse | D-096 review | N2(b) |
| FW-S3 | Confirm the yaw torque margin at the chosen torque limit with a measured torque-speed check before accepting it (the 1.6× figure is an estimate) | D-096 review | N3 |
| FW-S4 | No `ARM_REQ`, no READY pair, no watchdog on PCB-12; motion starts on command | D-093 | — |
| FW-S5 | Read each servo's load, temperature and status regularly; stop and report a servo in overload | D-093 | N2(b) |
| FW-S6 | The yaw rail is 11.1 V: no firmware step may assume 12 V (speed and torque tables) | D-093 Q8 | N3 |

## 3. Base (C3)

| ID | Requirement | Source | Proved by |
|---|---|---|---|
| FW-B1 | Feed the PCB-10 TPS3436 watchdog and drive `MCU_RDY`; the watchdog and U4 AND gate hold both DRV8833 `nSLEEP` low if C3 hangs. This is now the hardware motor stop | D-068, D-093 | Existing PCB-10 F-25/F-26 |
| FW-B2 | **`MOTOR_PRESENT` (`J10-12` pin 3, GPIO17) always reads low**: PCB-03 is gone and the 100 kΩ pull-down holds it. Do not treat it as a fault | D-093, PCB-10 README | — |
| FW-B3 | Keep the D-038 speed clamp (`6.0 V / V_bus` duty limit) and the latching fault on `FLT`; `V_bus` now comes from C0's INA226 reading | power-boards §2.4 | N4 |
| FW-B4 | Read the LSM6DSOX on `J10-7` (SPI); check WHO_AM_I | D-094 M7 | N10 |

## 4. Audio (C0)

| ID | Requirement | Source | Proved by |
|---|---|---|---|
| FW-A1 | **Custom device-tree overlay:** an I²S0 pin group of GPIO 18–22 only (keep GPIO23 `AMP_SD` and GPIO24 `FAN_EN` out of it), one clock, four capture channels on SDI0 (front pair) and SDI1 (rear pair), playback on SDO0. Start from the HiFiBerry DAC8x/ADC8x overlay and `rpi-simple-soundcard` path (Raspberry Pi RP-009699), which muxes GPIO 18–27 and so cannot be used as is | D-093 Q6, PCB-09 README | N9 |
| FW-A2 | Drive GPIO23 `AMP_SD` to mute the amp when no audio plays | D-067 CR-01 | N9 |
| FW-A3 | Prove four-channel capture on loose breakouts before the shell bosses are printed. Fallback: the front pair alone on SDI0 with a stock two-channel path | D-093 R8 | N9, N11 |

## 5. Not firmware's job any more

The permit chain, `SYSTEM_ARM`, `PERMIT_OK`, `ARM_REQ`, `ENERGY_OK`, `CHARGE_ABSENT`, `SEQ_EN`, the power-good lines (`PG_*`), `HEAD_OC` and `HEAD_PGOOD`, the charger's I²C (BQ25798) and the STUSB4500 NVM image. All of these were removed by D-093.
