# Filament log

One entry per filament decision, in the order the colours are tackled
([palette](../03-build/final/v1/printguide.md#4-colour-scheme)). The builder
searches and buys the spools by hand, because most palette colours are not
sold in the right material. Match colour to the neutral-light hex, not to a
screenshot.

| # | Colour | Hex (neutral light) | Status |
|---|---|---|---|
| 1 | Ivory | `#DAD5C3` | Chosen 2026-11-16, not yet ordered |
| 2 | Taupe | `#9D9886` | Decided 2026-11-16, paint only, no taupe spool: panels = white ASA painted; keel and bezel = structure PETG, primed and painted |
| 3 | Deep slate | `#34495C` | Chosen 2026-11-16: Sunlu PETG grey, 1 kg, not yet bought |
| 3a | Deep slate, head PLA | `#34495C` | Chosen 2026-11-16: eSUN ePLA-Matte dark grey, 1 kg, not yet bought |
| 4 | Slate blue | `#587A94` | Decided 2026-11-16: no spool; rims and clamp rings print in the structure grey, painting optional |
| 5 | Gunmetal | `#3A464D` | Decided 2026-11-16: no spool; hub caps print in the structure grey, painting optional |
| 6 | Amber | `#B88636` | Decided 2026-11-16: paint only, no spool; printed parts in white ASA, painted |
| 7 | Signal amber | `#D39F36` | Decided 2026-11-16: paint only, no spool; rear button bezel land |
| 8 | Carbon | `#2A2C2E` | Chosen 2026-11-16: 3Idea PLA-CF black, 1 kg, ₹1,099, not yet bought; stiffness unverified (bar test) |
| 9 | Tyre black | `#2B3034` | Decided 2026-11-16: black TPU 95A from the lab (builder: lab has it in black) |

## 1. Ivory (2026-11-16)

No ivory or cream ASA exists in the builder's market; ASA is sold in black and
white only, while PETG and PLA come in ivory. Decision: **white ASA, painted
matte ivory**, the fallback in print guide §4. PETG and PLA were rejected for
the shell: PLA softens near 55–60 °C in Mumbai heat, and PETG is satin and
heavier (1.27 against 1.07 g/cm³) and loses the matte look.

**Spool:** 3Idea ASA Filament, 1.75 mm, White, reusable spool, 1 kg
([listing](https://www.3idea.in/product-detail/3idea-asa-filament-1-75mm-white-reusable-spool-1kg-roll)).

| Listing spec | Value |
|---|---|
| Material | ASA, 1.75 mm, 1 kg net |
| Diameter tolerance | ±0.02 mm |
| Nozzle / bed | 240–260 °C / 90–110 °C |
| Nozzle | 0.4 mm brass is enough |
| Not stated | matte or satin; spool hub and width; sealed with desiccant |

Covers about 310 g of shell and head skins (221 g + 91 g, preliminary, see
print guide §3) plus arch pods and ears; one spool leaves room for reprints.

**Open before ordering:**

- **Brand approval.** [lab.md](lab.md) lists approved own-spool brands (Elegoo,
  Polymaker, Sunlu, Numakers, Brahma, eSun, Fibreel, Dream Polymers). **3Idea
  is not on the list**, so the Lab Manager has to approve it. Ask first; if
  refused, buy an approved-brand white ASA (Polymaker and eSun both make it).
- **ASA permission** on the X1E with an own spool is still unconfirmed.
- **Spool fit** in the AMS (hub hole and width are not on the listing).
- **Paint:** matte cream or ivory paint in the `#DAD5C3` family plus an
  ASA-compatible primer, tested on a printed coupon before the shell is painted.

## 2a. Taupe service panels (2026-11-16)

The front and rear service panels are separate removable parts in taupe
`#9D9886`, about 2:1 darker than the ivory shell so they read as removable.
The rear panel has the power-button well printed in it and a signal-amber
bezel land (`#D39F36`). Material is the same ASA as the shell (print guide §2).

No taupe or khaki-grey ASA exists in the builder's market (ASA is black and
white only), and black and white do not mix to taupe. Decision: **print the
panels in the same white ASA spool as the shell (entry 1), then prime and
paint them matte taupe.** No extra spool. The panel mass is already inside the
~221 g body-shell-and-panels figure.

**Paint rules:**

- Mask the mating edges, screw seats and the button well before painting;
  paint thickness can stop a removable panel from seating.
- Use a durable matte finish (a matte clear coat over the taupe), because the
  panels are handled.
- The rear signal-amber bezel land is masked and painted `#D39F36`. An AMS
  colour change would need amber ASA, which is not expected to exist.
- Test the taupe on a printed coupon against `#9D9886` under room light before
  painting a panel.

Depends on entry 1: brand approval, ASA permission and spool fit.

**Keel and bezel (decided 2026-11-16):** the rear TCRT keel (CH-008) and its sensor
bezel (CH-010) stay **PETG** and are **painted taupe with the same panel paint**, so
the rear reads as one colour. No taupe PETG spool is bought: they print from the
structure PETG spool and take primer first. Keep paint out of the bezel's optical
window and sensor cradles, and mask the mating faces; details in the
[keel README §1.3](01-chassis/keel/README.md#13-filament-and-finish-2026-11-16).

## 3. Deep slate: the structure PETG spool (2026-11-16)

Hidden structure is PETG (PLA for the head frames, which are a later entry). No
dark blue-grey PETG was found, and the colour is hidden, so a grey spool
stands in for deep slate `#34495C`: it only has to tell the parts apart.
Translucent grades were rejected (eSUN PETG+ Translucent Grey) because the nose
pod and keel hold IR sensors and must block stray light.

**Spool:** Sunlu PETG, grey, 1.75 mm, 1 kg. Sunlu is on the lab's approved
own-spool brand list. The listing gives only material, diameter, colour and a
1.3 kg shipping weight: no density, temperatures or stiffness, so treat it as
standard PETG (1.27 g/cm³, about 230–250 °C nozzle). The mass registers stay valid.

**Used for:** chassis frame modules, motor carriers, bearing housings, battery
tub and hatch, ball pod seat and lid, keel wear shoe and TCRT shims, body frame,
foot cassette, compute tray, the yaw stage. It is also the base for the **painted
taupe keel and bezel** (entry 2). Not for the wheel rims (slate blue, entry 4),
the head frames (PLA) or the yoke legs (CF).

**Quantity:** one 1 kg spool. From [lab.md](lab.md), about 420 g of finished PETG
less the slate-blue wheel parts is roughly 500 g per set with the 40–50 % overhead,
so 1 kg covers one set plus reprints. A second spool, if needed, should be the same
grey. These masses are from the older registers; print guide §8 will replace them.

**Open before use:**
- **Shade.** Confirm from the product photo or the spool that it is a dark, opaque
  grey, not light or translucent. A light grey works but will not look like the slate family.
- **Dry it** before printing (the lab dryer runs at 60 °C, 4–6 h).

## 4. Wheels (2026-11-16)

| Part | Material | Palette colour | Decision |
|---|---|---|---|
| Rims and clamp rings (CH-004) | PETG | slate blue `#587A94` | **Structure grey spool** (entry 3), left grey or painted slate blue later. No slate blue spool |
| Hub caps (CH-058) | PETG | gunmetal `#3A464D` | Same: structure grey, left grey or painted gunmetal. No gunmetal spool |
| Tyres (CH-005) | TPU 95A | black `#2B3034` | **Lab TPU 95A, black.** The builder reports the lab stocks it in black |

The wheel parts are small, so extra spools for them would be mostly waste. Paint,
if used, is optional and cosmetic; it is not needed for function.

**Open:**
- **BOM.** [Wheels README](01-chassis/wheels/README.md) lists CH-091 (own slate blue PETG)
  and CH-092 (own gunmetal PETG) as separate spools. With this decision they are not
  bought. The BOM lives in `03-build`; update it there when the builder says so.
- **Paint.** If the rims or hub caps are painted, mask the Ø74 tyre seat, the clamp face,
  the Ø10 bore and the peg holes: a paint coat changes those fits (proposed, not tried).
- **Lab TPU.** `lab.md` records a HOLD on the lab printing the tyres, and the TPU brand and
  price (₹9/g) are from the visit. Confirm the lab will print its own TPU 95A before relying on it.
  TPU prints on the A1 (direct drive), not through the AMS; dry the spool first.

## 3a. Deep slate: the head PLA spool (2026-11-16)

The head frames stay PLA, not PETG or ASA: the head FEA used PLA at about 3.5 GPa
(2.3 GPa worst case), and the pitch frame has only 30.8 Hz against a 30 Hz floor, while
PETG and ASA are about 2.0 GPa ([print guide §2](../03-build/final/v1/printguide.md#head-stiffness-limits-the-material-choice)).

**Spool:** eSUN ePLA-Matte, dark grey, 1.75 mm, 1 kg. eSUN is on the lab's approved
own-spool brand list. The listing gives only brand, grade, colour, diameter and weight.
Dark grey stands in for deep slate `#34495C`; it will read greyer than the hex.

**Used for:** head cradle, pitch frame and saddle, bearing cartridge, turntable disc
(the neck, visible), display rear frame, ear inner mounts, the ear dark centres and the
CSI guide. Not for the head skins (white ASA, entry 1) or the yoke legs (CF, entry 8).

**Quantity:** one 1 kg spool. [lab.md](lab.md) puts finished PLA at about 140 g, so about
200 g per set with the 40–50 % overhead; 1 kg leaves a large margin for reprints. These
masses are from the older hand-kept registers; print guide §8 will replace them.

**Closed 2026-11-16: the builder accepted this spool.** The items below are accepted risks,
not verified facts; they become checks at the first print.
- **Stiffness is unverified.** Matte PLAs are usually standard PLA with a matting
  additive, but no eSUN datasheet was seen. Compare any flexural modulus on the product
  page with the 2.3 GPa worst case. If there is none, treat it as unverified and check the
  first printed pitch frame for stiffness, as with the CF legs.
- **Shade.** Confirm it is a dark, opaque grey from the photo or the spool.
- **Heat.** PLA softens near 55–60 °C and creeps under screw clamps in Mumbai heat. The
  guide's fallback if creep shows at the inserts is the CF grade chosen for the legs, which
  makes these parts black and needs a mass update.
- **Dry it** before printing.

## 6 and 7. Amber and signal amber (2026-11-16)

Amber is only ever a small accent, so it needs no spool of its own. Decision: **paint**,
on white ASA for the printed parts (the spool from entry 1), not PLA. These parts sit
beside ASA skins, so they share its heat and UV resistance (PLA softens near 55-60 C),
and white is the best base for a saturated amber.

| Part | Colour | Base | How |
|---|---|---|---|
| Wheel-arch trim rings | amber `#B88636` | white ASA | Print, paint matte ochre or mustard |
| Ear inlays | amber `#B88636` | white ASA (separate solids in the CAD) | Print, paint |
| Rear power-button bezel land | signal amber `#D39F36` | taupe panel (white ASA) | Mask and paint, or an AMS colour change on the bezel layers |
| Yoke-leg spine inlays | amber `#B88636` | CF leg (black) | Paint the 0.15 mm pocket |

**Buy:** matte ochre or mustard paint (amber), a brighter safety yellow-amber (signal
amber), and a clear coat; the thin accents wear first. The bezel is a safety cue for the
red button: keep the paint durable and check it does not fade.

**Not yet checked:**
- Whether the wheel-arch trim rings are separate solids that can be printed and painted
  alone, or part of the pods (the palette lists them as body trims).
- How the 0.15 mm yoke-leg inlay is built in the CAD; the CAD comment allows a second
  printed colour or a painted pocket.
- Paint on mating or running faces changes fits; mask them.
- Depends on entry 1 (white ASA brand approval and ASA permission).

## 8. Carbon: the yoke-leg spool (2026-11-16)

The yoke legs need a carbon-fibre-filled filament ([D-049](../03-build/decisions.md#d-049)).
The builder's budget is **₹2,000 at most**, which rules out PA-CF (eSUN ePA-CF ~₹4,600,
Polymaker PA6-CF ₹7,650+) and eSUN ePLA-CF (~₹4,180). The legs use only about 30 g, so
the price is the spool, not the part.

**Spool:** 3Idea PLA-CF Premium, black, 1.75 mm, 1 kg, **₹1,099** on 3idea.in (MRP ₹3,793;
about ₹1,276 on Amazon)
([listing](https://www.3idea.in/product-detail/3idea-pla-cf-premium-3d-printing-filament-black-1-75mm-net-weight-1kg)).
Black matches the Carbon `#2A2C2E` palette colour as printed.

| Listing spec | Value |
|---|---|
| Material | PLA + carbon fibre, 1.75 mm, 1 kg; made in China |
| Finish | Matte black |
| Not stated | Stiffness (modulus), fibre content, temperatures, density, datasheet |

**Stiffness is the open risk.** D-049 asks for E ≥ 4.5 GPa along the layers, which this
grade will not reach. Other brands' datasheet bending stiffness along the layers
(Elegoo 3.34, Polymaker 3.38, Bambu 3.7–3.95, eSUN 5.0–5.4 GPa) shows that cheap PLA-CF
lands around 3.3–4 GPa. The only way it works:

- **Leg floor ~3.2 GPa, my arithmetic, not a recorded decision.** D-050's 41.9 N·m/rad leg
  floor against the leg's 46.2 N·m/rad at 3.5 GPa gives 3.5 × 41.9 / 46.2 ≈ 3.2 GPa.
  Re-checked in series with the frame (112.5 N·m/rad at 3.5 GPa), that floor reaches
  30 Hz **only with the frame at 3.5 GPa**. With the frame at the 2.3 GPa worst case the
  legs still need 4.5 GPa.
- **So the pitch frame prints from this spool too** (proposed), to take the frame off the
  2.3 GPa worst case. That makes the frame black and needs a mass-register update.
- **A new decision entry** has to lower the leg requirement before the legs are printed.

**Bar test before printing a leg (proposed):** print a 120 × 10 × 4 mm bar flat, with the
lines along its length. Rest it on two supports 100 mm apart and hang 1 kg (9.81 N) at
mid-span. E = F·L³ / (48·δ·I), with I = 10 × 4³ / 12 = 53.3 mm⁴. **Pass: mid-span sag
≤ 1.20 mm** (E ≥ 3.2 GPa); 0.85 mm would be 4.5 GPa. Measure the sag with a dial gauge or
the caliper depth rod against a fixed reference, and subtract the zero-load reading. Then
leave the load on for a day somewhere warm and check that the sag does not keep growing
(PLA creep). If it fails, the next spool is Bambu PLA-CF (₹1,799, datasheet bending
3.7–3.95 GPa).

**Open before use:**
- **Brand approval.** 3Idea is not on the lab's approved list (same question as the
  entry 1 ASA; ask both in one email).
- **Hardened nozzle.** CF wears brass; print on the X1E or the X-CF Pro.
- **Heat.** PLA-CF softens near 53–55 °C, the same risk as the PLA head frames (entry 3a).
- **Dry it** before printing (about 55 °C, 6–8 h is typical for PLA-CF).
- **BOM** and the print guide §2 CF row still say "grade not chosen"; update when the
  builder says so.
