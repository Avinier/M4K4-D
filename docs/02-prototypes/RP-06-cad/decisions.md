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
| `RP03-CAD-04` | **Fixed in CAD context — pending permanent propagation** | Replace the `RP03-CAD-02` nose structure with one printed ball pod that seats on the vendor flange, and move the GP2Y obstacle sensor into it on the centreline, ahead of the ball contact. Keep the ball fixed at `X=110`. |
| `RP03-CAD-05` | **Fixed in CAD context — pending permanent propagation** | Make the drivetrain physically fit: bolt each coaxial gearmotor's face to a chassis flange whose boss carries the 608 pair inside a pocket in a dished wheel, run the wheel on an 8 mm stub shaft, delete the axle crossmember, and carry the rails round the gearboxes. Keep track, wheel envelope and axle height frozen. |
| `RP03-CAD-06` | **Fixed in CAD context — pending permanent propagation** | Move every body-side part 16 mm forward of the drive axle and put the battery in a low chassis tub, to bring the register CoM from x +9.4 to +20.0 mm. The skid moves forward with the body's rear wall to 27 mm behind the axle. |
| `RP03-CAD-07` | **Fixed in CAD context — pending permanent propagation** | Replace the 48 × 75 × 24 mm, 280 g battery placeholder with the RP-02 working selection: a 2S1P pack of two Samsung INR18650-25R cells with a 2S 20 A balanced BMS on top (37.6 × 67 × 23.8 mm, 110 g), and shrink the tub to it. This alone drops the register CoM to x +18.8 / h 107.9 mm, under the `physics.md` §2.5 line; `RP03-CAD-08` restores it. |
| `RP03-CAD-08` | **Fixed in CAD context — pending permanent propagation** | Add an 81.6 g mild-steel ballast bar under the deck between the battery tub and the front crossmember to bring the register CoM back over the `physics.md` §2.5 +20 mm line after the lighter pack. Register CoM +20.6 / 105.8 mm; the +25 / 124 target is still missed. |
| `RP03-CAD-09` | **Fixed in CAD context — pending permanent propagation** | Accept the register CoM that results from the RP-02 power boards (x +18.77 / h 105.05 mm, 2568 g, a_tip 1.75 m/s²) as the working baseline instead of +25 / 124, add no ballast, and re-base the `physics.md` §2.5 check from "x ≥ +20 mm" to the same tip acceleration it encodes at the 124 mm baseline (a_tip ≥ 1.582 m/s²). Builder acceptance 2026-09-25 (`BA-06`). |

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

Re-affirmed by the builder on 2026-09-23 alongside `RP03-CAD-04`: forward edges are
left to camera perception. The camera is still not a low-level stop channel, so the
forward-travel restrictions above stand.

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

**Layout 02 amendment (2026-09-23).** The floor-contact and sensing functions move
into a compact faceted keel under `REAR_SKID_CROSSMEMBER`: wear shoe at `X=-43 mm`,
TCRT at `X=-70 mm`, same 3.5/7/10 mm heights and 27 mm lookahead. The visible tail
becomes a separate, purely cosmetic `REAR_TAIL_STINGER` on the rear service panel:
a slate hub, three telescoping eight-sided ivory segments and a blunt amber chisel tip,
fastened with hidden M3 screws into heat-set inserts. A longer drooping S-curve variant
was rejected because it extended the spin-in-place radius from 128 mm to 164 mm at
ankle/pet height, had no rear contact sensing, and ended in a needle point. The tail must
stay inside the ball-nose spin circle and below the body top. It is currently parked as
an optional accessory (`REAR_TAIL_ENABLED = False`), and the keel is translucent ivory
so its internals remain reviewable.

**Layout 02 amendment 2 (2026-09-24, `RP03-CAD-06`).** The rear crossmember and keel move
16 mm forward with the body's rear wall: wear shoe at `X=-27 mm`, TCRT at `X=-54 mm`.
Heights and the 27 mm lookahead are unchanged. The skid reach falls from 43 to 27 mm
(33 mm to the shoe's rear edge), so the shoe now touches at 6.1° of back-pitch, still
before the CoM crosses the axle at 10.9°. The skid inequality `h/d < x/h` holds at
3.5/33 = 0.11 against 0.19. The parked tail moves forward with the rear panel.

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

## RP03-CAD-04 — Lean ball pod with centred range sensor

Recorded 2026-09-23. Measuring the `RP03-CAD-02` nose found four defects its checks
missed, because those checks compared constants rather than solids:

- the collar (Z 20–26) and keepers (Z 33–36) never touched the flange (Z 27–31), so
  the stated load path did not exist in the model;
- the vendor housing and flange were two disconnected solids;
- the nose rails passed through the purchased flange;
- the ball housing reached X 126.8–128, ahead of the 124.75 fascia face, so a low
  frontal hit, including RP-03's 20 mm `C12` floor object, missed the switch.

Separately, the GP2Y sat at `(84, 38, 68)`: 26 mm behind the ball contact and 38 mm
off the centreline, with a narrow beam that never crossed the centreline. Under
`physics.md` §6 that charged 26 mm to every look-ahead case, and the 0.70 m/s case
needed 315 mm against the sensor's 300 mm rating.

The rails, collar, posts, keepers, shroud and fascia are replaced by:

- one printed pod, 35 mm wide, with an eight-sided section echoing the body end profile. It runs X 92–128.5, exactly the flange footprint plus the sensor, and its rear passes one open-bottom notch in the shell's lower front band. The vendor flange's top face seats on it
  at Z 29. Three M3 screws from inside the pod pocket clamp the flange, clocked at
  0°/120°/240° so every head is reachable from the pocket. Two M3 screws tie the pod
  to heat-set inserts in the front crossmember, which sits inside the shell directly
  behind the flange at X 80–92 with the rails and deck ending at X 92 (moved forward
  from X 67–79 on 2026-09-24 so the pod shrank from 49.5 to 36.5 mm; the battery tub
  gained its own front wall), so no full-width bar or rail stubs protrude. They are driven through the cap window
  once the sensor is out;
- the GP2Y on the centreline in the pod pocket, face at `(128, 0, 41)`, 18 mm ahead of
  the ball contact, under a removable lid. Needed look-ahead from the face is 161 / 203
  / 271 mm at 0.50 level, 0.50 on 2° downhill and 0.70 m/s, or 184.5 / 226.5 / 294.5 mm
  if charged to the nose front. All fit the 300 mm rating; 0.70 m/s is the thin case;
- a 40 mm octagonal touch hood on compliant side arms, open at the bottom and rear,
  from the pod seat (Z 29) to Z 56.6. Its face at X 133.5 leaves 3 mm of travel ahead
  of every rigid part onto a side-actuated tact switch in the lid.

Amended 2026-09-24 at the user's direction: the hood's lower skirt, which reached Z 9
in front of the ball housing, was cut at the pod seat for appearance. Floor-level
objects below the GP2Y beam (Z 41), including RP-03's 20 mm `C12` cube, are therefore
no longer caught by contact. Swept straight at the nose, `C12` now meets the ball's
retaining lip first (X 126.8), and nothing signals it. The contact channel covers only
Z 29–56.6 in front of the pod; forward low-object coverage falls to the camera, which
is not a low-level stop channel. RP-03 still describes the bump as the last layer for
that blind region; under the propagation hold this stays recorded here, not there.

Service order for the ball: lid, then sensor, then the three flange screws. The pod
comes off without removing the body.

Trade-offs: the nose is 12 mm narrower (40 vs 52 mm) and reads as one part, but the
cap's travel moves the front 5 mm forward, so the spin radius grows from 128 to
134.8 mm. The pod top at Z 54 is 5 mm above the old shroud, and the hood top is at Z 56.6. The GP2Y's 40 mm minimum
range falls inside the cap's contact zone. The Pololu hole pattern and screw-from-above
fastening are envelope assumptions to verify on the vendor drawing. Cap flexure
stiffness, switch force, over-travel stop and debounce remain open.

This fixed pod does not take the `D20` caster that RP-03 `decision.md` BD-08,
`rig.md` and `research.md` `R-MNT` still require on the same mount. Under the
propagation hold that swap stays a rig-only comparison until a reviewed change set
updates those documents.

## RP03-CAD-05 — Axle stack that lets the wheels turn

A solid-interference sweep of Layout 02 on 2026-09-24 found that, as drawn, the
drive wheels could not turn and the motors did not fit:

- the 34 mm square bearing carriers reached 11 mm into each wheel (8,342 mm³ per
  side) and the axle crossmember 5 mm (1,080 mm³);
- the carrier bore and the wheel hub both claimed the space around the 608 pair;
- the axle crossmember ran through both coaxial motors (about 14,000 mm³ per side);
- the deck cut the motor-can tops (they stand to Z 57.4 above a Z 52 deck
  underside), and the rails ran through the gearboxes;
- the motors hung 3.4 mm below the shell floor.

No check covered any of it. `axle_crossmember_reaches_wheel_hubs` passed *because*
the crossmember reached into the wheel.

The frozen envelope stays: 170 mm track, Ø84 × 24 mm wheel, 42 mm axle height, motor
output face at |Y| 69. Inside it:

- **Flange and boss.** Each gearbox face bolts to a 2 mm chassis flange (|Y| 69–71,
  34 × 30 mm). Its R15 boss runs to |Y| 86 and carries the 608 pair at |Y| 74 / 81.5
  in an R11.25 bore.
- **Dished wheel.** The wheel's inner face is pocketed R18 to |Y| 88. The boss sits
  inside the wheel's envelope with 3 mm radial and 2 mm end running gaps. The web
  carries the hub.
- **Stub shaft.** An Ø8 steel stub (|Y| 70.5–95) runs in the bearings, takes the motor's
  Ø4 D-shaft (9.5 mm assumed) in a bore at its inboard end, and is fixed to the web.
  It starts 1.5 mm off the gearbox face, which is the tightest running gap.
- **Structure.** The axle crossmember, square carriers and gussets are deleted. The
  motors fill the axle line, so each rail is split at |X| 17. Cheek plates at
  |X| 13.5–17, 1 mm off the gearbox, carry it round to the flange. The deck becomes
  two plates either side of a |X| 17 relief over the motor cans. The shell floor is
  slotted |X| 17 across the axle, joining the wheel wells, so the body still lowers
  onto the chassis.
- **Encoder leads.** The pigtail reserve moves over the encoder end, behind the axle,
  in the deck relief.

New checks measure this from solids:

- `wheel_running_clearance_to_static_parts` (≥ 1.5 mm);
- `drivetrain_static_parts_do_not_interfere`;
- `motor_face_seats_on_axle_flange`;
- `bearings_sit_inside_flange_boss`.

The wheel is axisymmetric, so its own solids are its swept volume.

Still open: the gearmotor's face-screw pattern and shaft length, the stub-to-web
fixing and axial retention (RP-03 P06 ≥ 3 N axial), the bearing preload/spacing,
the wheel's printed mass, and whether a two-plate deck plus cheeks is stiff enough.
That last one needs a structural check, not a packaging one.

## RP03-CAD-06 — Body forward on the chassis and a low battery tub

The dimensional baseline targets x_CoM +25 / h 124 mm. Before this decision, Layout 02's
register gave x +9.4 / h 106.7, so the ball lifted at 0.86 m/s². RP-03's authored
launches are 0.80–1.20 m/s², so that left no margin. The ball also carried 8.5 % of the
weight, under `physics.md`'s 9 % walking-spin flag. Moving the battery alone could not
fix it: the pack could move about 4 mm forward before meeting the front crossmember and
the speaker keep-out, and it already overlapped the speaker cavity and lower front
cross (`physics.md` §2.2 reaches the same conclusion).

The builder chose a 16 mm body shift over a 21 mm shift, nose ballast, or a
battery-only change with a recorded baseline miss:

- **What moves.** `BODY_SHIFT_X = 16` moves every body-side part: shell, panels, body
  frame and mounts, electronics, audio, harness, yaw stage and the RP-01 head. The yaw
  axis is now at X 16. The wheels, motors, ball, pod, front crossmember and deck front
  edge stay in the chassis frame.
- **Rear chassis.** The rear crossmember, rails and keel move forward with the body's
  rear wall (see the `RP03-CAD-03` amendment).
- **Battery.** It lies across the robot in a chassis tub under the deck (48 × 75 × 24 mm
  at X 18–66, Z 32–56), flush with the deck top. It drops out through a bottom hatch that
  hangs in a shell-floor opening.
- **Body locators.** The rear locating pin moves a further 10 mm aft so its deck bore stays
  on the rear plate.

Result (hand-kept register, with the `RP03-CAD-05` chassis change and the previously
missing 608 bearings added):

| | Before | After |
|---|---:|---:|
| Mass | 2627 g | 2615 g |
| CoM x / h | +9.4 / 106.7 mm | **+20.2 / 103.7 mm** |
| x/h | 0.088 | 0.195 |
| a_tip = g·x/h | 0.86 m/s² | **1.91 m/s²** |
| Ball share | 0.085 | 0.18 |

This clears the `physics.md` §2.5 line (x ≥ +20 mm gives the 0.80–1.00 m/s² launches
margin), but only just: +20.21 mm (+20.03 before the `RP03-CAD-04` crossmember moved
forward). It still misses the +25 / 124 target (x/h 0.195 vs 0.202, a_tip 1.91 vs
1.98 m/s²). Under the baseline's rule, that is either recovered by
geometry or the baseline is revised; commanded acceleration is not quietly reduced.

Consequences to carry into propagation:

- the head yaw axis is 16 mm ahead of the drive axle, so the head orbits during a spin
  (negligible at 220 °/s);
- the wheels sit in the rear third of the body;
- battery swap is from underneath (or by lifting the body);
- the tub-to-body harness path is unrouted;
- every CoM number depends on the manual mass register, not on the geometry.

## RP03-CAD-07 — 2S1P 18650 battery pack

RP-02 never fixed a chemistry or a construction; it held a 2S protected-18650 holder as an
`E` planning case and left the rest to a ledger envelope of 2.6–5.3 Wh over the 20-minute
`MD-01` workload. On 2026-09-24 the builder closed **2S**, chose Li-ion NMC cylindrical
cells, and set price and CAD fit as the two constraints (see RP-02 `decision.md`). The
pack that meets both is two Samsung INR18650-25R cells (2500 mAh, 20 A continuous, about
18–22 mΩ, Ø18.33 × 64.85 mm, 45 g) in series, with a 2S 20 A balanced protection board.
That is about 18 Wh nominal, about twice the 9.2 Wh high-case requirement.

What changed in the model:

- **Pack.** `battery_pack()` builds two cells (Ø18.4 × 65 mm, axes along Y, 18.6 mm pitch),
  a strap-and-insulation plate at each cell end (1 mm) and a 48 × 20 × 4.5 mm BMS board lying on top of the cells.
  Envelope 37.6 × 67.0 × 23.8 mm at X 27.9–65.5, Z 32–55.8, 0.2 mm under the deck top.
  The replaced placeholder was 48 × 75 × 24 mm at X 18–66.
- **Tub.** The tub is now derived from the pack: 1.5 mm retention gap on each side, front
  wall inner face unchanged at X 67, rear wall moved forward from X 16.5 to 24.9, half-width
  39 → 36.5 mm. The deck cut-out and the shell-floor opening follow. Tub volume −2.1 cm³;
  the register moves −1.2 g on the chassis row and +2.6 g on the shell row (floor returned).
- **Mass.** `BATTERY` row 280 → 110 g (2 × 45 g + about 8 g board + about 12 g sleeve, straps
  and leads), all `E`, no purchase or weighing.

Result (hand-kept register):

| | Before | After |
|---|---:|---:|
| Mass | 2615 g | 2444 g |
| CoM x / h | +20.2 / 103.7 mm | **+18.8 / 107.9 mm** |
| x/h | 0.195 | 0.175 |
| a_tip = g·x/h | 1.91 m/s² | **1.71 m/s²** |
| Ball share | 0.18 | 0.17 |

A 170 g lighter pack takes forward mass out of the robot. Height rises toward the 124 mm
target, but x falls 1.4 mm away from +25 and under the `physics.md` §2.5 line of +20 mm
(by 1.16 mm), so `com_forward_of_physics_margin_line` failed with this change alone.
`RP03-CAD-06` had rejected nose ballast, so the builder chose the ballast option on
2026-09-24 and it is recorded as `RP03-CAD-08`.

Still open on the pack: the BMS board thickness (4.5 mm assumed, 0.2 mm of deck-top margin
is left), the sleeve and pack tolerance, tub retention (foam or straps), the hatch
fastening, the lead and connector (Anderson SBS Mini is RP-02's lead, unchosen), the NTC
position, and the tub-to-body harness. No vendor STEP was used; the cells and the board are
datasheet and listing envelopes.

## RP03-CAD-08 — Ballast bar ahead of the battery tub

The lighter 2S1P pack (`RP03-CAD-07`) took 170 g of forward mass out of the robot and left the
register CoM at x +18.8 mm, 1.16 mm under the `physics.md` §2.5 line. The builder chose ballast
(over moving other weight or revising the line) on 2026-09-24.

- **Part.** A mild-steel bar, 9 × 60 × 19 mm (X 69.5–78.5, Y ±30, Z 33–52), 7.85 g/cm³, 79.7 g
  after two tapped holes, plus two M3 screws (1.9 g): **81.6 g** in the register, centred at
  (74, 0, 42.5) mm. It is not a nose weight: it sits under the deck, inside the shell.
- **Place.** It fills the free 11.5 mm between the tub's front wall (X 68.5) and the front
  crossmember (X 80), with 1.0 mm and 1.5 mm of clearance and its top face against the deck
  underside. The battery still drops out through the bottom hatch; the bar does not block it.
- **Fixing.** Two M3 screws from the deck top at (74, ±20), with the heads sunk in counterbores
  in the 4 mm deck and 8 mm of thread in the bar. Thread engagement and pull-out in the printed
  deck are unverified.

Result (hand-kept register):

| | Before (`RP03-CAD-06`) | After `RP03-CAD-07` | After `RP03-CAD-08` |
|---|---:|---:|---:|
| Mass | 2615 g | 2444 g | **2526 g** |
| CoM x / h | +20.2 / 103.7 mm | +18.8 / 107.9 mm | **+20.6 / 105.8 mm** |
| x/h | 0.195 | 0.175 | **0.195** |
| a_tip = g·x/h | 1.91 m/s² | 1.71 m/s² | **1.91 m/s²** |
| Ball share | 0.18 | 0.17 | 0.19 |

All 98 checks pass. The +20 mm margin is **0.62 mm**, so a small register change can flip it
again. The +25 / 124 target is still missed (x/h 0.195 vs 0.202); reaching +25 mm would need
about 376 g of ballast at this position or a change of geometry. The pack plus ballast weighs
192 g against the old 280 g placeholder, so the robot is 89 g lighter overall than the
placeholder assumed. The ballast position was chosen for the free space, not optimised: a bar
further forward is not possible without moving the crossmember.

## RP03-CAD-09 — CoM baseline revised for the power boards

The RP-02 power boards (`board-specs.md` v0.18, layout 02 as of 2026-09-25) replaced the 121.5 g
`CONTROL_POWER_SENSORS` row with per-board rows (121.0 g), added the 40 g E-stop, and raised the
pack row to 113.7 g. The register moved from x +20.63 / h 105.73 mm to **x +18.77 / h 105.05 mm**
(2524.6 → 2567.8 g). The builder accepted that result on 2026-09-25 rather than adding ballast
(about 59 g at X 74 would restore +20 mm, and the ballast slot cannot take it) or moving weight.

**What the "+20 mm line" is.** `physics.md` §2.5 gives the margin as `a_tip = g·x/h` against the
authored `a_peak` 0.80–1.00 m/s², evaluated at the baseline height h = 124 mm: `9.81 · 20 / 124 =
1.582 m/s²`. The check tested the x value alone. The register height has since fallen to about
105 mm, so the same 1.582 m/s² is reached at **x = +16.94 mm**. The check now tests the tip
acceleration (`a_tip ≥ 1.582`), which is the quantity the line was written to protect. This is a
re-basing on the accepted baseline, not a relaxation of the margin: a_tip is 1.753 m/s², 1.11×
the 1.582 floor and 1.75× the authored `a_peak` of 1.00.

**Other loading cases (`E`, `physics.md` §2.6, §2.8 with the register CoM and the head lump
geometry of §2.8, head mass 509–557 g, lever 52 mm).**

| Case | x / h (mm) | a_tip |
|---|---|---:|
| Neutral head | 18.77 / 105.05 | 1.753 m/s² |
| `HP-PITCH-FWD` (+35° nose down) | 24.7–25.2 / 103.0–103.2 | 2.35–2.40 m/s² |
| `HP-PITCH-AFT` (−18° look up), the worst head pose | 15.3–15.6 / 104.5 | **1.44–1.46 m/s²** |
| Forward brake / reverse launch, spin | unchanged in kind | far above the authored 1.20 m/s² (`physics.md` §2.6) |

The worst head pose stays above the authored `a_peak` 1.00 (1.44×), where `physics.md` §2.8 had it
below 1.00 for the Layout 03 lumps. The rear-skid check (`rear_skid_catches_before_com_crosses_axle`)
and the ball share (≥ 0.09) pass at the new CoM.

**What this does not change.** The +25 / 124 target is still missed (x/h 0.179 vs 0.202) and the
`a_tip ≈ 2.0 m/s²` planning value is not reached; per `physics.md` §2.5 the dimensional baseline is
revised, and RP-03 must not read the commanded `a_peak` as re-approved. The mass register is
hand-kept and the head lumps in §2.8 are `E`; a weighed robot (`W`) replaces both.

Result: 108 of 108 checks pass after the re-base (the geometry is unchanged from the run with one
failure). Propagation to the permanent RP-03 documents stays on hold with the other `RP03-CAD` items.

## Propagation hold

Do not edit the permanent RP-03 documents merely because this geometry now exists.
When Layout 01 is accepted, propagate the retained choices and their consequences as
one reviewed change set: sensor/BOM count, GPIO allocation, electrical stop path,
motion restrictions, receiving/calibration tests and safety claims. Permanent RP-03
documents must replace the prior full-width bumper requirement only after that review.
