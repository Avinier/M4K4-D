# PCB-14 (×3) — Yaw rotor joiner

Straight-through 22-pin 0.5 mm FFC joiner with two FH34SRJ ZIFs ([D-101](../../decisions.md#d-101): lower contact *n* → upper contact 23 − *n*, one conductor per X), passing the cassette FFCs through the rotating yaw hub. Three boards use six ZIFs; PCB-08 uses two more of the same part.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-062 in [BOM.csv](../../BOM.csv) |
| Location | Body, inside the rotating yaw hub |
| Specification | [02-body/v1/BOM.md](../../02-body/v1/BOM.md)<br>[D-052](../../decisions.md#d-052) |
| CAD placeholder | `_yaw_joiner_parts()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB14_JOINER_BOARD_1` … `_3` and their ZIFs |
| Final CAD | `Custom PCBs › PCB-14 yaw rotor joiners x3` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Rev A draft complete** ([D-101](../../decisions.md#d-101)): straight-through map, 4.5 mm pitch; [fab/revA](fab/revA/README.md) written (**do not order**) | [design/](design/): Nightly ERC 0/0, netlist audit 6/6 on 44 pins, parity DRC 0 violations / 0 unconnected / 0 parity; [STEP](cad/pcb-14-yaw-rotor-joiner-revA.step); [fit](../../final/v1/cad/check_pcb14_fit.py) 22/22 | 2026-11-10 |
| 2. Procure | Waits for PCB-12 (D-064) and the gates in [fab/revA](fab/revA/README.md#before-ordering) | Do not order fab/revA yet | — |
| 3. Integrate | Rev A STEP installed in final CAD (`pcb_integration.py`, integration PASS) | Physical acceptance open | 2026-11-10 |

## Inputs

The D-052 envelope is **height out from the 0.8 mm board ≤ 2.0 mm; insertion depth along the board ≤ 5.2 mm**. FH12-22S-0.5SH(55) is 6.4 mm deep and fails. FH34SRJ-22S-0.5SH(99) is the active shared PCB-08/14 candidate: 13 mm long, 3.8 mm deep, 1.0 mm high, 0.3 ± 0.03 mm FFC/FPC and 0.5 A/contact. [Hirose part and specification](https://www.hirose.com/en/product/p/CL0580-1254-3-99); [Mouser India listing](https://www.mouser.in/en/ProductDetail/Hirose-Connector/FH34SRJ-22S-0.5SH99). Its body is smaller in all three dimensions than the existing 16 × 5.2 × 2.0 mm CAD reserve at the same centre; that passes only a bounding-box screen. Its actual pad/courtyard footprint, actuator-open access and both head/cassette cable exits must fit all three rotor positions. Keep the 1:1 pin numbering, verify the top/bottom contact-side and the physical mirroring of every cable, especially CSI.

The BO-050 CSI cable is described as a Pi 5 camera cable, but the usual official camera lead is 15-to-22 standard-mini. This joiner requires **22-to-22 mini-mini** on the cassette section. Raspberry Pi documents a mini-mini 200 mm product, but its end stiffener thickness and exact order code are not yet verified against FH34SRJ. Its published **standard-mini display** drawing gives 0.309 ± 0.05 mm at the 22-way end, a wider tolerance than FH34SRJ's 0.30 ± 0.03 mm acceptance; that drawing cannot qualify the different mini-mini cable. [Raspberry Pi mini-mini declaration](https://pip-assets.raspberrypi.com/categories/907-approvals/documents/RP-005161-CF/Mini_-_Mini_EU_DoC_Cam_Display); [standard-mini drawing](https://pip-assets.raspberrypi.com/categories/903-flexible-printed-circuit-fpc-cable-for-display-and-camera/documents/RP-008145-DS-1-mini-display-cable-200mm-reference-drawing.pdf); [official camera installation guidance](https://www.raspberrypi.com/documentation/accessories/camera-software.html).

**[D-100](../../decisions.md#d-100) (2026-11-09).** The three **cassette** runs (power, sideband, CSI) are now one generic 22-way, 0.5 mm-pitch, 0.3 mm-thick FFC with a stated contact side, cut to length, so the down-facing ZIFs no longer depend on a branded mini-mini cable. The shared [FH34SRJ footprint](../lib/README.md) follows Hirose's 22-way copper and 0.1 mm-stencil signal-aperture patterns; assembler approval and PCB-14 populated placement still need review. The CSI cassette run ends in the Pi 5 camera socket, which takes the same 0.3 mm FPC. **Still open here:** the up-facing CSI ZIF takes the head-side run to the Camera Module 3 (15-way 1 mm), which stays a Pi standard-mini cable; its 22-way end (0.309 ± 0.05 mm) against FH34SRJ's 0.30 ± 0.03 mm needs a sample check, and CSI-2 stream errors through the generic FFC and both ZIFs need the BO-050 bench test.


**From the PCB-08 fold prediction (2026-11-09, [`check_pcb08_ffc_fold.py`](../../final/v1/cad/check_pcb08_ffc_fold.py)).** The cassette convention is **conductor 1 on the top edge** of every cassette FFC. That makes PCB-08's map straight. Through the D-052 drum-core fold (slit at 0°, one 45° fold up), conductor 1 then arrives at the **−X end of the lower ZIF** at yaw 0. Put lower-ZIF contact 1 there for a 1:1 path. The CSI run must keep the same convention, since the three boards are identical; check its Pi-end fold against the Pi 5 camera socket when its path is drawn.
## Design (rev A, 2026-11-10)

**Envelope, measured in the final CAD.** The yaw moving half (hub, rotor) and the head disc from `03-head/v1/cad/yaw-yoke.step` bound the boards. Measured disc bore **R10.45**, pilot ring R10.5–13 down to **Z 144.4**. Hub shoulder bore R13.15 at Z 144–145.8; rotor ring R11–27 to Z 137.0; drum R11–13.5. D-052 kept the board rectangle, Z 133.9–150.7, and the tabs (|x| 13.6, Z 137.4–143.0).

**Two changes from D-052 ([D-101](../../decisions.md#d-101), builder):**
- **Straight-through map.** The upper ZIF is the lower turned 180°, so its contact 1 is at +X. J1 contact *n* is joined to the J2 contact straight above it, 23 − *n*. Each conductor keeps its X, and the board behaves as one continuous cable. A literal *n* → *n* map would swap all 22 lanes end for end (≥ 42 vias).
- **4.5 mm pitch.** FH34SRJ's back-flip actuator opens to 90°: about 3.4 mm high (`E`), against the 2.5 mm gap of the 3.3 mm pitch. Back faces are now at Y −5.725/−1.225/3.275 and the FFC planes at −4.5/0/+4.5. The board body narrows to |x| ≤ 7.25. The rotor posts are rebuilt in `makad-v1.step.py` (`PCB14_*`).

**Orientation.**

| | Lower ZIF J1 (cassette) | Upper ZIF J2 (head) |
|---|---|---|
| Mouth | Down, entry face Z 134.40 | Up, entry face Z 150.20 |
| Footprint rotation | 0° | 180° |
| Contact 1 | −X (world X 10.75 at yaw 0) | +X (X 21.25) |
| Conductor 1 | Contact 1 | **Contact 22** (−X) |

**Inputs for other boards.**
- **PCB-12:** the head FFC carries conductor 1 (= cassette conductor 1 = PCB-08 `J8-6`/`J8-7` contact 1) on its **−X edge**. Travelling +Y in the disc channel at yaw 0, conductor 1 is on the −X side. The riser up the +Y leg is still unrouted; follow conductor 1 through it to PCB-12's ZIF.
- **CSI:** PCB-14 keeps conductor order. The path is 1:1 to the camera if (a) cassette conductor 1 lands on Pi 5 camera pin 1 at the Pi end, checked when the drop from the cassette window is drawn, and (b) the head standard-mini cable's 22-way end goes in with its pin-1 conductor at −X (contact 22, marked "22"). FH34SRJ's dual contacts accept either face, so (b) is an installation rule. A mirrored CSI cable would put 3.3 V on a ground conductor; meter it before power. The 0.309 ± 0.05 mm standard-mini end still needs a sample in FH34SRJ (0.30 ± 0.03 mm).

## Schematic

[design/pcb-14-yaw-rotor-joiner.kicad_sch](design/pcb-14-yaw-rotor-joiner.kicad_sch) ([PDF](design/pcb-14-yaw-rotor-joiner-schematic.pdf)), written by [build_schematic.py](design/build_schematic.py) from stock Nightly symbols (PCB-08's method). Two `Conn_01x22` symbols on the shared [FH34SRJ footprint](../lib/README.md). Nets are named by cassette conductor, `FFC01`…`FFC22`: J1 pin *n* = `FFCnn`, J2 pin *m* = `FFC(23−m)`. The board is passive, so there are no power flags, and the solder tabs are unnamed pads.

**Checks.** `kicad-cli sch erc --severity-all`: **0 errors, 0 warnings** ([report](design/schematic-erc.rpt)). [audit_netlist.py](design/audit_netlist.py) on the exported [netlist](design/pcb-14-yaw-rotor-joiner.net): manifest match, two connectors only, J1 *n* = conductor *n*, every net exactly J1 *n* + J2 23 − *n*, 22 two-pin nets, no contact isolated: **PASS** ([netlist-audit.json](design/netlist-audit.json)).

## Layout

[layout_pcb14.py](design/layout_pcb14.py) writes the board **headless** (no F8; two footprints). It builds the `.kicad_pcb` from PCB-08's header and placed FH34SRJ block, with this schematic's symbol paths and pad nets, then places, routes and runs DRC. Mapping: KiCad x = 116 − world X, y = 242.3 − world Z, component face +Y.
- **Board:** 2 layers, **0.8 mm**, 1 oz. Body 14.5 × 16.8 mm, tabs to 27.2 mm across at Z 137.4–143.0; no holes.
- **ZIFs:** solder-tab copper 0.35 mm from the edges (D-062 ≥ 0.3).
- **Lanes:** 22 straight F.Cu lanes, 0.3 mm wide (the pad width, 0.2 mm gap), 8.7 mm long: about 13 mΩ each at 35 µm, so 0.5 A on any contact rises a few kelvin. One design serves W42 power (7 + 7 head at 6.3 V ≤ 2.4 A, 2 + 2 C2, 2 + 2 display), W43 signal and CSI. B.Cu is bare: a plane would tie the board to one function, and the FFCs on either side have no reference plane either.
- **Silkscreen:** "1" by J1 contact 1 and "22" by J2 contact 22, both at −X, marking conductor 1. "PCB-14 A" on B.Silkscreen.
- **DRC:** Nightly `--schematic-parity` with [the fab-neutral rules](design/pcb-14-yaw-rotor-joiner.kicad_dru): **0 / 0 / 0** ([report](design/placement-drc.json)). A scratch copy with the edge rule at 0.5 mm flagged all four tabs, which proves the rules file is enforced.
- **STEP:** [cad/pcb-14-yaw-rotor-joiner-revA.step](cad/pcb-14-yaw-rotor-joiner-revA.step), with the detailed FH34SRJ model ([generate_connector_models.py](../lib/generate_connector_models.py)) on both ZIFs.

**Fit in the robot ([`check_pcb14_fit.py`](../../final/v1/cad/check_pcb14_fit.py), 22/22, [report](../../final/v1/cad/check_pcb14_fit-report.json)).** The STEP is placed three times. The check covers:
- all three boards clear of the robot, the rebuilt rotor posts, the hub, the disc and each other;
- tabs on the slot floors and captured (0.457 mm overhang, 1.0 mm lift gap);
- the rotor with the boards rising 15 mm into the bench cartridge;
- board corners at R9.24 and upper ZIFs at R8.24, inside the R10.45 bore;
- opened actuators (`E` 3.4 mm high, 1.8 mm behind the body) 0.3 mm from the next board, with a 3 mm tool column to each upper actuator;
- head FFCs up the bore and flat in the channel (board 3 lowest, top 0.35 mm under the disc top), and 1.55 mm cassette tails;
- the drum-core fold at the new planes (square R7.61; S-bend R2.57, `E`);
- the conductor-1 frame.

**Service order (head off).** Board 1's head FFC lies on top of the channel stack: lift it first, then board 2's, then board 3's.

**Not done here.** The real boards do not yet replace the placeholders in `pcb_integration.py` (stage 3), and the whole-robot STEPs are not rebuilt. The hand-kept body mass register still carries D-052's estimates: three boards at 0.51 g, six ZIFs at 0.4 g; rev A is about 0.47 g per board and 0.1 g per ZIF.

**Stage 3 and cassette assignment (2026-11-10).** The rev A STEP is installed three times in the final CAD (`pcb_integration.py`; integration PASS, 10 boards). PCB-16 ([D-103](../../decisions.md#d-103)) needs **W43 on board 3, W42 on board 2 and the CSI on board 1**, so that the lowest head FFC in the channel is W43. Mass: −2.09 g against D-052's estimate (`check_batch_mass.py`).

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-11-09:** FH12 depth exceeds D-052's reserve. FH34SRJ is the shared eight-connector candidate; India listing found. Exact CSI mini-mini cable and real three-board actuator/cable fit remain open.
- **2026-11-09:** [D-100](../../decisions.md#d-100): generic 0.3 mm cassette FFC for all three runs; the head-side CSI standard-mini end thickness stays open.
- **2026-11-09:** PCB-08 fold prediction: conductor 1 on the cassette top edge; lower-ZIF contact 1 at −X (yaw 0).
- **2026-11-10:** rev A draft ([D-101](../../decisions.md#d-101)): straight-through map (J1 *n* → J2 23 − *n*) and a 4.5 mm pitch so the FH34SRJ actuators open in place; rotor posts rebuilt in final CAD. ERC 0/0, netlist audit PASS, parity DRC 0/0/0, STEP, fit 22/22; fab/revA written, do not order. PCB-12 input: head FFC conductor 1 on the −X edge.
- **2026-11-10:** stage 3: rev A STEP ×3 installed in the final CAD; cassette assignment from D-103 (board 1 CSI, 2 W42, 3 W43).
