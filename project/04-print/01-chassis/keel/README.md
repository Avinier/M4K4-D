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
