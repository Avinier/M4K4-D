# Makad V1 Moving-Head Harness Routing Study

| Field | Value |
|---|---|
| Status | **Research-backed candidate architecture — no production harness selected** |
| Version | 0.1 |
| Owner | Project builder |
| Created | 2026-08-29 |
| Last reviewed | 2026-08-29 |
| Feeds | RP-01 mechanism/cable rig, RP-02 electrical backbone, RP-06 layout, ADR-02/ADR-03/ADR-08/ADR-12 |
| Fixed inputs | Bounded roll/pitch/yaw; body-mounted primary compute; selected Camera Module 3 Wide SC0874; selected Waveshare display SKU 30493 |

## Decision boundary

Makad V1 does **not** need unlimited yaw. Slip rings therefore remain out of the active V1 architecture unless a later requirement introduces continuous rotation or the service-loop concepts fail their registered workspace/endurance gates. This note does not select a cable SKU, connector family, CSI bridge or production harness. It converts external examples into candidate geometry and a test protocol.

The central problem is not simply cable flexibility. A viable assembly must simultaneously preserve camera signal integrity, remain inside the 60 mm neck/head-intrusion package, contribute acceptable moving mass, avoid objectionable restoring torque, protect connector exits and remain replaceable.

## What the cited designs actually support

| Evidence | Supported lesson | Important limit |
|---|---|---|
| Bosch [US20100128122A1 / US8325229B2](https://patents.google.com/patent/US20100128122A1/en) | An anti-rotation arm moves the FFC endpoint with the camera so its tilt region bends along its length in one plane instead of twisting during pan. This is directly useful as a geometry pattern. | Bosch still uses a slip ring for pan. It does not prove that the same FFC can cross Makad's three axes unaided. |
| [Humanoid robot with advanced wiring assembly](https://exa.ai/library/legal/patent/xh7d1t7842qnmw2v6ncyp8) | Through-bore wiring, adjacent-actuator bundles and constraining a moving wire portion to one degree of freedom can reduce pinch exposure and the length that must move. | This is a patent architecture, not an industry mandate. Passive segmentation at every joint may damage MIPI CSI impedance and loss budgets. |
| [igus chainflex robotic cables](https://www.igus.com/cables/robotic-cables) | Continuous-flex/torsion cable is a real qualified product category; igus advertises variants through ±180° per 3 ft and up to ±360°/m with millions-of-cycle testing. | The family page does not establish that a small, camera-compatible cable exists for Makad. OD, mass, protocol, conductor geometry, shield and connector termination still need an exact quote/datasheet. |
| [Newnex high-flex active USB3](https://newnex.com/high-flex-active-usb-3-cable.php) | A vendor can qualify live USB streaming during millions of cycles rather than offering only static continuity data. Newnex states ≥6 million cycles. | Its stated dynamic radius is approximately 75 mm (12× cable OD), already larger than Makad's 60 mm neck allocation; this exact long active cable is evidence of the category, not a current fit candidate. |
| [Adapted Pepper](https://ar5iv.labs.arxiv.org/html/2009.03648) | A research team routed Ethernet and USB externally through the chest because routing through Pepper's removable moving neck required too much integration work. External bypass is a legitimate prototype/fallback route. | Pepper's geometry, camera and duty cycle differ. The paper demonstrates integration cost, not an internal-harness impossibility. |
| [Robot vision moving-cable guide](https://roboticscableassembly.com/blog/robot-vision-cable-assemblies-moving-joints) | Test at the installed radius while monitoring live data; inspect connector exits/clamps at milestones; treat the first 30–50 mm after a connector as a design input; use 100k/250k/500k+ screens proportional to risk. | This is supplier guidance, not a neutral standard. Cycle thresholds must be derived from Makad's duty/life target and frozen before scored testing. |

The universal “slip rings start at ±180–270°” claim is **not** adopted as a hard threshold. Makad avoids a slip ring because its actual authored ranges are bounded and a service-loop solution is lighter/simpler if it passes. The decision is driven by Makad's geometry and evidence, not a vendor slogan.

## Candidate V1 harness architecture

### 1. Partition by function

Do not force every circuit into one physical cable strategy.

| Branch | Candidate treatment |
|---|---|
| Camera MIPI CSI-2 | Its own controlled-impedance route. Keep passive connector count minimal; use a continuous guided FPC or an explicitly compatible active bridge. |
| Display/head-node power and semantic link | Fine-strand power plus UART/USB/CAN candidate as RP-02 decides; may use joint-segmented replaceable branches. |
| Servo power/bus | Sized and shielded/separated for peak current and noise; route near each axis without sharing camera strain relief. |
| Status-light/local signals | Keep local to the head node where practical so only low-bandwidth aggregate traffic crosses the neck. RP-01 has no runtime head IMU; any temporary bench IMU lead is instrumentation, not a production harness branch. |

### 2. Condition motion one joint at a time

For Concept A's body-fixed yaw → elevated pitch → head-fixed roll stack:

1. Enter yaw close to the yaw axis through the open/hollow centre and give yaw its own controlled loop or helical section.
2. Fix the downstream reference at the yoke so yaw motion is not passed into the pitch loop as uncontrolled torsion.
3. Enter pitch near one pitch pivot and guide a rolling, predominantly single-plane bend.
4. Fix the downstream reference again before the roll branch.
5. Give roll its own short symmetric loop or purpose-designed torsion section near the roll axis.
6. Provide strain relief and a service break only where connector access and signal integrity justify it.

“One moving segment per degree of freedom” is the preferred **mechanical decomposition**, not a command to insert an electrical connector after every axis. Low-speed branches may be connectorized per joint. The CSI branch must remain continuous unless the exact connector/adapter/bridge path is proven at its lane rate.

### 3. Control FFC orientation

Borrow the Bosch anti-rotation principle without copying its slip-ring architecture: use guides, saddles or rotating anchors so each FFC flex zone has a defined neutral shape and bends about the intended axis. Do not allow a flat cable to decide its own compound bend-plus-twist shape inside an empty cavity.

The guide must not create a hard hinge, scrape an edge, pinch at an extreme pose or load the camera ZIF. Clamp position and free length are configuration-controlled dimensions.

## Camera-link concepts to put on the RP-01 rig

| ID | Link concept | Why test it | Main failure mode |
|---|---|---|---|
| H1 | Continuous camera-compatible FPC with three mechanically isolated flex zones | Lowest head electronics and protocol conversion mass | Ordinary FPC may lack dynamic rating; compound motion or ZIF load may remain |
| H2 | Short static CSI FPC in the head → compatible active bridge → purpose-built fine high-flex round link across the joints | Moves the difficult flex duty onto a cable family that may have published dynamic data | Bridge mass/power/heat/latency; no exact IMX708-compatible bridge or cable selected yet |
| H3 | External protected bypass near the joint axes | Fastest diagnostic route and a credible prototype fallback when internal packaging blocks progress | Visual compromise, snag/service risk and uncertain effect on motion |

Do not buy the cited Newnex active cable as H2: its stated 75 mm dynamic radius is not compatible with the current neck package. Ask igus/Newnex or a local cable-assembly supplier for an exact lightweight construction only after the pose map, conductor/protocol requirement, installed radii and target cycles are known.

## RP-01 endurance protocol candidate

Freeze the final thresholds before scored testing. The first fixture protocol should include:

1. Build the exact installed route with production-intent clamps, guides, connector retention, mount and cover clearances.
2. Record every axis range, minimum installed radius, free length, clamp coordinate, connector-exit straight length and worst torsion angle. Photograph neutral and all extreme/recovery poses.
3. Measure cable restoring torque versus angle on each axis before cycling, including both sweep directions and unpowered pull.
4. Run a motion script containing individual yaw/pitch/roll sweeps, combined authored moves, reversals, extreme dwell, home/recovery and the realistic busy-minute sequence.
5. Stream the selected camera continuously. Log frame sequence/timestamps, frame gaps/drops, capture errors, driver/kernel camera errors, device resets/re-enumeration where applicable and visible corruption. Static continuity before/after is insufficient.
6. Run representative servo power, display animation and communications concurrently so EMI and voltage interactions are present.
7. Stop at configuration-controlled milestones for photographs and inspection of clamp creep, guide wear, FPC whitening/delamination, shield/jacket abrasion, connector/backshell rotation and ZIF movement. Candidate milestones: 0, 50k and 100k cycles; continue to 250k and 500k only when the registered duty/life target requires them.
8. Re-measure restoring torque and camera error/latency behaviour after each milestone. Any route or clamp change creates a new configuration and restarts comparable evidence.
9. Time replacement of the most exposed branch without disturbing unrelated structure.

One “cycle” must be defined by the exact pose sequence, not by a motor revolution counter. Final cycle-life acceptance must be derived from expected motions per busy minute × required operating life × safety factor.

## Immediate design outputs

- Add H1/H2/H3 routing volumes and clamp points to the Concept A section blockout.
- Produce a branch map listing camera, display/head node, servo power/bus and local sensor/light circuits separately.
- Draw neutral, all extrema and recovery pose cable geometry before requesting quotes.
- Keep the supplied Camera Module 3 FPC for static image/driver work only until H1 earns moving use.
- Request exact OD, mass per metre, dynamic radius, torsion rating, conductor/shield construction, connector termination and cycle-test conditions from any high-flex supplier.
- Carry all moving cable, guides, clamps, adapters and connector-retention hardware in the 250 g head mass tree and per-axis moving-mass sets.

## Selection rule

Select the production harness only when one candidate passes packaging, restoring-torque, live-signal endurance, installed mass/CoM, EMI/concurrent-load and service-replacement gates. Reopen the selected camera module only if no viable interconnect can be produced without disproportionate mass, latency, cost or architecture change under `camera-candidate-study.md` change control.
