# Body v1 bill of materials — working snapshot

Started 2026-10-03 from the [project BOM](../../BOM.csv) for **one body**. Quantities are installed quantities, with no spare or scrap allowance. This is a procurement and design worklist, **not a released order or fabrication package**. The states are the same as in the [chassis v1 BOM](../../01-chassis/v1/BOM.md): `DESIGN`, `CANDIDATE`, `SELECTED`, `HOLD` and `OPEN`. No row is marked received or measured.

The model basis is [body_v1_model.py](cad/body_v1_model.py). The project BOM carries the detailed specification, source and release check for every ID below.

**Coverage:** this snapshot holds the **audio system**, the **wheel arches** and the **power button** only. The shell, body frame, service panels, compute (Pi 5 and cooler), yaw stage and their hardware are not yet in the project BOM. Shared power boards (PCB-02, PCB-03, PCB-04) and the C3 carrier are counted once, in the chassis rows CH-041 to CH-044.

## Audio

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-001 | [Visaton K 50 WP – 8 Ω speaker, art. 2915](https://in.element14.com/visaton/2915/speaker-k-50-wp-8-ohms/dp/1683894) (element14 India 1683894) ([D-034](../../decisions.md#d-034)) | 1 | SELECTED |
| BO-002 | Audio front end PCB-05, 30 × 38 mm | 1 assembly | HOLD |
| BO-003 | MAX98357AETE+T I²S class-D amplifier, on PCB-05 | 1 | CANDIDATE |
| BO-004 | ADAU7002ACBZ-R7 PDM-to-I²S converter, on PCB-05 (LCSC C481886) | 2 | CANDIDATE |
| BO-005 | Mic board PCB-06, 12 × 14 mm, with one Infineon IM73D122V01; shell-mounted ([D-037](../../decisions.md#d-037)) | 4 assemblies | HOLD |
| BO-006 | Audio cable set: W12, W26, W27 × 4, W28 | 1 set | HOLD |
| BO-012 | [Infineon IM73D122V01XTMA1 PDM mic](https://in.element14.com/infineon/im73d122v01xtma1/mems-microphone-pdm-122db-pg-llga/dp/4125831) (element14 India 4125831), one per BO-005 board; buy 6 for reflow spares ([D-036](../../decisions.md#d-036)) | 4 | SELECTED |
| BO-013 | M2 × 4 pan-head thread-forming screw for plastics, two per mic board into the shell boss ([D-037](../../decisions.md#d-037)) | 8 | CANDIDATE |
| BO-014 | Mic port gasket, closed-cell foam ring Ø6.5/Ø2.0 × 1.0 mm, compressed 30% in the boss pocket ([D-037](../../decisions.md#d-037)) | 4 | CANDIDATE |

**Bench articles** (not installed; not counted in `BODY_AUDIO`):

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-007 | [SmartElex MAX98357A I²S breakout](https://robocraze.com/products/smartelex-max98357a-i2s-audio-breakout-amplifier-for-raspberry-pi-and-microcontrollers) (Robocraze, ₹195) ([D-035](../../decisions.md#d-035)): drives BO-001 until PCB-05 exists; one is a spare. Its SD pin is likely pulled up (amp on at power-up) and it lacks PCB-05's series resistors | 2 | SELECTED |

**Signal chain.** The Pi 5's i2s0 drives every converter from one clock (48 kHz, BCLK 3.072 MHz on GPIO18, LRCLK on GPIO19).
- **Capture:** each ADAU7002 turns one stereo pair of PDM mics into one I²S lane. The front pair goes to SDI0 (GPIO20) and the rear pair to SDI1 (GPIO22). ALSA channels 0–3 are FRONT_L, FRONT_R, REAR_L, REAR_R.
- **Playback:** SDO0 (GPIO21) feeds the MAX98357A, which drives the speaker.
- **Amp enable:** GPIO23 drives `AMP_SD`. A 100 kΩ pull-down holds the amplifier off by default.
- **Echo reference:** capture and playback share the clock, so playback is a sample-aligned echo reference.
- **Pins:** GPIO22 and GPIO23 need RP-02 `CA-06` change request CR-01.

Design basis: [peripheral selection](../../../02-prototypes/RP-06-cad/peripheral-selection.md) §2.

**Power.**
- **Amplifier:** the 5 V `PB-AUDIO-OUT` branch on PCB-04 (TPS259474L e-fuse at 2.0 A), through W12. About 0.4 A average, 0.7 A peak, 2.4 mA idle.
- **Mics and ADAU7002s:** the Pi header 3.3 V, through W26 and a filter on PCB-05, under 10 mA. The front end is therefore off whenever the Pi is off and cannot back-power its GPIO. RP-02 still has to confirm this source.

**Cables** ([connector schedule](../../../02-prototypes/RP-06-cad/connector-schedule.md)):

| Cable | From → to | Connector | Wires |
|---|---|---|---|
| W26 audio host | PCB-09 `J9-3` → PCB-05 `J5-1` | JST GH 10 | BCLK, LRCLK, SDI0, SDI1, SDO0, AMP_SD, 3V3, 2 × GND, spare |
| W27 mics (× 4) | PCB-06 pads (soldered) → PCB-05 `J5-2…5` | Pre-crimped JST GH 4 AWG28 lead, about 150 mm front / 200 mm rear | 3V3, GND, CLK, DATA |
| W28 speaker | K 50 WP tabs (soldered) → PCB-05 `J5-6` | JST GH 2 | 2 × AWG26, twisted, under 150 mm |
| W12 amp power | PCB-04 `J4-5` → PCB-05 `J5-7` | Micro-Fit 3.0 2×1 | 2 × AWG22 |

**Placement (model coordinates, mm).**

| Part | Location | How it is mounted |
|---|---|---|
| Speaker | Exposed face at X 100, axis (Y 0, Z 99) | Unobstructed Ø46 panel aperture; face recessed 2.6 mm behind the lip, Ø50 flange bonded to its rear across a 0.8 mm silicone seal. Ø54 speaker clearance reserve X 82–97.5; rear enclosure sealing still requires physical verification |
| PCB-05 | Flat at (60, 0, 118.5) | Above the Pi 5's front end, under the front upper cross |
| PCB-06 boards | Front pair X 54, Z 118; rear pair X −22, Z 108; outer face on \|Y\| 71.3 | On printed bosses on the shell's inner skin, coaxial with the ports: a foam gasket ring in a pocket seals each port, two M2 × 4 thread-forming screws clamp the board, and a soldered GH lead replaces the header ([D-037](../../decisions.md#d-037), [CAD README](cad/README.md#microphone-mounts-d-037)) |

The `BODY_AUDIO` mass row carries 61 g at (74.5, 0, 102.1): speaker 48 g, PCB-05 about 6 g, mic boards about 2 g, cables about 4 g, and about 1 g of mic screws, gaskets and larger boards (D-037). The four mic bosses are in the shell row (+4.0 g).

**Speaker choice.** [D-034](../../decisions.md#d-034) locks the K 50 WP: it is the outline the CAD already carries, and among the 50 mm Visatons it has the widest range at the lowest price seen. The fallback is the Visaton K 50 – 8 Ω (art. 2901), which fits the same envelope but covers only 250 Hz–10 kHz. A replacement must fit within Ø50 × 18 mm, be 8 Ω and be rated at least 2 W.

**Microphone choice.** [D-036](../../decisions.md#d-036) locks the IM73D122V01 for its 73 dB(A) SNR (quiet-room wake word) and bottom port. The array is four mics, two per ADAU7002 lane; six would need a third lane and converter. The cheaper fallback is the bottom-port MEMSensing MSM261D3526Z1CM (64 dB SNR).

## Wheel arches

Separate prints fastened to the shell on the bench before it is lowered; see the [CAD README](cad/README.md#wheel-arch-pods).

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-008 | Wheel-arch pod, printed outer face down without supports | 2 | DESIGN |
| BO-009 | Wheel-arch trim ring, amber, glued to the pod | 2 | DESIGN |
| BO-010 | ISO 7380 M3 × 8 button head, from inside the shell (same article as CH-048) | 6 | CANDIDATE |
| BO-011 | M3 × 4 brass heat-set insert in the pod (same article as CH-049) | 6 | CANDIDATE |

The pod and trim mass is in the `BODY_SHELL_AND_PANELS` row; the screws and inserts are in the mixed fastener allowance.

## Power button

The red mushroom on the rear panel is the power button; **there is no E-stop** ([D-041](../../decisions.md#d-041)). It is the `PB` input of the LTC2954 latch on PCB-02, wired to a GH2 `J2-9`. A press also stops the motors in hardware ([power-boards.md §6](../../04-pcbs/power-boards.md#6-pcb-02-power-button-input-d-041)).

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-018 | 16 mm momentary red mushroom pushbutton, 1NO, metal head, IP65, with nut and gasket: [SparkFun-type 16 mm metal mushroom](https://www.tanotis.com/products/metal-mushroom-head-pushbutton-panel-mount-16mm-red) (Tanotis, ₹850). It must fit the existing well (Ø16.2 cut-out, 2 mm floor, mushroom ≤ Ø30 and ≤ 20.6 mm above the floor, ≤ 23.9 mm behind it) | 1 | CANDIDATE |

It replaces the IDEC XA1E-BV3U02KT-R E-stop (CH-046). That part latches when pushed and has NC contacts, so it cannot drive the latch. The `W40` lead (GH2, single-ended, 150 mm) is in the harness buy list (HN-004).

**Use:**
- Hold about 0.5 s to turn on.
- Any press while running stops the drive and head at once, in hardware. They stay stopped until C2 re-arms.
- Hold 1 s for an orderly shutdown.
- Hold about 5 s to force off.
- In `CHARGE` the button does nothing.

**Mounting.** It sits on the floor of the existing octagonal well, inside the amber bezel. It comes off with the rear panel after `W40` is unplugged at `J2-9`. The `POWER_BUTTON_MUSHROOM_16MM_AND_W40` mass row carries 15 g (`E`).

**Fallback:** the Daier A16-11SM 16 mm momentary mushroom (Evelta, ₹118). It is plastic and rated for only 10,000 operations, so it is a bench part.

## Open before release

1. **Order and measure the speaker:** order BO-001. Caliper and weigh it against Ø50 × 18 mm and 48 g, then update `BODY_AUDIO`. The element14 India price and stock were not read on 2026-10-03.
2. **Bench test:** order BO-007 with BO-001 and check its SD pull-up on receipt. Listen first, then Pi 5 two-lane capture plus playback on one i2s0: `arecord -c 4` and `aplay` together, a tap test per mic port, and an hour with no xruns.
3. **Boards:** schematics and layouts for PCB-05 and PCB-06 are not started. Settle whether 5 V reaches PCB-05 on W12 only, or also on the GH 10.
4. **Pins:** approve `CA-06` CR-01 for GPIO22 (SDI1) and GPIO23 (`AMP_SD`).
5. **CAD details:** the exposed-speaker flange bond and front-panel seal, a printed shell-boss coupon for the mic mount (seat, Ø1.6 pilots, skin witness marks, gasket seal by tap test), and supports for the front-panel speaker cup print.
6. **Acoustics:** speaker-to-mic coupling (RP-05 `AR-60`), cooler and drive noise (`AR-61` to `AR-63`), and low-end response in the 15.5 mm cavity.
7. **Ordering the boards:** quotes for the JLCPCB order (PCB-05 to PCB-08). IM73D122 mics come as cut tape or are sourced by JLCPCB, since reels are 5000.
8. **Power button:** order BO-018. Check on receipt that the mushroom, the collar and the body behind the floor fit the well envelope, and that the contact is 1NO and momentary. Weigh it, then run bench PB-01 to PB-06.
