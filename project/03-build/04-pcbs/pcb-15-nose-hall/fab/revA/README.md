# PCB-15 rev A: fabrication outputs

Exported 2026-10-25 from `../../design/pcb-15-nose-hall.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)).

| File | Contents |
|---|---|
| `pcb-15-nose-hall-revA-gerbers.zip` | The files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Front and back copper (Gerber X2, Protel extensions) |
| `gerbers/*.gts, *.gbs` | Front and back solder mask |
| `gerbers/*.gtp, *.gbp` | Front and back paste (stencil) |
| `gerbers/*.gto, *.gbo` | Silkscreen: no text, only the 0402 body marks on the back |
| `gerbers/*.gm1` | Board outline, 6.0 × 4.6 mm |
| `gerbers/*-PTH.drl, *-NPTH.drl` | Excellon drill, mm: three 0.35 mm plated vias; the NPTH file is empty |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `pcb-15-nose-hall-revA-bom.csv` | Fab BOM: U1, C1, C2, R1. The wire pads P1–P3 are bare copper, so they are left out. MPNs for the passives are chosen at stage 2 |
| `pcb-15-nose-hall-revA-pos.csv` | KiCad placement file, mm, both sides |
| `pcb-15-nose-hall-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. Check every part's rotation in the fab's preview, because bottom-side rotation conventions differ between fabs |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 6.0 × 4.6 mm, single board; panelise at quote (below) |
| Thickness | 0.8 mm. **State the tolerance on the order:** ±10 % (≤ 0.88 mm) or tighter. The board sits in a 1.0 mm slot |
| Copper | 1 oz outer |
| Finish | HASL lead-free (ENIG acceptable) |
| Solder mask | Any colour; vias tented both sides |
| Silkscreen | None needed |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, copper ≥ 0.3 mm from the edge |

## Open for stage 2

- **Panel.** The board is smaller than JLCPCB's 10 × 10 mm and Lion Circuits' 50 × 100 mm assembly minimums ([04-pcbs README](../../../README.md#fab-neutral-design-rules)), so it needs a panel with rails, made by the fab or drawn by us.
- **Two-sided assembly.** U1 is on the front, while C1, C2 and R1 are on the back. Each fab's quote must say whether it assembles both sides, and at what cost. The fallback is fab-assembled U1 with the back 0402s fitted by hand.
- **Parts.** Choose stocked MPNs for the 100 nF X7R 0402 (10 V or higher) and the 1 kΩ 0402.
