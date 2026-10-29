# PCB-13 — Charge inlet

USB-C inlet: GCT USB4140, STUSB4500 PD sink, TVS2200/ESDA25W protection and the input P-FET.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | BO-015 in [BOM.csv](../../BOM.csv) |
| Location | Body, rear-panel pad (comes off with the panel) |
| Specification | [charge-path.md §3](../charge-path.md#3-pcb-13--charge-inlet-board), [§6](../charge-path.md#6-the-inlet-on-the-panel), [§8](../charge-path.md#8-stusb4500-nvm-image)<br>[open items](../open-items.md) CP-OI-01, CP-OI-03 to CP-OI-05<br>[D-040](../../decisions.md#d-040) |
| CAD placeholder | `charge_inlet_pcb13()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `CHARGE_INLET_PCB13` |
| Final CAD | `Custom PCBs › PCB-13 charge inlet` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | In progress: placed and routed (DRC 0 errors, 0 unconnected, parity clean); checks and outputs next | *Inputs* to *Layout*; `check_pcb13_relief.py` 13/13 | 2026-10-29 |
| 2. Procure | — | — | — |
| 3. Integrate | — | — | — |

## Inputs

Drafted 2026-10-28 (lesson 1). **Frozen 2026-10-29 with [D-069](../../decisions.md#d-069)**: the builder took the recommended option for gaps 1, 3, 4 and 5, and chose to hand-solder J1 (gap 2).

**Spec sources.**

- [charge-path.md](../charge-path.md) §2 (power path), §3 (this board's parts and layout rules), §5.3 (voltage ratings), §6 (the inlet on the panel), §7 (sequence and faults), §8 (NVM image), §9 (bench CP-01 to CP-03, CP-13, CP-14).
- [D-040](../../decisions.md#d-040); [open items](../open-items.md) CP-OI-01, CP-OI-03 (closed here), CP-OI-04, CP-OI-05.
- BOM rows BO-015 (this board), BO-016 (adapter and cable), BO-017 (M2 × 5 screws), HN-003 (Micro-Fit housings for `J2-8`).
- [05-harness §5](../../05-harness/README.md#5-pinouts): `J2-8` is 1 VSNK, 2 GND, with the female contacts on the `W16` side.
- CAD: the `CHARGE_INLET_*`, `PCB13_*` and `USB4140_*` constants, `rear_panel_charge_inlet()` and `charge_inlet_pcb13()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py); [`check_charge_inlet.py`](../../02-body/v1/cad/check_charge_inlet.py). Measured in the droid tree (`makad-v1.step.py` with its droid edits), see *Envelope*.

**Datasheets read** (2026-10-28):

- GCT [USB4140](https://gct.co/files/drawings/usb4140.pdf), drawing revision A3, 29/08/24 (sheets 1–2: part, recommended PCB layout, pin table).
- TI [TVS2200](https://www.ti.com/lit/ds/symlink/tvs2200.pdf), SLVSED5C (August 2023), with the DRV0006A outline 4222173/C.
- ST STUSB4500 DS12499 Rev 3 ([SparkFun mirror](https://cdn.sparkfun.com/assets/b/6/e/8/9/DS-15801-STUSB4500.pdf)).
- ST ESDAxxxWx Rev 2, August 2005 ([mirror](https://media.bostk.com/Datasheet/ST/1037976----ESDA25W.pdf)): the ESDA25W's own datasheet, which closes the CP-OI-03 gap.
- ST STL6P3LLH6 DS9257 Rev 4, March 2020 ([mirror](https://www.semiconductors-chips.com/files/00/stl6p3llh6.pdf)).

st.com still times out; the mirrors are copies of ST's own PDFs (document numbers and revisions shown above).

### Circuit

The circuit is charge-path §3 unchanged. Every part was checked against its maker's datasheet:

| Ref | Part | Package (max height) | Pins (datasheet) | Ratings confirmed (`D`) | Footprint |
|---|---|---|---|---|---|
| J1 | GCT USB4140-GF-0170-C | Vertical, 6.50 above the board, on the −X face | One row of six SMT tails: B12 GND, B9 VBUS, A5 CC1, B5 CC2, A9 VBUS, A12 GND (left to right in GCT's layout view), at x = −2.75, −1.52, −0.50, +0.50, +1.52, +2.75. Shell (four stakes) GND | VBUS 3.00 A together, GND 4.25 A together, CC 1.25 A; 48 V DC; 40 mΩ maximum per contact initially, 50 mΩ after test; mating 5–20 N; 20k cycles (plug replaced at 10k in GCT's test); −25…+85 °C. Stake S = 1.70 ± 0.15 | **Project footprint** (KiCad has no USB4140); see *J1 land pattern* |
| D1 | TI TVS2200DRVR | WSON-6 DRV 2 × 2, 0.8 | 1–3 GND, 4–6 IN, thermal pad GND | VRWM 22 V; VBR 24.6–27.6 V; clamp 28.0 V maximum at 40 A (8/20 µs, 27 °C), **28.35 V** maximum at 35 A from VRWM at 125 °C; 105 pF | Stock `WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm` (TI's example layout: pad 1.0 × 1.6, pitch 0.65) |
| D2 | ST ESDA25W | SOT-323-3L, 1.1 | 1, 2 cathodes (lines), 3 common anode (GND) | VRM 24 V; VBR 25–30 V; 65 pF typical at 0 V; IEC 61000-4-2 level 4 (8 kV contact, 15 kV air); 400 W (8/20 µs). It is ST's own CC part in the STUSB4500 application diagram | Stock `SOT-323_SC-70` |
| U1 | ST STUSB4500QTR | QFN-24 4 × 4, EP 2.70; A 1.00 maximum | 1 CC1DB, 2 CC1, 3 NC, 4 CC2, 5 CC2DB, 6 RESET, 7 SCL, 8 SDA, 9 DISCH, 10 GND, 11 ATTACH, 12 ADDR0, 13 ADDR1, 14 POWER_OK3, 15 GPIO, 16 VBUS_EN_SNK, 17 A_B_SIDE, 18 VBUS_VS_DISCH, 19 ALERT, 20 POWER_OK2, 21 VREG_1V2, 22 VSYS, 23 VREG_2V7, 24 VDD, EP GND | VDD 28 V; CC 22 V; VBUS-side pins (`VBUS_EN_SNK`, `VBUS_VS_DISCH`, `DISCH`, `POWER_OK2`) 28 V; every other I/O −0.3…6 V. `VBUS_VS_DISCH` 50 mA maximum (R1: 20 mA at 20 V); `DISCH` 500 mA maximum (R2: 32 mA at 15 V). `VSYS` to GND when unused (as §3) | Stock `QFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm`; check it against ST's Fig. 12 at set-up |
| Q1 | ST STL6P3LLH6 | PowerFLAT 3.3 × 3.3 type F, 0.90 | 1–3 S, 4 G, 5–8 D (pad) | VDS −30 V; VGS ±20 V; RDS(on) 24/**30 mΩ** at −10 V and 38/**50 mΩ** at −4.5 V (typ./max, 3 A); VGS(th) ≥ 1 V; ID 6 A; Rthj-pcb 42.8 °C/W on 1 in² of 2 oz copper | **Project footprint** from ST's Fig. 16 (KiCad has no PowerFLAT 3.3 × 3.3) |

So `D2` and `Q1` move from "distributor summary" to `D`, and charge-path §3 is right on both. Two notes for the record:

- The TVS2200's clamp reaches 28.35 V at 125 °C after a 35 A surge, a little above the 28 V in charge-path §5.3. The conclusion does not change: only a 35–40 A surge on a hot part reaches the STUSB4500's 28 V `VDD` rating.
- The TVS2200 starts to conduct on edges faster than 2.5 V/µs (0.7 V/µs at 125 °C). TI says this does no harm unless it repeats. USB PD sources slew `VBUS` at 0.03 V/µs at most, so it never happens in normal use.

### J1 land pattern (GCT recommended layout, ±0.05)

Coordinates are in the part's frame: x along the 8.94 mm shell, y = 0 on the shell's centre line through the outer stakes, +y toward the SMT tails.

| Feature | Centres | Copper | Hole |
|---|---|---|---|
| SMT pads, six | x as above; y +1.20 (pad top at +2.20) | 2.00 tall; 0.70 wide (A5, B5), 0.76 (A9, B9), 0.80 (A12, B12) | — |
| Outer shell stakes, two | x ±4.32, y 0 | 1.10 × 1.50, plated | Slot 0.60 × 1.00 |
| Inner shell stakes, two | x ±2.30, y −1.43 | 1.60 × 1.10, plated | Slot 1.10 × 0.60 |
| Locating pegs (Ø0.55 ± 0.05) | x ±3.875, y −1.80 | None | Ø0.70 hole at −x; 1.00 × 0.70 slot at +x |

The copper spans x ±4.87, y −2.15…+2.20. The stake, 1.55–1.85 long, passes through a 1.44–1.76 board (1.6 ± 10 %), so it ends between 0.06 mm below and 0.41 mm above the +X face. Board thickness does not move the mouth, because J1 stands on the −X face, which seats on the pad.

### Envelope (measured in the droid CAD)

Survey of the droid tree built from `makad-v1.step.py` with its droid edits: 595 leaves, 40 within the region X −75…−25, Y −35…50, Z 40…95. The script is in the session scratchpad; the results are below. The droid edits touch nothing near the inlet.

| Item | World box (X; Y; Z) | Note |
|---|---|---|
| Board `PCB13_CHARGE_INLET_PCB` | −55.10…−53.50; −14.0…14.0; 56.5…71.5 | 28 × 15 × 1.6, long axis Y. −X face on the pad seat at X −55.10 |
| Holes | Ø2.2 at (Y, Z) (±11.0, 64.0) | On J1's centre line, as CP-OI-01 asks |
| J1 shell | −61.60…−55.10; ±4.47; 62.42…65.58 | Axis Y 0, Z 64. Mouth flush with the pocket floor at X −61.60 |
| Screw heads (BO-017) | X −53.5…−52.2, Ø3.8 at each hole | On the +X face |
| Parts envelope (CAD) | −53.5…−51.5; −14.0…9.0; 57.0…71.0 | +X face, 2.0 mm |
| `W16` lead reserve 1 | −53.5…−50.0; 10.0…41.0; 66.0…71.0 | Starts on the +X face over Y 10–14, Z 66–71: the solder-pad area |

Facing each face:

| Face | Nearest | Gap | What it limits |
|---|---|---|---|
| +X (parts) | PCB-02's board (its −X face) at X −49.6, over the whole of PCB-13 | **3.9 mm** from the +X copper | Parts ≤ 2.0 mm leave 1.9 mm, as D-040 has it. **PCB-02's −X face is bare in its placeholder** (its parts envelope is on +X). PCB-02 must keep it so over PCB-13's area: see *Interface to PCB-02* |
| +X, beyond | PCB-02 parts envelope X −48; frame main print X −36 | 5.5 / 17.5 | — |
| −X (J1) | Rear-panel pad (the seat) | 0 | Only J1 and its land pattern may touch; the rest of the −X face sits on print |
| Edges | Shell 2.5 mm away; chassis rear module 10.1 mm below | — | Nothing near |
| +Y end | `W16` reserve, `J2-8` plug at Y 25–37 | — | — |

**Courtyards on the +X face.** The board has 420 mm². Not usable:

- J1's land pattern, about 10 × 4.6 mm, round the four stake slots and two pegs (only stake copper on this side);
- two screw-head keep-outs, Ø3.8 head + 0.4 mm, so about Ø4.6 at (±11, 64);
- the `W16` pads, Y 10–14, Z 66–71, above the +Y screw;
- the 0.3 mm edge rule.

That leaves about 300 mm². The parts' courtyards add up to about 105 mm²:

| Parts | Courtyard (stock footprint, approx.) |
|---|---|
| U1 QFN-24 | 5.0 × 5.0 |
| Q1 PowerFLAT | 4.3 × 4.0 |
| D1, D2 | 2.6 × 2.6 each |
| C1, R2 (1206) | 4.0 × 2.2 each |
| C2, R1 (0603) | 2.3 × 1.5 each |
| C3–C5, R3–R7 (0402) | 1.9 × 1.0 each |

The test pads take another 40–65 mm² (gap 4). That fits, but at about 55–60 % fill it is the densest board yet. **Heights:** C1 (4.7 µF 50 V X7R 1206) is the tallest SMD, 1.6 ± 0.2 mm on most makers' 50 V values, so it fits under 2.0, just. Confirm the chosen part's thickness at schematic. Then come D2 at 1.1, U1 at 1.0 and Q1 at 0.9; the stake tips with solder stand under 1 mm. Every part sits under the 2.0 mm envelope. The screw heads, at 1.3 mm, are lower than the parts.

**−X face against the pad: one clash.** The pad's pin relief, `CHARGE_INLET_PIN_RELIEF`, is 9.60 × 5.60 × 1.2 mm, so it spans Y ±4.80. GCT's outer stake copper reaches Y **±4.87**. Each outer ring therefore lands 0.07 mm onto the printed seat, and so does its solder fillet on the −X side. Probes of the real land pattern against the built panel:

| Probe | Copper and mask only (0.05 thick) | With a 0.3 mm fillet |
|---|---|---|
| Outer stake rings | **0.005 mm³** | **0.032 mm³** |
| Inner stake rings | 0 | 0 |
| SMT pad row (either way up) | 0 | 0 |

The board would sit on two solder fillets, not flat on the pad. That was gap 1. D-069 widens the relief to 10.60 mm in `final/v1/cad` (`DROID_CUTS`); [`check_pcb13_relief.py`](../../final/v1/cad/check_pcb13_relief.py) now measures 0.430 mm from the copper to the wall, with no overlap in either orientation. In Z the relief clears the copper (−2.15…+2.20) by 0.6 mm either way up.

**Removal path.** The board comes off with the panel along −X; `W16` is unplugged at `J2-8` first. Nothing on the board's −X side moves relative to it, and `check_charge_inlet.py`'s 40 mm sweep of the pad and board is clean (D-040). Two things the sweep does not cover:

- **Hand room to unplug `J2-8`**: it sits at Y 25–37, 11 mm beyond the board's +Y end.
- **The `W16` loop**: the lead must reach `J2-8` while the panel is drawn out. charge-path §6 says reach in and unplug, and 150 mm gives the slack.

Neither needs a CAD change before layout.

### Power path and copper

This is the first board that carries real current. Design current is **3 A**, J1's `VBUS` rating. The normal current is 0.84–0.95 A at 15 V and at most 1.38 A, the BQ25798 input clamp (charge-path §5.2). Voltage is at most 20 V (blank NVM) and 28 V in a surge.

| Item | At 1.38 A | At 3 A | Rule |
|---|---|---|---|
| Track width, outer layer, IPC-2221, 1 oz | 0.47 mm (ΔT 10 °C) | **1.37 mm** (ΔT 10 °C); 0.90 mm (ΔT 20 °C) | `VBUS`/`VSNK`/`GND` as pours ≥ 2 mm wide; no power track below 1.4 mm |
| Same, 2 oz | — | 0.69 mm (ΔT 10 °C) | Not needed (gap 3) |
| Vias −X ↔ +X (0.35 hole, about 20 µm plating; ≈ 1.7 A each, taken as 1 A) | 2 | **≥ 4 per net** for `VBUS`, and ≥ 4 for `GND` beside the shell stakes | Stakes and their plated slots also join the two `GND` layers |
| Q1 loss, RDS(on) maximum × 1.5 for a hot junction | 0.14 W at 9 V (75 mΩ); 0.09 W at 15 V (45 mΩ) | 0.68 W at 9 V; 0.41 W at 15 V | Drain pad on a `VSNK` pour on both layers. At 3 A and 9 V, about 60 °C rise on ≈ 80–100 °C/W, which is acceptable for a case that is not a normal one |
| Copper, `VBUS` + `GND` loop, ≈ 20 mm of 2 mm pour each | ≈ 10 mΩ | 90 mW | — |
| `W16` 2 × AWG22, 150 mm (52.9 mΩ/m) | 16 mΩ, 30 mW | 0.14 W | Micro-Fit 3.0 AWG22 crimp 8.5 A maximum (05-harness) |
| R2 470 Ω 1206 anti-surge (DISCH) | 0.48 W pulses up to 756 ms (§3) | — | ERJ-P08 class (0.66 W), as specified |
| Spacing at ≤ 30 V | — | — | IPC-2221 B2: 0.1 mm; the fab-neutral 0.16 mm rules |

**Copper weight: 1 oz on both outer layers, two layers, 1.6 mm** (recommended, gap 3). 3 A fits in pours on 1 oz, and the [fab-neutral rules](../README.md#fab-neutral-design-rules) are written for 1 oz. 2 oz would put the QFN-24's 0.5 mm pitch (0.2–0.25 mm gaps) at the fabs' 2 oz spacing limits, and it costs more for nothing. 1.6 mm is fixed by the 1.70 mm stake and the screw engagement: 5 − 1.76 = 3.24 mm at +10 %, which is still ≥ 3.0. So the standard ±10 % thickness is fine and need not be stated on the order.

### NVM test pads and programming jig (CP-OI-05 plan)

Program before PCB-13 goes on the panel (charge-path §8). The STUSB4500's NVM is written over I²C with the chip powered from `VDD`. A plain 5 V on `VBUS` is enough; no PD contract is needed.

- **Pads (10).**
  - Programming: `VBUS`, `GND`, `SCL`, `SDA`, `RESET`.
  - Bench probing: `VSNK`, `CC1`, `CC2`, `ATTACH`, `POWER_OK2`.
  - All are on the +X face. `ALERT`, `GPIO`, `POWER_OK3` and `A_B_SIDE` have no connection.
  - `SCL`, `SDA`, `ATTACH` and `POWER_OK2` are open-drain or input-only, with no pull-ups on the board. The jig supplies 3.3 V pull-ups; these pins are rated 6 V at most. `RESET` keeps its 100 kΩ to GND (R7), so the jig can drive it high.
- **Pitch (gap 4).** Spec §3 says a 1.27 mm grid. Recommended: **2.54 mm, Ø1.0 pads**, for P75-series pogo pins (Ø1.02 barrel), which are common in India (Robu, Evelta). P50 pins for 1.27 mm are fragile and harder to buy. A 2 × 5 block takes about 12.7 × 5.1 mm. If it doesn't fit whole, the five programming pads stay on the 2.54 grid and the five probe pads may sit anywhere.
- **Jig.** A printed base with a pocket for J1, which hangs 6.5 mm below the board, and two Ø2.0 pins through the M2 holes. A printed top plate carries the pogos and locates on the same two pins. J1 standing on the base takes the pogo force.
  - **Host:** a bench Raspberry Pi on 3.3 V I²C (smbus2), or the ST STSW-STUSB002 GUI.
  - **Script:** writes the five NVM banks from the image, power-cycles the chip by switching 5 V off and on, then reads all banks back and compares them byte for byte (CP-01).
  - The image file and its checksum go beside charge-path.md (CP-OI-05).
  - The jig is drawn after layout, because it needs the pad positions.

### India sourcing (CP-OI-04, PCB-13 parts)

Checked 2026-10-28. element14 India counts as an India source; Mouser India is the next best.

| Part | India source | Stock / price | LCSC (JLCPCB) |
|---|---|---|---|
| USB4140-GF-0170-C | element14 India **3955430** | 157, US stock, 5–7 days; ₹74.99 (1+). Order code 3973078 is the same part, lead time only | C5452033: JLCPCB 0, LCSC 8; "assembly difficulty High" |
| STUSB4500QTR | element14 India **2980889** | 5,554, UK stock, 4–6 days; ₹226.95 | C2678061: 4,494, Extended |
| STL6P3LLH6 | element14 India **3132757** | 1,602, UK stock; ₹79.55 (5+, multiples of 5) | C457492: 1 in stock |
| ESDA25W | element14 India **2341655** | 25,148, UK stock; ₹40.97 (5+), ₹20.60 (10+) | 3,340 |
| TVS2200DRVR | **Not at element14 India.** Mouser India 595-TVS2200DRVR | 527; US$1.41 (1+), US$0.877 (10+) | **No genuine TI part.** Only clones carry the name: ElecSuper, Wuxi Maxinmicro, Leiditech, with other clamp ratings. Not accepted |
| Passives, 0402–1206 | Fab stock (JLCPCB basic and extended parts) | — | — |

So the actives are bought in India (D-069): J1 by the builder, who solders it; the other four are consigned to the fab, as on PCB-06 and PCB-10. JLCPCB's own stock can't build even one board: USB4140 0, STL6P3LLH6 1, and no genuine TVS2200. CH-041's BQ25798 and Würth inductor belong to PCB-02, so CP-OI-04 stays open for them.

### Interface to PCB-02 (fixed here)

| Item | Value |
|---|---|
| Connector | `W16`: 2 × AWG22, 150 mm, soldered to PCB-13, Micro-Fit 3.0 43025-0200 receptacle with 43030 female terminals at the PCB-02 end, into **`J2-8`** (43045-0200 class, right angle) on PCB-02's +Y edge, plug exiting +Y |
| **Pin order** | **`J2-8` pin 1 `VSNK`, pin 2 `GND`** (05-harness §5, confirmed). PCB-13's solder pads: **P1 `VSNK`, P2 `GND`**; final pad positions at layout. Wire colours red = `VSNK`, black = `GND` |
| `VSNK` voltage | 0 V until a contract exists (Q1 off; `POWER_ONLY_ABOVE_5V`). 9 or 15 V in normal use. 20 V on a blank NVM. Surges up to the TVS2200 clamp, 28.35 V maximum (PCB-02 parts ≥ 30 V absolute maximum; 50 V capacitors, as §4) |
| `VSNK` current | 0.84–1.38 A normal (BQ25798 input clamp); design 3 A (J1 rating) |
| Turn-on | Q1 ramps with τ ≈ 2.5 ms (R3 ∥ R4 × C5), so PCB-02's 2 × 10 µF + 100 nF input draws about 0.15 A |
| Turn-off | U1 `DISCH` bleeds `VSNK` through R2 470 Ω on PCB-13: 32 mA at 15 V, for up to 756 ms after a detach or PDO step-down |
| No other signals | No D+/D−, CC or status on `W16`. PCB-02 ties its own D+ to D− (charge-path §4) |
| PCB-02 mechanical | PCB-02's −X face is 3.9 mm from PCB-13's +X face over Y −14…14, Z 56.5…71.5 (world). **Over that area PCB-02 may carry no parts on its −X face, and no through-hole tails longer than 1.0 mm** (PCB-05 trap: Micro-Fit THT tails stand 1.6 mm proud). That keeps at least 0.9 mm to PCB-13's 2.0 mm parts |

### Gaps (settled 2026-10-29, D-069)

1. **Pin relief in the rear-panel pad.** GCT's outer stake rings land 0.07 mm on the printed seat (measured above). Recommended: **widen the relief from 9.60 to 10.60 mm** (Y ±5.30). That leaves 0.43 mm beyond the copper for a fillet, with 4.9 mm to the screw pilots. Keep 5.60 × 1.2 in Z and depth. This is a droid CAD change: a `DROID_CUTS` entry on `REAR_SERVICE_PANEL_OCTAGONAL` in `final/v1/cad/makad-v1.step.py`, plus a new `check_pcb13_relief.py`. The check probes the GCT land pattern and fillets against the panel, checks the panel stays one solid with the relief walls clear, and plants a clash to prove the probes work. It needs a decision entry.
2. **J1 assembly.** J1 is alone on the −X face, so the board is two-sided. Options:
   - (a) **The fab assembles both sides**, with J1 consigned (recommended). JLCPCB's two-sided assembly is its Standard service, not Economic.
   - (b) The fab assembles +X; the builder hand-solders J1 (six SMT tails plus four stakes from the +X side).
3. **Copper:** 1 oz, two layers, 1.6 mm (recommended), or 2 oz.
4. **Test-pad pitch:** 2.54 mm for P75 pogos (recommended), or charge-path §3's 1.27 mm.
5. **Sourcing:** the four ST/GCT actives from element14 India and the TVS2200DRVR from Mouser India, consigned to the fab (recommended). Mouser India ships DDP only on a GST business invoice; on a card invoice, duty is paid at delivery.

**Settled (D-069):**

1. Relief **10.60 mm**: `PCB13_RELIEF` in `DROID_CUTS`; `check_pcb13_relief.py` 13/13, the planted old relief caught.
2. **J1 hand-soldered by the builder.** The fab assembles the +X face only, so the order can be single-sided. At layout, J1 is excluded from the fab BOM and the position file. Its six SMT tails reach 0.62 mm past the shell (pad top at +2.20, shell at +1.58), so an iron can reach them. Solder the stakes from the +X side.
3. **1 oz, two layers, 1.6 mm.**
4. **2.54 mm test-pad grid**, Ø1.0, P75 pogos.
5. **element14 India** for USB4140, STUSB4500, STL6P3LLH6 and ESDA25W, and **Mouser India** for TVS2200DRVR. All but J1 are consigned.

## Schematic

[`design/pcb-13-charge-inlet.kicad_sch`](design/pcb-13-charge-inlet.kicad_sch), with a PDF print, [`pcb-13-charge-inlet-schematic.pdf`](design/pcb-13-charge-inlet-schematic.pdf). It is one A3 sheet, written for the KiCad 10.99 nightly. As on PCB-05 and PCB-10, every pin end carries a short wire and a local label, nets join by label name, and the notes sit in one block at the bottom left.

**Project set-up.**

| File | Holds |
|---|---|
| `pcb-13-charge-inlet.kicad_pro` | PCB-06's two-layer project, renamed: the fab-neutral board minimums and the default net class |
| `pcb-13-charge-inlet.kicad_dru` | The fab-neutral rules ([D-062](../../decisions.md#d-062)), copied from PCB-15 |
| `sym-lib-table`, `pcb13.kicad_sym` | Project symbol library `pcb13`, all three flattened from stock bodies, so ERC sees no library mismatch: <br>• **`TVS2200DRV`**: the stock symbol derives from `TVS0500DRV`, so the base body is embedded with TVS2200's fields (the playbook's derived-symbol trap). Pins 1–3 and 7 (pad) GND, 4–6 IN. <br>• **`ESDA25W`**: KiCad has no ESDA25W, so it uses `SP0502BAHT`'s body (dual common-anode TVS: 1, 2 cathodes, 3 anode) with the SOT-323 footprint and ST's fields. <br>• **`STL6P3LLH6`**: `SiS415DNT`'s P-FET body; pins 1–3 S (stacked), 4 G, 5 D, which is ST's pinout |
| `fp-lib-table`, `pcb13.pretty/` | Three project footprints, below |
| Stock parts | `Interface_USB:STUSB4500QTR`, whose pins match DS12499 Table 1 one for one, EP = 25 GND. `Connector:USB_C_Receptacle_PowerOnly_6P` (A5, A9, A12, B5, B9, B12, SH). Footprints `QFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm`, `WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm`, `SOT-323_SC-70`, 0402–1206 passives, `TestPoint_Pad_D1.0mm`, `MountingHole_2.2mm_M2` |

**Project footprints** (`pcb13.pretty/`):

- **`GCT_USB4140-GF-0170-C`**: GCT's recommended layout (drawing A3, 29/08/24), as tabled in *J1 land pattern*. Six SMT pads, B12 B9 A5 B5 A9 A12. Four plated slots, all numbered `SH`: 1.10 × 1.50 copper round a 0.60 × 1.00 slot at x ±4.32; 1.60 × 1.10 round 1.10 × 0.60 at x ±2.30, y +1.43. The two peg holes are NPTH: Ø0.70, and a 1.00 × 0.70 slot. F.Fab draws the 8.94 × 3.16 shell. The courtyard is 10.3 × 4.9. J1 goes on B.Cu at layout (the −X face). No 3D model yet: lesson 5 builds one from the drawing.
- **`ST_PowerFLAT-3.3x3.3_TypeF`**: ST's Fig. 16.
  - Drain pad `5`: 2.45 × 2.40 with two 0.53 × 0.40 side tabs, and four paste windows (about 65 %).
  - Pads 1–4: 0.40 × 0.75 at 0.65 pitch, 0.65 mm below the drain pad, 3.80 overall.
  - No 3D model yet (lesson 5).
- **`W16_SolderPads_2x_AWG22`**: two 3.2 × 1.6 mm lap pads 2.5 mm apart, 1 `VSNK`, 2 `GND`. No paste, so they are left out of the BOM and position files: the builder solders the lead. Wires lie along the pad, toward +Y in the robot. **Strain relief: a silicone bead, gap 6 (a).**

**Footprints on a scratch board** (playbook set-up step, 2026-10-29):

- Every footprint above sat on a scratch board with this board's `.kicad_dru` copied under the scratch name, which is the PCB-06 trap. The pads carry their real nets: with no nets, DRC skips pad pairs and proves nothing.
- **No clearance, hole or mask violation in any footprint.** GCT's 1.00 mm oval peg slot comes closest: it clears the inner stake copper by 0.33 mm. Both ends are rounded, so this is above the 0.31 mm hole rule, not the 0.275 a straight-edge sum gives.
- **Planted:** a via 0.20 mm from another net's pad was caught by `fab-neutral via to other copper` (0.31), so the custom rules were live.
- The remaining warnings are stock reference text at 0.15 mm stroke; `kp.refs_to_fab()` handles them at layout.
- Every stock footprint's 3D model file exists on disk (PCB-05 trap).
- Stock QFN-24 against ST's Fig. 12: KiCad's pads are 0.825 long against ST's 0.6. They run 0.175 further out (toe) and keep 0.20 to the 2.70 exposed pad. Kept.

**Circuit** (references as drawn; charge-path §3 unchanged except R1):

| Ref | Part | Nets |
|---|---|---|
| J1 | GCT USB4140-GF-0170-C, hand-soldered by the builder (D-069) | A9, B9 `VBUS`; A12, B12, SH `GND`; A5 `CC1`; B5 `CC2` |
| D1 | TVS2200DRVR | IN (4–6) `VBUS`; GND (1–3, 7) |
| C1 | 4.7 µF 50 V X7R 1206, Samsung CL31B475KBHNNNE (1.6 ± 0.2 mm: the tallest part) | `VBUS`–`GND` |
| D2 | ESDA25W | 1 `CC2`, 2 `CC1` (swapped at placement), 3 `GND` |
| U1 | STUSB4500QTR | 1 CC1DB + 2 CC1 → `CC1`; 4 CC2 + 5 CC2DB → `CC2` (dead battery); 6 `RESET`; 7 `SCL`; 8 `SDA`; 9 `DISCH`; 10, 22 (VSYS), 25 (EP) `GND`; 11 `ATTACH`; 12 `ADDR0`; 13 `ADDR1`; 16 `EN_SNK`; 18 `VS_DISCH`; 20 `POWER_OK2`; 21 `VREG_1V2`; 23 `VREG_2V7`; 24 VDD `VBUS`. No connection: 3 NC, 14 POWER_OK3, 15 GPIO, 17 A_B_SIDE, 19 ALERT |
| C2 | 1 µF 50 V X7R 0603 (CL10B105KB8NNNC) | U1 VDD (`VBUS`)–`GND` |
| C3, C4 | 1 µF 10 V 0402 (CL05A105KP5NNNC) | `VREG_1V2`, `VREG_2V7` |
| R1 | **1 kΩ 0805 anti-surge, Panasonic ERJ-P06J102V** (was 0603) | `VBUS`–`VS_DISCH` |
| R2 | 470 Ω 1206 anti-surge, ERJ-P08J471V | `DISCH`–`VSNK` |
| Q1 | STL6P3LLH6 | S (1–3) `VBUS`, G (4) `GATE`, D (5) `VSNK` |
| R3, C5, R4 | 100 kΩ 0402; 100 nF 50 V 0603 (CL10B104KB8NNNC); 33 kΩ 0402 | `VBUS`–`GATE`; `VBUS`–`GATE`; `GATE`–`EN_SNK` |
| (R5–R7) | Deleted at placement | `ADDR0`, `ADDR1`, `RESET` tied straight to `GND` at the QFN (address 0x28); see *Layout* |
| J2 | `W16` lap pads | 1 `VSNK`, 2 `GND` → PCB-02 `J2-8` 1, 2 |
| TP1–TP4 | Ø1.0 pads, 2.54 mm grid (P75 pogos), not in the BOM | `VBUS`, `GND`, `SCL`, `SDA` (programming; TP5 `RESET` deleted at placement) |
| TP9, TP10 | Ø1.0 pads, not in the BOM | `ATTACH`, `POWER_OK2` (probing; TP6–TP8 deleted at placement: `VSNK` on J2 pad 1, CC on D2's leads) |
| H1, H2 | Ø2.2 holes | M2 × 5 screws (BO-017); no net |

**R1, rated at last.** At 20 V, `VBUS_VS_DISCH` draws 20 mA through R1, which is **0.4 W** in R1. That happens during every discharge: on detach, on a PDO step-down, and after a hard reset. The 50 mA pin limit was checked in charge-path §3, but R1's own dissipation was not. A standard 0603 is rated 0.1 W (about 0.25 W for 5 s as an overload). The ERJ-P06 anti-surge 0805 is rated 0.5 W. ST's Fig. 9 also spreads this path over two resistors (470 Ω + 1 kΩ). Recorded in charge-path §3 and as a D-069 amendment.

`PWR_FLAG` sits on `VBUS` (enters on J1) and `GND`. `VSNK` has no power-input pins, so it needs none. The two holes carry no net.

**ERC** (nightly `kicad-cli sch erc --severity-all`, 2026-10-29): **0 errors, 0 warnings.**

**Check against the inputs**, from the exported netlist (2026-10-29): **all 18 nets match charge-path §3 pin for pin.** After the placement changes (*Layout*), 15 nets remain and all match; ERC is still 0/0. The nets are `VBUS` (15 pins), `GND` (20), `VSNK`, `CC1`, `CC2`, `GATE`, `EN_SNK`, `VS_DISCH`, `DISCH`, `VREG_1V2`, `VREG_2V7`, `SCL`, `SDA`, `RESET`, `ADDR0`, `ADDR1`, `ATTACH` and `POWER_OK2`. The only one-pin nets are U1's five no-connects.

### Gap 6 (settled 2026-10-29: option a): `W16` strain relief

charge-path §3 says `W16` is "tied through two slots". A cable tie through two slots wraps round the board, so its strap would cross the −X face. That face sits flat on the printed pad, so the board would rock on the tie, as it would have on the stake fillets (gap 1). There is also little room: the pads fill Y 10–14, Z 66–71 above the +Y screw head, and slots would sit within 0.5 mm of the board edge.

| Option | What it needs |
|---|---|
| **(a) Lap pads + a bead of neutral-cure silicone (or hot-melt) over the joints and 5 mm of insulation, on the +X face** (recommended) | No CAD change. The bead stays inside the `W16` reserve: 3.5 mm from the board face, 0.4 mm short of PCB-02. `J2-8` is unplugged by its housing and latch, so the lead itself carries little pull |
| (b) The tie, as in D-040, through two NPTH slots | A 1.2 mm groove in the pad under the strap (`DROID_CUTS`, added to `check_pcb13_relief.py`). It also takes board area at the +Y end and leaves thin webs at the edge |

## Board set-up

[`design/pcb-13-charge-inlet.kicad_pcb`](design/pcb-13-charge-inlet.kicad_pcb), with no parts yet; they arrive with F8 at lesson 4.

**Coordinates.**
- The board is seen from its F face, the parts face, which is world +X (toward PCB-02). World +Y is then to the right and +Z up.
- KiCad x = 114 + Y, y = 171.5 − Z. Board-local u = x − 100 (= Y + 14) and v = 115 − y (= Z − 56.5). The aux and grid origins sit at local (0, 0), the bottom-left corner in KiCad's view.
- B.Cu is the −X face, seated on the rear-panel pad; J1 is the only part there. KiCad's STEP puts the F face at +Z, which becomes world +X.

| Feature | World (Y, Z) | KiCad (x, y) | Note |
|---|---|---|---|
| Outline | Y −14…14, Z 56.5…71.5 | 100…128, 100…115 | 28 × 15 |
| J1 (on B.Cu) | (0, 64) | (114, 107.5) | Shell along x. Its pad row sits 1.2 mm above or below the centre, chosen at placement; both orientations are proved below |
| H1, H2 (Ø2.2, M2 × 5) | (∓11, 64) | (103, 107.5), (125, 107.5) | Stock `MountingHole_2.2mm_M2`: its Ø4.9 courtyard covers the Ø3.8 screw head, so courtyard DRC keeps parts off the head |
| J2 (`W16` lap pads) | Y 10.4…13.6, Z 66.5…71.0 | origin (126.0, 102.7), rot 0 | Inside the `W16` reserve (Y 10–14, Z 66–71); pad 1 `VSNK` on top; wires leave +x. Its courtyard clears H2's by 0.05 mm |
| Pad relief (B face) | Y ±5.30, Z 61.2…66.8 | 108.7…119.3, 104.7…110.3 | D-069; J1's courtyard (10.3 × 4.9) lies inside it with 0.15/0.35 mm to spare |

**Set-up.**

| Item | Value |
|---|---|
| Stackup | Two layers, **1.6 mm** (FR-4 core 1.51), 1 oz (35 µm) copper both sides (D-069). PCB-06's two-layer stackup with the core thickened, because no earlier board had 2 layers at 1.6 mm. **Vias tented on both faces**, so the B face stays flat under mask on the printed seat |
| Rules | `pcb-13-charge-inlet.kicad_dru`: the fab-neutral set, copied from PCB-15 |
| `B_SEAT_LEFT/RIGHT/TOP/BOTTOM` | B.Cu rule areas over the whole B face except the relief: **no footprints**. Tracks, vias and pads (J1's slots, through-hole rings) stay allowed: tented copper is flat |
| `F_SCREW_HEAD_1/2_NO_VIAS` | F.Cu, Ø4.4 round each hole: **no vias** under the screw heads, so they seat on flat mask. Tracks allowed |
| User.1 `Panel.Relief` | The 10.60 × 5.60 relief outline |
| User.2 `Screw.Heads` | The Ø3.8 heads |
| User.3 `W16.Reserve` | The lead reserve and exit direction |
| User.4 `F.Ceiling` | Parts ≤ 2.0 mm on F; PCB-02's bare back face 3.9 mm away. KiCad has no height rule, so the lesson 5 fit check measures it |
| User.5 `J1.Shell` | The 8.94 × 3.16 shell on B |

**DRC** (nightly `kicad-cli pcb drc --severity-all`, 2026-10-29): the empty board gives **0 violations**.

**Fixed parts and rule areas proved** on scratch copies with their own `.kicad_pro`/`.kicad_dru` (PCB-06 trap):
- **Fixed parts at their CAD places** (PCB-10 trap, real footprints with real nets): J1 on B, both ways round, plus H1, H2 and J2. Result: **no courtyard, keep-out, clearance or hole violation**. The only flags were back-side text warnings from the hand-made flip; F8 and a real flip mirror the text.
- **Planted, all caught:**
  - a via 1.9 mm from H1's centre (`F_SCREW_HEAD_1_NO_VIAS`);
  - an 0402 on B over the seat (`B_SEAT_LEFT`);
  - a 0.12 mm track (`fab-neutral track width`).
- **Planted, correctly passed:** an 0402 on F in open space.

**Area left for placement on F** (lesson 1 budget): about 300 mm² after J1's stake rings, the two head courtyards, J2 and the edge rule. The parts' courtyards take about 105 mm², and the test pads 40–65 mm² (TP1–TP5 on the 2.54 mm grid).

**Next (lesson 4).** The builder opens `pcb-13-charge-inlet.kicad_pro` in the **nightly**, opens the PCB editor, presses **F8** (Update PCB from Schematic) and saves. The layout then starts with `tools/kp.py`:
- flip J1 to B at (114, 107.5);
- place H1, H2 and J2 at their proved origins;
- then place by group: protection at J1 (D1, C1, D2 within 3 mm), Q1 and its gate parts, U1 and its capacitors, the test pads last;
- leave J1, J2 and the test pads out of the position files.

## Layout

Placed and routed 2026-10-29 with [`tools/kp.py`](../tools/kp.py) in the open nightly, after the builder's F8. The design is two layers at 1.6 mm, 1 oz. No autorouter was used: every track was placed by hand and is 0°, 45° or 90° (`kp.track()` refuses anything else).

**Floor plan, and why the first two failed.** The deciding fact is that U1's pads span 4.75 mm, and every side of the QFN has used pins.

1. **U1 below J1:** between J1's stakes and the board edge, the pads came within 0.03 mm of the 0.3 mm edge rule. Five signal pins faced the edge with no room for a track, and a track can't pass between 0.5 mm-pitch pads.
2. **U1 above J1 with J1's pad row up:** U1's I²C side faced Q1 and its `VBUS` feed, and the CC lines crossed.
3. **Final:**
   - **J1 on B at rot 0**, pad row down: CC1 at x 113.5 and CC2 at x 114.5, the same order as U1's CC pins. The inner stakes and pegs are up.
   - **U1 at rot 90 in the top band** (114.0, 103.05). Its CC side faces J1, its `VDD`/`VREG` side faces the capacitors on the left, and its I²C/DISCH side faces the test pads on the right. The side toward the top edge (pins 13–18) has only three used pins.
   - **Q1 at the bottom right**, so the 3 A path is J1 → back bar → 4 vias → front pour → Q1 → right-edge strip → J2.

**Schematic changes made at placement** ([D-069](../../decisions.md#d-069) amended; ERC 0/0; the netlist matches on all 15 nets):

| Change | Why |
|---|---|
| **ADDR0, ADDR1 and RESET tied straight to GND** at the QFN (pins 12, 13, 6 by stubs to the exposed pad); **R5–R7 deleted** | All three are corner pins with no room for an exit track. ST: "to ground if no MCU". The address stays 0x28. NVM programming over I²C does not need RESET: the jig cycles the 5 V |
| **TP5 (RESET), TP6 (`VSNK`), TP7/TP8 (CC1/CC2) deleted** | RESET is now GND. `VSNK` is probed on J2 pad 1. There is no room beside the CC vias; CC is scoped on D2's leads, or with an inline PD tester as bench CP-02 uses |
| **D2 pins swapped**: 1 `CC2`, 2 `CC1` | The ESDA25W's two diodes are identical with a common anode. The swap lets D2's GND lead face outward to its own via |
| **J2 turned 180°**: pad 1 `VSNK` now lower (126.0, 103.95), pad 2 `GND` upper | The `VSNK` strip comes up the right edge. The pin numbers and the `J2-8` order are unchanged |

**Placement** (KiCad mm; board 100–128 × 100–115):

| Group | Parts |
|---|---|
| Fixed | J1 (114, 107.5) B rot 0; H1 (103, 107.5), H2 (125, 107.5); J2 (126.0, 102.7) rot 180 |
| U1 and support (top left) | U1 (114.0, 103.05) rot 90; C3 (110.2, 102.8) and C4 (110.2, 103.8), the `VREG` capacitors, 1.3 mm from their pins; C2 (108.3, 104.0) at `VDD`; R1 (108.5, 101.1) on `VS_DISCH`; TP10 `POWER_OK2` (106.4, 103.3) |
| Programming block (top right, 2.54 mm grid) | TP1 `VBUS` (119.6, 102.95), TP2 `GND` (122.14, 102.95), TP3 SCL (119.6, 105.49), TP4 SDA (122.14, 105.49); TP9 `ATTACH` (119.6, 100.9) |
| CC protection (over J1) | D2 (111.6, 108.4) rot 180, 1.3 mm from the CC vias |
| `VBUS` protection (bottom left) | D1 TVS2200 (110.6, 111.6), C1 (107.6, 112.4) rot 90, both within 3 mm of J1's `VBUS` pads |
| Switch and bleed | Q1 (124.9, 112.4) rot 270, source left, drain right; R2 (120.9, 108.9) rot 270, `DISCH` top, `VSNK` bottom; R3 (121.2, 113.6), C5 (119.3, 113.4), R4 (117.5, 113.6), standing along the bottom edge |

Fine margins found: U1's corner pads clear J1's inner stake rings by 0.20 mm; TP3 clears the right peg by 0.45 mm and the stake ring by 0.24 mm; TP4's courtyard clears H2's by 0.05 mm; J2's clears H2's by 0.05 mm.

**Routing.**

| Net | Route |
|---|---|
| `VBUS` (3 A) | J1 A9/B9 (B) → `VBUS_B_BAR` pour below the pad row → **4 vias** (112.6–115.6, 111.3) → `VBUS_F` pour across the bottom band → Q1 source, D1, C1, C5, R3. The narrowest poured section between the vias and Q1 is **2.41 mm** (needs 1.37 at ΔT 10 °C) |
| `VSNK` (3 A) | Q1 drain → `VSNK_F` pour up the right edge, past H2's hole → J2 pad 1. The strip between the hole's 0.31 mm keep-out and the 0.3 mm edge rule is **1.29 mm** wide and about 4 mm long: IPC-2221 gives 2.9 A at ΔT 10 °C. At the real 1.4 A it is a fraction of that |
| `GND` | Solid `GND_B` plane over the whole B face. It is cut only by the `VBUS` bar and two thin tracks right of J1, and joins J1's GND pads and four stakes directly. `GND_F` fills the rest of F. Vias: 4 in U1's exposed pad, one for each of the capacitor group, D2, D1 (in its pad), C1 and TP2, and 2 in J2's GND lap pad. All vias are tented |
| `VDD`, `R1` feed | `VBUS` 0.3 mm from D1 up the left channel between H1 and J1's left stake, to C2, then U1 pin 24; a branch to R1 |
| CC1, CC2 | J1 pads (B) up 0.8 mm to vias at (113.5/114.5, 106.9). On F, up to U1 pins 1–2 and 4–5 (each pair joined at its tips) and down to D2. No crossing |
| SCL, SDA, DISCH, ATTACH | Out of U1's right side in lanes at y 104.95, 104.4, 103.85 and 102.3/101.3, to TP3, TP4, R2 (down the gap left of H2) and TP9. The SCL lane clears the peg by 0.32 mm |
| `EN_SNK`, `VS_DISCH` | The single 0.16 mm lane above U1: `VS_DISCH` left to R1; `EN_SNK` right to a via at (117.3, 100.9), down the B face right of J1, then up to R4 |
| `GATE` | One bus along y 114.3: R4 → C5 → R3 → Q1 pin 4 |
| TP1 `VBUS` | B track right of J1 (x 119.2), via at (119.0, 102.15) |

Track widths: 0.16 mm on slow signals, 0.2 mm on CC and `GATE`, 0.25–0.3 mm on `VDD`, `VREG` and the grounds, pours on the power path.

**DRC** (nightly `kicad-cli pcb drc --schematic-parity --severity-all`, 2026-10-29):
- **0 errors, 0 unconnected pads, schematic parity clean.**
- The 10 warnings left are all `lib_footprint_mismatch` on the ten rotated footprints. That is the playbook's 1 nm round-off trap; the unrotated C1 and D1 are not flagged.

The reference text moved to the fab layers with `kp.refs_to_fab()`. J1, J2 and the test pads are excluded from the position files (`kp.exclude_from_pos`): J1 is fitted by the builder, and J2 and the test pads are bare copper.

**Trap found on this board.** KiPy's `Zone.is_rule_area` is a method. Testing `not z.is_rule_area` is always False, so the "remove the old pours" step removed nothing and every rerun added another copy of each pour (three of each before it was caught). Call `z.is_rule_area()`, and count the zones after every routing run.

## Log

- **2026-10-28 — Lesson 1, inputs.**
  - Read all five makers' datasheets: GCT direct; TI direct; ST via mirrors of ST's own PDFs. **CP-OI-03 closed**: ESDA25W and STL6P3LLH6 confirmed, now `D`.
  - Measured the envelope in the droid tree. The pin relief is 0.07 mm short of GCT's outer stake copper (gap 1). PCB-02's −X face must stay bare over PCB-13.
  - Sized the power path for 3 A: 1 oz pours ≥ 2 mm, ≥ 4 vias per net.
  - Planned the NVM pads and jig.
  - Checked India sourcing for all five actives: JLCPCB stock can't build the board, and LCSC has no genuine TVS2200.
  - Fixed the `W16`/`J2-8` interface for PCB-02.
  - Gaps 1–5 raised.
- **2026-10-29 — Inputs frozen ([D-069](../../decisions.md#d-069)).** Builder: relief widened (gap 1), J1 hand-soldered (gap 2), 1 oz two layers (gap 3), 2.54 mm P75 pads (gap 4), element14 India and Mouser India (gap 5). `DROID_CUTS` relief plus `check_pcb13_relief.py` 13/13. BO-015 sources updated.
- **2026-10-29 — Lesson 2, schematic.**
  - Project set up; three flattened project symbols and three project footprints.
  - ERC 0/0; the netlist matches charge-path §3 on all 18 nets.
  - All footprints DRC-clean on a scratch board with the rules (planted via caught); every stock model file present.
  - R1 moved to a 0805 anti-surge part: 0.4 W at 20 V, not rated before.
  - Gap 6 raised: the `W16` tie would cross the seated −X face.
- **2026-10-29 — Gap 6 settled** (builder: "whatever is recommended"): option (a). `W16` is lap-soldered to J2 and held by a bead of neutral-cure silicone over the joints and 5 mm of insulation on the +X face. No tie and no slots, so no CAD change. D-069 amended.
- **2026-10-29 — Lesson 3, board set-up.**
  - Outline 28 × 15 mm, origins at local (0, 0), two layers at 1.6 mm, vias tented.
  - Rule areas: B face no footprints outside the relief; no vias under the screw heads.
  - Envelope drawn on User.1–5.
  - Empty-board DRC 0. Fixed parts (J1 on B both ways round, H1, H2, J2) DRC-clean at their CAD places; every planted violation caught.
- **2026-10-29 — Lesson 4, layout.**
  - Placed after two failed floor plans (U1 has no room below J1). D-069 amended: ADDR0/ADDR1/RESET to GND (R5–R7 out); TP5–TP8 out; D2 inputs swapped; J2 turned 180°.
  - Routed by hand, octolinear. `VBUS`/`VSNK` as pours: narrowest 2.41 mm and 1.29 mm.
  - DRC 0 errors, 0 unconnected, parity clean; 10 round-off warnings on rotated footprints.
  - New trap: KiPy `is_rule_area` is a method; duplicate pours removed.
