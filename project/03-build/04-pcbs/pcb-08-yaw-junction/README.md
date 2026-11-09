# PCB-08 — Yaw junction

Stationary end of the clock spring: body-side power and signal connectors to the cassette FFCs (`J8-6`, `J8-7`).

**[D-093](../../decisions.md#d-093) scope (2026-11-06).** PCB-02 and PCB-03 are bought modules now, so the `W23a` (`J8-3`) and `W23b` (`J8-5`) permit and status cables and the D-082 `ARM_REQ` conductor are gone. PCB-08 **gains the yaw servo plug** that was PCB-03 `J3-5`: Feetech 5264-3P, 1 GND, 2 `+11V1_YAW` (from the bought yaw buck-boost, 11.1 V), 3 `SERVO_DATA` (from C2 through W43). It keeps `J8-1` (head power from the bought modules), `J8-4` (RS-422 head link, J9-1 order per D-092) and the `J8-6`/`J8-7` cassette FFCs. Reassign the freed W43 conductors at design.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-083 in [BOM.csv](../../BOM.csv) |
| Location | Body, under the yaw adapter plate |
| Specification | [05-harness](../../05-harness/README.md)<br>[D-039](../../decisions.md#d-039), [D-044](../../decisions.md#d-044) |
| CAD placeholder | `_yaw_junction_board()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `YAW_JUNCTION_PCB08` |
| Final CAD | `Custom PCBs › PCB-08 yaw junction` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | Inputs in progress | Interface and connector study below; no KiCad revision yet | 2026-11-09 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Design inputs (2026-11-09; preliminary)

The board is a passive stator junction: it distributes three head power/return pairs from `J8-1` to `J8-6`, passes the two RS-422 pairs from `J8-4` through `J8-7`, brings `SERVO_DATA` back from `J8-7` to the body-fixed yaw `J8-8`, and takes the yaw rail/return from `W17` pads to `J8-8`. There is no `ARM_REQ`, permit chain, or old `J8-3`/`J8-5` header. No 11.1 V yaw power goes onto either FFC. See [D-093](../../decisions.md#d-093), [D-092](../../decisions.md#d-092), the [harness pinouts](../../05-harness/README.md#5-pinouts-and-polarity), and the [servo link contract](../feetech-link-contract.md).

| Interface | Fixed electrical contract | Board action |
|---|---|---|
| `J8-1`, Micro-Fit 3.0 2×3, right-angle, mating −X | 1 `+5V5_HEAD_PR`, 2 `+5V_C2`, 3 `+5V_DISPLAY`, 4 `GND_HEAD`, 5 `GND_C2`, 6 `GND_DISPLAY` | Preserve the three supply/return pairs; do not use a signal return as a power-current shortcut |
| `J8-4`, GH6 | 1 GND, 2 `C0TX+`, 3 `C0TX−`, 4 `C2TX−`, 5 `C2TX+`, 6 spare | Pass both differential pairs to `J8-7` in the same polarity. Keep pin 6 isolated unless a later interface decision assigns it |
| `J8-6`, 22-way power FFC | Pitch/roll 7 positive + 7 return; C2 2 + 2; display 2 + 2 | A conductor may carry no more than its connector and cable rating; pair the same rail only at the board ends |
| `J8-7`, 22-way sideband FFC | RS-422 pairs, signal reference and `SERVO_DATA`; former permit/status nets removed | Allocate explicit grounds beside signal groups; leave unused contacts unconnected and labelled, never silently repurpose them as power |
| `W17` → `J8-8`, yaw servo | `J8-8`: 1 GND, 2 `+11V1_YAW`, 3 `SERVO_DATA` | W17 enters on rated pads/strain relief; check the received servo cable by cavity number before energizing |

**Candidate FFC maps, pending power-drop and cable-orientation decision.** Number by the *connector's marked contact number* at PCB-08, then measure whether each cable arrives straight or mirrored at PCB-14. PCB-14 remains 1:1; its physical orientation must not reverse these names. `J8-6` candidate: 1–7 `+5V5_HEAD_PR`, 8–14 `GND_HEAD`, 15–16 `+5V_C2`, 17–18 `GND_C2`, 19–20 `+5V_DISPLAY`, 21–22 `GND_DISPLAY`. `J8-7` signal candidate: 1 GND reference, 2 `C0TX+`, 3 `C0TX−`, 4 GND reference, 5 `C2TX−`, 6 `C2TX+`, 7 GND reference, 8 `SERVO_DATA`, 9 GND reference. Pins 10–22 are **reserved for the head-rail voltage-drop decision**, not assumed isolated or free for unrelated signals. One deliberate option is 10–15 `GND_HEAD`, 16–21 `+5V5_HEAD_PR`, 22 isolated: 13 positive and 13 return paths across W42+W43. This is not yet a schematic netlist. The GND reference source and head-end return must be resolved with PCB-12; the separate `J8-1` returns must not be unintentionally joined on the stator.

**Current and voltage-drop screen (`E`, not a measured cable).** FH34SRJ is rated 0.5 A/contact. Seven equal-sharing contacts have a nominal 3.5 A sum against the 2.8 A head allowance; two have 1.0 A for each C2/display branch. For voltage, assume copper resistivity 0.01724 Ω·mm²/m, conductor width 0.3 mm, total FFC length 0.3 m, four ZIF contact interfaces in series, and the FH34SRJ specification's 0.1 Ω maximum per contact **including 8 mm of FFC bulk**. Adding that limit to the full cable length double-counts a small portion, so it is deliberately conservative. The table is reproduced by [`head_power_drop.py`](head_power_drop.py). It shows a 0.035 mm conductor and a thinner 0.027 mm sensitivity case. The latter matches the nominal copper thickness in Raspberry Pi's **standard-mini display cable drawing**, but neither case is a claim about the actual BO-050 mini-mini or power FFC. [FH34SRJ specification](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Raspberry Pi cable drawing](https://pip-assets.raspberrypi.com/categories/903-flexible-printed-circuit-fpc-cable-for-display-and-camera/documents/RP-008145-DS-1-mini-display-cable-200mm-reference-drawing.pdf).

| Copper thickness | Head positive/return conductors | Calculated loop Ω | Drop at 2.8 A | Terminal at 5.5 V | Terminal at 6.0 V |
|---:|---:|---:|---:|---:|---:|
| 0.035 mm | 7 / 7 | 0.255 | 0.714 V | 4.79 V | 5.29 V |
| 0.027 mm | 7 / 7 | 0.297 | 0.831 V | 4.67 V | 5.17 V |
| 0.035 mm | 13 / 13 | 0.137 | 0.384 V | 5.12 V | 5.62 V |
| 0.027 mm | 13 / 13 | 0.160 | 0.447 V | 5.05 V | 5.55 V |

The present **5.5 V setpoint fails the 5.23 V N2 terminal target** even with all 13 W43 spare conductors allocated optimally in this screen. A provisional 6.0 V M2 setpoint **plus six extra positive and six extra return conductors on W43** clears it in both sensitivity cases. D-046 already identified 6.0 V as the preferable setpoint once yaw has its own rail; the STS3045M is specified for 4.8–7.4 V. This is a design proposal, not a changed M2 setting or frozen FFC map: the M2 capacity at 2.8 A, loaded output, cable resistance/current sharing, C2/display peaks, signal coupling and N2 bench result still gate it. [D-046](../../decisions.md#d-046); [M2 selection](../../module-selection.md).

**Shared mechanical candidate.** FH12-22S-0.5SH is **out for PCB-08 and PCB-14**: its 6.4 mm depth exceeds PCB-14's 5.2 mm limit. FH19SC-22S is 13 × 3 × 0.93 mm, but Hirose marks it **not recommended for new designs**. The active FH34SRJ-22S-0.5SH(99) is 13 × 3.8 × 1.0 mm, takes 0.3 ± 0.03 mm FFC/FPC and has top/bottom contacts. Mouser India lists the exact part. This is the leading family for **all eight ZIFs** (PCB-08 ×2, PCB-14 ×6), subject to the actual 22-to-22 CSI cable stiffener, pin order, footprint and populated fit. Dual contact does not undo a pin-1 ↔ pin-22 mirror. [FH12](https://www.hirose.com/en/product/p/CL0586-0532-7-55); [FH19SC](https://www.hirose.com/en/product/p/CL0580-0506-9-09); [FH34SRJ](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Mouser India](https://www.mouser.in/en/ProductDetail/Hirose-Connector/FH34SRJ-22S-0.5SH99).

**PCB-08 envelope probe.** The CAD placeholder is a 32 × 21 × 1.6 mm plate at world X −22..10, Y −44..−23, Z 112..113.6, with a 10 × 17.5 mm extension at X 10..20, Y −42..−24.5. [`check_pcb08_zif_envelopes.py`](../../final/v1/cad/check_pcb08_zif_envelopes.py) uses the FH34SRJ **body** dimensions and straight stiffened-exit boxes against the full robot tree. Two same-face bodies fit in X but an outward-facing inner cable crosses the outer body. A back-to-back lower ZIF and its cable exit intersect the Pi 5 **bounding envelope** (27.14 and 11.07 mm³); the top ZIF is clear. Opposing the mouths on the top face gives a clear *straight inward exit* for one cable, but demands a separate bend/service-route study to bring it toward the +X cassette. Thus neither placement has passed the real land pattern, open-actuator and mated-exit check. The [report](../../final/v1/cad/check_pcb08_zif_envelopes-report.json) is **6/8 with the two back-to-back failures**. Do not fix the outline or choose the assembly side from body boxes alone.

**Yaw connector naming.** Feetech calls the servo cable `5264-3P`; Molex's 5264 is the *cable receptacle* series, while its mating 3-circuit, 2.50 mm vertical PCB header is 5267 / 22035035. Treat the CAD `5264-3P header` as an envelope label, not a footprint selection. Check the received cable's key, pitch and cavity numbering against a sample before selecting the header and accepting the J8-8 fit. [Feetech servo specification](https://www.feetechrc.com/Data/feetechrc/upload/file/20240507/6385067068652648096680943.pdf); [Molex 5264](https://www.molex.com/en-us/products/series-chart/5264); [Molex 5267](https://www.molex.com/en-us/products/series-chart/5267).

**Next design gate.** Verify the received or exact-order 22-to-22 camera FPC thickness/stiffener, then make an FH34SRJ land pattern and real connector/actuator CAD probe for PCB-08 and PCB-14 together. Resolve PCB-08's inward cable turn or change its extension/outline, confirm the M2 6.0 V proposal and 13/13 head map against measured FFC resistance, and freeze `J8-7` reference ground with PCB-12. Then build the KiCad schematic, ERC/netlist audit, footprint placement, routed board and parity DRC. This board is not ready for fab output or order.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): loses the `W23a`/`W23b` permit and status sideband and `ARM_REQ`; gains the yaw servo plug.
- **2026-11-07:** [D-095](../../decisions.md#d-095) CAD: the J8-3/J8-5 placeholders are removed and the yaw servo plug sits where J8-3 was, as a Feetech 5264-3P top-entry header (ID `J8-8` proposed) at X -9.5..0.4, Y -42.6..-36.85 on the board, mated plug above it to Z 126 (`PCB08_SERVO` in `final/v1/cad/makad-v1.step.py`; `check_pcb08_servo_plug.py` 5/5). Header body and plug are envelopes (E) until the footprint is chosen at design.
- **2026-11-09:** Shared PCB-08/14 FH34SRJ input study, BO-050 mini-mini cable correction and head-rail drop screen. CAD body/straight-exit probe rejects a back-to-back pair over the Pi and two same-face outward mouths; opposing top-side mouths need a cable-turn study. No connector or rail setting frozen for fabrication.
