# Chassis v1 joint register

**Status:** working engineering register, not a fabrication release. It records the joint architecture in current CAD and source documents, including gaps between them. “Defined in CAD” means geometry and intended load path exist; it does not mean fit, strength, service access or physical tests have passed. Printer/nozzle/material are not selected and no motor is on hand.

**Coordinates:** chassis origin at axle line on floor; +X forward, +Y robot-left, +Z up. Counts are for one chassis unless noted. “Open” names detail or evidence still required before release.

## Summary

| ID | Interface | State | Main release gate |
|---|---|---|---|
| J01 L/R | Motor face to carrier | Provisional CAD | Motor pattern, screw engagement, clamp and alignment |
| J02 L/R | Bearings, housing, cap and stub | Designed; fits provisional | Supplier drawing/lot, fit coupons, retention and endplay |
| J03 L/R | Motor shaft to stub to wheel | Designed; fit/torque provisional | Motor fit, shaft coupling, runout and reversals |
| J04 L/R | Carrier to front/rear rails | Defined in CAD | Coupon fit, insert pull-out and loaded stiffness/clearance |
| J05 | Front crossmember to rails | Provisional CAD | Receiver match, inserts, fit and load proof |
| J06 | Rear crossmember to rails | Provisional CAD | Receiver match, inserts, fit and impact/torsion proof |
| J07A | Ball caster to pod | Defined in CAD (D-011) | Received-caster measurement, insert pull-out, load tests |
| J07B | Pod to front crossmember | Defined in CAD (D-011) | Insert coupon, tool access and load test |
| J08A | Range sensor to pod | Defined in CAD (D-011) | Vibration retention and lens alignment |
| J08B | Nose cap/snap fingers/Hall sensing to pod | Defined in CAD (D-011, D-013) | Bench trip point, spring return, finger fatigue, removal cycles |
| J08C | Sensor lid to pod | Defined in CAD (D-011) | Dry-fit, removal cycles, screw strip torque |
| J09A | Rear keel to rear crossmember | CAD defined (D-014) | Insert coupon; skid load and impact test |
| J09B | Rear TCRT cartridge to keel | CAD defined (D-014, D-016); soldered lead, no board | PCB-10 J10-10 change; optical height on real floors |
| J10A | Wear shoe to keel | CAD defined (D-014); PETG recommended (D-017) | Retention and abrasion test |
| J10B | TCRT guards to keel | CAD defined in the J09B bezel (D-014) | Floor-strike and sensor-protection test |
| J11A | Battery hatch to tub | Provisional geometry | Add screw/insert BOM items; retention test |
| J11B | Battery pack to tub | Not fully defined | Restraint, isolation, access and safe removal |
| J12 | Ballast bar to deck | M3 × 12 CSK candidate modeled with a 90° seat (D-026) | Verify received head against the seat, tool/load check |
| J13 | Body frame to chassis deck | M4 × 12/plain nut candidate stack defined | Verify head seat, pin fits, nut access and lift-off |
| J14 | TPU tyre to wheel rim | Designed in wheel CAD | Material/process fit, clamp, creep and runout |
| J15A | IMU board to deck | Modeled | Board-hole confirmation and screw fit |
| J15B | Drivers/boards/cable restraints | Incomplete | Mount hardware, strain relief, access and service |
| J16 | Split decks to rails | Provisional CAD | Insert/screw BOM, fit, racking and tool access |

## Detailed interfaces

### J01 L/R — motor face to carrier

- **Parts/load path:** ThinkRobotics MOT3001-6V230RPM motor face to integrated printed carrier plate. Motor reaction torque passes through face screws into carrier; wheel radial load is carried by the separate bearing stack.
- **Location/joint:** assumed Ø7 pilot boss in Ø7.6 plate opening (0.3 mm nominal radial float); two assumed M3 face holes at ±8.5 mm on axle line. Motor floats while stub is aligned; screws tighten last.
- **Hardware/clamp:** 2 × DIN 7984 M3 × 6 per motor (CH-030), through Ø3.6 holes with Ø6.5 × 2.2 counterbores, into assumed 5 mm-deep motor threads. Modeled stack gives ~3.2 mm thread engagement after 2.8 mm clamp. Loctite 222 proposed (CH-057).
- **Material/access/service:** candidate PETG carrier; actual material and motor threads unknown. Reach screws through housing key slots with a long 2 mm hex key. Remove axle cartridge/wheel-side stack as needed, then motor inward per J04. Tool access is not dry-run.
- **Proof/state:** CAD architecture present. Measure received motor face pattern, pilot, threads/depth and gearbox envelope; inspect counterbore walls and verify drag/current before and after final tightening. **Open until motor receipt and fit test.**

### J02 L/R — bearing pair, housing, cap and stub

- **Parts/load path:** two OnlyScrews-listing 688 ZZ bearings (CH-015; 8 × 16 × 5) per side, printed housing CH-051, aluminium cap CH-052, steel stub CH-012 and carrier. Radial load: stub → races → housing → cap screws/carrier. Axial loads: stub shoulder/compound and housing shoulder/cap.
- **Location/joint:** Ø8 k5 stub seats at |Y| 76.51–86.51; Ø9.5 shoulder locates inner rings. Housing outer seat Ø16 × 10 mm is coupon-tuned; outer rings captured between housing shoulder and cap. Cap Ø12.5 land must contact outer ring only. No preload intended. Set-screw station is |Y| 74.8 so its Ø2.5 tap drill clears the first bearing face by 0.46 mm; verify the actual turned hole edge and bearing-land transition before release. A shared 0.01 mm axial datum offset avoids a degenerate mirrored housing boolean and is far below process tolerance.
- **Hardware/clamp:** 4 × ISO 7380 M3 × 18 screws and four M3 × 4 heat-set inserts per side (CH-053/054; eight each total). Outward inner-ring retention is Ø8 k5 plus Loctite 641; no circlip modeled. Loctite 222 proposed on screws/set screw (CH-057).
- **Material/fit/access/service:** housing is a candidate structural print; process/material unselected; cap 1.2 mm aluminium. Coupon housing seat at Ø15.90–16.10 mm in 0.05 mm steps and verify actual bearing/stub. Replace by removing wheel, set screw, four cap screws, then slide housing/cartridge outboard; press bearings off via inner rings.
- **Proof/state:** D-012 selects the OnlyScrews 688 ZZ listing, with stock observed on 2026-09-30 and recorded in the [project BOM](../../BOM.csv); the page still omits maker, drawing and load rating. Confirm the supplied lot; check fit, shield contact, race drag, runout, endplay ≤0.10 mm target and the 0.46 mm set-screw-hole edge margin. Pull inner-ring/stub joint to 100 N for 10 s with <0.10 mm relative motion. **Designed; procurement, physical fit and retention open.**

### J03 L/R — motor shaft to stub to wheel

- **Parts/load path:** motor 4 mm D-shaft → EN8/C45 stub CH-012 → flange → wheel web CH-004. Torque passes through set screw on motor flat and three wheel screws into wheel.
- **Location/joint:** Ø4.05 H8 bore gives 8 mm shaft engagement; DIN 916 screw bears on flat at |Y| 74.8 (D-012, maintaining tap-drill edge clearance to the wider bearing). Ø10 g6 stub spigot locates wheel in Ø10 H7 hub bore; stub shoulder/bearing stack establish axial datum.
- **Hardware/clamp:** 1 × DIN 916 M3 × 2.5 set screw with Loctite 222 per side (CH-055/057); 3 × ISO 7380 M3 × 6 into flange per side (CH-056; six total), modeled 2 mm thread engagement. Six M2 × 6 thread-forming cap screws per side (CH-059) retain the hub cover, not the torque joint.
- **Material/access/service:** turned steel stub; wheel/carrier candidate PETG, tyre TPU. Access set screw through housing slot with 1.5 mm key after wheel removal. Wheel removal: cap off, three M3 screws out, pull from spigot. Stub drawing/quote open.
- **Proof/state:** nominal CAD checks exist. Verify motor shaft fit, spigot, concentricity, runout ≤0.30 mm TIR and no set-screw mark shift after 200 reversals. **Design defined; coupling/torque proof open.**

### J04 L/R — carrier to front/rear rail ends

- **Parts/load path:** one integrated printed motor plate/front cheek/rear cheek carrier per side joins split rail ends. Load path: tyre/stub/bearings → housing/cap → carrier → keyed rail faces and screws/inserts → rails → crossmembers/deck/body.
- **Location/joint:** datum at X = ±17 mm. Each cheek has a 2 × 3 × 2.5 mm key; rail pocket 2.4 × 3.4 × 3.2 mm (0.2 mm nominal side clearance, 0.7 mm end allowance). Key locates Y/Z; screws clamp faces.
- **Hardware/clamp:** two DIN 7984 M3 × 8 screws at Z = 38/48 at each of two interfaces; 6 mm axial M3 rail inserts. Four screws/inserts per side, eight each total (CH-060/061). Cheek holes R1.7, recess R2.9 × 2.1; insert pilot Ø4.3 with 1 mm tip relief.
- **Material/access/service:** one printed carrier per side and four rail print units; structural material/process unselected. Screws are reached from motor-relief bay after removing motor and wheel-side stack; carrier withdraws toward chassis centre. Tool path and cheek strength unproven.
- **Proof/state:** nominal CAD architecture defined. Coupon targets: key seats by hand, face gap ≤0.10 mm, rails coplanar ≤0.20 mm, no bottoming/cracks/spin after three cycles. Insert pull-out ≥100 N. At service loads 31 N radial/8 N lateral: deflection ≤0.25 mm and wheel gap ≥1.5 mm; at 2× proof no crack/movement and residual set ≤0.10 mm. **Physical gates open.**

### J05 — front crossmember to front rails

- **Parts/load path:** front crossmember to both front rails; caster pod loads enter crossmember and pass to rails/deck.
- **Location/joint:** 3 mm rail tongue at each end engages matching pocket at 0.2 mm nominal clearance. Screw axes Y = ±54, Z = 41 mm.
- **Hardware/clamp:** frame-split study proposes 1 × M3 × 16 button-head screw per side from +X into axial short M3 heat-set rail inserts; two total. Pilot/clearance geometry is provisional (Ø4.3 × 6 insert pilot). J05 fastener/insert rows are **missing from chassis BOM**.
- **Material/access/service:** candidate structural prints; crossmember spans Y ±62. Fit tongue first, drive from front; caster pod may need removal for tool access. Exact screw/washer/insert, engagement, edge distance and tolerance open.
- **Proof/state:** geometry modeled, receiver fit/load unproved. Coupon, check coplanarity and tool access with pod/shell; load-test pod/crossmember path. **Open.**

### J06 — rear crossmember to rear rails

- **Parts/load path:** rear skid crossmember to both rear rails; skid impact and frame torsion pass into rails/deck.
- **Location/joint:** 3 mm rail tongues engage crossmember pockets; axes Y = ±58.5, Z = 41 mm. Rail ends widen locally to Y ±66.
- **Hardware/clamp:** provisional 1 × M3 × 20 button-head screw per side from −X into axial short M3 rail inserts; two total. Pilot/head geometry provisional; J06 hardware rows are **missing from chassis BOM**.
- **Material/access/service:** candidate structural prints. Assemble tongues first and drive from rear; body may need lifting for tool access. Exact screw/washer/insert, engagement, edge margin and tolerance open.
- **Proof/state:** concept geometry only. Coupon fit, dry-run access and coplanarity; load/twist rear crossmember and inspect insert movement/cracks. **Open.**

### J07A — Pololu #2691 caster to printed pod

- **Parts/load path:** the vendor base's top face seats on the 6 mm pod seat (Z 29–35). Ball reaction goes into the pod through that face; the screws only clamp.
- **Location/joint:** three holes at 120° on the 14.08 mm bolt circle (0°, 120° and 240° about X 110). Pololu's drawing 2691 shows a 2.7 mm web with Ø6.3 counterbores from the ball side, and the model now includes them.
- **Hardware/clamp:** 3 × ISO 7380 M3 × 8 (CH-031), driven from below through the web into 3 × CNC Kitchen M3 × 5.7 inserts (CH-063). The inserts are pressed from the seat face into Ø4.0 bores and sit flush with it. Thread engagement is 5.3 mm. Button heads sit 0.43 mm off the ball ([D-011](../../decisions.md#d-011)).
- **Access/service:** from below with the body on and nothing else removed.
  1. Unsnap the housing (ball and rollers come with it).
  2. Undo the three screws with a 2 mm hex key.
  3. Lower the base.

  `cad/check_nose_service.py` sweeps each of these steps clear.
- **Print:** pod seat face down (3.4 % support area).
- **Proof/state:** CAD defined; `check_layout.py` → `ball_screws_thread_into_seat_inserts`. **Open:**
  - measure the received #2691 (web, counterbore, hole Ø);
  - insert pull-out coupon;
  - static, drop and threshold tests at 2.55 kg with limits set first.

### J07B — pod to front crossmember

- **Parts/load path:** the pod's rear face bears on the crossmember front face at X 92. The caster and nose loads enter the crossmember.
- **Location/joint:** two horizontal M3 axes at Y ±10, Z 42, driven +X → −X from inside the sensor pocket.
- **Hardware/clamp:** 2 × ISO 7380 M3 × 8 (CH-032): 3 mm of pod wall plus 5 mm in 2 × CNC Kitchen M3 × 5.7 inserts (CH-033). The inserts sit in Ø4.0 crossmember bores, which give 0.3 mm/side of knurl interference. This closes the old insert-location conflict: the inserts are in the crossmember.
- **Access/service:** sensor and lid out. A 2 mm L-key has about 12 mm between the heads and the GP2Y body, so check tool reach at the dry run.
- **Proof/state:** CAD defined. **Open:** insert coupon, dry-run access and load test.

### J08A — front range sensor to pod

- **Parts/load path:** the GP2Y0A21YK0F (CH-018), modeled from its vendor STEP ([D-027](../../decisions.md#d-027)), sits directly on the pod floor (Z 35) with its lenses forward and its connector up. Both mounting ears are trimmed off at the 29.5 mm body at assembly. The side slots that used to take the ears are now vestigial.
- **Location/joint:** the pocket walls locate the body in Y. It has 0.25 mm per side ahead of X 122.1 (±15.0) and 0.7 mm per side behind (±15.5). The lid underside (Z 49) is 1 mm over the body top (Z 48) and 0.5 mm over the connector, with its hump, so the lid retains the sensor as well. No separate clip. The J10-8 wires are soldered to the S3B-PH pins with no plug. They run rearward inside the lid hump, then down behind the sensor (X 109–114.5) to the floor channel.
- **Access/service:** J08B cap off, then J08C lid off. Lift the sensor straight up with its soldered lead. The Hall board (J08B) can only come out after the sensor, whose body stands over its slot. The lead and the Hall pair leave as one J10-8 cable:
  - through a round-cornered slot in the pod's back wall (Z 32–35, 1 mm flared mouth);
  - under the crossmember;
  - up a Ø5 bore through the crossmember and deck at (86, −31);
  - into the sensor trunk, and on to C3 J10-8.
- **Proof/state:** CAD defined; the removal path is swept in `nose-service.md` (subset C, D-027). **Open:** fit of the received unit against the vendor STEP; ear trim quality and lead strain relief; vibration retention; lens alignment on the print.

### J08B — nose touch cap and contact sensing to pod

- **Parts/load path:** the cap (CH-007) slides on the pod's constant-section nose (X 122.5–128.5) with a 0.5 mm running gap. A push travels 3.0 mm rearward until the cap's inner face stops on the pod face.
- **Retention and return:** two vertical snap fingers, 2.0 × 16.5 mm, hold the cap. Their 0.8 mm hooks ride in flank slots, at about 2.2 % strain for a 1 mm spread. Two Ø3 × 10 stainless springs (CH-066) in seat pockets at Y ±3 push the cap back against the hooks: about 0.4 N preload, about 1.6 N at the stop.
- **Removal:** spread the finger tips and slide the cap forward.
- **Sensing ([D-013](../../decisions.md#d-013)):** contactless, so nothing bottoms out.
  - A Ø2 × 1 N35 magnet (CH-065) sits in the cap wall.
  - A DRV5055A3 linear Hall sensor (CH-019) sits on a 6.0 × 4.6 mm board (CH-064) in a slot in the seat's front face. It clears the magnet by 3.1 mm at rest and 0.1 mm at the stop.
  - C3 trips at rest + 5 mT: 0.71 mm of cap travel nominal, 0.50–0.95 mm across tolerances. See [nose-hall-board.md](research/nose-hall-board.md).
- **Print:** nose face down (2.8 % support area).
- **Proof/state:** CAD defined; `check_nose_joints.py` → `touch_cap_sweeps_3mm_rearward` (includes the magnet clearance at the stop), `touch_cap_running_clearance`. **Open:**
  - bench trip point 0.4–1.2 mm;
  - spring rate and return;
  - snap-finger fatigue;
  - removal cycles;
  - PCB-10 J10-8 pin change (+3V3 and HALL_OUT replace the switch pair).

### J08C — sensor lid to pod

- **Parts/load path:** the lid (CH-003) carries only cover and contact loads.
- **Location/joint:**
  - a rear 12 × 1.5 × 2 mm tongue drops into a pod-wall groove that is open forward;
  - the shell band overhangs the lid top by 0.5 mm with the body on;
  - one M2 × 8 countersunk thread-forming screw (CH-062) goes into a pod boss at (111.8, −11.8), behind the sensor body (D-027; it was at X 124.6, inside the real sensor's footprint);
  - a hump over the sensor header (to Z 58.6), open 11.5 mm rearward so the lid can make its 11 mm forward slide; the cap has a matching top notch that clears the hump through its 3 mm travel.
- **Access/service:** cap off, screw out, slide forward 11 mm, lift. With the body off, the rear is held only by the tongue.
- **Print:** on its side (3.4 % support area).
- **Proof/state:** CAD defined. **Open:** dry-fit, removal cycles, and screw strip torque in PETG.

### J09A — rear keel to rear crossmember

- **Parts/load path:** printed keel (CH-008) seats flat on the rear crossmember underside at Z 34; skid load goes through four screws into the crossmember and on to both rails.
- **Location/joint:** four vertical screws at X −36.5 / −44.0, Y ±5.5. The rear pair moved 1.5 mm forward of the old X −45.5 so the insert keeps a wall to the crossmember's rear face.
- **Hardware/clamp:** four ISO 4762 M3 × 30 (CH-034) into CNC Kitchen M3 × 5.7 inserts (CH-067) pressed from below; engagement 5.5 mm (front pair) and 5.7 mm (rear pair), limited by the insert length. Heads sit in Ø6.5 counterbores, recessed 0.5 and 1.5 mm. The old Ø6 cable bore through the crossmember is closed.
- **Material/access/service:** screws drive from below with the keel, shoe and bezel fitted (hex-key paths clear in CAD). Keel removal: pull the sensor and its lead out below (J09B), then undo four screws.
- **Proof/state:** CAD defined ([D-014](../../decisions.md#d-014)); `cad/check_rear_keel.py` passes. **Open:** insert pull-out coupon, strip torque, skid impact and bending test.

### J09B — rear TCRT cartridge to keel

- **Parts/load path:** the TCRT5000 sits in a pocket open below the keel belly, face down on 0.6 mm end ledges of a printed bezel (CH-010). A 4-wire GH lead is soldered to its legs under heat-shrink (CH-020, [spec](research/rear-tcrt-lead.md), D-016) and leaves straight up through the pocket, which runs out through the keel top.
- **Location/joint:** optical height = keel belly (Z 12) minus 1 mm shims (CH-068): two shims give the nominal Z 10; zero to four give Z 12 to 8 (±2 mm). The shims have a window, so nothing bears on the leads; the flexible lead and its slack loop take up the travel.
- **Hardware/access/service:** one M2 × 10 thread-forming screw (CH-069) and a moulded Ø1.8 pin fix bezel and shims. Sensor swap from below with the keel on: screw out, bezel and shims off, unplug J10-10 at PCB-10 (rear panel off), cut the zip tie, and pull the sensor and lead down through the pocket. The keel comes off only after that; there is no disconnect at the keel. The lead rises behind the crossmember, with a 30 mm slack loop, a zip tie (CH-072) at a lug on the crossmember's rear face, and a route beside PCB-02 and over PCB-04 to C3 J10-10.
- **Proof/state:** CAD defined (D-014). **Open:** PCB-10 J10-10 circuit, optical height on real floors, joint sleeve and lead bend in hardware.

### J10A — wear shoe to keel

- **Parts/load path:** 12 × 10 × 2.5 mm shoe (CH-009) backed by the flat keel belly; a 2.5 mm dovetail tongue on its top runs in a groove open at the keel's front.
- **Location/joint:** the shoe slides in from the front and stops on the groove end. One M2 × 6 thread-forming screw (CH-070) crosses the tongue from the keel's +Y side, with clearance in the keel and threads in the shoe.
- **Material/access/proof:** PETG recommended ([D-017](../../decisions.md#d-017)). Swap: screw out, slide forward. **Open:** retention and abrasion test.

### J10B — TCRT guards to keel

- **Parts/load path:** both guard lips (Z 7.0–8.5) are part of the J09B bezel, so they are retained by its screw and pin and seat on the shim stack along their full length.
- **Location/joint:** lips at Y ±5.6, X −61.5 to −49. They move with the sensor across the J09 height range, so the lip-to-face offset is constant (3 mm below the face).
- **Hardware/access/proof:** as J09B; bezel in PETG (D-017). **Open:** floor-strike, snag and optical-field test.

### J11A — battery hatch to tub

- **Parts/load path:** removable bottom hatch closes tub floor; pack weight bears on hatch and transfers to tub/deck bosses.
- **Location/joint:** separate hatch and four external bosses are modeled; pack should drop downward after hatch removal.
- **Hardware/clamp:** frame-split study proposes 4 × M3 × 6 button-head screws from below into short M3 inserts in bosses; Ø4.3 × 6 mm pilots provisional. These four screw/insert items have **no dedicated chassis BOM IDs**. SKU, washer/head stack, engagement and boss edge margin open.
- **Material/access/service:** candidate structural prints. Support robot, disconnect/isolate battery, then reach all four screws from below. Check pack/wire clearance and access.
- **Proof/state:** add BOM rows, coupon insert fit/pull-out, cycle hatch, verify inversion/shock retention and safe removal. **Provisional; BOM incomplete.**

### J11B — battery pack to tub

- **Parts/load path:** two-cell pack sits in tub with nominal pad clearance; inertia must transfer to tub without loading cells/wires.
- **Location/joint:** CAD has tub walls/removable floor but no defined strap, foam specification, positive restraint or cell separator.
- **Hardware/access/proof:** connector exits +Y service window; disconnect/isolation must precede hatch removal. Define pad/strap, compression, cable slack, insulation and service sequence; shock-test and verify safe removal. **Open.**

### J12 — ballast bar to front deck

- **Parts/load path:** 9 × 60 × 19 mm steel bar under deck; two screws transfer ballast inertia to front deck.
- **Location/joint:** flat face seats on deck underside; two axes at X = 74, Y = ±20. 90° countersinks, Ø6.5 at the deck top, modeled from above (D-026).
- **Hardware/clamp:** 2 × M3 × 12 countersunk screws (CH-038, modeled to ISO 7046-1: Ø6.3 theoretical head, k 1.65) into 9 mm-deep tapped holes in the bar. The head seats 0.1 mm below the deck top, giving 8.1 mm of engagement and 0.9 mm of tip clearance to the hole floor (`cad/check_battery_ballast.py`). Confirm the received head angle and diameter against the seat before release.
- **Material/access/service:** steel bar, candidate printed deck. Access from deck top before packaging closes the area; check narrow gap to tub and front crossmember.
- **Proof/state:** confirm received screw head fit, torque and tool access; test loosening and deck crushing/cracking under vibration/impact. **Hardware candidate defined; fit/proof open.**

### J13 — body frame to chassis deck

- **Parts/load path:** body-frame feet/pads to split decks. Four M4 bolts clamp; two diagonal pins carry repeatable lateral location/shear.
- **Location/joint:** four Ø4.5 clearance holes at modeled points; two Ø4 pins in Ø4.1 nominal holes; pins establish XY datum, bolts clamp pads to deck.
- **Hardware/clamp:** candidate stack is 4 × M4 × 12 button-head through-bolts and four accessible M4 plain hex nuts (CH-035/036), plus 2 × Ø4 × 8 mm pins (CH-037). Current modeled clamp stack is 4 mm frame foot + 4 mm deck + 3.2 mm nut = 11.2 mm, leaving about 0.8 mm nominal thread projection without washers. Confirm actual head seat, nut height, stack, and projection on the received parts; add washers only if the resulting stack is rechecked.
- **Material/access/service:** printed frame candidates. Bolt heads from above; nuts held from below through rail socket paths. Remove bolts and lift body vertically off pins. Verify slim-socket access with tub/rails/shell installed.
- **Proof/state:** check pin/hole fit and foot coplanarity; dry-run access/lift-off; test clamp retention, deck crushing and body shear under representative mass. **Candidate stack defined; fit/proof open.**

### J14 — TPU tyre to wheel rim

- **Parts/load path:** handed TPU 95A tyre on PETG rim; torque/traction transferred through 12 keyed ribs and clamped sidewalls.
- **Location/joint:** twelve 0.8 mm ribs on Ø74 seat engage tyre slots; integral 2 mm inboard lip and 3 mm outboard clamp ring overlap tyre by 2 mm. Target tyre bore Ø73.6 (~0.5% stretch), width 19.3 mm (~0.3 mm clamp); print fit unproven.
- **Hardware/clamp:** 6 × ISO 7380 M3 × 8 screws into 12 M3 × 4 heat-set inserts per wheel, Ø68 BCD (CH-048/049; 12 each total). Insert article/process fit open. Spin index removed; no separate index joint.
- **Material/access/service:** TPU 95A availability unknown; D-005 records an unmodeled three-O-ring fallback. Remove six ring screws to change tyre without wheel removal.
- **Proof/state:** coupon tyre/rim and inserts; measure loaded radius, L/R diameter match (~0.3 mm target), runout, clamp retention, stall creep and grip. **Designed; material/physical proof open.**

### J15A — IMU board to deck

- **Parts/load path:** PCB-07 IMU to deck crossbar; board vibration/mass passes through two screws into deck.
- **Location/joint:** 16 × 20 × 1 mm board flat on deck; two holes modeled at X = 22, Y = ±7.5.
- **Hardware/clamp:** 2 × M2 × 5 thread-forming screws (CH-039) into nominal 4 mm deck; CAD assumes 4 mm thread engagement. Confirm PCB clearance and head/component stand-off.
- **Material/access/proof:** connector points −X; install before body/electronics closure. Verify tool access, board flatness/interference and vibration retention. **Modeled; fit unconfirmed.**

### J15B — drivers, other boards and cable restraints

- **Parts/load path:** DRV8874 carriers, sensors/connectors and harness segments to deck/frame. Motor reaction and cable pull must not load connector solder joints.
- **Location/joint:** board/envelope placements and some cable routes exist, but full mounting bosses/holes, clips, strain-relief points and service disconnects are not defined.
- **Hardware/access/proof:** no complete chassis clip/fastener schedule in BOM. Connector schedule is integration reference, not a released mount design. Define hardware, strain relief, mating access and removal order; perform tug/vibration/service checks. **Open.**

### J16 — split deck prints to rails

- **Parts/load path:** front/rear deck prints clamp to four rail segments; deck transfers body, battery, ballast and crossmember loads into rails.
- **Location/joint:** deck lands on rail tops. Six positions: front at X = 30/70, Y = ±54; rear at X = −25, Y = ±58.5; vertical screw axes.
- **Hardware/clamp:** frame-split study proposes 6 × M3 × 8 screws from above into short M3 rail inserts. Deck holes Ø3.4, insert pilots nominal Ø4.3 × 6; local 8 × 8 mm deck ears support heads/washers. These six screws/inserts have **no dedicated chassis BOM IDs**.
- **Material/access/service:** separate candidate prints; calibrate insert/hole fit. Assemble rails/crossmembers first, decks second, before body and upper packaging. Above access may be blocked after body installation.
- **Proof/state:** add BOM rows/select hardware; coupon, check coplanarity/racking and access, then test bending/shear and insert pull-out. **Provisional; BOM incomplete.**

## Release actions

1. CAD receiver gaps are closed: J07/J08 by D-011, J09A/B and J10A/B by D-014. Confirm the J07B and J09A crossmember insert fit and screw engagement with the real hardware.
2. Add BOM rows for J05, J06, J11A and J16 hardware; select J12 screw and complete J13 clamp stack.
3. Select printer/nozzle/material/orientation and insert articles. Print coupons for bearing fits, insert orientations, keys/tongues and thin walls; record dimensions and pull-out results.
4. Update J01/J03 using measured motor/stub hardware when received. Build axle rig and record test results separately from CAD checks.
5. Dry-run assembly/service with body installed, including tool access, wiring disconnects, battery isolation/removal, and per-part print/export validation.
