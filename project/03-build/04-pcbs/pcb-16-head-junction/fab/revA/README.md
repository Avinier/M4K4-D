# PCB-16 rev A: draft fabrication outputs

**Do not order yet.** These are design outputs ([D-062](../../../../decisions.md#d-062), [D-064](../../../../decisions.md#d-064)). Gates are under [Before ordering](#before-ordering).

Exported 2026-11-10 by `python3 layout_pcb16.py --export` (KiCad 10.99 Nightly) after parity DRC 0/0/0. The board STEP passes `check_pcb16_fit.py` 7/7 ([D-103](../../../../decisions.md#d-103)). One origin for every file: the board's bottom-left corner seen from the top.

| File | Contents |
|---|---|
| `pcb-16-head-junction-revA-gerbers.zip` | Gerber, drill and job files, ready to upload |
| `gerbers/*.gtl, *.gbl` | **F.Cu**: both ZIF land patterns, the head-power fields, the C2/display and signal lanes, the wire pads. **B.Cu**: empty |
| `gerbers/*.gm1` | Stepped outline, 36.4 × 18.5 mm overall, with two Ø2.2 mm M2 holes |
| `gerbers/*.drl` | No drilled holes (the M2 holes are routed) |
| `pcb-16-head-junction-revA-bom.csv` | Fab BOM: 2 × FH34SRJ-22S-0.5SH(99). The wire pads are bare copper |
| `pcb-16-head-junction-revA-pos.csv`, `-cpl-jlcpcb.csv` | Placement; both ZIF mouths face the board's front (−Y) edge |

## Order parameters

| Parameter | Value |
|---|---|
| Layers / thickness | 2 / **0.8 mm** |
| Copper / finish | 1 oz; ENIG (0.5 mm-pitch FH34SRJ pads) |
| Smallest features | Track 0.2 mm, gap ≥ 0.16 mm, copper ≥ 0.3 mm from the edge (fab-neutral, D-062) |
| Assembly | Top side SMD: J1, J2. Wires are soldered to the pads by hand at harness assembly |

## Assembly and installation

- Solder the harness wires to the pads on the bench (wire map in [05-harness §5](../../../../05-harness/README.md#5-pinouts-and-polarity)), then fit the board to the disc with two M2 × 4 button screws into the disc's M2 inserts.
- **Plug order:** W43 signal into J1 (near) and close it, then W42 power over it into J2 (far).
- Dress the bundles out of the two exits (+X edge and far edge) and keep everything below the sweep floor, 4 mm above the disc top.

## Before ordering

- Route the wire bundle across the pitch and roll joints from the labelled exits, and the CSI path to the camera.
- A strip of the received generic FFC through both S-bends into an FH34SRJ sample.
- Check the pad sizes against the received AWG20/AWG28 wire.
- The PCB-08, PCB-12 and PCB-14 gates, for the single D-064 order.
