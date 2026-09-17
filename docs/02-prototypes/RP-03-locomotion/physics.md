# RP-03 Physics — Stability, Traction, Demand, Stopping, Coverage

| Field | Value |
|---|---|
| Status | **Paper envelope v0.1 — ranges, not a freeze.** No motor, sensor or caster selected. No single `a_tip`. No pass threshold. No purchase |
| Created | 2026-09-17 |
| Owner | Project builder |
| Governing plan | `plan.md` Part 2; `plan.md` §5 checklist |
| Method | `../../intuition.md` §5.1 step 3; safety toolkit `d_available > v·t_latency + v²/(2·a_brake) + d_margin` |
| Consumes | `intent.md`; `storyboard.md`; `../../01-system/dimensional-baseline.md` v1.10; `../../01-system/mass-envelope-ledger.md` v0.14; `../../01-system/power-energy-ledger.md` v0.13; RP-01 `fullproofmath.md` yaw **0.1099 N·m** (`E`, paper) |
| Feeds | `concepts/`; `drivetrain-screen-01.md`; `sensing-screen-01.md`; `gates.md`; ledger `LG-04`/`LG-10` `E` refresh |
| Does not claim | A measured CoM, a measured lift onset, a selected drivetrain, a selected sensor, a frozen footprint, a frozen `a_tip`, or any gate pass |

This file recomputes the locomotion envelope as **ranges**. Every numeric input carries `W`/`D`/`E`/`U`. An `E` value is not a target, not a measurement, and not a freeze. The dimensional-baseline figure `a_tip ≈ 1.98 m/s²` is a **placement target** at `x_CoM = +25 mm`, `h_CoM = 124 mm`. It is not a property of the Layout 03 mass roll-up.

## 1. Assumption register

### 1.1 Evidence grades

| Grade | Meaning here |
|---|---|
| `W` | Measured on the recorded article, with a run ID. **This file contains none.** |
| `D` | Manufacturer or published-standard value applied to a named article (Korad 5 A ceiling; conventional `g = 9.81 m/s²`) |
| `E` | Engineering estimate, authored hypothesis, CAD/ledger allowance, or calculation from `E`/`D` inputs. Never present as measured |
| `U` | Unknown. Never silently zero. Name the owner and what it blocks |

Rules carried in from `intent.md` §9 and RP-01 `fullproofmath.md` §2:

- Never present a D/E tree as measured hardware.
- Never silently set an unknown friction, trail, latency or current term to zero.
- Never collapse a range to a point because a screen wants a threshold.
- Never select a motor, sensor or SKU in this file.
- Never treat the 2.0 m/s² planning value as a mass-roll-up result.

### 1.2 Coordinate frame

Inherited from `dimensional-baseline.md` v1.10. Do not re-derive.

- Origin at the floor, on the drive-axle ground-contact line.
- `+x` forward (toward the caster). `x = 0` at the drive axle.
- `+h` upward from the floor.
- Yaw-positive about vertical. Track is the lateral wheel centre-to-centre.
- Wheelbase `L` is drive-axle centreline to **front-caster ground contact**, not a second powered-axle spacing.
- Every lumped-block `(m, x, h)` in §2 is `E`.

### 1.3 Inherited geometry — cite, do not re-derive

| ID | Quantity | Value | Class | Source |
|---|---|---|---|---|
| G01 | Drive-wheel diameter `D_wheel` | 84 mm nominal (Ø80–85 acceptable) | `E` | dimensional-baseline v1.10 |
| G02 | Drive-wheel radius `r` | 42 mm = 0.042 m | `E` | `D_wheel/2`; axle height ~42 mm |
| G03 | Wheel circumference | `π·0.084 = 0.2639 m` | `E` | G01; `π` conventional |
| G04 | Tread width | 21 mm nominal (~20–22) | `E` | dimensional-baseline |
| G05 | Track (centre-to-centre) | 170 mm | `E` | dimensional-baseline |
| G06 | Wheelbase `L` | 110 mm target (105–115) | `E` | dimensional-baseline |
| G07 | Caster diameter | 25–32 mm (~30 mm target) | `E` | dimensional-baseline |
| G08 | Rear skid reach `d` | 70 mm behind axle | `E` | dimensional-baseline; MEM-20260825-02 |
| G09 | Rear skid height `h_skid` | ≤14 mm above floor at 70 mm | `E` | dimensional-baseline |
| G10 | Stance / overall width | 205 mm (CON-14 width) | `E` | dimensional-baseline; CON-14 |
| G11 | Layout 03 vertical stack | 304 mm (140 + 60 + 104) | `E` | dimensional-baseline; RP-06 accepts or recovers 4 mm |
| G12 | Conventional `g` | 9.81 m/s² | `D` | standard gravity used throughout |
| G13 | Follow ceiling | ≤ 0.5 m/s; cannot be weakened | `E` | CON-19; dimensional-baseline |
| G14 | Design wheel speed | 160–200 RPM unloaded at 0.70 m/s | `E` | dimensional-baseline |
| G15 | Speed bands | normal 0.15–0.40; fast 0.40–0.60; max 0.65–0.70 m/s | `E` | dimensional-baseline |
| G16 | Yaw-rate band | 120–220 °/s commanded; 300 °/s+ is headroom, not a command | `E` | dimensional-baseline |
| G17 | Whole-robot CoM **target** | `x = +25 mm`, `h = 124 mm` | `E` | dimensional-baseline v1.8/v1.10; **placement target, not a roll-up** |

Skid inequality (baseline, at the target CoM only): `h_skid/d < x_CoM/h_CoM`. At the target, `25/124 ≈ 0.202` and `14/70 = 0.200` — just clears. Recompute against the §2 range; do not freeze 14 mm.

### 1.4 Inherited mass, energy, time, reaction

| ID | Quantity | Value | Class | Source |
|---|---|---|---|---|
| M01 | Drive mass | 200–600 g | `E` | mass-envelope-ledger v0.14. **Physics does not move this bound** |
| M02 | Battery mass | 150–500 g, low and forward of the axle | `E` | same |
| M03 | Body mass | 400–900 g | `E` | same |
| M04 | Electronics mass | 150–400 g | `E` | same |
| M05 | Wiring mass | 60–180 g | `E` | same |
| M06 | Fasteners mass | 40–120 g | `E` | same |
| M07 | Structural / integration margin | 150–400 g | `E` | same |
| M08 | Layout 03 complete head | 499 / 509 / 524 g at M008 = 10 / 20 / 35 g | `E` | mass-envelope-ledger; payload-mass-capture; Layout 03 tree. Not M900 |
| M09 | Whole-robot analytical low | 1649 g ≈ 1.65 kg | `E` | ledger low rows + 499 g head |
| M10 | Other-subsystem high, before head | ≈ 3.10 kg | `E` | ledger high rows |
| M11 | Whole-robot analytical high used here | 3624 g = 3100 g + 524 g | `E` | M10 + M08 high |
| M12 | Head CoM height in the lumped model | ~250–255 mm | `E` | head sitting on the 304 mm stack; not a CAD CoM |
| E01 | `LG-04` idle (inhibited) | 0 W (motors not energized) | `E` | power-energy-ledger v0.13; a requirement, not a measured enabled-driver idle |
| E02 | `LG-04` average working (ledger, pre-refresh) | 3–8 W | `E` | same; §5 proposes 2–8 W and forbids narrowing below that |
| E03 | `LG-04` peak both stall/reversal | 20–40 W | `E` | same |
| E04 | Per-motor current class | 1.5–3 A | `E` | same |
| E05 | `LG-10` (ledger, pre-refresh) | idle 0.2–0.4 W; avg 0.3–0.6 W; peak ≤ 1 W | `U` | same; C3 identity is selected, sensors are not |
| E06 | 2S-class bus | 6.0–8.4 V | `E` | RP-02 `PB-MAIN` planning case, **not a freeze** |
| T01 | C3 hazard scan | 200 Hz → `t_hazard = 5 ms` | `E` | CA-12 target; not measured jitter |
| T02 | C3 wheel loop | 500 Hz → `t_loop = 2 ms` | `E` | CA-12 target |
| T03 | Detection-to-deceleration invariant | ≤ 50 ms | `E` | CA-12; MEM-20260812-01. **Score with this, not with the optimistic sum** |
| T04 | Korad KA3005D current ceiling | 5 A | `D` | `workbench.md`; manufacturer ceiling |
| R01 | RP-01 paper yaw peak (reaction into the base) | **0.1099 N·m at 90.5 °/s** | `E` | `fullproofmath.md` BC-60 screened peak 0.109917 N·m. External rigid-body paper; not `W` |

### 1.5 Authored storyboard kinematics — hypotheses, not gates

`storyboard.md` is authoritative for panel assignment. Every row below is an **authored hypothesis** (`E`) until `gates.md` freezes a threshold. Controlling cases as exported:

| ID | Quantity | Min viable / best-case | Class | Controlling panel |
|---|---|---|---|---|
| S01 | Creep speed | 0.04 / 0.08 m/s | `E` | `BM-02` |
| S02 | Follow speed cap | 0.45 m/s (hard follow ceiling remains 0.50 m/s) | `E` | `BM-04` |
| S03 | Follow acceleration | 0.40 m/s² | `E` | `BM-04` |
| S04 | Controlling `a_peak` | **0.80 / 1.00 m/s²** | `E` | `BM-07` / `BM-08` |
| S05 | High-mass torque sensitivity `a` | 1.20 m/s² | `E` | demand probe only; not a storyboard command |
| S06 | Controlling `ω_peak` | **180 / 220 °/s** | `E` | `BM-06` |
| S07 | Authored `a_brake` | 1.20 m/s² | `E` | `BM-09` / stop path; §6 |
| S08 | Calibration speed ceiling | 0.05–0.06 m/s | `E` | `BM-11`; CON-TBD-14 proposal |

These are not pass/fail numbers. They are what the envelope is screened against.

### 1.6 Coefficients estimated in this file

None of these is `W`. None is silently zero.

| ID | Quantity | Value | Class | Basis |
|---|---|---|---|---|
| C01 | Rolling-resistance coeff. `C_rr` | 0.025 | `E` | moderate-grip rubber/TPU on hard floor; analogical |
| C02 | Tile μ | 0.40–0.70 | `E` | household tile, dry, moderate-grip tyre. BD-04 will name the room |
| C03 | Wood / laminate μ | 0.35–0.60 | `E` | same |
| C04 | Thin rug μ | 0.45–0.80 | `E` | same; threshold geometry is not a μ problem |
| C05 | Sensor sample-age bound | 20 ms | `E` | ToF frame or analog-IR settle. Digital cliff can be ~1–5 ms; do not take the fast number as the bound |
| C06 | Driver response | 8 ms | `E` | H-bridge + current loop, analogical; not a named driver |
| C07 | Floor stopping margin `d_margin` | 50 mm | `E` | clearance hypothesis for G03 |
| C08 | Tabletop stopping margin | 40 mm inside the mark | `E` | CON-TBD-14 proposal |
| C09 | Gearbox efficiency, N20/JGA25 class | 40–70 % | `E` | class, not a SKU. Do not collapse electrical demand by assuming the top of the band |
| C10 | Motor no-load speed, hobby class | 3000–18000 RPM | `E` | class window for ratio screening |
| C11 | Signed regen current class | 0.3–1.5 A | `E` | `LP-04-REV/BRAKE`; polarity opposite traction |
| C12 | Blind-region object | 20 mm square × 20 mm tall, floor level | `E` | caster-shadow failure mode |
| C13 | Scrub lever | `tread/3 = 7 mm` per wheel | `E` | order-of-magnitude patch centroid for a scrubbing tyre, not a measured contact patch |

Lumped-block masses and `(x, h)` coordinates are tabulated in §2. Every one is `E`.

### 1.7 What is still `U` (not zero)

| Item | Why it is `U` | What it blocks |
|---|---|---|
| Installed complete-head mass M900 | Layout 03 tree is D/E | A point `a_tip`; waits on RP-01 |
| Real integrated `x_CoM`, `h_CoM` | No ballast article exists | Lift-onset `W`; RP-03 scores BD-05 corners instead |
| Floor μ on the builder's surfaces | BD-04 unnamed | Traction `W`; G01 surface matrix |
| Caster trail / swivel friction | No caster selected | `BM-07` heading-glitch magnitude |
| Ball-transfer rolling resistance and floor denting | No support selected | Concept A vs B comparison numbers stay order-of-magnitude |
| Driver + gearbox electrical efficiency as a product | No motor selected | `LG-04` stays a band |
| `LG-10` sensing load | No sensor candidate on the bench | Class remains `U`; do not invent a `W` |
| First loaded structural mode of the base | No chassis | Not used as a pass in this paper |
| Acoustic dB at the body array | No drivetrain | §9 records the obligation, not a number |

---

## 2. Stability recomputed as a range

### 2.1 The placement target is not a roll-up

The dimensional baseline gives

```text
a_tip = g · x_CoM / h_CoM = 9.81 · 25 / 124 = 1.978 m/s²
```

at `x = +25 mm`, `h = 124 mm`. Call this **1.98 m/s²** in prose. It is a **placement target**. It is **not** a property of the Layout 03 mass roll-up.

A lumped `E` model with the heavier head at ~250 mm CoM height pulls `x_CoM` aft and `h_CoM` into the 100–120 mm band unless the battery is aggressively low and forward. Screens that still treat `2.0 m/s²` as the robot's `a_tip` are repeating the 250 g-head error.

Convention in this section: `a_tip` means the **forward-launch caster-lift** acceleration `g·x/h`, the governing tip case. The other three loading cases are separate because they load different supports.

### 2.2 Lumped `E` model — state every coordinate as `E`

Eight rigid lumps. Origin: floor, drive axle. `+x` forward. Masses from the ledger corners. Coordinates are packaging hypotheses, not CAD CoMs.

**LOW** — analytical minimum 1649 g.

| Lump | `m` (g) `E` | `x` (mm) `E` | `h` (mm) `E` | `m·x` (g·mm) | `m·h` (g·mm) |
|---|---:|---:|---:|---:|---:|
| Drive | 200 | 0 | 42 | 0 | 8 400 |
| Battery | 150 | +60 | 30 | 9 000 | 4 500 |
| Body | 400 | +20 | 80 | 8 000 | 32 000 |
| Electronics | 150 | +10 | 60 | 1 500 | 9 000 |
| Wiring | 60 | 0 | 80 | 0 | 4 800 |
| Fasteners | 40 | 0 | 60 | 0 | 2 400 |
| Margin | 150 | +10 | 80 | 1 500 | 12 000 |
| Head | 499 | +5 | 250 | 2 495 | 124 750 |
| **Sum** | **1649** | | | **22 495** | **197 850** |

```text
x = 22495 / 1649 = 13.64 mm
h = 197850 / 1649 = 119.98 mm
x/h = 0.114
a_tip = 9.81 · 13.64 / 119.98 = 1.115 m/s²
h_skid/d = 14/70 = 0.200
skid inequality 0.200 < 0.114 ?  NO.  FAILS (0.200 ≮ 0.114).
```

**NOM** — 2559 g (ledger mids + 509 g nominal head).

| Lump | `m` (g) `E` | `x` (mm) `E` | `h` (mm) `E` | `m·x` | `m·h` |
|---|---:|---:|---:|---:|---:|
| Drive | 400 | 0 | 42 | 0 | 16 800 |
| Battery | 300 | +50 | 32 | 15 000 | 9 600 |
| Body | 650 | +18 | 85 | 11 700 | 55 250 |
| Electronics | 250 | +5 | 70 | 1 250 | 17 500 |
| Wiring | 120 | 0 | 85 | 0 | 10 200 |
| Fasteners | 80 | 0 | 65 | 0 | 5 200 |
| Margin | 250 | +10 | 85 | 2 500 | 21 250 |
| Head | 509 | +5 | 252 | 2 545 | 128 268 |
| **Sum** | **2559** | | | **32 995** | **264 068** |

```text
x = 32995 / 2559 = 12.89 mm
h = 264068 / 2559 = 103.19 mm
x/h = 0.125
a_tip = 9.81 · 12.89 / 103.19 = 1.226 m/s²
skid 0.200 < 0.125 ?  NO.  FAILS.
```

**HIGH** — 3624 g = 3100 g + 524 g.

| Lump | `m` (g) `E` | `x` (mm) `E` | `h` (mm) `E` | `m·x` | `m·h` |
|---|---:|---:|---:|---:|---:|
| Drive | 600 | 0 | 42 | 0 | 25 200 |
| Battery | 500 | +30 | 40 | 15 000 | 20 000 |
| Body | 900 | +15 | 90 | 13 500 | 81 000 |
| Electronics | 400 | 0 | 80 | 0 | 32 000 |
| Wiring | 180 | 0 | 90 | 0 | 16 200 |
| Fasteners | 120 | 0 | 70 | 0 | 8 400 |
| Margin | 400 | +10 | 90 | 4 000 | 36 000 |
| Head | 524 | 0 | 255 | 0 | 133 620 |
| **Sum** | **3624** | | | **32 500** | **352 420** |

```text
x = 32500 / 3624 = 8.97 mm
h = 352420 / 3624 = 97.25 mm
x/h = 0.092
a_tip = 9.81 · 8.97 / 97.25 = 0.905 m/s²
skid 0.200 < 0.092 ?  NO.  FAILS.
```

**HIGH_AFT** — HIGH masses; battery CoM on/aft of the axle. A 500 g pack is not a point mass: the tabulated case places the pack CoM at `x = −43 mm` `E` (pack sitting over the axle, mass behind the centreline). All other HIGH coordinates unchanged.

```text
Σ(m x)_without_battery = 32500 − 15000 = 17500 g·mm
battery at x = −43 mm: 500 · (−43) = −21500
Σ(m x) = −4000 g·mm
x = −4000 / 3624 = −1.10 mm
h = 97.25 mm  (heights unchanged)
a_tip = 9.81 · (−1.10) / 97.25 = −0.111 m/s²
```

`a_tip` is negative: the caster lifts at **any** forward acceleration. **Forbidden placement.** Even the milder `x_battery = 0` variant (pack centreline on the axle, HIGH's other forward offsets retained) only yields `x = +4.83 mm`, `a_tip = 0.487 m/s²` — not a usable margin against `a_peak = 0.80 m/s²`. Behind-axle battery is not a concept; it is a packaging fault.

**LOW_FWD** — LOW masses; battery at the forward geometric limit `x = +80 mm` (caster contact is at +110 mm) and low (`h = 18 mm`); body bay that holds it pulled forward and down with it. Head stays at `h = 250 mm`. This is the recovery lever, not a second robot.

| Lump | `m` (g) `E` | `x` (mm) `E` | `h` (mm) `E` | `m·x` | `m·h` |
|---|---:|---:|---:|---:|---:|
| Drive | 200 | 0 | 42 | 0 | 8 400 |
| Battery | 150 | +80 | 18 | 12 000 | 2 700 |
| Body | 400 | +45.2 | 50 | 18 080 | 20 000 |
| Electronics | 150 | +10 | 60 | 1 500 | 9 000 |
| Wiring | 60 | 0 | 80 | 0 | 4 800 |
| Fasteners | 40 | 0 | 60 | 0 | 2 400 |
| Margin | 150 | +10 | 80 | 1 500 | 12 000 |
| Head | 499 | +5 | 250 | 2 495 | 124 750 |
| **Sum** | **1649** | | | **35 575** | **184 050** |

```text
x = 35575 / 1649 = 21.57 mm
h = 184050 / 1649 = 111.61 mm
x/h = 0.193
a_tip = 9.81 · 21.57 / 111.61 = 1.896 m/s²
skid 0.200 < 0.193 ?  NO.  STILL MARGINAL (0.200 vs 0.193).
```

Battery alone cannot hit `x = +25 mm` on the LOW article: stripping the battery from LOW leaves `Σ(m x) = 13495 g·mm`, so `x_battery = (25·1649 − 13495)/150 = 185 mm` — beyond the 110 mm wheelbase. Recovery requires the battery **and** the body bay that rides with it. Even then the 14 mm / 70 mm skid does not cleanly clear.

**TARGET** — not a lumped roll-up. The dimensional-baseline placement, restated for the inequality:

```text
x = +25 mm,  h = 124 mm
a_tip = 9.81 · 25 / 124 = 1.978 m/s²
x/h = 0.202
skid 14 mm @ 70 mm: 0.200 < 0.202  — just clears.
```

### 2.3 Envelope summary

| Case | `M` (g) | `x` (mm) | `h` (mm) | `a_tip` (m/s²) | `x/h` | Skid 14 mm @ 70 mm |
|---|---:|---:|---:|---:|---:|---|
| LOW | 1649 | +13.64 | 119.98 | 1.115 | 0.114 | **FAILS** |
| NOM | 2559 | +12.89 | 103.19 | 1.226 | 0.125 | **FAILS** |
| HIGH | 3624 | +8.97 | 97.25 | 0.905 | 0.092 | **FAILS** |
| HIGH_AFT | 3624 | −1.10 | 97.25 | −0.111 | negative | **FORBIDDEN** |
| LOW_FWD | 1649 | +21.57 | 111.61 | 1.896 | 0.193 | **marginal** (0.200 vs 0.193) |
| TARGET | — | +25 | 124 | 1.978 | 0.202 | just clears |

All `a_tip` values are `E`. The range under Layout 03 lumps is roughly **0.9–1.9 m/s²**, and it goes **negative** if the battery sits on or behind the axle. There is no single `a_tip` to freeze.

### 2.4 Sensitivity at the target

Differentiate `a_tip = g x / h` at `(x, h) = (25, 124)` mm:

```text
∂a/∂x = g/h = 9.81 / 0.124 = 79.1 s⁻²
        → +10 mm forward  ⇒  +0.791 m/s²

∂a/∂h = −g x / h² = −9.81 · 0.025 / 0.124² = −15.95 s⁻²
        → +10 mm up       ⇒  −0.160 m/s²
```

Battery placement is the lever that recovers margin: it moves `x` more cheaply than any other lump (low, and the only large mass that is allowed to sit well forward of the axle). Head height is a weaker opposite lever. The rig must set `x_CoM` and `h_CoM` **independently** (`plan.md` §6). Changing ballast must not change frame stiffness or support geometry.

### 2.5 Conclusion — copy this into screens

**The 2.0 m/s² planning value does NOT survive as a mass-roll-up result under Layout 03. It survives only as a placement target that RP-06 / the rig ballast must actually hit. If the target is missed, the dimensional baseline is revised — RP-03 does not quietly shrink commanded acceleration to hide a CoM miss. Commanded `a_peak` in the storyboard (0.80–1.00 m/s²) is an authored hypothesis that only has margin when `x_CoM ≥ +20 mm`. The rig must set `x_CoM` and `h_CoM` independently (`plan.md` §6).**

Check the margin statement. At `x = +20 mm`, `h = 124 mm`: `a_tip = 9.81 · 20 / 124 = 1.582 m/s²`, which still sits above `a_peak = 1.00 m/s²`. At HIGH's lumped `x = 8.97 mm`, `a_tip = 0.905 m/s²` and `a_peak = 1.00` has **no margin**. At LOW's lumped `x = 13.64 mm`, `a_tip = 1.115 m/s²` and `a_peak = 0.80` has 0.32 m/s² of paper margin — not a registered margin, and the skid already fails.

### 2.6 Four loading cases — they load different supports

Evaluate at the **target** CoM first, then re-evaluate at every lumped corner. Do not quote only the target.

**1. Forward launch (governing).** Wheels accelerate `+x`. Inertia at the CoM loads the rear. Caster unloads, then lifts. Rear skid is the catch.

```text
a_tip,fwd = g · x / h
          = 1.978 m/s²   at TARGET
          = 1.115 / 1.226 / 0.905 m/s²   at LOW / NOM / HIGH
```

This is the number commanded `a_peak` is screened against. It is a range.

**2. Forward brake (not governing vs traction).** Decelerating from forward motion. Inertia loads the caster. Nose-down onto the caster; the skid unloads.

```text
a_brake,tip = g · (L − x) / h
            = 9.81 · (110 − 25) / 124
            = 9.81 · 85 / 124
            = 6.725 m/s²    at TARGET
```

Authored `a_brake = 1.20 m/s²` (S07) is far below 6.7 m/s². Nose-down does not govern. Traction on the drive wheels during braking is a separate §3 question; it still does not undercut 1.20 m/s² on the μ ranges in this file.

**3. Reverse launch — not the same as forward.** Wheels accelerate `−x`. Inertia loads the caster. The skid unloads. Nothing behind the axle catches a forward rotation except the caster geometry itself, and then the robot is rotating over the caster.

```text
a_tip,rev = g · (L − x) / h = 6.725 m/s²    at TARGET
```

Same number as forward brake, different support, different failure: a forward flip over the caster, not a rear catch. Reverse is **not** the dual of forward. `BM-08` startle retreat loads this case. The skid does not help.

**4. Spin.** CoM sits 25 mm forward of the axle at the target, so it orbits. At `ω = 220 °/s = 3.840 rad/s`:

```text
a_cent = ω² · x = (3.840)² · 0.025 = 0.37 m/s²
a_lat,tip = g · (track/2) / h = 9.81 · 85 / 124 = 6.725 m/s²
```

Spin does **not** govern tip. It governs scrub (§3) and caster swivel. A walking spin is a scrub/caster problem, not a lateral-tip problem, at these rates and this track.

At HIGH, `a_lat,tip = 9.81 · 85 / 97.25 = 8.57 m/s²` — still not governing. At HIGH_AFT, forward launch is already forbidden; do not bother screening spin.

### 2.7 Skid geometry is not frozen at 14 mm

`14 mm @ 70 mm` is **tight** against the target (`0.200` vs `0.202`) and **fails** against every lumped Layout 03 CoM unless ballast restores `x`. The rig must adjust reach **60–80 mm** and height **8–16 mm** (`plan.md` §6). Do not freeze 14 mm. Do not freeze 70 mm. Recompute `h/d < x/h` at the ballast corner being scored.

If the target is hit, a 14 mm / 70 mm skid just clears. If the target is missed, lengthen reach or drop the skid — or restore `x`. Do not command a smaller `a_peak` to hide it.

---

## 3. Traction and scrub

### 3.1 Friction ranges (`E`)

| Surface | μ `E` | Notes |
|---|---|---|
| Tile | 0.40–0.70 | Dry household tile, moderate-grip rubber/TPU |
| Wood / laminate | 0.35–0.60 | Dust and polish move this; BD-04 names the room |
| Thin rug | 0.45–0.80 | Pile can also jam a caster or a ball transfer |
| Threshold strip | — | **Geometric**, not a μ problem. Treat as an obstacle / pitch disturbance |

Do not pick a single μ. Do not treat the top of a band as available.

### 3.2 Drive-wheel share at the target CoM

Three-point support, static, level floor, caster at `+L`:

```text
N_caster = M g · x / L = M g · 25 / 110 = 0.227 M g
N_drive  = M g · (L − x) / L = 0.773 M g
```

Available longitudinal acceleration from drive-wheel friction, before the caster contributes (it is passive):

```text
a_trac = μ · (N_drive / M) = μ · 0.773 · g
```

| Surface | μ | `a_trac` (m/s²) `E` |
|---|---|---|
| Tile | 0.40–0.70 | **3.03–5.31** |
| Wood / laminate | 0.35–0.60 | 2.65–4.55 |
| Thin rug | 0.45–0.80 | 3.41–6.07 |

The mixed-household span is about **2.7–5.3 m/s²**. On tile at the target CoM it is **3.0–5.3 m/s²**.

Tipping still governs first **if the CoM target is hit**: `a_tip = 1.98` sits below `a_trac ≈ 3.0` even at the bottom of tile μ. Commanded `a_peak = 0.80–1.00` then has paper margin to tip, and more to traction.

They swap when `μ (1 − x/L) < x/h`, i.e. when `x` is far forward or μ is poor. At the target, the swap μ is `0.202 / 0.773 = 0.26` — below this household set. If `x_CoM` **collapses aft**, `a_tip` falls into or below the storyboard `a_peak` band and tipping remains the first limit, now **without margin**. That is not a traction gift. If `x_CoM` is pushed far forward, `N_drive` falls and traction can become the first limit on dirty tile. Screen both.

At HIGH (`x = 8.97 mm`, `L = 110 mm`): `N_drive/M = 0.918`, `a_trac` on tile ≈ 3.6–6.3 m/s², `a_tip = 0.905 m/s²`. Tip governs even earlier. Traction will not save a CoM miss.

### 3.3 Differential-turn scrub

In-place pivot at 170 mm track, 21 mm tread. Each drive wheel scrubs about a patch. Order-of-magnitude resisting torque **per wheel**, `E`:

```text
τ_scrub ~ μ · N_wheel · (tread / 3)
N_wheel = N_drive / 2 = 0.3865 M g     at the target CoM
tread/3 = 0.007 m
```

At the 2.40 kg demand mid, μ = 0.40–0.70:

```text
N_wheel = 0.3865 · 2.40 · 9.81 = 9.10 N
τ_scrub ≈ 0.40·9.10·0.007  to  0.70·9.10·0.007
        ≈ 0.025  to  0.045 N·m per wheel
```

Comparable to launch torque at the wheel (§4), not a rounding error. During `BM-06` spin and `BM-05` pivot this is a continuous scrubbing load, not a transient. It heats the tyre, yanks the caster, and is the floor of the `LP-04-SPIN` current. Treat the formula as `E` order-of-magnitude; the real patch is not `tread/3`. Do not use it to pick a motor.

### 3.4 Caster swivel / trail vs ball transfer

This is why Concept A vs B exists. Numbers here are comparable, not a winner.

| | Swivel caster with trail | Ball transfer |
|---|---|---|
| Forward roll | Low resistance if aligned | Higher rolling resistance `E` |
| `BM-07` reversal | The trail makes the caster yaw to the new heading; one-cycle heading glitch is expected | No trail, no swivel glitch |
| `BM-06` spin | Swivel + scrub; can walk if trail and μ fight the controller | Spins in place with higher drag |
| Soft floors | Kind | Can dent |
| Tip geometry | Contact patch moves as it swivels; `L` is not a fixed 110 mm during a reverse | Contact stays put |

A swivel caster with trail yaws during `BM-07` reversal and can produce a one-cycle heading glitch. A ball transfer has no trail but higher rolling resistance and can dent soft floors. Do not select either in this file. Carry both into `concepts/` with the §2 `a_tip` range and the §6 stopping table as the screens.

---

## 4. Drivetrain demand (from the storyboard export)

### 4.1 Kinematic conversion

```text
r = 0.042 m
circ = π · 0.084 = 0.2639 m
```

Speed at the 0.70 m/s design point:

```text
n = v / circ · 60 = 0.70 / 0.2639 · 60 = 159.2 RPM
```

Confirms the 160 RPM design point (G14). Unloaded design 160–200 RPM remains the screening window.

| Panel | `v` or `ω` | Wheel `v` | Wheel `n` |
|---|---|---:|---:|
| `BM-02` creep min / best | 0.04 / 0.08 m/s | 0.04 / 0.08 | **9.1 / 18.2 RPM** |
| `BM-04` follow cap | 0.45 m/s | 0.45 | 102.3 RPM |
| Follow hard ceiling | 0.50 m/s | 0.50 | 113.7 RPM |
| Max band | 0.70 m/s | 0.70 | 159.2 RPM |
| `BM-06` 220 °/s pivot | 220 °/s = 3.840 rad/s | `ω · track/2 = 0.326 m/s` | **74 RPM** |

Wheel speed at 220 °/s is 74 RPM — well under 160. `ω_peak` does **not** size the no-load RPM. `a_peak` and the 0.70 m/s band do.

### 4.2 Torque at the wheel

Two-wheel share, rolling resistance included, `C_rr = 0.025` `E`:

```text
τ_wheel = ((M a + C_rr M g) / 2) · r
```

| Corner | `M` | `a` | `M a` (N) | `C_rr M g` (N) | `τ_wheel` (N·m) `E` |
|---|---:|---:|---:|---:|---:|
| Low, min-viable launch | 1.65 kg | 0.80 | 1.320 | 0.405 | **0.036** |
| Mid, best-case launch | 2.40 kg | 1.00 | 2.400 | 0.589 | **0.063** |
| High, sensitivity | 3.624 kg | 1.20 | 4.349 | 0.889 | **0.110** |

The 2.40 kg row is a rounded demand mid, not the lumped NOM 2.559 kg. At 2.559 kg and `a = 1.00`, `τ_wheel = 0.067 N·m` — same class.

`a_peak` against the `a_tip` **range**, not against 2.0 m/s²:

| `a_peak` (m/s²) | TARGET 1.978 | LOW 1.115 | NOM 1.226 | HIGH 0.905 | LOW_FWD 1.896 |
|---|---|---|---|---|---|
| 0.80 min viable | margin 1.18 | margin 0.32 | margin 0.43 | **no margin** (0.80 vs 0.91 is paper-thin; do not call it margin) | margin 1.10 |
| 1.00 best-case | margin 0.98 | **exceeds** | **exceeds** | **exceeds** | margin 0.90 |
| 1.20 probe | margin 0.78 | exceeds | exceeds | exceeds | margin 0.70 |

Read this as: the storyboard 0.80–1.00 m/s² hypothesis has envelope margin only when `x_CoM` is restored toward the target. HIGH with the lumped CoM cannot be commanded at 0.80 m/s² without lifting the caster on paper. That is a ballast/placement problem, not a motor problem.

### 4.3 `BM-01` reaction hold

RP-01 paper yaw peak 0.1099 N·m (`E`) reacts into the base as a couple on the 170 mm track:

```text
F_wheel = 0.1099 / 0.170 = 0.646 N     (equal-and-opposite at the two contact patches)
τ_wheel = 0.646 · 0.042 = 0.027 N·m
```

Smaller than launch. Hold is a **static**, not peak, problem: current (or ratio, or a brake) at `v = 0`, for as long as the head performs. Free coasting reads as slop (MEM-20260812-08). Do not size the motor on 0.027 N·m and then discover launch is 0.06–0.11 N·m. Do not ignore 0.027 N·m because launch is larger — `BM-00`/`BM-01` fail by rolling, not by stalling a launch.

### 4.4 RMS over a representative follow minute

`BM-04`: `v = 0.45 m/s` cap, `a = 0.40 m/s²`. Mechanical power at the floor is `P = (M a + C_rr M g) · v` during accel and `C_rr M g · v` during cruise.

| | Low 1.65 kg | Mid 2.40 kg | High 3.624 kg |
|---|---:|---:|---:|
| Cruise `P` at 0.45 m/s | 0.18 W | 0.26 W | 0.40 W |
| Accel `P` at 0.40 m/s², 0.45 m/s | 0.48 W | 0.70 W | 1.05 W |

A follow minute is mostly cruise with sparse accel. Treat **0.4–1.4 W mechanical at the floor** as the `E` RMS band (cruise at the high-mass end through accel at the high-mass end, with room for a gentle arc's scrub). This is not a measured RMS and not an electrical wattage.

Electrical demand after gearbox and driver is a different class. Gearbox efficiency 40–70 % `E` for N20/JGA25 class; driver loss sits on top. Do **not** collapse `LG-04` below the §5 band because the floor-mechanical number is small. `0.4 W / 0.70 ≈ 0.6 W` at the optimistic end; `1.4 W / 0.40 = 3.5 W` at the pessimistic gearbox end, plus driver idle and scrub. The working electrical band is watts, not tenths.

### 4.5 Gear-ratio window

Wheel 160–200 RPM at 0.70 m/s. Motor no-load 3000–18000 RPM typical (`E` class window):

```text
n_motor / n_wheel = 3000/200 to 18000/200  →  15:1 to 90:1
```

Already inside hobby gearmotors. Screen the **output** RPM (loaded, at the wheel, at 0.70 m/s and at 0.04 m/s creep), not the motor nameplate RPM. A 150:1 N20-class unit may still make 160 RPM on a fast motor and fail creep or backdrivability for other reasons; that is a screen, not a selection.

### 4.6 Reflected inertia / backdrivability for `BM-00` / `BM-01`

Hold at `v = 0` can come from any of three places. State all three. Do not pick.

| Option | What it is | `BM-00` (unpowered / inhibited rest) | `BM-01` (armed, head performing) | Cost |
|---|---|---|---|---|
| **Ratio** | High reduction, residual gearbox friction | May hold unpowered — good for `BM-00` | Hold comes from ratio + friction; may still need some current against 0.027 N·m plus disturbance | Poor backdrivability. Pushing the robot for service fights the box. High-ratio N20-class (~150:1) is the picture. Idle current if you also actively hold |
| **Active hold** | Current at `v = 0` on a backdrivable box | Does **not** hold when inhibited/unpowered — `BM-00` fails unless something else is present | Works; needs a current loop that does not hunt | Idle energy on `LG-04`. Audible whine. JGA25-class ~20–50:1 is the picture |
| **Brake** | Mechanical hold, released when moving | Holds unpowered if the brake is default-on (check the fail-safe against `PA-13` / E-stop) | Holds without motor current | Extra mass inside the 200–600 g drive row; extra current/noise on release/engage; another fault row |

High-ratio N20-class (~150:1) is poorly backdrivable — hold comes from ratio + residual friction; costs idle current if actively held, but may hold unpowered (good for `BM-00`, bad if you need to push it). JGA25-class ~20–50:1 is backdrivable — `BM-00` needs active hold or a brake; `BM-01` needs current at `v = 0`. Cost: idle energy and audible whine.

Reflected inertia at the wheel grows with `N²`. A high-ratio box makes `BM-07` reversal a current spike and a heading glitch; a low-ratio box makes `BM-00` a brake-or-whine decision. Both are `E` class statements about classes, not SKUs. The drivetrain screen scores all three hold options against `LG-04` idle, acoustic §9, and the 200–600 g row. It does not pick one here.

---

## 5. Electrical demand for the ledger

### 5.1 Bus and current class

2S-class bus **6.0–8.4 V** is RP-02's `E` planning case, not a freeze. Do not treat 7.4 V as a selected pack.

Per-motor stall / launch / reversal: **1.5–3 A class** (`E`, unchanged decade). Composite both-motor stall: **3–6 A**.

Signed regen on `LP-04-REV` / `LP-04-BRAKE`: **0.3–1.5 A class** `E`, polarity **opposite** traction. Must be observable on `PB-DRIVE-L` and `PB-DRIVE-R` separately (`PA-13`). An unsigned current sensor that folds regen into "less traction" is not compliant.

`CC-PEAK-01`: drive share **20–40 W both** at stall/reversal still holds. At 6.0 V, 20–40 W is 3.3–6.7 A composite — the same 3–6 A class, touching the Korad ceiling.

### 5.2 Korad 5 A consequence

State it explicitly.

Two motors at **2.5 A** stall = **5.0 A**, at the KA3005D ceiling. Two motors at **3.0 A** = **6.0 A**, exceeds.

Therefore:

- Phase B stall/reversal characterisation is **per-motor**, or needs a second source.
- Both-motor transients close in **Phase C** on a candidate pack.
- Logic analyzer **never** on the motor rail (`workbench.md`).
- An electronic-load substitute reproduces a current-time trace, not inductive kick or regeneration. No stall, lift, or stopping claim from it.

### 5.3 Refresh proposal for `power-energy-ledger` (`E`, not `W`)

Propose these as revised `E` ranges. This file does not edit the ledger; the change-log row is a Part 2 follow-up.

**`LG-04` drive** — class remains `E`.

| Field | Proposed `E` | Why |
|---|---|---|
| Idle | 0 W inhibited | Motors not energized. Enabled-driver idle is not this row; do not call an armed-hold current "idle 0" |
| Average working | **2–8 W** | Mechanical 0.4–1.4 W at the floor; gearbox 40–70 % `E` plus driver bring it into this band. **Do not narrow below 2–8 W.** The previous 3–8 W band is compatible; the floor is lowered to 2 W so a quiet cruise is not treated as out-of-family |
| Peak | 20–40 W both stall/reversal | Unchanged |
| Current | 1.5–3 A per motor class | Unchanged decade |

**`LG-10` base MCU + safety sensing** — class remains **`U`** until a sensing candidate is on the bench. Do not invent a `W`.

| Field | Proposed `U` range | Why |
|---|---|---|
| Composition | C3 N8 + cliff / obstacle / IMU | C3 identity is selected; sensors are not |
| Idle | 0.25–0.50 W | DevKitC-1-N8 plus emitters dark / pulsed-off. Wider than the ledger's 0.2–0.4 W idle because a cliff emitter may not be fully off |
| Average working | 0.4–0.8 W | Hazard scan at 200 Hz with pulsed emitters |
| Peak | ≤ 1.0 W if emitters are pulsed; **≤ 1.2 W if ToF + IR all continuous (flag)** | The 1.2 W continuous case is a flag against `PB-SAFE-BASE` and against the "≤ 1 W" ledger line, not a permission to run continuous |

Drive mass **200–600 g**: physics does **not** move this bound. Do not ask the mass ledger to change. A brake, if chosen later, still has to fit inside it.

---

## 6. Stopping inequality per speed band

### 6.1 Latency budget

```text
d_stop = v · t_latency + v² / (2 · a_brake) + d_margin
```

Decompose `t_latency`:

| Term | Value | Class | Notes |
|---|---:|---|---|
| Sensor sample age | 20 ms | `E` | ToF frame or analog-IR settle. Digital cliff ~1–5 ms is faster; do not score with the fast number |
| C3 hazard scan period | 5 ms | `E` | 200 Hz target (T01) |
| Wheel-loop period | 2 ms | `E` | 500 Hz target (T02) |
| Driver response | 8 ms | `E` | C06 |
| **Sum** | **35 ms** | `E` | Under the 50 ms invariant |

**Score with `t_latency = 50 ms`** — the invariant, not the optimistic sum. A 35 ms paper sum is not evidence that the invariant has 15 ms of spare. Jitter, missed frames and a slow surface on analog IR eat it. If a later measured sum exceeds 50 ms, the invariant is the thing that stays; the sensing or the loop changes.

`a_brake` authored = **1.20 m/s²** (S07). Bounded above by nose-down 6.7 m/s² (does not govern) and by the `a_tip` **range** (governs **forward** accel; brake is the opposite transfer and does not lift the caster). `d_margin = 50 mm` `E` for floor; `40 mm` `E` for tabletop creep.

### 6.2 Floor table — `t = 50 ms`, `a_brake = 1.20 m/s²`, `d_margin = 50 mm`

Exact, then the millimetre table the screens use.

| `v` (m/s) | `v t` (mm) | `v²/(2a)` (mm) | margin (mm) | `d_stop` (mm) |
|---:|---:|---:|---:|---:|
| 0.05 creep | 2.5 → **3** | 1.04 → **1** | 50 | **54** |
| 0.15 | 7.5 → **8** | 9.4 → **9** | 50 | **67** |
| 0.40 | 20 | 66.7 → **67** | 50 | **137** |
| 0.50 follow cap | 25 | 104.2 → **104** | 50 | **179** |
| 0.70 max | 35 | 204.2 → **204** | 50 | **289** |

This table is what the sensing screen and the tabletop footprint are screened against. Look-ahead at the **leading contact** must exceed `d_stop` minus the sensor mounting offset (a sensor ahead of the contact is credited; a sensor behind it is charged).

### 6.3 Calibration / tabletop

At 0.05–0.06 m/s with the 40 mm tabletop margin:

```text
v = 0.05:  2.5 + 1.0 + 40 = 43.5 mm
v = 0.06:  3.0 + 1.5 + 40 = 44.5 mm
```

With the 50 mm floor margin at 0.05 m/s, `d_stop = 54 mm`. Cliff look-ahead at calibration speed is the **45–54 mm** band. §7 uses this at each leading contact.

---

## 7. Obstacle and edge coverage geometry

### 7.1 Leading contacts

Stance 205 mm + turn sweep. Leading contacts, from the drive axle:

| Direction | Leading contact | Offset from axle | Offset from centreline |
|---|---|---|---|
| Forward | Caster | **110 mm ahead** | 0 |
| Lateral | Wheels | **0 mm ahead** | **85 mm** off centre |
| Reverse | Skid | **70 mm behind** | 0 |

### 7.2 Forward obstacle look-ahead

From **caster contact**, using §6.2:

- ≥ **179 mm** at 0.50 m/s
- ≥ **289 mm** at 0.70 m/s

A sensor mounted at the axle needs that **plus 110 mm** (289 → 399 mm at 0.70 m/s; 179 → 289 mm at 0.50 m/s). A sensor mounted at the caster needs `d_stop` itself. Do not credit an axle-mounted ToF with caster-contact look-ahead.

### 7.3 Lateral / pivot

During a pivot the shoulder sweeps a `205/2 ≈ 102 mm` radius from centre. Coverage must include that sweep **plus** `d_stop` at the pivot-equivalent tangential speed.

At 220 °/s, wheel `v = 0.326 m/s`:

```text
v t     = 0.326 · 0.050 = 16 mm
v²/(2a) = 0.1063 / 2.40 = 44 mm
d_margin              = 50 mm
d_stop                = 110 mm   →  ~120 mm class
```

A sensor that only looks forward along the body axis does not cover a furniture leg at the shoulder during `BM-05`/`BM-06`. Carry this into the sensing screen as a coverage hole, not as a SKU.

### 7.4 Blind-region tolerance

A **20 mm square by 20 mm tall** object at floor level in the caster's shadow is the failure mode. The caster body, fork and any bumper hide a near-floor volume that a forward-looking sensor on the axle never sees. Bump bar is the **last** layer, not the first. Do not close G03 with bump-only at follow speed.

### 7.5 Cliff look-ahead — count and where, before any part is named

At each leading contact, at calibration speed 0.05–0.06 m/s: `d_stop ~ 45–54 mm`. Need downward sensors that see the floor disappearing at least **~40 mm before that contact arrives**.

That fixes **count and where**:

- **Caster-forward** look-down — the forward leading contact.
- **One covering reverse / skid** — `BM-08` and any rearward creep. The skid is 70 mm behind the axle; a forward-only cliff does not see a rear edge.
- **Wheel-adjacent downs** — the lateral / turn case. During a pivot the wheel is the leading contact.

**Minimum three look-down channels.** A single forward cliff is not enough. A perimeter ring is Concept B, not a requirement yet.

Dark or glossy tabletop is the cliff failure mode to test, not an afterthought. Analog IR in the stop path and ToF as telemetry are different architectures (§10 / Part 3); this file does not pick.

---

## 8. Tabletop footprint proposal for CON-TBD-14

**Proposed, not registered.** Registration waits on G04 freeze and BD-01 / BD-07. Ordinary come / follow / spin are never granted in `OM-02`.

| Item | Proposal | Derivation |
|---|---|---|
| Marked circular radius | **250 mm** (diameter 500 mm) on the tabletop | Calibration `d_stop ~ 45 mm` plus caster 110 mm plus a place to stand the robot at rest without already sitting on the mark. Not a scored stopping radius |
| Calibration speed ceiling | **0.06 m/s** | `BM-11`; S08 |
| Stopping margin | **40 mm inside the mark** | C08 |
| Edge-test headings | Approach the mark at **0, 45, 90, 135, 180°** relative to heading | Hits caster, wheel and skid as leading contact |
| Surfaces | **Dark and glossy** samples | Cliff failure mode |
| Catch fixture | Outside ~**300 mm** radius | Must **not** sit in the cliff sensors' view (**BD-07**) |
| Permission | Armed `CC-12C` only | `OM-02` inhibited-by-default |

A 250 mm radius is not "the robot may move 250 mm". It is the marked validated circle inside which an armed calibration creep is permitted, with a catch beyond it. If BD-01 later removes moving tabletop from V1, this proposal remains the geometry against which unintended-activation edge sensing is proven, and the catch still exists.

---

## 9. Acoustic and vibration note

MEM-20260812-04: drivetrain vibration reaches all body mics coherently; beamforming does not fix it. This is structure-borne, near-simultaneous energy, not a far-field source to steer away from.

**Measurement obligation** (not a design): record sound level at a **fixed position** during `BM-04` (follow / cruise) and `BM-06` (spin / scrub). Same position, same instrument, both panels, both load corners if BD-05 asks for them. Log it on the common timebase when that exists; until then, a session note with the instrument identity.

No isolation design in RP-03. Inhibit / isolation is a later body decision (MEM-20260812-05 already created a locomotion-inhibit request for listening). Do not invent a dB number. Do not treat a quiet bench motor-on-a-stand as the body-array number.

---

## 10. What this file does not do

- No motor SKU.
- No sensor SKU.
- No caster SKU, no ball-transfer SKU, no skid SKU.
- No single `a_tip`.
- No pass threshold.
- No purchase.
- No freeze of 14 mm skid height, 70 mm skid reach, 2.0 m/s², 3–8 W, or CON-TBD-14.
- No quiet shrinking of commanded `a_peak` to hide a CoM miss.
- No `W` row. Every computed newton, watt and millimetre in this file is `E` or is inherited `D`/`E`/`U`.

---

## Implication for Part 3

Concepts **must** differ on (1) swivel caster vs ball transfer (scrub / `BM-07` reversal), (2) battery / motor placement vs the 110 mm wheelbase (the CoM lever that decides whether `a_tip` is ~0.9 or ~1.9 m/s²), (3) 3-look-down vs perimeter ring, (4) analog-IR-in-the-stop-path vs ToF-as-telemetry. Screens against the §6 stopping table and the §2 `a_tip` **range**, not against 2.0 m/s². A concept that only exists at the placement target has not been compared; a concept that quietly assumes a rear battery is already HIGH_AFT and is not a concept. The drivetrain screen then names `D01…` against this envelope without becoming a freeze; the sensing screen names `S01…` against coverage and the 50 ms invariant, never because a driver board happened to have the pins.
