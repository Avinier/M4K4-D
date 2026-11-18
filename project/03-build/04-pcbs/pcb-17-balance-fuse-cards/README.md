# PCB-17 — Balance-tap fuse cards

Two small passive cards that put a 1 A very-fast fuse in each of the pack's three balance taps (B−, BM, B+) right at the PCB-01 BMS pads. These taps feed the rear balance port ahead of PCB-01 and the 15 A main fuse, so the cards are their only short-circuit protection ([D-111](../../decisions.md#d-111), [D-115](../../decisions.md#d-115), [D-116](../../decisions.md#d-116), [D-117](../../decisions.md#d-117)).

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-103 in [BOM.csv](../../BOM.csv) |
| Location | Chassis tub, lying component side up on the PCB-01 (HW-391) BMS: card A at its +Y (BM/P) end, card B at its −Y (0V/8.4V) end, each under a 0.8 mm relief in the CH-106 plate |
| Final CAD | `BALANCE_FUSE` and `BMS_PADS` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py); check `check_ch103_protection.py` |

## Stages

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Rev A complete**; [fab/revA](fab/revA/README.md) written (do not order before the gates) | [design/](design/): Nightly ERC 0/0, netlist audit 13/13, parity DRC 0/0/0; [STEP](cad/pcb-17-balance-fuse-cards-revA.step) | 2026-11-18 |
| 2. Procure | Panelise with PCB-11 and PCB-15 (same 0.8 mm stackup) in the D-064 batch | — | — |
| 3. Integrate | Droid CAD envelopes match the KiCad outlines (card A 6 × 9, card B 9.5 × 10, 2.0 mm with fuse and potting); `check_ch103_protection` 12/12. Board STEP not yet swapped in by `pcb_integration.py` | Physical acceptance open | 2026-11-18 |

## Circuit

| Card | Fuse | Cell-side pad | Protected pad | Silk |
|---|---|---|---|---|
| A (6 × 9 mm) | F1, BM | J1 `BM_CELL` (from the HW-391 4.2V pad) | J2 `BM_FUSED` | `BM`; back `17A` |
| B (9.5 × 10 mm) | F2, B− | J3 `BMINUS_CELL` (0V pad) | J4 `BMINUS_FUSED` | `B-`; back `17B` |
| B | F3, B+ | J5 `BPLUS_CELL` (8.4V pad) | J6 `BPLUS_FUSED` | `B+` |

Fuses: Littelfuse 0466001.NRHF, 1206, 1 A, 63 VDC, 50 A interrupt, ~0.075 Ω cold. Each fuse's pin 1 faces its card's BMS pad end. Wire pads are 2.5 × 1.5 mm bare copper for AWG24 laid flat along X. Tracks are 0.8 mm, one straight column per tap. B− and B+ copper is 1.5 mm apart.

## Coordinates

KiCad (x, y down) to droid CAD: card A X = x − 59.0, Y = 124.0 − y; card B X = x − 70.7, Y = 86.0 − y. Board Z 0 is the card's underside on the BMS (droid Z 54.2). Fab origin (100, 110), the bottom-left of the two-card group.

## Open

- **Received HW-391:** confirm the pad corners (the `BMS_PADS` values are estimates from the listing photos) and the full board height. If board + card exceeds the pack-to-plate gap at either end, deepen that CH-106 relief, keeping at least a 1.5 mm roof, and re-run `check_ch103_protection.py`.
- **Potting:** thin silicone or epoxy, ≤ 0.6 mm over the fuse. The fuse ratings assume an uncoated part, so N5 is run with the cards potted ([D-116](../../decisions.md#d-116)).
- **N5:** the PD60 open-tap, adjacent-short and main-lead-off cases, plus 0.5 A fuse heating, per D-116. W02P stays unbuilt until N5 passes.
