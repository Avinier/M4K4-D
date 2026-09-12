# Head CAD decisions

Recorded: **2026-09-07**. Revised: **2026-09-12**. Scope: **RP-01 Layout 03 planning architecture and retained hardware-specific gaps**.

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
| HEAD-CAD-08 | **Builder selected after Layout 01 review** | Restore the octagonal head with crisp perimeter facets, a slim inner octagonal opening, coordinated bezel/crown height reduction, visible real screw points and larger hollow rolling ears |
| HEAD-CAD-09 | **Modelled in Layout 03; hardware-specific gaps remain** | Layered/tapered head: feasibility first vs Layout 02, reject only if way worse; yoke length by engineering judgment; **no shroud**; keep **modular service splits** (easy disassembly / module removal); 3 mm camera gap; C2 tray; inserts/bearings/coupling/stops; **look into vignetting**. Intended last RP-01 packaging/detailing pass |
| HEAD-CAD-10 | **Modelled in Layout 03; hardware-specific gaps remain** | Labelled viewer tree: physical subgroups; separate physics overlays (axes, CoM, gravity); separate trial harness; per-component global XYZ and size annotations, all hideable |

These choices develop the existing body → yaw → pitch → roll candidate. They do not change joint order or close the [RP-01 mechanism decision](../../decision.md).

## HEAD-CAD-01 — Construction and repeated disassembly

Print the structural ribs and rear backplate together in PLA for RP-01. Make the display/camera/window front carrier removable, with separate rear access, removable cosmetic ear shells, and replaceable servo mounts and rear bearing cartridge. The front split is justified by access to the front assembly during repeated iterations; arbitrary cosmetic seams remain integral.

Use locating shoulders or other registered mating features to position structural parts, with screws providing clamping. Use captive nuts or metal inserts at repeatedly serviced internal joints; choose the exact hardware and validate its retention in the printed parts during detailing. Do not assume every internal structural screw must be M2: **visible M2 button-head hardware** is the existing appearance decision, while internal sizes and screw counts remain open.

This preserves the rugged, inspectable, screw-together droid character in the [foundation](../../../../00-foundation/constraints.md) while avoiding a separate bolted joint at every rib. Apply the existing PLA, weathering, panel-offset and cosmetic-seam decisions in the [material record](../../material-finish-mass-decision.md). Layout 03 must not undo these splits: layered appearance lives on the removable parts; do not trap display, camera, C2, servos or the bearing cartridge behind a fused hull.

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

**C2 and M008 refer to the same separate ESP32-S3 motion-controller assembly.** The display's ESP32-S3 renderer is already owned by M002. The two-controller boundary is already locked in the [RP-01 decision](../../decision.md#locked-controller-and-sensing-boundary); this record adds a working placement, not another board.

**Module selected 2026-09-07:** Waveshare **ESP32-S3-Zero**, headerless, **23.5 × 18 mm**. It fits the reserved 35 × 25 × 15 mm pocket with clearance on both sides. Solder the harness to its castellated edges — pre-soldered 2.54 mm headers would consume most of the pocket depth, which is why the `-M` variant is excluded. The mount must expose the board's USB-C and BOOT/RESET, or route a defined flashing break-out, per CAD-04a. **Installed mass remains open**: M008 is board + mount + connectors + local harness, weighed as one assembly.

## HEAD-CAD-06 — Camera crown and continuous bezel

The builder selected a **local upward protrusion of the head shell at the central camera position**, above the display. In front view, this raised region has a **trapezoidal crown-like silhouette**, with sloping shoulders joining the surrounding head shape. Continue the face bezel into this raised camera region so the camera housing reads as a coherent part of the head.

Use this crown to provide camera packaging space above the main roofline. This supersedes the earlier proposal to solve the camera/display height conflict primarily by staggering their depth within the existing roofline. Depth staggering may still help the detailed fit, but the crown is now the selected appearance and packaging direction. The selected Camera Module 3 Wide is unchanged.

The visual continuity does not require an extra permanent assembly joint or prevent the existing removable front-carrier/service arrangement. The crown and camera remain part of the rolling head and follow all three axes with the face.

**Shape direction is locked; Layout 03 establishes the planning dimensions:** 104 mm crown-inclusive height, 150 mm width and 115 mm depth. The earlier 95 mm nominal / 90–100 mm band is superseded by dimensional baseline v1.10. Manufacturing tolerances and integrated RP-06 fit remain open.

Check lens field-of-view clearance, camera connector access, display clearance and the crown's swept envelope. Revise the shell/finish and camera-mount mass estimates and per-axis mass properties from the resulting geometry; the existing approximately 490 g pre-M008 model does not establish the revised crown-equipped head's mass.

## HEAD-CAD-07 — A0 balance target

The builder selected **A0 for the first layout**. Target zero fore–aft and vertical offset between the pitch axis and the centre of mass of the assembly carried by pitch (`x=0`, `z=0` in the existing pitch sensitivity model). Keep the roll axis near the rolling assembly's own centre of mass; the two carried assemblies need not have identical CoMs.

This selects a balance target, not an absolute pivot coordinate or a demonstrated tolerance. Calculate the component distribution, including moving actuator housings, rolling ears, camera crown, C2 and assigned wiring, then position the axes and iterate the layout. Do not equate the geometric centre of the shell with its CoM. Bearing support, display clearance and combined-motion clearance still need to be established.

Retain A1 (pitch pivot 5 mm behind the carried CoM) and A2 (5 mm behind and 10 mm below) as fallback/sensitivity comparisons. They are not equally active first-layout choices. Revisit them only if packaging or measured reversal/hold behaviour provides a reason, recording any changed decision. No deliberate gravity-bias offset or spring preload is selected for the initial A0 layout.

## HEAD-CAD-08 — Exterior refinements after Layout 01

The builder's appearance review is captured in [the Layout 02 brief](layout-02-brief.md), including the supplied close-up. Use real component dimensions at physical scale to determine the shell; lower both the excessive upper bezel and the crown's highest point as a coordinated revision. Restore clipped outer corners through the front/shell/rear cover, with crisp flat facets rather than softened exterior edges. The front-to-side transition has a sloping perimeter band bounded by **two distinct edges**. Clip inner aperture corners minimally to maximize visible active display area.

The builder accepted one front bezel incorporating the compact crown and a separate removable camera bracket. Place the entire LED package within the crown if practical; omission is authorized if compact packaging cannot accommodate it. Retain the existing real M2 screw appearance requirements and include actual wells/bosses and visible screw locations in the next revision. Larger, hollow or thinner-wall cosmetic ears are accepted; precise diameter/thickness and the revised head dimensions remain open. Recalculate balance and clearance rather than scaling the physical components or carrying over Layout 01's validation.

## HEAD-CAD-09 — Layout 03: layered taper, yoke, no shroud

The builder directed a **Layout 03 pass** after reviewing Layout 02, recorded in [the Layout 03 brief](layout-03-brief.md). [Layout 03](layout-03/README.md) is now generated and checked; Layout 02 remains preserved. See [verification](layout-03/review/verification.md) for the 104 mm crown, retained 32 mm yoke, mass/A0, service checks and explicitly open cable/hardware details.

**Taper:** use [`visuals/mvp-updated-after-spechseet.png`](../../../../../visuals/mvp-updated-after-spechseet.png) as a non-binding appearance cue (not ear mics, not body CAD). The head is not a plain octagonal tube — it may be layered and tapered. The modelling agent must first **deem that feasible** around 1:1 hardware and reject it only if it is way worse than Layout 02. Aesthetic layering comes after that call.

**Yoke:** the agent chooses the visible length below the head bottom. Do what is best for stiffness, look-up, cable loop and stack height. Do not drop A0.

**Shroud:** builder does not want one. Combined-motion clearance still applies; visible yoke at the ear openings is accepted.

Builder follow-up, 2026-09-09: Layout 03 is the intended last RP-01 packaging/detailing pass. Include a **3 mm** camera–display board gap, a removable C2 tray with CAD-04a flashing access, insert/captive-nut pockets, named bearing seats, coupling fastening and mechanical hard stops. **Look into vignetting** via the camera FOV cone overlay and a written clear/hit report. Do not recentre the pitch servo. Concept B will not be authored.

**Practicality:** keep the head modular and fairly simple to disassemble. Layered taper is appearance on the existing service parts, not a reason to glue stacks or trap modules. A scheme that is much harder to service than Layout 02 is way worse and is rejected.

## HEAD-CAD-10 — Layout 03 inspection tree

The builder required the Layout 03 STEP to be inspectable by group, recorded in [the Layout 03 brief](layout-03-brief.md#inspection-tree-head-cad-10). Layout 02’s three motion compounds plus one shell switch are not enough.

Build a labelled occurrence tree with four top groups: **physical**, **physics**, **harness**, **annotations**. Master viewer toggles hide each of the last three as a whole; named subgroups and parts remain independently hideable in the scene tree. Physics overlays show the three joint axes, origin triad, estimated roll/pitch/complete CoMs and gravity, driven from A0 and the mass tree. Harness is trial centreline-and-jacket geometry partitioned by function (CSI, display link, servo bus, LED, C2 local, yaw service loop), posed with the joint it rides; it does not select a cable SKU or certify flex. Annotations put each named part’s global XYZ (head-layout frame) and bounding-box size in a sibling subgroup, generated from the dimensions script.

Default open state: physical, physics and harness visible; annotations hidden. Overlays are not fabrication solids and must not enter the mass tree as PLA.

## What is still open

**Superseded Layout 02 revision, 2026-09-08:** [Layout 02](layout-02/README.md) implemented HEAD-CAD-08 with an **86 mm main roof, 102 mm crown-inclusive head, 130 mm core width, 150 mm complete width, 115 mm depth and Ø60 mm hollow rolling ears**. Bezel and crown were one part; the light reserve fit entirely in the crown. The 99 × 58 mm opening used 3 mm clips outside the active image. It added real screw/well/boss geometry, connected cradle and frame supports, a revised C2 footprint/service direction, and a provisional mass/A0 tree. These historical dimensions are recorded in baseline v1.9; Layout 03 and baseline v1.10 now govern. A per-part bounding-box log was added on 2026-09-09 at [layout-02/dimensions.md](layout-02/dimensions.md).

**Current CAD pass, 2026-09-10:** [Layout 03](layout-03/README.md) packaging is the accepted direction (104 mm stern, 3 mm camera gap, A0). Camera PCB clamp, C2 tray keepers and through-face insert pockets are modelled; see [verification](layout-03/review/verification.md). Display/servo/shaft retention and harness flex remain open. Concept A only.

**Layout evidence, 2026-09-08:** [Layout 01](layout-01/README.md) proposes a 109 mm crown-equipped head height, a 35 × 25 × 15 mm C2 installed-assembly pocket and provisional A0 pitch coordinates about 37.3 mm behind the front plane / 47.5 mm above the main-head bottom. It records 56 sampled clearance poses, inward/rearward yoke placement and hidden ear/skin reliefs. These are reviewed study inputs, not newly locked dimensions or a complete fit release; see the study's validation limits and imported-geometry findings.

| Item | Evidence needed |
|---|---|
| Rolling-ear attachment geometry | Mounting and hidden clearance around the non-rolling supports through combined poses; attachment to the face is selected; **no shroud** |
| Layered / tapered shell | Layout 03: feasibility vs Layout 02 using `visuals/mvp-updated-after-spechseet.png`; reject only if way worse, including if serviceability is much worse; aesthetics after that call |
| Service / modularity | Layout 03: preserve HEAD-CAD-01 splits; fairly simple to disassemble and remove display, camera, C2, ears, servos, bearing cartridge; do not trap parts behind layered shells |
| Visible yoke length | Layout 03: agent chooses what is best; do not drop A0 |
| Vignetting | Layout 03: FOV cone overlay plus a written clear/hit report at neutral and authored extrema |
| Camera crown dimensions | Size the selected trapezoidal protrusion, camera mount and optical opening; report total head height and revised shell/mass properties |
| Actual component fit | Exact variant envelopes, horn/coupling hardware, connector exits, tool access and complete front/camera stack |
| Exact axis coordinates and achieved balance | A0 target is selected; derive coordinates from per-axis mass, 3D centre of mass and inertia, then verify fit and achieved offsets |
| Servo selection | Actual trajectory torque/speed demand plus thermal, reversal and settling evidence |
| Bearing and printed interfaces | Layout 03: insert/captive-nut pockets, named bearing seats, coupling fastening, hard stops; purchased SKUs and PLA creep still later |
| Cable routing | Layout 03: trial centreline/jacket branches in a hideable harness group per HEAD-CAD-10; live data, restoring torque, flex endurance and SKU remain later evidence |
| Inspection overlays | Layout 03: physics, harness and annotation groups with per-component global XYZ and ΔX×ΔY×ΔZ, hideable independently |
| Camera–display gap | Layout 03: **3 mm** board-to-board; report crown height vs 102 mm |
| C2 mount, flashing access and pin assignment | Layout 03: removable Zero tray, CAD-04a USB/BOOT path; keep E-stop/fault off GPIO0/3/45/46 and GPIO21 |

The historical approximately **490 g pre-M008 spreadsheet** already included provisional mechanism masses. Layout 03 supersedes it with a nominal ~362/436/509 g per-axis tree at M008=20 g while retaining M008 sensitivity. Replace reference allowances with candidate-specific boundary-owned parts; do not add the full mechanism again. Neither model is measured mass or the payload of every individual axis.

## Revision rule

When a fixed first-layout choice changes, record the affected HEAD-CAD ID, reason and replacement here, then update the relevant layout inputs and upstream mass/harness/prototype records. Label fit assumptions as assumptions until supported. Final mechanism acceptance remains in the RP-01 decision record.

| Date | Change |
|---|---|
| 2026-09-07 | Recorded the fitting discussion as five first-layout decisions; kept ear attachment, fit and actuator selection explicitly open |
| 2026-09-07 | Builder selected ears attached to the rolling face. Closed attachment ownership, updated mass membership, and retained mounting/clearance as layout work. Pivot positions will be reviewed in geometry; internal arrangement is prepared before modeling. |
| 2026-09-07 | Builder selected an integrated trapezoidal camera crown and continuous bezel. Local upward shell extension is authorized; crown dimensions, complete-head envelope and mass effects remain to be established. |
| 2026-09-07 | Builder selected A0 as the first-layout balance target. Exact coordinates remain derived layout inputs; A1/A2 remain fallback comparisons. |
| 2026-09-08 | Builder approved all Layout 02 changes and the 1:1 method. Implemented slimmer octagonal head, integrated compact crown, crown-only LED reserve, Ø60 hollow rolling ears, real screw features and updated support geometry; revised baseline envelope and recalculated the provisional mass/A0 tree. |
| 2026-09-08 | Recorded that the current ear/skin clearance openings are temporary packaging reliefs. A finished moving or overlapping shroud must hide the yoke while preserving combined-motion clearance. |
| 2026-09-09 | Logged Layout 02 per-part dimensions from the parametric model. Opened Layout 03 (HEAD-CAD-09): rear flank taper, visible-yoke length vs stiffness without dropping A0, shroud on the revised shell. Not modelled. |
| 2026-09-09 | HEAD-CAD-10: Layout 03 occurrence tree must expose physics overlays, a trial harness group, and per-component global XYZ plus bounding-box dimensions, each hideable as a group and by named part. |
| 2026-09-09 | Builder: Layout 03 is the intended last packaging/detailing pass. 3 mm camera–display gap; C2 tray/CAD-04a; insert pockets, coupling, bearings, stops. Concept A is the RP-01 path; Concept B will not be authored. |
| 2026-09-09 | Builder: no yoke shroud. Yoke visible length is the modeller’s best judgment without dropping A0. Layered/tapered head is a feasibility call against Layout 02 (MVP3 visual; aesthetics after); reject only if way worse. Look into vignetting. |
| 2026-09-09 | Builder: preserve practicality and modularity. Fairly simple to disassemble and remove components; layered appearance must not trap modules or undo HEAD-CAD-01 service splits. |
| 2026-09-09 | Implemented Layout 03 on Layout 02: modest stern taper, 3 mm camera gap / 104 mm crown, 32 mm visible yoke, C2 tray and service path, trial inserts/bearing retention/coupling/stops, field-envelope check, grouped overlays and trial harness islands. Final sampled motion and revised service checks pass; cable-flex transitions and hardware-specific fabrication details remain open. |
| 2026-09-09 | Helmet refinement after review of that conservative 122 mm stern: 104 mm rear (Z10…84), 24 mm upper shoulders, rear M2 lands at Y±44 / Z26/65, and a clipped pitch-servo adapter corner for combined roll/look-up. 56-pose grid, jackets, optics, hard stops and C2/camera extraction pass. Not a fabrication release. |
| 2026-09-10 | Closed three Layout 03 detailing gaps without changing the 104 mm packaging: camera PCB edge clamp (0.10 mm to imported module), C2 tray edge/top keepers, front/rear insert pockets opened through the insertion faces. Display, servo, shaft and harness retention remain open. |
