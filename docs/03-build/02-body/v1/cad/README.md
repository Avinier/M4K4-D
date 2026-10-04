# Body v1 CAD

This directory follows the chassis v1 CAD layout: an editable model and STEP entry point at the root, `generated/` for derived reports, `snapshots/` for review images, and `purchased/` for vendor-reference provenance. Subsystem folders are added when a body component has its own model. The current body is one scoped assembly, so its source remains in the root.

| Path | Purpose |
|---|---|
| `body_v1_model.py` | Geometry, dimensions, labels, and the body/chassis scope boundary. |
| `body-v1.step.py` | CADgen build entry point for `body-v1.step`. |
| `body-v1.step` | Derived body assembly; ignored by Git and regenerated from source. |
| `body-frame-v1.step.py` | Focused two-print frame and joint-hardware review export. |
| `check_shell_frame_fit.py` | Static fit, lowering path, and outside screw access check. |
| `check_body_panel_fit.py` | Sloped service-panel, frame, functional-part, and fastener clearance check. |
| `check_mic_mounts.py` | Shell-mounted mic boards: seat, gasket, sound path, screw depth, rail clearance and clashes (D-037). |
| `check_charge_inlet.py` | Rear-panel charge inlet PCB-13: pocket depth, flush mouth, maximum-overmold fit, seat, screw engagement, clashes, PCB-02 clearance and the panel-removal sweep (D-040; about 6 min). |
| `check_compute_mount.py` | Compute tray, Pi 5 and Active Cooler retention, frame lugs, tray-screw driver access and the front insertion sweep (D-042). |
| `check_cooling_path.py` | Enclosure fan (BO-040 3010, D-043), +Y intake grille and collar, rear vent slots, shell lowering past the fan, mic-port distances and a first-order thermal estimate (D-042). |
| `check_yaw_stage.py` | Head yaw stage (D-044): fit, ±61° sweep with the counter-rotating pinion, ±62° hard stops, involute mesh clearance, cartridge and pinion install paths, and load, spring, FFC-loop and mass estimates (about 5 min). |
| `check_power_button.py` | Rear-panel mushroom power button: well clearance, PCB-02 clearance, W40 lead and `J2-9` plug clashes and the panel-removal sweep (D-041; about 5 min). |
| `check_body_layout.py` | CAD-volume mass/CoM, body axes/envelope, and whole-robot stability-screen audit. |
| `write_outputs.py` | Writes body dimensions, frames, and a partial body mass-register report to `generated/`. |
| `purchased/` | Provenance and current import locations for vendor STEP sources. |
| `snapshots/` | Dated images from STEP review. |

Build with the project's CAD Python environment from this directory:

```bash
python /path/to/text-to-cad/skills/cad/scripts/gen body-v1.step.py --write
python body-frame-v1.step.py
python check_body_frame_fit.py
python check_shell_frame_fit.py
python check_body_panel_fit.py
python check_mic_mounts.py
python check_charge_inlet.py
python check_power_button.py
python check_compute_mount.py
python check_cooling_path.py
python check_yaw_stage.py
python check_body_layout.py
python write_outputs.py
```

The view includes the body frame, shell, service panels and their internal frames, panel hardware, speaker, microphones, compute tray with its Pi fixings, Raspberry Pi 5 and cooler, enclosure fan, C3 carrier/DevKitC, power-distribution boards, yaw stage, internal wiring, and body connector/plug reserves. It also includes `CHASSIS_V1_REFERENCE`, loaded from the current chassis v1 Python source at build time. Hide that group in the viewer for body-only work. The chassis-owned battery pack, fuse holder, Adafruit drive boards, deck IMU, nose sensor, contact module, and motor wiring remain with the chassis group instead of being duplicated in the body groups. The combined view omits the chassis source's original J13 bolt/pin group and replaces it with the body integration hardware, which reverses the front-left M4 bolt and nut for fuse-shelf access. The chassis frame geometry and hole pattern are unmodified.

## Body frame/chassis assembly

`BODY_PRIMARY_FRAME` now has two connected print solids. `BODY_FRAME_MAIN_PRINT` carries three integral feet, the posts, side rails, upper cross rails and yaw adapter plate. `BODY_FRAME_FRONT_LEFT_FOOT_CASSETTE` is the fourth foot at (64, +48). It is separate because the fixed chassis fuse-holder shelf covers that mount and the locating pin at (59, +42); a one-piece four-foot frame cannot lower vertically over the shelf. The deck and its four M4 holes remain unchanged.

Assembly order in the CAD design:

1. Lower the main print onto the chassis rear locating pin and its three feet. Fasten those feet with three M4 × 12 button-head bolts from above and plain nuts from below.
2. Press the two M3 inserts into the cassette from its +Y face and place an M4 plain nut in its hexagonal pocket. Slide the cassette outward along +Y, under the fuse shelf, until its face meets the main frame's front-left side rail. Fit the two M3 × 16 side screws from the outboard face of the rail into those inserts before fitting the body shell.
3. Insert the front-left Ø4 × 8 locating pin from below. Insert the fourth M4 × 12 bolt upward through the existing chassis hole into the trapped nut. The chassis rail has the existing Ø10.4 relief around this bolt axis for underside access.
4. Remove the front-left bolt and pin, undo the two M3 side screws, slide the cassette toward −Y, then lift the main frame off the rear pin.

`check_body_frame_fit.py` tests connected solids, nominal chassis and hardware intersections, three-foot vertical lift, cassette slide, and vertical access for the other three M4 heads against the current chassis v1 source. The generated result is `generated/body-frame-fit.json`. This is a CAD fit check only. Print orientation and process, fit coupons, actual nut insertion and socket reach, insert retention, clamp loads, fatigue and head-to-chassis load proof remain release gates. The upper body shell has a clearance slot around the yaw adapter plate; the lower front cross rail was removed to clear PCB-03/04 and the chassis drive electronics.

`body-frame-v1.step` passes CAD solid validation. The full `body-v1.step` may report self-intersection failures in pre-existing imported Raspberry Pi 5 and cooler leaves; the new frame parts are not among those failures.

## Shell/frame assembly

The shell is one printable, open-bottom piece. Only the rear keeps a 4 mm lower rim; a front rim would hit the chassis front module while lowering, so the front and side walls end square at full thickness. Its four integral side bosses align with the frame posts at X = −32 and +64 mm, Y = ±64 mm, Z = 95 mm. Each boss has a Ø3.4 mm M3 clearance bore and stands 0.4 mm off the post face during lowering. Four M3 heat-set inserts sit in Ø4 mm post pilots. Four M3 × 16 screws enter horizontally from outside the shell and clamp the bosses to the posts. These are the shell retention points; the service panels have separate panel fasteners.

Assembly order after the first three frame/chassis steps above:

1. Fit the four shell-joint inserts to the frame posts. Fit the enclosure fan to its web (its lead plugs into PCB-09 `J9-4` later), then slide in the compute tray with the Pi and screw it down (D-042), then the C3 carrier. Install and test the frame-mounted body electronics and wiring. Leave the rear service panel with its power button, the other service panels, and the head/yaw moving parts off.
2. On the bench, fit both wheel-arch pods and the four microphone boards to the loose shell (see below). Leave the mic leads hanging free.
3. Lower the shell vertically over the assembled frame and chassis. The open floor passes the chassis, the shell bosses pass outside the posts, and the open-bottomed arches pass over the tyres. Fit the four outside-driven M3 × 16 screws.
4. Through the open front service aperture, plug the four mic leads into PCB-05: the +Y boards into `J5-2`/`J5-3`, the −Y boards into `J5-4`/`J5-5`. Unplug them first when removing the shell.
5. Install the rear service panel with its power button (plug `W40` into PCB-02 `J2-9` and `W16` into `J2-8` first), the front service panel and other shell-mounted fittings, then complete the yaw/head assembly and reconnect the service wiring. To remove the shell, reverse these steps after making the robot electrically safe.

### Wheel-arch pods

Each wheel arch is two separate prints: an ivory pod and an amber trim ring. The pod is a half ring over the tyre, radius 46–54 mm about the axle. Its inner face is the shell's outer skin, so it seats on the skin without entering it, and its outer face is flush with the tyre face at |Y| = 97 mm. Three M3 × 8 screws per side, at 20°, 90° and 160° about the axle on a 50 mm radius, enter from inside the shell. Each passes through a flat-seat boss on the inner skin into an M3 heat-set insert in a Ø4 pod pilot, pressed 0.5 mm below the seat. Drive them from inside the loose shell before it is lowered. A short hex key fits; the straight driver path to the centre line is checked clear. The trim ring keeps its 44–48 mm radii and is glued to the pod's outer face over their 46–48 mm overlap. The pod prints with that outer face on the bed, without supports.

### Power button (D-041)

The red mushroom in the rear-panel well is the power button. **There is no E-stop.** Body v1 imports the photo-derived [SparkFun COM-31041 STEP](purchased/sparkfun_com_31041_mushroom_red.step), a 16 mm momentary 1NO switch, from `purchased/`. Its local gasket face is mounted on the well floor and its actuator points out along −X. The model estimates a Ø25.2 mushroom, 9.0 mm projection in front of the floor, and 21.8 mm behind the floor's back face. The Ø16.2 cut-out in the 2 mm floor and the original XA1E keep-out remain as conservative clearance limits. The `ESTOP_*` constants retain their names for the well geometry and keep-out; the imported parts are labelled `POWER_BUTTON_MUSHROOM_*`.

The `W40` GH2 lead leaves the two terminals past the end of the contact block. It runs +Y beside the Pi's rear edge, then back above PCB-02's +Y edge, and drops to `J2-9` (`POWER_BUTTON_W40_LEAD_RESERVE_1…4`, `J2_9_GHR02_MATED_PLUG`). The button comes off with the panel: draw the panel out, unplug `J2-9` beside `J2-8`, then lift it away.

`check_power_button.py` writes `generated/power-button-fit.json`. Results with the locknut clocked 30°:
- The mushroom is 3.13 mm from the well wall.
- The button is at least 1.5 mm from PCB-02 by a conservative bounding-box clearance check, and its contact-block keep-out is 0.5 mm away (0.4 mm running-gap rule).
- The lead and plug are clear.
- The 40 mm removal sweep is clear.

The chassis reference group still carries the old XA1E at the same place; the checks filter it out.

### Compute tray and Pi 5 retention (D-042)

The compute tray is its own print, `COMPUTE_TRAY`: a 3 mm plate at Z 84.5–87.5, a 2 × 4 mm perimeter rib on top, slots for air to rise through, three ears and four bosses.
- **Pi 5:** sits on the four Ø6 bosses, which rise to the PCB underside at Z 94.05. Each boss takes an M2.5 × 4 heat-set insert (as CH-080). Four M2.5 × 6 low-head screws from above give 4.6 mm of thread.
- **Active Cooler:** held by its own two spring push pins in the Pi's cooler holes, as Raspberry Pi designed it. Nothing on the tray enters the Ø5 × 3.5 mm keep-out under each pin tip (`PI5_COOLER_PUSH_PIN_TIP_KEEP_OUT_*`, `E`).
- **Tray to frame:** three supports printed on the frame, each taking an ISO 7380 M3 × 8 screw from above into an M3 × 6 insert:
  - a lug on the rear −Y post, under an ear at (−32, −50.5);
  - a column on the front −Y foot's dog-leg, at (64, −33);
  - a block under the tray's rear +Y corner, on a short column from the lower rear cross rail, at (−24, 33).
- **Why these points:** the C3 carrier's `J10-1` plug keeps an ear off the front −Y post. On +Y, nothing may stand proud of the tray edge, because the tray goes in from the front past the chassis fuse holder (D-032, X 52–82, Y 39–49, Z 73–99). The front +Y corner is free; the rib stiffens it.

Assembly: screw the Pi to the tray on the bench, fit the cooler, then slide the tray in from the front, 2 mm high, and drop it onto the lugs. Do this before the C3 carrier, PCB-09 and the plugged harness go in, and after the enclosure fan (below). The tray screws are driven from above, before the yaw servo, PCB-09 and the `W40` lead are fitted.

`check_compute_mount.py` writes `generated/compute-mount-fit.json`. It checks:
- the PCB on the bosses and the boss clearance to the Pi's underside;
- the push-pin keep-outs, the screw heads against the Pi's top parts and the cooler, and the thread engagement;
- the tray on its three supports and the wall round each insert;
- clashes with every fixed body and chassis part;
- the driver path to each tray screw;
- the front insertion sweep, with the vendor Pi and cooler leaves swept as their bounding boxes (booleans on their moved vendor solids stall).

### Cooling path (D-042, D-043)

Air enters through a grille in the +Y side wall and leaves through the open floor and two slot grilles in the rear panel.
- **Fan:** BO-040, the photo-derived 2-wire DC 5 V 3010 hydraulic fan from [`purchased/dc5v_3010_hydraulic_usb_fan.step`](purchased/dc5v_3010_hydraulic_usb_fan.step), 30 × 30 × 10, centred at X 17.5, Z 107, midway between the +Y mic ports. D-043 replaced the 4010 at X 24, whose grille edge was 14 mm from FRONT_L. It sits on a web of the body frame between the +Y side rails (`FAN_WEB_*`), with its intake face at Y 68.9. Two 12 mm self-tapping screws (BO-041), driven from inboard through the web into the fan frame, hold it at (5.5, 95) and (29.5, 119), so its outer face stays clear for the shell to pass. Their heads sit 1.4 mm under and 0.9 mm forward of the yaw servo; the other two holes are behind it. Its modeled hole pattern (24 mm), hole size, airflow, noise and mass are unmeasured (`E`); verify the purchased fan before fabrication.
- **Switching:** it has no PWM or tach, so it runs on/off. A low-side MOSFET on PCB-09 is switched by Pi GPIO24 under the standard `gpio-fan` overlay, with a threshold to be set on the bench. It is fed from the 40-pin header's 5 V.
- **Wiring (`W41`):** the fan's own lead, cut to about 80 mm and re-crimped into its XH2.54-2P housing, runs from the fan's top-front corner above PCB-09's top-entry plugs to `J9-4` on PCB-09 (`HARNESS_W41_FAN_LEAD_*`, `C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE`).
- **Side grille:** vertical 2.5 mm slots inside R14, giving 373 mm² of free area. They stay out of the wheel-arch pod band, and a printed collar (R15–16.5, edge at Y 70.5, 2.55 mm from the 90° pod boss) limits recirculation round the fan face.
- **Rear slots:** eight 2.5 × 23 mm slots beside the button well, 460 mm² in all, inside the panel-frame aperture.
- **Floor:** at least 10,000 mm² of free horizontal area, so the inlet is not the limit.

The grille's edge is 24.1 mm from the FRONT_L port (38.6 mm centre to port) and 25.9 mm from REAR_L (40.0 mm). The rear slots are 42.7 mm from REAR_L/R. No mic pigtail crosses the intake path.

`check_cooling_path.py` writes `generated/cooling-path.json`. It checks:
- fan, screw, `W41` and grille clashes;
- the shell, with the +Y mic boards riding on it, lowering past the fan and web;
- the open intake path and the pod and boss clearances;
- that the rear slots pass the panel frame;
- the mic-port distances;
- a first-order thermal estimate (`E`).

That estimate assumes 0.44 W/K through the walls. BO-040 has no published curve, so it uses a typical 3010 5 V listing class (about 3 CFM free air, 3 mm H₂O shut-off) and a half-flow sensitivity case. At 8.5 W (Pi 6 W plus converters) it gives an internal air rise of:

| Fan | Rise |
|---|---|
| Sealed, no vents | 19.3 K |
| Vents only, fan off | 15.2 K |
| Fan on, half the listing-class flow | 10.1 K |
| Fan on, listing-class flow | 6.9 K |

The 4010 it replaced gave 7.0 K and 4.3 K with the fan on (D-042).

These numbers compare options; the bench measures the real ones, including the fan's real airflow.

The shell collar is a horizontal tube on a vertical wall in the roof-down print, so expect local support. The fresh DfAM measurement is still pending.

### Head yaw stage (D-044)

The head turns on a **61810-2Z** bearing (50 × 65 × 7, shielded) in a printed cartridge on the frame's yaw plate. The XC330-M181 drives it 1:1 through a scissor pinion. The head cables cross the joint as three 22-pin FFCs in a clock-spring cassette under the plate. Angles below are about the yaw axis (16, 0), from +X at yaw 0.

**Stack (Z, mm).**

| Z | Stationary | Rotating with the head |
|---|---|---|
| 155–151 | | head disc plate (head-owned) |
| 151–145.8 | pinion 146.4–150.6 at (16, 37) | hub gear, m1 z37, and three insert bosses |
| 145.6–144 | clamp ring (BO-049) | hub shoulder on the inner ring, 144–145.8 |
| 144–137 | bearing outer ring in the housing wall | bearing inner ring on the hub spigot |
| 141–135.5 | housing flange on the plate (138–141), seat lip in the plate pocket (135.5–137) | rotor clamp ring under the inner ring (133.6–137) |
| 138–134 | frame plate: R44 ring, R28 bore, R36.6 pocket | |
| 133.2–120 | FFC cassette stator | rotor drum, 121.4–133.6 |

**Parts.**
- **Cartridge housing (BO-057):** seat lip, wall and an R36.5–44 flange. Three ISO 7380 M3 × 6 screws at R40 (0°, 180°, 270°) go into inserts in the plate, driven from above. A stepped pocket at the pinion clears the drive hub, collar and spring; there the bearing OD is open for about 14°.
- **Clamp ring (BO-049):** stationary. Three M2 × 8 thread-forming screws at R34.5 (0°, 135°, 225°), outside the pinion's 58–122° shadow.
- **Hub (BO-045):** one PETG print.
  - Gear: m1, z37, 20° involute, both flanks thinned 0.0375 mm (0.15 mm nominal backlash for FDM).
  - The R12.15 bore pilots the head disc's R12 hub.
  - The shoulder sits on the inner ring; the R18–25 spigot fills the ring's bore.
  - Bosses at R22 (210°, 270°, 330°) take three M3 × 4 inserts. The head disc's three M3 screws (head-side) go in from above. Nothing on the hub outside R19.5 rises above Z 145.8 outside the 184–356° band, so the pinion never meets a boss within ±62°.
- **Rotor (BO-058):** one print holding three parts:
  - a ring that clamps the inner ring up against the hub shoulder, with three M2.5 × 8 thread-forming screws into the spigot;
  - the FFC drum;
  - the hard-stop **dog** at 270°.

  This screw path also carries uplift: lifting the robot by its head loads rotor → inner ring → balls → outer ring → clamp ring → housing → flange screws.
- **Hard stops:** the dog meets two bumps on the housing seat at 200.1° and 339.9° when the head is at ±62°. The bumps are 2.7 mm of radial engagement at R29. Usable travel is ±55°; set the XC330 position limits to ±58°.
- **Pinion (BO-046 to BO-048, BO-056):**
  - A printed hub sits on the horn (4 × M2 into its 12 mm PCD) and carries a Ø5 steel D-shaft.
  - The torsion spring (music wire Ø1.2, OD 8, 4 coils) sits on the hub's collar. Its legs go into the collar and the sprung half.
  - The sprung half (below) turns on the shaft, on a 0.2 mm thrust land. The fixed half (above) is keyed by the D-flat and held by an M2 countersunk screw into the shaft end.
  - Preload is 0.22 N·m at about 51° (5.25 teeth) of wind-up. A peg on the fixed half in an arc slot of the sprung half holds the wind-up off the mesh.
  - 0.5 mm lead-in chamfers let the pinion drop into mesh with the hub. No pin is needed under the disc.
- **Servo mount:** the XC330 hangs from a pad under the plate (part of the main frame print). Its four case screws are lengthened to M2 × 26 (BO-061) and thread 3.4 mm into the pad's pilots. Fit it from below before PCB-09, with the drive hub and shaft already on the horn.
- **FFC cassette (BO-050, BO-059):** three 22-pin 0.5 mm FFCs, 11.5 mm wide, run on edge in a 12.2 mm band. They make a rolling loop between the drum (R13.7) and the stator wall (R22.1), with a U-turn of R4.2. The stator hangs from the housing on three posts (45°, 150°, 270°) that pass notches in the plate bore.
  - Neutral wraps are 120° inner and 120° outer. The loop is sized for ±90°, beyond the stops: at ±90° the inner wrap runs 64–176° and the outer 86–154°.
  - The FFCs leave through a window at 300°. The CSI drops to the Pi 5 camera socket. Power and sideband run under the cassette floor to two ZIFs on PCB-08's new +X extension (`J8-6`, `J8-7`).
  - The inner ends rise through the drum core to **PCB-14**, a Ø35 ring board in the hub. The head harness demates on PCB-14's top, inside the hub, with the head disc off.
  - The cassette floor is 13 mm above the real cooler top (Z 107), inside the 10.5 mm headroom rule.

**Assembly (shell on).**
1. **Bench:** press the bearing into the housing and screw down the clamp ring. Drop the hub in from the top and screw the rotor on from below. Fit PCB-14 in the hub and plug the FFCs into it. Wind the FFCs into the stator and screw the stator's posts into the housing.
2. Fit the servo from below before PCB-09, with its drive hub, shaft and spring collar already on the horn.
3. Hold the cartridge above the plate. Reach through the R28 bore to plug the power and sideband FFCs into PCB-08 `J8-6`/`J8-7` and the CSI into the Pi. Lower the cartridge; the posts pass the notches. Screw the flange down.
4. Drop the pre-wound pinion onto the shaft. The chamfers take it into mesh. Fit the fixed-half screw.
5. Plug the head harness into PCB-14 through the hub bore. Screw the head disc and yoke to the hub (3 × M3, from above). Then fit the head's tilting assembly.

To remove the head, reverse these steps. Removing the cartridge needs the disc off first, then the pinion.

**Check.** `check_yaw_stage.py` writes `generated/yaw-stage.json`. It checks:
- the stage against every fixed part and itself;
- the yaw sweep;
- the stops at ±61.5° and ±62.5°;
- the mesh over one pitch: no interference, 0.072 mm running gap;
- the cartridge lowering (40 mm) and the pinion drop (12 mm);
- the axial gaps: pinion to shoulder 0.6, to clamp ring 0.8, to disc 0.4; spring to bearing OD 0.5.

It also gives these estimates (`E`):
- **Bearing static safety:** 17 or more, including a 100 N fall load at 100 mm.
- **Tilt play:** about 0.1° (single deep-groove bearing).
- **PETG tooth stress (Lewis):** 15.5 MPa at preload alone, 25 MPa at peak, 37 MPa at the servo's current limit. The sustained preload will creep the teeth; the spring follows it, losing about 0.0013 N·m per 0.1 mm. Swap to metal pinion halves if B4 fails.
- **Spring:** 0.25 N·m/rad, 1.49 GPa at preload.
- **Servo side load:** 8.7 N at rest, 13.3 N at peak, 0.2 N·m on its output. XC330 radial ratings are unpublished.
- **Drag:** the scissor's mesh friction (about 0.02 N·m) is the one that can use up RP-01's 8% yaw margin. B1 measures it.

### Microphone mounts (D-037)

The four PCB-06 mic boards are fixed to the shell, not the frame. Each board lands on a printed boss on the inner skin, coaxial with its side port (FRONT_L/R at X 54, Z 118; REAR_L/R at X −22, Z 108). The boss's flat seat is at |Y| = 71.3 mm and fills out to the sloped skin. Its upper face rises at 45° because the shell prints roof-down. A closed-cell foam ring (Ø6.5/Ø2.0 × 1.0 mm) sits in a Ø7.0 × 0.7 mm pocket round the port. The board lands on the seat, so the gasket is compressed 30% to a hard stop. Two M2 × 4 thread-forming screws, 5 mm above and below the port, clamp the board. They pass Ø2.2 board holes into Ø1.6 × 3.3 mm blind pilots, so each forms 3.0 mm of thread and leaves at least 0.98 mm of skin outside the pilot. The mic package is Infineon's PG-LLGA-5-4 STEP (`purchased/`). Its sound port is 0.68 mm off the package centre, so the package is placed by its port, not its centre. Sound reaches the bottom-port IM73D122 through a Ø2.0 bore in the skin and boss, the gasket bore and the Ø0.8 PCB hole: 5.9 mm in all at the front ports and 7.1 mm at the rear.

The boards ride down with the shell, past the frame's upper side rails (|Y| ≤ 68 mm). Nothing on a board may reach inboard of |Y| 69.0, so the boards have no header. Each carries a pre-crimped GH 4-way AWG28 lead soldered to pads beside the mic, lying flat on the board and leaving toward the body centre. The screw heads are the inboard-most parts, 1.0 mm clear of the rails. Fit the gaskets and boards to the loose shell on the bench, together with the wheel-arch pods.

`check_mic_mounts.py` writes `generated/mic-mount-fit.json`. Per board, it checks:
- the board seats on its boss and the gasket in its pocket,
- the mic sits on the port axis and the Ø0.7 sound path is clear,
- the port is open through the skin,
- the screw engagement and the skin left beyond each pilot,
- the clearance to the rails,
- no clashes with the shell, each other, or any body or chassis part.

It also gives a Helmholtz estimate of the port resonance: 13–23 kHz for a 1–3 mm³ mic front chamber (`E`), above the speech band. A printed boss coupon still has to prove the seat, the pilots, skin witness marks and the seal.

`check_shell_frame_fit.py` checks the static geometry, shell lowering against the frame, fixed chassis, frame-mounted electronics and PCB-05 with its edge connectors, and straight access to the four screw heads. It lowers the pods, trims, their screws and the four mic boards with their screws, gaskets and pigtails with the shell, checks them against the chassis and wheels, and checks that the shell, pods, trims, screws and inserts do not intersect, plus the inside driver path to each pod screw. Its result is `generated/shell-frame-fit.json`. The mushroom power button (D-041) is excluded only from the lowering-path check because it is mounted with the rear service panel after the shell; it remains at its final position in the combined CAD. This is a nominal CAD fit, pending printed fit coupons, insert pull-out testing, screw torque and vibration checks, and shell load/impact testing.

## Selected body shell and service panels

The faceted-shoulder shell is now the `BODY_SHELL` in `body-v1.step`. Its lower belly reaches X −61.1/+101.1 mm and Y ±91.1 mm at Z 70 mm, and a broad bevel cuts the belt crest between Z 70 and 82 mm. The front and rear service panels and their internal frames track the shell's sloped end stations. Their four M3 screws per panel use fitted wedge washers to seat on the sloped skins. The front panel has an integral annular speaker cup and an unobstructed Ø46 mm aperture, without a grille. The K 50 WP face sits at X 100 mm, 2.6 mm behind the printed lip; a modeled 0.8 mm annular silicone bond seals its Ø50 flange to the lip from inside. Its Ø54 clearance reserve runs X 82–97.5 mm and clears the compute tray. Install and seal the speaker in the removable front panel before fitting the panel to the shell. The rear button well (D-041; it held the E-stop) is fused with its panel and sits at X −60 mm, clear of PCB-02. `check_body_panel_fit.py` writes `generated/body-panel-fit.json` and checks the panel prints, frame, chassis, speaker, power button, washers, and screws for nominal interference.

FDM printability is still provisional. The 2026-10-03 DfAM mesh measurement (45° self-supporting limit, 1.2/1.6 mm FDM walls), with the earlier seven-slot front panel remeasured on 2026-10-04, found those prints watertight and single-bodied. The exposed-speaker panel is a single CAD solid but still needs a fresh mesh thickness and support measurement:

| Print | Orientation | Support area | Thinnest wall (min / 5th pct) |
|---|---|---|---|
| Shell | roof on the bed (upright needs support under the whole roof: 11%) | 3.0% | 1.7 mm on the 45° belly and shoulder facets |
| Front panel / inner frame | upright, as installed | pending / 3.8% | front mesh pending / 1.80 mm; Ø46 open lip has no grille webs |
| Rear panel / inner frame | upright, as installed | 1.5% / 3.1% | 1.57 / 2.07 mm |
| Wheel-arch pod | outer (tyre-face) side on the bed | 0% | 1.97 mm, round the insert pilots |
| Wheel-arch trim | flat | 0% | 3.0 mm |

The shell's 2.4 mm inset is horizontal, so its 45° facets are 1.7 mm normal to the skin. The panels follow the faceted ends and cannot lie flat (35–44% support), so they print upright: the speaker cup and button well need planned supports, and the 2.4 mm lower edges need a brim. Upright panels load their layer bonds across the face; the internal frames back the panel edges. The rear button well's earlier sub-1 mm junctions now measure 1.57 mm minimum. Treat these as unreleased until a test print verifies the supports, panel stiffness and fit.

## Mass and physics refresh

`check_body_layout.py` derives the selected shell/panels at 248.7 g (including the D-037 mic bosses, the D-040 charge-inlet pad, the D-043 3010 fan grille and collar and the D-042 rear vent slots) and the connected frame, cassette and modeled joint hardware at 178.5 g (with the D-043 fan web and the D-042 tray supports) from their CAD volumes and centroids. The estimate uses 1.20 g/cm³ effective PETG for skins, frames and the conservative structural print; 0.571 g/cm³ for wheel arches; and 7.85/8.50 g/cm³ for modeled steel/brass. The earlier Layout 02 mass rows (285.6 g shell/panels and 335 g frame) no longer described the authored body-v1 solids. The revised whole-robot register, with the D-042 compute tray and fixings (29.5 g, never counted before) and the D-043 3010 enclosure fan (10 g, `E`), is 2,478.7 g at CoM (+18.22, +0.52, 105.62) mm. Neutral forward-launch tip acceleration is 1.693 m/s² versus the accepted 1.582 m/s² paper screen; a conservative bound over the current balanced head's yaw, pitch and roll centroids is 1.689 m/s². The `shell_symmetric_about_y` check now allows 0.5 mm, because the +Y fan grille is deliberately one-sided. The head yaw datum remains (16, 0, 140) mm and its sweep floor remains 19 mm above the body roof. `generated/body-layout-checks.json` records the component breakdown, assumptions and checks.

The selected shell and printed frame contribute about 0.00261 kg·m² about the drive-axle vertical axis under those material assumptions, versus about 0.00291 kg·m² for their earlier CAD shapes under the same assumptions. This is a roughly 10% reduction in that subset's yaw inertia; it is not the whole-robot yaw inertia or the head yaw-servo load, because the shell and frame do not rotate with the head.

The 95 g remaining harness/fastener allowance is still unweighed and placed at X +20 mm in the register. With the other rows fixed, its actual mass-weighted X must remain forward of about −11.3 mm to retain the paper head-pose screen; placing all 95 g at X −20 mm would lower that estimate to 1.552 m/s² and fail it. Route and weigh the final harness and hardware before treating the margin as robust. These are CAD/material estimates, not weighed mass, motor approval, or a measured lift threshold.

The separate head assembly is not part of the body enclosure. Its body-side yaw drive and body-side head wiring are included. This is a subsystem review model, not a fabrication release. The model still depends on purchased STEP files in the prototype and chassis directories; see `purchased/README.md`.
