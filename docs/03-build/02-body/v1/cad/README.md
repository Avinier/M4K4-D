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
| `check_body_layout.py` | CAD-volume mass/CoM, body axes/envelope, and whole-robot stability-screen audit. |
| `write_outputs.py` | Writes body dimensions, frames, and a partial body mass-register report to `generated/`. |
| `purchased/` | Provenance and current import locations for vendor STEP sources. |
| `snapshots/` | Dated images from STEP review. |

Build with the project's CAD Python environment from this directory:

```bash
python body-v1.step.py
python body-frame-v1.step.py
python check_body_frame_fit.py
python check_shell_frame_fit.py
python check_body_panel_fit.py
python check_body_layout.py
python write_outputs.py
```

The view includes the body frame, shell, service panels and their internal frames, panel hardware, speaker, microphones, compute tray, Raspberry Pi 5 and cooler, C3 carrier/DevKitC, power-distribution boards, yaw stage, internal wiring, and body connector/plug reserves. It also includes `CHASSIS_V1_REFERENCE`, loaded from the current chassis v1 Python source at build time. Hide that group in the viewer for body-only work. The chassis-owned battery pack, fuse holder, Adafruit drive boards, deck IMU, nose sensor, contact module, and motor wiring remain with the chassis group instead of being duplicated in the body groups. The combined view omits the chassis source's original J13 bolt/pin group and replaces it with the body integration hardware, which reverses the front-left M4 bolt and nut for fuse-shelf access. The chassis frame geometry and hole pattern are unmodified.

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

The shell is one printable, open-bottom piece with a narrow lower perimeter rim. Its four integral side bosses align with the frame posts at X = −32 and +64 mm, Y = ±64 mm, Z = 95 mm. Each boss has a Ø3.4 mm M3 clearance bore and stands 0.4 mm off the post face during lowering. Four M3 heat-set inserts sit in Ø4 mm post pilots. Four M3 × 16 screws enter horizontally from outside the shell and clamp the bosses to the posts. These are the shell retention points; the service panels have separate panel fasteners.

Assembly order after the first three frame/chassis steps above:

1. Fit the four shell-joint inserts to the frame posts. Install and test the frame-mounted body electronics and wiring. Leave the rear service panel and its E-stop operator, the other service panels, and the head/yaw moving parts off.
2. Lower the shell vertically over the assembled frame and chassis. The open floor passes the chassis and the shell bosses pass outside the posts. Fit the four outside-driven M3 × 16 screws.
3. Install the rear service panel with its E-stop operator, the front service panel and other shell-mounted fittings, then complete the yaw/head assembly and reconnect the service wiring. To remove the shell, reverse these steps after making the robot electrically safe.

`check_shell_frame_fit.py` checks the static geometry, shell lowering against the frame, fixed chassis and frame-mounted electronics, and straight access to the four screw heads. Its result is `generated/shell-frame-fit.json`. The E-stop operator is excluded only from the lowering-path check because it is mounted with the rear service panel after the shell; it remains at its final position in the combined CAD. This is a nominal CAD fit, pending printed fit coupons, insert pull-out testing, screw torque and vibration checks, and shell load/impact testing.

## Selected body shell and service panels

The faceted-shoulder shell is now the `BODY_SHELL` in `body-v1.step`. Its lower belly reaches X −61.1/+101.1 mm and Y ±91.1 mm at Z 70 mm, and a broad bevel cuts the belt crest between Z 70 and 82 mm. The front and rear service panels and their internal frames track the shell's sloped end stations. Their four M3 screws per panel use fitted wedge washers to seat on the sloped skins. The front panel has an integral annular speaker seat and slotted grille; the speaker face moves to X 95 mm and its cavity ends at X 92.5 mm to clear the compute tray. The rear E-stop well is fused with its panel and sits at X −60 mm, clear of PCB-02. `check_body_panel_fit.py` writes `generated/body-panel-fit.json` and checks the panel prints, frame, chassis, speaker, E-stop, washers, and screws for nominal interference.

FDM printability is still provisional. Both panel meshes are watertight single bodies. With the panels upright in model +Z, a 45° overhang measurement flags 5.8% of front-panel area and 1.5% of rear-panel area; the front speaker cup and rear E-stop well need planned supports. The front grille was thickened to 1.8 mm and the E-stop well nominal wall to 2.4 mm. Mesh ray sampling still finds isolated rear-well junctions below 1 mm even though its fifth-percentile thickness exceeds 2 mm. The lower panel edges offer only about 2.4 mm of bed contact, so upright printing needs a brim and a printer-specific slice review. These panels should not be treated as released print files until the rear junction is reinforced or the well becomes a separately printed, mechanically retained part, and a test print verifies the supports and fit.

## Mass and physics refresh

`check_body_layout.py` derives the selected shell/panels at 249.3 g and the connected frame, cassette and modeled joint hardware at 170.9 g from their CAD volumes and centroids. The estimate uses 1.20 g/cm³ effective PETG for skins, frames and the conservative structural print; 0.571 g/cm³ for wheel arches; and 7.85/8.50 g/cm³ for modeled steel/brass. The earlier Layout 02 mass rows (285.6 g shell/panels and 335 g frame) no longer described the authored body-v1 solids. The revised whole-robot register is 2,425.7 g at CoM (+18.48, +0.24, 105.92) mm. Neutral forward-launch tip acceleration is 1.712 m/s² versus the accepted 1.582 m/s² paper screen; a conservative bound over the current balanced head's yaw, pitch and roll centroids is 1.708 m/s². The head yaw datum remains (16, 0, 140) mm and its sweep floor remains 19 mm above the body roof. `generated/body-layout-checks.json` records the component breakdown, assumptions and checks.

The selected shell and printed frame contribute about 0.00262 kg·m² about the drive-axle vertical axis under those material assumptions, versus about 0.00291 kg·m² for their earlier CAD shapes under the same assumptions. This is a roughly 10% reduction in that subset's yaw inertia; it is not the whole-robot yaw inertia or the head yaw-servo load, because the shell and frame do not rotate with the head.

The 95 g remaining harness/fastener allowance is still unweighed and placed at X +20 mm in the register. With the other rows fixed, its actual mass-weighted X must remain forward of about −14.7 mm to retain the paper head-pose screen; placing all 95 g at X −20 mm would lower that estimate to 1.563 m/s² and fail it. Route and weigh the final harness and hardware before treating the margin as robust. These are CAD/material estimates, not weighed mass, motor approval, or a measured lift threshold.

The separate head assembly is not part of the body enclosure. Its body-side yaw drive and body-side head wiring are included. This is a subsystem review model, not a fabrication release. The model still depends on purchased STEP files in the prototype and chassis directories; see `purchased/README.md`.
