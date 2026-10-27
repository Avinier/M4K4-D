# PCB-05 — Audio front end

MAX98357A speaker amplifier and 2 × ADAU7002 PDM-to-I²S converters for the mic array.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-002 in [BOM.csv](../../BOM.csv) |
| Location | Body, above the Pi |
| Specification | [audiosystem.md §2](../../02-body/v1/research/audiosystem.md#2-pcb-05-audio-front-end), [§5](../../02-body/v1/research/audiosystem.md#5-how-the-boards-will-be-made), [§6](../../02-body/v1/research/audiosystem.md#6-open-items-for-the-pcbs) |
| CAD placeholder | `body_audio()` and `_pcb05_connectors()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `PCB05_AUDIO_FRONT_END`, `PCB05_CONNECTORS` |
| Final CAD | `Custom PCBs › PCB-05 audio front end` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | In progress: inputs frozen ([D-067](../../decisions.md#d-067)); schematic next | — | 2026-10-27 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Frozen 2026-10-27 with [D-067](../../decisions.md#d-067). The builder took the recommended option of each decision A–G the same day (*Decisions*, below).

**Spec sources.** [audiosystem.md §1.2–1.3, §2, §5, §6](../../02-body/v1/research/audiosystem.md#2-pcb-05-audio-front-end); [D-036](../../decisions.md#d-036) (mic part), [D-037](../../decisions.md#d-037) (mic leads: +Y boards to `J5-2`/`J5-3`, −Y boards to `J5-4`/`J5-5`), [D-066](../../decisions.md#d-066) (L/R straps); BOM row BO-002, with BO-003 (amp), BO-004 (converter), BO-006 (W26/W27/W28/W12); [PCB-06 README](../pcb-06-pdm-mic/README.md#inputs) (*Interface*, *Strap per position*, *Clock and data over the lead*); RP-06 [peripheral selection](../../../02-prototypes/RP-06-cad/peripheral-selection.md) §2.5–2.6 and RP-02 `CA-06` (read-only). CAD: `body_audio()`, `_pcb05_connectors()` and the `PCB05_*` reserves in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py).

**Datasheets** (all read 2026-10-27):

| Part | Document | Used for |
|---|---|---|
| ADAU7002 | [ADI Rev. C](https://www.analog.com/media/en/technical-documentation/data-sheets/ADAU7002.pdf) (11/2019, the current revision) | Fig. 2/Table 4 pins, Fig. 11 application circuit, Fig. 12 and Table 5 PDM timing, Table 6 CONFIG, Fig. 22 package |
| MAX98357A | [ADI Rev 16](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf) (2/26). Revs 8–16 changed specs, startup and ordering text only; pins and ratings match Rev 7 | Pin description, absolute maximum ratings, Table 5 SD_MODE, Table 8 gain, startup, layout and grounding, package 21-0136 (T1633+4) |
| IM73D122V01 | [Infineon v1.00](https://www.infineon.com/assets/row/public/documents/24/49/infineon-im73d122-datasheet-en.pdf) | Table 6 timing (tDD, tHZ, tDV), Table 8 L/R, clock rise and duty |
| RP1 | [RP1 peripherals](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf) | GPIO function table (CR-01) |

ADI's PDFs time out with a plain `curl`. They download with a full Safari header set (`User-Agent`, `Accept`, `Accept-Language`, `Sec-Fetch-*`, `Upgrade-Insecure-Requests`).

**Circuit** (from the spec, with the datasheet corrections marked; final values at the schematic):

| Block | Parts | Pins and nets |
|---|---|---|
| U1, U2 ADAU7002ACBZ-R7 (BO-004), WLCSP-8 | One per mic pair: U1 front pair → SDI0, U2 rear pair → SDI1 | A1 PDM_DAT ← both mics' DATA; A2 PDM_CLK → both mics' CLK; B1 SDATA → SDI0 / SDI1; B2 BCLK, C2 LRCLK ← Pi; C1 GND; D1 IOVDD ← mic rail; D2 CONFIG → IOVDD (I²S, Table 6). 0.1 µF at IOVDD (Fig. 11) |
| U3 MAX98357AETE+T (BO-003), TQFN-16 3 × 3, EP | Mono amp, left channel | 1 DIN ← SDO0, 16 BCLK, 14 LRCLK (each through 100 Ω); 4 SD_MODE ← AMP_SD; 2 GAIN_SLOT → resistor footprint; 7, 8 VDD ← +5V_AMP; 3, 11, 15 GND; 9 OUTP, 10 OUTN → `J5-6`; 5, 6, 12, 13 NC; EP → GND plane (thermal only, "not internally connected"). 10 µF + 0.1 µF at VDD |
| SD_MODE network | 100 kΩ to GND (spec), **2.2 kΩ series from AMP_SD** (decision C) | Internal 100 kΩ pull-down too (`RPD` 92–108 kΩ). With both pull-downs (48 kΩ) and 2.2 kΩ, a 3.0 V GPIO high gives 2.87 V, above B2 (1.5 V max): left channel |
| Mic rail | FB1 600 Ω at 100 MHz (0603, DCR ≤ 0.5 Ω) + R 2.2 Ω + C 10 µF X5R from the Pi 3V3; 100 nF at each ADAU7002 IOVDD and each mic connector (decision F) | Feeds U1, U2 and the four mics through `J5-2…5` |
| EMI | Unfitted ferrite + capacitor footprints on OUTP and OUTN (§2.4) | Fit only if the camera or radios pick up noise |
| PDM clock | Series resistor per clock branch, at U1/U2 (new; value on the bench) | Four branches: each PDM_CLK feeds two leads |
| Test points | §2.4 list: BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, both PDM clocks, 3V3 before and after the filter, 5 V, GND | Top face |
| 5V-present divider | Unfitted resistor pair from +5V_AMP to the `J5-1` spare pin (about 5 V → 3 V) | Decision C: lets a later `CA-06` change bring the amp's supply state to the Pi without a new board |
| Fixings H1–H3 | Würth 9774080243R M2 SMT spacer, Ø4.35 × 8 mm, steel, MSL 1, reflowed on the top face | Decision E. Würth's land pattern and KiCad library (WA-SMSI) at board set-up |

**Pinout checks.**

- **ADAU7002** (Fig. 2, Table 4; top view, ball side down): A1 PDM_DAT, A2 PDM_CLK, B1 SDATA, B2 BCLK, C1 GND, C2 LRCLK, D1 IOVDD, D2 CONFIG. Package 1.56 × 0.76 × 0.50 mm (Fig. 22), balls Ø0.26 (0.22–0.30) at **0.40 mm pitch**, 2 × 4. ADI gives no land pattern. Every ball is on the outside of the array, so each net leaves on the surface with no via-in-pad. Pads must be ≤ 0.24 mm to keep the 0.16 mm copper gap. The 0.16 mm mask web cannot be held between them, so the WLCSP gets one shared mask opening (settle at board set-up). JLCPCB lists the part as "X-ray inspection required".
- **MAX98357A TQFN-16** (pin description, unchanged Rev 7 → Rev 16): 1 DIN, 2 GAIN_SLOT, 3 GND, 4 SD_MODE, 5 NC, 6 NC, 7 VDD, 8 VDD, 9 OUTP, 10 OUTN, 11 GND, 12 NC, 13 NC, 14 LRCLK, 15 GND, 16 BCLK, EP. Package T1633+4 (21-0136): 3.00 × 3.00 × 0.75 (max 0.80) mm, 0.50 mm pitch, leads 0.20–0.30 wide and 0.30–0.50 long, exposed pad 1.10 (0.95–1.25) square. Land pattern 90-0031 (analog.com/packages) to be read at the schematic. KiCad's stock `TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm` is the candidate.
- **Absolute maximum ratings that matter here.** DIN, BCLK and LRCLK are rated −0.3 to **+6 V to GND, whatever VDD is**, so the Pi can stream into an unpowered amp without back-powering it. **SD_MODE is not**: it is an "other pin", −0.3 to **VDD + 0.3 V**. The datasheet's remedy when VDDIO can exceed VDD (the Pi is up and the amp branch is off, as in CHARGE) is "a small resistance (~2 kΩ) in series with SD_MODE". At 3.3 V into an unpowered VDD that limits the pin to about 1.2 mA, under its 20 mA continuous input rating. The spec's 100 Ω resistors on BCLK/LRCLK/DIN were meant as back-power protection; they are not needed for that, but stay as edge damping on the clock lines.
- **Startup** (Rev 12 on): at BCLK 3.072 MHz the only rule is that LRCLK must start within half an LRCLK period of BCLK. The 256 kHz sequence does not apply. RP1 starts both together.

**PDM edge convention: checked, matches PCB-06.** ADAU7002 Fig. 12: the bit labelled **L** straddles the PDM_CLK **rising** edge (setup before it, hold after), and **R** straddles the falling edge. IM73D122 Table 8: LR = GND drives DATA after the **falling** edge and releases it after the rising edge, so its bit is valid while the clock is low and is latched on the next rising edge, as **L**. LR = VDD lands on the falling edge, as **R**. So the PCB-06 straps are right: FRONT_L and REAR_L (R_L, LR to GND) are left, FRONT_R and REAR_R (R_R, LR to 3V3) are right. The tap test still has to confirm how RP1 orders the two lanes in ALSA (§2.2).

**PDM timing over the leads** (IM73D122 Table 6 against ADAU7002 Table 5; clock 3.072 MHz, half period 162.8 ns, 156.3 ns at 48 % duty):

| Margin | Budget | Result |
|---|---|---|
| Setup (≥ 10 ns before the latching edge) | Clock out to the mic: 200 mm lead about 1.1 ns plus about 2.5 ns for the series resistor × lead capacitance. Mic tDV ≤ 100 ns. Data back: about 1.1 ns | 156.3 − 100 − 4.7 − 10 = **41 ns** spare |
| Hold (≥ 7 ns after it) | The mic releases DATA tHZ ≥ 5 ns after the edge reaches it, which is ≥ 3.6 ns after the ADAU7002 sent it; the change takes 1.1 ns to come back. After release, the line's capacitance holds the bit until the other mic drives it, tDD ≥ 40 ns | ≥ 9.7 ns, about 2.7 ns spare even counting only tHZ |
| Clock at the mic | Rise and fall ≤ 13 ns; duty 48–52 % above 3 MHz | Edge about 5 ns (2.2 × 100 Ω × 25 pF). **Duty is not in the ADAU7002 datasheet**; PDM_CLK follows the Pi's BCLK. A bench item (`U`), as PCB-06 gap 9 says |

**Interface.**

| Connector | Part | Edge, position (CAD) | Pins |
|---|---|---|---|
| `J5-1` host | JST GH SM10B-GHS-TB, side entry | Rear (−X), X 45–49.95, Y ±7.88 | BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, 3V3, 2 × GND, spare (5V-present, unfitted); **no 5 V** (W26 to PCB-09 `J9-3`). Order set in the schematic; PCB-09 told |
| `J5-2…5` mics | SM04B-GHS-TB, side entry | +Y: `J5-2` X 46–54.25, `J5-3` 55.25–63.5. −Y: `J5-4`, `J5-5` the same | **1 3V3, 2 CLK, 3 GND, 4 DATA** (fixed by the PCB-06 schematic). **`J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R** (decision D) |
| `J5-6` speaker | SM02B-GHS-TB, side entry | +Y, X 64.5–70.25 | OUTP, OUTN (W28, twisted, < 150 mm) |
| `J5-7` amp power | Molex Micro-Fit 3.0 43650-0200, 2 × 1 right angle, through hole | −Y, X 64.5–71.76, 10 mm deep (Y −19…−9) | +5V_AMP, GND (W12 from PCB-04 `J4-5`, `PB-AUDIO-OUT`) |

**Supply.**

| Rail | Source | Load | Notes |
|---|---|---|---|
| +5V_AMP | `PB-AUDIO-OUT` on W12: TPS630701 behind a TPS259474L e-fuse (2.0 A trip), off in CHARGE | 2.4 mA idle (Rev 16: 2.75 typ at 5 V), about 0.4 A average, 0.7 A peak at 1.75 W into 8 Ω | W12 only (decision A) |
| 3V3 (Pi) | Pi header 3.3 V on W26 | Feeds only the filter | Off whenever the Pi is off, so the front end can't back-drive GPIO20/22 |
| +3V3_MIC | Filtered Pi 3V3 (decision F; never above its input) | Mics 4 × 1.12 mA max; ADAU7002 2 × 1.33 mA typ (3.3 V); PDM clock charging about 2 × 0.4 mA. **About 9 mA; design for 15 mA** | ≤ 3.6 V: the IM73D122's abs max and the ADAU7002's IOVDD and input abs max |

**Envelope** (body v1 CAD, measured 2026-10-27 on the built `build_body_assembly()`, `chassis_v1_reference()` and the yaw drive; per-solid boxes for the vendor Pi and cooler, exact booleans for the frame and shell). The `final/v1/cad` droid edits don't touch this area. World mm.

| Face | What is there | Clearance |
|---|---|---|
| Board | 30 × 38 × 1.6, X 45–75, Y ±19, Z 114.0–115.6; top-face parts reserve to Z 123.0 | — |
| **Top**, rear band X 45.5–53.5 | Front upper cross rail (`BODY_FRAME_MAIN_PRINT`), underside Z 126.0 | **10.4 mm**; 3.0 above the 123 reserve |
| Top, X 55–70 | Yaw adapter plate underside, Z 134.0 | 18.4 mm |
| Top, X 65–75 | Shell roof, Z 137.6 | 22.0 mm |
| Top, `J5-7` | Micro-Fit block (CAD, 10 mm, to Z 125.6) under the yaw plate | 8.4 mm |
| **Bottom**, X 59.4–77.0, Y −12.0…21.7 | Pi 5 USB jack stacks, top Z 111.90 | **2.10 mm** |
| Bottom, Y −19…−15 | Pi 5 Ethernet jack (X 55.5–76.7), top 109.35 | 4.65 mm |
| Bottom, rear X 45–53.6 | Active Cooler plate (X ≤ 52.75) top 107.00; push-pin head (X 46.9–53.6, Y 11.0–16.8) top 108.05 | 7.0 / 5.95 mm |
| Bottom, blower | Ø28.6 rotor centred (31.8, −0.2), ends at X 46.1 | The board covers 1.1 mm of the inlet's edge, 7.3 mm above it: negligible |
| Bottom, Y 16.3–19 | PCB-09 board, Z 106.4–108.0 | 6.0 mm |
| **Rear** (X 45) | `J5-1` plug X 41.8–45, Z 115.6–119.75. Yaw FFC cassette stator above it from Z 120 (X ≤ 42.4); cooler posts below (Z ≤ 108.6) | Plug to cassette **2.31 mm**. The plug-and-lead reserve touches the cassette (0 mm, reserve to reserve) |
| **+Y** (Y 19) | `J5-2`, `J5-3`, `J5-6` plugs to Y 22.2. PCB-09's top-entry `J9-2` plug (X 48–56.75, Y 24.4–28.55, Z 112.2–115.4) and `J9-3` (Y 30.9–35.05) | Plug to plug **2.21 mm** (`J9-2`), 8.7 mm (`J9-3`). The +Y plug-and-lead reserve overlaps PCB-09's top-entry reserve by 36 mm³ (Z 115.6–116): the W27 leads leave over `J9-2`, whose own lead rises there. Leads aren't routed in CAD; stage 3 |
| **−Y** (Y −19) | `J5-4`, `J5-5` plugs to Y −22.2; `J5-7` plug to Y −31. Ethernet jack below | 6.25 mm under the `J5-7` plug |
| **Front** (X 75) | USB jacks run on under to X 77.0 (Z ≤ 111.9). Speaker magnet and cavity keep-out from X 82 (Y ±27, Z 72–126) | 7.0 mm |

**Two changes since the board was placed.** `COMPUTE_SHIFT_X` (+10 mm) moved the Pi and cooler forward after PCB-05 was positioned. The note "forward of the cooler headroom (cooler X ≤ 43.6)" in audiosystem.md and `body_v1_model.py` is out of date: the cooler now runs 7.75 mm under the board's rear, 5.95 mm below it, and the Pi's USB stacks lie under the front half at 2.10 mm. Nothing clashes. But the compute tray slides in from the front **2 mm high** (D-042), so the Pi's box passes **0.10 mm** under the board's underside. `check_compute_mount.py` passes on that 0.10 mm, which the board's ±0.16 mm thickness tolerance can eat. **So PCB-05 must go in after the compute tray**, and its fixing must allow that (decision E).

**Height and area budget.**

| Face | Max part height | Area |
|---|---|---|
| Top | 7.4 mm (to the CAD reserve; 10.4 mm to the rail). Tallest: Micro-Fit (CAD block 10 mm, already modelled to Z 125.6, 8.4 under the plate; check the 43650 drawing at the schematic), GH headers 4.25 mm, 10 µF 0805 1.45 mm | Connector footprints about 380 mm² of 1,140. The interior left is about 25 × 27 mm (X 50.3–75 past `J5-1`'s courtyard, Y ±13.5 between the side headers' courtyards), less `J5-7`'s intrusion: about 630 mm². Parts courtyards about 200 mm²: U1/U2 2.1 × 1.3, U3 4 × 4, about 25 passives at 0402/0603 (1.8 × 0.9 / 2.9 × 1.4), the ferrite, 2 × 0805, about 13 test points (Ø1.5 + courtyard), 2–3 fixings |
| Bottom | **No parts.** An 0402 would fit by height over the USB jacks (2.10 − 0.16 tolerance − 0.55 = 1.39 mm), but it would hit the tray's insertion sweep, and single-sided assembly is cheaper | A near-solid ground plane |

So everything fits by height and by courtyard on the top face, at the CAD position and size. The one envelope change is the fixing (decision E): three Ø4.35 × 8 mm spacers (Ø5.3 solder rings) on the top face, which reach Z 123.6, 0.6 mm past the old parts reserve, onto bosses printed on the frame.

**Layout notes carried from the spec (§2.4)**, with what this lesson changed:

- **Class-D output.** The MAX98357A's outputs are 300 kHz PWM square waves, 0–5 V, edge-rate limited and spread-spectrum, with no LC filter: the speaker coil's inductance (> 10 µH; the K 50 WP is 8 Ω) does the filtering. Keep the VDD capacitors at pins 7/8 and the EP so the switching current loop is a few mm². Run OUTP/OUTN as a short, wide pair to `J5-6`, over ground and away from the PDM and I²S lines. Their parasitic capacitance costs VDD × 300 kHz × C (50 pF a side is 150 µA). Unfitted EMI ferrite and capacitor footprints go at `J5-6`.
- **Placement follows the connectors.** `J5-7` (5 V in, −Y) and `J5-6` (speaker, +Y) are both at X 64.5–72, so the amplifier and its power loop take the front third. `J5-1` (host, rear) and `J5-2…5` (mics, X 46–63.5) put the I²S and PDM in the rear two-thirds. The two halves meet only at SDO0/BCLK/LRCLK into U3.
- **Grounding.** One unbroken ground plane on the bottom; no split. The mics are digital, so nothing on this board is a small analog signal. What needs protecting is the mic **supply** (the mic's ADC reference) and the PDM edges. W12's GND and W26's GND both land on this plane, so the amp's return current divides between W12 (about 6 mΩ) and the long path back through W26, the Pi and `PB-COMPUTE`. Most of it takes W12. The share through W26 (estimated under 100 mA peak, a few mV of ground shift) is harmless to 3.3 V logic. That is one reason for decision A.
- **PDM clock distribution.** Each ADAU7002's PDM_CLK fans out to two leads (150 + 150 mm front, 200 + 200 mm rear). Split it at the pin into two branches, each with its own series resistor, so each lead is source-terminated and a fault on one lead doesn't stop the other. Keep CLK away from DATA on the board as the lead does (GND between them). The two DATA wires of a pair meet at PDM_DAT: each mic already has 100 Ω at its own end (PCB-06 R1).
- **Layers:** two (decision G).
- **Gain:** a GAIN_SLOT resistor footprint (Table 8: 15 dB = 100 kΩ to GND, 12 dB = GND, 9 dB open, 6 dB = VDD, 3 dB = 100 kΩ to VDD). Fit after the BO-007 bench listen (D-034's capped gain).
- **Test points:** the §2.4 list, on the top face.

**Sourcing** (2026-10-27). India means element14 India too, which ships UK stock and handles the import ([D-066](../../decisions.md#d-066)).

| Part | element14 India | LCSC / JLCPCB |
|---|---|---|
| ADAU7002ACBZ-R7 | 4028782: **740 in stock** (UK), ₹233.15 each, ₹173.24 at 10+; MSL 1 | C481886: LCSC 100 in stock, US$4.67 at 1+. JLCPCB extended part, **X-ray inspection required** |
| MAX98357AETE+T | 2949165: **23,382 in stock** (UK), ₹390.67, ₹295.50 at 10+ | C910544, extended part (stock not read) |
| JST GH SM10B / SM04B / SM02B-GHS-TB | 5110305 / 5110298 / 5110296: **no stock**, "available to order" (SM02B: 40-week lead, 100 minimum) | SM04B is C189895; the others to look up. Stock not read |
| Molex 43650-0200 | 2324861: 12,847 in stock (SG/UK), ₹81.93 | Through hole: hand-soldered or THT assembly |
| Passives, ferrite | — | Fab basic parts |

The route (consign the ICs from element14 India as PCB-06 does, or let the fab buy them) is a procure-stage choice. Nothing above blocks the design. The GH headers have no India stock, so they come from the fab's stock whichever route is chosen.

**Gaps.**

1. **Closed with D-067: spec text.** audiosystem.md §1.3, §2.1, §2.3, §2.4, §4.2 and §6, the body BOM and BO-002/BO-006 now carry decisions A–G. Still stale, and left alone: the RP-06 peripheral selection (read-only) and the comment above `PCB05_CENTER` in `body_v1_model.py` (a subsystem source) both say the cooler is behind the board (*Two changes*).
2. **Closed with D-067: tray sweep at 0.10 mm.** PCB-05 goes in after the compute tray and PCB-09; the order is in D-067 and `check_pcb05_mount.py`.
3. **PDM_CLK duty** at 3.072 MHz is unspecified for the ADAU7002 and must be 48–52 % at the mic: bench (§5.3, with PCB-06 gap 9).
4. **WLCSP on fab-neutral rules:** pads ≤ 0.24 mm, one mask opening, X-ray at JLCPCB. **Lion Circuits MII's WLCSP capability is unverified**, and its assembly minimum is 50 × 100 mm (panelise). Check before the fab DFM.
5. **The +Y leads cross PCB-09's top-entry plugs** (36 mm³ reserve overlap). Route the W26/W27 harness in stage 3.
6. **Micro-Fit 43650-0200 height** from its drawing (the CAD uses a 10 mm block); read it at the schematic.
7. **Spacer assembly.** The 8 mm WA-SMSI comes on 24 mm tape with a polyimide pick-up tape; check each fab can place it (or hand-solder the three). Use Würth's KiCad footprint (WA-SMSI library) at board set-up.

### Decisions

Taken 2026-10-27 by the builder, the recommended option of each ([D-067](../../decisions.md#d-067)). The options are kept as the record.

**A. 5 V route.** The peripheral selection put 5 V on the GH 10 as well as on W12; W26 in the connector schedule has none.
- **A1 (chosen): W12 only.** The GH 10 carries signals, the Pi's 3V3 and two grounds. Amp current stays off the I²S grounds and off GH's 1 A contacts. And 5 V on the GH 10 could only come from the Pi's header 5 V through PCB-09, which would bypass `PB-AUDIO-OUT`'s e-fuse and its CHARGE-off.
- A2: both, which needs a 5 V source on PCB-09 and ties two supplies together on PCB-05.

**B. `CA-06` CR-01.** GPIO22 → I²S0 SDI1, GPIO23 → `AMP_SD` (plain output, default low). RP1's function table confirms GPIO22's function 2 is `I2S0_SDI[1]` (GPIO23's is `I2S0_SDO[1]`, unused). They collide with none of the UART0/2, I²C1 or SPI0 reservations, nor with CR-02's GPIO24 `FAN_EN` (D-042). **Accepted.**

**C. Power-good to the Pi.** §4.2: nothing carries `PB-AUDIO-OUT`'s power-good to the Pi. The datasheet removes the reason it was wanted: the amp's data inputs tolerate 6 V with VDD off, and SD_MODE's only risk is fixed by a series resistor.
- **C1 (chosen): no power-good path.** 2.2 kΩ in series with SD_MODE, keep the 100 kΩ pull-down, and software raises `AMP_SD` when it plays. Also lay out an unfitted divider from +5V_AMP to the W26 spare pin, so C2 needs no new board.
- C2: fit that divider (5 V → about 3 V) on the spare pin to a Pi GPIO. Needs a CR-03 and a PCB-09 trace.
- C3: a 74LVC1G08 on PCB-05 ANDs `AMP_SD` with 5V-present before SD_MODE. A hardware interlock, but no information reaches the software.

**D. `J5-2…5` map.** D-037 already puts the +Y (L) mics on `J5-2`/`J5-3` and the −Y (R) mics on `J5-4`/`J5-5`.
- **D1 (chosen): by position along X.** `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R. The rear headers (X 46–54) take the rear leads, which arrive from behind. U2 (rear pair, SDI1) sits between `J5-2` and `J5-4`, and U1 (front pair, SDI0) between `J5-3` and `J5-5`. Each converter's PDM traces cross the board once, about 30 mm.
- D2: front first: `J5-2` FRONT_L, `J5-3` REAR_L, `J5-4` FRONT_R, `J5-5` REAR_R. The numbering reads front to back, but the rear leads plug in forward of the front ones and cross them.

**E. Fixing points.** None in CAD. Constraints: no screwdriver can reach the underside (the Pi is 2.1 mm below); the board must go in after the compute tray; the frame's front upper cross is 10.4 mm above the rear band, and the yaw plate 18.4 mm above the middle.
- **E1 (chosen):** hang the board from the frame, as built in `final/v1/cad` (`PCB05_MOUNT`):
  - **Spacers:** three Würth 9774080243R M2 SMT steel spacers, Ø4.35 × 8 mm, through thread, reflowed on the top face. World (48.5, ±11.0) and (63.0, 0.0); **board-local (3.5, 30.0), (3.5, 8.0) and (18.0, 19.0)** from the corner at (45, −19). The rear pair sits between `J5-1` and the `J5-2`/`J5-4` headers; the front one where the amp's third of the board begins.
  - **Frame:** Ø7 printed bosses on `BODY_FRAME_MAIN_PRINT` meet the spacer tops at Z 123.6: 2.4 mm under the front upper cross rail, 10.4 mm under the yaw plate. Ø2.4 bores above them.
  - **Screws** (BO-064): ISO 7380 M2, driven from above. Two M2 × 16 from Ø4.0 × 1.5 counterbores in the rail top (head seat Z 134.0), which stay under the yaw housing seat (Z 135.5) and inside its R36.6; one M2 × 20 from the yaw plate top (Z 138.0), open above. Each ends 5.6 mm into its spacer (tip Z 118.0). 0.2 N·m maximum.
  - **Order:** after the compute tray, PCB-09 and its leads, before the yaw cartridge. Slide the board in from the front 1 mm low over the USB jacks, lift it onto the bosses, drive the screws (1.3 mm hex key). Removing it later means lifting the yaw cartridge; plugging and unplugging the leads does not.
  - **Mount check:** 7/7 pass (about 28 min, most of it the install sweep). The bosses fuse into the one frame print (volumes compared round each point, exact). The three bores are open with full 1 mm walls (10.4, 10.4 and 14.4 mm of print). Each screw ends 5.6 mm into its spacer; the rear heads sit 0.40 mm under the yaw housing, with the counterbore edge at R36.31 inside the R36.6 seat. The spacers are 0.88 mm from the `J5-2`/`J5-4` headers (their Ø5.3 solder rings 0.40). The nearest other part is 0.40 mm away (a rear screw head to the yaw housing). The board, spacers and J5 headers slide in from 40 mm in front, 1 mm low, and lift into place, at least 0.50 mm from every part fitted by then. The driver paths are open from above; the rear pair is later covered by the yaw cartridge and its clamp ring, the front one stays open. An earlier run found the bosses' 0.2 mm overlap into the frame stood proud of the cross rail's rear face; the bosses now end at the frame's underside.
- E2: printed card guides hung from the rail. The board slides in from the front over the Pi and is held by one screw at the front edge. No yaw removal, but the guides need edge strips that the side connectors leave little room for.
- E3: posts from the compute tray in front of the Pi. The board would grow forward to about X 81 (the speaker keep-out is at 82) and the posts would block the USB and Ethernet jacks. Not recommended.

**F. Mic rail filter.** It must not exceed 3.6 V. A passive filter can't raise its input, so the rail stays at or below the Pi's 3V3, nominally 3.3 V (measured at bring-up, §5.3 step 2). The mic rejects supply ripple well (PSR −80 dBFS for 100 mVpp), so the filter is for the Pi's switching hash and load steps, not audio-band ripple.
- **F1 (chosen):** ferrite bead (600 Ω at 100 MHz, 0603, DCR ≤ 0.5 Ω) + 2.2 Ω + 10 µF X5R, then 100 nF at each ADAU7002 IOVDD and at each mic connector. The bead's low-frequency inductance (about 1.5 µH) and the rail's total capacitance (10 µF + 4 × 1.1 µF on the PCB-06 boards + about 0.6 µF ≈ 15 µF) resonate near 34 kHz. Without the 2.2 Ω, Q is about 1.6 (+4 dB peak). With it, Q is about 0.12: no peak. The drop at 15 mA is about 40 mV.
- F2: a 3.0 V LDO from the Pi 3V3. It gives a hard ceiling whatever the Pi does and better low-frequency rejection, but costs dropout margin (3.3 → 3.0 V needs < 0.3 V) and one more part. The ADAU7002's I²S inputs still see the Pi's 3.3 V, within their 3.6 V absolute rating.

**G. Layers.** §2.4 suggested four.
- **G1 (chosen): two layers, 1.6 mm.** The bottom is a near-solid ground plane, since it carries no parts. The WLCSP fans out on the surface (every ball is on the outside of the array). The fab-neutral rules are written for 2-layer boards, and all three fabs make them.
- G2: four layers (signal, GND, power, signal). Easier routing, but more cost, and the fab-neutral rules would need 4-layer limits for all three fabs.

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-27:** design started (lesson 1). Read the ADAU7002 (Rev. C), MAX98357A (Rev 16), IM73D122 and RP1 datasheets; measured the board's neighbourhood in the built body CAD. Found: ADAU7002 Fig. 12 latches L on the rising edge, so the PCB-06 straps are right; the amp's data inputs are 6 V-tolerant with VDD off, but SD_MODE needs ~2 kΩ in series; GPIO22 is RP1's I2S0_SDI[1]; the compute shift put the cooler and the Pi's USB jacks under the board (2.10 mm), and the tray's insertion sweep passes 0.10 mm under it, so PCB-05 goes in after the tray; the frame cross rail is 10.4 mm above. The ICs are in stock at element14 India (UK stock); the GH headers are not. Decisions A–G raised.
- **2026-10-27:** decisions A–G taken, the recommended option of each ([D-067](../../decisions.md#d-067)): 5 V on W12 only; CR-01 accepted; no power-good path (2.2 kΩ into SD_MODE, unfitted 5V-present divider on the spare pin); mic map `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R; ferrite + 2.2 Ω + 10 µF mic rail; two layers. Mounting built in `final/v1/cad`: Würth's M2 SMT spacers stop at 8 mm, so three 8 mm spacers meet printed frame bosses, with ISO 7380 M2 screws from above; `check_pcb05_mount.py` added. audiosystem.md, the body BOM, BO-002 and BO-006 updated, BO-064 added, PCB-09 told about `J9-3`. Inputs frozen.
