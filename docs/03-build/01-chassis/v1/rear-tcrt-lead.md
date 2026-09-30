# Rear TCRT lead (CH-020) and cliff reading

**Status:** design, not built. Decision [D-016](../../decisions.md#d-016), which replaces the D-015 board. CAD: `REAR_TCRT_LEAD_JOINTS` and `REAR_TCRT_PIGTAIL_*` in [`body_chassis_model.py`](cad/body_chassis_model.py), and `HARNESS_REAR_TCRT_J10_10_*` in `harness_routes()`. Checked by [`check_rear_keel.py`](cad/check_rear_keel.py).

There is no board in the keel. A 4-wire lead is soldered straight to the TCRT5000's legs, runs up out of the keel and through the body, and plugs into J10-10 on the controller carrier (PCB-10). The parts a breakout would carry sit on PCB-10 instead: the LED resistor, the LED switch and the load resistor.

## What it costs in service

- **Sensor swap:** undo the bezel screw, and drop the bezel and shims. Unplug J10-10 at PCB-10, cut the zip tie at the crossmember, and pull the sensor and lead out downward through the keel. Feed the new one up the same way. The body's rear panel must be off to reach J10-10.
- **Keel removal:** the lead passes through the keel, so pull the sensor out first (as above), then undo the four keel screws. There is no longer a disconnect at the keel.
- **Height change (J09):** add or remove shims with the lead in place. The 30 mm slack loop behind the crossmember takes up the ±2 mm.

## Parts

| Part | Spec | Notes |
|---|---|---|
| Sensor | Vishay TCRT5000, standard 3.5 mm leads | [Datasheet](https://www.vishay.com/docs/83760/tcrt5000.pdf). Collector current 0.5 / 1 / 2.1 mA (min/typ/max) at IF 10 mA, 5 mm to a mirror; peak response at 2.5 mm; about 0.4 relative at 10 mm |
| Lead | JST GH 4-way pre-crimped single-ended cable, AWG28, **350 mm**, GHR-04V-S housing on one end | Cut the loose end to length and solder it to the TCRT. The route from the keel to J10-10 is about 300 mm, including the 30 mm loop; 350 mm leaves room to trim |
| Joints | Heat-shrink over each solder joint (1.5 mm), then one 4.8 mm sleeve over all four and the package top | Modelled as a 7.4 × 4.6 mm envelope, 6.5 mm tall, above the package. The sleeve is also the strain relief at the sensor. It fits the 7.6 mm pocket, so the sensor can come out downward |
| Strain relief | CH-072 zip tie at the crossmember lug | Keep the slack loop between the tie and the keel |

**Wiring at the sensor**, labelled on the housing and mapped to the TCRT5000 pin marks:

| GH pin | Wire | TCRT pin |
|---:|---|---|
| 1 | LED_A | A (emitter anode) |
| 2 | LED_K | K (emitter cathode) |
| 3 | TCRT_OUT | C (collector) |
| 4 | GND | E (emitter of the phototransistor) |

Solder with a short dwell (the datasheet allows 260 °C for 10 s at 2 mm from the case). The standard leads are 3.5 mm long, which leaves about 2 mm to solder to; do not trim them.

## PCB-10 J10-10 circuit

| Ref | Part | Connection |
|---|---|---|
| R1 | 100 Ω 0603 | +3V3 → J10-10 pin 1 (LED_A); about 20 mA with VF 1.2 V |
| Q1 | Logic-level N-MOSFET, SOT-23, VGS(th) ≤ 1.5 V (AO3400A class) | Drain to pin 2 (LED_K), source to GND, gate on a GPIO (LED_EN) |
| R3 | 100 kΩ 0402 | Q1 gate to GND, so the LED stays off at boot |
| R2 | 10 kΩ 0603, **value set at the bench** | +3V3 → pin 3 (TCRT_OUT): phototransistor load and fail-safe pull-up. Try 22–47 kΩ if dark floors read too close to the cliff level |
| C3 | 1 nF 0402 | Pin 3 to GND at the ADC input |
| — | ESP32-S3 **ADC1** channel | Pin 3. ADC2 is unavailable while Wi-Fi runs |

This replaces the RP-06 schedule's W36 line (5 V, GND, analog, digital): there is no 5 V and no comparator. J10-10 stays a GH 4-way header.

**Fail-safe:** an unplugged lead, a broken wire or a dead LED all leave TCRT_OUT at +3V3 through R2, which reads as a cliff, so the robot stops.

## Reading and firmware

The phototransistor pulls TCRT_OUT down when the floor reflects the LED. A cliff or no floor leaves it high.

1. Sample TCRT_OUT with the LED off (V_off), switch LED_EN on, wait 300 µs, sample again (V_on), and switch it off. Signal = V_off − V_on. Repeat at 500 Hz or faster, at a few % duty.
2. **Cliff** when the signal falls below the threshold for 3 consecutive reads. The threshold is set at the bench to half the darkest floor's signal.
3. **Fault, treated as a cliff (stop):** V_off below 2.5 V (strong ambient IR or a short), or no signal on a known floor at boot.

**Expected signal (an estimate, to be replaced by bench data):** on a mirror at 10 mm with IF 20 mA, the collector current is about 1.1 mA typical (0.6–2.4 mA). That is the datasheet's 5 mm value, scaled by 0.4 / 0.7 from its distance curve and doubled for IF. Real floors are diffuse: expect tens of µA on dark tile and a few hundred µA on light floors. With R2 = 10 kΩ, light floors saturate the output, and a 20 µA dark floor gives only about 0.2 V of signal. That is why R2 is a bench value: the TCRT's best response is at 2.5 mm, and the design runs it at 10 mm. The analog line is about 300 mm long at 10 kΩ; C3 and the on/off subtraction handle pickup, and the bench log should confirm it with the motors running.

## Bench checks (to-do item 20)

- Log V_off, V_on and the signal at optical heights of 8, 10 and 12 mm (four, two and zero shims) over the real floors, dark and light, and over a table edge. Pass: the darkest floor's signal is at least 3 × the cliff signal, with R2 set.
- Repeat on one floor with both drive motors running.
- Unplug J10-10 and confirm the firmware stops (fail-safe).
- Shine a phone torch and daylight on it: V_off stays above 2.5 V, or the fault trips.
- Fit: the sensor, with its sleeved joints, drops out of the pocket and goes back in without forcing the lead.
