# Head v1 fabrication and service audit

**Status: CAD blockers closed; not yet released for printing.** The geometry
defects found on 2026-10-05 are fixed in source and re-measured
(2026-10-07, below). Release now waits on process choice, slicing, fit
coupons and one real assembly, none of which CAD can close.

The process screen assumes FDM/FFF. No printer, nozzle, material or layer
height is chosen. Default DfAM thresholds: 1.2 mm supported wall, 1.6 mm
unsupported wall, 45° from horizontal for self-supporting down-facing faces.
Machine-specific rules may change the verdict.

## What changed (2026-10-07)

The 2026-10-05 audit sampled eight parts at 2,000 rays. Re-screening **all
27 printed parts** at 20,000 rays found more than it reported:

| Finding | Was | Fix |
|---|---|---|
| Pitch stop-pin lug | Ø2 bore tangent to the lug face; non-manifold STL | Lug extended; 2 mm ligament round the pin |
| Main skin | p05 0.80 mm: recessed stern lands 0.80, tapered rear facets 1.12–1.16 | 1.3 mm section inset (≥ 1.2 normal on the taper); 0.5 mm doubler behind the lands |
| Front bezel | p05 0.95 mm: window lip 0.95, sloped band 1.04–1.17, board-corner clearance left 0.78 at the lower chamfer | Lip 1.3 (glass 0.35 mm further back); band and crown offset 1.3 along their normals; front chamfer 9.5 (was 10); clearance corner follows the board's measured corner |
| Crown rear CSI opening | ±18 box notched the sloped crown sides to 0.45 mm and the roof to 1.0 | Opening follows the crown cavity |
| Front side screws | Counterbores 0.5 mm from the bezel side; pads 1.15 round the bore | Window glass **106 mm** wide (was 110); side screws at \|Y\| 56.4; pads R2.5 |
| Camera crown receivers | 0.6 mm round the Ø3.2 insert | Moved to Y ±16, R2.8 (1.2 mm wall, 0.7 mm to the camera PCB) |
| Camera bracket | Channel lips 0.10 / 0.15 mm thick; boss 1.05 round the bore | Lips 1.35–2.0 mm, cap 1.34, boss R2.4 |
| C2 tray | Jaws 0.85 mm; USB notch left a 0.3 mm sliver of front wall | Jaws 1.25; notch cut through |
| Roll-servo strap | Posts left 0.55 mm round the bore; frame insert pockets broke out of the 2.6 mm saddle walls; no screws | Redesigned (below) |
| Roll-bearing retainers | 0.8 mm plates; insert pockets at R9 broke 0.15 mm into the Ø15.1 bearing seats | 1.2 mm plates; inserts at R10.5 on the lower diagonals, 1.35 mm from the seats |
| Hidden ear-mount screws | Heads seated on a 0.4 mm web floor; counterbores left crescent slivers | 1.2 mm seat boss; counterbore closed inboard, open outboard |

### Mesh printability (re-measured)

All authored parts were exported from `build_parts` at 0.05 mm
tessellation and measured with `dfam_tool.py` (20,000 samples per part).
All 27 are **watertight single bodies**, including the pitch frame.

| Part | Wall p05 (was) | Note |
|---|---:|---|
| Front bezel and camera crown | 1.30 (0.95) | Remaining low samples are the 39° camera-aperture chamfer edge and ray artefacts at the band's back edge |
| Main octagonal skin | 1.21 (0.80) | Local samples at the open rear edge, land steps and motion-relief cut edges are edge artefacts |
| Pitch frame and roll-servo saddle | 2.60, watertight (non-manifold) | |
| Bearing cartridge | 1.82 (1.37) | |
| Ear inner mount ±Y | 1.40 (1.80) | Lower p05 is the new 1.2 mm seat boss and open counterbore slot |
| Ear cap ±Y, rear cover, yoke legs, disc | unchanged | 1.57–2.0 |
| Camera bracket | 1.99 (1.05) | |
| C2 tray | 1.20 (0.85) | |
| Roll-servo strap | 1.33 (0.63) | |
| Roll-bearing retainers | 1.20 (0.80, not screened before) | |
| Pitch-servo adapter, inlays, ear colour parts | 1.20 | 1.2 mm design thickness |

Down-facing (support) areas were not re-measured; the 2026-10-05 orientation
figures still apply to the unchanged parts. Choose orientations in the
slicer.

## Screws and inserts

**Insert article.** Every printed M2 receiver takes one article: **M2 × 3
brass heat-set, OD 3.6, in a Ø3.2 pilot at least 3.5 mm deep** (CNC Kitchen /
Purecrea class: vendor hole Ø3.2, min depth 3.5). The usual supplier's
OnlyScrews M2 × 3 insert is **OD 3.9** and does not suit this pilot; it would
need about a Ø3.5 pilot and thinner walls. No supplier is selected yet.

**Fastener-stack check.** `cad/check_fasteners.py` samples each modeled M2
screw from head seat to tip against the printed parts and purchased
references. It **passes for all 50 screws**: no shank cuts plastic, every
insert joint has 2.6–3.0 mm of shank in the insert, and no pocket is
shallower than the insert. Servo screws have 3.0 mm in the tapped holes.
Before the fixes, 26 of 30 screws failed:
- Tips ran 0.4–2.2 mm past the insert into solid plastic.
- The ear-cap screws had no insert at all (4.2 mm into a Ø1.6 pilot).
- The front and rear pockets were only 2.6 mm deep in plastic.

| Joint | Screw | Thread |
|---|---|---|
| Front carrier (6) | ISO 7380-style M2 × 8 | Insert at the front of a skin boss that runs forward to the bezel pad (X −5); the pad clamps on it |
| Rear cover (4) | M2 × 6 | Insert 3.0, tip in relief |
| Ear cap (2 per ear) | M2 × 6 | New inserts in the receivers |
| Ear inner mount (2 per ear) | M2 × 4 | Inserts in the cradle pads |
| Ear trim (1 per ear) | M2 × 5 (was × 6) | 2.5 mm; stack always built to 2.5 mm with spacers |
| Camera bracket (2), C2 tray (2) | M2 × 6 | Inserts |
| Roll-bearing retainers (4) | M2 × 4 | Inserts at R10.5, lower diagonals |
| Bearing cartridge (4), **new** | ISO 4762 M2 × 25 | Head in a 2 mm spot face; insert in the pitch-frame slab, widened to ±13 |
| Roll-servo strap (2), **new** | ISO 4762 M2 × 25 | Strap at X −94 clears the servo-bus exit; inserts in frame bosses |
| Roll-servo case (2) | M2 | XC330 tapped holes |
| Pitch servo (4), **new** | M2 × 6 | XC330 inboard-face tapped holes (from the vendor STEP) through a 3 mm adapter face plate |

The head-to-body M3 × 6 joint is unchanged (3.8 mm engagement,
`check_integration.py`).

**Still open:**
- **Pitch adapter to yoke leg.** The adapter now carries the servo on its
  real hole pattern, but it only rests on the +Y yoke leg with no fastener.
  There is no room for a vertical insert above the leg's pitch-bearing bore.
  Print adapter and leg as one part, or redesign the joint.
- **Display retention** and the precise spindle/horn fastening are not
  released.
- **Physical checks.** Insert fit, pull-out and torque need coupons in the
  chosen material. Screw lengths are nominal, with no tolerance stack.

## Assembly and removal

Unchanged in principle. With the rear cover's four screws removed, the C2
tray unplugs, unscrews (two screws), lifts 27 mm and withdraws rearward. The
camera bracket comes off after the six-screw front carrier. Each ear cap
withdraws outboard after two screws; the inner mount after two more. All
pass at neutral (`revision-checks.json`, `generated/ear-service.json`).

New hardware sets some order:
- **Bearing cartridge screws** drive vertically from above, so they go in
  during frame sub-assembly, before the cradle and skin. Removing the
  cartridge is a teardown, not a service step.
- **Strap screws** are vertical at X −94. From the rear opening only a short
  1.5 mm L-key reaches them (about 24 mm above the strap). This is unproven.
- **Pitch-servo screws** are on the servo's inboard face, so they go in
  before the servo and adapter are mounted.

None of this has been tried with real wiring, tools and parts. Treat it as
*planned* service access.

## Mass

The estimated head (R+P+Y) rises from 594.0 to **604.3 g** (thicker walls,
new bosses and hardware). The CoM moves ≤ 0.16 mm from the A0 axes.
`axes.json` and `mass-placement.json` are **not** regenerated: body v1 reads
both, and re-solving A0 would move the body interface. Refresh them
deliberately, with the body owner, when the head is weighed. The mass model
counts hidden screws only as a fixed allowance. The pitch frame's new
hardware (six M2 × 25 and four M2 × 4, roughly 5–6 g of steel) exceeds its
3 g allowance, so the frame is about 3 g light in the estimate.

## Release work, in order

1. ~~Pitch stop-pin lug~~, ~~thin shell regions~~, ~~missing fastener
   models~~: done in CAD (above).
2. Confirm the **106 mm window** with the glass/acrylic supplier (M003).
3. Choose printer, material and orientation per part. Slice and inspect the
   crown, shell interior, ears and disc; check the camera-aperture chamfer
   edge and the 1.2 mm ear colour parts in the slicer.
4. Buy the M2 × 3 × 3.6 insert and the screw set. Print an insert coupon
   (Ø3.2 × 3.5 pocket in a 1.2 mm wall boss) for fit, pull-out and strip
   torque.
5. Fasten the pitch adapter to the yoke (or merge them).
6. One complete assembly and reverse disassembly with the real display,
   camera, servos, bearings and harness. Record time, force and any screw a
   tool cannot reach.

The CAD checks prove nominal geometry and sampled access only. They do not
establish process-specific printability, loaded strength, insert retention
or repeatable service.
