# PCB-12 — C2 head carrier

Signals-only carrier for the ESP32-S3-Zero (C2): RS-422 head link, Feetech servo-bus buffers and the display RS-485 ([D-102](../../decisions.md#d-102)). It replaces the printed C2 tray in the head's roll frame. No watchdog since [D-093](../../decisions.md#d-093).

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-086 in [BOM.csv](../../BOM.csv) |
| Location | Head, roll frame, in place of the C2 tray's front wall |
| Specification | [feetech-link-contract.md](../feetech-link-contract.md) |
| CAD placeholder | [`layout_model.py`](../../03-head/v1/cad/layout_model.py) (only the ESP32-S3-Zero module is drawn) |
| CAD labels | `C2_ESP32_S3_Zero_23_5x18_footprint` |
| Final CAD | `Custom PCBs › PCB-12 C2 head controller` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Rev A draft complete** ([D-102](../../decisions.md#d-102)); [fab/revA](fab/revA/README.md) written (**do not order**) | [design/](design/): Nightly ERC 0/0, netlist audit 13/13 on 76 pins, parity DRC 0/0/0; [STEP](cad/pcb-12-c2-head-carrier-revA.step); [fit](../../final/v1/cad/check_pcb12_fit.py) 7/7 | 2026-11-10 |
| 2. Procure | Waits for the gates in [fab/revA](fab/revA/README.md#before-ordering) (D-064 batch) | Do not order fab/revA yet | — |
| 3. Integrate | — | — | — |

## Inputs

**[D-093](../../decisions.md#d-093) scope (2026-11-06).** Minimal safety: **no TPS3436 watchdog, no `ARM_REQ` output, no `C2_READY_H/L` pair** (PCB-03 and its permit chain are gone). The bought Waveshare ESP32 Servo Driver was checked and **does not fit** the head's C2 bay: it is 65 × 30 mm against the 18 × 23.5 mm vertical board envelope, and it carries a plain ESP32, not the S3 ([D-094](../../decisions.md#d-094)). So this carrier is designed. A custom carrier keeps the servo bus half-duplex interface, the RS-422 head link (J9-1 order per D-092) and the display link.

**Shared PCB-08/12 interface input ([D-100](../../decisions.md#d-100), 2026-11-09; not yet a schematic).** W43/`J8-7` is **signal-only**: pins 1/4/7/9 `GND_SIG`, 2/3 `C0TX+/−`, 5/6 `C2TX−/+`, 8 `SERVO_DATA`, 10–22 isolated. On PCB-08, `GND_SIG` joins the C0 link GND (`J8-4` pin 1) and the yaw servo ground (`J8-8` pin 1 / W17), so `SERVO_DATA` has its return beside it. W42/`J8-6` carries the head pitch/roll rail (now **6.3 V**, M2 per D-100 amendment) on 7 + 7 conductors and the C2 and display pairs on 2 + 2 each; those returns arrive as separate named nets. **PCB-12 must bond `GND_SIG` to its C2 logic ground near the RS-422 receiver and the servo-bus driver**, where all head grounds join. The resulting ground loop through W17, W24 and the star is accepted; measure W24 GND current at yaw stall and the C0↔C2 common-mode voltage under load. The 13/13 map (W43 10–21 as head power) is D-100's fallback only. Preserve all names, polarities and pin numbering across PCB-14's 1:1 joiner. [PCB-08 inputs](../pcb-08-yaw-junction/README.md#design-inputs-2026-11-09-preliminary).

**Head FFC orientation from PCB-14 ([D-101](../../decisions.md#d-101), 2026-11-10).** PCB-14 is a straight-through joiner: each conductor keeps its X, so the three head FFCs continue the cassette FFCs conductor for conductor. Conductor *n* of a head FFC is conductor *n* of its cassette FFC, which is contact *n* of `J8-6`/`J8-7` at PCB-08. Each head FFC leaves PCB-14's upper ZIF with **conductor 1 on its −X edge** (upper contact 22). Lying flat in the disc channel and travelling +Y at yaw 0, conductor 1 is on the −X side. Follow that edge through the still-unrouted riser up the +Y leg to set the contact-1 end of PCB-12's receiving ZIFs; dual contacts do not undo a mirror. The CSI head run is a Raspberry Pi standard-mini cable, not part of PCB-12, and goes into PCB-14 with its pin-1 conductor at −X.

## Design (rev A, 2026-11-10)

**Scope ([D-102](../../decisions.md#d-102), builder).** PCB-12 carries signals only. The W42/W43 head FFCs end at a separate FFC-to-wire break in the pitch frame, a head-harness item still to be designed or bought. That break feeds servo power to the two servos and display power to D1, and sends the rest to PCB-12 on wires. The head FFC conductor-1 rule (above) applies at that break.

**Envelope, measured in the head CAD.** The C2 tray held only the bare Zero, with no carrier room. A voxel survey of the roll frame found the space below and beside the tray free. PCB-12 is one 0.8 mm board in the tray's front-wall plane, head-local **X −25.0…−24.2, Y −44…−14, Z 8…51.5** (30 × 43.5 mm):
- The Zero solders by its castellations onto the rear face at its old seat. USB-C stays up and BOOT/RESET stay reachable from the rear.
- Transceivers, buffers and headers sit below the Zero, with the plugs mating rearward.
- The printed tray and its screws are removed. Two M2 × 4 button screws at Y −41.5/−16.5 (roll-axis height) go into new crossbar bosses with M2 inserts (`PCB12` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py)).

**Interfaces** (also in [05-harness §5](../../05-harness/README.md#5-pinouts-and-polarity)).

| Ref | Part | Pins |
|---|---|---|
| J1 | JST GH BM07B-GHS-TBT | 1 `GND_SIG`, 2 `C0TX_P`, 3 `C0TX_N`, 4 `C2TX_N`, 5 `C2TX_P` (J9-1 order, D-092), 6 `+5V_C2`, 7 GND (C2 return) |
| J2 | JST GH BM02B-GHS-TBT | 1 `GND_HEAD_REF`, 2 `SERVO_DATA` |
| J3 | JST GH BM03B-GHS-TBT | 1 `GND_DISPLAY`, 2 `DISP_B`, 3 `DISP_A` (D1's RS-485 port) |

**Circuit** ([schematic](design/pcb-12-c2-head-carrier.kicad_sch), [PDF](design/pcb-12-c2-head-carrier-schematic.pdf), written by [build_schematic.py](design/build_schematic.py) from stock Nightly symbols).
- **U1 ESP32-S3-Zero** (Waveshare SKU 25081, without header). Its ME6217 LDO (800 mA) makes +3V3 from `+5V_C2` (C1, 10 µF bulk). Only pads all pinout sources agree on are used:

  | GPIO | Net |
  |---|---|
  | 1 | DISP_TX |
  | 2 | DISP_DE |
  | 4 | DISP_RX |
  | 5 | LINK_TX |
  | 6 | LINK_RX |
  | 7 | SERVO_RX |
  | 8 | SERVO_TX |
  | 9 | SERVO_DIR |

  GPIO3 (strapping) and pads 13–18 (GPIO13/RX/TX, order disputed; GPIO10–12) are unused. The land pattern is [`Waveshare_ESP32-S3-Zero_Castellated`](../lib/generate_esp32s3_zero.py): 2 × 9 at 2.54 mm, rows 15.24 mm apart, pads 3.0 × 1.5 mm across the castellated edges, antenna keep-out on both layers, bottom pads not landed.
- **U2 THVD1451** head link, as PCB-09's. It receives C0TX (R2, 120 Ω, here) and drives C2TX; R3 4.7 kΩ holds LINK_TX idle high.
- **U3 SN74LVC1G126 / U4 SN74LVC1G125**, the one-wire servo bus. SERVO_DIR high transmits through U3 and R4 (47 Ω); low receives through U4. R6 10 kΩ holds receive at boot, and R5 10 kΩ is the bus's only pull-up, to 3.3 V. LVC inputs and disabled outputs tolerate 5.5 V, with Ioff (feetech-link-contract).
- **U5 THVD1450** display RS-485, half duplex. DE and /RE are tied, with R9 10 kΩ holding receive. There is no termination: the fail-safe receiver covers a short 115 200-baud run. The schematic symbol is LTC2850xS8 (same pinout), because the nested derived THVD1450D symbol fails ERC's library match.
- **Grounds (D-100):** R1 (`GND_SIG`), R7 (`GND_HEAD_REF`) and R10 (`GND_DISPLAY`) are 0 Ω links to C2 logic ground, so any one can become a ferrite at the bench. TP1 is a GND bench pad.

**Checks.** ERC **0/0** ([report](design/schematic-erc.rpt)). [audit_netlist.py](design/audit_netlist.py) **13/13** on 76 pins ([netlist-audit.json](design/netlist-audit.json)): J9-1 order, RS-422 polarity both ways, C0TX terminated here only, one 0 Ω bond per ground, the single 3.3 V bus pull-up, complementary buffer enables, display DE/RE tied, agreed Zero pads only, Zero power, no servo or display power on the board, logic on 3V3.

## Layout (rev A)

[layout_pcb12.py](design/layout_pcb12.py) writes the board **headless**. For each symbol it builds a skeleton block, swaps it for the library land pattern with `kfile.replace_footprint`, then places, routes and pours. Mapping: KiCad x = 71 − Y, y = 139.75 − Z, component face −X.
- **Board:** 2 layers, 0.8 mm, 1 oz. M2 holes are Edge.Cuts circles with F.Cu keep-outs under the screw heads.
- **Escape:** signals leave the Zero's pad outer ends into side strips. The left strip carries the display and link lanes, the right strip the servo lanes. Nothing but power vias is routed under the module.
- **Placement:** display group (U5, J3) on the left, link group (U2 straight down to J1, R2 inline on the pair) in the middle, servo group (U4/U3 with R4 between, J2 above) on the right.
- **Power and ground:** +5V_C2 and +3V3 trunks run on B.Cu under the left pad row, outside the antenna keep-out. B.Cu is a GND plane, with an F.Cu GND pour everywhere except under the module.
- **Crossings:** two on B.Cu (SERVO_DIR to U4).
- **DRC:** Nightly `--schematic-parity` with the fab-neutral rules: **0 / 0 / 0** ([report](design/placement-drc.json)). A scratch copy with a 0.8 mm via minimum flagged all 20 vias, which proves the rules file is enforced.
- **STEP:** [cad/pcb-12-c2-head-carrier-revA.step](cad/pcb-12-c2-head-carrier-revA.step), with Waveshare's Zero model (`lib/pcb12.pretty`) and KiCad's IC, connector and passive models.

**Fit ([`check_pcb12_fit.py`](../../final/v1/cad/check_pcb12_fit.py), 7/7, [report](../../final/v1/cad/check_pcb12_fit-report.json)).**
- Core at X −25.0…−24.29; Zero model on its seat (Y/Z within 0.01 mm).
- Every part and mated GH plug envelope (9 mm rearward, `E`) clear at neutral.
- Screws through the holes, heads 1.75 mm from the Zero; bosses 0.09 mm behind the board, 1.8 mm from the display frame.
- USB-C and BOOT/RESET service reserves free.
- 25-pose roll × pitch sweep clear, nearest **1.57 mm** (−Y yoke leg, roll −21° and pitch 43°).

The first layout put J2 in the board's low −Y corner. That corner sweeps into the −Y yoke leg, so a placement map moved J2 into the servo group.

**Not done here.** Stage 3 (the real board replacing `C2_ESP32_S3_Zero_23_5x18_footprint` in `pcb_integration.py`), rebuilding the whole-robot STEPs, the head mass register (tray off, board on), and the head-harness break.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): watchdog, `ARM_REQ` and READY pair dropped; Waveshare ESP32 Servo Driver fit check comes first.
- **2026-11-07:** [D-094](../../decisions.md#d-094): Waveshare board doesn't fit the C2 bay; this stays a simplified custom carrier.
- **2026-11-09:** PCB-08/12 W43 candidate interface and return-current measurement gate recorded before either schematic is frozen.
- **2026-11-09:** interface updated for D-100: J8-7 signal-only with `GND_SIG` (C0 link GND + yaw servo ground on PCB-08); bond to C2 logic ground here; head rail 6.3 V after the routed-board amendment.
- **2026-11-10:** PCB-14 rev A ([D-101](../../decisions.md#d-101)): head FFC conductor 1 arrives on the −X edge (straight-through joiner); recorded as an input.
- **2026-11-10:** rev A draft ([D-102](../../decisions.md#d-102)): signals-only carrier replacing the C2 tray (30 × 43.5 mm, 0.8 mm), head FFCs end at a separate head-harness break. ERC 0/0, netlist audit 13/13, parity DRC 0/0/0, fit 7/7 through the roll/pitch envelope; fab/revA written, do not order.
