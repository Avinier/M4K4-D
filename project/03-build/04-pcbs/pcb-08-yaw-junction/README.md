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
| 1. Design | **Layout routed** (rev A draft); populated fit and fold mock-up open | [design/](design/): Nightly ERC 0/0, netlist audit 14/14 on 51 pins, parity DRC 0 violations / 0 unconnected / 0 parity; [STEP](cad/pcb-08-yaw-junction-revA.step) is incomplete for populated fit | 2026-11-09 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Design inputs (2026-11-09; preliminary)

The board is a passive stator junction: it distributes three head power/return pairs from `J8-1` to `J8-6`, passes the two RS-422 pairs from `J8-4` through `J8-7`, brings `SERVO_DATA` back from `J8-7` to the body-fixed yaw `J8-8`, and takes the yaw rail/return from `W17` pads to `J8-8`. There is no `ARM_REQ`, permit chain, or old `J8-3`/`J8-5` header. No 11.1 V yaw power goes onto either FFC. See [D-093](../../decisions.md#d-093), [D-092](../../decisions.md#d-092), the [harness pinouts](../../05-harness/README.md#5-pinouts-and-polarity), and the [servo link contract](../feetech-link-contract.md).

| Interface | Fixed electrical contract | Board action |
|---|---|---|
| `J8-1`, Micro-Fit 3.0 2×3, right-angle, mating −X | 1 `+6V0_HEAD_PR` (D-100), 2 `+5V_C2`, 3 `+5V_DISPLAY`, 4 `GND_HEAD`, 5 `GND_C2`, 6 `GND_DISPLAY` | Preserve the three supply/return pairs; do not use a signal return as a power-current shortcut |
| `J8-4`, GH6 | 1 GND, 2 `C0TX+`, 3 `C0TX−`, 4 `C2TX−`, 5 `C2TX+`, 6 spare | Pass both differential pairs to `J8-7` in the same polarity. Keep pin 6 isolated unless a later interface decision assigns it |
| `J8-6`, 22-way power FFC | Pitch/roll 7 positive + 7 return; C2 2 + 2; display 2 + 2 | A conductor may carry no more than its connector and cable rating; pair the same rail only at the board ends |
| `J8-7`, 22-way sideband FFC | RS-422 pairs, signal reference and `SERVO_DATA`; former permit/status nets removed | Allocate explicit grounds beside signal groups; leave unused contacts unconnected and labelled, never silently repurpose them as power |
| `W17` → `J8-8`, yaw servo | `J8-8`: 1 GND, 2 `+11V1_YAW`, 3 `SERVO_DATA` | W17 enters on rated pads/strain relief; check the received servo cable by cavity number before energizing |

**FFC maps ([D-100](../../decisions.md#d-100), pending cable orientation).** Number by the *connector's marked contact number* at PCB-08, then measure whether each cable arrives straight or mirrored at PCB-14. PCB-14 remains 1:1; its physical orientation must not reverse these names. `J8-6`: 1–7 `+6V0_HEAD_PR`, 8–14 `GND_HEAD`, 15–16 `+5V_C2`, 17–18 `GND_C2`, 19–20 `+5V_DISPLAY`, 21–22 `GND_DISPLAY`. `J8-7` is **signal-only**: 1 GND reference, 2 `C0TX+`, 3 `C0TX−`, 4 GND reference, 5 `C2TX−`, 6 `C2TX+`, 7 GND reference, 8 `SERVO_DATA`, 9 GND reference, 10–22 isolated and labelled. The 13/13 option (10–15 `GND_HEAD`, 16–21 head positive on `J8-7`) is the recorded fallback only if the measured FFC or N2 fails the 7/7 map. The GND reference source and head-end return must be resolved with PCB-12; the separate `J8-1` returns must not be unintentionally joined on the stator.

**Signal ground (builder, 2026-11-09; [D-100](../../decisions.md#d-100) amendment).** PCB-08 has one signal ground net, **`GND_SIG`**: `J8-4` pin 1 (C0 link GND over W24), `J8-7` pins 1/4/7/9, and `J8-8` pin 1 with the W17 yaw return. `SERVO_DATA` is a single-ended 1 Mbps half-duplex line from C2 to the yaw servo, so its return must run beside it on the `J8-7` references and meet the servo's own ground at `J8-8`. `GND_HEAD` (`J8-1` pin 4 → `J8-6` 8–14), `GND_C2` and `GND_DISPLAY` stay separate on PCB-08, each paired with its supply back to the star. PCB-12 bonds `GND_SIG` to C2 logic ground near the RS-422 receiver and servo-bus driver; all head grounds join there. **Accepted loop:** Pi → M4 → star → M3 → W17 → PCB-08 → W24 → PCB-09 → Pi. Most yaw stall current returns directly on W17, but some can share the W24 GND (GH, 1 A contacts); RS-422 is differential. **Bench:** W24 GND current at yaw stall, C0↔C2 common-mode voltage under simultaneous servo/display load, and `SERVO_DATA` edges at `J8-8`. **Fallback:** a series ferrite or low-value resistor between `J8-4` pin 1 and `GND_SIG` (leave a footprint at layout).

**Current and voltage-drop screen (`E`, not a measured cable).** FH34SRJ is rated 0.5 A/contact. Seven equal-sharing contacts have a nominal 3.5 A sum against the 2.8 A head allowance; two have 1.0 A for each C2/display branch. For voltage, assume copper resistivity 0.01724 Ω·mm²/m, conductor width 0.3 mm, total FFC length 0.3 m, four ZIF contact interfaces in series, and the FH34SRJ specification's 0.1 Ω maximum per contact **including 8 mm of FFC bulk**. Adding that limit to the full cable length double-counts a small portion, so it is deliberately conservative. The table is reproduced by [`head_power_drop.py`](head_power_drop.py). It shows a 0.035 mm conductor and a thinner 0.027 mm sensitivity case. The latter matches the nominal copper thickness in Raspberry Pi's **standard-mini display cable drawing**, but neither case is a claim about the actual BO-050 mini-mini or power FFC. [FH34SRJ specification](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Raspberry Pi cable drawing](https://pip-assets.raspberrypi.com/categories/903-flexible-printed-circuit-fpc-cable-for-display-and-camera/documents/RP-008145-DS-1-mini-display-cable-200mm-reference-drawing.pdf).

| Copper thickness | Head positive/return conductors | Calculated loop Ω | Drop at 2.8 A | Terminal at 5.5 V | Terminal at 6.0 V |
|---:|---:|---:|---:|---:|---:|
| 0.035 mm | 7 / 7 | 0.255 | 0.714 V | 4.79 V | 5.29 V |
| 0.027 mm | 7 / 7 | 0.297 | 0.831 V | 4.67 V | 5.17 V |
| 0.035 mm | 13 / 13 | 0.137 | 0.384 V | 5.12 V | 5.62 V |
| 0.027 mm | 13 / 13 | 0.160 | 0.447 V | 5.05 V | 5.55 V |

The **5.5 V setpoint fails the 5.23 V N2 terminal target** in this screen. At 6.0 V with the 7/7 map the terminals are **5.49 V at 2.0 A** (0.035 mm copper) and **5.41 V** (0.027 mm), and the cable-only 5.23 V target holds up to about **3.0 A** and **2.6 A**. **[D-100](../../decisions.md#d-100) selects M2 at 6.0 V, the 7/7 map and a signal-only `J8-7`, on the condition that the head pitch/roll total is limited to ≤ 2.4 A.** At 2.4 A in the thinner-copper screen, the terminal estimate is only **5.29 V**, 0.06 V over N2, before any extra rail droop. M2's capacity near a 6.0 V pack and the actual FFC drop must be measured in N2(b). The STS3045M is specified for 4.8–7.4 V, and D-046 already preferred 6.0 V. [D-046](../../decisions.md#d-046); [M2 selection](../../module-selection.md).

**Shared mechanical candidate.** FH12-22S-0.5SH is **out for PCB-08 and PCB-14**: its 6.4 mm depth exceeds PCB-14's 5.2 mm limit. FH19SC-22S is 13 × 3 × 0.93 mm, but Hirose marks it **not recommended for new designs**. The active FH34SRJ-22S-0.5SH(99) is 13 × 3.8 × 1.0 mm, takes 0.3 ± 0.03 mm FFC/FPC and has top/bottom contacts. Mouser India lists the exact part. This is the leading family for **all eight ZIFs** (PCB-08 ×2, PCB-14 ×6), subject to the footprint and populated fit. [D-100](../../decisions.md#d-100) makes the three cassette runs one generic 0.3 mm FFC, so the CSI cassette run no longer depends on a branded mini-mini cable; the head-side CSI run (Pi standard-mini, 0.309 ± 0.05 mm at its 22-way end) against FH34SRJ's 0.30 ± 0.03 mm remains a PCB-14 check. Dual contact does not undo a pin-1 ↔ pin-22 mirror. [FH12](https://www.hirose.com/en/product/p/CL0586-0532-7-55); [FH19SC](https://www.hirose.com/en/product/p/CL0580-0506-9-09); [FH34SRJ](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Mouser India](https://www.mouser.in/en/ProductDetail/Hirose-Connector/FH34SRJ-22S-0.5SH99).

**PCB-08 envelope probe.** The CAD placeholder is a 32 × 21 × 1.6 mm plate at world X −22..10, Y −44..−23, Z 112..113.6, with a 10 × 17.5 mm extension at X 10..20, Y −42..−24.5. [`check_pcb08_zif_envelopes.py`](../../final/v1/cad/check_pcb08_zif_envelopes.py) uses the FH34SRJ **body** dimensions and straight stiffened-exit boxes against the full robot tree. Two same-face bodies fit in X but an outward-facing inner cable crosses the outer body. A back-to-back lower ZIF and its cable exit intersect the Pi 5 **bounding envelope** (27.14 and 11.07 mm³); the top ZIF is clear. Opposing the mouths on the top face gives a clear *straight inward exit* for one cable, but demands a separate bend/service-route study to bring it toward the +X cassette. Thus neither placement has passed the real land pattern, open-actuator and mated-exit check. The [report](../../final/v1/cad/check_pcb08_zif_envelopes-report.json) is **6/8 with the two back-to-back failures**. Do not fix the outline or choose the assembly side from body boxes alone.

**Stepped stack and Pi survey (2026-11-09, [D-100](../../decisions.md#d-100)).** [`check_pcb08_zif_stepped.py`](../../final/v1/cad/check_pcb08_zif_stepped.py) **14/14** ([report](../../final/v1/cad/check_pcb08_zif_stepped-report.json)):
- **The back-to-back failure was the Pi's bounding box.** A face-by-face Bnd_Box survey of the Pi 5 STEP under the extension tops out at **Z 99.85**, 11.2 mm under a bottom-face ZIF. Back to back stays geometrically open as the fallback.
- **Selected: stepped stack.** Both ZIFs on the top face, mouths +X. The shared [FH34SRJ footprint](../lib/README.md) places the outer body at X 15.7–19.5 so its outer solder tab has **0.35 mm** clearance to the X 20 board edge, above D-062's 0.3 mm rule. The inner body is X 5.86–9.66; reserve X 4.0–10.7 × Y −40..−27 for its open actuator and straight cable exit. The inner cable has an assumed 1.0 mm straight exit, climbs 0.95 mm in an S-bend (R 3 mm, 3.24 mm run) and runs over the outer body at Z 114.9–115.2. **Plug the outer cable first and latch it**; the inner cable then lies over its actuator.
- Both bodies, the stiffener, bend, raised and outer cables and both opened actuators (1.8 × 3.4 mm, `E`) clear the robot's parts, and the column to Z 117.2 is free.
- The Hirose 22-way copper land pattern, 0.25 × 0.65 mm recommended signal-paste apertures for a 0.1 mm stencil, and a conservative body/pad courtyard are now drafted in the shared footprint. The assembler still needs to approve the stencil. The catalog specifies a 1.5 ± 0.3 mm exposed FFC area and a 2.5 ± 0.3 mm reinforcing section; these do not establish the probe's 1.0 mm straight exit. The S-bend is still represented by an enclosing box, not a modeled cable surface or a verified bend radius.
- Still open: the **45° creased fold** from the cassette's −Y window (X 26–31, Y −27.5..−21.5, Z 119.8–133, cables on edge) down to the horizontal mouths, following the drum-core method in D-052. The window and ZIF centre spans are about **9 mm apart in Y and 12 mm apart in Z**. A full-width twist needs too much free length here. First make an 11.5 mm-wide paper or scrap-FFC mock-up and verify that the two folded cables keep their stacked order: the upper cable must land on the inner ZIF. Then model the proven fold and replace `HARNESS_YAW_FFC_TO_PCB08` (currently Y −27.5..−24); its present reserve misses the ZIF span Y −40..−27.

**Yaw connector naming.** Feetech calls the servo cable `5264-3P`; Molex's 5264 is the *cable receptacle* series, while its mating 3-circuit, 2.50 mm vertical PCB header is 5267 / 22035035. Treat the CAD `5264-3P header` as an envelope label, not a footprint selection. Check the received cable's key, pitch and cavity numbering against a sample before selecting the header and accepting the J8-8 fit. [Feetech servo specification](https://www.feetechrc.com/Data/feetechrc/upload/file/20240507/6385067068652648096680943.pdf); [Molex 5264](https://www.molex.com/en-us/products/series-chart/5264); [Molex 5267](https://www.molex.com/en-us/products/series-chart/5267).

**Next design gate.** Mock up the cassette-window fold and update `HARNESS_YAW_FFC_TO_PCB08`; verify the open-actuator and straight-exit assumptions with a sample. The `J8-7` ground is set (`GND_SIG`, above), and the schematic can start before the fold mock-up; only the J8-6/J8-7 contact order may change after it. Then build the KiCad schematic, ERC/netlist audit, footprint placement, routed board and parity DRC. The received FFC (four-wire resistance) and N2(b) confirm the 6.0 V / 7/7 decision. This board is not ready for fab output or order.


## Schematic

The project is [design/pcb-08-yaw-junction.kicad_pro](design/pcb-08-yaw-junction.kicad_pro), with its [schematic](design/pcb-08-yaw-junction.kicad_sch) and [PDF](design/pcb-08-yaw-junction-schematic.pdf), in **KiCad Nightly 10.99**. [build_schematic.py](design/build_schematic.py) writes it from stock symbols (same method as PCB-09); `fp-lib-table` points at the shared [`../../lib/fh34.pretty`](../lib/README.md). The board is passive: nine parts plus eight power flags.

| Ref | Interface | Footprint | Nets |
|---|---|---|---|
| J1 | `J8-1` head power in (W13 + W14) | Molex Micro-Fit 3.0 43045-0621, 2×3 right-angle THT with retention pegs | 1 `+6V0_HEAD_PR`, 2 `+5V_C2`, 3 `+5V_DISPLAY`, 4 `GND_HEAD`, 5 `GND_C2`, 6 `GND_DISPLAY` |
| J2 | `J8-4` head link (W24, D-092 order) | JST GH BM06B-GHS-TBT, top entry | 1 `LINK_GND`, 2 `C0TX_P`, 3 `C0TX_N`, 4 `C2TX_N`, 5 `C2TX_P`, 6 NC |
| R1 | `LINK_GND` → `GND_SIG` | 0805, fitted **0 Ω**; a BLM21-class ferrite or low resistor is the fallback (D-100) | |
| J3 | `J8-6` W42 power FFC | shared FH34SRJ-22S | 1–7 head positive, 8–14 `GND_HEAD`, 15–16 `+5V_C2`, 17–18 `GND_C2`, 19–20 `+5V_DISPLAY`, 21–22 `GND_DISPLAY` |
| J4 | `J8-7` W43 signal FFC | shared FH34SRJ-22S | 1/4/7/9 `GND_SIG`, 2 `C0TX_P`, 3 `C0TX_N`, 5 `C2TX_N`, 6 `C2TX_P`, 8 `SERVO_DATA`, 10–22 NC |
| J5 | `J8-8` yaw servo (W15) | Molex SPOX 5267-03A, 2.5 mm vertical | 1 `GND_SIG`, 2 `+11V1_YAW`, 3 `SERVO_DATA` |
| J6 | W17 yaw rail landing | AWG20 (0.5 mm²) solder-wire pads, 4.6 mm pitch, not in BOM | 1 `+11V1_YAW`, 2 `GND_SIG` |
| TP1, TP2 | Bench: `SERVO_DATA` edges and `GND_SIG` | 1.0 mm pads, not in BOM | |

**Choices made here.**
- **Net rename:** `+5V5_HEAD_PR` is now `+6V0_HEAD_PR` (D-100); the harness `J8-1` pinout follows.
- **J1 is the THT 43045-0621**, not the SMT 43045-0610: the head trunk is a cable connector, and its pins plus the two pegs take the plug forces in the board, as PCB-10's THT Micro-Fit does.
- **W17 pads have no strain-relief holes**: the stock relief variant adds holes 12.6 mm behind the pads, which the 21 mm board cannot spare. Strain relief is a tie or adhesive point to be set at placement.
- **J5's cavity order** follows the harness (1 GND, 2 V+, 3 data) and is checked against a received ST3215-HS lead before the footprint is frozen.
- **The FH34SRJ solder tabs are unnamed pads** (no net), as the shared footprint defines them.

**Checks.** Nightly `kicad-cli sch erc --severity-all`: **0 errors, 0 warnings** ([schematic-erc.rpt](design/schematic-erc.rpt)). The exported [netlist](design/pcb-08-yaw-junction.net) passes [audit_netlist.py](design/audit_netlist.py) on 51 connected pins ([netlist-audit.json](design/netlist-audit.json)): manifest match, `J8-1` harness order, `J8-6` 7 + 7 and 2 + 2 + 2 + 2, `J8-7` carrying no power net and 10–22 isolated, the W24 order, the RS-422 pairs running only J2 ↔ J4, `LINK_GND` reaching `GND_SIG` only through R1, the `GND_SIG` members, the `J8-8` order, `+11V1_YAW` only W17 → J8-8, and the three power returns kept to J1/J3.

**Layout notes carried forward.** The yaw return (up to 2.4 A stall) flows in `GND_SIG` copper between J6.2 and J5.1: route it as a wide pour, not a signal track. The W17 pads and J5 sit on the main plate beside the existing J8-8 envelope; the inner ZIF needs X 4.2–10 × Y −40…−27 free. The head pair (J1.1/.4 → J3 1–14) carries up to 2.4 A and the C2/display pairs about 1 A each.

## Rev A layout draft

[layout_pcb08.py](design/layout_pcb08.py) builds the two-layer, 1.6 mm board from the schematic transfer. The main outline is X −22…10, Y −44…−23 mm; the stepped ZIF extension is X 10…20, Y −42…−24.5 mm. J3 is the outer power ZIF and J4 the inner signal ZIF **provisionally** until the physical fold mock-up confirms cable order. J2 was centred on its CAD mated-plug datum; J1 overhangs the −X edge enough to clear J2's courtyard. J5 is shifted 1.44 mm from its earlier CAD envelope and needs a populated plug check. The custom [pcb08 Micro-Fit footprint](../lib/pcb08.pretty/Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal.kicad_mod) moves edge-overhanging silk graphics to F.Fab; pads and courtyard match the stock footprint.

The head path uses a 1.4 mm B.Cu positive trunk, a 1.3 mm F.Cu return trunk, and direct copper groups across J3's seven contacts on each side. The yaw rail and return each have dedicated 0.8 mm routes; `GND_SIG` also has a solid B.Cu pour. Nightly parity DRC is **0/0/0** ([report](design/placement-drc.json)); ERC and the netlist audit were rerun after the J1 footprint change. The [rev A STEP](cad/pcb-08-yaw-junction-revA.step) aligns the board core with the CAD outline. The [STEP fit probe](../../final/v1/cad/check_pcb08_step_fit.py) passes 5/6: board, J2 and R1 clear external robot parts, and J2 exactly matches its mating-plug reserve. The board's nearest modeled Pi clearance is only 0.135 mm. The populated-model row fails because the environment lacks J1, J5 and J6 models and the FH34 footprint has no 3D body. Populated fit, mated plug access, and folded cable clearance therefore remain open. **No fab outputs are released.**

**Head voltage-drop screen (estimate).** The two PCB-08 trunks total roughly 90 mm of 1.3–1.4 mm copper. At 2.4 A, 35 µm copper adds about 0.08 V of round-trip drop; 27 µm copper adds about 0.10 V, before connector and via resistance. D-100's worst-case FFC calculation left only about 0.06 V at the servo terminals. The 2.4 A condition therefore cannot be accepted from the present estimate alone: measure the received FFC, include PCB and connector resistance in N2(b), and revisit the current limit or contact map before fabrication.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-06:** rescoped by [D-093](../../decisions.md#d-093): loses the `W23a`/`W23b` permit and status sideband and `ARM_REQ`; gains the yaw servo plug.
- **2026-11-07:** [D-095](../../decisions.md#d-095) CAD: the J8-3/J8-5 placeholders are removed and the yaw servo plug sits where J8-3 was, as a Feetech 5264-3P top-entry header (ID `J8-8` proposed) at X -9.5..0.4, Y -42.6..-36.85 on the board, mated plug above it to Z 126 (`PCB08_SERVO` in `final/v1/cad/makad-v1.step.py`; `check_pcb08_servo_plug.py` 5/5). Header body and plug are envelopes (E) until the footprint is chosen at design.
- **2026-11-09:** Shared PCB-08/14 FH34SRJ input study, BO-050 mini-mini cable correction and head-rail drop screen. CAD body/straight-exit probe rejects a back-to-back pair over the Pi and two same-face outward mouths; opposing top-side mouths need a cable-turn study. No connector or rail setting frozen for fabrication.
- **2026-11-09:** [D-100](../../decisions.md#d-100) (builder): M2 at 6.0 V, 7/7 head map, `J8-7` signal-only, one generic 0.3 mm cassette FFC. Pi face survey clears back to back (Pi top Z 99.85); stepped stack selected. The Hirose land pattern moved the pair 0.5 mm inward to meet D-062; `check_pcb08_zif_stepped.py` 14/14.
- **2026-11-09:** builder approved one `GND_SIG` net (J8-4.1, J8-7 refs, J8-8.1/W17 GND); power returns stay separate; ferrite/resistor footprint fallback on J8-4.1 (D-100 amendment).
- **2026-11-09:** rev A schematic: nine parts, `+6V0_HEAD_PR`, THT Micro-Fit J1, SPOX 5267 J5, W17 AWG20 pads, R1 0 Ω `LINK_GND`→`GND_SIG`, two bench pads. ERC 0/0; netlist audit PASS (51 pins).
- **2026-11-09:** rev A layout routed on two layers; Nightly parity DRC 0/0/0. J2 aligned to the CAD plug datum, J1 shifted toward its mating edge, and the head-pair copper-drop screen flagged the remaining N2 margin. STEP exported with missing connector bodies; fold mock-up and populated fit remain gates before fab output.
