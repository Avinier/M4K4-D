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
- Audio: provisional 50 mm speaker basket, 44 mm cone, 34 mm acoustic-cavity reservation, amplifier envelope, and four body-mounted PDM microphone boards/ports. Exact parts remain unselected.
- Neck/yoke: no cladding. Head Layout 04's yaw disc stands 15 mm proud of the body top over a Ø90 opening. The body carries the adapter plate (on the upper cross-members), thin-section bearing, clock-spring reserve, a 1:1 spur pair and an off-axis XC330-M181 yaw servo, all starting 10.5 mm above the Pi 5 cooler. Full head motion; stops 3° beyond usable travel keep the head at least 4.2 mm off the disc.
- Internal packaging: exact downloaded Raspberry Pi 5 STEP; exact downloaded 608ZZ STEP pair; documented envelopes for motor, ball transfer, battery, cooler, drivers, DevKitC, power/safety, sensors, and cables when exact STEP is unavailable. The battery lies across the robot in a chassis tub under the deck (X 18–66, Z 32–56), flush with the deck top, and drops out through a bottom hatch.
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
| Axle stack | Motor face at \|Y\| 69 on a 2 mm flange; R15 boss to \|Y\| 86 with 608 pair at \|Y\| 74 / 81.5; Ø8 stub shaft \|Y\| 70.5–95; wheel pocket R18 to \|Y\| 88; min running gap 1.5 mm (stub to gearbox face), 2 mm boss end and arch trim, 3 mm radial |
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
| Speaker | 50 mm basket / 44 mm cone, centered at `(88, 0, 99)` mm |
| Battery | 48 × 75 × 24 mm envelope at `(42, 0, 44)` mm in a chassis tub; bottom hatch through the shell floor |
| Whole-robot CoM (register) | 2615 g at x +20.2, h 103.7 mm: x/h 0.195, a_tip 1.91 m/s², ball share 0.18 (target +25 / 124, x/h 0.202) |
| Microphones | Four provisional body PDM ports; front/rear left/right |
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

- exact GM25-370 rear cap, pigtail, and mounting-face details, including the face-screw pattern into the axle flange and the D-shaft length (9.5 mm assumed) that sets the stub-shaft bore;
- exact custom wheel/hub/tread geometry beyond the frozen 84 × 24 mm envelope, the stub-shaft-to-web fixing and axial retention (RP-03 P06 ≥ 3 N), and the dished wheel's printed mass;
- exact battery and body power-module geometries from RP-02, the battery hatch fastening and the harness path from the tub to the body;
- exact ICM-42688-P breakout and selected TCRT5000 breakout/comparator and connector bodies; the modeled carrier is an adjustable guarded requirement envelope;
- rear-only cliff sensing intentionally provides no dedicated forward or lateral coverage; level-floor operating restrictions and later propagation are tracked by `RP03-CAD-01`;
- the skid/TCRT functions live in a faceted keel under the rear crossmember and the visible tail is purely cosmetic (amending `RP03-CAD-03`); exact cartridge details remain provisional until the selected breakout and connector are measured, and the tail's heat-set insert engagement in the hub is unverified;
- the prior exposed full-width bumper is removed; the 40 mm touch cap has central-contact coverage only, pending propagation under `RP03-CAD-02`/`RP03-CAD-04`;
- the Pololu 1″ ball transfer is an envelope: its hole pattern (12.2 mm read as a radius) and screw-from-above fastening are unverified against the vendor drawing, and the pod's cap flexures, switch force and over-travel stop are unqualified;
- the GP2Y's rated 300 mm is a datasheet figure; the 0.70 m/s case leaves 5.5 mm of margin if charged to the nose front and must be confirmed on the target floor and obstacle set;
- exact speaker, amplifier, PDM microphone and acoustic-mesh parts, plus acoustic testing and isolation details;
- fastener thread engagement, inserts, sealing/gasket detail, tolerances, material/process selection and structural proof;
- RP-01 Layout 04 yaw legs, turntable and the body-side bearing/spur pair/servo are packaging envelopes; bearing SKU, gear module and backlash treatment, plate/cross-member load rating and fabrication detail are not finalized here.
