# Frame print-split study

**Status:** frame print units after D-033, not a fabrication release. Open `frame-split.step` in CAD Viewer. `frame-split.step.py` is the editable source. This view calls the same frame print-unit geometry as the main `chassis-v1.step.py` assembly.

The view keeps the chassis coordinate system: origin at the axle line on the floor, +X forward, +Y robot-left, +Z up. The gray motor barrels and green battery block are **reference envelopes**, not print units. They show why the top deck has a motor relief and battery aperture. This frame-only view leaves the rail ends visible; the integrated J04 carriers are defined in the main chassis CAD and [axle-stack §9](../../axle-stack.md#9-j04-carrier-and-test-plan). J04 print fit and strength proof are still open.

## Print units (D-033)

| Part label | Quantity | Current extent / purpose |
|---|---:|---|
| `FS_FRAME_FRONT_MODULE` | 1 | One print: front deck, battery tub walls and hatch bosses, both front rails, front crossmember, driver posts and the D-032 fuse bracket. X +17 to +92. |
| `FS_FRAME_REAR_MODULE` | 1 | One print: rear deck, both rear rails and the rear skid crossmember with the keel inserts and cable-tie lug. X −51 to −17. |
| `FS_BATTERY_HATCH_FOUR_M3` | 1 | Separate downward-removable hatch with four M3 clearance holes; carries the strapped pack. |

The two modules join only through the two removable J04 carriers in the main chassis CAD, so the frame is **five prints** (two modules, two carriers, the hatch), down from eleven. [D-033](../../../../decisions.md#d-033) fused each end after the fastener review found no service or printer reason for the old split: the rails and crossmembers had been kept separate only so their joints could be reviewed. The fusion removes J05, J06 and J16: ten M3 screws and ten inserts. It also removes the rear deck's two detached screw pads, which sat 1 mm off the deck plate, so the old rear J16 screws clamped nothing to the deck.

Where the deck covers a crossmember, the crossmember now rises to the deck underside: the front one from Z 51 to 52, the rear one from Z 48 to 52 under the deck (X −41 to −32). Deck and crossmember are continuous, and the rear module prints deck-down without a floating crossmember.

## Interfaces that remain

1. **Carrier boundary (J04).** The rail ends stop at X ±17 and take the keyed carriers: two M3 × 8 per end into 6 mm inserts in the rail ends. The carriers stay removable because the motor face pattern is unmeasured ([D-007](../../../../decisions.md#d-007)).
2. **Body M4 receiver access (J13).** The rails keep open vertical socket paths at the four body bolt positions (Y ±48), with a local outside rib. The nut bears on the deck underside.
3. **Battery hatch (J11).** Four bosses are integral with the front module. Four M3 × 6 button heads go through the 1.5 mm hatch into M3 × 6 inserts. The pack is strapped to the hatch and drops out with it.
4. **Nose pod, keel, ballast, IMU and drivers** keep their own joints (J07B, J09A, J12, J15A, J15B).

## Hardware schedule

| Joint | Screw | Receiver | Qty |
|---|---|---|---:|
| J04 carriers to modules | CH-060 ISO 7380 M3 × 8 | CH-061 M3 × 6 insert in the rail ends | 8 |
| J11A battery hatch | CH-076 ISO 7380 M3 × 6, driven from below | CH-077 insert pressed up into each tub boss | 4 |

D-030's J05 (CH-073), J06 (CH-074) and J16 (CH-075) screws and their ten CH-077 inserts are deleted by D-033.

## Assembly and service order

1. Print the two modules, two carriers, the hatch and the fit coupons. Install the eight J04 inserts in the rail ends, the four hatch-boss inserts, the four driver-post inserts, the two pod inserts in the front crossmember and the four keel inserts in the rear crossmember.
2. Fit each carrier's keys into the front and rear rail ends and drive its four J04 screws. Check that the two modules' deck tops are coplanar across the motor bay.
3. Install the rear keel and the front caster pod from their own joint work packages.
4. Fit the pack strapped to the hatch, connect through the +Y window, and close the hatch from below with four screws.
5. Place the body on its two pins. Fit the four M4 bolts from above and hold each nut from below through the rail socket path.

## Work required before printable parts

- Measure the lab printer's usable build volume (the front module is about 75 × 128 × 41 mm with the fuse bracket, the rear about 34 × 132 × 22 mm) and confirm filament, nozzle, enclosure, layer height, and support limits. Choose print orientation for each unit against its main load; check access to remove supports from the tub, pilot pockets and nut features.
- Verify carrier-to-rail coupon fit and wheel alignment against the J04 locating keys before releasing either rail end; screw clearance alone is not an alignment check.
- Select exact M3 inserts, screw standards and washers for the provisional lengths above. Print pull-out and joint coupons; the Ø4.3 insert bore and the 0.2 mm J04 key allowance must be calibrated to the printer. Check the module junctions (rail to crossmember, crossmember to deck) under caster/skid impact loads.
- Check body-on and body-off tool access, caster pod removal, rear keel removal, downward battery exit, connector reach, and cable strain relief through a numbered assembly/service sequence.
- Print mating and insert coupons on the selected process. Revise the pilot allowance and hole/receiver dimensions from measurements. Then dry-assemble the frame and inspect alignment, racking, forced fits, damaged inserts and tool collisions.
- Assign final part IDs, add chosen hardware to the project BOM, update the build decision ledger, make per-part printable exports and rerun CAD/mesh checks before any fabrication release.

The existing `engineering-checklist.md` remains the release gate. This CAD view is a reviewable starting point for its print-split work package; it does not check off that package or claim a proven structural joint.
