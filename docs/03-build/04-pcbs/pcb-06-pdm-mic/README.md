# PCB-06 (×4) — PDM microphone board

One IM73D122 bottom-port PDM microphone per board; four boards form the array.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-005 in [BOM.csv](../../BOM.csv) |
| Location | Body shell bosses (front/rear, left/right) |
| Specification | [audiosystem.md §3](../../02-body/v1/research/audiosystem.md#3-pcb-06-mic-board--4), [§8](../../02-body/v1/research/audiosystem.md#8-speaker-cavity-and-mic-placement)<br>[D-037](../../decisions.md#d-037) (mounting, lead), [D-066](../../decisions.md#d-066) (strap, mic source) |
| CAD placeholder | `_mic_board()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PDM_MIC_FRONT_L` … `PDM_MIC_REAR_R` |
| Final CAD | `Custom PCBs › PCB-06 PDM microphone boards x4` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Done: rev A.** Schematic, layout, fab outputs (L and R variants) and board STEP; D-066 records the strap, the mic source and the seal-ring clearance; the fit check passes at all four positions | [design/](design/), [fab/revA/](fab/revA/README.md), [cad/](cad/) | 2026-10-27 |
| 2. Procure | Waits for the design batch ([D-064](../../decisions.md#d-064)) | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-26, with [D-066](../../decisions.md#d-066). The builder confirmed C1, C2, R1 and the lead-pad position (gap 5) the same day.

**Spec sources.** [D-037](../../decisions.md#d-037) (shell mounting, 12 × 14 × 1.0 board, soldered lead, vendor-STEP addendum), [D-036](../../decisions.md#d-036) (mic part), BOM rows BO-005, BO-006 (W27), BO-012 (mic), BO-013 (screws), BO-014 (gasket), [audiosystem.md §2.2, §3, §8](../../02-body/v1/research/audiosystem.md#3-pcb-06-mic-board--4), and the CAD in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) (`MIC_*`, `_mic_boss`, `_mic_boss_cuts`, `_mic_board`). Datasheet: [Infineon IM73D122V01 v1.00](https://www.infineon.com/assets/row/public/documents/24/49/infineon-im73d122-datasheet-en.pdf) (2022-08-12; Fig. 12 package, Table 9 pins, Fig. 13 land pattern, Table 8 stereo PDM). Where audiosystem.md and D-037 disagree, D-037 holds: audiosystem.md §1.1, §1.3, §3 and §8 still describe the pre-D-037 board (12 × 9.5, GH header, port boot, Ø3 port, frame-mounted). See gap 1.

**Circuit.**

| Ref | Part | Pins and nets |
|---|---|---|
| MK1 | Infineon IM73D122V01XTMA1, PG-LLGA-5-3 (Infineon's web page calls it PG-LLGA-5-4), bottom port | 1 DATA → MIC_DATA (through R1), 2 VDD → +3V3, 3 CLOCK → CLK, 4 LR → LR, 5 GND (ring round the port) → GND |
| C1 | 1 µF X5R 0402, 10 V | +3V3 to GND at MK1 pin 2. Datasheet Table 5 note 4: "a 1 µF bypass capacitor shall be placed close to the microphone VDD pad" |
| C2 | 100 nF X7R 0402 | +3V3 to GND, at MK1 pin 2. Datasheet §3.5 note: "strongly recommended" |
| R1 | 100 Ω 0402 | MK1 DATA to the DATA wire pad. Datasheet §3.5: "a termination resistor of about 100 Ω may be added to reduce ringing". The BOM's 33 Ω was an estimate (`E`) |
| R_L, R_R | 1 kΩ 0402, exactly one fitted ([D-066](../../decisions.md#d-066)) | R_L: LR to GND (L variant: FRONT_L, REAR_L). R_R: LR to +3V3 (R variant: FRONT_R, REAR_R) |
| P1–P4 | Wire pads for the W27 lead, inner face | GH pin order: P1 +3V3, P2 CLK, P3 GND, P4 DATA (set in the schematic) |

**Pinout check.** Datasheet Table 9: 1 DATA, 2 VDD, 3 CLOCK, 4 LR, 5 GND. KiCad's stock `Sensor_Audio:IM69D120` symbol (the IM69D130's base) has 1 DATA, 2 VDD, 3 CLOCK, 4 SELECT, 5 GND: the same pins, so a derived IM73D122 symbol can use its body. The IM73D122 is not in KiCad's library. The stock footprint `Sensor_Audio:Infineon_PG-LLGA-5-1` (IM69D130) matches Fig. 13 in pad positions: pads at 0.8 and 1.5 mm from the package centre on the side away from the port, ± 0.85 across it, port 0.68 mm from the centre, GND ring R 0.58–1.04, Ø0.8 NPTH. Its pin order is Fig. 13's top view. It differs in pad size: 0.45 × 0.70 mm against Infineon's **0.45 × 0.75**. Its 3D model is the 1.0 mm-tall IM69D130, not this 1.2 ± 0.1 mm part. So stage 2 needs a project footprint with Fig. 13 pads and the Infineon STEP already in `02-body/v1/cad/purchased/`. Fig. 13's pads are solder-mask defined. Stencil: six ring segments and 0.65 × 0.4 mm pad apertures.

**PCB sound hole.** Ø0.8 mm, under the mic's port, not under the package centre: datasheet §5 recommends exactly R 0.4. The CAD has it there (`MIC_PCB_PORT_RADIUS` 0.4, `check_mic_mounts.py` "sound ports on port axes" PASS).

**Interface.** No connector on the board ([D-037](../../decisions.md#d-037)): a pre-crimped, single-ended JST GH 4-way AWG28 lead (W27, BO-006) is soldered to four pads on the inner face and plugs into PCB-05 `J5-2…5` (GHR-04V housing). The +Y boards go to `J5-2`/`J5-3`, the −Y boards to `J5-4`/`J5-5`. Lead length about 150 mm front, 200 mm rear (`E`). The spec's "GH 4 header on the board" (audiosystem.md §1.1, §1.3 W27 "GH 4 at both ends", §3) is the pre-D-037 design. D-037, BO-005, BO-006 and the CAD (`PDM_MIC_*_GH4_PIGTAIL_RESERVE`) all have the soldered lead.

**Strap per position** (audiosystem.md §2.2). Datasheet Table 8: LR = GND drives DATA after the falling clock edge (high-Z on rising); LR = VDD drives it after the rising edge.

| Position | LR | ADAU7002 | Lane | Mounted (see *Envelope*) |
|---|---|---|---|---|
| FRONT_L | GND | #1 | SDI0 left | Turned over |
| FRONT_R | VDD | #1 | SDI0 right | Upright |
| REAR_L | GND | #2 | SDI1 left | Upright |
| REAR_R | VDD | #2 | SDI1 right | Turned over |

The ADAU7002 text says only that PDM data is latched on both edges. Which edge it calls left is in its Fig. 12. The array tap test settles it (§2.2, `U`). A wrong guess swaps the two channels of a lane, which the software can undo, so the board does not depend on it. The two mics on one lane must have opposite straps, or both drive the line on the same edge.

**Supply and protection.** +3V3 is PCB-05's filtered mic rail, which comes from the Pi's 3V3 (audiosystem.md §2.1). The mic draws 0.98 mA typical and 1.12 mA maximum at 3.072 MHz. Its supply range is 1.62–3.6 V, and 3.6 V is also the absolute maximum on any pin, so the rail must not exceed 3.6 V. No ESD or polarity parts: the mic is rated ±2 kV HBM on all pins and ±8 kV contact to the lid, and the board is wired once inside the shell.

**Clock and data over the lead** (PCB-05 design inputs, `U` until the bench). CLK at 3.072 MHz is in the mic's high-performance window (2.9–3.3 MHz). Above 3 MHz the datasheet asks for **48–52 % duty** and ≤ 13 ns rise and fall at the mic. So CLK's source termination at PCB-05 must keep the edge under 13 ns over 200 mm of AWG28. DATA is valid ≤ 100 ns after the clock edge (100 pF load), within the 163 ns half-period less the ADAU7002's 10 ns setup. The lead adds about 10–20 pF, far under the mic's 200 pF limit.

**Sourcing** (2026-10-26).

| Route | Source | State on 2026-10-26 |
|---|---|---|
| Fab's own stock, not used | LCSC/JLCPCB C5563886 | JLCPCB 4,561 in stock, extended part, US$2.89 each in 1–9s; LCSC 4,325 |
| Lion Circuits (MII) | Parts page, ₹355.58 each | "In stock, ships in 7–10 days": probably bought in from a distributor for the order |
| **element14 India 4125831 (BO-012), chosen** ([D-066](../../decisions.md#d-066)) | ₹305.52 each, ₹232.24 in 10s | 19,310 in stock, listed as UK stock, delivery 4–6 business days. The builder counts element14 India as an India source: it invoices in rupees and handles the import. The builder buys the mics and supplies them to the fab |
| Held in India | Evelta, Hubtronics | None found. Robu's search could not be read (Cloudflare). Industrybuying resells Mouser stock (726- part number), shipping in 45 days |

The part is MSL 1 (no floor-life limit). BO-012's "keep sealed in the moisture-barrier bag" is good practice but not required.

**Envelope** (body v1 CAD, measured 2026-10-26 on the built `body_shell()`, `body_audio()`, frame, chassis reference, electronics and hardware solids, and swept over the shell's 0–125 mm lowering path). None of the `final/v1/cad` droid edits touch the body near the mics. Per-position frame: **u** along X toward the body centre (the lead side), **v** = world Z − port Z, **n** inboard from the inner face. The outer face is n = −1.0 at |Y| 71.3.

| Item | Value (all four positions alike in u, v, n) |
|---|---|
| Board | 12 × 14 × 1.0 mm, u −6…6, v −7…7, centred on the port axis. Outer face on the boss seat at \|Y\| 71.3, inner face \|Y\| 70.3 |
| Port | FRONT_L/R (54, ±70, 118), REAR_L/R (−22, ±70, 108). Ø0.8 board hole at (0, 0) |
| Mic | u −2.68…1.32, v −1.5…1.5, n 0…1.30 (vendor STEP); its pads on the post side (−u), its port ring at u 0 |
| Screws | Ø2.2 holes at (0, ±5). M2 × 4 pan heads Ø3.8 × 1.3 on the inner face, u ±1.9, v ±3.1…6.9 |
| Lead reserve (CAD) | u 2.5 to 16 (10 mm past the edge), v ±2, n 0…1.0 |
| Outer face | **Flat, nothing on it.** The seat touches 125.5 of the 168 mm²: the whole board less the Ø7 gasket pocket and the two pilots. The seat runs 2 mm past each side edge (u ±8) and 1.5 mm past the top and bottom (v −8.5…8.55 front, −11…8.55 rear). The gasket (Ø6.5/Ø2.0) presses on the outer face round the hole |
| Inner face, u −6…−5 (post side, full height) | **1.3 mm of air** to the frame's corner post (`BODY_FRAME_MAIN_PRINT`, \|Y\| 69.0), both installed and while the shell is lowered |
| Inner face, u −5…6 | **2.3 mm of air** to the upper side rail (\|Y\| 68.0), which the board passes as the shell is lowered. Nothing nearer when installed |
| Edges | Post side: the frame post starts at u −5 but only from n 1.3 inboard, so the board edge itself is clear. Top: the boss face rises 4.7 mm above the top edge (front). Rear boards, bottom post-side corner: a shell feature at the frame-screw boss, u ≤ −5.4, v ≤ −8, up to n 0.9: 1.0 mm below the board's bottom edge |

**One design, four positions.** The board's lead side (+u) points toward the body centre at every position, which is −X at the front and +X at the rear. Keeping it there needs two orientations: FRONT_R and REAR_L mount one way up and FRONT_L and REAR_R the other way. (Seen from the component face with the lead to the right, world up is +v on FRONT_R/REAR_L and −v on FRONT_L/REAR_R.) Everything above is symmetric in v, so the board must be laid out against the envelope folded about v = 0: a part allowed at (u, v) must also fit at (u, −v).

**Height and area budget** (inner face, with 0.5 mm margin to anything that passes while lowering):

| Zone | Max part height | Courtyard area free |
|---|---|---|
| u −6…−5 | 0.8 mm (an 0402 is 0.55 max) | Shares the post-side zones below |
| Post side beside the mic, u −5.7…−2.93, v ±1.75 | 1.8 mm; the D-037 rule ≤ 1.3 mm | 2.8 × 3.5 mm: three upright 0402s (1.82 × 0.92 courtyards) next to MK1's pins |
| Post-side corners, u −5.7…−2.2, v 1.75…6.7 and mirror | 1.8; D-037 ≤ 1.3 | 3.5 × 4.9 mm each, clear of the screw heads |
| Lead-side corners, u 2.2…5.7, v 2.6…6.7 and mirror | 1.8; D-037 ≤ 1.3 | 3.5 × 4.1 mm each |
| MK1 | 1.30 max (1.2 ± 0.1) + solder | Stock courtyard u −2.93…1.57, v ±1.75 |
| Screw heads | — | Keep parts out of Ø4.4 round each hole: head plus driver |

So the five passives fit by courtyard as well as by height. No envelope change is needed: the board stays 12 × 14 × 1.0 at the CAD position, and nothing goes in `final/v1/cad`.

**Gaps.**

1. **Spec text predates D-037.** audiosystem.md §1.1 (12 × 9.5, "brings it out on a GH 4"), §1.3 (W27 "GH 4 at both ends"), §3 (header, "screwed to the body frame", seal "not designed yet") and §8 (outer face on \|Y\| 70 against a port boot, Ø3 ports) describe the old board. D-037, BOM and CAD agree with each other. Fix the text in the lesson 1 commit.
2. **Closed 2026-10-26 (C1 1 µF, C2 100 nF): decoupling.** The spec had one 0.1 µF (`E`). The datasheet asks for 1 µF close to VDD (Table 5 note 4) and recommends 100 nF (§3.5).
3. **Closed 2026-10-26 (R1 100 Ω): DATA resistor.** BO-005 had 33 Ω (`E`); the datasheet suggests about 100 Ω. The timing margin above allows it: 100 Ω × about 25 pF is 2.5 ns.
4. **Closed by [D-066](../../decisions.md#d-066): mic sourcing.** The builder buys the mics from element14 India (UK stock, counted as an India source) and supplies them to the fab. Check the fab's consigned-parts terms for a reflow-only MEMS part at procure.
5. **Closed 2026-10-26 (pads at u ≥ 3.5): lead pads too close to the mic.** The CAD reserve starts at u 2.5, 1.2 mm from the mic's edge. A soldering iron that close to a reflow-only MEMS part risks heating it. The pads go at u ≥ 3.5 (2.2 mm away), still inside the CAD reserve, so the CAD needn't change.
6. **Frame post over the post-side strip.** Only 1.3 mm of air over u −6…−5 (|Y| 69.0). No spec mentions it. Parts there ≤ 0.8 mm. A rule area in stage 3.
7. **Outer face must stay flat.** It is the seat and the gasket face. No through-hole joints (the wire pads are SMD on the inner face), vias tented, no silkscreen inside Ø7 round the hole.
8. **Edge convention unverified** (ADAU7002 Fig. 12). The tap test settles it; see *Strap per position*.
9. **CLK duty and edge at the mic** (48–52 %, ≤ 13 ns): PCB-05's termination and a bench check. Not a PCB-06 item, but PCB-05's inputs.
10. **Lead strain relief** is not designed. The boards ride down with the shell with their leads hanging free (D-037), and the joints carry the lead's weight. Proposed: a dab of adhesive over the wires at the pad row. Decide at layout.
11. **Panelisation.** A 12 × 14 mm board may be under a fab's assembly minimum; check at fab outputs. D-066's L and R variants are either two BOM/CPL sets on one Gerber set, or one panel mixing L and R boards. Settle that at fab outputs.

### Strap and mic source: decided

[D-066](../../decisions.md#d-066) (builder, 2026-10-26):

- **Strap: option A1, an assembly variant.** R_L (LR to GND) and R_R (LR to +3V3), both 1 kΩ 0402, and the fab fits exactly one. The L variant goes to FRONT_L and REAR_L, the R variant to FRONT_R and REAR_R. Of the other options, A2 (a solder jumper cut by hand) and A3 (an open jumper) need hand work, and A3 leaves LR floating if it is forgotten. Either footprint's pads can be bridged with solder by hand as a fallback.
- **Mic source: option B2.** element14 India 4125831, bought by the builder and supplied to the fab, or reflowed by hand.

## Schematic

[`design/pcb-06-pdm-mic.kicad_sch`](design/pcb-06-pdm-mic.kicad_sch), with a PDF print, [`pcb-06-pdm-mic-schematic.pdf`](design/pcb-06-pdm-mic-schematic.pdf). The design folder was written for the KiCad 10.99 nightly, so it may not open in 10.0.6.

**Project set-up.**

| File | Holds |
|---|---|
| `pcb-06-pdm-mic.kicad_pro` | PCB-11's project, renamed: the fab-neutral board minimums and default net class |
| `pcb-06-pdm-mic.kicad_dru` | The fab-neutral rules ([D-062](../../decisions.md#d-062)), copied from PCB-11 |
| `sym-lib-table`, `pcb06.kicad_sym` | Project symbol library `pcb06`. `IM73D122V01` is KiCad's stock `Sensor_Audio:IM69D120` body (the IM69D130's base symbol, the same five pins), with its own name, fields and datasheet. Pin 4 is renamed SELECT → LR (Table 9) |
| `fp-lib-table`, `pcb06.pretty/` | Project footprint library `pcb06`. `IM73D122V01_PG-LLGA-5-3` is KiCad's stock `Infineon_PG-LLGA-5-1` with pads 1–4 widened from 0.45 × 0.70 to Fig. 13's **0.45 × 0.75 mm**, and the GND ring's inner edge pulled from R 0.58 to **R 0.63** (decision C2, [Layout](#layout)). Unchanged: the pad positions, the ring's outer edge (R 1.04), the Ø0.8 NPTH at the port (0.68 mm off the package centre), and the separate paste apertures (six ring segments, four pad apertures). `WirePad_0.9x2.0mm` is PCB-11's wire pad, sized for one AWG28 conductor lying along it; it has no paste and is left out of the BOM and the position file |
| `pcb06.3dshapes/IM73D122V01_PG-LLGA-5-3.step` | Infineon's PG-LLGA-5-4 package STEP, a copy of `02-body/v1/cad/purchased/infineon_pg_llga_5_4.stp` (SHA-256 `ebf2602a…f873f9b`). Pin 1 and the lid's pin-1 dot fall where the footprint has pin 1, so the model needs no offset or rotation. KiCad's own model would be the 1.0 mm IM69D130 |

The purchased README had this STEP's SHA-256 mistyped (shifted by one character). It is corrected; the file itself is unchanged.

**Parts and fields.** MK1 carries `MPN` IM73D122V01XTMA1, `Manufacturer` Infineon, `Supplier` element14 India 4125831 (builder-supplied, D-066) and the datasheet link. R2 and R3 carry a `Fit` field: R2 for the L variant only (FRONT_L, REAR_L), R3 for the R variant only (FRONT_R, REAR_R). Both are in the schematic and the BOM; the variant is chosen at the fab outputs by leaving one out of each BOM and placement file. D-066's R_L is R2 and its R_R is R3. H1 and H2 are `MountingHole_2.2mm_M2` footprints. Their Ø4.9 courtyard keeps parts off the M2 heads (Ø3.8), so DRC checks the screw-head keep-out. P1–P4 use `Connector:TestPoint`, marked not in the BOM. `PWR_FLAG` sits on +3V3 and GND, which enter through wire pads. The passives get MPNs at procure, as PCB-11's did.

**W27 pin order** (set here, for PCB-05 `J5-2…5` to match): GH pin **1 +3V3, 2 CLK, 3 GND, 4 DATA**. The GND wire runs between CLK and DATA in the lead, so the 3 MHz clock couples less into the data line.

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-26): 0 errors, 0 warnings. KiCad skips its footprint-filter check by default.

**Check against the spec**, row by row, using the exported netlist:

| Spec row ([Inputs](#inputs), D-066) | Netlist | Result |
|---|---|---|
| +3V3: MK1 VDD (pin 2), C1, C2, R_R, wire pad | `+3V3`: MK1.2, C1.1, C2.1, R3.1, P1.1 | Match |
| GND: MK1 GND ring (pin 5), C1, C2, R_L, wire pad | `GND`: MK1.5, C1.2, C2.2, R2.2, P3.1 | Match |
| CLK: wire pad to MK1 CLOCK (pin 3) | `/CLK`: MK1.3, P2.1 | Match |
| DATA: MK1 DATA (pin 1) through R1 to the wire pad | `/MIC_DATA`: MK1.1, R1.2; `/DATA`: R1.1, P4.1 | Match. `MIC_DATA` is the mic side of R1 |
| LR: MK1 LR (pin 4) to R_L and R_R | `/LR`: MK1.4, R2.1, R3.2 | Match |
| MK1 IM73D122V01, pins 1 DATA / 2 VDD / 3 CLOCK / 4 LR / 5 GND | Project symbol pins 1 DATA / 2 VDD / 3 CLOCK / 4 LR / 5 GND; footprint `pcb06:IM73D122V01_PG-LLGA-5-3` | Match (Table 9, Fig. 13) |
| C1 1 µF X5R 0402 10 V, C2 100 nF X7R 0402 | `1u X5R 10V`, `100n X7R 10V`, `C_0402_1005Metric` | Match |
| R1 100 Ω 0402 | `100`, `R_0402_1005Metric` | Match |
| R_L, R_R 1 kΩ 0402, one fitted | R2, R3 `1k`, `R_0402_1005Metric`, `Fit` fields | Match |
| Two Ø2.2 screw holes | H1, H2 `MountingHole_2.2mm_M2`, no net | Match |
| Four wire pads, not in the BOM | P1–P4 on `pcb06:WirePad_0.9x2.0mm`, `in_bom no` | Match |

## Layout

KiCad 10.99 nightly, laid out by hand through KiPy, with no autorouter ([D-060](../../decisions.md#d-060), [layout rules](../README.md#layout-rules)).

**Board set-up** (`design/pcb-06-pdm-mic.kicad_pcb`, written before any part is placed):

| Item | Value | Why |
|---|---|---|
| Outline | KiCad x 100–112, y 100–114 | Board-local xb = x − 100, yb = 114 − y, from the bottom-left corner. The aux and grid origins sit at local (0, 0), so the position file reads in board-local mm. The port is at local (6, 7), KiCad (106, 107). In the lesson-1 frame, u = xb − 6 (toward the body centre, the lead side) and v = yb − 7 |
| Faces | **F.Cu is the inner face**: MK1, the passives and the W27 pads. **B.Cu is the outer face**, on the boss seat and the gasket: copper and mask only | D-037; the outer face must stay flat |
| Stackup | 1.0 mm: 35 µm copper, 0.91 mm FR4 core, mask, HASL lead-free | D-037. Tolerance ±10 % at all three fabs (0.9–1.1 mm): at 1.1 mm the M2 × 4 still forms 2.9 mm of thread, above the 2.5 mm minimum |
| Rules | Fab-neutral ([D-062](../../decisions.md#d-062)) in the `.kicad_pro` and `.kicad_dru`, plus one PCB-06 rule (below) | Any of JLCPCB, PCBWay or Lion Circuits MII can make it |
| Rule areas | `POST_STRIP` (F.Cu, u −6…−5, full height): no footprints, tracks and vias allowed. `OUTER_FACE` (B.Cu, whole board): no footprints. `GASKET_NO_VIAS` (B.Cu, Ø7.0 round the port; a via passes through both faces, so it covers both): no vias | The frame post leaves 1.3 mm over the strip, so no parts there. A rule area can't check height, so "≤ 0.8 mm" becomes "none", which costs 1 mm of width. The outer face is the seat. A via whose mask tent broke under the gasket would let body noise round the seal into the port |
| Custom rule | `PCB-06 wire pads clear of MK1`: courtyard clearance ≥ 1.9 mm between P1–P4 and MK1 | Gap 5: the pads stay ≥ 2.2 mm from the package (MK1's courtyard is 0.25 mm outside it) |
| Already enforced | H1/H2 courtyards (Ø4.9) keep parts off the M2 heads | From the footprints |
| By part choice | Height ≤ 1.3 mm everywhere else (0402s 0.55 max, MK1 1.3) | Not checkable by DRC |
| Drawings | `Frame.Post` (the strip), `Gasket` (Ø2.0, Ø6.5, Ø7.0 pocket), `Screw.Heads` (Ø3.8), `Lead.Exit` (the CAD lead reserve, the u = 3.5 pad limit), `Boss.Seat` (16 × 17) on user layers | Orientation while placing. User layers are not in the fab set |

**DRC on the empty board** (nightly, 2026-10-26): 0 violations. A scratch copy, with deliberate bad placements beside clean controls, proved every envelope rule:

| Test | Result |
|---|---|
| 0402 in the post strip | `items_not_allowed`, `POST_STRIP` |
| 0402 on the outer face | `items_not_allowed`, `OUTER_FACE` |
| Via 2.5 mm from the port / 4.0 mm from it | Flagged by `GASKET_NO_VIAS` / clean |
| Wire pad at u 2.5 / u 3.6 | Flagged: courtyard 0.94 mm against 1.9 / clean |
| 0402 at u −4, v 4 (legal) | Clean |

KiCad loads only the rules file named after the board. The first scratch run, with the file under the wrong name, silently skipped every custom rule, which is a trap worth knowing.

**Open: the sound-hole ring is too close to its hole.** The same scratch run flagged MK1's own GND ring against its Ø0.8 hole: `hole_clearance` 0.21 mm (KiCad's polygon) against the fab-neutral 0.31 mm. By the datasheet, Fig. 13's ring starts at R 0.58 round a R 0.40 hole: **0.18 mm**. Published limits: JLCPCB "NPTH to track 0.2 mm"; PCBWay and Lion Circuits publish no NPTH-to-copper figure. The fab-neutral 0.31 mm came from Lion's 12 mil via-to-trace rule. The ring is the solder seal between the board and the mic's own port ring (R 0.6–1.0). A leak there opens the port to the air inside the body. Options: (C1) keep the datasheet ring, with a DRC exception for MK1's own hole, and confirm at each fab's DFM; (C2) pull the ring's inner edge to R 0.63 (0.23 mm, clear of JLCPCB's 0.2); (C3) pull it to R 0.71 (0.31 mm, fab-neutral); (C4) plate the hole, which risks solder wicking into it and narrowing the port.

**Decided: C2** (builder, 2026-10-26; [D-066](../../decisions.md#d-066) amended). The project footprint's ring is R 0.63–1.04: a 0.835 mm-radius circle 0.41 mm wide, with the pad anchor moved onto it. The seal still overlaps 0.37 mm of the mic's 0.40 mm port ring (R 0.6–1.0). The stencil's six ring apertures are unchanged. Rule `PCB-06 MK1 sound hole to its own seal ring` gives MK1's own hole 0.2 mm in place of the fab-neutral 0.31 mm, and nothing else. Re-run on the scratch copy: the ring measures 0.235 mm and passes; with the rule tightened to 0.3 mm it is flagged, so the rule is live. PCBWay and Lion Circuits publish no NPTH-to-copper limit, so confirm it in their DFM checks.

**Placement** (2026-10-27, through KiPy, one functional group at a time). KiCad coordinates, mm:

| Part | Position, rotation | Notes |
|---|---|---|
| MK1 | (105.32, 107.0), 0° | Its sound hole lands on the port, (106.0, 107.0); the package extends toward the post side, as in the CAD. Pins: 1 MIC_DATA (103.82, 106.15), 2 +3V3 (104.52, 106.15), 3 CLK (103.82, 107.85), 4 LR (104.52, 107.85), 5 GND ring round the port |
| H1, H2 | (106, 102), (106, 112) | The M2 holes, ±5 mm from the port on its axis |
| C2 100 nF, C1 1 µF | (103.6, 104.6) 180°, (102.8, 103.6) 180° | Just above the mic's pins, their +3V3 pads toward VDD: C2 is about 1 mm of track from pin 2. They fit between MK1's courtyard and H1's (C1 clears H1's by 0.11 mm) |
| R1 100 Ω | (101.6, 107.0), 90° | Post side, beside pin 1: MIC_DATA at the top pad, DATA at the bottom |
| R2, R3 (L/R strap) | (108.6, 108.2) 0°, (108.6, 109.2) 180° | Between the mic and the pads. Their LR pads face each other and share one stub |
| P1–P4 | x 110.6 at y 103.7 / 105.9 / 108.1 / 110.3, 90° | +3V3, CLK, GND, DATA: the W27 GH order, lying along the lead direction (u 3.6–5.6). **2.2 mm pitch**, so a via fits in each gap. The four wires fan out to v ±3.3 from the CAD's v ±2 reserve, all on the board |

**Why the pads are 2.2 mm apart.** No via may sit within 3.835 mm of the port: the Ø7.0 rule area plus the via's own radius. The mic's pins are 2.3 mm from the port, so every net leaves the mic on F.Cu. Each pin row then has a forced order: the pin nearer the port must take the inner track (VDD on the top row, LR on the bottom). At a 1.4 mm pitch nothing fits between the pads, so the two middle pads could be reached only from the left on F.Cu, where CLK and GND would cross. At 2.2 mm each gap takes a 0.67 mm via with 0.315 mm clearance either side, and any pad can be fed from B.Cu.

**Routing** (by hand through KiPy, no autorouter). Every track is 0.2 mm (the mic draws about 1 mA), and every segment is horizontal, vertical or 45°.

| Net | Route |
|---|---|
| +3V3 | Pin 2 up to C2, then C1. Along the top band (y 105.04, under H1) and up 45° into P1. Via in the P1/P2 gap (111.0, 104.8), straight down B.Cu to a via in the P3/P4 gap (111.0, 109.2), then F.Cu to R3 |
| GND | C1, C2 to a via on the post side (101.7, 104.4). From the seal ring's anchor (106.0, 106.165) round to R2 and P3, and a via in the P2/P3 gap (110.0, 107.0). The B.Cu pour `GND_OUTER_FACE` joins both vias and covers the whole outer face |
| MIC_DATA → DATA | Pin 1 left to R1. R1 down the post side and along the bottom (y 110.4, between the ring and H2) into P4 |
| LR | Pin 4 down, along under the mic (y 108.75) to the R2/R3 stub |
| CLK | Pin 3 left to a via (102.6, 108.9), 3.9 mm from the port. On B.Cu up the post side and across the top at y 103.6, between H1's hole and the gasket's outer edge. Via in the P1/P2 gap (109.9, 104.8), then down into P2 |

**Outer face.** B.Cu is the GND pour plus two tracks: CLK across the top and +3V3 down the pad column. The pour keeps 0.31 mm from the sound hole, so a bare Ø1.42 mm ring surrounds the hole, inside the gasket's Ø2.0 bore. The gasket's contact ring (Ø2.0–6.5) lands on plain poured copper under mask. The edge of the CLK track's 0.2 mm clearance channel reaches 0.15 mm inside the gasket's outer edge, at the top only. That is a 35 µm step under foam compressed 0.3 mm, which is negligible.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, 2026-10-27): **0 errors, 0 unconnected pads, 0 schematic-parity issues.** No keep-out, courtyard or clearance hits. Four warnings remain, `lib_footprint_mismatch` on C1, C2, R1 and R3. They are the cosmetic kind PCB-15 and PCB-11 found: only the rotated parts are flagged, and R2 (0°) is not. `audit()`: MK1 and the five 0402s each have their 3D model; P1–P4 and H1/H2 are out of the BOM and the position file (set again after F8). Reference labels moved to the fab layers (`refs_to_fab()`).

## Checks and outputs (rev A)

- **ERC** 0 errors, 0 warnings. **DRC** with schematic parity: 0 errors, 0 unconnected, and the 4 cosmetic warnings above. **`audit()`**: MK1 and the five 0402s have their 3D models. P1–P4 and H1/H2 are out of the BOM and the position file.
- **Board STEP:** [`cad/pcb-06-pdm-mic-revA.step`](cad/pcb-06-pdm-mic-revA.step). It lists the board, MK1 (Infineon's package model) and the five 0402s. The board core runs Z 0–0.91; the parts sit 0.04 mm above the front mask. The sound hole and both screw holes are open in the solid.
- **Outputs:** [`fab/revA/`](fab/revA/README.md) holds Gerber X2 and Excellon drill, both from the board-local origin, and one Gerber set with **two assembly variants**: L (R2 fitted) and R (R3 fitted), each with its own BOM and placement files in KiCad and JLCPCB CPL formats. It also holds a Gerber zip and the order parameters. The set has no silkscreen; the fitted strap resistor identifies the variant.
- **Fit in the robot:** [`final/v1/cad/check_pcb06_fit.py`](../../final/v1/cad/check_pcb06_fit.py) places the STEP on all four bosses: FRONT_R and REAR_L upright, FRONT_L and REAR_R turned over, the lead side toward the body centre each time. It measures against the body CAD, the chassis reference, and the shell's 0–125 mm lowering path (about 8 min). **PASS at all four:**

  | Check | Result (same at all four positions) |
  |---|---|
  | Outline and holes | Core matches the CAD placeholder's 12 × 14 outline to 0.01 mm. The sound hole is open on the port axis and both screw holes on the pilots |
  | MK1 | Package centre on the CAD package (offset 0.000, 0.000), i.e. its port on the port axis |
  | Seat | Core 0.045 mm from the boss, exactly the outer copper and mask; no clash |
  | Static | Nearest part to anything: R1 0.97 mm to the frame post; C1/C2 1.04 mm to the shell. The core's 0.04–0.05 mm to the boss and screw heads is the copper and mask |
  | Lowering path | Every part passes the upper side rail at n 2.30. With datasheet maximum heights (MK1 1.30 + 0.04, 0402s 0.55 + 0.04, wire joints 1.0), the worst is **MK1, 0.96 mm** |

  `check_mic_mounts.py` (D-037) is unchanged by this board: the board keeps the placeholder's outline, holes, mic position and height.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-26:** design started (lesson 1). Inputs measured: the IM73D122 datasheet against D-037, BOM and CAD; the four boards in the body CAD, static and along the shell's lowering path. Found: audiosystem.md predates D-037 (header, 12 × 9.5); the datasheet asks for 1 µF + 100 nF and about 100 Ω on DATA; element14 India's stock is in the UK, and JLCPCB now stocks C5563886; the frame post leaves 1.3 mm over the board's post-side strip; FRONT_R/REAR_L mount the other way up from FRONT_L/REAR_R, so the layout must fit the envelope folded about the port axis. No envelope change needed. Open: strap method (A), mic source (B).
- **2026-10-26:** [D-066](../../decisions.md#d-066) taken: strap by assembly variant (R_L/R_R 1 kΩ, one fitted), mic bought from element14 India and supplied to the fab. BO-005, BO-012 and the body BOM updated; audiosystem.md brought in line with D-037. Inputs frozen.
- **2026-10-26:** lesson 2. Schematic drawn for the KiCad 10.99 nightly: MK1, C1, C2, R1, R2/R3 (L/R variants), P1–P4 and H1/H2. Project symbol (IM69D120 body, pin 4 LR) and footprint (PG-LLGA-5-1 land pattern, pads widened to Fig. 13's 0.75 mm, Infineon STEP). W27 pin order set: 1 +3V3, 2 CLK, 3 GND, 4 DATA. ERC 0 errors, 0 warnings; the netlist matches the spec row by row.
- **2026-10-26:** lesson 3. Board set up: 12 × 14 outline, 1.0 mm stackup, origins at board-local (0, 0), envelope rule areas (post strip, outer face, gasket vias) and the wire-pad clearance rule, all proven on a scratch copy. Found: Infineon's sound-hole GND ring is 0.18 mm from the Ø0.8 NPTH, under JLCPCB's 0.2 mm and the fab-neutral 0.31 mm. Decision open.
- **2026-10-26:** decision C2: MK1's seal ring pulled back to R 0.63 (0.23 mm from the hole), with a scoped 0.2 mm hole-clearance rule for MK1 alone; [D-066](../../decisions.md#d-066) amended. Re-proved on the scratch copy.
- **2026-10-27:** lesson 4. Placed and routed by hand through KiPy on the nightly. The no-via circle round the port forces every net out of the mic on F.Cu, so the W27 pads went to a 2.2 mm pitch to take a via in each gap. Five vias, 0.2 mm octolinear tracks, B.Cu GND pour over the outer face. DRC 0 errors, 0 unconnected, parity clean; 4 cosmetic `lib_footprint_mismatch` warnings. Position-file flags set again after F8.
- **2026-10-27:** lesson 5. Board STEP exported with parts; new fit check `final/v1/cad/check_pcb06_fit.py` PASS at all four positions (MK1 0.96 mm under the upper rail on the way down, seat 0.045 mm, holes on the port and pilots). Rev A outputs in `fab/revA/`: one origin, two assembly variants, no silkscreen. Stage 1 done.
