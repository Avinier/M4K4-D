# Head pre-layout brief

Prepared: **2026-09-07**. Status: **existing evidence reviewed; internal arrangement proposed; CAD modeling not started**.

RP-01 already provides component envelopes, a detailed provisional mass model, motion targets, support concepts and candidate pivot offsets. The missing spatial inputs are the positions of those components and joints, followed by verified clearances and per-axis mass properties. Use the existing estimates to prepare the first layout and retain their evidence labels; do not treat every input as unknown or wait for a complete physical weigh-in before making a provisional blockout.

The builder has selected **ears attached to the rolling face/cradle** and an **integrated trapezoidal camera crown continuing the face bezel above the main roofline**. Pivot positions will be reviewed in geometry. The internal arrangement below is prepared before that first CAD layout and implements the choices in [decisions.md](decisions.md).

## Evidence already available

| Input | Existing evidence | Remaining work |
|---|---|---|
| Head/neck envelope | Earlier nominal 95 H × 150 W × 115 D mm complete head; 60 mm neck allocation; complete-width allowance already includes ears | Include the selected camera crown in the revised total height and swept volume; crown dimensions remain open |
| Display | Selected Waveshare no-touch SKU 30493, approximately 106.1 W × 67.8 H mm; 95.04 × 53.86 mm active image | Actual thickness/projections, plugs, sample mass and installed retention |
| Camera | Selected Camera Module 3 Wide SC0874, 25 W × 24 H × 12.4 D mm | Lens/PCB relationship, retainer, optical clearance and moving CSI cable |
| Head mass | Approximately 490 g before C2/M008 in the 1.2 mm PLA planning model; approximately 472 g before M008 at 1.0 mm | Replace provisional component masses and assign spatial positions; accepted weigh-in cells and M900 remain blank |
| Motion | Proposed best-case usable pitch −22…+40°, yaw ±55°, roll ±18°; authored trajectory speed/acceleration tables already exist | Check combined poses and set final stopping/cable margins |
| Pivot target | **A0 selected for first layout:** pitch CoM at pitch axis; A1/A2 retained as fallback comparisons | Compute each carried assembly's CoM, place axes, revise as mechanism masses change |
| Roll support | Rear metal spindle/cartridge, trial 20–25 mm bearing-centre spacing and direct coaxial drive | Exact shaft/bearings/retention, overhung loads and fits |
| Depth | Provisional X330 coaxial stack totals 105 mm; trial range 95–123 mm | A complete 3D fit, including camera, pitch pocket, controller, plugs and tool access |

Sources: [dimensional baseline](../../../../01-system/dimensional-baseline.md), [mass capture](../../payload-mass-capture.md), [physics](../../physics.md), [mechanism recommendation](../../concepts/servo-mechanism-recommendation.md), and [packaging estimates](packaging-estimates.md). The old 250 g mass, 0.001 kg·m² inertia and 0.2 N·m torque proxies remain invalid for servo sizing.

### What the approximately 490 g contains

These are grouped **planning values**, not new measurements. IDs and original rows remain in [payload-mass-capture.md](../../payload-mass-capture.md#parallel-provisional-model).

| Group | Existing estimate | Owners |
|---|---:|---|
| Installed display | 133 g | M002 |
| Window/mask, installed camera, camera cable and light | 38 g | M003 + M005 + M006 + M007 |
| Moving printed structure | 80 g | M010 + M011 + M012 |
| Moving actuator hardware | 35 g | M013–M015; provisional allowance to replace |
| Moving bearing portions | 22 g | M016–M018 |
| Finished installed shell, including ears | 148 g | M019c; includes 109 g PLA, 29 g finish, 10 g retained inserts/magnets/adhesive |
| Non-camera moving harness | 15 g | M020 |
| Hidden and visible fasteners | 19 g | M021 + M021a |
| **Total before C2** | **490 g** | Rounded provisional rows |
| Dedicated C2 board/mount/connectors | **Unknown** | M008; exact module not selected |

The 35 g actuator allowance is not a limit into which all servo hardware must fit. Replace it with actual candidate hardware masses carried downstream of yaw. Likewise, ear covers already exist inside M019c: attaching them to the face changes pitch/roll membership and inertia without adding a second ear mass to the complete-head inventory. Added mounting features can change the revised totals and must be owned explicitly.

## Tentative components

Yes, the servo references are already present in [packaging estimates](packaging-estimates.md#candidate-servo-envelopes):

| Reference | Package used in the existing research | Use in preparation |
|---|---|---|
| XL330-M288 | 20 × 34 × 26 mm; 18 g | Small-package comparison |
| XC330-M288 | 20 × 34 × 26 mm; 23 g | Current roll packaging reference |
| XC430-W240 | 28.5 × 46.5 × 34 mm; 65 g | Larger-package comparison |
| Feetech STS3215 family | Approximately 45.2 × 24.7 × 35 mm nominal; approximately 55 g | Family comparison; match the exact variant |

The inspected ST3215-C046 drawing has a 36.5 mm full axial outline, which the existing depth comparison already uses. These references are not three selected per-axis servos. Use replaceable servo adapters so a candidate change does not require redesigning the face carrier. Final axis assignments follow the torque-speed and thermal calculations with the revised mass tree.

For C2, only **ESP32-S3** and its separate-controller role are selected; no exact module SKU/envelope is recorded in the [control study](../../../../01-system/control-topology-options.md). Keep its reserved pocket provisional until a module/pinout/connector package is chosen. The display ESP32-S3 remains part of M002, not an additional M008 board.

## Proposed arrangement before modeling

This is a spatial proposal, not a demonstrated fit. Frame membership follows the existing serial yaw → pitch → roll order.

| Region | Proposed contents and attachment | Packaging instruction |
|---|---|---|
| Front face and camera crown | Window/mask and display below the central camera; camera housed in an upward trapezoidal shell protrusion with a continuous bezel; adjacent status light and removable front-carrier access retained | Implement HEAD-CAD-06; size the crown around the optical cone, board, mount and plugs, and include it in the full head envelope |
| Behind display | Rib/backplate structure and an accessible C2 pocket on the rolling cradle, just off the roll centreline | Keep the central spindle/flange corridor clear; place C2 near the axis where its board and connectors permit |
| Rear centre | Rolling spindle/flange; bearing cartridge and coaxial roll servo housing on the pitch frame | Preserve separate torque and load paths; neither spindle nor shaft must pass through the display |
| Side/rear mechanism pocket | One pitch servo on the yaw yoke, coupled to a supported pitch trunnion; passive bearing on the other side | Examine inboard/aft placement relative to the cosmetic ears; do not allocate the ear's 8–12 mm side allowance to an entire servo |
| Outer ears | Removable cosmetic parts attached to the rolling face/cradle | Keep their rounded outward silhouette; examine hidden inner/rear clearance around the yoke and pivots |
| Neck/body interface | Solid supported yaw spindle, body-fixed yaw servo below it, yoke rising to pitch pivots | Use the existing head/body intrusion allowance and keep the rear external cable route accessible |

### Selected camera crown needs a section view

The nominal head is 95 mm tall. Simply stacking the 67.8 mm display body and 24 mm camera PCB vertically consumes **91.8 mm**, leaving **3.2 mm** for all top/bottom walls, intervening gap and mounts. That arithmetic does not prove impossibility, but it makes a simple flat stack a poor unverified assumption.

The builder has resolved the shape direction with [HEAD-CAD-06](decisions.md#head-cad-06--camera-crown-and-continuous-bezel): **raise the shell locally above the camera as a trapezoidal crown, integrated into the continuous face bezel**. Size this upward extension around the selected camera, mount and optical opening. The complete-head height includes the crown; the earlier 95 mm nominal is a comparison baseline, not proof that the new silhouette fits it.

Depth staggering remains available during detailed packaging, but is no longer the primary selected solution to the height conflict. Use the actual lens-to-board position, field of view and connector drawing to establish clearances. Crown dimensions and the resulting envelope/mass changes remain open; the existing 18 mm front-stack allowance is still provisional.

### Ear appearance and pitch geometry are separate inputs

The ears move with the face; the outer yoke and pitch-bearing housings do not roll. Their neutral visual centres therefore need not dictate the exact pitch-axis position. Examine the mechanical supports behind/inboard of the cosmetic ear volume and any necessary opening on a hidden surface. Confirm this in front, side and combined-motion views before detailing the mounts. Clearance remains an engineering task under the selected ear attachment, not a reason to revert to fixed ears without a new decision.

For balance, use the builder-selected **A0 target** in [HEAD-CAD-07](decisions.md#head-cad-07--a0-balance-target): place the pitch axis through the estimated pitch-carried assembly's CoM and keep roll near the rolling assembly's own CoM. Derive absolute coordinates from the component layout, including servo housings, controller, wiring, ears and camera crown. A1/A2 remain fallback/sensitivity comparisons if packaging or measured motion quality warrants reconsideration.

## Other fitting details to carry into the layout

| Detail | Starting point from the existing work | What still needs detailing |
|---|---|---|
| Internal fasteners | The [sourcing matrix](../../../../01-system/candidate-sourcing-matrix.md#structure--fasteners) already lists M3 heat-set inserts and screws for service assembly; use this candidate in the initial boss/access study. Visible fasteners remain the selected M2 button heads | Exact insert, screw lengths/counts, captive-nut alternatives, engagement and retention in PLA |
| Printed parts/window | Retain 1.2 mm PLA skin and 1.5 mm PMMA window as mass-model reference cases; structural ribs/bosses need their own sizing | Actual wall/rib dimensions, window material/optical result and fit coupons; these thicknesses are not final fabrication specifications |
| Structural joints | Located mating features with screws clamping; matched metal horn/hub, removable coupling and supported spindle | Fits, alignment accommodation, shaft retention, bearing sizes and any measured need for preload |
| Wiring | Existing UART/USB semantic-link direction; separate camera CSI route and guided flex regions for yaw, pitch and roll; external yaw loop behind neck | Exact branches, compatible connectors, bend radii, clamps and electrical clearances; avoid unnecessary CSI connectors |
| Service access | Removable rear cover, front carrier, ear shells, controller mount, servo adapters and bearing cartridge | An unpowered removal sequence with access to screws/connectors before a part is withdrawn; flashing/BOOT/RESET path; yaw-plane demating for M900 weighing |
| Stops and power-off support | Reserve structural stop/support locations on the frames | Contact angles and stopping margin after the motion sweep; verify passive rest rather than rely on a servo position command |
| Heat and stiffness | RP-01 PLA and the existing thermal/creep and motion-quality checks | Keep connector/servo access and thermal assessment possible; final reinforcement or ventilation depends on layout and evidence |

The [CAD requirements](requirements.md), [harness study](../../../../01-system/head-harness-routing-study.md) and [RP-01 gates](../../gates.md) already define the relevant outcomes. These are implementation details to resolve using those records, not a new list of product preferences for the builder to choose blindly.

## What the first layout must establish

1. Front/camera stack and rear roll stack fit together, with actual side/rear space for pitch and C2.
2. Selected rolling ears and shell clear the yoke, supports, body and cables through compound motion.
3. A component table records mass evidence, position and yaw/pitch/roll membership in the RP-01 coordinate frame (+X forward, +Y robot-left, +Z up).
4. That table yields provisional per-axis CoMs/inertias and axis coordinates targeting A0; unknown masses remain explicit and measured values replace estimates later. Retain A1/A2 for fallback/sensitivity checks.
5. The resulting trajectory loads determine which tentative servo can serve each axis, with assembly and bench evidence closing final suitability.

No CAD geometry, fit validation, new weigh-in or final servo selection is claimed by this brief.
