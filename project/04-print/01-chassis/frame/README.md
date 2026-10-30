# Primary frame — parts, joints and the review layout

The frame of [chassis v1](../README.md): the front module, the rear module and the battery
hatch, and every joint they carry. This page starts the frame review (2026-10-30). §1–§4 lay
out the parts and joints. Printing, assembly order, the gap table and the check come next and
follow the [wheels](../wheels/README.md) and [axle](../axle/README.md) pages.

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py)
  (`frame_module()`, `frame_deck()`, `frame_rail()`, `frame_crossmember()`, `battery_tub()`). The
  module split is [D-033](../../../03-build/decisions.md#d-033). Fixes from this review go in as
  droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py).
- **Joints:** the [joint register](../../../03-build/01-chassis/v1/joint-register.md) (J04, J11A,
  J11B, J12, J13, J15A, J15B).
- **View:** [`chassis-frame.step.py`](http://127.0.0.1:3245/Users/avinier/robotics/makad/project/03-build/final/v1/cad?file=chassis-frame.step.py).
  Two copies: **1 assembled** and **2 exploded** (260 mm to −Y), with every part pulled out along
  the direction it is fitted. Each joint is its own group in the tree, so it can be hidden or
  isolated. The three frame prints are solid colours: front module blue-grey, rear module tan,
  hatch dark grey. Bought parts and the axle carriers (already reviewed) are pale.

Coordinates are the chassis frame: origin on the floor under the axle line, +X forward, +Y
robot-left, +Z up. The deck top is Z 56.

## 1. Print units

| Print | BOM | Size (X × Y × Z) | Volume | Material, colour | Joins to |
|---|---|---|---|---|---|
| **Front module** `CHASSIS_FRAME_FRONT_MODULE` | CH-001 | 75 × 128 × 41 mm (X 17–92, Z 32–73) | 83.2 cm³ (75.8 before D-074) | PETG, deep slate | Carriers (J04), hatch (J11A), ballast (J12), body (J13), IMU (J15A), drivers (J15B), nose pod (J07B) |
| **Rear module** `CHASSIS_FRAME_REAR_MODULE` | CH-001 | 34 × 132 × 22 mm (X −51 to −17, Z 34–56) | 57.8 cm³ (50.4 before D-074) | PETG, deep slate | Carriers (J04), body (J13), keel (J09A) |
| **Battery hatch** `BATTERY_TUB_BOTTOM_HATCH` | CH-011 | 54 × 93 × 1.5 mm (X 21–75, Z 30.5–32) | 7.4 cm³ | PETG, deep slate | Tub bosses (J11A), pack straps (J11B) |

The modules touch nothing but the two J04 carriers. Between them, X −17 to +17, is the open
motor bay: the motors sit in it, and the deck has no plate there.

### 1.1 Front module, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Deck plate, 4 mm | X 17–92, Y ±56, Z 52–56 | Body feet sit on it (J13); IMU and driver posts stand on it |
| Battery aperture | 39.5 × 68 mm over the pack | The pack sits flush with the deck top; the BMS is in the opening |
| Battery tub, 1.5 mm walls | X 24–68.5, Y ±36.5, Z 32–52, open at the bottom | Holds the pack sideways (J11B foam); the hatch closes the floor |
| Tub service window | +Y wall, X 26.9–49.5, Z 40–50 | The pack disconnect (CN-05) passes through it |
| 4 hatch bosses, 7 × 7 mm | (28, ±39.5) and (71.5, ±34.35), Z 32–39.5; Ø4.0 insert pilots from below (D-073; were Ø4.3) | J11A inserts |
| Front rails, 8 mm wide | X 17–80, Y ±50 to ±58, Z 32–52 (Z 35 before D-074) | Carry the deck into the carriers and the crossmember |
| J04 rail ends | X 17 face: two Ø4.0 × 7 axial pilots at Y ±54, Z 38/48 (D-073); key pocket 3.2 × 2.4 × 3.4 at Y ±51.5 | Carrier screws and key |
| J13 rib and socket | X 57.5–70.5, out to Y ±64; Ø10.4 vertical socket at (64, ±48) | Socket path for the M4 nut under the deck |
| J13 deck holes | Ø4.5 at (64, ±48); pin hole Ø4.1 at (59, 42) | Body bolts and the front locating pin |
| Front crossmember | X 80–92, Y ±62, Z 35–52; Z 32 up to X 90.5 (D-074) | Nose pod seat (J07B); takes caster loads into the rails |
| Pod insert pilots | Ø4.0 axial, X 85–93, at (Y ±10, Z 42) | J07B inserts (nose review) |
| J10-8 cable bore | Ø5 vertical at (86, −31), through crossmember and deck | Nose sensor cable riser |
| Ballast screw holes | Ø3.4 with a 90° countersink Ø6.5 at (74, ±20) | J12 |
| Driver posts, 4 × Ø7 | Z 56–66 at (41.05, ±34.04) and (41.05, ±54.36); Ø3.5 × 4.1 insert pilot (D-073; was Ø3.9) | J15B |
| Motor-lead tie bridges, 2 | X 19–24, \|Y\| 37–43, Z 56–59 | One zip tie each (CH-082) |
| Fuse bracket (D-032) | Column X 75–81, Y 40–48, up to Z 71; shelf X 52–82, Y 39–49, Z 71–73 | Main-fuse holder (ATOF) on the +Y side |
| IMU seat | Flat deck at X 13–29, Y ±10; Ø1.6 pilots through the deck at (22, ±7.5) (D-073) | J15A |

### 1.2 Rear module, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Deck plate, 4 mm | X −41 to −17, Y ±56, Z 52–56 | Body feet (J13) |
| J13 deck holes | Ø4.5 at (−22, ±48); pin hole Ø4.1 at (−27, −42) | Body bolts and the rear locating pin |
| Rear rails | X −32 to −17, Y ±50 to ±58, Z 35–52; gusset X −32 to −23 out to Y ±66 | Into the carriers and the crossmember |
| J04 rail ends | X −17 face: two Ø4.0 × 7 pilots at Y ±58.5, Z 38/48 (D-073); key pocket at Y ±51.5 | Carrier screws and key |
| J13 rib and socket | Ø10.4 socket at (−22, ±48) | M4 nut access |
| Skid crossmember | X −48 to −32, Y ±66, Z 34–48, rising to the deck (Z 52) at X −41 to −32; the strip X −48 to −41 up to the deck top, Z 56 (D-074) | Keel seat (J09A) |
| Keel insert pilots, 4 | Ø4.0 from below at (−36.5, ±5.5) and (−44, ±5.5) | J09A inserts (keel review) |
| Cable-tie lug | X −51 to −48, Y −33 to −27, Z 36–44 | Holds the J10-10 TCRT cable |

### 1.3 Hatch

A flat 1.5 mm PETG plate, X 21–75, Y ±46.5. Four Ø3.4 screw holes under the bosses, and four
10.4 × 11 mm strap slots beside the pack's X faces at Y ±29. It hangs in an opening in the
body shell's floor with 0.5 mm all round.

## 2. Joints

| Joint | What holds what | Hardware | Driven from | Register |
|---|---|---|---|---|
| **J04** (rail side) | Each carrier's two cheeks to the front and rear rail ends; the key locates Y/Z, the screws clamp the faces at X ±17 | 8 × ISO 7380 M3 × 8 (CH-060) into 8 × M3 × 6 inserts (CH-061) | Inside the motor bay, motor and housing off | [J04](../../../03-build/01-chassis/v1/joint-register.md#j04-lr--carrier-to-frontrear-rail-ends) |
| **J11A** | Hatch to the 4 tub bosses | 4 × ISO 7380 M3 × 6 (CH-076) into 4 × M3 × 6 inserts (CH-077) | Below, robot on its back or raised | [J11A](../../../03-build/01-chassis/v1/joint-register.md#j11a--battery-hatch-to-tub) |
| **J11B** | Pack strapped to the hatch; both drop out together | 2 hook-and-loop straps (CH-078), 2 foam pads (CH-079) | Below | [J11B](../../../03-build/01-chassis/v1/joint-register.md#j11b--battery-pack-to-tub) |
| **J12** | Steel ballast bar (9 × 60 × 19, about 80 g) to the deck underside, between the tub's front wall and the crossmember | 2 × M3 × 12 CSK (CH-038) from the deck top into tapped holes in the bar | Above | [J12](../../../03-build/01-chassis/v1/joint-register.md#j12--ballast-bar-to-front-deck) |
| **J13** | Body frame feet to both decks; 2 diagonal pins locate, 4 bolts clamp | 4 × M4 × 12 button (CH-035), 4 × M4 nuts (CH-036), 2 × Ø4 × 8 pins (CH-037), Loctite 222 | Bolts from above, nuts from below through the rail sockets. The front-left one (64, 48) is reversed: head in the rail socket, nut in the body cassette (body v1) | [J13](../../../03-build/01-chassis/v1/joint-register.md#j13--body-frame-to-chassis-deck) |
| **J15A** | IMU board PCB-07 flat on the deck | 2 × M2 × 5 thread-forming (CH-039) | Above | [J15A](../../../03-build/01-chassis/v1/joint-register.md#j15a--imu-board-to-deck) |
| **J15B** | Two Adafruit #3297 driver boards on 4 posts; motor leads tied to the deck | 4 × M2.5 × 6 (CH-081) into 4 × M2.5 × 4 inserts (CH-080); 2 zip ties (CH-082) | Above | [J15B](../../../03-build/01-chassis/v1/joint-register.md#j15b--driver-boards-and-motor-lead-restraint) |

The front module also receives the nose pod (J07B) and the rear module the keel (J09A). Their
pilots are cut into these prints, so they are listed in §1, but their joints are reviewed with
the nose and the keel.

## 3. Hardware going into the frame prints

| Item | BOM | Qty | Hole in the print | State |
|---|---|---|---|---|
| M3 × 6 slant-knurled insert, OD 4.4 (OnlyScrews) | CH-061 (J04), CH-077 (J11A) | 8 + 4 | Ø4.0 (D-073) | In hand |
| M3 × 6 insert, used for the CNC Kitchen M3 × 5.7 positions | CH-063 (pod), CH-067 (keel) | 2 front + 4 rear here | Ø4.0 | In hand (nose and keel reviews) |
| M2.5 × 4 insert, OD 3.9 | CH-080 | 4 | Ø3.5 (D-073) | **Not bought** |
| ISO 7380 M3 × 8 | CH-060 | 8 | Ø3.4 in the carrier cheeks | |
| ISO 7380 M3 × 6 | CH-076 | 4 | Ø3.4 in the hatch | |
| M3 × 12 CSK, black oxide | CH-038 | 2 | Ø3.4 + 90° × Ø6.5 | |
| M4 × 12 button, M4 nut, Ø4 × 8 pin | CH-035/036/037 | 4, 4, 2 | Ø4.5 deck, Ø10.4 socket, Ø4.1 pin | |
| M2 × 5 thread-forming | CH-039 | 2 | Ø1.6 through the deck (D-073) | |
| M2.5 × 6 low button | CH-081 | 4 | — | |

## 4. Issues going in and what was done ([D-073](../../../03-build/decisions.md#d-073))

Carried over from the [chassis print list](../README.md#before-the-first-export), plus what the
layout above turned up. Fixes are droid edits in `final/v1`, checked by
[`check_frame_print.py`](../../../03-build/final/v1/cad/check_frame_print.py): **29/29** on
2026-10-30.

| # | Issue | Outcome |
|---|---|---|
| 1 | M3 × 6 insert pilots Ø4.3 for an OD 4.4 insert (8 J04 rail ends, 4 hatch bosses): 0.05 mm of bite a side. The J04 pilots were also only 0.1 mm deeper than the insert | **Fixed.** Ø4.0, as everywhere else in the chassis. J04 pilots 7 mm deep (insert plus 1 mm); boss walls 1.35 → 1.5 mm |
| 2 | Module print orientation, on hold since D-033 | **Settled ([D-074](../../../03-build/decisions.md#d-074), §5):** front tub bottom down, rear deck down, hatch outer face down; two fills give both modules a flat bed face |
| 3 | D-033's coupon requirement against the no-test-print rule | **Settled: no coupons.** The pod seat (plate P02) tries the same M3 × 6 in the same Ø4.0 pilot before the modules print. The junctions are proved on the assembled frame by the test system |
| 4 | J13 pins and deck flatness across the two modules (≤ 0.20 mm) | **Tracked** to the J04 dry fit (measure on the real parts) |
| 5 | M2.5 × 4 inserts (CH-080) not bought; pilot Ø3.9 equals their listed OD | **Fixed in CAD** (Ø3.5, OD − 0.4). Still to buy; measure the OD on arrival and correct the pilot before export if it isn't 3.9 |
| 6 | No IMU pilots; the BOM spoke of a Ø1.6 pilot the CAD didn't have. The board's rear 4 mm (X 13–17) overhangs the motor bay | **Fixed:** Ø1.6 through the deck. The overhang is the connector end; the plug is pushed in along X, so the two screws take it. Kept |
| 7 | The 1.5 mm hatch carries the about 110 g pack | **Closed by calculation:** about 3 N per screw at 10 g; head pull-through about 400 N. The J11B inversion and shock test stays |
| 8 | Fuse shelf, a 30 mm cantilever on one 6 × 8 mm column | **Printed on support** (§5). A gusset under it would fill the body's front-left foot cassette. It carries only the fuse holder |

Not ours but found here: the body's service-panel inserts (BO-063) are the same OD 4.4 insert in
Ø4.3 pilots. They go to the body print review.

## 5. Printing ([D-074](../../../03-build/decisions.md#d-074))

Every face pointing at the bed was measured for all six orientations of each print. The
check repeats the measurement for the chosen ones: a face counts as bridged when material lies
within 15 mm on both sides, or as a ledge when within 2 mm on one side; everything else needs
support. Both modules print with their layers in the XY plane, so the rails bend along the
filaments, the J04 inserts pull along the layers and the J13 bolts clamp across them.

| Print | Face on the bed | Bed | Support (tree, PETG) | Faces that must come out clean |
|---|---|---|---|---|
| Front module | **Tub bottom** (Z 32), as it sits in the robot | 2879 mm² | 1299 mm²: deck underside at X 17–24 (7 mm ledge on the motor bay), the two corner pockets beside the tub's front corners and round the J13 sockets, the fuse shelf, the tub window head | J04 rail-end faces, keys and pilots; deck top (J13 feet, posts); the four hatch bosses (on the bed); J13 sockets; pod pilots and the crossmember front face |
| Rear module | **Deck top** (Z 56) | 3567 mm² | 202 mm²: the four crossmember ends beyond the deck (\|Y\| 56–66) and the tie lug | Deck top (on the bed: J13 seat); J04 rail-end faces, keys and pilots; keel pilots and the crossmember underside |
| Hatch | **Outer face** (Z 30.5) | 4915 mm² | None | Flat both sides; four screw holes; strap slots |

- **The two fills (D-074).** The front rails, J13 ribs and crossmember ran down only to Z 35,
  3 mm above the tub, so the module stood on the 1.5 mm tub walls (469 mm²) with 2588 mm²
  floating. They now run down to Z 32. The rear crossmember strip behind the deck stopped 8 mm
  short of the deck top and now reaches it. Every fill keeps 1.5 mm from the shell, the
  ballast, the pod seat, the body frame and PCB-02; the J13 sockets and J10-8 bore stay open.
  Together they add 14.6 cm³, about 8 g, low in the frame.
- **Why not other faces.** Front deck-down: the posts and fuse bracket stand on the deck top.
  Front on an end or a side: the tub walls become 20 mm ledges (1400–2000 mm² each). Rear
  bottom-down: the deck is a 15 mm ledge over the motor bay (1499 mm²).
- **Why the supports stay.** A 45° wedge under the front X 17–24 ledge would meet the encoder
  plug if the motor arrives with its header turned +X (D-072). Filling the rear crossmember
  ends would touch the carriers and the body frame. A gusset under the fuse shelf would fill
  the body's front-left foot cassette.
- **Bed-face holes.** The rear J13 holes (Ø4.5) and rear pin hole (Ø4.1) open on the bed, so
  elephant's foot narrows them. Use the slicer's elephant-foot compensation, and run a Ø4.1
  drill through the pin hole by hand.
- **Inner driver posts.** The two posts at Y ±34.04 stand half over the battery aperture
  (edge \|Y\| 34.0). They print on a little support and carry a 3 g board. Back each one with
  a dowel through the aperture, with the pack out, while pressing its insert in.
- **Printer.** Both modules fit the A1 (256 mm); the front is 75 × 128 × 41 mm as it lies.
  Settings (walls, infill, hole compensation) go in with the settings column for the whole
  chassis list.

## Next

6. Assembly and service order, with tool access per joint.
7. Gap table and fixes (droid edits in `final/v1`), with a check script.
8. Still open (physical).
