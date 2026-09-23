# RP-03 Layout 02 generated mass properties

- Total modeled mass: 2614.7 g
- Whole-robot CoM: X=20.21, Y=0.60, Z=103.69 mm
- Static ball share (x/L): 0.184 of weight; RP-03 physics.md §3.6 flags < 0.09 as a spin-walk risk
- Forward-launch ball lift (a_tip = g·x/h): 1.91 m/s² vs compiled a_max ≤ 0.80 m/s²

| Item | Mass (g) | CoM (mm) | Source |
|---|---:|---|---|
| `RP01_HEAD_LAYOUT04` | 556.59 | (15.26, 0.67, 222.59) | RP-01 generated mass tree |
| `BODY_SHELL_AND_PANELS` | 287.80 | (20.00, 0.00, 96.00) | Layout 02 CAD estimate; +15 g for the internal panel frames (+15.6 cm3 net printed volume, near-solid 2.4 mm walls); -27.2 g for the -22.7 cm3 of shell floor opened over the motors, battery hatch and pod tongue (RP03-CAD-05/06) at ~1.2 g/cm3 |
| `BODY_PRIMARY_FRAME` | 335.00 | (20.00, 0.00, 94.00) | Layout 02 CAD estimate incl. mounts |
| `CHASSIS_PRIMARY_FRAME` | 173.30 | (19.80, 0.00, 47.40) | front crossmember moved 13 mm forward to X 80-92, rails and deck extended to X 92 (+2.1 g, +3.3 g), battery-tub front wall added (+1.3 g); before that CAD estimate; 219.8 g before RP03-CAD-05/06, then -53.3 g for the net -93.3 cm3 printed volume at ~45% effective PETG density: axle crossmember and square carriers/gussets removed, flange bosses and gearbox cheeks added, rails split and shortened to X -46, deck opened over the motors and battery, rear crossmember moved 16 mm forward, 11.2 cm3 battery tub added |
| `WHEEL_L` | 90.00 | (0.00, 85.00, 42.00) | custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately |
| `WHEEL_R` | 90.00 | (0.00, -85.00, 42.00) | custom dished wheel envelope; the 13.7 cm3 pocket roughly offsets the stub shaft now listed separately |
| `AXLE_BEARINGS_AND_STUB_SHAFTS` | 65.40 | (0.00, 0.00, 42.00) | E: four 608ZZ at ~12 g (not in the register before 2026-09-24) + two 8 mm steel stub shafts at ~8.7 g; symmetric about the centre plane |
| `MOTOR_L` | 110.00 | (0.00, 52.00, 42.00) | vendor |
| `MOTOR_R` | 110.00 | (0.00, -52.00, 42.00) | vendor |
| `BALL_TRANSFER` | 16.50 | (110.00, 0.00, 14.00) | vendor |
| `BATTERY` | 280.00 | (42.00, 0.00, 44.00) | RP-02 placeholder |
| `RASPBERRY_PI5_AND_COOLER` | 76.00 | (22.00, 0.00, 102.00) | vendor + estimate |
| `CONTROL_POWER_SENSORS` | 121.50 | (22.00, 0.00, 80.00) | estimate; one rear TCRT channel; GP2Y (3.5 g) moved to BALL_NOSE_POD_SENSOR_CAP |
| `BALL_NOSE_POD_SENSOR_CAP` | 17.60 | (110.50, 0.00, 41.20) | CAD volume: octagonal pod + lid 13.1 cm3 (X 92-128.5) and touch hood 3.6 cm3 (skirt cut at Z 29) at ~45% effective PETG density (7.5 + 2.0 g); 5 M3 screws + 2 heat-set inserts 4.6 g; GP2Y0A41SK0F 3.5 g E |
| `BODY_AUDIO` | 90.00 | (64.00, 0.00, 102.00) | speaker, amplifier and four microphones; CAD estimate |
| `HARNESS_AND_FASTENERS` | 95.00 | (20.00, 0.00, 88.00) | estimate |
| `BODY_YAW_STAGE` | 88.00 | (16.00, 13.50, 134.30) | E: 50 g thin-section bearing placeholder + 23 g XC330-M181 + 2 x 6 g 1:1 spur gears + 2 g clamp ring + 1 g coupling shaft; no SKU |
| `REAR_SKID_KEEL` | 12.00 | (-39.90, 0.00, 20.40) | CAD volume: 15.4 cm3 keel body at ~45% effective PETG density, 12x10 mm shoe, guards, 4 M3 screws |

Estimated/custom masses must be replaced by measurements before release.
