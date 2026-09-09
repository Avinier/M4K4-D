# Layout 03 — layered taper, yoke, inspection tree

Status: **modelled as [Layout 03](layout-03/README.md); checked packaging revision, not fabrication release**. See the [verification and remaining gaps](layout-03/review/verification.md). Preserve [Layout 02](layout-02/README.md) unchanged. Do not treat Layout 02 sampled clearance, mass tree or A0 datums as valid for the revised shell, yoke or harness.

This brief records the 2026-09-09 review of Layout 02. The [Layout 02 dimensions log](layout-02/dimensions.md) is **not** part of this pass; it is a Layout 02 logging artifact generated from the current model. Layout 03 must emit its own dimensions log after the geometry exists.

## What stays locked

Keep yaw → pitch → roll, A0 as the balance *target*, rolling cosmetic ears, coaxial roll on a supported spindle, C2 on the rolling cradle, 1:1 purchased envelopes, crisp planar facets, integral bezel/crown, the selected display/camera/C2 modules, and the HEAD-CAD-01 service splits (removable front carrier, rear cover, ears, servo mounts, bearing cartridge). Do not scale hardware to make a prettier shell.

Do **not** drop the pitch axis to fake shorter yoke legs. The ~45 mm from pitch (Z 45.3) to the head bottom (Z 0) is the elevated-pivot / A0 segment.

Do **not** relocate the display, slide C2 onto the spindle, or recentre the pitch servo. Concept B will not be authored; the one-sided pitch XC330 stays. C2 **tray and flashing path** are in this pass (the board seat stays).

Layout 03 is the **intended last RP-01 head packaging and detailing pass**. It is still not a servo freeze, not an optical certification, and not a scored-gate pass.

## Camera–display gap

Layout 02’s **1 mm** vertical PCB gap is too tight for a finished stack (CSI first bend, connector, assembly). Layout 03 **fixes** it: target **3 mm** board-to-board (Layout 01 used 4 mm). Report any crown-height change against the 102 mm working envelope. Do not silently grow the robot stack.

## C2 tray and flashing (CAD-04a)

Replace the purple footprint with a removable rolling-cradle tray for the headerless ESP32-S3-Zero: castellated harness, USB-C toward +Z, BOOT/RESET reachable with the rear cover off, or a wire break-out to the CAD-05 yaw plane. Installed depth and plug withdrawal stay distinct reserves. Do not use GPIO0/3/45/46 for E-stop/fault.

## Inserts, coupling, bearings, stops

Go beyond trial boxes. Layout 03 must show:

- heat-set / captive-nut pockets at repeatedly serviced joints (visible M2 stay appearance; internal size may be M3 as already listed in the sourcing matrix)
- named roll-bearing seats and retention on the 22 mm pair (fits still trial until a SKU)
- coaxial coupling with a shaft bore and a fastening scheme, still XC330-size as the envelope
- mechanical hard stops for pitch and roll at the usable-travel limits, independent of servo commands

Receiving pilots are not PLA threads. Exact purchased insert SKU can remain a BOM line; the CAD must have the pockets.

## Optical cone and vignetting

Layout 03 **must look into vignetting**. Put the Camera Module 3 Wide **field cone** (~102° horizontal) in the physics overlay, from the lens through the crown hole. Report whether the cone clears the bezel, mask and window at neutral and at authored pitch/roll extrema.

If the cone hits plastic, that is vignetting (dark image corners). Record the hit, then enlarge the hole or thin the rim — do not shrink the camera. Clearing the overlay is a layout check, not an optical-lab certification.

## Layered taper (feasibility first)

Appearance reference: [`visuals/mvp-updated-after-spechseet.png`](../../../../../visuals/mvp-updated-after-spechseet.png). That sheet is **non-binding** (eyes-only, no ear microphones, rolling ears stay). What to take from it for the **head** is that the shell is not a plain octagonal extrusion: it is **layered** — panel offsets, recessed lands, bevels, visible fasteners — and it tapers rather than staying a constant-width tube. Body/base taper on that sheet is RP-06, not this pass.

**Before adding aesthetic layers**, the modelling agent must think through a tapered/layered head around 1:1 hardware (display, camera, pitch servo keep-out, roll stack, ears) and **deem it feasible**. Compare mass, clearance, A0, stiffness and service to Layout 02.

- **Do it** if it is as good as Layout 02 or only modestly different.
- **Reject it** only if it is **way worse** than Layout 02 (fit, inertia, balance, unworkable pitch-servo/ear collision, or serviceability — trapped modules, destructive disassembly). Record the reason and keep the Layout 02 tube.
- Cosmetic layering (panel steps, recessed facets) comes **after** that feasibility call, not instead of it. Keep crisp planar facets; no smooth hull.

Keep full width at the face and ears. Rear M2 lands and the +Y pitch XC330 still set how far a stern taper can go. Re-run `mass_layout.py --solve` if the shell changes. Serviceability is part of this call: a prettier hull that is much harder to take apart is way worse.

## Yaw yoke length

Layout 02 yoke, from the dimensions log:

| Segment | mm | Role |
|---|---:|---|
| Pitch axis above head bottom | 45.3 | A0 / elevated ear-pivot — **not a styling knob** |
| Visible yoke below head bottom | 32 | Knee at Z −32; look-up clearance and cable-loop space |
| Pitch axis to knee | 77.3 | Structural leg length |
| Yaw interface | Z −60 | 60 mm neck allocation |

The modelling agent **chooses the visible length** (the segment below Z=0). Do what is best for stiffness, look-up clearance, the external cable loop and the 302 mm stack. Do **not** drop the pitch axis to fake a shorter neck. Do not lengthen without a recorded reason. A rearward knee stays unless a new pitch-up check replaces it. Report the chosen millimetres and why.

## No shroud

The builder does **not** want a yoke shroud. Do not add a moving or overlapping cover to hide the yoke. Combined-motion **clearance** at the ears still has to work (reliefs are allowed). Visible mechanism at those openings is accepted.

## Practicality and modularity

Layered taper and detailing must **not** make the head harder to take apart. Preserve [HEAD-CAD-01](decisions.md#head-cad-01--construction-and-repeated-disassembly), [CON-P01](../../../../00-foundation/constraints.md) and D-06: modular, screw-together, service splits only where they earn their keep.

Keep it fairly simple to disassemble and to **remove components** without destroying structure or pulling unrelated assemblies:

- Front carrier, rear cover, cosmetic ears, C2 tray, camera bracket, servo mounts and bearing cartridge stay independently removable.
- Display, camera and C2 come out along their existing access paths (front carrier / rear cover / tray) with captive or insert fasteners — not glued, not trapped behind a fused layered hull.
- Aesthetic panel offsets, recessed lands and bevels live **on** those removable parts. Do not add nested shells, snap-only stacks or extra cosmetic splits that only look layered.
- A tapered/layered proposal that traps hardware, needs destructive disassembly, or turns a two-cover service into a full tear-down is **way worse** than Layout 02 and is rejected on that ground even if the silhouette is nicer.

## Inspection tree (HEAD-CAD-10)

Layout 02 only groups by moving frame (roll / pitch-carried / yaw) plus a single **Show shell** switch. Layout 03 must be a labelled occurrence tree so the viewer can hide and show **groups and named components** without rebuilding STEP. Viewer booleans are master switches over those groups; the scene tree is the per-part control.

**Global frame** for every XYZ readout is the existing head-layout frame: origin at the front/bottom centre of the main head, **+X forward (face), +Y robot-left, +Z up**. That is “global” inside this model. Robot-base coordinates wait for RP-06.

Default visibility when the model opens: physical **on**, physics **on**, harness **on**, annotations **off**. Each master switch is independent. Pose sliders still move every child that belongs to R, P or Y, including overlays and wires.

```
RP01_Layout03
├── physical                          master: always the product
│   ├── rolling                       frame R
│   │   ├── display_camera
│   │   ├── c2
│   │   ├── skin_ears
│   │   ├── cradle
│   │   └── fasteners
│   ├── pitch_carried                 frame P
│   │   ├── roll_drive
│   │   └── pitch_frame
│   └── yaw_carried                   frame Y
│       ├── yoke
│       └── pitch_actuator
├── physics                           master: show_physics
│   ├── axes                          roll, pitch, yaw lines through current A0; origin triad
│   ├── com                           spheres at estimated roll / pitch / complete CoMs
│   └── other                         gravity −Z; A0 axis-to-CoM residual if any
├── harness                           master: show_harness
│   ├── csi
│   ├── display_link
│   ├── servo_bus
│   ├── led_local
│   ├── c2_local
│   └── yaw_service_loop
└── annotations                       master: show_annotations
    └── <same physical subgroups>
        └── <named part>
            ├── frame_xyz             triad at geometric centre; label X,Y,Z in the global frame
            └── dimensions            ΔX × ΔY × ΔZ from the generated bounding box
```

Fasteners stay one subgroup, not eighteen triads. Reserves stay with their parent physical part unless they are harness keep-outs.

### Physics overlays

Separate group, not baked into the PLA. Driven from the solved A0 datums and the mass tree so they cannot be placed by eye.

| Overlay | What to model | Caution |
|---|---|---|
| Origin triad | RGB at (0,0,0), ~20 mm legs | Layout origin, not a body datum |
| Roll / pitch / yaw axes | Distinct colours, finite cylinders through the current axis points, spanning the assembly | Move with their joints |
| CoM — roll, pitch, complete | Three spheres at the D/E mass-tree centres (R, RP, RPY) | Estimates until weighed; label which set |
| Gravity | Small −Z arrow at the complete CoM | Neutral pose only is enough |
| A0 residual | If axis and CoM still differ, a short dimension between them | After `--solve` this should be ~0 in the targeted coordinates |
| Camera FOV cone | ~102° horizontal cone from the Module 3 Wide through the crown hole | Inspection only; hit on the bezel means vignetting risk, not a certified FOV |

Do **not** put torque, RMS, modal frequency or storyboard numbers into solids. Those stay in `physics.md`. Overlays are geometry for inspection.

### Harness — trial routes, separate group

This is the hard part. Model it, but keep it obviously trial.

Follow [HEAD-CAD-04](decisions.md#head-cad-04--yaw-wiring) and the [harness study](../../../../01-system/head-harness-routing-study.md): partition by function; one mechanical flex zone per joint; external guided yaw loop beside a solid spindle; CSI is its own branch. First geometry is an H1-style continuous camera route with isolated yaw/pitch/roll flex zones. H2/H3 are fallbacks, not this model.

Rules:

- Centreline + a simplified jacket OD per branch. No invented connector SKUs, no claimed CSI impedance, no claimed bend radius or cycle life.
- Name clamp/guide solids. Treat the first 30–50 mm after a connector as straight until a real exit drawing exists.
- Assign each segment to R, P or Y so it poses with the joint it actually rides. The yaw loop is yaw-carried; CSI in the crown is rolling.
- Replace the existing M020 harness *allowances* with these solids’ mass later; do not add a second full cable mass.
- CAD-05 remains a yaw-plane demate **reserve**, not a chosen connector.
- Combined-motion checks: jacket vs mechanism pinch is a fail; jacket occupying empty cavity is not.
- If a branch cannot be routed without a guessed radius that would break CSI or the 60 mm neck, stop that branch at a labelled keep-out and record the gap. Do not draw a pretty cable through an impossible corner.

### Per-component frames and dimensions

Under **annotations**, each named physical part (not every fastener) gets:

1. A small triad at its geometric centre, with the **global** X, Y, Z of that centre in the head-layout frame.
2. The axis-aligned size ΔX × ΔY × ΔZ from the Layout 03 dimensions generator (same method as [Layout 02 dimensions](layout-02/dimensions.md)).

Generate those solids from the dimension script so they cannot drift from the log. If the viewer cannot do native dimension objects, labelled construction bars in this group are acceptable. Subgroup them with the physical components so one part can be isolated: hide everything, show `display_module` plus its `frame_xyz` and `dimensions`.

## Order of work

1. Use the Layout 02 [dimensions log](layout-02/dimensions.md) as the as-is map.
2. Feasibility of a layered/tapered head vs Layout 02 using the MVP3 visual; reject only if way worse, including if it hurts serviceability. Aesthetics after that call.
3. Choose visible yoke length (below Z=0) for stiffness, look-up and cable loop; do not drop A0.
4. Model Layout 03 physical geometry with the labelled occurrence tree above, including C2 tray, insert pockets, coupling, bearing seats and hard stops. No shroud. Keep the HEAD-CAD-01 service splits; do not trap modules.
5. Set camera–display board gap to 3 mm; report crown height.
6. Add physics overlays from the re-solved A0 and mass tree, including the camera FOV cone; **report vignetting**.
7. Route trial harness branches last, one function at a time, CSI first.
8. Emit annotations from the new dimensions generator; re-run the 56-pose grid including harness pinch pairs.

## Review output

When modelled: feasibility note on the layered/tapered shell (or a recorded reject); chosen yoke millimetres and why; front/side/rear/iso; a pitch-up pose that proves the knee; combined roll/pitch clearance **without** a shroud; FOV cone on/off with a **vignetting report**; harness on/off; C2 tray with rear-cover flashing access; one isolated component with XYZ and size; a short **service sequence** (what comes off, in what order, to reach display / camera / C2 / servos); revised envelope, mass tree, A0 and a Layout 03 dimensions log. No servo-SKU freeze, no cable-flex endurance claim, no optical lab certification.
