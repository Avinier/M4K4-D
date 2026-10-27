# Body v1 audio system

Started 2026-10-03. This file collects the body v1 audio system as one picture. Sections 1–6 cover the **custom PCBs**: what each board does in the audio chain, how the boards connect, and how they will be made. Section 7 covers the parts and the alternatives that were rejected, section 8 covers the speaker, cavity and mic placement with the acoustic open items, and section 9 covers finding the direction of a voice with the mic array. Software and bench results will be added later.

This is a working write-up, **not a fabrication release**. No schematic, layout or Gerber exists yet for any board below.

| Source | What it holds |
|---|---|
| [Body v1 BOM](../BOM.md), project [BOM.csv](../../../BOM.csv) rows BO-001…BO-007 | Part IDs and states |
| [D-034](../../../decisions.md#d-034), [D-035](../../../decisions.md#d-035) | Speaker locked; bench amplifier breakout selected |
| [Peripheral selection](../../../../02-prototypes/RP-06-cad/peripheral-selection.md) §2 | Design basis for the audio chain (read-only reference) |
| [Connector schedule](../../../../02-prototypes/RP-06-cad/connector-schedule.md) §3.2, W12/W26–W28 | Cable IDs, connectors and conductors (read-only reference) |
| [RP-02 board specs](../../../../02-prototypes/RP-02-electrical/board-specs.md) §6.5 | The `PB-AUDIO-OUT` power branch (read-only reference) |
| [`body_v1_model.py`](../cad/body_v1_model.py) | Board outlines, header positions and placement (`body_audio()`, `_pcb05_connectors()`, `_c0_link_adapter()`) |

Evidence tags follow the project: `D` datasheet or vendor page, `E` estimate or recommendation, `U` unknown until measured or checked.

---

## 1. Custom PCBs in the audio system

### 1.1 The boards at a glance

Four custom boards touch audio. Two are audio-only (PCB-05, PCB-06). Two are shared boards that each carry one audio function (PCB-04 for power, PCB-09 for the Pi's signals).

| Board | BOM | Audio role | Size (mm) | Where it sits |
|---|---|---|---|---|
| **PCB-05** audio front end | BO-002 | The audio hub. Converts mic PDM to I²S (2 × ADAU7002), amplifies the speaker (MAX98357A), filters the mic 3.3 V, and is the connection point for every audio cable | 30 × 38 × 1.6, parts to 9 total | Flat above the Pi 5's front end, centre (60, 0, 118.5): X 45–75, Y ±19, Z 114–123 |
| **PCB-06** mic board, × 4 | BO-005 | Holds one IM73D122V01 mic over a sound hole, sets the mic's L/R channel with a strap (L and R assembly variants, [D-066](../../../decisions.md#d-066)), and brings it out on a soldered GH 4 lead ([D-037](../../../decisions.md#d-037)) | 12 × 14 × 1.0 | On printed bosses on the shell's inner skin, outer face on \|Y\| 71.3 ([D-037](../../../decisions.md#d-037)). FRONT_L/R at X 54, Z 118; REAR_L/R at X −22, Z 108 |
| **PCB-09** C0 link adapter | none yet | Breaks the Pi's I²S pins and 3.3 V out of the 2 × 20 header to the GH 10 `J9-3`. Its main job is the two RS-422 links (2 × THVD1451) | Strip + wide part, about X 26–56, Y 28.5–45, Z 104–112 | Stacked on the Pi 5 header beside the yaw servo |
| **PCB-04** branch converters | CH-043 | Supplies the amplifier's 5 V `PB-AUDIO-OUT` branch (TPS630701 converter behind a TPS259474L e-fuse at 2.0 A) on `J4-5` | 70 × 44 | Under the compute tray, X −30…40, Z 60–77 |

The speaker (BO-001) is a bought part, not a board. It connects to PCB-05 by a soldered lead.

### 1.2 How they connect

```text
                Pi 5 2×20 header
                      │ (stacked socket)
              ┌───────▼────────┐
              │ PCB-09 C0 link │  GPIO18 BCLK, GPIO19 LRCLK, GPIO20 SDI0,
              │    adapter     │  GPIO22 SDI1, GPIO21 SDO0, GPIO23 AMP_SD,
              └───────┬────────┘  Pi 3V3, GND  (straight pass-through)
                J9-3  │ W26  GH 10
                      │
 PCB-04 J4-5 ──W12──► J5-7          J5-1 ◄─┘
 5 V PB-AUDIO-OUT  ┌──────────────────────────────────────┐
 Micro-Fit 3.0 2×1 │ PCB-05 audio front end               │
                   │  3V3 filter ─► mics + ADAU7002s      │
                   │  ADAU7002 #1 ◄─ PDM ◄─ front pair    │──► SDI0
                   │  ADAU7002 #2 ◄─ PDM ◄─ rear pair     │──► SDI1
                   │  SDO0 ─► 100 Ω ─► MAX98357A ─────────│──► J5-6 ─W28─► K 50 WP speaker
                   └───┬──────┬──────────┬──────┬─────────┘
                    J5-2   J5-3       J5-4   J5-5     W27 × 4, GH 4
                      │      │          │      │      (3V3, GND, CLK, DATA)
                   PCB-06 PCB-06     PCB-06 PCB-06
                   (+Y side mics)    (−Y side mics)
```

All converters run from the one Pi i2s0 clock (48 kHz, BCLK 3.072 MHz), so mic capture and speaker playback stay sample-aligned. That is what lets playback serve as the echo reference.

### 1.3 Cables between the boards

| Cable | From → to | Connector, each end | Conductors | Length (`E`, from CAD positions) |
|---|---|---|---|---|
| **W26** audio host | PCB-09 `J9-3` → PCB-05 `J5-1` | GH 10: top entry on PCB-09 (at X 37, Y 36.5); side entry on PCB-05's rear (−X) edge | BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, 3V3, 2 × GND, spare | ~60 mm |
| **W27** mics × 4 | PCB-06 → PCB-05 `J5-2…5` | Soldered to pads at PCB-06 ([D-037](../../../decisions.md#d-037)); GH 4 at PCB-05, side entry on its ±Y edges | 3V3, GND, CLK, DATA, AWG28. `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R ([D-067](../../../decisions.md#d-067)) | About 150 mm front, 200 mm rear, so they plug in through the front service opening after the shell is lowered ([D-037](../../../decisions.md#d-037)) |
| **W28** speaker | K 50 WP solder tabs → PCB-05 `J5-6` | Soldered at the speaker; GH 2 on PCB-05's +Y edge | 2 × AWG26, twisted | Under 150 mm (EMI limit) |
| **W12** amp power | PCB-04 `J4-5` → PCB-05 `J5-7` | Micro-Fit 3.0 2×1 right-angle, both ends; `J5-7` on PCB-05's −Y edge | 5 V, GND; 2 × AWG22 | ~120 mm |

Pin order inside each connector is set by the board schematics. **W27** is set by [PCB-06's schematic](../../../04-pcbs/pcb-06-pdm-mic/README.md#schematic): GH pin 1 3V3, 2 CLK, 3 GND, 4 DATA, with GND between the clock and the data line. PCB-05's `J5-2…5` use the same order. The [PCB-05 schematic](../../../04-pcbs/pcb-05-audio-front-end/README.md#schematic) sets the rest: **W26** (`J5-1`, `J9-3` wired 1:1) 1 3V3, 2 GND, 3 BCLK, 4 GND, 5 LRCLK, 6 SDO0, 7 SDI0, 8 SDI1, 9 AMP_SD, 10 spare (5V_SENSE); **W28** (`J5-6`) 1 SPK+, 2 SPK−; **W12** (`J5-7`) 1 +5 V, 2 GND, which PCB-04's `J4-5` must match.

Crimp tools: GH needs its own tool (terminal `SSHL-002T-P0.2`), and Micro-Fit 3.0 needs another.

---

## 2. PCB-05 audio front end

### 2.1 What is on it

| Block | Parts | Function |
|---|---|---|
| Mic converters | 2 × ADAU7002ACBZ-R7 (BO-004), 8-ball WLCSP | Each takes one mic pair on one PDM data line, clocks the pair at 64 × fs (3.072 MHz at 48 kHz) from BCLK, and outputs one stereo I²S lane. No registers, no I²C (`D`) |
| Amplifier | MAX98357AETE+T (BO-003), TQFN-16 | I²S in, filterless class-D out, 1.75 W into 8 Ω at 5 V (`D`) |
| Amp enable | 100 kΩ pull-down on `SD_MODE` (the chip has its own 100 kΩ too), **2.2 kΩ in series from `AMP_SD`** ([D-067](../../../decisions.md#d-067)) | Amp **off by default**. The Pi raises `AMP_SD` (GPIO23) to turn it on; about 2.9 V on `SD_MODE` selects the left channel. `SD_MODE` is rated only to VDD + 0.3 V, so with the 5 V branch off (CHARGE) the 2.2 kΩ limits its current to about 1.2 mA, the datasheet's remedy. No power-good signal is needed (§4.2) |
| Amp input damping | 100 Ω series resistors on BCLK, LRCLK and DIN at the amp | Edge damping. They are not needed as protection: the datasheet rates DIN, BCLK and LRCLK to 6 V whatever VDD is, so the Pi can stream while the amp's 5 V branch is off ([D-067](../../../decisions.md#d-067)) |
| Mic supply | Ferrite bead (600 Ω at 100 MHz) + 2.2 Ω + 10 µF from the Pi 3V3 on W26, 100 nF at each ADAU7002 and mic connector ([D-067](../../../decisions.md#d-067)) | Feeds the four mics and both ADAU7002s (about 9 mA). Passive, so never above the Pi's 3V3 and the parts' 3.6 V limit; the 2.2 Ω damps the bead/capacitor resonance near 34 kHz. Because it comes from the Pi, the front end is off whenever the Pi is off and cannot back-power its GPIO |
| Connectors | `J5-1` GH 10, `J5-2…5` GH 4, `J5-6` GH 2, `J5-7` Micro-Fit 3.0 2×1 | See the edge layout below |

### 2.2 How the four mics share two converters

A PDM data line can carry two mics. One mic drives the line on the rising clock edge and the other on the falling edge. The strap on each PCB-06 (LR to GND or to VDD) picks the edge, so it sets which I²S channel the mic lands on. The strap is set by the board's assembly variant, L or R ([D-066](../../../decisions.md#d-066)).

| Mic | LR strap | ADAU7002 | Pi lane | ALSA channel |
|---|---|---|---|---|
| FRONT_L | GND | #1 | SDI0 (GPIO20), left | 0 |
| FRONT_R | VDD | #1 | SDI0 (GPIO20), right | 1 |
| REAR_L | GND | #2 | SDI1 (GPIO22), left | 2 |
| REAR_R | VDD | #2 | SDI1 (GPIO22), right | 3 |

On PCB-05, the DATA pins of a pair's two GH 4 headers are tied into that ADAU7002's PDM data input, and its PDM clock output fans out to both CLK pins. The lane order and the edge convention are confirmed by a tap test on the bench before any array processing (`U`).

### 2.3 Edge layout (as modelled)

| Edge | Connectors, X start (mm) | Faces |
|---|---|---|
| Rear (X 45) | `J5-1` GH 10, centred on Y 0 | −X, towards PCB-09 |
| +Y (Y 19) | `J5-2` GH 4 (X 46), `J5-3` GH 4 (X 55.25), `J5-6` GH 2 (X 64.5) | +Y |
| −Y (Y −19) | `J5-4` GH 4 (X 46), `J5-5` GH 4 (X 55.25), `J5-7` Micro-Fit 3.0 (X 64.5–74.8) | −Y |

Mic to header ([D-067](../../../decisions.md#d-067)): **`J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R.** The +Y edge takes the L mics, which sit at +Y, and the −Y edge the R mics ([D-037](../../../decisions.md#d-037)), so no mic cable crosses over the board. Along each edge the rear header takes the rear lead, which arrives from behind. ADAU7002 #2 (rear pair, SDI1) sits between `J5-2` and `J5-4`, and #1 (front pair, SDI0) between `J5-3` and `J5-5`; each one's PDM traces cross the board once.

### 2.4 Layout notes (`E`, recommendations for the schematic and layout)

- **Layers:** two, 1.6 mm, with a near-solid ground plane on the bottom, which carries no parts ([D-067](../../../decisions.md#d-067)). Every ADAU7002 ball is on the outside of its 2 × 4 array, so it fans out on the surface. The fab-neutral rules are 2-layer rules.
- **Amplifier:** ground the exposed pad with thermal vias. Put 10 µF + 0.1 µF right at VDD, close to `J5-7`. Keep the OUTP/OUTN pair short to `J5-6`.
- **EMI:** leave unpopulated footprints for a ferrite bead + capacitor on each speaker output. Fit them only if the camera or radios pick up noise (the peripheral selection's rule).
- **Gain:** the MAX98357A's `GAIN_SLOT` pin sets 3–15 dB by strapping. Open is 9 dB. Choose the value after the bench listen on BO-007 (D-034 asks for a capped gain). Lay out a resistor footprint so any setting can be fitted.
- **Test points:** BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, both PDM clocks, 3V3 (before and after the filter), 5 V and GND.
- **Mounting** ([D-067](../../../decisions.md#d-067)): three M2 SMT spacers (Würth 9774080243R, 8 mm) on the top face, at (48.5, ±11.0) under the front upper cross and (63, 0) under the yaw plate, onto printed bosses on the frame. ISO 7380 M2 screws are driven from above after the compute tray and PCB-09, before the yaw cartridge. The board slides in from the front over the Pi's USB jacks (2.1 mm below), so it goes in after the compute tray, whose insertion passes 0.10 mm under it. CAD: `final/v1/cad` (`PCB05_MOUNT`, `check_pcb05_mount.py`).

---

## 3. PCB-06 mic board (× 4)

All four boards are **one design**. Only the LR strap changes per position.

| Item | Detail |
|---|---|
| Mic | Infineon IM73D122V01XTMA1: digital PDM, 73 dB(A) SNR, bottom port, 4 × 3 × 1.2 mm (`D`) |
| Sound path | Ø2.0 port through the skin and the shell boss → foam gasket ring → Ø0.8 mm hole through the PCB → the mic's bottom port ([D-037](../../../decisions.md#d-037)) |
| Board | 12 × 14 × 1.0 mm ([D-037](../../../decisions.md#d-037)). The mic and the lead pads sit on the inboard face, so the outer face stays flat on the boss seat and the gasket |
| Connector | None on the board. A pre-crimped JST GH 4-way AWG28 lead (W27) is soldered to four pads beside the mic: 3V3, GND, CLK, DATA ([D-037](../../../decisions.md#d-037), which dropped the SM04B header: it would hit the frame's upper side rails as the shell is lowered) |
| Strap | LR to GND (L mics) or VDD (R mics): two 1 kΩ 0402 footprints, and the fab fits one. L and R assembly variants of one board ([D-066](../../../decisions.md#d-066)) |
| Other parts | Decoupling and a DATA series resistor. The datasheet asks for 1 µF at VDD and recommends 100 nF, and suggests about 100 Ω on DATA. Values are set in the [PCB-06 schematic](../../../04-pcbs/pcb-06-pdm-mic/README.md#inputs) |
| Fixing | Two M2 × 4 thread-forming screws into the shell boss clamp the board on a foam gasket that seals the port ([D-037](../../../decisions.md#d-037)). All four boards are on the one shell print, so the array stays rigid |

**Layout notes (`E`):**
- Two layers are enough.
- Keep the sound hole clear of copper and solder mask as the Infineon land pattern specifies.
- MEMS mics must not be washed after reflow, and flux must stay out of the port. Ask for no-clean assembly and check JLCPCB's handling for bottom-port MEMS parts (`U`).

---

## 4. Audio functions on the shared boards

### 4.1 PCB-09 C0 link adapter

PCB-09 plugs onto the Pi 5's 2 × 20 header through a stacked socket. For audio it is only a pass-through: GPIO18–23, the Pi's 3.3 V and GND go straight to the GH 10 `J9-3`. It has no audio parts.

What audio needs from PCB-09's design:

- Route GPIO18–23 to `J9-3` without stubs or crossings next to the RS-422 lines.
- Carry the Pi's 3.3 V on one `J9-3` pin and two grounds on two others.
- Optional: a 22–33 Ω series resistor on BCLK near the Pi to tame the edges over the ~60 mm cable (`E`; decide at the bench).

PCB-09 is registered as CH-084 in [BOM.csv](../../../BOM.csv) ([D-038](../../../decisions.md#d-038)).

### 4.2 PCB-04 `PB-AUDIO-OUT` branch

| Item | Value |
|---|---|
| Converter | TPS630701 buck-boost to 5 V, provisional (RP-02 §6.5) |
| Protection | TPS259474L e-fuse, 2.0 A trip (1.80–2.20 A), latch-off |
| Enable | From the sequencing latch on PCB-02, AND-ed like the display and compute branches; off in CHARGE |
| Load | About 0.4 A average and 0.7 A peak at 1.75 W into 8 Ω; 2.4 mA idle (`E`/`D`) |
| Output | `J4-5`, Micro-Fit 3.0 2×1 on PCB-04's +Y edge → W12 |

The audio software was to raise `AMP_SD` only after this branch reports power-good, and no cable carried that signal to the Pi. **Closed by [D-067](../../../decisions.md#d-067): no power-good path.** The amp's data inputs tolerate the Pi streaming while the branch is off, and a 2.2 kΩ series resistor keeps `SD_MODE` within its rating (§2.1). PCB-05 carries an unfitted divider from its 5 V to the W26 spare pin, so a 5V-present signal can be added later without a new PCB-05.

---

## 5. How the boards will be made

### 5.1 Fabrication route

PCB-05 and PCB-06 are ordered as **assembled boards (PCBA) from JLCPCB**, on the same order as PCB-07 (base IMU) and PCB-08 (yaw junction).

- **PCB-05 can't be hand-built.** The ADAU7002 is an 8-ball WLCSP about 1.6 × 0.8 mm, and no Indian or stocked ADAU7002 breakout exists.
- **PCB-06 is assembled to match.** The IM73D122 is a reflow-only LGA part.

| Step | Output | Notes |
|---|---|---|
| 1. Schematics | PCB-05, PCB-06 (and PCB-09's audio pins) | Pin order for every connector is fixed here |
| 2. Layout | Board files on the CAD outlines | PCB-05 at 30 × 38 with the headers at the modelled positions (§2.3); PCB-06 at 12 × 14 × 1.0 |
| 3. Fit check | Export the board STEPs and run them in the body CAD | Replace the box envelopes in `body_v1_model.py` and re-run the targeted body checks |
| 4. DFM | JLCPCB design-rule and assembly checks | Check the WLCSP pitch and pad rules, and bottom-port MEMS handling, against JLCPCB's capability (`U`) |
| 5. Order | PCBA, PCB-05 to PCB-08 together | Order spares: at least 2 × PCB-05 and 6 × PCB-06 (`E`); JLCPCB minimum quantities apply (`U`) |
| 6. Bring-up | §5.3 | Results go in this file and in a decision |

### 5.2 Part sourcing for the order

| Part | Source | Unit (`E`, 2026-09-26 snapshot) |
|---|---|---|
| ADAU7002ACBZ-R7 × 2 per PCB-05 | LCSC C481886 (about 147 in stock) | US$4.10 |
| MAX98357AETE+T × 1 per PCB-05 | LCSC / JLCPCB | US$2–3 |
| IM73D122V01XTMA1 × 1 per PCB-06 | element14 India 4125831 on cut tape, bought by the builder and supplied to the fab ([D-066](../../../decisions.md#d-066)) | ₹305 (₹232 at 10+), 2026-10-26 |
| GH headers (SM10B, SM04B, SM02B), Micro-Fit 3.0 2×1 RA | LCSC / JLCPCB | — |
| Passives, ferrite | JLCPCB basic parts | — |

The whole PCBA order (PCB-05 to PCB-08, fab, setup, shipping, customs) was estimated at **₹4,000–7,000** (`E`). Get written quotes before ordering.

### 5.3 Bring-up order (`E`)

1. **Bare board:** check for shorts between 5 V, 3V3 and GND.
2. **Power:** 5 V on `J5-7` from a current-limited bench supply, and 3V3 on `J5-1`. Measure the idle current with `AMP_SD` low; it should be a few µA on 5 V.
3. **Playback:** stream silence, raise `AMP_SD`, then a tone. Listen for pops at enable and measure 5 V current at full output.
4. **One mic:** connect a single PCB-06 and run `arecord` on its lane.
5. **Full array:** all four mics. Tap each port and confirm the ALSA 0–3 order (§2.2).
6. **Duplex:** `arecord -c 4` and `aplay` together for one hour with no xruns. Check whether RP1's "symmetric channels" limit forces 4-channel playback.

### 5.4 What can be tested before the boards exist

- **Playback can.** The SmartElex MAX98357A breakout (BO-007, D-035) uses the same chip, wired BCLK → GPIO18, LRC → GPIO19, DIN → GPIO21, SD → GPIO23. Its SD pin is probably pulled up, so it's on at power-up, and it has no series resistors.
- **Capture can't.** The selected chain has no bench stand-in. The ADAU7002 has no stocked breakout, and Infineon's `KIT_IM73D122V01_FLEX` is out of stock (US$75). So the first four-mic test needs PCB-05 and PCB-06. To prove two-lane capture earlier, a pair of any I²S MEMS mic breakouts on GPIO20/GPIO22 would exercise the Pi side (`E`, not selected).

---

## 6. Open items for the PCBs

1. **5 V route:** closed, [D-067](../../../decisions.md#d-067): 5 V on W12 only. The GH 10 carries signals, 3V3 and grounds.
2. **Pins:** closed, [D-067](../../../decisions.md#d-067): `CA-06` CR-01 accepted, GPIO22 (I²S0 SDI1) and GPIO23 (`AMP_SD`).
3. **Power-good to the Pi:** closed, [D-067](../../../decisions.md#d-067): none needed (§4.2).
4. **Mic to header map:** closed, [D-067](../../../decisions.md#d-067) (§2.3).
5. **PCB-09 BOM row:** done, CH-084 in the shared rows (D-038).
6. **Mounting:** closed, [D-067](../../../decisions.md#d-067) for PCB-05 (§2.4); [D-037](../../../decisions.md#d-037) for PCB-06.
7. **Schematics and layouts:** PCB-05 started 2026-10-27, inputs frozen ([board README](../../../04-pcbs/pcb-05-audio-front-end/README.md)); PCB-06 started 2026-10-26 ([board README](../../../04-pcbs/pcb-06-pdm-mic/README.md)).
8. **Model comment:** done. The comment above `MIC_BOARD_OUTER_Y` in `body_v1_model.py` now describes the D-037 board.
9. **Mass:** replace the PCB-05 (~6 g) and mic-board (~2 g total) estimates in `BODY_AUDIO` with weighed boards.

---

## 7. Parts and alternatives

### 7.1 Selected parts

States are from [BOM.csv](../../../BOM.csv) as of 2026-10-03. Prices are the 2026-09-26/10-03 snapshots (`E`, not quotes).

| Role | Part | BOM | State | Qty | Key facts | Source | ≈ ₹ |
|---|---|---|---|---:|---|---|---|
| Speaker | Visaton K 50 WP – 8 Ω, art. 2915 | BO-001 | SELECTED (D-034) | 1 | Ø50 × 18 mm, Ø46 cutout, 48 g, 2 W rated / 3 W max, 84 dB (1 W/1 m), 180 Hz–17 kHz, fs 300 Hz, IP65 front when sealed (`D`) | element14 India 1683894 (price not read) | 600–1,500 |
| Amplifier | MAX98357AETE+T, TQFN-16 | BO-003 | CANDIDATE | 1 | I²S in, no MCLK, 2.5–5.5 V, 1.75 W into 8 Ω at 5 V, 2.4 mA idle, 0.6 µA shutdown, click/pop suppression (`D`) | LCSC/JLCPCB | 150–300 |
| Mic converter | ADAU7002ACBZ-R7, WLCSP-8 | BO-004 | CANDIDATE | 2 | Stereo PDM → I²S, no registers, 1.62–3.6 V (`D`) | LCSC C481886 | ~720 |
| Microphone | Infineon IM73D122V01XTMA1 | on BO-005 | HOLD (board) | 4 | PDM, 73 dB(A) SNR, −26 dBFS, 122 dB SPL AOP, ±1 dB matched, bottom port, IP57 (`D`) | DigiKey/Mouser cut tape, or JLCPCB | 600–1,000 |
| Bench amp | SmartElex MAX98357A breakout | BO-007 | SELECTED (D-035), bench only | 2 | Same chip as BO-003; SD probably pulled up (on at power-up) | Robocraze ₹195 | 390 |

Parts total ≈ ₹2,500–3,900, bench breakouts included, before the PCBA order (§5.2, ₹4,000–7,000 shared with PCB-07/08).

### 7.2 Alternatives and why they lost

| Candidate | Outcome |
|---|---|
| AC108, TLV320ADC3140, PCMD3140 (4-slot TDM codec) | Rejected. The Pi 5's RP1 I²S has no true TDM: one stereo pair per data line, so a 4-slot codec gives one live channel. Two lanes are needed anyway, and these add I²C setup and driver trouble |
| XMOS/XVF-class USB mic array | Rejected. Fixed ~65 mm capsule circle cannot reach the ports ±70 mm apart on the side walls, and separate USB playback splits the clock (no sample-aligned echo reference) |
| Infineon IM69D130 | Marked "not for new design" (2026-09) |
| Infineon IM69D128S / IM69D129F | Viable, same footprint and current, but 69 dB SNR; IM73D122 keeps 4 dB more for far-field wake |
| Visaton K 50 (2901, metal) | 250 Hz–10 kHz, fs 400–500 Hz, dearer. **Fallback** if 2915 is unavailable (D-034) |
| Visaton K 28 GI (2830) | 0.5 W, 450–7000 Hz: too quiet and thin, and the MAX98357A could overdrive it |
| Visaton FRS 5 X | 140 g against a 90 g audio row; its bass is wasted in a ~46 cm³ cavity |
| PUI AS05008MR-4-R | Ø50 × 7.5 mm, 8 Ω, 1.5 W. Kept as the **thin alternate** if the cavity must shrink |
| Local generic 50 mm 8 Ω (e.g. Robomart ₹174) | No datasheet; most are Ø52–55 × 25–45 mm, too big for the cup and cavity |

---

## 8. Speaker, cavity and mic placement

Body model coordinates, mm, from [`body_v1_model.py`](../cad/body_v1_model.py).

| Item | Placement |
|---|---|
| Speaker | Centre (90.5, 0, 99), axis +X, face at X 100 (`SPEAKER_FRONT_X`) |
| Front panel seat | Integral annular cup on the front service panel with an unobstructed Ø46 aperture. The exposed speaker face is recessed 2.6 mm behind the lip; its flange is bonded and sealed behind the lip across a modeled 0.8 mm annulus. The cup needs print supports |
| Back cavity | Ø54 speaker clearance reserve, X 82–97.5 (15.5 mm deep), shifted forward with the speaker to clear the compute tray and Pi 5; actual rear enclosure sealing remains to be verified |
| Mic ports | Ø2.0 bores through the shell bosses and the skin ([D-037](../../../decisions.md#d-037)). FRONT_L/R at (54, ±70, 118); REAR_L/R at (−22, ±70, 108) |
| Mic boards | PCB-06 outer face on \|Y\| 71.3 on its shell boss, sealed by a gasket (§3, [D-037](../../../decisions.md#d-037)). Front pair is 41 mm behind the speaker face along X and ±70 mm off the centreline |
| Mass row | `BODY_AUDIO` 61 g at (78.4, 0, 102.1): speaker 48, PCB-05 ~6, mic boards ~2, cables ~4 (`E`) |

**Capture rate:** 48 kHz, decimated to 16 kHz in software where needed. At 48 kHz the ADAU7002 clocks the mics at 3.072 MHz, inside the IM73D122 high-performance window; at 16 kHz the 1.024 MHz clock falls between its power-mode windows (`D`).

**Acoustic trade-off:** the open front removes grille obstruction, while the short rear clearance reserve and unverified enclosure seal leave low-end response uncertain. Measure the assembled response before treating the nominal 300 Hz driver resonance as the installed resonance (RP-05 `AR-36`, `U`).

**Open acoustic items:**

1. Low-end response of the 15.5 mm cavity (bench listen at a capped gain, D-034).
2. Speaker-to-mic coupling, `AR-60`. Estimate about 110 dB SPL at 5 cm on axis at 1.75 W, under the mics' 122 dB AOP (`E`).
3. Pi 5 cooler noise at the mics, `AR-61`; drive and servo noise, `AR-62/63` (RP06-G03 acoustic matrix).
4. Exposed speaker flange bond, rear enclosure and panel-to-shell seal method; mic port gasket seal (tap test, D-037).
5. Caliper and weigh the received speaker against Ø50 × 18 mm and 48 g, then update `BODY_AUDIO`.

---

## 9. Finding where a voice comes from (sound source localisation)

The four body mics can tell the robot **which direction a voice is coming from**, as well as what was said. This gives Makad a second way to find a person besides the camera (computer vision). It still works when the person is behind or beside the robot, outside the camera's view, or in the dark. A typical use: hear a voice from behind-left, turn the body or head that way, then let the camera confirm the face.

This is direction of arrival (DOA): RP-05 `CAND-01` / `ADR-13`, a later software feature, not a Core requirement. The hardware chosen here already supports it, so no part or board changes are needed.

### 9.1 Two cues: loudness and timing

| Cue | What it measures | How much it tells us on this body |
|---|---|---|
| **Loudness (level difference)** | The mic nearer the speaker hears the voice slightly louder, and the body casts an acoustic "shadow" on the far side at higher frequencies | Coarse. With mics 140 mm apart, the distance difference alone is about 1 dB at 1 m and 0.6 dB at 2 m (`E`). That's smaller than the normal mismatch between mics and the effect of echoes in a room. Enough for "left or right, front or back", not for an angle |
| **Timing (time difference of arrival, TDOA)** | Sound travels at about 343 m/s, so it reaches the nearer mic a fraction of a millisecond earlier | Precise. This is the main cue. Across the 140 mm left–right spacing the largest delay is 408 µs (≈ 20 samples at 48 kHz); across the 76 mm front–rear spacing it is 222 µs (≈ 11 samples) (`E`, from the CAD port positions) |

The plan is to **estimate direction from timing and use loudness as a supporting check**: for example, to pick the right answer when the timing result is ambiguous, or to reject a bearing that loudness contradicts.

### 9.2 Why this hardware can do it

- **One clock for all four mics** (§1.2, `AR-03`, `AR-51`): all four channels are sampled at exactly the same moments, so a delay of a few samples between them is real, not drift between separate devices. A USB array plus a separate mic, or four separate gadgets, couldn't guarantee this.
- **Four mics in a rectangle, not a line** (`AR-04`): the ports at (54, ±70) and (−22, ±70) form a 140 × 76 mm rectangle. Two mics alone can't tell front from back; this layout gives a full 360° direction around the robot.
- **Rigid mounting** (`AR-64`): the mic boards are screwed to bosses on the one shell print (D-037), so the spacing that the maths assumes doesn't change.
- **Echo reference** (§1.2): because the speaker shares the same clock, the robot's own voice can be subtracted before localising, so it doesn't "find itself".

### 9.3 Limits to expect

| Limit | Why | Status |
|---|---|---|
| Direction around the robot only, not height | The front and rear pairs differ by only 10 mm in Z | Hardware fact |
| Accuracy: a few degrees in theory, worse indoors | Room echoes, several speakers at once and background noise blur the timing peak. Typical results for small arrays are on the order of 10–20° indoors | `U` until bench-measured |
| Unreliable while driving | Motor, wheel and servo noise reach the mics (`AR-62`, `AR-63`); the bearing should be gated (marked unreliable) during motion, not silently trusted | `AR-63` |
| Cooler and speaker noise | The Pi 5 cooler (`AR-61`) and the robot's own playback (`AR-60`) | §8 open items 2–3 |

### 9.4 Software (later)

- **Method:** GCC-PHAT on each mic pair, or SRP-PHAT over all four mics, on the 48 kHz capture. This is standard and works on the Pi 5 CPU. Libraries such as `pyroomacoustics` or ODAS provide both.
- **Output:** a bearing angle with a confidence value, published for the behaviour layer.
- **With vision:** audio gives "turn towards ~135°", the camera then finds and tracks the face. Each covers the other's blind spots: audio sees behind, vision gives the exact position.

### 9.5 Bench test (once PCB-05/06 exist)

1. Tap each port in turn to confirm the channel map (bring-up step 5, §5.3).
2. Play speech from a phone at 1 m and 2 m, every 30° around the robot, in a quiet room and a normal room. Log the estimated bearing against the true one.
3. Repeat with the cooler running and with the robot speaking, to check the echo subtraction.
