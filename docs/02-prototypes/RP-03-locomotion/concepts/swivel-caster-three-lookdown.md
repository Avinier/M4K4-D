# RP-03 Concept A — Swivel caster, three look-downs, analog-IR stop-path

| Field | Value |
|---|---|
| Status | **Paper concept v0.1. Working lead after the comparison matrix is filled — not a freeze, not a selection, not a purchase** |
| Created | 2026-09-17 |
| Owner | Project builder |
| Comparison | [`README.md`](README.md) |
| Counterpart | [`ball-transfer-perimeter-cliff.md`](ball-transfer-perimeter-cliff.md) (retained; not waived) |
| Consumes | `../physics.md` ranges; `../storyboard.md`; dimensional baseline v1.10 (Ø84, 170 track, 110 WB, 70 skid) |
| Does not contain | CAD; a SKU freeze; a single `a_tip`; a trail number presented as measured |

Concept A is the classic differential chassis the dimensional baseline already describes, made explicit as an architecture: **two encoder drive wheels, a front swivel caster, a mandatory rear skid, three look-down cliff channels at the leading contacts, and analog IR in the obstacle stop path.** Motors sit on the axle. The battery **must** sit low and forward of the axle. HIGH_AFT is not a variant of this concept; it is a packaging fault.

## 1. Napkin geometry

Inherited numbers, not a freeze. Origin at the floor on the drive-axle ground-contact line; `+x` forward (caster); `+h` up. Wheelbase `L` is axle to **caster ground contact**.

```text
TOP  (+x up the page)

                         caster contact  x = +110 mm
                         Ø25–32 mm swivel (Ø30 target)
                              ○   trail TBD  U
                              |   look-down #1 (caster-forward)
                              |   analog-IR stop-path, looking +x
                     battery  |   x = +50…+80 mm, h = 18–32 mm
                     bay      |   LOW and FORWARD of the axle
                              |
         y = +85          y = 0              y = −85
           ●==============● axle ===============●
         L wheel        x = 0, h ≈ 42         R wheel
         Ø84 × 21       motors coaxial,        Ø84 × 21
         look-down #3   outboard               (lateral channel:
         (one lateral)                         one wheel-adjacent
                                               is the minimum)
                              |
                              ▬  skid contact  x = −70 mm (adjust 60–80)
                                 h_skid = 8–16 mm (14 mm is tight, not frozen)
                                 look-down #2 (reverse / skid)

STAN 205 mm overall (CON-14 width). Track 170 mm centre-to-centre.
Neck void on the body centreline; harness rises here, demates at the body.
```

| ID | Quantity | Napkin value | Class | Notes |
|---|---|---|---|---|
| G01 | Drive wheels | Ø84 × 21 mm, moderate-grip rubber/TPU | `E` | Ø80–85 acceptable. Hub 4 mm to match JGA25-class D-shaft, or 6 mm with an adapter — spec band, not SKU |
| G05 | Track | 170 mm | `E` | Inherited |
| G06 | Wheelbase `L` | 110 mm target (105–115) | `E` | To caster **contact**, not to the fork crown |
| G07 | Caster | Ø25–32 mm swivel | `E` | Trail `U`. Contact patch moves as it yaws; `L` is not fixed during `BM-07` reverse |
| G08/G09 | Skid | Reach 60–80 mm, height 8–16 mm; inherited start 70 mm / ≤14 mm | `E` | `14/70 = 0.200` is tight against target `x/h = 0.202` and **fails** every lumped Layout 03 CoM unless ballast restores `x` |
| G10 | Stance | 205 mm | `E` | Shoulder sweep ~102 mm from centre during pivot |
| — | Battery bay | Pack CoM `x = +50…+80`, `h = 18–32` mm | `E` | **Required.** Behind-axle is HIGH_AFT and forbidden |
| — | Motors | Coaxial with axle, `x ≈ 0`, `h ≈ 42` mm | `E` | Do not recover `x_CoM`; keep mass off the head stack |
| — | Neck / demate | Harness up through neck void; demate at body | `E` | See §4 |

No CAD. Bracket envelopes, caster-fork trail, and the analog-IR mounting offset from caster contact are `U` until the rig exists. A sensor ahead of contact is credited; a sensor behind it is charged (`physics.md` §6.2).

## 2. Load path

Three-point support on a level floor, plus the skid as a catch. Evaluate the four `physics.md` §2.6 cases at the **range**, not at the placement target alone.

| Case | What loads | What unloads | Concept A path |
|---|---|---|---|
| **1. Forward launch** (governing tip) | Drive patches; inertia at CoM loads the rear | Caster unloads, then lifts | Rear skid is the catch. `a_tip,fwd = g·x/h` is a **range**: TARGET 1.978 / LOW 1.115 / NOM 1.226 / HIGH 0.905 / LOW_FWD 1.896 m/s², all `E`. HIGH_AFT is negative and excluded |
| **2. Forward brake** | Caster | Skid | Nose-down onto the caster. `a_brake,tip = g·(L−x)/h = 6.73 m/s²` at TARGET — authored `a_brake = 1.20 m/s²` does not govern. Traction during brake is a separate §3 question |
| **3. Reverse launch** (`BM-08`) | Caster | Skid | **Not** the dual of forward. Nothing behind the axle catches a forward rotation except caster geometry; then the robot is rotating over the caster. Skid does not help. `a_tip,rev = 6.73 m/s²` at TARGET |
| **4. Spin** (`BM-06`) | Drive patches scrub; caster swivels | — | Lateral tip `a_lat,tip = 6.73 m/s²` at TARGET does **not** govern. Scrub `τ ~ 0.025–0.045 N·m` per wheel at the 2.40 kg mid (`E`, order-of-magnitude) is comparable to launch torque. Trail yanks the caster |

Static share at the **target** CoM only (do not quote this as the lumped robot): `N_caster = 0.227 Mg`, `N_drive = 0.773 Mg`. If `x` collapses aft, drive share rises and `a_tip` falls — that is not a traction gift.

**Load path through hardware.** Wheel bearings / gearbox output take radial tyre load and the scrub couple. Caster fork takes the residual front share and, in reverse launch, the nose-down / reverse-tip share. Skid takes the catch after caster lift; the pad must not be a single printed tab that shears. Motor reaction torque goes into the axle brackets, not into the neck. Head yaw reaction (RP-01 paper peak `0.1099 N·m` `E`) is a couple on the 170 mm track: `τ_wheel = 0.027 N·m` — smaller than launch, but it is a **static hold** (`BM-00`/`BM-01`), not a rounding error.

## 3. Actuator class (not a SKU freeze)

**Class: JGA25-370-class, ~6 V, ~35:1, output no-load in the 160–200 RPM band, AB Hall encoder on the motor.** Named comparison articles live in `../drivetrain-screen-01.md` (`D02` lead *reference unit*, `D03` slower comparison, `D01` N20 lower bound, `D04` 37D upper bound). This file does not pick a suffix.

Why this class, on paper:

| Demand (`physics.md` §4) | Class answer | Class |
|---|---|---|
| Wheel `τ` 0.036 / 0.063 / 0.110 N·m at low/nom/high-mass launch | Oz JGA25-370 6 V 176 RPM: rated 0.85 kg·cm = **0.083 N·m**, stall 5 kg·cm = **0.490 N·m**, stall current 900 mA `D` ([Oz Robotics table](https://ozrobotics.com/shop/micro-dc-encoder-deceleration-motor-jga25-370b-25mm-motor-6v-176rpm/)) | `D` table, `E` conversion (`1 kg·cm = 0.0981 N·m`) |
| P01: stall ≥ 2× 0.110 = 0.220 **and** rated ≥ 0.063 | 0.490 ≥ 0.220; 0.083 ≥ 0.063 | Paper **pass for the class**, not a freeze |
| 0.70 m/s = 159 RPM on Ø84; unloaded design 160–200 RPM | 176 RPM no-load at 6 V sits in-band | `D` |
| `BM-02` 0.04 m/s encoder | ~11 PPR motor × 35:1 ≈ 385 counts/rev → 0.69 mm/count, ~58 counts/s | `E` from NFP 11 PPR `D` ([NFP-GM25-370-EN](https://nfpmotor.com/25mm-metal-gear-motor-model-nfp-jga25-370-en)) |
| `BM-00`/`BM-01` hold | 35:1 is **backdrivable** — needs **active hold** (or a brake, which still has to fit 200–600 g). High-ratio N20 (~150:1 / 1000:1) is the poorly-backdrivable alternative and is not this concept's class | `E` class statement |
| Current class 1.5–3 A vs Korad 5 A | Oz stall **900 mA** is *below* the ledger class (better electrically) but **conflicts** with NFP stall ≤ 3 A `D`. Do not pick. Screen P03 as HOLD until the purchased article is metered. If the article is 3 A, both-motor stall exceeds 5 A → Phase B per-motor | `D` conflict |

N20-class is the lower bound, not the Concept A actuator: bins that hit 160–200 RPM typically stall below 0.110 N·m; bins that stall hard are ~15 RPM and fail the speed band. 37D-class is the upper bound: two motors of ~150–200 g eat the drive row. See the drivetrain screen.

Wheels, caster, skid are spec bands (`D10`/`D20`/`D30`), not SKUs.

## 4. Cable route to the body

All base energy and signals that leave the chassis go **up through the neck void** and **demate at the body**. This is the same mass-boundary idea as RP-01's yaw-plane demate, applied to the base.

```text
wheels / caster / skid / cliffs / analog-IR / bump / IMU / drivers
        → short pigtails on the chassis (service loops)
        → trunk in the neck void
        → body-side demate (keyed, not Dupont)
        → C3 / PB-DRIVE / PB-SAFE-BASE live in the body, not in the base tub
```

| Bundle | Contents | Constraint |
|---|---|---|
| `PB-DRIVE-L/R` | Two motor pairs, separately observable; signed current | Behind the hardware E-stop / motor-arm. Logic analyzer **never** on the motor rail |
| Encoder | 2× (A, B, V, G) Hall | Direct C3 PCNT/GPIO. Not through an expander |
| Stop-path sensors | 3 cliff GPIO, 1 analog IR, 1 bump | Direct C3. **Never** I2C-only, **never** a GPIO expander |
| Driver control | 2× nFAULT, enable (pulled to inhibit), PWM/PH per channel, IPROPI analog | Enable fails safe on a broken loop |
| IMU | SPI + INT1 | Telemetry / slip-lift; not a substitute for cliffs |
| Optional ToF | I2C | Telemetry only, if GPIO spare remains ≥ 2 |

No slip ring. Neck yaw in V1 is the head's, not the base's; the trunk sees the body's yaw travel, not a continuous rotation. Strain relief at both demate faces. Motor current does not share a connector cavity with 3.3 V logic without a key and a missing-pin barrier.

## 5. Service story

The rig is an ugly decision instrument (`plan.md` §6). Concept A has to come apart without changing ballast geometry.

| Action | How |
|---|---|
| Swap a motor | Outboard JGA25-class on the axle bracket; hub screw; encoder pigtail. Ballast bays do not move |
| Swap a wheel | Ø84 press/clamp on the D-shaft; do not use set-screw-on-round as the production path |
| Swap the caster | Fork drops down through the deck. Trail articles can be compared without respinning the frame. Look-down #1 stays with the caster carrier so coverage geometry does not walk |
| Adjust the skid | Screw-adjust reach 60–80 mm and height 8–16 mm; lock. Recompute `h/d < x/h` at the scored corner — do not freeze 14 mm |
| One cliff channel dies | Pigtail at that carrier; the other two stay. Mask/freeze/corrupt is a sensor interposer job (`F-19`), not a solder job |
| Body demate | One keyed trunk at the neck. Base can sit on the bench with a dummy body connector for Phase A/B |
| Push for service | 35:1 is backdrivable: inhibited `BM-00` will **not** hold. Either inhibit *and* chock the wheels, or accept that a nudge of ~2 N may roll. That is a known class cost, not a surprise |

Ballast sets `M`, `x_CoM` and `h_CoM` **independently**. Changing a wheel or the caster must not be how CoM is “tuned”.

## 6. Physics quantities — screened with margin, as ranges

Do **not** score this concept against `2.0 m/s²`. The placement target survives only if RP-06 / rig ballast actually hit `x ≈ +25 mm`, `h ≈ 124 mm`. Commanded `a_peak` is not quietly reduced to hide a miss.

### 6.1 `a_tip` range vs authored `a_peak`

| Case | `a_tip` (m/s²) `E` | vs `a_peak` 0.80 | vs `a_peak` 1.00 |
|---|---:|---|---|
| LOW lumped | 1.115 | paper-thin margin 0.32 — not registered | **exceeds** |
| NOM lumped | 1.226 | margin 0.43, skid already fails `h/d` | **exceeds** |
| HIGH lumped | 0.905 | **no margin** (0.80 vs 0.91 is paper-thin; do not call it margin) | **exceeds** |
| HIGH_AFT | −0.111 | **forbidden** | forbidden |
| LOW_FWD (this concept's recovery) | 1.896 | margin 1.10 | margin 0.90 |
| TARGET (placement, not a roll-up) | 1.978 | margin 1.18 | margin 0.98 |

**Clearance statement:** Concept A is credible only when the battery bay *and* the body that rides with it are pulled forward and down, and the rig ballast is allowed to finish the job. The concept **includes** that bay. It does not include a rear pack. Skid geometry stays adjustable; `14 mm @ 70 mm` is not cleared on the lumped CoMs.

### 6.2 Stopping table — look-ahead from caster contact

`t_latency = 50 ms` invariant, `a_brake = 1.20 m/s²`, `d_margin = 50 mm` floor (`physics.md` §6.2). Analog-IR sample-age bound used in the screen is 25 ms `E` (one 16.5 ms cycle + scan), still scored against 50 ms.

| `v` (m/s) | `d_stop` (mm) | Concept A coverage |
|---:|---:|---|
| 0.05–0.06 calibration | 45–54 (tabletop 40 mm margin → ~44 mm) | Look-down #1 must see floor disappear **~40 mm before caster contact**. TCRT-class useful range 0.2–15 mm `D` is a **geometry** sensor for “floor present”, not a ranging sensor — mount it looking down at the floor just ahead of contact |
| 0.50 follow cap | **179** | Analog IR at the **caster**: 4–30 cm `D` covers 179 mm. **PASS** for follow if caster-mounted. Axle-mounted would need 289 mm and is not this mounting |
| 0.70 design point | **289** | 300 mm max is **tight** — P-gate **HOLD** for the 0.70 design point; not a reason to weaken the 0.50 follow cap |
| Pivot 220 °/s (wheel 0.326 m/s) | ~110–120 class | Look-down #3 (lateral) + bump at the shoulder. A forward-only IR does **not** cover a furniture leg at the shoulder (`BM-05`/`BM-06`) |

Blind-region: 20 mm cube in the caster's shadow is the failure mode. Bumper is last layer, not the first.

### 6.3 Wheel torque, encoder, current, mass

| Quantity | Envelope | Concept A class | Result |
|---|---|---|---|
| `τ_wheel` | 0.036 / 0.063 / 0.110 N·m | Stall 0.490 `D`, rated 0.083 `D` (Oz 6 V 176 RPM) | Class clears P01 on that table. NFP 34:1 stall 4.5 kg·cm = 0.441 N·m also ≥ 0.220. Not a SKU |
| Encoder creep | ≲ 2 mm/count and ≳ 20 counts/s at 0.04 m/s | 0.69 mm/count, ~58 c/s `E` | Class **PASS**. 12 CPR at the wheel is **FAIL** and is not used |
| Current | 1.5–3 A per motor `E`; both-motor vs Korad 5 A `D` | Oz 0.90 A both = 1.8 A (under 5 A). NFP ≤ 3 A both = 6 A (over 5 A) | **HOLD** until metered. 0.9 A is below the ledger class (better) but the conflict is cited, not averaged |
| Mass | Drive row 200–600 g | Two motors ~170–220 g + wheels + caster + skid + brackets → 350–500 g `E` | Inside the row. Physics does not move the bound |
| Backdrivability | `BM-00` unpowered hold vs `BM-01` armed hold | 35:1 needs active hold; will not hold when inhibited | Class cost: idle energy on `LG-04` when armed; chock when inhibited. Not a brake freeze |

### 6.4 Sensing architecture (this concept's half of ADR-07)

| Function | Channel | Interface | Stop-path? |
|---|---|---|---|
| Cliff forward | Look-down #1 at caster | GPIO analog or digital (TCRT-class lead in the sensing screen) | **Yes** |
| Cliff reverse | Look-down #2 at skid | GPIO | **Yes** |
| Cliff lateral | Look-down #3 wheel-adjacent | GPIO | **Yes** |
| Obstacle | GP2Y-class analog IR at caster, looking +x | C3 ADC | **Yes** |
| Bump | Lever spanning stance | Direct GPIO | **Yes**, last layer |
| IMU | ICM-42688-class SPI + INT | SPI + interrupt | Slip/lift/tip; not a cliff substitute |
| ToF | Optional, not required by this concept | I2C | **Telemetry only** |

Dark or glossy tabletop is the cliff **failure mode**, not an afterthought. TCRT measures reflectivity, not geometry; glossy black can look like floor. A dark+glossy trial is mandatory if TCRT-class is the GPIO cliff. Age bounds `E` (not registered): cliff GPIO 10 ms; analog IR 25 ms; bump 5 ms; IMU 10 ms. Unknown = inhibit.

C3 budget: 3 cliff + 1 analog + 1 bump + IMU SPI+INT + 2 nFAULT + enable fits the planned Part 4 map with ≥ 2 spare GPIO. That check is repeated in the sensing screen; it is not a pin-map freeze here.

## 7. What this file does not do

- Does not freeze JGA25-370 6 V 176 RPM as a SKU. `D02` is a reference unit for the bench.
- Does not freeze trail, skid height, or `a_tip`.
- Does not waive Concept B.
- Does not pass a gate or authorize purchase.
- Does not claim the lumped robot has `1.98 m/s²` of tip margin.

## 8. Handoff

Working-lead status is recorded in [`README.md`](README.md) §3, **after** the comparison table. Drivetrain rows `D02`/`D10`/`D20`/`D30` and sensing rows `S01`/`S04`/`S06`/`S07` are the matching screens, not this file's to select.
