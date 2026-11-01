# Chassis hardware order reconciliation — 2026-11-01

Evidence: the builder pasted the OnlyScrews order lines in this session. This
records ordered quantities. The builder subsequently reported the motors,
bearings and 1.5 mm EVA foam received on 2026-11-01. No dimensional
measurement or fit acceptance is recorded. Earlier records reported M3 inserts in hand on 2026-10-30; that
history is retained in the [project BOM](../../03-build/BOM.csv). An item absent
from this list may have been bought elsewhere; no such purchase is assumed.
Installed quantities below cover one chassis, excluding body/head allocations
and spares. Shared stock is counted once, not once per BOM ID.

## Ordered lines with chassis uses

| Ordered article | Ordered quantity | Chassis installed quantity | BOM allocation / remaining check |
|---|---:|---:|---|
| 688 ZZ, 8 × 16 × 5 mm, double metal shield | 25 | 4 | CH-015, two per side. Standard purchased bearing; no custom manufacture. Received per builder; markings, measurements and first-housing fit pending |
| M3 × 4 slant-knurled brass inserts | 35 | 20 | CH-049 rims 12 + CH-054 motor plates 8; measure OD on use |
| M3 × 6 slant-knurled brass inserts | 15 | 21 positions shared with the next line, conditionally | CH-061 rails 8 + CH-077 hatch 4 + CH-033 front crossmember 2 + CH-063 pod 3 + CH-067 rear crossmember 4 |
| Other M3 × 6 brass inserts, ₹2.80 article | 10 | No automatic allocation | Both this and the selected slant-knurled listing specify OD 4.4 × L6. The order has 25 nominally sized inserts, but only 15 of the selected article. Qualify the other article's installation/retention for at least six positions, or obtain six more selected inserts. Do not silently treat different knurls as proven equivalent |
| M3 × 6 hex-button screws | 15 | 14 | CH-030 motor faces 4 + CH-056 wheel flanges 6 + CH-076 hatch 4 |
| M3 × 8 hex-button screws | 40 | 25 | CH-031 caster 3 + CH-032 pod 2 + CH-048 wheel clamp rings 12 + CH-060 rail joints 8 |
| M3 × 16 hex-button screws | 15 | 8 | CH-053 bearing housings/caps; retain hex-button head, not the CSK line |
| M4 × 12 hex-button screws | 25 | 4 | CH-035 body feet; three into inserts, one into cassette nut |
| M3 × 12 black-oxide Phillips-CSK screws | 25 | 2 | CH-038 ballast; received head against the 90° seat |
| Ø4 × 8 hard dowel pins | 8 | 2 | CH-037 body locating pins; fit/retention check |
| M2.5 × 6 Phillips round-head laptop screws | 15 | 4 | CH-081 driver boards. Supplier lists metric 0.45 mm pitch; requires CH-080 inserts. Head/actual Phillips driver envelope still to confirm |
| N35 Ø3 × 1.5 mm magnet | 1 | 1 | CH-065; polarity/orientation and sensing calibration later |

The order also contains M2 × 4 SS304 Phillips-pan screws (₹27 / ₹1.80 implies
15; explicit quantity not shown), five M3 × 16 Phillips-CSK screws, twenty
M3 × 8 Phillips-pan screws and a storage box. These are not allocated as
substitutes for the reviewed chassis joints. Head style, length, drive and
thread type all matter. The M2 × 4 line does not establish a plastic
thread-former specification and does not match any of the direct-to-PETG
chassis screw lengths below.

## Mechanical items absent from this order

| Needed article | Installed quantity | Function / state |
|---|---:|---|
| M2 × 5 plastic thread-former, pan/rounded head | 2 | CH-039, IMU to PETG deck, Ø1.6 pilots; JCPlas B4B66 candidate pending exact sample |
| M2 × 8 plastic thread-former, 90° countersunk | 1 | CH-062, nose lid to PETG pod; JCPlas B4B67 candidate |
| M2 × 10 plastic thread-former, pan/rounded head | 1 | CH-069, TCRT bezel/shims to PETG keel; B4B66 candidate |
| M2 × 6 plastic thread-former, pan/rounded head | 1 | CH-070, replaceable shoe to keel; B4B66 candidate |
| M2.5 × 4 heat-set insert, listed OD 3.9 | 4 | CH-080, driver-board posts, Ø3.5 pilots |
| M4 × 8 heat-set insert, listed OD 5.9 | 3 | CH-095, body-foot bolts to deck, Ø5.5 × 9 pilots |
| M3 × 30 ISO 4762 socket-head screw | 4 | CH-034, keel to rear crossmember |
| M3 × 10 hex-button screw | 2 | CH-059, wheel hub caps |
| M3 × 3 cup-point set screw, shortened to 2.5 | 2 | CH-055, motor shaft to turned stub; shop operation per axle drawing/instructions |
| Plain M4 nut | 1 | CH-036, front-left body-foot cassette only |
| Loctite 222 and Loctite 641 | Shared lot | CH-057: screw locking and bearing retention are distinct uses |
| 10 mm hook-and-loop one-wrap strap, ≥150 mm, ≤1.5 mm thick | 2 | CH-078, battery pack to hatch; target about 1.2 mm thickness. Bought flexible straps, not prints; source still open |
| 1.5 mm adhesive closed-cell EVA/neoprene pads | 2 cut pads | CH-079: builder reports 1.5 mm EVA foam received; cut 36 × 17 and 13.5 × 17 mm pads, keep service window clear; adhesive backing/fit to confirm |
| 2.5 × 100 mm cable ties | 3 | CH-072 rear sensor lead 1 + CH-082 motor leads 2 |

Motors are now reported received; caster, springs, sensors, electronics and pack parts remain
in their own BOM rows. This fastener-order record does not establish their
order/receipt status.

## Why the first-part fit checks remain

The CAD uses specified nominal dimensions, not visual estimates. For example,
the selected M3 × 6 insert has a listed 4.4 mm outside diameter and fits a
designed Ø4.0 pilot: the 0.4 mm diametral difference leaves plastic to flow
around its knurls during heat installation. M3 names its internal screw
thread, not its outside body. Likewise the M2.5 × 4 insert is OD 3.9 in Ø3.5,
and the M4 × 8 insert is OD 5.9 in Ø5.5.

CAD verifies nominal walls, bore depths, screw engagement, mating and tool
paths. It cannot establish the as-printed hole diameter or installed insert
retention, which depend on the printer, material, hole compensation and heat
installation. Verify the received article once per lot/type and try it on
the first real part; no separate test coupons are required. The pod seat
establishes the M3 × 6 fit before the large modules. Its 6 mm through-seat
needs the insert flush at both faces so it does not lift the sensor or caster.
The separate non-slant article needs its own installation/retention check if
used. M2 thread-former confirmation means an actual screw intended for
thermoplastics, in the required length/head envelope, forms a retaining
thread in the Ø1.6 PETG pilot without splitting or stripping the boss.

## Metal shop work

| Part | Quantity | Shop capability / existing handoff |
|---|---:|---|
| CH-013 ballast | 1 | Mild-steel bar 9 × 60 × 19 mm, cut/machined flat and deburred, two M3 tapped holes matching J12. Basic machining/drill-and-tap work; source still open |
| CH-012 stub shaft | 2 installed; axle page suggests 1 spare | EN8/C45 precision turning, boring and tapping; bearing-seat/spigot tolerances and concentricity per [existing shop drawing](../../03-build/final/v1/fab/CH-012_stub_drawing.pdf) and [STEP](../../03-build/final/v1/fab/CH-012_stub.step). A steel stockist alone is insufficient |
| CH-052 bearing cap | 2 installed; optional spares | Flat 1.2 mm 5052-H32 or 6061-T6 aluminium, accurately cut/drilled and deburred per [DXF](../../03-build/final/v1/fab/CH-052_cap.dxf) / [STEP](../../03-build/final/v1/fab/CH-052_cap.step). Fibre laser, waterjet or suitable machining; preserve flatness |
| CH-055 set-screw finishing | 2 | Shorten the purchased M3 × 3 cup-point screw to 2.5 mm per axle instructions; retain the functional cup point and usable hex socket |

One shop can coordinate all of this if it has or subcontracts those
capabilities. No shop capability, price or manufacturing acceptance is inferred
from proximity. No fabrication orders have been placed by this session.

## Bearing source lookup (Exa, 2026-11-01)

The pasted order already contains the [OnlyScrews 688 ZZ](https://onlyscrews.in/products/688-zz-deep-groove-ball-bearing-8x16x5)
at the correct nominal size; no additional bearing order is needed for
quantity. Its manufacturer/load rating remain unspecified. These are alternate
source leads, not an automatic replacement of the selected BOM article:

| Listing | Observed price / availability text | What is actually established |
|---|---|---|
| [SantEnt NTN 688ZZ](https://store.santent.in/products/ntn-688zz) | ₹100 listed; delivery/stock to confirm | Seller identifies NTN, 8 × 16 × 5, ZZ/2Z, normal clearance; authenticity/authorised-distributor status not independently established |
| [iMakerStore 688ZZ](https://imakerstore.com/ball-bearing-688zz) | ₹43.66 incl. tax; page says in stock | 8 × 16 × 5, ABEC 1; manufacturer unspecified |
| [Moglix NBC 688ZZ](https://www.moglix.com/nbc-688zz-deep-groove-ball-bearing-8x16x5-mm/mp/msn2qntugviqel) | ₹113 incl. tax; available on request | Seller identifies NBC, 8 × 16 × 5, both sides steel-shielded; listing has inconsistent price/GST arithmetic, so obtain checkout/quote total |

These are page observations, not guaranteed stock/dispatch or audited supplier
quality. Ask for 688ZZ / 688-2Z, unflanged, 8 mm bore × 16 mm OD × 5 mm wide,
metal shields on both sides. Do not substitute 608, 698 or flanged F688.

Source checks for the screw/insert distinctions:
[JCPlas plastic thread-formers](https://www.jcfasteners.com/products/plastite-screws/),
[selected M3 × 6 slant-knurled insert](https://onlyscrews.in/products/m3-x-6mm-3d-printing-brass-threaded-inserts-dia-3mm-length-6mm),
[other M3 × 6 insert](https://onlyscrews.in/products/m3-x-6mm-brass-threaded-inserts),
[M2.5 × 4 insert](https://onlyscrews.in/products/m2-5-x-4mm-brass-threaded-inserts),
[M4 × 8 insert](https://onlyscrews.in/products/m4-x-8mm-brass-threaded-inserts),
[ordered M2.5 × 6 screw](https://onlyscrews.in/products/m2-5-x-6mm-phillips-round-head-laptop-screw).

## Builder sequencing

Hardware reconciliation and documentation cleanup happen now. Filament
selection/procurement and ASA permission wait for the lab discussion. The
builder will handle exports and slicing after this session is finalised.
Motor and bearing receiving measurements can proceed alongside early
printing. Check motor face pattern, shaft, boss and thread depth before
accepting carrier geometry; check the first printed housing against the real
bearings. A mismatch may require print or CAD correction before the full batch.
Fit, grip, retention and load tests happen after printing the relevant real
parts. Electrical commissioning is a later staged powered check, not a
prerequisite to exporting or printing passive chassis parts.
