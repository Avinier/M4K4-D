# Rear keel — parts, printing, assembly and service

The rear keel of [chassis v1](../README.md): the faceted keel under the rear crossmember, its
replaceable wear shoe, the TCRT bezel with its guard lips and the height shims, and every joint
they carry. This page reviews the keel for printing, together with the [nose](../nose/README.md),
the same way as the [frame](../frame/README.md) (2026-10-31). The CAD review and its checks are recorded below (2026-11-01).

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py)
  (`rear_skid_tcrt_keel()`, `rear_crossmember_inserts()`, `frame_crossmember("REAR")`). The design
  is [D-014](../../../03-build/decisions.md#d-014) (keel, J09, J10), [D-016](../../../03-build/decisions.md#d-016)
  (the soldered TCRT lead) and [D-017](../../../03-build/decisions.md#d-017) (PETG wear parts). Fixes
  from this review go in as droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py).
- **Joints:** the [joint register](../../../03-build/01-chassis/v1/joint-register.md) (J09A, J09B, J10A, J10B).
- **View:** [`nose-keel.step.py`](../../../03-build/final/v1/cad/nose-keel.step.py),
  shared with the nose. Two copies, **1 assembled** and **2 exploded** (150 mm to −Y): the keel
  drops 40 mm off the crossmember, its screws, the TCRT, shims, bezel and bezel screw come out
  below it, the shoe slides forward and its screw out to +Y. Each joint is its own group. The
  four keel prints are solid colours (keel and bezel taupe, shoe and shims slate); bought parts
  and the rear module (already reviewed) are pale.

Coordinates are the chassis frame: origin on the floor under the axle line, +X forward, +Y
robot-left, +Z up. The crossmember underside, the keel's seat, is Z 34.

## 1. Print units

| Print | BOM | Size (X × Y × Z) | Volume | Material, colour | Joins to |
|---|---|---|---|---|---|
| **Keel** `REAR_KEEL_FACETED_BODY` | CH-008 | 50 × 19 × 28 mm (X −67 to −17, Z 6–34) | 14.47 cm³ | PETG, taupe | Rear crossmember (J09A), bezel (J09B), shoe (J10A) |
| **Wear shoe** `REAR_KEEL_REPLACEABLE_WEAR_SHOE` | CH-009 | 12 × 10 × 6 mm (X −33 to −21, Z 3.5–9.5) | 0.46 cm³ | PETG, deep slate | Keel (J10A) |
| **TCRT bezel** `REAR_TCRT_BEZEL_WITH_GUARDS` | CH-010 | 14 × 15 × 9 mm with its pin (X −61.5 to −47.5, Z 7–16) | 0.38 cm³ | PETG, taupe | Keel through the shims (J09B); carries the guard lips (J10B) |
| **Height shims** `REAR_TCRT_HEIGHT_SHIM_*` | CH-068 | 14 × 15 × 1.2 mm each | 0.14 cm³ each | PETG, deep slate | Between bezel and keel belly (J09B); two fitted, four printed |

The keel is the rear floor-contact part: the shoe takes the skid when the robot tips back, and
the TCRT looks down through the keel's sensor flat for cliffs and edges.

### 1.1 Keel, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Seat (top face) | Z 34, X −48 to −32, the crossmember underside | J09A |
| Screw bores, 4 | Ø3.4 at (−36.5, ±5.5) and (−44, ±5.5); Ø6.5 counterbores from below to Z 9.5 (front pair) and Z 12 (rear pair) | J09A M3 × 30 socket heads |
| Shoe belly | Z 6, X −21 to −38 | The shoe sits under it (J10A) |
| Dovetail groove | X −32.15 to −13, open at the front where the belly rises; 4.3 → 6.3 mm wide, 3.65 deep (D-077) | J10A shoe tongue |
| Shoe screw holes | From the +Y side at (−27, Z 7.25): Ø2.2 clearance Y 0–5.3, Ø3.8 head counterbore Y 5.3 out | J10A M2 × 6 |
| Sensor flat | Belly Z 12.4 (D-077), X −46 to −62, half-width 9.5 | Bezel and shims seat on it (J09B) |
| Cradle pockets (D-077) | End reliefs round X −59.8..−58.5 and −49.5..−48.2, with 0.1 mm clearance, through Z 16.5 | Clear the contoured case supports even at zero shims |
| TCRT pocket | 10.8 × 7.6 mm about (−54, 0), open below the belly and up through the keel top | The TCRT drops out below; its lead rises through the top |
| Bezel pilot | Ø1.6 at (−54, −5.6), Z 11–21.9 (D-077) | J09B M2 × 10 thread-forming |
| Pin hole | Ø2.0 at (−54, +5.6), Z 11–19.4 (D-077) | The bezel's Ø1.8 moulded pin |

### 1.2 Wear shoe, bezel and shims

- **Shoe:** a 12 × 10 × 2.5 mm octagonal sole (2.5 mm corner chamfers), X −33 to −21, Z 3.5–6.
  On top, a dovetail tongue 4 mm wide at the root and 6 mm at the top, 3.5 mm tall (Z 6–9.5; upper 1 mm straight-sided, D-077), X
  −32 to −21. A Ø1.6 pilot crosses the tongue at Z 7.25 for the M2 × 6.
- **Bezel:** a 1.5 mm plate (Z 8.5–10), X −61.5 to −47.5, Y ±7.5, with a 9 × 7.6 mm optical window. D-077 adds contoured end cradles rising to Z 14
  over the original flat end ledges, to support the actual rounded vendor case at its existing pose. Two guard lips under it (J10B), 2.5 mm wide at Y
  ±5.6, X −61.5 to −49, down to Z 7. A Ø1.8 pin rises 6 mm at (−54, +5.6). At (−54, −5.6) a
  Ø2.2 screw hole, with a Ø3.8 head recess through the lip.
- **Shims:** the bezel's outline, 1.2 mm thick (D-077), with the 11.8 × 7.6 mm cradle-clearance window and two Ø2.2 holes. The
  optical face sits on the bezel at Z 12.4 − total shim thickness: two give Z 10.

## 2. Joints

| Joint | What holds what | Hardware | Driven from | Register |
|---|---|---|---|---|
| **J09A** | Keel seat to the crossmember underside; skid loads go through the screws into the crossmember and both rails | 4 × ISO 4762 M3 × 30 (CH-034) into 4 × M3 × 6 inserts in the crossmember (CH-067) | Below, keel, shoe and bezel fitted | [J09A](../../../03-build/01-chassis/v1/joint-register.md#j09a--rear-keel-to-rear-crossmember) |
| **J09B** | TCRT face down on contoured bezel cradles; bezel and shims to the keel belly; height = Z 12.4 − total shim thickness | 1 × M2 × 10 thread-forming (CH-069) and the moulded pin; shims (CH-068) | Below, keel on | [J09B](../../../03-build/01-chassis/v1/joint-register.md#j09b--rear-tcrt-cartridge-to-keel) |
| **J10A** | Shoe tongue in the keel groove, stopped by the groove end, held by a screw across the tongue | 1 × M2 × 6 thread-forming (CH-070): clearance in the keel, thread in the shoe | +Y side, then the shoe slides out forward | [J10A](../../../03-build/01-chassis/v1/joint-register.md#j10a--wear-shoe-to-keel) |
| **J10B** | Guard lips, part of the bezel, 3 mm below the optical face at any shim count | As J09B | As J09B | [J10B](../../../03-build/01-chassis/v1/joint-register.md#j10b--tcrt-guards-to-keel) |

The rear module also carries the J10-10 tie lug (X −51 to −48, Y −33 to −27) on the
crossmember's rear face: one zip tie (CH-072) holds the TCRT lead at the foot of its riser.

## 3. Hardware going into the keel prints

| Item | BOM | Qty | Hole in the print | State |
|---|---|---|---|---|
| M3 × 6 slant-knurled insert, OD 4.4 (OnlyScrews), in the CNC Kitchen M3 × 5.7 positions | CH-067 | 4 | Ø4.0 from the crossmember underside | In hand (the CH-061 stock) |
| ISO 4762 M3 × 30 socket head | CH-034 | 4 | Ø3.4, Ø6.5 counterbores | |
| M2 × 10 pan thread-forming | CH-069 | 1 | Ø1.6 pilot in the keel; Ø2.2 in bezel and shims | Candidate (JCPlas B4B66) |
| M2 × 6 pan thread-forming | CH-070 | 1 | Ø1.6 pilot in the shoe; Ø2.2 in the keel | Candidate (JCPlas B4B66) |
| Zip tie, 2.5 mm | CH-072 | 1 | Lug slot on the rear module | |


## 4. Issues going in and what was done (D-077)

The final-tree checks are `check_nose_keel_print.py` and `check_nose_keel_assembly.py`.
All CAD changes are droid edits in `final/v1`, leaving subsystem sources unchanged.

| Issue | Outcome |
|---|---|
| Four CNC Kitchen M3 × 5.7 inserts unbought | In-hand OnlyScrews M3 × 6, OD 4.4; retain Ø4 pilots, deepen 6.5 → 7 mm (insert plus 1 mm). Least wall beyond knurl 1.75 mm |
| 1 mm shims under lab's preferred 1.2 mm minimum | Builder approved 1.2 mm shims and a 0.4 mm recess in the keel's sensor flat. Two still give optical face Z 10 and lips Z 7 |
| Bezel screw would bottom at zero shims | Ø1.6 pilot to Z 21.9, 1 mm beyond tip; locating-pin hole to Z 19.4, 1 mm beyond pin at zero shims |
| Shoe M2 pilot had 0.45 mm of plastic above it | Tongue top and groove 1 mm taller; 1.45 mm remains above the Ø1.6 pilot. Screw axis, floor height and hardware unchanged |
| Thin wall from bezel thread toward sensor pocket | 0.75 mm past the M2 thread. Keep; snug only and qualify with the candidate screw, checking the sensor still drops freely |
| The actual vendor case floats above the flat end ledges | Case-contoured end cradles, with clearance in the shims and keel, hold the sensor within 0.05 mm at its unchanged modeled position; old bezel permits 0.2 mm drop with no contact |
| Extra shims undermine shoe-first floor contact | Nominal two-shim stack retains the D-014 order. Three/four shims are restricted experimental settings, not cleared for normal running |
| M2 thread-formers remain candidates | CH-069/070 require actual head, pilot and repeated-service qualification; a machine screw is not an approved substitute |

## 5. Printing (D-078)

Same six-direction triangle survey and bridge/ledge rules as the nose page §5. Numbers are
surface areas, not slicer support volume. Check the lab's actual slice before printing.

| Print | Face on the bed | Bed | Support area | Faces that must come out clean |
|---|---|---|---|---|
| Keel | **Crossmember seat, +Z** | 196 mm² | 312 mm² | Flat crossmember seat; four counterbores; shoe groove; sensor pocket; recessed bezel flat; screw/pin holes |
| Shoe | **Sole, −Z** | 108 mm² | None | Dovetail flanks and extended tongue top; Ø1.6 pilot; flat sole |
| Bezel/guards | **Guard lips, −Z**, as fitted | 54 mm² | 26 mm² | Contoured case seats; shim seat; locating pin; screw head recess |
| Shims | **Flat, ±Z** | 113 mm² each | None | Both faces parallel, thickness 1.2 ±0.05 mm; window and holes open |

All four types are PETG on the A1; keel and bezel taupe, shoe and shims deep slate. Add a brim
on the keel and bezel if needed, kept outside their fit faces. The keel's groove and pocket
are accessible for support removal from below/front; inspect the whole groove after cleanup.
Keep the crossmember seat flat and remove elephant's foot at the four bore mouths. The shoe's
threads run across its layers, so drive the thread-former gently. Print four identical shims,
fit two initially; the additional two do not authorize the lower sensor setting for running.

Keel seat-down uses the 196 mm² planar mounting face as its bed and prints the sensor/shim
flat upward. Bottom-down has 129 mm² bed and only 144 mm² support: the chosen orientation trades
support for the larger mounting-bed face and controlled critical surfaces. Side-down needs
676 mm² support. The shoe's sole-down bed is larger than its tongue-down bed. A bezel Y-end
orientation reduces support to 7 mm² but has only 21 mm² bed; lips-down gives 54 mm² and keeps
the case seats facing upward and the locating pin vertical.

**Six-direction survey, final geometry (bed / support, mm²).** Direction is toward the bed.

| Print | −Z | +Z | −X | +X | −Y | +Y |
|---|---|---|---|---|---|---|
| Keel | 128.5 / 144 | 195.6 / 312 | 34.7 / 332 | 54.7 / 176 | 204.4 / 676 | 204.4 / 676 |
| Shoe | 107.5 / 0 | 66.0 / 0 | 12.5 / 6 | 31.0 / 0 | 17.5 / 38 | 17.5 / 38 |
| Bezel | 53.7 / 26 | 2.5 / 84 | 30.0 / 44 | 22.5 / 41 | 21.0 / 7 | 21.0 / 7 |
| Shim | 112.7 / 0 | 112.7 / 0 | 18.0 / 0 | 18.0 / 0 | 16.8 / 0 | 16.8 / 0 |

## 6. Assembly and service (D-079)

The check models the body fitted and wheels on, with each removed component stated explicitly.
The 2.5 mm key uses a radius 1.443 mm across corners; PH0 uses a Ø3 shaft. A Ø6 iron envelope
reaches the crossmember insert mouths with the loose rear module on the bench. Flexible cable
routing, tool handles and hands still need a physical dry run.

**Tools:** straight 2.5 mm hex key; PH0 (confirm against CH-069/070 samples); M3 insert iron;
flat plate; torque driver to 0.3 N·m; cutters and a replacement 2.5 mm zip tie for TCRT service.

| Screw | Torque | Basis, as D-076 |
|---|---|---|
| J09A keel, M3 × 30 socket | 0.3 N·m | About 500 N at nut factor 0.2, about 35 MPa under a Ø5.5 head around a Ø3.4 bore, below the review's approximately 50 MPa PETG yield assumption |
| J09B bezel, M2 × 10 thread-forming | Snug only | Stop when the bezel and stack seat, without crushing the cradles or splitting the 0.75 mm pocket wall |
| J10A shoe, M2 × 6 thread-forming | Snug only | Stop when the retaining screw seats; do not split the dovetail tongue |

### On the bench, before the body

1. Clean the keel supports, check the crossmember seat flat and dry-slide the shoe to its stop.
2. With the rear module loose, melt four M3 × 6 inserts **up from below** into its Ø4 × 7 mm
   pilots, flush with Z 34. The module prints deck-down, so these pilots open upward in its
   print orientation. The iron reaches with the keel off.
3. Offer the keel up against the crossmember. Drive four M3 × 30 from below using the 2.5 mm
   key, diagonally to 0.3 N·m. The front pair engage 5.5 mm, the rear pair the full 6 mm; tip
   relief remains above both. Do not use the screws to pull a warped mounting face flat.
4. Slide the shoe in from the front to the groove end; drive CH-070 from +Y, snug.
5. Feed the soldered TCRT lead up through the pocket, seat the TCRT in the bezel's contoured end cradles,
   then put **two 1.2 mm shims** above the bezel. Lift this stack onto the recessed flat,
   locating pin in its hole. Drive CH-069 from below, snug. Face Z 10, guard lips Z 7.
6. Route the cable with its 30 mm slack loop, restrain it at the crossmember lug with CH-072,
   and connect J10-10 at PCB-10. Check no load reaches the sensor's soldered legs.

### Service, body fitted

| To do | Sequence | Access |
|---|---|---|
| Wear shoe | CH-070 out from +Y; slide shoe forward 15 mm out of the groove | PH0 shaft path checked with wheels on; retained screw is a planted blocker |
| Bezel/shims | CH-069 out; lower bezel and shims 30 mm | PH0 from below; keel remains fitted |
| TCRT | Bezel/shims off; rear service panel off; unplug J10-10 and cut the crossmember tie; release slack and draw sensor/lead down through the pocket | Lead is continuous to PCB-10; do not pull against the tie or plug. Bezel is a planted blocker |
| Keel | TCRT and lead out first; four M3 × 30 out; keel and shoe down 40 mm through the shell slot | 2.5 mm key from below with shoe/bezel fitted; screw retained is a planted blocker |

**Shim limits.** Optical height is `12.4 − 1.2 × count` mm. Counts 0/1/2 give 12.4/11.2/10 mm.
Counts 3/4 give 8.8/7.6 mm, but the lowered lips hit the floor before the shoe on tip-back.
At the nominal stack the shoe contacts at 6.05°, guards at 6.49°, keel at 8.97° and sensor at
10.43°. Keep two shims until real-floor optical and snag tests justify a different stack.
The 0.44° nominal shoe/guard margin must be verified with loaded tyre radius and real floors.
Z 10 is the existing CAD datum at the lowest projecting feature of the vendor STEP, not proof
that the whole case has a flat underside there. The new cradles seat on its curved case; check
the actual optical standoff and the received package on the first cartridge.

## 7. Gap table

| Gap | Fix or disposition | Decision | Check |
|---|---|---|---|
| Rear insert bores too short for insert + 1 mm | Ø4 × 7 mm pilots; replacement M3 × 6 models | D-077 | print: four pilots, walls and engagement; raw geometry planted |
| Shims below lab minimum | 1.2 mm plus flat recessed 0.4 mm, nominal sensor position retained | D-077 | print: thickness, flat, optical stack and contact order |
| Bezel screw/pin bottoming at zero shims | Pilot/hole extended 1 mm beyond each tip | D-077 | print: depths; raw pilot planted |
| Thin shoe tongue above pilot | Tongue and groove +1 mm; roof 1.45 mm | D-077 | print: pilot roof/groove; raw shoe planted |
| Vendor case not supported at the declared datum | Contoured end cradles; shim windows widened; keel pockets clear all shim settings; sensor pose unchanged | D-077 | print: actual contact at 0.05 mm, static clearance at all stacks; raw bezel planted |
| Orientation undecided | Seat-down keel, sole-down shoe, lips-down bezel, flat shims | D-078 | print: six directions and selected orientation limits |
| Tool and service sequence unproved on final geometry | State-specific keys, screw access and removal sweeps | D-079 | assembly: positive paths and retained-part blockers |
| No keel torques | M3 0.3 N·m; M2 snug only | D-079 | Calculation above; physical insert/strip proof remains open |


Verified on 2026-11-01 with the legacy runtime: **print 42/42**, **assembly 53/53**; regressions
**frame print 36/36**, **frame assembly 50/50**, **axle 27/27**. The strict `makad-v1.step.py`
build passed with every droid edit hitting. The review STEP has **104 valid leaf occurrences**
(topology, closure and positive volumes; full self-intersection search skipped), and four
opposed/orthographic snapshots were reviewed. The all-six-direction survey above uses the
final printed geometry. Physical release items remain in §8.

## 8. Still open (physical)

| What | How |
|---|---|
| Inserts and mounting face | Measure in-hand OD; check no spin at 0.3 N·m, face flat and keel seated; impact/bending tests on the assembled chassis, no coupons |
| CH-069/070 candidates | Receive samples; confirm PH0/head envelopes, Ø1.6 pilots, strip torque and repeated-service retention in PETG |
| TCRT | Check sensor fit, solder sleeves, cable pull-through and bend/slack at each service step; test real-floor signal and cliff stop |
| Shim stack / guards | Measure thickness, loaded optical height, shoe-first tip order and snag behavior; three/four-shim settings need explicit requalification |
| Shoe | Pull/abrasion test and service cycles; verify enlarged tongue still slides after printing |
| Supports | Inspect pocket, groove, mounting face and bezel ledges on actual slice/print |
| Mass | Measure key dimensions and weigh keel, shoe, bezel and shims; update register under rule 6 |
