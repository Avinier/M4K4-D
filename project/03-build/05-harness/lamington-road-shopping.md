# Lamington Road shopping list: harness

| Field | Value |
|---|---|
| Purpose | Harness items still open on 2026-11-21 that are easier to buy in person, plus small parts stuck elsewhere |
| Sources | `BOM.csv` procurement column, [TODO.md](../TODO.md) part B, `final/v1/cad/harness-cut-list.csv` |
| Already ordered (not on this list) | Micro-Fit+ / 3.0 housings and contacts, PH / XH / XT30 (D-123); GH leads and housings (HN-004); WAGO 221-415 (HN-006); zip ties, straps, 15 A fuses, 56 kΩ resistors, cable clips, VHB tape; W47 silicone wire |
| Take with you | **Digital calipers**, this list |

Checks for every wire at the counter: **copper all the way through** (cut a strand; not silver-grey aluminium/CCA), **stranded** (never solid), and the **overall diameter (OD)** within the limit given.

## 1. Must buy

### 1.1 AWG16 thin-wall wire (replaces UL1061, HN-007)

UL1061 is not sold in India in small lengths. The crimped runs go into the Micro-Fit+ 16 AWG contacts (206460-0041 / 215953-0041), which take **insulation OD ≤ 2.0 mm** (rule H-05).

Ask for: **"16 gauge teflon wire"** (PTFE, stranded, 1.3 mm²). If they don't have it: "1.3 sq mm thin-wall / aircraft / MIL wire".

| Runs | Red need (mm) | Black need (mm) |
|---|---:|---:|
| Crimped into Micro-Fit+: W01, W03a, W03a−, W03b, W03r, W05c | 650 | 529 |
| Solder only: W04 (XT30), W05 (M1, M6, stars, − splice) | 308 | 228 |
| **Total need** | **958** | **757** |
| **Buy** | **2 m** | **2 m** |

| Accept | Reject |
|---|---|
| OD 1.8–2.0 mm, 19+ strands, copper (tinned or silver-plated) | OD > 2.0 mm (UL1007 / UL1015 16 AWG are ~2.3 mm), solid core, aluminium, "1.5 sq mm" (usually too thick) |

If only thicker 16 AWG exists, buy **0.5 m red + 0.5 m black** of it for the solder-only runs and keep looking for thin wall for the crimped runs. Do not drop to 18 AWG: the contacts you bought are 16 AWG only.

### 1.2 Pi 5 power lead (HN-010, revised by the other session)

| Item | Need | Buy | Check |
|---|---:|---:|---|
| **Right-angle (up/down-angle) USB-C to USB-A cable, 3 A rated** | 1 | **2** | Angle plug turns the cable **down** when the Pi's USB-C faces sideways; plug body ≤ 13 mm beyond the socket face. It gets cut 40–60 mm behind the C plug; its C-to-A wiring already carries the 56 kΩ CC resistor |

## 2. Wire backup (only if the 2026-11-21 HN-007 order fails)

`BOM.csv` records the rest of HN-007 as ordered on 2026-11-21. If any line doesn't arrive or is out of stock, buy it here:

| Gauge | Buy | OD limit | Ask for |
|---|---|---|---|
| AWG18 | 1.5 m red + 1.5 m black | none (solder/WAGO only) | any flexible copper, silicone or PVC |
| AWG20 | 1.5 m red + 1.5 m black | ≤ 1.85 mm (Micro-Fit 3.0) | UL1007 20 AWG (~1.6 mm) or 20 AWG teflon |
| AWG22 | 2 m red + 2 m black | ≤ 1.85 mm | UL1007 22 AWG (~1.6 mm) |
| AWG24 | 1 m × 3 colours | none | any |
| AWG28 | 2 m of 10-way | ≤ 1.22 mm (C-Grid) / 1.27 mm | **rainbow ribbon cable, 28 AWG stranded, 1.27 mm pitch** (peel 6-way strips for the four mic leads) |

Need totals from the CAD cut list: AWG18 0.69 m per colour, AWG20 0.57 m, AWG22 0.89 m, AWG24 0.3 m (W40), AWG28 7.3 m of conductor (W27 6.9 m + W44/W40 0.4 m).

## 3. While you're there (non-harness parts stuck online)

| Item | BOM | Need | Buy | Check |
|---|---|---:|---:|---|
| M2.5 × 4 brass heat-set insert | CH-080, BO-037 | 8 | **12** | **Must buy**: out of stock online. **OD 3.9 mm** (holes are Ø3.5 pilot). If only another OD exists, note it: the pilots get re-sized |
| M2 × 5 female-female round standoff | CH-110 | 4 | **6** | **Must buy**: out of stock online (builder, 2026-11-21). Round, M2 thread both ends, 5 mm body |

(BO-065 standoffs were ordered from Mouser on 2026-11-20. No punch set: the builder cuts the BO-014 / HD-015 foam discs by hand. No CA gel: BO-052 trims use the CH-112 Araldite.)

## 3a. Yaw preload torsion spring (BO-048): get it wound in Mumbai

Custom part; off-the-shelf kits have sideways (tangential) legs and will not fit. Spring winders cluster around **CP Tank / Girgaon**, a short walk from Lamington Road. [Dchel Springs](https://dchelsprings.com/torsion-spring-manufacturer-india.php), Office 1401, Anapurna Sadan, VP Road, CP Tank, Mumbai 400004, +91 86579 11405, sales@dchelsprings.com. Phone first and ask whether they wind 10 pieces. If not, ask them (or any shop on Lamington Road) for the nearest small-quantity spring winder.

| Parameter | Value |
|---|---|
| Type | Torsion spring, close-wound, **both legs straight axial** (parallel to the coil axis) |
| Wire | **1.2 mm music wire** (IS 4454 Gr 3 / ASTM A228) |
| Outer diameter | **8.0 mm** (ID 5.6 mm; rides on the Ø5 pinion shaft) |
| Active coils | **4**; body length about 6 mm |
| Legs | 4 mm long each, at the coil OD; **0° free angle** (legs in line) |
| Rate | about **4.2 N·mm per degree** (0.23–0.25 N·m/rad); 3.8–4.6 is acceptable |
| Working deflection | about 55° (0.22 N·m preload) |
| Quantity | **10: 5 left-hand + 5 right-hand wound** (the right hand is whichever closes the coil under preload) |
| Finish | Plain or black oxide |

Show them this, or say it:

> Custom torsion spring, 10 pcs (5 left-hand + 5 right-hand). Music wire 1.2 mm, OD 8.0 mm, 4 coils, close-wound. Both legs straight axial, 4 mm long, legs in line. Rate about 4.2 N·mm per degree, working angle 55°. Plain finish.

At pickup: OD 7.9–8.1 mm with calipers, the coil slides over a 5 mm rod (bring an offcut of the 5 mm D-shaft or a 5 mm drill bit), both legs straight and parallel to the axis, no cracks at the leg bends. After it arrives, the printed collar and sprung pinion half get Ø1.4 mm leg holes (small CAD edit).

## 4. Totals

| Line | Buy |
|---|---|
| AWG16 teflon, OD 1.8–2.0 mm | 2 m red + 2 m black = **4 m** |
| Right-angle USB-C to USB-A cable, 3 A | **2** |
| M2.5 × 4 inserts OD 3.9 / M2 × 5 F-F standoffs | **12 / 6** |
| BO-048 torsion spring, custom wound (CP Tank) | **10** (5 LH + 5 RH) |
| Backup wire (section 2) | only for lines the online order misses |

## 5. After the trip

Report back so `BOM.csv` and TODO can be updated (HN-007, HN-010, CH-080, BO-037, CH-110, BO-048):

- [ ] Spring: shop name, quoted rate, price, delivery date, measured OD and leg length

- [ ] AWG16: measured OD, strand count, plating, price
- [ ] USB-C cable: measured plug body length beyond the socket face and the angle direction
- [ ] What wasn't found
