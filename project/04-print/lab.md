# The print lab

The ISDI rapid-prototyping lab, Atlas SkillTech University, Mumbai. Visited
2026-10-28: the rules and rates come from the lab poster, the machines from
photos of their labels. Requests go to `rapidprototyping@atlasuniversity.edu.in`.

This file owns everything about **where and how** Makad is printed: the rules,
the machines, the rates and the open permissions. What each part is made of,
and its colour, stays in the [print guide](../03-build/final/v1/printguide.md).

## Rules (lab poster)

| Item | What the poster says | What it means for Makad |
|---|---|---|
| Build volume | 250 × 250 × 250 mm maximum; larger parts must be split | Every part fits. The largest, the body shell, is 162 × 182 × 110 mm |
| Wall thickness | 1.2 mm preferred minimum | Two printed parts are thinner: the head pivot retainer (1.0 mm, D-051) and the keel's TCRT height shims (1 mm, D-014). Ask whether they will print them |
| Files | STL, STEP or OBJ; watertight, no non-manifold edges; own designs only | Export a per-part STL or STEP |
| Requests | Email with the purpose, dimensions, material and print type; academic prints CC a faculty member; submit at least 4 days ahead | Plan print batches a week out |
| Printing | Slicing is done at the lab. A print starts only with the Lab Manager present. The student stays for the first 5 layers and leaves an ID card | Each plate costs a supervised start, so group parts into few plates |
| Drying | A heated dryer at 60 °C that holds 4 spools; drying 4–6 h before printing | Covers PETG, TPU and nylon drying |
| Lab filament | PLA ₹5.5/g, special PLA ₹6–10/g, PETG ₹6/g, ABS ₹8/g, TPU ₹9/g | TPU is offered, so the tyres (D-005) are likely printable. ABS is offered, so an enclosed printer probably exists. **No ASA or CF is listed** |
| Own filament | Academic prints are free with your own filament. Approved brands: Elegoo, Polymaker, Sunlu, Numakers, Brahma, eSun, Fibreel, Dream Polymers; others need the Lab Manager's approval | ASA and PA-CF have to be your own spools, from an approved brand (Polymaker and eSun make both). Damage to the printers is the student's responsibility, which matters for abrasive CF |

## Machines

Read from the printer labels. "Label" means the lab's own sticker; the rest is
the maker's specification.

| Machine | Count seen | Volume | Label materials | What it is for in Makad |
|---|---|---|---|---|
| **Bambu Lab X1E with AMS** | 1 | 256 × 256 × 256 mm | PETG, PLA, ABS, TPU, nylon | **The key machine.** Enclosed, heated chamber, built-in fume filter, hardened-steel nozzle, 4-spool AMS. The ASA skins (body shell included), two-tone parts (ears, rear panel), and possibly the PA-CF yoke legs |
| **QIDI X-CF Pro** | 1 | about 300 × 250 × 300 mm | (label not legible) | A printer built for carbon-fibre nylon: enclosed, hardened nozzle. **The first choice for the PA-CF yoke legs (D-049)** |
| Flashforge Guider II | 2 | 300 × 300 × 300 mm (label) | TPU, PLA, ABS, PETG | Enclosed, large. PETG frames; a backup for ABS or ASA |
| Bambu Lab A1, some with AMS Lite | several | 256 × 256 × 256 mm | — | Open frame, direct drive, textured PEI plates seen. PETG and PLA parts; **TPU tyres (D-005)** |
| Bambu Lab A1 mini | 2 | 180 × 180 × 180 mm | — | Small parts only; the shell does not fit |
| Enclosed Bambu (model not confirmed), Creality enclosed printer, small Flashforge | 1 each | — | — | Spare capacity |
| Vacuum-forming machine | 1 | sheet frame about 400 mm | — | Not a printer. Could form a clear display window (M003) over a printed buck |

This confirms the print guide's pre-visit assumptions: an enclosed, filtered printer exists for
ASA; there is CF-capable kit; TPU has a direct-drive printer; textured PEI plates
are in use. Who may use the X1E and the X-CF Pro, and with which filaments, is
still to ask.

## Cost

Finished printed mass, from the CAD mass registers: about 360 g ASA, 420 g PETG,
140 g PLA, 30 g PA-CF and 40 g TPU, about **1.0 kg** in all. Supports, brims,
AMS purge and failed prints add about 40–50 %, and test coupons about 200 g, so
one complete set uses about **1.6 kg** of filament. The [print guide §8](../03-build/final/v1/printguide.md)
replaces these masses with per-part figures.

| Route | Estimate | Notes |
|---|---|---|
| A. All lab filament (ABS in place of ASA, no CF) | about ₹10,000 | Lab colours only; the yoke legs cannot be made |
| B. Lab PETG, PLA and TPU, plus own ASA and PA-CF spools | about ₹5,500 lab + ₹9,000–11,000 spools ≈ ₹15,000 | Lab colours may not match the [palette](../03-build/final/v1/printguide.md#4-colour-scheme) |
| **C. All own filament, as an academic project (recommended)** | ₹0 printing + ₹13,000–16,000 spools | Needs a faculty member CC'd. Matches the palette; the leftover spools cover reprints |
| Paint (primer, matte colours, clear coat, wash) | + ₹2,000–3,000 | Any route |

Spool prices are estimates from Indian retail, not quotes. Plan for 1.5–2 sets
of prints in total: the yaw gears, tight fits and the CF leg will need reprints.

## Answered on the 2026-10-28 visit

- **TPU 95A:** offered as lab filament (₹9/g), and the Bambu A1 printers are
  direct drive. The tyre hold on [D-005](../03-build/decisions.md#d-005) can lift
  after one test tyre prints and fits; until then the O-ring fallback stands.
- **CF for the yoke legs ([D-049](../03-build/decisions.md#d-049)):** the lab has a
  QIDI X-CF Pro (built for CF nylon) and an X1E (hardened nozzle). No CF
  filament is stocked; bring an approved-brand PA-CF (Polymaker or eSun). The
  ≥ 4.5 GPa coupon is still to be printed and tested.
- **Largest bed:** 300 × 300 × 300 mm (Flashforge Guider II); the poster caps
  parts at 250 mm. The shell (162 × 182 × 110 mm) fits every machine except the
  A1 mini.
- **ASA:** the X1E is enclosed with a heated chamber and a fume filter, and ABS
  is a lab filament, so ASA is physically possible. Permission is still to
  confirm (below).
- **Textured PEI:** seen on the A1 printers.
- **Drying:** a 60 °C four-spool dryer; the poster asks for 4–6 h before printing.
- **Two-tone parts:** the X1E has a 4-spool AMS; several A1s have AMS Lite.

## Still open

Ask by email or on the next visit; record the answer here with its date.

- **ASA on the X1E with an own spool:** is the X1E open to students, and is ASA
  allowed?
- **PA-CF on the X-CF Pro:** allowed, given that printer damage is the
  student's responsibility?
- **Slicer:** Bambu Studio or Orca? Makad hands over raw STLs with the settings
  written on each part card, so ask whether the lab can paint fuzzy skin onto
  chosen faces and split colours for the AMS at slicing time.
- **Walls under 1.2 mm:** the head pivot retainer (1.0 mm) and the keel TCRT
  shims (1 mm). Will the lab print them, or do they thicken?
- **Academic status:** which faculty member to CC so own-filament prints are free.
- Filament colours in stock, by brand and material, against the [palette](../03-build/final/v1/printguide.md#4-colour-scheme): ivory or white **ASA** and a warm taupe or khaki-grey **ASA**, matte amber or ochre, a very dark blue-grey (deep slate) in **PETG** and **PLA**, a lighter blue-grey (slate blue) **PETG** for the wheels, taupe **PETG** for the keel, matte gunmetal, black TPU 95A. Take photos next to a printed colour card. Screen hex values are only a guide. Numakers and Polymaker spools were seen on the shelves.
- Heat-set insert tip, a spray area for primer and paint, and use of the
  vacuum former (a possible clear display window, M003).
- Whether any lab on campus has a UTM for the CF modulus coupon.
