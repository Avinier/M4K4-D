# Wheels — parts, printing, assembly and service

The two drive wheels of [chassis v1](../README.md): what is printed, how each
joint holds, how to put a wheel together and take it apart, and the gaps found
on the 2026-10-29 review with their fixes ([D-070](../../../03-build/decisions.md#d-070)).

- **Geometry:** the wheel source is [`wheel_model.py`](../../../03-build/01-chassis/v1/cad/wheel/wheel_model.py)
  (chassis v1, [wheel README](../../../03-build/01-chassis/v1/cad/wheel/README.md)).
  The print fixes are droid edits in [`makad-v1.step.py`](../../../03-build/final/v1/cad/makad-v1.step.py)
  (D-070). STLs are exported from the final assembly with those edits, never from the wheel source alone.
- **Check:** [`check_wheel_print.py`](../../../03-build/final/v1/cad/check_wheel_print.py), 29/29 on 2026-10-29.
- **Axle side:** the stub, bearings and motor are the D-007 axle stack, described in
  [axle-stack.md](../../../03-build/01-chassis/v1/research/axle-stack.md). It is built and serviced by the [axle page](../axle/README.md).

## 1. Parts

For one wheel. The robot has two, so double every quantity.

| # | Part | BOM | Made by | Material, colour | Qty per wheel |
|---|---|---|---|---|---|
| 1 | **Rim**: six framed spokes, hex hub with a Ø10 bore and two Ø1.8 clocking pegs (D-070), Ø74 tyre seat with 12 ribs, inboard lip, six insert holes | CH-004 | Print | PETG, slate blue | 1 |
| 2 | **Tyre**: 18 chevrons, OD 84, printed with a Ø73.6 bore and 19.3 wide (D-070) | CH-005 | Print | TPU 95A, black | 1 |
| 3 | **Clamp ring**: 12-sided, six screw flats and six vent slots | CH-004 set | Print | PETG, slate blue | 1 |
| 4 | **Hub cap**: 26 mm hex with a faceted boss, two Ø2.1 peg holes (D-070) | CH-058 | Print | PETG, gunmetal | 1 |
| 5 | Heat-set insert, M3 × 4, brass, slant knurled, OD 4.4 (OnlyScrews; ordered 2026-10-30), in the rim | CH-049 | Buy | — | 6 |
| 6 | Clamp-ring screw, ISO 7380 M3 × 8 button head | CH-048 | Buy | Steel | 6 |
| 7 | Wheel-to-stub screw, ISO 7380 M3 × 6 button head | CH-056 | Buy | Steel | 3 |
| 8 | Hub-cap screw, ISO 7380 M3 × 10 button head | CH-059 | Buy | Steel | 1 |
| 9 | Loctite 222, on the three wheel screws (D-070) | CH-057 | Buy | — | a drop each |
| — | Turned steel stub: bearing seats, flange, Ø10 spigot, tapped centre hole | CH-012 | Machined | EN8 | 1 (axle stack) |

**Totals for the robot:** 8 printed parts (2 rims, 2 tyres, 2 clamp rings, 2 hub
caps), 12 inserts, 12 × M3 × 8, 6 × M3 × 6, 2 × M3 × 10. One wheel is about
92.5 g at solid density without the wheel screws (chassis mass register).

**One STL per part serves both sides** (`check_wheel_print.py` §5, 0.000 mm³ difference):

- The right **rim, clamp ring and hub cap** are the left ones turned over.
- The right **tyre** is the left tyre moved across, not turned. The tyre is symmetric about its mid-plane. "Left" and "right" tyres (D-009) are the same print; what matters is which way round it goes on (§4A step 2).

## 2. Printing

| Part | Print | Face on the bed | Supports | Faces that must come out clean |
|---|---|---|---|---|
| Rim | 2 | **The lip side (inboard face)** | Inside the dish only: under the spoke backs (17 mm up, 1,188 mm²) and under the hub web (20 mm up, 766 mm²). Tree supports from the bed, taken out through the open inboard side | Tyre seat and ribs (vertical walls); lip and ring-seat faces (both face up); insert holes (vertical, open upward); Ø10 bore (vertical); **the web's underside**: the stub flange clamps on it, so use a PLA support interface on the AMS, or check it flat and sand it lightly on glass |
| Clamp ring | 2 | Its flat inboard face | None | The inboard face, which clamps the tyre and stops on the rim |
| Hub cap | 2 | **Its underside**, flat since D-070 | None. The recess roof bridges 6.7 mm, column to wall | The visible top: it prints as top surfaces and 45° facets |
| Tyre | 2 (one at first, see the [chassis order](../README.md#order)) | Either side face, axis vertical | None | The bore and its 12 slots; the side faces |

- **Rim: why the lip side down.** The wheel README said "outer face down". That way, the ring-seat face, which holds the six insert holes, floats 3 mm above the bed: 1,137 mm² that needs supports. The lip's tyre face also prints as a 2 mm ledge 22 mm up. Lip side down, every fit face is either vertical or on top. Only hidden faces need supports.
- **Tyre:** print it on an A1, which is direct drive. TPU does not go through the AMS. Dry the spool first.
- **Inserts** go into the printed rim (§4A step 1), not during the print.

## 3. How each joint holds

### 3.1 Tyre to rim (J14)

There is no glue. The tyre is held three ways.

- **It can't spin on the rim.** The Ø74 seat carries **12 ribs**, each 3 mm wide and 0.8 mm tall, running the full width of the seat. The tyre's bore has **12 matching slots**, 3.4 mm wide and 1.0 mm deep, so each rib has 0.2 mm of clearance at each side and on top.
  - At the 0.40 N·m design torque (2 × the 0.20 N·m stall, D-003), the seat carries 0.40 / 0.037 ≈ 11 N in all, under 1 N per rib. The ground force is 0.40 / 0.042 ≈ 9.5 N.
- **It can't slide sideways.**
  - The rim's integral **lip** (inboard, 2 mm thick) and the **clamp ring** (outboard, 3 mm) each overlap the tyre's side by 2 mm, out to R39.
  - The ring stops on the rim's barrel face, not on the tyre. So the squeeze is set by the tyre's width, and it doesn't grow if a screw is over-tightened.
  - The tyre is printed **19.3 mm** wide into a 19.0 mm gap, so it is squeezed 0.3 mm (D-070).
- **It sits tight on the seat.** The bore is printed **Ø73.6** onto the Ø74 seat: a 0.54 % stretch (D-070). The free-state tyre clears the ribs with the stretch applied (check §6).

The assembly CAD shows the tyre fitted: Ø74 and 19.0 wide. The print state is
`wheel_tyre_print()`, listed in `PRINT_STATES` in `makad-v1.step.py`. The STL
export uses it for the tyre.

### 3.2 Clamp ring to rim

- **Centring:** the ring's Ø63.4 bore slides over a Ø63 spigot on the rim's outboard end, with 0.2 mm radial clearance.
- **Seating:** it sits flat on the rim's barrel face, the annulus from R31.7 to R37.
- **Screws:** six M3 × 8 button heads go through Ø3.4 holes on a Ø68 circle into six M3 × 4 brass inserts melted into the rim.
  - Each screw has the full 4 mm of insert thread and ends 1 mm into the empty bottom of the 6 mm hole, so it can't bottom out.
- **Position:** the ring fits in any of six positions, 60° apart.

### 3.3 Rim to axle (J03, D-007)

The axle is the **turned steel stub** (CH-012), not a printed part. From the motor outward:

1. A Ø4.05 bore on the motor's D-shaft, 8 mm deep, locked by an M3 set screw on the flat.
2. Two 688 ZZ bearings in the printed housing.
3. A Ø9.5 shoulder.
4. A **Ø24 × 2 mm flange** with three tapped M3 holes on a Ø16 circle.
5. A **Ø10 × 3 mm spigot** with an M3 hole tapped 8 mm into its end.

The rim's hub is a 4 mm web with a Ø10 bore:

- **The spigot centres the wheel.** It's Ø10 g6 in a Ø10 H7 bore, 3 mm long.
- **The flange face sets the wheel square.** The web's underside sits flat on the flange, which is why that face must print flat (§2).
- **Three M3 × 6 screws** go through the web into the flange: 4 mm of web and 2 mm of thread in steel. The tips end flush with the flange's back, so they can't touch the bearing cap.
  - At the design torque each screw carries 0.40 / 0.008 / 3 ≈ 17 N, which is small.
  - The risk is loosening, not strength: the heads clamp on PETG, which creeps. They get Loctite 222 (D-070).
- **Clearance:** the rim's R18 pocket clears the fixed bearing housing by 2 mm all round. The flange spins inside the pocket.

**Torque path:** motor D-flat → set screw → stub → flange → 3 wheel screws → web → spokes → ribs → tyre.

### 3.4 Hub cap to stub

- **What it covers:** the cap's underside recess (R11.2, 1.9 deep) covers the three wheel-screw heads, with 0.25 mm over them.
- **Screw:** one **M3 × 10** goes through the cap into the tapped end of the spigot, with 6.9 mm of thread in steel. The head sits in a Ø6.2 counterbore, 0.25 mm below the top of the boss.
- **Clocking:** two **Ø1.8 × 1.5 pegs on the hub** go into **Ø2.1 × 1.8 holes in the cap**, 0.15 mm radial and 0.3 mm at the tip. That lines the cap's hex up with the hub's.
  - The pegs fit two ways round, 180° apart.
  - Before D-070 the pegs were on the cap and the holes in the hub (§6 B).

### 3.5 Why two kinds of screws at the hub

- **The 3 wheel screws** hold the wheel on and carry the drive torque. They sit off-centre because the centre is taken by the spigot that locates the wheel.
- **The 1 centre screw** holds only the cosmetic cap.
  - D-033 replaced the cap's six M2 screws into plastic with this one screw into steel.
  - One centre screw could not drive the wheel: it would hold by friction alone, and reversing the motor would work it loose.

The motor also has **two screws** of its own, the face screws (CH-030). The gearmotor's face has just two tapped holes. They are tightened while the alignment plug holds the motor shaft on the bearing axis, before the bearings and stub go in ([axle page §4C](../axle/README.md#c-align-the-motor-d-071)).

## 4. Assembly, one wheel

**Tools:**
- 2 mm hex key: every M3 button head here.
- 1.5 mm hex key: the set screw.
- Soldering iron with an M3 insert tip.
- Flat steel or glass plate.

**Consumables:** Loctite 222 and 641 (CH-057).

### A. The wheel on the bench

1. **Inserts.**
   - Stand the rim lip-down on the plate.
   - Melt the six M3 × 4 inserts into the Ø4 holes in the ring-seat face, vertically, until each is flush. Use the iron's PETG setting, typically about 240 °C.
   - Let them cool, then scrape off any raised plastic round each insert. The ring must sit flat on this face.
   - Measure an insert first. The listing says OD 4.4 in a Ø4.0 hole, which leaves 0.8 mm of PETG under the tyre seat (§6 F). Press slowly and let the plastic flow; don't push it in hot and fast.
2. **Tyre.**
   - Hold the rim the way it sits on its side of the robot: hub cap outboard, nose (+X) forward.
   - Offer the tyre up and look at the chevrons at the top. The **V's point must face forward**. If it faces backward, turn the tyre over.
   - Both wheels follow the same rule. Don't mark a face "outboard": the same tyre face goes outboard on one wheel and inboard on the other.
   - Line up the 12 slots with the 12 ribs and push the tyre on from the outboard end, working round, until it stops on the lip. The 0.54 % stretch needs a firm push, no tools.
3. **Clamp ring.**
   - Slide the ring over the spigot with its flat face to the tyre, and line up the holes.
   - Drive the six M3 × 8 screws in a star pattern, a little at a time, until the ring sits on the rim all round. It squeezes the tyre 0.3 mm on the way.
   - Stop when it's seated: more torque only strips the inserts.
   - Check that no gap shows between the ring and the rim.

### B. The axle stack (once per side, before the wheel)

Build it by the [axle page §4](../axle/README.md#4-assembly-one-side). The order matters: since
[D-071](../../../03-build/decisions.md#d-071) the motor is aligned with the printed alignment plug before the
bearings and stub go in, because the face screws can't be reached once they are in.

### C. The wheel onto the stub

1. Push the rim's Ø10 bore onto the spigot until the web sits flat on the flange.
2. Turn the wheel until the three Ø3.4 holes line up with the flange's tapped holes. There are three positions.
3. Put a drop of Loctite 222 on each M3 × 6. Drive them in turn, a little at a time, with the 2 mm key until snug.
4. Spin the wheel and watch the tyre's edge against something fixed. Wobble means the web isn't flat on the flange.

### D. The hub cap

1. Set the cap on the hub with its holes over the two pegs (two positions, 180° apart). It should drop flat with no rock.
2. Drive the M3 × 10 into the stub's centre with the 2 mm key. Hold the tyre while you tighten, so the torque doesn't go into the gearbox. Snug is enough: the screw only holds the cap.

## 5. Disassembly and service

| To do | Steps | Tools |
|---|---|---|
| **Change a tyre** (wheel stays on the robot) | Take out the six ring screws and lift the ring off. Slide the tyre off outboard, then fit the new one by §4A steps 2–3 | 2 mm hex |
| **Take a wheel off** | Take out the cap screw and lift the cap off the pegs. Take out the three wheel screws. Pull the wheel straight off the spigot | 2 mm hex |
| **Bearings or motor** | Take the wheel off, then follow the [axle page §5](../axle/README.md#5-disassembly-and-service). A motor refit needs the alignment plug again | 2 mm and 1.5 mm hex, press |

- The inserts and the stub's steel threads are reusable.
- Loctite 222 is low-strength and breaks loose with a hand key. Clean the old compound off and put a new drop on when refitting.
- A worn tyre is the only routine change, and it needs only the six ring screws.

## 6. Gaps found on 2026-10-29 and their fixes

Found by walking through the assembly above against the CAD.

| # | Gap | Effect | Fix | Status |
|---|---|---|---|---|
| **A** | **The rim's print orientation was wrong.** "Outer face down" left the ring-seat face, which holds the insert holes (1,137 mm²), floating 3 mm above the bed. The lip's tyre face printed as a bare 2 mm ledge 22 mm up | Supports on a clamp face; a sagging lip | Print **lip side down** (§2). Only the hidden spoke backs and the web's underside need support; the web face gets a PLA interface or a flatness check | **Fixed** here and in the wheel README; `check_wheel_print.py` §4 lists every overhang face |
| **B** | **The hub cap needed support on its visible face.** Face down, its outer ring sat 1 mm above the bed (364 mm²). It couldn't print underside down either, because the pegs and the centre column stood out below it | Support marks on the gunmetal face | **D-070 CAD edit:** the pegs move onto the hub (old hub holes filled) and the holes into the cap. Each hole sits in a Ø3.7 boss, because a bare Ø2.1 hole broke 0.05 mm into the screw-head recess. The column is trimmed flush. The cap now prints underside down with no supports | **Fixed**, `check_wheel_print.py` §1–4 |
| **C** | **The tyre fit wasn't in the CAD.** The Ø73.6 bore and 19.3 width were README notes; the model was line-to-line | A loose, unclamped tyre, or the slicer changing geometry, which breaks [rule 2](../../README.md#rules) | **D-070 CAD edit:** `wheel_tyre_print()` builds the tyre from the wheel source with a Ø73.6 bore and 19.3 width, and `PRINT_STATES` tells the export to use it. The assembly keeps the fitted state | **Fixed**, `check_wheel_print.py` §6 |
| **D** | **"Left" and "right" tyres are the same part.** The docs said "handed, not interchangeable" (D-009). D-009 assumed the right wheel was the left turned round, but the tyre is symmetric about its mid-plane: the right tyre is the left one moved across, unturned (0.000 mm³). | Fine for printing (one STL, two prints). The risk is fitting it the wrong way round | One STL, printed twice. The fitting rule is "the V at the top points forward", checked on each wheel (§4A step 2). A face mark would be wrong on one side, so there isn't one | **Fixed** in the docs; D-070 amends D-009's wording. The CAD is unchanged and both tyres already lead forward |
| **E** | **No thread locker on the three wheel screws.** The button heads clamp on PETG, which creeps, with 2 mm of thread in the flange | Preload drops, the wheel develops play and the screws can back out | **Loctite 222** on the wheel screws (D-070); re-check them after the first runs (§4C) | **Fixed** in the docs: axle-stack, BOM |
| **F** | **The insert wall is 1.0 mm to the tyre seat**, and the CH-049 insert's outside diameter wasn't known | Melting a fat insert in can bulge the seat under the tyre | The ordered insert (OnlyScrews M3 × 4 slant knurled) is listed at **OD 4.4**: 0.2 mm of knurl in the Ø4.0 hole, a normal bite, leaving 0.8 mm under the seat. Each insert sits directly under a rib (both at 30° + n × 60°), so the thin spot is backed by the rib, and a small bulge goes into the 0.2 mm slot clearance over the rib. No CAD change | **Spec OK.** Measure one on arrival and check the seat on the first rim |
| **G** | **Two doc errors.** J14 said "12 M3 × 4 inserts per wheel" (it's 6). The axle-stack service table took the wheel off without taking the cap off first (D-033) | Confusion at the bench | Text corrected | **Fixed** |

**Also found while making the fixes:**

- **The tyre's OD grows when it's stretched.** The free tyre is printed at OD 84.0. Stretching the bore 0.2 mm moves the tread out by about the same amount, so the fitted OD is about 84.4 and the axle about 0.2 mm higher. That's an estimate. It belongs to the open loaded-radius measurement in the [wheel README](../../../03-build/01-chassis/v1/cad/wheel/README.md#open-physical-not-closable-in-cad).
- **The slot roof clearance is set by the stretch.** In the free state the tyre's slot roof is level with the rib top (R37.8). Stretched onto the seat, it is about 0.2 mm above the rib top, as the fitted model shows. The slot sides keep their 0.2 mm.

## 7. Check

[`check_wheel_print.py`](../../../03-build/final/v1/cad/check_wheel_print.py)
builds the chassis tree with the droid edits applied, in about 1 minute. Run it
as in the [final v1 README](../../../03-build/final/v1/README.md). **29/29 pass on 2026-10-29:**

1. **Cap underside:** the cap's lowest material is at y 12.000 on both sides. The old pegs and the column stub are gone (0.000 mm³). The holes are open and roofed. Each boss leaves a 0.80 mm wall, and the screw column is kept above y 12.
2. **Hub:** the old holes are filled (12.165/12.165 mm³), and the two pegs stand on the face with nothing above them.
3. **Assembly:** the cap is clear of the rim and its pegs, the three wheel screws, the cap screw and the stub. The pegs have 0.15 mm radial clearance and 0.30 mm at the tip.
4. **Print orientation:**
   - Rim, lip side down: overhangs only on the spoke backs (1,188 mm²) and the hub web (766 mm²).
   - Cap, underside down: only the recess roof (327 mm²) and the two hole roofs (7 mm²), all bridges.
5. **Both sides:** one print each for the rim, clamp ring, hub cap and tyre (0.000 mm³ difference).
6. **Tyre print state:**
   - Bore Ø73.60 (0.54 % stretch), width 19.30 (0.30 squeeze), OD 84.00.
   - No overlap with the ribs (0.000 mm³). The stretch and lip-squeeze overlaps are as intended.
   - The assembled tyres are unchanged.
7. **Planted:** the unedited subsystem cap reaches y 10.5 (its old pegs), so it fails check 1. The check can tell the difference.

## 8. Still open (physical)

- **The first printed tyre:** it must go on by hand, sit on the lip all round, clamp without bulging past the ring, and grip. Its result settles D-005's TPU question.
- **The insert's measured outside diameter** (listed 4.4, gap F), and the seat after the first six go in.
- **The peg fit on the first cap.** If the cap rocks or binds, tune the hole with the slicer's XY hole compensation, not the CAD.
- **The web's flatness** where the flange clamps, and the **runout** of the assembled wheel. Match the left and right ODs within about 0.3 mm.
- **Retention:** the wheel screws and the cap screw after the first runs, and tyre creep at motor stall.
- From the [wheel README](../../../03-build/01-chassis/v1/cad/wheel/README.md#open-physical-not-closable-in-cad): loaded radius, and grip on tile, laminate and rug.
