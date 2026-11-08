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

**Candidate FFC maps, pending connector and cable orientation.** Number by the *connector's marked contact number* at PCB-08, then measure whether each cable arrives straight or mirrored at PCB-14. PCB-14 remains 1:1; its physical orientation must not reverse these names. `J8-6` candidate: 1–7 `+5V5_HEAD_PR`, 8–14 `GND_HEAD`, 15–16 `+5V_C2`, 17–18 `GND_C2`, 19–20 `+5V_DISPLAY`, 21–22 `GND_DISPLAY`. `J8-7` candidate: 1 GND reference, 2 `C0TX+`, 3 `C0TX−`, 4 GND reference, 5 `C2TX−`, 6 `C2TX+`, 7 GND reference, 8 `SERVO_DATA`, 9 GND reference, 10–22 isolated. The GND reference source and head-end return must be resolved with PCB-12 before this becomes a schematic netlist; the separate `J8-1` returns must not be unintentionally joined on the stator.

**Current screen.** Hirose rates the FH12-22S-0.5SH(55) and FH19SC-22S-0.5SH(09) at 0.5 A per contact. Seven equal-sharing contacts have a nominal 3.5 A sum in each direction against the 2.8 A head pitch/roll allowance; two have a nominal 1.0 A sum for each C2/display branch. Equal sharing, the actual FFC copper, bend-cycle heating and C2/display peak currents are unproved. Measure and qualify the complete cable plus both PCB-14 ZIFs, rather than treating the contact rating sum as a cable rating. [FH12 product](https://www.hirose.com/en/product/p/CL0586-0532-7-55); [FH19SC product](https://www.hirose.com/en/product/p/CL0580-0506-9-09).

**Mechanical envelope.** The existing CAD placeholder is a 32 × 21 × 1.6 mm plate at world X −22..10, Y −44..−23, Z 112..113.6, with a 10 × 17.5 mm +X FFC extension at X 10..20, Y −42..−24.5. Its ZIF pair is only a reserve block, not two fitted connector models. The stock KiCad footprint for FH12-22S-0.5SH is available, and Hirose specifies a 15.1 × 6.4 × 2.0 mm connector: two beside each other need at least 12.8 mm in X before courtyard/actuator clearance, exceeding the 10 mm extension. FH19SC-22S is 13 × 3 × 0.93 mm, but Hirose marks it **not recommended for new designs**. A promising active candidate is the FH34SRJ-22S-0.5SH(99): 13 × 3.8 × 1.0 mm, 0.3 mm FFC/FPC, top and bottom contact, 0.5 A/contact. Two bodies nominally use 7.6 mm of the 10 mm extension; this is **not yet a courtyard, actuator or cable-exit fit**. Place both real land patterns and open actuators, verify the PCB-14 mating orientation and rerun populated CAD fit before selecting it or fixing the outline. [FH12 product](https://www.hirose.com/en/product/p/CL0586-0532-7-55); [FH19SC product](https://www.hirose.com/en/product/p/CL0580-0506-9-09); [FH34SRJ product](https://www.hirose.com/en/product/p/CL0580-1254-3-99).

**Yaw connector naming.** Feetech calls the servo cable `5264-3P`; Molex's 5264 is the *cable receptacle* series, while its mating 3-circuit, 2.50 mm vertical PCB header is 5267 / 22035035. Treat the CAD `5264-3P header` as an envelope label, not a footprint selection. Check the received cable's key, pitch and cavity numbering against a sample before selecting the header and accepting the J8-8 fit. [Feetech servo specification](https://www.feetechrc.com/Data/feetechrc/upload/file/20240507/6385067068652648096680943.pdf); [Molex 5264](https://www.molex.com/en-us/products/series-chart/5264); [Molex 5267](https://www.molex.com/en-us/products/series-chart/5267).

**Next design gate.** Select the two ZIFs and FFC stock together; prove contact orientation, open-actuator access and both mated cable exits in the real CAD envelope. Freeze `J8-7` GND source with PCB-12 and confirm power-FFC peak current. Then build the KiCad schematic, ERC/netlist audit, footprint placement, routed board and parity DRC. This board is not ready for fab output or order.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): loses the `W23a`/`W23b` permit and status sideband and `ARM_REQ`; gains the yaw servo plug.
- **2026-11-07:** [D-095](../../decisions.md#d-095) CAD: the J8-3/J8-5 placeholders are removed and the yaw servo plug sits where J8-3 was, as a Feetech 5264-3P top-entry header (ID `J8-8` proposed) at X -9.5..0.4, Y -42.6..-36.85 on the board, mated plug above it to Z 126 (`PCB08_SERVO` in `final/v1/cad/makad-v1.step.py`; `check_pcb08_servo_plug.py` 5/5). Header body and plug are envelopes (E) until the footprint is chosen at design.
