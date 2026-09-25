# RP-03 Layout 02 generated mass properties

- Total modeled mass: 2602.0 g
- Whole-robot CoM: X=18.73, Y=0.96, Z=106.55 mm
- Static ball share (x/L): 0.170 of weight; RP-03 physics.md §3.6 flags < 0.09 as a spin-walk risk
- Forward-launch ball lift (a_tip = g·x/h): 1.72 m/s² vs compiled a_max ≤ 0.80 m/s²

| Item | Mass (g) | CoM (mm) | Source |
|---|---:|---|---|
| `RP01_HEAD_LAYOUT04` | 588.38 | (15.32, 0.50, 222.55) | RP-01 generated mass tree |
| `BODY_SHELL_AND_PANELS` | 290.40 | (20.00, 0.00, 96.00) | Layout 02 CAD estimate; +15 g for the internal panel frames (+15.6 cm3 net printed volume, near-solid 2.4 mm walls); -27.2 g for the -22.7 cm3 of shell floor opened over the motors, battery hatch and pod tongue (RP03-CAD-05/06) at ~1.2 g/cm3; +2.6 g for the ~0.9 cm2 x 2.4 mm of shell floor returned when the battery opening shrank to the 2S1P pack tub (RP03-CAD-07) |
| `BODY_PRIMARY_FRAME` | 335.00 | (20.00, 0.00, 94.00) | Layout 02 CAD estimate incl. mounts |
| `CHASSIS_PRIMARY_FRAME` | 172.10 | (19.80, 0.00, 47.40) | front crossmember moved 13 mm forward to X 80-92, rails and deck extended to X 92 (+2.1 g, +3.3 g), battery-tub front wall added (+1.3 g); before that CAD estimate; 219.8 g before RP03-CAD-05/06, then -53.3 g for the net -93.3 cm3 printed volume at ~45% effective PETG density: axle crossmember and square carriers/gussets removed, flange bosses and gearbox cheeks added, rails split and shortened to X -46, deck opened over the motors and battery, rear crossmember moved 16 mm forward, 11.2 cm3 battery tub added; -1.2 g for the -2.1 cm3 smaller battery tub (RP03-CAD-07) |
| `WHEEL_L` | 90.00 | (0.00, 85.00, 42.00) | custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately |
| `WHEEL_R` | 90.00 | (0.00, -85.00, 42.00) | custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately |
| `AXLE_BEARINGS_AND_STUB_SHAFTS` | 65.40 | (0.00, 0.00, 42.00) | E: four 608ZZ at ~12 g (not in the register before 2026-09-24) + two 8 mm steel stub shafts at ~8.7 g; symmetric about the centre plane |
| `MOTOR_L` | 110.00 | (0.00, 52.00, 42.00) | vendor |
| `MOTOR_R` | 110.00 | (0.00, -52.00, 42.00) | vendor |
| `BALL_TRANSFER` | 16.50 | (110.00, 0.00, 14.00) | vendor |
| `BALLAST_STEEL_BAR` | 81.60 | (74.00, 0.00, 42.50) | E: mild-steel bar 9 x 60 x 19 mm at 7.85 g/cm3 (less two M3 tapped holes) + two M3 screws; sized so the register CoM clears the physics.md 2.5 line after the 110 g pack (RP03-CAD-08) |
| `BATTERY` | 113.70 | (46.70, 0.00, 43.10) | E: 2 x Samsung INR18650-25R (45 g max each = 90 g) + RP-02 PCB-01 pack-protection assembly (~5 g: 48 x 20 mm board 3.7 g + parts 1.3 g) + Bourns AC72ABD thermal cutoff and NTC (~0.7 g) + nickel straps, sleeve and AWG14 leads (~12 g) + pack-side SBS Mini housing (~6 g, U: dimension sheet not read); working selection, no purchase or measured mass; was 110 g with a generic ~8 g BMS (RP-02 board-specs.md sec 3, 2026-09-25) |
| `RASPBERRY_PI5_AND_COOLER` | 76.00 | (22.00, 0.00, 102.00) | vendor + estimate |
| `PCB02_CHARGE_AND_SYSTEM_POWER` | 18.00 | (-43.80, 0.00, 76.00) | E (proposal): 50 x 36 mm board 6.8 g + USB-C 1.2 + connectors 3 + inductor 2 + capacitors 3 + ICs 0.6 + misc 1; vertical on the rear-panel frame |
| `PACK_INTERFACE_SBS_MINI_AND_FUSE` | 14.00 | (42.00, 43.70, 41.00) | E: SBS Mini receptacle housing + contacts ~6 g (U; no modelled home, 13 mm wide against an 11.3 mm channel) + ATOF 15 A holder and fuse ~6 g + ~2 g; placed at the fuse holder |
| `PCB03_MOTOR_GATE_AND_HEAD_RAIL` | 24.00 | (38.50, 0.00, 69.00) | E (proposal): 2460 mm2 board 9.4 g + 4 x Micro-Fit+ 8 + inductor 3 + capacitors 2 + FETs, shunt, TVS, misc 1.6 |
| `PCB04_BRANCH_CONVERTERS` | 45.00 | (-5.00, 0.00, 70.05) | E (proposal): WS-H 35 g (3080 mm2 board 11.7 g + inductors 5.4 + connectors 8 + ICs 1 + polymer/ceramics ~1) with the hold-up raised from 4 x 1 mF (~8 g) to 2 x 3.3 mF (~9 g each, Ø12.5 x 20 lying) per board-specs.md sec 8.1: +10 g; the board footprint is NOT enlarged (no slack in the bay) |
| `C3_DEVKITC_N8` | 9.00 | (-8.00, 44.00, 80.80) | E: ESP32-S3-DevKitC-1-N8 board |
| `DRV8874_CARRIERS_X2` | 6.00 | (46.00, 0.00, 67.40) | E: 2 x Pololu 4035 at ~3 g (weight not read); symmetric about the centre plane |
| `IMU_BREAKOUT` | 2.00 | (16.00, 0.00, 60.00) | E |
| `TCRT5000_BREAKOUT_AND_CABLE` | 3.00 | (-54.00, 0.00, 13.50) | E: breakout, comparator and cable in the rear keel cartridge; was inside the old CONTROL_POWER_SENSORS row at the body centre |
| `ESTOP_XW1E_BV402M_R` | 40.00 | (-48.90, 0.00, 110.80) | E (not in the register before 2026-09-25): IDEC XW1E-BV402M-R operator Ø40 + two contact blocks + terminal cover; ~15 g outside the rear panel, ~25 g inside |
| `BALL_NOSE_POD_SENSOR_CAP` | 15.90 | (110.50, 0.00, 41.20) | CAD volume: raked prow pod + lid 11.8 cm3 (X 92-128.5) and touch hood 1.8 cm3 (2026-09-24 prow rework) at ~45% effective PETG density (6.8 + 1.0 g); 5 M3 screws + 2 heat-set inserts 4.6 g; GP2Y0A41SK0F 3.5 g E |
| `BODY_AUDIO` | 90.00 | (64.00, 0.00, 102.00) | speaker, amplifier and four microphones; CAD estimate |
| `HARNESS_AND_FASTENERS` | 95.00 | (20.00, 0.00, 88.00) | estimate |
| `BODY_YAW_STAGE` | 89.00 | (16.00, 13.50, 134.30) | E: 50 g thin-section bearing placeholder + 23 g XC330-M181 + 6 g driven spur + 6 g scissor pinion (two 2.4 mm halves) + 1 g torsion spring and retaining clip (2026-09-25) + 2 g clamp ring + 1 g coupling shaft; no SKU |
| `REAR_SKID_KEEL` | 12.00 | (-39.90, 0.00, 20.40) | CAD volume: 15.4 cm3 keel body at ~45% effective PETG density, 12x10 mm shoe, guards, 4 M3 screws |

Estimated/custom masses must be replaced by measurements before release.
