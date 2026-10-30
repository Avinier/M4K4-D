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
| **Front module** `CHASSIS_FRAME_FRONT_MODULE` | CH-001 | 75 × 128 × 41 mm (X 17–92, Z 32–73) | 75.8 cm³ | PETG, deep slate | Carriers (J04), hatch (J11A), ballast (J12), body (J13), IMU (J15A), drivers (J15B), nose pod (J07B) |
| **Rear module** `CHASSIS_FRAME_REAR_MODULE` | CH-001 | 34 × 132 × 22 mm (X −51 to −17, Z 34–56) | 50.4 cm³ | PETG, deep slate | Carriers (J04), body (J13), keel (J09A) |
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
| 4 hatch bosses, 7 × 7 mm | (28, ±39.5) and (71.5, ±34.35), Z 32–39.5; Ø4.3 insert pilots from below | J11A inserts |
| Front rails, 8 mm wide | X 17–80, Y ±50 to ±58, Z 35–52 | Carry the deck into the carriers and the crossmember |
| J04 rail ends | X 17 face: two Ø4.3 × 6.1 axial pilots at Y ±54, Z 38/48; key pocket 3.2 × 2.4 × 3.4 at Y ±51.5 | Carrier screws and key |
| J13 rib and socket | X 57.5–70.5, out to Y ±64; Ø10.4 vertical socket at (64, ±48) | Socket path for the M4 nut under the deck |
| J13 deck holes | Ø4.5 at (64, ±48); pin hole Ø4.1 at (59, 42) | Body bolts and the front locating pin |
| Front crossmember | X 80–92, Y ±62, Z 35–52 | Nose pod seat (J07B); takes caster loads into the rails |
| Pod insert pilots | Ø4.0 axial, X 85–93, at (Y ±10, Z 42) | J07B inserts (nose review) |
| J10-8 cable bore | Ø5 vertical at (86, −31), through crossmember and deck | Nose sensor cable riser |
| Ballast screw holes | Ø3.4 with a 90° countersink Ø6.5 at (74, ±20) | J12 |
| Driver posts, 4 × Ø7 | Z 56–66 at (41.05, ±34.04) and (41.05, ±54.36); Ø3.9 × 4.1 insert pilot | J15B |
| Motor-lead tie bridges, 2 | X 19–24, \|Y\| 37–43, Z 56–59 | One zip tie each (CH-082) |
| Fuse bracket (D-032) | Column X 75–81, Y 40–48, up to Z 71; shelf X 52–82, Y 39–49, Z 71–73 | Main-fuse holder (ATOF) on the +Y side |
| IMU seat | Flat deck at X 13–29, Y ±10; screws at (22, ±7.5) | J15A, no pilot holes modelled |

### 1.2 Rear module, feature by feature

| Feature | Where | What it is for |
|---|---|---|
| Deck plate, 4 mm | X −41 to −17, Y ±56, Z 52–56 | Body feet (J13) |
| J13 deck holes | Ø4.5 at (−22, ±48); pin hole Ø4.1 at (−27, −42) | Body bolts and the rear locating pin |
| Rear rails | X −32 to −17, Y ±50 to ±58, Z 35–52; gusset X −32 to −23 out to Y ±66 | Into the carriers and the crossmember |
| J04 rail ends | X −17 face: two Ø4.3 × 6.1 pilots at Y ±58.5, Z 38/48; key pocket at Y ±51.5 | Carrier screws and key |
| J13 rib and socket | Ø10.4 socket at (−22, ±48) | M4 nut access |
| Skid crossmember | X −48 to −32, Y ±66, Z 34–48, rising to the deck (Z 52) at X −41 to −32 | Keel seat (J09A) |
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
| M3 × 6 slant-knurled insert, OD 4.4 (OnlyScrews) | CH-061 (J04), CH-077 (J11A) | 8 + 4 | Ø4.3 | In hand |
| M3 × 6 insert, used for the CNC Kitchen M3 × 5.7 positions | CH-063 (pod), CH-067 (keel) | 2 front + 4 rear here | Ø4.0 | In hand (nose and keel reviews) |
| M2.5 × 4 insert, OD 3.9 | CH-080 | 4 | Ø3.9 | **Not bought** |
| ISO 7380 M3 × 8 | CH-060 | 8 | Ø3.4 in the carrier cheeks | |
| ISO 7380 M3 × 6 | CH-076 | 4 | Ø3.4 in the hatch | |
| M3 × 12 CSK, black oxide | CH-038 | 2 | Ø3.4 + 90° × Ø6.5 | |
| M4 × 12 button, M4 nut, Ø4 × 8 pin | CH-035/036/037 | 4, 4, 2 | Ø4.5 deck, Ø10.4 socket, Ø4.1 pin | |
| M2 × 5 thread-forming | CH-039 | 2 | None modelled | |
| M2.5 × 6 low button | CH-081 | 4 | — | |

## 4. Issues going in

Carried over from the [chassis print list](../README.md#before-the-first-export), plus what the
layout above turned up. Each gets a row in the gap table once it is checked.

1. **Insert pilots Ø4.3 for an OD 4.4 insert** (8 J04 rail ends, 4 hatch bosses): 0.05 mm of
   bite per side. Everywhere else in the chassis the same insert goes in Ø4.0. To fix as a
   droid edit to Ø4.0, deeper than the insert.
2. **Module print orientation** has been on hold since D-033. These are the two largest prints.
   Neither face is obviously the bed: deck-down puts the posts, fuse bracket and tie bridges
   under the deck, and deck-up leaves the deck spanning the open tub and the rail bays.
3. **D-033's coupon requirement** (junction and insert coupons) conflicts with the 04-print
   rule that the small parts are the test prints. To settle in the gap table.
4. **J13 pins and deck flatness** across the two modules once the carriers join them (register
   target: coplanar to 0.20 mm).
5. **M2.5 × 4 inserts (CH-080) not bought.** Their Ø3.9 pilot also equals the insert's listed
   OD 3.9, the same zero-bite problem as item 1.
6. **No IMU pilot holes.** The two M2 thread-forming screws are modelled straight into the solid
   deck. The rear 4 mm of the IMU board (X 13–17) overhangs the motor bay.
7. **The hatch is a 1.5 mm plate carrying the 110 g pack** on four screws through 1.5 mm.
   Whether it sags or cracks at the screw holes is part of the J11A/J11B check.
8. **The fuse shelf** is a 30 mm cantilever at Z 71–73 on one 6 × 8 mm column: a print and
   stiffness question for the orientation review.

## Next

5. Printing: orientation per print, checked for overhangs and support area.
6. Assembly and service order, with tool access per joint.
7. Gap table and fixes (droid edits in `final/v1`), with a check script.
8. Still open (physical).
