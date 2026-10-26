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
| 1. Design | In progress: inputs frozen 2026-10-26 ([D-066](../../decisions.md#d-066)); schematic next | — | 2026-10-26 |
| 2. Procure | — | — | — |
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
| P1–P4 | Wire pads for the W27 lead, inner face | +3V3, GND, CLK, DATA (order set in the schematic) |

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

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-26:** design started (lesson 1). Inputs measured: the IM73D122 datasheet against D-037, BOM and CAD; the four boards in the body CAD, static and along the shell's lowering path. Found: audiosystem.md predates D-037 (header, 12 × 9.5); the datasheet asks for 1 µF + 100 nF and about 100 Ω on DATA; element14 India's stock is in the UK, and JLCPCB now stocks C5563886; the frame post leaves 1.3 mm over the board's post-side strip; FRONT_R/REAR_L mount the other way up from FRONT_L/REAR_R, so the layout must fit the envelope folded about the port axis. No envelope change needed. Open: strap method (A), mic source (B).
- **2026-10-26:** [D-066](../../decisions.md#d-066) taken: strap by assembly variant (R_L/R_R 1 kΩ, one fitted), mic bought from element14 India and supplied to the fab. BO-005, BO-012 and the body BOM updated; audiosystem.md brought in line with D-037. Inputs frozen.
