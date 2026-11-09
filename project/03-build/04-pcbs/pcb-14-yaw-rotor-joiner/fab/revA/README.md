# PCB-14 rev A: draft fabrication outputs

**Do not order yet.** These are design outputs. The fab is chosen by quote at stage 2 ([D-062](../../../../decisions.md#d-062)), and no board is ordered until every board in the batch is designed ([D-064](../../../../decisions.md#d-064)). The board-level gates are listed under [Before ordering](#before-ordering).

Exported 2026-11-10 from `../../design/pcb-14-yaw-rotor-joiner.kicad_pcb` by `python3 layout_pcb14.py --export`, with the KiCad 10.99 Nightly `kicad-cli`. Every file was written after parity DRC passed: 0 violations, 0 unconnected, 0 parity issues. The board STEP (`../../cad/pcb-14-yaw-rotor-joiner-revA.step`) passes `check_pcb14_fit.py` 22/22 ([D-101](../../../../decisions.md#d-101)).

**Every file uses one origin**: the board's bottom-left corner as seen from the component face (the −X world tab tip at yaw 0, board bottom edge). The Gerbers, the drill files and the placement files agree.

| File | Contents |
|---|---|
| `pcb-14-yaw-rotor-joiner-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Copper, Gerber X2. **F.Cu**: both ZIF land patterns and 22 straight 0.3 mm lanes. **B.Cu**: empty |
| `gerbers/*.gts, *.gbs` | Solder mask, both faces |
| `gerbers/*.gtp` | Paste, top only. FH34SRJ signal apertures are Hirose's 0.25 × 0.65 mm for a **0.1 mm stencil**; 22 signal and 2 tab apertures per ZIF |
| `gerbers/*.gto, *.gbo` | Silkscreen: ZIF outlines and the conductor-1 marks "1" (J1) and "22" (J2) on top; "PCB-14 A" on the bottom |
| `gerbers/*.gm1` | Outline: 27.2 × 16.8 mm overall: a 14.5 × 16.8 mm body with a 6.35 × 5.6 mm tab each side |
| `gerbers/*.drl` | Excellon, mm. **No holes** (both files are empty) |
| `gerbers/*-job.gbrjob` | Gerber job file: 2 layers |
| `pcb-14-yaw-rotor-joiner-revA-bom.csv` | Fab BOM: 1 line, 2 parts (J1, J2) per board |
| `pcb-14-yaw-rotor-joiner-revA-pos.csv` | KiCad placement file, mm, board-local origin |
| `pcb-14-yaw-rotor-joiner-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. In the fab preview check that J1's mouth faces the bottom edge and J2's the top edge, and that both "1"/"22" marks sit on the same side |

## Order parameters

| Parameter | Value |
|---|---|
| Quantity | **3 boards per robot** (identical), plus spares for one rework. Panelise with the other D-064 boards |
| Layers | **2** |
| Size | 27.2 × 16.8 mm, tabbed outline; tab edges are a slide fit in printed slots (0.1 mm a side), so ask for routed edges, no V-score stubs on the tabs |
| Thickness | **0.8 mm** (D-052): the posts' slots are 1.0 mm wide. Confirm the fab's thickness tolerance at quote (D-062: PCBWay states it only from 1.0 mm) |
| Copper | 1 oz both sides |
| Finish | **ENIG** preferred for the 0.5 mm-pitch FH34SRJ pads; HASL lead-free only if the assembler accepts it |
| Solder mask | Any colour |
| Smallest features | Track 0.3 mm, gap 0.2 mm (fab-neutral minimums 0.16/0.16, D-062); copper ≥ 0.35 mm from the edge. Finest pitch: FH34SRJ 0.5 mm |
| Assembly | **Top side SMD only**: J1, J2. No through-hole parts |

## Parts

| Ref | Part | Source |
|---|---|---|
| J1, J2 | **Hirose FH34SRJ-22S-0.5SH(99)**, 22-way 0.5 mm back-flip ZIF, top and bottom contact | Mouser India; consign. Six per robot here, two more on PCB-08 |

## Assembly and installation notes

- **Conductor 1 is at −X** on both ZIFs: J1 contact 1 (silk "1") and J2 contact 22 (silk "22"). The cassette FFCs carry conductor 1 on their top edge (D-100), which brings it to J1 contact 1 through the drum fold.
- **Head FFCs, CSI especially:** insert with conductor 1 at the "22" end. The dual-contact ZIF accepts either face, so a cable flipped over is mirrored. Before powering, meter the camera's 3.3 V and ground conductors through to the Pi.
- **Bench order:** with the boards in the rotor posts, plug each lower (cassette) FFC and close its actuator. The 4.5 mm pitch leaves 0.3 mm beside an opened actuator (`E`).
- **Head service:** lift board 1's head FFC first (top of the channel stack), then board 2, then board 3.

## Before ordering

- An FH34SRJ sample confirms the opened-actuator height (`E` 3.4 mm; the pitch allows about 3.6 mm) and the 1.55 mm cassette tail.
- The D-052 fold mock-up, rerun at the 4.5 mm planes (−4.5/0/+4.5 mm): fan-out S-bend, 45° fold and tail into the lower ZIFs.
- A Raspberry Pi standard-mini cable's 22-way end in an FH34SRJ (0.309 ± 0.05 mm against 0.30 ± 0.03 mm), and the BO-050 CSI stream test through both ZIF pairs.
- The CSI drop to the Pi 5 camera socket is drawn, with cassette conductor 1 on Pi pin 1.
- PCB-12 is designed, for the single D-064 order.

## 3D model

The board STEP uses the detailed drawing-based FH34SRJ model from `../../../lib/generate_connector_models.py` on both ZIFs; KiCad's library has none for this part.
