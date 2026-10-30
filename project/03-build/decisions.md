# 03 — Build decision ledger

The central record of every decision and change made during the build phase. Newest entries go at the bottom. Each entry states what was decided, why, what changed (docs, BOM, CAD), what is still unverified, and the next action. Supersede an entry with a new one instead of rewriting it.

`02-prototypes/` is read-only reference ([D-001](#d-001)); earlier RP decisions are linked, not copied or edited.

| ID | Date | Area | Decision | Status |
|---|---|---|---|---|
| [D-001](#d-001) | 2026-09-28 | Governance | `03-build/` governs; `02-prototypes/` is read-only reference | ACTIVE |
| [D-002](#d-002) | 2026-09-28 | Chassis / drive | DFRobot FIT0521 as drive gearmotor | SUPERSEDED by D-003 |
| [D-003](#d-003) | 2026-09-28 | Chassis / drive | Drive gearmotor: ThinkRobotics MOT3001-6V230RPM, with a reduced drive envelope | ACTIVE; inventory/workflow corrected by D-005 |
| [D-004](#d-004) | 2026-09-29 | Chassis / wheels | Wheel rim and tyre: six-spoke PETG rim with a clamped TPU tyre (A) or three O-rings (B) | SUPERSEDED by D-005 |
| [D-005](#d-005) | 2026-09-29 | Chassis / wheels | Wheel: TPU chevron tyre on a restyled clamped rim; O-rings as fallback only; spin index removed | ACTIVE for tyre, retention and fallback; face styling superseded by D-006 |
| [D-006](#d-006) | 2026-09-29 | Chassis / wheels | Wheel face: five swept blade spokes after builder references; round 5-screw clamp ring | SUPERSEDED by D-008 |
| [D-005](#d-005) | 2026-09-29 | Chassis / motor interface | No motor on hand; proceed with documented assumptions and replaceable interface | ACTIVE |
| [D-007](#d-007) | 2026-09-29 | Chassis / axle | Axle stack architecture: turned steel stub, paired bearings, set-screw motor coupling, floating motor | ACTIVE for architecture; bearing selection superseded by D-012; HOLD on quote, coupons, rig and motor receipt |
| [D-008](#d-008) | 2026-09-29 | Chassis / wheels | Wheel face: six framed spokes, 12-sided vented beadlock ring and a proud hex hub cap, after the builder's reference; hub on the D-007 interface | ACTIVE, HOLD with D-005 and D-007 |
| [D-009](#d-009) | 2026-09-29 | Chassis / wheels | Handed left/right tyres; D-008 wheel merged into chassis-v1 as the single wheel source | ACTIVE; full `check_layout.py` rerun pending; "handed" amended by D-070 (one part) |
| [D-010](#d-010) | 2026-09-29 | Chassis / axle/frame | Keyed single-print motor carriers join to split rails through J04 | ACTIVE for J04; bearing selection superseded by D-012; HOLD on fit coupons, full clearance rerun and physical rig |
| [D-011](#d-011) | 2026-09-30 | Chassis / nose (J07, J08) | Ball-transfer nose closed in CAD: caster screwed from below into seat inserts, sliding snap-retained touch cap on a constant nose, ESE22MV21 switch, screwed lid, J10-8 cable exit | ACTIVE; switch superseded by D-013; HOLD on received-caster measurement, coupons and physical tests |
| [D-012](#d-012) | 2026-09-30 | Chassis / axle | Select 688 ZZ, 8 × 16 × 5, from the OnlyScrews listing; revise paired-bearing seats | ACTIVE; HOLD on supplier stock/lot evidence, drawing/load data, fit coupons, clearance rerun and retention test |
| [D-013](#d-013) | 2026-09-30 | Chassis / nose (J08) | Nose contact sensing: DRV5055 linear Hall sensor and cap magnet, firmware trip at about 0.7 mm; replaces the D-011 ESE22MV21 switch; cap return springs | ACTIVE; HOLD on bench trip-point check and the PCB-10 J10-8 pin change |
| [D-014](#d-014) | 2026-09-30 | Chassis / rear keel (J09, J10) | Rear TCRT keel closed in CAD: M3 × 30 into crossmember inserts, bezel-and-shim TCRT retention with ±2 mm height, dovetail shoe, J10-10 disconnect at the keel with a route behind the crossmember | ACTIVE; HOLD on CH-020 breakout, CH-009/CH-010 materials, coupons and physical tests |
| [D-015](#d-015) | 2026-09-30 | Chassis / rear TCRT (CH-020, J09B) | Custom passive TCRT board that floats on the seated sensor; J10-10 becomes +3V3, GND, TCRT_OUT (ADC), LED_EN | SUPERSEDED by D-016 |
| [D-016](#d-016) | 2026-09-30 | Chassis / rear TCRT (CH-020, J09B) | No board: TCRT soldered to a GH4 lead that plugs into C3 J10-10; LED switch and load on PCB-10 | ACTIVE; HOLD on the PCB-10 J10-10 change and bench item 20 |
| [D-017](#d-017) | 2026-09-30 | Chassis / rear keel wear parts (CH-009, CH-010) | Recommendation: PETG for the wear shoe and the TCRT bezel; UHMW-PE tape on the shoe as an optional upgrade | RECOMMENDED; confirm after the item 20–22 tests |
| [D-020](#d-020) | 2026-09-30 | Chassis / nose springs (CH-066) | Industrybuying RS PRO 821245 selected for purchase; retain 9/6 mm installed gaps pending force and guidance tests | SELECTED; higher preload, cap force, buckling and hook retention unverified |
| [D-021](#d-021) | 2026-09-30 | Chassis / rear floor sensor (CH-020) | Bare Vishay TCRT5000 selected; Robu comparator module excluded from the designed keel interface | SENSOR SELECTED; supplier provenance, assembly fit and floor/cliff validation open |
| [D-022](#d-022) | 2026-09-30 | Chassis / fastener sourcing | Use best available supplier candidates after OnlyScrews checks; define J12/J13 nominal screw stacks | Superseded in part by D-023 |
| [D-023](#d-023) | 2026-09-30 | Chassis / fastener availability update | CH-035 and CH-038 reported available; CH-030/055/060 remain unsourced | Superseded in part by D-024 |
| [D-024](#d-024) | 2026-09-30 | Chassis / remaining fastener source leads | ACME low-head screw family and Dalloyed grub-screw family added as Indian quote/sample leads | OPEN; exact size/stock still to confirm |
| [D-025](#d-025) | 2026-09-30 | Chassis / mixed CSK fastener assortment | Mixed M3/M4/M5 kit may cover CH-038; M4 CSK does not fit CH-035 | CANDIDATE; kit source/material and fit unverified |
| [D-026](#d-026) | 2026-09-30 | Chassis / battery and ballast CAD (CH-022, CH-038, J12) | BOM and CAD reconciled: 1.1 mm cell gap, countersunk CH-038 seat, 350 mm TCRT mass note; chassis-v1.step rebuilt | ACTIVE; PCB-01 height, received-screw fit and full `check_layout.py` rerun open |
| [D-027](#d-027) | 2026-09-30 | Chassis / purchased-part models (CH-017, CH-018; J08A/J08C) | Vendor STEP for the A21 and a board-file STEP for the #3297 replace boxes; A21 ears trimmed, lead soldered, nose lid/cap reworked for the real package | ACTIVE; received-unit fit, ear trim and lead strain relief open |
| [D-028](#d-028) | 2026-10-01 | Chassis / battery tub interfaces (J11A, CN-05) | Shell opening sized to the hatch; front hatch bosses moved onto the tub front wall; bosses cut to Z 39.5 and the pack disconnect lifted 3 mm; IMU screw overlap recorded as accepted | ACTIVE; `check_layout.py` 116/119 (three D-027 failures open); boss and insert fit unproven |
| [D-029](#d-029) | 2026-10-01 | Chassis / nose lid (J08) | GP2Y soldered-lead reserve 3.0 to 2.0 mm, so the lid hump (top Z 57.6) clears the front panel's lift-off path | ACTIVE; lead bend in 2 mm to confirm at assembly |
| [D-030](#d-030) | 2026-10-01 | Chassis / frame fasteners, pack restraint, driver mounts (J05, J06, J11A, J11B, J12, J13, J15B, J16; CH-030, CH-055, CH-060) | J05/J06 inserts moved into the rail tongues; all frame, hatch and driver hardware modeled and added (CH-073–CH-082); pack strapped to the hatch; DIN 7984 → ISO 7380; set screw = M3 × 3 faced to 2.5 | ACTIVE; HOLD on coupons, strap/foam source and physical tests |
| [D-031](#d-031) | 2026-10-02 | Chassis / driver boards (J15B), inline motor pairs, motor face screws | #3297 boards turned long side along Y at X 38.5–56.3, posts at X 41.05; inline pairs re-placed; face-screw heads modelled as ISO 7380 domes; `check_layout.py` 119/119 | ACTIVE; supersedes the D-030 J15B layout; post coupon and received-board fit open |
| [D-032](#d-032) | 2026-10-02 | Chassis / main fuse holder (CH-028) | Inline Littelfuse 0FHA0001ZXJ ATO holder on a printed front-deck bracket above the +Y channel; the old channel envelope could not hold any ATO fuse | ACTIVE; CH-028 HOLD for an India source |
| [D-033](#d-033) | 2026-10-02 | Chassis / frame print units and hub cap (J03, J05, J06, J16; CH-001, CH-012, CH-058, CH-059, CH-073–CH-075, CH-077) | Each frame end printed as one module (deck + rails + crossmember), removing J05/J06/J16 and ten screws and inserts; hub cap held by one central M3 into the tapped stub end instead of six M2 | ACTIVE; HOLD on module print orientation, junction coupons and cap retention; full `check_layout.py` not rerun |
| [D-034](#d-034) | 2026-10-03 | Body / audio speaker (BO-001; BO-002–BO-006 registered) | Speaker: Visaton K 50 WP 8 Ω (art. 2915), element14 India 1683894; body audio chain entered in the project BOM | ACTIVE; speaker SELECTED, not ordered; HOLD on received-part measurement and bench listen |
| [D-035](#d-035) | 2026-10-03 | Body / audio bench amplifier (BO-007) | SmartElex MAX98357A I²S breakout (Robocraze) as the bench amplifier until PCB-05 exists | ACTIVE; SELECTED, not ordered; bench only |
| [D-036](#d-036) | 2026-10-03 | Body / audio microphones (BO-012, BO-005) | Mic IC: Infineon IM73D122V01XTMA1, element14 India 4125831; four-mic array (two per ADAU7002 lane), not six | ACTIVE; SELECTED, not ordered; HOLD on PCB-06 layout and the array tap test |
| [D-037](#d-037) | 2026-10-03 | Body / microphone mounting (BO-005, BO-006, BO-013, BO-014) | Mic boards mount on gasketed shell bosses with two M2 thread-forming screws and a soldered GH lead, not on the frame | ACTIVE; DESIGN; HOLD on boss coupon and PCB-06 layout |
| [D-038](#d-038) | 2026-10-03 | Power boards (PCB-01, PCB-03, PCB-10; CH-017, CH-023, CH-041–CH-043; CH-083–CH-086 registered) | PCB-03 drive feed re-specified for the DRV8833: SMBJ8.5A bus TVS, VM entry, AND-gate sleep, latched FLT, INA181 feed monitors; TIFPS0629 bench acceptance window; 04-pcbs home and board register; PCB-12 assigned to the C2 head carrier | ACTIVE; DESIGN; HOLD on TIFPS0629 bench acceptance and MOT3001 winding R/L |
| [D-039](#d-039) | 2026-10-04 | Harness (W01–W39, J-PK, J2-1, J3-1, J3-4, J8-1; CH-025–CH-027, CH-041, CH-042, CH-083; HN-001–HN-010 registered) | Fused pack feed split at butt splices beside the fuse (W04, J2-2 deleted); J-PK is the isolator; NTC break is a JST SM 2p in the +Y channel; Micro-Fit+ only on AWG16/18 UL1061, Micro-Fit 3.0 on AWG22, pre-crimped GH; J3-4/J8-1 to Micro-Fit 3.0; full wire list, pinouts and service breaks in 05-harness | ACTIVE; DESIGN; HOLD on housing PNs, crimp qualification and the first harness build |
| [D-040](#d-040) | 2026-10-04 | Charge path (PCB-02, PCB-13 registered; CH-041, HN-003; BO-015–BO-017 registered) | Charge inlet moves to a panel-mounted board PCB-13 (GCT USB4140, TVS2200, ESDA25W, STUSB4500, input P-FET) in a pocket that takes any compliant plug; charger straps closed: D+ tied to D−, BATP sense, TS 8.45 k / 324 k for 0–50 °C, 20 V-rated input | ACTIVE; DESIGN; HOLD on schematic, NVM image and bench CP-01 to CP-14 |
| [D-041](#d-041) | 2026-10-04 | Body / power button; E-stop removed (BO-018 registered; CH-041, CH-042, CH-046, HN-001, HN-004; W40, J2-9; W22, J3-7, W38 removed) | No E-stop: the rear red mushroom becomes the momentary power button (LTC2954 `PB`, GH2 `J2-9` on PCB-02's +Y edge, 10 k wetting pull-up); a press also resets `SYSTEM_ARM`, so it stops the motors in hardware; the latching NC IDEC XA1E is replaced by a 16 mm momentary 1NO mushroom in the same well | ACTIVE; DESIGN; HOLD on the received part's fit in the well and bench PB-01 to PB-06 |
| [D-042](#d-042) | 2026-10-04 | Body / compute retention and cooling (BO-033–BO-042; CH-084; W41, J9-4) | Pi 5 screwed to a vented three-point compute tray (rear −Y lug, front −Y column, rear +Y block); Active Cooler on its push pins with tip keep-outs; BO-040 2-wire 4010 side intake fan on a +Y frame web, switched on/off by Pi GPIO24 through a MOSFET on PCB-09 (`J9-4`, `gpio-fan`); +Y shell grille and collar, rear-panel vent slots, open floor as the outlet | ACTIVE; fan size and position superseded by D-043; HOLD on the bench thermal test, the AR-61 noise check, CR-02 and coupons |
| [D-043](#d-043) | 2026-10-04 | Body / enclosure fan vs mic ports (BO-040, BO-041; W41) | The +Y enclosure fan shrinks from a 4010 to the purchased 3010 hydraulic model and moves to X 17.5, Z 107, midway between the +Y mic ports: grille edge 24.1 mm from FRONT_L (was 14) and 25.9 mm from REAR_L; mic array unchanged | ACTIVE; DESIGN; HOLD on measured mounting holes, the bench thermal test and the AR-61 noise check |
| [D-044](#d-044) | 2026-10-04 | Body / head yaw stage (BO-043–BO-050, BO-056–BO-062; PCB-08/14; W37/W42/W43) | 61810-2Z bearing cartridge, 1:1 printed scissor spur pair, ±62° hard stops and FFC clock-spring cassette | ACTIVE; DESIGN; HOLD on received parts, coupons and B1/B4/cassette tests; D-047 changes its servo |
| [D-045](#d-045) | 2026-10-05 | Body / service-panel internal frames (BO-022, BO-023, BO-053; BO-031; BO-063 registered) | Internal panel frames printed as part of the shell, not bonded; bosses lengthened to 7.1–7.7 mm with M3 × 6 heat-set inserts for the M3 × 8 machine screws | ACTIVE; DESIGN; HOLD on the panel-boss coupon and the shell print |
| [D-046](#d-046) | 2026-10-07 | Head / pitch and roll actuators (HD-001 registered; RP-01 `ACT-01` overridden for pitch/roll) | Feetech STS3045M (metal gear, coreless, 34.8 g) for pitch and roll, replacing the XC330-M288; fastest pitch moves capped at 70% speed; head rail setpoint must rise above the servo's 4.8 V minimum; yaw servo and bus protocol open | SELECTED; HOLD on head CAD re-fit, rail setpoint, bench B1/B4 |
| [D-047](#d-047) | 2026-10-07 | Body / yaw servo (BO-043) | Waveshare ST3215-HS on a 12 V yaw-only rail on PCB-03 replaces the D-044 XC330-M181-T: speed margin first, one Feetech protocol with D-046; STS3250 fallback on lash, XC330-M181 if no Feetech case fits | SELECTED; provisional case fit found; HOLD on mount/hub integration, rail and bench B1/B4 |
| [D-048](#d-048) | 2026-10-07 | Body / ST3215-HS yaw integration and compute-stack shift (BO-043, BO-056, BO-061; CH-084 PCB-09, CH-086 PCB-10, PCB-04; W15) | HS on the true horn axis, horn up, case to -X, 7.6 mm lower, clamped by four M2 screws to a frame ring; Pi, cooler, tray bosses and PCB-09 move +10 X / -6 Y; tray +Y edge to Y 23.5; C3 Z 92 header row repacked | ACTIVE; CAD packaging screens clean; HOLD on a matching plug, torque/gear proof, received HS, head re-balance and bench B1/B2/B4 |
| [D-049](#d-049) | 2026-10-08 | Head / STS3045M pitch and roll installation (HD-002–HD-007; head v1 CAD, A0, body v1 hand-off) | Roll servo on an ear plate driving the spindle through a goBILDA 25T-to-Ø6 coupler, rear bearing forward; pitch servo on the pitch frame with its horn screwed to a widened +Y yoke leg; CF-filled yoke legs; rear trim off-axis; A0 re-solved | ACTIVE; CAD and checks complete; HOLD on received horn/coupler fits, the CF leg coupon and bench B1/B4/B6 |
| [D-050](#d-050) | 2026-10-09 | Head / yoke legs and turntable restyle (M011-Y, M012; head v1 CAD, mass tree, body v1 hand-off) | Both yoke legs become one faceted design inscribed in the D-049 free corridor (plinth, waist, arm), replacing the +Y leg's stair-stepped raster outline, ledge and box foot; disc rim tapers R62.5 to R58.5; opaque presentation model | ACTIVE; CAD and checks complete; HOLD on the CF leg coupon and print orientation |
| [D-051](#d-051) | 2026-10-10 | Head / passive pitch pivot and yoke-leg joints (HD-008–HD-011; M011-Y, M012; head v1 CAD, mass tree, body v1 hand-off) | −Y pivot becomes an MR106ZZ in the −Y leg pad, a flush printed retainer and a Ø6 D-shaft pin into a D-bore boss on the pitch frame; each leg plinth keys over a block on the disc top and takes two M2 screws from its inner face | ACTIVE; CAD and checks complete; HOLD on received bearing/D-shaft fits, a seat and key coupon, and bench B6 |
| [D-052](#d-052) | 2026-10-10 | Body + head / yaw cable path (BO-045, BO-050, BO-058, BO-062; M012; W37/W42/W43) | The cassette FFCs enter the drum through a full-height slit at 0° (wraps 150°/90°), fold once and plug into three vertical PCB-14 joiner boards held in rotor posts under the hub shoulder; the head FFCs rise from their upper ZIFs through a Ø21 disc bore into a 12.5 × 1.5 mm channel, demating with the disc on; hub bore R13.15, disc pilot R10.5–13 | ACTIVE; CAD and checks complete; HOLD on the ZIF selection, an FFC fold mock-up and the cassette bench test |
| [D-054](#d-054) | 2026-10-10 | Head / camera housing restyle (M019a; head v1 CAD) | The 46 mm crown and its hipped roof cap become a slim raked fin: the crown narrows to 40 mm with 3 mm top chamfers and keeps its flat top to X −24; the skin hood behind it rakes down at 35.5° to the roof, about 25 mm long instead of running back to X −78 | ACTIVE; front section revised by D-056 |
| [D-055](#d-055) | 2026-10-10 | Body / shell review fixes (BO-019, BO-024; body v1 CAD) | Remove the Layout 02 front badge land that sat inside the speaker cup; raise the enclosure fan, web opening and +Y grille 3 mm (Z 110) so the grille clears the wheel-arch pod; teardrop fan collar for the roof-down print; drill the Ø2 mic ports after printing | ACTIVE; CAD and targeted checks complete; HOLD on a printed grille/collar coupon |
| [D-056](#d-056) | 2026-10-11 | Head / camera fin front section (M019a; head v1 CAD) | The D-054 fin becomes trapezoidal from the front: sides slope in from 44 mm at Z 85 to a 34 mm flat top at Z 104, replacing 40 mm vertical sides with 3 mm top chamfers; the rake, depth and hood are unchanged | ACTIVE; CAD and checks complete |
| [D-057](#d-057) | 2026-10-13 | PCBs / register numbering (CH-064; final v1 CAD) | The custom nose Hall carrier, listed in the board register only by its BOM ID CH-064, becomes **PCB-15**; the BOM line stays CH-064 | ACTIVE; numbering only, no design change |
| [D-058](#d-058) | 2026-10-14 | PCBs / design toolchain (all custom boards; 04-pcbs workflow) | Design every custom board in **KiCad 10**, with `kicad-cli` running the electrical and layout checks and the fab and STEP exports, **Freerouting** for autorouting, and **JLCPCB** as the default fab and assembler | PARTLY SUPERSEDED by [D-060](#d-060) (KiCad version, no autorouter); `kicad-cli` and JLCPCB stay ACTIVE |
| [D-059](#d-059) | 2026-10-14 | PCBs / PCB-15 seat relief (CH-064; final v1 CAD) | Cut a 0.9 mm relief pocket into the nose seat behind the Hall board, so C1, R1 and C2 all go on the board's back face; the cut is made in `final/v1/cad`, not in the chassis source | ACTIVE; cut measured; schematic and layout not started |
| [D-060](#d-060) | 2026-10-14 | PCBs / layout method (all custom boards; 04-pcbs workflow) | LLM-driven layout uses **KiCad 10.99 nightly** through KiPy and computer-use tools, places parts one at a time or in small functional groups, and routes by hand-planned octolinear buses with current-sized tracks; **no autorouter**. Replaces D-058's KiCad version and Freerouting | ACTIVE; nightly and KiPy installed 2026-10-25; no board laid out |
| [D-061](#d-061) | 2026-10-25 | PCBs / fab-neutral design rules (all custom boards; 04-pcbs workflow) | Design every board to the **strictest of JLCPCB, Lion Circuits and PCB Power** standard 2-layer limits, so either the Chinese default or an Indian fab can make it; choose the fab by quote at procure. Replaces D-058's "layout follows JLCPCB's limits"; JLCPCB stays the default | SUPERSEDED by D-062 |
| [D-062](#d-062) | 2026-10-25 | PCBs / fab shortlist and design rules (all custom boards; 04-pcbs workflow) | Only **JLCPCB, PCBWay and Lion Circuits** make Makad boards. Every layout meets the strictest standard 2-layer limits of the three, with Lion Circuits' **MII (Make in India)** service as the target, which sets the vias at 0.35/0.67 mm and 0.31 mm via spacing. PCB Power is dropped. Replaces D-061 | ACTIVE; PCB-15 re-laid to it, DRC clean |
| [D-063](#d-063) | 2026-10-25 | Chassis / nose: PCB-15 moved 0.4 mm back (CH-064, CH-065; final v1 CAD) | The nose Hall board and its 1.0 mm slot move **0.4 mm back** (board X 126.2–127.0). The relief pocket deepens to 1.3 mm. U1 then clears the cap magnet at the 3 mm stop by 0.195 mm in the worst case, where D-013 had assumed 0.1 mm and the real part could hit it by 0.205 mm | ACTIVE; fit and relief checks pass; trip point to re-measure on the bench |
| [D-064](#d-064) | 2026-10-25 | PCBs / workflow order (all custom boards; 04-pcbs workflow) | **Design every board first**, one at a time, then procure them together in shared orders, then integrate. Replaces the one-board-at-a-time path through all three stages | ACTIVE; PCB-15 rev A designed, its procurement waits for the batch |
| [D-065](#d-065) | 2026-10-26 | Head / crown: PCB-11 status LED socket, part and circuit (CH-085; final v1 CAD) | A printed **socket fused inside the crown** holds the PCB-11 board and the light pipe, which nothing held. The LED is the **WS2812B-2020-V6** (LCSC C52917434), not the pre-V6 C965555 the BOM named. PCB-11 gains **C1 100 nF** and **R1 330 Ω** in DIN, and its wire pads move to the back's right half | ACTIVE; socket check passes; India V6 stock to confirm at procure |
| [D-066](#d-066) | 2026-10-26 | Body / audio: PCB-06 L/R strap and mic source (BO-005, BO-012) | One PCB-06 design serves all four positions; the LR strap is an **assembly variant**: two 0402 1 kΩ footprints, R_L (LR to GND) and R_R (LR to 3V3), and the fab fits exactly one. The mic is **bought by the builder from element14 India** (4125831, UK stock) and supplied to the fab, not bought by the fab from its own stock. Amended: MK1's sound-hole seal ring pulled back to R 0.63 (0.23 mm from the hole), with a scoped 0.2 mm rule | ACTIVE; PCB-06 board set up, placement next |
| [D-067](#d-067) | 2026-10-27 | Body / audio: PCB-05 inputs, mounting and CR-01 (BO-002, BO-006, BO-064; final v1 CAD) | PCB-05 takes **5 V on W12 only**; `CA-06` **CR-01 is accepted** (GPIO22 SDI1, GPIO23 `AMP_SD`); **no power-good path**: `AMP_SD` drives SD_MODE through 2.2 kΩ; mics map `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R; ferrite + 2.2 Ω + 10 µF mic rail; two layers. The board **hangs from the frame** on three 8 mm M2 SMT spacers and ISO 7380 M2 screws from above, and goes in after the compute tray. Amended at board set-up (J7 tails clipped, spacer holes plated) and at placement (one rear and two front spacers; `J5-1` 2 mm toward −Y) | ACTIVE; PCB-05 rev A designed, 4 layers (amended at routing), fit check passes |
| [D-068](#d-068) | 2026-10-27 | Body / electronics: PCB-10 C3 carrier inputs, mounting, DevKitC and parts (CH-044, CH-045; final v1 CAD) | The C3 module is held by the **two lower M2.5 screws and two printed hooks** over the board's top edge (the upper screws sat under the DevKitC); the uprights get **pin-tail reliefs**. The DevKitC is **genuine Espressif ESP32-S3-DevKitC-1-N8 v1.1** only, modelled from Espressif's drawing (rows 22.86 mm, not the CAD clone's 25.4). Watchdog: **TPS3436CCCBGDDFRQ1** (the BD-10 fallback; the CFDBE has no stock anywhere reachable) from **Mouser India**; link transceiver on a SOIC-8 footprint (THVD1451DR or MAX3490EESA+); Schottky in the `J10-1` feed against USB back-feed; GPIO map v0.2; `J10-2` named by direction. Amended at board set-up: the board grows 6 mm down (70 × 49.5, notched over a DRV8833 terminal block) for a third connector row; at placement: **four layers** (In1 GND, In2 +3V3), `J10-2` reordered, GPIO map v0.3 | ACTIVE; `check_pcb10_mount.py` 9/9; PCB-10 placed, routing |
| [D-069](#d-069) | 2026-10-29 | Body / electronics: PCB-13 charge inlet inputs (BO-015; final v1 CAD) | The rear-panel pin relief widens **9.60 → 10.60 mm** so GCT's USB4140 stake copper clears the seat (`DROID_CUTS`); J1 **hand-soldered** by the builder, the fab assembles the +X face only; **1 oz, two layers, 1.6 mm**; NVM test pads on a **2.54 mm grid** for P75 pogos; actives from **element14 India** (USB4140, STUSB4500, STL6P3LLH6, ESDA25W) and **Mouser India** (TVS2200DRVR); `W16`/`J2-8` interface and PCB-02 back-face keep-out fixed | ACTIVE; `check_pcb13_relief.py` 13/13; PCB-13 inputs frozen, schematic next |
| [D-070](#d-070) | 2026-10-29 | Chassis / wheels: print fixes (CH-004, CH-005, CH-056, CH-058; J03, J14; final v1 CAD) | The hub-cap clocking **pegs move onto the hub** and the holes into the cap (each in a Ø3.7 boss), and the cap column is trimmed flush, so the cap prints underside down with no supports; the **tyre is printed in its free state** (Ø73.6 bore, 19.3 wide; `PRINT_STATES`), the assembly keeps the fitted state; the **rim prints lip side down**; **Loctite 222** on the wheel screws; left and right tyres are **one part** (amends D-009's "not interchangeable") | ACTIVE; `check_wheel_print.py` 29/29; physical fits open |
| [D-071](#d-071) | 2026-10-30 | Chassis / axle stack: assembly fixes (CH-001, CH-012, CH-051, CH-089; J01, J02, J03; final v1 CAD) | The stub flange shrinks **Ø24 → Ø21** so a straight key reaches the housing screws with the stub in; the motor is aligned with a printed **alignment plug** (CH-089, a tool) in the bearing seat, because the face screws cannot be reached once the bearings and stub are in; the housing's screw holes close **Ø3.4 → Ø3.2** so it refits where the motor was aligned; a **notch** in the carrier hub clears the set-screw key; print orientations recorded (housing inboard face down, carrier outboard face down); the housings are the fit test, no bore coupons | ACTIVE; `check_axle_stack.py` 21/21; stub drawing and physical proof open |
| [D-072](#d-072) | 2026-10-30 | Chassis / axle stack: motor-to-axle follow-up (CH-053, CH-089; J01, J02; final v1 CAD) | The housing screws go **M3 × 18 → M3 × 16**: an 18 mm screw at its long limit bottomed out in its blind hole before it clamped the cap; the alignment gets an **error budget** of 0.05 mm: the plug becomes a close sliding fit (Ø15.8 → Ø15.96) and the housing screws are tightened only after the set screw is in and the stub has turned | ACTIVE; `check_axle_stack.py` 27/27 |

Status words: `ACTIVE` is in force, `SUPERSEDED` names its replacement, and `HOLD` names the evidence that must arrive before dependent work is released.

---

## D-001

**2026-09-28 · Governance · ACTIVE**

**Decision:** from this date, `docs/03-build/` is the governing context. Every new decision, part selection, BOM change and CAD edit is recorded in `03-build/`, in the subsystem and version folder it belongs to, and logged in this ledger. `docs/02-prototypes/` (all RPs, including RP-03 locomotion and RP-06 CAD) is read-only reference. Where an RP document disagrees with `03-build/`, `03-build/` wins.

**Changed:** [README.md § Governing context](README.md#governing-context).

**Note:** chassis v1 CAD still reads purchased STEPs and the Layout 04 head from `02-prototypes/RP-06-cad` by path ([cad/README.md](01-chassis/v1/cad/README.md)). Reading them is allowed; moving or copying them is a `03-build/` change and gets its own entry.

---

## D-002

**2026-09-28 · Chassis / drive (CH-014) · SUPERSEDED by [D-003](#d-003)**

DFRobot FIT0521 (6 V, 34:1, 3.2 A stall) was briefly the working choice on budget. It was dropped the same day: TME India had stock, but DigiKey quoted a lead time of about 9 weeks, and the builder chose the in-India ThinkRobotics part instead. Its CAD and BOM changes were replaced by D-003.

---

## D-003

**2026-09-28 · Chassis / drive (CH-014) · ACTIVE, HOLD on receipt measurements**

**Decision:** the chassis v1 drive gearmotor is the **ThinkRobotics MOT3001-6V230RPM**, "25mm DC Metal Encoder Gearmotor", 6 V / 230 rpm variant, ₹1,179.99, in stock ([product page](https://thinkrobotics.com/products/25mm-encoder-dc-metal-gearmotors)). It is a generic JGA25-370 with an 11 PPR Hall encoder on the motor shaft. It replaces the Pololu #4804 (about ₹5,956 in India) and the FIT0521 (D-002), and was chosen by the builder on cost and in-India availability.

**Performance accepted:** this motor **does not meet** the RP-03 drive gate ([gearmotor-sku-decision.md](../02-prototypes/RP-03-locomotion/gearmotor-sku-decision.md)): at least 159.2 rpm at 0.110 N·m (0.70 m/s heavy launch on the Ø84 wheel), and at least 0.220 N·m stall. ThinkRobotics does not tabulate the 230 rpm variant. The figures below are linear-motor estimates (`E`) from the family data: about a 6,000 rpm base, 1.8 A stall at 6 V, and stall torque about 0.08 kg·cm per unit of ratio. They imply about 26:1 and about 2.1 kg·cm stall.

| Case, 6 V motor | Speed at 0.110 N·m heavy launch | Speed at 0.063 N·m nominal load | Stall torque |
|---|---:|---:|---:|
| 6.0 V at motor | about 107 rpm (0.47 m/s) | about 160 rpm (0.70 m/s) | about 0.20 N·m (fails ≥0.22) |
| 5.3 V at motor (nearly empty pack) | about 80 rpm (0.35 m/s) | about 133 rpm (0.58 m/s) | about 0.18 N·m |

**Consequence:** plan chassis v1 around a **reduced drive envelope** until measured: about 0.5 m/s cruise at nominal load, gentler launch and acceleration limits, and a stall margin below the 2× rule. Heavy-mass launch, threshold climbing and slope hold at full ballast are the tests most likely to fail. The 0.70 m/s RP-03 target is not claimed for v1. Good side effects: 1.8 A stall suits the DRV8874 and the 5 A bench supply, and 11 × 26 × 4 ≈ 1,140 encoder counts per wheel revolution is enough for creep and hold.

**Motor availability:** no motor is currently on hand. A MOT3001-**6V170RPM** was considered as a possible lower-speed bench stand-in, but it has not been procured and is not available for fit, encoder or firmware tests. The selected MOT3001-6V230RPM units also remain to be ordered.

**CAD changed** ([body_chassis_model.py](01-chassis/v1/cad/body_chassis_model.py)):

- The motor is modelled parametrically from the ThinkRobotics/JGA25 drawing (no vendor STEP): Ø25 gearbox (21 mm assumed; the drawing gives 19–27 mm by ratio), Ø24.4 × 31 mm can, encoder board with a rearward 6-pin connector, Ø7 × 2.5 bushing boss, and a Ø4 D-shaft 12.0 mm from the faceplate (was 12.5 on the #4804) with an 8 mm flat. Faceplate to encoder end is about 61 mm (was 66.5).
- Axle flange, 2 mm diaphragm, 608 pair and stub shaft are unchanged. The shaft engages the stub for 8.0 mm (was 8.5).
- Face screws keep 2 × ISO 10642 M3 × 8 at ±8.5 mm. That pattern and the 5 mm tapped depth are **assumptions**; the drawing does not give them.
- The motor pigtail reserve is extended rearward to X −21 to meet the connector.
- Mass register: MOTOR_L/R 101 g at |Y| 39.2 → 110 g at |Y| 40.2. The 110 g is the NFP-JGA25-370-EN figure for this platform; ThinkRobotics lists a 130 g shipping weight. Weigh on receipt.
- Check results: _pending the full rerun_.

**BOM changed:** CH-014 in [BOM.csv](BOM.csv) and [01-chassis/v1/BOM.md](01-chassis/v1/BOM.md).

**Release holds and next actions:**

1. Order two MOT3001-6V230RPM plus one spare.
2. When a motor is received, measure face hole spacing, thread and depth; gearbox length; shaft protrusion and D-flat; connector position and cable exit; and mass. Verify those measurements against the CAD assumptions and update the model if anything differs.
3. Bench test on a current-limited supply: no-load speed and current at 6.0 V and 5.3 V to confirm the winding and ratio; speed under a known 0.063 N·m and 0.110 N·m load; encoder counts per output revolution; a brief current-limited stall. Record the measured drive envelope here and set the firmware speed and acceleration limits from it.
4. Run the chassis heavy-launch, threshold and slope-hold tests at representative ballast early. If they fail, open a new entry. Fallbacks, in order: Pololu #4803 (₹5,956, passes with margin) or FIT0521 (TME India).

---

## D-004

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-006, J14) · SUPERSEDED by [D-005](#d-005)**

**Decision:** the drive wheel is a PETG six-spoke rim carrying one of two tyres. The builder asked for a rugged look, a simple build, and one printed and one non-printed rubber option. A later entry picks one variant from test results.

- **Variant A, printed:** a TPU 95A tyre with two staggered rows of lugs. It is keyed to 12 ribs on the rim seat and clamped between an integral inboard lip and a bolt-on outboard ring by 6 × ISO 7380 M3 × 8 screws into heat-set inserts. The tyre can be changed without removing the wheel.
- **Variant B, bought:** three 70 × 5 mm NBR 70A O-rings stretched 5.7% into grooves on a one-piece rim. No hardware.
- **Spin index:** a paint-filled notch in one spoke instead of a separate inlay.

**Why:**

- **A smooth ring on a smooth rim was never a joint.** Positive keying plus side clamping (A), or a stretched seal in a groove (B), are the simplest retention methods that don't rely on glue.
- **The clamp ring makes the tyre serviceable in place** (CON-P01).
- **O-rings need no flexible printing at all.** They cover the case where the lab can't print TPU.

**CAD added:** the standalone [wheel CAD](01-chassis/v1/cad/wheel/README.md) (`wheel_model.py`, three STEP entries, `check_wheel.py`, 26/26 measured checks passing). It keeps the chassis Ø84 × 24 envelope, the R18 boss pocket and the Ø8 stub bore. **The chassis model and `chassis-v1.step` are not changed**, and still show the placeholder tyre. Mass at solid density: A 90.0 g, B 80.8 g, against 89 g in the chassis register.

**BOM changed:** CH-004/005/006 set to DESIGN. Added CH-048 (screws), CH-049 (inserts) and CH-050 (O-rings); only the chosen variant's hardware is bought.

**Unverified:** TPU print allowances (bore Ø73.6, width 19.3), O-ring cord thinning (estimated OD 83.7), loaded radius, grip, creep at stall, left/right OD match and runout. The stub-to-hub torque joint (J03) is still open; the R4 bore is a placeholder.

**Next actions:**

1. Confirm whether the 3D lab can print TPU 95A. If not, variant B is the only option.
2. Print one rim of each variant plus the tyre coupon. Measure loaded radius at about 1 kg, μ on S-TILE/S-LAM/S-RUG, stall-torque creep and runout.
3. Choose the variant in a new entry. Then port it into `wheel_assembly()` in the chassis model, replace `loaded_radius_matches_axle_height` with the measured radius, and rerun the chassis checks.

---

## D-005

**2026-09-29 · Chassis / motor interface · ACTIVE**

**Correction:** the builder has **no motor on hand**. A 6V170RPM unit had been mentioned as a possible bench stand-in, but it was not purchased or available for measurement. The 6V230RPM motor selection and reduced drive-envelope estimate remain the working choice; all motor fit and performance checks await receipt of hardware.

**Design direction:** continue chassis engineering from the supplier drawing and clearly labeled CAD assumptions. Put the uncertain face-hole/pilot/shaft interface in replaceable or adjustable parts so a mismatch does not force a complete frame reprint. The [motor interface sheet](01-chassis/v1/research/motor-interface-sheet.md) is parked, and the [mechanical checklist](01-chassis/v1/research/engineering-checklist.md) no longer includes a motor-measurement task.

**Limit:** an assumed interface can support a provisional CAD and fit print, but it is not evidence of physical motor fit, safe shaft coupling, or drive performance. Those remain unverified until actual hardware is assembled and tested. No motor-dependent part is marked physically passed by this decision.

**Next:** engineer the frame split and replaceable carrier/plate (J04/J01), then revise the axle stack and wheel hub with explicit assumption ranges and service access.

---

## D-005

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-006, CH-050, J14) · ACTIVE, HOLD on lab TPU capability and grip/retention tests**

**Decision:** the builder chose the printed TPU tyre from D-004. It is the only modelled wheel. Three further changes come with it:

- **Tread:** the plain lugs are replaced by a chevron tread: 18 V-lugs 1.5 mm tall, bars at 40° to the axle, apexes on the tyre centre line. Below about 37°, the Vs leave gaps on the contact line and the wheel bumps 18 times per revolution; the check caught 18 of 72 angles open at 30°.
- **Outboard face, restyled to the droid's shell language** ([vision](../00-foundation/vision.md#character-and-visual-direction), RP-01 D-07 stepped panels):
  - six windows in a 1.5 mm stepped surround, leaving stepped spokes 10 mm wide at the root with a 6 mm crest;
  - a two-step hex hub;
  - a 12-sided beadlock-style clamp ring with a flat facing each screw.
- **Spin index removed:** no notch, no paint and no part. CH-006 is deleted.

Retention is unchanged from D-004: 12 seat ribs, an inboard lip, and a clamp ring with 6 × M3 × 8 button heads into heat-set inserts.

**Fallback, recorded here only (not modelled, no BOM row):** if the 3D lab can't print TPU 95A, use a one-piece PETG rim with three grooves, 5.4 mm wide and 2 mm deep, with a Ø74 bottom and Ø78 lands, at y −7.1 / 0 / +7.1 mm. Fit three **70 × 5 mm NBR 70 Shore A O-rings**, stretched 5.7%; the cord is 36% seated and about 83.7 mm OD mounted. No hardware; the O-rings roll off to replace them. If they creep in the groove, put a drop of CA glue in each groove. D-004 checked this geometry (all 12 O-ring check rows passed).

**CAD changed:** in the [wheel CAD](01-chassis/v1/cad/wheel/README.md), the O-ring model, the variants entry and the index were removed. The single entry is now `wheel.step.py`, and `check_wheel.py` passes 18/18. The checks now also cover spoke section, clamp-ring corners, hub cap and chevron contact continuity. Mass at solid density is 93.7 g per wheel, against 89 g in the register. The chassis model is still not changed.

**BOM changed:** CH-004 and CH-005 re-specified. CH-006 and CH-050 deleted. CH-048 and CH-049 are no longer marked as variant-only.

**Next actions:**

1. Confirm the lab can print TPU 95A (direct-drive extruder).
2. Print a rim, a clamp ring and a tyre coupon. Measure fit, loaded radius at about 1 kg, μ on S-TILE/S-LAM/S-RUG, stall creep and runout.
3. Port the wheel into `wheel_assembly()` in the chassis model. At the same time: remove the placeholder index inlay, update the mass register (+4.7 g per wheel) and the loaded-radius check, and rerun the chassis checks.

---

## D-006

**2026-09-29 · Chassis / wheels (CH-004, CH-048, CH-049) · SUPERSEDED by [D-008](#d-008)**

**Decision:** the builder found D-005's six stepped spokes too plain and supplied three reference wheels: automotive five-spoke rotor designs with swept, faceted, two-tone blades. The rim face now follows them:

- **Blades:** five blades, each leaving a whole flat of a pentagon hub. The straight leading edge sweeps 30°; the trailing edge kinks at R20 and flares, so each blade covers 48° at the rim and leaves a 24° window.
- **Two-level face:** each blade face is split by a ridge. The leading band stays at full height, and the trailing flank slopes 15° down, to about 4.3 mm at the flare corner. This gives two tones under light, and takes a two-tone paint finish if wanted.
- **Details:** a through-slot in each flare, and a round cap on the hub.
- **Clamp ring:** round, not 12-sided, so the face reads as one clean lip as in the references. It now uses **5** M3 button heads, one mid-window, matching the five blades.

Tyre, tread, rib keying and the O-ring fallback are unchanged from D-005.

**Why the numbers:**

- **15° flank, not 20°:** the wider flare would otherwise fall below 2.5 mm at its trailing corner.
- **Five screws still clamp the full bead:** the ring covers the tyre side by 2 mm all round.

**CAD changed:** `wheel_model.py` and `check_wheel.py` in the [wheel CAD](01-chassis/v1/cad/wheel/README.md). The spoke checks now cover the blade solid on its ridge, flank thickness ≥ 2.5 mm (measured 4.3) and the leading band at full height. **20/20 pass.** Mass at solid density is **88.5 g per wheel**, against 89 g in the register, so the D-005 register update is no longer needed. The chassis model is not changed.

**Print impact:** the rim still prints outer face down, because the hub cannot float over the inboard dish. The 15° flanks are then shallow overhangs and need tree supports.

**BOM changed:** CH-004 and CH-005 re-specified; CH-048 and CH-049 quantities go from 12 to 10.

---

## D-007

**2026-09-29 · Chassis / axle (CH-012, CH-015, CH-030, CH-051–CH-057; J01, J02, J03) · ACTIVE, HOLD on shop quote, fit coupons, axle rig and motor receipt**

**Decision:** the builder accepted the [axle stack](01-chassis/v1/research/axle-stack.md) architecture and its three choices: the bearing change, the turned one-piece stub, and designing around an absent motor. Per side, the stack is:

- **Stub.** One turned EN8 part carries torque and locates the wheel. It has Ø8 k5 bearing seats, a Ø4.05 bore on the motor's D-shaft (8 mm engagement), a DIN 916 M3 × 2.5 set screw on the flat, a Ø24 flange with three tapped M3, and a Ø10 spigot that centres the wheel.
- **Bearings.** Two **MR148ZZ** (8 × 14 × 4) in a bolt-on printed housing, held between a housing shoulder and a 1.2 mm aluminium cap. Four M3 × 18 screws pass through cap and housing into heat-set inserts in a 5 mm motor plate.
- **Motor alignment.** The motor floats on 0.3 mm of clearance at its pilot and face screws. The face screws are tightened last, through key slots, once the motor has aligned itself to the stub.
- **Wheel.** Three M3 × 6 screws through the web into the stub flange. Removing the wheel needs only those three screws.

**Why:**

- **The modelled stack was not buildable** ([axle-stack.md §1](01-chassis/v1/research/axle-stack.md#1-why-the-previous-stack-could-not-be-built-as-modelled)): no torque path motor → stub → wheel, no bearing retention, an over-constrained motor, and screw heads buried behind the bearings.
- **608ZZ does not fit.** A 608 pair is 14 mm wide, so it cannot sit inside the fixed Ø84 × 24 wheel together with a coupling and a flange.
- **A 678ZZ is not a substitute.** It is 8 × 12 × 3.5, not 8 × 14 × 4.

**Review holds from the proposal, and how the model now answers them:**

1. **Bearing designation** → MR148ZZ, not 678ZZ. CH-015 still needs the exact supplier article and drawing.
2. **Set screw breaking out of the stub end** → the stub now starts at |Y| 73 (1.5 mm off the motor pilot, in a 2.5 mm plate recess). The hole at 75.7 leaves 1.2 mm of steel to the end and 1.3 mm to the bearing seat. The M3 × 2.5 cup point sits flush with the Ø8.
3. **Edge margins** → four cap screws on the diagonals at R 12. The insert is ≥ 4.5 mm from the plate edges. The housing is Ø32, leaving 2.3 mm of wall outside each hole. The face-screw key paths now open into the bearing bore as slots at 0°/180°, instead of leaving a 0.2 mm skin. The slots sit off the vertical load line.
4. **Outward thrust on the inner rings** → still a k5 press fit plus Loctite 641; there is no room for a circlip. Required: 100 N outward hold, about 4× the load of lifting the robot by one wheel. Over 2 × π × 8 × 4 mm² of seat, that is 0.5 N/mm², far below any retaining compound's rated shear. **Not proven**: the axle rig includes a 100 N outward pull test.
5. **Screw-tip clash** → the wheel screws are M3 × 6, flush at the flange's inner face. A new check sweeps each rotating screw as a full ring: all are ≥ 1.55 mm clear.
6. **Fits** → all remain provisional until coupons (housing bore, spigot bore, inserts) and a quote.
7. **Shop quote** → still needed before ordering.
8. **Alignment proof** → axle-rig items: runout, drag and no-load current before and after tightening the face screws.

**Motor assumptions carried** ([D-005 motor interface](#d-005)): M3 face holes at ±8.5 mm, 5 mm deep; Ø7 × 2.5 pilot; Ø4 shaft 12 mm long with an 8 mm flat. The motor plate is the only part that encodes the face pattern. If the received motor differs, reprint the plate (or the carrier, J04). The stub's bore and set-screw position are the only turned features that depend on the shaft.

**CAD changed** ([body_chassis_model.py](01-chassis/v1/cad/body_chassis_model.py)):

- The flange/boss/diaphragm is replaced by `AXLE_MOTOR_PLATE`, `AXLE_BEARING_HOUSING` and `AXLE_BEARING_CAP`, plus the cap screws and inserts.
- New stub, set screw and wheel screws. The 608 STEP is replaced by parametric MR148 rings.
- The wheel pocket floor moves to |Y| 93, and the hub bore is Ø10 with 3 × Ø3.4 holes at PCD 16.
- Checks: `motor_face_joint_is_engaged` now requires ≥ 6 mm of shaft engagement. New checks: `axle_stack_is_retained`, `rotating_screws_swept_clear`, `bearing_model_is_mr148zz`. The old boss and 608 checks are removed.
- Mass register: frame +20.9 g, wheels −1.7 g each, axle row 64.4 → 44.0 g; all at the axle line.
- Check results: _pending the full rerun_.

**Interface for the standalone wheel CAD** ([D-005](#d-005)/[D-006](#d-006), [wheel model](01-chassis/v1/cad/wheel/README.md)): the wheel must now take the stub, not an Ø8 bore.

- Pocket R 18 to |Y| 93 (the web runs 93–97).
- Ø10 H7 bore through the web.
- 3 × Ø3.4 holes at PCD 16, clocked 30°/150°/270°.
- A flat seat for three ISO 7380 heads (Ø5.7) on the outer hub face.

The wheel model has not been changed by this entry.

**BOM changed:** CH-012 re-specified and set to DESIGN. CH-015 changed 608ZZ → MR148ZZ. CH-030 changed ISO 10642 M3 × 8 → DIN 7984 M3 × 6. Added CH-051 (housing), CH-052 (cap), CH-053 (M3 × 18 ×8), CH-054 (inserts ×8), CH-055 (set screws), CH-056 (M3 × 6 wheel screws ×6), CH-057 (Loctite 222/641).

**Next actions:**

1. Dimensioned stub drawing, then a quote from a local turning shop.
2. Print coupons: MR148 bore Ø13.90–14.10 in 0.05 mm steps; spigot bore Ø9.9–10.1; M3 × 4 insert holes; a plate section with counterbores.
3. Port the stub interface into the wheel model.
4. J04: the motor carrier and frame split.
5. Axle rig on receipt of the motor, with limits set before testing: runout ≤ 0.3 mm TIR, end play ≤ 0.1 mm, 100 N outward hold, drag and current before and after face-screw tightening, 200 reversals with set-screw paint marks.

---

## D-008

**2026-09-29 · Chassis / wheels (CH-004, CH-005, CH-048, CH-049, CH-058, CH-059; J14) · ACTIVE, HOLD with D-005 and D-007**

**Decision:** the builder chose this face over D-006's five-blade design. Two sessions had been restyling the wheel in parallel. D-006 was logged, but the CAD on disk became this design, and the builder confirmed this one. The design follows the builder's reference image: a 12-sided bolted beadlock, framed spokes, and a screwed hex hub cap. The tyre, chevron tread, rib keying and O-ring fallback are unchanged from D-005.

- **Spokes:** six framed spokes, 10 mm at the root, chamfered 1.5 × 1.5 to a 7 mm face, each with a recessed slot 3 mm wide and 2 mm deep. They run from a 26 mm hex hub, flats facing the spokes, to an inner ring with a 45° inner bevel. A 1 mm shadow groove sits between the inner ring and the clamp ring.
- **Clamp ring:** 12 sides, with six M3 × 8 screw flats (CH-048/049 back to 12 per robot) alternating with six recessed vent slots. The corners are chamfered and the flats are not.
- **Hub on the D-007 interface:**
  - the R18 pocket floor is at |Y| 93, over the bearing housing;
  - the web is 4 mm, with a Ø10 H7 bore on the stub spigot;
  - three Ø3.4 holes at PCD 16 (30/150/270° from +X) take the D-007 M3 × 6 button heads (CH-056) into the stub flange.

  Inside the pocket the spokes shrink to the 4 mm web, and the slot floor there is 2 mm.
- **Hub cap (new CH-058, CH-059):** a dark PETG hex cap, 26 mm across flats, with a faceted 16 mm boss. It stands 3 mm proud of the face (4.3 mm including screw heads), and a 1.9 mm-deep underside recess covers the three wheel screws. It is held by 6 × M2 × 6 thread-forming screws with 3 mm engagement. To remove the wheel: cap off, three M3 screws out, pull the wheel off the spigot.
- **Two-tone print:** rim and ring in light PETG, cap in dark PETG.

**Trade-offs:**

- The cap puts the hub 4.3 mm outboard of the wheel face, so the robot is **202.6 mm wide**, against the 205 mm target. Nothing on the chassis sits outboard of the hub.
- The rim and hub are 94.6 g per wheel at solid density, against 88.5 g for D-006 and 89 g in the register. The register needs +5.6 g per wheel when the wheel is ported into the chassis.

**CAD changed:** [wheel_model.py](01-chassis/v1/cad/wheel/wheel_model.py) and `check_wheel.py`. The checks add the D-007 pocket and turning flange clearance, the spigot bore, the 1.3 mm wall from bore to screw hole (D-007 geometry), wheel screws seated and ending at the flange face, the cap covering bore and screws, cap-screw engagement and seating, and a ≥ 0.5 mm cap wall (0.6). **23/23 pass.** The chassis model is still not changed; its `wheel_assembly()` keeps the D-007 plain rim.

**BOM changed:** CH-004 and CH-005 re-specified; CH-048/049 back to 12; CH-058 (hub cap) and CH-059 (M2 × 6 screws, 12) added.

**Records note:** the ledger has two entries numbered D-005, "Chassis / wheels" and "Chassis / motor interface", so `#d-005` links resolve to the first. Renumbering one is left to the builder, because D-007 links to the motor-interface D-005.

**Next actions:** the D-005 coupon adds the cap fit, the M2 pilot and strip torque, and the cap recess over real M3 heads. Port the wheel into `wheel_assembly()` together with the D-005/D-007 follow-ups: mass register, loaded radius, and the rotating-screw sweep, which must now include the cap.

---

## D-009

**2026-09-29 · Chassis / wheels (CH-005, J14) · ACTIVE; full `check_layout.py` rerun pending**

**Decision:** the builder asked for a second tyre and for the D-008 wheel to be merged into the chassis-v1 CAD.

- **Handed tyres.** The right wheel is the left one turned round. With identical tyres, the right chevrons would point backward relative to travel. The right tyre is now the left one **mirrored**, so on the robot both chevrons lead forward, apex at the top toward +X (tractor convention). The chevron was flipped to lead forward on the left as well. Rim, clamp ring, hub cap and hardware are symmetric and identical on both sides. CH-005 becomes one left and one right tyre; they are not interchangeable. **Amended by [D-070](#d-070) (2026-10-29):** the tyre is symmetric about its mid-plane, so the "right" tyre is the left one turned over: one part, printed twice and fitted with the V at the top pointing forward. The CAD and the forward-leading check stand.
- **Merged into chassis-v1.** [`wheel/wheel_model.py`](01-chassis/v1/cad/wheel/wheel_model.py) is now the single source for the wheel. `wheel_assembly()` in [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py) places its `mounted_leaves(side, …)` and keeps D-007's stub and set screw. A new `_check_wheel_interface()` stops the build if the wheel's hub constants drift from the D-007 ones: pocket, bore, spigot, flange, and screw PCD, length, head and angles. The placeholder tyre and rim and the spin-index inlay (and its constants) are gone.

**Checks:**

- **Wheel alone:** `check_wheel.py` 24/24. New: `both_tyres_lead_forward_when_mounted` measures +7.0 mm on each side, and an un-mirrored right tyre reads −7.0, so the check discriminates.
- **Wheel on the chassis:** the new targeted script [`check_wheel_on_chassis.py`](01-chassis/v1/cad/wheel/check_wheel_on_chassis.py). `check_layout.py` assumes an axisymmetric wheel and treats its solids as the swept volume, which is no longer true. So every rotating part except the rim and the (axisymmetric) stub is swept as a revolved envelope, and the rim is turned through its 60° period in 5° steps. **All clear of the 1.5 mm running gap:**
  - rim ≥ 3.05 mm through 60°, to the bearing cap;
  - tyre 3.6 mm to the wheel-arch trim;
  - hub cap, ring screws and cap screws are further away;
  - the tightest are D-007's own parts: stub 1.5 mm to the bearing cap, set screw 1.53 mm, wheel screws 1.65 mm.

  Wheel on stub: 3 screws, 2.0 mm of thread each in the flange, no internal overlaps.
- **`check_layout.py`:** its `rotating_screws_swept_clear` count goes 8 → 32. The full run was **stopped at 42 minutes by the builder's choice** (normally about 10 min; the lugged tyre slows its whole-robot boolean sweeps). **It has not been rerun**, so its other wheel-dependent rows (track from the rim centre, loaded radius, connector/power clash maps) are unverified. Rerun it with the frame-split work.

**Mass register:** WHEEL_L/R 87.3 → 92.5 g (the wheel without the D-007 screws, which are counted with the axle), CoM kept on the wheel centre (in fact about 1 mm outboard).

**Not updated:** `body-chassis.step` (whole robot, gitignored, about 0.5 GB) still shows the old wheel until it is regenerated. `chassis-v1.step` is rebuilt.

**Next:** rerun `check_layout.py` in full; the D-005/D-008 print coupons; print one tyre of each hand.

---

## D-010

**2026-09-29 · Chassis / axle and frame (CH-001, CH-015, CH-060, CH-061; J02, J04) · ACTIVE; HOLD on printer/material coupons, clearance rerun and axle rig**

**Decision:** select the manufacturer article NMB L-1480ZZ (8 × 14 × 4 mm, MR148ZZ size) and define J04 as a removable, keyed carrier-to-rail joint. Use one printed carrier per motor side, combining the 5 mm motor plate and its front/rear cheeks; keep the bearing housing and retaining cap separate. Each carrier keys into the front and rear rail ends and clamps with two DIN 7984 M3 × 8 screws at each end, into 6 mm M3 heat-set inserts in the rails.

**Why:** this creates a modeled structural load path from the bearing housing through the motor plate/cheeks into both longitudinal rails while retaining independent wheel axles. The crossmembers span left-to-right at the front and rear; there is no axle shaft across the centreline. Keys set the carrier position so the screws clamp rather than locate it.

**CAD changed:** `body_chassis_model.py` fuses each motor plate with its two cheeks into `AXLE_MOTOR_CARRIER_L/R`; rail ends now contain 2.0 × 3.0 × 2.5 mm keys/pockets, two axial insert bores and tip relief per end. The model includes the eight J04 screws/inserts. `check_layout.py` now measures the gearbox seat and bearing housing against the carrier label. The README, checklist, axle-stack plan and BOM were updated.

**Nominal joint:** key pocket has 0.2 mm per-side and 0.7 mm end clearance; screw axes are at Z 38/48 mm, Y ±54 mm front and ±58.5 mm rear. Rail insert pilot is Ø4.3 × 6 mm. These are coupon starting values, not final process compensation.

**Bearing source:** NMB's [official L-1480ZZ page](https://nmbtc.com/parts/l-1480zz/) confirms the 8 × 14 × 4 mm article, 819 N dynamic rating and 386 N static rating. Official CAD is offered through PARTcommunity; retrieving its drawing/CAD and confirming the supply lot remain release actions. Ratings are catalog values and do not certify the printed housing, axle arrangement or retaining-compound joint.

**Verification:** a focused source-geometry check found no positive-volume intersection across the carrier, rail, screw and insert solids. This does not prove strength, print fit or fatigue. The latest wheel-on-chassis sweep was attempted but interrupted after several minutes before it produced results; the pre-J04 D-009 sweep remains the last complete nominal result. Full `check_layout.py` remains pending.

**Physical pass targets:** axle datum deflection ≤0.25 mm under 31 N radial and 8 N lateral service loads; ≥1.5 mm running gap at those loads using measured print stack; proof at 62 N, 16 N and 0.8 N·m with no cracks/insert movement and ≤0.10 mm residual set. Each insert coupon must hold 100 N axially. Axle rig limits remain runout ≤0.30 mm TIR, end play ≤0.10 mm, 100 N inner-ring retention for 10 s with <0.10 mm movement, current change within max(0.05 A, 10%) after face-screw tightening, and 200 low-speed reversals.

**Next:** retrieve the NMB technical drawing/CAD and confirm a lot; print bearing, insert and J04 key coupons after printer/material selection; rerun the current wheel sweep and full layout checks; build the side-specific axle rig when the real motor and turned stub are available. No physical test has passed yet.

---

## D-011

**2026-09-30 · Chassis / nose (CH-002, CH-003, CH-007, CH-019, CH-031–033, CH-062–064; J07, J08) · ACTIVE; HOLD on received caster, coupons and physical tests**

**Decision:** close the ball-transfer section's blocking CAD items from the printability and service-access review in one change, in [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py). The [joint register](01-chassis/v1/joint-register.md) J07/J08 entries carry the details.

**Changes, by the builder's to-do numbering:**

1. **Caster fastening (J07A).** The three M3 screws used to end 3 mm into Ø3.2 clearance holes and held nothing.
   - Pololu's drawing 2691 shows a 2.7 mm web with Ø6.3 counterbores from the ball side. The imported STEP lacked them, and the model now cuts them.
   - The screws are now 3 × ISO 7380 M3 × 8 (CH-031), driven from below into 3 × CNC Kitchen M3 × 5.7 inserts (CH-063). The inserts go in Ø4.0 bores in a pod seat thickened from 3 to 6 mm.
   - Result: 5.3 mm of thread engagement, and the heads sit 0.43 mm off the ball.
   - The GP2Y now rests on the seat top (Z 35), so its rails are gone. No reclocking was needed.
   - The old `ball_screws_engage_flange` check is replaced by `ball_screws_thread_into_seat_inserts`. It needs ≥ 4.5 mm of shank inside a coaxial insert that sits in the seat.
2. **Touch cap (J08B).** The cap could only travel about 0.7 mm before it jammed on the raked prow, so the 3 mm switch travel was not real.
   - The nose is now a constant octagonal section from X 122.5 to the face. The cap's 0.5 mm running gap is now true: it measured 0.41 mm before.
   - The 0.5 mm flexures are replaced by two 2.0 × 16.5 mm vertical snap fingers with 0.8 mm hooks in flank slots, at about 2.2 % strain for a 1 mm spread.
   - The cap slides 3.0 mm and stops on the pod face. It slides off forward.
3. **Pod sliver.** The 0.40 mm skin sat at the ear slot's front end, where the old taper began at the slot.
   - The belt now holds full width to X 121.0, and a chamfer wedge outside the ear window is removed.
   - The slot's outer edge cannot move in to Y 21.5: the GP2Y ear flange measures ±22.25 mm, and the slot must stay full height so the sensor can lift out.
   - The same pass found an older open slit: the 15.5 mm pocket broke through the upper chamfer at Z 47–49 behind the belt, X 95–109. The pocket now narrows at 45° above the pod screw heads, to |Y| 12.3.
4. **Lid retention (J08C).**
   - A rear tongue drops into a pod-wall groove that is open forward.
   - The shell band sits 0.5 mm over the lid.
   - One M2 × 8 countersunk thread-forming screw (CH-062) goes into a pod boss at (124.6, −11.8).
   - Official removal: cap off, screw out, slide the lid 11 mm forward, lift.
5. **Cable exit.** The J10-8 route is modelled as harness reserves:
   - a round-cornered 6 × 3 mm slot at Z 32–35 through the pod back wall, with a 1 mm flared mouth;
   - a floor trough, plus a groove for the switch pair;
   - a run under the crossmember;
   - a new Ø5 bore through the crossmember and deck at (86, −31);
   - a riser beside the speaker cavity into the sensor trunk, and a drop to C3 J10-8 below the compute tray.

   No grommet.
6. **Switch (CH-019).** Panasonic ESE22MV21 detector switch: 4.25 mm full travel, 290 mN max ([datasheet](https://industrial.panasonic.com/cdbs/www-data/pdf/ATB0000/ATB0000C12.pdf)). It sits on an 8 × 6 × 0.8 carrier board (CH-064) in a floor recess. The lever tip sits 0.2 mm off the cap at rest. Tact switches were rejected because their travel is well under 1 mm.
7. **Cap clearance.** Fixed by the constant nose (item 2): the running clearance measures 0.50 mm.
8. **Inserts (CH-033, CH-063).** CNC Kitchen M3 × 5.7 standard, Ø4.0 hole and Ø4.6 knurl ([source](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)). The Ø4.0 bores now give 0.3 mm/side of interference; before, the modelled insert equalled the bore. The crossmember pod screws (CH-032) become ISO 7380 M3 × 8 with 5 mm of engagement.

**Verification (2026-09-30):**

- **Full `check_layout.py`: not rerun, by the builder's choice.** Its saved report still dates from 27 Sep, and the D-009/D-010 reruns also remain pending.
- **Nose checks:** the new [`check_nose_joints.py`](01-chassis/v1/cad/check_nose_joints.py) runs the J07/J08 rows of `check_layout.py` on the nose parts in about 30 s. All 12 pass:
  - thread engagement;
  - insert interference;
  - flange seat;
  - no nose clashes;
  - travel reserve clear;
  - 3 mm cap sweep with the hard stop and forward retention;
  - 0.50 mm running clearance;
  - nose width 40.6 mm;
  - shell notch clear;
  - CoM margin.

  `check_layout.py` itself parses but has not been run end to end with the new rows.
- **Service sweeps, body on:** [`check_nose_service.py`](01-chassis/v1/cad/check_nose_service.py) → [`nose-service.md`](01-chassis/v1/cad/generated/nose-service.md). Clear:
  - caster housing, ball, screws and base from below, with nothing else removed;
  - the three hex-key paths;
  - cap forward;
  - lid forward, then up;
  - sensor and switch up;
  - lid-screw driver;
  - every J10-8 reserve.

  The first run found three problems, all fixed and re-swept: the sensor was trapped by the new neck, the lid hit the front panel when lifted after 8 mm, and the cable drop hit the compute tray.
- **Printability** (DfAM tool, 4000 samples):
  - Pod: minimum wall 1.3 mm, was 0.40; 3.2 % support area printed seat face down.
  - Cap: 0.94 mm, the same bottom edge as before; 2.8 % support nose face down.
  - Lid: 3.4 % support on its side, against 41 % flat. Its lowest samples, 0.3–0.6 mm, are 45° knife edges along the split line through the chamfer, as before; they are edges, not skins.
- **Mass register** (hand-kept):
  - `BALL_NOSE_POD_SENSOR_CAP`: 15.9 → 18.7 g at (111.4, 0, 37.9), measured from the solids.
  - `CHASSIS_PRIMARY_FRAME`: −0.3 g for the bore.
  - Whole robot: 2590.1 g, CoM X +19.30 / Z 106.28 mm. a_tip is 1.78 against the 1.58 minimum, so the margin line passes (equivalent to X ≥ 17.1 mm at this height).
- **Exports:** `chassis-v1.step` is rebuilt. `body-chassis.step` is not regenerated.

**Still unverified:**

- the received #2691 web, counterbore, hole diameter and housing;
- insert pull-out in the pod seat and crossmember;
- the switch's ON point and force against the cap;
- snap-finger fatigue;
- lid screw strip torque;
- static load at 2.55 kg, drop and threshold climbing (set the pass numbers before testing);
- the timed body-on service dry run for the caster swap and the sensor swap;
- the J07B L-key reach at the dry run (about 12 mm to the GP2Y).

**Next:** measure the caster on receipt; print the pod, lid and cap in the stated orientations; run insert coupons, then the load, cap and service tests; write the caster and sensor service procedures from the dry run.

---

## D-012

**2026-09-30 · Chassis / axle (CH-015, CH-051; J02) · ACTIVE; HOLD on supplier availability, lot verification, drawing/load data, fit coupons, clearance rerun and retention test**

**Decision:** select the **688 ZZ, 8 × 16 × 5 mm** double-metal-shielded chrome-steel bearing listed by [OnlyScrews](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5) as the chassis design article. This supersedes the NMB L-1480ZZ/MR148ZZ selection in D-007/D-010; the axle-stack architecture, Ø8 stub and wheel interface remain. Use two bearings per side, four total.

**Reason:** the user selected a locally listed, standard 8 mm-bore bearing family after the previously selected L-1480ZZ could not be procured. The 688 ZZ uses the same 8 mm bore but has a larger 16 mm OD and 5 mm width, so its seat and positions must be changed in the CAD.

**Supplier evidence and procurement hold:** the listing gives ID 8 mm, OD 16 mm, width 5 mm, ZZ shields and chrome steel. It does not identify a manufacturer or publish a drawing, internal-clearance class or load ratings. At review, the page shows “Sold out” in its purchase panel while also displaying “In stock” in its descriptive copy. Treat current stock as unavailable/unconfirmed; obtain a confirmed orderable lot and preserve its markings and manufacturer data before physical qualification. No load rating is inferred from the page's generic claims.

**CAD change:** `body_chassis_model.py` now models 688 ZZ rings, OD radius 8 mm and 5 mm width. The pair occupies |Y| 76.51–81.51 and 81.51–86.51; the 0.01 mm inboard datum offset avoids a degenerate mirrored housing boolean. The Ø16 outer seat is coupon-tuned; bearings stand 0.16 mm proud of the housing's 86.35 mm outboard face for cap retention. The stub shoulder and wheel positions stay fixed. The set-screw station remains |Y| 74.8, giving 0.46 mm nominal from the Ø2.5 tap drill to the first bearing face. Verify this narrow land on the stub drawing and part. CAD checks assert the selected bearing and seat dimensions. Supplier STEP/drawing is unavailable, so the rings remain parametric placeholders.

**Fit and proof gates:** coupon the printed seat Ø15.90–16.10 mm in 0.05 mm steps; verify the actual Ø8 k5 shaft fit, race drag, shield clearance, runout and endplay with delivered bearings. Retain the inner rings by k5 plus Loctite 641 and pass the 100 N outward-hold test for 10 s with <0.10 mm movement. Rerun wheel-to-chassis clearance and full `check_layout.py`; inspect the nominal 0.46 mm edge clearance from set-screw tap drill to first bearing face on the turned-stub drawing. No physical fit, load or retention test has passed.

**Next:** monitor/order from the selected listing when available or obtain the same specified article from a confirmed supplier; request manufacturer, internal-clearance class, drawing and load data; then print fit coupons and run the motor-independent retention fixture. Motor-dependent axle testing remains separately blocked on motor receipt.

---

## D-013

**2026-09-30 · Chassis / nose (CH-007, CH-019, CH-064, CH-065, CH-066; J08B) · ACTIVE; HOLD on bench trip-point check and the PCB-10 J10-8 pin change**

**Decision:** replace the D-011 nose switch with contactless sensing. A TI DRV5055A3 linear Hall sensor on a small board in the pod seat reads a Ø2 × 1 N35 magnet in the touch cap, and the C3 firmware sets the trip point. Two small compression springs return the cap. Details: [nose-hall-board.md](01-chassis/v1/research/nose-hall-board.md).

**Why:** D-011 misread the Panasonic ESE22MV21 drawing. The "4.25 mm (2.05 mm)" figure means a full travel of **2.05 mm**; 4.25 is a height. The switch turns on at 1.5 ± 0.3 mm. A rigid 3 mm cap therefore either misses the switch or crushes it, with 0.25 mm of worst-case margin. Other options were considered and rejected:

- **DRV5033AJ Hall switch:** its worst-case thresholds (operate 3–12 mT, release 1–5 mT) need a 12:1 field ratio across the stroke. A small magnet over 3 mm gives about 7:1.
- **DRV5032ZE:** 20 Hz sampling, up to 75 ms latency.
- **Omron D2F hinge lever:** operating position tolerance of ±1.5 mm.
- **Foam pad, or a 2 mm stroke:** these depend on material properties or print tolerances.

The linear sensor with a boot-calibrated threshold has none of these limits. It also has no mechanical wear.

**CAD** ([`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py)):

- **Hall board:** 6.0 × 4.6 × 0.8 mm, standing in an open-top slot at X 126.6–127.4. The SOT-23 sensor sits in a notch through the seat's front face, centred at (Y 10, Z 32.6).
- **Magnet:** in a pocket in the cap wall, below the window slit. It clears the sensor by 3.1 mm at rest and 0.1 mm at the 3 mm stop.
- **Springs:** two spring pockets, Ø3.3 × 6 mm at Y ±3, Z 32.
- **Removed:** the D-011 floor recess, switch and lever.
- **Lead groove:** extended to the board.
- **Checks:** `check_layout.py` and `check_nose_joints.py` now check the magnet against the sensor at the stop, and treat the springs as compressible.

**Trip point** (on-axis field of the magnet, Hall plate 0.65 mm under the package top, still to confirm):

- 7.3 mT at rest, 15.7 mT at 1 mm, saturated at the stop.
- Firmware trips at rest + 5 mT and releases at rest + 3 mT.
- Trip is 0.71 mm of cap travel nominal, 0.50–0.95 mm over ±0.4 mm of gap and ±5 % Br. Release is at 0.48 mm.

**Interface change:** J10-8 becomes +5V, GND, GP2Y_VO, +3V3, HALL_OUT. The PCB-10 carrier must bring +3V3 and an ADC-capable pin to J10-8 in place of the switch pair.

**BOM:**

- CH-019 → DRV5055A3QDBZR.
- CH-064 → Hall board.
- New: CH-065 magnet, CH-066 return springs (2).
- CH-007 gains the magnet pocket.

The mass row is unchanged at about 0.3 g for the sensing parts.

**Verification (2026-09-30):**

- `check_nose_joints.py`: 12/12 pass. Magnet gap is 3.1 mm at rest and 0.1 mm at the stop, with no hits.
- `check_nose_service.py`: the Hall board lifts out once the cap and lid are off, and the cap slides off forward. The tool paths and the whole J10-8 route are clear. See [nose-service.md](01-chassis/v1/cad/generated/nose-service.md).
- `chassis-v1.step` is rebuilt.
- Full `check_layout.py` has not been run, by the builder's choice.

**Open:**

- the bench trip point (pass: 0.4–1.2 mm against a dial indicator);
- the spring rate, and whether the cap returns to its hooks from any position;
- the Hall plate depth from TI's package drawing;
- the PCB-10 J10-8 pin change and the C3 firmware threshold;
- magnet polarity at assembly.

---

## D-014

**2026-09-30 · Chassis / rear keel (CH-008, CH-009, CH-010, CH-020, CH-034, CH-067 to CH-072; J09A/B, J10A/B) · ACTIVE; HOLD on the CH-020 breakout, CH-009/CH-010 materials, coupons and physical tests**

**Decision:** close the rear TCRT keel's attachment, cartridge, cable and wear-part joints in CAD (to-do sections A–D). Joint details are in the [joint register](01-chassis/v1/joint-register.md#j09a--rear-keel-to-rear-crossmember).

**Why:** the keel screws ran into solid crossmember plastic, and the TCRT had no retention. The cable's Ø6 holes would not pass the 6.5 mm GH plug, and the old riser clipped them. The height shim overlapped the leads, and the shoe and guards were only fused to the keel.

**CAD** ([`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py)):

- **J09A, keel to crossmember:**
  - Four ISO 4762 M3 × 30 screws go into CNC Kitchen M3 × 5.7 inserts, fitted from below. Engagement is 5.5 / 5.7 mm; the insert length caps it below the 6–8 mm first asked for.
  - The rear pair moves from X −45.5 to −44.0. At −45.5 the insert left 0.2 mm of wall to the crossmember's rear face; the wall is now 1.7 mm (2.2 mm at the front face).
  - The counterbores are Ø6.5, and the crossmember's Ø6 cable bore is closed.
- **J09B, TCRT to keel:**
  - The pocket is open below the keel. The TCRT sits face down on the 0.6 mm end ledges of a printed bezel.
  - The leads go into a pass-through socket on the breakout, which sits in an open-top cavity behind the crossmember.
  - The height is set by 1 mm shims between the bezel and the keel belly (Z 12): two shims give Z 10, and zero to four give 12 to 8.
  - One M2 × 10 and a moulded pin fix the bezel. The old steel shim that overlapped the leads is removed.
- **Keel section:** the sensor flat widens to a 9.5 mm half-width, and a station at X −46 keeps the belly flat over the shim stack. The pocket wall at the chamfered edge goes from about 1.6 to 3.9 mm (to-do 15). The keel still has 1.0 mm of clearance in the 10.5 mm shell slot.
- **J10A, wear shoe:** it has a 2.5 mm dovetail tongue in a groove open at the front, held by one M2 × 6 thread-forming screw across the tongue.
- **J10B, guards:** both guard lips are now part of the bezel.
- **J10-10 cable:**
  - The disconnect is a top-entry GH4 on the breakout, so the keel comes off with four screws and one plug.
  - The cable leaves upward behind the crossmember, in the 7.6 mm gap to the shell wall, so neither the crossmember nor the deck needs a hole.
  - `harness_routes()` gains a 30 mm slack loop, a riser beside PCB-02 and a run over PCB-04, under the compute tray, to C3 J10-10.
  - A zip tie through a new lug on the crossmember's rear face gives the strain relief.
- **Breakout (CH-020):** still unselected. It is modelled as a 12.3 × 13 mm custom-PCB reserve; the 32 × 14 mm LM393 module does not fit.

**Mass:** REAR_SKID_KEEL goes from 12.0 g at (−39.9, 0, 20.4) to 19.6 g at (−40.2, 0, 22.4), with volumes measured from the solids. The model now reports 2605.1 g with the CoM at (19.07, 0.16, 105.87). The margin line needs X ≥ 17.08.

**BOM:** CH-008, CH-009, CH-010 (now one bezel), CH-020 and CH-034 are updated. New rows: CH-067 inserts (4), CH-068 shims (2), CH-069 to CH-071 M2 screws, CH-072 zip tie.

**Verification (2026-09-30):**

- New `cad/check_rear_keel.py` (about 2 min): 21 of 21 checks pass. It writes [rear-keel-checks.json](01-chassis/v1/cad/generated/rear-keel-checks.json). It covers:
  - no clashes in the keel stack;
  - screws in clear holes, with at least 5 mm of engagement;
  - hex-key paths from below;
  - shims clear of the TCRT;
  - the ±2 mm range;
  - sensor swap from below with the keel on;
  - the shoe sliding out forward;
  - the keel dropping 30 mm;
  - the board lifting out;
  - the J10-10 route clear of the frame, shell, electronics, body frame, panels, audio and sensors.
- `check_layout.py` keel rows are updated: the count-only screw row is replaced, and the shoe/guard backing rows follow the new parts. The pitch order (shoe 6.05°, guards 6.49°, keel 8.97°, sensor 10.43°), backing and CoM rows were run on their own and pass.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- to-do 8: select the CH-020 breakout and socket;
- to-do 12: choose the wear-shoe and bezel materials;
- E (print orientation and exports) and the rest of F;
- G (optical height on real floors, service timing, tip order).

---

## D-015

**2026-09-30 · Chassis / rear TCRT (CH-020, CH-071; J09B) · SUPERSEDED by [D-016](#d-016)**

**Decision:** CH-020 is a custom passive board. Its spec was removed by D-016. The TCRT5000 plugs into two 1 × 2 female headers underneath the board, and a top-entry GH4 on top is the J10-10 disconnect. The board has no comparator: the C3 node pulses the LED through a MOSFET and reads the phototransistor on an ADC1 pin. It subtracts ambient light, and any fault reads as a cliff.

**Why:** the builder asked for an off-the-shelf board first, and none fits the keel cavity of about 13 × 14.8 mm:

- the LM393 modules are 35 × 10 mm;
- the Soldered breakout is 22 × 22 mm;
- the Pololu QTR-1A fits, but carries a QRE1113 rated to 6 mm, against our 10 mm optical height, and cannot be swapped from below.

**Changes to D-014:**

- **Floating board:** the TCRT5000's standard 3.5 mm leads cannot stay engaged over ±2 mm in a socket on a fixed board. The board now rides on the fully seated sensor and moves with the shims (Z 20–25.6). A ledge at Z 19.8 only catches it while the sensor is out. The M2 × 5 board screw (CH-071) is dropped.
- **Socket:** the datasheet lead pitch is 5.5 × 2.54 mm, so the D-014 4-way block becomes two 1 × 2 strips, with the package's mounting clips between them.
- **Board size:** the GH4 moves to +Y 4.6 to clear the strips' solder joints. The board grows to 14.2 mm in Y, and the cavity to ±7.4 (keel side wall 2.1 mm).

**Interface change:** J10-10 changes from 5 V / GND / analog / digital to +3V3 / GND / TCRT_OUT / LED_EN. PCB-10 must provide an ADC1 pin with a 100 kΩ pull-up (fail-safe when unplugged) and a spare GPIO.

**CAD:** in `body_chassis_model.py`:

- the board, the two header strips and the moved GH4 are modelled;
- the cavity is widened and has a new ledge;
- the J10-10 service loop is widened to Y +7;
- the REAR_SKID_KEEL row goes from 19.6 to 19.4 g, without the M2 × 5 screw.

**Verification (2026-09-30):**

- `check_rear_keel.py` passes 23 of 23. The new rows cover:
  - the sensor stack clearing the keel at both ends of the J09 range;
  - the board sitting 0.2 mm above the ledge at the lowest setting;
  - the board riding on the seated sensor.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- confirm the emitter end against the placed STEP;
- check JST's BM04B land pattern against the 14.2 mm board edge;
- confirm a 5.0 mm dual-leaf header part;
- make the PCB-10 J10-10 change;
- bench item 20, which sets R2 and checks the fail-safe.

---

## D-016

**2026-09-30 · Chassis / rear TCRT (CH-020; J09B) · ACTIVE; HOLD on the PCB-10 J10-10 change and bench item 20**

**Decision:** there is no board in the keel. The TCRT5000's legs are soldered to a JST GH 4-way pre-crimped lead (AWG28, 350 mm) under heat-shrink, and the lead plugs into C3 J10-10. The LED resistor, the LED switch MOSFET, the gate pull-down and the phototransistor load/pull-up go on PCB-10. Spec: [rear-tcrt-lead.md](01-chassis/v1/research/rear-tcrt-lead.md). Supersedes [D-015](#d-015).

**Why:** the builder asked why a board was needed. Electrically it isn't: the D-015 board only carried a connector and a socket. The builder chose the simpler build over the two things the board gave:

- **Keel removal** now needs the sensor pulled out first, and J10-10 unplugged at PCB-10.
- **A sensor swap** replaces the sensor and its lead together.

**Changes from D-015:**

- **Keel:** the board cavity and ledge are removed, and the sensor pocket runs straight out through the keel top. This restores the full side walls. Keel body 14.64 cm³; the REAR_SKID_KEEL row is now 20.0 g at (−40.5, 0, 22.7).
- **CAD:** a heat-shrink joint envelope and the lead are modelled, and the slack loop goes back to Y −26 to 3.
- **J10-10:** pins are LED_A, LED_K, TCRT_OUT and GND. It is still a GH 4-way header, now wired to the PCB-10 circuit in the spec.
- **Fail-safe:** an open lead or dead LED reads high through the PCB-10 pull-up, which is a cliff.

**BOM:** CH-020 becomes the sensor and lead (CANDIDATE). CH-071 stays DROPPED.

**Verification (2026-09-30):**

- `check_rear_keel.py` passes 20 of 20.
- The new rows cover:
  - the sensor and lead dropping out below with the keel on;
  - the lead leaving through the keel top without touching it;
  - the stack clearing the keel across the J09 range.
- `chassis-v1.step` is rebuilt.
- The full `check_layout.py` has not been rerun.

**Open:**

- the PCB-10 J10-10 circuit;
- bench item 20 (sets R2, includes a motors-running pickup check);
- the joint sleeve fitting the 7.6 mm pocket on the real part.

---

## D-017

**2026-09-30 · Chassis / rear keel wear parts (CH-009, CH-010; J10A/B) · RECOMMENDED; confirm after the physical tests**

**Recommendation:** print the wear shoe and the TCRT bezel (with its guard lips) in **PETG**. The builder asked for a recommendation and delegated the choice.

**Why PETG over PLA:**

- **Impact:** the 1.5 mm guard lips and the shoe take floor strikes on a tip. PETG bends where PLA snaps.
- **Screws:** both parts carry thread-forming M2 screws (CH-069, CH-070), and PLA tends to crack around them.
- **Heat:** PLA softens around 55–60 °C and creeps under the screw clamp; PETG holds to about 75 °C.
- **Same print:** the keel is already a PETG candidate, so all the keel parts print in one material.
- TPU is excluded: its friction would grab the floor.

**Optional upgrade, not modelled:** if the shoe wears fast or drags on carpet or tile, add UHMW-PE tape (about 0.25 mm) to its sole, and thin the shoe by the same amount so the floor clearance and tip order stay unchanged. Nylon (PA) is the better printed wear material, if a printer that can run it becomes available.

**Changed:** CH-009 goes from OPEN to DESIGN, and CH-010's release check names PETG. J10A and J10B record the material. No CAD change.

**Open:** retention, abrasion, floor-strike and snag tests (items 21–22); revisit after the tests.

---

## D-018

**2026-09-30 · Chassis procurement and release scope · ACTIVE; receiving, fabrication and physical validation remain open**

**Decision:** record the user's settled **Pololu #2691 plastic-roller caster** and **Samsung INR18650-25R cells** as SELECTED. Correct the current motor row to SELECTED under D-003/D-005; purchasing the motor enables its receiving and load checks. SELECTED does not mean ordered, received, fitted or passed. Supplier-page stock and physical release checks are separate fields.

The canonical [BOM](BOM.csv) and [chassis snapshot](01-chassis/v1/BOM.md) contain the current supplier candidates, exact-match qualifications, and release checks.

**Recommendations, not new installed substitutions:** retain two DRV8874 carriers and the Sharp A41 for the current design; reject the OD8/free15/wire1 return spring; sample MISUMI C-UR3-10 if its quote is acceptable; buy the bare TCRT specified by D-016; consider Robokits MPU6050 for budget bench use. Ø3 × 1.5 mm N35, the purchased balanced 2S module and 5 A ATOF are conditional alternatives. Magnet pocket/threshold, IMU interface/mount, protection thickness and fuse/holder/current requirements must be resolved before adopting those changes. BF-013A compatibility is not established. No corresponding CAD substitution was made.

**Sourcing correction:** OnlyScrews BB688ZZ now shows in stock, superseding D-012's dated sold-out observation. Its maker/grade/load evidence, received fit and retention remain open. Common matched-size hardware and dowel links are recorded; DIN 7984 low heads, M3 × 18 button heads, M3 × 2.5 cup-point set screws, plastic thread-forming screws, selected 5.7 mm inserts and Loctite 641 retain exact-source work. Nearby articles are not approved substitutions.

**Test scope:** regulated supply-powered chassis tests may use a documented development controller, driver carriers, temporary harness and relevant sensor circuits before final system PCB fabrication. Verify intentional voltage/current limits, encoder logic, default disable, physical stop and braking/transient behaviour. Keep cells disconnected and use secured inert ballast for that scope. Battery-powered tests retain protected-pack construction, fuse/disconnect, thermal/charging and 8.4 V motor-control gates.

**Genuine new findings:** Samsung recommends >1 mm cell spacing against the current 0.2 mm CAD gap. The nose Hall note now treats trip values as predictions and records startup-pressed, missing-magnet and wire-break checks; shared 3.3 V supply does not make the ESP32-S3 ADC ratiometric. Define and verify diagnostic bias, ADC calibration and contact thresholds before functional release. These documentation corrections do not claim implementation or a passed test.

**Release audit:** nose/rear joint architecture is defined under D-011/D-013/D-014/D-016, while physical proof is open. Remaining detail gaps include J05/J06/J16, J11A/B, J12/J13 and J15A/B; purchased interfaces/stub drawing and print/process release are also pending. The saved full-layout baseline predates current source/checker changes. Stage gates are summarized in the chassis BOM; #4804 is superseded, not a current variant blocker.

**Custom PCB work:** a separate [04-custom-pcb folder](04-pcbs/README.md) (renamed `04-pcbs/` in D-038) now records the unreleased board work packages. No schematic, Gerbers or fabricated-board result is implied. Pre-existing edits to the chassis checker and engineering checklist were preserved. A malformed comma-delimited CH-012 release-check field was repaired while updating the BOM; installed quantities are unchanged.

**Verification:** thirteen review reports produced; supplier observations and documentation audited. No hardware purchase, receipt, CAD regeneration or physical PASS was performed in this review. Final CAD checks require the compatible pinned runtime and the release revision.

## D-019

**2026-09-30 · Chassis user selections: drivers, front range, nose magnet and pack protection · SELECTED; receiving and system validation open**

**Selected by the builder:** two Adafruit #3297 DRV8833 boards, one per motor, with both bridges paralleled within each individual board; Sharp GP2Y0A21YK0F from Robocraze; N35 Ø3 × 1.5 mm nose magnet; and Robocraze TIFPS0629 balanced 2S protection module, which the builder intends to buy. The builder reports the Sharp sensor is in stock and the only possible source/choice. These selections supersede prior alternatives and recommendations recorded in D-018 and the point reports.

**CH-064 conclusion:** retain the 6.0 × 4.6 × 0.8 mm custom nose Hall carrier. Its job is to hold the bare TI DRV5055A3, decoupling/filter parts and three-wire interface in the seat's specific slot. An adapter board can test the circuit on a bench but cannot satisfy the installed envelope. Layout/fabrication and contact/fault validation remain open.

**Engineering gates:** Adafruit/TI documentation supports the proposed bridge-parallel arrangement, but not an unconditional chassis current or thermal pass. Commission at a regulated 6 V supply with measured motor current, board temperature and braking/transient checks. The A21's 100 mm minimum range and 38.3 ± 9.6 ms measurement cycle do not satisfy the existing 50 ms stop-path budget once scan/control delay is included; revise and demonstrate the system timing/stopping distance while retaining the selected sensor. Measure actual A21 mounting datums before fit release. The 3 mm magnet changes the CAD pocket; check cap wall, pole, air gap and calibrated contact trip on the physical assembly. Robocraze's module listing gives a 48 × 20 mm footprint but does not establish its thickness or protection behavior; measure and qualify the received board before connecting cells. SELECTED or intended to buy does not mean ordered, received, fitted or passed.

**CAD and BOM:** update the source model, CAD checker names and project/chassis BOM to these choices. The model represents the A21 and Adafruit boards as nominal envelopes until received parts are measured. Generated STEP and reports are stale until the pinned compatible CAD runtime is restored and the affected checks are rerun. The 2.9 mm BMS height remains an unverified legacy placeholder, not a measured module dimension.

## D-020

**2026-09-30 · Chassis / nose return springs (CH-066) · SELECTED for purchase; installed behavior unverified**

**Decision:** the builder selected the Industrybuying listing for RS PRO 821245 stainless compression springs (pack of 10), with two required for the chassis. Published listing/datasheet values are OD 2.75 mm, 0.25 mm wire, 15.7 mm free length, 0.18 N/mm rate and 5 mm minimum working length. The builder said they are getting them; an order or receipt is not recorded.

**Geometry and force:** OD fits the current Ø3.3 mm pockets. Leave the seat floor and 9 mm rest / 6 mm full-travel gaps unchanged for the sample test. At those gaps, nominal pair force is approximately 2.41 N at rest, 2.67 N near the 0.71 mm Hall trip and 3.49 N at the 3 mm stop. At the stop, nominal length is 1 mm above the catalog minimum working length; tolerate as a limit to verify, not a proven coil-bind margin. The free spring is 15.7 mm and the seated gap is much shorter, so check seating, unsupported coil behavior/buckling, cap push force, return from intermediate positions and printed snap-hook retention. High force may make the nose less compliant than planned.

**CAD/BOM:** CH-066 is now SELECTED and the source spring envelope uses the actual 2.75 mm OD and 15.7 mm free-length data. The displayed model remains in its installed 9/6 mm envelope. No seat-floor redesign is made before sample measurements. Generated STEP and check reports remain stale pending the compatible pinned CAD runtime. Keep nose release gated on actual load and 3 mm stroke tests.

## D-021

**2026-09-30 · Chassis / rear floor sensor (CH-020) · SENSOR TYPE SELECTED; sourcing and physical validation open**

**Decision:** use a **bare Vishay TCRT5000 reflective sensor with its four individual leads** in the rear keel assembly. Solder the specified 350 mm AWG28 JST GH4 lead to the sensor under heat-shrink and connect it to J10-10. Do not use the Robu TCRT5000 IR Reflex Tracking Sensor Module (SKU 699619) as CH-020: it is a 5 V comparator/digital-output PCB with a different mechanical and electrical interface. D-016's no-board-in-the-keel design remains in force.

**Reason:** the bare sensor is the part envelope and pin-level interface specified by the existing keel CAD and D-016 lead assembly. The Robu module listing describes a 35 × 10 mm PCB and digital comparator output; it cannot fit the 7.6 mm sensor service pocket or connect directly to the four-wire analog/LED-drive interface.

**Procurement distinction:** the sensor type is settled, but no supplier order or receipt is recorded. The Robocraze pack-of-five listing remains a sourcing candidate; confirm that delivered parts are separate four-lead TCRT5000 packages and verify Vishay manufacturer provenance before representing them as genuine Vishay parts. A seller's generic TCRT5000 listing alone does not establish that provenance.

**Release checks remain open:** receive and measure the part, assemble and fit the sleeved lead in the real keel, then complete the documented 8/10/12 mm floor/edge, ambient-light, motor-running-noise and unplugged-fault checks. Selection does not mean the optical cliff function has passed; the nominal 10 mm floor gap remains a test risk because the datasheet's peak response is at 2.5 mm.

## D-022

**2026-09-30 · Chassis / fastener sourcing and J12/J13 stacks · CANDIDATES; supplier confirmation and fit qualification open**

**Decision:** when OnlyScrews did not show a suitable exact item, record the best next-source candidate or a supplier quote request in the canonical BOM. Do not represent a family listing or a near size as confirmed stock or a drop-in part.

**Joint stack candidates:** J12 / CH-038 uses an M3 × 12 hex-socket countersunk screw candidate, based on the modeled 4 mm deck and 8 mm tapped engagement. J13 / CH-035–037 uses M4 × 12 button-head bolts, accessible plain M4 hex nuts and the existing Ø4 × 8 dowel candidate. The modeled J13 stack is 11.2 mm, leaving 0.8 mm nominal bolt projection without washers. The BOM and [joint register](01-chassis/v1/joint-register.md) now record these choices and the needed seat, engagement, clearance, access and fit checks.

**Other source decisions:** seek DIN 7984 low-head screws from Royal Fasteners; use the Desertcart M3 × 5.7 × 4.6 insert variant only if the exact option is confirmed and coupons pass; use JCPlas B4B66/B4B67 plastic thread-formers as quote/sample candidates for M2 joints; use UAVstore's M3 × 18 button screw option as a sample candidate; and ask Royal Fasteners whether it can supply the still-unconfirmed M3 × 2.5 DIN 916 cup-point set screw. Industrybuying's Loctite 641 is the source candidate for bearing retention, separate from Loctite 222 threadlocker. Probots is the primary candidate for exact 2.5 × 100 mm cable ties, with RoboComp as a backup. CH-061 remains an OnlyScrews candidate with a marginal 0.05 mm nominal radial interference in its current pilot and requires a coupon.

**Status and limits:** source pages and stock were reviewed on 2026-09-30; availability may change. No suppliers were contacted and no fasteners ordered or received. CH-030/060 exact stock and head dimensions, CH-055's 2.5 mm availability, plastic-screw geometry/pilot, and all physical fit/proof checks remain open. No CAD geometry changed under this decision.


## D-023

**2026-09-30 · Chassis / fastener availability update · CH-035 and CH-038 reported available; CH-030/055/060 unsourced**

**Builder-reported availability:** CH-035, M4 × 12 mm hex-socket button-head SS304, is available from OnlyScrews. CH-038, M3 × 12 mm Phillips CSK mild-steel black-oxide, is available. The CH-038 product URL was not supplied, and the previously inspected OnlyScrews page showed a different SS304 item with conflicting stock text; confirm the received part's identity and countersink fit. Neither report records an order or receipt.

**Open sourcing:** the builder could not find a buyable match from the Royal Fasteners leads. CH-030 DIN 7984 M3 × 6 low head, CH-060 DIN 7984 M3 × 8 low head, and CH-055 DIN 916 M3 × 2.5 cup-point remain unsourced. No near-size substitute is approved.

**Image kit:** the pictured assortment contains M5 screws, M5 washers and M5 nuts. It does not match the chassis fastener sizes and is not needed for the listed M3/M4 joints; do not buy it for this BOM.

**Changed:** updated the BOM availability notes, chassis snapshot and fastener sourcing review. No CAD change. J12/J13 received-part fit checks remain open.


## D-024

**2026-09-30 · Chassis / remaining fastener source leads · OPEN; exact size and availability to confirm**

**New leads:** for CH-030 DIN 7984 M3 × 6 and CH-060 DIN 7984 M3 × 8, request exact standard/length and samples from ACME Fasteners through its [TradeIndia low-head socket screw listing](https://www.tradeindia.com/products/low-head-socket-cap-screw-din-7984-or-din-6912-5649111.html). The page is marked in stock and says samples are available, but it does not show the exact M3 lengths or clarify whether its inventory is DIN 7984 versus DIN 6912. Confirm dimensions and standard before treating it as a match.

For CH-055 DIN 916 / ISO 4029 M3 × 2.5 cup-point, [Dalloyed Fasteners](https://www.dalloyedfasteners.com/grub-screw.html) is an Indian manufacturer lead for the ISO 4029/DIN 916 family and M3 grub screws. Its published page does not list a buyable M3 × 2.5 item; ask whether it can supply this short length and provide a sample. The M3 × 3 OnlyScrews item remains an unapproved alternate because it is 0.5 mm longer.

**Changed:** BOM and sourcing review now record the new supplier leads. No supplier was contacted and no purchase or physical fit is recorded. The three exact fastener rows remain open pending source confirmation and received-part fit.

## D-025

**2026-09-30 · Chassis / mixed Phillips-CSK fastener assortment · CANDIDATE; source and fit unverified**

**Correction:** the later assortment image contains M3, M4 and M5 Phillips countersunk screws, plus matching M3/M4/M5 nuts and washers; it is not an M5-only kit. The M3 × 12 compartment is a possible source for CH-038, pending seller confirmation of material/grade and measured countersink dimensions. The M4 × 12 compartment is countersunk and does not replace the selected M4 × 12 button-head candidate for CH-035. The earlier separate image was an M5 button-head assortment and does not match the chassis fastener sizes.

**Changed:** clarified the chassis BOM and fastener sourcing review. No kit link, purchase, receipt or fit check is recorded.

## D-026

**2026-09-30 · Chassis / battery and ballast CAD (CH-022, CH-038, J12) · ACTIVE; PCB-01 height and received-part fit open**

**Why:** an audit found the CAD out of step with the BOM. The two 25R cells were 0.2 mm apart, but the BOM notes Samsung asks for more than 1 mm. CH-038 is a countersunk screw, but the CAD modeled a cylinder head in a flat counterbore. The TCRT mass note said ~300 mm, but CH-020 specifies a 350 mm lead. `chassis-v1.step` also predated the latest source edits.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Cells:** `BATTERY_CELL_PITCH` went from 18.6 to 19.5 mm, giving a 1.1 mm gap at the 18.4 mm maximum cell diameter. The pack envelope grows to 38.5 × 67.0 × 23.5 mm. The tub front wall stays at X 67, so the rear wall moves 0.9 mm back to X 24.0 and the pack centre to X 46.25. The hatch, deck opening and shell floor opening follow from the same constants.
- **CH-038 / J12:** the ISO 7046-1 M3 × 12 head is modeled as a 90° cone to the Ø5.5 rim with k 1.65. It sits in a 90° deck countersink, Ø6.5 at the deck top, 0.1 mm below flush. The bar's tapped holes deepen from 8 to 9 mm, giving 8.1 mm engagement with 0.9 mm tip clearance; before, the tip reached the hole floor. The screw mass now comes from the modeled head.
- **TCRT mass note** now says 350 mm (CH-020). The mass is unchanged.

**Mass register:** the ballast row went from 81.6 to 81.1 g (lighter CSK heads, deeper holes). The battery row centroid moves −0.45 mm in X. Total mass went from 2605.5 to 2605.0 g and CoM X from +19.05 to +19.03 mm (h 105.87 mm). a_tip is 1.763 m/s², against a 1.582 minimum. Measured printed-volume changes (hatch +126, tub walls +52, front deck −134, shell −162 mm³) come to less than 0.2 g, so those rows were not edited.

**Checks:** the new `cad/check_battery_ballast.py` (about 10 min) passes all ten rows and writes `generated/battery-ballast-checks.json`. Those rows cover pack clashes, cell gap, tub margins (1.8 mm front/rear, 1.5 mm side), ballast clashes, head seat, screw length, tip clearance and the CoM margin line. It reports four overlaps as OPEN. They are identical, or differ only by the lengthened hatch, in a copy of the model with this change reversed:
- **Hatch flange × shell floor:** 1689 mm³ (1665 mm³ before). The flange is wider than the shell opening. This is a real, unresolved interface issue that the Sep 27 saved report does not show.
- **Front deck × shell:** 39 mm³.
- **Front deck × power-board proposal envelopes:** 178 mm³.
- **Front deck × IMU screws:** 25 mm³, by design.

The full `check_layout.py` was not rerun. `chassis-v1.step` was rebuilt from the current source. Its product list also reflects earlier source changes: the DRV8833 and GP2Y0A21 envelopes and the Ø3 × 1.5 magnet.

**Changed docs:** the chassis BOM battery note, the CH-022 and CH-038 rows in `BOM.csv`, joint-register J12 and the CAD README.

**Open:** the PCB-01 height is still a 2.9 mm placeholder, pending measurement. The pack build must hold the 1.1 mm cell gap. The received CH-038 head angle and diameter must be checked against the seat. The hatch/shell interface is unresolved. A full `check_layout.py` rerun is needed before release.

## D-027

**2026-09-30 · Chassis / purchased-part models (CH-017, CH-018; J08A, J08C) · ACTIVE; received-unit fit open**

**Why:** the builder asked why the Adafruit driver was only a box, and for other boxed modules to be found and fixed. Two purchased modules in the chassis v1 export were boxes: the Adafruit #3297 driver and the GP2Y0A21YK0F.

**Sources** (details in [purchased/README.md](01-chassis/v1/cad/purchased/README.md)):
- **step.parts:** has neither part (searched 2026-09-30).
- **Sharp:** a community STEP of the A21 sits byte-identical in two unrelated GitHub repositories. It matches the Sharp datasheet outline (E4-A00201EN) to 0.05 mm.
- **Adafruit:** no STEP exists. `purchased/adafruit_3297_drv8833.py` builds one from Adafruit's own Eagle board file: outline, corner radii, holes and part placements. Package bodies are nominal, and the terminal-block height is estimated.

**What the real sensor showed:** the model had the package wrong, and Layout 02 had it wrong with the A41 STEP too. It read the connector as the lens face, so the A41 in Layout 02 was looking upward.
- The lenses and the Ø3.2 ear holes face the same way.
- The package is 13.5 mm deep along the optical axis, and 18.9 mm tall because the connector sits on one edge.
- The ears span 44.5 mm, but the pod is 35 mm wide.

**Builder decisions (2026-09-30):** trim both ears to the 29.5 mm body and clamp the body between seat and lid. Solder the J10-8 wires to the S3B-PH pins, with no plug.

**Changed in CAD (`body_chassis_model.py`):**
- **Sensor:** the STEP (ears trimmed in the model) sits lenses +X, connector up, face at X 128, on the Z 35 seat. The optical axis moves from Z 40.3 to Z 41.5 (lens 6.5 above the body bottom), and the window follows.
- **Pod:** the nose top rises from Z 49 to Z 51. The lid underside is level at Z 49 all the way to the face, replacing the step down over a "lens hood". The front pocket is ±15.0, up from ±14.0. The lid screw moves to (111.8, −11.8), behind the sensor, from (124.6, −11.8), which was inside the real sensor.
- **Lid hump:** the lid has a hump over the header and a 3 mm soldered-lead reserve, 1.2 mm walls, top at Z 58.6. It runs 11.5 mm rearward so the D-011 11 mm forward slide still works, and it gives the lead a path back and down behind the sensor.
- **Cap:** the cap has a top notch so the hump clears its 3 mm travel. The ear slots stay, now vestigial.
- **Drivers:** the #3297 boards lie flat at Z 66 with their long side along X and the terminal block forward, 10.1 mm tall. They are centred 1.5 mm further back, at X 44.5. The real PCB corner otherwise reaches 0.7 mm into the front body-mount doglegs; the old box overlapped them by about 20 mm³.

**Mass:** the nose row goes from 18.7 to 18.9 g (measured pod/lid/cap volume +0.27 cm³). The driver row moves to X 44.5. The register total is 2605.2 g, with CoM (+19.03, 0.16, 105.86) and a_tip 1.763 m/s² against 1.582.

**Checks:**
- `check_nose_joints.py`: all 12 rows pass.
- Nose clash sweep: pod, lid, sensor, cap at rest and at 3 mm, against the body, frame, electronics and harness. Only the designed insert interference shows, and the optical axis is unobstructed. The sensor has 0.5 mm to the lid and 0.5 mm to the cap at full travel.
- Driver sweep: no clashes, 0.8 mm to the dogleg.
- `check_nose_service.py` subset C: cap, lid, sensor and lid-screw paths are clear.
  - `hall_board_up` now needs the sensor removed first (the sweep was updated); the old order hit the sensor at 3 mm.
  - The subset run overwrote the full report, so I restored the committed full report and merged the rerun rows (§) into it.
- `chassis-v1.step` rebuilt. The full `check_layout.py` was not rerun.

**Changed docs:** `purchased/` with its README, the CH-018 row in `BOM.csv`, the chassis BOM A21 note, joint-register J08A/J08C (J08A still named the A41), the CAD README and `check_layout.py` labels.

**Still boxes:** the PCB-01 protection module has no drawing or model and an unmeasured height. The custom boards (PCB-07, the Hall carrier, the power-board proposals) are the project's own designs.

**Open:** check the received A21 and #3297 against the STEPs; ear-trim quality; soldered-lead strain relief; hump and cap-notch print and dust ingress; bench-check the stop-path timing (unchanged).

## D-028

**2026-10-01 · Chassis / battery tub interfaces (J11A, CN-05) · ACTIVE; boss and insert fit unproven**

**Why:** `check_battery_ballast.py` (D-026) reported four overlaps as OPEN. The builder asked for the hatch, deck and power-envelope overlaps to be fixed, and the IMU one recorded as accepted.

**Root causes:**
- **Hatch × shell (1689 mm³):** the hatch lies inside the shell floor's thickness (Z 30.5–32.0 in a Z 30.0–32.4 floor). The floor opening was the tub plus 1 mm, but the hatch flange is wider, so its screw holes sat in shell material.
- **Front deck × shell (39 mm³):** four 0.4 mm slivers where the tub screw bosses (from Z 32) entered the shell floor outside the opening.
- **Front deck × power envelopes (178 mm³):** the CN-05 fuse-holder and disconnect-pair envelopes share the 11.3 mm channel between the tub's +Y wall and the rail with the +Y bosses. Neither envelope can move sideways. Raising the fuse would hit body-mount nut 4 (Z 48.8).
- **Front deck × IMU (25.133 mm³):** exactly the two M2 shanks, 4 mm into the deck (2·π·1²·4), by design.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Shell opening:** now the hatch outline plus `BATTERY_HATCH_GAP` 0.5 mm, from new `BATTERY_HATCH_X` / `BATTERY_HATCH_HALF_Y` constants shared with the hatch.
- **Bosses:** one constant, `TUB_BOSS_XY`, now used by both the tub and the front deck print. The rear pair stays at (28, ±39.5). The front pair moves from (64, ±39.5) onto the front wall's face at (71.5, ±34.35), midway between the ballast bar (|Y| 30) and the fuse holder (Y 38.7). All four stop at `TUB_BOSS_TOP_Z` 39.5, 1 mm over the unchanged Ø4.3 × 7 insert pilots (was Z 41).
- **Hatch:** grows forward from X 71 to X 75 to carry the front screws, leaving 3.5 mm to the edge (M3 washer radius). Its Y extent is unchanged.
- **Pack interface (CN-05):** the disconnect pair, its tub-wall service window and slide path move from Z 37–47 to Z 40–50, clear of the rear +Y boss. The fuse holder is unchanged.

**Mass register (measured against the committed model):** shell −4.04 cm³, so `BODY_SHELL_AND_PANELS` goes from 290.4 to 285.6 g. Frame +0.29 cm³ at 0.571 g/cm³, so `CHASSIS_PRIMARY_FRAME` goes from 206.8 to 207.0 g. The register total is 2600.6 g, CoM (+19.03, 0.16, 105.88), a_tip 1.763 m/s² against 1.582.

**Checks:**
- `check_battery_ballast.py`: all ten rows pass with no OPEN overlaps. The IMU overlap is in a new ACCEPTED list and passes only at 25.133 mm³. Hatch/shell or deck/shell overlaps now fail instead of being reported.
- Pack-interface sweep (pair, fuse, slide path against the whole model): no clashes. The window still opens through the wall.
- `chassis-v1.step` and `body-chassis.step` rebuilt.
- Full `check_layout.py`: 116 of 119 rows pass, in 14 min. All the tub, hatch, ballast, pack-disconnect and IMU rows pass. The window reads Z 40–50. The three failures are listed under **Found, not changed**.
- **`check_layout.py` repaired so it completes** (first full run since Sep 27). Under the substitute runtime (OCC 7.9.3), whole-compound booleans against the C3/DevKitC compound ran away: the J33/J34 reserve reached 133 GB and macOS killed the run at about 37 min, twice.
  - `_boxes_meet` now also needs a leaf of each compound to meet. That only drops pairs whose overlap must be zero.
  - The C3 carrier's own plug reserves are skipped against the C3 compound before the boolean; their results were already discarded.
  - The IMU deck row picked the first `CHASSIS_DECK_WITH_BODY_INTERFACE`, which since the frame split is the rear print. It now picks the print the IMU screws are in, and reads 12.566 mm³ per shank.

**Found, not changed** (the three failing `check_layout.py` rows, all outside this change and likely from D-027):
- `connector_reserves_clear_of_real_hardware`: the PCB-03 J31/J32 and J33/J34 edge-connector reserves overlap the #3297 driver boards by 140 mm³ each.
- `connector_bodies_clear_of_hardware_and_each_other`: the J3_1 and J3_4 mated Micro-Fit plugs overlap the driver boards by 82 and 89 mm³.
- `front_panel_lifts_off_forward`: the front panel's removal path hits `BALL_POD` by 171 mm³, which points to the D-027 nose rework (nose top Z 49 to 51).

**Changed docs and scripts:** the CAD README, joint-register J11A, `check_battery_ballast.py`, `check_layout.py`, and the regenerated `generated/checks.md` and `checks.json`.

**Open:** boss print quality with a 1 mm roof over the inserts; front-boss access with the ballast bar fitted; the J11A screw and insert BOM rows (unchanged); the three D-027 `check_layout.py` failures above.

## D-030

**2026-10-01 · Chassis / frame fasteners, pack restraint and driver mounts (J05, J06, J11A, J11B, J12, J13, J15B, J16; CH-011, CH-030, CH-038, CH-055, CH-060) · ACTIVE; coupons, strap/foam source and physical tests open**

**Why:** the joint register still had open items: J05/J06 crossmembers and J16 deck-to-rail; J11A hatch screws and inserts with no BOM IDs and CH-011 OPEN; no J11B pack restraint; the J12 ballast screw, J13 clamp stack, and J15B board mounts and cable restraint; and CH-030, CH-055 and CH-060 with no exact source. The builder chose (2026-10-01):
- CAD, BOM and docs together;
- standard stocked screws in place of the three odd sizes;
- the pack strapped to the hatch;
- printed posts for the drivers.

D-029 is reserved by a parallel session (lid hump), so this is D-030.

**Found:** the J05/J06 receivers could not be assembled. Each rail's Ø4.3 insert pilot sat behind a Ø3.4 bore through the tongue, so the insert could not be pressed in. The J16 screws at (70, ±54) and (−25, ±58.5) sat under the body M4 feet. On the #3297 boards, the plated holes lie along one long edge. The left board's holes were over the battery opening, and the right board's were on a body foot.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **One frame insert:** M3 × 6, OD 4.4, in a Ø4.3 pilot with a Ø3.4 tip relief: CH-077, the same article as CH-061. Button heads seat straight on the printed faces, with no washers.
- **J05/J06:** the inserts are pressed into the rail tongues' end faces. The tongues widen from ±3.2 to ±4.0 (1.85 mm of wall round the insert), and the pockets to ±4.2. The rear rail ends widen to X −23.
  - J05: ISO 7380 M3 × 16 from X +92 (CH-073);
  - J06: ISO 7380 M3 × 20 from X −48 (CH-074);
  - both have 6 mm of thread.
- **J16:** ISO 7380 M3 × 10 (CH-075) into inserts flush with the rail tops, 6 mm of thread. The axes are (30, ±54), (77.5, ±54) and (−27.5, ±61), each with a deck ear. Off the body feet, the heads clear by 0.65 and 1.15 mm.
- **J11A:** ISO 7380 M3 × 6 (CH-076) through the hatch into boss inserts, 4.5 mm of thread. CH-011 becomes DESIGN.
- **J11B:** two 10 × 1.2 mm hook-and-loop straps (CH-078) at Y ±29 loop under the hatch, through four hatch slots and over the cell tops, clear of the BMS. Two 1.5 mm foam pads (CH-079) sit on the Y-end walls; the +Y pad stops short of the service window. Pack and hatch drop out together.
- **J15B:** the left board is turned 180° (terminal block now rearward) so both sets of holes are outboard. Both boards move 5 mm back to X 39.5. They sit on four Ø7 × 10 posts on the front deck with M2.5 × 4 inserts (CH-080) and M2.5 × 6 screws (CH-081). A tie bridge on each side at X 19–24 takes a motor-lead tie (CH-082). The `HARNESS_MOTOR_BRANCH` reserve moves to run between the posts.
- **J01/J04:** DIN 7984 low heads become ISO 7380 button heads of the same length and key (CH-030, CH-060). The J04 recess goes from R2.9 to R2.95 for the Ø5.7 head.
- **CH-055:** M3 × 2.5 is not a standard ISO 4029 length. The builder approved a stocked M3 × 3 faced down 0.5 mm at the hex end, so the model stays at 2.5.
  - An unmodified M3 × 3 swept only **1.07 mm** past the face-screw heads (rule ≥ 1.5).
  - Faced to 2.5 it sweeps **1.54 mm** (the old DIN heads gave 1.56).
  - A plate-recess and housing-cavity enlargement tried for the M3 × 3 was reverted.
- **J12:** the CH-038 source is the OnlyScrews M3 × 12 Phillips CSK, mild steel, black oxide, matching the builder's report. No geometry change.
- **J13:** the stack stays M4 × 12, plain nut, no washer, leaving 0.8 mm past the nut. Loctite 222 (CH-057) on the nut is the locking method. No geometry change.

**Mass register:**
- `CHASSIS_PRIMARY_FRAME` goes from 207.0 to 229.1 g at (18.14, 0, 46.64):
  - +21.4 g of new hardware, measured from the solids;
  - +0.7 g for the measured +1.24 cm³ of printed volume.
- New `BATTERY_RESTRAINT` row: 3.4 g.
- The driver row follows `DRIVER_CENTER_X` to X 39.5.
- The total goes from 2600.6 to **2626.1 g**, CoM (+19.15, 0.16, 105.30).

**Checks:**
- New `cad/check_frame_fasteners.py` (about 20 min): all nine rows pass. It writes `generated/frame-fastener-checks.json`.
  - No clashes between the changed or new solids and the whole model. The only overlaps are the designed ones already recorded: insert knurls, motor-face threads and IMU shanks.
  - Thread engagement: M3 ≥ 4.5 mm, M2.5 4 mm.
  - Every insert can be pressed in from a free face.
  - The set screw clears by ≥ 1.5 mm, turned about the axle in 3° steps.
  - Heads sit on their seats; the boards sit on their posts.
  - Straps and foam touch the pack without overlap; the pack cartridge drops 60 mm clear.
- `wheel/check_wheel_on_chassis.py`: 6 of 6 rows pass (16 min). Its swept-ring envelope put the set screw 1.378 mm from the button heads. That ring puts the screw's maximum radius along its whole length, so the set screw is now swept by rotation, as above.
- `check_battery_ballast.py`: all ten rows pass. The straps and foam add no overlaps. a_tip is 1.784 m/s², against a 1.582 minimum (was 1.763).
- `chassis-v1.step` rebuilt. The full `check_layout.py` was not rerun; its set-screw label and harness note were updated.

**Changed docs:** the joint register (J01, J03, J04, J05, J06, J11A, J11B, J12, J13, J15B, J16, release actions), `BOM.csv`, the chassis `BOM.md`, the CAD and frame-split READMEs, `research/axle-stack.md` and the engineering checklist.
- `BOM.csv` rows: CH-011, CH-030, CH-036, CH-038, CH-055, CH-057 and CH-060 updated; CH-073 to CH-082 added.
- The CH-030, CH-035 and CH-038 rows had unquoted commas that spilled into extra columns; they are repaired.

**Open:**
- coupons: tongue inserts (1.85 mm walls), tub-boss inserts (1.35 mm walls), driver posts;
- strap and foam source; strap ≤ 1.5 mm thick; pack shock/inversion test;
- facing the M3 × 3 set screws (cup intact, hex depth for the 1.5 mm key);
- M2.5 head diameter;
- tool access with the body on and lifted;
- the driver move against the PCB-03 connector reserves that D-028 found failing in `check_layout.py`.

## D-029

**2026-10-01 · Chassis / nose lid (J08) · ACTIVE; lead bend to confirm at assembly**

**Why:** `check_layout.py` row `front_panel_lifts_off_forward` failed after D-027. The lid's lead hump reached Z 58.6, but the front panel's bottom edge is Z 58.0, and the panel slides forward over the nose to come off (171 mm³ against `BALL_POD`).

**Changed:** `FRONT_RANGE_LEAD_RESERVE_H` goes from 3.0 to 2.0 mm, so the hump top drops from Z 58.6 to Z 57.6, 0.4 mm under the panel's path. The 3.0 mm was a D-027 modelling allowance, not a builder decision. 2.0 mm still leaves room for a 90° bend in the AWG30 J10-8 lead (about 0.5 mm OD) at the solder joint. The cap's top notch follows the hump. The lid loses 0.077 cm³ (about 0.04 g), so the nose mass row is unchanged.

**Checks:** `check_nose_joints.py` 12/12; `front_panel_lifts_off_forward` passes in the full `check_layout.py` (see D-031).

**Changed docs:** joint-register J08 lid note.

**Open:** confirm the soldered lead bends within 2 mm above the S3B-PH pins.

## D-031

**2026-10-02 · Chassis / driver boards (J15B), inline motor pairs, motor face screws · ACTIVE; supersedes the D-030 J15B layout**

**Why:** the full `check_layout.py` failed four rows after D-030:
- **Driver boards:** the #3297 boards overlapped the PCB-03 J31–J34 edge-connector reserves (up to 598 mm³) and the mated Micro-Fit+ plugs (up to 328 mm³). With the long side along X, a board needs 25.4 mm, but only 21 mm is free between the plugs (X 37) and the body-mount doglegs (X 58). D-030's 5 mm rearward move made it worse, and its posts and M2.5 screws also sat in the plug reserves.
- **`rotating_screws_swept_clear`:** the axle set screw passed 1.4 mm from the motor face-screw head, against a 1.5 mm minimum. The model drew the D-030 ISO 7380 head as a full-radius cylinder.
- **IMU row:** it read the deck top from the deck's bounding box, which the D-030 driver posts now raise to Z 66.

**Changed in `01-chassis/v1/cad/body_chassis_model.py`:**
- **Driver boards (J15B):** both turned 180° from the STEP, long side along Y, at X 38.5–56.3, |Y| 31.3–56.9 (`DRIVER_CENTER_X` 47.4, `DRIVER_Y` 44.2). The hole edge faces rearward on both. The terminal block is inboard on the left board and outboard on the right. The four D-030 posts, inserts and screws move to (41.05, ±34.04) and (41.05, ±54.36): through the plated holes (checked), 0.5 mm off the PCB-03 edge and behind the body M4 feet (X 54, which rule out front-edge posts).
- **Inline motor pairs:** the reserves are now set per side (`MOTOR_INLINE_RESERVE`). The left pair stays along X over its board, raised 0.6 mm to clear the M2.5 heads (Z 69.1). The right pair stands along Y at X 50.9–57.9, between the outboard terminal block (0.4 mm) and the dogleg.
- **Motor-lead harness branch:** narrows to 7 mm and runs across the deck at X 30–37, behind the posts and clear of the IMU.
- **Motor face screws:** the heads are modelled as an ISO 7380 spherical cap (dk 5.7, k 1.65) instead of a cylinder. The set-screw sweep clears again.
- **Mass register:** the driver row follows `DRIVER_CENTER_X`. Total 2626.1 g, CoM (+19.17, 0.16, 105.30), a_tip 1.786 m/s² against 1.582.

**Changed in `check_layout.py`:** the IMU row takes the deck top from `DECK_Z + 2`.

**Checks:**
- Full `check_layout.py`: **119/119 pass** (16 min).
- `check_frame_fasteners.py`: 9/9. `check_battery_ballast.py`: all pass. `check_nose_joints.py`: 12/12.
- Driver sweep (boards, posts, inserts, screws, harness branch and inline pairs against the whole model): no clashes. The closest gaps are 0.4 mm (right terminal block to its inline reserve) and 0.5 mm (inner posts to PCB-03).
- `chassis-v1.step` and `body-chassis.step` rebuilt.

**Changed docs:** joint-register J15B.

**Open:** post coupon (unchanged from D-030); the right board's outboard terminal block needs a lead path to its inline pair; confirm board hole positions on a received board; tug and vibration tests (D-030).

## D-032

**2026-10-02 · Chassis / main fuse holder (CH-028, CH-029) · ACTIVE; CH-028 stays HOLD for an India source**

**Why:** CH-028 was HOLD because the CAD (an envelope in the +Y channel beside the tub) and the BOM note (a PCB-mount holder on PCB-02) disagreed. `RP-02-electrical/board-specs.md` places the pack interface tile **beside the battery tub** (or on PCB-03's front edge) and requires the main fuse to be source-adjacent (PA-02). PCB-02 is on the rear panel, about 100 mm from the pack, so it is ruled out. The builder chose an inline holder beside the tub.

**Found:** the D-028 channel envelope (24 × 10 × 10 mm) could never hold an ATO fuse. The fuse alone is 19.1 × 5.1 × 18.8 mm with its blades. The channel is 11.3 × 19.6 mm, so no ATO holder fits there in any orientation. A free-space search for the holder (30 × 10 × 26 mm, all six orientations, 0.5 mm clearance) found room only above the deck. The builder chose the spot above the +Y channel, on a deck bracket.

**Changed in `body_chassis_model.py`:**
- **Holder:** `PACK_FUSE_HOLDER_BOX` is now the Littelfuse 0FHA0001ZXJ inline ATO holder (16 AWG leads, 20 A at 32 VDC, 30 × 10 × 26 mm with the fuse, per the Littelfuse catalog). It sits at X 52–82, Y 39–49, Z 73–99: wire axis along X, fuse loading from the top, about 25 mm above the disconnect pair.
- **Bracket:** on the front deck print, a 6 × 8 mm column at X 75–81 (in front of the body M4 foot, 1.0 mm clear) and a 2 mm shelf under the holder (`FUSE_BRACKET_COLUMN`, `FUSE_BRACKET_SHELF`).
- **Bosses:** the front tub bosses no longer take their Y from the fuse box. It is fixed at 34.35 (unchanged).
- **Mass register:** frame +0.8 g (bracket 1.32 cm³ at 0.571 g/cm³), now 229.9 g. The pack-interface row follows the holder box. Total 2626.9 g, CoM (+19.19, 0.17, 105.43), a_tip 1.786 m/s² against 1.582.

**Changed in `check_layout.py`:** in the power running-gap sweep, the holder's contact with its own bracket shelf counts as mounted, like the E-stop on its well.

**Checks:**
- Full `check_layout.py`: 119/119.
- `check_battery_ballast.py`: all pass. `check_frame_fasteners.py`: 9/9.
- Holder and bracket sweep against the whole model: no clashes; 0.5 mm to the left inline motor-pair reserve, 1.0 mm from the column to the M4 foot.
- STEPs rebuilt.

**Changed docs:** `BOM.csv` CH-028 row, the chassis `BOM.md` fuse paragraph, the CAD README.

**Open:** an India source for 0FHA0001ZXJ or an equivalent inline ATO holder; check the received body against the envelope; confirm 16 AWG leads for the 15 A fuse; how the holder is tied to the shelf; bracket print. Fuse access needs the body off.

## D-033

**2026-10-02 · Chassis / frame print units and hub cap (CH-001, CH-012, CH-058, CH-059, CH-073–CH-075, CH-077; J03, J05, J06, J16) · ACTIVE; HOLD on printer/orientation review, junction coupons and a cap retention test**

**Decision:** the builder asked to implement the fastener review. Two of its recommendations are adopted:

- **Frame modules.** Each end of the frame is one print: deck, both rails and crossmember. J05, J06 and J16 are deleted, with their ten M3 screws (CH-073, CH-074, CH-075) and ten of the fourteen CH-077 inserts. The two modules join only through the two J04 carriers, which stay removable.
- **Hub cap.** One central ISO 7380 M3 × 10 per cap, into a tapped hole in the steel stub's spigot end, replaces the six M2 × 6 thread-forming screws (CH-059 goes from 12 to 2).

The review's other proposals are not adopted here. They need physical evidence first: a screwless nose lid, stretch-fit tyres or fewer ring screws, integrated carriers, a two-screw keel, and a hinged hatch. Everything else keeps its hardware.

**Why:**

- The frame split had no printer or service reason. The frame-split study kept the rails and crossmembers separate only so their joints could be reviewed. No service step removes a rail from its deck or crossmember.
- The split was also defective. `frame_deck("REAR")` was three solids: its two J16 screw pads sat 1.00 mm off the deck plate, so the rear J16 screws clamped detached pads onto the rails, not the deck.
- The J05/J06 tongues carried inserts in 1.85 mm walls, an open coupon risk. Fusing removes them.
- The six cap screws only retain a cosmetic cover. One screw keeps the cap removable for wheel service.

**CAD changed:**

- [`body_chassis_model.py`](01-chassis/v1/cad/body_chassis_model.py):
  - New `frame_module(region)` gives `CHASSIS_FRAME_FRONT_MODULE` and `CHASSIS_FRAME_REAR_MODULE`. They replace the labels `CHASSIS_RAIL_*`, `FRONT_CROSSMEMBER`, `REAR_SKID_CROSSMEMBER` and `CHASSIS_DECK_WITH_BODY_INTERFACE`.
  - The tongues, pockets, J05/J06/J16 screw and insert bores, the J16 deck ears and the J05/J06/J16 hardware are removed, along with their constants.
  - Where the deck covers a crossmember, the crossmember rises to the deck underside (`FRAME_MODULE_FILLS`): front Z 51 → 52, rear Z 48 → 52 at X −41 to −32. The J10-8 cable bore is recut through the front fill.
  - The rear rails keep their widened end as a gusset into the crossmember.
  - J04 receivers, keys, body-nut socket paths, tub, bosses, posts, the D-032 fuse bracket, pod inserts, keel inserts and the cable-tie lug are unchanged.
  - Stub: `STUB_CAP_TAP` adds an M3 tapped hole in the spigot end, 8 mm of thread and a 9.5 mm drill, which leaves 4.5 mm of steel to the D-shaft bore. `_check_wheel_interface()` now also checks the tap.
- [`wheel/wheel_model.py`](01-chassis/v1/cad/wheel/wheel_model.py):
  - The cap has a central Ø3.4 hole and a Ø6.2 counterbore. The head sits 0.25 mm under the boss top, so the robot is 202.0 mm wide (was 202.6).
  - A Ø9 column under the head stops 0.65 mm inside the wheel-screw heads and 0.6 mm above the spigot tip.
  - Two Ø1.8 × 1.5 mm pegs at R12.2 (30°/210°) sit in Ø2.1 × 1.8 mm hub holes and clock the cap. The six M2 pilots are gone.
- `frame-split.step.py` now shows the two modules and the hatch.

**Counts:** screws 90 → **70** (−10 frame, −12 M2 cap screws, +2 central cap screws), inserts 55 → **45**. Frame prints 11 → 5: two modules, two carriers, the hatch.

**Mass register:**
- `CHASSIS_PRIMARY_FRAME` goes from 229.9 to **219.1 g**, CoM (17.71, 0.15, 46.73):
  - −10.7 g for the ten screws and −3.8 g for the ten inserts, measured from the solids at 7.9/8.5 g/cm³;
  - +3.7 g for the measured +6.52 cm³ of printed volume at 0.571 g/cm³ (fills, filled bores and pockets).
- `AXLE_BEARINGS_AND_STUB_SHAFTS` goes from 51.4 to 50.4 g, for the two tapped holes.
- `WHEEL_L/R` stays at 92.5 g: `check_wheel.py` gives 92.5 g with the M3 × 10 in place of six M2 × 6.
- Register total 2626.9 → **2615.1 g**, CoM (+19.15, 0.17, 105.69); a_tip 1.778 m/s² against the 1.582 minimum.

**Checks (2026-10-02):**
- `check_frame_fasteners.py`: **9/9**. The new row `frame_modules_are_single_prints` replaces `tongue_fit`: each module is one solid (front 75.84 cm³, 75 × 128 × 41 mm; rear 50.37 cm³, 34 × 132 × 22 mm), no J05/J06/J16 hardware or split part remains, and the rear deck plate fills both rear-rail probes. No new clashes; the accepted overlaps are the existing insert knurls, motor-face threads and IMU shanks, now against the module labels. The run used the patched model before the mass rows changed; the rows do not affect geometry.
- `check_nose_joints.py` 12/12, `check_rear_keel.py` 21/21, `check_battery_ballast.py` all pass (no new tub clashes with the fused front module).
- `wheel/check_wheel.py` **25/25**. New rows: cap-screw engagement in the stub (6.9 mm), head seated and recessed (0.25 mm), column clearances (0.65 mm to the wheel-screw heads, 0.6 mm to the spigot), and pegs in the hub holes (1.38 mm wall to the hex). The pocket keep-out row now excludes the cap screw, which runs into the stub on the axle line, like the wheel screws.
- `wheel/check_wheel_on_chassis.py` **6/6**. The central screw sweeps 3.67 mm clear of the bearing cap and meets the tapped stub with no overlap.
- `check_layout.py` full run: **119/119 pass** (~4.6 min). The first run failed only `rotating_screws_swept_clear`, whose expected screw count still assumed six cap screws per wheel. Every gap passed (minimum 1.64 mm against 1.5 mm; the cap screw is 3.67 mm clear). The count is now `2 × (1 + 3 + 6 + 1)`. The updated frame label lookups (crossmembers, nose inserts, fuse holder, IMU deck) are exercised and pass. Chassis front is now X 92.0 (was 93.65) because the J16 ears are gone.
- `chassis-v1.step`, `frame-split.step`, `wheel.step`, `wheel-pair.step` and the local `body-chassis.step` rebuilt; `write_outputs.py` reports regenerated. Those reports also pick up earlier stale values (688 ZZ positions, the A21 sensor and the battery X).

**Changed docs:** joint register (J03, J05, J06, J16, summary, release actions), chassis `BOM.md`, `BOM.csv`, the CAD, wheel and frame-split READMEs, the engineering checklist and the fastener review's status line.

**BOM changed:**
- CH-001 is re-specified as two frame modules, two carriers, the tub and the hatch.
- CH-012 gains the spigot-end tap.
- CH-058 and CH-059 are re-specified: CH-059 is ISO 7380 M3 × 10, 2 each.
- CH-077 goes from 14 to 4 (J11A only).
- CH-073, CH-074 and CH-075 are retired; do not reuse the IDs.

**Open:**
- Printer and orientation review for each module. The front module has features above and below the deck (driver posts and fuse bracket above; rails and tub below). The rear module prints deck-down.
- Junction coupons: rail-to-crossmember and crossmember-to-deck under caster and skid loads.
- Deck coplanarity across the motor bay through the J04 carriers.
- Cap retention and peg fit on a coupon. Tapped-hole depth on the stub drawing.
- Physical retention of the remaining joints, as before.

## D-034

**2026-10-03 · Body / audio speaker (BO-001; BO-002–BO-006 registered) · ACTIVE; speaker SELECTED, not ordered; HOLD on received-part measurement and bench listen**

**Decision:** the builder locked the body speaker as the **Visaton K 50 WP – 8 Ω (art. 2915)**, bought from [element14 India, order code 1683894](https://in.element14.com/visaton/2915/speaker-k-50-wp-8-ohms/dp/1683894). The body audio chain from the RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2 is entered in the project BOM as BO-001 to BO-006. Only the speaker is selected. The amplifier, front end, mic boards and cables stay `CANDIDATE` or `HOLD`.

**Why:**

- It is the driver the CAD already carries: Ø50 × 18 mm, Ø46 cutout, 48 g, behind the front-panel grille with a sealed Ø54 back cavity (X 77–92.5). No geometry or mass change.
- 8 Ω and 2 W rated / 3 W max match the MAX98357A on the 5 V `PB-AUDIO-OUT` branch (1.75 W, about 0.7 A peak, under the 2.0 A e-fuse).
- Of the 50 mm Visaton drivers it has the widest range (180 Hz–17 kHz, fs 300 Hz) and the lowest price seen (about €5.74 in the EU).
- Alternatives compared on 2026-10-03:
  - **K 50 (2901, metal basket):** 250 Hz–10 kHz, fs 400–500 Hz, and it cost more. Kept as the fallback if 2915 is unavailable.
  - **K 28 GI (2830):** 0.5 W, 450–7000 Hz, fs 730 Hz. Too quiet and thin as the only speaker, and the MAX98357A could overdrive it.
  - **Local generic 50 mm 8 Ω (for example Robomart, ₹174):** cheaper, but with no datasheet, so depth and resonance are unknown until measured. Most local "2-inch full-range" units are Ø52–55 mm and 25–45 mm deep, too big for the front cup and cavity.

**BOM changed:** [`BOM.csv`](BOM.csv) gains the `body` owner and rows BO-001 to BO-006: the speaker (`SELECTED`), PCB-05, the MAX98357A, 2 × ADAU7002, 4 × PCB-06 mic boards with IM73D122V01, and the W12/W26–W28 audio cable set. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) is the body v1 snapshot.

**CAD:** no change. `body_v1_model.py` already models the K 50 WP outline (`SPEAKER_*`), and the `BODY_AUDIO` mass row (60 g) already counts it at 48 g.

**Unverified:**

- element14 India price and stock for 1683894 were not read; check them at order.
- Received outline, depth and mass against Ø50 × 18 mm and 48 g.
- Low-end response in the 15.5 mm sealed cavity, and speaker-to-mic coupling (RP-05 `AR-60`).
- Flange bond and grille seal method.

**Next:** order BO-001 with a MAX98357A bench breakout. Caliper and weigh the speaker, update `BODY_AUDIO`, and bench-listen to the character cues and a music clip at a capped gain.

## D-035

**2026-10-03 · Body / audio bench amplifier (BO-007) · ACTIVE; SELECTED, not ordered; bench only**

**Decision:** the builder selected the [SmartElex MAX98357A I²S breakout from Robocraze](https://robocraze.com/products/smartelex-max98357a-i2s-audio-breakout-amplifier-for-raspberry-pi-and-microcontrollers) (₹195, 78 in stock on 2026-10-03) as the bench amplifier. It is BO-007, qty 2 (one spare). It drives the BO-001 speaker until PCB-05 exists. The installed amplifier is still the MAX98357AETE+T on PCB-05 (BO-003, `CANDIDATE`).

**Why:**

- It has the same chip as BO-003, so the i2s0 overlay, wiring and software carry over to PCB-05 unchanged.
- It is the "Adafruit #3006-class breakout" that the [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.7 and D-034 name for Phase A, and it is in stock in India.

**Bench wiring:** BCLK → GPIO18, LRC → GPIO19, DIN → GPIO21 (SDO0), SD → GPIO23 (`AMP_SD`), VIN → 5 V, GND → GND. The speaker goes on the screw terminal. Leave GAIN open to start.

**Differences from PCB-05 (accepted for the bench):**

- **Not off by default.** The listing publishes no schematic. If the board follows Adafruit's layout, SD has a 1 MΩ pull-up to VIN, so the amp is on at power-up. A 100 kΩ pull-down against that gives about 0.45 V, which is (L+R)/2 mode, not shutdown (< 0.16 V). Fit about 10 kΩ from SD to GND if off-at-boot is wanted. GPIO23 high (3.3 V) selects the left channel.
- **No 100 Ω series resistors** on BCLK, LRC or DIN. Do not stream into it while it is unpowered.
- **Screw terminal, not JST GH**, and no mounting in the CAD. It is not an installed article.

**BOM changed:** [`BOM.csv`](BOM.csv) gains BO-007. BO-003's release check now points at it. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) lists it under bench articles.

**CAD:** no change.

**Unverified:** the SD pull-up value and the default gain on the received board; its outline; the listing's stock and price at order.

**Next:** order BO-007 with BO-001. Check the SD network on receipt, then run the bench listen and the Pi 5 two-lane capture-plus-playback test.

## D-036

**2026-10-03 · Body / audio microphones (BO-012, BO-005) · ACTIVE; SELECTED, not ordered; HOLD on PCB-06 layout and the array tap test**

**Decision:** the builder locked the body microphone as the **Infineon IM73D122V01XTMA1** (PDM, PG-LLGA-5-4, bottom port), bought from [element14 India, order code 4125831](https://in.element14.com/infineon/im73d122v01xtma1/mems-microphone-pdm-122db-pg-llga/dp/4125831). It is the new row BO-012: four installed, one on each BO-005 (PCB-06) board. Buy six (two reflow spares). The array stays at **four mics**: FRONT_L/R and REAR_L/R.

**Why this mic:**

- **73 dB(A) SNR** (about 21 dBA self-noise). Cheap PDM mics are about 64 dB (about 30 dBA). The difference shows in a quiet room at 2–3 m, which is the quiet-sleep wake-word case (RP-05 `audio-path.md` rule 2), when the Pi cooler is likely off. With the fan or motors running, their noise dominates and the gap narrows.
- Bottom port, which the PCB-06 design needs (mic on the inboard face, listening through a Ø0.8 mm hole). Matched to ±1 dB, 122 dB SPL overload, IP57. Runs in its high-performance clock window at the 3.072 MHz the ADAU7002 gives at 48 kHz.
- It is the part the RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.2 named, so the CAD (`MIC_PACKAGE_SIZE` 4 × 3 × 1.2) and the `BODY_AUDIO` mass row need no change.
- Cost: six cost about ₹1,500–2,000. A cheaper mic would save about ₹1,200–1,700 of the ₹6,500–11,000 audio estimate; the builder kept the SNR.
- Availability: the builder saw 9,000+ in stock at element14 India. The 45-week figure on the page is Infineon's factory lead time for orders beyond that stock. JLCPCB (C5563886) showed 0 stock, so the mics go to JLCPCB as consigned parts or are reflowed by hand.

**Alternatives:**

- **MEMSensing MSM261D3526Z1CM:** PDM, bottom port, 64 dB SNR, 3.5 × 2.65 mm. The cheaper fallback; PCB-06 is not laid out, so the footprint change would be free. Not the **MSM261D3526H1CPM**, which is top port.
- **Infineon IM69D128S:** 69 dB SNR at a similar price. No gain.
- **IM69D130:** not for new designs.

**Why four, not six:** RP-05 `AR-01` asks for four synchronised body mics at the existing ports. Each ADAU7002 carries one stereo pair on one Pi 5 capture lane, so four mics use SDI0/SDI1 (GPIO20/22). Six would need a third ADAU7002, a third lane (GPIO24, another `CA-06` change), two more PCB-06 boards and shell ports, and new placement checks. A ±70 mm four-mic rectangle already supports direction finding and beamforming.

**BOM changed:** [`BOM.csv`](BOM.csv) gains BO-012 (`SELECTED`); BO-005's supplier column points to it. [`02-body/v1/BOM.md`](02-body/v1/BOM.md) lists BO-012.

**CAD:** no change.

**Unverified:** element14 price and stock at order; the received package against 4 × 3 × 1.2 mm; PCB-06 layout; channel order and L/R convention by the array tap test.

**Next:** order six with BO-001 and BO-007. Store them sealed. Lay out PCB-06 around the PG-LLGA-5-4 land pattern.

**Array checks (added 2026-10-03, builder review of the side-only layout):** the four side ports stay. The array is centred on the yaw axis (X 16), 76 × 140 mm, and keeps the mics away from the forward speaker. Three checks are added to the BOM release checks:

- **Calibration (BO-012):** the body shadows the far-side mics above about 1.5–2 kHz (`E`), so free-field DOA is biased. Each robot gets a spin-in-place calibration: loudspeaker at 1 m, chirp every 10° as the base rotates, measured responses stored for DOA and beamforming.
- **Noise (BO-005):** FRONT_L and REAR_L are about 30 mm from the yaw-servo envelope; the −Y pair is far from it. Before ordering PCB-06, run the yaw servo and the cooler at full speed and compare left and right channels. If the +Y pair is worse, isolate the board mounts rather than move the ports. Confirm the cooler exhaust does not reach the front ports (`AR-61`).
- **Port seal (BO-005):** the boot must seal between the board and the shell skin.

## D-037

**2026-10-03 · Body / microphone mounting (BO-005, BO-006; BO-013, BO-014 new) · ACTIVE; DESIGN in CAD, checks green; HOLD on a printed boss coupon and the PCB-06 layout**

**Decision:** the four PCB-06 mic boards mount on the **shell**, not the body frame.
- Each board lands on a printed boss on the inner skin, coaxial with its side port.
- A closed-cell foam gasket ring in a pocket round the port seals it.
- Two M2 × 4 thread-forming screws clamp it.
- The side-entry GH header is dropped. Each board carries a soldered, pre-crimped GH 4-way lead that plugs into PCB-05 after the shell is lowered.

This replaces "screwed to the body frame" in BO-005 and RP-06 [peripheral selection](../02-prototypes/RP-06-cad/peripheral-selection.md) §2.7. It also replaces the GH header at the mic end of W27 in the RP-06 [connector schedule](../02-prototypes/RP-06-cad/connector-schedule.md).

**Why:**

- **Nothing held the boards.** The CAD had no fixing. There is also no frame material at the ports: between the lower rail (Z 69) and the upper rail (Z 126) the frame side is open, apart from the corner posts about 5 mm from each board.
- **A frame-mounted board cannot seal to the shell.** The shell lowers vertically, so a boot between board and skin would be wiped sideways as the shell drops. The old Ø6 × 5 boot also overlapped the leaning skin unevenly: 26 mm³ at the front ports, 2.4 mm³ at the rear. No check covered it, because the mics were outside `check_shell_frame_fit.py`.
- **On the shell, port and seat are one print.** They stay coaxial with no frame-to-shell tolerance between them. The screws compress the gasket squarely to a hard stop, so the seal does not depend on how the shell lands.
- **The array stays rigid.** All four mics are fixed to one part (RP-05 `AR-64`), and the D-036 spin calibration absorbs print tolerance. The boards also come off the frame that carries the yaw servo (the D-036 noise concern).
- **The header had to go.** The boards ride down with the shell past the frame's upper side rails (|Y| ≤ 68). The 4.25 mm GH header would hit them. With a soldered lead, the inboard-most part is a screw head at |Y| 69.0, 1.0 mm clear.

**Geometry** (`body_v1_model.py`: `MIC_*` constants, `_mic_boss`, `_mic_boss_cuts`, `_mic_board`):

| Item | Value |
|---|---|
| PCB-06 | 12 × 14 × 1.0 mm (was 12 × 9.5). IM73D122 on the inboard face, on the port axis, over a Ø0.8 hole. Ø2.2 screw holes 5 mm above and below the port. Four lead pads beside the mic |
| Boss | 16 × 17 mm flat seat at \|Y\| 71.3, filled out to the sloped skin. Its upper face rises at 45°, because the shell prints roof-down. Depth from seat to inner skin is 2.5 mm at the front port axis and 3.7 mm at the rear |
| Gasket | Ø6.5/Ø2.0 × 1.0 mm closed-cell foam in a Ø7.0 × 0.7 mm pocket. The board lands on the seat, so compression is 30% |
| Port | Ø2.0 through boss and skin (was Ø3.0 through the skin). Skin-to-mic chain is 5.9 mm front and 7.1 mm rear. Helmholtz estimate 13–23 kHz for a 1–3 mm³ mic front chamber (`E`) |
| Screws | M2 × 4 pan head, thread-forming, into Ø1.6 × 3.3 mm blind pilots: 3.0 mm engagement, at least 0.98 mm of skin left beyond each pilot (front top screws) |
| Lead | 4 × AWG28 lying flat on the inboard face, leaving toward the body centre. About 150 mm front and 200 mm rear (`E`). The +Y boards plug into `J5-2`/`J5-3`, the −Y boards into `J5-4`/`J5-5` |

**Assembly:** on the bench, stick a gasket to each board and screw the boards to the loose shell, in the same step as the wheel-arch pods. Leave the leads hanging free. Lower the shell. With the front panel and speaker still off, plug the leads in through the front service aperture. Unplug them before lifting the shell off.

**BOM changed:** [`BOM.csv`](BOM.csv):
- **BO-005:** respecified (shell-mounted, 12 × 14 mm, no header, DATA series resistor).
- **BO-006:** W27 becomes four pre-crimped GH leads soldered at PCB-06.
- **BO-013 (new):** M2 × 4 thread-forming screw, 8 off, `CANDIDATE`. Same family and pilot qualification as CH-039.
- **BO-014 (new):** mic port gasket, 4 off, `CANDIDATE`.

[`02-body/v1/BOM.md`](02-body/v1/BOM.md) is updated to match.

**CAD and checks:**
- The shell gains the four bosses, and the boot and port placeholders are removed.
- New [`check_mic_mounts.py`](02-body/v1/cad/check_mic_mounts.py): 15/15 checks pass (16/16 after the vendor-STEP addendum below), written to `generated/mic-mount-fit.json`. It covers seat, gasket, sound path, port, screw depth, rail clearance, and clashes against the shell, each other and every body and chassis part.
- `check_shell_frame_fit.py` lowers the 32 mic parts with the shell, against PCB-05 and its edge connectors added to the fixed parts. Result: no overlaps (29 min; 69 min after the vendor-STEP addendum, still clean).
- `check_body_layout.py`: 14/14 checks pass.

**Mass:**
- `BODY_SHELL_AND_PANELS`: 246.7 → 250.7 g at (19.8, 0, 93.5).
- `BODY_AUDIO`: 60 → 61 g at (74.5, 0, 102.1).
- Whole robot: 2,423.1 → 2,428.1 g, CoM (+18.47, +0.24, 106.01) mm.
- Neutral a_tip: 1.711 → 1.709 m/s². Head-pose bound: 1.708 → 1.706 m/s². Paper screen: 1.582.
- Propagated to `01-system/dimensional-baseline.md` v1.15 and `mass-envelope-ledger.md` v0.19.

**Not changed:** the chassis v1 model's legacy copy of the body (`01-chassis/v1/cad/body_chassis_model.py`) and its `check_layout.py` mic checks still describe the old frame-side boards. Chassis v1 does not fabricate the body.

**Unverified:**

- Print: a side-wall coupon with one boss. Check seat flatness, the Ø1.6 pilots drilled to 3.3 mm, no witness mark on the outer skin over the pilots, and the roof-down 45° boss face.
- Seal: a tap test with the port taped and open, and gasket compression set after a week clamped. The gasket material and source are open.
- The thread-forming screw itself (CH-039 qualification) and repeated-service strip resistance.
- Reaching and mating the four GH plugs at PCB-05 through the front aperture, and the lead lengths. The leads are not routed in CAD.
- PDM over a 200 mm AWG28 lead: CLK and DATA integrity at 3.072 MHz. Termination is set in the PCB-05/06 layouts.
- The mic front-chamber volume behind the resonance estimate.

**Next:** print the boss coupon with the next shell test print, lay out PCB-06 to the 12 × 14 outline (everything inboard within 1.3 mm of the board), and pick and punch a gasket sample.

**Vendor STEP (added 2026-10-03, builder review):** the mic package was a 4 × 3 × 1.2 mm placeholder box. It is now Infineon's own PG-LLGA-5-4 STEP, downloaded from the Infineon package page into [`02-body/v1/cad/purchased/`](02-body/v1/cad/purchased/README.md) with its SHA-256.
- The body measures 4 × 3 × 1.30 mm; the datasheet gives 1.2 ± 0.1 mm.
- **The sound port is 0.68 mm off the package centre** along the 4 mm side, away from pins 1–4 (datasheet Fig. 12/13). The placeholder had it at the centre.
- The package is now placed by its port, which sits on the port axis and the Ø0.8 PCB hole. The body extends 2.68 mm toward the frame post and 1.32 mm toward the lead pads.
- `check_mic_mounts.py` now checks the port position and the vendor outline: 16/16 pass.
- **PCB-06 layout:** use the Fig. 13 land pattern with the PCB hole at the port, not at the package centre. Everything inboard must stay within 1.3 mm of the board face.

## D-038

**2026-10-03 · Power boards (PCB-01, PCB-03, PCB-10; CH-017, CH-023, CH-041–CH-043; CH-083–CH-086 new) · ACTIVE; DESIGN; HOLD on TIFPS0629 bench acceptance and MOT3001 winding R/L**

**Why:** the whole-system power review found that the RP-02 power-board spec still assumes the custom PCB-01, Pololu DRV8874 carriers and the Pololu #4804 motor. The build uses the bought TIFPS0629 (D-019), Adafruit #3297 DRV8833 boards (D-019) and the MOT3001-6V230RPM (D-003). RP-02 is read-only, so the build deltas now live in [04-pcbs/power-boards.md](04-pcbs/power-boards.md).

**Decisions:**

- **Motor-bus TVS: SMBJ8.5A replaces SMBJ10A.** The DRV8833's `VM` absolute maximum is 11.8 V (TI SLVSAR1E). The SMBJ10A's 11.1–12.3 V breakdown and 17 V clamp do not protect it. The SMBJ8.5A breaks down at 9.44 V minimum and clamps at about 10.9–11.3 V at 5 A (`E`). The bus never exceeds the 8.4 V pack because the charger is cut off by `CHARGE_ABSENT`. Each #3297 keeps at least 100 µF + 0.1 µF at `VM`.
- **Power entry:** `PB-DRIVE-L/R` lands on the #3297 `VM` pin, not on the polarity-protected `Vmotor` terminal, which could block regeneration.
- **Sleep gate:**
  - A 74LVC1G08 on PCB-10 drives both `SLP` pins from C3 GPIO21 AND `BASE_READY`.
  - It replaces the series N-FET stages. A 3.3 V signal passed through an N-FET falls below the DRV8833's 2.5 V `nSLEEP` `VIH`.
- **Fault:** both `FLT` pins are wired-OR to GPIO9. Firmware latches any fault and requires a fresh arm, which defeats the chip's 1.35 ms auto-retry.
- **Inputs:** GPIO13/14 change from DIR to a second LEDC output (`IN2`), so both directions run in slow decay. Brake is `1, 1`. C3 caps the duty at `6.0 V / V_bus` (71% at 8.4 V).
- **Current observation:** two bidirectional INA181A2 monitors (5 mΩ, 0.25 V/A around 1.25 V) on the PCB-03 drive feeds. They replace the DRV8874 `CS` signal. No C3 pin is added.
- **Hardware limit:** the fitted 0.2 Ω sense resistors chop each board at 1.6–2.4 A.
- **Regeneration:** the 3 A / zero-below-0 °C rule holds with margin. Slow-decay deceleration returns at most `E_b² / (4 · V_bus · R)` ≈ 0.32–0.45 A per motor (`E`). Below 0 °C, C3 stops by brake and coast only.
- **PCB-01 acceptance:** the TIFPS0629 publishes no trip points, so it must pass a bench window before cells are connected:
  - overcharge 4.275–4.35 V per cell;
  - over-discharge 2.30–2.70 V per cell, so the pack cuts out after `ENERGY_OK`;
  - discharge overcurrent ≥ 15 A, ≥ 20 A preferred, so the motor gate opens first;
  - short-circuit trip ≤ 1 ms, ≤ 30 mΩ series resistance, ≤ 16 µA quiescent, ≤ 4.5 mm height.

  The AC72ABD and 103AT-2 stay separate from the module.
- **Folder:** `04-custom-pcb/` is replaced by [04-pcbs/](04-pcbs/README.md), with a register of every board.
- **New BOM rows:** PCB-08 (CH-083), PCB-09 (CH-084), PCB-11 (CH-085) and **PCB-12**, a new ID for the C2 head carrier (RP-02 `CCD-HDL-02`, CH-086).

**Recomputed (`E`):**

- Peak pack current at a 6.0 V pack is about 10.2 A (11.0 A at the upper chopping corner), below the historical 11.7 A. The 15 A main fuse and 3 mΩ gate shunt stand.
- The OFF budget is 34–84 µA plus the module.
- `V_SRC_SAFE` no longer comes from the driver (DRV8833 runs to 2.7 V). The brownout thresholds are unchanged.

**BOM changed:**

- CH-017 and CH-023 release checks.
- CH-041–CH-043 now point to `04-pcbs/power-boards.md`; CH-042 lists the new parts.
- BO-002's folder reference.
- CH-083–CH-086 added.

**CAD:** not changed. `body_v1_model.py` has uncommitted edits from other work. The J10-5/J10-6 labels ("mapping TBD") take the power-boards §2.4 mapping at the next body CAD edit. The RP-06 connector schedule (W06/W07, W32/W33, §3.3) is superseded by power-boards §2.3–2.4 where they differ.

**Open:**

- TIFPS0629 bench acceptance on two received units.
- MOT3001 winding resistance and inductance on receipt, then recheck the TVS and regeneration numbers.
- NTC lead and disconnect (CH-025).

**Update 2026-10-03 (same day):** paper items closed.
- SMBJ8.5A leakage is at most 20 µA at 8.5 V (Littelfuse).
- The drive-feed monitors are one INA2181A2 (dual, separate `REF` pins) with a REF3312 1.25 V reference, fed from a local 3.3 V LDO so the output cannot exceed 3.3 V.
- The `J10-5`/`J10-6` labels in `body_v1_model.py` and `body_chassis_model.py` carry the mapping (strings only, no geometry).
- The temporary `power-review-todo.md` is deleted. Its remaining bench items are tracked in [power-boards.md §5](04-pcbs/power-boards.md#5-open) and CH-023.

## D-039

**2026-10-04 · Harness: connectors, wires and service breaks (W01–W39; CH-025–CH-027, CH-041, CH-042, CH-083; HN-001–HN-010) · ACTIVE; DESIGN; HOLD on housing part numbers, crimp qualification and the first harness build**

**Decision:** the harness is specified in [05-harness/README.md](05-harness/README.md), which replaces RP-06 `connector-schedule.md` §3 and §5 for the build. It closes that schedule's open items 1 (NTC break), 6 (pinouts and mating order), 7 (tooling) and 8 (wire list).

**Builder choice (2026-10-04): the fused pack feed splits at the fuse.** The fuse output and the pack negative each fork at a crimped butt splice above the PCB-03 +Y edge (X 22–48, Y 36.5–49, Z 77–83). One branch feeds PCB-03 `J3-1`, the other PCB-02 `J2-1`. **`W04` and PCB-02 `J2-2` are deleted.** The negative splice is the power star.

**Why:** the RP-02 route ran pack → fuse → PCB-02 on the rear panel → back to PCB-03: about 0.5 m and four mated pairs. With typical contacts (2.5 mΩ) the pack-to-gate path falls from 44 to **25 mΩ**; at Molex's 10 mΩ maximum it falls from 104 to **55 mΩ**. That is still above the ledger's 10 mΩ wiring allowance, because the contacts dominate. The pack model becomes about 99 mΩ typical, at the top of the ledger's 80–100 mΩ range. Measure it in Phase C.

**Other rules set:**
- **`J-PK` is the isolator.** `J2-1` and `J3-1` mate only with `J-PK` open. Every other connector mates only in `OFF`, with the charger out, when every body rail is dead. That replaces a mating-order requirement Micro-Fit parts cannot meet: they have no first-mate pins.
- **One tool per crimp family.** Micro-Fit+ is used only on AWG16/18 (Molex 213309-4400). Micro-Fit 3.0 is used only on AWG20–24. Every GH cable is a pre-crimped lead.
- **Micro-Fit+ needs thin-wall wire.** The 206460-0041 terminal is specified for 2.00 mm insulation, so the pack lead and every Micro-Fit+ lead are UL1061 class, not silicone (CH-026, CH-027).
- **`J3-4` and `J8-1` move to Micro-Fit 3.0, with all head power pairs at AWG22.** The PCB-03 −Y edge margin rises from 0.4 to 1.44 mm.
- **Pack NTC break:** a JST SM 2-way wire-to-wire pair in the +Y channel ahead of `J-PK` (X 52–76, Z 41.6–47.4), in the space the fuse left in D-032. Its section passes the tub window.
- **Body removal:** 11 chassis leads (12 with the IMU) unplug at the body-side boards; there is no bulkhead connector.
- **Encoders:** run from the C3 carrier 3V3.

The document also holds the full wire list with estimated lengths, every pinout, the drop and current checks, the GH buy list and the service sequences.

**CAD changed:**
- `01-chassis/v1/cad/body_chassis_model.py`:
  - `PACK_NTC_BREAK_RESERVE`/`_PAIR` and `BATBUS_SPLICE_RESERVE` with two Ø6 × 26 splices in `connectors_and_exits()`;
  - `J2-2` removed from the PCB-02 edge;
  - `J2-1`/`J3-1` relabelled;
  - `J3-4` and `J8-1` changed to Micro-Fit 3.0.
- `02-body/v1/cad/body_v1_model.py`: the same connector edits, without the chassis reserves.
- New `01-chassis/v1/cad/check_harness.py` (about 30 s). It runs the check_layout connector rows plus the NTC and splice measurements.

**Checks:**
- `check_harness.py`: **ALL PASS**. There are no reserve or body clashes. Edge margins: PCB-03 +Y 0.4 mm, −Y 1.44, PCB-04 −Y 1.18, PCB-02 13.4. The slide path is clear, the splices sit 2.65 mm from the `J3-1` plug, and the NTC pair passes the window.
- A planted clash (NTC reserve moved onto the fuse holder) was caught.
- The free space for both reserves was found by a clash probe against the whole model.
- The full `check_layout.py` was not rerun.

**Found, not caused by this change (confirmed against the HEAD body model):**
- `body_v1_model.py` still carries pre-D-031 driver positions and the pre-D-032 fuse envelope, so its PCB-03 edge reserves clash with the stale drivers.
- In the body model, the PCB-04 edge reserves clash with `BODY_FRAME_MAIN_PRINT` (108 mm³ each), and so does the `J4-1` plug (45.7 mm³). This is real body-v1 frame geometry.
- `body_v1_model.wheel_assembly()` raises `NameError: WHEEL_MODEL`.

**BOM changed:**
- CH-025 (NTC break defined), CH-026 (UL1061 leads), CH-027 (terminal PN), CH-041/CH-042 (feed entry), CH-083 (`J8-1`).
- New HN-001 to HN-010: harness set, Micro-Fit+ and Micro-Fit 3.0 parts, pre-crimped GH leads, the NTC break pair, splices, wire, the two crimp tools and the Pi power plug.

**Open:**
- Exact Micro-Fit+ housing and male-terminal part numbers, and confirmation of the Micro-Fit 3.0 tool PN.
- The MOT3001 cable colours on receipt.
- Crimp pull tests.
- First-build lengths, the 4-wire pack-to-`J3-1` resistance and plug reach.
- The body-model drift and the frame/PCB-04 edge clash above.

## D-040

**2026-10-04 · Charge path: inlet board PCB-13 and the PCB-02 charger block (CH-041, HN-003; BO-015–BO-017 registered) · ACTIVE; DESIGN; HOLD on schematic capture, the STUSB4500 NVM image and bench CP-01 to CP-14**

**Decision:** the charge path is specified in [04-pcbs/charge-path.md](04-pcbs/charge-path.md). It replaces RP-02 board-specs §4.1 "Charge inlet" and "Input switch" and corrects §4.5.1. Builder request (2026-10-04): design the inlet properly and close the recharging circuit.

**Why the inlet moved:**
- The vertical receptacle on PCB-02's back face had its mouth 3.3 mm behind the sloped panel's inner face, not the 1.05 mm its CAD comment said. A plug had to push its overmold 5.7 mm into a 13.2 × 7.2 mm cut-out, with 0.35–0.43 mm a side against an untoleranced panel-to-board stack.
- Every insertion and pull loaded PCB-02, which has no mounting.
- The part number was open.

**Inlet (PCB-13, BO-015):**
- A 28 × 15 mm board on a pad printed with the rear panel.
- **GCT USB4140-GF-0170-C**: vertical, 6-pin power-only, 6.50 mm high, four through-hole shell stakes, 20k cycles, 5–20 N mating (`D`).
- Its mouth is flush with the floor of a 13.4 × 7.6 mm, R 1.0 pocket in the 7° facet. A sharp-cornered 12.35 × 6.5 mm overmold, the USB Type-C maximum, clears it by at least 0.35 mm.
- Two M2 × 5 thread-forming screws (BO-017) 11 mm either side carry the plug loads into the panel.
- The board also carries the TVS2200, the ESDA25W on CC, the STUSB4500 and the STL6P3LLH6 input switch.
- `W16` (2 × AWG22) runs to a new PCB-02 `J2-8`, Micro-Fit 3.0 on the free +Y edge. Unplug it when the panel comes off; the inlet stays on the panel.

**Circuit corrections found against the datasheets** (BQ25798 SLUSDV2C June 2026, STUSB4500 DS12499, TVS2200 SLVSED5C):
- **`TS` divider 5.23 k / 30.1 k → 8.45 k / 324 k.** Across all tolerances, the old values let charging run from −3.5 °C up to 62 °C. The 25R allows 0–50 °C at the surface. The new window is 0.1–3.9 °C to 46.4–49.5 °C. Cost: the JEITA warm step (8.0 V) now starts at about 35 °C instead of 45 °C.
- **`D+` tied to `D−`.** This reads as a BC1.2 DCP, and the `ILIM_HIZ` pin clamps it at 1.18–1.38 A. Floating lines risk an SDP result: 500 mA, about 7 W.
- **`BATP`** (pack voltage sense) gets 100 Ω and a Kelvin trace to `J2-1`. RP-02 omitted the pin.
- **The `VBUS` side is rated for 20 V,** because a blank STUSB4500 asks for 20 V.
  - TVS2200: 22 V standoff, 28 V clamp, under the charger's 30 V absolute maximum. The ESDA25P35 does not fit both limits.
  - A 100 k / 33 k divider keeps the P-FET `VGS` at −15 V at 20 V.
  - 50 V capacitors on `VBUS`/`PMID`.
- **Both NTC leads land on PCB-02.** A return on a cell would sit behind the TIFPS0629 FETs and block recovery charging.
- **Defaults confirmed** (`D`): 8.4 V (8.379–8.455 V), 1 A, 12 h timer, `VSYSMIN` 7 V, `VAC_OVP` 26 V. The register reset value is 85h; the field's "POR: 11b" reads as 7 V and is treated as a datasheet slip, with bench check CP-04 to confirm. The inductor is Würth 74437346022 (Isat 10 A), which closes the RP-02 item.

**CAD changed** (`02-body/v1/cad/body_v1_model.py`):
- The `CHARGE_INLET_*`/`PCB13_*`/`USB4140_*` constants.
- `rear_panel_charge_inlet()`, the pad and cuts unioned into the rear panel.
- `charge_inlet_pcb13()` in `POWER_DISTRIBUTION_BOARDS`.
- The `PCB02_PY` edge strip with `J2-8`.
- The `W16` lead reserves, and the plug corridor redrawn at the maximum overmold.
- The old PCB-02 receptacle envelope and the 13.2 × 7.2 cut-out are removed.
- Mass: `PCB02_CHARGE_AND_SYSTEM_POWER` keeps 18.0 g (receptacle out, header in); new `CHARGE_INLET_PCB13` row, 4.5 g (`E`). The pad is in `BODY_SHELL_AND_PANELS`: 253.7 g, re-measured, +3.0 g.

The chassis model's Layout 02 body copy (`body_chassis_model.py`) still has the old inlet and its `charge_inlet_is_cut_through_rear_panel` row. Body v1 governs the body, so the copy is left as it is.

**Checks:**
- New `check_charge_inlet.py` (about 6 min): **ALL PASS**.
  - Pocket depth 0.62–1.60 mm.
  - Mouth to floor 0.00 mm.
  - Board seated (0.00 mm).
  - Receptacle to panel 0.28 mm.
  - Overmold to pocket wall 0.346 mm.
  - PCB-13 parts to PCB-02 1.9 mm.
  - Screw engagement 3.4 mm, with 3.97 mm of print beyond each pilot.
  - No clash for the inlet, corridor, lead or `J2-8` against the shell, the frames or any body or chassis part.
  - The 40 mm removal sweep of the pad and board is clear.
- Planted clashes were caught: 328.9 mm³ with PCB-13's parts moved 3 mm into PCB-02, and 49.5 mm³ with the pad dropped 2.5 mm onto the panel frame.
- `check_body_panel_fit.py`: clean.
- `check_body_layout.py`: all checks true. Whole robot 2435.6 g, CoM x +18.24 / z 105.87 mm, a_tip 1.690 m/s² against the 1.582 minimum.
- The full chassis `check_layout.py` was not run; nothing in the chassis model changed.

**BOM changed:** CH-041 (charger block, `J2-8`) and HN-003 (`J2-8` plug). New BO-015 (PCB-13), BO-016 (≥ 30 W PD adapter with 15 V and a 3 A cable) and BO-017 (M2 × 5 screws).

**Open:**
- Schematic and layout of PCB-13 and the PCB-02 charger block.
- ST PDFs for the ESDA25W and STL6P3LLH6; only distributor summaries were read.
- India sourcing for the USB4140, TVS2200 and BQ25798.
- The NVM programming jig.
- Bench CP-01 to CP-14.
- Whether summer charging to 8.0 V above 35 °C is acceptable. A host would be needed to move T3.
- PCB-02 mounting, which is still absent from the CAD; the rear lower cross rail is the candidate seat.

## D-041

**2026-10-04 · Body / power button: the rear mushroom is the power button and there is no E-stop (BO-018 registered; CH-041, CH-042, CH-046, HN-001, HN-004; W40, J2-9 added; W22, J3-7 removed; W38, J10-11 not fitted) · ACTIVE; DESIGN; HOLD on the received part's fit in the well and bench PB-01 to PB-06**

**Decision:** Makad has **no E-stop**. The red mushroom in the rear-panel well is now the **power button**. Builder (2026-10-04): "remove the newly made power button, and rewire the red mushroom to be the power button, instead of the estop button".

The first draft of this entry, earlier the same day and not committed, added a separate 12 mm GQ12 ring-lit button beside the E-stop. That button, its pad, its LED feed and its mass row are removed.

**Why the part changes.** The fitted IDEC XA1E-BV3U02KT-R (CH-046) is a push-lock, turn-reset E-stop with two NC contacts. The power latch (`LTC2954`) needs a momentary NO contact. Held in, the XA1E would keep `PB` pressed; released, its NC contact would short `PB` all the time. It cannot be rewired to do the job. BO-018 is a **16 mm momentary red mushroom, 1NO**, in the same well and inside the XA1E's envelope:
- Ø16.2 cut-out in the 2 mm floor;
- mushroom Ø30 or less, rising no more than 20.6 mm above the floor;
- 23.9 mm or less behind the floor.

Candidate: a SparkFun-type metal 16 mm mushroom (Tanotis, ₹850). Bench fallback: the Daier A16-11SM (Evelta, ₹118), which is plastic and rated for 10k operations.

**Why removing the E-stop is acceptable.** The builder's call, with the hazard as context: a 2.4 kg robot at about 0.5 m/s, with about 2 A stall motors. Robots of this class (Roomba, TurtleBot 4) carry no mushroom E-stop. This supersedes, for the build, RP-02 `PA-13`'s dominant latching hardware E-stop and the `E_STOP_OK` term of `MOTOR_PERMIT` (`BR-05`). The separate bench E-stop on motion rigs (`workbench.md`, F4) is unchanged.

**What keeps a hardware stop.** The latch's `INT` output also resets the `SYSTEM_ARM` latch on PCB-02. RP-02 cleared that latch on an E-stop assertion. So any press while running opens `Q_ARM` in the permit chain, and the `LTC4368` cuts the drive and head bus through its fast `UV` path, with no firmware involved. The arm never resumes on release (F-13); C2 has to re-arm.

What this loses against the XA1E:
- a stop that stays latched where you can see it;
- the second, independent contact;
- the universally recognised E-stop meaning, although the button is still red.

**Circuit** ([power-boards.md §6](04-pcbs/power-boards.md#6-pcb-02-power-button-input-d-041)):
- `J2-9` is a side-entry GH2 on PCB-02's +Y edge at Z 88.6, above `J2-8`. Pin 1 is `PB_SW`, pin 2 is GND.
- `R_WET`: 10 kΩ from the latch `VIN` to `PB_SW`. A press passes 0.84 mA instead of 19 µA, and a released button draws nothing (`D`, LTC2954; `PB` accepts up to 26.4 V).
- `INT` resets `SYSTEM_ARM`.
- On PCB-03, a 0 Ω link replaces the E-stop NC contact at the head of the permit chain. `J3-7` is deleted.
- **Firmware:** C2 starts an orderly shutdown only after `INT_PB` has been low for 1 s. A shorter press only stops motion.
- Turn-on still needs the 0.5 s `ONT` hold, and about 5.2 s forces off in hardware. In `CHARGE` a press does nothing (`Q_kill`).
- The button has no light; the head display shows the state.

**Harness** ([05-harness](05-harness/README.md)):
- `W40` is a 150 mm single-ended GH2, terminals to `J2-9`. It comes off with the panel.
- `W22` (to `J3-7`) is deleted.
- `W38` and C3 `J10-11` (E-stop status) are not fitted. The `J3-8` `E_STOP_STATUS` pin is spare.

**CAD changed** (`02-body/v1/cad/body_v1_model.py`):
- The XA1E header comment is rewritten.
- `estop_switch()` becomes `power_button_mushroom()`, with two terminals instead of three tabs.
- Labels change: `ESTOP_XA1E_*` → `POWER_BUTTON_MUSHROOM_*`, and `REAR_PANEL_ESTOP_*` → `REAR_PANEL_BUTTON_*`. The `ESTOP_*` geometry constants keep their names.
- New `POWER_BUTTON_LEAD_RESERVES` (W40) and `_power_button_lead()` with `J2_9_GHR02_MATED_PLUG`.
- `J3-7` is dropped from the PCB-03 connector list, and `J10-11` is marked not fitted.
- The mass row is now `POWER_BUTTON_MUSHROOM_16MM_AND_W40`: 15 g (`E`; was the XA1E, 14 g `D`).
- Check scripts follow the new labels: `check_body_panel_fit.py`, `check_charge_inlet.py`, `check_shell_frame_fit.py` (the button stays out of the lowering path) and `write_outputs.py`.
- The chassis v1 model still carries the XA1E in its reference copy. It is filtered out of the body checks and was not edited.

**Checks:**
- New `check_power_button.py` (about 5 min): **ALL PASS**.
  - Mushroom to the well wall 3.98 mm.
  - Button solids to PCB-02 2.5 mm; contact-block keep-out to PCB-02 0.5 mm, against the 0.4 mm running-gap rule.
  - No clash for the button, the `W40` reserves or the `J2-9` plug.
  - The 40 mm panel-removal sweep is clear.
- `check_body_panel_fit.py`: clean.
- `check_body_layout.py`: all checks true. Whole robot 2433.1 g, CoM (+18.20, +0.24, 105.88) mm, a_tip 1.686 m/s² against the 1.582 minimum, head-pose bound 1.682. The 95 g harness allowance must sit forward of X −7.7 mm.
- `body-v1.step` rebuilt with `--force`; snapshot `snapshots/body-v1-rear-power-button.png`.
- Not run: `check_shell_frame_fit.py` (70 min) and the chassis `check_layout.py`.

**BOM changed:**
- BO-018 (mushroom power button).
- CH-046 SUPERSEDED.
- CH-041: `J2-9`, `R_WET`, the `INT` → `SYSTEM_ARM` reset.
- CH-042: `J3-7` deleted, 0 Ω link in the permit chain.
- HN-001 and HN-004: `W40` GH2, `W22` deleted, `W38` not fitted.

**Docs changed:**
- [power-boards.md §6](04-pcbs/power-boards.md#6-pcb-02-power-button-input-d-041) and the [04-pcbs board register](04-pcbs/README.md) (PCB-02, PCB-03).
- [05-harness](05-harness/README.md): wire list, buy list, pinouts and the panel-removal step.
- The [02-body BOM](02-body/v1/BOM.md) and [CAD README](02-body/v1/cad/README.md#power-button-d-041).
- The [chassis BOM](01-chassis/v1/BOM.md) (CH-046) and the [chassis CAD README](01-chassis/v1/cad/README.md).
- The [charge-path](04-pcbs/charge-path.md) service note.
- `01-system/power-energy-ledger.md` (`PB-MOTOR`) and `01-system/workbench.md`: the robot has no E-stop, but the bench motion rigs keep theirs.
- Not edited: `02-prototypes/` (read-only, D-001) and the `01-system` option and sourcing studies (dated analyses).

**Open:**
- Order BO-018 and check its fit in the well envelope: momentary 1NO, weight.
- Add `J2-9`, `R_WET` and the `INT` → `SYSTEM_ARM` reset to the PCB-02 schematic, and the 0 Ω link to the PCB-03 schematic.
- Add the 1 s `INT_PB` rule to the C2 firmware.
- Run bench PB-01 to PB-06.
- Update the chassis v1 reference copy of the E-stop at the next chassis CAD pass.

## D-042

**2026-10-04 · Body / compute retention and cooling path: the Pi 5 is screwed to a vented three-point tray, and a +Y side intake fan switched by the Pi ventilates the body (BO-033 to BO-042; CH-084 PCB-09 fan switch; W41, J9-4) · ACTIVE; DESIGN; HOLD on the bench thermal test, the AR-61 noise check, the GPIO24 change request (CR-02) and printed coupons**

**Decision.** The builder chose the side intake fan (2026-10-04) after the passive and rear-exhaust options were compared. The builder then chose BO-040, a generic 2-wire DC 5 V 4010 double-ball fan, over the Noctua NF-A4x10 5V PWM this entry first drew, and chose to switch it on/off from a Pi GPIO through PCB-09 rather than PWM it inline or run it always on.

**Why the change.** The Pi 5 and its cooler were not held down. The compute tray was a plain 3 mm box that floated in CAD, with no standoffs, no screws and no tie to the frame (RP-06 TODO). The shell had no cooling path: the Pi and its fan sat in a closed PETG body.

**Why a fan, not vents only.** The measured layout leaves almost no high outlet area.
- **Inlet:** the open floor is already a large inlet, with at least 11,600 mm² free in horizontal sections from Z 31 to 90.
- **Outlet:** the only high wall area away from the mic ports is the rear-panel aperture beside the button well, about 460 mm². The 1 mm gap under the yaw disc passes almost nothing.
- **Pi cooler:** its exhaust runs rearward into the button's contact block, with 5 mm between them, so it cannot be ducted out.
- **Estimate (`E`):** at 8.5 W (Pi 6 W plus converters 2.5 W) the internal air rise is 19.3 K sealed and 14.7 K with vents only. With the fan on it is 4.3 K at a typical 4010 listing-class flow (about 5.5 CFM, 4 mm H₂O) and 7.0 K at half that flow. BO-040's real curve is unmeasured.
- **Throttling:** the Pi 5 throttles from 80 °C and the Active Cooler holds the SoC roughly 30–40 K above its local air. That leaves vents only throttling under sustained load in a 30–35 °C room.

**Why the +Y side.** A 40 mm rear exhaust fan does not fit:
- The panel-frame aperture beside the button well is about 23 mm wide.
- The rear cavity is about 23 mm deep before the Pi, PCB-02 and the W40 lead.

The +Y side wall has one place that clears all of these:
- the wheel-arch pod band (R ≤ 54 about the axle);
- the 90° pod screw boss;
- both +Y mic bosses;
- the upper side rail.

**Compute retention (CAD).**
- **Tray:** a separate PETG print (`COMPUTE_TRAY`). It is a 108 × 76 × 3 mm plate at Z 84.5–87.5 with a 2 × 4 mm perimeter rib, vent slots and four Ø6 bosses up to the Pi's PCB underside at Z 94.05.
- **Pi 5:** four M2.5 × 6 low-head screws into M2.5 × 4 heat-set inserts (as CH-080/081), with 4.6 mm of thread.
- **Active Cooler:** kept on its own two spring push pins, the vendor design. A Ø5 × 3.5 mm keep-out under each pin tip (`E`) stays clear of the tray.
- **Tray to frame:** three supports printed on the frame, each taking an ISO 7380 M3 × 8 screw from above into an M3 × 6 insert (as CH-077):
  - a lug on the rear −Y post, under an ear at (−32, −50.5);
  - a column on the front −Y foot's dog-leg, at (64, −33);
  - a block under the rear +Y corner, on a column from the lower rear cross rail, at (−24, 33).
- **Why these points:** the C3 carrier's `J10-1` plug keeps an ear off the front −Y post. On +Y, nothing may stand proud of the tray edge: the tray goes in from the front past the chassis fuse holder (D-032, X 52–82, Y 39–49, Z 73–99). That fuse holder is where the first-draft front +Y lug was, and the check found it. The front +Y corner is free; the rib stiffens it.
- **Assembly order:** enclosure fan, then the tray with the Pi and cooler slid in from the front 2 mm high, dropped onto the supports and screwed, then the C3 carrier, PCB-09, the yaw servo and the plugged harness.

**Cooling path (CAD).**
- **Fan:** BO-040, DC 5 V 4010 double-ball, 40 × 40 × 10 mm, 2-wire (no PWM or tach), XH2.54-2P lead. Hole pattern 32 mm assumed (`E`); airflow, noise, current and mass unmeasured. It is centred at X 24, Z 105.5, with its intake face at Y 68.9.
- **Fan web:** a new web of the main frame print, X 4–44, Y 56.1–58.9, Z 84–133.2. Roots join it to the upper and lower +Y side rails, and it sits 1.1 mm outboard of the yaw servo.
- **Fan fixing:** two 12 mm self-tapping screws (BO-041), driven from inboard through the web into the fan frame at (8, 89.5) and (40, 121.5); the tips stop 0.8 mm short of the fan face. The other two holes are behind the yaw servo.
- **Shell grille:** vertical 2.5 mm slots inside R18.5, 605 mm² free. A collar, R19.5–21 with its edge at Y 70.5, limits recirculation; 1.6 mm gap and 98 mm² of leak in the estimate.
- **Exhaust:** the open floor, plus eight 2.5 × 23 mm slots in the rear panel beside the button well (460 mm²).
- **Switching (PCB-09, CH-084):** Pi GPIO24 (`FAN_EN`, header pin 18) drives a logic-level N-MOSFET (AO3400A class) on the fan's low side, through 100 Ω with a 100 kΩ gate pull-down so the fan is off at boot and reset. A Schottky sits across the fan and 10 µF on its 5 V. The fan runs from the 40-pin header's 5 V, not the fan header, so the Active Cooler's lead is untouched.
  - Linux: the standard `gpio-fan` overlay on GPIO24 with a temperature threshold and hysteresis, set from the bench test (start at about 60 °C on, 55 °C off).
  - GPIO24 is outside every `CA-06` reservation (UARTs on 4/5 and 14/15, I²C on 2/3, SPI on 8–11, audio on 18–23) and leaves the PWM-capable 12/13 free. It still needs a `CA-06` change request, recorded here as CR-02, as GPIO22/23 did (CR-01).
- **Wiring (`W41`):** the fan's own lead, cut to about 80 mm and re-crimped into its XH2.54-2P housing, runs from the fan's top-front corner above PCB-09's top-entry plugs to `J9-4`, a JST B2B-XH-A top-entry header on PCB-09 (pin 1 FAN+, pin 2 FAN−). CAD: `HARNESS_W41_FAN_LEAD_1/2` and `C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE`.
- **Mic distances:** the grille's edge is 14 mm from the FRONT_L port (33 mm centre to port) and 28 mm from REAR_L. The rear slots are 42.7 mm from REAR_L/R.
- **FRONT_L pigtail:** its first 10 mm crosses the top of the gap between the fan face and the collar, 0.4 mm off the fan face. Dress it outboard when the shell goes on.

**Checks.**
- New `check_cooling_path.py`: **ALL PASS**.
  - No clash for the fan, its screws, `W41` or the `J9-4` plug reserve.
  - The shell, with the +Y mic boards, lowers past the fan and web clear.
  - The intake path is open, apart from the FRONT_L pigtail noted above.
  - The grille clears the pod; the collar is 2.54 mm from the pod boss and 1.36 mm from the FRONT_L mic boss.
  - The rear slots pass the panel frame.
- New `check_compute_mount.py` (about 1 min): **ALL PASS**.
  - The PCB lands on the bosses (0.0 mm). The bosses and screw heads clear the Pi and cooler by 0.3 mm or more.
  - Nothing enters the push-pin keep-outs; the tray is 0.5 mm from them.
  - Thread: 4.6 mm (Pi) and 5.0 mm (tray). At least 1.35 mm of wall round each insert.
  - No clash with any fixed part. The tray screw drivers are clear.
  - The front insertion sweep is clear, with the vendor Pi and cooler leaves swept as their boxes.
  - The tray crosses the existing signal and sensor trunk route reserves (reported, unchanged from before).
- `check_body_frame_fit.py`: clean.
- `check_body_layout.py`: all checks true.
  - Shell and panels 248.3 g (−1.9 g); frame and joints 178.4 g (+7.5 g, web and tray supports).
  - New rows: `COMPUTE_TRAY_AND_PI_FIXINGS` 29.5 g (the tray was in no row before) and `ENCLOSURE_FAN_4010_AND_W41` 15 g (`E`).
  - Whole robot 2,483.2 g, CoM (+18.27, +0.63, 105.62) mm, a_tip 1.697 m/s² against the 1.582 minimum, head-pose bound 1.694.
  - The 95 g harness allowance must stay forward of X −11.3 mm (was −7.7).
  - `shell_symmetric_about_y` now allows 0.5 mm, because the grille is one-sided.
- `write_outputs.py` re-run.
- Not run: `check_shell_frame_fit.py` (about 70 min; `check_cooling_path.py` covers the shell lowering past the fan), `check_body_panel_fit.py`, the chassis `check_layout.py`, and a `body-v1.step` rebuild.

**BOM.** The body BOM pass running in parallel registered the parts:
- BO-033 tray;
- BO-034 Pi 5, BO-035 Active Cooler;
- BO-036 to BO-039 Pi and tray hardware;
- BO-040 fan, BO-041 fan screws;
- BO-042 `W41`.

This entry changed:
- BO-042: now the fan's own lead to `J9-4`, no splice; DESIGN.
- The tray-support wording in BO-025, BO-033, BO-038 and BO-039.
- CH-084 (PCB-09): the fan switch and `J9-4`.

**Docs changed:**
- [CAD README](02-body/v1/cad/README.md#compute-tray-and-pi-5-retention-d-042): the compute-tray and cooling-path sections, the assembly order and the mass refresh.
- [05-harness](05-harness/README.md): `W41` and the `J9-4` pinout.
- [04-pcbs](04-pcbs/README.md): the PCB-09 register row.
- [02-body BOM](02-body/v1/BOM.md): the fan-choice note, BO-042 and the cooling open item.

**Open:**
- **CR-02:** accept GPIO24 `FAN_EN` against the final PCB-09 pin audit, and add the switch and `J9-4` to the PCB-09 schematic.
- **BO-040 on receipt:** measure hole size and pitch, current, airflow against a known restriction, and mass, then update the CAD and `check_cooling_path.py`.
- **AR-61 noise:** this fan is on/off at full speed, with the grille edge 14 mm from FRONT_L. Run it with the yaw servo and compare FRONT_L/REAR_L against the −Y pair. If it is too loud, options are a series resistor or a second GPIO speed step on PCB-09, holding the fan off while listening (firmware), or narrowing the grille's front half.
- **Bench thermal test:** sustained `stress-ng` with the shell on, at a measured room temperature. Log the SoC temperature, `vcgencmd get_throttled`, the internal air near the cooler intake and the cooler RPM, with the enclosure fan on and off. Set the `gpio-fan` threshold from it. Pass: no throttle flag at 35 °C room equivalent under the typical load.
- **Push-pin tips:** measure the Active Cooler pin-tip protrusion against the 3.5 mm keep-out.
- **Prints:** the tray (flatness and boss height), the lug and insert coupons, and the shell collar's support in the roof-down print (DfAM to re-measure).
- **Fan current:** measure BO-040's running and start current against the MOSFET and the Pi 5 V rail (it draws from the 40-pin header, not the fan header).

## D-043

**2026-10-04 · Body / enclosure fan against the mic ports (BO-040, BO-041; W41) · ACTIVE; DESIGN in CAD, checks green; HOLD on measured mounting holes, the bench thermal test and the AR-61 noise check**

**Decision:** the builder rejected the D-042 fan position, which put FRONT_L right beside the fan. The +Y enclosure fan becomes the purchased **3010 hydraulic fan** (30 × 30 × 10 mm, 2-wire, DC 5 V, USB-A lead that is cut and reterminated for W41). It sits **midway between the +Y mic ports**, centred at X 17.5, Z 107. The mic array (D-036/D-037) does not move. Everything else in D-042 stands: the GPIO24 on/off switch on PCB-09, `J9-4`, `W41`, the rear slots and the open floor.

**Why:**

- **Too close.** The 4010 grille's edge was 14 mm from the FRONT_L port and 28 mm from REAR_L. FRONT_L would hear the blade noise and the intake turbulence across its port, and the array's +Y pair would be unbalanced.
- **A 4010 cannot move.** The +Y wall is boxed in: the wheel-arch pod band below (R ≤ 54 about the axle), the upper side rail above (Z 126), and the mic ports at X 54 and X −22. A 4010 at the midpoint (X 16) overlaps the 90° pod screw boss by 1.6 mm. There is no room under the compute tray for a floor-intake fan: the harness trunks and plug layers fill Z 75–86.
- **Moving the mics was the alternative.** Moving the front pair forward to X 78 would give 37 mm, but takes the array's centre off the yaw axis (X 28 vs 16) and brings the mics toward the speaker. The builder chose the smaller fan.
- **Position.** At X 17.5 the diagonal screw pair clears the yaw servo (X 6–26, Z 99–133). The bottom-left head is 1.4 mm under the servo and the top-right head 0.9 mm forward of it. X 16 would put a head on the servo either way round.

**Geometry** (`body_v1_model.py`):

| Item | D-042 (4010) | D-043 (3010) |
|---|---|---|
| Fan centre (X, Z) | 24, 105.5 | 17.5, 107 |
| Hole pattern | 32 mm (`E`) | 24 mm, Ø3.3 (`E`) |
| Screws (BO-041) | (8, 89.5), (40, 121.5) | (5.5, 95), (29.5, 119) |
| Frame web X / opening | 4–44 / R18.5 | 1–33 / R14 |
| Grille / free area | R18.5 / 605 mm² | R14 / 373 mm² |
| Collar | R19.5–21 | R15–16.5, 2.55 mm from the pod boss |
| `W41` | from X 44 | from the fan's top-front corner (X 32.5), forward of the web end (X 33), down to `J9-4` |
| Grille edge to FRONT_L / REAR_L | 14.0 / 28.4 mm | 24.1 / 25.9 mm |

The FRONT_L pigtail no longer crosses the intake path, so `check_cooling_path.py` drops that allowance.

**Cost: airflow.** A 3010 of this class moves about 3 CFM against about 5.5 CFM (`E`, both unmeasured). The first-order estimate at 8.5 W (Pi 6 W plus converters) is:

| Case | 4010 (D-042) | 3010 |
|---|---|---|
| Fan on, listing-class flow | 4.3 K | 6.9 K |
| Fan on, half that flow | 7.0 K | 10.1 K |
| Vents only, fan off | 14.7 K | 15.2 K |

That is still well under the vents-only case. With the Active Cooler holding the SoC 30–40 K over its local air, a 30–35 °C room stays under the 80 °C throttle at typical load, but the margin is about 2.5 K smaller. The bench thermal test decides.

**CAD and checks:**
- `check_cooling_path.py`: **ALL PASS**, with no fan, screw, `W41` or shell clash, a clean shell-lowering sweep and an open intake path. Its mic-distance gate rises from 12 mm to 22 mm.
- `check_body_layout.py`: all checks true after the mass rows were re-measured:
  - shell and panels 248.3 → 248.7 g;
  - frame 178.4 → 178.5 g;
  - `ENCLOSURE_FAN_3010_AND_W41` 15 → 10 g (`E`).
  - Whole robot 2,483.2 → 2,478.7 g, CoM (+18.22, +0.52, 105.62) mm. a_tip 1.693 m/s² (was 1.697) against the 1.582 minimum; head-pose bound 1.689. The harness allowance must stay forward of X −10.0 mm (was −11.3).
- `check_body_frame_fit.py`: clean. It also now treats an empty boolean (`None`) as no overlap; it crashed on that before.
- The dedicated photo-derived fan STEP and body-v1 STEP were rebuilt; their fan groups validate as closed positive solids. Not run: `check_shell_frame_fit.py` (about 70 min; the cooling check covers the shell lowering past the fan), `check_body_panel_fit.py`, and the chassis `check_layout.py`.

**BOM changed:** BO-040 is now the purchased hydraulic 3010. BO-041 is sized to the estimated Ø3.3 hole (`E`). [`BOM.csv`](BOM.csv), [`02-body/v1/BOM.md`](02-body/v1/BOM.md) and the [CAD README](02-body/v1/cad/README.md#cooling-path-d-042-d-043) are updated.

**Unverified:** the purchased fan's hole pitch and size, airflow, noise, current and mass. The noise check (`AR-61`) still applies: compare FRONT_L/REAR_L against the −Y pair with the fan on. A small 3010 runs at a higher blade-pass frequency than a 4010, so check the spectrum, not just the level.

**Next:** on receipt, measure the holes and update `ENCLOSURE_FAN_HOLE_HALF_PITCH` (`FAN_SCREW_POINTS` follow it), then run the bench thermal and noise tests from D-042.

**Fan bought (added 2026-10-04, builder):** BO-040 is the [Robu.in DC5V 3010 Hydraulic Cooling Fan with USB](https://oldwp.robu.in/product/dc-5v-3010-hydraulic-cooling-fan-with-usb-size303010mm/): 30 × 30 × 10 mm, hydraulic bearing, 100 mA max, 90 cm lead with a USB-A plug.
- **Connector:** the listing describes no detachable connector at the fan, and the photos show the wires going straight into the housing, so the lead stays on the fan. The USB-A plug is cut off. The lead is cut to about 80 mm and crimped into a new XH2.54-2P housing for `J9-4` (BO-042). Fan+ (red) goes to pin 1. Before cutting, check the delivered fan: the listing warns that it may differ from the photos. If it does have a connector at the fan, rework the BO-042 plan before cutting anything. Check polarity before crimping.
- **Hole pitch:** the listing says 26 mm. Other sellers of the same fan say 25 mm, and the usual 3010 standard is 24 mm. The CAD keeps 24 mm until the received fan is measured. 26 mm would move the screws to (4.5, 94) and (30.5, 120). They still clear the yaw servo (1.9 mm), but the top-right head would reach X 33.1, so the web end and `W41` would move about 1 mm forward.
- **STEP:** there is no vendor model. The body imports a [photo-derived 3010 STEP](02-body/v1/cad/purchased/dc5v_3010_hydraulic_usb_fan.step) from `purchased/`. Its mounting holes are estimated. A separate generic step.parts 30 × 30 × 10 fan (24 mm pitch) may be used for comparison but is not imported.
- **Listing data (builder, 2026-10-04):** a seller's spec sheet confirms 5 V, hydraulic, USB-A and a 900 mm lead. It gives the current as "100 (A)", which must mean 100 mA, and a 0.04 kg shipping weight that includes packaging and the full lead; the 10 g row (`E`) stands. No listing gives hole size, airflow, RPM or noise, and the hole-pitch claims disagree, so these come from the received fan, not a listing.
- **How to measure the holes (open, builder):**
  - *Hole size:* inside jaws of the calipers in two holes; expect about 2.7–3.4 mm. Without calipers, the largest drill-bit shank that slides through freely.
  - *Hole pitch:* across two holes on one edge, take **A** (outside jaws over the holes' outer edges) and **B** (inside jaws between their inner edges). Pitch = (A + B) / 2, independent of hole size. Repeat on a second edge; the sides should agree within 0.2 mm, or the pattern is not square and every side is recorded.
  - *Through or blind:* note whether the holes pass right through the frame.
  - *No calipers:* print a pin plate with rows at 24, 25 and 26 mm pitch and see which row drops into the fan. A ruler (±0.5 mm) cannot tell 25 from 26.
  - *Then:* update the STEP's `HOLE_PITCH`/`HOLE_DIAMETER` and `ENCLOSURE_FAN_HOLE_HALF_PITCH` (the screw points and web holes follow it), recheck the screw heads against the yaw servo and `W41` (26 mm puts the top-right head at X 33.1), size BO-041, and re-run `check_cooling_path.py`.

## D-044

**2026-10-04 · Body / head yaw stage designed: 61810-2Z bearing cartridge, printed scissor-pinion mesh, ±62° hard stops and an FFC clock-spring cassette (BO-043 to BO-050, BO-056 to BO-062; CH-083 PCB-08; new PCB-14; W37, W42, W43) · ACTIVE; DESIGN in CAD, checks green; HOLD on parts, printed coupons and the B1/B4 and cassette bench tests**

**Decision.** The builder chose two things for the yaw stage on 2026-10-04:
- **FDM-printed gears for the first build.** They accept creep and wear as a bench finding, and will move to metal or PA12 later if they fail.
- **An FFC clock-spring cassette** for the head cables, rather than a loose-wire loop or leaving the volume reserved.

Everything else here fills the open items in the old envelope stage: the 50 g bearing placeholder, the preload spring and clip, the clock-spring, the tooth and material spec, bearing and servo retention, and load and life.

**What fixed the layout.** The 1:1 spur pair (m1 z37, pitch Ø37) sits under the head disc (plate underside Z 151). Its pinion, at (16, 37), reaches in to R17.5 from the yaw axis. That has three consequences:
1. **The inner ring rotates.** A rotating cup on the outer ring would have to pass through the pinion.
2. **The order is fixed.** Nothing stationary can be lowered past an installed pinion, and the disc hides everything under it. So the order is: cartridge, then pinion, then head disc, all from above with the shell on.
3. **The disc screws go in from above,** with the head's tilting assembly off (head README service step 5).

**Bearing (BO-044).** A **61810-2Z / 6810ZZ**, 50 × 65 × 7: C 6.76 kN, C₀ 6.8 kN ([SKF via RS](https://uk.rs-online.com/web/p/ball-bearings/2076972)), about 55 g (`E`). It is in India as the [Koyo 6810ZZ on Moglix](https://www.moglix.com/koyo-deep-groove-bearing-6810/mp/msn8580ypj8492) (₹955, on request).
- It fits the old Ø50/Ø66 × 7 reserve.
- It is **shielded, not sealed**: 2RS contact seals add about 0.015 N·m (`E`), which is more than the yaw servo's 8% margin.
- Head CoM is 82 mm above the bearing. Static safety s₀ is 17 or more in every case, including a 100 N fall on the head at 100 mm and lifting the robot by the head at 3 × its weight. L10 is effectively unlimited.
- The weakness of a single deep-groove bearing is **tilt play**, about 0.1° (about 0.2 mm at the crown). It shows once the moment exceeds about 0.17 N·m, which is head weight × dm/2. Measure it.

**Cartridge (bench-built, lowered into the frame plate).**
- **Frame plate:** the ring grows R33.5 → R44, 1 mm inside the R45 shell opening. It is bored R28 and pocketed R36.6 down to Z 135.5. It has three post notches, three M3 inserts at R40 and the drive-hub hole.
- **Housing (BO-057):** seat lip, wall and an R36.5–44 flange. Three ISO 7380 M3 × 6 screws hold it from above.
- **Bearing seat:** the bearing sits at Z 137–144, 1 mm into the plate. That gives the clamp ring 1.6 mm and the hub shoulder 1.8 mm under the pinion.
- **Clamp ring (BO-049):** now stationary. It holds the outer ring with three M2 × 8 screws, at 0°, 135° and 225°, outside the pinion's shadow.
- **Hub (BO-045):** one print with:
  - the driven gear;
  - a shoulder on the inner ring;
  - an R18–25 spigot in its bore;
  - an R12.15 bore that pilots the disc's R12 hub;
  - three M3-insert bosses at 210°, 270° and 330°. Hub features above Z 145.8 stay outside the band the pinion sweeps within ±62°.
- **Rotor (BO-058):** clamps the inner ring up against the shoulder with three M2.5 × 8 screws into the spigot. It also carries the FFC drum and the stop dog. Uplift path: rotor → inner ring → balls → outer ring → clamp ring → housing → flange screws (24 N per screw at 3 × robot weight).
- **Hard stops (RP-01 P08):** the dog at 270° meets bumps at 200.1° and 339.9° at ±62°, with 2.7 mm of engagement at R29. At a 2 N·m hand twist the bump sees 12 MPa of shear. Usable travel is ±55°; set the XC330 position limits to ±58°.

**Gears and preload (BO-045, BO-046, BO-048, BO-056, BO-047).**
- **Tooth form:** m1, z37, 20° full-depth involute, profile shift x = 0. Contact ratio is 1.70; tip thickness about 0.7 mm. Both gears are thinned for 0.15 mm nominal backlash (0.46° if the scissor were absent), so FDM error does not bind the fixed half. The CAD carries real involute teeth. The mesh check finds no interference over a full pitch, with a 0.072 mm running gap.
- **Pinion halves:** two 2.0 mm halves (were 2.4). They leave 0.6 mm over the hub shoulder, 0.8 mm over the clamp ring and 0.4 mm under the disc.
  - The sprung half sits below, free on the shaft, on a printed 0.2 mm thrust land.
  - The fixed half sits above. It is keyed by a D-flat and held by an M2 countersunk screw into the shaft end.
- **Preload spring (BO-048, custom):** music wire Ø1.2, OD 8, 4 coils, about 0.25 N·m/rad. It takes about 51° (5.25 teeth) of wind-up for 0.22 N·m, at 1.49 GPa bending (`E`, against about 1.6 GPa allowed). It sits on the drive hub's collar, 0.5 mm off the bearing OD.
- **Wind-up and assembly:** a peg on the fixed half, in an arc slot of the sprung half, holds the wind-up off the mesh. With 0.5 mm lead-in chamfers, the pinion drops into mesh without a pin under the disc.
- **Shaft and drive hub:** the shaft (BO-047) is Ø5 h6 steel. The printed drive hub (BO-056) goes on the horn's four Ø1.6 holes on a 12 mm PCD.
- **PETG tooth stress (Lewis, `E`):** 15.5 MPa at preload alone, 25 MPa at peak demand, 37 MPa at the servo current limit.
  - The sustained preload will creep the teeth. The spring follows that creep and loses only about 0.0013 N·m per 0.1 mm.
  - Move to metal pinion halves if B4 lash or wear fails; the CAD allows a drop-in swap.
- **Servo side load:** 8.7 N at rest from the preload separating force, and 13.3 N at peak. That is about 0.2 N·m at the XC330 output, which ROBOTIS does not rate.
- **Drag:** scissor mesh friction is estimated at about 0.02 N·m. On the RP-01 paper screen it alone could use up yaw's 8% margin. B1 decides.

**Servo mount (BO-043, BO-061).** The XC330 hangs from a pad under the plate, fused into the main frame print. Its four case screws are lengthened to M2 × 26 (`E`, stock + 4 mm) into pilots in the pad. It goes in from below before PCB-09, with the drive hub and shaft already on the horn.

**FFC clock-spring cassette (BO-050, BO-059, BO-062).**
- **Location:** under the plate, R ≤ 23.5, Z 120–133.2. That is 13 mm over the real cooler top (Z 107), so the 10.5 mm headroom rule holds.
- **Cables:** three 22-pin 0.5 mm FFCs (11.5 mm wide, 0.5 A per conductor `E`) run on edge in a 12.2 mm band. They form a rolling loop between the drum (R13.7) and the stator wall (R22.1), with an R4.2 U-turn (about 0.7% copper strain, `E`).
  - **W42 power:** the three `J8-1` pairs on 7 + 7, 2 + 2 and 2 + 2 conductors.
  - **W43 sideband:** the `J8-3`, `J8-5` and `J8-4` signals, spares dropped.
  - **W37 CSI:** a Raspberry Pi 5 camera cable.
- **Travel:** the loop is sized for ±90°, beyond the stops. Neutral wraps are 120°/120°; at ±90° they run 64–176° inner and 86–154° outer.
- **Exit:** the FFCs leave at 300°. The CSI drops to the Pi; W42 and W43 go to two new ZIFs, `J8-6`/`J8-7`, on PCB-08's +X extension.
- **Rotor end:** the inner ends rise through the drum core to **PCB-14**. This is a new Ø35 ring board in the hub, on HOLD, where the head harness demates with the disc off.
- **Mounting:** the stator hangs from the housing on three posts at 45°, 150° and 270°. The 30° post moved because the front upper cross rail sits at X 45.5. The posts pass notches in the plate bore.

**Assembly (shell on).**
1. **Bench:** bearing into the housing, then the clamp ring, the hub and the rotor. Then PCB-14 and the FFCs, then the cassette stator.
2. Servo from below, before PCB-09.
3. Plug `J8-6`/`J8-7` and the CSI through the R28 bore, lower the cartridge, and screw the flange down.
4. Drop the pinion onto the shaft and fit the fixed-half screw.
5. Plug the head harness into PCB-14 and screw the disc and yoke to the hub (3 × M3 from above). Then fit the tilting assembly.

**Mass.**
- **`BODY_YAW_STAGE`:** **150.3 g** at (14.81, 7.81, 136.22), from the solids (was an 89 g estimate at (16, 13.5, 134.3)). The bearing 55 g and servo 23 g are `E`/`D`; the FFCs (4.5 g) and PCB-14 (3 g) are `E`.
- **`BODY_PRIMARY_FRAME`:** 169.18 g, −9.3 g. The plate bore and pocket remove more than the ring and pad add.
- **Whole robot:** 2,530.7 g at CoM (+18.10, +0.51, 106.32). a_tip is **1.670** m/s² against 1.582 (head-pose bound 1.667). The 95 g harness allowance must now stay forward of **X −4.3 mm** (was about −11). That margin is shrinking.

**Checks.**
- New `check_yaw_stage.py` (about 5 min). It covers fit, a ±61° sweep with the counter-rotating pinion, the stops at ±61.5/±62.5°, the mesh over one pitch, the cartridge lowering, the pinion drop, the axial gaps, the load, spring and FFC-loop estimates, and the mass-row match.
- `check_body_layout.py`: all true.
- `check_body_frame_fit.py`: clean. `check_compute_mount.py`, `check_cooling_path.py`: ALL PASS. `check_mic_mounts.py`: ok. All include the new yaw parts as fixed parts.
- `check_body_panel_fit.py`: clean, after a one-line fix to its overlap helper. It crashed on build123d's `None` for an empty intersection, which the new yaw parts' boxes triggered.
- `write_outputs.py`: re-run.
- Not run: `check_shell_frame_fit.py` (about 70 min; the shell opening and roof are unchanged, and the plate ring stays inside them), the chassis `check_layout.py`, and the `body-v1.step` rebuild.

**Interfaces to the head (03-head / RP-01 Layout 04, not edited here).** The disc needs:
- three Ø3.4 holes at R22, at 210°, 270° and 330° about the yaw axis, for M3 screws into the hub inserts;
- its R12 hub to pilot in the R12.15 gear bore;
- the head harness to end in connectors that plug into PCB-14 through the disc bore.

The yaw-carried mass tree does not include the hub, rotor, inner ring or PCB-14. Their yaw inertia is under 1 × 10⁻⁶ kg·m², against 0.00128 for the head.

**BOM.**
- BO-043 to BO-050 are rewritten.
- New rows:
  - BO-056 drive hub;
  - BO-057 housing;
  - BO-058 rotor;
  - BO-059 cassette stator;
  - BO-060 cartridge fasteners;
  - BO-061 servo screws;
  - BO-062 PCB-14.
- CH-083 (PCB-08) gets the two ZIFs.
- 05-harness: W37 changed; W42 and W43 added. 04-pcbs: PCB-08 updated and PCB-14 added.

**Open:**
- **Buy and measure:** BO-044 (weigh it; measure tilt play at the crown) and the BO-048 spring (rate and wind-up). Confirm the stock XC330 case-screw length (BO-061) and that the horn screws hold in its Ø1.6 holes.
- **Print coupons:** the hub spigot and housing fits on a real bearing, the gear teeth, and the chamfered drop-in mesh.
- **Bench, RP-01:**
  - B1: drag and current through the mesh, and the yaw margin.
  - B4: lash through the scissor (≤0.25° best case).
  - XC330 side-load endurance with the pinion fitted.
  - 2 N·m stop proof and 3 × robot-weight uplift proof.
- **Cassette:** 100k ±55° sweeps with the CSI streaming (no frame errors), plus W42 voltage drop at 1 A and at the stall transient.
- **PCB-14 and PCB-08:** choose the head-side connectors with the head harness, and lay out both boards (ZIF pin order).
- **Head:** add the disc holes and record the interface in 03-head.
- **Stability:** weigh the harness and keep its centroid forward of X −4.3 mm.

## D-045

**2026-10-05 · Body / service-panel internal frames (BO-022, BO-023, BO-053; BO-031; BO-063 registered) · ACTIVE; DESIGN in CAD; HOLD on the panel-boss coupon and the shell print**

**Decision:** the front and rear internal panel frames are **printed as part of the shell** (BO-019). They are not separate prints and are not bonded. Each boss takes an **M3 × 6 heat-set insert** (BO-063, the BO-030 article), and the BO-031 M3 × 8 machine screws thread into it. This closes BO-053.

**What the frames are.** Each service opening has a 2.4 mm plate behind the end wall. It reaches 1 mm past the panel outline and 12 mm inside it, and carries the four panel bosses. The panel laps a 2 mm land round the opening; its screws pull it onto that land.

**Why part of the shell:**
- **Assembly.** A frame is larger than its opening, so it can never be fitted through it. It has to enter the body with the shell, and with the panel off it has to stay where it is. A loose frame cannot do either.
- **Bond (rejected).** The only bond area is the 3 mm overlap band on the inner skin. That means PETG-to-PETG adhesive on layer lines, a fixture to hold the alignment, and still a separate supported print for each frame (3.8% / 3.1% support upright).
- **Screws into the skin (rejected).** That needs more bosses in a 2.4 mm skin and more parts, for a frame that only carries its own weight and the screw clamp.
- **Cost of the choice: printability.** Fused into the roof-down shell, the frames add about 1,330 mm² of unsupported overhang (2.19% → 2.94% of the surface by my 45° triangle-normal measure; the earlier DfAM tool gave 3.0% for the shell alone). Most of it is the frames' 2.4 mm edges facing the openings and the boss undersides, so the supports come out through the openings. A damaged boss now means a shell repair, which the inserts make unlikely.

**Why inserts.** BO-031 is a machine screw, which cannot thread into a printed Ø2.8 hole. The panels also come off for service: the speaker, the power button, the charge inlet and PCB-02 access.

**CAD changed** (`02-body/v1/cad/body_v1_model.py`):
- New `panel_internal_frame(face)`, fused into `body_shell()`. `panel_mount_hardware()` no longer returns the frames; it now holds the eight inserts, the wedge washers and the screws.
- **Bosses:** the tail behind the frame grows from 2.6 to 3.5 mm (`PANEL_BOSS_TAIL`). The sloped panels had shortened the upper bosses to about 6.2 mm, less than the insert pilot; they are now 7.07–7.65 mm.
- **Holes:** each boss has an Ø4.3 × 6.5 insert pilot (`FRAME_INSERT_RADIUS`, `PANEL_INSERT_PILOT_DEPTH`) and an Ø3.2 relief beyond it. This replaces the Ø2.8 through hole. The wall round the pilot is 2.35 mm.
- **Screw model:** the shank now starts at the head seat on the wedge washer, not at the panel's outer face. Thread in the insert is 3.6–4.4 mm, and the tip stops 3.2–3.5 mm short of the boss end.
- **Assembly:** the frames lower with the shell. A sweep of both frames down the lowering path is clean except for PCB-13, which is installed later with the rear panel.

**Checks:**
- `check_body_panel_fit.py` gains the insert and screw stack per boss, insert-press access (a Ø6 iron tip straight through the opening) and screw/insert-against-shell overlap: **ALL PASS**.
- `check_charge_inlet.py`, `check_power_button.py` and `check_cooling_path.py` now test against `panel_internal_frame("REAR")` as well as the shell.
- `check_shell_frame_fit.py` now leaves PCB-13 out of the fixed parts during lowering, like the power button, because both arrive with the rear panel.
- `check_charge_inlet.py`, `check_power_button.py` and `check_cooling_path.py`: **ALL PASS**.
- Mass: shell and panels measure 248.62 g against the 248.7 g `BODY_SHELL_AND_PANELS` row, so the row is unchanged; the eight inserts are in the fastener allowance, as before. `check_body_layout.py` itself could not run: it fails with `KeyError: 'RP01_HEAD_LAYOUT04'` on the in-progress head-v1 rename in the working tree, which is not part of this change.
- `check_shell_frame_fit.py` (about 70 min, the first run since D-040): **ALL PASS**. The shell, with both frames fused, is one solid. The lowering, frame, chassis, joint-hardware, driver-access and wheel-arch results are all empty.

**BOM changed:** BO-022 and BO-023 become features of BO-019. BO-053 is closed (DESIGN). BO-031's release check names the inserts. New row BO-063: eight M3 × 6 inserts. [`BOM.csv`](BOM.csv), [`02-body/v1/BOM.md`](02-body/v1/BOM.md) and the [CAD README](02-body/v1/cad/README.md#panel-internal-frames-and-inserts-d-045) are updated.

**Open:**
- **Panel-boss coupon:** print a frame corner with two bosses in the shell's roof-down orientation. Press BO-063 inserts and check the 2.35 mm wall does not split. Then do a pull-out test and 20 panel removals with BO-031.
- **Shell print:** confirm the supports at the frame edges and boss undersides, and re-measure the shell's support area with the DfAM tool.
- **Torque:** set a hand-tight limit for the M3 × 8 into the inserts once the coupon has been tested.

## D-046

**2026-10-07 · Head / pitch and roll actuators (HD-001 registered; overrides RP-01 `ACT-01` for pitch and roll) · SELECTED; HOLD on the head CAD re-fit, the head-rail setpoint and bench B1/B4**

**Decision.** The builder chose the **Feetech STS3045M** for both pitch and roll, on cost (₹3,661 incl. GST, [Evelta](https://evelta.com/sts3045m-6v-6kg-cm-360deg-metal-gear-digital-servo-motor/), 5 in stock on 2026-10-07) and accepted the head remodel it needs. The fastest pitch moves are capped at **70% speed**; roll keeps full speed. Yaw stays BO-043 (XC330-M181) for now; see Open.

**Part (`D`, Evelta listing and [Feetech specification](https://pages.switch-science.com/comparison/files/feetech/serial-sts/STS3045M_datasheet.pdf)):** 4.8–7.4 V; 6 kg·cm (0.59 N·m) stall and 2 kg·cm (0.20 N·m) rated at 6 V; 0.133 s/60° (75 rpm) no-load at 6 V; 1.4 A stall; 120 mA no-load; **34.8 ± 1 g**; 36 × 15 × 29.2 mm case and 48.8 mm mounting-ear span; aluminium case, metal gears, coreless motor, ball bearings; 12-bit magnetic encoder, 360°; half-duplex TTL serial, 38.4 kbps–1 Mbps; 25T/Ø5.9 mm spline and M3 × 6 horn screw. The specification **does publish 1:281 reduction and ≤0.5° gearbox backlash**; rotor/gear inertia remains unpublished (`U`). Its table says 4.0 V minimum while Feetech's product page says 4.8 V; use 4.8 V until the received revision is checked.

**Why (paper screen, `E`).** Demands are the RP-01 `actuator-screen-01.md` values with the high internal-inertia bound; a k× slower move cuts the inertial terms by k², gravity unchanged. Capability is the straight-line endpoint proxy × 0.86 (the XC330 graph-to-proxy ratio), at the 5.23 V worst servo terminal of the proposed 5.5 V rail (below).

| Axis | Demand | STS3045M capability | Ratio |
|---|---|---|---|
| Pitch, 100% | 0.249 N·m at 39.3 rpm | about 0.20 N·m | **fails** |
| Pitch, 70% cap | about 0.145 N·m at 27.5 rpm | about 0.25 N·m | about 1.7× |
| Pitch, RMS | 0.075 N·m | 0.20 N·m rated | 2.6× (XL330-M288 about 1.4×) |
| Roll, 100% | 0.129 N·m at 30 rpm | about 0.24 N·m | about 1.8× |

- **Against the XL330-M288** (the cheaper Dynamixel option): similar torque, but metal gears and a stated continuous rating suit pitch's constant gravity load, and the India price and stock are known.
- **Against the XC330-M288 (`ACT-01`):** about one third of the price; lower torque, which the 70% pitch cap pays for.

**Mass (`E`, not yet in the mass tree).** +11.8 g per servo against the 23 g XC330 rows. Pitch-carried 470.3 → about 482 g; yaw-carried 594.0 → about 618 g (C2 20 g case). Raising the robot CoM by about 0.8 mm puts a_tip near 1.66 m/s² against the 1.582 minimum (D-044: 1.670), by a rough height-only scaling. Re-run the mass tree after the CAD re-fit; do not edit the rows by hand.

**Consequences.**
- **Head-rail voltage.** The servo's 4.8 V minimum is above the rail's worst-case 4.74 V at the terminal (`LTC3119` 4.891–5.109 V less the 150 mV drop, RP-02 §5.4). Proposed: raise `PB-HEAD` to **5.5 V** (about 5.23–5.62 V at the terminals). That fits both the STS3045M (4.8–7.4 V) and the XC330-M181 yaw (3.7–6.0 V) if yaw shares the rail. The 5.74 V regeneration clamp then sits too close, so move it to about 5.9 V. If yaw leaves the rail (ST3215-HS on its own 12 V rail), 6.0 V is the better setpoint.
- **Bus protocol.** Pitch and roll now speak Feetech, not Dynamixel 2.0. The physical layer stays half-duplex TTL, but C2's servo driver, the PCB-12 servo interface and the RP-02 `BD-13` per-axis protection (Dynamixel Current Limit, Operating Mode 5, Shutdown 0x35, Bus Watchdog) must be redone with Feetech's protection-current, overload and torque-limit registers.
- **Head CAD.** The case is longer, thinner and taller than the XC330, with a different mounting pattern. Re-fit the pitch-servo saddle and yoke adapter and the roll-servo mount on the torsion box, then re-run the P07 FEA (41 Hz pitch frame, 84 Hz roll mount), `check_revision.py`, `check_fasteners.py` and the mass tree, and hand the new axes and masses to body v1.
- **Storyboard.** The 70% pitch cap re-authors the fastest pitch moves (laugh reversal, startle); gate P07 needs the slower trajectory re-screened.

**BOM.** New row **HD-001** (qty 2), the first head row.

**Open:**
- **Yaw servo.** Keeping the XC330-M181 means two protocols on two buses. The ST3215-HS on a 12 V yaw-only rail on PCB-03 would make the system all-Feetech and widen yaw's margin, but needs the rail, a yaw-bay CAD re-fit and a lash check. Decide after bench B1/B4.
- **Bench B1** (one STS3045M against a pitch inertia and CoM mock-up, 0.00079 kg·m², at 5.23 V): measured current and margin on the 70% trajectory.
- **Bench B4:** loaded and unloaded lash with an external angle reference; dead-zone registers at minimum first.
- **Datasheet:** confirm the mounting drawing, gear ratio and protection registers from the Feetech datasheet before the CAD re-fit.
- **Rail:** record the 5.5 V setpoint and clamp change in `04-pcbs/power-boards.md` before the PCB-03 schematic.

## D-047

**2026-10-07 · Body / yaw servo (BO-043; affects BO-056, BO-061, PCB-03) · SELECTED; provisional case fit found; HOLD on mount/hub integration, the yaw rail and bench B1/B4**

**Decision.** The builder chose the **Waveshare ST3215-HS** (20 kg·cm, 106 rpm) as the yaw servo, replacing the D-044 XC330-M181-T. It runs from a **12 V yaw-only rail** on PCB-03. This closes the D-046 open item on the yaw servo and the bus protocol: the robot uses the Feetech protocol on all three axes.

**Priorities used, in order:** (1) speed at 63 rpm while accelerating the head's 0.0013 kg·m², since yaw is the tightest axis on paper; (2) lash, which shows most on yaw (no gravity preload, and the spur pair is outside the servo's loop); (3) fit in the yaw bay; (4) one protocol; (5) cost. Mass does not matter, because the servo is body-fixed.

**Part (`D`, Waveshare listing):** 6–12.6 V; 20 kg·cm stall and 0.094 s/60° (106 rpm) no-load at 12 V; 2.4 A stall, 240 mA no-load; kt 8.3 kg·cm/A; 68 g; metal gears; 360° magnetic encoder (4096 counts); Feetech serial bus, 38.4 kbps–1 Mbps. Case about 45 × 25 × 35 mm (`E`, STS3215 class; confirm). Gear ratio and lash are not published (`U`). ₹2,049.99 at [ThinkRobotics](https://thinkrobotics.com/products/st3215-hs) as a pre-order on 2026-10-07; $21.99 at Waveshare.

**Comparison (`E`, straight-line endpoint proxy × graph factor, demand 0.22 N·m at 63 rpm including the D-044 mesh drag):**

| | XC330-M181 at 5.5 V rail | ST3215-HS at 12 V | STS3250 at 12 V |
|---|---|---|---|
| Speed margin | about 16–27% | about 40% or more | about 6–14% |
| Lash | unpublished | unmeasured; STS3215 family 0.6–1.3° | 0.13° / 0.33° loaded (Robonine) |
| Protocol | Dynamixel | Feetech | Feetech |
| Price | ₹11,459 | ₹2,050 | ₹6,100 |

**Fallbacks.** If bench B4 shows the HS over about 0.5° loaded, yaw moves to the **STS3250** (same rail and protocol, similar size class to confirm). If no Feetech case fits the yaw bay, yaw returns to the **XC330-M181-T** on the 5.5 V head rail, with Dynamixel as a second protocol.

**Consequences.**
- **Rail:** a second `LTC3119` on PCB-03 boosting to 12 V for yaw only (about 2 A from a low pack, `E`); set the servo's protection current below it. Nothing new crosses the FFC cassette.
- **CAD:** the case is about twice the XC330's volume. The frame pad, the BO-056 drive hub (made for the XC330 horn's 12 mm PCD) and the BO-061 case screws are re-designed after the fit check. Neighbours: the D-043 fan web (1.1 mm), the PCB-09 strip, the +Y mic ports (BO-005 noise check) and the Pi cooler.
- **Yaw-bay correction and trial route (2026-10-07):** the first fit screen omitted PCB-09's over-header strip. At the existing pinion centre the 0° case overlaps that strip by 156.892 mm³, its GPIO socket by 342.194 mm³ and the Pi STEP by 310.502 mm³ with the original compute layout. The [corrected check](02-body/v1/cad/feetech-yaw-fit.md) found no usable case clocking with that layout. An exact-solid follow-up found a provisional packaging route at the **same R37 pinion centre and height**: delete the XC330 pad, move Pi/cooler/PCB-09 −Y 6 mm, reshape PCB-09's outer bay +X 6 mm, and join a new U-cradle to the frame. The HS STEP has zero solid overlap with the trial frame, tray, Pi, cooler, PCB-09, housing, cassette and shell. The candidate cradle/frame is one valid solid. This is not a released mounting or drive design; prove the retainer, shaft datum/BO-056 coupling, altered Pi/PCB-09 hardware, harness, assembly and yaw sweep before switching the live body source. The HS STEP's main-case topology is invalid, so confirm on received hardware.
- **Yaw-rail alternative:** 11.1 V nominal gives more braking-clamp headroom than 12 V but reduces the current provisional torque margin to about 2.53× nominal, about 2.28× at the assumed low terminal corner. [PCB-03 power delta](04-pcbs/power-boards.md) records the calculation; retain 12 V as the selected paper target until the B1/B2 curve and braking measurements choose the setpoint.
- **Mass:** +45 g in the body near the yaw plate. Re-run `BODY_YAW_STAGE` and a_tip after the CAD re-fit.
- **Firmware:** the yaw servo moves to the Feetech driver with HD-001.

**BOM.** BO-043 rewritten in [`BOM.csv`](BOM.csv) and [`02-body/v1/BOM.md`](02-body/v1/BOM.md); listed in [`03-head/v1/BOM.md`](03-head/v1/BOM.md) with the actuator set. BO-056 and BO-061 are unchanged until the re-fit.

**Open:**
- **Yaw-bay integration:** turn the non-clashing trial into a fastened, serviceable frame/compute/PCB-09 assembly and re-run the D-044 checks before any build order.
- **Bench B1:** one HS on a yaw inertia mock-up with the scissor mesh, bearing and cassette fitted; log current and position.
- **Bench B4:** loaded and unloaded lash with an external angle reference, dead zone at minimum.
- **Rail:** record the 12 V yaw rail in `04-pcbs/power-boards.md` with the D-046 5.5 V head rail.

## D-048

**2026-10-07 · Body / ST3215-HS yaw integration and compute-stack shift (BO-043, BO-056, BO-061; CH-084 PCB-09, CH-086 PCB-10 headers, PCB-04 plug reserve; W15) · ACTIVE; CAD packaging screens clean; HOLD on the specified plug, torque/gear proof, the received HS, head re-balance and bench B1/B2/B4**

**Decision.** The builder asked to make the Feetech yaw servo (D-047) work by rearranging the body rather than falling back to the XC330. The ST3215-HS stays on the D-044 pinion axis and gear height. The compute stack moves to make room and to pay back the tip margin.

**Correction to the earlier fit screens.** `check_feetech_yaw_fit.py`, `check_feetech_yaw_relocation.py`, `check_feetech_yaw_compute_shift.py` and `feetech_yaw_cradle.py` put the STEP origin on the pinion. The horn axis is **25.5 mm from it**: Waveshare's 2D drawing (`ST3215-2D.zip`, sheet "SCS215") puts the Ø19.2 horn 10.11 mm from the case end, which is STEP X −25.5 after the −90° turn about X. The Ø2.5 holes the trials treated as case screws are the horn's four holes on a 7.11 mm radius. Turned 180° about the true axis, the case envelope is almost the same box (X −19.1…26.1 against −19.6…25.6), so the packaging conclusion held, but those trial results are superseded by the live-model checks below.

**Servo installation (`body_v1_model.py`, `yaw_servo_st3215_hs()`).**
- **Orientation:** horn up on the pinion axis (16, 37), case running −X (`YAW_SERVO_CLOCK_DEG` 180).
- **Height:** overall purchased-STEP maximum Z 122.4, **7.6 mm below** the old top datum; this is not the case seating face. The drawing puts both bus plugs in a recess on the horn face, so they plug in from above and need about 10 mm under the plate. The offset also keeps the bottom (idler) disc above the PCB-03/04 plug layers (Z 84.3).
- **Mount:** four M2 × 8 screws, from above, into the horn-face corner holes (STEP: Ø1.6 × 2.8 deep, in a step 2.58 mm below the case top). They clamp four Ø4.8 pillars of a frame-integral ring. Two side walls carry the ring up to the pad under the plate, which grows to X −21…25.5, Y 23.8…50.2. A window (X −15.6…4.9, Y 28.8…45.2) over the plug recess opens to −X for the W15 exit. Driver holes run up through the pad and plate. The two screws inside R44 sit under the cartridge flange, so **servo replacement needs the cartridge out**.
- **Drive:** BO-056 hub r 8.8 from the horn face (Z 121.85) to Z 136.2, with a Ø12.4 pocket over the horn's centre boss. Four horn screws at 10.1° + 90°k (Ø2.5 horn holes: M2.5 or M3 to confirm on the received horn).
- **Proposed torque ceiling:** `YAW_SERVO_TORQUE_LIMIT_NM` 0.30 is a CAD stress assumption, not an implemented or measured limit. The Feetech percentage register must be calibrated under load at the required 63 rpm; an effective 0.30 N·m ceiling leaves only about 1.36× the 0.22 N·m paper peak demand. The PETG pinion-half Lewis estimate is already 15.5 MPa at preload alone against its 15 MPa screen flag, and rises to 36.7 MPa at this ceiling. Full 1.96 N·m stall would be much worse. Prove the gear/stop load path or redesign the teeth and protection before release.

**Compute stack (`COMPUTE_SHIFT_X/Y` = +10, −6 mm).**
- **What moves:** the Pi 5, the Active Cooler, the four tray bosses and inserts, the push-pin keep-outs, PCB-09 (all parts) and its plug reserves, J9-4, and the Pi USB-C plug reserve. The pigtail drop moves +10 mm in X only.
- **Why −6 Y:** the Pi's GPIO-header edge was under the servo case.
- **Why +10 X:** about 112 g moves forward to recover the tip margin the Feetech servos cost.
- **Tray (BO-033):**
  - its +Y edge stops at **Y 23.5**, 1.1 mm inboard of the servo, so it still slides in from the front;
  - the front grows to X 80.5;
  - the front screw moves to (64, −41.5) on a new −Y ear, with the column to Y −45;
  - the rear +Y screw, block and column move to (−24, 17.5), because the old corner swept under the lowered servo;
  - the vent row at Y 21 is dropped.

  Tray print 20.58 g (was 23.1 g).
- **PCB-04 (paper):** its top-entry plug reserve now starts at X −14 (was −26), so **J4-6 must sit forward of X −14**. The tray block uses the freed corner.
- **C3 carrier PCB-10 (paper):** the Z 92 GH row is repacked to start at X 6.5, right of the moved USB-C plug: J10-7, J10-3, J10-4, J10-10, J10-12. **J10-11 (spare, not fitted since D-041) loses its header.**
- **Harness:** the `HARNESS_SIGNAL_TRUNK` reserve moves 4 mm toward −Y, clear of the servo's bottom disc.

**Checks (D-048 model; reviewed 2026-10-08).**
- `check_yaw_stage.py` **ALL PASS after mount-axis correction**: no stage, sweep, cartridge-lowering, pinion-drop or moving-part clashes, and the frame is one solid. All four case-screw axes match the vendor STEP holes; only horn-screw/horn engagement is informational.
- `check_compute_mount.py` **ALL PASS** (2026-10-08) after the plug fix below. It first failed on the Pi power-plug reserve against the C3 DevKitC (0.120 mm³) once the missing fixed-part test was added. Tray retention, front-slide sweep and driver paths remain clear. The under-tray harness reserves overlap the tray as recorded below.
- `check_cooling_path.py` current-source rerun **ALL PASS**; `check_charge_inlet.py` and `check_power_button.py` originally passed.
- `check_body_frame_fit.py` current-source rerun **clean**; `check_body_panel_fit.py` and `check_mic_mounts.py` originally clean.
- `check_body_layout.py` ok, after the one-line fix D-045 recorded (the `HEAD_V1` row key).
- `check_shell_frame_fit.py` saved 2026-10-08 result is clean for the current D-048 source: no frame, chassis, hardware, lowering or driver overlaps at its sampled positions. Chassis `check_layout.py` was not run.

**Mass and stability.**
- `BODY_YAW_STAGE` is 199.4 g at (11.62, 15.0, 126.86), was 150.3 g. `BODY_PRIMARY_FRAME` is 172.59 g, was 169.18. `COMPUTE_TRAY_AND_PI_FIXINGS` is 27.07 g at (21.16, −10.44, 86.98).
- **Whole robot with the current head tree (XC330 rows):** a_tip **1.667**, worst head pose 1.663, against 1.582. The harness allowance must stay forward of **X −4.0**.
- **With the STS3045M head what-if** (`feetech-mass-whatif.json`, D-046): a_tip **1.621**, a 2.5% margin. The head-pose bound needs the head A0 re-balance first: the unbalanced what-if moves the pitch-carried CoM 1.5 mm off the axis.

**Side load (risk).** The 7.6 mm drop lengthens the pinion-to-horn lever to 26.6 mm. The moment on the HS output is **0.355 N·m** at the 13.3 N peak (XC330: about 0.2). Feetech does not rate radial load. If bench B1/B4 or endurance shows wear, add a support bearing for the hub in the pad, and drive the pinion through a compliant coupling so the servo's bearings are not doubly constrained.

**BOM.** BO-043, BO-056 and BO-061 rewritten.

**Open:**
- **Received part:** measure the HS. Check the horn-axis offset, the corner-hole positions (the drawing and the STEP differ by 0.8 mm), the step height, the horn hole thread and the plug height with cables. The official STEP has one invalid-topology case solid.
- **Mount-hole audit:** the first D-048 CAD screw axes were 0.8 mm from every STEP hole axis, and `check_yaw_stage.py` incorrectly waived the resulting screw/case overlap as thread engagement. The CAD now uses the STEP axes (X 7.7 and −16.75), and the checker rejects case-screw overlap and axis offset. The drawing discrepancy remains a received-part gate.
- **Pi power connector (fixed in CAD 2026-10-08, part to select):** the 15.4 mm sideways plug reserve clipped the C3 DevKitC by 0.120 mm³ (X −6.20…−3.73, Y −50.00…−49.69, Z 99.90…100.20); only 14 mm remains from the shifted Pi edge to the DevKitC face. HN-010 is now specified as a right-angle USB-C whose **cable exits down (−Z)** into the existing pigtail drop, body **≤ 13 mm** beyond the receptacle face. The reserve now ends at Y −47.8: 1.74 mm to the DevKitC and 2.19 mm to the nearest C3 plug (J10-7). No catalogue drawing was found for a solder-type down-exit plug, so the chosen part must be measured against this envelope.
- **Under-tray wiring:** the current `check_compute_mount.py` rerun reports 622.875 mm³ overlap with the signal-trunk reserve and 487.255 mm³ with the sensor-trunk reserve as information, not pass criteria. Re-route and check the actual cables/clips before claiming a complete installation path.
- **Assembly:** confirm the M2 driver path through the pad and plate before the cartridge, and the W15 route from the plug window to PCB-03 `J3-5`.
- **Service:** two mount screws are under the cartridge flange.
- **Head:** refit the STS3045M mounts and re-solve A0, then re-run this tip screen with the real head tree.
- **Shell:** the current-source lowering screen is clean; confirm on the first physical assembly.
- **Boards:** place J4-6 forward of X −14 on PCB-04. PCB-10 header row as above. PCB-09 outline unchanged relative to the Pi.
- **Bench B1/B4** with the pinion fitted, including side-load endurance.
- **B2 torque-speed and protection:** validate the proposed yaw torque ceiling at 63 rpm, and include a stall/fault test of the teeth and hard stops; a CAD constant does not enforce a physical cap.

## D-049

**2026-10-08 · Head / STS3045M pitch and roll installation (HD-001–HD-007; head v1 CAD, mass tree, axes; body v1 hand-off) · ACTIVE; CAD and checks complete; HOLD on received servo, horn and coupler fits, the CF leg coupon and bench B1/B4/B6**

**Decision.** Install the two D-046 STS3045M servos in the head v1 CAD. The roll servo stays on the pitch frame and drives the Ø6 spindle through a goBILDA clamping coupler. The pitch servo moves onto the pitch frame and its horn is screwed to the +Y yoke leg, so the case turns round a fixed output. This is the only arrangement that fits; the reasons are below.

**Step 0: servo model against the drawing.** The Feetech drawing (STS3045M spec p. 6) confirms the reference STEP's horn axis (6 mm off the case centre), ear slot centres (±21.3 mm from the case centre, rows 7.5 mm apart), 48.8 mm span, ears at Z 19.7–21.7 and spline tip at 33.1. Three details were wrong and are corrected: the lead exits the shaft-end face, centred (the model had it beside the case); the slot necks are 2.4 mm wide (were 4.2); the boss is Ø10.4 (was Ø9.5). No axis error like D-048's. The trial clash screen changed only in its pitch-rearward cradle value (7.7 → 10.8 mm³).

**Why pitch moved onto the pitch frame.** With the servo on the yoke, the cradle cross bar sweeps everything within 16.5 mm of the pitch axis forward and below it under combined roll and pitch, so no clocking clears the servo's 18.4 mm short-side ear (sweep map, all 360°). Carried by the pitch frame, the servo only sees roll relative to the cradle. At a 244° clocking (long side down-rear) every point clears by ≥ 2 mm on the sweep map. Axially, a servo, horn and a separate trunnion arm do not fit between the cradle flange (Y ≤ 15.9) and the leg (Y 52), so the horn bolts to the leg itself.

**Roll (`feetech.py`).**
- Servo case X −112.4…−83.2, 1.0 mm in front of the rear cover; spline on the roll axis, long side down.
- goBILDA 4001-0025-0006 (HD-004, official STEP): spline face at X −82.6, clamp boss up at neutral, M4 × 10 clamp; ISO 4762 M3 × 5 through its floor into the output (3.8 mm thread). Spline engagement 2.9 mm.
- Ø6 spindle lengthened to X −74.6…−40 (9.0 mm in the coupler bore, all of the clamp zone).
- Rear bearing moved forward: 696-2Z at X −43 and −60.6 (spacing 17.6, was 22); cartridge X −64.6…−39; rear cartridge screws to X −57.5. Coupler runs 1.0 mm from the cartridge and 0.9 mm from the retainer.
- Mount: 5 mm plate on the ears' front faces with a window round the case, ±18.7 mm wide and joined to the torsion box rear wall; its −Y upper corner is cut back for the C2 tray's service path. Ear screws drive from behind with the rear cover off.

**Pitch (`feetech.py`).**
- Servo on the pitch axis, spline +Y, case Y 18.3…47.5 (2.4 mm clear of the cradle flange), long side at 244°.
- 25T aluminium disc horn (HD-002, `E` dimensions: Ø20 disc, Ø10 hub, 4.5 total, 4 × M3 on Ø14 PCD) in a Ø20.4 × 0.6 pocket on the +Y leg, four ISO 7380 M3 × 6 from the leg's outer face, ISO 4762 M3 × 5 centre screw reached through the leg. Spline engagement 3.3 mm.
- Collar: a 6 mm XZ plate under the ears, round the case's rear-up side, joined by a web to the torsion box front wall and by a floor to the keel.
- The +Y trunnion pin, adapter and the frame's +Y arm and web are removed. The +Y side of the head now rides on the servo's output bearings (side load: bench).
- Assembly: horn and centre screw on the servo; servo into the collar; frame lowered between the legs and pushed 0.6 mm +Y into the pocket (1.0 mm float on the −Y side); −Y trunnion pin from outside; horn screws from outside.

**Ear joints (HD-006/007).** ISO 7380 M2 × 6 on an ISO 7089 M2.5 washer (Ø6 × 0.5) into the head's M2 × 3 inserts. The slot is 3.3 mm from the case end: an M3 insert would leave 0.8–1.0 mm of wall, the M2 pocket leaves 1.4 mm. The M2 head is smaller than the slot, and a 0.3 mm M2 washer would dish over it.

**Yoke legs.** The +Y leg now carries the pitch reaction from the horn to the disc. The old 8 × 6 mm spine screened at 8.6 N·m/rad; the XC330 adapter also hung the reaction on this leg, so the earlier 41 Hz frame-only result never covered it. The +Y leg is widened inside the free corridor of the R/P swept volume (1.5 mm margin), with a foot inside the disc radius (Y 48–58) and an inboard rib; its horn pad is Ø22.4. About half its twist is in a 6 mm band just above the foot, where the swept volume limits the spine to about 8 mm, so geometry cannot stiffen it further. **Both yoke legs are to be printed in a carbon-fibre-filled filament with E ≥ 4.5 GPa along the layers** (coupon to measure).

The A0 shift moved both legs about 2.4 mm against the ears. A leg-versus-everything sweep (both legs, 56 poses) against the committed head found its +Y ear trim stack only **0.028 mm** from the leg and the −Y one 0.17 mm. Both legs now have a 1.2 mm relief band on the outer face along the trim-stack path, and their styling rails stop at Z disc+32.5 (the upper halves sit under the head and grazed the ears' amber rings). The +Y leg also has a 0.5 mm outer-face step where the skin passes. The skin, ear and cradle reliefs are still cut by the pre-D-049 legs, so no shell, ear or cradle volume changes. After these changes every leg pair is at least as clear as in the committed head (same 56-pose grid): +Y / −Y trim stacks 1.14 / 1.28 mm (were 0.028 / 0.17), amber rings 0.81 / 0.95 mm (0.22 / 0.35), skin 0.83 / 1.24 mm (0.72 / 0.72), and every new pair ≥ 1.1 mm.

**Rear trim.** Two Ø14 brass stacks at Y = roll axis ±30, 22 mm above it, on the rear cover (built equal: no roll moment; above the C2 BOOT/RESET corridor). Capacity 7.85 g (was 8.0 g on the axis).

**Mass and axes (`mass_layout.py --solve`).** The committed `mass-placement.json` was stale: the committed source gives 604.3 g yaw-carried, not 594.0 g (fabrication-audit skin and screws). D-049 against the committed source:

| | Committed source | D-049 |
|---|---|---|
| Roll-carried | 382.8 g | 388.8 g |
| Pitch-carried | 478.6 g | 535.7 g |
| Yaw-carried | 604.3 g | 648.5 g |
| Pitch inertia | 0.000807 | 0.000878 kg·m² |
| Yaw inertia | 0.001322 | 0.001438 kg·m² |

A0 axes: roll Y −1.027, Z 48.157; pitch X −42.419 (2.41 mm rearward), Z 45.551. Fresh-process residuals ≤ 0.003 mm. A solver bug (`feetech.py` was not reloaded between iterations) was found and fixed.

**Checks (head v1).** `check_revision.py` pass: 56 poses, no mechanism or harness hits, service extraction, retention, insert mouths and hard stops clean. `check_fasteners.py` pass (all M2, including the eight ear screws: 3.0 mm in each insert). `check_integration.py` pass. `motion_envelope.py`: full ±21° roll at every pitch row; lowest point Z −28.39, 4.94 mm above the disc at 1° overtravel. `check_feetech_mounts.py`: every interface fact passes: spline engagement 2.9 (roll) / 3.3 mm (pitch), centre-screw thread 3.8 mm, coupler 1.0 / 0.9 mm from the cartridge / retainer, case 1.0 mm from the rear cover, horn seated, 0.4 mm frame float beyond the pocket, horn screws 2.0 mm in the horn thread, ear-screw shanks clear of the slots, insert walls 1.4 / 1.5 mm, and all eight ear-screw driver paths clear (ISO 7380 M2: 1.3 mm key). Posed clearance: every D-049 part is ≥ 0.99 mm from every part that moves relative to it (the coupler-to-cartridge running gap measures 0.997 mm, designed 1.0, because the goBILDA STEP is 17.003 mm long); pairs that already existed are no closer than in the committed head ([baseline](03-head/v1/cad/generated/feetech-mounts-baseline.json)). Evidence: the full 7 × 8 grid (2026-10-08 22:52) for the servo, coupler, horn, frame, plate and trim parts, `check_leg_clearance.py` for both legs after their final edits, and a 3 × 3 re-run on the final geometry.

**P07 FEA (`fea/`, RP-06 method).** Frame and +Y leg in series ([results](03-head/v1/cad/fea/results.json)):

| Case | Stiffness | Frequency |
|---|---|---|
| Pitch frame, E 3.5 / 2.3 GPa | 112.5 / 74.0 N·m/rad (was 51.4) | 57 Hz frame only |
| +Y yoke leg, E 3.5 / 2.3 GPa | 49.9 / 32.8 N·m/rad (old spine 8.6) | — |
| Pitch chain, PLA 3.5 GPa | 34.6 N·m/rad | **31.6 Hz** |
| Pitch chain, PLA 2.3 GPa | 22.7 N·m/rad | **25.6 Hz**, below 30 |
| Pitch chain, CF legs at 4.5 GPa (frame 3.5 / 2.3) | — | **34.3 / 31.5 Hz** |
| Roll mount, 3.5 / 2.3 GPa | 455.9 / 299.6 N·m/rad (was 187.5) | 126 / 102 Hz |

Pitch is clamped at the pitch-servo ear seats with the couple on the cartridge seat; roll at the −Y trunnion and pitch ear seats with the couple on the roll ear seats; the leg on its foot with the couple on the horn pocket. Leg mesh convergence 1.4 → 1.0 mm: −0.6% (previous outline); the frame's 1.0 mm runs exceeded memory. The CF leg requirement comes from the 2.3 GPa row. Servo, horn and joint compliance are excluded (B6).

**Motion workbook (§11.3, `busy_minute.py`).** Rebuilt from the RP-01 workbook traces (validated: reproduces its RMS/peaks exactly), with the D-046 70% pitch cap (laugh reversals 145/175/160 ms, startle recoils 260/360 ms, rounded up) and the D-049 inertias. Nominal A0, output side:

| Case | Pitch RMS / peak | Roll RMS / peak | Yaw RMS / peak |
|---|---|---|---|
| BC-60 | 0.0086 / 0.0475 N·m (Yes, 80°/s) | 0.0034 / 0.0247 | 0.0197 / 0.1183 |
| MV-60 | 0.0053 / 0.0294 | 0.0019 / 0.0137 | 0.0122 / 0.0722 |

STS3045M moving-curve margins (proxy at the 5.23 V terminal, reflected motor inertia 0.000869–0.001974 kg·m², with and without the 0.020 N·m bias): pitch **1.71×** worst (BC-60 Yes at 24.7 rpm), roll **3.04×**. Yaw output torque rose 34% with the heavier head (HS ratio unknown).

**Body v1 hand-off.** Dry run, then accepted: `check_body_layout.py` all checks true; a_tip **1.628** neutral and **1.589** worst head pose against 1.582 (was 1.667); the unweighed 95 g harness/fastener allowance must stay forward of X **18.06** (assumed 20). Head yaw-carried CoM is about 2.4 mm off the yaw axis, toward +Y. `check_yaw_stage.py` ALL PASS. The head origin moved 2.41 mm +X relative to the body with the pitch axis.

**BOM.** HD-002/003 rewritten, HD-004–HD-007 added.

**Open:**
- **Received parts:** measure the pitch horn before printing the +Y leg (pocket, PCD, hub, web); fit the goBILDA coupler on the STS3045M spline (H25T vs Feetech 25T); output thread depth ≥ 4.2 mm; ear tab-root fillet against the Ø6 washer.
- **CF leg coupon:** modulus ≥ 4.5 GPa along the layers, or revisit the leg.
- **Tip margin:** 0.4% at the worst head pose. Weigh the harness and fasteners, keep them forward of X 18.1, or add body ballast.
- **Side load:** the +Y side of the head rides on the pitch servo's output bearings; include in B1/B4 endurance.
- **Bench B1/B4/B6:** loaded motion, lash (spline, horn and coupler included), loaded modes.
- **Firmware sign:** pitch CAD angle = −(servo output angle about +Y), because the case turns; roll CAD angle = +(output angle about +X). Confirm the Feetech count direction before writing limits.
- **Harness:** both 5264 leads leave short-side end faces near the case bottom; only 8–10 mm straight exits are reserved.

## D-050

**2026-10-09 · Head / yoke legs and turntable restyle after the Feetech migration (M011-Y, M012; head v1 CAD, mass tree, body v1 hand-off) · ACTIVE; CAD and checks complete; HOLD on the D-049 CF leg coupon and print orientation**

**Why.** After D-046 to D-049 the builder found the robot uglier. A before/after render of the integrated model (`6ce00df` against `54a3533`) showed what changed and what did not:
- **The +Y yoke leg (D-049)** was the real regression. Its spine and inboard rib were the free corridor traced in 1 mm steps, so their edges were stair-stepped. It also had a flat ledge out to dx +10 at disc+15 and a 24.5 × 15 mm box foot. All three sit between the disc and the head, where they show. The −Y leg stayed slim, so the pair no longer matched.
- **The disc** was not changed by the migration. It has been Ø125 since head v1, and the yaw axis is 4 mm behind the roof's centre, so it overhung the roof's rear edge by 2.4 mm.
- **The body shell's exterior** is unchanged since D-034 to D-037.
- **The two discs at the back of the head** are D-049's rear trim stacks. They are visible only because the inspection models draw the skin at alpha 0.28.

**Legs (`feetech.py`, `layout_model.py`).** Both legs now share one outline:
- **Outline.** The D-049 corridor is eroded 0.5 mm and simplified at 0.45 mm (shapely), so every facet lies inside it. The fit is unioned with the pre-D-049 leg, which is free by construction because the skin, ear and cradle reliefs are cut around it.
- **Shape.** A plinth flares onto the disc as a ruled loft from the D-049 foot's plan to 12.4 mm wide at disc+15. The waist at disc+23 runs from dx −21.6 to −13.5. The arm rises into the head to the Ø22.4 pad. An inboard gusset (Y 48.5–52), fitted to the D-049 rib corridor the same way, fans out under the head.
- **Side-specific features.** +Y keeps the horn pocket, screws and counterbores. −Y keeps the trunnion bore and the pitch-stop sector.
- **Shared features.** Both legs have the rail, the trim-stack band and the 0.5 mm skin step; the step was +Y only in D-049. The spine recess and inlay end at disc+30.5, leaving a lip of at least 1.2 mm.
- **Reliefs unchanged.** The skin, ear and cradle reliefs are still cut by the pre-D-049 leg, so no head shell volume changes.

**Stiffness had to be kept.** Two narrower drawn outlines screened at 24.4 and 31.9 N·m/rad against D-049's 49.9. The leg's in-plane stiffness goes with its X width cubed, and the waist band at disc+20–25 took a third of the twist. The final outline screens at **46.2 N·m/rad** (E 3.5 GPa, h 1.4).

| Pitch chain (frame + leg) | D-049 | D-050 |
|---|---|---|
| PLA 3.5 GPa | 31.6 Hz | 30.7 Hz |
| PLA 2.3 GPa | 25.6 Hz | 24.9 Hz |
| CF legs 4.5 GPa, frame 3.5 GPa | 34.3 Hz | 33.5 Hz |
| CF legs 4.5 GPa, frame 2.3 GPa (the 30 Hz case) | 31.5 Hz | **30.8 Hz** |

The CF leg requirement stands, with 0.7 Hz less margin. The leg floor for 30 Hz in that case is 41.9 N·m/rad.

**Disc.** The rim tapers from R62.5 under the plate to R58.5 at its foot (2 mm wall), with a 0.6 mm top chamfer. Its lower edge sits 1.6 mm inside the roof's rear edge, and the rim keeps 2.0 mm from the yaw pinion's sprung half at every yaw angle. The skin reliefs keep the cylindrical disc (`relief_tool`).

**Presentation model.** New `head-v1-presentation.step.py` is the integrated robot with every part opaque and the reservations and overlays left out. Judge appearance from it; the inspection models stay translucent.

**Mass and stability.** A0 is unchanged: the roll-carried and pitch-carried totals and CoMs match D-049 to 0.001 mm.
- **Yaw-carried mass:** 648.5 → **654.2 g**. The −Y leg gains 8.7 g, the +Y leg loses 2.5 g and the disc loses 0.4 g.
- **Yaw-carried CoM offset from the axis:** 2.30 → **1.45 mm**.
- **Body tip (`check_body_layout.py`, all true):** a_tip is 1.622 neutral (was 1.628) and **1.603** at the worst head pose (was 1.589), against 1.582. The 95 g harness allowance must now stay forward of X 13.5 (was 18.1).

**Checks.** `run_checks.py` on the full 7 × 8 grid (2026-10-09) passes mass, envelope, revision (56 poses, no mechanism or harness hits), the D-049 mounts audit (`passed`, minimum 0.99 mm, every interface fact), integration, layout clearance, fasteners, body layout and yaw stage. `busy_minute.py` fails in the runner only because the CAD runtime lacks `openpyxl`; run with it, validation passes. Yaw RMS/peak rises about 1% (BC-60 0.0198 / 0.119 N·m). `fea/run_fea.py`, which the runner expects, is not in the repo, so the leg FEA was run by hand. `check_leg_clearance_d050.py` covers both legs on 56 poses: every pair is at or above the committed baseline and every new pair is at least 1.0 mm. Only the −Y leg to the skin is closer than in D-049 (0.981 mm against 1.24; baseline 0.717). The yaw stage loads move by 1% or less with the heavier head. The pinion half reaches 26.0 MPa at peak (was 25.8), so the D-048 flag stands. `head-v1-integrated.step` and the new `head-v1-presentation.step` are regenerated. `head-v1.step`, `yaw-yoke.step` and body v1's `body-v1.step` are not.

**Open:**
- **Print orientation.** Each leg now has the plinth and gusset on its inner face and the rail on its outer face, so neither face prints flat without supports. D-049's foot and rib had already ended the flat inside-face print. Choose the orientation with the CF coupon, which needs its modulus along the layers.
- **CF leg coupon** (D-049), now against the 30.8 Hz case.
- **The skin's side windows** round the arms are D-049's bounding-box reliefs. They are not restyled here.

## D-051

**2026-10-10 · Head / passive pitch pivot and yoke-leg joints (HD-008–HD-011; M011-Y, M012; head v1 CAD, mass tree, body v1 hand-off) · ACTIVE; CAD and checks complete; HOLD on received bearing and D-shaft fits, a seat and key coupon, and bench B6**

**Why.** Reading the D-049/D-050 CAD for the builder found two joints that were never designed. No check or BOM row covered either.
- **The −Y pitch pivot.** `pitch_trunnion_-49` was a Ø8 × 9 steel pin in Ø8.4 holes in both the frame arm and the −Y leg. It reached 1.5 mm into the leg and 4 mm into the arm, and nothing retained it. That side carries half the 536 g pitch-carried head.
- **The legs to the disc.** The legs (CF filament) and the disc (PLA) are separate prints, and nothing joined them. The leg FEA assumed a rigid foot. They cannot be one print: the legs must be printed with their layers in the leg plane for the modulus D-049 needs.

**Constraints the joints had to meet.**
- **Nothing outboard of the −Y leg.** A trial cylinder standing 5 mm proud of the outer face at the pivot touched the skin at roll 21°; the skin passes the face at 0.98 mm. So the pivot must be retained inside the 6 mm pad.
- **Little inboard.** A Ø14 boss reaching to Y −40 came within 0.42 mm of the C2 tray at roll −21°, pitch 43°.
- **The disc underside stays untouched.** The stationary yaw pinion runs 0.4 mm under the plate, and the +Y foot passes over it at yaw 0. So no screw heads or pockets from below.
- **Assembly order.** The head is lowered into the yoke with its skin on and then pushed 0.6 mm +Y into the horn pocket. The pin therefore has to go in from outside afterwards.

**Pivot (`feetech.TRUNNION`).**
- **Bearing (HD-008):** MR106ZZ, 6 × 10 × 3, seated in the −Y leg pad from the outer face (Ø10.1 seat) on a 0.7 mm lip. The lip's Ø8.0 hole clears the turning inner ring.
- **Retainer:** a printed 1.0 mm plate on the outer ring, relieved Ø8 × 0.3 over the inner ring and the pin end. It sits in a 2.3 mm recess. Two ISO 7380 M2 × 4 (HD-010) go into M2 × 3 inserts at R8.5, 240° and 300°, and their heads finish 0.12 mm below the leg face. Each insert keeps 1.85 mm to the seat and 2.5 mm to the pitch-stop slot.
- **Pin (HD-009):** Ø6 h6 steel D-shaft, cut to 11.5 mm. It slides through the inner ring into a D-bore (Ø6.1, flat +Z at neutral) in an R6.2 boss on the frame's −Y arm, 6.7 mm engaged, so it turns with the frame. Its outer end stops 0.2 mm under the retainer, which also keeps it from walking out.
- **Boss size:** set by the C2 tray. At R6.5 to Y −42.6 the tray came to 0.92 mm (roll −21°, pitch −25°); at R6.2 to Y −43 it keeps 1.22 mm.
- **Axial location stays at the +Y horn pocket.** The bearing's outer ring is a plain seat, so the −Y side floats. The frame still has 0.4 mm of float beyond the 0.6 mm pocket.

**Leg feet (`feetech.LEG_KEY`).**
- **Key:** each leg's plinth sits over a 11 × 4.5 × 6 mm key on the disc top (dx −20.5…−9.5, |Y| 51–55.5), with 0.15 mm side and 0.3 mm top clearance. The key takes the shear and the pitch couple.
- **Screws (HD-011):** two ISO 7380 M2 × 6 per leg, from the plinth's inner face (spot-faced) through its wall into M2 × 3 inserts in the key, hold the leg down. They engage 3.0 mm, with key walls of 1.4 mm.
- **Walls:** the socket leaves ≥ 1.2 mm of plinth wall everywhere except the screw holes. The first layout (dx −21…−10) left about 1.0 mm at the rear-top corner, so the key moved 0.5 mm forward.
- **Screw heads:** the plinth inner face keeps ≥ 3.2 mm to every moving part, so the heads may stand on it.
- **Assembly:** fit the legs on the bench, then screw the disc to the body hub (the three R22 M3 screws are reachable between the legs).
- **Printing:** print the disc top face down with a support under each key.

**Checks (head v1).**
- **New `check_d051_joints.py`: PASS** on the full 7 × 8 grid. It covers the pivot stack, seat, lip, retainer flush, insert and socket walls, key screws, frame float and posed clearance. Every new or changed part is ≥ 1.0 mm from every part that moves relative to it: pin to −Y leg 1.0, frame to +Y leg 1.0, frame to C2 tray 1.22, retainer to skin 4.56. Pairs that existed before are unchanged, including the −Y leg to skin at 0.981 mm.
- **`check_fasteners.py`:** 46 M2 screws pass, including the six new ones (3.0 mm in each insert, no plastic cut).
- **`check_revision.py`:** 56 poses with no mechanism or harness hits, and service, retention, insert-mouth and hard-stop checks clean. Every part is one valid solid, and the source hashes are current.
- **Also passing:** `check_layout.py` (no hits) and `check_integration.py`.
- **Not re-run:** the 1.8 h `check_feetech_mounts.py`. Its interface facts are untouched; its posed pairs for the frame and legs are covered by the new sweep.

**FEA (`fea/`, D-051 block in `results.json`, E 3.5 GPa, h 1.4).**
- **Frame:** pitch stiffness 112.6 N·m/rad (was 112.5).
- **Roll mount:** 450.9 N·m/rad (was 455.9). The roll case now clamps the D-bore instead of the Ø8.4 bore.
- **+Y leg:** 46.6 N·m/rad with the keyed foot (ring plus socket walls), 45.9 with the foot ring alone (D-050: 46.2 on a solid foot; floor 41.9).

| Pitch chain | D-050 | D-051 |
|---|---|---|
| PLA 3.5 GPa | 30.7 Hz | 30.8 Hz |
| PLA 2.3 GPa | 24.9 Hz | 25.0 Hz |
| CF legs 4.5 GPa, frame 2.3 GPa (the 30 Hz case) | 30.8 Hz | **30.9 Hz** (30.8 with the ring-only foot) |
| Roll, 3.5 GPa | 126 Hz | 125 Hz |

`frame_fea.py` gains a `legkey` case. Joint, screw and insert compliance are still excluded (B6).

**Mass and stability (`mass_layout.py`, plain run; A0 not re-solved).**
- **Residuals:** the A0 residuals are ≤ 0.003 mm, so `axes.json` is unchanged.
- **Pitch-carried:** 535.7 → 536.3 g. The boss sits on the axis.
- **Yaw-carried:** 654.2 → 655.2 g. The keys add 0.6 g, the frame boss 0.6 g, and the retainer and the six D-051 screws (now modelled steel, `D051_HARDWARE`) 1.3 g. The leg sockets and the −Y pad's seat and recess remove 1.4 g.
- **Body:** `check_body_layout.py` all true. a_tip is 1.621 neutral (was 1.622) and 1.603 at the worst head pose (unchanged), against 1.582. The harness allowance must stay forward of X 13.46 (was 13.5).

**Exports.** `yaw-yoke.step`, `head-v1-integrated.step` and `head-v1-presentation.step` are regenerated with the pivot, keys and screws. `head-v1.step` is not.

**BOM.** HD-008 to HD-011 are added. The retainer and keys are prints (M011-Y, M012). The six M2 × 3 inserts are the head's OD 3.6 article.

**Open:**
- **Received parts:** check that the MR106ZZ slides into a printed CF seat coupon (Ø10.1) and that its inner-ring land is under Ø7.6. Check the D-shaft slip fit in a printed D-bore and in the bearing.
- **Coupons:** the 0.7 mm lip in CF, key and socket fit, and insert pull-out in the PLA key.
- **Bench B6:** loaded pitch stiffness with the real joints.
- **The spindle-to-cradle fastening** (fabrication audit) is still not released; it is not part of this decision.

## D-052

**2026-10-10 · Body + head / yaw cable path: drum slit, PCB-14 joiner boards, disc bore and channel (BO-045, BO-050, BO-058, BO-062; M012; W37, W42, W43; head v1 and body v1 CAD) · ACTIVE; CAD and checks complete; HOLD on the ZIF selection, an FFC fold mock-up and the D-044 cassette bench test**

**Why.** Reading the D-044 stage and the head disc for the builder found that the head cables had no buildable route from the cassette to the head. No check covered it: the checks only test solid overlap, and the cables were placeholders.
- **The drum slot was shorter than the FFC.** It was 11.4 mm tall (Z 121.8–133.2) for an 11.5 mm FFC.
- **PCB-14 could not exist as drawn.** It was a Ø35 ring (R6–17.6) on the rotor ring.
  - Its three 22-pin ZIFs underneath had to fit inside the R11 drum core, around an R6 hole. A 16 mm ZIF does not fit there.
  - Its head-side connectors were a 3 mm tall ring (R12.4–17.6) boxed in by the solid hub shoulder above and the disc's own hub wall (R7–12) inside. That wall's lower end was 0.2 mm above the board. A cable plugged in there had no way into the disc bore.
- **The disc was sized for a Ø3 placeholder.** The bore was Ø14 and the groove 3.6 × 3.4 mm, for `yaw_branch_bore_and_disc_groove_OD3_Y`. The real branch is three 22-pin FFCs: 6 power conductors, up to 22 signals and the CSI.
- **The cassette angles did not close.** In a clock spring the inner wrap runs one way from the anchor and the outer wrap the other way to the exit, so exit = anchor − W_in + W_out. Equal 120°/120° wraps need the anchor at the exit angle (300°). With the slot at 90° and the 240° loop budget, the wraps are 15°/225°, and the inner wrap runs out at −55.6° of yaw.

**Decision.** Keep the D-044 architecture (the head demates at PCB-14 inside the hub) and make every step of the path physical.

**1. Drum slit (BO-058).**
- The FFC enters the drum core through a slit at **0°**, 1.6 mm wide (three FFCs at 0.35 mm), open at the bottom and running up to the rotor ring.
- The FFC band is centred in the cassette (Z 121.35–132.85), 0.75 mm under the slit top.
- **Wraps:** with the exit at 300°, the D-044 240° budget gives **150° inner** (clockwise from the slit) and **90° outer**, with the U-turn at 210°. At the ±90° loop capacity the inner wrap runs 94–206° and the outer 56–124° (D-044's paper values were 64–176° / 86–154°). `check_yaw_stage.py` now derives the wraps from the two angles instead of assuming 120°/120°.

**2. Fold in the drum core.**
- In the core each FFC fans out to its own plane (Y −2.9, 0.4, 3.7; an S-bend of about R2.9 through the thickness) and takes **one 45° fold**. That turns it upward with its width along X.
- The fold square sits inside R6.7, 4.3 mm inside the R11 drum bore and 0.35 mm above the stationary cassette floor (which has an R9 hole under it).
- A 1.05 mm straight tail runs into the lower ZIF.

**3. PCB-14 becomes three joiner boards (BO-062 ×3).**
- **Boards:** three identical vertical boards (0.8 mm FR4, 17 mm wide, Z 133.9–150.7), stacked in Y at a 3.3 mm pitch and centred on the axis.
- **ZIFs:** each board is a straight 1:1 22-pin FFC joiner with two side-entry ZIFs on its +Y face. The lower one faces down (Z 133.9–139.1) and takes the cassette FFC; the upper one faces up (Z 145.5–150.7) and takes the head FFC. The ZIF envelope is FH12 class, 16 × 5.2 × 2.0 mm (`E`).
- **Tabs and posts:** each board has tabs (|X| up to 13.6, Z 137.4–143.0). They seat on 0.4 mm floors in two slotted posts on the rotor ring (|X| 11–15.2, up to Z 143.4), 2.4 mm inside the hub spigot.
- **Capture:** the hub shoulder (R13.15, Z 144) overhangs every tab by at least 0.45 mm radially with a 1.0 mm lift gap, so the boards cannot come out once the rotor is screwed up.
- **The upper ZIFs sit inside R9.3,** under the disc's R10.5 bore. The head FFCs therefore demate through the bore with the disc on. Removing the head no longer needs the disc off.

**4. Hub and disc (BO-045, M012).**
- **Hub:** the bore grows from R12.15 to **R13.15**, leaving a 4.1 mm web under the tooth roots. The shoulder still bears on the inner ring.
- **Disc pilot and bore:** the disc's pilot becomes an **R10.5–13 ring** reaching 10.6 mm below the top (to Z 144.4): 6.6 mm of engagement, 0.15 mm radial clearance, 1.4 mm above the board tabs. It replaces the R7–12 ring that ran 14 mm down. The **bore is Ø21**; it keeps 0.8 mm to the joiner boards.
- **Channel:** a **12.5 × 1.5 mm channel** runs from the bore to Y 46 and replaces the 3.6 × 3.4 mm groove. It leaves a 2.5 mm floor (the groove left 0.6 mm).
  - The three head FFCs rise from the upper ZIFs in XZ planes, bend over toward +Y, and lie flat in the channel as a stack of about 1.05 mm. The top of the stack is 0.4 mm under the disc top.
  - No fold is needed, because the 0° slit puts every FFC's width along X.
- **Riser keep-out:** widened to the channel width (Y 44–47.6). It is 0.4 mm from the +Y leg and is still `UNROUTED`.
- **Relief tool:** the skin relief tool keeps the RP-06 bore and groove; the reliefs only use the rim.

**5. Harness.**
- **W37, W42, W43** now end at their joiner boards' lower ZIFs.
- **Head side:** each continues as a 22-pin 0.5 mm FFC from the upper ZIF through the disc channel. The CSI must stay at 22-pin width (11.5 mm) through the disc, so any 15-pin transition to the Camera Module 3 is inside the head.
- **Not changed here:** the riser up the +Y leg and the pitch and roll crossings are unrouted, as before.

**Assembly (replaces D-044 steps 1 and 5).**
1. **Bench:**
   - Press the bearing into the housing and screw down the clamp ring, then drop in the hub.
   - On the rotor, drop the three boards into the post slots.
   - Thread each FFC through the slit from below, fold it and plug it into its board's lower ZIF.
   - Raise the rotor into the hub from below and screw it on. The hub shoulder now captures the boards.
   - Wind the FFCs into the stator.
5. Screw the disc and yoke to the hub. Plug the three head FFCs into the upper ZIFs through the Ø21 bore, lay them in the channel, then fit the tilting assembly.

**Checks.**
- **`check_yaw_stage.py`: ALL PASS** (body v1, serial relief build).
  - The stage, sweep, cartridge-lowering, pinion-drop and moving-part results are all empty. The rotor and hub are one solid each, and the mesh gap is 0.072 mm.
  - **New `cable_path_d052` block:**
    - slit 0.75 mm over the FFC band and 0.55 mm wider than the stack;
    - fold square R7.16, 3.84 mm inside the drum bore and 0.35 mm over the stator floor;
    - a 1.05 mm tail before the lower ZIFs and a fan-out S-bend of R2.68 (`E`);
    - no joiner overlaps with the rotor, hub or disc; boards 0.79 mm from the disc and 1.0 mm from the hub;
    - upper ZIFs 1.22 mm inside the disc bore;
    - disc pilot 0.15 mm radial clearance and 6.6 mm engagement;
    - tabs captured by 0.46 mm with a 1.0 mm lift gap, 1.4 mm under the pilot;
    - posts 1.8 mm inside the spigot;
    - the placed head FFC stack touches nothing but the channel floor, and its top is 0.4 mm under the disc top.
- **Head v1:** `check_revision.py` passes on all 56 poses with the new FFC jackets: no mechanism hits, no harness pinches, and service, retention and insert checks clean. `check_integration.py` and `check_layout.py` also pass.
- **Exports:** `motion_envelope.py --write` changes only the disc record (bore, pilot); the sweep rows are unchanged. `yaw-yoke.step`, `head-v1-integrated.step` and `head-v1-presentation.step` are regenerated.
- **Not re-run:** `check_fasteners.py` (no M2 screw changed), `check_d051_joints.py` (keys, pivot and legs untouched) and the 1.8 h mounts audit.
- **Tooling note:** body scripts that build the head after a head edit hang in the spawn relief pool. Run them with `MAKAD_RELIEF_SERIAL=1`.

**Mass and stability.**
- **Head (`mass_layout.py`, plain run; A0 not re-solved):** the disc goes from 72.73 to 69.34 g. Yaw-carried mass goes from 655.2 to **651.8 g**, and yaw inertia from 0.001456 to 0.001455 kg·m². The roll- and pitch-carried totals and CoMs are unchanged, so `axes.json` stands.
- **`BODY_YAW_STAGE`:** 199.4 → **200.3 g** at (11.63, 14.94, 126.95).
  - The boards weigh 3 × 0.51 g and the ZIFs 6 × 0.4 g (`E`), replacing the 3 g ring estimate.
  - The rotor, with its posts, is 11.01 g; the hub, with the larger bore, is 15.11 g.
- **Body (`check_body_layout.py`, all true):** a_tip is 1.621 neutral (unchanged) and **1.604** at the worst head pose (was 1.603), against 1.582. The harness allowance must stay forward of X 13.20 (was 13.46).

**BOM.**
- **BO-062** becomes three joiner boards. The ring board is withdrawn.
- **BO-058** adds the slit and the board posts.
- **BO-045:** R13.15 bore.
- **W37/W42/W43** and the 04-pcbs register are updated.

**Open:**
- **ZIF:** select a 22-pin 0.5 mm side-entry ZIF no taller than 2.0 mm and no deeper than 5.2 mm with its actuator open. Lay out the joiner with power traces sized for the paralleled W42 conductors.
- **Fold mock-up:** print the rotor and fold three real FFCs through the slit into ZIFs on dummy boards. Check the fan-out S-bend, the 45° fold and the 1.05 mm tail, and that the rotor rises into the hub without loading them. Then run D-044's 100k-sweep cassette test with the 150°/90° wraps.
- **Coupons:** board-slot fit in PETG (0.1 mm per side) and the disc pilot in the R13.15 hub bore.
- **CSI:** signal check through two ZIF pairs (unchanged from D-044).
- **Head riser:** the route up the +Y leg into the pitch-carried frame is still unrouted.

## D-053

**2026-10-10 · Head / assembly paths: split skin, pitch-stop entry channel, pivot service ports, roll spindle joint and display retention (HD-012–HD-016; M002, M010, M011-Y, M019a; head v1 CAD, body v1 README) · ACTIVE; CAD and checks complete; HOLD on one real assembly and the coupons listed under Open**

**Why.** A head-to-chassis assembly pass found that the head could not be put together as drawn. Every check passed, because each one tests overlap at the final position. None tested the path a part takes to get there or whether a tool can reach a screw. Rigid straight-line probes on the cached parts found:
- **The skin could not go over the cradle.** The one-piece cradle's ear stalks reach |Y| 69.2 through ports in a skin only ±65 wide. Every ±X/±Z move of the bare skin hit the cradle or pitch frame within 2–40 mm. Its own bezel and rear-cover receivers would also have trapped it on X.
- **The head could not be lowered into the yoke.** The Ø2 pitch-stop dowel, pressed into the frame lug, rides in a closed arc slot in the −Y leg's ring. It hit the ring from 8 mm above its seat, at both 0.6 and 1.0 mm Y offset. It could not be fitted afterwards either: the ring is solid outboard and the head interior is inboard.
- **Two horn screws could not be driven.** The skin wall lay across the axes of the 45° and 135° horn-to-leg screws even with the ear off. The −Y D-pin's Ø6 path clipped the skin edge (axis 2.4 mm from it). Its retainer (R10.9) had no way in at all.
- **The roll spindle had no joint to the cradle.** It stopped at the cradle's rear face (X −40), touching it, with no bore, key or pin. The fabrication audit listed it as not released.
- **Nothing held the display from behind.** Its only rear contact was the −Y connector strip, 0.3 mm from a cradle rail. The glass could move about 1.25 mm.

**1. Skin split (M019a).**
- The skin is now two prints split at the ear line, **Z 42**, through the stalk ports. `main_octagonal_skin` is the upper half; `main_octagonal_skin_lower` is new.
- Each half has a straight path: the upper half lifts clear for 120 mm and the lower half drops clear for 120 mm.
- **Joint.** The bezel and rear cover each screw to both halves: front receivers at Z 16 are in the lower half, those at Z 64 and 78 in the upper; rear receivers at Z 26 lower, Z 65 upper. The ear inner mounts clamp across the seam at mid-length.
- **Lap lip.** A 1.2 × 4 mm lip on the lower half rises inside the upper wall with 0.15 mm clearance, rooted 2 mm into the lower wall. It stops short of the recessed side lands (X −104…−81), whose inner doubler fills that band.
- The split is cut after the motion reliefs, so the reliefs are unchanged and cut once on the whole skin.

**2. Pitch-stop entry channel (M011-Y).** A 2.4 mm vertical channel runs from the dowel's neutral position (180°) out through the top of the −Y leg's ring, 4 mm deep in Y. The dowel now drops in as the head is lowered. It joins the slot mid-travel, so both stops are unchanged: no overlap at −25° and +43°, overlap 1° beyond each. The skin relief tool keeps the closed slot.

**3. Pivot service ports (M019a).** An R12 port through each skin side wall on the pitch axis, under the ear cap. With the ear off:
- **+Y:** all four horn screws (Ø5.9 head path) and the horn centre screw have straight paths.
- **−Y:** the D-pin (Ø6.2) and the whole retainer (R11) have straight paths.
The ports sit inside the ear web's R20.3 and the inner mount's R28 seat.

**4. Roll spindle joint (M010, M016).**
- The spindle runs 9.8 mm further forward (now Ø6 × 44.4) into a **D-bore** (Ø6.1, flat at 2.55, +Z at neutral) in a new **R8 boss** on the cradle, X −36…−28. Its front 10 mm carry the D-flat, ahead of the front bearing's inner ring.
- An **ISO 4029 M3 × 5 cup-point set screw** (HD-012) in an M3 × 4 insert (HD-013) from +Z bears on the flat. The flat carries the roll torque; the set screw holds the cradle on axially. The insert keeps 0.95 mm of plastic above the bore.
- The boss is on the roll axis, so its swept volume is itself. It keeps 1.5 mm from the roll stop pin and 2.6 mm from the front retainer screws.

**5. Display retention (M002).**
- The Waveshare board has four **M3 standoffs** behind its PCB (Ø5.5, rear faces at X −16.3, Y ±49.0, Z 9.88 / 69.85; found in the vendor STEP). A printed **display rear frame** presses them forward through **closed-cell foam pads** (HD-015, 1.5 mm free, 0.7 mm installed). The display's forward stop is the bezel pocket face 0.3 mm ahead, so the pads stay about 33% compressed there.
- **The frame hangs from the four upper front receivers.** Their screws become **M2 × 18** (HD-014) through Ø2.3 clearance bores the full boss length into M2 × 3 inserts (HD-016) in the frame's tabs. One screw clamps the bezel, the skin half and the frame.
- The two Z 16 screws stay M2 × 8 into skin inserts. A frame tab behind those bosses touches the +Y leg at pitch 43°.
- Two feet at Y ±26…34 bear rearward on the cradle's bottom rail (0.1 mm nominal), so rearward loads go into the cradle, not the screws. A notch clears the −Y connector strip.
- The frame keeps 2.17 mm from the yoke legs and 7.0 mm from the pitch frame over the 7 × 8 grid.
- **Order.** The frame goes in after the lower skin half and before the upper one: its upper tabs sit right behind the upper half's bosses. The display then slides in from the front.

**Assembly order.** See the [head CAD README](03-head/v1/cad/README.md#assembly-order-d-053). The head goes into the yoke with the skin on and the ears off; the horn screws, D-pin and retainer go in through the ports; then the ears.

**Also corrected.** The body v1 README's yaw-stage step 2 still described the XC330 mounted from below. It now gives the D-048 ST3215-HS mount: four M2 × 8 from above through the plate, before the cartridge.

**Checks.**
- **`run_checks.py`, full 7 × 8 grid (head v1 and body v1 hand-off): PASS.** Mass, envelope, revision, mounts, integration, clearance, fasteners, body layout and yaw stage pass. `busy_minute.py` fails in the runner only because the CAD runtime lacks `openpyxl`; run with it, validation passes. `fea/run_fea.py` is still missing (D-050).
  - **Revision:** 56 poses, no motion, harness, static or service hits; every part, including both skin halves and the frame, is one valid solid. Hard stops are unchanged.
  - **Mounts audit:** passed, minimum 0.99 mm, no new pair under 1 mm.
  - **Fasteners:** all 46 M2 screws pass. Each M2 × 18 has 3.0 mm in its frame insert, no plastic cut, tip in the relief.
- **`check_d051_joints.py`: PASS**, no new pair under 1 mm. **`check_ears.py`: PASS**, output unchanged.
- **Assembly paths (rigid straight-line probes, neutral pose):**
  - lower skin half up from below, frame in from above, upper half down over the frame: all clear for 120 mm;
  - display out forward with the bezel off: clear;
  - pitch-stop dowel lowered into the yoke: clear at 0, 0.6 and 1.0 mm Y offset;
  - all four horn screws, the horn centre screw, the D-pin and the retainer: clear apart from the ear parts.
- **Not re-run:** the leg FEA (legs and their joints are unchanged apart from the 2.4 mm channel in the −Y leg's stop ring, which is not on the +Y leg the FEA covers).

**Mass.**
- **Head (`mass_layout.py`, plain run; A0 not re-solved):** roll-carried 388.8 → **392.1 g**, pitch-carried 536.3 → **539.6 g**, yaw-carried 651.8 → **655.1 g**. The cradle boss adds 1.6 g and the longer spindle 2.1 g; the two skin halves (34.7 + 18.6 g) weigh 0.3 g less than the one-piece skin. The display frame (about 8 g) is inside the M002 display allowance. The pitch-carried CoM moves 0.025 mm off the A0 axis, so `axes.json` stands.
- **Body (`check_body_layout.py`, all true):** a_tip is **1.619** neutral (was 1.621) and **1.600** at the worst head pose (was 1.604), against 1.582. The 95 g harness allowance must now stay forward of X 14.3 (was 13.2).

**BOM.** HD-012 to HD-016 are added. The frame, both skin halves, the cradle boss and the leg channel are prints (M002, M019a, M010, M011-Y).

**Open:**
- **One real assembly** in this order, with the real servos, display, bearings and tools. Record any screw a tool cannot reach. The probes are rigid, straight-line and at neutral; they do not prove hand room, wire slack or tilt.
- **Coupons:** the split seam and lap lip in the skin material; the cradle D-bore on the real spindle; the M3 × 4 insert above the bore; the frame tab inserts.
- **Received display:** confirm the standoff positions and thread, the pad seating and that the board stops on the bezel pocket face.
- **Appearance:** the seam is visible at Z 42 on the front and rear of the side walls, outside the ears. Judge it in the presentation export.
- **Not changed here:** the head harness route up the +Y leg and across the pitch and roll axes (D-052 open), the leg key's 0.15 mm side clearance (B6), and the body-to-chassis J13 washers.

## D-054

**2026-10-10 · Head / camera housing restyle: slim raked fin (M019a; head v1 CAD) · ACTIVE; CAD and checks complete**

**Why.** The builder found the camera housing too heavy visually. It was a 46 mm crown with sloped sides on the front bezel, plus a hipped roof cap in the skin that ran 54 mm back to X −78 with triangular side facets. The camera cannot drop into the face: the display fills Z 6–74 and the camera clamp reaches Z 102.3 against an 86 mm roof, so about 18 mm of housing must stand above the roof at the front. Three concepts were rendered against the current design (slim raked fin, integrated forehead, soft blister). The builder chose the slim raked fin.

**Decision.**
- **Crown (`front_bezel_integral_camera_crown`):** `CROWN_OUTER` becomes 40 mm wide (Y ±20, was ±23 sloping in from Z 85 to ±17), vertical sides to Z 101 and 3 mm × 45° top chamfers to the Z 104 top. It keeps its 24 mm depth, flat top, front optics cut, LED hole, rear CSI opening and the 1.3 mm normal walls from `crown_inner`.
- **Hood (`main_octagonal_skin`, `crown_roof_cap`):** the same section, above the roof, runs back from the crown's rear face at X −24 and rakes down at **35.5°** (`CROWN_RAKE_DEG`). It meets the Z 86 roof about 25 mm behind the crown (base edge at X −50.6). It is hollow (1.6 mm wall), open to the crown and to the roof it is fused into. It replaces the hipped cap to X −78 and its 0.4 mm top panel.
- **Roof notch:** follows the crown width plus the 0.8 mm seam (Y ±20.8, was ±23.8).
- **Unchanged:** the camera, its edge clamp and bracket screws, the LED and diffuser, the CSI exit and roof guide, the crown height (104 mm) and the bezel/skin joint.

**Fit.** Inside the fin the clamp keeps 3.7 mm a side and the LED reserve 1.0 mm. The camera bracket receiver bosses (Y ±16, R2.8) now fuse into the side walls. The camera's nearest gap to the bezel stays 0.723 mm and the bracket's 0.2 mm, the same as before.

**Mass.** The printed volume falls by 0.21 cm³ (bezel +0.09, skin −0.30; about −0.3 g PLA). `mass-placement.json` and `axes.json` are not regenerated, by the standing rule that head edits do not silently move the body hand-off; the change is far below the register's resolution.

**Checks (head v1).**
- `check_revision.py`: **PASS.** 56 roll/pitch poses run this time (not reused), 3,936 mechanism pairs per pose. Same-frame, motion, harness-pinch, service-extraction, retention and C2 service lists are all empty. Bezel and skin are one valid solid each (`revision-checks.json`).
- `check_fasteners.py`: **PASS**, 46 screws; output unchanged.
- `write_dimensions.py`: `dimensions.json`/`.md` regenerated. They were last written at the 2026-10-07 fabrication fixes and still carried pre-D-049 XC330 rows and axes. This refresh brings them to the current source.
- Not rerun: the mounts audit, D-051 joint sweep, leg clearance and FEA (no part they cover changed), and `compare_golden.py` (goldens are the D-049 set).

**Views.** `head-v1.step`, `head-v1-integrated.step` and `head-v1-presentation.step` regenerated locally (untracked); new presentation snapshots in `03-head/v1/cad/snapshots/`.

**Next.** Judge the fin on the first skin and bezel print.

## D-055

**2026-10-10 · Body / shell review fixes: front badge, fan grille height, fan collar, mic ports (BO-019, BO-024; body v1 CAD) · ACTIVE; CAD and targeted checks complete; HOLD on a printed shell or grille coupon**

**Why.** The builder reviewed the opaque presentation model (`head-v1-presentation.step.py`) and raised five points. Measuring them against the body v1 source found:
- **Front badge land.** The square amber block over the speaker was `FRONT_BADGE_LAND`, a 30 × 4 × 2 mm box carried over from Layout 02 (`BODY_X_FRONT + 3.4`, Z 124), where the front panel was flat. The exposed-speaker panel later added a cup up to Z 128, so the box ended up inside the cup, behind the lip (X 91.1–93.1 against the lip at X 100.8–102.6). It overlapped the cup wall by 58.6 mm³ and the speaker acoustic-cavity keep-out by 153 mm³, sat 2.9 mm from the K 50 WP, and could not be printed. No check covered it.
- **Fan grille.** The 28 mm grille circle was cut off 1 mm above the wheel-arch pod (window cut at R55 about the axle, pod outer R54), so in the model the grille seemed to touch the arch. Moving the fan and its screws up in 1 mm steps, nothing but the fan web (which moves with the fan) is hit up to +10 mm. At +5 mm the fan frame reaches the web's upper rail root (Z 126).
- **Fan collar.** In the roof-down print, a measure of the grille and collar region (triangle normals, 45° limit) found 309 mm² of overhang. Most of it was the bore floor (145 mm², 2–4 mm off the skin) and the top of the outer face (72 mm²).
- **Mic ports.** Ø2.0 is acoustically sufficient. The Ø0.8 PCB-06 hole is the narrowest point, and the D-037 Helmholtz estimate is 13–23 kHz. But a Ø2 hole lying horizontal in the roof-down print comes out under size.
- **Shell-to-frame screws.** The four outside-driven M3 × 16 screws (BO-029) are the shell's only retention to the frame. They stay.

**Decision.**
- **Badge:** delete `FRONT_BADGE_LAND`. BO-024 is now the rear-button bezel only.
- **Fan:** `ENCLOSURE_FAN_CENTER` moves from (17.5, 107) to **(17.5, 110)**. The web opening, the two fan screw holes, the grille and the collar follow it. The whole grille circle now clears the pod by 2.2 mm, and the fan top stops 1 mm under the upper rail root. The W41 lead reserves (Z 118–124) are unchanged; they still run beside the fan's front face to its top-front corner.
- **Collar:** `_fan_collar()` becomes a teardrop. The outer face gets a 45° peak on top, the bore a 45° peak at the bottom, and the outer face a matching peak below to keep the 1.5 mm wall (new `_teardrop_y()`).
- **Mic ports:** unchanged at Ø2.0. Drill them to Ø2.0 after printing (`MIC_PORT_RADIUS` comment, README).

**Checks (body v1).**
- `check_cooling_path.py`: **PASS.** Fan, W41, intake path, grille-to-pod and lowering-sweep clash lists are empty. Grille free area is 382 mm² (was 373). Collar to the 90° pod boss is 4.6 mm (was 2.55) and to the FRONT_L mic boss 12.0 mm. Grille edge to FRONT_L is 23.4 mm (was 24.1; the gate is 22) and to REAR_L 25.9 mm. Fan-on rise at 8.5 W is 6.8 K (was 6.9).
- `check_body_panel_fit.py`: **PASS.**
- `check_body_layout.py`: **PASS** once the shell row was updated to 248.4 g at (18.09, −0.05, 92.92) (was 248.7 g at (18.17, −0.09, 92.95)). The fan row's centroid moves to Z 111. On the branch, the whole robot was unchanged to three places (2,645.1 g; neutral a_tip 1.621 m/s²). Re-run after merging with the D-053/D-054 head mass tree: 2,647.8 g at CoM (18.07, 1.15, 109.45); neutral a_tip 1.620 m/s² and pose-conservative 1.596 m/s², both above the 1.582 m/s² screen.
- **Shell-frame fit, targeted:** the full `check_shell_frame_fit.py` was stopped after about an hour of CPU. It sweeps the whole shell against every Pi 5 STEP leaf, which stalls. The collar is the only shell geometry changed, so it was run alone through the same tests. It does not overlap the frame, chassis or joint hardware, nor the pods, trims, their screws and inserts, or the mic boards. It clears every fixed part at each 5 mm lowering step from 0 to 120 mm, and both the pod-screw and frame-screw driver paths. The shell stays one solid. `check_cooling_path.py` also sweeps the shell past the fan, its screws, W41 and the web with no clash.
- **Printability (my triangle-normal measure, roof-down, 45° limit):** grille and collar region 309 → 81 mm². What remains is the slot ends (34 mm², 2.5 mm bridges) and a 13 mm² line where the top peak meets the skin. The whole shell is 2.93% → 2.77%.
- **Not rerun:** `check_mic_mounts.py` (no mic geometry changed) and `check_yaw_stage.py` (the fan sweep found no yaw-stage part near the fan). `check_feetech_yaw_fit.py` is a superseded D-048 trial; its regenerated JSON is not committed.
- **Not refreshed:** `write_outputs.py` reports (`dimensions.json`, `frames.json`, `mass-properties.*`) were already stale on main (they list 2,530.7 g against the current 2,644.8 g). They are left for a separate refresh.

**Views.** `body-v1.step` and the head presentation and integrated STEPs need regenerating to show the change.

**Next.** Print a grille-and-collar coupon roof-down to confirm the slot bridges and the peaks. Drill-test a Ø2 port in the same coupon.

## D-056

**2026-10-11 · Head / camera fin front section: trapezoid (M019a; head v1 CAD) · ACTIVE; CAD and checks complete**

**Why.** Reviewing the D-054 fin in the presentation model, the builder wanted the camera bump trapezoidal from the front, not rectangular.

**Decision.** `CROWN_OUTER` becomes a trapezoid: vertical below the roof to Z 85 at Y ±22, then straight sides sloping in to a **34 mm flat top at Z 104** (Y ±17). D-054 had 40 mm vertical sides with 3 mm × 45° top chamfers. The crown depth, flat top to X −24, the hood's 35.5° rake and length, and the 1.3 mm crown / 1.6 mm hood walls are unchanged; the hood and the roof notch (now Y ±22.8) follow the section. `crown_roof_cap` now drops the repeated corner that clamping the section at the hood base creates.

**Fit.** The slope is set by the LED reserve's outer top corner (Y 17.7, Z 94.3), which keeps **0.49 mm** to the sloped inner wall (1.0 mm in D-054). The camera clamp keeps 1.1 mm under the wall at its top corners, and the camera bracket receiver bosses (Y ±16) stand free inside the 41.4 mm cavity again, as they did in the original crown. Camera 0.723 mm, bracket 0.2 mm, diffuser 0.141 mm and CSI reserve 2.2 mm to the bezel are unchanged.

**Mass.** Printed volume −0.22 cm³ (bezel −0.12, upper skin −0.10; about −0.3 g PLA). `mass-placement.json` and `axes.json` are not regenerated.

**Checks (head v1, on the D-053 split skin).**
- `check_revision.py`: **PASS.** 56 poses run (not reused), 4,328 mechanism pairs per pose; same-frame, motion, harness-pinch, service-extraction, retention and C2 service lists all empty.
- `check_fasteners.py`: **PASS**, 46 screws; output unchanged.
- `write_dimensions.py`: regenerated.
- Not rerun: mounts audit, D-051/D-053 joint sweeps, leg clearance, FEA (no part they cover changed).

**Views.** Integrated and presentation render packages rebuilt; new snapshots in `03-head/v1/cad/snapshots/`.

## D-057

**2026-10-13 · PCBs / register numbering: nose Hall carrier becomes PCB-15 (CH-064; final v1 CAD) · ACTIVE; numbering only, no design change**

**Why.** The nose Hall carrier came out of the chassis nose work ([D-013](#d-013)) before the [04-pcbs board register](04-pcbs/README.md#board-register) existed, and the register took it in under its BOM ID. It was the only custom board without a `PCB-xx` number, which made it read as something other than a custom PCB in the board list and in the whole-robot CAD's `Custom PCBs` group.

**Decision.** The 6.0 × 4.6 × 0.8 mm DRV5055A3 nose Hall carrier is **PCB-15**. PCB-15 is the board ID and CH-064 stays its BOM line, the same pairing as PCB-12/CH-086 and PCB-14/BO-062. The board, its design and its open work are unchanged.

**Changed.**
- [04-pcbs/README.md](04-pcbs/README.md): the register row is PCB-15.
- [BOM.csv](BOM.csv): CH-064 is named "Nose Hall board PCB-15"; its spec path is corrected to `01-chassis/v1/research/nose-hall-board.md` (the note moved to `research/` earlier and the BOM path was stale).
- [01-chassis/v1/BOM.md](01-chassis/v1/BOM.md) and [nose-hall-board.md](01-chassis/v1/research/nose-hall-board.md): PCB-15 added next to CH-064.
- `final/v1/cad/makad-v1.step.py`: the `Custom PCBs` subgroup is `PCB-15 nose Hall carrier`. The CAD part labels (`BALL_NOSE_HALL_CARRIER_PCB`, `BALL_NOSE_HALL_DRV5055A3_SOT23`) are unchanged, so no chassis or body check is affected.

**Not changed.** Earlier entries that say CH-064 are left as written.

**Next.** None for the numbering. The board's own open items (layout, cap trip and wire-break fault bench) stay as listed in the register.

## D-058

**2026-10-14 · PCBs / design toolchain: KiCad 10, Freerouting, JLCPCB (all custom boards; [04-pcbs workflow](04-pcbs/workflow.md)) · PARTLY SUPERSEDED by [D-060](#d-060): KiCad version and autorouting. `kicad-cli` checks and outputs and JLCPCB stay ACTIVE**

**Why.** The [PCB workflow](04-pcbs/workflow.md) takes each custom board through design, procurement and integration into the final CAD, and stage 1 needed a design tool. Three options were checked:

- **Fusion Electronics** cannot be driven by the agent. The Fusion MCP's electronics tool only reads designs, and the Fusion Python API's `adsk.electron` module is a read-only preview: nothing in it places a part, draws a net or routes a track. Its designs also live in Autodesk's cloud, not in the repo.
- **text-to-cad (cadgen)** models solids only. Its KiCad support ([PR #518](https://github.com/earthtojake/text-to-cad/pull/518), `cadgen.pcb`) was open and unreleased on 2026-10-14; the latest release was 0.7.21.
- **KiCad** keeps schematic and board as plain-text files that can be written, diffed and committed. `kicad-cli` runs every check and export without the GUI, and the GUI is there for review and hand routing.

**Decision.**

- **Design tool: KiCad 10** (10.0.6, Homebrew cask, `/Applications/KiCad`). Each board's KiCad project lives in its folder's `design/`. The global symbol and footprint tables are KiCad's defaults.
- **Checks and outputs: `kicad-cli`.** ERC on the schematic. DRC with `--schematic-parity` on the board, which also catches any difference between schematic and board. Gerbers, drill, pick-and-place and BOM for fab. The populated board as STEP for stage 3.
- **Autorouting: Freerouting 2.5.0** (`~/.local/share/freerouting/freerouting.jar`, SHA-256 checked against the GitHub release; runs on the Homebrew OpenJDK). The board goes out as Specctra DSN and comes back as a session, then KiCad's DRC checks the result. Small boards (PCB-06, PCB-11, PCB-14, PCB-15) may be fully autorouted. On PCB-02, PCB-03, PCB-04 and PCB-13 the high-current and switching paths are routed by hand and locked first; the autorouter then routes only the signal nets. Track widths and clearances come from KiCad net classes set before routing.
- **Fab and assembly: JLCPCB PCBA by default**, as [audiosystem.md §5](02-body/v1/research/audiosystem.md#5-how-the-boards-will-be-made) already planned for PCB-05 to PCB-08. Layout follows JLCPCB's limits. A board goes elsewhere only by decision.

**Evidence (2026-10-14, throwaway board in the session scratchpad, not in the repo).** A three-part board (2-pin header, 1 kΩ 0603, 0603 LED) went through the whole flow. Schematic written as text, then ERC: 0 violations. Netlist exported, then the board built from it in KiCad's Python: DRC 0 violations, 0 unconnected, 0 parity issues. Gerbers, drill, pick-and-place and BOM exported. The STEP loaded in the project's 0.4.28 build123d runtime, with one labelled child per part. With its tracks removed and the connector moved so that straight tracks would cross, Freerouting routed all three nets in 0.19 s, and KiCad's DRC on the result was again clean.

**Integration notes for stage 3.**
- KiCad's STEP has Y flipped: board Y points down, so the test board came out at Y −12…0.
- The board solid runs Z 0…1.51 mm because copper isn't modelled. The CAD placeholders assume 1.6 mm.
- The default Gerber export writes every layer, including user layers; fab exports must name JLCPCB's layer set.

**Changed.**
- [04-pcbs/README.md](04-pcbs/README.md): a Tools section.
- [04-pcbs/workflow.md](04-pcbs/workflow.md): the tools replace "choose the EDA tool and fab house by decision", and `design/` is the KiCad project.

**Not changed.** No board is drawn. Each board folder still holds only its README.

**Unverified.** Freerouting on a dense two-layer board. JLCPCB's assembly checks on WLCSP and bottom-port MEMS parts (PCB-05, PCB-06), already open in audiosystem.md §6.

**Next.** Start stage 1 on the first board. When text-to-cad releases its KiCad support, decide whether boards move to `cadgen.pcb` scripts.

## D-059

**2026-10-14 · PCBs / PCB-15 component relief in the nose seat (CH-064; final v1 CAD) · ACTIVE; cut measured; schematic and layout not started**

**Why.** Freezing PCB-15's design inputs showed that the seat has room only for U1 and the three wire pads. On the front face, the only opening is the sensor notch. U1's SOT-23 pads fill it to local Z 3.9, which leaves 0.7 mm under the top edge, and that is too little for an 0402 part with its edge clearance. Behind the board, the slot leaves 0.1 mm per side, and the only open space is the lead groove, which the wire pads fill. The spec's C1, at local Y 5.2, falls outside the notch. Its R1 and C2, at local Z 1.0–2.0, face solid seat. The CAD drew the board as a plain block carrying only U1, so no check could see the problem. The datasheet requires C1.

**Options.**
- **A (chosen):** a relief pocket behind the board, with all three passives on the back face.
- **B:** the same pocket, with R1 and C2 moved to PCB-10. C1 still needs the pocket, and another board's spec would change.
- **C:** a taller board reaching above the seat top. It would run into the GP2Y pocket and the cap.

**Decision.**
- **Pocket:** cut from `BALL_POD_PRINTED_SEAT` at world X 125.7–126.6, Y 7.8–12.2, Z 30.3 to the seat top (Z 35). It is 0.9 mm deep behind the board's back face, open at the top, and joins the lead groove.
- **Parts:** C1, R1 and C2 all go on the back face. C1 sits behind U1 and connects to it through vias.
- **Back-face part zone, board-local:** Y 0.8–5.2, Z 0–4.6, parts at most 0.9 mm tall. 0402 parts with solder are about 0.55 mm.
- **Support:** the board's ends, local Y 0–0.8 and 5.2–6.0, still rest on the slot's back wall. The front slot wall still holds the board on either side of the notch.
- **Unchanged:** board outline, U1 position, notch and trip-point model.

**Where the cut lives.** The builder ruled on 2026-10-14 that droid CAD changes are made only in `final/v1/cad`. `DROID_CUTS` in [makad-v1.step.py](final/v1/cad/makad-v1.step.py) cuts the box from the seat when the droid is built. `body_chassis_model.py` and `body_v1_model.py` are unchanged, so the chassis checks (`check_layout.py`, `check_nose_joints.py`) do not see the pocket. Its own check is [check_pcb15_relief.py](final/v1/cad/check_pcb15_relief.py).

**Evidence (2026-10-14).** `check_pcb15_relief.py` run on the chassis tree, PASS:
- 13.304 mm³ removed. That equals the box less the slot strip and lead groove it overlaps, so the pocket opens into no other cavity.
- No seat material is left inside the box.
- A 0.6 mm shell around the pocket is solid.
- The seat is solid behind the slot wall at both board ends.
- Board-to-seat clearance is still 0.1 mm.

**Changed.**
- [makad-v1.step.py](final/v1/cad/makad-v1.step.py): `DROID_CUTS` and `_apply_droid_cuts()`.
- [check_pcb15_relief.py](final/v1/cad/check_pcb15_relief.py): new.
- [nose-hall-board.md](01-chassis/v1/research/nose-hall-board.md): C1, R1 and C2 placement.
- [pcb-15-nose-hall/README.md](04-pcbs/pcb-15-nose-hall/README.md): envelope, gap 1 closed.
- [04-pcbs/README.md](04-pcbs/README.md) and [workflow.md](04-pcbs/workflow.md): the rule that droid CAD changes go in `final/v1/cad`.
- [final/v1/README.md](final/v1/README.md): the folder now holds droid-level changes.

**Not checked.** Printability of the 0.9 mm open-top pocket. It has the same form as the existing 1.0 mm board slot.

**Next.** PCB-15 schematic, then a layout inside the back-face zone above.

## D-060

**2026-10-14 · PCBs / layout method: KiCad 10.99 nightly, no autorouter (all custom boards; [04-pcbs workflow](04-pcbs/workflow.md)) · ACTIVE; nightly and KiPy installed 2026-10-25; no board laid out**

**Why.** The builder supplied layout tips from someone else's experience of LLM-driven KiCad layout and ruled that they take priority over D-058 (2026-10-14).

**Decision.** When an LLM lays out a board:

- **Tool:** KiCad 10.99, the nightly build, which adds scripting features. Drive it through KiPy and computer-use tools. Replaces D-058's KiCad 10.0.6 as the layout tool.
- **No autorouter.** Freerouting and other autorouters are not used. Replaces D-058's autorouting bullet, including the full autoroute of small boards and the signal-net autoroute on power boards.
- **Placement:** place components one at a time or in small functional groups. Adjusting placement after routing is acceptable.
- **Routing:** octolinear traces, organised into buses of parallel, equally spaced tracks. Plan fanouts first. Keep detours and roundabout routes to a minimum, especially on signal nets. Size track widths and pours for each net's current.
- **Self-checks (optional):** write reusable scripts that check these routing properties, and use them to check the layout.

**Removed (2026-10-25).** At the builder's request, Freerouting is deleted from the machine: the 2.5.0 jar and its symlink in `~/.local/share/freerouting`, plus its settings and log under `~/Library/Application Support/freerouting` and `~/Library/Logs/freerouting`. The path in D-058 no longer exists. No Makad board was ever autorouted. The Homebrew OpenJDK it ran on is left installed.

**Unchanged from D-058.** `kicad-cli` ERC, DRC with `--schematic-parity`, fab and STEP outputs; JLCPCB as the default fab and assembler; each board's project in its folder's `design/`; the stage-3 STEP integration notes.

**Changed.**
- [04-pcbs/README.md](04-pcbs/README.md): Tools table and the *Layout rules* section.
- [04-pcbs/workflow.md](04-pcbs/workflow.md): tools line and stage 1 layout step.

**Installed (2026-10-25).** KiCad 10.99.0 nightly (build 20261024, `de08734017`) in `/Applications/KiCad-nightly`, beside 10.0.6 in `/Applications/KiCad`. Its `kicad-cli` ran ERC on a scratch copy of the PCB-15 schematic: 0 violations. The bundle has no Python framework, so the SWIG `pcbnew` module D-058's flow used is gone and boards are scripted only through KiPy against the running GUI. KiPy (`kicad-python` 0.8.0, Python 3.13) is in `~/.local/share/kipy/venv`, the API server is on in the 10.99 preferences, and KiPy connects (`GetVersion` returns 10.99.0-5923-gde08734017).

**Unverified.** Files saved by the nightly may not open in 10.0.6, so `kicad-cli` must come from the same install as the layout. KiPy's coverage of placement and routing in the nightly is untested.

**Next.** Install the nightly and KiPy, and repeat D-058's throwaway-board flow with hand routing before the first Makad board.

## D-061

**2026-10-25 · PCBs / fab-neutral design rules (all custom boards; [04-pcbs workflow](04-pcbs/workflow.md)) · SUPERSEDED by D-062**

**Why.** D-058 set JLCPCB as the fab and said layouts follow its limits. Importing from China adds courier duty: about 31% under heading 9804 since IGST fell to 18% in September 2025. A 30% anti-dumping duty on Chinese PCBs, in force since March 2024, may also apply. Brokerage is ₹500–3,000 on top. Indian fabs avoid all of that, and the builder ruled that every board should be makeable by either kind of fab.

**Decision.**
- Each board's layout meets the **strictest standard limit** of JLCPCB, Lion Circuits (Bengaluru) and PCB Power (Gujarat), 2-layer, 1 oz copper. The values and their sources are in the [04-pcbs README](04-pcbs/README.md#fab-neutral-design-rules).
- Each board carries them as a KiCad custom rules file, `design/<board>.kicad_dru`. KiCad applies it on top of the board's own settings, and the open PCB editor does not overwrite it.
- The fab is chosen **by quote at procure**: JLCPCB with duty, Lion Circuits and PCB Power, for the same revision. JLCPCB stays the default. A board goes elsewhere by decision, as D-058 says.
- Each board's order states the thickness tolerance its mounting needs. PCB Power's standard ±0.20 mm on 0.8 mm would not fit PCB-15's 1.0 mm slot.

**Not decided.** Assembly. Lion Circuits' PCBA minimum board size is 50 × 100 mm, and JLCPCB's is 10 × 10 mm, so small boards need panels either way. Whether a fab will assemble 0402 parts in prototype quantities is settled by quote.

**PCB-15 change.** Vias grow from 0.5/0.3 to 0.62/0.3 mm. The HALL_RAW via moves to (102.93, 103.95), wire pads P1–P3 move 0.05 mm down to keep 0.3 mm from the top edge, and R1 moves 0.19 mm right. DRC against the custom rules: 0 errors, 0 unconnected, schematic parity clean ([PCB-15 README](04-pcbs/pcb-15-nose-hall/README.md#layout)).

**Unverified.** Lion Circuits' minimum drill: its capabilities page gave 0.25–6.3 mm on 2026-10-25, while an earlier search snippet of the same page said 0.35 mm. The rule uses 0.3 mm (the spec's via). Confirm at quote. The limits were read from the fabs' web pages and none has been confirmed with a fab.

**Changed.**
- [04-pcbs/README.md](04-pcbs/README.md): new *Fab-neutral design rules* section; Tools row for JLCPCB.
- [04-pcbs/workflow.md](04-pcbs/workflow.md): stage 1 checks and stage 2 sourcing.
- [pcb-15-nose-hall](04-pcbs/pcb-15-nose-hall/README.md): `design/pcb-15-nose-hall.kicad_dru` and the re-routed layout.

## D-062

**2026-10-25 · PCBs / fab shortlist and design rules: JLCPCB, PCBWay, Lion Circuits MII (all custom boards; [04-pcbs workflow](04-pcbs/workflow.md)) · ACTIVE; PCB-15 re-laid to it, DRC clean**

**Why.** The builder ruled on 2026-10-25 that only three fabs will be used: Lion Circuits, JLCPCB and PCBWay. D-061 listed JLCPCB, Lion Circuits and PCB Power. It also took Lion Circuits' limits from the wrong column. Lion's capabilities page has three columns, one per service: **MII** (Make in India), **Custom** and **Rush**. D-061 used the Custom column (0.25 mm drill, 10 mil via spacing). MII is Lion's base service, and its Indian manufacture is the reason D-061 brought in an Indian fab: it avoids the import duty on Chinese boards. MII's limits are tighter (0.35 mm drill, 12 mil via spacing).

**Decision.**
- **Fabs:** JLCPCB (China, the default), PCBWay (China) and Lion Circuits (Bengaluru). No other fab is used. PCB Power is dropped.
- **Rules:** each layout meets the strictest standard 2-layer, 1 oz limit of JLCPCB, PCBWay and **Lion Circuits MII**, as the [04-pcbs README table](04-pcbs/README.md#fab-neutral-design-rules) lists them. Lion MII sets every via rule: hole ≥ 0.35 mm, annular ring ≥ 0.16 (pad ≥ 0.67), and via copper and hole ≥ 0.31 mm from other-net copper. Lion's "12 mil, via to trace" is read as via copper to trace, the stricter of the two readings, and the hole is kept 0.31 mm away as well. Hole to hole is also ≥ 0.31 mm.
- **Lion Rush is not a target.** Its 0.4 mm minimum drill and 8 mil tracks would grow every board. A board that needs Rush is checked against it first.
- Each board still carries the rules as `design/<board>.kicad_dru`. The fab is still chosen by quote at procure, from these three only, and a fab other than JLCPCB still needs a decision. D-061's *Not decided* (assembly) stands.

**PCB-15 change.** Vias grow from 0.62/0.3 to 0.67/0.35. C1 moves 0.2 mm left, to (102.55, 102.0). The GND via moves to (103.85, 102.02), and the HALL_RAW via to (103.05, 103.1), under U1 between pins 1 and 2. The +3V3 via moves to (101.2, 103.275). Every via also stays 0.16 mm from its own net's pads, a solder-mask web that keeps solder from wicking into the hole. A grid search over the board found the only legal via spots before the re-layout. DRC against the new `.kicad_dru`: 0 errors, 0 unconnected, schematic parity clean, and the same 4 nightly `lib_footprint_mismatch` warnings. A scratch copy with the hole minimum set to 0.4 mm flagged all three vias, which proves the rules file is enforced.

**Unverified.** The limits come from the three fabs' web pages, read 2026-10-25, and none has been confirmed with a fab. PCBWay's page gives no solder-mask web and states thickness tolerance only for boards 1.0 mm and thicker. PCB-15 is 0.8 mm in a 1.0 mm slot, so confirm the tolerance at quote.

**Changed.**
- [04-pcbs/README.md](04-pcbs/README.md): Tools row and *Fab-neutral design rules* table.
- [04-pcbs/workflow.md](04-pcbs/workflow.md): tools line and stage 2 quoting.
- [pcb-15-nose-hall](04-pcbs/pcb-15-nose-hall/README.md): `design/pcb-15-nose-hall.kicad_dru`, the re-laid board, Layout section and log.


## D-063

**2026-10-25 · Chassis / nose: PCB-15 and its slot move 0.4 mm back, so U1 clears the magnet at the cap stop (CH-064, CH-065; final v1 CAD) · ACTIVE; fit and relief checks pass; trip point to re-measure on the bench**

**Why.** PCB-15's stage-1 fit check ([check_pcb15_fit.py](final/v1/cad/check_pcb15_fit.py)) placed the KiCad board STEP in the nose seat. At the cap's 3 mm stop, the magnet face reaches the pod face, X 128.5. D-013 kept 0.1 mm of air there, but only for a 1.0 mm sensor block on a board that never moves in its slot. The real stack-up:

| Case | U1 top, world X | Air at the stop |
|---|---|---|
| D-013 placeholder, 1.0 mm block | 128.400 | +0.100 |
| Real part: 1.0 mm nominal, plus copper and solder, board at X 126.6–127.4 | 128.465 | +0.035 |
| KiCad's 1.2 mm SOT-23 model | 128.640 | −0.140 |
| TI DBZ0003A at 1.12 mm max, 0.88 mm board against the front slot wall | 128.705 | **−0.205** |

So a full press could drive the magnet into U1.

**Options.**
- **A (chosen, builder 2026-10-25):** move the board back 0.4 mm. The slot keeps its 1.0 mm width and the relief deepens with it.
- **B:** recess the magnet 0.4 mm into the cap and relieve the cap's inner face. This changes the cap and moves the magnet part.
- **C:** add stop ribs, so the stroke shrinks to 2.6 mm from D-013's 3 mm.

**Decision.**
- **Board:** world X 126.2–127.0, from 126.6–127.4. The outline, the U1 position in Y/Z and the PCB-15 design are unchanged.
- **Slot:** X 126.1–127.1, still 1.0 mm wide. Its back wall moves 0.4 mm back (cut X 126.1–126.5, Y 6.9–13.1). Its front wall moves 0.4 mm back beside the notch (material added at X 127.1–127.5, Y 6.9–8.3 and 11.7–13.1). The slot locates the board by itself, so no assembly care is needed.
- **Relief:** D-059's pocket deepens 0.4 mm to X 125.3–126.6 (1.3 mm). The back parts keep 0.25–0.50 mm of clearance.
- **Sensor notch:** unchanged at Y 8.3–11.7, Z ≥ 31.2. It now opens from the new front wall.

**Where it lives.** All in `final/v1/cad` ([makad-v1.step.py](final/v1/cad/makad-v1.step.py)). `DROID_CUTS` holds the deepened relief and the back-wall cut. Two new tables join it: `DROID_ADDS` unions in the front-wall material, and `DROID_MOVES` shifts the `BALL_NOSE_HALL_*` placeholder board and sensor 0.4 mm back. `body_chassis_model.py` and `body_v1_model.py` are unchanged, so their checks still see the D-013 slot.

**Evidence (2026-10-25).**
- `check_pcb15_fit.py`, PASS. With KiCad's model, U1's top is at X 128.240, which leaves 0.260 mm of air, and nothing touches the magnet or the cap at the stop. The real part has 0.435 mm nominal and 0.195 mm in the worst case (1.12 mm part, 0.88 mm board against the front wall). The board and all four parts clear the seat by 0.10–0.50 mm.
- `check_pcb15_relief.py`, updated and PASS. 17.896 mm³ net removed, which equals the cut boxes less the old slot and groove, less the added front wall, so no other cavity opened. Nothing is left in the pocket, and the 0.6 mm shell is solid. Both board ends are backed by the new back wall, and the front wall is solid. The notch is open, and the board-to-seat gap is 0.100 mm.

**Trip point.** The on-axis model for the Ø3 × 1.5 mm N35 magnet (Br 1.19 T, Hall plate 0.65 mm under U1's top) gives these numbers. The rest gap grows from 3.75 to 4.09 mm, and the field at rest drops from 19.7 to 16.1 mT. The +12 mT bench starting threshold trips at about **0.89 mm** of travel instead of 0.73 mm, which is still inside bench item 19's 0.4–1.2 mm window. At the stop the field (166 mT) is still past the linear range. These are model figures; the bench measurement decides.

**Not checked.** Printability of the 0.4 mm front-wall strips beside the notch, which are 1.4 mm wide and 4.7 mm tall in the printed seat.

**Changed.**
- [makad-v1.step.py](final/v1/cad/makad-v1.step.py): `DROID_CUTS`, new `DROID_ADDS` and `DROID_MOVES`, and `_apply_droid_cuts()`.
- [check_pcb15_relief.py](final/v1/cad/check_pcb15_relief.py) and [check_pcb15_fit.py](final/v1/cad/check_pcb15_fit.py).
- [nose-hall-board.md](01-chassis/v1/research/nose-hall-board.md): board position, retention and trip point.
- [pcb-15-nose-hall/README.md](04-pcbs/pcb-15-nose-hall/README.md): envelope and fit.
- [final/v1/README.md](final/v1/README.md).

**Next.** Bench item 19 measures the trip with the moved board. Stage 3 places the PCB-15 STEP at X 126.2–127.0.


## D-064

**2026-10-25 · PCBs / workflow order: design all boards first, then procure together (all custom boards; [04-pcbs workflow](04-pcbs/workflow.md)) · ACTIVE; PCB-15 rev A designed, its procurement waits for the batch**

**Why.** The workflow took each board through design, procurement and integration before starting the next. PCB-15 finished design on 2026-10-25, and the builder asked to design the other boards before buying any.
- **Cost.** Each import order from China pays shipping, about 31 % courier duty and brokerage ([D-061](#d-061)). PCB-15 is below every fab's assembly minimum and needs a panel anyway, so it can share a panel and an order with other boards.
- **Interfaces.** Boards connect to each other. PCB-10 is the far end of PCB-15's cable and carries the wire-break pull-up that PCB-15's design deferred to it. Both ends should be designed before either is bought.
- **Lessons carry over.** PCB-15's design traps are written down and handled in the tooling: KiPy's flip strips 3D models, F8 drops the position-file flag, the seat keep-outs work, and so does the fit check.

**Decision.**
- **Design first.** Boards are designed one at a time, each in its own session if the builder wants, to a committed revision with schematic, layout, fab outputs and board STEP, as stage 1 says. The suggested order runs from simple to complex: PCB-11, PCB-06, PCB-10, PCB-13, then PCB-05, PCB-09 and PCB-12, then the power boards PCB-02, PCB-03 and PCB-04. PCB-07, PCB-08 and PCB-14 each need a decision before they can be designed.
- **Then procure.** Stage 2 starts when the design batch is done. Boards on HOLD do not hold up the batch. Boards from the same fab go on one order, panelised together where that helps.
- **Then integrate**, as stage 3 says.

**Risk accepted.** No board is bench-checked until the batch is ordered, so a mistake common to several boards would surface late. Datasheet pinout checks, ERC and DRC with schematic parity, and the 3D fit check in each board's subsystem stay mandatory in stage 1.

**Changed.**
- [04-pcbs/workflow.md](04-pcbs/workflow.md): intro, stage 2 start and the PCB-15 row.
- [04-pcbs/design-playbook.md](04-pcbs/design-playbook.md): new. The per-board design steps proven on PCB-15.
- [04-pcbs/tools/kp.py](04-pcbs/tools/kp.py): new. The KiPy layout helpers, which restore models after a flip.
- [pcb-15-nose-hall/README.md](04-pcbs/pcb-15-nose-hall/README.md): stage 2 status.

## D-065

**2026-10-26 · Head / crown: PCB-11 status LED socket, LED part and circuit (CH-085; final v1 CAD) · ACTIVE; socket check passes; India V6 stock to confirm at procure**

**Why.** Freezing PCB-11's stage-1 inputs ([PCB-11 README](04-pcbs/pcb-11-status-led/README.md#inputs)) turned up five problems with the RP-06 selection (`HEAD-CAD-12`):

1. **Nothing holds the board or the light pipe.** The 5 × 5 × 0.8 mm board is a free block in the crown cavity, 0.49 mm from the crown's sloped wall. The Ø3.4 × 2.9 pipe sits at X −5.0…−2.1, entirely behind the 2 mm crown front wall (X −2…0) that carries its Ø3.6 bore, and touches nothing.
2. **The camera bracket's front lip** (`removable_camera_edge_bracket_trial`, X −8.6) sits 0.6 mm behind the left half of the board's back (Y 12.7–15.0). The spec's three back-face wire joints don't fit there.
3. **The BOM named the wrong LED.** CH-085 says WS2812B-2020-V6 but cites LCSC C965555, the pre-V6 WS2812B-2020, which is rated 3.7–5.3 V. The V6 is LCSC C52917434, rated 3.3–5.3 V. D1 powers the LED at 3.3 V.
4. **The V6 datasheet's application circuit gained a 100 nF VDD capacitor** (V1.1, 2025-12-01; V1.2, 2026-03-18). The spec had relied on the earlier "no external components" claim.
5. **No series resistor on the data line.** A broken 3V3 wire with GPIO6 high would push current into the LED's input clamp.

**Options (mounting).**
- **A (chosen, builder 2026-10-26):** a printed socket fused to the inside of the crown. It holds the board in a pocket and the pipe in a full-length bore.
- **B:** a sleeve only, with the board glued to its back end. Front parts would then have to move to the back's narrow right half.
- **C:** no CAD change, the board and pipe glued by hand. LED-to-pipe alignment would be uncontrolled.

**Decision.**
- **Socket** (`PCB11_SOCKET` in [makad-v1.step.py](final/v1/cad/makad-v1.step.py), head frame R). A 6.8 × 6.8 mm block from X −8.0 to −1.9, clipped to the crown's outer surface and fused into `front_bezel_integral_camera_crown`. Its 0.8 mm walls merge into the front wall and the sloped side wall. Inside it:
  - **Board pocket:** X −8.1…−7.2, 0.1 mm per side, open at the back. The board's front edge rests on a 0.5 mm shoulder all round.
  - **Front cavity** for the parts: board-local u, v 0.5–4.5 mm, 1.8 mm deep (X −7.2…−5.4).
  - **Pipe stop lip:** X −5.4…−5.0, with a Ø2.6 window.
  - **Ø3.6 bore** from X −5.0 into the crown bore. The pipe's position, X −5.0…−2.1, is unchanged.
- **Assembly.**
  1. Bond the light pipe in from the front until it rests on the lip.
  2. Fit PCB-11, already wired, into the pocket from behind and glue it at its edges (UV glue or CA).
  3. Fit the camera and its bracket last: the bracket lip covers part of the pocket mouth.
- **PCB-11 board.**
  - LED at the centre of the front face, inside the shoulder ring (u, v 0.5–4.5). C1 and R1 were placed beside it here; the layout amendment below moves them to the back.
  - The three wire pads go on the back's right half (u 2.3–5.0), and the wires leave straight back, rearward of X −8. Nothing goes on the back's left half.
- **LED part: Worldsemi WS2812B-2020-V6 only.** Worldsemi moved all WS2812B production to V6 on 2025-09-30. The datasheet footprint and pinout are unchanged.
  - **For fab assembly:** LCSC/JLCPCB **C52917434**, 783k in stock on 2026-10-26.
  - **In India:** only **Hubtronics** (Pune, SKU 07957, ₹10 incl. GST) lists the V6, and it showed 0 in stock on 2026-10-26. Confirm by RFQ before procurement.
  - **Not a substitute:** the pre-V6 WS2812B-2020 that Robu, Evelta, Hubtronics, Quartz Components, Punoscho and Sharvi stock fits the same footprint but is rated 3.7–5.3 V. It is not used on D1's 3.3 V. Using it would mean a 5 V feed to the crown, which is a new decision.
- **Circuit.**
  - **C1:** 100 nF X7R 0402 10 V across VDD–GND at the LED.
  - **R1:** 330 Ω 0402 in series with DIN at the LED. With the LED's 15 pF input this is a 5 ns time constant against the 220 ns shortest pulse.

**Where it lives.** All in `final/v1/cad`.
- `DROID_ADDS` now accepts a world-frame shape as well as a box. The socket is defined in head frame R and moved by `HEAD_ORIGIN_IN_CHASSIS`; at the neutral pose the head adds no rotation.
- `_apply_droid_cuts(strict=False)` lets the subsystem check scripts skip entries for parts outside their tree.
- `layout_model.py` and the head checks are unchanged, so they still see the free block.

**Evidence (2026-10-26).**
- [check_pcb11_socket.py](final/v1/cad/check_pcb11_socket.py), all 8 checks PASS:
  - **Fused:** the bezel gains 189.85 mm³, the socket less what the bezel already had, and stays one solid. Nothing pokes out of the crown skin.
  - **Board:** no overlap with the bezel. The shoulder is under all 8 ring points, all four walls are present, and the edge-to-wall gap is 0.100 mm.
  - **Front parts:** a 0.99 mm (maximum) LED leaves 0.81 mm to the lip, and 0.55 mm 0402s fit anywhere in u, v 0.5–4.5.
  - **Light pipe:** it rests on the lip with a 0.100 mm radial gap, the bore wall runs its full length, and the window is open.
  - **Nearest parts:** camera bracket 0.60 mm, camera 2.06 mm, skin 4.90 mm.
  - **Wire zone:** Y 15.0–17.7, back to X −34, is clear.
  - **Insertion path:** the way in from behind is blocked only by the camera bracket, which is fitted later.
- `check_pcb15_relief.py` and `check_pcb15_fit.py` still pass, with the same figures as D-063.

**Mass.** +0.19 cm³ of bezel material, about 0.2 g of ASA. This is below the head mass register's resolution and is not entered there.

**Not checked.**
- Printability of the 0.8 mm walls and the 0.4 mm lip in the bezel's print orientation.
- **Light bleed through ivory ASA:** 0.8–1.3 mm walls may glow. Paint the cavity matte black if the G03 bench shows a halo.
- The pipe's exit face sits 2.1 mm behind the crown face, as `HEAD-CAD-12` drew it. A pipe flush with the face would be an optics change.

**Supersedes (read-only per [D-001](#d-001), not edited).** The LCSC number C965555 in RP-06 [peripheral-selection.md §3](../02-prototypes/RP-06-cad/peripheral-selection.md#3-status-light--ws2812b-2020-behind-the-existing-light-pipe) and in RP-06 body-chassis layout-02 `india-availability.md`. The "built-in capacitor" and "three back pads" wiring there too.

**Changed.**
- [makad-v1.step.py](final/v1/cad/makad-v1.step.py): `PCB11_SOCKET`, `pcb11_socket_local()`, a `DROID_ADDS` entry, `_tool()`, and `_apply_droid_cuts(strict=)`.
- [check_pcb11_socket.py](final/v1/cad/check_pcb11_socket.py): new. [check_pcb15_relief.py](final/v1/cad/check_pcb15_relief.py) and [check_pcb15_fit.py](final/v1/cad/check_pcb15_fit.py): `strict=False`.
- [BOM.csv](BOM.csv) CH-085, [03-head/v1/BOM.md](03-head/v1/BOM.md) CH-085, the [04-pcbs register](04-pcbs/README.md#board-register), [workflow.md](04-pcbs/workflow.md), the [PCB-11 README](04-pcbs/pcb-11-status-led/README.md), [final/v1/README.md](final/v1/README.md) and the [sourcing matrix](../01-system/candidate-sourcing-matrix.md) status-light row.

**Amended 2026-10-26, at layout (builder's choice).** C1 and R1 move to the back's right half, beside the wire pads. Inside the 4.0 × 4.0 mm ring, the centred LED's courtyard (3.04 × 2.50 mm) leaves strips only 0.75 mm tall above and below it, but an 0402's courtyard needs 0.92–0.94 mm. The evidence above checked part heights against the cavity, not footprint areas. Other options were narrowing the shoulder to 0.3 mm (a socket change) or waiving courtyard overlaps. The socket and its check are unchanged, and the front now carries only the LED. C1 reaches the LED's VDD and GND through one via each, a loop of a few millimetres, which is fine for a 2 kHz, 36 mA load. Placement, routing and DRC are in the [PCB-11 README](04-pcbs/pcb-11-status-led/README.md#layout).

**Next.** Lesson 5: checks and outputs. At procure, RFQ Hubtronics for the V6, or have the fab supply C52917434. Run the G03 brightness, colour and stray-light bench with the socket printed.

## D-066

**2026-10-26 · Body / audio: PCB-06 L/R strap, mic source and sound-hole ring (BO-005, BO-012) · ACTIVE; PCB-06 board set up, placement next**

**Why.** Freezing PCB-06's stage-1 inputs ([PCB-06 README](04-pcbs/pcb-06-pdm-mic/README.md#inputs)) left two choices open:

1. **The LR strap.** The four boards are one design. Two mics on each ADAU7002 lane share a PDM data line, and each mic's LR pin picks the clock edge it drives on. FRONT_L and REAR_L strap LR to GND; FRONT_R and REAR_R strap it to 3V3 ([audiosystem.md §2.2](02-body/v1/research/audiosystem.md#22-how-the-four-mics-share-two-converters)). If both mics on a lane carry the same strap, they drive the line on the same edge.
2. **The mic's source.** BO-012 names element14 India 4125831. On 2026-10-26 its 19,310 parts are listed as **UK stock** (delivery 4–6 business days), and no stock held in India was found (Evelta, Hubtronics). JLCPCB, meanwhile, now stocks the part itself (C5563886, 4,561 in stock), where the BOM had recorded 0.

**Options (strap).**
- **A1 (chosen, builder 2026-10-26):** an assembly variant. Two 0402 footprints, and the fab fits one.
- **A2:** a three-pad solder jumper bridged to GND in copper. The R boards are cut and re-bridged by hand.
- **A3:** an open jumper bridged at install. An unbridged board leaves LR floating and spoils its lane.

**Options (source).**
- **B1:** the fab buys the mic from its own stock (JLCPCB C5563886, or Lion Circuits on MII).
- **B2 (chosen, builder 2026-10-26):** the builder buys it from element14 India and supplies it. The builder counts element14 India as an India source, even when it ships from UK stock: it invoices in rupees and handles the import itself.

**Decision.**
- **Strap.** Two 0402 footprints on PCB-06: **R_L** from LR to GND and **R_R** from LR to 3V3, each **1 kΩ**, and exactly one fitted per board. LR is a static CMOS input, so 1 kΩ holds it firmly, and fitting both by mistake can't short the mic rail. One Gerber set, two placement variants: L (R_L fitted) for FRONT_L and REAR_L, R (R_R fitted) for FRONT_R and REAR_R. Two BOM/CPL sets, or one panel that mixes L and R boards: settle that at the fab outputs. The fitted resistor marks which board is which. Either footprint's pads can also be bridged with solder by hand, which serves as a fallback.
- **Source.** The builder orders BO-012 from element14 India 4125831 and supplies the parts to whichever fab assembles PCB-06 (D-062; check each fab's consigned-parts terms at procure), or reflows them by hand. Order quantity follows the number of boards at procure (element14's price drops from ₹305.52 to ₹232.24 at 10). JLCPCB's own stock is not used.

**BOM changed:** [`BOM.csv`](BOM.csv) BO-005 (strap variants, fab route), BO-012 (element14 stock and route of 2026-10-26; MSL 1). [`02-body/v1/BOM.md`](02-body/v1/BOM.md) is updated to match.

**Also confirmed by the builder (2026-10-26), outside the decision:** C1 1 µF and C2 100 nF at VDD, and R1 100 Ω on DATA (all datasheet values; the spec had 0.1 µF and an estimated 33 Ω).

**Unverified:** element14 stock and price at order; the fab's handling of consigned parts for a reflow-only bottom-port MEMS part (no-clean, no wash); which edge the ADAU7002 calls left, which the array tap test settles. A wrong guess only swaps a lane's channels in software.

**Next.** PCB-06 lesson 2: the schematic.

**Amended 2026-10-26, at board set-up (builder's choice, option C2).** Infineon's land pattern (Fig. 13) puts MK1's GND seal ring 0.18 mm from the Ø0.8 non-plated sound hole (ring R 0.58, hole R 0.40). That is under JLCPCB's published "NPTH to track 0.2 mm" and the fab-neutral 0.31 mm ([D-062](#d-062)); PCBWay and Lion Circuits publish no NPTH-to-copper limit. The project footprint pulls the ring's inner edge to **R 0.63** (0.23 mm from the hole). The seal still covers 0.37 of the 0.40 mm of the mic's own port ring (R 0.6–1.0). A rule in `pcb-06-pdm-mic.kicad_dru` gives that one hole 0.2 mm; every other hole keeps 0.31. The other options were: keep the datasheet's 0.18 mm with an exception (C1); 0.31 mm, fab-neutral, with a 0.29 mm seal (C3); or plate the hole, which risks solder wicking in and narrowing the port (C4). **Unverified:** PCBWay's and Lion Circuits' acceptance, in their DFM checks.

## D-067

**2026-10-27 · Body / audio: PCB-05 inputs, mounting and CR-01 (BO-002, BO-006, BO-064 new; final v1 CAD) · ACTIVE; PCB-05 rev A designed, 4 layers (amended at routing), fit check passes**

**Why.** Freezing PCB-05's stage-1 inputs ([PCB-05 README](04-pcbs/pcb-05-audio-front-end/README.md#inputs)) left the open items of [audiosystem.md §6](02-body/v1/research/audiosystem.md#6-open-items-for-the-pcbs), two new ones from the datasheets, and one from the CAD:

- **Datasheets.** The MAX98357A (ADI Rev 16) rates DIN, BCLK and LRCLK to 6 V whatever VDD is, so the Pi can stream into an unpowered amp. SD_MODE is rated only to VDD + 0.3 V; the datasheet's remedy is about 2 kΩ in series. ADAU7002 Fig. 12 latches L on the rising edge, which matches the PCB-06 straps (IM73D122 Table 8: LR = GND is L).
- **CAD.** `COMPUTE_SHIFT_X` moved the Pi and cooler 10 mm forward after PCB-05 was placed. The Pi's USB jacks are now 2.10 mm under the board, and the compute tray, which slides in from the front 2 mm high (D-042), passes 0.10 mm under it. PCB-05 had no fixing.

**Decision** (builder, 2026-10-27, the recommended option of each):

- **A. 5 V on W12 only.** The GH 10 (`W26`, `J9-3` → `J5-1`) carries signals, the Pi's 3V3, two GND and a spare. 5 V on it could only come from the Pi's header 5 V and would bypass `PB-AUDIO-OUT`'s e-fuse and its CHARGE-off.
- **B. `CA-06` CR-01 accepted:** GPIO22 → I²S0 SDI1, GPIO23 → `AMP_SD` (plain output, default low). RP1's function table gives GPIO22 `I2S0_SDI[1]` as function 2. No collision with UART0/2, I²C1, SPI0 or CR-02 (GPIO24 `FAN_EN`, D-042). RP-02 `compute-control-architecture.md` is read-only ([D-001](#d-001)); this entry is the acceptance.
- **C. No power-good path.** `AMP_SD` drives SD_MODE through **2.2 kΩ**, with the 100 kΩ pull-down kept (the chip has its own 100 kΩ). A 3.0 V high gives 2.87 V at SD_MODE, above B2 (1.5 V max): left channel. With the branch off, the pin current is about 1.2 mA, under its 20 mA rating. The 100 Ω resistors on BCLK/LRCLK/DIN stay as edge damping. An **unfitted** 5V-present divider goes on the `J5-1` spare pin, so a later `CA-06` change can bring it to the Pi without a new PCB-05.
- **D. Mic map:** `J5-2` REAR_L, `J5-3` FRONT_L, `J5-4` REAR_R, `J5-5` FRONT_R (within D-037's +Y/−Y split). ADAU7002 #2 (SDI1) sits between `J5-2` and `J5-4`, #1 (SDI0) between `J5-3` and `J5-5`.
- **E. Mounting: hung from the frame.** Three **Würth 9774080243R** M2 SMT steel spacers (Ø4.35 × 8 mm, through thread, element14 India 2497611) reflowed on the board's top face at world **(48.5, ±11.0)** and **(63.0, 0.0)**, board-local (3.5, 30.0), (3.5, 8.0) and (18.0, 19.0) from the corner at (45, −19). Printed bosses (Ø7) on `BODY_FRAME_MAIN_PRINT` come down to the spacer tops at Z 123.6: 2.4 mm under the front upper cross rail, 10.4 mm under the yaw plate. **ISO 7380 M2** screws (BO-064, new) go down from above through Ø2.4 bores: two M2 × 16 from Ø4.0 × 1.5 counterbores in the rail top (Z 134.0), under the yaw housing seat (Z 135.5, R36.6), and one M2 × 20 from the yaw plate top (Z 138.0), which is open above. Each ends 5.6 mm into its spacer (tip Z 118.0). 0.2 N·m maximum (the spacer's rating).
- **F. Mic rail filter:** ferrite bead (600 Ω at 100 MHz, 0603, DCR ≤ 0.5 Ω) + 2.2 Ω + 10 µF from the Pi 3V3, with 100 nF at each ADAU7002 and mic connector. Passive, so never above the Pi's 3V3 or the parts' 3.6 V limit. The 2.2 Ω takes the bead/capacitor resonance (about 34 kHz) from Q 1.6 to 0.12. About 9 mA load; 40 mV drop at 15 mA.
- **G. Two layers**, 1.6 mm, near-solid ground plane on the bottom, which carries no parts. The ADAU7002's eight balls are all on the outside of its array and fan out on the surface.

**Assembly** (adds to the body CAD order): after the compute tray, PCB-09 and its plugged leads, and before the yaw cartridge: slide PCB-05 in from the front, 1 mm low over the Pi's USB jacks, lift it onto the bosses and drive the three screws from above (1.3 mm hex key). The rear pair is then covered by the yaw cartridge housing; removing PCB-05 later means lifting the cartridge. Plugging and unplugging the leads does not.

**Options not taken.** A2: 5 V on the GH 10 as well. C2: fit the divider to a Pi GPIO now (CR-03, PCB-09 trace); C3: a 74LVC1G08 interlock on SD_MODE. D2: `J5-2`/`J5-4` front. E2: card guides from the rail with one front screw; E3: posts from the compute tray in front of the Pi (board grows to X 81, blocks the USB/Ethernet jacks). F2: a 3.0 V LDO. G2: four layers.

**CAD:** [`makad-v1.step.py`](final/v1/cad/makad-v1.step.py) `PCB05_MOUNT`: `DROID_CUTS` (three bores, two counterbores) and `DROID_ADDS` (three bosses) on `BODY_FRAME_MAIN_PRINT`, and the three spacers on `PCB05_AUDIO_FRONT_END_PCB` (they are part of the assembled board). The screws are modelled only in the check. New [`check_pcb05_mount.py`](final/v1/cad/check_pcb05_mount.py): 7/7 pass (about 28 min, most of it the install sweep). The bosses fuse into the one frame print (volumes compared round each point, exact). The three bores are open with full 1 mm walls (10.4, 10.4 and 14.4 mm of print). Each screw ends 5.6 mm into its spacer; the rear heads sit 0.40 mm under the yaw housing, with the counterbore edge at R36.31 inside the R36.6 seat. The spacers are 0.88 mm from the `J5-2`/`J5-4` headers (their Ø5.3 solder rings 0.40). The nearest other part is 0.40 mm away (a rear screw head to the yaw housing). The board, spacers and J5 headers slide in from 40 mm in front, 1 mm low, and lift into place, at least 0.50 mm from every part fitted by then. The driver paths are open from above; the rear pair is later covered by the yaw cartridge and its clamp ring, the front one stays open. An earlier run found the bosses' 0.2 mm overlap into the frame stood proud of the cross rail's rear face; the bosses now end at the frame's underside.

**BOM changed:** [`BOM.csv`](BOM.csv) BO-002 (circuit, map, mounting), BO-006 (W26 without 5 V, W27 map), **BO-064 new** (3 × ISO 7380 M2 screws). [`02-body/v1/BOM.md`](02-body/v1/BOM.md) and [audiosystem.md](02-body/v1/research/audiosystem.md) §1.3, §2.1, §2.3, §2.4, §4.2 and §6 are updated to match.

**Mass:** about +3 g (three steel spacers about 0.6 g each, three screws, bosses), not yet in `BODY_AUDIO`'s hand-kept 6 g PCB-05 estimate; update it with the weighed board at stage 3.

**Unverified:** PDM_CLK duty at the mics (48–52 % above 3 MHz; not in the ADAU7002 datasheet); the Pi 5 3V3 rail's maximum; the fabs' placement of an 8 mm spacer from 24 mm tape and of the 0.4 mm WLCSP (JLCPCB requires X-ray; Lion Circuits MII unverified); printed boss strength under 0.2 N·m and plug mating forces; the real lead routing over PCB-09's top-entry plugs (stage 3).

**Next.** PCB-05 lesson 2: the schematic, with the `J5-1` pin order.

**Amended 2026-10-27, at board set-up (builder's choices H1 and I1).** Setting up the PCB-05 board ([README](04-pcbs/pcb-05-audio-front-end/README.md#layout)) found two parts that broke the envelope or the fab rules:

- **H1: `J5-7` stays the through-hole Molex 43650-0200, with its tails clipped.** Its pins sit 9.9 mm in from the −Y edge, over the Pi's USB stack (2.10 mm below the board). Molex's 3.18 mm tails come about 1.6 mm out of a 1.57 mm board, about 0.5 mm from the jack, and the Ø3 snap-in peg about 0.4 mm. After soldering, both tails are clipped to ≤ 0.5 mm below the board and the peg is cut flush, leaving about 1.2 mm: an assembly note on J7 and the fab order, or the builder solders J7 by hand. The board's `USB_JACKS_NO_THT_1` rule area is notched round J7's position only. Not taken: H2, the surface-mount 43650-0212 (15.2 mm wide with its tabs; about 11 mm is free beside `J5-5`); H3, swapping `J5-7` with `J5-4` (spacer H2 is there).
- **I1: the spacer holes are plated.** KiCad's stock Würth land pattern has its solder ring at the Ø3 non-plated hole's edge (0 mm; anchor pads 0.254 mm), against JLCPCB's 0.2 mm and the fab-neutral 0.31. The project footprint `pcb05:Wurth_WA-SMSI-M2_H8mm_9774080243_PTH` plates the hole as pad 1, so the ring is its annular ring: ordinary for every fab, and more solder area. Nothing passes through the hole. Spacer H3 sits over the USB stack; its ring is flush, so the rule area is notched round it too. Not taken: I2, the ring pulled back to R 1.81 (59 % of the solder area; about 22 MPa shear at the rated 0.2 N·m against about 14); I3, a DRC exception.

DRC re-run: the empty board is clean; on a scratch copy, J7 at its CAD position and the plated spacers pass, and the same header anywhere else over the jacks is still flagged. **Unverified:** the tail clipping on the received boards (measure the bottom), and whether the fab will clip (else the builder fits J7). BO-002 is updated.

**Amended again 2026-10-27, at placement (builder's choice J1).** Placing the fixed parts on the board showed the lesson-1 fixing collided with the real footprints: spacer H1's Ø5.3 ring overlapped `J5-2`'s signal pads (and H2 `J5-4`'s) by up to 0.1 mm, and both spacers' Ø5.8 courtyards overlapped `J5-1`'s and `J5-2`/`J5-4`'s. The mount check had measured the spacers against the CAD's connector bodies; the GH footprints' pads run 1.1 mm further inboard than those bodies. The Micro-Fit's housing is also 9.65 mm wide (Molex SD-43650-001), not the placeholder's 7.26.

- **J1: three points in a new triangle.** H1 rear at **(48.5, 9.8)** under the cross rail (counterbore edge R35.95 inside the R36.6 seat); H2 and H3 front at **(61.3, ±9.8)** under the yaw plate, open above until the yaw cartridge is fitted (a Ø5 driver path clears the shell by 4.8 mm; the cartridge's flange then covers them, as it covers the rear screw, so removing PCB-05 means lifting the cartridge). Board-local (3.5, 28.8), (16.3, 28.8), (16.3, 9.2). Screws: one M2 × 16 from a counterbore in the rail top (rear), two M2 × 20 from the yaw plate top (front). **BO-064 becomes 1 × M2 × 16 + 2 × M2 × 20.** The rear corners cannot hold a second spacer: `J5-1`'s 17 mm courtyard and the corner headers' leave 4.3 mm each side for a 5.8 mm courtyard, and the counterbore limit (inside R36.6) keeps the spacer at X ≤ 48.9.
- **`J5-1` slides 2.0 mm toward −Y** (centre Y −2.0); its plug reaches 0.9 mm past the old rear plug reserve, which moves with it. **`J5-7` moves 1.5 mm forward** to fit its real 9.65 mm housing (X 64.8–74.46, inside the −Y plug reserve). **`J5-2`, `J5-4` move 0.225 mm toward −X and `J5-6` 0.225 mm toward +X**, so the GH footprints' courtyards stop touching.
- Not taken: J2, two rear spacers with `J5-1` split into two GH 5 (changes W26 and PCB-09 `J9-3`); J3, the old points with a smaller custom ring and accepted courtyard overlaps (copper 0.1 mm from `J5-2`'s pads).

**CAD:** `PCB05_MOUNT` takes the new points (`rear=1`, one counterbore); `DROID_MOVES` moves the `J5-1`, `J5-2`/`J5-4` and `J5-6` headers, plugs and the rear plug reserve; `DROID_ADDS` widens the `J5-7` header and plug blocks to the real housing. `check_pcb05_mount.py`: 7/7 pass. The bosses fuse into the one frame print (local volumes exact). The three bores are open with 1 mm walls (10.4, 14.4, 14.4 mm of print). Each screw ends 5.6 mm into its spacer; the rear head sits 0.40 mm under the yaw housing, its counterbore edge at R35.95 in the R36.6 seat. The spacers are at least 1.03 mm from every CAD connector (their solder rings 0.55). The board slides in from the front 1 mm low and lifts into place with at least 0.50 mm to every part fitted by then. The driver paths are open from above; the yaw cartridge covers all three later. The first run failed the slide on the CAD's 10 mm `J5-7` block, which met the front −Y boss; the real Micro-Fit is 6.98 mm tall mated (Molex), 1.0 mm under the boss, so the block is cut to that height (`DROID_CUTS`). **Board:** the USB rule areas are re-notched round J7 and spacers H2/H3 (both sit over a USB stack; their plated rings are flush). Placement DRC: no copper, clearance or courtyard violations.

**Lesson:** an envelope check against CAD placeholder bodies is not a footprint check. Fixings and connectors are now checked against the real footprints' pads and courtyards in KiCad as soon as they are placed (added to the playbook's traps).

**Amended again 2026-10-27, at routing (builder's choices L2 and the `J5-1` reorder).** Routing the left half on two layers needed a crossing at each converter (the ADAU7002's BCLK and LRCLK balls are neighbours on one side while both clocks run on to the next chip) and one for every mic feed to the far edge (each converter serves a header on the +Y and on the −Y edge, across the clock bus): about 12–16 hops through the bottom ground plane, slotting it under the clock lines. G1 had been chosen on the WLCSP fan-out alone.

- **L2: four layers**, 1.6 mm: F.Cu parts and signals, **In1.Cu solid GND**, In2.Cu GND, B.Cu signals (still no parts). 35 µm outer, 15.2 µm inner copper, 0.2104 mm prepreg and a 1.065 mm core (the JLCPCB 7628 build). Every crossing becomes a via to B.Cu over an unbroken plane. The fab-neutral rules stand: Lion Circuits' MII service makes 2 and 4 layers with the same 6/6 mil, 0.35 mm drill, 12 mil via-to-trace and 1 oz limits; JLCPCB's and PCBWay's 4-layer limits are looser. Not taken: L1, two layers with the hops; L3, re-pairing the mic lanes by side (removes the feed crossings only, and changes the PCB-06 variant positions and the ALSA map).
- **`J5-1` reorder: 1 +3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 spare (5V_SENSE).** LRCLK above BCLK, the order both converters' balls and the amplifier's inputs have, so the bus leaves `J5-1` without a crossing; BCLK keeps a ground on each side. SDI1 above SDI0 (set while routing): U2, the nearer converter, takes the upper In2 row, so U1's longer row passes under U2's drop without a crossing. W26 and PCB-09 `J9-3` follow (PCB-09 is not designed yet).

The amplifier corner routed on two layers carries over unchanged. **BOM changed:** BO-002 (4 layers). **Unverified:** each fab's 4-layer price and its DFM on this board.

## D-068

**2026-10-27 · Body / electronics: PCB-10 C3 carrier inputs, mounting, DevKitC and parts (CH-044, CH-045; final v1 CAD) · ACTIVE; `check_pcb10_mount.py` passes; PCB-10 inputs frozen, schematic next**

**Why.** Freezing PCB-10's stage-1 inputs ([PCB-10 README](04-pcbs/pcb-10-c3-carrier/README.md#inputs)) in the built body CAD found:

- **The two upper M2.5 screws (Z 116) sit under the DevKitC.** Once it is soldered on, no driver reaches them, so the carrier and DevKitC could not go in as one module (`CN-06`).
- **The DevKitC's pin tails land on the printed uprights.** Neither CAD model has header pins; 14 joints stand 4 mm or more proud of the back face, where the uprights bear on it.
- **The CAD DevKitC is a generic board's STEP** (FreeCAD model, rows 25.4 mm apart on a 28.3 mm board). Espressif's v1.1 drawing has rows **22.86 mm** apart on 25.40 mm, USB fronts 8.0 mm past pin 22, and Espressif's own KiCad footprint (`espressif/kicad-libraries`, `ESP32-S3-DevKitC`) agrees. Espressif publishes no 3D model. On v1.1 the RGB LED is on **GPIO38**, not 48, and the 5V header pin is `VCC_5V` after the USB Schottky diodes, so a service USB cable back-feeds `J10-1`.
- **TPS3436CFDBEDDFRQ1 (`BD-10`) cannot be bought**: none in India (element14 India lists no TPS3436), none at LCSC/JLCPCB, out of stock at TI, and 0 at Mouser (Findchips, 2026-10-27). The builder reports DigiKey does not ship to India. **THVD1451** is not on element14 India; JLCPCB stocks only the VSON-8.

**Decision** (builder, 2026-10-27: "do whatever you feel is best"; Espressif's board only; the TPS from the next best source):

- **A. Mounting: two screws and two hooks** (CAD below). The upper screws and their inserts are deleted. Each upright gets a hook over the board's top edge (lip 1.7 mm thick, 0.1 mm off the front face, 1.9 mm engagement; bridge 0.1 mm over the edge, tied into the upper rail) and a relief under both header rows (3 mm deep, from 3.7 below to 1.75 above each row). The module goes in 2 mm low, slides up under the hooks, and the two Z 86 screws fix it. DevKitC pin tails are clipped to 1.5 mm after soldering. **Assembly order:** the module goes on before the compute tray; with the tray in, a driver still has 17 mm of reach to the lower screws (enough for a 1.5 mm L-key's short leg), so service does not need the tray out.
- **B. DevKitC: genuine Espressif ESP32-S3-DevKitC-1-N8, board v1.1, no clones** (CH-045). Bought in India with a GST invoice: Tech Depot ₹2,273.70, Sharvi ₹1,678.45 + GST, Compoindia ₹2,410 + GST. The carrier uses Espressif's footprint, with the drill opened from 0.8 to about 1.0 mm (the pre-soldered 0.64 mm square pins are 0.9 mm across the diagonal; settled at the footprint). The final CAD replaces the generic STEP with a v1.1 model built from Espressif's drawing (board, WROOM-1 module, two USB-C, header plastic, 44 pins), keeping the subsystem's pin columns.
- **C. Watchdog: TPS3436CCCBGDDFRQ1**, the fallback `BD-10` already names (RP-02 board-specs §7), for PCB-10 and PCB-12. Same pinout C and DDF package, so the footprint is unchanged. Timing: 500 ms startup delay, tWC 5 ms, open ratio 4 at `SET[1:0]` = 00 (tWO 15 ms), 200 ms `WDO` assert. Feed window 5.5–18 ms, late fault at most 22 ms after the last edge (was 44), feed every 10 ms: every second 200 Hz hazard cycle. **The first `WDI` edge must come within 500 ms of power-up** (firmware: feed from early boot; `MCU_RDY` still stays low until a healthy loop). Stock 2026-10-27: Mouser 1,710 (595-S3436CCCBGDDFRQ1, US$3.25 each), DigiKey 8,239. **Source: Mouser India** (mouser.in, Mouser Electronics (India) Pvt Ltd, INR). With a GST business invoice Mouser ships DDP and pays the duty; on a standard (card) invoice it ships FCA and duty and GST are collected at delivery. The builder chooses which at the order.
- **D. Base-link transceiver: SOIC-8 footprint** taking either THVD1451DR (`CA-05` lead; Mouser India with the watchdog) or MAX3490EESA+ (element14 India 2518822, same pinout, 12 Mbps; open-input fail-safe only, so its idle-bias resistor footprints are fitted only with it).
- **E. USB back-feed:** a Schottky diode from `J10-1` to the DevKitC 5V pin; the GP2Y stays on the `J10-1` side.
- **F. Defaults adopted:** GPIO map v0.2 (`HALL_OUT` GPIO10, `TCRT_LED_EN` GPIO47, IMU `INT2` not connected, GPIO38 left to the LED); `J10-2` pairs named by direction (`C3TX±`, `C0TX±`) so `W25` is wired 1:1, recorded at PCB-09 and 05-harness §5.2; `J10-8` and `J10-10` orders kept; `MR` pulled up; 10 µF at both ends of the GP2Y feed; `JP_SVC` reachable outside the DevKitC's shadow.
- Not taken: a socketed DevKitC (lifts it into the Pi USB-C plug reserve, 1 mm away); upper screws above the DevKitC (2.45 mm free); a slower India-stocked watchdog (TPS3813, MAX6323: windows of hundreds of ms against `BD-10`'s tens).

**CAD** (`final/v1/cad/makad-v1.step.py`): `PCB10_MOUNT`; `DROID_CUTS` (four reliefs) and `DROID_ADDS` (two lips, two bridges) on `BODY_FRAME_C3_CARRIER_UPRIGHT_1/2`; two new edit kinds, `DROID_REMOVES` (the generic DevKitC STEP, its header blocks and the upper screws) and `DROID_INSERTS` (the v1.1 DevKitC into `C3_CARRIER_PCB10_WITH_DEVKITC`), both strict like the others. **`check_pcb10_mount.py`: 8/8 pass**, including pins 1.38 mm from the uprights through the slide, hooks 0.55 mm from the DevKitC, the slide clear, approach clear to 5.0 mm from the wall (then PCB-08), screws reachable, and the DevKitC 2.95 mm from the frame. Information only: the v1.1 board's USB end now reaches into `C3_DEVKITC_USB_SERVICE_CORRIDOR_KEEP_OUT` (as intended) and touches `HARNESS_HEAD_RISER_LOWER` (0.5 × 0.6 mm), which already crossed the corridor. Re-route the head riser at stage 3. The subsystem source and its checks still have the clone and four screws.

**BOM changed:** CH-044, CH-045. **Unverified:** the received board's revision and bottom-side protrusions; hook strength and print orientation; the 500 ms first-feed on real boot times; Mouser's stock on the order date.

**Amended 2026-10-28 (PCB-10 board set-up): the board grows 6 mm down for a third connector row.** The real connector footprints, placed at the CAD positions on a scratch board, gave 23 courtyard overlaps in KiCad DRC. The CAD's GH rows are 6 mm apart against a 6.6 mm courtyard, and the real Micro-Fit `J10-1` (9.65 × 9.9 mm, Molex SD-43650-001) is larger than its 7.26 mm placeholder and lands on three GH headers.
- **Board 70 × 49.5 mm (Z 76–125.5), notched** over the right DRV8833's terminal block (chassis; X 43.5–50.5, top Z 76.1, 0.11 mm in front of the board plane): the bottom edge steps up to Z 79 over X 42.5–51.
- **Three rows:** A `J10-7`, `J10-3`, `J10-4`, `J10-10`; B `J10-2`, `J10-5`, `J10-6` (with the screws); C `J10-12`, `J10-8`. `J10-1` keeps its right-angle Micro-Fit mating +X and spans B and C, housing Z 78.6–88.26. Positions in the [PCB-10 README](04-pcbs/pcb-10-c3-carrier/README.md#board-set-up), proved by KiCad DRC.
- **CAD:** `PCB10_GH`, `PCB10_J10_1`, `PCB10_BOARD_GROWTH` in `makad-v1.step.py`: the board and the plug-layer reserve grow (`DROID_ADDS`), the headers, plugs and `J10-1` reserve move (`DROID_MOVES`), and the `J10-1` blocks are replaced by the real housing (`DROID_REMOVES`/`INSERTS`). **`check_pcb10_mount.py`: 9/9 pass**, with the grown board 0.52 mm from the terminal block and `J10-1` 0.7 mm above it.
- **Harness (stage 3):** `J10-8`, `J10-12` and `J10-10` moved, so the `HARNESS_NOSE_J10_8_*` and `HARNESS_REAR_TCRT_J10_10_*` drops need re-routing with the head riser. Mass: about +0.9 g of board, inside the 20 g `C3_CARRIER_PCB10` row's estimate.
- **Lesson:** a CAD connector row is not a footprint check. Place the real footprints at the CAD positions on a scratch board before trusting a placeholder layout, and survey the chassis as well as the body below a board (playbook PCB-10 traps).

**Amended 2026-10-28 (PCB-10 placement): four layers, J10-2 order, GPIO map v0.3.**
- **Four layers** (builder, the recommended option): F.Cu parts and signals, **In1.Cu solid GND**, **In2.Cu +3V3 plane**, B.Cu signals with no parts; 1.6 mm, 35 µm outer and 15.2 µm inner copper, 0.2104 mm prepregs and a 1.065 mm core (PCB-05's build). Why: under the DevKitC the front is full of parts and a fence of 44 header pins splits the board from the three connector rows; on two layers the +3V3 and GND networks (about 40 points) and about 25 crossing signals would not route without long detours and a broken ground return. With the planes every supply pad is one via, and only signals are routed. The fab-neutral rules stand (all three fabs make 4 layers to the same limits, as for PCB-05).
- **`J10-2` reordered** to 1 GND, 2 `C0TX+`, 3 `C0TX−`, 4 `C3TX−`, 5 `C3TX+`, 6 spare: U2's own pin order seen from J2, so the pairs run straight (PCB-09 `J9-2` and 05-harness §5.2 follow).
- **GPIO map v0.3**: the roles of v0.2, with the pins reassigned so each track runs from its DevKitC pin to its connector without crossings (table in the PCB-10 README). Same rules: no strapping or USB pins, analog on ADC1, at least two safe spares (35, 39, 40).

## D-069

**2026-10-29 · Body / electronics: PCB-13 charge inlet inputs (BO-015; final v1 CAD) · ACTIVE; `check_pcb13_relief.py` passes; PCB-13 inputs frozen, schematic next**

**Why.** Freezing PCB-13's stage-1 inputs ([PCB-13 README](04-pcbs/pcb-13-charge-inlet/README.md#inputs)) against the makers' datasheets and the built droid CAD found:

- **The pin relief is narrower than GCT's land pattern.** D-040 cut the relief in the rear-panel inlet pad 9.60 mm wide (`CHARGE_INLET_PIN_RELIEF`, Y ±4.80). GCT's recommended layout (USB4140 drawing A3, 29/08/24) puts the outer shell-stake copper at Y **±4.87**. Probing the real land pattern against the built panel gave 0.005 mm³ of overlap for the copper alone and 0.032 mm³ with a 0.3 mm fillet. So PCB-13 would sit on two solder fillets, not flat on its seat. The inner stakes and the SMT pad row clear in either orientation.
- **J1 is the only part on the −X face**, so a fab-assembled board would be two-sided.
- **The board carries 3 A** (J1's `VBUS` rating; 1.38 A normal), the first to do so.
- **JLCPCB/LCSC cannot supply the actives:** USB4140 0 at JLCPCB, STL6P3LLH6 1, and no genuine TI TVS2200 (clones only). element14 India has the USB4140 (3955430), STUSB4500 (2980889), STL6P3LLH6 (3132757) and ESDA25W (2341655). Mouser India has the TVS2200DRVR.
- **PCB-02's −X face is 3.9 mm from PCB-13's +X face**, over the whole board.

**Decision** (builder, 2026-10-29, gaps 1–5 of the PCB-13 inputs):

1. **Relief 10.60 mm wide** (Y ±5.30), Z 5.60 and depth 1.2 unchanged. That leaves 0.43 mm from the copper to the wall and 4.9 mm of print to the screw pilots.
2. **J1 is hand-soldered by the builder**: the six SMT tails, which reach 0.62 mm past the shell, and the four stakes from the +X side. The fab assembles the +X face only. J1 is left out of the fab's BOM and position file, and the builder buys it.
3. **Copper: 1 oz on two layers, 1.6 mm board.** Power nets are pours ≥ 2 mm wide, with ≥ 4 vias per net between layers (IPC-2221: 1.37 mm for 3 A at ΔT 10 °C). 1.6 mm suits the 1.70 mm stake and keeps the screw engagement ≥ 3.24 mm at +10 %.
4. **NVM test pads on a 2.54 mm grid**, Ø1.0, for P75 pogo pins (Robu, Evelta). This replaces charge-path §3's 1.27 mm grid. The five programming pads (`VBUS`, `GND`, `SCL`, `SDA`, `RESET`) stay on the grid; the five probe pads (`VSNK`, `CC1`, `CC2`, `ATTACH`, `POWER_OK2`) may sit anywhere. The jig is a printed base and pogo plate located on the two M2 holes, drawn after layout (CP-OI-05).
5. **Sourcing:**
   - element14 India: USB4140-GF-0170-C, STUSB4500QTR, STL6P3LLH6, ESDA25W.
   - Mouser India: TVS2200DRVR.
   - All but J1 are consigned to the fab; passives come from fab stock.

**Interface fixed for PCB-02** (recorded in the PCB-02 log):

- `J2-8` pin 1 `VSNK`, pin 2 `GND`, as in 05-harness §5. PCB-13's pads are P1 `VSNK`, P2 `GND`.
- `VSNK` is 9 or 15 V, 20 V on a blank NVM, 28.35 V at most in a surge.
- 1.38 A normal, 3 A design.
- PCB-02 carries no parts and no through-hole tails over 1.0 mm on its −X face over PCB-13's area (world Y −14…14, Z 56.5…71.5).

**Datasheets** (CP-OI-03 closed): the ESDA25W (ESDAxxxWx Rev 2) and STL6P3LLH6 (DS9257 Rev 4), read from mirrors of ST's PDFs, confirm charge-path §3; their labels are now `D`. The TVS2200's clamp is 28.35 V at most at 125 °C after a 35 A surge from VRWM, against the 28 V in charge-path §5.3. Only a hot-part surge reaches the STUSB4500's 28 V `VDD` rating, as before.

**CAD changed** (`final/v1/cad/makad-v1.step.py` only; the body source keeps the 9.60 relief and the droid edit supersedes it):

- `PCB13_RELIEF` = X −56.3…−55.0, Y ±5.3, Z 61.2…66.8.
- The `DROID_CUTS` entry on `REAR_SERVICE_PANEL_OCTAGONAL`.

**Checks:**

- New `final/v1/cad/check_pcb13_relief.py` (about 10 s): **13/13 PASS**.
  - The panel stays one solid.
  - Exactly the two 0.5 mm strips are removed (6.720 mm³).
  - The land pattern and 0.3 mm fillets are clear with the SMT pads toward +Z and toward −Z.
  - Relief wall to copper 0.430 mm.
  - The board still seats (0.000 mm) with no overlap.
  - 4.90 mm of print to the screw pilots.
- **Planted:** the same probes against the panel without the cut catch the old relief (0.0104 mm³, both orientations).
- `check_charge_inlet.py` is unaffected: it builds the body source, and the cut only removes print beside the relief.

**BOM changed:** BO-015's supplier and procurement fields name the sources above, with J1 bought and hand-fitted by the builder.

**Open:**

- PCB-13 schematic and layout (CP-OI-01).
- Project footprints for J1 (from GCT's drawing) and Q1 (ST Fig. 16).
- NVM image, jig and read-back (CP-OI-05).
- The BQ25798 and Würth inductor sourcing for PCB-02 (CP-OI-04 stays open for them).
- Full `makad-v1.step` rebuild after the next droid change.

**Amended 2026-10-29 (PCB-13 schematic): R1 is a 1 kΩ 0805 anti-surge resistor (Panasonic ERJ-P06J102V, 0.5 W), not a 0603.** It drops the whole `VBUS_VS_DISCH` discharge: 20 mA at 20 V is 0.4 W, four times a standard 0603's rating. charge-path §3 checked only the pin's 50 mA limit. Schematic: ERC 0/0, and all 18 nets match §3 ([PCB-13 README](04-pcbs/pcb-13-charge-inlet/README.md#schematic)).

**Amended 2026-10-29 (PCB-13 `W16` strain relief, builder: the recommended option).** `W16` is lap-soldered to two SMD pads (J2) and held by a bead of neutral-cure silicone over the joints and 5 mm of insulation. D-040's tie through two slots is dropped: its strap would cross PCB-13's −X face, which sits flat on the printed pad, and the slots would leave thin webs at the board's +Y edge. No CAD change: the bead stays inside the `W16` reserve, 0.4 mm short of PCB-02.

**Amended 2026-10-29 (PCB-13 placement, builder: the recommended options).** U1's 4.75 mm pad span left no room for exit tracks from its corner pins, so:

- **ADDR0, ADDR1 and RESET are tied straight to GND** at the QFN, and R5–R7 are deleted. ST says to ground them with no MCU; the address stays 0x28, and NVM programming over I²C does not need RESET.
- **TP5 (RESET), TP6 (`VSNK`), TP7 and TP8 (CC) are deleted.** `VSNK` is probed on J2's lap pad, and CC on D2's leads or with an inline PD tester. The programming block is TP1–TP4 (`VBUS`, `GND`, SCL, SDA) on the 2.54 mm grid.
- **D2's two identical inputs are swapped** (1 CC2, 2 CC1), and **J2 is turned 180°**. Neither changes the circuit or the `J2-8` pin order.

Layout: DRC 0 errors, 0 unconnected, parity clean ([PCB-13 README](04-pcbs/pcb-13-charge-inlet/README.md#layout)).

## D-070

**2026-10-29 · Chassis / wheels: print fixes (CH-004, CH-005, CH-056, CH-058; J03, J14; final v1 CAD) · ACTIVE; `check_wheel_print.py` 29/29; physical fits open**

**Why.** Walking the wheel's assembly and print steps against the CAD before the chassis STL export ([wheels page](../04-print/01-chassis/wheels/README.md#6-gaps-found-on-2026-10-29-and-their-fixes)) found:

- **The rim's print orientation leaves a fit face on supports.** The wheel README said "outer face down". That way, the ring-seat face, which holds the six insert holes, floats 3 mm above the bed (1,137 mm²), and the lip's tyre face is a bare 2 mm ledge 22 mm up.
- **The hub cap can't print without supports on its visible face.** Face down, its outer ring is 1 mm above the bed (364 mm²). Underside down, the two pegs (1.5 mm) and the screw column (0.4 mm) stand out below it.
- **The tyre fit is only in the README.** The Ø73.6 bore and 19.3 mm width were print notes; the CAD is line-to-line. Applying them in the slicer would change geometry outside the CAD ([04-print rule 2](../04-print/README.md#rules)).
- **The "handed" tyres are one part.** D-009 assumed the right wheel is the left one turned round, so identical tyres would lead backward. But the tyre is symmetric about its mid-plane. The right tyre in the CAD is the left one moved across, unturned (0.000 mm³ difference), and `tyre("R")` is `tyre("L")` turned over. Both lead forward on the robot; the CAD was right, the wording wasn't.
- **Nothing locks the three wheel screws.** The heads clamp on PETG, which creeps, with 2 mm of thread in the stub flange.

**Decision** (builder, 2026-10-29: "make b and c in cad … do the doc changes"):

1. **Hub-cap pegs onto the hub** (`DROID_ADDS`/`DROID_CUTS`, `WHEEL_PEGS`):
   - Each Ø2.1 × 1.8 hub hole is filled and carries a Ø1.8 × 1.5 peg at R12.2, 30° and 210°.
   - The cap gets the Ø2.1 × 1.8 holes. Each sits in a Ø3.7 boss up to the recess roof, because a bare hole broke 0.05 mm into the R11.2 screw-head recess.
   - The cap's centre column is trimmed flush at its underside; it stood 0.4 mm into the hub bore.
   - The fit is unchanged: 0.15 mm radial, 0.3 mm at the tip.
   - The cap prints underside down with no supports. The recess roof bridges 6.7 mm.
2. **Tyre print state** (`WHEEL_TYRE_PRINT`, `wheel_tyre_print()`, `PRINT_STATES`):
   - The tyre is built from the wheel source with a Ø73.6 bore and 19.3 width: a 0.54 % stretch onto the Ø74 seat and a 0.3 mm squeeze by the ring, which stops on the rim.
   - The droid assembly keeps the fitted state. The STL export uses `PRINT_STATES` for the tyre labels.
3. **Rim prints lip side down.** Only the spoke backs (1,188 mm²) and the hub web's underside (766 mm²) need support. The web face carries the stub flange, so it gets a PLA support interface or a flatness check.
4. **One STL per wheel part.** The rim, clamp ring, hub cap and tyre each serve both sides. The tyre's fitting rule is "the chevron V at the top points forward", checked on each wheel. There is no face mark, because the same face goes outboard on one side and inboard on the other. D-009's "one left and one right, not interchangeable" is withdrawn; its CAD stays.
5. **Loctite 222 on the three wheel screws (CH-056)**, re-checked after the first runs.

**CAD:** `makad-v1.step` rebuilt with this change (2026-10-30, 5 min). `makad-v1.step.py` gains `WHEEL_PEGS`, `wheel_peg_edits()` (two rim adds, three cap cuts and two cap adds per side), `WHEEL_TYRE_PRINT`, `wheel_tyre_print()` and `PRINT_STATES`. The wheel source (`01-chassis/v1/cad/wheel/wheel_model.py`) is unchanged, so `check_wheel.py` still describes the subsystem wheel.

**Checks:** [`final/v1/cad/check_wheel_print.py`](final/v1/cad/check_wheel_print.py) passes 29/29 on the chassis tree with the droid edits:

- Cap underside flat at y 12.000. The old pegs and the column stub are gone. The holes are open, roofed and walled 0.80 mm.
- The hub holes are filled and the pegs stand on the face.
- The cap is clear of the rim, the wheel screws, the cap screw and the stub.
- The print-orientation overhangs are only the faces listed above.
- One print serves both sides for all four parts (0.000 mm³).
- Tyre print state: Ø73.60, 19.30 wide, no rib overlap. The assembled tyres are unchanged.
- **Planted:** the unedited subsystem cap fails the flat-underside test (it reaches y 10.5).

**Docs:** the [wheels page](../04-print/01-chassis/wheels/README.md) holds the parts, printing, joints, assembly, service and the gap table. Corrected to match:

- The [wheel README](01-chassis/v1/cad/wheel/README.md) print notes and tyre wording.
- J14 in the [joint register](01-chassis/v1/joint-register.md): 6 inserts per wheel, not 12.
- [axle-stack.md](01-chassis/v1/research/axle-stack.md): Loctite on the wheel screws, and the cap comes off before the wheel.
- The chassis [BOM](01-chassis/v1/BOM.md), `BOM.csv` rows CH-005, CH-056 and CH-058, and the [chassis print parts](../04-print/01-chassis/README.md).

**BOM changed:** CH-005 is one part printed twice (was one left, one right), with the print state. CH-058's pegs are now on the hub (CH-004). CH-056 gets Loctite 222 (CH-057).

**Open:**

- The fitted tyre's OD is about 84.4 (the stretch moves the tread out about 0.2 mm). That's an estimate, folded into the open loaded-radius measurement.
- The CH-049 insert: the ordered OnlyScrews M3 × 4 slant-knurled insert is listed at OD 4.4 (0.2 mm bite in Ø4.0, 0.8 mm left under the seat, under a rib). Measure one on arrival.
- First-print fits: tyre on and clamped, the pegs, the web's flatness and runout.

## D-071

**2026-10-30 · Chassis / axle stack: assembly fixes (CH-001, CH-012, CH-051, CH-089; J01, J02, J03; final v1 CAD) · ACTIVE; `check_axle_stack.py` 21/21; stub drawing and physical proof open**

**Why.** Checking every step of the D-007 assembly against the CAD, with keys modelled across their corners ([axle page](../04-print/01-chassis/axle/README.md#6-gaps-found-on-2026-10-30-and-their-fixes)), found:

- **The housing screws can't be reached with the stub in.** The four M3 × 18 sit at R12. The stub's Ø24 flange (R12) sits 1.6 mm in front of their heads and covers half of each socket: a straight 2 mm key hits it (4.1 mm³), and a ball-end key would need about 30°. The screws clamp the cap, so they can only go in with the stub already in the housing. The documented order (§5 step 4) could not be done.
- **The motor face screws can't be reached once the bearings and stub are in.** At R8.5 the key path is crossed by both 688 ZZ outer rings (R8, 0.65 mm into the key) and by the flange. D-007's "motor floats, face screws tightened last" (§5 step 6, J01) was impossible.
- **The set-screw key rubs the plate hub** by 0.07 mm (0.34 mm³).
- **No print orientation was recorded** for the housing or carrier. The housing printed outboard face down puts the bearing shoulder (75 mm²) on supports.
- **axle-stack.md still planned bore coupons**, which [04-print rule 5](../04-print/README.md#rules) replaces with the real parts as the test.

**Decision** (builder, 2026-10-30: "fix everything and commit properly"; option B1 of the review):

1. **Stub flange Ø24 → Ø21** (`DROID_CUTS` on `WHEEL_[LR]_STUB_SHAFT_8MM`). A straight 2 mm key clears it by 0.345 mm at the housing screws. 1.0 mm of steel stays outside the wheel-screw threads (M3 at R8). The wheel web's clamp face on the flange becomes R5–10.5. The stub has no drawing or quote yet, so this costs nothing.
2. **Motor alignment with a printed plug** (CH-089, `axle_alignment_plug()`, listed in `PRINT_TOOLS`):
   - A Ø15.8 body in the bearing seat and a Ø12.2 nose in the housing's inboard cavity, with a Ø4.05 bore that takes 6.9 mm of the motor shaft.
   - Notches outside R7.2 at the two face-screw key paths.
   - Housing, plug and cap go on, and the face screws are tightened through the cap key holes, housing slots and notches. The housing then comes off for the cartridge.
   - The cap holds the plug in, with 0.2 mm axial play.
   - This keeps D-007's intent: the motor is fixed only once its shaft is on the bearing axis.
3. **Housing screw holes Ø3.4 → Ø3.2** (`DROID_ADDS`), 0.1 mm radial on the M3 shank. The housing refits to within about 0.1 mm of where the motor was aligned to it.
4. **Set-screw key notch** in the carrier hub over the set screw, 3 × 0.5 mm (`DROID_CUTS`).
5. **Print orientations:**
   - Housing: inboard face down, no overhangs.
   - Carrier: outboard plate face down, supports only under the square plate's corners (260 mm², 2.5 mm up).
   - Plug: on its outboard end, no overhangs.
6. **No bore coupons.** The first housing is tried with the real bearings, and the seat is corrected with the slicer's XY hole compensation. This replaces axle-stack §8 item 2 and §9 gate 2's coupon series.

Option B2, locating the motor by a close-fit plate pilot and tightening the face screws first, was not taken. It reintroduces the over-constraint D-007 removed.

**CAD:** `makad-v1.step.py` gains `AXLE_FIX`, `_axle_cyl()`, `axle_edits()` (per side: one stub cut, one carrier cut, four housing adds), `axle_alignment_plug()` and `PRINT_TOOLS`. A new view, [`axle-alignment.step.py`](final/v1/cad/axle-alignment.step.py), shows the left side at the alignment step beside the finished stack. The chassis source is unchanged; its `_check_wheel_interface()` still holds the subsystem flange at R12, and the droid overrides it. `makad-v1.step` was rebuilt with this change.

**Checks:** [`final/v1/cad/check_axle_stack.py`](final/v1/cad/check_axle_stack.py) passes 21/21, both sides:

- Flange Ø21.
- All four housing screws reachable with a straight key with the stub in.
- Ø3.2 holes over the full housing.
- Set-screw key clear.
- The plug clear of every part present when it's used, with its fits.
- Both face-screw keys clear through the plug, and blocked by the bearings and stub without it.
- Housing and plug print with no overhangs.
- **Planted:** the Ø24 flange blocks every housing-screw key (4.126 mm³), and the unedited carrier blocks the set-screw key (0.338 mm³).

**Docs:**

- The [axle page](../04-print/01-chassis/axle/README.md): parts, printing, how it works, the full assembly and service sequence, gaps and order list.
- Corrected: [axle-stack.md](01-chassis/v1/research/axle-stack.md) §3, §5, §6, §8 and §9; J01, J02 and J03 in the [joint register](01-chassis/v1/joint-register.md); the chassis [BOM](01-chassis/v1/BOM.md); `BOM.csv` rows CH-001, CH-012, CH-051 and the new CH-089; and the [chassis print parts](../04-print/01-chassis/README.md).

**BOM changed:**

- CH-012: flange Ø21.
- CH-051: Ø3.2 holes, printed inboard face down, no coupons.
- CH-001: the carriers' set-screw notch and print orientation.
- New **CH-089**: the axle alignment plug, a printed tool.

**Open:**

- **The stub drawing**, then a quote. This is the critical path.
- The DXF for the aluminium caps (CH-052).
- Ordering the bearings and motors.
- The physical gates in axle-stack §9: the 100 N bearing pull test, the J04 carrier fit, the axle rig, and powered acceptance including no-load current after the face screws are tightened.

**Amended 2026-10-30 (builder: "so do the f and g"): fabrication files, and the outward retention closed by calculation.**

- **F, fabrication files:** generated from the final droid geometry into `final/v1/fab/` by [`export_axle_fab.py`](final/v1/cad/export_axle_fab.py) and [`stub_drawing.py`](final/v1/cad/stub_drawing.py).
  - The stub: [`CH-012_stub_drawing.pdf`](final/v1/fab/CH-012_stub_drawing.pdf) (rev A, A3 2:1) and `CH-012_stub.step`.
    - The sheet carries Ø8 k5 (8.001/8.007), Ø10 g6 (9.986/9.995) and the Ø4.05 H8 bore (4.050/4.068), all turned in one setup and concentric within 0.02.
    - The shoulder and flange faces are square to the axis within 0.02, and the shoulder corner is sharp or undercut (≤ R0.15).
    - Threads: the radial M3 through one wall only, 3 × M3 on Ø16 PCD, and the spigot end M3 8 deep.
    - Material EN8 or C45, quantity 3, ISO 2768-m.
  - The cap: `CH-052_cap.dxf` (eight circles, mm) and `CH-052_cap.step`, in 1.2 mm 5052-H32 or 6061-T6.
  - Placing orders and getting quotes is the builder's ([axle page §7](../04-print/01-chassis/axle/README.md#7-to-order-or-make)).
- **G, outward retention:** the [Loctite 641 TDS](https://datasheets.tdx.henkel.com/LOCTITE-641-en_GL.pdf) gives ≥ 6.5 N/mm² on steel (ISO 10123, 24 h at 22 °C).
  - Two inner rings (251 mm²) hold ≥ 1,630 N. One ring at half strength holds about 410 N, about 4× the 100 N design load, without counting the k5 friction.
  - The cap: about 35 MPa bending at 100 N, against ≥ 160 MPa yield (about 4.5×), a rough screen.
  - No load for 24 h at about 22 °C after pressing.
  - G is closed by calculation. The bench pull test (10.2 kg hung from the spigot, < 0.10 mm movement; [axle page §9](../04-print/01-chassis/axle/README.md#9-outward-retention-of-the-bearings-gap-g)) checks workmanship when the parts arrive. The DIN 6799 clip stays the fallback.

## D-072

**2026-10-30 · Chassis / axle stack: motor-to-axle follow-up (CH-053, CH-089; J01, J02; final v1 CAD) · ACTIVE; `check_axle_stack.py` 27/27**

**Why.** A second pass over the motor assembly after D-071, checked against the source, the docs and a clearance probe on the chassis tree, found gaps D-071 left open. The builder (2026-10-30): "fix all the gaps, so do it properly, and commit step by step". Each gap is fixed in its own commit and recorded here as it lands.

**1. Housing screws M3 × 18 → M3 × 16 (CH-053).**

- The M3 × 18 tip sat at |Y| 69.71. The plate's blind tip hole ends at 69.51, leaving 0.51 mm of plastic over the gearbox face (69.0); the screws sit at R12, over the R12.5 gearbox face.
- ISO 7380's length tolerance on 18 mm is ±0.35 (js15), the 1.2 mm cap can be 0.08 thin, and plastic pushed down when the insert is melted in collects below it. A long screw could bottom out before its head clamped the cap, so it would feel tight with the bearings unclamped, and could push the skin onto the gearbox.
- M3 × 16 puts the tip at 71.71: 2.20 mm above the hole bottom against a 0.93 mm stack, and 2.29 mm in the 4 mm insert (1.94 mm with the screw at its short limit, against 1.5 mm minimum). The load is about 21 N per screw (axle-stack.md §4).
- Source: the [OnlyScrews M3 × 16 SS304 button head](https://onlyscrews.in/products/hex-allen-button-head-m3-x-16-screw-pack-of-20), the same shop and family as the M3 × 6 (CH-030, CH-056). The listing was live on 2026-10-30; ISO 7380 head dimensions are checked on the sample. This drops the UAVstore M3 × 18 lead.
- CAD: `makad-v1.step.py` gains `AXLE_FIX["cap_screw"]` and `axle_cap_screws()`: `DROID_REMOVES` drops `AXLE_CAP_SCREW_M3X18_[LR]_[1-4]`, and `DROID_INSERTS` puts `AXLE_CAP_SCREW_M3X16_[LR]_[1-4]` into `AXLE_HOUSING_HARDWARE_[LR]`. The chassis source is unchanged. The blind tip hole stays as it is, 2.2 mm below the new tip. Mass: −0.9 g for the eight screws, not re-totalled in the hand-kept mass rows.
- Check: `check_axle_stack.py` §8, both sides, with the M3 × 18 planted (0.20 mm above the hole bottom, inside the 0.93 mm stack).

**BOM changed:** CH-053 is ISO 7380 M3 × 16 (8), OnlyScrews.

**2. The motor alignment gets an error budget (CH-089; J01).**

- D-071 aligned the motor with the plug, then refitted the housing. Neither error was budgeted: the plug body (Ø15.8) sat 0.10 mm radial in the Ø16 seat plus 0.025 on the shaft, and the Ø3.2 holes let the housing refit within about 0.1 mm. The stub bore has only 0.025–0.034 mm radial play on the shaft (Ø4.05 H8 on Ø4), so up to about 0.2 mm would have gone into the gearbox shaft or its bushing, which D-007 set out to avoid.
- **Budget: 0.05 mm radial**, the stub bore's own play, which the set screw already pushes the shaft across when it is tightened.
- **The plug body goes Ø15.8 → Ø15.96**, a close sliding fit. It is printed after the housing seat has been tuned to the real bearings, with the same settings, and must slide in with no rock you can feel; the bore is drilled Ø4.0 by hand. Its error is then 0.020 + 0.025 = 0.045 mm.
- **The housing takes up its own refit error.** At the refit its screws stay finger-tight while the set screw is tightened and the stub is turned (or the motor run briefly at about 3 V); then they are tightened diagonally in two passes, checking that the stub turns as freely as before. The housing's 0.11 mm hole float covers its refit error; in the worst case (the housing sat at the edge of its float at the alignment step) the plug's own error is what remains, hence the budget on it.
- CAD: `AXLE_FIX["plug_body"]` R7.9 → R7.98 and a new `ALIGN_BUDGET` in `makad-v1.step.py`. Check: `check_axle_stack.py` §9, with the D-071 plug planted (0.125 mm).
- The axle rig (axle-stack.md §6 hold 8: drag, current and runout before and after tightening) remains the physical proof.

**BOM changed:** CH-089 body Ø15.96, printed after the seat is tuned.
