# PCB-13 rev A: fabrication outputs

Exported 2026-10-29 from `../../design/pcb-13-charge-inlet.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)), and every board is designed before any is ordered ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's bottom-left corner as seen from the top (F, parts) face, world (Y −14, Z 56.5). The Gerbers (`--use-drill-file-origin`), the drill files (`--drill-origin plot`) and the placement files agree.

| File | Contents |
|---|---|
| `pcb-13-charge-inlet-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/`, in one zip, ready to upload |
| `gerbers/*.gtl, *.gbl` | Copper, Gerber X2, Protel extensions. **F.Cu**: all parts but J1, the signals, and the `VBUS`/`VSNK`/`GND` pours. **B.Cu**: J1's six SMT pads, a solid GND plane, the `VBUS` bar under J1, and two thin tracks (`EN_SNK`, TP1 `VBUS`) right of J1 |
| `gerbers/*.gts, *.gbs` | Front and back solder mask. **Vias tented both sides.** The back opens only at J1's six pads, its four plated stake slots and the non-plated holes. **The back face sits flat on a printed pad**, so nothing else may stand proud there |
| `gerbers/*.gtp` | Front paste only. No back paste: J1 is soldered by hand |
| `gerbers/*.gto` | Front silkscreen: footprint outlines only. Reference labels are on the fab layer |
| `gerbers/*.gm1` | Board outline, 28.0 × 15.0 mm |
| `gerbers/*-PTH.drl` | Excellon, mm, plated: vias of 0.35 mm, and **J1's four stake slots** (0.60 × 1.00 at x ±4.32; 1.10 × 0.60 at x ±2.30). The slots are routed: confirm each fab's minimum plated-slot width in its DFM check |
| `gerbers/*-NPTH.drl` | Non-plated: two Ø2.2 screw holes (H1, H2), J1's Ø0.70 peg hole and 1.00 × 0.70 peg slot |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `gerbers/*-job.gbrjob` | Gerber job file: 2 layers, 1.6 mm |
| `pcb-13-charge-inlet-revA-bom.csv` | Fab BOM, grouped: 12 lines, 13 parts. Left out: **J1, the USB4140** (the builder buys and hand-solders it, D-069), J2 (bare `W16` lap pads), the test pads and the holes |
| `pcb-13-charge-inlet-revA-pos.csv` | KiCad placement file, mm, top only, board-local origin: the same 13 parts |
| `pcb-13-charge-inlet-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. In the fab's preview, check **U1 pin 1** (QFN-24, rotated 90°), **Q1** (PowerFLAT: pins 1–3 source and 4 gate on the left, the drain pad toward the right edge), **D1** (WSON-6: IN pins 4–6 toward the board centre), and **D2** (SOT-323, pin 3 GND toward the left) |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | 2 (D-069) |
| Size | 28.0 × 15.0 mm: above JLCPCB's 10 × 10 mm assembly minimum, but under Lion MII's 50 × 100 mm, which needs a **panel** (fab-neutral rules) |
| Thickness | **1.6 mm**, standard ±10 %. J1's 1.70 mm stakes and the M2 × 5 screws' 3 mm engagement both hold over 1.44–1.76 |
| Copper | **1 oz** both sides (D-069). The 3 A path is poured: narrowest 2.41 mm (`VBUS`), 1.29 mm (`VSNK` past H2's hole) |
| Finish | HASL lead-free or ENIG. ENIG gives a flatter B face on the panel seat and better 0.5 mm QFN pads |
| Solder mask | Any colour; vias tented both sides |
| Silkscreen | Top only |
| Smallest features | Track 0.16 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, via copper ≥ 0.31 mm to other copper, copper ≥ 0.3 mm from the edge (fab-neutral, D-062). Smallest pitch: U1's 0.5 mm |
| Assembly | **One side (top), reflow**: the 13 parts in the BOM. Economic/standard single-sided service. **J1 is not fab-assembled** (below) |

## Parts

| Ref | Part | Source (D-069) |
|---|---|---|
| J1 | GCT **USB4140-GF-0170-C** | element14 India 3955430. **Builder-bought, hand-soldered after assembly**; not on the fab BOM |
| U1 | ST **STUSB4500QTR** | element14 India 2980889, **consigned** |
| Q1 | ST **STL6P3LLH6** | element14 India 3132757 (multiples of 5), **consigned** |
| D2 | ST **ESDA25W** | element14 India 2341655, **consigned** |
| D1 | TI **TVS2200DRVR** | Mouser India 595-TVS2200DRVR, **consigned**. LCSC lists only clones under this name: not accepted |
| C1 | 4.7 µF 50 V X7R 1206, Samsung CL31B475KBHNNNE (1.6 ± 0.2 mm) | Fab stock; any 50 V X7R 1206 no taller than 1.8 mm |
| C2 | 1 µF 50 V X7R 0603 (CL10B105KB8NNNC) | Fab stock |
| C3, C4 | 1 µF 10 V X5R 0402 (CL05A105KP5NNNC) | Fab stock |
| C5 | 100 nF 50 V X7R 0603 (CL10B104KB8NNNC) | Fab stock |
| R1 | 1 kΩ 0805 **anti-surge**, Panasonic ERJ-P06J102V (0.5 W) | Fab stock, or consign: a plain 0805 is not a substitute (0.4 W pulses) |
| R2 | 470 Ω 1206 **anti-surge**, Panasonic ERJ-P08J471V (0.66 W) | Fab stock, or consign |
| R3 | 100 kΩ 0402, 1 % | Fab stock |
| R4 | 33 kΩ 0402, 1 % | Fab stock |

## J1, by hand (after assembly)

1. Seat J1 on the B face with its pegs in the peg hole and slot; they fit only one way round. The pad row then faces the board edge that carries Q1 (the lower edge in the robot, −Z).
2. Solder the four stakes from the F (parts) side first, through the plated slots, so the receptacle is held square.
3. Then solder the six SMT tails on the B face; they reach 0.62 mm past the shell.
4. **Keep the B face flat.** Clip or file the stake fillets on B flush with the pads. Nothing but J1's land pattern may stand proud: the face sits on the printed pad's seat, and only the 10.60 × 5.60 mm relief is cut ([D-069](../../../../decisions.md#d-069)).
5. Check for no short between `VBUS` (A9/B9) and the GND pads, or between CC1 and CC2.

## Open for stage 2

- **DFM check** with each quoting fab: plated slot sizes, the 0.5 mm QFN, via tenting, and the 28 × 15 mm size (panelise for Lion MII).
- **Consign** U1, Q1, D2 (element14 India) and D1 (Mouser India). J1 comes to the builder with them.
- **NVM image and jig** ([CP-OI-05](../../../open-items.md)): programming pads TP1–TP4 (`VBUS`, `GND`, SCL, SDA) on the 2.54 mm grid at board-local (19.6, 12.05), (22.14, 12.05), (19.6, 9.51), (22.14, 9.51). The jig base locates on the two Ø2.2 holes, with a pocket for J1, which stands 6.5 mm below the B face.
- **`W16`**: 2 × AWG22, 150 mm, lap-soldered to J2 (pad 1 `VSNK`, pad 2 `GND`) and held by a silicone bead. Micro-Fit 3.0 43025-0200 with 43030 females at the far end, into PCB-02 `J2-8` (pin 1 `VSNK`).
- **Quantity**: one board is installed; order at least 3 (a spare and a bench board).
