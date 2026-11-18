# PCB-17 rev A: fabrication outputs

**Do not order on its own.** These boards go in the D-064 batch, panelised with PCB-11 and PCB-15 ([D-117](../../../../decisions.md#d-117)). Gates are under [Before ordering](#before-ordering).

Exported 2026-11-18 by `python3 layout_pcb17.py --export` (KiCad 10.99 Nightly) after parity DRC 0/0/0. One origin for every file: (100, 110), the bottom-left corner of the two-card group seen from the top.

| File | Contents |
|---|---|
| `pcb-17-balance-fuse-cards-revA-gerbers.zip` | Gerber, drill and job files for both cards (two separate outlines, 4 mm apart) |
| `gerbers/*.gtl, *.gbl` | **F.Cu**: three 1206 fuse lands, six wire pads, 0.8 mm tracks. **B.Cu**: empty |
| `gerbers/*.gm1` | Card A 6 × 9 mm, card B 9.5 × 10 mm |
| `pcb-17-balance-fuse-cards-revA-bom.csv` | 3 × Littelfuse 0466001.NRHF (F1–F3). The wire pads are bare copper |
| `pcb-17-balance-fuse-cards-revA-pos.csv`, `-cpl-jlcpcb.csv` | Placement of F1–F3 |

## Order parameters

| Parameter | Value |
|---|---|
| Layers / thickness | 2 / **0.8 mm** (matches PCB-11 and PCB-15) |
| Copper / finish | 1 oz; HASL lead-free |
| Smallest features | Track 0.8 mm, copper gap ≥ 0.16 mm, copper ≥ 0.3 mm from the edge (fab-neutral, D-062) |
| Assembly | Optional. 0466001.NRHF may not be a fab stock part: if not, order bare boards and hand-solder the three 1206 fuses |

## Before ordering

1. Received TIFPS0629 pad corners and height checked, and the CAD updated if they differ ([board README](../../README.md#open)).
2. Panel with PCB-11 and PCB-15 laid out at DFM, with board size, panel rails and V-score or mouse-bites chosen by the fab quote.
3. Order 2 spare panels' worth of fuses (5 total) for N5 fault tests.
