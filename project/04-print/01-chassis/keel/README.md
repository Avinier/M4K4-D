# Rear keel — parts, joints and the review layout

The rear keel of [chassis v1](../README.md): the faceted keel under the rear crossmember, its
replaceable wear shoe, the TCRT bezel with its guard lips and the height shims, and every joint
they carry. This page reviews the keel for printing, together with the [nose](../nose/README.md),
the same way as the [frame](../frame/README.md) (2026-10-31). §1–§3 lay out the parts and joints.

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py)
  (`rear_skid_tcrt_keel()`, `rear_crossmember_inserts()`, `frame_crossmember("REAR")`). The design
  is [D-014](../../../03-build/decisions.md#d-014) (keel, J09, J10), [D-016](../../../03-build/decisions.md#d-016)
  (the soldered TCRT lead) and [D-017](../../../03-build/decisions.md#d-017) (PETG wear parts). Fixes
  from this review go in as droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py).
- **Joints:** the [joint register](../../../03-build/01-chassis/v1/joint-register.md) (J09A, J09B, J10A, J10B).
- **View:** [`nose-keel.step.py`](http://127.0.0.1:3245/Users/avinier/robotics/makad/project/03-build/final/v1/cad?file=nose-keel.step.py),
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
| **Keel** `REAR_KEEL_FACETED_BODY` | CH-008 | 50 × 19 × 28 mm (X −67 to −17, Z 6–34) | 14.64 cm³ | PETG, taupe | Rear crossmember (J09A), bezel (J09B), shoe (J10A) |
| **Wear shoe** `REAR_KEEL_REPLACEABLE_WEAR_SHOE` | CH-009 | 12 × 10 × 5 mm (X −33 to −21, Z 3.5–8.5) | 0.40 cm³ | PETG, deep slate | Keel (J10A) |
| **TCRT bezel** `REAR_TCRT_BEZEL_WITH_GUARDS` | CH-010 | 14 × 15 × 9 mm with its pin (X −61.5 to −47.5, Z 7–16) | 0.30 cm³ | PETG, taupe | Keel through the shims (J09B); carries the guard lips (J10B) |
| **Height shims** `REAR_TCRT_HEIGHT_SHIM_*` | CH-068 | 14 × 15 × 1.0 mm each | 0.12 cm³ each | PETG, deep slate | Between bezel and keel belly (J09B); two fitted, four printed |

The keel is the rear floor-contact part: the shoe takes the skid when the robot tips back, and
the TCRT looks down through the keel's sensor flat for cliffs and edges.

### 1.1 Keel, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Seat (top face) | Z 34, X −48 to −32, the crossmember underside | J09A |
| Screw bores, 4 | Ø3.4 at (−36.5, ±5.5) and (−44, ±5.5); Ø6.5 counterbores from below to Z 9.5 (front pair) and Z 12 (rear pair) | J09A M3 × 30 socket heads |
| Shoe belly | Z 6, X −21 to −38 | The shoe sits under it (J10A) |
| Dovetail groove | X −32.15 to −13, open at the front where the belly rises; 4.3 → 6.3 mm wide, 2.65 deep | J10A shoe tongue |
| Shoe screw holes | From the +Y side at (−27, Z 7.25): Ø2.2 clearance Y 0–5.3, Ø3.8 head counterbore Y 5.3 out | J10A M2 × 6 |
| Sensor flat | Belly Z 12, X −46 to −62, half-width 9.5 | Bezel and shims seat on it (J09B) |
| TCRT pocket | 10.8 × 7.6 mm about (−54, 0), open below the belly and up through the keel top | The TCRT drops out below; its lead rises through the top |
| Bezel pilot | Ø1.6 at (−54, −5.6), Z 11–20.5 | J09B M2 × 10 thread-forming |
| Pin hole | Ø2.0 at (−54, +5.6), Z 11–18.5 | The bezel's Ø1.8 moulded pin |

### 1.2 Wear shoe, bezel and shims

- **Shoe:** a 12 × 10 × 2.5 mm octagonal sole (2.5 mm corner chamfers), X −33 to −21, Z 3.5–6.
  On top, a dovetail tongue 4 mm wide at the root and 6 mm at the top, 2.5 mm tall (Z 6–8.5), X
  −32 to −21. A Ø1.6 pilot crosses the tongue at Z 7.25 for the M2 × 6.
- **Bezel:** a 1.5 mm plate (Z 8.5–10), X −61.5 to −47.5, Y ±7.5, with a 9 × 7.6 mm window that
  leaves 0.6 mm end ledges under the TCRT. Two guard lips under it (J10B), 2.5 mm wide at Y
  ±5.6, X −61.5 to −49, down to Z 7. A Ø1.8 pin rises 6 mm at (−54, +5.6). At (−54, −5.6) a
  Ø2.2 screw hole, with a Ø3.8 head recess through the lip.
- **Shims:** the bezel's outline, 1.0 mm thick, with the sensor window and two Ø2.2 holes. The
  optical face sits on the bezel at Z 12 − shims: two give Z 10.

## 2. Joints

| Joint | What holds what | Hardware | Driven from | Register |
|---|---|---|---|---|
| **J09A** | Keel seat to the crossmember underside; skid loads go through the screws into the crossmember and both rails | 4 × ISO 4762 M3 × 30 (CH-034) into 4 × M3 × 6 inserts in the crossmember (CH-067) | Below, keel, shoe and bezel fitted | [J09A](../../../03-build/01-chassis/v1/joint-register.md#j09a--rear-keel-to-rear-crossmember) |
| **J09B** | TCRT face down on the bezel ledges; bezel and shims to the keel belly; height = Z 12 − shims | 1 × M2 × 10 thread-forming (CH-069) and the moulded pin; shims (CH-068) | Below, keel on | [J09B](../../../03-build/01-chassis/v1/joint-register.md#j09b--rear-tcrt-cartridge-to-keel) |
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
