# 04-cnc — Makad's machined and cut parts

Eight parts on Makad are not printed. They are turned, milled, ground, EDM or laser cut. This
folder is the order pack for them: what each part is, which shop route suits it, the
files to upload and the text for each quote form ([RFQ.md](RFQ.md)). It follows the
[04-print rules](../README.md#rules). **No geometry is edited here.** Every file in
`upload/` is a copy of `03-build/final/v1/fab/`, which is generated from the final droid
geometry.

| Path | What it holds |
|---|---|
| [RFQ.md](RFQ.md) | Paste-ready quote text per part: material, quantity, finish, fits and threads |
| `upload/<part>/` | STEP + drawing PDF per part (and the DXF for CH-052 and BO-046), copied from `fab/` |
| `upload/makad-cnc-pack-revA.zip` | All eight parts in one zip, for platforms that take a single upload |
| `upload/manifest.json` | SHA-256 of every file; `package_cnc.py --check` compares it with `fab/` |

## 1. The parts

| Part | What it does | Process | Material | Qty | Stock | Critical features | Mass |
|---|---|---|---|---|---|---|---|
| **CH-012** axle stub | Drive axle: carries two 688 bearings, takes the motor D-shaft, centres the wheel | CNC turning | EN8 / C45 | 3 (2 + spare) | Shop | Ø8 **k5** seats, Ø10 **g6** spigot, Ø4.05 **H8** bore, one-setup concentricity 0.02, 5 × M3 | ~13 g |
| **HD-004** roll hub collar | Couples the Probots 25T roll horn to the roll spindle (D-120) | CNC turning | 6061-T6 / 6082-T6 | 2 (1 + spare) | Shop | Ø6 **H7** bore, face square 0.02, 4 × M2 on Ø14 PCD, 2 × radial M3 | 4.8 g |
| **CH-052** bearing cap | Holds the 688 outer rings in the housing | Fibre laser or waterjet | 1.2 mm 5052-H32 / 6061-T6 | 3 (2 + spare) | Shop | DXF profile; flat 0.1; deburred bore | ~2 g |
| **CH-013** ballast bar | Tipping ballast under the deck (D-026; copper per D-109) | CNC milling | C110 / ETP copper | 1 | **Builder has a ~10 × 20 offcut** (or shop C110) | 9 × 60 × 19, 2 × M3 × 8 at 40 ± 0.1, top face flat 0.1, **mass ~90.8 g** | 90.8 g |
| **BO-047** yaw pinion shaft | Carries the scissor pinion on the yaw servo hub (D-044) | Cut to length | 5 mm ground D-shaft | 2 (1 + spare) | **Builder ordered** (dc3d 4 × 60 mm) | Ø5 h6 and flat as stock, 17.4 ± 0.1, no holes (D-125) | 2.5 g |
| **BO-046 fixed half** | Upper scissor-pinion half, keyed on BO-047's flat, carries the preload (D-125) | Wire EDM (or fibre laser) | 2 mm 7075-T6 (6061-T6 ok) | 2 (1 + spare) | Shop | DXF profile, m1 z37, span over 5 teeth 13.732 −0.03; Ø5 H7 bore with 4.55 +0.03 flat; Ø2 H7 peg hole at R10 | 5.8 g |
| **HD-009** pitch pivot pin | Passive pitch pivot through the MR106 bearing (D-051) | Cut + surface grind | Ø6 h6 hardened EN-31 rod | 2 (1 + spare) | **Builder ordered** (Robocraze 200 mm) | 11.5 ± 0.05, flat 5.5 +0/−0.05 full length | 2.4 g |
| **HD-034** roll spindle | Roll axis shaft in two 696 bearings (M016; D-053, D-120) | Cut + surface grind | Ø6 h6 hardened EN-31 rod | 2 (1 + spare) | **Builder ordered** (same rod as HD-009) | 44.4 ± 0.1, two flats 5.5 +0/−0.05 at 90° ± 2°, journals unmarked | 9.7 g |

One 200 mm Ø6 rod covers both HD-034 (2 × 44.4) and both HD-009 (2 × 11.5): 112 mm
plus four cuts. One 60 mm D-shaft gives both BO-047.

## 2. Two routes

The parts split by who supplies the material.

**A. Online CNC platform, the shop supplies the material.** CH-012, HD-004, CH-052 and
the BO-046 fixed half (ask for wire EDM; fibre laser if not) can go on one order, and CH-013 too if the platform stocks C110 copper (the
[platform survey](#4-platforms) has Xometry and BRHTC listing copper). Upload the STEP
and the PDF for each part. The PDF is not optional: CH-012 and HD-004 have ISO 286 fits
(k5, g6, H8, H7) and tapped holes that the instant price does not include. Without the
drawing the shop works to ISO 2768-m (about ±0.1 mm) and the bearings will not fit. With
a drawing, the order goes to an engineer for a manual quote, usually within hours to a day.

**B. Local machinist or tool room, the builder supplies the stock.** BO-047, HD-009 and
HD-034 are cut from the rod and D-shaft already ordered, and CH-013 from the copper
offcut. Online platforms do not take customer-supplied material. Take the PDFs and
the stock to a tool room with an abrasive cut-off saw, a surface grinder with a V-block
(for the 0.5 mm flats) and a drill press. This is small work: about six cuts, three
ground flats, and milling plus two tapped holes on the copper bar.

- **HD-009 and HD-034 are hardened EN-31 (~60 HRC).** They are cut with an abrasive
  disc and the flats are ground, not milled. They cannot be drilled or tapped, so HD-009
  has **no M2 extraction hole** (the BOM listed it as optional). The Ø6 is used as
  supplied (h6/g6); nobody turns or polishes it.
- **BO-047 is only cut to length** since D-125 (no tap): the stock's own flat
  (4.45–4.55 across) is the part's flat, full length.
- If route B is not available, a platform can make BO-047, HD-009 and HD-034 from its
  own EN8/C45 ground to h6. The drawings allow it ("OR EN8/C45 GROUND h6"); the cost
  goes up because each part then needs grinding.

## 3. How to order (route A)

1. Upload `upload/<part>/<part>.step` per part (or the zip). For CH-052 the DXF is the
   cut file; add the STEP for the thickness.
2. Material, quantity and finish from §1. Finish: as machined, no plating, light oil on
   the steel.
3. Attach `<part>_drawing.pdf` to every part, and paste that part's block from
   [RFQ.md](RFQ.md) into the notes box.
4. Ask for a manual quote. Confirm before paying: k5/g6/H8/H7 accepted, 1.2 mm
   aluminium in stock for CH-052 (1.0–1.5 acceptable), copper grade if CH-013 is
   included.
5. Pay (prices in ₹ + 18 % GST). Lead time is typically 3–10 days.
6. On receipt, measure as in §5 before assembly.

Send the same pack to two or three platforms and compare quotes.

## 4. Platforms

From the 2026-11-21 survey (prices not yet quoted):

| Platform | CNC turning | Laser Al | Copper | Notes |
|---|---|---|---|---|
| Xometry India | ✓ | ✓ | ✓ | Global; ISO 286 grade 6/7 fits offered; 7–10 days |
| Partwork | ✓ | ✓ | ✓ | Pune/Bengaluru/Chennai/Delhi hubs; ±0.01 possible; QC report; 3–15 days |
| BRHTC | ✓ | — | ✓ C110 | Hosur; student/Robocon-friendly; quote in ~6 h |
| Fyord / MechHub | ✓ | ✓ | — | Drawing + engineer review; MechHub's sheet list starts at 1 mm |
| MakeItNow / TruSkew | ✓ | ✓ | — | Newer sites; 4–7 days |

## 5. Receiving checks

| Part | Measure | Accept |
|---|---|---|
| CH-012 | Ø8 seats, Ø10 spigot (micrometer); Ø4.05 bore on the motor shaft; a 688 on the seat (dry trial) | 8.001–8.007; 9.986–9.995; slides onto the Ø4 shaft; the 688 needs a light push (assembly uses Loctite 641, axle page §9) |
| HD-004 | Bore on the spindle; M2 holes against the received horn | Slides on with no rock; four M2 × 6 start by hand through the horn |
| CH-052 | Thickness; holes on the housing | 1.0–1.5 mm; four M3 × 16 pass |
| CH-013 | **Weigh**; M3 × 12 CSK through the deck holes into both taps | Within ±2 g of 90.8 g; record the mass in the chassis log |
| BO-047 | Length; across the flat | 17.3–17.5; 4.45–4.55 |
| BO-046 fixed half | Span over 5 teeth (disc micrometer); bore on BO-047; peg hole on a Ø2 dowel | 13.70–13.73; slides on with no rock, flat keys it; dowel presses in |
| HD-009 | Length; across the flat; slide through an MR106 | 11.45–11.55; 5.45–5.50; through by hand or a light push |
| HD-034 | Length; both flats and their angle; through two 696 and the HD-004 bore | 44.3–44.5; 5.45–5.50; front flat 9.8–10.1, rear 8.3–8.9; rear flat at 9 o'clock seen from the rear |

## 6. Where the files come from

All in [`03-build/final/v1/cad/`](../../03-build/final/v1/cad/); run with the legacy CAD
runtime (see [final/v1 README](../../03-build/final/v1/README.md)).

| Script | Writes |
|---|---|
| `export_axle_fab.py` | CH-012 STEP, CH-052 STEP + DXF (D-071) |
| `stub_drawing.py` | CH-012 drawing |
| `export_d120_fab.py`, `d120_collar_drawing.py` | HD-004 STEP and drawing (D-120) |
| `export_cnc_fab.py` | CH-013, BO-046 fixed half (+ DXF), BO-047, HD-009, HD-034 STEPs and `fab/cnc-facts.json`, from the same constants as the droid geometry |
| `cnc_drawings.py` | CH-013, BO-046, BO-047, HD-009, HD-034 and CH-052 drawings (cadgen 0.6.6 drawing module) |
| `check_cnc_fab.py` | Compares every part with the droid geometry (symmetric difference < 0.01 mm³), checks the STEPs are current and the pack complete, and checks the spindle flats, journals and screw positions: **14/14 on 2026-11-21**. `check_d125_pinion_dbore.py` checks the BO-046 half and peg in the droid: **10/10** |
| `package_cnc.py` | This folder's `upload/`, zip and manifest; `--check` finds stale copies |

After any change to one of these parts: re-run its exporter and drawing,
`check_cnc_fab.py`, then `package_cnc.py`.

## 7. Points found while making the pack ([D-125](../../03-build/decisions.md#d-125))

1. **BO-047 / BO-046 key: closed.** A 2 mm PETG fixed half would see 49–73 MPa on its
   D-key under the preload alone (`E`), so (builder, 2026-11-21) the fixed half is
   aluminium, on BO-047's full-length flat with Loctite 641. The D-044 M2 screw never
   held the half (its head sat on the shaft end), so it and BO-047's tap are dropped.
   The pre-wind peg (BO-072, a Ø2 × 4 dowel) and the sprung half's arc slot are now in
   the droid. Copper tipping margin 4.35 → 4.27 %.
2. **Spindle flat lengths — closed.** BOM.csv HD-034 and the head BOM now state
   9.8 (+0.3/−0) and 8.6 (±0.3), as modelled and drawn.
3. **HD-009 has no extraction thread — closed.** BOM.csv HD-009 says so. To remove the
   pin, push it out from the boss side, or pull it with a magnet once the retainer is off.
4. **CH-013 mass.** Copper at 8.94 g/cm³ gives 90.8 g (the droid's Ø3 holes give
   90.6 g). Brass or steel would cut the tipping margin (D-109: steel 2.79 %, copper
   4.36 %), so the drawing forbids substitution. Weigh it on receipt.

## 8. Quotes and orders

| Date | Platform / shop | Parts | Quote (₹ incl. GST) | Lead time | Status |
|---|---|---|---|---|---|
| | | | | | |
