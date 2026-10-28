# PCB-11 rev A: fabrication outputs

Exported 2026-10-26 from `../../design/pcb-11-status-led.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)), and every board is designed before any is ordered ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's bottom-left corner as seen from the front (board-local u, v). The Gerbers, the drill file and both placement files agree, so the fab's placement preview lines up without manual offsets. PCB-15's set uses KiCad's absolute frame instead, which is also self-consistent.

| File | Contents |
|---|---|
| `pcb-11-status-led-revA-gerbers.zip` | The Gerber and drill files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Front and back copper (Gerber X2, Protel extensions) |
| `gerbers/*.gts, *.gbs` | Front and back solder mask |
| `gerbers/*.gtp, *.gbp` | Front and back paste (stencil). The wire pads have no paste: they are hand-soldered |
| `gerbers/*.gm1` | Board outline, 5.0 × 5.0 mm |
| `gerbers/*-PTH.drl, *-NPTH.drl` | Excellon drill, mm: three 0.35 mm plated vias; the NPTH file is empty |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `pcb-11-status-led-revA-bom.csv` | Fab BOM: LED1, C1, R1, with an `LCSC Part #` column. The wire pads P1–P3 are bare copper and are left out. The passives' MPNs are chosen at stage 2 |
| `pcb-11-status-led-revA-pos.csv` | KiCad placement file, mm, both sides, board-local origin |
| `pcb-11-status-led-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns, rotations 0–360. Check every part's rotation in the fab's preview, because bottom-side conventions differ between fabs |

**No silkscreen.** The set has no silkscreen layers. Reference labels are on the fab layers, and the stock footprints' silkscreen outlines are 0.12 mm lines, below the fab-neutral 0.16 mm ([04-pcbs README](../../../README.md#fab-neutral-design-rules): "or leave silkscreen off"). Nothing on this board needs marking: it is assembled by machine and glued into the socket.

## Order parameters

| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 5.0 × 5.0 mm, single board; panelise at quote (below) |
| Thickness | 0.8 mm, ±10 %. The socket pocket is 0.9 mm deep (X −8.1…−7.2), and the board's front face rests on the shoulder ([D-065](../../../../decisions.md#d-065)) |
| Copper | 1 oz outer |
| Finish | HASL lead-free (ENIG acceptable) |
| Solder mask | **Black preferred**, any colour acceptable; vias tented both sides. A dark board reflects less of the LED's light back into the crown cavity (G03 stray-light bench) |
| Silkscreen | None |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, copper ≥ 0.3 mm from the edge |

## Parts

| Ref | Part | Source |
|---|---|---|
| LED1 | **Worldsemi WS2812B-2020-V6** only | Fab-supplied LCSC/JLCPCB **C52917434**. In India only Hubtronics lists it (SKU 07957), with 0 in stock on 2026-10-26, so send an RFQ. The pre-V6 WS2812B-2020 (C965555, and the stock at Robu, Evelta and others) is rated 3.7–5.3 V and **must not be substituted** ([D-065](../../../../decisions.md#d-065)). MSL 5a: if hand-soldered, bake per the datasheet first |
| C1 | 100 nF X7R 0402, 10 V or higher | Choose a stocked MPN at stage 2 |
| R1 | 330 Ω 0402, 1 % | Choose a stocked MPN at stage 2 |

## Open for stage 2

- **Panel.** The board is smaller than JLCPCB's 10 × 10 mm and Lion Circuits' 50 × 100 mm assembly minimums, so it needs a panel with rails. PCB-15 needs the same, so the two can share a panel.
- **Two-sided assembly.** LED1 is on the front, while C1 and R1 are on the back. Each fab's quote must say whether it assembles both sides, and at what cost. The fallback is a fab-assembled LED1, with the back 0402s fitted by hand.
- **Online DFM.** Upload the zip to each quoting fab's DFM check before ordering.
- **Wires.** 3 × AWG30 PTFE to P1–P3 (+3V3, GND, DIN), soldered before the board goes into the socket. They leave straight back from the back's right half.
