# Peripheral selection: audio, status light, base IMU

| Field | Value |
|---|---|
| Status | **Selected 2026-09-26 as working choices** (same standing as RP-01 `ACT-01`): parts, interfaces and CAD are fixed; bench proof, builder dated acceptance and purchase remain. No gate registered |
| Closes | RP-06 TODO "Select the status LED and diffuser/optic", "Select microphone front end, microphone boards, speaker, and amplifier", "ICM-42688-P IMU breakout"; RP-05 `BD-A04`…`A06`; RP-03 base-IMU SKU row; RP-01 `M007` article |
| CAD | Body [Layout 02](body-chassis/layout-02/README.md) `RP03-CAD-11`; head [Layout 04](head/layout-04/README.md) `HEAD-CAD-12` |
| Research | Exa web search 2026-09-26; stock and prices are a snapshot |

Evidence tags follow the project: `D` datasheet or vendor page, `E` estimate, `U` unknown until measured.

## 1. Criteria used

| Source | What it demands |
|---|---|
| RP-05 [`audio-requirements.md`](../RP-05-interaction/audio-requirements.md) `AR-01…07`, `AR-30…36`, `AR-50…54`, `AR-60…65` | Four synchronized body mics at the Layout 02 ports; a real front end (Pi 5 has no 4-ch PDM); GPIO18–21 only, no UART theft; no back-power; body speaker in the reserved 50 mm / 34 mm cavity; duplex with a recoverable speaker↔mic time relation; rigid array; serviceable modules |
| RP-05 [`audio-path.md`](../RP-05-interaction/audio-path.md) §3 | Seven reject rules; a family is chosen by applying them, not by preference |
| RP-02 [`board-specs.md`](../RP-02-electrical/board-specs.md) `PB-AUDIO-OUT` | 5 V rail through `TPS259474L` at 2.0 A; RP-05 must supply amp supply range, RMS/crest current, idle/shutdown current, pop behaviour, mute default **off**, enable source, EMI, ripple budget |
| RP-02 `CA-06` | Pi GPIO18–21 reserved for audio; UART0 GPIO14/15, UART2 GPIO4/5, I²C1 GPIO2/3 untouchable |
| RP-03 [`sensing-screen-01.md`](../RP-03-locomotion/sensing-screen-01.md) `S07`, `BD-03` | ICM-42688-P, **SPI + INT1 to the silicon**, 10 ms data-ready age, rigid base mount, not in the head; UART-angle modules and I²C-only boards rejected |
| `SCOPE-17`, `SC-21`, `SC-TBD-19`; `LIGHT_STATE`/`LIGHT_REPORT`; `CA-04` | At least one controllable, colour-capable LED beside the camera; D1 executes it (C2 relays); onset reported; no unacceptable camera contamination (RP06-G03) |
| Head Layout 04 | LED package reserve 3 × 5 × 5 mm behind a Ø3.4 × 2.9 mm diffuser in a Ø3.6 bore; `M007` 5 g allowance; crown too shallow for a 30 mm straight rearward exit |
| Sourcing | India-obtainable or single-order importable; active (not NRND) parts; hand-reworkable where possible, otherwise JLCPCB/LCSC-assemblable |

## 2. Audio path — `AP-TDM`, realised as two I²S lanes

### 2.1 What the Pi 5 can actually do

- The RP1 I²S block has **no true TDM**: word select is always 50:50 and each data line carries one stereo pair (Raspberry Pi engineer, forums t=383641 and linux#6568, `D`). A 4-slot TDM codec on one data line is not a supported path, which is why AC108/TLV320ADC-on-Pi-5 reports show one live channel (forums t=373301).
- It **does** run up to four synchronous stereo lanes on one clock: `i2s0` SDI0–3 on GPIO20/22/24/26 and SDO0–3 on GPIO21/23/25/27. The stock kernel's `hifiberry-adc8x` overlay muxes `gpio18, 19, 20, 22, 24, 26` on `i2s_clk_producer` for 8-channel capture, and `hifiberry-dac8x` plays 8 channels on GPIO21/23/25/27 (`D`, raspberrypi/linux `rpi-6.12.y`, PR #6662).

So four mic channels need **two capture lanes**, SDI0 (GPIO20) and SDI1 (GPIO22). GPIO22 is outside the `CA-06` reservation; see §2.6.

### 2.2 Selected chain

```text
Pi 5 i2s0 (clock producer, 48 kHz, 32-bit slots, BCLK 3.072 MHz)
 ├─ GPIO18 BCLK ─┬─────────────┬───────────────┐
 ├─ GPIO19 LRCLK ┼─────────────┼───────────────┤
 ├─ GPIO20 SDI0 ◄┤ ADAU7002 #1 ◄ PDM ◄ FRONT_L (LR=GND) + FRONT_R (LR=VDD)
 ├─ GPIO22 SDI1 ◄┤ ADAU7002 #2 ◄ PDM ◄ REAR_L  (LR=GND) + REAR_R  (LR=VDD)
 ├─ GPIO21 SDO0 ─┴─────────────► MAX98357A ─► Visaton K 50 WP 8 Ω
 └─ GPIO23 AMP_SD (GPIO out, 100 kΩ pull-down: amp off by default)
```

One clock tree drives every converter, so capture and playback are **sample-synchronous by construction** (`AR-03`, `AR-50`, `AR-51`): the playback buffer is a sample-aligned echo reference for AEC or a barge-in gate (`AR-53`), with a fixed pipeline latency to measure once.

| Item | Selection | Key facts |
|---|---|---|
| Front end | **2 × Analog Devices ADAU7002** (`ADAU7002ACBZ-R7`, LCSC C481886) | Stereo PDM→I²S, no register programming, 1.62–3.6 V, PDM clock = 64 × fs derived from BCLK, 8-ball 1.56 × 0.76 mm WLCSP (JLCPCB assembly only), 0.67 mA at 1.8 V, < 1 µA shutdown (`D`). Mainline `adi,adau7002` codec driver and the Pi `adau7002-simple` overlay exist (`D`) |
| Microphones | **4 × Infineon IM73D122V01** (`IM73D122V01XTMA1`, "active and preferred") | Digital PDM, **73 dB(A) SNR** at 3.072 MHz, −26 dBFS sensitivity, 122 dB SPL AOP, 20 Hz LFRO, ±1 dB matched, 4 × 3 × 1.2 mm bottom port, **IP57 at component level**, 0.98 mA, 1.62–3.6 V; high-performance mode 2.9–3.3 MHz (`D`) |
| Amplifier | **Analog Devices MAX98357A** (TQFN-16 `MAX98357AETE+T` on the installed board) | I²S in, no MCLK, 2.5–5.5 V, **1.75 W into 8 Ω / 3.2 W into 4 Ω at 5 V**, 2.4 mA quiescent, 0.6 µA shutdown, 7 ms turn-on, click-and-pop suppression, filterless spread-spectrum output, 77 dB PSRR (`D`). `SD_MODE` low = shutdown; high = left channel |
| Speaker | **Visaton K 50 WP – 8 Ω** (art. 2915) | Ø50 × 18 mm, Ø46 cutout, **48 g**, 2 W rated / 3 W max, 84 dB (1 W/1 m), 180 Hz–17 kHz, fs 300 Hz, ABS basket, Mylar cone, IP65 front when sealed (`D`) |

**Sample rate is 48 kHz.** At 48 kHz the ADAU7002 clocks the mics at 3.072 MHz, inside the IM73D122 high-performance window. At 16 kHz it would clock them at 1.024 MHz, which lies between the datasheet's power-mode windows; capture at 48 kHz and decimate in software.

**Channel map** (`AR-03`): SDI0 L/R = `FRONT_L`/`FRONT_R`, SDI1 L/R = `REAR_L`/`REAR_R`, i.e. ALSA channels 0–3 in that order. Lane ordering and the ADAU7002 L/R edge convention are bench-verified with a tap test before any array processing (`U`).

### 2.3 Why not the alternatives

| Candidate | Outcome |
|---|---|
| AC108 / TLV320ADC3140 / PCMD3140 as a 4-slot TDM codec | **Rejected on the host.** RP1 cannot receive >2 slots per lane (§2.1). A TLV320ADC3140 with its secondary ASI output would still need two lanes, and adds I²C set-up and a driver with reported Pi register errors (TI E2E 1321953) for no gain over the ADAU7002 |
| XMOS/XVF-class USB array (`AP-USB`, `AP-USB-IO`) | **Rejected by §3 rules 1 and 4.** Commercial arrays fix their own capsule geometry (≈ 65 mm circle), so they cannot place mics at the Layout 02 ports ±70 mm apart on the side walls (`AR-04`, `AR-64`), and a separate playback device splits the clock (`AR-51`) |
| `AP-SPLIT` | Negative comparison only; fails `AR-51` by design |
| Infineon IM69D130 | Infineon marks it **"not for new design"** (`D`, 2026-09) |
| Infineon IM69D128S / IM69D129F | Viable, 69 dB SNR; the IM73D122 keeps 4 dB more SNR for far-field wake at the same footprint and current |
| Visaton FRS 5 X | 140 g against a 90 g audio row, for bass a ~46 cm³ sealed cavity cannot use |
| Visaton K 50 (metal) | fs 400–500 Hz, 250 Hz–10 kHz: too narrow for music (`AR-36`) |
| PUI AS05008MR-4-R | Ø50 × 7.5 mm, 8 Ω, 1.5 W: kept as the **thin alternate** if the cavity must shrink; its SPL is an 0.8–1.5 kHz average, not comparable to Visaton's |

### 2.4 `audio-path.md` §3 reject rules

| Rule | Result |
|---|---|
| 1. Four capsules at the Layout 02 ports | Pass: discrete mic boards at the unchanged port coordinates |
| 2. Quiet-sleep listen without camera or cloud | Pass: I²S capture is local; needs only C0 and the 3.3 V front end |
| 3. No mute-to-play / mute-to-listen | Pass: full duplex on one i2s0 instance |
| 4. Recoverable speaker↔mic time relation | Pass by construction: one BCLK/LRCLK for all converters |
| 5. No UART collision, back-power, or speaker current in a safety return | Pass subject to §2.5 and `CA-06` CR-01 (§2.6) |
| 6. No English-TTS character voice | Not a hardware property; unchanged |
| 7. Kit speaker must not abandon the cavity | Pass with an RP-06 envelope revision: the K 50 WP is the 50 mm / 18 mm driver the reservation assumed, but the cavity behind it is 20 mm, not 34 mm (§5) |

### 2.5 Electrical binding (answers RP-02 `PB-AUDIO-OUT` §8.x "RP-05 must supply")

| Item | Answer |
|---|---|
| Amplifier part | MAX98357A, TQFN-16, on `PCB-05` |
| Supply range / absolute max | 2.5–5.5 V operating; take the 5 V `PB-AUDIO-OUT` rail directly |
| RMS and crest current | 1.75 W into 8 Ω = 0.47 A RMS in the speaker; about 0.4 A average and 0.7 A crest from 5 V at ~85% efficiency (`E`), well under the 2.0 A breaker |
| Idle / shutdown current | 2.4 mA typ, 2.85 mA max (at 3.7 V, `D`); 0.6 µA typ, 2 µA max shutdown |
| Pops | Internal click/pop suppression on enable and shutdown; 7 ms turn-on. Stream silence before raising `AMP_SD` (`U`, bench-listen) |
| Mute default | **Off**: `SD_MODE` held low by a 100 kΩ pull-down until C0 drives `AMP_SD` (GPIO23) high |
| Logic level / enable source | 3.3 V from the Pi; enable is the C0 GPIO, not a power-rail sequence |
| EMI | Filterless spread-spectrum output; speaker leads twisted, under 150 mm; add ferrite beads only if the camera or radios show it |
| Mic-side ripple | Mics and ADAU7002s run from their own 3.3 V domain (below), 80 dB PSR in the mics (`D`) |
| `PB-AUDIO-IN` source (`AR-07`) | The 3.3 V mic/ADAU7002 domain is fed from the **Pi header 3.3 V** (< 10 mA `E`), so the front end is unpowered whenever C0 is off: no ADAU7002 output can back-drive GPIO20/22 into an off SBC, and `LP-07-OFF` follows C0 power. RP-02 to confirm this attribution |
| Amp inputs when the amp branch is off | 100 Ω series resistors on BCLK/LRCLK/DIN at `PCB-05`; `makad-audio` raises `AMP_SD` only after the branch reports `PG` |

Power ledger inputs: `LG-07` about 4 × 0.98 mA + 2 × ~1 mA at 3.3 V ≈ 20 mW (`E`); `LG-08` idle ≈ 14 mW, peak ≈ 2.1 W at full sine into 8 Ω (`E`).

### 2.6 `CA-06` change request CR-01

| Pin | Now | Requested | Collision check |
|---|---|---|---|
| GPIO18–21 | Audio reservation | BCLK, LRCLK, SDI0, SDO0 | Unchanged |
| **GPIO22** | Unassigned | **I²S0 SDI1** (rear mic pair) | Not UART0/UART2, not I²C1, not SPI0 GPIO8–11 |
| **GPIO23** | Unassigned | **`AMP_SD`**, GPIO output, default low | Same |

The overlay is a custom `simple-audio-card` on `i2s_clk_producer` with pins 18–22 muxed to `i2s0` and 23 as a plain GPIO. The DAC8x/ADC8x driver notes "symmetric operation only"; if RP1 requires equal channel counts, playback opens 4 channels and lane 1's output stays unmuxed (`U`, first bench item).

### 2.7 Boards and articles

| Article | Bench (Phase A) | Installed |
|---|---|---|
| Front end + amp | 2 × ADAU7002 on a JLCPCB-assembled `PCB-05` from day one (no stocked ADAU7002 breakout); MAX98357A may be an Adafruit #3006-class breakout meanwhile | **`PCB-05` audio front end**, 30 × 38 × 1.6 mm, flat above the Pi 5's front end (X 45–75, Z 114–123, §5): 2 × ADAU7002, MAX98357A, 3.3 V filter, 4 × JST-SH 4-pin mic inputs, 2-pin speaker, 10-pin host cable (BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, 3V3, 2 × GND, 5 V from the branch on its own pair) |
| Mics | Infineon `KIT_IM73D122V01_FLEX` (five 25 × 4.5 mm flex boards + ZIF adapter; DigiKey US$75.19, 0 in stock, restock 2026-10-19; standard lead time 97 weeks) | **4 × `PCB-06` mic board**, 12 × 8 × 1.0 mm: one IM73D122 on the inboard face, Ø0.8 mm port through the PCB, JST-SH 4-pin (3V3, GND, CLK, DATA), LR strap per position; screwed to the body frame so the array is rigid and calibrated (`AR-64`) |
| Speaker | K 50 WP | Same, bonded at its flange behind the front grille; sealed back cavity Ø54 × 20 mm (X 77–97, about 46 cm³ gross), cut from the 34 mm reservation because that ran through the compute tray and Pi 5 (§5) |

`AR-60` (speaker to mic coupling) and `AR-61` (cooler) remain measurements. The speaker is on the front panel, the front mic pair is 49 mm behind it and ±70 mm off the centreline; at 1.75 W the SPL at the nearest port is estimated well under the 122 dB SPL AOP (`E`, about 110 dB SPL at 5 cm on axis).

## 3. Status light — WS2812B-2020 behind the existing light pipe

| Item | Selection | Key facts |
|---|---|---|
| LED | **Worldsemi WS2812B-2020-V6** (LCSC C965555) | 2.0 × 2.0 × 0.84 mm addressable RGB, **3.3–5.5 V**, 12 mA per colour, 8-bit per colour, **2 kHz PWM**, built-in capacitor, reverse-polarity tolerant, < 1 µA static, 800 kbit/s single-wire (`D`) |
| Carrier | **`PCB-08`**, 5 × 5 × 0.8 mm FR4, LED on the front face, three pads on the back | Fits the head's existing 3 × 5 × 5 reserve: board X −8…−7.2, LED −7.2…−6.36, **1.36 mm air gap** to the diffuser's rear face at X −5 |
| Optic | **Ø3.4 × 2.9 mm clear light pipe** (the existing `crown_status_light_diffuser` geometry), SLA clear resin or turned from Ø4 mm PMMA rod, exit face bead-blasted, UV-bonded in the Ø3.6 crown bore | No head aperture change, so the Layout 03/04 optics verification stands |
| Driver | **D1 GPIO6** on its Sensor-AD PH2.0 header, RMT peripheral; LED powered from that header's 3.3 V | D1 executes `LIGHT_STATE` (C2-relayed, `CA-04`); RMT gives the `LIGHT_REPORT` onset stamp at frame latch (+280 µs reset) |
| Wiring | 3 × AWG30 PTFE (3V3, GND, DIN) soldered to the back pads, turned 90° within 2 mm | Replaces the 30 mm straight rearward exit the crown could not hold; the routed path to D1 is still a keep-out (§5) |

Why this part:

- **Camera contamination** (`SC-TBD-19`, RP06-G03): the 2 kHz PWM puts 20 PWM periods inside a 10 ms indoor exposure, so band ripple from reflected LED light averages out; the 400 Hz WS2811/WS2812 (pre-V5) and ~1.1 kHz SK6812 classes are worse. Full-on colours have no PWM at all. The light pipe is beside the lens, not in its field; stray light into the lens is the G03 bench test.
- **Colour capability** (`SC-TBD-19`): full RGB, so meaning can be assigned later without a hardware change.
- **Timing**: one data line, fixed 30 µs per pixel frame; onset uncertainty is the RMT start plus reset, bounded and loggable (`IR-07`).
- **3.3 V operation**: no level shifter from D1 and no 5 V run into the crown. Blue/green brightness at 3.3 V is lower than at 5 V (`U`); the status light needs tens of mcd through a diffuser, not full output.

Rejected: APA102-2020 / SK9822 (high PWM but needs a second pin D1 does not have free); 5050 packages (do not fit the 3 mm reserve depth with a carrier); single-colour LED + driver (the sourcing matrix's fallback) loses colour capability for no packaging gain.

## 4. Base IMU — ICM-42688-P on its own rigid board

| Item | Selection | Key facts |
|---|---|---|
| Silicon | **TDK InvenSense ICM-42688-P** (`S07` lead) | 6-axis, SPI to 24 MHz, INT1/INT2, 2 kB FIFO, 1.71–3.6 V, 2.5 × 3 × 0.91 mm LGA-14, 0.88 mA 6-axis low-noise mode, 20 000 g shock (`D`). India: Robu ₹314 (bare part), RS India ₹755 (pack of 2) |
| Installed article | **`PCB-07` IMU board**, 20 × 16 × 1.0 mm: ICM-42688-P, 0.1 µF + 2.2 µF + 10 nF per datasheet, JST-SH 8-pin (3V3, GND, SCLK, MOSI, MISO, CS, INT1, INT2/CLKIN), two M2 holes 15 mm apart | Screwed flat to the chassis deck on the body axis (X 6–26, Y ±8), so it sees the base frame directly (`BD-03`: rigid base mount, not the head) |
| Bench article (Phase A) | Any breakout that brings **SPI and INT1 out**, verified by continuity and photograph on receipt: MikroE **MIKROE-4237** (6DOF IMU 14 Click, SPI default, INT on mikroBUS) where stocked; LogicalEdges (Tindie) or Sysrox SPI boards otherwise | MikroE lists MIKROE-4237 as out of stock and DigiKey shows 0 (2026-09-26); a few distributors hold stock at US$22–36 |

Why a custom board rather than a breakout installed: the obtainable breakouts either lack mounting holes (MikroE Click, Sysrox), are expensive imports (Tindie US$98), or are the UART-angle MCU modules `S07` rejects (Robu 601N1). A one-chip board on the same JLCPCB order as `PCB-05/06/08` gives SPI + INT1 to the silicon, two screws into the base, and the exact footprint the CAD carries.

## 5. CAD result (body Layout 02 `RP03-CAD-11`, head Layout 04 `HEAD-CAD-12`)

Modelling the real parts exposed two reservations that had overlapped other hardware since Layout 02 began, because nothing measured them:

- the 38 × 30 × 9 amplifier reservation at (49, 0, 103) lay inside the Pi 5 (2296 mm³) and the Active Cooler (764 mm³). `PCB-05` now lies flat above the Pi's front end, X 45–75, Y ±19, Z 114–123: forward of the cooler headroom (cooler X ≤ 43.6), 2.1 mm over the Pi's top (Z 111.9), 3 mm under the front upper cross (Z 126);
- the 34 mm speaker cavity (X 63–97) ran through the compute tray (1844 mm³) and the Pi 5 (903 mm³). It is now X 77–97 (20 mm, Ø54, about 46 cm³ gross before the driver's own volume), 1 mm off the tray. With fs 300 Hz this raises the sealed-box resonance; chirps and speech are above it, music bass is not (`AR-36`, `U` until measured). This is an RP-06 envelope revision under `AR-31`.

New checks in `check_layout.py`: `selected_audio_and_imu_parts_are_clear` (26 parts against chassis, shell, panels, frame, power boards, electronics, sensors, yaw stage, motors, tub: 0 clashes), `speaker_is_k50wp_outline_behind_front_panel` (Ø50 × 18, face 0.5 mm behind the panel), `mic_packages_on_port_axes_against_boots` (all four on axis), `imu_board_seated_on_deck_with_both_screws_in_material` (board on Z 56, both M2 shanks 4 mm in the crossbar). 113 of 114 checks pass; the failure, `rear_tail_clears_shell_and_panels` (220 mm³, parked tail), predates this change. The cavity keep-out still touches the unrouted signal and sensor harness volumes by 23 mm³ each; those volumes are placeholders.

Mass register (`E`): `BODY_AUDIO` 90 g at (64, 0, 102) → 60 g at (77.9, 0, 101.9); `IMU_BREAKOUT` 2 g → `IMU_PCB07` 2.5 g at (21, 0, 57.5). Total 2558.9 → **2529.4 g**; CoM x +18.89 → **+19.38 mm**, h 106.98 → **106.96 mm**; a_tip 1.732 → **1.777 m/s²** (floor 1.582).

Head Layout 04: the LED carrier and package sit inside the unchanged `M007` reserve; `check_revision.py` passes, `check_layout.py` 56 poses × 159 pairs, 0 hits, no static package hits. No aperture or mass change.

## 5a. Cost estimate (2026-09-26, `E`, about ₹88/US$, not quotes)

| Item | Unit | Qty | ≈ ₹ |
|---|---|---|---|
| IM73D122V01 | ~US$2 (not quoted; IM69D130 is US$2.16 at DigiKey) | 4 | 600–1,000 |
| ADAU7002ACBZ-R7 | US$4.10 LCSC | 2 | ~720 |
| MAX98357A | chip US$2–3; India breakout ₹150–300 | 1 | 150–300 |
| Visaton K 50 WP | €5.74 EU; Tanotis India price not read | 1 | 600–1,500 |
| ICM-42688-P | Robu ₹314 | 1 | 314 |
| WS2812B-2020 | cents | 1 | ~20 |
| **Parts** | | | **≈ 2,400–3,900** |
| JLCPCB order, `PCB-05…08` (fab, assembly setup, shipping, customs) | one-off | 1 | 4,000–7,000 |
| **Total** | | | **≈ 6,500–11,000** |

Against the sourcing matrix's earlier ranges for these rows (mics + front end, speaker + amp, IMU, status light: ≈ ₹3,500–15,000), this is inside the band; most of it is the one-off PCBA order. Skip the optional `KIT_IM73D122V01_FLEX` (US$75, ≈ ₹6,600) and put the mics straight on `PCB-06`. Cheaper options: a MAX98357A breakout instead of the chip on `PCB-05` (loses the built-in series-resistor protection), IM69D128S mics (69 dB SNR). Get written quotes before purchase.

## 6. What stays open

| Item | Owner | Evidence needed |
|---|---|---|
| Pi 5 two-lane capture + one-lane playback on one `i2s0` instance, channel map, symmetric-channel constraint | RP-05 bench | `arecord -c 4` + `aplay` simultaneously, tap test per port, 1 h no xrun |
| Speaker↔mic coupling (`AR-60`), cooler noise (`AR-61`), servo/drive noise (`AR-62/63`) | RP-05 / RP06-G03 | Acoustic matrix |
| `PCB-05/06/07/08` schematics and layouts | RP-02 / RP-05 | Not started |
| Mic board fixing to the body frame; speaker flange bond and grille; LED wire route from the crown to D1 | RP-06 | CAD detail and service-path check (`AR-65`, SC-17) |
| WS2812B-2020 brightness and colour at 3.3 V through the light pipe; stray light into the camera | RP06-G03 | Bench |
| ICM-42688-P mounting stiffness on the printed deck, bias vs temperature near `PCB-03/04` | RP-03 G01/G05 | Bench |
| Measured masses of every article | RP-06 | Weigh |
| Supplier quotes (IM73D122 reels are 5000; order cut tape through DigiKey/Mouser India or have JLCPCB source it) | Builder | Quote |
