# Axle stack — parts, printing, assembly and service

The two drive axles of [chassis v1](../README.md): the motor carrier, bearing housing and
cap, the turned steel stub, the bearings and the motor. Covered here: what is printed, how
the stack works, how to put one side together and take it apart, and the gaps found on
the 2026-10-30 review with their fixes ([D-071](../../../03-build/decisions.md#d-071)).

- **Geometry:** chassis v1, [`body_chassis_model.py`](../../../03-build/01-chassis/v1/cad/body_chassis_model.py). The design reasoning is in [axle-stack.md](../../../03-build/01-chassis/v1/research/axle-stack.md) (D-007, D-012, D-030). The D-071 fixes are droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py). STLs are exported from the final assembly with those edits.
- **Check:** [`check_axle_stack.py`](../../../03-build/final/v1/cad/check_axle_stack.py), 25/25 on 2026-10-30 (D-071, D-072).
- **Fabrication files** (non-printed parts) in [`final/v1/fab/`](../../../03-build/final/v1/fab/): the stub drawing and STEP (CH-012), and the cap DXF and STEP (CH-052) (§7).
- **View:** [`axle-alignment.step.py`](http://127.0.0.1:3245/Users/avinier/robotics/makad/project/03-build/final/v1/cad?file=axle-alignment.step.py) shows the left side twice: the alignment step (§4C) and the finished stack.
- **Wheel side:** the wheel goes on after this; see the [wheels page](../wheels/README.md).

## 1. Parts

For one side. The robot has two, so double every quantity.

| Part | BOM | Made by | Material | Qty per side |
|---|---|---|---|---|
| **Motor carrier**: 5 mm motor plate with front and rear cheeks, one print. It holds the motor and joins the front and rear frame modules (J04) | CH-001 set | Print | PETG, deep slate | 1 |
| **Bearing housing**: Ø32 × 12.35, a Ø16 bearing seat with a shoulder, the set-screw slot (+Z), two face-screw key slots, four Ø3.2 screw holes (D-071) | CH-051 | Print | PETG, deep slate | 1 |
| **Bearing cap**: 1.2 mm ring, OD 32, ID 12.5, four Ø3.4 and two Ø2.6 key holes. It holds the bearings' outer rings in | CH-052 | Cut | Aluminium sheet | 1 |
| **Stub**: Ø8 k5 bearing seats, Ø4.05 D-shaft bore, M3 set-screw hole, Ø9.5 shoulder, **Ø21 × 2 flange** (D-071) with 3 tapped M3, Ø10 g6 spigot with a tapped M3 centre | CH-012 | Turned | EN8/C45 steel | 1 |
| 688 ZZ bearing, 8 × 16 × 5 | CH-015 | Buy | Chrome steel | 2 |
| Gearmotor, ThinkRobotics MOT3001-6V230RPM with encoder | CH-014 | Buy | — | 1 |
| Motor face screw, ISO 7380 M3 × 6 | CH-030 | Buy | Steel | 2 |
| Housing screw, ISO 7380 M3 × 16 (D-072; was M3 × 18), through cap and housing into the plate | CH-053 | Buy | SS304 | 4 |
| Heat-set insert, M3 × 4 slant knurled, OD 4.4 (ordered; the same as the rims), in the plate's Ø4.0 holes | CH-054 | Buy | Brass | 4 |
| Set screw, ISO 4029 M3 × 3 cup point, ground to 2.5 mm at the hex end | CH-055 | Buy, then grind | SS304 | 1 |
| Loctite 641 (bearings on the stub) and 222 (set screw, face screws) | CH-057 | Buy | — | — |
| **Alignment plug**: a printed tool, kept for every motor refit (D-071) | CH-089 | Print | PETG, any colour | 1 for the robot |

**Printed for the robot:** 2 carriers, 2 housings, 1 alignment plug. The two carriers and housings are mirror images: one STL each for left and right.

## 2. Printing

| Part | Face on the bed | Supports | Faces that must come out clean |
|---|---|---|---|
| Housing | **Inboard face** (the one that sits on the plate) | **None** (check §6: no overhang faces) | Ø16 bearing seat and its shoulder (both vertical or facing up); the inboard face (it seats on the plate); the four Ø3.2 holes (they set where the housing refits) |
| Carrier | **Outboard face of the motor plate** (the housing face) | Only under the corners of the square plate, 2.5 mm up (260 mm²). The rest are small bridges: counterbore floors, insert-hole roofs, the set-screw notch | The plate's outboard face (the housing seats on it); Ø7.6 pilot hole; insert holes; the cheek faces and keys that seat on the frame rails |
| Alignment plug | Its outboard end | None | Ø4.05 bore (on the motor shaft); Ø15.8 body (in the bearing seat) |

- **Why the housing goes inboard face down:** printed the other way up, the shoulder the bearings sit against becomes a 75 mm² overhang.
- **Why the carrier goes outboard face down:** printed on its cheek ends, the motor plate would bridge the whole motor bay (828 mm², 19 mm up). Printed on its bottom, the plate's holes print sideways.
- **Fits:** the housings are the test parts ([04-print rule 5](../../README.md#rules)): no separate bore coupons. Try the real bearings in the first housing. If the seat is tight or loose, correct it with the slicer's XY hole compensation for that printer, and reprint.

## 3. How it works

- **The steel stub is the only rotating datum.** The two bearings hold it in the housing, and the wheel centres on its spigot.
- **The motor floats until it is aligned.**
  - The plate's pilot hole is Ø7.6 for the motor's Ø7 pilot, a 0.3 mm float.
  - The two face screws are tightened only once the motor shaft is held on the bearing axis, by the alignment plug since D-071.
  - That keeps print error from bending the Ø4 gearbox shaft into its bushing.
- **Torque:** motor D-flat → set screw → stub → flange → 3 wheel screws → wheel.
  - At the 0.40 N·m design torque the set screw carries about 300 N on the flat.
  - The face screws carry only the motor's reaction torque, about 12 N each.
- **Weight and bumps:** tyre → stub → bearings → housing → housing screws and plate → carrier → frame rails (J04). Design case: 31 N radial and 8 N lateral per wheel.
- **Inward push:** flange → stub shoulder → inner rings → outer rings → housing shoulder → plate.
- **Outward pull:** inner rings (k5 press fit plus Loctite 641) → outer rings → aluminium cap → housing screws. There is no circlip; that is by design, and it is proved by a 100 N pull test (§8).

## 4. Assembly, one side

**Tools:**
- 2 mm hex key: every M3 button head. A straight key reaches all of them since D-071.
- 1.5 mm hex key: the set screw.
- Soldering iron with an M3 insert tip.
- A bench vice or arbor press with a tube that pushes on a bearing's inner ring only.
- A file or grinder for the set screw.

**Consumables:** Loctite 641 and 222.

### A. On the bench

1. **Plate inserts.** Melt the four M3 × 4 inserts into the motor plate's outboard face, flush. Scrape off any raised plastic: the housing must sit flat on this face.
2. **Set screw.** Grind the M3 × 3 down to 2.5 mm at the hex end. Check it sits flush with the stub's Ø8 when screwed in.
3. **Bearings onto the stub.**
   - Put Loctite 641 on the stub's bearing seats.
   - Press both 688 ZZ bearings on from the stub's inboard (shaft) end, pushing on the **inner ring only**, until the second one sits against the Ø9.5 shoulder.
   - Let the 641 cure as its datasheet says. This bearing-and-stub unit is the "cartridge".

### B. Carrier and motor

4. **Carrier onto the frame (J04).**
   - Seat the carrier's cheeks on the front and rear rail ends, keys in their pockets.
   - Drive the four M3 × 8 screws from the motor bay into the rail inserts.
   - Do this before the motor: the motor body covers these screws.
5. **Motor into the carrier.**
   - Drop the motor into the bay, from above or below, and slide it outboard until its Ø7 pilot is in the plate hole.
   - Start both M3 × 6 face screws, with Loctite 222, through the plate into the motor face, **finger-tight only**.

### C. Align the motor (D-071)

6. **Plug into the housing.** Put the alignment plug in the housing's bearing seat with its small nose toward the plate. Put the aluminium cap over it: the plug can't fall out now.
7. **Housing onto the plate.**
   - Offer the housing (with the plug and cap) to the plate. The plug's bore slides onto the motor shaft, and the motor moves to the housing's axis.
   - Drive the four M3 × 16 screws into the plate inserts, snug.
8. **Tighten the face screws.** Put the 2 mm key straight in through each cap key hole, housing slot and plug notch, into the face-screw head. Tighten both. The motor is now fixed on the housing's axis.
9. **Housing off.**
   - Take out the four housing screws and slide the housing (with the cap and plug) off the shaft.
   - Take the cap off and push the plug out.
   - **Keep the plug:** a motor refit needs it again.

The housing goes back on the same four screws in close-fit Ø3.2 holes. It returns to within about 0.1 mm of where the motor was aligned to it.

### D. The cartridge in

10. **Cartridge into the housing.**
    - Push the bearings and stub into the housing seat from the outboard side until the first outer ring meets the shoulder.
    - Fit the cap over the outer rings.
11. **Line up the set screw.**
    - Turn the stub so its tapped hole points at the housing's slot (+Z, up).
    - Turn the motor shaft so its D-flat also faces up. Turn it gently by hand through the gearbox, or with a short pulse of power.
12. **Housing onto the plate.**
    - Slide the stub onto the shaft and seat the housing on the plate.
    - Drive the four M3 × 16 screws with a straight 2 mm key. Since D-071 the Ø21 flange leaves the key 0.35 mm clear.
13. **Set screw.** With Loctite 222, drive it through the housing slot onto the flat with the 1.5 mm key. The key passes the plate through the D-071 notch.
14. **Check:**
    - The stub turns freely, and there's no end play you can feel.
    - Then, powered, the motor's no-load current at 6.0 V is within max(0.05 A, 10 %) of the motor on its own ([axle-stack.md §9](../../../03-build/01-chassis/v1/research/axle-stack.md#coupon-and-assembly-gates), gate 7).

Then the wheel: [wheels page §4C–D](../wheels/README.md#c-the-wheel-onto-the-stub).

## 5. Disassembly and service

| To do | Steps | Tools |
|---|---|---|
| **Wheel or tyre** | See the [wheels page §5](../wheels/README.md#5-disassembly-and-service) | 2 mm hex |
| **Bearings or stub** | Take the wheel off. Loosen the set screw from +Z through the slot. Take out the four housing screws. Slide the housing, cartridge and cap off outboard. Take the cap off and push the cartridge out. Press the bearings off the stub, pushing on the inner rings | 2 mm and 1.5 mm hex, press |
| **Motor** | As for the bearings, then take out the two face screws. They are reachable once the housing is off. Slide the motor inboard off its pilot and lift it out of the bay. **Refitting: repeat §4C with the plug** | 2 mm hex |
| **Carrier** | Take the motor out, then take out the four J04 screws from the motor bay. The carrier comes out toward the chassis centre | 2 mm hex |

- **Loctite:** 222 is low-strength and breaks loose with a hand key. Clean off the old compound and put a new drop on when refitting.
- **641 bearings:** they come off only with a press.
- **Inserts:** the brass inserts are reusable.

## 6. Gaps found on 2026-10-30 and their fixes

Found by checking every documented step against the CAD: tool paths, the motor's way in,
and print orientation. Keys are modelled across their corners: 2 mm hex r 1.155, 1.5 mm hex r 0.87.

| # | Gap | Effect | Fix | Status |
|---|---|---|---|---|
| **A** | **The housing screws couldn't be reached with the stub in.** They sit at R12, and the stub's Ø24 flange (R12) sat 1.6 mm in front of their heads, over half of each socket. A ball-end key would need about 30°, more than its ~25°. The housing can only be bolted on with the stub inside it | The stack couldn't be assembled as documented | **Flange Ø24 → Ø21** (D-071 edit to the stub; the stub isn't drawn or quoted yet, so it costs nothing). A straight key now clears it by 0.35 mm, with 1.0 mm of steel left outside the wheel-screw threads | **Fixed**, `check_axle_stack.py` §1–2, planted §7 |
| **B** | **The motor face screws couldn't be reached once the cartridge was in.** At R8.5 the key path is crossed by both bearings (outer rings R8, 0.65 mm into the key) and by the flange. "Tighten the face screws last" was impossible, so the motor couldn't be aligned to the stub | The motor would be fixed wherever it sat in its 0.3 mm float, and the shaft could be bent | **Alignment plug** (CH-089, a printed tool) in the bearing seat holds the shaft on the housing axis while the face screws are tightened through the plug's notches (§4C). **Housing holes Ø3.4 → Ø3.2**, so the housing goes back where the motor was aligned to it | **Fixed**, §3 and §5 of the check; the keys are blocked without the plug |
| C | **The set-screw key rubbed the edge of the plate hub by 0.07 mm** | The key binds on the plate | **A notch** 3 mm wide and 0.5 mm deep in the carrier hub over the set screw | **Fixed**, check §4, planted |
| D | **Print orientations weren't recorded** (the BOM said only "axle vertical") | The lab might print the housing upside down, putting the bearing shoulder on supports | Housing inboard face down (no overhangs); carrier outboard face down; plug on its end (§2) | **Fixed** |
| E | **axle-stack.md still planned test coupons:** bearing bores Ø15.90–16.10 in 0.05 mm steps, plus spigot and insert sections | Conflicts with the no-test-print rule | The housings and rims are the test parts; correct with XY hole compensation | **Fixed** in the docs |
| F | **Long-lead parts not started:** the stub had no drawing or quote; the bearings, motor and screws aren't ordered; the aluminium caps had no maker or cut file; the set screws need grinding | **The stub is the critical path**, since it has to be drawn, quoted and turned | **Made:** the stub's shop drawing ([CH-012_stub_drawing.pdf](../../../03-build/final/v1/fab/CH-012_stub_drawing.pdf), rev A, A3 2:1, with fits, threads and turning notes) and its STEP; the cap's laser-cut DXF ([CH-052_cap.dxf](../../../03-build/final/v1/fab/CH-052_cap.dxf), eight circles) and STEP. All are generated from the final droid geometry by `export_axle_fab.py` and `stub_drawing.py`. §7 is the order list | **Ready to send.** Placing the orders and getting quotes is yours (§7) |
| G | **No positive outward stop for the bearing inner rings** (k5 plus Loctite 641, no circlip) | Known, by design (D-007) | **Calculated (§9):** at least 3.7× the 100 N design load even with one ring at half strength. The aluminium cap is about 4.5× on yield, as a rough estimate. The bench pull test (§9) checks the workmanship. The DIN 6799 clip stays the fallback if a test fails | **Closed by calculation**; the test runs when the parts arrive |

**Found on the second pass, 2026-10-30 ([D-072](../../../03-build/decisions.md#d-072)):**

| # | Gap | Effect | Fix | Status |
|---|---|---|---|---|
| H | **The M3 × 18 housing screws ended 0.2 mm above the bottom of their blind holes**, 0.51 mm over the gearbox face. Their length tolerance is ±0.35 | A long screw bottoms out before its head clamps the cap: it feels tight, but the bearings aren't held, and the tip can push the plastic onto the gearbox | **M3 × 16**: the tip is 2.2 mm above the hole bottom, with 2.29 mm in the insert | **Fixed**, check §8, planted |
| N | **The wheels page still had the pre-D-071 axle order** (M3 × 18, face screws tightened last with the stub in) | Two pages gave different build orders, and one couldn't be done | The wheels page §4B now points here | **Fixed** |

**What passed without change:**
- The motor drops into the carrier from above or below with nothing in the way.
- The set-screw key's long arm has a clear path outboard once the wheel is off.
- The plate inserts fit the ordered OD 4.4 insert in Ø4.0 holes.

## 7. To order or make

| What | Qty for the robot | Where | Note |
|---|---|---|---|
| Stub, CH-012 | 3 (2 + 1 spare) | A local turning shop | Send [CH-012_stub_drawing.pdf](../../../03-build/final/v1/fab/CH-012_stub_drawing.pdf) and [CH-012_stub.step](../../../03-build/final/v1/fab/CH-012_stub.step). EN8 or C45; k5, g6 and H8 limits are on the sheet |
| 688 ZZ bearings, CH-015 | 4 | OnlyScrews listing (sold out at the last check) | Confirm the maker, ZZ shields and dimensions on the delivered lot |
| Aluminium caps, CH-052 | 2 (+2 spare) | Laser or waterjet cutting from 1.2 mm aluminium, 5052-H32 or 6061-T6 | Send [CH-052_cap.dxf](../../../03-build/final/v1/fab/CH-052_cap.dxf) (mm, layer CUT): OD 32, ID 12.5, 4 × Ø3.4 on R12, 2 × Ø2.6 on R8.5. Deburr; the ID face bears on the outer rings |
| Gearmotors, CH-014 | 2 | ThinkRobotics MOT3001-6V230RPM | Measure the face holes, pilot and shaft flat on arrival (axle-stack.md §7) |
| M3 × 16 button heads, CH-053 | 8 | [OnlyScrews](https://onlyscrews.in/products/hex-allen-button-head-m3-x-16-screw-pack-of-20), SS304 | Not M3 × 18: it can bottom out in the plate (D-072) |
| M3 × 6 button heads, CH-030 | 4 | OnlyScrews (the same as the wheel screws) | |
| M3 × 3 cup-point set screws, CH-055 | 2 (+2 spare) | OnlyScrews | Ground to 2.5 mm |
| M3 × 4 slant-knurled inserts, CH-054 | 8 | Ordered | |
| Loctite 222 and 641, CH-057 | 1 each | | |

## 8. Check and proof (CAD)

[`check_axle_stack.py`](../../../03-build/final/v1/cad/check_axle_stack.py) builds the chassis
tree with and without the droid edits, in about 1.5 min. Run it as in the
[final v1 README](../../../03-build/final/v1/README.md). **25/25 pass on 2026-10-30:**

1. **Flange Ø21:** nothing outside R10.5, the rest of the flange intact, 1.0 mm of steel outside the wheel-screw threads.
2. **Housing screws:** all four reachable with a straight 2 mm key with the stub in, 0.345 mm off the flange.
3. **Housing holes:** Ø3.2 over the full housing; the screws are clear, 0.10 mm radial.
4. **Set screw:** a straight 1.5 mm key from +Z is clear.
5. **Alignment plug:**
   - It's clear of all 18–19 parts present when it's used.
   - Fits: 6.9 mm on the shaft (0.025 radial); body 0.1 mm radial in the seat; held in by the cap, with 0.2 mm axial play.
   - Both face-screw keys are clear through it. With the bearings and stub in its place they're blocked, which is why the plug exists.
6. **Print orientation:** housing and plug have no overhangs; the carrier's are listed in §2.
7. **Planted:** the unedited Ø24 flange blocks every housing-screw key (4.126 mm³ each), and the unedited carrier blocks the set-screw key (0.338 mm³).
8. **Housing screws, M3 × 16 (D-072):** the tips are 2.20 mm above the bottom of their blind holes, against a 0.93 mm worst-case stack (length +0.35, cap −0.08, 0.5 for insert melt), and a screw at its short limit keeps 1.94 mm in the insert (1.5 minimum). Planted: the old M3 × 18 sits 0.20 mm above the bottom.

**Physical proof still to come** ([axle-stack.md §9](../../../03-build/01-chassis/v1/research/axle-stack.md#coupon-and-assembly-gates), and §9 below):
- The 100 N bearing pull test.
- The first housing with the real bearings.
- The J04 carrier to the rails.
- The axle rig: deflection, then running clearance, then proof loads.
- Powered acceptance: runout ≤ 0.30 mm, end play ≤ 0.10 mm, current within the limit after the face screws are tightened, and 200 reversals with no set-screw shift.

## 9. Outward retention of the bearings (gap G)

Pulling the wheel outward, by lifting the robot by one wheel or by a side knock, tries
to pull the stub out through the bearings. Nothing positive stops that. What holds it is
the bond between the stub and the two inner rings (k5 press fit plus Loctite 641), then
the outer rings on the aluminium cap, and the cap on the four housing screws. D-007 sets
the design load at **100 N**, about 4× the load of lifting the robot by one wheel.

**Bond.** The [Loctite 641 datasheet](https://datasheets.tdx.henkel.com/LOCTITE-641-en_GL.pdf)
(Henkel TDS, May 2004) gives a compressive shear strength of **≥ 6.5 N/mm²** on steel pins
and collars (ISO 10123, after 24 h at 22 °C). At 50 °C it keeps about 90 % of that.

| Case | Bonded area | Hold | Against 100 N |
|---|---|---|---|
| Both inner rings, datasheet strength | 2 × π × 8 × 5 = 251 mm² | ≥ 1,630 N | 16× |
| One ring only, at half strength (poor coverage on a press fit, part cure, warm) | 126 mm² × 3.25 N/mm² | ≈ 410 N | **≈ 4×** |

This doesn't count the k5 press fit's own friction. G is closed by calculation: even the
pessimistic case is about 4× the design load.

**The rest of the path** (rough screens):

- **Cap.** 1.2 mm aluminium, clamped by four screws at R12, loaded by the outer rings at R6.25–8. Treated as a strip about 60 mm round and 5 mm in lever arm, 100 N gives about 35 MPa of bending, against 160–275 MPa yield for 5052-H32 or 6061-T6: about 4.5×.
- **Housing screws.** Four, so 25 N each into the brass inserts.
- The pull test below proves all of it together.

**Assembly rules from the datasheet:**

- Clean both surfaces first.
- Coat both the stub seat and the inner-ring bore.
- Press in one steady stroke on the inner ring.
- No load for **24 h at about 22 °C**: steel reaches near full strength by then and full strength by 72 h. Cold slows it a lot: at 5 °C it reaches most of its strength only after about a day.
- To take it apart later, heat to about 250 °C.

**Bench pull test** (per side, once the cartridge has cured; no motor needed):

1. Build the side up to step 13 without the motor: carrier, housing with the cartridge, cap and four screws.
2. Clamp the carrier in a vice, axle vertical, spigot down.
3. Screw an M3 screw with a wire loop, or an M3 eye bolt, into the spigot's tapped end, at least 6 mm deep.
4. Mark or measure the flange-to-cap gap with feeler gauges or a dial gauge.
5. Hang **10.2 kg** (100 N) on the loop for 10 s: a bag of rice or water bottles, weighed. Lower it gently; don't drop it.
6. **Pass:** the gap changes by less than 0.10 mm and is back after unloading; the stub still turns freely; nothing cracks and no insert moves.
7. **If it fails:** the fallback is a DIN 6799 clip and shim inboard of the first bearing. That needs about 1.5 mm and moves the set screw, so it means a new decision and a stub revision.

