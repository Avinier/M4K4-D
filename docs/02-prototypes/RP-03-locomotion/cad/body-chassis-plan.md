# RP-03 integrated body/chassis CAD requirements and closure checklist

Status: Layout 02 implemented for packaging review. This is the living CAD acceptance
checklist, not a fabrication release.

## 1. Frozen inputs

- [x] Use Concept A: two independently driven encoder wheels and a passive front
  support.
- [x] Use the ball transfer as the frozen front support. Do not keep a caster swap in
  the active assembly.
- [x] Make the ball-transfer mount fixed and article-specific; reject interchangeable
  adapter geometry in the integrated body/chassis.
- [x] Use the frozen SKU register in [`../research.md`](../research.md). A part may
  remain a custom-made article or a measured envelope; that does not reopen selection.
- [x] Build on RP-01 head Layout 03 as a live source dependency. Do not redraw it and
  do not substitute a mass box.
- [x] Treat RP-02 as the electrical authority for compute, storage, power distribution,
  protection, control and interconnect.
- [x] Use the supplied robot images only for cosmetic language. Their architecture is
  not authoritative.

## 2. Coordinate and interface contract

The chassis frame is the master whole-body frame:

- origin: ground plane on the drive-axle contact line at robot centre;
- `+X`: forward toward the ball transfer;
- `+Y`: robot left;
- `+Z`: upward;
- drive axle: `X=0`, `Z=42 mm`;
- wheel axes: parallel to `Y`;
- wheel centres: `Y=±85 mm` for 170 mm track;
- ball contact: `(110, 0, 0) mm`;
- head-yaw datum: `(0, 0, 140) mm`.

The RP-01 head-local frame remains unchanged. Layout 03 is placed with its origin at
`(37.9645316623, 0, 200) mm`, which maps the head yaw datum
`(-37.9645316623, 0, -60) mm` exactly onto the body yaw datum.

- [x] Encode both frames and the transform in source, generated JSON, and selectable
  geometry.
- [x] Label ground, axle, wheel, ball-contact, body, IMU and head-yaw datums.
- [x] Keep all mass and stability calculations in the chassis frame.
- [ ] Confirm loaded wheel radius from the physical custom wheel before release.
- [ ] Confirm ball-transfer loaded height and shimming from the physical article.

## 3. Assembly and geometry requirements

The active model must remain a labelled multipart assembly rather than a fused display
solid.

### 3.1 Head and body interface

- [x] Import the complete RP-01 Layout 03 assembly from its source.
- [x] Provide a body-side yaw collar, adapter plate and structural posts terminating at
  the yaw datum.
- [x] Preserve a centre harness passage and a visible cable route into the head.
- [x] Provide a viewer parameter for head yaw about the exact body datum.
- [x] Record the neutral stack as 304 mm and the RP-01 yoke as inherited trial
  geometry, not a finalized or load-rated mechanism.
- [x] Add a stationary neck cowl and yaw-moving hollow shroud/lower-leg cladding to
  reduce the visually empty U-shape without changing the inherited yaw or pitch axes.
- [ ] Replace the body-side yaw collar with the final bearing/fastener stack once the
  selected physical joint is measured.
- [ ] Check ±55° head motion against shell, cable loop and all service panels.
- [ ] Resolve axial, radial, torsional and impact load cases with a mechanical reviewer.

### 3.2 Chassis and locomotion

- [x] Model a primary chassis independent of the cosmetic shell.
- [x] Attach the body frame to the chassis deck with four explicit M4 through-bolts
  and two locating pins; eliminate frame/chassis solid interpenetration.
- [x] Maintain 170 mm wheel-centre track and 42 mm nominal axle height.
- [x] Model the frozen 84 × 24 mm custom wheel envelope on both sides.
- [x] Keep motors, wheel carriers and 608ZZ bearings as separate selectable parts.
- [x] Model the ball transfer at the frozen front contact.
- [x] Carry the ball transfer through a fixed three-hole flange, annular cradle,
  twin nose rails and front crossmember; service keep-out is physics-only.
- [x] Connect the rear skid root, diagonal arm, captured pad seat and replaceable pad.
- [x] Keep the body inside the wheel stance and the lower body clear of the ground.
- [x] Provide a continuous load path from wheel/motor carriers through the chassis and
  body frame into the head-yaw interface.
- [ ] Replace wheel, hub, motor and ball-transfer envelopes with exact measured parts.
- [ ] Add final shafts, keys/flats, retainers, fasteners, inserts and assembly tools.
- [ ] Close tyre scrub, hub runout, bearing preload and motor service access.
- [ ] Validate tip, traction and braking cases with measured mass and loaded radii.

### 3.3 Body structure and shell

- [x] Provide an internal body frame with vertical posts, cross-members and chassis
  attachment points.
- [x] Provide a faceted, tapered outer body derived from the visual references without
  inheriting their obsolete internal layout.
- [x] Make the shell intrinsically translucent and independently hideable.
- [x] Separate the pale upper body, dark mobility belt, front panel/grille and rear
  service panel into reviewable groups.
- [x] Model the lower mobility belt as a physical removable fascia with four M3 side
  fasteners; it is not a moving belt or drive element.
- [x] Match front and rear shell openings to the trapezoidal panels with a continuous
  2 mm overlap, internal frames, bosses and four M3 screws per panel.
- [x] Turn the front slat motif into open grille slots over the speaker package.
- [x] Preserve wheel, floor, ball-transfer and sensor clearances.
- [ ] Define the production shell split, fastening direction and removal sequence.
- [ ] Add bosses, inserts, ribs, draft/print strategy, tolerances and edge treatments.
- [ ] Close ventilation, acoustic openings, liquid/dust paths and pinch points.
- [ ] Run manufacturing-specific DfAM checks after the process is selected.

## 4. RP-02 internal packaging requirements

Packaging must show both part volumes and the access volume needed to install, cable,
cool and remove them.

- [x] Place the exact Raspberry Pi 5 STEP on a removable compute tray.
- [x] Reserve an active-cooler volume and airflow space above the Pi.
- [x] Place the battery forward of the axle and low in the body.
- [x] Place controller, dual motor-driver, power/safety and IMU groups separately.
- [x] Keep the IMU on the rigid body frame, away from wheel carriers and loose panels.
- [x] Keep power/safety access reachable through a service opening.
- [x] Provide cable-trunk volumes from battery/power to compute, drivers, motors,
  sensors and head.
- [x] Allocate a provisional 50 mm speaker basket, 44 mm cone, acoustic cavity,
  amplifier and four body-mounted PDM microphones with shell ports.
- [ ] Replace the battery, DevKit, DRV8874 carriers, power board and sensor breakouts
  with exact RP-02 parts or measurements.
- [ ] Add microSD/storage access and every required USB, Ethernet, display, camera,
  debug and power connector body.
- [ ] Model connector insertion/removal volumes, bend radii, strain relief and slack.
- [ ] Separate noisy motor/power wiring from sensitive sensing/data routes.
- [ ] Define fuse, disconnect, charge and emergency-access service paths.
- [ ] Complete a thermal path and airflow review using RP-02 dissipation estimates.

## 5. Sensors and external interaction

- [x] Include concealed front contact geometry and a front-facing distance-sensor
  keep-out/window below the speaker.
- [x] Include the selected rear-only TCRT5000 requirement envelope and optical datum;
  make no unsupported forward/lateral cliff-safety claim.
- [x] Keep sensors selectable independently of body and structure.
- [ ] Replace generic sensor envelopes with the exact frozen modules and carriers.
- [ ] Check fields of view against shell, floor, wheels, ball transfer and bumper travel.
- [ ] Add real connector exits, light seals, lens windows and cleaning access.
- [ ] Verify bumper stroke and switch actuation without loading the cosmetic shell.

## 6. Transparency and bifurcated review views

The review system follows RP-01 Layout 03. One source produces multiple purposeful
views; separate presentation-only CAD copies are not allowed.

- [x] Clean exterior view: head/body/chassis visible and physics hidden; remove
  free-standing dimension bars from the assembly.
- [x] Shell-hidden internal view: structure, electronics, drive and harness visible.
- [x] Physics view: support/contact geometry, CoM, axes and dimensions visible.
- [x] Head-yaw view: representative non-zero yaw about the body datum.
- [x] Viewer controls: shell, head, structure, drive, electronics, sensors, audio,
  harness and physics can be shown or hidden independently.
- [x] Every serviceable group has a stable assembly name for selection and inspection.
- [ ] Add subsystem-isolated electrical, drivetrain, sensing and service-removal views
  as exact component geometry closes.

## 7. Purchased/custom geometry and provenance

Every external geometry item must carry one of these states:

- `EXACT_VENDOR_STEP` — matched to the frozen article and checksum recorded;
- `MEASURED` — generated from an in-hand measurement record;
- `DATASHEET` — generated from an official dimensioned drawing;
- `ENVELOPE` — explicitly provisional keep-out; not fabrication authority;
- `CUSTOM` — owned source plus drawing and manufacturing assumptions.

Current state:

| Item | CAD state | Required closure |
|---|---|---|
| Raspberry Pi 5 | `EXACT_VENDOR_STEP` | confirm fitted cooler/connectors |
| 608ZZ bearing | `EXACT_VENDOR_STEP` | confirm selected supplier tolerance |
| RP-01 head Layout 03 | owned live source | preserve source transform and update on regeneration |
| custom wheel/hub | `CUSTOM` envelope | drawing and physical measurement |
| GM25-370 class motor | `ENVELOPE` | exact frozen article measurement or vendor STEP |
| ball transfer | `ENVELOPE` | exact article measurement or vendor drawing |
| battery and RP-02 boards | `ENVELOPE` | exact purchased articles and connector orientations |
| small sensors/connectors | `ENVELOPE` | exact board/carrier measurements |

- [x] Store purchased STEP files under `references/purchased/`.
- [x] Keep a generated/prose distinction between exact imports and envelopes.
- [ ] Add a measurement sheet for every in-hand custom or catalog article.
- [ ] Record source URL, part number, revision, capture date and checksum for every
  external CAD file before fabrication release.

## 8. Mass, CoM and physics

- [x] Maintain a component mass table with per-item CoM and source status.
- [x] Compute whole-robot mass and CoM from that table.
- [x] Display the resulting CoM and ground-contact/support geometry in CAD.
- [x] Check that CoM remains within the longitudinal support span.
- [x] Keep physics overlays separate from manufactured geometry.
- [ ] Replace all CAD estimates with measured masses for custom/fabricated items.
- [ ] Recalculate CoM after exact RP-02 parts, cables, fasteners and shell process close.
- [ ] Re-run forward/rear/side tip, turn, brake, slope and threshold cases from
  [`../physics.md`](../physics.md).
- [ ] Add inertia estimates only after mass and geometry are credible enough to support
  them; do not infer them from bounding boxes.

Current generated estimate: **2456.54 g**, CoM
**`(9.68, 0.15, 107.90) mm`**. It is a packaging estimate, not a test result.

## 9. Generation, checks and outputs

Required files in the active layout:

- [x] `body-chassis.step.py` — buildable CAD entry;
- [x] `body_chassis_model.py` — authoritative parametric model;
- [x] `body-chassis.step` — generated STEP assembly;
- [x] `body-chassis.params.js` — viewer controls;
- [x] `generated/dimensions.{json,md}`;
- [x] `generated/frames.json`;
- [x] `generated/mass-properties.{json,md}`;
- [x] `generated/checks.{json,md}`;
- [x] clean, internal, physics and yaw snapshots;
- [x] exact purchased reference files under `references/purchased/`.

Every accepted revision must pass:

- [x] source generation and STEP write;
- [x] assembly reference, geometry fact, plane and positioning inspection;
- [x] all Layout 02-authored solids validate closed and positive-volume; the full
  assembly retains five documented self-intersection warnings inside the exact
  Raspberry Pi 5 vendor STEP only;
- [x] wheel-centre track measurement;
- [x] RP-01-to-body yaw-transform check;
- [x] body width, ground clearance, battery position and CoM checks;
- [x] visual review from exterior, internal and orthographic directions;
- [x] interactive CAD Viewer handoff.

Before fabrication release it must additionally pass:

- [ ] exact-part collision and clearance checks at worst-case tolerances;
- [ ] head-yaw and cable motion sweep;
- [ ] installation/removal paths for every service item;
- [ ] fastener access and tool-clearance review;
- [ ] final DfAM/manufacturing review;
- [ ] physical mass/CoM reconciliation and mechanical sign-off.

## 10. Context-first propagation

1. Make a proposed dimension, placement or interface change in Layout 02 source.
2. Regenerate reports and snapshots and run the deterministic checks.
3. Review the affected exterior, internal, physics and service views.
4. Mark the change accepted or rejected in the CAD review context.
5. Only after acceptance, propagate the value to `research.md`, `physics.md`, RP-02
   contracts, dimensional baselines or decision records that depend on it.

This is deliberately the same lightweight pattern as RP-01 Layout 03. The CAD is the
place to test a proposed spatial change; accepted project requirements remain in the
appropriate Markdown authority.
