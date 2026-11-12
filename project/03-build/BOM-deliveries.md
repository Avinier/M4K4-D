# Delivered parts record

This file lists parts that have physically arrived and maps each one to its row in the [project BOM](BOM.csv). `BOM.csv` is still the parts register. Its `procurement` and `received_measurements` columns are updated in one pass when Level 6 closes ([simplification-plan.md](simplification-plan.md)). Until then, this file is the receipt record.

"Delivered" means the builder confirmed the parcel arrived. It does not mean the part has been measured, fitted or tested. Those checks stay open in each BOM row's `release_check`.

## 2026-11-12: six orders, 26 lines

Source: the builder's summary of supplier emails and delivery confirmations, pasted 2026-11-12.

### ThinkRobotics: TR66306, TR66406

| Article | Qty | BOM row | Note |
|---|---:|---|---|
| 25 mm DC metal encoder gearmotor, 6 V, 230 RPM | 2 | CH-014 | Already recorded as received 2026-11-01 |
| Jetson Nano 4020 cooling fan, 5 V, 4-pin, reverse-proof | 1 | none (see [problem 1](#problems)) | Accidental purchase; not selected for Makad |
| Raspberry Pi 5, 2 GB | 1 | BO-034 | |

### OnlyScrews: ONLSCR63381ze

This is the order pasted on 2026-11-01 and reconciled in [04-print hardware-order.md](../04-print/01-chassis/hardware-order.md).

| Article | Qty | BOM rows | Demand vs stock |
|---|---:|---|---|
| M2 × 4 Phillips pan head SS304 | 15 | CH-110 (4, S13V30F5 standoffs), CH-086 PCB-12 (2), CH-111 PCB-16 (2) | 8 used, 7 spare; see [problem 4](#problems) |
| M3 × 16 Phillips countersunk SS304 | 5 | none assigned | Spare |
| M2.5 × 6 Phillips round-head laptop screw | 15 | CH-081 (4), BO-036 (4) | 8 used, 7 spare |
| Brass threaded inserts, size garbled in the summary | 10 | possibly CH-080 + BO-037 (M2.5 × 4, 8) | **Size to confirm** |
| M3 × 8 Phillips pan head SS304 | 20 | none assigned | Spare |
| M3 × 16 Allen button head SS304 | 15 | CH-053 (8), CH-109 (2), BO-027 (2), BO-029 (4) | 16 needed: **1 short** |
| 8-grid screw storage box | 1 | none | Tooling |
| M4 × 12 Allen button head SS304 | 25 | CH-035 (4) | OK |
| M3 × 12 Phillips countersunk, black-oxide steel | 25 | CH-038 (2) | OK |
| Ø4 × 8 hardened dowel pin | 8 | CH-037 (2) | OK |
| M3 × 6 slant-knurled brass insert | 15 | CH-033/061/063/067/077 (21), BO-028/030/039/063 (17) | 38 needed: **23 short**, unless the earlier M3 × 6 plain stock covers it |
| M3 × 4 slant-knurled brass insert | 35 | CH-049 (12), CH-054 (8), BO-011 (6), BO-060 (3), HD-013 (1) | 30 needed: OK |
| M3 × 6 Allen button head SS304 | 15 | CH-030 (4), CH-056 (6), CH-076 (4), CH-109 (2), BO-060 (3), HD-005 (4) | 23 needed: **8 short** |
| M3 × 8 Allen button head SS304 | 40 | CH-031 (3), CH-032 (2), CH-048 (12), CH-060 (8), CH-109 (2), BO-010 (6), BO-038 (3), BO-031 (8 if button head) | 36–44 needed: **up to 4 short** |
| Ø3 × 1.5 mm N35 disc magnet | 1 | CH-065 | OK |
| 688 ZZ bearing, 8 × 16 × 5 mm | 25 | CH-015 (4) | OK; already recorded as received 2026-11-01 |

### Order 389404 (supplier not named in the summary)

| Article | Qty | BOM row | Note |
|---|---:|---|---|
| TCRT5000 IR sensor, pack of 5 | 5 | CH-020 (1) | 4 spare |
| Sharp GP2Y0A21YK0F | 1 | CH-018 | |

### Robu: 3787165

| Article | Qty | BOM row | Note |
|---|---:|---|---|
| Samsung INR18650-25R, 2500 mAh | 3 | CH-022 (2) | 1 spare |
| BF-013A fuse holder | 4 | not in the design (CH-028 is the 0FHA0001ZXJ) | See [problem 2](#problems) |
| Littelfuse 0287005.PXCN, 5 A, 32 V ATO fuse | 5 | CH-029, chassis-test alternative only | See [problem 2](#problems) |
| EVA foam tape, 50 mm × 5 m | 1 roll | CH-079 | Thickness not stated; the row needs 1.5 mm |

### MG Super Labs: 23718

| Article | Qty | BOM row | Note |
|---|---:|---|---|
| Pololu #2691 ball caster, 1-inch plastic ball | 1 | CH-016 | |

## Not delivered

| Supplier | Article | Qty | Status | BOM consequence |
|---|---|---:|---|---|
| Tanotis | 16 mm red metal mushroom-head pushbutton | 1 | Pending | BO-018 |
| Fab.to.Lab | Adafruit #3297 DRV8833 breakout | 2 | **Payment failed** | CH-017 has no order. Reorder; the base cannot drive without it |
| element14 | Infineon IM73D122V01XTMA1 PDM mic | 4 | Cancelled | Fine: BO-012 is `SUPERSEDED` (D-093) |
| element14 | ADAU7002ACBZ-R7 | 4 | Cancelled | Fine: BO-004 is `SUPERSEDED` (D-093) |
| element14 | Visaton K 50 WP 2915 speaker | 1 | Cancelled | **BO-001 is still needed** and now has no source |

These items were reported ordered on 2026-11-08 but are not in this delivery: Adafruit #4438 IMU (CH-021), MAX98357A breakouts (BO-007), INMP441 × 5 (BO-066), USB-C PD adapter (BO-016), Pololu #2813 (CH-096), #2572 × 2 (CH-097), #4082 × 2 (CH-098), INA226 (CH-099), ISDT PD60 (CH-100), VM protection set (CH-104) and the SS34 Schottky (CH-105).

## Problems

1. **The Jetson Nano 4020 fan was bought accidentally and is not a Makad part.** The builder will obtain the selected official Pi 5 Active Cooler (BO-035). The Jetson fan lacks the Pi-specific heatsink and mount, and its 40 × 40 × 20 mm envelope does not fit the current compute bay without redesign. It also does not replace the BO-040 3010 enclosure fan. Keep this line as a receipt record only; do not substitute it into BO-035 or the CAD.
2. **The fuse and holder are for testing only.** CH-029 lists the 0287005.PXCN 5 A fuse only as a "chassis-test evaluation alternative". It is fine for a chassis-only bench run (two gearmotors at about 1.8 A stall each). It is not the full-system fuse, because coincident demand is about 16 A, so a 15 A ATOF is still needed. D-018 records that "BF-013A compatibility is not established". The CAD fuse shelf (X 52–82, Y 39–49, Z 73–99) is sized for the 0FHA0001ZXJ (about 30 × 10 × 26 mm), so measure a BF-013A against that envelope. If it fits, it can replace CH-028, which has no India source. Only one holder and one fuse are installed; the rest are spares. These ATO fuses are not the CH-103 cell-end balance-tap fuses, which need about 1 A very-fast fuses.
3. **Some OnlyScrews stock falls short.** The order is short of M3 × 6 slant inserts (23), M3 × 6 button head (8), M3 × 8 button head (up to 4) and M3 × 16 button head (1). See the table above.
4. **The M2 × 4 screws are machine screws.** They fit the joints that go into metal threads: the S13V30F5 standoffs and the PCB-12/PCB-16 inserts. PCB-12/16 were modelled with ISO 7380 button heads (Ø3.5 × 1.1). Check the pan head (about Ø3.8 × 1.3) against the PCB-16 clearance, which is 0.3 mm at the leg foot. The direct-to-PETG M2 × 4 joints still need thread-forming screws: BO-013 mics (8) and the CH-110 audio hub (2). BO-048 still needs one M2 × 4 countersunk screw.
5. **The supplier summary has gaps.** The insert line's size is garbled, and order 389404 has no supplier name. Confirm both from the order emails.
