# RP-03 Part Research

| Field | Value |
|---|---|
| Status | **Paper research v0.3 — 2026-09-19.** Constraints, inventory, filled envelopes, and print-vs-buy in one file. No SKU freeze. No purchase. No CAD blockout |
| Created | 2026-09-19 |
| Owner | Project builder |
| Consumes | `intent.md`; `physics.md`; `concepts/`; `drivetrain-screen-01.md`; `sensing-screen-01.md`; `base-control-architecture.md`; `rig.md`; `decision.md` BD-01…08 |
| Method | Datasheet / vendor pages (Oz, NFP, Vishay, Sharp, TI, Pololu, Alwayse, Robu, Zbotic, Fab.to.Lab). India stock is a class snapshot, re-check before any later buy |
| Feeds | Ugly CAD envelopes in the RP-06 CAD folder; dated snapshots into [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md) §Drive & base |
| Does not contain | A buy list; a second sourcing matrix; a motor/sensor SKU freeze; a pass against `2.0 m/s²`; pretty-chassis CAD |
| Replaces | `research-criteria.md` v0.2 and `research-findings.md` v0.1 (merged) |

This file exists so research and CAD start from **the same constraints**, not from a catalog page. Screens already named class leads (`D02`, `D21`, `DRV-B`, `S01`/`S04`/`S06`/`S07`). Research here is: *what envelope, interface, mass and keep-out that class must have before a blockout is honest* — then the filled rows from the 2026-09-19 paper pass.

Three findings change the rig drawing **before** any solid is pretty:

1. **Axle height vs front support.** Ø84 wheels put the axle at **42 mm**. A 1″ ball caster sits at **~29 mm** overall (Pololu). A 30 mm swivel caster sits at **~38 mm**. The interchangeable mount must **shim or drop the deck 4–13 mm**, or the robot sits on the wheels with the front support in the air.
2. **`D10` Ø84 × 21 mm is not a stock India article.** Closest classes are 83×35 (too wide), 80×10 with 4 mm D collet (too narrow), or 84×24 skate + 608 + 4 mm adapter (best diameter, extra hub). **Print the hub/adapter. Buy the tread.**
3. **India does not currently list the D02 encoder 176 RPM suffix.** Robu `25GA-370` 6 V 130 RPM has **no encoder**. Zbotic encoder listings that appeared are **26 RPM** (P02 fail). The reference-unit class is still NFP / Aslong / Oz **import**. Do not print a motor.

---

## 0. How to use this file

1. Read **§1** before opening a datasheet, a vendor page, or a slicer.
2. Research one **ID** at a time against **§2**. A row that cannot fill §2 is `U`, not a candidate.
3. Put landed cost, stock and substitutes in the **programme matrix**, not here.
4. CAD pass 1 may consume **envelopes and datums** from filled §4 rows and **§5**. It may not consume a SKU as frozen geometry.
5. A miss iterates the article, the mount, or a **printed adapter**. It does not quietly shrink storyboard `a_peak`, weaken follow ≤ 0.50 m/s, hide a stop-path sensor behind an expander, or substitute an FDM tyre / printed ball for a scored article.
6. **Lead** in a filled row = current path for CAD envelope, not a buy.

Conversion used: `1 kg·cm = 0.0981 N·m`.

---

## 1. Research constraints — apply to every row

These are inherited. Research does not re-derive them. A candidate that needs one of them to move is not an RP-03 finding; it is a baseline revision.

### 1.1 Authority and evidence

| Rule | Meaning for research |
|---|---|
| This is not a purchase | A filled row is still a class. Builder buy is a separate authorization (`decision.md`, matrix) |
| Do not fork sourcing | Quote India class, suffix risk and ₹ bands into `candidate-sourcing-matrix.md`. Do not keep a price table here |
| `W` / `D` / `E` / `U` | Manufacturer table is `D`. Envelope from a photo is `E`. Missing trail, CPR location, stall, or SPI pins is `U` — never silently zero |
| Leads are not freezes | `D02` / `D21` / `DRV-B` / `S01`/`S04`/`S06`/`S07` are the current path. `D20`, `D03`, QRE1113, MPU-6500-if-SPI stay live substitutes |
| Screen the range | `a_tip` is **0.9–1.9 m/s²** under Layout 03 lumps, negative if the battery is on/behind the axle. Do not research motors against `1.98 m/s²` as if it were the robot |
| HAT must not choose sensors | A driver board with “cliff” headers is a reject for ADR-07. Pin map v0.1 already owns C3 I/O |
| Print does not freeze | A printed adapter is geometry. It is not a motor SKU, a `D10` freeze, or a G01 pass |

### 1.2 Geometry envelope (CAD cannot violate)

Origin: floor, drive-axle ground-contact line. `+x` toward the front support. `+h` up.

| Constraint | Value | CAD / research implication |
|---|---|---|
| Overall envelope CON-14 | **300 H × 205 W × 180 D mm** (rounded target) | Nothing purchased or printed may require a larger stance without a baseline revision |
| Track | **170 mm** centre-to-centre | Motor bodies, wheels and brackets must clear each other at this spacing |
| Wheelbase `L` | **105–115 mm**, **110 mm** target, axle to **front-support ground contact** | Mount is adjustable. Instantaneous `L` on a trailed caster is `L ± trail`, not frozen 110 |
| Drive wheels | **Ø84 mm** nominal (Ø80–85 ok), **~21 mm** tread | Hub must match the motor shaft. Loaded radius 41–42 mm is a log, not a G02 retarget |
| Front support (V1) | **`D21` Ø1 inch ball transfer** (BD-08) | Type selected. SKU open. Cup + deck must clear battery tray and three look-downs |
| Front support (required swap) | **`D20` Ø25–32 mm swivel**, trail **10–18 mm** target | **Same pocket.** CAD that only fits the ball has not researched the swap |
| Rear skid | Reach **60–80 mm**, height **8–16 mm**. Inherited 70 / ≤14 is **not frozen** | Recompute `h/d < x/h` at the scored CoM. 14/70 fails every lumped Layout 03 CoM unless ballast restores `x` |
| Shell ground clearance | **~25–35 mm** | Cliff carriers and bumper live in this band; they must not become a fourth “skid” |
| Neck void | Centreline trunk; **demate at the body** | No slip ring. No motor current in a servo-style daisy chain |
| Battery bay | **Low and forward of the axle.** Pack CoM target band `x = +50…+80 mm`, `h = 18–32 mm` `E` | **HIGH_AFT is forbidden.** A part that only fits behind the axle is not a candidate |
| Drive mass row | **200–600 g** for motors + wheels + support + skid + brackets + driver share owned by drive | Physics does not enlarge this. 37D-class eats it. Printed hubs/adapters count here |

### 1.3 Motion and electrical (research cannot weaken)

| Constraint | Value | Research implication |
|---|---|---|
| Follow ceiling | **≤ 0.50 m/s** | Hard. Analog-IR must cover `d_stop` at this speed from **front contact** (179 mm level; 221 mm on 2.0° downhill) |
| Commanded spin | **180–220 °/s**; 300 °/s is never commanded | Scrub and front-support drag are continuous loads, not transients |
| Authored `a_peak` | **0.80 / 1.00 m/s²** | Has paper margin only if `x_CoM ≳ +20 mm`. Do not pick a weaker motor and then cut `a_peak` to match |
| Creep | **0.04 m/s** | Encoder must resolve ≲ 2 mm/count and ≳ 20 counts/s. 12 CPR **at the wheel** fails |
| Wheel torque class | **0.036 / 0.063 / 0.110 N·m** low/nom/high launch `E` | Stall `D` ≥ 0.220 N·m and rated ≥ 0.063 N·m (P01) |
| Unloaded design RPM | **160–200** at Ø84 / 6 V case | 0.70 m/s = 159 RPM. Set B 133 RPM is a comparison HOLD, not a silent retarget |
| Bus | **2S-class 6.0–8.4 V** onto `PB-DRIVE` in Set A | No motor-domain buck in the lead set. 8.4 V no-load on D02 class ≈ 1.08 m/s → C3 clamp at 0.70 is mandatory |
| Per-motor current | **1.5–3 A class `E`**; Korad **5 A** both-motor ceiling | Oz 0.90 A vs NFP ≤ 3 A is a **cited conflict**, not an average. Meter the article |
| Regen | Signed, separately observable L and R | Unsigned sense that folds regen into “less traction” is reject |
| Stop-path latency | **≤ 50 ms** detection-to-decel | Score with 50 ms, not the 35 ms paper sum. I2C-only is not a stop-path |
| C3 I/O | Pin map v0.1; **≥ 2 spare safe GPIO**; no stop-path on an expander; no safety **output** on GPIO0/3/45/46 | A fourth cliff that spends the spare is a Part 4 change, not a silent add |

### 1.4 What research is for (CAD vs buy vs gate)

| Output | Allowed from research | Not allowed |
|---|---|---|
| CAD pass 1 | Bounding box, mount holes, shaft, cable exit, 360° keep-out, mass/`(x,h)` lump `E` | Pretty shell; frozen SKU solids treated as the robot |
| Print | Adapters, shims, clamps, frame, carriers (see §1.5) | A printed substitute for a scored rolling element, motor, or stop-path sensor |
| Matrix | Dated India class, suffix risk, ₹ band, substitute | Purchase authorization |
| Screens | Confirm or HOLD an existing `D*` / `S*` / `DRV-*` row | A new architecture because a HAT was in stock |
| Gates | Nothing. Thresholds freeze in `gates.md` before data | A paper PASS used as G01 |

### 1.5 Print versus buy

Print the **interfaces and missing geometry**. Do not print the parts the screens actually score.

**Already supposed to be printed** (never catalog SKUs): `R-FRM`, `R-CLP`, `R-BAY`, `R-HDUM`, `R-INT`, `R-CUE`, `R-CHK`, bumper bar, skid carrier, and the front-support **drop/shim** (`R-MNT`) that eats the 4–13 mm height gap.

| Catalog gap | Print | Buy and keep |
|---|---|---|
| Ø84 × 21 wheel not in stock | Hub / D-bore adapter / 608 carrier so a bought tyre sits on the 4 mm shaft | The **tread**. PU skate 84×24, Pololu 80×10, or an India 83 mm tyre |
| Ball 29 mm vs axle 42 mm | Drop-deck or shim + Pololu 3-hole adapter | The 1″ **POM ball** |
| Caster 38 mm vs axle 42 mm | Same shim stack, 33×38 plate adapter | The swivel wheel + its bearing |
| Gearbox radial unpublished | Clamp that holds two 608s so the shaft is not a cantilever | The motor |
| No India D02 encoder SKU | Nothing | The **import** motor |

**Do not print as a substitute:** motors, encoders, DRV8874, TCRT / GP2Y / IMU, the ball itself, or a caster fork treated as the `D20` comparison. A printed cup or printed swivel bearing will fail `S-LAM` dent, `S-RUG` jam, trail/flutter, and `C_rr` in ways that do not teach you about the V1 article.

A **full TPU tyre** is a rig experiment, not the missing SKU. The baseline already allows TPU tread, but FDM wheels usually miss runout ≤ 0.5 mm, squash the loaded radius (which moves the 42 mm axle vs the 29 mm ball), and go slick or oval under `BM-06` scrub. Slick PLA / PETG / ABS rims are reject. If a tyre is printed at all, it is a bonded TPU tread on a concentric hub with a **metal D-insert or 608s** — and loaded radius is calipered before the shim stack is trusted.

Honest path: import the encoder motor, buy a PU wheel in the Ø80–85 band, print the hub + 0–15 mm front-support adapters. That closes the Ø84×21 hole. It is not a printed robot.

---

## 2. What a complete research row must capture

Copy this checklist onto every ID below. If a cell cannot be filled from a datasheet or a measured article, write `U` and name what it blocks.

| Capture | Why CAD / the rig needs it |
|---|---|
| **Envelope** | Max L × W × H, and which corner is the origin. Including cable strain-relief, not the pretty body |
| **Mass** | Article mass `D` or weighed `W`. Two-of on the drive row |
| **CoM in part frame** | Even a crude `E`. Battery, motors and front support move whole-robot `x,h` |
| **Mounting** | Hole pattern, shaft diameter/type (D-shaft 4 mm vs 6 mm), stack height from deck to contact |
| **Motion keep-out** | Ball/caster **every azimuth**; bumper travel; wheel radial/axial load path |
| **Interface** | Voltage, pinout, logic level (3.3 vs 5), encoder CPR **and whether it is motor-side**, SPI vs UART, ADC vs GPIO |
| **Cable exit** | Side, length to the neck void, cannot cross a wheel or the ball cup |
| **Failure mode** | Dent, jam, flutter, dark/glossy, stall-current conflict, backdrive, shaft walk |
| **Receiving check** | Photograph / continuity / RPM / PPR / SPI pins **on the article**, not the category photo |
| **Service** | Comes off without moving ballast bays or the opposite wheel |

---

## 3. RP-03 inventory

IDs are research rows, not SKUs. **Lead** = current path. **Swap** = must still fit. **Fab** = printed/cut here. **Else** = owned in RP-02 / workbench / matrix; criteria only, no second screen.

Filled capture is **§4**. Remaining `U` is **§6**.

### 3.1 Drive — purchased class

| ID | Part | Lead / status | Research criteria (must-pass) | CAD must have | Reject / HOLD if |
|---|---|---|---|---|---|
| `R-MTR` | Two encoder gearmotors | Lead `D02` JGA25-370-class 6 V ~176 RPM 1:35, 4 mm D-shaft, AB Hall. Comparison `D03` 1:45 | P01 stall ≥ 0.220 N·m and rated ≥ 0.063; P02 160–200 RPM at the voltage used; P04 motor-side CPR × ratio ≲ 2 mm/count; body Ø fits 170 mm track with Ø84 wheels | Gearbox length, shaft stick-out, encoder cap, cable exit, clamp lands. Radial load at 8–10 mm ≥ ~8 N `E` or add a bearing | N20 14–15 RPM or 5:1; wheel-only 12 CPR; 37D pair (mass); 12 V box silently dropped onto 2S; **printed gearbox** |
| `R-ENC` | Quadrature encoder (usually on the motor) | Included with `D02` class: ~11 PPR motor-side × 35:1 ≈ 385 CPR | 3.3/5 V Hall A/B; CPR **location stated**; ~58 counts/s at 0.04 m/s | Connector and keep-out behind the clamp | CPR at the wheel; encoder omitted to “save mass” |
| `R-WHL` | Two Ø84 × 21 mm wheels | `D10` rubber/TPU, **4 mm D-hub** matching JGA25. Exact 21 mm tread **not a stock article** — see §4 `R-WHL` | Moderate grip; runout ≤ 0.5 mm radial; D-bore + set-screw on the flat or collet; axial walk under spin is a fail | Tread OD, hub length, dish vs motor, scrub volume in a 180° pivot | Slick PLA/PETG/ABS rims; **FDM tyre as a D10 freeze**; 6 mm hub without adapter mass in 200–600 g |
| `R-HUB` | Shaft retention / optional bearing | HOLD on the mount today. **Print** the carrier; **buy** 608s / D-insert | D-shaft retention under `BM-06` scrub; extra radial bearing if gearbox `D` radial is unpublished | Bearing bore, offset from housing, does not grow track past 205 mm | Set-screw-on-round as the production path |
| `R-DRV` | Two brushed H-bridges | Lead `DRV-B` DRV8874-class, **one chip per wheel** | nFAULT, per-channel current (IPROPI or documented signed path), enable **pull-down to inhibit**, commanded brake (not only coast), 6.0–8.4 V, stall class 0.9–3 A | Board/IC envelope in the **body**, not the tub; sense resistors; logic vs motor cavity barrier | TB6612 as installed if stall ~3 A; Cytron MDD3A as installed freeze (bench-only); unsigned sense; driver HAT that freezes cliffs |

### 3.2 Support — type selected, SKU open

| ID | Part | Lead / status | Research criteria | CAD must have | Reject / HOLD if |
|---|---|---|---|---|---|
| `R-BALL` | Ø1" ball transfer | **BD-08 selected V1** (`D21`). Not a SKU | Starting force ≤ 2 N at contact; cup takes residual front share; no-trail (contact stays at `+L`); rolling resistance bounded before claiming extra torque margin | Cup depth, flange, deck cut-out, hair/grit access, height vs skid, **360° clearance vs battery tray, look-downs, Ø84 tyre** | Treating selection as a G01 pass; importing Concept B bump-only stop; a cup that makes HIGH_AFT the only battery fit; **printed ball / printed cup as D21**; Robu 15.9 mm steel “caster” |
| `R-CAS` | Ø25–32 mm swivel caster | **Required swap** `D20` on the **same mount** | Trail 10–18 mm (`< 8 mm` HOLD flutter); 360° fork; flutter screen at 0.50 m/s on tile/laminate (Ø30 → ~318 RPM) | Fork swing volume, trail as a function of azimuth, instantaneous `L` | CAD pocket that only accepts the ball; trail `U` presented as measured; **printed fork treated as the D20 comparison** |
| `R-MNT` | Interchangeable front-support mount | **Fab.** Two adapters + 0–15 mm shim | Swap ball ↔ caster **without changing** the 105–115 mm contact number just set; look-down #1 stays with the carrier | Datum at **ground contact**, not the fork crown; lockable mm scale | Two different wheelbases after a swap |
| `R-SKID` | Rear anti-tip skid + pad | `D30` polymer or PTFE pad, printed carrier | Catch only (`N_skid = 0` in the normal pose); adjustable 60–80 × 8–16; pad must not shear; reverse cliff sees this contact | Reach/height screws, lock, pad area, look-down #2 carrier | Frozen 14 mm @ 70 mm; a pretty tab; skid used as a fourth load wheel |

### 3.3 Sensing — stop-path vs telemetry

Stop-path: native GPIO or C3 ADC. **Never I2C-only. Never expander.** Unknown = inhibit.

| ID | Part | Lead / status | Research criteria | CAD must have | Reject / HOLD if |
|---|---|---|---|---|---|
| `R-CLF-F` | Look-down, front | `S01` TCRT-class × **floor-present ~40 mm before ball contact** | GPIO; useful standoff ~2–8 mm for TCRT; **dark+glossy trial is mandatory**; pulsed emitters vs `LG-10` | Patch pose relative to **contact**, not to the axle; no view of the catch lip | VL53 as the cliff; one forward-only channel for the whole robot |
| `R-CLF-L` | Look-down, lateral | Same class, wheel-adjacent | Covers shoulder during 220 °/s pivot (~102 mm sweep) | One wheel-adjacent minimum; does not collide with Ø84 at lock-to-lock | Spending spare GPIO on a 4+ ring without a Part 4 change (that is Concept B) |
| `R-CLF-R` | Look-down, rear | Same class, skid-leading | Valid **before** reverse travel (`BM-08`) | On the skid carrier so coverage does not walk when reach is adjusted | Forward-only cliffs used as reverse permission |
| `R-IR` | Analog-IR obstacle | `S04` GP2Y-class 4–30 cm, **at front-support contact** | ADC stop-path; look-ahead ≥ **179 mm** at 0.50 (PASS if contact-mounted); 221 mm on 2° downhill HOLD; 289 mm at 0.70 HOLD; cycle ~16.5 ms; 4.5–5.5 V with documented divider to C3 | Optical axis `+x`; min range 40 mm (bumper owns nearer); not buried in the ball shadow | Axle-mounted credited as leading-contact; ToF as sole obstacle; GP2Y used as a cliff |
| `R-BMP` | Stance-spanning bumper | `S06` lever / microswitch, direct GPIO. **Bar printed**; switch bought | Last layer; spans **205 mm** stance; safe-level on any contact; travel/height `U` until rig | Lever path vs ball/caster 360°; one centre button is not this part | Closing G03 with bump-only at follow speed |
| `R-IMU` | Base IMU | `S07` ICM-42688-class **SPI + INT1** | Rigid **base** mount; data-ready interrupt; not a cliff | Keep-out, SPI run length, not in the head | UART-angle modules (601N1 class); I2C-only breakouts; head mounting |
| `R-TOF` | Forward ToF | Optional `S05` telemetry | I2C only; **not** stop-path; only if spare GPIO/bus rule still holds | Must not steal analog-IR’s contact mount | Wired as the sole inhibitor |

### 3.4 Power, control, harness on this chassis

C3, watchdog, link PHY, E-stop **operator**, motor-arm **stage**, and pack chemistry are **RP-02 / workbench** rows. Research here is only what the **base** must reserve.

| ID | Part | Owner | Research / CAD criteria |
|---|---|---|---|
| `R-C3` | ESP32-S3-DevKitC-1-N8 | Selected (RP-02). On the **body**, not the tub | Header keep-out; USB-UART service (`GPIO43/44`); strapping 0/3/45/46; N8R8 is not a silent substitute |
| `R-EST` | Motor-bus E-stop sense | Operator SKU is `PCD-EST-01` elsewhere | `ESTOP_N` is GPIO3 **input-only**; cuts `PB-MOTOR`, not logic; release does not restart |
| `R-ARM` | Motor-arm / `nSLEEP` | `PCD-EST-02` elsewhere; C3 enable on GPIO21 | Fail-safe **inhibit** on a broken loop; normally-off |
| `R-INA` | Signed L/R current | Rig instrument until IPROPI on a spare | High-side, signed regen visible; not on the MCU in pin map v0.1 |
| `R-WDI` | Window-watchdog feed | TPS3436-Q1 family elsewhere | GPIO48 `WDI`; READY is a **carrier** function, not a C3 GPIO |
| `R-LNK` | C0↔C3 differential UART | THVD1451D lead elsewhere | GPIO17/18 behind the transceiver; TTL is bench-only |
| `R-SAFE` | `PB-SAFE-BASE` | RP-02 PA-11 | Cliffs/bump/IMU must not back-power a dead branch; off in charging |
| `R-HARN` | Neck-void trunk + body demate | RP-02 connector family | Keyed, not Dupont; motor cavities isolated from 3.3 V; strain relief both faces; service loop on the chassis |
| `R-BATT` | Pack **or** mass dummy | Chemistry ADR-06 open | Dummy/pack CoM **low, forward of axle**; HIGH_AFT physically **unfittable**; 150–500 g band |

### 3.5 Fabricate — CAD owns these (not a catalog SKU)

| ID | Part | What it must do | Research / DfAM criteria |
|---|---|---|---|
| `R-FRM` | Open axle frame | 170 mm track; does not change stiffness when ballast moves | Ugly rig, not a mini-droid. Print or plate. Wheel stops for bench so it cannot walk off a desk |
| `R-CLP` | L/R motor clamps | Axle-centred; service one motor without dropping the battery tray | Independent L/R; takes radial tyre load or hosts `R-HUB` (608s bought, carrier printed) |
| `R-BAY` | Forward battery / ballast bay | Independent **`x` slide** and **`h` stack**; BD-05 1.65 kg and 3.10 kg+head | Changing a wheel must not be how CoM is “tuned” |
| `R-HDUM` | Head-mass dummy | Layout 03 ~499–524 g at ~250–255 mm CoM height; pose extras `HP-PITCH-FWD/AFT`, `HP-YAW-L/R` | A 304 mm stick is **not** BD-05. Pitch lever ~52 mm `E` |
| `R-INT` | Sensor interposer | Mask / freeze / corrupt **one** stop-path channel for `F-19` | Logged timestamp; not casual unplug |
| `R-CUE` | Status-light timing cue | In the top-down camera view | Co-visible with the chassis; not the DevKit RGB (GPIO48 is `WDI`) |
| `R-CHK` | Wheel chocks | Unpowered 35:1 **will roll** | `BM-00` is not a mechanical brake |
| `R-ADP-BALL` | Pololu 3-hole drop adapter | Lands 1″ POM caster at loaded wheel radius | Native height ~29 mm; shim 0–15 mm. Does not replace the ball |
| `R-ADP-CAS` | 33×38 caster-plate adapter | Same contact datum as the ball adapter | Trail still measured on the **bought** fork |

### 3.6 Rig environment — required to move, not on the vehicle BOM

| ID | Part | Criteria |
|---|---|---|
| `R-PSU` | Korad KA3005D (workbench) | 5 A ceiling; Phase B stall **per motor**; limit set before first power-up |
| `R-CRS` | Marked floor course | `S-TILE` / `S-LAM` / `S-RUG` / `S-THR`; speed marks 0.15 / 0.40 / 0.50 (0.60 exploratory) |
| `R-PRP` | Obstacle props | Person-leg proxy, furniture leg, box, cable/flat; **20 mm cube** in the front-support shadow |
| `R-CAT` | Tabletop catch | Overhead tether primary (BD-07). **No uncaught trial.** Catch must not sit in cliff FoV |
| `R-2DEG` | 2.0° ramp board | G01 condition, not a fifth floor |

---

## 4. Filled capture — 2026-09-19 paper pass

### 4.1 Drive

#### `R-MTR` — two encoder gearmotors (lead `D02`)

**2026-09-26 decision update:** This 2026-09-19 capture is the reference-class screen. [Pololu #4804](gearmotor-sku-decision.md) is the preferred prototype candidate: HP 6 V / 34.014:1 / encoder, 290 rpm no-load and 6 A extrapolated stall. Fab.to.Lab lists it in India, but exact-variant stock is unverified; **no SKU is locked**. NFP `-EN-0685` remains a comparison with no verified India source. The 176 rpm / 0.9 A `D02` table below is a different winding; do not use those values for either candidate. Current-limit, geometry and bench proof remain open.

| Capture | Finding | Class |
|---|---|---|
| Envelope | Gearbox **Ø25 mm**, length **21 mm** at 35:1 / 34:1 / 45:1. Motor can **~30.8 mm** + gearbox (`D`, NFP). Total length along axis **~52 + L mm** (Bringsmart) → **~73 mm** at L=21 **before** encoder cap. Encoder cap **+10–15 mm `E`**. CAD keep-out cylinder **Ø28 × 90 mm** including cable pigtail | `D` / `E` |
| Mass | **~110 g** with encoder (NFP). ~85 g listed without encoder — do not use that number. Two motors **~220 g** | `D` |
| CoM | Gearbox + motor roughly on axle, `x ≈ 0`, `h ≈ 42 mm`. Encoder mass is inboard if the gearbox faces the wheel | `E` |
| Mounting | **4 mm D-shaft**, length **10–12 mm**, D-flat **~8 mm** (NFP 59 mm-type). Face **two M3**, spacing **19 mm `E`** (Electra; confirm on the article). Commodity L-bracket 26 × 34 × 33.5 mm exists; RP-03 still wants an axle-centred **printed clamp** that takes radial load | `D` / `E` |
| Motion keep-out | Two Ø25 bodies on 170 mm track: **~120 mm** between cans before clamps. Radial load at 8–10 mm from housing vs `N_wheel ≈ 11 N` at 2.4 kg is **HOLD** — gearbox `D` radial unpublished | `E` |
| Interface | 6 V winding for Set A. 8.4 V no-load scales ~1.4× → **~1.08 m/s** on Ø84; C3 clamp at 0.70 remains mandatory. Encoder: see `R-ENC` | `D` |
| Cable exit | PH2.0 / 6-pin class, ~140 mm pigtail on some 25GA encoder articles (`D` Zbotic 12 V). Route **inboard then up the neck**, not across the tyre | `E` |
| Failure | **P03 stall conflict stands:** Oz/Aslong 6 V 176 RPM stall **900 mA / 0.490 N·m**; NFP 6 V 34:1 stall **≤ 3 A / 0.441 N·m**. Do not average. 35:1 is **backdrivable** — active hold | `D` |
| Receiving | Photograph suffix; **no-load RPM at 6.0 V**; stall current on a current-limited supply; D-shaft vs round; encoder magnet count; gearbox length 21 mm | — |
| Service | Outboard clamp; opposite wheel stays | — |
| Print | Clamp and optional 608 carrier only. **Do not print the motor** | — |

**Paper vs P01/P02 (unchanged, confirmed):**

| Table | No-load | Rated τ | Stall τ | Stall I | P01 | P02 |
|---|---:|---:|---:|---:|---|---|
| Oz/Aslong 6 V 1:35 | 176 RPM | 0.085 N·m | 0.490 N·m | 0.90 A | Pass | Pass |
| NFP 6 V 34:1 | 175 RPM ±15 % | 0.128 N·m | 0.441 N·m | ≤ 3 A | Pass | Pass |
| NFP / Oz 45:1 (`D03`) | 130–133 RPM | 0.108–0.177 N·m | 0.589 N·m | 0.90 A / ≤3 A | Pass | **HOLD** (below 160; still > follow 0.50) |

**India 2026-09-19:** Robu `25GA-370-6V-130 RPM` SKU 473400: 89 g, 4 mm shaft **9.4 mm**, rated 0.8 kg·cm, stall 4.4 kg·cm, **no encoder** — not D02. Zbotic encoder 25GA rows that surfaced are **26 RPM**. Exact 6 V ~170 RPM encoder suffix **`U` in India**. Import path: NFP-GM25-370-EN or Aslong JGA25-370B 6 V 176 RPM 1:35.

CAD STEP exists for *a* JGA25-370 (NXP Cup `114090046`); treat as class geometry, not the purchased winding.

#### `R-ENC` — AB Hall on the motor

| Capture | Finding | Class |
|---|---|---|
| Envelope | Magnetic disc on the **motor** can, behind the gearbox. Connector PH2.0 or ZH2.0-6 | `D` |
| Interface | **11 PPR motor-side** × ratio. 35:1 → **~385 CPR** (Oz class) / 34:1 → **374.11 PPR** (NFP). 3.3 / 5 V, built-in pull-ups, 100 kHz. Typical 6-pin: M+, M−, GND, VCC, A, B (colour `U` until the article) | `D` |
| Creep | 0.04 m/s → **~58 counts/s**, **0.69 mm/count** — P04 pass **if** 11 PPR is motor-side | `E` |
| Reject | 12 CPR **at the wheel**; encoder omitted; 26 RPM encoder SKU | — |

#### `R-WHL` — Ø84 × 21 mm class (`D10`)

**No exact Ø84 × 21 mm 4 mm D-hub article found.** Three envelopes for CAD; pick one family before printing hubs. Print closes the **hub**, not the missing tyre SKU.

| Envelope | Ø × width | Hub | Mass | Stance vs 205 mm | Notes |
|---|---:|---|---:|---|---|
| **A — India toy (common)** | 83 × **35** mm | 4 mm **round** hole, not D | 54 g | Track 170 + 35 = **205 mm** — fills CON-14 with no shell margin | Extra scrub vs 21 mm spec. **Printed D-adapter** still required |
| **B — Pololu multi-hub** | **80 × 10** mm | 4 mm **D collet** (also 3 mm) | `U` pair | Narrow tread; Ø80 is in Ø80–85 | Best shaft retention story. Speed +4.8 % vs Ø84 kinematic |
| **C — skate + adapter** | **84 × 24** mm PU | **608** bore + Pololu 4 mm scooter adapter **or printed 608 carrier** | 90 g wheel | Width 24 ≈ spec 21 | **Best diameter match.** Forces `R-HUB`. Adapter mass in 200–600 g |

| Capture | Finding | Class |
|---|---|---|
| CAD must have | Tread OD, width, dish, hub stick-out past the D-shaft (only 10–12 mm of shaft exists) | — |
| Failure | Set-screw on round (India 83 mm). Axial walk in `BM-06`. 35 mm tread continuous scrub. FDM ovality if the whole tyre is printed | — |
| Receiving | Caliper Ø and width on the article; D vs round; runout ≤ 0.5 mm; **loaded radius before trusting the 0–15 mm shim** | — |
| Print | Hub / D-insert carrier / 608 carrier. Full TPU tyre = experiment only, not a freeze | — |

**CAD recommendation (not a freeze):** envelope **C** if radial load is solved with 608s; envelope **B** if we accept Ø80 and 10 mm tread; do **not** draw 21 mm as if it were in the drawer.

#### `R-HUB` — retention / radial bearing (HOLD)

| Capture | Finding | Class |
|---|---|---|
| Envelope | If skate wheel: two **608** (Ø22 × 7 mm) per wheel + 4 mm adapter. If D-collet: Pololu collet stack **~6 mm**, wants shaft ≥ 7.5 mm — NFP 10–12 mm **clears** | `D` |
| Why it exists | Gearbox radial `U`. NOM wheel load ~11 N on an 8–10 mm stub is tight | `E` |
| Print | 608 / D-insert **carrier**. Bearings and metal inserts are bought | — |
| Reject | Set-screw-on-round as the production path | — |

#### `R-DRV` — two DRV8874-class (`DRV-B`)

| Capture | Finding | Class |
|---|---|---|
| Envelope (bench carrier) | Pololu #4035: **15.2 × 17.8 mm**, 0.9 g, 0.6″ × 0.7″. CAD pair + wiring: **two 20 × 20 × 12 mm** keep-outs in the **body** | `D` |
| IC | HTSSOP-16 **5.00 × 4.40 mm**, 4.5–37 V | `D` |
| Interface | PH/EN or PWM; **nSLEEP active-high enable** (pull-**down** to inhibit — matches pin map GPIO21); **nFAULT**; **IPROPI** analog. Logic 1.8–5.5 V. Pololu current sense **1.13 V/A**; default chop ~**4.4 A** with 5 V on SLEEP | `D` |
| Current | 2.1 A continuous / 4.4 A peak on the carrier — covers both 0.9 A and 3 A stall articles. Two chips, not one dual | `D` |
| Body rule | Not a HAT with cliff headers. Motor copper isolated from 3.3 V | — |
| HOLD | TB6612 if stall ~3 A. Cytron MDD3A = Phase A eval board only | — |
| Print | Standoffs / body pocket only | — |

### 4.2 Support

#### `R-BALL` — Ø1″ ball transfer (BD-08, `D21`)

**Do not CAD the common Robu “metal ball caster.”** That article is a **15.9 mm (5/8″)** steel ball, 21 mm tall — not D21. **Do not print the ball.**

| Envelope candidate | Ball | Overall height | Mass | Mount | Floor note |
|---|---|---:|---:|---|---|
| **Pololu 2691 / 2692** (CAD lead) | **1″ POM** plastic, 3 rollers or 3× 608 | **29 mm** (1.10″) | 16.5 / 18.5 g | 3× M3, hole span **12.2 mm** (0.48″) | Plastic ball is the **dent** preference on `S-LAM`. Rated ~10 lb robot — HIGH 3.62 kg is inside on paper |
| Alwayse 1010 flange (industrial) | 25.4 mm steel / nylon / SS | Working ht **15.4 mm** below flange; body Ø **36.8**; flange **73**; seating hole **50** | 195 g | Flange | 73 mm flange **fights** the forward battery bay in 180 mm depth. Nylon ball SKU exists |
| Clarke BT-1-CS | 1″ steel | **30.2 mm** (1-3/16″) | `U` | 2-hole flange, 55.6 mm spacing | 75 lb — overkill; steel dent risk |

| Capture | Finding | Class |
|---|---|---|
| Height vs axle | Axle **42 mm**. Pololu **29 mm** → **13 mm drop or shim**. Alwayse working 15.4 mm is a through-deck geometry, not a 42 mm stick-on | `D` |
| Keep-out | Sphere Ø25.4 + housing. Pololu housing is compact (~Ø32 `E`). **360°** vs battery tray, three look-downs, Ø84 tyre. No trail (`L` stays put) | `E` |
| Failure | Hair/grit in cup (`S-RUG`); laminate **dent** if steel; higher `C_rr` than an aligned caster `U` | `U` / `E` |
| India | Fab.to.Lab lists Pololu 1″ plastic. Robu 1″ **swivel nylon** (26 mm wheel, 33×38 plate) is a **caster**, not a ball transfer | snapshot |
| Receiving | Caliper ball Ø **25.4 mm**, not 16 mm. POM vs steel. Overall height vs the **actual** wheel loaded radius | — |
| Print | `R-ADP-BALL` only | — |

#### `R-CAS` — Ø25–32 mm swivel (`D20` required swap)

| Capture | Finding | Class |
|---|---|---|
| Envelope (common 30 mm robot caster) | Wheel **Ø30 × 13 mm**; plate **33 × 38 mm**; holes **30 × 23 mm** M4; overall height **38 mm**; load ~10 kg; nylon PP | `D` class |
| 25 mm variant | Ø25 × 12.4; plate 32×38; holes 30×25; height **34.5 mm**; **32 g** | `D` |
| Height vs axle | 38 mm vs 42 mm → **4 mm shim** (same mount as the ball must also eat the ball’s 13 mm) | `E` |
| Trail | **Not published.** Screen target 10–18 mm. Cheap offset forks are often **short-trail** → flutter HOLD if `< 8 mm`. Measure on the article: swivel-axis to contact | `U` |
| Keep-out | Fork + wheel **360°**. Instantaneous `L = 110 ± trail` | `U` |
| Flutter | Ø30 at 0.50 m/s → **~318 RPM** caster spin (`physics.md`) | `E` |
| Same pocket as ball | Plate 33×38 vs Pololu 3-hole ~12 mm span are **different**. The interchangeable mount is a **carrier + two adapters**, not one hole pattern | CAD |
| Print | `R-ADP-CAS` only. Do not print the fork as the scored `D20` article | — |

#### `R-MNT` / `R-SKID` — fabricate

| ID | CAD envelope to reserve | Why |
|---|---|---|
| `R-MNT` | Adjustable +x **105–115 mm** to **ground contact**; vertical shim **0–15 mm** to match loaded wheel radius; two drop-in adapters (Pololu 3-hole vs 33×38 caster plate) | Height mismatch and the two hole patterns |
| `R-SKID` | Pad area `E` 20×20 mm; reach 60–80; height 8–16; look-down #2 on the carrier | Unchanged. 14/70 still not frozen |

### 4.3 Sensing

#### `R-CLF-*` — TCRT5000-class (`S01`)

| Capture | Finding | Class |
|---|---|---|
| Envelope | **10.2 × 5.8 × 7.0 mm** (Vishay). Leads 3.5 mm (TCRT5000) or 15 mm (TCRT5000L). Two mounting clips | `D` |
| Optical | Peak **2.5 mm**; useful 0.2–15 mm; 950 nm; daylight-block | `D` |
| CAD | Three carriers: **~40 mm ahead of ball contact**, skid contact, one wheel-adjacent. Standoff **2–8 mm** to the floor. Not a ranger | `E` |
| Failure | **Reflectivity**, not geometry. Dark+glossy trial mandatory. Three emitters pulsed vs `LG-10` | `D` / `E` |
| India | Commodity on Robu | snapshot |
| Print | Three carriers / patches. Buy the optos | — |

#### `R-IR` — GP2Y0A41SK0F (`S04`)

| Capture | Finding | Class |
|---|---|---|
| Envelope | **29.5 × 13.0 × 13.5 mm**, **3.5 g**. Optical axis from datasheet drawing (not extracted as a number here — **keep the Sharp PDF on the CAD desk**) | `D` |
| Interface | Analog, **4–30 cm**, cycle **16.5 ± 3.7 ms**, 4.5–5.5 V, 12 mA typ / 22 mA max. Divider to C3 ADC documented | `D` |
| Mount | At **front-support contact**, looking +x. Covers 179 mm at 0.50. **HOLD** 221 mm downhill and 289 mm at 0.70 | `D` |
| Near lobe | Ambiguous **< 40 mm** — bumper owns that | `D` |
| CAD | Body 30×14×14 plus 10 µF on Vcc; must clear ball 360° and not stare into the floor | `E` |
| Print | Bracket on the front carrier | — |

#### `R-BMP` — spanning bumper (`S06`)

| Capture | Finding | Class |
|---|---|---|
| Switch | Miniature snap-action (KW11 / SS-5GL class) **~20 × 6 × 10 mm `E`**, direct GPIO | `E` |
| Bar | **Printed**, 205 mm stance, last layer. Travel `U` | fab |
| CAD | Lever vs ball/caster 360°. One centre button is not this part | — |

#### `R-IMU` — ICM-42688-P SPI (`S07`)

| Capture | Finding | Class |
|---|---|---|
| Silicon | LGA **2.5 × 3.0 × 0.91 mm** | `D` |
| Interface | 4-wire SPI + **INT1**. VDD 1.71–3.6 V class. Pin map already has GPIO35–37, CS 41, INT 42 | `D` |
| **Reject** | Robu **601N1**: 21×21 mm, **onboard MCU, UART angle**, 8 mA. Marketing name ICM-42688 is not the CA article | `D` |
| CAD | Rigid base, not head. Module envelope **`U` until a SPI breakout is named** — reserve **25 × 25 × 5 mm** | `E` |
| Receiving | Continuity: CS, SCLK, MOSI, MISO, INT1 are the **silicon** pins | — |
| Print | Base mount only | — |

#### `R-TOF`

Telemetry only. Not researched as stop-path. Do not steal the GP2Y contact mount.

### 4.4 Power / control keep-outs (owned elsewhere)

| ID | Envelope to reserve on the RP-03 chassis | Note |
|---|---|---|
| `R-C3` | DevKitC-1-N8 board **~69 × 25.4 mm `E`** plus USB | Selected. Body, not tub |
| `R-HARN` | Neck-void trunk; keyed demate; motor vs 3.3 V cavities | Connector family is RP-02 |
| `R-BATT` | Pack/dummy **low, `x > 0`**. Volume that only fits aft of the axle is illegal | Chemistry still ADR-06 |
| `R-INA` | Until IPROPI on a spare: two INA breakouts on `PB-DRIVE-L/R` | Rig |

---

## 5. CAD pass 1 — datum list

Pretty geometry still waits on a gate freeze. Working CAD lives in [`RP-06-cad/`](../RP-06-cad/README.md). Use this list, not napkin 110/14/21:

1. Ground plane; axle at **h = 42 mm**; track **170 mm**.
2. Wheel envelope: **Ø80–85 × 10–35 mm** until `R-WHL` family is chosen; do not solid a fake 21 mm tyre. Hub is printed; tread is bought.
3. Motor keep-out **Ø28 × 90 mm** each, gearbox outboard, encoder inboard, M3 face **19 mm**.
4. Front contact at **x = 105–115 mm**, with a **0–15 mm vertical shim** (`R-MNT`).
5. **Two** front-support adapters: Pololu 1″ 3-hole (29 mm native) and 33×38 caster plate (38 mm native).
6. Battery bay entirely forward of x=0; **73 mm industrial flange is not the first-fit** (too wide vs 180 mm depth + tray).
7. TCRT patches 10×6×7 at three contacts; GP2Y 30×14×14 on the front carrier.
8. Bumper bar 205 mm, inboard of tyre scrub.
9. Two DRV8874 carriers 20×20 in the body.
10. Skid 60–80 × 8–16, not a frozen 14/70 solid.

A 360° front-support sweep that only uses the straight-ahead pose has not been researched.

---

## 6. Still `U` (blocks a freeze, not a napkin)

| Item | Blocks |
|---|---|
| India SKU for 6 V ~176 RPM **with** encoder | Bench reference unit buy, if authorized. Print does not close this |
| D-shaft vs round on the wheel that is actually bought | Hub print |
| Caster **trail** millimetres | Flutter / `BM-07` heading |
| Ball `C_rr` and laminate dent of POM vs steel | D21 iterate-to-caster |
| Gearbox radial rating | Whether 608s are mandatory |
| SPI IMU **module** outline (not the 601N1) | Base keep-out |
| GP2Y optical-axis number from the PDF drawing | Exact look-ahead vs contact |
| Loaded wheel radius (squash) | Shim stack vs 42 mm |

---

## 7. Research order

Do not research drivers or ToF first. Geometry first, then stop-path placement, then body electronics.

| Step | IDs | Why this order |
|---|---|---|
| 1 | `R-MTR` `R-ENC` `R-WHL` `R-HUB` | Track, shaft, RPM, CPR, radial load — everything else hangs on this |
| 2 | `R-BALL` `R-CAS` `R-MNT` `R-SKID` | Contact datums and 360° keep-outs; CAD cannot start without both supports |
| 3 | `R-CLF-*` `R-IR` `R-BMP` | Coverage is millimetres from **contact**, not from a pretty bumper drawing |
| 4 | `R-DRV` `R-IMU` `R-C3` `R-HARN` | Fit the pin map and neck trunk after the chassis datums exist |
| 5 | `R-BAY` `R-HDUM` `R-BATT` | CoM lumps for the envelope model; still `E` until weighed |
| 6 | Matrix snapshot | Dated India class into `candidate-sourcing-matrix.md`, not a new table here |

Phase A bench (one reference motor + eval driver) may start at step 1 without a chassis. It produces **no** traction, scrub, lift, stopping or edge claim.

---

## 8. Explicit no-research / no-buy / do-not-print

Do not spend research time trying to make these fit:

1. N20 1000:1 / 14–15 RPM or N20 5:1 ~2500 RPM as the drive.
2. Wheel-only 12 CPR as the creep encoder.
3. 37D pair as the lead (eats 200–600 g).
4. Behind-axle battery to “make the motors fit.”
5. ToF or I2C as the sole cliff or sole obstacle stop.
6. GPIO expander in the stop path.
7. UART fused-angle IMU as the CA IMU.
8. Driver HAT whose cliff pins would freeze ADR-07.
9. Treating `D21` as ADR-04 closed or as a reason to drop analog-IR.
10. Quietly shrinking `a_peak` because a lumped CoM missed +25 / 124 mm.

Research-confirmed do-not-buy:

1. Robu `25GA-370` **without** encoder as D02.
2. Zbotic / any 25GA encoder at **26 RPM**.
3. Robu **15.9 mm** “metal ball caster” as D21.
4. Robu 601N1 UART IMU as S07.
5. Drawing a 21 mm tyre that is not on the bench.

Do-not-print as a scored substitute:

1. Motor, gearbox, or encoder.
2. The ball transfer or its rolling cup.
3. A caster fork presented as the `D20` comparison.
4. An FDM / PLA / PETG / ABS rim or a full FDM tyre treated as frozen `D10`.
5. DRV8874, TCRT, GP2Y, or IMU silicon.

---

## 9. Handoff

| Document | What it takes from this file |
|---|---|
| `drivetrain-screen-01.md` / `sensing-screen-01.md` | Confirm, HOLD, or add a dated `D`/`U` — do not invent a parallel screen |
| `candidate-sourcing-matrix.md` | India class, suffix, ₹, substitute — the only price/stock home |
| `../RP-06-cad/README.md` | Envelope/datum list in §5 when a blockout is actually authorized. Print adapters, not pretty shell |
| `rig.md` | Adjustable numbers that research proved must stay adjustable; print-vs-buy for the ugly frame |
| `decision.md` | Nothing until a freeze. This file does not issue `BD-` or a purchase |

Screens: no architecture change. P03 HOLD and analog-IR 0.70 HOLD stand.

---

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-19 | 0.1 | First research brief (`research-criteria.md`): global constraints, §2 capture checklist, RP-03 inventory, CAD datums, research order |
| 2026-09-19 | 0.2 | First findings (`research-findings.md`): drive/support/sensing envelopes; three CAD-critical mismatches |
| 2026-09-19 | 0.3 | Merged criteria + findings into this file. Added §1.5 print-vs-buy: print adapters/hubs/shims; import the encoder motor; buy the tread and the POM ball |
