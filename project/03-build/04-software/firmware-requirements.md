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
| FW-P1 | Read the INA226 (M6) on I²C1 (GPIO2/3, address 0x40 unless taken). Use its **bus voltage under load** as the battery measure, not an open-circuit estimate | D-094 M6, D-096 | N6 |
| FW-P2 | **Low-battery stop:** at a loaded bus voltage of 6.0 V (threshold to re-register after N6), command C2 and C3 to stop all motion and hold torque off | RP-02 §8.1 soft-critical, D-093 | N6 |
| FW-P3 | **Low-battery shutdown:** after FW-P2, shut the Pi down cleanly, then turn M1 off (FW-P5) before the TIFPS0629 under-voltage trip. Filter for load peaks: a coincident stall can pull each cell about 0.35 V below its resting voltage (cell resistance only), so no shutdown on a single sample | D-096 duration screen | N6 with a peak-load pulse at the 6.0 V point |
| FW-P4 | **Power button:** a press while on (sensed through a qualified high-impedance interface, never the M1 ON pad directly) starts an orderly shutdown | D-093 Q1, D-096 `W40` | N1(a) |
| FW-P5 | **Power off:** after shutdown, pulse M1's OFF input (> 1 V); never drive M1 ON from a GPIO | D-094 M1, D-096 | N1(a) |
| FW-P6 | Leave the Pi in its non-PD 5 V / 3 A mode: do **not** set `PSU_MAX_CURRENT` or `usb_max_current_enable`. USB peripherals stay within 600 mA | D-094 M4, Raspberry Pi RP-009856 | N12 |
| FW-P7 | Log `vcgencmd get_throttled` at boot and during operation; report any under-voltage flag | D-094 M4 | N12(c) |
| FW-P8 | No sequencing logic: every rail comes up together. Each controller must tolerate the others starting in any order | D-093 | N7 |
| FW-P9 | Charging happens only in `OFF`. Firmware cannot see the charger; the operating rule is in the user notes | D-093 | N5 |

**Open interface (blocks FW-P1, FW-P4 and FW-P5 wiring).** D-096 puts the button sense on GPIO12 (header pin 32) and the M1 OFF drive on GPIO13 (pin 33). On [PCB-09 rev A](../04-pcbs/pcb-09-c0-link-adapter/README.md) both pins are **not connected**, and the full SSW-120 socket covers the header, so nothing else can reach them (PCB-09 HA-02). I²C1 is reachable only on PCB-09's labelled SDA/SCL/GND service pads (D-073); the INA226's 3.3 V supply also needs an accessible pad. **Resolution needed before harness build:** a PCB-09 rev B adding pads for GPIO12, GPIO13 and 3V3 (PCB-09 is not fabricated yet, so this costs a layout edit, not a scrapped board), or reassign these jobs to another controller, by decision.

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
