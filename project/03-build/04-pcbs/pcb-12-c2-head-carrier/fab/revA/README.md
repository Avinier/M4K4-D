# PCB-12 rev A: draft fabrication outputs

**Do not order yet.** These are design outputs. The fab is chosen by quote at stage 2 ([D-062](../../../../decisions.md#d-062)), and no board is ordered until every board in the batch is designed ([D-064](../../../../decisions.md#d-064)). The board-level gates are under [Before ordering](#before-ordering).

Exported 2026-11-10 from `../../design/pcb-12-c2-head-carrier.kicad_pcb` by `python3 layout_pcb12.py --export` (KiCad 10.99 Nightly `kicad-cli`), after parity DRC 0 violations / 0 unconnected / 0 parity. The board STEP (`../../cad/pcb-12-c2-head-carrier-revA.step`) passes `check_pcb12_fit.py` 7/7 ([D-102](../../../../decisions.md#d-102)).

**One origin for every file**: the board's bottom-left corner seen from the component face.

| File | Contents |
|---|---|
| `pcb-12-c2-head-carrier-revA-gerbers.zip` | Gerber, drill and job files from `gerbers/`, ready to upload |
| `gerbers/*.gtl, *.gbl` | Copper. **F.Cu**: all parts, signal lanes, GND pour (none under the Zero). **B.Cu**: GND plane, +5V_C2 and +3V3 trunks, two SERVO_DIR crossings |
| `gerbers/*.gts, *.gbs` | Solder mask; vias tented (several sit under the Zero) |
| `gerbers/*.gtp` | Paste, top only |
| `gerbers/*.gto, *.gbo` | Silkscreen: outlines on top (references are on Fab); "PCB-12 A" on the bottom |
| `gerbers/*.gm1` | Outline 30 × 43.5 mm with two Ø2.2 mm M2 clearance holes |
| `gerbers/*.drl` | Excellon, mm: 20 vias of 0.35 mm plated; the two M2 holes are routed outline circles |
| `pcb-12-c2-head-carrier-revA-bom.csv` | Fab BOM, 15 lines. TP1 is bare copper and left out |
| `pcb-12-c2-head-carrier-revA-pos.csv`, `-cpl-jlcpcb.csv` | Placement, board-local origin. Check in the preview that the Zero's USB-C end is at the top edge and its 5V pad top left |

## Order parameters

| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 30 × 43.5 mm, single board |
| Thickness | **0.8 mm** (fits the head's tray plane between the Zero seat and the crossbar bosses) |
| Copper / finish | 1 oz; ENIG preferred for the castellation lands and SOT-23-5/SOIC pads |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, via 0.35 / 0.67 mm, copper ≥ 0.3 mm from the edge (fab-neutral, D-062) |
| Assembly | Top side SMD: U2–U5, J1–J3, passives. **U1 (the Zero) is soldered by hand** at its castellations after reflow, or by the assembler as a consigned module |

## Parts

| Ref | Part | Source |
|---|---|---|
| U1 | Waveshare ESP32-S3-Zero, **without header** (SKU 25081) | India distributors (Robu, Hubtronics); consign |
| U2 | TI THVD1451DR | As PCB-09; Mouser India / element14 India |
| U5 | TI THVD1450DR | Mouser India / element14 India |
| U3, U4 | TI SN74LVC1G126DBVR, SN74LVC1G125DBVR | Fab stock |
| J1–J3 | JST BM07B/BM02B/BM03B-GHS-TBT | Fab stock |
| Passives | 0603 / 0805, values in the BOM | Fab basic parts |

## Assembly and installation notes

- Mate the GH plugs with the board supported from behind: the 20 mm lower extension is a cantilever (about 0.7 mm deflection at 5 N, `E`).
- Fit the board with the Zero already soldered. Two M2 × 4 button screws go through the board into the crossbar inserts; there is no tray any more.
- **Bring-up:** power from J1 with the servos unplugged. Check +3V3, then the C0/C2 link loopback with PCB-09, then the servo bus at J2 with one servo (feetech-link-contract commissioning).

## Before ordering

- Meter a received Zero: 5V pad to USB VBUS, GND, 3V3. Confirm GPIO1–9 by firmware toggle, and confirm that the castellation pitch and edge positions match the land pattern.
- B5: ST3215-HS VIH/VIL, output high and unpowered leakage against the 3.3 V LVC bus.
- Define the head FFC-to-wire break in the pitch frame (W42/W43 head end) that feeds J1–J3.
- PCB-08 and PCB-14 gates, for the single D-064 order.
