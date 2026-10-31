# Nose (ball transfer) — parts, printing, assembly and service

The nose of [chassis v1](../README.md): the printed pod that carries the ball caster and the
front range sensor, its sensor lid and the sliding touch cap, and every joint they carry. This
page reviews the nose for printing, together with the [rear keel](../keel/README.md), the same
way as the [frame](../frame/README.md) (2026-10-31). The CAD review and its checks are recorded below (2026-11-01).

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py)
  (`ball_pod()`, `ball_pod_lid()`, `ball_pod_hardware()`, `tactile_ball_nose()`, `ball_transfer()`).
  The design is [D-011](../../../03-build/decisions.md#d-011) (pod, lid, cap), [D-013](../../../03-build/decisions.md#d-013)
  (Hall sensing) and [D-027](../../../03-build/decisions.md#d-027) (the real GP2Y). Fixes from this
  review go in as droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py).
  The PCB-15 slot edits ([D-059](../../../03-build/decisions.md#d-059), [D-063](../../../03-build/decisions.md#d-063)) are already droid edits.
- **Joints:** the [joint register](../../../03-build/01-chassis/v1/joint-register.md) (J07A, J07B, J08A, J08B, J08C).
- **View:** [`nose-keel.step.py`](../../../03-build/final/v1/cad/nose-keel.step.py),
  shared with the keel. Two copies: **1 assembled** and **2 exploded** (150 mm to −Y), with every
  part pulled out along the direction it is fitted: the pod forward off the crossmember, the
  caster down, the sensor and Hall board up, the lid 12 mm forward then up, the cap forward. Each
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
| **J08C** | Lid on the pod: rear tongue in the groove, front screw; the shell band holds the rear down | 1 × M2 × 8 countersunk thread-forming (CH-062) into the boss | Above; cap off to slide the lid forward 12 mm and lift | [J08C](../../../03-build/01-chassis/v1/joint-register.md#j08c--sensor-lid-to-pod) |

## 3. Hardware going into the nose prints

| Item | BOM | Qty | Hole in the print | State |
|---|---|---|---|---|
| M3 × 6 slant-knurled insert, OD 4.4 (OnlyScrews), in the CNC Kitchen M3 × 5.7 positions | CH-063 (seat), CH-033 (crossmember) | 3 + 2 | Ø4.0 | In hand (the CH-061 stock) |
| ISO 7380 M3 × 8 | CH-031, CH-032 | 3 + 2 | Ø3.2 in the caster web; Ø3.3 in the pod back wall | |
| M2 × 8 countersunk thread-forming | CH-062 | 1 | Ø1.6 pilot in the boss; Ø2.2 + 90° countersink in the lid | Candidate (JCPlas B4B67) |
| Return spring, RS PRO 821245 | CH-066 | 2 | Ø3.3 pockets | |
| Magnet, N35 Ø3 × 1.5 axial | CH-065 | 1 | Ø3.06 × 1.5 pocket in the cap | |


## 4. Issues going in and what was done (D-077)

All geometry fixes are droid edits in `final/v1`; the subsystem source stays unchanged.
The final-tree checks are `check_nose_keel_print.py` and `check_nose_keel_assembly.py`.

| Issue | Outcome |
|---|---|
| Five nose inserts specified as the unbought CNC Kitchen M3 × 5.7 | Use the in-hand OnlyScrews M3 × 6, OD 4.4, in the existing Ø4.0 bores: three through the 6 mm seat, two in 7 mm crossmember pilots. Models and BOM now agree |
| The insert under the GP2Y finishes at the sensor floor | A Ø5 × 0.5 relief around its upper end takes displaced plastic. Press from below, flush with the caster seat, and clean the floor before fitting the sensor |
| Seat insert 2 is close to the Hall-lead groove | Least wall past the knurl is 1.15 mm; keep, press slowly, inspect the groove after installation |
| Lid thread-former sourcing | Existing Ø1.6 pilot is real, with 1.15 mm minimum wall beyond the thread. CH-062 remains a JCPlas B4B67 candidate; qualify the received head and PETG pilot before export, as CH-039 in D-073 |
| Nose-face-down cap orientation starts the snap fingers above their slits | Print top down; keep support out of the finger slits (D-078) |
| ASA on the X1E awaits permission | Still open. Keep ASA and the existing geometry; an alternative material needs fit and snap-fatigue qualification before adoption |
| The documented 11 mm lid slide does not provide a clear upward path past the speaker panel | 12 mm forward then up is clear; 11 mm then up hits the panel, and sliding 13 mm hits the GP2Y. Both wrong paths are planted (D-079) |
| Trimmed GP2Y inspection solid had invalid topology | Heal its trimmed solid in the droid tables at the same pose and bounds; printed geometry and sensor position unchanged |
| PCB-15 slot and relief could be lost in new edits | D-059 and D-063 retained and checked on the final seat |

## 5. Printing (D-078)

The check surveys all six axis directions. Bed area is contact with the bed; support area is
surface requiring support, not filament volume or slicer time. Downward triangles beyond the
45° rule count unless bridged within 15 mm, a ledge within 2 mm, or a small cylindrical hole.
The 44° normal threshold tolerates tessellation at nominal 45° chamfers. The lab must still
check the actual slice, especially the cap's fingers and small horizontal holes.

| Print | Face on the bed | Bed | Support area | Faces that must come out clean |
|---|---|---|---|---|
| Pod seat | **Caster seat, −Z** | 1264 mm² | None | Caster flange seat; Ø4 bores; sensor floor; Hall slot and lead groove; crossmember back face |
| Lid | **Front end, +X** | 67 mm² | 89 mm² | Rear tongue; pod seat rim; hump interior for the soldered lead; countersink |
| Cap | **Top, +Z** | 145 mm² | 33 mm² | Snap fingers and 0.6 mm slits; running faces; magnet pocket; visor opening |

Use a brim for the lid's small end face, kept off the fitting tongue. Remove support through
the lid's open underside. On the cap, support only the surveyed interior overhangs; never bridge
support across a finger slit. The top is visible and on the bed: confirm the lab's bed finish
is acceptable for ivory ASA. Remove elephant's foot from running edges without widening the
nominal 0.5 mm gap. The pod's horizontal crossmember clearance holes and spring pockets need a
clean slice; do not enlarge the insert pilots by drilling.

The seat prints flat on the A1; the lid stands on its front end. The cap uses the enclosed X1E,
with the lab's permission for ASA. A material fallback is not qualified by CAD: shrinkage,
sliding friction and finger fatigue must be checked on the real part before changing material.
No separate coupons (rule 5): the pod seat on P02 tries the M3 × 6 / Ø4.0 fit before the modules.

**Six-direction survey, final geometry (bed / support, mm²).** Direction is toward the bed.

| Print | −Z | +Z | −X | +X | −Y | +Y |
|---|---|---|---|---|---|---|
| Seat | 1264.4 / 0 | 185.3 / 644 | 624.3 / 436 | 255.8 / 679 | 110.2 / 374 | 110.2 / 367 |
| Lid | 18.0 / 901 | 284.6 / 621 | 50.0 / 89 | 67.2 / 89 | 0.0 / 277 | 0.0 / 277 |
| Cap | 99.9 / 114 | 144.8 / 33 | 138.6 / 453 | 577.7 / 70 | 104.5 / 39 | 104.5 / 37 |

## 6. Assembly and service (D-079)

Tools are checked against the final chassis and body in each stated assembly condition.
Whole-pod J07B tool entry needs the body off; the smaller nose service steps keep it fitted.
Hex cylinders enclose the key across its corners: 2 mm key radius 1.155 mm. The PH0 envelope
is a Ø3 shaft; confirm the bit against the actual candidate screw. Sweeps sample removal at
1 mm steps; lead flexibility, fingers spreading and hands are physical checks.

**Tools:** straight 2 mm hex key plus a shortened 2 mm L-key for J07B (8 mm from
the screw-head face to the bend, approximately 10 mm short leg including engagement); PH0 for the specified candidate lid screw; M3 insert iron
with a Ø6 tip envelope; flat backing plate; torque driver covering 0.2–0.3 N·m. For J07B with the L-key, 4 N
perpendicular to a 50 mm lever arm gives 0.2 N·m; use a force gauge or a calibrated adapter.

| Screw | Torque | Basis, as D-076 |
|---|---|---|
| J07A caster, M3 × 8 | 0.3 N·m | About 500 N per screw using nut factor 0.2; head bears on the vendor flange. Limit remains insert retention in the seat |
| J07B pod, M3 × 8 | 0.2 N·m | About 333 N; roughly 20 MPa under the Ø5.7 head around the Ø3.3 hole, below the review's approximately 50 MPa PETG yield assumption |
| J08C lid, M2 × 8 thread-forming | Snug only | Stop when the countersunk head seats; sample and repeat-service qualification remain open |

### On the bench, before the body

1. Clean the prints and dry-fit the lid tongue, sensor and cap. Do not glue a binding cap.
2. Install the three M3 × 6 seat inserts **from below**, flush on a flat backing surface.
   These are through bores: no blind-hole bottom clearance is needed. The insert occupies the
   full 6 mm seat. Clean the relief over insert 1 and check the sensor still sits flat; check
   the lead groove beside insert 2. Check no spin at the chosen screw torque before P01.
3. With the pod off, install the two front-crossmember inserts along −X from the front.
   The Ø6 iron envelope reaches both mouths with the loose frame on the bench. Their Ø4 pilots
   are 7 mm deep and the inserts finish flush with X 92.
4. Fit the caster base to the pod from below, housing and ball unsnapped. Drive its three
   M3 × 8 screws with the 2 mm key to 0.3 N·m (5.3 mm thread engagement), then snap the housing,
   rollers and ball onto the base. Confirm the received caster matches the modeled flange.
5. Offer the pod against the crossmember at X 92. Cap, lid and GP2Y are out. Use the shortened 2 mm L-key, short leg along −X into each head and long leg up
   through the pocket; the bend is at X 104.65. Swing the long leg **inward across the pocket**, 5–65°
   from upright toward the centre, then withdraw/re-index. Drive to 0.2 N·m, with 5 mm thread engagement.
   A straight key hits the lid boss on the −Y side; do not cut the boss for access.
   Fit this before the body. For service take the body off first: the shell band blocks the
   L-key entering from above, even with the front panel removed.
6. Install PCB-15 in the retained D-059/D-063 slot. Route its leads in the groove; fit the
   trimmed-ear GP2Y on the floor with its soldered lead routed through the rear channel.
   Check the actual PCB-15 board fit and magnet polarity before retaining the cap.
7. Fit the lid by reversing the checked removal path; screw snug. Install the two return
   springs, the magnet in the cap, and spread the fingers to slide the cap on from the front.
   Check full 3 mm travel and positive return without a trapped wire.

### Service

| To do | Sequence | Access |
|---|---|---|
| Caster | Unsnap housing, ball and rollers; three screws out; base down 40 mm | 2 mm key from below. Housing blocks all three keys if left on |
| Cap | Spread both fingers to disengage hooks, slide forward 20 mm; catch springs | From front. Hooks left engaged are a planted blocker |
| Lid | Cap off; lid screw out; slide forward **12 mm**, then lift 40 mm | PH0 from above; 0.5 mm in X past the panel. Do not over-slide: GP2Y hit begins at 13 mm |
| GP2Y | Cap and lid off; release cable slack and unplug J10-8 before pulling the tether; sensor out along the checked path | Sensor and Hall board share a routed cable; do not pull a fixed harness |
| Hall board | GP2Y out first, then board up 30 mm | The GP2Y stands over the slot and is a planted blocker |
| Whole pod (body off) | Take body off by frame page §6E/service; cap, lid and GP2Y out; two pod screws out; pod and caster forward 40 mm | Short 2 mm L-key enters from above, body off, with a 60° inward swing. The GP2Y blocks a straight key; retained screws block removal |

## 7. Gap table

| Gap | Fix or disposition | Decision | Check |
|---|---|---|---|
| CNC Kitchen inserts unbought; 6 mm replacement not represented | Nine M3 × 6 models, nose bores and walls measured | D-077 | print: insert bores, walls and engagement |
| GP2Y over the through insert's far end | Ø5 × 0.5 relief and floor cleanup | D-077 | print: relief, PCB-15 preservation |
| Candidate M2 screw | Ø1.6 actual pilot; manufacturer/sample qualification | D-077 | print: lid boss |
| Wrong cap orientation | Top down; fingers start from supported material | D-078 | print: all-six survey and planted face-down case |
| Lid short lift meets speaker panel | 12 mm forward then 40 mm up; no sensor move | D-079 | assembly: short path planted, replacement path |
| Straight −Y pod key meets the lid boss; fitted shell blocks L-key entry | Short L-key: 8 mm from head face to bend, long leg up; whole-pod service with body off | D-079 | assembly: L-key clear; straight key planted |
| No nose torques | J07A 0.3, J07B 0.2 N·m; lid snug | D-079 | Calculation above; physical retention remains open |


Verified on 2026-11-01 with the legacy runtime: **print 42/42**, **assembly 53/53**; regressions
**frame print 36/36**, **frame assembly 50/50**, **axle 27/27**. The strict `makad-v1.step.py`
build passed with every droid edit hitting. The review STEP has **104 valid leaf occurrences**
(topology, closure and positive volumes; full self-intersection search skipped), and four
opposed/orthographic snapshots were reviewed. The all-six-direction survey above uses the
final printed geometry. Physical release items remain in §8.

## 8. Still open (physical)

| What | How |
|---|---|
| First P02 pod seat / in-hand inserts | Measure OD; install square and flush; check no spin at torque, no bulged sensor floor or Hall-lead groove; then print modules |
| Caster | Measure the received flange, web and holes; prove snap service and clear screw heads; static/drop/threshold loads at the test-system limits |
| CH-062 thread-former | Buy the candidate sample; confirm PH0/head angle, Ø1.6 PETG pilot, strip resistance and repeated service |
| Cap | Obtain ASA permission; print in ASA; verify slide, spring return, hook release and fatigue; no unqualified material swap |
| Sensing | PCB-15 board fit, magnet orientation, trip point, return force, sensor retention and lens alignment; check J10-8 cable slack through the full service path |
| Supports and bed finish | Inspect the lid hump, finger slits and visible cap top on the actual slice and print |
| Mass | Measure key dimensions and weigh all three prints; update the hand-kept register (rule 6) |
