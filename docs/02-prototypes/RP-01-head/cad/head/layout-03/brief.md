# Layout 03 construction brief

Revision of Layout 02 source, preserved in its own directory. Millimetres; origin front/bottom centre, +X face, +Y left, +Z up. Catalog camera and XC330 files reused at scale 1; display and C2 positions unchanged. Same text-to-cad 0.4.28 runtime and explicit R/P/Y transforms.

## Feasibility decision before detailing

Helmet refinement requested after reviewing the first Layout 03: the previous 122 mm rear width was a conservative choice, not a proven maximum. Test 104 mm rear width (Z10…84), retaining the 130 mm ear mounting belt to X−78. Upper shoulder chamfers deepen from 14 to 24 mm between X−26 and X−60, leaving the face/display/cradle pocket and ear attachment belt unchanged. Rear upper chamfer returns to 10 mm so the roof and C2 extraction corridor remain useful. All faces remain planar; no smooth hull or extra shell. Move the four rear M2 lands to Y±44 at Z26/65 with their matching receivers and insert pockets. Recheck rear servo, combined motion, shell connectivity, C2 lift/extraction, mass/A0 and optics. Keep the 104 mm camera crown and 32 mm yoke. The preceding source and evidence are preserved in review/pre-helmet-source-and-evidence.zip; earlier snapshots provide the before view.

Retain the 32 mm visible yoke segment and rearward knee: the original look-up clearance and external yaw-loop allocation are valuable, while shortening without a cable SKU would consume useful free space. Do not change the pitch axis for styling; recompute it only from the revised mass tree. Yaw interface remains Z−60.

## Detail targets

Camera PCB bottom Z77 gives 3 mm above the fixed display top Z74. Crown top Z104 allows the camera/bracket and roof: +2 mm versus Layout 02 and a 304 mm provisional 140+60+104 stack. Preserve board and servo dimensions.

Trial M2 insert pockets: 3.2 mm diameter, 3 mm depth, visible M2 retained; exact insert SKU/thermal fit unselected. Internal removable joints use explicit screw clearance and insert seats. Bearing pair remains Ø16 × 6 at X−43/−65, 22 spacing, with stepped seats, shoulders and removable end retention. Coupling retains 6 mm shaft bore with radial fastening. Geometric pitch −22/+40 and roll ±18 hard-stop slots act independently of software.

C2 rear-removable tray, upper USB installed plug and withdrawal corridors, BOOT/RESET access; camera, servo mounts, bearing cartridge independently removable. No shroud. Optical overlay uses 102° horizontal field with conservative corner coverage and a stated pupil assumption; check actual plastic intersections.

Separate physical, physics, harness, annotations occurrence groups. Pose switches act by named frame groups. Dimensions and triads share one measurement function. Physical/physics/harness on, annotations off. Trial branch diameters and straight exits are geometric assumptions; unresolved joint bends stop at named keep-outs. Existing M006/M020 mass allowances remain single-counted until cable SKUs are weighed.

## Validation

Neutral all-part checks; independent 56-pose grid including new mechanisms and jacket pinch pairs; explicit hard-stop contact/overtravel checks; optical cone versus bezel/mask/window at neutral and combined extrema; A0 re-solve and Layout 02 mass/inertia comparison; exported solid/closed topology checks; front/side/rear/iso, pitch-up, combined motion, overlays on/off, tray access and isolated annotated component snapshots. No servo freeze, optical certification, cable endurance, print release or scored-gate claim.
