# RP-03 Concept B — Ball transfer, perimeter cliff, ToF telemetry

| Field | Value |
|---|---|
| Status | **Paper concept v0.1. Comparison retained — not waived, not a winner, not a purchase** |
| Created | 2026-09-17 |
| Owner | Project builder |
| Comparison | [`README.md`](README.md) |
| Counterpart | [`swivel-caster-three-lookdown.md`](swivel-caster-three-lookdown.md) (working lead after the matrix; not a freeze) |
| Consumes | `../physics.md` ranges; `../storyboard.md`; dimensional baseline v1.10 |
| Does not contain | CAD; a SKU freeze; a claim that no-trail makes `BM-07` free; a claim that ToF may be the sole stop-path |

Concept B exists to keep three questions honest: (1) is the `BM-07` heading glitch a swivel-trail problem or a controller problem; (2) does a perimeter ring earn its GPIO; (3) does putting motors *into* the 110 mm wheelbase recover `x_CoM` cheaper than sliding only the battery. It is **not** “Concept A plus more sensors.” The stop-path architecture is different on purpose: **ToF is telemetry only; obstacle stop-path is the GPIO bumper.** That is a real coverage cost at 0.50 m/s, not an oversight.

HIGH_AFT is still forbidden. The battery still sits low and forward of the axle.

## 1. Napkin geometry

Same inherited envelope (Ø84, 170 track, 110 WB to **front-support contact**, skid start 70 mm). Different support, different mass placement, different sensing ring.

```text
TOP  (+x up the page)

                         ball-transfer contact  x = +110 mm
                         Ø1 inch (25.4 mm) ball in a cup
                              ●   NO trail — contact stays put
                              |   higher rolling resistance  E
                     battery  |   U-tray around the cup
                     tray     |   pack CoM x = +60…+85 mm, h = 18–32 mm
                              |   LOW and FORWARD of the axle
                    motors hung INTO the wheelbase
                    motor CoM x ≈ +20…+35 mm  E
                    (coupling / shaft to the axle  U)
                              |
         y = +85          y = 0              y = −85
           ●==============● axle ===============●
         L wheel        x = 0, h ≈ 42         R wheel
         Ø84 × 21                             Ø84 × 21
                              |
                              ▬  skid  x = −70 mm (adjust 60–80)
                                 h_skid = 8–16 mm

         PERIMETER LOOK-DOWNS (4+):
           C  caster/ball-forward
           L  left shoulder / wheel-adjacent
           R  right shoulder / wheel-adjacent
           S  skid / reverse
           (optional fifth at a diagonal — GPIO cost)

         ToF looking +x  — I2C telemetry, NOT stop-path
         bump bar spanning stance — GPIO stop-path obstacle
```

| ID | Quantity | Napkin value | Class | Notes |
|---|---|---|---|---|
| G01 | Drive wheels | Ø84 × 21 mm | `E` | Same spec band as A. Hub must match whatever coupling reaches the axle |
| G05 | Track | 170 mm | `E` | Unchanged. Spin scrub is still a tyre problem |
| G06 | Wheelbase `L` | 110 mm to **ball contact** | `E` | Contact stays put (unlike a swivelling caster), so `L` is more nearly constant during reverse |
| — | Front support | Ø1 inch ball transfer (`D21`) | `E` class | Paper identity of this concept. **V1 also uses `D21`**, but on the Concept A chassis (BD-08) — not with this file's ring or bump-only stop. Soft floors / pile can dent or jam. Rolling resistance `U` |
| G08/G09 | Skid | 60–80 mm reach, 8–16 mm height | `E` | Same inequality as A. Ball height vs skid height must still satisfy `h/d < x/h` at the scored CoM |
| — | Motor placement | Inboard, into the WB; CoM `x ≈ +20…+35` mm | `E` | First-order axis vs A. Adds a +`x` lever; adds a coupling. Coupling mass/compliance `U` |
| — | Battery bay | U-tray around the ball cup, `x = +60…+85`, `h = 18–32` | `E` | Still forward of the axle. Competes with the cup for floor area. HIGH_AFT excluded |
| — | Cliff ring | 4+ look-downs on the stance perimeter | `E` | First-order axis vs A's 3 |
| — | Obstacle | ToF telemetry + bump stop-path | `E` | First-order axis vs A's analog-IR stop-path |
| — | Neck / demate | Same as A: up through neck void, demate at body | `E` | Architecture is not allowed to differ here |

No CAD. Ball-cup depth, coupling type (timing belt, D-shaft extension, gear) and ring bracketry are `U`. Do not draw a winner from a prettier napkin.

## 2. Load path

Same four cases, different front support.

| Case | Difference from Concept A |
|---|---|
| **1. Forward launch** | Ball does not swivel-unload the way a trailed caster does; the contact stays at `+L`. Tip physics is still `a_tip = g·x/h` on the **range**. The ball cup must take residual front share without the fork's trail moment. Skid remains the catch |
| **2. Forward brake** | Nose-down onto the **ball**. Point contact vs a caster's tyre patch: higher contact stress `E`, dent risk on wood. `a_brake,tip` still ~6.7 m/s² at TARGET; authored 1.20 m/s² does not govern tip, but it can govern **denting** |
| **3. Reverse launch** | Still not the dual of forward. Ball cannot “flop” a trail, so the reverse heading is cleaner; the robot can still rotate over the front contact if `a` is silly. Skid still does not catch a forward flip |
| **4. Spin** | **No trail glitch.** The ball is a spherical contact that scrubs in place. Drag is higher `E` than an aligned caster. `LP-04-SPIN` current floor may sit above A's. Lateral tip still does not govern at 220 °/s |

Floor-load path: drive patches → axle bearings → (coupling) → inboard motors. Front share → ball cup → deck. Catch → skid. Motor reaction is inboard of the axle; the coupling carries torque and must not be the compliance that `BM-07` through-zero sees. If the coupling winds up, Concept B fails `DECEL0` for a reason A does not have.

Head-yaw reaction into the track is unchanged: `0.027 N·m` per wheel `E`. Hold is still a static problem. Inboard motors do not create a brake.

## 3. Actuator class (not a SKU freeze)

**Same JGA25-class as Concept A.** The concepts are not allowed to differ by silently swapping in 37D or N20; those are screen bounds, not B's identity. Demand at the wheel is the same `0.036–0.110 N·m` plus **higher rolling resistance** of the ball `U` and the coupling loss `U`. Do not treat A's Oz 0.083 N·m rated figure as extra margin until those terms are bounded.

| Item | Concept B note |
|---|---|
| P01 torque | Class still screens on Oz/NFP tables. Add an `E` allowance for ball `C_rr` above 0.025 and coupling efficiency. Until those are numbered, B does **not** claim a better torque margin than A |
| P02 speed | Same 160–200 RPM band at Ø84. Coupling ratio 1:1 unless a later screen says otherwise — do not hide a 45:1 motor behind a further reduction |
| P04 encoder | Encoder is on the **motor**. Coupling backlash appears as a deadband at the wheel. `BM-07` ≤ 80 ms visible stop at zero is the quality hypothesis this joint can fail |
| P05 hold | Still backdrivable JGA25-class. Active hold. Coupling friction is not an acceptable `BM-00` brake |
| P06 mass | Motors ~170–220 g **plus** cup, ring brackets, coupling. Upper half of 200–600 g `E`. A 37D swap is still rejected by the row |

Ball transfer is `D21`. On this concept it rides with the ring and bump-only stop. On the selected V1 path it rides on the Concept A chassis (BD-08). Skid `D30` unchanged. Wheels `D10` unchanged.

## 4. Cable route to the body

Identical rule: **up through the neck void, demate at the body.**

The ring adds conductors on the chassis side:

```text
4+ cliff pigtails + bump + ToF I2C + IMU SPI+INT + drive/encoder/nFAULT/enable
        → chassis harness (ring is the expensive part)
        → neck-void trunk
        → body demate
```

ToF on I2C may share a bus with other **telemetry**. It may not share a GPIO expander with cliffs. Cliffs remain native GPIO. If the ring is 5–6 channels, the Part 4 map is the thing that fails, not the expander rule.

Motor power still splits `PB-DRIVE-L/R` with signed observability. Inboard motors make the motor leads shorter and the encoder leads longer, or the reverse, depending where C3 sits — C3 sits in the **body**, so both are trunked. Do not relocate C3 into the base tub to save pins; that splits the safety authority from the body demate.

## 5. Service story

| Action | How |
|---|---|
| Clean the ball | Scheduled. Hair, grit and laminate dust pack a cup. A seized ball is a **fixed** front contact with high μ — `BM-06` walks, `BM-07` yanks. This is B's caster-equivalent maintenance |
| Swap the front support | Cup drops out of the deck the way A's fork does. The rig's interchangeable front support is how A and B share a frame (`plan.md` §6) |
| Service a motor | Inboard + coupling: worse than A's outboard-on-axle. Two joints (motor, coupling) instead of one |
| Ring channel dies | More pigtails. Interposer still required for `F-19`. A ring that cannot mask one channel without dropping the lot is not a serviceable ring |
| Body demate | Same keyed trunk as A |
| Push for service | Same backdrivable warning as A; chock the wheels when inhibited |

Dent inspection after any wood/laminate session is part of B's story. A dented floor is a `BD-04` surface change, not a rounded-off result.

## 6. Physics quantities — screened with margin, as ranges

Same envelope as A. Different recovery lever, different coverage hole.

### 6.1 `a_tip` range vs authored `a_peak`

Battery-forward is still the lever (`∂a/∂x = 79.1 s⁻²` at the target: +10 mm → +0.79 m/s²). Concept B adds a **small** extra +`x` from motor mass in the wheelbase.

Order-of-magnitude only (`E`): two motors ~0.22 kg at `x = +30 mm` add `6600 g·mm` to `Σ(mx)`. On the LOW 1649 g article that is +4.0 mm of `x` — not nothing, not a substitute for the battery bay. On HIGH 3624 g it is +1.8 mm. Head height still sits at ~250 mm and still dominates `h`.

**Do not claim B wins `a_tip`.** Coupling mass, a taller ball cup, and a U-tray that lifts the pack to clear the cup can spend that +`x` on +`h`. Screen the same table as A until the rig measures:

| Case | `a_tip` (m/s²) `E` | B-specific note |
|---|---:|---|
| LOW / NOM / HIGH lumped | 1.115 / 1.226 / 0.905 | Unchanged until coordinates are re-lumped with motor `x > 0` and cup height |
| HIGH_AFT | −0.111 | **Still forbidden.** Inboard motors do not license a rear pack |
| LOW_FWD | 1.896 | Still the recovery case; B may sit slightly above this if motors stay at +`x` **and** `h` does not grow |
| TARGET | 1.978 | Placement target, not a roll-up. Not `2.0 m/s²` as a property of Layout 03 |

Authored `a_peak` 0.80 / 1.00 m/s² still has no margin at HIGH lumped `0.905`. B does not get to command 1.00 because the ball “feels stable.”

Skid inequality is unchanged: `14 mm @ 70 mm` fails lumped CoMs. Adjust 60–80 / 8–16.

### 6.2 Stopping table — the coverage hole this concept accepts

| `v` (m/s) | `d_stop` (mm) | Concept B coverage |
|---:|---:|---|
| 0.05–0.06 calibration | ~40 mm look-ahead at **each** leading contact | **Better than A on headings**: ring covers caster, both wheels, skid without arguing about “one lateral.” Dark/glossy remains the failure mode on every channel |
| 0.50 follow cap | **179** from front contact | ToF *can* range past 179 mm (`D`, VL53-class) but is **I2C telemetry**, not the stop path. Bumper does not look 179 mm ahead. **`d_stop` coverage at 0.50: FAIL / HOLD as a G03 architecture** unless analog-IR is added — which would erase first-order axis 4 |
| 0.70 design point | **289** | Same hole, larger. ToF as redundant look-ahead is useful for logging; it must not be wired as the sole inhibitor |
| Pivot 220 °/s | ~120 class at the shoulder | Ring **does** cover shoulders. This is B's clean win versus A's single lateral |

Blind-region 20 mm cube: a ball cup is a different shadow than a caster fork. Still a near-floor volume a bumper may miss at follow speed. Do not close G03 with bump-only (`physics.md` §7.4).

### 6.3 Wheel torque, encoder, current, mass

| Quantity | Envelope | Concept B | Result |
|---|---|---|---|
| `τ_wheel` | 0.036–0.110 N·m plus ball drag `U` | JGA25-class stall/rated as A, minus coupling and extra `C_rr` | Class still plausible; **margin not claimed better than A** |
| Encoder creep | ≲ 2 mm/count, ≳ 20 c/s | Same motor CPR; coupling backlash `U` | Motor-class PASS; wheel-class HOLD until backlash is bounded |
| Current | 1.5–3 A class; Korad 5 A | Same P03 HOLD (Oz 0.9 A vs NFP ≤ 3 A). Spin/wiggle current may run higher than A because of ball drag | Do not average the conflict |
| Mass | 200–600 g | Upper half `E` (cup + ring + coupling) | Must still fit. Physics does not enlarge the row |
| `BM-07` trail | Heading glitch vs drag | **No trail glitch**; drag and possible dent/walk instead | Different failure. Not a free quality win |

### 6.4 Sensing architecture

| Function | Channel | Interface | Stop-path? |
|---|---|---|---|
| Cliff ring | 4+ look-downs on the perimeter | GPIO each | **Yes** |
| Obstacle | VL53-class ToF forward | I2C | **No** — telemetry / redundant look-ahead |
| Bump | Lever spanning stance | Direct GPIO | **Yes**, and in this concept it is the **only** obstacle stop-path layer |
| IMU | SPI + INT | SPI + interrupt | Same as A |
| Analog IR | Not part of B's identity | — | Adding it collapses the comparison axis |

C3 GPIO: 4+ cliff + bump + IMU SPI+INT + 2 nFAULT + enable. Spare ≥ 2 is **at risk**. Part 4 either drops a diagonal channel, moves to a WROOM-1-N8 carrier under change control, or B is only exercisable on the rig with a harness that the installed map will not carry. It never falls back to a GPIO expander, and never to N8R8.

Age bounds `E`: cliff GPIO 10 ms; bump 5 ms; ToF sample 20–50 ms (telemetry; must not be scored as if it were the 50 ms stop-path); IMU 10 ms. Unknown = inhibit.

Dark/glossy tabletop is still the cliff failure mode, on more channels.

## 7. Why this stays a comparison

Concept A is the working lead because it has a stop-path obstacle sensor that can cover `d_stop` at 0.50 from the front contact, a cliff count that matches the leading-contact minimum without spending the spare GPIO, and a motor placement that does not add a coupling to `BM-07`.

Concept B is retained because:

1. `BM-07` trail is `U`. If A's heading glitch is unfixable in firmware, the ball is the experiment, not a regret.
2. A single lateral look-down can miss a heading. The ring is how that is falsified.
3. Motor-in-WB is a real CoM lever. It is worth one lumped re-evaluation on the rig, not a paper win.

It is not waived. It is not the lead. It is not a purchase.

## 8. What this file does not do

- Does not authorize a ball-transfer SKU.
- Does not permit ToF as the sole obstacle inhibitor.
- Does not permit HIGH_AFT.
- Does not claim `a_tip` better than A.
- Does not freeze a 4- vs 5- vs 6-channel ring.
- Does not pass G03 by writing “ToF range is 1.2 m.”
