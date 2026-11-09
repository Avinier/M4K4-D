# PCB-08 rev A: draft fabrication outputs

**Do not order yet.** These are design outputs. The fab is chosen by quote at stage 2 ([D-062](../../../../decisions.md#d-062)), and no board is ordered until every board in the batch is designed ([D-064](../../../../decisions.md#d-064)). The board-level gates are listed under [Before ordering](#before-ordering).

Exported 2026-11-09 from `../../design/pcb-08-yaw-junction.kicad_pcb` by `python3 layout_pcb08.py --export`, with the KiCad 10.99 Nightly `kicad-cli`. Every file was written after parity DRC passed: 0 violations, 0 unconnected, 0 parity issues. The board STEP (`../../cad/pcb-08-yaw-junction-revA.step`) passes `check_pcb08_step_fit.py` 18/18, and the cable path passes `check_pcb08_ffc_fold.py` 10/10.

**Every file uses one origin**: the board's bottom-left corner as seen from the top face, world (−22, −44). The Gerbers, the drill files and the placement files agree.

| File | Contents |
|---|---|
| `pcb-08-yaw-junction-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Copper, Gerber X2. **F.Cu**: all parts, the RS-422 exits from J2 and J4, `SERVO_DATA`, and the head-power field from J1 to J3 pins 1–7. **B.Cu**: the four RS-422 channels under J2, the `GND_HEAD` field to J3 pins 8–14, the C2/display pairs and the `GND_SIG` copper between J6 and J5 |
| `gerbers/*.gts, *.gbs` | Solder mask, both faces; vias tented |
| `gerbers/*.gtp` | Paste, top only. The FH34SRJ signal apertures are Hirose's 0.25 × 0.65 mm for a **0.1 mm stencil** |
| `gerbers/*.gto, *.gbo` | Silkscreen: footprint outlines only; references are on the fab layers |
| `gerbers/*.gm1` | Outline: 42 × 21 mm overall. A 32 × 21 mm main plate with a 10 × 17.5 mm +X extension for the two ZIFs |
| `gerbers/*-PTH.drl` | Excellon, mm, plated: 19 vias of 0.35 mm; J1's six 1.02 mm pins and two 2.41 mm retention-clip holes; J5's three 0.85 mm pins; J6's two 1.15 mm wire pads |
| `gerbers/*-NPTH.drl` | Non-plated: none (the file is empty) |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `gerbers/*-job.gbrjob` | Gerber job file: 2 layers, 1.6 mm |
| `pcb-08-yaw-junction-revA-bom.csv` | Fab BOM: 6 lines, 6 parts. The W17 wire pads (J6) and the two bench pads (TP1, TP2) are bare copper and left out |
| `pcb-08-yaw-junction-revA-pos.csv` | KiCad placement file, mm, board-local origin. J6, TP1 and TP2 are left out |
| `pcb-08-yaw-junction-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. In the fab preview, check that both ZIF mouths face +X (the board's narrow extension end), with contact 1 toward the +Y edge, and J1's mating face over the −X edge |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | **2** |
| Size | 42 × 21 mm stepped outline; single board |
| Thickness | **1.6 mm**: Micro-Fit 43045's drawing recommends 1.57 mm |
| Copper | 1 oz both sides |
| Finish | **ENIG** preferred: the FH34SRJ's 0.5 mm-pitch pads want a flat finish. HASL lead-free is acceptable only if the assembler accepts it for 0.5 mm pitch |
| Solder mask | Any colour; vias tented |
| Smallest features | Track 0.16 mm, gap 0.16 mm, via 0.35 / 0.67 mm, copper ≥ 0.3 mm from the edge (fab-neutral, D-062). Finest pitch: FH34SRJ 0.5 mm |
| Assembly | **Top side SMD**: J2, J3, J4, R1. **THT**: J1 (Micro-Fit) and J5 (SPOX), hand-soldered by the builder or fab THT. J6 takes the W17 AWG20 wires by hand |

## Parts

| Ref | Part | Source |
|---|---|---|
| J1 | **Molex 43045-0621**, Micro-Fit 3.0, 2 × 3 right angle, THT with press-fit clips | element14 India / Mouser India |
| J2 | JST BM06B-GHS-TBT, GH 6-way top entry | Fab stock |
| J3, J4 | **Hirose FH34SRJ-22S-0.5SH(99)**, 22-way 0.5 mm back-flip ZIF | Mouser India; consign. The same part is used ×6 on PCB-14 |
| J5 | **Molex 22-03-5035** (5267-03A), Mini-SPOX 3-way vertical | element14 India / Mouser India. Check against a received ST3215-HS lead first |
| R1 | 0 Ω 0805 (Yageo RC0805JR-070RL) | Fab basic part. Its pads take a BLM21-class ferrite if the bench needs one (D-100) |

## Assembly notes

- **Trim** the J1, J5 and J6 tails to **≤ 1.5 mm** below the board after soldering. Keep J1's two press-fit retention clips; solder them, as the Molex drawing advises.
- **Strain-relieve W17** with a tie or adhesive point beside J6; the pads have no relief holes.
- **FFC orientation:** both cassette FFCs carry **conductor 1 on the top edge** inside the cassette (D-100 amendment). W42 power goes in **J3** (outer), W43 signal in **J4** (inner).
- **Plug order:** latch J3's cable first; J4's cable then runs over J3.

## Before ordering

- A strip of the received FFC confirms the predicted fold (`check_pcb08_ffc_fold.py`).
- An FH34SRJ sample confirms the stiffener overhang, S-bend radius and opened-actuator envelope used in the CAD.
- J5's cavity order is checked against a received ST3215-HS lead.
- **Bench, with the received parts:** four-wire FFC resistance and N2(b) at 6.3 V confirm D-100's head rail.
- The PCB-12 and PCB-14 designs are complete, for the single D-064 order.

## 3D model

The board STEP uses detailed drawing-based models for J1, J3, J4 and J5, from `../../../lib/generate_connector_models.py`; KiCad's library has none for these parts. J2 and R1 use KiCad's own models. Renders: `../../cad/pcb-08-yaw-junction-revA-iso-*.png`.
