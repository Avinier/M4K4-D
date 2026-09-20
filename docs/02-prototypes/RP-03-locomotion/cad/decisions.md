# RP-03 CAD decisions

Recorded: **2026-09-20**. Scope: active body/chassis CAD iteration only.

This is the CAD-local decision register, following the RP-01 head CAD pattern. A
choice marked **fixed in CAD context** governs the active model and its generated
checks, but is not yet a permanent RP-03 architecture decision. Once the body and
chassis CAD is accepted, each retained choice must be propagated deliberately to
`decision.md`, `research.md`, operating constraints, controls and test documents.

## Decision register

| ID | Status | Choice |
|---|---|---|
| `RP03-CAD-01` | **Fixed in CAD context — pending permanent propagation** | Reduce the ground-reflectance architecture from three TCRT5000 channels to one guarded rear channel. Remove the front and lateral TCRT packages, mounts, booms and cable reserves from Layout 01. |
| `RP03-CAD-02` | **Fixed in CAD context — pending permanent propagation** | Remove the exposed stance-wide bumper. Replace it with a narrow concealed-contact fascia integrated into a lean fixed ball-transfer nose; preserve the frozen Concept A ball contact datum. |
| `RP03-CAD-03` | **Fixed in CAD context — pending permanent propagation** | Consolidate the rear skid and retained TCRT channel into one separately selectable, sharp-edged faceted rear-tail module with a hollow translucent shell, visible internal load/sensor paths, replaceable wear shoe and guards, and a flush top-loaded sensor cartridge. |

## RP03-CAD-01 — Rear-only ground-reflectance channel

M4's current intended work environment is a continuous, level indoor floor. Broad
cliff/edge detection is not a primary work function for this MVP, and three exposed
low-clearance sensor carriers add packaging, wiring, calibration and snag complexity.
The active CAD therefore retains only the rear look-down channel, where chassis
motion is least observable by the forward/head camera.

The retained rear channel remains on the skid-side carrier with its optical face
nominally 10 mm above the floor, protective rails beginning at 7 mm, and its sample
patch 27 mm behind the nominal skid contact. The replaceable skid pad begins at
3.5 mm and is therefore the first sacrificial rear contact. The selected breakout/comparator PCB,
connector, actual adjustment range and calibrated threshold remain open.

This choice intentionally removes any CAD or safety claim for dedicated forward or
lateral cliff detection. Camera perception may provide forward warning but is not
treated here as an independent low-level stop channel. Until permanent propagation
and testing, the implied operating constraints are:

- continuous, level indoor floors only;
- no autonomous operation near open stairs, platforms or loading edges;
- reverse travel kept slow and bounded;
- an unknown or failed rear-floor reading inhibits reverse motion;
- no claim of cliff protection during forward travel or pivoting.

Revisit this decision if M4's operating environment includes unguarded drops, if
unrestricted pivoting near edges becomes required, or if tests show the rear TCRT is
unreliable on the target dark/glossy floor set.

## RP03-CAD-03 — Faceted rear tail and sensor cartridge

The earlier rear design exposed a separate skid arm and seat, sensor boom,
adjustment ears, retainer and cable gland. Layout 01 now consolidates those functions
into an eleven-station ruled tail tied directly to the rear crossmember. Its side
silhouette is made only from straight links: it drops to the skid belly, rises
rearward through progressively shorter terminal links, and closes in a narrow distal
point. It deliberately uses no smooth spline,
matching Makad's sharp-edge visual language. Small exterior chamfers control edge
fragility while load relief remains internal. The visible shell uses the RP-01
Layout 03 ivory `#E3DDC9`, not a black or dark chassis finish. The shell is now
hollow and intrinsically translucent (alpha `0.34`), exposing a blue internal load
spine, yellow TCRT package, guide/shim stack, connector reserve and cyan cable route.
The complete tail is its own top-level `REAR_SKID_TCRT_MODULE` group, parallel to the
separate ball-transfer group, so it can be hidden or inspected without the chassis.

A chamfered replaceable wear shoe retains the nominal `X=-70 mm` skid datum and
3.5 mm ground clearance. Replaceable protective lips nest into the tail side walls,
begin at 7 mm, and protect the retained 10 mm optical face without becoming the first
floor-contact feature.

Layout 01.5 moves the rear TCRT from `X=-110 mm` to `X=-97 mm` and raises its optical
face from 8 mm to 10 mm. This reduces the sensing offset from 40 mm to a deliberately
bounded 27 mm, shortens the tail root-to-tip projection from 84 mm to 66 mm, and lets
the ruled links rise sooner rather than continuing as a long horizontal shank. The
10 mm sensing height is still provisional and requires target-floor calibration;
raising it further is not accepted without measured contrast-margin evidence.
It installs from above as a compact cartridge beneath a flush, chamfered service cap;
guides, height shim, connector clearance and the cable route are contained inside
the tail rather than represented as boxes or an external gland. This is a packaging decision;
the exact breakout, connector, shim stack and fastening details still require the
selected SKU to be measured.

## RP03-CAD-02 — Lean fixed ball nose with concealed contact

The exposed full-width bumper bar was behind the existing ball-transfer projection,
so it could not be the first point of frontal contact. It also added stance width and
an unresolved U-shaped visual element. Layout 01 therefore deletes that bar and both
outboard switches.

The frozen Concept A support geometry is unchanged: the 25.4 mm ball remains at the
`X=110 mm` ground-contact datum and its three-hole flange remains fixed rather than
interchangeable. The surrounding structure is narrowed to close-fitting rails, a
load-bearing collar with two keeper clips, and a compact shroud. The collar supports
the purchased flange from below and the keepers capture its top face, making the load
path into the front crossmember explicit. Vendor-internal rollers and individual
fasteners are suppressed in the layout so the purchased transfer reads as one SKU.

Near-contact protection is retained through a 42 mm-wide fascia integrated into the
ball nose. It has a nominal 3 mm compliant travel reserve, two concealed flexures and
one hidden microswitch. This is deliberately not a full-stance bumper: it protects and
senses the central ball-nose contact region but does not claim to detect every oblique
wheel-arch or body-corner impact. Flexure stiffness, switch force, over-travel stops,
debounce and impact qualification remain open engineering work.

## Propagation hold

Do not edit the permanent RP-03 documents merely because this geometry now exists.
When Layout 01 is accepted, propagate the retained choices and their consequences as
one reviewed change set: sensor/BOM count, GPIO allocation, electrical stop path,
motion restrictions, receiving/calibration tests and safety claims. Permanent RP-03
documents must replace the prior full-width bumper requirement only after that review.
