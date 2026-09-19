# RP-03 CAD pass 1 — adjustable envelope model requirements and todo

Status: requirements and execution plan only. This document does **not** authorize a blockout, freeze a SKU, or contain geometry.

What this plan authorizes when work starts: **CAD pass 1**, an *ugly, adjustable envelope model* of the Concept A base. Bounding boxes, mount holes, shafts, cable exits, 360° keep-outs, contact datums, and mass/`(x,h)` lumps.

What it does not authorize, at any point, without a separate gate freeze:

- a cosmetic shell, fillets, or styling surfaces;
- a purchased SKU solid treated as the robot;
- final chassis CAD, or integrated whole-body packaging — those are a post-freeze activity and **RP-06**'s scope (`plan.md` §10);
- a G01–G06 claim, an ADR-04 closure, or a purchase.

Inherited inputs, with their real status:

| Input | Status | Authority |
|---|---|---|
| Locomotion architecture | Concept A: two powered encoder wheels, passive front support, **mandatory** rear anti-tip skid | `decision.md` locked table; `dimensional-baseline.md` v1.12 |
| Front support **type** | Ball transfer selected as V1 (`D21`) | BD-08 |
| Front support **swap** | `D20` Ø25–32 mm swivel caster is **required**, on the **same mount** | BD-08; baseline v1.12 |
| SKU set | **Not frozen.** `D02`, `D21`, `DRV-B`, `S01`/`S04`/`S06`/`S07` are *leads*; `D20`, `D03`, QRE1113, MPU-6500-if-SPI stay live substitutes | `research.md` §1.1, status line; `decision.md` conclusion |
| Head geometry | Inherit RP-01 Layout 03 as a **mass and interface lump**; do not re-author the head | RP-01 `cad/head/layout-03/` |
| Electrical architecture | Inherit RP-02; reserve keep-outs only | RP-02 registers |

The objective of pass 1 is narrow and testable: **an envelope model in which every scored geometric question can be measured and every adjustable dimension can actually be adjusted.** Nothing in it is a selection.

---

## 1. Source hierarchy

Use sources in this order when values conflict. This plan is **not** at the top of that list, and may not promote itself there.

1. [`dimensional-baseline.md`](../../../01-system/dimensional-baseline.md) for whole-robot geometry, CoM targets, and the skid inequality.
2. [`decision.md`](../decision.md) for locked decisions, `BD-` rows, and what is *not* closed.
3. [`RP-03 research.md`](../research.md) for part identities, envelopes, capture class (`W`/`D`/`E`/`U`), print-vs-buy, and the §5 datum list.
4. [`physics.md`](../physics.md) for tip, traction, stopping, and coverage geometry; [`storyboard.md`](../storyboard.md) for the motion cases those serve.
5. RP-01 head CAD — [`head/layout-03`](../../RP-01-head/cad/head/layout-03/) — for the head envelope, mass tree, yaw interface, and the parameter/output/check *pattern*.
6. RP-02 electrical documents for what the base must reserve:
   [`README.md`](../../RP-02-electrical/README.md) ·
   [`compute-control-architecture.md`](../../RP-02-electrical/compute-control-architecture.md) ·
   [`power-branch-contracts.md`](../../RP-02-electrical/power-branch-contracts.md) ·
   [`link-contract.md`](../../RP-02-electrical/link-contract.md)
7. Official manufacturer drawings, STEP models, and datasheets.
8. Direct measurement of the exact in-hand article.
9. Labelled placeholder envelopes, only where neither exists.

Rules carried in:

- **Leads are not freezes.** A lead may be drawn as a *class envelope*. It may not be drawn as the purchased article.
- **Print does not freeze.** A printed adapter is geometry, not a SKU selection, not a `D10` freeze, not a G01 pass.
- Do not infer a board outline from the silicon package inside it. The breakout is the mechanical part.
- Do not average conflicting figures. Record both, the source, and which one the model uses. The motor stall conflict is the standing example.
- `research.md` remains the part-identity register. This plan is not a second BOM and issues no `BD-` row.
- Accepted pass-1 values become authoritative only after checks pass **and** the values are propagated to the affected Markdown.

---

## 2. Coordinate system and datum contract

This is the first CAD task and it is not open to restyling. The chassis frame is **axle-origin**, per `research.md` §1.2 and the baseline. Every CoM figure, tip acceleration, battery band, and skid inequality in the project is already expressed in it.

- origin: **floor plane, on the drive-axle ground-contact line**, at the robot longitudinal centre plane;
- `+x`: forward, **toward the front support**;
- `+y`: robot left;
- `+h` (`+z`): up from the floor;
- ground plane: `h = 0` at nominal loaded ride height;
- centre plane: `y = 0`;
- drive axle: `x = 0`, `h = 42 mm`;
- wheel axes: parallel to `y`;
- left/right always from the robot's perspective.

RP-01 Layout 03 uses a **head-local** origin (front/bottom centre, `+X` face, `+Y` left, `+Z` up). It is imported through an explicit transform at the yaw interface. **Do not adopt the head origin as the chassis origin.** Doing so silently reinterprets every number above.

Required named frames:

- `F_GROUND` — origin as defined above
- `F_AXLE` — drive axle centreline
- `F_WHEEL_L`, `F_WHEEL_R`
- `F_FRONT_CONTACT` — front-support **ground contact**, not the fork crown or flange face
- `F_MOUNT_FRONT` — the interchangeable support mount datum
- `F_SKID_CONTACT`
- `F_CLIFF_F`, `F_CLIFF_L`, `F_CLIFF_R`
- `F_IR_OPTICAL` — analog-IR optical axis origin
- `F_BUMPER`
- `F_IMU` — base IMU axes, labelled against the body frame
- `F_BAY` — ballast/battery bay slide datum
- `F_NECK` — head/yaw demate plane, with the RP-01 transform stated
- `F_BODY` — body electronics volume datum

Todo:

- [ ] Publish the frame table and the RP-01 import transform before any solid exists.
- [ ] State nominal loaded ride height and the loaded tyre radius assumption separately from nominal wheel OD.
- [ ] Define positive wheel rotation and the forward sign convention.
- [ ] Show an axis triad and datum labels on every dimensional and physics view.
- [ ] Export the frame table as generated Markdown/JSON.

---

## 3. Parameter set — `research.md` §5 datum list, adopted verbatim

These are the model's centralized parameters. They are ranges where research found ranges. **Do not collapse a range to a point value to make modelling easier**, and do not substitute napkin `110 / 14 / 21`.

| # | Parameter | Value | Note |
|---|---|---|---|
| 1 | Ground plane, axle height, track | `h_axle = 42 mm`; track **170 mm** c-c | Fixed by baseline |
| 2 | Wheel envelope | **Ø80–85 × 10–35 mm** | Family not chosen; see §5 |
| 3 | Motor keep-out | **Ø28 × 90 mm** each, gearbox outboard, encoder inboard, M3 face **19 mm** | Includes cable pigtail |
| 4 | Front contact | `x = **105–115 mm**` (110 target), with **0–15 mm** vertical shim (`R-MNT`) | Adjustable, lockable |
| 5 | Front-support adapters | **Two**: Pololu 1″ 3-hole (29 mm native) and 33×38 caster plate (38 mm native) | Both, on one mount |
| 6 | Battery bay | **Entirely forward of `x = 0`**; 73 mm industrial flange is **not** first-fit | See §8 |
| 7 | Cliff patches | **10 × 6 × 7 mm** at three contacts | Contact-referenced |
| 8 | Analog-IR | **30 × 14 × 14 mm** on the front carrier | At front contact |
| 9 | Bumper | **205 mm** bar, inboard of tyre scrub | Printed bar, bought switch |
| 10 | Rear skid | **60–80 mm** reach × **8–16 mm** height | Not a frozen 14/70 solid |

Envelope and motion constraints the model may not violate:

| Constraint | Value |
|---|---|
| Overall envelope (CON-14) | 300 H × 205 W × 180 D mm |
| Shell ground clearance | 25–35 mm |
| Drive mass row | 200–600 g (motors, wheels, support, skid, brackets, driver share) |
| Follow ceiling | ≤ 0.50 m/s |
| Commanded spin | 180–220 °/s |
| Authored `a_peak` | 0.80 / 1.00 m/s² |
| Creep | 0.04 m/s |
| Stop-path latency budget | ≤ 50 ms detection-to-decel |

A 360° front-support sweep that only uses the straight-ahead pose has not been researched.

---

## 4. Assembly tree

A multi-part, adjustable assembly. Not one fused solid, and not a styled body.

```text
RP03_BASE_PASS1
├── RP01_HEAD_LUMP                   # mass + yaw-interface reference only; not re-authored
├── FRAME
│   ├── R_FRM_AXLE_FRAME             # open frame, 170 mm track, stiffness independent of ballast
│   ├── R_CLP_MOTOR_CLAMP_L / _R      # axle-centred, independently serviceable
│   ├── R_HUB_CARRIER_L / _R          # 608 or D-insert carrier (printed); bearings bought
│   ├── R_BAY_BALLAST_BAY             # independent x-slide and h-stack
│   └── NECK_TRUNK_VOID               # centreline; demate at the body
├── DRIVE
│   ├── MOTOR_L / MOTOR_R            # Ø28 × 90 keep-out cylinders
│   ├── ENCODER_CAP_L / _R
│   ├── WHEEL_L / WHEEL_R            # selected envelope family, labelled
│   └── HUB_L / HUB_R
├── FRONT_SUPPORT
│   ├── R_MNT_MOUNT                  # ONE mount, shared datum, 0–15 mm shim stack
│   ├── R_ADP_BALL                   # Pololu 3-hole adapter
│   ├── R_ADP_CAS                    # 33×38 caster-plate adapter
│   ├── BALL_TRANSFER                # D21, installed V1
│   └── SWIVEL_CASTER                # D20, required swap — modelled, not excluded
├── REAR_SKID                        # MANDATORY
│   ├── R_SKID_CARRIER               # adjustable reach and height, lockable
│   └── SKID_PAD
├── SENSING
│   ├── CLIFF_F / CLIFF_L / CLIFF_R  # carriers at contacts
│   ├── IR_FRONT                     # at front-support contact
│   ├── BUMPER_BAR + SWITCHES
│   └── IMU_BASE                      # rigid base mount
├── BODY_ELECTRONICS_KEEPOUT
│   ├── C3_DEVKIT
│   ├── DRIVER_L / DRIVER_R
│   ├── BATTERY_OR_DUMMY
│   └── HARNESS_TRUNK_VOLUMES
└── RIG_ONLY
    ├── R_HDUM_HEAD_DUMMY            # Layout 03 mass lump with pose extras
    ├── R_INT_SENSOR_INTERPOSER
    ├── R_CUE_STATUS_LIGHT
    └── R_CHK_WHEEL_CHOCKS
```

Every fabricated part carries its `R-` ID from `research.md`. Every purchased envelope carries its identity **and its capture class** (`W`/`D`/`E`/`U`).

---

## 5. Drive — motors, encoders, wheels, hubs

### 5.1 Motors and encoders (`R-MTR`, `R-ENC`)

- [ ] Model the keep-out cylinder, not a cosmetic motor: **Ø28 × 90 mm** including the cable pigtail, gearbox outboard, encoder inboard.
- [ ] Place the two-M3 face pattern at **19 mm** spacing, marked `E` until confirmed on the article.
- [ ] Model the **4 mm D-shaft** at **10–12 mm** length with a ~8 mm D-flat. Hub stick-out may not exceed available shaft.
- [ ] Check the **~120 mm** clear span between cans at 170 mm track, before clamps.
- [ ] Route the cable exit **inboard then up the neck**, never across the tyre.
- [ ] Carry motor mass as **~110 g each with encoder**. Do not use the ~85 g encoderless figure.
- [ ] Record the standing **stall conflict** beside the model: 900 mA / 0.490 N·m versus ≤ 3 A / 0.441 N·m. Do not average, do not pick one silently.
- [ ] Design an axle-centred **printed clamp** that takes radial load. A commodity L-bracket is not the design.
- [ ] Service check: one motor comes out without dropping the ballast bay and without disturbing the opposite wheel.

Not permitted: a printed gearbox; a 37D-class pair; a JGA25 STEP from a third party treated as the purchased winding.

### 5.2 Wheels (`R-WHL`)

There is **no exact Ø84 × 21 mm article**. Pass 1 picks an envelope *family* and says so; it does not draw the missing SKU.

| Envelope | Ø × width | Hub | Mass | Note |
|---|---|---|---|---|
| A — India toy | 83 × 35 mm | 4 mm **round** | 54 g | Fills the 205 mm stance with no shell margin; needs a printed D-adapter |
| B — Pololu multi-hub | 80 × 10 mm | 4 mm **D collet** | `U` | Best shaft retention; Ø80 is in band |
| C — skate + adapter | 84 × 24 mm PU | **608** bore + adapter | 90 g | Best diameter match; forces `R-HUB` |

- [ ] Model the chosen family as a labelled envelope with the alternatives retained as suppressed configurations.
- [ ] Do **not** solid a 21 mm tread. It is not on the bench.
- [ ] Model scrub volume through a 180° pivot, not just the rolling envelope.
- [ ] Treat **loaded radius** as an open input that gates the shim stack, not as nominal OD.

### 5.3 Hubs and retention (`R-HUB`, HOLD)

- [ ] Model the printed 608 / D-insert carrier as its own part; bearings and metal inserts are bought.
- [ ] Verify the carrier does not push track past the 205 mm stance.
- [ ] Reserve the radial-load solution as a **HOLD**: the gearbox radial rating is unpublished against ~11 N wheel load on an 8–10 mm stub.
- [ ] Reject set-screw-on-round as the production path; model it only if the bought wheel turns out round-bored.

---

## 6. Front support — one mount, two articles

This is the highest-value geometry in pass 1 and the original plan inverted it. `research.md` lists *"CAD pocket that only accepts the ball"* as an explicit reject.

- [ ] Build **one** mount (`R-MNT`) whose datum is the **ground contact**, not the fork crown or the flange face.
- [ ] Provide a **0–15 mm** lockable vertical shim with a readable mm scale.
- [ ] Model **both** adapters as installed-capable parts: `R-ADP-BALL` (Pololu 1″ 3-hole, 29 mm native, 34 mm housing width, 12.2 mm hole span, 16.5–18.5 g) and `R-ADP-CAS` (33 × 38 plate, holes 30 × 23 M4, 38 mm native; the 25 mm variant is 34.5 mm and 32 g).
- [ ] Prove the swap **does not change** the `105–115 mm` contact number once set.
- [ ] Sweep the front-support pocket through **360°** and through its **service removal**, against the battery tray, all three look-downs, and the wheel envelope.
- [ ] Model instantaneous wheelbase on the caster as `L ± trail`; trail is `U` and must be shown as a range, not a measurement.
- [ ] Keep look-down #1 travelling **with** the carrier so coverage does not walk when reach is adjusted.
- [ ] Do not model a printed ball, a printed cup, or a printed fork as the scored article.
- [ ] Do not model the 15.9 mm steel "metal ball caster" as `D21`, and note the 73 mm industrial flange fights the forward bay in 180 mm depth.

Required output: a support-interface table giving, for each article, native height, shim required against the 42 mm axle, hole pattern, 360° swept volume, and the resulting contact `x`.

---

## 7. Rear anti-tip skid — mandatory

The skid is a locked architectural element, not an optional protection part.

- [ ] Model an adjustable carrier: reach **60–80 mm** behind the axle, height **8–16 mm** above the floor, both lockable.
- [ ] Do **not** freeze 14 mm at 70 mm. That pair fails every lumped Layout 03 CoM unless ballast restores forward `x`.
- [ ] Enforce the inequality `h/d < x_CoM / h_CoM` as a generated check at the **scored** CoM, not the target CoM.
- [ ] Model it as a **catch**: normal-pose skid load is zero. It is not a fourth support wheel and not a cosmetic tab.
- [ ] Carry look-down #3 on the skid carrier so rear coverage tracks reach adjustment.
- [ ] Verify the pad area and that the pad cannot shear off in a reverse contact.

---

## 8. Ballast, battery, and CoM control

`HIGH_AFT` is a forbidden placement, and the model must make it *physically unfittable* rather than merely discouraged.

- [ ] Place the battery/dummy volume **entirely forward of `x = 0`**, in the pack CoM band `x = +50…+80 mm`, `h = 18–32 mm`, mass band 150–500 g.
- [ ] Run a deterministic check that **no** pack-sized volume fits on or behind the axle.
- [ ] Build `R-BAY` with **independent `x` slide and `h` stack**. Ballast is the CoM instrument; changing a wheel must never be how CoM is tuned.
- [ ] Cover the BD-05 load cases: 1.65 kg and 3.10 kg-plus-head.
- [ ] Model `R-HDUM` as the Layout 03 head lump: **~499–524 g** at ~250–255 mm CoM height, with `HP-PITCH-FWD/AFT` and `HP-YAW-L/R` pose extras and a ~52 mm pitch lever. A plain 304 mm stick is not BD-05.
- [ ] Keep high-current paths short and segregated; keep terminals clear of service drop paths.
- [ ] Reserve fuse, disconnect, and charge-connector access, per RP-02.

---

## 9. Sensing — placement is millimetres from contact

Coverage is measured from **contact geometry**, not from the axle and not from a bumper drawing.

### 9.1 Look-downs (`R-CLF-*`, `S01` TCRT-class)

- [ ] Three carriers: **~40 mm ahead of ball contact**, on the **skid** contact, and one **wheel-adjacent**.
- [ ] Standoff **2–8 mm** to the floor, adjustable and calibratable; peak response is at 2.5 mm.
- [ ] Lateral channel covers the shoulder through a 220 °/s pivot (~102 mm sweep) without colliding with the wheel at lock-to-lock.
- [ ] Rear channel is valid **before** reverse travel, and does not view the tabletop catch lip.
- [ ] Record that the dominant failure is **reflectivity**, not geometry: the dark-and-glossy trial is mandatory and is a rig task, not a CAD claim.

### 9.2 Analog-IR obstacle (`R-IR`, `S04` GP2Y-class)

- [ ] Mount at the **front-support contact**, optical axis `+x`. An axle-mounted sensor may not be credited as leading-contact.
- [ ] Body 30 × 14 × 14 mm plus the Vcc capacitor; clear the support's 360° sweep and do not stare into the floor.
- [ ] Carry the look-ahead budget as a result, not an assumption: covers 179 mm at 0.50 m/s; **HOLD** at 221 mm on a 2° downhill and 289 mm at 0.70 m/s.
- [ ] Leave the near lobe below 40 mm to the bumper.
- [ ] Extract the optical-axis datum from the Sharp drawing. It is currently `U`.

### 9.3 Bumper, IMU, ToF

- [ ] Bumper bar spans the **205 mm** stance, inboard of tyre scrub, with switch envelopes ~20 × 6 × 10 mm. One centre button is not this part.
- [ ] Model lever travel against the support's 360° sweep; travel and height stay `U` until the rig.
- [ ] Reserve **25 × 25 × 5 mm** for the base IMU breakout on a **rigid base** mount, never in the head, with SPI run length and axis labels relative to the body frame. The module outline is `U` until a breakout is named; the silicon package is not a proxy for it.
- [ ] ToF is **telemetry only**. Model it only if the spare-GPIO rule still holds, and it may **not** take the analog-IR contact mount.

### 9.4 Stop-path rules the geometry must not break

These are architectural, and CAD can violate them by accident:

- stop-path sensing is native GPIO or C3 ADC. Never shared-bus-only, never through an expander;
- unknown sensor state means inhibit;
- the base controller keeps **≥ 2 spare safe GPIO**, and no safety **output** sits on the strapping pins;
- the DevKit RGB is not the status cue, because that pin is the watchdog feed;
- a driver board carrying its own cliff headers is a reject, not a packaging convenience.

---

## 10. Body electronics and harness keep-outs

Reserve volumes; do not redesign RP-02.

- [ ] Two driver carriers as **20 × 20 × 12 mm** keep-outs in the **body**, not the tub, with motor copper isolated from logic.
- [ ] C3 DevKitC board **~69 × 25.4 mm** plus USB plug and service access; header keep-out; strapping pins reserved.
- [ ] Neck-void trunk on the centreline with a **keyed demate at the body**. No slip ring, no motor current in a servo daisy chain, no Dupont.
- [ ] Strain relief on both faces of the demate, and a service loop on the chassis.
- [ ] Separate motor-power routes from encoder and sensor routes; document any unavoidable crossing.
- [ ] Model harness as routed volumes with bend envelopes, not decorative lines.
- [ ] Keep harness out of wheel, support 360°, skid-adjustment, bumper, and fastener-tool swept volumes.
- [ ] Produce a connector table: source, destination, family, mate direction, and disconnect order.

---

## 11. Mass, CoM, and stability outputs

### 11.1 Mass register

One generated row per physical item: ID, description, quantity, mass, **source** (`measured` / `vendor` / `CAD density` / `estimate`), **capture class** (`W`/`D`/`E`/`U`), local CoM, placed CoM in the **axle frame**, state (`installed` / `swap` / `rig-only` / `placeholder`), and date.

Cable, connector, fastener, adapter, and printed-part mass are explicit rows. Contingency is a separate documented line, never a hidden margin.

### 11.2 Required calculations

- [ ] Total mass and mass by subsystem; **drive row against the 200–600 g budget**.
- [ ] Whole-robot CoM `(x, h)` at the BD-05 load cases and head pose extras.
- [ ] Tip acceleration `a_tip = g·x_CoM / h_CoM` reported as the **lumped range** (~0.9–1.9 m/s² with battery forward), against the authored `a_peak` of 0.80 / 1.00.
- [ ] Explicit sign check: `a_tip` must be positive. Report the failure loudly if any configuration puts CoM at or behind the axle.
- [ ] Skid inequality `h/d < x_CoM / h_CoM` at the scored CoM, per adjustment setting.
- [ ] Wheel normal-load split and front-support normal load.
- [ ] Support triangle from two wheel contacts and the front contact; CoM projection margin to each edge.
- [ ] Wheel torque and speed from loaded radius: the 0.70 m/s case needs ~159 wheel RPM at Ø84; a 220 °/s in-place pivot at 170 mm track needs ~74 RPM per wheel.
- [ ] Encoder resolution against creep: ≲ 2 mm/count and ≳ 20 counts/s at 0.04 m/s.
- [ ] Ground clearance and threshold break-over against the 25–35 mm band.
- [ ] Overall envelope against CON-14.

Pass 1 reports these as **paper values with capture classes**. None of them is a gate result. Lift onset, scrub, dent, jam, drag, flutter, and stopping distance are **rig measurements**, and CAD may not claim them.

### 11.3 Physics overlays

Generated from the same parameters as the model, never typed onto a screenshot: CoM markers with coordinates, the three contacts and support triangle, the skid inequality state, tip margin, axis triads, and swept volumes.

---

## 12. Purchased-part evidence and the open-`U` register

### 12.1 Evidence package per item

Manufacturer and orderable number; official page, datasheet, 2D drawing, STEP where available; in-hand photos with scale; direct measurement of critical mating features; measured mass; **capture class**; discrepancy notes; adopted CAD value.

### 12.2 Primary-source anchors already captured

Sourcing anchors, not permission to substitute a variant.

| Item | Official geometry in hand | Remaining closure |
|---|---|---|
| Pololu 1″ plastic ball transfer (#2691) | 29 mm height, 34 mm housing width, 12.2 mm hole span, 16.5–18.5 g | Verify the in-hand article is this one; measure contact height against **loaded** wheel radius before fixing the shim |
| Pololu DRV8874 carrier (#4035) | 15.2 × 17.8 mm PCB, 0.9 g | Model as 20 × 20 × 12 mm installed, with headers and wire bend |
| NFP / Aslong GM25-370 family | Ø25 gearbox, 21 mm at 35:1, can ~30.8 mm, 4 mm D-shaft, ~110 g with encoder | Exact suffix, rear cap, face pattern, cable exit; the stall conflict stays open |
| Sharp GP2Y0A41SK0F | 29.5 × 13 × 13.5 mm, 3.5 g, 16.5 ms cycle | Optical-axis datum from the drawing; connector and cable envelope |
| Vishay TCRT5000 | 10.2 × 5.8 × 7 mm, peak at 2.5 mm | Valid for the bare component only; capture the carrier board if one is installed |
| ESP32-S3-DevKitC-1-N8 | Official drawing / DXF; ~69 × 25.4 mm | Exact N8 revision, antenna keep-out, USB plug, header stack |

The ICM-42688-P package drawing is **not** a mechanical proxy for its breakout. Reserve the envelope and leave it `U`.

### 12.3 Open `U` items that gate a freeze

Pass 1 must carry these visibly and may not model around them:

| Open item | What it gates |
|---|---|
| India encoder SKU at 6 V / ~176 RPM | Bench reference unit; printing closes nothing here |
| D-shaft versus round on the wheel actually bought | Hub print |
| Caster trail in millimetres | Flutter and heading behaviour |
| Ball rolling resistance and laminate dent | Whether `D21` iterates to the caster |
| Gearbox radial rating | Whether the 608 carrier is mandatory |
| SPI IMU module outline | Base keep-out |
| GP2Y optical-axis number | Exact look-ahead from contact |
| Loaded wheel radius under squash | The whole shim stack against 42 mm |

### 12.4 Fabricated parts

Each `R-` part gets: stable ID and revision, material and process, parameterized interface dimensions, tolerance and fit notes, fastener and insert spec, print orientation, minimum wall/rib/boss checks, mass and density assumption, export requirement, and post-fabrication inspection dimensions.

---

## 13. Review views

Pass 1 needs fewer views than a styled body, and different ones. Independent visibility groups: frame, drive, front support (both articles), skid, sensing, body electronics, harness volumes, ballast, swept volumes, physics overlays, annotations, rig-only parts.

1. Side elevation through the centreline, dimensioned to axle, front contact, and skid.
2. Front elevation through both wheel axes, dimensioned to track and stance.
3. Underside view with all three contacts and the sensor patches.
4. Front-support detail: **ball installed**, with shim stack and 360° sweep.
5. Front-support detail: **caster installed**, same mount, same contact `x`, showing `L ± trail`.
6. Support-swap comparison overlay.
7. Skid adjustment view at both reach extremes with the inequality annotated.
8. Wheel / motor / hub section showing shaft engagement and clamp load path.
9. Cliff-sensor view: three patches, standoff, and coverage from contact.
10. Analog-IR view: optical axis, look-ahead from contact, near-lobe handoff to the bumper.
11. Bumper span and lever travel against the support sweep.
12. Body electronics and keep-outs.
13. Harness volumes with route classes.
14. Ballast bay at `x` and `h` extremes.
15. Physics view: CoM at each load case, support triangle, tip margin.
16. Axis and frame view with all triads.
17. Envelope check against CON-14.
18. Service views: motor removal, wheel removal, support swap, battery removal.

Every image states the layout revision, which wheel envelope family is shown, and which items are placeholder or `U`.

---

## 14. Deterministic checks

Small scripts in the spirit of RP-01's `write_dimensions.py`, `check_layout.py`, and `check_assembly.py`. Machine-readable JSON plus a short Markdown summary.

**Geometry**

- [ ] Track, axle height, and contact `x` match parameters.
- [ ] Wheel axes collinear; left/right symmetric where intended.
- [ ] Front contact `x` is **identical** with the ball and with the caster fitted.
- [ ] Shim stack spans 0–15 mm and reaches both native heights.
- [ ] Skid reach and height are adjustable across their full bands and lock.
- [ ] Overall envelope within CON-14; ground clearance within 25–35 mm.
- [ ] Hub stick-out does not exceed available shaft length.
- [ ] No pack-sized volume fits at or behind `x = 0`.

**Motion and clearance**

- [ ] Front-support 360° sweep clears battery tray, all look-downs, and the wheel, for **both** articles.
- [ ] Wheel rotation and 180° pivot scrub clear frame, guards, harness, and sensors.
- [ ] Bumper travel clears wheels, support sweep, and sensor optics.
- [ ] Harness volumes clear every swept volume and tool path.
- [ ] Every fastener has a tool approach with wheels and support installed.
- [ ] Support removal and motor removal trajectories are valid.

**Physics**

- [ ] Mass register total equals assembly total within tolerance.
- [ ] No installed item has zero or unknown mass.
- [ ] `a_tip` positive in every configuration; lumped range reported.
- [ ] Skid inequality satisfied at the scored CoM for the chosen adjustment.
- [ ] CoM projection inside the support triangle with margin, at every load case.
- [ ] Drive mass row within 200–600 g.
- [ ] IMU axis export agrees with the frame contract.

**Provenance**

- [ ] Every purchased envelope carries identity, source, and capture class.
- [ ] Every `U` from §12.3 appears in the output, unclosed and visible.
- [ ] No lead is labelled "frozen" anywhere in generated output.
- [ ] `dimensions.json` and `dimensions.md` agree.

---

## 15. Iteration and propagation

1. Work inside the active `base/pass-01/` folder.
2. Change centralized parameters and regenerate outputs.
3. Review the saved views and run the checks.
4. Keep provisional dimensions **local to the CAD folder** while evaluating.
5. Propagate only accepted values, and only to the right owner:
   - `research.md` — capture facts, closed `U` rows, measured envelopes;
   - `rig.md` — adjustability ranges the model proved must stay adjustable;
   - `physics.md` — geometry inputs, never a gate result;
   - `candidate-sourcing-matrix.md` — dated India class and substitutes, the only price and stock home;
   - `dimensional-baseline.md` — only if an accepted value contradicts a baseline target, which is a **baseline revision**, not a quiet edit;
   - `decision.md` — **nothing** until a freeze. Pass 1 issues no `BD-` row and authorizes no purchase.
6. Record the CAD revision beside every propagated value.
7. Open `pass-02` only for a materially different architecture, not routine tuning.

---

## 16. Ordered todo

Ordered to match `research.md` §7: geometry first, then stop-path placement, then body electronics.

### Phase 0 — Authority and evidence index

- [ ] Record in the CAD brief that the architecture is Concept A with a ball-transfer V1 type and a required caster swap, and that **no SKU is frozen**.
- [ ] Build the evidence index with capture class per item.
- [ ] Copy the §12.3 `U` register into the brief as live blockers.
- [ ] Record the consumed RP-01 and RP-02 revisions.

Exit: every item has an identity, a class, and a route to closure. No item is mislabelled as frozen.

### Phase 1 — Frame contract

- [ ] Publish the axle-origin frame table and the RP-01 import transform.
- [ ] Set ground, axle height, track, and the loaded-radius assumption.
- [ ] Define the front-contact datum and the shim reference.

Exit: contacts, axle, and head interface are locatable without interpretation.

### Phase 2 — Drive envelopes

- [ ] Motor and encoder keep-outs, face pattern, shaft, cable exit.
- [ ] Choose and label a wheel envelope family; retain the others suppressed.
- [ ] Motor clamps and the hub/bearing carrier.
- [ ] Check span, stance, scrub, and the drive mass row.

Exit: track, shaft, and radial-load story are coherent.

### Phase 3 — Both front supports and the skid

- [ ] Build the single mount, the shim stack, and **both** adapters.
- [ ] Place ball and caster; prove identical contact `x`; sweep both through 360° and through service removal.
- [ ] Build the adjustable skid carrier and run the inequality check.

Exit: the swap is real geometry, and the anti-tip catch is adjustable.

### Phase 4 — Stop-path placement

- [ ] Place three look-downs at their contacts with adjustable standoff.
- [ ] Place the analog-IR at the front contact; compute look-ahead from contact.
- [ ] Place the bumper bar and switches; check lever path against the sweeps.
- [ ] Place the base IMU envelope.

Exit: coverage is measured in millimetres from contact and the architectural rules hold.

### Phase 5 — Body electronics and harness

- [ ] Reserve driver, C3, battery, and connector volumes.
- [ ] Route harness classes as volumes; add strain relief, demate, and service loop.
- [ ] Check clearances against every swept volume.

Exit: the wiring can exist without unmodelled empty space.

### Phase 6 — Ballast and mass

- [ ] Build the ballast bay with independent `x` and `h`.
- [ ] Add the head dummy with pose extras.
- [ ] Populate the mass register and generate CoM, tip, skid, and support-triangle outputs across the load cases.

Exit: CoM is an instrument-driven output, not an assumption.

### Phase 7 — Review and propagation

- [ ] Generate all views and run all checks.
- [ ] Review fabricated parts for printability and purchased envelopes for provenance.
- [ ] List every remaining `U` and placeholder explicitly.
- [ ] Propagate accepted geometry per §15.

Exit: the rig can be built and measured from this model, and nothing is claimed that was not modelled.

### Deferred until a gate freeze exists

Shell surfacing, cosmetic cues from the concept renders, panel seams and grilles, integrated whole-body packaging, and final chassis CAD. Those belong after G01–G06 and, for integration, to **RP-06**.

---

## 17. Definition of done for pass 1

Pass 1 is complete when:

- the model is on the **axle origin**, and every output is expressed in it;
- the ball transfer and the caster both install on one mount at the same contact `x`, both swept through 360°;
- the rear skid is present, adjustable across its bands, and its inequality is checked at the scored CoM;
- the battery volume is forward of the axle and an aft fit is geometrically impossible;
- the ballast bay moves CoM in `x` and `h` independently;
- all three look-downs, the analog-IR, the bumper, and the IMU are placed from **contact** datums;
- every purchased item is a labelled class envelope with a capture class, and no lead is labelled frozen;
- the drive mass row, the overall envelope, and the ground clearance band all pass;
- the `U` register is visible and unclosed rather than modelled around;
- checks pass with no zero-mass installed item and no undocumented placeholder;
- no gate result, no ADR closure, and no purchase is claimed anywhere in the output.
