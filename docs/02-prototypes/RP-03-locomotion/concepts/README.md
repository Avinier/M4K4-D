# RP-03 Concepts — Comparison Matrix

| Field | Value |
|---|---|
| Status | **Paper comparison v0.1. Not a selection, not a freeze, not a purchase.** Concept A is named as a working lead only after the matrix below is filled. Concept B is retained as a comparison and is not waived |
| Created | 2026-09-17 |
| Owner | Project builder |
| Governing plan | `../plan.md` Part 3; `../intent.md` ADR-04 / ADR-07 split |
| Consumes | `../physics.md` (ranges, not a point `a_tip`); `../storyboard.md` `BM-00…BM-12`; `../../01-system/dimensional-baseline.md` v1.10 |
| Feeds | `../drivetrain-screen-01.md`; `../sensing-screen-01.md`; later `../rig.md` (interchangeable front support) |
| Does not claim | A winner freeze; a motor / sensor / caster SKU; a measured CoM; a pass against `2.0 m/s²`; CAD |

Two concepts are authored because `physics.md` made four first-order axes comparable. A concept without a filled comparison row is a sketch, not a concept. Naming a working lead after the table is filled is a packaging/sensing *direction for the rig*, not ADR-04/ADR-07 closure and not a purchase authorization.

Full notes: [`swivel-caster-three-lookdown.md`](swivel-caster-three-lookdown.md) (Concept A); [`ball-transfer-perimeter-cliff.md`](ball-transfer-perimeter-cliff.md) (Concept B).

## 1. Evidence and credibility

### 1.1 Grades

| Grade | Meaning here |
|---|---|
| `W` | Measured on a recorded article. **This folder contains none.** |
| `D` | Manufacturer or published-standard value applied to a named article |
| `E` | Engineering estimate, napkin geometry, or calculation from `D`/`E` inputs. Never present as measured |
| `U` | Unknown. Never silently zero |

Rules carried from `physics.md` §1.1 and RP-01/RP-02 screens: never collapse the `a_tip` range to the placement-target `1.98 m/s²`; never treat a working lead as a freeze; never put a stop-path sensor behind I2C-only or a GPIO expander.

### 1.2 Credibility checklist (both concepts must clear)

A concept is credible only when every row below is present in its file. Missing a row is a sketch.

| Check | What it must show |
|---|---|
| Napkin geometry | Ø84 wheels, 170 mm track, 110 mm wheelbase to **front-support ground contact**, 70 mm skid reach as the inherited *starting* numbers; skid reach/height remain adjustable 60–80 / 8–16 mm. No CAD |
| Load path | Where floor load goes (drive patches, front support, rear skid) under the four `physics.md` §2.6 cases. Rear skid is mandatory. HIGH_AFT battery is not a concept |
| Actuator class | JGA25-class (or a named comparison class) with a sourcing path. **Class, not a SKU freeze** |
| Cable route to body | Drive, encoder, sensor and E-stop/enable harness **up through the neck void**, demate at the body. No slip ring. No motor current through a servo-style daisy chain |
| Service story | How a motor, wheel, front support, skid pad, cliff channel and body demate come apart without destroying the CoM ballast setup |
| Physics quantities with margin | Screened against the `a_tip` **range**, the §6 stopping table, wheel torque `0.036–0.110 N·m`, encoder creep, and current class — not against `2.0 m/s²` |

### 1.3 First-order axes they must differ on

These are the axes `physics.md` §10 made comparable. Cosmetic differences do not count.

| # | Axis | Concept A | Concept B |
|---|---|---|---|
| 1 | Front support (`BM-07` trail / scrub) | Swivel caster with trail (`U` until a part is on the bench) | Ø1 inch ball transfer; no trail |
| 2 | Motor / battery vs 110 mm wheelbase (CoM lever) | Motors coaxial with the drive axle (`x = 0`); battery bay **low and forward of the axle** | Motors hung **into** the wheelbase (motor CoM `x > 0`); battery as a low floor tray around the ball well, still **forward of the axle**. HIGH_AFT is forbidden in both |
| 3 | Cliff count / placement | **Three** look-down channels: caster-forward + reverse/skid + one lateral | **Perimeter ring (4+)** look-downs around the stance |
| 4 | Obstacle stop-path class | Analog-IR (GP2Y-class ADC) **in the stop path** | ToF **as telemetry only**. Stop-path obstacle is bump GPIO. Stop-path never behind I2C-only or an expander |

Battery **must** be able to sit low and forward of the axle in both concepts. A behind-axle pack is the HIGH_AFT packaging fault (`physics.md` §2.2): `a_tip` goes negative. It is not an option in either column.

## 2. Comparison matrix

Screen against `physics.md` ranges. `a_peak = 0.80 / 1.00 m/s²` (`storyboard.md` `BM-07`/`BM-08`) has envelope margin only when `x_CoM` is restored toward the placement target. HIGH lumped `a_tip = 0.905 m/s²` has **no margin** at `0.80 m/s²`. Neither concept is allowed to hide that by shrinking commanded acceleration.

Scan line (two rows, thirteen columns). Detail follows in the criterion table so cells stay evidence-bearing rather than slogan-sized.

| | Support type | Motor placement | Battery bay | Cliff count/placement | Obstacle class | BM-07 trail | a_tip recovery | d_stop coverage at 0.50 | reverse cliff | C3 GPIO | Mass vs 200–600 | Service | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | Ø25–32 swivel at +110 | JGA25-class coaxial with axle, `x ≈ 0` | Low + forward, `x = +50…+80`, `h = 18–32`. HIGH_AFT excluded | **3**: caster + skid + one lateral | Analog-IR ADC **in stop path** (GP2Y-class) | Trail `U`; one-cycle heading glitch expected | Battery-forward lever (LOW_FWD 1.90 m/s² `E`). Range, not 2.0 | **PASS** if caster-mounted (179 ≤ 300 mm `D`) | Dedicated skid look-down | 3 cliff + analog + bump + SPI/INT + 2 nFAULT + enable; ≥2 spare | 350–500 g `E`, inside | Outboard motors; caster drops; neck demate | **Working lead** (after this table). Not a freeze |
| **B** | Ø1" ball transfer at +110 | JGA25-class hung **into** WB, motor CoM `x ≈ +20…+35` | Low U-tray around cup, `x = +60…+85`. HIGH_AFT excluded | **4+** perimeter ring | ToF **telemetry only**; bump is stop-path | No trail; drag / dent / pile instead | Same battery rule + small motor +`x`. Do not claim a win | **FAIL/HOLD** as G03: bump has no 179 mm look-ahead | Ring includes rear by construction | 4+ cliff spends the spare; no expander | Upper half of 200–600 g `E` (cup+ring+coupling) | Cup clean; coupling joint; neck demate | **Comparison retained; not waived** |

| Criterion | Concept A — swivel caster, three look-downs, analog-IR stop-path | Concept B — ball transfer, perimeter cliff, ToF telemetry |
|---|---|---|
| **Support type** | Ø25–32 mm swivel caster at `+110 mm`. Trail `U`. Contact patch moves as it yaws; instantaneous `L` is not a frozen 110 mm during reverse | Ø1 inch ball transfer at `+110 mm`. Contact stays put. Higher rolling resistance `E`. Can dent soft floors / pile |
| **Motor placement** | Two JGA25-class gearmotors coaxial with the drive axle, outboard, `x ≈ 0`, `h ≈ 42 mm` (axle height). Drive mass does **not** recover `x_CoM` | Two JGA25-class gearmotors hung **into** the 110 mm wheelbase (motor CoM `x ≈ +20…+35 mm` `E`). Drive mass **does** contribute a small +`x` lever. Track still 170 mm; wheels still on the axle via belt/shaft/`E` coupling — coupling is a cost, not a freeze |
| **Battery bay** | Low bay **between axle and caster**, pack CoM `x = +50…+80 mm`, `h = 18–32 mm` `E`. This is the recovery lever (`physics.md` §2.4). HIGH_AFT excluded by construction | Low **U-tray around the ball well**, pack CoM `x = +60…+85 mm`, `h = 18–32 mm` `E`. Still forward of the axle. HIGH_AFT excluded by construction. Tray fights the ball cup for the same floor real-estate |
| **Cliff count / placement** | **3** look-downs: (1) caster-forward, (2) reverse / skid, (3) one wheel-adjacent lateral. Matches `physics.md` §7.5 minimum | **4+** perimeter ring (caster, both shoulders, skid as a starting count). Better heading coverage on paper; spends GPIO and harness |
| **Obstacle class** | GP2Y-class analog IR **in the stop path** on a C3 ADC, mounted at the caster. Triangulation, less colour-sensitive than TCRT. Bumper is last layer | VL53-class ToF **telemetry / redundant look-ahead only** (I2C). Stop-path obstacle is the GPIO bumper. Physics §7.4: do not close G03 with bump-only at follow speed |
| **BM-07 trail** | Trail makes the caster yaw on reversal; **one-cycle heading glitch is expected** (`physics.md` §3.4). Heading change > 5° per cycle is a storyboard never. Trail `U` until measured | **No trail, no swivel glitch.** Higher rolling drag on every `WIGGLE` half-cycle; ball can walk a pile or dent laminate. Different `BM-07` failure, not a free win |
| **`a_tip` recovery** | Recovers by sliding the battery bay forward and down (LOW_FWD `a_tip = 1.896 m/s²` `E`). Motors at `x = 0` do not help `x`. Lumped LOW/NOM/HIGH without that bay are `1.115 / 1.226 / 0.905 m/s²` — **not** `1.98`. Skid `14 mm @ 70 mm` still fails or is marginal until ballast restores `x`. Rig: independent `x`/`h`, skid 60–80 / 8–16 mm | Recovers by the same battery rule **plus** a small motor-mass +`x` lever. Paper `a_tip` can sit slightly above A's equivalent lumped case `E`, still a range, still not `2.0 m/s²`. HIGH_AFT remains forbidden. Coupling/shaft mass and ball-cup height can push `h_CoM` the wrong way — do not claim a better `a_tip` until the rig measures |
| **`d_stop` coverage at 0.50** | Caster-mounted analog IR: look-ahead from **caster contact** must be ≥ **179 mm** (`physics.md` §6.2). GP2Y-class max 300 mm `D` covers 179 mm with paper room. Axle-mounted would need 179+110 = 289 mm — this concept does **not** credit that | ToF telemetry can *see* past 179 mm, but it is **not** the stop path. Bumper span of the stance does not provide 179 mm look-ahead. **Coverage at 0.50 is a G03 hole** unless an analog-IR stop-path channel is added — which would collapse axis 4 and make B a variant of A, not a competing concept |
| **Reverse cliff** | Dedicated look-down covering the skid (70 mm behind axle). `BM-08` reverse launch loads the caster; reverse *creep toward an edge* is the skid-leading case. Forward-only cliff does not see it | Perimeter ring includes a rear channel by construction. Count is the advantage; dark/glossy failure mode is unchanged |
| **C3 GPIO** | 3 cliff GPIO + 1 analog obst + 1 bump + IMU SPI+INT + 2× nFAULT + fail-safe enable. Fits the planned Part 4 map with ≥ 2 spare GPIO (`compute-control-architecture.md` CA budget). No expander in the stop path | 4+ cliff GPIO **plus** bump, IMU SPI+INT, 2× nFAULT, enable. Ring spends the spare. Adding ToF I2C is bus-only and is allowed as telemetry; it does not buy back GPIO. Risk: the map fails the ≥ 2 spare rule and forces a WROOM carrier — a Part 4 change, not a silent expander |
| **Mass vs 200–600 g** | Two JGA25-class motors ~170–220 g `D`/`E` + Ø84 wheels + caster + skid + brackets → **350–500 g `E`**, inside the ledger row. Physics does not move the bound | Same motor class, **plus** ball cup / transfer, perimeter sensor brackets, and (if used) axle coupling. Likely **upper half of 200–600 g `E`**, still required to fit. A 37D-class swap would eat the row in either concept |
| **Service** | Caster fork drops down; three cliff pigtails; motors outboard on the axle; neck-void harness demates at the body. Skid pad is a screw-adjust shim. Ballast bays independent of the caster swap | Ball cup contamination (hair, grit) is a scheduled clean. Perimeter ring is more connectors. Motor-in-WB coupling is an extra service joint. Neck demate identical. Interchangeable front support on the rig still lets A/B swap without a new chassis |
| **Verdict** | **Working lead for the rig direction** — after this table is filled, not before. Clears the stop-path architecture, the three-contact cliff minimum, the battery-forward CoM lever, and the JGA25-class demand window on paper. Trail/`BM-07` glitch, dark/glossy TCRT failure, and P03 stall-current conflict remain open. **Not a freeze, not a purchase, not ADR-04/07 closure** | **Comparison retained; not waived.** No-trail `BM-07` and extra cliff headings are the reasons it exists. It loses `d_stop` at 0.50 if ToF stays telemetry-only; it spends C3 GPIO; ball denting/`U` rolling resistance are unowned. Keep it on the rig as the interchangeable front-support / ring-harness alternative. Do not silently drop it because A is the working lead |

## 3. Working lead (after the table)

**Concept A is the working lead** for how the open chassis is first detailed: swivel caster, three look-downs, analog-IR in the stop path, motors on the axle, battery bay low and forward of the axle, JGA25-class reference motors.

That sentence is weaker than a selection:

- It does not freeze a SKU, a trail, a skid height, or `a_tip`.
- It does not waive Concept B. The rig (`plan.md` §6) still carries an interchangeable front support (caster / ball transfer) and must be able to hang a fourth look-down without respinning the frame.
- It does not pass G01–G06. Those freeze in `gates.md` after Phase B/C.
- It does not authorize purchase. A JGA25-class article bought for Phase A is bench equipment until a freeze says otherwise (`plan.md` §10).

Concept B remains the comparison that keeps `BM-07` trail from being treated as inevitable, and that keeps a perimeter ring from being forgotten if three channels fail a heading.

## 4. What neither concept is allowed to do

- Place the battery on or behind the axle (HIGH_AFT).
- Put a stop-path sensor behind I2C-only or a GPIO expander.
- Close G03 with bump-only at follow speed.
- Quote `2.0 m/s²` as the robot's `a_tip`.
- Quietly shrink `a_peak` to hide a CoM miss (`physics.md` §2.5).
- Freeze 14 mm skid height or 70 mm reach. Recompute `h/d < x/h` at the ballast corner being scored.
- Let a motor-driver HAT choose the cliff sensors.

## 5. Handoff

| Document | What it takes from this comparison |
|---|---|
| `../drivetrain-screen-01.md` | JGA25-class as the reference-unit *class*; N20 as lower bound; 37D as upper bound; caster D20 vs ball D21; skid D30 adjustable |
| `../sensing-screen-01.md` | A's 3-channel + analog-IR stop-path vs B's ring + ToF telemetry; dark/glossy as the cliff failure mode |
| `../rig.md` (later) | Interchangeable front support; independent `x`/`h` ballast; skid 60–80 / 8–16 mm |
| `../decision.md` (later) | Working lead ≠ ADR-04/07 close |
