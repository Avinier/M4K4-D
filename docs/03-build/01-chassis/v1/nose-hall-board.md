# Nose Hall board (CH-064) and contact trip point

**Status:** design, not ordered or built. Decision [D-013](../../decisions.md#d-013). CAD: `NOSE_HALL_*` and `NOSE_MAGNET` in [`body_chassis_model.py`](cad/body_chassis_model.py).

The touch cap carries a magnet. A linear Hall sensor on a small board in the pod seat reads it, and the C3 firmware decides when the cap counts as pressed. Nothing mechanical is struck, so the cap uses its full 3 mm stroke to the pod-face stop. The ESE22MV21 detector switch chosen in D-011 is dropped: it bottoms out at 2.05 mm.

## Parts

| Ref | Part | Notes |
|---|---|---|
| U1 | TI DRV5055A3QDBZR, SOT-23 | Ratiometric linear Hall sensor. At 3.3 V: 15 mV/mT (14.3–15.8), 1.65 V output at zero field, ±88 mT linear range, 20 kHz bandwidth, 10 µs delay, 2 mA. It senses the field perpendicular to the package top. [Datasheet](https://www.ti.com/lit/ds/symlink/drv5055.pdf) |
| C1 | 100 nF X7R 0402, 10 V | Supply decoupling between U1 VCC and GND (the datasheet asks for ≥ 10 nF) |
| R1, C2 | 1 kΩ 0402 and 100 nF 0402 | 1.6 kHz RC low-pass on OUT at the board. It filters cable pickup and adds about 0.1 ms of delay, far below the cap's contact time |
| Magnet (CH-065) | NdFeB N35, Ø2 × 1 mm, magnetised through the thickness | Pressed and glued (CA) into the cap's Ø2.06 × 1 mm pocket, **south pole toward the sensor**, so the output rises when the cap is pushed |
| Springs (CH-066) | 2 × stainless compression spring, OD 3.0, wire 0.25, free length 10, about 10 coils (solid ≈ 2.5 mm) | In Ø3.3 × 6 mm seat pockets at Y ±3, Z 32. Installed length 9.0 mm, 6.0 mm at the stop. Estimated rate ≈ 0.2 N/mm each, so about 0.4 N preload and about 1.6 N at the stop for the pair. Confirm the rate on the received part |

## Board

- **Outline and stack:** 6.0 (Y) × 4.6 (Z) × 0.8 mm FR4, two layers, 1 oz copper, HASL or ENIG.
- **Mounting:** the board stands vertically in a 6.2 × 1.0 mm slot in the pod seat, which is open at the top. Its world span is X 126.6–127.4, Y 7.0–13.0, Z 30.4–35.0.
- **Front face (+X):** U1 is centred at board-local (Y 3.0, Z 2.2), which is world (Y 10.0, Z 32.6). The package's long axis runs along Y, and U1 sits in a notch through the seat's front face. C1 goes beside it at local (5.2, 2.2).
- **U1 land pattern:** IPC-7351 SOT-23-3.
- **Back face:** R1 and C2 go at local Z 1.0–2.0. Three wire pads, 0.8 × 1.2 mm, sit at local Y 2.9 / 4.0 / 5.1 and Z 3.4–4.6: +3V3, GND, OUT, in that order. They lie in line with the pod's lead groove (world Y 9.5–12.5, Z 33.5–35).
- **Vias:** 0.3 mm drill, connecting the front and back.
- **Retention:** the slot holds the board with 0.1 mm per side of clearance. Fix it with a drop of CA or hot glue at the slot top. No force acts on it: the magnet never touches the package, and 0.1 mm of air remains at the stop.

| Net | U1 pin | Goes to |
|---|---|---|
| +3V3 | 1 VCC | C1, wire pad 1 |
| GND | 3 GND | C1, C2, wire pad 2 |
| HALL_OUT | 2 OUT | through R1 to wire pad 3, with C2 from pad 3 to GND |

## J10-8 cable (PCB-10 carrier, GH 5-circuit)

| Pin | Signal | Load |
|---:|---|---|
| 1 | +5V | GP2Y0A41SK0F Vcc |
| 2 | GND | GP2Y and Hall board |
| 3 | GP2Y_VO | GP2Y analog output |
| 4 | +3V3 | Hall board VCC |
| 5 | HALL_OUT | C3 ADC input, 0–3.3 V |

This reassigns pins 4 and 5, which were the switch pair. The PCB-10 carrier must route +3V3 and an ADC-capable GPIO to J10-8 instead of a switch input. Powering the Hall sensor from the ADC's 3.3 V supply keeps the reading ratiometric.

## Trip point

The Hall plate sits 0.65 mm under the package top (confirm on TI's mechanical drawing). That puts it 3.75 mm from the magnet face at rest and 0.75 mm at the 3 mm stop. The field was computed from the on-axis field of a cylindrical magnet with Br = 1.19 T.

| Cap travel (mm) | 0 | 0.5 | 0.75 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| Field (mT) | 7.3 | 10.5 | 12.8 | 15.7 | 25.0 | 42.6 | 160 (saturated) |
| Output change (mV, at 15 mV/mT) | 0 | +48 | +82 | +126 | +265 | +529 | clipped at 3.1 V |

**Firmware:**

1. At boot, with the cap untouched, take the rest reading as the median of 64 samples.
2. Reject the rest reading as a fault if it falls outside 1.65 V + 2–15 mT (1.68–1.88 V). Nominal is 7.3 mT (1.76 V); a missing magnet reads about 1.65 V.
3. **Trip (pressed)** at rest + 5 mT (+75 mV). **Release** at rest + 3 mT (+45 mV).
4. Sample at ≥ 1 kHz and average 4 samples.
5. Treat a reading pinned near 0 V or 3.3 V at rest as a fault (board unplugged or shorted).

**Predicted trip:** 0.71 mm of cap travel nominal. The 0.50–0.95 mm range covers ±0.4 mm on the rest gap (print and assembly) and Br 1.13–1.25 T. Release is at about 0.48 mm. Sensor noise (0.2 mT peak to peak) is negligible against the 5 mT step. Static fields from the speaker magnet or the ballast are removed by the boot calibration.

**Bench check (item 19):** mount the pod and cap and log HALL_OUT against a dial indicator on the cap from 0 to 3 mm. Pass if the trip falls within 0.4–1.2 mm and the release is below the trip. Also record the push force at the trip and at the stop against the spring estimate.
