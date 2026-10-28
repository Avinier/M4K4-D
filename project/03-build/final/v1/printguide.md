# Makad v1 — print guide

What every printed part of Makad v1 is made of, what colour and finish it has,
and what it weighs. The goal is a finished, realistic CAD: each printed part
in `makad-v1-presentation.step.py` should carry its real filament colour, and
the mass registers should use the real material and fill. Slicer settings and
shop-floor steps come later.

It covers the printed parts of [chassis v1](../../01-chassis/v1/BOM.md),
[body v1](../../02-body/v1/BOM.md) and [head v1](../../03-head/v1/BOM.md).

**Status:** draft, being written one section at a time. The lab was visited on
2026-10-28: the ISDI rapid-prototyping lab at Atlas SkillTech University
([§1](#1-the-lab)). Its machines, rules and rates are recorded; a few
permissions and the stock colours are still open
([§9](#9-lab-visit-checklist)).

The BOM and [decisions](../../decisions.md) stay the authority for part
geometry and material decisions. This guide collects them in one place. Where
it proposes something the decisions do not yet record, it says **proposed**.

## Contents

1. [The lab](#1-the-lab)
2. [Material palette](#2-material-palette)
3. [Finish and texture](#3-finish-and-texture)
4. [Colour scheme](#4-colour-scheme)
5. Chassis parts: material, colour, finish, mass — *next*
6. Body parts: material, colour, finish, mass — *to do*
7. Head parts: material, colour, finish, mass — *to do*
8. Mass roll-up against the registers — *to do*
9. [Lab-visit checklist](#9-lab-visit-checklist) — *visited; a few items open*

## 1. The lab

The ISDI rapid-prototyping lab, Atlas SkillTech University, Mumbai, visited
2026-10-28. The rules and rates come from the lab poster, the machines from
photos of their labels.

### Confirmed from the lab poster (2026-10-28)

The lab is the ISDI rapid-prototyping lab at Atlas SkillTech University. Requests
go to `rapidprototyping@atlasuniversity.edu.in`. The poster lists FDM printing
and a separate resin area.

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

### Machines seen in the lab (photos, 2026-10-28)

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

This answers most of §1's assumptions: an enclosed, filtered printer exists for
ASA; there is CF-capable kit; TPU has a direct-drive printer; textured PEI plates
are in use. Who may use the X1E and the X-CF Pro, and with which filaments, is
still to ask.

### Printing cost estimate (2026-10-28)

Finished printed mass, from the CAD mass registers: about 360 g ASA, 420 g PETG,
140 g PLA, 30 g PA-CF and 40 g TPU, about **1.0 kg** in all. Supports, brims,
AMS purge and failed prints add about 40–50 %, and test coupons about 200 g, so
one complete set uses about **1.6 kg** of filament. Section 8 replaces these
masses with per-part figures.

| Route | Estimate | Notes |
|---|---|---|
| A. All lab filament (ABS in place of ASA, no CF) | about ₹10,000 | Lab colours only; the yoke legs cannot be made |
| B. Lab PETG, PLA and TPU, plus own ASA and PA-CF spools | about ₹5,500 lab + ₹9,000–11,000 spools ≈ ₹15,000 | Lab colours may not match §4 |
| **C. All own filament, as an academic project (recommended)** | ₹0 printing + ₹13,000–16,000 spools | Needs a faculty member CC'd. Matches the §4 palette; the leftover spools cover reprints |
| Paint (primer, matte colours, clear coat, wash) | + ₹2,000–3,000 | Any route |

Spool prices are estimates from Indian retail, not quotes. Plan for 1.5–2 sets
of prints in total: the yaw gears, tight fits and the CF leg will need reprints.

### Pre-visit assumptions (superseded)

Written before the visit; kept so the reasoning behind the material picks stays
visible. Where the visit differs:

- There is no SLS/MJF powder printer or resin printer on record; the poster
  shows a resin area but no machine was photographed. PA12 gears remain an
  outsourcing item.
- The large-format row is met by the two Flashforge Guider II (300 mm).

| Kit | Assumed model class | What it decides for Makad | Confidence |
|---|---|---|---|
| Enclosed CoreXY FDM, multi-material | Bambu Lab X1C / P1S with AMS; 256 × 256 × 256 mm; a hardened-steel nozzle on at least one machine; textured PEI plates | Nearly every part. The enclosure allows ASA, the hardened nozzle allows CF filament, the AMS allows two-tone parts, the textured plate gives the grain in §3 | High |
| Open-frame FDM, direct drive | Prusa MK4 / Creality class | TPU 95A tyres (TPU does not run through an AMS) | High |
| Large-format FDM | Creality K1 Max / Ultimaker S5 class, ~300 mm bed | Spare room for the body shell if a 256 mm bed is tight | Medium |
| Resin SLA | Formlabs Form 3+ / Form 4 | Optional: small cosmetic head parts. Not planned for structure | Medium |
| Powder bed (SLS / MJF nylon) | Formlabs Fuse 1, or outsourced | Fallback for the yaw gears if PETG fails (D-044 names PA12 as the next step) | Low in-house; outsource from a Mumbai service bureau |
| Filament dryer | Dryer box or oven, 50–70 °C | PETG, TPU and CF-nylon all absorb water quickly in Mumbai humidity | Medium; buy one if missing |

**Mumbai conditions that drive the material choices:**

- **Humidity.** Relative humidity sits around 70–90 % in the monsoon. Wet
  PETG strings, wet TPU foams, and wet nylon or CF-nylon loses much of its
  stiffness. Dry them before printing and store them sealed.
- **Heat.** Room temperature is 30–35 °C most of the year, and a closed room
  or a parked car goes well above that. PLA softens near 55–60 °C and creeps
  under screw clamps well below that. This is why the chassis and body
  structure are PETG, and part of why the skins move to ASA (§3).
- **Supply.** PLA, PETG, TPU 95A, ASA and PLA-CF / PETG-CF are easy to buy in
  India (Robu, Bambu India, eSun, Solidspace and similar). PA-CF is harder to
  find but Polymaker and eSun sell it, and the lab can print it (§1). PA12
  powder parts still need a service bureau.

## 2. Material palette

Six materials cover the robot. PETG, TPU, PLA and CF filament are already in
the decisions or the mass registers. ASA is proposed for the visible skins (§3).
Resin is optional.

| Material | Density, solid (g/cm³) | Look as printed | Heat (softens near) | Stiffness (GPa) | Used for | Status |
|---|---|---|---|---|---|---|
| **ASA** | 1.07 | Naturally dead matte; UV-stable; takes primer and paint well | ~95 °C | ~2.0 | Every visible skin: body shell and panels, head skins and covers, ear caps | **Proposed** (§3); body BOM records PETG today |
| **PETG** | 1.27 | Satin to gloss; layer lines visible; paint needs a primer | ~75 °C | ~2.0 | Hidden or working parts: chassis frame, wheel rims, keel parts, body frame, compute tray, the whole yaw stage | Recorded (D-017, D-033, D-044, body BOM) |
| **TPU 95A** | 1.21 | Soft semi-matte rubber; reads as a real tyre | ~80 °C | — (flexible) | Tyres | Recorded (D-005); HOLD on the lab printing it |
| **PLA** | 1.24 | Matte grades available; hides layer lines well | ~55 °C | ~3.5 (2.3 worst case) | Head frames, cradle and turntable disc (the parts the head FEA is based on) | Recorded in the head mass tree |
| **CF-filled filament** | ~1.15–1.30, grade dependent | Matte, slightly textured; **black or dark grey only** for the stiff grades | Grade dependent: PLA-CF ~55 °C, PA-CF ~100 °C+ | Must be ≥ 4.5 along the layers | Head yoke legs | Recorded (D-049); grade not chosen, coupon open |
| **Resin (tough / standard)** | ~1.15–1.20 | Smooth, no layer lines | ~50–60 °C (standard) | — | Small cosmetic head details only | Optional |

### What this means for the CAD

- **Weight.** The three registers use three different bases today. The head
  uses solid PLA at 1.24 g/cm³ with no infill. The body shell and frame use
  PETG at a "near-solid" 1.20. The chassis keel and wheel-arch pods use an
  effective 0.571 for infill. Section 8 puts every part on one basis: solid
  density × an estimated fill fraction from its wall count and infill.
- **Looks fixed by the material:**
  - The **yoke legs are black or charcoal** if they are CF. The CAD paints them
    slate blue (`#536B78`).
  - The **tyres are black TPU**. The CAD already shows them as rubber.

### Head stiffness limits the material choice

The head's frames cannot simply move from PLA to PETG or ASA. Both are about
2.0 GPa, below the 2.3 GPa worst case the D-049 and D-050 FEA used for the
pitch frame (30.8 Hz against a 30 Hz floor). So the head splits:

- **Skins** (bezel and camera crown, octagonal skin halves, rear cover, ear
  caps) carry no structural load. They move to ASA to match the body.
- **Frames** (cradle, pitch frame and saddle, bearing cartridge, turntable disc)
  stay PLA, the FEA basis. If heat creep shows up at inserts, the fallback is the
  CF grade chosen for the legs. That makes these parts black and needs a mass
  update.

## 3. Finish and texture

[Vision](../../../00-foundation/vision.md#character-and-visual-direction) asks
for a Star Wars droid that looks "rugged, used, and characterful rather than
glossy and appliance-like", with screws, panels and seams left visible. In
print terms, nothing on the outside should shine. Every visible surface gets
one of two textures:

- **Housing grain:** the fine matte grain of a TV remote or a power tool. Used
  on the skins.
- **Metal casing:** a bead-blasted or anodised aluminium look, the matte
  metal of an electronics enclosure. Used on accent and mechanical parts.

### How each texture is made

| Texture | Reads like | Made by | Notes |
|---|---|---|---|
| **Housing grain** | TV remote, power-tool housing | Matte ASA, plus two print-side effects: (1) the **textured PEI plate** stamps a powder-coat grain on the face printed down; (2) **fuzzy skin** on the outer walls gives a fine sand-cast grain on the rest | Fuzzy skin must stay off mating faces, seams, insert bosses and the mic and grille openings: it adds about 0.1–0.2 mm of jitter. ASA must **not** be acetone-smoothed; that makes it glossy |
| **Metal casing** | Dark blue anodised or bead-blasted aluminium | Either a **matte metallic-pigment filament** in a dark blue-grey, or **paint**: filler primer, light sanding, matte metallic deep slate (gunmetal for the hub caps), then a matte clear coat | Paint is more convincing; filament is faster and doesn't chip. CF parts are left raw: CF's own matte texture already reads as dark anodised or machined composite |
| **Accent** | Painted trim on a worn machine | Matte amber filament | Amber gives the colour accent; it is not a separate texture |
| **Hidden structure** | — | No finish work | Material is chosen for strength. The CAD colour only helps tell parts apart |

### Where each texture goes (provisional)

| Texture | Parts |
|---|---|
| Housing grain | Body shell, front and rear service panels, wheel-arch pods, head bezel and camera crown, octagonal skins, rear cover, ear caps, nose touch cap, rear TCRT keel and bezel |
| Metal casing | Wheel rims, clamp rings and hub caps, yaw turntable disc, ear dark centres (blue anodised look, §4), the yoke legs (raw CF) |
| Accent | Wheel-arch trim rings, ear inlays, yoke-leg spine inlays, rear power-button bezel |
| Hidden structure | Chassis frame modules, body frame, compute tray, yaw stage internals, head cradle and pitch frame, wear shoe |

Sections 5–7 confirm each part, including the edge cases: the chassis belly
and keel are seen from low angles, and the turntable disc shows between the
head and the body.

### Weathering: the "used" look

Weathering is optional and comes last, after v1 fits are proven. It is what
makes a Star Wars droid look used rather than new:

- a dark grey **panel wash** into the seams, screw recesses and grille slots;
- a silver **dry-brush** on the edges hands and the floor would wear;
- light **chipping** on the amber trims.

Keep wash and paint off mating faces, bearing seats and the mic ports.
Exposed screws are part of the look (vision: "visibly assembled"). They are
**plain steel** (§4), bright against the matte skins.

### What the CAD can and cannot show

STEP stores only colour and transparency per part, so the viewer cannot show
grain, fuzzy skin or weathering. In the CAD, the finish appears as:

- the **colour** of each part (§4), set to a matte, slightly desaturated
  version of the real filament;
- a **finish note** per part in sections 5–7.

### Mass effect

ASA at 1.07 g/cm³ against the current bases (preliminary; section 8 redoes it
properly):

| Group | Current register | As ASA | Change |
|---|---|---|---|
| Body shell and panels (PETG basis 1.20) | 248.4 g | ~221 g | ~−27 g |
| Head skins, M019a (PLA basis 1.24) | 105.2 g | ~91 g | ~−14 g |

Paint adds a few grams per part. Fuzzy skin changes nothing that matters. The
lighter head helps the pitch and roll servos. Both registers are hand-kept
tables, so neither changes until section 8 updates them.

## 4. Colour scheme

The CAD uses nearly twenty colours today. Most were chosen to tell parts apart
in an inspection view: frame blue, slate, bronze, teal-grey and others. None
of them is a filament anyone has picked. This section replaces them with twelve
real finishes, keeping **ivory and amber** as the droid's identity.

**The scheme in one line:**
- **Body:** an ivory shell with taupe service panels and a taupe rear keel.
- **Head:** ivory.
- **Frames, neck disc and ear centres:** one deep slate blue.
- **Wheels:** a lighter slate blue from the same family.
- **Accents:** amber.
- **Screws:** steel.

### The palette

All hex values are the matte, clean base colour. Weathering (§3) is not
shown in the CAD.

**The cadgen viewer is not a colour reference.** Its cool lighting adds blue
and takes yellow out. The first deep slate (`#4F575B`, saturation 7 %) looked
dark blue there but plain grey in Fusion, and it would have bought grey
filament. The ivory looked cooler in the viewer than it really was.
Sampled pixels, 2026-10-13:

| Part | Viewer | Fusion, before the retune |
|---|---|---|
| Neck disc | `#404D55`, blue | `#3B3C39`, grey |
| Shell | `#A9A794`, cool cream | `#C9BEA0`, warm tan |

So four finishes carry **two values**:

- **Viewer value:** what the text-to-cad presentation model
  (`finish_colours.py` `PALETTE`) uses, tuned by eye in the cadgen viewer.
- **Neutral-light value:** what the Fusion `makad-v1` appearances use, and the
  value to match filament or paint to (`NEUTRAL_LIGHT`).

Judge colour in Fusion, or on a physical swatch. When buying, use the
neutral-light value.

| Name | Hex | Finish (§3) | Used on | How to get it |
|---|---|---|---|---|
| **Ivory** | Viewer `#DDD4BA`; neutral light `#DAD5C3` (a cool cream) | Housing grain | Body shell (with its internal panel frames), wheel-arch pods, every head skin: bezel and crown, octagonal skins, rear cover, ear caps; the nose touch cap | Ivory ASA is uncommon. If the lab has none, print white or light-grey ASA and paint it matte ivory; the weathering needs paint anyway |
| **Taupe** | Viewer `#A9A28E`; neutral light `#9D9886` | Housing grain | Front and rear service panels (with the button well printed in them); the rear TCRT keel and its sensor bezel | Warm taupe or khaki-grey ASA, or primer and taupe paint. Darker panels on the ivory shell (2.0:1) mark them as removable ("visibly assembled"). The keel is PETG, so it needs a taupe PETG or a primer before paint |
| **Amber** | `#B88636` (unchanged) | Accent | Wheel-arch trim rings, ear inlays, yoke-leg spine inlays | Matte ochre or mustard filament, or paint. The parts are small, so paint is easy |
| **Signal amber** | `#D39F36` (unchanged) | Accent | Rear power-button bezel only | Same as amber, lifted toward safety yellow so the red button stands out. Keep it: it is a safety cue, not decoration |
| **Deep slate** | Viewer `#4F575B`; neutral light `#34495C` | Metal casing on visible parts; hidden structure elsewhere | Visible: the yaw turntable disc (the neck), ear dark centres. Hidden: chassis frame modules, motor carriers and plates, bearing housings, battery tub and hatch, ball pod and lid, keel wear shoe and TCRT shims, body frame and foot cassette, compute tray, the whole yaw stage, head cradle, pitch frame, bearing cartridge, display rear frame, ear inner mounts, CSI guide | A very dark blue-grey: one colour ties the frame and neck together. Dark blue-grey PETG (chassis, body) and PLA (head). The visible parts can be painted matte metallic in the same tone |
| **Slate blue** | Viewer `#6F8189`; neutral light `#587A94` | Metal casing | Wheel rims (spokes) and clamp rings | A lighter version of deep slate, so the wheels read as a separate part but stay in the frame's blue family. Blue-grey PETG, or primer and matte metallic paint |
| **Gunmetal** | `#3A464D` (unchanged) | Metal casing | Hub caps | Matte gunmetal or iron-grey metallic filament, or paint. Darker than the slate-blue rim around it |
| **Aluminium** | `#9DA3A6` (new) | Bare metal | The 1.2 mm aluminium axle bearing caps (D-007) | Purchased or cut metal, not printed; hidden behind the wheels |
| **Carbon** | `#2A2C2E` (new) | Raw CF | Yoke legs and their pivot retainer | The CF filament's own colour. Stiff CF grades come only in black, so the legs stay black unless they are painted deep slate |
| **Tyre black** | `#2B3034` (unchanged) | Rubber | Tyres | Black TPU 95A |
| **Brass** | `#C38A47` (the old bronze) | — | Heat-set inserts only | Purchased; no print |

**Visible screws: classic steel**, `#B7BFC0` (the existing `STEEL` colour).
Buy **A2 stainless** button heads rather than zinc-plated: they keep the
bright steel look without rusting in Mumbai humidity. The body and chassis
already draw screws in `STEEL`. The head draws its screws dark (`#555B5A`,
`#535957`), so the presentation view should switch those to steel.

### What changes from today's CAD

| CAD colour today | Hex | Painted on now | Becomes |
|---|---|---|---|
| `IVORY` | `#E3DDC9` | Shell, arch pods, rear panel, head skins, nose cap; also the keel, wear shoe and TCRT bezel | Shell, arch pods, head skins and nose cap stay ivory, retuned to `#DAD5C3`. **Rear panel → taupe.** **Keel and TCRT bezel → taupe**, the panel colour. **Wear shoe → deep slate**: it is the part that drags on the floor and is hidden under the keel |
| `PANEL_WARM_GRAY` | `#C5C0AD` | Front service panel | **Taupe**: the old sand was too close to ivory |
| `SLATE_DARK` | `#707D82` | Shell's internal panel frames; rear button well; yaw gear, pinion, hub and clamp ring | **Panel frames → ivory**: they print as part of the shell (D-045), so they come out in its filament. **Button well → taupe**: it prints with the rear panel. Yaw parts → deep slate |
| `FRAME_BLUE` | `#86A1A8` | Chassis and body frames, carriers, housings, yaw housing and stator; wheel rim and clamp ring | Deep slate; **wheel rim and clamp ring → slate blue** |
| `SLATE` | `#87949A` | Ball pod and lid, battery hatch, chassis rails | Deep slate |
| `BRONZE` | `#C38A47` | Inserts; pinion sprung half; yaw rotor; head pitch frame, bearing cartridge, roll retainers, spine inlays | Inserts stay brass; **spine inlays → amber**; the printed parts → deep slate |
| `COMPUTE_TRAY_COLOR` | `#7A858B` | Compute tray | Deep slate |
| `GUNMETAL` | `#3A464D` | Hub cap | Gunmetal (unchanged) |
| Head `#536B78` | | Yoke legs, pivot retainer | Carbon |
| Head `#647787` | | Turntable disc | Deep slate |
| Head `#718D95`, `#5D6B70`, `#678C81`, `#303A3C` | | Cradle, display rear frame, CSI guide, ear inner mounts | Deep slate |
| Head `#3D484A` | | Ear dark centres | Deep slate |

Purchased parts keep their own colours: the motors, speaker, servos, PCBs, the
red power button, the POM caster ball and the foam gaskets.

### Two-tone parts

Three printed parts carry two colours and need either an AMS (multi-material)
print, a separate part bonded in, or paint:

- **Ears:** an ivory cap with an amber inlay and a deep slate centre. They are
  already modelled as separate solids, so they can be printed separately.
- **Yoke legs:** a carbon leg with an amber spine inlay that is 0.15 mm proud.
  The CAD comment already allows "printed flat in a second colour or the pocket
  can be painted".
- **Rear panel:** taupe, with the signal-amber bezel land. Use an AMS colour
  change on the bezel layers, or mask and paint it.

### Applying it to the CAD

Changing the colour constants in each subsystem model would also change the
inspection views, where the distinguishing colours are useful. So the palette
is applied in one place instead:

- **[`cad/finish_colours.py`](cad/finish_colours.py)** holds the palette above
  and an ordered list of label rules: part label → finish name. Whenever this
  section changes, change that file too.
- **Presentation view** (`makad-v1-presentation.step.py`) applies it while it
  makes every part opaque. A part that no rule matches keeps its model colour.
  That is deliberate for purchased parts: motors, servos, PCBs, the speaker, the
  display, the camera, the button, the fan and the battery.
- **Inspection view** (`makad-v1.step.py`) keeps its distinguishing colours.

Checked on 2026-10-13 against all 2,286 parts in the assembly:

- every printed part matches a rule;
- every rule matches at least one part;
- the brass rule matches only heat-set inserts (and the brass rear-cover
  washers).

The shell's internal panel frames and the rear button well are features of the
shell and panel solids, not separate parts. So they take ivory and taupe
automatically.

**When a subsystem adds or renames a printed part,** add a rule for it here.
Otherwise it shows in its inspection colour, which is a visible miss in a
render.

## 9. Lab-visit checklist

### Answered on 2026-10-28

- **TPU 95A:** offered as lab filament (₹9/g), and the Bambu A1 printers are
  direct drive. The tyre hold on [D-005](../../decisions.md#d-005) can lift
  after one test tyre prints and fits; until then the O-ring fallback stands.
- **CF for the yoke legs ([D-049](../../decisions.md#d-049)):** the lab has a
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

### Still open

- **ASA on the X1E with an own spool:** is the X1E open to students, and is ASA
  allowed?
- **PA-CF on the X-CF Pro:** allowed, given that printer damage is the
  student's responsibility?
- **Slicer:** Bambu Studio or Orca, and can a prepared 3MF project be submitted
  in place of an STL? Fuzzy skin painting and colour assignment live in it.
- **Walls under 1.2 mm:** the head pivot retainer (1.0 mm) and the keel TCRT
  shims (1 mm). Will the lab print them, or do they thicken?
- **Academic status:** which faculty member to CC so own-filament prints are free.
- Filament colours in stock, by brand and material, against the [§4 palette](#4-colour-scheme): ivory or white **ASA** and a warm taupe or khaki-grey **ASA**, matte amber or ochre, a very dark blue-grey (deep slate) in **PETG** and **PLA**, a lighter blue-grey (slate blue) **PETG** for the wheels, taupe **PETG** for the keel, matte gunmetal, black TPU 95A. Take photos next to a printed colour card. Screen hex values are only a guide. Numakers and Polymaker spools were seen on the shelves.
- Heat-set insert tip, a spray area for primer and paint, and use of the
  vacuum former (a possible clear display window, M003).
- Whether any lab on campus has a UTM for the CF modulus coupon.
