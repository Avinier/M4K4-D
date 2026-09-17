# RP-03 Drivetrain Candidate Screen — D01…

| Field | Value |
|---|---|
| Status | **Paper screen complete v0.1. No motor selected. No freeze. No purchase.** `D02` is a **lead for a reference unit (bench)**, not a freeze |
| Date | 2026-09-17 |
| Scope | Named gearmotor / wheel / caster / skid / driver-**class** rows `D01…` screened against `physics.md` demand. Exact driver IC lead is a Part 4 name; Part 3 screens the class |
| Inputs | `physics.md` §4–5 (torque 0.036–0.110 N·m, 160–200 RPM, 1.5–3 A class, Korad 5 A `D`, drive mass 200–600 g); `storyboard.md` `BM-00…BM-07`; `concepts/` working lead Concept A (JGA25-class, caster D20); Concept B comparison (ball D21) |
| Evidence | Manufacturer / vendor tables `D`. India Robu / Zbotic 2026-09-17 snapshot is availability, not a rating. Prices ranges `E`. Exact SKU stock `U` |
| Excluded | A freeze; a mass row promoted past `E`; purchase; HIGH_AFT packaging; treating `2.0 m/s²` as the robot's `a_tip` |

Same discipline as RP-01's first actuator screen and RP-02's power-component screen: a datasheet rectangle is not installed behaviour, a conflict between two `D` tables is not averaged away, and a lead is not a selection.

## 1. Paper gates

A missing value is not a pass. Score against the **range**, not against `2.0 m/s²`. Wheel radius `r = 0.042 m`, circumference `0.2639 m` (`physics.md` G01–G03). `0.70 m/s = 159.2 RPM` on Ø84 — confirms the 160 RPM design point.

| Gate | Question | Pass rule |
|---|---|---|
| **RP03-P01 torque** | Wheel `τ` vs **0.110 N·m** high-mass launch and **0.063 N·m** nom | **Pass** if stall `D` ≥ **2× 0.110 = 0.220 N·m** **and** rated `D` ≥ nom **0.063 N·m**. Else HOLD/FAIL |
| **RP03-P02 speed** | Output no-load in **160–200 RPM** at the 6 V or 12 V case used | In-band pass. Below 160: HOLD (state the Ø84 speed). Above 200: HOLD/FAIL. High-ratio 14–15 RPM is FAIL. `0.70 m/s` is a drivetrain design point, not a storyboard command |
| **RP03-P03 current** | Per-motor stall in **1.5–3 A class?** **and** both-motor vs Korad **5 A** `D` | If stall `D` is **0.9 A**, note it is **below** the ledger class (better electrically) but **cite any conflict**. If stall `D` is **3 A**, both-motor **6 A** exceeds 5 A → Phase B **per-motor**. Do not average two `D` tables |
| **RP03-P04 encoder vs BM-02 0.04 m/s** | Need **≲ 2 mm/count** and **≳ 20 counts/s** | 11–12 PPR motor Hall × 35:1 ≈ 385 CPR → **0.69 mm/count, ~58 c/s PASS**. **12 CPR at the wheel FAIL** (22 mm/count) |
| **RP03-P05 backdrivability vs BM-00/01** | Where does `v = 0` hold come from? | High-ratio N20 poorly backdrivable (passive hold, hunt risk). JGA25 ~35:1 **backdrivable** (needs **active hold**). State the cost. Do not pick a brake here |
| **RP03-P06 mass** | Two motors + wheels + caster/ball + skid + brackets inside **200–600 g** | Physics does **not** move this bound. A brake, if chosen later, still fits inside it |

Conversion used throughout: `1 kg·cm = 0.0981 N·m` (`g` conventional `D`). Encoded arithmetic is `E` from `D` counts and inherited circumference.

## 2. Disposition vocabulary

| Label | Meaning |
|---|---|
| **Lead** | Best presently documented route into **bench** evaluation; not selected, not frozen |
| **Conditional** | Admissible only if the stated evidence closes |
| **Bench-only** | Useful for characterization; missing an installed-product requirement |
| **Hold** | Potentially admissible; an upstream number or conflict is unresolved |
| **Reject** | Fails a current paper gate for the stated use, or is the wrong bound |

## 3. Outcome (not a selection)

| Function | Lead carried forward | Disposition |
|---|---|---|
| Gearmotor | JGA25-370-class 6 V ~176 RPM 1:35 with AB Hall (`D02`) | **Lead for reference unit (bench), not a freeze.** P03 HOLD on stall-current conflict |
| Gearmotor lower bound | N20-class (`D01`) | **Reject / lower-bound Hold.** Bins that hit 160–200 RPM fail P01 at 0.110; bins that stall hard fail P02 |
| Gearmotor comparison | JGA25 6 V 133 RPM 1:45 (`D03`) | **Comparison / P02 HOLD.** 0.58 m/s on Ø84 still above follow 0.50 |
| Gearmotor upper bound | 37D-class 12 V ~150–200 RPM (`D04`) | **Hold / upper bound**, not lead. Mass eats the drive row |
| Wheels | Ø84 × 21 mm rubber/TPU, 4 mm or 6 mm hub (`D10`) | Spec band, not SKU |
| Front support A | Ø25–32 mm swivel (`D20`) | Spec band; trail `U`. Concept A |
| Front support B | Ø1 inch ball transfer (`D21`) | Concept B **only** |
| Skid | Printed polymer or PTFE pad (`D30`) | Adjustable 60–80 mm reach, 8–16 mm height |
| Driver class | TI DRV8874 (`DRV-B`) | **Lead class** (two chips, L/R observability). Exact part is Part 4 |
| Driver class | TB6612FNG (`DRV-A`) | **Hold** — fails if stall is 3 A `D` |
| Driver class | Cytron MDD3A (`DRV-C`) | **Bench-only** evaluation board, India-common, not a freeze |

## 4. Gearmotor candidates

### 4.1 `D01` — N20-class 6 V encoder

**Class, not one SKU.** Typical hobby N20 with 12–14 CPR Hall, mass ~30–50 g, stall current **0.36–1.6 A** depending torque bin (Xinhe LP/MP/HP).

**`D` sources (2026-09-17 retrieval):**

- Xinhe **N20L** tables: [N20L encoder gear motor](https://www.xinhe-motors.com/sale-55271345-n20l-12v-6v-dc-micro-encoder-gear-motor-with-spur-gearbox-for-stem-robots-rc-toys.html). 5:1 → 2500 RPM, stall 0.05 kg·cm; **1000:1 → 14 RPM**, stall 5.0 kg·cm. Stall-current bins quoted **360 / 700 / 1600 mA**. Encoder listed as 12 CPR **or** 3 PPR depending paragraph — treat CPR location (motor vs wheel) as `U` until the article is in hand.
- [robotics.org.za N20 15 RPM 6 V encoder](https://www.robotics.org.za/N20-15RPM-ENC-6V): no-load **15 RPM**, stall **4 kg·cm = 0.392 N·m**, stall current 1 A, encoder **14 CPR**.

**Honest screen of the bins that look tempting:**

| Bin | No-load | Stall `τ` | P01 | P02 | Notes |
|---|---|---|---|---|---|
| N20L5 5:1 | 2500 RPM | 0.05 kg·cm = **0.0049 N·m** | **FAIL** | **FAIL** (far above 200) | Weak stall |
| N20L75 ~75:1 | **170 RPM** (in 160–200) | 0.8 kg·cm = **0.078 N·m** | **FAIL** (0.078 < 0.110, far from 2× 0.220) | Pass band | The “100–200 RPM N20 exists” row. Stall typically **< 0.15 N·m** |
| N20L100 | 120 RPM | 1.0 kg·cm = 0.098 N·m | **FAIL** | **FAIL** (< 160) | |
| N20L1000 | **14 RPM** | 5.0 kg·cm = 0.490 N·m | Stall number would pass 2× | **FAIL P02** | High-ratio; poorly backdrivable (P05) |
| robotics.org.za 15 RPM | **15 RPM** | 4 kg·cm = 0.392 N·m | Stall ≥ 0.220 | **FAIL P02** | User-cited bound; 15 RPM is not 159 RPM |

Xinhe **N20H** high-torque tables quote e.g. N20H150 at 200 RPM, 3.0 kg·cm = 0.294 N·m stall (would clear P01 stall 2×) at **1600 mA** and ~150:1. That bin is poorly backdrivable (P05), thermally a different motor, and still not the common India N20. Do not treat it as the class. If someone later benches it, it is a new `D0x` row.

**P04:** If 12–14 CPR is **at the wheel**, mm/count = `263.9/12 ≈ 22 mm` — **FAIL**. If 12 CPR is motor-side × 75:1 ≈ 900 CPR, P04 would pass — **`U` until the pinout is the article's pinout.** Xinhe's mixed 3 PPR / 12 CPR listing is the warning.

**P05:** High-ratio N20 is poorly backdrivable: residual gearbox friction may hold unpowered (`BM-00` friend) and hunt or feel like a limp when forced through zero (`BM-07` enemy). Not Concept A's class.

**P03:** 0.36 A LP is below class; 1.6 A HP is in class; both-motor 3.2 A still under 5 A. Current is not why D01 fails.

**P06:** Two motors ~60–100 g — mass is the one gate it would pass.

**India snapshot 2026-09-17.** N20 6 V / encoder class on Robu / Zbotic (example: [Zbotic N20 6 V 15 RPM 1:1000](https://zbotic.in/product/high-torque-n20-6v-15rpm-micro-dc-metal-gear-reduction-motor-reduction-ratio-11000/) is the P02-fail bin). Price band `E` ₹200–800. Stock `U`.

**Disposition: Reject as the drive lead / retain as lower-bound comparison.** Likely FAIL P01 at high-mass 0.110 N·m **or** FAIL P02. Do not buy a 15 RPM or 1000:1 N20 for RP-03 motion.

### 4.2 `D02` — JGA25-370 / JGA25-370B 6 V 176 RPM 1:35 (reference unit)

**Identity for the screen:** 25 mm gearmotor class, **4 mm** D-shaft, encoder AB Hall, ~**110 g** with encoder (NFP) / ~85 g without (Open Impulse — encoder article is the one that matters).

**`D` Oz Robotics table** — [JGA25-370B 6 V 176 RPM 1:35](https://ozrobotics.com/shop/micro-dc-encoder-deceleration-motor-jga25-370b-25mm-motor-6v-176rpm/):

| 6 V | rpm | Current | Torque |
|---|---:|---:|---|
| No-load | **176** | 80 mA | — |
| Rated | 150 | 380 mA | **0.85 kg·cm = 0.083 N·m** |
| Stall | — | **900 mA** | **5 kg·cm = 0.490 N·m** |
| Ratio | 35:1 | — | gearbox length 21 mm |

Open Impulse repeats the same endpoints and lists **85 g** without calling the encoder: [JGA25-370 176 RPM 6 V](https://www.openimpulse.com/blog/products-page/25d-gearmotors/jga25-370-dc-gearmotor-176-rpm-6-v/).

**`D` NFP-GM25-370-EN** — [NFP 25 mm metal gear motor](https://nfpmotor.com/25mm-metal-gear-motor-model-nfp-jga25-370-en) / [NFP shop table](https://nfpshop.ch/product/25mm-metal-gear-motor-model-nfp-gm25-370-en):

| Item | Value |
|---|---|
| Mass | appr. **110 g** |
| Shaft | 4 mm |
| Encoder | AB Hall, 3.3/5 V, **11 PPR motor**; 4.4:1 → **48.4 PPR** so ~11 PPR × ratio |
| 34:1 ~ 6 V | no-load 175 RPM; rated 1.3 kg·cm / 130 RPM / ≤0.5 A; stall **4.5 kg·cm**, **≤ 3 A** |
| 20:1 6 V | stall **≤ 3 A** (the cited conflict row) |
| 45:1 6 V | stall 6 kg·cm, ≤ 3 A, no-load 130 RPM |

**P01:** Oz stall 0.490 ≥ 0.220 (**2.23×**); Oz rated 0.083 ≥ 0.063. NFP 34:1 stall 4.5 kg·cm = 0.441 ≥ 0.220; rated 1.3 kg·cm = 0.127 ≥ 0.063. **Pass on both `D` tables.** Not a freeze.

**P02:** Oz no-load **176 RPM** in 160–200 at the **6 V** case. **Pass.** NFP 34:1 175 RPM same band; NFP 45:1 130 RPM is `D03`.

**P03: HOLD.** Oz stall **900 mA** is **below** the 1.5–3 A ledger class — better electrically, both-motor 1.8 A under Korad 5 A. NFP stall **≤ 3 A** is inside the ledger class — both-motor **6 A exceeds 5 A** → Phase B per-motor. **Both are `D`. Do not pick. Do not average.** Screen as HOLD until the **purchased article is metered**. If the article is 0.9 A, record that the ledger class was conservative. If it is 3 A, Korad consequence is the `physics.md` §5.2 paragraph, not a surprise.

**P04: PASS (class arithmetic).** 11 PPR × 35:1 ≈ **385 counts/rev**. `263.9 mm / 385 = 0.686 mm/count` ≈ **0.69 mm/count**. At 0.04 m/s: `0.04 / 0.2639 × 385 ≈ 58 counts/s`. Both ≲ 2 mm/count and ≳ 20 c/s. NFP 34:1 lists 374.11 PPR — same class. **12 CPR at the wheel would FAIL; that is not this encoder.**

**P05:** 35:1 JGA25-class is **backdrivable**. `BM-00` inhibited/unpowered **will not hold** — chock, or fail the ~2 N nudge. `BM-01` needs **active hold** current at `v* = 0` (RP-01 0.1099 N·m → 0.027 N·m/wheel, smaller than launch but continuous). Cost: idle energy on `LG-04` when armed; audible whine risk. Hunt is a current-loop problem, not a ratio gift.

**P06:** Two motors ~**220 g** (110 g × 2 `D` NFP). + Ø84 wheels + caster + skid + brackets → **350–500 g `E`**, inside 200–600 g. Open Impulse 85 g × 2 is the no-encoder article; do not use it to “make mass.”

**India snapshot 2026-09-17.** JGA25-370 / GA25 / “25 mm encoder gear motor 6 V ~170 RPM” class on Robu / Zbotic. Price band `E` ₹400–1 200. Exact suffix (370 vs 370B, encoder magnet count) **`U`**. Reconfirm no-load RPM and encoder PPR on the invoice line, not the category photo.

**Disposition: Lead for a reference unit (bench). NOT a freeze. NOT a purchase authorization.** Same status RP-01 gave a named XC330: encouraging paper envelope, installed behaviour OPEN.

### 4.3 `D03` — JGA25 6 V 133 RPM 1:45 (comparison)

**`D` Oz same table:** rated **1.1 kg·cm = 0.108 N·m**, stall **6 kg·cm = 0.589 N·m**, stall 900 mA, no-load **133 RPM**.

**P01:** stall 0.589 ≥ 0.220; rated 0.108 ≥ 0.063. **Pass**, stronger than `D02`.

**P02: HOLD.** 133 RPM is **below 160**. On Ø84: `v = 133 × 0.2639 / 60 = 0.585 m/s`. That is still **above the follow cap 0.50 m/s** (113.7 RPM) and below the 0.70 design point. Do not silently retarget G02. Do not treat 0.58 m/s as “close enough to 0.70.”

**P03:** same 900 mA vs NFP ≤ 3 A conflict as `D02`. HOLD.

**P04:** 11 PPR × 45:1 ≈ 495 CPR — finer than `D02`, still PASS.

**P05:** 45:1 still backdrivable class; slightly more residual friction `E`, still needs active hold.

**Disposition: Comparison / P02 HOLD.** Keep on the selector if `D02` overspeeds or if stall-current metering favours a longer box. Not the reference-unit lead.

### 4.4 `D04` — 37D-class 12 V ~150–200 RPM (upper bound)

**Class:** 37 mm brushed gearmotors, 12 V nominal, 150–200 RPM output bins exist in hobby catalogues. Mass **~150–200 g each** `E` analogical (Pololu-class 37D with encoder is this picture). Stall several amperes `E`.

**P01:** stall typically several N·m-class at the wheel after 30–50:1 — would pass 2× 0.110. Not interesting; the mass is.

**P02:** 150–200 RPM bins exist at 12 V. In-band is possible. 12 V vs RP-02 2S-class 6.0–8.4 V `E` planning case is a **rail fork**, not a silent “it also runs at 7.4 V” (torque/speed both move).

**P03:** stall several A; both-motor **exceeds Korad 5 A**. Phase B per-motor is mandatory. Signed regen still required.

**P06: FAIL as lead.** Two motors **300–400 g** before wheels, caster, skid, brackets. They **eat the drive row**. A brake would not fit after them.

**P05:** ratio-dependent; not scored as lead.

**Disposition: Hold / upper bound, not lead.** Use only if JGA25-class fails P01 on the **metered** article *and* the mass ledger is revised — which physics said not to do from this screen.

## 5. Wheel, caster, ball, skid

### 5.1 `D10` — wheels

Ø**84 × 21 mm** rubber/TPU, moderate grip. Hub **4 mm** to match JGA25 D-shaft, or **6 mm** with a documented adapter (adapter mass in the 200–600 g row). Spec band, not SKU. Shore / µ remain `E` (`physics.md` C02–C04). Threshold strips are geometric, not a tyre SKU.

**India snapshot:** “84 mm robot wheel” class, Robu / generic. Price band `E` ₹150–600 **per pair**. Stock `U`. Hub bore vs 4 mm D-shaft is the receiving check.

### 5.2 `D20` — swivel caster (Concept A)

Ø**25–32 mm** (~30 mm target). Trail **TBD `U`**. This is the `BM-07` heading-glitch owner. Contact patch moves; instantaneous `L` is not frozen 110 mm during reverse.

**Disposition:** spec band for Concept A. No SKU. Interchangeable on the rig with `D21`.

### 5.3 `D21` — ball transfer (Concept B only)

Ø**1 inch** ball transfer. No trail. Higher rolling resistance `E`; dent risk on wood; pile can jam. **Not** fitted on the Concept A working-lead path except as the interchangeable front-support experiment.

**Disposition:** Concept B comparison article. Not a purchase with `D02`.

### 5.4 `D30` — rear skid

Printed polymer or PTFE pad. **Adjustable reach 60–80 mm, height 8–16 mm.** Inherited start 70 mm / ≤14 mm is **tight** against target `x/h = 0.202` and **fails** lumped Layout 03 CoMs (`physics.md` §2.7). Do not freeze 14 mm. Recompute `h/d < x/h` at the ballast corner.

## 6. Motor driver CLASS

Part 3 screens **class**. Part 4 names a lead on the pin map. Required of any installed class:

1. Hardware **fault output** (`nFAULT` or equivalent) per channel or otherwise **observable L/R**.
2. **Current sense per channel** (signed, or a documented path to signed regen on `PB-DRIVE-L/R` — unsigned “less traction” is not `PA-13`).
3. Logic-level **enable that fails safe** (pulled to **inhibit** on a broken loop).

### 6.1 `DRV-A` — TB6612FNG

**`D`:** Toshiba TB6612FNG, [product](https://toshiba.semicon-storage.com/ap-en/semiconductor/product/motor-driver-ics/brushed-dc-motor-driver-ics/detail.TB6612FNG.html) / [datasheet reprint](https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Robotics/TB6612FNG.pdf): **1.2 A** continuous average, **3.2 A** peak (single pulse, tw = 10 ms). Dual channel. STBY pin. No IPROPI. No nFAULT pin of the DRV8874 kind.

**Screen:** Fine if the metered stall is **0.9 A**. **Fails / HOLD** if stall is **3 A `D`** (NFP table): 3 A > 1.2 A cont; peak 3.2 A is a 10 ms pulse, not a stall. Dual 1.2 A also does not give per-channel current sense.

**Disposition: Hold.** Not the class lead. Reject as installed driver if the article meters ~3 A stall.

### 6.2 `DRV-B` — TI DRV8874

**`D`:** [TI DRV8874](https://www.ti.com/product/DRV8874), [datasheet](https://www.ti.com/lit/ds/symlink/drv8874.pdf). **4.5–37 V**. Peak **6 A** (device). **IPROPI** current sense, **nFAULT**, hardware current chop / regulation (IMODE), PH/EN or PWM. One H-bridge per chip.

**Screen:** Voltage window covers 2S-class 6.0–8.4 V and a 12 V `D04` experiment. Current class covers both 0.9 A and 3 A stall without relying on a 10 ms peak. IPROPI + nFAULT + nSLEEP/enable match the must-have list. **Two chips** for L/R observability (do not share one sense resistor across motors). nFAULT during chop vs true fault must be decoded as the datasheet says — firmware work, not a reason to drop the part.

**Disposition: Lead class.** Exact suffix, layout, `RIPROPI`, and enable pull are Part 4. Not a freeze. Not a purchase.

### 6.3 `DRV-C` — Cytron MDD3A

**`D`:** [Cytron MDD3A](https://www.cytron.io/p-3amp-4v-16v-dc-motor-driver-2-channels): 4–16 V, **3 A cont / 5 A peak** per channel, dual. India-common evaluation board.

**Screen:** Current class covers 3 A stall **per motor**; both-motor stall still a pack/Phase C problem, not a Korad 5 A both-motor problem if the bench uses this board **one motor at a time** or a second PSU. **Missing** a documented per-channel analog current sense and a hardware nFAULT of the TI kind on the hobby board. Test buttons and a 5 V buck are bench conveniences, not CA features. Enable/fail-safe must be verified against the actual input circuit (inputs are PWM-in; a floating input is not automatically inhibit).

**Disposition: Bench-only evaluation board.** Useful for Phase A loop-rate / encoder work. Not an installed freeze. India-common does not beat `DRV-B`'s observability.

## 7. India snapshot (ranges `E`, stock `U`)

Dated **2026-09-17**. Robu / Zbotic as **class**. Exact SKU stock is `U`. Reconfirm suffix, encoder magnet, shaft, and GST before any later payment.

| Row | Class signal | Price band `E` | Stock |
|---|---|---|---|
| N20 encoder 6 V | Robu / Zbotic N20 class | ₹200–800 | `U` |
| JGA25-370 encoder 6 V ~170 RPM | Robu / Zbotic 25 mm class | ₹400–1 200 | `U` |
| 37D encoder 12 V | Import / industrial class | ₹1 500–4 000 | `U` |
| Ø84 wheels | Generic robot wheel | ₹150–600 / pair | `U` |
| Ø25–32 caster | Commodity | ₹50–400 | `U` |
| Ø1" ball transfer | Commodity | ₹100–500 | `U` |
| TB6612FNG module | Commodity dual driver | ₹150–400 | `U` |
| DRV8874 | IC / breakout | ₹200–800 | `U` |
| Cytron MDD3A | India-common board | ₹800–1 800 | `U` |

Not a budget. Not added to a BOM. Clone silkscreens vs Aslong / NFP / Cytron genuine is `U` until receiving photographs.

## 8. Explicit no-buy list

This screen **does not authorize purchase**. If a later builder note authorizes bench equipment, it still must not be these:

1. **N20 1000:1 / 14–15 RPM** (P02 FAIL) — including the robotics.org.za 15 RPM 4 kg·cm article and Zbotic 15 RPM 1:1000.
2. **N20 5:1 / ~2500 RPM** (P01 and P02 FAIL).
3. **Wheel-only 12 CPR** as the sole `BM-02` encoder.
4. **37D pair as the lead** (P06 eats 200–600 g).
5. **TB6612FNG as installed** if stall `D`/meter is ~3 A.
6. **Ball transfer (`D21`) as a Concept A part** except on the interchangeable rig mount.
7. **Behind-axle battery** to “make the motors fit” (HIGH_AFT).
8. **Unsigned current-sense** that folds regen into “less traction.”
9. **Driver HAT with built-in cliff inputs** that would freeze ADR-07.
10. Any SKU treated as frozen because it was convenient on 2026-09-17.

Permissible later as **bench equipment** if separately authorized: one (preferably two) **JGA25-370-class 6 V ~176 RPM encoder** article as the `D02` reference unit; one Cytron MDD3A **or** a DRV8874 breakout for Phase A; Ø84 test wheels; a Ø25–32 caster **and** a ball transfer for the interchangeable mount; a printed skid shim. That authorization is not this document.

## 9. Completion state

**Screen complete. No freeze.**

`D02` is the reference-unit **lead** for the bench: P01/P02/P04 pass on the Oz 6 V 176 RPM table; P05 is the known active-hold cost; P06 fits 350–500 g `E`; **P03 is HOLD** until that article is metered (Oz 900 mA vs NFP ≤ 3 A, both `D`). `D03` remains a slower comparison. `D01` is the rejected lower bound. `D04` is the mass upper bound. `DRV-B` is the driver **class** lead; `DRV-C` is the India bench board; `DRV-A` holds.

Concept A's working-lead geometry (axle motors, forward battery, caster `D20`, skid `D30`) is the packaging this screen assumes. Concept B's ball `D21` and in-WB motors stay a comparison, not waived.
