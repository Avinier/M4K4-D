# Head v1 fabrication and service audit

2026-10-05. **Status: not released for printing or assembly.** This is a
source and mesh audit of the current head v1, not a printed fit test. The
process screen assumes FDM/FFF; no printer, nozzle, material, layer height,
insert SKU, or screw supplier was specified. The default DfAM thresholds used
here are 1.2 mm supported wall, 1.6 mm unsupported wall, and 45 degrees from
horizontal for self-supporting down-facing faces. Machine-specific rules may
change the verdict.

## Mesh printability

Eight important authored parts were exported from the current `build_parts`
solids as STL (0.1 mm tessellation; the pitch frame was also re-exported at
0.01 mm), then measured with the installed DfAM tool. The purchased-part
proxies do not alter these authored shapes. This is a priority sample, not an
exhaustive screen of every printable detail or a slicer preview.

| Part | Mesh | Sampled wall p05 | Down-facing area below 45 degrees, assembled orientation | Finding |
|---|---:|---:|---:|---|
| Front bezel and camera crown | watertight | 0.950 mm | 2,442 mm² | Below the 1.2 mm default; 90° about +Y reduces flagged area to 229 mm² but puts the visible face toward the bed. |
| Main octagonal skin | watertight | 1.115 mm | 13,050 mm² | Below the 1.2 mm default; standing on either end reduces flagged area to 667–702 mm². Check the contact edge and crown support in the slicer. |
| Rear cover | watertight | 1.600 mm | 212 mm² | Broad wall passes the supported-wall screen; local sampled minimum 0.600 mm near a detail warrants a section check. |
| Outer ear cap, +Y (revised) | watertight | 1.564 mm | Support orientation pending | Two upper screw bosses; inspect sliced cap and supports. |
| Inner ear mount, +Y (revised) | watertight | 1.790 mm | Support orientation pending | The 2 mm radial ring, 1.8 mm annular web, and two stepped receiver feet exceed the default unsupported-wall threshold at p05. |
| Ear amber ring and dark centre, +Y (revised) | watertight | 1.200 mm each | 0 mm² laid flat | Actual 1.2 mm print parts with a 0.1 mm adhesive bed. |
| Pitch frame and roll-servo saddle | **nonmanifold STL** | 2.600 mm | 3,693 mm² | One edge has four incident triangles at approximately X -51.12, Y -51…-46, Z 45.09 mm. A 0.01 mm export has the same defect. The CAD B-rep reports one valid solid, but the exact exported mesh is not watertight. |
| Yaw yoke leg, +Y | watertight | 1.400 mm | 130 mm² | Structural web is thicker; printing flat on the plain face reduces flagged area to 5.7 mm². Small accent features still need a slicer check. |
| Yaw turntable disc | watertight | 1.997 mm | 11,001 mm² | Flipping it reduces flagged area to 198 mm²; bearing/gear mating faces and groove quality need review. |

The pitch-frame defect is explained by `details.py`: the hard-stop pin is
radius 1 mm, centred at `PITCH_X-10`, while its lug begins at `PITCH_X-11`.
The bore is exactly tangent to the lug's outer X face and leaves zero wall.
Extend the lug or move the pin enough to leave a real printable ligament,
then re-export and rerun the motion, stop, and DfAM checks. The lower sampled
wall minima elsewhere may include edge/ray artefacts; the fifth-percentile
values are the stronger warning signal.

The revised ear parts were also exported separately at 0.05 mm tessellation,
both sides. All eight meshes were watertight single bodies. The -Y/+Y cap
sampled wall p05 was 1.587/1.564 mm; the inner mounts were 1.800/1.790 mm.
Local minimum samples near screw holes and curved edges are much thinner,
so inspect the actual sliced toolpaths. The old 1.200 mm cap and 0.999 mm
inner mount figures are superseded.
The two cap screws sit on the upper arc because lower screw
heads contacted the yaw yoke at the roll stops. The trim stack was shortened
from 4 to 2.5 mm for the same reason, reducing estimated capacity to 5.46 g
per ear. The updated mass solve and head motion envelope were regenerated.

## Screws and inserts

- **Modeled and nominally aligned:** six front M2 × 10 screws, four rear M2 × 6,
  two cap screws and two hidden mount screws per ear, plus a central trim
  retainer per ear, camera and C2 tray screws,
  roll bearing end-plate screws, and three head-disc M3 × 6 screws. The
  head/body integration check gives 3.8 mm nominal engagement into the
  body-side M3 × 4 hub inserts. The 56-pose check includes modeled fasteners
  in its cross-frame collision grid and checks front/rear insert mouths.
- **Not specified enough for fabrication:** front/rear and other M2 insert
  pockets are nominal Ø3.2 × 3 mm, with no purchased insert SKU or printed
  heat-set fit trial. Screw length, bottoming, thread engagement, boss
  pull-out, and torque have not been checked against real hardware. The
  same-frame overlap check intentionally excludes screw/thread contact.
- **Incomplete:** the four vertical bearing-cartridge fixing bores and two
  roll-servo strap holes have no corresponding modeled screws. The pitch
  servo-to-yoke adapter is explicitly a trial solid with no final XC330
  mounting-hole pattern or proven driver access. Display retention hardware
  and the precise spindle/horn fastening are not released. The pitch stop
  pin lug has the zero-wall defect above.

## Assembly and removal

The service architecture is reasonable but **not yet demonstrated as easy**.
With the rear cover's four screws removed, the modeled C2 tray can be
unplugged, unfastened with two screws, lifted 27 mm, and withdrawn rearward.
The camera bracket can be removed after the six-screw front carrier is off.
Each ear now has two cap screws, two hidden inner-mount screws, and a trim
retainer. The cap and its bonded finish withdraw outboard first; the two
hidden screws then expose a straight outboard inner-mount path. Both paths
pass `cad/generated/ear-service.json` at neutral without modeled interference.
The lower cap arc is held by the stiffness of the continuous cap shell; its
pry resistance and screw boss life need a print trial.

`check_revision.py` verifies the C2 path and camera movement relative to the
removed carrier. It does not prove a complete front-carrier or rear-cover
withdrawal with installed harnesses, screwdriver swept volumes, hand room,
or repeated snap/insert service life. Roll-servo access uses both front and
rear openings and coupling release. The body yaw cartridge requires the
tilting assembly and three disc screws to come off before it can be removed.
This is serviceable in a planned sequence, but not a quick field swap.

## Release work, in order

1. Give the pitch stop-pin lug a real wall; re-export a watertight frame STL
   and rerun the head motion and stop checks.
2. Thicken or redesign the front and main-skin thin regions;
   section the local minima and rerun DfAM on *every* printable part.
3. Choose a printer/material/orientation for each part and inspect sliced
   layers and supports, especially the crown, inside shell, ears, and disc.
4. Select actual inserts and screws, model the missing retention hardware,
   check engagement/bottoming and driver paths, then print fit/torque coupons.
5. Perform one complete assembly and reverse disassembly with the real
   display, camera, servos, bearings, and cable harness; record time and any
   required force or inaccessible screw.

Existing CAD checks prove nominal geometry and sampled access only. They do
not establish process-specific printability, loaded strength, thermal insert
retention, or repeatable service.
