# PCB-16 — Head junction

Passive FFC-to-wire break for the two head FFCs (W42 power, W43 signal). It lies flat on the yaw disc beside the +Y yoke leg's foot, so the tilting head needs only wires across its pitch and roll joints ([D-103](../../decisions.md#d-103)).

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-111 in [BOM.csv](../../BOM.csv) |
| Location | Head, yaw frame: flat on the yaw disc (M012) top, over the channel's outer end |
| Specification | [D-103](../../decisions.md#d-103), [D-100](../../decisions.md#d-100), [D-101](../../decisions.md#d-101), [D-102](../../decisions.md#d-102) |
| Final CAD | `Custom PCBs › PCB-16 head junction` (installed by `pcb_integration.py`); fixings and reserves `PCB16`, `PCB16_RESERVES` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Rev A draft complete**; [fab/revA](fab/revA/README.md) written (**do not order**) | [design/](design/): Nightly ERC 0/0, netlist audit 10/10 on 44 pins, parity DRC 0/0/0; [STEP](cad/pcb-16-head-junction-revA.step); [fit](../../final/v1/cad/check_pcb16_fit.py) 7/7 | 2026-11-10 |
| 2. Procure | Waits for the gates in [fab/revA](fab/revA/README.md#before-ordering) (D-064 batch) | — | — |
| 3. Integrate | Rev A STEP installed in the final CAD with disc inserts and screws; `check_pcb_integration.py` PASS (10 boards) | Physical acceptance open | 2026-11-10 |

## Inputs

**Why a board on the disc.** D-052 meant the head FFCs to climb the +Y leg into the pitch frame. The pitch servo fills the inside of that leg from Z ≈ 15 to 65 (head-local), so that route is blocked. A roll × pitch sweep shows the band from the disc top (Z −34.5) to about Z −24 stays clear beside the leg foot. The head already reserves everything below Z −30.5 as moving-part clearance (`SWEEP_FLOOR_Z`), and PCB-16 with both FFC arrivals stays under it.

**Envelope (head-local).**
- Board: X −62.4…−26, Y 35.5…54, Z −34.5…−33.7.
- The edge steps in to X −47.6 from Y 47.7, keeping 0.3 mm from the leg foot's flare (which reaches X −47.95 from Y 48.05 at the disc).
- The −X tab (Y 35.5…41) clears the foot's M2 screw heads, which start at Y 46.97.
- Two M2 holes at (X −57.4, Y 38.2) and (X −31.9, Y 52.0) take M2 × 4 button screws into M2 inserts in the 4 mm disc plate, leaving a 0.8 mm floor.

**FFC arrival** (`HARNESS_HEAD_FFC_*` in the droid CAD, at PCB-14's D-101 planes):
- The head FFCs rise up the bore (Y ±4.65), lie flat in the disc channel, and leave it from Y 30.
- The **lower** FFC (**W43 signal**) S-bends up (about R3, `E`) and runs 1 mm straight into **J1** (mouth Y 36.0).
- The **upper** FFC (**W42 power**) rises higher, runs 0.055 mm over J1's closed body and drops into **J2** (mouth Y 43.4).
- The **CSI** is the top FFC and leaves before Y 29.8 (`HARNESS_HEAD_CSI_EXIT_UNROUTED`). Its path to the camera is open.
- Cassette input: W43 on PCB-14 board 3, W42 on board 2, CSI on board 1. Confirm with the fold mock-up.
- **Plug order:** W43 into J1 first, close J1, then W42 over it into J2.

**Conductor 1.** The head FFC carries conductor 1 on its −X edge (D-101), and each ZIF's contact 22 is at −X. So **contact *m* carries conductor 23 − *m***, and nets are named by conductor (PCB-08's `J8-6`/`J8-7` maps).

## Circuit and pads

[Schematic](design/pcb-16-head-junction.kicad_sch) ([PDF](design/pcb-16-head-junction-schematic.pdf)), written by [build_schematic.py](design/build_schematic.py). The board is passive and the four grounds stay separate; PCB-12 bonds them (D-100). Wire pads ([generate_wire_pads.py](../lib/generate_wire_pads.py)) sit where their nets are, are bare copper, and are left out of the BOM and position files.

| Ref | Part | Nets / wires |
|---|---|---|
| J1 | FH34SRJ-22S, near | W43: conductors 1/4/7/9 `GND_SIG`, 2 C0TX+, 3 C0TX−, 5 C2TX−, 6 C2TX+, 8 `SERVO_DATA`; 10–22 isolated |
| J2 | FH34SRJ-22S, far | W42: 1–7 `+6V3_HEAD_PR`, 8–14 `GND_HEAD`, 15–16 `+5V_C2`, 17–18 `GND_C2`, 19–20 `+5V_DISPLAY`, 21–22 `GND_DISPLAY` |
| J3 | 2 pads 2.2 × 3.5 mm | 1 `+6V3_HEAD_PR`, 2 `GND_HEAD`: AWG20 servo bundle to the pitch servo's 5264 (daisy chain to roll). Pad 2 also takes PCB-12's J2-lead `GND_HEAD` wire |
| J4 | 7 pads 1.0 × 2.5 mm | 1 `GND_SIG`, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+ (PCB-12 J1-lead wires 1–5); 6 `SERVO_DATA` (PCB-12 J2-lead wire 2); 7 `SERVO_DATA` (servo bundle) |
| J5 | 2 pads | 1 `+5V_C2`, 2 `GND_C2` (PCB-12 J1-lead wires 6–7) |
| J6 | 2 pads | 1 `+5V_DISPLAY`, 2 `GND_DISPLAY` (to D1) |

The PCB-12 leads are pre-crimped single-ended GH7 and GH2 leads, cut and soldered here; they plug into PCB-12 J1/J2. The head comes off by unplugging at PCB-12, the servo and D1.

**Checks.** ERC 0/0 ([report](design/schematic-erc.rpt)). [audit_netlist.py](design/audit_netlist.py) **10/10** ([netlist-audit.json](design/netlist-audit.json)): W42 and W43 conductor maps against `J8-6`/`J8-7`, no power on W43, the pad maps, the grounds kept separate, the `SERVO_DATA` hub.

## Layout

[layout_pcb16.py](design/layout_pcb16.py) writes the board headless (PCB-12's method). Mapping: KiCad x = X + 142.4, y = 150 − Y, component face +Z.
- **Board:** two layers, 0.8 mm.
- **J2 power** runs straight back into its pads: `+6V3_HEAD_PR` and `GND_HEAD` as F.Cu fields over seven contacts each (2.4 A), the C2 and display pairs as 0.3 mm tracks.
- **J1 signal:** its four `GND_SIG` contacts join under the ZIF body (Hirose allows traces there). The signal lanes leave the pad tails, cross the band between the ZIFs and land on the J4 column.
- **DRC:** Nightly parity **0/0/0** ([report](design/placement-drc.json)). A scratch copy with a 0.5 mm edge rule flags the four ZIF tabs.
- **STEP:** [cad/pcb-16-head-junction-revA.step](cad/pcb-16-head-junction-revA.step), with the detailed FH34SRJ model.

**Fit ([`check_pcb16_fit.py`](../../final/v1/cad/check_pcb16_fit.py), 7/7).**
- Placed; clear of the yaw-frame parts (leg foot 0.3 mm).
- Under the sweep floor; 10.04 mm from the moving head over 30 poses.
- FFC paths into both mouths; inserts in the plate; conductor 1 on contact 22.

**Mass:** about 1.34 g (`check_batch_mass.py`).

## Open

- ~~The wire bundle's routes across the pitch and roll joints~~: routed by [D-104](../../decisions.md#d-104) from the +X exit, along the disc to the −Y leg and through a hollow −Y trunnion (`check_d104_head_routes.py` 7/7). The +Y exit reserve stays unused.
- The CSI's path to the camera across both joints, as an FFC.
- A strip of the received FFC to confirm the S-bends.
- Pad sizes against the received wire.

## Log

- **2026-11-10:** rev A draft ([D-103](../../decisions.md#d-103)): yaw-disc FFC-to-wire break, stepped FH34SRJ pair, per-net wire pads. The board moved 5.5 mm toward −Y and stepped past the leg foot after the fit check found it on the foot; ERC 0/0, netlist audit 10/10, parity DRC 0/0/0, fit 7/7; installed in the final CAD (integration PASS, 10 boards).
