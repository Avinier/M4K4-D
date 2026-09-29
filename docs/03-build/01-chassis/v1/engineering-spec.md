# Chassis v1 engineering specification — working brief

**Status:** draft for decisions and measurement; not a fabrication release. This brief records inherited requirements and the choices needed to turn the current assembly CAD into printable parts. New build decisions belong in [`../../decisions.md`](../../decisions.md); purchased-part status belongs in [`../../BOM.csv`](../../BOM.csv).

## Inherited design basis

| Topic | Current basis | Evidence and status |
|---|---|---|
| Construction | Modular, screw-together, serviceable | [Foundation constraint CON-P01](../../../00-foundation/constraints.md); required |
| Overall target | 300 H × 205 W × 180 D mm | [Dimensional baseline](../../../01-system/dimensional-baseline.md); rounded system target, not a part tolerance |
| Drive geometry | Two powered wheels, Ø84 mm nominal, 170 mm track, axle Z 42 mm; front 1-inch ball contact X +110 mm | [Dimensional baseline](../../../01-system/dimensional-baseline.md) and [CAD dimensions](cad/generated/dimensions.md); preserve until an explicit revision |
| Rear support | Anti-tip skid, 27 mm behind axle with 3.5 mm nominal floor gap | [Dimensional baseline](../../../01-system/dimensional-baseline.md); physical contact and stability proof open |
| Body interface | Four M4 through-bolts and two Ø4 locating pins; body shifted +16 mm relative to axle | [CAD dimensions](cad/generated/dimensions.md); hole positions modeled, joint stack and receivers open |
| Mass and stability | Whole-robot CAD estimate about 2.57 kg, CoM X +19.3 mm / Z 106.8 mm, static ball share about 18% | [Mass register](cad/generated/mass-properties.md); estimates only; verify with representative ballast and then measured assemblies |
| Drive motor | ThinkRobotics MOT3001-6V230RPM | [Build decision D-003](../../decisions.md#d-003); selected with a reduced drive envelope; received dimensions and bench performance still on hold |

The [chassis CAD README](cad/README.md) defines the v1 boundary. The [BOM](BOM.md) lists the current design parts, candidates, and release holds. RP-03 and RP-06 documents are reference inputs; `03-build/` governs new decisions.

**Fabrication access known so far:** the builder can use a 3D lab. The printer model, usable volume, nozzle, enclosure and filament inventory are still unknown. Continue part splitting and joint design using this as a constraint to check, rather than assuming a specific machine.

**First material trial, pending the lab inventory:** PETG is the structural-print candidate for the split frame, integrated plate-and-cheek motor carriers, wheel rims and caster pod; PLA can be used for inexpensive geometry/fit trials. A flexible tyre and replaceable low-friction skid shoe need separate material choices. These are trial candidates, not approved v1 materials. The structural choice requires printed joint and heat/creep evidence, especially at the carrier-to-rail keys/inserts and motor-face carrier.

## Decisions to close before printable CAD

| Order | Decision or measurement | Required output |
|---:|---|---|
| 1 | Identify the actual printer, usable build volume, nozzle, enclosure, and available filaments. Choose structural, flexible, and wear materials by part function. | Material/process schedule with a test coupon plan; no blanket material assignment from the RP-01 head PLA choice. |
| 2 | Carry sourced-part dimensions into CAD with explicit assumptions, adjustment allowances and replaceable adapters. No motor is currently on hand. | Assumption/interface register and a motor plate/coupling that can be revised without reprinting the whole frame; physical motor fit stays unverified. |
| 3 | Confirm the provisional `CH-001` split against the selected machine volume and assembly order: two deck prints (tub integral with front deck), four rail segments, two crossmembers, two integrated motor carriers and a separate hatch. | Per-part names and CAD solids, accessible fastener joints, build orientation, and removal paths. |
| 4 | Engineer the critical load paths: motor face → plate-and-cheek carrier → J04 rails; stub/bearings → wheel; caster flange → pod → front crossmember; body bolts/pins → frame; rear skid → rear crossmember. | Complete joint register with hardware, clamp stack, receiver, engagement, edge distance, tool access, and load/stiffness check. |
| 5 | Resolve the remaining custom interfaces: tyre and rim, shaft axial retention, bearing fit/preload, battery retention and hatch, touch cap, keel wear shoe and sensor guards. | Detailed mating geometry and BOM rows for every retained or replaceable item. |
| 6 | Set process-specific dimensions and verification: clearances, holes, insert bores, press/slip fits, minimum features, orientations, supports, and print settings. | Print drawings/settings and calibrated coupons for the selected printer and filament. |
| 7 | Define physical release tests before printing the scored article. | Fit/retention, loaded stiffness, wheel runout, traction/turning, braking/tip, support/skid, motor temperature, and service-access pass criteria with representative body/head mass and CoM. |

## Immediate engineering priority

The current axle design uses a 5 mm motor plate integrated with front/rear cheeks as one keyed carrier per side, separate printed housings for two 688 ZZ bearings per side (8 × 16 × 5; D-012), aluminium retaining caps, and turned Ø8 steel stubs with an M3 set screw acting on the motor D-flat. This replaces the earlier 2 mm diaphragm and 608-bearing arrangement. The selected supplier listing is currently marked sold out and does not identify the manufacturer or provide load ratings. The revised geometry still needs bearing-lot confirmation, motor fit, calibrated bearing/carrier coupons, an insert pull test, an updated clearance run and axle-rig results. Keep assumptions visible until hardware and a print process are available.

The chassis may be printed in stages for fit coupons and joint tests before the complete release. A fit coupon or bench rig must be labeled as such; it does not close the v1 print package or physical gates.

The detailed work packages, joint register, and assembly/service gates are in the [mechanical engineering checklist](engineering-checklist.md). Start with its wheel-to-chassis work package and carry its outputs into the frame split.
