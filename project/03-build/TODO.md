# 03-build TODO

| Field | Value |
|---|---|
| Status | **Open.** Started 2026-11-08 for D-093 procurement |
| Register | [BOM.csv](BOM.csv) is the parts record; this list only tracks actions. Tick a box here, then update the row's `procurement` / `received_measurements` |
| Plan | [simplification-plan.md §7](simplification-plan.md#7-levels-of-work) |

## Order

- [ ] **CH-103 balance-tap fuses, 3 + 2 spares.** One per balance wire (B−, mid, B+) at the cell end; the taps bypass the main fuse and PCB-01. Candidate Littelfuse 0251001.MXL (Pico II, 1 A very fast, 125 V AC/DC, 0.128 Ω cold), element14 India / Mouser India. Before ordering, confirm the PD60 balance current is well under 1 A. Can wait for the harness review
- [ ] **BO-068 DIN 9021 M2 washers (Ø6), 8.** Clamp the INMP441 edges under the BO-013 screws. Skip if they came with the screw order
- [ ] **CH-110 non-screw items:** 4 × M2 × 5 F-F round standoffs (S13V30F5 modules) and VHB foam tape. Skip if already in hand

## Order after the 05-harness review (part B)

- [ ] CH-101 XT30U female panel port + XT60→XT30 lead for the PD60
- [ ] CH-102 JST PA 3P balance break (PAP-03V-S / PALR-03VF, pre-crimped SPHD/SPAL AWG24) + JST XH 3P rear balance port (XHP-3, pre-crimped SXH AWG24)
- [ ] Micro-Fit+ 2-way pairs for `J-BAT` and `J-CHASSIS` (206460/215953 series, AWG16); exact gender/key/PN open
- [ ] Micro-Fit 3.0 2-way pairs for `J-S18-H` and `J-S18-Y` (43030/43025 + 43031/43020)
- [ ] Crimp tools (Molex 213309-4400 MF+, 63819-0900 MF3; check PN) or professionally terminated pairs
- [ ] AWG16 UL1061 red/black wire; rated multi-wire AWG16 splices (charge splice, rear ± star, tub branch)
- [ ] Sample each connector first: confirm mate/key, pull-test three per wire/contact combination ([05-harness §9](05-harness/README.md#9-open-and-acceptance))

## On receipt (ordered 2026-11-08)

- [ ] Record seller, price and exact article in `BOM.csv` for CH-021, CH-096–CH-100, CH-104, CH-105, CH-109, CH-110, BO-007, BO-013, BO-016, BO-066, BO-067
- [ ] CH-099 INA226: confirm the shunt is R010 (else fit a loose R010 2512 ≥ 1 W); confirm the I²C address
- [ ] CH-100: note whether the ISDT PD60 or a fallback charger arrived; set LiPo 4.20 V/cell, never LiHV
- [ ] BO-016 adapter: BIS CRS number on the label and a 15 V PDO
- [ ] Measure outlines of M6 (CH-099), M8 (BO-007) and M9 (BO-066) and compare with the D-095 UNMEASURED envelopes
- [ ] CH-039 (old 2 × M2 × 5 IMU screw row): check whether CH-110 covers it, then retire or order
