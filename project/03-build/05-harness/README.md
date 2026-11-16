# 05 — Harness: chassis wiring and D-107 head umbilical

| Field | Value |
|---|---|
| Status | **Released for build with conditions**, 2026-11-15 ([D-108](../decisions.md#d-108)): the builder lifted the 2026-11-07 electrical HOLD, accepting the §6 ~16 A all-loads-stalled screen as unlikely. Conditions: W02P stays unbuilt until CH-103 tap protection; no R010 in the switched-bus path; one closed-body 30-minute normal-duty heat check of M1 (< 70 °C) at first power-up. No wire cut, crimped or tested yet; lengths are estimates |
| Basis | [D-093](../decisions.md#d-093), [D-094](../decisions.md#d-094), [D-095](../decisions.md#d-095), [module selection](../module-selection.md), [simplification plan](../simplification-plan.md#44-harness), final-v1 CAD |
| Scope | Installed body/chassis wiring and D107 W47 head wiring (§4.3) |
| Evidence | `D` vendor/documented, `E` estimate, `U` verify on receipt, `W` measured. No `W` values yet |

PCB-02/03/04/05/06/07/13 are superseded. The remaining custom boards keep their designed connectors; bought modules get soldered pigtails to those connectors. All lengths below are millimetres.

## 1. Decisions

| ID | Decision |
|---|---|
| H-01 | The 15 A fuse remains on the chassis front. Its output crosses the body joint once, then forms an **unswitched** charge splice in the rear bay. The rear-panel XT30 and M1 VIN leave that splice. Pack negative reaches the matching rear negative splice and XT30 negative. Charge current bypasses M1 and M6. |
| H-02 | `J-PK` is the isolator. Unplug the charger and open `J-PK` before changing any other power connection. M1 OFF does **not** de-energize the charge splice. |
| H-03 | An insulated, supported AWG16 positive star lies beside M6 in the rear bay, **after** M6 `IN−`; a matching negative star lies beside it. One positive/negative feeder crosses to a tub-plate distribution feeding both #3297 drivers and M2/M3. M4/M5 branch in the body. Rated multiwire crimp splices are used, with no exposed bus bar. |
| H-04 | Micro-Fit+ carries AWG16/18, Micro-Fit 3.0 AWG20–24, GH purchased pre-crimped signal leads. Balance PA/XH contacts are bought as **pre-crimped AWG24 leads** and joined with staggered solder and adhesive sleeve; no PA crimp tool for one break. Qualify each joint by pull test. |
| H-05 | Micro-Fit+ uses thin-wall UL1061-class wire, insulation OD ≤2.0 mm. Do not substitute silicone wire. Exact housing/contact/tool combinations must be checked at order. |
| H-06 | Head power remains `J8-1` Micro-Fit 3.0 2×3. Yaw is PCB-08 `J8-8` 5264-3P; check actual cable orientation before energizing. |
| H-07 | JST PA 3-way replaces the NTC/SM break in the pack channel. The body lead follows D-095 `M12_BALANCE_*_RESERVE`: channel loop, Ø5 front-deck hole, under left driver and cross rail, rear XHP-3 port. |
| H-08 | After pack removal, **11 body-lift plugs**: fused feed, switched chassis feeder, two S18 outputs, and seven signals (`W29/30/31/32/33/34/36`). The PA and `J-PK` were opened for pack removal. No bulkhead. Accessibility and slack are first-build checks. |
| H-09 | Encoders remain on C3 3V3. PCB-10 `J10-12` stays unmated. No old permit, arm, NTC or PCB-02 signal is carried. |

## 2. Power tree as wired

```text
CHASSIS                                     BODY / REAR PANEL
cells → PCB-01 → W01 → J-PK → W03a → FUSE 15 A → W03b → J-BAT → (+) charge splice ┬→ XT30 charge + (unswitched)
       balance taps → W02P → PA 3p → W02B → XHP-3                         └→ M1 VIN → VOUT → M6 IN+ → SHUNT (OPEN) → IN− → +STAR
pack − ─────────────────────────── J-PK − ───────────── J-BAT − → (−) charge splice ─→ XT30 −                  → −STAR

+/− STAR ┬→ J-CHASSIS → tub distribution ┬→ #3297 L/R VM/GND (SMBJ8.5A + 100 µF + 0.1 µF at each VM)
         │                               ├→ M2 S18V20ALV 6.3 V → W13 → J8-1 → pitch/roll
         │                               └→ M3 S18V20ALV 11.1 V → W17 → PCB-08 J8-8 → W15 yaw
         ├→ M4 S13V30F5 5 V → W10 USB-C → Pi 5
         └→ M5 S13V30F5 5 V ┬→ W11 + SS34 → C3 J10-1
                            ├→ W12 → MAX98357A amp
                            └→ W14 → J8-1 C2/display
```

M6 measures the **entire switched positive bus**, but its shunt value is **OPEN (CH-099)**. An INA226 with R010 (10 mΩ) and ±81.92 mV shunt range clips above about **8.2 A**; at the §6 ~16 A screen it dissipates **2.56 W**, beyond the originally proposed ≥1 W minimum. **Do not fit R010 in the full switched-bus path.** A 5 mΩ shunt rated ≥2 W is a candidate: it would dissipate 1.28 W at 16 A and reach full scale at 16.4 A, leaving little measurement margin. Use an independent current probe for N1–N3 peak waveforms, then select and calibrate a shunt/module after the measured peaks and thermal duty are known. An R010 board is useful only on an isolated, current-limited bench load within its verified range and rating. The chassis negative return runs through `J-CHASSIS` to the rear negative star, then `J-BAT`/`J-PK` to the pack. Charger connects to both rear ports only with M1 OFF.

## 3. Connector families and parts

| Family | Fitted use and count | Parts and tooling |
|---|---|---|
| Micro-Fit+ | `J-PK`, `J-BAT`, `J-CHASSIS`: three 2-way pairs, 12 total contacts across both halves | AWG16 UL1061 red/black; 206460/215953 contact series and mating housings, exact gender and PN to confirm. Molex 213309-4400 16/18 AWG tool or professionally terminated pairs. Distinct keys/labels for three unlike supplies |
| Micro-Fit 3.0 | `J8-1` 6 harness contacts, `J10-1` 2, two motor 2-way inline pairs 8 across both halves, two S18 output body-lift pairs 8 across both halves: **24 harness contacts**; fixed board-header pins are separate | AWG20–24; 43030-0007 female / matching 43031 male and 43025/43645/43640 housings; verify AWG20 terminal/tool compatibility and exact keys. Check 63819-0900 tool PN |
| JST GH | Existing board-facing signals; W26 GH10 **still required** | GHR housings and bought pre-crimped AWG28 leads, solder/sleeve at module ends. No GH tool |
| JST PA | One 3-way pack balance break | PAP-03V-S/PALR-03VF and SPHD/SPAL **pre-crimped AWG24** tails. Check received mating size and latch against D-095 channel |
| JST XH | Rear-panel balance port | XHP-3 and SXH pre-crimped AWG24 leads; check charger mate and cell order |
| XT30 | Rear-panel **female** charge port, one; XT60→XT30 charger adapter | Two insulated AWG16 solder-cup leads; print polarity on panel; strain relieve |
| Feetech 5264-3P | PCB-08 `J8-8` to ST3215-HS | Vendor servo lead; verify cavity orientation |
| Splices and passives | Rear charge pair, rear star pair, tub branch pair; M13 | **Rated sealed multiwire AWG16 splices** selected for actual wire count/cross-section; never force multiple wires into a single-wire butt barrel. Two SMBJ8.5A, two 100 µF ≥16 V, two 0.1 µF at VM; SS34-class W11 diode; audio hub resistors |

The fuse, holder, PCB-01 and cell breaker retain prior selections. The table defines families and counts for Level 6; choose exact orderable PNs after sample mating and pull tests.

## 4. Wire list

**Chassis CAD view (2026-11-15).** `final/v1/cad/chassis_harness.py` adds
`Harness → Chassis wires` beside `Harness → Head wires` in the whole-robot
inspection model. It contains 34 labelled, insulated wire/cable envelopes plus
two nominal tub-splice envelopes. The earlier power/sensor runs follow D-106
corridors and the D-095 balance channel; W29–W33 use the new neutral-pose
signal paths. `chassis-harness.step.py` is a
focused review entry. The route boxes remain visible under `Bought modules →
D-106 chassis harness routes` as *reserves*, distinct from the installed-wire
view. The coloured geometry is a nominal routing sketch, **not** a measured
cut length, accepted bend, conductor separation, electrical release, or a
replacement for the physical harness check.

| CAD labels | What they carry |
|---|---|
| `W01` / `W02P` / `W02B` | Protected pack main +/− to J-PK; three unfused cell taps to the PA break, then to the rear XHP-3 balance port. Cell-end protection is still unplaced |
| `W03a` / `W03b` | J-PK positive to the front 15 A fuse; pack negative to J-BAT; fuse output back to J-BAT positive |
| `W05c` / `W05t` / `HN006` | Switched +/− through J-CHASSIS to the tub plate, then the M2/M3 input distribution. Two Ø6.5 × 24 mm insulated splice envelopes are placed above the CH-106 rear arms; their actual rated parts and fan-out are still open |
| `W06` / `W07` | Tub distribution +/− to left/right motor-driver VM and GND |
| `W08` / `W09` | Left/right driver outputs through their inline motor plugs to the motors |
| `W13` / `W17` | M2 6.3 V head rail and M3 11.1 V yaw rail, each with its return, to their body-lift plugs |
| `W29` | C3 J10-7 GH8 to the IMU. One outer cable envelope represents its eight conductors |
| `W30` / `W31` | Left/right motor encoder signals to C3 J10-3/J10-4 GH4. These are separate from the motor power pairs |
| `W32` / `W33` | Left/right motor-driver logic to C3 J10-5/J10-6 GH6. These do not carry motor VM |
| `W34` / `W36` | Nose Hall/touch GH5 cable to J10-8; rear TCRT GH4 cable to J10-10. Each appears as one outer cable envelope because the bores do not define core spacing |

`W29`–`W33` now have continuous neutral-pose CAD paths to their GH plugs.
The chassis-side source exit, clips, body-lift slack and separation from live
motor leads still need a physical dressing check. The HN-006 bodies are
**placement envelopes**, not selected splices; W05c and W05t do not yet form
an electrically complete fan-out at them. Pack cell-end joints, balance-tap
protection and exact module-pad terminations also remain open. The visible
shapes are routing aids; the wire list and terminations remain the tables below.

Lengths are `E` cut allowances with service loop, **not measured CAD centerlines**. String-route and record `W` lengths on the assembled robot before cutting. At every module, solder to its *marked* VIN/GND/VOUT or signal pad, photograph pad labels and support the tail so the pad carries no cable strain. Leave ≥40 mm withdrawable slack at body-lift plugs.

### 4.1 Pack and power

| ID | From → to / termination | Conductors; E cut | Route and check |
|---|---|---|---|
| `W01` | Pack protected +/− → `J-PK` pack half, solder/MF+ | 2×AWG16; 120 | Tub window; 1:+, 2:− |
| `W02P` | Cell taps B−/mid/B+ → PA PAP half, solder/pre-crimp tails | 3×AWG24; 110 each | D-095 pack reserves beside W01. These taps bypass PCB-01's main power path and the 15 A fuse; **do not build** until a cell-end short-protection method, compatible with charger balancing/sensing, is selected and checked |
| `W02B` | PA PALR half → rear XHP-3, pre-crimp/joined | 3×AWG24; 390 each | D-095 loop, deck hole X52/Y47.4, under left driver/cross rail; meter each cell at port |
| `W03a` | `J-PK` body half → fuse input | AWG16 +; 110 | Front channel. Negative `W03a−` AWG16 to J-BAT −, E 270 |
| `W03b` | Fuse output → `J-BAT` chassis half | AWG16 +; 250 | Front X52–82 to rear X−50, supported +Y; old W03d corridor reused |
| `W03r` | `J-BAT` body half → rear +/− charge splices | 2×AWG16; 60 | Rear bay strain relief |
| `W04` | Unswitched charge splices → female XT30 | 2×AWG16; 100 | Rear panel. A keyed AWG16 2-pole service pair is required **if** the panel cannot rest safely within this loop; mock up before build. Old W04 meaning retired |
| `W05` | +splice→M1 VIN; M1 VOUT→M6 IN+; M6 IN−→+STAR; −splice→M1 GND/−STAR | AWG16; 40/80/60/100 | Rear bay; solder/screw at received module terminals, insulated and tie-supported |
| `W05c` | +/−STAR → `J-CHASSIS` → tub distribution | 2×AWG16; 310 | Rear to front, one body-lift pair; sealed multiwire branch |
| `W05b` | Body +/−STAR → M4 and M5 VIN/GND pads | 2×AWG18 per module; E 180 each | Down to under-tray modules. Each branch is independent and strain-relieved; check peak input current against AWG18 and splice capacity |
| `W05t` | Tub +/−distribution → M2 and M3 VIN/GND pads | 2×AWG18 per module; E 110 each | Front tub plate; keep input and output leads on separate labelled sides, verify pad bend clearance |
| `W05s` | M5 VOUT/GND pads → insulated shared-5 V +/− distribution | 2×AWG18; E 60 | One supported pigtail pair leaves M5; W11/W12/W14 branch at rated multiwire splices so the module pads do not carry three cables |
| `W06/07` | Tub branch → #3297 L/R VM/GND pads | 2×AWG18 each; 90 | VM TVS/bulk/ceramic **at each driver** |
| `W08/09` | #3297 paralleled outputs → MOT3001 via existing MF3 inline | 2×AWG22 each; 230 | Existing motor route/tie; the right inline pair sits on top of the right board (D-106: its D-031 place is PCB-10), verify forward polarity |
| `W10` | M4 VOUT/GND → Pi right-angle USB-C solder plug | 2×AWG18; 100 | Under tray; ≤13 mm shell overhang, 56 kΩ Rp CC-to-VBUS per CN-03; N12 |
| `W11` | M5 VOUT→SS34 anode→cathode→C3 `J10-1.1`; GND→.2 | 2×AWG22; 110 | Diode beside M5, **stripe toward C3**, separately sleeved/tied; N8. **Ordered 2026-11-08: Slkor SS34, SMA (DO-214AC) SMD**, so no leads: tin both pads, solder the AWG22 wires flat along the body, then pot the joint in epoxy or hot glue under heat-shrink so the wires cannot lever on the pads |
| `W12` | M5 VOUT/GND → M8 amp VIN/GND pins | 2×AWG22; 160 | Amp bracket; solder and strain relief |
| `W13` | M2 VOUT/GND → `J-S18-H` body-lift MF3 → `J8-1.1/.4` | 2×AWG20; 250 | Tub plate to −Y head riser; N2 head stall |
| `W14` | M5 VOUT/GND → `J8-1.2/.5` and `.3/.6` | 4×AWG22; 140 | Independent C2/display pairs in riser sleeve |
| `W17` | M3 VOUT/GND → `J-S18-Y` body-lift MF3 → PCB-08 yaw power pads | 2×AWG20; 250 | Tub plate to body; PCB-08 schematic must provide labelled 11.1 V landing pads |
| `W15` | PCB-08 `J8-8` → ST3215-HS | Vendor 3-wire; 120 target | Restrain excess outside cassette; confirm orientation |

`W02a/b`, old `W03c/d`, old OPBUS/CHGBUS `W05`, and `W16` are deleted. New W04 and W05 reuse numbers only after explicitly retiring their former functions.

### 4.2 Signals and audio

| ID | From → to | Length / build |
|---|---|---|
| `W24` | PCB-09 `J9-1` ↔ PCB-08 `J8-4`, head RS-422 | Existing GH6 1:1, 170 |
| `W25` | PCB-09 `J9-2` ↔ C3 `J10-2`, base RS-422 | Existing GH6 1:1, 200 |
| `W26` | PCB-09 `J9-3` GH10 → audio-hub perfboard | GH10 pre-crimp at PCB-09, solder at hub, E 160. Pin 10 remains isolated test pad, **never 5 V or a GPIO** |
| `W27` | Hub → four INMP441 breakout pads | **6×AWG28 per mic**: VDD, GND, SCK, WS, SD, L/R. E 250 front / 190 rear, revise from CAD pigtail reserves. Front pair shares SDI0, rear pair SDI1; opposite L/R straps within each pair |
| `W28` | M8 amp screw terminal → speaker | Twisted 2×AWG22, E 100, mark polarity |
| `W29` | C3 `J10-7` GH8 → M7 LSM6DSOX solder pads | E 220. Pins 1–8: +3V3→VIN, GND, SCLK→SCK, MOSI→SDA/SI, MISO←DO, CS, INT1, INT2. Verify module pad lettering; no IMU-end GH8 |
| `W30/31` | MOT3001 encoder → `J10-3/.4` | Existing GH4 220/230, 3V3 |
| `W32/33` | #3297 logic → `J10-5/.6` | Existing GH6 180/80 |
| `W34` | Nose sensor/Hall → `J10-8` | Existing GH5 220 |
| `W36` | Rear TCRT → `J10-10` | Existing GH4 CH-020, 350 |
| `W40` | Mushroom NO → M1 ON/GND; qualified button-sense output → PCB-09 rev B GPIO12 (physical 32); PCB-09 rev B GPIO13 (physical 33) → M1 OFF interface | E 150 switch pair + 220 tap/control, carried on J6 pins 5/6 through a **detachable rear service break before the W40/W44 split**. **Do not wire M1 ON straight to Pi**: its idle voltage may follow pack. Measure pull-up and add a high-impedance divider/buffer giving valid 0–3.3 V logic over 6.0–8.4 V pack without back-powering an unpowered Pi. Verify the GPIO13 inactive state through reset/boot/halt, OFF drive voltage and pulse length, and no M1-to-Pi injection when off; buffer if needed. Firmware must complete its storage shutdown steps before pulsing OFF; test under N1. [D-098](../decisions.md#d-098) selects PCB-09 rev B; no piggyback/header contact or J9-3 spare |
| `W41` | Fan → PCB-09 `J9-4` | Existing GH2 / GPIO24 switch |
| `W44` | M6 SDA/SCL/VCC/GND → PCB-09 rev B service termination → Pi `i2c-gpio`/3V3/GND | 4×AWG28, E 160, carried on J6 pins 1–4 through the **same detachable rear service break as W40**. Pi physical 36 / GPIO16 is SDA and 37 / GPIO26 is SCL, with 4.7 kΩ pull-ups on PCB-09. Rev A I²C1 TP1/TP2/TP5 are 1 mm probe pads and stay outside this harness. Use only the designed, strain-relieved rev B interface after fit and continuity checks ([D-098 amendment](../decisions.md#d-098)). No 5 V I²C. Set/verify address 0x40 unless occupied |

**Draft J6 GH6 lead:** one pre-crimped six-way lead leaves PCB-09 and reaches a detachable six-circuit service break at the rear-bay plate, then splits into W44's INA226 four wires and W40's button/OFF pair. This choice avoids storing about 90 mm of extra cable for the tray slide. Rev B CAD places J6 at the +X extension and checks a 3 mm lead corridor via world Y 20 and Z 118 to the rear buffer volume. Choose and CAD-fit the rear connector and its support before building this harness; the current CAD check covers the lead corridor and buffer reserve, not that connector. Freeze lead length, split support and strain relief after the populated fit and pull test.

**Tray assembly and service order:** (1) mate J6 on the bench with the rear service break open; (2) slide the Pi/tray assembly into the body while the free lead follows the checked corridor; (3) dress and secure the lead at the rear bay; (4) mate the rear service break, then connect the W44 and W40 tails. For tray removal, open the rear service break before sliding the tray out. Do not pull on soldered INA226 or buffer joints.

| J6 pin | Net | Rear destination |
|---|---|---|
| 1 | +3V3_PI | M6 VCC |
| 2 | I2C_GPIO_SDA | M6 SDA |
| 3 | I2C_GPIO_SCL | M6 SCL |
| 4 | GND | M6 GND |
| 5 | BTN_SENSE | Rear button buffer output |
| 6 | PWR_OFF | M1 OFF input interface |

`W20`, `W21`, `W23a/b`, `W39`, and old NTC GH2 are deleted. GH pre-crimp buy: GH2 W41; GH4 W30/31 plus CH-020 W36; GH5 W34; GH6 W24/25 double-ended, W32/33 single-ended and one single-ended J6 lead shared by W40/W44; GH8 W29 single-ended; **GH10 one single-ended W26**. Buy one spare per fitted size after measured stock lengths are chosen.

**Audio hub, solder side concept (freeze after N9):**

```text
J9-3 → [3V3/GND rails]  BCLK ─┬─33–100 Ω→ FL SCK  ┬─33–100 Ω→ FR SCK
                              └─33–100 Ω→ RL SCK  ┴─33–100 Ω→ RR SCK
          LRCLK ─ four separate 33–100 Ω branches → four WS pads
          SDI0 ← front pair SD, 100 kΩ to GND at hub
          SDI1 ← rear pair SD, 100 kΩ to GND at hub
          SDO0 → amp DIN; AMP_SD → amp SD
          pin 10 → isolated labelled pad only
```

Hub pads 1–10 follow `J9-3`: 3V3, LRCLK, GND, BCLK, GND, SDO0, SDI1, SDI0, AMP_SD, isolated. Each mic gets 3V3/GND; its **sixth conductor** carries the chosen hub-side 3V3 or GND strap to L/R. Strap one low and one high within each pair; label all four tails. Check actual channel assignment, clock edges and all four simultaneous captures (N9/N11). Measure 3V3 draw; prior PCB-09 audio allowance was 15 mA.

### 4.3 W47 head umbilical (D-107)

W47 replaces W37/W42/W43/W45/W46, PCB-14/16 and the hollow trunnion. Twelve loose silicone wires and the B0091 HDMI inner conductors rise through the yaw-axis bore. The 95 mm neck span has no jacket, hose or tight sleeve. The physical wire/HDMI combination must pass C0 and C4; the solver is geometric evidence only.

| Net | Wire | PCB-08 rev B body end | Head end |
|---|---|---|---|
| +6V3_HEAD_PR | AWG22 | J8-9.1 | Servo pin2 |
| +5V_C2 | AWG26 | J8-9.2 | PCB-12 J1.6 |
| +5V_DISPLAY | AWG26 | J8-9.3 | D1 power+ (K3 inlet to verify) |
| GND_HEAD | AWG22 | J8-9.4 | Servo pin1; AWG28 branch PCB-12 J2.1 |
| GND_C2 | AWG26 | J8-9.5 | PCB-12 J1.7 |
| GND_DISPLAY | AWG26 | J8-9.6 | D1 power− |
| GND_SIG | AWG28 | J8-10.1 | PCB-12 J1.1 |
| C0TX+ / C0TX− | AWG28 pair | J8-10.2 / .3 | PCB-12 J1.2 / .3 |
| C2TX− / C2TX+ | AWG28 pair | J8-10.4 / .5 | PCB-12 J1.4 / .5 |
| SERVO_DATA | AWG28 | J8-10.6 | Servo pin3; branch PCB-12 J2.2 in the head |
| Camera | HDMI inner pairs | B0091 body board | B0091 head board → HD-026150mm static15-way ribbon → SC0874 |

J8-9 mirrors J8-1. PCB-08 keeps all three power returns separate; LINK_GND reaches GND_SIG through R1. PCB-12 bonds signal, servo reference and display return to its local GND through R1/R7/R10. The exported-netlist audit is `04-pcbs/pcb-08-yaw-junction/design/audit_w47.py`. C2 status LED driver K2 remains a PCB-12 order hold.

The corrected collar is at head-local X−50.4,Y0,Z6, with a 34×30.2 mm underside opening. Z13 failed the exact full-length bundle check at full roll. The flared bushing and liner leave Ø18 clear. Do not restore the source's cassette, PCB-14 posts, PCB-16 pockets, leg channel or camera mast.

## 5. Pinouts and polarity

Pin 1 means the **moulded cavity number**, not the leftmost cavity in a photograph. Meter every cable from cells to exposed ports before connecting a charger. Print `+`, `−`, `B−`, `BM`, `B+` next to rear ports at print stage.

| Interface | Pin / pad map |
|---|---|
| `J-PK`, `J-BAT`, `J-CHASSIS` 2-way | 1 positive, 2 negative. Respectively protected pack, fused unswitched, switched shunt-monitored. Give unlike feeds distinct keys/labels |
| M1 #2813 | VIN from charge +splice; GND from −splice; VOUT to M6 IN+; ON from mushroom NO-to-GND; OFF from verified Pi GPIO interface; CTRL unused. Check received board hole labels |
| M6 INA226 (shunt OPEN, CH-099) | IN+ M1 VOUT, IN− +STAR, bus voltage sense at IN− if separate pad exists; VCC Pi 3V3, GND −STAR, SDA/SCL PCB-09 `i2c-gpio` bus. Check board trace/jumper arrangement; choose and calibrate shunt after peak measurements |
| M2/M3 S18V20ALV | VIN+/GND from tub branch; VOUT+/GND to W13 6.3 V (D-100 amendment; was 6.0 V) or W17 11.1 V. Label setpoints at modules |
| M4/M5 S13V30F5 | VIN+/GND from body stars; M4 VOUT Pi-only 5 V; M5 VOUT shared 5 V. Keep outputs separate |
| `J8-1` MF3 2×3 | 1 +6V3_HEAD_PR (D-100; was +5V5_HEAD_PR), 2 +5V_C2, 3 +5V_DISPLAY, 4 GND_HEAD, 5 GND_C2, 6 GND_DISPLAY |
| `J8-9` MF3 2×3 | Same numbered net map as J8-1; head output W47 |
| `J8-10` GH6 | 1 GND_SIG, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+, 6 SERVO_DATA |
| `J10-1` MF3 2-way | 1 +5V_C3 **after Schottky**, 2 GND |
| PCB-08 `J8-8` 5264-3P | 1 GND, 2 +11V1_YAW, 3 SERVO_DATA, after received cable orientation check |
| PA break and XHP-3 | Cavity 1 B−, 2 BM, 3 B+ on both halves **by cavity number**. Exposed XHP-3: 1→2 and 2→3 each one cell; 1→3 full pack. Confirm charger plug key and its cavity order |
| XT30 female | Moulded + fused unswitched positive, moulded − pack negative; recessed source contacts, epoxied/retained and strain-relieved |
| `J9-3` GH10 | 1 3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 isolated sense pad |
| `J10-7` GH8 | 1 3V3, 2 GND, 3 SCLK, 4 MOSI, 5 MISO, 6 CS, 7 INT1, 8 INT2 |
| PCB-12 `J1` GH7 (D-102) | 1 GND_SIG, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+ (J9-1 order), 6 +5V_C2, 7 GND_C2. From W47 direct wire fan-out (§4.3) |
| PCB-12 `J2` GH2 | 1 GND_HEAD reference, 2 SERVO_DATA. Servo power does not pass PCB-12 |
| PCB-12 `J3` GH3 | 1 GND_DISPLAY, 2 RS-485 B, 3 RS-485 A, to D1's RS-485 port; check D1's terminal labels before crimping |

`J9-1/2`, `J10-2/3/4/5/6/8/10`, `J8-4/9/10` keep their designed-board maps. No J2/J3/J4/J5 or PCB-13 header is fitted. PCB-10 `J10-12` exists but is unmated.

## 6. Electrical and mass estimates

AWG16/18/20/22 resistance at 20 °C: 13.2/21/33.3/53 mΩ/m; ×1.16 hot. These **screening estimates** omit unknown solder, fuse holder, splices and module losses. Micro-Fit+ contact assumed 2.5 mΩ typical or 10 mΩ maximum per mated contact. Two-way power pairs have a positive and return contact. Four-wire test the assembled pack-to-star and pack-to-driver paths at 5 A.

| Segment | Hot round-trip copper | Typical/max MF+ contacts | Drop at current, before omitted losses |
|---|---:|---:|---:|
| J-PK→fuse→rear splice: + 0.11+0.25 m, − 0.27 m AWG16 | 9.7 mΩ | J-PK + J-BAT: 10/40 mΩ | **0.315/0.795 V at 16 A demand** |
| Rear M1/M6/star, ~0.24 m + and 0.10 m − AWG16 | 5.2 mΩ | none | 0.083 V at 16 A, **plus** M1 and the open M6 shunt choice (5 mΩ candidate: 0.080 V at 16 A) |
| Star→tub 0.31 m each way AWG16 | 9.5 mΩ | J-CHASSIS: 5/20 mΩ | 0.171/0.348 V at 11.8 A illustrative chassis demand |
| Tub→each driver 0.09 m each way AWG18 | 4.4 mΩ | none | 0.009 V at 2 A each |
| M2/M3→body 0.25 m each way AWG20 | 19.3 mΩ | MF3 resistance unmeasured | 0.054 V at 2.8 A head; 0.046 V at 2.4 A yaw, before connector/W47 |
| M4→Pi 0.10 m each way AWG18 | 4.9 mΩ | USB-C loss unknown | 0.015 V at 3 A; N12 measures Pi input |
| M5→C3 0.11 m each way AWG22 | 13.5 mΩ | MF3 and diode unknown | N8 measures loaded voltage/back-feed |

**D-093 low-pack current screen, 6.0 V input, assumed 90% conversion efficiency (`E`):** Pi 5 V × 3 A → 2.78 A pack; head 5.5 V × 2.8 A → 2.85 A; yaw 11.1 V × 2.4 A → 4.93 A; shared 5 V × 1.5 A → 1.39 A; both drives at the old 2 A each → 4.0 A. **Sum ≈15.95 A demand** (≈11.39 A at 8.4 V with the same output loads/efficiency). This is a coincident-stall *demand*, not a claim the chosen M2/M3 can deliver it: their ~2 A output capability may collapse first. Even limiting head and yaw outputs to 2 A yields about **14.3 A** at 6 V under the same assumptions. The former 10.2 A came from a superseded rail configuration and cannot size this harness. **[D-100](../decisions.md#d-100) sets M2 to 6.3 V** with the head limited to ≤ 2.4 A in total: 6.3 V × 2.4 A → 2.80 A pack, below the 2.85 A head term above, so the screen is not raised; the unlimited 6.3 V × 2.8 A case would be 3.27 A. M2 current delivery at the 6.0 V low-pack point remains an N2(b) gate.

**Duration-based design candidate, not a new limit:** if both head servos are proved to stay at or below 1.0 A each and yaw at or below 1.5 A **from the first instant of a stall**, the same arithmetic gives about **13.0 A** at a true 6.0 V *module input*. Feetech's protection-current register and overload timeout must not be assumed to be an instantaneous current regulator; measure current waveforms, persistence after power cycle, fault reset and torque/speed on the received servos. An 8 A continuous / ≤2 s peak budget is only a proposal until the real duty cycle, closed-body temperatures and source sag are measured. At 6.0 V **open-circuit** pack voltage, the old 84 mΩ pack estimate implies 1.09 V sag already at 13 A, so treating 6.0 V as both open-circuit and module-input voltage understates converter input current. Define the voltage observation point before adopting either number.

At the 16 A demand screen, the table sums to **0.558/1.038 V** typical/contact-maximum pack-to-M4/M5 input, **0.729/1.386 V** pack-to-M2/M3 input, and about **0.738/1.395 V** pack-to-driver VM; these exclude fuse/holder, PCB-01, M1, splices, pads and temperature rise beyond the 1.16 factor. The electrical path therefore needs redesign or a proved, enforced load/current envelope before release. Output copper adds 0.054 V head or 0.046 V yaw at the cited stall currents, plus MF3/FFC; M4 output adds 0.015 V at 3 A plus USB-C loss. Measure at the 6.0 V low-pack threshold and recompute from logged simultaneous branch currents.

`J-PK`, fuse, `J-BAT`, M1 and the charge splice face the ~16 A demand screen, **above** the harness's assumed 13 A Micro-Fit+ AWG16 contact rating and nominal 15 A fuse. The HP switch's 16 A vendor figure is at a 150 °C board, unacceptable in the PETG bay; N1 must establish a lower safe limit. Check fuse/holder time-current coordination and every connector's derated current, then enforce servo/drive limits and measure the coincident load. Charging in **OFF** instead carries only the selected charger's 1–2 A through J-PK/fuse/J-BAT/charge splice; XT30 carries charge current and the balance contacts carry balancing current. Charging while ON is prohibited, so charge current is not added to the operating case. Validate charger behavior if either main lead or balance lead disconnects. M3's ~2 A capability is below 2.4 A yaw lock; M2's ~2 A is below 2.8 A head stall. N2(b), N3 and N12 gate those rails.

The **13 A Micro-Fit+ value is a continuous temperature-rise rating**, not an immediate trip threshold; a 16 A pulse is not automatically unacceptable. Its temperature rise after repeated pulses in the actual two-way wire-to-wire housings is unmeasured. [Molex's specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/206/206460/2064600000-PS-000.pdf?inline=) calls for ambient/circuit derating. [Littelfuse's ATOF data](https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/automotive-fuses/blade-fuses-shunt/atof/287/0287015-l) makes 15 A the nominal part; the series time-current and ambient derating must be applied to the installed holder, not inferred from the label. [Pololu's #2813 data](https://www.pololu.com/product/2813/specs) calls 16 A continuous only at a **150 °C board**; its detailed thermal table gives **6 A at 55 °C** in 22 °C still air. N1 must log 8 A continuous and 13–16 A pulses in the **closed PETG body** before accepting a proposed duty budget.

**Balance-lead fault path:** W02P/B connects the cell taps to an external panel port **ahead of** the main fuse and PCB-01's output FETs. A short between balance cavities can draw cell current through AWG24 without the main fuse clearing it. Before fabrication, select and bench-check cell-end protection and wire/connector current limits against the chosen charger's sense and balancing behaviour. N5 must include reversed/mis-seated plug prevention, one open balance wire, main-lead disconnected and adjacent balance-pin short tests with a current-limited cell simulator, not live cells for fault injection. The D-095 CAD clearance checks do not establish electrical fault safety.

**Cell-end fuse candidate:** one suitably DC-rated fuse per balance tap close to the cell is a plausible way to protect the long AWG24 lead; [Batrium's cell-monitor wiring guidance](https://wiki.batrium.com/en/product/cell-monitor/cellmate-k9) uses this pattern for larger packs. It is **not yet a three-part BOM selection** for Makad. Choose actual fuse clearing current/time, DC interrupt rating, cold resistance and construction against the selected charger's balance current and the cell fault source. An open tap must be detected before charging; check that a fuse opening cannot cause the charger to apply the wrong cell voltage. Add the three fuse bodies, joints, insulation and strain relief to pack CAD and mass before claiming D-095's channel and tub clearances still pass. A resettable PTC is not interchangeable with a one-shot fuse without its hot-state leakage and trip-time analysis.

**Mass:** former ~73 g harness estimate excluded pack, IMU, TCRT and audio. New working allowance: ~52 g insulated conductors plus ~35 g connectors/splices/sleeve/ties = **~87 g (`E`)**, excluding W01 pack, W02 balance, W04 charge, W26–29 audio/IMU and CH-020 TCRT. This is a provisional +14 g to the former harness row, **not** an addition to the separate balance/charge rows already counted by D-095. Weigh the built sets and reconcile the whole-robot mass register at Level 7.

## 7. Service procedures

### 7.1 Pack out and charge

1. Orderly shutdown, verify M1 OFF and remove **both** charger leads. Open `J-PK` before touching any other power connector.
2. Remove J11A hatch screws and lower the strapped pack. Bring `J-PK` into the tub window and separate it.
3. Draw the PA break to the tub window and unlatch it. Pull the **pack half** back through the window; leave body half and rear port in place.
4. Refit PA first with cavity order checked, then `J-PK` last, charger absent.

For in-place charging: M1 **OFF**; confirm port polarity; connect charger XT30 and balance plug; select **2S Li-ion 4.20 V/cell, 1–2 A**; charge. Remove both leads before ON or service. Rear panel is not a USB-C charge inlet.

### 7.2 Body off chassis; rear panel off

1. Do pack-out steps 1–3, remove shell and support body.
2. For rear-panel removal, separate W04 at a selected AWG16 service pair **or** lay panel beside body within its verified service loop. Unpark XHP-3 lead only if it obstructs travel; unplug mushroom W40 if its block has a detachable lead. Never pull XT30 cups or balance wires. Charge splice and M1 stay on rear-bay plate.
3. Unmate **four power** body-lift plugs: `J-BAT`, `J-CHASSIS`, `J-S18-H`, `J-S18-Y`. Cap the chassis ends.
4. Unmate **seven signals** at body boards: W29 `J10-7`; W30/31 `J10-3/.4`; W32/33 `J10-5/.6`; W34 `J10-8`; W36 `J10-10`.
5. Confirm no cable crosses the J13 lift plane, undo J13, lift body. Refit by labels; `J-PK` last. Measure far-end rails before drive/servo enable.

The **11** body-lift plugs are counted *after* J-PK and PA pack removal. A fitted rear-panel W04 service pair is additional. Verify hand access, strain relief and ≥40 mm withdrawal slack at first build.

### 7.3 Head off

1. Power off and remove the shell for body-end access.
2. Unplug W47 at PCB-08 J8-9/J8-10 and the HDMI cable at the body B0091. Release the body strain-relief ties.
3. Lift the head and pass the small housings through the Ø18 clear liner one at a time. Verify the received plug sections before assembly. A full-size HDMI housing need not pass: unplug at the head B0091 and leave that cable in the body if required.
4. For cable replacement, remove the head rear cover, unplug the fan-out leads, undo the split jaw and draw the replaceable bundle down through the underside opening. Keep the pivot bearing, pin and retainer installed.

## 8. Schedule change record

| Retired | Replacement |
|---|---|
| NTC W02a/b, SM2, J2-7 | PA W02P/B balance break and XHP-3 |
| PCB-02/03/04/05/06/07/13 headers, old W03c/d, W04/05, W16 | Charge splice, M1/M6, stars, bought modules, new W04/W05 |
| W20, W21, W23a/b, W39 | No cables; J10-12 unmated |
| PCB-05 W26, PDM W27, old amp W28 | GH10 to hub, four six-wire I²S mics, direct breakout speaker |
| PCB-07 GH8 at IMU | Soldered W29 at LSM6DSOX |
| PCB-03 J3-5 yaw | M3→PCB-08 W17, J8-8→yaw W15 |
| Former H-08 body-board list | Four power plus seven signal body-lift plugs |

## 9. Open and acceptance

The [2026-11-15 chassis design review](chassis-design-review.md) separates the
static CAD/planning work completed now from decisions that need selected parts
or measured hardware. The priority list below is the current release checklist.

| Item | Closure |
|---|---|
| Connector order — **open, P1** | Verify MF+ housing gender/key and AWG16 contacts, MF3 AWG20 tool/contacts, PA/XH pre-crimp gauge/mate, multiwire splice capacity. Pull-test three samples per wire/contact combination. Choose W04 panel service pair after extraction mock-up |
| CH-103 balance-tap protection — **open, P0** | Four fixed-geometry rows of three assumed insulated fuse envelopes were screened; none cleared the cells/straps and J-PK. Select a protection method and actual joint/sleeve dimensions, revise the pack-end arrangement, then re-run fit, removal and charger fault checks. [Study and report](../final/v1/cad/study_ch103_fuse_fit.py) |
| HN-006 tub distribution — **placement done; design P1** | Two nominal splice envelopes clear the print and other modeled wires. Each polarity needs one AWG16 feed and four AWG18 outputs (M2, M3, left/right drivers). Select a rated five-wire or staged-splice topology, connect the tails explicitly, then recheck actual body dimensions, support and insulation |
| W04 panel service — **distance screen done; physical P1** | A 40 mm rearward withdrawal puts the CAD splice-to-XT30 inner-body-end separation at 47.6 mm against the 100 mm cut allowance; the actual cup exit, bends and stable panel rest are unproved. Mock up the withdrawal; add a keyed AWG16 break if the supported loop loads the cups or splice |
| CAD reserves — **CAD done; first-build P1** | **Placed 2026-11-07 ([D-099](../decisions.md#d-099)); moved and routed 2026-11-13 ([D-106](../decisions.md#d-106), `check_d106_harness.py` 134/134):** `J-BAT` X −19.5..2.5, Y −31..−22.7, Z 57–67 and `J-CHASSIS` the same X at Y 22.7..31 (drawn 40 mm inward to unmate; 8 mm lead room past both ends); `J-S18-Y` / `J-S18-H` X −3..16 at Y −38..−31 / −45.5..−38.5, Z 59.4–69.4 (unmated in place); chassis half +X, body half −X on all four; the ± star splices along Y above the rail at X −31.75/−25.25, Z 74.25. Every chassis run of §4 is drawn as a reserve chain (`HARNESS_D106_*`): W03a up a new deck slot past J-PK and over the left driver into the fuse; W03b from the fuse back along Y 33–38.5 and the +Y trunk, across the motor bay into J-BAT; W05c to the tub-plate +Y strip; W13/W17 from the −Y strip to the J-S18 chassis ends; W06–W09 (the right motor inline pair now on top of its board); W34 through the restored under-crossmember tunnel; W36 tied at the rear lug. Five more 2.5 mm ties (CH-082): fuse column, two deck lugs, two tub-plate lugs. 2026-11-15 update: nominal HN-006 splice envelopes are placed without printed-part collision, but actual splice selection and fan-out remain open; CH-103 fuse bodies failed the four tested three-fuse pack-exit rows (see design review). Module pad ends and fuse-holder lead height are `E`; string-route W03b/W05c/W13/W17 with modules installed and the body moving, and check hand reach at first build |
| Chassis signal dressing — **CAD done; physical P1** | W29 IMU, W30/W31 motor encoders, and W32/W33 driver logic now have continuous neutral-pose cable envelopes in `Harness → Chassis wires`; printed-part and modeled power-lead intersections clear. Dress and retain the actual leads, check source exits and separation, verify body-lift motion and ≥40 mm withdrawal slack, then replace estimated cuts with measured lengths |
| M6/control interfaces — **open, P0** | Record the received INA226 board's shunt marking/rating, sense routing and I²C address; keep R010 off the full switched bus. Measure N1–N3 peaks independently; select a shunt/module with input-range and thermal margin (5 mΩ ≥2 W is only a candidate), then calibrate against a meter. Measure #2813 ON idle voltage/OFF recognition; qualify GPIO12 buffer and GPIO13 OFF drive. PCB-09 rev B must pass six-net continuity, no-short, populated fit, and strain-relief checks before W40/W44 are built ([D-098](../decisions.md#d-098)) |
| Bench — **open, P0** | N1 switch heat, N2 head/shared rails, N3 yaw, N4 VM, N5 charge/balance fault cases, N8 Schottky/back-feed, N9 audio, N10 IMU, N11 mic timing, N12 Pi voltage: exact setup/pass in [plan §4.12](../simplification-plan.md#412-tests), with the added balance-lead cases in §6. Four-wire pack-to-star/driver at 5 A and hot load drop |
| First build — **open, P1** | Record `W` cut lengths, pad/termination photos, full polarity and balance voltages, 11-plug reach/slack, panel removal path and cable-set masses; reconcile D-095 balance/charge mass rows |

These rows feed the Level 6 BOM. An estimated length, unverified pad or connector family name is not an assembly release.

### D-107 acceptance update (2026-11-13)

The earlier FFC resistance/fold acceptance is superseded. AWG22 copper alone over 0.30 m each way is about0.0318Ω, 0.076V at2.4A (`E`, excludes plugs/PCB). At350mm each way it is about0.0371Ω /0.089V at20°C, or0.0430Ω /0.103V with the §6 hot factor1.16. Review M2's 6.3V setpoint against measured servo voltage; retain N2(b), ground-loop current and servo-bus edge checks. Camera gates C0–C4 are in `head-umbilical-plan.md` §3.5. Inspect bushing and clamp wear after the first hour. K2 LED driver, K3 D1 inlet, crimp/contact selection, received connector sizes and physical cable life remain open.

W47 contact stock: AWG26 power leads need genuine Micro-Fit contacts rated for that gauge; the older AWG20–24 H04 stock alone is insufficient. GH leads must satisfy JST eGH AWG30–26 and insulation OD0.76–1.0mm. Verify actual housings, contact part numbers and crimp tool before cutting wire.


### D107 received-cable corrections —2026-11-14

Static camera ribbons are separate BOM items: HD-026150mm15-way head FFC (route111.20mm +25mm insertion/service), HD-027150mm15-to22 Pi5 FPC (route59.97mm +25mm). B0091’s included60mm15-way ribbons are spares. Check contact faces, continuity, insertion and static excess-length dressing; never tension the sockets.

Buy/measure the entire HDMI plug housing/latch/boot before printing closed inserts: their finished bore is18mm, versus bare21mm. The assumed16×7mm plug is not receipt evidence. If it fails, unplug at the head or separately design/check split inserts. At the head clamp, repack/tape the bundle to6.8±0.05mm; if bare OD>6.85mm revise pads/clamp instead of crushing pairs.

The roll-frame servo anchor is now(−28,−12,46), with1.5418mm minimum screw clearance across85 poses at0.5°. Secure/dress actual wires and inspect the first full sweep for rubbing. The body route ends at(28,−24,118) before the saddle atY−16. The strengthened PCB08 cradle removes by front tilt15°, +Y6mm then−X60mm after all five plugs and the keeper are removed.

PCB08 uses separate solid head supply/return fills,1.5mm yaw tracks and >=35µm finished inner copper;17.5µm is not accepted. N2(b) must still establish actual terminal voltage and closed-body PCB temperature. See [functional/proof record](../final/v1/d107-corrections.md).


### Camera signal path and head fan-out

The camera does **not** use a ribbon through the neck. The installed chain is:

`SC0874 camera → HD-026 150 mm 15-way ribbon → B0091 head adapter → HDMI plug → stripped HDMI inner pairs through head clamp / neck (alongside W47) → intact HDMI cable in body → B0091 body adapter → HD-027 150 mm 15-to-22 ribbon → Pi 5 CSI socket`.

One selected Arducam B0091 kit (HD-023) supplies the **pair** of passive boards represented by `D107_B0091_HEAD_*` and `D107_B0091_BODY_*` CAD envelopes. The slim HDMI cable (HD-028) and two installed150mm ribbons (HD-026/027) are separate purchase rows; the kit's60mm camera ribbon is too short. Buy/measure the HDMI cable before printing the closed bore inserts. B0091 does not replace the Camera Module 3 Wide.

In the head, the clamp takes the common loose bundle before separate leads fan out: head power continues to the first head servo; link and C2 power go to PCB-12 J1; servo data/ground branch to PCB-12 J2 and the servo lead crossing the roll joint; display power reaches D1; the camera inner pairs continue as `W47_LEAD_HEAD_CAMERA_HDMI` to the B0091 head adapter's **mated HDMI plug**. This is a physical cable branch, not an electrical splice of CSI into the twelve W47 wires. The route now terminates inside the plug envelope, instead of stopping beyond it.

The body Pi ribbon is shown as one continuous thin, tapered FPC envelope through the static body route, with mitered bends. **This geometry failed follow-up verification:** its stock-length slack is absent and the Viewer shape is not a credible installed fold. The head HDMI lead also approaches the plug from below despite overlapping its envelope. See the [camera verification](../final/v1/d107-camera-verification.md); the camera harness remains HOLD.
