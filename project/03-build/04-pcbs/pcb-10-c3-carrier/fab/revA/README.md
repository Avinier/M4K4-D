# PCB-10 rev A: fabrication outputs

Exported 2026-10-28 from `../../design/pcb-10-c3-carrier.kicad_pcb` with the KiCad 10.99 nightly `kicad-cli`. These are design outputs, not an order: stage 2 (procure) chooses the fab by quote ([D-062](../../../../decisions.md#d-062)), and every board is designed before any is ordered ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's bottom-left corner as seen from the top (component) face, world (56, Z 76). The Gerbers, the drill files and the placement files agree, so the fab's placement preview lines up without manual offsets.

| File | Contents |
|---|---|
| `pcb-10-c3-carrier-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.g1, *.g2, *.gbl` | Copper, Gerber X2, Protel extensions. **F.Cu**: all parts and most signals. **In1.Cu**: solid GND plane. **In2.Cu**: +3V3 plane, plus three slow tracks (WDO, C3_READY, SLP). **B.Cu**: no parts; the top-row descents, UART, watchdog control lines and `+5V_DK` round the edges |
| `gerbers/*.gts, *.gbs` | Front and back solder mask. **Vias are tented both sides.** The back opens only at the THT pads (the DevKitC's 44, JP1's 2, the Micro-Fit's 2) and the three non-plated holes |
| `gerbers/*.gtp` | Front paste (stencil). No back paste |
| `gerbers/*.gto` | Front silkscreen: footprint outlines only. Reference labels are on the fab layer. J1's outline runs past the +X edge (the plug mates there), and the fab clips it |
| `gerbers/*.gm1` | Board outline, 70.0 × 49.5 mm, **notched** 8.5 × 3.0 mm at the bottom edge (x 5.0–13.5 from the left corner, as seen from the top) over the chassis DRV8833's terminal block |
| `gerbers/*-PTH.drl` | Excellon drill, mm, plated: 96 vias of 0.35 mm, the DevKitC's 44 holes of **1.0 mm**, JP1's two 0.8 mm holes, the Micro-Fit's two 1.02 mm holes |
| `gerbers/*-NPTH.drl` | Non-plated: the two Ø2.7 M2.5 screw holes (H1, H2) and the Micro-Fit's Ø3.0 peg |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `gerbers/*-job.gbrjob` | Gerber job file: 4 layers, 1.6 mm, the stackup below |
| `pcb-10-c3-carrier-revA-bom.csv` | Fab BOM, grouped: 30 lines, 66 parts. Left out: the unfitted parts (R18, R19, R24–R27), the test pads, the holes, and **U1, the DevKitC** (hand-soldered after assembly) |
| `pcb-10-c3-carrier-revA-pos.csv` | KiCad placement file, mm, top only, board-local origin: the same 66 parts |
| `pcb-10-c3-carrier-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. In the fab's preview, check **U3 pin 1** (DDF0008A), U2/U4/U5 and Q1 pin 1 against the silkscreen, D1's cathode bar, and the GH headers' latches toward the board's top edge |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | **4** ([D-068](../../../../decisions.md#d-068), amended at placement) |
| Size | 70.0 × 49.5 mm, notched; single board |
| Thickness | **1.6 mm**: the DevKitC's headers, the Micro-Fit and the printed hooks all expect it |
| Stackup | F.Cu 35 µm, prepreg 0.2104, In1 15.2 µm, core 1.065, In2 15.2 µm, prepreg 0.2104, B.Cu 35 µm: JLCPCB's 7628 build. Any fab's standard 1.6 mm 4-layer build will do; impedance isn't controlled |
| Copper | 1 oz outer, 0.5 oz inner |
| Finish | HASL lead-free or ENIG |
| Solder mask | Any colour; vias tented both sides. The back face bears on the printed uprights |
| Silkscreen | Top only |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 mm hole / 0.67 mm pad, via copper ≥ 0.31 mm to other copper, copper ≥ 0.3 mm from the edge (fab-neutral, D-062). Smallest pitch: U3's 0.65 mm |
| Assembly | **One side (top).** Reflow: every SMD part. **THT: J1 (Micro-Fit, keep the full 3.18 mm tails; 10 mm of air behind the board) and JP1.** **U1 is not fab-assembled**: the genuine Espressif v1.1 is hand-soldered through its own headers after assembly, tails clipped to 1.5 mm (D-068; the uprights' reliefs take them) |

## Parts

| Ref | Part | Source (lesson 1, 2026-10-27) |
|---|---|---|
| U1 | **ESP32-S3-DevKitC-1-N8, genuine Espressif board v1.1** (CH-045) | Builder: Tech Depot (GST invoice), Sharvi or Compoindia (D-068). Not on the fab BOM |
| U2 | **THVD1451DR**, SOIC-8 | Mouser India (D-068). Pin-compatible fallback: MAX3490EESA+, element14 India 2518822 |
| U3 | **TPS3436CCCBGDDFRQ1**, DDF0008A (CH-086) | **Mouser India** 595-S3436CCCBGDDFRQ1; DDP on a GST business invoice, otherwise duty at delivery. Consign it: no LCSC stock |
| U4 | SN74LVC1G08DBVR | element14 India 3120596, or LCSC C7666 |
| U5 | SN74LVC1G11DBVR | element14 India 3006613, or LCSC C22046 |
| Q1 | AO3400A | LCSC C20917 (basic part) |
| D1 | B5819W, SOD-123 | LCSC C8598 |
| J1 | Molex 43650-0200 | element14 India 2324861 |
| J2, J5, J6 | JST BM06B-GHS-TBT | From the fab's stock (LCSC part to look up) |
| J3, J4, J10, J12 | JST BM04B-GHS-TBT | From the fab's stock (LCSC part to look up) |
| J7 | JST BM08B-GHS-TBT | From the fab's stock (LCSC part to look up) |
| J8 | JST BM05B-GHS-TBT | From the fab's stock (LCSC part to look up) |
| JP1 | 1 × 2 header, 2.00 mm pitch, plus a 2.00 mm shunt (service: watchdog off) | Choose at stage 2 |
| C1, C3, C10 | 10 µF X5R 0805, **10 V** or higher (C1/C10 on the 5 V input) | Choose a stocked MPN at stage 2 |
| C2, C4–C8, C11 | 100 nF X7R 0402, 16 V | Choose a stocked MPN at stage 2 |
| C9, C12 | 1 nF X7R 0402, 50 V | Choose a stocked MPN at stage 2 |
| R1–R5, R15, R33, R38 | 10 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| R6, R9, R10, R16, R32, R37, R41, R42 | 1 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| R7, R8, R35, R43 | 100 kΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| R11–R14, R20–R23 | 100 Ω 0402, 1 % | Choose a stocked MPN at stage 2 |
| R17 | 120 Ω 0402, 1 % (RS-422 termination) | Choose a stocked MPN at stage 2 |
| R28–R31 | 33 Ω 0402, 1 % (SPI series) | Choose a stocked MPN at stage 2 |
| R34 | 100 Ω 0603 (TCRT LED) | Choose a stocked MPN at stage 2 |
| R36 | 10 kΩ 0603 | Choose a stocked MPN at stage 2 |
| R39, R40 | 22 kΩ, 1 MΩ 0402, 1 % | Choose a stocked MPN at stage 2 |
| Not fitted | R18, R19 (RS-422 fail-safe bias, 560 Ω), R24–R27 (encoder pull-ups, 10 kΩ) | Footprints only; fit on the bench if needed |

## Open for stage 2

- **DFM check.** Upload the zip to each quoting fab's DFM check. Watch U3's 0.65 mm pitch, the notched outline and the via tenting.
- **Consign U2 and U3.** Neither is at LCSC with stock. Order them from Mouser India with the build's other Mouser parts (one GST business invoice ships DDP), and consign them to the fab, as PCB-06 does with its mic.
- **The DevKitC goes on last.** Solder it after assembly, by hand, through its own header pins: check it sits flat on its plastic, then clip the tails to 1.5 mm below the board. Before soldering, confirm it is the genuine Espressif v1.1 (LED on GPIO38).
- **Quantity.** One board is installed; order at least 3 (a spare and a bench board).
