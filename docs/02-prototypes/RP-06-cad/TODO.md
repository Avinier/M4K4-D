# RP-06 TODO

| Field | Value |
|---|---|
| Status | **Open.** Working CAD is head Layout 04 + body/chassis Layout 02. Physical validation 0% |
| Home | [`README.md`](README.md) |
| Detail | [`checklist.md`](checklist.md) |

Checking a box here does not freeze a SKU, promote `E` to `W`, or register a gate.

## CAD progress and largest remaining gaps (audit 2026-09-27)

Layout 02 is an integrated packaging model, not a fabrication release. The rear module now contains only the skid/TCRT keel. The full `check_layout.py` suite on the current source passes **115/115**; the keel guard seats along its length and the former PCB-03/motor connector-reserve overlaps are absent. The 2,551.9 g / X +19.46 / Z 107.27 mm mass and CoM figures come from a hand-kept register, not measured hardware.

Completed at the CAD packaging level:

- [x] Compose the active Layout 04 head with the body, chassis, wheels, motors, fixed ball nose, rear keel, shell, service panels, electronics, yaw stage, and inspection layers in one buildable STEP; regenerate the visual snapshot packet.
- [x] Establish the nominal 170 mm track, 84 mm wheels, 16 mm forward body shift, four-M4/two-pin body interface, service-panel outlines, and 293.5 mm neutral height. These are modeled dimensions, not as-built measurements.
- [x] Model the Pololu #4804-based motor face, flange, 608 bearing pair, stub shaft, dished-wheel clearance, battery tub, ball caster, front range sensor, speaker cavity, E-stop well, charge cut-out, and pack-disconnect service window.
- [x] Allocate working CAD positions and connector exits for the Pi 5/cooler, power boards, C3 carrier, audio boards, IMU, yaw junction, and head trunk. The custom boards and cables are still estimated envelopes or route volumes.
- [x] Clear the two previously reported PCB-03/motor connector-reserve overlaps and complete the full current-source geometry suite (115/115 on 2026-09-27).
- [x] Recheck the proposed +6.5 mm height addition against the current model (2026-09-27). The seated Pi 5 cooler STEP spans Z 94.35–108.57; `PI_COOLER_TOP_Z = 123` is a conservative clearance datum, 14.43 mm above its actual top. The neutral stack is already 293.5 mm against the rounded 300 mm target, so no height was added. The Pi reaches Z 111.9; PCB-05 spans Z 114–123 (2.1 mm above that top), its connector bodies reach Z 125.6, and the front upper cross begins at Z 126. Moving the tray and Pi up 6.5 mm would require redesign of those interfaces, plus a new dimensional-baseline decision. The cooler is still unretained and must be fitted on hardware.

Largest gaps, in order of impact on CAD closure:

1. [ ] **Prove the latest assembled geometry.** The full Layout 02 suite passes 115/115. Complete an all-group clash sweep, including the composed head, signal/sensor harness, yaw plate/upper rails, microphone boots, and wheel arches, then resolve unintended overlaps. The inherited Pi 5 vendor STEP also has five self-intersecting occurrences, so distinguish vendor topology defects from authored geometry. See the detailed check item and `openitems.md`.
2. [ ] **Reconcile the safety geometry with RP-03.** The current rear-only TCRT leaves no dedicated forward/lateral cliff channel, and objects below the GP2Y beam can reach the ball housing without a touch signal. Decide the sensing/contact coverage and operating limits, then propagate `RP03-CAD-01…08` into the permanent locomotion baseline before physical layout closure.
3. [ ] **Engineer the load-bearing and service joints.** Close the wheel-to-stub fixing and axial retention, motor-face diaphragm and chassis stiffness, bearing preload, yaw bearing/gear load path, Pi/cooler retention, wheel-arch attachment, battery hatch/retention, and fastener/insert stacks. Add material, tolerances, tool access, and joint checks; details are in “CAD gaps and inefficiencies” below.
4. [ ] **Replace envelopes with buildable boards and sourced parts.** Complete PCB-01…10 schematics/layouts where applicable, fit the real pack/BMS, power components, connector bodies, sensor breakout, audio hardware, and purchased yaw bearing. PCB-03/04 consume the available bay, and the working `PCB-03` connector-edge margin is only 0.4 mm; rerun fit checks against laid-out boards and measured articles.
5. [ ] **Complete and qualify the installed harness.** Convert route reserves to a wire/connector build with lengths, bend radii, strain relief, demate paths, pinouts, and the moving yaw/CSI clock-spring construction. Check cooler airflow and service access with the harness installed.
6. [ ] **Replace paper mass and fit with physical evidence.** Weigh the robot and head, recompute the neutral and head-pose CoM/lift margins, fit sourced parts, then register and execute RP06-G01…G06. The project currently records **0% physical validation**.

---

- [x] Neutral stack: **closed 2026-09-26.** Head Layout 04 cut the neck from 60 to 49.5 mm (turntable in place of the spindle), so the stack is 140 + 49.5 + 104 = **293.5 mm**, under the 300 mm target (`neutral_stack_is_documented_293p5_mm`, `neck_allocation_is_49p5_mm`). Registered in `dimensional-baseline.md` v1.13; physical height remains a G01 measurement.

- [x] (superseded by the item above; the target is met without it) Use the real Pi 5 cooler height: with the cooler seated on the SoC (top Z 107.5, not 123) the body's 10.5 mm cooler headroom has ~15 mm of slack. Re-derive the yaw stage / neck stack from `PI_SOC_TOP_Z` and see whether the 4 mm needed for the 300 mm target can be recovered (changes the head neck, the body-top datum and the CoM gap below).

- [x] Close the CoM gap (baseline revised, see below): Layout 02 is at x +20.6 / h 105.8 mm (a_tip 1.91 m/s²) with the 81.6 g ballast bar (`RP03-CAD-08`) that offsets the lighter 110 g battery (`RP03-CAD-07`); the target is +25 / 124. The +20 mm `physics.md` §2.5 line clears by only 0.62 mm. Recover the rest by geometry or revise the baseline; the ballast screws' thread engagement in the deck and the bar's mass are unverified.
  - **Resolved 2026-09-25 (`RP03-CAD-09`, `BA-06`):** the builder accepted the then-current layout-02 register with the power boards, x +18.77 / h 105.05 mm (a_tip 1.75 m/s²), instead of +25 / 124. The 81.6 g `RP03-CAD-08` bar stays; no additional ballast was added. The `physics.md` §2.5 check is re-based from x ≥ +20 mm to the a_tip 1.582 m/s² that line encodes at h = 124 mm. The latest generated mass register is 2,551.9 g, x +19.46 / h 107.27 mm, a_tip 1.78 m/s²; the 2026-09-27 current-source suite passes 115/115. The earlier worst-head-pose figure of about 1.44 m/s² still needs recalculation against this register. Still open: a weighed robot (`W`) to replace the hand-kept register and head lumps

- [ ] Close the new axle stack (`RP03-CAD-05`) on real parts: ~~gearmotor face-screw pattern and shaft length~~ (in CAD from Pololu's drawing and STEP, `RP03-CAD-10`, 2026-09-26; confirm tapped length 2.85 mm, bushing boss and shaft on received #4804 samples), stub-to-web fixing and axial retention, bearing preload, deck/cheek stiffness, and the 2 mm printed diaphragm that now carries the motor face screws (stiffness and PETG creep under preload).

- [ ] Resolve the older body-side clashes the 2026-09-24 sweep found (harness power volumes against electronics: re-routed clear 2026-09-26; rear frame against power/safety envelopes, yaw plate and upper rails against the shell); see `openitems.md`.

- [ ] Resolve inherited RP-01 blockers:
  - [x] two screw collisions (closed 2026-09-25 in head Layout 04: 0.51 mm clearance, 30 fasteners in the 56-pose grid, 0 hits)
  - [ ] pitch-frame stiffness (redesigned 2026-09-25, FEA about 41 Hz; loaded tap/ring-down B6 open)
  - [ ] roll-saddle stiffness (redesigned 2026-09-25, FEA about 84 Hz; B6 open)
  - [ ] hard-stop margin (stops 3 deg past usable travel, Ø2 steel dowels; stop impact at speed is a bench item)
  - [x] bearing SKU (696-2Z selected 2026-09-25; trial fit and preload on printed seats open)
  - [ ] balance trim (trim path modelled 2026-09-25; weigh and trim on the built head)
  - [x] CAD/firmware sign mapping (closed 2026-09-25: `head/layout-04/motion-signs.json`, pitch +1, yaw -1, roll -1)
  - [x] actuator family: working choice `ACT-01` (2026-09-25), XC330-M181-T yaw, XC330-M288-T pitch/roll at 5 V (RP-01 `decision.md`). Not frozen: bench tests B1-B6 and dated builder approval remain
  - [ ] production camera interconnect

- [ ] Replace remaining CAD envelopes with exact vendor or measured geometry:
  - [ ] motors and gearboxes (vendor STEP for Pololu #4804 in since `RP03-CAD-10`; measured article pending the SKU lock)
  - [ ] wheels and hubs
  - [ ] ball-transfer article
  - [ ] battery: 2S1P Samsung 25R + BMS is modeled as datasheet envelopes (`RP03-CAD-07`); replace with the measured pack and the real BMS board
  - [ ] power modules
  - [ ] motor drivers
  - [ ] sensors (IMU now `PCB-07` from its datasheet, 2026-09-26; TCRT breakout and comparator still an envelope)
  - [ ] audio hardware (parts selected 2026-09-26 and modelled from datasheet outlines; measured articles pending)
  - [ ] connectors and cable exits: schedule and layout rule set 2026-09-26 in [`connector-schedule.md`](connector-schedule.md) (JST GH signals, Micro-Fit power on free board edges, re-crimped #4804 leads, USB-C Pi pigtail, rear charge-inlet cut-out, head trunk re-routed via a -Y yaw junction, Micro-Fit+ pack disconnect `CN-05`, C3 carrier `PCB-10` on the -Y wall `CN-06`). Open: Micro-Fit+ drawings, pin-outs, vertical USB-C inlet part, bench fit of the 0.1 mm Pi-header adapter strip

- [ ] Replace remaining boxed body-chassis Layout 02 parts with exact STEP or measured geometry (several vendor STEPs have been integrated since the 2026-09-24 audit; the detailed entries below distinguish imported parts from estimates):
  - [x] Wired into `body_chassis_model.py` from `layout-01/references/purchased/` (2026-09-24; 95/95 checks pass; STEP rebuilt, snapshots refreshed):
    - [x] `pololu_drv8874_carrier.step` (Pololu 4035; bare board 15.2 x 17.8 x 2.8 mm, no headers) replaces the 20 x 20 x 12 DRV8874 boxes; sits flat with its bottom on the old envelope floor (Z 66), mounting unspecified
    - [x] `vishay_tcrt5000.step` (10.2 x 7.1 x 10.5 mm incl. leads) replaces the 10.2 x 5.8 x 7.0 package box; keel sensor pocket and `TCRT_PACKAGE_SIZE` Y widened to fit (7.1 wide, 10.5 tall)
    - [x] `sharp_gp2y0a41sk0f.step` wired in (2026-09-24 prow rework): the 29.6 mm body and 44.4 mm belt now sit in side slots of a swelled pod; sensor bottom Z 35, lens tip X 128; cap window is a 27 x 10.5 visor slit
    - [x] `robotis_xc330_dummy_assy.step` (20 x 34 x 29 mm, 15 solids) replaces the yaw servo box; it is a third-party mirror (xiaoyatec.com) of ROBOTIS's XL/XC-330 file, so verify against the official ROBOTIS download once signed in. Oriented -90 deg about Z so the body runs along X (the +Y orientation hit the left upper rail); output axis on the pinion centre. Envelope Z height was 34, real stack is 29
  - [x] Login-gated STEPs, added by hand from GrabCAD and Digi-Key and now wired in:
    - [x] Raspberry Pi 5 active cooler: GrabCAD `raspberry-pi-5-active-cooler-1` / `raspberry-pi-5-stock-active-cooler-1`; official mechanical drawing PDF on Olimex RPi5-ACOOL resources. File `Heatsink+fan RPi-5.STEP` (64.8 x 14.2 x 43.5 mm). Seated 2026-09-24: spring posts in the Pi's two cooler holes (58 x 37 mm apart; the first -90 deg turn mirrored them), plate on the tallest package under it (Z 97.7), top at Z 107.5. The old envelope floated the cooler 11 mm too high, so the 10.5 mm yaw headroom datum (`PI_COOLER_TOP_Z` 123) is now ~15 mm conservative
    - [x] ESP32-S3-DevKitC-1-N8: Digi-Key model page 15295894 (the listing is N8R8; the model uses N8, confirm the board outline matches). File `ESP32-S3-WROOM-1_devkit_2xUSBC_c.step` is 28.3 x 64.1 x 5.5 mm (no headers), wider than the old 25.4 mm envelope; USB end rearward; confirm it is the N8 board
  - [ ] CAD not found, use a vendor drawing or measure:
    - [x] Pololu ball caster 1" with plastic rollers (item 2691): no vendor STEP; authored from the dimension drawing with Ø14.1 mm bolt circle after correcting the 12.2 mm hole-spacing misread. Measured fit, screws and ABS thread engagement remain open below.
    - [x] Gearmotor: switched to the preferred Pololu #4804 and wired in its official STEP (`pololu_25d_34-47_encoder.step`, 2026-09-26, `RP03-CAD-10`); axle stack rebuilt round its face, leads clocked rearward. The 110/110 pass was a historical run, before later connector changes; rerun the current model. The JGA25-370 community STEP is no longer needed
  - [x] Head STEPs wired into head Layout 04 (2026-09-24); files in `head/layout-01/parts/`; head checks pass, dimensions and assembly reports regenerated:
    - [x] `waveshare_esp32_s3_touch_lcd_4_3.stp` for the display. SKU 30493 is the non-touch board (105.4 x 67.1 mm); the Touch STEP (106.1 x 68.3 x 16.9 mm) is used as the conservative outline, glass front on X -3.8. Fit checks use a slab plus connector-strip proxy (12.5 mm deep, 16.9 mm over one 5 mm strip on the -Y edge). Still open: replace with the non-touch model if Waveshare publishes one
    - [x] `waveshare_esp32_s3_zero_v2.step` for C2 (18.0 x 23.5 x 1.9 mm, bare PCB: the STEP has no USB-C shell or headers, so the authored USB reserves stay). Components face -X
  - [x] Ball caster: Pololu 1" caster 2691 (rollers; 2692 is the bearing variant, same envelope). India: Fab.to.Lab (bearings +₹337), MG Super Labs (₹399 incl. GST). Indian industrial ball-transfer units (25.4 mm, ₹105-125) are 130-220 g steel with 14-21 mm working height, so they do not match. The hole pattern was misread: Pololu's 12.2 mm is the spacing between holes, so the bolt circle is O14.1 (radius 7.04, model had 12.2), base O34 x 8.8 (model had O36 x 4). STEP authored by `build_ball_caster_step.py` into `purchased/pololu_ball_caster_1in_2691.step`; the supplied `Pololu Ball Caster.STEP` is the 3/8" caster (9.5 mm ball) so it was used as a structural template only. Still open: verify screw length and thread engagement on a real unit, and ABS thread-forming vs. inserts in the base
  - [ ] Fasteners are authored cylinders; real STEPs exist on step.parts (ISO 4762 M3/M4/M2, ISO 7380, M3 heat-set insert bosses, M3 nuts). Only worth swapping once head/body fastener SKUs are chosen (P-07)
  - [ ] Ball caster form check: the CAD is a form match to the Pololu photo (dome shoulder, roller windows, rim notch, snap slits), built from the vendor drawing, not a scan. When a sample 2691/2692 arrives, caliper the base O.D., roller-window positions, notch width, slit positions and the real bolt circle, then update `build_ball_caster_step.py`. Note the photo shows the 2692 bearing version; the model uses plain rollers.
  - [ ] SKU not chosen, so nothing to download yet:
    - [x] ICM-42688-P IMU: own `PCB-07` board screwed to the chassis deck crossbar, modelled (`RP03-CAD-11`); bench article any SPI+INT1 breakout, MIKROE-4237 where stocked ([`peripheral-selection.md`](peripheral-selection.md) §4)
    - [ ] yaw thin-section bearing (50 g placeholder in `MASS_ROWS`)
    - [x] speaker, amplifier and four PDM microphones: selected and modelled from vendor outlines (2026-09-26); no vendor STEP read, the speaker's internal profile is estimated
    - [ ] power-distribution and safety/watchdog boards (RP-02); the battery is working-selected (2 × Samsung INR18650-25R + 2S 20 A balanced BMS), with no STEP for the BMS board
    - [ ] harness: modeled as volumes, not parts. Head trunk re-routed 2026-09-26 (plate bore, -Y junction `PCB-08`, -Y riser; CSI FFC beside the cooler); [`connector-schedule.md`](connector-schedule.md) now lists wire IDs, functions, conductors and tentative lengths, but final lengths, pinouts, bend/strain relief and moving-cable construction remain open.

- [ ] Resolve the RP-03 CAD-versus-safety issue:
  - the controller/safety design expects multiple direct stop-path sensors
  - current Layout 02 only packages one guarded rear TCRT channel and explicitly makes no full forward/lateral cliff-protection claim
  - since the touch-cap skirt cut (`RP03-CAD-04`, 2026-09-24), floor objects below the GP2Y beam (Z 41), including `C12`, meet the ball's retaining lip with no contact signal; forward edges and low obstacles now rely on the camera, which is not a low-level stop channel
  - this must be reconciled before physical layout closure

- [ ] Complete an all-group sweep of the composed head and body-side groups. The current full Layout 02 geometry suite passes **115/115**. The rear keel guard was shortened 2 mm at its forward end and now seats along its length, ending 0.1 mm behind the TCRT package front; the former PCB-03/motor Micro-Fit reserve overlaps are clear in the current report.

- [x] Replace the six misplaced `_vertical_bore` calls with bottom-aligned `_z_cylinder` (2026-09-26). Targeted cylinder extent checks pass; the STEP was rebuilt and the visual snapshot packet refreshed. Full-assembly check completion remains tracked above.

- [ ] Close the ball-nose touch cap on real parts: flexure stiffness, tact-switch force and over-travel stop, debounce, and the 3 mm travel.

- [ ] Confirm the GP2Y 0.70 m/s look-ahead on real floors: charged to the nose front it needs 294.5 mm against the 300 mm rating.

- [ ] Propagate `RP03-CAD-01`…`08` to the permanent RP-03 documents as one reviewed change set (sensor count, bump coverage, the fixed ball-only mount versus the required `D20` swap, CoM and motion restrictions).

- [x] Select the status LED and diffuser/optic. **Working selection 2026-09-26** ([`peripheral-selection.md`](peripheral-selection.md) §3, `HEAD-CAD-12`): Worldsemi WS2812B-2020-V6 on a 5 × 5 mm carrier (`PCB-08`) behind the unchanged Ø3.4 × 2.9 light pipe (clear resin or PMMA, frosted face), D1 GPIO6 at 3.3 V. Still open: route the three leads from the crown to D1, bench brightness at 3.3 V and camera stray light (G03).

- [x] Select microphone front end, microphone boards, speaker, and amplifier. **Working selection 2026-09-26** ([`peripheral-selection.md`](peripheral-selection.md) §2, RP-05 `BD-A04`…`A06`, `RP03-CAD-11`): `AP-TDM` as two I²S lanes on the Pi 5 (RP1 has no true TDM), 2 × ADAU7002 and a MAX98357A on `PCB-05`, four Infineon IM73D122V01 on `PCB-06` boards at the unchanged ports, Visaton K 50 WP 8 Ω. Modelling them showed the old amplifier box sat inside the Pi 5 and the 34 mm cavity ran through the compute tray, so `PCB-05` moved above the Pi's front end and the cavity is now 20 mm (X 77–97). Still open: `CA-06` CR-01 (GPIO22 SDI1, GPIO23 `AMP_SD`), the Pi 5 overlay and duplex bench proof, mic-board fixing to the body frame, speaker flange bond and grille, acoustic tests.

- [ ] Finish the battery and power-hardware selection against real parts. The 2S1P Samsung 25R pack, Micro-Fit+ 1×2 disconnect, fuse tile and estimated board envelopes are working CAD choices. Open: exact connector/terminal drawings and ratings, pack retention and hatch fastening, board layouts, and who builds the pack (workbench battery gate). The power-board spec is v0.17; estimated CAD envelopes cannot prove the laid-out boards fit.

- [ ] Design the small boards the 2026-09-26 selections created ([`peripheral-selection.md`](peripheral-selection.md)); none has a schematic:
  - [ ] `PCB-05` audio front end (2 × ADAU7002 WLCSP, MAX98357A TQFN, 100 Ω series on the amp inputs, JST GH mic inputs (`CN-01`)); JLCPCB assembly because of the WLCSP
  - [ ] `PCB-06` mic board ×4 (IM73D122V01, Ø0.8 port hole, LR strap per position, JST GH 4-pin, board 12 x 9.5 mm; `CN-01`) and its fixing to the body frame
  - [ ] `PCB-07` IMU board (ICM-42688-P, JST GH 8-pin (`CN-01`), two M2 holes 15 mm apart)
  - [ ] `PCB-08` LED carrier (WS2812B-2020, three pads)
  - [ ] Raise `CA-06` CR-01 in RP-02 (GPIO22 `i2s0` SDI1, GPIO23 `AMP_SD`) and prove the custom `simple-audio-card` overlay: 4-channel capture on SDI0+SDI1 with 2-channel playback on SDO0 at 48 kHz, lane order, and whether RP1 forces symmetric channel counts

- [ ] Obtain or fabricate representative articles and measure:
  - [ ] every relevant mass
  - [ ] complete robot CoM
  - [ ] head installed mass/CoM
  - [ ] service clearances
  - [ ] cable bend and demate volumes
  - [ ] airflow and temperatures

- [ ] Perform the physical display tests:
  - [ ] smoked window
  - [ ] viewing angle
  - [ ] distance
  - [ ] lighting
  - [ ] frame rate and tearing

- [ ] Perform camera tests:
  - [ ] FOV and occlusion
  - [ ] calibration
  - [ ] focus lock
  - [ ] motion smear
  - [ ] LED/display contamination
  - [ ] live CSI endurance

- [ ] Perform audio tests:
  - [ ] speaker level and vibration
  - [ ] microphone contamination
  - [ ] cooler and mechanism noise
  - [ ] playback-while-listening behaviour

- [ ] Demonstrate replacement of a named high-risk module and record time/tools.

- [ ] Verify current suppliers, landed costs, and substitutes.

- [ ] Register and execute RP06-G01…G06.

## CAD gaps and inefficiencies

Running list of ways the current CAD falls short of a production design. Add to it as they turn up.

- [ ] Layout 02 is a packaging and fit-check model, not a production design (noted 2026-09-24). Passing checks means no clashes and the clearances hold, not that the design is complete. Open causes:
  - [ ] Pi 5 and active cooler have no retention: no standoffs, cooler push-pins or fasteners, and the compute tray is a plain 3 mm box. The cooler is only positioned (`PI_COOLER_TOP_Z`), and nothing ties it to the Pi
  - [ ] Check underside clearance for the cooler push-pin tips and the Pi-to-tray standoff gap (currently an assumed ~16 mm)
  - [ ] Check fan intake and airflow: only 10.5 mm of headroom over the cooler under the yaw stage
  - [ ] Yaw-stage parts are packaging envelopes, not selected or load-rated parts
  - [ ] Head-harness route: no longer through the compute tray and cooler (2026-09-26, check `head_trunk_and_csi_avoid_tray_pi_cooler_and_yaw_stage`); the clock-spring, `PCB-08` junction and cable qualification remain open

- [ ] Wheel arches and trim have no attachment (noted 2026-09-24). `WHEEL_ARCH_POD_L/R` and the amber `WHEEL_ARCH_UPPER_TRIM_L/R` are separate solids under `BODY_PANELS`, not part of `BODY_SHELL`, and nothing fixes them in place: no screws, tabs, bosses or adhesive land, and no snap or bond for the trim on the arch.
  - [ ] Decide the concept: integral flanges in the printed shell, or bolt-on fenders fixed to the chassis cheeks. The shell floor is open across the axle so the body lowers on from above, which rules out a simple bond
  - [ ] The arches are X-centred on the axle (0.0), not on the body, so they don't follow `BODY_SHIFT_X` (16 mm). Confirm that's intended
  - [ ] Measure the arch-to-shell overlap or gap, and whether the arch sits inside or outside the shell wall; it is part of the open panel-versus-shell clash sweep
  - [ ] Add the fixing and its clearances to the checks

- [ ] Fasteners are positions and bores, not engineered joints (noted 2026-09-24). `CON-P01` (`00-foundation/constraints.md`) makes screw-together construction a requirement for serviceability, and `brief.md` leaves "thread engagement, inserts, sealing/gasket detail, tolerances, material/process selection and structural proof" unresolved. The checks cover screw count, edge inset and ball-flange thread engagement (>= 2.5 mm), not load or stiffness. To do:
  - [ ] List every joint (M4 body/chassis through-bolts and locating pins, M3 service panels, ball flange and pod, keel, axle flange, yaw stage, arches) with its screw, insert or nut, clamp stack, and load path
  - [ ] Set thread engagement and boss geometry per joint: heat-set insert depth, boss wall, edge distance, pull-out margin
  - [ ] Add clearance holes, counterbores, captive nuts or inserts, and washers where the joint needs them, so the CAD carries what would be bought and machined
  - [ ] Size for preload, shear and stiffness on the load-bearing joints first: axle flange, body/chassis bolts, yaw plate and bearing
  - [ ] Choose the material and process (printed, machined or moulded), then the tolerances and any gasket or seal
  - [ ] Add per-joint checks: engagement, edge distance, tool access and service removal path
  - [ ] Add a fastener schedule (BOM) to the generated outputs

## Custom power and safety boards

Spec: [`../RP-02-electrical/board-specs.md`](../RP-02-electrical/board-specs.md) v0.17, 2026-09-25 (working direction, **not registered**; decisions `BD-01…14`). Four custom PCBs plus a watchdog block: `PCB-01` pack protection, `PCB-02` charge and system power, `PCB-03` motor gate and head/drive distribution, `PCB-04` branch converters. Part choices, values and estimated packaging envelopes are in CAD; schematics, layouts, selected connector parts and bench proof are open. Nothing here selects a SKU for purchase.

- [x] Part choices on paper (working choices, 2026-09-25; each is a datasheet-derived proposal, none bench-proved):
  - [x] `PCB-01`: `S-8252AAC` + `bq29200`, two `PSMN1R5-30YLC`, 5 mOhm Vishay `WSK2512` shunt, Bourns `AC72ABD` thermal cutoff
  - [x] `PCB-02`: `BQ25798` in default mode (no host), `STUSB4500` (5/9/15 V at 1.5 A), `LTC2954-2` latch, `SYS` gate `TPS22810`
  - [x] `PCB-03`: `LTC4368-1` + 3 mOhm shunt + two `PSMN1R0-30YLE`, `SMBJ10A` TVS; head rail `LTC3119` behind a latching `TPS259824`
  - [x] `PCB-04`: `TPS630701` + `TPS259474L` per branch; Pi rail `LTC3119`
  - [x] Watchdog: `TPS3436CFDBEDDFRQ1` per C2/C3 carrier
- [x] Place C3 carrier `PCB-10` in CAD (`CN-06`, 2026-09-26): 70 × 43.5 mm, vertical on the -Y side wall, DevKitC soldered on, ten installed GH headers plus one Micro-Fit 3.0, and four M2.5 screws into printed uprights on the -Y rails. `J10-9` was dropped when the touch switch joined `J10-8`.
- [ ] Finish `PCB-10` for fabrication: schematic after the RP-03 pin map freeze, real board layout, upright/insert strength, exact connector fit, and harness lengths.
- [ ] Decisions waiting on the builder (details in `board-specs.md` section 10): Pi setpoint 5.10 V vs 5.15 V; `PA-14` wording for the 43-100 uA `OFF` draw; ~~servo family~~ (settled 2026-09-25: XC330 at 5 V, RP-01 `ACT-01`); brownout threshold registration; purchase.

- [ ] Draw the schematics (start with `PCB-01`), then layouts:
  - [ ] Heavy copper and a short loop for the gate, shunt and drive feed on `PCB-03`; motor return straight to the star point
  - [ ] Keep the charge-logic net away from `PCB-03`; keep noisy converters away from C2/base converters and sense lines
  - [ ] Test points on every rail, branch current, gate state and each `MOTOR_PERMIT` term
  - [ ] `PCB-01` FET land pattern and an assembly route if the chip-scale alternate is used (the selected LFPAK56 parts are hand-solderable)

- [x] Give the boards estimated CAD volumes from the unlaid-out part inventory (`board-specs.md` section 2): `PCB-01` on the pack, `PCB-02` on the rear-panel frame, `PCB-03` above the battery tub, `PCB-04` under the compute tray. The connector and harness revisions moved the original clashes. Replace these envelopes with actual laid-out boards and rerun the fit sweep before release.
  - [ ] Check the `PCB-04` hold-up capacitors and connector exits in a real layout; the bay has little slack.
  - [x] Pack interface placed 2026-09-26 (`CN-05`, [`connector-schedule.md`](connector-schedule.md)): Micro-Fit+ 1×2 wire-to-wire pair beside the tub (X 27–49), ATOF holder moved next after it (X 51–75), service window in the +Y tub wall. Open: Molex outline and terminal rating, the bench service move, the pack NTC break
  - [x] The rear-panel E-stop is modelled: IDEC XA1E-BV3U02KT-R (Ø29 mushroom, 23.9 mm deep) in an 8 mm octagonal well with an amber bezel, replacing the Ø40 XW1E (2026-09-25)
  - [x] Rear-panel USB-C charge-inlet window is cut as a 13.2 × 7.2 mm envelope; select the actual receptacle and check tool/plug access.
  - [x] `CONTROL_POWER_SENSORS` was split into per-board mass rows, the E-stop changed to the 14 g XA1E, and the battery row was revised for the pack-side Micro-Fit+ half. The current hand-kept total is 2,551.9 g; verify on weighed hardware.
  - [x] The accepted CoM screen is a_tip ≥ 1.582 m/s², with the RP03-CAD-08 bar retained. Current estimate is x +19.46 / h 107.27 mm, a_tip 1.78 m/s². Recheck the pose corners and weigh the robot.

- [ ] Replace estimated power-hardware geometry with selected part drawings, vendor STEP and laid-out PCB geometry: `LTC3119`, `PSMN1R5-30YLC`/`PSMN1R0-30YLE`, `TPS630701RNMR`, `TPS259474L`/`TPS259824`, `BQ25798RQMR`, vertical USB-C receptacle, Micro-Fit+ pack disconnect and board connectors, ATO FLR fuse holder `178.6165.0001`, IDEC `XA1E-BV3U02KT-R`, `AC72ABD`, `WSK2512`/`CSS2H-2512`, and `XAL5030-332ME`. The DRV8874 carrier STEP is already imported.

- [x] Resolve the head-servo dependency. **Resolved 2026-09-25 as working choice `ACT-01`** (RP-01 `decision.md`): XC330-M181-T yaw, XC330-M288-T pitch/roll on the 5 V `PB-HEAD` rail, Dynamixel 2.0 over TTL half-duplex; 7.4 V and 12 V classes rejected for V1. The family is not frozen until bench tests B1-B6 pass. Original note: RP-01 had not frozen the family. The head rail is designed for the 5 V XC330 case (M181 yaw, M288 pitch/roll); a 7.4 V-class servo would be direct-fed, change the bus to Feetech half-duplex TTL, and runs into the 8.4 V versus charger worst-case conflict above. A 12 V variant would force 3S and reopen the pack, tub and charger.

- [ ] Yaw cable across the joint (`board-specs.md` section 9):
  - [ ] Confirm loop length, cycle targets and the life assumption (placeholders: 1 m loop, 3 years); the sideband list grew to about 14-20 AWG28 conductors
  - [ ] CSI FFC vs the O14 mm disc bore: the Camera Module 3's 15-pin FFC is 16.0 mm wide and does not pass flat; order the Raspberry Pi PCN-36 revision of the 15-to-22-pin cable (11.5 mm wide, 1.25 mm per side), and check its bend life in the clock-spring
  - [ ] Route it in CAD as a clock-spring (bending, not a straight twist; a straight bundle needs about 288 mm free length for +-55 deg at 1% strain)
  - [ ] Build and run the qualification: 10^6 cycles at +-15 deg, 10^5 at +-40 deg, 10^4 at +-55 deg plus over-travel at 378 deg/s, logging loop resistance, CSI, UART and servo-bus errors

- [ ] Drive stage (`BD-02`): [gearmotor SKU lock remains open](../RP-03-locomotion/gearmotor-sku-decision.md). Pololu #4804, HP 6 V / 34.014:1 / encoder is the preferred prototype candidate (290 rpm no-load, 240 rpm at 0.127 N·m maximum-efficiency point, 6 A extrapolated stall). Fab.to.Lab lists #4804 in India, but exact-variant stock and quantity need confirmation. ~~Reconcile the 12.5 mm shaft and 67 mm body with the CAD~~ (done 2026-09-26, `RP03-CAD-10`). Get a written Fab.to.Lab quote naming the current #4804 revision: their page carries older figures (280 rpm, 6.5 A) and a wrong CPR. Proposed DRV8874 limit about 3 A (about 0.30 N·m, and it also caps regeneration at 3 A). Read the DRV8874 carrier's current-limit resistor (the Pololu page gives both 3.5 A and 4.4 A); set and verify a launch-compatible limit before bench power, then verify C3 motor-terminal voltage/speed clamp on the 8.4 V bus.

- [ ] **Regeneration limit (new hard requirement, `board-specs.md` sections 5.2.4 and 5.3):** the cells' maximum charge is 4 A, so the drive stage must hold regeneration into the bus to 3 A or less and to zero below 0 degC (brake, not coast). Nothing enforces it yet; it belongs to the DRV8874 current limit and the C3 braking policy (RP-03).

- [ ] Measure before relying on any number: pack loaded sag against state of charge (cold and aged), a measured 25R voltage curve, real head and drive currents, `LTC3119` output current at 5.4 V and thermal at 3 A, converter behaviour at the low line, brownout thresholds, hold-up capacitance and discharge time.

- [ ] Promote `board-specs.md` decisions (`BD-01…14`) to the registered RP-02 documents only after the above closes, and fix the candidate-screen outcome table where it still describes items superseded by addenda.
