# PCB-06 rev A: fabrication outputs

Exported 2026-10-27 from `../../design/pcb-06-pdm-mic.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)), and every board is designed before any is ordered ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's bottom-left corner as seen from the component (inner) face. The Gerbers, the drill file and the placement files agree, so the fab's placement preview lines up without manual offsets.

**Two assembly variants, one Gerber set** ([D-066](../../../../decisions.md#d-066)). The variants differ only in which strap resistor is fitted:

| Variant | Fitted | Left off | Positions | Mic drives DATA |
|---|---|---|---|---|
| **L** | R2, 1 kΩ from LR to GND | R3 | FRONT_L, REAR_L | After the falling clock edge |
| **R** | R3, 1 kΩ from LR to +3V3 | R2 | FRONT_R, REAR_R | After the rising clock edge |

Never fit both. The fitted resistor shows which board is which; there is no silkscreen. If a fab can't take two placement files on one order, build one panel holding both variants (decide at quote).

| File | Contents |
|---|---|
| `pcb-06-pdm-mic-revA-gerbers.zip` | The Gerber and drill files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Front (inner face, all parts) and back (outer face: GND pour, the CLK and +3V3 tracks) copper, Gerber X2, Protel extensions |
| `gerbers/*.gts, *.gbs` | Front and back solder mask. Vias are tented both sides |
| `gerbers/*.gtp` | Front paste (stencil): Infineon's six ring segments and four pad apertures for MK1, and the 0402s. There is no back paste, and no paste on the wire pads, which are hand-soldered |
| `gerbers/*.gm1` | Board outline, 12.0 × 14.0 mm |
| `gerbers/*-PTH.drl` | Excellon drill, mm: five 0.35 mm plated vias |
| `gerbers/*-NPTH.drl` | Non-plated: the **Ø0.80 sound hole** at local (6, 7) and two **Ø2.20 screw holes** at (6, 2) and (6, 12) |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `pcb-06-pdm-mic-revA-L-bom.csv`, `-R-bom.csv` | Fab BOM for each variant: MK1, C1, C2, R1, and R2 (L) or R3 (R). Wire pads P1–P4 and holes H1/H2 are left out |
| `pcb-06-pdm-mic-revA-L-pos.csv`, `-R-pos.csv` | KiCad placement file, mm, front only, board-local origin |
| `pcb-06-pdm-mic-revA-L-cpl-jlcpcb.csv`, `-R-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. Check MK1's rotation in the fab's preview: its sound hole must sit over the Ø0.8 NPTH |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 12.0 × 14.0 mm, single board; panelise at quote (below) |
| Thickness | **1.0 mm**, ±10 %. The board's outer face seats on the shell boss, and the M2 × 4 screws keep at least 2.9 mm of thread at 1.1 mm |
| Copper | 1 oz outer |
| Finish | HASL lead-free (ENIG acceptable; it is flatter for the LGA) |
| Solder mask | Any colour, both sides; **vias tented both sides**. The outer face is the gasket and seat face: no via may be open there |
| Silkscreen | None |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, copper ≥ 0.3 mm from the edge. **MK1's GND seal ring is 0.23 mm from the Ø0.8 NPTH** (decision C2, D-066 amended): within JLCPCB's published 0.2 mm; PCBWay and Lion publish no limit, so check it in their DFM |
| Assembly | One side (front). Reflow only for MK1, **no-clean paste, no washing, no ultrasonic or air-blow cleaning**, port not exposed to vacuum (IM73D122 datasheet §7) |

## Parts

| Ref | Part | Source |
|---|---|---|
| MK1 | **Infineon IM73D122V01XTMA1**, PG-LLGA-5-3 | **Builder-supplied** from element14 India 4125831, consigned to the assembling fab ([D-066](../../../../decisions.md#d-066)); LCSC/JLCPCB C5563886 is the same part but is not used. MSL 1 |
| C1 | 1 µF X5R 0402, 10 V or higher | Choose a stocked MPN at stage 2 |
| C2 | 100 nF X7R 0402, 10 V or higher | Choose a stocked MPN at stage 2 |
| R1 | 100 Ω 0402, 1 % | Choose a stocked MPN at stage 2 |
| R2 (L) / R3 (R) | 1 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |

## Open for stage 2

- **Variants and quantity.** Four boards are installed, two of each variant. Order spares of both: at least 3 L and 3 R ([audiosystem.md §5.1](../../../../02-body/v1/research/audiosystem.md#51-fabrication-route) asked for 6 boards in all). BO-012's mic order must cover every board the fab assembles, plus reflow spares.
- **Panel.** The board is above JLCPCB's 10 × 10 mm assembly minimum but below Lion Circuits' 50 × 100 mm, so Lion needs a panel. A panel holding both variants also solves the two-placement-file question.
- **Consigned mic.** Confirm each fab's terms for customer-supplied parts on cut tape, and its handling of a bottom-port MEMS part.
- **Online DFM.** Upload the zip to each quoting fab's DFM check, with the seal-ring clearance as the item to watch.
- **Wires.** Four AWG28 conductors of the W27 pre-crimped GH 4-way lead, soldered to P1–P4 in GH pin order (1 +3V3, 2 CLK, 3 GND, 4 DATA), lying flat toward the board edge. Keep the iron on the pads only; the pads are 2.2 mm from MK1.
