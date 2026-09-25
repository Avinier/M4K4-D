# RP-01 Layout 04

Layout 04 is Layout 03 with a new yaw stage. The helmet, face carrier, ears, C2 tray, camera, display, roll drive, pitch frame, hard stops and service sequence are unchanged Layout 03 geometry. Layout 03 is preserved. See the [brief](brief.md) for the sweep study and decision.

[Interactive CAD Viewer](http://127.0.0.1:3245/Users/avinier/robotics/makad/docs/02-prototypes/RP-06-cad?file=head%2Flayout-04%2Fhead-layout.step.py) · [STEP](head-layout.step) · [construction brief](brief.md) · [motion envelope](motion-envelope.json) · [dimensions](dimensions.md)

## What changed from Layout 03

- **Neck 60 → 49.5 mm, spindle replaced by a turntable.** The 24 mm vertical spindle band and the 4 mm bridge are gone. A Ø125 **yaw turntable disc** (4 mm top plate, 14 mm skirt rim, bearing hub, Ø14 cable bore) has its top at head Z −34.5 and stands 15 mm proud of the body top (head Z −49.5), leaving a 1 mm running gap. In RP-06 the neutral stack is **140 + 49.5 + 104 = 293.5 mm** (was 304).
- **Hard stops moved 3° beyond usable travel.** `storyboard.md` requires the stops to sit outside usable travel. They are now roll ±21 and pitch −25/+43 (usable travel stays roll ±18, pitch −22…+40). The stop-slot ends in `details.py` follow the shared constants in `motion_envelope.py`. This resolves the Layout 03 audit's hard-stop/range conflict; the stop load path is still unproven.
- **Full motion, guaranteed by the hard stops.** Across the full hard-stop grid the head sweeps to Z −30.3. The disc top keeps **4.3 mm** at the stops and **3.1 mm** at a further 1° of overtravel. No firmware roll/pitch limit is needed: [`motion-envelope.json`](motion-envelope.json) lists the full stop range for every row and records both cases.
- **Pi 5 cooler headroom kept.** The disc stands proud so the RP-06 yaw stage starts 10.5 mm above the cooler, as in body/chassis Layout 02.
- **Yaw drive is 1:1.** RP-06 couples an off-axis **XC330-M181** yaw servo (129 rpm at 5 V, 95 rpm at 3.7 V; peak yaw needs 63 rpm) to the disc through a 1:1 spur pair (pitch Ø37) under the disc plate. This keeps the actuator screen's direct-1:1 assumption and fixes its M288 yaw failure at 3.7 V. The spur mesh sits outside the servo's position loop, so the body's pinion is a scissor gear (module 1, 37 teeth, two 2.4 mm halves, 0.22 N·m spring preload against a 0.130 N·m peak; RP-01 gate P09). Lash is removed up to the preload; B4 measures what remains.
- **Short-knee legs.** Each leg rises vertically 13.5–21.5 mm behind the pitch axis, clear of the face carrier's chin-down sweep, then angles forward to the trunnion. The external yaw loop no longer needs the long Layout 03 knee because it runs through the disc.
- **Yaw cable.** The Y-side branch drops through the disc bore and lies flush in a disc-top groove to a keep-out below the +Y leg. The yaw twist is taken by the body-side clock-spring reserve (RP-06). The CAD-05 demating reserve sits just under the disc bore.
- **Regenerated evidence.** `revision-checks.json` (pass), `fit-checks.json` (0 hits), `assembly-checks.json`, `dimensions.*`, `motion-envelope.json`, the STEP and viewer parameters, `validate_geometry.py` (369 authored occurrences, all topology; the vendor display and C2 solids are now excluded from the authored check, since one display solid self-intersects in the Waveshare file) and the `review/` snapshots (`*_20260925T115158Z.png`).
- **Mass and A0.** The disc is authored PLA volume (M012), replacing the 20 g bridge allowance. A0 was re-solved from the revised mass tree and iterated with the envelope to convergence; see `axes.json`. The pitch axis was not moved for styling.
- **Still compromised against Layout 03:** the head-to-disc gap bottoms out at 4.3 mm at the stops (about 8 mm at usable travel), under the 25 mm finger gap of EN ISO 13854. The yaw stage is internal, gear-driven and harder to service. The camera sees body geometry from about 21.5° of chin-down (Layout 03: 23.6°).

## Revision 2026-09-25 — RP-01 CAD blockers

This pass closes the Layout 03 closure-audit items that are CAD work (RP-01 `gates.md` P07–P09, `fullproofmath.md` §12). The actuator family is the working `ACT-01` (XC330-M181 yaw in the body, XC330-M288 pitch and roll). Evidence is in `revision-checks.json`, `fit-checks.json`, `motion-signs.json` and [`fea/results.json`](fea/results.json).

- **Screw collisions fixed and checked.** The two front bearing-retainer screw heads (`bearing_retainer_M2_39.5_±9`) sat inside the rolling flange by about 5.53 mm³ each. The flange's back face now has two swept pockets (radius 9 ± 2.25 mm, ±22°: the stop travel plus 1° of overtravel). They clear the heads by 0.51 mm at every roll angle. `check_revision.py` now puts all 30 fasteners in the cross-frame motion grid (1,228 pairs per pose, 56 poses) and keeps them out only of the same-frame check, where thread engagement is intended. Result: zero hits.
- **Pitch-frame stiffness (P07).** FEA of the old frame, with the pitch couple applied on the cartridge seat and the +Y trunnion clamped, gave **0.98 N·m/rad, about 6 Hz**, which confirms the audit. The torque now runs from the trunnion arm through a 4 mm thick, about 18 mm deep **side web** on each side, a hollow **rear torsion box** (X −80.5…−68, Z 20.7…34.7, 3 mm walls) and a hollow **keel** under the cartridge slab. FEA: **51.4 N·m/rad, about 41 Hz** (33.8 N·m/rad, about 33 Hz, at E = 2.3 GPa), against the 30/40 Hz targets. The frame is 37.9 g, up from 18.6 g. The box steps down 2 mm under the C2 BOOT/RESET corridor (Y −37…−21), on the passive side. The front of the box stays outside the pitch servo's and adapter's sweep (28.8 mm radius).
- **Roll-servo mount (P07).** The servo case now bolts to the box's rear wall through the two lower front-face M2 holes on the official ROBOTIS drawing (16 mm apart, 22.5 mm below the output axis). The saddle walls and strap stay. FEA: **187.5 N·m/rad, about 84 Hz**; the old saddle was 17.9 N·m/rad, about 27 Hz. The screws are driven from the front, through Ø4.5 holes in the box's front wall, with the front carrier removed.
- **Bearing SKU.** 696-2Z (ISO 619/6-2Z), 6 × 15 × 5 mm, replaces the Ø16.2 × 6.2 trial seats. Seats are Ø15.1 × 5.2 mm, 22 mm apart, with the same end plates and outer-race shoulders. The seat fit and preload are bench items.
- **Hard stops.** Both pins are Ø2 hardened steel dowels (ISO 8734). The roll pin is 5 mm long, pressed through the whole flange (it used to sit 0.2 mm deep). The pitch pin is 8 mm long, 5 mm of it in a longer root lug. Under the `BD-13` Current Limits (roll 0.6 A, pitch 0.8 A; 0.31 / 0.41 N·m) the pin shear is 9–13 MPa and the PLA bearing stress 9–10 MPa. At a fault stall (0.93 N·m) they are 28–30 MPa and 23–28 MPa. The stops still sit 3° past usable travel and engage at 1° of overtravel. Impact at speed is untested.
- **Balance trim (physical path).** The ear caps carry up to Ø12 × 4 mm of tungsten on an M2 boss (roll, lever about 70 mm). The rear cover carries up to Ø20 × 3 mm of brass washers on an M3 insert on the roll axis (pitch, lever about 70 mm; coaxial, so it has no effect on roll). Both are at half capacity in the mass tree, so trim can be added or removed: **±1.69 mm roll-Y** and **±0.60 mm pitch-X** CoM correction (tungsten washers at the rear would give about ±1.4 mm). Full-capacity envelopes are physical parts in the motion grid. Z trim is not provided.
- **Signs.** `motion_signs.py` derives the storyboard-to-CAD multipliers from geometry (pitch +1, yaw −1, roll −1) and writes `motion-signs.json`, which is the firmware interface record.
- **Official servo data.** Both repo XC330 STEP copies are byte-identical to ROBOTIS download no. 1987. The mass tree uses ROBOTIS's published CoG and inertia tensor (`layout-01/parts/robotis_xl_xc330_moment_of_inertia.pdf`) in place of box estimates. The roll-servo CoG sits 3.2 mm further back than the old estimate. The roll-servo proxy is the 23 mm case plus two Ø16 × 3 horns, per the drawing.
- **Mass and A0.** Nominal roll/pitch/yaw is now **370 / 464 / 588 g** (was 356 / 431 / 555): +19 g of frame, +13 g of nominal trim, plus the corrected servo CoG. Inertia is 0.000675 / 0.000779 / 0.001282 kg·m² (+8 / +7 / +9 %). A0 was re-solved: the pitch axis moved 1.98 mm back and 0.88 mm down. The sweep still clears the disc (lowest shell Z −29.5 against the −30.5 floor).

## Geometry

- Full face/ear width retained. Helmet shoulders deepen from 14 to 24 mm between X−26 and X−60. The ear mounting belt stays 130 mm wide through X−78, then narrows to 104 mm at X−115; the rear lower edge rises to Z10 and the rear top is Z84. The pitch-servo adapter has a diagonal rear/outboard corner relief for shoulder clearance. Recessed lands and the existing planar front band belong to removable parts; no nested cosmetic shell or shroud.
- Display remains at Z6…74. Camera PCB starts Z77, giving the requested 3 mm gap. Crown top is **Z104**, +2 mm against Layout 02. The 140 mm body +49.5 mm neck +104 mm head stack is **293.5 mm** in the RP-06 integration.
- Neck is **49.5 mm** from the head underside to the body top; the proud yaw disc takes 15 mm of it (see above). Pitch remains an elevated, mass-derived axis; it was not lowered for appearance.
- M2 serviced receivers have nominal **Ø3.2 × 3 mm insert pockets** that open through the front and rear insertion faces. Existing visible screw appearance is retained. Final purchased insert dimensions, screw engagement and printed fits still need a SKU and trial coupon.
- Bearing cartridge has two **696-2Z (6 × 15 × 5) seats**, Ø15.1 × 5.2 mm, 22 mm apart, central shoulders and removable end retention plates. The 6 mm spindle and coaxial coupling remain independently bearing-supported. The coupling has radial M3 fastening bores and two simplified grub screws.
- Pitch and roll hard stops use a Ø2 steel dowel and an annular slot. Endpoint contact is authored at pitch −25/+43° and roll ±21°, 3° beyond the storyboard's usable travel (pitch −22/+40°, roll ±18°). Loads are in the revision section above; impact at speed is a bench item.
- C2 retains its original board seat in a removable open-rear tray. Rear edge jaws and USB-end corner caps keep the castellated PCB in the tray during lift. USB-C installed-plug depth, upward withdrawal and rear tool access are separate reserves. BOOT/RESET access assumes rear-cover removal. GPIO0/3/45/46 and GPIO21 are excluded from E-stop/fault assignments; no pin allocation is frozen here.
- Camera bracket and roll-servo saddle strap are removable. The camera bracket C-channels the Module 3 PCB Y-edges and pads the rear shield; two rear-access M2s still fasten the bracket to the crown. Actual servo attachment patterns, bearing fits, shaft retention and mount preload still need hardware-specific detailing.

## Optical layout

The physics group contains a rectangular field envelope covering the **102° horizontal field and image corners**, with vertical tangent inferred from 16:9. The assumed pupil lies at X−8, behind the X−2 lens front, with a conservative 3 mm entrance half-size. These assumptions are recorded in `optics.py`; they are not measured entrance-pupil data.

The old Ø17.2 opening clips that conservative envelope. A flared aperture with 0.4 mm additional edge margin replaces it. The verification report checks the revised crown, mask, window, skin and diffuser at neutral and pitch/roll extrema. Optical overlays are inspection geometry, never plastic or mass.

## Inspection controls

Physical, physics and harness open **on**; annotations open **off**. Independent master switches coexist with the named occurrence tree. Shell and FOV switches are subordinate to their respective masters. Roll, pitch and yaw sliders transform physical parts and overlays by their assigned frames. Neutral STEP includes all groups; use the viewer controls to hide inspection geometry.

Annotations contain small RGB triads and labelled construction bars. Values are the neutral global XYZ and axis-aligned dimensions, generated by the same `measure()` function as the dimensions log. The annotations move with their parts; their labels continue to describe the neutral reference pose. Fasteners have no individual triads. Camera and servo annotations use the actual imported solids, not the proxy boxes used for conservative fit checks.

## Trial harness and explicit gaps

The harness group contains separate CSI, display, servo bus, C2, LED and yaw-loop branches. The modeled straight connector exits are 30 mm long, with simplified jackets and centrelines. Connector positions within existing reserves and jacket diameters remain trial assumptions. The CSI guide is named separately. The Y-carried branch runs through the turntable bore; CAD-05 remains a demating reserve under the disc.

**This is not a continuous qualified H1 cable route.** The R/P/Y islands terminate before unresolved flex transitions. Named keep-outs show the gaps; no rigid wire silently bridges moving frames. The LED's 30 mm rearward exit cannot fit inside the crown, so that branch remains a keep-out pending the actual on-hand package drawing. The yaw branch stops at a keep-out below the +Y leg; its riser to the pitch frame and the body-side clock-spring are unqualified packaging reserves. The pitch-actuator connector exit remains unresolved. CSI needs actual FPC width, orientation and bend/cycle data before closing the route.

Existing M006/M020 cable allowances are retained once in the mass ledger. Jacket solids and reserves add no second full cable mass. The volume-based shell/frame rows are recalculated, while installed camera/C2/module allowances continue to include their small mounts.

The current mass artifact uses **M008=20 g as a nominal E case** and retains **10/20/35 g sensitivity**, producing approximately **370/464/588 g roll/pitch/yaw nominal** after the 2026-09-25 revision (first Layout 04: 358/432/557; Layout 03: 362/436/509). M008 remains physically `U`. The two head servos use ROBOTIS's published XC330 mass properties (23 g, official CoG and tensor).

The A0 coordinates are numerical balance targets from D/E masses, not machinable micron-level datums. For example, replacing the 23 g roll reference with a 55 g actuator moves estimated pitch balance by about 3.69 mm and adds about 0.017 N·m neutral hold torque. The physical design needs a measured trim/adjustment method.

## Structural and collision audit — 2026-09-13 (superseded where marked, 2026-09-25)

- *Superseded 2026-09-25:* the open pitch frame screened at 6–9 Hz (FEA later: about 6 Hz). It was redesigned; frame FEA gives about 41 Hz. Representative loaded modal validation, including the servo's own compliance, is still required (bench test B6).
- *Superseded 2026-09-25:* the open roll-servo saddle screened near 21 Hz (FEA later: about 27 Hz). The servo case is now bolted to the torsion box; FEA gives about 84 Hz.
- *Fixed 2026-09-25:* the two `bearing_retainer_M2_39.5_±9` screws overlapped the rolling flange by about 5.53 mm³ each; the flange is pocketed and fasteners are in the motion grid.
- Bearing reactions, spindle bending and yaw-yoke stiffness have not been demonstrated by the present record. Keep them OPEN rather than calling them acceptable without calculations or measurements.

## Motion-interface signs

Storyboard signs are the external command convention. Relative to the raw CAD right-hand rotations, use:

| Axis | Storyboard positive | CAD right-hand mapping |
|---|---|---:|
| Pitch | Chin down | `+1` |
| Yaw | Robot-right | `-1` |
| Roll | Robot-left side lowers | `-1` |

Magnitude-only clearance and torque screens are unaffected. Signed gravity, cable, asymmetric-pose and firmware checks must apply this mapping explicitly.

## Service sequence

1. Power off and support the head. Remove the four rear-cover screws. C2 BOOT/RESET tool access and upward USB plug/withdrawal reserves are then exposed. Remove the two tray screws and disconnect its local harness, lift the tray 27 mm in +Z into the upper service space, then withdraw rearward (−X). The PCB stays in the tray (edge jaws and corner caps). The sideways route was rejected because it hits the pitch frame.
2. For display/camera service, remove six front-carrier screws and unplug local branches. Withdraw the integral front carrier forward. Display retention is accessible through this split; release the retained display mount before extracting the full-size module. On the removed carrier, undo the two camera-bracket screws and withdraw the camera/bracket through the crown's rear opening. The bracket C-channels keep the camera on the bracket until those screws are released. No destructive shell split is required.
3. Remove four screws from each cosmetic ear cap to reach its two hidden mount screws. Ears remain tied to the rolling cradle when installed.
4. Rear access exposes the roll-servo strap and coupling grub screws. The two case screws into the torsion box are driven from the front, through the box's Ø4.5 access holes, with the front carrier removed. Release all of them to lift the servo out. The passive bearing cartridge is a separate part fixed to the pitch frame; release its four vertical fixings and end plates for bearing service, supporting/disconnecting the spindle first.
5. The one-sided pitch servo stays on the yaw-carried adapter. Release its adapter/retention hardware after supporting the tilting assembly. The exact selected-servo screw pattern and tool access remain hardware-specific completion items; the layout does not claim a finished purchased adapter.

## Reproduce

Use `/Users/avinier/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python` and the matching plugin scripts. Run from the repository root; prefix shell commands with `rtk proxy`.

1. Iterate `motion_envelope.py --write` and `mass_layout.py --solve` until `layout_axes.py` stops changing (three passes converge to a few µm), then write the envelope once more. It exits non-zero if the full-range sweep or the 1° overtravel clearance fails.
2. `check_revision.py` checks neutral intersections, the full 7 × 8 roll × pitch grid, jackets, hard stops, optics and C2 access; `check_layout.py` retains the original display/package checks. As of this audit, `check_revision.py` excludes fasteners from the physical cross-frame grid and therefore does not prove fastener clearance.
3. Matching `scripts/gen …/head-layout.step.py --write` exports the inspection assembly. `write_dimensions.py` creates the real imported-part dimension log.
4. `write_viewer_params.py` resolves named source groups against the generated occurrence tree, then rerun the generator to package the updated sidecar. Re-resolve after changing the tree.
5. `motion_signs.py` checks and writes the sign multipliers. [`fea/`](fea/README.md) holds the frame stiffness FEA (separate gmsh/scikit-fem venv).
6. `validate_geometry.py` checks exported references and solid validity. Matching `scripts/snapshot --job …/review/snapshot-job.json` creates the review packet. `check_viewer.mjs` checks the actual viewer feature resolver and switches.

Results are in `fit-checks.json`, `revision-checks.json` and `motion-envelope.json`; snapshots in `review/`. The Layout 03 [verification](../layout-03/review/verification.md) still covers the unchanged helmet, service and optics evidence.
