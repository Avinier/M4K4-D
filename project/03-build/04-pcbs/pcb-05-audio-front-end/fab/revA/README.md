# PCB-05 rev A: fabrication outputs

Exported 2026-10-27 from `../../design/pcb-05-audio-front-end.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)), and every board is designed before any is ordered ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's corner at world (45, −19), bottom left as seen from the top (component) face. The Gerbers, the drill files and the placement files agree, so the fab's placement preview lines up without manual offsets.

| File | Contents |
|---|---|
| `pcb-05-audio-front-end-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.g1, *.g2, *.gbl` | Copper, Gerber X2, Protel extensions. **F.Cu**: all parts and most signals. **In1.Cu**: solid GND plane. **In2.Cu**: GND pour plus the slow rows, mic feeds and mic supply. **B.Cu**: the clock bus and the two mic data down-feeds, no parts |
| `gerbers/*.gts, *.gbs` | Front and back solder mask. **Vias are tented both sides.** The back opens only at J7's two pins, its peg hole and the three spacer rings. The ADAU7002s have **one mask opening over each ball array** (0.80 × 1.60 mm, no mask webs between 0.4 mm-pitch balls) |
| `gerbers/*.gtp` | Front paste (stencil). No back paste |
| `gerbers/*.gto` | Front silkscreen: footprint outlines only; reference labels are on the fab layer (the board is small) |
| `gerbers/*.gm1` | Board outline, 30.0 × 38.0 mm |
| `gerbers/*-PTH.drl` | Excellon drill, mm, plated: 59 vias of 0.35 mm, J7's two 1.02 mm pins, and **three Ø3.00 plated holes** under the spacers (decision I1) |
| `gerbers/*-NPTH.drl` | Non-plated: J7's Ø3.00 snap-in peg |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `gerbers/*-job.gbrjob` | Gerber job file: 4 layers, 1.6 mm, the stackup below, HASL lead-free |
| `pcb-05-audio-front-end-revA-bom.csv` | Fab BOM, grouped. Unfitted parts (R13–R16, C10, C11) and test pads TP1–TP12 are left out |
| `pcb-05-audio-front-end-revA-pos.csv` | KiCad placement file, mm, top only, board-local origin; 37 parts, unfitted parts left out |
| `pcb-05-audio-front-end-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. Check every rotation in the fab's preview: **U1/U2 ball A1** and **U3 pin 1** against the silkscreen, and the GH and Micro-Fit headers facing out of the board edge |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | **4** ([D-067](../../../../decisions.md#d-067), amended at routing) |
| Size | 30.0 × 38.0 mm, single board; panelise at quote (below) |
| Thickness | **1.6 mm**. The spacers stand on the top face and the Micro-Fit expects 1.57 |
| Stackup | F.Cu 35 µm, prepreg 0.2104, In1 15.2 µm, core 1.065, In2 15.2 µm, prepreg 0.2104, B.Cu 35 µm: JLCPCB's 7628 build. Any fab's standard 1.6 mm 4-layer build will do; impedance isn't controlled |
| Copper | 1 oz outer, 0.5 oz inner |
| Finish | HASL lead-free, or ENIG: it is flatter for the 0.4 mm WLCSP, so prefer it if the fab prices it close |
| Solder mask | Any colour; vias tented both sides. The back face sits 2.10 mm above the Pi's USB jacks |
| Silkscreen | Top only |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, via copper ≥ 0.31 mm to other copper, copper ≥ 0.3 mm from the edge (fab-neutral, D-062). **WLCSP pads Ø0.23 mm, 0.17 mm apart**, under one shared mask opening |
| Assembly | **One side (top).** Reflow: everything except J7. **U1/U2 are 0.4 mm-pitch WLCSP**: X-ray inspection at JLCPCB (extended part). **J7 is through hole**: THT assembly or hand-soldered, then **tails clipped to ≤ 0.5 mm below the board and the snap-in peg cut flush** (decision H1; the board sits 2.10 mm above a USB jack). **H1–H3 are 8 mm SMT spacers** on 24 mm tape with a polyimide pick-up tape: confirm the fab can place them, or hand-solder them |

## Parts

| Ref | Part | Source (lesson 1, 2026-10-27) |
|---|---|---|
| U1, U2 | **ADAU7002ACBZ-R7**, WLCSP-8 | element14 India 4028782 (UK stock), or LCSC/JLCPCB C481886 (extended part, X-ray). MSL 1 |
| U3 | **MAX98357AETE+T**, TQFN-16 3 × 3 | element14 India 2949165 (UK stock), or LCSC/JLCPCB C910544 (extended part) |
| J1 | JST SM10B-GHS-TB(LF)(SN) | No India stock: from the fab's stock (LCSC part to look up) |
| J2–J5 | JST SM04B-GHS-TB(LF)(SN) | LCSC C189895 |
| J6 | JST SM02B-GHS-TB(LF)(SN) | From the fab's stock (LCSC part to look up); element14 India has a 40-week lead |
| J7 | Molex 43650-0200 | element14 India 2324861 |
| H1–H3 | Würth 9774080243R, M2 × 8 SMT spacer | Choose the source at stage 2 |
| C1 | 10 µF X5R 0805, 10 V or higher | Choose a stocked MPN at stage 2 |
| C8 | 10 µF X5R 0805, **16 V** or higher (5 V rail) | Choose a stocked MPN at stage 2 |
| C2–C7, C9 | 100 nF X7R 0402 (C9 16 V) | Choose a stocked MPN at stage 2 |
| FB1 | 600 Ω at 100 MHz, 0603 | Choose a stocked MPN at stage 2 |
| FB2, FB3 | 0 Ω 0603 (a ferrite if EMI needs it) | Choose a stocked MPN at stage 2 |
| R1 | 2.2 Ω 0402 | Choose a stocked MPN at stage 2 |
| R2–R5, R8–R10 | 100 Ω 0402, 1 % | Choose a stocked MPN at stage 2 |
| R6, R7, R12 | 100 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| R11 | 2.2 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| Not fitted | R13, R14 (gain), R15, R16 (5 V sense), C10, C11 (speaker EMI) | Footprints only; fit on the bench if needed |

## Open for stage 2

- **Fab and WLCSP.** JLCPCB assembles the ADAU7002 with X-ray. Lion Circuits MII's WLCSP capability is unverified, and its assembly minimum is 50 × 100 mm (panel). Upload the zip to each quoting fab's DFM check; the items to watch are the WLCSP pads and their shared mask opening, and the plated Ø3 holes with their solder rings.
- **Consign or buy.** The ICs are in stock at element14 India and at LCSC. Consign them (as PCB-06 does with its mic) or let the fab buy them. The GH headers come from the fab's stock either way.
- **J7 clipping.** Put the clipping instruction on the order (the schematic's `Assembly` field). Otherwise solder J7 by hand on receipt, then measure the tails and peg against the 0.5 mm limit.
- **Quantity.** One board is installed; order at least 3 (a spare and a bench board).
