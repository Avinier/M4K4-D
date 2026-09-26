# RP-06 integrated body/chassis Layout 02 — CAD brief

- Model: labeled whole-body assembly combining the RP-03 body/chassis with the live RP-01 head Layout 04 source.
- Task: resolve the first-pass body/chassis attachment, fascia, service-panel, audio-packaging and yaw-yoke appearance questions without changing the frozen drivetrain geometry (track, wheel, axle height, ball contact) or head axes. `RP03-CAD-05` makes the drivetrain physically fit; `RP03-CAD-06` moves the body forward on it to recover CoM.
- Units: millimetres.
- Chassis frame: origin at ground on the drive-axle line and robot center plane; `+X` forward, `+Y` robot-left, `+Z` up.
- Head dependency: compose `RP-06-cad/head/layout-04/layout_model.py` directly. Do not redraw or substitute an AABB.
- Body placement (`RP03-CAD-06`): every body-side part (shell, panels, body frame, electronics, audio, harness, yaw stage, head) sits `BODY_SHIFT_X` = 16 mm forward of the drive axle. The drivetrain, ball, chassis and keel keep their chassis-frame positions; the rear crossmember and keel move forward with the body's rear wall.
- Head transform: Layout 04 head origin `(16 − pitch_x, 0, 189.5)` in the chassis frame (pitch_x from the head's `axes.json`); the yaw datum is the body top on the yaw axis, `(16, 0, 140)`.
- Drivetrain: 170 mm track, 42 mm loaded radius/axle height, frozen two-wheel Concept A, and a fixed non-interchangeable 1-inch ball-transfer module at `X=110`. Axle stack (`RP03-CAD-05`): each coaxial gearmotor bolts its output face to a chassis flange whose R15 boss carries the 608 pair and reaches into a pocket in the dished wheel; an 8 mm stub shaft runs in the bearings, takes the motor's 4 mm D-shaft and is fixed to the wheel web. No axle crossmember; cheek plates carry the rails round the gearboxes. Every stationary part keeps ≥ 1.5 mm to the wheel's rotating solids.
- External body: compact faceted shell, pale upper body, enlarged octagonal front/rear service panels that repeat the shell silhouette, and a functional front speaker grille. The shell floor is open across the axle (motors hang below the floor plane), under the battery hatch and along the pod tongue, so the body lowers onto the chassis from above. Visual references control cosmetics only.
- Structure: independent chassis rails (split round the gearboxes), axle flanges and cheeks, a two-plate deck with a relief over the motors, a battery tub, body posts and cross-members; four M4 body/chassis through-bolts and two locating pins; front/rear internal panel frames with fused bosses and four M3 fasteners per panel; a separately selectable rear module made of a compact faceted skid/TCRT keel under the rear crossmember (replaceable shoe/guards, TCRT cartridge) and a parked (not assembled) cosmetic telescoping stinger tail accessory for the rear service panel; a lean printed ball pod (`RP03-CAD-04`) that seats directly on the vendor flange, reaches back through the shell to the front crossmember (now inside the shell), and carries the centred front range sensor under a lid, covered by an octagonal touch hood on compliant arms; and the head-yaw load path.
- Audio (`RP03-CAD-11`, working selection 2026-09-26, [`../../peripheral-selection.md`](../../peripheral-selection.md)): Visaton K 50 WP 8 Ω speaker (Ø50 × 18 mm, frame face 0.5 mm behind the front panel) in the front of the body; the sealed back cavity is cut from 34 mm (X 63–97) to 20 mm (X 77–97, about 46 cm³ gross) because the old reservation ran through the compute tray and the Pi 5; `PCB-05` (MAX98357A + 2 × ADAU7002), 30 × 38 mm, lies flat above the Pi 5's front end (board Z 114, parts reserve to Z 123), because the old 38 × 30 × 9 amplifier reservation at (49, 0, 103) sat inside the Pi 5 and cooler; four `PCB-06` boards (12 × 8 × 1.0 mm, IM73D122V01 on the port axis, JST-SH 4-pin) against the port boots at the unchanged Layout 02 port coordinates.
- Neck/yoke: no cladding. Head Layout 04's yaw disc stands 15 mm proud of the body top over a Ø90 opening. The body carries the adapter plate (on the upper cross-members), thin-section bearing, clock-spring reserve, a 1:1 spur pair with a scissor (anti-backlash) pinion and an off-axis XC330-M181 yaw servo, all starting 10.5 mm above the Pi 5 cooler. Full head motion; stops 3° beyond usable travel keep the head at least 4.2 mm off the disc.
- Internal packaging: exact vendor STEPs for the Raspberry Pi 5 and its Active Cooler, the 608ZZ pair, the DevKitC-1, the two DRV8874 carriers, the TCRT5000, the GP2Y0A41SK0F, the XC330 yaw servo and the Pololu 1" ball caster (2691, authored from its drawing); datasheet-outline models for the selected speaker, `PCB-05`, the four `PCB-06` mic boards and the `PCB-07` IMU board (`RP03-CAD-11`); documented envelopes for power/safety and cables when exact STEP is unavailable. The battery is a 2S1P pack of two Samsung INR18650-25R cells with a 2S 20 A balanced BMS on top (`RP03-CAD-07`; datasheet/listing envelopes, no vendor STEP). It lies across the robot in a chassis tub sized to it under the deck (X 24.9–68.5 outer, pack X 27.9–65.5, Z 32–55.8), below the deck top, and drops out through a bottom hatch.
- Transparency: shell, service panels and wheel-arch pods share one intrinsic alpha (`SHELL_ALPHA` 0.28) and the nose hood is 0.45, so the internals read in every view; CAD Viewer controls independently hide shell, head, electronics, harness, and physics. Free-standing dimension bars are not part of the assembly.
- Assembly labels: every serviceable/fabricated/purchased group is independently selectable.
- Outputs: `body-chassis.step.py`, generated sibling `body-chassis.step`, parameter sidecar, dimensions/frames/mass JSON+Markdown, and diagnostic snapshots.
- Validation: generation, refs/facts/planes/positioning, solid validation, key frame measurements, deterministic source checks, opaque and transparent multi-view snapshots, and CAD Viewer handoff.
- Status: packaging-quality Layout 02, not fabrication release or structural certification.

## Primary dimensions

| Parameter | Value |
|---|---:|
| Wheel track | 170 mm |
| Wheel OD / width | 84 / 24 mm |
| Axle height | 42 mm |
| Front ball contact | `(110, 0, 0)` mm |
| Axle stack (`RP03-CAD-10`) | Pololu #4804 (official STEP, leads clocked to −X) face at \|Y\| 69 on a 2 mm flange with a Ø7.5 pilot for the bushing boss; 2 mm diaphragm \|Y\| 71–73 in the R15 boss takes 2 × M3 × 8 countersunk face screws at X ±8.5; boss to \|Y\| 88 with 608 pair at \|Y\| 77 / 84; Ø8 stub shaft \|Y\| 73–96 takes 8.5 mm of the 12.5 mm D-shaft; wheel pocket R18 to \|Y\| 90; min running gap 1.5 mm (stub to bushing boss and diaphragm), 2 mm boss end and arch trim, 3 mm radial |
| Body shift | Body and head 16 mm forward of the axle (`BODY_SHIFT_X`) |
| Body shell X range | −58 to +98 mm |
| Body shell Z range | 30 to 140 mm |
| Body width | 174 mm lower / 148 mm upper |
| Head-yaw body datum | `(16, 0, 140)` mm |
| Shell nominal thickness | 2.4 mm |
| Body/chassis attachment | Four M4 through-bolts + two 4 mm locating pins |
| Service-panel land | 2 mm constant-width overlap (inward offset of the panel outline); four M3 screws per panel |
| Service-panel lower edge | Front Z = 58 mm (clears chassis deck and ball pod); rear Z = 42 mm |
| Service-panel edge alignment | Front and rear panel straight side edges are parallel to their shell end-profile side edges |
| Speaker | Visaton K 50 WP 8 Ω: Ø50 × 18 mm, frame face at X 97.5 (0.5 mm behind the front panel), magnet end at X 79.5, axis Y 0 / Z 99; Ø46 cutout; internal basket/magnet split estimated |
| Battery | 2S1P 18650 pack, 37.6 × 67 × 23.8 mm at `(46.7, 0, 43.9)` mm: two Samsung 25R cells (Ø18.4 × 65, axes along Y) + 2S 20 A BMS (48 × 20 × 4.5, assumed thickness) on top, 110 g E; chassis tub with 1.5 mm gaps; bottom hatch through the shell floor |
| Whole-robot CoM (register) | 2568 g at x +18.77, h 105.05 mm: x/h 0.179, a_tip 1.75 m/s² (worst head pose about 1.44), ball share 0.17. Baseline revised from +25 / 124 by the builder on 2026-09-25 (`RP03-CAD-09`); the +20 mm line is re-based to the a_tip 1.582 it encodes at h = 124 |
| Ballast | 81.6 g mild-steel bar 9 × 60 × 19 mm at X 69.5–78.5, Z 33–52 under the deck, between the battery tub and the front crossmember; two M3 screws from the deck top at (74, ±20) (`RP03-CAD-08`) |
| Microphones | Four IM73D122V01 on `PCB-06` boards, outer face \|Y\| 70 against the port boots; ports `FRONT_L/R` (54, ±70, 118), `REAR_L/R` (−22, ±70, 108) mm; `FRONT_*` on ADAU7002 #1 (I²S SDI0), `REAR_*` on #2 (SDI1) |
| Audio front end | `PCB-05` 30 × 38 × 1.6 mm at X 45–75, Y ±19, Z 114 (parts reserve to Z 123), above the Pi 5's front end and forward of the cooler headroom: MAX98357A, 2 × ADAU7002 |
| Speaker back cavity | Ø54 × 20 mm sealed, X 77–97 (was 34 mm, X 63–97, through the compute tray and Pi 5); about 46 cm³ gross |
| Base IMU | `PCB-07` 16 × 20 × 1.0 mm on the chassis deck top (Z 56) at X 13–29, Y ±10; ICM-42688-P at (21, 0); two M2 × 5 at (22, ±7.5) into the deck crossbar; JST-SH 8-pin facing −X |
| Front range sensor | GP2Y0A41SK0F face at `(128, 0, 41)` mm: on the centreline in the ball pod, 18 mm ahead of the ball contact, behind a window in the touch cap |
| Front range look-ahead | Needed from the face: 161 / 203 / 271 mm at 0.50 level / 0.50 on 2° downhill / 0.70 m/s (`physics.md` §6, §10), or 184.5 / 226.5 / 294.5 mm if charged to the nose front; all inside the 300 mm rated range. The GP2Y's 40 mm minimum range is covered by the touch cap |
| Ball pod | Printed, octagonal section, X 92–128.5 (flange footprint), 35 mm wide, Z 29–54; its rear passes a shell notch to the front crossmember at X 80–92 inside the shell; vendor flange seats at Z 29; three M3 from inside the pocket; two M3 into crossmember heat-set inserts |
| Visible body-shell height | 110 mm |
| Neutral physical height stack | 293.5 mm (49.5 mm neck; yaw disc 15 mm proud) |
| Rear skid-pad ground clearance | 3.5 mm nominal |
| TCRT optical-face ground clearance | 10 mm nominal; must be calibrated on the target floor set |
| TCRT protective-guard bottom | 7 mm |
| TCRT channels | Rear only; CAD-context decision pending propagation |
| Rear skid-pad center | `(−27, 0, 4.75)` mm; replaceable shoe 12 × 10 × 2.5 mm; first contact at 6.1° pitch, before the CoM crosses the axle at 10.9° |
| Rear TCRT center | `(−54, 0, 13.5)` mm |
| Rear TCRT contact lookahead | 27 mm behind skid contact |
| Rear tail construction | Slate root hub + three telescoping eight-sided segments sweeping up 23°→37°→52° + 66° chisel tip; tip at X = −105, Z = 123 mm |
| Rear tail footprint | Planar radius 105.9 mm, inside the 134.8 mm ball-nose spin circle; top 123.4 mm, below the 140 mm body top |
| Rear tail finish | Opaque ivory `#E3DDC9` segments, `#707D82` hub, `#B88636` tip; no visible fasteners |
| Rear tail status | Parked accessory; `REAR_TAIL_ENABLED = False` |
| Rear keel finish | Translucent ivory `#E3DDC9`, alpha 0.34; cartridge, cable riser and M3 hardware visible |
| Rear module assembly group | `REAR_SKID_TCRT_MODULE` = `REAR_SKID_TCRT_KEEL` (+ `REAR_TAIL_STINGER` when enabled) |
| Touch cap | 40 mm octagonal hood, face at X 133.5, Z 29–56.6 (lower skirt cut 2026-09-24); 3 mm travel onto a lid-mounted side-actuated tact switch; floor-level objects below the GP2Y beam are not caught by contact |

## Assumptions still requiring measured closure

- the Pololu #4804 face as received (the CAD uses Pololu's drawing and STEP, SKU not locked): tapped length of the M3 face holes (2.85 mm in the STEP), bushing-boss height, shaft protrusion and D-flat length, and the lead exit and bend room behind the axle; the 2 mm printed diaphragm under the face screws needs a stiffness/creep check;
- exact custom wheel/hub/tread geometry beyond the frozen 84 × 24 mm envelope, the stub-shaft-to-web fixing and axial retention (RP-03 P06 ≥ 3 N), and the dished wheel's printed mass;
- exact body power-module geometries from RP-02; for the battery, the BMS board thickness and outline (4.5 mm assumed), the sleeve and tolerance stack, tub retention, the hatch fastening, the pack lead/connector and NTC, and the harness path from the tub to the body;
- the selected TCRT5000 breakout/comparator and connector bodies (the modeled carrier is an adjustable guarded requirement envelope); `PCB-07` is modelled from the ICM-42688-P datasheet and an unlaid-out board outline, and its M2 thread-forming engagement in the printed deck is unverified;
- rear-only cliff sensing intentionally provides no dedicated forward or lateral coverage; level-floor operating restrictions and later propagation are tracked by `RP03-CAD-01`;
- the skid/TCRT functions live in a faceted keel under the rear crossmember and the visible tail is purely cosmetic (amending `RP03-CAD-03`); exact cartridge details remain provisional until the selected breakout and connector are measured, and the tail's heat-set insert engagement in the hub is unverified;
- the prior exposed full-width bumper is removed; the 40 mm touch cap has central-contact coverage only, pending propagation under `RP03-CAD-02`/`RP03-CAD-04`;
- the Pololu 1″ ball caster is modeled from its dimension drawing (bolt circle O14.1, base O34 x 8.8); screw length and thread engagement in the ABS base are unverified on a real unit, and the pod's cap flexures, switch force and over-travel stop are unqualified;
- the GP2Y's rated 300 mm is a datasheet figure; the 0.70 m/s case leaves 5.5 mm of margin if charged to the nose front and must be confirmed on the target floor and obstacle set;
- the K 50 WP's internal profile (only its Ø50 × 18 mm outline and Ø46 cutout are vendor data), its flange bond and the grille/acoustic mesh; `PCB-05`/`PCB-06` outlines are unlaid-out estimates; how the mic boards fix to the body frame; acoustic testing and isolation (`AR-60…63`);
- fastener thread engagement, inserts, sealing/gasket detail, tolerances, material/process selection and structural proof;
- RP-01 Layout 04 yaw legs, turntable and the body-side bearing/spur pair/servo are packaging envelopes; bearing SKU, the scissor spring SKU and preload friction, plate/cross-member load rating and fabrication detail are not finalized here.
