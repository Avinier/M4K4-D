# Body v1 bill of materials — working inventory

Started 2026-10-03 from the [project BOM](../../BOM.csv) for **one body**; expanded 2026-10-04 against the body-v1 CAD. Quantities are installed quantities, with no spare or scrap allowance unless a row says otherwise. This is a procurement and design worklist, **not a released order or fabrication package**. The states are the same as in the [chassis v1 BOM](../../01-chassis/v1/BOM.md): `DESIGN`, `CANDIDATE`, `SELECTED`, `HOLD` and `OPEN`. `DESIGN` means geometry exists, not that a print is qualified. No row is marked received or measured.

The model basis is [body_v1_model.py](cad/body_v1_model.py). The project BOM carries the specification, source and release check for every ID below. The working-tree compute mount and cooling geometry is included as a **provisional CAD basis**; it has not been released by a recorded decision or physical test.

**Counting boundary:** the BO rows below cover the enclosure, body frame and chassis joints, compute and enclosure cooling, audio, charge inlet, power button, and the body-side yaw mechanism. Subcomponents listed beside a board or assembly are an **exploded inventory**, not additional complete assemblies to buy. Shared PCB-02/03/04 and PCB-10 are counted once under CH-041 to CH-044; yaw junction PCB-08 and C0 link adapter PCB-09 are counted once under CH-083 and CH-084. The complete W01–W40 harness and its connector/wire stock are counted under HN-001 to HN-010; BO-006 identifies its audio branch, and BO-042 identifies the newly proposed W41 fan lead. The head assembly, chassis, battery and deck sensors are outside this body BOM.

## Enclosure, panels and body frame

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-019 | Open-bottom faceted body shell, one print with four frame bosses, four mic bosses, wheel-arch seats and the +Y fan grille/collar | 1 | DESIGN |
| BO-020 | Front service panel print with open Ø46 speaker aperture and cup | 1 | DESIGN |
| BO-021 | Rear service panel print with power-button well, charge-inlet pad and vent slots | 1 | DESIGN |
| BO-022 | Front internal service-panel frame with four screw bosses | 1 | DESIGN |
| BO-023 | Rear internal service-panel frame with four screw bosses | 1 | DESIGN |
| BO-024 | Amber rear-button bezel and front badge land, separate trim prints | 1 set (2 prints) | DESIGN |
| BO-025 | Main body-frame print: three feet, posts, side/cross rails, yaw adapter plate, compute-tray supports and fan web | 1 | DESIGN |
| BO-026 | Removable front-left foot cassette print with captive-nut pocket | 1 | DESIGN |
| BO-027 | M3 × 16 cassette-to-frame side screw | 2 | CANDIDATE |
| BO-028 | M3 × 6 heat-set insert in the cassette | 2 | CANDIDATE |
| BO-029 | M3 × 16 outside-driven shell-to-frame screw | 4 | CANDIDATE |
| BO-030 | M3 × 6 heat-set insert in the frame posts | 4 | CANDIDATE |
| BO-031 | M3 × 8 service-panel screw, four at each end | 8 | CANDIDATE |
| BO-032 | Profiled M3 wedge washer for the sloped service-panel screw seat | 8 | DESIGN |
| BO-053 | Front and rear internal-panel-frame attachment or bond | 1 set | OPEN |

The body-to-chassis joint uses existing **CH-035 M4 × 12 bolts (4), CH-036 plain M4 nuts (4), and CH-037 Ø4 × 8 locating pins (2)**. Three bolt heads are driven from above; the front-left head is driven from below into a nut trapped in BO-026. These are chassis-owned purchase rows and are not counted again as BO items.

The shell is lowered after the frame and the bench-fitted wheel arches and microphones. The front-left cassette slides in under the fixed fuse shelf before the shell is installed. [The CAD assembly sequence](cad/README.md#body-framechassis-assembly) and `check_body_frame_fit.py`, `check_shell_frame_fit.py`, and `check_body_panel_fit.py` define nominal fit checks. Confirm actual tool access, insert retention, panel stiffness, print process and joint load before fabrication release. The panel screws currently enter printed bosses without modeled threaded inserts; their thread-forming specification, pilot size and service-cycle life remain open.

The [current CAD mass check](cad/generated/body-layout-checks.json) estimates **248.3 g** for shell/panels and **176.9 g** for the frame with its modeled joint hardware; these are material/geometry estimates, not weighed parts. The 95 g mixed harness/fastener allowance remains separate. Reconcile individual weights after printing and assembly.

## Compute and enclosure cooling

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-033 | Vented compute-tray print, four Pi bosses, perimeter rib and one rear −Y ear (three-point support) | 1 | DESIGN |
| BO-034 | Raspberry Pi 5, 2 GB, application computer C0 | 1 | SELECTED |
| BO-035 | Official Raspberry Pi 5 Active Cooler, including its two supplied push pins | 1 | SELECTED |
| BO-036 | M2.5 × 6 low-head Pi-to-tray screw | 4 | CANDIDATE |
| BO-037 | M2.5 × 4 brass heat-set insert in the tray bosses | 4 | CANDIDATE |
| BO-038 | ISO 7380 M3 × 8 tray-to-frame screw | 3 | CANDIDATE |
| BO-039 | M3 × 6 heat-set insert in the three tray supports (rear −Y lug, front −Y column, rear +Y block) | 3 | CANDIDATE |
| BO-040 | **Chosen 2026-10-04:** DC5V 4010 Double Ball Cooling Fan with XH2.54-2P 30CM Cable, 40 × 40 × 10 mm (2-wire, no PWM or tach) | 1 | SELECTED |
| BO-041 | Fan fixing screw, bought with the fan (not relied on as supplied); self-tapping, about 12 to 16 mm; two diagonal positions | 2 | CANDIDATE |
| BO-042 | W41 fan lead: the BO-040 fan's own 2-wire lead cut to about 80 mm and re-crimped into its XH2.54-2P housing, to PCB-09 `J9-4` | 1 assembly | DESIGN |

**Fan choice (2026-10-04):** the builder chose the 2-pin 5 V double-ball 4010 fan over the Noctua NF-A4x10 5V PWM (≈₹2,000). It has no PWM or tach, so it runs on/off: a low-side MOSFET on PCB-09 (CH-084), switched by Pi GPIO24 under the `gpio-fan` overlay, drives it from the 40-pin header's 5 V ([D-042](../../decisions.md#d-042)). The CAD fan model, the two 12 mm self-tapping screws, the W41 route and `J9-4`, the 15 g mass row (`E`) and the airflow figures (a typical 4010 listing class plus a half-flow case) now follow this fan. Its hole size, hole pitch (32 mm assumed), airflow, noise and mass are still unmeasured.

The Pi's four M2.5 holes are modeled over tray bosses; the Active Cooler's push-pin tips have underside keep-outs. The tray drops 2 mm onto three supports (a rear −Y lug, a front −Y column and a rear +Y block) and is retained by three M3 screws. The +Y enclosure fan sits on an integral frame web behind the shell grille; the rear panel has eight exhaust slots. The [current cooling-path check](cad/generated/cooling-path.json) is geometric and its airflow/temperature figures are estimates. [W41](../../05-harness/README.md) plugs the fan into PCB-09 `J9-4`; no splice into the Active Cooler lead. Measure Pi throttling, internal air and each mic channel with the fan on and off, and set the `gpio-fan` threshold from that. The selected Pi/cooler and enclosure fan have no reported purchase or receipt. The CAD mass register estimates 29.5 g for tray and fixings and 15 g for the fan; neither is weighed.

## Body-side yaw stage and shared board interfaces

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-043 | ROBOTIS XC330-M181-T yaw servo on the body frame, working actuator choice | 1 | CANDIDATE |
| BO-044 | Thin-section yaw bearing, modeled Ø50/Ø66 envelope | 1 | OPEN |
| BO-045 | Driven 1:1 spur gear on the yaw disc | 1 | DESIGN |
| BO-046 | Split scissor drive pinion, fixed and sprung halves | 1 assembly (2 halves) | DESIGN |
| BO-047 | Yaw-servo coupling shaft | 1 | DESIGN |
| BO-048 | Scissor-pinion preload spring and retaining clip | 1 set | OPEN |
| BO-049 | Yaw-bearing clamp ring | 1 | DESIGN |
| BO-050 | Head-yaw clock-spring/flex interconnect | 1 | HOLD |
| BO-054 | Retention hardware for PCB-05, PCB-08 and other body-mounted boards without defined mounts | 1 set | OPEN |

The model carries a mass allowance of 89 g for this stage, including a **50 g bearing placeholder**. It does not establish a bearing SKU, gear tooth specification/material, spring article, servo-to-shaft fastening, bearing retention or load life. PCB-08 (`CH-083`) is the stationary yaw junction, PCB-09 (`CH-084`) is the Pi-header link adapter; both are HOLD in the project BOM. BO-054 is a placeholder for **unresolved board mounting**, not a specified fastener pack. The body-side W13–W15 and W23–W26 wiring belongs to HN-001. Head-side moving parts belong to the head assembly, so count each gear and interconnect only once at integration release.

## Audio

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-001 | [Visaton K 50 WP – 8 Ω speaker, art. 2915](https://in.element14.com/visaton/2915/speaker-k-50-wp-8-ohms/dp/1683894) (element14 India 1683894) ([D-034](../../decisions.md#d-034)) | 1 | SELECTED |
| BO-002 | Audio front end PCB-05, 30 × 38 mm | 1 assembly | HOLD |
| BO-003 | MAX98357AETE+T I²S class-D amplifier, on PCB-05 | 1 | CANDIDATE |
| BO-004 | [ADAU7002ACBZ-R7](https://in.element14.com/analog-devices/adau7002acbz-r7/tdm-conversion-ic-2-channel-wlcsp/dp/4028782) PDM-to-I²S converter, on PCB-05 (element14 India 4028782; LCSC C481886); distributor description "Audio Control, Sample Rate Converter, 1.62V to 3.6V, I2S, TDM, WLCSP, 8 Pins, -40 °C" | 2 | CANDIDATE |
| BO-005 | Mic board PCB-06, 12 × 14 mm, with one Infineon IM73D122V01; shell-mounted ([D-037](../../decisions.md#d-037)) | 4 assemblies | HOLD |
| BO-006 | Audio cable set: W12, W26, W27 × 4, W28 | 1 set | HOLD |
| BO-012 | [Infineon IM73D122V01XTMA1 PDM mic](https://in.element14.com/infineon/im73d122v01xtma1/mems-microphone-pdm-122db-pg-llga/dp/4125831) (element14 India 4125831), one per BO-005 board; buy 6 for reflow spares ([D-036](../../decisions.md#d-036)) | 4 | SELECTED |
| BO-013 | M2 × 4 pan-head thread-forming screw for plastics, two per mic board into the shell boss ([D-037](../../decisions.md#d-037)) | 8 | CANDIDATE |
| BO-014 | Mic port gasket, closed-cell foam ring Ø6.5/Ø2.0 × 1.0 mm, compressed 30% in the boss pocket ([D-037](../../decisions.md#d-037)); cut from Robu EVA foam tape, 50 mm × 5 m, 1 mm (builder-reported 2026-10-04) | 4 | CANDIDATE |
| BO-051 | 0.8 mm annular silicone speaker-flange bond/seal behind the front-panel lip | 1 application | HOLD |

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

The `BODY_AUDIO` mass row carries 61 g at (78.4, 0, 102.1): speaker 48 g, PCB-05 about 6 g, mic boards about 2 g, cables about 4 g, and about 1 g of mic screws, gaskets and larger boards (D-037). The mic bosses and speaker cup are in the shell/panel row. The silicone bond quantity and cured mass remain unmeasured.

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
| BO-052 | PETG-compatible adhesive for the two amber trim rings | 1 application | HOLD |

The pod and trim mass is in the `BODY_SHELL_AND_PANELS` row; the screws and inserts are in the mixed fastener allowance.

## Charge inlet

| ID | Part | Qty | State |
|---|---|---:|---|
| BO-015 | Charge inlet PCB-13 with vertical power-only USB-C, PD sink and protection ([D-040](../../decisions.md#d-040)) | 1 assembly | HOLD |
| BO-016 | BIS-registered USB-C PD wall adapter ≥30 W with a 15 V ≥1.5 A PDO, plus 1 m 3 A C-to-C cable | 1 set | CANDIDATE |
| BO-017 | M2 × 5 thread-forming screw for PCB-13 into the rear-panel pad | 2 | CANDIDATE |

PCB-13 is mounted on the removable rear panel. Its W16 150 mm power lead is counted in HN-001/003/007. The adapter and cable are **external equipment**, not installed body mass. Board schematic, programmed PD NVM, plug fit and panel removal are release checks in [charge-path.md](../../04-pcbs/charge-path.md) and `check_charge_inlet.py`.

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

1. **Enclosure and joints:** select the print material/process and support plan for BO-019–026 and BO-033; print fit coupons. Define BO-053 internal-frame attachment and the service-panel screw/pilot specification; qualify inserts and the front-left cassette captive nut, and prove loaded joint retention, panel stiffness, shell removal and actual driver access.
2. **Compute and cooling:** verify the Pi/Active Cooler mounting and pin-tip clearance, tray insertion and screw engagement. Add the GPIO24 fan switch and `J9-4` to the PCB-09 schematic (CA-06 CR-02), then measure air temperatures, Pi throttling, cooler RPM and microphone noise in the closed body with the fan on and off. Replace the 29.5 g tray/fixings and 15 g fan CAD estimates with measured masses and recheck stability.
3. **Yaw stage:** select and load-rate BO-044, BO-048 and BO-050, detail gear teeth, material and bearing/servo retention, and validate head-sweep, backlash, life and cable twist. PCB-08/09 and the head-harness service path remain on HOLD.
4. **Order and measure the speaker:** order BO-001. Caliper and weigh it against Ø50 × 18 mm and 48 g, then update `BODY_AUDIO`. The element14 India price and stock were not read on 2026-10-03.
5. **Bench audio:** order BO-007 with BO-001 and check its SD pull-up on receipt. Listen first, then Pi 5 two-lane capture plus playback on one i2s0: `arecord -c 4` and `aplay` together, a tap test per mic port, and an hour with no xruns.
6. **Boards and pins:** schematics and layouts for PCB-05 and PCB-06 are not started. Settle whether 5 V reaches PCB-05 on W12 only, or also on GH10. Approve `CA-06` CR-01 for GPIO22 (SDI1) and GPIO23 (`AMP_SD`).
7. **Acoustic and seal coupons:** prove the speaker flange bond, front-panel seal, mic boss seat/pilots/gasket seal and trim adhesive. Test speaker-to-mic coupling (RP-05 `AR-60`), cooler and drive noise (`AR-61` to `AR-63`), and low-end response in the 15.5 mm cavity.
8. **Board orders:** define BO-054 board retention; get PCB-05/06/08/09/13 schematics, layout, assembly plans and quotes. IM73D122 mics come as cut tape or are sourced by the assembler, since reels are 5000.
9. **Charge inlet and power button:** qualify PCB-13's programmed PD profiles and rear-panel fit. Order BO-018, measure its well fit and confirm momentary 1NO contact; weigh it and run bench PB-01 to PB-06.
