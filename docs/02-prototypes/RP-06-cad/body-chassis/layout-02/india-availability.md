# Layout 02 SKU availability in India — 2026-09-26

Checked with Exa web search against the SKUs named in `body_chassis_model.py`, `README.md`, `brief.md` and `RP-02-electrical/board-specs.md`. Stock and prices are a snapshot and change daily. This is a sourcing check, not a purchase decision; the gearmotor lock stays in `../../../RP-03-locomotion/gearmotor-sku-decision.md`.

| Part | India status | Best source and price |
|---|---|---|
| **Raspberry Pi 5 (8 GB)** | Available | Robocraze (authorised seller) ₹19,999–21,999; Hubtronics ₹20,349; Silverline ₹16,825 |
| **Pi 5 Active Cooler** | Available | Probots ₹749 (in stock), Robocraze ₹529, ThinkRobotics ₹600 |
| **ESP32-S3-DevKitC-1-N8** | Available | Tech Depot ₹2,274 (in stock), Sharvi ₹2,080, Amazon.in. Some listings are out of stock. |
| **Pololu DRV8874 carrier 4035** | Available | Fab.to.Lab, The Engineer Store, and TME India as a distributor |
| **Pololu 1" ball caster 2691** | Available | Fab.to.Lab (in stock), MG Super Labs ₹399 |
| **Sharp GP2Y0A41SK0F** | Available | Makestore ₹550 (3 in stock), Techtonics ₹549. Some stockists are sold out. |
| **Samsung INR18650-25R** | Available | Hubtronics/rareComponents ₹588 (in stock), Batteryworks ₹699. Fakes are common; only buy from these tested sellers. |
| **Robotis XC330-M181-T** | Available | MG Super Labs ₹11,459 (listed, stock not stated). The alternative is Robotis direct, $89.90 plus duty. |
| **IDEC XW1E-BV402M-R** | Import only | Industrybuying, "ships within 15 days", imported via Newark |
| **Littelfuse ATO FLR holder 178.6165.0001** | Import only | Industrybuying, "ships within 30 days", imported via Farnell |
| **Littelfuse ATOF 15 A fuse 0287015.L** | Not verified | I found only Littelfuse and overseas listings. |
| **Anderson SBS Mini (B02265G1, 261G3-LPBK)** | Not verified | Anderson has an India page and IDEAL Industries India (Gurgaon) is its local entity, but I found no stockist. |
| **Bourns AC72ABD** | Not verified | Only Chinese brokers list the 72 °C variant. The Indian listing is the AC90ABD, which is a different trip temperature and ships in 45 days. |
| **Visaton K 50 WP 8 Ω** (speaker, 2026-09-26 selection) | Available | Tanotis (Bangalore, element14 reseller) lists art. 2915; EU stock: Schukat 92 pcs, SoundImports €5.74 |
| **MAX98357A** (amp) | Available | Common as Adafruit #3006-class breakouts in Indian stores (bench); the installed TQFN part goes on `PCB-05` via LCSC/JLCPCB |
| **ADAU7002ACBZ-R7** (PDM→I²S) | Import (PCBA) | LCSC C481886, 8-ball WLCSP, about 147 in stock at US$4.10; JLCPCB-assembled only, no Indian breakout found |
| **Infineon IM73D122V01** (mics) | Import | Infineon "active and preferred"; `KIT_IM73D122V01_FLEX` DigiKey US$75.19, 0 in stock, restock 2026-10-19 (standard lead 97 weeks); reels are 5000, so buy cut tape via DigiKey/Mouser India or let JLCPCB source it |
| **Worldsemi WS2812B-2020** (status LED) | Import (PCBA) | LCSC C965555; for the 5 × 5 mm `PCB-08` carrier |
| **ICM-42688-P** (IMU, bare) | Available | Robu ₹314 (bare LGA, for `PCB-07`); RS India ₹755 each in a pack of 2. MIKROE-4237 bench board: MikroE and DigiKey out of stock, TME US$36.25, RS UK restocking |
| **NFP-JGA25-370-EN-0685 gearmotor** | No India source | This matches `gearmotor-sku-decision.md`: the lock is open and no India stock is verified. |

## Notes

- **Gearmotor:** the real blocker. The `-0685` 242 rpm winding has no Indian listing, and the vendor's checkout only offers the 170 rpm variant. The ThinkRobotics family page is not proof of stock for that winding. The plan in `gearmotor-sku-decision.md` stands: get a written import quote or pick a local alternative.
- **IMU:** resolved 2026-09-26 by putting the bare chip on its own `PCB-07` board (`../../peripheral-selection.md` §4), not on `PCB-04`, to keep it off the converters' heat and on the base frame.
- **Power-board parts:** the SBS Mini, ATOF fuse and AC72ABD come up short. Get quotes from Mouser India, DigiKey India (which `board-specs.md` already says ships) or Element14 India before treating them as sourced. If the AC72ABD proves hard to get, a different trip temperature changes the thermal cutoff design.
- **Not searched:**
  - The 608ZZ bearings, the TCRT5000 module and the DevKitC-adjacent generics (all common in India).
  - The head parts (display, C2), which come from RP-01 Layout 04 rather than this layout.
  - ~~The audio parts~~: checked 2026-09-26 with the selection (rows above).
