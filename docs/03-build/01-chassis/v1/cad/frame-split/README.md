# Frame print-split study

**Status:** detailed provisional split, not a fabrication release. Open `frame-split.step` in CAD Viewer. `frame-split.step.py` is the editable source. This view calls the same frame print-unit geometry as the main `chassis-v1.step.py` assembly.

The view keeps the chassis coordinate system: origin at the axle line on the floor, +X forward, +Y robot-left, +Z up. The gray motor barrels and green battery block are **reference envelopes**, not print units. They show why the top deck has a motor relief and battery aperture. This frame-only view leaves the rail ends visible; the integrated J04 carriers are defined in the main chassis CAD and [axle-stack §9](../../axle-stack.md#9-j04-carrier-and-test-plan). J04 print fit and strength proof are still open.

## Provisional print units

| Part label | Quantity | Current extent / purpose |
|---|---:|---|
| `FS_DECK_REAR` | 1 | Rear deck, X −41 to −17; rear body holes and rail clamp holes |
| `FS_DECK_FRONT_BATTERY_TUB` | 1 | Front deck, X +17 to +92; battery opening and tub walls, front body holes, ballast and rail clamp holes |
| `FS_RAIL_L/R_REAR` | 2 | Rail segments from the rear crossmember to the carrier boundary |
| `FS_RAIL_L/R_FRONT` | 2 | Rail segments from the carrier boundary to the front crossmember |
| `FS_CROSSMEMBER_REAR` | 1 | Rear transverse member, X −48 to −32, Z 34 to 48; keel/sensor clearance reserve |
| `FS_CROSSMEMBER_FRONT` | 1 | Front transverse member, X +80 to +92, Z 35 to 51; existing pod screw axes retained |
| `FS_BATTERY_HATCH_FOUR_M3` | 1 | Separate downward-removable hatch with four M3 clearance holes |

This is nine proposed print units. The front deck and tub walls are shown as one print; the hatch stays separate. The study deliberately keeps the rails and crossmembers separate so their joints can be reviewed. Fusing any of these units requires a printer-volume and orientation review, followed by a revised part map.

## Joint concept in the view

1. **Crossmember to rail (J05/J06).** Each rail has a 3 mm pilot tongue at its crossmember end. The member has a matching pocket with 0.2 mm nominal clearance. A front M3 × 16 screw from X +92 or rear M3 × 20 screw from X −48 passes through the crossmember and enters a short M3 heat-set insert in the rail end. One screw and tongue per side. The front joint axes are at Y ±54; the rear axes move outward to Y ±58.5 so their inserts do not intersect the nearby body-nut access path. The crossmembers extend to Y ±62 front and Y ±66 rear to retain material around the pockets. Front pod screws remain at Y ±10 and do not block the rail screws.
2. **Deck to rail.** Six candidate M3 × 8 screws enter short M3 heat-set inserts in the rails: X 30 and 70 at Y ±54 on the front rails, and X −25 at Y ±58.5 on two small rear deck ears. The rear axes are outside the body M4 nut clearance. The four-millimetre deck is drilled Ø3.4; the rail has a nominal Ø4.3 × 6 mm insert bore. Local deck ears support the screw-head/washer footprint. Heads are approached from above before the body is installed.
3. **Body M4 receiver access (J13).** The rails have open vertical socket paths at the four body bolt positions (Y ±48), with a local outside rib replacing the removed section. The model includes a 10 mm OD, 18 mm long reference socket at each location; it clears the rail, battery tub and motor envelopes. This permits underside M4 nuts with the existing through-bolts. Nut standard, washer, bolt length and loaded joint proof remain to be selected.
4. **Battery hatch (J11).** Four bosses are integral with the front deck/tub print, outside the thin tub walls. Four candidate M3 × 6 button heads enter underside short inserts through the 1.5 mm hatch. The hatch extends far enough beyond the screw axes for an M3 washer. The downward pack removal path and +Y connector service window remain open. Pack foam/restraint and electrical isolation belong to battery integration.
5. **Carrier boundary (J04).** The rail ends stop at X ±17 and mate to the keyed carriers in the main chassis CAD. Their datum, locating keys, screws/inserts, load path and removal direction are defined in [axle-stack §9](../../axle-stack.md#9-j04-carrier-and-test-plan); coupon fit, tool access and structural proof remain open.
6. **Other service interfaces retained.** The four body M4 holes, two Ø4 locating-pin bores, battery opening and +Y tub service window, ballast axes, front pod screw axes and rear sensor clearance reserve are shown. Their complete clamp and receiver hardware belongs to their respective joint work packages.

The earlier body-nut/rail overlap is removed geometrically in this study. This is a clearance check, not yet a strength or tool-handling test; confirm that an actual nut and slim socket can be seated with a dry assembly.

## Working hardware schedule

| Joint | Candidate screw and access | Receiver | Qty |
|---|---|---|---:|
| J05 front member to rails | M3 × 16 button head, driven from the front at Y ±54 | Short M3 insert installed axially in each front rail end | 2 |
| J06 rear member to rails | M3 × 20 button head, driven from the rear at Y ±58.5 | Short M3 insert installed axially in each widened rear rail end | 2 |
| Deck to four rails | M3 × 8 button head, driven from above | Short M3 insert installed downward into each rail | 6 |
| J11 battery hatch | M3 × 6 button head, driven from below | Short M3 insert installed upward in each tub boss | 4 |

All 14 candidate M3 screws use small OD ≈7 mm washers. The nominal insert pilot is Ø4.3 mm, with at least 6 mm modeled depth. These are **working dimensions**, not selected supplier articles or proven printed fits; verify a real insert drawing and printed coupon before buying a full set or releasing print files. The inherited body joint uses four M4 through-bolts and nuts, separately specified under J13.

## Proposed assembly and service order

1. Print the nine units and the fit coupons. Ream or clean only the features called out by the calibrated process sheet. Install the 14 M3 inserts in the rails and tub bosses; reject any split or loose boss.
2. Fit the front and rear crossmembers to the rails by their tongues and pockets. Drive the front screws from X +92 and the rear screws from X −48. Check that both rails seat without forcing and that their upper faces are coplanar.
3. Place the rear and front decks on the rail tops. Drive the six deck screws from above, then check body-hole and locating-pin coordinates. Fit the J04 carriers at X ±17 per [axle-stack §9](../../axle-stack.md#9-j04-carrier-and-test-plan); keep the interface removable for service.
4. Install the rear keel and front caster pod from their separate joint work packages. Confirm their fasteners remain clear of the crossmember screws.
5. Fit the battery pack only after its electrical isolation/retention detail is approved. Connect through the +Y service window, then close the hatch from below with four screws. The pack should be restrained by a specified pad or fixture without crushing its cells or wiring.
6. Place the body on its two pins. Install the four M4 through-bolts from above and hold each nut with a slim socket from below through the rail cutout. Check the body lift-off path after removing those bolts.

For service: the hatch comes off downward after the robot is safely supported; the front crossmember screws are reached from the front after removing the pod if its wiring obstructs the tool; the rear screws are reached from the back with the body lifted if its shell obstructs the tool. A motor/carrier removal sequence belongs to J04 and must be dry-run before claiming frame serviceability.

## Work required before printable parts

- Measure the lab printer's usable build volume and confirm filament, nozzle, enclosure, layer height, and support limits. Choose print orientation for each unit against its main load; check access to remove supports from the tub, pilot pockets and nut features.
- Verify carrier-to-rail coupon fit and wheel alignment against the J04 locating keys before releasing either rail end; screw clearance alone is not an alignment check.
- Select exact M3 inserts, screw standards and washers for the provisional lengths above. Print pull-out and joint coupons; the Ø4.3 insert bore and 0.2 mm tongue allowance must be calibrated to the printer. Check the thin walls around the rail-end insert and the tongue under caster/skid impact loads.
- Check body-on and body-off tool access, caster pod removal, rear keel removal, downward battery exit, connector reach, and cable strain relief through a numbered assembly/service sequence.
- Print mating and insert coupons on the selected process. Revise the pilot allowance and hole/receiver dimensions from measurements. Then dry-assemble the frame and inspect alignment, racking, forced fits, damaged inserts and tool collisions.
- Assign final part IDs, add chosen hardware to the project BOM, update the build decision ledger, make per-part printable exports and rerun CAD/mesh checks before any fabrication release.

The existing `engineering-checklist.md` remains the release gate. This CAD view is a reviewable starting point for its print-split work package; it does not check off that package or claim a proven structural joint.
