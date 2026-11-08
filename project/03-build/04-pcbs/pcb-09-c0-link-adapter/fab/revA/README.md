# PCB-09 rev A: fabrication outputs

**Historical — do not order.** D-098 requires a rev B interface for the button, M1 OFF and INA226 before PCB-09 fabrication. These files predate that interface.

Exported 2026-11-06 from `../../design/pcb-09-c0-link-adapter.kicad_pcb` by `python3 layout_pcb09.py --export` with the KiCad 10.99 Nightly `kicad-cli`. These are design outputs, not an order. At stage 2 the fab is chosen by quote ([D-062](../../../../decisions.md#d-062)), and no board is ordered until every board is designed ([D-064](../../../../decisions.md#d-064)).

**Every file uses one origin**: the board's bottom-left corner as seen from the top face, world (−11, 16.3). The Gerbers, the drill files and the placement files agree.

| File | Contents |
|---|---|
| `pcb-09-c0-link-adapter-revA-gerbers.zip` | The Gerber, drill and job files in `gerbers/` in one zip, ready to upload |
| `gerbers/*.gtl, *.g1, *.g2, *.gbl` | Copper, Gerber X2, Protel extensions. **F.Cu**: U1, C1, the five GH headers, the head and audio signals, GND pour. **In1.Cu**: GND plane, cut only by the 3V3 and 5V tracks along the strip. **In2.Cu**: +3V3 plane over the bay; BCLK, SDI0 and AMP_SD along the strip. **B.Cu**: the socket J1, U2 and the passives; FAN_EN and the base link; GND pour |
| `gerbers/*.gts, *.gbs` | Solder mask, both faces. Vias are tented both sides |
| `gerbers/*.gtp, *.gbp` | Paste, both faces: **SMD parts on both faces** |
| `gerbers/*.gto, *.gbo` | Silkscreen: footprint outlines only; references are on the fab layers |
| `gerbers/*.gm1` | Outline: a 77.0 × 22.7 mm L. A 40.7 × 6.1 mm strip over the socket, the bridge, a 36 × 16.5 mm connector bay, and two standoff tabs round the M2.5 holes |
| `gerbers/*-PTH.drl` | Excellon, mm, plated: 27 vias of 0.35 mm and J1's 40 holes of 1.0 mm |
| `gerbers/*-NPTH.drl` | Non-plated: the two Ø2.7 M2.5 holes (H1, H2) |
| `gerbers/*-drl_map.pdf` | Drill maps |
| `gerbers/*-job.gbrjob` | Gerber job file: 4 layers, 1.6 mm |
| `pcb-09-c0-link-adapter-revA-bom.csv` | Fab BOM, grouped: 14 lines, 21 parts. The test pads and holes are left out |
| `pcb-09-c0-link-adapter-revA-pos.csv` | KiCad placement file, mm, both faces, board-local origin |
| `pcb-09-c0-link-adapter-revA-cpl-jlcpcb.csv` | The same placement in JLCPCB's CPL columns. In the fab preview, check U1/U2 pin 1, Q1, D1's cathode bar (toward J5 pin 1's via) and J1's pin 1 against the socket map |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | **4** ([D-092](../../../../decisions.md#d-092)) |
| Size | 77.0 × 22.7 mm L-shaped outline; single board |
| Thickness | **1.6 mm**: the socket's 2.64 mm tails and the standoff stack expect it |
| Stackup | F.Cu 35 µm, prepreg 0.2104, In1 15.2 µm, core 1.065, In2 15.2 µm, prepreg 0.2104, B.Cu 35 µm (JLCPCB's 7628 build). Impedance isn't controlled |
| Copper | 1 oz outer, 0.5 oz inner |
| Finish | ENIG or HASL lead-free |
| Solder mask | Any colour; vias tented both sides |
| Smallest features | Track 0.16 mm, gap 0.16 mm, via 0.35 / 0.67 mm, via copper ≥ 0.31 mm to other copper, copper ≥ 0.3 mm from the edge (fab-neutral, D-062). Finest pitch: SOIC 1.27 mm, GH 1.25 mm |
| Assembly | **Two sides, SMD.** Top: U1, C1, J2–J5. Bottom: U2, Q1, D1, R1–R6, C2–C4. **THT: J1** on the bottom face, soldered from the top. Its tails stand about 1.0 mm proud of the top face over the strip, where nothing else is placed. It can be fab-soldered or hand-soldered |

## Parts

| Ref | Part | Source |
|---|---|---|
| J1 | **Samtec SSW-120-01-T-D**, 2 × 20, 2.54 mm, 8.51 mm, tin | element14 (UK stock; an India source, D-066) |
| U1, U2 | **THVD1451DR**, SOIC-8 | Mouser India (D-068); consign. Fallback MAX3490EESA+ (pin-compatible) |
| Q1 | AO3400A, SOT-23 | LCSC C20917 (basic part) |
| D1 | 1N5819HW (Diodes 1N5819HW-7-F), SOD-123 | Check the variant and stock at stage 2; size against the measured fan current |
| J2 | JST SM06B-GHS-TB, side entry | Fab stock |
| J3 | JST BM06B-GHS-TBT | Fab stock |
| J4 | JST BM10B-GHS-TBT | Fab stock |
| J5 | JST BM02B-GHS-TBT (D-092 amended) | Fab stock |
| C1, C2, C4 | 100 nF X7R 0603, 16 V | Choose a stocked MPN at stage 2 |
| C3 | 10 µF X5R 0805, **10 V** or higher (on 5 V) | Choose a stocked MPN at stage 2 |
| R1, R2 | 4.7 kΩ 0603, 1 % (TX pull-ups, D-073) | Choose a stocked MPN at stage 2 |
| R3, R4 | 120 Ω 0603, 1 % (RS-422 receiver terminations) | Choose a stocked MPN at stage 2 |
| R5 | 100 Ω 0603 (FAN_EN series) | Choose a stocked MPN at stage 2 |
| R6 | 100 kΩ 0603 (gate pull-down) | Choose a stocked MPN at stage 2 |
| Not on the board | 2 × M2.5 × 11 mm round male-female standoffs (6 mm thread, Ø ≤ 4.5) and 2 × M2.5 × 5 DIN 912 screws (BO-065) | Hardware, at stage 2 |

## Open for stage 2

- **DFM check.** Upload the zip to each quoting fab's DFM check. Watch the L-shaped outline with its thin +X tab: there is a 0.78 mm web from the hole to the edge. Also check the via tenting, and that bottom paste is present.
- **Two-sided assembly quote**, and whether the fab solders J1. Otherwise the builder hand-solders it, checking it sits square: the board's height above the Pi comes from J1 and the standoffs together.
- **Consign U1 and U2** with the other Mouser India parts.
- **Quantity.** One board is installed; order at least 3 (a spare and a bench board).
