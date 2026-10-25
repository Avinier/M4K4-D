# PCB-15 — Nose Hall carrier

DRV5055A3 Hall sensor with decoupling and output filter, for the ball-nose touch.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-064 in [BOM.csv](../../BOM.csv) |
| Location | Chassis nose, in the pod-seat slot |
| Specification | [nose-hall-board.md](../../01-chassis/v1/research/nose-hall-board.md)<br>[D-013](../../decisions.md#d-013), [D-057](../../decisions.md#d-057), [D-059](../../decisions.md#d-059) |
| CAD placeholder | `_nose_sensing_parts()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py); seat relief: `DROID_CUTS` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |
| CAD labels | `BALL_NOSE_HALL_CARRIER_PCB`, `BALL_NOSE_HALL_DRV5055A3_SOT23` |
| Final CAD | `Custom PCBs › PCB-15 nose Hall carrier` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Done: rev A.** Schematic, layout, fab outputs and board STEP committed; the envelope change has its decision ([D-063](../../decisions.md#d-063)) | [design/](design/), [fab/revA/](fab/revA/README.md), [cad/](cad/) | 2026-10-25 |
| 2. Procure | Waits for the design batch ([D-064](../../decisions.md#d-064)) | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-14.

**Spec sources.** [nose-hall-board.md](../../01-chassis/v1/research/nose-hall-board.md) (parts, nets, placement, J10-8 pinout), [D-013](../../decisions.md#d-013), [D-057](../../decisions.md#d-057), the [DRV5055 datasheet](https://www.ti.com/lit/ds/symlink/drv5055.pdf). KiCad stock parts: symbol `Sensor_Magnetic:DRV5055A3xDBZxQ1`, footprints `Package_TO_SOT_SMD:SOT-23`, `Capacitor_SMD:C_0402_1005Metric`, `Resistor_SMD:R_0402_1005Metric`.

**Circuit.**

| Ref | Part | Pins and nets |
|---|---|---|
| U1 | DRV5055A3QDBZR, SOT-23 | 1 VCC → +3V3, 2 OUT → HALL_RAW, 3 GND → GND |
| C1 | 100 nF X7R 0402, 10 V | +3V3 to GND, at U1 (datasheet: ≥ 10 nF) |
| R1 | 1 kΩ 0402 | HALL_RAW to HALL_OUT |
| C2 | 100 nF 0402 | HALL_OUT to GND (R1 + C2: 1.6 kHz low-pass) |
| P1, P2, P3 | 0.8 × 1.2 mm wire pads, back face | +3V3, GND, HALL_OUT |

**Interface.** No connector: three wires of the J10-8 cable are soldered to P1–P3, which go to PCB-10 J10-8 pins 4 (+3V3), 2 (GND) and 5 (HALL_OUT, a C3 ADC input).

**Supply and protection.** +3V3 from PCB-10. The datasheet (SBAS640C) gives I<sub>CC</sub> 2 mA typical and 4 mA maximum at 3.3 V, and a 3.0–3.63 V supply range. The board has no polarity or ESD protection of its own: it is wired once and stays inside the pod. Detecting a broken or unplugged wire needs a defined bias on HALL_OUT at the C3 end (the spec's 2026-09-30 review gate). That bias belongs to PCB-10, not to this board.

**Envelope** (from the CAD source; both `body_v1_model.py` and `01-chassis/v1/cad/body_chassis_model.py` carry the same constants). Board-local coordinates: local Y = world Y − 7.0, local Z = world Z − 30.4. The front face points +X, towards the cap.

| Item | Value |
|---|---|
| Outline | 6.0 (Y) × 4.6 (Z) × 0.8 mm, world X 126.2–127.0 ([D-063](../../decisions.md#d-063); X 126.6–127.4 before it), Y 7.0–13.0, Z 30.4–35.0. Slot X 126.1–127.1 |
| Mounting | No holes. The board stands in a slot open at the top, 0.1 mm clearance per side, fixed with CA or hot glue |
| U1 | Front face, centred at local (3.0, 2.2), long axis along Y. Body 1.0 mm tall in CAD (1.12 max) |
| Front clear zone | Only the sensor notch: local Y 1.3–4.7, Z 0.8 up to the top edge |
| Back clear zone | Seat relief pocket ([D-059](../../decisions.md#d-059); 1.3 mm deep since D-063): local Y 0.8–5.2, Z 0–4.6, parts at most 0.9 mm tall (the design limit is unchanged). It joins the lead groove (local Y 2.5–5.5, Z 3.1 up), where P1–P3 sit. C1, R1 and C2 go here |
| Everywhere else | 0.1 mm to the seat on each face: no parts. The board's ends bear on both slot walls |

**Gaps.**

1. **Closed by [D-059](../../decisions.md#d-059): no room for C1, R1 and C2.** On the front, U1's SOT-23 pads reach local Z 3.9, which leaves 0.7 mm under the top edge of the notch. An 0402 with its edge clearance does not fit there. The spec's C1 position, local Y 5.2, lies outside the notch (it ends at 4.7). On the back, R1 and C2 at local Z 1.0–2.0 are below the lead groove and face the seat wall 0.1 mm away. The CAD models the board as a plain block with only U1 on it, so no check could have caught this. D-059 adds the seat relief behind the board, and all three parts move to the back face.
2. **Closed 2026-10-25:** datasheet SBAS640C Figure 6-5 puts the SOT-23 Hall element 650 ± 80 µm below the package top, centred within ± 50 µm. That confirms the trip-point model's 0.65 mm.
3. The spec's last paragraph still calls Ø2 × 1 mm the baseline magnet, but its parts table and the CAD use Ø3 × 1.5 mm. This does not affect the board.
4. A 6.0 × 4.6 mm board is below the assembly minimum of every shortlisted fab (JLCPCB 10 × 10 mm, Lion Circuits 50 × 100 mm, PCBWay by quote), so it needs a panel. Check this at DFM.

## Schematic

[`design/pcb-15-nose-hall.kicad_sch`](design/pcb-15-nose-hall.kicad_sch), with a PDF print, [`pcb-15-nose-hall-schematic.pdf`](design/pcb-15-nose-hall-schematic.pdf). Project footprint library `pcb15` ([`design/pcb15.pretty`](design/pcb15.pretty)) holds the wire pad `WirePad_0.8x1.2mm`. It is marked as left out of the BOM and the pick-and-place file, because it is bare copper.

**ERC** (`kicad-cli sch erc --severity-all`, 2026-10-14): 0 errors, 0 warnings.

**Check against the spec**, row by row, using the exported netlist:

| Spec row | Schematic | Result |
|---|---|---|
| +3V3: U1 pin 1 VCC, C1, wire pad 1 | `+3V3`: U1.1, C1.1, P1 | Match |
| GND: U1 pin 3, C1, C2, wire pad 2 | `GND`: U1.3, C1.2, C2.2, P2 | Match |
| HALL_OUT: U1 pin 2 through R1 to pad 3, C2 from pad 3 to GND | `HALL_RAW`: U1.2, R1.1. `HALL_OUT`: R1.2, C2.1, P3 | Match. `HALL_RAW` names the U1-to-R1 link the spec leaves unnamed |
| U1 DRV5055A3QDBZR, SOT-23, pins 1 VCC / 2 OUT / 3 GND | Stock KiCad symbol `DRV5055A3xDBZxQ1`, footprint `SOT-23`; pinout checked against datasheet Table 4-1 | Match |
| C1 100 nF X7R 0402 10 V, ≥ 10 nF | 100n X7R 10V, `C_0402_1005Metric` | Match (datasheet §7.4: ≥ 0.01 µF ceramic) |
| R1 1 kΩ 0402, C2 100 nF 0402: 1.6 kHz | 1k and 100n X7R 10V, 0402 | Match: 1/(2π · 1 kΩ · 100 nF) = 1.59 kHz |
| No capacitor directly on OUT | C2 sits behind R1 | Match (datasheet §7.1.3) |
| Wire pads 0.8 × 1.2 mm: +3V3, GND, OUT | P1, P2, P3 on `WirePad_0.8x1.2mm` | Match |

**Carry to PCB-10.** For wire-break detection, the datasheet (§7.1.4) puts a 20–100 kΩ pull-up from HALL_OUT to VCC at the receiving end, and reads a fault when the output is within 150 mV of either rail. At the 3 mm stop the field is far past the linear range, so the PCB-10 and firmware design must check that a pressed cap cannot read as a fault.

## Layout

KiCad 10.99 nightly, laid out by hand through KiPy without an autorouter ([D-060](../../decisions.md#d-060), [Layout rules](../README.md#layout-rules)).

**Board set-up** (`design/pcb-15-nose-hall.kicad_pcb`, `.kicad_pro`):

| Item | Value | Why |
|---|---|---|
| Outline | KiCad x 100–106, y 100–104.6 | Board-local Y = x − 100, Z = 104.6 − y. The aux and grid origins sit at local (0, 0), so the pick-and-place file reads in board-local Y/Z |
| Faces | F.Cu is the front face, towards the cap; B.Cu is the back face | U1 is the only front part |
| Stackup | 0.8 mm: 35 µm copper, 0.71 mm FR4 core, mask, HASL lead-free | Spec |
| Rules | Fab-neutral ([D-062](../../decisions.md#d-062)), in `design/pcb-15-nose-hall.kicad_dru`: gap and track ≥ 0.16 (0.2 used), via 0.67/0.35, via copper and hole ≥ 0.31 from other-net copper, copper to edge ≥ 0.3, hole to hole ≥ 0.31 | The strictest of JLCPCB, PCBWay and Lion Circuits MII ([table](../README.md#fab-neutral-design-rules)), so any of the three can make the board. `.kicad_pro` still holds the older JLCPCB-only minimums (0.15, via 0.5/0.3). The `.kicad_dru` overrides them in DRC. Update the `.kicad_pro` while KiCad is closed |
| Seat keep-outs | Rule areas forbid footprints on F.Cu outside the notch (`FRONT_SEAT`) and on B.Cu outside the relief and lead groove (`BACK_SEAT_L`, `BACK_SEAT_R`). The notch, relief and groove are also drawn on the user layers `Seat.Notch`, `Seat.Relief` and `Seat.Groove` | DRC then checks the D-059 envelope on every run |

**Land-pattern changes from the spec:**

- **U1 uses `pcb15:SOT-23_NoseNotch`, not the stock SOT-23.** The notch's bottom edge is 1.40 mm below U1's centre (local Z 2.2 vs 0.8). The stock pads reach 1.675 mm and TI's land example 1.70 mm, so the lower pads' solder toes would sit against the seat 0.1 mm away. The trimmed pads run 0.40–1.35 mm. That keeps the heel as TI draws it and leaves a 0.17 mm toe at nominal lead span (0.03 mm at the 2.64 mm maximum), roughly IPC-7351 least density. The courtyard stops at 1.39 mm on the toe sides.
- **Wire pads P1–P3 move down 0.3 mm** to local Z 3.1–4.3 (the spec gives 3.4–4.6). That keeps their copper 0.3 mm from the top edge (fab-neutral rule), and they stay inside the lead groove (Z ≥ 3.1).

**Placement and routing** (2026-10-25, through KiPy, parts placed in functional groups, no autorouter). KiCad coordinates, mm:

| Part | Side | Position, rotation | Notes |
|---|---|---|---|
| U1 | Front | (103.0, 102.4), 90° | Pin 3 GND up at (103.0, 101.525); pin 1 VCC (102.05, 103.275) and pin 2 OUT (103.95, 103.275) down |
| C1 | Back | (102.55, 102.0), 0° | Behind U1: +3V3 pad left, GND pad right. 0.2 mm left of centre to make room for the GND via |
| C2 | Back | (104.7, 102.48), 90° | GND pad up, in line with the GND via; HALL_OUT pad down |
| R1 | Back | (104.19, 103.95), 0° | HALL_RAW left; HALL_OUT right, in line with C2's HALL_OUT pad |
| P1, P2, P3 | Back | (102.9 / 104.0 / 105.1, 100.9) | +3V3, GND, HALL_OUT |
| Vias, 0.67/0.35 | — | +3V3 (101.2, 103.275); GND (103.85, 102.02); HALL_RAW (103.05, 103.1), under U1 between pins 1 and 2 | One per U1 pin, tented. At least 0.31 mm from other-net copper, and 0.16 mm from their own net's pads, a mask web that keeps solder out of the hole. A grid search found these as the only legal spots |

The front carries only U1's three fan-out stubs. Every other track is on the back: 0.2 mm wide, horizontal, vertical or 45° (the routing script refuses any other angle). HALL_OUT runs up the right edge to P3, 0.45 mm in from it.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, fab-neutral `.kicad_dru` of D-062 in place, 2026-10-25): 0 errors, 0 unconnected pads, 0 schematic-parity issues, 0 seat keep-out hits. A scratch copy with the via-hole minimum raised to 0.4 mm flagged all three vias, so the rules file is enforced. Four warnings remain, all `lib_footprint_mismatch`, on U1, C1, C2 and R1. The board copies were placed straight from the libraries by Update PCB from Schematic and not edited. The flagged footprints are the ones with rounded-rectangle pads, and the warning appeared before any routing. It looks like a quirk of the 10.99 nightly's library comparison, not a real difference. Recheck it on a later nightly.

Reference labels moved from silkscreen to the fab layers: 1 mm silkscreen text (JLCPCB's minimum) has no room on this board.

**Corrections, 2026-10-25 (lesson 6).**

- **The `lib_footprint_mismatch` warnings were not only a nightly quirk.** The 3D models of U1, C1, C2 and R1 had been stripped. KiCad's local history (`design/.history`) shows the snapshot saved after Update PCB from Schematic (12:54) had 4 models, and the next save (12:57, the first KiPy placement, which flipped parts to the back) had none. A board without models exports a STEP without parts. The models were restored through KiPy (`Footprint3DModel`), and they survive later KiPy updates. The four warnings that remain are cosmetic. U1's pads and model match the library exactly; its fab outline differs by about 1 nm of rotation round-off (`-0.649999` against `-0.65`). C1, C2 and R1 also carry the reference labels moved to the fab layers.
- **Update PCB from Schematic drops `exclude_from_pos_files`.** The schematic symbol says only "not in BOM", so P1–P3 lost the footprint's "not in position files" flag and appeared in the placement file. The flag was set again on P1–P3 through KiPy. **After any future F8, set it again**, or the wire pads go to the assembler as parts.

## Checks and outputs (rev A)

- **ERC** 0 errors, 0 warnings. **DRC** with schematic parity: 0 errors, 0 unconnected, the 4 cosmetic warnings above.
- **Outputs:** [`fab/revA/`](fab/revA/README.md) holds Gerber X2, Excellon drill, the placement file (KiCad and JLCPCB CPL formats), the fab BOM, a Gerber zip and the order parameters.
- **Board STEP:** [`cad/pcb-15-nose-hall-revA.step`](cad/pcb-15-nose-hall-revA.step), with parts. Its board core runs Z 0–0.71. Components sit 0.085 mm off the core. KiCad's SOT-23 model is 1.2 mm tall (TI: 1.12 max), and the 0402 models are 0.5 mm (C) and 0.35 mm (R).
- **Fit in the robot:** [`final/v1/cad/check_pcb15_fit.py`](../../final/v1/cad/check_pcb15_fit.py) places the STEP in the nose seat with the core on the board's nominal mid-plane. The first run, at D-013's position (mid-plane world X 127.0), cleared the seat everywhere (gaps 0.10 mm for the board, 0.15 for U1 at the notch walls, 0.25–0.50 for the back parts) but **FAILed on the cap stop:**

  | Case | U1 top, world X | Air to the magnet at the 3 mm stop (pod face X 128.5) |
  |---|---|---|
  | CAD placeholder, 1.0 mm block (D-013's figure) | 128.400 | +0.100 |
  | Real part: nominal 1.0 mm, board at its CAD position | 128.465 | +0.035 |
  | KiCad's 1.2 mm model, board on its mid-plane | 128.640 | −0.140 (0.49 mm³ overlap with the magnet) |
  | Real part: 1.12 mm max, 0.88 mm board against the front slot wall | 128.705 | −0.205 |

  At full press the magnet could bear on U1. D-013's "0.1 mm of air remains" holds only for the 1.0 mm placeholder on a board that never moves in its slot.

  **Fixed by [D-063](../../decisions.md#d-063)** (builder, 2026-10-25): the board and its 1.0 mm slot move 0.4 mm back, and the relief deepens to 1.3 mm. The board design is unchanged. Re-run at mid-plane X 126.6, **PASS**: KiCad model air +0.260 mm with no contact with the magnet or cap; real part +0.435 nominal and +0.195 worst case; gaps to the seat 0.10 (board), 0.20 (U1) and 0.25–0.50 (back parts). `check_pcb15_relief.py` also passes on the moved slot. Predicted trip at +12 mT moves from 0.73 to 0.89 mm of travel; bench item 19 measures it.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-14:** design started. Inputs frozen from the spec and the CAD source. Envelope gap 1 found: the seat leaves room only for U1 and the wire pads.
- **2026-10-14:** [D-059](../../decisions.md#d-059) taken (option A). A 0.9 mm relief pocket is cut from the seat behind the board, in `final/v1/cad` only. `check_pcb15_relief.py` passes, and both droid STEPs were rebuilt.
- **2026-10-14:** schematic drawn in KiCad 10 from the spec. ERC 0 errors, 0 warnings. The netlist matches the spec's net table row by row. Supply current confirmed from the datasheet (2 mA typ, 4 mA max).
- **2026-10-25:** layout started on the KiCad 10.99 nightly (D-060). Board file set up with the outline, 0.8 mm stackup, JLCPCB-margin rules and seat keep-outs; DRC on the empty board: 0 violations. Custom U1 land pattern `SOT-23_NoseNotch` added (toes trimmed to fit the notch), and wire pads moved 0.25 mm off the top edge. Hall element depth confirmed from the datasheet (gap 2 closed).
- **2026-10-25:** placed and routed by hand through KiPy on the 10.99 nightly (D-060): U1 on the front with three via fan-outs; C1, R1, C2 and P1–P3 on the back. DRC 0 errors, 0 unconnected, schematic parity clean. 4 `lib_footprint_mismatch` warnings, believed to be a nightly quirk.
- **2026-10-25:** re-checked against the fab-neutral rules ([D-061](../../decisions.md#d-061)). The first run flagged 10 errors: vias too small (0.5 → 0.62), the HALL_RAW via 0.22 mm from U1's VCC pad, and the wire pads 0.25 mm from the edge. Fixed by re-placing P1–P3 (+0.05 mm) and R1 (+0.19 mm) and re-routing. DRC 0 errors, 0 unconnected, parity clean; the same 4 `lib_footprint_mismatch` warnings.
- **2026-10-25:** re-laid to [D-062](../../decisions.md#d-062): the fabs are JLCPCB, PCBWay and Lion Circuits MII only. Vias 0.62/0.3 → 0.67/0.35, with 0.31 mm via spacing (Lion MII). C1 moved 0.2 mm left, and all three vias moved to the only legal spots a grid search found; re-routed by hand through KiPy. DRC 0 errors, 0 unconnected, parity clean; the same 4 `lib_footprint_mismatch` warnings.
- **2026-10-25:** lesson 6. 3D models restored (stripped by KiPy's flip) and the wire pads' position-file flag set again (dropped by F8). Rev A outputs exported to `fab/revA/`; board STEP to `cad/`. New fit check `final/v1/cad/check_pcb15_fit.py`: the board fits the seat, but U1 can touch the magnet at the cap's 3 mm stop (air +0.035 mm nominal, −0.205 mm worst case). Decision needed before release.
- **2026-10-25:** [D-063](../../decisions.md#d-063) taken (option A): board and slot 0.4 mm back, relief 1.3 mm deep, all in `final/v1/cad` (new `DROID_ADDS` and `DROID_MOVES`). Fit and relief checks PASS. Rev A committed: stage 1 done.
- **2026-10-25:** [D-064](../../decisions.md#d-064): every board is designed before any is procured, so PCB-15's stage 2 waits for the batch and its order is shared with the other boards.
