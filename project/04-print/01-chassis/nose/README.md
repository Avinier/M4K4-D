# Nose (ball transfer) — parts, joints and the review layout

The nose of [chassis v1](../README.md): the printed pod that carries the ball caster and the
front range sensor, its sensor lid and the sliding touch cap, and every joint they carry. This
page reviews the nose for printing, together with the [rear keel](../keel/README.md), the same
way as the [frame](../frame/README.md) (2026-10-31). §1–§3 lay out the parts and joints.

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py)
  (`ball_pod()`, `ball_pod_lid()`, `ball_pod_hardware()`, `tactile_ball_nose()`, `ball_transfer()`).
  The design is [D-011](../../../03-build/decisions.md#d-011) (pod, lid, cap), [D-013](../../../03-build/decisions.md#d-013)
  (Hall sensing) and [D-027](../../../03-build/decisions.md#d-027) (the real GP2Y). Fixes from this
  review go in as droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py).
  The PCB-15 slot edits ([D-059](../../../03-build/decisions.md#d-059), [D-063](../../../03-build/decisions.md#d-063)) are already droid edits.
- **Joints:** the [joint register](../../../03-build/01-chassis/v1/joint-register.md) (J07A, J07B, J08A, J08B, J08C).
- **View:** [`nose-keel.step.py`](http://127.0.0.1:3245/Users/avinier/robotics/makad/project/03-build/final/v1/cad?file=nose-keel.step.py),
  shared with the keel. Two copies: **1 assembled** and **2 exploded** (150 mm to −Y), with every
  part pulled out along the direction it is fitted: the pod forward off the crossmember, the
  caster down, the sensor and Hall board up, the lid 11 mm forward then up, the cap forward. Each
  joint is its own group in the tree. The three nose prints are solid colours (seat slate, lid
  lighter slate, cap ivory); bought parts and the front module (already reviewed) are pale.

Coordinates are the chassis frame: origin on the floor under the axle line, +X forward, +Y
robot-left, +Z up. The ball touches the floor at (110, 0, 0).

## 1. Print units

| Print | BOM | Size (X × Y × Z) | Volume | Material, colour | Joins to |
|---|---|---|---|---|---|
| **Pod seat** `BALL_POD_PRINTED_SEAT` | CH-002 | 36.5 × 49 × 20 mm (X 92–128.5, Z 29–49) | 12.43 cm³ | PETG, deep slate | Front crossmember (J07B), caster (J07A), sensor (J08A), cap and Hall board (J08B), lid (J08C) |
| **Sensor lid** `BALL_POD_SENSOR_LID` | CH-003 | 36.5 × 35.6 × 10.6 mm (X 92–128.5, Z 47–57.6) | 2.54 cm³ | PETG, deep slate | Pod (J08C) |
| **Touch cap** `BALL_NOSE_TOUCH_CAP` | CH-007 | 7.8 × 40.6 × 24.5 mm (X 125.7–133.5, Z 29–53.5) | 2.12 cm³ | ASA, ivory (X1E) | Pod nose (J08B) |

The pod is the nose's structure: the caster hangs under its 6 mm seat, the sensor stands on the
seat's top face, and the whole pod hangs on the crossmember's front face (X 92) by two screws.

### 1.1 Pod seat, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Seat, 6 mm | Z 29–35 over the caster flange (Ø34 about (110, 0)) | Its underside is the caster's seat face (J07A); its top is the sensor floor (J08A) |
| Caster insert bores, 3 | Ø4.0 through the seat at (117.04, 0) and (106.48, ±6.10), the 14.08 mm bolt circle | J07A inserts, pressed from the seat face; the flange bears on their ends |
| Back wall, 3 mm | X 92–95; two Ø3.3 holes at (Y ±10, Z 42) | J07B screws, driven −X from inside the pocket |
| Sensor pocket | X 95–128.5, \|Y\| ≤ 15.5 (15.0 ahead of X 122.1), open at the top and the front; behind X 109 it narrows at 45° above Z 42.9 to \|Y\| 12.3 | GP2Y body (X 114.5–128) and its lead |
| Constant nose | X 122.5–128.5: one octagonal section, half-width 17.8, top Z 51 | The cap slides 3 mm on it (J08B) |
| Snap slots | Both flanks, X 122.4–127.2, Z 32.7–34.9, from \|Y\| 16.8 out | The cap's finger hooks |
| Hall slot | X 126.1–127.1 (1.0 wide, both walls moved 0.4 mm back by D-063), Y 6.9–13.1, Z 30.3–35, open at the top, with a notch through the front face and a relief behind ([D-059](../../../03-build/decisions.md#d-059), [D-063](../../../03-build/decisions.md#d-063)) | PCB-15 Hall board |
| Spring pockets, 2 | Ø3.3, from X 122.5 to the front face, at (Y ±3, Z 32) | J08B return springs |
| Cable channel | 6 × 3 mm, round-cornered, X 91–103, Y ±3, Z 32–35, out through the back wall (1 mm flared mouth), under the crossmember | J10-8 cable to the Ø5 bore at (86, −31) |
| Hall-lead groove | X 100–126.6, Y 9.5–12.5, Z 33.5–35 | PCB-15 leads to the channel |
| Lid tongue groove | X 93.3–95.5, Y ±6.2, Z 46.8–50, open forward | J08C tongue |
| Lid screw boss | Ø4.4 at (111.8, −11.8), fused to the −Y wall, up to the lid underside (Z 49); Ø1.6 pilot from Z 36 | J08C screw |
| Ear slots | X 111.4–119.8, \|Y\| 14.6–22.9 | Vestigial since the GP2Y ears are trimmed (D-027); kept |

### 1.2 Lid

A 2 mm plate (Z 49–51) on the pod's octagonal section, X 92–128.5. A 12 × 1.5 × 2 mm tongue
under its rear edge (X 93.5–95, Z 47–49). A hump over the GP2Y header and its soldered lead, up
to Z 57.6 and open 11.5 mm rearward. A Ø2.2 hole with a 90° countersink at (111.8, −11.8) for
the M2 × 8 countersunk screw.

### 1.3 Touch cap

A 2 mm hood over the constant nose (0.5 mm running gap), open at the bottom and rear, X
125.7–133.5. The face (X 131.5–133.5) has a visor slit, 27 × 10.5 mm with full-round ends, for the
sensor. A top notch passes the lid hump through the 3 mm travel. Two vertical snap fingers,
2.0 mm thick and 16.5 mm tall (Z 29–45.5), each freed by a 0.6 mm slit, carry 0.8 mm hooks
that ride in the pod's flank slots. A Ø3.06 × 1.5 mm magnet pocket opens on the inside of the
face at (Y 10, Z 32.6).

## 2. Joints

| Joint | What holds what | Hardware | Driven from | Register |
|---|---|---|---|---|
| **J07A** | Caster base to the seat underside; the ball load goes into the seat through the flange, the screws only clamp | 3 × ISO 7380 M3 × 8 (CH-031) through the base's 2.7 mm web into 3 × M3 × 6 inserts in the seat (CH-063) | Below, housing and ball unsnapped; body on | [J07A](../../../03-build/01-chassis/v1/joint-register.md#j07a--pololu-2691-caster-to-printed-pod) |
| **J07B** | Pod's back face (X 92) to the crossmember front face | 2 × ISO 7380 M3 × 8 (CH-032) through the 3 mm back wall into 2 × M3 × 6 inserts in the crossmember (CH-033) | Inside the pocket, along −X: cap, lid and sensor out | [J07B](../../../03-build/01-chassis/v1/joint-register.md#j07b--pod-to-front-crossmember) |
| **J08A** | GP2Y0A21YK0F (CH-018) on the pocket floor; the pocket walls locate it in Y, the lid holds it down | None: the lid retains it | Above, cap and lid off | [J08A](../../../03-build/01-chassis/v1/joint-register.md#j08a--front-range-sensor-to-pod) |
| **J08B** | Cap slides 3 mm rearward on the constant nose; snap hooks hold it on, two springs push it back; a magnet in the cap passes the Hall board in the seat | 2 springs (CH-066), Ø3 × 1.5 magnet (CH-065), PCB-15 (CH-064, CH-019) | Front: spread the fingers, slide forward | [J08B](../../../03-build/01-chassis/v1/joint-register.md#j08b--nose-touch-cap-and-contact-sensing-to-pod) |
| **J08C** | Lid on the pod: rear tongue in the groove, front screw; the shell band holds the rear down | 1 × M2 × 8 countersunk thread-forming (CH-062) into the boss | Above; cap off to slide the lid forward 11 mm and lift | [J08C](../../../03-build/01-chassis/v1/joint-register.md#j08c--sensor-lid-to-pod) |

## 3. Hardware going into the nose prints

| Item | BOM | Qty | Hole in the print | State |
|---|---|---|---|---|
| M3 × 6 slant-knurled insert, OD 4.4 (OnlyScrews), in the CNC Kitchen M3 × 5.7 positions | CH-063 (seat), CH-033 (crossmember) | 3 + 2 | Ø4.0 | In hand (the CH-061 stock) |
| ISO 7380 M3 × 8 | CH-031, CH-032 | 3 + 2 | Ø3.2 in the caster web; Ø3.3 in the pod back wall | |
| M2 × 8 countersunk thread-forming | CH-062 | 1 | Ø1.6 pilot in the boss; Ø2.2 + 90° countersink in the lid | Candidate (JCPlas B4B67) |
| Return spring, RS PRO 821245 | CH-066 | 2 | Ø3.3 pockets | |
| Magnet, N35 Ø3 × 1.5 axial | CH-065 | 1 | Ø3.06 × 1.5 pocket in the cap | |
