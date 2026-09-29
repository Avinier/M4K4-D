# Wheel-to-chassis axle stack — work package 1

**Status:** D-007 axle stack accepted and modelled; J04 carrier-to-frame architecture added to CAD on 2026-09-29. Neither is physically proven: the motor is not on hand, parts have not been printed or assembled, and the stub has not been quoted. This page records the selected design plus the remaining coupon and test gates.

The motor is the **ThinkRobotics MOT3001-6V230RPM** ([D-003](../../decisions.md#d-003)). No unit is on hand ([D-005, motor interface](../../decisions.md#d-005)). Every motor-facing dimension is therefore a supplier-drawing or CAD assumption, listed in §7. The [motor interface sheet](motor-interface-sheet.md) is parked for later fit evidence.

All positions are **|Y| from the robot centre plane**, the same convention as the CAD. The fixed constraints are the 170 mm track (wheel mid-plane |Y| 85), the Ø84 × 24 mm wheel (|Y| 73–97) and the motor faceplate at |Y| 69.

## 1. Why the previous stack could not be built as modelled

| # | Previous CAD (RP03-CAD-05 geometry) | Defect |
|---|---|---|
| 1 | The motor's D-shaft engaged a **round** Ø4 bore in the stub, entirely under the inner 608. | No torque path, and no room for a set screw or pin. |
| 2 | The stub sat in a plain Ø8 hole in the printed web. | No torque path to the wheel and no axial retention. |
| 3 | The 608 seat was Ø22.5 for a Ø22 bearing, with nothing retaining either ring. | The bearings were not located. |
| 4 | The motor was rigidly bolted **and** its shaft was held by a separately supported stub. | Over-constrained: print error bends the Ø4 shaft into the motor bushing. |
| 5 | Countersunk M3 heads sat in a 2 mm printed diaphragm, behind the bearings. | The heads would split the diaphragm and relax, and they could not be reached for service. |
| 6 | Wheel load passed through a 2 mm flange plate butted to the cheek ends. | The plate was flexible, and the joint did not exist (J04). |

## 2. Loads used

| Case | Value | Basis |
|---|---:|---|
| Static radial load per wheel | 10.4 N | 2.570 kg × (1 − 0.176 ball share) ÷ 2, from the [mass register](cad/generated/mass-properties.md) before D-007 |
| Bump/drop radial load | 31 N | 3 g on the static load |
| Lateral scrub at the tyre | 8.3 N at r 42 → 350 N·mm | μ 0.8 on the static load |
| Combined moment at the bearing pair | ≈ 459 N·mm | 350 N·mm + 31 N × 3.5 mm from the wheel plane to the revised pair centre |
| Drive torque, design value | 0.40 N·m | 2 × the estimated 0.20 N·m stall ([D-003](../../decisions.md#d-003)) |
| Outward axial hold, design value | 100 N | About 4× the load of lifting the robot by one wheel |

## 3. The stack

**The design idea:** the steel stub is the only rotating datum. The bearings locate the stub, and the stub locates the wheel on a turned spigot. The motor **floats** on its face screws until it has aligned itself to the stub; the face screws are tightened last.

```
|Y|  69    71.5  73  74    74.8   76.5      81.5      86.5 87.7 89.35 91   93      97
     | plate      |recess|  set  |shoulder                   |cap|heads |flange| web  |
motor|====(pilot) |      |screw |[ 688ZZ ][ 688ZZ ]|     |===|      |      |      |
face |            | stub ━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━spigot━┫
                       (Ø8; Ø4.05 bore 73–82)             Ø9.5 shoulder  Ø24     Ø10
```

| \|Y\| (mm) | Item | BOM | Material and process | Key features |
|---|---|---|---|---|
| 69.0–74.0 | **Motor plate**, the outboard wall of the motor carrier | CH-001 | Candidate structural print; integral with the front/rear cheeks in one J04 carrier | 34 × 30 square to 71.5, then an R 16.5 hub to 74. Inside the wheel pocket, 1.5 mm clear of it. Ø7.6 pilot hole (0.3 mm float). R 6 × 2.5 recess on the outboard face, floor at the pilot end. 2 × Ø3.6 face-screw holes at R 8.5 with Ø6.5 × 2.2 counterbores. 4 × M3 × 4 inserts at R 12, 45°/135°/225°/315°, ≥ 4.5 mm from the plate edges. |
| 65.8–73.8 | **Face screws** ×2 | CH-030 | DIN 7984 M3 × 6 low head, Loctite 222 | Heads 0.2 mm below the plate face. 2.8 mm clamp, 3.2 mm thread in an assumed 5 mm tapped hole. Tightened **last**, through the housing key slots. |
| 74.0–86.35 | **Bearing housing** ×2, mirrored | CH-051 | PETG print, axle vertical | Ø32. Inboard cavity and outer-ring shoulder Ø12.5 (74–76.5). 688ZZ seat Ø16, coupon-tuned (76.5–86.35); bearings stand 0.15 mm proud at 86.5. Set-screw slot Ø3.4 at +Z, open to the base. Face-screw key paths Ø2.6 at R 8.5 (0°/180°), opened into the bore as slots, off the vertical load line. 4 × Ø3.4 at R 12, leaving 2.3 mm of wall outside. |
| 73.0–96.0 | **Stub** ×2 | CH-012 | EN8/C45, turned in one setup | Ø8 from 73 (1.5 mm off the motor pilot). **k5** bearing seats 76.5–86.5. Ø4.05 H8 bore 73–82, giving **8 mm** on the shaft. M3 tapped radial hole at 74.8 onto the D-flat; its Ø2.5 tap-drill edge is 0.45 mm from the first bearing face. Ø9.5 shoulder 86.5–91. Ø24 × 2 flange 91–93 with 3 × M3 tapped at PCD 16 (30°/150°/270°). Ø10 g6 spigot 93–96. |
| 74.8 | **Set screw** ×2 | CH-055 | DIN 916 M3 × 2.5 cup point, Loctite 222 | Bears on the flat and sits flush with the Ø8. Fitted and driven through the housing slot with a 1.5 mm key once the wheel is off. The revised hole location requires edge-break inspection on the turned stub. |
| 76.5–86.5 | **Bearings** ×4 | CH-015 | **688 ZZ** 8 × 16 × 5, double metal shield, chrome steel per [OnlyScrews listing](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5) | Inner rings: k5 press + Loctite 641 against the shoulder. Outer rings: slip to light press, between housing shoulder and cap. Listing does not identify the manufacturer or state load ratings; obtain the actual drawing/data with the delivered lot. |
| 86.5–87.7 | **Retaining cap** ×2 | CH-052 | 1.2 mm aluminium | ID Ø12.5 bears on the outer ring only. OD Ø32. 4 × Ø3.4 at R 12; 2 × Ø2.6 key holes at R 8.5. |
| 69.7–89.35 | **Cap screws** ×8 | CH-053 | ISO 7380 M3 × 18 | Through cap and housing into the plate inserts; they clamp the housing and hold the outer rings outboard. |
| 70.0–74.0 | **Inserts** ×8 | CH-054 | M3 × 4 brass heat-set | In the plate. |
| 93.0–97.0 | **Wheel web** | CH-004 | PETG print | Pocket R 18 to 93; the stub flange turns inside it. Ø10 H7 bore through, 3 × Ø3.4 at PCD 16, flat seats for the heads. Adopted by the handed left/right [wheel model](cad/wheel/README.md) and imported into the chassis assembly. |
| 91.0–98.65 | **Wheel screws** ×6 | CH-056 | ISO 7380 M3 × 6 | Through the web into the flange. The full 2 mm flange is threaded, with the tip flush at 91. Overall width over the heads is 197.3 mm, inside the 205 mm target. |

**Load paths.**

- **Radial:** tyre → web → spigot and flange → stub → 688 ZZ pair → housing → cap screws and plate → carrier (J04).
- **Inward axial:** flange → shoulder → inner rings → outer rings → housing shoulder → plate.
- **Outward axial:** stub → inner rings (k5 + 641) → outer rings → cap → cap screws.
- **Torque:** motor flat → set screw → stub → flange → 3 wheel screws → web.
- **What the motor carries:** the bushing carries only float error. The face screws carry only reaction torque, about 12 N shear each.

## 4. Checks

**In the CAD** (`check_layout.py`, rerun with this revision):

| Check | Result |
|---|---|
| Rotating parts vs static parts | ≥ 1.5 mm everywhere. Rim vs plate 1.5; stub shoulder vs cap 1.5; set screw vs plate 1.96. |
| Rotating screws swept as full rings | Wheel screws 1.65 mm to the cap-screw heads; set screw 1.55 mm to the face-screw heads |
| Interferences | None except the modelled face-screw threads in the gearbox |
| Retention | Bearings touch the housing shoulder, the cap and the stub without overlap. Housing seated on the plate. Set screw on the flat. 2 mm of thread per wheel screw. |
| Shaft in stub | 8.0 mm |

**Hand calculations.** These are screens, not proof.

| Check | Result | Verdict |
|---|---|---|
| Bearing reaction: 459 N·mm ÷ 5 mm + 31 N | ≈ 123 N | Supplier-specific dynamic/static ratings are unavailable; verify against the received bearing maker's data |
| Stub torsion, Ø8/Ø4 at 0.40 N·m | τ ≈ 4 MPa | Low; the radial hole is a stress raiser, but the load is small |
| Set-screw force ≈ T ÷ 1.3 mm | ≈ 300 N | Plausible for 2 mm of steel thread (4 threads); **prove by reversals on the rig** |
| Outward hold: 100 N over the 2 × π × 8 × 5 mm² total two-bearing contact | ≈ 0.40 N/mm² nominal | Screening estimate only; actual k5/compound interface must **pass pull test** |
| Wheel screws: 0.40 N·m over 3 at R 8 | ≈ 17 N each | Friction joint; check web creep |
| Cap screws: 459 N·mm over 4 at R 12 | ≈ 21 N peak tension | Low; confirm insert pull-out on a coupon |

## 5. Assembly and service (one side)

**Bench subassembly**
1. Press both 688 ZZ bearings onto the stub from the inboard end, pushing on the **inner ring only**, until they sit against the Ø9.5 shoulder. Use Loctite 641.

**Install**
2. Put the motor in the carrier, pilot in the plate hole. Start both face screws finger-tight.
3. Push the stub cartridge into the housing until outer ring 1 meets the shoulder. Fit the cap.
4. Offer the housing to the plate. Turn the stub until its tapped hole lines up with the shaft flat, then slide it onto the shaft. Fit the four cap screws.
5. Fit the set screw through the slot and tighten it.
6. Turn the stub by hand so the motor centres itself. Tighten both face screws through the key slots with a long 2 mm ball-end key.
7. Check drag and end play. Fit the wheel on the spigot and tighten its three screws.

**Service paths**

| Replace | Remove first | Tools |
|---|---|---|
| Wheel or tyre | 3 wheel screws | 2 mm hex |
| Bearing pair | wheel → loosen set screw → 4 cap screws → housing and cartridge slide off outboard → press the bearings off | 2 mm and 1.5 mm hex, press |
| Motor | as for bearings → 2 face screws → motor out (exit direction set by J04) | as above |

## 6. Proposal review holds and their status

| # | Hold raised in review (2026-09-29) | Status |
|---|---|---|
| 1 | Bearing family was previously specified as MR148ZZ/L-1480ZZ, 8 × 14 × 4. | **Superseded by D-012:** use 688 ZZ, 8 × 16 × 5. The housing seat and axial bearing positions were revised in CAD. The supplier page currently says sold out; manufacturer, drawing and load rating remain to be confirmed for the received lot. |
| 2 | The set-screw hole touched the stub end. | **Fixed:** stub starts at 73; current 688 ZZ layout moves the hole to 74.8, leaving 0.55 mm from the Ø2.5 tap drill to the stub end and 0.45 mm to the first bearing face. Verify these narrow lands on the turned drawing and part. |
| 3 | Insert 0.5 mm from the plate edge; 1.3 mm housing wall; 0.2 mm skin at the key holes. | **Fixed:** 4 diagonal screws at R 12 (≥ 4.5 mm margin); Ø32 housing (2.3 mm wall); key paths opened as slots. |
| 4 | No positive outward retention of the inner rings. | **Open, by design:** there is no room for a circlip. Retention is k5 + 641, with a 100 N axial hold test on the bearing/stub assembly; this test can use a standalone fixture and does not need the motor. If it fails, the fallback is a DIN 6799 clip plus shim, which needs about 1.5 mm and moves the set screw. |
| 5 | Wheel-screw tips vs cap hardware, across a full revolution. | **Fixed and checked:** M3 × 6 screws flush at 91; swept-ring check ≥ 1.65 mm. |
| 6 | Fits and strength are provisional. | **Open:** coupons and rig. |
| 7 | No shop quote for the stub. | **Open:** drawing, then a quote. |
| 8 | The floating-motor alignment is unproven. | **Open:** rig, with drag, current and runout measured before and after tightening. |

## 7. Motor assumptions and where they live

| Assumption | Value | Encoded in | If the received motor differs |
|---|---|---|---|
| Face holes | 2 × M3 at ±8.5 mm on the axle line, 5 mm deep | Motor plate only | Reprint the plate (carrier) |
| Pilot | Ø7 × 2.5 | Plate hole and recess | Reprint the plate |
| Shaft | Ø4, 3.5 across the flat, 12 mm long, flat on the last 8 mm | Stub bore depth and set-screw position (74.8 must land on the flat) | Re-turn the stub, or move the set screw if the flat is still under it |
| Gearbox length | 21 mm | Carrier cradle (J04), not this stack | Adjust the carrier |

## 8. Next

1. **Stub drawing, then a quote** from a local turning shop.
2. **Coupons**, on the lab printer: bearing bores Ø15.90–16.10 in 0.05 mm steps; spigot bore Ø9.9–10.1; M3 × 4/6 insert sections; plate counterbore section; and J04 key/rail-end pair. Record printer, material, orientation, settings and measured fits.
3. **Wheel model port.** Done in D-009; rerun `check_wheel_on_chassis.py` after the new J04 cheeks and complete `check_layout.py` against this revision before release.
4. **Axle rig** once motor, bearings and stubs arrive. The fixture concept and numeric criteria are specified in §9.

## 9. J04 carrier and test plan

### Selected CAD architecture

Each motor side has one replaceable printed carrier combining the 5 mm motor plate with its front and rear cheeks. The bearing housing and 1.2 mm cap remain separate service parts. The carrier's cheeks seat against the two split rails at X = +17 and −17 mm. This keeps the left and right wheel axes independent; no shaft spans the chassis centreline. The front/rear crossmembers and deck continue to tie the rail pairs together.

Each rail end has a 2.0 × 3.0 × 2.5 mm locating key and matching 2.4 × 3.4 × 3.2 mm pocket (0.2 mm nominal side clearance, 0.7 mm end clearance). Two axial M3 insert pilots sit at Z = 38 and 48 mm on each interface: Y = ±54 mm at the front and ±58.5 mm at the rear. DIN 7984 M3 × 8 low-head screws enter from the open motor bay through 1.7 mm-radius cheek clearance holes and 2.9 mm-radius × 2.1 mm-deep head recesses into 6 mm rail inserts. There are four screws and four inserts per carrier, eight of each for the chassis. The rail bores include a 1 mm screw-tip relief beyond the insert.

The assembly datum is the carrier-to-rail cheek face at X = ±17 mm, with the asymmetric key setting Y/Z position. Screws clamp the faces; the key, not screw friction, locates the carrier. Load path: tyre → rim/stub → bearing pair → housing/cap screws → carrier plate and cheeks → keyed rail faces and J04 screws/inserts → rails → deck/crossmembers/body. The screws are reachable from the motor-relief opening after the motor and wheel-side stack are removed; the carrier withdraws toward the chassis centre once both rail-end joints are released.

These dimensions are starting print geometry, not calibrated fits. The 0.2 mm key allowance and Ø4.3 mm insert pilots must be adjusted from coupons for the selected printer and material. Motor-face dimensions remain assumptions until the motor is measured.

### Coupon and assembly gates

1. **Supplier part and drawing.** Procure four 688 ZZ bearings through the selected [OnlyScrews listing](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5) when it is available. Confirm the maker, ZZ shields, dimensions, lot and drawing/load data; the listing currently says sold out and does not publish a maker or ratings. Keep the delivered-lot evidence with CH-015.
2. **Fit coupons.** After printer/material/orientation are selected, print outer-bearing-seat coupons at Ø15.90, 15.95, 16.00, 16.05 and 16.10 mm, plus the stub-spigot bore, insert sections and J04 key/rail pair. Record post-print bore, actual bearing insertion force, race drag and shield clearance. Verify the turned stub's Ø8 k5 seat with the received bearing. Select a free-to-light-press outer fit captured by the shoulder/cap; do not force a distorted bearing into the housing.
3. **100 N inner-ring retention test (motor-independent).** Assemble the actual bearing pair on the finished stub using the selected k5 seat and Loctite 641 cured per its datasheet. Capture the outer rings with the selected housing/cap and clamp that stationary stack in a guarded axial test fixture. Pull the stub outward to 100 N for 10 s with a calibrated force readout; measure inner-ring-to-stub relative movement. Pass: <0.10 mm movement, no bearing damage or loss of free rotation after unloading. Test both side assemblies and record bearing lot, stub dimensions, compound/cure, fixture and readings. A motor is not part of this load path.
4. Pull each candidate M3 insert coupon axially to 100 N. Pass: no insert movement, boss split or permanent bore growth. Record the insert SKU, print orientation and result in BOM CH-054/CH-061.
5. Assemble one carrier to two rail coupons. Pass: key seats by hand without forcing; datum-face gap ≤0.10 mm; both rails coplanar within 0.20 mm; screws reach full insert engagement without bottoming; no cracking or insert spin after three assembly cycles.
6. On the side-specific axle rig, at service loads 31 N radial and 8 N lateral, axle-datum deflection must be ≤0.25 mm and worst-case measured wheel running clearance must remain ≥1.5 mm through a revolution. At 2× proof loads (62 N radial, 16 N lateral and 0.8 N·m drive torque), no crack or insert movement is allowed; residual axle-datum set after unloading must be ≤0.10 mm.
7. Powered axle acceptance: tyre runout ≤0.30 mm TIR; axial end play ≤0.10 mm; after face screws are tightened, no-load current change at the same 6.0 V and duty must be within max(0.05 A, 10% of baseline); complete 200 low-speed reversals with no set-screw mark shift, rubbing, cracks or bearing damage. Record temperature rather than claiming a polymer limit until print material is selected.

The test loads are conservative design targets based on D-007's 31 N radial, 8.3 N lateral and 0.40 N·m torque cases; they are pass/fail proposals, not measured material allowables. The 100 N bearing-retention fixture can be prepared and run without a motor after the actual bearings, stubs and cured print process are available. The integrated axle rig and powered acceptance checks wait for the motor.
