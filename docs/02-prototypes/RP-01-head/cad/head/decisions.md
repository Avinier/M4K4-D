# Head CAD decisions

Recorded: **2026-09-07**. Scope: **first RP-01 head layout**.

This is the current record of the head fitting discussion. **Fixed for first layout** means use the choice when laying out the head; it does not mean the mechanism has passed RP-01, an actuator has been selected, or manufacturing dimensions have been frozen. Estimates remain in [packaging-estimates.md](packaging-estimates.md), and inherited geometric requirements remain in [requirements.md](requirements.md).

## Decision register

| ID | Status | Choice |
|---|---|---|
| HEAD-CAD-01 | **Fixed for first layout** | One printed structural rib/backplate assembly; removable front carrier, rear cover, cosmetic ear shells, servo mounts and bearing cartridge |
| HEAD-CAD-02 | **Fixed for first layout** | Coaxial direct 1:1 roll drive with an independently supported metal spindle; XC330-size envelope as a packaging reference |
| HEAD-CAD-03 | **Fixed for first layout — builder selected** | Attach both removable cosmetic ears to the rolling face/cradle; preserve their rounded, cute shape |
| HEAD-CAD-04 | **Fixed for first layout** | Solid yaw spindle with an external guided cable/service loop behind the neck |
| HEAD-CAD-05 | **Fixed for first layout** | Mount the separate C2 motion controller, M008, removably on the rolling cradle, near the roll axis where practical |
| HEAD-CAD-06 | **Fixed for first layout — builder selected** | Form an integrated trapezoidal crown above the camera, continuing the head shell and face bezel into one coherent silhouette |
| HEAD-CAD-07 | **Fixed for first layout — builder selected** | Use A0 as the balance target: pitch axis through the estimated pitch-carried CoM; roll axis near the rolling assembly's own CoM |

These choices develop the existing body → yaw → pitch → roll candidate. They do not change joint order or close the [RP-01 mechanism decision](../../decision.md).

## HEAD-CAD-01 — Construction and repeated disassembly

Print the structural ribs and rear backplate together in PLA for RP-01. Make the display/camera/window front carrier removable, with separate rear access, removable cosmetic ear shells, and replaceable servo mounts and rear bearing cartridge. The front split is justified by access to the front assembly during repeated iterations; arbitrary cosmetic seams remain integral.

Use locating shoulders or other registered mating features to position structural parts, with screws providing clamping. Use captive nuts or metal inserts at repeatedly serviced internal joints; choose the exact hardware and validate its retention in the printed parts during detailing. Do not assume every internal structural screw must be M2: **visible M2 button-head hardware** is the existing appearance decision, while internal sizes and screw counts remain open.

This preserves the rugged, inspectable, screw-together droid character in the [foundation](../../../../00-foundation/constraints.md) while avoiding a separate bolted joint at every rib. Apply the existing PLA, weathering, panel-offset and cosmetic-seam decisions in the [material record](../../material-finish-mass-decision.md).

Open details: wall/rib thickness, locating features, fastener sizes/counts, insert or captive-nut pockets, access direction, print orientation and assembly sequence. No press fits or bearing-seat tolerances are selected yet.

## HEAD-CAD-02 — Roll drive

Start with the roll servo coaxial with the face-forward roll axis, driving 1:1 through a short coupling. A metal spindle and rear bearing cartridge carry the head load and overhung moment independently of the servo output bearing. Attach the roll servo housing and cartridge housing to the tilting pitch frame; the spindle, rib/backplate assembly and front payload roll.

The **XC330-size package is a layout reference, not an XC330 purchase or torque/speed selection**. The initial 20–25 mm bearing-centre spacing and approximately 105 mm depth stack are trial geometry only; see the [assumptions and candidate dimensions](packaging-estimates.md).

A pulley/belt arrangement remains a fallback if the real coaxial layout cannot fit or a quantified load/dynamic comparison justifies it. Changing to a belt must account for pulleys, tensioning, bearing loads, compliance, reversal behaviour and service space. Exact servo, shaft diameter, bearings, retention, coupling and preload remain open.

## HEAD-CAD-03 — Ears and moving frames

The builder selected **removable cosmetic ears attached to the rolling face/cradle**. Both ears therefore follow yaw, pitch and roll with the face. Their rounded, cute character is retained. Structural pitch pivots remain on their appropriate non-rolling frames; the ears carry their own cosmetic loads and do not form the joint's bearing support.

Attachment ownership is now closed for the first layout. Attachment geometry and clearance still need to be demonstrated: provide clearance around the pivots/yoke through combined motion without unacceptable visible gaps or silhouette changes. Do not switch back to yaw-yoke-mounted ears as an unrecorded packaging fix.

Terminology for the current serial arrangement:

| Part | Meaning | Moves with |
|---|---|---|
| Outer yaw yoke | The U-shaped support rising from the neck | Yaw |
| Pitch trunnions | The short side pivot shafts, with their bearings defining the pitch joint | Their shafts/housings follow their respective attached frames |
| Inner pitch frame | The frame tilting between the yoke's side pivots | Yaw and pitch |
| Rolling cradle and face | The payload rotating about the face-forward roll spindle | Yaw, pitch and roll |
| Cosmetic ear covers | Removable rounded parts attached to the face/cradle | **Yaw, pitch and roll** |

The U-shaped yoke is not itself a trunnion and does not roll in this joint order. Making that whole yoke roll would require an architecture change and a new mass/load comparison; it is not part of this decision.

The builder's selection supersedes the September 5 yaw-yoke cover proposal. With an illustrative ear centre 70 mm from the roll axis, an 18° roll moves that centre approximately **22 mm** relative to its neutral position. This explains why a rolling cover cannot be treated as a snug stationary bearing cap. It does not establish the required opening or prove a fit.

Validate the selected arrangement with front/side views and a combined-motion clearance sweep. Both ear covers and their attached fasteners now belong to all three moving sets. Split them into named M019c/fastener subitems without adding their mass again to M900; their mass was already included in the complete-head estimate.

## HEAD-CAD-04 — Yaw wiring

Use a solid, independently supported yaw spindle and route the wiring beside it as a guided service loop behind the neck. Visible insulated wiring is acceptable to the builder and compatible with the exposed mechanical appearance. A hollow spindle is not required for the first layout.

Here **service loop** means a controlled length of flexible wiring, with strain relief and defined attachment points. A **control loop** is the feedback/control algorithm; it is not a wire. Keep camera CSI, servo power/bus and other branches appropriate to their electrical and flex requirements rather than assume one undifferentiated cable can handle everything.

Provide the existing separable yaw-plane boundary for service and mass measurement. Route and guide the pitch and roll branches as well as the yaw loop. Exact cable, connector, dynamic bend radius, loop length, clamp coordinates and exposure protection remain open. The [harness study](../../../../01-system/head-harness-routing-study.md) still owns live-signal, restoring-torque and endurance evidence.

## HEAD-CAD-05 — C2 controller placement

Place M008 on a removable mount on the rolling cradle, close to the roll axis where packaging allows, with programming and connector access. Its board, mount, connectors and attached moving wiring therefore contribute to yaw, pitch and roll payloads.

**C2 and M008 refer to the same separate ESP32-S3 motion-controller assembly.** The display's ESP32-S3 renderer is already owned by M002. The two-controller boundary is already locked in the [RP-01 decision](../../decision.md#locked-controller-and-sensing-boundary); this record adds a working placement, not another board. Exact module, dimensions and installed mass remain open.

## HEAD-CAD-06 — Camera crown and continuous bezel

The builder selected a **local upward protrusion of the head shell at the central camera position**, above the display. In front view, this raised region has a **trapezoidal crown-like silhouette**, with sloping shoulders joining the surrounding head shape. Continue the face bezel into this raised camera region so the camera housing reads as a coherent part of the head.

Use this crown to provide camera packaging space above the main roofline. This supersedes the earlier proposal to solve the camera/display height conflict primarily by staggering their depth within the existing roofline. Depth staggering may still help the detailed fit, but the crown is now the selected appearance and packaging direction. The selected Camera Module 3 Wide is unchanged.

The visual continuity does not require an extra permanent assembly joint or prevent the existing removable front-carrier/service arrangement. The crown and camera remain part of the rolling head and follow all three axes with the face.

**Shape direction is locked; dimensions remain open:** crown height, width, depth, shoulder angles, edge treatment, wall thickness and camera mounting coordinates will be established in the layout. The decision authorizes the local upward extension; the resulting complete-head height, including the crown, must be reported explicitly against the earlier 95 mm nominal / 90–100 mm height band. Do not claim that the crown already fits that band, or silently treat it as outside the measured head envelope. Propagate the resulting dimensions when known.

Check lens field-of-view clearance, camera connector access, display clearance and the crown's swept envelope. Revise the shell/finish and camera-mount mass estimates and per-axis mass properties from the resulting geometry; the existing approximately 490 g pre-M008 model does not establish the revised crown-equipped head's mass.

## HEAD-CAD-07 — A0 balance target

The builder selected **A0 for the first layout**. Target zero fore–aft and vertical offset between the pitch axis and the centre of mass of the assembly carried by pitch (`x=0`, `z=0` in the existing pitch sensitivity model). Keep the roll axis near the rolling assembly's own centre of mass; the two carried assemblies need not have identical CoMs.

This selects a balance target, not an absolute pivot coordinate or a demonstrated tolerance. Calculate the component distribution, including moving actuator housings, rolling ears, camera crown, C2 and assigned wiring, then position the axes and iterate the layout. Do not equate the geometric centre of the shell with its CoM. Bearing support, display clearance and combined-motion clearance still need to be established.

Retain A1 (pitch pivot 5 mm behind the carried CoM) and A2 (5 mm behind and 10 mm below) as fallback/sensitivity comparisons. They are not equally active first-layout choices. Revisit them only if packaging or measured reversal/hold behaviour provides a reason, recording any changed decision. No deliberate gravity-bias offset or spring preload is selected for the initial A0 layout.

## What is still open

| Item | Evidence needed |
|---|---|
| Rolling-ear attachment geometry | Mounting and hidden clearance around the non-rolling supports through combined poses; attachment to the face is selected |
| Camera crown dimensions | Size the selected trapezoidal protrusion, camera mount and optical opening; report total head height and revised shell/mass properties |
| Actual component fit | Exact variant envelopes, horn/coupling hardware, connector exits, tool access and complete front/camera stack |
| Exact axis coordinates and achieved balance | A0 target is selected; derive coordinates from per-axis mass, 3D centre of mass and inertia, then verify fit and achieved offsets |
| Servo selection | Actual trajectory torque/speed demand plus thermal, reversal and settling evidence |
| Bearing and printed interfaces | Loads, retention, fits, stiffness, creep and assembly access |
| Cable routing | Selected cable geometry, live data, restoring torque, flex endurance and service replacement |

The approximately **490 g pre-M008 planning lower bound** already includes provisional mechanism masses. Replace those allowances with boundary-owned parts; do not add the full mechanism again. It is neither measured mass nor the payload of every individual axis. Existing component masses, envelopes, candidate pivots and the proposed internal arrangement are collected in the [pre-layout brief](pre-layout-brief.md); the project is not starting from an empty mass or fit model.

## Revision rule

When a fixed first-layout choice changes, record the affected HEAD-CAD ID, reason and replacement here, then update the relevant layout inputs and upstream mass/harness/prototype records. Label fit assumptions as assumptions until supported. Final mechanism acceptance remains in the RP-01 decision record.

| Date | Change |
|---|---|
| 2026-09-07 | Recorded the fitting discussion as five first-layout decisions; kept ear attachment, fit and actuator selection explicitly open |
| 2026-09-07 | Builder selected ears attached to the rolling face. Closed attachment ownership, updated mass membership, and retained mounting/clearance as layout work. Pivot positions will be reviewed in geometry; internal arrangement is prepared before modeling. |
| 2026-09-07 | Builder selected an integrated trapezoidal camera crown and continuous bezel. Local upward shell extension is authorized; crown dimensions, complete-head envelope and mass effects remain to be established. |
| 2026-09-07 | Builder selected A0 as the first-layout balance target. Exact coordinates remain derived layout inputs; A1/A2 remain fallback comparisons. |
