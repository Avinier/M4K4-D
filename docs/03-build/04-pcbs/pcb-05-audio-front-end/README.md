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
| 1. Design | In progress: placed (D-067 amended again: one rear and two front spacers), no placement violations; routing next | — | 2026-10-27 |
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
| `J5-1` host | JST GH SM10B-GHS-TB, side entry | Rear (−X), X 45–49.95, Y −9.88…5.88 (centred Y −2.0, D-067 amended at placement) | BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, 3V3, 2 × GND, spare (5V-present, unfitted); **no 5 V** (W26 to PCB-09 `J9-3`). Order set in the schematic; PCB-09 told |
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
6. **Closed (lesson 3): Micro-Fit height.** Molex gives 6.98 mm mated; the CAD's 10 mm block is conservative. Its pins are decision H.
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
  - **Superseded at placement (decision J below):** the points are now (48.5, 9.8), (61.3, ±9.8). As first chosen:
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
- **G1 (chosen at first, replaced by four layers at routing, decision L below): two layers, 1.6 mm.** The bottom is a near-solid ground plane, since it carries no parts. The WLCSP fans out on the surface (every ball is on the outside of the array). The fab-neutral rules are written for 2-layer boards, and all three fabs make them.
- G2: four layers (signal, GND, power, signal). Easier routing, but more cost, and the fab-neutral rules would need 4-layer limits for all three fabs.

## Schematic

[`design/pcb-05-audio-front-end.kicad_sch`](design/pcb-05-audio-front-end.kicad_sch), with a PDF print, [`pcb-05-audio-front-end-schematic.pdf`](design/pcb-05-audio-front-end-schematic.pdf). One A3 sheet, written for the KiCad 10.99 nightly. Every pin end carries a short wire and a local label; nets join by label name.

**Project set-up.**

| File | Holds |
|---|---|
| `pcb-05-audio-front-end.kicad_pro` | PCB-06's project, renamed: the fab-neutral board minimums and default net class |
| `sym-lib-table`, `pcb05.kicad_sym` | Project symbol library `pcb05`. `ADAU7002` is new: KiCad has none. Pins from Rev. C Fig. 2/Table 4, typed from Table 4 (SDATA tri-state, since it floats outside its 20 bits). `MAX98357A` is KiCad's stock `Audio:MAX98357A` (pins checked against Rev 16) with the exposed pad (pin 17) typed passive: the stock "unspecified" type draws an ERC warning on GND |
| `fp-lib-table`, `pcb05.pretty/` | Project footprint `ADAU7002_WLCSP-8_0.76x1.56mm_P0.4mm`: KiCad has no 0.4 mm 2 × 4 WLCSP. Balls at ±0.2 × ±0.2/±0.6 mm, A1 top left (Fig. 2/22). **Ø0.23 mm non-solder-mask-defined pads** (0.8 × the Ø0.26 ball), so the copper gap is 0.17 mm against the fab-neutral 0.16. A 0.16 mm mask web can't fit between them, so the pads carry no mask margin and **one mask opening covers the array** (0.80 × 1.60 mm), the usual answer for 0.4 mm WLCSP. Courtyard 0.25 mm outside the package's maximum size |
| `pcb05.3dshapes/ADAU7002_WLCSP-8_0.76x1.56mm_P0.4mm.step` | Built from Fig. 22 nominals: body 0.76 × 1.56, 0.50 tall, Ø0.26 × 0.20 balls, A1 mark. So the board STEP shows the part (the PCB-11 trap) |
| Stock footprints | `TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm` (U3; the T1633+4 pad is 0.95–1.25), JST GH `SM10B/SM04B/SM02B-GHS-TB` side entry, `Molex_Micro-Fit_3.0_43650-0200`, `Mounting_Wuerth_WA-SMSI-M2_H8mm_9774080243`'s STEP (its land pattern is copied as `pcb05:Wurth_WA-SMSI-M2_H8mm_9774080243_PTH` with the Ø3 hole plated, D-067 I1), 0402/0603/0805 passives, `TestPoint_Pad_D1.0mm` |

**Circuit** (references as drawn):

| Ref | Part | Nets |
|---|---|---|
| J1 (`J5-1`) | JST SM10B-GHS-TB, W26 | **1 +3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 5V_SENSE**; MP GND (reordered at routing, D-067). BCLK, the edge everything is clocked on, has a ground wire on each side; LRCLK above it is the order the converters' balls and the amp's inputs have, so the bus leaves J1 without a crossing. SDI1 above SDI0: U2's row back to J1 is the upper one, so U1's passes under U2's drop. PCB-09 `J9-3` must match |
| J2–J5 (`J5-2…5`) | SM04B-GHS-TB, W27 | 1 +3V3_MIC, 2 CLK, 3 GND, 4 DATA (PCB-06 order). J2 REAR_L, J3 FRONT_L, J4 REAR_R, J5 FRONT_R (D-067 D) |
| J6 (`J5-6`) | SM02B-GHS-TB, W28 | 1 SPK_P, 2 SPK_N |
| J7 (`J5-7`) | Molex 43650-0200, W12 | 1 +5V_AMP, 2 GND. PCB-04 `J4-5` must match. `Assembly` field: tails clipped to ≤ 0.5 mm and peg cut flush after soldering (D-067 H1) |
| FB1, R1, C1 | 600 Ω at 100 MHz 0603; 2.2 Ω; 10 µF X5R 10 V 0805 | +3V3 → MIC_FILT → +3V3_MIC (D-067 F) |
| C4–C7 | 100 nF at each mic connector | +3V3_MIC to GND |
| U1, U2 | ADAU7002ACBZ-R7 | U1: PDM_DAT1 ← J3/J5 DATA, PDM_CLK1, SDATA → SDI0. U2: PDM_DAT2 ← J2/J4 DATA, PDM_CLK2, SDATA → SDI1. Both: BCLK, LRCLK, IOVDD and CONFIG on +3V3_MIC (I²S), GND. C2, C3 100 nF at IOVDD (Fig. 11) |
| R2–R5 | 100 Ω, one per mic lead | PDM_CLK1 → CLK_FL (J3), CLK_FR (J5); PDM_CLK2 → CLK_RL (J2), CLK_RR (J4). Source termination: the lead is about 200 Ω (`E`, two AWG28 wires 1.25 mm apart), the edge at the mic about 5 ns (≤ 13 ns). Tune on the bench |
| R6, R7 | 100 kΩ | SDI0, SDI1 to GND: SDATA floats outside its 20 bits (Fig. 11's optional pull-down) |
| U3 | MAX98357AETE+T | DIN_AMP, BCLK_AMP, LRCLK_AMP, SD_MODE, GAIN_SLOT, VDD (7, 8) +5V_AMP, OUTP, OUTN, GND (3, 11, 15) and EP (17) GND; NC 5, 6, 12, 13 |
| R8–R10 | 100 Ω | BCLK, LRCLK, SDO0 into the amp (edge damping) |
| R11, R12 | 2.2 kΩ, 100 kΩ | AMP_SD → SD_MODE, SD_MODE → GND (D-067 C) |
| R13, R14 | unfitted | GAIN_SLOT to GND (0 Ω 12 dB, 100 kΩ 15 dB) or to +5V_AMP (0 Ω 6 dB, 100 kΩ 3 dB). Both open: 9 dB |
| C8, C9 | 10 µF X5R 16 V 0805, 100 nF | At U3's VDD |
| FB2, FB3 | 0 Ω 0603 (ferrite if EMI needs it) | OUTP → SPK_P, OUTN → SPK_N |
| C10, C11 | unfitted 1 nF | SPK_P, SPK_N to GND (EMI option) |
| R15, R16 | unfitted 10 kΩ / 15 kΩ | +5V_AMP → 5V_SENSE → GND: 5.0 V → 3.0 V on J1 pin 10 (D-067 C) |
| TP1–TP12 | Ø1.0 pads, not in the BOM | BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, PDM_CLK1, PDM_CLK2, +3V3, +3V3_MIC, +5V_AMP, GND |
| H1–H3 | Würth 9774080243R | No net; assembled (in the BOM and the position file); plated Ø3 holes (D-067 I1) |

`PWR_FLAG` sits on +3V3 and +5V_AMP (they enter through connectors), on +3V3_MIC (it is made of passives, but the ADAU7002s' IOVDD pins are power inputs), and on GND. Unfitted parts carry KiCad's DNP flag; the fab outputs leave them out of the BOM and position file (lesson 5).

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-27): **0 errors, 0 warnings.** The first run, before `pcb05.pretty` existed, flagged only the missing footprint library.

**Check against the inputs**, row by row, from the exported netlist:

| Input (lesson 1, D-067) | Netlist | Result |
|---|---|---|
| Mic rail: Pi 3V3 → bead → 2.2 Ω → +3V3_MIC with 10 µF; 100 nF at each converter and mic connector | `+3V3`: J1.1, FB1.1, TP9. `MIC_FILT`: FB1.2, R1.1. `+3V3_MIC`: R1.2, C1, C2, C3, C4–C7, J2–J5 pin 1, U1/U2 D1 and D2, TP10 | Match |
| Front pair → U1 → SDI0, rear pair → U2 → SDI1 (§2.2, D-067 D) | `PDM_DAT1`: J3.4, J5.4, U1.A1. `PDM_DAT2`: J2.4, J4.4, U2.A1. `SDI0`: U1.B1, J1.8 (J1.7 before the reorder), R6, TP3. `SDI1`: U2.B1, J1.7 (was J1.8), R7, TP4 | Match |
| One series resistor per mic clock | `PDM_CLK1`: U1.A2, R2, R3, TP7 → `CLK_FL` J3.2, `CLK_FR` J5.2. `PDM_CLK2`: U2.A2, R4, R5, TP8 → `CLK_RL` J2.2, `CLK_RR` J4.2 | Match |
| One Pi clock to all three chips; 100 Ω at the amp | `BCLK`: J1.4 (J1.3 before the reorder), U1.B2, U2.B2, R8, TP1 → `BCLK_AMP` U3.16. `LRCLK`: J1.2 (was J1.5), U1.C2, U2.C2, R9, TP2 → `LRCLK_AMP` U3.14. `SDO0`: J1.6, R10, TP5 → `DIN_AMP` U3.1 | Match |
| CONFIG to IOVDD (I²S) | U1.D2, U2.D2 on `+3V3_MIC` | Match |
| AMP_SD through 2.2 kΩ, 100 kΩ pull-down | `AMP_SD`: J1.9, R11, TP6. `SD_MODE`: R11, R12, U3.4 | Match |
| 5 V on W12 only (D-067 A) | `+5V_AMP`: J7.1, U3.7, U3.8, C8, C9, R14 (DNP), R15 (DNP), TP11. No J1 pin | Match |
| Speaker pair, EMI option | `OUTP` U3.9 → FB2 → `SPK_P` J6.1, C10 (DNP); `OUTN` U3.10 → FB3 → `SPK_N` J6.2, C11 (DNP) | Match |
| Gain strap footprints, 9 dB default | `GAIN_SLOT`: U3.2, R13 (DNP to GND), R14 (DNP to +5V_AMP) | Match |
| Spare pin, unfitted divider | `5V_SENSE`: J1.10, R15, R16 (both DNP) | Match |
| One ground: chips, EP, connectors, mounting pads | `GND`: J1.3, J1.5 (J1.2, J1.4 before the reorder), J7.2, all J MP pads, U1/U2.C1, U3.3/11/15/17, every capacitor and pull-down | Match |
| Fixings no net; amp NC pins open | H1–H3 pad 1, U3 5/6/12/13 unconnected | Match |

## Layout

KiCad 10.99 nightly, laid out by hand through KiPy, with no autorouter ([D-060](../../decisions.md#d-060), [layout rules](../README.md#layout-rules)).

**Board set-up** (`design/pcb-05-audio-front-end.kicad_pcb`, written before any part is placed):

| Item | Value | Why |
|---|---|---|
| Outline | KiCad x 100–130, y 100–138 | World X = x − 55, Y = 119 − y, so the +Y edge (`J5-2`, `J5-3`, `J5-6`) is the top, `J5-1` the left. Board-local xb = x − 100, yb = 138 − y, from the corner at world (45, −19); aux and grid origins at local (0, 0), so the position file reads in board-local mm. Spacers H1–H3 at KiCad (103.5, 108), (103.5, 130), (118, 119) |
| Faces | **F.Cu: all parts. B.Cu: none**; B.Cu carries signals only, In1/In2 are the ground planes | Lesson 1: the board is 2.10 mm above the USB jacks, and single-sided assembly is cheaper |
| Stackup | 1.6 mm, **4 layers** (decision L): F.Cu 35 µm, prepreg 0.2104, In1.Cu 15.2 µm GND plane, core 1.065, In2.Cu 15.2 µm GND, prepreg 0.2104, B.Cu 35 µm; HASL lead-free. Set up first as 2 layers (1.51 mm core) | BO-002; Molex's recommended thickness for the Micro-Fit (1.57); the JLCPCB 7628 build |
| Rules | Fab-neutral (D-062) in the `.kicad_pro` and `.kicad_dru`, plus one PCB-05 rule: **tracks on +5V_AMP, OUTP/OUTN and SPK_P/SPK_N at least 0.5 mm** | 0.4 A average, 0.7 A peak, behind a 2.0 A e-fuse; the logic and mic nets draw milliamps |
| Rule areas | `BOTTOM_NO_PARTS` (B.Cu, whole board): no footprints. `USB_JACKS_NO_THT_1/2` (B.Cu, over the two USB stacks): no footprints and **no pads**, so no through-hole pin can come through over a jack; vias stay allowed (flush). `_1` is notched round J7 (tails clipped, H1) and spacer H3 (plated, flush ring, I1) | The jacks are 2.10 mm below |
| WLCSP mask | The ADAU7002 footprint carries `allow_soldermask_bridges`, so DRC accepts its one shared mask opening, and only there | Lesson 2 |
| Drawings | `Connectors.CAD` (the seven connectors where the body CAD has them), `Below.Board` (USB stacks, Ethernet, cooler, push-pin head, PCB-09, blower circle, each with its gap), `Frame.Bosses` (Ø7 bosses over Ø4.35 spacers), `Above.Board` (cross rail 10.4, yaw plate 18.4, shell 22.0), `Leads.Exit` | User layers, not in the fab set |

**DRC on the empty board** (nightly, 2026-10-27): 0 violations. A scratch copy with deliberate bad placements beside clean controls proved every rule:

| Test | Result |
|---|---|
| 0402 on the bottom face / on the top | `items_not_allowed`, `BOTTOM_NO_PARTS` / clean |
| Via over a USB stack | Clean (allowed) |
| `+5V_AMP` track 0.3 mm / 0.5 mm | `track_width`, PCB-05 rule / clean |
| ADAU7002 footprint (shared mask opening) | Clean |
| **J5-7 as drawn, Molex 43650-0200 through hole, at its CAD position** | **Both pins and the snap-in peg: `items_not_allowed`, `USB_JACKS_NO_THT_1`** (decision H) |
| **Würth spacer footprint (KiCad stock, as H1)** | **`hole_clearance` 0.254 mm (its four paste-anchor pads) and 0 mm (its solder ring) to its own Ø3 hole**, against the fab-neutral 0.31 (decision I) |
| After H1/I1: J7 at its CAD position / the same header elsewhere over the jacks | Clean (notch) / both pins and peg flagged, `USB_JACKS_NO_THT_1` |
| After I1: `pcb05:Wurth_WA-SMSI-M2_H8mm_9774080243_PTH` at H1 and H3 | Clean |

### Decisions (lesson 3)

Taken 2026-10-27 by the builder: **H1 and I1** ([D-067](../../decisions.md#d-067), amended). J7 carries an `Assembly` field with the clipping instruction; H1–H3 use the plated-hole footprint, a copy of Würth's with the Ø3 hole as pad 1. The options are kept as the record.


**H. J5-7 is through hole, and its pins land over a USB jack.** The 43650-0200's pins are 9.9 mm in from its mating face, so at the −Y edge they sit at world Y −9.1, over the Pi's USB stack (Y −12.0…3.8, top 2.10 mm below the board). Molex's drawing (SD-43650-001) gives 3.18 mm tails: 1.6 mm out of the bottom of a 1.57 mm board, plus solder, so about **0.5 mm** to the jack. The Ø3 snap-in peg (about 3.3 mm long) sits on the stack's edge, about 0.4 mm above it. That is under the 0.5 mm margin, with no tolerance. (Molex gives a 6.98 mm mated height, so lesson-1 gap 6 is closed: the CAD's 10 mm block is conservative.)
- **H1 (chosen): keep the 43650-0200, clip the tails and the peg.** After soldering, the two tails are clipped to ≤ 0.5 mm below the board and the peg is cut flush. That leaves about 1.2 mm to the jack. A work instruction on the fab order (or the builder solders J5-7 by hand: one 2-pin THT part on an SMT board), and the USB rule area gets an exception for J5-7's own pads. Measure the clipped board at receipt.
- H2: the surface-mount 43650-0212 (element14 India 2614956, 8,715 in stock, ₹214.53). No tails at all, but its solder tabs make it 15.2 mm wide; the −Y edge has about 11 mm between `J5-5` and the front edge. It fits only if `J5-4`/`J5-5` move or the board grows: an envelope change.
- H3: swap `J5-7` with `J5-4` along the −Y edge, so its pins land over the cooler plate (7.0 mm below). It stays inside the existing −Y plug reserve, but spacer H2 at (48.5, −11.0) is in the way, so the D-067 fixing moves, and the amp's 5 V then enters at the rear while the speaker leaves at the front.

**I. The Würth spacer's own solder ring meets its hole.** Würth's land pattern (KiCad's `Mounting_Wuerth_WA-SMSI-M2_H8mm_9774080243`) is a copper ring R 1.50–2.65 round a Ø3 non-plated hole: 0 mm of copper-to-hole clearance, and 0.254 mm from four small anchor pads. JLCPCB publishes "NPTH to copper 0.2 mm", the fab-neutral rule is 0.31. The spacer's base is an annulus about R 1.40–2.18 and is rated 0.2 N·m.
- **I1 (chosen): plate the hole.** A project copy of the footprint with the Ø3 hole plated and the ring as its annular ring. A plated hole with a pad is ordinary for every fab, so no exception is needed, and the barrel adds solder area. Solder may wick a little into the barrel; nothing passes through it (the screw ends 2.4 mm above the board, inside the spacer).
- I2: pull the ring back to R 1.81 (0.31 mm from the hole). Fab-neutral, but the solder area under the spacer drops to about 59 %, and at the rated 0.2 N·m the joint's shear stress rises from about 14 to 22 MPa, near tin solder's strength.
- I3: keep Würth's pattern with a DRC exception for that hole and confirm at each fab's DFM, as PCB-06's option C1 would have.

### Decision J (placement)

Placing the fixed parts showed the lesson-1 fixing collided with the real footprints: spacer H1's Ø5.3 ring overlapped `J5-2`'s signal pads (H2 `J5-4`'s) by up to 0.1 mm, both spacers' Ø5.8 courtyards overlapped `J5-1`'s and the corner headers', and `J5-7`'s housing is 9.65 mm wide where the CAD block had 7.26. The lesson-1 mount check had measured the spacers against the CAD's connector bodies, and the GH pads run 1.1 mm further inboard than those bodies. A rear corner leaves 4.3 mm between `J5-1`'s courtyard and the corner header's for a 5.8 mm spacer courtyard, and the counterbore must stay inside the yaw housing's R36.6 seat, so two rear spacers cannot fit.

**Taken 2026-10-27 by the builder: J1** ([D-067](../../decisions.md#d-067), amended again). One rear spacer, two front:

| Spacer | World (X, Y) | KiCad | Board-local | Above |
|---|---|---|---|---|
| H1 | (48.5, 9.8) | (103.5, 109.2) | (3.5, 28.8) | Cross rail; M2 × 16 from a counterbore (edge R35.95 in the R36.6 seat) |
| H2 | (61.3, 9.8) | (116.3, 109.2) | (16.3, 28.8) | Yaw plate; M2 × 20; open above until the yaw cartridge's flange covers it |
| H3 | (61.3, −9.8) | (116.3, 128.8) | (16.3, 9.2) | Yaw plate; M2 × 20; open above until the yaw cartridge's flange covers it |

`J5-1` slides 2.0 mm toward −Y; `J5-7` moves 1.5 mm forward for its real housing; `J5-2`/`J5-4` and `J5-6` move 0.225 mm apart. H2 and H3 sit over the USB stacks, so both USB rule areas are notched round them (plated rings, flush). Options not taken: J2, two rear spacers with `J5-1` split into two GH 5 (W26 and PCB-09 change); J3, the old points with a smaller ring and accepted courtyard overlaps. `final/v1/cad` and `check_pcb05_mount.py` are updated: 7/7 pass. The bosses fuse into the one frame print (local volumes exact). The three bores are open with 1 mm walls (10.4, 14.4, 14.4 mm of print). Each screw ends 5.6 mm into its spacer; the rear head sits 0.40 mm under the yaw housing, its counterbore edge at R35.95 in the R36.6 seat. The spacers are at least 1.03 mm from every CAD connector (their solder rings 0.55). The board slides in from the front 1 mm low and lifts into place with at least 0.50 mm to every part fitted by then. The driver paths are open from above; the yaw cartridge covers all three later. The first run failed the slide on the CAD's 10 mm `J5-7` block, which met the front −Y boss; the real Micro-Fit is 6.98 mm tall mated (Molex), 1.0 mm under the boss, so the block is cut to that height (`DROID_CUTS`).

### Decision L (routing)

The amplifier corner routed cleanly on two layers. The left half could not: each ADAU7002's BCLK and LRCLK balls are neighbours on one side while both clocks run on to the next chip, so each chip needs one crossing; and each converter feeds a header on both edges, so every mic clock and data line to the far edge crosses the clock bus, as do the slow lines back to J1. That is about 12–16 hops through the bottom ground plane, each one slotting the plane under the clock lines whose return current it carries. Lesson 1's G1 had looked only at the WLCSP fan-out.

**Taken 2026-10-27 by the builder: L2 and the J1 reorder** ([D-067](../../decisions.md#d-067), amended again). Four layers: F.Cu parts and signals, In1 solid GND, In2 GND, B.Cu signals with no parts; crossings become vias to B.Cu over an unbroken plane. J1 becomes 1 +3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 5V_SENSE (SDI1 above SDI0 was set while routing; see below). Lion Circuits' MII makes 4 layers with its 2-layer limits, so the fab-neutral rules stand. Not taken: L1 (two layers with the hops), L3 (re-pair the mic lanes by side).

**Placement** (2026-10-27, through KiPy, one functional group at a time; KiCad coordinates):

| Group | Parts and positions | Notes |
|---|---|---|
| Fixed | J1 (103.0, 121.0) 270°; J2 (104.9, 103.0), J3 (114.375, 103.0), J6 (122.6, 103.0) at 180°; J4 (104.9, 135.0), J5 (114.375, 135.0) at 0°; J7 (126.13, 128.1) 180°; H1–H3 as above | GH mating faces 0.55 mm inside the board edge, so their mounting tabs keep 0.3 mm of copper to the edge. J1 pins top to bottom 1–10 at x 104.85, y 115.375–126.625 |
| Converters | U2 (109.6, 120.0) 180°, C3, R4 (CLK_RL up to J2), R5 (CLK_RR down to J4); U1 (116.3, 119.4) 180°, C2, R2 (up to J3), R3 (down to J5) | Rotated so BCLK/LRCLK face J1. U2 between `J5-2`/`J5-4`, U1 between `J5-3`/`J5-5` and between spacers H2/H3. Each clock resistor sits at its converter |
| Mic rail and bypass | FB1 (107.9, 113.3), R1 (110.4, 113.3), C1 (110.6, 111.2) beside J1's 3V3 pin; C4 (108.2, 107.8), C5 (120.08, 106.05), C6 (102.545, 130.6) 180°, C7 (112.02, 130.6) 180° at the mic connectors' pin 1; R7 (111.5, 119.6) 90° and R6 (118.8, 119.3) at their converters' SDATA vias | Positions as routed. R6/R7 started by J1 pins 7/8 and moved at routing: their ground via had no legal spot between the In2 rows |
| Amplifier | U3 (124.6, 115.6) 90°: outputs up toward J6 (OUTP/OUTN in J6's order, no crossing), supply right, clocks left, DIN/GAIN/SD_MODE down. C9 at pins 7/8, C8 on the way to J7. FB2/FB3 (series 0 Ω) and C10/C11 (DNP) between U3 and J6. R8–R10 left of U3; R14, R13, R12 below it (GAIN branches left, SD_MODE right); R11 right | The class-D loop: J7 → C8/C9 → pins 7/8 → EP/GND, all in the right third; the outputs run 10 mm straight up to J6 |
| Others | R15/R16 (DNP 5V sense) by J7; TP1–TP12 by their nets: TP4/TP3 (SDI1/SDI0) beside J1's vias, TP7/TP8 off the PDM clock branches, TP10 on the C4 feed | Test pads have Ø2 courtyards, so several moved at routing |

**DRC after placement** (nightly, with schematic parity): **no copper, clearance or courtyard violations.** What remains is routing (114 unconnected), the cosmetic `lib_footprint_mismatch` on rotated parts, and silkscreen reference text, which moves to the fab layer at the end.

### Routing (lesson 4)

Routed by hand through KiPy on four layers (decision L), 2026-10-27. Track widths: 0.2 mm for signals, 0.3 mm for grounds and the mic supply, 0.5 mm for the amplifier's 5 V and speaker nets (the PCB-05 rule).

| Layer | Carries |
|---|---|
| F.Cu | All parts. J1's pad-to-via stubs, the converter escapes and taps, the whole amplifier corner, the PDM clock branches, the down-feeds `CLK_RR` and `CLK_FR`, every header's supply, ground and shell pads |
| In1.Cu | **Solid GND, no tracks.** The reference every layer can reach in one via |
| In2.Cu | GND pour, plus the slow rows back to J1 (SDI1 y 122.875, SDI0 124.125, `AMP_SD` 125.375, `5V_SENSE` 125.8), the four up-feeds to J2/J3 (`CLK_RL`/`PDM_DAT2` and `PDM_DAT1`/`CLK_FL`), and the +3V3_MIC feed down the west side to J4/J5 |
| B.Cu | The clock bus from J1's vias east to R8–R10 (LRCLK y 115.35, BCLK 116.6, SDO0 117.85; no vias within 0.745 mm of it), the data down-feeds to J4/J5, and the short hop for the unfitted R14/R15 5 V branch |

**What this board teaches** (the parts new since PCB-15, PCB-11 and PCB-06):

- **Class-D output.** The amplifier's high current is confined to the right third: J7 → C8 → C9 at pins 7/8 → the exposed pad's ground vias, a loop a few mm across, all at 0.5 mm. OUTP/OUTN leave the top of U3 in J6's order and run as a pair straight up to J6 through FB2/FB3, with no other net between them and nothing routed under them. The PWM edges then stay between the two wires to the speaker and never travel through the converters' ground.
- **PDM clock distribution.** Each mic lead has its own 100 Ω series resistor at its converter, so each 200 mm lead is source-terminated on its own: one resistor can't match two leads hanging off it in parallel. The clock splits at the converter ball, not at a header. Where each pair crosses the bus band, its clock and data run as neighbours on In2 (0.75–0.9 mm apart). Spacer H2 and the header vias part them elsewhere.
- **Mixed-signal grounding.** One ground, never split. Every ground pad, shell pad and decoupler has its own via into In1/In2 right beside it. The mic supply is filtered once (FB1 → R1 → C1) and fans out from C1 to the four connectors and both converters. **Found while routing:** the B.Cu clock bus is 0.21 mm from In2, so In2, not In1, carries its return current, and the four up-feeds slot In2 where they cross under the bus (x 111.55/112.3 and 118.4/119.3). The bus is about 14 mm long against edges about a metre long, so the effect is small. Still, four GND stitching vias beside the slots, (113.1, 118.9), (113.2, 113.4), (117.6, 113.4) and (120.4, 113.4), plus the existing ones at (110.75, 119.15) and (117.45, 118.65), give the return current a path down to the solid In1 plane and back up round each slot. On a later board where that matters more, swap the roles of In2 and B.Cu: bus on In2 against In1, feeds on B.Cu.
- **The via rule is via copper to other copper, 0.31 mm** (D-062's Lion MII spacing), not hole to copper. Five vias failed it on the first run and moved 0.05–0.1 mm. Two vias can't sit between rows 1.25 mm apart, which is why the pull-downs moved to the converters.

Totals: 296 mm of track on F.Cu, 171 mm on In2, 84 mm on B.Cu; 59 vias, all 0.67/0.35.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, fab-neutral `.kicad_dru`, 2026-10-27): **0 errors, 0 unconnected pads, 0 schematic-parity issues**, and no keep-out, courtyard or clearance hits. Reference labels are on the fab layers (`refs_to_fab()`), so the silkscreen findings are gone. 30 warnings remain, all `lib_footprint_mismatch`, on parts that were turned at some point during placement, including some turned back to 0°. R2 was diffed against the library: identical pads, and outlines 1 nm off (`0.469999` against `0.47`), the round-off PCB-15 found. `audit()`: every footprint has its 3D model; TP1–TP12 are out of the BOM and position file. **U1 and U2 had none:** the project ADAU7002 footprint writes its `(model …)` on one line, and `kp.library_models()` only parsed the multi-line form, so `place()` could never restore it. The parser now balances parentheses, and the models are back (the board STEP would otherwise have left out both converters, PCB-11's trap).

## Log

Record dated entries: decisions raised, revisions, orders, bench results.

- **2026-10-27:** design started (lesson 1). Read the ADAU7002 (Rev. C), MAX98357A (Rev 16), IM73D122 and RP1 datasheets; measured the board's neighbourhood in the built body CAD. Found: ADAU7002 Fig. 12 latches L on the rising edge, so the PCB-06 straps are right; the amp's data inputs are 6 V-tolerant with VDD off, but SD_MODE needs ~2 kΩ in series; GPIO22 is RP1's I2S0_SDI[1]; the compute shift put the cooler and the Pi's USB jacks under the board (2.10 mm), and the tray's insertion sweep passes 0.10 mm under it, so PCB-05 goes in after the tray; the frame cross rail is 10.4 mm above. The ICs are in stock at element14 India (UK stock); the GH headers are not. Decisions A–G raised.
- **2026-10-27:** decisions A–G taken, the recommended option of each ([D-067](../../decisions.md#d-067)): 5 V on W12 only; CR-01 accepted; no power-good path (2.2 kΩ into SD_MODE, unfitted 5V-present divider on the spare pin); mic map `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R; ferrite + 2.2 Ω + 10 µF mic rail; two layers. Mounting built in `final/v1/cad`: Würth's M2 SMT spacers stop at 8 mm, so three 8 mm spacers meet printed frame bosses, with ISO 7380 M2 screws from above; `check_pcb05_mount.py` added. audiosystem.md, the body BOM, BO-002 and BO-006 updated, BO-064 added, PCB-09 told about `J9-3`. Inputs frozen.
- **2026-10-27:** lesson 2. Schematic drawn for the KiCad 10.99 nightly, generated pin end by pin end from the library symbols: J1–J7, U1/U2 ADAU7002, U3 MAX98357A, the mic-rail filter, PDM clock resistors, SDATA pull-downs, amp damping and SD_MODE network, unfitted gain, EMI and 5V-sense parts, 12 test points, H1–H3 spacers. New project parts: an ADAU7002 symbol, its WLCSP footprint (Ø0.23 pads, one mask opening) and a 3D model from Fig. 22; the stock MAX98357A with its pad typed passive. `J5-1` order set: 1 +3V3, 2 GND, 3 BCLK, 4 GND, 5 LRCLK, 6 SDO0, 7 SDI0, 8 SDI1, 9 AMP_SD, 10 5V_SENSE. ERC 0 errors, 0 warnings; the netlist matches the inputs row by row.
- **2026-10-27:** lesson 3. Board set up: 30 × 38 outline, 1.6 mm stackup, origins at board-local (0, 0), rule areas for the bare bottom face and for no pins over the USB jacks, a 0.5 mm minimum on the amp's power and speaker tracks, the envelope on user layers; all proven on a scratch copy. Found: J5-7's through-hole pins and peg land about 0.5 mm above a USB jack (decision H), and Würth's spacer land pattern puts copper at its own hole's edge (decision I).
- **2026-10-27:** decisions H1 and I1 taken ([D-067](../../decisions.md#d-067) amended): J7 stays the through-hole 43650-0200 with its tails clipped and its peg cut flush; the spacers sit on plated Ø3 holes (project footprint from Würth's). USB rule area notched round J7 and H3; DRC re-proved on a scratch copy; ERC still 0/0. BO-002 updated.
- **2026-10-27:** lesson 4, placement. F8 by the builder; parts placed through KiPy in groups. The fixed parts collided with the D-067 fixing (spacer rings on GH pads, courtyards, J7's real 9.65 mm housing): decision J1 taken, one rear spacer at (48.5, 9.8) and two front at (61.3, ±9.8), `J5-1` 2 mm toward −Y; D-067 amended, CAD and mount check updated, USB rule areas re-notched. All parts placed; no copper, clearance or courtyard violations. Routing next.
- **2026-10-27:** routing started. The amp corner routed on two layers (0.5 mm 5 V trunk and speaker pair, a B.Cu hop for the unfitted R14/R15 branch, ground vias) and a B.Cu GND plane poured. The left half needed 12–16 plane hops on two layers: decision L2 taken (four layers, In1/In2 GND) and J1 reordered (LRCLK above BCLK); D-067 amended. Mount check for decision J: 7/7 after cutting the CAD's J5-7 block to Molex's 6.98 mm mated height.
- **2026-10-27:** routing finished on four layers. The bus runs on B.Cu, the slow rows and mic up-feeds on In2, and the down-feeds on F.Cu and B.Cu. J1 pins 7/8 swapped while routing (7 SDI1, 8 SDI0) so the In2 rows don't cross; D-067, audiosystem.md and PCB-09 updated. Moved while routing: R6/R7 to the converters, C5–C7 and TP3/4/6/7/8/10. Found and fixed: the 0.31 mm via-copper rule (five vias moved), J6's shell pads unconnected, U1/U2 without 3D models (`kp.library_models()` one-line parse), In2 slotted under the clock bus (four stitching vias). DRC 0 errors, 0 unconnected, parity clean; 30 cosmetic `lib_footprint_mismatch`.
